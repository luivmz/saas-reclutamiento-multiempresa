# F36-SBX — Contrato de datos y de evidencia sintética

> Fase F36-SBX, versión 1 (26/10/2026). Candidata a auditoría independiente. **Es un contrato de diseño: F36-SBX no genera ningún corpus.** La versión legible por máquina es [`f36sbx_evidence_contract.json`](contrato/f36sbx_evidence_contract.json), y la verifica [`validate_f36sbx.py`](../tools/f36sbx/validate_f36sbx.py) (regla CTR).

## 1. Principios

1. **Solo sintético.** `source_type = synthetic` y `environment = sandbox` en todo registro. No existe un valor que admita una fuente real.
2. **Fuentes cerradas.** Solo pueden alimentar F37-SBX el dataset de F34 ([`datos-sinteticos/dataset`](../datos-sinteticos/README.md)), los fixtures de F35-SBX ([`evidencia-sbx/fixtures`](../evidencia-sbx/README.md)) y un generador nuevo con plantillas y semilla. Los adjuntos de gobierno (`g0-evidence/adjuntos/`), `storage/` y cualquier base de datos están excluidos.
3. **Procedencia obligatoria** en cada artefacto, en cada fragmento y en cada salida.
4. **Sin campos de persona ni de juicio.** La lista de campos prohibidos está en el JSON; un campo nuevo que no esté declarado en el contrato invalida el artefacto.
5. **Generador sin LLM** (EI-17 BLOCKED): plantillas versionadas, semilla declarada y salida reproducible byte a byte.

## 2. Qué se reutiliza

| Fuente | Qué aporta | Uso en F37-SBX | Límite |
|---|---|---|---|
| F34 `vacancies`, `criteria`, `rubric_levels` y `requirements` | Criterios explícitos y versionados | EI-01 a EI-04 y el texto de consulta de EI-07, EI-09 y EI-10 | Sin cambios: se leen, no se reescriben |
| F34 `evidence` y `annotations` | Evidencia registrada por personas sintéticas, con procedencia | EI-01, EI-03 y EI-04 | **No sirve para evaluar la recuperación.** Su texto plantilla cita literalmente el nombre del criterio (por ejemplo, «… vinculada a «Planificación de la enseñanza»»), así que cualquier búsqueda léxica acierta por construcción |
| F34 `requirement_checks` y `expected_alerts` | Oráculo de alertas deterministas | EI-02 | El oráculo no sustituye a la regla |
| F34 `fairness_sintetico` | Atributos de grupo sintéticos | Solo EI-24, para construir pares contrafactuales | Nunca como feature ni dentro de un texto de evidencia |
| F35-SBX contrato y fixtures | Seis marcadores, hash canónico y cadena de provenance | Patrón de los marcadores y de la provenance | Están congelados: no se modifican. Se crea un espacio de nombres propio (`SBX36-`) |

## 3. Qué evidencia sintética nueva haría falta en F37-SBX

| Tipo | Representación | Campos clave | Etapa |
|---|---|---|---|
| `cv_document` | Texto plano UTF-8 estructurado por secciones, sin nombre, foto, edad, género, dirección ni contacto | `sections[]` con `section_kind` y `text_synthetic` | A |
| `certificate` | Texto plano corto | `issuer_synthetic` (institución ficticia) y `title_synthetic` | A |
| `interview_transcript` | Texto escrito como transcripción **ya revisada**; no proviene de audio (EI-21 BLOCKED) | `question_id`, `turns[]` y `review_status = revisada_sintetica` | A |
| `human_observation` | Nota de un evaluador sintético | `author_kind = human_synthetic`, `author_token` y `observation_kind` (conducta observada o aclaración) | A |
| `relevance_annotation` | Enlace de oro fragmento → criterio, hecho por dos anotadores | `fragment_id`, `criterion_id`, `relevance` (relevante o no relevante) y `annotator_token` | A |
| `adversarial_case` | Texto con instrucciones incrustadas, caracteres de control, PII ficticia evidente, tamaños extremos o Unicode engañoso | `attack_kind` y `expected_outcome` (rechazo o abstención) | A |
| `counterfactual_pair` | Dos variantes de un documento que solo difieren en un marcador de grupo sintético | `variant_of`, `perturbation` y `grupo_sintetico` | B (EI-24) |
| `rendered_document` | PDF o DOCX nacido digital a partir de un `cv_document`, con el hash del origen | `rendered_from` y `format` | B (EI-11) |

