# Formato 07 — Requerimientos no funcionales

> Espejo en Markdown de `F7_Requerimientos_No_Funcionales_Colegio_Andino.docx`, generado desde el mismo modelo (`docs/academico/tools/f27b/`). El entregable es el DOCX.

## 1. Datos generales del proyecto

| Campo | Valor |
|---|---|
| Nombre del proyecto | Análisis y Diseño de una Plataforma SaaS Multiempresa para la Gestión del Reclutamiento, Evaluación y Selección de Personal – Caso de estudio: Colegio Andino de Huancayo |
| Integrantes del equipo | Coronacion Meza Fredy; Peña Arroyo Anthony; Vila Meza Luis Antonio |
| Módulo / Sistema | Plataforma SaaS multiempresa de reclutamiento, evaluación y selección (línea base RF-01 a RF-27) |
| Docente | Dr. Maglioni Arana Caparachin |
| Fecha | 26/09/2026 |

> **Estado de la información de este formato**
>
> **HECHO VERIFICADO:** comprobado en el repositorio (código, pruebas ejecutadas, documentos versionados).
>
> **AS-IS PRELIMINAR:** reconstrucción del proceso actual hecha por el equipo; **sujeta a validación institucional** (RR. HH. / Administración del Colegio). No es un procedimiento validado por la institución.
>
> **TO-BE PROPUESTO:** proceso mejorado diseñado por el equipo; su adopción en la institución no está validada.
>
> **SOFTWARE IMPLEMENTADO:** comportamiento de la plataforma v1.1 (etiqueta v1.1.0-academic), verificado con pruebas.
>
> **EXPERIMENTAL / PROPUESTO:** RF-28 (candidato, no implementado), RF-29 (experimental, solo sobre el proceso) y RNF-C (propuesta). No forman parte de la línea base RF-01 a RF-27.
>
> La prioridad es una **priorización analítica del equipo**. Cada RNF declara su **estado real de validación**: verificado, evidencia parcial, no verificado o propuesto. Las pruebas exploratorias no se presentan como SLA, y RNF-C no se presenta como requisito implementado.
>
> La plataforma **nunca** selecciona, descarta ni contrata automáticamente: el ranking calcula, ordena y compara.
>
> La decisión final de selección es **humana**: la registra el Aprobador / Dirección con confirmación explícita y justificación (RF-23).
>
> Todos los datos de ejemplo son ficticios. No se usan datos personales reales.

## 2. Descripción general del sistema

*Describir brevemente el sistema a desarrollar.*

**Objetivo del sistema.**

> Gestionar de forma centralizada, trazable y multiempresa el ciclo de reclutamiento, evaluación y selección de personal: desde el requerimiento hasta el cierre de la convocatoria. Los datos de cada organización quedan aislados y la decisión final de selección se reserva a una persona autorizada (Aprobador / Dirección).

**Funcionalidades principales.**

- Requerimientos de personal con validación y aprobación (RF-01 a RF-04).
- Vacantes con perfil, criterios ponderados, validación y publicación (RF-05 a RF-07).
- Cuenta, perfil, CV y postulación del postulante (RF-08 a RF-11).
- Revisión, etapas y notificaciones (RF-12 a RF-15).
- Evaluaciones y entrevistas con convocatoria y registro de resultados (RF-16 a RF-20).
- Ranking y comparación explicables, decisión humana, selección, cierre y resultado (RF-21 a RF-26).
- Auditoría de solo inserción (RF-27).

**Relación con los requerimientos funcionales.**

> Los RNF son **transversales**: se aplican a los 27 RF del Formato 06 y no crean módulos propios. La matriz de trazabilidad F2–F9 indica los RNF más relevantes para cada RF.

## 3. Lista de requerimientos no funcionales

