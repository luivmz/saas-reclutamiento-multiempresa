<?php

namespace App\Http\Requests\Evidence;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Validator;

/**
 * EXPERIMENTAL (F37 flow). Base of every evidence write.
 *
 * R-05: no write may carry a field about the person or a judgment. A field name is rejected when any of its words
 * (camelCase split too) is a forbidden token of the evidence contract v4 (`forbidden_field_tokens`). The list is
 * copied here and a test keeps it identical to the contract.
 */
abstract class EvidenceWriteRequest extends FormRequest
{
    public const FORBIDDEN_FIELD_TOKENS = [
        'name', 'dni', 'email', 'phone', 'address', 'photo', 'image', 'age', 'birth', 'gender', 'sex', 'nationality',
        'ethnicity', 'religion', 'health', 'disability', 'marital', 'score', 'rank', 'ranking', 'recommendation',
        'recommended', 'fit', 'suitability', 'best', 'verdict', 'emotion', 'personality', 'honesty', 'intelligence',
        'stress', 'nervousness', 'voice', 'face', 'prosody', 'accent', 'audio', 'video', 'biometric', 'level', 'hire',
        'hired', 'select', 'selected', 'discard', 'discarded',
    ];

    public const SYNTHETIC_PREFIX = '[SINTÉTICO]';

    /** R-09: closed input, no URL nor external source in the text. */
    protected const NO_URL = 'not_regex:/(https?:\/\/|www\.)/i';

    /**
     * @return list<string>
     */
    public static function fieldTokens(string $field): array
    {
        $spaced = preg_replace('/(?<=[a-z0-9])(?=[A-Z])/', '_', $field) ?? $field;

        return array_values(array_filter(preg_split('/[_\W]+/u', mb_strtolower($spaced)) ?: [], fn ($t) => $t !== ''));
    }

    /**
     * @return list<string>
     */
    public static function forbiddenFields(array $input, string $prefix = ''): array
    {
        $bad = [];

        foreach ($input as $key => $value) {
            $key = (string) $key;
            $path = $prefix === '' ? $key : "{$prefix}.{$key}";

            if (! str_starts_with($key, '_') && array_intersect(self::fieldTokens($key), self::FORBIDDEN_FIELD_TOKENS) !== []) {
                $bad[] = $path;
            }

            if (is_array($value)) {
                $bad = [...$bad, ...self::forbiddenFields($value, $path)];
            }
        }

        return $bad;
    }

    /**
     * @return array<int, callable(Validator): void>
     */
    public function after(): array
    {
        return [
            function (Validator $validator): void {
                foreach (self::forbiddenFields($this->all()) as $field) {
                    $validator->errors()->add('evidence', "Campo no admitido en una evidencia: {$field} (R-05).");
                }
            },
            ...$this->additionalChecks(),
        ];
    }

    /**
     * @return array<int, callable(Validator): void>
     */
    protected function additionalChecks(): array
    {
        return [];
    }

    /**
     * @return array<string, string>
     */
    public function messages(): array
    {
        return [
            'description.starts_with' => 'El texto debe empezar por [SINTÉTICO]: este entorno solo admite datos ficticios.',
            'reason.starts_with' => 'El motivo debe empezar por [SINTÉTICO]: este entorno solo admite datos ficticios.',
            'description.not_regex' => 'El texto no puede contener enlaces ni fuentes externas.',
            'reason.not_regex' => 'El motivo no puede contener enlaces ni fuentes externas.',
        ];
    }

    /**
     * @return array<string, string>
     */
    public function attributes(): array
    {
        return [
            'type' => 'tipo',
            'source' => 'fuente',
            'description' => 'descripción',
            'criterion_id' => 'criterio',
            'reason' => 'motivo',
        ];
    }
}
