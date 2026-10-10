# F35-SBX-B — B0: sucesión de gates

> Subfase B0 de F35-SBX-B, versión 1 (09/10/2026). Base: `develop` `8054fedf02f1b91ab6b6baa45c743725166af1a6`, que integra el cierre de F35-SBX-A con su commit E `61f94e23fc30b00a848a4558830b6d65f81dff87`. **Solo documentación**: B0 no crea pipeline, runner, almacenamiento SQLite, fixtures, modelos ni dependencias. Estado: **B0 IMPLEMENTADA, PENDIENTE DE AUDITORÍA. F35-SBX-B NO INICIADA.**

## 1. Problema

Los validadores de las fases cerradas son *gates de alcance* de su propia fase: comparan el repositorio con su ancla y solo admiten las rutas, ramas y textos de gobierno que esa fase autorizó. El commit E congeló además los artefactos de F35-SBX-A, sin excepciones. Antes de B0 se comprobó con Git real, en clones desechables, que cualquier avance de B los hace fallar:

| Situación | Validadores que fallan | Causa |
|---|---|---|
| Rama nueva sin ningún cambio | `validate_f34b.py`, `validate_f34e.py`, `validate_f35sbx.py` | La excepción de F35-SBX-A para f30/f33/f34 solo vale en su rama, en `develop` o en `main` |
| Carpetas nuevas de B, también en `develop` | Los mismos tres | Rutas fuera de las listas de F34B/F34E y del alcance de F35-SBX-A |
| Registro de «F35-SBX-B INICIADA» en el gobierno | `validate_f30.py`, `validate_f33.py`, `validate_f34.py`, `validate_f34b.py`, `validate_f34e.py`, `validate_f35sbx.py` | Gobierno distinto del texto exacto que admitían |

Adaptar esos validadores reabriría el congelamiento auditado de A (su regla de historia rechaza cualquier commit posterior a E sobre el adaptador). B0 resuelve el conflicto sin modificarlos.

## 2. Decisión: gates históricos anclados y gate sucesor sobre HEAD

| Tipo | Qué es | Dónde se ejecuta | Qué demuestra |
|---|---|---|---|
| **Gate histórico** | `validate_f30.py`, `validate_f33.py`, `validate_f34.py`, `validate_f34b.py`, `validate_f34e.py`, `validate_f35sbx.py`, congelados | En un clon o worktree aislado, sobre su contexto de cierre compatible (§2.1) | Solo que el estado histórico auditado sigue verde |
| **Gate sucesor** | Validador de F35-SBX-B, a implementar en B | Sobre HEAD de la rama de B, de `develop` y de `main` | La validez del estado actual |
| **Validadores vigentes** | `validate.py`, `validate.py --cierre-f29`, `validate_f29.py`, `test_f32_safety.py`, `validate_f34a.py` | Sobre HEAD | Lo que ya comprobaban; si alguno fallara por diseño histórico, su reclasificación exige una decisión documentada |

### 2.1 Contexto de cierre compatible

Los gates de F35-SBX-A dependen del nombre de la rama, y `validate_f34a.py` necesita la referencia `develop`. Por eso un worktree con HEAD separado no basta: la ejecución anclada usa un clon temporal sin remoto, con `main` en el último commit de integración que los dejó verdes (`d63d094fb6f0eb335fee8d1766d33905004a1678`) y `develop` en `8054fedf02f1b91ab6b6baa45c743725166af1a6`, ejecuta los seis gates históricos y borra el clon. Nunca toca las ramas reales.

### 2.2 Principios

- **A.** Un PASS histórico solo demuestra el estado histórico correspondiente.
- **B.** Un PASS histórico nunca prueba que HEAD sea válido.
- **C.** El gate sucesor valida efectivamente HEAD, en todo lo que lista §3.
- **D.** Las excepciones son exactas: rutas o reglas concretas, nunca carpetas completas cuando se pueda evitar.
- **E.** F35-SBX-A permanece congelada: no se modifican `docs/academico/evidencia-sbx/**` ni `docs/academico/tools/f35sbx/**`.
- **F.** Los validadores históricos no son una dependencia mutable de B. Si B reutiliza alguna ayuda suya, primero verifica la integridad del archivo contra E y prefiere lógica propia, pequeña e independiente.

## 3. Requisitos del gate sucesor

A implementar en B, antes de cualquier pipeline. Todo estado Git o de sistema de archivos desconocido falla cerrado.

