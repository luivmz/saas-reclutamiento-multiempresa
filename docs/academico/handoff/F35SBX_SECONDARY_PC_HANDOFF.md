# Continuidad en una PC secundaria después de F35-SBX

> **Estado: receta de traslado posterior al cierre de F35-SBX.** Preparada el 25/10/2026 sobre `develop` = `e366cbf81f7c6e158ddd848268cf66f1247b4ed8`, en la rama `chore/handoff-secondary-pc-post-f35sbx`.
>
> - No inicia F36-SBX ni cambia ningún estado de gobierno: ninguna F36-SBX empieza sin una autorización sucesora nueva, con su propia gobernanza.
> - Todo lo que hace falta está en el repositorio. Ninguna ruta, carpeta temporal ni memoria de sesión de la PC principal forma parte de esta receta.

## 1. Checkpoint de transferencia

| Referencia | Valor |
|---|---|
| Rama estable | `main` |
| `HANDOFF_ANCHOR` | `2876d48e4e3aa17aef46f2e73fcd8f85cc16d449`, un commit conocido de este incremento: contiene el registro de GC-AF-L01, esta guía y la continuidad de gobierno. Todo `main` que incluya el handoff lo contiene, también con sus correcciones posteriores; el `main` anterior, `06b789f`, no |
| `MAIN_HEAD` | Se obtiene después de clonar y actualizar, con `git rev-parse HEAD`. Cambia con el merge administrativo de este incremento, así que aquí no se anota ningún hash futuro |
| Cierre de F35-SBX en `main` (antecedente) | `06b789f9e9e99268eccfb72a15df2dd30fe47360`, con el CI `tests` en verde: run 40221523362 (#70), job 121253935073 |
| Cierre de F35-SBX en `develop` | `e366cbf81f7c6e158ddd848268cf66f1247b4ed8`, con el CI `tests` en verde: run 40221309615 (#69), job 121253273972 |
| Candidato auditado del cierre | `858b5fa71c01bf794715f78068ea0557fd56a16b`, árbol `eb56582de34d57be8a6be2a7b4b33dfecea83970`, conservado en `origin/chore/f35-sbx-global-closure` |
| Etiquetas | Solo `v1.0.0-academic` y `v1.1.0-academic`. No hay etiquetas ni releases nuevas |
| F35-SBX | CERRADA, CONGELADA E INTEGRADA, solo en su alcance académico y sintético |
| F36-SBX | NO iniciada; F36–F40 siguen BLOQUEADAS |

**Cómo se prueba el checkpoint.** `MAIN_HEAD` cambia cuando este incremento se integra en `main`, y la guía no puede citar el hash de ese merge sin citarse a sí misma. Por eso el checkpoint se demuestra con `HANDOFF_ANCHOR`, que ya existe. Si es ancestro de `MAIN_HEAD`, el clon incluye el handoff. Si no lo es, o si Git no conoce ese commit, la PC secundaria no está en el checkpoint posterior al handoff y la receta se detiene (§2). Las comprobaciones del cierre de F35-SBX son necesarias pero no bastan: el `main` anterior, `06b789f`, también las supera.

El estado de gobierno completo está en el bloque «Estado vigente» de [`CLAUDE.md`](../../../CLAUDE.md), igual en [`docs/PROGRESS.md`](../../PROGRESS.md), [`ACADEMIC_BASELINE.md`](../ACADEMIC_BASELINE.md) y [`README.md`](../../../README.md). El cierre está registrado en [`F35SBX_Cierre_Global.md`](../evidencia-sbx-cierre-global/F35SBX_Cierre_Global.md).

## 2. Clonar desde GitHub

GitHub es la única fuente de sincronización: el repositorio no se copia a mano desde la PC principal. Comandos de clonación y verificación:

```sh
git clone https://github.com/luivmz/saas-reclutamiento-multiempresa.git
cd saas-reclutamiento-multiempresa
git fetch --all --prune
git checkout main
git pull --ff-only
git rev-parse HEAD
git status --short --branch
```

Comprobaciones del checkpoint. La primera es la del handoff y, si falla, la receta se detiene:

```sh
MAIN_HEAD=$(git rev-parse HEAD); echo "MAIN_HEAD = $MAIN_HEAD"
if git merge-base --is-ancestor 2876d48e4e3aa17aef46f2e73fcd8f85cc16d449 HEAD; then
  echo "OK: este main contiene el handoff posterior a F35-SBX (HANDOFF_ANCHOR)"
else
  echo "DETENERSE: este main no contiene el HANDOFF_ANCHOR; no es el checkpoint posterior al handoff"
fi
git merge-base --is-ancestor 06b789f9e9e99268eccfb72a15df2dd30fe47360 HEAD && echo "contiene el cierre de F35-SBX"
git merge-base --is-ancestor 858b5fa71c01bf794715f78068ea0557fd56a16b HEAD && echo "contiene el candidato auditado"
git ls-remote --tags origin
```

Si aparece «DETENERSE», no se sigue con la receta. El `main` clonado es anterior al handoff, por ejemplo `06b789f`, o el handoff aún no está integrado. En ese caso se comprueba con el equipo qué `main` está publicado.

- **Identidad Git.** Se configura la propia de la PC secundaria y se comprueba con `git config user.name` y `git config user.email`. La autenticación con GitHub usa el mecanismo seguro habitual del equipo, sin tokens en comandos ni en documentos.
- **Finales de línea.** [`.gitattributes`](../../../.gitattributes) fuerza `eol=lf`, así que el clon tiene los mismos bytes en Windows, macOS y Linux.

## 3. Entorno y dependencias

No hay dependencias nuevas. Todo se restaura desde los archivos versionados, sin `composer update` ni `npm install` que cambien los locks. El detalle sigue vigente en la [receta F34E](F34E_MACOS_HANDOFF.md#restauración-y-arranque-soportados) y en [`docs/docker.md`](../../docker.md).

| Componente | Cómo se restaura | Fuente |
|---|---|---|
| Docker y Compose | Docker Desktop o Docker Engine con Compose 2.24 o superior. Laravel, Node, PostgreSQL y Redis corren en contenedores | [`docs/docker.md`](../../docker.md), [`docker-compose.yml`](../../../docker-compose.yml) |
| PHP 8.4 y Composer | `docker compose exec -T app composer install --no-interaction --prefer-dist`, desde `composer.lock`. El entrypoint lo hace solo si falta `vendor/` | [`composer.json`](../../../composer.json), [entrypoint](../../../docker/php/entrypoint.sh) |
| Node 22 y npm | `docker compose exec -T app npm ci` y `docker compose exec -T app npm run build`, desde `package-lock.json` | [`package.json`](../../../package.json) |
| PostgreSQL 17.11 y Redis 7.4.11 | Imágenes de Compose (`postgres:17.11-alpine` y `redis:7.4.11-alpine`); la base de PHPUnit la crea el script de inicio | [`docker-compose.yml`](../../../docker-compose.yml) |
| Python 3.12 o superior | Para los validadores académicos, que usan la biblioteca estándar. `test_f32_safety.py` necesita además Pillow | [receta F34E](F34E_MACOS_HANDOFF.md#checklist-ejecutable-después-del-traslado) |
| Servicio ML experimental (opcional) | En `ml-service/`: `python -m venv .venv`, `pip install -e ".[dev]"` con el Python del entorno virtual y `python -m pytest -q`. No hace falta para continuar | [`ml-service/README.md`](../../../ml-service/README.md) |

Arranque:

```sh
test -e .env || cp .env.example .env
docker compose up -d --build --wait
curl --fail http://localhost:8000/health
```

Antes del primer arranque hay que revisar `.env`, como indica la [receta F34E](F34E_MACOS_HANDOFF.md#configuración-privada-antes-del-primer-arranque): una base local nueva y descartable, `SEED_ON_BOOT=false` y `ML_SERVICE_ENABLED=false`.

## 4. Archivos locales que no viajan con el clon

Se recrean en la PC secundaria y nunca se copian ni se versionan. La lista sale de [`.gitignore`](../../../.gitignore):

| Qué | Cómo |
|---|---|
| `.env` y `.env.e2e` | Desde [`.env.example`](../../../.env.example) y [`.env.e2e.example`](../../../.env.e2e.example). El de E2E lo crea `npm run e2e:setup`. Sin secretos reales |
| `vendor/`, `node_modules/`, `public/build/` y `public/hot` | Los genera el contenedor (`composer install`, `npm ci`, `npm run build`) |
| `bootstrap/cache/*.php` y el contenido de `storage/` | Los genera Laravel al arrancar |
| Volúmenes de PostgreSQL y Redis | Los crea Compose. Solo datos ficticios |
| `ml-service/.venv/`, `ml-service/artifacts/`, `__pycache__/` y `.pytest_cache/` | Se regeneran con [`ml-service/README.md`](../../../ml-service/README.md), si se usa el servicio |
| `cypress/results/`, `cypress/videos/`, `cypress/screenshots/` y `cypress/downloads/` | Los genera la suite E2E |
| `.claude/settings.local.json` | Configuración local de cada equipo |

No se copian credenciales, tokens, configuración global, bases de datos ni archivos de la PC principal.

## 5. Validación mínima del clon

Los validadores se ejecutan desde la raíz del clon, con Python 3.12 o superior: `python3` en macOS y Linux, `python` en Windows. Conviene hacerlo con el clon tal como llega de GitHub, antes del primer arranque de Docker, que genera dependencias, compilados y cachés en el árbol de trabajo.

**Identidad del clon.**

```sh
git status --short --branch     # sin cambios
git rev-parse HEAD origin/main  # iguales
```

**Gate del cierre de F35-SBX, sobre su ancla.** Se ejecuta en un worktree aparte, sin dependencias instaladas. FSY exige que las superficies materiales no tengan artefactos generados.

```sh
git worktree add -b chore/f35-sbx-global-closure ../f35sbx-cierre-global origin/chore/f35-sbx-global-closure
python3 -I -B ../f35sbx-cierre-global/docs/academico/tools/f35sbx_cierre_global/validate_f35sbx_cierre_global.py
```

Resultado esperado: `13 comprobaciones correctas, 0 fallas`, y la línea INFO de FRZ con el commit `858b5fa71c01bf794715f78068ea0557fd56a16b`. El gate solo admite las ramas `chore/f35-sbx-global-closure`, `develop` y `main`, por eso el worktree crea esa rama local. Puede conservarse para repetir la verificación; si se quita, se hace con `git worktree remove ../f35sbx-cierre-global`. Sobre un HEAD posterior, este gate y los congelados de A y B fallan por diseño en las reglas de contexto, gobierno y alcance, porque el gobierno y el alcance cambiaron después de su ancla (DG-02). No es una regresión.

**Validadores académicos, sobre `main`.**

```sh
git branch --track develop origin/develop      # validate_f34a.py necesita una rama local develop
python3 -B docs/academico/tools/f35sbxb3/test_sbxb_pipeline.py
python3 -B docs/academico/tools/f27b/validate.py
python3 -B docs/academico/tools/f27b/validate.py --cierre-f29
python3 -B docs/academico/powerdesigner/scripts/validate_f29.py
python3 -B docs/academico/tools/f30/validate_f30.py
python3 -B docs/academico/tools/f27b/test_f32_safety.py
python3 -B docs/academico/tools/f33/validate_f33.py
python3 -B docs/academico/tools/f34/validate_f34.py
python3 -B docs/academico/tools/f34a/validate_f34a.py
python3 -B docs/academico/tools/f34b/validate_f34b.py
python3 -B docs/academico/tools/f34e/validate_f34e.py
git status --short --branch
```

| Validador | Resultado esperado |
|---|---|
| `test_sbxb_pipeline.py` | 30/30 |
| `validate.py` y `validate.py --cierre-f29` | 0 fallas |
| `validate_f29.py` | 225/0 |
| `validate_f30.py` | OK |
| `test_f32_safety.py` | OK |
| `validate_f33.py`, `validate_f34.py` y `validate_f34a.py` | 451/0, 403/0 y 108/0 |
| `validate_f34b.py` | 340/1. La falla está en su regla GIT y es histórica de ciclo de vida (clase A): su vocabulario congelado solo admite F35-SBX HABILITADA y no conoce las capas posteriores |
| `validate_f34e.py` | 247/1. La falla está en su regla GIT y es histórica (DH-B13, clase A), con «criterios SBX: 18/18 cumplen». Su línea INFO conserva la derivación congelada «F35-SBX = HABILITADA»; el estado vigente lo fija el gobierno |

**Aplicación, dentro de Docker.** Es la misma secuencia que el CI ([`tests.yml`](../../../.github/workflows/tests.yml)) y no hace falta repetir baterías históricas:

```sh
docker compose exec -T app npx tsc --noEmit
docker compose exec -T app npm run build
docker compose exec -T app php artisan test
```

PHPUnit usa su propia base, `reclutamiento_testing`. Cypress y el servicio ML son opcionales para continuar.

## 6. Qué está permitido y qué sigue bloqueado

- **F35-SBX está cerrada.** Terminó como sandbox académico y sintético: el contrato y los fixtures de F35-SBX-A, el almacén efímero y el pipeline determinista de F35-SBX-B, y los gates sucesores. Todo está congelado: no se modifica.
- **F36–F40 siguen BLOQUEADAS.** Ninguna F36-SBX empieza sin una autorización sucesora nueva, con su propia gobernanza. Esa decisión es un incremento separado de este handoff.
- **G0.** G0 real = NO APROBADA. G0-02, G0-03 y G0-12 = PENDIENTE EXTERNO. G0-09 y G0-14 = CUMPLIDO. G0-SBX = APROBADA CON RESTRICCIONES. ADR-005 = PROPUESTA.
- **Datos y alcance.** Datos reales PROHIBIDOS; solo datos ficticios o sintéticos. F35 productiva y alcance C BLOQUEADOS.
- **Requisitos.** RF-23 sigue siendo la decisión final humana del Aprobador o Dirección. RF-29 sigue experimental. RF-01 a RF-27 no cambian.
- **Deuda pendiente.** GC-AF-L01 (LOW), abierta y diferida, en el [registro de deuda técnica](../TECHNICAL_DEBT.md). No bloquea el cierre y se trata en un incremento propio.
- **Git.** Ramas nuevas desde `develop`, merges `--no-ff`, y nada de push, merge, etiqueta ni release sin autorización explícita del equipo ([`CLAUDE.md`](../../../CLAUDE.md), contratos 9 y 10).

## 7. Relación con los handoffs anteriores

La [receta F34E para macOS](F34E_MACOS_HANDOFF.md) y [`MAC_HANDOFF.md`](../MAC_HANDOFF.md) conservan su valor como fotografías de su momento. Sus estados vigentes, con F35-SBX HABILITADA o sin iniciar, son anteriores a este cierre. Para continuar después de F35-SBX valen esta guía y el gobierno vigente.
