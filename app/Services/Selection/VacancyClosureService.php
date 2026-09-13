<?php

namespace App\Services\Selection;

use App\Enums\ApplicationStatus;
use App\Enums\AuditAction;
use App\Enums\VacancyClosureType;
use App\Enums\VacancyStatus;
use App\Exceptions\BusinessRuleException;
use App\Exceptions\InvalidStateTransition;
use App\Models\Application;
use App\Models\SelectionDecision;
use App\Models\User;
use App\Models\Vacancy;
use App\Services\Applications\ApplicationStageService;
use App\Services\Audit\AuditLogger;
use Illuminate\Support\Facades\DB;

/**
 * RF-25: closes a vacancy once the human decision (RF-23) and the selection (RF-24) are registered.
 * Closing without a selection is not offered because no TO-BE document supports it (docs/assumptions.md A-30).
 */
class VacancyClosureService
{
    public function __construct(
        private readonly ApplicationStageService $stages,
        private readonly AuditLogger $audit,
    ) {}

    public function close(Vacancy $vacancy, User $hr, ?string $notes): Vacancy
    {
        return DB::transaction(function () use ($vacancy, $hr, $notes): Vacancy {
            $locked = Vacancy::query()->withoutGlobalScopes()->lockForUpdate()->findOrFail($vacancy->getKey());

            if (! $locked->status->canTransitionTo(VacancyStatus::Closed)) {
                throw InvalidStateTransition::between('la convocatoria', $locked->status->label(), VacancyStatus::Closed->label());
            }

            $decision = SelectionDecision::query()->withoutGlobalScopes()->where('vacancy_id', $locked->id)->first();

            if ($decision === null || ! $decision->isSelectionRegistered()) {
                throw new BusinessRuleException('Para cerrar la convocatoria primero deben registrarse la decisión final (RF-23) y la selección del candidato (RF-24).');
            }

            $pending = Application::query()
                ->withoutGlobalScopes()
                ->where('vacancy_id', $locked->id)
                ->whereKeyNot($decision->selected_application_id)
                ->whereNotIn('status', array_map(
                    fn (ApplicationStatus $status) => $status->value,
                    [ApplicationStatus::Selected, ApplicationStatus::NotSelected, ApplicationStatus::Discarded],
                ))
                ->orderBy('id')
                ->get();

            foreach ($pending as $application) {
                $this->stages->transition($application, ApplicationStatus::NotSelected, $hr, 'Proceso cerrado: no seleccionado.', notify: false);
            }

            $locked->forceFill([
                'status' => VacancyStatus::Closed,
                'closed_at' => now(),
                'closed_by' => $hr->id,
                'closure_type' => VacancyClosureType::WithSelection,
                'closure_notes' => $notes,
            ])->save();

            $this->audit->record(AuditAction::VacancyClosed, $locked, [
                'closure_type' => VacancyClosureType::WithSelection->value,
                'selected_application_id' => $decision->selected_application_id,
                'not_selected' => $pending->count(),
            ], $hr);

            return $locked;
        });
    }
}
