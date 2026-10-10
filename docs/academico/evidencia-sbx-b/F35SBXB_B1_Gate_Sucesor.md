# F35-SBX-B — B1: gate sucesor sobre HEAD

> Incremento B1 de F35-SBX-B, versión 2 (10/10/2026): la versión 1 se auditó en `f30cfe6c4adf9c3f7704b6bd665b6363a137b91a` y esta incorpora la corrección B1.1 (§8). Rama `feature/f35-sbx-b-deterministic-pipeline`, creada desde `develop` `430f3f544c3542cabac8028a122c8a0c2a97390b`, que integra [B0](F35SBXB_B0_Sucesion_de_Gates.md). B1 construye solo el **mecanismo de control** que exigen DH-B04 y DH-B13 antes de cualquier pipeline: no hay pipeline funcional, SQLite, máquina de estados, informe, purga ni ML.

## 1. Qué es el gate

[`validate_f35sbxb.py`](../tools/f35sbxb/validate_f35sbxb.py) valida el **HEAD actual** de la rama de B, de `develop` o de `main`. No sustituye esa validación por los gates históricos: estos siguen congelados y se ejecutan anclados como evidencia complementaria (DH-B01, DH-B02). Solo usa la biblioteca estándar.

El gate primero **recoge** el estado real (Git, índice, sistema de archivos y documentos) y después **evalúa** reglas puras sobre ese estado. Los casos negativos mutan una copia del estado en memoria; la detección real de flags, enlaces y archivos ocultos se demuestra además con Git real en clones desechables (§7).

## 2. Comprobaciones

| ID | Qué comprueba | Origen |
|---|---|---|
| CTX | Rama `feature/f35-sbx-b-deterministic-pipeline`, `develop` o `main`; HEAD no separado; E, el cierre de B0 y la base de B como ancestros de HEAD | Plan B1 §4.A y §4.J; DH-B04 |
| AIN | F35-SBX-A idéntica a E: 22 archivos con los bytes reales del blob de E, sin archivos extra ni enlaces; árbol de HEAD sin cambios frente a E en esas rutas | DH-B09 |
| HST | Historia completa de E a HEAD: el gate rechaza todo commit que haya tocado F35-SBX-A (contenido, modo, altas, bajas o renombrados), aunque después se restaure; en un merge cuenta lo que difiere de todos sus padres. Un repositorio superficial o una historia ilegible fallan cerrado | B1.1 M04; DH-B09 |
| B0F | El documento de B0 idéntico a su cierre auditado | B0 CERRADA |
| SBX | SBX-01..SBX-18 recalculados uno por uno sobre HEAD (§4) | DH-B13 |
| GOV | Los trece estados de gobierno exactos en `CLAUDE.md` y `docs/PROGRESS.md`; F35-SBX-B solo INICIADA. En el estado vigente, la cabecera y las líneas añadidas, el gate rechaza toda declaración de estado contradictoria para G0 real, ADR-005, G0-SBX, F35 productiva, F36–F40, alcance C, datos reales, F35-SBX-A/B, B0 y B1, en cualquier forma (mayúsculas, Markdown, `=`, `:`, `:=`, `->`); las citas y las prohibiciones no cuentan como declaración | DH-B11; B1.1 M02 |
| SCP | Delta exacto respecto de la base de B (árbol de HEAD, árbol de trabajo, índice y archivos sin seguimiento): solo las rutas autorizadas, con el estado esperado, y las obligatorias presentes | DH-B03; plan B1 §4.F y §4.K |
| FSY | Recorrido real de `evidencia-sbx-b/`, `tools/f35sbxb/` y de las superficies del runtime, el dataset y la evidencia (§8.3): todo archivo debe estar en el árbol de HEAD aunque Git lo ignore, ningún archivo de HEAD puede faltar y no se admiten enlaces; solo hay las excepciones explícitas de §8.3 | Plan B1 §4.I; B1.1 M03 |
| FLG | Ningún flag del índice en todo el repositorio: solo `H` en `git ls-files -v` (`h` = assume-unchanged, `S` = skip-worktree, `s` = ambos) | Plan B1 §4.I |
| CNT | Archivos de B: UTF-8 sin NUL, CR ni BOM; sin correos, DNI, teléfonos ni RUC; solo `.md`, `.json` y `.py`; claves JSON sin vocabulario de capacidades prohibidas; y, en los documentos mutables de B, el gate rechaza toda afirmación positiva que habilite una capacidad prohibida (§8.2) | Plan B1 §7; B1.1 M01 |
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
| Intento de modificar RF-23 | SBX-08; SCP impide tocar la matriz de trazabilidad |
| Intento de desbloqueo falso de G0 real, ADR-005, F35 productiva, F36–F40, alcance C o datos reales | GOV; CNT; SBX-13, SBX-17 y SBX-18 |

