<?php

namespace Tests\Feature\Concurrency;

use App\Enums\ApplicationStatus;
use App\Exceptions\BusinessRuleException;
use App\Exceptions\InvalidStateTransition;
use App\Models\Application;
use App\Models\Organization;
use App\Models\SelectionDecision;
use App\Models\User;
use App\Models\Vacancy;
use App\Services\Ranking\RankedCandidate;
use App\Services\Ranking\VacancyRankingBuilder;
use Illuminate\Contracts\Process\InvokedProcess;
use Illuminate\Database\Connection;
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Process;
use Illuminate\Support\Str;
use PHPUnit\Framework\Attributes\Group;
use Tests\Concerns\BuildsRankingScenario;
use Tests\TestCase;

/**
 * SEG-02 (diagnostic): a manual stage change racing the final decision (A-28), with real PHP processes, separate
 * PostgreSQL connections and the real services. Not a simulation of the algorithm. RED while the runtime lets the
 * race through; the assertions only accept outcomes of some serial order, so they also hold once it is fixed.
 *
 * Deterministic coordination without runtime hooks: a third "barrier" connection holds a lock that the first worker
 * only meets after its own rule check. The test confirms through pg_stat_activity and pg_blocking_pids that the
 * worker waits on that lock and on the expected statement, then runs the second worker. If the second worker ends
 * while the first one is still held, the order of the commits is known: second, then first. If it waits on a lock
 * of the first worker instead, the runtime serializes both operations. Either way the barrier is then released.
 *
 *  - LOCK_APPLICATION_ROW (FOR SHARE) stops ApplicationStageService::transition() at its FOR UPDATE, which only
 *    runs after the A-28 check of moveTo(). It does not conflict with the FOR KEY SHARE of foreign-key checks.
 *  - LOCK_RANKING_INPUT (ACCESS EXCLUSIVE on interview_results) stops FinalDecisionService inside the ranking, which
 *    only runs after its «Finalista» check. The stage-change path never reads that table.
 *
 * Fixtures are committed so the workers can see them: this class does not use RefreshDatabase. It works only on
 * the isolated test database and leaves it freshly migrated.
 */
#[Group('seg02')]
class DecisionStageConcurrencyTest extends TestCase
{
    use BuildsRankingScenario;

    private const WORKER = __DIR__.'/Support/seg02-worker.php';

    private const TEST_DATABASE = 'reclutamiento_testing';

    private const EXPECTED_REJECTIONS = [BusinessRuleException::class, InvalidStateTransition::class];

    private const LOCK_APPLICATION_ROW = 'select id from applications where id = ? for share';

    private const LOCK_RANKING_INPUT = 'lock table interview_results in access exclusive mode';

    /** Fragments of the statement on which the first worker must be found waiting. */
    private const WAITS_IN_TRANSITION = ['from "applications"', 'for update'];

    private const WAITS_IN_RANKING = ['from "interview_results"'];

    private Organization $organization;

    private User $hr;

    private User $approver;

    private Vacancy $vacancy;

    private Application $chosen;

    private Application $other;

    private string $run;

    /** @var array{database: string, server: string, server_started: string, isolation: string} */
    private array $server;

    private ?Connection $barrier = null;

    /** @var list<InvokedProcess> */
    private array $processes = [];

    /** @var list<array<string, mixed>> */
    private array $timeline = [];

    private bool $reported = false;

    protected function setUp(): void
    {
        parent::setUp();

        $this->assertSame(self::TEST_DATABASE, DB::connection()->getDatabaseName(), 'ENTORNO: la conexión no apunta a la base de pruebas aislada.');
        $this->server = $this->serverOf(DB::connection());
        $this->assertSame(self::TEST_DATABASE, $this->server['database'], 'ENTORNO: la base efectiva no es la de pruebas.');

        Artisan::call('migrate:fresh', ['--force' => true]);

        $this->run = Str::lower(Str::random(6));
        $this->organization = Organization::factory()->create();
        $this->hr = User::factory()->hr($this->organization)->create();
        $this->approver = User::factory()->approver($this->organization)->create();
        $this->vacancy = Vacancy::factory()->for($this->organization)->configured()->published()->create();
        $this->chosen = $this->candidateWithScores($this->vacancy, 18, 16, 17);
        $this->other = $this->candidateWithScores($this->vacancy, 20, 10, 19);
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
            DB::purge('seg02_barrier');
        }

