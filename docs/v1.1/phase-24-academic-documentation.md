# Fase 24 — Documentación académica final: Formato 09

**Fecha:** 24 de septiembre de 2026
**Rama:** `feature/phase-24-academic-documentation` · **Base:** `8211851` (cierre de la Fase 23)
**Writer principal:** Claude Code · **Reviewer:** Codex (auditoría posterior)

> Fase **documental**. Produce el Formato 09 v1.1 a partir del trabajo académico que el equipo ya tenía y del estado real del sistema. No cambia código, pruebas, dependencias, rutas, migraciones, Policies, el servicio ML ni los modelos de PowerDesigner. RF-01 a RF-27 siguen siendo la línea base oficial; RF-28, RF-29 y RNF-C siguen siendo candidatos; RF-23 sigue siendo una decisión humana.

---

## 1. Objetivo

Actualizar, consolidar y cerrar el entregable académico *Formato 09 — Alcance del proyecto software*, sin crearlo desde cero: el documento que el equipo desarrolló en v1.0 se lleva al estado consolidado de v1.1, se completan los campos de la plantilla oficial que faltaban y se retiran las afirmaciones que ya no describen el sistema. En todo el documento se distinguen cuatro cosas: los hechos verificados, el AS-IS académico preliminar (pendiente de validación institucional), el TO-BE propuesto y lo implementado en el prototipo.

## 2. Baseline

| | |
|---|---|
| `develop` = `origin/develop` | `8211851dab47d52dc3fd41ff9baea64c96367a0b` (*merge: close phase 23 powerdesigner*) |
| `main` = `origin/main` | `4563c69` (v1.0 académica), sin cambios |
| `v1.0.0-academic` | `9a946c2`, intacto |
| Árbol al empezar | Limpio, salvo los tres DOCX de `docs/academico/phase-24/`, sin rastrear, que el equipo acababa de agregar (esperado) |
| Entorno | macOS, sin PowerDesigner. No hacía falta: F24 trabaja con las exportaciones versionadas de F23 |

## 3. Fuentes académicas

Las tres fuentes están en [`docs/academico/phase-24/`](../academico/phase-24/), se versionaron tal como llegaron (commit `a925053`) y no se modificaron. Sus SHA-256 son idénticos antes y después de la fase ([README](../academico/phase-24/README.md)).

| Fuente | Papel |
|---|---|
| `GUÍA PRÁCTICA 09.docx` | Guía oficial: instrucciones |
| `Formato 09 Alcance del proyecto software.docx` | Plantilla oficial: estructura y campos |
| `F9_Alcance_Proyecto_Software_Colegio_Andino_NRC30180.docx` | Documento histórico v1.0: base principal de contenido |

## 4. Guía oficial

La guía (NRC 28607, Dr. Maglioni Arana Caparachin, práctica en equipo) define el propósito: delimitar el alcance del proyecto y los límites del sistema. Pide cinco actividades: analizar el contexto, revisar los requerimientos, definir incluye y no incluye, delimitar los límites (entradas, salidas, actores externos y fronteras) y validar la coherencia del alcance. Los entregables son el contexto del sistema, las funcionalidades incluidas y las excluidas, los límites y el alcance validado. El entregable final los cubre en las secciones 3, 5, 6, 7 y 12.

## 5. Plantilla oficial

La plantilla tiene siete apartados, que el entregable cubre así (tabla completa en el propio documento, §1.4):

| Apartado de la plantilla | Sección del entregable |
|---|---|
| 1. Datos generales (nombre, integrantes, módulo/sistema, docente, fecha) | 1.2 |
| 2. Contexto (problema, objetivo general, usuarios principales, entorno de uso) | 3.1–3.5 y 4.1 |
| 3. Objetivos (general y específicos) | 4.1 y 4.2 |
| 4. Alcance (IN SCOPE con relación a requerimientos; OUT OF SCOPE con justificación) | 5 y 6 |
| 5. Límites (actores externos, entradas con fuente, salidas con destino) | 7.1, 7.4 y 7.5 |
| 6. Restricciones (tecnológicas, operativas, legales) y supuestos | 10.1–10.3 y 11.1 |
| 7. Criterios de aceptación (coherencia, claridad IN/OUT, viabilidad, ausencia de ambigüedades) | 12 y 12.1 |

## 6. Documento histórico utilizado

