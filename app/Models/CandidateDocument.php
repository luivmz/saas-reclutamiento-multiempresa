<?php

namespace App\Models;

use App\Enums\DocumentType;
use Database\Factories\CandidateDocumentFactory;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Support\Carbon;

/**
 * @property int $id
 * @property int $candidate_profile_id
 * @property DocumentType $type
 * @property string $original_name
 * @property string $stored_path
 * @property string $mime_type
 * @property int $size_bytes
 * @property Carbon $created_at
 * @property-read CandidateProfile $profile
 */
class CandidateDocument extends Model
{
    /** @use HasFactory<CandidateDocumentFactory> */
    use HasFactory;

    protected function casts(): array
    {
        return [
            'type' => DocumentType::class,
            'size_bytes' => 'integer',
        ];
    }

    /**
     * Public-safe summary: never exposes the storage path.
     *
     * @return array{id: int, original_name: string, size_bytes: int, uploaded_at: string, download_url: string}
     */
    public function toSummary(): array
    {
        return [
            'id' => $this->id,
            'original_name' => $this->original_name,
            'size_bytes' => $this->size_bytes,
            'uploaded_at' => $this->created_at->toIso8601String(),
            'download_url' => route('documents.download', $this, absolute: false),
        ];
    }

    /**
     * @return BelongsTo<CandidateProfile, $this>
     */
    public function profile(): BelongsTo
    {
        return $this->belongsTo(CandidateProfile::class, 'candidate_profile_id');
    }
}
