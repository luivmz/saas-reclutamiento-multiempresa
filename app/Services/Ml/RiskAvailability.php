<?php

namespace App\Services\Ml;

/**
 * En qué situación queda la estimación de riesgo de un proceso.
 *
 * Los tres estados son excluyentes y ninguno inventa un número: cuando no hay
 * predicción **no hay score**, ni cero ni valor neutro. Un cero se leería como
 * "riesgo nulo" y sería una afirmación que nadie ha medido.
 */
enum RiskAvailability: string
{
    /** Hay estimación válida del servicio, verificada contra el experimento aprobado. */
    case PredictiveAvailable = 'predictive_available';

    /**
     * El proceso queda fuera del alcance del modelo, o falta el plazo
     * objetivo. Se muestra el panel descriptivo y el flujo sigue igual.
     */
    case DescriptiveOnly = 'descriptive_only';

    /** El servicio no respondió, o respondió algo que no puede aceptarse. */
    case Unavailable = 'unavailable';

    public function label(): string
    {
        return match ($this) {
            self::PredictiveAvailable => 'Estimación disponible',
            self::DescriptiveOnly => 'Solo información descriptiva',
            self::Unavailable => 'Servicio no disponible',
        };
    }
}
