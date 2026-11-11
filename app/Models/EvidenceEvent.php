<?php

namespace App\Models;

use App\Models\Concerns\BelongsToOrganization;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Support\Carbon;

/**
 * EXPERIMENTAL (F37 flow). An inserted event on one evidence version: reviewed, withdrawn, linked to a criterion
 * of the same vacancy, or unlinked (R-04). Never updated nor deleted.
 *
 * @property int $id
 * @property int $organization_id
 * @property int $evidence_item_id
 * @property string $action
 * @property int|null $evaluation_criterion_id
 * @property string|null $reason
 * @property int|null $actor_id
 * @property Carbon $created_at
 * @property-read EvidenceItem $evidence
 * @property-read EvaluationCriterion|null $criterion
 * @property-read User|null $actor
 */
class EvidenceEvent extends Model
{
    use BelongsToOrganization;

    public const UPDATED_AT = null;

    public const REVIEWED = 'revisada';

    public const WITHDRAWN = 'retirada';

    public const LINKED = 'enlazada';

    public const UNLINKED = 'enlace_retirado';

    protected function casts(): array
    {
        return [
            'created_at' => 'datetime',
        ];
    }

    /**
     * @return BelongsTo<EvidenceItem, $this>
     */
    public function evidence(): BelongsTo
    {
        return $this->belongsTo(EvidenceItem::class, 'evidence_item_id');
    }

    /**
     * @return BelongsTo<EvaluationCriterion, $this>
     */
    public function criterion(): BelongsTo
    {
        return $this->belongsTo(EvaluationCriterion::class, 'evaluation_criterion_id');
    }

    /**
     * @return BelongsTo<User, $this>
     */
    public function actor(): BelongsTo
    {
        return $this->belongsTo(User::class, 'actor_id');
    }
}
