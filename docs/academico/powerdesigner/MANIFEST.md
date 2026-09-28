# Manifiesto F29 — modelos y exportaciones de PowerDesigner

Generado por [`scripts/make_f29_docs.py`](scripts/make_f29_docs.py). **SHA-256 del contenido versionado** (`git show :<ruta>`, el blob que se confirma): git normaliza a LF los finales de línea de `.bpm`, `.oom` y `.svg`, así que el hash del archivo de trabajo en Windows (CRLF) puede diferir; el del blob es reproducible en cualquier checkout.

**Estado:** FORMALIZADO en la F29 (auditada con observaciones) y corregido por el hotfix F29B (reproducibilidad tras recarga), pendiente de la auditoría F29B. Ningún formato (DOCX o PDF) se sustituyó todavía.

## Modelos y exportaciones

| Artefacto | Tipo | Modelo fuente | Diagrama | Formato | SHA-256 | Estado |
|---|---|---|---|---|---|---|
| [`models/F29_BPM_Academico.bpm`](models/F29_BPM_Academico.bpm) | Modelo BPM (BPMN 2.0 Descriptive) | — | F3 - BPMN AS-IS; F5 - BPMN TO-BE | BPM (XML) | `ebe6b96309cdc20c2be2e570c2343527bc0242524f3ddcad320b97b8a4593932` | FORMALIZADO |
| [`models/F29_UML_Academico.oom`](models/F29_UML_Academico.oom) | Modelo OOM (UML, Analysis) | — | F8 - Casos de Uso Academicos; ARQ-01 - Arquitectura Conceptual | OOM (XML) | `9ce5f28d87898f44ec5bc1d2d29e72b8060ef97f1df8f61940dd32c5abdfe0d9` | FORMALIZADO |
| [`exports/F3_BPMN_ASIS.png`](exports/F3_BPMN_ASIS.png) | Exportación | F29_BPM_Academico.bpm | F3 - BPMN AS-IS | PNG (rasterizado del SVG, escala 2) | `685a9380cf24b0b21d93e6efdcee67b60fd5ca8f52d3746c8930fbd1b3de2df5` | FORMALIZADO |
| [`exports/F3_BPMN_ASIS.svg`](exports/F3_BPMN_ASIS.svg) | Exportación | F29_BPM_Academico.bpm | F3 - BPMN AS-IS | SVG (exportación nativa) | `12189d6b13c860e22faa51313615887b8ae2b934d9c9aefbb8ae8d90aee0ae9e` | FORMALIZADO |
| [`exports/F5_BPMN_TOBE.png`](exports/F5_BPMN_TOBE.png) | Exportación | F29_BPM_Academico.bpm | F5 - BPMN TO-BE | PNG (rasterizado del SVG, escala 2) | `b3af8824cc3ad92e814e2d62d79ce584450699ad5f5a0cfec7f52f4036447d67` | FORMALIZADO |
| [`exports/F5_BPMN_TOBE.svg`](exports/F5_BPMN_TOBE.svg) | Exportación | F29_BPM_Academico.bpm | F5 - BPMN TO-BE | SVG (exportación nativa) | `3615cc3fe137ef6fe6b8c6cbc89944d07db2241a54c15bf7b2316640f49c046b` | FORMALIZADO |
| [`exports/F8_Casos_de_Uso_Academicos.png`](exports/F8_Casos_de_Uso_Academicos.png) | Exportación | F29_UML_Academico.oom | F8 - Casos de Uso Academicos | PNG (rasterizado del SVG, escala 2) | `94dee7b176dbd529385392b82e60b81c5cc3b1ebfad829da7481b7f931f05aa3` | FORMALIZADO |
| [`exports/F8_Casos_de_Uso_Academicos.svg`](exports/F8_Casos_de_Uso_Academicos.svg) | Exportación | F29_UML_Academico.oom | F8 - Casos de Uso Academicos | SVG (exportación nativa) | `307d84ed1199e75668390b22806ec192524556c13498529b3272c242e12e705d` | FORMALIZADO |
| [`exports/ARQ-01_Arquitectura_Conceptual.png`](exports/ARQ-01_Arquitectura_Conceptual.png) | Exportación | F29_UML_Academico.oom | ARQ-01 - Arquitectura Conceptual | PNG (rasterizado del SVG, escala 2) | `4084af202f7af08adca7545c4ea3fe3906c8d0d575da3e946385f168047e3ee5` | FORMALIZADO |
| [`exports/ARQ-01_Arquitectura_Conceptual.svg`](exports/ARQ-01_Arquitectura_Conceptual.svg) | Exportación | F29_UML_Academico.oom | ARQ-01 - Arquitectura Conceptual | SVG (exportación nativa) | `3db92419d9523bc60c1ecb028fb8c0bd2c7de7304bff4cc603249ac98ab09916` | FORMALIZADO |

## Recursos, scripts e informes

