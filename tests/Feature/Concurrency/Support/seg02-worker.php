<?php

/**
 * SEG-02 test worker. Test-only instrumentation: the application never loads it.
 *
 * Runs ONE real service call in its own PHP process and its own PostgreSQL connection, so that two workers can
 * race like two HTTP requests would. It prints one JSON line per event to STDOUT for the orchestrating test.
 *
 * Usage: php seg02-worker.php <label> <operation> <json payload>
 *   operations: discard, move, decide, register, close, schedule
 *
 * It refuses to run unless the effective database is the isolated test database.
 */

use App\Enums\ApplicationStatus;
use App\Models\Application;
use App\Models\User;
use App\Models\Vacancy;
use App\Services\Applications\ApplicationStageService;
use App\Services\Assessments\AssessmentScheduler;
use App\Services\Selection\FinalDecisionService;
use App\Services\Selection\SelectionRegistrationService;
use App\Services\Selection\VacancyClosureService;
use Illuminate\Contracts\Console\Kernel;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\DB;

require __DIR__.'/../../../../vendor/autoload.php';

$app = require __DIR__.'/../../../../bootstrap/app.php';
$app->make(Kernel::class)->bootstrap();

[$label, $operation, $json] = [$argv[1] ?? '?', $argv[2] ?? '', $argv[3] ?? '{}'];
$payload = json_decode($json, true, 512, JSON_THROW_ON_ERROR);

// Monotonic clock (CLOCK_MONOTONIC, nanoseconds): shared by every process of the kernel and immune to wall-clock steps.
$emit = function (string $event, array $data = []) use ($label): void {
    fwrite(STDOUT, json_encode(['t' => hrtime(true), 'worker' => $label, 'event' => $event] + $data, JSON_UNESCAPED_UNICODE).PHP_EOL);
    fflush(STDOUT);
};

$database = DB::connection()->getDatabaseName();
$current = DB::selectOne('select current_database() as name')->name;

if (app()->environment() !== 'testing' || $database !== 'reclutamiento_testing' || $current !== 'reclutamiento_testing') {
    $emit('abort', ['reason' => 'not the isolated test database', 'env' => app()->environment(), 'database' => $current]);
    exit(3);
}

DB::statement('set application_name = '.DB::getPdo()->quote((string) $payload['application_name']));

$server = DB::selectOne(
    "select pg_backend_pid() as pid, extract(epoch from pg_postmaster_start_time())::text as started,
            coalesce(host(inet_server_addr()), 'socket') || ':' || coalesce(inet_server_port()::text, '-') as address"
);

$emit('config', [
    'env' => app()->environment(),
    'database' => $current,
    'isolation' => DB::selectOne('show transaction_isolation')->transaction_isolation,
    'pid' => $server->pid,
    'server' => $server->address,
    'server_started' => $server->started,
    'queue' => config('queue.default'),
]);

$actor = User::query()->findOrFail($payload['actor']);
Auth::setUser($actor);

try {
    $emit('call', ['operation' => $operation]);

    $result = match ($operation) {
        'discard' => app(ApplicationStageService::class)
            ->discard(Application::query()->withoutGlobalScopes()->findOrFail($payload['application']), $actor, 'SEG02 descarte ficticio concurrente')
            ->status->value,
        'move' => app(ApplicationStageService::class)
            ->moveTo(Application::query()->withoutGlobalScopes()->findOrFail($payload['application']), ApplicationStatus::from($payload['target']), $actor, 'SEG02 cambio ficticio concurrente')
            ->status->value,
        'decide' => app(FinalDecisionService::class)
            ->decide(Vacancy::query()->withoutGlobalScopes()->findOrFail($payload['vacancy']), $actor, (int) $payload['application'], 'SEG02 decisión ficticia registrada durante la prueba de concurrencia.')
            ->selected_application_id,
        'register' => app(SelectionRegistrationService::class)
            ->register(Vacancy::query()->withoutGlobalScopes()->findOrFail($payload['vacancy']), $actor)
            ->status->value,
        'close' => app(VacancyClosureService::class)
            ->close(Vacancy::query()->withoutGlobalScopes()->findOrFail($payload['vacancy']), $actor, 'SEG02 cierre ficticio')
            ->status->value,
        'schedule' => app(AssessmentScheduler::class)
            ->scheduleEvaluation(Application::query()->withoutGlobalScopes()->findOrFail($payload['application']), $actor, [
                'type' => 'conocimientos',
                'evaluator_id' => $payload['evaluator'],
                'modality' => 'presencial',
                'location' => 'SEG02 aula ficticia',
                'scheduled_at' => now()->addWeek()->setTime(10, 0)->toDateTimeString(),
                'duration_minutes' => 60,
                'instructions' => 'SEG02 convocatoria ficticia',
            ])
            ->status->value,
        default => throw new InvalidArgumentException("Unknown operation {$operation}"),
    };

    $emit('result', ['outcome' => 'ok', 'value' => $result]);
    exit(0);
} catch (Throwable $e) {
    $emit('result', ['outcome' => 'rejected', 'class' => $e::class, 'message' => $e->getMessage()]);
    exit(0);
}
