<?php

namespace Tests\Feature\Audit;

use App\Enums\AuditAction;
use App\Models\AuditLog;
use App\Models\Organization;
use App\Models\User;
use App\Services\Audit\AuditLogger;
use Illuminate\Foundation\Testing\RefreshDatabase;
use LogicException;
use Tests\TestCase;

class AuditLoggerTest extends TestCase
{
    use RefreshDatabase;

    public function test_records_actor_action_entity_and_organization(): void
    {
        $organization = Organization::factory()->create();
        $hr = User::factory()->hr($organization)->create();
        $this->actingAs($hr);

        $log = app(AuditLogger::class)->record(AuditAction::UserRegistered, $hr, ['source' => 'test']);

        $this->assertSame($organization->id, $log->organization_id);
        $this->assertSame($hr->id, $log->user_id);
        $this->assertSame(AuditAction::UserRegistered, $log->action);
        $this->assertSame('user', $log->auditable_type);
        $this->assertSame($hr->id, $log->auditable_id);
        $this->assertSame(['source' => 'test'], $log->metadata);
        $this->assertNotNull($log->created_at);
    }

    public function test_sensitive_metadata_is_never_stored(): void
    {
        $candidate = User::factory()->candidate()->create();

        $log = app(AuditLogger::class)->record(AuditAction::UserRegistered, $candidate, [
            'password' => 'secret-value',
            'password_confirmation' => 'secret-value',
            'remember_token' => 'abc',
            'api_token' => 'abc',
            'two_factor_secret' => 'abc',
            'cv_content' => 'binary',
            'nested' => ['token' => 'abc', 'kept' => 'yes'],
            'email_domain' => 'correo.test',
        ]);

        $this->assertSame(['nested' => ['kept' => 'yes'], 'email_domain' => 'correo.test'], $log->fresh()->metadata);
    }

    public function test_audit_logs_cannot_be_updated(): void
    {
        $log = app(AuditLogger::class)->record(AuditAction::UserRegistered, User::factory()->candidate()->create());

        $this->expectException(LogicException::class);

        $log->update(['ip_address' => '10.0.0.99']);
    }

    public function test_audit_logs_cannot_be_deleted(): void
    {
        $log = app(AuditLogger::class)->record(AuditAction::UserRegistered, User::factory()->candidate()->create());

        $this->expectException(LogicException::class);

        $log->delete();
    }
}
