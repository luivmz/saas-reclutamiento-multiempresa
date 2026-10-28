# F36-SBX — Contrato de datos y de evidencia sintética

> Fase F36-SBX, versión 4 (26/10/2026). Corrige AF1-M02 ([corrección AF1](F36SBX_Correccion_AF1.md)), AF2-M02, AF2-M03 y AF2-L01 ([corrección AF2](F36SBX_Correccion_AF2.md)) y AF3-M02 ([corrección AF3](F36SBX_Correccion_AF3.md)); las correcciones [AF4](F36SBX_Correccion_AF4.md) y [AF5](F36SBX_Correccion_AF5.md) no lo cambian. Candidata a una sexta auditoría independiente. **Es un contrato de diseño: F36-SBX no genera ningún corpus.** La fuente normativa es [`f36sbx_evidence_contract.json`](contrato/f36sbx_evidence_contract.json) (`contract_version = 4`); este documento lo explica y, si difiriera, manda el JSON. Su [ejemplo de conformidad](contrato/f36sbx_contract_example.json) demuestra que el contrato se puede cumplir. Ambos los verifica [`validate_f36sbx.py`](../tools/f36sbx/validate_f36sbx.py) con la regla CTR.

## 1. Principios

1. **Solo sintético.** `source_type = synthetic` y `environment = sandbox` en todo registro. No existe un valor que admita una fuente real.
2. **Contrato cerrado.** Cada estructura tiene una lista exacta de campos: sobre del artefacto, contenido por tipo, elementos de lista, fragmento, output, configuración del método, provenance, referencia upstream, manifiesto de particiones, particiones y umbrales. Un campo ausente o adicional, un tipo desconocido, un valor fuera de su enumerado o un identificador fuera de patrón invalidan el registro.
3. **Fuentes cerradas y tipadas.** Una referencia upstream solo puede citar las tres tablas F34 de `upstream_files` (`applications.csv`, `criteria.csv` y `vacancies.csv`). Cada una declara su clave, su ámbito de tenant, las columnas de contexto que se comparan y su cardinalidad (sección 5.3). El hash de cada tabla debe coincidir con el que declara el [manifiesto F34](../datos-sinteticos/README.md) y con el del archivo. Los fixtures de F35-SBX son un patrón de marcadores y de provenance, no una fuente de registros. Los adjuntos de gobierno (`g0-evidence`), `storage`, cualquier base de datos y cualquier URL están excluidos.
4. **Sin fuentes globales.** `global_upstream_sources` está vacía. Una fuente global futura exigiría un tipo explícito, ser no personal, una semántica documentada y una versión nueva del contrato (`global_upstream_policy`).
5. **Cada identificador del contenido tiene una sola clase**, comprobada por el validador (sección 7):

   | Clase | Campos | Qué se comprueba |
   |---|---|---|
   | Ligado al tenant (`tenant_bound_tokens`) | `author_token` (`EV-S1-01`), `annotator_token` (`ANT36-S1-02`) | Su grupo `S1..S3` es la organización del artefacto |
   | Upstream (`content_upstream_bindings`) | `criterion_id` | Se cita entre las referencias upstream del artefacto, en `criteria.csv` y de su misma vacante |
   | Interno (`internal_references`) | `fragment_id`, `variant_of` y `rendered_from` | Apunta a un fragmento o artefacto del mismo conjunto y contexto (REL-08, REL-09 y REL-10) |
   | Global documentado (`global_identifiers`) | `question_id` | Catálogo sintético de preguntas que F34 comparte entre organizaciones (`pregunta:PRG-nnn` en `evidence.csv`). No es personal, no se resuelve upstream, se valida solo por patrón y no aporta contexto de tenant |

6. **Sin campos de persona ni de juicio.** Hay 44 nombres de campo prohibidos y una lista de tokens prohibidos (`score`, `rank`, `fit`, `name`, `email`, `emotion`, `level`, `select`…). Ningún campo de registro puede contener uno de esos tokens, así que un sinónimo como `candidate_score` tampoco pasa.
7. **Generador sin LLM** (EI-17 BLOCKED): plantillas versionadas, semilla declarada y salida reproducible byte a byte.
8. **Integridad.** El validador fija el SHA-256 del JSON canónico del contrato y comprueba además sus invariantes con mensajes propios. Cambiarlo exige un incremento auditado que actualice también el validador.

