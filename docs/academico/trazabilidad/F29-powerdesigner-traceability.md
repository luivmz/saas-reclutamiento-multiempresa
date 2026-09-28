# Trazabilidad F29 — especificación → modelo PowerDesigner → exportación

Generado por [`powerdesigner/scripts/make_f29_docs.py`](../powerdesigner/scripts/make_f29_docs.py) a partir de los modelos guardados y de las fuentes del contenido (`tools/f27b/m_asis.py`, `m_tobe.py`, `m_cu.py` y `practica-11/COMPONENTS.md`). No editar a mano: volver a generarlo.

**«Dibujado»** indica que el objeto tiene símbolo en el diagrama de su vista. **«Carril»** es el responsable (atributo *Organization Unit*) guardado en el modelo.

## Vistas

**Estado (28/09/2026):** las cuatro vistas están auditadas (F29 y F29B) y su exportación formal es el diagrama principal del Formato (FORMAL EXPORT INTEGRATED). Las 7 capturas reales de PowerDesigner están registradas en el [manifiesto](../powerdesigner/MANIFEST.md) (POWERDESIGNER EVIDENCE CAPTURED).

| Vista | Especificación | Modelo · paquete | Diagrama | Exportaciones | Verificación | Formato (DOCX / PDF) | Capturas | Estado |
|---|---|---|---|---|---|---|---|---|
| F3 | [`POWERDESIGNER_PENDING.md`](../practica-03/POWERDESIGNER_PENDING.md) | `F29_BPM_Academico.bpm · F3` | «F3 - BPMN AS-IS» | [PNG](../powerdesigner/exports/F3_BPMN_ASIS.png) · [SVG](../powerdesigner/exports/F3_BPMN_ASIS.svg) | [`F3_model_check.txt`](../powerdesigner/validation/F3_model_check.txt) | [DOCX](../practica-03/F3_Diagrama_BPM_ASIS_Colegio_Andino.docx) · [PDF](../practica-03/F3_Diagrama_BPM_ASIS_Colegio_Andino.pdf) | [1](../powerdesigner/evidencias/capturas/F3_BPMN_ASIS_PowerDesigner.png) · [2](../powerdesigner/evidencias/capturas/F3_SP-01_detalle_PowerDesigner.png) | FORMAL EXPORT INTEGRATED · POWERDESIGNER EVIDENCE CAPTURED |
| F5 | [`POWERDESIGNER_PENDING.md`](../practica-05/POWERDESIGNER_PENDING.md) | `F29_BPM_Academico.bpm · F5` | «F5 - BPMN TO-BE» | [PNG](../powerdesigner/exports/F5_BPMN_TOBE.png) · [SVG](../powerdesigner/exports/F5_BPMN_TOBE.svg) | [`F5_model_check.txt`](../powerdesigner/validation/F5_model_check.txt) | [DOCX](../practica-05/F5_Modelo_BPM_TOBE_Colegio_Andino.docx) · [PDF](../practica-05/F5_Modelo_BPM_TOBE_Colegio_Andino.pdf) | [1](../powerdesigner/evidencias/capturas/F5_BPMN_TOBE_PowerDesigner_parte1.png) · [2](../powerdesigner/evidencias/capturas/F5_BPMN_TOBE_PowerDesigner_parte2.png) · [3](../powerdesigner/evidencias/capturas/F5_SP-P_detalle_PowerDesigner.png) | FORMAL EXPORT INTEGRATED · POWERDESIGNER EVIDENCE CAPTURED |
| F8 | [`POWERDESIGNER_PENDING.md`](../practica-08/POWERDESIGNER_PENDING.md) | `F29_UML_Academico.oom · F8` | «F8 - Casos de Uso Academicos» | [PNG](../powerdesigner/exports/F8_Casos_de_Uso_Academicos.png) · [SVG](../powerdesigner/exports/F8_Casos_de_Uso_Academicos.svg) | [`F8_model_check.txt`](../powerdesigner/validation/F8_model_check.txt) | [DOCX](../practica-08/F8_Diagrama_Casos_de_Uso_Colegio_Andino.docx) · [PDF](../practica-08/F8_Diagrama_Casos_de_Uso_Colegio_Andino.pdf) | [1](../powerdesigner/evidencias/capturas/F8_Casos_de_Uso_PowerDesigner.png) | FORMAL EXPORT INTEGRATED · POWERDESIGNER EVIDENCE CAPTURED |
| F11 ARQ-01 | [`POWERDESIGNER_PENDING.md`](../practica-11/POWERDESIGNER_PENDING.md) | `F29_UML_Academico.oom · ARQ01` | «ARQ-01 - Arquitectura Conceptual» | [PNG](../powerdesigner/exports/ARQ-01_Arquitectura_Conceptual.png) · [SVG](../powerdesigner/exports/ARQ-01_Arquitectura_Conceptual.svg) | [`ARQ01_model_check.txt`](../powerdesigner/validation/ARQ01_model_check.txt) | [DOCX](../practica-11/F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.docx) · [PDF](../practica-11/F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.pdf) | [1](../powerdesigner/evidencias/capturas/ARQ01_Arquitectura_Conceptual_PowerDesigner.png) | FORMAL EXPORT INTEGRATED · POWERDESIGNER EVIDENCE CAPTURED |

