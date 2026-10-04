# Manifiesto F29 — modelos y exportaciones de PowerDesigner

Generado por [`scripts/make_f29_docs.py`](scripts/make_f29_docs.py). **SHA-256 del contenido que se versionará**: los formatos textuales se normalizan a LF, como hace git, por lo que los hashes son reproducibles en cualquier checkout.

**Estado (28/09/2026): F29 CLOSED WITH DOCUMENTED OBSERVATIONS.** F29 AUDITED (con observaciones), F29B AUDITED / APPROVED, capturas COMPLETED (7, reales), exportaciones formales INTEGRATED en los Formatos 03, 05, 08 y 11 y sus DOCX y PDF UPDATED. Cierre F31: F29-L02 RESUELTA; F29-L01 y F29B-OBS-01 ACEPTADAS por limitación de PowerDesigner, sin impacto semántico ni de portabilidad.

## Modelos y exportaciones

| Artefacto | Tipo | Modelo fuente | Diagrama | Formato | SHA-256 | Estado |
|---|---|---|---|---|---|---|
| [`models/F29_BPM_Academico.bpm`](models/F29_BPM_Academico.bpm) | Modelo BPM (BPMN 2.0 Descriptive) | — | F3 - BPMN AS-IS; F5 - BPMN TO-BE | BPM (XML) | `ebe6b96309cdc20c2be2e570c2343527bc0242524f3ddcad320b97b8a4593932` | AUDITED |
| [`models/F29_UML_Academico.oom`](models/F29_UML_Academico.oom) | Modelo OOM (UML, Analysis) | — | F8 - Casos de Uso Academicos; ARQ-01 - Arquitectura Conceptual | OOM (XML) | `13465d9ed9cd1f0778803ce7b7cb5f90c6242119ec1bde191eb7307ac33d1574` | AUDITED |
| [`exports/F3_BPMN_ASIS.png`](exports/F3_BPMN_ASIS.png) | Exportación | F29_BPM_Academico.bpm | F3 - BPMN AS-IS | PNG (rasterizado del SVG, escala 2) | `685a9380cf24b0b21d93e6efdcee67b60fd5ca8f52d3746c8930fbd1b3de2df5` | AUDITED · INTEGRATED |
| [`exports/F3_BPMN_ASIS.svg`](exports/F3_BPMN_ASIS.svg) | Exportación | F29_BPM_Academico.bpm | F3 - BPMN AS-IS | SVG (exportación nativa) | `12189d6b13c860e22faa51313615887b8ae2b934d9c9aefbb8ae8d90aee0ae9e` | AUDITED · INTEGRATED |
| [`exports/F5_BPMN_TOBE.png`](exports/F5_BPMN_TOBE.png) | Exportación | F29_BPM_Academico.bpm | F5 - BPMN TO-BE | PNG (rasterizado del SVG, escala 2) | `b3af8824cc3ad92e814e2d62d79ce584450699ad5f5a0cfec7f52f4036447d67` | AUDITED · INTEGRATED |
| [`exports/F5_BPMN_TOBE.svg`](exports/F5_BPMN_TOBE.svg) | Exportación | F29_BPM_Academico.bpm | F5 - BPMN TO-BE | SVG (exportación nativa) | `3615cc3fe137ef6fe6b8c6cbc89944d07db2241a54c15bf7b2316640f49c046b` | AUDITED · INTEGRATED |
| [`exports/F8_Casos_de_Uso_Academicos.png`](exports/F8_Casos_de_Uso_Academicos.png) | Exportación | F29_UML_Academico.oom | F8 - Casos de Uso Academicos | PNG (rasterizado del SVG, escala 2) | `94dee7b176dbd529385392b82e60b81c5cc3b1ebfad829da7481b7f931f05aa3` | AUDITED · INTEGRATED |
| [`exports/F8_Casos_de_Uso_Academicos.svg`](exports/F8_Casos_de_Uso_Academicos.svg) | Exportación | F29_UML_Academico.oom | F8 - Casos de Uso Academicos | SVG (exportación nativa) | `307d84ed1199e75668390b22806ec192524556c13498529b3272c242e12e705d` | AUDITED · INTEGRATED |
| [`exports/ARQ-01_Arquitectura_Conceptual.png`](exports/ARQ-01_Arquitectura_Conceptual.png) | Exportación | F29_UML_Academico.oom | ARQ-01 - Arquitectura Conceptual | PNG (rasterizado del SVG, escala 2) | `eb4065a2b703413730d13bab1b1567e3cd3b872eba7bee02454d25265bde2e5d` | AUDITED · INTEGRATED |
| [`exports/ARQ-01_Arquitectura_Conceptual.svg`](exports/ARQ-01_Arquitectura_Conceptual.svg) | Exportación | F29_UML_Academico.oom | ARQ-01 - Arquitectura Conceptual | SVG (exportación nativa) | `885b95cd1ce339267a2debc8c6a555c7835cc60b99dccb3f44a3bdab65c8259d` | AUDITED · INTEGRATED |

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
| [`scripts/capture_f29_views.ps1`](scripts/capture_f29_views.ps1) | Script de construcción o validación | `fdf4e29c028a490265e025534bdda2d70ecd377f9eb9d7e73c5839384f526710` |
| [`scripts/f29-arq01-arquitectura.ps1`](scripts/f29-arq01-arquitectura.ps1) | Script de construcción o validación | `d810029ee563d12483f546e24d2c2cee35c970fea2a5b7be6e7016a39ed29013` |
| [`scripts/f29-f3-bpmn-asis.ps1`](scripts/f29-f3-bpmn-asis.ps1) | Script de construcción o validación | `d0f25ccb324ba35c36c0e9f39922bf81397d73bbf668e8331ac9303ed73bae4f` |
| [`scripts/f29-f5-bpmn-tobe.ps1`](scripts/f29-f5-bpmn-tobe.ps1) | Script de construcción o validación | `008389529182fa9102bc85b6f0d8231908582dd0c248a2b0d6d9803c76157a8a` |
| [`scripts/f29-f8-casos-de-uso.ps1`](scripts/f29-f8-casos-de-uso.ps1) | Script de construcción o validación | `350463d0510c737ebe439036ea7d4fd2f47d01ba384baa5204640699be56fdd7` |
| [`scripts/f29lib.ps1`](scripts/f29lib.ps1) | Script de construcción o validación | `2c973c8aadf93acb09f05556b75e28109cb1492e29ed4aa9acee5357ef5f1f96` |
| [`scripts/f31-arq01-label-cleanup.ps1`](scripts/f31-arq01-label-cleanup.ps1) | Script de construcción o validación | `5b4a5475da26bd414a75438d56cc24cf95b8202a5ffaf15888410c663228bd97` |
| [`scripts/f31-arq01-label-layout.ps1`](scripts/f31-arq01-label-layout.ps1) | Script de construcción o validación | `6b362696a4e96dcbbc3056fb4f6f246c6ca0df07872522208f83653b5387cc3c` |
| [`scripts/make_f29_docs.py`](scripts/make_f29_docs.py) | Script de construcción o validación | `03cb26f6ce649da6db27117c39a430aa0d5a888e28cc02ef5c139c5a8ecc3920` |
| [`scripts/svg2png.py`](scripts/svg2png.py) | Script de construcción o validación | `befa8f03d16df16fff84a599c3d58f847d7ed6da83c09fb60664482f36fe386e` |
| [`scripts/validate_f29.py`](scripts/validate_f29.py) | Script de construcción o validación | `5da90b58657369ad31eda04fb53aa8c1167a842bbd46b2ca49bb870c51128011` |
| [`validation/ARQ01_model_check.txt`](validation/ARQ01_model_check.txt) | Informe de verificación (salida de los scripts) | `354532f60593a43f7489ff197cfdb7d0c21845c7bb80eff19c4098e72469ef92` |
| [`validation/F31_ARQ01_label_cleanup.txt`](validation/F31_ARQ01_label_cleanup.txt) | Informe de verificación (salida de los scripts) | `3cbf4719586d5142c40fe908e2358238b24809453450fffe4b9402af04f557ef` |
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

