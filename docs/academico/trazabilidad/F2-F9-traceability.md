# Trazabilidad F2 → F9 (Fases 27B y 27D)

Cadena académica completa: actividad AS-IS → problema → solución → actividad TO-BE → RF → RNF relevantes → CU → alcance del F9.
Se genera desde los mismos modelos que los Formatos 02 a 08 (`docs/academico/tools/f27b/`), así que no puede contradecirlos.
Para regenerarla: `python docs/academico/tools/f27b/build.py trace`.

Alcance de la validación automática: [`README.md`](README.md). `validate.py` comprueba la coherencia **estructural**, no la semántica completa.

| Formato | Entregable |
|---|---|
| F2 | [`practica-02`](../practica-02/README.md) |
| F3 | [`practica-03`](../practica-03/README.md) |
| F4 | [`practica-04`](../practica-04/README.md) |
| F5 | [`practica-05`](../practica-05/README.md) |
| F6 | [`practica-06`](../practica-06/README.md) |
| F7 | [`practica-07`](../practica-07/README.md) |
| F8 | [`practica-08`](../practica-08/README.md) |
| F9 | [`phase-24/output`](../phase-24/README.md) (publicado, sin cambios) y [`practica-09`](../practica-09/F9_POST_RELEASE_ADDENDUM.md) (adenda) |

**Estado de cada eslabón:**

| Eslabón | Estado |
|---|---|
| AS-IS (F2 a F4) | **Preliminar**, sujeto a validación institucional |
| TO-BE (F5) | **Propuesto** |
| RF (F6) y CU (F8) | Describen el **software implementado** v1.1 |
| RNF (F7) | Cada uno con su estado de verificación |
| RF-28, RF-29 y RNF-A a RNF-D | **Fuera** de la cadena de la línea base |

## 1. Cadena completa por actividad TO-BE

**Dos columnas de problema (H-06):**

- **«Problema directo (F4)»:** solo los problemas que el Formato 04 asigna a la actividad AS-IS de origen.
- **«Problema vía solución»:** el problema que atiende la solución (F5, relación de §2.3) donde participa esa actividad TO-BE.

Una columna no se deduce de la otra, y no se atribuye a ninguna actividad un problema que F4 no le asignó.

