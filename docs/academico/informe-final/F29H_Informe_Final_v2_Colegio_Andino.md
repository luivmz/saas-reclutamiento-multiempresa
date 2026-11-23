# SaaS Reclutamiento Multiempresa

## CAPÍTULO 1. INFORMACIÓN GENERAL DEL PROYECTO

### 1.1. Resumen Ejecutivo

Este informe presenta el análisis, diseño, implementación y verificación del proyecto grupal SaaS Reclutamiento Multiempresa. El caso académico es el Colegio Andino de Huancayo. El equipo propuso centralizar el expediente de cada convocatoria, registrar su avance y aplicar criterios comparables. El enunciado y el proceso preliminar se desarrollan en los capítulos 2 y 3.

La solución integrada cubre los 27 requisitos funcionales de la línea base. Una convocatoria pasa por la aprobación del requerimiento, la publicación, la postulación, la evaluación y la decisión de Dirección. El ranking explica sus cálculos. RF-23 exige que una persona autorizada confirme y justifique la decisión.

El corte documental es el **22 de noviembre de 2026, hora de Lima**. La base integrada es main [04d3cfa](https://github.com/luivmz/saas-reclutamiento-multiempresa/commit/04d3cfa1db6f82d9cda8db2254338805137cdc3c), con el mismo árbol que develop [4371d90](https://github.com/luivmz/saas-reclutamiento-multiempresa/commit/4371d90e6fb9682fe8076c978f33a3ce5f086b49). La rama de Reportes y SonarQube tiene sus propias evidencias. La rama del anfitrión incluye los dos vídeos de la continuación de presentación. El capítulo 9 fija los SHA y el capítulo 13 atribuye cada medición a su revisión.

En la presentación integrada, el registro experimental de evidencias versionadas y la búsqueda léxica ML-02 se habilitan con una bandera desactivada por omisión. ML-01 queda como servicio opcional de riesgo de demora del proceso. Los resultados técnicos se interpretan con datos ficticios. La adopción institucional, el uso productivo y los beneficios en el colegio siguen sin validación.

### 1.2. Introducción

El informe sigue los 14 capítulos oficiales del curso Pruebas y Calidad de Software, NRC 28607. Se preserva la reconstrucción AS-IS como hipótesis preliminar y el proceso TO-BE como diseño sujeto a validación del colegio. El software se documenta según su implementación y pruebas. Los resultados de ramas experimentales o académicas se vinculan con la revisión que se probó.

**Objetivo general.** Implementar y verificar una plataforma que apoye el reclutamiento de docentes y personal desde el requerimiento hasta el cierre, con trazabilidad por organización y decisión final humana.

- Consolidar requerimientos, vacantes, CV y expedientes con controles de acceso (P1).
- Hacer verificable el avance con estados, transiciones válidas y avisos en eventos clave (P2 y P4).
- Aplicar criterios ponderados y mostrar el cálculo para fundamentar la comparación (P3).
- Conservar la justificación y la auditoría del cierre, y estudiar indicadores operativos en una rama separada (P5).

## CAPÍTULO 2. CONTEXTO ORGANIZACIONAL Y ANÁLISIS DEL PROBLEMA

### 2.1. Contexto de la Organización

El Colegio Andino de Huancayo es el **caso de estudio académico** del proyecto. El repositorio no contiene documentación institucional verificada: no hay estadísticas de contratación, número de postulantes, organigrama ni herramientas actuales confirmadas. El contexto se describe como AS-IS PRELIMINAR, pendiente de validación con RR. HH. y la Administración del colegio.

- **Actividades principales (AS-IS PRELIMINAR):** 1) Detectar la necesidad de personal y comunicarla; 2) Revisar y aprobar la necesidad; 3) Definir el perfil del puesto y difundir la convocatoria; 4) Recibir las postulaciones y los CV; 5) Revisar y preseleccionar candidatos; 6) Coordinar evaluaciones y entrevistas; 7) Consolidar resultados y comparar candidatos; 8) Decidir y comunicar el resultado.
- **Área donde se presenta el problema:** reclutamiento, evaluación y selección de docentes y personal, con participación del área solicitante, RR. HH., la Dirección, los evaluadores y los postulantes.
- **Herramientas actuales:** no identificadas. El AS-IS preliminar no identifica ninguna herramienta informática del Colegio, y no se afirma que el proceso sea en papel, por correo ni con otra herramienta: queda pendiente de validación.

Fuentes. Formato 02 (análisis del proceso) y capítulo 2 de la documentación v1.0.

**Enunciado del caso práctico.** Diseñar e implementar una plataforma web multiempresa para gestionar el reclutamiento, la evaluación y la selección de personal, tomando como caso académico al Colegio Andino de Huancayo. El área solicitante inicia el requerimiento. RR. HH. lo valida y publica una convocatoria con perfil y criterios después de que la Dirección lo aprueba. Las personas interesadas postulan mediante el portal. Los evaluadores registran resultados de las sesiones asignadas. Dirección contrasta la evidencia disponible, confirma su decisión y la justifica. El equipo debe demostrar el flujo y las restricciones de acceso, y reconstruir las acciones críticas mediante evidencias con datos ficticios en un entorno reproducible.

### 2.2. Identificación del Problema

Problemas del proceso actual (AS-IS PRELIMINAR, Formato 04). Ninguno se midió: son hallazgos del análisis del equipo pendientes de validación.

| ID | Problema | Descripción | Causa | Impacto operativo | Nivel |
|---|---|---|---|---|---|
| P1 | Información distribuida | Los datos del proceso (requerimiento, perfil del puesto, CV, evaluaciones y decisiones) no están centralizados en un único registro por convocatoria. | Ausencia de un registro único por convocatoria | Dificulta reconstruir el expediente y el estado integral de una postulación; riesgo de pérdida o duplicación de información y menor trazabilidad. | Alta |
| P2 | Seguimiento manual | El avance de cada requerimiento y postulación se controla sin estados ni historial sistematizados. | Estados del proceso no definidos ni registrados | Poca visibilidad del estado del proceso y de quién hizo cada cambio; más esfuerzo para controlar etapas y responsables. | Alta |
| P3 | Evaluaciones heterogéneas | Los candidatos no se evalúan con criterios, ponderaciones y rangos definidos de antemano y comunes a toda la convocatoria. | Criterios de evaluación no definidos antes de evaluar | Comparaciones poco objetivas y difíciles de justificar; menor comparabilidad de resultados. | Alta |
| P4 | Comunicación manual | Los avisos a postulantes y participantes (recepción, cambios de etapa, convocatorias y resultado) dependen de gestiones manuales. | Avisos que dependen de una gestión manual en cada evento | Demoras u omisiones en la comunicación; es difícil comprobar qué se comunicó y cuándo. | Media |
| P5 | Indicadores limitados | No se dispone de información consolidada para comparar candidatos ni de trazabilidad de las acciones críticas. | Datos no consolidados y sin registro de acciones críticas | Decisiones con menos sustento, baja capacidad de auditoría y dificultad para medir demoras y resultados del proceso. | Media |

**Impacto en la eficiencia del proceso:** la falta de un registro único, de estados sistematizados y de criterios comunes dificulta reconstruir cada convocatoria, justificar la decisión y comunicar a tiempo a los postulantes. No se cuantificó ese impacto (no hay línea base medida).

## CAPÍTULO 3. ANÁLISIS DE PROCESOS DE NEGOCIO

### 3.1. Descripción del Proceso Actual

El proceso actual (AS-IS PRELIMINAR) se modeló en el Formato 02 con 14 actividades (AS-01 a AS-14) agrupadas en 8 macroactividades:

| # | Macroactividad | Responsable | Problemas |
|---|---|---|---|
| 1 | Detectar la necesidad de personal y comunicarla | Área solicitante | P1, P2 |
| 2 | Revisar y aprobar la necesidad | RR. HH. / Dirección | P2 |
| 3 | Definir el perfil del puesto y difundir la convocatoria | RR. HH. | P1 |
| 4 | Recibir las postulaciones y los CV | RR. HH. | P1, P4 |
| 5 | Revisar y preseleccionar candidatos | RR. HH. | P2 |
| 6 | Coordinar evaluaciones y entrevistas | RR. HH. / Evaluadores | P3, P4 |
| 7 | Consolidar resultados y comparar candidatos | RR. HH. | P3, P5 |
| 8 | Decidir y comunicar el resultado | Dirección / RR. HH. | P4, P5 |

### 3.2. Modelado del Proceso Actual (AS-IS)

El diagrama BPMN AS-IS se formalizó en PowerDesigner (Formato 03 y fase F29): pools del Colegio y del Postulante, carriles por actor y mensajes entre pools. La {{ref:asis}} reproduce el primer tramo en el anexo A.1.

