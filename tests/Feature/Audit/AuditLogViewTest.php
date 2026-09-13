<?php

namespace Tests\Feature\Audit;

use App\Enums\AuditAction;
use App\Models\JobRequest;
use App\Models\Organization;
use App\Models\User;
use App\Models\Vacancy;
use App\Services\Audit\AuditLogger;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Auth;
use Inertia\Testing\AssertableInertia;
use Tests\TestCase;

class AuditLogViewTest extends TestCase
{
    use RefreshDatabase;

    private Organization $orgA;

    private Organization $orgB;

    private User $approverA;

    private User $hrA;

    private JobRequest $jobRequestA;

    private JobRequest $jobRequestB;

    protected function setUp(): void
    {
        parent::setUp();

        $this->orgA = Organization::factory()->create();
        $this->orgB = Organization::factory()->create();
        $this->approverA = User::factory()->approver($this->orgA)->create();
        $this->hrA = User::factory()->hr($this->orgA)->create();
        $requesterA = User::factory()->requester($this->orgA)->create();
        $requesterB = User::factory()->requester($this->orgB)->create();

        $this->jobRequestA = JobRequest::factory()->requestedBy($requesterA)->create(['code' => 'REQ-2026-0101']);
        $this->jobRequestB = JobRequest::factory()->requestedBy($requesterB)->create(['code' => 'REQ-2026-0909']);
        $vacancyA = Vacancy::factory()->for($this->orgA)->configured()->published()->create(['code' => 'VAC-2026-0101']);
        $candidate = User::factory()->candidate()->create();

        $this->travelTo(now()->subHours(3));
        $this->record(AuditAction::JobRequestCreated, $this->jobRequestA, $requesterA, ['code' => 'REQ-2026-0101', 'comment' => 'Nota interna privada']);
        $this->record(AuditAction::JobRequestCreated, $this->jobRequestB, $requesterB, ['code' => 'REQ-2026-0909']);
        $this->record(AuditAction::UserRegistered, $candidate, $candidate, ['channel' => 'autoregistro']);
        $this->travelBack();
        $this->travelTo(now()->subHour());
        $this->record(AuditAction::VacancyPublished, $vacancyA, $this->hrA, ['code' => 'VAC-2026-0101']);
        $this->travelBack();
        Auth::logout();
    }

    /**
     * @param  array<string, mixed>  $metadata
     */
    private function record(AuditAction $action, $subject, User $actor, array $metadata): void
    {
        app(AuditLogger::class)->record($action, $subject, $metadata, $actor);
    }

    public function test_rf27_approver_views_the_organization_audit_trail_latest_first(): void
    {
        $this->actingAs($this->approverA)
            ->get(route('audit.index'))
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->component('audit/index')
                ->has('logs.data', 2)
                ->where('logs.data.0.action.value', AuditAction::VacancyPublished->value)
                ->where('logs.data.0.actor', $this->hrA->name)
                ->where('logs.data.0.entity.type', 'vacancy')
                ->where('logs.data.0.entity.label', 'Vacante')
                ->where('logs.data.1.action.value', AuditAction::JobRequestCreated->value)
                ->where('logs.data.1.entity.id', $this->jobRequestA->id));
    }

    public function test_rf27_unauthorized_roles_cannot_view_the_audit_trail(): void
    {
        $this->get(route('audit.index'))->assertRedirect(route('login'));

        foreach ([
            $this->hrA,
            User::factory()->requester($this->orgA)->create(),
            User::factory()->evaluator($this->orgA)->create(),
            User::factory()->candidate()->create(),
        ] as $user) {
            $this->actingAs($user)->get(route('audit.index'))->assertForbidden();
        }
    }

    public function test_rf27_organization_never_sees_audit_logs_of_another_organization(): void
    {
        $this->actingAs($this->approverA)
            ->get(route('audit.index'))
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->where('logs.data', fn ($logs) => collect($logs)->every(fn ($log) => $log['entity']['id'] !== $this->jobRequestB->id || $log['entity']['type'] !== 'job_request')));

        $this->actingAs(User::factory()->approver($this->orgB)->create())
            ->get(route('audit.index'))
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->has('logs.data', 1)
                ->where('logs.data.0.entity.id', $this->jobRequestB->id));
    }

    public function test_rf27_logs_without_organization_are_not_listed(): void
    {
        $this->actingAs($this->approverA)
            ->get(route('audit.index', ['accion' => AuditAction::UserRegistered->value]))
            ->assertInertia(fn (AssertableInertia $page) => $page->has('logs.data', 0));
    }

    public function test_rf27_audit_trail_can_be_filtered_by_action(): void
    {
        $this->actingAs($this->approverA)
            ->get(route('audit.index', ['accion' => AuditAction::JobRequestCreated->value]))
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->has('logs.data', 1)
                ->where('logs.data.0.entity.id', $this->jobRequestA->id)
                ->where('filters.accion', AuditAction::JobRequestCreated->value));
    }

    public function test_rf27_view_shows_only_a_safe_summary(): void
    {
        $this->actingAs($this->approverA)
            ->get(route('audit.index', ['accion' => AuditAction::JobRequestCreated->value]))
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->missing('logs.data.0.metadata')
                ->missing('logs.data.0.ip_address')
                ->where('logs.data.0.details', function ($details) {
                    $values = collect($details)->pluck('value');

                    return $values->contains('REQ-2026-0101') && ! $values->contains('Nota interna privada');
                }));
    }
}
