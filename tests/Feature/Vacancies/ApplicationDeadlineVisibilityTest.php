<?php

namespace Tests\Feature\Vacancies;

use App\Enums\VacancyStatus;
use App\Models\Organization;
use App\Models\User;
use App\Models\Vacancy;
use Carbon\CarbonImmutable;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Collection;
use Inertia\Testing\AssertableInertia;
use Tests\TestCase;

/**
 * DEF-27: una vacante publicada con el plazo de postulación vencido se veía igual que una abierta. El estado
 * formal sigue siendo «Publicada» y el detalle sigue disponible; el plazo vencido se informa aparte, con la misma
 * regla de fechas que decide si se aceptan postulaciones (`Vacancy::acceptsApplications`).
 */
class ApplicationDeadlineVisibilityTest extends TestCase
{
    use RefreshDatabase;

    private Organization $organization;

    private Vacancy $expired;

    private Vacancy $lastDay;

    private Vacancy $upcoming;

    protected function setUp(): void
    {
        parent::setUp();

        $this->travelTo(CarbonImmutable::parse('2026-11-23 10:00', config('app.timezone')));
        $this->organization = Organization::factory()->create();
        $this->expired = $this->published('VAC-2026-0901', '2026-11-01', '2026-11-22');
        $this->lastDay = $this->published('VAC-2026-0902', '2026-11-01', '2026-11-23');
        $this->upcoming = $this->published('VAC-2026-0903', '2026-11-30', '2026-12-15');
    }

    private function published(string $code, string $opens, string $closes): Vacancy
    {
        return Vacancy::factory()->for($this->organization)->configured()->published()
            ->create(['code' => $code, 'opens_at' => $opens, 'closes_at' => $closes]);
    }

    public function test_rf07_public_listing_flags_only_the_vacancy_whose_deadline_passed(): void
    {
        $this->get(route('jobs.index'))
            ->assertOk()
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->component('jobs/index')
                // El orden del listado no cambia: sigue por fecha de cierre.
                ->where('vacancies.data.0.code', 'VAC-2026-0901')
                ->where('vacancies.data.0.status.value', VacancyStatus::Published->value)
                ->where('vacancies.data.0.accepts_applications', false)
                ->where('vacancies.data.0.application_deadline_passed', true)
                ->where('vacancies.data.1.code', 'VAC-2026-0902')
                ->where('vacancies.data.1.accepts_applications', true)
                ->where('vacancies.data.1.application_deadline_passed', false)
                ->where('vacancies.data.2.code', 'VAC-2026-0903')
                ->where('vacancies.data.2.application_deadline_passed', false));
    }

    public function test_rf07_expired_vacancy_detail_stays_available_with_its_formal_status(): void
    {
        $this->get(route('jobs.show', $this->expired))
            ->assertOk()
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->component('jobs/show')
                ->where('vacancy.status.value', VacancyStatus::Published->value)
                ->where('vacancy.accepts_applications', false)
                ->where('vacancy.application_deadline_passed', true));
    }

    public function test_hr_vacancy_list_carries_the_same_flag(): void
    {
        $this->actingAs(User::factory()->hr($this->organization)->create())
            ->get(route('vacancies.index'))
            ->assertOk()
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->component('vacancies/index')
                ->where('vacancies.data', fn (Collection $data) => $data->firstWhere('code', 'VAC-2026-0901')['application_deadline_passed'] === true
                    && $data->firstWhere('code', 'VAC-2026-0902')['application_deadline_passed'] === false
                    && $data->firstWhere('code', 'VAC-2026-0903')['application_deadline_passed'] === false));
    }

    public function test_deadline_rule_matches_the_acceptance_rule_and_ignores_closed_vacancies(): void
    {
        $closed = Vacancy::factory()->for($this->organization)->configured()->closed()
            ->create(['code' => 'VAC-2026-0904', 'opens_at' => '2026-11-01', 'closes_at' => '2026-11-10']);

        $this->assertTrue($this->expired->applicationDeadlinePassed());
        $this->assertFalse($this->lastDay->applicationDeadlinePassed());
        $this->assertFalse($this->upcoming->applicationDeadlinePassed());
        $this->assertFalse($closed->applicationDeadlinePassed());
        $this->assertFalse($this->expired->applicationDeadlinePassed(CarbonImmutable::parse('2026-11-22 23:59', config('app.timezone'))));
    }
}
