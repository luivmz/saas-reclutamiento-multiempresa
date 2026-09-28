# F29B — Hotfix de reproducibilidad de PowerDesigner

**Estado:** AUDITED / APPROVED (auditoría F29B de Codex). Integración posterior (28/09/2026): se tomaron las 7 capturas, se integraron las exportaciones en los Formatos 03, 05, 08 y 11, y la F29 quedó cerrada con observaciones documentadas ([`README.md`](README.md)). Lo que sigue describe el hotfix tal como se implementó.

**Alcance del hotfix:** los dos modelos de la F29, sus scripts, exportaciones, informes y esta documentación. **No se tocaron** los DOCX y PDF de F3, F5, F8 y F11, ni la F23, el F9, el runtime, el ML, las etiquetas o el release.

## Problema

La integración posterior a la F29 se bloqueó: al comparar los modelos reabiertos desde el disco con las exportaciones confirmadas y con las capturas del equipo, no coincidían.

| Vista | Síntoma | Tipo |
|---|---|---|
| ARQ-01 | Las 6 agrupaciones vuelven al tamaño por defecto al reabrir (p. ej., «Capa de negocio», de 116 000 × 32 000 a 7 648 × 4 000) y los vínculos se redibujan | Defecto real de reproducibilidad |
| F3 y F5 | El editor no dibuja el contenido de SP-01 ni de SP-P al reabrir, aunque el modelo lo guarda | Defecto de representación |
| F8 y F3 / F5 | Al reabrir, casos de uso, tareas y eventos también se redimensionan; la exportación del modelo reabierto difiere de la confirmada (171 diferencias en el SVG del F8) | Defecto real, detectado por la prueba nueva de recarga |

## Causa raíz

### A. Ajuste automático al texto

PowerDesigner crea cada símbolo con `AutoAdjustToText = True`. Con ese valor, el símbolo se vuelve a dimensionar según su texto **al abrir el modelo**, y la geometría fijada por el script (la de la exportación) se pierde.

Prueba controlada en un modelo de ensayo (fuera del repositorio): un paquete de 30 000 × 30 000 vuelve como 4 800 × 4 000 con el valor por defecto, y conserva la geometría exacta con `AutoAdjustToText = False`. En la misma prueba, `KeepSize` o `ManuallyResized` también la conservaron. Se eligió desactivar el ajuste automático porque es la causa directa.

### B. Vista compuesta de los subprocesos expandidos

PowerDesigner 16.6 pinta la vista compuesta de un proceso compuesto de dos maneras distintas:

- **El editor** dibuja solo el contenido del **diagrama por defecto** del proceso compuesto. En la F29 ese diagrama estaba vacío, porque el contenido se había colocado como subsímbolos del diagrama padre. Por eso el recuadro aparecía vacío.
- **La exportación** (`ExportImage`) dibuja los subsímbolos del diagrama padre **y además** el diagrama por defecto, reajustado al recuadro.

Evidencia en un modelo de ensayo, en [`evidencias/f29b/`](evidencias/f29b/):

| Captura o exportación | Qué muestra |
|---|---|
| [01](evidencias/f29b/01_prueba_editor_subsimbolos_sin_contenido.png) | Editor real con el diagrama por defecto vacío: recuadro vacío |
| [02](evidencias/f29b/02_prueba_editor_diagrama_por_defecto_con_contenido.png) | Editor real con el diagrama por defecto lleno: contenido visible |
| [03](evidencias/f29b/03_prueba_exportacion_duplica_diagrama_por_defecto.png) | Exportación con ese mismo diagrama lleno: contenido **duplicado** y desplazado |
| [04](evidencias/f29b/04_prueba_exportacion_con_detalle_sin_duplicados.png) | Exportación con el contenido en un diagrama de detalle (no por defecto): sin duplicados |

Conclusión: ninguna representación hace que el editor muestre el contenido **dentro** del recuadro sin que la exportación lo duplique. Es una limitación de la herramienta (**F29B-OBS-01**).

## Solución