| Archivo | Uso | SHA-256 |
|---|---|---|
| [`exports/F3_BPMN_ASIS_svg_Files/svg_bitmap1.png`](exports/F3_BPMN_ASIS_svg_Files/svg_bitmap1.png) | Icono referenciado por el SVG (exportado por PowerDesigner) | `66d8e0012e84547b80cabb27febcefa8bc0b28780fa8ff019ddf56d5653ec977` |
| [`exports/F3_BPMN_ASIS_svg_Files/svg_bitmap2.png`](exports/F3_BPMN_ASIS_svg_Files/svg_bitmap2.png) | Icono referenciado por el SVG (exportado por PowerDesigner) | `3ff937578cee32c209ecd689e609b25c8544b7ceadd522fd64fe93ca7284d38a` |
| [`exports/F3_BPMN_ASIS_svg_Files/svg_bitmap3.png`](exports/F3_BPMN_ASIS_svg_Files/svg_bitmap3.png) | Icono referenciado por el SVG (exportado por PowerDesigner) | `0c1e9cec2d9b8305dc6a7f090d686da339ca9b6065c206a5dfde37cda891672e` |
| [`exports/F3_BPMN_ASIS_svg_Files/svg_bitmap4.png`](exports/F3_BPMN_ASIS_svg_Files/svg_bitmap4.png) | Icono referenciado por el SVG (exportado por PowerDesigner) | `76e1f01614c61309f4bdb0ea1204e08489f4d0ba57ff314763d2f8cd0c3c1e72` |
| [`exports/F3_BPMN_ASIS_svg_Files/svg_bitmap5.png`](exports/F3_BPMN_ASIS_svg_Files/svg_bitmap5.png) | Icono referenciado por el SVG (exportado por PowerDesigner) | `3e7c695b76de5132677d35248e4b7555e583461c66afeb4db6a63872d9efc955` |
| [`exports/F5_BPMN_TOBE_svg_Files/svg_bitmap1.png`](exports/F5_BPMN_TOBE_svg_Files/svg_bitmap1.png) | Icono referenciado por el SVG (exportado por PowerDesigner) | `3ff937578cee32c209ecd689e609b25c8544b7ceadd522fd64fe93ca7284d38a` |
| [`exports/F5_BPMN_TOBE_svg_Files/svg_bitmap2.png`](exports/F5_BPMN_TOBE_svg_Files/svg_bitmap2.png) | Icono referenciado por el SVG (exportado por PowerDesigner) | `0c1e9cec2d9b8305dc6a7f090d686da339ca9b6065c206a5dfde37cda891672e` |
| [`exports/F5_BPMN_TOBE_svg_Files/svg_bitmap3.png`](exports/F5_BPMN_TOBE_svg_Files/svg_bitmap3.png) | Icono referenciado por el SVG (exportado por PowerDesigner) | `76e1f01614c61309f4bdb0ea1204e08489f4d0ba57ff314763d2f8cd0c3c1e72` |
| [`exports/F5_BPMN_TOBE_svg_Files/svg_bitmap4.png`](exports/F5_BPMN_TOBE_svg_Files/svg_bitmap4.png) | Icono referenciado por el SVG (exportado por PowerDesigner) | `3e7c695b76de5132677d35248e4b7555e583461c66afeb4db6a63872d9efc955` |
| [`exports/F5_BPMN_TOBE_svg_Files/svg_bitmap5.png`](exports/F5_BPMN_TOBE_svg_Files/svg_bitmap5.png) | Icono referenciado por el SVG (exportado por PowerDesigner) | `9a446094598d1025d70a89f3c5b8973b226f68870db41016157fca2d3a5b4f9e` |
| [`scripts/f29-arq01-arquitectura.ps1`](scripts/f29-arq01-arquitectura.ps1) | Script de construcción o validación | `d34a81fec286028bfd37d66888346b9d62b1162836791c00989aa82a65a9d3f1` |
| [`scripts/f29-f3-bpmn-asis.ps1`](scripts/f29-f3-bpmn-asis.ps1) | Script de construcción o validación | `d0f25ccb324ba35c36c0e9f39922bf81397d73bbf668e8331ac9303ed73bae4f` |
| [`scripts/f29-f5-bpmn-tobe.ps1`](scripts/f29-f5-bpmn-tobe.ps1) | Script de construcción o validación | `008389529182fa9102bc85b6f0d8231908582dd0c248a2b0d6d9803c76157a8a` |
| [`scripts/f29-f8-casos-de-uso.ps1`](scripts/f29-f8-casos-de-uso.ps1) | Script de construcción o validación | `350463d0510c737ebe439036ea7d4fd2f47d01ba384baa5204640699be56fdd7` |
| [`scripts/f29lib.ps1`](scripts/f29lib.ps1) | Script de construcción o validación | `2c973c8aadf93acb09f05556b75e28109cb1492e29ed4aa9acee5357ef5f1f96` |
| [`scripts/make_f29_docs.py`](scripts/make_f29_docs.py) | Script de construcción o validación | `d5b2e194bab5c116312fc35dfe243e771f3f87b7f0efb8895ff1b9ce319ebcbd` |
| [`scripts/svg2png.py`](scripts/svg2png.py) | Script de construcción o validación | `befa8f03d16df16fff84a599c3d58f847d7ed6da83c09fb60664482f36fe386e` |
| [`scripts/validate_f29.py`](scripts/validate_f29.py) | Script de construcción o validación | `eed0e4575383f68083be401dcec74be864f0d248fe7d72af8aa16ad06dc3ed07` |
| [`validation/ARQ01_model_check.txt`](validation/ARQ01_model_check.txt) | Informe de verificación (salida de los scripts) | `354532f60593a43f7489ff197cfdb7d0c21845c7bb80eff19c4098e72469ef92` |
| [`validation/F3_model_check.txt`](validation/F3_model_check.txt) | Informe de verificación (salida de los scripts) | `370473b6151f130df6f556b74d93037587138b1494e4c91897867ccdeb3fff40` |
| [`validation/F5_model_check.txt`](validation/F5_model_check.txt) | Informe de verificación (salida de los scripts) | `66a91442488e10ed51293f0d4aeed1ed80b61293e51e3fc5c6ec242e6612cda9` |
| [`validation/F8_model_check.txt`](validation/F8_model_check.txt) | Informe de verificación (salida de los scripts) | `e1c7afd708e351ca8b26becb14cc82538135ec3af851af2f3999a572ffbd96e9` |
| [`evidencias/f29b/01_prueba_editor_subsimbolos_sin_contenido.png`](evidencias/f29b/01_prueba_editor_subsimbolos_sin_contenido.png) | Evidencia diagnóstica del hotfix F29B (captura real del editor o exportación de prueba) | `2b440ebf2229ce65d21548c0798a4dcdc2fc822c0bee52d7eeda1fa0bf390e00` |
| [`evidencias/f29b/02_prueba_editor_diagrama_por_defecto_con_contenido.png`](evidencias/f29b/02_prueba_editor_diagrama_por_defecto_con_contenido.png) | Evidencia diagnóstica del hotfix F29B (captura real del editor o exportación de prueba) | `15ef707dc632558787aea6a34ed81a2a5d0813bdfef6280d30cde58ec81987bb` |
| [`evidencias/f29b/03_prueba_exportacion_duplica_diagrama_por_defecto.png`](evidencias/f29b/03_prueba_exportacion_duplica_diagrama_por_defecto.png) | Evidencia diagnóstica del hotfix F29B (captura real del editor o exportación de prueba) | `0d04e5b7dff83bce28da588d8a46bec3e6bad547ba2e3151f3e5ae70ca017508` |
| [`evidencias/f29b/04_prueba_exportacion_con_detalle_sin_duplicados.png`](evidencias/f29b/04_prueba_exportacion_con_detalle_sin_duplicados.png) | Evidencia diagnóstica del hotfix F29B (captura real del editor o exportación de prueba) | `8827bc4982a751df4d1d6bae9b178b9bbe8525cdd61a8750b18a25ad2cac73fc` |
| [`evidencias/f29b/05_editor_F3_SP-01_detalle_tras_recarga.png`](evidencias/f29b/05_editor_F3_SP-01_detalle_tras_recarga.png) | Evidencia diagnóstica del hotfix F29B (captura real del editor o exportación de prueba) | `880aa1be42de5e22c3098006bd7f932f5deb6128e0ccbd229efe160579a428a8` |
| [`evidencias/f29b/06_editor_F5_SP-P_detalle_tras_recarga.png`](evidencias/f29b/06_editor_F5_SP-P_detalle_tras_recarga.png) | Evidencia diagnóstica del hotfix F29B (captura real del editor o exportación de prueba) | `3c063c6c742eefc9ce9922315deee5ac4f39883a458995db2c0089eed2ca23d8` |

