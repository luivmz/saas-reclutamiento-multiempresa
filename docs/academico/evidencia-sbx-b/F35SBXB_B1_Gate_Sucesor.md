# F35-SBX-B — B1: gate sucesor sobre HEAD

> Incremento B1 de F35-SBX-B, versión 5 (10/10/2026): la versión 1 se auditó en `f30cfe6c4adf9c3f7704b6bd665b6363a137b91a`, la versión 2 en `298c5a4dc19594980a22a877ad9d4a89f5acdf23`, la versión 3 en `bd93c69b5a6b712a0cacb17646cd593023dc187e` y la versión 4 en `ddf82c28f2cbb9b33e65969de20e7bee073e2752`; esta incorpora las correcciones B1.1 (§8), B1.2 (§9), B1.3 (§10) y B1.4 (§11). Rama `feature/f35-sbx-b-deterministic-pipeline`, creada desde `develop` `430f3f544c3542cabac8028a122c8a0c2a97390b`, que integra [B0](F35SBXB_B0_Sucesion_de_Gates.md). B1 construye solo el **mecanismo de control** que exigen DH-B04 y DH-B13 antes de cualquier pipeline: no hay pipeline funcional, SQLite, máquina de estados, informe, purga ni ML.

## 1. Qué es el gate

[`validate_f35sbxb.py`](../tools/f35sbxb/validate_f35sbxb.py) valida el **HEAD actual** de la rama de B, de `develop` o de `main`. No sustituye esa validación por los gates históricos: estos siguen congelados y se ejecutan anclados como evidencia complementaria (DH-B01, DH-B02). Solo usa la biblioteca estándar.

El gate primero **recoge** el estado real (Git, índice, sistema de archivos y documentos) y después **evalúa** reglas puras sobre ese estado. Los casos negativos mutan una copia del estado en memoria; la detección real de flags, enlaces y archivos ocultos se demuestra además con Git real en clones desechables (§7).

## 2. Comprobaciones

