<?php

namespace App\Services\Testing;

use Illuminate\Contracts\Queue\ClearableQueue;
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Queue;

/**
 * Known starting state for the Cypress suite: fresh schema, DemoSeeder data, no pending jobs and no cached
 * rate limits. Only reachable through `e2e:reset` or the guarded `/__e2e/*` endpoints (never in production).
 */
class E2eEnvironment
{
    public function reset(): void
    {
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

    private function clearQueue(): void
    {
        $queue = Queue::connection();

        if ($queue instanceof ClearableQueue) {
            $default = config('queue.default');
            $queue->clear(config("queue.connections.{$default}.queue", 'default'));
        }
    }
}
