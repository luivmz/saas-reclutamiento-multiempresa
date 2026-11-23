<?php

use App\Http\Controllers\Applications\ApplicationController;
use App\Http\Controllers\Applications\ApplicationStageController;
use App\Http\Controllers\Applications\VacancyApplicationController;
use App\Http\Controllers\Assessments\AssessmentAssignmentController;
use App\Http\Controllers\Assessments\AssessmentScheduleController;
use App\Http\Controllers\Assessments\EvaluationController;
use App\Http\Controllers\Assessments\InterviewController;
use App\Http\Controllers\Audit\AuditLogController;
use App\Http\Controllers\Candidates\ApplyController;
use App\Http\Controllers\Candidates\CandidateApplicationController;
use App\Http\Controllers\Candidates\CandidateCvController;
use App\Http\Controllers\Candidates\CandidateProfileController;
use App\Http\Controllers\Documents\CandidateDocumentDownloadController;
use App\Http\Controllers\Evidence\ApplicationEvidenceController;
use App\Http\Controllers\Evidence\EvidenceItemController;
use App\Http\Controllers\JobRequests\JobRequestController;
use App\Http\Controllers\JobRequests\JobRequestTransitionController;
use App\Http\Controllers\NotificationController;
use App\Http\Controllers\PublicVacancyController;
use App\Http\Controllers\Reports\RecruitmentReportController;
use App\Http\Controllers\Selection\FinalDecisionController;
use App\Http\Controllers\Selection\SelectionRegistrationController;
use App\Http\Controllers\Selection\VacancyClosureController;
use App\Http\Controllers\Selection\VacancyComparisonController;
use App\Http\Controllers\Vacancies\VacancyController;
use App\Http\Controllers\Vacancies\VacancyOperationalRiskController;
use App\Http\Controllers\Vacancies\VacancyPublicationController;
use Illuminate\Support\Facades\Route;

Route::inertia('/', 'welcome')->name('home');

Route::get('empleos', [PublicVacancyController::class, 'index'])->name('jobs.index');
Route::get('empleos/{vacancy}', [PublicVacancyController::class, 'show'])->whereNumber('vacancy')->name('jobs.show');

