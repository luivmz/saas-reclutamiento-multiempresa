# SEG-03 — El personal podía descargar versiones del CV que el candidato no le presentó

> Mantenimiento de seguridad del sistema existente, del 28/10/2026, en la rama `fix/seg-03-cv-document-authorization`. **Corregido en la rama y pendiente de auditoría de Codex.** No inicia F37-SBX, no supera ningún gate y no cambia estados formales de gobierno. Registrado como DEF-16 en el [registro de defectos](../../defects.md); la precisión de la regla queda como A-37 en los [supuestos](../../assumptions.md).

## 1. Base

| Dato | Valor |
|---|---|
| Base | `develop` = `origin/develop` = `2e5378699aa98a63ad1a67215f738a40ac3d623f`, árbol `e386ae2434b1c554115bf39cb8b063cfb2cb9d01`. Incluye SEG-01 y SEG-02, con la CI `tests` #40804808195 en verde |
| Rama | `fix/seg-03-cv-document-authorization`, creada desde esa base en un worktree aislado |
| Trabajo previo | Ninguna rama local ni remota contenía trabajo de SEG-03 |
| Commits | RED: `ef9a274601a9ca0e0fce63bc96aef104ec97b3da`. Corrección: `afa62825b959aa3ec0ab0f7af68e2b98e9117c54`. El commit de este documento se consulta en Git |

## 2. Regla afectada y precisión

| Regla | Texto vigente | Relación con SEG-03 |
|---|---|---|
| A-04 | «Una organización solo ve datos del postulante a través de postulaciones a **sus** vacantes.» | El acceso empresarial nace de una postulación concreta |
| A-11 | «La postulación guarda la referencia al CV vigente en ese momento.» | `ApplicationService::apply` guarda en `candidate_document_id` el último CV; las versiones que el candidato sube después no cambian esa referencia |
| A-12 | «[…] descarga solo para el propio postulante, RR. HH./Dirección de una organización donde postuló y evaluadores asignados.» | Admite dos lecturas: cualquier versión del candidato o solo la presentada. La política publicada aplicaba la primera |

**Precisión, registrada como A-37.** La pidió Luis Vila Meza y rige de aquí en adelante. El acceso empresarial corresponde al documento efectivamente presentado, no a todas las versiones del candidato:

- RR. HH. y Dirección solo descargan la versión que una postulación a su organización referencia.
- Un evaluador solo descarga la de una postulación en la que tiene una evaluación o entrevista asignada.
- El propietario conserva todas sus versiones.

A-11 y A-12 no se modifican, y la numeración de RF no cambia.

## 3. Causa

`CandidateDocumentPolicy::download`, antes de la corrección:

1. permitía al propietario;
2. permitía a RR. HH. y al Aprobador si el candidato tenía **cualquier** postulación en su organización;
3. permitía al evaluador si tenía **cualquier** evaluación o entrevista asignada sobre **cualquier** postulación del candidato en su organización.

Ninguna rama comparaba el documento pedido con el `candidate_document_id` de la postulación. La ruta `documentos/{document}/descargar` solo exige `auth`, y la vinculación encuentra cualquier documento porque `CandidateDocument` no tiene scope de organización. El identificador del documento, visible en los enlaces de descarga, bastaba para pedir cualquier otra versión.

## 4. Reproducción HTTP

[`CandidateDocumentAuthorizationTest`](../../../tests/Feature/Candidates/CandidateDocumentAuthorizationTest.php) hace peticiones reales a `documents.download`, con middleware, vinculación, Gate y Policy. Usa solo datos ficticios:

- **Organizaciones:** A y B.
- **Un candidato con cuatro versiones del CV:**
  - «antigua»: subida antes de postular y nunca presentada;
  - «A»: presentada a una vacante de A;
  - «B»: presentada a una vacante de B;
  - «nueva»: subida después de postular y nunca presentada.
- **Escenarios con datos adicionales:**
  - «A2», presentada a otra vacante de A;
  - «AyB», presentada a la vez a una vacante de A y a otra de B;
  - una postulación en una tercera organización, C, sin CV referenciado.
- **Evaluadores asignados** a postulaciones concretas: una evaluación y una entrevista sobre la postulación de A, una evaluación sobre la de A2 y una entrevista sobre la de B.

Cada versión está guardada en el disco privado (`Storage::fake('local')`), con contenido y nombre propios. Cada denegación comprueba antes que el archivo existe, para no confundir un 403 con un archivo inexistente.

**RED, con la política original y el commit `ef9a274`:** 4 fallos y 3 aciertos (68 aserciones). Cada fallo es un acceso indebido con respuesta 200:

- «personal de A, versión presentada solo a B»;
- «versión nueva no presentada», en la prueba del CV compartido;
- «evaluador de A, CV de otra postulación del mismo candidato»;
- «organización con una postulación sin CV referenciado».

Una ejecución anterior falló además en el caso del invitado por un error de la propia prueba: la petición salía autenticada por un `actingAs` anterior. Se corrigió antes del commit RED; no era el defecto.

