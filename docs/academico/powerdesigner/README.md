# PowerDesigner académico — Fase 29

Formalización en **PowerDesigner 16.6** de las cuatro vistas académicas especificadas en las fases F27D y F28:

- F3 BPMN AS-IS;
- F5 BPMN TO-BE;
- F8 casos de uso;
- ARQ-01, la arquitectura conceptual del F11.

**Estado:** FORMALIZADO en la F29 (auditada con observaciones) y corregido por el **hotfix F29B** ([`F29B_HOTFIX.md`](F29B_HOTFIX.md)): los modelos reabiertos desde el disco reproducen exactamente sus exportaciones. Pendiente de la auditoría F29B. Ningún Formato (DOCX o PDF) se sustituyó todavía: según el criterio de aceptación de cada especificación y la regla 3 de la [lista de trabajo](../POWERDESIGNER_WORKLIST.md), el borrador de cada Formato se sustituye **solo después de una nueva auditoría**.

Los modelos de la F23 ([`docs/v1.1/powerdesigner/`](../../v1.1/powerdesigner/README.md)) no se abrieron para editarlos ni se modificaron: UC-01, CO-01, PK-01, DE-01, AC-01 y el resto de sus 22 vistas y exportaciones siguen igual.

## Contenido

| Carpeta o archivo | Qué contiene |
|---|---|
| [`models/F29_BPM_Academico.bpm`](models/F29_BPM_Academico.bpm) | Modelo BPM (lenguaje *BPMN 2.0 Descriptive*). Paquete **F3**, con el diagrama «F3 - BPMN AS-IS», y paquete **F5**, con «F5 - BPMN TO-BE» |
| [`models/F29_UML_Academico.oom`](models/F29_UML_Academico.oom) | Modelo OOM (UML, *Analysis*). Paquete **F8**, con «F8 - Casos de Uso Academicos», y paquete **ARQ01**, con «ARQ-01 - Arquitectura Conceptual» |
| [`exports/`](exports/) | 8 exportaciones: PNG y SVG de cada vista. Cada SVG se acompaña de la carpeta `*_svg_Files` con los iconos BPMN que referencia |
| [`validation/`](validation/) | Informes de verificación que escriben los scripts, uno por vista |
| [`scripts/`](scripts/) | Construcción reproducible (PowerShell sobre COM), rasterizado, validación independiente y generación del manifiesto y la trazabilidad |
| [`MANIFEST.md`](MANIFEST.md) | Artefactos con su SHA-256 |
| [`F29_VALIDATION.md`](F29_VALIDATION.md) | Resultado PASS/OBS por vista |
| [`F29B_HOTFIX.md`](F29B_HOTFIX.md) | Hotfix F29B: causa raíz, corrección y pruebas de reproducibilidad tras la recarga |
| [`evidencias/f29b/`](evidencias/f29b/) | Evidencia diagnóstica del hotfix (capturas reales del editor y exportaciones de prueba) |
| [`evidencias/capturas/`](evidencias/capturas/CAPTURAS_PENDIENTES.md) | Capturas de PowerDesigner del equipo: **PENDING RETAKE** tras el hotfix, con instrucciones |

Trazabilidad por elemento (especificación → objeto del modelo → carril o agrupación → RF → exportación): [`../trazabilidad/F29-powerdesigner-traceability.md`](../trazabilidad/F29-powerdesigner-traceability.md).

## Cómo reproducirlo

Requiere Windows, PowerDesigner 16.6 con el lenguaje *BPMN 2.0 Descriptive*, Python con Pillow y Microsoft Edge (para el rasterizado). Desde la raíz del repositorio, en PowerShell:

```powershell
. .\docs\academico\powerdesigner\scripts\f29lib.ps1
. .\docs\academico\powerdesigner\scripts\f29-f3-bpmn-asis.ps1
. .\docs\academico\powerdesigner\scripts\f29-f5-bpmn-tobe.ps1
. .\docs\academico\powerdesigner\scripts\f29-f8-casos-de-uso.ps1
. .\docs\academico\powerdesigner\scripts\f29-arq01-arquitectura.ps1
python docs/academico/powerdesigner/scripts/validate_f29.py
python docs/academico/powerdesigner/scripts/make_f29_docs.py
```