`F9_…_NRC30180.docx`, versión 1.0 del 20/09/2026: 22 páginas, 14 secciones y tres anexos (TO-BE, casos de uso de referencia y arquitectura conceptual). Su diseño se conserva: portada institucional, índice, encabezado con el logotipo, pie numerado, borde de página, títulos que abren página y tablas con cabecera azul. El entregable final se construyó **editando una copia de su `word/document.xml`**, sin reserializar el XML, con el script versionado [`tools/build.py`](../academico/phase-24/tools/build.py).

## 7. Diferencias detectadas

La inspección cruzó las tres fuentes con el estado de v1.1 (matriz completa, sección por sección, en [`source-map.md`](../academico/phase-24/source-map.md)):

| # | Diferencia | Tipo |
|---|---|---|
| D-01 | NRC 30180 en la portada, en 1.2, en CA-11, en 14.3 y en las propiedades del archivo; la guía y el proyecto usan **28607** | Dato académico incorrecto |
| D-02 | Faltaban campos de la plantilla: «Usuarios principales», «Entorno de uso», «Módulo / Sistema» y la columna «Destino» de las salidas; los cuatro criterios oficiales no aparecían de forma explícita | Cobertura de la plantilla |
| D-03 | Seis afirmaciones de ML obsoletas: Laravel no consume FastAPI, GAP-01 abierto, «eventual integración», dependencia bloqueada por GAP-01, «ausencia de integración con Laravel» y OUT-11 | Estado vigente incorrecto |
| D-04 | El anexo B (casos de uso) mostraba Administrador de la Organización, Superadministrador SaaS, suscripciones, banco de talentos, indicadores y reportes: contradice OUT-01 a OUT-07 y los cinco actores | Contradicción con el alcance |
| D-05 | El anexo C (arquitectura conceptual) mostraba SSO/MFA, suscripciones y planes, y los perfiles Administrador y Superadministrador | Contradicción con el alcance |
| D-06 | El anexo A (TO-BE) tiene una rama «cerrar sin selección» que el prototipo no implementa (RF-25 solo cierra con selección) | Propuesta frente a implementado |
| D-07 | Sin rastro de la evolución v1.1 (F13–F23) ni de los candidatos RF-28, RF-29 y RNF-C | Estado incompleto |
| D-08 | Catálogo de CU: el F9 usa CU-01 a CU-20; el informe del repositorio (`final-report/04-requerimientos.md` §4.4) agrupa en CU-01 a CU-13; el UML v1.1 usa un caso por RF | Divergencia de numeración (§15, O-02) |
| D-09 | Catálogo de RNF: el F9 usa RNF-01 a RNF-10 (seguridad, multitenencia, trazabilidad, privacidad…); el informe del repositorio usa RNF-01 a RNF-11 con otro reparto | Divergencia de numeración (§15, O-03) |

## 8. Correcciones

| Diferencia | Corrección en el entregable |
|---|---|
| D-01 | **NRC 28607** en la portada, en 1.2, en CA-11 y en las propiedades. La referencia 14.3 al informe «hasta el Capítulo 5» queda como documento histórico «referenciado en la versión 1.0 con el NRC anterior», sin repetir el número. El DOCX final no contiene «30180» en ninguna de sus partes (verificado, §14). Los originales no se tocaron |
| D-02 | Nuevas secciones 3.4, 3.5, 1.4 y 12.1; filas nuevas en 1.2; columna «Destino» en 7.5, con los destinatarios tomados de las notificaciones y Policies reales |
| D-03 | Reescritas 2 (párrafo 4), OUT-11, 6.1, 6.2, 11.2 y 14.2 con el estado vigente: integración experimental por HTTP interno autenticado, opcional y desactivada por defecto; ninguna frase obsoleta queda como estado vigente (ver el cuadro de frases retiradas en `source-map.md`) |
| D-04 | Anexo B sustituido por UC-01 de PowerDesigner |
| D-05 | Anexo C sustituido por CO-01 de PowerDesigner; nuevo anexo D con DE-01 |
| D-06 | Leyenda del anexo A: propuesta académica, no validada; la rama «cerrar sin selección» no está implementada. Nuevo anexo E (AC-01) como referencia complementaria del comportamiento verificado |
| D-07 | Nuevas 5.9 (evolución técnica F13–F23 y su efecto nulo sobre el alcance oficial) y 5.10 (candidatos); CA-13 y CA-14 |
| D-08, D-09 | **No se reconcilian**: el Formato conserva los catálogos académicos del equipo (20 CU y 10 RNF), que el encargo de la fase fija como oficiales. La divergencia se declara en el documento (11.1 y 13.2) y aquí; reconciliarlos es una decisión del equipo |