**COMPLETED.** Son capturas reales de la ventana de PowerDesigner 16.6, tomadas el 28/09/2026 con los modelos reabiertos desde el disco ([`scripts/capture_f29_views.ps1`](scripts/capture_f29_views.ps1), registro en [`evidencias/capturas/CAPTURAS_PENDIENTES.md`](evidencias/capturas/CAPTURAS_PENDIENTES.md)). Ninguna es simulada. Sustituyen a las cinco anteriores al hotfix F29B (RETAKE REQUIRED, nunca versionadas).

| Captura | Tipo | Modelo fuente | Vista | SHA-256 | Estado |
|---|---|---|---|---|---|
| [`evidencias/capturas/F3_BPMN_ASIS_PowerDesigner.png`](evidencias/capturas/F3_BPMN_ASIS_PowerDesigner.png) | Captura PNG | F29_BPM_Academico.bpm | F3 - BPMN AS-IS | `92d1aad40f7027f10e3a360b6a0c84a1ec9c2cf4338a085310ba9f3bed728986` | VALID |
| [`evidencias/capturas/F3_SP-01_detalle_PowerDesigner.png`](evidencias/capturas/F3_SP-01_detalle_PowerDesigner.png) | Captura PNG | F29_BPM_Academico.bpm | SP-01 Evaluar al candidato — detalle (F29B-OBS-01) | `76c33fff908a8dfa8c981ea73185e2fc449cae14d702996638f527045d0ea46f` | VALID |
| [`evidencias/capturas/F5_BPMN_TOBE_PowerDesigner_parte1.png`](evidencias/capturas/F5_BPMN_TOBE_PowerDesigner_parte1.png) | Captura PNG | F29_BPM_Academico.bpm | F5 - BPMN TO-BE, parte 1 | `2d0e66eee8b1b599c9bd6bd90963e0dc71d9444b8a1aecc8bc21e76676352a23` | VALID |
| [`evidencias/capturas/F5_BPMN_TOBE_PowerDesigner_parte2.png`](evidencias/capturas/F5_BPMN_TOBE_PowerDesigner_parte2.png) | Captura PNG | F29_BPM_Academico.bpm | F5 - BPMN TO-BE, parte 2 | `2ed5c40ff80300eb50d68368d11852a1a21b257ab49d3bc1cf8ca4122ae9b2f5` | VALID |
| [`evidencias/capturas/F5_SP-P_detalle_PowerDesigner.png`](evidencias/capturas/F5_SP-P_detalle_PowerDesigner.png) | Captura PNG | F29_BPM_Academico.bpm | SP-P Gestionar la postulación — detalle (F29B-OBS-01) | `aefbcf0026f63592a77c96d079d58de7f78bd85da5e72c6fd207a0fee3569ded` | VALID |
| [`evidencias/capturas/F8_Casos_de_Uso_PowerDesigner.png`](evidencias/capturas/F8_Casos_de_Uso_PowerDesigner.png) | Captura PNG | F29_UML_Academico.oom | F8 - Casos de Uso Academicos | `e842cc0cd84e105205ff66ef056a32afc132a2f9cc795a5f2ab24076643ebc6c` | VALID |
| [`evidencias/capturas/ARQ01_Arquitectura_Conceptual_PowerDesigner.png`](evidencias/capturas/ARQ01_Arquitectura_Conceptual_PowerDesigner.png) | Captura PNG | F29_UML_Academico.oom | ARQ-01 - Arquitectura Conceptual | `dc26391f8c4b84e1db9b46382a50e3c86b05b5709ebce2ddede2449947931810` | VALID |

