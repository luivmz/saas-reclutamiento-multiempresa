<?php

namespace App\Models;

use App\Enums\AssessmentStatus;
use App\Enums\InterviewOutcome;
use App\Enums\Modality;
use App\Models\Concerns\BelongsToOrganization;
use Database\Factories\InterviewFactory;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Support\Carbon;

/**
 * RF-18 and RF-19.
 *
 * @property int $id
 * @property int $organization_id
 * @property int $application_id
 * @property int $evaluator_id
 * @property int $scheduled_by
 * @property Modality $modality
 * @property string $location
 * @property Carbon $scheduled_at
 * @property int|null $duration_minutes
 * @property string|null $instructions
 * @property AssessmentStatus $status
 * @property InterviewOutcome|null $outcome
 * @property Carbon|null $invitation_sent_at
 * @property Carbon|null $completed_at
 * @property string|null $observations
 * @property-read Application $application
 * @property-read User $evaluator
 */
class Interview extends Model
{
    /** @use HasFactory<InterviewFactory> */
    use BelongsToOrganization, HasFactory;

    protected function casts(): array
    {
        return [
            'modality' => Modality::class,
            'status' => AssessmentStatus::class,
            'outcome' => InterviewOutcome::class,
            'scheduled_at' => 'datetime',
            'invitation_sent_at' => 'datetime',
            'completed_at' => 'datetime',
            'duration_minutes' => 'integer',
        ];
    }

    /**
     * @return BelongsTo<Application, $this>
     */
    public function application(): BelongsTo
    {
        return $this->belongsTo(Application::class);
    }

    /**
     * @return BelongsTo<User, $this>
     */
    public function evaluator(): BelongsTo
    {
        return $this->belongsTo(User::class, 'evaluator_id');
    }

    /**
     * @return HasMany<InterviewResult, $this>
     */
    public function results(): HasMany
    {
        return $this->hasMany(InterviewResult::class);
    }
}
