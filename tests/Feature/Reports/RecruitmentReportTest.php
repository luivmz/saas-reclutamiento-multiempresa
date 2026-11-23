<?php

namespace Tests\Feature\Reports;

use App\Enums\ApplicationStatus;
use App\Enums\VacancyStatus;
use App\Models\Application;
use App\Models\ApplicationStageHistory;
use App\Models\Organization;
use App\Models\User;
use App\Models\Vacancy;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Carbon;
use Inertia\Testing\AssertableInertia;
use Tests\TestCase;

/**
 * RF-28 (candidato): reportes operativos del proceso de reclutamiento.
 *
 * Los indicadores se calculan sobre registros almacenados, siempre dentro de
 * la organización del usuario, y nunca exponen datos de personas.
 */
class RecruitmentReportTest extends TestCase
{
    use RefreshDatabase;

    private Organization $orgA;

    private Organization $orgB;

    private User $hrA;

    private User $approverA;

    private Vacancy $mathA;

    private Vacancy $artA;

    private Vacancy $draftA;

    private Vacancy $vacancyB;

    protected function setUp(): void
    {
        parent::setUp();

        $this->travelTo(Carbon::parse('2026-11-09 10:00:00'));

        $this->orgA = Organization::factory()->create();
        $this->orgB = Organization::factory()->create();
        $this->hrA = User::factory()->hr($this->orgA)->create();
        $this->approverA = User::factory()->approver($this->orgA)->create();

        $this->mathA = Vacancy::factory()->for($this->orgA)->configured()->published()->create([
            'code' => 'VAC-2026-0101', 'title' => 'Docente de Matemática', 'published_at' => '2026-10-20 09:00:00',
        ]);
        $this->artA = Vacancy::factory()->for($this->orgA)->configured()->published()->create([
            'code' => 'VAC-2026-0102', 'title' => 'Docente de Arte', 'published_at' => '2026-08-01 09:00:00',
        ]);
        $this->draftA = Vacancy::factory()->for($this->orgA)->configured()->create([
            'code' => 'VAC-2026-0103', 'title' => 'Borrador sin publicar',
        ]);
        $this->vacancyB = Vacancy::factory()->for($this->orgB)->configured()->published()->create([
            'code' => 'VAC-2026-0909', 'title' => 'Vacante de otra organización', 'published_at' => '2026-10-25 09:00:00',
        ]);

        // Matemática (A): 4 postulaciones en el período por defecto.
        $this->application($this->mathA, ApplicationStatus::Submitted, '2026-10-21 08:00:00');
        $this->application($this->mathA, ApplicationStatus::Shortlisted, '2026-10-22 08:00:00', shortlistedAt: '2026-10-24 08:00:00');
        $this->application($this->mathA, ApplicationStatus::Interview, '2026-10-28 08:00:00', shortlistedAt: '2026-10-29 08:00:00');
        // Descartada después de haber sido preseleccionada: sí alcanzó la preselección.
        $this->application($this->mathA, ApplicationStatus::Discarded, '2026-11-02 08:00:00', shortlistedAt: '2026-11-05 08:00:00');

        // Arte (A): 1 en el período y 1 fuera de él (antes de los últimos 90 días).
        $this->application($this->artA, ApplicationStatus::Evaluation, '2026-11-03 08:00:00');
        $this->application($this->artA, ApplicationStatus::Submitted, '2026-07-15 08:00:00');

        // Organización B: no debe aparecer nunca para A.
        $this->application($this->vacancyB, ApplicationStatus::Shortlisted, '2026-10-26 08:00:00', shortlistedAt: '2026-10-27 08:00:00');
        $this->application($this->vacancyB, ApplicationStatus::Submitted, '2026-10-26 09:00:00');
        $this->application($this->vacancyB, ApplicationStatus::Submitted, '2026-10-26 10:00:00');
    }

    private function application(Vacancy $vacancy, ApplicationStatus $status, string $appliedAt, ?string $shortlistedAt = null): Application
    {
        $application = Application::factory()->create([
            'vacancy_id' => $vacancy->id,
            'status' => $status,
            'applied_at' => $appliedAt,
            'stage_changed_at' => $shortlistedAt ?? $appliedAt,
        ]);

        if ($shortlistedAt !== null) {
            $history = new ApplicationStageHistory;
            $history->forceFill([
                'organization_id' => $application->organization_id,
                'application_id' => $application->id,
                'from_status' => ApplicationStatus::Submitted,
                'to_status' => ApplicationStatus::Shortlisted,
                'changed_by' => User::factory()->hr($vacancy->organization)->create()->id,
                'created_at' => $shortlistedAt,
            ])->save();
        }

        return $application;
    }

