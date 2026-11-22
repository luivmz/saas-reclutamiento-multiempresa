<?php

namespace App\Http\Requests\Evidence;

/**
 * desenlazar and revisar (F37 §3): no payload, but still a write, so R-05 applies to whatever is sent.
 * The route defines which policy ability is checked.
 */
class EvidenceActionRequest extends EvidenceWriteRequest
{
    public function authorize(): bool
    {
        $ability = $this->routeIs('evidence.review') ? 'review' : 'link';

        return $this->user()->can($ability, $this->route('evidence'));
    }

    /**
     * @return array<string, array<mixed>>
     */
    public function rules(): array
    {
        return [];
    }
}