| AS-IS | Problema directo (F4) | Problema vía solución | Solución | Actividad TO-BE | RF | RNF relevantes | CU | Alcance F9 |
|---|---|---|---|---|---|---|---|---|
| AS-01, AS-02 | P1, P2 | P1 | S-01 | TB-01 Registrar el requerimiento de personal | RF-01 | RNF-01, RNF-02, RNF-03, RNF-10 | CU-01 | IN-01 |
| AS-02 | P1, P2 | P2 | S-02 | TB-02 Enviar el requerimiento a RR. HH. | RF-02 | RNF-01, RNF-02, RNF-03, RNF-10 | CU-02 | IN-01 |
| AS-03 | P2 | P2 | S-02 | TB-03 Revisar el requerimiento y validarlo u observarlo | RF-02 | RNF-01, RNF-02, RNF-03, RNF-10 | CU-02 | IN-01 |
| AS-03 | P2 | P2 | S-02 | TB-04 Corregir y reenviar el requerimiento observado | RF-02 | RNF-01, RNF-02, RNF-03, RNF-10 | CU-02 | IN-01 |
| AS-04 | P2 | P2 | S-02 | TB-05 Aprobar o rechazar el requerimiento | RF-03 | RNF-01, RNF-02, RNF-03, RNF-10 | CU-03 | IN-01 |
| AS-04 | P2 | P4 | S-04 | TB-06 Notificar el rechazo al área solicitante | RF-04 | RNF-02 | CU-03 | IN-01 |
| AS-05 | P1 | P1, P3 | S-01, S-03 | TB-07 Crear la vacante y registrar el perfil y los criterios ponderados | RF-05 | RNF-01, RNF-02, RNF-03, RNF-10 | CU-04 | IN-02 |
| AS-05 | P1 | P1 | S-01 | TB-08 Configurar la vacante | RF-06 | RNF-01, RNF-02, RNF-03, RNF-10 | CU-05 | IN-02 |
| AS-05 | P1 | P3 | S-03 | TB-09 Validar la configuración, las ponderaciones y los rangos | RF-06, RF-20 | RNF-01, RNF-02, RNF-03, RNF-10 | CU-05, CU-16 | IN-02, IN-06 |
| AS-06 | P1 | — | — | TB-10 Publicar la vacante en el portal de empleos | RF-07 | RNF-01, RNF-02, RNF-03, RNF-10 | CU-06 | IN-02 |
| AS-07 | P4 | — | — | TB-11 Crear la cuenta e iniciar sesión | RF-08 | RNF-01, RNF-04 | CU-07 | IN-03 |
| AS-07 | P4 | P1 | S-01 | TB-12 Completar el perfil y cargar el CV | RF-09 | RNF-04, RNF-05 | CU-08 | IN-03 |
| AS-07 | P4 | P1 | S-01 | TB-13 Registrar la postulación | RF-10 | RNF-04, RNF-10 | CU-09 | IN-03 |
| AS-07 | P4 | P4 | S-04 | TB-14 Confirmar la postulación | RF-11 | RNF-04 | CU-09 | IN-03 |
| AS-08 | P1 | P1 | S-01 | TB-15 Revisar las postulaciones y el expediente | RF-12 | RNF-02, RNF-04, RNF-06 | CU-10 | IN-04 |
| AS-09 | P2 | P2 | S-02 | TB-16 Preseleccionar o descartar | RF-13 | RNF-01, RNF-02, RNF-03, RNF-10 | CU-11 | IN-04 |
| AS-09 | P2 | P4 | S-04 | TB-17 Notificar el cambio de etapa al postulante | RF-15 | RNF-04 | CU-12 | IN-04 |
| AS-10 | P4 | P3 | S-03 | TB-18 Programar la evaluación | RF-16 | RNF-01, RNF-02, RNF-03, RNF-10 | CU-13 | IN-05 |
| AS-10 | P4 | P3, P4 | S-03, S-04 | TB-19 Enviar la convocatoria al postulante y el aviso al evaluador | RF-17 | RNF-04 | CU-13 | IN-05 |
| AS-10 | P4 | P3 | S-03 | TB-20 Programar la entrevista | RF-18 | RNF-01, RNF-02, RNF-03, RNF-10 | CU-14 | IN-05 |
| AS-11 | P3 | P3 | S-03 | TB-21 Registrar puntajes, resultado y observaciones | RF-19 | RNF-01, RNF-02, RNF-03, RNF-10 | CU-15 | IN-05 |
| AS-11 | P3 | P3 | S-03 | TB-22 Validar los puntajes dentro del rango de cada criterio | RF-20 | RNF-10 | CU-16 | IN-06 |
| AS-11 | P3 | P2 | S-02 | TB-23 Actualizar la etapa de la postulación (finalista o descarte) | RF-14 | RNF-01, RNF-02, RNF-03, RNF-10 | CU-12 | IN-04 |
| AS-12 | P3, P5 | P3, P5 | S-03, S-05 | TB-24 Calcular el ranking ponderado explicable | RF-21 | RNF-06, RNF-10 | CU-17 | IN-06 |
| AS-12 | P3, P5 | P3, P5 | S-03, S-05 | TB-25 Presentar la comparación de candidatos | RF-22 | RNF-02, RNF-05, RNF-06 | CU-17 | IN-06 |
| AS-13 | P5 | P5 | S-05 | TB-26 Registrar la decisión final humana | RF-23 | RNF-01, RNF-02, RNF-03 | CU-18 | IN-07 |
| AS-14 | P4 | P2 | S-02 | TB-27 Registrar la selección del candidato decidido | RF-24 | RNF-01, RNF-02, RNF-03, RNF-10 | CU-19 | IN-07 |
| AS-14 | P4 | P2 | S-02 | TB-28 Cerrar la convocatoria (con selección) | RF-25 | RNF-01, RNF-02, RNF-03, RNF-10 | CU-20 | IN-07 |
| AS-14 | P4 | P4 | S-04 | TB-29 Notificar el resultado a cada postulante | RF-26 | RNF-04 | CU-20 | IN-07 |
| — (nueva) | — | P5 | S-05 | TB-30 Registrar la auditoría de las acciones críticas | RF-27 | RNF-02, RNF-03 | RF-27: — (transversal; fuera del catálogo CU-01..CU-20) | IN-08 |
| — (nueva) | — | — | — | TB-F1 Cerrar la convocatoria sin selección (convocatoria desierta) | — (propuesta futura) | — | — | Fuera de alcance (OUT) |

