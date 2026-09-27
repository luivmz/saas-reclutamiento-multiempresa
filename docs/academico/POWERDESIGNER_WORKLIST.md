# Lista de trabajo de PowerDesigner (líneas F27 a F29)

Qué diagramas académicos deben formalizarse en PowerDesigner y en qué orden.

**Durante la F27B no se abrió PowerDesigner.** No se modificaron `.oom` ni `.pdm`, ni ninguna de las 22 exportaciones de la F23. La formalización ocurre en la **F29**, solo después de que la auditoría **F27C** apruebe el contenido: AS-IS, TO-BE y casos de uso.

**Estados:**

| Estado | Significado |
|---|---|
| NO REQUERIDO | No necesita un diagrama nuevo |
| BORRADOR DISPONIBLE | Hay un borrador PNG de revisión en `practica-XX/diagramas/draft/` |
| REQUIERE POWERDESIGNER | Debe modelarse formalmente |
| READY FOR POWERDESIGNER | Especificación cerrada y corregida tras la F27C; lista para modelarse en la F29 sin reinterpretar nada |
| DEFER / F28 | Se decide en la F28, no antes. Usado hasta la F28 para el F11 |

**Actualización F28:** el F11 adaptado se desarrolló y su vista ARQ-01 quedó especificada.

**Actualización F27D:** tras la auditoría F27C se cerraron las especificaciones de F3 (H-01, H-02, H-13), F5 (H-03, H-04, H-05) y F8 (H-11, H-12 y la decisión del equipo sobre los CU).

| Práctica | Diagrama | Estado | Fuente | Acción | Prioridad |
|---|---|---|---|---|---|
| F2 | Flujo del proceso actual (símbolos básicos) | NO REQUERIDO · BORRADOR DISPONIBLE | [`practica-02/diagramas/draft/`](practica-02/diagramas/draft/) | Ninguna: la guía pide un diagrama de flujo y el BPMN formal es el de F3 | Baja |
| F3 | BPMN AS-IS preliminar | **READY FOR POWERDESIGNER** | [`practica-03/POWERDESIGNER_PENDING.md`](practica-03/POWERDESIGNER_PENDING.md) | Modelar 2 pools, 4 lanes, 14 tareas, SP-01 de instancia múltiple, 2 compuertas, 6 + 2 eventos y MF-01 a MF-04, según el glosario | **Alta** |
| F4 | BPMN AS-IS anotado con P1–P5 | NO REQUERIDO · BORRADOR DISPONIBLE | [`practica-04/diagramas/draft/`](practica-04/diagramas/draft/) | Derivarlo de F3 (anotaciones P1–P5) cuando exista el modelo formal | Media |
| F5 | BPMN TO-BE propuesto | **READY FOR POWERDESIGNER** | [`practica-05/POWERDESIGNER_PENDING.md`](practica-05/POWERDESIGNER_PENDING.md) | Modelar los dos niveles, SP-P, 10 compuertas (con GM1 y GM2), 9 eventos, MT-01 a MT-08 y TB-F1 desconectado | **Alta** |
| F8 | Casos de uso, vista académica (CU-01 a CU-20) | **READY FOR POWERDESIGNER** | [`practica-08/POWERDESIGNER_PENDING.md`](practica-08/POWERDESIGNER_PENDING.md) | Nuevo diagrama en un paquete propio, con CU-18 «Registrar decisión final humana» y sin CU-21 (diferido); **no** editar UC-01 | Media |
| F8 | UC-01 técnico (UC-RF01 a UC-RF29) | NO REQUERIDO | [`docs/v1.1/powerdesigner/`](../v1.1/powerdesigner/README.md) | Ninguna: se usa sin cambios como referencia | — |
| F11 | Arquitectura conceptual ARQ-01 (adaptación académica) | **READY FOR POWERDESIGNER** (condicionado a la auditoría de la F28) | [`practica-11/POWERDESIGNER_PENDING.md`](practica-11/POWERDESIGNER_PENDING.md) | Modelar 17 bloques en 6 agrupaciones y R-01 a R-20; C10 como decisión humana y C17 experimental y aislado; **no** editar CO-01, PK-01 ni DE-01 | Media |

## Reglas para la F29

1. **Modelos de la F23:** cada diagrama nuevo va en un modelo o paquete propio. No se modifican los diagramas de la F23 (22 vistas) ni sus exportaciones, salvo con una autorización explícita del equipo.
2. **Correspondencia:** el contenido debe coincidir uno a uno con el formato corregido en la F27D y aprobado en la reauditoría F27E: mismos IDs, actores, compuertas, eventos y mensajes.
3. **Exportación:** PNG y SVG. El borrador del formato se sustituye solo después de una nueva auditoría.
4. **Etiquetas de estado:** se mantienen. El AS-IS es «preliminar»; el TO-BE, «propuesto»; RF-29, «experimental»; TB-F1, «propuesta futura».
