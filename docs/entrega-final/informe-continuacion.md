# Informe de la continuación F36–F40

> Rama local `feature/continuacion-f36-f40`, creada el 08/11/2026 desde `f5003c967e0caa19f4236bae0705de08f33fae12`: el commit de la demo auditada, con APTO PARA PRESENTAR. Worktree `D:/Universidad/PruebasCalidadSoftware/Project/continuacion-f36-f40-20261107/worktree`. **Entrega local:** sin push, merge, tag ni release. El hash del commit candidato se consulta en Git; este documento no lo anticipa.
>
> **Estados vigentes, sin cambios:** F36-SBX = EN DISEÑO; F36-SBX-GATE = NO SUPERADO; F37-SBX = BLOQUEADA; F36–F40 = BLOQUEADAS; alcance C = BLOQUEADO; datos reales = PROHIBIDOS; Q2 ADOPTADA (RR-001), sin facultades delegadas utilizables. Ningún acto, voto ni delegación se emite aquí.

## 1. Entorno

| Elemento | Valor |
|---|---|
| Proyecto Docker | `continuacion`: app en `http://localhost:8020`, E2E en 8021, PostgreSQL en 5452 y Redis en 6399, todo en loopback salvo la app. Volúmenes `continuacion_*` |
| Base de datos | `continuacion_pgdata`, solo con datos de `DemoSeeder`. Antes de cargarla se comprobó que la app apunta a su PostgreSQL (`172.25.0.2`, red `continuacion_default`) |
| Demo de la exposición | Intacta: `feature/entrega-academica-demo` en `f5003c9`, su worktree y el proyecto `entregaacad`, con sus volúmenes. No se usaron para estas pruebas |
| Checkout principal | `4a2b2d7`, limpio, con el stash. El proyecto `reclutamiento` no se tocó |
| `.env` y `.env.e2e` | Propios de esta rama e ignorados por Git |

## 2. Estado por fase

> Corresponde al 08/11/2026. Las correcciones y los recuentos del 09/11/2026 están en §3.1.

### F36 · B-01: especificación S v2

| | Contenido |
|---|---|
| **Implementado** | Nada en el validador: B-01 exige D-02b |
| **Preparado** | [S v2](../academico/f36-sbx/expediente-final/F36SBX_B01_Especificacion_S.md): T-09 medido con siete sondas reales del validador (§5.9.1), su efecto sobre la selección de H (§5.9.2), opciones (a-i), (a-ii), (b), (c) y (d) (§5.9.3), invariante I-14, pruebas S-T11 a S-T17, criterios de aceptación AC-01 a AC-14 (§10), dependencias (§11) y puntos de auditoría (§12) |
| **Hallazgo principal** | Sobre `main` (`55f758e`, árbol de AF5), el expediente completo posterior a SEG da **59/0** (V-5). Sobre `develop` da 56/3, por SEG (V-2 y V-4). Los subárboles del paquete y de sus herramientas son idénticos en ambas ramas. Recomendación técnica, no vinculante: (a-ii), una rama de H nueva desde el commit `55f758e` |
| **Pendiente** | D-10 determinada (P-S1; para T-09 (b) además D10-1); auditoría de S (P-S2); D-02b por el mecanismo colegiado (P-S4); merges y push de H con autorización explícita del equipo del contrato 10 (D-11 fijaría el formato) |

### F37 · Evidencias

| | Contenido |
|---|---|
| **Implementado** | Un prototipo **separado de la aplicación**, en memoria y con la biblioteca estándar: flujo, matriz de roles y reglas R-01 a R-09. No implementa ninguna EI |
| **Preparado** | [Especificación del flujo mínimo](../academico/preparacion-f37-evidencias/F37_Flujo_Minimo_Evidencias.md): piezas reutilizables del SaaS, flujo, permisos de los cinco roles, aislamiento y huecos de integración. Más 33 escenarios ficticios en dos organizaciones |
| **Pendiente** | Nivel A, sandbox F37-SBX-A: F36-SBX-GATE SUPERADO anclado en H, con FG-02, FG-03 (lista cerrada de EI), FG-10 y FG-12. Nivel B, SaaS: **bloqueado por EI-23**; exige la G0 real y una decisión N5 |

### F38 · ML-02