| ID | Actividad | Descripción |
|---|---|---|
| AS-01 | Identificar la necesidad de personal | El área detecta que requiere cubrir un puesto (vacante, reemplazo o nueva plaza). |
| AS-02 | Comunicar la necesidad a RR. HH. | El área transmite la necesidad a RR. HH. El canal y el formato no están verificados. |
| AS-03 | Revisar la necesidad | RR. HH. revisa la necesidad comunicada antes de elevarla a Dirección. |
| AS-04 | Aprobar o no aprobar la necesidad | Dirección decide si la necesidad procede. Si no procede, el proceso termina para esa necesidad. |
| AS-05 | Definir el perfil del puesto | RR. HH. define el perfil del puesto a cubrir. |
| AS-06 | Difundir la convocatoria | RR. HH. da a conocer la convocatoria. Los medios de difusión no están verificados. |
| AS-07 | Presentar la postulación y el CV | La persona interesada presenta su postulación y su CV. |
| AS-08 | Recibir y reunir postulaciones y CV | RR. HH. recibe y reúne las postulaciones de la convocatoria. |
| AS-09 | Revisar el CV y preseleccionar al candidato | RR. HH. revisa el CV de cada candidato y decide si continúa (dentro de SP-01, una vez por candidato). No está verificado si se informa a quien no continúa. |
| AS-10 | Coordinar evaluaciones y entrevistas | RR. HH. coordina fechas y participantes, y cita a los candidatos preseleccionados. |
| AS-11 | Realizar evaluaciones y entrevistas | Los evaluadores evalúan y entrevistan a los candidatos y entregan sus resultados. No hay constancia de criterios, ponderaciones ni rangos comunes definidos de antemano. |
| AS-12 | Consolidar resultados y comparar candidatos | RR. HH. reúne los resultados de cada candidato y los compara. |
| AS-13 | Decidir el candidato seleccionado | Dirección decide a quién seleccionar a partir de la información consolidada. |
| AS-14 | Comunicar el resultado | RR. HH. comunica el resultado a los postulantes. El canal y el alcance de la comunicación no están verificados. |

### 3.3. Problemas del Proceso Actual

Relación entre los problemas y las actividades del AS-IS en las que aparecen (Formato 04):

| Problema | Actividades AS-IS | Validación pendiente con |
|---|---|---|
| P1 Información distribuida | AS-02, AS-05, AS-06, AS-08 | RR. HH. |
| P2 Seguimiento manual | AS-02, AS-03, AS-04, AS-09 | RR. HH. |
| P3 Evaluaciones heterogéneas | AS-11, AS-12 | RR. HH. / Dirección |
| P4 Comunicación manual | AS-07, AS-10, AS-14 | RR. HH. |
| P5 Indicadores limitados | AS-12, AS-13 | Dirección |

### 3.4. Modelado del Proceso Propuesto (TO-BE)

El proceso propuesto (TO-BE PROPUESTO, Formato 05) atiende cada problema con una solución y un objetivo de mejora. El BPMN TO-BE formal de PowerDesigner se referencia en el anexo A.1. La {{ref:tobe}} muestra el tramo del requerimiento. Su adopción por la institución no está validada.

| ID | Solución | Descripción | RF |
|---|---|---|---|
| P1 | S-01 Centralización de la información | Registro único por convocatoria en la plataforma multiempresa: requerimiento, vacante con perfil y criterios, perfil del postulante con CV privado y expediente de postulación. | RF-01, RF-05, RF-06, RF-09, RF-10, RF-12 |
| P2 | S-02 Control del avance y responsables identificados | Estados e historial sistematizados del requerimiento y de la postulación (quién, cuándo y de qué estado a cuál), con transiciones controladas. | RF-02, RF-03, RF-13, RF-14, RF-24, RF-25 |
| P3 | S-03 Evaluación uniforme y comparable | Criterios con ponderación y rango definidos antes de publicar; puntajes validados; ranking ponderado explicable y comparación común. | RF-05, RF-16, RF-17, RF-18, RF-19, RF-20, RF-21, RF-22 |
| P4 | S-04 Comunicación oportuna y con constancia | Notificaciones automáticas en cada evento clave: rechazo, recepción, cambio de etapa, convocatoria y resultado. No incluyen datos confidenciales. | RF-04, RF-11, RF-15, RF-17, RF-26 |
| P5 | S-05 Sustento y trazabilidad de la decisión (parcial) | Comparación explicable como apoyo a la decisión humana y auditoría de solo inserción consultable por Dirección. **Límite:** los indicadores agregados de RF-28 se implementaron y probaron en la rama de Reportes. La base integrada conserva la comparación y la auditoría. | RF-21, RF-22, RF-23, RF-27 |

| Objetivo de mejora | Descripción | Problema |
|---|---|---|
| OM-01 | Centralizar la información de cada convocatoria en un único registro por organización. | P1 |
| OM-02 | Controlar el avance con estados, transiciones válidas e historial con autor y fecha. | P2 |
| OM-03 | Evaluar con criterios, ponderaciones y rangos comunes definidos antes de publicar. | P3 |
| OM-04 | Eliminar la dependencia de avisos manuales en los eventos clave del proceso. | P4 |
| OM-05 | Dar sustento y trazabilidad a la decisión final, que sigue siendo humana. | P5 |

## CAPÍTULO 4. ANÁLISIS DE REQUERIMIENTOS DEL SISTEMA

### 4.1. Identificación de Actores del Sistema

| ID | Actor | Rol en el sistema | Tipo |
|---|---|---|---|
| ACT-01 | Área solicitante | solicitante | Interno |
| ACT-02 | Recursos Humanos (RR. HH.) | rrhh | Interno |
| ACT-03 | Aprobador / Dirección | aprobador | Interno |
| ACT-04 | Postulante | postulante | Externo |
| ACT-05 | Evaluador | evaluador | Interno |

Además actúa el **Sistema** en las notificaciones automáticas (RF-04, RF-11, RF-15, RF-17 y RF-26). No hay rol de superadministración (fuera de alcance, OUT-03).

### 4.2. Requerimientos Funcionales

Línea base de 27 requerimientos funcionales (Formato 06), todos SOFTWARE IMPLEMENTADO y con prueba automatizada. RF-28 es candidato implementado en la rama de Reportes. RF-29 es candidato experimental integrado como opción. Ambos conservan su estado formal fuera de la línea base.

| RF | Requerimiento | Descripción | Actor |
|---|---|---|---|
| RF-01 | Registrar requerimiento de personal | El sistema debe permitir al área solicitante registrar un requerimiento de personal. | Área solicitante |
| RF-02 | Validar y corregir requerimiento | El sistema debe permitir enviar el requerimiento a RR. HH., que lo valida u observa, y al área corregir y reenviar lo observado. | Área solicitante (enviar, corregir y reenviar) · RR. HH. (validar u observar) |
| RF-03 | Registrar aprobación o rechazo del requerimiento | El sistema debe permitir al Aprobador / Dirección aprobar o rechazar un requerimiento validado, con motivo obligatorio si lo rechaza. | Aprobador / Dirección |
| RF-04 | Notificar rechazo del requerimiento | El sistema debe notificar automáticamente al área solicitante el rechazo de su requerimiento, con el motivo. | Sistema (destinatario: área solicitante) |
| RF-05 | Registrar perfil y criterios del puesto | El sistema debe permitir a RR. HH. crear una vacante desde un requerimiento aprobado y registrar su perfil y sus criterios ponderados. | RR. HH. |
| RF-06 | Configurar y validar vacante | El sistema debe permitir configurar la convocatoria y mostrar una lista de validación previa a la publicación. | RR. HH. (configura) · Sistema (valida) |
| RF-07 | Publicar vacante | El sistema debe publicar en el portal público de empleos las vacantes que cumplan la validación. | RR. HH. |
| RF-08 | Gestionar cuenta y acceso del postulante | El sistema debe permitir al postulante crear su cuenta e iniciar sesión. | Postulante |
| RF-09 | Gestionar perfil y CV del postulante | El sistema debe permitir al postulante completar su perfil y cargar su CV en PDF de forma privada. | Postulante |
| RF-10 | Registrar postulación | El sistema debe registrar una única postulación por postulante y vacante publicada y vigente. | Postulante |
| RF-11 | Confirmar postulación al postulante | El sistema debe confirmar cada postulación con un código de seguimiento y un aviso de recepción. | Sistema (destinatario: postulante) |
| RF-12 | Consultar y revisar postulaciones | El sistema debe listar las postulaciones de cada vacante y mostrar el expediente con datos, CV e historial. | RR. HH. (también consulta el Aprobador / Dirección) |
| RF-13 | Registrar preselección o descarte | El sistema debe permitir a RR. HH. preseleccionar o descartar una postulación. El descarte lleva un motivo interno. | RR. HH. |
| RF-14 | Gestionar cambio de etapa de la postulación | El sistema debe permitir a RR. HH. cambiar la etapa de una postulación según las transiciones permitidas, con historial. | RR. HH. |
| RF-15 | Notificar cambio de etapa al candidato | El sistema debe avisar al postulante de cada cambio de etapa, sin revelar observaciones internas. | Sistema (destinatario: postulante) |
| RF-16 | Programar evaluación | El sistema debe permitir a RR. HH. programar una evaluación con un evaluador de la organización. | RR. HH. |
| RF-17 | Generar convocatoria de evaluación | El sistema debe generar la convocatoria al postulante y el aviso de asignación al evaluador. | Sistema (destinatarios: postulante y evaluador) |
| RF-18 | Programar entrevista | El sistema debe permitir a RR. HH. programar una entrevista con un evaluador asignado y su convocatoria. | RR. HH. |
| RF-19 | Registrar entrevista y su resultado | El sistema debe permitir al evaluador asignado registrar, una sola vez, los puntajes, el resultado y las observaciones de su sesión. | Evaluador asignado |
| RF-20 | Validar rangos y ponderaciones | El sistema debe validar que las ponderaciones y los rangos de los criterios sean coherentes y que cada puntaje esté dentro de su rango. | Sistema (lo configura RR. HH.) |
| RF-21 | Calcular ranking configurable | El sistema debe calcular un ranking ponderado, determinista y explicable, sin seleccionar a ningún candidato. | Sistema |
| RF-22 | Presentar comparación de candidatos | El sistema debe presentar la comparación de candidatos con criterios, promedios, aportes, total y posición. | RR. HH. · Aprobador / Dirección |
| RF-23 | Registrar decisión final de selección | El sistema debe permitir al Aprobador / Dirección registrar la decisión final humana, con confirmación explícita y justificación. | Aprobador / Dirección |
| RF-24 | Registrar selección del candidato | El sistema debe permitir a RR. HH. aplicar la decisión final registrando la selección del candidato decidido. | RR. HH. |
| RF-25 | Cerrar vacante o convocatoria | El sistema debe permitir a RR. HH. cerrar la convocatoria después de registrar la selección. | RR. HH. |
| RF-26 | Notificar resultado y cierre al postulante | El sistema debe notificar a cada postulante su propio resultado al cerrar la convocatoria. | Sistema (destinatarios: postulantes) |
| RF-27 | Generar registro de auditoría | El sistema debe registrar de forma de solo inserción las acciones críticas y permitir al Aprobador / Dirección consultarlas. | Sistema (registro) · Aprobador / Dirección (consulta) |

