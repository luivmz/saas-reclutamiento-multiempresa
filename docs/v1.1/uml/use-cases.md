# UC-01 · Diagrama de casos de uso

| | |
|---|---|
| **Objetivo** | Mostrar qué hace cada actor con el sistema y cómo se reparten RF-01 a RF-29 |
| **Alcance** | Sistema completo en `develop` (`aced6da`). Un solo diagrama principal |
| **Fuente de verdad** | `routes/web.php`, `app/Policies/*`, `EnsureUserHasRole`, `app/Enums/UserRole.php`, servicios que disparan notificaciones y auditoría |
| **Borrador textual** | [`puml/uc-01-use-cases.puml`](puml/uc-01-use-cases.puml) |
| **RF** | RF-01 a RF-29 (RF-28 como candidato no implementado) |

## 1. Actores

| Actor | Tipo | Generalización |
|---|---|---|
| Área solicitante | Primario | — |
| Recursos Humanos | Primario | — |
| Aprobador / Dirección | Primario | — |
| Evaluador | Primario | — |
| Postulante | Primario | Incluye al visitante sin sesión para la consulta pública (RF-07) y el registro (RF-08) |
| Servicio de riesgo operacional | Secundario, `<<external service>>` `<<experimental>>` | — |

No hay generalización entre actores del personal: sus permisos no se heredan (por ejemplo, el Aprobador no puede validar requerimientos ni RR. HH. decidir). Dibujar un actor «Personal» abstracto sería una simplificación falsa.

## 2. Casos de uso

Nombres del catálogo oficial, sin renumerar ni fusionar. **Iniciado por** = quién lo ejecuta según las Policies; **sistema** = el caso lo ejecuta el sistema como efecto de otro (no lo inicia un actor).

| CU | Caso de uso | RF | Iniciado por | Estado |
|---|---|---|---|---|
| UC-RF01 | Registrar requerimiento de personal | RF-01 | Área solicitante | AS-IS |
| UC-RF02 | Validar y corregir requerimiento | RF-02 | Área solicitante (corregir y reenviar lo propio) · RR. HH. (validar u observar) | AS-IS |
| UC-RF03 | Registrar aprobación o rechazo del requerimiento | RF-03 | Aprobador / Dirección | AS-IS |
| UC-RF04 | Notificar rechazo del requerimiento | RF-04 | Sistema | AS-IS |
| UC-RF05 | Registrar perfil y criterios del puesto | RF-05 | RR. HH. | AS-IS |
| UC-RF06 | Configurar y validar vacante | RF-06 | RR. HH. | AS-IS |
| UC-RF07 | Publicar vacante | RF-07 | RR. HH. (publica) · Postulante/visitante (consulta pública) | AS-IS |
| UC-RF08 | Gestionar cuenta y acceso del postulante | RF-08 | Postulante | AS-IS |
| UC-RF09 | Gestionar perfil y CV del postulante | RF-09 | Postulante | AS-IS |
| UC-RF10 | Registrar postulación | RF-10 | Postulante | AS-IS |
| UC-RF11 | Confirmar postulación al postulante | RF-11 | Sistema | AS-IS |
| UC-RF12 | Consultar y revisar postulaciones | RF-12 | RR. HH. · Aprobador / Dirección | AS-IS |
| UC-RF13 | Registrar preselección o descarte | RF-13 | RR. HH. | AS-IS |
| UC-RF14 | Gestionar cambio de etapa de la postulación | RF-14 | RR. HH. | AS-IS |
| UC-RF15 | Notificar cambio de etapa al candidato | RF-15 | Sistema | AS-IS |
| UC-RF16 | Programar evaluación | RF-16 | RR. HH. | AS-IS |
| UC-RF17 | Generar convocatoria de evaluación | RF-17 | Sistema | AS-IS |
| UC-RF18 | Programar entrevista | RF-18 | RR. HH. | AS-IS |
| UC-RF19 | Registrar entrevista y su resultado | RF-19 | Evaluador asignado | AS-IS |
| UC-RF20 | Validar rangos y ponderaciones | RF-20 | Sistema | AS-IS |
| UC-RF21 | Calcular ranking configurable | RF-21 | Sistema | AS-IS |
| UC-RF22 | Presentar comparación de candidatos | RF-22 | RR. HH. · Aprobador / Dirección | AS-IS |
| UC-RF23 | Registrar decisión final de selección | RF-23 | **Aprobador / Dirección** `<<human decision>>` | AS-IS |
| UC-RF24 | Registrar selección del candidato | RF-24 | RR. HH. | AS-IS |
| UC-RF25 | Cerrar vacante o convocatoria | RF-25 | RR. HH. | AS-IS (solo cierre con selección, A-30) |
| UC-RF26 | Notificar resultado y cierre al postulante | RF-26 | Sistema | AS-IS |
| UC-RF27 | Generar registro de auditoría | RF-27 | Sistema (registro) · Aprobador / Dirección (consulta) | AS-IS |
| UC-RF28 | Panel operativo descriptivo | RF-28 | — | **CANDIDATO, NO IMPLEMENTADO** `<<propuesto v1.1>>` |
| UC-RF29 | Consultar riesgo operacional del proceso | RF-29 | RR. HH. · Aprobador / Dirección, con el servicio de riesgo como actor secundario | **EXPERIMENTAL** `<<experimental>>` |

