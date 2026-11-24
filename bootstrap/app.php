<?php

use App\Http\Controllers\HealthController;
use App\Http\Controllers\Testing\E2eController;
use App\Http\Middleware\EnsureE2eSupportEnabled;
use App\Http\Middleware\EnsureExperimentalFeature;
use App\Http\Middleware\EnsureUserHasRole;
use App\Http\Middleware\HandleAppearance;
use App\Http\Middleware\HandleInertiaRequests;
use Illuminate\Foundation\Application;
use Illuminate\Foundation\Configuration\Exceptions;
use Illuminate\Foundation\Configuration\Middleware;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Middleware\AddLinkHeadersForPreloadedAssets;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use Inertia\Inertia;
use Symfony\Component\HttpFoundation\Response;

return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        web: __DIR__.'/../routes/web.php',
        commands: __DIR__.'/../routes/console.php',
        health: '/up',
        then: function (): void {
            Route::get('health', HealthController::class)->name('health');

            // Cypress support, outside the web group (no session/CSRF); inert unless enabled (see config/e2e.php).
            Route::prefix('__e2e')->middleware(EnsureE2eSupportEnabled::class)->group(function (): void {
                Route::post('reset', [E2eController::class, 'reset']);
                Route::get('queue', [E2eController::class, 'queue']);
            });
        },
    )
    ->withMiddleware(function (Middleware $middleware): void {
        // TrustProxies reads trustedproxy.proxies when handling the request, after configuration is loaded.
        $middleware->trustProxies(headers: Request::HEADER_X_FORWARDED_PROTO);

        $middleware->encryptCookies(except: ['appearance', 'sidebar_state']);

        $middleware->alias([
            'role' => EnsureUserHasRole::class,
            'experimental' => EnsureExperimentalFeature::class,
        ]);

        $middleware->web(append: [
            HandleAppearance::class,
            HandleInertiaRequests::class,
            AddLinkHeadersForPreloadedAssets::class,
        ]);
    })
    ->withExceptions(function (Exceptions $exceptions): void {
        $exceptions->shouldRenderJsonWhen(
            fn (Request $request) => $request->is('api/*') || $request->expectsJson(),
        );

        // DEF-28: en una visita interna de Inertia, un 403 o 404 en HTML se abría en la ventana modal de Inertia.
        // Se responde con una página Inertia y el mismo código. Las cargas completas siguen con las vistas Blade,
        // el JSON no cambia y el 500 conserva su vista autónoma, que no depende de base, sesión ni caché.
        $exceptions->respond(function (Response $response, Throwable $e, Request $request): Response {
            if ($request->header('X-Inertia') && ! $response instanceof JsonResponse
                && in_array($response->getStatusCode(), [403, 404], true)) {
                return Inertia::render('errors/http', ['status' => $response->getStatusCode()])
                    ->toResponse($request)
                    ->setStatusCode($response->getStatusCode());
            }

            return $response;
        });
    })->create();