| ID | Categoría | Nombre del requerimiento | Descripción | Métrica / Criterio | Prioridad |
|---|---|---|---|---|---|
| RNF-01 | Seguridad | Seguridad y control de acceso | El sistema debe autenticar a todo usuario y autorizar cada operación en el servidor según su rol y su organización. | Toda ruta del personal exige sesión y rol (middleware `role` y Policies). Contraseñas con hash bcrypt. Límite de 5 intentos de inicio de sesión por minuto. Las pruebas de autorización por rol pasan sin fallos. | Alta |
| RNF-02 | Seguridad | Multitenencia y aislamiento | El sistema debe garantizar que ninguna organización acceda a los datos de otra. | Toda entidad de negocio lleva `organization_id` y un scope global. Las Policies comparan rol y organización. Las pruebas cross-tenant pasan sin fallos. | Alta |
| RNF-03 | Seguridad (responsabilidad) | Trazabilidad y auditoría | El sistema debe registrar el usuario, la organización, la acción, la fecha y el objeto afectado de cada acción crítica, en un registro que no se pueda modificar. | Cada acción crítica deja un registro. La tabla `audit_logs` rechaza UPDATE y DELETE mediante un trigger. Los historiales de estado registran quién, cuándo y de qué estado a cuál. | Alta |
| RNF-04 | Seguridad (confidencialidad) | Privacidad | El sistema debe minimizar los datos del postulante y restringir su acceso según el rol y el vínculo con la vacante. | No se almacenan DNI, fecha de nacimiento ni atributos sensibles no requeridos. El CV se guarda en disco privado con nombre UUID y solo lo descargan los usuarios autorizados por la Policy. Las notificaciones no incluyen datos de otros candidatos. | Alta |
| RNF-05 | Usabilidad | Usabilidad | El sistema debe ofrecer formularios, mensajes y navegación comprensibles y consistentes. | Interfaz en español; errores por campo; estados vacíos; navegación por rol; diseño adaptable de 320 a 1440 px; contraste AA en modo claro y oscuro; foco visible y enlace de salto. | Media |
| RNF-06 | Eficiencia de desempeño | Rendimiento | El sistema debe permitir medir sus operaciones críticas contra una línea base documentada. | **Criterio propuesto:** fijar un entorno de referencia, medir una línea base de las operaciones críticas (listado de postulaciones, comparación, registro de decisión) y aprobar umbrales antes de cualquier aceptación productiva. **No hay umbral aprobado.** | Media |
| RNF-07 | Fiabilidad | Disponibilidad y recuperabilidad | El sistema debe permitir detectar fallas y recuperarse de ellas sin corromper los datos. | **Criterio propuesto:** procedimiento de respaldo y restauración de la base probado, y objetivos de disponibilidad aprobados. **No definidos.** | Media |
| RNF-08 | Compatibilidad | Compatibilidad | El sistema debe operar en los navegadores modernos definidos para el entorno académico. | **Criterio propuesto:** lista de navegadores y versiones aprobada, y pruebas en cada uno. **No hay matriz formal.** | Baja |
| RNF-09 | Mantenibilidad | Mantenibilidad | El sistema debe mantener una arquitectura modular con separación de responsabilidades. | Monolito modular por dominio: controlador delgado → Form Request → Policy → servicio → modelo, con máquinas de estado en enums. Suites automatizadas de regresión en CI: build, tsc y PHPUnit. | Media |
| RNF-10 | Seguridad (integridad) | Integridad de datos | El sistema debe validar estados, rangos, ponderaciones y resultados antes de guardarlos. | Form Requests en cada operación; máquinas de estado que rechazan transiciones inválidas; validadores de ponderaciones y puntajes; restricciones CHECK, UNIQUE y FK; un solo seleccionado por vacante; los IDs no numéricos devuelven 404. | Alta |

## 4. Detalle de requerimientos no funcionales

**RNF-01: Seguridad y control de acceso**

| Campo | Detalle |
|---|---|
| Categoría | Seguridad |
| Descripción | El sistema debe autenticar a todo usuario y autorizar cada operación en el servidor según su rol y su organización. |
| Métrica o criterio de aceptación | Toda ruta del personal exige sesión y rol (middleware `role` y Policies). Contraseñas con hash bcrypt. Límite de 5 intentos de inicio de sesión por minuto. Las pruebas de autorización por rol pasan sin fallos. |
| Justificación | El sistema gestiona datos de postulantes y decisiones de contratación: un acceso indebido compromete la confidencialidad y la decisión. |
| Método de verificación | Pruebas automatizadas: AuthenticationTest, RoleMiddlewareTest, pruebas «solo X puede…», E2E-01 y E2E-12. |
| Estado real de validación | **VERIFICADO** |
| Evidencia y límites | QA de la F25: PHPUnit 411 superadas y 0 fallidas; Cypress 85/85 (docs/v1.1/phase-25-final-qa.md). |

