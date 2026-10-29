# SEG-01 y SEG-02 — Integración local y validación conjunta

> Integración local del 28/10/2026 en la rama `fix/seg-01-02-integration`. **Candidato combinado pendiente de la revisión de integración de Codex.** No se integró en `develop` ni en `main`, no se publicó, no hay tag ni release, no inicia F37-SBX y no cambia estados formales de gobierno.

## 1. Autorización y alcance

Según el encargo recibido el 28/10/2026, Luis Vila Meza autorizó expresamente:

- crear una rama local de integración desde `develop`, contrastando antes su estado;
- integrar los dos candidatos auditados con merges que conserven su historia;
- resolver el conflicto previsto en `docs/defects.md`;
- ejecutar la validación conjunta;
- preparar el candidato resultante para revisión.

La autorización **no incluye** push, merge hacia `develop` o `main`, tag ni release. Este documento registra la autorización recibida; no la amplía ni añade otras aprobaciones.

## 2. Base y candidatos

| Objeto | Commit | Árbol | Estado recibido |
|---|---|---|---|
| Base: `develop` = `origin/develop` | `55456943059efaa7b34fd7550de97986f0d13061` | `01dc59a80eed0e9f7c26143f6787010fcefb406c` | Sin cambios respecto de la base conocida |
| SEG-01, `fix/seg-01-internal-application-authorization` | `9d1095c092ccec3a88099a53e4f2ee7f8665ab24` | `fa8f17afed772495bf1d4487636560bb75ec79ce` | APROBADO CON OBSERVACIONES NO BLOQUEANTES; pendiente SEG01-AUD-L01 (LOW) |
| SEG-02, `fix/seg-02-decision-stage-concurrency` | `50feb745de621821c4b0805f0fde20d64701807c` | `ba784583b14aa003efee19a82f56e39415915889` | APROBADO TÉCNICAMENTE; pendiente SEG02-AUD-I01 (INFO) |

Relaciones comprobadas antes de integrar:

- las puntas de ambas ramas son exactamente los commits auditados, con los árboles indicados;
- la base común de cada candidato con `develop`, y la de ambos entre sí, es `5545694`;
- SEG-01 va 3 commits por delante de `develop` y SEG-02, 5; ninguno está por detrás;
- los candidatos solo coinciden en `docs/defects.md`. SEG-01 cambia `ApplicationController`, `ApplicationPolicy`, su documento y su prueba; SEG-02 cambia `ApplicationStageService`, su documento y sus tres fuentes de concurrencia;
- ninguno toca superficies congeladas de F35-SBX o F36-SBX, gates, ML, frontend, skills, permisos ni configuración.

## 3. Rama y merges

La rama `fix/seg-01-02-integration` se creó desde `5545694` en un worktree aislado; no existía ni local ni remotamente. Ambos merges usaron `--no-ff --no-commit` para revisar el resultado antes de confirmarlo, sin squash, rebase ni cherry-pick.

| Paso | Orden | Revisión antes del commit | Commit | Árbol | Padres |
|---|---|---|---|---|---|
| 1. SEG-01 | `git merge --no-ff --no-commit 9d1095c092ccec3a88099a53e4f2ee7f8665ab24` | Sin conflictos. Preparados los 5 archivos de SEG-01 (330 inserciones y 1 eliminación); el árbol preparado no difería del de `9d1095c` | `b69c6c38cf2a691de15d09b5b8be7c539a20a2c7` | `fa8f17afed772495bf1d4487636560bb75ec79ce`, el mismo de SEG-01 | `5545694` y `9d1095c` |
| 2. SEG-02 | `git merge --no-ff --no-commit 50feb745de621821c4b0805f0fde20d64701807c` | Conflicto solo en `docs/defects.md` (§4); los otros 5 archivos se combinaron sin conflicto. Tras resolverlo, preparados los 6 archivos de SEG-02 (1408 inserciones y 4 eliminaciones) | `f5b7c591cf7f81c6dbb33142731c786c28cd2e46` | `244b25f4523bdcfc41e97fa86cbdff90127840a2` | `b69c6c3` y `50feb74` |

Cada merge conserva como segundo padre el candidato auditado, y la historia de ambos queda completa en la rama.

## 4. Resolución del conflicto en `docs/defects.md`

**Causa.** Los dos candidatos añaden una fila después de DEF-13: SEG-01 añade DEF-14 y SEG-02, DEF-15.

**Resolución.** Se construyó el archivo a partir de los propios candidatos, sin `ours` ni `theirs`:

1. las filas de la base, hasta DEF-13, sin cambios;
2. la fila DEF-14, byte a byte la de `9d1095c`;
3. la fila DEF-15, byte a byte la de `50feb74`.

