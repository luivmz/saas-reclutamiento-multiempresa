<?php

namespace Tests\Feature\Ml;

use App\Enums\VacancyStatus;
use App\Models\AuditLog;
use App\Models\JobRequest;
use App\Models\Organization;
use App\Models\User;
use App\Models\Vacancy;
use Carbon\CarbonInterface;
use Illuminate\Database\QueryException;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schema;
use Tests\TestCase;

/**
 * GAP-01: `vacancies.target_completion_at`.
 *
 * Era la única feature del contrato sin fuente en Laravel, y sin ella el
 * modelo de la Fase 15 no podía integrarse. Estas pruebas fijan las tres
 * propiedades de las que depende que la feature sea utilizable: existe, es
 * posterior al cierre de postulaciones, y **deja de poder moverse cuando la
 * vacante se publica** -- si el plazo pudiera correrse durante el proceso, la
 * feature filtraría información del desenlace.
 */
class TargetCompletionTest extends TestCase
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

    // -- esquema ------------------------------------------------------------

    public function test_the_column_exists_and_is_nullable(): void
    {
        $this->assertTrue(Schema::hasColumn('vacancies', 'target_completion_at'));

        $vacancy = Vacancy::factory()->for($this->organization)->create();

        $this->assertNull($vacancy->target_completion_at);
    }

    public function test_the_value_is_cast_to_a_datetime(): void
    {
        $vacancy = Vacancy::factory()
            ->for($this->organization)
            ->withTargetCompletion()
            ->create();

        // El proyecto usa fechas inmutables, asi que se comprueba la interfaz.
        $this->assertInstanceOf(CarbonInterface::class, $vacancy->fresh()->target_completion_at);
    }

    public function test_the_database_rejects_a_target_before_the_application_close(): void
    {
        $vacancy = Vacancy::factory()->for($this->organization)->create([
            'closes_at' => now()->addDays(10)->startOfDay(),
        ]);

        $this->expectException(QueryException::class);

        DB::table('vacancies')
            ->where('id', $vacancy->id)
            ->update(['target_completion_at' => now()->addDays(5)]);
    }

    public function test_existing_vacancies_keep_working_without_a_target(): void
    {
        /* No se rellena ningún valor por retrocompatibilidad: inventar un plazo
           contaminaría justamente la feature que justifica la integración. */
        $vacancy = Vacancy::factory()->for($this->organization)->published()->create();

        $this->assertNull($vacancy->target_completion_at);
        $this->assertSame(VacancyStatus::Published, $vacancy->status);
    }

    // -- validación ---------------------------------------------------------

    /**
     * @return array<string, mixed>
     */
    private function payload(JobRequest $jobRequest, array $overrides = []): array
    {
        return array_replace([
            'job_request_id' => $jobRequest->id,
            'title' => 'Docente de Matemática',
            'summary' => 'Convocatoria ficticia para pruebas.',
            'location' => 'Huancayo, Junín',
            'contract_type' => 'tiempo_completo',
            'positions' => 1,
            'opens_at' => now()->toDateString(),
            'closes_at' => now()->addDays(15)->toDateString(),
            'profile' => [
                'education' => 'Licenciatura en Educación',
                'experience' => 'Mínimo 2 años',
                'functions' => 'Funciones ficticias.',
                'competencies' => 'Competencias ficticias.',
            ],
            'criteria' => [
                ['name' => 'Conocimientos', 'stage' => 'evaluacion', 'weight' => 60, 'min_score' => 0, 'max_score' => 20],
                ['name' => 'Entrevista', 'stage' => 'entrevista', 'weight' => 40, 'min_score' => 0, 'max_score' => 20],
            ],
        ], $overrides);
    }

    public function test_hr_can_register_a_target_completion_date(): void
    {
        $jobRequest = JobRequest::factory()->for($this->organization)->approved()->create();
        $target = now()->addDays(45)->setTime(18, 0);

        $this->actingAs($this->hr)
            ->post(route('vacancies.store'), $this->payload($jobRequest, [
                'target_completion_at' => $target->toIso8601String(),
            ]))
            ->assertRedirect();

        $vacancy = Vacancy::query()->latest('id')->firstOrFail();

        $this->assertNotNull($vacancy->target_completion_at);
        $this->assertSame($target->toDateString(), $vacancy->target_completion_at->toDateString());
    }

    public function test_the_target_must_be_after_the_application_close(): void
    {
        $jobRequest = JobRequest::factory()->for($this->organization)->approved()->create();

        $this->actingAs($this->hr)
            ->post(route('vacancies.store'), $this->payload($jobRequest, [
                'closes_at' => now()->addDays(15)->toDateString(),
                'target_completion_at' => now()->addDays(10)->toIso8601String(),
            ]))
            ->assertSessionHasErrors('target_completion_at');
    }

    public function test_the_target_is_optional(): void
    {
        $jobRequest = JobRequest::factory()->for($this->organization)->approved()->create();

        $this->actingAs($this->hr)
            ->post(route('vacancies.store'), $this->payload($jobRequest))
            ->assertRedirect()
            ->assertSessionHasNoErrors();

        $this->assertNull(Vacancy::query()->latest('id')->firstOrFail()->target_completion_at);
    }

    // -- inmutabilidad tras publicar ---------------------------------------

    public function test_the_target_cannot_be_changed_once_published(): void
    {
        $vacancy = Vacancy::factory()
            ->for($this->organization)
            ->configured()
            ->published()
            ->withTargetCompletion()
            ->create();
        $original = $vacancy->fresh()->target_completion_at;

        $this->actingAs($this->hr)
            ->put(route('vacancies.update', $vacancy), $this->payload($vacancy->jobRequest, [
                'target_completion_at' => now()->addDays(120)->toIso8601String(),
            ]));

        $this->assertTrue($original->equalTo($vacancy->fresh()->target_completion_at));
    }

    public function test_the_model_reports_when_the_target_is_editable(): void
    {
        $draft = Vacancy::factory()->for($this->organization)->create();
        $published = Vacancy::factory()->for($this->organization)->published()->create();

        $this->assertTrue($draft->targetCompletionIsEditable());
        $this->assertFalse($published->targetCompletionIsEditable());
    }

    // -- auditoría ----------------------------------------------------------

    public function test_the_target_is_recorded_in_the_audit_trail(): void
    {
        $jobRequest = JobRequest::factory()->for($this->organization)->approved()->create();
        $target = now()->addDays(40)->setTime(17, 0);

        $this->actingAs($this->hr)->post(route('vacancies.store'), $this->payload($jobRequest, [
            'target_completion_at' => $target->toIso8601String(),
        ]));

        $log = AuditLog::query()->withoutGlobalScopes()->latest('id')->firstOrFail();

        $this->assertArrayHasKey('target_completion_at', $log->metadata);
        $this->assertNotNull($log->metadata['target_completion_at']);
    }

    // -- multiempresa -------------------------------------------------------

    public function test_hr_cannot_set_a_target_on_another_organizations_vacancy(): void
    {
        $other = Organization::factory()->create();
        $foreign = Vacancy::factory()->for($other)->configured()->create();
        // Se resuelve antes de autenticar: con sesion iniciada, el scope global
        // de organizacion ya no dejaria cargar la relacion ajena.
        $foreignRequest = $foreign->jobRequest;

        $this->actingAs($this->hr)
            ->put(route('vacancies.update', $foreign), $this->payload($foreignRequest, [
                'target_completion_at' => now()->addDays(60)->toIso8601String(),
            ]))
            ->assertNotFound();

        $this->assertNull($foreign->fresh()->target_completion_at);
    }
}