**RNF-02: Multitenencia y aislamiento**

| Campo | Detalle |
|---|---|
| Categoría | Seguridad |
| Descripción | El sistema debe garantizar que ninguna organización acceda a los datos de otra. |
| Métrica o criterio de aceptación | Toda entidad de negocio lleva `organization_id` y un scope global. Las Policies comparan rol y organización. Las pruebas cross-tenant pasan sin fallos. |
| Justificación | Es la condición del modelo SaaS multiempresa: una fuga entre organizaciones invalida el producto. |
| Método de verificación | Pruebas automatizadas: CrossTenantAccessTest, OrganizationScopeTest, pruebas cross-tenant por RF y E2E-11. |
| Estado real de validación | **VERIFICADO** |
| Evidencia y límites | F25: sin fugas entre organizaciones y 22 pruebas cross-tenant explícitas (phase-25-final-qa.md §14). |

**RNF-03: Trazabilidad y auditoría**

| Campo | Detalle |
|---|---|
| Categoría | Seguridad (responsabilidad) |
| Descripción | El sistema debe registrar el usuario, la organización, la acción, la fecha y el objeto afectado de cada acción crítica, en un registro que no se pueda modificar. |
| Métrica o criterio de aceptación | Cada acción crítica deja un registro. La tabla `audit_logs` rechaza UPDATE y DELETE mediante un trigger. Los historiales de estado registran quién, cuándo y de qué estado a cuál. |
| Justificación | Da sustento a la decisión humana y permite reconstruir el proceso (P2, P5). |
| Método de verificación | Pruebas automatizadas: AuditTrailTest, AuditLogViewTest, AuditLoggerTest y E2E-11; inspección del trigger `audit_logs_append_only`. |
| Estado real de validación | **VERIFICADO** |
| Evidencia y límites | DEF-07 y DEF-08 corregidos y cubiertos por pruebas (docs/defects.md). |

**RNF-04: Privacidad**

| Campo | Detalle |
|---|---|
| Categoría | Seguridad (confidencialidad) |
| Descripción | El sistema debe minimizar los datos del postulante y restringir su acceso según el rol y el vínculo con la vacante. |
| Métrica o criterio de aceptación | No se almacenan DNI, fecha de nacimiento ni atributos sensibles no requeridos. El CV se guarda en disco privado con nombre UUID y solo lo descargan los usuarios autorizados por la Policy. Las notificaciones no incluyen datos de otros candidatos. |
| Justificación | Protege a los postulantes y limita la exposición de datos personales. |
| Método de verificación | Pruebas automatizadas: CandidateProfileTest y ProcessResultNotificationTest; inspección de la Policy CandidateDocumentPolicy y del modelo de datos (A-15). |
| Estado real de validación | **VERIFICADO** |
| Evidencia y límites | Solo datos ficticios en el repositorio; barrido de secretos y PII en la F25 y la F26. |

**RNF-05: Usabilidad**

| Campo | Detalle |
|---|---|
| Categoría | Usabilidad |
| Descripción | El sistema debe ofrecer formularios, mensajes y navegación comprensibles y consistentes. |
| Métrica o criterio de aceptación | Interfaz en español; errores por campo; estados vacíos; navegación por rol; diseño adaptable de 320 a 1440 px; contraste AA en modo claro y oscuro; foco visible y enlace de salto. |
| Justificación | Los usuarios del Colegio y los postulantes no son técnicos. Los errores de uso afectan a la calidad del registro. |
| Método de verificación | Recorrido manual (docs/manual-smoke-test.md), QA visual y de accesibilidad de la F21 (E2E-16, E2E-19, contraste automatizado) y QA de la F25. |
| Estado real de validación | **EVIDENCIA PARCIAL** |
| Evidencia y límites | No hay pruebas de usabilidad con usuarios reales, y la prueba con un lector de pantalla real está pendiente. La accesibilidad WCAG 2.1 AA como requisito es el candidato RNF-A (propuesta). |

