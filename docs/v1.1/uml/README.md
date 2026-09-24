# UML AS-IS de v1.1

Especificación UML del sistema **tal como está implementado** en `develop` (`aced6da`, Fase 22, 23/09/2026). Documento de la fase: [`../phase-22-uml-update.md`](../phase-22-uml-update.md).

Estos archivos son la **especificación** de los diagramas. La formalización gráfica en PowerDesigner es la Fase 23. Los `.puml` de [`puml/`](puml/) son borradores textuales para revisar y orientar esa formalización: **no sustituyen a PowerDesigner** y no se renderizaron en esta fase.

## Cómo leer esta carpeta

| Orden | Documento | Qué contiene |
|---|---|---|
| 1 | [`uml-inventory.md`](uml-inventory.md) | Inventario verificado contra el código: actores, módulos, entidades, estados, integraciones, despliegue y lo que **no** existe. Base de todo lo demás |
| 2 | [`use-cases.md`](use-cases.md) | UC-01: RF-01 a RF-29, actores, `<<include>>`/`<<extend>>` justificados |
| 3 | [`class-model.md`](class-model.md) | CL-01: 17 clases, 37 asociaciones con multiplicidad, multiempresa, enums |
| 4 | [`component-model.md`](component-model.md) | CO-01 componentes y PK-01 paquetes, con la frontera Laravel ↔ FastAPI |
| 5 | [`deployment-model.md`](deployment-model.md) | DE-01: contenedores reales y servicio de inferencia fuera de Compose |
| 6 | [`sequence-diagrams.md`](sequence-diagrams.md) | SEQ-01 a SEQ-08: flujos críticos |
| 7 | [`activity-diagrams.md`](activity-diagrams.md) | AC-01 proceso completo y AC-02 riesgo operacional |
| 8 | [`state-diagrams.md`](state-diagrams.md) | ST-01 a ST-04: requerimiento, vacante, postulación y sesiones |
| 9 | [`traceability-matrix.md`](traceability-matrix.md) | RF ↔ UML ↔ clase ↔ código ↔ pruebas, roles y permisos, discrepancias |
| 10 | [`powerdesigner-handoff.md`](powerdesigner-handoff.md) | Guía práctica para F23: orden, fichas por diagrama, exclusiones |

## Convenciones

- **AS-IS** = implementado y probado. **Experimental** = implementado, no productivo (`<<experimental>>`). **Candidato** = no implementado (`<<propuesto v1.1>>`).
- Nombres técnicos idénticos al código; etiquetas en español para la lectura.
- Toda afirmación cita su fuente (`archivo`, método o migración). Lo que no se pudo verificar se marca como pendiente de confirmación.
