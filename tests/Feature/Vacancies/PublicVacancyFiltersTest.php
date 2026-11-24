<?php

namespace Tests\Feature\Vacancies;

use App\Enums\ContractType;
use App\Models\Organization;
use App\Models\Vacancy;
use Carbon\CarbonImmutable;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\DB;
use Inertia\Testing\AssertableInertia;
use PHPUnit\Framework\Attributes\DataProvider;
use Tests\TestCase;

/**
 * Lote 3 de UX (RF-07): búsqueda por puesto y filtros por organización, ubicación y tipo de contrato en el
 * listado público. Las opciones y los valores aceptados salen solo de convocatorias publicadas; un borrador o una
 * vacante cerrada no aparecen ni como resultado ni como opción.
 */
class PublicVacancyFiltersTest extends TestCase
{
    use RefreshDatabase;

    private Organization $uno;

    private Organization $dos;

    private Organization $oculta;

    protected function setUp(): void
    {
        parent::setUp();

        $this->travelTo(CarbonImmutable::parse('2026-11-23 10:00', config('app.timezone')));
        $this->uno = Organization::factory()->create(['name' => 'Colegio Uno (ficticio)']);
        $this->dos = Organization::factory()->create(['name' => 'Instituto Dos (ficticio)']);
        $this->oculta = Organization::factory()->create(['name' => 'Organización Sin Publicar (ficticia)']);

        $this->published($this->uno, 'VAC-F-01', 'Docente de Matemática', 'Huancayo', ContractType::FullTime, '2026-12-10');
        $this->published($this->uno, 'VAC-F-02', 'Auxiliar de Biblioteca', 'Lima', ContractType::PartTime, '2026-12-11');
        // Publicada con el plazo vencido: sigue en el listado, con su distintivo.
        $this->published($this->dos, 'VAC-F-03', 'Docente de Inglés', 'Huancayo', ContractType::Hourly, '2026-11-20');

        // Solo en borrador o cerradas: no deben verse ni como resultado ni como opción.
        Vacancy::factory()->for($this->oculta)->configured()->create([
            'code' => 'VAC-F-90', 'title' => 'Docente Borrador', 'location' => 'Ciudad Reservada',
            'contract_type' => ContractType::FixedTerm, 'opens_at' => '2026-11-01', 'closes_at' => '2026-12-20',
        ]);
        Vacancy::factory()->for($this->oculta)->configured()->closed()->create([
            'code' => 'VAC-F-91', 'title' => 'Docente Cerrada', 'location' => 'Ciudad Reservada',
            'contract_type' => ContractType::FixedTerm, 'opens_at' => '2026-10-01', 'closes_at' => '2026-10-20',
        ]);
        Vacancy::factory()->for($this->uno)->configured()->create([
            'code' => 'VAC-F-92', 'title' => 'Docente oculto en borrador', 'location' => 'Huancayo',
            'contract_type' => ContractType::FullTime, 'opens_at' => '2026-11-01', 'closes_at' => '2026-12-20',
        ]);
    }

    private function published(Organization $org, string $code, string $title, string $location, ContractType $type, string $closes): Vacancy
    {
        return Vacancy::factory()->for($org)->configured()->published()->create([
            'code' => $code, 'title' => $title, 'location' => $location, 'contract_type' => $type,
            'opens_at' => '2026-11-01', 'closes_at' => $closes,
        ]);
    }

    /**
     * @param  array<string, mixed>  $query
     * @return list<string>
     */
    private function codes(array $query): array
    {
        $codes = [];
        $this->get(route('jobs.index', $query))
            ->assertOk()
            ->assertInertia(function (AssertableInertia $page) use (&$codes) {
                $codes = array_column($page->toArray()['props']['vacancies']['data'], 'code');
            });

        return $codes;
    }

    public function test_options_come_only_from_published_vacancies(): void
    {
        $this->get(route('jobs.index'))
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->where('options.organizaciones', [
                    ['value' => (string) $this->uno->id, 'label' => 'Colegio Uno (ficticio)'],
                    ['value' => (string) $this->dos->id, 'label' => 'Instituto Dos (ficticio)'],
                ])
                ->where('options.ubicaciones', [
                    ['value' => 'Huancayo', 'label' => 'Huancayo'],
                    ['value' => 'Lima', 'label' => 'Lima'],
                ])
                ->where('options.contratos', [
                    ['value' => 'tiempo_completo', 'label' => 'Tiempo completo'],
                    ['value' => 'tiempo_parcial', 'label' => 'Tiempo parcial'],
                    ['value' => 'por_horas', 'label' => 'Por horas'],
                ]));

