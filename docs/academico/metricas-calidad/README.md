# F29G — Defectos y métricas de calidad

Registro final de defectos y métricas de calidad calculadas **solo con datos existentes**.

**Estado:** desarrollado en la fase F29G (30/09/2026), **pendiente de auditoría**.

| Archivo | Contenido |
|---|---|
| [`F29G_Defectos_y_Metricas.md`](F29G_Defectos_y_Metricas.md) | Registro de defectos (v1.0 y v1.1), métricas de ejecución, casos de prueba, cobertura funcional, defectos, estabilidad y evaluación con ISO/IEC 25010 como marco |

## Fuentes y límites

- **Defectos:**
  - v1.0: [`docs/defects.md`](../../defects.md).
  - v1.1: los documentos de fase ([F21](../../v1.1/phase-21-visual-qa.md), [F25](../../v1.1/phase-25-final-qa.md) y [F26](../../v1.1/phase-26-release-closeout.md)).
  - Además, las observaciones abiertas de la [F29F](../qa-final/README.md).
  - La ejecución F29F no produjo defectos nuevos del software.
- **Métricas:** de la [ejecución F29F](../qa-final/README.md) y de los [casos F29E](../casos-prueba/README.md).
- **Cobertura de código:** **NO MEDIDA**. El contenedor no tiene Xdebug ni PCOV y el proyecto nunca la midió. La «cobertura funcional» (RF con CP aprobado) es otra métrica.
- **ISO/IEC 25010:** se usa como marco de evaluación. No se declara certificación ni conformidad.
- **Métricas no calculables, por falta de datos:** densidad por KLOC, tiempo medio de corrección y defectos escapados a producción.

```
python docs/academico/tools/f27b/build.py f29g
```

Generador: [`f29g.py`](../tools/f27b/f29g.py) · registro de defectos: [`m_defectos.py`](../tools/f27b/m_defectos.py).
