<?php

namespace Tests\Feature\Evidence;

use App\Enums\EvidenceSource;
use App\Enums\EvidenceType;
use App\Enums\UserRole;
use App\Models\Application;
use App\Models\Evaluation;
use App\Models\EvaluationCriterion;
use App\Models\EvidenceEvent;
use App\Models\EvidenceItem;
use App\Models\Interview;
use App\Models\Organization;
use App\Models\User;
use App\Models\Vacancy;
use App\Services\Evidence\EvidenceService;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Auth;
use Illuminate\Testing\TestResponse;
use PHPUnit\Framework\Attributes\DataProvider;
use Tests\TestCase;

/**
 * EXPERIMENTAL (exp/evidencias-ml02). The 38 fictitious scenarios of the F37 prototype
 * (docs/academico/preparacion-f37-evidencias/ejemplos/f37_ejemplos_ficticios.json), replayed against the real
 * HTTP endpoints, policy, form requests, service and PostgreSQL triggers. Each scenario starts from a fresh database
 * with the prototype's two organizations, nine users, three vacancies, four applications, three assignments and
 * four initial evidence records. Expected results come from the JSON, not from this test.
 */
class EvidenceScenarioTest extends TestCase
{
    use RefreshDatabase;

    private const EXAMPLES = 'docs/academico/preparacion-f37-evidencias/ejemplos/f37_ejemplos_ficticios.json';

    /** @var array<string, User> */
    private array $users = [];

    /** @var array<string, Application> */
    private array $applications = [];

    /** @var array<string, int> */
    private array $criteria = [];

    /** @var array<string, EvidenceItem> */
    private array $evidence = [];

    /**
     * @return array<string, mixed>
     */
    private static function examples(): array
    {
        return json_decode((string) file_get_contents(dirname(__DIR__, 3).'/'.self::EXAMPLES), true, flags: JSON_THROW_ON_ERROR);
    }

    /**
     * @return array<string, array{string}>
     */
    public static function scenarios(): array
    {
        $cases = [];
        foreach (self::examples()['scenarios'] as $scenario) {
            $cases["{$scenario['id']} {$scenario['rule']} {$scenario['action']} → {$scenario['expected']}"] = [$scenario['id']];
        }

        return $cases;
    }

    protected function setUp(): void
    {
        parent::setUp();
        config()->set('experimental.evidencias', true);
    }

    public function test_the_examples_keep_38_scenarios_12_allowed_and_26_denied(): void
    {
        $expected = array_count_values(array_column(self::examples()['scenarios'], 'expected'));

        $this->assertSame(['permitido' => 12, 'denegado' => 26], $expected);
    }

    #[DataProvider('scenarios')]
    public function test_scenario_matches_the_prototype(string $id): void
    {
        $data = self::examples();
        $scenario = collect($data['scenarios'])->firstWhere('id', $id);
        $this->buildFixture($data);

        foreach ($scenario['setup'] ?? [] as $step) {
            $this->runThroughService($step['actor'], $step['action'], $step['params']);
        }

        $before = [EvidenceItem::query()->withoutGlobalScopes()->count(), EvidenceEvent::query()->withoutGlobalScopes()->count()];
        Auth::forgetGuards();

        $response = $this->perform($scenario['actor'], $scenario['action'], $scenario['params']);
        $allowed = $this->wasAllowed($response, $scenario['action']);

        $this->assertSame(
            $scenario['expected'] === 'permitido',
            $allowed,
            "{$id}: esperado {$scenario['expected']}, respuesta {$response->getStatusCode()} ".json_encode(session('errors'), JSON_UNESCAPED_UNICODE),
        );

        if (! $allowed) {
            $after = [EvidenceItem::query()->withoutGlobalScopes()->count(), EvidenceEvent::query()->withoutGlobalScopes()->count()];
            $this->assertSame($before, $after, "{$id}: una acción denegada no debe insertar filas");
        }
    }