Cada script hace tres cosas:

1. **Reemplaza su paquete entero**, lo que permite repetirlo sin dejar restos.
2. **Verifica la vista y escribe su informe** en `validation/`.
3. **Guarda el modelo y exporta** el PNG y el SVG.

`f29lib.ps1` se niega a abrir o guardar cualquier archivo que no sea uno de los dos modelos de la F29.

## Decisiones de modelado

| Tema | Decisión | Motivo |
|---|---|---|
| Una vista, un paquete | F3, F5, F8 y ARQ01 son paquetes separados | Los nombres se repiten entre vistas (por ejemplo, EP-02 «Postulación presentada» en F3 y en F5) y cada paquete es su propio espacio de nombres |
| Pools y carriles compartidos | Las unidades organizativas son objetos del modelo y se reutilizan por nombre: «Área solicitante», «RR. HH.» y el pool «Postulante» son los mismos objetos en F3 y en F5 | PowerDesigner no admite unidades organizativas dentro de paquetes y exige nombres únicos |
| Orden de los carriles | F3: Área solicitante · Dirección · RR. HH. · Evaluadores. F5: Área solicitante · Aprobador / Dirección · RR. HH. · Plataforma SaaS (sistema) · Evaluador | Así los carriles que abarca cada subproceso (SP-01 y SP-P) quedan contiguos. En BPMN, el orden de los carriles no tiene significado |
| Pool Postulante | Un solo carril sin nombre | PowerDesigner exige al menos un carril por pool. La especificación no define carriles para el Postulante |
| SP-01 y SP-P | Subprocesos **expandidos** (vista compuesta con sus subsímbolos), con el marcador de instancia múltiple paralela (\|\|\|), en el nivel superior del diagrama, sobre los carriles que abarcan; cada tarea interna declara su responsable (*Organization Unit*). Además, cada uno tiene un **diagrama de detalle** («SP-01 Evaluar al candidato — detalle», «SP-P Gestionar la postulación — detalle») con los mismos objetos, y su diagrama por defecto queda vacío (F29B) | Un símbolo dentro de un carril queda recortado por él. El editor de PowerDesigner dibuja la vista compuesta desde el diagrama por defecto, y la exportación dibuja los subsímbolos y ese diagrama; con el diagrama por defecto vacío la exportación no duplica, y el detalle deja ver el contenido en el editor (F29B-OBS-01) |
| Eventos BPMN de mensaje | EP-01 (F3 y F5) son procesos con el estereotipo *Message Start Event*; EFP-02 y EFP-03 son procesos con *Message End Event* | Así los define el lenguaje *BPMN 2.0 Descriptive* de PowerDesigner. Un inicio o fin simple no admite flujos de mensaje |
| Mensajes hacia el borde del pool | MF-03 y MF-04 (F3) y MT-03 a MT-08 (F5) terminan en el pool Postulante, sin evento receptor. MT-02 termina en el borde de SP-P | Lo exige la especificación. El contenido de cada mensaje va como formato de mensaje (MF-xx / MT-xx) |
| Rótulos de eventos y compuertas | Texto con «ID» y nombre oficial junto al icono | PowerDesigner no muestra el nombre de los eventos ni de las compuertas BPMN 2.0 dentro del icono |
| TB-30 y TB-F1 | Cada uno dentro de un grupo discontinuo con su anotación, sin flujos | TB-30 es transversal. TB-F1 es una propuesta futura (A-30), desconectada |
| F8 | 5 actores y CU-01 a CU-20 en 5 áreas funcionales (A a E, las mismas del F5). RR. HH. y Aprobador / Dirección van a la derecha, con sus casos en una columna | Ninguna línea atraviesa un símbolo ajeno; se comprueba en cada construcción |
| ARQ-01 | Las 6 agrupaciones son paquetes UML que contienen sus componentes y se dibujan como contenedores. R-03, R-04, R-13, R-14 y R-16 usan el paquete «Capa de negocio» como extremo | Es lo que pide la especificación: relaciones con el marco. El diagrama muestra los componentes de los subpaquetes mediante accesos directos internos, con el icono de acceso directo oculto |
| Actores en ARQ-01 | Paquete «Actores (fuera del sistema)» con la lista de los 5 actores del F8 y una sola dependencia «usan» hacia C01 | Un diagrama de componentes no admite símbolos de actor. Se evita duplicar los actores definidos en el F8 |
| Exportación PNG | El PNG se rasteriza desde el SVG exportado por PowerDesigner (`svg2png.py`, Edge sin interfaz, escala 2), sin retoques | El PNG nativo de PowerDesigner 16.6 omite el contenido de los subprocesos expandidos. El SVG es la exportación nativa |
| Reproducibilidad (F29B) | Todo símbolo dimensionado por los scripts tiene desactivado el ajuste automático al texto, y cada vista se publica guardando, cerrando y reabriendo el modelo: la exportación sale del modelo reabierto y una segunda recarga la reproduce | Con el ajuste automático activado (valor por defecto), PowerDesigner redimensiona los símbolos al abrir el modelo y la geometría deja de coincidir con la exportada |