## 7. Pruebas de B1

Los casos negativos viven dentro del gate, igual que en F35-SBX-A, sin `tests/` productivos. Cada uno muta una copia del estado recogido y exige que la regla indicada lo detecte. La tabla reproduce literalmente los casos del gate: CNT solo trata una fila «NB-xx» como descripción de un negativo si coincide con un caso del código.

| Caso | Regla | Negativo |
|---|---|---|
| NB-01 | SBX | SBX-05 incumplido (campo de puntaje en schema.json) |
| NB-02 | GOV | G0 real declarada APROBADA |
| NB-03 | CNT | dato personal real en un documento de B |
| NB-04 | AIN | archivo protegido de F35-SBX-A alterado |
| NB-05 | SCP | cambio productivo fuera del alcance (app/) |
| NB-06 | FSY | archivo extra no autorizado en evidencia-sbx-b (ignorado por Git) |
| NB-07 | FSY | enlace simbólico en una ruta de B |
| NB-08 | FLG | assume-unchanged en CLAUDE.md |
| NB-09 | FLG | skip-worktree en el documento de B0 |
| NB-10 | CTX | error de Git |
| NB-11 | CTX | estado desconocido: HEAD separado |
| NB-12 | SBX | estado desconocido: criterio SBX-18 no evaluable |
| NB-13 | GOV | intento de habilitar F36–F40 |
| NB-14 | GOV | línea añadida que habilita el alcance C |
| NB-15 | GOV | F35-SBX-B declarada CERRADA en el estado vigente |
| NB-16 | B0F | documento de B0 modificado |
| NB-17 | DEP | dependencia de ML en el código de B |
| NB-18 | CNT | JSON de B con un campo de puntaje |
| NB-19 | SBX | Módulo de `compute_sbx()` alterado: no se importa |
| NB-20 | CNT | Markdown de B que afirma habilitar scoring y recomendación del mejor candidato |
| NB-21 | CNT | mayúsculas: OCR y alcance C habilitados |
| NB-22 | CNT | inglés: scoring y búsqueda semántica habilitados |
| NB-23 | CNT | datos reales permitidos |
| NB-24 | CNT | RF-23 automatizada |
| NB-25 | CNT | F36 autorizada |
| NB-26 | CNT | endpoints productivos activados |
| NB-27 | GOV | estado canónico más «g0 real = aprobada» |
| NB-28 | GOV | contradicción con Markdown en F35 productiva |
| NB-29 | GOV | contradicción con := en el alcance C |
| NB-30 | GOV | contradicción con dos puntos en datos reales |
| NB-31 | GOV | contradicción con flecha en G0 real |
| NB-32 | GOV | B1 declarada cerrada |
| NB-33 | FSY | archivo de runtime que no está en HEAD (ignorado) |
| NB-34 | FSY | archivo de HEAD ausente del runtime |
| NB-35 | FSY | enlace en una superficie del runtime |
| NB-36 | HST | commit posterior a E que toca F35-SBX-A (aunque se restaure) |
| NB-37 | HST | repositorio superficial |
| NB-38 | CNT | RF-23 declarada automática con dos puntos |

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
| Intento de declarar APROBADA la G0 real | FAIL | GOV |
| Correo personal en un documento de B | FAIL | CNT |
| Archivo de F35-SBX-A alterado | FAIL | AIN, SCP |
| Cambio en `app/Models/User.php` | FAIL | SCP; además SBX-08 y SBX-09 por el runtime modificado |
| Archivo extra oculto por `.git/info/exclude` | FAIL | FSY |
| Enlace simbólico en `evidencia-sbx-b/` | FAIL | FSY, SCP |
| assume-unchanged más intento de declarar APROBADA la G0 real (`git status` no ve nada) | FAIL | FLG, GOV |
| skip-worktree en el documento de B0 | FAIL | FLG |
| `GIT_DIR` inválido | FAIL cerrado | Todas |
| HEAD separado o rama desconocida | FAIL | CTX |
| Intento de habilitar F36–F40 o el alcance C | FAIL | GOV |

Cuando el cambio real altera el texto de partida de un negativo en memoria, ese negativo también falla («la mutación no se pudo aplicar»), lo que mantiene el gate en fallo.

