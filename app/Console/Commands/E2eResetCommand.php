<?php

namespace App\Console\Commands;

use App\Services\Testing\E2eEnvironment;
use Illuminate\Console\Command;

class E2eResetCommand extends Command
{
    protected $signature = 'e2e:reset';

    protected $description = 'Restore the demo database to the known state used by the Cypress E2E suite (drops all data)';

    public function handle(E2eEnvironment $environment): int
    {
        if ($this->laravel->isProduction()) {
            $this->error('e2e:reset no está permitido en producción.');

            return self::FAILURE;
        }

        $environment->reset();
        $this->info('Base de datos restablecida con los datos de demostración.');

        return self::SUCCESS;
    }
}
