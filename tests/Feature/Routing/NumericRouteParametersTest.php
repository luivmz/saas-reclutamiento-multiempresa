<?php

namespace Tests\Feature\Routing;

use App\Models\Organization;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

/**
 * Fase 25 (QA global, F25-M01): un identificador que no es numérico no debe llegar a
 * PostgreSQL. Antes, `/requerimientos/create` o `/vacantes/abc` hacían una consulta
 * `where id = 'abc'` sobre una columna `bigint` y respondían 500 (SQLSTATE 22P02).
 * Un recurso que no existe responde 404.
 */
class NumericRouteParametersTest extends TestCase
{
    use RefreshDatabase;

    public function test_non_numeric_identifiers_respond_not_found_instead_of_a_server_error(): void
    {
        $organization = Organization::factory()->create();
        $hr = User::factory()->hr($organization)->create();

        foreach ([
            '/requerimientos/create',
            '/requerimientos/abc',
            '/requerimientos/abc/editar',
            '/vacantes/abc',
            '/vacantes/abc/postulaciones',
            '/vacantes/abc/comparacion',
            '/vacantes/abc/riesgo-operacional',
            '/postulaciones/abc',
            '/documentos/abc/descargar',
        ] as $uri) {
            $this->actingAs($hr)->get($uri)->assertNotFound();
        }

        $evaluator = User::factory()->evaluator($organization)->create();
        $this->actingAs($evaluator)->get('/evaluaciones/abc')->assertNotFound();
        $this->actingAs($evaluator)->get('/entrevistas/abc')->assertNotFound();

        $candidate = User::factory()->candidate()->create();
        $this->actingAs($candidate)->get('/mis-postulaciones/abc')->assertNotFound();
    }

    public function test_the_localized_create_route_still_works(): void
    {
        $organization = Organization::factory()->create();

        $this->actingAs(User::factory()->requester($organization)->create())
            ->get('/requerimientos/crear')
            ->assertOk();

        $this->actingAs(User::factory()->hr($organization)->create())
            ->get('/vacantes/crear')
            ->assertOk();
    }
}
