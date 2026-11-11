<?php

namespace Tests\Feature\Evidence;

use App\Enums\AuditAction;
use App\Enums\EvidenceState;
use App\Http\Requests\Evidence\EvidenceWriteRequest;
use App\Models\Application;
use App\Models\AuditLog;
use App\Models\Evaluation;
use App\Models\EvaluationCriterion;
use App\Models\EvidenceEvent;
use App\Models\EvidenceItem;
use App\Models\Organization;
use App\Models\User;
use App\Models\Vacancy;
use App\Services\Audit\AuditLogger;
use App\Services\Evidence\EvidenceLedger;
use App\Services\Evidence\EvidenceService;
use Illuminate\Database\QueryException;
use Illuminate\Validation\ValidationException;
use RuntimeException;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\DB;
use Inertia\Testing\AssertableInertia;
use Tests\TestCase;

/**
 * EXPERIMENTAL (exp/evidencias-ml02). End-to-end behaviour of the evidence flow on the real stack: versions,
 * inherited links, append-only storage at database level, audit without text, tenant isolation for every role and
 * route, the disabled flag and the documentary aid on the page. All data are fictitious.
 */
class EvidenceFlowTest extends TestCase
{
    use RefreshDatabase;

    private const MARKER = 'FLUJO-TEXTO-PRIVADO-7731';

    private Organization $org;

    private User $hr;

    private User $director;

    private User $evaluator;

    private Application $application;

    private EvaluationCriterion $planning;

    private EvaluationCriterion $teaching;

    protected function setUp(): void
    {
        parent::setUp();
        config()->set('experimental.evidencias', true);

        $this->org = Organization::factory()->create();
        $this->hr = User::factory()->hr($this->org)->create();
        $this->director = User::factory()->approver($this->org)->create();
        $this->evaluator = User::factory()->evaluator($this->org)->create();

        $vacancy = Vacancy::factory()->published()->state(['organization_id' => $this->org->id])->create();
        $this->planning = EvaluationCriterion::factory()->state(['vacancy_id' => $vacancy->id, 'name' => 'Planificación de la enseñanza', 'position' => 0])->create();
        $this->teaching = EvaluationCriterion::factory()->state(['vacancy_id' => $vacancy->id, 'name' => 'Conducción de la clase', 'position' => 1])->create();

        $this->application = Application::factory()->state(['vacancy_id' => $vacancy->id])->create();
        Evaluation::factory()->forApplication($this->application)->assignedTo($this->evaluator)->state(['scheduled_by' => $this->hr->id])->create();
    }

    public function test_routes_answer_404_when_the_experimental_flag_is_off(): void
    {
        config()->set('experimental.evidencias', false);

        $this->actingAs($this->hr)->get(route('applications.evidence.index', $this->application))->assertNotFound();
        $this->actingAs($this->hr)->post(route('applications.evidence.store', $this->application), $this->certificate())->assertNotFound();
        $this->assertSame(0, EvidenceItem::query()->count());
    }

    public function test_full_flow_keeps_every_version_and_derives_the_state(): void
    {
        $this->actingAs($this->hr)->post(route('applications.evidence.store', $this->application), $this->certificate())
            ->assertRedirect(route('applications.evidence.index', $this->application))->assertSessionHasNoErrors();
        $first = EvidenceItem::query()->sole();

        $this->post(route('evidence.link', $first), ['criterion_id' => $this->planning->id])->assertSessionHasNoErrors();
        $this->post(route('evidence.review', $first))->assertSessionHasNoErrors();
        $this->post(route('evidence.correct', $first), [
            'source' => 'documento_presentado',
            'description' => '[SINTÉTICO] Certificado ficticio corregido: curso de planificación de unidades.',
        ])->assertSessionHasNoErrors();

        $second = EvidenceItem::query()->where('supersedes_id', $first->id)->sole();
        $ledger = EvidenceLedger::for($this->application);

        $this->assertSame(EvidenceState::Superseded, $ledger->state($first->fresh()));
        $this->assertSame(EvidenceState::Registered, $ledger->state($second), 'la revisión no se hereda: la versión nueva se revisa otra vez');
        $this->assertSame([$this->planning->id], $ledger->activeLinks($second), 'la versión nueva hereda los enlaces vigentes');
        $this->assertSame('[SINTÉTICO] Certificado ficticio de un curso de planificación curricular. '.self::MARKER, $first->fresh()->description, 'la versión anterior no se modifica');

        $this->delete(route('evidence.unlink', [$second, $this->planning->id]))->assertSessionHasNoErrors();
        $this->post(route('evidence.withdraw', $second), ['reason' => '[SINTÉTICO] Duplicado por error de carga.'])->assertSessionHasNoErrors();

        $ledger = EvidenceLedger::for($this->application);
        $this->assertSame(EvidenceState::Withdrawn, $ledger->state($second));
        $this->assertSame([], $ledger->activeLinks($second));
        $this->assertSame(2, EvidenceItem::query()->count());
        $this->assertSame(
            ['enlazada', 'revisada', 'enlazada', 'enlace_retirado', 'retirada'],
            EvidenceEvent::query()->orderBy('id')->pluck('action')->all(),
        );

        $this->post(route('evidence.correct', $second), ['source' => 'documento_presentado', 'description' => '[SINTÉTICO] Tarde.'])
            ->assertSessionHasErrors('evidence');
    }

