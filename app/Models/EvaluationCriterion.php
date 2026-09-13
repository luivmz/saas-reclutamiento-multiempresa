<?php

namespace App\Models;

use App\Enums\CriterionStage;
use App\Models\Concerns\BelongsToOrganization;
use App\Services\Evaluation\CriterionDefinition;
use Database\Factories\EvaluationCriterionFactory;
use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

/**
 * @property int $id
 * @property int $organization_id
 * @property int $vacancy_id
 * @property string $name
 * @property CriterionStage $stage
 * @property float $weight
 * @property float $min_score
 * @property float $max_score
 * @property int $position
 */
#[Fillable(['name', 'stage', 'weight', 'min_score', 'max_score', 'position'])]
class EvaluationCriterion extends Model
{
    /** @use HasFactory<EvaluationCriterionFactory> */
    use BelongsToOrganization, HasFactory;

    protected $table = 'evaluation_criteria';

    protected function casts(): array
    {
        return [
            'stage' => CriterionStage::class,
            'weight' => 'float',
            'min_score' => 'float',
            'max_score' => 'float',
            'position' => 'integer',
        ];
    }

    /**
     * @return array<int, CriterionDefinition> keyed by criterion id
     */
    public static function definitionsFor(int $vacancyId, CriterionStage $stage): array
    {
        return static::query()
            ->withoutGlobalScopes()
            ->where('vacancy_id', $vacancyId)
            ->where('stage', $stage)
            ->orderBy('position')
            ->orderBy('id')
            ->get()
            ->mapWithKeys(fn (self $criterion) => [$criterion->id => $criterion->toDefinition()])
            ->all();
    }

    public function toDefinition(): CriterionDefinition
    {
        return new CriterionDefinition($this->name, $this->stage, $this->weight, $this->min_score, $this->max_score);
    }

    /**
     * @return BelongsTo<Vacancy, $this>
     */
    public function vacancy(): BelongsTo
    {
        return $this->belongsTo(Vacancy::class);
    }
}
