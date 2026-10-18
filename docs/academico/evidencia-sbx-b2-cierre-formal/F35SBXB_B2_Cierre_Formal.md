# F35-SBX-B — B2: registro del cierre formal (R2-A)

> **Estado: R2-A = IMPLEMENTADO / VALIDADO LOCALMENTE / CANDIDATO A AUDITORÍA INDEPENDIENTE.** Fecha: 18/10/2026. Rama `chore/f35-sbx-b2-r2a-final-closure`, desde `develop` = `04895aacd96f0f03dde84e10a558bbdf26f050c6`.
>
> - **B2 = CIERRE FORMAL PREPARADO / PENDIENTE DE AUDITORÍA R2-A.** El gobierno de esta rama ya registra el cierre (§3.3), pero ese registro solo vale cuando la auditoría independiente apruebe este incremento y el equipo autorice su integración. Hasta entonces, `develop` y `main` siguen diciendo «PENDIENTE DE CIERRE FORMAL».
> - **B2-GOVERNMENT-CLOSURE = AUDITADO / APROBADO / INTEGRADO**, con la decisión R2-A de la auditoría independiente.
> - Este incremento no se autoaprueba: lo decide la auditoría independiente sobre su ancla.
>
> Las secciones 1 a 4 registran el contrato y el diseño, escritos antes de la transición de gobierno y del gate (commit RED `c2c1f6e`). La sección 5 añade los resultados.

## 1. Punto de partida verificado

### 1.1 Anclas aprobadas

| Ancla | Commit | Qué es |
|---|---|---|
| B1 | `8e94a60274fe39ebda3e9961bc58036b389dfc00` | Ancla auditada de B1 |
| B1-FREEZE | `3d9b78307684a0dfb093e31d28fde290b2b1cb4a` | Cierre de B1 |
| Base de B2 | `72e86c5838984ea873d6dd56c179d94217b27317` | `develop` al crear la rama de B2 |
| Transición de gobierno de B2 | `12c1c36e409f81c048fccf7fcb3e6d2a2d5d40aa` | Blob de B1 → blob de B2 |
| Candidato de B2 | `2472fd6fadfc0634ec68cbcb76cfc9fbfe105194` | B2 reauditada |
| B2-FREEZE | `9961d2d65ed51a17c14aae5db0edb7d71c622c22` | Freeze del candidato |
| Sucesor | `9d6fb157bb818574217e3675da1849e8d1010962` | Gate sucesor (AF-M01) |
| B2-SUCCESSOR-FREEZE | `89694244b81b0bd84dbe6ae5d04b5c7a198bafef` | Cierre de la capa sucesora (AF-L02) |
| Integración de B2 | `eb02c2d84335347c52b81a76c1e73dc30b93e88a` (`develop`) y `5bf4f4e58c3860be4c5d9f94d1c4b5a031570d33` (`main`) | Merges `--no-ff` con el árbol de `8969424` |
| Transición del cierre de gobierno | `d346597e988d2f7f5d0d84e119709012b67715da` | Blob de B2 → blob del cierre de gobierno |
| B2-GOVERNMENT-CLOSURE | `363273ead5794ea7a2dba74c011a0efd6d59e906` | Ancla externa aprobada del cierre de gobierno. Árbol `53f6252b0c5c69140c0d75224f9d0a155125bd80` |

### 1.2 Integración del cierre de gobierno

| Hecho | Valor | Cómo se verificó |
|---|---|---|
| Rama publicada | `origin/chore/f35-sbx-b2-government-closure` = `363273e` | `git fetch` y `git ls-remote` |
| Merge en `develop` | `04895aacd96f0f03dde84e10a558bbdf26f050c6`, con padres `eb02c2d` y `363273e` | Objetos Git; `origin/develop` = `04895aa` |
| Merge en `main` | `d5a4b4e7c4ba01c1b923d215a51f0d2f22c8f163`, con padres `5bf4f4e` y `04895aa` | Objetos Git; `origin/main` = `d5a4b4e` |
| Árboles | `363273e`, `04895aa` y `d5a4b4e` tienen el mismo árbol `53f6252b` | `git rev-parse <commit>^{tree}` |
| CI de `develop` | Workflow `tests`, run 59, id `39092994296`, SHA `04895aa`: `completed` / `success` | API pública de GitHub |
| CI de `main` | Workflow `tests`, run 60, id `39093918299`, SHA `d5a4b4e`: `completed` / `success` | API pública de GitHub |
| Etiquetas | `v1.0.0-academic` → `9a946c2` y `v1.1.0-academic` → `634f354`, sin etiquetas nuevas | `git ls-remote --tags` |

La auditoría independiente del cierre de gobierno lo dejó AUDITADO, APROBADO E INTEGRADO, con su gate en 13/0 y su batería en 26/26, y decidió **R2-A**: un incremento mínimo posterior para registrar en el gobierno el cierre formal de B2, que ya está acreditado.

### 1.3 Qué falta

El gobierno integrado (`CLAUDE.md` y `docs/PROGRESS.md` en `04895aa` y `d5a4b4e`) todavía describe a B2 como «PENDIENTE DE CIERRE FORMAL» y a su cierre de gobierno como candidato a auditoría. Es el riesgo R2 que el propio cierre de gobierno dejó registrado: la regla monotónica no admite otra transición sin otro incremento. Este documento es ese incremento.

## 2. Contrato de R2-A

### 2.1 De dónde sale

| Fuente | Regla |
|---|---|
| [Cierre de gobierno](../evidencia-sbx-b2-cierre-gobierno/F35SBXB_B2_Cierre_Gobierno.md), §2.3 y R2 | El cierre formal lo acredita la auditoría sobre el ancla del cierre de gobierno. Su registro en el gobierno corresponde al incremento sucesor que el equipo autorice, con su propio delta cerrado |
| [Contrato de B2](../evidencia-sbx-b2/F35SBXB_B2_Contrato_Verificacion.md), §2.3 | Una transición de gobierno es única y monotónica: un solo commit con un solo padre la introduce en las dos rutas a la vez, todo descendiente la conserva y ninguna otra la reintroduce. «Una transición de gobierno distinta en el futuro solo podrá autorizarla otro incremento sucesor, con su propio contrato y su propia ancla» |
| [B2-FREEZE](../evidencia-sbx-b2-freeze/F35SBXB_B2_Freeze.md), §8 y R3 | El gobierno está en su nivel A: el incremento que lo cambie aporta su propio gate sucesor |
| [B0](../evidencia-sbx-b/F35SBXB_B0_Sucesion_de_Gates.md), DH-B13 | Un gate congelado que no reconoce una evolución autorizada falla por clase A. Esa falla no se ignora: obliga a la evaluación sucesora completa sobre HEAD, sin reducir ni reinterpretar sus criterios |

