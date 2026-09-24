# Handoff a PowerDesigner (Fase 23)

Guía de trabajo para formalizar en PowerDesigner los diagramas especificados en la Fase 22. **F22 no creó ningún archivo de PowerDesigner** (`.oom`, `.pdm`, `.cdm`, `.bpm`, `.xsm`). Cada diagrama tiene su especificación completa (elementos, relaciones, multiplicidades, notas y fuente) en esta carpeta; aquí va lo necesario para construirlo sin volver a leer el código.

Procedimiento general de la herramienta: [`.claude/skills/powerdesigner-uml/POWERDESIGNER.md`](../../../.claude/skills/powerdesigner-uml/POWERDESIGNER.md).

## 1. Reglas para F23

1. **Solo lo especificado.** Si un elemento no está en estas especificaciones, no se añade; si algo parece faltar, se contrasta con el código y se anota en el informe antes de dibujarlo.
2. **Nombres técnicos idénticos al código** (`SelectionDecision`, `en_evaluacion`, `POST /v1/predict`). Se puede añadir una etiqueta en español para la presentación, conservando el nombre técnico en una nota.
3. **Los modelos de v1.0 no se editan.** v1.1 va en modelos nuevos con nombre versionado (por ejemplo `reclutamiento-v1.1-oom`).
4. **Estereotipos**, con el mismo significado en todos los diagramas:

   | Estereotipo | Uso | Sugerencia gráfica |
   |---|---|---|
   | `<<tenant scoped>>` | Las 13 clases con `organization_id` y `OrganizationScope` | — |
   | `<<human decision>>` | UC-RF23, `SelectionDecision`, actividad 17 de AC-01, SEQ-07 | Borde grueso |
   | `<<experimental>>` | UC-RF29, riesgo operacional, servicio de inferencia, SEQ-08, AC-02 | Color de advertencia |
   | `<<external service>>` | Servicio de riesgo operacional (actor y componente) | — |
   | `<<append only>>` | `AuditLog` | — |
   | `<<propuesto v1.1>>` | UC-RF28 | Gris |

5. **Validar tras construir** cada diagrama contra su especificación y registrar el resultado en el informe de diagramas de v1.1.

## 2. Orden de creación sugerido

El orden va de lo que se puede verificar automáticamente a lo que depende de ello.