Historial del documento: se conserva la fila 1.0 y se añade la **1.1** (24/09/2026): «Actualización del Formato 09 al estado consolidado v1.1, incorporando trazabilidad UML/PowerDesigner y diferenciando la línea base académica de las capacidades experimentales. Corrige el NRC a 28607».

## 9. Tratamiento de RF-28

Candidato **descriptivo operacional**: el panel de seguimiento de convocatorias (etapas, tiempos y cuellos de botella, sin datos de personas). **No está implementado.** En el Formato aparece solo en 5.10 (candidato), OUT-07 (exclusión) y 6.2 (trabajo futuro), y en 13.2 como UC-RF28 `<<propuesto v1.1>>` sin asociaciones. No está en la tabla de RF de la sección 8, en ningún bloque IN ni en los criterios de línea base.

## 10. Tratamiento de RF-29

Candidato y **experimental**. Está implementado técnicamente e integrado en v1.1 (Fases 15 a 17): estima el riesgo de demora **del proceso**, no se persiste (SEQ-08: «nada se guarda en la base»), no es productivo, no evalúa, puntúa, selecciona ni descarta personas y no toca el ranking. No se incorpora a RF-01 a RF-27. El Formato lo documenta como evolución técnica experimental: resumen, 5.9, 5.10, la tabla de contrato de 6.1, OUT-11 (queda excluido su uso productivo o decisorio), 10.2, 10.3, CA-08 y 14.2. Contrato citado, sin cambios: frontera Laravel → HTTP interno autenticado → FastAPI; exactamente 15 variables operacionales, sin identificadores, PII, atributos sensibles ni texto libre; respuesta `risk_score`, `risk_flag`, `threshold`, `model_version`, `freeze_fingerprint` y `status`, **sin campo de incertidumbre**; Logistic Regression `C=10`, `class_weight=None`, `StandardScaler`, sin calibración; *freeze* `9ee1843055e75d4039dd84fd666db7a594e1a45ec7e9b354820fabfcb21ebcd2` y *threshold* `0.1679418172266036`. El detalle científico se remite a la documentación técnica de v1.1.

**RF-23** se mantiene de forma explícita: CA-07, 5.6, 10.2, 13.2 (SEQ-07 `<<human decision>>`, «ningún mensaje al ML») y 14.2. Ningún texto atribuye la selección, el descarte ni la decisión al ranking o al ML.

## 11. Tratamiento de RNF-C

Sigue siendo una **propuesta**. La Fase 20 autorizó e implementó una escena CSS 3D puntual en la portada, pero implementarla no promueve el requisito (`scope-preliminary.md`, pregunta 13). En el Formato aparece en 5.9 (F20, «RNF-C sigue siendo una propuesta»), 5.10 y 9.1. La tabla de RNF-01 a RNF-10 no cambia.

## 12. UML incorporado

Solo exportaciones versionadas de la Fase 23 ([`powerdesigner/exports/`](powerdesigner/exports/)). No se abrieron ni se modificaron los `.oom` ni el `.pdm`.

| Anexo | Diagrama | Archivo | Nota |
|---|---|---|---|
| B | UC-01 Casos de uso | `UC-01-casos-de-uso.png` | Copia girada 90° dentro del DOCX para ganar tamaño; el archivo de F23 no cambia |
| C | CO-01 Componentes | `CO-01-componentes.png` | — |
| D | DE-01 Despliegue | `DE-01-despliegue.png` | Girado 90° dentro del DOCX |
| E | AC-01 Proceso de reclutamiento | `AC-01-proceso-reclutamiento.png` | Complementa el TO-BE; no valida el AS-IS institucional |
| F | CL-01 Clases del dominio | `CL-01-clases-del-dominio.png` | — |

Se usó PNG porque los SVG de DE-01 y PDM-01 dependen de carpetas `*_svg_Files/` externas, que el DOCX no puede resolver. La trazabilidad RF → diagrama de la sección 13.2 del Formato reproduce la de `phase-23-powerdesigner.md` §11. El servicio ML aparece en UC-01 solo como actor técnico secundario `<<external service, experimental>>`; el Formato lo aclara en 7.1 y no lo cuenta entre los actores del alcance.