### 4.3. Requerimientos no Funcionales

Diez RNF académicos (Formato 07), clasificados con ISO/IEC 25010 como marco de referencia. Estado: 5 verificados, 3 con evidencia parcial y 2 no verificados.

| RNF | Característica | Nombre | Criterio | Estado |
|---|---|---|---|---|
| RNF-01 | Seguridad | Seguridad y control de acceso | Toda ruta del personal exige sesión y rol (middleware `role` y Policies). Contraseñas con hash bcrypt. Límite de 5 intentos de inicio de sesión por minuto. Las pruebas de autorización por rol pasan sin fallos. | VERIFICADO |
| RNF-02 | Seguridad | Multitenencia y aislamiento | Los registros internos multiempresa se acotan con `organization_id` y los scopes pertinentes. Las Policies comparan rol y organización. Las pruebas cross-tenant pasan sin fallos. | VERIFICADO |
| RNF-03 | Seguridad (responsabilidad) | Trazabilidad y auditoría | Cada acción crítica deja un registro. La tabla `audit_logs` rechaza UPDATE y DELETE mediante un trigger. Los historiales de estado registran quién, cuándo y de qué estado a cuál. | VERIFICADO |
| RNF-04 | Seguridad (confidencialidad) | Privacidad | No se almacenan DNI, fecha de nacimiento ni atributos sensibles no requeridos. El CV se guarda en disco privado con nombre UUID y solo lo descargan los usuarios autorizados por la Policy. Las notificaciones no incluyen datos de otros candidatos. | VERIFICADO |
| RNF-05 | Usabilidad | Usabilidad | Interfaz en español; errores por campo; estados vacíos; navegación por rol; diseño adaptable de 320 a 1440 px; contraste AA en modo claro y oscuro; foco visible y enlace de salto. | EVIDENCIA PARCIAL |
| RNF-06 | Eficiencia de desempeño | Rendimiento | **Criterio propuesto:** fijar un entorno de referencia, medir una línea base de las operaciones críticas (listado de postulaciones, comparación, registro de decisión) y aprobar umbrales antes de cualquier aceptación productiva. **No hay umbral aprobado.** | NO VERIFICADO |
| RNF-07 | Fiabilidad | Disponibilidad y recuperabilidad | **Criterio propuesto:** procedimiento de respaldo y restauración de la base probado, y objetivos de disponibilidad aprobados. **No definidos.** | NO VERIFICADO |
| RNF-08 | Compatibilidad | Compatibilidad | **Criterio propuesto:** lista de navegadores y versiones aprobada, y pruebas en cada uno. **No hay matriz formal.** | EVIDENCIA PARCIAL |
| RNF-09 | Mantenibilidad | Mantenibilidad | Monolito modular por dominio: controlador delgado → Form Request → Policy → servicio → modelo, con máquinas de estado en enums. Suites automatizadas de regresión en CI: build, tsc y PHPUnit. | EVIDENCIA PARCIAL |
| RNF-10 | Seguridad (integridad) | Integridad de datos | Form Requests en cada operación; máquinas de estado que rechazan transiciones inválidas; validadores de ponderaciones y puntajes; restricciones CHECK, UNIQUE y FK; un solo seleccionado por vacante; los IDs no numéricos devuelven 404. | VERIFICADO |

### 4.4. Casos de Uso del Sistema

Veinte casos de uso (Formato 08), formalizados en PowerDesigner. La {{ref:casos}} ilustra los casos iniciales en el anexo A.1.

| CU | Caso de uso | Descripción | RF |
|---|---|---|---|
| CU-01 | Registrar requerimiento de personal | El área registra la necesidad de personal. | RF-01 |
| CU-02 | Validar y corregir requerimiento | RR. HH. valida u observa; el área corrige y reenvía. | RF-02 |
| CU-03 | Aprobar o rechazar requerimiento | La Dirección decide sobre el requerimiento validado; el rechazo se notifica. | RF-03, RF-04 |
| CU-04 | Registrar perfil y criterios del puesto | RR. HH. crea la vacante con perfil y criterios ponderados. | RF-05 |
| CU-05 | Configurar y validar vacante | RR. HH. configura la convocatoria; el sistema valida. | RF-06 |
| CU-06 | Publicar vacante | RR. HH. publica la vacante válida en el portal. | RF-07 |
| CU-07 | Gestionar cuenta y acceso | El postulante crea su cuenta e inicia sesión. | RF-08 |
| CU-08 | Gestionar perfil y CV | El postulante completa su perfil y carga su CV. | RF-09 |
| CU-09 | Registrar postulación | El postulante postula y recibe la confirmación. | RF-10, RF-11 |
| CU-10 | Consultar y revisar postulaciones | Revisa el listado por vacante y el expediente. | RF-12 |
| CU-11 | Registrar preselección o descarte | RR. HH. preselecciona o descarta con motivo interno. | RF-13 |
| CU-12 | Gestionar cambio de etapa | RR. HH. cambia la etapa; el postulante recibe el aviso. | RF-14, RF-15 |
| CU-13 | Programar evaluación | RR. HH. programa la evaluación; se envía la convocatoria. | RF-16, RF-17 |
| CU-14 | Programar entrevista | RR. HH. programa la entrevista; se envía la convocatoria. | RF-18 |
| CU-15 | Registrar resultados de evaluación y entrevista | El evaluador asignado registra puntajes y resultado. | RF-19 |
| CU-16 | Validar rangos y ponderaciones | Validación incluida por la configuración, el registro de resultados y el ranking. | RF-20 |
| CU-17 | Consultar ranking y comparación | Ranking y comparación explicables. No selecciona. | RF-21, RF-22 |
| CU-18 | Registrar decisión final humana | **Decisión humana** del Aprobador / Dirección, con confirmación explícita y justificación. El ranking no elige. | RF-23 |
| CU-19 | Registrar selección | RR. HH. aplica la decisión registrada. | RF-24 |
| CU-20 | Cerrar convocatoria y notificar resultado | RR. HH. cierra con selección; cada postulante recibe su resultado. | RF-25, RF-26 |

## CAPÍTULO 5. PLANIFICACIÓN DEL PROYECTO Y PLAN DE CALIDAD

### 5.1. Alcance del Proyecto

Alcance del Formato 09 (entregable final v1.1): ocho bloques incluidos y once exclusiones explícitas.

| Incluido | Bloque |
|---|---|
| IN-01 | Requerimientos |
| IN-02 | Vacantes |
| IN-03 | Cuenta y postulación |
| IN-04 | Seguimiento |
| IN-05 | Evaluación y entrevista |
| IN-06 | Comparación y ranking |
| IN-07 | Decisión y cierre |
| IN-08 | Auditoría |

| Excluido | Descripción |
|---|---|
| OUT-01, OUT-02 | Facturación SaaS, planes y suscripciones |
| OUT-03 | Superadministración comercial |
| OUT-04, OUT-05 | Selección automática por IA o ML e inferencia de personalidad o idoneidad |
| OUT-06, OUT-07 | Banco de talentos; dashboards e indicadores avanzados |
| OUT-08 a OUT-10 | Proveedores externos, infraestructura productiva en la nube, integraciones no especificadas |
| OUT-11 | Uso productivo o decisorio del riesgo operacional ML (RF-29) |

