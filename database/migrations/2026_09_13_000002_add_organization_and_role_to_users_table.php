<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('users', function (Blueprint $table) {
            $table->foreignId('organization_id')->nullable()->after('id')->constrained()->restrictOnDelete();
            $table->string('role', 20)->default('postulante')->after('email');
            $table->index(['organization_id', 'role']);
        });

        DB::statement("ALTER TABLE users ADD CONSTRAINT users_role_valid CHECK (role IN ('solicitante', 'rrhh', 'aprobador', 'evaluador', 'postulante'))");
        DB::statement("ALTER TABLE users ADD CONSTRAINT users_role_organization CHECK ((role = 'postulante' AND organization_id IS NULL) OR (role <> 'postulante' AND organization_id IS NOT NULL))");
    }

    public function down(): void
    {
        DB::statement('ALTER TABLE users DROP CONSTRAINT IF EXISTS users_role_organization');
        DB::statement('ALTER TABLE users DROP CONSTRAINT IF EXISTS users_role_valid');

        Schema::table('users', function (Blueprint $table) {
            $table->dropIndex(['organization_id', 'role']);
            $table->dropConstrainedForeignId('organization_id');
            $table->dropColumn('role');
        });
    }
};