        if (! $this->reported && $this->timeline !== []) {
            $this->report('ejecución interrumpida');
        }

        Artisan::call('migrate:fresh', ['--force' => true]);

        parent::tearDown();
    }

    /**
     * S3: the discard passes its A-28 check and stops at its row lock; the decision is recorded; the discard goes on.
     */
    public function test_seg02_s3_discard_that_passed_its_check_before_the_decision_must_not_discard_the_chosen_application(): void
    {
        $race = $this->race(self::LOCK_APPLICATION_ROW, [$this->chosen->id], self::WAITS_IN_TRANSITION,
            first: ['A', 'discard', $this->manualChange($this->chosen)],
            second: ['B', 'decide', $this->decisionFor($this->chosen)],
        );
        $effects = $this->downstreamEffects();
        $this->report('S3: el descarte supera su comprobación A-28, se registra la decisión y el descarte continúa', $race, $effects);

        $this->assertInvariants($race, manualFirst: true, effects: $effects);
    }

    /**
     * S3b: the decision passes its «Finalista» check and stops in the ranking; the discard ends; the decision goes on.
     */
    public function test_seg02_s3b_decision_that_passed_its_finalist_check_before_the_discard_must_not_point_to_a_discarded_application(): void
    {
        $race = $this->race(self::LOCK_RANKING_INPUT, [], self::WAITS_IN_RANKING,
            first: ['B', 'decide', $this->decisionFor($this->chosen)],
            second: ['A', 'discard', $this->manualChange($this->chosen)],
        );
        $effects = $this->downstreamEffects();
        $this->report('S3b: la decisión supera su comprobación de «Finalista», el descarte termina y la decisión continúa', $race, $effects);

        $this->assertInvariants($race, manualFirst: false, effects: $effects);
    }

    /**
     * S4: the discard of another application of the same vacancy passes its A-28 check before the decision.
     */
    public function test_seg02_s4_discard_of_another_application_that_passed_its_check_before_the_decision_must_be_rejected(): void
    {
        $race = $this->race(self::LOCK_APPLICATION_ROW, [$this->other->id], self::WAITS_IN_TRANSITION,
            first: ['A', 'discard', $this->manualChange($this->other)],
            second: ['B', 'decide', $this->decisionFor($this->chosen)],
        );
        $effects = $this->downstreamEffects();
        $this->report('S4: descarte de otra postulación de la misma vacante contra la decisión final', $race, $effects);

        $this->assertInvariants($race, manualFirst: true, effects: $effects);
    }

    /**
     * S4b: the same race with a stage change («En entrevista» → «Finalista») instead of a discard.
     */
    public function test_seg02_s4b_stage_change_of_another_application_that_passed_its_check_before_the_decision_must_be_rejected(): void
    {
        $interviewing = $this->candidateWithScores($this->vacancy, 12, 12, 12, ApplicationStatus::Interview);

        $race = $this->race(self::LOCK_APPLICATION_ROW, [$interviewing->id], self::WAITS_IN_TRANSITION,
            first: ['A', 'move', $this->manualChange($interviewing) + ['target' => ApplicationStatus::Finalist->value]],
            second: ['B', 'decide', $this->decisionFor($this->chosen)],
        );
        $effects = $this->downstreamEffects();
        $this->report('S4b: cambio de etapa de otra postulación de la misma vacante contra la decisión final', $race, $effects);

        $this->assertInvariants($race, manualFirst: true, effects: $effects);
    }

    /**
     * S5 (control): a decision in one vacancy does not block legitimate manual changes in another one.
     */
    public function test_seg02_s5_a_decision_in_another_vacancy_does_not_block_manual_changes(): void
    {
        $vacancyB = Vacancy::factory()->for($this->organization)->configured()->published()->create();
        $elsewhere = $this->candidateWithScores($vacancyB, 15, 15, 15);

        $race = $this->race(self::LOCK_APPLICATION_ROW, [$elsewhere->id], self::WAITS_IN_TRANSITION,
            first: ['A', 'discard', $this->manualChange($elsewhere)],
            second: ['B', 'decide', $this->decisionFor($this->chosen)],
        );
        $this->report('S5 (control): decisión en la vacante 1 y descarte en la vacante 2', $race);

        $this->assertSame(['ok', 'ok'], [$race['second']['outcome'], $race['first']['outcome']],
            'CONTROL: la decisión de la vacante 1 y el descarte de la vacante 2 son legítimos.');
        $this->assertSame(ApplicationStatus::Discarded, $elsewhere->fresh()->status);
        $this->assertSame(ApplicationStatus::Finalist, $this->chosen->fresh()->status);
        $this->assertSame(0, SelectionDecision::query()->withoutGlobalScopes()->where('vacancy_id', $vacancyB->id)->count());
    }

    /**
     * S6 (control of the instrument): two decisions on the same vacancy do share a lock, the vacancy row, so the
     * second one must be seen waiting on the first and only the first may be recorded.
     */
    public function test_seg02_s6_two_concurrent_decisions_are_serialized_by_the_vacancy_lock(): void
    {
        $race = $this->race(self::LOCK_RANKING_INPUT, [], self::WAITS_IN_RANKING,
            first: ['B', 'decide', $this->decisionFor($this->chosen)],
            second: ['E', 'decide', $this->decisionFor($this->other)],
        );
        $this->report('S6 (control del instrumento): dos decisiones concurrentes sobre la misma vacante', $race);

        $this->assertTrue($race['serialized'], 'CONTROL: la segunda decisión debía esperar el lock de la vacante que tiene la primera.');
        $this->assertSame(['ok', 'rejected'], [$race['first']['outcome'], $race['second']['outcome']]);
        $this->assertSame($this->chosen->id, SelectionDecision::query()->withoutGlobalScopes()->sole()->selected_application_id);
    }

    /**
     * I1: a recorded decision never points to a discarded application.
     * I2 (A-28): no manual stage change of the vacancy is committed after its final decision.
     * I3: with a recorded decision, the process can still be completed through RF-24 and RF-25.
     *
     * @param  array{first: array<string, mixed>, second: array<string, mixed>, serialized: bool}  $race
     * @param  array<string, mixed>  $effects
     */
    private function assertInvariants(array $race, bool $manualFirst, array $effects): void
    {
        [$manual, $decision] = $manualFirst ? [$race['first'], $race['second']] : [$race['second'], $race['first']];
        $manualCommittedLast = $manualFirst !== $race['serialized'];
        $context = sprintf(
            'Cambio manual = %s; decisión = %s; %s; RF-24 = %s; RF-25 = %s.',
            $this->outcome($manual),
            $this->outcome($decision),
            $race['serialized'] ? 'el runtime serializó ambas operaciones' : 'la segunda operación terminó mientras la primera esperaba en la barrera',
            $this->outcome($effects['rf24']),
            $this->outcome($effects['rf25']),
        );

        $this->assertNotSame(ApplicationStatus::Discarded->value, $effects['decision']['selected_status'] ?? null,
            "INVARIANTE I1 VIOLADA (A-28): la decisión registrada apunta a una postulación descartada. {$context}");

        $this->assertFalse($manualCommittedLast && $manual['outcome'] === 'ok' && $decision['outcome'] === 'ok',
            "INVARIANTE I2 VIOLADA (A-28): un cambio manual de etapa se confirmó después de la decisión final de la misma vacante. {$context}");

        if ($effects['decision'] !== null) {
            $this->assertSame(['ok', 'ok'], [$effects['rf24']['outcome'], $effects['rf25']['outcome']],
                "INVARIANTE I3 VIOLADA: con la decisión registrada, RF-24 y RF-25 deben poder completar el proceso. {$context}");
        }
    }

    /**
     * Runs RF-24 and then RF-25 as HR would after the decision and gathers what the race left behind. These are
     * observations for the report; the assertions are in assertInvariants().
     *
     * @return array<string, mixed>
     */
    private function downstreamEffects(): array
    {
        $registration = $this->runWorker('C', 'register', ['actor' => $this->hr->id, 'vacancy' => $this->vacancy->id]);
        $closure = $this->runWorker('D', 'close', ['actor' => $this->hr->id, 'vacancy' => $this->vacancy->id]);
        $decision = SelectionDecision::query()->withoutGlobalScopes()->where('vacancy_id', $this->vacancy->id)->first();

        return [
            'decision' => $decision === null ? null : [
                'selected_application_id' => $decision->selected_application_id,
                'selected_status' => Application::query()->withoutGlobalScopes()->findOrFail($decision->selected_application_id)->status->value,
                'selected_position' => $decision->selected_position,
                'ranked_candidates' => $decision->ranked_candidates,
            ],
            'rf24' => $registration,
            'rf25' => $closure,
            'vacancy_status' => $this->vacancy->fresh()->status->value,
            'applications' => Application::query()->withoutGlobalScopes()->where('vacancy_id', $this->vacancy->id)->orderBy('id')->get()
                ->mapWithKeys(fn (Application $application) => ["#{$application->id}" => $application->status->value])->all(),
            'live_ranking' => array_map(
                fn (RankedCandidate $entry) => "#{$entry->applicationId}",
                app(VacancyRankingBuilder::class)->forVacancy($this->vacancy->fresh())->entries,
            ),
            'stage_history' => DB::table('application_stage_histories')->orderBy('id')->get(['application_id', 'from_status', 'to_status'])
                ->map(fn (object $row) => "#{$row->application_id} {$row->from_status} -> {$row->to_status}")->all(),
            'audit_trail' => DB::table('audit_logs')->orderBy('id')->get(['action', 'auditable_type', 'auditable_id'])
                ->map(fn (object $row) => "{$row->action} {$row->auditable_type}#{$row->auditable_id}")->all(),
            'notifications' => DB::table('notifications')->orderBy('created_at')->get(['notifiable_id', 'data'])
                ->map(fn (object $row) => "usuario #{$row->notifiable_id}: ".json_decode($row->data, true)['message'])->all(),
        ];
    }

    /**
     * @param  list<int>  $bindings
     * @param  list<string>  $waitsIn
     * @param  array{0: string, 1: string, 2: array<string, mixed>}  $first
     * @param  array{0: string, 1: string, 2: array<string, mixed>}  $second
     * @return array{first: array<string, mixed>, second: array<string, mixed>, serialized: bool}
     */
    private function race(string $barrier, array $bindings, array $waitsIn, array $first, array $second): array
    {
        config(['database.connections.seg02_barrier' => config('database.connections.pgsql')]);
        $this->barrier = DB::connection('seg02_barrier');
        $this->assertSame($this->server, $this->serverOf($this->barrier), 'ENTORNO: la barrera no apunta a la base de pruebas aislada.');
        $this->barrier->statement('set application_name = '.$this->barrier->getPdo()->quote("seg02-{$this->run}-barrier"));
        $barrierPid = (int) $this->barrier->selectOne('select pg_backend_pid() as pid')->pid;

        $this->barrier->beginTransaction();
        $this->barrier->statement($barrier, $bindings);
        $this->event('orchestrator', 'barrier-locked', ['pid' => $barrierPid, 'sql' => $barrier, 'bindings' => $bindings]);

        $firstProcess = $this->startWorker(...$first);
        $firstPid = $this->waitUntilBlocked($firstProcess, $first[0], $barrierPid, $waitsIn);

        $secondProcess = $this->startWorker(...$second);
        $serialized = $this->secondWaitsOnFirst($secondProcess, $second[0], $barrierPid, $firstPid);

        $this->barrier->commit();
        $this->event('orchestrator', 'barrier-released');

        $firstProcess->wait();
        $secondProcess->wait();

        return [
            'first' => $this->collect($first[0], $firstProcess),
            'second' => $this->collect($second[0], $secondProcess),
            'serialized' => $serialized,
        ];
    }

    /**
     * Waits until the first worker is blocked by the barrier on the expected statement and returns its backend pid.
     *
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
                $this->assertSame(self::TEST_DATABASE, $row->datname, "ENTORNO: el backend de {$label} no está conectado a la base de pruebas.");

                foreach ($waitsIn as $fragment) {
                    $this->assertStringContainsString($fragment, (string) $row->query, "ORQUESTACIÓN: {$label} espera la barrera en una sentencia inesperada.");
                }

                $this->event('orchestrator', 'observed-blocked', $this->describe($label, $row));

                return (int) $row->pid;
            }

            usleep(20_000);
        }

        $this->fail("ORQUESTACIÓN: {$label} no quedó bloqueado por la barrera en 30 s.");
    }

    /**
     * Lets the second worker run while the first one is held by the barrier. Returns false when it ends meanwhile, so
     * its commit precedes the first worker's; true when it waits on a lock of the first worker instead, so the runtime
     * serializes both operations and the first one commits first.
     */
    private function secondWaitsOnFirst(InvokedProcess $process, string $label, int $barrierPid, int $firstPid): bool
    {
        $deadline = hrtime(true) + 60 * 1_000_000_000;

        while ($process->running()) {
            $row = $this->activityOf($label);
            $blockers = $row?->wait_event_type === 'Lock' ? $this->pids($row->blockers) : [];

            if (in_array($firstPid, $blockers, true)) {
                $this->event('orchestrator', 'observed-serialized', $this->describe($label, $row));

                return true;
            }

            if (in_array($barrierPid, $blockers, true)) {
                $this->fail("ORQUESTACIÓN: {$label} espera un lock de la barrera; el escenario no fuerza el orden buscado.\n"
                    .json_encode($this->describe($label, $row), JSON_UNESCAPED_UNICODE));
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
                'APP_ENV' => 'testing',
                'DB_CONNECTION' => 'pgsql',
                'DB_DATABASE' => self::TEST_DATABASE,
                'DB_URL' => '',
                'CACHE_STORE' => 'array',
                'QUEUE_CONNECTION' => 'sync',
                'SESSION_DRIVER' => 'array',
                'MAIL_MAILER' => 'array',
                'BROADCAST_CONNECTION' => 'null',
                'PULSE_ENABLED' => 'false',
                'TELESCOPE_ENABLED' => 'false',
                'NIGHTWATCH_ENABLED' => 'false',
                'E2E_ENABLED' => 'false',
            ])
            ->timeout(120)
            ->start([PHP_BINARY, self::WORKER, $label, $operation, json_encode($payload + ['application_name' => "seg02-{$this->run}-{$label}"])]);

        $this->processes[] = $process;
        $this->event('orchestrator', 'started', ['process' => $label, 'operation' => $operation]);

        return $process;
    }

    /**
     * @return array{outcome: string, value: mixed, class: string|null, message: string|null}
     */
    private function runWorker(string $label, string $operation, array $payload): array
    {
        $process = $this->startWorker($label, $operation, $payload);
        $process->wait();

        return $this->collect($label, $process);
    }

    /**
     * Checks the effective configuration the worker reported and returns its result.
     *
     * @return array{outcome: string, value: mixed, class: string|null, message: string|null}
     */
    private function collect(string $label, InvokedProcess $process): array
    {
        $output = $process->output();
        $events = array_values(array_filter(array_map(
            fn (string $line) => json_decode($line, true),
            preg_split('/\R/', trim($output)) ?: [],
        )));

        array_push($this->timeline, ...$events);

        $config = collect($events)->firstWhere('event', 'config');
        $result = collect($events)->firstWhere('event', 'result');

        if ($config === null || $result === null) {
            $this->fail("ENTORNO: el worker {$label} no confirmó su configuración o su resultado.\n{$output}\n{$process->errorOutput()}");
        }

        $this->assertSame(
            ['testing', $this->server['database'], $this->server['server'], $this->server['server_started'], $this->server['isolation'], config('queue.default')],
            [$config['env'], $config['database'], $config['server'], $config['server_started'], $config['isolation'], $config['queue']],
            "ENTORNO: la configuración efectiva del worker {$label} no coincide con la de la base de pruebas aislada.",
        );

        if ($result['outcome'] === 'rejected' && ! in_array($result['class'], self::EXPECTED_REJECTIONS, true)) {
            $this->fail("ENTORNO O PRUEBA: el worker {$label} falló con un error inesperado {$result['class']}: {$result['message']}");
        }

        return [
            'outcome' => $result['outcome'],
            'value' => $result['value'] ?? null,
            'class' => $result['class'] ?? null,
            'message' => $result['message'] ?? null,
        ];
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

    private function activityOf(string $label): ?object
    {
        return DB::selectOne(
            'select pid, datname, wait_event_type, wait_event, query, pg_blocking_pids(pid)::text as blockers
               from pg_stat_activity where application_name = ?',
            ["seg02-{$this->run}-{$label}"],
        );
    }

    /**
     * @return array<string, mixed>
     */
    private function describe(string $label, object $row): array
    {
        return [
            'process' => $label,
            'pid' => $row->pid,
            'database' => $row->datname,
            'wait' => "{$row->wait_event_type}/{$row->wait_event}",
            'blocked_by' => $row->blockers,
            'query' => Str::limit((string) preg_replace('/\s+/', ' ', (string) $row->query), 170),
        ];
    }

    /**
     * @return array<string, int>
     */
    private function manualChange(Application $application): array
    {
        return ['actor' => $this->hr->id, 'application' => $application->id];
    }

    /**
     * @return array<string, int>
     */
    private function decisionFor(Application $application): array
    {
        return ['actor' => $this->approver->id, 'vacancy' => $this->vacancy->id, 'application' => $application->id];
    }

    private function outcome(array $result): string
    {
        return $result['class'] === null
            ? "{$result['outcome']} (".json_encode($result['value'], JSON_UNESCAPED_UNICODE).')'
            : "{$result['outcome']} (".class_basename($result['class']).": {$result['message']})";
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

    /**
     * Prints the merged timeline of the orchestrator and the workers (STDERR), then the race and its effects. Times
     * come from the monotonic clock shared by all the processes: in the Docker Desktop VM the wall clock steps back
     * by about 0.2 s every 30 s, which misordered the events of one run.
     */
    private function report(string $title, array $race = [], array $effects = []): void
    {
        $this->reported = true;
        $flags = JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES;
        $events = collect($this->timeline)->sortBy('t')->values();
        $start = $events->first()['t'] ?? hrtime(true);
        $lines = $events->map(function (array $event) use ($start, $flags) {
            $data = array_diff_key($event, array_flip(['t', 'worker', 'event']));

            return sprintf('  +%8.1f ms  %-12s %-19s %s', ($event['t'] - $start) / 1_000_000, $event['worker'], $event['event'], json_encode($data, $flags));
        });

        fwrite(STDERR, "\nSEG-02 {$title}\n".$lines->implode("\n")."\n"
            .(isset($race['serialized']) ? '  serializado por el runtime: '.($race['serialized'] ? 'sí' : 'no')."\n" : '')
            .($effects === [] ? '' : '  efectos: '.json_encode($effects, $flags | JSON_PRETTY_PRINT)."\n"));
    }
}