Reportes cubre indicadores operativos acotados y permanece fuera de main. Las pruebas visuales posteriores corresponden a ramas de presentación. La ayuda documental y el registro experimental de evidencias se integraron con bandera apagada en la base F37. G0 real sigue sin aprobación, ADR-005 permanece como propuesta, F35-SBX está cerrada y congelada y la integración formal EI-23 permanece bloqueada. El uso de datos reales queda fuera del corte.

### 5.2. Herramientas Tecnológicas del Proyecto

| Área | Herramienta |
|---|---|
| Backend | PHP 8.4, Laravel 13, Fortify, Inertia 3 |
| Frontend | React 19, TypeScript, Tailwind 4, Vite |
| Datos | PostgreSQL 17, Redis 7 |
| ML experimental | Python 3.12, scikit-learn, FastAPI (fuera de Compose) |
| Pruebas | PHPUnit, Cypress 15.3.0, Vitest, pytest |
| Entorno | Docker Desktop y Docker Compose |
| Versiones y CI | Git, GitHub y GitHub Actions |
| Modelado | PowerDesigner (BPMN, UML y modelo físico) |
| Asistencia | Claude (implementación asistida) y Codex (auditoría), bajo dirección del equipo |

La planificación registrada se apoya en iteraciones por flujo, TDD con ciclos RED y GREEN observados, revisión de cambios y entornos aislados. La [metodología complementaria](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/5e2eae37f63c7ac5d35ed2def9b2e843a644cd98/docs/metologia/investigacion-ia/METODOLOGIA_DESARROLLO_ASISTIDO_IA.md) compara el trabajo con AI-DLC y registra brechas de procedencia. La historia permite afirmar asistencia al desarrollo y separación entre implementación y revisión. La adopción formal de AI-DLC, el historial completo de prompts y un efecto causal de la IA sobre el esfuerzo quedan sin demostración.

### 5.3. Normas y Estándares de Calidad

ISO/IEC 25010 se usa como **marco de referencia** para clasificar los RNF y organizar la evaluación de calidad (capítulo 13). No se declara certificación ni conformidad con la norma.

- Estándares de práctica: TDD, integración continua, revisión independiente de cada fase y registro de defectos con prueba de regresión.
- Accesibilidad: criterios WCAG 2.2 revisados en la Fase 21 (contraste AA, reflow y foco visible), sin auditoría formal externa.
- Datos: solo ficticios; ninguna información personal real.

### 5.4. Plan de Pruebas del Proyecto

El plan formal está en el Plan de Pruebas de Software (F29D, docs/academico/plan-pruebas/), sobre la plantilla del curso. Define alcance, estrategia en niveles, criterios de aceptación CA-01 a CA-07, suspensión y reanudación, recursos, RACI, cronograma y riesgos. El plan se conserva como evidencia académica de F29D. La aprobación y las firmas requieren confirmación documental del curso.

| Criterio | Descripción |
|---|---|
| CA-01 | PHPUnit sin fallos; solo las 8 omitidas del starter kit |
| CA-02 | Cypress 20 specs sin fallos ni reintentos |
| CA-03 | Vitest y pytest sin fallos |
| CA-04 | TypeScript y build sin errores |
| CA-05 | CI en verde en develop |
| CA-06 | Cada RF-01 a RF-27 con un caso automatizado aprobado |
| CA-07 | Ningún defecto Alto abierto |

### 5.5. Lineamientos de Seguridad Informática

- Autenticación con Fortify; contraseñas con hash; límite de intentos de inicio de sesión (RNF-01).
- Autorización en el servidor con Policies que comparan rol **y** organización; middleware de rol.
- Aislamiento multiempresa por `organization_id` con scope global y pruebas de acceso cruzado (RNF-02).
- Auditoría de solo inserción: la tabla `audit_logs` rechaza UPDATE y DELETE con un trigger (RNF-03).
- Privacidad: perfil mínimo del postulante y CV en almacenamiento privado (RNF-04).
- Endpoints de soporte E2E inertes fuera del entorno aislado y protegidos por token (DEF-13).
- Secretos fuera de Git (`.env`, `.env.e2e`); Postgres y Redis publicados solo en 127.0.0.1.
- Límites: sin pruebas de penetración ni análisis dinámico (OWASP ZAP); RLS de PostgreSQL no implementado.

## CAPÍTULO 6. DISEÑO DEL SISTEMA

### 6.1. Arquitectura Conceptual del Sistema

**Arquitectura del proyecto grupal.** Un monolito modular Laravel concentra las reglas, la autorización y la persistencia. React y TypeScript se ejecutan en el navegador. Inertia enlaza rutas del servidor, páginas y propiedades. Los controladores coordinan las acciones, los Form Requests validan entradas y las Policies aplican permisos. Servicios y transacciones mantienen las invariantes. La {{ref:arquitectura}} muestra esas dependencias y los cinco roles.

PostgreSQL es el registro de negocio y auditoría. Redis mantiene sesiones, caché y trabajos. El worker consume la cola y procesa avisos. Los CV se guardan en almacenamiento privado y se entregan mediante una ruta autorizada. FastAPI se ejecuta aparte para ML-01. En la rama académica, Reportes consulta agregados en el mismo monolito, como muestra la {{ref:reportes-arq}}.

{{fig:arquitectura}}

