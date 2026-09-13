<?php

namespace Tests\Feature\Audit;

use App\Enums\AuditAction;
use App\Enums\CriterionStage;
use App\Models\Application;
use App\Models\AuditLog;
use App\Models\CandidateProfile;
use App\Models\Evaluation;
use App\Models\Interview;
use App\Models\JobRequest;
use App\Models\Organization;
use App\Models\SelectionDecision;
use App\Models\User;
use App\Models\Vacancy;
use App\Services\Audit\AuditLogger;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\QueryException;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Notification;
use Illuminate\Support\Facades\Route;
use Tests\TestCase;

class AuditTrailTest extends TestCase
{
    use RefreshDatabase;

    private function assertAudited(Organization $organization, AuditAction $action, Model $subject, User $actor): void
    {
        $this->assertTrue(
            AuditLog::query()->withoutGlobalScopes()
                ->where('organization_id', $organization->id)
                ->where('action', $action)
                ->where('auditable_type', $subject->getMorphClass())
                ->where('auditable_id', $subject->getKey())
                ->where('user_id', $actor->id)
                ->exists(),
            "Missing audit [{$action->value}] on [{$subject->getMorphClass()}#{$subject->getKey()}] by user #{$actor->id}.",
        );
    }

    public function test_rf27_full_process_generates_an_audit_trail_with_tenant_actor_and_entity(): void
    {
        Notification::fake();
        $organization = Organization::factory()->create();
        $requester = User::factory()->requester($organization)->create();
        $hr = User::factory()->hr($organization)->create();
        $approver = User::factory()->approver($organization)->create();
        $evaluator = User::factory()->evaluator($organization)->create();
        $candidate = User::factory()->candidate()->has(CandidateProfile::factory()->withCv(), 'candidateProfile')->create();

        $requestPayload = [
            'position_title' => 'Docente de Ciencias',
            'area' => 'Coordinación Académica',
            'headcount' => 1,
            'contract_type' => 'tiempo_completo',
            'justification' => 'Necesidad ficticia de docente para la prueba de auditoría.',
        ];

        $this->actingAs($requester)->post(route('job-requests.store'), $requestPayload)->assertSessionHasNoErrors();
        $jobRequest = JobRequest::query()->withoutGlobalScopes()->sole();
        $this->actingAs($requester)->post(route('job-requests.submit', $jobRequest))->assertSessionHasNoErrors();
        $this->actingAs($hr)->post(route('job-requests.observe', $jobRequest), ['comment' => 'Precisar la justificación.'])->assertSessionHasNoErrors();
        $this->actingAs($requester)->put(route('job-requests.update', $jobRequest), [...$requestPayload, 'justification' => 'Justificación corregida para la prueba de auditoría.'])->assertSessionHasNoErrors();
        $this->actingAs($requester)->post(route('job-requests.submit', $jobRequest))->assertSessionHasNoErrors();
        $this->actingAs($hr)->post(route('job-requests.validate', $jobRequest))->assertSessionHasNoErrors();
        $this->actingAs($approver)->post(route('job-requests.decide', $jobRequest), ['decision' => 'aprobar'])->assertSessionHasNoErrors();

        $this->actingAs($hr)->post(route('vacancies.store'), [
            'job_request_id' => $jobRequest->id,
            'title' => 'Docente de Ciencias',
            'summary' => 'Convocatoria ficticia para la prueba de auditoría.',
            'location' => 'Huancayo',
            'contract_type' => 'tiempo_completo',
            'positions' => 1,
            'opens_at' => now()->toDateString(),
            'closes_at' => now()->addDays(10)->toDateString(),
            'profile' => ['education' => 'Licenciatura', 'experience' => '2 años', 'functions' => 'Funciones ficticias.', 'competencies' => 'Competencias ficticias.'],
            'criteria' => [
                ['name' => 'Conocimientos', 'stage' => 'evaluacion', 'weight' => 40, 'min_score' => 0, 'max_score' => 20],
                ['name' => 'Clase modelo', 'stage' => 'evaluacion', 'weight' => 30, 'min_score' => 0, 'max_score' => 20],
                ['name' => 'Entrevista', 'stage' => 'entrevista', 'weight' => 30, 'min_score' => 0, 'max_score' => 20],
            ],
        ])->assertSessionHasNoErrors();
        $vacancy = Vacancy::query()->withoutGlobalScopes()->sole();
        $criteria = $vacancy->criteria()->withoutGlobalScopes()->get();
        $this->actingAs($hr)->post(route('vacancies.publish', $vacancy))->assertSessionHasNoErrors();

        $this->actingAs($candidate)->post(route('jobs.apply', $vacancy))->assertSessionHasNoErrors();
        $application = Application::query()->withoutGlobalScopes()->sole();
        $this->actingAs($hr)->post(route('applications.shortlist', $application))->assertSessionHasNoErrors();

        $session = ['evaluator_id' => $evaluator->id, 'modality' => 'presencial', 'location' => 'Aula demo', 'scheduled_at' => now()->addDay()->format('Y-m-d H:i')];
        $this->actingAs($hr)->post(route('applications.evaluations.store', $application), [...$session, 'type' => 'conocimientos'])->assertSessionHasNoErrors();
        $evaluation = Evaluation::query()->withoutGlobalScopes()->sole();
        $evaluationCriteria = $criteria->where('stage', CriterionStage::Evaluation)->values();
        $this->actingAs($evaluator)->post(route('evaluations.results.store', $evaluation), [
            'scores' => [$evaluationCriteria[0]->id => ['score' => 17], $evaluationCriteria[1]->id => ['score' => 15]],
        ])->assertSessionHasNoErrors();

        $this->actingAs($hr)->post(route('applications.interviews.store', $application), $session)->assertSessionHasNoErrors();
        $interview = Interview::query()->withoutGlobalScopes()->sole();
        $this->actingAs($evaluator)->post(route('interviews.results.store', $interview), [
            'scores' => [$criteria->firstWhere('stage', CriterionStage::Interview)->id => ['score' => 16]],
            'outcome' => 'recomendado',
            'observations' => 'Entrevista ficticia registrada para auditoría.',
        ])->assertSessionHasNoErrors();

        $this->actingAs($hr)->post(route('applications.stage', $application), ['status' => 'finalista'])->assertSessionHasNoErrors();
        $this->actingAs($approver)->post(route('vacancies.decision.store', $vacancy), [
            'application_id' => $application->id,
            'justification' => 'Decisión humana ficticia para la prueba de auditoría.',
            'human_confirmation' => '1',
        ])->assertSessionHasNoErrors();
        $decision = SelectionDecision::query()->withoutGlobalScopes()->sole();
        $this->actingAs($hr)->post(route('vacancies.selection.store', $vacancy))->assertSessionHasNoErrors();
        $this->actingAs($hr)->post(route('vacancies.close', $vacancy))->assertSessionHasNoErrors();

        $this->assertAudited($organization, AuditAction::JobRequestCreated, $jobRequest, $requester);
        $this->assertAudited($organization, AuditAction::JobRequestSubmitted, $jobRequest, $requester);
        $this->assertAudited($organization, AuditAction::JobRequestObserved, $jobRequest, $hr);
        $this->assertAudited($organization, AuditAction::JobRequestUpdated, $jobRequest, $requester);
        $this->assertAudited($organization, AuditAction::JobRequestValidated, $jobRequest, $hr);
        $this->assertAudited($organization, AuditAction::JobRequestApproved, $jobRequest, $approver);
        $this->assertAudited($organization, AuditAction::VacancyCreated, $vacancy, $hr);
        $this->assertAudited($organization, AuditAction::VacancyPublished, $vacancy, $hr);
        $this->assertAudited($organization, AuditAction::ApplicationSubmitted, $application, $candidate);
        $this->assertAudited($organization, AuditAction::ApplicationStageChanged, $application, $hr);
        $this->assertAudited($organization, AuditAction::EvaluationScheduled, $evaluation, $hr);
        $this->assertAudited($organization, AuditAction::EvaluationResultRecorded, $evaluation, $evaluator);
        $this->assertAudited($organization, AuditAction::InterviewScheduled, $interview, $hr);
        $this->assertAudited($organization, AuditAction::InterviewResultRecorded, $interview, $evaluator);
        $this->assertAudited($organization, AuditAction::SelectionDecisionRecorded, $decision, $approver);
        $this->assertAudited($organization, AuditAction::CandidateSelected, $application, $hr);
        $this->assertAudited($organization, AuditAction::VacancyClosed, $vacancy, $hr);
        $this->assertAudited($organization, AuditAction::ProcessResultNotified, $vacancy, $hr);

        $this->assertSame(0, AuditLog::query()->withoutGlobalScopes()->whereNot('auditable_type', 'user')->whereNull('organization_id')->count());

        AuditLog::query()->withoutGlobalScopes()->get()->each(function (AuditLog $log): void {
            $metadata = json_encode($log->metadata, JSON_UNESCAPED_UNICODE);

            $this->assertDoesNotMatchRegularExpression('/password|token|secret|cookie|%PDF/i', $metadata);
            $this->assertStringNotContainsString('Decisión humana ficticia para la prueba de auditoría.', $metadata);
        });
    }