### 2.2 Estado antiguo y estado nuevo

| | Antes (gobierno de `04895aa`) | Después (gobierno de R2-A) |
|---|---|---|
| B2, en la sección «Estado vigente» | IMPLEMENTADA, CORREGIDA, REAUDITADA, CONGELADA E INTEGRADA TÉCNICAMENTE, PENDIENTE DE CIERRE FORMAL | CERRADA, CONGELADA E INTEGRADA |
| Incremento B2, en la frase de commits | IMPLEMENTADO, CORREGIDO, REAUDITADO, CONGELADO E INTEGRADO TÉCNICAMENTE en `develop` y `main` (ancla `8969424`, merges `eb02c2d` y `5bf4f4e`), y PENDIENTE DE CIERRE FORMAL | CERRADO, CONGELADO E INTEGRADO en `develop` y `main` (la misma ancla y los mismos merges) |
| Cierre de gobierno | IMPLEMENTADO y CANDIDATO A AUDITORÍA INDEPENDIENTE, en su rama; su integración requiere autorización | AUDITADO E INTEGRADO en `develop` y `main` (ancla `363273e`, merges `04895aa` y `d5a4b4e`) |
| Cierre formal | No registrado | Registrado en [`evidencia-sbx-b2-cierre-formal`](F35SBXB_B2_Cierre_Formal.md) |
| Cabecera de `docs/PROGRESS.md` | 2026-10-14; «B2 INTEGRADA TÉCNICAMENTE Y PENDIENTE DE CIERRE FORMAL» | 2026-10-18; «B2 CERRADA E INTEGRADA» |
| Los trece estados, F35-SBX-B INICIADA y el resto del gobierno | Sin cambios | Sin cambios |

La forma canónica es la que el gobierno ya usa para B1: «B1 (gate sucesor sobre HEAD) CERRADA, CONGELADA E INTEGRADA» y «su incremento B1 … está CERRADO, CONGELADO E INTEGRADO en `develop` y `main` (ancla …, cierre …), registrado en …». El nuevo texto de B2 la sigue palabra por palabra y conserva sus anclas y merges. No dice nada del estado de auditoría de R2-A: ese estado lo registra la auditoría fuera del repositorio, y así el texto sigue siendo cierto después de integrarse.

### 2.3 Qué significa el cierre y qué no

El cierre significa solo esto: **F35-SBX-B2 completó y cerró su alcance académico y sintético autorizado**, el almacén efímero aislado por organización sintética, con su freeze, su gate sucesor, el cierre de la capa sucesora y el cierre de gobierno auditados e integrados.

El cierre no cambia nada fuera de ese alcance:

- no es un permiso de uso productivo;
- no sustituye la revisión institucional, legal ni de privacidad;
- no se validó con candidatos reales ni demuestra eficacia institucional;
- no da paso a datos reales ni a IA de selección de personas;
- no abre F36 ni ninguna fase productiva.

Se conservan:

| Estado | Valor |
|---|---|
| G0 real | NO APROBADA |
| G0-02, G0-03 y G0-12 | PENDIENTE EXTERNO |
| G0-09 y G0-14 | CUMPLIDO |
| G0-SBX | APROBADA CON RESTRICCIONES |
| ADR-005 | PROPUESTA, con la aprobación interna del equipo registrada |
| F35 productiva, F36–F40 y alcance C | BLOQUEADOS |
| Datos reales | PROHIBIDOS |
| F35-SBX-B | INICIADA (B1 y B2 cerradas; la fase no se cierra con R2-A) |
| RF-23 | Decisión final humana del Aprobador/Dirección |
| RF-29 | Experimental e informativo |

### 2.4 Invariantes

1. Solo cambian `CLAUDE.md` y `docs/PROGRESS.md`, mediante la transición única de §3.3, y se añaden las tres rutas de esta capa.
2. Las capas congeladas, de B1 a B2-GOVERNMENT-CLOSURE, conservan sus bytes y su historia desde sus anclas.
3. La transición es la cuarta etapa de la cadena monotónica de gobierno: blob de B1 → blob de B2 → blob del cierre de gobierno → blob del cierre formal.
4. Los trece estados de gobierno y «F35-SBX-B INICIADA» no cambian.
5. No hay runtime, CI, dependencias, dataset, migraciones, endpoints ni capacidades nuevas.
6. La evaluación vigente se conserva: el gate del cierre de gobierno, B2-SUCCESSOR-FREEZE y el gate de B2 se ejecutan intactos sobre HEAD y su falla de clase A se clasifica con exactitud.

### 2.5 Delta permitido y criterios de aceptación

| Ruta | Estado frente a `04895aa` | Contenido |
|---|---|---|
| `docs/academico/evidencia-sbx-b2-cierre-formal/F35SBXB_B2_Cierre_Formal.md` | A | Este documento |
| `docs/academico/tools/f35sbxb2_cierre_formal/validate_f35sbxb2_cierre_formal.py` | A | Gate sucesor sobre HEAD |
| `docs/academico/tools/f35sbxb2_cierre_formal/test_f35sbxb2_cierre_formal.py` | A | Batería CF01..CF36 |
| `CLAUDE.md`, `docs/PROGRESS.md` | M | Solo mediante la transición de §3.3 |

R2-A queda aceptado como candidato si se cumple todo:

- el gate da 14/0 sobre la rama, y sobre los merges `--no-ff` en `develop` y `main` (CF02);
- la batería da 36/36, con todos los negativos rechazados;
- los gates anclados siguen en verde: B2-GOVERNMENT-CLOSURE 13/0 sobre `363273e`, B2-SUCCESSOR-FREEZE 12/0, el sucesor 7/0, B2-FREEZE 10/0, B2 119/0, B1 159/0 y B1-FREEZE 14/0, con SBX 18/18;
- cada gate congelado que falla sobre HEAD falla solo por la clase A prevista (§3.5), sin falla nueva;
- `validate.py`, `--cierre-f29`, F29, F32, F33, F34 y F34A siguen en verde, y F34E en su 247/1 histórico;
- enlaces, MANIFEST y evidencias sin discrepancias, y `git diff --check` limpio.

### 2.6 Amenazas de reapertura y de sobredeclaración

