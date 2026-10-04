# Generador de los Formatos 02 a 08 (Fase 27B)

Genera los entregables académicos F2 a F8 a partir de **un único modelo de datos**. De él salen el DOCX, su espejo en Markdown, los borradores de diagramas y la trazabilidad, así que no pueden contradecirse.

| Archivo | Función |
|---|---|
| `m_common.py` | Datos generales, leyenda de estados (hecho verificado, AS-IS preliminar, TO-BE propuesto, implementado, experimental) y reglas fijas |
| `m_asis.py` | AS-IS preliminar: actividades AS-01 a AS-14, actores, observaciones y elementos BPMN (F2 y F3) |
| `m_problems.py`, `m_tobe.py` | Problemas P1 a P5 (F4) y TO-BE TB-01 a TB-29 (F5) |
| `m_rf.py`, `m_rnf.py`, `m_cu.py` | RF-01 a RF-27 y extensiones (F6), RNF-01 a RNF-10 con su equivalencia técnica (F7) y casos de uso (F8) |
| `docxgen.py` | Rellena una **copia en memoria** de la plantilla oficial (estilos, cabecera con el logotipo, numeración y página) y escribe el espejo Markdown |
| `diagrams.py` | Borradores PNG con Pillow: flujo, BPMN con carriles verticales y casos de uso. Llevan la marca «BORRADOR» |
| `build.py` | Construye las claves vigentes indicadas; sin argumentos excluye `f11`. Para arquitectura oficial: `python docs/academico/tools/f27b/build.py f11r` |
| `validate.py` | Comprobaciones de coherencia F2→F9 (§17 del encargo) y de integridad de los DOCX |
| `topdf.ps1` | Exporta DOCX a PDF con Microsoft Word, la misma herramienta que usó la F24 |

## Reglas

- **Plantillas oficiales:** las de [`00-fuentes-oficiales`](../../00-fuentes-oficiales/README.md) **solo se leen**.
- **Borradores:** los PNG de `practica-XX/diagramas/draft/` no son modelos de PowerDesigner. La formalización está en [`POWERDESIGNER_WORKLIST.md`](../../POWERDESIGNER_WORKLIST.md).
- **Salida reproducible:** las fechas internas del ZIP son fijas, así que el mismo modelo da el mismo DOCX. Por eso los hashes de `evidencias/` son estables.
- **Dependencias:** Python 3.12 con Pillow y Microsoft Word para el PDF. No se instalaron herramientas nuevas.
- **Historia F11 (F32-M01):** `f11` está bloqueada, incluso por llamada directa; un lote que la incluya se rechaza antes de ejecutar cualquier builder. Se conserva su fuente como antecedente, no como ruta ejecutable. `f11r` es la única clave vigente para el Formato 11. El DOCX/PDF/MD adaptado y sus registros no se sobrescriben.
- **Comprobación sin regenerar:** `python -B -m unittest discover -s docs/academico/tools/f27b -p test_f32_safety.py` prueba el dispatcher y las excepciones de alcance con mocks, sin escribir entregables.

## PDF

Si la política de ejecución de PowerShell no permite `.\topdf.ps1`, se puede pegar su contenido en una consola de PowerShell. No hace falta cambiar la política. Word abre cada DOCX en modo de solo lectura y guarda el PDF junto a él.