## Capturas de PowerDesigner

**PENDING RETAKE.** Las capturas manuales del equipo se tomaron antes del hotfix F29B y muestran el estado anterior de los modelos (geometría reajustada al abrir y subprocesos sin contenido en el editor). No se registran como evidencia final ni se versionan todavía; se repiten según [`evidencias/capturas/CAPTURAS_PENDIENTES.md`](evidencias/capturas/CAPTURAS_PENDIENTES.md). Detalle en [`F29B_HOTFIX.md`](F29B_HOTFIX.md).

| Captura | Vista | Estado |
|---|---|---|
| `F3_BPMN_ASIS_PowerDesigner.png` | F3 (vista principal) | PENDING RETAKE |
| `F5_BPMN_TOBE_PowerDesigner_parte1.png` | F5 (vista principal, parte 1) | PENDING RETAKE |
| `F5_BPMN_TOBE_PowerDesigner_parte2.png` | F5 (vista principal, parte 2) | PENDING RETAKE |
| `F8_Casos_de_Uso_PowerDesigner.png` | F8 | PENDING RETAKE |
| `ARQ01_Arquitectura_Conceptual_PowerDesigner.png` | ARQ-01 | PENDING RETAKE |
| `F3_SP-01_detalle_PowerDesigner.png` | F3, diagrama de detalle de SP-01 (nueva) | PENDING RETAKE |
| `F5_SP-P_detalle_PowerDesigner.png` | F5, diagrama de detalle de SP-P (nueva) | PENDING RETAKE |
