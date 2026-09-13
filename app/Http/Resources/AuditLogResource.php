<?php

namespace App\Http\Resources;

use App\Models\AuditLog;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

/**
 * Safe projection of an audit record: raw metadata, IP address and free-text comments are never exposed.
 *
 * @mixin AuditLog
 */
class AuditLogResource extends JsonResource
{
    private const ENTITY_LABELS = [
        'organization' => 'Organización',
        'user' => 'Usuario',
        'job_request' => 'Requerimiento',
        'vacancy' => 'Vacante',
        'candidate_profile' => 'Perfil de postulante',
        'candidate_document' => 'Documento de postulante',
        'application' => 'Postulación',
        'evaluation' => 'Evaluación',
        'interview' => 'Entrevista',
        'selection_decision' => 'Decisión final',
    ];

    private const SAFE_DETAILS = [
        'code' => 'Código',
        'job_request' => 'Requerimiento',
        'vacancy' => 'Vacante',
        'from' => 'Estado anterior',
        'to' => 'Estado nuevo',
        'fields' => 'Campos modificados',
        'type' => 'Tipo',
        'scheduled_at' => 'Fecha programada',
        'criteria' => 'Criterios registrados',
        'outcome' => 'Resultado',
        'application_id' => 'Postulación',
        'selected_application_id' => 'Postulación seleccionada',
        'selected_position' => 'Posición del elegido al decidir',
        'ranked_candidates' => 'Candidatos en el ranking',
        'closure_type' => 'Tipo de cierre',
        'selected' => 'Seleccionados notificados',
        'not_selected' => 'No seleccionados',
        'channel' => 'Canal',
    ];

    /**
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'created_at' => $this->created_at->toIso8601String(),
            'actor' => $this->user?->name ?? 'Sistema',
            'action' => $this->action->present(),
            'entity' => [
                'type' => $this->auditable_type,
                'label' => self::ENTITY_LABELS[$this->auditable_type] ?? $this->auditable_type,
                'id' => $this->auditable_id,
            ],
            'details' => $this->safeDetails(),
        ];
    }

    /**
     * @return list<array{label: string, value: string}>
     */
    private function safeDetails(): array
    {
        $details = [];

        foreach (self::SAFE_DETAILS as $key => $label) {
            $value = $this->metadata[$key] ?? null;

            if ($value === null || $value === '' || $value === []) {
                continue;
            }

            $details[] = [
                'label' => $label,
                'value' => is_array($value) ? implode(', ', array_map('strval', $value)) : (string) $value,
            ];
        }

        return $details;
    }
}