| Requisito | Comprobación |
|---|---|
| Alcance cerrado de B | Delta respecto de la base de B igual a la lista exacta de rutas autorizadas, sin subconjuntos ni superconjuntos |
| Invariantes vigentes | Los trece estados de gobierno, RF-01..RF-27, RF-23 humana y RF-29 experimental, sin cambios |
| Dataset y provenance | `evidence.csv` de F34 y fixtures de A verificados por SHA-256 contra sus manifests y contra E |
| Integridad de A respecto de E | Bytes reales de `evidencia-sbx/**`, `tools/f35sbx/**` y de los cinco validadores históricos adaptados idénticos a sus blobs en E, sin archivos extra |
| Rutas nuevas de B | Solo las autorizadas en §6, con tipo y contenido de texto comprobados |
| Ciclo de vida de B | Textos exactos de apertura y cierre de B sobre su base, sin otro cambio de gobierno |
| Árbol, índice y archivos sin seguimiento | Comparados con la base y con E; renombrados como eliminación más alta |
| Bytes reales | Blob-id calculado sobre el archivo real, sin depender de `git diff` |
| Artefactos ocultos o ignorados | Recorrido del sistema de archivos; `.git/info/exclude` no oculta nada |
| Enlaces simbólicos y objetos especiales | Rechazados en rutas protegidas y nuevas |
| Flags del índice | Solo `H` en `git ls-files -v`: assume-unchanged (`h`), skip-worktree (`S`) y ambos (`s`) fallan |
| Historia y ascendencia | E como ancestro de HEAD y B0 integrada antes que B, identificadas por la historia y no por hashes futuros; historia completa sin simplificar |

## 4. Decisiones humanas de B

| Decisión | Resultado |
|---|---|
| DH-B01 | Sucesión de gates: gates históricos anclados más gate sucesor sobre HEAD (§2) |
| DH-B02 | Los gates históricos solo aportan evidencia complementaria del estado histórico (principios A y B) |
| DH-B03 | B usa rutas nuevas, separadas de A: `docs/academico/tools/f35sbxb/` y `docs/academico/evidencia-sbx-b/`. Sustituye la ubicación `tools/f35sbx/` que preveía §4 de los criterios de A, incompatible con el congelamiento de E |
| DH-B04 | Gate sucesor obligatorio sobre HEAD antes de cualquier implementación funcional (§3) |
| DH-B05 | Conformidad con el oráculo de A mediante una proyección, no por igualdad del informe completo (§5.2) |
| DH-B06 | Purga definida de forma verificable y sin prometer borrado físico de memoria (§5.3) |
| DH-B07 | SQLite solo `:memory:`, con la configuración de §5.4 |
| DH-B08 | Aislamiento por tenant: una conexión y un run por organización sintética, tenant validado antes de escribir |
| DH-B09 | Integridad de A respecto de E en cada ejecución del gate sucesor |
| DH-B10 | Fail-closed: cualquier error, excepción o estado desconocido deja el run en `fallido`, sin resultado parcial, y el gate con código de salida distinto de cero |
| DH-B11 | Todas las restricciones de G0 real, G0-SBX y sus prohibiciones siguen vigentes |
| DH-B12 | B no autoriza ML, CAP-33, CAP-34, F36–F40 ni ninguna fase posterior |

## 5. Hallazgos de la auditoría del plan

### 5.1 B0-M01: los gates históricos no validan HEAD

Resuelto por DH-B01, DH-B02 y DH-B04: el gate sucesor sobre HEAD es obligatorio y los gates históricos son solo evidencia complementaria.

### 5.2 B0-M02: proyección de conformidad con el oráculo

El informe de B no se compara byte a byte con los fixtures de A. Se compara una **proyección** con lo que el oráculo realmente fija:

| Se compara con el oráculo | Queda fuera, como metadato propio de B |
|---|---|
| Contenido de cada evidencia según el contrato | `run_kind`, `pipeline_version` e identificadores del run de B |
| Transformación T1 (`hash_before`, `hash_after`) | Estados de ejecución propios (`fallido`, `purgado`) |
| `content_hash` y cadenas definidas por el contrato | Fallos inyectados y sus códigos |
| Provenance y su encadenamiento | Comprobante de purga |
| Secuencia de estados y acciones de auditoría del oráculo | Rutas, instantes reales y datos de plataforma |

La lista exacta de campos se congela en el contrato de B antes de implementar. Para el determinismo, el informe usa JSON canónico en UTF-8, finales de línea LF, orden estable de claves y filas y el reloj lógico del run. No depende de rutas absolutas, de la hora real ni de diferencias entre Windows y macOS.

### 5.3 B0-M03: purga

La purga de B no es un borrado seguro de memoria ni una sanitización física de la RAM. Consiste en:

1. Almacenamiento exclusivamente SQLite `:memory:`.
2. Cierre explícito de cursores y conexiones.
3. Comprobación de que esas conexiones ya no se pueden usar.
4. Comprobación de que B no creó ningún archivo SQLite ni temporal persistente.
5. Un comprobante externo mínimo de finalización y purga en el informe.

La evidencia es de solo inserción durante toda la ejecución. El almacenamiento efímero se destruye cerrando la base `:memory:`, nunca con `DELETE` sobre tablas protegidas.

### 5.4 B0-M04: configuración de SQLite

- `PRAGMA foreign_keys = ON`, verificado tras activarlo.
- `temp_store` en memoria, verificado.
- Solo SQL fijo o parametrizado.
- `ATTACH`, exportación y persistencia prohibidos.
- Triggers que no se pueden modificar ni desactivar desde el pipeline.
- Una conexión y un run por tenant; tenant validado antes de cualquier escritura.

