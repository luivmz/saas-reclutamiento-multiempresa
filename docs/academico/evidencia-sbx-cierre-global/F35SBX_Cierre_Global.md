# F35-SBX — Cierre global

> **Estado: CIERRE GLOBAL IMPLEMENTADO / VALIDADO LOCALMENTE / CANDIDATO A AUDITORÍA INDEPENDIENTE.** Fecha: 24/10/2026. Rama `chore/f35-sbx-global-closure`, desde `develop` = `f082b4165ca756659b998716e2647494a3ec7be6`.
>
> - Este documento reconstruye el alcance global de F35-SBX desde sus contratos, evalúa si puede cerrarse, fija el contrato y el diseño del incremento que registra ese cierre y recoge sus resultados. El gobierno de esta rama ya registra el cierre (§3.2).
> - El cierre solo vale en el alcance académico y sintético de F35-SBX, y solo cuando la auditoría independiente apruebe este incremento y el equipo autorice su integración. Hasta entonces, `develop` y `main` siguen diciendo «F35-SBX = HABILITADA».
> - Este incremento no se autoaprueba: lo decide la auditoría independiente sobre su ancla.
>
> Las secciones 1 a 4 registran la reconstrucción, la evaluación, el contrato y el diseño, escritos antes de la transición de gobierno y del gate (commit RED `7746bf2`). El commit que completa la capa solo los corrige donde la medición lo exigió, con su causa en §5.2. La sección 5 registra los resultados.

## 1. Punto de partida verificado

### 1.1 Anclas

| Ancla | Commit | Qué es |
|---|---|---|
| Decisión G0-SBX (F34E) | `0ea5e63bb84db717bcc5f2a94c3c93572d5b863e` y `c016a75401eb127aa11cd9185423e2866b0fc936` | Commits A y B de F34E: G0-SBX APROBADA CON RESTRICCIONES y la apertura de F35-SBX como sandbox sintético |
| F35-SBX-A, commit E | `61f94e23fc30b00a848a4558830b6d65f81dff87` | Contrato, fixtures, manifest y validador de A, congelados |
| Cierre de B0 | `cc634eb9dcc5c0cc0d77b911bb3815182b8319c2` | Sucesión de gates de B, solo documentación |
| B1 y B1-FREEZE | `8e94a60274fe39ebda3e9961bc58036b389dfc00` y `3d9b78307684a0dfb093e31d28fde290b2b1cb4a` | Gate sucesor de B y su cierre |
| B2 | `2472fd6fadfc0634ec68cbcb76cfc9fbfe105194`, `9961d2d65ed51a17c14aae5db0edb7d71c622c22`, `9d6fb157bb818574217e3675da1849e8d1010962` y `89694244b81b0bd84dbe6ae5d04b5c7a198bafef` | Almacén efímero, B2-FREEZE, gate sucesor y B2-SUCCESSOR-FREEZE |
| Cierres de B2 | `363273ead5794ea7a2dba74c011a0efd6d59e906` y `ad193f9565bf23246fadb9f85fc0ceddf8ddf698` | B2-GOVERNMENT-CLOSURE y R2-A, el cierre formal |
| B3 | `8d39d0e547821f7d6f63dc12b9c01803f985d797` | Pipeline determinista de doce pasos |
| Integración de B3 | `53c0eb55a8f64f5576c43c2bfb5dccf095e30412` (`develop`) y `9424f1ea2a1e25dd29e8cfc0b9f446b3118b7a9a` (`main`) | Merges `--no-ff` |
| Cierre terminal de F35-SBX-B | `5517a12a4d35c6d8c3281ace2f072ddc692f16f2` y `9ebb90929f34079b42e88e21e144f80182ba7565` | Transición de gobierno y ancla aprobada |
| Integración del cierre terminal | `f082b4165ca756659b998716e2647494a3ec7be6` (`develop`) y `57eeb5329c7ef5cc3fa219918536400fcb846570` (`main`) | Merges `--no-ff`, con el árbol `7e122321b88b145f832f3c0c7a69a8798cb243fb` del ancla; base de este incremento |

### 1.2 Estado de entrada

| Hecho | Valor | Cómo se verificó |
|---|---|---|
| `origin/develop` y `origin/main` | `f082b41` y `57eeb53`, sin commits posteriores a los merges | `git fetch` y `git ls-remote` |
| Árboles | `9ebb909`, `f082b41` y `57eeb53` tienen el árbol `7e122321` | `git rev-parse <commit>^{tree}` |
| CI de `develop` | Workflow `tests`, run 66, id `40142849248`, SHA `f082b41`: `completed` / `success` | API pública de GitHub |
| CI de `main` | Workflow `tests`, run 67, id `40143578990`, SHA `57eeb53`: `completed` / `success` | API pública de GitHub |
| Auditoría del cierre terminal | «F35-SBX-B TERMINAL CLOSURE APROBADO PARA INTEGRACIÓN», sin hallazgos BLOCKER, HIGH ni MEDIUM abiertos | Registro de la auditoría, fuera del repositorio |
| Gate del cierre terminal | 15/0 sobre `9ebb909` y sobre los dos merges, antes de cada push | Clon aislado de GitHub, con temporales propios |
| Etiquetas y releases | `v1.0.0-academic` → `9a946c2` y `v1.1.0-academic` → `634f354`; una sola release | `git ls-remote --tags` y API pública |

## 2. Alcance global y evaluación del cierre

### 2.1 Fuentes

Solo se usan los contratos existentes. Ninguna definición se crea para este cierre.

