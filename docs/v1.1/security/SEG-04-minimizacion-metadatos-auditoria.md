# SEG-04 — Los comentarios libres de etapas y requerimientos se copiaban en los metadatos de auditoría

> Mantenimiento de seguridad del sistema existente, del 29/10/2026, en la rama `fix/seg-04-audit-metadata-minimization`. **Corregido en la rama y pendiente de auditoría de Codex.** No inicia F37-SBX, no supera ningún gate y no cambia estados formales de gobierno. Registrado como DEF-17 en el [registro de defectos](../../defects.md); la política de minimización queda como A-38 en los [supuestos](../../assumptions.md).

## 1. Base

| Dato | Valor |
|---|---|
| Base | `develop` = `origin/develop` = `25462977dd5d499e2734ccf381d9c0287f062b47`, árbol `7292344726a15c8e3668ddf715e8391cf9b7008d`. Incluye SEG-01, SEG-02 y SEG-03; su CI `tests` #40904841417 terminó en verde |
| Rama | `fix/seg-04-audit-metadata-minimization`, creada desde esa base en un worktree aislado |
| Trabajo previo | Ninguna rama local ni remota contenía trabajo de SEG-04; los documentos de SEG-01 a SEG-03 solo lo citan como fuera de alcance |
| Commits | RED: `1f2deb6a50ebb5f123b8ebb8a7eab746e11585d8`. Corrección: `74bcdf5fca81c54bc1e3db21564e343adcdee68d`. El commit de este documento se consulta en Git |

## 2. Diagnóstico

**Conclusión: confirmado como persistencia indebida, no como filtración HTTP.** El comentario libre se guardaba en `audit_logs.metadata`, pero ninguna consulta lo devolvía.

| Dimensión | Antes de la corrección | Evidencia |
|---|---|---|
| Almacenamiento en `audit_logs.metadata` | **Sí.** El comentario de cada cambio de etapa y de cada transición del requerimiento se copiaba en la clave `comment` | RED y sonda (§4) |
| Acceso autorizado al historial funcional | Correcto. El comentario vive en el historial y en el propio requerimiento, con sus Policies | Prueba 4 (§6) |
| Exposición por HTTP o interfaz | **No.** La única lectura de `audit_logs` es `AuditLogController`: solo Dirección, filtrada por organización y proyectada con la lista blanca de `AuditLogResource`, sin metadatos crudos, IP ni textos libres (A-33) | Prueba 3 (§6) |
| Logs y otros destinos | Sin copia en logs: `AuditLogger` solo escribe en la tabla, y las únicas llamadas a `Log::` están en `HealthController` y `MlRiskClient`. El aviso de cambio de etapa no lleva comentarios (A-14). El rechazo de un requerimiento envía el motivo al solicitante (RF-04): destino funcional legítimo, sin cambios | Inspección del código |

**a) Qué comentarios llegaban a los metadatos.** Dos productores pasaban `'comment' => $comment` dentro de un `array_filter`:

| Productor | Acciones | Comentarios |
|---|---|---|
| `ApplicationStageService::transition` | `postulacion.etapa_cambiada` | Escritos por RR. HH.: preselección (opcional, hasta 1000 caracteres), descarte (obligatorio, de 5 a 1000) y cambio manual (opcional). Fijos del sistema: «Evaluación programada.» y «Entrevista programada.» (`AssessmentScheduler`, A-16), «Selección registrada conforme a la decisión final.» (`SelectionRegistrationService`) y «Proceso cerrado: no seleccionado.» (`VacancyClosureService`) |
| `JobRequestWorkflow::transition` | `requerimiento.enviado`, `observado`, `validado`, `aprobado` y `rechazado` | Observación de RR. HH. (obligatoria, de 5 a 1000), motivo de aprobación (opcional) y de rechazo (obligatorio). El envío no lleva comentario y la validación no lo recibe por HTTP |

**b) La sanitización filtra nombres de clave, no contenido.** `AuditLogger::sanitize` ([`AuditLogger.php:62`](../../../app/Services/Audit/AuditLogger.php)) descarta, también en arrays anidados, las claves que coinciden con `SENSITIVE_KEY_PATTERN` (línea 14: `password`, `token`, `secret`, `cookie`, `authorization`, `api_key`, `cv_content`…). No mira los valores. `comment` no coincide, así que el texto se guardaba tal cual. DEF-08 amplió esa lista de claves; nunca hubo un control de contenido.

