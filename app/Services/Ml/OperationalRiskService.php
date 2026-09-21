<?php

namespace App\Services\Ml;

use App\Models\Vacancy;
use Carbon\CarbonInterface;
use Illuminate\Support\Carbon;

/**
 * Coordina la estimación de riesgo operacional de una vacante.
 *
 * Orden: comprobar que el proceso está dentro del alcance del modelo →
 * construir features → llamar al servicio → devolver un resultado validado.
 * El controlador no habla HTTP ni conoce features.
 *
 * Sobre el alcance del modelo
 * ---------------------------
 * El experimento de la Fase 15B observó **siempre** el mismo instante: el día
 * siguiente al cierre de postulaciones. Preguntar por un proceso en otro punto
 * de su vida es extrapolar fuera de lo que el modelo vio, y un número obtenido
 * así aparentaría el mismo rigor sin tenerlo. Por eso esta capa se niega a
 * estimar antes de que cierre la ventana de postulaciones y devuelve el panel
 * descriptivo.
 *
 * Es una restricción deliberada, no una limitación técnica: el equipo puede
 * revisarla si una fase futura entrena con checkpoints múltiples.
 */
class OperationalRiskService
{
    public const REASON_NOT_PUBLISHED = 'vacancy_not_published';

    public const REASON_MISSING_TARGET = 'missing_target_completion_at';

    public const REASON_TARGET_REACHED = 'target_completion_reached';

    public const REASON_WINDOW_OPEN = 'application_window_still_open';

    public function __construct(
        private readonly OperationalRiskFeatureBuilder $features,
        private readonly MlRiskClient $client,
    ) {}

    public function assess(Vacancy $vacancy, ?CarbonInterface $checkpoint = null): RiskAssessment
    {
        $at = Carbon::instance(($checkpoint ?? Carbon::now())->toDateTime())
            ->setTimezone(config('app.timezone'));

        $outOfScope = $this->outOfScopeReason($vacancy, $at);
        if ($outOfScope !== null) {
            return RiskAssessment::descriptive($outOfScope);
        }

        return $this->client->predict($this->features->build($vacancy, $at));
    }

    /**
     * Motivo por el que el proceso queda fuera del alcance del modelo, o
     * `null` si puede estimarse.
     */
    public function outOfScopeReason(Vacancy $vacancy, CarbonInterface $at): ?string
    {
        if ($vacancy->published_at === null) {
            return self::REASON_NOT_PUBLISHED;
        }

        // GAP-01: sin plazo objetivo no hay ML-FEAT-02, y no se inventa.
        if ($vacancy->target_completion_at === null) {
            return self::REASON_MISSING_TARGET;
        }

        if ($vacancy->closes_at !== null && $vacancy->closes_at->copy()->endOfDay()->gte($at)) {
            return self::REASON_WINDOW_OPEN;
        }

        // El contrato del servicio exige `days_remaining_to_target >= 1`. Un
        // plazo vencido no se recorta a uno: es un proceso que el modelo no
        // vio nunca, porque el dataset solo contiene plazos futuros.
        if ($this->features->daysRemainingToTarget($vacancy, $at) < 1) {
            return self::REASON_TARGET_REACHED;
        }

        return null;
    }

    /**
     * Texto en español para la interfaz. Tono neutro a propósito: la tasa de
     * alerta del modelo es alta (73.5 % en test) y presentar la señal como
     * alarma crítica sería desproporcionado.
     */
    public function explain(RiskAssessment $assessment): string
    {
        return match (true) {
            $assessment->isPredictive() => $assessment->flag
                ? 'Señal de riesgo para revisión. Conviene revisar el avance del proceso; no es una decisión ni una alarma.'
                : 'Sin señal de riesgo en este momento. El proceso avanza dentro de lo esperado por el modelo.',
            $assessment->reason === self::REASON_MISSING_TARGET => 'Sin plazo objetivo configurado: registra la fecha límite del proceso para habilitar la estimación.',
            $assessment->reason === self::REASON_TARGET_REACHED => 'El plazo objetivo ya venció. El modelo solo se entrenó con procesos dentro de plazo, así que no se estima riesgo.',
            $assessment->reason === self::REASON_WINDOW_OPEN => 'Las postulaciones siguen abiertas. El modelo observa el proceso tras el cierre, así que todavía no se estima riesgo.',
            $assessment->reason === self::REASON_NOT_PUBLISHED => 'La vacante aún no se publica: no hay proceso que estimar.',
            $assessment->reason === MlRiskClient::REASON_DISABLED => 'La estimación de riesgo está desactivada en este entorno.',
            $assessment->availability === RiskAvailability::Unavailable => 'El servicio de estimación no está disponible. Los indicadores descriptivos del proceso siguen vigentes.',
            default => 'Solo hay información descriptiva del proceso.',
        };
    }
}