UC-RF19 cubre, como en el catálogo, el registro de resultados de **evaluaciones y entrevistas**: ambos los registra el Evaluador asignado con la misma planilla por criterio.

## 3. Relaciones `<<include>>` y `<<extend>>`

Solo las que corresponden a un comportamiento real. Cada una se justifica con el código.

| Base | Relación | Destino | Por qué |
|---|---|---|---|
| UC-RF03 | `<<extend>>` (condición: decisión = rechazar) | UC-RF04 | `JobRequestWorkflow::reject` notifica al solicitante; `approve` no. Es condicional, luego *extend* |
| UC-RF06 | `<<include>>` | UC-RF20 | `WeightingValidator` valida ponderaciones y rangos al configurar |
| UC-RF07 | `<<include>>` | UC-RF06 | `VacancyService::publish` vuelve a validar con `VacancyValidator`; no se publica sin configuración válida |
| UC-RF10 | `<<include>>` | UC-RF11 | `ApplicationService::apply` siempre envía `ApplicationReceivedNotification` |
| UC-RF13 | `<<include>>` | UC-RF15 | Preseleccionar y descartar notifican siempre al candidato |
| UC-RF14 | `<<include>>` | UC-RF15 | El cambio manual de etapa notifica siempre al candidato |
| UC-RF16 | `<<include>>` | UC-RF17 | `AssessmentScheduler` envía la convocatoria al candidato y el aviso al evaluador |
| UC-RF18 | `<<include>>` | UC-RF17 | La entrevista usa la misma convocatoria (`AssessmentConvocationNotification`). El nombre del RF dice «evaluación»; la implementación la aplica a ambas sesiones |
| UC-RF19 | `<<include>>` | UC-RF20 | `ScoreSheetValidator` rechaza puntajes fuera de rango o criterios ajenos |
| UC-RF22 | `<<include>>` | UC-RF21 | La comparación calcula el ranking en cada consulta (`VacancyRankingBuilder`) |
| UC-RF21 | `<<include>>` | UC-RF20 | `RankingService` rechaza configuración o puntajes inválidos |
| UC-RF23 | `<<include>>` | UC-RF21 | La decisión recalcula el ranking **solo para guardar la instantánea** (posición, puntaje, candidatos rankeados). No elige: el candidato lo elige la persona |
| UC-RF25 | `<<include>>` | UC-RF26 | `VacancyClosureService` notifica el resultado a cada postulante al cerrar |

**Relaciones que no se dibujan, a propósito:**

- **RF-27 no se une con 20 líneas `<<include>>`**. Toda acción crítica llama a `AuditLogger` (23 acciones). Se representa como una nota transversal anclada a UC-RF27 que enumera los casos auditados, más la asociación del Aprobador con UC-RF27 para la consulta. Dibujar todas las inclusiones saturaría el diagrama sin información nueva.
- **UC-RF24 no incluye a UC-RF23**: lo *requiere* (precondición, `BusinessRuleException` si no hay decisión), que no es lo mismo que incluirlo. Va como nota de precondición.
- **UC-RF29 no se relaciona con UC-RF21, UC-RF22 ni UC-RF23**: el riesgo operacional no alimenta el ranking ni la decisión. Esa ausencia de relación es la frontera de RF-29 y se dibuja como nota.
- **UC-RF14 no incluye el avance automático** que hace `AssessmentScheduler` al programar (postulación a `en_evaluacion` o `en_entrevista`): es un efecto interno de UC-RF16 y UC-RF18, sin notificación de etapa propia; va en la especificación de esos casos.

## 4. Semántica crítica (notas obligatorias en el diagrama)

