# F35-SBX-B — Cierre terminal

> **Estado: CIERRE TERMINAL IMPLEMENTADO / VALIDADO LOCALMENTE / CANDIDATO A AUDITORÍA INDEPENDIENTE.** Fecha: 22/10/2026. Rama `chore/f35-sbx-b-terminal-closure`, desde `develop` = `53c0eb55a8f64f5576c43c2bfb5dccf095e30412`.
>
> - Este documento fija los criterios del cierre terminal de F35-SBX-B, el contrato del incremento, su diseño y sus resultados. El gobierno de esta rama ya registra el cierre (§3.3).
> - El cierre solo vale en el alcance académico y sintético de F35-SBX, y solo cuando la auditoría independiente apruebe este incremento y el equipo autorice su integración. Hasta entonces, `develop` y `main` siguen diciendo «F35-SBX-B INICIADA».
> - F35-SBX sigue HABILITADA, sin cerrar. Este incremento no se autoaprueba: lo decide la auditoría independiente sobre su ancla.
>
> Las secciones 1 a 4 registran la reconstrucción, el contrato y el diseño, escritos antes de la transición de gobierno y del gate (commit RED `56783cb`). El commit que completa la capa solo los corrige donde la medición lo exigió, con su causa en §5.2. La sección 5 registra los resultados.

## 1. Punto de partida verificado

### 1.1 Anclas

| Ancla | Commit | Qué es |
|---|---|---|
| F35-SBX-A, commit E | `61f94e23fc30b00a848a4558830b6d65f81dff87` | Contrato, fixtures, manifest y validador de A, congelados |
| Cierre de B0 | `cc634eb9dcc5c0cc0d77b911bb3815182b8319c2` | Sucesión de gates, solo documentación |
| Base de B | `430f3f544c3542cabac8028a122c8a0c2a97390b` | `develop` al iniciar F35-SBX-B, con B0 integrada |
| B1 | `8e94a60274fe39ebda3e9961bc58036b389dfc00` | Ancla auditada de B1 |
| B1-FREEZE | `3d9b78307684a0dfb093e31d28fde290b2b1cb4a` | Cierre de B1 |
| Base de B2 | `72e86c5838984ea873d6dd56c179d94217b27317` | `develop` al crear la rama de B2 |
| Transición de gobierno de B2 | `12c1c36e409f81c048fccf7fcb3e6d2a2d5d40aa` | Blob de B1 → blob de B2 |
| Candidato de B2 | `2472fd6fadfc0634ec68cbcb76cfc9fbfe105194` | Almacén efímero reauditado |
| B2-FREEZE | `9961d2d65ed51a17c14aae5db0edb7d71c622c22` | Freeze del candidato |
| Sucesor | `9d6fb157bb818574217e3675da1849e8d1010962` | Gate sucesor (AF-M01) |
| B2-SUCCESSOR-FREEZE | `89694244b81b0bd84dbe6ae5d04b5c7a198bafef` | Cierre de la capa sucesora (AF-L02) |
| Integración de B2 | `eb02c2d84335347c52b81a76c1e73dc30b93e88a` (`develop`) y `5bf4f4e58c3860be4c5d9f94d1c4b5a031570d33` (`main`) | Merges `--no-ff` con el árbol de `8969424` |
| Transición del cierre de gobierno | `d346597e988d2f7f5d0d84e119709012b67715da` | Blob de B2 → blob del cierre de gobierno |
| B2-GOVERNMENT-CLOSURE | `363273ead5794ea7a2dba74c011a0efd6d59e906` | Cierre de gobierno de B2 |
| Integración del cierre de gobierno | `04895aacd96f0f03dde84e10a558bbdf26f050c6` (`develop`) y `d5a4b4e7c4ba01c1b923d215a51f0d2f22c8f163` (`main`) | Merges `--no-ff` |
| Transición del cierre formal | `ddefb7dae00a7b57eb32c1046de634c0be2805de` | Blob del cierre de gobierno → blob del cierre formal |
| R2-A | `ad193f9565bf23246fadb9f85fc0ceddf8ddf698` | Registro del cierre formal de B2 |
| Integración de R2-A | `ca36875938eca035c97205921ec5f9633381c571` (`develop`) y `8a00505c8a8adc6ebd125f3b30d3cf97dc03b475` (`main`) | Merges `--no-ff`; base de B3 |
| Transición de B3 | `fa5664a0a3660519744a32b320822ecc396b1619` | Blob del cierre formal → blob de B3 |
| B3 | `8d39d0e547821f7d6f63dc12b9c01803f985d797` | Ancla aprobada de B3. Árbol `d9f3d37ed6a1d8e1537b301c85ca8eb804a6c889` |
| Integración de B3 | `53c0eb55a8f64f5576c43c2bfb5dccf095e30412` (`develop`) y `9424f1ea2a1e25dd29e8cfc0b9f446b3118b7a9a` (`main`) | Merges `--no-ff`; base de este incremento |

### 1.2 Auditoría e integración de B3

| Hecho | Valor | Cómo se verificó |
|---|---|---|
| Veredicto de la auditoría independiente | «B3 APROBADO PARA INTEGRACIÓN», sobre el candidato `8d39d0e`, con árbol `d9f3d37e`, padre `fa5664a` y bases `ca36875` y `8a00505` | Registro de la auditoría, fuera del repositorio |
| Rama publicada | `origin/feature/f35-sbx-b3-deterministic-pipeline` = `8d39d0e` | `git fetch` y `git ls-remote` |
| Merge en `develop` | `53c0eb5`, con padres `ca36875` y `8d39d0e` | Objetos Git; `origin/develop` = `53c0eb5` |
| Merge en `main` | `9424f1e`, con padres `8a00505` y `53c0eb5` | Objetos Git; `origin/main` = `9424f1e` |
| Árboles | `8d39d0e`, `53c0eb5` y `9424f1e` tienen el árbol `d9f3d37e` | `git rev-parse <commit>^{tree}` |
| CI de `develop` | Workflow `tests`, run 64, id `39702724276`, SHA `53c0eb5`: `completed` / `success` | API pública de GitHub |
| CI de `main` | Workflow `tests`, run 65, id `39703376726`, SHA `9424f1e`: `completed` / `success` | API pública de GitHub |
| Gate de B3 | 19/0 sobre el candidato y sobre los dos merges; FRZ deriva `8d39d0e` | Ejecución en un clon limpio, con temporales propios |
| Etiquetas y releases | `v1.0.0-academic` → `9a946c2` y `v1.1.0-academic` → `634f354`; una sola release, `v1.1.0-academic`; ninguna nueva | `git ls-remote --tags` y API pública |

### 1.3 Qué falta

- El gobierno integrado (`CLAUDE.md` y `docs/PROGRESS.md` en `53c0eb5` y `9424f1e`) registra «F35-SBX-B INICIADA» y «B3 … IMPLEMENTADA».
- El bloque vigente de [`ACADEMIC_BASELINE.md`](../ACADEMIC_BASELINE.md) sigue diciendo «F35-SBX-B NO INICIADA» y conserva la frase de F35-SBX-A previa a su integración: «F35-SBX-A queda cerrada documentalmente en `feature/f35-sbx-synthetic-evidence-pipeline`, con publicación pendiente de regresión post-commits y CI».
- B3 dejó derivados los criterios del cierre posterior ([B3, §3.6](../evidencia-sbx-b3/F35SBXB_B3_Pipeline.md)). Tres de ellos le tocan a este incremento: el congelamiento de B, el registro del cierre en el gobierno con su transición y su gate sucesor, y el registro en `ACADEMIC_BASELINE.md`.

## 2. Criterios del cierre de F35-SBX-B

### 2.1 Fuentes

Solo se usan criterios que ya fijaron los contratos existentes. Ninguno se crea para este cierre.