        $this->get(route('jobs.index'))->assertDontSee('Organización Sin Publicar')->assertDontSee('Ciudad Reservada');
    }

    public function test_each_filter_works_on_its_own_and_keeps_the_existing_order(): void
    {
        $this->assertSame(['VAC-F-03', 'VAC-F-01', 'VAC-F-02'], $this->codes([]));
        $this->assertSame(['VAC-F-01', 'VAC-F-02'], $this->codes(['organizacion' => $this->uno->id]));
        $this->assertSame(['VAC-F-03', 'VAC-F-01'], $this->codes(['ubicacion' => 'Huancayo']));
        $this->assertSame(['VAC-F-03'], $this->codes(['contrato' => 'por_horas']));
    }

    public function test_search_and_filters_combine_with_and(): void
    {
        $this->assertSame(['VAC-F-03', 'VAC-F-01'], $this->codes(['q' => 'docente']));
        $this->assertSame(['VAC-F-01'], $this->codes(['q' => 'docente', 'ubicacion' => 'Huancayo', 'organizacion' => $this->uno->id]));
        $this->assertSame([], $this->codes(['organizacion' => $this->dos->id, 'contrato' => 'tiempo_completo']));

        $this->get(route('jobs.index', ['q' => 'docente', 'ubicacion' => 'Huancayo', 'contrato' => 'tiempo_completo']))
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->where('filters', ['q' => 'docente', 'organizacion' => null, 'ubicacion' => 'Huancayo', 'contrato' => 'tiempo_completo'])
                ->where('vacancies.meta.total', 1));
    }

    public function test_published_vacancies_whose_deadline_passed_stay_listed_with_their_flag(): void
    {
        $this->get(route('jobs.index', ['organizacion' => $this->dos->id]))
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->where('vacancies.data.0.code', 'VAC-F-03')
                ->where('vacancies.data.0.accepts_applications', false)
                ->where('vacancies.data.0.application_deadline_passed', true));
    }

    public function test_hidden_organizations_and_locations_are_rejected_like_unknown_ones(): void
    {
        $hidden = $this->get(route('jobs.index', ['organizacion' => $this->oculta->id]));
        $hidden->assertRedirect(route('jobs.index'))->assertSessionHasErrors('organizacion');
        $hiddenMessage = session('errors')->first('organizacion');

        $unknown = $this->get(route('jobs.index', ['organizacion' => 999999]));
        $unknown->assertRedirect(route('jobs.index'))->assertSessionHasErrors('organizacion');
        $this->assertSame($hiddenMessage, session('errors')->first('organizacion'));
        $this->assertStringNotContainsString('Sin Publicar', $hiddenMessage);

        $this->get(route('jobs.index', ['ubicacion' => 'Ciudad Reservada']))
            ->assertRedirect(route('jobs.index'))
            ->assertSessionHasErrors('ubicacion');
    }

    /**
     * @return array<string, array{array<string, mixed>, string}>
     */
    public static function malformedParameters(): array
    {
        return [
            'organización no numérica' => [['organizacion' => 'abc'], 'organizacion'],
            'organización con inyección' => [['organizacion' => '1 OR 1=1'], 'organizacion'],
            'organización negativa' => [['organizacion' => '-1'], 'organizacion'],
            'organización como lista' => [['organizacion' => ['1']], 'organizacion'],
            'ubicación como lista' => [['ubicacion' => ['Huancayo']], 'ubicacion'],
            'ubicación demasiado larga' => [['ubicacion' => str_repeat('a', 121)], 'ubicacion'],
            'contrato solo en convocatorias privadas' => [['contrato' => 'plazo_fijo'], 'contrato'],
            'página como lista' => [['page' => ['2']], 'page'],
            'página negativa' => [['page' => '-1'], 'page'],
            'página excesiva' => [['page' => '9223372036854775807'], 'page'],
            'contrato inexistente' => [['contrato' => 'indefinido'], 'contrato'],
            'contrato como lista' => [['contrato' => ['por_horas']], 'contrato'],
            'búsqueda como lista' => [['q' => ['docente']], 'q'],
            'búsqueda demasiado larga' => [['q' => str_repeat('a', 151)], 'q'],
        ];
    }

    /**
     * @param  array<string, mixed>  $query
     */
    #[DataProvider('malformedParameters')]
    public function test_malformed_parameters_return_to_the_full_listing_with_a_visible_notice(array $query, string $field): void
    {
        $this->get(route('jobs.index', $query))
            ->assertRedirect(route('jobs.index'))
            ->assertSessionHasErrors($field);

        $this->followingRedirects()->get(route('jobs.index', $query))
            ->assertOk()
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->component('jobs/index')
                ->has('errors.'.$field)
                ->where('vacancies.meta.total', 3));
    }

    public function test_pagination_keeps_search_and_filters_and_reports_the_total_of_the_whole_query(): void
    {
        foreach (range(10, 23) as $n) {
            $this->published($this->dos, 'VAC-P-'.$n, 'Docente de Aula '.$n, 'Lima', ContractType::FullTime, '2026-12-15');
        }

        $query = ['q' => 'aula', 'organizacion' => $this->dos->id, 'ubicacion' => 'Lima'];

        $this->get(route('jobs.index', $query))
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->where('vacancies.meta.total', 14)
                ->where('vacancies.meta.last_page', 2)
                ->has('vacancies.data', 12)
                ->where('vacancies.links.next', fn (string $next) => str_contains($next, 'q=aula')
                    && str_contains($next, 'organizacion='.$this->dos->id)
                    && str_contains($next, 'ubicacion=Lima')
                    && str_contains($next, 'page=2')));

        $first = $this->codes($query);
        $second = $this->codes([...$query, 'page' => 2]);
        $this->assertCount(2, $second);
        $this->assertSame([], array_intersect($first, $second), 'Ninguna convocatoria se repite entre páginas');
    }

    public function test_listing_runs_a_constant_number_of_queries(): void
    {
        $count = function (): int {
            DB::flushQueryLog();
            DB::enableQueryLog();
            $this->get(route('jobs.index'))->assertOk();
            DB::disableQueryLog();

            return count(DB::getQueryLog());
        };

        $few = $count();
        foreach (range(30, 38) as $n) {
            $org = Organization::factory()->create();
            $this->published($org, 'VAC-N-'.$n, 'Puesto '.$n, 'Ciudad '.$n, ContractType::PartTime, '2026-12-15');
        }

        $this->assertSame($few, $count(), 'El número de consultas no crece con las convocatorias');
    }
}
