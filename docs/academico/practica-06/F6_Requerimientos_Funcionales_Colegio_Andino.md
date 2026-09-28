# Formato 06 — Requerimientos funcionales

> Espejo en Markdown de `F6_Requerimientos_Funcionales_Colegio_Andino.docx`, generado desde el mismo modelo (`docs/academico/tools/f27b/`). El entregable es el DOCX.

## 1. Datos generales del proyecto

| Campo | Valor |
|---|---|
| Nombre del proyecto | Análisis y Diseño de una Plataforma SaaS Multiempresa para la Gestión del Reclutamiento, Evaluación y Selección de Personal – Caso de estudio: Colegio Andino de Huancayo |
| Integrantes del equipo | Coronacion Meza Fredy; Peña Arroyo Anthony; Vila Meza Luis Antonio |
| Nombre de la empresa o institución | Colegio Andino de Huancayo (caso de estudio académico) |
| Nombre del proceso clave | Reclutamiento, evaluación y selección de personal |
| Docente | Dr. Maglioni Arana Caparachin |
| Fecha de elaboración | 26/09/2026 |

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
> Los RF-01 a RF-27 describen el **SOFTWARE IMPLEMENTADO** v1.1 (27 de 27 trazados a código y pruebas). La prioridad es una **priorización analítica del equipo**. RF-28 y RF-29 están en una sección aparte y **no** forman parte de la línea base.
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

**Usuarios principales.**

| Actor | Rol en el sistema | Tipo |
|---|---|---|
| Área solicitante | `solicitante` | Interno |
| Recursos Humanos (RR. HH.) | `rrhh` | Interno |
| Aprobador / Dirección | `aprobador` | Interno |
| Postulante | `postulante` | Externo |
| Evaluador | `evaluador` | Interno |

El Sistema valida, calcula, notifica y audita, pero **nunca selecciona**. No existe un rol de superadministrador.

**Relación con el proceso TO-BE.**

> Cada RF soporta al menos una actividad del TO-BE del Formato 05 (TB-01 a TB-30). La tabla de la sección 5 muestra la relación completa. La actividad TB-F1 («cerrar sin selección») es una propuesta futura y no tiene RF en la línea base.

## 3. Lista de requerimientos funcionales