| Fuente | Qué fija |
|---|---|
| [Autorización de F35-SBX](../g0-sandbox/F34E_Autorizacion_F35_SBX.md), [alcance autorizado](../g0-sandbox/F34E_Alcance_Autorizado.md), [prohibiciones](../g0-sandbox/F34E_Prohibiciones.md) y [decisión G0-SBX](../g0-sandbox/F34E_Decision_G0_SBX.md) | F35-SBX existe solo con G0-SBX APROBADA CON RESTRICCIONES; su alcance es el pipeline experimental de evidencias sintéticas; cada entrega vuelve a ejecutar `validate_f34e.py`; nada migra a trabajo real sin SAL-01 a SAL-05; F36–F40 no se inician sin su propia autorización |
| [Definición](../g0-sandbox/F34E_Definicion_G0_SBX.md) y [matriz de criterios](../g0-sandbox/F34E_Matriz_Criterios_G0_SBX.md) de G0-SBX | Los 18 criterios SBX, que se reevalúan en cada fase SBX |
| [Alcance de A](../evidencia-sbx/F35SBX_Alcance.md) y [criterios de A](../evidencia-sbx/F35SBX_Criterios_Cierre_y_Revocacion.md) | Objetivos O1..O6, ACS-01..ACS-10, la revocación REV-01..REV-14 y el encargo a B; CAP-33 y CAP-34 no figuran en el alcance autorizado de F34E |
| [B0](../evidencia-sbx-b/F35SBXB_B0_Sucesion_de_Gates.md), §3 y §3.1 | Requisitos del gate sucesor y DH-B13: el gate sucesor recalcula SBX-01..SBX-18 uno por uno sobre HEAD |
| [B1](../evidencia-sbx-b/F35SBXB_B1_Gate_Sucesor.md), §5 | Después de B, el gate de B se ejecuta anclado sobre su cierre y la fase siguiente aporta un gate sucesor sobre HEAD que verifica la integridad de B y recalcula SBX-01..SBX-18 |
| [Cierre terminal de F35-SBX-B](../evidencia-sbx-b-cierre-terminal/F35SBXB_Cierre_Terminal.md), §2.3 y §2.8 | Cerrar B no basta para cerrar F35-SBX: hace falta otra decisión del equipo y otro incremento |

### 2.2 Qué es F35-SBX

F35-SBX es la fase de experimentación académica autorizada por G0-SBX en F34E: un pipeline experimental de evidencias sintéticas del alcance B de ADR-005, aislado del runtime y sin personas reales. Se ejecutó en dos subfases:

1. **F35-SBX-A** fijó el diseño, el contrato cerrado, los fixtures sintéticos de tres organizaciones, el manifest y el validador. Se cerró con ACS-01..ACS-10 y auditoría PASS, y su commit E está integrado.
2. **F35-SBX-B** ejecutó ese contrato:
   - B0 fijó la sucesión de gates;
   - B1 construyó el gate sucesor;
   - B2 construyó el almacén efímero aislado y lo cerró en tres pasos (B2-FREEZE, el cierre de gobierno y el cierre formal R2-A);
   - B3 implementó el pipeline determinista de doce pasos sobre los fixtures de A;
   - el cierre terminal congeló B.

   Todas esas capas están auditadas e integradas en `develop` y `main`.

### 2.3 Objetivos, entrada, salida y entregables

| Elemento | Contenido | Fuente |
|---|---|---|
| Objetivo | Un pipeline de evidencia sintética aislado, auditable y reproducible: contrato cerrado, provenance, tenants sintéticos, revisión humana simulada solo de integridad y procedencia, auditoría encadenada, purga y determinismo | F34E; A, §2 |
| Criterio de entrada | G0-SBX APROBADA CON RESTRICCIONES, con SBX-01..SBX-18 en CUMPLE | F34E, decisión y definición |
| Criterio de permanencia | Cada entrega reevalúa SBX-01..SBX-18; cualquier hecho REV-01..REV-14 revoca G0-SBX y detiene el trabajo SBX | A, §3; F34E, decisión §4 |
| Criterio de salida | F35-SBX-A y F35-SBX-B cerradas e integradas, con su alcance completo, G0-SBX vigente y los invariantes intactos, y el cierre registrado por un incremento propio | §2.4 |
| Entregables | A: diez documentos, contrato, fixtures, manifest y validador. B: B0, el gate de B1, el almacén de B2, el pipeline de B3, sus gates sucesores y el cierre terminal | A, §3; B0 a B3 |
| Restricciones | Solo datos sintéticos; las prohibiciones de F34E; sin runtime, dependencias, migraciones ni endpoints | F34E |
| Dependencias | G0-SBX; la G0 real sigue NO APROBADA y no es requisito de F35-SBX | F34E |
| Fuera de F35-SBX | CAP-33 (acuerdo entre evaluadores) y CAP-34 (alertas deterministas), que no están en el alcance autorizado de F34E; F36–F40, también en sandbox | A, §4; F34E |

### 2.4 Matriz de criterios del cierre global

| ID | Criterio | Evidencia | Estado |
|---|---|---|---|
| GC-C01 | G0-SBX vigente: SBX-01..SBX-18 en CUMPLE y ningún hecho REV-01..REV-14 | Recalculados en cada capa de B; 18/18 en la integración del cierre terminal; `validate_f34e.py` solo con su falla histórica de alcance (DH-B13, clase A) | CUMPLIDO; se recalcula otra vez aquí |
| GC-C02 | F35-SBX-A cerrada e integrada | Commit E en la historia de `develop` y `main`; gobierno; validador de A anclado en E: 846/0 | CUMPLIDO |
| GC-C03 | A y B no se contradicen | B no modificó A: las carpetas de A y los cinco validadores adaptados siguen idénticos a E | CUMPLIDO; INT lo comprueba aquí |
| GC-C04 | B0, B1, B2 y B3 cerradas, congeladas e integradas | Anclas de §1.1 y sus gates anclados en verde | CUMPLIDO |
| GC-C05 | F35-SBX-B cerrada, congelada e integrada | Cierre terminal aprobado e integrado; CI 66 y 67 en verde; su gate, 15/0 | CUMPLIDO |
| GC-C06 | Alcance autorizado completo | A aportó contrato, fixtures, provenance, tenants, revisión simulada y validador; B, el almacén aislado, el pipeline determinista, la auditoría encadenada, la purga y el informe con hashes | CUMPLIDO |
| GC-C07 | Nada pendiente dentro de F35-SBX | CAP-33 y CAP-34 nunca formaron parte de F35-SBX; ningún criterio de A ni de B queda abierto | CUMPLIDO |
| GC-C08 | Ninguna capacidad prohibida | SBX-05..SBX-07, las prohibiciones de F34E, el esquema cerrado del informe y DEP y SEM de cada capa | CUMPLIDO |
| GC-C09 | Invariantes de gobierno | Los trece estados del gobierno vigente | CUMPLIDO |
| GC-C10 | Riesgos residuales no bloqueantes | §2.6 | CUMPLIDO |
| GC-C11 | Registro del cierre en el gobierno, con una transición única y un gate sucesor que verifique la integridad de A y de B y recalcule SBX-01..SBX-18 | B1, §5; DH-B13 | ESTE INCREMENTO (§3) |
| GC-C12 | `README.md` coherente con el estado vigente | TC-H4 | ESTE INCREMENTO (§3.2) |
| GC-C13 | F36–F40 bloqueadas y la regla de que ninguna F36-SBX empieza sin una autorización sucesora nueva, escritas de forma explícita | F34E, autorización §1 | ESTE INCREMENTO (§3.2) |

