<?php

namespace Tests\Feature\Frontend;

use App\Http\Requests\Candidates\CandidateCvRequest;
use App\Models\CandidateProfile;
use App\Models\Organization;
use App\Models\User;
use App\Models\Vacancy;
use Carbon\CarbonImmutable;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;
use Inertia\Testing\AssertableInertia;
use Tests\TestCase;

/**
 * Lote 2 de UX: la portada cuenta solo las convocatorias que hoy aceptan postulaciones y anuncia los requisitos
 * reales del perfil y del CV, tomados de las mismas reglas que los validan.
 */
class HomePageTest extends TestCase
{
    use RefreshDatabase;

    public function test_open_vacancy_count_uses_the_same_rule_that_allows_applying(): void
    {
        $this->travelTo(CarbonImmutable::parse('2026-11-23 10:00', config('app.timezone')));
        $orgA = Organization::factory()->create();
        $orgB = Organization::factory()->create();
        $factory = fn (Organization $org) => Vacancy::factory()->for($org)->configured();

        $factory($orgA)->published()->create(['opens_at' => '2026-11-01', 'closes_at' => '2026-12-01']);
        $factory($orgB)->published()->create(['opens_at' => '2026-11-01', 'closes_at' => '2026-11-23']);
        $factory($orgA)->published()->create(['opens_at' => '2026-11-01', 'closes_at' => '2026-11-22']);
        $factory($orgA)->published()->create(['opens_at' => '2026-11-30', 'closes_at' => '2026-12-10']);
        $factory($orgA)->create(['opens_at' => '2026-11-01', 'closes_at' => '2026-12-01']);
        $factory($orgA)->closed()->create(['opens_at' => '2026-10-01', 'closes_at' => '2026-10-20']);

        $expected = Vacancy::query()->withoutGlobalScopes()->get()->filter->acceptsApplications()->count();
        $this->assertSame(2, $expected);

        $this->get(route('home'))
            ->assertOk()
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->component('welcome')
                ->where('convocatoriasAbiertas', $expected));
    }

    public function test_home_announces_the_requirements_that_the_validation_enforces(): void
    {
        $this->get(route('home'))
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->where('requisitos.perfil', array_values(CandidateProfile::REQUIRED_FIELDS))
                ->where('requisitos.cv.formato', 'PDF')
                ->where('requisitos.cv.max_kb', CandidateCvRequest::maxKilobytes()));

        Storage::fake('local');
        $candidate = User::factory()->candidate()->create();
        $max = CandidateCvRequest::maxKilobytes();

        $this->actingAs($candidate)
            ->post(route('candidate.cv.store'), ['cv' => UploadedFile::fake()->create('cv.pdf', $max, 'application/pdf')])
            ->assertSessionHasNoErrors();
        $this->post(route('candidate.cv.store'), ['cv' => UploadedFile::fake()->create('cv.pdf', $max + 1, 'application/pdf')])
            ->assertSessionHasErrors('cv');
        $this->post(route('candidate.cv.store'), ['cv' => UploadedFile::fake()->create('cv.docx', 100, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')])
            ->assertSessionHasErrors('cv');
    }

    public function test_cv_limit_never_exceeds_five_megabytes_even_if_configuration_is_higher(): void
    {
        config(['recruitment.cv.max_kb' => 10240]);
        $this->assertSame(5120, CandidateCvRequest::maxKilobytes());

        config(['recruitment.cv.max_kb' => 2048]);
        $this->assertSame(2048, CandidateCvRequest::maxKilobytes());
    }
}