## Formatos integrados

El diagrama principal de cada formato es la exportación formal de esta tabla de modelos. Los DOCX se generan con [`tools/f27b/build.py`](../tools/f27b/build.py) y los PDF, con Microsoft Word ([`tools/f27b/topdf.ps1`](../tools/f27b/topdf.ps1)).

| Formato | Tipo | Exportación integrada | SHA-256 | Estado |
|---|---|---|---|---|
| [`practica-03/F3_Diagrama_BPM_ASIS_Colegio_Andino.docx`](../practica-03/F3_Diagrama_BPM_ASIS_Colegio_Andino.docx) | DOCX | `F3_BPMN_ASIS.png` | `a15d40ba597b34cd36541c7bc5eb58e4456faf5c17da77d4c695e9567bf2f7d3` | UPDATED |
| [`practica-03/F3_Diagrama_BPM_ASIS_Colegio_Andino.pdf`](../practica-03/F3_Diagrama_BPM_ASIS_Colegio_Andino.pdf) | PDF | `F3_BPMN_ASIS.png` | `c6311e2bf9dae98e3e32ad76fb75bd0b1f959450519d075ffcfa13a0a0efb6ff` | UPDATED |
| [`practica-05/F5_Modelo_BPM_TOBE_Colegio_Andino.docx`](../practica-05/F5_Modelo_BPM_TOBE_Colegio_Andino.docx) | DOCX | `F5_BPMN_TOBE.png` | `bde8acfbdd34e9f122c234a78cd422e04d2caca00234a0a86e51fb8cb60db14c` | UPDATED |
| [`practica-05/F5_Modelo_BPM_TOBE_Colegio_Andino.pdf`](../practica-05/F5_Modelo_BPM_TOBE_Colegio_Andino.pdf) | PDF | `F5_BPMN_TOBE.png` | `b97e5b358c588cdd000b47aec59ef59f848e0b06287e03c678b265d8abdd6489` | UPDATED |
| [`practica-08/F8_Diagrama_Casos_de_Uso_Colegio_Andino.docx`](../practica-08/F8_Diagrama_Casos_de_Uso_Colegio_Andino.docx) | DOCX | `F8_Casos_de_Uso_Academicos.png` | `2dcc4de9c8d3d90496b34b02c0336f30fb446ab29c71c804f292be8fd9b9c835` | UPDATED |
| [`practica-08/F8_Diagrama_Casos_de_Uso_Colegio_Andino.pdf`](../practica-08/F8_Diagrama_Casos_de_Uso_Colegio_Andino.pdf) | PDF | `F8_Casos_de_Uso_Academicos.png` | `215157ebc0870b95ea1d5364c854a27adcbbdcfce0b1bcfc6755569505c17633` | UPDATED |
| [`practica-11/F11_Arquitectura_del_Sistema_Colegio_Andino.docx`](../practica-11/F11_Arquitectura_del_Sistema_Colegio_Andino.docx) | DOCX | `ARQ-01_Arquitectura_Conceptual.png` | `40bbaacd12be0af46d35620d6be7aa6bb75c22db49cc02834e79a12eebc3715d` | UPDATED |
| [`practica-11/F11_Arquitectura_del_Sistema_Colegio_Andino.pdf`](../practica-11/F11_Arquitectura_del_Sistema_Colegio_Andino.pdf) | PDF | `ARQ-01_Arquitectura_Conceptual.png` | `bd4a039868f1caf8edec2ef2348f26eda86361400d7cdca0606e86f13c1709d1` | UPDATED |

## Documentación de validación y del hotfix

| Documento | Contenido | SHA-256 |
|---|---|---|
| [`README.md`](README.md) | Estado, contenido, reproducción y decisiones de modelado | `c9d9e62410603fda5da019397c85cecb9e9e9bc56832d3648b7f63e9d72b76c9` |
| [`F29_VALIDATION.md`](F29_VALIDATION.md) | Resultado PASS/OBS por vista | `e1abbc4313b7b08d82eb54c1e753ae11035373ee308c8aaaaab5018d7e01f258` |
| [`F29B_HOTFIX.md`](F29B_HOTFIX.md) | Hotfix F29B: causa raíz, corrección, pruebas de recarga y F29B-OBS-01 | `14ae1d839bf9643df813c28e5c18849fd065300c0c906b0708612587b1a5d2a7` |
| [`evidencias/capturas/CAPTURAS_PENDIENTES.md`](evidencias/capturas/CAPTURAS_PENDIENTES.md) | Registro de las capturas (STATUS: COMPLETED) | `e16ebbce7fa5fca8f78573cf5d1971280b78f216d4cc436ff75ff9fc55f29890` |
