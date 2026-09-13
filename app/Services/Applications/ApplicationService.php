<?php

namespace App\Services\Applications;

use App\Enums\ApplicationStatus;
use App\Enums\AuditAction;
use App\Exceptions\BusinessRuleException;
use App\Models\Application;
use App\Models\ApplicationStageHistory;
use App\Models\CandidateProfile;
use App\Models\User;
use App\Models\Vacancy;
use App\Notifications\ApplicationReceivedNotification;
use App\Services\Audit\AuditLogger;
use Illuminate\Database\UniqueConstraintViolationException;
use Illuminate\Support\Facades\DB;

/**
 * RF-10 and RF-11: register an application and confirm it to the candidate.
 */
class ApplicationService
{
    public function __construct(private readonly AuditLogger $audit) {}

    public function apply(User $candidate, Vacancy $vacancy): Application
    {
        try {
            [$application, $locked] = DB::transaction(function () use ($candidate, $vacancy): array {
                $locked = Vacancy::query()->withoutGlobalScopes()->with('organization:id,name')->lockForUpdate()->findOrFail($vacancy->getKey());

                if (! $locked->acceptsApplications()) {
                    throw new BusinessRuleException('La convocatoria no está abierta a postulaciones.');
                }

                $profile = CandidateProfile::query()->with('latestCv')->where('user_id', $candidate->id)->first();

                if ($profile === null || ! $profile->isComplete()) {
                    throw new BusinessRuleException('Complete su perfil de postulante antes de postular.');
                }

                if ($profile->latestCv === null) {
                    throw new BusinessRuleException('Cargue su CV en formato PDF antes de postular.');
                }

                if ($this->alreadyApplied($candidate, $locked)) {
                    throw new BusinessRuleException('Ya registró una postulación para esta vacante.');
                }

                $application = new Application;
                $application->forceFill([
                    'organization_id' => $locked->organization_id,
                    'vacancy_id' => $locked->id,
                    'candidate_id' => $candidate->id,
                    'candidate_document_id' => $profile->latestCv->id,
                    'status' => ApplicationStatus::Submitted,
                    'applied_at' => now(),
                    'stage_changed_at' => now(),
                ])->save();

                $history = new ApplicationStageHistory;
                $history->forceFill([
                    'organization_id' => $application->organization_id,
                    'application_id' => $application->id,
                    'from_status' => null,
                    'to_status' => ApplicationStatus::Submitted,
                    'changed_by' => $candidate->id,
                ])->save();

                $this->audit->record(AuditAction::ApplicationSubmitted, $application, ['vacancy' => $locked->code], $candidate);

                return [$application, $locked];
            });
        } catch (UniqueConstraintViolationException) {
            throw new BusinessRuleException('Ya registró una postulación para esta vacante.');
        }

        $candidate->notify(new ApplicationReceivedNotification($application, $locked->title, $locked->organization->name));

        return $application;
    }

    private function alreadyApplied(User $candidate, Vacancy $vacancy): bool
    {
        return Application::query()
            ->withoutGlobalScopes()
            ->where('vacancy_id', $vacancy->id)
            ->where('candidate_id', $candidate->id)
            ->exists();
    }
}