## 2. Qué se reutiliza

| Fuente | Qué aporta | Uso en F37-SBX | Límite |
|---|---|---|---|
| F34 `vacancies`, `criteria`, `rubric_levels` y `requirements` | Criterios explícitos y versionados | EI-01 a EI-04 y el texto de consulta de EI-07, EI-09 y EI-10 | Sin cambios: se leen, no se reescriben |
| F34 `applications`, `vacancies` y `criteria` | Identidad sintética de la postulación, la vacante y el criterio, con su organización | Referencias upstream obligatorias y contextuales de cada artefacto (REL-02, REL-04 y REL-13) | Solo los tokens sintéticos; nunca `person_token` ni datos de persona |
| F34 `evidence` y `annotations` | Evidencia registrada por personas sintéticas, con procedencia | EI-01, EI-03 y EI-04 | **No sirve para evaluar la recuperación.** Su texto plantilla cita literalmente el nombre del criterio (por ejemplo, «… vinculada a «Planificación de la enseñanza»»), así que cualquier búsqueda léxica acierta por construcción |
| F34 `requirement_checks` y `expected_alerts` | Oráculo de alertas deterministas | EI-02 | El oráculo no sustituye a la regla |
| F34 `fairness_sintetico` | Atributos de grupo sintéticos | Solo EI-24, para construir pares contrafactuales | Nunca como feature ni dentro de un texto de evidencia |
| F35-SBX contrato y fixtures | Seis marcadores, hash canónico y cadena de provenance | Patrón de los marcadores y de la provenance | Están congelados: no se modifican. Se crea un espacio de nombres propio (`SBX36-`) |

## 3. Registros

### 3.1 Sobre del artefacto

Todo artefacto tiene exactamente estos 16 campos: `synthetic_id`, `artifact_type`, `stage`, `synthetic_organization_id`, `scenario_id`, `vacancy_token`, `application_token`, `partition`, `template_family`, `source_type`, `environment`, `hash_algorithm`, `content`, `content_hash`, `provenance` y `record_hash`. Los cinco campos de contexto son organización, escenario, vacante, postulación y partición.

### 3.2 Tipos y contenido

| Tipo | Etapa | Contenido cerrado | Fragmentable |
|---|---|---|---|
| `cv_document` | A | `sections[]`, con `section_kind` (`formacion`, `experiencia` o `capacitacion`) y `text_synthetic` | Sí |
| `certificate` | A | `issuer_synthetic` (institución ficticia) y `title_synthetic` | Sí |
| `interview_transcript` | A | `question_id`, `transcript_kind = texto_sintetico_revisado`, `review_status = revisada_sintetica` y `turns[]`, con `speaker_role` y `text_synthetic`. No proviene de audio (EI-21 BLOCKED) | Sí |
| `human_observation` | A | `author_kind = human_synthetic`, `author_token` de su organización, `observation_kind` (`conducta_observada` o `aclaracion`, nunca una inferencia) y `text_synthetic` | Sí |
| `relevance_annotation` | A | `fragment_id`, `criterion_id`, `relevance` (`relevante` o `no_relevante`), `annotator_token` de su organización y `overlap_stratum` | No |
| `adversarial_case` | A | `attack_kind` (cinco valores cerrados), `text_synthetic` y `expected_outcome` (`rechazo` o `abstencion`) | Sí |
| `counterfactual_pair` | B (EI-24) | `variant_of`, `perturbation = marcador_de_grupo` y `grupo_sintetico`, el único lugar donde puede aparecer | No |
| `rendered_document` | B (EI-11) | `rendered_from` (un `cv_document`) y `format` (`pdf` o `docx`) | No |

Los textos son NFC, empiezan por `[SINTÉTICO]`, no superan 4000 caracteres, no tienen caracteres de control, de formato (como U+200B), privados ni no asignados, y no contienen correo, teléfono ni DNI (guardia EI-05). Las listas no pueden estar vacías.

