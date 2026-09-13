<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('selection_decisions', function (Blueprint $table) {
            $table->id();
            $table->foreignId('organization_id')->constrained()->restrictOnDelete();
            $table->foreignId('vacancy_id')->unique()->constrained()->restrictOnDelete();
            $table->foreignId('selected_application_id')->constrained('applications')->restrictOnDelete();
            $table->foreignId('decided_by')->constrained('users')->restrictOnDelete();
            $table->text('justification');
            $table->unsignedSmallInteger('selected_position');
            $table->decimal('selected_score', 6, 2);
            $table->unsignedSmallInteger('ranked_candidates');
            $table->timestamp('decided_at');
            $table->foreignId('selection_registered_by')->nullable()->constrained('users')->restrictOnDelete();
            $table->timestamp('selection_registered_at')->nullable();
            $table->timestamps();

            $table->index('organization_id');
        });

        DB::statement('ALTER TABLE selection_decisions ADD CONSTRAINT selection_decisions_position_valid CHECK (selected_position >= 1 AND ranked_candidates >= selected_position)');
        DB::statement('ALTER TABLE selection_decisions ADD CONSTRAINT selection_decisions_score_range CHECK (selected_score BETWEEN 0 AND 100)');
        DB::statement('ALTER TABLE selection_decisions ADD CONSTRAINT selection_decisions_registration_consistent CHECK ((selection_registered_by IS NULL) = (selection_registered_at IS NULL))');

        DB::statement("CREATE UNIQUE INDEX applications_one_selected_per_vacancy ON applications (vacancy_id) WHERE status = 'seleccionado'");
    }

    public function down(): void
    {
        DB::statement('DROP INDEX IF EXISTS applications_one_selected_per_vacancy');
        Schema::dropIfExists('selection_decisions');
    }
};
