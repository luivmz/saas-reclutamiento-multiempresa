<?php

namespace Tests\Feature\JobRequests;

use App\Enums\AuditAction;
use App\Enums\JobRequestStatus;
use App\Models\AuditLog;
use App\Models\JobRequest;
use App\Models\Organization;
use App\Models\User;
use App\Notifications\JobRequestRejectedNotification;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Notification;
use Inertia\Testing\AssertableInertia;
use Tests\TestCase;

class JobRequestWorkflowTest extends TestCase
{
    use RefreshDatabase;

    private Organization $organization;

    private User $requester;

    private User $hr;

    private User $approver;

    protected function setUp(): void
    {
        parent::setUp();

        $this->organization = Organization::factory()->create();
        $this->requester = User::factory()->requester($this->organization)->create();
        $this->hr = User::factory()->hr($this->organization)->create();
        $this->approver = User::factory()->approver($this->organization)->create();
    }

    /**
     * @return array<string, mixed>
     */
    private function payload(array $overrides = []): array
    {
        return array_merge([
            'position_title' => 'Docente de Matemática - Secundaria',
            'area' => 'Coordinación Académica de Secundaria',
            'headcount' => 1,
            'contract_type' => 'tiempo_completo',
            'justification' => 'Cobertura de plaza por incremento de secciones en el nivel secundario.',
            'required_by' => now()->addMonth()->toDateString(),
        ], $overrides);
    }

    public function test_rf01_requester_registers_a_job_request(): void
    {
        $this->actingAs($this->requester)
            ->post(route('job-requests.store'), $this->payload())
            ->assertRedirect();

        $jobRequest = JobRequest::query()->sole();

        $this->assertSame(JobRequestStatus::Draft, $jobRequest->status);
        $this->assertSame($this->organization->id, $jobRequest->organization_id);
        $this->assertSame($this->requester->id, $jobRequest->requested_by);
        $this->assertMatchesRegularExpression('/^REQ-\d{4}-\d{4}$/', $jobRequest->code);
        $this->assertSame(1, $jobRequest->statusHistories()->count());
        $this->assertTrue(AuditLog::query()->where('action', AuditAction::JobRequestCreated)->where('auditable_id', $jobRequest->id)->exists());
    }

    public function test_rf01_required_fields_are_validated(): void
    {
        $this->actingAs($this->requester)
            ->post(route('job-requests.store'), $this->payload(['position_title' => '', 'headcount' => 0, 'justification' => '']))
            ->assertSessionHasErrors(['position_title', 'headcount', 'justification']);

        $this->assertSame(0, JobRequest::query()->count());
    }

    public function test_rf02_hr_observes_and_requester_corrects_and_resubmits(): void
    {
        $jobRequest = JobRequest::factory()->for($this->organization)->requestedBy($this->requester)->create();

        $this->actingAs($this->requester)->post(route('job-requests.submit', $jobRequest))->assertSessionHasNoErrors();
        $this->assertSame(JobRequestStatus::Submitted, $jobRequest->fresh()->status);

        $this->actingAs($this->hr)
            ->post(route('job-requests.observe', $jobRequest), ['comment' => 'Precisar el sustento de la plaza.'])
            ->assertSessionHasNoErrors();
        $this->assertSame(JobRequestStatus::Observed, $jobRequest->fresh()->status);
        $this->assertSame('Precisar el sustento de la plaza.', $jobRequest->fresh()->observation);

        $this->actingAs($this->requester)
            ->put(route('job-requests.update', $jobRequest), $this->payload(['justification' => 'Sustento corregido: se abrieron dos nuevas secciones de 3.er grado.']))
            ->assertSessionHasNoErrors();
        $this->actingAs($this->requester)->post(route('job-requests.submit', $jobRequest))->assertSessionHasNoErrors();

        $jobRequest->refresh();
        $this->assertSame(JobRequestStatus::Submitted, $jobRequest->status);
        $this->assertStringContainsString('Sustento corregido', $jobRequest->justification);
        $this->assertSame(
            ['enviado', 'observado', 'enviado'],
            $jobRequest->statusHistories()->orderBy('id')->get()->map(fn ($history) => $history->to_status->value)->all(),
        );
    }

    public function test_rf02_observation_requires_a_comment(): void
    {
        $jobRequest = JobRequest::factory()->for($this->organization)->requestedBy($this->requester)->submitted()->create();

        $this->actingAs($this->hr)
            ->post(route('job-requests.observe', $jobRequest), ['comment' => ''])
            ->assertSessionHasErrors('comment');

        $this->assertSame(JobRequestStatus::Submitted, $jobRequest->fresh()->status);
    }

