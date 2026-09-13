<?php

namespace App\Http\Controllers\Candidates;

use App\Http\Controllers\Controller;
use App\Http\Requests\Candidates\CandidateCvRequest;
use App\Http\Support\Toast;
use App\Services\Candidates\CandidateProfileService;
use Illuminate\Http\RedirectResponse;

class CandidateCvController extends Controller
{
    public function __invoke(CandidateCvRequest $request, CandidateProfileService $profiles): RedirectResponse
    {
        $profiles->storeCv($request->user(), $request->file('cv'));
        Toast::success('CV cargado correctamente.');

        return back();
    }
}
