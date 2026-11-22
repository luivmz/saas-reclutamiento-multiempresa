<?php

namespace Tests\Feature\Concurrency;

use App\Enums\EvidenceSource;
use App\Enums\EvidenceType;
use App\Enums\VacancyStatus;
use App\Exceptions\BusinessRuleException;
use App\Models\Application;
use App\Models\AuditLog;
use App\Models\EvaluationCriterion;
use App\Models\EvidenceEvent;
use App\Models\EvidenceItem;
use App\Models\Organization;
use App\Models\User;
use App\Models\Vacancy;
use App\Services\Evidence\EvidenceService;
use App\Services\Selection\FinalDecisionService;
use App\Services\Selection\SelectionRegistrationService;
use Illuminate\Auth\Access\AuthorizationException;
use Illuminate\Contracts\Process\InvokedProcess;
use Illuminate\Database\Connection;
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Process;
use Illuminate\Support\Str;
use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\Attributes\Group;
use Tests\Concerns\BuildsRankingScenario;
use Tests\TestCase;

/**
 * APP-M01 (Codex, 10/11/2026), EXPERIMENTAL evidence flow: a write already authorized while the vacancy was open
 * must not be committed after the closure of that vacancy (R-08). Real PHP processes, separate PostgreSQL connections
 * and the real services, with the coordination method of SEG-02 (DecisionStageConcurrencyTest): a barrier connection
 * holds a lock that the held worker only meets after its own checks; pg_stat_activity and pg_blocking_pids confirm
 * where it waits; then the second worker runs. If the second one finishes while the first is held, its commit came
 * first; if it waits on a lock of the first one, the runtime serializes them.
 *
 *  - Write held, closure arrives: the barrier is an ACCESS EXCLUSIVE lock on the evidence table the write touches
 *    after its checks. The closure never reads those tables.
 *  - Closure held, write arrives (control): the barrier is an ACCESS EXCLUSIVE lock on selection_decisions, which the
 *    closure reads after locking the vacancy. The evidence writes never read that table.
 *
 * Fixtures are committed so the workers can see them: no RefreshDatabase. Only the isolated test database is used,
 * and it is left freshly migrated.
 */
#[Group('app-m01')]
class EvidenceClosureConcurrencyTest extends TestCase
{
    use BuildsRankingScenario;

    private const WORKER = __DIR__.'/Support/evidence-worker.php';

    private const TEST_DATABASE = 'reclutamiento_testing';

    private const EXPECTED_REJECTIONS = [BusinessRuleException::class, AuthorizationException::class];

    private Organization $organization;

    private User $hr;

    private Vacancy $vacancy;

    private Application $chosen;

    private EvaluationCriterion $criterion;

    private EvidenceItem $item;

    private string $run = '';

    /** @var array{database: string, server: string, server_started: string, isolation: string} */
    private array $server = [];

    private ?Connection $barrier = null;

    /** @var list<InvokedProcess> */
    private array $processes = [];

    /** @var list<array<string, mixed>> */
    private array $timeline = [];

    protected function setUp(): void
    {
        parent::setUp();

        config()->set('experimental.evidencias', true);
        $this->assertSame(self::TEST_DATABASE, DB::connection()->getDatabaseName(), 'ENTORNO: la conexión no apunta a la base de pruebas aislada.');
        $this->server = $this->serverOf(DB::connection());
        Artisan::call('migrate:fresh', ['--force' => true]);

        $this->run = Str::lower(Str::random(6));
        $this->organization = Organization::factory()->create();
        $this->hr = User::factory()->hr($this->organization)->create();
        $approver = User::factory()->approver($this->organization)->create();
        $this->vacancy = Vacancy::factory()->for($this->organization)->configured()->published()->create();
        $this->chosen = $this->candidateWithScores($this->vacancy, 18, 16, 17);
        $this->candidateWithScores($this->vacancy, 20, 10, 19);
        $this->criterion = EvaluationCriterion::query()->withoutGlobalScopes()->where('vacancy_id', $this->vacancy->id)->orderBy('position')->firstOrFail();

        // Committed preconditions of the closure (RF-23 and RF-24) and one evidence record on the selected application.
        Auth::setUser($approver);
        app(FinalDecisionService::class)->decide($this->vacancy, $approver, $this->chosen->id, 'APP-M01 decisión ficticia registrada para la prueba de concurrencia.');
        Auth::setUser($this->hr);
        app(SelectionRegistrationService::class)->register($this->vacancy->fresh(), $this->hr);
        $this->item = app(EvidenceService::class)->register($this->hr, $this->chosen->fresh(), EvidenceType::Certificate,
            EvidenceSource::SubmittedDocument, '[SINTÉTICO] Certificado ficticio previo a la prueba de concurrencia.');
        Auth::logout();
    }

