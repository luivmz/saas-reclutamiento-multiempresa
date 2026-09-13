<?php

namespace Tests\Feature\Tenancy;

use App\Enums\ApplicationStatus;
use App\Enums\JobRequestStatus;
use App\Models\Application;
use App\Enums\VacancyStatus;
use App\Models\JobRequest;
use App\Models\Organization;
use App\Models\User;
use App\Models\Vacancy;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Inertia\Testing\AssertableInertia;
use Tests\TestCase;

class CrossTenantAccessTest extends TestCase
{
    use RefreshDatabase;

    private Organization $orgA;

    private Organization $orgB;

    protected function setUp(): void
    {
        parent::setUp();

        $this->orgA = Organization::factory()->create(['name' => 'Colegio Andino (Demo)']);
        $this->orgB = Organization::factory()->create(['name' => 'Organización Demo B']);
    }

    public function test_hr_of_other_organization_cannot_view_or_review_job_requests(): void
    {
        $jobRequest = JobRequest::factory()->for($this->orgA)->submitted()->create();
        $hrB = User::factory()->hr($this->orgB)->create();

        $this->actingAs($hrB)->get(route('job-requests.show', $jobRequest))->assertNotFound();
        $this->actingAs($hrB)->post(route('job-requests.validate', $jobRequest))->assertNotFound();

        $this->assertSame(JobRequestStatus::Submitted, $jobRequest->fresh()->status);
    }

    public function test_approver_of_other_organization_cannot_decide_job_requests(): void
    {
        $jobRequest = JobRequest::factory()->for($this->orgA)->validated()->create();

        $this->actingAs(User::factory()->approver($this->orgB)->create())
            ->post(route('job-requests.decide', $jobRequest), ['decision' => 'aprobar'])
            ->assertNotFound();

        $this->assertSame(JobRequestStatus::Validated, $jobRequest->fresh()->status);
    }

    public function test_job_request_listing_only_contains_own_organization(): void
    {
        JobRequest::factory()->for($this->orgA)->submitted()->count(2)->create();
        JobRequest::factory()->for($this->orgB)->submitted()->count(3)->create();

        $this->actingAs(User::factory()->hr($this->orgB)->create())
            ->get(route('job-requests.index'))
            ->assertInertia(fn (AssertableInertia $page) => $page->has('jobRequests.data', 3));
    }

    public function test_hr_of_other_organization_cannot_view_edit_or_publish_vacancies(): void
    {
        $vacancy = Vacancy::factory()->for($this->orgA)->configured()->create();
        $hrB = User::factory()->hr($this->orgB)->create();

        $this->actingAs($hrB)->get(route('vacancies.show', $vacancy))->assertNotFound();
        $this->actingAs($hrB)->get(route('vacancies.edit', $vacancy))->assertNotFound();
        $this->actingAs($hrB)->post(route('vacancies.publish', $vacancy))->assertNotFound();

        $this->assertSame(VacancyStatus::Draft, $vacancy->fresh()->status);
    }

    public function test_hr_of_other_organization_cannot_list_view_or_move_applications(): void
    {
        $vacancy = Vacancy::factory()->for($this->orgA)->configured()->published()->create();
        $application = Application::factory()->for($vacancy)->create();
        $hrB = User::factory()->hr($this->orgB)->create();

        $this->actingAs($hrB)->get(route('vacancies.applications.index', $vacancy))->assertNotFound();
        $this->actingAs($hrB)->get(route('applications.show', $application))->assertNotFound();
        $this->actingAs($hrB)->post(route('applications.shortlist', $application))->assertNotFound();

        $this->assertSame(ApplicationStatus::Submitted, $application->fresh()->status);
    }

    public function test_rf20_hr_of_other_organization_cannot_modify_vacancy_criteria(): void
    {
        $vacancy = Vacancy::factory()->for($this->orgA)->configured()->create();
        $weights = $vacancy->criteria()->withoutGlobalScopes()->pluck('weight')->all();

        $this->actingAs(User::factory()->hr($this->orgB)->create())
            ->put(route('vacancies.update', $vacancy), [
                'title' => 'Intento cruzado',
                'criteria' => [['name' => 'Único', 'stage' => 'evaluacion', 'weight' => 100, 'min_score' => 0, 'max_score' => 20]],
            ])
            ->assertNotFound();

        $this->assertSame($weights, $vacancy->criteria()->withoutGlobalScopes()->pluck('weight')->all());
        $this->assertNotSame('Intento cruzado', $vacancy->fresh()->title);
    }

    public function test_hr_cannot_create_vacancy_from_another_organization_request(): void
    {
        $jobRequest = JobRequest::factory()->for($this->orgA)->approved()->create();

        $this->actingAs(User::factory()->hr($this->orgB)->create())
            ->post(route('vacancies.store'), ['job_request_id' => $jobRequest->id, 'title' => 'Intento cruzado'])
            ->assertSessionHasErrors('job_request_id');

        $this->assertSame(0, Vacancy::query()->withoutGlobalScopes()->count());
    }
}