## F3 — BPMN AS-IS

| ID | Nombre oficial | Tipo (estereotipo) | Carril | Dibujado | Problemas / origen |
|---|---|---|---|---|---|
| EI-01 | Necesidad de personal identificada | Start Event | — | sí | Evento de inicio (pool Colegio) |
| G-01 | ¿Necesidad aprobada? | Exclusive Gateway | — | sí | Compuerta exclusiva |
| EF-01 | Necesidad no aprobada | End Event | — | sí | Evento de fin del proceso |
| SP-01 | Evaluar al candidato | Sub-Process | RR. HH. | sí | Subproceso de instancia múltiple (paralela), una instancia por candidato |
| SI-01 | Candidato a evaluar | Start Event | — | sí | Evento de inicio de SP-01 |
| G-02 | ¿Candidato preseleccionado? | Exclusive Gateway | — | sí | Compuerta exclusiva (dentro de SP-01) |
| EF-02 | El candidato no continúa | End Event | — | sí | Evento de fin de SP-01 |
| EF-04 | Candidato evaluado | End Event | — | sí | Evento de fin de SP-01 |
| EF-03 | Resultado comunicado | End Event | — | sí | Evento de fin del proceso |
| EP-01 | Convocatoria recibida | Message Start Event | — | sí | Evento de inicio de mensaje (pool Postulante) |
| EP-02 | Postulación presentada | End Event | — | sí | Evento de fin (pool Postulante) |
| AS-01 | Identificar la necesidad de personal | Task | Área solicitante | sí | — · macro 1 |
| AS-02 | Comunicar la necesidad a RR. HH. | Task | Área solicitante | sí | P1, P2 · macro 1 |
| AS-03 | Revisar la necesidad | Task | RR. HH. | sí | P2 · macro 2 (desagregación) |
| AS-04 | Aprobar o no aprobar la necesidad | Task | Dirección | sí | P2 · macro 2 (desagregación) |
| AS-05 | Definir el perfil del puesto | Task | RR. HH. | sí | P1 · macro 3 (desagregación) |
| AS-06 | Difundir la convocatoria | Task | RR. HH. | sí | P1 · macro 3 (desagregación) |
| AS-07 | Presentar la postulación y el CV | Task | — | sí | P4 · macro 4 (desagregación) |
| AS-08 | Recibir y reunir postulaciones y CV | Receive Task | RR. HH. | sí | P1 · macro 4 |
| AS-09 | Revisar el CV y preseleccionar al candidato | Task | RR. HH. | sí | P2 · macro 5 |
| AS-10 | Coordinar evaluaciones y entrevistas | Task | RR. HH. | sí | P4 · macro 6 (desagregación) |
| AS-11 | Realizar evaluaciones y entrevistas | Task | Evaluadores | sí | P3 · macro 6 (desagregación) |
| AS-12 | Consolidar resultados y comparar candidatos | Task | RR. HH. | sí | P3, P5 · macro 7 |
| AS-13 | Decidir el candidato seleccionado | Task | Dirección | sí | P5 · macro 8 (desagregación) |
| AS-14 | Comunicar el resultado | Task | RR. HH. | sí | P4 · macro 8 (desagregación) |

Mensajes: MF-01 AS-06 → EP-01; MF-02 AS-07 → AS-08; MF-03 AS-10 → borde del pool Postulante; MF-04 AS-14 → borde del pool Postulante (formatos de mensaje `F3_MF_01` a `F3_MF_04`).

## F5 — BPMN TO-BE

