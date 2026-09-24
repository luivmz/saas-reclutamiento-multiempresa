# Mapa de fuentes del Formato 09 v1.1

Origen de cada sección del entregable final ([`output/F9_Alcance_Proyecto_Software_Colegio_Andino_FINAL_v1.1.docx`](output/F9_Alcance_Proyecto_Software_Colegio_Andino_FINAL_v1.1.docx)) y qué cambió respecto de la versión 1.0 ([`F9_Alcance_Proyecto_Software_Colegio_Andino_NRC30180.docx`](F9_Alcance_Proyecto_Software_Colegio_Andino_NRC30180.docx)).

**Fuentes oficiales:** **G** = `GUÍA PRÁCTICA 09.docx` (actividades 1 a 5 y entregables) · **P** = `Formato 09 Alcance del proyecto software.docx` (apartados 1 a 7 de la plantilla) · **H** = F9 histórico v1.0.

**Estados:** **Conservado** (texto de H sin cambios) · **Actualizado** (texto de H corregido al estado v1.1) · **Nuevo** (no existía en H) · **Sustituido** (contenido de H reemplazado porque contradecía el alcance o el AS-IS verificado).

Las rutas técnicas son relativas a la raíz del repositorio.

## Portada e índice

| Sección final | Fuente oficial | Fuente técnica | Cambio realizado | Estado |
|---|---|---|---|---|
| Portada | H | `CLAUDE.md`, `README.md` (NRC 28607) | NRC 30180 → **28607**; se añade «Versión 1.1 · septiembre de 2026»; se quita una línea vacía para que la portada siga en una página | Actualizado |
| Tabla de contenido | H | Páginas medidas en el PDF exportado por Word (`docs/academico/phase-24/tools/toc.py`) | Números de página recalculados; «Anexos técnicos de referencia» → «Anexos A a F» | Actualizado |
| Propiedades del DOCX | — | — | Descripción «NRC 30180» → «NRC 28607 · Versión 1.1 (Fase 24)»; fecha de modificación | Actualizado |

## 1. Control del documento

| Sección final | Fuente oficial | Fuente técnica | Cambio realizado | Estado |
|---|---|---|---|---|
| 1.1 Historial de versiones | H | — | Se conserva la fila 1.0 y se añade la 1.1 (24/09/2026) con la descripción pedida por la fase | Actualizado |
| 1.2 Información del proyecto | **P §1** (nombre, integrantes, módulo/sistema, docente, fecha) | `docs/final-report/01-informacion-general.md` | NRC 28607; se añaden los campos oficiales «Nombre del proyecto», «Módulo / Sistema» e «Integrantes del equipo», además de versión, fecha y sistema de referencia | Actualizado |
| 1.3 Aprobaciones | H | — | Sin cambios. La columna «Firma» conserva «Espacio reservado» a propósito: es el lugar de la firma manuscrita | Conservado |
| 1.4 Correspondencia con el Formato 09 oficial | P (siete apartados) | — | Tabla campo oficial → sección del documento | Nuevo |
| 1.5 Convenciones de estado | G act. 5 (claridad) | `AGENTS.md` (AS-IS, TO-BE, implementado), `docs/v1.1/scope-preliminary.md` (leyenda) | Distingue lo verificado, el AS-IS preliminar, el TO-BE propuesto, lo implementado y lo experimental o candidato | Nuevo |

## 2. Resumen ejecutivo

| Sección final | Fuente oficial | Fuente técnica | Cambio realizado | Estado |
|---|---|---|---|---|
| Párrafos 1 y 3 | H | — | Sin cambios (alcance y decisión humana) | Conservado |
| Párrafo 2 | H | `docs/PROGRESS.md` (Fase 12) | Se precisa que la verificación de los 27 RF corresponde a la v1.0, en el QA final de la Fase 12 | Actualizado |
| Párrafo 4 (ML) | H | `docs/v1.1/phase-16-laravel-ml-integration.md`, `docs/PROGRESS.md` | **Se retira** «Laravel todavía no lo consume, GAP-01 permanece abierto». Se describen la evolución v1.1 (F13–F23) y la integración experimental, y se aclara que no amplía la línea base | Actualizado |
| 2.1 Resultado de la delimitación | H | — | Se añade una viñeta que remite a 5.9 y 5.10 | Actualizado |

## 3. Contexto y problema

