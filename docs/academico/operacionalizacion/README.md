# F29C — Variables y matriz de operacionalización

Variables del proyecto, su matriz de operacionalización y el diseño conceptual que las relaciona. Siguen la guía de laboratorio **E1 «Desarrollo de Software con Inteligencia Artificial»** del curso. La **L1**, de Taller de Investigación 2 y con el mismo contenido, es fuente complementaria. Ambas están en [`../00-fuentes-oficiales/guias-ia/`](../00-fuentes-oficiales/guias-ia/) y figuran con su SHA-256 en el [inventario](../00-fuentes-oficiales/inventory.md).

**Estado vigente: AUDITADA, CERRADA E INTEGRADA** ([baseline académico](../ACADEMIC_BASELINE.md)). Se conserva el entregable del 30/09/2026 y su registro de evidencia sin reescribir respuestas históricas. `validate.py --cierre-f29c` pasa sin pendientes. La matriz, el diagrama y el anexo Word están desarrollados. La evidencia de ChatGPT P-01 a P-06 (R-01 a R-04, R-17 y R-18) está registrada literalmente como texto proporcionado por el equipo, sin enlace ni captura, e integrada frente a los capítulos 1 y 2 canónicos, que no se modificaron. Alcance efectivo según el **criterio docente informado por el equipo**: Gemini, DeepSeek, Copilot y el chat del docente, que la guía E1/L1 sí propone, quedan **NO REQUERIDOS** y no se ejecutaron.

- La matriz define qué se mide y con qué instrumento; **no contiene valores medidos**.
- No hay línea base del AS-IS y los cuestionarios Likert no se han aplicado.
- No hay validación institucional.

## Entregables

| Archivo | Contenido |
|---|---|
| [`F29C_Operacionalizacion_Variables.docx`](F29C_Operacionalizacion_Variables.docx) · [PDF](F29C_Operacionalizacion_Variables.pdf) | Documento Word con la cabecera institucional, en páginas horizontales: variables con su definición conceptual y operacional, relaciones, **Anexo 1. Matriz de Operacionalización de Variables**, trazabilidad de los indicadores y **Anexo 2. Diseño conceptual de variables**, como pide la guía |
| [`F29C_Operacionalizacion_Variables.md`](F29C_Operacionalizacion_Variables.md) | Espejo en Markdown, con el mismo contenido, para revisarlo en Git |
| [`diagramas/F29C_diagrama_conceptual_variables.png`](diagramas/F29C_diagrama_conceptual_variables.png) · [SVG](diagramas/F29C_diagrama_conceptual_variables.svg) | Diseño conceptual de variables, generado con Python (la guía propone código Python) |
| [`ACTIVIDAD_IA_COMPARACION.md`](ACTIVIDAD_IA_COMPARACION.md) | **Paquete de ejecución** (se genera). Distingue el requisito de la guía, el alcance efectivo del entregable, la evidencia ejecutada y lo no requerido. Incluye el protocolo y los prompts P-01 a P-06 listos para copiar |
| [`evidencias-ia/REGISTRO_EJECUCIONES_IA.md`](evidencias-ia/REGISTRO_EJECUCIONES_IA.md) | **Registro que completa el equipo:** ejecuciones de ChatGPT R-01 a R-04, R-17 y R-18, su integración con los capítulos 1 y 2 canónicos, y constancia NO REQUERIDO de R-05 a R-16 y de las comparaciones. El builder lo crea vacío solo si no existe y nunca lo sobrescribe |

## Resumen

| Variable | Tipo | Estado | Dimensiones |
|---|---|---|---|
| VI — Plataforma SaaS multiempresa de reclutamiento, evaluación y selección | Independiente (la solución) | SOFTWARE IMPLEMENTADO | 5 (S-01 a S-05 del F5) |
| VD — Gestión del proceso de reclutamiento, evaluación y selección | Dependiente (el problema) | AS-IS PRELIMINAR | 5 (P1 a P5 del F4 y OM-01 a OM-05 del F5) |
| VIN-1 — TDD y pruebas automatizadas | Intermedia (metodología) | HECHO VERIFICADO | 2 |
| VIN-2 — ISO/IEC 25010 como marco de referencia | Intermedia (norma) | HECHO VERIFICADO | 2 |
| VIN-3 — Arquitectura modular multiempresa y entorno reproducible | Intermedia (herramientas) | HECHO VERIFICADO | 2 |
| VIN-4 — Aprendizaje automático experimental (RF-29) | Intermedia (predicción) | EXPERIMENTAL / PROPUESTO | 2 |

**Reglas de la guía aplicadas:**

- Cada variable tiene al menos dos dimensiones, cada dimensión al menos dos indicadores y cada indicador al menos dos ítems.
- Los instrumentos son solo los de la guía: ficha de observación, lista de cotejo y cuestionario Likert.
- Los indicadores de la VD contienen las 15 variables que usa el modelo experimental de RF-29.

**Límites que se mantienen:**

- **Sin intermedias inventadas.** Scrum, DevOps y SOLID son ejemplos de la guía y no se incluyen: el proyecto no los documenta.
- **VI → VD sin efecto afirmado.** Es la hipótesis de trabajo (TO-BE PROPUESTO) y no se ha medido.
- **Decisión humana.** RF-29 estima el riesgo de demora del proceso y no evalúa personas. La decisión final es humana (RF-23).

## Cómo se genera y se valida

```
python docs/academico/tools/f27b/build.py f29c
powershell -ExecutionPolicy Bypass -File docs/academico/tools/f27b/topdf.ps1 docs/academico/operacionalizacion/F29C_Operacionalizacion_Variables.docx
python docs/academico/tools/f27b/validate.py                 # trabajo: PENDIENTE no es falla
python docs/academico/tools/f27b/validate.py --cierre-f29c   # cierre: PENDIENTE cuenta como falla
```

- **Modelo de contenido:** [`m_variables.py`](../tools/f27b/m_variables.py). El generador [`f29c.py`](../tools/f27b/f29c.py) produce el DOCX, el espejo Markdown, el diagrama y el registro de la actividad; ninguno se edita a mano.
- **DOCX:** reutiliza el paquete de la plantilla oficial del Formato 11 solo por su cabecera institucional y sus estilos. La plantilla no se modifica.
- **Validación:** el bloque «F29C» de `validate.py` comprueba:
  - las reglas de la guía;
  - que los RF, RNF, CU y variables de RF-29 citados existen;
  - que los estados pertenecen a la leyenda;
  - en un bloque aparte, la actividad según el alcance efectivo. Es FALLA si hay datos incoherentes, si algo NO REQUERIDO aparece como ejecutado o citado, o si la integración se escribe sin evidencia. Cada requisito efectivo sin evidencia completa queda PENDIENTE, y los no requeridos se informan como NO REQ;
  - que una regeneración produce los mismos bytes;
  - que no hay cambios fuera de alcance.
- **PDF:** se exporta con Microsoft Word, así que no forma parte de la comparación byte a byte.