**Decisión.** GC-C01 a GC-C10 están cumplidos con evidencia existente, verificada por identidad de commits, árboles, CI y evidencia persistida. El cierre global procede. GC-C11 a GC-C13 son el contenido de este incremento.

### 2.5 Qué significa el cierre y qué no

El cierre significa solo esto: **F35-SBX completó y cerró su alcance académico y sintético autorizado**, con F35-SBX-A y F35-SBX-B cerradas, congeladas e integradas.

El cierre de F35-SBX:

- no aprueba la G0 real ni sustituye su evidencia externa;
- no habilita la F35 productiva ni ninguna integración productiva;
- no habilita F36 ni ninguna fase posterior, tampoco en sandbox;
- no habilita F36-SBX: ninguna F36-SBX empieza sin una autorización sucesora nueva, con su propia gobernanza;
- no permite datos reales;
- no permite puntuar ni clasificar ni recomendar candidatos;
- no permite la selección automática;
- no habilita biometría ni inferencias de emoción, personalidad, honestidad, inteligencia o estrés;
- no habilita el alcance C;
- no habilita OCR ni parsing ni embeddings ni búsqueda semántica;
- no cambia RF-23, que sigue siendo la decisión final humana del Aprobador/Dirección;
- no cambia RF-29, que sigue experimental e informativo;
- no revoca ni amplía G0-SBX, que sigue APROBADA CON RESTRICCIONES;
- no reutiliza ningún artefacto SBX en trabajo real, que exige SAL-01 a SAL-05.

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
| RF-23 | Decisión final humana del Aprobador/Dirección |
| RF-29 | Experimental e informativo |

Cambia un solo estado: F35-SBX pasa de HABILITADA a CERRADA Y CONGELADA.

### 2.6 Riesgos residuales

Los riesgos de B y del cierre terminal se registran tal como los clasificaron sus auditorías, sin elevarlos ni rebajarlos. Este cierre no corrige los LOW: hacerlo exigiría cambiar código congelado.

| ID | Nivel | Descripción | Evidencia y mitigación | Estado |
|---|---|---|---|---|
| B3-AF-L01 | LOW | Comprobante de purga no completamente independiente del pipeline: lo emite el propio pipeline y el gate no observa la memoria de su proceso | La observación en el proceso de B3 (PT06) y el congelamiento del código | Aceptado, no bloqueante |
| B3-AF-L02 | LOW | La comprobación CNF no demuestra por sí sola la unicidad global de `audit_id` | El almacén de B2 declara `audit_id` como clave primaria | Aceptado, no bloqueante |
| B3-R3 | LOW | Los diagnósticos de los gates históricos profundamente anidados pueden quedar truncados | El gate del cierre terminal exige recuentos exactos y compara las violaciones visibles con las previstas | Aceptado, no bloqueante |
| TC-AF-I01 | INFO | SEM no es un detector universal de lenguaje natural: reconoce el vocabulario de estados y afirmaciones que fijaron las capas, no cualquier redacción | Las afirmaciones se revisan además en la auditoría independiente; el vocabulario no se amplía aquí | Aceptado, no bloqueante |
| TC-H4 | INFO | `README.md` conservaba en su bloque «Estado vigente F34E» la frase «F35-SBX AÚN NO INICIADA», anterior a F35-SBX | Tras el cierre global esa frase sería engañosa | Corregido por la transición de este incremento (§3.2) |

Ninguno bloquea el cierre global: los tres LOW afectan a la fuerza de comprobaciones internas de B, ya acotadas y congeladas; los dos INFO no afectan a ningún criterio de §2.4.

### 2.7 Invariantes

1. Solo cambian `CLAUDE.md`, `docs/PROGRESS.md`, `docs/academico/ACADEMIC_BASELINE.md` y `README.md`, mediante la transición única de §3.2, y se añaden las tres rutas de esta capa.
2. A y B conservan sus bytes y su historia desde sus anclas.
3. Los doce estados de gobierno distintos de F35-SBX no cambian.
4. No hay runtime, CI, dependencias, dataset, migraciones, endpoints ni capacidades nuevas.
5. Los gates congelados no se modifican. Siguen valiendo anclados sobre sus anclas, y el gate de este incremento es el gate sucesor sobre HEAD.

### 2.8 Delta permitido y criterios de aceptación

| Ruta | Estado frente a `f082b41` | Contenido |
|---|---|---|
| `docs/academico/evidencia-sbx-cierre-global/F35SBX_Cierre_Global.md` | A | Este documento |
| `docs/academico/tools/f35sbx_cierre_global/validate_f35sbx_cierre_global.py` | A | Gate sucesor sobre HEAD |
| `docs/academico/tools/f35sbx_cierre_global/test_f35sbx_cierre_global.py` | A | Batería GC01..GC35 |
| `CLAUDE.md`, `docs/PROGRESS.md`, `docs/academico/ACADEMIC_BASELINE.md` y `README.md` | M | Solo mediante la transición de §3.2 |

El cierre queda aceptado como candidato si se cumple todo:

- el gate da 12/0 sobre la rama y sobre los merges `--no-ff` en `develop` y `main` (GC02);
- la batería da 35/35, con todos los negativos rechazados;
- los controles de mutación del gate se detectan;
- `validate_f34e.py` da SBX 18/18 y solo su falla histórica de clase A (DH-B13), y los validadores afectados siguen en verde;
- enlaces y MANIFEST sin discrepancias, y `git diff --check` limpio.