| ID | Qué comprueba | Origen |
|---|---|---|
| CTX | Rama `feature/f35-sbx-b-deterministic-pipeline`, `develop` o `main`; HEAD no separado; E, el cierre de B0 y la base de B como ancestros de HEAD; intérprete aislado (`python -I`, al que el gate se relanza solo) y sin `PYTHONPATH`, `PYTHONHOME` ni `PYTHONUSERBASE` (§11.2) | Plan B1 §4.A y §4.J; DH-B04; B1.4 |
| AIN | F35-SBX-A idéntica a E: 22 archivos con los bytes reales del blob de E, sin archivos extra ni enlaces; árbol de HEAD sin cambios frente a E en esas rutas | DH-B09 |
| HST | Historia completa de E a HEAD: el gate rechaza todo commit que haya tocado F35-SBX-A (contenido, modo, altas, bajas o renombrados), aunque después se restaure; en un merge cuenta lo que difiere de todos sus padres. Un repositorio superficial o una historia ilegible fallan cerrado | B1.1 M04; DH-B09 |
| B0F | El documento de B0 idéntico a su cierre auditado | B0 CERRADA |
| SBX | SBX-01..SBX-18 recalculados uno por uno sobre HEAD (§4) | DH-B13 |
| GOV | Los trece estados de gobierno exactos en `CLAUDE.md` y `docs/PROGRESS.md`; F35-SBX-B solo INICIADA. En el estado vigente, la cabecera y las líneas añadidas, el gate rechaza toda declaración de estado contradictoria para G0 real, ADR-005, G0-SBX, F35 productiva, F36–F40, alcance C, datos reales, F35-SBX-A/B, B0 y B1, en cualquier forma (mayúsculas, Markdown, `=`, `:`, `:=`, `->`), con verbo copulativo o con verbo finito sobre la entidad, y rechaza también la declaración de G0-SBX sin restricciones (§10.2); las citas y las prohibiciones no cuentan como declaración | DH-B11; B1.1 M02; B1.3 |
| SCP | Delta exacto respecto de la base de B (árbol de HEAD, árbol de trabajo, índice y archivos sin seguimiento): solo las rutas autorizadas, con el estado esperado, y las obligatorias presentes | DH-B03; plan B1 §4.F y §4.K |
| FSY | Recorrido real de `evidencia-sbx-b/`, `tools/f35sbxb/` y de las superficies del runtime, el dataset y la evidencia (§8.3): todo archivo debe coincidir byte a byte con su blob en la base autorizada `430f3f5` aunque Git lo ignore, ningún archivo de la base puede faltar y no se admiten enlaces; un `.pyc` solo se admite si es derivable de su fuente, y las únicas excepciones son los directorios de metadatos de §10.3 | Plan B1 §4.I; B1.1 M03; B1.2; B1.3 |
| FLG | Ningún flag del índice en todo el repositorio: solo `H` en `git ls-files -v` (`h` = assume-unchanged, `S` = skip-worktree, `s` = ambos) | Plan B1 §4.I |
| CNT | Archivos de B: UTF-8 sin NUL, CR ni BOM; sin correos, DNI, teléfonos ni RUC; solo `.md`, `.json` y `.py`; claves JSON sin vocabulario de capacidades prohibidas; y, en los documentos mutables de B, el gate rechaza toda afirmación positiva que habilite una capacidad prohibida (§8.2) y toda declaración de estado contradictoria con el gobierno vigente (§10.2) | Plan B1 §7; B1.1 M01; B1.3 |
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
- Desde B1.3 (§10.4) verifica también, antes de ejecutar nada, que los directorios que esos módulos ponen en `sys.path` (`tools/f34`, `tools/f34a`, `tools/f34b` y `tools/f34e`) contienen exactamente lo de E, incluido `generate_synthetic.py`, que `validate_f34.py` importa. Ninguna ruta del repositorio queda en `sys.path` y ningún `.pyc` sustituye a una fuente verificada.
- Desde B1.4 (§11) no ejecuta ningún código del repositorio antes de verificarlo. Usa un inventario cerrado de todo lo que `compute_sbx()` puede ejecutar, incluido el `schema.py` del servicio RF-29, comparado con el blob de su referencia; recalcula el grafo por AST sin importar; y una guarda sirve solo los bytes verificados.
- Ejecuta solo `compute_sbx()`, sin generar ni reutilizar bytecode, y exige exactamente SBX-01..SBX-18.
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
| NB-39 | CNT | acción de puntuar candidatos |
| NB-40 | CNT | recomendación automática del candidato más apto |
| NB-41 | CNT | selección final predicada como automática |
| NB-42 | CNT | el sistema selecciona al candidato ganador |
| NB-43 | CNT | el motor decide automáticamente |
| NB-44 | CNT | RF-23 decidido automáticamente |
| NB-45 | CNT | inglés: ranking automático de candidatos |
| NB-46 | CNT | el motor elige a los mejores postulantes |
| NB-47 | CNT | contratación predicada como automática |
| NB-48 | GOV | ADR-005 queda APROBADA |
| NB-49 | GOV | ADR-005 fue o está APROBADA |
| NB-50 | GOV | alcance C pasa a HABILITADO |
| NB-51 | GOV | F35 productiva no está BLOQUEADA |
| NB-52 | GOV | datos reales están permitidos |
| NB-53 | FSY | código no autorizado dentro de una excepción de FSY |
| NB-54 | CNT | primera persona del futuro: asignaremos una calificación automática |
| NB-55 | CNT | inglés: ranking automático de candidatos habilitado |
| NB-56 | CNT | futuro: el motor priorizará automáticamente candidatos |
| NB-57 | CNT | la decisión final la tomará el sistema |
| NB-58 | CNT | inglés: el sistema elige al postulante final |
| NB-59 | CNT | el sistema realizará la selección final |
| NB-60 | CNT | la plataforma escoge al ganador sin intervención humana |
| NB-61 | CNT | variante: el algoritmo efectuará la contratación final |
| NB-62 | CNT | variante: el sistema selecciona y el Aprobador solo recibe aviso |
| NB-63 | GOV | verbo antes de la entidad: se aprueba ADR-005 |
| NB-64 | GOV | primera persona: aprobamos ADR-005 |
| NB-65 | GOV | ADR-005 ha sido aprobada |
| NB-66 | GOV | G0-SBX queda sin restricciones |
| NB-67 | GOV | se eliminan las restricciones de G0-SBX |
| NB-68 | GOV | G0-SBX queda plenamente habilitada |
| NB-69 | CNT | Markdown de B: se aprobó ADR-005 |
| NB-70 | FSY | bundle de Vite no versionado aunque el manifiesto lo nombre |
| NB-71 | FSY | TypeScript de Wayfinder no versionado |
| NB-72 | FSY | caché PHP de Laravel no versionada |
| NB-73 | FSY | archivo del runtime con bytes distintos de la base autorizada |
| NB-74 | SBX | Archivo ajeno en una ruta de importación de `compute_sbx()`: no se importa |
| NB-75 | SBX | `generate_synthetic.py` alterado: no se importa |
| NB-76 | FSY | `.pyc` distinto de su fuente: no se certifica |
| NB-77 | FSY | `.pyc` reescrito por pytest: no se certifica |
| NB-78 | SBX | `schema.py` alterado: no se ejecuta y el marcador no aparece |
| NB-79 | SBX | `f35sbx_scope.py` alterado: no se ejecuta y el marcador no aparece |
| NB-80 | SBX | Módulo plantado que sombrearía una importación de `compute_sbx()`: no se ejecuta nada |
| NB-81 | SBX | Ejecución dinámica en el grafo estático: no verificable |
| NB-82 | SBX | Módulo del repositorio ya cargado: no se acepta |
| NB-83 | SBX | La guarda rechaza código del repositorio no verificado antes de ejecutarlo |
| NB-84 | CTX | intérprete no aislado o con PYTHONPATH |
| NB-85 | CNT | el sistema asigna notas automáticamente a los postulantes |
| NB-86 | CNT | inglés: candidatos ordenados automáticamente para la selección |
| NB-87 | CNT | el motor sugiere qué candidato debe avanzar |
| NB-88 | CNT | el sistema calcula la calificación de cada candidato |
| NB-89 | CNT | el sistema determina al seleccionado sin decir automático |
| NB-90 | CNT | la plataforma decide quién obtiene la plaza |
| NB-91 | CNT | inglés: el motor determina al postulante elegido |
| NB-92 | GOV | ADR-005 recibe aprobación |
| NB-93 | GOV | tiempo compuesto: hemos aprobado ADR-005 |
| NB-94 | GOV | G0-SBX ya no tiene restricciones |
| NB-95 | GOV | G0-SBX deja de tener restricciones |

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

