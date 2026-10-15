# F35-SBX-B — B2-GOVERNMENT-CLOSURE: incremento sucesor de gobierno para el cierre formal de B2

> **Estado: B2-GOVERNMENT-CLOSURE = IMPLEMENTADO / CANDIDATO A AUDITORÍA INDEPENDIENTE.** Fecha: 14/10/2026. Rama `chore/f35-sbx-b2-government-closure`, desde `develop` = `eb02c2d84335347c52b81a76c1e73dc30b93e88a`.
>
> - **B2 = IMPLEMENTADA / CORREGIDA / REAUDITADA / CONGELADA / INTEGRADA TÉCNICAMENTE / PENDIENTE DE CIERRE FORMAL.**
> - Este incremento no se autoaprueba: el cierre formal de B2 lo decide la auditoría independiente.
>
> Las secciones 1 a 4 registran la investigación del contrato y el diseño, escritos antes de la transición de gobierno y del gate (commit RED). La sección 5 añade los resultados.

## 1. Punto de partida verificado

### 1.1 Anclas técnicas aprobadas

| Ancla | Commit | Qué es |
|---|---|---|
| B1 | `8e94a60274fe39ebda3e9961bc58036b389dfc00` | Ancla auditada de B1 |
| B1-FREEZE | `3d9b78307684a0dfb093e31d28fde290b2b1cb4a` | Cierre de B1 |
| Base de B2 | `72e86c5838984ea873d6dd56c179d94217b27317` | `develop` al crear la rama de B2 |
| Transición de gobierno de B2 | `12c1c36e409f81c048fccf7fcb3e6d2a2d5d40aa` | Paso único del blob de B1 al blob de B2 |
| Candidato de B2 | `2472fd6fadfc0634ec68cbcb76cfc9fbfe105194` | B2 reauditada (H01, M01 y M02 corregidos) |
| B2-FREEZE | `9961d2d65ed51a17c14aae5db0edb7d71c622c22` | Freeze del candidato |
| Sucesor | `9d6fb157bb818574217e3675da1849e8d1010962` | Gate sucesor vigente (AF-M01) |
| B2-SUCCESSOR-FREEZE | `89694244b81b0bd84dbe6ae5d04b5c7a198bafef` | Cierre de la capa sucesora (AF-L02). Árbol `ae182fe936a89b2155932c4d34194547c3e4c59a`; padre `1e5677e8aee73f3267dcd81a0273bdeddd832b8b` |

La auditoría independiente fijó como ancla externa aprobada del cierre de la capa sucesora el commit `89694244b81b0bd84dbe6ae5d04b5c7a198bafef`, que es el que informa la línea INFO de FRZ de su validador. Decisiones registradas por la auditoría: AF-M01 = RESUELTO; AF-L02 = RESUELTO; SF26 = CORRECTO; B2-SUCCESSOR-FREEZE = IMPLEMENTADO / AUDITADO / APROBADO PARA INTEGRACIÓN; no hace falta otro freeze del freeze.

### 1.2 Integración técnica ya realizada

| Hecho | Valor | Cómo se verificó en este incremento |
|---|---|---|
| Publicación de la rama de B2 | `origin/feature/f35-sbx-b2-ephemeral-store` = `89694244b81b0bd84dbe6ae5d04b5c7a198bafef` | `git fetch` y `git ls-remote` |
| Merge en `develop` | `eb02c2d84335347c52b81a76c1e73dc30b93e88a`, con padres `72e86c5` y `8969424` | Objetos Git; `origin/develop` = `eb02c2d` |
| Merge en `main` | `5bf4f4e58c3860be4c5d9f94d1c4b5a031570d33`, con padres `3fdfdce` y `eb02c2d` | Objetos Git; `origin/main` = `5bf4f4e` |
| Árboles | `8969424`, `eb02c2d` y `5bf4f4e` tienen el mismo árbol `ae182fe` | `git log --format=%T` |
| Ascendencia | `8969424` → `eb02c2d` → `5bf4f4e` | `git merge-base --is-ancestor` |
| CI de `develop` | Workflow `tests`, run 57, id `38650923020`, SHA `eb02c2d`: `completed` / `success` | API pública de GitHub (`actions/runs/38650923020`) |
| CI de `main` | Workflow `tests`, run 58, id `38652088845`, SHA `5bf4f4e`: `completed` / `success` | API pública de GitHub (`actions/runs/38652088845`) |
| Etiquetas | `v1.0.0-academic` → `9a946c2` y `v1.1.0-academic` → `634f354`, sin cambios ni etiquetas nuevas | `git ls-remote --tags` |
| Repositorio | Sin injertos, sin objetos de reemplazo, historia completa, árbol limpio | `git replace -l`, `info/grafts`, `--is-shallow-repository` |

