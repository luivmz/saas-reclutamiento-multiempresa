<?php

namespace App\Console\Commands;

use App\Services\Ml02\Bm25Retriever;
use App\Services\Ml02\LexicalSearch;
use Illuminate\Console\Command;

/**
 * EXPERIMENTAL ML-02. Runs the SAME classes the evidence page uses (Bm25Retriever, LexicalSearch) over the F38
 * synthetic set and writes the output format of the F38 harness (`f38_evaluar.py`), for one partition at a time.
 * It reads no database and no real data. The harness, not this command, computes the metrics.
 *
 *   php artisan ml02:evaluar --particion=dev --metodo=bm25 --salida=storage/app/ml02/dev_bm25.json
 *
 * --metodo=bm25    EI-09 with BM25 (EXP-BM25-LEXICO-v1) and EI-07 with exact search.
 * --metodo=exacta  baseline of F38 §6.6: EI-09 with «any content word of the criterion», in identifier order.
 */
class Ml02Evaluate extends Command
{
    protected $signature = 'ml02:evaluar
        {--particion=dev : dev o test}
        {--metodo=bm25 : bm25 o exacta}
        {--salida= : archivo JSON de salida}
        {--conjunto=docs/academico/preparacion-f38-ml02/conjunto/ml02_casos_sinteticos.json : conjunto sintético F38}';

    protected $description = 'EXPERIMENTAL: ejecuta la ayuda documental ML-02 sobre el conjunto sintético F38 y escribe la salida para su arnés';

    public function handle(Bm25Retriever $bm25, LexicalSearch $search): int
    {
        $partition = (string) $this->option('particion');
        $method = (string) $this->option('metodo');

        if (! in_array($partition, ['dev', 'test'], true) || ! in_array($method, ['bm25', 'exacta'], true)) {
            $this->error('Partición admitida: dev o test. Método admitido: bm25 o exacta.');

            return self::INVALID;
        }

        $set = json_decode((string) file_get_contents(base_path((string) $this->option('conjunto'))), true, flags: JSON_THROW_ON_ERROR);
        $vacancies = array_flip($set['partitions'][$partition]);
        $vacancyOf = array_column($set['applications'], 'vacancy', 'token');
        $inPartition = fn (string $application) => isset($vacancies[$vacancyOf[$application] ?? '']);

        $criteria = [];
        foreach ($set['vacancies'] as $vacancy) {
            foreach ($vacancy['criteria'] as $criterion) {
                $criteria[$criterion['id']] = $criterion['text'];
            }
        }

        $fragmentsOf = fn (string $application) => array_column(
            array_values(array_filter($set['fragments'], fn (array $f) => $f['application'] === $application)),
            'text',
            'id',
        );

        $ei07 = [];
        foreach ($set['tasks']['EI-07']['queries'] as $query) {
            if ($inPartition($query['application'])) {
                $ei07[] = [
                    'query' => $query['id'],
                    'fragments' => $search->search($query['query'], $fragmentsOf($query['application']), $query['mode']),
                ];
            }
        }

        $k = (int) $set['tasks']['EI-09']['k'];
        $pairs = [];
        foreach ([...$set['tasks']['EI-09']['annotations'], ...$set['tasks']['EI-09']['no_evidence_cases']] as $row) {
            if ($inPartition($row['application'])) {
                $pairs[$row['application'].'|'.$row['criterion']] = [$row['application'], $row['criterion']];
            }
        }
        ksort($pairs);

        $ei09 = [];
        foreach ($pairs as [$application, $criterion]) {
            $refs = $method === 'bm25'
                ? array_column($bm25->retrieve($criteria[$criterion], $fragmentsOf($application), $k)['hits'], 'id')
                : $search->anyContentWord($criteria[$criterion], $fragmentsOf($application), $k);

            $ei09[] = ['application' => $application, 'criterion' => $criterion, 'fragment_refs' => $refs, 'abstained' => $refs === []];
        }

        $output = [
            'set_id' => $set['set_id'],
            'method_id' => $method === 'bm25' ? Bm25Retriever::METHOD_ID : 'EXP-LINEA-BASE-EXACTA-v1',
            'outputs' => ['EI-07' => $ei07, 'EI-09' => $ei09],
        ];

        $json = json_encode($output, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_THROW_ON_ERROR)."\n";
        $target = $this->option('salida');

        if ($target) {
            $path = str_starts_with((string) $target, '/') ? (string) $target : base_path((string) $target);
            @mkdir(dirname($path), 0775, true);
            file_put_contents($path, $json);
            $this->info("Salida escrita en {$target} (SHA-256 ".hash('sha256', $json).').');
        } else {
            $this->output->write($json);
        }

        return self::SUCCESS;
    }
}
