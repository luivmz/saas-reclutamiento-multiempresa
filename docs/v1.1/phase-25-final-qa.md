# Fase 25 — QA global final / release readiness de v1.1

**Fecha:** 24–25 de septiembre de 2026
**Rama:** `feature/phase-25-final-qa` · **Base:** `4469128` (cierre de la Fase 24)
**Writer principal:** Claude Code · **Reviewer:** Codex (auditoría posterior)

> Fase de **verificación**. No agrega funciones, no promueve RF-28, RF-29 ni RNF-C, no cambia el modelo ML, su *freeze* ni su *threshold*. Solo se corrigieron defectos objetivos encontrados por el QA, cada uno con su prueba. Matriz de controles: [`phase-25-qa-matrix.md`](phase-25-qa-matrix.md).

---

## 1. Objetivo

Responder: *¿la versión v1.1 completa está técnicamente consistente, reproducible, trazable y suficientemente estable para pasar a la Fase 26 (release y cierre)?* Para eso se ejecutaron todas las suites, se revisaron la seguridad, la multitenencia, la frontera del ML y la experiencia visual, y se verificaron los artefactos documentales.

## 2. Baseline

| | |
|---|---|
| `develop` = `origin/develop` = HEAD inicial | `4469128a7363ecc9221999cbc53b2288445d1ad7` (*merge: close phase 24 academic documentation*) |
| `main` = `origin/main` | `4563c696ba08fd6d2a689af733020d849edebad2` (v1.0 académica) |
| `v1.0.0-academic^{}` | `9a946c202ef7473230e8efa371ace13479ab889c` |
| Fases cerradas | F0–F12 (v1.0) y F13–F24; F23 cerrada; F24 cerrada con observaciones |
| Línea base funcional | RF-01 a RF-27. RF-23 humano. RF-28 candidato no implementado. RF-29 experimental (proceso, no personas). RNF-C propuesta |
| Referencias históricas | F21: PHPUnit 408 + 8 omitidas · pytest 532 · componentes 42 · Cypress 20 specs / 84 tests |

## 3. Entorno

| Elemento | Valor | Nota |
|---|---|---|
| Sistema | Windows 11 Pro 10.0.26200 | — |
| Hardware | AMD Ryzen 9 5900X (12 núcleos / 24 hilos), 31,9 GB RAM, SSD NVMe WD SN350 1 TB | **No es un equipo modesto** (§21) |
| Docker | Docker 29.7.2 (Docker Desktop, 24 CPU y 16,7 GB para la VM), Compose v5.5.1 | Servicios `app`, `queue`, `postgres`, `redis`, `app-e2e`, `queue-e2e`, todos *healthy* |
| Contenedor `app` | PHP **8.4.25**, Composer 2.10.3, Node 22.23.2, npm 10.9.8, Laravel **13.31.0** | Donde corren PHPUnit, `tsc`, Vitest y el build |
| Bases de datos | PostgreSQL **17.11** (`postgres:17.11-alpine`), Redis **7.4.11** | Postgres y Redis publicados solo en `127.0.0.1` |
| Servicio ML | `ml-service/.venv`: Python 3.12.5, pytest 8.3.3 | Fuera de Compose, como está documentado |
| Cypress | Imagen `cypress/included:15.3.0`, Electron 136 (headless), Node 22.20.0 | — |
| Host (no usado por el proyecto) | PHP 8.2.12 (XAMPP), Composer 2.10.2, Node 20.16.0, npm 10.8.1, git 2.55.0, Python 3.12.5 | INFO: el proyecto no usa PHP ni Node del host |

**Configuración de Laravel** (`php artisan about`): entorno `local`, *debug* activado (desarrollo), zona `America/Lima`, locale `es`; drivers pgsql, redis (caché, cola y sesión) y mail `log`. **93 rutas**. `optimize:clear` sin errores.

