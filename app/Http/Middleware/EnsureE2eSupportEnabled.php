<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

/**
 * The E2E endpoints behave as non-existent unless explicitly enabled outside production, and require the shared token.
 */
class EnsureE2eSupportEnabled
{
    public function handle(Request $request, Closure $next): Response
    {
        abort_unless(config('e2e.enabled') && ! app()->isProduction(), 404);

        $token = (string) config('e2e.token');

        abort_if($token === '' || ! hash_equals($token, (string) $request->header('X-E2E-Token')), 403);

        return $next($request);
    }
}