| ID | Nombre del requerimiento | Descripción | Actor | Entradas | Salidas | Prioridad |
|---|---|---|---|---|---|---|
| RF-01 | Registrar requerimiento de personal | El sistema debe permitir al área solicitante registrar un requerimiento de personal. | Área solicitante | Puesto requerido, área, número de plazas (1–50), tipo de contrato, justificación (20–2000 caracteres) y fecha requerida (opcional, desde hoy). | Requerimiento en estado «borrador», con historial y registro de auditoría. | Alta |
| RF-02 | Validar y corregir requerimiento | El sistema debe permitir enviar el requerimiento a RR. HH., que lo valida u observa, y al área corregir y reenviar lo observado. | Área solicitante (enviar, corregir y reenviar) · RR. HH. (validar u observar) | Acción: enviar, validar u observar. La observación lleva un comentario de 5 a 1000 caracteres. Datos corregidos. | Estado «enviado», «observado» o «validado», con historial. | Alta |
| RF-03 | Registrar aprobación o rechazo del requerimiento | El sistema debe permitir al Aprobador / Dirección aprobar o rechazar un requerimiento validado, con motivo obligatorio si lo rechaza. | Aprobador / Dirección | Decisión (aprobar o rechazar) y motivo (obligatorio al rechazar, hasta 1000 caracteres). | Estado final «aprobado» o «rechazado», con historial y auditoría. | Alta |
| RF-04 | Notificar rechazo del requerimiento | El sistema debe notificar automáticamente al área solicitante el rechazo de su requerimiento, con el motivo. | Sistema (destinatario: área solicitante) | Rechazo registrado en RF-03, con su motivo. | Notificación en la plataforma y por correo, que se registra con el driver «log»: sin envío real (OUT-08). | Media |
| RF-05 | Registrar perfil y criterios del puesto | El sistema debe permitir a RR. HH. crear una vacante desde un requerimiento aprobado y registrar su perfil y sus criterios ponderados. | RR. HH. | Requerimiento aprobado; título, resumen, lugar, tipo de contrato y plazas; perfil (formación, experiencia, funciones y competencias); criterios con etapa, ponderación y rango. | Vacante en estado «borrador» con perfil y criterios. | Alta |
| RF-06 | Configurar y validar vacante | El sistema debe permitir configurar la convocatoria y mostrar una lista de validación previa a la publicación. | RR. HH. (configura) · Sistema (valida) | Plazas (sin superar las aprobadas) y fechas de apertura y cierre. **Nota (H-09):** desde la v1.1 (Fase 16) el formulario incluye además el campo opcional `target_completion_at` (plazo objetivo del proceso), un soporte operativo introducido para el servicio experimental RF-29. **No forma parte del RF-06 de la línea base v1.0.** | Lista de validación: ponderaciones, rangos, fechas, criterios y plazas. | Alta |
| RF-07 | Publicar vacante | El sistema debe publicar en el portal público de empleos las vacantes que cumplan la validación. | RR. HH. | Orden de publicación de una vacante en borrador. | Vacante «publicada», visible en el portal público de empleos. | Alta |
| RF-08 | Gestionar cuenta y acceso del postulante | El sistema debe permitir al postulante crear su cuenta e iniciar sesión. | Postulante | Nombre, correo y contraseña para el registro; credenciales para el inicio de sesión. | Cuenta global con rol de postulante, sin organización (A-04), y sesión iniciada. | Alta |
| RF-09 | Gestionar perfil y CV del postulante | El sistema debe permitir al postulante completar su perfil y cargar su CV en PDF de forma privada. | Postulante | Teléfono, ciudad, nivel educativo, título u ocupación, años de experiencia y resumen (opcional); CV en PDF de hasta 5 MB. | Perfil completo y CV guardado en disco privado con nombre UUID. | Alta |
| RF-10 | Registrar postulación | El sistema debe registrar una única postulación por postulante y vacante publicada y vigente. | Postulante | Vacante elegida. | Postulación en estado «postulado», con la referencia al CV vigente. | Alta |
| RF-11 | Confirmar postulación al postulante | El sistema debe confirmar cada postulación con un código de seguimiento y un aviso de recepción. | Sistema (destinatario: postulante) | Postulación registrada. | Código de seguimiento y notificación de recepción. | Media |
| RF-12 | Consultar y revisar postulaciones | El sistema debe listar las postulaciones de cada vacante y mostrar el expediente con datos, CV e historial. | RR. HH. (también consulta el Aprobador / Dirección) | Vacante y postulación seleccionadas. | Listado por vacante; expediente con datos, CV (descarga autorizada) e historial. | Alta |
| RF-13 | Registrar preselección o descarte | El sistema debe permitir a RR. HH. preseleccionar o descartar una postulación. El descarte lleva un motivo interno. | RR. HH. | Acción (preseleccionar o descartar) y motivo interno obligatorio al descartar (5–1000 caracteres). | Estado «preseleccionado» o «descartado», con historial; notificación RF-15. | Alta |
| RF-14 | Gestionar cambio de etapa de la postulación | El sistema debe permitir a RR. HH. cambiar la etapa de una postulación según las transiciones permitidas, con historial. | RR. HH. | Etapa de destino entre las asignables manualmente y observación opcional (hasta 1000 caracteres). | Nueva etapa, con historial y notificación RF-15. | Alta |
| RF-15 | Notificar cambio de etapa al candidato | El sistema debe avisar al postulante de cada cambio de etapa, sin revelar observaciones internas. | Sistema (destinatario: postulante) | Cambio de etapa (RF-13 o RF-14). | Aviso de cambio de etapa sin observaciones internas (A-14). | Media |
| RF-16 | Programar evaluación | El sistema debe permitir a RR. HH. programar una evaluación con un evaluador de la organización. | RR. HH. | Tipo de evaluación, evaluador de la organización, modalidad, lugar o enlace, fecha y hora futuras, duración opcional (15–480 min) e indicaciones. | Evaluación programada; postulación en «en evaluación»; convocatoria RF-17. | Alta |
| RF-17 | Generar convocatoria de evaluación | El sistema debe generar la convocatoria al postulante y el aviso de asignación al evaluador. | Sistema (destinatarios: postulante y evaluador) | Sesión programada (RF-16 o RF-18). | Convocatoria con fecha, modalidad, lugar e indicaciones; aviso al evaluador. | Media |
| RF-18 | Programar entrevista | El sistema debe permitir a RR. HH. programar una entrevista con un evaluador asignado y su convocatoria. | RR. HH. | Evaluador, modalidad, lugar, fecha futura, duración opcional e indicaciones. | Entrevista programada; postulación en «en entrevista»; convocatoria RF-17. | Alta |
| RF-19 | Registrar entrevista y su resultado | El sistema debe permitir al evaluador asignado registrar, una sola vez, los puntajes, el resultado y las observaciones de su sesión. | Evaluador asignado | Puntaje de cada criterio de la etapa (con comentario opcional). En la entrevista, además, el resultado (recomendado, recomendado con reservas o no recomendado) y observaciones (10–2000 caracteres); en la evaluación las observaciones son opcionales. | Sesión «realizada» con resultados que no se pueden editar. | Alta |
| RF-20 | Validar rangos y ponderaciones | El sistema debe validar que las ponderaciones y los rangos de los criterios sean coherentes y que cada puntaje esté dentro de su rango. | Sistema (lo configura RR. HH.) | Ponderaciones y rangos de los criterios; puntajes registrados. | Aceptación o rechazo, con mensaje. | Alta |
| RF-21 | Calcular ranking configurable | El sistema debe calcular un ranking ponderado, determinista y explicable, sin seleccionar a ningún candidato. | Sistema | Resultados de sesiones «realizada» de la vacante y de su organización, y ponderaciones. | Ranking de 0 a 100 con aportes por criterio, empates marcados (1, 2, 2, 4) y candidatos incompletos aparte. **No cambia estados.** | Alta |
| RF-22 | Presentar comparación de candidatos | El sistema debe presentar la comparación de candidatos con criterios, promedios, aportes, total y posición. | RR. HH. · Aprobador / Dirección | Vacante de la organización. | Vista de comparación explicable. | Alta |
| RF-23 | Registrar decisión final de selección | El sistema debe permitir al Aprobador / Dirección registrar la decisión final humana, con confirmación explícita y justificación. | Aprobador / Dirección | Candidato elegido (finalista con resultados completos), justificación (20–2000 caracteres) y confirmación explícita de decisión humana. | Decisión única e inmutable, con la posición y el puntaje del elegido en ese momento, y auditoría. **No cambia estados.** | Alta |
| RF-24 | Registrar selección del candidato | El sistema debe permitir a RR. HH. aplicar la decisión final registrando la selección del candidato decidido. | RR. HH. | Orden de registrar la selección. | La postulación decidida pasa a «seleccionado». Solo puede haber una por vacante (índice único). | Alta |
| RF-25 | Cerrar vacante o convocatoria | El sistema debe permitir a RR. HH. cerrar la convocatoria después de registrar la selección. | RR. HH. | Notas de cierre (opcional, hasta 1000 caracteres). | Vacante «cerrada»; las demás postulaciones activas pasan a «no seleccionado»; notificaciones RF-26. | Alta |
| RF-26 | Notificar resultado y cierre al postulante | El sistema debe notificar a cada postulante su propio resultado al cerrar la convocatoria. | Sistema (destinatarios: postulantes) | Cierre de la vacante (RF-25). | Resultado propio para el seleccionado y para cada no seleccionado, sin puntajes, ranking, justificaciones ni datos de otros. | Media |
| RF-27 | Generar registro de auditoría | El sistema debe registrar de forma de solo inserción las acciones críticas y permitir al Aprobador / Dirección consultarlas. | Sistema (registro) · Aprobador / Dirección (consulta) | Acción crítica ejecutada: usuario, organización, acción, entidad, fecha y metadatos permitidos. | Registro inmutable y vista de consulta paginada, filtrada por organización. | Alta |

