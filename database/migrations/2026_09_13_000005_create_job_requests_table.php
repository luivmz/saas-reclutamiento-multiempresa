<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('job_requests', function (Blueprint $table) {
            $table->id();
            $table->foreignId('organization_id')->constrained()->restrictOnDelete();
            $table->foreignId('requested_by')->constrained('users')->restrictOnDelete();
            $table->string('code', 20);
            $table->string('position_title', 150);
            $table->string('area', 120);
            $table->unsignedSmallInteger('headcount');
            $table->string('contract_type', 20);
            $table->text('justification');
            $table->date('required_by')->nullable();
            $table->string('status', 20)->default('borrador');
            $table->text('observation')->nullable();
            $table->timestamp('submitted_at')->nullable();
            $table->foreignId('validated_by')->nullable()->constrained('users')->nullOnDelete();
            $table->timestamp('validated_at')->nullable();
            $table->foreignId('decided_by')->nullable()->constrained('users')->nullOnDelete();
            $table->timestamp('decided_at')->nullable();
            $table->text('decision_comment')->nullable();
            $table->timestamps();

            $table->unique(['organization_id', 'code']);
            $table->index(['organization_id', 'status']);
            $table->index('requested_by');
        });

        DB::statement('ALTER TABLE job_requests ADD CONSTRAINT job_requests_headcount_positive CHECK (headcount >= 1)');
        DB::statement("ALTER TABLE job_requests ADD CONSTRAINT job_requests_status_valid CHECK (status IN ('borrador', 'enviado', 'observado', 'validado', 'aprobado', 'rechazado'))");
        DB::statement("ALTER TABLE job_requests ADD CONSTRAINT job_requests_contract_type_valid CHECK (contract_type IN ('tiempo_completo', 'tiempo_parcial', 'por_horas', 'plazo_fijo'))");

        Schema::create('job_request_status_histories', function (Blueprint $table) {
            $table->id();
            $table->foreignId('organization_id')->constrained()->restrictOnDelete();
            $table->foreignId('job_request_id')->constrained()->cascadeOnDelete();
            $table->string('from_status', 20)->nullable();
            $table->string('to_status', 20);
            $table->foreignId('changed_by')->constrained('users')->restrictOnDelete();
            $table->text('comment')->nullable();
            $table->timestamp('created_at')->useCurrent();

            $table->index(['job_request_id', 'created_at']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('job_request_status_histories');
        Schema::dropIfExists('job_requests');
    }
};