### 2.9 Amenazas

| Amenaza | Qué la rechaza | Casos |
|---|---|---|
| Ataque: declarar F35-SBX cerrada sobre una historia distinta de la integrada | CTX, ANC, GOV y FRZ | GC28..GC30, GC33 |
| Ataque: alterar A o B después del cierre | INT y ALC | GC13, GC14 |
| Ataque: reabrir F35-SBX o volver al gobierno anterior | GOV y SEM | GC05..GC07, GC34 |
| Ataque: habilitar F36, F36-SBX, la G0 real, el alcance C o los datos reales, o cambiar RF-29 | GOV y SEM | GC08..GC12, GC35 |
| Ataque: tocar el runtime o el dataset | ALC y SBX | GC15, GC16 |
| Ataque: ocultar o reclasificar un riesgo | RSK y FRZ | GC17, GC18 |
| Ataque: afirmar una capacidad prohibida o quitar un límite en este documento | SEM y FRZ | GC19, GC20 |
| Ataque: archivos fuera del delta | ALC | GC21 |
| Ataque: entorno de Git hostil o incompleto | ENT, FLG, CTX y fallo cerrado | GC22..GC27 |
| Ataque: código de la capa con dependencias o ejecución dinámica | DEP y FRZ | GC31, GC32 |

## 3. Diseño

### 3.1 Rama, base y commits

- **Base:** `develop` integrado, `f082b4165ca756659b998716e2647494a3ec7be6`.
- **Rama:** `chore/f35-sbx-global-closure`, en un worktree hermano del checkout del equipo, que no se toca.
- **Commits:**
  1. RED: este documento y la batería, sin gate.
  2. Transición de gobierno: un solo padre; cambia exactamente las cuatro rutas de §3.2.
  3. GREEN: el gate, que registra la transición (ya existe: no hay autorreferencia), y los resultados de §5. Es el commit que completa la capa y su ancla.

### 3.2 Delta de gobierno

La transición aplica una lista cerrada de reemplazos literales a los blobs de `f082b41`, cada bloque antiguo presente exactamente una vez:

- `CLAUDE.md`: `d4ba0968e6ebbcaca667d47954db46f7088fae9a`;
- `docs/PROGRESS.md`: `a6322415e7705395dde1e185a3e501155f1989f5`;
- `ACADEMIC_BASELINE.md`: `e9fb4bbbc1534802fc196cca021eeeef69414571`;
- `README.md`: `a4cecb0fe904a698228f5c06910d00970b45ffa1`.

El gate calcula el resultado por su cuenta. Los enlaces se escriben relativos a cada ruta.

```text
Las cuatro rutas, el estado de F35-SBX en la lista de los trece estados
  antes:   - F35-SBX = HABILITADA
  después: - F35-SBX = CERRADA Y CONGELADA

CLAUDE.md, docs/PROGRESS.md y ACADEMIC_BASELINE.md, en el estado vigente
  antes:   F35-SBX exclusivamente sintético.
  después: F35-SBX CERRADA Y CONGELADA solo como sandbox académico y sintético: F35-SBX-A y F35-SBX-B cerradas e integradas.

CLAUDE.md, docs/PROGRESS.md y ACADEMIC_BASELINE.md, el final del estado vigente
  antes:   …/F35SBXB_Cierre_Terminal.md). F36–F40 siguen BLOQUEADAS.
  después: …/F35SBXB_Cierre_Terminal.md). F35-SBX está CERRADA Y CONGELADA, con su cierre global registrado en [`evidencia-sbx-cierre-global`](…/F35SBX_Cierre_Global.md). F36–F40 siguen BLOQUEADAS: ninguna F36-SBX empieza sin una autorización sucesora nueva, con su propia gobernanza.

docs/PROGRESS.md, cabecera
  antes:   Última actualización: 2026-10-21 (…; F35-SBX sintética HABILITADA; F35-SBX-A CERRADA E INTEGRADA; B0 CERRADA E INTEGRADA; F35-SBX-B CERRADA, CONGELADA E INTEGRADA: B1, B2 y B3 CERRADAS E INTEGRADAS).
  después: Última actualización: 2026-10-24 (…; F35-SBX CERRADA Y CONGELADA solo como sandbox académico y sintético: F35-SBX-A, B0 y F35-SBX-B CERRADAS E INTEGRADAS; F36–F40 BLOQUEADAS).

docs/PROGRESS.md, nota de historia
  antes:   … El 21/10/2026 pasó a F35-SBX-B cerrada, congelada e integrada, con B3 auditada e integrada y su cierre terminal registrado.
  después: … El 21/10/2026 pasó a F35-SBX-B cerrada, congelada e integrada, con B3 auditada e integrada y su cierre terminal registrado. El 24/10/2026 pasó a F35-SBX cerrada y congelada, con su cierre global registrado.

README.md, en el bloque «Estado vigente F34E» (TC-H4)
  antes:   F35-SBX exclusivamente sintético. F35-SBX AÚN NO INICIADA.
  después: F35-SBX CERRADA Y CONGELADA solo como sandbox académico y sintético: F35-SBX-A y F35-SBX-B cerradas e integradas, con su cierre global registrado en [`evidencia-sbx-cierre-global`](docs/academico/evidencia-sbx-cierre-global/F35SBX_Cierre_Global.md).
  antes:   Próximo trabajo autorizado aquí: handoff macOS, no iniciar F35-SBX.
  después: F36–F40 siguen BLOQUEADAS y ninguna F36-SBX empieza sin una autorización sucesora nueva, con su propia gobernanza.
```

En `README.md` solo cambian esas tres líneas del bloque vigente. Las fotografías históricas, los documentos de F34E y los de cada capa de B no se reescriben: registran el estado de su momento, y la decisión de F34E se conserva tal como se tomó.

### 3.3 Gate sucesor

Ubicación: `docs/academico/tools/f35sbx_cierre_global/validate_f35sbx_cierre_global.py`. Solo biblioteca estándar, sin red, aislado (`python -I`, al que se relanza solo), con objetos Git verificados recalculando su identificador y con fallo cerrado ante cualquier error o estado no evaluable.