**Migraciones** (`migrate:status` en la base de desarrollo): 18, todas `Ran`. PHPUnit usa la base aislada `reclutamiento_testing` (`force="true"` en `phpunit.xml`) y Cypress usa `reclutamiento_e2e`. No se ejecutó `migrate:fresh` fuera del entorno E2E.

## 4. Herramientas

No se instaló, actualizó ni desinstaló nada. Se usaron las herramientas existentes:

- Docker Compose y los contenedores del proyecto;
- el entorno virtual del servicio ML;
- la imagen de Cypress fijada;
- `pdftotext` (Git for Windows), en lugar del `pdftext.swift` de macOS, para validar el Formato 09;
- PowerShell y CIM para el inventario de hardware.

Dependencias: `composer validate` válido; `composer install --dry-run` → *Nothing to install, update or remove*; `npm ls --depth=0` sin errores. **Sin `composer update` ni `npm update`.**

## 5. Preflight

`git status --short --branch`, `git rev-parse HEAD develop origin/develop main origin/main v1.0.0-academic^{}` y `git log -15`: **todo coincide** con lo esperado (§2), árbol limpio, en `feature/phase-25-final-qa`.

## 6. Suites ejecutadas

| Suite | Comando | Inicial | Tras los arreglos |
|---|---|---|---|
| PHPUnit | `docker compose exec app php artisan test` | 408 passed · 8 skipped · 0 failed · 1478 assertions · 50,87 s | **411 passed · 8 skipped · 0 failed · 1498 assertions · 55,50 s** |
| pytest | `ml-service/.venv/Scripts/python.exe -m pytest` | 532 passed · 0 failed · 0 skipped · 58,72 s | **533 passed · 65,59 s** |
| TypeScript | `docker compose exec app npx tsc --noEmit` | 0 errores | **0 errores** |
| Componentes | `docker compose exec app npx vp test --run` | 6 archivos · 42 passed | **42 passed** |
| Build | `docker compose exec app npm run build` | 2375 módulos · 27,63 s · 0 avisos | **2375 módulos · 30,18 s · 0 avisos** |
| Cypress | `npm run cy:run` | 20 specs · 84/84 · 5:13 | **20 specs · 85/85 · 5:24** |

Pruebas nuevas: PHPUnit +3 (2 de rutas y 1 cross-tenant de evaluaciones), pytest +1 (y una aserción nueva en la CLI) y Cypress +1 (evaluaciones asignadas en E2E-16). Ninguna prueba se eliminó ni se debilitó.

## 7. Resultados Laravel

- **0 fallos.** Las **8 omitidas** son pruebas del *starter kit* para la verificación de correo de Fortify, desactivada por diseño (A-01): «Fortify feature [email-verification] is not enabled». INFO.
- Evidencia por área crítica: autenticación (9 archivos), requerimientos, vacantes, postulaciones, evaluaciones y entrevistas, ranking (unitarias y de comparación), decisión final (10 pruebas), selección y cierre, auditoría (3 archivos, 16 pruebas), CV privado, notificaciones y ML (8 archivos).

## 8. Resultados Python

**533 passed, 0 failed, 0 skipped** (65,59 s). `filterwarnings = "error"` convierte cualquier aviso en fallo, así que no quedan avisos, salvo el único silenciado a propósito (alias de `anyio` en `starlette.testclient`, código de terceros). Se ejecutó con `-p no:cacheprovider` para no dejar `.pytest_cache`.

Nota operativa: el comando del README (`pytest -q`) suma su `-q` al `addopts = "-q"` y resulta en `-qq`, que oculta la línea de resumen; sin el `-q` extra el resumen aparece.

## 9. Integración ML

**Contrato congelado.** Verificado cargando el artefacto en solo lectura:

- `Pipeline(StandardScaler, LogisticRegression)` con `C=10.0` y `class_weight=None`, sin envoltura de calibración;
- *freeze* `9ee1843055e75d4039dd84fd666db7a594e1a45ec7e9b354820fabfcb21ebcd2`;
- *threshold* `0.1679418172266036`.