### 7.3 Validación del incremento

- Validadores vigentes sobre HEAD: `validate.py`, `validate.py --cierre-f29`, `test_f32_safety.py`, `validate_f34a.py` y `validate_f29.py`, sin fallas.
- Gates históricos sobre HEAD: `validate_f30.py`, `validate_f33.py` y `validate_f34.py` pasan. `validate_f34b.py` y `validate_f34e.py` fallan solo por su alcance Git histórico (clase A de DH-B13). `validate_f35sbx.py` termina con un `StopIteration` no controlado: falla cerrado, sin diagnóstico (riesgo LOW ya registrado, que no se corrige porque A está congelada).
- Gates históricos anclados (`main` en `d63d094`, `develop` en `8054fed`): los seis pasan.

## 8. Corrección B1.1

La auditoría independiente de la versión 1 (`f30cfe6`) dejó B1 «IMPLEMENTADA / NO APROBADA PARA CIERRE» con cuatro hallazgos MEDIUM y uno LOW. B1.1 los corrige sin cambiar la arquitectura (recogida del estado más reglas puras), DH-B13, SBX-01..SBX-18 ni el alcance de B1. El gate sigue en desarrollo y necesita reauditoría: no está congelado.

### 8.1 Hallazgos y resolución

| Hallazgo | Problema | Resolución |
|---|---|---|
| M01 | CNT solo revisaba claves JSON: un Markdown autorizado podía afirmar capacidades prohibidas | CNT analiza el texto de los documentos mutables de B (§8.2) |
| M02 | GOV solo exigía las líneas canónicas: se podían añadir estados contradictorios en minúsculas | GOV analiza las declaraciones de estado en cualquier forma (§8.2) |
| LOW | GOV podía leer una prohibición como declaración | Las citas, las prohibiciones y los ejemplos negativos no cuentan como declaración |
| M03 | Un archivo de runtime ignorado por Git no se veía | FSY recorre el sistema de archivos real de las superficies (§8.3) |
| M04 | Un cambio en A deshecho por un commit posterior no se veía | Regla HST sobre la historia completa (§8.4) |

### 8.2 Semántica acotada de CNT y GOV

No es un detector lingüístico universal. El texto se normaliza (minúsculas, sin acentos, sin Markdown básico, guiones unificados) y se divide en oraciones y en celdas de tabla.

- **CNT.** Por familia (puntaje, recomendación, mejor candidato, selección automática, ranking nuevo, OCR o extracción, embeddings, búsqueda semántica, ML, alcance C, datos reales, producción, F36–F40, G0 real y RF-23), el gate rechaza toda oración que combine un término de la familia con un verbo o estado que intente habilitarla. Un término o un verbo no cuentan cuando una negación o prohibición aparece en las tres palabras anteriores de su mismo tramo; las comas, los dos puntos, el punto y coma, las celdas y los paréntesis cortan ese tramo. Las citas entre comillas se descartan solo cuando la oración que las rodea las rechaza o las presenta como ejemplo. Las oraciones que empiezan por «Ejemplo negativo» describen pruebas. Una fila «NB-xx» de la tabla de negativos solo describe un negativo si coincide con un caso del propio gate. El documento de B0 queda fuera porque B0F lo congela.
- **GOV.** En el estado vigente, la cabecera y las líneas añadidas, el gate localiza las declaraciones de G0 real, ADR-005, G0-SBX, F35 productiva, F35–F40, F36–F40, alcance C, datos reales, F35-SBX, F35-SBX-A, F35-SBX-B, B0 y B1 con `=`, `:`, `:=`, `==`, `->`, `→` o sin separador, y exige el valor vigente; G0-SBX además «con restricciones». Las citas no cuentan, y tampoco una declaración que una prohibición o un ejemplo introducen en su propio tramo. Las líneas añadidas pasan además por el análisis de CNT.

Límites conocidos: una afirmación redactada fuera de esos patrones, o con la negación a más de tres palabras, puede no detectarse; el prefijo «Ejemplo negativo» y las citas rechazadas son exenciones explícitas y auditables. Los controles positivos del gate (negación, prohibición, cita rechazada, ejemplo e intento) evitan falsos positivos sobre el texto legítimo.

### 8.3 Superficies del sistema de archivos