| ID | Comprueba |
|---|---|
| ENT | Intérprete aislado y sin `PYTHONPATH`, `PYTHONHOME` ni `PYTHONUSERBASE`; ninguna variable de Git que redirija el repositorio, el índice o los objetos; Git sobre el repositorio de este archivo, con historia completa, sin injertos ni objetos de reemplazo |
| CTX | Rama `chore/f35-sbx-global-closure`, `develop` o `main`, y el merge `f082b41` como ancestro de HEAD |
| ANC | Las quince anclas de §1.1 desde el commit E de A hasta `f082b41`, verificadas y ancestros de HEAD; `f082b41`, con los padres `53c0eb5` y `9ebb909` y el árbol `7e122321` de su ancla |
| INT | Estado de A y de B: las carpetas de A y los cinco validadores que A adaptó, idénticos a E; las carpetas de B, del cierre terminal incluido, idénticas a `9ebb909`; en cada commit posterior a `f082b41`, en el índice y en el disco |
| FLG | Ningún flag en el índice |
| GOV | Transición única y monotónica de los blobs de `f082b41` a los del cierre global, en las cuatro rutas a la vez, y registrada |
| SEM | Semántica del gobierno vigente y de este documento, con las piezas verificadas de los gates de B1 y R2-A (§3.6) |
| SBX | SBX-01..SBX-18 recalculados uno por uno sobre HEAD con `sbx_eval()` del gate de B1, cargado de los bytes verificados de su blob (DH-B13) |
| RSK | Los cinco riesgos de §2.6, con su nivel y su estado |
| ALC | Alcance exacto frente a `f082b41` en HEAD, el índice y el árbol de trabajo; ningún archivo sin seguimiento |
| FRZ | Nivel B: un único commit posterior a `f082b41` completa la capa; desde él, nada de la capa cambia. La línea INFO informa ese commit |
| DEP | Biblioteca estándar autorizada; la única ejecución dinámica es la carga verificada de los gates de B1 y R2-A |

**Por qué un gate proporcional (DG-01).** B1, §5, fija lo que exige la sucesión después de B: el gate de B pasa a ser histórico y se ejecuta anclado sobre su cierre, y la fase siguiente aporta un gate sucesor sobre HEAD que verifica la integridad de B y recalcula SBX-01..SBX-18. No exige ejecutar sobre HEAD los gates congelados de cada capa, cosa que AF-M01 pidió solo dentro de B. Este gate no los ejecuta:

- la identidad verificada de `f082b41` fija toda la historia auditada de A y de B;
- INT exige que sus bytes no cambien;
- el gate del cierre terminal ya dio 15/0 anclado sobre `9ebb909` y sobre los dos merges, y esa evidencia se reutiliza.

Así el gate tarda segundos, no minutos, y no añade otra cadena de gates anidados.

**Los gates congelados sobre HEAD (DG-02).** Después de este incremento, los gates de A a B fallan sobre HEAD por diseño: su vocabulario solo admite «F35-SBX = HABILITADA». No es una regresión. Siguen acreditando sus estados sobre sus anclas, y `validate_f34e.py` conserva su falla histórica (DH-B13, clase A), que obliga a la evaluación sucesora completa de SBX-01..SBX-18 que hace este gate.

### 3.4 SBX-01..SBX-18

SBX carga el gate de B1 desde los bytes de su blob en `8e94a60`, verificados, y ejecuta su `sbx_eval()`. Esa función verifica contra E los bytes de `validate_f34e.py` y de todo el código que este carga, y solo entonces ejecuta su `compute_sbx()` con esos bytes. Cada criterio produce su ID, PASS o FAIL, su fuente y la comprobación aplicada, en una línea INFO. Un criterio en FAIL o no evaluable hace fallar SBX: sería un incumplimiento sustantivo (DH-B13, clase B) y revocaría G0-SBX.

### 3.5 GOV

- Las cuatro rutas de gobierno tienen en `f082b41` los blobs de §3.2.
- Cada commit posterior a `f082b41` en la historia de HEAD tiene los blobs de `f082b41`, si no desciende de la transición, o los del cierre global, si desciende de ella o es ella.
- Solo la transición los introduce, en las cuatro rutas a la vez: con un solo padre, que tiene los blobs de `f082b41`, y sin cambiar otras rutas.
- La transición derivada coincide con la registrada.
- HEAD, el índice y el disco tienen los blobs del cierre global.

### 3.6 SEM

En las cuatro rutas de gobierno:

- una única sección «Estado vigente F34E», con los trece estados exactos y F35-SBX CERRADA Y CONGELADA;
- las frases del cierre de §3.2 presentes;
- en `CLAUDE.md`, `docs/PROGRESS.md` y `ACADEMIC_BASELINE.md`, también la declaración del cierre de F35-SBX-B y «RF-23 sigue humana; RF-29 sigue experimental/informativa.»;
- ninguna frase anterior al cierre, como «F35-SBX = HABILITADA», «F35-SBX AÚN NO INICIADA» o «no iniciar F35-SBX»;
- ninguna reapertura de F35-SBX, F35-SBX-A, F35-SBX-B, B1, B2 o B3;
- ninguna declaración contradictoria con el vocabulario del cierre, en lo vigente y en las líneas nuevas;
- ninguna afirmación positiva que habilite una capacidad prohibida en las líneas nuevas.

Este documento pasa las mismas comprobaciones: sin datos personales, afirmaciones positivas ni declaraciones contradictorias, y con los catorce límites de §2.5. Los bloques de código citan literalmente el gobierno anterior y el nuevo, así que no cuentan como declaraciones de estado, pero sí se revisan en busca de afirmaciones positivas.

| Vocabulario | Admitido |
|---|---|
| F35-SBX | Cerrada o congelada |
| F35-SBX-A | Cerrada |
| F35-SBX-B, B1, B2 y B3 | Cerradas o congeladas (B1, B2 y B3 también implementadas) |
| F36, F36-SBX y F36–F40 | Bloqueadas o en una forma negada |
| Los demás estados | Los de la G0-SBX vigente |

