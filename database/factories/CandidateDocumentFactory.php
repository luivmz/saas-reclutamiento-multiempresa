<?php

namespace Database\Factories;

use App\Enums\DocumentType;
use App\Models\CandidateDocument;
use App\Models\CandidateProfile;
use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;

/**
 * @extends Factory<CandidateDocument>
 */
class CandidateDocumentFactory extends Factory
{
    public function definition(): array
    {
        return [
            'candidate_profile_id' => CandidateProfile::factory(),
            'type' => DocumentType::Cv,
            'original_name' => 'cv-ficticio.pdf',
            'stored_path' => fn () => 'cvs/demo/'.Str::uuid()->toString().'.pdf',
            'mime_type' => 'application/pdf',
            'size_bytes' => 2048,
        ];
    }

    public function configure(): static
    {
        return $this->afterCreating(function (CandidateDocument $document): void {
            Storage::disk('local')->put($document->stored_path, "%PDF-1.4\n% Documento ficticio de demostración\n");
        });
    }
}