### 3.3 Fragmento

Exactamente: `fragment_id`, `artifact_id`, `artifact_record_hash`, los cinco campos de contexto, `text_path` (por ejemplo, `sections/1/text_synthetic`), `char_start`, `char_end`, `text_hash` y `fragment_hash`.

### 3.4 Output de localización

Exactamente: `output_id`, `ei` (solo EI-07, EI-09 o EI-10), `method_id`, `method_version`, `method_config`, los cinco campos de contexto, `query_criterion_id`, `fragment_refs`, `fragment_ref_hashes`, `abstained`, `input_manifest_hash` y `output_hash`. `method_config` es cerrado: `normalization` (solo `nfkc_casefold`) y `top_k` (entero de 1 a 20). **El output no tiene ningún campo de texto ni de puntaje**: solo cita fragmentos (TEI-09 y TEI-14). `abstained` es booleano y es verdadero exactamente cuando no hay fragmentos. Sus cinco campos de contexto no son libres: son el contexto canónico de su postulación (sección 7.1, REL-15), también cuando se abstiene.

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
| 5 | `hash_algorithm = f36sbx-content-sha256-v1`, el marcador del algoritmo de `content_hash` |
| 6 | `synthetic_organization_id` en `ORG-S1..S3` |

## 5. Hashes y procedencia

### 5.1 JSON canónico y hash con etiqueta

- **JSON canónico:** `json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':'))`, codificado en UTF-8.
- **Hash con etiqueta:** SHA-256 de la etiqueta en UTF-8, un salto de línea y el JSON canónico. La etiqueta separa los dominios: un hash de un nivel nunca vale para otro.
- **Sin circularidad:** la preimagen de cada hash de registro es el registro completo **sin su propio campo de hash**. Por tanto, incluye todos los campos semánticos, también los hashes de los niveles inferiores.

### 5.2 Niveles

| Nivel | Etiqueta | Preimagen | Qué fija |
|---|---|---|---|
| `content_hash` | (sin etiqueta) | JSON canónico de `content` | El contenido. Se repite en la provenance |
| `record_hash` | `f36sbx-artifact-record-v1` | El artefacto completo sin `record_hash` | Identidad, tipo y etapa, organización, escenario, vacante, postulación, partición, familia, marcadores, contenido, `content_hash` y provenance completa: generador, versión, plantilla, familia, semilla y referencias upstream |
| `text_hash` | (sin etiqueta) | UTF-8 del texto de `text_path` entre `char_start` y `char_end` | El texto exacto del fragmento |
| `fragment_hash` | `f36sbx-fragment-v1` | El fragmento completo sin `fragment_hash` | Identidad, `artifact_id`, `artifact_record_hash` vigente de su artefacto, los cinco campos de contexto, `text_path`, offsets y `text_hash` |
| `input_manifest_hash` | `f36sbx-input-manifest-v1` | `{application_token, partition, fragments}`, con la lista ordenada de pares `[fragment_id, fragment_hash]` de la misma postulación y partición | El conjunto de entrada del output |
| `output_hash` | `f36sbx-output-v1` | El output completo sin `output_hash` | Identidad, EI, método, versión y `method_config`, contexto, criterio de la consulta, `fragment_refs`, `fragment_ref_hashes`, abstención e `input_manifest_hash` |
| `seal_sha256` | `f36sbx-test-seal-v2` | Sección 6.2 | El conjunto de test y lo que ajusta los umbrales |

**Encadenamiento.** El `artifact_record_hash` de un fragmento debe ser el `record_hash` vigente de su artefacto, y los `fragment_ref_hashes` de un output, los `fragment_hash` vigentes de sus `fragment_refs`, en el mismo orden. El validador recalcula cada nivel y nunca corrige: cambiar un registro sin recalcular su hash falla en ese nivel; recalcularlo sin actualizar el nivel siguiente falla en el siguiente.

### 5.3 Provenance y referencias upstream

