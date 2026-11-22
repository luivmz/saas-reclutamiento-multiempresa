<?php

namespace App\Http\Requests\Evidence;

/**
 * enlazar (F37 §3). The criterion must belong to the vacancy of the application (R-03), checked by the service.
 */
class LinkEvidenceRequest extends EvidenceWriteRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('link', $this->route('evidence'));
    }

    /**
     * @return array<string, array<mixed>>
     */
    public function rules(): array
    {
        return [
            'criterion_id' => ['required', 'integer'],
        ];
    }
}