    /**
     * Codex plan, step 3: if the audit row of a correction fails, the new version and its inherited links roll back
     * with it; nothing is left half-written.
     */
    public function test_a_failing_audit_rolls_back_the_correction_and_its_inherited_links(): void
    {
        $this->actingAs($this->hr)->post(route('applications.evidence.store', $this->application), $this->certificate());
        $item = EvidenceItem::query()->sole();
        $this->post(route('evidence.link', $item), ['criterion_id' => $this->planning->id]);
        $rows = [EvidenceItem::query()->count(), EvidenceEvent::query()->count(), AuditLog::query()->count()];

        $real = app(AuditLogger::class);
        $this->mock(AuditLogger::class, function ($mock) use ($real) {
            $mock->shouldReceive('record')->andReturnUsing(function (AuditAction $action, ...$rest) use ($real) {
                if ($action === AuditAction::EvidenceCorrected) {
                    throw new RuntimeException('fallo simulado de auditoría');
                }

                return $real->record($action, ...$rest);
            });
        });

        try {
            app(EvidenceService::class)->correct($this->hr, $item->fresh(), $item->type, $item->source, '[SINTÉTICO] Versión que no debe quedar.');
            $this->fail('La corrección debía fallar con la auditoría.');
        } catch (RuntimeException $e) {
            $this->assertSame('fallo simulado de auditoría', $e->getMessage());
        }

        $this->assertSame($rows, [EvidenceItem::query()->count(), EvidenceEvent::query()->count(), AuditLog::query()->count()]);
        $this->assertSame(EvidenceState::Registered, EvidenceLedger::for($this->application)->state($item->fresh()));
    }

    public function test_correcting_the_same_version_twice_is_rejected_without_a_second_successor(): void
    {
        $this->actingAs($this->hr)->post(route('applications.evidence.store', $this->application), $this->certificate());
        $item = EvidenceItem::query()->sole();
        $service = app(EvidenceService::class);
        $service->correct($this->hr, $item->fresh(), $item->type, $item->source, '[SINTÉTICO] Primera corrección.');

        $this->expectException(ValidationException::class);
        try {
            $service->correct($this->hr, $item->fresh(), $item->type, $item->source, '[SINTÉTICO] Segunda corrección de la misma versión.');
        } finally {
            $this->assertSame(1, EvidenceItem::query()->where('supersedes_id', $item->id)->count());
            $this->assertSame(2, EvidenceItem::query()->count());
        }
    }

    public function test_the_database_refuses_updates_and_deletes(): void
    {
        $this->actingAs($this->hr)->post(route('applications.evidence.store', $this->application), $this->certificate());
        $this->post(route('evidence.link', EvidenceItem::query()->sole()), ['criterion_id' => $this->planning->id]);

        foreach ([
            fn () => DB::table('evidence_items')->update(['description' => '[SINTÉTICO] reescrito']),
            fn () => DB::table('evidence_items')->delete(),
            fn () => DB::table('evidence_events')->update(['action' => 'revisada']),
            fn () => DB::table('evidence_events')->delete(),
        ] as $i => $attempt) {
            try {
                DB::transaction($attempt);
                $this->fail("la operación {$i} debía fallar");
            } catch (QueryException $e) {
                $this->assertStringContainsString('solo inserción', $e->getMessage());
            }
        }

        $this->assertSame(1, EvidenceItem::query()->count());
        $this->assertSame(1, EvidenceEvent::query()->count());
    }