FSY recorre, sin seguir enlaces e incluidos los archivos ocultos: `app/`, `routes/`, `database/`, `config/`, `resources/`, `bootstrap/`, `public/`, `lang/`, `tests/`, `cypress/`, `docker/`, `.github/`, `ml-service/src/`, `ml-service/tests/`, `ml-service/pyproject.toml`, `artisan`, `composer.json`, `composer.lock`, `package.json`, `package-lock.json`, `docker-compose.yml`, `.dockerignore`, `phpunit.xml`, `vite.config.ts`, `docs/academico/datos-sinteticos/`, `docs/academico/g0-sandbox/` y `docs/academico/g0-evidence/`. Cada archivo debe estar en el árbol de HEAD, aunque `.gitignore` o `.git/info/exclude` lo ignoren, y ningún archivo de HEAD puede faltar.

Excepciones, todas artefactos locales generados que existen en el repositorio de trabajo:

| Excepción | Origen |
|---|---|
| `public/build/` | Salida de Vite (`npm run build`) |
| `resources/js/actions/`, `resources/js/routes/`, `resources/js/wayfinder/` | Generados por Laravel Wayfinder |
| `cypress/results/` | Resultados de Cypress |
| `ml-service/src/recruitment_ml.egg-info/` | Instalación editable del servicio ML |
| `bootstrap/cache/packages.php`, `bootstrap/cache/services.php` | Caché de Laravel |
| `__pycache__/` dentro de `ml-service/src/` y `ml-service/tests/` | Solo archivos regulares `.pyc` |

No se recorren `vendor/`, `node_modules/`, `storage/`, `.git/`, `ml-service/.venv/` ni `ml-service/artifacts/`, que quedan fuera del modelo de amenaza de B1: sus cambios no alteran el código versionado ni el dataset, y SBX-15 y SBX-16 siguen revisando el runtime.

### 8.4 Historia de F35-SBX-A

HST recorre `git rev-list --parents E..HEAD` sin filtrar por rutas, de modo que ninguna simplificación de la historia oculta commits, y compara cada commit con cada padre mediante `git diff-tree` sin detección de renombrados. Un commit normal falla si cambia contenido, modo, altas o bajas en las rutas de A; un merge, si su versión difiere de la de todos sus padres. Un cambio que otro commit deshace sigue siendo una violación. E no tiene que ser padre directo: la regla funciona en la rama de B, en `develop` y en `main`. Un repositorio superficial, un commit sin padres o un error de Git fallan cerrado.

### 8.5 RED → GREEN (10/10/2026)

Con Git real, en clones desechables sin remoto y ya eliminados:

| Caso | Gate B1 (`f30cfe6`): RED | Gate B1.1: GREEN |
|---|---|---|
| Afirmación positiva en Markdown autorizado (M01) | 29/0, PASS | FAIL en CNT |
| Estados canónicos más contradicciones en minúsculas (M02) | 29/0, PASS | FAIL en GOV |
| Archivo de `app/` oculto por `.git/info/exclude` (M03) | 29/0, PASS | FAIL en FSY |
| A modificada y restaurada por commits (M04) | 29/0, PASS | FAIL en HST |

Variantes distintas de las de la auditoría, también con Git real, todas en FAIL:
- **CNT:** puntaje automático con Markdown y mayúsculas; recomendación del mejor candidato en inglés; embeddings y búsqueda semántica.
- **GOV**, rechazadas: «**G0 real** := Aprobada», «Scope C: HABILITADO» y «ADR-005 = aceptado».
- **FSY:** archivo extra normal, oculto, anidado e ignorado por `.git/info/exclude`, ignorado por `.gitignore` en `bootstrap/cache/`, enlace en `routes/` y archivo no `.pyc` en un `__pycache__` del servicio ML.
- **HST:** borrado, cambio de modo y renombrado de A, cada uno deshecho por un commit posterior.
- **Estados no verificables:** clon superficial y `GIT_DIR` inválido, que fallan cerrados sin trazas.

Pasan, como deben, el estado limpio, las negaciones, el ejemplo negativo y la cita rechazada en Markdown, la prohibición textual en el gobierno, los artefactos locales reales dentro de sus excepciones y la integración de B1.1 en `develop` y en `main` con `merge --no-ff`.

Durante estas pruebas apareció un defecto propio de B1.1: con un estado incompleto (clon superficial o `GIT_DIR` inválido), los controles positivos detenían el gate con `KeyError` en lugar de informar. Se corrigió y ahora fallan cerrados con diagnóstico. En el gate quedan 37 negativos en memoria (NB-01..NB-18 y NB-20..NB-38), NB-19 y once controles positivos: 60 comprobaciones correctas y 0 fallas sobre HEAD, con SBX-01..SBX-18 en PASS.