    public function test_rf27_audit_logs_are_append_only_at_database_level(): void
    {
        $candidate = User::factory()->candidate()->create();
        $log = app(AuditLogger::class)->record(AuditAction::UserRegistered, $candidate, ['channel' => 'prueba'], $candidate);

        $this->assertThrows(fn () => DB::transaction(fn () => DB::table('audit_logs')->where('id', $log->id)->update(['action' => 'alterado'])), QueryException::class);
        $this->assertThrows(fn () => DB::transaction(fn () => DB::table('audit_logs')->where('id', $log->id)->delete()), QueryException::class);

        $this->assertSame(AuditAction::UserRegistered, AuditLog::query()->findOrFail($log->id)->action);
    }

    public function test_rf27_deleting_a_user_keeps_the_audit_record_without_the_actor_reference(): void
    {
        $candidate = User::factory()->candidate()->create();
        $log = app(AuditLogger::class)->record(AuditAction::UserRegistered, $candidate, ['channel' => 'prueba'], $candidate);

        $candidate->delete();

        $kept = AuditLog::query()->findOrFail($log->id);
        $this->assertNull($kept->user_id);
        $this->assertSame(AuditAction::UserRegistered, $kept->action);
    }

    public function test_rf27_sensitive_values_are_never_stored_in_metadata(): void
    {
        $candidate = User::factory()->candidate()->create();

        $log = app(AuditLogger::class)->record(AuditAction::UserRegistered, $candidate, [
            'password_hash' => '$2y$12$abc',
            'cookie' => 'laravel_session=abc',
            'authorization' => 'Bearer abc',
            'api_key' => 'sk-demo',
            'session_token' => 'abc',
            'nested' => ['client_secret' => 'abc', 'file_contents' => '%PDF-1.4', 'code' => 'REQ-2026-0001'],
            'fields' => ['phone', 'city'],
        ]);

        $stored = $log->fresh()->metadata;

        $this->assertEquals(['nested' => ['code' => 'REQ-2026-0001'], 'fields' => ['phone', 'city']], $stored);
        foreach (['password_hash', 'cookie', 'authorization', 'api_key', 'session_token'] as $key) {
            $this->assertArrayNotHasKey($key, $stored);
        }
        $this->assertArrayNotHasKey('client_secret', $stored['nested']);
        $this->assertArrayNotHasKey('file_contents', $stored['nested']);
    }

    public function test_rf27_audit_trail_is_exposed_read_only(): void
    {
        $auditRoutes = collect(Route::getRoutes()->getRoutes())
            ->filter(fn ($route) => str_contains($route->uri(), 'auditoria') || str_contains((string) $route->getActionName(), 'Audit'));

        $this->assertNotEmpty($auditRoutes->all(), 'The audit trail must be consultable (RF-27).');
        $auditRoutes->each(fn ($route) => $this->assertSame([], array_values(array_diff($route->methods(), ['GET', 'HEAD'])), "Audit route [{$route->uri()}] must be read-only."));
    }
}