| Cambio | Archivo |
|---|---|
| `Set-Rect` desactiva `AutoAdjustToText` en todo símbolo que dimensiona (nodos, pools, carriles, paquetes, notas, textos y marcos) | `scripts/f29lib.ps1` |
| **Publicación reproducible** (`Publish-F29View`). Pasos: (1) instantánea de la geometría de cada símbolo y subsímbolo (ruta de puntos en los vínculos); (2) guardar, cerrar y reabrir desde el disco; (3) comparar con tolerancia 0; (4) exportar **desde el modelo reabierto**; (5) volver a cerrar y reabrir; (6) comprobar que el SVG es el mismo (mismas líneas; PowerDesigner puede variar el orden de escritura de algunos vínculos). Los cuatro scripts de vista terminan con este paso | `scripts/f29lib.ps1` y los 4 scripts de vista |
| **Diagramas de detalle** de SP-01 y SP-P (`Sync-CompositeSubDiagram`): el diagrama por defecto de cada subproceso queda vacío (la exportación no duplica nada) y un diagrama de detalle del mismo proceso, «SP-01 Evaluar al candidato — detalle» y «SP-P Gestionar la postulación — detalle», representa **los mismos objetos** (sin duplicar ninguno), con la misma disposición desplazada junto al origen para que el editor lo muestre al abrirlo, y un título que explica su relación con la vista compuesta | `scripts/f29lib.ps1`, `f29-f3-bpmn-asis.ps1`, `f29-f5-bpmn-tobe.ps1` |
| Se eliminan los diagramas vacíos que PowerDesigner crea por defecto en los paquetes de agrupación de ARQ-01 | `scripts/f29-arq01-arquitectura.ps1` |
| Geometría de las 6 agrupaciones en el informe de ARQ-01: pedida frente a la del modelo reabierto | `scripts/f29-arq01-arquitectura.ps1` |
| Validación independiente ampliada (sin PowerDesigner). Nuevas comprobaciones: ajuste automático desactivado en todo símbolo de nodo; geometría de las 6 agrupaciones igual a la declarada; detalle con todos los hijos de SP-01 y SP-P y vista compuesta vacía; cada tarea de SP-01 y SP-P dibujada **una sola vez** en la exportación; recarga sin cambios y exportación reproducible registradas en los cuatro informes | `scripts/validate_f29.py` |

**Sin cambios de semántica:** no se renombró, añadió ni eliminó ningún objeto de negocio; TB-30 y TB-F1 siguen desconectados y MT-02 conserva su formato. Check Model da los mismos hallazgos aceptados en la auditoría de la F29:

- BPM: TB-30 y TB-F1 (esperados por especificación) y MT-02 (límite de la herramienta);
- OOM: CU-16 (esperado por especificación).

## Pruebas tras la recarga

Resultado de los scripts, en [`validation/`](validation/). En cada caso la exportación se hizo desde el modelo reabierto y una segunda recarga la reprodujo.

| Vista | Diagrama | Símbolos antes de guardar / tras reabrir | Cambiados (tolerancia 0) | SVG reproducido |
|---|---|---|---|---|
| F3 | F3 - BPMN AS-IS | 75 / 75 | 0 | Sí (923 líneas) |
| F3 | SP-01 Evaluar al candidato — detalle | 14 / 14 | 0 | — |
| F5 | F5 - BPMN TO-BE | 156 / 156 | 0 | Sí (1 696 líneas) |
| F5 | SP-P Gestionar la postulación — detalle | 45 / 45 | 0 | — |
| F8 | F8 - Casos de Uso Academicos | 67 / 67 | 0 | Sí (418 líneas) |
| ARQ-01 | ARQ-01 - Arquitectura Conceptual | 55 / 55 | 0 | Sí (700 líneas) |

**ARQ-01, las 6 agrupaciones.** X izquierda, Y superior, ancho y alto son **iguales** antes de guardar y tras reabrir:

| Agrupación | X | Y | Ancho | Alto |
|---|---|---|---|---|
| Capa de presentación | 22 000 | 88 000 | 22 000 | 18 000 |
| Capa de acceso y seguridad | 50 000 | 88 000 | 48 000 | 18 000 |
| Experimental (opcional) | 108 000 | 88 000 | 30 000 | 18 000 |
| Capa de negocio | 22 000 | 62 000 | 116 000 | 32 000 |
| Servicios transversales | 22 000 | 25 000 | 94 000 | 14 000 |
| Persistencia e infraestructura | 22 000 | 7 000 | 116 000 | 14 000 |

**Editor real tras la recarga.** Capturas del editor tomadas con la API de ventanas, no simuladas: los diagramas de detalle muestran el contenido de SP-01 ([05](evidencias/f29b/05_editor_F3_SP-01_detalle_tras_recarga.png)) y de SP-P ([06](evidencias/f29b/06_editor_F5_SP-P_detalle_tras_recarga.png)).

