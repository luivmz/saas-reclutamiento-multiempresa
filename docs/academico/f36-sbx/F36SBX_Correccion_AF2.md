# F36-SBX — Corrección AF2 (segunda auditoría independiente)

> Fase F36-SBX, corrección focal del 26/10/2026, en la rama `feature/f36-sbx-authorization-design`, sobre el candidato auditado `2a4e68c913cf378fe5f5543f9dc537fd45760c63`. Candidata a una **tercera auditoría independiente**. Los MEDIUM quedan **corregidos por implementación, pendientes de tercera auditoría independiente**: este documento no los declara cerrados.

## 1. Veredicto recibido

La segunda auditoría independiente (AF2) del candidato `2a4e68c` concluyó **no aprobado para integración**, con 0 BLOCKER, 0 HIGH, 3 MEDIUM y 1 LOW. Este registro transcribe lo comunicado; el informe de la auditoría no forma parte del repositorio.

| ID | Severidad | Hallazgo |
|---|---|---|
| AF2-M01 | MEDIUM | El registro FG-02 o FG-12 podía contradecir el informe de auditoría o el ADR que cita: bastaba con que el informe nombrara el commit, y se aceptaban auditores como «...» o invisibles |
| AF2-M02 | MEDIUM | El sello de test solo cubría `[id, content_hash]`: trasplantar postulación, vacante, organización, escenario, familia, generador, semilla o provenance de un artefacto de test no se detectaba |
| AF2-M03 | MEDIUM | Faltaba aislamiento entre tenants: un autor de otra organización o una referencia upstream adicional de otro tenant pasaban |
| AF2-L01 | LOW | `example_id` admitía cualquier valor, incluso un objeto con `candidate_score`, y un ejemplo vacío pasaba |

## 2. Reproducción sobre `2a4e68c`

Antes de cambiar nada se reprodujeron en memoria, contra el validador de `2a4e68c`, doce mutaciones derivadas de los hallazgos. Las doce fueron falsos PASS: el validador terminaba con 0 fallas.

| # | Mutación | Hallazgo | En `2a4e68c` | En este candidato |
|---|---|---|---|---|
| 1 | FG-02 aprobado con un informe que declara no aprobado y HIGH = 2 | M01 | Falso PASS | Falla (AF2-01, AF2-02, D17, D18) |
| 2 | Informe que solo contiene el SHA del candidato | M01 | Falso PASS | Falla (AF2-03) |
| 3 | Auditor «...» | M01 | Falso PASS | Falla (AF2-04) |
| 4 | Auditor formado solo por U+200B | M01 | Falso PASS | Falla (AF2-05, D21) |
| 5 | FG-12 aprobado con un ADR que declara PROPUESTO | M01 | Falso PASS | Falla (AF2-09, D28, D29) |
| 6 | Trasplante coherente de APP-00013 a APP-00015 en test, sin resellar | M02 | Falso PASS | Falla (AF2-13) |
| 7 | Semilla de un artefacto de test cambiada sin resellar | M02 | Falso PASS | Falla (AF2-19) |
| 8 | `generator_version` de un artefacto de test cambiada sin resellar | M02 | Falso PASS | Falla (AF2-18) |
| 9 | Autor EV-S2-01 en una observación de ORG-S1 | M03 | Falso PASS | Falla (AF2-25) |
| 10 | Referencia upstream adicional a APP-00003 (ORG-S2) | M03 | Falso PASS | Falla (AF2-26) |
| 11 | `example_id` como objeto con `candidate_score` | L01 | Falso PASS | Falla (AF2-31, AF2-32) |
| 12 | Ejemplo vacío | L01 | Falso PASS | Falla (AF2-33) |

## 3. Corrección de AF2-M01: una sola fuente estructurada

- **Bloque canónico.** El informe de FG-02 y el ADR de FG-12 contienen exactamente un bloque de código cercado con la etiqueta `f36sbx-audit-metadata` o `f36sbx-adr-metadata`, cuyo JSON (sin claves duplicadas) tiene campos cerrados. El documento entero queda fijado por el SHA-256 que declara el registro.
- **Coherencia exacta.** El registro y el bloque deben coincidir, comparando JSON canónico, en commit candidato, veredicto, recuentos BLOCKER, HIGH, MEDIUM y LOW, y auditor (informe); y en id, estado, relación con ADR-005, alcance, `covered_ei` y decisión sobre EI-09 (ADR). Un registro APROBADO con un ADR PROPUESTO falla.
- **Contexto.** El bloque del informe nombra el gate, su versión, el criterio y el commit candidato, y su fecha queda entre la del candidato y la del registro. El ADR forma parte del commit candidato y no cambia después; por eso su bloque no puede citar ese commit, que lo contiene (sería autorreferente): fija el gate, su versión y la base, y su `decided_on` no es posterior al candidato.
- **Sin segunda fuente.** Fuera del bloque no pueden aparecer los tokens canónicos ni aserciones `clave = valor` o `clave: valor` de veredicto, recuentos o estado, tampoco dentro de un JSON señuelo. El documento debe tener título, las secciones exigidas y al menos 200 letras de contenido humano, en NFC y sin caracteres invisibles. El validador no interpreta prosa libre (sin NLP): la prosa no es normativa y su lectura sigue siendo revisión humana.
- **Identidad visible.** El auditor debe ser texto NFC sin espacios exteriores, sin caracteres de control, formato (U+200B, U+202E…), uso privado ni no asignados, con al menos tres letras, como máximo 120 caracteres y distinto de un marcador de posición. **Una identidad declarada estructuralmente válida no es una identidad externa autenticada**: esa verificación sigue siendo humana.

