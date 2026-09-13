<?php

namespace App\Console\Commands;

use App\Services\Testing\E2eEnvironment;
use Illuminate\Console\Command;

class E2eResetCommand extends Command
{
    protected $signature = 'e2e:reset';

    protected $description = 'Restore the dedicated E2E database to the known demo state used by the Cypress suite (drops all data)';

    public function handle(E2eEnvironment $environment): int
    {
        if ($this->laravel->isProduction()) {
            $this->error('e2e:reset no está permitido en producción.');

            return self::FAILURE;
        }

        if (! $environment->usesE2eDatabase()) {
            $this->error('e2e:reset rechazado: la base activa no es la base E2E configurada (E2E_DATABASE). Use el servicio app-e2e.');

            return self::FAILURE;
        }

        $environment->reset();
        $this->info('Base de datos E2E restablecida con los datos de demostración.');

        return self::SUCCESS;
    }
}
