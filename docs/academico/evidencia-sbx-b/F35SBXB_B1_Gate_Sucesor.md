# F35-SBX-B — B1: gate sucesor sobre HEAD

> Incremento B1 de F35-SBX-B, versión 1 (09/10/2026). Rama `feature/f35-sbx-b-deterministic-pipeline`, creada desde `develop` `430f3f544c3542cabac8028a122c8a0c2a97390b`, que integra [B0](F35SBXB_B0_Sucesion_de_Gates.md). B1 construye solo el **mecanismo de control** que exigen DH-B04 y DH-B13 antes de cualquier pipeline: no hay pipeline funcional, SQLite, máquina de estados, informe, purga ni ML.

## 1. Qué es el gate

[`validate_f35sbxb.py`](../tools/f35sbxb/validate_f35sbxb.py) valida el **HEAD actual** de la rama de B, de `develop` o de `main`. No sustituye esa validación por los gates históricos: estos siguen congelados y se ejecutan anclados como evidencia complementaria (DH-B01, DH-B02). Solo usa la biblioteca estándar.

El gate primero **recoge** el estado real (Git, índice, sistema de archivos y documentos) y después **evalúa** reglas puras sobre ese estado. Los casos negativos mutan una copia del estado en memoria; la detección real de flags, enlaces y archivos ocultos se demuestra además con Git real en clones desechables (§7).

## 2. Comprobaciones

| ID | Qué comprueba | Origen |
|---|---|---|
| CTX | Rama `feature/f35-sbx-b-deterministic-pipeline`, `develop` o `main`; HEAD no separado; E, el cierre de B0 y la base de B como ancestros de HEAD | Plan B1 §4.A y §4.J; DH-B04 |
| AIN | F35-SBX-A idéntica a E: 22 archivos con los bytes reales del blob de E, sin archivos extra ni enlaces; árbol de HEAD sin cambios frente a E en esas rutas | DH-B09 |
| B0F | El documento de B0 idéntico a su cierre auditado | B0 CERRADA |
| SBX | SBX-01..SBX-18 recalculados uno por uno sobre HEAD (§4) | DH-B13 |
| GOV | Los trece estados de gobierno exactos en `CLAUDE.md` y `docs/PROGRESS.md`; F35-SBX-B solo INICIADA; ninguna línea añadida que desbloquee G0 real, ADR-005, F35 productiva, F36–F40, el alcance C o los datos reales | DH-B11; plan B1 §4.E |
| SCP | Delta exacto respecto de la base de B (árbol de HEAD, árbol de trabajo, índice y archivos sin seguimiento): solo las rutas autorizadas, con el estado esperado, y las obligatorias presentes | DH-B03; plan B1 §4.F y §4.K |
| FSY | Recorrido real de `evidencia-sbx-b/` y `tools/f35sbxb/`: ningún archivo fuera de la lista, aunque Git lo ignore; ningún enlace; solo `.pyc` regulares en `tools/f35sbxb/__pycache__` | Plan B1 §4.I |
| FLG | Ningún flag del índice en todo el repositorio: solo `H` en `git ls-files -v` (`h` = assume-unchanged, `S` = skip-worktree, `s` = ambos) | Plan B1 §4.I |
| CNT | Archivos de B: UTF-8 sin NUL, CR ni BOM; sin correos, DNI, teléfonos ni RUC; solo `.md`, `.json` y `.py`; claves JSON sin vocabulario de puntaje, ranking, recomendación, selección, OCR, extracción ni embeddings | Plan B1 §7 |
| DEP | Código de `tools/f35sbxb/` solo con la biblioteca estándar autorizada, sin importaciones dinámicas, red ni dependencias de ML | DH-B12; TSBB-09 |

Cualquier error de Git, de lectura o de importación, criterio no evaluable o estado desconocido hace fallar el gate (DH-B10).

## 3. Alcance exacto de B1

Delta respecto de la base de B (`430f3f5`), sin subconjuntos de las obligatorias ni superconjuntos:

