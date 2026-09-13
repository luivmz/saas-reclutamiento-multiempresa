# Informe del modelo de clases

## 1. Propósito

Describir las clases del dominio, sus atributos clave y sus relaciones, como base del modelo de datos y de las reglas de negocio.

**Disponibilidad:**
- No existe un diagrama de clases UML original en el repositorio.
- En la carpeta del curso tampoco: el archivo `SaaS Reclutamiento - Diagramas UML.oom` contiene un diagrama de secuencia, no de clases.

Este informe describe las clases reales por escrito; no genera un UML gráfico nuevo.

## 2. Elementos principales

**Modelos Eloquent** (`app/Models`):

| Clase | Rol en el dominio | Relaciones principales | Multiempresa |
|---|---|---|---|
| `Organization` | Empresa u organización cliente del SaaS | Tiene personal, requerimientos, vacantes y auditoría | Raíz |
| `User` | Personal (con rol) o postulante (global) | Pertenece a una organización (excepto el postulante); tiene `CandidateProfile` | `organization_id` nulo solo para postulantes |
| `JobRequest` | Requerimiento de personal (`JobRequestStatus`) | Solicitante, validador y decisor; `JobRequestStatusHistory`; genera una `Vacancy` | Sí |
| `JobRequestStatusHistory` | Historial de estados del requerimiento | `JobRequest`, usuario | Sí |
| `Vacancy` | Convocatoria (`VacancyStatus`, `VacancyClosureType`) | `JobProfile` (1:1), `EvaluationCriterion` (1:N), `Application` (1:N), `SelectionDecision` (0..1) | Sí |
| `JobProfile` | Perfil del puesto | `Vacancy` | Sí |
| `EvaluationCriterion` | Criterio con etapa, ponderación y rango | `Vacancy`; resultados de evaluación y entrevista | Sí |
| `CandidateProfile` | Perfil profesional del postulante | `User`; `CandidateDocument` | No (dato global del postulante) |
| `CandidateDocument` | CV en PDF privado | `CandidateProfile` | No |
| `Application` | Postulación (`ApplicationStatus`) | `Vacancy`, postulante, CV usado, `ApplicationStageHistory`, `Evaluation`, `Interview` | Sí |
| `ApplicationStageHistory` | Historial de etapas | `Application`, usuario | Sí |
| `Evaluation` | Evaluación programada o realizada (`EvaluationType`) | `Application`, evaluador; `EvaluationResult` | Sí |
| `EvaluationResult` | Puntaje por criterio de evaluación | `Evaluation`, `EvaluationCriterion` | Sí |
| `Interview` | Entrevista (`InterviewOutcome`) | `Application`, evaluador; `InterviewResult` | Sí |
| `InterviewResult` | Puntaje por criterio de entrevista | `Interview`, `EvaluationCriterion` | Sí |
| `SelectionDecision` | Decisión final humana (justificación, posición y puntaje al decidir, registro de la selección) | `Vacancy` (única), postulación elegida, decisor | Sí |
| `AuditLog` | Registro de auditoría de solo inserción | Organización, actor, entidad polimórfica | Sí (nulo para cuentas globales) |

**Enums con comportamiento** (`app/Enums`):
- `JobRequestStatus`, `ApplicationStatus` y `VacancyStatus`, con transiciones permitidas.
- `UserRole`, `CriterionStage`, `EvaluationType`, `InterviewOutcome`, `VacancyClosureType`, `AssessmentStatus`, `Modality`, `ContractType`, `EducationLevel`, `DocumentType` y `JobRequestDecision`.
- `AuditAction`, con 23 acciones.

**Servicios de dominio**, que concentran el comportamiento:
- `JobRequestWorkflow`
- `VacancyService` y `VacancyValidator`
- `CandidateProfileService`
- `ApplicationService` y `ApplicationStageService`
- `AssessmentScheduler`, `AssessmentResultRecorder` y `ScoreSheetValidator`
- `WeightingValidator`
- `RankingService` y `VacancyRankingBuilder`
- `FinalDecisionService`, `SelectionRegistrationService` y `VacancyClosureService`
- `AuditLogger`

## 3. Relación con requerimientos

| Clases | RF |
|---|---|
| `JobRequest` y su historial | RF-01 a RF-04 |
| `Vacancy`, `JobProfile`, `EvaluationCriterion` | RF-05 a RF-07, RF-20 |
| `CandidateProfile`, `CandidateDocument`, `Application` e historial | RF-08 a RF-15 |
| `Evaluation`, `Interview` y sus resultados | RF-16 a RF-20 |
| `SelectionDecision` + servicios de ranking y selección | RF-21 a RF-25 |
| Notificaciones | RF-26 |
| `AuditLog` | RF-27 |

## 4. Relación con implementación

- Cada clase corresponde a una tabla creada por las 17 migraciones.
- Las restricciones de la base de datos refuerzan las invariantes: estados válidos, rango de puntajes, un único seleccionado por vacante y una decisión por vacante.
- El modelo de datos completo (ERD) está en el [capítulo 6, sección 6.7](../06-diseno-sistema.md#67-modelo-de-datos).

## 5. Consistencias

Las clases, relaciones y *enums* descritos existen en el código y los usan las pruebas PHPUnit: por ejemplo, `ApplicationStatusTest` y `JobRequestStatusTest` para las transiciones, y `RankingServiceTest` para el ranking.

## 6. Diferencias detectadas

No hay un diagrama original contra el cual comparar.

## 7. Limitaciones

La descripción es escrita. La representación Mermaid del capítulo 6 es derivada del código y no sustituye a un diagrama UML del equipo.

## 8. Estado para entrega

**Vigente** (descripción escrita basada en el código).

## 9. Recomendación

Si el curso exige un diagrama de clases gráfico, elaborarlo a partir de esta tabla y del capítulo 6 en la herramienta del equipo, y verificarlo contra `app/Models`.