| Elemento | Qué se exige |
|---|---|
| Provenance del artefacto | Exactamente `generator_id` (`GEN36-…`), `generator_version` (semver), `template_id` de la misma familia que el artefacto, `template_family` igual a la del artefacto, `seed` (entero ≥ 0), `upstream_refs` (lista no vacía) y `content_hash` igual al del artefacto |
| Referencia upstream | Exactamente `{source, ref, sha256}`, sin repetir. `source` es una de las tres tablas tipadas; cualquier otra es una fuente global no admitida. `sha256` coincide con el manifiesto F34 y con el archivo, y `ref` existe en la tabla |
| `applications.csv` | Clave `application_token`. Contexto comparado: organización, vacante y postulación. El artefacto cita **exactamente una vez** su propia postulación |
| `vacancies.csv` | Clave `vacancy_token`. Contexto comparado: organización y vacante. El artefacto cita **exactamente una vez** su propia vacante |
| `criteria.csv` | Clave `criterion_id`. Contexto comparado: la vacante y, a través de ella, la organización. Admite cualquier criterio de la misma vacante; el `criterion_id` del contenido tiene que estar citado |

El escenario de una referencia es el que el conjunto asigna a su vacante (REL-05 exige que sea único). Toda la provenance entra en `record_hash`: cambiar el generador, su versión, la plantilla, la semilla o una referencia upstream cambia ese hash y, si el artefacto es de test, el sello.

## 6. Particiones, sello de test y resellado

### 6.1 Particiones

| Regla | Contenido | Cómo se verifica |
|---|---|---|
| Solo `dev` y `test` | `train` está prohibida y cualquier otro valor es desconocido | REL-11 en cada registro y en el manifiesto |
| Sin conjunto de entrenamiento | El ajuste fino está BLOCKED (EI-22) | `train_allowed = false` en el contrato |
| Unidad de partición | `template_family` + `vacancy_token`. Ninguna familia de plantillas ni vacante aparece en más de una partición | REL-05 |
| Manifiesto | `partitions` (`dev` con `artifacts`; `test` con `artifacts`, `sealed`, `seal_algorithm` y `seal_sha256`), `thresholds` (`tuning_partition` y `tuning_outputs`) y `test_used_for_tuning`. Cada artefacto figura una sola vez y en su partición | REL-11 |
| Umbrales | Se ajustan solo con outputs de `dev` (`tuning_partition = dev`). La partición que cuenta es la canónica de la postulación del output, no la que declara. `test_used_for_tuning = false` | REL-11 y REL-15: un output de ajuste cuya postulación es de `test` falla, aunque se declare `dev` |
| Embargo temporal | Si se usan instantes del proceso, las vacantes de `test` cierran después de las de `dev`, con una purga igual a la de `process_splits` de F34 | `temporal_embargo = process_splits_f34` en el contrato |
| Contrafactuales | Las dos variantes van en la misma organización, escenario, vacante, partición y familia | REL-09 |
| Anotación | Dos anotadores independientes; el acuerdo se mide antes de usar el oro | Plan de evaluación, en F37-SBX |

### 6.2 Sello de test v2

`test.sealed = true`, `test.seal_algorithm = f36sbx-test-seal-sha256-v2` y `test.seal_sha256` es el hash con etiqueta `f36sbx-test-seal-v2` de:

| Campo de la preimagen | Contenido |
|---|---|
| `seal_algorithm`, `contract_version` | El algoritmo y la versión del contrato |
| `test_artifacts` | Pares ordenados `[synthetic_id, record_hash]` de los artefactos de test, incluido el oro de test (las anotaciones de relevancia) |
| `test_fragments` | Pares `[fragment_id, fragment_hash]` de los fragmentos de test |
| `test_outputs` | Pares `[output_id, output_hash]` de los outputs de test |
| `tuning_outputs` | Pares `[output_id, output_hash]` de los outputs de ajuste. Por la cadena de hashes fijan también los fragmentos y artefactos de dev que usan |
| `tuning_gold` | Pares `[synthetic_id, record_hash]` de las anotaciones de relevancia de dev, el oro con el que se ajustan los umbrales |
| `thresholds`, `test_used_for_tuning` | El manifiesto de umbrales y la prohibición de ajustar con test |