**Estratos de solapamiento léxico.** Para que la evaluación de la recuperación no sea trivial, cada par fragmento-criterio relevante se genera en tres estratos declarados: `alto` (comparte términos con el criterio), `medio` (paráfrasis parcial) y `nulo` (paráfrasis sin términos comunes). Las métricas se informan por estrato ([plan de evaluación](F36SBX_Plan_Evaluacion.md)).

**Tamaño.** No se genera nada en F36-SBX. Como referencia de diseño, estimar una exhaustividad cercana a 0,5 con una semiamplitud de 0,05 al 95 % exige unos 385 pares relevantes por estrato (n = 1,96² · 0,25 / 0,05²). F37-SBX debe justificar el tamaño final antes de generar.

## 4. Marcadores synthetic-only

Mismo patrón que F35-SBX, con su propio espacio de nombres. Se exigen los seis a la vez; si falta uno, el artefacto se rechaza:

| # | Marcador |
|---|---|
| 1 | `synthetic_id` con prefijo `SBX36-` y el tenant |
| 2 | Todo campo de texto empieza por `[SINTÉTICO]` |
| 3 | `source_type = synthetic` |
| 4 | `environment = sandbox` |
| 5 | `hash_algorithm = f36sbx-content-sha256-v1` |
| 6 | `synthetic_organization_id` en `ORG-S1..S3` |

## 5. Provenance

Cada artefacto lleva `generator_id`, `generator_version`, `template_id`, `seed`, `upstream_refs` (fuentes F34 o F35 con su hash) y `content_hash`. Cada fragmento lleva `fragment_id`, `artifact_id`, `char_start` y `char_end` (offsets sobre el texto canónico NFC) y `fragment_hash`. Cada salida de un método lleva `method_id`, `method_version`, `input_manifest_hash` y `output_hash`. Una salida sin provenance completa se descarta (TEI-12).

## 6. Particiones y fuga

| Regla | Contenido |
|---|---|
| Sin conjunto de entrenamiento | El ajuste fino está BLOCKED (EI-22). Solo hay `dev`, para fijar umbrales, y `test`, sellado |
| Unidad de partición | `template_family` + `vacancy_token`. Ninguna familia de plantillas ni vacante aparece en más de una partición |
| Sellado | El manifiesto de `test` (hash de cada artefacto y de cada anotación) se registra **antes** de ejecutar cualquier método. Cambiarlo después invalida la evaluación |
| Embargo temporal | Si se usan instantes del proceso, las vacantes de `test` cierran después de las de `dev`, con una purga igual a la de `process_splits` de F34 |
| Umbrales | Se fijan solo en `dev`. Nunca se ajusta nada mirando `test` |
| Criterio y evidencia | El texto del criterio no puede copiarse en la evidencia fuera del estrato `alto` |
| Contrafactuales | Las dos variantes de un `counterfactual_pair` van siempre en la misma partición |
| Anotación | Dos anotadores independientes; el acuerdo se mide antes de usar el oro |

## 7. Garantía de que ninguna fuente real entra

1. Las fuentes cerradas de la sección 1 son la única entrada admitida, comprobada por ruta y por hash del manifiesto.
2. La guardia EI-05 rechaza cualquier coincidencia de PII.
3. Un archivo sin los seis marcadores no entra.
4. No se admiten rutas fuera del repositorio, URL ni descargas.
5. Nombres de persona: los documentos no tienen campo de nombre. Los `counterfactual_pair` usan marcadores de grupo sintéticos (`grupo_sintetico`) y no nombres propios.
