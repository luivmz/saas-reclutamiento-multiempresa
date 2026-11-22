<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schema;

/**
 * EXPERIMENTAL (rama local exp/evidencias-ml02, F37 flow). Not the formal SaaS integration, which stays
 * conditioned on the real G0, a scope ADR and the N5 decision (EI-23).
 *
 * Fictitious evidence records per application, append-only (R-04): a correction inserts a new version that
 * points to the one it supersedes; reviewing, withdrawing, linking and unlinking are inserted events. The state
 * is derived, never stored. As with audit_logs, the only update allowed is the ON DELETE SET NULL of the actor
 * when a user account is deleted.
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::create('evidence_items', function (Blueprint $table): void {
            $table->id();
            $table->foreignId('organization_id')->constrained()->restrictOnDelete();
            $table->foreignId('application_id')->constrained()->restrictOnDelete();
            $table->foreignId('supersedes_id')->nullable()->unique()->constrained('evidence_items')->restrictOnDelete();
            $table->string('type', 32);
            $table->string('source', 32);
            $table->text('description');
            $table->foreignId('registered_by')->nullable()->constrained('users')->nullOnDelete();
            $table->timestamp('created_at')->useCurrent();

            $table->index(['organization_id', 'application_id']);
        });

        Schema::create('evidence_events', function (Blueprint $table): void {
            $table->id();
            $table->foreignId('organization_id')->constrained()->restrictOnDelete();
            $table->foreignId('evidence_item_id')->constrained()->restrictOnDelete();
            $table->string('action', 32);
            $table->foreignId('evaluation_criterion_id')->nullable()->constrained('evaluation_criteria')->restrictOnDelete();
            $table->text('reason')->nullable();
            $table->foreignId('actor_id')->nullable()->constrained('users')->nullOnDelete();
            $table->timestamp('created_at')->useCurrent();

            $table->index(['organization_id', 'evidence_item_id']);
        });

        DB::unprepared(<<<'SQL'
            CREATE OR REPLACE FUNCTION evidence_append_only() RETURNS trigger AS $$
            DECLARE
                actor text := TG_ARGV[0];
            BEGIN
                IF TG_OP = 'UPDATE'
                    AND (to_jsonb(OLD) ->> actor) IS NOT NULL
                    AND (to_jsonb(NEW) ->> actor) IS NULL
                    AND (to_jsonb(NEW) - actor) = (to_jsonb(OLD) - actor) THEN
                    RETURN NEW;
                END IF;

                RAISE EXCEPTION '% es de solo inserción: operación % no permitida.', TG_TABLE_NAME, TG_OP
                    USING ERRCODE = 'insufficient_privilege';
            END;
            $$ LANGUAGE plpgsql;

            CREATE TRIGGER evidence_items_append_only
                BEFORE UPDATE OR DELETE ON evidence_items
                FOR EACH ROW EXECUTE FUNCTION evidence_append_only('registered_by');

            CREATE TRIGGER evidence_events_append_only
                BEFORE UPDATE OR DELETE ON evidence_events
                FOR EACH ROW EXECUTE FUNCTION evidence_append_only('actor_id');
        SQL);
    }

    public function down(): void
    {
        DB::unprepared(<<<'SQL'
            DROP TRIGGER IF EXISTS evidence_events_append_only ON evidence_events;
            DROP TRIGGER IF EXISTS evidence_items_append_only ON evidence_items;
            DROP FUNCTION IF EXISTS evidence_append_only();
        SQL);

        Schema::dropIfExists('evidence_events');
        Schema::dropIfExists('evidence_items');
    }
};