Coincide con `config/ml.php` y con los metadatos del artefacto. **Nada cambió.**

**API FastAPI en vivo** (uvicorn en `0.0.0.0:8008` con un token efímero generado para la prueba y borrado después):

- `GET /health`: `model_ready: true`.
- `GET /v1/model-info`:
  - `logistic_regression`, con el *freeze* y el *threshold* exactos;
  - `deployment_status: experimental`;
  - `gap_01_open: false`;
  - 15 features.
- `POST /v1/predict`:
  - la *request* tiene 15 enteros (`extra="forbid"`, `strict=True`);
  - la respuesta tiene **exactamente** `risk_score`, `risk_flag`, `threshold`, `model_version`, `freeze_fingerprint` y `status`, sin `uncertainty`;
  - sin token → **401**; con `candidate_id` extra → **422**; con `"2"` en lugar de `2` → **422**.

**Laravel → FastAPI real.** Se llamó a `OperationalRiskService::assess` desde el contenedor, con las variables ML solo en ese proceso; el `.env` no se tocó.

- Ninguna vacante demo tiene plazo objetivo, así que todas dan `descriptive_only` con motivo `missing_target_completion_at`, o `vacancy_not_published` en la de borrador. Es lo correcto: no se llama al modelo.
- Para ejercitar el camino real se asignó un plazo **solo en memoria**, sin `save()`, a una vacante publicada:

| Caso | Resultado |
|---|---|
| Token correcto | `predictive_available` · `risk_score` 0,2668 · `risk_flag` true · *freeze* y *threshold* exactos · 43 ms |
| Token incorrecto | `unavailable` (FastAPI 401; *fail-closed*) |
| Servicio deshabilitado (configuración real) | `descriptive_only (service_disabled)` |

En los tres casos la base no cambió (`target_completion_at` siguió en `null`) y no se escribió ningún registro de auditoría de riesgo. El 401 se informa como motivo `server_error`, **por diseño** (documentado en `phase-16` y probado en `test_a_401_falls_back_without_breaking`): INFO.

## 10. Frontend y componentes

Vitest: 6 archivos y **42 pruebas** (DataTable, experiencia 3D, formularios, contraseña, *motion* y QA visual), en verde antes y después de los arreglos.

**Frontera RF-29 en la interfaz y el servicio.**

- `app/Services/Ml/*` solo hace lecturas `count` y `max`, filtradas por `organization_id`.
- `risk_score` no está en ningún modelo ni migración: no se persiste.
- El servicio no llama a auditoría, notificaciones, transiciones de etapa, ranking ni decisión final.
- El *payload* son 15 conteos y días, sin IDs ni PII.
- E2E-15 verifica que la tarjeta no habla de candidatos, ranking ni recomendaciones, y que declara que no decide.

Ninguna violación.

## 11. TypeScript

`tsc --noEmit`: **0 errores** (8 s), antes y después de los arreglos.

## 12. Build

`npm run build`:

- 2375 módulos, 98 artefactos en `public/build/assets` (ignorado por Git);
- 27,63 s, y 30,18 s tras los arreglos;
- **0 avisos**;
- mayores *chunks*: `wayfinder` 338,83 kB, `app` 204,31 kB y CSS 99,88 kB (sin comprimir).

## 13. Cypress

`npm run cy:run`, Cypress 15.3.0 y Electron 136 *headless*, sin reintentos:

- **20 specs y 85 tests, 85/85, 0 fallidos, 0 pendientes y 0 omitidos, en 5:24**;
- antes de ampliar E2E-16 eran 84/84, en 5:13.

La guía `docs/testing/cypress-e2e.md` seguía en los 14 specs de v1.0 (F25-L02); se le añadió la §9 con los specs de v1.1.

## 14. Multitenencia

**Sin fuga cross-tenant.** Revisión de *scopes* globales, Policies, *route model binding* y consultas:

