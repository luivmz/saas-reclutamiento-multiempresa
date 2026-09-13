<?php

namespace App\Services\Testing;

use Illuminate\Contracts\Queue\ClearableQueue;
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Queue;
use RuntimeException;

/**
 * Known starting state for the Cypress suite: fresh schema, DemoSeeder data, no pending jobs and no cached
 * rate limits. Only reachable through `e2e:reset` or the guarded `/__e2e/*` endpoints (never in production),
 * and only against the dedicated E2E database (DEF-13).
 */
class E2eEnvironment
{
    public function usesE2eDatabase(): bool
    {
        $expected = (string) config('e2e.database');

        return $expected !== '' && $this->activeDatabase() === $expected;
    }

    public function reset(): void
    {
        if (! $this->usesE2eDatabase()) {
            throw new RuntimeException(sprintf(
                'Reset E2E rechazado: la base activa [%s] no es la base E2E configurada [%s].',
                $this->activeDatabase(),
                (string) config('e2e.database'),
            ));
        }

        $this->clearQueue();
        Artisan::call('migrate:fresh', ['--seed' => true, '--force' => true]);
        Cache::flush();
    }

    /**
     * Jobs still waiting (ready, delayed or reserved) on the default queue, e.g. notifications not yet delivered.
     */
    public function pendingJobs(): int
    {
        return Queue::connection()->size();
    }

    private function activeDatabase(): string
    {
        return (string) config('database.connections.'.config('database.default').'.database');
    }

    private function clearQueue(): void
    {
        $queue = Queue::connection();

        if ($queue instanceof ClearableQueue) {
            $default = config('queue.default');
            $queue->clear(config("queue.connections.{$default}.queue", 'default'));
        }
    }
}
