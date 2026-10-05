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
| F34A | **CERRADA** tras auditoría final **PASS**: paquete de readiness G0, matriz de 15 criterios, checklist jurídico, privacidad preliminar, instrumento institucional sin respuestas, 25 amenazas y 12 RF candidatos. Commits A `76d31b99661f78aaa413162ab6f55c726471a8cb` y B `003b502c35002f34931c1007c7e528abe4f0ef0a`; solo documentación, sin aprobaciones externas ni cambios productivos ([entregables](g0-readiness/README.md)) |
| F34B | **CERRADA** tras auditoría final **PASS**: formularios y matriz de evidencias externas, quórum/roles y fallo cerrado de los validadores. Commits A `c3d7c6de04a22a707e9893241b4dd712c221e642` y B `2cc2e49b27cc894b3a5edd7fcbff3a0050904645`; evidencias externas reales = 0; sin cambios productivos ([entregables](g0-evidence/README.md)) |
| F34C | **CERRADA** tras auditoría final **PASS**: cuatro adjuntos reales de tres integrantes, aprobación interna del equipo REGISTRADA y aceptación del threat model; G0-14/G0-09 CUMPLIDOS. ADR-005 canónico PROPUESTA y G0 NO APROBADA. Commits A `723001c13e193adace00650cf2c9296468483448` y B `c79fc24597ee0037978c9453df1eb762caf9497e`; sin cambios productivos ([entregables](g0-evidence/README.md)) |

**Estado vigente tras F34C (04/10/2026):** **F34C CERRADA** tras auditoría final **PASS**, sin cambios productivos. **G0-14 = CUMPLIDO; G0-09 = CUMPLIDO; ADR-005 canónico = PROPUESTA; aprobación interna del equipo = REGISTRADA; G0 = NO APROBADA. G0-02 = PENDIENTE EXTERNO; G0-03 = PENDIENTE EXTERNO; G0-12 = PENDIENTE EXTERNO; F35–F40 = BLOQUEADAS; datos reales PROHIBIDOS.** Hay cuatro adjuntos reales de tres integrantes: se documentan la copia histórica/restaurada de Luis y su confirmación adicional; no se confunden con aprobación jurídica, de privacidad ni institucional. RF-23 sigue humana; RF-29 experimental/informativa y RF-CAND fuera del baseline. Commits A `723001c13e193adace00650cf2c9296468483448` y B `c79fc24597ee0037978c9453df1eb762caf9497e`. Base preintegración: `develop` `619e1b217bf437376618b3eabd95d5013dba2f33`, `main` `b4d4d62456d437d313436eeffb4049f7d513d2cb`. Publicación autorizada con gates CI de develop/main; hashes de integración y resultados finales en Git/GitHub, sin anticiparlos. Sin nuevos tags ni releases.

**Fotografía histórica del cierre F34B (04/10/2026): F34B CERRADA; G0 = NO APROBADA; ADR-005 = PROPUESTA; evidencias externas reales = 0.** G0-02/03/12/14 siguen **PENDIENTE EXTERNO**, G0-09 **PARCIAL**, **F35–F40 = BLOQUEADAS** y los **datos reales siguen PROHIBIDOS**. Los formularios sin completar no son evidencia ni aprobación; el control positivo usa exclusivamente identidades y adjuntos sintéticos en memoria. RF-23 sigue humana y RF-29 experimental/informativa; RF-CAND sigue fuera del baseline. Base preintegración F34B: `develop` `417ea4fc4a800d8663e3af7909be59e6ea302f1e`, `main` `55bdb422e39b36983053cec9c0af398564f2c81a`. Integración autorizada con gates CI de develop/main, sin tag ni release; hashes finales en Git. Los documentos F34B se conservan como fotografía de entrega auditada («LISTA PARA AUDITORÍA»), sin completar ni simular firmas; el cierre documental no aprueba G0. Evidencias faltantes en la [decisión G0](g0-evidence/F34B_Decision_G0.md).

**Fotografía histórica del cierre F34A (04/10/2026): F34A CERRADA; G0 = NO APROBADA; ADR-005 = PROPUESTA.** G0-02/03/12/14 siguen **PENDIENTE EXTERNO**, G0-09 sigue **PARCIAL**, **F35–F40 = BLOQUEADAS** y los **datos reales siguen PROHIBIDOS**. Los nueve criterios CUMPLIDOS distinguen evidencia de diseño de implementación; G0-05 sigue NO APLICA para B. Para cerrar G0-02 se requiere evaluación de impacto COMPLETADA y documentada cuando aplica o conclusión jurídica fundamentada de NO APLICABILIDAD; una planificación no basta. La matriz y la aceptación del equipo no se completan automáticamente por esta fase. Base preintegración F34A: `develop` `1fb5a1f3663e10cc66289cb3530a8273d1b96b8f` y `main` `dc3093ea487a3694223f8f08560e390e26ec95c7`; publicación autorizada con gates CI, sin tag ni release. Los documentos F34A se conservan como fotografía de entrega auditada; su cierre documental no equivale a aprobar G0. Criterios pendientes en la [decisión de readiness](g0-readiness/F34A_Decision_Readiness_G0.md).

**Fotografía histórica tras F34 (04/10/2026):** **G0 = NO APROBADA**; **ADR-005 = PROPUESTA**. Cerrar el diseño o el dataset no aprueba el ADR ni autoriza implementación. **F34 CERRADA únicamente con datos sintéticos y gobernanza**, sin scoring ni recomendación de personas; **F35–F40 permanecen bloqueadas**. La alternativa B no usa dependencias nuevas ni extracción automática de documentos; C permanece futura y condicionada. Ningún estado de G0 ni el consentimiento autoriza datos reales: cualquier uso futuro exige autorización explícita adicional y revisión contractual, jurídica y de privacidad. RF-23 sigue siendo decisión humana y RF-29 experimental/informativa sobre el proceso. Criterios en [ADR-005](diseno-inteligente/F33_ADR_005_G0.md) y secuencia en el [mapa F34–F40](diseno-inteligente/F33_Mapa_F34_F40.md).

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