| Amenaza | Qué la rechaza | Caso |
|---|---|---|
| Volver a «PENDIENTE DE CIERRE FORMAL» | GOV (regla 3 y regla 4), SEM (declaración canónica ausente y estado pendiente presente), ALC y GCL | CF06 |
| Reabrir B2 con otro texto | GOV y SEM (declaración canónica ausente y reapertura) | CF07 |
| Cambiar el gobierno otra vez, aunque se restaure | GOV | CF04, CF05 |
| Transición fuera de un commit único, con otras rutas o en un merge | GOV | CF09–CF11 |
| Historia reconstruida o sin la integración del cierre de gobierno | GOV, CTX y FRZ | CF08, CF35 |
| Alterar una capa congelada | INT, más SUC, MAT, GCL o ALC según la capa | CF12–CF16 |
| Tocar dataset, runtime o dependencias | MAT, ALC y GCL, más SUC cuando la ruta es visible | CF17–CF20 |
| Intento de declarar G0 real aprobada | GOV, SEM, MAT y GCL | CF28 |
| Intento de quitar las restricciones de G0-SBX | GOV, SEM, MAT y GCL | CF29 |
| Intento de aprobar ADR-005 | GOV, SEM, MAT y GCL | CF30 |
| Intento de desbloquear F36–F40 | GOV, SEM, MAT y GCL | CF31 |
| Intento de habilitar el alcance C | GOV, SEM, MAT y GCL | CF32 |
| Intento de permitir datos reales | GOV, SEM, MAT y GCL | CF33 |
| Intento de habilitar scoring, recomendación y selección automática | GOV, SEM, MAT y GCL | CF34 |
| Entorno de Git hostil o incompleto | ENT, FLG y fallo cerrado | CF21–CF24 |

### 2.7 Por qué es un cierre terminal

- **No hay R2-B.** El texto nuevo describe hechos que no cambian al integrarse R2-A: B2 cerrada, su cierre de gobierno auditado e integrado y el lugar de su registro. No menciona el estado de auditoría de R2-A, así que no queda nada que registrar después.
- **No hay otro freeze.** El ancla de esta capa es el commit que la completa, que el gate deriva y la auditoría registra fuera, como en las capas anteriores. Un manifiesto no acreditaría nada por sí mismo: las anclas registradas en el gate y los objetos Git verificados son la fuente de verdad.
- **El ciclo de vida de B2 termina aquí.** El gate admite «cerrada» y rechaza la reapertura y cualquier estado posterior («aprobada», «productiva», «publicada» o «desplegada»). Un incremento futuro de otra fase que cambie el gobierno producirá una falla de clase A en este gate y aportará su propio gate sucesor, como prevé DH-B13; no es una capa más de B2.

El único mecanismo nuevo es el gate sucesor de §3.4, que la propia sucesión exige: todos los gates congelados fallan sobre un HEAD con otro gobierno, y el contrato pide que el incremento que lo cambie aporte su gate sobre HEAD.

## 3. Diseño

### 3.1 Rama, base y archivos

- **Base:** `develop` integrado, `04895aacd96f0f03dde84e10a558bbdf26f050c6`, como los incrementos anteriores.
- **Rama:** `chore/f35-sbx-b2-r2a-final-closure`, en un worktree hermano del checkout del equipo, que no se toca.
- **Archivos:** los de §2.5. Nada más.

### 3.2 Commits

1. **RED.** Este diseño y la batería, sin gate: la batería falla entera, y el gobierno sigue «PENDIENTE DE CIERRE FORMAL».
2. **Transición de gobierno.** Un solo padre; cambia exactamente `CLAUDE.md` y `docs/PROGRESS.md`, aplicando el delta de §3.3.
3. **GREEN.** El gate, que registra el commit de la transición (ya existe: no hay autorreferencia), y los resultados de §5. Es el commit que completa la capa.

### 3.3 Delta de gobierno

`B2_CLOSURE_GOVERNANCE_BLOB` es el blob de `d346597` (`dcf584c28f8b0f044e3ab9fc11cc117fc17e8a8c` en `CLAUDE.md` y `49390335d47a13468f0a5b4017cf6b5723ad8ecb` en `docs/PROGRESS.md`). `B2_FORMAL_GOVERNANCE_BLOB` resulta de aplicarle una lista cerrada de reemplazos literales, cada bloque antiguo presente exactamente una vez. El gate la calcula por su cuenta. Los bloques nuevos de `docs/PROGRESS.md` difieren de los de `CLAUDE.md` solo en la ruta relativa de los enlaces.

