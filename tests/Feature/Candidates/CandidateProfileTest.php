<?php

namespace Tests\Feature\Candidates;

use App\Enums\AuditAction;
use App\Models\Application;
use App\Models\AuditLog;
use App\Models\CandidateDocument;
use App\Models\CandidateProfile;
use App\Models\Organization;
use App\Models\User;
use App\Models\Vacancy;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;
use Tests\TestCase;

class CandidateProfileTest extends TestCase
{
    use RefreshDatabase;

    /**
     * @return array<string, mixed>
     */
    private function payload(array $overrides = []): array
    {
        return array_merge([
            'phone' => '964000111',
            'city' => 'Huancayo',
            'education_level' => 'titulado',
            'professional_title' => 'Licenciado en Educación',
            'years_of_experience' => 3,
            'summary' => 'Docente con experiencia ficticia en educación secundaria.',
        ], $overrides);
    }

    public function test_rf09_candidate_updates_profile(): void
    {
        $candidate = User::factory()->candidate()->create();

        $this->actingAs($candidate)
            ->put(route('candidate.profile.update'), $this->payload())
            ->assertSessionHasNoErrors();

        $profile = CandidateProfile::query()->where('user_id', $candidate->id)->sole();
        $this->assertSame('964000111', $profile->phone);
        $this->assertSame(3, $profile->years_of_experience);
        $this->assertTrue(AuditLog::query()->where('action', AuditAction::CandidateProfileUpdated)->exists());
    }

    public function test_rf09_profile_fields_are_validated(): void
    {
        $candidate = User::factory()->candidate()->create();

        $this->actingAs($candidate)
            ->put(route('candidate.profile.update'), $this->payload([
                'years_of_experience' => -1,
                'education_level' => 'inventado',
                'phone' => 'abc',
            ]))
            ->assertSessionHasErrors(['years_of_experience', 'education_level', 'phone']);
    }

    public function test_rf09_cv_is_stored_privately_with_a_safe_generated_name(): void
    {
        $candidate = User::factory()->candidate()->create();

        $this->actingAs($candidate)
            ->post(route('candidate.cv.store'), ['cv' => UploadedFile::fake()->create('Mi CV Final (1).pdf', 300, 'application/pdf')])
            ->assertSessionHasNoErrors();

        $document = CandidateDocument::query()->sole();
        $this->assertSame('Mi CV Final (1).pdf', $document->original_name);
        $this->assertMatchesRegularExpression('#^cvs/\d+/[0-9a-f-]{36}\.pdf$#', $document->stored_path);
        $this->assertSame('application/pdf', $document->mime_type);
        $this->assertSame(300 * 1024, $document->size_bytes);
        Storage::disk('local')->assertExists($document->stored_path);
        Storage::disk('public')->assertMissing($document->stored_path);

        $log = AuditLog::query()->where('action', AuditAction::CandidateCvUploaded)->sole();
        $this->assertArrayNotHasKey('stored_path', $log->metadata);
    }

    public function test_rf09_cv_rejects_invalid_type_and_oversized_files(): void
    {
        $candidate = User::factory()->candidate()->create();

        $this->actingAs($candidate)
            ->post(route('candidate.cv.store'), ['cv' => UploadedFile::fake()->create('virus.exe', 100, 'application/x-msdownload')])
            ->assertSessionHasErrors('cv');

        $this->actingAs($candidate)
            ->post(route('candidate.cv.store'), ['cv' => UploadedFile::fake()->create('cv.pdf', 6000, 'application/pdf')])
            ->assertSessionHasErrors('cv');

        $this->assertSame(0, CandidateDocument::query()->count());
    }

    public function test_rf09_staff_cannot_use_candidate_profile_routes(): void
    {
        $hr = User::factory()->hr(Organization::factory()->create())->create();

        $this->actingAs($hr)->get(route('candidate.profile.edit'))->assertForbidden();
        $this->actingAs($hr)->put(route('candidate.profile.update'), $this->payload())->assertForbidden();
    }

    public function test_cv_download_is_restricted_to_owner_and_organizations_where_candidate_applied(): void
    {
        $orgA = Organization::factory()->create();
        $orgB = Organization::factory()->create();
        $candidate = User::factory()->candidate()->has(CandidateProfile::factory()->withCv(), 'candidateProfile')->create();
        $document = $candidate->candidateProfile->documents()->sole();
        $vacancy = Vacancy::factory()->for($orgA)->configured()->published()->create();
        Application::factory()->for($vacancy)->forCandidate($candidate)->create();

        $this->actingAs($candidate)->get(route('documents.download', $document))->assertOk();
        $this->actingAs(User::factory()->hr($orgA)->create())->get(route('documents.download', $document))->assertOk();
        $this->actingAs(User::factory()->hr($orgB)->create())->get(route('documents.download', $document))->assertForbidden();
        $this->actingAs(User::factory()->candidate()->create())->get(route('documents.download', $document))->assertForbidden();
    }
}