Route::middleware(['auth'])->group(function () {
    Route::inertia('dashboard', 'dashboard')->name('dashboard');

    Route::get('notificaciones', [NotificationController::class, 'index'])->name('notifications.index');
    Route::post('notificaciones/leer-todas', [NotificationController::class, 'markAllAsRead'])->name('notifications.read-all');
    Route::post('notificaciones/{notification}/leer', [NotificationController::class, 'markAsRead'])->whereUuid('notification')->name('notifications.read');

    Route::get('documentos/{document}/descargar', CandidateDocumentDownloadController::class)->name('documents.download');

    // RF-01 a RF-04
    Route::resource('requerimientos', JobRequestController::class)
        ->except('destroy')
        ->parameters(['requerimientos' => 'jobRequest'])
        ->names('job-requests');

    Route::controller(JobRequestTransitionController::class)
        ->prefix('requerimientos/{jobRequest}')
        ->name('job-requests.')
        ->group(function () {
            Route::post('enviar', 'submit')->name('submit');
            Route::post('observar', 'observe')->name('observe');
            Route::post('validar', 'validate')->name('validate');
            Route::post('decision', 'decide')->name('decide');
        });

    // RF-05 a RF-07
    Route::resource('vacantes', VacancyController::class)
        ->except('destroy')
        ->parameters(['vacantes' => 'vacancy'])
        ->names('vacancies');

    Route::post('vacantes/{vacancy}/publicar', VacancyPublicationController::class)->name('vacancies.publish');

    // Fase 16: riesgo operacional del proceso. Experimental, informativo y
    // limitado a RR. HH. y Aprobador de la misma organizacion.
    Route::get('vacantes/{vacancy}/riesgo-operacional', VacancyOperationalRiskController::class)->name('vacancies.operational-risk');

    // RF-08 a RF-11 (postulante)
    Route::post('empleos/{vacancy}/postular', ApplyController::class)->whereNumber('vacancy')->name('jobs.apply');

    Route::middleware('role:postulante')->group(function () {
        Route::get('mi-perfil', [CandidateProfileController::class, 'edit'])->name('candidate.profile.edit');
        Route::put('mi-perfil', [CandidateProfileController::class, 'update'])->name('candidate.profile.update');
        Route::post('mi-perfil/cv', CandidateCvController::class)->name('candidate.cv.store');
        Route::get('mis-postulaciones', [CandidateApplicationController::class, 'index'])->name('candidate.applications.index');
        Route::get('mis-postulaciones/{application}', [CandidateApplicationController::class, 'show'])->name('candidate.applications.show');
    });

    // RF-12 a RF-15
    Route::get('vacantes/{vacancy}/postulaciones', VacancyApplicationController::class)->name('vacancies.applications.index');
    Route::get('postulaciones/{application}', ApplicationController::class)->name('applications.show');

    Route::controller(ApplicationStageController::class)
        ->prefix('postulaciones/{application}')
        ->name('applications.')
        ->group(function () {
            Route::post('preseleccionar', 'shortlist')->name('shortlist');
            Route::post('descartar', 'discard')->name('discard');
            Route::post('etapa', 'change')->name('stage');
        });

    // RF-16 a RF-19
    Route::post('postulaciones/{application}/evaluaciones', [AssessmentScheduleController::class, 'evaluation'])->name('applications.evaluations.store');
    Route::post('postulaciones/{application}/entrevistas', [AssessmentScheduleController::class, 'interview'])->name('applications.interviews.store');

    Route::get('mis-evaluaciones', AssessmentAssignmentController::class)->middleware('role:evaluador')->name('assessments.index');

    Route::get('evaluaciones/{evaluation}', [EvaluationController::class, 'show'])->name('evaluations.show');
    Route::post('evaluaciones/{evaluation}/resultados', [EvaluationController::class, 'recordResult'])->name('evaluations.results.store');
    Route::get('entrevistas/{interview}', [InterviewController::class, 'show'])->name('interviews.show');
    Route::post('entrevistas/{interview}/resultados', [InterviewController::class, 'recordResult'])->name('interviews.results.store');

    // RF-20 a RF-25
    Route::get('vacantes/{vacancy}/comparacion', VacancyComparisonController::class)->name('vacancies.comparison');
    Route::post('vacantes/{vacancy}/decision', FinalDecisionController::class)->name('vacancies.decision.store');
    Route::post('vacantes/{vacancy}/seleccion', SelectionRegistrationController::class)->name('vacancies.selection.store');
    Route::post('vacantes/{vacancy}/cerrar', VacancyClosureController::class)->name('vacancies.close');

    // RF-27 (solo lectura)
    Route::get('auditoria', [AuditLogController::class, 'index'])->name('audit.index');

    // RF-28 (candidato): reportes operativos del proceso, solo lectura y agregados.
    Route::get('reportes', RecruitmentReportController::class)->name('reports.index');

    // EXPERIMENTAL (rama local exp/evidencias-ml02): flujo de evidencias ficticias y ayuda documental ML-02.
    // Responde 404 salvo con EXPERIMENTAL_EVIDENCIAS=true (config/experimental.php). No es la integración formal
    // en el SaaS, que sigue condicionada a la G0 real, un ADR y la decisión N5 (EI-23). F37-SBX sigue BLOQUEADA.
    Route::middleware('experimental:evidencias')->group(function () {
        Route::get('postulaciones/{application}/evidencias', [ApplicationEvidenceController::class, 'index'])->name('applications.evidence.index');
        Route::get('postulaciones/{application}/evidencias/historial', [ApplicationEvidenceController::class, 'history'])->name('applications.evidence.history');
        Route::post('postulaciones/{application}/evidencias', [ApplicationEvidenceController::class, 'store'])->name('applications.evidence.store');

        Route::controller(EvidenceItemController::class)
            ->prefix('evidencias/{evidence}')
            ->name('evidence.')
            ->group(function () {
                Route::post('enlaces', 'link')->name('link');
                Route::delete('enlaces/{criterion}', 'unlink')->whereNumber('criterion')->name('unlink');
                Route::post('revision', 'review')->name('review');
                Route::post('correccion', 'correct')->name('correct');
                Route::post('retiro', 'withdraw')->name('withdraw');
            });
    });
});

require __DIR__.'/settings.php';