- **Evidencia en pruebas.** 22 pruebas con nombre cross-tenant explícito, `CrossTenantAccessTest`, `OrganizationScopeTest`, `MlCrossTenantValidationTest` (10 pruebas) y E2E-11. Cubren requerimientos, vacantes, postulaciones, entrevistas, ranking, comparación, decisión (RF-23), selección, cierre, notificaciones (RF-26), auditoría (RF-27), ML y CV.
- **Hueco cubierto en esta fase.** Las **evaluaciones** tenían pruebas de «evaluador de la misma organización» y de «solo el evaluador asignado», pero no un caso explícito entre organizaciones. Se agregó `EvaluationTest::test_actors_of_another_organization_cannot_schedule_view_or_record_evaluations`: RR. HH. y un evaluador de otra organización no programan, no ven y no registran. Es una prueba de caracterización: el comportamiento ya era correcto, con 6 aserciones.
- **Descarga de CV.** Requiere `auth` y la Policy compara rol **y** organización: RR. HH. o Aprobador solo si el postulante postuló a su organización; el Evaluador solo si está asignado en su organización. El disco es `local` privado y se envía `nosniff`. RR. HH. de otra organización recibe 403 (`CandidateProfileTest`).

## 15. Roles y autorización

- **Roles oficiales:** Área solicitante, Recursos Humanos, Aprobador / Dirección, Evaluador y Postulante. No hay administrador ni entrevistador.
- **RF-07:** solo RR. HH. publica.
- **RF-23:**
  - solo el Aprobador de la misma organización;
  - con confirmación humana explícita y justificación;
  - puede elegir a quien no es el primero;
  - decisión única e inmutable;
  - rechaza candidatos de otra vacante u organización y no finalistas (`FinalDecisionTest`, E2E-09).
- **Ranking (RF-20 a RF-22):**
  - determinista;
  - rangos y ponderaciones validados;
  - incompletos listados, no rankeados;
  - empates compartidos, sin romperlos;
  - nunca selecciona (`test_rf23_calculating_the_ranking_never_selects_a_candidate`);
  - no hay transición final automática.
- **RF-27:** solo lectura para el Aprobador de la organización.

## 16. Seguridad

- **Secretos:** ninguno versionado (§24).
- **Descarga de CV:** protegida (§14).
- **Robustez de rutas (F25-M01, MEDIUM, corregido).**
  - Los parámetros de modelo no tenían restricción. Un segmento no numérico (`/requerimientos/create`, `/vacantes/abc`) llegaba a PostgreSQL como `where id = 'abc'` sobre una columna `bigint` y respondía **500** (`SQLSTATE 22P02`).
  - En desarrollo, con *debug*, la página de error mostraba la consulta.
  - No había exposición entre organizaciones: la consulta ya llevaba `organization_id`.
  - Se encontró al revisar las páginas: la ruta localizada es `/requerimientos/crear` y la URL en inglés disparó el error.
  - Detalle en §26–27.

## 17. Auditoría

- *Trigger* `audit_logs_append_only`: impide UPDATE y DELETE en la base, con la única excepción documentada al borrar un usuario.
- Cada registro guarda organización, actor, acción, entidad y fecha, y **nunca** datos sensibles.
- Solo el Aprobador de la organización ve el registro, sin los de otra organización.
- Evidencia: `AuditLoggerTest`, `AuditTrailTest` y `AuditLogViewTest` (16 pruebas), todas en verde.

## 18. Visual

Revisión de 20 páginas críticas:

- públicas: portada, *login*, empleos y detalle;
- requerimientos: lista, detalle y creación;
- vacantes: lista, publicada con tarjeta RF-29 y cerrada;
- postulaciones y expediente;
- comparación de RR. HH. y del Aprobador (decisión);
- auditoría;
- evaluaciones y sesión;
- mis postulaciones y mi perfil.

Método: un spec **temporal y no versionado** (en `cypress/results/`, ignorado) capturó cada página a 375, 768 y 1440 px y midió el desborde. Las capturas se revisaron a ojo.