| ID | Nombre oficial | Tipo (estereotipo) | Carril | Dibujado | RF | Origen AS-IS |
|---|---|---|---|---|---|---|
| TB-01 | Registrar el requerimiento de personal | Task | Área solicitante | sí | RF-01 | AS-01, AS-02 |
| TB-02 | Enviar el requerimiento a RR. HH. | Task | Área solicitante | sí | RF-02 | AS-02 |
| TB-03 | Revisar el requerimiento y validarlo u observarlo | Task | RR. HH. | sí | RF-02 | AS-03 |
| TB-04 | Corregir y reenviar el requerimiento observado | Task | Área solicitante | sí | RF-02 | AS-03 |
| TB-05 | Aprobar o rechazar el requerimiento | Task | Aprobador / Dirección | sí | RF-03 | AS-04 |
| TB-06 | Notificar el rechazo al área solicitante | Task | Plataforma SaaS (sistema) | sí | RF-04 | AS-04 |
| TB-07 | Crear la vacante y registrar el perfil y los criterios ponderados | Task | RR. HH. | sí | RF-05 | AS-05 |
| TB-08 | Configurar la vacante | Task | RR. HH. | sí | RF-06 | AS-05 |
| TB-09 | Validar la configuración, las ponderaciones y los rangos | Task | Plataforma SaaS (sistema) | sí | RF-06, RF-20 | AS-05 |
| TB-10 | Publicar la vacante en el portal de empleos | Task | RR. HH. | sí | RF-07 | AS-06 |
| TB-11 | Crear la cuenta e iniciar sesión | Task | — | sí | RF-08 | AS-07 |
| TB-12 | Completar el perfil y cargar el CV | Task | — | sí | RF-09 | AS-07 |
| TB-13 | Registrar la postulación | Task | — | sí | RF-10 | AS-07 |
| TB-14 | Confirmar la postulación | Task | Plataforma SaaS (sistema) | sí | RF-11 | AS-07 |
| TB-15 | Revisar las postulaciones y el expediente | Task | RR. HH. | sí | RF-12 | AS-08 |
| TB-16 | Preseleccionar o descartar | Task | RR. HH. | sí | RF-13 | AS-09 |
| TB-17 | Notificar el cambio de etapa al postulante | Task | Plataforma SaaS (sistema) | sí | RF-15 | AS-09 |
| TB-18 | Programar la evaluación | Task | RR. HH. | sí | RF-16 | AS-10 |
| TB-19 | Enviar la convocatoria al postulante y el aviso al evaluador | Task | Plataforma SaaS (sistema) | sí | RF-17 | AS-10 |
| TB-20 | Programar la entrevista | Task | RR. HH. | sí | RF-18 | AS-10 |
| TB-21 | Registrar puntajes, resultado y observaciones | Task | Evaluador | sí | RF-19 | AS-11 |
| TB-22 | Validar los puntajes dentro del rango de cada criterio | Task | Plataforma SaaS (sistema) | sí | RF-20 | AS-11 |
| TB-23 | Actualizar la etapa de la postulación (finalista o descarte) | Task | RR. HH. | sí | RF-14 | AS-11 |
| TB-24 | Calcular el ranking ponderado explicable | Task | Plataforma SaaS (sistema) | sí | RF-21 | AS-12 |
| TB-25 | Presentar la comparación de candidatos | Task | Plataforma SaaS (sistema) | sí | RF-22 | AS-12 |
| TB-26 | Registrar la decisión final humana | Task | Aprobador / Dirección | sí | RF-23 | AS-13 |
| TB-27 | Registrar la selección del candidato decidido | Task | RR. HH. | sí | RF-24 | AS-14 |
| TB-28 | Cerrar la convocatoria (con selección) | Task | RR. HH. | sí | RF-25 | AS-14 |
| TB-29 | Notificar el resultado a cada postulante | Task | Plataforma SaaS (sistema) | sí | RF-26 | AS-14 |
| TB-30 | Registrar la auditoría de las acciones críticas | Task | Plataforma SaaS (sistema) | sí | RF-27 | — |
| TB-F1 | Cerrar la convocatoria sin selección (convocatoria desierta) | Task (propuesta futura A-30, desconectada) | RR. HH. | sí | — | — |
| EI | Necesidad de personal identificada | Start Event | — | sí | — | — |
| EFA | Requerimiento rechazado | End Event | — | sí | — | — |
| EFE | Convocatoria cerrada con selección | End Event | — | sí | — | — |
| SIP | Postulación registrada | Start Event | — | sí | — | — |
| EFP-01 | Postulación descartada en la preselección | End Event | — | sí | — | — |
| EFP-02 | Postulación finalista | Message End Event | RR. HH. | sí | — | — |
| EFP-03 | Postulación descartada tras la evaluación | Message End Event | Plataforma SaaS (sistema) | sí | — | — |
| EP-01 | Vacante publicada | Message Start Event | — | sí | — | — |
| EP-02 | Postulación presentada | End Event | — | sí | — | — |
| GA1 | ¿Requerimiento conforme? | Exclusive Gateway | — | sí | — | — |
| GA2 | ¿Requerimiento aprobado? | Exclusive Gateway | — | sí | — | — |
| GB1 | ¿Configuración válida? | Exclusive Gateway | — | sí | — | — |
| GD1 | ¿Candidato preseleccionado? | Exclusive Gateway | — | sí | — | — |
| GM1 | Unión antes de programar | Exclusive Gateway | — | sí | — | — |
| GD2 | ¿Qué sesión se programa? | Exclusive Gateway | — | sí | — | — |
| GM2 | Unión de sesiones programadas | Exclusive Gateway | — | sí | — | — |
| GV | ¿Puntajes válidos? | Exclusive Gateway | — | sí | — | — |
| GD3 | ¿Otra sesión? | Exclusive Gateway | — | sí | — | — |
| GF | ¿Finalista? | Exclusive Gateway | — | sí | — | — |
| SP-P | Gestionar la postulación | Sub-Process, instancia múltiple paralela | RR. HH. | sí | — | — |

