# SaaS Reclutamiento Multiempresa — contexto del proyecto

Plataforma SaaS multiempresa para reclutamiento, evaluación y selección de personal. Caso de estudio: Colegio Andino de Huancayo. Proyecto académico de la Universidad Continental, curso Pruebas y Calidad de Software, NRC 28607, docente Dr. Maglioni Arana Caparachin. Integrantes: Coronacion Meza Fredy, Peña Arroyo Anthony y Vila Meza Luis Antonio.

Stack real: Laravel 13 (PHP 8.4) + React 19 + TypeScript + Inertia 3 + Tailwind 4, PostgreSQL 17, Redis 7, PHPUnit, Cypress 15 y Docker Compose. En `develop` (v1.1) se suma el servicio experimental `ml-service/`: Python, scikit-learn y FastAPI, con `pytest`.

## Antes de cambiar cualquier cosa

**Usa la skill `project-guardian`.** Define el procedimiento obligatorio: qué leer primero, en qué rama trabajar, qué pruebas exigir y cuándo detenerse. Las demás skills del proyecto se apoyan en ella:

| Skill | Cuándo |
|---|---|
| `project-guardian` | Siempre, antes de editar o planificar |
| `laravel-saas-quality` | Backend Laravel: controladores, servicios, Policies, migraciones, pruebas |
| `academic-traceability` | Documentación, trazabilidad RF y entregables del curso |
| `powerdesigner-uml` | Diagramas UML/PlantUML derivados del código real |
| `ml-risk-service` | Servicio de riesgo operacional (RF-29): **implementado en `develop` como experimental** (Fases 15–17); marco, fronteras y evidencia exigida |
| `recruitment-3d-experience` | 3D público y progresivo: **implementado y acotado** a la portada con CSS 3D (Fase 20); condiciones para ampliarlo |

Skills externas instaladas (ver `PROVENANCE.md` de cada una): `frontend-design`, `animate` y `reviewing-a11y`.

## Contratos inviolables

1. **RF-01 a RF-27 conservan su número y su significado.** No se renumeran, eliminan ni reinterpretan.
2. **El sistema nunca selecciona, descarta ni contrata automáticamente.** El ranking calcula, ordena y compara; nada más.
3. **La decisión final pertenece al Aprobador/Dirección**, con confirmación humana explícita y justificación (RF-23).
4. **El ML es informativo y operacional**, sobre el proceso, nunca evaluando, puntuando ni clasificando personas. Vale para el servicio actual (RF-29) y para cualquier ML futuro.
5. **Se preservan la multiempresa (`organization_id`), las Policies, los roles y las pruebas cross-tenant.**
6. **Se preserva la auditoría segura y de solo inserción** (`AuditLogger` + trigger `audit_logs_append_only`).
7. **Solo datos ficticios.** Nunca datos personales reales ni PII.
8. **Nunca se versionan secretos** (`.env`, `.env.e2e`, tokens, claves).
9. **El tag `v1.0.0-academic` (`9a946c2`) no se mueve, borra ni reutiliza**, y la historia de v1.0 no se reescribe.
10. **Sin `push`, `merge`, release ni tag sin autorización explícita del equipo.**

## Documentación fuente

No dupliques estos documentos: enlázalos.

| Tema | Documento |
|---|---|
| Estado por fase | `docs/PROGRESS.md` |
| Trazabilidad RF-01 a RF-27 | `docs/final-report/traceability-master.md` · `docs/rf-implementation-matrix.md` |
| Decisiones de negocio (A-01…A-36) | `docs/assumptions.md` |
| Defectos (DEF-01…DEF-13) | `docs/defects.md` |
| Evidencia TDD | `docs/tdd-evidence.md` |
| Entorno y Docker | `docs/docker.md` |
| Suite E2E | `docs/testing/cypress-e2e.md` |
| Usuarios demo ficticios | `docs/demo-users.md` |
| Informe académico (14 capítulos) e informes de diagramas | `docs/final-report/` |
| Planificación y fases de v1.1 (F13–F26) | `docs/v1.1/` — cada fase en su `phase-*.md` |
| Release v1.1 (changelog, notas, manifiesto, aceptación) | `CHANGELOG.md` · `docs/v1.1/release-notes-v1.1.md` · `docs/v1.1/release-manifest-v1.1.md` · `docs/v1.1/final-acceptance-checklist.md` |
| Formato 09 (fuentes, entregable final v1.1 y mapa de fuentes) | `docs/academico/phase-24/` |
| Línea académica post-release (F27+) | `docs/academico/ACADEMIC_BASELINE.md` · `docs/academico/` |
| Modelos PowerDesigner de v1.1 (OOM, PDM y exportaciones) | `docs/v1.1/powerdesigner/` |
| Divergencias documentales entre v1.0 y v1.1 | `docs/v1.1/documentation-update-map.md` |
| Candidatos RF-28+, RNF y decisiones pendientes | `docs/v1.1/scope-preliminary.md` |

