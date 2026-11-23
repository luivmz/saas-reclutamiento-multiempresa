<?php

namespace Database\Seeders;

use App\Enums\JobRequestStatus;
use App\Models\JobRequest;
use App\Models\Organization;
use App\Models\User;
use App\Models\Vacancy;
use App\Services\JobRequests\JobRequestWorkflow;
use App\Services\Vacancies\VacancyService;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;
use RuntimeException;

/**
 * Ten additional fictitious job offers for the public listing demo (/empleos): six for «Colegio Andino de
 * Huancayo (Demo)» and four for «Organización Demo B». Runs on top of DemoSeeder and is never called by it:
 *
 *   php artisan db:seed --class=DemoJobOffersSeeder --force
 *
 * Each offer goes through the real domain services, as in normal use: a job request registered, submitted,
 * validated and approved, then a vacancy created with its profile and criteria (weights adding up to 100) and
 * published. Audit records and notifications are produced as usual. No applications, evaluations or decisions
 * are created.
 *
 * Idempotent: every offer carries a stable key in its job request justification («clave demo-ofertas-NN»).
 * An offer whose key already has a vacancy is skipped, so a second run adds nothing. Each offer is created in
 * its own transaction, so an interrupted run leaves no half-built offer behind.
 */
class DemoJobOffersSeeder extends Seeder
{
    public function __construct(
        private readonly JobRequestWorkflow $requests,
        private readonly VacancyService $vacancies,
    ) {}

    /** @var array<string, array{slug: string, requester: string, hr: string, approver: string}> */
    private const ORGANIZATIONS = [
        'andino' => [
            'slug' => 'colegio-andino-demo',
            'requester' => 'solicitante@andino.test',
            'hr' => 'rrhh@andino.test',
            'approver' => 'direccion@andino.test',
        ],
        'demob' => [
            'slug' => 'organizacion-demo-b',
            'requester' => 'solicitante@demob.test',
            'hr' => 'rrhh@demob.test',
            'approver' => 'direccion@demob.test',
        ],
    ];

    public function run(): void
    {
        config(['queue.default' => 'sync']);

        $created = [];

        foreach ($this->offers() as $offer) {
            $vacancy = DB::transaction(fn (): ?Vacancy => $this->offer($offer));

            if ($vacancy !== null) {
                $created[] = "{$vacancy->code} {$vacancy->title}";
            }
        }

        $this->command?->info(count($created) === 0
            ? 'DemoJobOffersSeeder: las 10 ofertas ya existían; no se añadió nada.'
            : 'DemoJobOffersSeeder: '.count($created).' ofertas nuevas: '.implode(' · ', $created));
    }

    /**
     * @param  array<string, mixed>  $offer
     */
    private function offer(array $offer): ?Vacancy
    {
        $people = $this->people($offer['org']);
        $marker = "(clave {$offer['key']})";

        $jobRequest = JobRequest::query()
            ->withoutGlobalScopes()
            ->where('organization_id', $people['organization']->id)
            ->where('justification', 'like', "%{$marker}%")
            ->first();

        if ($jobRequest?->vacancy()->withoutGlobalScopes()->exists()) {
            return null;
        }

        if ($jobRequest === null) {
            $jobRequest = $this->requests->register($people['requester'], [
                'position_title' => $offer['title'],
                'area' => $offer['area'],
                'headcount' => $offer['positions'],
                'contract_type' => $offer['contract_type'],
                'justification' => "Requerimiento ficticio de demostración para el listado público de empleos {$marker}.",
                'required_by' => now()->addDays(60)->toDateString(),
            ]);
        }

        if ($jobRequest->status === JobRequestStatus::Draft) {
            $jobRequest = $this->requests->submit($jobRequest, $people['requester']);
        }

        if ($jobRequest->status === JobRequestStatus::Submitted) {
            $jobRequest = $this->requests->validate($jobRequest, $people['hr']);
        }

        if ($jobRequest->status === JobRequestStatus::Validated) {
            $jobRequest = $this->requests->approve($jobRequest, $people['approver'], 'Conforme (demostración).');
        }

        $vacancy = $this->vacancies->create(
            $people['hr'],
            $jobRequest,
            [
                'title' => $offer['title'],
                'summary' => 'Convocatoria ficticia de demostración. '.$offer['summary'],
                'location' => $offer['location'],
                'contract_type' => $offer['contract_type'],
                'positions' => $offer['positions'],
                'opens_at' => now()->toDateString(),
                'closes_at' => now()->addDays($offer['closes_in_days'])->toDateString(),
            ],
            $offer['profile'],
            $offer['criteria'],
        );

        return $this->vacancies->publish($vacancy, $people['hr']);
    }

