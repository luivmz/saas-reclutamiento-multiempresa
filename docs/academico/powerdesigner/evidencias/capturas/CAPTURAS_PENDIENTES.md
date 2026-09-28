# Capturas de PowerDesigner — STATUS: COMPLETED

Las capturas son evidencia de que cada vista existe en su modelo nativo de PowerDesigner. Complementan las exportaciones PNG y SVG, que son la evidencia formal del contenido.

El archivo conserva su nombre para no romper los enlaces que lo citan. Hasta el 28/09/2026 registraba las capturas pendientes; ahora es el registro de las capturas tomadas.

## Estado (28/09/2026)

**COMPLETED.** Las 7 capturas se tomaron después del hotfix F29B y de su auditoría. Son capturas **reales** de la ventana de PowerDesigner 16.6: ninguna es simulada, reconstruida ni retocada.

**Cómo se tomaron:**

1. Se cerraron los dos modelos de la F29, sin cambios, y se volvieron a abrir desde el disco. Así cada captura muestra el estado guardado y confirmado en git.
2. Cada diagrama se abrió en el editor y se ajustó al lienzo. Después se localizó en el *Object Browser*.
3. Se capturó la ventana principal con la API de ventanas de Windows (`PrintWindow`). El equipo autorizó este método de forma explícita en lugar de la captura manual.
4. Ningún modelo quedó modificado y no se guardó nada.

El procedimiento está en [`../../scripts/capture_f29_views.ps1`](../../scripts/capture_f29_views.ps1). Una segunda ejecución del script, en una carpeta temporal, reprodujo las mismas vistas:

- en cinco capturas, el lienzo es idéntico;
- en ARQ-01 difiere el 0,04 % de los píxeles;
- en la vista principal del F3, la ventana de PowerDesigner tenía otro tamaño, por lo que la comparación no aplica.

En cada captura se ven:

- el título de la ventana, con la ruta del modelo;
- el *Object Browser*, con el paquete desplegado y el diagrama seleccionado;
- la pestaña del diagrama;
- el diagrama completo, o su parte en el caso del F5.

| Captura | Modelo | Diagrama | Estado |
|---|---|---|---|
| [`F3_BPMN_ASIS_PowerDesigner.png`](F3_BPMN_ASIS_PowerDesigner.png) | F29_BPM_Academico.bpm · F3 | F3 - BPMN AS-IS | VALID |
| [`F3_SP-01_detalle_PowerDesigner.png`](F3_SP-01_detalle_PowerDesigner.png) | F29_BPM_Academico.bpm · F3 › SP-01 | SP-01 Evaluar al candidato — detalle | VALID |
| [`F5_BPMN_TOBE_PowerDesigner_parte1.png`](F5_BPMN_TOBE_PowerDesigner_parte1.png) | F29_BPM_Academico.bpm · F5 | F5 - BPMN TO-BE, parte 1: nivel vacante hasta el inicio de SP-P | VALID |
| [`F5_BPMN_TOBE_PowerDesigner_parte2.png`](F5_BPMN_TOBE_PowerDesigner_parte2.png) | F29_BPM_Academico.bpm · F5 | F5 - BPMN TO-BE, parte 2: SP-P hasta el cierre, TB-30 y TB-F1 | VALID |
| [`F5_SP-P_detalle_PowerDesigner.png`](F5_SP-P_detalle_PowerDesigner.png) | F29_BPM_Academico.bpm · F5 › SP-P | SP-P Gestionar la postulación — detalle | VALID |
| [`F8_Casos_de_Uso_PowerDesigner.png`](F8_Casos_de_Uso_PowerDesigner.png) | F29_UML_Academico.oom · F8 | F8 - Casos de Uso Academicos | VALID |
| [`ARQ01_Arquitectura_Conceptual_PowerDesigner.png`](ARQ01_Arquitectura_Conceptual_PowerDesigner.png) | F29_UML_Academico.oom · ARQ01 | ARQ-01 - Arquitectura Conceptual | VALID |

SHA-256 en [`../../MANIFEST.md`](../../MANIFEST.md).

**F5 en dos partes.** Por su anchura, la vista principal del F5 se capturó en dos partes, que se solapan en SP-P. Entre ambas cubren todo el diagrama.

**Diagramas de detalle (F29B-OBS-01).** PowerDesigner 16.6 no dibuja el contenido de SP-01 ni de SP-P en la vista principal del editor: allí sus recuadros aparecen sin tareas. Las capturas de detalle muestran ese contenido, que son los mismos objetos del modelo. Detalle en [`../../F29B_HOTFIX.md`](../../F29B_HOTFIX.md).

## Historial: capturas anteriores al hotfix F29B

El equipo aportó cinco capturas antes del hotfix F29B. Mostraban el estado anterior de los modelos, así que se clasificaron como RETAKE REQUIRED y nunca se versionaron:

| Captura anterior | Clasificación (F29B) | Motivo |
|---|---|---|
| `F3_BPMN_ASIS_PowerDesigner.png` | RETAKE REQUIRED | Geometría anterior a la corrección; faltaba el detalle de SP-01 |
| `F5_BPMN_TOBE_PowerDesigner_parte1.png` | RETAKE REQUIRED | Geometría anterior a la corrección; faltaba el detalle de SP-P |
| `F5_BPMN_TOBE_PowerDesigner_parte2.png` | RETAKE REQUIRED | Lo mismo |
| `F8_Casos_de_Uso_PowerDesigner.png` | RETAKE REQUIRED | Casos de uso redimensionados al abrir (defecto corregido) |
| `ARQ01_Arquitectura_Conceptual_PowerDesigner.png` | RETAKE REQUIRED | Agrupaciones reducidas al abrir (defecto corregido) |

Las capturas nuevas las sustituyeron con los mismos nombres. Además, se añadieron las dos capturas de detalle que faltaban.