## Comandos habituales

Laravel y el frontend corren en Docker; no hay PHP ni Node locales del proyecto. El servicio ML es la excepción (ver abajo).

```
docker compose up -d --wait                                   # levantar
docker compose exec app php artisan test                      # PHPUnit (v1.0: 244 pruebas; develop: 408 + 8 omitidas; F25: 411 + 8)
docker compose exec app npm run build                         # compilar frontend
docker compose exec app npx tsc --noEmit                      # tipos
docker compose exec app npx vp test --run                     # pruebas de componente (develop)
npm run cy:run                                                # Cypress (entorno E2E aislado)
docker compose exec app php artisan migrate:fresh --seed --force   # datos demo
```

El servicio ML **no** corre en Docker Compose: se ejecuta desde `ml-service/` con su entorno virtual (`cd ml-service` y `.venv/Scripts/python.exe -m pytest`; el servidor, con `uvicorn` en el puerto 8008). Laravel solo lo llama si `ML_SERVICE_ENABLED=true`, y sin servicio la página funciona igual. Detalle en `docs/v1.1/phase-16-laravel-ml-integration.md`.

## Estado vigente F34E

F34E CERRADA (05/10/2026), tras auditoría final PASS y adaptación explícita de alcance para cierre/handoff. Este bloque sustituye el estado vigente anterior; los registros hasta F34D se conservan como fotografías históricas, no como instrucciones actuales.

- G0 real = NO APROBADA
- G0-09 = CUMPLIDO
- G0-14 = CUMPLIDO
- G0-02 = PENDIENTE EXTERNO
- G0-03 = PENDIENTE EXTERNO
- G0-12 = PENDIENTE EXTERNO
- ADR-005 = PROPUESTA
- G0-SBX = APROBADA CON RESTRICCIONES
- F35 productiva = BLOQUEADA
- F35-SBX = HABILITADA
- F36–F40 = BLOQUEADAS
- Alcance C = BLOQUEADO
- Datos reales = PROHIBIDOS

SBX-01..SBX-18 CUMPLE. Aprobación interna del equipo REGISTRADA; no constituye aprobación jurídica, de privacidad ni validación institucional. F35-SBX exclusivamente sintético. F35-SBX-A CERRADA — diseño, contratos, fixtures sintéticos y validador completados, tras auditoría independiente PASS. Sin runtime productivo ni capacidades de alcance C. F35-SBX-B NO INICIADA. RF-23 sigue humana; RF-29 sigue experimental/informativa. Sin scoring, recomendación ni selección automática; sin documentos, audio ni vídeo reales, sin integración productiva ni paso automático a producción. El baseline RF/CU/RNF permanece intacto.

Commits F34E: A `0ea5e63bb84db717bcc5f2a94c3c93572d5b863e`; B `c016a75401eb127aa11cd9185423e2866b0fc936`. El commit C y los merges se consultan en Git, sin hashes futuros/autorreferenciales. Publicación autorizada únicamente tras regresión y CI GREEN de develop/main. Sin tag ni release. El handoff macOS está publicado; F35-SBX-A queda cerrada documentalmente en `feature/f35-sbx-synthetic-evidence-pipeline`, con publicación pendiente de regresión post-commits y CI. F35-SBX-B NO INICIADA; requiere autorización nueva.

## Antecedentes de estado (hasta F34D)

*Baseline previo a la integración F34 verificado con Git el 04/10/2026. F31–F33 están integradas; los hashes siguientes son la fotografía pre-F34. F34 está CERRADA tras auditoría final PASS, exclusivamente con contrato, dataset sintético y gobernanza. Sus commits académicos son A `a4684d196e00fbe8fd3fdd2bea5b04d70f47bc70` y B `cafcbdbb81101fb40f91f0166019a1f5b9965de9`. Su publicación e integración están autorizadas con gates CI de develop y main; los hashes finales se consultan en Git y `docs/PROGRESS.md`, no se anticipan aquí.*

### `main` — v1.1 académica publicada y documentación post-release