**Hallazgo F25-M02 (MEDIUM, WCAG 1.4.10, corregido).** A 375 px, las fichas de la tabla de **auditoría** y de **«Mis evaluaciones»** se recortaban a la derecha:

- textos como «Resultado final notificado a postu» o «Cerrada con sele» quedaban cortados;
- el borde derecho de la ficha no se veía.

Causa: en móvil, `tbody`, `tr` y `td` pasan a `block`, pero el `<table>` seguía como tabla. El contenido que no parte línea (etiquetas largas, horario de la sesión) lo ensanchaba, y el contenedor con `overflow-x-auto` recortaba la ficha. **La página no desbordaba**, por eso ni E2E-16 ni la Fase 21 lo detectaron: medían el documento. Tras la corrección, las fichas caben enteras y los textos largos parten línea.

Artefactos de la captura, que no son defectos: la cabecera fija aparece repetida en las capturas de página completa, y las de escritorio salen a 1280 px porque la ventana *headless* limita el ancho de la captura, aunque la medición se hizo a 1440.

## 19. Responsive

60 mediciones (20 páginas × 375/768/1440): **0 px de desborde horizontal**, todas con `main` y `h1`. E2E-16 ahora exige además que **cada ficha quepa en el viewport móvil** e incluye la tabla de evaluaciones asignadas. En `md` y más anchos, las clases son las mismas que antes.

## 20. Accesibilidad

- **Automatizada:** E2E-16 (semántica de tabla en móvil), E2E-17 (movimiento reducido, teclado y foco; 8 pruebas), E2E-19 (regresiones de la Fase 21; 7 pruebas) y `visual-qa.test.tsx`, todas en verde. Las 20 páginas revisadas tienen `main` y `h1`.
- **Movimiento reducido y 3D:** E2E-18 (8 pruebas) y `experience-3d.test.tsx` (13). Muestran el póster con movimiento reducido, en móvil y en equipo modesto emulado; la escena no depende de WebGL, sin WebGL, Three.js, R3F ni Spline. No hay impacto en los flujos.
- **Lector de pantalla real (pendiente de F21): no ejecutado.** NVDA no está instalado. El Narrador de Windows existe, pero su salida de voz no puede observarse ni verificarse desde esta sesión automatizada. Se transfiere a F26 como prueba manual (INFO); no bloquea.

## 21. Rendimiento

**Evidencia exploratoria**, no un *benchmark*: equipo potente, Docker local, Electron *headless* y sin limitar CPU ni red.

Mediana de 3 visitas con la Navigation Timing API:

| Página | TTFB | DOMContentLoaded | load | Primera visita |
|---|---|---|---|---|
| Portada | 7 ms | 158 ms | 166 ms | 324 KB |
| Empleos | 4 ms | 159 ms | 159 ms | 328 KB |
| Requerimientos | 3 ms | 166 ms | 184 ms | 330 KB |
| Vacante con tarjeta RF-29 | 3 ms | 179 ms | 179 ms | 335 KB |
| Comparación | 8 ms | 208 ms | 224 ms | 340 KB |
| Auditoría | 4 ms | 157 ms | 157 ms | 332 KB |

Otros tiempos: build de 27–30 s, PHPUnit de 51–56 s, pytest de 59–66 s y Cypress de 5,2–5,4 min. No hubo congelamientos.

**El pendiente «rendimiento en equipo modesto» de F21 no puede cerrarse aquí**, porque este equipo no es modesto. Se mantiene para F26, con un equipo real o con limitación documentada.

## 22. Documentación

Estados técnicos obsoletos que afectaban el *release*:

- `ml-service/README.md`: decía que Laravel no consumía el servicio, que GAP-01 seguía abierto y usaba el puerto 8001 (F25-L01).
- `docs/testing/cypress-e2e.md`: seguía en 14 specs (F25-L02).

Ambos se corrigieron conservando la historia. Estado sincronizado en `CLAUDE.md`, `PROGRESS.md`, `scope-preliminary.md` y el mapa documental: F23 cerrada, F24 cerrada con observaciones, F25 en su rama y F26 sin iniciar.

