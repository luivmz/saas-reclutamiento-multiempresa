<?php

/**
 * APP-M01 test worker (experimental evidence flow). Test-only instrumentation: the application never loads it.
 *
 * Runs ONE real operation in its own PHP process and its own PostgreSQL connection, as an HTTP request would: first
 * the policy check of the controller/form request, then the real service. Prints one JSON line per event.
 *
 * Usage: php evidence-worker.php <label> <operation> <json payload>
 *   operations: close, register, link, unlink, review, correct, withdraw
 *
 * It refuses to run unless the effective database is the isolated test database.
 */

use App\Enums\EvidenceSource;
use App\Enums\EvidenceType;
use App\Models\Application;
use App\Models\EvidenceItem;
use App\Models\User;
use App\Models\Vacancy;
use App\Services\Evidence\EvidenceService;
use App\Services\Selection\VacancyClosureService;
use Illuminate\Contracts\Console\Kernel;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Gate;

require __DIR__.'/../../../../vendor/autoload.php';

$app = require __DIR__.'/../../../../bootstrap/app.php';
$app->make(Kernel::class)->bootstrap();

[$label, $operation, $json] = [$argv[1] ?? '?', $argv[2] ?? '', $argv[3] ?? '{}'];
$payload = json_decode($json, true, 512, JSON_THROW_ON_ERROR);

$emit = function (string $event, array $data = []) use ($label): void {
    fwrite(STDOUT, json_encode(['t' => hrtime(true), 'worker' => $label, 'event' => $event] + $data, JSON_UNESCAPED_UNICODE).PHP_EOL);
    fflush(STDOUT);
};

$current = DB::selectOne('select current_database() as name')->name;

if (app()->environment() !== 'testing' || DB::connection()->getDatabaseName() !== 'reclutamiento_testing' || $current !== 'reclutamiento_testing') {
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
]);

$actor = User::query()->findOrFail($payload['actor']);
Auth::setUser($actor);
$gate = Gate::forUser($actor);
$service = app(EvidenceService::class);
$evidence = fn () => EvidenceItem::query()->withoutGlobalScopes()->findOrFail($payload['evidence']);
$text = '[SINTÉTICO] Evidencia ficticia escrita durante la prueba de concurrencia APP-M01.';

try {
    $emit('call', ['operation' => $operation]);

    $result = match ($operation) {
        'close' => app(VacancyClosureService::class)
            ->close(Vacancy::query()->withoutGlobalScopes()->findOrFail($payload['vacancy']), $actor, 'APP-M01 cierre ficticio')
            ->status->value,
        'register' => (function () use ($gate, $service, $actor, $payload, $text, $emit) {
            $application = Application::query()->withoutGlobalScopes()->findOrFail($payload['application']);
            $gate->authorize('create', [EvidenceItem::class, $application]);
            $emit('authorized');

            return $service->register($actor, $application, EvidenceType::Certificate, EvidenceSource::SubmittedDocument, $text)->id;
        })(),
        'link', 'unlink' => (function () use ($gate, $service, $actor, $payload, $evidence, $operation, $emit) {
            $item = $evidence();
            $gate->authorize('link', $item);
            $emit('authorized');

            return $service->{$operation}($actor, $item, (int) $payload['criterion'])->id;
        })(),
        'review' => (function () use ($gate, $service, $actor, $evidence, $emit) {
            $item = $evidence();
            $gate->authorize('review', $item);
            $emit('authorized');

            return $service->review($actor, $item)->id;
        })(),
        'correct' => (function () use ($gate, $service, $actor, $evidence, $text, $emit) {
            $item = $evidence();
            $gate->authorize('correct', $item);
            $emit('authorized');

            return $service->correct($actor, $item, $item->type, $item->source, $text)->id;
        })(),
        'withdraw' => (function () use ($gate, $service, $actor, $evidence, $emit) {
            $item = $evidence();
            $gate->authorize('withdraw', $item);
            $emit('authorized');

            return $service->withdraw($actor, $item, '[SINTÉTICO] Retiro ficticio durante la prueba APP-M01.')->id;
        })(),
        default => throw new InvalidArgumentException("Unknown operation {$operation}"),
    };

    $emit('result', ['outcome' => 'ok', 'value' => $result]);
    exit(0);
} catch (Throwable $e) {
    $emit('result', ['outcome' => 'rejected', 'class' => $e::class, 'message' => $e->getMessage()]);
    exit(0);
}