### 3.7 RSK

La tabla de §2.6 contiene exactamente una fila por riesgo:

- B3-AF-L01, B3-AF-L02 y B3-R3, con LOW y «Aceptado, no bloqueante»;
- TC-AF-I01, con INFO y «Aceptado, no bloqueante»;
- TC-H4, con INFO y «Corregido por la transición de este incremento (§3.2)».

Ninguna otra fila de tabla los presenta con otra severidad o como resueltos.

### 3.8 Raíz de confianza y ancla de este incremento

- **Registradas en el gate:** las anclas de §1.1, los blobs de gobierno y la transición del cierre global, en el commit GREEN.
- **Derivada y registrada fuera:** el commit que completa la capa (nivel B), que el gate informa en la línea INFO de FRZ. La auditoría la anota y comprueba que coincide; ningún archivo guarda su propio hash.
- **El merge de `main` (`57eeb53`)** no es ancestro de esta rama. GC02 prueba la integración `--no-ff` sobre él.

## 4. Pruebas

Cada caso trabaja en un clon desechable de HEAD, fuera del repositorio, con objetos compartidos de solo lectura (en GC24, un clon superficial), configuración de Git aislada, identidad ficticia y fechas fijas. Ejecuta el gate con `python -I` y pasa si fallan exactamente las reglas esperadas.

| Caso | Escenario | Reglas en falla esperadas |
|---|---|---|
| GC01 | Estado válido; el ancla derivada es el commit que completa la capa | Ninguna (PASS) |
| GC02 | Merge `--no-ff` en `develop` (`f082b41`) y después de `develop` en `main` (`57eeb53`) | Ninguna en ambos |
| GC03 | Commit posterior sin cambios de contenido | Ninguna |
| GC04 | Ataque: un blob de gobierno más tras la transición | GOV |
| GC05 | Ataque: modificar y restaurar el gobierno tras la transición | GOV |
| GC06 | Ataque: vuelta al gobierno del cierre terminal en las cuatro rutas | GOV, SEM y ALC |
| GC07 | Ataque: F35-SBX reabierta en el estado vigente | GOV y SEM |
| GC08 | Ataque: F36–F40 habilitadas | GOV y SEM |
| GC09 | Ataque: F36-SBX iniciada | GOV y SEM |
| GC10 | Ataque: G0 real aprobada | GOV y SEM |
| GC11 | Ataque: alcance C habilitado | GOV y SEM |
| GC12 | Ataque: datos reales permitidos | GOV y SEM |
| GC13 | Ataque: un archivo de A alterado tras el cierre | INT y ALC |
| GC14 | Ataque: el gate del cierre terminal alterado tras el cierre | INT y ALC |
| GC15 | Ataque: archivo del runtime modificado | ALC y SBX |
| GC16 | Ataque: dataset sintético alterado | ALC y SBX |
| GC17 | Ataque: riesgo B3-AF-L02 eliminado de este documento | RSK y FRZ |
| GC18 | Ataque: TC-AF-I01 registrado con otro estado en este documento | RSK y FRZ |
| GC19 | Ataque: este documento afirma que el motor recomienda candidatos | SEM y FRZ |
| GC20 | Ataque: este documento pierde un límite de §2.5 | SEM y FRZ |
| GC21 | Ataque: archivo sin seguimiento en el árbol de trabajo | ALC |
| GC22 | Ataque: flag assume-unchanged en el índice | FLG |
| GC23 | Ataque: variable de Git que redirige el repositorio | ENT |
| GC24 | Ataque: clon superficial | Todas salvo FLG y DEP (fallo cerrado) |
| GC25 | Ataque: objeto de reemplazo en `refs/replace` | ENT |
| GC26 | Ataque: HEAD separado | CTX |
| GC27 | Ataque: rama no permitida | CTX |
| GC28 | Ataque: transición repartida en dos commits | GOV |
| GC29 | Ataque: transición introducida en un merge | GOV |
| GC30 | Ataque: historia del cierre reconstruida con el mismo contenido | GOV |
| GC31 | Ataque: la batería importa un módulo no autorizado | DEP y FRZ |
| GC32 | Ataque: la batería ejecuta código dinámico | DEP y FRZ |
| GC33 | Ataque: el cierre construido sobre `9ebb909` sin su integración `f082b41` | CTX, ANC, GOV y FRZ |
| GC34 | Ataque: `README.md` devuelto a «F35-SBX AÚN NO INICIADA» | GOV y SEM |
| GC35 | Ataque: RF-29 declarado fuera de lo experimental | GOV y SEM |

Si un conjunto resulta distinto al medirlo en GREEN, se corrige con su causa registrada en §5, como en las capas anteriores.

## 5. Resultados

### 5.1 Commits

| Commit | Padre | Contenido | Resultado |
|---|---|---|---|
| `7746bf2c5182182fa419915b896bb08def503491` | `f082b41` | Contrato y diseño (§1 a §4) y la batería GC01..GC35 (RED) | Batería 0/35, con 30 ejecuciones: el gate no existía en HEAD, y GC06, GC07, GC09, GC28, GC29 y GC34 dependen de la transición o del gate, que aún no existían |
| `c73611cb992dffd6e4be1fe49bce8b03b53506cd` | `7746bf2` | Transición de gobierno (§3.2): solo `CLAUDE.md`, `docs/PROGRESS.md`, `ACADEMIC_BASELINE.md` y `README.md`, con los blobs `2e988f22864ad86b05395d0d8a91110d9631c4a3`, `200355350414dceaac1ab39ba835f1e7c18a662d`, `5e523302279948389c78cb9dca70b82f5c7b92e4` y `0ed030e53d49f2c8a5f1dc5fca1269b6109020a3` | `GC_TRANSITION`, registrada en el gate del commit siguiente |
| El que completa la capa (este) | `c73611c` | Gate, correcciones de §5.2 y estos resultados (GREEN) | Gate 12/0; batería 35/35; 15 de 15 mutaciones detectadas |

Ese tercer commit es el ancla de nivel B de esta capa. Lo informa la línea INFO de FRZ, y su hash no se guarda en ningún archivo.

