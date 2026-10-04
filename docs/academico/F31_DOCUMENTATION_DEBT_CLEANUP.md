# F31 — cierre de deuda LOW y saneamiento documental

Fecha: 02/10/2026; correcciones de auditoría verificadas el 03/10/2026. **F31 CERRADA con observaciones aceptadas/futuras**: auditoría final **PASS WITH OBSERVATIONS**, apta para commit e integración autorizada con CI obligatorio. Alcance: documentación y artefactos académicos; **sin cambios de comportamiento productivo, RF, CU, RNF o ML**.

## Deudas objetivo

| ID | Estado F31 | Evidencia y decisión |
|---|---|---|
| H-14 | **RESUELTA** | El Formato 04 perdía `w:headerReference` al reconstruir su cuerpo. El generador conserva las referencias oficiales de encabezado/pie cuando no queda ninguna; DOCX/PDF regenerados, «Asignatura» visible y extraíble |
| F28-L01 | **NO APLICA** | El F11 adaptado histórico sí muestra visualmente la cabecera y «Asignatura». La omisión era de la capa/extractor usado en F28; el artefacto histórico se preserva sin cambios |
| F29-L01 | **ACEPTADA** | `RepositoryFilename` es metadata que PowerDesigner 16.6 reescribe con la ruta del archivo abierto. No se consume al reproducir, validar ni exportar; la API COM no expone una edición segura y la política prohíbe manipular el XML nativo a mano |
| F29-L02 | **RESUELTA** | Ajuste incremental de `CenterTextOffset` y saltos de línea de rótulos en las 24 dependencias de R-01…R-20; 17 componentes, 6 agrupaciones, palabras, extremos y rutas intactos; modelo guardado/reabierto y SVG reproducible |
| F29B-OBS-01 | **ACEPTADA** | Limitación demostrada de PowerDesigner 16.6: la vista principal del editor no muestra el contenido compuesto sin duplicarlo en la exportación. Los diagramas de detalle y exports reproducibles preservan el contenido completo |

## Otras LOW/OBS revisadas

| Deuda | Estado | Justificación |
|---|---|---|
| Gobierno activo pre-release (`CLAUDE.md`, `README.md`, `docs/PROGRESS.md`) | **RESUELTA** | Sincronizado con `develop`/`main` y con F27–F30; la historia queda en `GOVERNANCE_DEBT.md` |
| F11 activo aún referenciado como adaptado por F29 | **RESUELTA** | El manifiesto, la trazabilidad y `validate_f29.py` usan el F11 definitivo oficial; el adaptado permanece histórico |
| F30: rango oficial O01–O14 y estado pendiente | **RESUELTA** | Corregido a O01–O16 y estado auditado/integrado; no cambia ningún claim |
| Pint y `vp check` sobre código | **FUTURA** | Requieren una fase de formato con regresión funcional; F31 no toca runtime |
| Lector de pantalla real, hardware modesto y revisión manual 375 px | **FUTURA** | Evidencia manual no documental; no puede cerrarse con edición de textos |
| Fontaine opcional | **ACEPTADA** | Aviso informativo del build; instalarlo sería agregar una dependencia sin necesidad funcional |
| Observaciones históricas de F23/F24/F26 | **ACEPTADA** | Permanecen en informes cerrados como evidencia temporal; no se reescriben retrospectivamente |
| CI de `main` F29C, registrada en F29F | **NO APLICA al estado actual** | Es un hecho histórico de esa ejecución. F29D–F30 se integraron después en `main`; F31 no convierte retrospectivamente ese resultado en PASS |

## Correcciones de la auditoría F31

El primer ajuste de F29-L02 no bastaba: B-01 identificó rótulos sobre bordes o ambiguos. Se conserva ese antecedente; la resolución se sustenta ahora en la reexportación corregida, no en el primer intento.