**RNF-06: Rendimiento**

| Campo | Detalle |
|---|---|
| Categoría | Eficiencia de desempeño |
| Descripción | El sistema debe permitir medir sus operaciones críticas contra una línea base documentada. |
| Métrica o criterio de aceptación | **Criterio propuesto:** fijar un entorno de referencia, medir una línea base de las operaciones críticas (listado de postulaciones, comparación, registro de decisión) y aprobar umbrales antes de cualquier aceptación productiva. **No hay umbral aprobado.** |
| Justificación | Hace falta una base objetiva antes de fijar un SLA. El volumen académico es bajo. |
| Método de verificación | Medición en un entorno acordado (Navigation Timing o pruebas de carga), a definir. |
| Estado real de validación | **NO VERIFICADO** |
| Evidencia y límites | Solo hay medición exploratoria de la F25 en un equipo potente: no es un benchmark ni un SLA. No se ejecutaron pruebas de carga. El presupuesto de rendimiento es el candidato RNF-B (propuesta). |

**RNF-07: Disponibilidad y recuperabilidad**

| Campo | Detalle |
|---|---|
| Categoría | Fiabilidad |
| Descripción | El sistema debe permitir detectar fallas y recuperarse de ellas sin corromper los datos. |
| Métrica o criterio de aceptación | **Criterio propuesto:** procedimiento de respaldo y restauración de la base probado, y objetivos de disponibilidad aprobados. **No definidos.** |
| Justificación | Evita perder expedientes y decisiones. El entorno entregado es de desarrollo y demostración (A-36). |
| Método de verificación | Prueba de respaldo y restauración y monitoreo del servicio, a definir. |
| Estado real de validación | **NO VERIFICADO** |
| Evidencia y límites | Hay controles de integridad (transacciones, notificaciones tras el commit, restricciones de la base) y healthchecks de Docker Compose, pero no pruebas de respaldo o restauración ni objetivos de disponibilidad. |

**RNF-08: Compatibilidad**

| Campo | Detalle |
|---|---|
| Categoría | Compatibilidad |
| Descripción | El sistema debe operar en los navegadores modernos definidos para el entorno académico. |
| Métrica o criterio de aceptación | **Criterio propuesto:** lista de navegadores y versiones aprobada, y pruebas en cada uno. **No hay matriz formal.** |
| Justificación | El uso académico se concentra en navegadores de escritorio y móviles actuales. |
| Método de verificación | Suite E2E en cada navegador de la lista, a definir. |
| Estado real de validación | **EVIDENCIA PARCIAL** |
| Evidencia y límites | Cypress se ejecuta en Electron (motor Chromium), con anchos de 320 a 1440 px. Firefox y Safari no se probaron de forma sistemática. |

**RNF-09: Mantenibilidad**

| Campo | Detalle |
|---|---|
| Categoría | Mantenibilidad |
| Descripción | El sistema debe mantener una arquitectura modular con separación de responsabilidades. |
| Métrica o criterio de aceptación | Monolito modular por dominio: controlador delgado → Form Request → Policy → servicio → modelo, con máquinas de estado en enums. Suites automatizadas de regresión en CI: build, tsc y PHPUnit. |
| Justificación | Facilita la evolución (v1.1) sin romper la línea base. |
| Método de verificación | Inspección de la estructura de `app/`; suites PHPUnit, Vitest y tsc; CI de GitHub. |
| Estado real de validación | **EVIDENCIA PARCIAL** |
| Evidencia y límites | La estructura y las suites están verificadas (F25: 411 PHPUnit, 42 Vitest, tsc sin errores). No se midieron métricas de mantenibilidad (complejidad, cobertura) y hay deuda de formato aceptada (Pint, vp check). |

**RNF-10: Integridad de datos**