La prioridad es una priorización analítica del equipo: **Alta** si el RF está en el camino principal del proceso y **Media** si es una notificación derivada de otra acción. Los 27 RF son de la línea base y están implementados.

**Nombres canónicos, fuente y alias históricos**

**Nombre canónico:** el del catálogo técnico de la línea base. **Fuente:** Catálogo técnico de la línea base v1.1 (Fase 22): `docs/v1.1/uml/use-cases.md`, casos UC-RF01 a UC-RF27. Es el mismo catálogo del encargo F27B §2. **Alias histórico:** el rótulo que otro documento usó para el mismo RF (abreviatura o variante). No es otro RF ni otro nombre oficial.

| RF | Nombre canónico | Fuente | Alias histórico | Observación |
|---|---|---|---|---|
| RF-01 | Registrar requerimiento de personal | UC-RF01 (F22) | — | Mismo nombre en el F9 y en el cap. 4 de v1.0 |
| RF-02 | Validar y corregir requerimiento | UC-RF02 (F22) | — | Mismo nombre en el F9 y en el cap. 4 de v1.0 |
| RF-03 | Registrar aprobación o rechazo del requerimiento | UC-RF03 (F22) | Registrar aprobación o rechazo | Rótulo abreviado o variante usado en: F9 v1.0 y v1.1 (tabla de línea base funcional); informe v1.0, cap. 4 §4.2. No es un RF distinto |
| RF-04 | Notificar rechazo del requerimiento | UC-RF04 (F22) | Notificar rechazo | Rótulo abreviado o variante usado en: F9 v1.0 y v1.1 (tabla de línea base funcional); informe v1.0, cap. 4 §4.2. No es un RF distinto |
| RF-05 | Registrar perfil y criterios del puesto | UC-RF05 (F22) | Registrar perfil y criterios | Rótulo abreviado o variante usado en: informe v1.0, cap. 4 §4.2. No es un RF distinto |
| RF-06 | Configurar y validar vacante | UC-RF06 (F22) | — | Mismo nombre en el F9 y en el cap. 4 de v1.0 |
| RF-07 | Publicar vacante | UC-RF07 (F22) | — | Mismo nombre en el F9 y en el cap. 4 de v1.0 |
| RF-08 | Gestionar cuenta y acceso del postulante | UC-RF08 (F22) | Gestionar cuenta y acceso | Rótulo abreviado o variante usado en: F9 v1.0 y v1.1 (tabla de línea base funcional). No es un RF distinto |
| RF-09 | Gestionar perfil y CV del postulante | UC-RF09 (F22) | Gestionar perfil y CV | Rótulo abreviado o variante usado en: F9 v1.0 y v1.1 (tabla de línea base funcional); informe v1.0, cap. 4 §4.2. No es un RF distinto |
| RF-10 | Registrar postulación | UC-RF10 (F22) | — | Mismo nombre en el F9 y en el cap. 4 de v1.0 |
| RF-11 | Confirmar postulación al postulante | UC-RF11 (F22) | Confirmar postulación | Rótulo abreviado o variante usado en: F9 v1.0 y v1.1 (tabla de línea base funcional); informe v1.0, cap. 4 §4.2. No es un RF distinto |
| RF-12 | Consultar y revisar postulaciones | UC-RF12 (F22) | — | Mismo nombre en el F9 y en el cap. 4 de v1.0 |
| RF-13 | Registrar preselección o descarte | UC-RF13 (F22) | — | Mismo nombre en el F9 y en el cap. 4 de v1.0 |
| RF-14 | Gestionar cambio de etapa de la postulación | UC-RF14 (F22) | Gestionar cambio de etapa | Rótulo abreviado o variante usado en: F9 v1.0 y v1.1 (tabla de línea base funcional); informe v1.0, cap. 4 §4.2. No es un RF distinto |
| RF-15 | Notificar cambio de etapa al candidato | UC-RF15 (F22) | Notificar cambio de etapa | Rótulo abreviado o variante usado en: F9 v1.0 y v1.1 (tabla de línea base funcional); informe v1.0, cap. 4 §4.2. No es un RF distinto |
| RF-16 | Programar evaluación | UC-RF16 (F22) | — | Mismo nombre en el F9 y en el cap. 4 de v1.0 |
| RF-17 | Generar convocatoria de evaluación | UC-RF17 (F22) | Generar convocatoria | Rótulo abreviado o variante usado en: F9 v1.0 y v1.1 (tabla de línea base funcional). No es un RF distinto |
| RF-18 | Programar entrevista | UC-RF18 (F22) | — | Mismo nombre en el F9 y en el cap. 4 de v1.0 |
| RF-19 | Registrar entrevista y su resultado | UC-RF19 (F22) | Registrar entrevista y resultado | Rótulo abreviado o variante usado en: F9 v1.0 y v1.1 (tabla de línea base funcional); informe v1.0, cap. 4 §4.2. No es un RF distinto |
| RF-20 | Validar rangos y ponderaciones | UC-RF20 (F22) | — | Mismo nombre en el F9 y en el cap. 4 de v1.0 |
| RF-21 | Calcular ranking configurable | UC-RF21 (F22) | — | Mismo nombre en el F9 y en el cap. 4 de v1.0 |
| RF-22 | Presentar comparación de candidatos | UC-RF22 (F22) | Presentar comparación | Rótulo abreviado o variante usado en: F9 v1.0 y v1.1 (tabla de línea base funcional). No es un RF distinto |
| RF-23 | Registrar decisión final de selección | UC-RF23 (F22) | Registrar decisión final humana | Rótulo abreviado o variante usado en: F9 v1.0 y v1.1 (tabla de línea base funcional). No es un RF distinto |
| RF-24 | Registrar selección del candidato | UC-RF24 (F22) | Registrar selección | Rótulo abreviado o variante usado en: F9 v1.0 y v1.1 (tabla de línea base funcional). No es un RF distinto |
| RF-25 | Cerrar vacante o convocatoria | UC-RF25 (F22) | — | Mismo nombre en el F9 y en el cap. 4 de v1.0 |
| RF-26 | Notificar resultado y cierre al postulante | UC-RF26 (F22) | Notificar resultado y cierre | Rótulo abreviado o variante usado en: F9 v1.0 y v1.1 (tabla de línea base funcional); informe v1.0, cap. 4 §4.2. No es un RF distinto |
| RF-27 | Generar registro de auditoría | UC-RF27 (F22) | — | Mismo nombre en el F9 y en el cap. 4 de v1.0 |

