<?php

namespace Tests\Feature\Frontend;

use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Route;
use RuntimeException;
use Tests\TestCase;

/**
 * DEF-28: la página 500 en español no depende de la base de datos, la caché, la sesión ni de los assets de
 * Vite, así que se muestra aunque esos servicios fallen. Nunca muestra el detalle de la excepción.
 */
class ServerErrorPageTest extends TestCase
{
    protected function setUp(): void
    {
        parent::setUp();

        // En producción la depuración está apagada: es el caso en que Laravel usa la plantilla 500.
        config(['app.debug' => false]);
    }

    public function test_server_error_page_is_in_spanish_and_reveals_no_internal_detail(): void
    {
        Route::middleware('web')->get('/__prueba/500', fn () => throw new RuntimeException('detalle-interno-secreto'));

        $this->get('/__prueba/500')
            ->assertStatus(500)
            ->assertSee('<html lang="es"', false)
            ->assertSee('Algo falló de nuestro lado')
            ->assertSee('href="/"', false)
            ->assertDontSee('detalle-interno-secreto')
            ->assertDontSee('RuntimeException')
            ->assertDontSee('Server Error')
            ->assertDontSee('/build/', false);
    }

    public function test_server_error_page_renders_when_the_database_is_unavailable(): void
    {
        config([
            'database.connections.pgsql.host' => '127.0.0.1',
            'database.connections.pgsql.port' => 1,
        ]);
        DB::purge('pgsql');
        Route::middleware('web')->get('/__prueba/500-bd', fn () => DB::connection('pgsql')->select('select 1'));

        $this->get('/__prueba/500-bd')
            ->assertStatus(500)
            ->assertSee('Algo falló de nuestro lado')
            ->assertDontSee('SQLSTATE');
    }

    public function test_server_error_page_renders_when_the_cache_is_unavailable(): void
    {
        config([
            'cache.default' => 'redis',
            'database.redis.default.host' => '127.0.0.1',
            'database.redis.default.port' => 1,
            'database.redis.cache.host' => '127.0.0.1',
            'database.redis.cache.port' => 1,
        ]);
        Route::middleware('web')->get('/__prueba/500-cache', fn () => Cache::get('clave-de-prueba'));

        $this->get('/__prueba/500-cache')
            ->assertStatus(500)
            ->assertSee('Algo falló de nuestro lado');
    }
}
