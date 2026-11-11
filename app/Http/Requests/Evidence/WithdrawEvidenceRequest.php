<?php

namespace App\Http\Requests\Evidence;

/**
 * retirar (F37 §3): leaves the evidence without effect, with a fictitious reason. The row stays in the history.
 */
class WithdrawEvidenceRequest extends EvidenceWriteRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('withdraw', $this->route('evidence'));
    }

    /**
     * @return array<string, array<mixed>>
     */
    public function rules(): array
    {
        return [
            'reason' => ['required', 'string', 'max:500', 'starts_with:'.self::SYNTHETIC_PREFIX, self::NO_URL],
        ];
    }
}