| Fuente | Qué fija |
|---|---|
| [Criterios de A](../evidencia-sbx/F35SBX_Criterios_Cierre_y_Revocacion.md), §3 y §4 | B ejecuta el pipeline de doce pasos sobre los fixtures de A, con SQLite en memoria, solo inserción, auditoría encadenada, purga verificada, doble ejecución e informe con hashes y conteos, sin runtime ni dependencias nuevas. Los hechos REV-01..REV-14 revocan G0-SBX |
| [B0](../evidencia-sbx-b/F35SBXB_B0_Sucesion_de_Gates.md) | El ciclo de vida de B en el gobierno, con su apertura y su cierre (§3); DH-B01..DH-B13, con la sucesión normativa de SBX-01..SBX-18 (§3.1); conformidad en dos niveles, purga y TSBB-01..TSBB-13 (§5); `ACADEMIC_BASELINE.md` registra cierres (§5.6) |
| [B1](../evidencia-sbx-b/F35SBXB_B1_Gate_Sucesor.md), §3 y §5 | El cierre de B congela el gate y los artefactos de B con un commit identificado por la historia; después, la fase siguiente aporta su gate sucesor sobre HEAD |
| [Sucesor de B2](../evidencia-sbx-b2-sucesor/F35SBXB_B2_Sucesor.md), §2 (AF-M01) | El gate válido sobre HEAD ejecuta el gate vigente congelado, con su código verificado, y clasifica con exactitud su falla de clase A |
| [R2-A](../evidencia-sbx-b2-cierre-formal/F35SBXB_B2_Cierre_Formal.md), §2.3 y §2.7 | Forma canónica de un cierre en el gobierno, su alcance y su carácter terminal: sin otro freeze, con el ancla derivada por FRZ y registrada fuera |
| [B3](../evidencia-sbx-b3/F35SBXB_B3_Pipeline.md), §3.6 | Los criterios derivados del cierre posterior de F35-SBX-B |
| [Autorización de F35-SBX](../g0-sandbox/F34E_Autorizacion_F35_SBX.md) y [prohibiciones](../g0-sandbox/F34E_Prohibiciones.md) | El alcance sintético autorizado y la regla de revocación y bloqueo |

### 2.2 Matriz de criterios

| ID | Criterio | Evidencia | Estado |
|---|---|---|---|
| C01 | F35-SBX-A cerrada e integrada | Gobierno vigente, con su commit E; gate de A anclado en E sin fallas | CUMPLIDO |
| C02 | B0 cerrada e integrada | Gobierno vigente; cierre auditado `cc634eb` | CUMPLIDO |
| C03 | B1 cerrada, congelada e integrada | Ancla `8e94a60` y cierre `3d9b783`; gates de B1 y B1-FREEZE anclados en verde | CUMPLIDO |
| C04 | B2 cerrada, congelada e integrada | Ancla `8969424`, cierre de gobierno `363273e` y cierre formal `ad193f9`; gates anclados en verde | CUMPLIDO |
| C05 | B3 implementada, auditada e integrada | Ancla `8d39d0e`, veredicto de la auditoría, merges `53c0eb5` y `9424f1e`, CI 64 y 65 en verde (§1.2) | CUMPLIDO |
| C06 | Pipeline ejecutable de doce pasos | Regla PIP del gate de B3; B3, §2.2 y §6 | CUMPLIDO |
| C07 | Conformidad con el oráculo de A en dos niveles | Regla CNF del gate de B3, recalculada desde los fixtures de A y `evidence.csv` | CUMPLIDO |
| C08 | Determinismo y doble ejecución | Regla DET y pruebas PT02 y PT03 de B3; informe con SHA-256 `7efc00ee307c932955f2f3cc10b56dc08c14cd408c1fc7b43f612a712d174967` | CUMPLIDO |
| C09 | Informe canónico con hashes y conteos | Regla PIP: esquema cerrado, entradas verificadas y conteos por tenant | CUMPLIDO |
| C10 | Auditoría encadenada | Nivel 2 de CNF: cadenas de eventos, procedencia y auditoría recalculadas | CUMPLIDO |
| C11 | Purga verificable | Regla PUR y prueba PT06 de B3 | CUMPLIDO, con el riesgo LOW B3-AF-L01 (§2.4) |
| C12 | Fallo inyectado en cada paso | Regla FAL y pruebas PT19..PT30 de B3 | CUMPLIDO |
| C13 | TSBB-01..TSBB-13 con su prueba negativa | Pruebas PT08..PT18 y casos CB25..CB33 de B3 | CUMPLIDO |
| C14 | Sucesión de gates (DH-B13 y AF-M01) | Cada capa de B aporta su gate sucesor y clasifica la clase A del anterior | CUMPLIDO; este incremento aporta el suyo (§3.4) |
| C15 | SBX-01..SBX-18 | Recalculados sobre HEAD por el gate de B2 dentro de MAT; 18/18 en la integración de B3 | CUMPLIDO; se recalculan otra vez aquí |
| C16 | Invariantes de gobierno | Los trece estados del gobierno vigente | CUMPLIDO |
| C17 | Ninguna capacidad prohibida | SBX-05..SBX-07, esquema cerrado del informe, DEP y SEM de B3 | CUMPLIDO |
| C18 | G0-SBX vigente, sin hechos REV-01..REV-14 | SBX 18/18; `validate_f34e.py` solo con su falla histórica de alcance | CUMPLIDO |
| C19 | Congelamiento de B | B1, §5 | ESTE INCREMENTO (§3.9) |
| C20 | Registro del cierre en el gobierno, con su transición y su gate sucesor | B0, §3; DH-B13 | ESTE INCREMENTO (§3.3 y §3.4) |
| C21 | Registro del cierre en `ACADEMIC_BASELINE.md` | B0, §5.6; B1, §3 | ESTE INCREMENTO (§3.3) |

C01 a C18 están cumplidos con evidencia existente y C19 a C21 son el contenido de este incremento. No queda pendiente ningún requisito material fuera de ellos. CAP-33 y CAP-34 nunca fueron parte de B: siguen fuera, para una autorización aparte.

### 2.3 Qué significa el cierre y qué no

El cierre significa solo esto: **F35-SBX-B completó y cerró su alcance académico y sintético autorizado**, la ejecución determinista del pipeline de evidencia sintética de doce pasos, con B0, B1, B2 y B3 auditadas, integradas y congeladas, y su sucesión de gates completa.

El cierre de F35-SBX-B:

- no aprueba la G0 real ni sustituye su evidencia externa;
- no habilita la F35 productiva ni ninguna integración productiva;
- no habilita F36 ni ninguna fase posterior;
- no permite datos reales;
- no permite puntuar ni clasificar ni recomendar candidatos;
- no permite la selección automática;
- no habilita el alcance C;
- no habilita OCR ni parsing ni embeddings ni búsqueda semántica;
- no cambia RF-23, que sigue siendo la decisión final humana del Aprobador/Dirección;
- no cambia RF-29, que sigue experimental e informativo;
- mantiene F35-SBX HABILITADA, sin cerrarla.

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
| F35-SBX | HABILITADA |
| RF-23 | Decisión final humana del Aprobador/Dirección |
| RF-29 | Experimental e informativo |

### 2.4 Riesgos residuales aceptados

Los tres riesgos LOW de la auditoría independiente de B3 se registran tal como los clasificó, sin elevarlos ni rebajarlos. Este cierre no los corrige: hacerlo exigiría cambiar el código congelado de B3.

| ID | Severidad | Descripción | Evidencia y mitigación | Estado |
|---|---|---|---|---|
| B3-AF-L01 | LOW | Comprobante de purga no completamente independiente del pipeline: lo emite el propio pipeline y el gate no observa la memoria de su proceso, así que un pipeline alterado para forjar un comprobante coherente pasaría PUR | H4 y R5 de B3 y su caso CB25. Lo detectan la observación en el proceso (PT06, dentro de TSB) y el congelamiento del código (INT y FRZ) | Aceptado, no bloqueante |
| B3-AF-L02 | LOW | La comprobación CNF no demuestra por sí sola la unicidad global de `audit_id`: una duplicación con la cadena recalculada puede superar las comprobaciones locales | El candidato integrado conserva identificadores únicos y el almacén de B2 declara `audit_id` como clave primaria | Aceptado, no bloqueante |
| B3-R3 | LOW | Los diagnósticos de los gates históricos profundamente anidados pueden quedar truncados: cada línea FALLA muestra solo las tres primeras violaciones | R3 de B3. Este gate exige el recuento exacto de cada regla y compara las violaciones visibles con las que prevé la lógica verificada de cada gate | Aceptado, no bloqueante |

### 2.5 Invariantes

1. Solo cambian `CLAUDE.md`, `docs/PROGRESS.md` y `docs/academico/ACADEMIC_BASELINE.md`, mediante la transición única de §3.3, y se añaden las tres rutas de esta capa.
2. Las capas congeladas, de A a B3, conservan sus bytes y su historia desde sus anclas.
3. La transición es la sexta etapa de la cadena monotónica de gobierno: blob de B1 → blob de B2 → blob del cierre de gobierno → blob del cierre formal → blob de B3 → blob del cierre terminal.
4. Los trece estados de gobierno no cambian, y F35-SBX sigue HABILITADA.
5. No hay runtime, CI, dependencias, dataset, migraciones, endpoints ni capacidades nuevas.
6. La evaluación vigente se conserva: los gates de B3, de R2-A y de B2 se ejecutan intactos sobre HEAD y su falla de clase A se clasifica con exactitud.

