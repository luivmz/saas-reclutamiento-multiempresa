# SEG-01 — El postulante podía abrir el expediente interno de su propia postulación

> Mantenimiento de seguridad del sistema existente, del 28/10/2026, en la rama `fix/seg-01-internal-application-authorization`. **Corregido en la rama y pendiente de auditoría de Codex.** No inicia F37-SBX, no supera ningún gate y no cambia estados formales de gobierno. Registrado como DEF-14 en el [registro de defectos](../../defects.md).

## 1. Base

| Dato | Valor |
|---|---|
| Base | `develop` = `origin/develop` = `55456943059efaa7b34fd7550de97986f0d13061`, árbol `01dc59a80eed0e9f7c26143f6787010fcefb406c` (el mismo de `main` `55f758e`) |
| Rama | `fix/seg-01-internal-application-authorization`, creada desde esa base |
| Correcciones locales previas | Ninguna: ninguna referencia local ni remota modificaba el código afectado después de `develop` |
| Commit del candidato | Se consulta en Git; este documento no puede citar el commit que lo contiene |

## 2. Regla afectada

- **A-21.** «El postulante ve sus convocatorias (fecha, modalidad, lugar, indicaciones y estado), pero nunca puntajes, observaciones ni el resultado de la entrevista.»
- **A-14.** Las observaciones internas de RR. HH. no llegan al candidato.
- **A-04.** La cuenta del postulante es global, sin `organization_id`.
- **Requisitos:** RF-12 (expediente para RR. HH. y Dirección) y RF-17 (convocatorias al candidato).

## 3. Reproducción HTTP

Con datos ficticios marcados con textos reconocibles (`SEG01-…`), una postulación en entrevista tiene:

- un cambio de etapa comentado por RR. HH.;
- una evaluación con observaciones y un resultado con su comentario;
- una entrevista con observaciones, resultado «No recomendado» y un resultado con su comentario.

La prueba [`ApplicationFileAuthorizationTest`](../../../tests/Feature/Applications/ApplicationFileAuthorizationTest.php) pide, como el candidato propietario autenticado, `GET /postulaciones/{id}` (`applications.show`).

**RED, sobre la base y antes de cambiar el código:** 1 fallo y 7 aciertos (146 aserciones). La respuesta contenía `SEG01-HISTORY-COMMENT`.

**Sonda de diagnóstico** (temporal y no versionada, ejecutada sobre la base) con la misma petición:

- estado **200** y componente Inertia `applications/show`;
- **7 de 7** marcadores internos presentes;
- props recibidas por el candidato:
  - `history`, con el autor de RR. HH. y su comentario;
  - `assessments.evaluations`, con el evaluador, las observaciones y los resultados con puntaje (17,5 de 20) y comentario;
  - `assessments.interviews`, con las observaciones y `outcome` («No recomendado»);
  - `application.candidate`, con el correo y el perfil.

## 4. Causa

1. La ruta `postulaciones/{application}` solo exige `auth`, sin `role:`.
2. `OrganizationScope` no filtra a los candidatos, que no tienen organización (A-04), así que la vinculación de la ruta encuentra la postulación.
3. `ApplicationController` autorizaba con `ApplicationPolicy::view`, que permite al candidato propietario porque la usa también la consulta legítima `mis-postulaciones/{id}`.
4. El controlador entrega el expediente interno completo, con `AssessmentSessionPresenter::summary()` y `ApplicationStageHistory::toTimelineEntry()`.

## 5. Corrección

- **`ApplicationPolicy::viewFile()`, capacidad nueva:** el expediente interno solo para RR. HH. y Aprobador de la organización de la postulación.
- **`ApplicationController`** autoriza con `viewFile` en lugar de `view`.
- **`ApplicationPolicy::view` no cambia.** La sigue usando `CandidateApplicationController::show`, la vista del candidato, que solo entrega convocatorias.
- **La protección está en el backend.** La respuesta del candidato es un 403 sin props: no se ocultó nada en React. Ninguna notificación ni página del candidato enlazaba a la ruta interna (todas usan `candidate.applications.show`), así que ningún flujo legítimo cambia.

## 6. Matriz de autorización comprobada