| Ruta | Estado | Obligatoria |
|---|---|---|
| `CLAUDE.md` | M | Sí |
| `docs/PROGRESS.md` | M | Sí |
| `docs/academico/evidencia-sbx-b/README.md` | M | Sí |
| `docs/academico/evidencia-sbx-b/F35SBXB_B1_Gate_Sucesor.md` | A | Sí |
| `docs/academico/tools/f35sbxb/validate_f35sbxb.py` | A | Sí |

`docs/academico/ACADEMIC_BASELINE.md` no cambia: solo registra cierres. Cada incremento posterior de B amplía esta lista en el propio gate, con su auditoría.

## 4. DH-B13 en el gate

- Antes de importar nada, el gate comprueba que `validate_f34e.py` y los tres módulos que su función `compute_sbx()` carga (`validate_f34.py`, `validate_f34a.py` y `validate_f34b.py`) son idénticos byte a byte a sus blobs en E. Si no se puede verificar, el gate falla sin importar.
- Ejecuta solo `compute_sbx()`, sin generar bytecode, y exige exactamente SBX-01..SBX-18.
- Por cada criterio informa ID, PASS o FAIL, fuente, comprobación aplicada (de la [matriz de criterios](../g0-sandbox/F34E_Matriz_Criterios_G0_SBX.md)) y, si falla, el motivo.
- Un criterio ausente, una excepción o un resultado que no sea verdadero hacen fallar el gate: es un incumplimiento sustantivo (clase B) o no evaluable.
- `validate_f34e.py` completo sobre HEAD sigue fallando por su alcance Git histórico (clase A). El gate no lo presenta como revocación ni lo ignora: esa falla es justamente la que obliga a recalcular los 18 criterios.

No se reutiliza ninguna otra función de los validadores congelados.

## 5. El gate del gate

| Etapa | Integridad del gate |
|---|---|
| **Desarrollo de B** (ahora) | El gate es mutable y forma parte de la lista exacta de rutas de B. No se valida a sí mismo: cada cambio suyo se acredita con la auditoría del incremento que lo introduce, y el gate exige que esté presente y sea Python de la biblioteca estándar autorizada |
| **Congelamiento** (cierre de B) | Un commit de cierre fija el gate y los artefactos de B. Desde ese momento se comparan con ese cierre, identificado por la historia y no por hashes futuros |
| **Después de B** | Cuando una fase posterior autorizada empiece, el gate de B pasa a ser histórico: se ejecuta anclado sobre su cierre y la nueva fase aporta su propio gate sucesor sobre HEAD, que verifica la integridad de B y recalcula SBX-01..SBX-18 (protocolo de B0 y DH-B13) |

Así el gate de B nunca tiene que modificarse para que otra fase avance, y una fase posterior no queda bloqueada como quedó B ante los gates de A. Esto documenta la sucesión futura; **no autoriza F36** ni ninguna otra fase.

## 6. Reglas de seguridad concretas

| Intento | Cómo lo detecta el gate |
|---|---|
| Datos reales, PII, CV, audio o vídeo | SBX-01..SBX-04 y SBX-14; CNT (patrones de PII y tipos de archivo); integridad del dataset en SBX |
| Scoring, recomendación, «mejor candidato», selección automática o ranking nuevo | SBX-05..SBX-07 y SBX-09; claves JSON prohibidas en CNT |
| OCR, parsing, extracción, embeddings o búsqueda semántica | Claves JSON prohibidas en CNT; DEP; SCP impide tocar el runtime |
| Integración productiva, endpoints o migraciones | SCP (ninguna ruta del runtime autorizada); SBX-15 y SBX-16 |
| Dependencias de ML | DEP; SCP impide tocar `composer.json`, `package.json` y similares |
| Modificar RF-23 | SBX-08; SCP impide tocar la matriz de trazabilidad |
| Desbloqueo falso de G0 real, ADR-005, F35 productiva, F36–F40, alcance C o datos reales | GOV; SBX-13, SBX-17 y SBX-18 |

## 7. Pruebas de B1

Los casos negativos viven dentro del gate, igual que en F35-SBX-A, sin `tests/` productivos. Cada uno muta una copia del estado recogido y exige que la regla indicada lo detecte.

