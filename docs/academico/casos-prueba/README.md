# F29E — Casos de prueba

Catálogo formal de casos de prueba (CP-001 en adelante) y matriz de trazabilidad RF → CU → CP → prueba automatizada → evidencia. Aplica el [Plan de Pruebas (F29D)](../plan-pruebas/README.md).

**Estado vigente:** F29E **auditada, cerrada e integrada** ([baseline académico](../ACADEMIC_BASELINE.md)). El catálogo conserva la ejecución y los estados documentados de 30/09/2026; no se atribuyen nuevas ejecuciones al actualizar esta entrada.

| Archivo | Contenido |
|---|---|
| [`F29E_Casos_de_Prueba.md`](F29E_Casos_de_Prueba.md) | Catálogo con los campos de cada CP: ID, título, RF, CU, objetivo, precondiciones, datos, pasos, resultado esperado, tipo, prioridad, automatización, prueba asociada, comando, evidencia y estado |
| [`F29E_Matriz_Trazabilidad.md`](F29E_Matriz_Trazabilidad.md) | Cobertura de RF-01 a RF-27 (con sus CU) y casos transversales |
| [`F29E_Casos_de_Prueba.csv`](F29E_Casos_de_Prueba.csv) | Los mismos casos, para hojas de cálculo |

## Cómo se construyen (sin casos inventados)

- **PHPUnit:** un CP por clase de prueba y conjunto de RF del nombre del método (`test_rf10_rf11_…` → RF-10 y RF-11).
  - Los métodos sin prefijo RF forman un CP «reglas complementarias» con los RF que la [matriz maestra](../../final-report/traceability-master.md) asigna a la clase.
  - Si la clase no tiene RF asignados, el CP queda **transversal**: seguridad, multitenencia, ML o soporte.
- **Cypress, Vitest y pytest:** un CP por spec o archivo. Los RF de cada spec salen de la matriz maestra.
- **Estáticas y CI:** un CP para TypeScript, otro para el build, otro para Docker Compose y otro para la integración continua.
- **Manuales:** el recorrido visual de la Fase 8, con evidencia histórica, y tres casos **NO EJECUTADOS** con su razón: aceptación institucional, rendimiento (RNF-06) y disponibilidad (RNF-07). Se declaran `MANUAL / NO AUTOMATIZADO`.
- **Estado de cada CP:** se toma de la [ejecución F29F](../qa-final/README.md), desde sus archivos JUnit y registros.
- **Control de totales:** la suma de ejecuciones de todos los CP coincide con la ejecución real (419 PHPUnit, 85 Cypress, 42 Vitest y 533 pytest).

```
python docs/academico/tools/f27b/build.py f29e
```

Generador: [`f29e.py`](../tools/f27b/f29e.py) · lectura de fuentes: [`qa_data.py`](../tools/f27b/qa_data.py).