| Sección final | Fuente oficial | Fuente técnica | Cambio realizado | Estado |
|---|---|---|---|---|
| 3.1 Contexto organizacional | P §2 (problema), G act. 1 | — | Sin cambios; el AS-IS sigue como reconstrucción preliminar | Conservado |
| 3.2 Problemas oficiales (P1–P5) | P §2 (problema), G act. 1 | — | Sin cambios | Conservado |
| 3.3 Respuesta propuesta | G act. 1 | — | Sin cambios | Conservado |
| 3.4 Usuarios principales | **P §2 (usuarios principales)**, G act. 1 | `app/Policies/*`, `docs/v1.1/uml/use-cases.md` | Campo oficial que faltaba en H: cinco actores y ningún usuario comercial ni decisor artificial | Nuevo |
| 3.5 Entorno de uso | **P §2 (entorno organizacional y tecnológico)**, G act. 1 | `package.json`, `composer.json`, `docker-compose.yml`, `docs/v1.1/uml/deployment-model.md` | Campo oficial que faltaba en H: entorno organizacional y tecnológico, con FastAPI experimental fuera de Compose | Nuevo |

## 4. Objetivos del sistema

| Sección final | Fuente oficial | Fuente técnica | Cambio realizado | Estado |
|---|---|---|---|---|
| 4.1 Objetivo general | P §2 y §3, G act. 1 | — | Sin cambios | Conservado |
| 4.2 Objetivos específicos | P §3 | — | Sin cambios | Conservado |
| 4.3 Indicadores de logro | H | — | Sin cambios | Conservado |

## 5. Alcance incluido

| Sección final | Fuente oficial | Fuente técnica | Cambio realizado | Estado |
|---|---|---|---|---|
| Tabla IN-01 a IN-08 | **P §4 (IN SCOPE)**, G act. 3 | `docs/final-report/traceability-master.md` | Cabeceras alineadas con la plantilla («Funcionalidad», «Descripción»); RF y CU = «relación con requerimientos». Filas sin cambios | Actualizado |
| 5.1 a 5.7 | H | — | Sin cambios | Conservado |
| 5.8 Estado técnico | H | `docs/PROGRESS.md` («Fase 12 — resultados reales del QA final») | Se identifica la v1.0 (tag `v1.0.0-academic`) y los resultados de la Fase 12 (27/27 RF; PHPUnit 244 = 236 + 8 omitidas, 0 fallidas; Cypress 43/43) | Actualizado |
| 5.9 Evolución técnica v1.1 | — | `docs/PROGRESS.md` (tabla v1.1 y entradas F18–F23), `docs/v1.1/phase-13…23-*.md` | Tabla F13–F23 con su efecto sobre el alcance oficial; resultados de la regresión de la **Fase 21** (Laravel 408 + 8, Python 532, 42 de componente, Cypress 20 specs / 84), rotulados como históricos y no reejecutados | Nuevo |
| 5.10 Candidatos de v1.1 | — | `docs/v1.1/scope-preliminary.md` §2, §3 y §7 (decisión 11, preguntas 12 y 13) | RF-28 (propuesta, no implementado), RF-29 (experimental, candidato) y RNF-C (propuesta), más la mención de RF-30, RF-31, RNF-A, RNF-B y RNF-D | Nuevo |

## 6. Alcance excluido

| Sección final | Fuente oficial | Fuente técnica | Cambio realizado | Estado |
|---|---|---|---|---|
| Tabla OUT-01 a OUT-11 | **P §4 (OUT OF SCOPE)**, G act. 3 | `docs/v1.1/scope-preliminary.md`, `docs/v1.1/phase-16-laravel-ml-integration.md` | Cabecera «Funcionalidad excluida». OUT-07 menciona RF-28 como candidato. **OUT-11 reescrito**: antes «FastAPI no es consumido por Laravel… GAP-01 sigue abierto»; ahora «uso productivo o decisorio del riesgo operacional ML (RF-29)». Once exclusiones, como en H | Actualizado |
| 6.1 Tratamiento del componente ML | H | `config/ml.php` (`enabled` falso por defecto, *threshold*), `app/Policies/VacancyPolicy.php` (`viewOperationalRisk`), `docs/v1.1/uml/sequence-diagrams.md` SEQ-08 («nada se guarda en la base»), `ml-service/src/recruitment_ml/api/schemas.py` (respuesta), `CLAUDE.md` (contrato congelado) | **Se retira** «su eventual integración exige resolver GAP-01». Se describen el estado vigente, la tabla del contrato (frontera, 15 variables, seis campos, sin incertidumbre, modelo, *freeze*, *threshold*) y las prohibiciones | Actualizado |
| 6.2 Trabajo futuro | H | `docs/v1.1/scope-preliminary.md`, `docs/v1.1/phase-21-visual-qa.md` (lector de pantalla y rendimiento, que pasan a F24/F25) | Viñetas alineadas con los candidatos reales; se retira «integración opcional del riesgo operacional», que ya existe como experimental | Actualizado |

