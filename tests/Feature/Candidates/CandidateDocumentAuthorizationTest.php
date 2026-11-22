<?php

namespace Tests\Feature\Candidates;

use App\Models\Application;
use App\Models\CandidateDocument;
use App\Models\CandidateProfile;
use App\Models\Evaluation;
use App\Models\Interview;
use App\Models\Organization;
use App\Models\User;
use App\Models\Vacancy;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Storage;
use Illuminate\Testing\TestResponse;
use Tests\TestCase;

/**
 * SEG-03: a CV version is downloadable by staff only through an application of their organization that presented
 * exactly that document (A-04, A-11, A-12), and by an evaluator only through a session assigned to them on such an
 * application. Real HTTP requests to documents.download, with every version stored on the (fake) private disk, so a
 * denial is never confused with a missing file.
 */
class CandidateDocumentAuthorizationTest extends TestCase
{
    use RefreshDatabase;

    private Organization $orgA;

    private Organization $orgB;

    private User $candidate;

    private CandidateProfile $profile;

    /** Never presented, older than every application. */
    private CandidateDocument $oldCv;

    /** Presented only to organization A. */
    private CandidateDocument $cvForA;

    /** Presented only to organization B. */
    private CandidateDocument $cvForB;

    /** Uploaded after every application, never presented. */
    private CandidateDocument $newCv;

    private Application $applicationA;

    private Application $applicationB;

    /** @var array<int, string> file contents by document id */
    private array $contents = [];

    protected function setUp(): void
    {
        parent::setUp();

        $this->orgA = Organization::factory()->create();
        $this->orgB = Organization::factory()->create();
        $this->candidate = User::factory()->candidate()->has(CandidateProfile::factory(), 'candidateProfile')->create();
        $this->profile = $this->candidate->candidateProfile;

        $this->oldCv = $this->version('ANTIGUA-NO-PRESENTADA');
        $this->cvForA = $this->version('PRESENTADA-A');
        $this->cvForB = $this->version('PRESENTADA-B');
        $this->applicationA = $this->applyWith($this->orgA, $this->cvForA);
        $this->applicationB = $this->applyWith($this->orgB, $this->cvForB);
        $this->newCv = $this->version('NUEVA-NO-PRESENTADA');
    }

    public function test_rf09_seg03_owner_downloads_every_version_of_their_cv(): void
    {
        foreach ([$this->oldCv, $this->cvForA, $this->cvForB, $this->newCv] as $document) {
            $this->assertDownloads($this->candidate, $document);
        }
    }

    public function test_rf09_seg03_another_candidate_downloads_none(): void
    {
        $stranger = User::factory()->candidate()->has(CandidateProfile::factory()->withCv(), 'candidateProfile')->create();

        foreach ([$this->oldCv, $this->cvForA, $this->cvForB, $this->newCv] as $document) {
            $this->assertDenied($stranger, $document, 'otro candidato');
        }
    }

    public function test_rf09_seg03_hr_and_approver_download_only_the_cv_presented_to_their_organization(): void
    {
        foreach ([User::factory()->hr($this->orgA)->create(), User::factory()->approver($this->orgA)->create()] as $staffA) {
            $this->assertDownloads($staffA, $this->cvForA);
            $this->assertDenied($staffA, $this->cvForB, 'personal de A, versión presentada solo a B');
            $this->assertDenied($staffA, $this->oldCv, 'personal de A, versión antigua no presentada');
            $this->assertDenied($staffA, $this->newCv, 'personal de A, versión nueva no presentada');
        }

        foreach ([User::factory()->hr($this->orgB)->create(), User::factory()->approver($this->orgB)->create()] as $staffB) {
            $this->assertDownloads($staffB, $this->cvForB);
            $this->assertDenied($staffB, $this->cvForA, 'personal de B, versión presentada solo a A');
            $this->assertDenied($staffB, $this->oldCv, 'personal de B, versión antigua no presentada');
            $this->assertDenied($staffB, $this->newCv, 'personal de B, versión nueva no presentada');
        }
    }

    public function test_rf09_seg03_a_cv_presented_to_both_organizations_stays_available_to_both(): void
    {
        $shared = $this->version('PRESENTADA-A-Y-B');
        $this->applyWith($this->orgA, $shared);
        $this->applyWith($this->orgB, $shared);

        foreach ([User::factory()->hr($this->orgA)->create(), User::factory()->approver($this->orgB)->create()] as $staff) {
            $this->assertDownloads($staff, $shared);
            $this->assertDenied($staff, $this->newCv, 'versión nueva no presentada');
        }
    }