    /**
     * @param  array<string, mixed>  $data
     */
    private function buildFixture(array $data): void
    {
        $orgs = [];
        foreach ($data['organizations'] as $token) {
            $orgs[$token] = Organization::factory()->create();
        }

        foreach ($data['users'] as $u) {
            $role = UserRole::from($u['role']);
            $this->users[$u['token']] = User::factory()->state([
                'role' => $role,
                'organization_id' => $u['org'] ? $orgs[$u['org']]->id : null,
            ])->create();
        }

        $vacancies = [];
        foreach ($data['vacancies'] as $v) {
            $factory = Vacancy::factory()->state(['organization_id' => $orgs[$v['org']]->id]);
            $vacancies[$v['token']] = ($v['status'] === 'cerrada' ? $factory->closed() : $factory->published())->create();

            foreach ($v['criteria'] as $position => $token) {
                $this->criteria[$token] = EvaluationCriterion::factory()->state([
                    'vacancy_id' => $vacancies[$v['token']]->id,
                    'name' => "[SINTÉTICO] {$token}",
                    'position' => $position,
                ])->create()->id;
            }
        }

        foreach ($data['applications'] as $a) {
            $candidate = $this->users[$a['candidate']] ?? User::factory()->candidate()->create();
            $this->applications[$a['token']] = Application::factory()
                ->state(['vacancy_id' => $vacancies[$a['vacancy']]->id])
                ->forCandidate($candidate)
                ->create();
        }

        foreach ($data['assignments'] as $assignment) {
            $application = $this->applications[$assignment['application']];
            $hr = User::query()->where('organization_id', $application->organization_id)->where('role', UserRole::HumanResources)->first();
            $factory = $assignment['session'] === 'entrevista' ? Interview::factory() : Evaluation::factory();
            $factory->forApplication($application)
                ->assignedTo($this->users[$assignment['evaluator']])
                ->state(['scheduled_by' => $hr->id])
                ->create();
        }

        foreach ($data['initial_evidence'] as $i => $item) {
            $this->runThroughService($item['registered_by'], 'registrar', $item);
        }
    }

    /**
     * Setup steps and initial records go through the service, like the prototype's `execute`. Evidence tokens follow
     * the prototype's numbering: EVD-<org>-<global sequence>.
     *
     * @param  array<string, mixed>  $params
     */
    private function runThroughService(string $actorToken, string $action, array $params): void
    {
        $actor = $this->users[$actorToken];
        $service = app(EvidenceService::class);
        $this->actingAs($actor);

        $item = match ($action) {
            'registrar' => $service->register($actor, $this->applications[$params['application']], EvidenceType::from($params['type']), EvidenceSource::from($params['source']), $params['description']),
            'corregir' => $service->correct($actor, $this->evidence[$params['evidence']], EvidenceType::from($params['type'] ?? $this->evidence[$params['evidence']]->type->value), EvidenceSource::from($params['source']), $params['description']),
            'revisar' => $service->review($actor, $this->evidence[$params['evidence']]),
            default => throw new \LogicException("acción de preparación no prevista: {$action}"),
        };

        if ($item instanceof EvidenceItem) {
            $org = substr($this->tokenOf($actor), 4, 2);
            $this->evidence[sprintf('EVD-%s-%04d', $org, count($this->evidence) + 1)] = $item;
        }
    }

    private function tokenOf(User $user): string
    {
        return (string) array_search($user, $this->users, true);
    }

    /**
     * @param  array<string, mixed>  $params
     */
    private function perform(string $actorToken, string $action, array $params): TestResponse
    {
        if (isset($this->users[$actorToken])) {
            $this->actingAs($this->users[$actorToken]);
        }

        $evidence = isset($params['evidence']) ? ($this->evidence[$params['evidence']] ?? null) : null;
        $applicationId = isset($params['application'])
            ? ($this->applications[$params['application']]->id ?? 999999)
            : $evidence?->application_id;
        $body = array_diff_key($params, array_flip(['application', 'evidence', 'criterion']));
        if (isset($params['criterion'])) {
            $body['criterion_id'] = $this->criteria[$params['criterion']];
        }

        return match ($action) {
            'consultar' => $this->get(route('applications.evidence.index', $applicationId)),
            'historial' => $this->get(route('applications.evidence.history', $applicationId)),
            'registrar' => $this->post(route('applications.evidence.store', $applicationId), $body),
            'enlazar' => $this->post(route('evidence.link', $evidence), $body),
            'desenlazar' => $this->delete(route('evidence.unlink', [$evidence, $body['criterion_id']])),
            'revisar' => $this->post(route('evidence.review', $evidence), $body),
            'corregir' => $this->post(route('evidence.correct', $evidence), $body),
            'retirar' => $this->post(route('evidence.withdraw', $evidence), $body),
        };
    }

    private function wasAllowed(TestResponse $response, string $action): bool
    {
        if (in_array($action, ['consultar', 'historial'], true)) {
            return $response->getStatusCode() === 200;
        }

        return $response->isRedirect()
            && str_contains((string) $response->headers->get('Location'), '/evidencias')
            && ! session()->has('errors');
    }
}