**Validación:**

- `validate_f29.py`: 177 comprobaciones correctas, 0 fallas (antes 157; ninguna regla rebajada);
- `validate.py`: 0 fallas.

## Exportaciones regeneradas

Todas proceden de los modelos reabiertos desde el disco.

| Exportación | Cambio visible frente a la auditada |
|---|---|
| `ARQ-01_Arquitectura_Conceptual.png` | **Ninguno**: PNG idéntico byte a byte. El SVG solo cambia el orden de escritura |
| `F8_Casos_de_Uso_Academicos.png` | **Ninguno**: PNG idéntico byte a byte. El SVG solo cambia el orden de escritura |
| `F3_BPMN_ASIS.png` | Solo las puntas de flecha (2 524 píxeles de 11 millones). Al recargar, PowerDesigner aplica el estilo del lenguaje BPMN 2.0: triángulo lleno en los flujos de secuencia y triángulo hueco en los de mensaje (notación BPMN correcta). Sin cambios de geometría ni de contenido |
| `F5_BPMN_TOBE.png` | Lo mismo (4 888 píxeles de 31 millones) |

Hashes en [`MANIFEST.md`](MANIFEST.md).

## Capturas

| Captura del equipo | Estado | Motivo |
|---|---|---|
| `ARQ01_Arquitectura_Conceptual_PowerDesigner.png` | **RETAKE REQUIRED** | Muestra el defecto: agrupaciones reducidas y vínculos redibujados |
| `F3_BPMN_ASIS_PowerDesigner.png` | **RETAKE REQUIRED** | Geometría anterior a la corrección. Falta el diagrama de detalle de SP-01 |
| `F5_BPMN_TOBE_PowerDesigner_parte1.png` y `parte2.png` | **RETAKE REQUIRED** | Lo mismo con SP-P. Se aceptan dos partes si cubren el diagrama completo |
| `F8_Casos_de_Uso_PowerDesigner.png` | **RETAKE REQUIRED** | Muestra los casos de uso redimensionados al abrir (el defecto A). Tras el hotfix, el editor muestra la geometría exacta de la exportación |

Las cinco capturas se conservan en el árbol de trabajo, sin versionar y sin borrar, y no se registran como evidencia final. Hacen falta dos capturas nuevas: los diagramas de detalle de SP-01 y SP-P. Instrucciones en [`evidencias/capturas/CAPTURAS_PENDIENTES.md`](evidencias/capturas/CAPTURAS_PENDIENTES.md).

**Actualización (28/09/2026): capturas completadas.** Las cinco capturas se sustituyeron, con los mismos nombres, por capturas reales tomadas después del hotfix, y se añadieron las dos de detalle. Las 7 muestran:

- la geometría exacta de las exportaciones;
- en ARQ-01, las 6 agrupaciones con su tamaño;
- en los diagramas de detalle, el contenido de SP-01 y SP-P.

Registro en [`evidencias/capturas/CAPTURAS_PENDIENTES.md`](evidencias/capturas/CAPTURAS_PENDIENTES.md).

## Limitaciones restantes

- **F29B-OBS-01 (herramienta):** en la vista principal del editor, los recuadros de SP-01 y SP-P aparecen **sin contenido**. El contenido se ve en su diagrama de detalle y en las exportaciones, que son la evidencia formal y son reproducibles. Con la exportación nativa de PowerDesigner 16.6 no se puede obtener una sola representación que el editor muestre dentro del recuadro sin que la exportación la duplique.
- **Rótulos de eventos y compuertas en el detalle:** son textos libres de la vista principal, y el diagrama de detalle no los repite. Allí los eventos y compuertas se identifican por su posición, el título y los flujos; los nombres están en el modelo y en la vista principal.
- **Espacio de trabajo local de PowerDesigner:** las pruebas añadieron a la lista del *Object Browser* los modelos de ensayo `scratch_comp_*` y `ObjectOrientedModel_1`. Sus archivos están en una carpeta temporal fuera del repositorio. Se pueden quitar de la lista con clic derecho › *Close* o *Remove*.
- **LOW para la F31 (sin cambios):**
  - H-14 y F28-L01: cabeceras de los PDF;
  - F29-L01: `RepositoryFilename` con ruta local;
  - F29-L02: rótulos de ARQ-01 que rozan líneas, sin cambios con el hotfix.