Los merges no introdujeron contenido: `eb02c2d` y `5bf4f4e` tienen exactamente el árbol del candidato aprobado. Antes y después de la integración el equipo acreditó B2-SUCCESSOR-FREEZE 12/0 (batería 26/26), el sucesor histórico 7/0 (batería 14/14), B2-FREEZE 10/0 (batería 27/27), B2 histórico 119/0, B2 sobre HEAD 118/1 (solo SCP, clase A), B1 histórico 159/0 y B1-FREEZE 14/0.

### 1.3 Qué falta

B2 está integrada técnicamente, pero el gobierno (`CLAUDE.md` y `docs/PROGRESS.md`) la sigue describiendo como «candidata a auditoría independiente». La auditoría determinó que esa transición se hace como incremento sucesor explícitamente autorizado y no como cambio incidental durante los merges. Este documento es ese incremento.

## 2. Contrato de sucesión encontrado

### 2.1 Qué impide modificar el gobierno de forma incidental

Cinco capas lo establecen, todas congeladas:

| Fuente | Regla |
|---|---|
| [Contrato de B2](../evidencia-sbx-b2/F35SBXB_B2_Contrato_Verificacion.md), §2.3 y Q1 | La transición de gobierno de B2 es única y monotónica. Todo descendiente de `12c1c36` conserva el blob de B2 (regla 3), ningún otro commit introduce un blob de gobierno (regla 4) y «una transición de gobierno distinta en el futuro solo podrá autorizarla otro incremento sucesor, con su propio contrato y su propia ancla» |
| [B2-FREEZE](../evidencia-sbx-b2-freeze/F35SBXB_B2_Freeze.md), §8, §9 y R3 | `CLAUDE.md` y `docs/PROGRESS.md` están en el nivel A del freeze. «Si un incremento posterior autorizado cambia una ruta congelada (por ejemplo, el gobierno), este validador fallará sobre ese HEAD, y debe fallar. Ese incremento aportará su propio gate sucesor y ejecutará este validador anclado sobre el commit de freeze» |
| [Sucesor](../evidencia-sbx-b2-sucesor/F35SBXB_B2_Sucesor.md), §3 y R5–R6 | Un cambio legítimo de un incremento futuro es una falla de clase A, y ese incremento «aportará su propio gate sucesor». La actualización de gobierno queda pendiente de un incremento sucesor autorizado |
| [B2-SUCCESSOR-FREEZE](../evidencia-sbx-b2-sucesor-freeze/F35SBXB_B2_Sucesor_Freeze.md), §2, §3.6, R1, R5 y R6 | Es la última capa de B2: no se añade otra capa de freeze. Su ancla la anota la auditoría y «un incremento sucesor autorizado lo registra». Cambiar el gobierno ahora «rompería la cadena» sin ese incremento |
| [B0](../evidencia-sbx-b/F35SBXB_B0_Sucesion_de_Gates.md), §2.2 y DH-B13 | Un gate congelado que no reconoce una evolución autorizada de rutas o de ciclo de vida falla por clase A. Esa falla no se ignora: obliga a la evaluación sucesora completa sobre HEAD. La sucesión no reduce ni reinterpreta los criterios |

El precedente es la propia historia de B: el cierre de B1 lo registró en el gobierno el incremento siguiente (B2, commit `12c1c36`), aplicando un delta literal cerrado declarado por su contrato, nunca un merge.

### 2.2 Respuestas del contrato

