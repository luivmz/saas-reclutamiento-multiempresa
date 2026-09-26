<?php

namespace App\Providers;

use App\Models\Application;
use App\Models\CandidateDocument;
use App\Models\CandidateProfile;
use App\Models\Evaluation;
use App\Models\Interview;
use App\Models\JobRequest;
use App\Models\Organization;
use App\Models\SelectionDecision;
use App\Models\User;
use App\Models\Vacancy;
use App\Services\Evaluation\WeightingValidator;
use Illuminate\Support\Facades\Route;
use Carbon\CarbonImmutable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\Relation;
use Illuminate\Http\Resources\Json\JsonResource;
use Illuminate\Support\Facades\Date;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\ServiceProvider;
use Illuminate\Validation\Rules\Password;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        $this->app->bind(WeightingValidator::class, fn () => new WeightingValidator(config('recruitment.weights.required_total')));
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        $this->configureDefaults();
    }

    /**
     * Configure default behaviors for production-ready applications.
     */
    protected function configureDefaults(): void
    {
        Date::use(CarbonImmutable::class);

        Model::shouldBeStrict(! app()->isProduction());

        JsonResource::withoutWrapping();

        Relation::enforceMorphMap([
            'user' => User::class,
            'organization' => Organization::class,
            'job_request' => JobRequest::class,
            'vacancy' => Vacancy::class,
            'candidate_profile' => CandidateProfile::class,
            'candidate_document' => CandidateDocument::class,
            'application' => Application::class,
            'evaluation' => Evaluation::class,
            'interview' => Interview::class,
            'selection_decision' => SelectionDecision::class,
        ]);

        Route::resourceVerbs(['create' => 'crear', 'edit' => 'editar']);

        // Los identificadores de los modelos son `bigint`: un segmento no numérico
        // (p. ej. `/requerimientos/create`) no debe llegar a PostgreSQL, donde
        // provocaba un error 22P02 y un 500. Sin coincidencia de ruta responde 404.
        Route::patterns([
            'application' => '[0-9]+',
            'document' => '[0-9]+',
            'evaluation' => '[0-9]+',
            'interview' => '[0-9]+',
            'jobRequest' => '[0-9]+',
            'vacancy' => '[0-9]+',
        ]);

        DB::prohibitDestructiveCommands(
            app()->isProduction(),
        );

        Password::defaults(fn (): ?Password => app()->isProduction()
            ? Password::min(12)
                ->mixedCase()
                ->letters()
                ->numbers()
                ->symbols()
                ->uncompromised()
            : null,
        );
    }
}
