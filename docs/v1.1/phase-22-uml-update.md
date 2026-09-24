# Fase 22 — Actualización UML del sistema AS-IS

**Fecha:** 23 de septiembre de 2026
**Rama:** `feature/phase-22-uml-update` · **Base:** `aced6da` (cierre de la Fase 21)
**Writer principal:** Claude Code · **Reviewer:** Codex (auditoría posterior)

> Fase **exclusivamente documental**. No cambia código, pruebas, dependencias, rutas, modelos, Policies, migraciones ni el servicio ML. **No crea archivos de PowerDesigner**: eso es la Fase 23. RF-23 sigue siendo una decisión humana y RF-29 sigue siendo experimental.

---

## 1. Objetivo

Especificar los diagramas UML que representan **fielmente lo implementado**, de modo que la Fase 23 pueda formalizarlos en PowerDesigner sin volver a descubrir la arquitectura. Nada de arquitectura futura: lo que no está en el código no se modela como existente.

## 2. Baseline

| | |
|---|---|
| `develop` = `origin/develop` | `aced6dac76fc0263ef9fdeb30bcd79bb9fbdc92e`, árbol limpio, `git diff --check` limpio |
| `main` | `4563c69` (v1.0 académica) |
| `v1.0.0-academic` | `9a946c2`, intacto |
| Diagramas previos | Informes de v1.0 en `docs/final-report/diagram-reports/` (01 a 09). Los gráficos originales **no están en el repositorio** |

## 3. Skills aplicados

`project-guardian` (rama, alcance, contratos), `powerdesigner-uml` y su `POWERDESIGNER.md` (extraer antes de dibujar, nombres idénticos al código, matriz de correspondencia, no generar `.oom`/`.pdm`), `academic-traceability` (cadena RF → código → prueba → UML, evidencia admisible, preservar v1.0) y `laravel-saas-quality` (cadena Ruta → Form Request → Controller → Policy → Service → Modelo que siguen las secuencias).

## 4. Fuentes revisadas

**Código** (fuente de verdad): `routes/web.php`, `routes/settings.php`, `bootstrap/app.php`; `app/Enums/*` (15 enums); `app/Models/*` (17 modelos, *trait* y *scope* multiempresa); `app/Policies/*` (7); `app/Http/Controllers/*`, `Requests/*`, `Presenters/*`, `Resources/*`; `app/Services/*` (todos los módulos, incluido `Ml`); `app/Notifications/*`; `app/Actions/Fortify/*`; `database/migrations/*` (18); `resources/js/pages/*` (31), `components/*`, `layouts/*`; `ml-service/src/recruitment_ml/api/*` y `serving/*`; `docker-compose.yml`, `docker/php/*`, `docker/postgres/init/*`; `config/ml.php`, `config/filesystems.php`, `.env.example`; listados de `tests/`, `ml-service/tests/` y `cypress/e2e/`.

**Documentación** (contexto, contrastada con el código): `AGENTS.md`, `CLAUDE.md`, `docs/PROGRESS.md`, `documentation-update-map.md`, `scope-preliminary.md`, `phase-21-visual-qa.md`, `architecture-decisions/*`, `ml/*`, `phase-16-laravel-ml-integration.md`, `phase-17-ml-validation.md`, `docs/rf-implementation-matrix.md`, los informes `03-use-case-report.md`, `04-architecture-report.md`, `05-class-model-report.md` y `09-deployment-report.md` de `docs/final-report/diagram-reports/`.

## 5. Inventario UML

Detalle en [`uml/uml-inventory.md`](uml/uml-inventory.md). Resumen:

- **Actores**: cinco roles reales (Área solicitante, RR. HH., Aprobador/Dirección, Evaluador, Postulante) y el servicio de riesgo operacional como actor secundario técnico. **No hay administrador ni rol de entrevistador**: la entrevista la registra el Evaluador asignado.
- **Módulos**: 11 agrupaciones en un monolito por carpetas (8 de negocio, incluido el riesgo operacional experimental; notificaciones; cuenta y acceso; transversal).
- **Entidades**: 17 modelos; 13 `<<tenant scoped>>`; `User` (postulante), `CandidateProfile`, `CandidateDocument` y `Organization` sin *scope*.
- **Estados**: 4 máquinas (requerimiento, vacante, postulación, sesión).
- **ML**: integración experimental Laravel → HTTP interno con token → FastAPI → modelo congelado; 15 features de entrada y 6 campos de salida exactos.

## 6. Diagramas seleccionados

| Id | Diagrama | Por qué se incluye | Especificación |
|---|---|---|---|
| UC-01 | Casos de uso | Alcance funcional RF-01 a RF-29 por actor | [`uml/use-cases.md`](uml/use-cases.md) |
| CL-01 | Clases del dominio | Entidades, multiplicidades y multiempresa | [`uml/class-model.md`](uml/class-model.md) |
| CO-01 | Componentes | Subsistemas y frontera Laravel ↔ FastAPI | [`uml/component-model.md`](uml/component-model.md) |
| PK-01 | Paquetes | **Incluido**: muestra cómo cada módulo se reparte entre capas, que CO-01 no muestra, y aísla el paquete experimental | [`uml/component-model.md` §3](uml/component-model.md) |
| DE-01 | Despliegue | Contenedores reales y el servicio de inferencia fuera de Compose | [`uml/deployment-model.md`](uml/deployment-model.md) |
| SEQ-01…08 | Secuencia | Los ocho flujos críticos pedidos; ninguno redundante | [`uml/sequence-diagrams.md`](uml/sequence-diagrams.md) |
| AC-01 | Actividad | Proceso de extremo a extremo con responsables | [`uml/activity-diagrams.md`](uml/activity-diagrams.md) |
| AC-02 | Actividad | **Incluido**: la elegibilidad del ML tiene siete motivos y tres desenlaces que una secuencia no deja ver de un vistazo | [`uml/activity-diagrams.md`](uml/activity-diagrams.md) |
| ST-01…04 | Estados | **Incluidos**: el código define las máquinas explícitamente (`allowedTransitions()` + `CHECK`) | [`uml/state-diagrams.md`](uml/state-diagrams.md) |

Borradores PlantUML: 19 archivos en [`uml/puml/`](uml/puml/), uno por diagrama.

## 7. AS-IS representado

- **Multiempresa lógica**: `organization_id` + `OrganizationScope` + Policies que comparan rol y organización. Sin RLS ni base por tenant.
- **Decisión humana**: RF-23 solo por el Aprobador de la misma organización, con confirmación y justificación; el ranking (RF-21/22) calcula y ordena en memoria, no se guarda y no selecciona; la decisión guarda una instantánea y no cambia estados.
- **Auditoría transversal** (RF-27): 23 acciones, tabla de solo inserción con *trigger*.
- **Notificaciones**: 6 clases encoladas en Redis, `afterCommit`, canales `database` y `mail` (*log* en desarrollo).
- **CV**: disco local privado de Laravel.
- **Frontend**: React/Inertia compilado por Vite y servido por Laravel; sin servidor propio. La escena CSS 3D de la portada es presentación, no un componente.
- **RF-29 experimental**: consulta JSON aparte, elegibilidad, 15 features en el *checkpoint*, `POST /v1/predict` con `X-Internal-Token`, validación del contrato congelado, `predictive_available` / `descriptive_only` / `unavailable`. Nada persistente. Sin relación con ranking ni decisión.
- **GAP-01 resuelto técnicamente**: `vacancies.target_completion_at` existe (Fase 16).

## 8. Decisiones de modelado

