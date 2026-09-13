<?php

namespace Tests\Feature\Frontend;

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

/**
 * DEF-09: the frontend formatted dates in the browser timezone; the root view must expose APP_TIMEZONE.
 */
class AppTimezoneTest extends TestCase
{
    use RefreshDatabase;

    public function test_root_view_exposes_the_application_timezone_for_date_formatting(): void
    {
        config(['app.timezone' => 'America/Lima']);

        $this->actingAs(User::factory()->candidate()->create())
            ->get(route('dashboard'))
            ->assertOk()
            ->assertSee('<meta name="app-timezone" content="America/Lima">', false);
    }

    public function test_public_pages_also_expose_the_application_timezone(): void
    {
        $this->get(route('login'))
            ->assertOk()
            ->assertSee('<meta name="app-timezone" content="'.config('app.timezone').'">', false);
    }
}
