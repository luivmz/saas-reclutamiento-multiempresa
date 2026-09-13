<?php

use App\Http\Controllers\JobRequests\JobRequestController;
use App\Http\Controllers\JobRequests\JobRequestTransitionController;
use App\Http\Controllers\PublicVacancyController;
use App\Http\Controllers\Vacancies\VacancyController;
use App\Http\Controllers\Vacancies\VacancyPublicationController;
use Illuminate\Support\Facades\Route;

Route::inertia('/', 'welcome')->name('home');

Route::get('empleos', [PublicVacancyController::class, 'index'])->name('jobs.index');
Route::get('empleos/{vacancy}', [PublicVacancyController::class, 'show'])->whereNumber('vacancy')->name('jobs.show');

Route::middleware(['auth'])->group(function () {
    Route::inertia('dashboard', 'dashboard')->name('dashboard');

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

    Route::resource('vacantes', VacancyController::class)
        ->except('destroy')
        ->parameters(['vacantes' => 'vacancy'])
        ->names('vacancies');

    Route::post('vacantes/{vacancy}/publicar', VacancyPublicationController::class)->name('vacancies.publish');
});

require __DIR__.'/settings.php';
