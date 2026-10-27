# F36-SBX — Corrección AF3 (tercera auditoría independiente)

> Fase F36-SBX, corrección focal del 26/10/2026, en la rama `feature/f36-sbx-authorization-design`, sobre el candidato auditado `ecb22cc6cb35db110f164240e08c623eab16871f`. Candidata a una **cuarta auditoría independiente**. **AF3-M01, AF3-M02 y AF3-L01 corregidos por implementación, pendientes de cuarta auditoría independiente.** Este documento no los declara cerrados: los cierra, o no, esa auditoría.

## 1. Veredicto recibido

La tercera auditoría independiente del candidato `ecb22cc` concluyó **no aprobado para integración**, con 0 BLOCKER, 0 HIGH, 2 MEDIUM correctivos y 1 LOW. Este registro transcribe lo comunicado; el informe de la auditoría no forma parte del repositorio.

La auditoría reprodujo:

- `validate_f36sbx.py`: 55/0;
- `test_f36sbx.py`: 425/0;
- las 660 mutaciones de hojas, con 0 falsos PASS en esa familia;
- 93 ablaciones, todas detectadas;
- SBX-01..SBX-18: 18/18;
- `git diff --check`, limpio.

Sobre los hallazgos anteriores, dio por corregidos AF2-M02, AF2-M03 y AF2-L01. AF2-M01 quedó **no corregido de forma integral**: la coherencia entre el registro y el bloque canónico sí lo estaba, pero no la pertenencia del ADR al candidato, que es AF3-M01.

| ID | Severidad | Hallazgo |
|---|---|---|
| AF3-M01 | MEDIUM | El validador aceptaba como evidencia de FG-12 un ADR que no estaba versionado en `candidate_commit`: leía sus bytes del sistema de archivos, y un ADR bajo un directorio ignorado pasaba con 55/0 |
| AF3-M02 | MEDIUM | Una abstención, que no cita fragmentos, podía declarar otro escenario u otra partición, y entrar incluso entre los outputs de ajuste, con todos los hashes recalculados y `test` resellado |
| AF3-L01 | LOW | `auditor.name = "placeholder"` se aceptaba |

## 2. Reproducción independiente sobre `ecb22cc`

Antes de cambiar nada se reprodujeron los hallazgos sin depender de los archivos de la auditoría:

- AF3-M01, con Git real, en un clon local desechable del HEAD exacto;
- AF3-M02 y AF3-L01, en memoria, con hashes recalculados y `test` resellado.

Las seis variantes materiales fueron falsos PASS. Los cuatro ataques AF2 ya cerrados siguieron fallando.

| # | Ataque | En `ecb22cc` | En este candidato |
|---|---|---|---|
| 1 | ADR canónico válido bajo `htmlcov/` (ignorado): `git check-ignore` = 0 y `git cat-file -e` = 128; FG-03 y FG-12 sintéticas | Falso PASS (55/0) | Falla (G02, AF3-01) |
| 2 | Abstención OUT-0002 con `scenario_id` SC36-01 | Falso PASS | Falla (AF3-12) |
| 3 | Abstención OUT-0002 con `scenario_id` SC36-99 | Falso PASS | Falla (AF3-13) |
| 4 | Abstención OUT-0002 en `dev` y añadida a `tuning_outputs` | Falso PASS | Falla (AF3-19) |
| 5 | Abstención OUT-0002 en `dev`, sin ajuste | Falso PASS | Falla (AF3-18) |
| 6 | `auditor.name = "placeholder"` en el registro y en el bloque | Falso PASS | Falla (AF3-26) |
| 7 | Trasplante APP-00013 → APP-00015 sin resellar (AF2-M02) | Falla | Falla (AF2-13) |
| 8 | Autor EV-S2-01 en una observación de ORG-S1 (AF2-M03) | Falla | Falla (AF2-25) |
| 9 | `example_id` como objeto con `candidate_score` (AF2-L01) | Falla | Falla (AF2-32) |
| 10 | FG-02 aprobado con un informe NO_APROBADO (AF2-M01) | Falla | Falla (AF2-01) |

## 3. Corrección de AF3-M01: el ADR es el blob del commit candidato

**Causa.** `collect()` leía el ADR con `read_bytes()` del árbol de trabajo. El vínculo con el candidato se basaba en `git diff` y en `git ls-files --others --exclude-standard`, y ninguno de los dos enumera un archivo ignorado. Un ADR que no existía en `candidate_commit` pasaba, y además podía sustituirse.

**Solución.** Hay una sola vía para leer un documento de un commit, `git_blob(root, commit, ruta)`:

