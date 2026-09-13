<?php

use App\Http\Controllers\Applications\ApplicationController;
use App\Http\Controllers\Applications\ApplicationStageController;
use App\Http\Controllers\Applications\VacancyApplicationController;
use App\Http\Controllers\Assessments\AssessmentAssignmentController;
use App\Http\Controllers\Assessments\AssessmentScheduleController;
use App\Http\Controllers\Assessments\EvaluationController;
use App\Http\Controllers\Assessments\InterviewController;
use App\Http\Controllers\Candidates\ApplyController;
use App\Http\Controllers\Candidates\CandidateApplicationController;
use App\Http\Controllers\Candidates\CandidateCvController;
use App\Http\Controllers\Candidates\CandidateProfileController;
use App\Http\Controllers\Documents\CandidateDocumentDownloadController;
use App\Http\Controllers\JobRequests\JobRequestController;
use App\Http\Controllers\JobRequests\JobRequestTransitionController;
use App\Http\Controllers\NotificationController;
use App\Http\Controllers\PublicVacancyController;
use App\Http\Controllers\Selection\FinalDecisionController;
use App\Http\Controllers\Selection\SelectionRegistrationController;
use App\Http\Controllers\Selection\VacancyClosureController;
use App\Http\Controllers\Selection\VacancyComparisonController;
use App\Http\Controllers\Vacancies\VacancyController;
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
});

require __DIR__.'/settings.php';
