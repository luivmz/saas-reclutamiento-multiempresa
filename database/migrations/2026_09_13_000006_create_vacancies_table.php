<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('vacancies', function (Blueprint $table) {
            $table->id();
            $table->foreignId('organization_id')->constrained()->restrictOnDelete();
            $table->foreignId('job_request_id')->unique()->constrained()->restrictOnDelete();
            $table->string('code', 20);
            $table->string('title', 150);
            $table->text('summary');
            $table->string('location', 120);
            $table->string('contract_type', 20);
            $table->unsignedSmallInteger('positions');
            $table->date('opens_at')->nullable();
            $table->date('closes_at')->nullable();
            $table->string('status', 20)->default('borrador');
            $table->foreignId('created_by')->constrained('users')->restrictOnDelete();
            $table->foreignId('published_by')->nullable()->constrained('users')->nullOnDelete();
            $table->timestamp('published_at')->nullable();
            $table->foreignId('closed_by')->nullable()->constrained('users')->nullOnDelete();
            $table->timestamp('closed_at')->nullable();
            $table->string('closure_type', 20)->nullable();
            $table->text('closure_notes')->nullable();
            $table->timestamps();

            $table->unique(['organization_id', 'code']);
            $table->index(['organization_id', 'status']);
            $table->index(['status', 'closes_at']);
        });

        DB::statement('ALTER TABLE vacancies ADD CONSTRAINT vacancies_positions_positive CHECK (positions >= 1)');
        DB::statement('ALTER TABLE vacancies ADD CONSTRAINT vacancies_dates_consistent CHECK (opens_at IS NULL OR closes_at IS NULL OR closes_at >= opens_at)');
        DB::statement("ALTER TABLE vacancies ADD CONSTRAINT vacancies_status_valid CHECK (status IN ('borrador', 'publicada', 'cerrada'))");
        DB::statement("ALTER TABLE vacancies ADD CONSTRAINT vacancies_closure_consistent CHECK ((status = 'cerrada' AND closed_at IS NOT NULL AND closure_type IN ('con_seleccion', 'desierta')) OR (status <> 'cerrada' AND closure_type IS NULL))");

        Schema::create('job_profiles', function (Blueprint $table) {
            $table->id();
            $table->foreignId('organization_id')->constrained()->restrictOnDelete();
            $table->foreignId('vacancy_id')->unique()->constrained()->cascadeOnDelete();
            $table->string('education', 200);
            $table->string('experience', 200);
            $table->text('functions');
            $table->text('competencies');
            $table->timestamps();
        });

        Schema::create('evaluation_criteria', function (Blueprint $table) {
            $table->id();
            $table->foreignId('organization_id')->constrained()->restrictOnDelete();
            $table->foreignId('vacancy_id')->constrained()->cascadeOnDelete();
            $table->string('name', 120);
            $table->string('stage', 20);
            $table->decimal('weight', 6, 2);
            $table->decimal('min_score', 6, 2);
            $table->decimal('max_score', 6, 2);
            $table->unsignedSmallInteger('position')->default(0);
            $table->timestamps();

            $table->unique(['vacancy_id', 'name']);
        });

        DB::statement('ALTER TABLE evaluation_criteria ADD CONSTRAINT evaluation_criteria_weight_positive CHECK (weight > 0)');
        DB::statement('ALTER TABLE evaluation_criteria ADD CONSTRAINT evaluation_criteria_range_valid CHECK (min_score >= 0 AND max_score > min_score)');
        DB::statement("ALTER TABLE evaluation_criteria ADD CONSTRAINT evaluation_criteria_stage_valid CHECK (stage IN ('evaluacion', 'entrevista'))");
    }

    public function down(): void
    {
        Schema::dropIfExists('evaluation_criteria');
        Schema::dropIfExists('job_profiles');
        Schema::dropIfExists('vacancies');
    }
};