### 2.6 Delta permitido y criterios de aceptación

| Ruta | Estado frente a `53c0eb5` | Contenido |
|---|---|---|
| `docs/academico/evidencia-sbx-b-cierre-terminal/F35SBXB_Cierre_Terminal.md` | A | Este documento |
| `docs/academico/tools/f35sbxb_cierre_terminal/validate_f35sbxb_cierre_terminal.py` | A | Gate sucesor sobre HEAD |
| `docs/academico/tools/f35sbxb_cierre_terminal/test_f35sbxb_cierre_terminal.py` | A | Batería CT01..CT36 |
| `CLAUDE.md`, `docs/PROGRESS.md`, `docs/academico/ACADEMIC_BASELINE.md` | M | Solo mediante la transición de §3.3 |

El cierre queda aceptado como candidato si se cumple todo:

- el gate da 15/0 sobre la rama y sobre los merges `--no-ff` en `develop` y `main` (CT02);
- la batería da 36/36, con todos los negativos rechazados;
- los gates anclados siguen en verde: B3 19/0 sobre `8d39d0e`, R2-A 14/0, B2-GOVERNMENT-CLOSURE 13/0, B2-SUCCESSOR-FREEZE 12/0, el sucesor 7/0, B2-FREEZE 10/0, B2 119/0, B1 159/0 y B1-FREEZE 14/0, con SBX 18/18, y el validador de A sin fallas en E;
- cada gate congelado que falla sobre HEAD falla solo por la clase A prevista (§3.5), sin falla nueva;
- `validate.py`, `--cierre-f29`, F29, F32, F33, F34 y F34A siguen en verde, y F34E en su 247/1 histórico;
- enlaces, MANIFEST y evidencias sin discrepancias, y `git diff --check` limpio.

### 2.7 Amenazas de sobredeclaración y de reapertura

| Amenaza | Qué la rechaza | Casos |
|---|---|---|
| Ataque: declarar B cerrada sin B3 | INT, B3G, R2A, MAT y ALC | CT08 |
| Ataque: sustituir B3 por otro commit con el mismo contenido | CTX, INT, FRZ, GOV y B3G | CT09 |
| Ataque: reconstruir la historia del cierre con el mismo contenido | GOV | CT10 |
| Ataque: alterar una capa congelada o un ancla histórica | INT, ALC y B3G, más R2A si la capa es anterior a B3 | CT11, CT29 |
| Ataque: ocultar o eliminar un riesgo LOW registrado | LOW y FRZ | CT12 |
| Ataque: habilitar F36 | GOV, SEM, B3G, R2A y MAT | CT13 |
| Ataque: cerrar F35-SBX | GOV, SEM, B3G, R2A y MAT | CT14 |
| Ataque: aprobar la G0 real | GOV, SEM, B3G, R2A y MAT | CT15 |
| Ataque: habilitar el alcance C | GOV, SEM, B3G, R2A y MAT | CT16 |
| Ataque: permitir datos reales | GOV, SEM, B3G, R2A y MAT | CT17 |
| Ataque: cambiar RF-23 | MAT, ALC, B3G y R2A | CT18 |
| Ataque: cambiar RF-29 | GOV y SEM | CT19 |
| Ataque: tocar archivos fuera del delta | ALC, MAT, B3G y R2A | CT20, CT21 |
| Ataque: reabrir B o volver al gobierno de B3 | GOV y SEM, más los gates congelados cuando cambian los trece estados o el alcance | CT06, CT07, CT35, CT36 |
| Ataque: cambiar el gobierno otra vez o fuera de una transición única | GOV | CT04, CT05, CT25, CT26 |
| Ataque: afirmar una capacidad prohibida o quitar un límite del cierre en este documento | SEM y FRZ | CT30, CT31 |
| Ataque: código del cierre con dependencias o ejecución dinámica | DEP y FRZ | CT27, CT28 |
| Ataque: entorno de Git hostil o incompleto | ENT, CTX, FLG y fallo cerrado, más B3G, R2A y MAT cuando el gate congelado también lo rechaza | CT22..CT24, CT32..CT34 |

### 2.8 Por qué es un cierre terminal

- **No hay otro registro de B.** El texto nuevo del gobierno describe hechos que no cambian al integrarse este incremento. No menciona su estado de auditoría, así que no queda nada que registrar después.
- **No hay otro freeze.** El ancla de esta capa es el commit que la completa, que FRZ deriva y la auditoría registra fuera, como en R2-A. INT congela B1, B2 y B3 desde sus anclas. Un manifiesto no acreditaría nada por sí mismo: las anclas registradas en el gate y los objetos Git verificados son la fuente de verdad.
- **Este gate es el gate de B congelado** (B1, §5). Después de B se ejecuta anclado sobre su ancla, y la fase siguiente que el equipo autorice aporta su propio gate sucesor sobre HEAD, que verifica la integridad de B y recalcula SBX-01..SBX-18. Eso no autoriza F36 ni ninguna otra fase.
- **F35-SBX sigue HABILITADA.** Su cierre exige otra decisión del equipo y otro incremento.

## 3. Diseño

### 3.1 Rama, base y archivos

- **Base:** `develop` integrado, `53c0eb55a8f64f5576c43c2bfb5dccf095e30412`.
- **Rama:** `chore/f35-sbx-b-terminal-closure`, en un worktree hermano del checkout del equipo, que no se toca.
- **Archivos:** los de §2.6. Nada más.

### 3.2 Commits

1. **RED.** Este documento y la batería, sin gate: la batería falla entera, y el gobierno sigue diciendo «F35-SBX-B INICIADA».
2. **Transición de gobierno.** Un solo padre; cambia exactamente las tres rutas de gobierno, aplicando el delta de §3.3.
3. **GREEN.** El gate, que registra el commit de la transición (ya existe: no hay autorreferencia), y los resultados de §5. Es el commit que completa la capa y su ancla.

### 3.3 Delta de gobierno

`TC_GOVERNANCE_BLOB` resulta de aplicar una lista cerrada de reemplazos literales, cada bloque antiguo presente exactamente una vez, al blob de B3 (`8e908661b96a557d078d0036a41e319b2a3bb76c` en `CLAUDE.md` y `4146a9d331f2d3f6240aedd599eb0238c578f761` en `docs/PROGRESS.md`) y al de `ACADEMIC_BASELINE.md` (`dccdf8925f3dbba6ca14c5f4f4d74bd6276496cb`, sin cambios desde el cierre de F35-SBX-A). El gate lo calcula por su cuenta. Los bloques de `docs/PROGRESS.md` difieren de los de `CLAUDE.md` solo en la ruta relativa de los enlaces.

