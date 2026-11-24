<?php

namespace App\Http\Requests\Vacancies;

use App\Enums\ContractType;
use App\Enums\VacancyStatus;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;

/**
 * Búsqueda y filtros del listado público de convocatorias (RF-07).
 *
 * Mismo patrón que RecruitmentReportRequest: un valor no válido devuelve al listado completo, con el aviso
 * visible, en lugar de ignorarse en silencio y mostrar resultados que parecerían filtrados. La organización y la
 * ubicación solo se aceptan si aparecen en alguna convocatoria publicada, las únicas que el listado muestra: un
 * identificador o una ubicación que solo existen en borradores o en vacantes cerradas se rechazan igual que uno
 * inexistente, sin revelar nada de ellas.
 */
class PublicVacancyFilterRequest extends FormRequest
{
    public const MAX_SEARCH = 150;

    protected $redirectRoute = 'jobs.index';

    public function authorize(): bool
    {
        return true;
    }

    /**
     * @return array<string, array<mixed>>
     */
    public function rules(): array
    {
        $published = VacancyStatus::Published->value;

        return [
            'q' => ['nullable', 'string', 'max:'.self::MAX_SEARCH],
            // `bail`: con un valor no numérico, la consulta de `exists` no llega a ejecutarse.
            'organizacion' => ['bail', 'nullable', 'integer', 'min:1', Rule::exists('vacancies', 'organization_id')->where('status', $published)],
            'ubicacion' => ['bail', 'nullable', 'string', 'max:120', Rule::exists('vacancies', 'location')->where('status', $published)],
            'contrato' => ['bail', 'nullable', Rule::enum(ContractType::class), Rule::exists('vacancies', 'contract_type')->where('status', $published)],
            'page' => ['nullable', 'integer', 'between:1,2147483647'],
        ];
    }

    /**
     * @return array<string, string>
     */
    public function messages(): array
    {
        return [
            'q.string' => 'La búsqueda indicada no es válida.',
            'q.max' => 'La búsqueda admite hasta '.self::MAX_SEARCH.' caracteres.',
            'organizacion.integer' => 'La organización indicada no es válida.',
            'organizacion.min' => 'La organización indicada no es válida.',
            'organizacion.exists' => 'La organización indicada no tiene convocatorias publicadas.',
            'ubicacion.string' => 'La ubicación indicada no es válida.',
            'ubicacion.max' => 'La ubicación indicada no es válida.',
            'ubicacion.exists' => 'La ubicación indicada no tiene convocatorias publicadas.',
            'contrato' => 'El tipo de contrato indicado no está disponible.',
            'page' => 'El número de página indicado no es válido.',
        ];
    }

    /**
     * Criterios ya validados, con «sin filtro» como cadena vacía o null.
     *
     * @return array{q: string, organizacion: int|null, ubicacion: string|null, contrato: string|null}
     */
    public function criteria(): array
    {
        $valid = $this->validated();

        return [
            'q' => trim((string) ($valid['q'] ?? '')),
            'organizacion' => isset($valid['organizacion']) ? (int) $valid['organizacion'] : null,
            'ubicacion' => $valid['ubicacion'] ?? null,
            'contrato' => $valid['contrato'] ?? null,
        ];
    }
}
