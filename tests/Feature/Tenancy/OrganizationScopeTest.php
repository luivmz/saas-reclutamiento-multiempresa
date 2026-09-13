<?php

namespace Tests\Feature\Tenancy;

use App\Enums\AuditAction;
use App\Enums\UserRole;
use App\Models\AuditLog;
use App\Models\Organization;
use App\Models\User;
use App\Services\Audit\AuditLogger;
use Illuminate\Database\QueryException;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class OrganizationScopeTest extends TestCase
{
    use RefreshDatabase;

    public function test_staff_user_only_sees_records_of_own_organization(): void
    {
        $orgA = Organization::factory()->create();
        $orgB = Organization::factory()->create();
        $hrA = User::factory()->hr($orgA)->create();
        $hrB = User::factory()->hr($orgB)->create();

        $this->actingAs($hrA);
        app(AuditLogger::class)->record(AuditAction::UserRegistered, $hrA);
        $this->actingAs($hrB);
        app(AuditLogger::class)->record(AuditAction::UserRegistered, $hrB);

        $this->actingAs($hrA);
        $this->assertSame([$orgA->id], AuditLog::query()->pluck('organization_id')->unique()->values()->all());

        $this->actingAs($hrB);
        $this->assertSame([$orgB->id], AuditLog::query()->pluck('organization_id')->unique()->values()->all());
    }

    public function test_scope_is_not_applied_without_authenticated_staff_user(): void
    {
        $orgA = Organization::factory()->create();
        $orgB = Organization::factory()->create();
        app(AuditLogger::class)->record(AuditAction::UserRegistered, User::factory()->hr($orgA)->create());
        app(AuditLogger::class)->record(AuditAction::UserRegistered, User::factory()->hr($orgB)->create());

        $this->assertSame(2, AuditLog::query()->count());
    }

    public function test_database_rejects_staff_user_without_organization(): void
    {
        $this->expectException(QueryException::class);

        User::factory()->create(['role' => UserRole::HumanResources, 'organization_id' => null]);
    }

    public function test_database_rejects_candidate_linked_to_an_organization(): void
    {
        $this->expectException(QueryException::class);

        User::factory()->create([
            'role' => UserRole::Candidate,
            'organization_id' => Organization::factory()->create()->id,
        ]);
    }
}