| Campo | Detalle |
|---|---|
| Categoría | Seguridad (integridad) |
| Descripción | El sistema debe validar estados, rangos, ponderaciones y resultados antes de guardarlos. |
| Métrica o criterio de aceptación | Form Requests en cada operación; máquinas de estado que rechazan transiciones inválidas; validadores de ponderaciones y puntajes; restricciones CHECK, UNIQUE y FK; un solo seleccionado por vacante; los IDs no numéricos devuelven 404. |
| Justificación | La integridad es la base del ranking y de la decisión (P3). |
| Método de verificación | Pruebas automatizadas: WeightingValidatorTest, ScoreSheetValidatorTest, ApplicationStatusTest, SelectionRegistrationTest y NumericRouteParametersTest. |
| Estado real de validación | **VERIFICADO** |
| Evidencia y límites | F25-M01 corregido (500 → 404) con prueba de regresión. |

## 5. Clasificación por atributos de calidad

| Categoría | Requerimientos asociados |
|---|---|
| Rendimiento | RNF-06 |
| Seguridad | RNF-01, RNF-02, RNF-03, RNF-04, RNF-10 |
| Usabilidad | RNF-05 |
| Disponibilidad | RNF-07 |
| Compatibilidad | RNF-08 |
| Mantenibilidad | RNF-09 |

**Matriz de equivalencia: RNF académico ↔ RNF técnico ↔ evidencia ↔ estado**

| RNF académico (F9) | RNF técnico (informe v1.0, cap. 4 §4.3) | Relación | Estado |
|---|---|---|---|
| RNF-01 Seguridad y control de acceso | cap. 4 RNF-01 (autenticación) + RNF-02 (autorización) | 1 → 2 | VERIFICADO |
| RNF-02 Multitenencia y aislamiento | cap. 4 RNF-03 (aislamiento multiempresa) | 1 → 1 | VERIFICADO |
| RNF-03 Trazabilidad y auditoría | cap. 4 RNF-05 (responsabilidad) + RNF-10 (trazabilidad funcional) | 1 → 2 | VERIFICADO |
| RNF-04 Privacidad | cap. 4 RNF-06 (privacidad) | 1 → 1 | VERIFICADO |
| RNF-05 Usabilidad | cap. 4 RNF-07 (usabilidad); candidato RNF-A (accesibilidad, propuesta) | 1 → 1 (+ candidato) | EVIDENCIA PARCIAL |
| RNF-06 Rendimiento | Sin equivalente técnico (el cap. 4 declara que no hay SLA ni pruebas de carga); candidato RNF-B (propuesta) | 1 → 0 | NO VERIFICADO |
| RNF-07 Disponibilidad y recuperabilidad | Sin equivalente técnico | 1 → 0 | NO VERIFICADO |
| RNF-08 Compatibilidad | Sin equivalente técnico (el cap. 4 RNF-07 cubre el diseño adaptable, no los navegadores) | 1 → 0 (parcial) | EVIDENCIA PARCIAL |
| RNF-09 Mantenibilidad | cap. 4 RNF-08 (mantenibilidad) | 1 → 1 | EVIDENCIA PARCIAL |
| RNF-10 Integridad de datos | cap. 4 RNF-04 (integridad) | 1 → 1 | VERIFICADO |

La relación **no es 1:1**. Tres RNF académicos (RNF-06, RNF-07 y RNF-08) no tienen equivalente técnico, y dos RNF técnicos no tienen equivalente académico. Unificar los catálogos es una decisión del equipo (F24 L-01).

| RNF técnico sin equivalente académico | Requerimiento | Estado |
|---|---|---|
| cap. 4 RNF-09 | Portabilidad: ejecución completa con Docker e instalación desde cero documentada | VERIFICADO (docs/docker.md; validación en un clon limpio, cap. 10) |
| cap. 4 RNF-11 | Adecuación (localización): fechas y horas en America/Lima | VERIFICADO (AppTimezoneTest, DEF-09) |

**Candidatos fuera de la línea base**

| ID | Candidato | Estado | Observación |
|---|---|---|---|
| RNF-A | Accesibilidad WCAG 2.1 AA verificada en las pantallas de RF-01 a RF-27 | PROPUESTO | Hay evidencia parcial de la F21 y la F25; falta un lector de pantalla real |
| RNF-B | Presupuesto de rendimiento del frontend con línea base medida | PROPUESTO | Sin línea base aprobada |
| RNF-C | Experiencia 3D progresiva en pantallas públicas | PROPUESTO | Implementada en la F20 (portada, CSS 3D), pero **no promovida**: implementar no promueve un requisito (decisión 11) |
