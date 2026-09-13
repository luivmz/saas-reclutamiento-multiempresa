<?php

namespace Database\Seeders;

use App\Enums\CriterionStage;
use App\Enums\EducationLevel;
use App\Enums\InterviewOutcome;
use App\Enums\UserRole;
use App\Models\Application;
use App\Models\CandidateProfile;
use App\Models\EvaluationCriterion;
use App\Models\JobRequest;
use App\Models\Organization;
use App\Models\User;
use App\Models\Vacancy;
use App\Services\Applications\ApplicationService;
use App\Services\Applications\ApplicationStageService;
use App\Services\Assessments\AssessmentResultRecorder;
use App\Services\Assessments\AssessmentScheduler;
use App\Services\JobRequests\JobRequestWorkflow;
use App\Services\Selection\FinalDecisionService;
use App\Services\Selection\SelectionRegistrationService;
use App\Services\Selection\VacancyClosureService;
use App\Services\Vacancies\VacancyService;
use Illuminate\Database\Seeder;

/**
 * Fictitious demo data built through the real domain services (states, history, audit and notifications
 * are produced exactly as in normal use). Intended for `php artisan migrate:fresh --seed`.
 * Users and scenarios are documented in docs/demo-users.md.
 */
class DemoSeeder extends Seeder
{
    public function __construct(
        private readonly JobRequestWorkflow $requests,
        private readonly VacancyService $vacancies,
        private readonly ApplicationService $applications,
        private readonly ApplicationStageService $stages,
        private readonly AssessmentScheduler $scheduler,
        private readonly AssessmentResultRecorder $recorder,
        private readonly FinalDecisionService $decisions,
        private readonly SelectionRegistrationService $selections,
        private readonly VacancyClosureService $closures,
    ) {}