```text
CLAUDE.md, reemplazo 1 (y docs/PROGRESS.md, reemplazo 3)
  antes:   F35-SBX-B INICIADA solo como sandbox sintético: B1 (gate sucesor sobre HEAD) CERRADA, CONGELADA E INTEGRADA; B2 (almacén efímero SQLite `:memory:` por organización sintética) IMPLEMENTADA, CORREGIDA, REAUDITADA, CONGELADA E INTEGRADA TÉCNICAMENTE, PENDIENTE DE CIERRE FORMAL, sin pipeline funcional ni ML.
  después: F35-SBX-B INICIADA solo como sandbox sintético: B1 (gate sucesor sobre HEAD) CERRADA, CONGELADA E INTEGRADA; B2 (almacén efímero SQLite `:memory:` por organización sintética) CERRADA, CONGELADA E INTEGRADA, sin pipeline funcional ni ML.

CLAUDE.md, reemplazo 2 (y docs/PROGRESS.md, reemplazo 4, con enlaces relativos a docs/)
  antes:   F35-SBX-B INICIADA: su incremento B1 (gate sucesor sobre HEAD) está CERRADO, CONGELADO E INTEGRADO en `develop` y `main` (ancla auditada `8e94a60274fe39ebda3e9961bc58036b389dfc00`, cierre `3d9b78307684a0dfb093e31d28fde290b2b1cb4a`), registrado en [`evidencia-sbx-b-freeze`](docs/academico/evidencia-sbx-b-freeze/F35SBXB_B1_Freeze.md); su incremento B2 (almacén efímero aislado) está IMPLEMENTADO, CORREGIDO, REAUDITADO, CONGELADO E INTEGRADO TÉCNICAMENTE en `develop` y `main` (ancla aprobada `89694244b81b0bd84dbe6ae5d04b5c7a198bafef`, merges `eb02c2d84335347c52b81a76c1e73dc30b93e88a` y `5bf4f4e58c3860be4c5d9f94d1c4b5a031570d33`), registrado en [`evidencia-sbx-b2`](docs/academico/evidencia-sbx-b2/README.md), y está PENDIENTE DE CIERRE FORMAL: su incremento de cierre de gobierno está IMPLEMENTADO y es CANDIDATO A AUDITORÍA INDEPENDIENTE, en `chore/f35-sbx-b2-government-closure` y registrado en [`evidencia-sbx-b2-cierre-gobierno`](docs/academico/evidencia-sbx-b2-cierre-gobierno/F35SBXB_B2_Cierre_Gobierno.md). La integración y la publicación de ese incremento requieren autorización explícita del equipo.
  después: F35-SBX-B INICIADA: su incremento B1 (gate sucesor sobre HEAD) está CERRADO, CONGELADO E INTEGRADO en `develop` y `main` (ancla auditada `8e94a60274fe39ebda3e9961bc58036b389dfc00`, cierre `3d9b78307684a0dfb093e31d28fde290b2b1cb4a`), registrado en [`evidencia-sbx-b-freeze`](docs/academico/evidencia-sbx-b-freeze/F35SBXB_B1_Freeze.md); su incremento B2 (almacén efímero aislado) está CERRADO, CONGELADO E INTEGRADO en `develop` y `main` (ancla aprobada `89694244b81b0bd84dbe6ae5d04b5c7a198bafef`, merges `eb02c2d84335347c52b81a76c1e73dc30b93e88a` y `5bf4f4e58c3860be4c5d9f94d1c4b5a031570d33`), registrado en [`evidencia-sbx-b2`](docs/academico/evidencia-sbx-b2/README.md); su cierre de gobierno está AUDITADO E INTEGRADO en `develop` y `main` (ancla aprobada `363273ead5794ea7a2dba74c011a0efd6d59e906`, merges `04895aacd96f0f03dde84e10a558bbdf26f050c6` y `d5a4b4e7c4ba01c1b923d215a51f0d2f22c8f163`), registrado en [`evidencia-sbx-b2-cierre-gobierno`](docs/academico/evidencia-sbx-b2-cierre-gobierno/F35SBXB_B2_Cierre_Gobierno.md); su cierre formal está registrado en [`evidencia-sbx-b2-cierre-formal`](docs/academico/evidencia-sbx-b2-cierre-formal/F35SBXB_B2_Cierre_Formal.md).

docs/PROGRESS.md, reemplazo 1
  antes:   Última actualización: 2026-10-14 (F34E CERRADA; G0 real NO APROBADA; G0-SBX APROBADA CON RESTRICCIONES; F35-SBX sintética HABILITADA; F35-SBX-A CERRADA E INTEGRADA; B0 CERRADA E INTEGRADA; F35-SBX-B INICIADA: B1 CERRADA E INTEGRADA, B2 INTEGRADA TÉCNICAMENTE Y PENDIENTE DE CIERRE FORMAL).
  después: Última actualización: 2026-10-18 (F34E CERRADA; G0 real NO APROBADA; G0-SBX APROBADA CON RESTRICCIONES; F35-SBX sintética HABILITADA; F35-SBX-A CERRADA E INTEGRADA; B0 CERRADA E INTEGRADA; F35-SBX-B INICIADA: B1 CERRADA E INTEGRADA, B2 CERRADA E INTEGRADA).

docs/PROGRESS.md, reemplazo 2
  antes:   El 14/10/2026 pasó a B2 integrada técnicamente y pendiente de cierre formal, con su incremento de cierre de gobierno candidato a auditoría independiente.
  después: El 14/10/2026 pasó a B2 integrada técnicamente y pendiente de cierre formal, con su incremento de cierre de gobierno candidato a auditoría independiente. El 18/10/2026 pasó a B2 cerrada e integrada, con su cierre de gobierno auditado e integrado y su cierre formal registrado.
```

`B2_FORMAL_TRANSITION` es el commit que introduce, en las dos rutas a la vez, el paso `B2_CLOSURE_GOVERNANCE_BLOB` → `B2_FORMAL_GOVERNANCE_BLOB`. Se registra en el gate después de que exista, en el commit GREEN, nunca en el propio commit.

### 3.4 Gate sucesor

Ubicación: `docs/academico/tools/f35sbxb2_cierre_formal/validate_f35sbxb2_cierre_formal.py`. Solo biblioteca estándar, sin red, aislado (`python -I`, al que se relanza solo), con objetos Git verificados recalculando su identificador y con fallo cerrado ante cualquier error, salida incompleta o estado no evaluable.

| ID | Comprueba |
|---|---|
| ENT | Intérprete aislado y sin `PYTHONPATH`, `PYTHONHOME` ni `PYTHONUSERBASE`. Ninguna variable de Git que redirija el repositorio, el índice o los objetos. Git sobre el repositorio del gate, con historia completa y sin injertos ni objetos de reemplazo |
| CTX | Rama `chore/f35-sbx-b2-r2a-final-closure`, `develop` o `main`, y el merge `04895aa` como ancestro de HEAD |
| ANC | Anclas registradas como commits íntegros y en cadena: `8e94a60` → `3d9b783` → `72e86c5` → `12c1c36` → `2472fd6` → `9961d2d` → `9d6fb15` → `8969424` → `eb02c2d` → `d346597` → `363273e` → `04895aa`. Los merges `eb02c2d` (padres `72e86c5` y `8969424`, árbol de `8969424`) y `04895aa` (padres `eb02c2d` y `363273e`, árbol de `363273e`). Los blobs de gobierno de B1, de B2 y del cierre de gobierno son los registrados |
| HIS | El gate del cierre de gobierno, con los bytes de su blob en `363273e`, ejecutado anclado sobre `363273e` en un clon temporal sin remoto: código 0, 13/0, FRZ deriva `363273e` y GOV deriva `d346597` |
| GCL | El mismo gate sobre HEAD, verificado contra su blob: solo su clase A exacta (§3.5) |
| SUC | B2-SUCCESSOR-FREEZE sobre HEAD, verificado contra su blob: solo VIG y ALC. Las violaciones visibles de ALC solo nombran rutas del cierre de gobierno y de esta capa, en los tres planos. FRZ deriva `8969424`. VIG informa que el sucesor solo falla en ALC, CON o MAT y las mismas reglas del gate de B2 que observa MAT |
| MAT | El gate de B2, verificado contra su blob en el candidato, ejecutado sin cambios sobre HEAD. Solo puede fallar por lo que predice el estado observado: CTX solo en la rama de este incremento, SCP por las 17 rutas posteriores al candidato en tres planos (51), B1F y DYN (P25) por la historia de gobierno, que el gate cuenta por su cuenta, y GOV por el contenido del gobierno y por el ciclo de vida de B2 («integrada», «congelada» o «cerrada»). Total de comprobaciones: 119 |
| INT | Integridad propia de las capas congeladas, cada una desde su ancla: B1, B1-FREEZE, B2, B2-FREEZE, el sucesor, B2-SUCCESSOR-FREEZE y B2-GOVERNMENT-CLOSURE. En cada commit posterior a cada ancla que lleva a HEAD, merges incluidos, y en HEAD, el índice y el disco |
| FLG | Ningún flag en el índice |
| GOV | Transición única y monotónica en cuatro etapas (§3.6), en cada commit desde `8e94a60`; transición derivada igual a la registrada; estado efectivo en HEAD, índice y disco |
| SEM | Semántica del gobierno vigente y del documento de esta capa con las piezas verificadas del gate de B1, con el ciclo de vida de B2 cerrado (§3.7) |
| ALC | Alcance exacto frente a `04895aa`: HEAD, el índice y el árbol de trabajo solo añaden las tres rutas de la capa y modifican las dos de gobierno; ningún archivo sin seguimiento; carpetas de la capa exactas |
| FRZ | Nivel B: un único commit posterior a `04895aa` completa la capa y HEAD desciende de él. Desde él, cada commit, HEAD, el índice y el disco tienen exactamente sus archivos. La línea INFO informa ese commit |
| DEP | Los archivos Python de la capa solo importan la biblioteca estándar autorizada. La única ejecución dinámica es la carga del gate de B1 desde los bytes de su blob verificado en `8e94a60` |

