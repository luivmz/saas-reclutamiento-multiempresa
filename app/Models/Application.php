<?php

namespace App\Models;

use App\Enums\ApplicationStatus;
use App\Models\Concerns\BelongsToOrganization;
use Database\Factories\ApplicationFactory;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Support\Carbon;

/**
 * @property int $id
 * @property int $organization_id
 * @property int $vacancy_id
 * @property int $candidate_id
 * @property int|null $candidate_document_id
 * @property ApplicationStatus $status
 * @property Carbon $applied_at
 * @property Carbon|null $stage_changed_at
 * @property-read Vacancy $vacancy
 * @property-read User $candidate
 * @property-read CandidateDocument|null $cvDocument
 */
class Application extends Model
{
    /** @use HasFactory<ApplicationFactory> */
    use BelongsToOrganization, HasFactory;

    protected function casts(): array
    {
        return [
            'status' => ApplicationStatus::class,
            'applied_at' => 'datetime',
            'stage_changed_at' => 'datetime',
        ];
    }

    public function trackingCode(): string
    {
        return 'POS-'.str_pad((string) $this->id, 5, '0', STR_PAD_LEFT);
    }

    /**
     * @return BelongsTo<Vacancy, $this>
     */
    public function vacancy(): BelongsTo
    {
        return $this->belongsTo(Vacancy::class);
    }

    /**
     * @return BelongsTo<User, $this>
     */
    public function candidate(): BelongsTo
    {
        return $this->belongsTo(User::class, 'candidate_id');
    }

    /**
     * @return BelongsTo<CandidateDocument, $this>
     */
    public function cvDocument(): BelongsTo
    {
        return $this->belongsTo(CandidateDocument::class, 'candidate_document_id');
    }

    /**
     * @return HasMany<ApplicationStageHistory, $this>
     */
    public function stageHistories(): HasMany
    {
        return $this->hasMany(ApplicationStageHistory::class);
    }
}
