<?php

namespace Tests\Feature\Candidates;

use App\Enums\EducationLevel;
use App\Http\Requests\Candidates\CandidateCvRequest;
use App\Models\Application;
use App\Models\CandidateProfile;
use App\Models\Organization;
use App\Models\User;
use App\Models\Vacancy;
use Carbon\CarbonImmutable;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Http\Request;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;
use Inertia\Testing\AssertableInertia;
use Laravel\Passkeys\Contracts\PasskeyLoginResponse;
use PHPUnit\Framework\Attributes\DataProvider;
use Tests\TestCase;

/**
 * Lote 2 de UX: la convocatoria elegida se conserva al crear la cuenta, iniciar sesión (con contraseña, segundo
 * factor o clave de acceso) y completar el perfil. Solo se acepta el identificador de una vacante publicada;
 * volver nunca postula por nadie y la autorización sigue en el servidor.
 */
class VacancyReturnTest extends TestCase
{
    use RefreshDatabase;

    private Organization $organization;

    private Vacancy $vacancy;

    protected function setUp(): void
    {
        parent::setUp();

        $this->travelTo(CarbonImmutable::parse('2026-11-23 10:00', config('app.timezone')));
        $this->organization = Organization::factory()->create();
        $this->vacancy = Vacancy::factory()->for($this->organization)->configured()->published()
            ->create(['title' => 'Docente de Prueba', 'opens_at' => '2026-11-01', 'closes_at' => '2026-12-20']);
    }

    private function candidate(): User
    {
        return User::factory()->candidate()->create();
    }

    public function test_login_page_shows_the_chosen_vacancy_and_login_returns_to_it(): void
    {
        $candidate = $this->candidate();

        $this->get('/login?convocatoria='.$this->vacancy->id)
            ->assertOk()
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->component('auth/login')
                ->where('convocatoria', ['id' => $this->vacancy->id, 'title' => 'Docente de Prueba']));

        $this->post(route('login'), ['email' => $candidate->email, 'password' => 'password'])
            ->assertRedirect(route('jobs.show', $this->vacancy->id));