    /**
     * @return array{organization: Organization, requester: User, hr: User, approver: User}
     */
    private function people(string $org): array
    {
        $config = self::ORGANIZATIONS[$org];
        $organization = Organization::query()->where('slug', $config['slug'])->first();

        if ($organization === null) {
            throw new RuntimeException('DemoJobOffersSeeder necesita los datos de DemoSeeder: falta la organización «'.$config['slug'].'».');
        }

        $user = function (string $email) use ($organization): User {
            $found = User::query()->where('email', $email)->where('organization_id', $organization->id)->first();

            if ($found === null) {
                throw new RuntimeException("DemoJobOffersSeeder necesita los datos de DemoSeeder: falta el usuario {$email}.");
            }

            return $found;
        };

        return [
            'organization' => $organization,
            'requester' => $user($config['requester']),
            'hr' => $user($config['hr']),
            'approver' => $user($config['approver']),
        ];
    }

    /**
     * @param  array{0: string, 1: string, 2: int|float}  ...$criteria  name, stage, weight (scores from 0 to 20)
     * @return list<array<string, mixed>>
     */
    private static function criteria(array ...$criteria): array
    {
        return array_map(fn (array $c) => [
            'name' => $c[0],
            'stage' => $c[1],
            'weight' => $c[2],
            'min_score' => 0,
            'max_score' => 20,
        ], $criteria);
    }