    protected function tearDown(): void
    {
        foreach ($this->processes as $process) {
            if ($process->running()) {
                $process->signal(9);
            }
        }

        if ($this->barrier !== null) {
            if ($this->barrier->transactionLevel() > 0) {
                $this->barrier->rollBack();
            }
            DB::purge('evd01_barrier');
        }

        foreach ($this->backends() as $pid) {
            DB::select('select pg_terminate_backend(?)', [$pid]);
        }

        Artisan::call('migrate:fresh', ['--force' => true]);

        parent::tearDown();
    }

    /**
     * @return array<string, array{string, string}>
     */
    public static function writes(): array
    {
        return [
            'registrar' => ['register', 'evidence_items'],
            'enlazar' => ['link', 'evidence_events'],
            'desenlazar' => ['unlink', 'evidence_events'],
            'revisar' => ['review', 'evidence_events'],
            'corregir' => ['correct', 'evidence_events'],
            'retirar' => ['withdraw', 'evidence_events'],
        ];
    }

    /**
     * The write passed its policy check with the vacancy open and is held before touching the evidence tables; the
     * closure arrives. Valid outcomes: the closure waits for the write (write, then closure), or the write is
     * rejected after the closure commits. Never a write committed after the closure.
     */
    #[DataProvider('writes')]
    public function test_app_m01_write_authorized_before_the_closure_is_not_committed_after_it(string $operation, string $table): void
    {
        if ($operation === 'unlink') {
            Auth::setUser($this->hr);
            app(EvidenceService::class)->link($this->hr, $this->item, $this->criterion->id);
            Auth::logout();
        }
        $before = $this->counts();

        $race = $this->race("lock table {$table} in access exclusive mode", ["\"{$table}\""],
            first: ['W', $operation, $this->writePayload()],
            second: ['C', 'close', ['actor' => $this->hr->id, 'vacancy' => $this->vacancy->id]],
        );
        $this->report("APP-M01 · {$operation} retenida tras su autorización; llega el cierre", $race);

        $this->assertSame('ok', $race['second']['outcome'], 'El cierre (RF-25) debe completarse.');
        $this->assertSame(VacancyStatus::Closed, $this->vacancy->fresh()->status);

        if ($race['serialized']) {
            $this->assertSame('ok', $race['first']['outcome'], 'Orden válido: la escritura se confirmó antes del cierre que la esperó.');
        } else {
            $this->assertSame('rejected', $race['first']['outcome'],
                "APP-M01 (R-08): el cierre se confirmó mientras {$operation} esperaba y, aun así, la escritura se aplicó después.");
            $this->assertSame($before, $this->counts(), 'Una escritura rechazada no deja evidencias, eventos ni auditoría.');
        }
    }

    /**
     * Control: the closure holds the vacancy lock and the write arrives. It must wait for the closure, not deadlock,
     * and then be rejected because the evidence is frozen.
     */
    #[DataProvider('writes')]
    public function test_app_m01_write_that_arrives_during_the_closure_waits_and_is_rejected(string $operation, string $table): void
    {
        if ($operation === 'unlink') {
            Auth::setUser($this->hr);
            app(EvidenceService::class)->link($this->hr, $this->item, $this->criterion->id);
            Auth::logout();
        }
        $before = $this->counts();

        $race = $this->race('lock table selection_decisions in access exclusive mode', ['"selection_decisions"'],
            first: ['C', 'close', ['actor' => $this->hr->id, 'vacancy' => $this->vacancy->id]],
            second: ['W', $operation, $this->writePayload()],
        );
        $this->report("APP-M01 · el cierre retiene la vacante; llega {$operation}", $race);

        $this->assertSame('ok', $race['first']['outcome']);
        $this->assertTrue($race['serialized'], "La escritura {$operation} debía esperar el bloqueo de la vacante que tiene el cierre.");
        $this->assertSame(BusinessRuleException::class, $race['second']['class'], 'Tras el cierre, la evidencia queda congelada (R-08).');
        $this->assertSame($before, $this->counts());
    }

    /**
     * @return array<string, int>
     */
    private function writePayload(): array
    {
        return ['actor' => $this->hr->id, 'application' => $this->chosen->id, 'evidence' => $this->item->id, 'criterion' => $this->criterion->id];
    }

    /**
     * @return array{items: int, events: int, audit: int}
     */
    private function counts(): array
    {
        return [
            'items' => EvidenceItem::query()->withoutGlobalScopes()->count(),
            'events' => EvidenceEvent::query()->withoutGlobalScopes()->count(),
            'audit' => AuditLog::query()->withoutGlobalScopes()->where('auditable_type', 'evidence_item')->count(),
        ];
    }

