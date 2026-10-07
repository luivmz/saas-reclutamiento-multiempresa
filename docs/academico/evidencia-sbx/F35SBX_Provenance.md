# F35-SBX-A — Modelo de provenance

> Fase F35-SBX-A, versión 1 (07/10/2026). Cada evidencia sintética tiene exactamente una provenance, verificable sin confiar en lo que el fixture declara: el validador la recalcula desde el dataset F34.

## 1. Preguntas que responde

| Pregunta | Respuesta en los artefactos | Comprobación |
|---|---|---|
| ¿De qué fixture sintético vino cada evidencia? | Archivo `fixtures/ORG-S*_evidencias.json`, con su SHA-256 en el manifest | MAN |
| ¿De qué fila F34 procede? | `sources[].origin_record_id` (`SYN-NNNNNN`) en `evidence.csv`, con el SHA-256 del archivo | ORI, HSH |
| ¿Qué transformación determinista recibió? | `transformation_id = T1-normalizacion-nfc-espacios`, versión `1` | PRV |
| ¿Qué hash tenía antes? | `hash_before`, calculado sobre el texto F34 original | HSH |
| ¿Qué hash tiene después? | `hash_after`, igual al `content_hash` del registro | HSH |
| ¿Qué run produjo el resultado? | `pipeline_run_id` (`SBXR-…`), con `run_kind = oraculo_sbx_a` | RUN |
| ¿Qué revisión humana simulada ocurrió? | `review_id` (`SBXH-…`), enlazada al mismo registro | PRV, REV |
| ¿Cuándo? | `recorded_at`, según el reloj lógico del run | RUN |
| ¿Para qué tenant sintético? | `synthetic_organization_id`, igual en todas las piezas | ISO |

## 2. Reglas

- Una provenance por evidencia; una provenance sin evidencia, o una fuente sin evidencia, falla.
- `source_id` de la provenance coincide con el de la evidencia y existe en `sources`.
- El texto de la evidencia es exactamente `T1(texto F34)`; T1 es pura, determinista e idempotente. Con los textos actuales T1 no cambia nada, por eso `hash_before` y `hash_after` coinciden: el validador lo comprueba recalculando ambos, no lo supone.
- Las provenance de un run forman una cadena: `prev_provenance_hash` del primer elemento es `000…0` (64 ceros) y cada `provenance_hash` se calcula sin su propio campo.
- Los instantes salen del reloj lógico del run (`clock_start`), nunca del reloj del sistema, para que los hashes sean reproducibles.

## 3. Regla de selección determinista

Por cada organización sintética, las dos primeras filas de `evidence.csv` con `state = vinculada`, `source_type = synthetic` y `source_type_ev` en `formulario`, `nota_entrevista` o `prueba`, ordenadas por `evidence_id`. Elegir otra fila, aunque sea sintética y de la misma organización, falla (caso NS-30).

## 4. Por qué no se confunde con evidencia real

- Seis marcadores synthetic-only en cada evidencia ([contratos](F35SBX_Contratos_Datos.md#4-marcadores-synthetic-only)).
- Origen fijo: el `evidence.csv` sintético de F34, cuyo manifiesto declara `source = synthetic`; cualquier otra ruta falla, incluida `g0-evidence/adjuntos/`.
- El manifest de F35-SBX-A advierte que los fixtures no representan datos reales del Colegio Andino.