**Estado vigente tras F34D (05/10/2026): F34D CERRADA** tras auditoría final **PASS**, sin cambios productivos. **G0-12 = PENDIENTE EXTERNO; G0-02 = PENDIENTE EXTERNO; G0-03 = PENDIENTE EXTERNO; G0-09 = CUMPLIDO; G0-14 = CUMPLIDO; ADR-005 canónico = PROPUESTA; aprobación interna del equipo = REGISTRADA; G0 real = NO APROBADA; F35–F40 productivas = BLOQUEADAS; datos reales PROHIBIDOS.** La respuesta textual recibida para G0-12 queda **SIN EVIDENCIA ARCHIVADA**, con identidad **NO VERIFICABLE** y sin adjunto, SHA-256 ni formato real: no constituye aprobación jurídica, de privacidad ni autorización institucional. Los cuatro adjuntos anteriores del equipo solo respaldan G0-09/G0-14. RF-23 sigue humana; RF-29 experimental/informativa; no cambia RF/CU/RNF. Commits A `f68aef551012a59468710d1706431e903106cc03` y B `be0dfeeccbff476d9f8b29c2d06ea0a8fdc20937`. Base F34D: `a8b53c94a3202af26a99e270d5ed553df07e8569`. Publicación e integración autorizadas con gates CI obligatorios; resultados y hashes finales en Git/GitHub, sin anticiparlos. **F34E/G0-SBX no se publica ni se incorpora en esta fase; su WIP permanece preservado aparte en el stash, sin aplicar ni borrar.** Sin nuevos tags ni releases.

**Fotografía histórica del cierre F34C (04/10/2026):** **F34C CERRADA** tras auditoría final **PASS**, sin cambios productivos. **G0-14 = CUMPLIDO; G0-09 = CUMPLIDO; ADR-005 canónico = PROPUESTA; aprobación interna del equipo = REGISTRADA; G0 = NO APROBADA. G0-02 = PENDIENTE EXTERNO; G0-03 = PENDIENTE EXTERNO; G0-12 = PENDIENTE EXTERNO; F35–F40 = BLOQUEADAS; datos reales PROHIBIDOS.** Hay cuatro adjuntos reales de tres integrantes: se documentan la copia histórica/restaurada de Luis y su confirmación adicional; no se confunden con aprobación jurídica, de privacidad ni institucional. RF-23 sigue humana; RF-29 experimental/informativa y RF-CAND fuera del baseline. Commits A `723001c13e193adace00650cf2c9296468483448` y B `c79fc24597ee0037978c9453df1eb762caf9497e`. Base preintegración: `develop` `619e1b217bf437376618b3eabd95d5013dba2f33`, `main` `b4d4d62456d437d313436eeffb4049f7d513d2cb`. Publicación autorizada con gates CI de develop/main; hashes de integración y resultados finales en Git/GitHub, sin anticiparlos. Sin nuevos tags ni releases.

**Fotografía histórica del cierre F34B (04/10/2026): F34B CERRADA**, tras auditoría final PASS; únicamente documentación y validadores. **G0 = NO APROBADA; ADR-005 = PROPUESTA; evidencias externas reales = 0; G0-02/03/12/14 = PENDIENTE EXTERNO; G0-09 = PARCIAL; F35–F40 = BLOQUEADAS; datos reales PROHIBIDOS.** Los formularios vacíos no aprueban nada; el control positivo permanece en memoria y no es evidencia externa. RF-23 sigue humana y RF-29 experimental/informativa. Base preintegración F34B: `develop` = `origin/develop` = `417ea4fc4a800d8663e3af7909be59e6ea302f1e`, `main` = `origin/main` = `55bdb422e39b36983053cec9c0af398564f2c81a` (F34A integrada). Entrega auditada en [`g0-evidence`](docs/academico/g0-evidence/README.md); se conserva como fotografía histórica, y el cierre vigente se registra en gobierno. Integración autorizada con gates CI develop/main; hashes finales en Git. Sin tag ni release. Las referencias de cierre de fases previas que siguen son históricas, no el HEAD vigente.