    public function test_rf09_seg03_assigned_evaluators_download_only_the_cv_of_their_application(): void
    {
        $evaluator = User::factory()->evaluator($this->orgA)->create();
        $interviewer = User::factory()->evaluator($this->orgA)->create();
        Evaluation::factory()->forApplication($this->applicationA)->assignedTo($evaluator)->create();
        Interview::factory()->forApplication($this->applicationA)->assignedTo($interviewer)->create();

        // A second application of the same candidate in A, with another CV and another evaluator.
        $cvForA2 = $this->version('PRESENTADA-A-OTRA-VACANTE');
        $applicationA2 = $this->applyWith($this->orgA, $cvForA2);
        $evaluatorA2 = User::factory()->evaluator($this->orgA)->create();
        Evaluation::factory()->forApplication($applicationA2)->assignedTo($evaluatorA2)->create();

        $evaluatorB = User::factory()->evaluator($this->orgB)->create();
        Interview::factory()->forApplication($this->applicationB)->assignedTo($evaluatorB)->create();

        foreach ([$evaluator, $interviewer] as $assigned) {
            $this->assertDownloads($assigned, $this->cvForA);
            $this->assertDenied($assigned, $cvForA2, 'evaluador de A, CV de otra postulación del mismo candidato');
            $this->assertDenied($assigned, $this->cvForB, 'evaluador de A, versión presentada solo a B');
            $this->assertDenied($assigned, $this->oldCv, 'evaluador de A, versión antigua no presentada');
            $this->assertDenied($assigned, $this->newCv, 'evaluador de A, versión nueva no presentada');
        }

        $this->assertDownloads($evaluatorA2, $cvForA2);
        $this->assertDenied($evaluatorA2, $this->cvForA, 'evaluador asignado a otra postulación del mismo candidato');

        $this->assertDownloads($evaluatorB, $this->cvForB);
        $this->assertDenied($evaluatorB, $this->cvForA, 'evaluador de B, versión presentada solo a A');
    }

    public function test_rf09_seg03_unassigned_evaluator_requester_and_guest_get_nothing(): void
    {
        // The guest request goes first: actingAs() keeps the user authenticated for the rest of the test.
        $guest = $this->get(route('documents.download', $this->cvForA));
        $guest->assertRedirect(route('login'));
        $this->assertStringNotContainsString($this->contents[$this->cvForA->id], (string) $guest->getContent());

        $this->assertDenied(User::factory()->evaluator($this->orgA)->create(), $this->cvForA, 'evaluador no asignado');
        $this->assertDenied(User::factory()->requester($this->orgA)->create(), $this->cvForA, 'solicitante');
    }

    public function test_rf09_seg03_an_application_without_a_cv_grants_no_fallback(): void
    {
        $orgC = Organization::factory()->create();
        $withoutCv = $this->applyWith($orgC, null);
        $evaluatorC = User::factory()->evaluator($orgC)->create();
        Evaluation::factory()->forApplication($withoutCv)->assignedTo($evaluatorC)->create();

        foreach ([User::factory()->hr($orgC)->create(), User::factory()->approver($orgC)->create(), $evaluatorC] as $user) {
            foreach ([$this->oldCv, $this->cvForA, $this->cvForB, $this->newCv] as $document) {
                $this->assertDenied($user, $document, 'organización con una postulación sin CV referenciado');
            }
        }
    }

    private function version(string $label): CandidateDocument
    {
        $document = CandidateDocument::factory()->create([
            'candidate_profile_id' => $this->profile->id,
            'original_name' => 'cv-seg03-'.strtolower($label).'.pdf',
        ]);

        $this->contents[$document->id] = "%PDF-1.4\n% SEG03-{$label} documento ficticio\n";
        Storage::disk('local')->put($document->stored_path, $this->contents[$document->id]);

        return $document;
    }

    private function applyWith(Organization $organization, ?CandidateDocument $document): Application
    {
        $vacancy = Vacancy::factory()->for($organization)->configured()->published()->create();

        return Application::factory()->for($vacancy)->forCandidate($this->candidate)->inEvaluation()
            ->state(['candidate_document_id' => $document?->id])
            ->create();
    }

    private function download(User $user, CandidateDocument $document): TestResponse
    {
        return $this->actingAs($user)->get(route('documents.download', $document));
    }

    private function assertDownloads(User $user, CandidateDocument $document): void
    {
        $response = $this->download($user, $document);

        $response->assertOk();
        $this->assertSame($this->contents[$document->id], $response->streamedContent());
        $this->assertStringContainsString($document->original_name, (string) $response->headers->get('Content-Disposition'));
    }

    private function assertDenied(User $user, CandidateDocument $document, string $case): void
    {
        $this->assertTrue(Storage::disk('local')->exists($document->stored_path), "El archivo de prueba debe existir: {$case}.");

        $response = $this->download($user, $document);
        $body = (string) $response->getContent();

        $this->assertSame(403, $response->getStatusCode(), "SEG-03: acceso indebido al CV ({$case}).");
        $this->assertStringNotContainsString($this->contents[$document->id], $body, "SEG-03: bytes del CV en una respuesta denegada ({$case}).");
        $this->assertStringNotContainsString($document->stored_path, $body, "SEG-03: ruta privada en una respuesta denegada ({$case}).");
        $this->assertStringNotContainsString($document->original_name, $body, "SEG-03: nombre del archivo en una respuesta denegada ({$case}).");
        $this->assertFalse($response->headers->has('Content-Disposition'), "SEG-03: cabecera de descarga en una respuesta denegada ({$case}).");
    }
}