- **UC-RF21 / UC-RF22 — soporte a la decisión.** Calculan, ordenan y comparan; no seleccionan, no descartan y no cambian el estado de ninguna postulación (`test_rf23_calculating_the_ranking_never_selects_a_candidate`).
- **UC-RF23 — `<<human decision>>`.** Solo el Aprobador de la misma organización; exige `human_confirmation` aceptada y justificación de al menos 20 caracteres; el candidato debe ser **finalista** con resultados completos, **no necesariamente el primero** del ranking; la decisión es única e inmutable por vacante. No cambia el estado de la postulación por sí sola. **No depende del ML.**
- **UC-RF24 / UC-RF25.** Solo tras UC-RF23. El cierre deja `seleccionado` a la elegida y `no_seleccionado` al resto de las activas. Tras la decisión, RR. HH. no puede cambiar etapas en esa vacante (A-28).
- **UC-RF29 — `<<experimental>>`.** Riesgo operacional del **proceso** de la vacante, no del candidato. No selecciona, no descarta, no ordena ni modifica el ranking. La petición al servicio lleva 15 features operacionales y ningún identificador ni PII. Validado solo con datos sintéticos; no productivo. RF-29 sigue siendo candidato.
- **UC-RF28 — candidato no implementado.** Panel agregado de tiempos, *backlog* y cuellos de botella (definición en `docs/v1.1/ml/requirements-and-traceability-plan.md`). **El estado `descriptive_only` de la tarjeta de UC-RF29 no es este panel**: solo muestra una etiqueta y un mensaje explicativo. Dibujarlo con estereotipo `<<propuesto v1.1>>`, sin asociación a actores ni al sistema implementado.
- **Multiempresa.** Todos los casos del personal operan dentro de su organización (Policy de rol **y** organización). El Postulante es global y solo ve lo suyo.

## 5. Asociaciones actor ↔ caso

| Actor | Casos |
|---|---|
| Área solicitante | UC-RF01, UC-RF02 |
| Recursos Humanos | UC-RF02, UC-RF05, UC-RF06, UC-RF07, UC-RF12, UC-RF13, UC-RF14, UC-RF16, UC-RF18, UC-RF22, UC-RF24, UC-RF25, UC-RF29 |
| Aprobador / Dirección | UC-RF03, UC-RF12, UC-RF22, UC-RF23, UC-RF27, UC-RF29 |
| Evaluador | UC-RF19 |
| Postulante | UC-RF07 (consulta pública), UC-RF08, UC-RF09, UC-RF10 |
| Servicio de riesgo operacional | UC-RF29 |

Los casos del sistema (UC-RF04, UC-RF11, UC-RF15, UC-RF17, UC-RF20, UC-RF21, UC-RF26 y el registro de UC-RF27) no se asocian a actores: se alcanzan por `<<include>>` o `<<extend>>`. El destinatario de cada notificación figura en la nota del caso: UC-RF04 → solicitante; UC-RF11, UC-RF15, UC-RF26 → postulante; UC-RF17 → postulante y evaluador.

## 6. Contraste con el diagrama de v1.0

El informe [`03-use-case-report.md`](../../final-report/diagram-reports/03-use-case-report.md) agrupa los RF en 13 casos (CU-01 a CU-13). Este diagrama **no lo reemplaza**: presenta un caso por RF, que es lo que pide la trazabilidad de v1.1, y conserva los mismos cinco actores. Diferencias de contenido:

| v1.0 | v1.1 AS-IS |
|---|---|
| CU-09 atribuye RF-20 al Evaluador | RF-20 es un caso del sistema: lo incluyen la configuración (RF-06), el registro de resultados (RF-19) y el ranking (RF-21) |
| No hay riesgo operacional | UC-RF29 experimental, con actor secundario |
| — | UC-RF28 como candidato, sin implementar |

## 7. Instrucciones para F23

1. Crear el diagrama en el OOM como *Use Case Diagram* «UC-01 Casos de uso AS-IS v1.1».
2. Crear los seis actores; el servicio de riesgo con estereotipos `<<external service>>` y `<<experimental>>`.
3. Crear los 29 casos con el código `UC-RFnn` y el nombre oficial; UC-RF28 con `<<propuesto v1.1>>` y color gris.
4. Trazar las asociaciones de §5 y las relaciones de §3; ninguna otra.
5. Añadir las notas de §4 y la nota transversal de auditoría.
6. Registrar el resultado en el informe de diagramas de v1.1.