## 2. Del proceso actual al TO-BE

| AS-IS | Actividad actual | Problemas (F4) | Actividades TO-BE que la sustituyen |
|---|---|---|---|
| AS-01 | Identificar la necesidad de personal | — | TB-01 |
| AS-02 | Comunicar la necesidad a RR. HH. | P1, P2 | TB-01, TB-02 |
| AS-03 | Revisar la necesidad | P2 | TB-03, TB-04 |
| AS-04 | Aprobar o no aprobar la necesidad | P2 | TB-05, TB-06 |
| AS-05 | Definir el perfil del puesto | P1 | TB-07, TB-08, TB-09 |
| AS-06 | Difundir la convocatoria | P1 | TB-10 |
| AS-07 | Presentar la postulación y el CV | P4 | TB-11, TB-12, TB-13, TB-14 |
| AS-08 | Recibir y reunir postulaciones y CV | P1 | TB-15 |
| AS-09 | Revisar el CV y preseleccionar al candidato | P2 | TB-16, TB-17 |
| AS-10 | Coordinar evaluaciones y entrevistas | P4 | TB-18, TB-19, TB-20 |
| AS-11 | Realizar evaluaciones y entrevistas | P3 | TB-21, TB-22, TB-23 |
| AS-12 | Consolidar resultados y comparar candidatos | P3, P5 | TB-24, TB-25 |
| AS-13 | Decidir el candidato seleccionado | P5 | TB-26 |
| AS-14 | Comunicar el resultado | P4 | TB-27, TB-28, TB-29 |

## 3. Por requerimiento funcional

RF-23 va a CU-18 «Registrar decisión final humana» → UC-RF23 (IN-07). RF-27 es transversal → UC-RF27 (IN-08) y no se mezcla con RF-23 (H-07).