Así, el sello detecta cualquier cambio de un registro de test (postulación, vacante, organización, escenario, familia, generador, versión, semilla, provenance, referencias upstream, contexto de un fragmento o de un output, contenido u oro), de lo que ajusta los umbrales y de los propios umbrales.

### 6.3 Resellado

- Un cambio en un elemento sellado exige recalcular todos los hashes derivados, en orden (contenido, registro, fragmento, manifiesto de entrada y output), y volver a sellar **antes de ejecutar cualquier método** (`test_sealed_before_any_run`). Recalcular los registros sin resellar hace fallar REL-11.
- Un conjunto resellado es un conjunto sellado nuevo, y vale si es conforme. El sello no es una firma: prueba la integridad frente al valor registrado, y su ancla es el commit auditado que lo contiene. F37-SBX debe registrar el sello antes de la primera ejecución.
- Dev no se sella, salvo lo que fija el ajuste (outputs de ajuste, por transitividad sus fragmentos y artefactos, y el oro de dev). Un artefacto de dev que el ajuste no usa puede cambiar sin resellar; es un límite documentado, no una garantía del sello.

## 7. Aislamiento entre organizaciones

| Control | Regla | Relación |
|---|---|---|
| Identificadores | El segmento de organización de `synthetic_id`, `fragment_id` y `output_id` es `synthetic_organization_id` | REL-03 |
| Vacante y postulación | Existen en F34 con la misma organización, y la postulación es de esa vacante | REL-04 |
| Unicidad de contexto | Una vacante pertenece a una sola organización y a un solo escenario; una postulación, a una sola organización, escenario y vacante | REL-05 |
| Autor y anotador | `author_token` y `annotator_token` llevan el tenant en su grupo (`EV-S1-…`, `ANT36-S1-…`), que debe ser el del artefacto | REL-13 |
| Referencias upstream | Cada referencia se resuelve en su tabla y su contexto (organización, escenario, vacante y postulación, según la tabla) debe ser el del artefacto. Una referencia de otro tenant, de otra vacante, de otro escenario o de otra postulación falla | REL-13 |
| Fuentes globales | No hay ninguna admitida; una fuente fuera de las tres tablas tipadas falla | REL-13 |
| Fragmentos, outputs y referencias internas | Mismo contexto que su artefacto, sus fragmentos o el registro que citan | REL-06 a REL-10 |
| Contexto canónico de los outputs | Todo output, también una abstención y un output de ajuste, tiene el contexto canónico de su postulación (sección 7.1) | REL-15 |

### 7.1 Contexto canónico (REL-15)

La fuente del contexto es una sola: **los artefactos de la postulación en el conjunto** (`canonical_context`, con clave `application_token` y fuente `artifacts`). Como REL-05 obliga a que una postulación tenga una sola organización, escenario y vacante, y una vacante una sola partición, ese contexto es único. De él se derivan:

- los fragmentos, que deben tener el contexto de su artefacto (REL-06);
- todo output, que debe tener exactamente la organización, el escenario, la vacante, la postulación y la partición canónicas de su postulación. Así lo exige REL-15, también a una abstención, aunque no cite fragmentos que lo delaten, y a un output de ajuste;
- el ajuste: un output de ajuste debe ser de `dev` por el contexto canónico de su postulación (REL-11).

Un output cuya postulación no tiene artefactos en el conjunto no tiene contexto canónico y falla. También falla si el contexto es ambiguo. No se pueden inventar el escenario, la partición ni la vacante de una abstención, ni cambiarlos: con todos los hashes recalculados y `test` resellado, el cambio sigue fallando. Lo que sí admite el contrato es una abstención legítima de otra postulación que tenga evidencia en el conjunto, con su contexto canónico.

## 8. Relaciones verificables