Las excepciones de B1.1 eran directorios ignorados; B1.2 las sustituye por excepciones validadas (§9.3).

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

## 9. Corrección B1.2

La segunda auditoría independiente (`298c5a4`) dio por resueltos M04 (HST), el fallo cerrado, el LOW de negaciones en GOV, SBX-01..SBX-18 y la integridad de A, y dejó tres clases residuales. B1.2 corrige solo esas clases, no las frases concretas del auditor. El gate sigue en desarrollo, pendiente de reauditoría final: no está congelado.

### 9.1 M01 residual: acciones inequívocas

CNT añade tres reglas a la de término y verbo:

- **Acción sobre personas candidatas.** Formas verbales explícitas de puntuación, recomendación, elección, selección, descarte, contratación y ordenamiento, en español y en inglés, con una persona candidata en la oración (candidato, postulante, aspirante, ganador, más apto, mejor). Las de calificación, clasificación, evaluación y ordenamiento exigen además «automático». Las formas son explícitas para que los sustantivos (ranking, puntuación, identificador, determinista) no cuenten.
- **Decisión automática.** Las formas de decisión, determinación o resolución junto a «automáticamente».
- **Estado predicativo.** La selección, la decisión, la contratación, la recomendación o el puntaje predicados como automáticos; el gate rechaza, por ejemplo, «la selección final será automática».

Una negación en las tres palabras anteriores, o una prohibición no negada más adelante en el mismo tramo («puntuar candidatos está prohibido»), deja la oración como prohibición. Con los patrones explícitos de RF-23 el gate también rechaza «RF-23 será decidido automáticamente por el motor». Las comillas simples y los prefijos «Bypass reproducido» y «Ataque» se tratan igual que las citas y el prefijo «Ejemplo negativo».

### 9.2 M02 residual: declaraciones directas

GOV reconoce también las declaraciones con verbo copulativo (queda, quedó, fue, está, pasa a, se declara, permanece, sigue, resulta, es y sus equivalentes en inglés) para todas las entidades protegidas. Negar un estado positivo es coherente con un estado restrictivo («ADR-005 no está APROBADA»); negar un estado restrictivo es una contradicción («F35 productiva no está BLOQUEADA»). Las citas, las prohibiciones y los ejemplos siguen sin contar como declaración.

### 9.3 M03 residual: excepciones validadas

Por defecto se deniega todo. Una excepción ya no significa ignorar un directorio: el gate lo recorre y cada archivo debe cumplir un patrón estrecho, sin enlaces ni objetos especiales.

| Excepción | Patrón admitido | Origen |
|---|---|---|
| `public/build/` | `manifest.json`, `fonts-manifest.json` y `assets/<nombre>-<hash de 8>.{js,css,woff,woff2}` | Salida de Vite |
| `resources/js/actions/`, `resources/js/routes/`, `resources/js/wayfinder/` | Solo archivos `.ts` | Laravel Wayfinder |
| `cypress/results/` | Solo `.json` y `.log` en el primer nivel | Resultados de Cypress |
| `ml-service/src/recruitment_ml.egg-info/` | Solo `PKG-INFO`, `SOURCES.txt`, `dependency_links.txt`, `top_level.txt` y `requires.txt` | Instalación editable del servicio ML |
| `bootstrap/cache/packages.php`, `bootstrap/cache/services.php` | Solo un arreglo PHP literal (`<?php return array (...);` con cadenas, números y `=>`), sin variables, llamadas ni funciones | Caché de Laravel |
| `__pycache__/` dentro de `ml-service/src/` y `ml-service/tests/` | Solo archivos regulares `.pyc`, sin subdirectorios | Bytecode de Python |

