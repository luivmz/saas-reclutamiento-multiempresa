# Informe del diagrama de secuencia de postulación

## 1. Propósito

Representar la interacción del postulante con el sistema al consultar una vacante y registrar su postulación.

**Artefacto original:** `Diagramas/PD/SaaS Reclutamiento - Diagramas UML.oom` (PowerDesigner, carpeta del curso, fuera del repositorio). No se modificó.

## 2. Elementos principales

**Líneas de vida del diagrama original:**
- Postulante (actor)
- Interfaz Web: React
- Aplicación: Laravel 13 / Inertia 3
- Autorización: Policy
- BD: PostgreSQL

**Mensajes del diagrama original:**
1. Seleccionar vacante → Solicitar detalle de vacante → Consultar vacante → Retornar datos de vacante → Carga de datos.
2. Solicitar postulación → Enviar solicitud de postulación → Validar usuario y permisos → Usuario autorizado.
3. Consultar estado de vacante → Verificar postulación existente → Retornar resultado.
4. Registrar postulación → Confirmar registro → Confirmar postulación → Mostrar confirmación.

## 3. Relación con requerimientos

- RF-07 (consulta de vacante publicada)
- RF-08 (acceso del postulante)
- RF-09 (perfil y CV como requisito)
- RF-10 (registrar postulación)
- RF-11 (confirmar postulación)

## 4. Relación con implementación

| Paso | Implementación real |
|---|---|
| Actor y entrada | Postulante autenticado; `GET /empleos/{vacancy}` (`PublicVacancyController::show`, solo vacantes publicadas) y `POST /empleos/{vacancy}/postular` (`ApplyController`) |
| Validación de permisos | `Gate::authorize('apply', Application::class)` (`ApplicationPolicy`: rol postulante) |
| Validaciones de negocio | `ApplicationService::apply`: vacante publicada y dentro de plazo, perfil completo y CV cargado (A-11), postulación única por vacante (A-10; índice `UNIQUE (vacancy_id, candidate_id)`). Si falla, `BusinessRuleException` (clave `workflow`) |
| Persistencia | `applications` (estado `postulado`, referencia al CV vigente), `application_stage_histories` |
| Notificación | `ApplicationReceivedNotification` en cola (base de datos + correo con *driver* `log`), con código de seguimiento |
| Auditoría | `AuditAction::ApplicationSubmitted` (`postulacion.registrada`) |
| Respuesta | Redirección a `mis-postulaciones/{application}` con aviso de éxito |

**Pruebas:**
- PHPUnit: `ApplyToVacancyTest` (`test_rf10_rf11_candidate_applies_and_receives_confirmation`, duplicado, vacante cerrada o vencida, vacante en borrador, perfil incompleto o sin CV).
- Cypress: E2E-05, E2E-12 (vacante cerrada) y E2E-13.

## 5. Consistencias

- Los participantes (React, Laravel/Inertia, Policy, PostgreSQL) coinciden con la arquitectura real.
- Los pasos «validar usuario y permisos», «consultar estado de la vacante» y «verificar postulación existente» existen en la implementación, en ese mismo orden lógico.
- La confirmación al postulante existe (RF-11).

## 6. Diferencias detectadas

- El diagrama no muestra la validación de perfil completo y CV (A-11), que la implementación exige.
- El diagrama no muestra la notificación en cola ni el registro de auditoría. En la implementación la confirmación llega también como notificación asíncrona.
- La consulta de la vacante pública se resuelve sin Policy (portal público); la Policy se aplica al postular.

Son omisiones de detalle, no contradicciones del flujo.

## 7. Limitaciones

El artefacto está fuera del repositorio. Algunos mensajes tienen redacción informal («carga datos», «mostrae infromacion»).

## 8. Estado para entrega

**Vigente con observaciones.**

## 9. Recomendación

En una futura versión gráfica:
- agregar la validación de perfil y CV;
- agregar la notificación en cola y la auditoría;
- corregir la redacción de los mensajes.