1. **Un caso de uso por RF**, con los nombres oficiales, en lugar de los 13 casos agrupados de v1.0: la trazabilidad de v1.1 lo exige. El informe de v1.0 no se modifica.
2. **`<<include>>`/`<<extend>>` solo donde el código lo hace** (12 y 1), cada uno justificado. RF-27 se representa como nota transversal, no con 20 inclusiones.
3. **RF-28 como candidato no implementado** (ver §11, D-01).
4. **Clase ≠ tabla**: FK como asociaciones, sin timestamps; el PDM sale por ingeniería inversa en F23.
5. **Multiempresa por estereotipo** y una nota, no con 13 asociaciones a `Organization`.
6. **Composición** solo con `cascadeOnDelete` y dependencia existencial.
7. **Servicio de inferencia como componente externo** y proceso del anfitrión en el despliegue, porque así se ejecuta.
8. **Ranking y riesgo no son clases persistentes**: se calculan en cada consulta.
9. **Sin estereotipos de más**: seis, con significado fijo (`powerdesigner-handoff.md` §1).

## 9. Trazabilidad

[`uml/traceability-matrix.md`](uml/traceability-matrix.md): RF-01 a RF-29 → elementos UML → clase → ruta, controlador y servicio → pruebas PHPUnit, pytest y Cypress existentes; matriz de roles y permisos leída de las Policies; discrepancias del cruce con el código.

## 10. Exclusiones: no implementado, fuera del UML AS-IS

Administrador del SaaS o de organización · rol de entrevistador · facturación · *Talent Pool* · Meilisearch · IA en la nube · Kubernetes · proveedores cloud · PostgreSQL RLS · base por tenant · S3 o almacenamiento en la nube · proveedor de correo real · CDN · WebGL/Three.js · ML en producción · microservicios generales · **RF-28** (panel agregado) · cierre de vacante **desierta** · entorno de producción desplegado.

## 11. Deuda y observaciones

| # | Observación | Tratamiento |
|---|---|---|
| D-01 | El encargo describe RF-28 como «descriptivo operacional fallback». Lo definido para RF-28 (`ml/requirements-and-traceability-plan.md`) es un **panel agregado** de tiempos, *backlog* y cuellos de botella, **no implementado**; el estado `descriptive_only` de la tarjeta de RF-29 solo muestra una etiqueta y un mensaje | Modelado como candidato `<<propuesto v1.1>>`. **Decisión del equipo** si se quiere otra interpretación |
| D-02 | RF-17 se llama «convocatoria de evaluación» pero también convoca a entrevistas | Documentado; RF-18 incluye RF-17 |
| D-03 | `VacancyClosureType::Deserted` sin flujo (A-30) | Nota; sin transición |
| D-04 | La descripción OpenAPI de `days_remaining_to_target` en `ml-service/src/recruitment_ml/api/schemas.py` dice que Laravel no puede producirla: texto obsoleto desde la Fase 16 | **Deuda de texto en el runtime ML**, fuera del alcance de F22. En UML, GAP-01 figura **resuelto** |
| D-05 | El diagrama de casos de uso de v1.0 atribuye RF-20 al Evaluador | En v1.1 es un caso del sistema; registrado en el mapa documental |
| D-06 | El despliegue original de v1.0 incluía S3 | No se modela |
| O-01 | Los `.puml` no se renderizaron: no hay PlantUML en el equipo y la fase no instala software | Son borradores; la fuente gráfica será PowerDesigner (F23). Revisarlos al importarlos |
| O-02 | El servicio de inferencia no tiene contenedor en Compose | Se modela como proceso del anfitrión, que es lo real; contenedorizarlo sería trabajo futuro, no AS-IS |

Ningún elemento quedó como «pendiente de confirmación»: toda multiplicidad y relación se verificó con la relación Eloquent y la migración correspondiente.

## 12. Handoff a la Fase 23

[`uml/powerdesigner-handoff.md`](uml/powerdesigner-handoff.md): reglas, estereotipos, orden de creación (PDM → clases → estados → casos de uso → componentes → paquetes → despliegue → secuencias → actividades), una ficha por diagrama y la lista de lo que no se modela. La Fase 23 no se inició.
