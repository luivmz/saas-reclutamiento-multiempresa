<?php

namespace Tests\Feature\Testing;

use App\Services\Testing\E2eEnvironment;
use Illuminate\Support\Facades\Artisan;
use RuntimeException;
use Tests\TestCase;

/**
 * DEF-13: the destructive E2E reset must only ever run against the dedicated E2E database.
 */
class E2eEnvironmentTest extends TestCase
{
    private function activeDatabase(): string
    {
        return (string) config('database.connections.'.config('database.default').'.database');
    }

    public function test_detects_whether_the_active_database_is_the_configured_e2e_database(): void
    {
        $environment = app(E2eEnvironment::class);

        config(['e2e.database' => $this->activeDatabase()]);
        $this->assertTrue($environment->usesE2eDatabase());

        config(['e2e.database' => 'reclutamiento_e2e']);
        $this->assertFalse($environment->usesE2eDatabase());

        config(['e2e.database' => '']);
        $this->assertFalse($environment->usesE2eDatabase());
    }

    public function test_reset_never_touches_a_database_that_is_not_the_e2e_database(): void
    {
        Artisan::shouldReceive('call')->never();
        config(['e2e.database' => 'reclutamiento_e2e']);

        $this->expectException(RuntimeException::class);

        app(E2eEnvironment::class)->reset();
    }
}
