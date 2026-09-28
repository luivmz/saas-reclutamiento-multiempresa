# Capturas de PowerDesigner — pendientes

Faltan cuatro capturas de pantalla de PowerDesigner. Se piden como evidencia de que cada vista existe en su modelo nativo, además de las exportaciones PNG y SVG.

## Por qué no se incluyen

No se pudieron tomar de forma fiable desde la sesión automatizada de la F29:

- Windows impide que un proceso en segundo plano traiga la ventana de PowerDesigner al frente.
- La automatización (COM) de PowerDesigner no ofrece un comando «ajustar a la ventana».
- Las teclas enviadas como mensajes no llegan al lienzo.

Las capturas de prueba mostraban solo un fragmento de cada diagrama. Por eso se descartaron, y **no se incluye ninguna captura simulada**.

## Cómo tomarlas (unos 5 minutos)

1. Abrir PowerDesigner 16.6 y, con **File › Open**, los dos modelos:
   - `docs/academico/powerdesigner/models/F29_BPM_Academico.bpm`
   - `docs/academico/powerdesigner/models/F29_UML_Academico.oom`
2. Para cada vista de la tabla:
   1. En el *Object Browser*, desplegar el modelo y el paquete, y abrir el diagrama con doble clic.
   2. Ajustar el diagrama a la ventana con **View › Zoom to Fit**.
   3. Dejar visibles la ventana completa, el *Object Browser* con el paquete desplegado y la pestaña del diagrama.
   4. Capturar la ventana con **Alt + Impr Pant** y pegar en Paint, o con la Herramienta Recortes.
   5. Guardar en PNG con el nombre indicado, en esta carpeta (`docs/academico/powerdesigner/evidencias/capturas/`).

| Archivo | Modelo | Paquete | Diagrama |
|---|---|---|---|
| `F3_BPMN_ASIS_PowerDesigner.png` | F29_BPM_Academico.bpm | F3 - AS-IS preliminar | F3 - BPMN AS-IS |
| `F5_BPMN_TOBE_PowerDesigner.png` | F29_BPM_Academico.bpm | F5 - TO-BE propuesto | F5 - BPMN TO-BE |
| `F8_Casos_de_Uso_PowerDesigner.png` | F29_UML_Academico.oom | F8 - Casos de uso (vista academica) | F8 - Casos de Uso Academicos |
| `ARQ01_Arquitectura_Conceptual_PowerDesigner.png` | F29_UML_Academico.oom | ARQ-01 - Arquitectura conceptual (F11 adaptado) | ARQ-01 - Arquitectura Conceptual |

3. **Cerrar sin guardar** (**File › Close**, responder «No»): las capturas no deben modificar los modelos. Si PowerDesigner pregunta por cambios solo por haber abierto el modelo, no hay que guardar.
4. Registrar las capturas:
   1. Ejecutar `python docs/academico/powerdesigner/scripts/make_f29_docs.py`, que recalcula el manifiesto.
   2. Añadir las cuatro filas a la sección «Capturas» de [`../../MANIFEST.md`](../../MANIFEST.md).
   3. Cambiar esta nota a «tomadas».

## Qué debe verse en cada captura

- El título de la ventana, con la ruta del modelo de la F29.
- El paquete y el diagrama de la vista.
- El diagrama completo y legible, igual a su exportación en [`../../exports/`](../../exports/).

Las exportaciones ya son evidencia del contenido. Las capturas solo prueban que las vistas existen en PowerDesigner.
