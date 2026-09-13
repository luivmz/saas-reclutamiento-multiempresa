<?php

namespace Tests\Feature\Auth;

use App\Enums\AuditAction;
use App\Enums\UserRole;
use App\Models\AuditLog;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class CandidateRegistrationTest extends TestCase
{
    use RefreshDatabase;

    public function test_self_registration_creates_a_candidate_account_without_organization(): void
    {
        $this->post(route('register.store'), [
            'name' => 'Postulante Ficticio',
            'email' => 'ficticio@correo.test',
            'password' => 'password',
            'password_confirmation' => 'password',
        ])->assertRedirect();

        $user = User::query()->where('email', 'ficticio@correo.test')->firstOrFail();

        $this->assertAuthenticatedAs($user);
        $this->assertSame(UserRole::Candidate, $user->role);
        $this->assertNull($user->organization_id);
    }

    public function test_self_registration_cannot_escalate_role_or_organization(): void
    {
        $this->post(route('register.store'), [
            'name' => 'Intento Escalar',
            'email' => 'escalar@correo.test',
            'password' => 'password',
            'password_confirmation' => 'password',
            'role' => 'rrhh',
            'organization_id' => 1,
        ]);

        $user = User::query()->where('email', 'escalar@correo.test')->firstOrFail();

        $this->assertSame(UserRole::Candidate, $user->role);
        $this->assertNull($user->organization_id);
    }

    public function test_registration_is_audited_without_password(): void
    {
        $this->post(route('register.store'), [
            'name' => 'Postulante Auditado',
            'email' => 'auditado@correo.test',
            'password' => 'password',
            'password_confirmation' => 'password',
        ]);

        $log = AuditLog::query()->where('action', AuditAction::UserRegistered)->firstOrFail();

        $this->assertStringNotContainsString('password', json_encode($log->metadata));
    }
}
