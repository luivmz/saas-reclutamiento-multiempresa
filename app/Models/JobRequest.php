<?php

namespace App\Models;

use App\Enums\ContractType;
use App\Enums\JobRequestStatus;
use App\Models\Concerns\BelongsToOrganization;
use Database\Factories\JobRequestFactory;
use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\Relations\HasOne;
use Illuminate\Support\Carbon;

/**
 * @property int $id
 * @property int $organization_id
 * @property int $requested_by
 * @property string $code
 * @property string $position_title
 * @property string $area
 * @property int $headcount
 * @property ContractType $contract_type
 * @property string $justification
 * @property Carbon|null $required_by
 * @property JobRequestStatus $status
 * @property string|null $observation
 * @property Carbon|null $submitted_at
 * @property int|null $validated_by
 * @property Carbon|null $validated_at
 * @property int|null $decided_by
 * @property Carbon|null $decided_at
 * @property string|null $decision_comment
 * @property Carbon $created_at
 * @property-read User $requester
 * @property-read Vacancy|null $vacancy
 */
#[Fillable(['position_title', 'area', 'headcount', 'contract_type', 'justification', 'required_by'])]
class JobRequest extends Model
{
    /** @use HasFactory<JobRequestFactory> */
    use BelongsToOrganization, HasFactory;

    protected function casts(): array
    {
        return [
            'status' => JobRequestStatus::class,
            'contract_type' => ContractType::class,
            'headcount' => 'integer',
            'required_by' => 'date',
            'submitted_at' => 'datetime',
            'validated_at' => 'datetime',
            'decided_at' => 'datetime',
        ];
    }

    /**
     * @return BelongsTo<User, $this>
     */
    public function requester(): BelongsTo
    {
        return $this->belongsTo(User::class, 'requested_by');
    }

    /**
     * @return BelongsTo<User, $this>
     */
    public function validator(): BelongsTo
    {
        return $this->belongsTo(User::class, 'validated_by');
    }

    /**
     * @return BelongsTo<User, $this>
     */
    public function decider(): BelongsTo
    {
        return $this->belongsTo(User::class, 'decided_by');
    }

    /**
     * @return HasMany<JobRequestStatusHistory, $this>
     */
    public function statusHistories(): HasMany
    {
        return $this->hasMany(JobRequestStatusHistory::class);
    }

    /**
     * @return HasOne<Vacancy, $this>
     */
    public function vacancy(): HasOne
    {
        return $this->hasOne(Vacancy::class);
    }
}