```text
CLAUDE.md y docs/PROGRESS.md, la frase del estado vigente
  antes:   F35-SBX-B INICIADA solo como sandbox sintético: B1 (…) CERRADA, CONGELADA E INTEGRADA; B2 (…) CERRADA, CONGELADA E INTEGRADA; B3 (pipeline determinista de doce pasos sobre el almacén de B2) IMPLEMENTADA, sin ML.
  después: F35-SBX-B CERRADA, CONGELADA E INTEGRADA solo como sandbox sintético: B1 (…) CERRADA, CONGELADA E INTEGRADA; B2 (…) CERRADA, CONGELADA E INTEGRADA; B3 (pipeline determinista de doce pasos sobre el almacén de B2) CERRADA, CONGELADA E INTEGRADA, sin ML.

CLAUDE.md y docs/PROGRESS.md, el comienzo de la frase de los incrementos
  antes:   F35-SBX-B INICIADA: su incremento B1 (gate sucesor sobre HEAD) está CERRADO
  después: F35-SBX-B CERRADA, CONGELADA E INTEGRADA: su incremento B1 (gate sucesor sobre HEAD) está CERRADO

CLAUDE.md y docs/PROGRESS.md, el final de la frase de los incrementos (con enlaces relativos a su ruta)
  antes:   …; su incremento B3 (pipeline determinista de doce pasos sobre el almacén de B2) está IMPLEMENTADO, registrado en [`evidencia-sbx-b3`](…).
  después: …; su incremento B3 (pipeline determinista de doce pasos sobre el almacén de B2) está CERRADO, CONGELADO E INTEGRADO en `develop` y `main` (ancla aprobada `8d39d0e547821f7d6f63dc12b9c01803f985d797`, merges `53c0eb55a8f64f5576c43c2bfb5dccf095e30412` y `9424f1ea2a1e25dd29e8cfc0b9f446b3118b7a9a`), registrado en [`evidencia-sbx-b3`](…); su cierre terminal está registrado en [`evidencia-sbx-b-cierre-terminal`](…/evidencia-sbx-b-cierre-terminal/F35SBXB_Cierre_Terminal.md).

docs/PROGRESS.md, cabecera
  antes:   Última actualización: 2026-10-19 (…; F35-SBX-B INICIADA: B1 CERRADA E INTEGRADA, B2 CERRADA E INTEGRADA, B3 IMPLEMENTADA).
  después: Última actualización: 2026-10-21 (…; F35-SBX-B CERRADA, CONGELADA E INTEGRADA: B1, B2 y B3 CERRADAS E INTEGRADAS).

docs/PROGRESS.md, nota de historia
  antes:   … El 19/10/2026 pasó a B3 implementada: el pipeline determinista de doce pasos sobre el almacén de B2.
  después: … El 19/10/2026 pasó a B3 implementada: el pipeline determinista de doce pasos sobre el almacén de B2. El 21/10/2026 pasó a F35-SBX-B cerrada, congelada e integrada, con B3 auditada e integrada y su cierre terminal registrado.

docs/academico/ACADEMIC_BASELINE.md, el estado vigente
  antes:   Sin runtime productivo ni capacidades de alcance C. F35-SBX-B NO INICIADA. RF-23 sigue humana;
  después: Sin runtime productivo ni capacidades de alcance C. F35-SBX-B CERRADA, CONGELADA E INTEGRADA solo como sandbox sintético: B0, B1, B2 y B3 cerradas e integradas, sin ML. RF-23 sigue humana;

docs/academico/ACADEMIC_BASELINE.md, la frase de los commits
  antes:   F35-SBX-A queda cerrada documentalmente en `feature/f35-sbx-synthetic-evidence-pipeline`, con publicación pendiente de regresión post-commits y CI. F35-SBX-B NO INICIADA; requiere autorización nueva.
  después: F35-SBX-A está CERRADA E INTEGRADA en `develop` y `main`, con su commit E `61f94e23fc30b00a848a4558830b6d65f81dff87`. F35-SBX-B está CERRADA, CONGELADA E INTEGRADA, con su cierre terminal registrado en [`evidencia-sbx-b-cierre-terminal`](evidencia-sbx-b-cierre-terminal/F35SBXB_Cierre_Terminal.md). F36–F40 siguen BLOQUEADAS.
```

La forma es la que el gobierno ya usa para B1 y B2. En `ACADEMIC_BASELINE.md` solo cambian las dos frases del bloque vigente que describen F35-SBX: la de F35-SBX-A, cuyo estado canónico ya registra `CLAUDE.md` desde B0, y la de F35-SBX-B. Las fotografías históricas y la tabla de cierres no se reescriben. `README.md` no se toca: no es un registro exigido por el cierre (§2.1), y su bloque F34E previo a F35-SBX queda como observación (§5).

`TC_TRANSITION` es el commit que introduce el blob nuevo en las tres rutas a la vez. Se registra en el gate en el commit GREEN, nunca en el propio commit.

### 3.4 Gate sucesor

Ubicación: `docs/academico/tools/f35sbxb_cierre_terminal/validate_f35sbxb_cierre_terminal.py`. Solo biblioteca estándar, sin red, aislado (`python -I`, al que se relanza solo), con objetos Git verificados recalculando su identificador y con fallo cerrado ante cualquier error, salida incompleta o estado no evaluable.

| ID | Comprueba |
|---|---|
| ENT | Intérprete aislado y sin `PYTHONPATH`, `PYTHONHOME` ni `PYTHONUSERBASE`; ninguna variable de Git que redirija el repositorio, el índice o los objetos; historia completa, sin injertos ni objetos de reemplazo; el repositorio, a no más de dos niveles de clones compartidos |
| CTX | Rama `chore/f35-sbx-b-terminal-closure`, `develop` o `main`, y el merge `53c0eb5` como ancestro de HEAD |
| ANC | Anclas de §1.1 íntegras y en cadena, con la transición del cierre; los merges `eb02c2d`, `04895aa`, `ca36875` y `53c0eb5` con sus padres y el árbol de su ancla; los blobs de gobierno registrados de las seis etapas |
| HIS | El gate de B3, con los bytes de su blob en `8d39d0e`, anclado sobre `8d39d0e` en un clon temporal sin remoto y con sus alternates aplanados: código 0 y 19/0; FRZ en `8d39d0e`, GOV en `fa5664a`, el informe del pipeline con su SHA-256 registrado y R2-A anclado en 14/0 |
| B3G | El mismo gate sobre HEAD: su salida es la que da su propia lógica, cargada de los bytes verificados de su blob, sobre el estado observado, con recuentos, violaciones visibles y líneas INFO; solo falla por su clase A (§3.5) y las seis reglas del pipeline pasan |
| R2A | El gate de R2-A sobre HEAD, con la misma exigencia y su propia clase A (§3.5) |
| MAT | El gate de B2, verificado contra el candidato, sobre HEAD: solo su clase A exacta, con DEP limitado al pipeline y SBX-01..SBX-18 en verde |
| INT | Integridad de las capas congeladas, de A a B3, desde sus anclas, en cada commit posterior, el índice y el disco |
| FLG | Ningún flag en el índice |
| GOV | Transición única y monotónica en seis etapas (§3.6) |
| SEM | Semántica del gobierno vigente y de este documento, con las piezas verificadas del gate de B1 (§3.7) |
| LOW | Los tres riesgos residuales de §2.4, registrados con su severidad y su estado (§3.8) |
| ALC | Alcance exacto frente a `53c0eb5` en HEAD, el índice y el árbol de trabajo; ningún archivo sin seguimiento; carpetas de la capa exactas |
| FRZ | Nivel B: un único commit posterior a `53c0eb5` completa la capa; desde él, nada de la capa cambia. La línea INFO informa ese commit |
| DEP | Los archivos Python de la capa solo importan la biblioteca estándar autorizada; la única ejecución dinámica es la carga verificada de los gates congelados |

HIS, B3G, R2A y MAT se ejecutan en paralelo, cada uno con su temporal; el repositorio solo se lee.

### 3.5 Clase A

Sobre un HEAD válido, tres gates congelados fallan, y deben fallar. Se midió antes de escribir el gate, en un clon desechable con una capa de prueba y la transición de §3.3 aplicada, en la rama:

| Gate congelado sobre HEAD | Resultado | Fallas | Causa |
|---|---|---|---|
| B3 | 13/6 | CTX (solo en la rama), R2A, MAT, GOV, SEM y ALC | Rama nueva; rutas nuevas en R2-A y en el gate de B2; sexto blob de gobierno; el gobierno declara a F35-SBX-B y a B3 cerradas |
| R2-A | 7/7 | CTX (solo en la rama), GCL, SUC, MAT, GOV, SEM y ALC | Lo mismo, y `ACADEMIC_BASELINE.md` entre las rutas visibles del ALC de B2-SUCCESSOR-FREEZE, que hace fallar SUC |
| B2 | 112/7 | CTX (solo en la rama), B1F, SCP 78, DEP (el pipeline), DYN (P25) y GOV con 6 violaciones | Rama nueva; 26 rutas posteriores al candidato en tres planos; historia de gobierno; contenido distinto y «F35-SBX-B CERRADA», que su vocabulario rechaza |

Ninguna se oculta. Antes de clasificar, el gate calcula cada salida prevista con la lógica del propio gate congelado, cargada de los bytes verificados de su blob, y exige que la observada coincida en recuentos, violaciones visibles y líneas INFO:

- **B3G.** La predicción usa la lógica de B3 con la salida observada de R2-A y de B2. Las seis reglas del pipeline y ENT, ANC, HIS, INT, FLG, FRZ y DEP de B3 tienen que pasar, y su línea INFO de PIP lleva el SHA-256 registrado del informe.
- **R2A.** La predicción usa la lógica de R2-A, a través de las funciones verificadas de B3, y su SUC se deriva del ALC de B2-SUCCESSOR-FREEZE con la lógica de este.
- **MAT.** Los recuentos y validadores de R2-A, con las 26 rutas en SCP, y el GOV exacto con la lógica de B2.

Después clasifica con reglas propias. Una falla fuera de la clase A, o una clase A distinta de la prevista, hace fallar B3G, R2A o MAT:

- **CTX:** solo `rama no permitida` con el nombre de esta rama, y solo en ella.
- **Alcance:** las violaciones de alcance nombran exactamente las rutas de esta capa (A) y `ACADEMIC_BASELINE.md` (M), además de las de las capas posteriores a cada gate.
- **Gobierno:** las violaciones de gobierno nombran solo commits que descienden de la transición del cierre, más las del estado efectivo.
- **Semántica:** las semánticas se limitan a la declaración del cierre: F35-SBX-B y B3 cerradas, congeladas e integradas.
- **SCP del gate de B2:** cuenta exactamente las 26 rutas posteriores al candidato.

