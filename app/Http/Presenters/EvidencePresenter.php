<?php

namespace App\Http\Presenters;

use App\Enums\EvidenceState;
use App\Models\EvaluationCriterion;
use App\Models\EvidenceEvent;
use App\Models\EvidenceItem;
use App\Models\User;
use App\Services\Evidence\EvidenceLedger;

/**
 * EXPERIMENTAL (F37 flow). Shapes the evidence records of one application for the page: one entry per record, with
 * its current version, its versions oldest first, its active links and what the viewer may do with it.
 * It never exposes the candidate's name or contact data.
 */
class EvidencePresenter
{
    /**
     * @param  array<int, EvaluationCriterion>  $criteria  keyed by id
     * @return list<array<string, mixed>>
     */
    public function records(EvidenceLedger $ledger, User $viewer, array $criteria): array
    {
        $records = [];

        foreach ($ledger->lineages() as $versions) {
            $latest = end($versions);
            $state = $ledger->state($latest);
            $withdrawal = $ledger->events($latest)->firstWhere('action', EvidenceEvent::WITHDRAWN);

            $records[] = [
                ...$this->version($ledger, $latest, count($versions)),
                'record_code' => $versions[0]->code(),
                'links' => array_values(array_map(
                    fn (int $id) => ['id' => $id, 'name' => $criteria[$id]->name ?? "Criterio {$id}"],
                    $ledger->activeLinks($latest),
                )),
                'withdrawal_reason' => $withdrawal?->reason,
                'versions' => array_map(
                    fn (EvidenceItem $item, int $i) => $this->version($ledger, $item, $i + 1),
                    $versions,
                    array_keys($versions),
                ),
                'can' => [
                    'link' => $state->isCurrent() && $viewer->can('link', $latest),
                    'review' => $state === EvidenceState::Registered && $viewer->can('review', $latest),
                    'correct' => $state->isCurrent() && $viewer->can('correct', $latest),
                    'withdraw' => $state->isCurrent() && $viewer->can('withdraw', $latest),
                ],
            ];
        }

        return $records;
    }

    /**
     * @return array<string, mixed>
     */
    public function version(EvidenceLedger $ledger, EvidenceItem $item, int $number): array
    {
        return [
            'id' => $item->id,
            'code' => $item->code(),
            'version' => $number,
            'type' => $item->type->present(),
            'source' => $item->source->present(),
            'state' => $ledger->state($item)->present(),
            'description' => $item->description,
            'author' => $item->author ? ['name' => $item->author->name, 'role' => $item->author->role->label()] : null,
            'created_at' => $item->created_at->toIso8601String(),
        ];
    }

    /**
     * A fragment as the documentary aid shows it: the evidence and where it comes from (source attribution).
     *
     * @param  list<string>  $matchedWords
     * @return array<string, mixed>
     */
    public function fragment(EvidenceLedger $ledger, EvidenceItem $item, array $matchedWords = []): array
    {
        $version = 1;
        $cursor = $item;
        while ($cursor->supersedes_id !== null && ($previous = $ledger->items()->get($cursor->supersedes_id)) !== null) {
            $version++;
            $cursor = $previous;
        }

        return [
            'id' => $item->id,
            'code' => $item->code(),
            'version' => $version,
            'type' => $item->type->present(),
            'source' => $item->source->present(),
            'state' => $ledger->state($item)->present(),
            'description' => $item->description,
            'matched_words' => $matchedWords,
        ];
    }
}
