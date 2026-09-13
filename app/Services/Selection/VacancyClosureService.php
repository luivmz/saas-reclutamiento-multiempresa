<?php

namespace App\Services\Selection;

use App\Enums\ApplicationStatus;
use App\Enums\AuditAction;
use App\Enums\VacancyClosureType;
use App\Enums\VacancyStatus;
use App\Exceptions\BusinessRuleException;
use App\Exceptions\InvalidStateTransition;
use App\Models\Application;
use App\Models\Organization;
use App\Models\SelectionDecision;
use App\Models\User;
use App\Models\Vacancy;
use App\Notifications\ProcessResultNotification;
use App\Services\Applications\ApplicationStageService;
use App\Services\Audit\AuditLogger;
use Illuminate\Support\Facades\DB;

/**
 * RF-25: closes a vacancy once the human decision (RF-23) and the selection (RF-24) are registered.
 * RF-26: only then each affected candidate receives the final result (docs/assumptions.md A-31, A-32).
 * Closing without a selection is not offered because no TO-BE document supports it (A-30).
 */
class VacancyClosureService
{
    public function __construct(
        private readonly ApplicationStageService $stages,
        private readonly AuditLogger $audit,
    ) {}

    public function close(Vacancy $vacancy, User $hr, ?string $notes): Vacancy
    {
        [$closed, $selected, $notSelected] = DB::transaction(function () use ($vacancy, $hr, $notes): array {
            $locked = Vacancy::query()->withoutGlobalScopes()->lockForUpdate()->findOrFail($vacancy->getKey());

            if (! $locked->status->canTransitionTo(VacancyStatus::Closed)) {
                throw InvalidStateTransition::between('la convocatoria', $locked->status->label(), VacancyStatus::Closed->label());
            }

            $decision = SelectionDecision::query()->withoutGlobalScopes()->where('vacancy_id', $locked->id)->first();

            if ($decision === null || ! $decision->isSelectionRegistered()) {
                throw new BusinessRuleException('Para cerrar la convocatoria primero deben registrarse la decisión final (RF-23) y la selección del candidato (RF-24).');
            }

            $selected = Application::query()->withoutGlobalScopes()->where('vacancy_id', $locked->id)->findOrFail($decision->selected_application_id);

            $pending = Application::query()
                ->withoutGlobalScopes()
                ->where('vacancy_id', $locked->id)
                ->whereKeyNot($selected->id)
                ->whereNotIn('status', array_map(
                    fn (ApplicationStatus $status) => $status->value,
                    [ApplicationStatus::Selected, ApplicationStatus::NotSelected, ApplicationStatus::Discarded],
                ))
                ->orderBy('id')
                ->get();

            $notSelected = $pending->map(fn (Application $application) => $this->stages->transition(
                $application,
                ApplicationStatus::NotSelected,
                $hr,
                'Proceso cerrado: no seleccionado.',
                notify: false,
            ))->all();

            $locked->forceFill([
                'status' => VacancyStatus::Closed,
                'closed_at' => now(),
                'closed_by' => $hr->id,
                'closure_type' => VacancyClosureType::WithSelection,
                'closure_notes' => $notes,
            ])->save();

            $this->audit->record(AuditAction::VacancyClosed, $locked, [
                'closure_type' => VacancyClosureType::WithSelection->value,
                'selected_application_id' => $selected->id,
                'not_selected' => count($notSelected),
            ], $hr);

            $this->audit->record(AuditAction::ProcessResultNotified, $locked, [
                'selected' => 1,
                'not_selected' => count($notSelected),
            ], $hr);

            return [$locked, $selected, $notSelected];
        });

        $this->notifyResults($closed, $selected, $notSelected);

        return $closed;
    }

    /**
     * @param  list<Application>  $notSelected
     */
    private function notifyResults(Vacancy $vacancy, Application $selected, array $notSelected): void
    {
        $organizationName = Organization::query()->findOrFail($vacancy->organization_id)->name;

        $outcomes = [[$selected, ApplicationStatus::Selected]];
        foreach ($notSelected as $application) {
            $outcomes[] = [$application, ApplicationStatus::NotSelected];
        }

        foreach ($outcomes as [$application, $result]) {
            User::query()->findOrFail($application->candidate_id)->notify(
                new ProcessResultNotification($application, $result, $vacancy->title, $organizationName),
            );
        }
    }
}