## 13. Artefactos finales

| Artefacto | Ruta |
|---|---|
| Formato 09 final (entregable) | [`docs/academico/phase-24/output/F9_Alcance_Proyecto_Software_Colegio_Andino_FINAL_v1.1.docx`](../academico/phase-24/output/F9_Alcance_Proyecto_Software_Colegio_Andino_FINAL_v1.1.docx) |
| PDF del entregable (Microsoft Word, 28 páginas) | [`docs/academico/phase-24/output/F9_Alcance_Proyecto_Software_Colegio_Andino_FINAL_v1.1.pdf`](../academico/phase-24/output/F9_Alcance_Proyecto_Software_Colegio_Andino_FINAL_v1.1.pdf) |
| README académico | [`docs/academico/phase-24/README.md`](../academico/phase-24/README.md) |
| Mapa de fuentes | [`docs/academico/phase-24/source-map.md`](../academico/phase-24/source-map.md) |
| Scripts de construcción y validación | [`docs/academico/phase-24/tools/`](../academico/phase-24/tools/) |

**PDF:** se generó sin instalar nada. Microsoft Word para Mac, ya instalado, exportó el DOCX por AppleScript (`tools/topdf.sh`). El PDF no contiene rutas locales ni el nombre de usuario; solo el productor («macOS Version 26.6.2»).

## 14. Validación

Solo se hicieron validaciones documentales y estructurales. **No se ejecutaron suites funcionales** (PHPUnit, Vitest, pytest ni Cypress): la fase no toca código y el QA global es de la Fase 25.

| Verificación | Cómo | Resultado |
|---|---|---|
| El DOCX abre | Microsoft Word lo abrió y lo exportó a PDF por AppleScript, sin diálogo de reparación | Correcto |
| XML | Las 43 partes `.xml`/`.rels` analizadas con `xml.dom.minidom` | Todas bien formadas |
| Páginas | PDF de Word, leído con PDFKit | 28 (la v1.0 exportada igual: 22) |
| Revisión visual | Las 28 páginas renderizadas y revisadas a ojo | Portada en una página, encabezado, pie, bordes y tablas intactos; sin desbordes |
| Tablas | 25 tablas; cada fila con tantas celdas como columnas | Correctas |
| Imágenes | 7 incrustadas (logotipo de la portada, anexos A a F), cada una con su relación y archivo | Correctas |
| Encabezados y pies | Referencias *default* y de primera página; campo `PAGE` | Conservados |
| Índice | Cada entrada comparada con la página real en el PDF | 15 de 15 coinciden |
| Secciones y campos oficiales | 17 secciones y 5 campos buscados en el texto | Todos presentes |
| NRC | Búsqueda en todas las partes del DOCX y en `core.xml` | Sin «30180»; «28607» presente |
| Nombres | Integrantes, docente, colegio y asignatura | Correctos |
| Frases obsoletas | «Laravel todavía no», «FastAPI no es consumido», «GAP-01 permanece abierto», «GAP-01 sigue abierto», «no existe cliente HTTP», «eventual integración», «ausencia de integración con Laravel», «mientras GAP-01», «F23 pendiente», «F23 no iniciada», «Fase 15C del servicio»; «GAP-01» en general | Ninguna |
| Marcadores | `TODO`, `TBD`, `XXX`, `FIXME`, «Lorem», «[pendiente]», «……» | Ninguno |
| Contrato ML | *Freeze*, *threshold* y seis campos de respuesta exactos; aclaración de que no hay incertidumbre | Correcto |
| RF y actores | RF-01 a RF-27 presentes; RF máximo citado RF-31, como candidato; cinco actores; sin «Administrador general» ni «Entrevistador independiente» | Correcto |
| Originales | SHA-256 antes y después | Idénticos |

Script: [`tools/validate_f9.py`](../academico/phase-24/tools/validate_f9.py), ejecutado sobre el DOCX y el texto del PDF finales: **sin fallos**. La primera ejecución marcó «TODO» por error, porque coincidía con la palabra española «todo»; se corrigió el script para que distinga mayúsculas y la repetición salió limpia.

