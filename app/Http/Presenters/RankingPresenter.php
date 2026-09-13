<?php

namespace App\Http\Presenters;

use App\Models\Application;
use App\Services\Ranking\CriterionBreakdown;
use App\Services\Ranking\IncompleteCandidate;
use App\Services\Ranking\RankedCandidate;
use App\Services\Ranking\RankingResult;
use Illuminate\Support\Collection;

class RankingPresenter
{
    public const FORMULA = 'Puntaje total = Σ [(promedio del criterio − mínimo) ÷ (máximo − mínimo) × ponderación] ÷ Σ ponderaciones × 100';

    /**
     * @param  Collection<int, Application>  $applications  keyed by id
     * @return array{entries: list<array<string, mixed>>, incomplete: list<array<string, mixed>>}
     */
    public function present(RankingResult $result, Collection $applications): array
    {
        return [
            'entries' => array_map(fn (RankedCandidate $entry) => [
                'position' => $entry->position,
                'application_id' => $entry->applicationId,
                'candidate_name' => $entry->candidateName,
                'application_status' => $applications->get($entry->applicationId)?->status->present(),
                'total' => round($entry->total, 2),
                'tied' => $entry->tied,
                'breakdown' => array_map(fn (CriterionBreakdown $item) => [
                    'criterion_id' => $item->criterionId,
                    'name' => $item->name,
                    'weight' => $item->weight,
                    'average' => round($item->average, 2),
                    'normalized' => round($item->normalized, 4),
                    'contribution' => round($item->contribution, 2),
                ], $entry->breakdown),
            ], $result->entries),
            'incomplete' => array_map(fn (IncompleteCandidate $candidate) => [
                'application_id' => $candidate->applicationId,
                'candidate_name' => $candidate->candidateName,
                'application_status' => $applications->get($candidate->applicationId)?->status->present(),
                'missing_criteria' => $candidate->missingCriteria,
            ], $result->incomplete),
        ];
    }
}