**c) Qué necesita el evento.** RF-27 define el registro como «usuario, organización, acción, entidad, fecha y metadatos permitidos». Para una transición basta con el actor (`user_id`), la organización, la acción, la entidad (`auditable_type` e `auditable_id`), la fecha y los estados anterior y nuevo. El comentario no hace falta para reconstruir el hecho: está en la fila del historial escrita en la misma transacción, con la misma postulación o requerimiento, los mismos estados y el mismo autor.

**d) Dónde se conserva el comentario legítimo.** En `application_stage_histories.comment`, que es el historial del expediente interno, visible para RR. HH. y Dirección de la organización (SEG-01). En el requerimiento, en `job_request_status_histories.comment` y en `job_requests.observation` y `decision_comment`, visibles para el solicitante propietario, RR. HH. y Dirección de la organización.

**e) Qué devuelven las consultas autorizadas.**

| Consulta | Quién | Qué devuelve |
|---|---|---|
| `GET /auditoria` | Dirección de la organización (A-33); el resto, 403 | Fecha, actor, acción, entidad y detalles de la lista blanca (`Estado anterior` y `Estado nuevo` en las transiciones). Nunca `metadata`, IP ni comentarios |
| `GET /postulaciones/{id}` | RR. HH. y Dirección de la organización; otra organización, 404 | Expediente con el historial y sus comentarios |
| `GET /mis-postulaciones/{id}` | El postulante propietario | Línea de tiempo sin comentarios ni observaciones (A-21) |
| `GET /requerimientos/{id}` | Solicitante propietario, RR. HH. y Dirección de la organización; otra organización, 404 | Observación, motivo de decisión e historial con comentarios |

## 3. Regla, contradicción y política

| Fuente | Texto | Alcance |
|---|---|---|
| RF-27 ([F6](../../academico/practica-06/F6_Requerimientos_Funcionales_Colegio_Andino.md), línea 90) | «Acción crítica ejecutada: usuario, organización, acción, entidad, fecha y metadatos permitidos.» | Contenido del registro |
| [`AGENTS.md`](../../../AGENTS.md), línea 37, contratos del producto | «Conserva la auditoría segura y append-only; no almacenes PII o secretos en sus metadatos.» | Almacenamiento |
| Skills `project-guardian` (§3.4) y `laravel-saas-quality` | «`AuditLogger` para acciones críticas, sin datos sensibles» y «metadatos sin datos sensibles» | Almacenamiento |
| A-33 | «Muestra un resumen con una lista blanca de metadatos: no muestra IP, metadatos crudos ni textos libres (comentarios u observaciones).» | Lectura |
| A-34 | `audit_logs` es de solo inserción también en la base de datos | Inmutabilidad |
| [`AuditTrailTest.php:142-147`](../../../tests/Feature/Audit/AuditTrailTest.php) | Exige que la justificación libre de la decisión final (RF-23) no aparezca en ningún `metadata`; `FinalDecisionService` no la copia | Precedente en el código |

**La contradicción.** v1.0 admitía dos lecturas:

- **Guardar y ocultar.** A-33 y [`AuditLogViewTest.php:49`](../../../tests/Feature/Audit/AuditLogViewTest.php), que registra a propósito `'comment' => 'Nota interna privada'` para comprobar que la vista lo oculta, describen una vista que esconde textos libres que pueden estar guardados.
- **No guardar.** RF-27 limita el registro a metadatos permitidos, y el contrato de producto y las skills prohíben guardar en ellos PII o datos sensibles. El código ya lo aplicaba a la justificación de RF-23, pero no a los comentarios de etapas y requerimientos.

Un comentario sobre una postulación es información sobre una persona identificada: el registro lo vincula a la postulación (`auditable_id`) y, por ella, al postulante, sea cual sea su redacción. Además, un texto libre puede contener cualquier dato, y el sistema no puede garantizar lo contrario. Copiarlo en un almacén inmutable (A-34), donde no puede rectificarse ni eliminarse y que ninguna pantalla lee, contradice la regla de almacenamiento. Las pruebas RED lo hacen observable: un comentario con un DNI y un dato de salud inventados quedaba guardado literalmente.

**Política concreta, registrada como A-38.** Complementa A-33 sin modificarla; A-33 sigue rigiendo la vista.

- Los eventos de transición, `postulacion.etapa_cambiada` y `requerimiento.enviado`, `observado`, `validado`, `aprobado` y `rechazado`, guardan en `metadata` solo el estado anterior y el nuevo.
- El registro conserva, como siempre, usuario, organización, acción, entidad y fecha.
- Los comentarios y observaciones, también los textos fijos del sistema, quedan en el historial funcional, con su control de acceso.
- Los registros anteriores no se modifican (A-34).

