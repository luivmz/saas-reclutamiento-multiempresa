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

**Formatos 02 a 09 y 11** (plantillas vacías) y **Guías 02 a 09 y 11**, en [`00-fuentes-oficiales/`](00-fuentes-oficiales/README.md). Hashes en su [inventario](00-fuentes-oficiales/inventory.md). Desde la F29C también la **guía de laboratorio E1** sobre desarrollo de software con IA y su equivalente **L1** (Taller de Investigación 2), en [`00-fuentes-oficiales/guias-ia/`](00-fuentes-oficiales/guias-ia/).

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
| F2 a F8 | **Desarrollados, auditados e integrados**, sobre las plantillas oficiales ([`practica-02`](practica-02/README.md) a [`practica-08`](practica-08/README.md)). Los diagramas BPMN de F3/F5 y los CU de F8 están formalizados en PowerDesigner y sus exportaciones se integran en los entregables ([worklist](POWERDESIGNER_WORKLIST.md)) |
| F9 | **Completo.** Entregable final v1.1 en [`phase-24/output/`](phase-24/README.md) (DOCX y PDF), con el histórico v1.0 y su [mapa de fuentes](phase-24/source-map.md). No se modifica; la [adenda post-release](practica-09/F9_POST_RELEASE_ADDENDUM.md) (F27B) registra el estado posterior y las divergencias resueltas |
| F29 | **Formalización en PowerDesigner** de F3, F5, F8 y ARQ-01 ([`powerdesigner/`](powerdesigner/README.md)): cerrada, auditada e integrada. En F31, F29-L02 queda RESUELTA; F29-L01 y F29B-OBS-01 quedan ACEPTADAS como metadata/limitación de herramienta sin impacto semántico |
| F11 | **Regularizado, auditado e integrado** sobre la plantilla oficial en F11-R: [`F11_Arquitectura_del_Sistema_Colegio_Andino.docx`](practica-11/F11_Arquitectura_del_Sistema_Colegio_Andino.docx). Mantiene CMP-01 a CMP-17 equivalentes a C01 a C17. La adaptación de F28 se conserva sin cambios como evidencia histórica ([registro](practica-11/F11R_REGULARIZACION.md)) |
| F29C | **Variables y matriz de operacionalización** auditadas e integradas ([`operacionalizacion/`](operacionalizacion/README.md)): VI, VD y cuatro variables intermedias; sin valores medidos y con VI → VD como TO-BE PROPUESTO |
| F29D–F29H | **Plan de pruebas, 128 casos, ejecución QA, defectos/métricas e informe final v1**, auditados e integrados en `5c52ad2`; sin aprobaciones institucionales inventadas ([`plan-pruebas/`](plan-pruebas/README.md), [`qa-final/`](qa-final/README.md), [`informe-final/`](informe-final/README.md)) |
| F30 | **Investigación científica y tecnológica para IA de reclutamiento**, auditada e integrada en `2bf2a1e`; investigación documental, no implementación ([`investigacion-ia/`](investigacion-ia/README.md)) |
| F31 | **CERRADA con observaciones aceptadas/futuras** tras auditoría final PASS WITH OBSERVATIONS; integración autorizada con gates CI. No cambia producto, RF, CU, RNF ni ML; commits e integración trazados en Git ([registro](F31_DOCUMENTATION_DEBT_CLEANUP.md)) |
| F32 | **CERRADA CON OBSERVACIONES e integrada** en `develop` `d6094187` y `main` `40a79ede`, con CI verde; auditoría global y salvaguardas documentales ([registro](auditoria-global/README.md)) |
| F33 | **CERRADA e integrada** como fase de diseño tras auditoría final **PASS**; commit académico `63a36e71a00881f3baa2d306f24a3f766ddf0882`, merge develop `288039fbb7eaba9827072e736d2fff4f55d10408` y merge main `26ae8b34ed586fe19515dd6041491e8dd72f9a64`. No modifica runtime, RF, CU, RNF ni ML ([entregables](diseno-inteligente/README.md)) |
| F34 | **CERRADA** tras auditoría final **PASS**: contrato, generador, validador y dataset **100 % sintético** de 19 CSV y 120 vacantes. Commits A `a4684d196e00fbe8fd3fdd2bea5b04d70f47bc70` y B `cafcbdbb81101fb40f91f0166019a1f5b9965de9`; publicación e integración autorizadas con gates CI y hashes finales en Git/GitHub. Sin cambios productivos ni aprobación de G0 ([entregables](datos-sinteticos/README.md)) |

**Gobernanza vigente tras F34 (04/10/2026):** **G0 = NO APROBADA**; **ADR-005 = PROPUESTA**. Cerrar el diseño o el dataset no aprueba el ADR ni autoriza implementación. **F34 CERRADA únicamente con datos sintéticos y gobernanza**, sin scoring ni recomendación de personas; **F35–F40 permanecen bloqueadas**. La alternativa B no usa dependencias nuevas ni extracción automática de documentos; C permanece futura y condicionada. Ningún estado de G0 ni el consentimiento autoriza datos reales: cualquier uso futuro exige autorización explícita adicional y revisión contractual, jurídica y de privacidad. RF-23 sigue siendo decisión humana y RF-29 experimental/informativa sobre el proceso. Criterios en [ADR-005](diseno-inteligente/F33_ADR_005_G0.md) y secuencia en el [mapa F34–F40](diseno-inteligente/F33_Mapa_F34_F40.md).

**Fotografías de entrega preservadas:** los documentos auditados F33 y F34 no se reescriben durante la publicación. Sus estados «pendiente de auditoría» y «LISTA PARA AUDITORÍA» corresponden a la entrega original; el estado de cierre vigente es el registrado en esta tabla y en [`../PROGRESS.md`](../PROGRESS.md).

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

## Observaciones históricas de F27B-0

- **Gobierno pre-release:** fue una deuda real de F27B-0. F31 sincroniza `CLAUDE.md`, `README.md` y `docs/PROGRESS.md` con el estado Git actual; el contexto original se conserva en [`GOVERNANCE_DEBT.md`](GOVERNANCE_DEBT.md).
- **La Guía 04 dice «Formato 43»** donde corresponde el Formato 04. Es una errata del original y no se corrige.