| | Contenido |
|---|---|
| **Implementado** | Un arnés de evaluación **sin método**, fuera del SaaS: métricas M-01 a M-08, M-11 y M-12, sello de `test`, intervalo bootstrap por vacante e invalidaciones |
| **Preparado** | [Conjunto, resultados esperados y criterios](../academico/preparacion-f38-ml02/F38_Conjunto_Evaluacion_ML02.md): 12 fragmentos sintéticos, `dev` y `test` sellado, oro de EI-01 a EI-07 y EI-09, y dos salidas escritas a mano con sus valores calculados de antemano. También la especificación de datos, etiquetas y particiones que exigiría un entrenamiento (§7) |
| **Pendiente** | Métodos de EI-01 a EI-07: el gate y FG-03. EI-09: F36-M02, FG-12 y el preregistro. Entrenamiento: **bloqueado** (EI-22; requisito exacto en §7). Integración: **bloqueada** (EI-23). La decisión de selección sigue en manos de Dirección |

### F39 y F40 · Diseño y verificación

| | Contenido |
|---|---|
| **Implementado** | **Cronograma del proceso** en el detalle de la vacante (`/vacantes/{id}`). Cuatro hitos (publicación, cierre de postulaciones, plazo objetivo y cierre), un solo hito en curso (`aria-current="step"`), el estado en texto además del color, el avance «Día N de M» y el apilado vertical en móvil. Solo usa fechas que la vacante ya tiene: **no estima nada**, y la estimación sigue siendo la tarjeta de ML-01, aparte. Reutiliza `Section`, los tokens `--tone-*`, `formatDate` y los iconos existentes. Sin backend, sin dependencias y fuera del 3D (ADR-003) |
| **Alcance** | Línea visual ordinaria (roadmap §4, fila V1): no depende de la G0, del gate ni de F37-SBX. No crea un RF nuevo: presenta datos de RF-05 a RF-07 y de GAP-01 |
| **Recorrido** | El paso 7 del [guion](guion-demo.md) empieza por el cronograma. E2E-20 pasa de 7 a 12 tests |
| **Pendiente** | Las pruebas manuales con lector de pantalla y en un equipo modesto (V1), que exigen herramientas reales |

## 3. Pruebas ejecutadas

Todas se ejecutaron el 08/11/2026 en el proyecto `continuacion`, salvo las de Python, que corrieron en el anfitrión con `python -I -B`. **No se ejecutaron PHPUnit completo ni la suite completa de Cypress:** no hay cambios de backend, y el encargo pide pruebas dirigidas.

| Prueba | Comando | Resultado |
|---|---|---|
| Componente, RED | `npx vp test --run …/process-schedule.test.tsx`, antes del componente | 1 archivo fallido (import inexistente) |
| Componente, RED del caso límite | Ídem, con dos pruebas nuevas | 2 failed, 10 passed |
| Componentes, regresión | `npx vp test --run` | **7 archivos, 54 passed** |
| Tipos | `npx tsc --noEmit` | 0 errores |
| Lint y formato | `npx vp check` sobre los archivos nuevos | Sin avisos. `format.ts` y E2E-20 ya tenían deuda de formato en la base; solo se ajustó el bloque añadido |
| Build | `npm run build` | Correcto; el componente está en `show-*.js` |
| Cypress E2E-20 | `docker compose -p continuacion --profile e2e run --rm cypress --spec cypress/e2e/e2e-20-recorrido-demo.cy.js` | **12/12**, también tras añadir la comprobación de que el tema oscuro se aplica |
| Cypress dirigido: specs que visitan el detalle de la vacante | `--spec` con E2E-04, 10, 11, 14, 15, 16, 17 y 19 | **41/41 en 8 specs** (3:24) |
| Prototipo de F37 | `python -I -B -m unittest discover -s docs/academico/preparacion-f37-evidencias/prototipo` | **19 passed**; 33/33 escenarios; 6 ablaciones detectadas |
| Arnés de F38 | `python -I -B -m unittest discover -s docs/academico/preparacion-f38-ml02/evaluacion` | **17 passed**; 5 ablaciones detectadas |
| Validador F36 | `python -I -B docs/academico/tools/f36sbx/validate_f36sbx.py` | **55/4**, las mismas cuatro fallas que la entrega: rama no admitida, FRZ por alcance, FRZ por runtime y GATE (FG-01 y FG-05). Frente a `f5003c9`, las rutas externas pasan de 30 a 47 y las entradas de runtime, de 17 a 21. Las 4 de runtime nuevas son `format.ts`, `show.tsx` y el componente con su prueba |
| Sondas de T-09 | S §5.9.1, en worktrees temporales ya eliminados | V-1 59/0; V-2 56/3; V-3 59/0; V-4 56/3; V-5 59/0; V-6 57/2 |
| Revisión visual | Capturas de Electron sin ventana sobre la app de desarrollo (8020), fuera del repositorio | Claro, oscuro, vacante cerrada, borrador y 320 px: correctos |
| Espacios | `git diff --check` | Limpio |

