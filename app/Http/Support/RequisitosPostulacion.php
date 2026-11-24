<?php

namespace App\Http\Support;

use App\Http\Requests\Candidates\CandidateCvRequest;
use App\Models\CandidateProfile;

/**
 * Lo que se exige para poder postular a cualquier convocatoria, tomado de las mismas reglas que lo validan:
 * los campos obligatorios del perfil (CandidateProfile::REQUIRED_FIELDS) y el CV (CandidateCvRequest).
 * Los requisitos propios de cada convocatoria (formación, experiencia, funciones y criterios) van aparte,
 * en su detalle.
 */
final class RequisitosPostulacion
{
    /**
     * @return array{perfil: list<string>, cv: array{formato: string, max_kb: int}}
     */
    public static function toArray(): array
    {
        return [
            'perfil' => array_values(CandidateProfile::REQUIRED_FIELDS),
            'cv' => ['formato' => 'PDF', 'max_kb' => CandidateCvRequest::maxKilobytes()],
        ];
    }
}