| # | Pregunta | Respuesta |
|---|---|---|
| 1 | ¿Qué regla impide modificar el gobierno incidentalmente? | Las reglas 3 y 4 de §2.3 de B2, el nivel A de B2-FREEZE y §3.6 del cierre de la capa sucesora (§2.1) |
| 2 | ¿Qué transición monotónica existe? | `HISTORICAL_B1_BLOB` → `B2_GOVERNANCE_BLOB` en `12c1c36`. Este incremento añade una sola más: `B2_GOVERNANCE_BLOB` → `B2_CLOSURE_GOVERNANCE_BLOB`, con las mismas cuatro reglas |
| 3 | ¿Qué estado está registrado? | B1 cerrada, congelada e integrada; B2 implementada y candidata a auditoría independiente; los trece estados de gobierno; F35-SBX-B INICIADA |
| 4 | ¿Qué puede registrarse ahora con evidencia objetiva? | B2 implementada, corregida, reauditada, congelada e integrada técnicamente en `develop` y `main`, con el ancla aprobada y los dos merges (§1). No su cierre formal, que depende de la auditoría de este incremento |
| 5 | ¿Qué archivos pueden modificarse? | `CLAUDE.md` y `docs/PROGRESS.md`, solo mediante la transición única de §3.3, y las rutas nuevas de esta capa (§3.1) |
| 6 | ¿Qué archivos están congelados? | Los de B1, B1-FREEZE, B2, B2-FREEZE, el sucesor y B2-SUCCESSOR-FREEZE (§3.4), además de A, B0, el dataset y el runtime |
| 7 | ¿Hace falta un validador nuevo? | Sí. Todas las capas congeladas fallan sobre un HEAD con otro gobierno, y su contrato exige que el incremento que lo cambie aporte su propio gate sucesor sobre HEAD |
| 8 | ¿Hace falta evidencia de cierre? | Sí: este documento, con la integración verificada, el diseño, la batería y los resultados |
| 9 | ¿Hace falta un manifiesto? | No. Las anclas registradas en el gate y los objetos Git verificados son la fuente de verdad; un manifiesto no acreditaría nada por sí mismo (§3.5 de B2-SUCCESSOR-FREEZE) |
| 10 | ¿Hace falta otro freeze? | No. La auditoría lo descartó, y este incremento no protege su capa con otra capa: su ancla es el commit que la completa, derivado de Git y registrado fuera (§3.6) |

### 2.3 Transición de gobierno permitida

El estado máximo que este incremento puede registrar por sí mismo es:

- **B2-GOVERNMENT-CLOSURE = IMPLEMENTADO / CANDIDATO A AUDITORÍA INDEPENDIENTE**;
- **B2 = IMPLEMENTADA / CORREGIDA / REAUDITADA / CONGELADA / INTEGRADA TÉCNICAMENTE / PENDIENTE DE CIERRE FORMAL**.

El cierre formal lo decide la auditoría independiente sobre el ancla de este incremento. Igual que B1, su registro en el gobierno corresponde después al incremento sucesor que el equipo autorice. Los trece estados de gobierno no cambian, y F35-SBX-B sigue INICIADA.

## 3. Diseño

### 3.1 Rama, base y archivos

- **Base:** `develop` integrado, `eb02c2d84335347c52b81a76c1e73dc30b93e88a`. Es la convención real del proyecto: B0, B1 y B2 nacieron de `develop`, y los incrementos solo de gobierno usan `chore/` (`chore/f35-sbx-b0-gate-succession`, `chore/phase-13-governance`). `main` tiene el mismo árbol, pero se integra desde `develop`.
- **Rama:** `chore/f35-sbx-b2-government-closure`. La rama de B2 se conserva intacta en `8969424`.

| Ruta | Estado frente a la base | Contenido |
|---|---|---|
| `docs/academico/evidencia-sbx-b2-cierre-gobierno/F35SBXB_B2_Cierre_Gobierno.md` | A | Este documento |
| `docs/academico/tools/f35sbxb2_cierre_gobierno/validate_f35sbxb2_cierre_gobierno.py` | A | Gate sucesor sobre HEAD |
| `docs/academico/tools/f35sbxb2_cierre_gobierno/test_f35sbxb2_cierre_gobierno.py` | A | Batería GC01..GC26 |
| `CLAUDE.md`, `docs/PROGRESS.md` | M | Solo mediante la transición de §3.3 |

Nada más: ni runtime, ni CI, ni dataset, ni A, B0, B1, B1-FREEZE, B2, B2-FREEZE, el sucesor o B2-SUCCESSOR-FREEZE, ni `ACADEMIC_BASELINE.md`.