### 5.2 Medición y correcciones

Todo se midió el 24/10/2026, con temporales nuevos y exclusivos y sin ningún síntoma ambiental. El gate, la batería y los controles de mutación corrieron de uno en uno; los validadores, que son ligeros, coincidieron dos veces con la batería. El gate tarda unos 8 segundos. La batería, los controles de mutación y los validadores se ejecutaron sobre commits desechables hijos de la transición `c73611c`, en copias completas sin alternates. Su gate y su batería son, byte a byte, los de este commit, y el último de ellos tiene el árbol de este commit.

Correcciones, cada una con su causa medida antes de aplicarla:

- **GC06, expectativa de la batería.** La vuelta al gobierno del cierre terminal deja las cuatro rutas de gobierno con los blobs de `f082b41`, así que ya no figuran como modificadas frente a la base y ALC también rechaza el alcance. Es una detección correcta que la expectativa de RED no previó: GC06 espera ahora GOV, SEM y ALC. Se corrige también la fila de §4.
- **Precisiones de redacción de RED.** En §2.8 y §3.3, la falla de `validate_f34e.py` ya no es solo de alcance: también nombra el estado nuevo de F35-SBX (§5.6). ANC verifica las quince anclas de §1.1 desde el commit E hasta `f082b41`, no los commits de F34E ni los merges de `main`, que no son ancestros de esta rama.
- **INT, revisión del disco (autoauditoría, antes de este commit).** Un borrador del gate omitía las carpetas `__pycache__` al revisar el disco de las capas congeladas, algo que el gate del cierre terminal no admite. Se restauró la comprobación idéntica a la suya, y todas las mediciones de esta sección son posteriores.

### 5.3 Gate

| Dónde | Resultado |
|---|---|
| Rama, sobre un commit desechable con el árbol de este commit | 12/0 |
| Merge `--no-ff` en `develop` (`f082b41`) y de ese merge en `main` (`57eeb53`) | 12/0 y 12/0 (GC02) |

Líneas INFO:

- ANC: las quince anclas registradas, de `61f94e2` a `f082b41`, verificadas y ancestros de HEAD, más la transición registrada.
- SBX: una línea por criterio, SBX-01..SBX-18 en PASS, con su fuente y su comprobación.
- GOV: transición derivada `c73611c`, igual a la registrada.
- FRZ: el commit que completa la capa.

### 5.4 Batería

**35/35**, con 36 ejecuciones del gate en unos cuatro minutos: cada caso dio exactamente el resultado de §4 y, donde se indica, con su motivo.

### 5.5 Controles de mutación

Quince mutaciones del gate, cada una sobre un commit desechable cuyo gate solo difiere del de este commit en la sentencia mutada, con el caso que debe detectarla. Las quince se detectan:

| # | Mutación del gate | Caso | Resultado |
|---|---|---|---|
| M01 | ENT sin rechazar las variables de Git que redirigen el repositorio | GC23 | Detectada: GC23 pasa a PASS |
| M02 | CTX sin exigir una rama permitida | GC27 | Detectada: GC27 pasa a PASS |
| M03 | ANC sin exigir las anclas como ancestros de HEAD | GC33 | Detectada: deja de fallar en ANC |
| M04 | INT sin la capa de A | GC13 | Detectada: deja de fallar en INT |
| M05 | GOV sin comparar la transición derivada con la registrada | GC30 | Detectada: GC30 pasa a PASS |
| M06 | SEM sin la declaración canónica del estado vigente | GC35 | Detectada: deja de fallar en SEM |
| M07 | SEM sin las afirmaciones positivas de este documento | GC19 | Detectada: deja de fallar en SEM |
| M08 | SEM sin los límites de §2.5 | GC20 | Detectada: deja de fallar en SEM |
| M09 | SBX sin registrar los criterios en FAIL | GC15 | Detectada: deja de fallar en SBX |
| M10 | RSK sin efecto | GC17 | Detectada: deja de fallar en RSK |
| M11 | Sin ALC | GC21 | Detectada: GC21 pasa a PASS |
| M12 | Sin FRZ | GC17 | Detectada: deja de fallar en FRZ |
| M13 | DEP sin comprobar las importaciones | GC31 | Detectada: deja de fallar en DEP |
| M14 | DEP sin buscar ejecución dinámica | GC32 | Detectada: deja de fallar en DEP |
| M15 | FLG sin efecto | GC22 | Detectada: GC22 pasa a PASS |

### 5.6 Validadores y comprobaciones afectados por el delta

| Comprobación | Resultado |
|---|---|
| `validate_f35sbx_cierre_global.py` | 12/0 (§5.3) |
| `test_f35sbx_cierre_global.py` | 35/35 (§5.4) |
| `validate.py` y `validate.py --cierre-f29` | 0 fallas en ambos |
| `validate_f29.py`, `test_f32_safety.py`, `validate_f33.py` y `validate_f34.py` | 225/0, OK, 451/0 y 403/0 |
| `validate_f34a.py` | 108/0. Necesita una rama local `develop`: en un clon sin ella falla cerrado en su regla GIT, igual que sobre la base |
| `validate_f34e.py` | 247/1, la falla histórica de su regla GIT, con «criterios SBX: 18/18 cumplen». Su lista de rutas no autorizadas por DH-02 pasa de 37 a 40, las tres de esta capa, sin que desaparezca ninguna. Su vocabulario congelado solo admite HABILITADA o BLOQUEADA para F35-SBX, así que la regla añade «F35-SBX = CERRADA Y CONGELADA no admitido» en las cuatro rutas de gobierno. Es una falla histórica de ciclo de vida (DH-B13, clase A), no un incumplimiento de SBX-01..SBX-18 |
| `test_sbxb_pipeline.py` | 30/30 |
| Enlaces relativos | 1166 en `docs/academico` y 1575 en todo el repositorio, 0 rotos |
| MANIFEST y evidencias | 61 hashes y 0 discrepancias; 81 hashes de las evidencias de las prácticas 03, 05, 08 y 11, 0 discrepancias |
| `git diff --check` | Limpio frente a `f082b41` |
| Delta frente a `f082b41` | Exactamente las tres rutas de la capa (A) y las cuatro de gobierno (M) |

