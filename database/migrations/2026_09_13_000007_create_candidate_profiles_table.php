<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('candidate_profiles', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->unique()->constrained()->cascadeOnDelete();
            $table->string('phone', 20)->nullable();
            $table->string('city', 80)->nullable();
            $table->string('education_level', 20)->nullable();
            $table->string('professional_title', 150)->nullable();
            $table->unsignedSmallInteger('years_of_experience')->nullable();
            $table->text('summary')->nullable();
            $table->timestamps();
        });

        DB::statement('ALTER TABLE candidate_profiles ADD CONSTRAINT candidate_profiles_experience_range CHECK (years_of_experience IS NULL OR years_of_experience BETWEEN 0 AND 60)');
        DB::statement("ALTER TABLE candidate_profiles ADD CONSTRAINT candidate_profiles_education_valid CHECK (education_level IS NULL OR education_level IN ('secundaria', 'tecnico', 'bachiller', 'titulado', 'maestria', 'doctorado'))");

        Schema::create('candidate_documents', function (Blueprint $table) {
            $table->id();
            $table->foreignId('candidate_profile_id')->constrained()->cascadeOnDelete();
            $table->string('type', 20);
            $table->string('original_name', 255);
            $table->string('stored_path', 255)->unique();
            $table->string('mime_type', 100);
            $table->unsignedInteger('size_bytes');
            $table->timestamps();

            $table->index(['candidate_profile_id', 'type']);
        });

        DB::statement("ALTER TABLE candidate_documents ADD CONSTRAINT candidate_documents_type_valid CHECK (type IN ('cv'))");
        DB::statement('ALTER TABLE candidate_documents ADD CONSTRAINT candidate_documents_size_positive CHECK (size_bytes > 0)');
    }

    public function down(): void
    {
        Schema::dropIfExists('candidate_documents');
        Schema::dropIfExists('candidate_profiles');
    }
};