### 3.2 Commits

1. **RED.** Este diseño y la batería, sin gate: la batería falla entera.
2. **Transición de gobierno.** Un solo padre; cambia exactamente `CLAUDE.md` y `docs/PROGRESS.md`, aplicando el delta de §3.3.
3. **GREEN.** El gate, que registra el commit de la transición (ya existe: no hay autorreferencia), y los resultados de §5. Es el commit que completa la capa.

### 3.3 Delta de gobierno

`B2_GOVERNANCE_BLOB` es el blob de `12c1c36` (`74cc4a71c56918678e0a70c7f59a3f060d87b6a0` en `CLAUDE.md` y `07889bf8c82990651539a6e4b8a1098b4bd2d35a` en `docs/PROGRESS.md`). `B2_CLOSURE_GOVERNANCE_BLOB` resulta de aplicarle una lista cerrada de reemplazos literales, cada bloque antiguo presente exactamente una vez. El gate la calcula por su cuenta. Los bloques nuevos de `docs/PROGRESS.md` difieren de los de `CLAUDE.md` solo en la ruta relativa de los enlaces.

```text
CLAUDE.md, reemplazo 1 (y docs/PROGRESS.md, reemplazo 3)
  antes:   F35-SBX-B INICIADA solo como sandbox sintético: B1 (gate sucesor sobre HEAD) CERRADA, CONGELADA E INTEGRADA; B2 (almacén efímero SQLite `:memory:` por organización sintética) IMPLEMENTADA, sin pipeline funcional ni ML.
  después: F35-SBX-B INICIADA solo como sandbox sintético: B1 (gate sucesor sobre HEAD) CERRADA, CONGELADA E INTEGRADA; B2 (almacén efímero SQLite `:memory:` por organización sintética) IMPLEMENTADA, CORREGIDA, REAUDITADA, CONGELADA E INTEGRADA TÉCNICAMENTE, PENDIENTE DE CIERRE FORMAL, sin pipeline funcional ni ML.

CLAUDE.md, reemplazo 2 (y docs/PROGRESS.md, reemplazo 4, con enlaces relativos a docs/)
  antes:   F35-SBX-B INICIADA: su incremento B1 (gate sucesor sobre HEAD) está CERRADO, CONGELADO E INTEGRADO en `develop` y `main` (ancla auditada `8e94a60274fe39ebda3e9961bc58036b389dfc00`, cierre `3d9b78307684a0dfb093e31d28fde290b2b1cb4a`), registrado en [`evidencia-sbx-b-freeze`](docs/academico/evidencia-sbx-b-freeze/F35SBXB_B1_Freeze.md); su incremento B2 (almacén efímero aislado) está IMPLEMENTADO y es CANDIDATO A AUDITORÍA INDEPENDIENTE, en `feature/f35-sbx-b2-ephemeral-store` y registrado en [`evidencia-sbx-b2`](docs/academico/evidencia-sbx-b2/README.md). Su integración y su publicación requieren autorización explícita del equipo.
  después: F35-SBX-B INICIADA: su incremento B1 (gate sucesor sobre HEAD) está CERRADO, CONGELADO E INTEGRADO en `develop` y `main` (ancla auditada `8e94a60274fe39ebda3e9961bc58036b389dfc00`, cierre `3d9b78307684a0dfb093e31d28fde290b2b1cb4a`), registrado en [`evidencia-sbx-b-freeze`](docs/academico/evidencia-sbx-b-freeze/F35SBXB_B1_Freeze.md); su incremento B2 (almacén efímero aislado) está IMPLEMENTADO, CORREGIDO, REAUDITADO, CONGELADO E INTEGRADO TÉCNICAMENTE en `develop` y `main` (ancla aprobada `89694244b81b0bd84dbe6ae5d04b5c7a198bafef`, merges `eb02c2d84335347c52b81a76c1e73dc30b93e88a` y `5bf4f4e58c3860be4c5d9f94d1c4b5a031570d33`), registrado en [`evidencia-sbx-b2`](docs/academico/evidencia-sbx-b2/README.md), y está PENDIENTE DE CIERRE FORMAL: su incremento de cierre de gobierno está IMPLEMENTADO y es CANDIDATO A AUDITORÍA INDEPENDIENTE, en `chore/f35-sbx-b2-government-closure` y registrado en [`evidencia-sbx-b2-cierre-gobierno`](docs/academico/evidencia-sbx-b2-cierre-gobierno/F35SBXB_B2_Cierre_Gobierno.md). La integración y la publicación de ese incremento requieren autorización explícita del equipo.

docs/PROGRESS.md, reemplazo 1
  antes:   Última actualización: 2026-10-12 (F34E CERRADA; G0 real NO APROBADA; G0-SBX APROBADA CON RESTRICCIONES; F35-SBX sintética HABILITADA; F35-SBX-A CERRADA E INTEGRADA; B0 CERRADA E INTEGRADA; F35-SBX-B INICIADA: B1 CERRADA E INTEGRADA, B2 IMPLEMENTADA Y CANDIDATA A AUDITORÍA INDEPENDIENTE).
  después: Última actualización: 2026-10-14 (F34E CERRADA; G0 real NO APROBADA; G0-SBX APROBADA CON RESTRICCIONES; F35-SBX sintética HABILITADA; F35-SBX-A CERRADA E INTEGRADA; B0 CERRADA E INTEGRADA; F35-SBX-B INICIADA: B1 CERRADA E INTEGRADA, B2 INTEGRADA TÉCNICAMENTE Y PENDIENTE DE CIERRE FORMAL).

docs/PROGRESS.md, reemplazo 2
  antes:   a B1 cerrada e integrada y B2 implementada, candidata a auditoría independiente.
  después: a B1 cerrada e integrada y B2 implementada, candidata a auditoría independiente. El 14/10/2026 pasó a B2 integrada técnicamente y pendiente de cierre formal, con su incremento de cierre de gobierno candidato a auditoría independiente.
```

