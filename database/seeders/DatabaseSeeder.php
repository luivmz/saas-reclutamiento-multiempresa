<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    /**
     * Seed the application's database with fictitious demo data (see docs/demo-users.md).
     */
    public function run(): void
    {
        $this->call(DemoSeeder::class);
    }
}