**Fotografía histórica del cierre F34A (04/10/2026): F34A CERRADA**, con auditoría final PASS; únicamente documentación y validador. Base preintegración verificada: `develop` = `origin/develop` = `1fb5a1f3663e10cc66289cb3530a8273d1b96b8f` y `main` = `origin/main` = `dc3093ea487a3694223f8f08560e390e26ec95c7` (F34 integrada). **G0 = NO APROBADA; ADR-005 = PROPUESTA; G0-02/03/12/14 = PENDIENTE EXTERNO; G0-09 = PARCIAL; F35–F40 = BLOQUEADAS; datos reales PROHIBIDOS.** El cierre F34A no aprueba el ADR, no sustituye evidencia externa y no habilita scoring/recomendación ni implementación. G0-02 exige evaluación de impacto COMPLETADA si aplica o conclusión jurídica fundamentada de NO APLICABILIDAD, nunca solo planificada. RF-23 sigue humana y RF-29 experimental/informativa. Entrega auditada en [`g0-readiness`](docs/academico/g0-readiness/README.md); sus estados preauditoría se preservan como fotografía histórica. Integración autorizada con gates CI de develop/main; hashes finales en Git. Las referencias pre-F34 siguientes son históricas, no el HEAD vigente.

- Baseline pre-F34: `main` = `origin/main` = `26ae8b34ed586fe19515dd6041491e8dd72f9a64`; contiene el release v1.1 y la documentación académica integrada hasta F33. El tag `v1.1.0-academic` conserva el cierre técnico en `634f354`; el tag histórico `v1.0.0-academic` apunta a `9a946c2` y no se mueve.
- RF-01 a RF-27 son la línea base v1.0. Sus documentos de cierre (`docs/final-report/`) siguen siendo correctos **para v1.0** y no se reescriben.

### `develop` — línea académica post-release integrada hasta F33 (baseline pre-F34)

Baseline pre-F34: `develop` = `origin/develop` = `288039fbb7eaba9827072e736d2fff4f55d10408`; `main` contiene el mismo árbol aprobado de F33 mediante el merge `26ae8b34ed586fe19515dd6041491e8dd72f9a64`. Tras el release técnico se integraron los entregables académicos F27–F33 sin cambiar el runtime.

| Fase | Contenido | Estado |
|---|---|---|
| 13 · 14 · 14.5 | Gobierno de v1.1, definición del experimento de ML, flujo multiagente | Integradas |
| 15 | `ml-service/`: dataset sintético, entrenamiento y **servicio FastAPI experimental** (`/health`, `/v1/model-info`, `/v1/predict`) | Integrada |
| 16 | **Integración Laravel ↔ FastAPI**: `vacancies.target_completion_at` (GAP-01 resuelto técnicamente), cliente HTTP con validación y *fallback*, tarjeta de riesgo operacional | Integrada |
| 17 | Validación ML y regresión integral | Integrada |
| 18 · 19 | **Rediseño del frontend** y **motion** (sin biblioteca nueva, con movimiento reducido) | Integradas |
| 20 | **Experiencia 3D con CSS 3D**, solo en la portada pública | Integrada |
| 21 | QA visual, accesibilidad y responsive | Integrada (`aced6da`) |
| 22 | Especificación UML del AS-IS, solo documentación (`docs/v1.1/uml/`) | Integrada (`2621bee`) |
| 23 | Formalización en PowerDesigner: OOM y PDM nativos, 22 diagramas exportados (`docs/v1.1/powerdesigner/`) | Cerrada e integrada (`8211851`) |
| 24 | Documentación académica final: Formato 09 v1.1 (`docs/academico/phase-24/`) | Cerrada con observaciones e integrada (`4469128`) |
| 25 | QA global final / *release readiness* (`docs/v1.1/phase-25-final-qa.md`) | Cerrada con observaciones e integrada (`2b97fe3`) |
| 26 | GitHub, *release* y cierre de v1.1 (`docs/v1.1/phase-26-release-closeout.md`) | Cerrada; tag `v1.1.0-academic` publicado sobre `634f354` |
| 27–29 | Formatos académicos F2–F11, F11 oficial, PowerDesigner, matriz, plan y QA | Integradas en `develop` y `main`; ver `docs/academico/ACADEMIC_BASELINE.md` |
| 30 | Investigación científica y tecnológica para IA de reclutamiento | Integrada (`develop` `2bf2a1e`; `main` `59849c3`), solo documentación |
| 31 | Cierre de deuda LOW y saneamiento documental | CERRADA con observaciones aceptadas/futuras; integración autorizada con CI obligatorio, sin cambios productivos. Hashes finales en Git |
| 32 | Auditoría académica global y salvaguardas para F33 | CERRADA CON OBSERVACIONES e integrada (`develop` `d6094187`; `main` `40a79ede`), con CI verde |
| 33 | Diseño funcional del motor inteligente y ADR-005 / G0 | CERRADA e integrada (`develop` `288039f`; `main` `26ae8b34`); auditoría final PASS; solo documentación |
| 34 | Contrato de datos, dataset sintético y gobernanza | CERRADA tras auditoría final PASS; 19 CSV, 120 vacantes, exclusivamente sintética; integración autorizada con gates CI |
| 34A | Paquete G0, jurídico/privacidad preliminares, necesidad institucional, amenazas y RF candidatos | CERRADA tras auditoría final PASS; G0 NO APROBADA; ADR-005 PROPUESTA; pendientes externos y G0-09 PARCIAL; solo documentación |
| 34B | Formularios/matriz de evidencias externas y validadores endurecidos | CERRADA tras auditoría final PASS; evidencias externas reales = 0; G0 NO APROBADA; ADR-005 PROPUESTA; F35–F40 BLOQUEADAS; datos reales PROHIBIDOS |
| 34C | Evidencia real de aprobación interna del equipo y aceptación del threat model | CERRADA tras auditoría final PASS; G0-14/G0-09 CUMPLIDOS; ADR-005 canónico PROPUESTA; aprobación interna REGISTRADA; G0 NO APROBADA; G0-02/03/12 PENDIENTE EXTERNO; F35–F40 BLOQUEADAS; datos reales PROHIBIDOS |
| 34D | Registro de respuesta G0-12 sin evidencia archivada e identidad no verificable | CERRADA tras auditoría final PASS; G0-12/02/03 PENDIENTE EXTERNO; G0-09/14 CUMPLIDOS; G0 NO APROBADA; F35–F40 productivas BLOQUEADAS; F34E/G0-SBX no publicada |

