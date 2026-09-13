<?php

namespace App\Http\Controllers\Candidates;

use App\Enums\EducationLevel;
use App\Http\Controllers\Controller;
use App\Http\Requests\Candidates\CandidateProfileRequest;
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

    public function edit(Request $request): Response
    {
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
            'cvMaxKb' => (int) config('recruitment.cv.max_kb'),
        ]);
    }

    public function update(CandidateProfileRequest $request): RedirectResponse
    {
        $this->profiles->update($request->user(), $request->validated());
        Toast::success('Perfil actualizado.');

        return back();
    }
}
