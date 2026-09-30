# Baseline académico — línea de trabajo F27+

Punto de partida verificado de la línea académica y documental que sigue al release técnico v1.1. Se estableció en la Fase 27B-0 (26/09/2026), en la rama `feature/phase-27-academic-f2-f11`.

## Proyecto

**Análisis y Diseño de una Plataforma SaaS Multiempresa para la Gestión del Reclutamiento, Evaluación y Selección de Personal – Caso de estudio: Colegio Andino de Huancayo**

## Curso

Pruebas y Calidad de Software — Universidad Continental

## NRC

28607

## Docente

Dr. Maglioni Arana Caparachin

## Equipo

- Coronacion Meza Fredy
- Peña Arroyo Anthony
- Vila Meza Luis Antonio

## Release técnico

**v1.1 publicado.** Verificado con Git en la F27B-0:

| Referencia | Valor |
|---|---|
| `v1.1.0-academic` | Etiqueta anotada que apunta a `634f354` («merge: release v1.1 academic»), que es `origin/main` |
| `origin/develop` | `c712539` («merge: close phase 26 release closeout»), base de esta rama |
| Árbol del código | `develop` y `main` comparten el mismo árbol, `4918cccaef87b9e06480100f8643a732d9f5c875` |
| `v1.0.0-academic` | Apunta a `9a946c2`, sin cambios |

- Las dos etiquetas están protegidas: no se mueven ni se reescriben.
- El GitHub Release no se verificó en esta fase, porque `gh` no está instalado.
- Roadmap técnico: Fases 0 a 26 cerradas. Detalle en [`../PROGRESS.md`](../PROGRESS.md) y [`../v1.1/phase-26-release-closeout.md`](../v1.1/phase-26-release-closeout.md).

## Baseline funcional

**RF-01 a RF-27**: conservan su número y su significado. Trazabilidad en [`../final-report/traceability-master.md`](../final-report/traceability-master.md).

La decisión final de selección es humana: la registra el Aprobador/Dirección con confirmación y justificación (RF-23). El sistema nunca selecciona, descarta ni contrata automáticamente.

## Extensiones

Candidatos en [`../v1.1/scope-preliminary.md`](../v1.1/scope-preliminary.md), sin promoción al baseline:

| Elemento | Estado |
|---|---|
| RF-28 | Candidato, **no implementado** |
| RF-29 | Implementado de forma **experimental**: estima el riesgo de demora del **proceso**. No evalúa, puntúa, ordena, selecciona ni descarta candidatos. Validado solo con datos sintéticos, no institucionalmente |
| RNF-C | **Propuesta** |
| RNF-A, RNF-B y RNF-D | **Propuestas** (accesibilidad, presupuesto de rendimiento y observabilidad), fuera de los 10 RNF académicos |

## Fuentes oficiales disponibles

**Formatos 02 a 09 y 11** (plantillas vacías) y **Guías 02 a 09 y 11**, en [`00-fuentes-oficiales/`](00-fuentes-oficiales/README.md). Hashes en su [inventario](00-fuentes-oficiales/inventory.md).

## Formato 11

**Histórico (Fases 27B-0 a 28).** El Formato 11 oficial no estaba disponible: la Guía 11 remitía a un «Formato 11: Arquitectura del sistema» cuya plantilla no se había recibido. Por eso la F28 elaboró el F11 como **adaptación académica explícita** de la Guía 11, identificada como tal ([`F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.docx`](practica-11/F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.docx)). Esa adaptación fue válida en esas condiciones, no es un error y se conserva sin cambios como evidencia histórica.

**Estado actual:**

- **Plantilla oficial:** se incorporó al repositorio el **29/09/2026** y está registrada como fuente **OFICIAL** en el [inventario](00-fuentes-oficiales/inventory.md). El 29/09/2026 es la fecha de incorporación al repositorio: no se conoce una fecha de publicación institucional.
- **Entregable definitivo actual:** la fase F11-R regularizó el entregable sobre esa plantilla. [`F11_Arquitectura_del_Sistema_Colegio_Andino.docx`](practica-11/F11_Arquitectura_del_Sistema_Colegio_Andino.docx) es el definitivo, con la misma arquitectura: CMP-01 a CMP-17 equivalentes a C01 a C17, R-01 a R-20 y ARQ-01. Registro en [`practica-11/F11R_REGULARIZACION.md`](practica-11/F11R_REGULARIZACION.md).
- **Validación:** interna y académica; no hay aprobación institucional.

