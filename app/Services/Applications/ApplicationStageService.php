<?php

namespace App\Services\Applications;

use App\Enums\ApplicationStatus;
use App\Enums\AuditAction;
use App\Exceptions\BusinessRuleException;
use App\Exceptions\InvalidStateTransition;
use App\Models\Application;
use App\Models\ApplicationStageHistory;
use App\Models\SelectionDecision;
use App\Models\User;
use App\Models\Vacancy;
use App\Notifications\ApplicationStageChangedNotification;
use App\Services\Audit\AuditLogger;
use Illuminate\Support\Facades\DB;

/**
 * RF-13 to RF-15: shortlist, discard and stage changes with history, audit and candidate notification.
 */
class ApplicationStageService
{
    public function __construct(private readonly AuditLogger $audit) {}

    public function shortlist(Application $application, User $hr, ?string $comment = null): Application
    {
        return $this->moveTo($application, ApplicationStatus::Shortlisted, $hr, $comment);
    }

    public function discard(Application $application, User $hr, string $comment): Application
    {
        return $this->moveTo($application, ApplicationStatus::Discarded, $hr, $comment);
    }

    public function moveTo(Application $application, ApplicationStatus $target, User $hr, ?string $comment = null): Application
    {
        if (! $target->isManualTarget()) {
            throw new BusinessRuleException('Esta etapa solo se asigna al registrar la selección o al cerrar el proceso.', 'status');
        }

        if (SelectionDecision::query()->withoutGlobalScopes()->where('vacancy_id', $application->vacancy_id)->exists()) {
            throw new BusinessRuleException('La decisión final ya fue registrada; no se permiten cambios manuales de etapa en esta convocatoria.');
        }

        return $this->transition($application, $target, $hr, $comment);
    }

    /**
     * Also used by later process steps (evaluations, selection, closure); $notify lets the caller send its own message.
     */
    public function transition(Application $application, ApplicationStatus $target, User $actor, ?string $comment = null, bool $notify = true): Application
    {
        [$updated, $vacancyTitle] = DB::transaction(function () use ($application, $target, $actor, $comment): array {
            $locked = Application::query()->withoutGlobalScopes()->lockForUpdate()->findOrFail($application->getKey());
            $vacancy = Vacancy::query()->withoutGlobalScopes()->findOrFail($locked->vacancy_id);

            if ($vacancy->isClosed()) {
                throw new BusinessRuleException('La convocatoria está cerrada; no se permiten cambios en las postulaciones.');
            }

            $from = $locked->status;

            if (! $from->canTransitionTo($target)) {
                throw InvalidStateTransition::between('la postulación', $from->label(), $target->label());
            }

            $locked->status = $target;
            $locked->stage_changed_at = now();
            $locked->save();

            $history = new ApplicationStageHistory;
            $history->forceFill([
                'organization_id' => $locked->organization_id,
                'application_id' => $locked->id,
                'from_status' => $from,
                'to_status' => $target,
                'changed_by' => $actor->id,
                'comment' => $comment,
            ])->save();

            $this->audit->record(AuditAction::ApplicationStageChanged, $locked, array_filter([
                'from' => $from->value,
                'to' => $target->value,
                'comment' => $comment,
            ]), $actor);

            return [$locked, $vacancy->title];
        });

        if ($notify) {
            $updated->candidate->notify(new ApplicationStageChangedNotification($updated, $vacancyTitle, $target));
        }

        return $updated;
    }
}