Mensajes: MT-01 TB-10 Publicar la vacante → EP-01 Vacante publicada; MT-02 TB-13 Registrar la postulación → Borde de SP-P (crea una instancia); MT-03 TB-14 Confirmar la postulación → Borde del pool Postulante; MT-04 TB-17 Notificar el cambio de etapa → Borde del pool Postulante; MT-05 TB-19 Enviar la convocatoria → Borde del pool Postulante; MT-06 EFP-02 Postulación finalista → Borde del pool Postulante; MT-07 EFP-03 Postulación descartada tras la evaluación → Borde del pool Postulante; MT-08 TB-29 Notificar el resultado → Borde del pool Postulante.

## F8 — Casos de uso (vista académica)

| CU | Nombre | Actores | RF | CU del F9 v1.0 | Vista técnica | Dibujado |
|---|---|---|---|---|---|---|
| CU-01 | Registrar requerimiento de personal | ACT-01 | RF-01 | CU-01 | UC-RF01 | sí |
| CU-02 | Validar y corregir requerimiento | ACT-01, ACT-02 | RF-02 | CU-01 (corregir) · CU-02 (validar) | UC-RF02 | sí |
| CU-03 | Aprobar o rechazar requerimiento | ACT-03 | RF-03, RF-04 | CU-03 | UC-RF03, UC-RF04 «extend» | sí |
| CU-04 | Registrar perfil y criterios del puesto | ACT-02 | RF-05 | CU-04 | UC-RF05 | sí |
| CU-05 | Configurar y validar vacante | ACT-02 | RF-06 | CU-04 | UC-RF06 | sí |
| CU-06 | Publicar vacante | ACT-02 | RF-07 | CU-04 | UC-RF07 | sí |
| CU-07 | Gestionar cuenta y acceso | ACT-04 | RF-08 | CU-05 | UC-RF08 | sí |
| CU-08 | Gestionar perfil y CV | ACT-04 | RF-09 | CU-05 | UC-RF09 | sí |
| CU-09 | Registrar postulación | ACT-04 | RF-10, RF-11 | CU-06 | UC-RF10, UC-RF11 «include» | sí |
| CU-10 | Consultar y revisar postulaciones | ACT-02, ACT-03 | RF-12 | CU-07 | UC-RF12 | sí |
| CU-11 | Registrar preselección o descarte | ACT-02 | RF-13 | CU-07 | UC-RF13, UC-RF15 «include» | sí |
| CU-12 | Gestionar cambio de etapa | ACT-02 | RF-14, RF-15 | CU-07 | UC-RF14, UC-RF15 «include» | sí |
| CU-13 | Programar evaluación | ACT-02 | RF-16, RF-17 | CU-08 | UC-RF16, UC-RF17 «include» | sí |
| CU-14 | Programar entrevista | ACT-02 | RF-18 | CU-08 | UC-RF18, UC-RF17 «include» | sí |
| CU-15 | Registrar resultados de evaluación y entrevista | ACT-05 | RF-19 | CU-09 | UC-RF19 | sí |
| CU-16 | Validar rangos y ponderaciones | — (inclusión) | RF-20 | CU-04 · CU-09 | UC-RF20 | sí |
| CU-17 | Consultar ranking y comparación | ACT-02, ACT-03 | RF-21, RF-22 | CU-10 | UC-RF21, UC-RF22 | sí |
| CU-18 | Registrar decisión final humana | ACT-03 | RF-23 | CU-11 | UC-RF23 «human decision» | sí |
| CU-19 | Registrar selección | ACT-02 | RF-24 | CU-12 | UC-RF24 | sí |
| CU-20 | Cerrar convocatoria y notificar resultado | ACT-02 | RF-25, RF-26 | CU-12 | UC-RF25, UC-RF26 «include» | sí |