**Comprobaciones antes de prepararlo:**

- DEF-01 a DEF-15 en orden, sin duplicados ni renumeración;
- ningún marcador de conflicto;
- quitando DEF-15 queda exactamente el archivo de SEG-01, y quitando DEF-14, exactamente el de SEG-02;
- blob resultante: `1582c0764fbe602bcba5dcc322470349031531dc`.

El texto de estado de DEF-14 y DEF-15 («pendiente de auditoría») se conserva tal como se auditó en cada candidato. Actualizarlo después de las auditorías alteraría el contenido auditado y queda fuera de esta integración, igual que las frases equivalentes de los documentos de SEG-01 y SEG-02.

## 5. Comprobación del contenido combinado

| Comprobación | Resultado |
|---|---|
| `git diff 9d1095c HEAD` sobre `ApplicationController`, `ApplicationPolicy`, el documento de SEG-01 y `ApplicationFileAuthorizationTest` | Vacío: idénticos al candidato |
| `git diff 50feb74 HEAD` sobre `ApplicationStageService`, el documento de SEG-02 y `tests/Feature/Concurrency` | Vacío: idénticos al candidato |
| `git diff 9d1095c HEAD -- docs/defects.md` | Solo añade la fila DEF-15 |
| `git diff 50feb74 HEAD -- docs/defects.md` | Solo añade la fila DEF-14, antes de DEF-15 |
| `git diff --name-status 5545694 HEAD` | Exactamente los 10 archivos de la unión; ningún otro cambio |
| `phpunit.xml`, `docker-compose.yml`, `config/database.php`, `.env.example` y `.env.e2e.example` | Sin cambios respecto de la base |

Blobs del candidato combinado:

| Archivo | Blob | Origen |
|---|---|---|
| `app/Http/Controllers/Applications/ApplicationController.php` | `7a3823c1a6bbf74828058d40c1f46d516ae2d720` | SEG-01 |
| `app/Policies/ApplicationPolicy.php` | `8b710cd8f2d371e5b070f66f89451b474289c31e` | SEG-01 |
| `tests/Feature/Applications/ApplicationFileAuthorizationTest.php` | `c6297c1397813666d18d0fd96fbb4107d32fa61c` | SEG-01 |
| `docs/v1.1/security/SEG-01-expediente-interno-postulante.md` | `63150cc0c08b5b6f8354f517e7a630b0505be8ac` | SEG-01 |
| `app/Services/Applications/ApplicationStageService.php` | `bcf07371047c56cefed898e134e1b4a21b8faae9` | SEG-02 |
| `tests/Feature/Concurrency/DecisionStageConcurrencyTest.php` | `7f1d81b1a0f82ddc4d58a4deccf132119d794113` | SEG-02 |
| `tests/Feature/Concurrency/DecisionStageSequentialTest.php` | `3206f533306f6d29983943e0b89b79bdfdc793ca` | SEG-02 |
| `tests/Feature/Concurrency/Support/seg02-worker.php` | `9f4661427c99e0e4fbc70986d529f84ddd08783e` | SEG-02 |
| `docs/v1.1/security/SEG-02-concurrencia-decision-cambio-etapa.md` | `c2b7fbb04ece532d8f592cc3f422cd53d96a2624` | SEG-02 |
| `docs/defects.md` | `1582c0764fbe602bcba5dcc322470349031531dc` | Resolución de §4 |

El resultado es la unión de los cambios aprobados, con la única resolución documental de §4. No se refactorizó nada ni se corrigió ningún pendiente.

## 6. Validación conjunta

**Entorno.** Docker Compose del proyecto, montando el worktree de integración, con PostgreSQL 17.11. Las bases `reclutamiento`, `reclutamiento_testing` y `reclutamiento_e2e` están separadas. `phpunit.xml` fuerza `reclutamiento_testing`, con `DB_URL` vacío y cola `sync`. Además, la prueba de concurrencia exige que la base, el servidor, el aislamiento y la cola de cada proceso coincidan con los del orquestador.

