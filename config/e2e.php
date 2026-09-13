<?php

return [

    /*
    |--------------------------------------------------------------------------
    | End-to-end test support
    |--------------------------------------------------------------------------
    |
    | Enables the `/__e2e/*` endpoints used by the Cypress suite to reset the demo database to a known state
    | and to wait for queued notifications. Disabled by default and never available in production. Every
    | request must carry the token in the `X-E2E-Token` header. See docs/testing/cypress-e2e.md.
    |
    */

    'enabled' => (bool) env('E2E_ENABLED', false),

    'token' => env('E2E_TOKEN'),

];