HIS se ejecuta en paralelo, en su propio clon. GCL, SUC y MAT se ejecutan uno tras otro sobre el repositorio, que solo se lee.

### 3.5 Clase A, sin ocultar nada

Sobre un HEAD válido, los gates congelados fallan, y deben fallar. Esto se midió antes de escribir el gate, en un clon desechable con una capa de prueba y la transición de §3.3 aplicada, en la rama, tras el merge `--no-ff` en `develop` y tras el de `develop` en `main`:

| Gate congelado sobre HEAD | Falla observada | Causa |
|---|---|---|
| B2-GOVERNMENT-CLOSURE | CTX (solo en la rama), SUC, MAT, GOV, SEM y ALC: 7/6 en la rama, 8/5 en `develop` y `main` | Rama nueva; rutas nuevas visibles en B2-SUCCESSOR-FREEZE y en su gate de B2; cuarto blob de gobierno; el gobierno ya no dice «PENDIENTE DE CIERRE FORMAL» y declara «b2 cerrada» |
| B2-SUCCESSOR-FREEZE | VIG y ALC (10/2) | Compone el sucesor; rutas nuevas |
| B2 | CTX (solo en la rama), B1F, SCP 51, DYN (P25) y GOV: 113/6 en la rama, 114/5 en `develop` y `main` | Rama nueva; tres rutas nuevas; blob de gobierno distinto del suyo y «b2 cerrada», que su vocabulario rechaza |

Ninguna se oculta. GCL ejecuta el gate del cierre de gobierno intacto y exige que cada regla en falla sea la prevista, con su recuento y sus violaciones visibles:

- **CTX:** solo `rama no permitida` con el nombre de esta rama, y solo en ella.
- **SUC:** una violación, el ALC de B2-SUCCESSOR-FREEZE con las rutas que ve SUC; la línea INFO, igual que la que observa SUC.
- **MAT:** las que da su predicción frente a la salida del gate de B2 que observa MAT: CTX material solo en la rama, SCP 51 frente a 42 y GOV con «b2 cerrada».
- **GOV:** la regla 3 en cada commit posterior a `d346597` sin su blob, en el orden topológico, y las seis del estado efectivo.
- **SEM:** tres violaciones: «PENDIENTE DE CIERRE FORMAL» ausente en cada ruta y «b2 cerrada» en `docs/PROGRESS.md`.
- **ALC:** una violación por plano con exactamente las tres rutas de esta capa.
- **INFO:** transición `d346597` derivada y registrada, capa completada en `363273e`, B2-SUCCESSOR-FREEZE anclado en 12/0.
- **El resto** (ENT, ANC, HIS, INT, FLG, FRZ y DEP del cierre de gobierno) tiene que pasar.

Lo que esas fallas enmascaran se repone con reglas propias: MAT y SUC directos, INT con la capa del cierre de gobierno, GOV con la cuarta etapa y SEM con el ciclo de vida cerrado.

### 3.6 GOV: cuatro etapas

Para cada commit `C` de la ascendencia de HEAD que desciende de `8e94a60`, merges incluidos, lo admitido depende solo de su ascendencia:

1. **Antes de `12c1c36`, o si `C` no desciende de él:** el blob histórico de B1.
2. **Desde `12c1c36` y hasta `d346597`:** el blob de B2.
3. **Desde `d346597` y hasta la transición del cierre formal:** el blob del cierre de gobierno.
4. **En la transición del cierre formal y en todo descendiente:** `B2_FORMAL_GOVERNANCE_BLOB`.

Además:

- cada blob lo introduce solo su transición, en las dos rutas a la vez;
- la transición del cierre formal tiene un solo padre, con el blob del cierre de gobierno, desciende de `04895aa` y cambia exactamente las dos rutas;
- la transición derivada coincide con la registrada;
- HEAD, el índice y el disco tienen el blob del cierre formal.

Modificar y restaurar, volver al blob del cierre de gobierno, un quinto blob, una transición en un merge, en una sola ruta o que cambie otras rutas fallan. Un merge `--no-ff` legítimo en `develop` y en `main` desciende de la transición y lleva el blob del cierre formal: pasa.

### 3.7 SEM: ciclo de vida cerrado

SEM carga el gate de B1 desde los bytes de su blob en `8e94a60`, verificados, como el gate del cierre de gobierno. En el gobierno de HEAD comprueba:

- una única sección «Estado vigente F34E», con los trece estados exactos;
- F35-SBX-B solo INICIADA;
- la declaración canónica de B2 cerrada en la sección, y la ausencia de «PENDIENTE DE CIERRE FORMAL» en ella y en la cabecera;
- ninguna reapertura ni estado de B2 posterior al cierre en la sección y la cabecera;
- ninguna declaración contradictoria ni afirmación positiva que habilite una capacidad prohibida, en lo vigente y en las líneas nuevas frente al blob del cierre de gobierno.

| Ciclo de vida de B2 | Cierre de gobierno (congelado) | Este gate |
|---|---|---|
| Implementada, congelada, integrada | Admitidos | Admitidos |
| Cerrada | Rechazada | Admitida |
| Pendiente de cierre, reabierta, abierta, en desarrollo o no cerrada | Pendiente admitida | Rechazados |
| «Aprobada», «productiva», «publicada» o «desplegada» | Rechazados | Rechazados |

