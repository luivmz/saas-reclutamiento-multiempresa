# F34E — Matriz de criterios G0-SBX

> Fase F34E, versión 1 (04/10/2026). Los 18 criterios de [G0-SBX](F34E_Definicion_G0_SBX.md). Cada uno se verifica **dentro del repositorio** con una comprobación automática de [`validate_f34e.py`](../tools/f34e/validate_f34e.py), que vuelve a calcular el estado en cada ejecución y falla si esta matriz dice otra cosa. Estados admitidos: **CUMPLE** o **NO CUMPLE**; no existen estados pendientes.

| ID | Criterio | Verificación automática | Fuente | Estado |
|---|---|---|---|---|
| SBX-01 | Dataset 100 % sintético y trazable | Reglas DQ-05 a DQ-07 de F34 sin violaciones y manifiesto con `source = synthetic` | [F34](../datos-sinteticos/README.md), `validate_f34.py` | CUMPLE |
| SBX-02 | 0 PII real | Reglas PII-01 a PII-03 de F34 sin violaciones | `validate_f34.py` | CUMPLE |
| SBX-03 | 0 CV o documentos reales | Ningún archivo distinto de CSV, JSON o Markdown en `datos-sinteticos/` ni en `g0-sandbox/`; textos libres marcados `[SINTÉTICO]` | Árbol de archivos; DQ-04 de F34 | CUMPLE |
| SBX-04 | 0 audio o vídeo real de candidatos | Ningún archivo de audio ni de vídeo en `datos-sinteticos/` ni en `g0-sandbox/` | Árbol de archivos | CUMPLE |
| SBX-05 | 0 scoring ML de personas | Ningún campo de score, ranking ni selección en `schema.json`; LK-01 y LK-08 de F34 sin violaciones | `schema.json`, `validate_f34.py` | CUMPLE |
| SBX-06 | 0 recomendación automática de candidatos | Ningún campo de recomendación en `schema.json` ni afirmación habilitante en G0-SBX | `schema.json`, este paquete | CUMPLE |
| SBX-07 | 0 selección automática | Ningún campo de selección o contratación en `schema.json`; RF-23 humana | `schema.json`, matriz de trazabilidad | CUMPLE |
| SBX-08 | RF-23 permanece humana | La fila RF-23 de la matriz de trazabilidad dice «humana» y el archivo no cambió | `docs/final-report/traceability-master.md` | CUMPLE |
| SBX-09 | RF-21 vigente no se reemplaza | La fila RF-21 sigue presente, el archivo no cambió y la regla RANK de F34A pasa | Matriz de trazabilidad, `validate_f34a.py` | CUMPLE |
| SBX-10 | Aislamiento multiempresa en fixtures y schemas | Reglas CTX-01 a CTX-10 de F34 sin violaciones; `organization_token` en las tablas de contexto | `validate_f34.py`, `schema.json` | CUMPLE |
| SBX-11 | Provenance obligatorio | Campo `provenance` en `evidence` y `source_type`/`synthetic_record_id` en todas las tablas (DQ-07) | `schema.json`, `validate_f34.py` | CUMPLE |
| SBX-12 | Threat model aceptado por el equipo | G0-09 derivado como CUMPLIDO de los registros reales de F34C | `validate_f34b.py` | CUMPLE |
| SBX-13 | ADR-005 con aprobación interna registrada | G0-14 derivado como CUMPLIDO; ADR-005 canónico sigue PROPUESTA | `validate_f34b.py`, ADR-005 | CUMPLE |
| SBX-14 | Datos y fixtures sintéticos claramente marcados | `source_type = synthetic` en todas las filas, prefijo `[SINTÉTICO]` y advertencia del manifiesto | `validate_f34.py`, `manifest.json` | CUMPLE |
| SBX-15 | Resultados experimentales no alimentan producción | Ningún archivo de `app/`, `routes/`, `config/`, `database/`, `resources/`, `tests/`, `cypress/` ni `ml-service/src` referencia los datos sintéticos ni G0-SBX | Búsqueda en el árbol | CUMPLE |
| SBX-16 | Ningún endpoint, migración ni runtime productivo se activa | Sin cambios frente a la base fija `9e0fc92adbe563e99a7cb16fdb07aa26f8876d68` (main con F34D cerrada) en runtime, dependencias, migraciones ni baseline | Git | CUMPLE |
| SBX-17 | Alcance C sigue BLOQUEADO | La decisión G0 vigente declara el alcance C como no habilitado y nada en G0-SBX lo habilita | `F34B_Decision_G0.md`, este paquete | CUMPLE |
| SBX-18 | G0 real continúa NO APROBADA | La decisión G0 vigente declara «G0 = NO APROBADA» y G0-02, G0-03 y G0-12 siguen sin cerrar | `F34B_Decision_G0.md`, `validate_f34b.py` | CUMPLE |

## Resumen

| Estado | Criterios | Total |
|---|---|---|
| CUMPLE | SBX-01 a SBX-18 | 18 |
| NO CUMPLE | — | 0 |