| Caso | Regla | Negativo |
|---|---|---|
| NB-01 | SBX | SBX-05 incumplido (campo de puntaje en `schema.json`) |
| NB-02 | GOV | G0 real declarada APROBADA |
| NB-03 | CNT | Dato personal real en un documento de B |
| NB-04 | AIN | Archivo protegido de F35-SBX-A alterado |
| NB-05 | SCP | Cambio productivo fuera del alcance (`app/`) |
| NB-06 | FSY | Archivo extra no autorizado, aunque Git lo ignore |
| NB-07 | FSY | Enlace simbólico en una ruta de B |
| NB-08 | FLG | assume-unchanged |
| NB-09 | FLG | skip-worktree |
| NB-10 | CTX | Error de Git |
| NB-11 | CTX | Estado desconocido: HEAD separado |
| NB-12 | SBX | Estado desconocido: criterio SBX-18 no evaluable |
| NB-13 | GOV | Intento de habilitar F36–F40 |
| NB-14 | GOV | Línea añadida que habilita el alcance C |
| NB-15 | GOV | F35-SBX-B declarada CERRADA durante B1 |
| NB-16 | B0F | Documento de B0 modificado |
| NB-17 | DEP | Dependencia de ML en el código de B |
| NB-18 | CNT | JSON de B con un campo de puntaje |
| NB-19 | SBX | Módulo de `compute_sbx()` alterado: no se importa |

### 7.1 RED → GREEN (09/10/2026)

- **RED**, con la recogida del estado y los casos ya escritos y las diez reglas devolviendo una lista vacía: `validate_f35sbxb: 11 comprobaciones correctas, 18 fallas`. Ninguno de NB-01..NB-18 se detectó. NB-19 ya pasaba porque prueba la verificación previa a la importación, que pertenece a la recogida.
- **GREEN**, con las reglas implementadas: `validate_f35sbxb: 29 comprobaciones correctas, 0 fallas`, con SBX-01..SBX-18 en PASS.

### 7.2 Demostración con Git real

En un clon desechable sin remoto, ya eliminado:

| Escenario | Resultado | Reglas en FALLA |
|---|---|---|
| Rama de B limpia | 29/0, PASS | — |
| `develop` con B1 integrada (`merge --no-ff`) | 29/0, PASS | — |
| `main` con B1 integrada (`merge --no-ff`) | 29/0, PASS | — |
| Campo de puntaje añadido a `schema.json` | FAIL | SBX (SBX-05), SCP |
| G0 real declarada APROBADA | FAIL | GOV |
| Correo personal en un documento de B | FAIL | CNT |
| Archivo de F35-SBX-A alterado | FAIL | AIN, SCP |
| Cambio en `app/Models/User.php` | FAIL | SCP; además SBX-08 y SBX-09 por el runtime modificado |
| Archivo extra oculto por `.git/info/exclude` | FAIL | FSY |
| Enlace simbólico en `evidencia-sbx-b/` | FAIL | FSY, SCP |
| assume-unchanged más G0 real APROBADA (`git status` no ve nada) | FAIL | FLG, GOV |
| skip-worktree en el documento de B0 | FAIL | FLG |
| `GIT_DIR` inválido | FAIL cerrado | Todas |
| HEAD separado o rama desconocida | FAIL | CTX |
| F36–F40 HABILITADAS o línea que habilita el alcance C | FAIL | GOV |

Cuando el cambio real altera el texto de partida de un negativo en memoria, ese negativo también falla («la mutación no se pudo aplicar»), lo que mantiene el gate en fallo.

### 7.3 Validación del incremento

- Validadores vigentes sobre HEAD: `validate.py`, `validate.py --cierre-f29`, `test_f32_safety.py`, `validate_f34a.py` y `validate_f29.py`, sin fallas.
- Gates históricos sobre HEAD: `validate_f30.py`, `validate_f33.py` y `validate_f34.py` pasan. `validate_f34b.py` y `validate_f34e.py` fallan solo por su alcance Git histórico (clase A de DH-B13). `validate_f35sbx.py` termina con un `StopIteration` no controlado: falla cerrado, sin diagnóstico (riesgo LOW ya registrado, que no se corrige porque A está congelada).
- Gates históricos anclados (`main` en `d63d094`, `develop` en `8054fed`): los seis pasan.