**Matriz completa.** Una sonda de diagnóstico temporal, que no se versionó, recorrió la misma clase de datos con cada actor y cada versión. Los códigos HTTP fueron estos:

| Actor | antigua | A | A2 | B | AyB | nueva |
|---|---|---|---|---|---|---|
| Propietario | 200 → 200 | 200 → 200 | 200 → 200 | 200 → 200 | 200 → 200 | 200 → 200 |
| Otro candidato | 403 → 403 | 403 → 403 | 403 → 403 | 403 → 403 | 403 → 403 | 403 → 403 |
| RR. HH. y Aprobador de A | **200 → 403** | 200 → 200 | 200 → 200 | **200 → 403** | 200 → 200 | **200 → 403** |
| RR. HH. y Aprobador de B | **200 → 403** | **200 → 403** | **200 → 403** | 200 → 200 | 200 → 200 | **200 → 403** |
| Evaluador de A (evaluación o entrevista sobre la postulación de A) | **200 → 403** | 200 → 200 | **200 → 403** | **200 → 403** | **200 → 403** | **200 → 403** |
| Evaluador de A (postulación de A2) | **200 → 403** | **200 → 403** | 200 → 200 | **200 → 403** | **200 → 403** | **200 → 403** |
| Evaluador de B (entrevista sobre la postulación de B) | **200 → 403** | **200 → 403** | **200 → 403** | 200 → 200 | **200 → 403** | **200 → 403** |
| Evaluador de A sin asignar y solicitante de A | 403 → 403 | 403 → 403 | 403 → 403 | 403 → 403 | 403 → 403 | 403 → 403 |
| RR. HH. y evaluador de C (postulación sin CV) | **200 → 403** | **200 → 403** | **200 → 403** | **200 → 403** | **200 → 403** | **200 → 403** |

Cada celda indica el código antes y después de la corrección. En negrita, los accesos indebidos que se cierran.

## 5. Corrección

En `CandidateDocumentPolicy::download`:

- **El propietario** conserva todas sus versiones.
- **RR. HH. y el Aprobador** necesitan una postulación, sin scopes globales, con `candidate_id` igual al propietario del documento, `organization_id` igual a su organización y `candidate_document_id` igual al documento pedido.
- **Un evaluador** necesita, sobre una de esas postulaciones, una evaluación o una entrevista con `evaluator_id` igual a él y de su misma organización.
- **El resto** de roles y usuarios sigue denegado.

No hay respaldo con «el último CV del candidato» ni con otras postulaciones suyas. El controlador no cambia: autoriza con el Gate antes de tocar el almacenamiento, y la respuesta denegada es un 403 sin contenido del archivo, sin ruta privada, sin nombre original y sin `Content-Disposition`.

**Sin efecto en los flujos legítimos.** Toda pantalla del personal ya enlaza el documento presentado, `cvDocument`: el expediente (`ApplicationController` y `ApplicationResource`) y la sesión del evaluador (`AssessmentSessionPresenter`). Solo el perfil del propio candidato enlaza `latestCv`, y el propietario mantiene el acceso. Las pruebas existentes que descargan CV ya usaban el documento presentado (`CandidateProfileTest` y `EvaluationTest`), así que no hubo que cambiar ninguna fixture. Tampoco se modificó ninguna referencia `candidate_document_id`: `ApplicationService::apply` siempre la guarda (A-11).

## 6. Matriz de aceptación comprobada

Todas las filas, en `CandidateDocumentAuthorizationTest`:

| Requisito | Prueba | Resultado |
|---|---|---|
| El propietario descarga sus distintas versiones, con el contenido y el nombre de cada una | `owner_downloads_every_version_of_their_cv` | GREEN |
| Otro candidato no descarga ninguna | `another_candidate_downloads_none` | GREEN |
| RR. HH. y Aprobador de A descargan el CV presentado a A, pero no el presentado solo a B ni las versiones antigua o nueva no presentadas; lo mismo para B | `hr_and_approver_download_only_the_cv_presented_to_their_organization` | RED → GREEN |
| Un documento presentado a A y a B sigue disponible para ambas | `a_cv_presented_to_both_organizations_stays_available_to_both` | RED (por la versión nueva) → GREEN |
| Los evaluadores asignados a evaluación y a entrevista descargan el documento de su postulación; una asignación a otra postulación del mismo candidato no da acceso a otro documento | `assigned_evaluators_download_only_the_cv_of_their_application` | RED → GREEN |
| Evaluador no asignado y solicitante: 403; invitado: redirección a `login`, sin contenido | `unassigned_evaluator_requester_and_guest_get_nothing` | GREEN |
| Una postulación sin documento referenciado no da acceso a ningún CV, ni al personal ni al evaluador asignado | `an_application_without_a_cv_grants_no_fallback` | RED → GREEN |
| Ninguna respuesta denegada entrega bytes del documento, ruta privada, nombre original ni cabecera de descarga | Todas las denegaciones, con `assertDenied` | GREEN |

## 7. Pruebas ejecutadas

Todas en Docker, sobre PostgreSQL 17.11, con la base aislada `reclutamiento_testing`.