    public function run(): void
    {
        config(['queue.default' => 'sync']);

        $andino = Organization::query()->create([
            'name' => 'Colegio Andino de Huancayo (Demo)',
            'slug' => 'colegio-andino-demo',
            'tax_id' => '20000000001',
            'is_active' => true,
        ]);
        $demoB = Organization::query()->create([
            'name' => 'Organización Demo B',
            'slug' => 'organizacion-demo-b',
            'tax_id' => '20000000002',
            'is_active' => true,
        ]);

        $requester = $this->staff($andino, UserRole::Requester, 'Carmen Rojas (demo)', 'solicitante@andino.test');
        $hr = $this->staff($andino, UserRole::HumanResources, 'Luis Paredes (demo)', 'rrhh@andino.test');
        $approver = $this->staff($andino, UserRole::Approver, 'Rosa Huamán (demo)', 'direccion@andino.test');
        $evaluator = $this->staff($andino, UserRole::Evaluator, 'Jorge Salazar (demo)', 'evaluador@andino.test');
        $this->staff($andino, UserRole::Evaluator, 'Elena Quispe (demo)', 'evaluador2@andino.test');

        $requesterB = $this->staff($demoB, UserRole::Requester, 'Pedro Castro (demo B)', 'solicitante@demob.test');
        $hrB = $this->staff($demoB, UserRole::HumanResources, 'Ana Torres (demo B)', 'rrhh@demob.test');
        $approverB = $this->staff($demoB, UserRole::Approver, 'Mario Díaz (demo B)', 'direccion@demob.test');
        $this->staff($demoB, UserRole::Evaluator, 'Sofía Ramos (demo B)', 'evaluador@demob.test');

        $p1 = $this->candidate('Andrea Poma (ficticia)', 'postulante1@correo.test', 'Licenciada en Educación Secundaria', 4, 'Huancayo');
        $p2 = $this->candidate('Bruno Cárdenas (ficticio)', 'postulante2@correo.test', 'Licenciado en Lengua y Literatura', 6, 'El Tambo');
        $p3 = $this->candidate('Claudia Vilca (ficticia)', 'postulante3@correo.test', 'Profesora de Comunicación', 3, 'Chilca');
        $p4 = $this->candidate('Diego Mendoza (ficticio)', 'postulante4@correo.test', 'Licenciado en Educación Inicial', 5, 'Huancayo');
        $p5 = $this->candidate('Estela Ñahui (ficticia)', 'postulante5@correo.test', 'Profesora de Educación Inicial', 8, 'Concepción');
        $p6 = $this->candidate('Fabio Llanos (ficticio)', 'postulante6@correo.test', 'Auxiliar de Educación', 2, 'Huancayo');
        User::factory()->candidate()->create(['name' => 'Gabriela Nueva (ficticia)', 'email' => 'postulante.nuevo@correo.test']);

        // RF-01 a RF-04: requerimientos en cada estado.
        $this->requests->register($requester, $this->requestData('Docente de Educación Física', 'Coordinación Académica', 'Borrador ficticio pendiente de completar por el área solicitante.'));
        $this->requests->submit($this->requests->register($requester, $this->requestData('Docente de Arte', 'Coordinación Académica', 'Se requiere cubrir el taller de arte por reorganización de horarios (demo).')), $requester);
        $observed = $this->requests->submit($this->requests->register($requester, $this->requestData('Psicólogo(a) Escolar', 'Departamento de Tutoría', 'Apoyo psicopedagógico para el nivel secundario (dato ficticio).')), $requester);
        $this->requests->observe($observed, $hr, 'Precisar el horario y la carga horaria requerida.');
        $validated = $this->requests->submit($this->requests->register($requester, $this->requestData('Docente de Matemática - Secundaria', 'Coordinación Académica', 'Incremento de secciones de 4.º grado de secundaria (dato ficticio).')), $requester);
        $this->requests->validate($validated, $hr);
        $rejected = $this->requests->validate($this->requests->submit($this->requests->register($requester, $this->requestData('Asistente de Biblioteca', 'Dirección Administrativa', 'Apoyo en biblioteca durante el segundo semestre (dato ficticio).')), $requester), $hr);
        $this->requests->reject($rejected, $approver, 'No existe presupuesto aprobado para la plaza en este periodo.');
        $this->approvedRequest($requester, $hr, $approver, 'Docente de Religión', 'Coordinación Académica');

        // RF-05 a RF-07: vacante en borrador lista para publicar.
        $this->vacancy($hr, $this->approvedRequest($requester, $hr, $approver, 'Docente de Inglés', 'Coordinación Académica'), 'Docente de Inglés - Primaria', publish: false);

        // RF-08 a RF-19: vacante publicada con postulaciones en distintas etapas.
        $communication = $this->vacancy($hr, $this->approvedRequest($requester, $hr, $approver, 'Docente de Comunicación', 'Coordinación Académica'), 'Docente de Comunicación - Secundaria');
        $this->applications->apply($p1, $communication);
        $this->stages->shortlist($this->applications->apply($p2, $communication), $hr, 'Cumple el perfil requerido.');
        $inEvaluation = $this->stages->shortlist($this->applications->apply($p3, $communication), $hr, 'Experiencia pertinente.');
        $this->scheduleEvaluation($inEvaluation, $hr, $evaluator);

        // RF-20 a RF-23: finalistas con resultados completos (ranking disponible, decisión pendiente).
        $initial = $this->vacancy($hr, $this->approvedRequest($requester, $hr, $approver, 'Auxiliar de Educación Inicial', 'Dirección de Nivel Inicial'), 'Auxiliar de Educación Inicial');
        $this->finalist($initial, $p4, $hr, $evaluator, [18, 16, 17]);
        $this->finalist($initial, $p5, $hr, $evaluator, [20, 10, 19]);
        $this->finalist($initial, $p6, $hr, $evaluator, [14, 15, 12]);

        // RF-24 a RF-26: proceso concluido con selección, cierre y notificaciones.
        $tutoring = $this->vacancy($hr, $this->approvedRequest($requester, $hr, $approver, 'Coordinador(a) de Tutoría', 'Departamento de Tutoría'), 'Coordinador(a) de Tutoría');
        $chosen = $this->finalist($tutoring, $p5, $hr, $evaluator, [19, 18, 18]);
        $this->finalist($tutoring, $p6, $hr, $evaluator, [15, 14, 16]);
        $this->scheduleEvaluation($this->stages->shortlist($this->applications->apply($p1, $tutoring), $hr), $hr, $evaluator);
        $this->decisions->decide($tutoring, $approver, $chosen->id, 'Mejor desempeño en la clase modelo y experiencia en tutoría (decisión de demostración).');
        $this->selections->register($tutoring, $hr);
        $this->closures->close($tutoring, $hr, 'Proceso de demostración concluido con selección.');

        // Organización Demo B (aislamiento multiempresa).
        $assistant = $this->vacancy($hrB, $this->approvedRequest($requesterB, $hrB, $approverB, 'Asistente Administrativo', 'Administración'), 'Asistente Administrativo (Demo B)');
        $this->applications->apply($p2, $assistant);
    }

    private function staff(Organization $organization, UserRole $role, string $name, string $email): User
    {
        return User::factory()->create([
            'organization_id' => $organization->id,
            'role' => $role,
            'name' => $name,
            'email' => $email,
        ]);
    }

    private function candidate(string $name, string $email, string $title, int $years, string $city): User
    {
        $user = User::factory()->candidate()->create(['name' => $name, 'email' => $email]);

        CandidateProfile::factory()->withCv()->create([
            'user_id' => $user->id,
            'phone' => '900'.str_pad((string) $user->id, 6, '0', STR_PAD_LEFT),
            'city' => $city,
            'education_level' => EducationLevel::Graduate,
            'professional_title' => $title,
            'years_of_experience' => $years,
            'summary' => 'Perfil profesional ficticio creado para la demostración.',
        ]);

        return $user;
    }