## 4. Reproducción por el flujo real

[`AuditMetadataMinimizationTest`](../../../tests/Feature/Audit/AuditMetadataMinimizationTest.php) recorre los flujos HTTP reales, con middleware, Form Requests, Policies, servicios y PostgreSQL:

- preselección, cambio manual y descarte de postulaciones;
- envío, observación, aprobación y rechazo de requerimientos;
- la vista de auditoría, el expediente, la vista del postulante y la ficha del requerimiento.

Cada comentario es sintético y lleva una marca: «`SEG04MARCA-<etiqueta>`: motivo ficticio con un DNI inventado 00000000 y un dato de salud inventado.» La comprobación de almacenamiento se hace evento a evento y también en la base de datos, con `metadata::text like '%SEG04MARCA%'`.

**RED, sobre el código original y el commit `1f2deb6`:** 2 fallos y 2 aciertos (91 aserciones).

- **Fallos, ambos por la clave `comment`:**
  - `postulacion.etapa_cambiada stored more than the states in audit_logs.metadata`, con `'comment' => 'SEG04MARCA-PRESELECCION: …'` de más;
  - `requerimiento.observado …`, con `'comment' => 'SEG04MARCA-OBSERVACION: …'` de más. `requerimiento.enviado`, que no lleva comentario, ya pasaba.
- **Aciertos, que son caracterizaciones:**
  - la vista de auditoría nunca devolvió los comentarios;
  - el historial autorizado conserva el comentario y el postulante no lo ve.

**Flujo de datos antes y después.** Una sonda temporal, que no se versionó y se borró antes del commit de corrección, volcó lo guardado en dos ejecuciones reales. Recorrió el proceso completo de `AuditTrailTest` más los flujos de SEG-04 y produjo 32 eventos de 19 acciones:

| Acción | Eventos | Claves antes | Claves después | Textos libres que se guardaban |
|---|---|---|---|---|
| `postulacion.etapa_cambiada` | 9 | `comment`, `from`, `to` | `from`, `to` | 3 marcas de RR. HH. y 4 textos del sistema |
| `requerimiento.observado` | 2 | `comment`, `from`, `to` | `from`, `to` | «Precisar la justificación.» y una marca |
| `requerimiento.aprobado` | 2 | `comment`, `from`, `to` | `from`, `to` | Una marca; la aprobación sin motivo ya solo tenía estados |
| `requerimiento.rechazado` | 1 | `comment`, `from`, `to` | `from`, `to` | Una marca |
| `requerimiento.enviado` y `validado` | 3 y 1 | `from`, `to` | `from`, `to` | Ninguno |
| Las otras 13 acciones observadas | 13 | Sin cambios | Sin cambios | Ninguno |

Las otras 13 son: registro y corrección del requerimiento; registro y publicación de la vacante; postulación; programación y resultado de evaluación y de entrevista; decisión final; registro de la selección; cierre y notificación del resultado.

Evento a evento, 21 conservaron exactamente sus claves y 11 solo perdieron `comment`, con los mismos valores de `from` y `to`. La sonda también confirmó que `evaluacion.programada` no copia el lugar ni las indicaciones marcados, y que la decisión final no copia su justificación.

## 5. Corrección

En `ApplicationStageService::transition` ([líneas 91-96](../../../app/Services/Applications/ApplicationStageService.php)) y `JobRequestWorkflow::transition` ([líneas 140-145](../../../app/Services/JobRequests/JobRequestWorkflow.php)), el evento recibe una estructura explícita, `['from' => …, 'to' => …]`, en lugar del `array_filter` con el comentario. El historial funcional se sigue escribiendo justo antes, en la misma transacción y con el mismo comentario.

**Qué no cambia:**

- `AuditLogger`, su sanitización y sus otros llamadores;
- `AuditLogResource` y su lista blanca, `AuditAction` y el morph map;
- migraciones, el trigger `audit_logs_append_only` y los registros existentes;
- historiales, Form Requests, Policies, rutas, notificaciones, frontend y ML.

Ninguna prueba, seeder, pantalla ni spec de Cypress leía `metadata.comment`.

**Por qué no una lista blanca global en `AuditLogger`.** Habría que declarar y mantener las claves de las 23 acciones, entre ellas `target_completion_at` de GAP-01 o `selected_score` de RF-23; es decir, cambiar contratos de eventos ajenos a SEG-04. La estructura explícita en los dos productores corrige los casos confirmados sin tocar los demás. Tampoco se usa una expresión regular sobre el contenido: no puede garantizar la ausencia de datos personales en un texto libre.