`B2_CLOSURE_TRANSITION` es el commit que introduce, en las dos rutas a la vez, el paso `B2_GOVERNANCE_BLOB` → `B2_CLOSURE_GOVERNANCE_BLOB`. Se registra en el gate después de que exista, en el commit GREEN, nunca en el propio commit.

### 3.4 Gate sucesor

Ubicación: `docs/academico/tools/f35sbxb2_cierre_gobierno/validate_f35sbxb2_cierre_gobierno.py`. Solo biblioteca estándar, sin red, aislado (`python -I`, al que se relanza solo), con objetos Git verificados recalculando su identificador y con fallo cerrado ante cualquier error, salida incompleta o estado no evaluable.

| ID | Comprueba |
|---|---|
| ENT | Intérprete aislado y sin `PYTHONPATH`, `PYTHONHOME` ni `PYTHONUSERBASE`. Ninguna variable de Git que redirija el repositorio, el índice o los objetos. Git sobre el repositorio del gate, con historia completa y sin injertos ni objetos de reemplazo |
| CTX | Rama `chore/f35-sbx-b2-government-closure`, `develop` o `main`, y el merge de integración `eb02c2d` como ancestro de HEAD |
| ANC | Anclas registradas como commits íntegros y en cadena: `8e94a60` → `3d9b783` → `72e86c5` → `12c1c36` → `2472fd6` → `9961d2d` → `9d6fb15` → `8969424`. El merge `eb02c2d` tiene como padres `72e86c5` y `8969424`, y el mismo árbol que `8969424`. El blob de gobierno de `12c1c36` es el registrado |
| HIS | El validador de B2-SUCCESSOR-FREEZE, con los bytes de su blob en `8969424`, ejecutado anclado sobre `8969424` en un clon temporal sin remoto: código 0, 12 correctas y 0 fallas, y FRZ deriva exactamente `8969424`. Es el procedimiento de acreditación de §3.5 de ese cierre, automatizado |
| SUC | El mismo validador, verificado contra su blob, ejecutado sobre HEAD. Solo pueden fallar VIG y ALC (clase A). Las violaciones visibles de ALC solo nombran rutas de este incremento, en los tres planos. FRZ deriva `8969424`. VIG informa que el sucesor solo falla en ALC, CON o MAT, y que las reglas del gate de B2 en falla son las mismas que observa MAT |
| MAT | El gate de B2, verificado contra su blob en el candidato, ejecutado sin cambios sobre HEAD. Solo puede fallar por lo que se predice desde el estado observado (§3.5): CTX por la rama de este incremento, SCP por las 14 rutas posteriores al candidato en tres planos, y B1F, DYN (solo P25) y GOV por la divergencia del gobierno respecto de su blob. Total de comprobaciones: 119 |
| INT | Integridad propia de las capas congeladas, cada una desde su ancla: conjunto de B1 sin gobierno y su carpeta (`8e94a60`), B1-FREEZE (`3d9b783`), B2 sin gobierno (`2472fd6`), B2-FREEZE (`9961d2d`), sucesor (`9d6fb15`) y B2-SUCCESSOR-FREEZE (`8969424`). En cada commit posterior a cada ancla que lleva a HEAD, merges incluidos, y en HEAD, el índice y el disco |
| FLG | Ningún flag en el índice |
| GOV | Transición única y monotónica en tres etapas (§3.6), en cada commit desde `8e94a60`; transición derivada igual a la registrada; estado efectivo en HEAD, índice y disco |
| SEM | Semántica del gobierno vigente y de los documentos de esta capa con las piezas verificadas del gate de B1, más la sucesión del ciclo de vida de B2 (§3.7) |
| ALC | Alcance exacto frente a `eb02c2d`: HEAD, el índice y el árbol de trabajo solo añaden las tres rutas de la capa y modifican las dos de gobierno; ningún archivo sin seguimiento; carpetas de la capa exactas |
| FRZ | Nivel B: un único commit posterior a `eb02c2d` completa la capa y HEAD desciende de él. Desde él, cada commit, HEAD, el índice y el disco tienen exactamente sus archivos. La línea INFO informa ese commit |
| DEP | Los archivos Python de la capa solo importan la biblioteca estándar autorizada. La única ejecución dinámica es la carga del gate de B1 desde los bytes de su blob verificado en `8e94a60` |