### 3.1 Revisión del candidato `a9fa344` (09/11/2026)

La tabla anterior es la fotografía del 08/11/2026. El 09/11/2026 se revisó ese candidato, sin auditar todavía, y se corrigió sobre la misma rama. Los hechos actualizan §2: S pasa a la versión 2.1, F37 tiene 38 escenarios (12 permitidos y 26 denegados) y 21 pruebas, y F38 tiene 25 pruebas y un sello nuevo.

| Frente | Defecto encontrado | Corrección |
|---|---|---|
| F36 · S | AC-02 admitía registrar el RED en `docs/tdd-evidence.md`, que AC-05 y FRZ rechazan | AC-02 lo deja dentro del paquete |
| F36 · S | S-T11 a S-T17 solo estaban descritas | [`sondas_t09.py`](../academico/preparacion-f36-b01/sondas_t09.py), en un clon desechable (S §5.9.4) |
| F37 | R-05 no veía camelCase y no se aplicaba a enlazar ni a retirar. Una observación podía declararse con fuente `documento_presentado` | R-05 en toda escritura; una sola fuente por tipo; 5 escenarios nuevos |
| F38 | La semilla era 5945 en el código y 2381 en la especificación | Literal 2381, fijado por una prueba |
| F38 | Una tarea fuera del catálogo, una clave camelCase o un valor numérico pasaban. Una salida mal formada rompía el arnés. La partición `train` salía válida. El sello no cubría `k` | Catálogo y forma cerrados; particiones `dev` y `test`; `k` sellado. Sello nuevo: `fb7e7e13f664f93ca9e6fb7cf824a097469034d6096659e980e928d4df3eee72` |
| F39 | Con un plazo no posterior a la publicación decía «Sin plazo objetivo». Un proceso cerrado sin fecha de cierre mostraba un plazo vencido y un hito en curso | Resumen veraz; sin hito en curso en un proceso cerrado |

| Prueba | Comando | Resultado del 09/11/2026 |
|---|---|---|
| Sondas de T-09 | `python -I -B docs/academico/preparacion-f36-b01/sondas_t09.py` | **18 conformes, 0 discrepancias**. S-T11 con la rama admitida en memoria: 59/0, R = NO SUPERADO. Una ablación de lo esperado sale con código 1 |
| F37 | `python -I -B -m unittest discover -s …/prototipo` | RED 2 failed; GREEN **21 passed**; 38/38 escenarios |
| F38 | `python -I -B -m unittest discover -s …/evaluacion` | RED 6 failed y 1 error; GREEN **25 passed** |
| Componente | `npx vp test --run …/process-schedule.test.tsx` | RED 2 failed, 12 passed; GREEN **14 passed** |
| Componentes, regresión | `npx vp test --run` | **56 passed** |
| Tipos | `npx tsc --noEmit` | 0 errores |
| Lint y formato | `npx vp check` sobre el componente y su prueba | Sin avisos |
| Build | `npm run build` | Correcto: el texto nuevo del cronograma está en `show-*.js` |
| **PHPUnit completo** | `php artisan test`, en `continuacion` (base `reclutamiento_testing`) | **447 passed, 8 skipped** (2233 aserciones), 121 s |
| **Cypress** | E2E-20 y los specs que visitan el detalle de la vacante | **NO EJECUTADO en esta revisión.** El sistema detuvo la tarea por falta de memoria (403 MB libres de 16 GB), justo al arrancar Cypress. Los últimos resultados, 12/12 y 41/41, son del 08/11/2026 sobre `a9fa344`. Después solo cambiaron ramas de cálculo del componente, sin tocar `data-cy` ni el marcado; aun así, hay que repetirlo |
| Validador F36 | `python -I -B docs/academico/tools/f36sbx/validate_f36sbx.py` | **55/4**, las mismas cuatro fallas |

Para repetir Cypress, con memoria libre: `docker compose -p continuacion --profile e2e run --rm cypress --spec <E2E-20 y E2E-04, 10, 11, 14, 15, 16, 17 y 19>`, desde este worktree.

