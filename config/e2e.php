<?php

return [

    /*
    |--------------------------------------------------------------------------
    | End-to-end test support
    |--------------------------------------------------------------------------
    |
    | Enables the `/__e2e/*` endpoints used by the Cypress suite to reset the E2E database to a known state and
    | to wait for queued notifications. Disabled by default, never available in production, and only enabled in
    | the isolated E2E environment (.env.e2e, APP_ENV=e2e). Every request must carry the token in the
    | `X-E2E-Token` header. See docs/testing/cypress-e2e.md and docs/docker.md.
    |
    */

    'enabled' => (bool) env('E2E_ENABLED', false),

    'token' => env('E2E_TOKEN'),

    // The destructive reset refuses to run unless the active database is exactly this one.
    'database' => env('E2E_DATABASE', 'reclutamiento_e2e'),

];
