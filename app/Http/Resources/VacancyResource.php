<?php

namespace App\Http\Resources;

use App\Models\EvaluationCriterion;
use App\Models\Vacancy;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

/**
 * @mixin Vacancy
 */
class VacancyResource extends JsonResource
{
    /**
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'code' => $this->code,
            'title' => $this->title,
            'summary' => $this->summary,
            'location' => $this->location,
            'contract_type' => $this->contract_type->present(),
            'positions' => $this->positions,
            'opens_at' => $this->opens_at?->toDateString(),
            'closes_at' => $this->closes_at?->toDateString(),
            'status' => $this->status->present(),
            'published_at' => $this->published_at?->toIso8601String(),
            'closed_at' => $this->closed_at?->toIso8601String(),
            'closure_type' => $this->closure_type?->present(),
            'closure_notes' => $this->closure_notes,
            'accepts_applications' => $this->acceptsApplications(),
            'organization' => $this->whenLoaded('organization', fn () => ['id' => $this->organization->id, 'name' => $this->organization->name]),
            'job_request' => $this->whenLoaded('jobRequest', fn () => [
                'id' => $this->jobRequest->id,
                'code' => $this->jobRequest->code,
                'area' => $this->jobRequest->area,
                'headcount' => $this->jobRequest->headcount,
            ]),
            'profile' => $this->whenLoaded('profile', fn () => $this->profile?->only(['education', 'experience', 'functions', 'competencies'])),
            'criteria' => $this->whenLoaded('criteria', fn () => $this->criteria->map(fn (EvaluationCriterion $criterion) => [
                'id' => $criterion->id,
                'name' => $criterion->name,
                'stage' => $criterion->stage->present(),
                'weight' => $criterion->weight,
                'min_score' => $criterion->min_score,
                'max_score' => $criterion->max_score,
            ])->all()),
            'applications_count' => $this->whenCounted('applications'),
        ];
    }
}