Los IDs no cambian. La Fase 24 registró «seis rótulos abreviados» en el Formato 09 (observación L-02). La comparación completa contra el catálogo canónico encuentra **13** rótulos distintos en el F9: 11 abreviaturas y 2 variantes (RF-19 y RF-23). En el informe v1.0 hay 8. Todos quedan resueltos aquí con su alias; el F9 publicado no se modifica.

## 4. Detalle de requerimientos funcionales

**RF-01: Registrar requerimiento de personal**

| Campo | Detalle |
|---|---|
| Descripción | El sistema debe permitir al área solicitante registrar un requerimiento de personal. |
| Actor principal | Área solicitante |
| Precondiciones | Usuario autenticado con rol de área solicitante de la organización. |
| Flujo principal | 1. Abre el formulario de nuevo requerimiento.<br>2. Ingresa los datos del puesto y la justificación.<br>3. El sistema valida los datos.<br>4. El sistema guarda el requerimiento en borrador con la organización del usuario y registra el historial. |
| Flujo alternativo | a) Datos inválidos: el sistema muestra los errores por campo y no guarda.<br>b) Usuario sin el rol: el acceso se deniega. |
| Postcondiciones | Requerimiento en borrador, visible solo para el área. RR. HH. y Dirección no ven borradores (A-05). |
| Actividad TO-BE | TB-01 |
| Evidencia de implementación | JobRequestWorkflowTest (test_rf01_*), E2E-02, E2E-13 |

**RF-02: Validar y corregir requerimiento**

| Campo | Detalle |
|---|---|
| Descripción | El sistema debe permitir enviar el requerimiento a RR. HH., que lo valida u observa, y al área corregir y reenviar lo observado. |
| Actor principal | Área solicitante (enviar, corregir y reenviar) · RR. HH. (validar u observar) |
| Precondiciones | Enviar: requerimiento propio en borrador u observado. Validar u observar: requerimiento enviado de la organización. |
| Flujo principal | 1. El área envía el requerimiento (estado «enviado»).<br>2. RR. HH. lo revisa.<br>3. RR. HH. lo valida (estado «validado»). |
| Flujo alternativo | a) RR. HH. lo observa con un comentario (estado «observado»); el área corrige y reenvía; vuelve al paso 2.<br>b) Observación sin comentario: se rechaza la acción.<br>c) Transición no permitida: el sistema la rechaza. |
| Postcondiciones | Requerimiento validado, disponible para la decisión del Aprobador / Dirección. |
| Actividad TO-BE | TB-02, TB-03, TB-04 |
| Evidencia de implementación | JobRequestWorkflowTest (test_rf02_*), E2E-02, E2E-13 |

**RF-03: Registrar aprobación o rechazo del requerimiento**

| Campo | Detalle |
|---|---|
| Descripción | El sistema debe permitir al Aprobador / Dirección aprobar o rechazar un requerimiento validado, con motivo obligatorio si lo rechaza. |
| Actor principal | Aprobador / Dirección |
| Precondiciones | Requerimiento «validado» de la misma organización. |
| Flujo principal | 1. Revisa el requerimiento validado.<br>2. Elige aprobar o rechazar.<br>3. El sistema registra la decisión y el historial. |
| Flujo alternativo | a) Rechazo sin motivo: el sistema lo impide.<br>b) Usuario de otra organización o sin el rol: acceso denegado.<br>c) Requerimiento no validado: la acción no está disponible. |
| Postcondiciones | Aprobado: habilita crear la vacante (RF-05). Rechazado: dispara RF-04. |
| Actividad TO-BE | TB-05 |
| Evidencia de implementación | JobRequestWorkflowTest (test_rf03_*), CrossTenantAccessTest, E2E-03, E2E-13 |

**RF-04: Notificar rechazo del requerimiento**

| Campo | Detalle |
|---|---|
| Descripción | El sistema debe notificar automáticamente al área solicitante el rechazo de su requerimiento, con el motivo. |
| Actor principal | Sistema (destinatario: área solicitante) |
| Precondiciones | Rechazo registrado (RF-03). |
| Flujo principal | 1. Al registrarse el rechazo, el sistema genera la notificación.<br>2. El solicitante la ve en sus notificaciones y en el detalle del requerimiento. |
| Flujo alternativo | a) Si el requerimiento se aprueba, no hay notificación de rechazo. |
| Postcondiciones | El área solicitante queda informada del rechazo y de su motivo. |
| Actividad TO-BE | TB-06 |
| Evidencia de implementación | JobRequestWorkflowTest (test_rf04_*); E2E-03 (rechazo sin motivo impedido) |

**RF-05: Registrar perfil y criterios del puesto**

| Campo | Detalle |
|---|---|
| Descripción | El sistema debe permitir a RR. HH. crear una vacante desde un requerimiento aprobado y registrar su perfil y sus criterios ponderados. |
| Actor principal | RR. HH. |
| Precondiciones | Requerimiento «aprobado» de la misma organización. |
| Flujo principal | 1. Crea la vacante desde el requerimiento aprobado.<br>2. Completa el perfil del puesto.<br>3. Define los criterios. Se proponen tres editables (40/30/30, A-09).<br>4. El sistema guarda la vacante en borrador. |
| Flujo alternativo | a) Requerimiento no aprobado: no se puede crear la vacante.<br>b) Datos inválidos: errores por campo.<br>c) Vacante no «borrador»: el perfil y los criterios ya no se editan (A-07). |
| Postcondiciones | Vacante en borrador, lista para configurar. |
| Actividad TO-BE | TB-07 |
| Evidencia de implementación | VacancyPublicationTest (test_rf05_*), E2E-04, E2E-13 |

**RF-06: Configurar y validar vacante**