Se revisaron `rf-implementation-matrix.md`, `tdd-evidence.md`, `manual-smoke-test.md`, `final-report/` y `v1.1/`. Las demás menciones de «GAP-01 abierto» o «Laravel no consume» son registros históricos de fase (15C, 16 y 24) o entradas del mapa que ya explican el cambio. **No se reescribió ningún documento de v1.0.**

## 23. Artefactos F22, F23 y F24

- **F22:** 19 `.puml` en `docs/v1.1/uml/puml/`.
- **F23:** `.oom` y `.pdm` presentes, más 22 PNG y 22 SVG. No se abrió ni modificó PowerDesigner.
- **F24:**
  - presentes: los tres originales, el DOCX y el PDF finales, el `README`, el `source-map` y `phase-24-academic-documentation.md`;
  - `tools/validate_f9.py`, con el texto del PDF obtenido por `pdftotext` y adaptado al formato `=====PAGE N`: **93 comprobaciones OK, «SIN FALLOS», 28 páginas**;
  - no se regeneró el DOCX ni el PDF.

**Observaciones heredadas, reevaluadas para el *release*:**

| Origen | Observación | Reevaluación |
|---|---|---|
| F23 | Metadatos con rutas absolutas locales dentro de los modelos nativos | LOW; no impide abrirlos (la F23 verificó que abren desde Git). Aceptada; no se tocan modelos nativos |
| F23 | Pestaña `critical` de SEQ-02 y rótulos `[sí]`/`[no]` de AC-01 | LOW cosmético; aceptada |
| F23 | 21 diferencias justificadas | INFO; sin cambios |
| F23 / F22 | Texto OpenAPI de GAP-01 | **Corregida** en esta fase (F25-L01) |
| F24 L-01 | 10 RNF académicos frente a 11 técnicos | LOW; ya declarada en `phase-24` como decisión del equipo. Transferida |
| F24 L-02 | Seis rótulos de RF abreviados en el Formato 09 | LOW; el validador confirma RF-01 a RF-27 presentes y sin renumerar. Transferida |
| F24 L-03 | Conteo XML/RELS | LOW; sin efecto en el documento. Transferida |
| F24 I-01 | Sin validación contra XSD | INFO |
| F24 I-02 | Anexos densos | INFO |

## 24. Secretos

Resultado: **ningún secreto real versionado.** Búsqueda con `git grep` sobre los archivos rastreados:

- **Patrones buscados:** claves privadas, tokens de GitHub, AWS, Slack y OpenAI, `APP_KEY` con valor y asignaciones `PASSWORD`, `SECRET`, `TOKEN` y `API_KEY`.
- **Tipos de archivo rastreados:** `.pem`, `.key`, `.sqlite`, volcados, `.bak`, `.log` y `.env`.
- **Hallazgos:**
  - `security.py` solo define nombres de variable y de cabecera.
  - `DB_PASSWORD=secret` es el valor local de ejemplo de `.env.example`, con Postgres publicado solo en `127.0.0.1` (INFO).
  - `.env` y `.env.e2e` existen localmente y están ignorados.
  - `.env` no configura el ML, así que la integración está desactivada por defecto.
- **Token efímero de la prueba en vivo:** se guardó solo en la carpeta temporal del trabajo, fuera del repositorio, y se borró al terminar.

## 25. Git hygiene

Ninguna suite ni build modificó archivos rastreados, y `git diff --check` quedó limpio tras cada commit.

- **Rastreado:** no hay basura. Se buscaron `*.tmp`, `*.bak`, `*.log`, `__pycache__`, `.pytest_cache`, `.DS_Store`, `Thumbs.db`, `zz_*` y dumps.
- **Ignorado y local:**
  - `vendor/`, `node_modules/`, `ml-service/.venv`, `.pytest_cache` y `.coverage`;
  - `storage/logs`, `public/build` y `bootstrap/cache`;
  - `cypress/results`, con registros de fases anteriores que se conservan como evidencia local del equipo;
  - `.phpunit.result.cache` y `.claude/settings.local.json`.
