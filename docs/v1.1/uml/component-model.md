# CO-01 · Diagrama de componentes y PK-01 · Paquetes del monolito

| | |
|---|---|
| **Objetivo** | Mostrar los subsistemas reales, sus interfaces y sus dependencias, incluida la frontera Laravel ↔ FastAPI |
| **Alcance** | Arquitectura **lógica** AS-IS. Sin nodos físicos (van en [`deployment-model.md`](deployment-model.md)). Sin un componente por controlador |
| **Fuente de verdad** | `app/` (carpetas por módulo), `routes/web.php`, `bootstrap/app.php`, `resources/js/`, `config/ml.php`, `ml-service/src/recruitment_ml/`, `.env.example` |
| **Borradores** | [`puml/co-01-components.puml`](puml/co-01-components.puml) · [`puml/pk-01-packages.puml`](puml/pk-01-packages.puml) |
| **RF** | RF-01 a RF-27 por módulo; RF-29 en el componente de riesgo operacional |

## 1. Componentes

### Frontend (se ejecuta en el navegador; lo sirve Laravel)

| Componente | Contenido real | Depende de |
|---|---|---|
| Páginas Inertia | `resources/js/pages/<módulo>/*.tsx` (31 páginas: requerimientos, vacantes, postulaciones, evaluaciones, selección, auditoría, postulante, empleos, notificaciones, configuración, acceso) | Interfaz Inertia del backend |
| Componentes compartidos | `DataTable`, `Section`, `StatusBadge`, `StatusTimeline`, `WorkflowAlert`, formularios, `ui/*` (shadcn/Radix), *layouts* | — |
| Tarjeta de riesgo operacional `<<experimental>>` | `components/vacancies/operational-risk-card.tsx` | Endpoint JSON `vacancies.operational-risk` |

La experiencia 3D de la Fase 20 es un detalle de presentación de la portada pública (CSS 3D, sin WebGL ni dependencias). **No es un componente arquitectónico**: como mucho, una nota en «Páginas Inertia».

### Backend Laravel (monolito modular)

| Componente | Contenido real | Interfaces que ofrece | Depende de |
|---|---|---|---|
| Capa HTTP | Rutas con nombre, *middleware* `auth` y `role` (`EnsureUserHasRole`), `HandleInertiaRequests`, Form Requests, controladores delgados, *presenters* (`RankingPresenter`, `AssessmentSessionPresenter`) y *resources* (`AuditLogResource`, `VacancyResource`…) | **Inertia/HTTP** (páginas y redirecciones), **JSON** de riesgo operacional | Autorización, servicios de dominio |
| Autorización y multiempresa | 7 Policies (rol **y** organización), `OrganizationScope`, `BelongsToOrganization` | `Gate` | Modelos |
| Cuenta y acceso | Fortify (`CreateNewUser`, 2FA, restablecimiento), *passkeys*, `Settings/*` | Rutas de acceso | Modelos, auditoría |
| Servicios de dominio | Un paquete por módulo (§3): `JobRequestWorkflow`, `VacancyService`, `ApplicationService`, `ApplicationStageService`, `AssessmentScheduler`, `AssessmentResultRecorder`, `CandidateProfileService`, `FinalDecisionService`, `SelectionRegistrationService`, `VacancyClosureService` | Métodos de servicio | Modelos, auditoría, notificaciones, cálculo de ranking |
| Cálculo de ranking | `WeightingValidator`, `ScoreSheetValidator`, `RankingService` (puro, determinista), `VacancyRankingBuilder` | `rank()`, `forVacancy()` | Modelos (solo lectura) |
| Modelos de dominio | 17 modelos Eloquent + enums con transiciones | ORM | PostgreSQL |
| Auditoría | `AuditLogger` (registro); la consulta pasa por `AuditLogController` + `AuditLogResource` en la capa HTTP | `record()` | Modelo `AuditLog` → PostgreSQL (*trigger* de solo inserción) |
| Notificaciones | 6 notificaciones sobre `RecruitmentNotification` (`ShouldQueue`, `afterCommit`), canales `database` y `mail` | `notify()` | Cola Redis, PostgreSQL (`notifications`), *mailer* `log` |
| Almacenamiento de CV | Disco `local` = `storage/app/private`; descarga por `CandidateDocumentDownloadController` + `CandidateDocumentPolicy` | Lectura y escritura de archivos | Sistema de archivos |
| Riesgo operacional `<<experimental>>` | `OperationalRiskService` (elegibilidad y *checkpoint*), `OperationalRiskFeatureBuilder` (15 features), `MlRiskClient` (HTTP, validación, *fallback*), `RiskAssessment`, `RiskAvailability` | `assess()` | Modelos (solo lectura), **servicio de inferencia** |

### Infraestructura

| Componente | Uso real |
|---|---|
| PostgreSQL 17 | Único almacén de datos de negocio (sistema de registro) |
| Redis 7 | Sesiones, caché y cola |
| Trabajador de cola | `queue:work redis`: envía las notificaciones encoladas |

### Servicio de inferencia `<<external service>>` `<<experimental>>`