    public function test_audit_rows_carry_identifiers_and_never_the_text(): void
    {
        $this->actingAs($this->hr)->post(route('applications.evidence.store', $this->application), $this->certificate());
        $item = EvidenceItem::query()->sole();
        $this->post(route('evidence.link', $item), ['criterion_id' => $this->planning->id]);
        $this->post(route('evidence.withdraw', $item), ['reason' => '[SINTÉTICO] Motivo privado '.self::MARKER]);

        $logs = AuditLog::query()->where('auditable_type', $item->getMorphClass())->orderBy('id')->get();

        $this->assertSame(
            [AuditAction::EvidenceRegistered, AuditAction::EvidenceLinked, AuditAction::EvidenceWithdrawn],
            $logs->pluck('action')->all(),
        );
        foreach ($logs as $log) {
            $this->assertStringNotContainsString(self::MARKER, json_encode($log->getAttributes(), JSON_UNESCAPED_UNICODE));
            $this->assertEmpty(array_diff(array_keys($log->metadata), ['evidence_id', 'application_id', 'criterion_id', 'supersedes_id']));
        }
    }

    public function test_another_organization_reaches_nothing_with_any_role_or_route(): void
    {
        $this->actingAs($this->hr)->post(route('applications.evidence.store', $this->application), $this->certificate());
        $item = EvidenceItem::query()->sole();
        $rows = [EvidenceItem::query()->withoutGlobalScopes()->count(), EvidenceEvent::query()->withoutGlobalScopes()->count()];

        $other = Organization::factory()->create();
        $outsiders = [
            User::factory()->hr($other)->create(),
            User::factory()->approver($other)->create(),
            User::factory()->evaluator($other)->create(),
            User::factory()->requester($other)->create(),
            User::factory()->candidate()->create(),
        ];

        foreach ($outsiders as $user) {
            $this->actingAs($user);
            foreach ([
                $this->get(route('applications.evidence.index', $this->application)),
                $this->get(route('applications.evidence.history', $this->application)),
                $this->post(route('applications.evidence.store', $this->application), $this->certificate()),
                $this->post(route('evidence.link', $item), ['criterion_id' => $this->planning->id]),
                $this->delete(route('evidence.unlink', [$item, $this->planning->id])),
                $this->post(route('evidence.review', $item)),
                $this->post(route('evidence.correct', $item), ['source' => 'documento_presentado', 'description' => '[SINTÉTICO] x']),
                $this->post(route('evidence.withdraw', $item), ['reason' => '[SINTÉTICO] x']),
            ] as $response) {
                $this->assertContains($response->getStatusCode(), [403, 404], "{$user->role->value} alcanzó una ruta de otra organización");
            }
        }

        $this->assertSame($rows, [EvidenceItem::query()->withoutGlobalScopes()->count(), EvidenceEvent::query()->withoutGlobalScopes()->count()]);
    }

    public function test_the_page_never_exposes_the_candidate_and_shows_the_documentary_aid(): void
    {
        $candidate = $this->application->candidate;
        $this->actingAs($this->hr)->post(route('applications.evidence.store', $this->application), [
            'type' => 'cv', 'source' => 'documento_presentado',
            'description' => '[SINTÉTICO] Elaboró la planificación anual y las unidades didácticas del área.',
        ]);
        $this->actingAs($this->evaluator)->post(route('applications.evidence.store', $this->application), [
            'type' => 'observacion', 'source' => 'sesion_asignada',
            'description' => '[SINTÉTICO] Inició la clase modelo presentando los objetivos.',
        ]);

        $response = $this->actingAs($this->director)
            ->get(route('applications.evidence.index', ['application' => $this->application, 'criterio' => $this->planning->id]));

        $response->assertOk()->assertInertia(fn (AssertableInertia $page) => $page
            ->component('evidence/index')
            ->has('records', 2)
            ->where('aid.criterion.id', $this->planning->id)
            ->where('aid.abstained', false)
            ->has('aid.results', 1)
            ->where('aid.results.0.code', EvidenceItem::query()->orderBy('id')->first()->code())
            ->where('aid.results.0.source.value', 'documento_presentado')
            ->where('aid.results.0.matched_words', ['planificación'])
            ->where('can.create', false)
            ->where('can.viewHistory', true));

        $this->assertStringNotContainsString($candidate->name, $response->getContent());
        $this->assertStringNotContainsString($candidate->email, $response->getContent());
    }