- **Temporales de esta fase:** los specs de QA visual y de rendimiento, sus JSON y las capturas se **borraron** al terminar.

## 26. Defectos encontrados

| ID | Severidad | Área | Evidencia y reproducción | Impacto | Causa |
|---|---|---|---|---|---|
| **F25-M01** | MEDIUM | Rutas / robustez | `GET /requerimientos/create` (o `/vacantes/abc`, `/postulaciones/x`…) como RR. HH. → 500; log: `SQLSTATE[22P02] invalid input syntax for type bigint: "create"` | Error 500 en lugar de 404, ruido en logs y SQL en la página de *debug* de desarrollo. Sin fuga entre organizaciones | Parámetros de modelo sin restricción numérica |
| **F25-M02** | MEDIUM | UI móvil / WCAG 1.4.10 | A 375 px, auditoría y «Mis evaluaciones»: la ficha llega a 419 px de ancho en un viewport de 376 y el texto se corta | Información recortada en móvil en dos pantallas | El `<table>` seguía como tabla en móvil; el contenido que no parte línea lo ensanchaba y el contenedor lo recortaba |
| **F25-L01** | LOW | Documentación del contrato ML | Descripción OpenAPI de `days_remaining_to_target`, *docstring* de `serving`, línea de la CLI, comentario de `schema.py` y README: «GAP-01 abierto», puerto 8001 | Documentación que contradice la integración vigente (deuda heredada de F22/F23) | Textos de la Fase 15C no actualizados en la 16 |
| **F25-L02** | LOW | Documentación de pruebas | `docs/testing/cypress-e2e.md` en «14 specs y 43 tests» | Guía de la suite desactualizada | Las Fases 17 a 21 añadieron specs sin actualizarla |
| **F25-L03** | LOW | Estilo | `pint --test`: 8 archivos; `vp check`: 154 archivos con formato pendiente | Solo formato; el CI no lo verifica | Preexistente (ya en `4469128`) |

**Sin BLOCKER ni HIGH.**

## 27. Fixes

| Hallazgo | Archivos | Prueba (RED → GREEN) | Commit |
|---|---|---|---|
| F25-M01 | `app/Providers/AppServiceProvider.php` (`Route::patterns` numéricos para `application`, `document`, `evaluation`, `interview`, `jobRequest`, `vacancy`) | `tests/Feature/Routing/NumericRouteParametersTest.php`: 500 → 2 passed (14 aserciones); las rutas localizadas `crear` siguen funcionando y se mantienen las 93 rutas | `791d171` |
| F25-M02 | `resources/js/components/data-table.tsx` (`block md:table`), `status-badge.tsx` (parte línea solo en móvil), `pages/assessments/index.tsx` (`md:whitespace-nowrap`), `cypress/e2e/e2e-16-…` (fichas dentro del viewport y tabla de evaluaciones) | E2E-16: 2 fallos (419 px > 376) → 7/7 | `c18a983` |
| Hueco de cobertura | `tests/Feature/Assessments/EvaluationTest.php` | Caracterización cross-tenant: 1 passed (6 aserciones) | `9867ac1` |
| F25-L01 | `ml-service/src/recruitment_ml/api/schemas.py`, `schema.py`, `serving/__init__.py`, `serving/build_artifact.py`, `ml-service/README.md`, pruebas en `test_api_service.py` y `test_serving_cli.py` | 2 fallos → GREEN; pytest completo 533 | `962b132` |
| F25-L02 | `docs/testing/cypress-e2e.md` (§9 nueva) | Documental | commit de documentación |

Ningún fix cambió la arquitectura, un contrato, un RF ni el modelo ML. **Pint y Prettier:** los archivos tocados ya tenían avisos de formato en `HEAD`. No se reformatearon, para no mezclar formato ajeno con las correcciones (F25-L03). Los archivos nuevos pasan Pint.

