<?php

namespace App\Http\Controllers\Evidence;

use App\Http\Controllers\Controller;
use App\Http\Requests\Evidence\CorrectEvidenceRequest;
use App\Http\Requests\Evidence\EvidenceActionRequest;
use App\Http\Requests\Evidence\LinkEvidenceRequest;
use App\Http\Requests\Evidence\WithdrawEvidenceRequest;
use App\Http\Support\Toast;
use App\Models\EvidenceItem;
use App\Services\Evidence\EvidenceService;
use Illuminate\Http\RedirectResponse;

/**
 * EXPERIMENTAL (exp/evidencias-ml02). Writes on one evidence version: link, unlink, review, correct and withdraw.
 * Each one inserts a row (R-04); authorization lives in EvidenceItemPolicy through the form requests.
 */
class EvidenceItemController extends Controller
{
    public function __construct(private readonly EvidenceService $evidence) {}

    public function link(LinkEvidenceRequest $request, EvidenceItem $evidence): RedirectResponse
    {
        $this->evidence->link($request->user(), $evidence, (int) $request->validated('criterion_id'));
        Toast::success("Evidencia {$evidence->code()} enlazada al criterio.");

        return $this->back($evidence);
    }

    public function unlink(EvidenceActionRequest $request, EvidenceItem $evidence, int $criterion): RedirectResponse
    {
        $this->evidence->unlink($request->user(), $evidence, $criterion);
        Toast::success("Se retiró el enlace de {$evidence->code()}. El evento queda en el historial.");

        return $this->back($evidence);
    }

    public function review(EvidenceActionRequest $request, EvidenceItem $evidence): RedirectResponse
    {
        $this->evidence->review($request->user(), $evidence);
        Toast::success("Evidencia {$evidence->code()} revisada.");

        return $this->back($evidence);
    }

    public function correct(CorrectEvidenceRequest $request, EvidenceItem $evidence): RedirectResponse
    {
        $version = $this->evidence->correct($request->user(), $evidence, $request->evidenceType(), $request->evidenceSource(), $request->validated('description'));
        Toast::success("Se registró {$version->code()}, que sustituye a {$evidence->code()}. La versión anterior se conserva.");

        return $this->back($evidence);
    }

    public function withdraw(WithdrawEvidenceRequest $request, EvidenceItem $evidence): RedirectResponse
    {
        $this->evidence->withdraw($request->user(), $evidence, $request->validated('reason'));
        Toast::success("Evidencia {$evidence->code()} retirada. Sigue en el historial.");

        return $this->back($evidence);
    }

    private function back(EvidenceItem $evidence): RedirectResponse
    {
        return to_route('applications.evidence.index', $evidence->application_id);
    }
}