        $this->assertSame(0, Application::query()->withoutGlobalScopes()->count(), 'Volver no postula');
    }

    public function test_registration_returns_to_the_vacancy_and_announces_the_requirements(): void
    {
        $this->get('/register?convocatoria='.$this->vacancy->id)
            ->assertOk()
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->component('auth/register')
                ->where('convocatoria.id', $this->vacancy->id)
                ->where('requisitos.perfil', array_values(CandidateProfile::REQUIRED_FIELDS))
                ->where('requisitos.cv.formato', 'PDF')
                ->where('requisitos.cv.max_kb', CandidateCvRequest::maxKilobytes()));

        $this->post(route('register.store'), [
            'name' => 'Postulante Ficticia',
            'email' => 'ficticia.retorno@correo.test',
            'password' => 'password',
            'password_confirmation' => 'password',
        ])->assertRedirect(route('jobs.show', $this->vacancy->id));

        $this->assertAuthenticated();
    }

    public function test_two_factor_login_returns_to_the_vacancy_after_the_challenge(): void
    {
        $candidate = User::factory()->candidate()->withTwoFactor()->create();

        $this->get('/login?convocatoria='.$this->vacancy->id)->assertOk();
        $this->post(route('login'), ['email' => $candidate->email, 'password' => 'password'])
            ->assertRedirect(route('two-factor.login'));
        $this->assertGuest();

        $this->post(route('two-factor.login.store'), ['recovery_code' => 'recovery-code-1'])
            ->assertRedirect(route('jobs.show', $this->vacancy->id));
        $this->assertAuthenticatedAs($candidate);
    }

    public function test_passkey_login_response_also_returns_to_the_vacancy(): void
    {
        $candidate = $this->candidate();
        $this->get('/login?convocatoria='.$this->vacancy->id)->assertOk();
        $this->actingAs($candidate);

        $request = Request::create('/passkeys/login', 'POST');
        $request->setLaravelSession(app('session.store'));
        $request->setUserResolver(fn () => $candidate);

        $response = app(PasskeyLoginResponse::class)->toResponse($request);

        $this->assertSame(route('jobs.show', $this->vacancy->id), $response->getTargetUrl());
    }

    public function test_profile_keeps_the_vacancy_until_it_is_complete_and_then_offers_the_way_back(): void
    {
        Storage::fake('local');
        $candidate = $this->candidate();

        $this->actingAs($candidate)
            ->get(route('candidate.profile.edit', ['convocatoria' => $this->vacancy->id]))
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->where('retorno.disponible', true)
                ->where('retorno.id', $this->vacancy->id)
                ->where('retorno.title', 'Docente de Prueba')
                ->where('retorno.accepts_applications', true)
                ->where('cv', null));

        $this->put(route('candidate.profile.update'), [
            'phone' => '987654321',
            'city' => 'Huancayo',
            'education_level' => EducationLevel::cases()[0]->value,
            'professional_title' => 'Docente ficticia',
            'years_of_experience' => 3,
        ])->assertSessionHasNoErrors();
        $this->post(route('candidate.cv.store'), ['cv' => UploadedFile::fake()->create('cv.pdf', 200, 'application/pdf')])
            ->assertSessionHasNoErrors();

        // Sin parámetro, el perfil conserva la convocatoria y ya no falta nada.
        $this->get(route('candidate.profile.edit'))
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->where('retorno.id', $this->vacancy->id)
                ->where('missingFields', [])
                ->whereNot('cv', null));

        $this->get(route('jobs.show', $this->vacancy))
            ->assertOk()
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->where('candidate.profileComplete', true)
                ->where('candidate.hasCv', true)
                ->where('candidate.application', null));
        $this->assertSame(0, Application::query()->withoutGlobalScopes()->count(), 'Volver no postula');

        // Postular es una acción explícita y cierra el recorrido.
        $this->post(route('jobs.apply', $this->vacancy))->assertRedirect();
        $this->get(route('candidate.profile.edit'))
            ->assertInertia(fn (AssertableInertia $page) => $page->where('retorno', null));
    }

    /**
     * `{id}` se sustituye por el de la convocatoria publicada: cada variante «casi válida» apunta a una que sí
     * existe, así que solo el rechazo del formato explica que se ignore.
     *
     * @return array<string, array{string}>
     */
    public static function invalidDestinations(): array
    {
        return [
            'url externa' => ['https://sitio-externo.test/empleos/{id}'],
            'doble barra' => ['//sitio-externo.test'],
            'ruta interna' => ['/empleos/{id}'],
            'barra invertida' => ['\\\\sitio-externo.test'],
            'sufijo' => ['{id}abc'],
            'negativo' => ['-{id}'],
            'cero' => ['0'],
            'cero a la izquierda' => ['0{id}'],
            'espacio delante' => [' {id}'],
            'salto de línea detrás' => ["{id}\n"],
            'byte nulo detrás' => ["{id}\0"],
            'espacio de ancho cero' => ["\u{200B}{id}"],
            'codificado dos veces' => ['%2F%2Fsitio-externo.test'],
            'desbordado' => ['99999999999'],
        ];
    }

    #[DataProvider('invalidDestinations')]
    public function test_anything_but_the_id_of_a_published_vacancy_is_ignored(string $value): void
    {
        $candidate = $this->candidate();
        $value = str_replace('{id}', (string) $this->vacancy->id, $value);

        $this->get('/login?convocatoria='.rawurlencode($value))
            ->assertOk()
            ->assertInertia(fn (AssertableInertia $page) => $page->where('convocatoria', null));

        $this->post(route('login'), ['email' => $candidate->email, 'password' => 'password'])
            ->assertRedirect(route('dashboard'));
    }

    public function test_an_array_parameter_is_ignored(): void
    {
        $this->get('/login?convocatoria[]='.$this->vacancy->id)
            ->assertOk()
            ->assertInertia(fn (AssertableInertia $page) => $page->where('convocatoria', null));
    }

    public function test_draft_or_closed_vacancies_cannot_be_chosen(): void
    {
        $draft = Vacancy::factory()->for($this->organization)->configured()->create();
        $closed = Vacancy::factory()->for($this->organization)->configured()->closed()
            ->create(['opens_at' => '2026-10-01', 'closes_at' => '2026-10-20']);

        foreach ([$draft, $closed] as $vacancy) {
            $this->get('/login?convocatoria='.$vacancy->id)
                ->assertInertia(fn (AssertableInertia $page) => $page->where('convocatoria', null));
        }
    }

    public function test_other_roles_keep_their_navigation(): void
    {
        $hr = User::factory()->hr($this->organization)->create();

        $this->get('/login?convocatoria='.$this->vacancy->id)->assertOk();
        $this->post(route('login'), ['email' => $hr->email, 'password' => 'password'])
            ->assertRedirect(route('dashboard'));

        // La intención no queda pendiente para un acceso posterior en la misma sesión.
        $this->assertFalse(session()->has('postulacion.retorno'));
    }

    public function test_a_vacancy_that_closed_meanwhile_leads_to_the_listing_with_a_notice(): void
    {
        $candidate = $this->candidate();
        $this->get('/login?convocatoria='.$this->vacancy->id)->assertOk();

        $this->vacancy->forceFill(['status' => 'cerrada', 'closed_at' => now(), 'closure_type' => 'desierta'])->save();

        $this->post(route('login'), ['email' => $candidate->email, 'password' => 'password'])
            ->assertRedirect(route('jobs.index'));
        $this->assertFalse(session()->has('postulacion.retorno'));
    }

    public function test_a_vacancy_whose_deadline_passed_still_returns_to_its_detail_showing_the_real_state(): void
    {
        $candidate = $this->candidate();
        // Elige la convocatoria el último día del plazo y entra pasada la medianoche, dentro de la vigencia.
        $this->travelTo(CarbonImmutable::parse('2026-12-20 23:30', config('app.timezone')));
        $this->get('/login?convocatoria='.$this->vacancy->id)->assertOk();
        $this->travelTo(CarbonImmutable::parse('2026-12-21 00:30', config('app.timezone')));

        $this->post(route('login'), ['email' => $candidate->email, 'password' => 'password'])
            ->assertRedirect(route('jobs.show', $this->vacancy->id));
        $this->get(route('jobs.show', $this->vacancy))
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->where('vacancy.accepts_applications', false)
                ->where('vacancy.application_deadline_passed', true));
    }

    public function test_the_intent_expires_and_is_dropped_when_entering_without_it(): void
    {
        $candidate = $this->candidate();

        $this->get('/login?convocatoria='.$this->vacancy->id)->assertOk();
        $this->travel(3)->hours();
        $this->post(route('login'), ['email' => $candidate->email, 'password' => 'password'])
            ->assertRedirect(route('dashboard'));
        $this->post(route('logout'));

        $this->get('/login?convocatoria='.$this->vacancy->id)->assertOk();
        $this->get('/login')->assertInertia(fn (AssertableInertia $page) => $page->where('convocatoria', null));
        $this->post(route('login'), ['email' => $candidate->email, 'password' => 'password'])
            ->assertRedirect(route('dashboard'));
    }

    public function test_the_profile_route_stays_restricted_to_candidates(): void
    {
        $this->get(route('candidate.profile.edit', ['convocatoria' => $this->vacancy->id]))
            ->assertRedirect(route('login'));

        $this->actingAs(User::factory()->hr($this->organization)->create())
            ->get(route('candidate.profile.edit', ['convocatoria' => $this->vacancy->id]))
            ->assertForbidden();
    }
}