    /**
     * @param  list<string>  $waitsIn
     * @param  array{0: string, 1: string, 2: array<string, mixed>}  $first
     * @param  array{0: string, 1: string, 2: array<string, mixed>}  $second
     * @return array{first: array<string, mixed>, second: array<string, mixed>, serialized: bool}
     */
    private function race(string $barrier, array $waitsIn, array $first, array $second): array
    {
        config(['database.connections.evd01_barrier' => config('database.connections.pgsql')]);
        $this->barrier = DB::connection('evd01_barrier');
        $this->assertSame($this->server, $this->serverOf($this->barrier), 'ENTORNO: la barrera no apunta a la base de pruebas aislada.');
        $this->barrier->statement('set application_name = '.$this->barrier->getPdo()->quote("evd01-{$this->run}-barrier"));
        $barrierPid = (int) $this->barrier->selectOne('select pg_backend_pid() as pid')->pid;

        $this->barrier->beginTransaction();
        $this->barrier->statement($barrier);
        $this->event('orchestrator', 'barrier-locked', ['pid' => $barrierPid, 'sql' => $barrier]);

        $firstProcess = $this->startWorker(...$first);
        $firstPid = $this->waitUntilBlocked($firstProcess, $first[0], $barrierPid, $waitsIn);
        if ($first[1] !== 'close') {
            $this->assertStringContainsString('"event":"authorized"', $firstProcess->output(),
                'ORQUESTACIÓN: la escritura retenida tiene que haber superado ya su autorización (vacante abierta).');
        }

        $secondProcess = $this->startWorker(...$second);
        $serialized = $this->secondWaitsOnFirst($secondProcess, $second[0], $barrierPid, $firstPid);

        $this->barrier->commit();
        $this->event('orchestrator', 'barrier-released');
        $firstProcess->wait();
        $secondProcess->wait();

        $race = ['first' => $this->collect($first[0], $firstProcess), 'second' => $this->collect($second[0], $secondProcess), 'serialized' => $serialized];

        DB::purge('evd01_barrier');
        $this->barrier = null;
        $deadline = hrtime(true) + 5 * 1_000_000_000;
        while (($left = $this->backends()) !== [] && hrtime(true) < $deadline) {
            usleep(20_000);
        }
        $this->assertSame([], $left, 'RECURSOS: siguen abiertas conexiones de la prueba.');

        return $race;
    }

    /**
     * @param  list<string>  $waitsIn
     */
    private function waitUntilBlocked(InvokedProcess $process, string $label, int $barrierPid, array $waitsIn): int
    {
        $deadline = hrtime(true) + 30 * 1_000_000_000;

        while (hrtime(true) < $deadline) {
            if (! $process->running()) {
                $this->fail("ORQUESTACIÓN: {$label} terminó sin quedar bloqueado por la barrera.\n".$process->output().$process->errorOutput());
            }

            $row = $this->activityOf($label);

            if ($row?->wait_event_type === 'Lock' && in_array($barrierPid, $this->pids($row->blockers), true)) {
                foreach ($waitsIn as $fragment) {
                    $this->assertStringContainsString($fragment, (string) $row->query, "ORQUESTACIÓN: {$label} espera la barrera en una sentencia inesperada.");
                }
                $this->event('orchestrator', 'observed-blocked', ['process' => $label, 'query' => Str::limit((string) $row->query, 140)]);

                return (int) $row->pid;
            }

            usleep(20_000);
        }

        $this->fail("ORQUESTACIÓN: {$label} no quedó bloqueado por la barrera en 30 s.");
    }

    private function secondWaitsOnFirst(InvokedProcess $process, string $label, int $barrierPid, int $firstPid): bool
    {
        $deadline = hrtime(true) + 60 * 1_000_000_000;

        while ($process->running()) {
            $row = $this->activityOf($label);
            $blockers = $row?->wait_event_type === 'Lock' ? $this->pids($row->blockers) : [];

            if (in_array($firstPid, $blockers, true)) {
                $this->event('orchestrator', 'observed-serialized', ['process' => $label, 'query' => Str::limit((string) $row->query, 140)]);

                return true;
            }

            if (in_array($barrierPid, $blockers, true)) {
                $this->fail("ORQUESTACIÓN: {$label} espera la barrera; el escenario no fuerza el orden buscado.");
            }

            if (hrtime(true) > $deadline) {
                $this->fail("ENTORNO: {$label} no terminó en 60 s.");
            }

            usleep(20_000);
        }

        return false;
    }