### 5.7 SBX-01..SBX-18

Recalculados uno por uno sobre HEAD por SBX, con `sbx_eval()` del gate de B1 verificado en su ancla: 18/18 en PASS, con su fuente y su comprobación (§5.3). `validate_f34e.py` también da «criterios SBX: 18/18 cumplen». Ningún hecho REV-01..REV-14: G0-SBX sigue APROBADA CON RESTRICCIONES.

### 5.8 Evidencia reutilizada

No se repitió nada cuya evidencia sigue valiendo por la identidad de los commits, los árboles y el CI:

| Evidencia | Por qué vale sin repetirla |
|---|---|
| El cierre terminal: gate 15/0, batería 36/36, 20 mutaciones, sondas P1..P7 y la auditoría independiente | `9ebb909` y sus merges conservan su identidad, y INT exige que B no cambie |
| Los gates anclados de A a B (A 846/0, B1 159/0, B1-FREEZE 14/0, B2 119/0, B2-FREEZE 10/0, sucesor 7/0, B2-SUCCESSOR-FREEZE 12/0, cierre de gobierno 13/0, R2-A 14/0, B3 19/0 y el cierre terminal 15/0) | Se ejecutan sobre sus anclas, que no cambian; este incremento no toca sus bytes |
| PHPUnit, TypeScript y la compilación del frontend | CI 66 y 67 en verde sobre `f082b41` y `57eeb53`; este incremento no toca el runtime |
| Cypress | Fuera del alcance: el delta es solo documentación y gobierno |

### 5.9 Autoauditoría

Se intentó romper el cierre por cada vía de la consigna, con el resultado medido:

| Intento | Qué lo rechaza | Evidencia |
|---|---|---|
| Ataque: cierre circular o autorreferente | El gate registra solo hashes que existían antes que él; el ancla de esta capa la deriva FRZ y se registra fuera | §3.8 y GC01 |
| Ataque: falso PASS por un gate debilitado | La batería | 15 de 15 mutaciones detectadas (§5.5) |
| Ataque: estado contradictorio o reapertura | GOV y SEM | GC05..GC07 y GC34 |
| Ataque: habilitar F36, F36-SBX, la G0 real, el alcance C o los datos reales | GOV y SEM | GC08..GC12 |
| Ataque: relajar G0-SBX o perder una restricción | SEM y SBX: los trece estados exactos y SBX-01..SBX-18 recalculados | GC10..GC12, GC15 y GC16 |
| Ataque: reinterpretar un riesgo | RSK y FRZ | GC17 y GC18 |
| Ataque: afirmar una capacidad prohibida o quitar un límite | SEM y FRZ | GC19 y GC20 |
| Ataque: cambios fuera del alcance, en A, en B, en el runtime o en el dataset | ALC, INT y SBX | GC13..GC16 y GC21 |
| Ataque: historia distinta de la integrada | CTX, ANC, GOV y FRZ | GC28..GC30 y GC33 |
| Ataque: entorno de Git hostil o incompleto | ENT, FLG, CTX y fallo cerrado | GC22..GC27 |

| # | Nivel | Hallazgo | Tratamiento |
|---|---|---|---|
| GC-H1 | LOW | La expectativa de RED de GC06 no preveía la detección de ALC | Corregida con su causa medida (§5.2), sin cambiar el gate |
| GC-H2 | LOW | Un borrador del gate omitía `__pycache__` en la revisión del disco de las capas congeladas | Corregido antes de este commit: la comprobación es la del gate del cierre terminal |
| GC-H3 | INFO | `validate_f34e.py` añade a su falla histórica el estado nuevo de F35-SBX, que su vocabulario congelado no admite | Clasificado como falla histórica de ciclo de vida (DH-B13, clase A): SBX-01..SBX-18 se recalculan aquí y siguen en PASS. El validador congelado no se modifica |
| GC-H4 | INFO | `validate_f34a.py` necesita una rama local `develop` | Condición del entorno, igual sobre la base; no es una regresión |
| GC-H5 | INFO | El detector de afirmaciones de B1 trata como concesión cualquier mención de F36 que no esté negada | La regla se redacta en forma negada: «ninguna F36-SBX empieza sin una autorización sucesora nueva» |
| GC-H6 | INFO | Los documentos de F34E y los de A conservan «F35-SBX = HABILITADA» | Son registros históricos de su momento y no se reescriben (§3.2); el estado vigente está en el gobierno |

No quedó ningún hallazgo BLOCKER, HIGH ni MEDIUM abierto.

### 5.10 Riesgos residuales

Los riesgos de §2.6 se conservan tal como los clasificaron sus auditorías, sin corregirlos ni reclasificarlos. Además:

| # | Nivel | Riesgo | Tratamiento |
|---|---|---|---|
| GC-R1 | INFO | El gate no ejecuta los gates congelados sobre HEAD (DG-01) | La identidad de `f082b41` fija la historia auditada, INT exige que A y B no cambien y los gates congelados siguen valiendo anclados |
| GC-R2 | INFO | El ancla de nivel B solo autentica la capa si se registra fuera | La auditoría anota el commit que informa FRZ |
| GC-R3 | INFO | El gate trabaja sin red y no verifica `57eeb53`, que no es ancestro de esta rama | GC02 prueba los merges `--no-ff` sobre `f082b41` y `57eeb53`; el CI de la integración se comprueba al integrar |
| GC-R4 | INFO | SEM hereda el límite de TC-AF-I01: no es un detector universal de lenguaje natural | La auditoría independiente revisa además las afirmaciones |

### 5.11 Pendientes

- La auditoría independiente de este incremento, sobre su ancla: el commit que informa FRZ.
- Con su aprobación y la autorización expresa del equipo, la publicación de la rama y su integración `--no-ff` en `develop` y `main`, con CI en verde. Este incremento no hace push, merge, tag ni release.
- Ninguna fase posterior queda en curso: F36–F40 siguen BLOQUEADAS, y ninguna F36-SBX empieza sin una autorización sucesora nueva.
- Los pendientes externos de la G0 real (G0-02, G0-03 y G0-12), que este cierre no cambia.