## 7. Límites del sistema

| Sección final | Fuente oficial | Fuente técnica | Cambio realizado | Estado |
|---|---|---|---|---|
| 7.1 Actores externos | **P §5 (actores externos)**, G act. 4 | `docs/v1.1/uml/use-cases.md` | Tabla sin cambios (cinco actores); se añade una nota: el servicio ML es un actor técnico secundario del UML, no un actor del alcance | Actualizado |
| 7.2 Componentes internos | G act. 4 (fronteras) | `app/Models/Concerns/BelongsToOrganization.php`, `app/Policies/*`, `database/migrations` (sin RLS), `docs/v1.1/uml/component-model.md` | Se añade: monolito modular, multitenencia lógica sin RLS ni microservicios; y un párrafo sobre la frontera técnica experimental de FastAPI | Actualizado |
| 7.3 Frontera organizacional | G act. 4 | — | Sin cambios | Conservado |
| 7.4 Entradas | **P §5 (entradas, fuente)** | — | Sin cambios | Conservado |
| 7.5 Salidas | **P §5 (salidas, destino)** | `app/Services/**` (destinatarios de `notify`), `app/Policies/VacancyPolicy.php` (ranking) | **Se añade la columna oficial «Destino»**, que faltaba en H | Actualizado |

## 8 a 10. Línea base y restricciones

| Sección final | Fuente oficial | Fuente técnica | Cambio realizado | Estado |
|---|---|---|---|---|
| 8. Línea base funcional RF-01 a RF-27 | G act. 2 | `docs/final-report/traceability-master.md` | Tabla **sin cambios** (número, nombre y significado congelados); el párrafo aclara que RF-28 y RF-29 son candidatos y no están en la tabla | Actualizado (solo el párrafo) |
| 9. Línea base no funcional RNF-01 a RNF-10 | G act. 2 | — | Tabla sin cambios | Conservado |
| 9.1 Criterio de aplicación | H | `docs/v1.1/scope-preliminary.md` §3 y pregunta 13 | Se añade: RNF-A a RNF-D son candidatos y RNF-C sigue siendo propuesta pese a la escena de la Fase 20 | Actualizado |
| 10.1 Tecnológicas | **P §6 (tecnológicas)** | `package.json` (React 19, Inertia 3, Tailwind 4), `components.json` (shadcn), `CLAUDE.md` | Stack completo; multitenencia sin RLS; FastAPI experimental fuera de Compose | Actualizado |
| 10.2 Operativas | **P §6 (operativas)** | `docs/v1.1/uml/sequence-diagrams.md` SEQ-08 | Se añade que RF-29 es informativo | Actualizado |
| 10.3 Privacidad, seguridad y legales | **P §6 (legales)** | `ml-service/src/recruitment_ml/api/schemas.py` (`extra="forbid"`) | Se añade la restricción de datos del servicio ML | Actualizado |

## 11 a 14. Supuestos, criterios, trazabilidad y cierre