| Campo | Detalle |
|---|---|
| Descripción | El sistema debe permitir configurar la convocatoria y mostrar una lista de validación previa a la publicación. |
| Actor principal | RR. HH. (configura) · Sistema (valida) |
| Precondiciones | Vacante en borrador de la organización. |
| Flujo principal | 1. Configura la convocatoria.<br>2. El sistema evalúa la lista de validación.<br>3. El sistema muestra qué está completo y qué falta. |
| Flujo alternativo | a) Configuración inválida: se puede guardar en borrador, pero no publicar (A-06).<br>b) Más plazas que las aprobadas: error (A-08). |
| Postcondiciones | Vacante lista para publicar cuando todas las validaciones se cumplen. |
| Actividad TO-BE | TB-08, TB-09 |
| Evidencia de implementación | VacancyPublicationTest (test_rf05_rf06_*, test_rf06_*), E2E-04 |

**RF-07: Publicar vacante**

| Campo | Detalle |
|---|---|
| Descripción | El sistema debe publicar en el portal público de empleos las vacantes que cumplan la validación. |
| Actor principal | RR. HH. |
| Precondiciones | Vacante en borrador con la validación completa. |
| Flujo principal | 1. RR. HH. solicita publicar.<br>2. El sistema vuelve a validar la configuración.<br>3. El sistema cambia el estado y la muestra en el portal. |
| Flujo alternativo | a) Validación incumplida: no se publica y se indica el motivo.<br>b) Otro rol: no puede publicar (solo RR. HH.). |
| Postcondiciones | Los postulantes pueden consultar la vacante y postular. |
| Actividad TO-BE | TB-10 |
| Evidencia de implementación | VacancyPublicationTest (test_rf07_*), E2E-04, E2E-13 |

**RF-08: Gestionar cuenta y acceso del postulante**

| Campo | Detalle |
|---|---|
| Descripción | El sistema debe permitir al postulante crear su cuenta e iniciar sesión. |
| Actor principal | Postulante |
| Precondiciones | Visitante sin sesión (registro) o postulante registrado (inicio de sesión). |
| Flujo principal | 1. Se registra con sus datos.<br>2. El sistema crea la cuenta con rol de postulante.<br>3. Inicia sesión. |
| Flujo alternativo | a) Correo ya registrado o datos inválidos: errores.<br>b) Credenciales incorrectas: acceso denegado.<br>c) Más de 5 intentos por minuto: bloqueo temporal. |
| Postcondiciones | Postulante autenticado. No se exige verificación de correo (A-01). |
| Actividad TO-BE | TB-11 |
| Evidencia de implementación | CandidateRegistrationTest, AuthenticationTest, E2E-01, E2E-05 |

**RF-09: Gestionar perfil y CV del postulante**

| Campo | Detalle |
|---|---|
| Descripción | El sistema debe permitir al postulante completar su perfil y cargar su CV en PDF de forma privada. |
| Actor principal | Postulante |
| Precondiciones | Postulante autenticado. |
| Flujo principal | 1. Completa el perfil.<br>2. Carga el CV.<br>3. El sistema valida y guarda el perfil y el CV. |
| Flujo alternativo | a) CV que no es PDF o supera 5 MB: se rechaza.<br>b) Campos obligatorios faltantes: errores. |
| Postcondiciones | Postulante habilitado para postular. No se piden DNI ni fecha de nacimiento (A-15). |
| Actividad TO-BE | TB-12 |
| Evidencia de implementación | CandidateProfileTest (test_rf09_*), E2E-05, E2E-13 |

**RF-10: Registrar postulación**

| Campo | Detalle |
|---|---|
| Descripción | El sistema debe registrar una única postulación por postulante y vacante publicada y vigente. |
| Actor principal | Postulante |
| Precondiciones | Vacante publicada y no cerrada; perfil completo y CV cargado (A-11); sin postulación previa a esa vacante. |
| Flujo principal | 1. Elige una vacante publicada.<br>2. Confirma la postulación.<br>3. El sistema valida los requisitos y la registra. |
| Flujo alternativo | a) Postulación duplicada: se rechaza (A-10).<br>b) Perfil incompleto o sin CV: se rechaza con indicaciones.<br>c) Vacante cerrada: se rechaza (E2E-12). |
| Postcondiciones | Postulación registrada; dispara RF-11. |
| Actividad TO-BE | TB-13 |
| Evidencia de implementación | ApplyToVacancyTest (test_rf10_*), VacancyClosureTest, E2E-05, E2E-12, E2E-13 |

**RF-11: Confirmar postulación al postulante**

| Campo | Detalle |
|---|---|
| Descripción | El sistema debe confirmar cada postulación con un código de seguimiento y un aviso de recepción. |
| Actor principal | Sistema (destinatario: postulante) |
| Precondiciones | Postulación registrada (RF-10). |
| Flujo principal | 1. El sistema genera el código de seguimiento.<br>2. Envía la notificación de recepción.<br>3. El postulante la ve en sus postulaciones. |
| Flujo alternativo | a) No hay caminos alternativos: toda postulación registrada se confirma. |
| Postcondiciones | El postulante tiene constancia de su postulación. |
| Actividad TO-BE | TB-14 |
| Evidencia de implementación | ApplyToVacancyTest (test_rf10_rf11_*), E2E-05 |

**RF-12: Consultar y revisar postulaciones**

| Campo | Detalle |
|---|---|
| Descripción | El sistema debe listar las postulaciones de cada vacante y mostrar el expediente con datos, CV e historial. |
| Actor principal | RR. HH. (también consulta el Aprobador / Dirección) |
| Precondiciones | Vacante de la organización del usuario. |
| Flujo principal | 1. Abre la vacante.<br>2. Revisa el listado de postulaciones.<br>3. Abre el expediente y, si lo necesita, descarga el CV. |
| Flujo alternativo | a) Vacante o postulación de otra organización: no es accesible.<br>b) El CV solo se descarga si la Policy lo autoriza. |
| Postcondiciones | Solo consulta: no cambia datos. |
| Actividad TO-BE | TB-15 |
| Evidencia de implementación | ApplicationReviewTest (test_rf12_*), E2E-06 |

**RF-13: Registrar preselección o descarte**