## 28. Deudas aceptadas

| Deuda | Severidad | Destino |
|---|---|---|
| F25-L03: formato de Pint y `vp check` preexistente | LOW | F26 u otra fase de mantenimiento: aplicar `pint` y `vp check --fix` en un commit propio, sin cambios funcionales |
| Lector de pantalla real (NVDA o Narrador) en flujos críticos | INFO | F26, prueba manual |
| Rendimiento en un equipo modesto real | INFO | F26, prueba manual o con limitación documentada |
| F23: metadatos absolutos locales, `critical` de SEQ-02 y rótulos de AC-01 | LOW | Aceptadas; no se tocan modelos nativos |
| F24: L-01, L-02, L-03, I-01 e I-02 | LOW / INFO | Decisión del equipo (catálogos de RNF y CU) o aceptadas |
| `evaluation_criteria.position` fuera de CL-01 (F23 O-01) | INFO | Revisión futura de la especificación |
| Modelos de prueba `zz_*` de F23 en la carpeta temporal del equipo | INFO | Limpieza cuando el equipo la autorice |
| El motivo `server_error` agrupa 401, 500 y otros | INFO | Diseño documentado; solo si el equipo quiere motivos más finos |

## 29. Criterios de salida

| Criterio | Estado |
|---|---|
| Git limpio; `main`, el tag y `develop` intactos | ✅ |
| PHPUnit sin fallos bloqueantes | ✅ 411/0 (8 omitidas justificadas) |
| pytest sin fallos bloqueantes | ✅ 533/0 |
| Componentes | ✅ 42/42 |
| TypeScript | ✅ 0 errores |
| Build | ✅ |
| Cypress | ✅ 85/85 |
| Sin fuga cross-tenant | ✅ |
| RF-23 humano | ✅ |
| RF-29 respeta su frontera | ✅ |
| Contrato ML coincide | ✅ |
| Seguridad razonable | ✅ (F25-M01 corregido) |
| Visual sin regresión crítica | ✅ (F25-M02 corregido) |
| Documentación consistente | ✅ |
| Artefactos de F22, F23 y F24 presentes | ✅ |
| Sin secretos | ✅ |
| Deudas clasificadas | ✅ (§28) |
| F26 puede empezar sin trabajo técnico mayor | ✅ |

## 30. Release readiness

**Sí, con observaciones.** v1.1 está técnicamente consistente, es reproducible con los comandos documentados, es trazable y es estable: todas las suites están en verde y no hay BLOCKER ni HIGH. Los dos MEDIUM encontrados están corregidos y cubiertos por pruebas. Las deudas que quedan son LOW o INFO: formato, pruebas manuales de lector de pantalla y de equipo modesto, y observaciones heredadas de F23 y F24. Ninguna exige trabajo técnico mayor antes de F26.

## 31. Handoff a la Fase 26

La Fase 26 **no se inició**.

1. **Auditoría de Codex de F25:**
   - revisar los cuatro commits de corrección y sus pruebas;
   - reproducir la regresión: `php artisan test`, `pytest`, `tsc`, `vp test --run`, `npm run build` y `npm run cy:run`;
   - verificar que el diff no sale del alcance.
2. **Para F26** (GitHub, *release* y cierre), cuando el equipo la autorice:
   - integrar F25 en `develop` y decidir la integración de v1.1 en `main` y su etiqueta, sin mover `v1.0.0-academic`;
   - hacer las pruebas manuales pendientes (lector de pantalla y equipo modesto);
   - decidir si se aplica el formato (F25-L03) en un commit aparte;
   - resolver las decisiones del equipo sobre RF-28, RF-29 y RNF-C (preguntas 12 y 13) y sobre los catálogos de RNF y CU de F24.
3. **Sin cambios de contrato:** RF-01 a RF-27; RF-23 humano; RF-28 candidato; RF-29 experimental; RNF-C propuesta; multiempresa, Policies y auditoría de solo inserción.
