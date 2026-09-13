<?php

namespace App\Http\Resources;

use App\Models\JobRequest;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

/**
 * @mixin JobRequest
 */
class JobRequestResource extends JsonResource
{
    /**
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'code' => $this->code,
            'position_title' => $this->position_title,
            'area' => $this->area,
            'headcount' => $this->headcount,
            'contract_type' => $this->contract_type->present(),
            'justification' => $this->justification,
            'required_by' => $this->required_by?->toDateString(),
            'status' => $this->status->present(),
            'observation' => $this->observation,
            'decision_comment' => $this->decision_comment,
            'submitted_at' => $this->submitted_at?->toIso8601String(),
            'validated_at' => $this->validated_at?->toIso8601String(),
            'decided_at' => $this->decided_at?->toIso8601String(),
            'created_at' => $this->created_at->toIso8601String(),
            'requester' => $this->whenLoaded('requester', fn () => ['id' => $this->requester->id, 'name' => $this->requester->name]),
            'vacancy' => $this->whenLoaded('vacancy', fn () => $this->vacancy === null ? null : [
                'id' => $this->vacancy->id,
                'code' => $this->vacancy->code,
                'status' => $this->vacancy->status->present(),
            ]),
        ];
    }
}