| Actor | `GET /postulaciones/{id}` | Comprobación |
|---|---|---|
| Candidato propietario | **403**, sin ningún marcador interno | Prueba 1 (era 200 con datos internos) |
| Otro candidato | 403, sin datos | Prueba 2 |
| RR. HH. y Aprobador de la misma organización | 200, con el historial, las observaciones, los puntajes, los comentarios y el resultado de la entrevista | Prueba 3 |
| RR. HH. y Aprobador de otra organización | 404, sin datos (aislamiento por `OrganizationScope`) | Prueba 4 |
| Solicitante y evaluador de la misma organización | 403, sin datos | Prueba 5 |
| Evaluador asignado, en sus sesiones | 200 en `evaluaciones/{id}` y `entrevistas/{id}` | Prueba 6 |
| Candidato propietario, en su vista | 200 en `mis-postulaciones` y `mis-postulaciones/{id}`. Recibe las convocatorias con fecha, modalidad, lugar, indicaciones y estado, sin `observations`, `outcome`, `results` ni `evaluator`, y sin `history`, `assessments` ni `application.candidate`. `view` sigue permitiéndole su postulación | Prueba 7 (props de Inertia) |
| Invitado | Redirección a `login` | Prueba 8 |

## 7. Pruebas ejecutadas

Todas en Docker, sobre PostgreSQL, con la base aislada `reclutamiento_testing`. Comprobado antes de ejecutar:

- la base existe por separado de `reclutamiento` y de `reclutamiento_e2e`;
- `phpunit.xml` la fuerza con `force="true"`.

| Orden | Resultado real |
|---|---|
| Prueba focal, RED, sobre la base | 1 fallo y 7 aciertos (146 aserciones) |
| Prueba focal, GREEN, con la corrección | **8 aprobadas** (153 aserciones) |
| `php artisan test` de Applications, Assessments, Tenancy, Candidates, Routing, Selection y Notifications | 100 aprobadas (677 aserciones) |
| `docker compose exec app php artisan test` | **419 aprobadas y 8 omitidas** (1651 aserciones), 0 fallos. Las 8 omitidas son las preexistentes de verificación de correo de Fortify, una función desactivada |
| `docker compose exec app npm run build` | Correcto: 2375 módulos, salida 0 |
| `docker compose exec app npx tsc --noEmit` | 0 errores, salida 0 |
| `npm run cy:run` (Cypress, entorno E2E aislado con `reclutamiento_e2e`) | **«All specs passed!»**: 20 specs y 85 de 85 pruebas en 06:19, salida 0. Incluye los specs que pasan por el expediente o por la vista del candidato: e2e-05, e2e-06, e2e-11, e2e-12 y e2e-13. Sin cambios en `data-cy` |

## 8. Archivos

| Archivo | Cambio |
|---|---|
| `app/Policies/ApplicationPolicy.php` | Capacidad `viewFile` |
| `app/Http/Controllers/Applications/ApplicationController.php` | Autoriza con `viewFile` |
| `tests/Feature/Applications/ApplicationFileAuthorizationTest.php` | 8 pruebas HTTP nuevas |
| `docs/v1.1/security/SEG-01-expediente-interno-postulante.md` | Este documento |
| `docs/defects.md` | Fila DEF-14 |

Trazabilidad: A-21 y A-14 → `ApplicationPolicy::viewFile` y `ApplicationController` → `ApplicationFileAuthorizationTest`, pruebas 1 a 8.

## 9. Limitaciones y pendientes

- **Auditoría de Codex pendiente.** Este documento no cierra el ciclo.
- **`view` sigue admitiendo a RR. HH. y Aprobador.** Hoy solo la usa la vista del candidato, bajo `role:postulante`. Que el personal la conserve no abre ningún acceso, pero restringirla al candidato sería otro cambio, fuera de este alcance mínimo.
- **No se revisaron otros endpoints con el mismo patrón.** SEG-02, SEG-03 y SEG-04 quedan fuera de este incremento y no se implementó nada de ellos.
- **Validador de F36-SBX.** Al integrar este cambio en `develop` o `main`, ese validador fallará por diseño en la regla FRZ, porque detecta cambios ajenos a F36-SBX desde su base. Es el anclaje documentado en su README: se valida anclado en su rama. No es un defecto de este incremento.
- **Datos.** Las pruebas usan solo datos ficticios generados por las factories.
