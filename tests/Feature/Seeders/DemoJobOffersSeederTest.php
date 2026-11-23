<?php

namespace Tests\Feature\Seeders;

use App\Enums\JobRequestStatus;
use App\Enums\VacancyStatus;
use App\Models\Application;
use App\Models\Evaluation;
use App\Models\EvaluationCriterion;
use App\Models\Interview;
use App\Models\SelectionDecision;
use App\Models\Vacancy;
use App\Services\Vacancies\VacancyValidator;
use Database\Seeders\DemoJobOffersSeeder;
use Database\Seeders\DemoSeeder;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

/**
 * Diez ofertas ficticias adicionales para el listado público (`DemoJobOffersSeeder`), sobre los datos de
 * DemoSeeder. Se comprueba que entran por el flujo real (requerimiento aprobado, vacante con perfil y criterios
 * válidos, publicada), que no tocan lo que ya existía, que no crean postulaciones, evaluaciones ni decisiones,
 * y que una segunda ejecución no añade nada.
 */
class DemoJobOffersSeederTest extends TestCase
{
    use RefreshDatabase;

    protected function setUp(): void
    {
        parent::setUp();

        $this->seed(DemoSeeder::class);
    }

    public function test_adds_exactly_ten_published_fictitious_offers_through_the_real_flow(): void
    {
        $before = Vacancy::withoutGlobalScopes()->pluck('id');

        $this->seed(DemoJobOffersSeeder::class);

        $new = Vacancy::withoutGlobalScopes()
            ->with(['profile', 'criteria', 'jobRequest', 'organization'])
            ->whereNotIn('id', $before)
            ->get();

        $this->assertCount(10, $new);
        $this->assertSame(
            ['Colegio Andino de Huancayo (Demo)' => 6, 'Organización Demo B' => 4],
            $new->countBy(fn (Vacancy $v) => $v->organization->name)->sortKeys()->all(),
        );

        $validator = app(VacancyValidator::class);

        foreach ($new as $vacancy) {
            $this->assertSame(VacancyStatus::Published, $vacancy->status, $vacancy->title);
            $this->assertMatchesRegularExpression('/^VAC-\d{4}-\d{4}$/', $vacancy->code);
            $this->assertStringStartsWith('Convocatoria ficticia de demostración.', $vacancy->summary);
            $this->assertSame(JobRequestStatus::Approved, $vacancy->jobRequest->status);
            $this->assertStringContainsString('(clave demo-ofertas-', $vacancy->jobRequest->justification);
            $this->assertLessThanOrEqual($vacancy->jobRequest->headcount, $vacancy->positions);
            $this->assertNotNull($vacancy->profile);
            $this->assertNotSame('', $vacancy->profile->education);
            $this->assertNotSame('', $vacancy->profile->competencies);
            $this->assertTrue($vacancy->opens_at->isToday());
            $this->assertTrue($vacancy->closes_at->gte(now()->addDays(30)->startOfDay()));
            $this->assertGreaterThanOrEqual(3, $vacancy->criteria->count());
            $this->assertEqualsWithDelta(100.0, (float) $vacancy->criteria->sum('weight'), 0.001, $vacancy->title);
            $this->assertSame([], $validator->issues($vacancy), $vacancy->title);
        }

        $this->assertSame(
            $new->count(),
            $new->unique(fn (Vacancy $v) => $v->organization_id.'|'.$v->code)->count(),
            'códigos únicos por organización',
        );
    }

    public function test_keeps_existing_data_and_creates_no_applications_evaluations_or_decisions(): void
    {
        $vacancies = Vacancy::withoutGlobalScopes()->orderBy('id')->get(['id', 'code', 'title', 'status'])->toArray();
        $counts = $this->counts();

        $this->seed(DemoJobOffersSeeder::class);

        $this->assertSame(
            $vacancies,
            Vacancy::withoutGlobalScopes()->orderBy('id')->limit(count($vacancies))->get(['id', 'code', 'title', 'status'])->toArray(),
        );
        $this->assertSame($counts, $this->counts());
    }

    public function test_a_second_run_adds_nothing(): void
    {
        $this->seed(DemoJobOffersSeeder::class);
        $vacancies = Vacancy::withoutGlobalScopes()->count();
        $criteria = EvaluationCriterion::withoutGlobalScopes()->count();

        $this->seed(DemoJobOffersSeeder::class);

        $this->assertSame($vacancies, Vacancy::withoutGlobalScopes()->count());
        $this->assertSame($criteria, EvaluationCriterion::withoutGlobalScopes()->count());
    }

    /**
     * @return array<string, int>
     */
    private function counts(): array
    {
        return [
            'applications' => Application::withoutGlobalScopes()->count(),
            'evaluations' => Evaluation::withoutGlobalScopes()->count(),
            'interviews' => Interview::withoutGlobalScopes()->count(),
            'decisions' => SelectionDecision::withoutGlobalScopes()->count(),
        ];
    }
}