## Check Model

Se ejecuta sobre el modelo completo, sin autocorrección. La automatización no expone el objeto de cada mensaje, así que cada hallazgo se identifica **por aislamiento**: se cambia de forma temporal la condición que lo causa, se vuelve a comprobar y se deshace el cambio antes de guardar.

| Modelo | Hallazgos | Causa demostrada | Tipo |
|---|---|---|---|
| BPM | *CheckPrcsInputFlow* y *CheckPrcsOutputFlow* (errores) | TB-30 y TB-F1 no tienen flujos. Con flujos temporales, desaparecen | Exigido por la especificación |
| BPM | *CheckFlowIncohMsg* (advertencia) | MT-02, con su formato de mensaje, llega al borde de SP-P. Un subproceso compuesto no puede declarar un mensaje recibido en PowerDesigner: *Received Message* es de solo lectura y la acción de recepción no está disponible en su modo de implementación. Sin el formato de MT-02, el hallazgo desaparece | Límite de la herramienta. Se conserva el formato porque es el contenido del mensaje |
| OOM | *Use Case/Single* (error) | CU-16 no tiene actor directo; se incluye desde CU-05, CU-15 y CU-17. Con una asociación temporal, desaparece | Exigido por la especificación |

Durante la investigación se detectaron y borraron del modelo BPM 9 objetos huérfanos creados en las pruebas de la API (2 inicios, 2 fines y 5 compuertas en la raíz): eran la causa de las advertencias iniciales. El modelo final no tiene objetos en la raíz, salvo las unidades organizativas y los formatos de mensaje, que PowerDesigner no admite en paquetes.

## Limitaciones y observaciones

- **Capturas de PowerDesigner:** las cinco capturas que aportó el equipo son anteriores al hotfix F29B y quedan en **PENDING RETAKE**, junto con dos nuevas de los diagramas de detalle ([instrucciones](evidencias/capturas/CAPTURAS_PENDIENTES.md)). No se incluye ninguna captura simulada.
- **F29B-OBS-01 (herramienta):** en la vista principal del editor, los recuadros de SP-01 y SP-P aparecen sin contenido. Su contenido se ve en los diagramas de detalle y en las exportaciones reproducibles. Ver [`F29B_HOTFIX.md`](F29B_HOTFIX.md).
- **Formatos DOCX y PDF:** siguen con los borradores. La sustitución por las exportaciones formales queda para después de la auditoría F29.
- **Diagrama raíz vacío:** cada modelo conserva el diagrama raíz que PowerDesigner creó con él, vacío.
- **Finales de línea:** git normaliza a LF los `.bpm`, `.oom` y `.svg`. El manifiesto da el SHA-256 del contenido versionado.
- **LOW heredados:** H-14 y F28-L01 (cabeceras de PDF) siguen asignados a la F31; esta fase no los aborda.
