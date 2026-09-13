<?php

namespace Tests\Feature\Testing;

use App\Services\Testing\E2eEnvironment;
use Mockery\MockInterface;
use Tests\TestCase;

/**
 * The E2E reset endpoints must be inert unless explicitly enabled outside production and called with the token,
 * and must never reset a database that is not the dedicated E2E database.
 */
class E2eSupportTest extends TestCase
{
    private const TOKEN = 'token-de-prueba-e2e';

    private function enable(): void
    {
        config(['e2e.enabled' => true, 'e2e.token' => self::TOKEN]);
    }

    public function test_endpoints_do_not_exist_when_e2e_support_is_disabled(): void
    {
        $this->mock(E2eEnvironment::class, fn (MockInterface $mock) => $mock->shouldNotReceive('reset'));
        config(['e2e.enabled' => false, 'e2e.token' => self::TOKEN]);

        $this->postJson('/__e2e/reset', [], ['X-E2E-Token' => self::TOKEN])->assertNotFound();
        $this->getJson('/__e2e/queue', ['X-E2E-Token' => self::TOKEN])->assertNotFound();
    }

    public function test_endpoints_do_not_exist_in_production_even_if_enabled(): void
    {
        $this->mock(E2eEnvironment::class, fn (MockInterface $mock) => $mock->shouldNotReceive('reset'));
        $this->enable();
        $this->app->detectEnvironment(fn () => 'production');

        $this->postJson('/__e2e/reset', [], ['X-E2E-Token' => self::TOKEN])->assertNotFound();
    }

    public function test_enabled_endpoints_reject_a_missing_or_wrong_token(): void
    {
        $this->mock(E2eEnvironment::class, fn (MockInterface $mock) => $mock->shouldNotReceive('reset'));
        $this->enable();

        $this->postJson('/__e2e/reset')->assertForbidden();
        $this->postJson('/__e2e/reset', [], ['X-E2E-Token' => 'otro'])->assertForbidden();

        config(['e2e.token' => null]);
        $this->postJson('/__e2e/reset', [], ['X-E2E-Token' => ''])->assertForbidden();
    }

    public function test_reset_endpoint_restores_the_known_demo_state(): void
    {
        $this->mock(E2eEnvironment::class, function (MockInterface $mock): void {
            $mock->shouldReceive('usesE2eDatabase')->andReturn(true);
            $mock->shouldReceive('reset')->once();
        });
        $this->enable();

        $this->postJson('/__e2e/reset', [], ['X-E2E-Token' => self::TOKEN])
            ->assertOk()
            ->assertJson(['reset' => true]);
    }

    public function test_reset_endpoint_refuses_when_the_active_database_is_not_the_e2e_database(): void
    {
        $this->mock(E2eEnvironment::class, function (MockInterface $mock): void {
            $mock->shouldReceive('usesE2eDatabase')->andReturn(false);
            $mock->shouldNotReceive('reset');
        });
        $this->enable();

        $this->postJson('/__e2e/reset', [], ['X-E2E-Token' => self::TOKEN])
            ->assertStatus(409)
            ->assertJson(['reset' => false]);
    }

    public function test_queue_endpoint_reports_pending_jobs(): void
    {
        $this->mock(E2eEnvironment::class, fn (MockInterface $mock) => $mock->shouldReceive('pendingJobs')->once()->andReturn(3));
        $this->enable();

        $this->getJson('/__e2e/queue', ['X-E2E-Token' => self::TOKEN])
            ->assertOk()
            ->assertExactJson(['pending' => 3]);
    }

    public function test_reset_command_runs_against_the_e2e_database(): void
    {
        $this->mock(E2eEnvironment::class, function (MockInterface $mock): void {
            $mock->shouldReceive('usesE2eDatabase')->andReturn(true);
            $mock->shouldReceive('reset')->once();
        });

        $this->artisan('e2e:reset')->assertSuccessful();
    }

    public function test_reset_command_refuses_a_database_that_is_not_the_e2e_database(): void
    {
        $this->mock(E2eEnvironment::class, function (MockInterface $mock): void {
            $mock->shouldReceive('usesE2eDatabase')->andReturn(false);
            $mock->shouldNotReceive('reset');
        });

        $this->artisan('e2e:reset')->assertFailed();
    }

    public function test_reset_command_refuses_to_run_in_production(): void
    {
        $this->mock(E2eEnvironment::class, fn (MockInterface $mock) => $mock->shouldNotReceive('reset'));
        $this->app->detectEnvironment(fn () => 'production');

        $this->artisan('e2e:reset')->assertFailed();
    }
}
