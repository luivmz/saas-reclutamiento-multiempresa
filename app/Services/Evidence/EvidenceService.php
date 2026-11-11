<?php

namespace App\Services\Evidence;

use App\Enums\AuditAction;
use App\Enums\EvidenceSource;
use App\Enums\EvidenceState;
use App\Enums\EvidenceType;
use App\Exceptions\BusinessRuleException;
use App\Models\Application;
use App\Models\EvaluationCriterion;
use App\Models\EvidenceEvent;
use App\Models\EvidenceItem;
use App\Models\User;
use App\Models\Vacancy;
use App\Services\Audit\AuditLogger;
use Illuminate\Support\Facades\DB;
use Illuminate\Validation\ValidationException;

/**
 * EXPERIMENTAL (F37 flow, exp/evidencias-ml02). Append-only writes (R-04): every action inserts a row, nothing is
 * updated or deleted. Authorization (role matrix, R-01, R-02, R-08) is the policy's job; this service enforces the
 * state rules and R-03, and audits with identifiers only (R-07).
 *
 * APP-M01: the policy reads the vacancy before the write, so a closure committed in between would let the write
 * through. Every write therefore re-checks R-08 inside its own transaction under a SHARED lock of the vacancy, taken
 * before any application lock, the order of VacancyClosureService (vacancy, then applications) and of
 * ApplicationStageService::moveTo(). The closure's FOR UPDATE waits for writes in progress; writes that arrive while
 * the closure holds the vacancy wait for it and are then rejected. Two writes do not block each other on it.
 *
 * Nothing here feeds the ranking, the final decision or the ML-01 risk card (R-06).
 */
class EvidenceService
{
    public function __construct(private readonly AuditLogger $audit) {}

    public function register(User $actor, Application $application, EvidenceType $type, EvidenceSource $source, string $description): EvidenceItem
    {
        return DB::transaction(function () use ($actor, $application, $type, $source, $description): EvidenceItem {
            $this->lockOpenVacancy($application);
            $item = $this->insertItem($actor, $application, $type, $source, $description, null);
            $this->audit->record(AuditAction::EvidenceRegistered, $item, $this->ids($item), $actor);

            return $item;
        });
    }

    public function link(User $actor, EvidenceItem $evidence, int $criterionId): EvidenceEvent
    {
        return DB::transaction(function () use ($actor, $evidence, $criterionId): EvidenceEvent {
            $ledger = $this->lockedLedger($evidence);
            $this->assertCurrent($ledger, $evidence, 'Solo se enlaza evidencia vigente.');
            $criterion = $this->criterionOfVacancy($evidence, $criterionId);

            if ($ledger->isLinked($evidence, $criterion->id)) {
                throw ValidationException::withMessages(['criterion_id' => 'La evidencia ya está enlazada a ese criterio.']);
            }

            $event = $this->insertEvent($actor, $evidence, EvidenceEvent::LINKED, $criterion->id);
            $this->audit->record(AuditAction::EvidenceLinked, $evidence, $this->ids($evidence) + ['criterion_id' => $criterion->id], $actor);

            return $event;
        });
    }

    public function unlink(User $actor, EvidenceItem $evidence, int $criterionId): EvidenceEvent
    {
        return DB::transaction(function () use ($actor, $evidence, $criterionId): EvidenceEvent {
            $ledger = $this->lockedLedger($evidence);
            $this->assertCurrent($ledger, $evidence, 'Solo se desenlaza evidencia vigente.');
            $criterion = $this->criterionOfVacancy($evidence, $criterionId);

            if (! $ledger->isLinked($evidence, $criterion->id)) {
                throw ValidationException::withMessages(['criterion_id' => 'No hay un enlace vigente con ese criterio.']);
            }

            $event = $this->insertEvent($actor, $evidence, EvidenceEvent::UNLINKED, $criterion->id);
            $this->audit->record(AuditAction::EvidenceUnlinked, $evidence, $this->ids($evidence) + ['criterion_id' => $criterion->id], $actor);

            return $event;
        });
    }

    public function review(User $actor, EvidenceItem $evidence): EvidenceEvent
    {
        return DB::transaction(function () use ($actor, $evidence): EvidenceEvent {
            $ledger = $this->lockedLedger($evidence);

            if ($ledger->state($evidence) !== EvidenceState::Registered) {
                throw ValidationException::withMessages(['evidence' => 'Solo se revisa evidencia registrada y vigente.']);
            }

            $event = $this->insertEvent($actor, $evidence, EvidenceEvent::REVIEWED);
            $this->audit->record(AuditAction::EvidenceReviewed, $evidence, $this->ids($evidence), $actor);

            return $event;
        });
    }