    /**
     * Fictitious offers. Every text is invented for the demo.
     *
     * @return list<array<string, mixed>>
     */
    private function offers(): array
    {
        return [
            [
                'key' => 'demo-ofertas-01',
                'org' => 'andino',
                'title' => 'Docente de Matemática - Secundaria',
                'area' => 'Coordinación Académica',
                'contract_type' => 'tiempo_completo',
                'positions' => 2,
                'location' => 'Huancayo, Junín',
                'closes_in_days' => 30,
                'summary' => 'Docente de Matemática para 3.º a 5.º de secundaria, con enfoque por competencias y resolución de problemas. Trabajo presencial en la sede central.',
                'profile' => [
                    'education' => 'Licenciatura en Educación, especialidad Matemática, o afín',
                    'experience' => 'Mínimo 3 años en educación secundaria',
                    'functions' => 'Planificar y desarrollar sesiones de Matemática; elaborar instrumentos de evaluación formativa; acompañar a estudiantes con dificultades; coordinar con el área de Ciencias.',
                    'competencies' => 'Razonamiento matemático, didáctica de la matemática, manejo de GeoGebra y hojas de cálculo, comunicación asertiva.',
                ],
                'criteria' => self::criteria(
                    ['Dominio disciplinar', 'evaluacion', 35],
                    ['Clase modelo', 'evaluacion', 35],
                    ['Entrevista personal', 'entrevista', 30],
                ),
            ],
            [
                'key' => 'demo-ofertas-02',
                'org' => 'andino',
                'title' => 'Docente de Inglés - Primaria',
                'area' => 'Coordinación Académica',
                'contract_type' => 'tiempo_parcial',
                'positions' => 1,
                'location' => 'Huancayo, Junín',
                'closes_in_days' => 33,
                'summary' => 'Docente de Inglés para 3.º a 6.º de primaria, con metodología lúdica y comunicativa. Trabajo presencial, turno mañana.',
                'profile' => [
                    'education' => 'Licenciatura en Educación con mención en Inglés o afín; certificación de nivel B2 o superior',
                    'experience' => 'Mínimo 2 años enseñando inglés en primaria',
                    'functions' => 'Desarrollar sesiones de inglés; preparar material didáctico lúdico; evaluar habilidades orales y escritas; organizar actividades culturales en inglés.',
                    'competencies' => 'Inglés de nivel B2, didáctica lúdica, recursos audiovisuales, paciencia y trabajo en equipo.',
                ],
                'criteria' => self::criteria(
                    ['Dominio del idioma', 'evaluacion', 40],
                    ['Clase demostrativa', 'evaluacion', 30],
                    ['Entrevista personal', 'entrevista', 30],
                ),
            ],
            [
                'key' => 'demo-ofertas-03',
                'org' => 'andino',
                'title' => 'Docente de Educación Física',
                'area' => 'Coordinación Académica',
                'contract_type' => 'tiempo_completo',
                'positions' => 1,
                'location' => 'El Tambo, Junín',
                'closes_in_days' => 36,
                'summary' => 'Docente de Educación Física para primaria y secundaria, a cargo del deporte escolar y de los hábitos saludables. Trabajo presencial en el campo deportivo de El Tambo.',
                'profile' => [
                    'education' => 'Licenciatura en Educación Física o afín',
                    'experience' => 'Mínimo 2 años en educación básica',
                    'functions' => 'Planificar sesiones de educación física y deporte escolar; promover hábitos saludables; organizar juegos deportivos internos; velar por la seguridad de los estudiantes.',
                    'competencies' => 'Primeros auxilios, planificación deportiva, liderazgo de grupos y comunicación con las familias.',
                ],
                'criteria' => self::criteria(
                    ['Conocimientos de educación física', 'evaluacion', 30],
                    ['Sesión práctica', 'evaluacion', 40],
                    ['Entrevista personal', 'entrevista', 30],
                ),
            ],
            [
                'key' => 'demo-ofertas-04',
                'org' => 'andino',
                'title' => 'Psicólogo/a educativo/a',
                'area' => 'Departamento de Tutoría',
                'contract_type' => 'tiempo_completo',
                'positions' => 1,
                'location' => 'Huancayo, Junín',
                'closes_in_days' => 39,
                'summary' => 'Psicólogo/a educativo/a para acompañar a estudiantes y familias y fortalecer la tutoría y la convivencia escolar. Trabajo presencial.',
                'profile' => [
                    'education' => 'Licenciatura en Psicología, con colegiatura vigente',
                    'experience' => 'Mínimo 2 años en psicología educativa',
                    'functions' => 'Evaluar y acompañar a estudiantes; diseñar programas de tutoría y convivencia; orientar a las familias; coordinar derivaciones con especialistas externos.',
                    'competencies' => 'Escucha activa, ética profesional, instrumentos psicopedagógicos y trabajo interdisciplinario.',
                ],
                'criteria' => self::criteria(
                    ['Caso práctico', 'evaluacion', 40],
                    ['Conocimientos de psicología educativa', 'evaluacion', 30],
                    ['Entrevista personal', 'entrevista', 30],
                ),
            ],
            [
                'key' => 'demo-ofertas-05',
                'org' => 'andino',
                'title' => 'Bibliotecario/a escolar',
                'area' => 'Dirección Administrativa',
                'contract_type' => 'tiempo_parcial',
                'positions' => 1,
                'location' => 'Huancayo, Junín',
                'closes_in_days' => 42,
                'summary' => 'Bibliotecario/a escolar para organizar el fondo bibliográfico y animar la lectura en todos los niveles. Trabajo presencial, turno tarde.',
                'profile' => [
                    'education' => 'Bachiller en Bibliotecología, Educación o afín',
                    'experience' => 'Mínimo 1 año en bibliotecas o centros de recursos',
                    'functions' => 'Organizar y catalogar el fondo bibliográfico; atender a estudiantes y docentes; promover la lectura con actividades; gestionar los préstamos.',
                    'competencies' => 'Catalogación, animación lectora, sistemas de gestión de bibliotecas, orden y atención al usuario.',
                ],
                'criteria' => self::criteria(
                    ['Conocimientos de gestión bibliotecaria', 'evaluacion', 40],
                    ['Propuesta de animación lectora', 'evaluacion', 30],
                    ['Entrevista personal', 'entrevista', 30],
                ),
            ],
            [
                'key' => 'demo-ofertas-06',
                'org' => 'andino',
                'title' => 'Asistente de soporte informático',
                'area' => 'Dirección Administrativa',
                'contract_type' => 'plazo_fijo',
                'positions' => 1,
                'location' => 'Huancayo, Junín',
                'closes_in_days' => 45,
                'summary' => 'Asistente de soporte informático para mantener los laboratorios y apoyar a docentes con las plataformas educativas. Contrato a plazo fijo, presencial.',
                'profile' => [
                    'education' => 'Técnico en Computación e Informática o afín',
                    'experience' => 'Mínimo 1 año en soporte técnico',
                    'functions' => 'Atender incidencias de equipos y red; mantener los laboratorios de cómputo; apoyar a docentes con plataformas educativas; registrar el inventario tecnológico.',
                    'competencies' => 'Diagnóstico de hardware y software, redes básicas, atención al usuario y organización.',
                ],
                'criteria' => self::criteria(
                    ['Prueba técnica', 'evaluacion', 50],
                    ['Resolución de incidencias', 'evaluacion', 20],
                    ['Entrevista personal', 'entrevista', 30],
                ),
            ],
            [
                'key' => 'demo-ofertas-07',
                'org' => 'demob',
                'title' => 'Analista de Recursos Humanos',
                'area' => 'Recursos Humanos',
                'contract_type' => 'tiempo_completo',
                'positions' => 1,
                'location' => 'Lima, Lima',
                'closes_in_days' => 31,
                'summary' => 'Analista de Recursos Humanos para los procesos de selección, el legajo del personal y los indicadores de clima laboral. Trabajo presencial con un día remoto.',
                'profile' => [
                    'education' => 'Bachiller en Psicología, Administración o Relaciones Industriales',
                    'experience' => 'Mínimo 2 años en selección o gestión de personal',
                    'functions' => 'Gestionar procesos de selección; mantener los legajos; apoyar en planillas y clima laboral; elaborar reportes de indicadores de personal.',
                    'competencies' => 'Entrevista por competencias, normativa laboral básica, hojas de cálculo y confidencialidad.',
                ],
                'criteria' => self::criteria(
                    ['Caso de selección', 'evaluacion', 35],
                    ['Conocimientos de gestión de personal', 'evaluacion', 30],
                    ['Entrevista personal', 'entrevista', 35],
                ),
            ],
            [
                'key' => 'demo-ofertas-08',
                'org' => 'demob',
                'title' => 'Asistente de Contabilidad',
                'area' => 'Contabilidad',
                'contract_type' => 'tiempo_completo',
                'positions' => 2,
                'location' => 'Lima, Lima',
                'closes_in_days' => 34,
                'summary' => 'Asistente de Contabilidad para el registro de operaciones, las conciliaciones bancarias y el archivo de comprobantes. Trabajo presencial.',
                'profile' => [
                    'education' => 'Técnico o bachiller en Contabilidad',
                    'experience' => 'Mínimo 1 año en registros contables',
                    'functions' => 'Registrar operaciones contables; conciliar cuentas bancarias; preparar la documentación tributaria; archivar comprobantes.',
                    'competencies' => 'Contabilidad general, hojas de cálculo, sistemas contables, orden y precisión.',
                ],
                'criteria' => self::criteria(
                    ['Prueba de contabilidad', 'evaluacion', 50],
                    ['Manejo de hojas de cálculo', 'evaluacion', 20],
                    ['Entrevista personal', 'entrevista', 30],
                ),
            ],
            [
                'key' => 'demo-ofertas-09',
                'org' => 'demob',
                'title' => 'Coordinador/a de Operaciones',
                'area' => 'Operaciones',
                'contract_type' => 'tiempo_completo',
                'positions' => 1,
                'location' => 'Lima, Lima',
                'closes_in_days' => 37,
                'summary' => 'Coordinador/a de Operaciones para planificar el trabajo diario, coordinar proveedores y seguir los indicadores del área. Trabajo presencial.',
                'profile' => [
                    'education' => 'Bachiller en Ingeniería Industrial, Administración o afín',
                    'experience' => 'Mínimo 3 años coordinando equipos operativos',
                    'functions' => 'Planificar y supervisar las operaciones diarias; coordinar proveedores; controlar indicadores; proponer mejoras de procesos.',
                    'competencies' => 'Liderazgo, gestión de procesos, análisis de indicadores y negociación.',
                ],
                'criteria' => self::criteria(
                    ['Caso de gestión operativa', 'evaluacion', 40],
                    ['Análisis de indicadores', 'evaluacion', 20],
                    ['Entrevista personal', 'entrevista', 40],
                ),
            ],
            [
                'key' => 'demo-ofertas-10',
                'org' => 'demob',
                'title' => 'Técnico/a de Soporte TI',
                'area' => 'Tecnología',
                'contract_type' => 'por_horas',
                'positions' => 1,
                'location' => 'Lima, Lima',
                'closes_in_days' => 40,
                'summary' => 'Técnico/a de Soporte TI para la mesa de ayuda, la configuración de equipos y el mantenimiento de la red local. Por horas, presencial.',
                'profile' => [
                    'education' => 'Técnico en Computación, Redes o afín',
                    'experience' => 'Mínimo 1 año en mesa de ayuda',
                    'functions' => 'Atender tickets de soporte; instalar y configurar equipos; mantener la red local; documentar las soluciones.',
                    'competencies' => 'Soporte a usuarios, redes, sistemas operativos y documentación técnica.',
                ],
                'criteria' => self::criteria(
                    ['Prueba técnica de soporte', 'evaluacion', 40],
                    ['Diagnóstico de red', 'evaluacion', 30],
                    ['Entrevista personal', 'entrevista', 30],
                ),
            ],
        ];
    }
}
