<?php

namespace App\Services\Vacancies;

use App\Enums\AuditAction;
use App\Enums\JobRequestStatus;
use App\Enums\VacancyStatus;
use App\Exceptions\BusinessRuleException;
use App\Exceptions\InvalidStateTransition;
use App\Models\EvaluationCriterion;
use App\Models\JobProfile;
use App\Models\JobRequest;
use App\Models\User;
use App\Models\Vacancy;
use App\Services\Audit\AuditLogger;
use App\Services\Support\SequentialCodeGenerator;
use Illuminate\Support\Facades\DB;

/**
 * RF-05 to RF-07: vacancy profile, criteria, configuration and publication.
 */
class VacancyService
{
    public function __construct(
        private readonly AuditLogger $audit,
        private readonly SequentialCodeGenerator $codes,
        private readonly VacancyValidator $validator,
    ) {}

    /**
     * @param  array<string, mixed>  $attributes
     * @param  array<string, string>  $profile
     * @param  list<array<string, mixed>>  $criteria
     */
    public function create(User $hr, JobRequest $jobRequest, array $attributes, array $profile, array $criteria): Vacancy
    {
        if ($jobRequest->status !== JobRequestStatus::Approved) {
            throw new BusinessRuleException('La vacante solo puede generarse desde un requerimiento aprobado.', 'job_request_id');
        }

        if ($jobRequest->vacancy()->exists()) {
            throw new BusinessRuleException('El requerimiento ya tiene una vacante asociada.', 'job_request_id');
        }

        return DB::transaction(function () use ($hr, $jobRequest, $attributes, $profile, $criteria): Vacancy {
            $vacancy = new Vacancy($attributes);
            $vacancy->organization_id = $jobRequest->organization_id;
            $vacancy->job_request_id = $jobRequest->id;
            $vacancy->created_by = $hr->id;
            $vacancy->code = $this->codes->next(Vacancy::class, 'VAC', $jobRequest->organization_id);
            $vacancy->status = VacancyStatus::Draft;
            $vacancy->save();

            $this->saveProfile($vacancy, $profile);
            $this->syncCriteria($vacancy, $criteria);

            $this->audit->record(AuditAction::VacancyCreated, $vacancy, [
                'code' => $vacancy->code,
                'job_request' => $jobRequest->code,
                // GAP-01: el plazo objetivo queda en la bitacora desde su
                // primer valor, para que su inmutabilidad posterior sea
                // comprobable y no solo declarada.
                'target_completion_at' => $vacancy->target_completion_at?->toIso8601String(),
            ], $hr);

            return $vacancy;
        });
    }

    /**
     * @param  array<string, mixed>  $attributes
     * @param  array<string, string>  $profile
     * @param  list<array<string, mixed>>  $criteria
     */
    public function update(Vacancy $vacancy, User $hr, array $attributes, array $profile, array $criteria): Vacancy
    {
        if ($vacancy->status !== VacancyStatus::Draft) {
            throw new BusinessRuleException('Solo se puede configurar una vacante en borrador.');
        }

        return DB::transaction(function () use ($vacancy, $hr, $attributes, $profile, $criteria): Vacancy {
            $vacancy->fill($attributes)->save();
            $this->saveProfile($vacancy, $profile);
            $this->syncCriteria($vacancy, $criteria);

            $this->audit->record(AuditAction::VacancyUpdated, $vacancy, [
                'criteria' => count($criteria),
                'target_completion_at' => $vacancy->target_completion_at?->toIso8601String(),
            ], $hr);

            return $vacancy;
        });
    }

    public function publish(Vacancy $vacancy, User $hr): Vacancy
    {
        return DB::transaction(function () use ($vacancy, $hr): Vacancy {
            $locked = Vacancy::query()->lockForUpdate()->findOrFail($vacancy->getKey());

            if (! $locked->status->canTransitionTo(VacancyStatus::Published)) {
                throw InvalidStateTransition::between('la vacante', $locked->status->label(), VacancyStatus::Published->label());
            }

            $issues = $this->validator->issues($locked);
            if ($issues !== []) {
                throw new BusinessRuleException('La vacante no puede publicarse: '.implode(' ', $issues));
            }

            $locked->status = VacancyStatus::Published;
            $locked->published_by = $hr->id;
            $locked->published_at = now();
            $locked->opens_at ??= now()->startOfDay();
            $locked->save();

            $this->audit->record(AuditAction::VacancyPublished, $locked, ['code' => $locked->code], $hr);

            return $locked;
        });
    }

    /**
     * @param  array<string, string>  $data
     */
    private function saveProfile(Vacancy $vacancy, array $data): void
    {
        $profile = JobProfile::query()->where('vacancy_id', $vacancy->id)->first() ?? new JobProfile;
        $profile->fill($data);
        $profile->organization_id = $vacancy->organization_id;
        $profile->vacancy_id = $vacancy->id;
        $profile->save();
    }

    /**
     * @param  list<array<string, mixed>>  $criteria
     */
    private function syncCriteria(Vacancy $vacancy, array $criteria): void
    {
        $vacancy->criteria()->delete();

        foreach (array_values($criteria) as $position => $data) {
            $criterion = new EvaluationCriterion([
                'name' => trim((string) $data['name']),
                'stage' => $data['stage'],
                'weight' => $data['weight'],
                'min_score' => $data['min_score'],
                'max_score' => $data['max_score'],
                'position' => $position,
            ]);
            $criterion->organization_id = $vacancy->organization_id;
            $criterion->vacancy_id = $vacancy->id;
            $criterion->save();
        }

        $vacancy->unsetRelation('criteria');
    }
}
