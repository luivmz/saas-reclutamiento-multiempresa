<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('interviews', function (Blueprint $table) {
            $table->id();
            $table->foreignId('organization_id')->constrained()->restrictOnDelete();
            $table->foreignId('application_id')->constrained()->restrictOnDelete();
            $table->foreignId('evaluator_id')->constrained('users')->restrictOnDelete();
            $table->foreignId('scheduled_by')->constrained('users')->restrictOnDelete();
            $table->string('modality', 20);
            $table->string('location', 200);
            $table->timestamp('scheduled_at');
            $table->unsignedSmallInteger('duration_minutes')->nullable();
            $table->text('instructions')->nullable();
            $table->string('status', 20)->default('programada');
            $table->string('outcome', 30)->nullable();
            $table->timestamp('invitation_sent_at')->nullable();
            $table->timestamp('completed_at')->nullable();
            $table->text('observations')->nullable();
            $table->timestamps();

            $table->index('application_id');
            $table->index(['evaluator_id', 'status']);
            $table->index(['organization_id', 'scheduled_at']);
        });

        DB::statement("ALTER TABLE interviews ADD CONSTRAINT interviews_modality_valid CHECK (modality IN ('presencial', 'virtual'))");
        DB::statement('ALTER TABLE interviews ADD CONSTRAINT interviews_duration_range CHECK (duration_minutes IS NULL OR duration_minutes BETWEEN 15 AND 480)');
        DB::statement("ALTER TABLE interviews ADD CONSTRAINT interviews_outcome_valid CHECK (outcome IS NULL OR outcome IN ('recomendado', 'recomendado_con_reservas', 'no_recomendado'))");
        DB::statement("ALTER TABLE interviews ADD CONSTRAINT interviews_status_consistent CHECK ((status = 'programada' AND completed_at IS NULL AND outcome IS NULL) OR (status = 'realizada' AND completed_at IS NOT NULL AND outcome IS NOT NULL))");

        Schema::create('interview_results', function (Blueprint $table) {
            $table->id();
            $table->foreignId('organization_id')->constrained()->restrictOnDelete();
            $table->foreignId('interview_id')->constrained()->cascadeOnDelete();
            $table->foreignId('evaluation_criterion_id')->constrained('evaluation_criteria')->restrictOnDelete();
            $table->decimal('score', 6, 2);
            $table->string('comment', 500)->nullable();
            $table->timestamps();

            $table->unique(['interview_id', 'evaluation_criterion_id']);
        });

        DB::statement('ALTER TABLE interview_results ADD CONSTRAINT interview_results_score_non_negative CHECK (score >= 0)');
    }

    public function down(): void
    {
        Schema::dropIfExists('interview_results');
        Schema::dropIfExists('interviews');
    }
};