SQLite `:memory:` no es una frontera de seguridad frente a SQL arbitrario: la protección viene de que el pipeline solo ejecuta SQL fijo.

### 5.5 B0-L01: modelo de amenazas de B

| ID | Amenaza | Control | Prueba negativa | Resultado esperado |
|---|---|---|---|---|
| TSBB-01 | Contaminación con datos reales | Entradas solo con SHA-256 verificado contra E y el manifest de F34; reglas synthetic-only | Entrada alterada o con PII | FAIL; run `fallido` |
| TSBB-02 | Fuga entre tenants | Conexión y run por tenant; tenant validado antes de escribir | Fila de otro tenant | FAIL |
| TSBB-03 | Provenance manipulada | Cadena recalculada contra la proyección del oráculo | Eslabón alterado | FAIL; run `fallido` |
| TSBB-04 | Mutabilidad de la evidencia | Triggers que rechazan `UPDATE` y `DELETE` | `UPDATE` o `DELETE` sobre una tabla protegida | Error; run `fallido` |
| TSBB-05 | Replay | Identificador de run único y eventos contiguos | Evento reinsertado o run repetido | FAIL |
| TSBB-06 | Path traversal | Rutas fijas y normalizadas | Ruta con `..` o absoluta | FAIL |
| TSBB-07 | Artefactos ocultos | Delta exacto y recorrido del sistema de archivos | Archivo extra, ignorado o enlace | FAIL |
| TSBB-08 | Persistencia SQLite accidental | Solo `:memory:`; sin archivos antes ni después | Archivo `.db` o temporal creado | FAIL |
| TSBB-09 | Dependencia del runtime productivo | Solo biblioteca estándar autorizada; sin referencias a `app/`, `routes/`, `database/`, `storage/` ni `.env` | Importación o referencia prohibida | FAIL |
| TSBB-10 | Salida leída como scoring o recomendación | Esquema cerrado del informe; vocabulario prohibido | Campo de puntaje, orden o recomendación | FAIL |
| TSBB-11 | Fail-open | Toda excepción lleva a `fallido` y a código distinto de cero | Error inyectado en cada paso | FAIL controlado |
| TSBB-12 | No determinismo | Reloj lógico, orden explícito, JSON canónico | Dos ejecuciones con informes distintos | FAIL |
| TSBB-13 | Contenido activo o XSS | Texto plano sin marcado ni caracteres de control | Marcado HTML o script en el texto | FAIL |

### 5.6 B0-L02: estado documental de F35-SBX-A

Git confirma que F35-SBX-A, incluido su commit E, está integrada en `develop` y en `main`. B0 corrige solo la frase vigente que la daba como pendiente de publicación, en `CLAUDE.md` y `docs/PROGRESS.md`. `docs/academico/ACADEMIC_BASELINE.md` registra cierres de fase, conserva su texto del cierre de A y no cambia en B0. Los resultados de CI y los hashes de los merges se consultan en Git y GitHub.

## 6. Rutas de B

Autorizadas conceptualmente para la implementación; en B0 solo existe esta documentación.

| Ruta | Contenido admitido | Regla |
|---|---|---|
| `docs/academico/evidencia-sbx-b/` | Markdown y JSON de texto | Lista exacta de archivos, que fija el alcance de B |
| `docs/academico/tools/f35sbxb/` | Python con biblioteca estándar autorizada | Lista exacta de archivos; `sqlite3` solo aquí |

Pendiente para la implementación y fuera de B0: `sbxb_pipeline.py`, `sbxb_store.py`, el runtime SQLite, fixtures nuevos, modelos de ML y dependencias nuevas.

## 7. Gobierno y límites

- G0 real = NO APROBADA
- ADR-005 = PROPUESTA
- G0-SBX = APROBADA CON RESTRICCIONES
- F35 productiva = BLOQUEADA
- F35-SBX = HABILITADA, solo sandbox sintético
- F35-SBX-A = CERRADA E INTEGRADA
- F35-SBX-B = NO INICIADA hasta que B0 se audite y se autorice B
- F36–F40 = BLOQUEADAS
- Alcance C = BLOQUEADO
- Datos reales = PROHIBIDOS

B0 no cambia RF-01..RF-27, no modifica RF-23 y no habilita ranking, recomendación, scoring ni selección automática.

## 8. Validación de B0

- **Vigentes sobre HEAD**: `validate.py`, `validate.py --cierre-f29`, `validate_f29.py`, `test_f32_safety.py` y `validate_f34a.py` deben terminar sin fallas.
- **Históricos sobre HEAD**: fallan por diseño, por las causas de §1 (rama, rutas nuevas y gobierno). No se modifican para obtener PASS.
- **Históricos anclados** (§2.1): deben terminar sin fallas en su contexto de cierre.
- **Comprobaciones directas de B0**: delta exacto de B0 respecto de `develop`, integridad de A respecto de E, sin cambios en el runtime ni en las dependencias, sin flags del índice, `git diff --check` limpio y enlaces relativos válidos.

Hasta que exista el gate sucesor, estas comprobaciones directas sustituyen la validación de HEAD solo para B0, que es únicamente documental.