Los artefactos reales del repositorio de trabajo cumplen estos patrones. Cualquier otro archivo de `bootstrap/cache/` sigue siendo un extra frente al árbol de HEAD. B1.3 sustituye esta tabla (§10.3).

### 9.4 RED → GREEN (10/10/2026)

Con Git real, en clones desechables sin remoto y ya eliminados, el mismo conjunto de casos contra el gate de `298c5a4` (RED) y contra el gate corregido (GREEN):

| Caso | RED | GREEN |
|---|---|---|
| M01: las cuatro frases de la auditoría y tres variantes nuevas (elección del postulante idóneo, contratación del mejor postulante en inglés y ordenamiento automático de aspirantes) | Pasaban | FAIL en CNT |
| RF-23: se rechaza «el motor decide automáticamente la selección final» | Pasaba | FAIL en CNT |
| M02: ADR-005 con «queda», «fue», «está» y «pasa a» APROBADA | Pasaban | FAIL en GOV |
| M03: PHP en `public/build/` y en `public/build/assets/` con nombre de hash, archivo inesperado en `public/build/`, `services.php` con código, enlace en `public/build/`, código en el `egg-info`, PHP en Wayfinder | Pasaban | FAIL en FSY |

También se rechazan, ya antes y ahora, «G0 real se declara APROBADA», «F36–F40 quedan INICIADAS», un archivo nuevo en `bootstrap/cache/`, un archivo de `app/` ignorado u oculto y un `__pycache__` con subdirectorios.

Pasan en los dos casos: el estado limpio, la negación, el ejemplo negativo, la selección final bajo decisión humana, el rechazo citado, «ADR-005 permanece PROPUESTA», «ADR-005 no está APROBADA», el rechazo de una declaración y los artefactos locales que cumplen sus patrones, con copias reales de `bootstrap/cache/`.

Regresión de lo ya resuelto: A modificada y restaurada por commits sigue fallando en HST, la prohibición textual sigue pasando en GOV y el clon superficial y `GIT_DIR` inválido siguen fallando cerrados sin trazas. En el gate quedan 52 negativos en memoria (NB-01..NB-18 y NB-20..NB-53), NB-19 y diecinueve controles positivos: 83 comprobaciones correctas y 0 fallas sobre HEAD, con SBX-01..SBX-18 en PASS.

Límites que se mantienen: la semántica sigue acotada a patrones explícitos y documentados; una afirmación redactada fuera de ellos puede no detectarse. Dentro de cada excepción se valida la forma de los archivos, no el contenido de los artefactos de Vite, Wayfinder o Cypress.

## 10. Corrección B1.3

La tercera auditoría independiente (`bd93c69`) dejó tres clases residuales y un falso positivo LOW:

- **M01 y RF-23:** afirmaciones con formas verbales fuera de las explícitas, con la decisión como objeto directo o con capacidades nombradas como automáticas.
- **M02:** declaraciones por verbo finito sobre la entidad y sobre las restricciones de G0-SBX.
- **M03:** código ejecutable admitido por su nombre o su extensión.
- **Falso positivo LOW:** la selección manual del Aprobador con confirmación humana.

B1.3 corrige las clases, no frases sueltas. El gate sigue en desarrollo, pendiente de reauditoría final: no está congelado.

### 10.1 M01 y RF-23: conjugación, objeto de decisión y agente

- **Conjugación por clase.** Las formas verbales se generan por clase: presente, pretérito, futuro, primera persona del plural, condicional, gerundio y participio. Cubren las familias de puntuación, calificación, clasificación, recomendación, elección, selección, descarte, contratación, ordenamiento y priorización, y sus equivalentes en inglés. Las formas que coinciden con sustantivos del dominio («descarte», «contrato») siguen excluidas.
- **La decisión como objeto directo.** Cuenta tomar, adoptar, emitir, realizar, efectuar o ejecutar la selección, la decisión o la contratación, también con pronombre («la decisión final la tomará»). Exige que la oración tenga «automático» o un agente de sistema (sistema, motor, plataforma, algoritmo, modelo, IA o sus equivalentes en inglés). Por eso el gate rechaza «el sistema realizará la selección final».
- **Capacidad nombrada como automática.** Cuenta en cualquier orden, con hasta dos palabras intermedias que no sean negaciones, cuando un verbo la habilita. Por eso el gate rechaza «automatic final candidate selection is enabled».
- **Agente humano.** Una acción no cuenta si la ejecuta una persona:
  - un agente humano no negado antes del verbo (Aprobador, Dirección, comité, evaluador o reclutador);
  - ese agente introducido después con «por»;
  - «manualmente» en el mismo tramo.

  Ese agente nunca exime si la oración tiene «automático» o un agente de sistema que no sea instrumental («con apoyo del sistema» sí es instrumental). Tampoco exime el contexto humano situado en otro lugar: el gate rechaza «la plataforma escogerá al ganador sin intervención humana».