| Orden | Resultado real |
|---|---|
| Prueba focal de SEG-03, RED, sobre la política original | 4 fallos y 3 aciertos (68 aserciones) |
| Prueba focal de SEG-03, GREEN, con la corrección | **7 aprobadas** (297 aserciones) |
| `php artisan test` de `Candidates`, `Assessments` (evaluaciones y entrevistas), `Applications`, `Tenancy`, `Routing` y `Audit` | 13, 19, 24, 11, 2 y 16 aprobadas (324, 97, 237, 32, 14 y 208 aserciones), 0 fallos |
| Focal de SEG-01 (`ApplicationFileAuthorizationTest`) | 8 aprobadas (153 aserciones) |
| Grupo de SEG-02 (`--group seg02`) | 13 aprobadas (149 aserciones), sin fallos de orquestación, entorno, recursos ni invariante |
| `docker compose exec app php artisan test` | **439 aprobadas y 8 omitidas** (2097 aserciones), 0 fallos, en 97,44 s. Son las 432 previas más las 7 de SEG-03; las 8 omitidas son las preexistentes de verificación de correo de Fortify, una función desactivada |
| `docker compose exec app npm run build` | Correcto: 2375 módulos, salida 0 |
| `docker compose exec app npx tsc --noEmit` | 0 errores, salida 0 |
| Cypress completo, entorno E2E aislado (`reclutamiento_e2e`): `init-e2e-env.sh` y `docker compose --profile e2e run --rm cypress`, el equivalente sin npm en el host de `npm run cy:run` | **«All specs passed!»: 20 specs y 85 de 85 pruebas**, 0 fallidas, en 06:19 (Cypress 15.3.0, Electron 136 headless). Incluye los flujos que enlazan CV: postulación (e2e-05), preselección (e2e-06), evaluador (e2e-07), multiempresa (e2e-11) y flujo completo (e2e-13) |
| `vendor/bin/pint --test` sobre la prueba y la política | Correcto |

## 8. Archivos

| Archivo | Cambio | Commit |
|---|---|---|
| `tests/Feature/Candidates/CandidateDocumentAuthorizationTest.php` | 7 pruebas HTTP nuevas | `ef9a274` |
| `app/Policies/CandidateDocumentPolicy.php` | Autorización ligada al documento presentado y a la postulación autorizada | `afa6282` |
| `docs/assumptions.md` | Fila A-37: precisión de A-12 | Commit de este documento |
| `docs/defects.md` | Fila DEF-16 | Commit de este documento |
| `docs/v1.1/security/SEG-03-autorizacion-descarga-cv.md` | Este documento | Commit de este documento |

Trazabilidad: A-04, A-11, A-12 y A-37 (RF-09, RF-12 y RF-19) → `CandidateDocumentPolicy::download` → `CandidateDocumentAuthorizationTest`, con el apoyo de `CandidateProfileTest` y `EvaluationTest`.

## 9. Limitaciones y pendientes

- **Auditoría de Codex pendiente.** SEG-03 no está cerrado.
- **Fuera de alcance, sin cambios:**
  - restricciones por estado de la postulación o de la sesión, como permitir solo postulaciones activas;
  - políticas de retención;
  - SEG-04, SEG01-AUD-L01 y SEG02-AUD-I01.
- **Existencia de documentos.** Un identificador inexistente responde 404 y uno existente pero no autorizado, 403, así que se puede distinguir si un identificador existe. Es el comportamiento previo de la vinculación de rutas y no se cambió aquí.
- **Validador de F36-SBX.** Como con SEG-01 y SEG-02, si esta rama se integra, ese validador fallará por diseño en la regla FRZ; se valida anclado en su rama.
- **Recursos aislados y estado final.**
  - **Worktree** temporal en `.claude/worktrees/seg03`, sobre esta rama. Contenía archivos ignorados por Git: un `.env` generado desde `.env.example` (el `.env` real no se copió), un `.env.e2e` generado por `init-e2e-env.sh`, `public/build` y cachés. Se elimina al terminar; la rama se conserva.
  - **Sonda de la matriz.** Fue temporal, nunca se versionó y se borró antes de registrar la corrección.
  - **Contenedores.** `app` y `queue` se recrearon montando el worktree, y el perfil E2E levantó `app-e2e` y `queue-e2e`. Al terminar se ejecutó `docker compose --profile e2e down`, sin `-v`, y se recrearon los contenedores desde el checkout principal. Estado final verificado, igual al encontrado: los cuatro contenedores (`app`, `queue`, `postgres` y `redis`) creados y detenidos; `app`, `queue` y los scripts de inicio de `postgres` montan el checkout principal; una sola red `reclutamiento_default`; sin contenedores E2E.
  - **Volúmenes** `reclutamiento_pgdata`, `reclutamiento_redisdata`, `reclutamiento_vendor` y `reclutamiento_node_modules`: conservados.
  - **Bases de datos.** `reclutamiento_testing` quedó migrada y vacía; Cypress reinició `reclutamiento_e2e`, como está previsto. La base de desarrollo solo recibió el `migrate --force` del entrypoint, sin migraciones pendientes; no hubo migraciones destructivas sobre ella.