| Orden | Resultado real |
|---|---|
| `php artisan test tests/Feature/Applications/ApplicationFileAuthorizationTest.php` (focal de SEG-01) | **8 aprobadas** (153 aserciones) |
| `php artisan test --group seg02`, 3 ejecuciones | **13 aprobadas (149 aserciones) en cada una**, sin fallos de orquestación, entorno, recursos ni invariante. Cada escenario repitió el comportamiento validado en SEG-02: S3, S3b, S4, S4b, S4c, S6, S7 y S7b serializados; S5 y S8 sin espera |
| `php artisan test` de `Applications`, `Assessments` (evaluaciones y entrevistas), `Tenancy`, `Selection` (decisión, selección y cierre), `Notifications`, `Audit`, `Candidates` y `Routing` | 24, 19, 11, 30, 8, 16, 6 y 2 aprobadas (237, 97, 32, 206, 64, 208, 27 y 14 aserciones), 0 fallos |
| `docker compose exec app php artisan test` | **432 aprobadas y 8 omitidas** (1800 aserciones), 0 fallos, en 91,84 s. Las 8 omitidas son las preexistentes de verificación de correo de Fortify, una función desactivada |
| `docker compose exec app npm run build` | Correcto: 2375 módulos, salida 0 |
| `docker compose exec app npx tsc --noEmit` | 0 errores, salida 0 |
| Cypress, entorno E2E aislado (`init-e2e-env.sh` y `docker compose --profile e2e run --rm cypress`, el equivalente sin npm en el host de `npm run cy:run`) | **«All specs passed!»: 20 specs y 85 de 85 pruebas**, 0 fallidas, en 06:19 (Cypress 15.3.0, Electron 136 headless). Incluye los flujos de ambas correcciones: postulación (e2e-05), preselección (e2e-06), decisión final humana (e2e-09), selección y cierre (e2e-10), multiempresa (e2e-11), reglas negativas (e2e-12) y flujo completo (e2e-13) |

Todas las pruebas de esta tabla se ejecutaron en esta integración. Las ejecuciones de los auditores y las de cada candidato por separado no se cuentan aquí.

## 7. Pendientes conservados

- **SEG01-AUD-L01 (LOW).** Cobertura permanente de las claves públicas en ambas convocatorias. Sin cambios.
- **SEG02-AUD-I01 (INFO).** Esperas sin cota configurada (sin `lock_timeout`). Sin cambios.
- Siguen fuera de alcance: la programación sin comprobación de A-28 (observación de SEG-02, sin verificar), SEG-03 y SEG-04.

## 8. Limitaciones y siguiente revisión

- **Validación local.** Se hizo en Docker Desktop; la CI no se ejecutó porque no hubo push.
- **Gates de F35-SBX y F36-SBX.** Sus validadores no se ejecutaron. Un rechazo FRZ de un gate histórico sobre este incremento posterior es esperable por diseño, porque se validan anclados en su rama. No autoriza a modificar el gate ni demuestra por sí solo una regresión funcional.
- **Estado documental.** DEF-14, DEF-15 y los documentos de cada candidato siguen diciendo «pendiente de auditoría», como se auditaron (§4).
- **Concurrencia.** Las pruebas de concurrencia usan barreras deterministas; no miden la probabilidad natural de cada carrera.
- **Siguiente paso.** Revisión de Codex del candidato combinado. Integrarlo en `develop` o `main` exige otra autorización explícita.

## 9. Recursos aislados y estado final

- **Worktree** temporal en `.claude/worktrees/seg0102`, sobre la rama de integración, con el checkout principal intacto. Contenía archivos ignorados por Git: un `.env` generado por el entrypoint desde `.env.example`, con clave propia (el `.env` real no se copió), un `.env.e2e` generado por `init-e2e-env.sh`, `public/build` y cachés. Se elimina al terminar, ya registrado todo en commits; la rama se conserva.
- **Contenedores.** `app` y `queue` se recrearon montando el worktree, y el perfil E2E levantó `app-e2e` y `queue-e2e`. Al terminar se ejecutó `docker compose --profile e2e down`, sin `-v`, y se recrearon los contenedores desde el checkout principal. Estado final verificado, igual al encontrado: los cuatro contenedores (`app`, `queue`, `postgres` y `redis`) creados y detenidos; `app`, `queue` y los scripts de inicio de `postgres` montan el checkout principal; una sola red `reclutamiento_default`; sin contenedores E2E.
- **Volúmenes** `reclutamiento_pgdata`, `reclutamiento_redisdata`, `reclutamiento_vendor` y `reclutamiento_node_modules`: conservados; ninguno se borró ni recreó.
- **Bases de datos.** `reclutamiento_testing` queda migrada y vacía tras la suite; `reclutamiento_e2e` la reinició Cypress, como está previsto. La base de desarrollo `reclutamiento` solo recibió el `php artisan migrate --force` del entrypoint, sin migraciones pendientes porque ninguno de los candidatos añade migraciones; no se ejecutó ninguna migración destructiva sobre ella.

## 10. Commits de esta rama

Además de los dos merges de §3, la rama tiene un commit documental limitado a este documento. Ese commit se consulta en Git: este documento no puede citarlo.
