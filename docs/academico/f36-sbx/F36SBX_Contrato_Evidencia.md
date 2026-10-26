# F36-SBX — Contrato de datos y de evidencia sintética

> Fase F36-SBX, versión 2 (26/10/2026). Corrige AF1-M02 de la primera auditoría ([corrección AF1](F36SBX_Correccion_AF1.md)). Candidata a una segunda auditoría independiente. **Es un contrato de diseño: F36-SBX no genera ningún corpus.** La versión legible por máquina es [`f36sbx_evidence_contract.json`](contrato/f36sbx_evidence_contract.json). Su [ejemplo de conformidad](contrato/f36sbx_contract_example.json) demuestra que el contrato se puede cumplir. Ambos los verifica [`validate_f36sbx.py`](../tools/f36sbx/validate_f36sbx.py) con la regla CTR.

## 1. Principios

1. **Solo sintético.** `source_type = synthetic` y `environment = sandbox` en todo registro. No existe un valor que admita una fuente real.
2. **Contrato cerrado.** Cada estructura (sobre del artefacto, contenido por tipo, elementos de lista, fragmento, output, provenance, referencia upstream y manifiesto de particiones) tiene una lista exacta de campos. Un campo ausente o adicional, un tipo desconocido, un valor fuera de su enumerado o un identificador fuera de patrón invalidan el registro.
3. **Fuentes cerradas.** Una referencia upstream solo puede citar las tres tablas F34 de `upstream_files` (`applications.csv`, `criteria.csv` y `vacancies.csv`), con el SHA-256 que declara el [manifiesto F34](../datos-sinteticos/README.md). Los fixtures de F35-SBX son un patrón de marcadores y de provenance, no una fuente de registros. Los adjuntos de gobierno (`g0-evidence/adjuntos/`), `storage/`, cualquier base de datos y cualquier URL están excluidos.
4. **Procedencia verificable** en cada artefacto, en cada fragmento y en cada output: no basta con que el campo exista, la cadena tiene que poder recalcularse (sección 5).
5. **Sin campos de persona ni de juicio.** Hay 44 nombres de campo prohibidos y una lista de tokens prohibidos (`score`, `rank`, `fit`, `name`, `email`, `emotion`, `level`, `select`…). Ningún campo de registro puede contener uno de esos tokens, así que un sinónimo como `candidate_score` tampoco pasa.
6. **Generador sin LLM** (EI-17 BLOCKED): plantillas versionadas, semilla declarada y salida reproducible byte a byte.
7. **Integridad.** El validador fija el SHA-256 del JSON canónico del contrato. Cambiarlo exige un incremento auditado que actualice también el validador.

## 2. Qué se reutiliza

| Fuente | Qué aporta | Uso en F37-SBX | Límite |
|---|---|---|---|
| F34 `vacancies`, `criteria`, `rubric_levels` y `requirements` | Criterios explícitos y versionados | EI-01 a EI-04 y el texto de consulta de EI-07, EI-09 y EI-10 | Sin cambios: se leen, no se reescriben |
| F34 `applications` y `vacancies` | Identidad sintética de la postulación y de la vacante | Referencias upstream obligatorias de cada artefacto (REL-02) y comprobación de organización y vacante (REL-04) | Solo los tokens sintéticos; nunca `person_token` ni datos de persona |
| F34 `evidence` y `annotations` | Evidencia registrada por personas sintéticas, con procedencia | EI-01, EI-03 y EI-04 | **No sirve para evaluar la recuperación.** Su texto plantilla cita literalmente el nombre del criterio (por ejemplo, «… vinculada a «Planificación de la enseñanza»»), así que cualquier búsqueda léxica acierta por construcción |
| F34 `requirement_checks` y `expected_alerts` | Oráculo de alertas deterministas | EI-02 | El oráculo no sustituye a la regla |
| F34 `fairness_sintetico` | Atributos de grupo sintéticos | Solo EI-24, para construir pares contrafactuales | Nunca como feature ni dentro de un texto de evidencia |
| F35-SBX contrato y fixtures | Seis marcadores, hash canónico y cadena de provenance | Patrón de los marcadores y de la provenance | Están congelados: no se modifican. Se crea un espacio de nombres propio (`SBX36-`) |

## 3. Registros

### 3.1 Sobre del artefacto

Todo artefacto tiene exactamente estos campos: `synthetic_id`, `artifact_type`, `stage`, `synthetic_organization_id`, `scenario_id`, `vacancy_token`, `application_token`, `partition`, `template_family`, `source_type`, `environment`, `hash_algorithm`, `content`, `content_hash` y `provenance`.

### 3.2 Tipos y contenido

