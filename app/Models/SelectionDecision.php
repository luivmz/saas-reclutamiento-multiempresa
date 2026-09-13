<?php

namespace App\Models;

use App\Models\Concerns\BelongsToOrganization;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Support\Carbon;

/**
 * RF-23: final decision taken by an authorized human (Approver). RF-24 stores who registered the selection.
 *
 * @property int $id
 * @property int $organization_id
 * @property int $vacancy_id
 * @property int $selected_application_id
 * @property int $decided_by
 * @property string $justification
 * @property int $selected_position
 * @property float $selected_score
 * @property int $ranked_candidates
 * @property Carbon $decided_at
 * @property int|null $selection_registered_by
 * @property Carbon|null $selection_registered_at
 * @property-read Vacancy $vacancy
 * @property-read Application $selectedApplication
 * @property-read User $decider
 * @property-read User|null $selectionRegistrar
 */
class SelectionDecision extends Model
{
    use BelongsToOrganization;

    protected function casts(): array
    {
        return [
            'selected_position' => 'integer',
            'selected_score' => 'float',
            'ranked_candidates' => 'integer',
            'decided_at' => 'datetime',
            'selection_registered_at' => 'datetime',
        ];
    }

    public function isSelectionRegistered(): bool
    {
        return $this->selection_registered_at !== null;
    }

    /**
     * @return BelongsTo<Vacancy, $this>
     */
    public function vacancy(): BelongsTo
    {
        return $this->belongsTo(Vacancy::class);
    }

    /**
     * @return BelongsTo<Application, $this>
     */
    public function selectedApplication(): BelongsTo
    {
        return $this->belongsTo(Application::class, 'selected_application_id');
    }

    /**
     * @return BelongsTo<User, $this>
     */
    public function decider(): BelongsTo
    {
        return $this->belongsTo(User::class, 'decided_by');
    }

    /**
     * @return BelongsTo<User, $this>
     */
    public function selectionRegistrar(): BelongsTo
    {
        return $this->belongsTo(User::class, 'selection_registered_by');
    }
}
