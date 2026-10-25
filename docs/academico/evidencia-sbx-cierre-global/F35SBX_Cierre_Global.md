# F35-SBX — Cierre global

> **Estado: CONTRATO Y DISEÑO (RED).** Fecha: 24/10/2026. Rama `chore/f35-sbx-global-closure`, desde `develop` = `f082b4165ca756659b998716e2647494a3ec7be6`.
>
> - Este documento reconstruye el alcance global de F35-SBX desde sus contratos, evalúa si puede cerrarse y fija el contrato y el diseño del incremento que registra ese cierre. La transición de gobierno, el gate y los resultados llegan en los commits siguientes.
> - El cierre solo vale en el alcance académico y sintético de F35-SBX, y solo cuando la auditoría independiente apruebe este incremento y el equipo autorice su integración. Hasta entonces, `develop` y `main` siguen diciendo «F35-SBX = HABILITADA».
> - Este incremento no se autoaprueba: lo decide la auditoría independiente sobre su ancla.
>
> Las secciones 1 a 4 registran la reconstrucción, la evaluación, el contrato y el diseño, escritos antes de la transición de gobierno y del gate (commit RED). La sección 5 añade los resultados.

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
- `validate_f34e.py` da SBX 18/18 y solo su falla histórica de alcance, y los validadores afectados siguen en verde;
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
| ANC | Las anclas de §1.1, verificadas y ancestros de HEAD; `f082b41`, con los padres `53c0eb5` y `9ebb909` y el árbol `7e122321` de su ancla |
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

**Los gates congelados sobre HEAD (DG-02).** Después de este incremento, los gates de A a B fallan sobre HEAD por diseño: su vocabulario solo admite «F35-SBX = HABILITADA». No es una regresión. Siguen acreditando sus estados sobre sus anclas, y `validate_f34e.py` conserva su falla histórica de alcance (DH-B13, clase A), que obliga a la evaluación sucesora completa de SBX-01..SBX-18 que hace este gate.

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
| GC06 | Ataque: vuelta al gobierno del cierre terminal en las cuatro rutas | GOV y SEM |
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

Pendiente: se registran en el commit que completa la capa, con las ejecuciones reales.