| Componente | Contenido real |
|---|---|
| API FastAPI | `recruitment_ml.api.app`: `GET /health`, `GET /v1/model-info`, `POST /v1/predict`; `security.py` exige `X-Internal-Token` en `/v1/*` |
| Esquemas | `schemas.py`: `PredictionRequest` (15 features, `extra="forbid"`, `strict=True`), `PredictionResponse` (6 campos) |
| *Serving* | `serving/loader.py` (verifica SHA-256, *freeze* y versiones), `serving/predictor.py` |
| Artefacto del modelo | `ml-service/artifacts/` (`.joblib` + metadatos, no versionado): Logistic Regression `C=10`, `StandardScaler`, sin calibración, *threshold* `0.1679418172266036` |

Los módulos de entrenamiento y generación sintética (`training/`, `synthetic/`) existen en el repositorio pero **no participan en la ejecución**: producen el artefacto fuera de línea. Se mencionan en una nota, no como componentes en tiempo de ejecución.

## 2. Dependencias clave

| De | A | Interfaz | Nota |
|---|---|---|---|
| Navegador | Capa HTTP | HTTP + protocolo Inertia | Cada página llega como respuesta Inertia; la tarjeta de riesgo pide JSON aparte |
| Capa HTTP | Autorización | `Gate::authorize` / `FormRequest::authorize` | Antes de cualquier servicio |
| Servicios de dominio | Auditoría | `AuditLogger::record` | En la misma transacción |
| Servicios de dominio | Notificaciones | `notify()` | Se encolan y se despachan **después del commit** |
| `FinalDecisionService` | Cálculo de ranking | `VacancyRankingBuilder::forVacancy` | Solo para la instantánea; **no** elige al candidato |
| Riesgo operacional | Servicio de inferencia | **`POST /v1/predict`**, HTTP interno, `X-Internal-Token` | Timeouts de 1 s (conexión) y 3 s (total), 1 reintento. Sin respuesta válida → `unavailable`; desactivado → `descriptive_only` |
| Riesgo operacional | Cálculo de ranking, `FinalDecisionService` | **Ninguna** | Frontera de RF-29: el riesgo no alimenta el ranking ni la decisión |

## 3. PK-01 · Paquetes del monolito

Aporta una vista que el diagrama de componentes no da: cómo se reparte cada módulo de negocio entre las capas. Los paquetes son **carpetas reales**, no módulos de Composer.

| Paquete (módulo) | `Http/Controllers` | `Http/Requests` | `Services` | RF |
|---|---|---|---|---|
| Requerimientos | `JobRequests` | `JobRequests` | `JobRequests` | RF-01–RF-04 |
| Vacantes | `Vacancies`, `PublicVacancyController` | `Vacancies` | `Vacancies` | RF-05–RF-07 |
| Postulantes | `Candidates`, `Documents` | `Candidates` | `Candidates`, `Applications/ApplicationService` | RF-08–RF-11 |
| Postulaciones | `Applications` | `Applications` | `Applications/ApplicationStageService` | RF-12–RF-15 |
| Evaluaciones | `Assessments` | `Assessments` | `Assessments`, `Evaluation` | RF-16–RF-20 |
| Ranking y selección | `Selection` | `Selection` | `Ranking`, `Selection` | RF-20–RF-26 |
| Auditoría | `Audit` | — | `Audit` | RF-27 |
| Riesgo operacional `<<experimental>>` | `Vacancies/VacancyOperationalRiskController` | — | `Ml` | RF-29 |
| Compartido | `NotificationController`, `Settings` | `Settings` | `Support` | — |

Dependencias entre paquetes que el diagrama debe mostrar: todos → Modelos y Auditoría; Ranking y selección → Postulaciones (`ApplicationStageService::transition` para seleccionar y cerrar); Evaluaciones → Postulaciones (avance automático de etapa al programar); Riesgo operacional → Modelos, **y a ningún otro paquete de negocio**.

## 4. Discrepancias y precisiones

- La tarjeta de riesgo depende del endpoint JSON, no de la página: la página de la vacante se carga igual aunque el servicio de inferencia no exista.
- El servicio de inferencia **no está en Docker Compose**; lógicamente es un componente externo. Su nodo físico se trata en el despliegue.
- La descripción OpenAPI del campo `days_remaining_to_target` en `schemas.py` todavía dice que Laravel no puede producirlo (GAP-01). **Es texto obsoleto**: GAP-01 está resuelto técnicamente desde la Fase 16. No se modela como pendiente (ver [`../phase-22-uml-update.md`](../phase-22-uml-update.md) §11).

## 5. Instrucciones para F23

1. OOM, *Component Diagram* «CO-01 Componentes AS-IS v1.1», con tres grupos: navegador, monolito Laravel, servicio de inferencia; infraestructura aparte.
2. Interfaces provistas y requeridas como en §2; etiquetar la de inferencia con `POST /v1/predict · X-Internal-Token`.
3. Estereotipos `<<experimental>>` y `<<external service>>` solo en riesgo operacional, tarjeta de riesgo y servicio de inferencia.
4. Nota sobre la ausencia de dependencia entre riesgo operacional y ranking/decisión.
5. PK-01 como *Package Diagram* aparte, con los paquetes de §3 y sus dependencias.