| Tipo | Etapa | Contenido cerrado | Fragmentable |
|---|---|---|---|
| `cv_document` | A | `sections[]`, con `section_kind` (`formacion`, `experiencia` o `capacitacion`) y `text_synthetic` | Sí |
| `certificate` | A | `issuer_synthetic` (institución ficticia) y `title_synthetic` | Sí |
| `interview_transcript` | A | `question_id`, `transcript_kind = texto_sintetico_revisado`, `review_status = revisada_sintetica` y `turns[]`, con `speaker_role` y `text_synthetic`. No proviene de audio (EI-21 BLOCKED) | Sí |
| `human_observation` | A | `author_kind = human_synthetic`, `author_token`, `observation_kind` (`conducta_observada` o `aclaracion`, nunca una inferencia) y `text_synthetic` | Sí |
| `relevance_annotation` | A | `fragment_id`, `criterion_id`, `relevance`, `annotator_token` y `overlap_stratum` | No |
| `adversarial_case` | A | `attack_kind` (cinco valores cerrados), `text_synthetic` y `expected_outcome` (`rechazo` o `abstencion`) | Sí |
| `counterfactual_pair` | B (EI-24) | `variant_of`, `perturbation = marcador_de_grupo` y `grupo_sintetico`, el único lugar donde puede aparecer | No |
| `rendered_document` | B (EI-11) | `rendered_from` (un `cv_document`) y `format` (`pdf` o `docx`) | No |

Los textos son NFC, empiezan por `[SINTÉTICO]`, no superan 4000 caracteres y no contienen correo, teléfono ni DNI (guardia EI-05).

### 3.3 Fragmento

`fragment_id`, `artifact_id`, los cinco campos de contexto (organización, escenario, vacante, postulación y partición), `text_path` (por ejemplo, `sections/1/text_synthetic`), `char_start`, `char_end` y `fragment_hash`.

### 3.4 Output de localización

`output_id`, `ei` (solo EI-07, EI-09 o EI-10), `method_id`, `method_version`, los cinco campos de contexto, `query_criterion_id`, `fragment_refs`, `abstained`, `input_manifest_hash` y `output_hash`. **No tiene ningún campo de texto ni de puntaje**: un output solo cita fragmentos (TEI-09 y TEI-14).

### 3.5 Estratos y tamaño

**Estratos de solapamiento léxico.** Para que la evaluación de la recuperación no sea trivial, cada par fragmento-criterio relevante se genera en tres estratos declarados: `alto` (comparte términos con el criterio), `medio` (paráfrasis parcial) y `nulo` (paráfrasis sin términos comunes). Las métricas se informan por estrato ([plan de evaluación](F36SBX_Plan_Evaluacion.md)).

**Tamaño.** No se genera nada en F36-SBX. Como referencia de diseño, estimar una exhaustividad cercana a 0,5 con una semiamplitud de 0,05 al 95 % exige unos 385 pares relevantes por estrato (n = 1,96² · 0,25 / 0,05²). F37-SBX debe justificar el tamaño final antes de generar.

## 4. Marcadores synthetic-only

Mismo patrón que F35-SBX, con su propio espacio de nombres. Se exigen los seis a la vez; si falta uno, el artefacto se rechaza:

| # | Marcador |
|---|---|
| 1 | `synthetic_id` con prefijo `SBX36-` y el tenant, que debe coincidir con `synthetic_organization_id` |
| 2 | Todo campo de texto empieza por `[SINTÉTICO]` |
| 3 | `source_type = synthetic` |
| 4 | `environment = sandbox` |
| 5 | `hash_algorithm = f36sbx-content-sha256-v1` |
| 6 | `synthetic_organization_id` en `ORG-S1..S3` |

## 5. Provenance y hashes

| Eslabón | Qué se exige | Cómo se recalcula |
|---|---|---|
| Artefacto | `generator_id`, `generator_version`, `template_id` (de su misma familia), `template_family`, `seed` (entero ≥ 0), `upstream_refs` y `content_hash` | `content_hash` = SHA-256 del JSON canónico de `content`, con las claves ordenadas, separadores `,` y `:` y UTF-8 sin escapes |
| Referencia upstream | `source`, `ref` y `sha256`. Es obligatoria una referencia a su postulación en `applications.csv` y otra a su vacante en `vacancies.csv`; una anotación también cita su criterio en `criteria.csv` | `sha256` igual al del manifiesto F34 y al del archivo; `ref` existe en esa tabla |
| Fragmento | Un artefacto fragmentable existente, un `text_path` válido para su tipo y offsets dentro del texto | `fragment_hash` = SHA-256 del texto entre `char_start` y `char_end` |
| Output | Fragmentos existentes de su misma postulación y contexto | `input_manifest_hash` = SHA-256 del JSON canónico de la lista ordenada `[fragment_id, fragment_hash]` de la postulación y partición; `output_hash` = SHA-256 de `{abstained, ei, fragment_refs, method_id, method_version, output_id, query_criterion_id}` |

