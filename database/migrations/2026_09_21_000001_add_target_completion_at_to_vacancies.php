<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schema;

/**
 * GAP-01: plazo objetivo de cierre del proceso de selección.
 *
 * `ML-FEAT-02` (`days_remaining_to_target`) es la única feature del núcleo sin
 * equivalente en el sistema. El contrato la aprobó para el dataset sintético y
 * dejó anotado que Laravel no tenía fuente, lo que bloqueaba el despliegue del
 * modelo. Esta migración crea esa fuente.
 *
 * Tres decisiones de diseño, todas con consecuencias:
 *
 * 1. **Vive en `vacancies`.** La unidad que el modelo puntúa es el proceso de
 *    la vacante, y aquí están ya `published_at`, `closes_at` y `positions`.
 *    `job_requests.required_by` quedó **descartado** como origen por la Fase 14:
 *    es la fecha en que el área pide cubrir el puesto, no un compromiso
 *    operativo de cierre del proceso.
 * 2. **Es nullable y no se rellena.** Las vacantes existentes no tienen plazo y
 *    **no se les inventa uno**: quedan sin predicción y con el panel
 *    descriptivo. Fabricar un valor por retrocompatibilidad contaminaría la
 *    única feature que justifica esta fase.
 * 3. **Debe ser posterior a `closes_at`.** El plazo de cierre del proceso no
 *    puede caer antes de que termine la recepción de postulaciones. El `CHECK`
 *    lo impone en la base, no solo en el FormRequest.
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::table('vacancies', function (Blueprint $table) {
            $table->timestamp('target_completion_at')->nullable()->after('closes_at');
        });

        DB::statement(
            'ALTER TABLE vacancies ADD CONSTRAINT vacancies_target_after_close CHECK ('
            .'target_completion_at IS NULL OR closes_at IS NULL '
            .'OR target_completion_at > closes_at'
            .')'
        );
    }

    public function down(): void
    {
        DB::statement('ALTER TABLE vacancies DROP CONSTRAINT IF EXISTS vacancies_target_after_close');

        Schema::table('vacancies', function (Blueprint $table) {
            $table->dropColumn('target_completion_at');
        });
    }
};
