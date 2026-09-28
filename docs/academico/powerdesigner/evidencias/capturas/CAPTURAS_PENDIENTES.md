# Capturas de PowerDesigner — pendientes (PENDING RETAKE)

Las capturas son evidencia de que cada vista existe en su modelo nativo de PowerDesigner. Complementan las exportaciones PNG y SVG, que son la evidencia formal del contenido.

## Estado tras el hotfix F29B

El equipo aportó cinco capturas. Se tomaron **antes** del hotfix F29B y muestran el estado anterior de los modelos, así que hay que repetirlas todas. Se conservan en esta carpeta sin versionar y no se usan como evidencia final. Detalle en [`../../F29B_HOTFIX.md`](../../F29B_HOTFIX.md).

| Captura actual | Estado | Motivo |
|---|---|---|
| `F3_BPMN_ASIS_PowerDesigner.png` | RETAKE REQUIRED | Geometría anterior a la corrección; falta el detalle de SP-01 |
| `F5_BPMN_TOBE_PowerDesigner_parte1.png` | RETAKE REQUIRED | Geometría anterior a la corrección; falta el detalle de SP-P |
| `F5_BPMN_TOBE_PowerDesigner_parte2.png` | RETAKE REQUIRED | Lo mismo |
| `F8_Casos_de_Uso_PowerDesigner.png` | RETAKE REQUIRED | Casos de uso redimensionados al abrir (defecto corregido) |
| `ARQ01_Arquitectura_Conceptual_PowerDesigner.png` | RETAKE REQUIRED | Agrupaciones reducidas al abrir (defecto corregido) |

## Capturas que hay que tomar

| Archivo | Modelo | Paquete | Diagrama |
|---|---|---|---|
| `F3_BPMN_ASIS_PowerDesigner.png` | F29_BPM_Academico.bpm | F3 - AS-IS preliminar | F3 - BPMN AS-IS |
| `F3_SP-01_detalle_PowerDesigner.png` | F29_BPM_Academico.bpm | F3 - AS-IS preliminar › SP-01 Evaluar al candidato | SP-01 Evaluar al candidato — detalle |
| `F5_BPMN_TOBE_PowerDesigner.png` (o `_parte1` y `_parte2`) | F29_BPM_Academico.bpm | F5 - TO-BE propuesto | F5 - BPMN TO-BE |
| `F5_SP-P_detalle_PowerDesigner.png` | F29_BPM_Academico.bpm | F5 - TO-BE propuesto › SP-P Gestionar la postulación | SP-P Gestionar la postulación — detalle |
| `F8_Casos_de_Uso_PowerDesigner.png` | F29_UML_Academico.oom | F8 - Casos de uso (vista academica) | F8 - Casos de Uso Academicos |
| `ARQ01_Arquitectura_Conceptual_PowerDesigner.png` | F29_UML_Academico.oom | ARQ-01 - Arquitectura conceptual (F11 adaptado) | ARQ-01 - Arquitectura Conceptual |

Para el F5 se aceptan dos partes si entre ambas cubren el diagrama completo y no se contradicen.

## Cómo tomarlas

1. **Cerrar los modelos** de la F29 si están abiertos, **sin guardar**, y volver a abrirlos desde el disco con **File › Open**. Así la captura muestra el estado guardado.
2. Para cada diagrama:
   1. Abrirlo con doble clic en el *Object Browser*. Los diagramas de detalle están dentro del subproceso: por ejemplo, F3 - AS-IS preliminar › Sub-Processes › SP-01 Evaluar al candidato.
   2. Ajustar a la ventana con **View › Zoom to Fit**.
   3. Dejar visibles el título de la ventana (ruta del modelo), el *Object Browser* con el paquete desplegado y la pestaña del diagrama.
   4. Capturar la ventana con **Alt + Impr Pant** o la Herramienta Recortes y guardar en PNG en esta carpeta con el nombre de la tabla. Se reemplazan las capturas anteriores.
3. **Cerrar sin guardar.** Si PowerDesigner pregunta por cambios solo por haber abierto el modelo, responder «No».

## Qué debe verse

- En las vistas principales, el diagrama completo, igual a su exportación en [`../../exports/`](../../exports/).
- En la vista principal del F3 y del F5, el recuadro de SP-01 y de SP-P aparece **sin contenido**. Es la limitación F29B-OBS-01 de PowerDesigner 16.6: el contenido se ve en el diagrama de detalle y en la exportación.
- En los diagramas de detalle, las tareas, compuertas, eventos y flujos del subproceso.

## Después de tomarlas

1. Ejecutar `python docs/academico/powerdesigner/scripts/make_f29_docs.py`.
2. Registrar las capturas en el manifiesto con su SHA-256 y el estado VALID.
3. Cambiar esta nota a «tomadas».