**Productores revisados:**

| Acciones | Metadatos | Decisión |
|---|---|---|
| `postulacion.etapa_cambiada`; `requerimiento.enviado`, `observado`, `validado`, `aprobado` y `rechazado` | Estados y comentario | **Corregidas**: solo estados |
| `requerimiento.registrado`, `vacante.publicada`, `postulacion.registrada` | Código de requerimiento o vacante | Fuera: sin texto libre |
| `requerimiento.corregido`, `postulante.perfil_actualizado` | Nombres de los campos cambiados, no sus valores | Fuera |
| `vacante.registrada`, `vacante.configurada` | Códigos, número de criterios y `target_completion_at` (GAP-01) | Fuera |
| `postulante.cv_cargado` | Tamaño y tipo MIME, nunca el contenido | Fuera |
| `evaluacion.programada`, `entrevista.programada` | Tipo, fecha y evaluador; no el lugar ni las indicaciones | Fuera |
| `evaluacion.resultado_registrado`, `entrevista.resultado_registrado` | Número de criterios y resultado; puntajes, comentarios y observaciones quedan en sus tablas | Fuera |
| `seleccion.decision_registrada` | Postulación, posición, puntaje y tamaño del ranking; no la justificación | Fuera: dato numérico, no texto libre (§9) |
| `seleccion.candidato_registrado`, `vacante.cerrada`, `proceso.resultado_notificado`, `usuario.registrado` | Identificadores, tipo de cierre, conteos y canal | Fuera |

## 6. Matriz de aceptación comprobada

Las cinco pruebas de `AuditMetadataMinimizationTest`:

| # | Prueba | Antes | Después |
|---|---|---|---|
| 1 | `stage_change_comments_stay_in_the_history_and_out_of_audit_metadata` | RED | GREEN |
| 2 | `job_request_comments_stay_in_the_request_and_out_of_audit_metadata` | RED | GREEN |
| 3 | `audit_trail_view_never_returned_the_comments` | GREEN | GREEN |
| 4 | `authorized_history_keeps_the_comment_and_the_candidate_never_sees_it` | GREEN | GREEN |
| 5 | `scheduling_keeps_its_texts_out_of_audit_metadata` | Añadida con la corrección | GREEN |

La prueba 5 verifica una consecuencia, no un defecto: el paso automático conserva «Evaluación programada.» en el historial, y en la auditoría solo quedan los estados.

| Criterio | Evidencia | Resultado |
|---|---|---|
| La prueba demuestra el comportamiento previo | RED de las pruebas 1 y 2, por la clave `comment` | Observado |
| Las nuevas escrituras no copian el contenido prohibido | Pruebas 1, 2 y 5, evento a evento y con la consulta sobre `metadata::text` | GREEN |
| Se conservan los campos necesarios | Actor, organización, acción, entidad y estados comprobados en cada evento | GREEN |
| El historial funcional legítimo sigue funcionando | Historiales, `observation`, `decision_comment`, aviso de rechazo y vistas autorizadas (pruebas 1, 2, 4 y 5) | GREEN |
| No se amplía el acceso | Prueba 3: RR. HH. recibe 403 en la auditoría y otra organización no ve registros. Prueba 4: el postulante no ve comentarios y otra organización recibe 404. Sin cambios en Policies, rutas ni resources | GREEN |
| Se conserva el aislamiento multiempresa | Pruebas 3 y 4 y el grupo `Tenancy` | GREEN |
| Siguen activas las protecciones de integridad | Trigger presente; pruebas de solo inserción de `AuditTrailTest` y `AuditLoggerTest` en verde; sin migraciones | GREEN |
| Sin regresiones de SEG-01, SEG-02 ni SEG-03 | Focales y grupo de concurrencia (§7) | GREEN |

## 7. Pruebas ejecutadas

Todas en Docker, sobre PostgreSQL 17.11, con la base aislada `reclutamiento_testing`: `phpunit.xml` la fuerza con `force="true"`. Antes de las pruebas se comprobó que el servidor tenía `reclutamiento`, `reclutamiento_testing` y `reclutamiento_e2e`, y que el `migrate --force` del arranque respondió «Nothing to migrate».

