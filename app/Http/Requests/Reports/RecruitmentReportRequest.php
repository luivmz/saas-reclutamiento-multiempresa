<?php

namespace App\Http\Requests\Reports;

use App\Enums\ApplicationStatus;
use App\Enums\VacancyStatus;
use Carbon\CarbonImmutable;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;
use Illuminate\Validation\Validator;

/**
 * RF-28 (candidato): filtros del módulo de reportes.
 *
 * El período por defecto son los últimos 90 días hasta hoy. La vacante debe
 * pertenecer a la organización del usuario y no estar en borrador.
 */
class RecruitmentReportRequest extends FormRequest
{
    public const DEFAULT_PERIOD_DAYS = 90;

    public const MAX_PERIOD_DAYS = 731;

    /**
     * Un filtro inválido devuelve al reporte sin filtros, con el error visible.
     */
    protected $redirectRoute = 'reports.index';

    public function authorize(): bool
    {
        return $this->user()?->can('viewRecruitmentReports') ?? false;
    }

    /**
     * @return array<string, array<mixed>>
     */
    public function rules(): array
    {
        return [
            'desde' => ['nullable', 'date_format:Y-m-d'],
            'hasta' => ['nullable', 'date_format:Y-m-d', 'after_or_equal:desde'],
            'vacante' => [
                'nullable',
                'integer',
                Rule::exists('vacancies', 'id')
                    ->where('organization_id', $this->user()->organization_id)
                    ->whereNot('status', VacancyStatus::Draft->value),
            ],
            'estado' => ['nullable', Rule::enum(ApplicationStatus::class)],
        ];
    }

    /**
     * @return array<int, callable>
     */
    public function after(): array
    {
        return [
            function (Validator $validator): void {
                if ($validator->errors()->hasAny(['desde', 'hasta'])) {
                    return;
                }

                [$from, $to] = $this->period();

                if ((int) $from->diffInDays($to->startOfDay()) + 1 > self::MAX_PERIOD_DAYS) {
                    $validator->errors()->add('desde', 'El período consultado no puede superar los dos años.');
                }
            },
        ];
    }

    /**
     * @return array<string, string>
     */
    public function attributes(): array
    {
        return [
            'desde' => 'fecha desde',
            'hasta' => 'fecha hasta',
            'vacante' => 'vacante',
            'estado' => 'etapa',
        ];
    }

    /**
     * @return array<string, string>
     */
    public function messages(): array
    {
        return [
            'desde.date_format' => 'Ingrese la fecha desde con el formato AAAA-MM-DD.',
            'hasta.date_format' => 'Ingrese la fecha hasta con el formato AAAA-MM-DD.',
            'hasta.after_or_equal' => 'La fecha hasta debe ser igual o posterior a la fecha desde.',
            'vacante.exists' => 'La vacante seleccionada no está disponible en su organización.',
            'estado.enum' => 'La etapa seleccionada no es válida.',
        ];
    }

    /**
     * Período inclusivo [desde 00:00, hasta 23:59:59] en la zona horaria de la aplicación.
     *
     * @return array{0: CarbonImmutable, 1: CarbonImmutable}
     */
    public function period(): array
    {
        $to = $this->filled('hasta')
            ? CarbonImmutable::createFromFormat('Y-m-d', (string) $this->input('hasta'))
            : CarbonImmutable::today();

        $from = $this->filled('desde')
            ? CarbonImmutable::createFromFormat('Y-m-d', (string) $this->input('desde'))
            : $to->subDays(self::DEFAULT_PERIOD_DAYS - 1);

        if (! $this->filled('hasta') && $from->greaterThan($to)) {
            $to = $from;
        }

        return [$from->startOfDay(), $to->endOfDay()];
    }

    public function vacancyId(): ?int
    {
        return $this->filled('vacante') ? (int) $this->input('vacante') : null;
    }

    public function status(): ?ApplicationStatus
    {
        return ApplicationStatus::tryFrom((string) $this->input('estado'));
    }
}
