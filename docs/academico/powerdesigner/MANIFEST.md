# Manifiesto F29 — modelos y exportaciones de PowerDesigner

Generado por [`scripts/make_f29_docs.py`](scripts/make_f29_docs.py). **SHA-256 del contenido versionado** (`git show :<ruta>`, el blob que se confirma): git normaliza a LF los finales de línea de `.bpm`, `.oom` y `.svg`, así que el hash del archivo de trabajo en Windows (CRLF) puede diferir; el del blob es reproducible en cualquier checkout.

**Estado:** FORMALIZADO — pendiente de la auditoría F29. Ningún formato (DOCX o PDF) se sustituyó todavía.

## Modelos y exportaciones

| Artefacto | Tipo | Modelo fuente | Diagrama | Formato | SHA-256 | Estado |
|---|---|---|---|---|---|---|
| [`models/F29_BPM_Academico.bpm`](models/F29_BPM_Academico.bpm) | Modelo BPM (BPMN 2.0 Descriptive) | — | F3 - BPMN AS-IS; F5 - BPMN TO-BE | BPM (XML) | `0db229ef063c16dae878a5d5ec50f53686389ba8f49caea3264870927a345c3b` | FORMALIZADO |
| [`models/F29_UML_Academico.oom`](models/F29_UML_Academico.oom) | Modelo OOM (UML, Analysis) | — | F8 - Casos de Uso Academicos; ARQ-01 - Arquitectura Conceptual | OOM (XML) | `da5af8929bd70f2bc854d44985a6001173330f2922f5b9858b22036a14349bd1` | FORMALIZADO |
| [`exports/F3_BPMN_ASIS.png`](exports/F3_BPMN_ASIS.png) | Exportación | F29_BPM_Academico.bpm | F3 - BPMN AS-IS | PNG (rasterizado del SVG, escala 2) | `279e05f75fd270c26d8f39d490d4441f1364532b07f5a4d252410f7004e53608` | FORMALIZADO |
| [`exports/F3_BPMN_ASIS.svg`](exports/F3_BPMN_ASIS.svg) | Exportación | F29_BPM_Academico.bpm | F3 - BPMN AS-IS | SVG (exportación nativa) | `176dcbff23824f0e40912e7c2782d5d3178ed602ad0477fdf186f9ca98d77bbc` | FORMALIZADO |
| [`exports/F5_BPMN_TOBE.png`](exports/F5_BPMN_TOBE.png) | Exportación | F29_BPM_Academico.bpm | F5 - BPMN TO-BE | PNG (rasterizado del SVG, escala 2) | `51bc26dbb1d9ca57f8df1c62dba5e31c9f70a389eac2d8d1b6f3b42e12a35877` | FORMALIZADO |
| [`exports/F5_BPMN_TOBE.svg`](exports/F5_BPMN_TOBE.svg) | Exportación | F29_BPM_Academico.bpm | F5 - BPMN TO-BE | SVG (exportación nativa) | `b8b0a3a00c785a6ff33d97ba33a39731649f9715aea5cef0201d1c134e2d5870` | FORMALIZADO |
| [`exports/F8_Casos_de_Uso_Academicos.png`](exports/F8_Casos_de_Uso_Academicos.png) | Exportación | F29_UML_Academico.oom | F8 - Casos de Uso Academicos | PNG (rasterizado del SVG, escala 2) | `94dee7b176dbd529385392b82e60b81c5cc3b1ebfad829da7481b7f931f05aa3` | FORMALIZADO |
| [`exports/F8_Casos_de_Uso_Academicos.svg`](exports/F8_Casos_de_Uso_Academicos.svg) | Exportación | F29_UML_Academico.oom | F8 - Casos de Uso Academicos | SVG (exportación nativa) | `58a0090ff7b558b711e906d8c3ea7348bb25b2b1855c198e376bdb76de84daae` | FORMALIZADO |
| [`exports/ARQ-01_Arquitectura_Conceptual.png`](exports/ARQ-01_Arquitectura_Conceptual.png) | Exportación | F29_UML_Academico.oom | ARQ-01 - Arquitectura Conceptual | PNG (rasterizado del SVG, escala 2) | `4084af202f7af08adca7545c4ea3fe3906c8d0d575da3e946385f168047e3ee5` | FORMALIZADO |
| [`exports/ARQ-01_Arquitectura_Conceptual.svg`](exports/ARQ-01_Arquitectura_Conceptual.svg) | Exportación | F29_UML_Academico.oom | ARQ-01 - Arquitectura Conceptual | SVG (exportación nativa) | `fc04ae318e1ab0c905cf721e76ee75b4926a814bf27c80da7d624e9ed4948795` | FORMALIZADO |

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
| [`scripts/f29-arq01-arquitectura.ps1`](scripts/f29-arq01-arquitectura.ps1) | Script de construcción o validación | `71d750c8518577e4c2e77f86e1a3b6bd607dea07e28cbd49bcb60f7b0d20adee` |
| [`scripts/f29-f3-bpmn-asis.ps1`](scripts/f29-f3-bpmn-asis.ps1) | Script de construcción o validación | `8ba35c2438fb3072d5d70ed165fd032724f9463b4bbf2dc50e211ec31b974c25` |
| [`scripts/f29-f5-bpmn-tobe.ps1`](scripts/f29-f5-bpmn-tobe.ps1) | Script de construcción o validación | `4ec4560bcf8e6c4e85e65bb2a3792b94b08773325220a6d27ed43deff600f531` |
| [`scripts/f29-f8-casos-de-uso.ps1`](scripts/f29-f8-casos-de-uso.ps1) | Script de construcción o validación | `87f490ca4bd46d1897ed95e00b486ec9bb7ea147ea9d412389c47ce35b2d8468` |
| [`scripts/f29lib.ps1`](scripts/f29lib.ps1) | Script de construcción o validación | `70512d4a25ebe7d6017a55136180f161879b6fd1897021ae49d7bbbe4f212309` |
| [`scripts/make_f29_docs.py`](scripts/make_f29_docs.py) | Script de construcción o validación | `9df9ebed3ea132dcf8fa0eccd2fe58b8c8936a3e4e34fdabb032705d241fd80c` |
| [`scripts/svg2png.py`](scripts/svg2png.py) | Script de construcción o validación | `befa8f03d16df16fff84a599c3d58f847d7ed6da83c09fb60664482f36fe386e` |
| [`scripts/validate_f29.py`](scripts/validate_f29.py) | Script de construcción o validación | `a308b46fa439c64d1c0e05c6d90103fd89c2fc83accd9d40b2b1a977c57e908b` |
| [`validation/ARQ01_model_check.txt`](validation/ARQ01_model_check.txt) | Informe de verificación (salida de los scripts) | `955571409dd8d74d009b8d6be4fd220168428601d3a5102dad561a52c8a51315` |
| [`validation/F3_model_check.txt`](validation/F3_model_check.txt) | Informe de verificación (salida de los scripts) | `77899dfc1316769c640537fabb42757382eff3d963667e4d2da3a7554167a454` |
| [`validation/F5_model_check.txt`](validation/F5_model_check.txt) | Informe de verificación (salida de los scripts) | `12f8b5d892d825ecfecf617179f5247e0328051d6e77a27975875389dc45e49d` |
| [`validation/F8_model_check.txt`](validation/F8_model_check.txt) | Informe de verificación (salida de los scripts) | `d611765508b782978e948e053758634f23d674c3db01b1512b8071e2584fd263` |

## Capturas de PowerDesigner

No se incluyen capturas: no fue posible tomarlas de forma fiable desde la sesión automatizada. Instrucciones para tomarlas a mano en [`evidencias/capturas/CAPTURAS_PENDIENTES.md`](evidencias/capturas/CAPTURAS_PENDIENTES.md).