El documento de esta capa pasa las mismas comprobaciones (sin datos personales, afirmaciones positivas ni declaraciones contradictorias), y todos sus archivos son UTF-8 sin BOM, CR ni NUL.

### 3.8 Raíz de confianza y ancla de este incremento

- **Registradas en el gate,** porque ya existen: las anclas de §1.1, los merges `eb02c2d` y `04895aa`, la transición `d346597` y la transición del cierre formal (en el commit GREEN).
- **Derivada y registrada fuera:** el commit que completa la capa (nivel B), que el gate informa en la línea INFO de FRZ. Es el ancla de este incremento. La auditoría la anota y comprueba que el ancla derivada coincide; ningún archivo guarda su propio hash.
- **Los merges en `main`** (`5bf4f4e` y `d5a4b4e`) no son ancestros de esta rama, así que el gate no los verifica: se registran en §1 y en el gobierno, verificados con Git y con el CI, y CF02 prueba la integración `--no-ff` sobre `d5a4b4e`.

### 3.9 Lo que no cambia

- Los artefactos congelados de B1 a B2-GOVERNMENT-CLOSURE conservan sus bytes, y sus validadores no se ejecutan con constantes alteradas ni se reescriben.
- Los commits `8969424`, `363273e`, `eb02c2d`, `5bf4f4e`, `04895aa` y `d5a4b4e` no se tocan.
- G0, G0-SBX, ADR-005, F35 productiva, F36–F40, el alcance C y los datos reales conservan su estado (§2.3). RF-23 sigue siendo humana y RF-29 experimental. El baseline RF-01 a RF-27 no cambia.
- Este incremento es solo gobierno, documentación y QA. No añade datos, capacidades, endpoints, migraciones, dependencias ni runtime.

## 4. Pruebas

Cada caso trabaja en un clon desechable de HEAD, fuera del repositorio, con configuración de Git aislada, identidad ficticia y fechas fijas, y ejecuta el gate con `python -I`. Pasa si fallan exactamente las reglas esperadas y, cuando se indica, si las líneas FALLA o INFO contienen el motivo esperado. Las historias reconstruidas se crean con plumbing de Git sobre un índice propio, con el mismo contenido que HEAD.

| Caso | Escenario | Reglas en falla esperadas |
|---|---|---|
| CF01 | Estado válido; el ancla derivada es el commit que completa la capa | Ninguna (PASS) |
| CF02 | Merge `--no-ff` en `develop` (`04895aa`) y después de `develop` en `main` (`d5a4b4e`) | Ninguna en ambos |
| CF03 | Commit posterior sin cambios de contenido | Ninguna |
| CF04 | Quinto blob de gobierno tras la transición | GOV |
| CF05 | Modificar → restaurar el gobierno tras la transición | GOV |
| CF06 | Vuelta al gobierno del cierre de gobierno («PENDIENTE DE CIERRE FORMAL») | GOV, SEM, ALC y GCL |
| CF07 | Reapertura explícita de B2 en el gobierno | GOV y SEM |
| CF08 | Historia reconstruida con el mismo contenido | GOV (transición distinta de la registrada); FRZ informa otra ancla |
| CF09 | Transición que también cambia otra ruta | GOV |
| CF10 | Transición hecha en un merge | GOV |
| CF11 | Transición repartida en dos commits | GOV |
| CF12 | Gate del cierre de gobierno alterado y confirmado | INT, GCL y ALC |
| CF13 | Validador de B2-SUCCESSOR-FREEZE alterado y confirmado | INT, SUC, GCL y ALC |
| CF14 | Modificar → restaurar el documento del cierre de gobierno | INT y GCL |
| CF15 | Almacén de B2 alterado y confirmado | INT, ALC y GCL |
| CF16 | Rama lateral que altera y restaura el gate de B1, integrada con merge `--no-ff` | INT, MAT y GCL |
| CF17 | LF añadido a `evidence.csv` en el árbol de trabajo | MAT, SUC, ALC y GCL; MAT nombra SBX, FSY y PRE |
| CF18 | Artefacto ignorado en `public/build/` | MAT y GCL; MAT nombra FSY |
| CF19 | Dependencia (`composer.json`) modificada y confirmada | ALC, MAT, SUC y GCL |
| CF20 | Runtime (`routes/web.php`) modificado y confirmado | ALC, MAT y GCL |
| CF21 | Clon superficial | Todas salvo FLG y DEP (fallo cerrado) |
| CF22 | `GIT_DIR`, `GIT_WORK_TREE` y `GIT_INDEX_FILE` hacia un clon limpio | ENT |
| CF23 | Injertos sin efecto | ENT, SUC y GCL |
| CF24 | skip-worktree en `CLAUDE.md` con un cambio que `git status` no ve | GOV, FLG, MAT, SUC y GCL |
| CF25 | Documento de esta capa modificado tras completarla | FRZ |
| CF26 | Gate de esta capa alterado y confirmado: copia de confianza en el disco; copia alterada | FRZ y ALC; FRZ y DEP |
| CF27 | Dato personal ficticio en el documento de esta capa, confirmado | SEM y FRZ |
| CF28 | Intento de declarar G0 real aprobada | GOV, SEM, MAT y GCL |
| CF29 | Intento de quitar las restricciones de G0-SBX | GOV, SEM, MAT y GCL |
| CF30 | Intento de aprobar ADR-005 | GOV, SEM, MAT y GCL |
| CF31 | Intento de desbloquear F36–F40 | GOV, SEM, MAT y GCL |
| CF32 | Intento de habilitar el alcance C | GOV, SEM, MAT y GCL |
| CF33 | Intento de permitir datos reales | GOV, SEM, MAT y GCL |
| CF34 | Intento de habilitar scoring, recomendación y selección automática | GOV, SEM, MAT y GCL |
| CF35 | Cierre formal sin el merge de integración del cierre de gobierno (`04895aa`) | CTX, GOV y FRZ |
| CF36 | HEAD separado | CTX, MAT y GCL |

Propiedades que cubren:

- **CF01 a CF03:** los estados legítimos, incluidas las integraciones futuras `--no-ff`.
- **CF04 a CF11:** la monotonía de la transición, su registro y el ciclo de vida cerrado.
- **CF12 a CF16:** la integridad de las capas congeladas y su historia.
- **CF17 a CF20:** lo que solo la evaluación material y el alcance detectan.
- **CF21 a CF24:** el entorno de Git hostil o incompleto.
- **CF25 a CF27:** el nivel B de esta capa y su contenido.
- **CF28 a CF34:** que ninguna sobredeclaración pasa por el gobierno.
- **CF35 y CF36:** la historia y el contexto.

