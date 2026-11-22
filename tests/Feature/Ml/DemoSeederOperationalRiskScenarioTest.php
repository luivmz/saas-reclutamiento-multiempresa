<?php

namespace Tests\Feature\Ml;

use App\Enums\VacancyStatus;
use App\Models\Application;
use App\Models\Vacancy;
use App\Services\Ml\OperationalRiskFeatureBuilder;
use App\Services\Ml\OperationalRiskService;
use Database\Seeders\DemoSeeder;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

/**
 * Datos de demostración de RF-29 (ML-01, experimental).
 *
 * Con los datos demo originales ninguna vacante quedaba dentro de la ventana de
 * consulta del riesgo operacional: todas cerraban postulaciones en el futuro y
 * ninguna tenía plazo objetivo. Con el servicio activo, la tarjeta solo podía
 * mostrar el modo descriptivo, así que ML-01 no se podía demostrar.
 *
 * La demo añade, al final del seeder, un proceso ficticio reproducido en el
 * pasado: publicado, con el cierre de postulaciones vencido, todavía abierto y
 * con un plazo objetivo futuro. Los identificadores anteriores se conservan,
 * porque la suite Cypress los fija en `cypress/fixtures/demo.json`.
 */
class DemoSeederOperationalRiskScenarioTest extends TestCase
{
    use RefreshDatabase;

    private const SCENARIO_TITLE = 'Docente de Ciencia y Tecnología - Secundaria';

    protected function setUp(): void
    {
        parent::setUp();

        $this->seed(DemoSeeder::class);
    }

    public function test_the_demo_has_one_vacancy_inside_the_operational_risk_query_window(): void
    {
        $vacancy = $this->scenario();
        $service = app(OperationalRiskService::class);

        $this->assertSame(VacancyStatus::Published, $vacancy->status);
        $this->assertNull($vacancy->closed_at);
        $this->assertNotNull($vacancy->target_completion_at);
        $this->assertNull($service->outOfScopeReason($vacancy), 'La vacante de la demo debe poder consultarse a ML-01.');
    }

    public function test_the_scenario_history_happens_before_the_checkpoint(): void
    {
        $vacancy = $this->scenario();
        $checkpoint = app(OperationalRiskService::class)->checkpointFor($vacancy);
        $features = app(OperationalRiskFeatureBuilder::class)->build($vacancy, $checkpoint)->values;

        $applications = Application::query()->where('vacancy_id', $vacancy->id)->get();
        $this->assertGreaterThanOrEqual(3, $applications->count());
        $this->assertTrue($applications->every(fn (Application $a) => $a->applied_at->lte($checkpoint)));
        $this->assertSame($applications->count(), $features['applications_received_count']);
        $this->assertGreaterThanOrEqual(1, $features['days_remaining_to_target']);
    }

    public function test_the_existing_demo_identifiers_used_by_cypress_are_preserved(): void
    {
        $fixture = json_decode((string) file_get_contents(base_path('cypress/fixtures/demo.json')), true);

        // `e2e:reset` usa migrate:fresh, así que allí los identificadores empiezan en 1. Aquí las secuencias de
        // PostgreSQL no se reinician entre pruebas, de modo que se compara la posición relativa al primer registro.
        $vacancyBase = (int) Vacancy::withoutGlobalScopes()->min('id') - 1;
        $applicationBase = (int) Application::withoutGlobalScopes()->min('id') - 1;

        foreach ($fixture['vacancies'] as $vacancy) {
            $this->assertSame($vacancy['title'], Vacancy::withoutGlobalScopes()->findOrFail($vacancyBase + $vacancy['id'])->title);
        }
        foreach ($fixture['applications'] as $application) {
            $found = Application::withoutGlobalScopes()->with('candidate')->findOrFail($applicationBase + $application['id']);
            if (isset($application['candidate'])) {
                $this->assertSame($application['candidate'], $found->candidate->name);
            }
        }
    }

    private function scenario(): Vacancy
    {
        return Vacancy::withoutGlobalScopes()->where('title', self::SCENARIO_TITLE)->sole();
    }
}