| Orden | Resultado real |
|---|---|
| Focal de SEG-04, RED, sobre el código original (`1f2deb6`) | 2 fallos y 2 aciertos (91 aserciones) |
| Focal de SEG-04, GREEN, con la corrección (`74bcdf5`) | **5 aprobadas** (116 aserciones) |
| Grupos `Audit`, `Applications`, `Notifications`, `Tenancy`, `JobRequests`, `Assessments` y `Selection` | 21, 24, 8, 11, 11, 19 y 30 aprobadas (324, 237, 64, 32, 61, 97 y 206 aserciones), 0 fallos |
| Focal de SEG-01 (`ApplicationFileAuthorizationTest`) | 8 aprobadas (153 aserciones) |
| Focal de SEG-03 (`CandidateDocumentAuthorizationTest`) | 7 aprobadas (297 aserciones) |
| Grupo de SEG-02 (`tests/Feature/Concurrency`) | 13 aprobadas (149 aserciones) |
| `docker compose exec app php artisan test` | **444 aprobadas y 8 omitidas** (2213 aserciones), 0 fallos, en 100,03 s. Son las 439 previas más las 5 de SEG-04; las 8 omitidas son las preexistentes de verificación de correo de Fortify, una función desactivada |
| `docker compose exec app npm run build` | Correcto: 2375 módulos, salida 0 |
| `docker compose exec app npx tsc --noEmit` | 0 errores, salida 0 |
| `vendor/bin/pint --test` sobre los tres archivos cambiados | Correcto |
| `vendor/bin/pint --parallel --test` (`composer lint:check`) | Falla en 8 archivos que SEG-04 no toca, los mismos que fallan sobre la base `2546297`: `app/Models/Vacancy.php`, `app/Providers/AppServiceProvider.php`, `app/Services/Assessments/AssessmentResultRecorder.php`, `bootstrap/app.php`, `database/seeders/DemoSeeder.php`, `routes/web.php`, `tests/Feature/Audit/AuditLoggerTest.php` y `tests/Feature/Tenancy/CrossTenantAccessTest.php`. Es deuda previa y queda fuera de alcance |
| `vendor/bin/phpstan analyse` (`composer types:check`) | 91 errores sobre la base y 91 con SEG-04: el mismo conjunto al comparar archivo y mensaje sin número de línea, sin ninguno nuevo ni eliminado. Los de `ApplicationStageService` y `JobRequestWorkflow` son de inferencia (`findOrFail` visto como `Model\|Collection` y tipos de Carbon) y ya existían. Es deuda previa, fuera de alcance; la CI no ejecuta Pint ni PHPStan |
| Cypress completo, entorno E2E aislado (`reclutamiento_e2e`): `init-e2e-env.sh` y `docker compose --profile e2e run --rm cypress`, el equivalente sin npm en el host de `npm run cy:run` | **«All specs passed!»: 20 specs y 85 de 85 pruebas**, 0 fallidas, en 06:16 (Cypress 15.3.0, Electron 136 headless). Incluye los flujos que pasan por los dos productores: requerimientos (e2e-02 y e2e-03), preselección (e2e-06), evaluador (e2e-07), decisión, selección y cierre (e2e-09 y e2e-10), multiempresa (e2e-11) y flujo completo (e2e-13) |

## 8. Archivos

| Archivo | Cambio | Commit |
|---|---|---|
| `tests/Feature/Audit/AuditMetadataMinimizationTest.php` | 4 pruebas HTTP (RED) y la prueba de consecuencia | `1f2deb6` y `74bcdf5` |
| `app/Services/Applications/ApplicationStageService.php` | El evento guarda solo `from` y `to` | `74bcdf5` |
| `app/Services/JobRequests/JobRequestWorkflow.php` | El evento guarda solo `from` y `to` | `74bcdf5` |
| `docs/assumptions.md` | Fila A-38 | Commit de este documento |
| `docs/defects.md` | Fila DEF-17 | Commit de este documento |
| `docs/v1.1/security/SEG-04-minimizacion-metadatos-auditoria.md` | Este documento | Commit de este documento |

Trazabilidad: RF-27 con A-33, A-34 y A-38 (RF-02 a RF-04, RF-13 y RF-14) → `ApplicationStageService::transition` y `JobRequestWorkflow::transition` → `AuditMetadataMinimizationTest`, con el apoyo de `AuditTrailTest`, `AuditLogViewTest`, `ApplicationReviewTest` y `JobRequestWorkflowTest`.

## 9. Tratamiento histórico, riesgos y límites

**Registros anteriores: no se tocan en SEG-04.**