Lo que esas fallas enmascaran se repone con las reglas propias de este gate: INT, GOV, SEM, LOW, ALC, FRZ y DEP.

### 3.6 GOV: seis etapas

Para cada commit `C` de la ascendencia de HEAD que desciende de `8e94a60`, merges incluidos, lo admitido depende solo de su ascendencia:

1. **Antes de `12c1c36`:** el blob histórico de B1.
2. **Desde `12c1c36`:** el blob de B2.
3. **Desde `d346597`:** el blob del cierre de gobierno.
4. **Desde `ddefb7d`:** el blob del cierre formal.
5. **Desde `fa5664a`:** el blob de B3.
6. **En la transición del cierre terminal y en todo descendiente:** `TC_GOVERNANCE_BLOB`.

En las cinco primeras etapas, `ACADEMIC_BASELINE.md` conserva su blob `dccdf89`. Además:

- cada blob lo introduce solo su transición, en todas sus rutas a la vez;
- la transición del cierre tiene un solo padre, con el blob de B3, desciende de `53c0eb5` y cambia exactamente las tres rutas;
- la transición derivada coincide con la registrada;
- HEAD, el índice y el disco tienen el blob del cierre.

Modificar y restaurar, volver al blob de B3, un séptimo blob, una transición en un merge, en una parte de sus rutas o que cambie otras rutas fallan. Un merge `--no-ff` legítimo en `develop` y en `main` desciende de la transición y lleva el blob del cierre: pasa.

### 3.7 SEM: ciclo de vida de B cerrado

SEM carga el gate de B1 desde los bytes de su blob en `8e94a60`, verificados. En `CLAUDE.md`, `docs/PROGRESS.md` y `ACADEMIC_BASELINE.md` comprueba:

- una única sección «Estado vigente F34E», con los trece estados exactos;
- F35-SBX-B solo CERRADA en lo vigente y la declaración canónica del cierre (§3.3) presente; ninguna de las frases anteriores, como «F35-SBX-B INICIADA», «B3 (…) IMPLEMENTADA» o «PENDIENTE DE CIERRE FORMAL»;
- «RF-23 sigue humana» y «RF-29 sigue experimental/informativa» en el estado vigente;
- ninguna reapertura de F35-SBX-B, B1, B2 o B3 ni ningún estado posterior al cierre (tabla siguiente);
- ninguna declaración contradictoria con el vocabulario del cierre, en lo vigente y en las líneas nuevas frente al blob de B3, para los estados que conserva §2.3;
- ninguna afirmación positiva que habilite una capacidad prohibida en las líneas nuevas.

| Ciclo de vida | Gates congelados | Este gate |
|---|---|---|
| «F35-SBX-B INICIADA» | Admitida | Rechazada |
| F35-SBX-B y B3 cerradas, congeladas e integradas | Rechazadas | Admitidas |
| Reapertura, pendiente, abierta, en desarrollo o candidata | Según su vocabulario | Rechazadas |
| «Aprobada», «productiva», «publicada» o «desplegada» | Rechazadas | Rechazadas |
| «F35-SBX CERRADA» | Rechazada | Rechazada |

Este documento pasa las mismas comprobaciones: sin datos personales, afirmaciones positivas ni declaraciones contradictorias, con los once límites de §2.3 presentes. Los bloques de código del delta (§3.3) citan literalmente el gobierno anterior y el nuevo: no cuentan como declaración de estado, porque ambos se comprueban en las propias rutas de gobierno, pero sí se revisan en busca de afirmaciones positivas. Todos los archivos de la capa son UTF-8 sin BOM, CR ni NUL.

### 3.8 LOW: riesgos registrados

La tabla de §2.4 contiene exactamente las filas de B3-AF-L01, B3-AF-L02 y B3-R3. Cada una tiene severidad LOW, estado «Aceptado, no bloqueante» y el texto esencial de su descripción. Quitar, ocultar, reclasificar o dar por resuelto cualquiera de ellos hace fallar LOW.

### 3.9 Raíz de confianza y ancla de este incremento

- **Registradas en el gate,** porque ya existen: las anclas de §1.1, los merges y las transiciones de gobierno, y la transición del cierre en el commit GREEN.
- **Derivada y registrada fuera:** el commit que completa la capa (nivel B), que el gate informa en la línea INFO de FRZ. Es el ancla de este incremento y el commit de cierre que congela el gate y los artefactos de B (B1, §5). La auditoría la anota y comprueba que coincide; ningún archivo guarda su propio hash.
- **El merge de B3 en `main`** (`9424f1e`) no es ancestro de esta rama, así que el gate no lo verifica: se registra en §1.2 y en el gobierno, verificado con Git y con el CI, y CT02 prueba la integración `--no-ff` sobre él. Los resultados de CI no los consulta el gate, que trabaja sin red.

### 3.10 Lo que no cambia

- Las capas congeladas, de A a B3, conservan sus bytes, y sus validadores no se ejecutan con constantes alteradas ni se reescriben.
- Los commits integrados de B, de `8e94a60` a `9424f1e`, no se tocan.
- G0, G0-SBX, ADR-005, F35 productiva, F36–F40, el alcance C y los datos reales conservan su estado (§2.3). RF-23 sigue siendo humana y RF-29 experimental. El baseline RF-01 a RF-27 no cambia.
- Este incremento es solo gobierno, documentación y QA. No añade datos, capacidades, endpoints, migraciones, dependencias ni runtime.

## 4. Pruebas

Cada caso trabaja en un clon desechable de HEAD, fuera del repositorio, con objetos compartidos de solo lectura (en CT24, un clon superficial), configuración de Git aislada, identidad ficticia y fechas fijas, y ejecuta el gate con `python -I`. Pasa si fallan exactamente las reglas esperadas y, cuando se indica, si las líneas FALLA o INFO contienen el motivo esperado. Las historias reconstruidas se crean con plumbing de Git sobre el contenido de los commits originales.

| Caso | Escenario | Reglas en falla esperadas |
|---|---|---|
| CT01 | Estado válido; el ancla derivada es el commit que completa la capa | Ninguna (PASS) |
| CT02 | Merge `--no-ff` en `develop` (`53c0eb5`) y después de `develop` en `main` (`9424f1e`) | Ninguna en ambos |
| CT03 | Commit posterior sin cambios de contenido | Ninguna |
| CT04 | Ataque: séptimo blob de gobierno tras la transición | GOV |
| CT05 | Ataque: modificar → restaurar el gobierno tras la transición | GOV |
| CT06 | Ataque: vuelta al gobierno de B3 en las tres rutas | GOV, SEM, ALC, B3G, R2A y MAT |
| CT07 | Ataque: reapertura de F35-SBX-B en el estado vigente | GOV y SEM |
| CT08 | Ataque: B declarada cerrada sin la capa de B3 | INT, B3G, R2A, MAT y ALC |
| CT09 | Ataque: B3 sustituida por otro commit con el mismo árbol, con la integración y el cierre reconstruidos | CTX, INT, FRZ, GOV y B3G |
| CT10 | Ataque: historia del cierre reconstruida con el mismo contenido | GOV |
| CT11 | Ataque: capa congelada de B2 alterada tras el cierre | INT, B3G, R2A y ALC |
| CT12 | Ataque: riesgo B3-AF-L02 eliminado de este documento | LOW y FRZ |
| CT13 | Ataque: F36–F40 habilitadas en el gobierno | GOV, SEM, B3G, R2A y MAT |
| CT14 | Ataque: F35-SBX cerrada en el gobierno | GOV, SEM, B3G, R2A y MAT |
| CT15 | Ataque: G0 real aprobada en el gobierno | GOV, SEM, B3G, R2A y MAT |
| CT16 | Ataque: alcance C habilitado en el gobierno | GOV, SEM, B3G, R2A y MAT |
| CT17 | Ataque: datos reales permitidos en el gobierno | GOV, SEM, B3G, R2A y MAT |
| CT18 | Ataque: fila de RF-23 alterada en la matriz de trazabilidad | MAT, ALC, B3G y R2A |
| CT19 | Ataque: RF-29 declarado fuera de lo experimental en el gobierno | GOV y SEM |
| CT20 | Ataque: archivo del runtime modificado | ALC, MAT, B3G y R2A |
| CT21 | Ataque: archivo sin seguimiento en el árbol de trabajo | ALC, B3G, R2A y MAT |
| CT22 | Ataque: flag assume-unchanged en el índice | FLG, B3G, R2A y MAT |
| CT23 | Ataque: variable de Git que redirige el repositorio | ENT |
| CT24 | Ataque: clon superficial | Todas salvo FLG y DEP (fallo cerrado) |
| CT25 | Ataque: transición repartida en dos commits | GOV |
| CT26 | Ataque: transición introducida en un merge | GOV |
| CT27 | Ataque: la batería del cierre importa un módulo no autorizado | DEP y FRZ |
| CT28 | Ataque: la batería del cierre ejecuta código dinámico | DEP y FRZ |
| CT29 | Ataque: pipeline de B3 alterado tras el cierre | INT, B3G y ALC |
| CT30 | Ataque: este documento afirma que el motor recomienda candidatos | SEM y FRZ |
| CT31 | Ataque: este documento pierde un límite de §2.3 | SEM y FRZ |
| CT32 | Ataque: objeto de reemplazo en `refs/replace` | ENT, B3G y R2A |
| CT33 | Ataque: HEAD separado | CTX, B3G, R2A y MAT |
| CT34 | Ataque: rama no permitida | CTX, B3G, R2A y MAT |
| CT35 | Ataque: F35-SBX-B cerrada con B3 aún implementada en el gobierno | GOV y SEM |
| CT36 | Ataque: `ACADEMIC_BASELINE.md` devuelto a «F35-SBX-B NO INICIADA» | GOV, SEM, ALC, B3G, R2A y MAT |