    /**
     * A new version supersedes the current one and inherits its active links, as new link events (F37 §3).
     */
    public function correct(User $actor, EvidenceItem $evidence, EvidenceType $type, EvidenceSource $source, string $description): EvidenceItem
    {
        return DB::transaction(function () use ($actor, $evidence, $type, $source, $description): EvidenceItem {
            $ledger = $this->lockedLedger($evidence);
            $this->assertCurrent($ledger, $evidence, 'Solo se corrige evidencia vigente.');

            $version = $this->insertItem($actor, $evidence->application, $type, $source, $description, $evidence->id);

            foreach ($ledger->activeLinks($evidence) as $criterionId) {
                $this->insertEvent($actor, $version, EvidenceEvent::LINKED, $criterionId);
            }

            $this->audit->record(AuditAction::EvidenceCorrected, $version, $this->ids($version) + ['supersedes_id' => $evidence->id], $actor);

            return $version;
        });
    }

    public function withdraw(User $actor, EvidenceItem $evidence, string $reason): EvidenceEvent
    {
        return DB::transaction(function () use ($actor, $evidence, $reason): EvidenceEvent {
            $ledger = $this->lockedLedger($evidence);
            $this->assertCurrent($ledger, $evidence, 'Solo se retira evidencia vigente.');

            $event = $this->insertEvent($actor, $evidence, EvidenceEvent::WITHDRAWN, null, $reason);
            $this->audit->record(AuditAction::EvidenceWithdrawn, $evidence, $this->ids($evidence), $actor);

            return $event;
        });
    }

    /**
     * Serializes concurrent writes on the same application: SELECT ... FOR UPDATE is a read, so it does not
     * collide with the append-only trigger.
     */
    private function lockedLedger(EvidenceItem $evidence): EvidenceLedger
    {
        $this->lockOpenVacancy($evidence->application);
        Application::query()->whereKey($evidence->application_id)->lockForUpdate()->first();

        return EvidenceLedger::for($evidence->application);
    }

    /**
     * R-08 under lock (APP-M01): SHARED lock of the vacancy, then the closed check. Must run first in the transaction.
     */
    private function lockOpenVacancy(Application $application): void
    {
        $vacancy = Vacancy::query()->withoutGlobalScopes()->whereKey($application->vacancy_id)->sharedLock()->firstOrFail();

        if ($vacancy->isClosed()) {
            throw new BusinessRuleException('La convocatoria está cerrada: su evidencia queda congelada y ya no admite escrituras (R-08).');
        }
    }

    private function assertCurrent(EvidenceLedger $ledger, EvidenceItem $evidence, string $message): void
    {
        if (! $ledger->state($evidence)->isCurrent()) {
            throw ValidationException::withMessages(['evidence' => $message]);
        }
    }

    /**
     * R-03: a link only points to a criterion of the vacancy of the application, in the same organization.
     */
    private function criterionOfVacancy(EvidenceItem $evidence, int $criterionId): EvaluationCriterion
    {
        $application = $evidence->application;

        $criterion = EvaluationCriterion::query()
            ->whereKey($criterionId)
            ->where('vacancy_id', $application->vacancy_id)
            ->where('organization_id', $application->organization_id)
            ->first();

        if ($criterion === null) {
            throw ValidationException::withMessages(['criterion_id' => 'El criterio no pertenece a la vacante de esta postulación.']);
        }

        return $criterion;
    }

    private function insertItem(User $actor, Application $application, EvidenceType $type, EvidenceSource $source, string $description, ?int $supersedes): EvidenceItem
    {
        $item = new EvidenceItem;
        $item->forceFill([
            'organization_id' => $application->organization_id,
            'application_id' => $application->id,
            'supersedes_id' => $supersedes,
            'type' => $type,
            'source' => $source,
            'description' => $description,
            'registered_by' => $actor->id,
        ])->save();

        return $item->setRelation('application', $application);
    }

    private function insertEvent(User $actor, EvidenceItem $evidence, string $action, ?int $criterionId = null, ?string $reason = null): EvidenceEvent
    {
        $event = new EvidenceEvent;
        $event->forceFill([
            'organization_id' => $evidence->organization_id,
            'evidence_item_id' => $evidence->id,
            'action' => $action,
            'evaluation_criterion_id' => $criterionId,
            'reason' => $reason,
            'actor_id' => $actor->id,
        ])->save();

        return $event;
    }

    /**
     * @return array<string, int>
     */
    private function ids(EvidenceItem $evidence): array
    {
        return ['evidence_id' => $evidence->id, 'application_id' => $evidence->application_id];
    }
}