Correspondencia. [Configuración Compose](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docker-compose.yml) · [Rutas](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/routes/web.php) · [Policies](https://github.com/luivmz/saas-reclutamiento-multiempresa/tree/04d3cfa1db6f82d9cda8db2254338805137cdc3c/app/Policies) · [UML de componentes](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/v1.1/uml/component-model.md).

### 6.2. Modelo UML del Sistema

El AS-IS del software se modeló en F22 y se formalizó en PowerDesigner en F23. Incluye clases, enumeraciones, componentes, paquetes, despliegue, secuencias, estados y actividades. Los carriles del proceso institucional son otra vista y conservan las etiquetas AS-IS preliminar y TO-BE propuesto. En la {{ref:secuencia}}, la acción de Dirección pasa por autorización y validación, y el servicio persiste la decisión y su auditoría. La notación refleja el corte histórico F23. Los endurecimientos se desarrollan en §8.4 y §13.2.

{{fig:secuencia}}

### 6.3. Diseño de Interfaces de Usuario

React e Inertia ofrecen navegación por rol, errores de campo, modo claro y oscuro, foco, enlace de salto y tablas adaptadas. El portal muestra la convocatoria, perfil, criterios y acciones. En la {{ref:comparacion}} el panel explica la fórmula y aclara la responsabilidad de Dirección.

{{fig:comparacion}}

La continuación visual sitúa el vídeo del colegio en la portada y la carpeta decorativa en el detalle de empleo. Ambos responden al desplazamiento y tienen respaldo estático en móvil, con movimiento reducido o si falla el recurso. La capa de vídeo del empleo tiene 20 % de opacidad. Textos y controles conservan sus superficies. La portada se documenta en la {{ref:portada}} y el detalle en la {{ref:oferta}}.

El anfitrión de /empleos usa gestos pregrabados según la posición de una tarjeta, el cursor y el foco. La {{ref:anfitrion}} muestra un gesto de señalamiento. El listado, la búsqueda y la postulación son independientes del personaje. Según el dispositivo y la preferencia, se sustituye por un póster o se omite.

### 6.4. Diseño de Base de Datos

PostgreSQL conserva la cadena requerimiento → vacante → postulación → evaluación → decisión. La pertenencia a la organización se comprueba en los módulos internos. El postulante se registra en el portal y accede a sus propias postulaciones. Se aplican claves foráneas, CHECK y unicidad. Un trigger impide UPDATE y DELETE en auditoría. La {{ref:datos}} reproduce el modelo F23. La migración de noviembre añade evidencias y eventos experimentales posteriores a ese modelo.

| Relación | Función y restricción |
|---|---|
| Requerimiento y vacante | La vacante parte del requerimiento aprobado. Perfil y criterios anteceden a la publicación. |
| Vacante, postulación y candidato | La combinación de vacante y candidato es única. |
| Sesión y resultados | El evaluador asignado registra puntajes dentro de los rangos. Solo se permite un registro por sesión. |
| Vacante y decisión | La decisión se asocia a la vacante y a la postulación elegida. El cierre aplica la decisión autorizada. |
| Auditoría y evidencias | Auditoría de solo inserción. La extensión experimental conserva versiones y eventos con su procedencia. |

## CAPÍTULO 7. ARQUITECTURA TECNOLÓGICA DEL SISTEMA

### 7.1. Tecnologías del Frontend

| Tecnología | Uso |
|---|---|
| React 19 + TypeScript | Páginas y componentes |
| Inertia 3 | Puente SPA con Laravel, sin API separada |
| Tailwind 4 (componentes shadcn/ui) | Estilos y sistema de diseño |
| Vite (vite-plus `vp`) | Empaquetado, pruebas de componentes y formato |
| Laravel Wayfinder | Rutas tipadas |

### 7.2. Tecnologías del Backend

| Tecnología | Uso |
|---|---|
| PHP 8.4 + Laravel 13 | Aplicación y reglas de negocio (monolito modular) |
| Fortify | Autenticación |
| Policies y Form Requests | Autorización y validación en el servidor |
| Colas con Redis | Notificaciones asíncronas enviadas tras confirmar la transacción |
| Servicio ML (FastAPI) | RF-29 EXPERIMENTAL, llamado solo si `ML_SERVICE_ENABLED=true` |

**ML-01.** La regresión logística congelada (C = 10, StandardScaler, sin calibración) estima el riesgo de demora de una vacante elegible con variables operacionales. El artefacto se reconstruye localmente desde el freeze. Con servicio, artefacto y configuración disponibles Laravel presenta la estimación. En su ausencia queda el modo descriptivo. La {{ref:riesgo}} muestra ese panel en contexto. Durante el trabajo editorial el puerto local 8008 no aceptó conexión a FastAPI. La Fase 17 documentó una respuesta real en un escenario elegible (score 0,4411) y los modos de respaldo. Véanse la [ficha del modelo](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/v1.1/ml/model-card-draft.md) y la [validación de la integración](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/v1.1/phase-17-ml-validation.md).

### 7.3. Base de Datos del Sistema

- PostgreSQL 17 con tres bases: `reclutamiento` (desarrollo y demostración), `reclutamiento_testing` (PHPUnit) y `reclutamiento_e2e` (Cypress). Las pruebas nunca tocan la de demostración.
- Redis 7 para sesiones, caché y colas; el entorno E2E usa sus propias bases de Redis.
- Datos de demostración ficticios generados por `DemoSeeder` (docs/demo-users.md).

### 7.4. Infraestructura de Desarrollo

La aplicación y sus dependencias base corren en Docker Compose con versiones fijadas; no se usan PHP ni Node del equipo host. Servicios: `app`, `queue`, `postgres`, `redis` y, en el perfil e2e, `app-e2e`, `queue-e2e` y `cypress`. El servicio ML corre fuera de Compose, en su entorno virtual. La integración continua usa GitHub Actions.

## CAPÍTULO 8. DESARROLLO DEL SISTEMA

### 8.1. Iteración 1: Configuración Inicial del Proyecto

- Repositorio Git con `main` y `develop`; bootstrap de Laravel (`e87ef39`).
- Frontend React + Inertia + TypeScript y backend Laravel desde el kit inicial.
- PostgreSQL y Redis en Docker; autenticación, organizaciones, roles y aislamiento multiempresa (`feature/tenancy-roles`, merge `d696032`).
- Defectos DEF-01 y DEF-02 (entorno Docker y variables de PHPUnit), corregidos en esta iteración.

### 8.2. Iteración 2: Desarrollo de Funcionalidades Básicas

- Requerimientos de personal y vacantes: RF-01 a RF-07 (merge `5ab6e22`), con máquinas de estado y validación de ponderaciones.
- Primeras páginas Inertia conectadas a controladores delgados que delegan en servicios.
- Ciclos TDD registrados en docs/tdd-evidence.md.

### 8.3. Iteración 3: Implementación de Módulos Funcionales

- Postulantes y postulaciones: RF-08 a RF-15 (merge `f20f0b6`).
- Evaluaciones y entrevistas: RF-16 a RF-19 (merge `40eda7d`), con checkpoint RED previo (`3e66623`).
- Ranking, decisión humana, selección y cierre: RF-20 a RF-25 (merge `dda4bd0`).
- Notificaciones y auditoría: RF-26 y RF-27 (merge `cd092d1`). Formularios, validaciones y operaciones CRUD con autorización por rol y organización.

### 8.4. Iteraciones Posteriores

En la base integrada se añadieron el pulido visual de v1.1, controles del expediente y las descargas privadas, la serialización entre decisión y cambios de etapa y la reducción del texto libre en auditoría. La presentación F37 integró la portada con roles, cronograma y escenario de riesgo. La [guía de presentación](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/presentacion/README.md) registra los incrementos y su bandera experimental.

**Evidencias y ayuda documental.** La extensión conserva las versiones y su historial. La ayuda recupera hasta tres fragmentos vigentes en una postulación mediante coincidencias léxicas BM25 (Robertson y Zaragoza, 2009). La lectura de Recall@3 sigue el enfoque de evaluación de recuperación documental descrito por Manning et al. (2008). Conserva la fuente declarada, enlaza a la evidencia y se abstiene cuando faltan coincidencias. La {{ref:evidencias}} muestra el resultado de una consulta de demostración. El método prescinde de entrenamiento y queda separado del ranking. Con 12 fragmentos y una vacante por partición, Recall@3 fue 0,5 en dev y 0,0 en test, igual a la línea base. H2 fue rechazada. Hubo una abstención falsa en dev y dos en test. En los casos anotados sin evidencia, ambas particiones obtuvieron la abstención esperada. El intervalo fue no informativo. [Preregistro](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/academico/preparacion-f38-ml02/preregistro/PREREGISTRO_EXP-BM25-LEXICO-v1.md) · [Resultados](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/academico/preparacion-f38-ml02/resultados-exp-bm25-v1/RESULTADOS.md)

**Reportes.** La práctica RF-28 en [5e2eae3](https://github.com/luivmz/saas-reclutamiento-multiempresa/commit/5e2eae37f63c7ac5d35ed2def9b2e843a644cd98) incorpora /reportes para RR. HH. y Dirección, con filtros de fechas, vacante y etapa actual. Muestra postulaciones recibidas, vacantes publicadas, promedio por vacante con postulaciones, llegada a preselección y tasa, casos en evaluación o entrevista y tiempo a preselección. Las postulaciones se filtran por applied_at. El indicador de publicación usa published_at y su cálculo es independiente del filtro de etapa. La Policy, el Form Request y el filtro explícito por organization_id acotan la consulta. Los gráficos y la tabla muestran agregados. La {{ref:reportes}} documenta un filtro en el entorno ficticio. [Módulo y definiciones de indicadores](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/5e2eae37f63c7ac5d35ed2def9b2e843a644cd98/docs/architecture-cypress-reports/reportes/MODULO_REPORTES.md)

**Presentación posterior.** La rama del anfitrión desciende de la de los dos vídeos. El último commit agrega un seeder para diez ofertas ficticias. El corte de pruebas del anfitrión corresponde a b1dd8cb, anterior a ese seeder. Los vídeos y el anfitrión son recursos de interfaz. La decisión operativa continúa a cargo de Dirección.

## CAPÍTULO 9. CONTROL DE VERSIONES Y GESTIÓN DEL REPOSITORIO

### 9.1. Repositorio del Proyecto

GitHub aloja el repositorio del proyecto grupal, con su historia, fuentes, modelos y versiones académicas. [Repositorio SaaS Reclutamiento Multiempresa](https://github.com/luivmz/saas-reclutamiento-multiempresa)

[Release académica v1.1](https://github.com/luivmz/saas-reclutamiento-multiempresa/releases/tag/v1.1.0-academic) · [Trazabilidad RF y evidencia](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/final-report/traceability-master.md) · [Guía de presentación](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/presentacion/README.md) · [Evidencia histórica de Reportes, Cypress y SonarQube](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/5e2eae37f63c7ac5d35ed2def9b2e843a644cd98/docs/architecture-cypress-reports/README.md).

### 9.2. Estrategia de Control de Versiones

- Git Flow simplificado: `main` estable, `develop` de integración y ramas `feature/*` por fase.
- Cada fase se integra con `git merge --no-ff` tras su auditoría y con la CI en verde.
- Commits convencionales (`feat`, `test`, `docs`, `chore`) y checkpoints TDD (RED) como commits propios.
- Nunca `push --force`, rebase de historia publicada ni etiquetas movidas.

### 9.3. Gestión de Ramas del Proyecto

Se consultaron las referencias mediante fetch normal. Se cotejó el árbol de main y develop y la presencia, por ruta y por ascendencia, de las continuaciones.

| Referencia | SHA de corte | Estado del contenido |
|---|---|---|
| main / origin/main | [04d3cfa](https://github.com/luivmz/saas-reclutamiento-multiempresa/commit/04d3cfa1db6f82d9cda8db2254338805137cdc3c) | Base de presentación F37. Evidencias y BM25 detrás de la bandera experimental. |
| develop / origin/develop | [4371d90](https://github.com/luivmz/saas-reclutamiento-multiempresa/commit/4371d90e6fb9682fe8076c978f33a3ce5f086b49) | Árbol 74f1d82c2bf6, idéntico al de main. Base documental. |
| origin/chore/sonarqube-macos-setup | [5e2eae3](https://github.com/luivmz/saas-reclutamiento-multiempresa/commit/5e2eae37f63c7ac5d35ed2def9b2e843a644cd98) | Reportes, diagramas Draw.io, práctica de arquitectura, Cypress y SonarQube. Rama publicada, fuera de main. |
| feature/presentacion-dos-videos | 2b87f3667dce | Vídeos de portada y detalle. Candidato local. |
| design/anfitrion-empleos | f9703f4636d7 | Hereda los vídeos e incorpora el anfitrión y un seeder de ofertas de demostración. Candidato local. |
| design/presentacion-astra | c1b842a70388 | Antecedente de la escena de proceso tras la portada. |
| design/presentacion-higgsfield | b8f42b581456 | Antecedente del primer vídeo y las correcciones VIS-L01 y DEF-19. |

El registro de fuentes incluye los SHA completos. Reportes y la presentación posterior se documentan como dos demostraciones diferentes. Una futura integración conjunta requiere revisar los conflictos de rutas, progreso, defectos y TDD que registró la simulación previa. Las fuentes de la evidencia se conservan en sus ramas.

### 9.4. Registro de Commits Relevantes

| Revisión | Aporte |
|---|---|
| 9a946c2 | Línea histórica v1.0 académica. |
| 634f354 | Cierre técnico de v1.1. |
| bc44303 | Evidencia QA del informe F29H v1. |
| bb86991 | Código del candidato de presentación integrado en main. |
| 41a830c + cambios locales | Base de ejecución de Reportes y Sonar V3 el 09/11. |
| [5e2eae3](https://github.com/luivmz/saas-reclutamiento-multiempresa/commit/5e2eae37f63c7ac5d35ed2def9b2e843a644cd98) | Publicación de la práctica y sus evidencias históricas en Git. |
| 446b8fe · 2b87f36 · b1dd8cb | Corrección de IntersectionObserver, ubicación de los vídeos y anfitrión. |
| f9703f4 | Diez ofertas ficticias adicionales en la rama local del anfitrión. |

## CAPÍTULO 10. DOCKERIZACIÓN Y DESPLIEGUE DE MÓDULOS

### 10.1. Introducción a Docker en el Proyecto

Docker Compose permite levantar el sistema completo con un solo comando (`docker compose up -d --wait`) y garantiza que las pruebas y la demostración usen las mismas versiones. Todas las imágenes están fijadas.

### 10.2. Dockerización del Backend

Imagen `reclutamiento-php:dev` (PHP 8.4.25 con Composer y Node). El contenedor `app` instala dependencias si faltan, compila los assets, migra y sirve la aplicación; `queue` procesa las notificaciones. Su healthcheck `GET /health` verifica la base de datos y Redis.

### 10.3. Dockerización del Frontend

El frontend no tiene contenedor propio: Vite compila los assets dentro de la imagen de la aplicación (`npm run build`) y Laravel los sirve con Inertia. TypeScript, Vitest y el build se ejecutan en el mismo contenedor.

### 10.4. Orquestación con Docker Compose

| Servicio | Imagen | Función |
|---|---|---|
| app | reclutamiento-php:dev | Aplicación (healthcheck /health) |
| queue | reclutamiento-php:dev | Worker de notificaciones |
| postgres | postgres:17.11-alpine | Bases de desarrollo, pruebas y E2E |
| redis | redis:7.4.11-alpine | Sesiones, caché y colas |
| app-e2e, queue-e2e | reclutamiento-php:dev | Entorno aislado para Cypress (perfil e2e) |
| cypress | cypress/included:15.3.0 | Suite E2E |



La {{ref:despliegue}} muestra la configuración local de la práctica en macOS. Los servicios base corresponden a Compose. SonarQube se ejecutó fuera de Compose, con H2 de evaluación. FastAPI se arranca aparte para ML-01.

{{fig:despliegue}}

## CAPÍTULO 11. ESTRATEGIA DE PRUEBAS DE SOFTWARE

### 11.1. Enfoque de Pruebas del Proyecto

Enfoque guiado por pruebas: cada regla se especifica primero como una prueba que falla y la automatización tiene prioridad sobre la prueba manual. La estrategia completa está en el Plan de Pruebas (F29D). Los datos son siempre ficticios y las bases de prueba están aisladas de la de demostración.

### 11.2. Niveles de Pruebas Aplicados

| Nivel | Herramienta | Alcance |
|---|---|---|
| Unitario | PHPUnit (tests/Unit) | Estados, validadores y servicio de ranking |
| Integración / funcional | PHPUnit (tests/Feature) sobre PostgreSQL real | RF-01 a RF-27, autorización, notificaciones, auditoría |
| Sistema (E2E) | Cypress 15.3.0 | Flujos por rol y flujo completo en navegador |
| Componentes | Vitest | Componentes de interfaz y accesibilidad |
| Aceptación | Flujo E2E-13 y recorrido manual (Fase 8) | Sin aceptación institucional |

### 11.3. Tipos de Pruebas Ejecutadas

Distribución de los 128 casos de prueba de la F29E por tipo (el detalle está en docs/academico/casos-prueba/):

| Tipo de prueba | Casos |
|---|---|
| Aceptación (flujo completo) | 1 |
| Aceptación (manual) | 2 |
| Estática / build | 3 |
| Integración / funcional | 42 |
| ML experimental | 28 |
| Multitenencia | 4 |
| No funcional | 2 |
| Regresión | 4 |
| Regresión / CI | 1 |
| Seguridad básica | 15 |
| UI / E2E | 10 |
| UI / E2E (accesibilidad) | 4 |
| UI / componentes | 6 |
| Unitaria | 6 |

| Regla verificada | Caso dirigido y evidencia |
|---|---|
| RF-10, postulación única | La regresión de postulación cubre duplicados, precondiciones y vigencia. El flujo completo E2E-13 enlaza publicación, postulación y cierre. |
| RF-21 y RF-23, comparación y decisión | Las unitarias de RankingService verifican rangos, incompletos y empates. El recorrido de demostración comprueba fórmula, confirmación de Dirección y auditoría. |
| RNF-02, límites entre organizaciones | Las pruebas de acceso al expediente y las descargas verifican rol y pertenencia. En el corte experimental, el historial devuelve 403 a un rol sin permiso y 404 fuera de la organización. |
| RF-28 candidato, filtro y agregación | RecruitmentReportTest rechaza una vacante ajena, conserva datos de la organización y comprueba que las propiedades no incluyen datos personales. Cypress verifica ambos contextos y un cambio real de etapa reflejado en el KPI. |

Referencias de ejecución. [Matriz de trazabilidad](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/final-report/traceability-master.md) · [Cypress de la aplicación](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/testing/cypress-e2e.md) · [Pruebas de Reportes](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/5e2eae37f63c7ac5d35ed2def9b2e843a644cd98/docs/architecture-cypress-reports/reportes/MODULO_REPORTES.md).

### 11.4. Plan de Ejecución de Pruebas

Orden de ejecución de cierre (F29F), con el árbol de trabajo limpio y la salida completa de cada herramienta guardada como evidencia: configuración de Compose → PHPUnit → TypeScript → build → Vitest → pytest → Cypress. Cualquier fallo se clasifica (regresión real, flaky, ambiente, dependencia externa, documental o no aplicable) y nunca se oculta; el runtime no se corrige sin autorización del equipo.

El calendario histórico de F29D ubica los hitos de autorización, flujo completo, validación ML y QA visual por fecha de integración. El equipo define el alcance, revisa resultados y responde por la entrega. La matriz RACI del plan asigna implementación y revisión y deja la conformidad académica en el ámbito del curso. Los hitos de noviembre se identifican por fecha y herramienta en §13.1. [Plan F29D, roles y cronograma](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/academico/plan-pruebas/F29D_Plan_de_Pruebas_Colegio_Andino.md)

## CAPÍTULO 12. AUTOMATIZACIÓN DE PRUEBAS

### 12.1. Herramientas de Automatización

| Herramienta | Suite | Archivos de prueba en main |
|---|---|---|
| PHPUnit 12 | Unitarias e integración | 7 unitarios, 53 de integración |
| Cypress 15.3.0 | E2E | 23 specs |
| Vitest (vp test) | Componentes | 9 archivos |
| pytest | Servicio ML experimental | 18 archivos |
| GitHub Actions | Integración continua | .github/workflows/tests.yml |

### 12.2. Configuración del Entorno de Pruebas

- PHPUnit fuerza `DB_DATABASE=reclutamiento_testing` en phpunit.xml (DEF-02) y usa RefreshDatabase.
- Cypress corre en su imagen oficial contra `app-e2e`, con `.env.e2e` generado por `npm run e2e:setup` (token y clave aleatorios, nunca versionados) y reset por endpoint protegido.
- Sin reintentos en Cypress (`retries: 0`): un fallo intermitente se investiga.
- El servicio ML se prueba en su entorno virtual con dataset sintético y contrato congelado.

### 12.3. Scripts de Pruebas Automatizadas

Las pruebas viven con el código: `tests/Unit`, `tests/Feature`, `cypress/e2e`, `resources/js/**/*.test.tsx` y `ml-service/tests`. Los nombres `test_rfNN_*` enlazan cada prueba con su RF, y la matriz de trazabilidad (F29E) enlaza RF → CU → caso de prueba → prueba automatizada → evidencia.

Dos ejemplos trazables. [FinalDecisionTest](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/tests/Feature/Selection/FinalDecisionTest.php) prepara una vacante y una postulación elegible, envía la acción de Dirección y comprueba persistencia y restricciones. [E2E-09](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/cypress/e2e/e2e-09-human-final-decision.cy.js) abre la comparación, recorre el control de decisión y valida el resultado visible. [E2E-11](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/cypress/e2e/e2e-11-multitenancy.cy.js) usa los escenarios de organizaciones separadas para verificar el alcance de lectura.

### 12.4. Ejecución Automática de Pruebas

GitHub Actions automatiza instalación, build, TypeScript y PHPUnit en push y pull request hacia las ramas configuradas, y por ejecución manual. Cypress, Vitest y pytest tienen evidencias independientes. La consulta por SHA devolvió dos ejecuciones completadas con estado success el 22/11/2026.

| Rama | Commit | Resultado |
|---|---|---|
| main | 04d3cfa | [CI del corte integrado](https://github.com/luivmz/saas-reclutamiento-multiempresa/actions/runs/45080426261) · success |
| develop | 4371d90 | [CI de la base documental](https://github.com/luivmz/saas-reclutamiento-multiempresa/actions/runs/45079940215) · success |

El estado de CI pendiente del corte F29F se conserva como antecedente en la v1. En este corte el workflow se revisó en el archivo [tests.yml](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/.github/workflows/tests.yml).

## CAPÍTULO 13. MÉTRICAS DE CALIDAD

### 13.1. Ejecución de Casos de Pruebas

La matriz distingue cada ejecución por revisión. Esta edición verificó las fuentes y el estado de las referencias y reutilizó los resultados fechados. Las repeticiones quedan en sus propios cortes.

| Tipo | Alcance | Revisión | Fecha | Resultado | Evidencia |
|---|---|---|---|---|---|
| Regresión F29F | PHPUnit, Cypress, Vitest, pytest y compilación | bc44303 | 30/09/26 | 411 aprobadas y 8 omitidas. E2E 85/85. Componentes 42/42. Python 533/533. | [QA F29F](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/academico/qa-final/README.md) |
| Feature y cobertura | Backend Reportes, regresión, PCOV/Clover | 41a830c + cambios | 09/11/26 | Reportes 12/12. Suite 426 aprobadas, 8 omitidas, 1.715 aserciones. | [Auditoría y logs](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/5e2eae37f63c7ac5d35ed2def9b2e843a644cd98/docs/architecture-cypress-reports/AUDITORIA_CODEX.md) |
| Componentes y E2E | Reportes y regresión global | 41a830c + cambios | 09/11/26 | Vitest 54/54 (6 del módulo). Cypress 94/94 en 21 specs (9 casos de Reportes). | [Resultados Cypress](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/5e2eae37f63c7ac5d35ed2def9b2e843a644cd98/docs/architecture-cypress-reports/cypress/RESULTADOS_CYPRESS.md) |
| Análisis estático | Sonar V3, revisión independiente | 41a830c + cambios | 09/11/26 | Scanner y procesamiento exitosos. Gate evaluado. Véase §13.3. | [API final](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/5e2eae37f63c7ac5d35ed2def9b2e843a644cd98/docs/architecture-cypress-reports/evidencias/codex/sonar-final.json) |
| Recuperación léxica | BM25 y coincidencia base en dev y test | e3f80a1 | 10/11/26 | Recall@3 0,5 y 0,0. H2 rechazada. Abstención en §8.4. | [Resultados BM25](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/academico/preparacion-f38-ml02/resultados-exp-bm25-v1/RESULTADOS.md) |
| Regresión integrada | Código de la base de presentación | bb86991 | 22/11/26 | PHPUnit 525 aprobadas y 8 omitidas, 2.746 aserciones. Cypress 114/114 en 23 specs. Componentes 65/65. | [Guía, §6](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/presentacion/README.md) |
| Acceso y función | Bandera de evidencias activa e inactiva | bb86991 | 22/11/26 | 14/14 activa, incluidos 403 y 404. 7/7 inactiva. | [Verificación de la bandera](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/presentacion/README.md) |
| UI y E2E | Portada, dos ofertas, teclado, tema y respaldo | 2b87f36 | 22/11/26 | Componentes 81/81. E2E-18/22/23 29/29. Tipos, lint y build correctos. | Registro local de dos vídeos; anexo A.3 |
| UI y E2E | Anfitrión, foco, cursor, restauración y póster | b1dd8cb | 22/11/26 | Componentes 89/89. E2E-24 16/16, repetida tres veces. Seis specs existentes 39/39. | Registro local del anfitrión; anexo A.3 |

La {{ref:cypress}} conserva el resumen de una ejecución de Reportes. La reauditoría confirmó el mismo total. Un intento de PHPUnit concurrente con el build falló por CSS ausente del manifiesto. La repetición en serie dio 426 aprobadas y 8 omitidas. En un corte intermedio de F37, E2E-10 falló y pasó al repetirla. Se registró un desfase de reloj, sin evidencia de que causara el fallo.

### 13.2. Registro de Defectos

| Defecto o hallazgo | Severidad registrada | Corrección y regresión | Corte |
|---|---|---|---|
| DEF-14 a DEF-17 | Alta (14–16), media (17) | Controles del expediente y CV, bloqueo de decisión y etapas, auditoría sin texto libre. Pruebas de rol, otra organización y concurrencia. | Base integrada F37 |
| DEF-18 | Baja | DemoSeeder añade un escenario elegible para el riesgo operacional. | Base integrada F37 |
| APP-M01 | Media | Las escrituras experimentales comprueban el cierre bajo bloqueo. Los 12 casos de concurrencia fallaron sin el arreglo y pasaron al aplicarlo. | fd87b78 |
| APP-M02 | Media | La ayuda conserva el componente y el foco en consultas sucesivas. Cypress también verifica fallo HTTP 500, fallo de red y recuperación. | 153a523 |
| VIS-L01 y DEF-19 | Baja | Reveal muestra bloques pendientes al activar movimiento reducido. IntersectionObserver procesa el lote completo. | d67aa9d y 446b8fe, ramas visuales |
| AUD-01 / AUD-10 | Media / informativa | Reportes corrigió 14 errores PHPStan nuevos mediante PHPDoc. El fallo de assets concurrente se conservó y la repetición secuencial pasó. | Reportes, 09/11 |

DEF-14 y DEF-15 en la práctica Sonar tienen su propia cronología. Se citan por rama al consultar la [auditoría de Reportes](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/5e2eae37f63c7ac5d35ed2def9b2e843a644cd98/docs/architecture-cypress-reports/AUDITORIA_CODEX.md). El histórico F29F permanece en la v1 y el [registro de defectos](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/defects.md).

### 13.3. Métricas de Calidad del Software

F29F documentó cobertura funcional de 27/27 RF y 20/20 CU a través de sus requisitos, con 124 de 128 casos automatizados. Sonar registra instrumentación de código y usa otros denominadores. Las cifras siguientes son de la práctica del 09/11/26 sobre 41a830c con cambios locales, publicada después en [5e2eae3](https://github.com/luivmz/saas-reclutamiento-multiempresa/commit/5e2eae37f63c7ac5d35ed2def9b2e843a644cd98).

| Métrica Sonar V3 | Resultado | Interpretación |
|---|---|---|
| Quality Gate Sonar way | OK, condiciones evaluadas | Cobertura nueva 85,0 % (187/220), duplicación nueva 0,0 %, incidencias nuevas 0. |
| Cobertura global | 70,3 % | 4.407 líneas elegibles, 1.311 sin cubrir. |
| Backend app/ | 90,1 % | 3.436 líneas elegibles, 340 sin cubrir. Clover mide 2.666 de 2.945 sentencias. |
| Frontend resources/js/ | 0,0 % en Sonar | 913 líneas sin reporte LCOV importado. Vitest y Cypress ejecutaron frontend. |
| Rutas | 0,0 % | 58 líneas sin instrumentación de Clover. |
| Issues y duplicados | 0 issues abiertos y 0,0 % de duplicación | Resultado acotado a las fuentes y reglas del analizador. |

La {{ref:sonar}} muestra las condiciones del Gate V3. V1 y V2 se midieron el 20/10. En V2 el Gate fue OK por Small Changes, con cobertura nueva de 50,0 % e ignoredConditions=true. El 85,0 % corresponde a V3. Persistían 91 errores históricos de PHPStan, 8 archivos observados por Pint y deuda de formato global. Oxlint registró 5 advertencias y salió con código 1 por política. Community Build tiene alcance limitado de seguridad y H2 se usó para evaluación. [Análisis completo](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/5e2eae37f63c7ac5d35ed2def9b2e843a644cd98/docs/architecture-cypress-reports/sonarqube/RESULTADOS_SONARQUBE.md)

{{fig:sonar}}

### 13.4. Evaluación de Calidad basada en Estándares

Evaluación organizada con ISO/IEC 25010, sin certificación: seguridad (confidencialidad, integridad y responsabilidad) verificada por RNF-01 a RNF-04 y RNF-10; usabilidad, compatibilidad y mantenibilidad con evidencia parcial; eficiencia de desempeño y fiabilidad no verificadas. Detalle en docs/academico/metricas-calidad/.

Sobre 830 observaciones sintéticas de test, ML-01 obtuvo Average Precision de 0,769082 frente a 0,3807 de la línea trivial y 0,4252 de la operacional. Con el umbral congelado 0,1679418172266036, la precisión fue 0,483607 y el recall 0,933544. La tasa de alerta fue 0,734940. La AP por organización sintética osciló entre 0,476 y 0,840. La carga de alertas, la heterogeneidad y el carácter sintético limitan su uso fuera del experimento. El desempeño y la abstención de ML-02 constan en §8.4.

## CAPÍTULO 14. IMPLEMENTACIÓN Y MONITOREO

### 14.1. Preparación del Entorno de Implementación

La demostración requiere Docker Desktop o Docker Engine con Compose. Las variables y los volúmenes se aíslan por proyecto. La base estándar se documenta en el puerto 8000. Los worktrees de presentación usaron 8030 y 8040. Son direcciones locales. Los registros de las dos organizaciones de demostración son ficticios. [Guía Docker](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/docker.md) · [Escenarios de datos demo](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/demo-users.md)

### 14.2. Implementación del Sistema

Para reproducir, obtener la revisión, preparar la configuración local a partir del ejemplo, arrancar Compose y verificar /health antes del recorrido. El contenedor app resuelve las dependencias mediante Composer y npm, ejecuta el build de Vite y sirve los assets junto a las páginas Inertia. Laravel se conecta al servicio postgres por red Compose y Redis atiende sesiones, caché y cola. Para presentar, usar una base aislada y escenarios ficticios. El recorrido visual conjunto corresponde a la rama local del anfitrión. Reportes se presenta desde su propia rama. [Guía de implementación local](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/presentacion/README.md)

**Enlace de implementación publicada. Pendiente de confirmación del equipo.** Las fuentes describen instalaciones locales y la consulta de despliegues de GitHub devolvió una lista vacía. Se requiere una URL pública y una revisión asociada. El enlace a GitHub permite consultar el código y su documentación.

### 14.3. Verificación de Funcionamiento

Se comprobó en lectura el estado de los servicios locales y se reutilizó la evidencia del 22/11. La matriz del capítulo 13 ubica cada ejecución. La base integrada permite recorrer una convocatoria ficticia, autenticarse con el rol adecuado y consultar datos propios. Los controles experimentales aparecen al habilitar la bandera. La verificación técnica de la demostración deja pendiente la aceptación institucional.

### 14.4. Monitoreo del Sistema

| Mecanismo | Uso |
|---|---|
| GET /health | Estado de la base de datos y Redis |
| Healthchecks de Compose | app, queue, postgres y redis |
| Logs de Laravel | storage/logs y salida del contenedor |
| Tabla failed_jobs | Trabajos de cola fallidos |
| Auditoría | audit_logs de solo inserción, consultable por Dirección |

No hay monitoreo de errores en producción, alertas ni SLA: no se afirma disponibilidad ni rendimiento verificados.


## CONCLUSIONES

- La solución concentra el expediente y registra sus estados con responsables. La evidencia automatizada cubre los 27 RF de la línea base, incluidos aislamiento, decisión humana y auditoría.
- El corte distingue la operación integrada, la capacidad experimental detrás de bandera, los reportes operativos de una rama propia y los recursos visuales de la continuación local.
- La cobertura de código y las pruebas funcionales miden aspectos distintos. El Gate V3 evaluado convive con deuda estática y falta de instrumentación del frontend en Sonar.
- ML-01 mostró viabilidad técnica para riesgo operacional con datos sintéticos y una tasa de alerta elevada. ML-02 evidenció el límite de coincidencia léxica con Recall@3 cero en test. La decisión de selección sigue a cargo de Dirección.
- La práctica demuestra el comportamiento del software con datos ficticios. Los beneficios y la aceptación requieren trabajo de campo.

## RECOMENDACIONES

- Validar el AS-IS y el TO-BE con responsables autorizados y definir una línea base de tiempos, trazabilidad y comunicación.
- Someter Reportes y la continuación visual a revisión del candidato que se pretenda integrar. Repetir acceso, filtros y aislamiento si se cambia su base.
- Planificar instrumentación LCOV, corrección de deuda estática, recuperación de respaldos y mediciones de rendimiento, accesibilidad y compatibilidad.
- Para investigar ML-02, definir un método distinto con preregistro y conjunto de prueba independiente. Conservar el contrato experimental de ML-01.
- Registrar la URL de implementación y su revisión cuando el equipo disponga de un entorno publicado.

## REFERENCIAS

- Universidad Continental. (2026). Guías y formatos 02–11 de Pruebas y Calidad de Software. [Fuentes académicas](https://github.com/luivmz/saas-reclutamiento-multiempresa/tree/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/academico/00-fuentes-oficiales)
- Universidad Continental. (s. f.). Plantilla de estructura del proyecto final. Plantilla suministrada para esta edición.
- ISO/IEC. (2023). *ISO/IEC 25010:2023. Product quality model*. [Ficha oficial](https://www.iso.org/standard/78176.html).
- Manning, C. D., Raghavan, P., y Schütze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press. [Libro](https://doi.org/10.1017/CBO9780511809071).
- Robertson, S., y Zaragoza, H. (2009). The probabilistic relevance framework: BM25 and beyond. *Foundations and Trends in Information Retrieval, 3*(4), 333–389. [Artículo](https://doi.org/10.1561/1500000019).
- W3C. (2023). Web Content Accessibility Guidelines (WCAG) 2.2. [Recomendación WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- Equipo SaaS Reclutamiento Multiempresa. (2026). [Especificación UML v1.1](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/v1.1/uml/README.md) y [modelos PowerDesigner](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/v1.1/powerdesigner/README.md).
- Equipo SaaS Reclutamiento Multiempresa. (2026). [Práctica de arquitectura, Reportes y SonarQube](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/5e2eae37f63c7ac5d35ed2def9b2e843a644cd98/docs/architecture-cypress-reports/README.md).
- Equipo SaaS Reclutamiento Multiempresa. (2026). [Ficha de ML-01](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/v1.1/ml/model-card-draft.md) y [resultados de ML-02](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/academico/preparacion-f38-ml02/resultados-exp-bm25-v1/RESULTADOS.md).
- Equipo SaaS Reclutamiento Multiempresa. (2026). [Repositorio y documentación técnica](https://github.com/luivmz/saas-reclutamiento-multiempresa).

## ANEXOS

### A.1. Modelos y diagramas

Las figuras complementan los capítulos 3, 4 y 6. La {{ref:asis}} muestra el inicio del AS-IS preliminar. La {{ref:tobe}} expone la revisión del requerimiento en el proceso propuesto. La {{ref:casos}} vincula actores con los casos iniciales. El [catálogo Draw.io](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/5e2eae37f63c7ac5d35ed2def9b2e843a644cd98/docs/metologia/diagramas/README.md) conserva el conjunto editable completo. El [catálogo PowerDesigner](https://github.com/luivmz/saas-reclutamiento-multiempresa/tree/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/academico/powerdesigner) dispone de los BPMN formales.

{{fig:asis}}

{{fig:tobe}}

{{fig:casos}}

La {{ref:datos}} es una vista histórica del modelo físico, con ampliación disponible en la fuente. La {{ref:reportes-arq}} representa la autorización, las consultas y la página interna de Reportes en su rama.

{{fig:datos}}

{{fig:reportes-arq}}

### A.2. Evidencias funcionales y experimentales

La {{ref:reportes}} muestra el filtro aplicado y las cifras agregadas de una vacante ficticia. La {{ref:evidencias}} registra una versión de la evidencia y la ayuda léxica en una postulación. La {{ref:riesgo}} ilustra el panel de riesgo en el contexto de la vacante.

{{fig:reportes}}

{{fig:evidencias}}

{{fig:riesgo}}

La {{ref:cypress}} conserva el resumen de la ejecución 2 de la práctica. El contraste con la reauditoría se explica en §13.1.

{{fig:cypress}}

### A.3. Continuación de presentación

La portada se documenta en la {{ref:portada}} y el detalle en la {{ref:oferta}}. La {{ref:anfitrion}} corresponde a la revisión probada antes del seeder adicional.

{{fig:portada}}

{{fig:oferta}}

{{fig:anfitrion}}

### A.4. Trazabilidad y entregables anteriores

| Conjunto | Evidencia |
|---|---|
| Formatos F2–F11, F11-R y alcance F9 | [Línea base académica](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/academico/ACADEMIC_BASELINE.md) |
| Variables y operacionalización | [Paquete F29C](https://github.com/luivmz/saas-reclutamiento-multiempresa/tree/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/academico/operacionalizacion) |
| Plan y casos | [Plan F29D](https://github.com/luivmz/saas-reclutamiento-multiempresa/tree/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/academico/plan-pruebas) y [casos F29E](https://github.com/luivmz/saas-reclutamiento-multiempresa/tree/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/academico/casos-prueba) |
| QA y métricas históricas | [QA F29F](https://github.com/luivmz/saas-reclutamiento-multiempresa/tree/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/academico/qa-final) y [métricas F29G](https://github.com/luivmz/saas-reclutamiento-multiempresa/tree/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/academico/metricas-calidad) |
| Regresión y trazabilidad | [TDD](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/tdd-evidence.md) y [matriz RF](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/rf-implementation-matrix.md) |
| Gobernanza | [Guía experimental](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/experimental/README.md) y [progreso por fases](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/PROGRESS.md) |