Si un conjunto resulta distinto al medirlo en GREEN, se corrige con su causa registrada en §5, como en las capas anteriores.

## 5. Resultados

### 5.1 Commits

| Commit | Padre | Contenido | Resultado |
|---|---|---|---|
| `56783cbe314082ebc1e3c56c03e492e6e7256efc` | `53c0eb5` | Contrato y diseño (§1 a §4) y la batería CT01..CT36 (RED) | Batería 0/36, con 30 ejecuciones: el gate no existía en HEAD; CT06, CT07, CT25, CT26, CT35 y CT36 dependen de la transición, que aún no existía, y CT32 no podía prepararse (§5.2) |
| `5517a12a4d35c6d8c3281ace2f072ddc692f16f2` | `56783cb` | Transición de gobierno (§3.3): solo `CLAUDE.md`, `docs/PROGRESS.md` y `ACADEMIC_BASELINE.md`, con los blobs `d4ba0968e6ebbcaca667d47954db46f7088fae9a`, `a6322415e7705395dde1e185a3e501155f1989f5` y `e9fb4bbbc1534802fc196cca021eeeef69414571` | `TC_TRANSITION`, registrada en el gate del commit siguiente |
| El que completa la capa (este) | `5517a12` | Gate, correcciones de §5.2 y estos resultados (GREEN) | Gate 15/0; batería 36/36; 20 de 20 mutaciones detectadas |

Ese tercer commit es el ancla de nivel B de esta capa y el commit de cierre que congela el gate y los artefactos de B (§3.9). Lo informa la línea INFO de FRZ, y su hash no se guarda en ningún archivo.

### 5.2 Medición y correcciones

Todo se midió los días 21 y 22/10/2026 en clones sin remoto, con temporales cortos, nuevos y exclusivos. Las ejecuciones pesadas las lanzó un orquestador que limita cuántas corren a la vez, vigila la memoria del equipo y detiene la tanda ante cualquier síntoma ambiental (§5.6). La batería, la regresión y la autoauditoría se ejecutaron sobre dos commits desechables, hijos de la transición `5517a12`:

- `7fd910dc9508966445bdea0f60b85fbcb28371e8`, con la batería anterior a las correcciones de CT06, CT11, CT21 y CT29;
- `9e3e1789b8a643ef1d41db7866a896cd6832c790`, con ellas, y árbol `09ec0b4e33615e134ea010aef877556c3d0eb196`.

Su gate es, byte a byte, el de este commit (blob `acc20234fed043af58dcedf3dca858c77c81766f`). Su documento solo difiere del de este commit en la cabecera, en las filas que corrige esta sección y en la sección 5. Los controles de mutación usaron commits desechables iguales al segundo salvo en el gate (§5.6). El gate y los casos que dependen de este documento (CT12, CT30 y CT31) se ejecutaron además sobre un commit desechable con el árbol de este commit.

Correcciones, cada una con su causa medida antes de aplicarla. Ninguna cambia el gate:

- **CT32, arnés de la batería.** En RED el caso no podía prepararse: el arnés pasaba `data` a `Fixture.text`, que no lo admite (`TypeError`). Ahora crea el objeto de reemplazo con `Fixture.git`. Lo que el caso prueba no cambia.
- **Niveles de clones compartidos.** ENT admite dos niveles, no tres como decía §3.4 en RED. HIS ejecuta el gate de B3, que admite tres, en un clon compartido del repositorio, que suma uno. La batería añade otros dos, su clon base y el del caso, así que se ejecuta desde un repositorio sin alternates. Desde un clon compartido, en la tanda `bat3`, CT01 y CT03 fallaron en ENT y HIS solo por esa causa, confirmada con la función `alternates_depth` del propio gate. Esa tanda se detuvo y no cuenta. Se corrige §3.4.
- **CT06.** La vuelta al gobierno de B3 reintroduce, en un commit posterior, el blob de B3 y el `ACADEMIC_BASELINE.md` previo, que comparten las cinco etapas anteriores. GOV registra 14 violaciones: las tres visibles son de la regla 4 (los blobs de B2, del cierre de gobierno y del cierre formal, reintroducidos fuera de su transición) y la de la regla 3 es la quinta. CT06 busca ahora «regla 4».
- **CT11.** El gate de B2 no comprueba los bytes de su propio documento; eso lo hace B2-FREEZE. La alteración solo le suma un commit en B1F, de 20 a 21, que es de su clase A y MAT lo prevé. La detectan INT («capa B2»), B3G, R2A y ALC: CT11 espera ahora esas cuatro.
- **CT21.** El SCP del gate de B2 también cuenta el archivo sin seguimiento: 79 violaciones frente a las 78 previstas, así que MAT falla. CT21 espera ahora ALC, B3G, R2A y MAT.
- **CT29.** El pipeline alterado queda modificado frente a `53c0eb5`, fuera del alcance, y ALC también lo rechaza: CT29 espera ahora INT, B3G y ALC.
- **Fila CT32 de §4.** Decía solo ENT, pero la batería ya esperaba en RED ENT, B3G y R2A, y eso se midió: los gates de B3 y de R2-A también rechazan los objetos de reemplazo en su propio ENT, fuera de su clase A, y el de B2 no los busca. Se corrige la fila, y la de §2.7 sobre el entorno hostil nombra también los gates congelados.

### 5.3 Gate

| Dónde | Resultado |
|---|---|
| Rama, sobre `7fd910d` | 15/0 en 446 s |
| Rama, sobre `9e3e178` | 15/0 en 551 s, con otra ejecución pesada a la vez |
| Merge `--no-ff` de `9e3e178` en `develop` (`53c0eb5`), y de ese merge en `main` (`9424f1e`) | 15/0 y 15/0, en 589 y 509 s |
| Commit desechable con el árbol de este commit | 15/0 |

Líneas INFO sobre `9e3e178`:

- ANC: las diecinueve anclas registradas, de `8e94a60` a `5517a12`.
- HIS: el gate de B3 anclado sobre `8d39d0e`, código 0 y 19/0, con el ancla derivada `8d39d0e`, la transición derivada `fa5664a` y el informe `7efc00ee307c932955f2f3cc10b56dc08c14cd408c1fc7b43f612a712d174967`.
- B3G, R2A y MAT: los gates de B3, de R2-A y de B2 dan 13/6, 7/7 y 112/7, con SCP en 78 violaciones de 78 previstas. Cada salida es la que prevé su propia lógica.
- GOV: transición derivada `5517a12`, igual a la registrada.
- FRZ: el commit que completa la capa, que en la simulación es `9e3e178`.

### 5.4 Clase A medida

Medida sobre `9e3e178`, en la rama, y comparada con la base `53c0eb5` (`develop`), en clones limpios sin remoto. El gate del cierre ejecuta los tres primeros; los demás se miden como información:

| Gate congelado sobre HEAD | Resultado (base) | Fallas sobre HEAD |
|---|---|---|
| B3 | 13/6 (19/0) | La clase A de §3.5, exacta: CTX 1, la rama; R2A 6, MAT 3, GOV 8, SEM 9 y ALC 3 |
| R2-A | 7/7 (9/5) | La clase A de §3.5: CTX 1, la rama; GCL 9 (3), SUC 1, MAT 3 (2), GOV 10 (9), SEM 7 (3) y ALC 3 (3) |
| B2 | 112/7 (113/6) | CTX 1, la rama; B1F 20 (17: los tres commits de esta capa); SCP 78 (66: las cuatro rutas nuevas o modificadas, en tres planos); DEP 1, el pipeline; DYN 1 (P25); GOV 6 (3). SBX en verde |
| B2-GOVERNMENT-CLOSURE | 7/6 (8/5) | CTX 1, la rama; SEM 6 (3); SUC 1, MAT 3, GOV 10 y ALC 3, como sobre la base |
| B2-SUCCESSOR-FREEZE | 10/2 (10/2) | VIG 5 y ALC 3, como sobre la base |
| Sucesor | 4/3 (4/3) | CON 1, MAT 2 y ALC 3, como sobre la base |
| B2-FREEZE | 6/4 (6/4) | HIS 14 (11: los tres commits de esta capa); ARB 1, IDX 1 y DSK 2, como sobre la base |
| B1 | 104/55 (106/53) | CTX 1, la rama; GOV 4 (1), porque el gobierno declara F35-SBX-B CERRADA y su vocabulario solo admite la apertura; SCP 102 (90); los 51 casos PB de la base, ahora por ese mismo motivo; y NB-15, cuya mutación busca la frase «F35-SBX-B INICIADA solo como sandbox», que ya no existe |
| B1-FREEZE | 0/2 (0/2) | FRZ 35 (32: los tres commits de esta capa) y B1, como sobre la base |
| F35-SBX-A | Termina con `StopIteration` (igual sobre la base) | Su autoprueba de mutaciones no encuentra la frase canónica del ciclo de vida de A, igual que sobre la base. Anclado en su commit E da 846/0 (§5.7) |

En `develop` y `main` CTX pasa: sobre los merges `--no-ff` (CT02 y la regresión), el gate de B3 da 14/5, el de R2-A 8/6 y el de B2 113/6, con las mismas reglas de clase A sin CTX. B3G, R2A y MAT clasifican exactamente las tres primeras filas; lo que esas fallas enmascaran lo reponen INT, GOV, SEM, LOW, ALC, FRZ y DEP (§3.5).

### 5.5 Batería

**36/36.** Cada caso dio exactamente el resultado de §4 y, donde se indica, con su motivo:

| Tanda | Commit | Casos | Resultado |
|---|---|---|---|
| `bat4` | `7fd910d` | CT01..CT36, tres a la vez, con 37 ejecuciones del gate | 32/36. CT06, CT11, CT21 y CT29 fallaron con las expectativas de RED, por las causas de §5.2, y no se cuentan |
| `cor1` | `9e3e178` | CT01, CT06, CT11, CT21 y CT29, con 5 ejecuciones | 5/5 |
| Árbol final | Desechable, con el árbol de este commit | CT12, CT30 y CT31, dos a la vez | 3/3 |

En `bat4` no hubo ningún síntoma ambiental y la memoria comprometible libre no bajó de 2,1 GB.

### 5.6 Controles de mutación

Veinte mutaciones del gate, cada una sobre un commit desechable cuyo gate solo difiere del de este commit en la sentencia mutada, con el caso que debe detectarla. Las veinte se detectan, con 20 ejecuciones del gate y sin ningún síntoma ambiental:

| # | Mutación del gate | Caso | Resultado |
|---|---|---|---|
| M01 | ENT sin rechazar las variables de Git que redirigen el repositorio | CT23 | Detectada: CT23 pasa a PASS |
| M02 | CTX sin exigir una rama permitida | CT34 | Detectada: deja de fallar en CTX |
| M03 | CTX sin exigir `53c0eb5` como ancestro | CT09 | Detectada: deja de fallar en CTX |
| M04 | B3G sin clasificar la clase A | CT29 | Detectada: deja de fallar en B3G |
| M05 | R2A sin clasificar la clase A | CT20 | Detectada: deja de fallar en R2A |
| M06 | MAT acepta cualquier salida del gate de B2 | CT18 | Detectada: deja de fallar en MAT |
| M07 | INT sin la capa de B3 | CT29 | Detectada: deja de fallar en INT |
| M08 | INT sin la capa de B2 | CT11 | Detectada: deja de fallar en INT |
| M09 | FLG sin efecto | CT22 | Detectada: deja de fallar en FLG |
| M10 | GOV sin comparar la transición derivada con la registrada | CT10 | Detectada: CT10 pasa a PASS |
| M11 | GOV sin la regla 3 | CT05 | Detectada: la línea FALLA GOV ya no contiene «regla 3» |
| M12 | SEM sin la declaración canónica del estado vigente | CT19 | Detectada: deja de fallar en SEM |
| M13 | SEM sin buscar reaperturas | CT07 | Detectada: deja de fallar en SEM |
| M14 | SEM sin las afirmaciones positivas de este documento | CT30 | Detectada: deja de fallar en SEM |
| M15 | SEM sin los límites de §2.3 | CT31 | Detectada: deja de fallar en SEM |
| M16 | LOW sin efecto | CT12 | Detectada: deja de fallar en LOW |
| M17 | Sin ALC | CT20 | Detectada: deja de fallar en ALC |
| M18 | Sin FRZ | CT12 | Detectada: deja de fallar en FRZ |
| M19 | DEP sin comprobar las importaciones | CT27 | Detectada: deja de fallar en DEP |
| M20 | DEP sin buscar ejecución dinámica | CT28 | Detectada: deja de fallar en DEP |

M01..M12 corrieron tres a la vez. Con M13, M14 y M15 en curso, la memoria comprometible libre del equipo bajó hasta 1,4 GB, por debajo del margen exigido: se detuvo la tanda, esas tres ejecuciones interrumpidas se apartaron sin contarlas y M13..M20 se repitieron dos a la vez. M20 se repitió además entero tras un corte de la sesión. Desde entonces ninguna tanda ha superado dos ejecuciones a la vez.

### 5.7 Regresión

| Comprobación | Resultado |
|---|---|
| `validate_f35sbxb_cierre_terminal.py` | 15/0 en la rama (`9e3e178`), en su merge `--no-ff` en `develop` (`62b3114`) y en el de ese merge en `main` (`3699adc`), los tres con el árbol `09ec0b4e`. FRZ informa `9e3e178` y GOV deriva `5517a12`, igual a la registrada |
| Gates anclados en clones limpios sin remoto | B3 sobre `8d39d0e`: 19/0. R2-A sobre `ad193f9`: 14/0. B2-GOVERNMENT-CLOSURE sobre `363273e`: 13/0. B2-SUCCESSOR-FREEZE sobre `8969424`: 12/0. Sucesor sobre `9d6fb15`: 7/0. B2-FREEZE sobre `9961d2d`: 10/0. B2 sobre `2472fd6`: 119/0. B1 sobre `8e94a60`: 159/0. B1-FREEZE sobre `3d9b783`: 14/0. Validador de A sobre su commit E, `61f94e2`: 846/0 |
| `test_sbxb_pipeline.py` | 30/30 |
| `validate.py` y `validate.py --cierre-f29` | 0 fallas en ambos |
| `validate_f29.py`, `test_f32_safety.py`, `validate_f33.py` y `validate_f34.py` | 225/0, OK, 451/0 y 403/0 |
| `validate_f34a.py` | 108/0 |
| `validate_f34e.py` | 247/1, igual que sobre `53c0eb5`: la falla histórica de la regla GIT. Su lista de rutas no autorizadas por DH-02 pasa de 34 a 37, las tres de esta capa, sin que desaparezca ninguna. Su comprobación del cierre de F35-SBX-A, que exige «F35-SBX-B NO INICIADA», nombra ahora también `ACADEMIC_BASELINE.md`, además de `CLAUDE.md` y `docs/PROGRESS.md`, que ya nombraba sobre la base. Criterios SBX: 18/18 |
| Enlaces relativos | 1154 en `docs/academico` y 1560 en todo el repositorio, 0 rotos |
| MANIFEST y evidencias | 61 hashes y 0 discrepancias; 81 hashes de las evidencias de las prácticas 03, 05, 08 y 11, 0 discrepancias |
| `git diff --check` | Limpio frente a `53c0eb5`, `8d39d0e` y `ad193f9` |
| Delta frente a `53c0eb5` | Exactamente las tres rutas de la capa (A) y las tres de gobierno (M); ninguna fuera de `docs/academico`, `CLAUDE.md` y `docs/PROGRESS.md` |
| Gobierno de HEAD | Los trece estados sin cambios; la declaración del cierre en el estado vigente de las tres rutas, sin «F35-SBX-B INICIADA» ni «F35-SBX-B NO INICIADA» en lo vigente; «RF-23 sigue humana; RF-29 sigue experimental/informativa.» en las tres |
| Árboles de trabajo | Sin cambios en los cuatro clones tras la validación |

