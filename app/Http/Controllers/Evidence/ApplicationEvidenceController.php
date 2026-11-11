<?php

namespace App\Http\Controllers\Evidence;

use App\Enums\AuditAction;
use App\Enums\EvidenceType;
use App\Http\Controllers\Controller;
use App\Http\Presenters\EvidencePresenter;
use App\Http\Requests\Evidence\StoreEvidenceRequest;
use App\Http\Support\Toast;
use App\Models\Application;
use App\Models\AuditLog;
use App\Models\EvaluationCriterion;
use App\Models\EvidenceItem;
use App\Services\Evidence\EvidenceLedger;
use App\Services\Evidence\EvidenceService;
use App\Services\Ml02\Bm25Retriever;
use App\Services\Ml02\DocumentaryAid;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;
use Inertia\Inertia;
use Inertia\Response;

/**
 * EXPERIMENTAL (exp/evidencias-ml02). Evidence of one application: consult, register and the ML-02 documentary
 * aid (fragments by criterion and search, with their sources), plus the audit history. Not the formal SaaS
 * integration (EI-23 sigue BLOCKED; requiere la G0 real, un ADR y la decisión N5).
 */
class ApplicationEvidenceController extends Controller
{
    public function __construct(
        private readonly EvidencePresenter $presenter,
        private readonly DocumentaryAid $aid,
    ) {}

    public function index(Request $request, Application $application): Response
    {
        Gate::authorize('viewAny', [EvidenceItem::class, $application]);

        $application->load('vacancy:id,organization_id,code,title,status');
        $user = $request->user();
        $ledger = EvidenceLedger::for($application);

        $criteria = EvaluationCriterion::query()
            ->where('vacancy_id', $application->vacancy_id)
            ->orderBy('position')
            ->orderBy('id')
            ->get(['id', 'vacancy_id', 'organization_id', 'name', 'stage', 'position'])
            ->keyBy('id');

        $selected = $criteria->get((int) $request->query('criterio'));
        $query = trim((string) $request->query('buscar', ''));
        $query = mb_substr($query, 0, 120);

        $aid = null;
        if ($selected !== null) {
            $result = $this->aid->byCriterion($ledger, $selected);
            $aid = [
                'criterion' => ['id' => $selected->id, 'name' => $selected->name],
                'method' => Bm25Retriever::METHOD_ID,
                'k' => DocumentaryAid::K,
                'query_terms' => $result['query_terms'],
                'abstained' => $result['abstained'],
                'results' => array_map(
                    fn (array $hit) => $this->presenter->fragment($ledger, $hit['item'], $hit['words']),
                    $result['hits'],
                ),
            ];
        }

        $search = $query === '' ? null : [
            'query' => $query,
            'results' => array_map(fn (EvidenceItem $item) => $this->presenter->fragment($ledger, $item), $this->aid->search($ledger, $query)),
        ];

        return Inertia::render('evidence/index', [
            'application' => [
                'id' => $application->id,
                'code' => $application->trackingCode(),
                'vacancy' => [
                    'id' => $application->vacancy->id,
                    'code' => $application->vacancy->code,
                    'title' => $application->vacancy->title,
                    'closed' => $application->vacancy->isClosed(),
                ],
            ],
            'records' => $this->presenter->records($ledger, $user, $criteria->all()),
            'criteria' => $criteria->map(fn (EvaluationCriterion $c) => ['value' => (string) $c->id, 'label' => $c->name])->values(),
            'registrableTypes' => array_map(fn (EvidenceType $type) => [
                ...$type->present(),
                'source' => $type->source()->present(),
            ], EvidenceType::registrableBy($user->role)),
            'aid' => $aid,
            'search' => $search,
            'filters' => ['criterio' => $selected?->id, 'buscar' => $query === '' ? null : $query],
            'can' => [
                'create' => $user->can('create', [EvidenceItem::class, $application]),
                'viewHistory' => $user->can('viewHistory', [EvidenceItem::class, $application]),
                'viewFile' => $user->can('viewFile', $application),
            ],
        ]);
    }

    public function history(Application $application): Response
    {
        Gate::authorize('viewHistory', [EvidenceItem::class, $application]);

        $application->load('vacancy:id,organization_id,code,title,status');
        $ids = EvidenceItem::query()->where('application_id', $application->id)->pluck('id');
        $criteria = EvaluationCriterion::query()->where('vacancy_id', $application->vacancy_id)->pluck('name', 'id');

        $logs = AuditLog::query()
            ->where('organization_id', $application->organization_id)
            ->where('auditable_type', (new EvidenceItem)->getMorphClass())
            ->whereIn('auditable_id', $ids)
            ->with('user:id,name,role')
            ->orderBy('created_at')
            ->orderBy('id')
            ->get();

        return Inertia::render('evidence/history', [
            'application' => [
                'id' => $application->id,
                'code' => $application->trackingCode(),
                'vacancy' => ['code' => $application->vacancy->code, 'title' => $application->vacancy->title],
            ],
            'entries' => $logs->map(fn (AuditLog $log) => [
                'id' => $log->id,
                'action' => $log->action instanceof AuditAction ? $log->action->present() : ['value' => (string) $log->action, 'label' => (string) $log->action, 'tone' => 'neutral'],
                'evidence' => 'EVD-'.str_pad((string) $log->auditable_id, 5, '0', STR_PAD_LEFT),
                'criterion' => isset($log->metadata['criterion_id']) ? ($criteria[$log->metadata['criterion_id']] ?? null) : null,
                'supersedes' => isset($log->metadata['supersedes_id']) ? 'EVD-'.str_pad((string) $log->metadata['supersedes_id'], 5, '0', STR_PAD_LEFT) : null,
                'actor' => $log->user ? ['name' => $log->user->name, 'role' => $log->user->role->label()] : null,
                'created_at' => $log->created_at->toIso8601String(),
            ])->values(),
        ]);
    }

    public function store(StoreEvidenceRequest $request, Application $application, EvidenceService $evidence): RedirectResponse
    {
        $item = $evidence->register($request->user(), $application, $request->evidenceType(), $request->evidenceSource(), $request->validated('description'));
        Toast::success("Evidencia {$item->code()} registrada.");

        return to_route('applications.evidence.index', $application);
    }
}