### 3.5 Clasificación de clase A, sin ocultar nada

Sobre un HEAD válido, los gates congelados fallan, y deben fallar:

| Gate congelado sobre HEAD | Falla esperada | Causa |
|---|---|---|
| B2 (`validate_f35sbxb2.py`) | CTX, B1F, SCP, DYN, P25 y GOV | Rama nueva; tres rutas nuevas; tercer blob de gobierno (regla 3 de su §2.3) y su vocabulario de ciclo de vida, que no admite «b2 integrada» |
| B2-FREEZE | HIS, ARB, IDX y DSK | Solo por `CLAUDE.md` y `docs/PROGRESS.md`, del nivel A |
| Sucesor | CON, MAT y ALC | Componen los dos anteriores y las rutas nuevas |
| B2-SUCCESSOR-FREEZE | VIG y ALC | Compone el sucesor; rutas nuevas |

Ninguna se oculta. MAT ejecuta el gate de B2 intacto y exige que cada falla sea exactamente la que el estado observado predice:

- **CTX:** solo `rama no permitida` con el nombre de esta rama, y solo en ella; en `develop` y `main` tiene que pasar.
- **SCP:** 3 × 14 = 42 violaciones (las once rutas de B2-FREEZE, el sucesor y su cierre, y las tres de esta capa), todas visibles de esas rutas.
- **B1F:** una violación de la regla 3 por cada commit de la ascendencia que desciende de `12c1c36` y no tiene el blob de B2, más una por cada plano (árbol, índice, disco) y ruta en que HEAD difiere de él. El gate cuenta esos commits por su cuenta.
- **DYN y P25:** solo P25, con esas mismas violaciones.
- **GOV:** «contenido distinto» por cada ruta cuyo contenido no es ni el blob de B1 ni el de B2, y, como única afirmación semántica admitida, la declaración de B2 integrada o congelada, que ahora es un hecho verificado por ANC. Toda otra línea, o una lista truncada, hace fallar MAT.
- **El resto** (AIN, B0F, HST, SBX, FSY, FLG, DEP, PRE, STA, DET, ISO, PUR, DAT, CAP y los demás casos, historias F01..F21 y negativos) tiene que pasar.

Lo que esas fallas enmascaran se repone con reglas propias: la integridad de las capas (INT, en lugar de B1F, del freeze y de CON), la monotonía (GOV, en lugar de las reglas 1 a 4 de B2) y la semántica completa (SEM, en lugar de GOV de B2). La legitimidad de la divergencia de gobierno no la decide MAT, sino GOV y SEM.

