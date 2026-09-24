# PowerDesigner — modelos de la v1.1 (Fase 23)

Formalización en **SAP PowerDesigner 16.6.1.5066** de la especificación UML AS-IS de la Fase 22 ([`../uml/`](../uml/)) y del esquema físico real. Documento de la fase: [`../phase-23-powerdesigner.md`](../phase-23-powerdesigner.md).

Los diagramas describen **lo implementado** en `develop` (`2621bee`). RF-23 es una decisión humana; RF-28 es un candidato no implementado; RF-29 es experimental y no participa en selección, ranking ni decisión.

## Contenido

| Carpeta | Qué hay |
|---|---|
| `models/saas-recruitment-v1.1-oom.oom` | Modelo orientado a objetos (UML): 20 diagramas. CL-01 y CL-01b, UC-01, PK-01, CO-01, DE-01, SEQ-01 a SEQ-08, AC-01 y AC-02, ST-01 a ST-04 |
| `models/saas-recruitment-v1.1-pdm.pdm` | Modelo físico (DBMS *PostgreSQL 9.x*): PDM-01 esquema completo y PDM-02 tablas de dominio |
| `models/source/schema-postgresql.sql` | Esquema real (`pg_dump --schema-only`, sin datos ni credenciales) del que sale el PDM por ingeniería inversa |
| `exports/` | Cada diagrama en PNG y SVG. Las carpetas `*_svg_Files/` son imágenes que el SVG enlaza |
| `scripts/` | Scripts que construyen los modelos por la interfaz COM de PowerDesigner |
| [`inventory.md`](inventory.md) | Inventario: ID, tipo, modelo, archivo nativo, exportación, RF y validación |
| [`f22-checklist.md`](f22-checklist.md) | Correspondencia F22 ↔ PowerDesigner, con las diferencias justificadas |

## Cómo abrir

Abrir el `.oom` o el `.pdm` con PowerDesigner 16.6 (*File > Open*). En el Explorador de objetos, los diagramas de CL-01 están en el paquete `App\Models`, CL-01b en `App\Enums`, PK-01 en `Módulos del monolito` y cada diagrama de estados en su paquete `ST-01` a `ST-04`. Los demás están en la raíz del modelo.

## Cómo se construyeron

Los modelos no se escribieron a mano: los crea PowerDesigner a partir de scripts de PowerShell que usan su interfaz COM (`PowerDesigner.Application`), en modo *batch* (`InteractiveMode = 0`) para que ningún diálogo bloquee la sesión.

| Script | Hace | Reejecutar |
|---|---|---|
| `pdm/clean_schema.py`, `pdm/reverse_pdm.ps1`, `pdm/extract_checks.py`, `pdm/finish_pdm.ps1` | Limpieza del volcado, ingeniería inversa, CHECK e índice parcial, PDM-01/02 | Solo para regenerar el PDM desde un volcado nuevo |
| `01-class-model.ps1` | **Crea el OOM desde cero** con CL-01 y CL-01b | **No**: reemplaza el modelo entero |
| `02-use-cases.ps1`, `03-architecture.ps1` | Añaden UC-01 y PK-01/CO-01/DE-01 | **No**: duplicarían objetos |
| `05-structural-fixes.ps1` | Ajustes en sitio de UC-01, PK-01, CO-01 y DE-01 | Idempotente |
| `04-sequences.ps1` (+ `seqlib.ps1`) | SEQ-01 a SEQ-08 | Sí: cada diagrama se reemplaza, sin copias |
| `06-activities.ps1` (+ `flowlib.ps1`) | AC-01 y AC-02 | Sí: se reemplaza |
| `07-states.ps1` (+ `flowlib.ps1`) | ST-01 a ST-04 | Sí: se reemplaza |
| `08-export-pdm.ps1` | Exporta PDM-01/02 sin modificar el PDM | Sí |
| `09-remove-empty-diagrams.ps1` | Quita los diagramas vacíos que PowerDesigner crea por defecto en cada paquete | Sí |
| `tools/run-pd.ps1`, `tools/pd-status.ps1` | Ejecución con límite de tiempo; modelos abiertos | — |

Ejecución: `scripts\tools\pd-status.ps1` (debe decir `modelos abiertos: 0`) y luego `scripts\tools\run-pd.ps1 -Script 04-sequences.ps1`. `$env:PD_ONLY = 'SEQ-03,SEQ-05'` limita qué diagramas se regeneran. Los scripts guardan con BOM UTF-8, porque PowerShell 5.1 lee como ANSI los `.ps1` sin BOM.

## Reglas

- Solo datos ficticios; el esquema no contiene datos ni credenciales.
- No se versionan modelos de prueba (`zz_*`) ni copias de respaldo (`.oob`, `.pdb`, `.obb`, `.bak`); `Save-Model` las borra.
- Cambiar un diagrama es cambiar su script y regenerarlo, no editarlo a mano, para que el modelo y el script no diverjan. Si se edita a mano, hay que anotarlo en el inventario.