| RF | Nombre canónico | TO-BE | CU académico | CU agrupado (v1.0) | UC-RF | RNF relevantes | Alcance F9 |
|---|---|---|---|---|---|---|---|
| RF-01 | Registrar requerimiento de personal | TB-01 | CU-01 | CU-01 | UC-RF01 | RNF-01, RNF-02, RNF-03, RNF-10 | IN-01 |
| RF-02 | Validar y corregir requerimiento | TB-02, TB-03, TB-04 | CU-02 | CU-01 (corregir) · CU-02 (validar) | UC-RF02 | RNF-01, RNF-02, RNF-03, RNF-10 | IN-01 |
| RF-03 | Registrar aprobación o rechazo del requerimiento | TB-05 | CU-03 | CU-03 | UC-RF03, UC-RF04 «extend» | RNF-01, RNF-02, RNF-03, RNF-10 | IN-01 |
| RF-04 | Notificar rechazo del requerimiento | TB-06 | CU-03 | CU-03 | UC-RF03, UC-RF04 «extend» | RNF-02 | IN-01 |
| RF-05 | Registrar perfil y criterios del puesto | TB-07 | CU-04 | CU-04 | UC-RF05 | RNF-01, RNF-02, RNF-03, RNF-10 | IN-02 |
| RF-06 | Configurar y validar vacante | TB-08, TB-09 | CU-05 | CU-04 | UC-RF06 | RNF-01, RNF-02, RNF-03, RNF-10 | IN-02 |
| RF-07 | Publicar vacante | TB-10 | CU-06 | CU-04 | UC-RF07 | RNF-01, RNF-02, RNF-03, RNF-10 | IN-02 |
| RF-08 | Gestionar cuenta y acceso del postulante | TB-11 | CU-07 | CU-05 | UC-RF08 | RNF-01, RNF-04 | IN-03 |
| RF-09 | Gestionar perfil y CV del postulante | TB-12 | CU-08 | CU-05 | UC-RF09 | RNF-04, RNF-05 | IN-03 |
| RF-10 | Registrar postulación | TB-13 | CU-09 | CU-06 | UC-RF10, UC-RF11 «include» | RNF-04, RNF-10 | IN-03 |
| RF-11 | Confirmar postulación al postulante | TB-14 | CU-09 | CU-06 | UC-RF10, UC-RF11 «include» | RNF-04 | IN-03 |
| RF-12 | Consultar y revisar postulaciones | TB-15 | CU-10 | CU-07 | UC-RF12 | RNF-02, RNF-04, RNF-06 | IN-04 |
| RF-13 | Registrar preselección o descarte | TB-16 | CU-11 | CU-07 | UC-RF13, UC-RF15 «include» | RNF-01, RNF-02, RNF-03, RNF-10 | IN-04 |
| RF-14 | Gestionar cambio de etapa de la postulación | TB-23 | CU-12 | CU-07 | UC-RF14, UC-RF15 «include» | RNF-01, RNF-02, RNF-03, RNF-10 | IN-04 |
| RF-15 | Notificar cambio de etapa al candidato | TB-17 | CU-12 | CU-07 | UC-RF14, UC-RF15 «include» | RNF-04 | IN-04 |
| RF-16 | Programar evaluación | TB-18 | CU-13 | CU-08 | UC-RF16, UC-RF17 «include» | RNF-01, RNF-02, RNF-03, RNF-10 | IN-05 |
| RF-17 | Generar convocatoria de evaluación | TB-19 | CU-13 | CU-08 | UC-RF16, UC-RF17 «include» | RNF-04 | IN-05 |
| RF-18 | Programar entrevista | TB-20 | CU-14 | CU-08 | UC-RF18, UC-RF17 «include» | RNF-01, RNF-02, RNF-03, RNF-10 | IN-05 |
| RF-19 | Registrar entrevista y su resultado | TB-21 | CU-15 | CU-09 | UC-RF19 | RNF-01, RNF-02, RNF-03, RNF-10 | IN-05 |
| RF-20 | Validar rangos y ponderaciones | TB-09, TB-22 | CU-16 | CU-04 · CU-09 | UC-RF20 | RNF-10 | IN-06 |
| RF-21 | Calcular ranking configurable | TB-24 | CU-17 | CU-10 | UC-RF21, UC-RF22 | RNF-10, RNF-06 | IN-06 |
| RF-22 | Presentar comparación de candidatos | TB-25 | CU-17 | CU-10 | UC-RF21, UC-RF22 | RNF-02, RNF-05, RNF-06 | IN-06 |
| RF-23 | Registrar decisión final de selección | TB-26 | CU-18 | CU-11 | UC-RF23 «human decision» | RNF-01, RNF-02, RNF-03 | IN-07 |
| RF-24 | Registrar selección del candidato | TB-27 | CU-19 | CU-12 | UC-RF24 | RNF-01, RNF-02, RNF-03, RNF-10 | IN-07 |
| RF-25 | Cerrar vacante o convocatoria | TB-28 | CU-20 | CU-12 | UC-RF25, UC-RF26 «include» | RNF-01, RNF-02, RNF-03, RNF-10 | IN-07 |
| RF-26 | Notificar resultado y cierre al postulante | TB-29 | CU-20 | CU-12 | UC-RF25, UC-RF26 «include» | RNF-04 | IN-07 |
| RF-27 | Generar registro de auditoría | TB-30 | — (transversal; fuera del catálogo CU-01..CU-20) | CU-13 | UC-RF27 | RNF-03, RNF-02 | IN-08 |

## 4. RNF transversales

