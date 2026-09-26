<?php

namespace App\Services\Ml;

/**
 * Las 15 features operacionales que el servicio de riesgo espera, y nada más.
 *
 * El orden de las claves no importa para el servicio -- reindexa por su propio
 * `feature_order` --, pero sí importa que el conjunto sea **exactamente** este:
 * el contrato de la API rechaza cualquier campo desconocido, y eso es
 * deliberado. Es la frontera que impide que un identificador o un atributo
 * personal se cuele en el payload.
 *
 * Ninguna de estas features describe a una persona. Son conteos y diferencias
 * de días del proceso.
 */
final class OperationalRiskFeatures
{
    /**
     * @var list<string> Nombres canónicos, en el orden del contrato de features.
     */
    public const NAMES = [
        'elapsed_days_since_publication',
        'application_window_days',
        'positions_count',
        'applications_received_count',
        'configured_criteria_count',
        'evaluations_scheduled_count',
        'evaluations_completed_count',
        'evaluations_overdue_pending_count',
        'interviews_scheduled_count',
        'interviews_completed_count',
        'interviews_overdue_pending_count',
        'stage_transition_count',
        'days_since_last_operational_event',
        'concurrent_open_vacancies_count',
        'days_remaining_to_target',
    ];

    /**
     * @param  array<string, int>  $values
     */
    private function __construct(public readonly array $values) {}

    /**
     * @param  array<string, int>  $values
     *
     * @throws \InvalidArgumentException si sobra o falta alguna feature.
     */
    public static function fromArray(array $values): self
    {
        $missing = array_values(array_diff(self::NAMES, array_keys($values)));
        $unexpected = array_values(array_diff(array_keys($values), self::NAMES));

        if ($missing !== [] || $unexpected !== []) {
            throw new \InvalidArgumentException(sprintf(
                'El conjunto de features no cumple el contrato (faltan: %s; sobran: %s).',
                $missing === [] ? '-' : implode(', ', $missing),
                $unexpected === [] ? '-' : implode(', ', $unexpected),
            ));
        }

        $normalised = [];
        foreach (self::NAMES as $name) {
            $normalised[$name] = (int) $values[$name];
        }

        return new self($normalised);
    }

    /**
     * Payload listo para el servicio.
     *
     * @return array<string, int>
     */
    public function toPayload(): array
    {
        return $this->values;
    }

    public function get(string $name): int
    {
        return $this->values[$name] ?? throw new \InvalidArgumentException("Feature desconocida: {$name}");
    }
}
