<?php

namespace App\Services\Candidates;

use App\Enums\AuditAction;
use App\Enums\DocumentType;
use App\Models\CandidateDocument;
use App\Models\CandidateProfile;
use App\Models\User;
use App\Services\Audit\AuditLogger;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;
use RuntimeException;
use Throwable;

/**
 * RF-09: candidate profile and CV.
 */
class CandidateProfileService
{
    private const DISK = 'local';

    public function __construct(private readonly AuditLogger $audit) {}

    /**
     * @param  array<string, mixed>  $data
     */
    public function update(User $candidate, array $data): CandidateProfile
    {
        return DB::transaction(function () use ($candidate, $data): CandidateProfile {
            $profile = $this->profileFor($candidate);
            $profile->fill($data);
            $changedFields = array_values(array_diff(array_keys($profile->getDirty()), ['user_id']));
            $profile->save();

            $this->audit->record(AuditAction::CandidateProfileUpdated, $profile, ['fields' => $changedFields], $candidate);

            return $profile;
        });
    }

    public function storeCv(User $candidate, UploadedFile $file): CandidateDocument
    {
        $path = $file->storeAs('cvs/'.$candidate->id, Str::uuid()->toString().'.pdf', self::DISK);

        if ($path === false) {
            throw new RuntimeException('No se pudo almacenar el CV.');
        }

        try {
            return DB::transaction(function () use ($candidate, $file, $path): CandidateDocument {
                $profile = $this->profileFor($candidate);
                $profile->save();

                $document = new CandidateDocument;
                $document->forceFill([
                    'candidate_profile_id' => $profile->id,
                    'type' => DocumentType::Cv,
                    'original_name' => Str::limit($file->getClientOriginalName(), 250, ''),
                    'stored_path' => $path,
                    'mime_type' => $file->getMimeType() ?? 'application/pdf',
                    'size_bytes' => $file->getSize(),
                ])->save();

                $this->audit->record(AuditAction::CandidateCvUploaded, $document, [
                    'size_kb' => (int) ceil($document->size_bytes / 1024),
                    'mime_type' => $document->mime_type,
                ], $candidate);

                return $document;
            });
        } catch (Throwable $exception) {
            Storage::disk(self::DISK)->delete($path);

            throw $exception;
        }
    }

    private function profileFor(User $candidate): CandidateProfile
    {
        $profile = CandidateProfile::query()->where('user_id', $candidate->id)->first() ?? new CandidateProfile;
        $profile->user_id = $candidate->id;

        return $profile;
    }
}
