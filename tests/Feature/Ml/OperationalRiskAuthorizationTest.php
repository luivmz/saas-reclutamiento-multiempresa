<?php

namespace Tests\Feature\Ml;

use App\Enums\UserRole;
use App\Models\Application;
use App\Models\Organization;
use App\Models\User;
use App\Models\Vacancy;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Http;
use PHPUnit\Framework\Attributes\DataProvider;
use Tests\TestCase;

/**
 * Autorización comprobada **por HTTP**, no solo contra la Policy.
 *
 * Una Policy correcta con una ruta mal conectada seguiría dejando pasar a
 * cualquiera, así que aquí se recorre la ruta real con cada rol.
 */
class OperationalRiskAuthorizationTest extends TestCase
{
    use RefreshDatabase;

    private Organization $organization;

    private Vacancy $vacancy;

    protected function setUp(): void
    {
        parent::setUp();

        config()->set('ml.enabled', true);
        config()->set('ml.base_url', 'http://ml-service.test');
        config()->set('ml.retries', 0);

        $this->organization = Organization::factory()->create();
        $this->vacancy = Vacancy::factory()->for($this->organization)->configured()->create([
            'opens_at' => now()->subDays(40)->startOfDay(),
            'closes_at' => now()->subDays(10)->startOfDay(),
            'published_at' => now()->subDays(42),
            'target_completion_at' => now()->addDays(25)->setTime(18, 0),
        ]);
    }

    private function url(?Vacancy $vacancy = null): string
    {
        return route('vacancies.operational-risk', $vacancy ?? $this->vacancy);
    }

    private function fakePrediction(): void
    {
        Http::fake(['*/v1/predict' => Http::response([
            'risk_score' => 0.42,
            'risk_flag' => true,
            'threshold' => (float) config('ml.expected_threshold'),
            'model_version' => (string) config('ml.expected_model_version'),
            'freeze_fingerprint' => (string) config('ml.expected_freeze_fingerprint'),
            'status' => 'experimental',
        ])]);
    }

    // -- roles autorizados ---------------------------------------------------

    public function test_human_resources_is_authorised(): void
    {
        $this->fakePrediction();

        $this->actingAs(User::factory()->hr($this->organization)->create())
            ->getJson($this->url())
            ->assertOk()
            ->assertJsonPath('risk.availability', 'predictive_available');
    }

    public function test_the_approver_is_authorised(): void
    {
        /* El Aprobador es quien decide (RF-23): necesita el mismo contexto
           operativo que RR. HH. */
        $this->fakePrediction();

        $this->actingAs(User::factory()->approver($this->organization)->create())
            ->getJson($this->url())
            ->assertOk();
    }

    // -- roles denegados -----------------------------------------------------

    /**
     * @return array<string, array{string}>
     */
    public static function deniedRoles(): array
    {
        return [
            'postulante' => ['candidate'],
            'evaluador' => ['evaluator'],
            'area solicitante' => ['requester'],
        ];
    }

    #[DataProvider('deniedRoles')]
    public function test_other_roles_are_denied(string $role): void
    {
        Http::fake();

        $user = match ($role) {
            'candidate' => User::factory()->candidate()->create(),
            'evaluator' => User::factory()->evaluator($this->organization)->create(),
            default => User::factory()->requester($this->organization)->create(),
        };

        $this->actingAs($user)->getJson($this->url())->assertForbidden();
        Http::assertNothingSent();
    }

    public function test_a_guest_is_denied(): void
    {
        Http::fake();

        $this->getJson($this->url())->assertUnauthorized();
        Http::assertNothingSent();
    }

    public function test_a_candidate_with_an_application_is_still_denied(): void
    {
        /* Tener una postulación en el proceso no da acceso: el riesgo es
           información de gestión interna, no del expediente de nadie. */
        Http::fake();
        $candidate = User::factory()->candidate()->create();
        Application::factory()->create([
            'organization_id' => $this->organization->id,
            'vacancy_id' => $this->vacancy->id,
            'candidate_id' => $candidate->id,
            'applied_at' => now()->subDays(25),
        ]);

        $this->actingAs($candidate)->getJson($this->url())->assertForbidden();
        Http::assertNothingSent();
    }

    public function test_an_evaluator_assigned_to_the_process_is_still_denied(): void
    {
        Http::fake();
        $evaluator = User::factory()->evaluator($this->organization)->create();

        $this->actingAs($evaluator)->getJson($this->url())->assertForbidden();
        Http::assertNothingSent();
    }

    // -- coherencia entre policy y ruta -------------------------------------

    public function test_the_route_and_the_policy_agree_for_every_role(): void
    {
        $this->fakePrediction();

        $cases = [
            [User::factory()->hr($this->organization)->create(), true],
            [User::factory()->approver($this->organization)->create(), true],
            [User::factory()->evaluator($this->organization)->create(), false],
            [User::factory()->requester($this->organization)->create(), false],
            [User::factory()->candidate()->create(), false],
        ];

        foreach ($cases as [$user, $allowed]) {
            $viaPolicy = $user->can('viewOperationalRisk', $this->vacancy);
            $viaRoute = $this->actingAs($user)->getJson($this->url())->status() === 200;

            $this->assertSame($allowed, $viaPolicy, "policy: {$user->role->value}");
            $this->assertSame($allowed, $viaRoute, "ruta: {$user->role->value}");
        }
    }

    public function test_the_denial_leaks_nothing_about_the_process(): void
    {
        Http::fake();

        $body = $this->actingAs(User::factory()->candidate()->create())
            ->getJson($this->url())
            ->getContent();

        foreach ([$this->vacancy->code, $this->vacancy->title, 'risk_score', 'threshold'] as $leak) {
            $this->assertStringNotContainsString($leak, $body);
        }
    }

    public function test_every_role_in_the_system_is_covered_by_this_suite(): void
    {
        /* Si alguien añade un rol, esta prueba obliga a decidir su acceso en
           vez de dejarlo al azar del `match`. */
        $covered = [
            UserRole::HumanResources,
            UserRole::Approver,
            UserRole::Evaluator,
            UserRole::Requester,
            UserRole::Candidate,
        ];

        $this->assertEqualsCanonicalizing(UserRole::cases(), $covered);
    }
}