| Campo | Detalle |
|---|---|
| Descripción | El sistema debe permitir a RR. HH. preseleccionar o descartar una postulación. El descarte lleva un motivo interno. |
| Actor principal | RR. HH. |
| Precondiciones | Transición permitida por la máquina de estados (A-13); vacante sin decisión final registrada (A-28). |
| Flujo principal | 1. Revisa el expediente.<br>2. Preselecciona o descarta.<br>3. El sistema registra la etapa y el historial y notifica. |
| Flujo alternativo | a) Descarte sin motivo: error.<br>b) Decisión final ya registrada: acción bloqueada.<br>c) Transición no permitida: error. |
| Postcondiciones | Postulación en su nueva etapa; el postulante recibe el aviso (RF-15), sin el motivo interno. |
| Actividad TO-BE | TB-16 |
| Evidencia de implementación | ApplicationReviewTest (test_rf13_*), SelectionRegistrationTest, E2E-06 |

**RF-14: Gestionar cambio de etapa de la postulación**

| Campo | Detalle |
|---|---|
| Descripción | El sistema debe permitir a RR. HH. cambiar la etapa de una postulación según las transiciones permitidas, con historial. |
| Actor principal | RR. HH. |
| Precondiciones | Transición válida (A-13); vacante no cerrada; sin decisión final (A-28). |
| Flujo principal | 1. Elige la etapa de destino.<br>2. El sistema valida la transición.<br>3. Registra la etapa y el historial y notifica. |
| Flujo alternativo | a) «Seleccionado» y «no seleccionado» no se asignan a mano: solo por RF-24 y RF-25.<br>b) Transición no permitida o posterior a la decisión: error.<br>c) Al programar una sesión, la etapa avanza sola a «en evaluación» o «en entrevista» (A-16). |
| Postcondiciones | Postulación en la etapa elegida, con trazabilidad del cambio. |
| Actividad TO-BE | TB-23 |
| Evidencia de implementación | ApplicationReviewTest (test_rf14_*), ApplicationStatusTest, E2E-06, E2E-13 |

**RF-15: Notificar cambio de etapa al candidato**

| Campo | Detalle |
|---|---|
| Descripción | El sistema debe avisar al postulante de cada cambio de etapa, sin revelar observaciones internas. |
| Actor principal | Sistema (destinatario: postulante) |
| Precondiciones | Cambio de etapa registrado. |
| Flujo principal | 1. El sistema genera el aviso.<br>2. El postulante lo ve en sus notificaciones y en el detalle de la postulación. |
| Flujo alternativo | a) Si el cambio se debe a la programación de una sesión, se envía la convocatoria (RF-17) en lugar de este aviso (A-16). |
| Postcondiciones | El postulante conoce su etapa. |
| Actividad TO-BE | TB-17 |
| Evidencia de implementación | ApplicationReviewTest (test_rf13_rf15_*), E2E-06 |

**RF-16: Programar evaluación**

| Campo | Detalle |
|---|---|
| Descripción | El sistema debe permitir a RR. HH. programar una evaluación con un evaluador de la organización. |
| Actor principal | RR. HH. |
| Precondiciones | Postulación en «preseleccionado» o «en evaluación»; la vacante tiene criterios de la etapa y no está cerrada (A-16). |
| Flujo principal | 1. Elige la postulación.<br>2. Completa los datos de la sesión.<br>3. El sistema valida, programa y envía la convocatoria. |
| Flujo alternativo | a) Evaluador de otra organización o sin el rol: error (A-17).<br>b) Fecha pasada: error (A-18).<br>c) Etapa no permitida: error.<br>d) No hay cancelación ni reprogramación (A-22). |
| Postcondiciones | Sesión programada y comunicada. |
| Actividad TO-BE | TB-18 |
| Evidencia de implementación | EvaluationTest (test_rf16_*), E2E-13 |

**RF-17: Generar convocatoria de evaluación**

| Campo | Detalle |
|---|---|
| Descripción | El sistema debe generar la convocatoria al postulante y el aviso de asignación al evaluador. |
| Actor principal | Sistema (destinatarios: postulante y evaluador) |
| Precondiciones | Sesión programada. |
| Flujo principal | 1. El sistema genera la convocatoria.<br>2. La envía al postulante y avisa al evaluador asignado. |
| Flujo alternativo | a) El postulante nunca ve puntajes, observaciones ni el resultado de la entrevista (A-21). |
| Postcondiciones | Postulante y evaluador informados de la sesión. |
| Actividad TO-BE | TB-19 |
| Evidencia de implementación | EvaluationTest (test_rf16_rf17_*), InterviewTest (test_rf18_*), E2E-13 |

**RF-18: Programar entrevista**

| Campo | Detalle |
|---|---|
| Descripción | El sistema debe permitir a RR. HH. programar una entrevista con un evaluador asignado y su convocatoria. |
| Actor principal | RR. HH. |
| Precondiciones | Postulación en «preseleccionado», «en evaluación» o «en entrevista»; vacante no cerrada (A-16). |
| Flujo principal | 1. Elige la postulación.<br>2. Completa los datos de la entrevista.<br>3. El sistema valida, programa y envía la convocatoria. |
| Flujo alternativo | a) Evaluador no válido o fecha pasada: error.<br>b) Etapa no permitida: error. |
| Postcondiciones | Entrevista programada y comunicada. |
| Actividad TO-BE | TB-20 |
| Evidencia de implementación | InterviewTest (test_rf18_*), VacancyClosureTest, E2E-13 |

**RF-19: Registrar entrevista y su resultado**

| Campo | Detalle |
|---|---|
| Descripción | El sistema debe permitir al evaluador asignado registrar, una sola vez, los puntajes, el resultado y las observaciones de su sesión. |
| Actor principal | Evaluador asignado |
| Precondiciones | Ser el evaluador asignado; resultados aún no registrados; vacante no cerrada (A-19). |
| Flujo principal | 1. Abre la sesión asignada.<br>2. Registra los puntajes, el resultado y las observaciones.<br>3. El sistema valida (RF-20) y guarda. |
| Flujo alternativo | a) Puntaje fuera de rango o criterio faltante: error (RF-20).<br>b) Otro evaluador: acceso denegado.<br>c) Resultados ya registrados o vacante cerrada: bloqueado. |
| Postcondiciones | Resultados disponibles para el ranking (RF-21). |
| Actividad TO-BE | TB-21 |
| Evidencia de implementación | InterviewTest (test_rf19_*), EvaluationTest, E2E-07, E2E-13 |

