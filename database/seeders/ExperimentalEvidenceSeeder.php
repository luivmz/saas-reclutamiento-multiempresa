<?php

namespace Database\Seeders;

use App\Enums\EvidenceSource;
use App\Enums\EvidenceType;
use App\Enums\UserRole;
use App\Models\Application;
use App\Models\Evaluation;
use App\Models\EvaluationCriterion;
use App\Models\EvidenceItem;
use App\Models\User;
use App\Models\Vacancy;
use App\Services\Evidence\EvidenceService;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Auth;
use RuntimeException;

/**
 * EXPERIMENTAL (exp/evidencias-ml02). Fictitious evidence records for the demo of the evidence flow and the ML-02
 * documentary aid. Runs on top of DemoSeeder and is never called by it:
 *
 *   php artisan db:seed --class=ExperimentalEvidenceSeeder --force
 *
 * Target: the «Docente de Comunicación - Secundaria» application in evaluation, whose evaluation is assigned to
 * evaluador@andino.test. Every text starts with [SINTÉTICO]. The records are chosen so the aid shows a hit for
 * «Conocimientos pedagógicos» and «Clase modelo», a miss (an observation about the session that shares no words with
 * any criterion) and an abstention for «Entrevista personal».
 */
class ExperimentalEvidenceSeeder extends Seeder
{
    public function run(EvidenceService $evidence): void
    {
        $vacancy = Vacancy::withoutGlobalScopes()->where('title', 'Docente de Comunicación - Secundaria')->firstOrFail();
        $evaluation = Evaluation::withoutGlobalScopes()
            ->whereIn('application_id', Application::withoutGlobalScopes()->where('vacancy_id', $vacancy->id)->pluck('id'))
            ->firstOrFail();
        $application = Application::withoutGlobalScopes()->findOrFail($evaluation->application_id);
        $hr = User::query()->where('organization_id', $vacancy->organization_id)->where('role', UserRole::HumanResources)->orderBy('id')->firstOrFail();
        $evaluator = User::query()->findOrFail($evaluation->evaluator_id);
        $criterion = fn (string $name) => EvaluationCriterion::withoutGlobalScopes()->where('vacancy_id', $vacancy->id)->where('name', $name)->firstOrFail();

        if (EvidenceItem::withoutGlobalScopes()->where('application_id', $application->id)->exists()) {
            throw new RuntimeException('La postulación ya tiene evidencias: el seeder no se repite sobre los mismos datos.');
        }

        Auth::login($hr);
        $cv = $evidence->register($hr, $application, EvidenceType::Cv, EvidenceSource::SubmittedDocument,
            '[SINTÉTICO] Licenciatura ficticia en Educación Secundaria.');
        $evidence->correct($hr, $cv, EvidenceType::Cv, EvidenceSource::SubmittedDocument,
            '[SINTÉTICO] Licenciatura ficticia en Educación Secundaria, especialidad de Comunicación.');
        $certificate = $evidence->register($hr, $application, EvidenceType::Certificate, EvidenceSource::SubmittedDocument,
            '[SINTÉTICO] Constancia ficticia de un taller de conocimientos pedagógicos y evaluación formativa.');
        $evidence->link($hr, $certificate, $criterion('Conocimientos pedagógicos')->id);
        $evidence->review($hr, $certificate);

        Auth::login($evaluator);
        $model = $evidence->register($evaluator, $application, EvidenceType::Observation, EvidenceSource::AssignedSession,
            '[SINTÉTICO] En la clase modelo ficticia presentó los objetivos y cerró con preguntas al grupo.');
        $evidence->link($evaluator, $model, $criterion('Clase modelo')->id);
        $evidence->register($evaluator, $application, EvidenceType::Observation, EvidenceSource::AssignedSession,
            '[SINTÉTICO] Organizó la secuencia de actividades con metas por sesión.');

        Auth::logout();

        $this->command?->info("Evidencias ficticias cargadas en la postulación {$application->trackingCode()} (id {$application->id}).");
    }
}