## 5. Resultados

### 5.1 Commits

| Commit | Padre | Contenido | Resultado |
|---|---|---|---|
| `c2c1f6e1d0cd8064e6aeab4ae27b53ce92452d6e` | `04895aa` | Diseño (§1 a §4) y batería CF01..CF36 (RED) | 0 casos correctos y 36 fallas, con 30 ejecuciones: el gate no existía, y CF06–CF11 y CF26 ni siquiera podían prepararse |
| `ddefb7dae00a7b57eb32c1046de634c0be2805de` | `c2c1f6e` | Transición de gobierno (§3.3): solo `CLAUDE.md` y `docs/PROGRESS.md` | `B2_FORMAL_TRANSITION`, registrada en el gate del commit siguiente |
| El que completa la capa (este) | `ddefb7d` | Gate, correcciones de redacción de este documento (§5.2) y estos resultados (GREEN) | Gate 14/0; batería 36/36 |

Ese tercer commit es el ancla de nivel B de este incremento: lo informa la línea INFO de FRZ, y su hash no se guarda en ningún archivo.

### 5.2 GREEN y correcciones

Los resultados se midieron en clones temporales sin remoto. La batería y los controles de mutación, sobre commits desechables cuyo árbol solo difiere del de este commit en la cabecera de este documento y en esta sección 5; el gate y la regresión, sobre un commit desechable con el árbol de este commit.

- **Comprobación semántica previa de este documento: 9 afirmaciones positivas.** Antes de ejecutar el gate, las mismas piezas del gate de B1 que usa SEM encontraron nueve en el documento del commit RED. Eran falsos positivos de redacción: en §2.3, la negación quedaba lejos de la enumeración que negaba; en §2.6, cada fila «Intento de …» juntaba varias capacidades; y §2.7 y §3.7 enumeraban los estados rechazados sin citarlos. Se reescribieron esas frases sin tocar SEM (§2.3 como lista de negaciones, §2.6 con una fila por amenaza y los estados de §2.7 y §3.7 entre comillas latinas), y la comprobación dio 0 afirmaciones positivas y 0 declaraciones contradictorias.
- **Primeros casos de la batería: 3/4 (CF02, CF06, CF07 y CF35).** CF35 falló con GCL de más. El espejo de GOV del gate del cierre de gobierno tomaba por ajena a la clase A la regla 3 en los commits que no descienden de `04895aa`, cuando §3.5 la prevé en todo commit posterior a `d346597` sin su blob. En CF35 la capa se monta sobre `363273e` sin el merge `04895aa`, y GCL añadía su falla a las de CTX, GOV y FRZ, que son las que detectan esa historia. Se corrigió el gate, no la batería: el espejo sigue §3.5, y la exigencia de descender de `04895aa` queda en CTX, GOV y FRZ. CF35 y CF04 pasaron después.
- **Batería completa, repetida desde cero tras la corrección: 36/36,** con 38 ejecuciones del gate en seis tandas paralelas, y ninguna expectativa de RED corregida. La repetición completa de la batería sobre este commit se registra en el reporte de entrega.

### 5.3 Clase A observada sobre HEAD

Medida en la rama y comparada con la base `04895aa` (`develop`), en clones limpios sin remoto:

| Gate congelado sobre HEAD | Resultado | Fallas |
|---|---|---|
| B2-GOVERNMENT-CLOSURE | 7/6 (13/0 sobre la base) | La clase A de §3.5, exacta: CTX (solo la rama); SUC 1, el ALC de B2-SUCCESSOR-FREEZE con el gobierno y el documento de esta capa; MAT 3 (CTX material, SCP 51 frente a 42 y GOV con «b2 cerrada»); GOV 8, la regla 3 en `ddefb7d` y en el commit que completa la capa y las seis del estado efectivo; SEM 3, «PENDIENTE DE CIERRE FORMAL» ausente en cada ruta y «b2 cerrada» en `docs/PROGRESS.md`; ALC 3, las tres rutas de esta capa en cada plano |
| B2-SUCCESSOR-FREEZE | 10/2 (10/2) | VIG 5 y ALC 3, como sobre la base. VIG ve además CTX en la rama y SCP 51 en lugar de 42; ALC muestra el documento de esta capa. FRZ deriva `8969424` |
| Sucesor | 4/3 (4/3) | CON 1, MAT 2 y ALC 3, como sobre la base; MAT ve CTX en la rama y SCP 51 |
| B2-FREEZE | 6/4 (6/4) | HIS 6 (3 sobre la base: se suman `c2c1f6e`, `ddefb7d` y el commit que completa la capa), ARB 1, IDX 1 y DSK 2, solo por `CLAUDE.md` y `docs/PROGRESS.md` |
| B2 | 113/6 (114/5) | CTX (solo la rama); B1F 12 (9: los tres commits nuevos); SCP 51 (42: las tres rutas nuevas en tres planos); DYN 1 (P25); GOV 3, con «b2 cerrada» donde la base tiene «b2 integrada» |
| B1 | 105/54 (106/53) | GOV 1 y los 51 casos PB, idénticos a los de la base; SCP 75 (66: las tres rutas nuevas en tres planos); más CTX por el nombre de la rama |
| B1-FREEZE | 0/2 (0/2) | FRZ 27 (24: los tres commits nuevos, solo por `CLAUDE.md` y `docs/PROGRESS.md`) y B1, como sobre la base |

En `develop` y `main` CTX pasa (CF02). GCL clasifica exactamente la primera fila, SUC la segunda y MAT la quinta. Las demás se reponen con INT, GOV y SEM (§3.5).

### 5.4 Controles de mutación

La batería se ejecutó contra gates debilitados a propósito, en commits desechables. Cada mutación la detecta al menos un caso que falla:

| Mutación | Casos que la detectan |
|---|---|
| Sin GCL (el gate del cierre de gobierno no se ejecuta sobre HEAD) | CF14 y CF18, que pierden GCL |
| GOV sin comparar la transición derivada con la registrada | CF08, que pasa a PASS |
| SEM sin exigir el estado cerrado ni rechazar la reapertura o el estado pendiente | CF06 y CF07, que pierden SEM |
| Sin INT | CF14 y CF15, que pierden INT |
| MAT acepta cualquier salida del gate de B2 | CF17 y CF18, que pierden MAT |

### 5.5 Validación