1. Resuelve `commit:ruta` con `git --literal-pathspecs ls-tree -z --full-tree`: la ruta no admite comodines y tiene que identificar exactamente una entrada.
2. Exige un blob regular, de modo `100644`. Un árbol, un enlace simbólico, un submódulo o un ejecutable fallan.
3. Lee los bytes con `git cat-file blob`. `blob_problem()` comprueba además que el tipo, el modo y el identificador del objeto (SHA-1 de Git) corresponden a esos bytes.
4. `collect()` resuelve cada ADR citado contra cada commit candidato citado, y `fg12_errors` calcula el SHA-256 y lee el bloque canónico **solo** de esos bytes. Los del árbol de trabajo no intervienen.
5. `git_facts` lee de la misma forma el documento del gate en el candidato.

Cualquier error de Git produce un fallo cerrado, nunca un PASS. El ADR no contiene el SHA del commit que lo contiene, porque sería autorreferente: su pertenencia se deriva del árbol Git del candidato.

**Generalización: evidencia versionable.** El mismo hueco afectaba a cualquier evidencia que Git ignorase, que nunca podría llegar a un commit: por ejemplo, con una exclusión local. La regla GATE falla ahora si Git ignora un archivo de `gate/evidencia/` y, de forma cerrada, si no puede determinarlo.

**Pruebas.**

- En memoria, AF3-01..AF3-11: ADR ausente del candidato, versionado solo en otro commit, árbol, enlace, submódulo, ejecutable, bytes distintos del objeto, SHA-256 de otra copia, evidencia ignorada y Git no evaluable.
- Con Git real, [`test_f36sbx_git.py`](../tools/f36sbx/test_f36sbx_git.py): 28 casos.
  - U01..U15 resuelven objetos en un repositorio mínimo.
  - G01..G11 ejecutan el validador completo en un clon local compartido, con evidencia sintética de FG-03 y FG-12 sin confirmar. G01 es un control positivo realista: el ADR es un blob versionado en el candidato y el validador termina sin fallas. Los demás son ataques que fallan: ADR solo en el sistema de archivos bajo `htmlcov/`, sin versionar, sustituido en el árbol de trabajo o en un commit posterior, un árbol, una ruta inexistente, un commit candidato equivocado, evidencia ignorada y un ADR añadido después del candidato.
  - R00 y R01 comprueban que el repositorio original no cambió y que los directorios temporales se borraron.

## 4. Corrección de AF3-M02: contexto canónico de todo output

**Causa.** La unicidad de contexto (REL-05) solo recorría artefactos, y un output solo se comparaba con los fragmentos que cita (REL-07). Una abstención no cita ninguno, así que su escenario y su partición no quedaban ligados a nada. El ajuste, además, confiaba en la partición que declaraba el output.

**Solución.** El contrato pasa a la versión 4, con `canonical_context` y REL-15:

- **Una sola fuente de contexto:** los artefactos de la postulación en el conjunto. REL-05 ya garantiza que ese contexto es único.
- **Todo output** (normal, abstención o de ajuste) tiene que tener exactamente la organización, el escenario, la vacante, la postulación y la partición canónicas de su postulación.
- Un output de una postulación sin artefactos en el conjunto, o con contexto ambiguo, falla.
- REL-11 comprueba la partición canónica de cada output de ajuste, no la declarada.

Es una derivación central, no una excepción para las abstenciones. El ejemplo de conformidad se reselló con la versión 4 y sigue siendo conforme.

**Pruebas.**

- Negativas, AF3-12..AF3-25, todas con hashes válidos: escenario incorrecto e inexistente, otra organización, vacante y postulación coherentes en F34 pero sin evidencia en el conjunto, postulación de la misma vacante sin evidencia, postulación de `dev` con vacante de `test`, `dev` sobre evidencia de `test`, `test` sobre contexto de `dev`, abstención añadida al ajuste, contexto incorrecto sin recalcular, con registros recalculados y con resellado completo, output con fragmentos, output de ajuste y contexto ambiguo.
- Controles positivos, P-12..P-14: abstenciones válidas en `dev`, en `test` (de una postulación con evidencia no fragmentable) y como output de ajuste.
- Contrato, C52..C54.

## 5. Corrección de AF3-L01: marcadores de identidad

`placeholder_key()` compara la identidad sin mayúsculas, tildes, dígitos ni puntuación. La lista de marcadores incluye `placeholder` y otras variantes razonables. Una identidad formada solo por palabras genéricas, como «Revisora externa independiente», se rechaza.

Las pruebas AF3-26..AF3-35 cubren `placeholder` en el registro y en el bloque (también en el repositorio), `PLACEHOLDER`, `<Placeholder 1>`, `place_holder`, `Pláceholder`, `Auditor 1`, `por definir`, un espacio final, U+200B y una identidad genérica. P-07 comprueba que nombres legítimos con tildes, guiones y puntuación siguen siendo válidos, y P-08 el contraste.

**Límite.** Sigue siendo una validación estructural de una identidad declarada, no una autenticación: la autenticidad, la independencia y la procedencia del auditor siguen siendo revisión humana.

## 6. Metapruebas y oráculo

