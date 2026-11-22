<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

/**
 * Inert unless the experimental capability is enabled (config/experimental.php). Disabled, the routes answer
 * 404, as if they did not exist.
 */
class EnsureExperimentalFeature
{
    public function handle(Request $request, Closure $next, string $feature): Response
    {
        abort_unless(config("experimental.{$feature}") === true, 404);

        return $next($request);
    }
}
