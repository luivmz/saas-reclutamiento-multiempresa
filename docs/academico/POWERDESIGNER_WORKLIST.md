# Lista de trabajo de PowerDesigner (líneas F27 a F29)

Qué diagramas académicos deben formalizarse en PowerDesigner y en qué orden.

**Durante la F27B no se abrió PowerDesigner.** No se modificaron `.oom` ni `.pdm`, ni ninguna de las 22 exportaciones de la F23. La formalización ocurre en la **F29**, solo después de que la auditoría **F27C** apruebe el contenido: AS-IS, TO-BE y casos de uso.

**Estados:**

| Estado | Significado |
|---|---|
| NO REQUERIDO | No necesita un diagrama nuevo |
| BORRADOR DISPONIBLE | Hay un borrador PNG de revisión en `practica-XX/diagramas/draft/` |
| REQUIERE POWERDESIGNER | Debe modelarse formalmente |
| LISTO PARA F29 | Especificación completa; solo espera la aprobación de la F27C |

| Práctica | Diagrama | Estado | Fuente | Acción | Prioridad |
|---|---|---|---|---|---|
| F2 | Flujo del proceso actual (símbolos básicos) | NO REQUERIDO · BORRADOR DISPONIBLE | [`practica-02/diagramas/draft/`](practica-02/diagramas/draft/) | Ninguna: la guía pide un diagrama de flujo y el BPMN formal es el de F3 | Baja |
| F3 | BPMN AS-IS preliminar | BORRADOR DISPONIBLE · REQUIERE POWERDESIGNER · **LISTO PARA F29** | [`practica-03/POWERDESIGNER_PENDING.md`](practica-03/POWERDESIGNER_PENDING.md) | Modelar el BPMN con 2 pools, 4 lanes, 14 tareas, 2 compuertas y 4 eventos; anotarlo como preliminar | **Alta** |
| F4 | BPMN AS-IS anotado con P1–P5 | NO REQUERIDO · BORRADOR DISPONIBLE | [`practica-04/diagramas/draft/`](practica-04/diagramas/draft/) | Derivarlo de F3 (anotaciones P1–P5 sobre las tareas) cuando exista el modelo formal | Media |
| F5 | BPMN TO-BE propuesto | BORRADOR DISPONIBLE · REQUIERE POWERDESIGNER · **LISTO PARA F29** | [`practica-05/POWERDESIGNER_PENDING.md`](practica-05/POWERDESIGNER_PENDING.md) | Modelar TB-01 a TB-30, 6 compuertas y TB-F1 como propuesta futura; decisión humana en el lane del Aprobador / Dirección | **Alta** |
| F8 | Casos de uso, vista académica (CU-01 a CU-20) | BORRADOR DISPONIBLE · REQUIERE POWERDESIGNER · **LISTO PARA F29** (tras O-F8-01) | [`practica-08/POWERDESIGNER_PENDING.md`](practica-08/POWERDESIGNER_PENDING.md) | Nuevo diagrama en un paquete propio; **no** editar UC-01 | Media |
| F8 | UC-01 técnico (UC-RF01 a UC-RF29) | NO REQUERIDO | [`docs/v1.1/powerdesigner/`](../v1.1/powerdesigner/README.md) | Ninguna: se usa sin cambios como referencia | — |
| F11 | Arquitectura conceptual (futuro) | REQUIERE POWERDESIGNER (pendiente de definición) | Guía 11; CO-01 y DE-01 de la F23 como insumo | Primero redactar el F11 como **adaptación académica** (no hay Formato 11 oficial), después modelarlo | Media |

## Reglas para la F29

1. **Modelos de la F23:** cada diagrama nuevo va en un modelo o paquete propio. No se modifican los diagramas de la F23 (22 vistas) ni sus exportaciones, salvo con una autorización explícita del equipo.
2. **Correspondencia:** el contenido debe coincidir uno a uno con el formato aprobado en la F27C: mismos IDs, actores, compuertas y eventos.
3. **Exportación:** PNG y SVG. El borrador del formato se sustituye solo después de una nueva auditoría.
4. **Etiquetas de estado:** se mantienen. El AS-IS es «preliminar»; el TO-BE, «propuesto»; RF-29, «experimental»; TB-F1, «propuesta futura».