| Hallazgo | Corrección y evidencia |
|---|---|
| B-01 — ARQ-01 | R-08 separado de C05, R-07 separado de C06 y R-17 fuera de los bordes de negocio. R-01/R-02 y R-05…R-11 quedan junto a sus propios segmentos; R-06/R-07 no se confunden con R-08/R-12. Una configuración compartida conserva offsets y saltos de línea en construcción y ajuste incremental. Recarga: 55 símbolos, 0 cambios de geometría y SVG repetible |
| B-02 — F11-R | `f11r.py` genera «sin rediseñarla semánticamente», describe el ajuste visual F31 y regenera `F11R_REGULARIZACION.md` con su SHA-256 vigente. F11 definitivo y F29H regenerados con el PNG formal actualizado |
| Validación F29 tautológica | Sustituida por ruta/nombre/SHA-256 de la captura externa del F11 en evidencias y MANIFEST. La prueba negativa sin registro falla correctamente; se mantienen 225 comprobaciones |
| Excepciones de alcance permanentes | Ya no dependen de la existencia del informe F31. Solo se permiten archivos concretos en la rama F31 y su HEAD base aprobado; la excepción expira al cambiar rama o HEAD. Runtime, ML, F9, F23 y F11 adaptado no quedan exceptuados |
| README F4 / H-14 | Causa y antecedente conciliados. Comprobación automática mínima exige «Asignatura: Pruebas y Calidad de Software» en operadores textuales del PDF; una cadena en metadata no basta |
| Estado de gobierno | Durante la corrección, PROGRESS y ACADEMIC_BASELINE conservaron F31 en curso; tras la auditoría final aprobada, el commit C registra su cierre con observaciones aceptadas/futuras |

## Validación de las correcciones (sin cierre Git)

- `validate.py`: **0 fallas**.
- `validate.py --cierre-f29`: **0 fallas**, cierre F29 admitido; F11-R **16/16 PASS**.
- `validate_f30.py`: **OK** — 107 fuentes, 107 citadas, 30 decisiones y 49 herramientas.
- `validate_f29.py`: **225/225**, 0 fallas.
- Enlaces relativos: **747 revisados, 0 rotos**.
- `MANIFEST.md`: **61 referencias, 0 discrepancias** (incluye la nueva configuración compartida de rótulos).
- Evidencias: **121 referencias / 91 archivos únicos, 0 fallas**.
- MANIFEST y evidencias: mismos resultados sobre un índice temporal con staging simulado; el índice real permanece intacto.
- `git diff --check`: **PASS**; solo informa la normalización CRLF→LF prevista para el OOM/SVG de PowerDesigner.
- F4: la cabecera se comprobó visualmente y en los streams textuales del PDF; «Asignatura» y «Pruebas y Calidad de Software» son texto, no una imagen rasterizada.
- ARQ-01: PNG/SVG reexportados desde el modelo reabierto, rótulos solicitados separados de cajas/bordes y asociados a su propia relación. El grafo del OOM (IDs, nombres normalizados, estereotipos y extremos), los rectángulos y las rutas coinciden con HEAD.
- F11 (14 páginas) y F29H (28 páginas): renderizado de todas las páginas y revisión visual, con revisión ampliada de ARQ-01 y de los dos recortes del F11; sin nuevos cortes o solapamientos. F30 conserva la revisión visual de la primera pasada F31 y su validación reproducible.
- No se ejecutaron suites funcionales: el alcance no modifica Laravel, React, ML, base de datos ni dependencias.

## Salvaguardas

## Cierre autorizado y trazabilidad Git

Orden aprobado por el equipo: **A → B → C**, sin squash, rebase ni amend.

| Commit | Hash / identificación | Alcance |
|---|---|---|
| A | `99aa4bc972d57b0b67e44cd1b7f8a9dd346f5095` | `fix(academic): restore official F4 header in generated artifacts` — F4/H-14 y sus hunks específicos del validador |
| B | `359122e8589e0d2e2ba7b5d0de13ad111e7013d7` | `fix(powerdesigner): clean ARQ-01 relation labels and refresh evidence` — ARQ-01, evidencia, F11/F29H y scripts |
| C | Este commit, identificable en `git log` por `docs(governance): close F31 documentation debt and synchronize active state` | Gobierno, estado F30 y controles de alcance; su hash se obtiene tras confirmarlo, sin autorreferencia |

Base previa: `develop` `2bf2a1eaba1d76bf7d45e0e9aa7887e6758d13e6`; `main` `59849c382df43f7c272e450d5bd7c610efe4e016`. La publicación e integración siguen este orden: push de feature, merge no-ff y push a develop, CI develop verde, merge no-ff y push a main, CI main verde. Los resultados y hashes finales se registran en Git/GitHub Actions y en el reporte de ejecución, no se inventan antes de ejecutarlos. **Sin tag ni release nuevos; feature preservada.** Las observaciones aceptadas/futuras de las tablas anteriores permanecen vigentes.

### Contratos preservados

- RF-01…RF-27 y CU-01…CU-20 no cambian.
- RF-23 permanece como decisión final humana.
- RF-29 permanece experimental, operacional e informativo; F31 no modifica el servicio ML.
- Los modelos históricos de F23 no se abren ni se modifican.
- El F11 adaptado histórico no se regenera.
- No se instalan dependencias ni se ejecutan suites funcionales porque el diff es documental.
