<?php

namespace App\Services\Selection;

use App\Enums\ApplicationStatus;
use App\Enums\AuditAction;
use App\Enums\VacancyStatus;
use App\Exceptions\BusinessRuleException;
use App\Models\Application;
use App\Models\SelectionDecision;
use App\Models\User;
use App\Models\Vacancy;
use App\Services\Applications\ApplicationStageService;
use App\Services\Audit\AuditLogger;
use Illuminate\Support\Facades\DB;

/**
 * RF-24: HR registers the selection exactly as decided by the approver (RF-23). Only the chosen application changes.
 */
class SelectionRegistrationService
{
    public function __construct(
        private readonly ApplicationStageService $stages,
        private readonly AuditLogger $audit,
    ) {}

    public function register(Vacancy $vacancy, User $hr): Application
    {
        return DB::transaction(function () use ($vacancy, $hr): Application {
            $locked = Vacancy::query()->withoutGlobalScopes()->lockForUpdate()->findOrFail($vacancy->getKey());

            if ($locked->status !== VacancyStatus::Published) {
                throw new BusinessRuleException('Solo se puede registrar la selección en una convocatoria publicada y abierta.');
            }

            $decision = SelectionDecision::query()->withoutGlobalScopes()->where('vacancy_id', $locked->id)->lockForUpdate()->first();

            if ($decision === null) {
                throw new BusinessRuleException('Primero debe registrarse la decisión final del aprobador (RF-23).');
            }

            if ($decision->isSelectionRegistered()) {
                throw new BusinessRuleException('La selección ya fue registrada para esta vacante.');
            }

            $application = Application::query()
                ->withoutGlobalScopes()
                ->where('vacancy_id', $locked->id)
                ->findOrFail($decision->selected_application_id);

            $selected = $this->stages->transition(
                $application,
                ApplicationStatus::Selected,
                $hr,
                'Selección registrada conforme a la decisión final.',
                notify: false,
            );

            $decision->forceFill([
                'selection_registered_by' => $hr->id,
                'selection_registered_at' => now(),
            ])->save();

            $this->audit->record(AuditAction::CandidateSelected, $selected, ['decision_id' => $decision->id], $hr);

            return $selected;
        });
    }
}
