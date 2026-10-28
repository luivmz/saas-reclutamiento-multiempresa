# F36-SBX — Corrección AF1 (primera auditoría independiente)

> Fase F36-SBX, corrección focal del 26/10/2026, en la rama `feature/f36-sbx-authorization-design`, sobre el candidato auditado `06e933e5c5184172b1473ae282db272e63b55ab3`. Candidata a una **segunda auditoría independiente**. Este documento no declara cerrados los hallazgos: los cierra, o no, esa segunda auditoría.

## 1. Veredicto recibido

El equipo comunicó el resultado de la primera auditoría independiente (AF1) del candidato `06e933e`: **no aprobado para integración**. La auditoría reprodujo `validate_f36sbx.py` en 49/0 y `test_f36sbx.py` en 87/0, pero sus mutaciones independientes encontraron 11 falsos PASS, agrupados en dos hallazgos MEDIUM. No hubo BLOCKER ni HIGH. Este registro transcribe lo comunicado; el informe de la auditoría no forma parte del repositorio.

| ID | Severidad | Hallazgo |
|---|---|---|
| AF1-M01 | MEDIUM | El gate aceptaba la evidencia de los criterios de equipo (FG-02, FG-03, FG-10 y FG-12) por existencia y tamaño del archivo, sin leer su contenido |
| AF1-M02 | MEDIUM | El contrato de evidencia y su validación aceptaban valores desconocidos y modificaciones que eliminaban garantías de provenance y de partición |

Al revisar el oracle durante la corrección se encontraron tres defectos más, que se tratan en este mismo incremento:

| ID | Severidad | Hallazgo |
|---|---|---|
| AF1-A01 | MEDIUM | En `NOT_ALLOWED_WORDS`, los patrones de OCR, LLM, PDF, DOCX y NER contenían bytes de retroceso (0x08) en lugar de `\b`, así que nunca coincidían. Una capacidad ALLOWED podía nombrar esas técnicas sin fallar. El defecto se introdujo al editar el validador con una cadena Python sin prefijo `r` |
| AF1-A02 | MEDIUM | El bloque de estado vigente admitía líneas desconocidas, y el paquete admitía afirmaciones de estado sobre sujetos que no estaban en la lista prohibida: una línea que declaraba F37-SBX-A habilitada, un ADR sucesor declarado aprobado o un alcance C sintético declarado autorizado |
| AF1-A03 | LOW | La clase de cada EI no estaba fijada: EI-09 podía pasar a ALLOWED si se actualizaba también el resumen de la matriz |

## 2. Reproducción sobre `06e933e`

Antes de cambiar nada, se reprodujeron en memoria, contra el validador tal como estaba en `06e933e`, mutaciones reconstruidas a partir de la descripción de los hallazgos. En el control sin mutaciones el validador daba 0 fallas. **18 de 19 mutaciones fueron falsos PASS**: debilitaban una garantía y el validador terminaba con 0 fallas.

| # | Mutación | Área | En `06e933e` | En este candidato |
|---|---|---|---|---|
| 1 | FG-02 en CUMPLE con un archivo cualquiera: vacío de semántica, de otro commit o con veredicto rechazado | Gate | Falso PASS | Falla (AUD-01, E01..E06) |
| 2 | FG-03 en CUMPLE con una autorización 2/3, con identidad duplicada o con una EI BLOCKED | Gate | Falso PASS | Falla (AUD-02, E07..E11) |
| 3 | FG-10 en CUMPLE con un registro de estructura desconocida | Gate | Falso PASS | Falla (AUD-03, E12) |
| 4 | FG-12 en CUMPLE con un ADR propuesto, de otro contexto o que autoriza una EI BLOCKED | Gate | Falso PASS | Falla (AUD-04, E13..E15) |
| 5 | Tipo de artefacto desconocido | Contrato | Falso PASS | Falla (AUD-05, C02, R02) |
| 6 | Transcripción sin revisar | Contrato | Falso PASS | Falla (AUD-06, C16, R42) |
| 7 | Valor enumerado nuevo: una observación como inferencia emocional | Contrato | Falso PASS | Falla (AUD-07, C17) |
| 8 | Provenance del artefacto sin `upstream_refs` ni `seed` | Contrato | Falso PASS | Falla (AUD-08, C11, R06..R08) |
| 9 | Fragmento sin `artifact_id` | Contrato | Falso PASS | Falla (AUD-09, C12, R09) |
| 10 | Partición sin separación por familia de plantilla | Contrato | Falso PASS | Falla (AUD-10, C09, R22) |
| 11 | Propiedad adicional peligrosa en un tipo | Contrato | Falso PASS | Falla (AUD-11, C14, R15, R16) |
| 12 | Campo sinónimo de puntaje (`candidate_score`) | Contrato | Falso PASS | Falla (AUD-12, C15) |
| 13 | Fuentes prohibidas recortadas | Contrato | Falso PASS | Falla (AUD-13, C18) |
| 14 | Estado del contrato cambiado | Contrato | Falso PASS | Falla (AUD-14, C19) |
| 15 | Embargo temporal eliminado | Contrato | Falso PASS | Falla (AUD-15, C10) |
| 16 | Capacidad ALLOWED que nombra OCR | Matriz | Falso PASS | Falla (AUD-16, M29a..M29g) |
| 17 | EI-09 reclasificada como ALLOWED | Matriz | Detectado solo por el resumen | Falla aunque se edite el resumen (M30) |
| 18 | Línea desconocida en el estado vigente | Gobierno | Falso PASS | Falla (AUD-17, M13) |
| 19 | Afirmación de que ADR-006 está aprobado | Paquete | Falso PASS | Falla (AUD-18, M14..M17) |

