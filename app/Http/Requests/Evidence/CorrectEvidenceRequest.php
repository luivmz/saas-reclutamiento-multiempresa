<?php

namespace App\Http\Requests\Evidence;

use App\Enums\EvidenceSource;
use App\Enums\EvidenceType;
use App\Models\EvidenceItem;
use Illuminate\Validation\Rule;
use Illuminate\Validation\Validator;

/**
 * corregir (F37 §3): a new version that supersedes the current one. Authorization looks at the original evidence
 * (policy `correct`); the replacement is then validated like a new record of the same actor.
 */
class CorrectEvidenceRequest extends EvidenceWriteRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('correct', $this->evidence());
    }

    /**
     * @return array<string, array<mixed>>
     */
    public function rules(): array
    {
        return [
            'type' => ['sometimes', Rule::enum(EvidenceType::class)],
            'source' => ['required', Rule::enum(EvidenceSource::class)],
            'description' => ['required', 'string', 'max:2000', 'starts_with:'.self::SYNTHETIC_PREFIX, self::NO_URL],
        ];
    }

    protected function additionalChecks(): array
    {
        return [function (Validator $validator): void {
            $type = $this->has('type') ? EvidenceType::tryFrom((string) $this->input('type')) : $this->evidence()->type;
            $source = EvidenceSource::tryFrom((string) $this->input('source'));

            if ($type === null || $source === null) {
                return;
            }

            if (! in_array($type, EvidenceType::registrableBy($this->user()->role), true)) {
                $validator->errors()->add('type', 'Tu rol no puede declarar evidencias de este tipo.');
            }

            if ($type->source() !== $source) {
                $validator->errors()->add('source', "Un registro de tipo «{$type->label()}» solo admite la fuente «{$type->source()->label()}» (R-09).");
            }
        }];
    }

    public function evidence(): EvidenceItem
    {
        return $this->route('evidence');
    }

    public function evidenceType(): EvidenceType
    {
        return $this->has('type') ? EvidenceType::from($this->validated('type')) : $this->evidence()->type;
    }

    public function evidenceSource(): EvidenceSource
    {
        return EvidenceSource::from($this->validated('source'));
    }
}