**Puerta G0 tras F34: NO APROBADA. ADR-005: PROPUESTA.** El cierre de las fases de diseño y datos no aprueba el ADR ni habilita implementación. F34 queda CERRADA únicamente con datos sintéticos y gobernanza, sin scoring ni recomendación de personas. F35–F40 permanecen bloqueadas. No se autorizan datos reales por consentimiento ni por el cierre F34: cualquier uso futuro requiere autorización adicional explícita y revisión contractual, jurídica y de privacidad. Fuentes vigentes: [`F33`](docs/academico/diseno-inteligente/README.md), su mapa de fases y el cierre F34 en `docs/PROGRESS.md`. Los estados preauditoría de los entregables F33/F34 se conservan como fotografías históricas de entrega. RF-23 sigue humana y RF-29 experimental, informativa y operacional; no cambia ningún contrato ni el baseline RF-01 a RF-27.

**ML (RF-29).** Implementado e integrado **experimentalmente**: validado técnicamente con datos sintéticos, **no** validado institucionalmente ni autorizado para producción. Estima el riesgo de demora del **proceso**; no puntúa, ordena, selecciona ni descarta personas, no toca el ranking y no cambia RF-23. Contrato científico congelado, no se modifica: *freeze* `9ee1843055e75d4039dd84fd666db7a594e1a45ec7e9b354820fabfcb21ebcd2`, *threshold* `0.1679418172266036`, Logistic Regression `C=10`, `class_weight=None`, `StandardScaler`, sin calibración.

**3D.** Una sola superficie —la tarjeta del expediente de la portada pública—, con **CSS 3D** (perspectiva y capas de DOM): sin WebGL, Three.js, React Three Fiber ni Spline, y sin dependencias nuevas. Decorativa, fuera de todo flujo operativo, con póster de respaldo (movimiento reducido, pantallas de menos de 1024 px, ahorro de datos, equipos modestos o fallo del fragmento). **No se amplía sin una nueva decisión del equipo** (ADR-003 y skill `recruitment-3d-experience`).

**Requisitos.** RF-28, RF-29 y los RNF nuevos (RNF-A, RNF-B, RNF-C…) siguen siendo **candidatos** en `docs/v1.1/scope-preliminary.md`: implementar algo no lo promueve al baseline (decisión 11). La promoción de RF-28, RF-29 y RNF-C es una decisión pendiente del equipo (preguntas 12 y 13).

> Historia: hasta el hotfix documental de la Fase 21 esta sección decía que `main` y `develop` tenían el mismo contenido y que la Fase 13 era solo gobierno, sin ML, FastAPI, rediseño, motion ni 3D. Era cierto al abrir v1.1 (19/09/2026); dejó de serlo al integrarse las Fases 13 a 20.

## Permisos

No amplíes permisos por comodidad. `.claude/settings.local.json` es local y no se versiona; cualquier cambio de permisos, instalación global de skills o ejecución de hooks externos requiere autorización explícita del equipo.
