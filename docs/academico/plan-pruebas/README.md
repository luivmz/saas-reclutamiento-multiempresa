# F29D — Plan de Pruebas de Software

Plan maestro de pruebas de la plataforma v1.1 (rama `develop`, commit `bc44303`). Sigue la **plantilla del curso** [`Plantilla_de_Plan_de_Pruebas_de_Software.pdf`](../00-fuentes-oficiales/plan-pruebas/Plantilla_de_Plan_de_Pruebas_de_Software.pdf) y respeta su orden y sus 29 títulos, del historial de versiones al glosario.

**Estado vigente:** F29D **auditada, cerrada e integrada** ([baseline académico](../ACADEMIC_BASELINE.md)). El plan conserva su contenido y fecha de 30/09/2026; este cierre de auditoría no equivale a aprobación ni firma institucional.

- **Aprobación:** el plan **no está aprobado ni firmado**. La tabla de aprobaciones indica quién debe aprobarlo.
- **Validación institucional:** no la hay.

| Archivo | Contenido |
|---|---|
| [`F29D_Plan_de_Pruebas_Colegio_Andino.docx`](F29D_Plan_de_Pruebas_Colegio_Andino.docx) · [PDF](F29D_Plan_de_Pruebas_Colegio_Andino.pdf) | Plan de pruebas con portada, cabecera de la plantilla del curso y tabla de contenido |
| [`F29D_Plan_de_Pruebas_Colegio_Andino.md`](F29D_Plan_de_Pruebas_Colegio_Andino.md) | Espejo en Markdown, con el mismo contenido |
| [`F29D_REGISTRO.md`](F29D_REGISTRO.md) | Fuentes (con SHA-256), decisiones de generación y comandos |

## Qué fija el plan

- **Criterios de aceptación CA-01 a CA-07:** 0 fallos en PHPUnit, Cypress, Vitest y pytest; TypeScript y build sin errores; CI en verde; cada RF-01 a RF-27 con un caso de prueba automatizado aprobado; ningún defecto de severidad Alta abierto.
- **Criterios de suspensión y de reanudación.**
- **Riesgos R-01 a R-07.**
- **Cobertura de código:** no es criterio, porque no se mide con herramienta.
- **Fuera de alcance:** rendimiento (RNF-06), disponibilidad (RNF-07) y aceptación institucional quedan explícitamente como no probados.

Se aplica en los [casos de prueba (F29E)](../casos-prueba/README.md), la [ejecución QA (F29F)](../qa-final/README.md) y los [defectos y métricas (F29G)](../metricas-calidad/README.md).

## Generación

```
python docs/academico/tools/f27b/build.py f29d
powershell -ExecutionPolicy Bypass -File docs/academico/tools/f27b/topdf_toc.ps1 docs/academico/plan-pruebas/F29D_Plan_de_Pruebas_Colegio_Andino.docx
```

- **Contenido:** está en [`m_plan.py`](../tools/f27b/m_plan.py).
- **DOCX:** lo genera [`f29d.py`](../tools/f27b/f29d.py) con [`docxpkg.py`](../tools/f27b/docxpkg.py), porque la plantilla del curso solo existe en PDF.
- **Validación:** el bloque F29D de `validate.py` comprueba los títulos de la plantilla, que no haya aprobación simulada y que la regeneración dé los mismos bytes.