Así deja de fallar «El Aprobador seleccionará manualmente al candidato, con confirmación humana.».

### 10.2 M02: verbo finito sobre la entidad y G0-SBX

- **Cópulas compuestas y adverbios.** GOV reconoce «ha sido», «ha quedado» y «has been», y un adverbio entre la cópula y el valor. El gate rechaza «ADR-005 ha sido aprobada».
- **Verbo finito sobre la entidad.** Cuenta en los dos órdenes, y el verbo se traduce al estado equivalente: aprobar, habilitar, desbloquear, autorizar, activar, iniciar, aceptar, permitir, cerrar, congelar, implementar, bloquear o prohibir. Ese estado se compara con los valores admitidos para la entidad. El gate rechaza «se aprueba ADR-005» y «aprobamos ADR-005». No cuentan el infinitivo ni el subjuntivo, ni la negación de un estado positivo («no se aprueba» sigue siendo coherente).
- **G0-SBX solo admite APROBADA CON RESTRICCIONES.** El gate rechaza que se declare sin restricciones, irrestricta o plenamente habilitada, y que se eliminen o se levanten sus restricciones, en cualquier orden. Un marcador cuenta si ninguna negación lo precede desde la mención de la entidad. Negar el estado irrestricto es coherente.
- **CNT.** Aplica estas mismas declaraciones de estado al Markdown mutable de B. El documento de B0 queda fuera, porque B0F ya lo compara con su cierre.

### 10.3 M03: metadatos no son código ejecutable

Ningún archivo se certifica por su nombre ni por su extensión. Todo código ejecutable o importable de las superficies que recorre FSY queda en uno de tres casos:

| Artefacto | Caso | Motivo |
|---|---|---|
| Archivos del runtime, el dataset y la evidencia | (A) Bytes reales idénticos a su blob en la base autorizada `430f3f5` | Congelados frente a una referencia que ya existe; no se crea ninguna baseline nueva |
| `.pyc` en `ml-service/src/`, `ml-service/tests/`, `tools/f35sbx/` y `tools/f35sbxb/` | (B) Solo si su código coincide con el que `compile()` produce desde la fuente hermana, con la etiqueta del intérprete que ejecuta el gate | Derivable y verificable; si se reescribió con pytest, viene de otra versión de Python o no tiene fuente, falla cerrado |
| `public/build/`: bundles y manifiestos de Vite | (C) Fuera del conjunto permitido en B1 | No están versionados ni en la base ni en HEAD, y no se derivan sin un build; un manifiesto no autoriza un bundle |
| `resources/js/actions/`, `resources/js/routes/` y `resources/js/wayfinder/` | (C) | TypeScript importable que genera Wayfinder, sin versionar |
| `bootstrap/cache/packages.php` y `bootstrap/cache/services.php` | (C) | PHP que Laravel ejecuta; la gramática de B1.2 probaba su forma, no su origen |
| `cypress/results/` y `ml-service/src/recruitment_ml.egg-info/` | Excepción de metadatos, con su patrón estrecho | Nada los ejecuta ni los importa |

Consecuencia operativa: el gate se ejecuta sobre un checkout sin artefactos generados, como un clon limpio. Un árbol de trabajo con build de Vite, Wayfinder, la caché de Laravel o `.pyc` de pytest falla en FSY, y el diagnóstico los enumera. Ni B1.3 ni el gate borran esos artefactos. No se ejecutó ningún build ni se añadió ninguna dependencia: `importlib.machinery` es de la biblioteca estándar y entra en `importlib`, ya autorizado.

### 10.4 Código que ejecuta el propio gate (DH-B13)

Al revisar M03 apareció la misma clase dentro del gate. `validate_f34.py` importa `generate_synthetic.py` y módulos estándar mediante `sys.path`. Además, un `.pyc` de `__pycache__` cuya cabecera coincidiera con su fuente podía sustituir a la fuente verificada.

El gate ahora:

1. retira de `sys.path` las rutas del repositorio antes de cualquier otra importación;
2. apunta `sys.pycache_prefix` debajo de un archivo regular, de modo que ningún `.pyc` se reutiliza;
3. exige, antes de ejecutar nada, que `tools/f34`, `tools/f34a`, `tools/f34b` y `tools/f34e` contengan exactamente lo de E con los mismos bytes, más un `__pycache__` opcional con `.pyc` derivables.

### 10.5 RED → GREEN (10/10/2026)

Se ejecutó con Git real, en clones desechables sin remoto y ya eliminados. El mismo guion corrió contra el gate de `bd93c69` (RED) y contra el gate corregido (GREEN):

| Caso | RED | GREEN |
|---|---|---|
| M01 y RF-23: las catorce frases de la auditoría | Siete pasaban; las otras siete ya fallaban | FAIL en CNT |
| M01 y RF-23: seis variantes propias (futuro de primera persona, participio, inglés, contratación final, selección por el sistema con aviso al Aprobador y priorización automatizada) | Cinco pasaban y una ya fallaba | FAIL en CNT |
| M01: los nueve textos legítimos, incluida la selección manual del Aprobador | Fallaban dos: la selección manual del Aprobador y la elección de la Dirección | PASS |
| M02: seis formas de aprobar ADR-005, el rechazo de cinco formas de G0-SBX sin restricciones, el levantamiento de restricciones y el verbo después de la entidad | Diez pasaban; ya fallaban «queda», «pasa a» y «aprobada sin restricciones» | FAIL en GOV |
| M02: los nueve textos legítimos | Ocho pasaban; se rechazaba por error la negación del estado irrestricto de G0-SBX | PASS |
| M02 en el Markdown de B: se rechaza «Se aprobó ADR-005» | Pasaba | FAIL en CNT |
| M03: bundle de Vite con su manifiesto, TypeScript de Wayfinder, copias reales de la caché de Laravel, `.pyc` con código distinto de su fuente y `.pyc` con nombre de pytest | Pasaban | FAIL en FSY |
| M03: `.pyc` derivable de su fuente con `py_compile` | Pasaba | PASS |
| DH-B13: `csv.py` plantado e ignorado en `tools/f34/` | PASS (83/0) después de ejecutar el código plantado | FAIL en SBX, sin ejecutarse |
| DH-B13: `.pyc` plantado con la cabecera de `validate_f34.py` | PASS (83/0) después de ejecutar el código plantado | FAIL en SBX, sin ejecutarse |

Regresión de lo ya resuelto, igual en RED y en GREEN: A modificada y restaurada por commits falla en HST; `public/build/*.php`, un archivo de `app/` ignorado y código en el `egg-info` fallan en FSY; la prohibición textual pasa en GOV y en CNT; el clon superficial y `GIT_DIR` inválido fallan cerrados sin trazas. En el gate quedan 72 negativos en memoria (NB-01..NB-18 y NB-20..NB-73), NB-19, NB-74..NB-77, un control positivo de `.pyc` derivable y treinta y tres controles positivos de texto: 122 comprobaciones correctas y 0 fallas sobre un clon limpio de HEAD, con SBX-01..SBX-18 en PASS. Sobre un árbol de trabajo con artefactos generados, el gate falla en FSY (§10.3).

Límites LOW que se mantienen:

- La semántica sigue acotada a patrones explícitos y documentados: una afirmación redactada fuera de ellos puede no detectarse.
- Una prohibición situada más de tres palabras antes del verbo, sin coma intermedia, no se reconoce, y la oración cuenta como afirmación. Es un falso positivo conservador.
- El gate rechaza también una selección en voz pasiva sin agente («se seleccionará al candidato») aunque no diga «automático». Es un falso positivo conservador.
- La verificación de un `.pyc` deserializa su código con el cargador estándar, sin ejecutarlo. Un `.pyc` malformado hace fallar el gate, nunca pasar.
- En las dos excepciones de metadatos se valida la forma de los archivos, no su contenido.

## 11. Corrección B1.4

La cuarta auditoría independiente (`ddf82c2`) dejó un HIGH y tres MEDIUM:

- **H01 (DH-B13):** un `ml-service/src/recruitment_ml/schema.py` alterado se ejecutaba antes de que el gate fallara.
- **M01:** puntuación, ordenamiento y recomendación residuales.
- **M02:** RF-23 residual.
- **M03:** gobierno residual de ADR-005 y G0-SBX.

B1.4 corrige la clase de H01, no solo `schema.py`, y las tres familias semánticas. El gate sigue en desarrollo, pendiente de reauditoría final: no está congelado.

### 11.1 Inventario del código ejecutable

El inventario se construyó sin importar nada del repositorio: primero por lectura estática y después con una traza de las cargas de `compute_sbx()` sobre el árbol legítimo.

