<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('applications', function (Blueprint $table) {
            $table->id();
            $table->foreignId('organization_id')->constrained()->restrictOnDelete();
            $table->foreignId('vacancy_id')->constrained()->restrictOnDelete();
            $table->foreignId('candidate_id')->constrained('users')->restrictOnDelete();
            $table->foreignId('candidate_document_id')->nullable()->constrained()->restrictOnDelete();
            $table->string('status', 20)->default('postulado');
            $table->timestamp('applied_at');
            $table->timestamp('stage_changed_at')->nullable();
            $table->timestamps();

            $table->unique(['vacancy_id', 'candidate_id']);
            $table->index(['organization_id', 'status']);
            $table->index(['vacancy_id', 'status']);
            $table->index('candidate_id');
        });

        DB::statement("ALTER TABLE applications ADD CONSTRAINT applications_status_valid CHECK (status IN ('postulado', 'preseleccionado', 'en_evaluacion', 'en_entrevista', 'finalista', 'seleccionado', 'no_seleccionado', 'descartado'))");

        Schema::create('application_stage_histories', function (Blueprint $table) {
            $table->id();
            $table->foreignId('organization_id')->constrained()->restrictOnDelete();
            $table->foreignId('application_id')->constrained()->cascadeOnDelete();
            $table->string('from_status', 20)->nullable();
            $table->string('to_status', 20);
            $table->foreignId('changed_by')->constrained('users')->restrictOnDelete();
            $table->text('comment')->nullable();
            $table->timestamp('created_at')->useCurrent();

            $table->index(['application_id', 'created_at']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('application_stage_histories');
        Schema::dropIfExists('applications');
    }
};
