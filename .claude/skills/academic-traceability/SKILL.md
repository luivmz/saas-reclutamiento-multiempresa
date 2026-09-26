---
name: academic-traceability
description: Trazabilidad y entregables académicos del proyecto. Úsala al actualizar la matriz RF ↔ código ↔ pruebas ↔ UML ↔ Docker, al redactar capítulos del informe, al registrar evidencia TDD o defectos, y al preparar el Formato 09. Define qué evidencia es admisible y cómo preservar la historia de v1.0.
---

# Trazabilidad académica

Este proyecto se evalúa por su evidencia, no por sus afirmaciones. Una funcionalidad sin trazabilidad cuenta como no entregada, y una trazabilidad sin respaldo real es peor que no tenerla.

## La cadena completa

Cada requerimiento debe poder recorrerse entero:

```
RF-NN → regla de negocio (docs/assumptions.md)
      → código (ruta, Form Request, Controller, Policy, Service, Modelo, migración)
      → pruebas (PHPUnit test_rfNN_*, spec Cypress si aplica)
      → evidencia TDD (RED observado → GREEN)
      → diagrama UML que lo representa
      → entorno donde se ejecuta (Docker)
      → Formato 09
```

Si un eslabón falta, se declara faltante. No se rellena con una suposición.

## Dónde vive cada cosa

| Documento | Contenido |
|---|---|
| `docs/final-report/traceability-master.md` | Matriz maestra RF ↔ todo lo demás |
| `docs/rf-implementation-matrix.md` | RF ↔ archivos de implementación |
| `docs/tdd-evidence.md` | Ciclos RED/GREEN con salida real |
| `docs/defects.md` | DEF-NN: síntoma, causa, corrección, prueba que lo cubre |
| `docs/assumptions.md` | A-NN: supuestos de negocio con su justificación |
| `docs/final-report/01..14` | Capítulos del informe |
| `docs/final-report/diagram-reports/` | Informes escritos de los diagramas |
| `docs/final-report/evidence-index.md` | Índice de toda la evidencia |
| `docs/PROGRESS.md` | Estado por fase |

Numeración continua: los RF siguen desde RF-28, los supuestos desde A-37, los defectos desde DEF-14. Nunca se reutiliza un número retirado.

## Evidencia admisible

- **Resultados de pruebas**: solo los de una ejecución real, con el conteo exacto que devolvió el comando. Si no se ejecutó, se escribe "no ejecutado en esta sesión".
- **Capturas y salidas**: de este proyecto y de datos ficticios.
- **Métricas**: solo si se midieron. Nada de cifras de rendimiento, cobertura o precisión estimadas a ojo.
- **Escenarios**: siempre ficticios. Los candidatos, correos, DNI y CV de los ejemplos son inventados y deben parecerlo.
- **Citas de código**: `archivo:línea` verificado, no recordado.

Si un dato no se puede verificar en el momento, se marca como pendiente y se dice en el reporte. Una tabla con un hueco honesto vale más que una tabla completa e inventada.

## Preservar v1.0

- Los documentos históricos (informe final, reporte QA, checklist de entrega, informes de diagramas) **no se reescriben**. Lo que v1.1 cambie se anota como evolución, no como corrección del pasado.
- El tag `v1.0.0-academic` es la línea base histórica y no se mueve.
- Si un documento de v1.0 contradice el estado actual, **se señala la contradicción** en `docs/v1.1/documentation-update-map.md` indicando documento, sección y diferencia. No se edita silenciosamente el documento antiguo.
- Los documentos nuevos de v1.1 viven en `docs/v1.1/`.

## Al cerrar un cambio

1. Fila de la matriz maestra actualizada (RF, archivos, pruebas, diagrama, estado).
2. Evidencia TDD con la salida real del RED y del GREEN.
3. Defecto registrado si apareció uno, con severidad y prueba de regresión.
4. Supuesto registrado si se tomó una decisión de negocio nueva.
5. `docs/PROGRESS.md` con el estado y el siguiente paso.
6. Enlaces relativos verificados: un enlace roto en el informe es un defecto de entrega.
