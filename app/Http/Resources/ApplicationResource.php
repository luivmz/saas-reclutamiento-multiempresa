<?php

namespace App\Http\Resources;

use App\Models\Application;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

/**
 * @mixin Application
 */
class ApplicationResource extends JsonResource
{
    /**
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'code' => $this->trackingCode(),
            'status' => $this->status->present(),
            'applied_at' => $this->applied_at->toIso8601String(),
            'stage_changed_at' => $this->stage_changed_at?->toIso8601String(),
            'vacancy' => $this->whenLoaded('vacancy', fn () => [
                'id' => $this->vacancy->id,
                'code' => $this->vacancy->code,
                'title' => $this->vacancy->title,
                'status' => $this->vacancy->status->present(),
                'organization' => $this->vacancy->relationLoaded('organization') ? $this->vacancy->organization->name : null,
            ]),
            'candidate' => $this->whenLoaded('candidate', fn () => [
                'id' => $this->candidate->id,
                'name' => $this->candidate->name,
                'email' => $this->candidate->email,
                'profile' => $this->candidate->relationLoaded('candidateProfile') && $this->candidate->candidateProfile !== null ? [
                    'phone' => $this->candidate->candidateProfile->phone,
                    'city' => $this->candidate->candidateProfile->city,
                    'education_level' => $this->candidate->candidateProfile->education_level?->present(),
                    'professional_title' => $this->candidate->candidateProfile->professional_title,
                    'years_of_experience' => $this->candidate->candidateProfile->years_of_experience,
                    'summary' => $this->candidate->candidateProfile->summary,
                ] : null,
            ]),
            'cv' => $this->whenLoaded('cvDocument', fn () => $this->cvDocument?->toSummary()),
        ];
    }
}
