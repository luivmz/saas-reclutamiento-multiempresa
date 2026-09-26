# Patrones concretos del backend

Esqueletos orientativos. Antes de escribir, mira el equivalente real más parecido en el código: `JobRequestWorkflow`, `ApplicationStageService`, `VacancyClosureService` o `AssessmentScheduler`.

## Servicio con estado, auditoría y notificación

```php
final class ExampleService
{
    public function __construct(private readonly AuditLogger $audit) {}

    public function approve(Example $example, User $actor): Example
    {
        return DB::transaction(function () use ($example, $actor) {
            $locked = Example::query()->lockForUpdate()->findOrFail($example->id);

            if (! $locked->status->canTransitionTo(ExampleStatus::Approved)) {
                throw new BusinessRuleException('El registro no puede aprobarse en su estado actual.');
            }

            $from = $locked->status;
            $locked->forceFill(['status' => ExampleStatus::Approved])->save();

            $this->audit->record(AuditAction::ExampleApproved, $locked, [
                'from' => $from->value,
                'to' => ExampleStatus::Approved->value,
            ], $actor);

            $locked->owner->notify(new ExampleApprovedNotification($locked));

            return $locked;
        });
    }
}
```

## Policy con rol y organización

```php
class ExamplePolicy
{
    public function update(User $user, Example $example): bool
    {
        return $user->hasRole(UserRole::HumanResources)
            && $user->sharesOrganizationWith($example);
    }
}
```

## Controlador delgado

```php
public function __invoke(ExampleRequest $request, Example $example, ExampleService $service): RedirectResponse
{
    Gate::authorize('update', $example);

    $service->approve($example, $request->user());
    Toast::success('Registro aprobado.');

    return back();
}
```

## Enum con transiciones y presentación

```php
enum ExampleStatus: string
{
    use HasPresentation;

    case Draft = 'borrador';
    case Approved = 'aprobado';

    /** @return list<self> */
    public function allowedTransitions(): array
    {
        return match ($this) {
            self::Draft => [self::Approved],
            self::Approved => [],
        };
    }

    public function canTransitionTo(self $target): bool
    {
        return in_array($target, $this->allowedTransitions(), true);
    }

    public function label(): string
    {
        return match ($this) {
            self::Draft => 'Borrador',
            self::Approved => 'Aprobado',
        };
    }

    public function tone(): string
    {
        return match ($this) {
            self::Draft => 'neutral',
            self::Approved => 'success',
        };
    }
}
```

## Migración con integridad

```php
Schema::create('examples', function (Blueprint $table) {
    $table->id();
    $table->foreignId('organization_id')->constrained()->restrictOnDelete();
    $table->string('status', 20)->default('borrador');
    $table->timestamps();
    $table->index(['organization_id', 'status']);
});

DB::statement("ALTER TABLE examples ADD CONSTRAINT examples_status_valid CHECK (status IN ('borrador', 'aprobado'))");
```

Nunca edites una migración ya publicada: crea una nueva.

## Prueba Feature trazable

```php
public function test_rf28_hr_approves_an_example(): void
{
    $org = Organization::factory()->create();
    $hr = User::factory()->hr($org)->create();
    $example = Example::factory()->for($org)->create();

    $this->actingAs($hr)
        ->post(route('examples.approve', $example))
        ->assertRedirect();

    $this->assertSame(ExampleStatus::Approved, $example->refresh()->status);
}

public function test_rf28_hr_of_another_organization_cannot_approve(): void
{
    $example = Example::factory()->for(Organization::factory()->create())->create();
    $intruder = User::factory()->hr(Organization::factory()->create())->create();

    $this->actingAs($intruder)
        ->post(route('examples.approve', $example))
        ->assertForbidden();

    $this->assertSame(ExampleStatus::Draft, $example->refresh()->status);
}
```

## Errores ya cometidos en este proyecto

No los repitas; están documentados en `docs/defects.md`.

| Defecto | Lección |
|---|---|
| DEF-03 | No uses `firstOrNew` con atributos protegidos: asigna `organization_id` explícitamente. |
| DEF-05 | Los recursos individuales van sin envoltura `data` (`JsonResource::withoutWrapping()`); verifica las props reales en la prueba. |
| DEF-06 | No sobrescribas métodos de `Request` como `session()` en un Form Request. |
| DEF-07 | La inmutabilidad se garantiza en la base de datos, no solo con eventos de Eloquent. |
| DEF-08 | La lista de claves sensibles a eliminar en auditoría se amplía junto con los metadatos nuevos. |
| DEF-09 | Las fechas se muestran en `America/Lima`, no en la zona del navegador. |