    /**
     * @return array<string, mixed>
     */
    private function requestData(string $title, string $area, string $justification): array
    {
        return [
            'position_title' => $title,
            'area' => $area,
            'headcount' => 1,
            'contract_type' => 'tiempo_completo',
            'justification' => $justification,
            'required_by' => now()->addMonth()->toDateString(),
        ];
    }

    private function approvedRequest(User $requester, User $hr, User $approver, string $title, string $area): JobRequest
    {
        $jobRequest = $this->requests->register($requester, $this->requestData($title, $area, "Necesidad ficticia de {$title} para la demostración del sistema."));
        $jobRequest = $this->requests->submit($jobRequest, $requester);
        $jobRequest = $this->requests->validate($jobRequest, $hr);

        return $this->requests->approve($jobRequest, $approver, 'Conforme (demo).');
    }

    private function vacancy(User $hr, JobRequest $jobRequest, string $title, bool $publish = true): Vacancy
    {
        $vacancy = $this->vacancies->create(
            $hr,
            $jobRequest,
            [
                'title' => $title,
                'summary' => "Convocatoria ficticia para el puesto de {$title}. Los datos son de demostración.",
                'location' => 'Huancayo, Junín',
                'contract_type' => 'tiempo_completo',
                'positions' => 1,
                'opens_at' => now()->toDateString(),
                'closes_at' => now()->addDays(20)->toDateString(),
            ],
            [
                'education' => 'Título profesional en Educación o afín',
                'experience' => 'Mínimo 2 años en instituciones educativas',
                'functions' => 'Planificar y desarrollar sesiones de aprendizaje; participar en tutoría y reuniones de coordinación.',
                'competencies' => 'Comunicación asertiva, trabajo en equipo, manejo de TIC y enfoque por competencias.',
            ],
            [
                ['name' => 'Conocimientos pedagógicos', 'stage' => 'evaluacion', 'weight' => 40, 'min_score' => 0, 'max_score' => 20],
                ['name' => 'Clase modelo', 'stage' => 'evaluacion', 'weight' => 30, 'min_score' => 0, 'max_score' => 20],
                ['name' => 'Entrevista personal', 'stage' => 'entrevista', 'weight' => 30, 'min_score' => 0, 'max_score' => 20],
            ],
        );

        return $publish ? $this->vacancies->publish($vacancy, $hr) : $vacancy;
    }

    private function scheduleEvaluation(Application $application, User $hr, User $evaluator): void
    {
        $this->scheduler->scheduleEvaluation($application, $hr, [
            'evaluator_id' => $evaluator->id,
            'type' => 'conocimientos',
            'modality' => 'presencial',
            'location' => 'Aula 204 - Sede central (demo)',
            'scheduled_at' => now()->addDays(2)->setTime(9, 0)->format('Y-m-d H:i'),
            'duration_minutes' => 60,
            'instructions' => 'Presentarse 15 minutos antes con lapicero.',
        ]);
    }

    /**
     * @param  array{0: float|int, 1: float|int, 2: float|int}  $scores  knowledge, model class, interview
     */
    private function finalist(Vacancy $vacancy, User $candidate, User $hr, User $evaluator, array $scores): Application
    {
        $application = $this->stages->shortlist($this->applications->apply($candidate, $vacancy), $hr);

        $evaluation = $this->scheduler->scheduleEvaluation($application, $hr, [
            'evaluator_id' => $evaluator->id,
            'type' => 'clase_modelo',
            'modality' => 'presencial',
            'location' => 'Aula 101 - Sede central (demo)',
            'scheduled_at' => now()->addDay()->setTime(10, 0)->format('Y-m-d H:i'),
            'duration_minutes' => 45,
        ]);
        $evaluationCriteria = array_keys(EvaluationCriterion::definitionsFor($vacancy->id, CriterionStage::Evaluation));
        $this->recorder->recordEvaluation($evaluation, $evaluator, [
            $evaluationCriteria[0] => ['score' => $scores[0]],
            $evaluationCriteria[1] => ['score' => $scores[1]],
        ], 'Evaluación de demostración.');

        $interview = $this->scheduler->scheduleInterview($application, $hr, [
            'evaluator_id' => $evaluator->id,
            'modality' => 'virtual',
            'location' => 'https://reuniones.example.test/sala-demo',
            'scheduled_at' => now()->addDays(3)->setTime(16, 0)->format('Y-m-d H:i'),
            'duration_minutes' => 30,
        ]);
        $interviewCriteria = array_keys(EvaluationCriterion::definitionsFor($vacancy->id, CriterionStage::Interview));
        $this->recorder->recordInterview(
            $interview,
            $evaluator,
            [$interviewCriteria[0] => ['score' => $scores[2]]],
            InterviewOutcome::Recommended,
            'Entrevista de demostración con buena disposición.',
        );

        return $this->stages->moveTo($application, \App\Enums\ApplicationStatus::Finalist, $hr);
    }
}
