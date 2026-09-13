<?php

namespace Database\Factories;

use App\Models\Organization;
use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Str;

/**
 * @extends Factory<Organization>
 */
class OrganizationFactory extends Factory
{
    public function definition(): array
    {
        $name = 'Organización Demo '.fake()->unique()->numberBetween(1, 999999);

        return [
            'name' => $name,
            'slug' => Str::slug($name),
            'tax_id' => '20'.fake()->unique()->numerify('#########'),
            'is_active' => true,
        ];
    }
}