- **Base de desarrollo.** Se consultó en solo lectura antes de las pruebas: `audit_logs` tenía 0 registros, así que no contiene comentarios.
- **Otras bases.** Cualquier base usada o sembrada con el código anterior sí los contiene, porque `DemoSeeder` construye los datos de demostración con los servicios reales y pasa comentarios ficticios ([`DemoSeeder.php`](../../../database/seeders/DemoSeeder.php), líneas 86, 90, 99, 100 y 171). Son textos ficticios.
- **Propuesta separada, no ejecutada:**
  1. conservarlos tal cual, como exige A-34, y documentarlo;
  2. si el equipo decide tratarlos, hacerlo en un incremento propio y autorizado. Necesitaría una excepción controlada al trigger `audit_logs_append_only`, como la que ya existe para `user_id`, que solo retire la clave `comment`, con su ADR, pruebas y evidencia antes y después;
  3. fijar el plazo de retención de la auditoría, que el análisis de privacidad de F34A deja «a definir».

**Riesgos y límites:**

- **Integridad del comentario.** La auditoría ya no lo guarda, así que su conservación depende del historial funcional. La aplicación no tiene vía para editarlo, pero esa tabla no tiene trigger. Si el equipo necesitara probar que un comentario no cambió, sería una decisión de diseño aparte.
- **`AuditLogger::record` sigue aceptando cualquier clave** que no coincida con su patrón. La protección está en los dos productores y en sus pruebas; una lista blanca global sería una decisión aparte. Se recomienda recoger la regla en la skill `laravel-saas-quality`, que no se modificó aquí.
- **`AuditLogViewTest` sigue registrando un comentario a mano** para comprobar la defensa de la vista (A-33). Se conserva sin cambios.
- **Otros datos personales de la auditoría, fuera de alcance:**
  - la IP (`ip_address`), que forma parte del diseño de RF-27 y A-33 oculta;
  - `selected_score` de la decisión final, un dato numérico del ranking que también está en `selection_decisions`.

  Si se quisiera minimizarlos, haría falta una revisión aparte.
- **Validador de F36-SBX.** Como con SEG-01 a SEG-03, si esta rama se integra ese validador fallará por diseño en la regla FRZ; se valida anclado en su rama.
- **Pendientes heredados, sin cambios:** SEG01-AUD-L01 (LOW) y SEG02-AUD-I01 (INFO).
- **Auditoría de Codex pendiente.** SEG-04 no está cerrado.

**Recursos aislados y estado final.**

- **Worktree** temporal en `.claude/worktrees/seg04`, sobre esta rama. Contenía archivos ignorados por Git: un `.env` generado desde `.env.example` (el `.env` real no se copió), un `.env.e2e` generado por `init-e2e-env.sh`, `public/build` y cachés. Se elimina al terminar; la rama se conserva.
- **Sonda del flujo de datos.** Fue temporal, nunca se versionó y se borró antes del commit de corrección. Para medir la línea base de Pint y PHPStan, el worktree pasó un momento a `2546297` en modo *detached* y volvió a la rama.
- **Contenedores.** `app` y `queue` se recrearon montando el worktree, y el perfil E2E levantó `app-e2e` y `queue-e2e`. Al terminar se ejecutó `docker compose --profile e2e down`, sin `-v`, y se recrearon los contenedores desde el checkout principal.
- **Estado final verificado, igual al encontrado:**
  - los cuatro contenedores (`app`, `queue`, `postgres` y `redis`) creados y detenidos;
  - `app`, `queue` y los scripts de inicio de `postgres` montan el checkout principal. Docker Desktop muestra ese origen como `D:\…` o como `/run/desktop/mnt/host/d/…` según la creación, como ya ocurrió en restauraciones anteriores;
  - una sola red, `reclutamiento_default`, y ningún contenedor E2E;
  - los contenedores y volúmenes de las auditorías de Codex (`seg0…audit…`) no se tocaron.
- **Volúmenes** `reclutamiento_pgdata`, `reclutamiento_redisdata`, `reclutamiento_vendor` y `reclutamiento_node_modules`: conservados.
- **Bases de datos.**
  - `reclutamiento_testing` quedó migrada y vacía.
  - Cypress reinició `reclutamiento_e2e`, como está previsto.
  - La base de desarrollo solo recibió el `migrate --force` del entrypoint, que respondió «Nothing to migrate». Su `audit_logs` tenía 0 registros antes y después de las pruebas, y el trigger `audit_logs_append_only` sigue presente. No hubo migraciones destructivas.