**Límite de la validación:** el validador XSD de la skill `docx` (`scripts/office/validate.py`) no pudo ejecutarse. Requiere Python 3.10 o superior y `lxml`, y esta Mac tiene Python 3.9 sin `lxml`. No se instaló nada. Lo compensa que Word abre el archivo y lo exporta sin reparar nada, además de las comprobaciones anteriores.

## 15. Observaciones

| # | Observación | Tratamiento |
|---|---|---|
| O-01 | El NRC del documento histórico (30180) no era el vigente | Corregido en el entregable; el original se conserva con su NRC como evidencia |
| O-02 | Tres catálogos de CU conviven: el académico CU-01 a CU-20 (F9), CU-01 a CU-13 (informe del repositorio, cap. 4 §4.4, que advierte que el documento de casos de uso validado por el equipo «no está en el repositorio») y un caso por RF (UML v1.1) | Declarado en el Formato (11.1, 13.2). **Decisión del equipo**: reconciliar la numeración o mantener las tres vistas documentadas |
| O-03 | Dos catálogos de RNF: RNF-01 a RNF-10 (F9, académico) y RNF-01 a RNF-11 (informe del repositorio, cap. 4) | Se mantiene el académico como oficial, según el encargo. **Decisión del equipo** |
| O-04 | La columna «Firma» de 1.3 dice «Espacio reservado» | Intencional: es el lugar de la firma, no un contenido sin completar |
| O-05 | A tamaño de página, los diagramas de PowerDesigner se leen con dificultad en papel | UC-01 y DE-01 van girados 90°; las leyendas y el README remiten a los PNG y SVG de alta resolución de `docs/v1.1/powerdesigner/exports/` |
| O-06 | `docProps/app.xml` conserva las estadísticas del generador original (p. ej., `Pages` = 8) | No se tocó: Word las recalcula al guardar y no afectan al contenido |
| O-07 | La regla del mapa documental (§3) decía que el Formato 09 se actualiza «solo cuando el equipo apruebe requerimientos de v1.1» | El equipo encargó esta fase. El Formato **no añade ningún RF** a la línea base, así que la regla de numeración se respeta. Anotado en `documentation-update-map.md` |
| O-08 | GAP-01: el mapa documental preveía que el plazo operacional explícito necesitaría una entrada propia en el Formato 09 | Aparece como parte de la evolución experimental de RF-29 (5.9, F16: «plazo objetivo de cierre de la vacante»), **sin número de RF**, porque RF-29 no se promovió |
| O-09 | Pendientes de la Fase 21 que «pasan a F24/F25»: lector de pantalla real y rendimiento en un equipo modesto | No se ejecutaron: F24 es documental. **Pasan a F25** |
| O-10 | PowerDesigner no está instalado en esta Mac | No bloquea: se usaron las exportaciones versionadas |

## 16. Handoff a la Fase 25

La Fase 25 (QA global final) **no se inició**. Para quien la ejecute:

1. **Auditoría de Codex de F24.** Abrir el DOCX final en Word y comparar con el PDF; revisar `source-map.md`; ejecutar `tools/validate_f9.py`; confirmar los SHA-256 de los originales y que el diff no sale de `docs/`, `CLAUDE.md` y los documentos de gobierno.
2. **Regresión completa real**, que F24 no ejecutó: `php artisan test`, `npm run build`, `npx tsc --noEmit`, `npx vp test --run`, `pytest` del servicio ML y Cypress. La última cifra registrada es la de la Fase 21.
3. **Pendientes que llegan de la Fase 21:** lector de pantalla real y rendimiento en un equipo modesto (O-09).
4. **Decisiones del equipo:**
   - promoción de RF-28, RF-29 y RNF-C (preguntas 12 y 13);
   - reconciliación de los catálogos de CU y RNF (O-02, O-03);
   - `evaluation_criteria.position` en CL-01 y limpieza de los modelos de prueba de F23 en el equipo Windows (O-01 y O-04 de F23).
5. **Deudas aceptadas que siguen sin corregirse:**
   - descripción OpenAPI de GAP-01 en `schemas.py`;
   - metadatos con rutas absolutas en los modelos de PowerDesigner;
   - `critical` de SEQ-02 y rótulos `[sí]`/`[no]` de AC-01;
   - 21 diferencias justificadas entre F22 y PowerDesigner.
6. **Fase 26** (GitHub, *release* y cierre de v1.1): no iniciada. Ningún `push`, `merge`, *tag* ni *release* sin autorización.
