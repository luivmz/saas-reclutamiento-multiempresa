---
name: laravel-saas-quality
description: Patrón de implementación del backend Laravel multiempresa de este proyecto. Úsala al crear o modificar controladores, Form Requests, Policies, servicios, modelos, migraciones, notificaciones o auditoría, y al escribir sus pruebas PHPUnit. Define el orden Controller delgado → Form Request → Policy → Service → Model/PostgreSQL y la regresión obligatoria.
---

# Calidad del backend Laravel multiempresa

Toda funcionalidad del backend sigue la misma cadena. No la saltes: cada eslabón existe porque protege una regla del proyecto.

```
Ruta (+ middleware role) → Form Request → Controller delgado → Policy → Service → Model/Enum → PostgreSQL
                                                                      ↘ AuditLogger
                                                                      ↘ Notification (cola, afterCommit)
```

## Responsabilidad de cada capa

| Capa | Hace | No hace |
|---|---|---|
| Ruta (`routes/web.php`) | Slug en español, nombre en inglés, `role:` cuando el acceso es de un solo rol | Lógica |
| Form Request | Validación en servidor, mensajes y `attributes()` en español | Decidir permisos |
| Controller | `Gate::authorize`, llama a **un** servicio, responde con Inertia o redirección + `Toast` | Reglas de negocio, consultas complejas |
| Policy | Rol **y** organización (`$user->hasRole(...)` + `sharesOrganizationWith`) | Validar formato |
| Service | Transacción, transición de estado, auditoría y notificación | Conocer la petición HTTP |
| Modelo / Enum | Relaciones, casts, transiciones permitidas, etiquetas | Orquestar procesos |
| PostgreSQL | `CHECK`, `UNIQUE`, FK, índices parciales | — |

## Reglas que no se negocian

- **Multiempresa**: entidad de negocio nueva ⇒ `organization_id` (FK `restrictOnDelete`) + `use BelongsToOrganization` + Policy que compare organización. El postulante es global y no lleva `organization_id`.
- **Estados**: viven en un *enum* con `allowedTransitions()`; la base de datos replica los valores válidos con `CHECK`. Los dos lugares se cambian juntos.
- **Errores de negocio**: `throw new BusinessRuleException('mensaje en español')` dentro del servicio. Nunca devuelvas un 500 para una regla de negocio.
- **Concurrencia**: si dos usuarios pueden actuar sobre el mismo registro, `DB::transaction` + `lockForUpdate()`. El cierre de vacante es el ejemplo a imitar.
- **Auditoría**: acción crítica ⇒ caso nuevo en `AuditAction` (con `label()` y `tone()`) + `AuditLogger::record(...)` con metadatos sin datos sensibles + entrada en el morph map de `AppServiceProvider` + ampliación de las listas blancas de `AuditLogResource`.
- **Notificaciones**: extienden `RecruitmentNotification` (`ShouldQueue`, `afterCommit`). Nunca incluyen puntajes, observaciones internas ni datos de otros candidatos.
- **Servicios externos**: en pruebas se simulan con `Http::fake()`. Ninguna prueba sale a la red.
- **Decisión humana**: ningún servicio nuevo puede cambiar el estado de una postulación a `seleccionado` o `no_seleccionado` fuera de RF-24 y RF-25.

Ejemplos concretos y esqueletos: [PATTERNS.md](PATTERNS.md).

## Pruebas

- PHPUnit sobre PostgreSQL real (`reclutamiento_testing`), con `RefreshDatabase`. No se usa SQLite.
- Nombre de prueba trazable al requerimiento: `test_rfNN_descripcion_en_ingles`.
- Por cada funcionalidad: caso feliz, validación, autorización (otros roles reciben 403) y acceso desde otra organización.
- Fábricas por rol: `User::factory()->hr($org)`, `->approver($org)`, `->requester($org)`, `->evaluator($org)`, `->candidate()`.
- `phpunit.xml` ya fuerza caché y sesión en memoria y cola síncrona: las pruebas no necesitan Redis.

## Regresión obligatoria

Antes de cerrar cualquier cambio de backend:

```
docker compose exec app php artisan test        # 0 fallidas
docker compose exec app npm run build           # correcto
docker compose exec app npx tsc --noEmit        # 0 errores
```

Reporta los números reales de la ejecución. Si no la corriste, dilo.