    public function test_rf03_hr_validates_and_approver_approves(): void
    {
        $jobRequest = JobRequest::factory()->for($this->organization)->requestedBy($this->requester)->submitted()->create();

        $this->actingAs($this->hr)->post(route('job-requests.validate', $jobRequest))->assertSessionHasNoErrors();
        $this->assertSame(JobRequestStatus::Validated, $jobRequest->fresh()->status);

        $this->actingAs($this->approver)
            ->post(route('job-requests.decide', $jobRequest), ['decision' => 'aprobar', 'comment' => 'Conforme.'])
            ->assertSessionHasNoErrors();

        $jobRequest->refresh();
        $this->assertSame(JobRequestStatus::Approved, $jobRequest->status);
        $this->assertSame($this->approver->id, $jobRequest->decided_by);
        $this->assertNotNull($jobRequest->decided_at);
        $this->assertTrue(AuditLog::query()->where('action', AuditAction::JobRequestApproved)->exists());
    }

    public function test_rf04_rejection_notifies_the_requester(): void
    {
        Notification::fake();
        $jobRequest = JobRequest::factory()->for($this->organization)->requestedBy($this->requester)->validated()->create();

        $this->actingAs($this->approver)
            ->post(route('job-requests.decide', $jobRequest), ['decision' => 'rechazar', 'comment' => 'No existe presupuesto aprobado para la plaza.'])
            ->assertSessionHasNoErrors();

        $this->assertSame(JobRequestStatus::Rejected, $jobRequest->fresh()->status);
        Notification::assertSentTo($this->requester, JobRequestRejectedNotification::class);
        $this->assertTrue(AuditLog::query()->where('action', AuditAction::JobRequestRejected)->exists());
    }

    public function test_rf04_rejection_requires_a_comment(): void
    {
        $jobRequest = JobRequest::factory()->for($this->organization)->requestedBy($this->requester)->validated()->create();

        $this->actingAs($this->approver)
            ->post(route('job-requests.decide', $jobRequest), ['decision' => 'rechazar', 'comment' => ''])
            ->assertSessionHasErrors('comment');

        $this->assertSame(JobRequestStatus::Validated, $jobRequest->fresh()->status);
    }

    public function test_invalid_transition_is_rejected_and_state_is_kept(): void
    {
        $jobRequest = JobRequest::factory()->for($this->organization)->requestedBy($this->requester)->submitted()->create();

        $this->actingAs($this->approver)
            ->post(route('job-requests.decide', $jobRequest), ['decision' => 'aprobar'])
            ->assertSessionHasErrors('workflow');

        $this->assertSame(JobRequestStatus::Submitted, $jobRequest->fresh()->status);
    }

    public function test_submitted_request_cannot_be_edited(): void
    {
        $jobRequest = JobRequest::factory()->for($this->organization)->requestedBy($this->requester)->submitted()->create();

        $this->actingAs($this->requester)
            ->put(route('job-requests.update', $jobRequest), $this->payload(['position_title' => 'Cambio no permitido']))
            ->assertSessionHasErrors('workflow');

        $this->assertNotSame('Cambio no permitido', $jobRequest->fresh()->position_title);
    }

    public function test_roles_without_permission_are_forbidden(): void
    {
        $jobRequest = JobRequest::factory()->for($this->organization)->requestedBy($this->requester)->validated()->create();
        $evaluator = User::factory()->evaluator($this->organization)->create();

        $this->actingAs($this->requester)->post(route('job-requests.decide', $jobRequest), ['decision' => 'aprobar'])->assertForbidden();
        $this->actingAs($this->hr)->post(route('job-requests.decide', $jobRequest), ['decision' => 'aprobar'])->assertForbidden();
        $this->actingAs($this->approver)->post(route('job-requests.store'), $this->payload())->assertForbidden();
        $this->actingAs($evaluator)->get(route('job-requests.index'))->assertForbidden();
        $this->actingAs(User::factory()->candidate()->create())->get(route('job-requests.index'))->assertForbidden();

        $this->assertSame(JobRequestStatus::Validated, $jobRequest->fresh()->status);
    }

    public function test_requester_only_lists_own_requests_and_cannot_view_others(): void
    {
        $otherRequester = User::factory()->requester($this->organization)->create();
        JobRequest::factory()->for($this->organization)->requestedBy($this->requester)->create();
        $foreign = JobRequest::factory()->for($this->organization)->requestedBy($otherRequester)->create();

        $this->actingAs($this->requester)
            ->get(route('job-requests.index'))
            ->assertInertia(fn (AssertableInertia $page) => $page->component('job-requests/index')->has('jobRequests.data', 1));

        $this->actingAs($this->requester)->get(route('job-requests.show', $foreign))->assertForbidden();
    }
}