La batería AUD de [`test_f36sbx.py`](../tools/f36sbx/test_f36sbx.py) vuelve a aplicar estas mutaciones sobre el nuevo validador. Las cuatro primeras se aplican además como registro real en la fotografía del repositorio, con el estado del gate y la tabla FG actualizados.

## 3. Corrección de AF1-M01: evidencia de equipo

**Antes.** `evidence_ok()` comprobaba que existiera un archivo no vacío bajo `gate/evidencia/`. Cualquier contenido servía.

**Ahora** ([gate, secciones 8 y 9](F36SBX_Gate_Sucesor.md#8-formato-de-la-evidencia-de-equipo)):

1. **Formato cerrado y versionado.** [`f36sbx_team_evidence_schema.json`](gate/f36sbx_team_evidence_schema.json) (`f36sbx-team-evidence/v1`) fija un archivo por criterio, en una ruta fija, con campos exactos. Su SHA-256 canónico está fijado en el validador, y sus invariantes (veredictos aprobatorios, quórum 3/3, integrantes, ADR distinto de ADR-001..005…) se comprueban aparte.
2. **Semántica por criterio.**
   - FG-02 exige un veredicto aprobatorio y cero BLOCKER, HIGH y MEDIUM que requiera corrección, como enteros. También exige un auditor identificado e independiente, y un informe con su SHA-256 que nombra el commit candidato completo.
   - FG-03 exige la decisión de autorizar, la numeración confirmada, una lista explícita de EI ALLOWED o CONDITIONAL igual a la del estado del gate y la aprobación individual exacta de los tres integrantes.
   - FG-10 exige un registro cerrado, también cuando no hay dependencias nuevas: versión exacta, licencia admitida, origen canónico, 0 vulnerabilidades abiertas, EI relacionadas autorizadas y aprobación.
   - FG-12 exige un ADR sucesor APROBADO, existente y con hash, que nombra su id, F36-SBX y ADR-005. También exige la cobertura de las EI CONDITIONAL de alcance C autorizadas, sin EI BLOCKED, y la decisión explícita sobre EI-09.
3. **Vínculo reproducible con el candidato.** Todas las evidencias citan el mismo `candidate_commit` que el estado del gate. El validador comprueba en Git que es un commit que desciende de la base y es ancestro de HEAD. También comprueba que después solo cambiaron las rutas de registro, y en el documento del gate solo la columna Estado de la tabla FG.
4. **Fail-closed también en el validador, no solo en la decisión.** Un criterio de equipo en CUMPLE con evidencia inválida hace fallar la regla GATE, aunque el resultado siga siendo NO SUPERADO. En `06e933e` esa combinación pasaba con 0 fallas.
5. **Sin archivos sueltos.** `gate/evidencia/` no puede contener archivos sin citar, enlaces simbólicos ni archivos ilegibles.
6. **FG-10 nunca es NO APLICA**, y un estado no admitido para su criterio falla.

**Por qué el nuevo oracle impide los falsos PASS.** La decisión depende ahora del contenido, no de la existencia, y cada propiedad que la auditoría alteró es una comprobación explícita con su propio motivo de fallo: commit, veredicto, recuentos, quórum, identidad, lista de EI, estructura, estado del ADR, contexto y EI BLOCKED. La batería E lo prueba campo por campo contra un conjunto de evidencia válido que solo existe en memoria. El control positivo E00 demuestra que una evidencia correcta sí llevaría a SUPERADO, y GR01, que un registro parcial válido se acepta. Por tanto, el validador no se volvió simplemente más restrictivo.

**No se fabricó ninguna aprobación.** El estado del gate sigue con FG-02, FG-03, FG-10 y FG-12 PENDIENTES, `candidate_commit` nulo y sin carpeta `gate/evidencia/`. **F36-SBX-GATE = NO SUPERADO.**

## 4. Corrección de AF1-M02: contrato de evidencia

**Antes.** El contrato v1 listaba campos por tipo, pero el validador solo comprobaba unos pocos valores. Los enumerados, la provenance y las particiones podían cambiar sin fallar.

**Ahora** ([contrato v2](F36SBX_Contrato_Evidencia.md)):

1. **Contrato cerrado y fijado.** El validador fija el SHA-256 canónico del contrato y comprueba además sus invariantes con mensajes explícitos:
   - claves de primer nivel exactas;
   - `source_type` solo `synthetic`;
   - los ocho tipos;
   - enumerados cerrados sin `train`;
   - `author_kind`, `review_status` y `transcript_kind` únicos;
   - sobre, fragmento, output y provenance exactos;
   - campos y tokens prohibidos;
   - fuentes upstream cerradas;
   - garantías de partición exactas.
2. **Registros cerrados.** Sobre, contenido por tipo, elementos de lista, fragmento, output, provenance, referencia upstream y manifiesto de particiones tienen listas exactas de campos. Lo desconocido o ausente falla.
3. **Relaciones REL-01..REL-12.** Se validan sobre un [ejemplo de conformidad](contrato/f36sbx_contract_example.json) mínimo, con:
   - provenance recalculable;
   - referencias a F34 verificadas contra el manifiesto y contra el archivo;
   - vinculación de cada artefacto con su postulación y su vacante;
   - fragmentos que apuntan a artefactos existentes con su hash;
   - outputs que citan fragmentos existentes de su propio contexto;
   - aislamiento de organización, escenario, vacante y postulación;
   - partición cerrada con `test` sellado y ajuste solo con `dev`.

**Por qué el nuevo oracle impide los falsos PASS.** Cada debilitamiento reproducido cambia el hash fijado, y además viola una invariante semántica con su propio mensaje (batería C). Las garantías que la auditoría eliminaba en el contrato también se comprueban en los registros: quitar la provenance, una referencia obligatoria, el sello o la separación por familia falla en el ejemplo aunque el contrato no se toque (batería R). La validación de los registros usa el contrato fijado: si el contrato no supera sus invariantes, el ejemplo no se evalúa y la regla CTR falla.

## 5. Corrección de AF1-A01, AF1-A02 y AF1-A03

- **AF1-A01.** Los patrones usan `\b` real. La regla DEP rechaza cualquier byte 0x08 en `tools/f36sbx`, y las pruebas M29a..M29g y M51 lo comprueban.
- **AF1-A02.** El bloque de estado vigente debe tener exactamente las 16 líneas cerradas, sin desconocidas ni repetidas. Un escáner de afirmaciones `sujeto = ESTADO` revisa el paquete y los bloques de estado de gobierno. Cubre fases, puertas, ADR, alcance, datos, EI y RF, y solo admite el estado vigente de cada sujeto. La tabla de estados del charter se compara con el gobierno, y `CLAUDE.md` debe declarar exactamente a los tres integrantes que exige el quórum.
- **AF1-A03.** La clase y el alcance de las 24 EI están fijados en el validador. Reclasificar exige un incremento auditado.

## 6. Lo que no cambia

- F36-SBX = EN DISEÑO; F36-SBX-GATE = NO SUPERADO; F37-SBX = BLOQUEADA.
- G0 real = NO APROBADA; G0-SBX = APROBADA CON RESTRICCIONES; ADR-005 = PROPUESTA; Alcance C = BLOQUEADO; Datos reales = PROHIBIDOS.
- EI-09 sigue CONDITIONAL (F36-M02) y el ADR sucesor sigue siendo una propuesta sin número (F36-M03). F37-SBX-B sigue bloqueada.
- Los cuatro documentos de gobierno no cambian en este incremento.
- No hay ML, NLP, embeddings, OCR, parsing, LLM, endpoints, migraciones, UI ni dependencias nuevas. F35-SBX, el runtime y los datasets no cambian.

## 7. Límites conocidos

- La independencia del auditor es una declaración registrada (`kind` e `independent_of_candidate`). El validador no puede comprobar la identidad de una persona fuera del repositorio.
- El escáner de afirmaciones de estado reconoce la notación `sujeto = ESTADO` y `sujeto: ESTADO`. Una negación o una paráfrasis en prosa libre no son verificables por estructura y siguen dependiendo de la revisión humana.
- Esta versión del validador exige NO SUPERADO en el gobierno. Registrar toda la evidencia y declarar SUPERADO exige un incremento sucesor auditado.