    private function startWorker(string $label, string $operation, array $payload): InvokedProcess
    {
        $process = Process::path(base_path())
            ->env([
                'APP_ENV' => 'testing', 'DB_CONNECTION' => 'pgsql', 'DB_DATABASE' => self::TEST_DATABASE, 'DB_URL' => '',
                'CACHE_STORE' => 'array', 'QUEUE_CONNECTION' => 'sync', 'SESSION_DRIVER' => 'array', 'MAIL_MAILER' => 'array',
                'BROADCAST_CONNECTION' => 'null', 'E2E_ENABLED' => 'false', 'EXPERIMENTAL_EVIDENCIAS' => 'true',
            ])
            ->timeout(120)
            ->start([PHP_BINARY, self::WORKER, $label, $operation, json_encode($payload + ['application_name' => "evd01-{$this->run}-{$label}"])]);

        $this->processes[] = $process;
        $this->event('orchestrator', 'started', ['process' => $label, 'operation' => $operation]);

        return $process;
    }

    /**
     * @return array{outcome: string, value: mixed, class: string|null, message: string|null}
     */
    private function collect(string $label, InvokedProcess $process): array
    {
        $output = $process->output();
        $events = array_values(array_filter(array_map(fn (string $line) => json_decode($line, true), preg_split('/\R/', trim($output)) ?: [])));
        array_push($this->timeline, ...$events);
        $config = collect($events)->firstWhere('event', 'config');
        $result = collect($events)->firstWhere('event', 'result');

        if ($config === null || $result === null) {
            $this->fail("ENTORNO: el worker {$label} no confirmó su configuración o su resultado.\n{$output}\n{$process->errorOutput()}");
        }

        $this->assertSame(
            ['testing', $this->server['database'], $this->server['server'], $this->server['server_started'], $this->server['isolation']],
            [$config['env'], $config['database'], $config['server'], $config['server_started'], $config['isolation']],
            "ENTORNO: la configuración efectiva del worker {$label} no es la de la base de pruebas aislada.",
        );

        if ($result['outcome'] === 'rejected' && ! in_array($result['class'], self::EXPECTED_REJECTIONS, true)) {
            $this->fail("ENTORNO O PRUEBA: el worker {$label} falló con un error inesperado {$result['class']}: {$result['message']}");
        }

        return ['outcome' => $result['outcome'], 'value' => $result['value'] ?? null, 'class' => $result['class'] ?? null, 'message' => $result['message'] ?? null];
    }

    /**
     * @return array{database: string, server: string, server_started: string, isolation: string}
     */
    private function serverOf(Connection $connection): array
    {
        $row = $connection->selectOne(
            "select current_database() as name, extract(epoch from pg_postmaster_start_time())::text as started,
                    coalesce(host(inet_server_addr()), 'socket') || ':' || coalesce(inet_server_port()::text, '-') as address,
                    current_setting('transaction_isolation') as isolation"
        );

        return ['database' => $row->name, 'server' => $row->address, 'server_started' => $row->started, 'isolation' => $row->isolation];
    }

    /**
     * @return list<int>
     */
    private function backends(): array
    {
        return array_map('intval', DB::table('pg_stat_activity')->where('application_name', 'like', "evd01-{$this->run}-%")->pluck('pid')->all());
    }

    private function activityOf(string $label): ?object
    {
        return DB::selectOne(
            'select pid, wait_event_type, query, pg_blocking_pids(pid)::text as blockers from pg_stat_activity where application_name = ?',
            ["evd01-{$this->run}-{$label}"],
        );
    }

    /**
     * @return list<int>
     */
    private function pids(?string $array): array
    {
        return array_map('intval', array_filter(explode(',', trim((string) $array, '{}'))));
    }

    private function event(string $worker, string $event, array $data = []): void
    {
        $this->timeline[] = ['t' => hrtime(true), 'worker' => $worker, 'event' => $event] + $data;
    }

    private function report(string $title, array $race): void
    {
        $events = collect($this->timeline)->sortBy('t')->values();
        $start = $events->first()['t'] ?? hrtime(true);
        $lines = $events->map(fn (array $e) => sprintf('  +%8.1f ms  %-12s %-19s %s', ($e['t'] - $start) / 1_000_000, $e['worker'], $e['event'],
            json_encode(array_diff_key($e, array_flip(['t', 'worker', 'event'])), JSON_UNESCAPED_UNICODE)));
        fwrite(STDERR, "\n{$title}\n".$lines->implode("\n")."\n  resultado: ".json_encode($race, JSON_UNESCAPED_UNICODE)."\n");
        $this->timeline = [];
    }
}