### 3.2 Hallazgos MEDIUM de la auditoría de Codex sobre `138ce29` (09/11/2026)

Codex auditó `138ce29` (árbol `cf98578a…`) y dejó tres hallazgos MEDIUM. Se corrigieron en un solo commit, con las pruebas de regresión escritas y ejecutadas primero contra el código auditado. El RED y el GREEN están en [`tdd-evidence.md`](../tdd-evidence.md).

| Hallazgo | Defecto | Corrección |
|---|---|---|
| CONT-M01 · F37 | RR. HH. podía corregir la observación ajena `EVD-S1-0002` declarando `type='cv'` y `source='documento_presentado'`: se creaba un registro nuevo y la observación quedaba sustituida | La corrección se autoriza por el tipo y el autor de la evidencia original antes de mirar los datos de reemplazo: una `observacion` solo la corrige su autor. Las validaciones de la evidencia nueva se conservan |
| CONT-M02 · F38 | Una raíz JSON `[]`, `null`, cadena o número lanzaba `AttributeError` antes de devolver el resultado | `evaluate` valida la raíz antes de `.get()`: `valid = false`, sin métricas y con la causa «la raíz de la salida no es un objeto JSON» |
| CONT-M03 · F38 | En APP-ML-001 / CRI-01-CLASE, `['FRG-004', 'FRG-004', 'FRG-004']` pasaba como válida, con Recall@3 = 1,667 y nDCG@3 = 1,377 | Una lista de recuperación (`fragment_refs` o `fragments`) con IDs repetidos se rechaza antes de calcular métricas, con la causa «identificadores repetidos». El conjunto, la semilla, `k` y el sello no cambian |

| Prueba | Antes de corregir (código de `138ce29`) | Después |
|---|---|---|
| F37, `unittest` | **1 failed** de 23 | **23 passed** |
| F37, escenarios | 38/38 | **38/38** |
| F38, `unittest` | **1 failed y 1 error** de 28 | **28 passed** |
| Sello de `test` | `fb7e7e13…` | `fb7e7e13…`, sin cambios |
| `git diff --check` | — | Limpio |

Codex cerró CONT-M01, CONT-M02 y CONT-M03 en el commit de estas correcciones, `f42259016921e67eea2f1be2d766d1a581cb2f6a` (árbol `1ce27ba7e33cb7a2c8f9c149956b019313d990a5`). Ese commit es la referencia exacta del código auditado y probado. Este informe se actualiza en un commit posterior que solo cambia la documentación: un commit no puede contener los resultados de sus propias pruebas. Los resultados de `a9fa344` no valen como evidencia de este candidato.

**Regresión Cypress sobre `f422590`, 09/11/2026**

| Corrida | Qué se ejecutó | Resultado | Validez como evidencia |
|---|---|---|---|
| Primera, parcial | E2E-20, con `docker compose run --rm` | El sistema detuvo el proceso cliente por falta de memoria (unos 1,8 GB libres). El contenedor terminó con código 0, pero `--rm` lo eliminó antes de guardar su log: solo se observaron 5 de 12 pruebas | **No cuenta.** No hay log completo |
| Segunda, completa | Los 9 specs, uno por vez, cada uno en un contenedor con nombre único (`cy-f422590-<spec>`), en segundo plano y sin `--rm` | **53/53 pruebas aprobadas en 9 specs, todos con código 0**, sin OOM y sin fallos de aserción ni de infraestructura. Memoria libre antes de cada spec: de 1232 a 1754 MB | **Cuenta.** Log, resumen y código de salida se guardaron antes de eliminar cada contenedor |

| Spec | Pruebas | Código de salida | Duración |
|---|---|---|---|
| E2E-20 `e2e-20-recorrido-demo` (repetido) | 12/12 | 0 | 23 s |
| E2E-04 `e2e-04-configure-publish-vacancy` | 2/2 | 0 | 24 s |
| E2E-10 `e2e-10-selection-and-closure` | 1/1 | 0 | 18 s |
| E2E-11 `e2e-11-multitenancy` | 4/4 | 0 | 17 s |
| E2E-14 `e2e-14-target-completion-form` | 4/4 | 0 | 34 s |
| E2E-15 `e2e-15-operational-risk-panel` | 8/8 | 0 | 1 min 4 s |
| E2E-16 `e2e-16-tabla-accesible-movil` | 7/7 | 0 | 17 s |
| E2E-17 `e2e-17-motion-accesible` | 8/8 | 0 | 15 s |
| E2E-19 `e2e-19-qa-visual-accesible` | 7/7 | 0 | 16 s |
| **Total** | **53/53** | **9 de 9 con código 0** | — |

