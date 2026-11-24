<?php

namespace Tests\Feature\Audit;

use App\Enums\AuditAction;
use App\Http\Resources\AuditLogResource;
use App\Models\AuditLog;
use App\Models\Organization;
use App\Models\User;
use Illuminate\Database\Eloquent\Relations\Relation;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Collection;
use Inertia\Testing\AssertableInertia;
use Tests\TestCase;

/**
 * DEF-29: la auditoría mostraba el tipo interno «evidence_item». La etiqueta es solo de presentación: el
 * registro conserva el tipo original y la tabla sigue siendo de solo inserción.
 */
class AuditEntityLabelsTest extends TestCase
{
    use RefreshDatabase;

    public function test_rf27_every_audited_entity_type_has_a_readable_label(): void
    {
        foreach (array_keys(Relation::morphMap()) as $type) {
            $label = AuditLogResource::entityLabel($type);

            $this->assertNotSame($type, $label, "Falta la etiqueta legible de «{$type}»");
            $this->assertMatchesRegularExpression('/^\p{Lu}[\p{L} ]+$/u', $label);
        }
    }

    public function test_rf27_evidence_entries_show_a_readable_label_and_keep_the_stored_type(): void
    {
        $organization = Organization::factory()->create();
        $approver = User::factory()->approver($organization)->create();

        (new AuditLog)->forceFill([
            'organization_id' => $organization->id,
            'user_id' => $approver->id,
            'action' => AuditAction::EvidenceRegistered,
            'auditable_type' => 'evidence_item',
            'auditable_id' => 991,
            'metadata' => ['application_id' => 7],
        ])->save();

        $this->actingAs($approver)
            ->get(route('audit.index'))
            ->assertOk()
            ->assertInertia(fn (AssertableInertia $page) => $page
                ->component('audit/index')
                ->where('logs.data', fn (Collection $data) => $data->contains(
                    fn (array $row) => $row['entity'] === ['type' => 'evidence_item', 'label' => 'Evidencia', 'id' => 991],
                )));

        $this->assertDatabaseHas('audit_logs', ['auditable_type' => 'evidence_item', 'auditable_id' => 991]);
    }

    public function test_an_unknown_entity_type_falls_back_to_a_generic_label(): void
    {
        $this->assertSame('Registro', AuditLogResource::entityLabel('tipo_que_no_existe'));
    }
}