    public function test_the_aid_abstains_without_shared_words_and_says_why(): void
    {
        $this->actingAs($this->hr)->post(route('applications.evidence.store', $this->application), [
            'type' => 'certificado', 'source' => 'documento_presentado',
            'description' => '[SINTÉTICO] Constancia ficticia de un curso de ofimática.',
        ]);

        $this->get(route('applications.evidence.index', ['application' => $this->application, 'criterio' => $this->teaching->id]))
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->where('aid.abstained', true)
                ->has('aid.results', 0)
                ->where('aid.query_terms', ['conduccion', 'clas']));
    }

    /**
     * CONT-M01 (Codex, 09/11/2026), on the real stack: HR cannot correct someone else's observation by declaring
     * the replacement as a CV from a submitted document. Authorization looks at the original evidence first.
     */
    public function test_hr_cannot_rewrite_an_observation_by_declaring_another_type(): void
    {
        $this->actingAs($this->evaluator)->post(route('applications.evidence.store', $this->application), [
            'type' => 'observacion', 'source' => 'sesion_asignada',
            'description' => '[SINTÉTICO] Observación ficticia de la sesión asignada.',
        ]);
        $observation = EvidenceItem::query()->sole();

        $this->actingAs($this->hr)->post(route('evidence.correct', $observation), [
            'type' => 'cv', 'source' => 'documento_presentado',
            'description' => '[SINTÉTICO] Reescritura como CV.',
        ])->assertForbidden();

        $this->assertSame(1, EvidenceItem::query()->count());
        $this->assertSame(EvidenceState::Registered, EvidenceLedger::for($this->application)->state($observation));
    }

    /**
     * R-01 in the policy itself, not only through the organization scope of route binding: a model of another
     * organization handed straight to the gate is denied for every ability and role.
     */
    public function test_the_policy_alone_denies_another_organization(): void
    {
        $this->actingAs($this->hr)->post(route('applications.evidence.store', $this->application), $this->certificate());
        $item = EvidenceItem::query()->sole();

        $other = Organization::factory()->create();
        foreach ([User::factory()->hr($other)->create(), User::factory()->approver($other)->create(), User::factory()->evaluator($other)->create()] as $outsider) {
            $application = Application::query()->withoutGlobalScopes()->findOrFail($this->application->id);
            $evidence = EvidenceItem::query()->withoutGlobalScopes()->findOrFail($item->id);

            foreach (['viewAny', 'viewHistory', 'create'] as $ability) {
                $this->assertFalse($outsider->can($ability, [EvidenceItem::class, $application]), "{$outsider->role->value} {$ability}");
            }
            foreach (['link', 'review', 'correct', 'withdraw'] as $ability) {
                $this->assertFalse($outsider->can($ability, $evidence), "{$outsider->role->value} {$ability}");
            }
        }
    }

    public function test_evaluator_sees_assigned_evidence_but_not_the_history(): void
    {
        $this->actingAs($this->evaluator)->get(route('applications.evidence.index', $this->application))->assertOk();
        $this->actingAs($this->evaluator)->get(route('applications.evidence.history', $this->application))->assertForbidden();
        $this->actingAs($this->hr)->get(route('applications.evidence.history', $this->application))->assertOk();
    }

    public function test_forbidden_field_tokens_are_exactly_those_of_the_evidence_contract(): void
    {
        $contract = json_decode((string) file_get_contents(base_path('docs/academico/f36-sbx/contrato/f36sbx_evidence_contract.json')), true);

        $this->assertSame($contract['forbidden_field_tokens'], EvidenceWriteRequest::FORBIDDEN_FIELD_TOKENS);
        $this->assertSame(['candidate', 'score'], EvidenceWriteRequest::fieldTokens('candidateScore'));
        $this->assertSame(['nested.finalVerdict'], EvidenceWriteRequest::forbiddenFields(['nested' => ['finalVerdict' => 1, 'ok' => 2]]));
    }

    public function test_ranking_and_final_decision_do_not_read_evidence(): void
    {
        $sources = array_merge(
            glob(app_path('Services/Ranking/*.php')),
            glob(app_path('Services/Selection/*.php')),
            glob(app_path('Services/Ml/*.php')),
            glob(app_path('Http/Controllers/Selection/*.php')),
        );

        $this->assertNotEmpty($sources);
        foreach ($sources as $file) {
            $this->assertStringNotContainsString('Evidence', (string) file_get_contents($file), basename($file).' no debe leer evidencias (R-06)');
        }
    }

    /**
     * @return array<string, string>
     */
    private function certificate(): array
    {
        return [
            'type' => 'certificado',
            'source' => 'documento_presentado',
            'description' => '[SINTÉTICO] Certificado ficticio de un curso de planificación curricular. '.self::MARKER,
        ];
    }
}