| Comprobación | Resultado |
|---|---|
| `validate_f35sbxb2_cierre_formal.py` | 14/0, en unos 160 segundos sin otra carga. FRZ informa el commit que completa la capa; GOV deriva `ddefb7d`, igual a la registrada; HIS da 13/0, con el ancla derivada `363273e` y la transición `d346597`; GCL observa 7/6 con las reglas previstas; SUC, 10/2 con FRZ en `8969424`; MAT, 113/6 con SCP 51 de 51 previstas |
| `test_f35sbxb2_cierre_formal.py` | 36/36 (§5.2) |
| Gates anclados en clones limpios sin remoto | B2-GOVERNMENT-CLOSURE sobre `363273e`: 13/0, con FRZ en `363273e` y GOV en `d346597`. B2-SUCCESSOR-FREEZE sobre `8969424`: 12/0, con FRZ en `8969424`. Sucesor sobre `9d6fb15`: 7/0. B2-FREEZE sobre `9961d2d`: 10/0. B2 sobre `2472fd6`: 119/0, con la transición `12c1c36`. B1 sobre `8e94a60`: 159/0. B1-FREEZE sobre `3d9b783`: 14/0, con SBX-01..SBX-18 en 18/18 |
| `validate.py` y `validate.py --cierre-f29` | 0 fallas en ambos |
| `validate_f29.py`, `test_f32_safety.py`, `validate_f33.py` y `validate_f34.py` | 225/0, OK (10 pruebas), 451/0 y 403/0 |
| `validate_f34a.py` | 108/0 |
| `validate_f34e.py` | 247/1, igual que sobre `363273e` y las anclas anteriores: la falla histórica de la regla GIT. Su lista de rutas no autorizadas por DH-02 pasa de 26 a 29 (las tres de esta capa), sin que desaparezca ninguna, y el resto del mensaje no cambia. Criterios SBX: 18/18 |
| Enlaces relativos | 1130 en `docs/academico` (1125 en la base) y 1532 en todo el repositorio (1525), 0 rotos |
| MANIFEST y evidencias | 61 hashes y 0 discrepancias; 81 hashes de las evidencias de las prácticas 03, 05, 08 y 11, 0 discrepancias |
| `git diff --check` frente a `04895aa` | Limpio, y también frente a `363273e` y `2472fd6` |
| Delta frente a `04895aa` | Exactamente las tres rutas de la capa (A) y las dos de gobierno (M) |
| Gobierno de HEAD | Los trece estados y F35-SBX-B INICIADA, sin cambios; B2 con la declaración canónica de §3.3 en las dos rutas y sin «PENDIENTE DE CIERRE FORMAL» |

### 5.6 Sucesión vigente

| Gate | Papel | Dónde | Resultado en clon limpio |
|---|---|---|---|
| `validate_f35sbxb2_cierre_formal.py` | Gate sobre HEAD, en esta rama, `develop` y `main` | HEAD | 14/0 |
| `validate_f35sbxb2_cierre_gobierno.py` | Cierre de gobierno (dentro de HIS y GCL) | Anclado sobre `363273e` y HEAD | 13/0 y 7/6 (clase A) |
| `validate_f35sbxb2_sucesor_freeze.py` | Cierre de la capa sucesora (dentro de SUC) | Anclado sobre `8969424` y HEAD | 12/0 y 10/2 (clase A) |
| `validate_f35sbxb2.py` | Evaluación material (dentro de MAT) | HEAD | 113/6 (clase A) |
| `validate_f35sbxb2_sucesor.py`, `validate_f35sbxb2_freeze.py` | Capas anteriores de B2 | Anclados sobre `9d6fb15` y `9961d2d` | 7/0 y 10/0 |
| `validate_f35sbxb2.py` | Gate histórico de B2 | Anclado sobre `2472fd6` | 119/0 |
| `validate_f35sbxb.py`, `validate_f35sbxb_freeze.py` | Gates históricos de B1 y B1-FREEZE | Anclados sobre `8e94a60` y `3d9b783` | 159/0 y 14/0 |

Esta tabla supera la de §5.6 del cierre de gobierno, congelada en `363273e`.

### 5.7 Riesgos residuales

| # | Nivel | Riesgo | Tratamiento |
|---|---|---|---|
| R1 | INFO | Hasta que la auditoría independiente apruebe este incremento y el equipo autorice su integración, el registro del cierre en el gobierno de esta rama no vale: `develop` y `main` siguen diciendo «PENDIENTE DE CIERRE FORMAL» | Es el estado de todo candidato. El texto nuevo no menciona el estado de auditoría de R2-A, así que sigue siendo cierto después de integrarse (§2.7) |
| R2 | INFO | El ancla de nivel B solo autentica la capa si se registra fuera: una capa reconstruida con los mismos bytes en otra historia informa otra ancla (CF08) | La auditoría anota el commit que informa FRZ. No se añade otra capa de freeze |
| R3 | LOW | GCL, SUC y MAT solo ven las tres primeras violaciones de cada regla del gate que ejecutan | Los tres exigen recuentos exactos y predichos, y comparan una a una las violaciones visibles. El alcance exacto lo comprueba ALC y la integridad, INT |
| R4 | INFO | Cada ejecución tarda unos 160 segundos sin otra carga, y bastante más con varias en paralelo: el gate del cierre de gobierno anclado y sobre HEAD, B2-SUCCESSOR-FREEZE y el gate de B2 sobre HEAD, que a su vez ejecutan sus propias capas | Es el coste de conservar completa la evaluación vigente |
| R5 | INFO | En el checkout del equipo, MAT, SUC y GCL fallan por FSY si hay artefactos ignorados preexistentes (CF18) | Es deliberado: el checkout no se limpia y la certificación es en clon limpio |
| R6 | INFO | Cualquier cambio fuera de las rutas de este incremento hace fallar ALC y MAT, incluido uno legítimo de un incremento futuro, y cualquier cambio del gobierno hace fallar GOV | Es una falla de clase A para ese incremento, que aportará su propio gate sucesor (DH-B13). No es una capa más de B2 (§2.7) |
| R7 | INFO | Los merges en `main` (`5bf4f4e` y `d5a4b4e`) no son ancestros de esta rama, así que el gate no los verifica | Se registraron con Git y con el CI (§1.2), y CF02 prueba la integración `--no-ff` sobre `d5a4b4e` |

### 5.8 Próximo paso

Auditoría independiente de R2-A, que anota como ancla el commit que informa la línea INFO de FRZ. Hasta entonces:

- R2-A no se aprueba;
- B2 queda con el cierre formal preparado y pendiente de esa auditoría;
- no hay push, merge, tag ni release de este incremento.