| # | Diagrama | Tipo PowerDesigner | Modelo | Especificación | Borrador |
|---|---|---|---|---|---|
| 1 | Modelo físico | PDM por ingeniería inversa | PDM | [`class-model.md` §6](class-model.md#6-nota-para-el-modelo-físico-f23) | — |
| 2 | CL-01 Dominio | *Class Diagram* | OOM | [`class-model.md`](class-model.md) | `puml/cl-01-domain.puml` |
| 3 | ST-01 a ST-04 Estados | *Statechart Diagram* | OOM | [`state-diagrams.md`](state-diagrams.md) | `puml/st-0*.puml` |
| 4 | UC-01 Casos de uso | *Use Case Diagram* | OOM | [`use-cases.md`](use-cases.md) | `puml/uc-01-use-cases.puml` |
| 5 | CO-01 Componentes | *Component Diagram* | OOM | [`component-model.md`](component-model.md) | `puml/co-01-components.puml` |
| 6 | PK-01 Paquetes | *Package Diagram* | OOM | [`component-model.md` §3](component-model.md#3-pk-01--paquetes-del-monolito) | `puml/pk-01-packages.puml` |
| 7 | DE-01 Despliegue | *Deployment Diagram* | OOM | [`deployment-model.md`](deployment-model.md) | `puml/de-01-deployment.puml` |
| 8 | SEQ-01 a SEQ-08 | *Sequence Diagram* | OOM | [`sequence-diagrams.md`](sequence-diagrams.md) | `puml/seq-0*.puml` |
| 9 | AC-01, AC-02 | *Activity Diagram* | OOM | [`activity-diagrams.md`](activity-diagrams.md) | `puml/ac-0*.puml` |

Total: **1 PDM y 19 diagramas UML** (1 de casos de uso, 1 de clases, 4 de estados, 1 de componentes, 1 de paquetes, 1 de despliegue, 8 de secuencia, 2 de actividad).

## 3. Ficha por diagrama

### 1 · PDM (ingeniería inversa)

- **Origen**: `pg_dump --schema-only` del entorno Docker, sin credenciales en el comando documentado ni en archivos versionados.
- **Validar**: 17 tablas de dominio + tablas del *framework*; FK de §3 de `class-model.md`; `CHECK` de estado y coherencia; `UNIQUE (organization_id, code)` en `job_requests` y `vacancies`; `UNIQUE (vacancy_id, candidate_id)`; índice parcial `applications_one_selected_per_vacancy`; `vacancies_target_after_close`; *trigger* `audit_logs_append_only`.
- **RF**: RF-01 a RF-27; `target_completion_at` para RF-29.

### 2 · CL-01 Dominio

- **Elementos**: 17 clases (§2 de `class-model.md`) en `App\Models`; 10 enums en `App\Enums` (+ `AuditAction` como nota o diccionario).
- **Relaciones**: 35 asociaciones con multiplicidad y rol (§3); 8 composiciones.
- **Multiplicidades clave**: `JobRequest 1 — 0..1 Vacancy`; `Vacancy 1 — 1 JobProfile`; `Vacancy 1 — 0..1 SelectionDecision`; `User 1 — 0..* Application` con `UNIQUE (vacancy_id, candidate_id)`; `User 1 — 0..1 CandidateProfile`; `Organization 0..1 — 0..* User`.
- **Notas**: multiempresa lógica (sin RLS ni base por tenant); postulante global; índice parcial de selección; criterios por etapa; `desierta` sin flujo; *trigger* de solo inserción con su única excepción.

### 3 · ST-01 a ST-04 Estados

- **Elementos**: estados con su valor real; transiciones `disparador [guarda] / efecto` de `state-diagrams.md`.
- **Notas**: destinos manuales y bloqueo tras RF-23 (A-28) en ST-03; `desierta` en ST-02.
- **RF**: RF-01–RF-03, RF-05–RF-07, RF-10, RF-13–RF-19, RF-24, RF-25.

### 4 · UC-01 Casos de uso

- **Actores**: Área solicitante, Recursos Humanos, Aprobador / Dirección, Evaluador, Postulante, Servicio de riesgo operacional (`<<external service>>` `<<experimental>>`). **Ni administrador ni entrevistador.**
- **Casos**: 29, `UC-RF01` … `UC-RF29`, nombres oficiales; UC-RF28 `<<propuesto v1.1>>` sin asociaciones.
- **Relaciones**: 1 `<<extend>>` (RF-04 → RF-03) y 12 `<<include>>` (§3 de `use-cases.md`). Ninguna otra.
- **Notas**: RF-23 humano; RF-21/22 soporte; RF-29 experimental y sin relación con ranking ni decisión; auditoría transversal; precondición de RF-24.

### 5 · CO-01 Componentes

- **Elementos**: navegador (páginas Inertia, componentes compartidos, tarjeta de riesgo), monolito Laravel (capa HTTP, autorización y multiempresa, cuenta y acceso, servicios de dominio, cálculo de ranking, modelos, auditoría, notificaciones, almacenamiento de CV, riesgo operacional), infraestructura (PostgreSQL, Redis, trabajador de cola), servicio de inferencia (API FastAPI, *serving*, artefacto).
- **Interfaces**: Inertia/HTTP; JSON `GET vacantes/{id}/riesgo-operacional`; **`POST /v1/predict` + `X-Internal-Token`**.
- **Contrato en la interfaz de inferencia** (nota): petición = 15 features enteras, sin IDs ni PII; respuesta = `risk_score`, `risk_flag`, `threshold`, `model_version`, `freeze_fingerprint`, `status`. **Sin incertidumbre, `candidate_id`, `vacancy_id`, `organization_id` ni texto libre.**
- **No dibujar**: un componente por controlador; un «motor 3D»; dependencia alguna entre riesgo operacional y ranking/decisión.

### 6 · PK-01 Paquetes

- **Elementos**: 10 paquetes (8 de negocio, modelos, compartido).
- **Dependencias**: las de §3 de `component-model.md`; riesgo operacional → solo modelos.

### 7 · DE-01 Despliegue

- **Nodos**: equipo del usuario (navegador); equipo anfitrión con Docker Engine (`app`, `queue`, `postgres`, `redis`) y el proceso Python `uvicorn :8008` `<<experimental>>`.
- **Artefactos y almacenes**: aplicación Laravel, `public/build`, `storage/app/private`, bases PostgreSQL, Redis, artefacto `.joblib`.
- **Enlaces**: HTTP 8000; TCP 5432 y 6379 internos; HTTP `host.docker.internal:8008` condicionado a `ML_SERVICE_ENABLED=true`.
- **Notas**: frontend servido por Laravel; perfil `e2e` solo pruebas; mailer `log`; sin producción, nube, S3, CDN ni Kubernetes.

### 8 · SEQ-01 a SEQ-08

- **Lifelines**: las de cada tabla de `sequence-diagrams.md`.
- **Fragmentos**: `critical` (transacción), `alt` (reglas de negocio, desenlaces del ML), `opt` (notificación de rechazo).
- **Notas obligatorias**: SEQ-06 (el ranking no se guarda ni selecciona), SEQ-07 (decisión humana, puede no ser el primero, no toca el ML), SEQ-08 (proceso, no personas; nada persistente; sin incertidumbre; sin mensajes al ranking ni a la decisión).

### 9 · AC-01 y AC-02

- **AC-01**: seis particiones; decisiones de requerimiento, aprobación, configuración, preselección, más sesiones y decisión humana; nota de auditoría, A-28 y A-30.
- **AC-02**: elegibilidad → `descriptive_only`; habilitación → `descriptive_only`; respuesta → `unavailable` o `predictive_available`; fin sin efectos.

## 4. Lo que F23 no debe modelar

Administrador del SaaS · entrevistador como rol · facturación · *Talent Pool* · Meilisearch · IA en la nube · Kubernetes · proveedores cloud · PostgreSQL RLS · base por tenant · S3 · proveedor de correo · WebGL/Three.js · ML en producción · microservicios generales · RF-28 como implementado · cierre `desierta` como flujo · **GAP-01 como pendiente** (está resuelto técnicamente desde la Fase 16; la descripción OpenAPI que dice lo contrario es texto obsoleto) · RNF-C como requisito aprobado (sigue siendo propuesta; la escena CSS 3D es una implementación puntual autorizada, de presentación).

## 5. Registro esperado de F23

Por cada diagrama: modelo y versión de PowerDesigner, especificación de origen, pasos, conteo validado (clases, asociaciones, estados, mensajes…), diferencias con la especificación y su causa, y capturas exportadas. Destino sugerido: un informe de diagramas de v1.1 junto a `docs/final-report/diagram-reports/`, sin modificar los de v1.0.
