<?php

namespace App\Http\Controllers\Testing;

use App\Http\Controllers\Controller;
use App\Services\Testing\E2eEnvironment;
use Illuminate\Http\JsonResponse;

/**
 * Support endpoints for the Cypress suite (see EnsureE2eSupportEnabled and docs/testing/cypress-e2e.md).
 */
class E2eController extends Controller
{
    public function reset(E2eEnvironment $environment): JsonResponse
    {
        if (! $environment->usesE2eDatabase()) {
            return response()->json([
                'reset' => false,
                'message' => 'La base de datos activa no es la base E2E configurada (E2E_DATABASE).',
            ], 409);
        }

        $environment->reset();

        return response()->json(['reset' => true]);
    }

    public function queue(E2eEnvironment $environment): JsonResponse
    {
        return response()->json(['pending' => $environment->pendingJobs()]);
    }
}