La regresión corrió con dos bloques a la vez como máximo, sin ningún síntoma ambiental y con la memoria comprometible libre siempre por encima de 10 GB.

### 5.8 SBX-01..SBX-18

Recalculados sobre HEAD por el gate de B2 dentro de MAT, sin ninguna línea FALLA SBX: 18/18 en la rama y en los merges en `develop` y `main`. `validate_f34e.py` sobre HEAD: «SBX: 18/18 cumplen», con G0-SBX APROBADA CON RESTRICCIONES y F35-SBX HABILITADA. B1-FREEZE anclado: SBX-01..SBX-18 sobre HEAD (DH-B13), 18/18. Ningún hecho REV-01..REV-14: G0-SBX sigue vigente (C18).

### 5.9 Autoauditoría

Se intentó romper el cierre por cada vía de la consigna, con el resultado medido:

| Intento | Qué lo rechaza | Evidencia |
|---|---|---|
| Declarar B cerrada sin la capa de B3 | INT, B3G, R2A, MAT y ALC | CT08 |
| Cerrar sobre B3 sin su integración en `develop` | CTX, GOV y FRZ | Sonda P1 |
| Sustituir B3 o la historia del cierre por contenido equivalente | CTX, INT, FRZ, GOV y B3G; GOV | CT09 y CT10 |
| Alterar una capa congelada o el pipeline de B3 | INT, ALC, B3G y R2A | CT11 y CT29 |
| Cambiar un ancla registrada en el propio gate después del cierre | FRZ, ANC e INT, y el fallo cerrado de HIS, B3G, R2A, MAT, GOV y SEM | Sonda P7 |
| Ocultar o eliminar cualquiera de los tres riesgos LOW | LOW y FRZ | CT12 y las sondas P5 y P6 |
| Sobredeclarar en el gobierno: F36–F40, F35-SBX, la G0 real, el alcance C, los datos reales, RF-23 o RF-29 | GOV, SEM y los gates congelados | CT13..CT19 |
| Reabrir B o volver al gobierno de B3 | GOV, SEM y los gates congelados | CT06, CT07, CT35 y CT36 |
| Afirmar una capacidad prohibida o quitar un límite en este documento | SEM y FRZ | CT30 y CT31 |
| Tocar archivos fuera del delta | ALC, MAT, B3G y R2A | CT18, CT20 y CT21 |
| Entorno de Git hostil o incompleto | ENT, FLG, CTX y fallo cerrado | CT22..CT24 y CT32..CT34 |
| Ejecutar el gate con el temporal dentro del repositorio | Fallo cerrado de HIS, B3G, R2A y MAT | Sonda P2 |
| Ejecutar una copia del gate fuera del repositorio | Fallo cerrado de todas las reglas | Sonda P3 |
| Repositorio a tres niveles de clones compartidos | ENT y HIS | Sonda P4 |
| Debilitar una regla del gate | La batería | 20 de 20 mutaciones detectadas (§5.6) |

Las sondas P1..P7 completan la batería, sobre `9e3e178`, en clones desechables y como mucho dos a la vez:

| Sonda | Escenario | Resultado |
|---|---|---|
| P1 | El cierre construido directamente sobre `8d39d0e`, sin el merge de integración `53c0eb5` | 12/3: CTX, GOV (regla 2 y transición derivada distinta de la registrada) y FRZ |
| P2 | El temporal dentro del repositorio | 11/4: HIS, B3G, R2A y MAT fallan cerrados, con «directorio temporal no disponible fuera del repositorio» |
| P3 | Una copia del gate fuera del repositorio, ejecutada con el repositorio como directorio de trabajo | 0/15: Git no encuentra el repositorio del gate y DEP no encuentra los archivos de la capa; falla cerrado |
| P4 | El repositorio a tres niveles de clones compartidos | 13/2: ENT, que admite dos, y HIS, con el gate de B3 anclado a cuatro niveles |
| P5 | La fila de B3-AF-L01 eliminada de este documento | 13/2: LOW y FRZ |
| P6 | La fila de B3-R3 eliminada de este documento | 13/2: LOW y FRZ |
| P7 | El ancla de B3 cambiada por `fa5664a` en el gate, en un commit posterior | 6/9: ANC, HIS, B3G, R2A, MAT, INT, GOV, SEM y FRZ, que señala el propio gate, cambiado después del commit que completa la capa |

| # | Nivel | Hallazgo | Tratamiento |
|---|---|---|---|
| TC-H1 | LOW | §3.4 decía en RED que ENT admite tres niveles de clones compartidos; el gate admite dos | Corregido en este commit (§5.2). La condición de ejecución queda como TC-R1 |
| TC-H2 | LOW | La fila CT32 de §4 no coincidía con la batería de RED | Corregida en este commit (§5.2) |
| TC-H3 | LOW | Cuatro expectativas de RED (CT06, CT11, CT21 y CT29) no preveían detecciones correctas | Corregidas con su causa medida (§5.2), sin cambiar el gate |
| TC-H4 | INFO | `README.md` conserva en su bloque «Estado vigente F34E» la frase «F35-SBX AÚN NO INICIADA», anterior a F35-SBX | Fuera del alcance (§3.3): no es un registro exigido por el cierre y el delta no lo admite. Queda para una actualización documental aparte, con autorización del equipo |
| TC-H5 | INFO | Reintroducir el `ACADEMIC_BASELINE.md` previo, común a cinco etapas, produce una violación de la regla 4 por cada una de las cuatro etapas de B2 a B3 (CT06) | Diagnóstico redundante, no una falta de detección: GOV falla igual y el recuento es exacto |

No quedó ningún hallazgo BLOCKER, HIGH ni MEDIUM abierto.

### 5.10 Riesgos residuales

Los tres riesgos LOW de §2.4 se conservan tal como los clasificó la auditoría de B3, sin corregirlos ni reclasificarlos. Además:

| # | Nivel | Riesgo | Tratamiento |
|---|---|---|---|
| TC-R1 | INFO | El gate admite el repositorio a dos niveles de clones compartidos como mucho, y la batería suma dos: se ejecuta desde un repositorio sin alternates | Un clon normal o una copia `--no-local` cumplen la condición. Más allá del límite fallan ENT y HIS, en el gate (sonda P4) y en los casos de la batería (tanda `bat3`): nunca hay un PASS falso |
| TC-R2 | INFO | El ancla de nivel B solo autentica la capa si se registra fuera: una capa reconstruida con los mismos bytes en otra historia informa otra ancla (CT09 y CT10) | La auditoría anota el commit que informa FRZ |
| TC-R3 | INFO | El gate trabaja sin red: no consulta el CI ni verifica `9424f1e`, que no es ancestro de esta rama | §1.2 registra el CI y los merges de B3, verificados con Git y con la API pública de GitHub; CT02 y la regresión prueban los merges `--no-ff` |
| TC-R4 | INFO | Cada ejecución del gate lanza cuatro gates congelados en paralelo y tarda de 7 a 10 minutos sola o con otra, y unos 20 con tres a la vez; la batería completa suma 37 ejecuciones. Con tres a la vez, en un equipo de 32 GB con otras aplicaciones abiertas, la memoria comprometible libre bajó a 1,4 GB | Ejecutar como mucho dos a la vez, con la memoria vigilada (§5.6) |
| TC-R5 | INFO | La predicción de B3G, R2A y MAT usa la lógica de los propios gates congelados: un error común a esa lógica y a su salida no lo revela la comparación | La clasificación de clase A es propia, y lo enmascarado lo reponen INT, GOV, SEM, LOW, ALC, FRZ y DEP |
| TC-R6 | INFO | Hasta que la auditoría independiente apruebe este incremento y el equipo autorice su integración, el registro del cierre en el gobierno de esta rama no vale: `develop` y `main` siguen diciendo «F35-SBX-B INICIADA» | Es el estado de todo candidato. El texto nuevo no menciona el estado de auditoría, así que no habrá nada que registrar después (§2.8) |

### 5.11 Pendientes

- La auditoría independiente de este incremento, sobre su ancla: el commit que informa FRZ.
- Con su aprobación y la autorización expresa del equipo, la publicación de la rama y su integración `--no-ff` en `develop` y `main`, con CI en verde. Este incremento no hace push, merge, tag ni release.
- El cierre de F35-SBX, que exige otra decisión del equipo y otro incremento. Ninguna fase posterior queda habilitada.
- La observación TC-H4 sobre `README.md`, para una actualización documental aparte.
- Los pendientes externos de la G0 real (G0-02, G0-03 y G0-12), que este cierre no cambia.