**RF-20: Validar rangos y ponderaciones**

| Campo | Detalle |
|---|---|
| Descripción | El sistema debe validar que las ponderaciones y los rangos de los criterios sean coherentes y que cada puntaje esté dentro de su rango. |
| Actor principal | Sistema (lo configura RR. HH.) |
| Precondiciones | Configuración de la vacante, registro de puntajes o cálculo del ranking. |
| Flujo principal | 1. Al configurar o publicar: la suma de ponderaciones es la configurada (100 por defecto, A-06), los pesos son positivos y el mínimo es menor que el máximo.<br>2. Al registrar resultados: cada puntaje está en su rango y se cubren todos los criterios de la etapa.<br>3. Al calcular el ranking: la configuración es válida. |
| Flujo alternativo | a) Configuración inválida: la vacante no se publica y el ranking se rechaza.<br>b) Puntaje fuera de rango: no se registra. |
| Postcondiciones | Solo se usan datos coherentes para evaluar y comparar. |
| Actividad TO-BE | TB-09, TB-22 |
| Evidencia de implementación | WeightingValidatorTest, ScoreSheetValidatorTest, RankingServiceTest (test_rf20_*), E2E-04, E2E-07 |

**RF-21: Calcular ranking configurable**

| Campo | Detalle |
|---|---|
| Descripción | El sistema debe calcular un ranking ponderado, determinista y explicable, sin seleccionar a ningún candidato. |
| Actor principal | Sistema |
| Precondiciones | Vacante con configuración válida. |
| Flujo principal | 1. Filtra las postulaciones no descartadas de la vacante (A-23).<br>2. Promedia los puntajes por criterio y normaliza con la fórmula de A-24.<br>3. Ordena y marca los empates, sin desempatarlos (A-26). |
| Flujo alternativo | a) Configuración inválida: error.<br>b) Candidato sin todos los puntajes: se lista aparte, sin imputar cero (A-25). |
| Postcondiciones | Ranking disponible como apoyo. Ninguna postulación cambia de estado. |
| Actividad TO-BE | TB-24 |
| Evidencia de implementación | RankingServiceTest (test_rf21_*), RankingComparisonTest, E2E-08, E2E-13 |

**RF-22: Presentar comparación de candidatos**

| Campo | Detalle |
|---|---|
| Descripción | El sistema debe presentar la comparación de candidatos con criterios, promedios, aportes, total y posición. |
| Actor principal | RR. HH. · Aprobador / Dirección |
| Precondiciones | Permiso para ver el ranking de la vacante (Policy de rol y organización). |
| Flujo principal | 1. Abre la comparación de la vacante.<br>2. El sistema calcula el ranking (RF-21) y lo presenta con sus aportes. |
| Flujo alternativo | a) Otra organización o rol no autorizado: acceso denegado. |
| Postcondiciones | Información disponible para la decisión humana (RF-23). |
| Actividad TO-BE | TB-25 |
| Evidencia de implementación | RankingComparisonTest (test_rf21_rf22_*, test_rf22_*), E2E-08 |

**RF-23: Registrar decisión final de selección**

| Campo | Detalle |
|---|---|
| Descripción | El sistema debe permitir al Aprobador / Dirección registrar la decisión final humana, con confirmación explícita y justificación. |
| Actor principal | Aprobador / Dirección |
| Precondiciones | Rol de Aprobador de la misma organización; vacante sin decisión previa; candidato finalista con resultados completos. |
| Flujo principal | 1. Consulta la comparación (RF-22).<br>2. Elige a un finalista, que puede no ser el primero del ranking.<br>3. Escribe la justificación y confirma que la decisión es suya.<br>4. El sistema registra la decisión. |
| Flujo alternativo | a) Sin confirmación o con justificación corta: error.<br>b) Candidato no finalista o incompleto: error.<br>c) Ya existe una decisión: bloqueado.<br>d) Otro rol, incluido RR. HH.: acceso denegado. |
| Postcondiciones | Habilita RF-24 y bloquea los cambios manuales de etapa (A-28). **El sistema nunca decide por sí mismo.** |
| Actividad TO-BE | TB-26 |
| Evidencia de implementación | FinalDecisionTest (test_rf23_*), RankingComparisonTest::test_rf23_calculating_the_ranking_never_selects_a_candidate, E2E-09, E2E-12, E2E-13 |

**RF-24: Registrar selección del candidato**

| Campo | Detalle |
|---|---|
| Descripción | El sistema debe permitir a RR. HH. aplicar la decisión final registrando la selección del candidato decidido. |
| Actor principal | RR. HH. |
| Precondiciones | Decisión final registrada (RF-23); vacante no cerrada. |
| Flujo principal | 1. Abre la vacante con decisión.<br>2. Registra la selección.<br>3. El sistema cambia el estado de la postulación decidida. |
| Flujo alternativo | a) Sin decisión final: error de regla de negocio.<br>b) Vacante cerrada: bloqueado. |
| Postcondiciones | Selección registrada; habilita el cierre (RF-25). |
| Actividad TO-BE | TB-27 |
| Evidencia de implementación | SelectionRegistrationTest (test_rf24_*), E2E-10, E2E-12, E2E-13 |

**RF-25: Cerrar vacante o convocatoria**

| Campo | Detalle |
|---|---|
| Descripción | El sistema debe permitir a RR. HH. cerrar la convocatoria después de registrar la selección. |
| Actor principal | RR. HH. |
| Precondiciones | Selección registrada (RF-24). |
| Flujo principal | 1. Solicita el cierre.<br>2. El sistema cierra la vacante y actualiza las postulaciones activas.<br>3. Notifica los resultados (RF-26). |
| Flujo alternativo | a) Sin selección: no se puede cerrar. El cierre sin selección está fuera de la línea base (A-30); en el TO-BE es la propuesta futura TB-F1.<br>b) Vacante ya cerrada: error, sin notificar de nuevo (A-32). |
| Postcondiciones | Convocatoria cerrada. Se bloquean postulaciones, cambios, programación, resultados, decisión y selección. |
| Actividad TO-BE | TB-28 |
| Evidencia de implementación | VacancyClosureTest (test_rf25_*), ApplicationStatusTest, E2E-10, E2E-12, E2E-13 |