Un registro cuya cadena no se pueda recalcular se rechaza (TEI-12). Quitar la provenance, una referencia obligatoria o un campo de la cadena falla siempre.

## 6. Particiones y fuga

| Regla | Contenido | Cómo se verifica |
|---|---|---|
| Solo `dev` y `test` | `train` está prohibida y cualquier otro valor es desconocido | REL-11 en cada registro y en el manifiesto |
| Sin conjunto de entrenamiento | El ajuste fino está BLOCKED (EI-22) | `train_allowed = false` en el contrato |
| Unidad de partición | `template_family` + `vacancy_token`. Ninguna familia de plantillas ni vacante aparece en más de una partición | REL-05 |
| Sellado | El manifiesto de `test` lleva `sealed = true` y `seal_sha256`, el SHA-256 de la lista ordenada `[synthetic_id, content_hash]` de sus artefactos, registrado **antes** de ejecutar cualquier método | REL-11: cambiar un artefacto de `test` sin volver a sellar falla |
| Umbrales | Se ajustan solo con outputs de `dev` (`tuning_partition = dev`, `tuning_outputs`). `test_used_for_tuning = false` | REL-11: un output de `test` entre los de ajuste falla |
| Embargo temporal | Si se usan instantes del proceso, las vacantes de `test` cierran después de las de `dev`, con una purga igual a la de `process_splits` de F34 | `temporal_embargo = process_splits_f34` en el contrato |
| Contrafactuales | Las dos variantes van en la misma organización, escenario, vacante, partición y familia | REL-09 |
| Anotación | Dos anotadores independientes; el acuerdo se mide antes de usar el oro | Plan de evaluación, en F37-SBX |

## 7. Relaciones verificables

| ID | Relación |
|---|---|
| REL-01 | Sobre cerrado, tipo conocido con su etapa, seis marcadores y contenido cerrado con enumerados o patrones |
| REL-02 | Provenance cerrada y recalculable, con referencias upstream verificadas contra el manifiesto F34 |
| REL-03 | Identificadores únicos, con el segmento de organización igual a `synthetic_organization_id` |
| REL-04 | La vacante y la postulación existen en F34, con la misma organización y vacante |
| REL-05 | Aislamiento: vacante → una organización y un escenario; postulación → una vacante; familia y vacante → una partición |
| REL-06 | Cada fragmento apunta a un artefacto fragmentable existente, con el mismo contexto y su hash correcto |
| REL-07 | Cada output usa una EI de localización, cita fragmentos existentes de su propio contexto y trae sus hashes correctos |
| REL-08 | Cada anotación cita un fragmento existente de su contexto y un criterio F34 de su vacante |
| REL-09 | Cada par contrafactual cita una variante fragmentable de su misma organización, escenario, vacante, partición y familia |
| REL-10 | Cada documento renderizado cita un `cv_document` de su misma postulación, partición y familia |
| REL-11 | Manifiesto cerrado: solo `dev` y `test`, cada artefacto una vez y en su partición, `test` sellado y ajuste solo con `dev` |
| REL-12 | Textos NFC, con `[SINTÉTICO]` y sin patrones de PII |

## 8. Ejemplo de conformidad

[`f36sbx_contract_example.json`](contrato/f36sbx_contract_example.json) contiene el mínimo que ejercita las doce relaciones: ocho artefactos sintéticos de ORG-S1 (VAC-0001 en `dev` y VAC-0004 en `test`), cuatro fragmentos y dos outputs, uno de ellos con abstención. **No es un corpus ni un dataset y no autoriza ninguna capacidad.** Sus textos están escritos a mano, sin datos reales, y sus hashes los calcula el propio validador. Sirve como objetivo de las pruebas de mutación: cualquier mutación que rompa una relación falla.

## 9. Garantía de que ninguna fuente real entra

1. Las fuentes cerradas de la sección 1 son la única entrada admitida, comprobada por ruta, por el hash del manifiesto F34 y por el del archivo.
2. La guardia EI-05 rechaza cualquier coincidencia de PII.
3. Un registro sin los seis marcadores no entra.
4. No se admiten rutas fuera del repositorio, URL ni descargas.
5. Nombres de persona: los documentos no tienen campo de nombre y ningún campo puede contener el token `name`. Los `counterfactual_pair` usan marcadores de grupo sintéticos (`grupo_sintetico`) y no nombres propios.