**Reglas vigentes para el F11:**

- La arquitectura debe coincidir con el sistema implementado y con los modelos de la F22, la F23 y la F29 (ARQ-01). No se inventan componentes ni relaciones.
- Todo cambio del F11 se hace sobre la plantilla oficial.
- El F11 adaptado histórico no se modifica.

## Estado documental actual

| Formato | Estado |
|---|---|
| F2 a F8 | **Desarrollados en la F27B**, sobre las plantillas oficiales ([`practica-02`](practica-02/README.md) a [`practica-08`](practica-08/README.md)). **Pendientes de la auditoría F27C.** Los diagramas BPMN y de CU son borradores; se formalizan en PowerDesigner en la F29 ([worklist](POWERDESIGNER_WORKLIST.md)) |
| F9 | **Completo.** Entregable final v1.1 en [`phase-24/output/`](phase-24/README.md) (DOCX y PDF), con el histórico v1.0 y su [mapa de fuentes](phase-24/source-map.md). No se modifica; la [adenda post-release](practica-09/F9_POST_RELEASE_ADDENDUM.md) (F27B) registra el estado posterior y las divergencias resueltas |
| F29 | **Formalización en PowerDesigner** de F3, F5, F8 y ARQ-01 ([`powerdesigner/`](powerdesigner/README.md)): **CLOSED WITH DOCUMENTED OBSERVATIONS** (28/09/2026). F29 y F29B auditadas; las exportaciones formales son el diagrama principal de los DOCX y PDF de F3, F5, F8 y F11; hay 7 capturas reales de PowerDesigner. Los borradores quedan como DRAFT / SUPERSEDED BY F29 FORMAL EXPORT. LOW para la F31: F29-L01, F29-L02 y F29B-OBS-01. *Antes: FORMALIZED / DONE, pendiente de la auditoría F29* |
| F11 | **Regularizado sobre la plantilla oficial en la fase F11-R** (29/09/2026): [`F11_Arquitectura_del_Sistema_Colegio_Andino.docx`](practica-11/F11_Arquitectura_del_Sistema_Colegio_Andino.docx). Es la misma arquitectura, con CMP-01 a CMP-17 equivalentes a C01 a C17. **Pendiente de auditoría.** La adaptación académica de la F28 se conserva como versión histórica ([registro](practica-11/F11R_REGULARIZACION.md)). *Antes: adaptación académica desarrollada en la F28, sin plantilla oficial* |

**Insumos usados en la F27B** (trazabilidad completa en [`trazabilidad/F2-F9-traceability.md`](trazabilidad/F2-F9-traceability.md)):

- el análisis de requerimientos de la v1.0 ([`../final-report/04-requerimientos.md`](../final-report/04-requerimientos.md));
- los informes BPMN AS-IS y TO-BE, y el de casos de uso ([`../final-report/diagram-reports/`](../final-report/diagram-reports/));
- la especificación UML AS-IS de la F22 ([`../v1.1/uml/`](../v1.1/uml/README.md));
- los modelos de PowerDesigner de la F23 ([`../v1.1/powerdesigner/`](../v1.1/powerdesigner/README.md)).

**Regla de veracidad para F2 a F8.** Cada afirmación se clasifica como:

- hecho verificado;
- AS-IS preliminar;
- TO-BE propuesto;
- software implementado;
- elemento experimental.

Nada se presenta como «validado por la institución» sin evidencia explícita, y no se inventan hechos institucionales del Colegio Andino. Todos los datos son ficticios.

## Observaciones (F27B-0; vigentes en la F27B)

- **`CLAUDE.md` y `docs/PROGRESS.md` siguen en el estado previo al release** en la base `c712539`. Dicen que la etiqueta v1.1 no se ha creado y que la F26 está pendiente de auditoría. Esta fase no los modifica porque quedan fuera de su alcance. Conviene sincronizarlos en un cambio de gobierno autorizado. Detalle en [`GOVERNANCE_DEBT.md`](GOVERNANCE_DEBT.md).
- **La Guía 04 dice «Formato 43»** donde corresponde el Formato 04. Es una errata del original y no se corrige.