**RF-26: Notificar resultado y cierre al postulante**

| Campo | Detalle |
|---|---|
| Descripción | El sistema debe notificar a cada postulante su propio resultado al cerrar la convocatoria. |
| Actor principal | Sistema (destinatarios: postulantes) |
| Precondiciones | Vacante cerrada. |
| Flujo principal | 1. El sistema identifica a los destinatarios.<br>2. Envía a cada uno su resultado. |
| Flujo alternativo | a) Las postulaciones descartadas no reciben un segundo aviso (A-31).<br>b) Un reintento del cierre falla antes de notificar (A-32). |
| Postcondiciones | Cada postulante conoce su resultado. |
| Actividad TO-BE | TB-29 |
| Evidencia de implementación | ProcessResultNotificationTest (test_rf26_*), E2E-10, E2E-13 |

**RF-27: Generar registro de auditoría**

| Campo | Detalle |
|---|---|
| Descripción | El sistema debe registrar de forma de solo inserción las acciones críticas y permitir al Aprobador / Dirección consultarlas. |
| Actor principal | Sistema (registro) · Aprobador / Dirección (consulta) |
| Precondiciones | Registro: se ejecuta una acción crítica. Consulta: rol de Aprobador de la organización. |
| Flujo principal | 1. El sistema registra la acción crítica sin datos sensibles.<br>2. El Aprobador consulta la auditoría de su organización. |
| Flujo alternativo | a) Cualquier UPDATE o DELETE sobre la tabla lo rechaza el trigger de la base.<br>b) Los datos sensibles se descartan (DEF-08).<br>c) RR. HH. y los demás roles no consultan la auditoría (A-33). |
| Postcondiciones | Trazabilidad de las acciones críticas. |
| Actividad TO-BE | TB-30 |
| Evidencia de implementación | AuditTrailTest (test_rf27_*), AuditLogViewTest, AuditLoggerTest, E2E-11, E2E-13 |

## 5. Trazabilidad con el proceso TO-BE

| Actividad del proceso (TO-BE) | Requerimiento funcional asociado |
|---|---|
| TB-01 Registrar el requerimiento de personal | RF-01 |
| TB-02 Enviar el requerimiento a RR. HH. | RF-02 |
| TB-03 Revisar el requerimiento y validarlo u observarlo | RF-02 |
| TB-04 Corregir y reenviar el requerimiento observado | RF-02 |
| TB-05 Aprobar o rechazar el requerimiento | RF-03 |
| TB-06 Notificar el rechazo al área solicitante | RF-04 |
| TB-07 Crear la vacante y registrar el perfil y los criterios ponderados | RF-05 |
| TB-08 Configurar la vacante | RF-06 |
| TB-09 Validar la configuración, las ponderaciones y los rangos | RF-06, RF-20 |
| TB-10 Publicar la vacante en el portal de empleos | RF-07 |
| TB-11 Crear la cuenta e iniciar sesión | RF-08 |
| TB-12 Completar el perfil y cargar el CV | RF-09 |
| TB-13 Registrar la postulación | RF-10 |
| TB-14 Confirmar la postulación | RF-11 |
| TB-15 Revisar las postulaciones y el expediente | RF-12 |
| TB-16 Preseleccionar o descartar | RF-13 |
| TB-17 Notificar el cambio de etapa al postulante | RF-15 |
| TB-18 Programar la evaluación | RF-16 |
| TB-19 Enviar la convocatoria al postulante y el aviso al evaluador | RF-17 |
| TB-20 Programar la entrevista | RF-18 |
| TB-21 Registrar puntajes, resultado y observaciones | RF-19 |
| TB-22 Validar los puntajes dentro del rango de cada criterio | RF-20 |
| TB-23 Actualizar la etapa de la postulación (finalista o descarte) | RF-14 |
| TB-24 Calcular el ranking ponderado explicable | RF-21 |
| TB-25 Presentar la comparación de candidatos | RF-22 |
| TB-26 Registrar la decisión final humana | RF-23 |
| TB-27 Registrar la selección del candidato decidido | RF-24 |
| TB-28 Cerrar la convocatoria (con selección) | RF-25 |
| TB-29 Notificar el resultado a cada postulante | RF-26 |
| TB-30 Registrar la auditoría de las acciones críticas | RF-27 |
| TB-F1 Cerrar la convocatoria sin selección (convocatoria desierta) | — (propuesta futura, sin RF) |

## 6. Extensiones posteriores al baseline

Estas extensiones **no** forman parte de RF-01 a RF-27, no se mezclan con la tabla principal y su promoción es una decisión pendiente del equipo (`docs/v1.1/scope-preliminary.md`, preguntas 12 y 13).

| ID | Nombre | Estado | Descripción | Fuente |
|---|---|---|---|---|
| RF-28 | Panel operativo descriptivo (candidato) | CANDIDATO — NO IMPLEMENTADO | Panel agregado de etapas, tiempos, backlog y cuellos de botella de las convocatorias, sin datos de personas. Atendería la parte de indicadores de gestión de P5. No tiene rutas, pruebas ni pantallas. El estado `descriptive_only` de la tarjeta de RF-29 **no** es este panel. | docs/v1.1/scope-preliminary.md; docs/v1.1/uml/use-cases.md (UC-RF28 «propuesto v1.1», sin asociaciones) |
| RF-29 | Consultar riesgo operacional del proceso (experimental) | EXPERIMENTAL — process-only, no productivo | Estima el riesgo de demora del **proceso** de una vacante con un servicio externo opcional (desactivado por defecto con `ML_SERVICE_ENABLED=false`). **No evalúa candidatos, no decide, no selecciona ni descarta, no modifica el ranking** y no guarda su resultado. Validado solo con datos sintéticos; no autorizado para producción. No cambia RF-23. | docs/v1.1/phase-16-laravel-ml-integration.md; docs/v1.1/phase-17-ml-validation.md; UC-RF29 «experimental» |