- **Familia de sustitución por valores válidos del dominio**, nueva, en [`meta_f36sbx.py`](../tools/f36sbx/meta_f36sbx.py). Cada texto del ejemplo se sustituye por otro valor válido (el de otro registro, un valor enumerado del contrato o un identificador F34 coherente) y se resella todo.
  - Sobre el validador de `ecb22cc`, esta familia reproduce los tres falsos PASS de AF3-M02. Sobre este candidato, 810 sustituciones dan 0 falsos PASS.
  - Los 86 cambios conformes son legítimos y están en una lista cerrada y justificada: contenido libre o enumerado, autor o anotador del mismo tenant, plantilla de la misma familia, criterio de la misma vacante, una anotación de oro que pasa a otro fragmento del mismo contexto y un output de otra postulación con evidencia en su mismo contexto.
  - En la evidencia, también se sustituye cada valor enumerado de un solo lado.
- **Familia de forma.** Se conservan las 505 mutaciones del ejemplo, con 0 falsos PASS.
- **Ablación.** 113 ablaciones: 11 reglas, 19 funciones, 77 comprobaciones de código y 6 repeticiones con el ejemplo resellado por el validador debilitado.
  - Las ablaciones de las piezas que dependen de Git se ejecutan también contra la batería con Git real.
  - Una detección debida solo a una excepción global, o a un caso cuya mutación ya no se puede montar, no cuenta como pertinente.
  - Primera ejecución, sobre `9481fe2` (2024 s): 110 detectadas por casos pertinentes, ninguna solo por excepción y 3 supervivientes. Las tres eran ramas defensivas que la defensa en profundidad enmascaraba, sin ningún defecto del validador:
    - «una sola entrada con la ruta exacta» y «blob legible» no se alcanzan con Git real y rutas válidas. U16..U18 simulan la salida de Git y exigen un fallo cerrado con su propio motivo;
    - «resolución con error» seguía fallando, pero con otro motivo. AF3-01, AF3-11 y los escenarios G exigen ahora el motivo exacto.
  - Una reejecución dirigida detecta las tres. La ejecución completa sobre el candidato final se registra en la sección 6.1.
- **Oráculo independiente (T05).** Los hashes y el sello del ejemplo se recalculan con una implementación propia del esquema documentado, sin usar las funciones del validador. Así, un error compartido entre el validador y el generador aparecería como divergencia.
- **Límites.** Ninguna de estas metapruebas es una demostración universal de que no existen falsos PASS. La lista de marcadores de identidad es una guardia, no una autenticación. La prosa libre sigue sin interpretarse. El sello no es una firma. Dev, fuera de lo que usa el ajuste, no se sella.

### 6.1 Ejecución completa sobre el candidato final

`meta_f36sbx.py ablaciones` sobre `4107ba6` (2118 s), con línea base sin fallas en memoria y con Git real: **113 ablaciones, 113 detectadas por casos pertinentes, ninguna solo por excepción y 0 supervivientes.** Las ramas defensivas de la primera ejecución se detectan con U16 y U17 (una sola entrada con la ruta exacta), U18 (blob legible), y con AF3-01, AF3-11 y los escenarios G (resolución con error). `meta_f36sbx.py hojas` dio 505 mutaciones de forma, 810 sustituciones y 243 mutaciones y sustituciones de evidencia, con 0 falsos PASS. El código no cambió después de esa ejecución: este registro es el único cambio posterior.

## 7. No regresión de AF2

Siguen pasando, sin cambios de criterio:

- la parte corregida de AF2-M01, coherencia entre registro y bloque: AF2-01..AF2-12 y D01..D46;
- AF2-M02, cadena de hashes y sello: AF2-13..AF2-24, H01..H12 y P-01..P-04;
- AF2-M03, tenants: AF2-25..AF2-30, X01..X10, P-05 y P-06;
- AF2-L01, identificador y cobertura: AF2-31..AF2-33 y L01..L05.

La reproducción independiente confirma que sus ataques siguen fallando.

## 8. Lo que no cambia

- F36-SBX = EN DISEÑO; F36-SBX-GATE = NO SUPERADO. FG-02, FG-03, FG-10 y FG-12 siguen pendientes y sin evidencia registrada: la evidencia sintética de las pruebas solo existe en memoria o en clones desechables. F37-SBX = BLOQUEADA.
- G0 real = NO APROBADA; G0-SBX = APROBADA CON RESTRICCIONES; ADR-005 = PROPUESTA; Alcance C = BLOQUEADO; Datos reales = PROHIBIDOS.
- EI-09 sigue CONDITIONAL (F36-M02) y el ADR sucesor sigue siendo una propuesta (F36-M03); F36-M01 sigue pendiente de FG-03.
- RF-23 sigue siendo la decisión final humana y RF-29 sigue experimental.
- No hay ML, NLP productivo, embeddings, OCR, parsing, LLM, endpoints, migraciones, UI ni dependencias nuevas. F35-SBX, F34, el runtime y el gobierno global no cambian.
