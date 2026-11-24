<?php

namespace Tests\Feature\Frontend;

use App\Models\Organization;
use App\Models\User;
use App\Models\Vacancy;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Session\TokenMismatchException;
use Illuminate\Support\Facades\Route;
use Tests\TestCase;

/**
 * DEF-28: los errores 403, 404 y 419 usaban las plantillas de Laravel, en inglés y sin salida, y el 403
 * imprimía el mensaje de la excepción. Ahora son páginas propias en español con una salida según la sesión.
 * Los códigos HTTP, las respuestas JSON y la autorización no cambian.
 */
class ErrorPagesTest extends TestCase
{
    use RefreshDatabase;

    public function test_not_found_page_is_in_spanish_and_offers_public_exits_to_guests(): void
    {
        $this->get('/empleos/999999')
            ->assertNotFound()
            ->assertSee('<html lang="es"', false)
            ->assertSee('No encontramos esta página')
            ->assertSee('href="/empleos"', false)
            ->assertSee('href="/login"', false)
            ->assertDontSee('href="/dashboard"', false)
            ->assertDontSee('Not Found');
    }

    public function test_not_found_page_offers_the_dashboard_to_signed_in_users(): void
    {
        $this->actingAs(User::factory()->candidate()->create())
            ->get('/empleos/999999')
            ->assertNotFound()
            ->assertSee('Ir a mi panel')
            ->assertSee('href="/dashboard"', false)
            ->assertDontSee('href="/login"', false);
    }

    public function test_a_vacancy_of_another_organization_is_denied_without_revealing_it(): void
    {
        $vacancyA = Vacancy::factory()
            ->for(Organization::factory())
            ->configured()
            ->create(['title' => 'Vacante reservada de la organización A']);
        $hrB = User::factory()->hr(Organization::factory()->create())->create();

        $response = $this->actingAs($hrB)->get(route('vacancies.show', $vacancyA));

        $this->assertContains($response->getStatusCode(), [403, 404]);
        $response->assertSee('<html lang="es"', false)
            ->assertDontSee('Vacante reservada de la organización A')
            ->assertDontSee($vacancyA->code);
    }

    public function test_forbidden_page_is_in_spanish_and_hides_the_exception_message(): void
    {
        $hr = User::factory()->hr(Organization::factory()->create())->create();

        $this->actingAs($hr)
            ->get(route('audit.index'))
            ->assertForbidden()
            ->assertSee('<html lang="es"', false)
            ->assertSee('No tiene permiso para ver esta página')
            ->assertSee('href="/dashboard"', false)
            ->assertDontSee('This action is unauthorized');
    }

    public function test_forbidden_page_never_prints_the_reason_given_by_the_application(): void
    {
        Route::middleware('web')->get('/__prueba/403', fn () => abort(403, 'Motivo interno de la política'));

        $this->get('/__prueba/403')
            ->assertForbidden()
            ->assertSee('No tiene permiso para ver esta página')
            ->assertSee('href="/login"', false)
            ->assertDontSee('Motivo interno de la política');
    }

    public function test_page_expired_is_in_spanish_and_keeps_status_419(): void
    {
        Route::middleware('web')->post('/__prueba/419', fn () => throw new TokenMismatchException('CSRF token mismatch.'));

        $this->post('/__prueba/419')
            ->assertStatus(419)
            ->assertSee('<html lang="es"', false)
            ->assertSee('La página expiró')
            ->assertSee('href="/login"', false)
            ->assertDontSee('Page Expired')
            ->assertDontSee('CSRF token mismatch');
    }

    public function test_page_expired_only_links_back_to_a_page_of_this_application(): void
    {
        Route::middleware('web')->post('/__prueba/419', fn () => throw new TokenMismatchException);

        $this->post('/__prueba/419', [], ['Referer' => 'https://sitio-externo.test/trampa'])
            ->assertStatus(419)
            ->assertDontSee('sitio-externo.test');

        $this->post('/__prueba/419', [], ['Referer' => url('/mi-perfil?seccion=cv')])
            ->assertStatus(419)
            ->assertSee('href="/mi-perfil?seccion=cv"', false);
    }

    public function test_page_expired_offers_the_dashboard_to_signed_in_users(): void
    {
        Route::middleware('web')->post('/__prueba/419', fn () => throw new TokenMismatchException);

        $this->actingAs(User::factory()->candidate()->create())
            ->post('/__prueba/419')
            ->assertStatus(419)
            ->assertSee('href="/dashboard"', false)
            ->assertDontSee('href="/login"', false);
    }

    public function test_json_clients_keep_receiving_json_errors_with_the_same_status(): void
    {
        $this->getJson('/empleos/999999')
            ->assertNotFound()
            ->assertHeader('content-type', 'application/json')
            ->assertJsonStructure(['message']);

        $hr = User::factory()->hr(Organization::factory()->create())->create();

        $this->actingAs($hr)
            ->getJson(route('audit.index'))
            ->assertForbidden()
            ->assertHeader('content-type', 'application/json')
            ->assertJsonStructure(['message']);
    }
}