| Archivo | Cómo se ejecuta | Referencia autorizada |
|---|---|---|
| `tools/f34e/validate_f34e.py` | Punto de entrada de `compute_sbx()`; `validate_f34b.py` también lo carga por ruta | E |
| `tools/f34/validate_f34.py` | `load_module` de `validate_f34e.py` | E |
| `tools/f34/generate_synthetic.py` | `import` de `validate_f34.py` desde su directorio | E |
| `tools/f34a/validate_f34a.py` | `load_module` de `validate_f34e.py` | E |
| `tools/f34b/validate_f34b.py` | `load_module` de `validate_f34e.py` | E |
| `tools/f35sbx/f35sbx_scope.py` | Carga por ruta en `validate_f34b.py` e `import` en `validate_f34.py` | E |
| `ml-service/src/recruitment_ml/schema.py` | Carga por ruta, a nivel de módulo, en `validate_f34.py` (contrato RF-29) | Base de B `430f3f5` |

No hay otras cargas: los siete módulos solo usan la biblioteca estándar, no tienen `exec`, `eval` ni importaciones dinámicas, y sus subprocesos son exclusivamente `git`. `schema.py` se carga sin su paquete, por lo que `recruitment_ml/__init__.py` no se ejecuta.

### 11.2 Verificación antes de ejecutar

1. **Aislamiento del intérprete.** Si no se invoca con `python -I`, el gate se relanza a sí mismo aislado con `os.spawnv` antes de importar nada más, y devuelve su código de salida. CTX falla si están definidas `PYTHONPATH`, `PYTHONHOME` o `PYTHONUSERBASE`.
2. **Bytes autorizados.** Cada archivo del inventario debe ser un archivo regular, sin enlaces en su ruta, y con los bytes del blob 100644 de su referencia.
3. **Grafo estático.** El grafo se recalcula por AST sobre esos bytes, sin importarlos, resolviendo las rutas de `spec_from_file_location`, de `load_module` y de `sys.path`. Fallan cerrados:
   - una carga no resoluble;
   - un nombre importado que exista como módulo del repositorio en un directorio de `sys.path` (`.py`, `.pyc`, `.pyd` o paquete) y no esté en el inventario;
   - la ejecución dinámica;
   - un subproceso que no sea `git`.

   El grafo debe coincidir exactamente con el inventario.
4. **Módulos ya cargados.** Si en `sys.modules` ya hay un módulo cuyo origen está en el repositorio, el gate falla sin ejecutar.
5. **Guarda durante `compute_sbx()`.** El código del repositorio se sirve desde los bytes ya verificados en memoria: la verificación y la ejecución usan el mismo objeto, sin releer el archivo. La guarda rechaza cualquier otra fuente del repositorio, un `.pyc` sin fuente, una extensión nativa o un paquete, y el bytecode del repositorio nunca se reutiliza. Un rechazo hace fallar SBX aunque el validador lo capture. Al salir, la guarda restaura `sys.path`, `sys.modules` y los cargadores.

La guarda no es un sandbox de procesos: no protege frente a otro proceso que modifique los archivos de datos mientras el gate corre, ni frente a código que el intérprete ejecute antes del gate.

### 11.3 M01, RF-23 y M02

- **Puntuación.** El gate rechaza la asignación o el otorgamiento de notas, calificaciones o puntajes a personas candidatas por el sistema o con «automático». La misma tarea de un evaluador no cuenta.
- **Ordenamiento.** El gate rechaza el ordenamiento, la clasificación o la priorización de personas candidatas con «automático», o por el sistema con una finalidad decisional («para la selección»). «El ranking calcula, ordena y compara» sigue pasando.
- **Recomendación.** El gate rechaza la sugerencia o la recomendación, por el sistema, de quién continúa.
- **RF-23 sin «automático».** El gate rechaza la decisión, la determinación, la elección o la selección de una persona candidata, de «quién» o de la plaza cuando el agente es el sistema.
- **Agente de la acción.** Es el agente responsable más cercano antes del verbo; si no hay, uno pospuesto (el sistema, o una persona introducida por «por»). «El sistema muestra el ranking y el Aprobador elige al candidato» deja de rechazarse por error, y una acción del sistema nunca queda eximida.
- **ADR-005.** Cuentan los tiempos compuestos con «haber» y la aprobación recibida, obtenida o concedida por una entidad restrictiva. Las negaciones y la aprobación solo requerida siguen siendo coherentes. El gate rechaza «hemos aprobado ADR-005» y «ADR-005 recibe aprobación».
- **G0-SBX.** Cuentan «ya no tiene restricciones», «deja de tener restricciones», «no longer has restrictions» y «has no restrictions», aunque contengan «no». La protección solo la da una negación anterior a esa construcción. El gate rechaza «G0-SBX ya no tiene restricciones».