    public function test_rf28_hr_and_approver_open_the_reports_module(): void
    {
        foreach ([$this->hrA, $this->approverA] as $user) {
            $this->actingAs($user)
                ->get(route('reports.index'))
                ->assertOk()
                ->assertInertia(fn (AssertableInertia $page) => $page
                    ->component('reports/index')
                    ->has('indicators')
                    ->has('by_status', count(ApplicationStatus::cases()))
                    ->has('by_week')
                    ->has('by_vacancy')
                    ->where('filters.desde', '2026-08-12')
                    ->where('filters.hasta', '2026-11-09'));
        }
    }

    public function test_rf28_unauthorized_roles_cannot_open_the_reports_module(): void
    {
        $this->get(route('reports.index'))->assertRedirect(route('login'));

        foreach ([
            User::factory()->requester($this->orgA)->create(),
            User::factory()->evaluator($this->orgA)->create(),
            User::factory()->candidate()->create(),
        ] as $user) {
            $this->actingAs($user)->get(route('reports.index'))->assertForbidden();
        }
    }

    public function test_rf28_indicators_are_calculated_from_stored_records(): void
    {
        $this->actingAs($this->hrA)
            ->get(route('reports.index'))
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->where('indicators.applications', 5)
                ->where('indicators.published_vacancies', 1)
                ->where('indicators.vacancies_with_applications', 2)
                ->where('indicators.average_per_vacancy', 2.5)
                // Preseleccionada, en entrevista, descartada tras preselección y en evaluación.
                ->where('indicators.reached_shortlist', 4)
                ->where('indicators.shortlist_rate', 80)
                ->where('indicators.in_assessment', 2)
                // Solo las preselecciones con fecha registrada: (2 + 1 + 3) días / 3.
                ->where('indicators.average_days_to_shortlist', 2));
    }

    public function test_rf28_charts_and_table_group_the_same_filtered_records(): void
    {
        $this->actingAs($this->hrA)
            ->get(route('reports.index'))
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->where('by_status', fn ($rows) => collect($rows)->pluck('count', 'value')->all() === [
                    'postulado' => 1,
                    'preseleccionado' => 1,
                    'en_evaluacion' => 1,
                    'en_entrevista' => 1,
                    'finalista' => 0,
                    'seleccionado' => 0,
                    'no_seleccionado' => 0,
                    'descartado' => 1,
                ])
                ->where('by_week', fn ($weeks) => collect($weeks)->sum('count') === 5
                    && collect($weeks)->first()['week_start'] === '2026-08-10'
                    && collect($weeks)->last()['week_start'] === '2026-11-09'
                    && collect($weeks)->firstWhere('week_start', '2026-10-26')['count'] === 1)
                ->has('by_vacancy', 2)
                ->where('by_vacancy.0.code', 'VAC-2026-0101')
                ->where('by_vacancy.0.applications', 4)
                ->where('by_vacancy.0.reached_shortlist', 3)
                ->where('by_vacancy.0.shortlist_rate', 75)
                ->where('by_vacancy.0.in_assessment', 1)
                ->where('by_vacancy.1.code', 'VAC-2026-0102')
                ->where('by_vacancy.1.applications', 1));
    }

    public function test_rf28_reports_never_include_records_of_another_organization(): void
    {
        $this->actingAs($this->approverA)
            ->get(route('reports.index', ['desde' => '2026-01-01', 'hasta' => '2026-12-31']))
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->where('indicators.applications', 6)
                ->where('by_vacancy', fn ($rows) => collect($rows)->pluck('code')->doesntContain('VAC-2026-0909'))
                ->where('vacancies', fn ($options) => collect($options)->pluck('value')->doesntContain((string) $this->vacancyB->id)));

        $this->actingAs(User::factory()->hr($this->orgB)->create())
            ->get(route('reports.index', ['desde' => '2026-01-01', 'hasta' => '2026-12-31']))
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->where('indicators.applications', 3)
                ->where('indicators.reached_shortlist', 1)
                ->has('by_vacancy', 1)
                ->where('by_vacancy.0.code', 'VAC-2026-0909'));
    }

    public function test_rf28_vacancy_of_another_organization_cannot_be_used_as_filter(): void
    {
        $this->actingAs($this->hrA)
            ->from(route('reports.index'))
            ->get(route('reports.index', ['vacante' => $this->vacancyB->id]))
            ->assertRedirect(route('reports.index'))
            ->assertSessionHasErrors('vacante');
    }

    public function test_rf28_period_filter_changes_indicators_charts_and_table(): void
    {
        $this->actingAs($this->hrA)
            ->get(route('reports.index', ['desde' => '2026-07-01', 'hasta' => '2026-07-31']))
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->where('filters.desde', '2026-07-01')
                ->where('filters.hasta', '2026-07-31')
                ->where('indicators.applications', 1)
                ->where('indicators.published_vacancies', 0)
                ->where('indicators.reached_shortlist', 0)
                ->where('indicators.shortlist_rate', 0)
                ->where('indicators.average_days_to_shortlist', null)
                ->has('by_vacancy', 1)
                ->where('by_vacancy.0.code', 'VAC-2026-0102')
                ->where('by_week', fn ($weeks) => collect($weeks)->sum('count') === 1));
    }

    public function test_rf28_vacancy_and_status_filters_narrow_every_section(): void
    {
        $this->actingAs($this->hrA)
            ->get(route('reports.index', ['vacante' => $this->mathA->id]))
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->where('filters.vacante', (string) $this->mathA->id)
                ->where('indicators.applications', 4)
                ->where('indicators.published_vacancies', 1)
                ->has('by_vacancy', 1));

        $this->actingAs($this->hrA)
            ->get(route('reports.index', ['estado' => ApplicationStatus::Submitted->value]))
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->where('filters.estado', 'postulado')
                ->where('indicators.applications', 1)
                ->where('indicators.reached_shortlist', 0)
                ->where('by_status', fn ($rows) => collect($rows)->sum('count') === 1));
    }

    public function test_rf28_filters_are_validated(): void
    {
        $this->actingAs($this->hrA)->from(route('reports.index'));

        $this->get(route('reports.index', ['desde' => '2026-11-09', 'hasta' => '2026-11-01']))
            ->assertSessionHasErrors('hasta');
        $this->get(route('reports.index', ['desde' => 'ayer']))
            ->assertSessionHasErrors('desde');
        $this->get(route('reports.index', ['estado' => 'contratado']))
            ->assertSessionHasErrors('estado');
        $this->get(route('reports.index', ['desde' => '2024-01-01', 'hasta' => '2026-11-09']))
            ->assertSessionHasErrors('desde');
    }

    public function test_rf28_draft_vacancies_are_not_offered_as_filter_options(): void
    {
        $this->actingAs($this->hrA)
            ->get(route('reports.index'))
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->where('vacancies', fn ($options) => collect($options)->pluck('value')->sort()->values()->all() === collect([$this->mathA->id, $this->artA->id])->map(fn ($id) => (string) $id)->sort()->values()->all()));

        $this->assertSame(VacancyStatus::Draft, $this->draftA->status);
    }

    public function test_rf28_reports_expose_aggregates_only_and_no_personal_data(): void
    {
        $candidate = Application::query()->withoutGlobalScopes()->where('vacancy_id', $this->mathA->id)->firstOrFail()->candidate;

        $response = $this->actingAs($this->hrA)->get(route('reports.index'));

        $page = $response->viewData('page')['props'];
        $props = json_encode(array_intersect_key($page, array_flip(['indicators', 'by_status', 'by_week', 'by_vacancy', 'vacancies', 'statuses'])));

        $this->assertStringNotContainsString($candidate->name, $props);
        $this->assertStringNotContainsString($candidate->email, $props);
        $this->assertStringNotContainsString('candidate', $props);
        $this->assertStringNotContainsString('score', $props);
    }

    public function test_rf28_empty_organization_shows_zeros_instead_of_errors(): void
    {
        $empty = Organization::factory()->create();

        $this->actingAs(User::factory()->approver($empty)->create())
            ->get(route('reports.index'))
            ->assertOk()
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->where('indicators.applications', 0)
                ->where('indicators.average_per_vacancy', null)
                ->where('indicators.shortlist_rate', null)
                ->has('by_vacancy', 0)
                ->has('vacancies', 0));
    }
}