**El entorno `continuacion` servía el código de `f422590`:**
- **Worktree y montaje:** el worktree estaba limpio en ese commit, y `app`, `app-e2e` y `queue-e2e` lo montan en `/var/www/html`.
- **Archivos servidos:** `process-schedule.tsx`, `show.tsx` y el spec E2E-20 tienen el mismo SHA-256 dentro del contenedor y en el anfitrión, y su contenido es idéntico al de `HEAD`.
- **Recursos compilados:** ningún archivo de `resources/` es más reciente que el build. El `manifest.json` servido en el puerto 8021 es idéntico al del anfitrión, y el bundle servido contiene el texto del cronograma.

**Evidencias:** fuera de Git, en `D:/Universidad/PruebasCalidadSoftware/Project/continuacion-f36-f40-20261107/evidencias/cypress-f422590/`. Por cada spec hay tres archivos: `<spec>.log`, `<spec>.summary.txt` y `<spec>.exit`. Además, `manifest.txt` registra el SHA, la memoria y las horas de cada spec, y `verificacion-entorno.txt`, la verificación del entorno. En `SHA256SUMS.txt` están los hashes de esos 29 archivos, comprobados contra los originales.

## 4. Puntos que Codex debe auditar

0. **Revisión del 09/11/2026:** los defectos y correcciones de §3.1; S §12, puntos 7 y 8; que el cambio de sello de F38 se deba solo a `k`; que R-09 (una fuente por tipo) sea una regla razonable del prototipo y no contradiga el contrato v4; y **Cypress, no ejecutado sobre este candidato**.
   - **Corrección de CONT-M01 a CONT-M03 (§3.2):** que la corrección de F37 se autorice por la evidencia original; que ninguna raíz JSON rompa el arnés; que ninguna lista con IDs repetidos llegue a las métricas; y que el sello siga siendo `fb7e7e13…`.

1. **S v2, §12:**
   - que las sondas de §5.9.1 se puedan reproducir y que §5.9.2 no afirme más de lo medido;
   - que (a-ii) no anticipe D-10, D-02b ni T-04;
   - que §11 asigne bien cada dependencia;
   - que no haya ningún acto, voto ni estado del gate.
2. **F37:**
   - que el prototipo no implemente ninguna EI ni toque el runtime;
   - que la matriz sea coherente con `viewFile`, `CandidateDocumentPolicy` y `AuthorizesAssessmentSessions`;
   - que el nivel B de §8 conste como inalcanzable en F37-SBX (EI-23).
3. **F38:**
   - que el arnés no contenga ningún método;
   - que los valores de §5 se puedan recalcular a mano;
   - que el sello cubra todo `test` y nada de `dev`;
   - que §7 especifique sin habilitar el entrenamiento, con el requisito exacto;
   - que ninguna etiqueta se refiera a personas.
4. **F39:**
   - que el cronograma no estime ni hable de personas, y que no toque el ranking, la decisión ni ML-01;
   - accesibilidad: lista ordenada, un solo `aria-current`, estado en texto, contraste en los dos temas y 320 px;
   - que `toCalendarDate` use la misma zona horaria que el resto de las fechas (`meta app-timezone`);
   - el caso del plazo sin fecha.
5. **Gobierno:**
   - que ningún archivo de `GOV_FILES` haya cambiado (CLAUDE.md, README, PROGRESS y ACADEMIC_BASELINE);
   - que los estados formales sigan iguales;
   - que la demo auditada siga intacta.

## 5. Lo que no se hizo, y por qué

| Qué | Motivo |
|---|---|
| Implementar B-01 en el validador | Exige D-02b, que no está emitida |
| Implementar EI, o evidencias en el SaaS | El gate no está superado (EI-01 a EI-07) y EI-23 está BLOCKED |
| Entrenar ML-02 o ejecutar un método sobre evidencia | EI-22 está BLOCKED; no hay método autorizado |
| Sincronizar CLAUDE.md, PROGRESS.md y la trazabilidad | Los estados formales no cambian. Registrar esta continuación en el gobierno es un incremento propio |
| Push, merge, tag o release | Contrato 10: requieren autorización explícita del equipo |
