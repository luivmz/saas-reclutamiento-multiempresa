# F35-SBX-A — Aislamiento multiempresa y almacenamiento experimental

> Fase F35-SBX-A, versión 1 (07/10/2026). Equivalente sintético del contrato 5 del proyecto: toda pieza pertenece a una sola organización y ninguna referencia cruza tenants.

## 1. Aislamiento por tenant sintético

- Un fixture por organización: `ORG-S1`, `ORG-S2` y `ORG-S3`. El nombre del archivo, `fixture_id`, `tenant`, `run` y cada pieza llevan la misma organización.
- Cada identificador incluye el tenant (`SBXE-ORG-S1-000001`). Un identificador de otro tenant falla.
- La fila F34 de origen y el criterio (`CRI-NNNN`) pertenecen a la misma organización, comprobado con `applications.csv`, `vacancies.csv` y `criteria.csv` de F34.
- Ninguna evidencia, fuente ni origen F34 se repite entre tenants.
- El actor simulado de la revisión es el del tenant (`SIMREV-ORG-S*`).

## 2. Almacenamiento

| Permitido en F35-SBX-A | Condición |
|---|---|
| JSON versionado en `evidencia-sbx/contrato/` y `evidencia-sbx/fixtures/` | Texto UTF-8 con LF, sin NUL ni BOM, con SHA-256 y tamaño en el manifest |
| Markdown en `evidencia-sbx/` | Los diez documentos de la fase |
| Python en `tools/f35sbx/` | Solo biblioteca estándar autorizada |

| Prohibido en F35-SBX-A | Motivo |
|---|---|
| SQLite, en memoria o en archivo | DH-07: corresponde a F35-SBX-B |
| Almacenamiento temporal o archivos fuera de las dos carpetas | DH-07 |
| Base de datos del proyecto, `audit_logs`, `storage/` o tablas productivas | SBX-15 y SBX-16 |
| Imágenes, PDF, audio, vídeo, binarios o bases de datos dentro de `evidencia-sbx/` | Solo texto |

## 3. Retención y purga

F35-SBX-A no crea almacenamiento temporal, así que no hay nada que purgar. Los fixtures versionados no se purgan: su historia vive en Git. La purga verificada del almacenamiento temporal, con su evento `purgado`, se diseña aquí y se implementa en F35-SBX-B.

## 4. Alcance Git

`validate_f35sbx.py`, `validate_f34b.py` y `validate_f34e.py` comprueban por separado que, desde la base fija, solo cambian `evidencia-sbx/**` (Markdown o JSON), `tools/f35sbx/**` (Python), las dos adaptaciones de DH-02, el gobierno (`CLAUDE.md`, `docs/PROGRESS.md`) y tres validadores históricos como rutas exactas: `tools/f30/validate_f30.py`, `tools/f33/validate_f33.py` y `tools/f34/validate_f34.py`. Los errores de Git, las eliminaciones y los resultados desconocidos fallan cerrado.

[`f35sbx_scope.py`](../tools/f35sbx/f35sbx_scope.py) concentra las dos excepciones de esta fase. Solo valen en la rama F35-SBX y mientras la base `b67f644` sea ancestro de HEAD, así que siguen vigentes tras los commits técnicos y hasta que el commit de gobierno lo registre. Todo se compara con la base, nunca con HEAD:

| Archivo | Contenido admitido |
|---|---|
| `CLAUDE.md`, `docs/PROGRESS.md` | Exactamente la base con el registro de apertura de F35-SBX-A, sin otro cambio y con los 13 estados de gobierno intactos |
| `validate_f30.py`, `validate_f33.py`, `validate_f34.py` | Exactamente la base con la adaptación aprobada: carga de `f35sbx_scope`, uso de `governance_ok()`, sus regresiones y el ajuste mínimo de su comprobación Git |

Una rama distinta, una base que no es ancestro, un error de Git, una base ilegible o cualquier diferencia de contenido dejan la excepción sin efecto: el validador correspondiente falla.