### 11.4 RED → GREEN (10/10/2026)

Se ejecutó con Git real, en clones desechables sin remoto y ya eliminados. El mismo guion corrió contra el gate de `ddf82c2` (RED) y contra el gate corregido (GREEN). Cada carga útil intenta crear un archivo marcador fuera del clon, y el guion comprueba si aparece.

| Caso | RED (`ddf82c2`) | GREEN |
|---|---|---|
| H01: `schema.py` con la carga útil al final del módulo | Aparecía el marcador: el código se ejecutaba antes de que el gate fallara | FAIL en SBX, FSY y SCP, sin marcador |
| H01: `f35sbx_scope.py`, `generate_synthetic.py` y `validate_f34a.py` alterados | FAIL sin marcador (`compute_sbx()` no carga `f35sbx_scope.py`; B1.3 ya protegía los otros dos) | FAIL, también en SBX, sin marcador |
| Secuestro de importaciones con archivos plantados (ver la lista debajo) | FAIL sin marcador | FAIL sin marcador |
| Secuestro: `PYTHONPATH` externo con `json.py`, `hashlib.py`, `re.py` y `csv.py` | Aparecía el marcador y el gate terminaba sin informe | FAIL en CTX, sin marcador |
| Secuestro: `PYTHONPATH` externo con `sitecustomize.py` | El intérprete lo ejecutaba al arrancar y el gate daba PASS (122/0) | El intérprete lo sigue ejecutando antes que el gate, pero el gate da FAIL en CTX |
| M01: dos frases de la auditoría y seis variantes | Seis pasaban | FAIL en CNT |
| M01: seis textos legítimos | Se rechazaba por error la elección del Aprobador tras una mención del sistema | PASS |
| RF-23: tres frases de la auditoría y cuatro variantes | Pasaban todas | FAIL en CNT |
| RF-23: seis textos legítimos | Pasaban | PASS |
| M02: tres frases de la auditoría y siete variantes | Ocho pasaban | FAIL en GOV |
| M02: diez textos legítimos | Pasaban | PASS |

Los archivos plantados del tercer caso son:

- `csv.py`, `json.py`, `hashlib.py` y `pathlib.py` en `tools/f34/`;
- `csv.py` en `tools/f35sbx/` y `json.py` junto al gate;
- `PYTHONPATH=tools/f34`, y el directorio de trabajo en `tools/f34`;
- un `.pyc` malicioso con la cabecera de `validate_f34.py` o de `schema.py`;
- un `.pyc` sin fuente.

Regresión, igual en RED y en GREEN:

- el bundle de Vite, Wayfinder, la caché de Laravel y un archivo de `app/` ignorado fallan en FSY;
- el `.pyc` derivable pasa;
- A modificada y restaurada por commits falla en HST;
- el clon superficial y `GIT_DIR` inválido fallan cerrados sin trazas.

Durante el primer GREEN apareció una regresión propia: con Git no verificable, el caso NB-81 detenía el gate con una traza. Se corrigió antes del commit, y ahora los casos de integridad fallan cerrados con diagnóstico.

En el gate quedan:

- 84 negativos en memoria: NB-01..NB-18, NB-20..NB-73 y NB-84..NB-95;
- doce casos de integridad: NB-19, NB-74..NB-83 y el `.pyc` derivable;
- cuarenta y cuatro controles positivos de texto.

Sobre un clon limpio de HEAD dan 151 comprobaciones correctas y 0 fallas, con SBX-01..SBX-18 en PASS. Sobre un árbol de trabajo con artefactos generados, el gate sigue fallando en FSY (§10.3), sin ejecutar código no verificado.

Límites LOW que se mantienen:

- **Código que el intérprete ejecuta antes del gate.** Un `sitecustomize.py` en `PYTHONPATH` o el sitio de Python fuera del repositorio quedan fuera de su alcance. El gate falla si `PYTHONPATH` está definida, y la invocación recomendada es `python -I`.
- **No es un sandbox de procesos.** Los archivos de datos (CSV y Markdown) se verifican al recoger el estado y se leen después: otro proceso concurrente podría cambiarlos entre ambos momentos.
- **Análisis estático acotado.** El análisis del grafo solo resuelve literales y `os.path.*`. Cualquier otra construcción falla cerrada, aunque fuera inocua.
- **Agente de la acción.** Se determina por proximidad dentro de la oración, así que una oración con varias cláusulas puede atribuirlo mal. Ante la duda, la oración se trata como afirmación.
- **Límites de B1.3.** Siguen los de §10.5: la prohibición alejada del verbo y la voz pasiva sin agente son falsos positivos conservadores.