Actores: ACT-01 Área solicitante; ACT-02 Recursos Humanos; ACT-03 Aprobador / Dirección; ACT-04 Postulante; ACT-05 Evaluador. «include»: CU-05 → CU-16, CU-15 → CU-16, CU-17 → CU-16. CU-21 diferido, no modelado. RF-27: nota técnica (UC-RF27).

## F11 — ARQ-01 arquitectura conceptual

| ID | Componente | Estereotipo | Agrupación (paquete) | RF | CU | Dibujado |
|---|---|---|---|---|---|---|
| C01 | Interfaz web | conceptual | Capa de presentación | RF-01..RF-27 (interacción) | Todos (interfaz) | sí |
| C02 | Autenticación y cuentas | conceptual | Capa de acceso y seguridad | RF-08 | CU-07 | sí |
| C03 | Autorización y contexto multiempresa | conceptual, transversal | Capa de acceso y seguridad | RNF (seguridad y multitenencia); aplica a RF-01..RF-27 | Todos (transversal) | sí |
| C04 | Requerimientos de personal | conceptual | Capa de negocio | RF-01, RF-02, RF-03, RF-04 | CU-01, CU-02, CU-03 | sí |
| C05 | Vacantes y convocatorias | conceptual | Capa de negocio | RF-05, RF-06, RF-07, RF-20 | CU-04, CU-05, CU-06, CU-16 | sí |
| C06 | Postulantes y CV | conceptual | Capa de negocio | RF-09 | CU-08 | sí |
| C07 | Postulaciones y etapas | conceptual | Capa de negocio | RF-10, RF-11, RF-12, RF-13, RF-14, RF-15 | CU-09, CU-10, CU-11, CU-12 | sí |
| C08 | Evaluaciones y entrevistas | conceptual | Capa de negocio | RF-16, RF-17, RF-18, RF-19, RF-20 | CU-13, CU-14, CU-15, CU-16 | sí |
| C09 | Ranking y comparación | conceptual, apoyo | Capa de negocio | RF-20, RF-21, RF-22 | CU-16, CU-17 | sí |
| C10 | Decisión final humana | conceptual, human decision | Capa de negocio | RF-23 | CU-18 | sí |
| C11 | Selección y cierre | conceptual | Capa de negocio | RF-24, RF-25, RF-26 | CU-19, CU-20 | sí |
| C12 | Notificaciones | conceptual, transversal | Servicios transversales | RF-04, RF-11, RF-15, RF-17, RF-26 | Incluidas en CU-03, CU-09, CU-11, CU-12, CU-13, CU-14, CU-20 | sí |
| C13 | Auditoría | conceptual, transversal | Servicios transversales | RF-27 | Transversal (UC-RF27) | sí |
| C14 | Persistencia de datos (PostgreSQL) | conceptual, infraestructura | Persistencia e infraestructura | Soporte de RF-01..RF-27 | — | sí |
| C15 | Almacenamiento privado de CV | conceptual, infraestructura | Persistencia e infraestructura | RF-09, RF-12 | CU-08, CU-10 | sí |
| C16 | Sesiones, caché y cola (Redis) | conceptual, infraestructura | Persistencia e infraestructura | Soporte de C02 y C12 | — | sí |
| C17 | Riesgo operacional del proceso (RF-29) | conceptual, experimental | Experimental (opcional) | RF-29 (candidato, experimental) | — (fuera del catálogo; UC-RF29) | sí |

Relaciones (dependencias del paquete ARQ01): R-01 C01 → C02; R-02 C02 → C03; R-03 C03 → C04 a C11, C13; R-04 C01 → C04 a C11, C13; R-05 C04 → C05; R-06 C05 → C07; R-07 C06 → C07; R-08 C08 → C07; R-09 C08 → C09; R-10 C09 → C10; R-11 C10 → C11; R-12 C11 → C07; R-13 C04 a C11 → C13; R-14 C04, C07, C08, C11 → C12; R-15 C12 → C16; R-16 C04 a C13 → C14; R-17 C06, C07 → C15; R-18 C02 → C16; R-19 C05 → C17; R-20 C17 → C01. R-03, R-04, R-13, R-14 y R-16 usan el paquete «Capa de negocio» como extremo, como pide la especificación.