| ID | Relación |
|---|---|
| REL-01 | Sobre cerrado, tipo conocido con su etapa, seis marcadores, contenido cerrado con enumerados, patrones o listas no vacías, `content_hash` y `record_hash` correctos |
| REL-02 | Provenance cerrada: generador, plantilla de su familia, semilla, el mismo `content_hash` y referencias upstream verificables contra el manifiesto F34, con la cardinalidad de su tabla y el criterio del contenido citado |
| REL-03 | Identificadores únicos, con el segmento de organización igual a `synthetic_organization_id` |
| REL-04 | La vacante y la postulación existen en F34, con la misma organización y la misma vacante |
| REL-05 | Vacante → una organización y un escenario; postulación → una organización, un escenario y una vacante; familia y vacante → una partición |
| REL-06 | Cada fragmento apunta a un artefacto fragmentable existente y a su `record_hash` vigente, con `text_path` válido, offsets dentro del texto, `text_hash` y `fragment_hash` correctos y el mismo contexto |
| REL-07 | Cada output usa una EI de localización y la configuración cerrada, consulta un criterio F34 de su vacante, cita fragmentos existentes de su mismo contexto con sus `fragment_hash`, se abstiene solo sin fragmentos y trae `input_manifest_hash` y `output_hash` correctos |
| REL-08 | Cada anotación cita un fragmento existente de su contexto y un criterio F34 de su vacante |
| REL-09 | Cada par contrafactual cita una variante fragmentable de su misma organización, escenario, vacante, partición y familia |
| REL-10 | Cada documento renderizado cita un `cv_document` de su misma postulación, partición y familia |
| REL-11 | Manifiesto cerrado: solo `dev` y `test`, cada artefacto una vez y en su partición, `test` sellado con el sello v2 y umbrales ajustados solo con outputs de `dev` por el contexto canónico de su postulación |
| REL-12 | Textos NFC, con `[SINTÉTICO]`, sin caracteres invisibles ni de control y sin patrones de PII |
| REL-13 | Aislamiento entre tenants: autores y anotadores de la organización del artefacto, referencias upstream resueltas y compatibles con su contexto, sin fuentes globales, y cada identificador del contenido con una sola clase |
| REL-14 | Identificador cerrado del ejemplo y cobertura mínima |
| REL-15 | Contexto canónico: todo output, también una abstención sin fragmentos y un output de ajuste, tiene la organización, el escenario, la vacante, la postulación y la partición de su postulación, derivados de sus artefactos del conjunto; una postulación sin artefactos o con contexto ambiguo no admite outputs |

## 9. Ejemplo de conformidad

[`f36sbx_contract_example.json`](contrato/f36sbx_contract_example.json) contiene el mínimo que ejercita las quince relaciones: nueve artefactos sintéticos de ORG-S1, cuatro fragmentos y tres outputs, en dos escenarios (SC36-01 con VAC-0001 en `dev` y SC36-02 con VAC-0004 en `test`). Tiene oro en `dev` y en `test`, un output de ajuste en `dev`, un output de test con fragmentos y otro con abstención, y su `test` está sellado con el sello v2. **No es un corpus ni un dataset y no autoriza ninguna capacidad.** Sus textos están escritos a mano, sin datos reales, y sus hashes los calculan las funciones del propio validador.

Su `example_id` es exactamente `f36sbx-contract-example`. La cobertura mínima (`example_coverage`) exige los ocho tipos de artefacto, al menos un fragmento, un output con fragmentos, un output con abstención, un artefacto de test, una anotación de oro en test, un output de test, un output de ajuste y dos escenarios: un ejemplo vacío o recortado no es conforme. Sirve como objetivo de las pruebas de mutación: cualquier mutación que rompa una relación falla. La mutación exhaustiva de sus hojas, que incluye la sustitución de cada valor por otro válido de su dominio con todo resellado, está en [`meta_f36sbx.py`](../tools/f36sbx/meta_f36sbx.py).

## 10. Garantía de que ninguna fuente real entra

1. Las tres tablas tipadas de la sección 5.3 son la única entrada admitida, comprobada por ruta, por el hash del manifiesto F34 y por el del archivo. No hay fuentes globales.
2. La guardia EI-05 rechaza cualquier coincidencia de PII.
3. Un registro sin los seis marcadores no entra.
4. No se admiten rutas fuera del repositorio, URL ni descargas.
5. Nombres de persona: los documentos no tienen campo de nombre y ningún campo puede contener el token `name`. Los `counterfactual_pair` usan marcadores de grupo sintéticos (`grupo_sintetico`) y no nombres propios.