| RNF | Nombre | Estado | Equivalente técnico |
|---|---|---|---|
| RNF-01 | Seguridad y control de acceso | VERIFICADO | cap. 4 RNF-01 (autenticación) + RNF-02 (autorización) |
| RNF-02 | Multitenencia y aislamiento | VERIFICADO | cap. 4 RNF-03 (aislamiento multiempresa) |
| RNF-03 | Trazabilidad y auditoría | VERIFICADO | cap. 4 RNF-05 (responsabilidad) + RNF-10 (trazabilidad funcional) |
| RNF-04 | Privacidad | VERIFICADO | cap. 4 RNF-06 (privacidad) |
| RNF-05 | Usabilidad | EVIDENCIA PARCIAL | cap. 4 RNF-07 (usabilidad); candidato RNF-A (accesibilidad, propuesta) |
| RNF-06 | Rendimiento | NO VERIFICADO | Sin equivalente técnico (el cap. 4 declara que no hay SLA ni pruebas de carga); candidato RNF-B (propuesta) |
| RNF-07 | Disponibilidad y recuperabilidad | NO VERIFICADO | Sin equivalente técnico |
| RNF-08 | Compatibilidad | EVIDENCIA PARCIAL | Sin equivalente técnico (el cap. 4 RNF-07 cubre el diseño adaptable, no los navegadores) |
| RNF-09 | Mantenibilidad | EVIDENCIA PARCIAL | cap. 4 RNF-08 (mantenibilidad) |
| RNF-10 | Integridad de datos | VERIFICADO | cap. 4 RNF-04 (integridad) |

## 5. Validación de coherencia estructural (§17 del encargo)

Resultado de `docs/academico/tools/f27b/validate.py` al generar este documento: **37 de 37 reglas OK, 0 fallas.**

Es una validación **estructural**. En la F27D, además, se revisaron a mano F3, F5, F8 y esta trazabilidad (ver [`README.md`](README.md)).

| Regla | Resultado | Detalle |
|---|---|---|
| F2: toda actividad AS-IS tiene un actor que la ejecuta o valida | OK |  |
| F4: todo problema tiene actividades AS-IS existentes | OK |  |
| F2 ↔ F4: las etiquetas de problema de las actividades coinciden con F4 | OK |  |
| F2 ↔ F4: cada problema P1–P5 tiene una observación en F2 | OK |  |
| F5: toda solución responde a un problema de F4 | OK |  |
| F5: todo problema de F4 tiene solución | OK |  |
| F5: las actividades de cada solución existen en el TO-BE | OK |  |
| F5: toda actividad TO-BE tiene actor | OK |  |
| F2 → F5: toda actividad AS-IS tiene continuidad en el TO-BE | OK |  |
| F5: los RF de cada solución están soportados por sus actividades TO-BE | OK |  |
| F6: todo RF-01..RF-27 tiene actividad TO-BE | OK |  |
| F6: el TO-BE no usa RF fuera de la línea base | OK |  |
| F6: hay exactamente 27 fichas, en orden y sin duplicados | OK |  |
| F6 ↔ F5: la actividad TO-BE de cada ficha contiene ese RF | OK |  |
| F6: todo RF tiene actor | OK |  |
| F6: RF-28 y RF-29 solo están en extensiones | OK |  |
| F6: RF-23 es una decisión humana del Aprobador / Dirección | OK |  |
| F7: hay 10 RNF académicos, cada uno con método de verificación y estado | OK |  |
| F7: los estados usan solo el vocabulario permitido | OK |  |
| F7: RNF-C figura solo como propuesta | OK |  |
| F8: todo RF-01..RF-27 está en algún CU o declarado transversal (RF-27) | OK |  |
| F8: RF-23 solo en el CU de decisión final humana y sin RF-27 | OK |  |
| F8: ningún CU usa RF fuera de la línea base | OK |  |
| F8: todo CU tiene actor directo o es un caso incluido | OK |  |
| F8: todo CU tiene RF | OK |  |
| F8: hay 20 CU académicos (CU-01..CU-20) | OK |  |
| F9: se leyó la tabla RF → CU del F9 publicado (27 filas) | OK | 27 |
| F8 ↔ F9: la relación RF → CU → bloque IN coincide con el F9 publicado (RF-27: solo el bloque, divergencia de CU documentada en D-CU-04) | OK |  |
| Ninguna afirmación de validación institucional sin negación o condición | OK |  |
| F3/F5: no quedan variantes de nombre retiradas (glosario único) | OK |  |
| DOCX F2_Analisis_del_Proceso_Colegio_Andino.docx: ZIP y XML válidos, imágenes presentes, sin campos vacíos de plantilla | OK | 2 imágenes |
| DOCX F3_Diagrama_BPM_ASIS_Colegio_Andino.docx: ZIP y XML válidos, imágenes presentes, sin campos vacíos de plantilla | OK | 2 imágenes |
| DOCX F4_Problemas_del_Proceso_Colegio_Andino.docx: ZIP y XML válidos, imágenes presentes, sin campos vacíos de plantilla | OK | 2 imágenes |
| DOCX F5_Modelo_BPM_TOBE_Colegio_Andino.docx: ZIP y XML válidos, imágenes presentes, sin campos vacíos de plantilla | OK | 5 imágenes |
| DOCX F6_Requerimientos_Funcionales_Colegio_Andino.docx: ZIP y XML válidos, imágenes presentes, sin campos vacíos de plantilla | OK | 0 imágenes |
| DOCX F7_Requerimientos_No_Funcionales_Colegio_Andino.docx: ZIP y XML válidos, imágenes presentes, sin campos vacíos de plantilla | OK | 0 imágenes |
| DOCX F8_Diagrama_Casos_de_Uso_Colegio_Andino.docx: ZIP y XML válidos, imágenes presentes, sin campos vacíos de plantilla | OK | 3 imágenes |