| Sección final | Fuente oficial | Fuente técnica | Cambio realizado | Estado |
|---|---|---|---|---|
| 11.1 Supuestos | **P §6 (supuestos)** | `docs/v1.1/scope-preliminary.md` (decisión 11), `docs/final-report/04-requerimientos.md` §4.4 | Se añaden dos supuestos: los candidatos no se promueven al implementarse y el catálogo CU-01 a CU-20 es académico | Actualizado |
| 11.2 Dependencias | H | `config/ml.php`, `docs/v1.1/phase-23-powerdesigner.md` | Fila «Gobierno de ML» reescrita (antes: «mientras GAP-01 siga abierto»); nueva fila sobre los modelos de PowerDesigner | Actualizado |
| 11.3 Riesgos | H | `docs/v1.1/architecture-decisions/ADR-001…`, `ADR-002…` | Mitigación del riesgo ML con el contrato de 15 variables; nuevo riesgo «confundir la evolución v1.1 con una ampliación del alcance» | Actualizado |
| 12. Criterios CA-01 a CA-14 | **P §7**, G act. 5 | — | CA-07 cita RF-23; CA-08 reescrito (RF-29 experimental); CA-11 con **NRC 28607** (antes 30180); nuevos CA-13 (evolución v1.1) y CA-14 (evidencia de modelado) | Actualizado |
| 12.1 Correspondencia con los criterios del Formato 09 | **P §7** (coherencia, claridad IN/OUT, viabilidad, ausencia de ambigüedades) | — | Los cuatro criterios oficiales, explícitos y vinculados a los CA | Nuevo |
| 13. Trazabilidad y 13.1 Matriz compacta | H | — | Sin cambios | Conservado |
| 13.2 Correspondencia con el UML AS-IS v1.1 | — | `docs/v1.1/phase-23-powerdesigner.md` §11, `docs/final-report/04-requerimientos.md` §4.4 | Trazabilidad RF → diagramas de PowerDesigner; se registra la divergencia de numeración de CU (observación O-02 de la fase) | Nuevo |
| 14.1 Procedimiento de cambio | H | — | Sin cambios | Conservado |
| 14.2 Conclusión | H | `docs/v1.1/phase-16-…`, `phase-22-…`, `phase-23-…` | Párrafo 2: **se retira** «mientras subsistan GAP-01, la ausencia de integración con Laravel…»; se describe la integración experimental y se reafirma RF-23 | Actualizado |
| 14.3 Referencias | H | `docs/v1.1/architecture-decisions/` | La referencia al informe con «NRC 30180» se marca como histórica, sin repetir el número; se añaden el informe del repositorio, ADR-003 y la documentación de v1.1; se retira «Fase 15C» como única fuente del ML | Actualizado |

## Anexos

| Sección final | Fuente oficial | Fuente técnica | Cambio realizado | Estado |
|---|---|---|---|---|
| Anexo A. Proceso TO-BE propuesto | H | `docs/PROGRESS.md` (regla 6: RF-25 solo cierre con selección) | Misma imagen; la leyenda aclara que es una propuesta académica no validada y que la rama «cerrar sin selección» no está implementada | Actualizado |
| Anexo B. Casos de uso (UC-01) | G act. 4 (representar el límite) | `docs/v1.1/powerdesigner/exports/UC-01-casos-de-uso.png` | **Sustituye** la vista de H, que incluía Administrador de la Organización, Superadministrador SaaS, suscripciones, banco de talentos, indicadores y reportes. Girado 90° | Sustituido |
| Anexo C. Componentes (CO-01) | G act. 4 | `docs/v1.1/powerdesigner/exports/CO-01-componentes.png` | **Sustituye** la arquitectura conceptual de H, que mostraba SSO/MFA, suscripciones y planes, y los perfiles Administrador y Superadministrador | Sustituido |
| Anexo D. Despliegue (DE-01) | — | `docs/v1.1/powerdesigner/exports/DE-01-despliegue.png` | Girado 90° | Nuevo |
| Anexo E. Actividad (AC-01) | — | `docs/v1.1/powerdesigner/exports/AC-01-proceso-reclutamiento.png` | Complementa el TO-BE del anexo A; no es una validación institucional del AS-IS | Nuevo |
| Anexo F. Clases (CL-01) | — | `docs/v1.1/powerdesigner/exports/CL-01-clases-del-dominio.png` | 17 clases y 37 asociaciones | Nuevo |

## Frases del documento histórico retiradas como estado vigente

| Frase en H | Ubicación en H | Tratamiento |
|---|---|---|
| «Laravel todavía no lo consume, GAP-01 permanece abierto» | 2, párrafo 4 | Reescrita (integración experimental vigente desde la Fase 16) |
| «FastAPI no es consumido por Laravel… GAP-01 sigue abierto» | OUT-11 | Reescrita |
| «Su eventual integración exige resolver GAP-01…» | 6.1 | Reescrita |
| «Integración opcional del riesgo operacional del proceso» (trabajo futuro) | 6.2 | Sustituida por la validación institucional de RF-29 |
| «Bloquea cualquier integración… mientras GAP-01 siga abierto» | 11.2 | Reescrita |
| «…mientras subsistan GAP-01, la ausencia de integración con Laravel…» | 14.2 | Reescrita |
| «NRC 30180» | Portada, 1.2, CA-11, 14.3, propiedades | 28607; en 14.3 queda como referencia histórica, sin el número |
| «Documentación de Fase 15C del servicio FastAPI experimental» | 14.3 | Sustituida por la documentación de las Fases 15 a 17, 22 y 23 |
