<?php

namespace App\Http\Requests\Evidence;

use App\Enums\EvidenceSource;
use App\Enums\EvidenceType;
use App\Models\EvidenceItem;
use Illuminate\Validation\Rule;
use Illuminate\Validation\Validator;

/**
 * registrar (F37 §3): a person declares type, source and a fictitious description.
 */
class StoreEvidenceRequest extends EvidenceWriteRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('create', [EvidenceItem::class, $this->route('application')]);
    }

    /**
     * @return array<string, array<mixed>>
     */
    public function rules(): array
    {
        return [
            'type' => ['required', Rule::enum(EvidenceType::class)],
            'source' => ['required', Rule::enum(EvidenceSource::class)],
            'description' => ['required', 'string', 'max:2000', 'starts_with:'.self::SYNTHETIC_PREFIX, self::NO_URL],
        ];
    }

    protected function additionalChecks(): array
    {
        return [function (Validator $validator): void {
            $type = EvidenceType::tryFrom((string) $this->input('type'));
            $source = EvidenceSource::tryFrom((string) $this->input('source'));

            if ($type === null || $source === null) {
                return;
            }

            if (! in_array($type, EvidenceType::registrableBy($this->user()->role), true)) {
                $validator->errors()->add('type', 'Tu rol no puede registrar evidencias de este tipo.');
            }

            if ($type->source() !== $source) {
                $validator->errors()->add('source', "Un registro de tipo «{$type->label()}» solo admite la fuente «{$type->source()->label()}» (R-09).");
            }
        }];
    }

    public function evidenceType(): EvidenceType
    {
        return EvidenceType::from($this->validated('type'));
    }

    public function evidenceSource(): EvidenceSource
    {
        return EvidenceSource::from($this->validated('source'));
    }
}
