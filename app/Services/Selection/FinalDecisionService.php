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
use App\Services\Audit\AuditLogger;
use App\Services\Ranking\VacancyRankingBuilder;
use Illuminate\Support\Facades\DB;

/**
 * RF-23: records the final decision taken by an authorized human. The ranking is consulted only to snapshot
 * the chosen candidate's position; it never chooses. Application states are not changed here (RF-24 does it).
 */
class FinalDecisionService
{
    public function __construct(
        private readonly VacancyRankingBuilder $rankings,
        private readonly AuditLogger $audit,
    ) {}

    public function decide(Vacancy $vacancy, User $approver, int $applicationId, string $justification): SelectionDecision
    {
        return DB::transaction(function () use ($vacancy, $approver, $applicationId, $justification): SelectionDecision {
            $locked = Vacancy::query()->withoutGlobalScopes()->lockForUpdate()->findOrFail($vacancy->getKey());

            if ($locked->status !== VacancyStatus::Published) {
                throw new BusinessRuleException('Solo se puede registrar la decisión final de una convocatoria publicada y abierta.');
            }

            if (SelectionDecision::query()->withoutGlobalScopes()->where('vacancy_id', $locked->id)->exists()) {
                throw new BusinessRuleException('Ya se registró la decisión final para esta vacante; no puede modificarse.');
            }

            $application = Application::query()
                ->withoutGlobalScopes()
                ->where('vacancy_id', $locked->id)
                ->where('organization_id', $locked->organization_id)
                ->find($applicationId);

            if ($application === null) {
                throw new BusinessRuleException('El candidato elegido no pertenece a esta vacante.', 'application_id');
            }

            if ($application->status !== ApplicationStatus::Finalist) {
                throw new BusinessRuleException('Solo se puede elegir a un candidato en la etapa «Finalista».');
            }

            $ranking = $this->rankings->forVacancy($locked);
            $entry = $ranking->entryFor($application->id);

            if ($entry === null) {
                throw new BusinessRuleException('El candidato elegido no tiene resultados completos en el ranking.');
            }

            $decision = new SelectionDecision;
            $decision->forceFill([
                'organization_id' => $locked->organization_id,
                'vacancy_id' => $locked->id,
                'selected_application_id' => $application->id,
                'decided_by' => $approver->id,
                'justification' => $justification,
                'selected_position' => $entry->position,
                'selected_score' => round($entry->total, 2),
                'ranked_candidates' => count($ranking->entries),
                'decided_at' => now(),
            ])->save();

            $this->audit->record(AuditAction::SelectionDecisionRecorded, $decision, [
                'application_id' => $application->id,
                'selected_position' => $entry->position,
                'selected_score' => round($entry->total, 2),
                'ranked_candidates' => count($ranking->entries),
            ], $approver);

            return $decision;
        });
    }
}