### 3.6 GOV: tres etapas

Para cada commit `C` de la ascendencia de HEAD que desciende de `8e94a60`, merges incluidos, lo admitido depende solo de su ascendencia:

1. **Antes de `12c1c36`, o si `C` no desciende de él:** el blob histórico de B1.
2. **Desde `12c1c36` y hasta la transición del cierre, o si `C` no desciende de ella:** `B2_GOVERNANCE_BLOB`.
3. **En la transición del cierre y en todo descendiente:** `B2_CLOSURE_GOVERNANCE_BLOB`.

Además:

- solo `12c1c36` introduce el blob de B2 y solo la transición del cierre introduce el blob del cierre, en las dos rutas a la vez;
- la transición tiene un solo padre, con el blob de B2, desciende de `eb02c2d` y cambia exactamente las dos rutas;
- la transición derivada coincide con la registrada;
- HEAD, el índice y el disco tienen el blob del cierre.

Modificar y restaurar, volver al blob de B2, un tercer blob, una transición en un merge, en una sola ruta o que cambie otras rutas fallan. Un merge `--no-ff` legítimo en `develop` y en `main` desciende de la transición y lleva el blob del cierre: pasa.

### 3.7 SEM: sucesión del ciclo de vida de B2

SEM carga el gate de B1 desde los bytes de su blob en `8e94a60`, verificados recalculando su identificador, como hace el gate de B2 (Q5). Con sus piezas comprueba, en el gobierno de HEAD:

- una única sección «Estado vigente F34E», con los trece estados exactos;
- F35-SBX-B solo INICIADA;
- ninguna declaración contradictoria ni afirmación positiva que habilite una capacidad prohibida en lo vigente y en las líneas añadidas frente al blob de B2;
- la mención expresa de que B2 sigue PENDIENTE DE CIERRE FORMAL.

La única diferencia con la semántica del gate de B2 es la sucesión del ciclo de vida de B2, que ya está verificada por ANC:

| Ciclo de vida de B2 | Gate de B2 (congelado) | Este gate |
|---|---|---|
| Implementada | Admitida | Admitida |
| Congelada | Rechazada | Admitida |
| Integrada | Rechazada | Admitida |
| Cierre formal y estados posteriores | Rechazados | Rechazados |

Los dos gates rechazan los estados posteriores, empezando por el cierre formal (la lista exacta es `B2_FORBIDDEN_RX` del gate). Por eso el gobierno no puede registrar el cierre formal de B2 antes de la auditoría de este incremento. Los documentos `.md` de esta capa pasan las mismas comprobaciones (sin datos personales, afirmaciones positivas ni declaraciones contradictorias), y todos sus archivos son UTF-8 sin BOM, CR ni NUL.

### 3.8 Raíz de confianza y ancla de este incremento

- **Registradas en el gate,** porque ya existen: las anclas de §1.1, el merge `eb02c2d` y la transición del cierre.
- **Derivada y registrada fuera:** el commit que completa la capa (nivel B), que el gate informa en la línea INFO de FRZ. Es el ancla de este incremento. La auditoría la anota y comprueba que el ancla derivada coincide; ningún archivo guarda su propio hash.
- **No se añade otra capa de freeze.** Una capa reconstruida con los mismos bytes en otra historia falla en GOV (la transición derivada no es la registrada) e informa otra ancla en FRZ (GC07).
- **El merge en `main` (`5bf4f4e`)** no es ancestro de esta rama, así que no se verifica en el gate: se registra en §1.2 y en el gobierno, verificado con Git y con el CI, y será ancestro tras integrar este incremento en `main`.

### 3.9 Lo que no cambia

- Los artefactos congelados de B1 a B2-SUCCESSOR-FREEZE conservan sus bytes, y sus validadores no se ejecutan con constantes alteradas ni se reescriben.
- El candidato `8969424` y los merges `eb02c2d` y `5bf4f4e` no se tocan.
- G0 real = NO APROBADA; G0-SBX = APROBADA CON RESTRICCIONES; ADR-005 = PROPUESTA, con la aprobación interna del equipo registrada y sin aprobación jurídica, de privacidad ni institucional; G0-02, G0-03 y G0-12 = PENDIENTE EXTERNO; F35 productiva, F36–F40 y el alcance C siguen BLOQUEADOS y los datos reales, PROHIBIDOS.
- RF-23 sigue siendo decisión final humana del Aprobador/Dirección y RF-29 sigue experimental e informativa. El baseline RF-01 a RF-27 no cambia.
- Este incremento es solo gobierno, documentación y QA. No añade datos, capacidades, endpoints, migraciones, dependencias ni runtime.

