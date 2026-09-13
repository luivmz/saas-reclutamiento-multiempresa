<?php

namespace Tests\Feature\Vacancies;

use App\Enums\AuditAction;
use App\Enums\VacancyStatus;
use App\Models\AuditLog;
use App\Models\JobRequest;
use App\Models\Organization;
use App\Models\User;
use App\Models\Vacancy;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Inertia\Testing\AssertableInertia;
use Tests\TestCase;

class VacancyPublicationTest extends TestCase
{
    use RefreshDatabase;

    private Organization $organization;

    private User $hr;

    protected function setUp(): void
    {
        parent::setUp();

        $this->organization = Organization::factory()->create();
        $this->hr = User::factory()->hr($this->organization)->create();
    }

    /**
     * @return array<string, mixed>
     */
    private function payload(JobRequest $jobRequest, array $overrides = []): array
    {
        return array_replace_recursive([
            'job_request_id' => $jobRequest->id,
            'title' => 'Docente de Matemática - Secundaria',
            'summary' => 'Buscamos docente para el nivel secundario con enfoque por competencias.',
            'location' => 'Huancayo, Junín',
            'contract_type' => 'tiempo_completo',
            'positions' => 1,
            'opens_at' => now()->toDateString(),
            'closes_at' => now()->addDays(15)->toDateString(),
            'profile' => [
                'education' => 'Licenciatura en Educación, especialidad Matemática',
                'experience' => 'Mínimo 2 años en educación secundaria',
                'functions' => 'Planificar sesiones, evaluar aprendizajes y participar en tutoría.',
                'competencies' => 'Comunicación, trabajo en equipo, manejo de TIC.',
            ],
            'criteria' => [
                ['name' => 'Conocimientos pedagógicos', 'stage' => 'evaluacion', 'weight' => 40, 'min_score' => 0, 'max_score' => 20],
                ['name' => 'Clase modelo', 'stage' => 'evaluacion', 'weight' => 30, 'min_score' => 0, 'max_score' => 20],
                ['name' => 'Entrevista personal', 'stage' => 'entrevista', 'weight' => 30, 'min_score' => 0, 'max_score' => 20],
            ],
        ], $overrides);
    }

    public function test_rf05_rf06_hr_creates_vacancy_with_profile_and_criteria_from_approved_request(): void
    {
        $jobRequest = JobRequest::factory()->for($this->organization)->approved()->create();

        $this->actingAs($this->hr)->post(route('vacancies.store'), $this->payload($jobRequest))->assertSessionHasNoErrors();

        $vacancy = Vacancy::query()->sole();
        $this->assertSame(VacancyStatus::Draft, $vacancy->status);
        $this->assertSame($jobRequest->id, $vacancy->job_request_id);
        $this->assertSame('Mínimo 2 años en educación secundaria', $vacancy->profile->experience);
        $this->assertSame(3, $vacancy->criteria()->count());
        $this->assertTrue(AuditLog::query()->where('action', AuditAction::VacancyCreated)->exists());
    }

    public function test_rf05_vacancy_cannot_be_created_from_a_request_that_is_not_approved(): void
    {
        $jobRequest = JobRequest::factory()->for($this->organization)->validated()->create();

        $this->actingAs($this->hr)->post(route('vacancies.store'), $this->payload($jobRequest))->assertSessionHasErrors('job_request_id');

        $this->assertSame(0, Vacancy::query()->count());
    }

    public function test_rf06_validation_report_lists_issues_of_an_invalid_vacancy(): void
    {
        $vacancy = Vacancy::factory()->for($this->organization)->configured()->create();
        $vacancy->criteria()->first()->update(['weight' => 5]);

        $this->actingAs($this->hr)
            ->get(route('vacancies.show', $vacancy))
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->component('vacancies/show')
                ->where('validation.publishable', false)
                ->has('validation.issues', 1));
    }

    public function test_rf07_hr_publishes_a_valid_vacancy_and_it_becomes_public(): void
    {
        $vacancy = Vacancy::factory()->for($this->organization)->configured()->create();

        $this->actingAs($this->hr)->post(route('vacancies.publish', $vacancy))->assertSessionHasNoErrors();

        $vacancy->refresh();
        $this->assertSame(VacancyStatus::Published, $vacancy->status);
        $this->assertNotNull($vacancy->published_at);
        $this->assertSame($this->hr->id, $vacancy->published_by);
        $this->assertTrue(AuditLog::query()->where('action', AuditAction::VacancyPublished)->exists());

        $this->get(route('jobs.index'))
            ->assertInertia(fn (AssertableInertia $page) => $page->component('jobs/index')->has('vacancies.data', 1));
    }

    public function test_rf07_invalid_weights_prevent_publication(): void
    {
        $vacancy = Vacancy::factory()->for($this->organization)->configured()->create();
        $vacancy->criteria()->first()->update(['weight' => 10]);

        $this->actingAs($this->hr)->post(route('vacancies.publish', $vacancy))->assertSessionHasErrors('workflow');

        $this->assertSame(VacancyStatus::Draft, $vacancy->fresh()->status);
    }

    public function test_rf07_vacancy_without_criteria_or_with_expired_deadline_cannot_be_published(): void
    {
        $withoutCriteria = Vacancy::factory()->for($this->organization)->configured()->create();
        $withoutCriteria->criteria()->delete();
        $expired = Vacancy::factory()->for($this->organization)->configured()->create(['opens_at' => now()->subDays(10), 'closes_at' => now()->subDay()]);

        $this->actingAs($this->hr)->post(route('vacancies.publish', $withoutCriteria))->assertSessionHasErrors('workflow');
        $this->actingAs($this->hr)->post(route('vacancies.publish', $expired))->assertSessionHasErrors('workflow');

        $this->assertSame(VacancyStatus::Draft, $withoutCriteria->fresh()->status);
        $this->assertSame(VacancyStatus::Draft, $expired->fresh()->status);
    }

    public function test_draft_vacancies_are_not_public(): void
    {
        $vacancy = Vacancy::factory()->for($this->organization)->configured()->create();

        $this->get(route('jobs.show', $vacancy))->assertNotFound();
    }

    public function test_published_vacancy_configuration_cannot_be_modified(): void
    {
        $vacancy = Vacancy::factory()->for($this->organization)->configured()->published()->create();

        $this->actingAs($this->hr)
            ->put(route('vacancies.update', $vacancy), $this->payload($vacancy->jobRequest, ['title' => 'Cambio no permitido']))
            ->assertSessionHasErrors('workflow');

        $this->assertNotSame('Cambio no permitido', $vacancy->fresh()->title);
    }

    public function test_non_hr_roles_cannot_manage_vacancies(): void
    {
        $vacancy = Vacancy::factory()->for($this->organization)->configured()->create();

        $this->actingAs(User::factory()->requester($this->organization)->create())->get(route('vacancies.index'))->assertForbidden();
        $this->actingAs(User::factory()->evaluator($this->organization)->create())->post(route('vacancies.publish', $vacancy))->assertForbidden();
        $this->actingAs(User::factory()->approver($this->organization)->create())->post(route('vacancies.publish', $vacancy))->assertForbidden();

        $this->assertSame(VacancyStatus::Draft, $vacancy->fresh()->status);
    }
}
