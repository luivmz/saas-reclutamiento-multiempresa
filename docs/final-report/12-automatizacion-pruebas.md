# Capítulo 12. Automatización de pruebas

Documentación detallada de la suite: **`docs/testing/cypress-e2e.md`**.

## 12.1 Herramienta y entorno

| Elemento | Valor |
|---|---|
| Herramienta | Cypress **15.3.0** (imagen oficial `cypress/included:15.3.0`) |
| Navegador | **Electron 136**, *headless* |
| Ejecución | Servicio `cypress` de Docker Compose (perfil `e2e`) contra `http://app-e2e:8000` |
| Entorno de la aplicación | `app-e2e` + `queue-e2e` con `APP_ENV=e2e`, base `reclutamiento_e2e` y Redis DB 2/3 |
| Datos | `DemoSeeder` ficticio y reproducible, restablecido antes de cada spec (o de cada test que modifica datos) |
| Aislamiento de tests | `testIsolation: true`; sin reintentos (`retries: 0`) |
| Evidencia | Capturas solo en fallos; sin video |

Comandos: `npm run cy:run` (suite completa) y `npm run cy:run -- --spec "cypress/e2e/e2e-10-*.cy.js"` (un spec). `cy:run` crea `.env.e2e` si falta y levanta el entorno E2E.

## 12.2 Reset protegido

Antes de cada spec, `cy.resetDatabase()` llama a `POST /__e2e/reset`, que ejecuta `migrate:fresh --seed`, vacía la cola y limpia la caché. El endpoint tiene cuatro barreras, todas cubiertas por PHPUnit:

1. Responde 404 si `E2E_ENABLED` no está activo o el entorno es producción.
2. Responde 403 sin el token `X-E2E-Token` correcto (`hash_equals`).
3. Responde 409 si la base activa no es exactamente `E2E_DATABASE` (DEF-13).
4. `E2eEnvironment::reset()` vuelve a verificar la base antes de `migrate:fresh`.

Las notificaciones en cola se esperan con `cy.waitForQueue()`, que consulta el tamaño real de la cola en lugar de usar esperas fijas.

## 12.3 Specs

| ID | Spec | Qué automatiza | Tests |
|---|---|---|---|
| Soporte | `e2e-00-app-dates.cy.js` | Fechas de los formularios en `America/Lima` (DEF-12) | 3 |
| E2E-01 | `e2e-01-login.cy.js` | Login real de los 5 roles con el menú correcto; credenciales inválidas | 6 |
| E2E-02 | `e2e-02-register-job-request.cy.js` | Registrar y enviar un requerimiento; formulario vacío rechazado | 2 |
| E2E-03 | `e2e-03-approve-job-request.cy.js` | Aprobar un requerimiento; rechazo sin motivo impedido | 2 |
| E2E-04 | `e2e-04-configure-publish-vacancy.cy.js` | Crear, validar y publicar una vacante; ponderaciones ≠ 100 impiden publicar (botón deshabilitado y 422 en el servidor) | 2 |
| E2E-05 | `e2e-05-candidate-apply.cy.js` | Perfil, carga de CV, postulación y confirmación | 1 |
| E2E-06 | `e2e-06-shortlist-candidate.cy.js` | Preselección con notificación; descarte sin motivo impedido | 2 |
| E2E-07 | `e2e-07-evaluator-records-results.cy.js` | El evaluador registra puntajes; puntaje fuera de rango rechazado | 1 |
| E2E-08 | `e2e-08-comparison-ranking.cy.js` | Ranking ponderado (85.5 / 83.5 / 68.5); **nadie queda seleccionado** y RR. HH. no puede decidir | 1 |
| E2E-09 | `e2e-09-human-final-decision.cy.js` | Decisión humana con justificación y confirmación, eligiendo al 2.º del ranking; los estados no cambian | 2 |
| E2E-10 | `e2e-10-selection-and-closure.cy.js` | Selección, cierre, «No seleccionado» para el resto y notificación de resultado a cada candidato | 1 |
| E2E-11 | `e2e-11-multitenancy.cy.js` | Aislamiento entre organizaciones: listados, IDs ajenos, auditoría | 4 |
| E2E-12 | `e2e-12-negative-rules.cy.js` | Rol sin permiso, postular a vacante cerrada, decisión no autorizada, selección tras el cierre | 4 |
| E2E-13 | `e2e-13-full-recruitment-flow.cy.js` | Flujo integral (12 pasos) | 12 |
| **Total** | **14 specs** | | **43** |

## 12.4 Flujo integral automatizado (E2E-13)

Un spec ordenado en el que cada `it` es un traspaso entre roles; se justifica porque el proceso es secuencial por naturaleza:

1. El área solicitante registra y envía el requerimiento.
2. RR. HH. lo valida.
3. El aprobador lo aprueba.
4. RR. HH. genera, valida y publica la vacante.
5. El postulante completa su perfil, carga su CV y postula.
6. RR. HH. preselecciona y programa evaluación y entrevista.
7. El evaluador registra los resultados de ambas sesiones.
8. RR. HH. pasa la postulación a finalista y consulta el ranking: **no existe decisión** hasta el paso 9.
9. El aprobador registra la **decisión final humana**.
10. RR. HH. registra la selección y cierra la convocatoria.
11. El postulante ve «Seleccionado» y la notificación de resultado.
12. El aprobador consulta la auditoría (cierre, selección, decisión, notificación).

## 12.5 Buenas prácticas aplicadas

- Selectores estables `data-cy` y atributos de datos; sin clases de Tailwind ni textos frágiles.
- Sin `cy.wait` arbitrarios: se espera a la URL, a elementos visibles, al estado de la interfaz y a la cola vacía.
- Comandos personalizados solo donde reducen duplicación: `dataCy`, `resetDatabase`, `loginAs` (`cy.session`), `waitForQueue`, `appRequest` e `idFromPath`.
- Los negativos combinan interfaz (la acción no se ofrece) y HTTP (el servidor la rechaza).

## 12.6 Resultados reales

| Corrida | Specs | Tests | Passed | Failed | Skipped | Duración |
|---|---|---|---|---|---|---|
| Fase 9, suite completa, 1.ª | 13 | 40 | 40 | 0 | 0 | 04:01 |
| Fase 9, suite completa, 2.ª | 13 | 40 | 40 | 0 | 0 | 03:56 |
| Fase 10, instalación limpia | 14 | 43 | 43 | 0 | 0 | 03:26 |
| Fase 10, entorno principal | 14 | 43 | 43 | 0 | 0 | 03:34 |

- **Defectos de la aplicación encontrados por la suite:** ninguno.
- **Tests corregidos por expectativas erróneas:** 2 (E2E-04 y E2E-10).
- **Defectos de la infraestructura de pruebas corregidos en la Fase 10:** DEF-12 y DEF-13.

## 12.7 Limitaciones

- Solo se probó Electron 136.
- `cy:open` está documentado pero no se ejecutó.
- No hay integración continua.
- La suite dura unos 3,5 min en serie.