## 6. Rupturas y pendientes conocidos (historial y resolución)

La descripción original de la F27B se conserva y la resolución de la F27D se añade al lado.

| ID | Eslabón | Pendiente (F27B) | Estado (F27D) | Resolución |
|---|---|---|---|---|
| T-01 | AS-IS | Todo el AS-IS es **preliminar**: sin validación de RR. HH. ni de la Administración del Colegio | ACEPTADO / DOCUMENTADO | Se mantiene el rótulo en F2 a F4; no se afirman hechos institucionales |
| T-02 | AS-IS → problema | AS-01 no tiene un problema asociado | INFO, no bloqueante | No toda actividad es problemática |
| T-03 | Problema → solución | P5 se atiende **en parte**: los indicadores dependen de RF-28, un candidato no implementado | ACEPTADO | Declarado en F4, F5 y F6 |
| T-04 | TO-BE → RF | TB-F1 «cerrar sin selección» no tiene RF | RESUELTO (F27D, H-04) | TB-F1 desconectado del flujo como propuesta futura (A-30), sin condición del sistema |
| T-05 | TO-BE ← AS-IS | TB-30 (auditoría) no tiene actividad AS-IS de origen | INFO | Capacidad nueva y transversal; atiende P5 a través de S-05 (§2.3) |
| T-06 | RF → CU | La consulta de auditoría (RF-27) no tiene un CU académico propio | RESUELTO como DIFERIDO (F27D, H-11) | CU-21 diferido por decisión del equipo; RF-27 es transversal → UC-RF27, IN-08 |
| T-07 | CU | Los nombres de CU-01 a CU-20 los asignó la F27B | RESUELTO por decisión del equipo (F27D, H-12) | 20 CU aprobados; CU-18 renombrado a «Registrar decisión final humana» |
| T-08 | RNF | RNF-06 y RNF-07 no verificados; RNF-05, RNF-08 y RNF-09 con evidencia parcial | ACEPTADO | Criterios propuestos en el F7, sin umbrales inventados |
| T-09 | RNF ↔ catálogo técnico | La equivalencia no es 1:1 (10 académicos frente a 11 técnicos) | ACEPTADO | Unificarla es una decisión del equipo (F24 L-01) |
| T-10 | Diagramas | Los BPMN de F3 y F5 y la vista académica de F8 eran borradores con ambigüedades (MEDIUM en la F27C) | RESUELTO EN ESPECIFICACIÓN; pendiente de formalización en PowerDesigner | Especificaciones cerradas (H-01 a H-05, H-11 a H-13): READY FOR POWERDESIGNER en la F29 |
| T-11 | F9 | El F9 publicado no refleja el release, la QA de la F25 ni la resolución de los rótulos | CUBIERTO POR ADENDA | [Adenda post-release](../practica-09/F9_POST_RELEASE_ADDENDUM.md); el F9 no se modifica |
| T-12 | Problema → RF | RF-07 (TB-10) y RF-08 (TB-11) no aparecen en la relación problema → RF de §2.3 | RESUELTO / CONCILIADO (F27D, H-06) | La columna «Problema directo» muestra los problemas que F4 asigna a su actividad AS-IS (AS-06 → P1; AS-07 → P4). La columna «vía solución» queda vacía porque §2.3 no los incluye en ninguna solución. No se inventan relaciones |
