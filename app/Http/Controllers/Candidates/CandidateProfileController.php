<?php

namespace App\Http\Controllers\Candidates;

use App\Enums\EducationLevel;
use App\Http\Controllers\Controller;
use App\Http\Requests\Candidates\CandidateCvRequest;
use App\Http\Requests\Candidates\CandidateProfileRequest;
use App\Http\Support\ConvocatoriaDeRetorno;
use App\Http\Support\Toast;
use App\Models\CandidateProfile;
use App\Services\Candidates\CandidateProfileService;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Inertia\Inertia;
use Inertia\Response;

class CandidateProfileController extends Controller
{
    public function __construct(private readonly CandidateProfileService $profiles) {}

    public function edit(Request $request, ConvocatoriaDeRetorno $retorno): Response
    {
        // Desde el detalle de una convocatoria llega `?convocatoria=ID`; sin parámetro se conserva la que ya había.
        $retorno->capturar($request, olvidarSinParametro: false);
        $profile = CandidateProfile::query()->with('latestCv')->where('user_id', $request->user()->id)->first();

        return Inertia::render('candidate/profile', [
            'profile' => $profile === null ? null : [
                'phone' => $profile->phone,
                'city' => $profile->city,
                'education_level' => $profile->education_level?->value,
                'professional_title' => $profile->professional_title,
                'years_of_experience' => $profile->years_of_experience,
                'summary' => $profile->summary,
            ],
            'cv' => $profile?->latestCv?->toSummary(),
            'missingFields' => $profile?->missingFields() ?? array_values(CandidateProfile::REQUIRED_FIELDS),
            'educationLevels' => EducationLevel::options(),
            'cvMaxKb' => CandidateCvRequest::maxKilobytes(),
            'retorno' => $this->retorno($request, $retorno),
        ]);
    }

    public function update(CandidateProfileRequest $request): RedirectResponse
    {
        $this->profiles->update($request->user(), $request->validated());
        Toast::success('Perfil actualizado.');

        return back();
    }

    /**
     * Convocatoria a la que el postulante podrá volver cuando su perfil esté completo. Si dejó de estar publicada
     * se avisa sin revelar su título y se descarta.
     *
     * @return array<string, mixed>|null
     */
    private function retorno(Request $request, ConvocatoriaDeRetorno $retorno): ?array
    {
        $estado = $retorno->estado($request);

        if ($estado === null) {
            return null;
        }

        if (! $estado['disponible']) {
            $retorno->olvidar($request);

            return ['disponible' => false];
        }

        $vacante = $estado['vacante'];

        return [
            'disponible' => true,
            'id' => $vacante->id,
            'title' => $vacante->title,
            'accepts_applications' => $vacante->acceptsApplications(),
            'application_deadline_passed' => $vacante->applicationDeadlinePassed(),
            'closes_at' => $vacante->closes_at?->toDateString(),
        ];
    }
}
