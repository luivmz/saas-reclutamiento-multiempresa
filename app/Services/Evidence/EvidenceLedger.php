<?php

namespace App\Services\Evidence;

use App\Enums\EvidenceState;
use App\Models\Application;
use App\Models\EvidenceEvent;
use App\Models\EvidenceItem;
use Illuminate\Support\Collection;

/**
 * EXPERIMENTAL (F37 flow). Derives the state of every evidence version of one application from its append-only
 * rows (R-04): a version is superseded when a newer one points to it; otherwise its own events say whether it was
 * withdrawn or reviewed. A link is active when the last link event for that criterion is `enlazada`.
 */
class EvidenceLedger
{
    /** @var Collection<int, EvidenceItem> */
    private Collection $items;

    /** @var Collection<int, Collection<int, EvidenceEvent>> */
    private Collection $eventsByItem;

    /** @var array<int, true> */
    private array $superseded = [];

    public function __construct(public readonly Application $application)
    {
        $this->items = EvidenceItem::query()
            ->where('application_id', $application->id)
            ->with('author:id,name,role')
            ->orderBy('id')
            ->get()
            ->each(fn (EvidenceItem $item) => $item->setRelation('application', $application))
            ->keyBy('id');

        $application->loadMissing('vacancy');

        $this->eventsByItem = EvidenceEvent::query()
            ->whereIn('evidence_item_id', $this->items->keys())
            ->with(['criterion:id,name', 'actor:id,name,role'])
            ->orderBy('id')
            ->get()
            ->groupBy('evidence_item_id');

        foreach ($this->items as $item) {
            if ($item->supersedes_id !== null) {
                $this->superseded[$item->supersedes_id] = true;
            }
        }
    }

    public static function for(Application $application): self
    {
        return new self($application);
    }

    /**
     * @return Collection<int, EvidenceItem>
     */
    public function items(): Collection
    {
        return $this->items;
    }

    /**
     * @return Collection<int, EvidenceEvent>
     */
    public function events(EvidenceItem $item): Collection
    {
        return $this->eventsByItem->get($item->id, collect());
    }

    public function state(EvidenceItem $item): EvidenceState
    {
        if (isset($this->superseded[$item->id])) {
            return EvidenceState::Superseded;
        }

        $actions = $this->events($item)->pluck('action');

        return match (true) {
            $actions->contains(EvidenceEvent::WITHDRAWN) => EvidenceState::Withdrawn,
            $actions->contains(EvidenceEvent::REVIEWED) => EvidenceState::Reviewed,
            default => EvidenceState::Registered,
        };
    }

    /**
     * @return list<int> criterion ids with an active link, in ascending order
     */
    public function activeLinks(EvidenceItem $item): array
    {
        $last = [];

        foreach ($this->events($item) as $event) {
            if ($event->evaluation_criterion_id !== null) {
                $last[$event->evaluation_criterion_id] = $event->action;
            }
        }

        $active = array_keys(array_filter($last, fn (string $action) => $action === EvidenceEvent::LINKED));
        sort($active);

        return $active;
    }

    public function isLinked(EvidenceItem $item, int $criterionId): bool
    {
        return in_array($criterionId, $this->activeLinks($item), true);
    }

    /**
     * Versions of each record, oldest first, grouped by their first version. Records are ordered by first id.
     *
     * @return list<list<EvidenceItem>>
     */
    public function lineages(): array
    {
        $next = [];
        foreach ($this->items as $item) {
            if ($item->supersedes_id !== null) {
                $next[$item->supersedes_id] = $item;
            }
        }

        $lineages = [];
        foreach ($this->items as $item) {
            if ($item->supersedes_id !== null) {
                continue;
            }

            $chain = [$item];
            while (isset($next[end($chain)->id])) {
                $chain[] = $next[end($chain)->id];
            }
            $lineages[] = $chain;
        }

        return $lineages;
    }

    /**
     * Current versions only (registered or reviewed), the corpus of the ML-02 documentary aid.
     *
     * @return Collection<int, EvidenceItem>
     */
    public function currentItems(): Collection
    {
        return $this->items->filter(fn (EvidenceItem $item) => $this->state($item)->isCurrent())->values();
    }
}
