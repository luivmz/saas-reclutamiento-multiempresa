<?php

namespace App\Models;

use App\Enums\ContractType;
use App\Enums\VacancyClosureType;
use App\Enums\VacancyStatus;
use App\Models\Concerns\BelongsToOrganization;
use Carbon\CarbonInterface;
use Database\Factories\VacancyFactory;
use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\Relations\HasOne;
use Illuminate\Support\Carbon;

/**
 * @property int $id
 * @property int $organization_id
 * @property int $job_request_id
 * @property string $code
 * @property string $title
 * @property string $summary
 * @property string $location
 * @property ContractType $contract_type
 * @property int $positions
 * @property Carbon|null $opens_at
 * @property Carbon|null $closes_at
 * @property Carbon|null $target_completion_at
 * @property VacancyStatus $status
 * @property int $created_by
 * @property int|null $published_by
 * @property Carbon|null $published_at
 * @property int|null $closed_by
 * @property Carbon|null $closed_at
 * @property VacancyClosureType|null $closure_type
 * @property string|null $closure_notes
 * @property-read JobRequest $jobRequest
 * @property-read JobProfile|null $profile
 * @property-read \Illuminate\Database\Eloquent\Collection<int, EvaluationCriterion> $criteria
 */
#[Fillable(['title', 'summary', 'location', 'contract_type', 'positions', 'opens_at', 'closes_at', 'target_completion_at'])]
class Vacancy extends Model
{
    /** @use HasFactory<VacancyFactory> */
    use BelongsToOrganization, HasFactory;

    protected function casts(): array
    {
        return [
            'status' => VacancyStatus::class,
            'contract_type' => ContractType::class,
            'closure_type' => VacancyClosureType::class,
            'positions' => 'integer',
            'opens_at' => 'date',
            'closes_at' => 'date',
            'target_completion_at' => 'datetime',
            'published_at' => 'datetime',
            'closed_at' => 'datetime',
        ];
    }

    /**
     * GAP-01: el plazo objetivo solo puede fijarse o cambiarse en borrador.
     *
     * Congelarlo al publicar es lo que hace utilizable a `ML-FEAT-02`: si el
     * plazo pudiera moverse durante el proceso, la feature filtraría
     * información del desenlace -- se correría la meta cada vez que el proceso
     * se retrasara -- y el contrato de features la prohibiría.
     */
    public function targetCompletionIsEditable(): bool
    {
        return $this->status === VacancyStatus::Draft;
    }

    /**
     * @param  Builder<self>  $query
     */
    public function scopePublished(Builder $query): void
    {
        $query->where('status', VacancyStatus::Published);
    }

    public function acceptsApplications(?CarbonInterface $today = null): bool
    {
        $today = ($today ?? now())->startOfDay();

        return $this->status === VacancyStatus::Published
            && ($this->opens_at === null || $this->opens_at->lte($today))
            && ($this->closes_at === null || $this->closes_at->gte($today));
    }

    public function isClosed(): bool
    {
        return $this->status === VacancyStatus::Closed;
    }

    /**
     * @return BelongsTo<JobRequest, $this>
     */
    public function jobRequest(): BelongsTo
    {
        return $this->belongsTo(JobRequest::class);
    }

    /**
     * @return HasOne<JobProfile, $this>
     */
    public function profile(): HasOne
    {
        return $this->hasOne(JobProfile::class);
    }

    /**
     * @return HasMany<EvaluationCriterion, $this>
     */
    public function criteria(): HasMany
    {
        return $this->hasMany(EvaluationCriterion::class)->orderBy('position')->orderBy('id');
    }

    /**
     * @return HasOne<SelectionDecision, $this>
     */
    public function selectionDecision(): HasOne
    {
        return $this->hasOne(SelectionDecision::class);
    }

    /**
     * @return HasMany<Application, $this>
     */
    public function applications(): HasMany
    {
        return $this->hasMany(Application::class);
    }

    /**
     * @return BelongsTo<User, $this>
     */
    public function creator(): BelongsTo
    {
        return $this->belongsTo(User::class, 'created_by');
    }

    /**
     * @return BelongsTo<User, $this>
     */
    public function closer(): BelongsTo
    {
        return $this->belongsTo(User::class, 'closed_by');
    }

    /**
     * @return BelongsTo<User, $this>
     */
    public function publisher(): BelongsTo
    {
        return $this->belongsTo(User::class, 'published_by');
    }
}