## 4. Pruebas

Cada caso trabaja en un clon desechable de HEAD, fuera del repositorio, con configuración de Git aislada, identidad ficticia y fechas fijas, y ejecuta el gate con `python -I`. Pasa si fallan exactamente las reglas esperadas y, cuando se indica, si las líneas FALLA o INFO contienen el motivo esperado. Las historias reconstruidas se crean con plumbing de Git sobre un índice propio, con el mismo contenido que HEAD.

| Caso | Escenario | Reglas en falla esperadas |
|---|---|---|
| GC01 | Estado válido; el ancla derivada es el commit que completa la capa | Ninguna (PASS) |
| GC02 | Merge `--no-ff` en `develop` (`eb02c2d`) y después de `develop` en `main` (`5bf4f4e`) | Ninguna en ambos |
| GC03 | Commit posterior sin cambios de contenido | Ninguna |
| GC04 | Tercer blob de gobierno tras la transición | GOV |
| GC05 | Modificar → restaurar el gobierno tras la transición | GOV |
| GC06 | Vuelta al blob de gobierno de B2 | GOV, SEM y ALC |
| GC07 | Historia reconstruida con el mismo contenido | GOV (transición distinta de la registrada); FRZ informa otra ancla |
| GC08 | Transición que también cambia otra ruta | GOV |
| GC09 | Transición hecha en un merge | GOV |
| GC10 | Transición repartida en dos commits, una ruta en cada uno | GOV |
| GC11 | Almacén de B2 alterado y confirmado | INT, MAT, SUC y ALC |
| GC12 | Validador de B2-SUCCESSOR-FREEZE alterado y confirmado | INT, SUC y ALC |
| GC13 | Modificar → restaurar el documento del sucesor | INT y SUC |
| GC14 | Rama lateral que altera y restaura el gate de B1, integrada con merge `--no-ff` | INT y MAT |
| GC15 | LF añadido a `evidence.csv` en el árbol de trabajo | MAT, SUC y ALC; MAT nombra SBX, FSY y PRE |
| GC16 | Artefacto ignorado en `public/build/` | MAT, que nombra FSY |
| GC17 | Clon superficial | Todas salvo FLG y DEP (fallo cerrado) |
| GC18 | `GIT_DIR`, `GIT_WORK_TREE` y `GIT_INDEX_FILE` hacia un clon limpio | ENT |
| GC19 | Injertos sin efecto | ENT y SUC |
| GC20 | skip-worktree en `CLAUDE.md` con un cambio que `git status` no ve | GOV, FLG, MAT y SUC |
| GC21 | Documento de esta capa modificado y confirmado tras completarla | FRZ |
| GC22 | Gate de esta capa alterado y confirmado: copia de confianza en el disco; copia alterada | FRZ; FRZ y DEP |
| GC23 | Dato personal ficticio en el documento de esta capa, confirmado | SEM y FRZ |
| GC24 | Gobierno que anticipa el cierre formal de B2, confirmado | GOV, SEM y MAT |
| GC25 | Gobierno que altera el estado de G0 real, confirmado | GOV, SEM y MAT |
| GC26 | HEAD separado | CTX y MAT |

Propiedades que cubren:

- **GC01 a GC03:** los estados legítimos, incluidas las integraciones futuras `--no-ff`.
- **GC04 a GC10:** la monotonía de la transición y su registro.
- **GC11 a GC14:** la integridad de las capas congeladas y su historia.
- **GC15 y GC16:** lo que solo la evaluación material detecta.
- **GC17 a GC20:** el entorno de Git hostil o incompleto.
- **GC21 a GC23:** el nivel B de esta capa y su contenido.
- **GC24 y GC25:** que ni un cierre formal anticipado de B2 ni un cambio de G0 pasan por el gobierno.
- **GC26:** el contexto.

## 5. Resultados

Pendiente del commit GREEN.