## 4. Corrección de AF2-M02: cadena de hashes y sello v2

Cada hash usa `sha256(etiqueta + salto de línea + JSON canónico)`, con una etiqueta por nivel, y su preimagen es el registro completo sin su propio campo de hash, sin circularidad:

| Nivel | Qué fija |
|---|---|
| `content_hash` | El contenido del artefacto |
| `record_hash` | El artefacto completo: contexto, tipo, familia, marcadores, contenido, `content_hash` y provenance (generador, versión, plantilla, semilla y referencias upstream) |
| `fragment_hash` | Identidad, `artifact_record_hash` vigente, contexto, `text_path`, offsets y `text_hash` |
| `input_manifest_hash` | Los pares `[fragment_id, fragment_hash]` de la postulación y partición del output |
| `output_hash` | Identidad, EI, método, versión y `method_config` cerrada, contexto, consulta, `fragment_refs`, `fragment_ref_hashes`, abstención y manifiesto de entrada |
| Sello de test v2 | `record_hash` de los artefactos de test, `fragment_hash` de sus fragmentos, `output_hash` de sus outputs y de los outputs de ajuste, el oro de dev, los umbrales y `test_used_for_tuning` |

Cualquier cambio de postulación, vacante, organización, escenario, familia, generador, versión, semilla, provenance, contexto de un fragmento o de un output, contenido u oro rompe un eslabón: si no se recalcula, falla su hash; si se recalcula sin resellar, falla el sello. Las pruebas AF2-13..AF2-20 y AF2-24 muestran que, con los registros recalculados, el sello es lo único que lo detecta, y los controles P-01..P-04 que el mismo cambio, resellado, es conforme. Límite documentado: los artefactos de dev que no usa el ajuste no se sellan (P-11).

## 5. Corrección de AF2-M03: aislamiento entre tenants

- `author_token` y `annotator_token` llevan su tenant (`EV-S1-01`, `ANT36-S1-02`) y deben ser de la organización del artefacto.
- Cada referencia upstream se resuelve en su tabla F34 tipada y se compara con la organización, el escenario, la vacante y la postulación del artefacto. La vacante y la postulación propias se citan exactamente una vez; los criterios, solo de la misma vacante.
- No se admite ninguna fuente global (`global_upstream_sources = []`). El único identificador global del contenido es `question_id`, tipado, no personal y documentado; cada identificador con patrón tiene una sola clase: tenant, upstream, interno o global.

## 6. Tratamiento de AF2-L01

`example_id` debe ser exactamente `f36sbx-contract-example`. El ejemplo exige cobertura mínima: los ocho tipos, fragmentos, outputs con fragmentos y con abstención, test con artefactos, oro y outputs, ajuste en dev y dos escenarios. El nuevo ejemplo tiene nueve artefactos, cuatro fragmentos y tres outputs en SC36-01 y SC36-02.

## 7. Pruebas y metapruebas

- [`test_f36sbx.py`](../tools/f36sbx/test_f36sbx.py) incluye AF2-01..AF2-33 y los grupos H, X, D, L y P. Las pruebas de evidencia AF2 se comprueban en memoria y registradas en la fotografía del repositorio, donde el validador completo falla.
- [`meta_f36sbx.py`](../tools/f36sbx/meta_f36sbx.py) anula cada comprobación AF2 en el árbol sintáctico del validador y exige que la batería lo detecte. Además muta una a una cada hoja del ejemplo y de la evidencia: sin recalcular, todo falla; resellado, solo pasan los cambios legítimos de su lista cerrada.

## 8. Lo que no cambia

- F36-SBX = EN DISEÑO; F36-SBX-GATE = NO SUPERADO; FG-02, FG-03, FG-10 y FG-12 siguen pendientes, sin evidencia registrada; F37-SBX = BLOQUEADA.
- G0 real = NO APROBADA; G0-SBX = APROBADA CON RESTRICCIONES; ADR-005 = PROPUESTA; Alcance C = BLOQUEADO; Datos reales = PROHIBIDOS.
- EI-09 sigue CONDITIONAL (F36-M02) y el ADR sucesor sigue siendo una propuesta (F36-M03); F36-M01 sigue pendiente de FG-03.
- RF-23 sigue siendo la decisión final humana y RF-29 sigue experimental. Sin ML, NLP, embeddings, OCR, parsing, LLM, endpoints, migraciones, UI ni dependencias nuevas; F35-SBX, el runtime y los datasets no cambian.
