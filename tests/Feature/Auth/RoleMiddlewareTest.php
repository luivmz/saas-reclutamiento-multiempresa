<?php

namespace Tests\Feature\Auth;

use App\Models\Organization;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Route;
use Tests\TestCase;

class RoleMiddlewareTest extends TestCase
{
    use RefreshDatabase;

    protected function setUp(): void
    {
        parent::setUp();

        Route::middleware(['web', 'auth', 'role:rrhh,aprobador'])
            ->get('/_test/solo-rrhh-aprobador', fn () => 'ok');
    }

    public function test_guest_is_redirected_to_login(): void
    {
        $this->get('/_test/solo-rrhh-aprobador')->assertRedirect(route('login'));
    }

    public function test_user_without_allowed_role_is_forbidden(): void
    {
        $organization = Organization::factory()->create();

        $this->actingAs(User::factory()->requester($organization)->create())
            ->get('/_test/solo-rrhh-aprobador')
            ->assertForbidden();

        $this->actingAs(User::factory()->candidate()->create())
            ->get('/_test/solo-rrhh-aprobador')
            ->assertForbidden();
    }

    public function test_user_with_allowed_role_passes(): void
    {
        $organization = Organization::factory()->create();

        $this->actingAs(User::factory()->hr($organization)->create())
            ->get('/_test/solo-rrhh-aprobador')
            ->assertOk();

        $this->actingAs(User::factory()->approver($organization)->create())
            ->get('/_test/solo-rrhh-aprobador')
            ->assertOk();
    }
}
