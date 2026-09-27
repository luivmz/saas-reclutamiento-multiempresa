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

**Formatos 02 a 09** (plantillas vacías) y **Guías 02 a 09 y 11**, en [`00-fuentes-oficiales/`](00-fuentes-oficiales/README.md). Hashes en su [inventario](00-fuentes-oficiales/inventory.md).

## Formato 11

**No disponible oficialmente.** La Guía 11 («arquitectura conceptual del sistema») remite a un «Formato 11: Arquitectura del sistema», pero esa plantilla no se recibió.

## Regla para el F11 futuro

- **Forma:** el F11 se crea como **adaptación académica explícita** del equipo, basada en la Guía 11 y en la estructura común de los Formatos 02 a 09. Nunca se presenta como plantilla oficial.
- **Identificación:** el propio documento dirá que es una adaptación y por qué, y figurará como GENERADO en el inventario.
- **Contenido:** la arquitectura que describa debe coincidir con el sistema implementado y con los modelos de la F22 y la F23. No se inventan componentes.

## Estado documental actual

| Formato | Estado |
|---|---|
| F2 a F8 | **Desarrollados en la F27B**, sobre las plantillas oficiales ([`practica-02`](practica-02/README.md) a [`practica-08`](practica-08/README.md)). **Pendientes de la auditoría F27C.** Los diagramas BPMN y de CU son borradores; se formalizan en PowerDesigner en la F29 ([worklist](POWERDESIGNER_WORKLIST.md)) |
| F9 | **Completo.** Entregable final v1.1 en [`phase-24/output/`](phase-24/README.md) (DOCX y PDF), con el histórico v1.0 y su [mapa de fuentes](phase-24/source-map.md). No se modifica; la [adenda post-release](practica-09/F9_POST_RELEASE_ADDENDUM.md) (F27B) registra el estado posterior y las divergencias resueltas |
| F11 | **Pendiente.** No hay plantilla oficial (ver la regla anterior) |

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
