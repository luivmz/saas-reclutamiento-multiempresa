# Continuar el proyecto desde macOS

Guía práctica para retomar el proyecto en una Mac tras el cierre académico de las fases F27 a F29 (28/09/2026). No sustituye a la documentación de origen; enlaza a ella.

## Estado del proyecto

| Elemento | Valor |
|---|---|
| Repositorio | https://github.com/luivmz/saas-reclutamiento-multiempresa |
| `main` | Rama publicada. Contiene la v1.1 académica (etiqueta `v1.1.0-academic`) y el cierre académico F2–F11 |
| `develop` | Rama de integración. **Aquí se continúa el trabajo** |
| `feature/phase-27-academic-f2-f11` | Rama de las fases F27–F29, integrada en `develop` y `main` y **conservada** para trazabilidad y auditoría. Se limpiará en la F31 o la F32 |
| Etiquetas | `v1.0.0-academic` → `9a946c2` y `v1.1.0-academic` → `634f354`. No se mueven ni se reutilizan |

**Commits antes de integrar (28/09/2026):**

- `feature/phase-27-academic-f2-f11`: `194105a` «docs(academic): integrate audited PowerDesigner evidence into deliverables»;
- `develop`: `c712539`;
- `main`: `634f354`.

La integración añade encima un commit con esta guía y los *merges* explícitos a `develop` y a `main`. Para ver los commits actuales:

```bash
git fetch --all --prune
git log --oneline -1 origin/main origin/develop origin/feature/phase-27-academic-f2-f11
```

## Clonar en la Mac

```bash
git clone https://github.com/luivmz/saas-reclutamiento-multiempresa.git
cd saas-reclutamiento-multiempresa
git fetch --all --prune
git switch main && git pull --ff-only
git switch develop && git pull --ff-only        # rama de trabajo
```

Los binarios académicos (DOCX, PDF, PNG, SVG, `.bpm` y `.oom`) están versionados: llegan con el clon.

## Lo que no viene en el clon

Estos archivos no están versionados y hay que crearlos o regenerarlos en la Mac:

| Qué | Cómo |
|---|---|
| `.env` y `.env.e2e` | Se crean desde las plantillas (ver «Variables de entorno»). Nunca se versionan |
| `vendor/`, `node_modules/`, `public/build/` | Los genera el contenedor de Docker al arrancar |
| `ml-service/.venv/` y `ml-service/artifacts/` (dataset y modelo) | Se regeneran con [`ml-service/README.md`](../../ml-service/README.md) |
| `.claude/settings.local.json` | Configuración local de cada equipo; no se copia |

## Variables de entorno

```bash
cp .env.example .env
```

- `.env.example` trae valores de desarrollo para Docker: PostgreSQL en el servicio `postgres`, Redis en `redis` y la aplicación en el puerto 8000.
- Si un puerto está ocupado en la Mac, se cambia en `.env`: `APP_PORT`, `FORWARD_DB_PORT` y `FORWARD_REDIS_PORT`.
- **No se versionan secretos**: ni `.env`, ni `.env.e2e`, ni tokens ni claves.
- Esta guía no incluye contraseñas reales. Los usuarios de demostración son ficticios ([`docs/demo-users.md`](../demo-users.md)).
- El entorno E2E crea su propio `.env.e2e` con `npm run e2e:setup`, a partir de `.env.e2e.example`.

## Puesta en marcha (Docker, flujo oficial)

Laravel y el frontend corren en Docker: el proyecto no usa PHP ni Node instalados en el equipo. Hace falta **Docker Desktop para Mac** con Compose 2.24 o superior, y Git. Detalle en [`docs/docker.md`](../docker.md).

```bash
cp .env.example .env
docker compose up -d --build --wait                                 # primera vez: dependencias, compilación y migraciones
docker compose exec app php artisan migrate:fresh --seed --force    # datos de demostración ficticios
```

Abrir http://localhost:8000.

**Frontend**, dentro del contenedor (scripts reales de `package.json`):

```bash
docker compose exec app npm run build        # vp build
docker compose exec app npx tsc --noEmit     # tipos
docker compose exec app npm run dev          # servidor de desarrollo (vp dev)
```

**Laravel:** `composer.json` define `composer setup`, `composer dev` y `composer test`. En el flujo oficial se ejecutan dentro del contenedor, por ejemplo `docker compose exec app php artisan test`.

**Apple Silicon.** Las imágenes base son oficiales:

- `php:*-cli-bookworm`, `node:*-bookworm-slim` y `composer`;
- `postgres:17.11-alpine` y `redis:7.4.11-alpine`;
- `cypress/included:15.3.0`.

**Este flujo no se ha probado en macOS.** Si una imagen fallara en `arm64`, se documenta como observación antes de cambiar el `docker-compose.yml`.

## Servicio ML experimental (opcional)

No corre en Docker. En la Mac, dentro de `ml-service/`:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
.venv/bin/python -m pytest -q
```

Requiere Python 3.12 o superior. El dataset sintético y el modelo se regeneran con los comandos de [`ml-service/README.md`](../../ml-service/README.md), cambiando `.venv/Scripts/python.exe` por `.venv/bin/python`.

Laravel solo llama al servicio si `ML_SERVICE_ENABLED=true`. Sin él, la aplicación funciona igual.

## Documentación académica

`docs/academico/` ([línea base y estado](ACADEMIC_BASELINE.md)) contiene los Formatos F2 a F11, la formalización de PowerDesigner (F29) y la trazabilidad. El F9 publicado está en [`phase-24/output/`](phase-24/README.md) y **no se modifica**.

| Formato | Carpeta | Entregable |
|---|---|---|
| F2 Análisis del proceso | [`practica-02/`](practica-02/README.md) | DOCX, PDF y espejo `.md` |
| F3 BPMN AS-IS | [`practica-03/`](practica-03/README.md) | DOCX y PDF con la exportación formal de PowerDesigner |
| F4 Problemas del proceso | [`practica-04/`](practica-04/README.md) | DOCX, PDF y espejo `.md` |
| F5 BPMN TO-BE | [`practica-05/`](practica-05/README.md) | DOCX y PDF con la exportación formal (y cuatro ampliaciones) |
| F6 RF y F7 RNF | [`practica-06/`](practica-06/README.md) · [`practica-07/`](practica-07/README.md) | DOCX, PDF y espejo `.md` |
| F8 Casos de uso | [`practica-08/`](practica-08/README.md) | DOCX y PDF con la exportación formal |
| F9 Alcance (publicado) | [`phase-24/output/`](phase-24/README.md) · adenda en [`practica-09/`](practica-09/F9_POST_RELEASE_ADDENDUM.md) | Solo lectura |
| F11 Arquitectura | [`practica-11/`](practica-11/README.md) | Definitivo: DOCX y PDF sobre la plantilla oficial (F11-R), con la vista ARQ-01. Se conserva además la adaptación histórica de la F28 |
| F29C Variables y operacionalización | [`operacionalizacion/`](operacionalizacion/README.md) | DOCX y PDF con el Anexo 1 (matriz) y el Anexo 2 (diagrama conceptual), espejo `.md` y paquete de ejecución de la actividad E1 y registro de la evidencia de ChatGPT (P-01 a P-06; el resto es NO REQUERIDO). `validate.py --cierre-f29c` pasa. **Lista para auditoría** |

**PowerDesigner (F29):**

| Qué | Ruta |
|---|---|
| Modelos | [`powerdesigner/models/F29_BPM_Academico.bpm`](powerdesigner/models/F29_BPM_Academico.bpm) · [`powerdesigner/models/F29_UML_Academico.oom`](powerdesigner/models/F29_UML_Academico.oom) |
| Exportaciones (PNG y SVG) | [`powerdesigner/exports/`](powerdesigner/exports/) |
| Capturas de PowerDesigner | [`powerdesigner/evidencias/capturas/`](powerdesigner/evidencias/capturas/CAPTURAS_PENDIENTES.md) |
| Manifiesto (SHA-256) | [`powerdesigner/MANIFEST.md`](powerdesigner/MANIFEST.md) |
| Estado, validación y hotfix | [`powerdesigner/README.md`](powerdesigner/README.md) · [`F29_VALIDATION.md`](powerdesigner/F29_VALIDATION.md) · [`F29B_HOTFIX.md`](powerdesigner/F29B_HOTFIX.md) |

## PowerDesigner y macOS

**PowerDesigner 16.6 es una aplicación de Windows y no tiene versión nativa para macOS.**

- En la Mac, los modelos `.bpm` y `.oom` se **conservan y se versionan** como cualquier archivo, pero **no se pueden abrir ni editar**. No hay que modificarlos a mano: son XML de PowerDesigner y los regeneran los scripts.
- Para editarlos o volver a exportarlos hace falta Windows: un equipo Windows, una máquina virtual con Windows o una solución que el equipo apruebe más adelante.
- Los scripts de `powerdesigner/scripts/*.ps1` usan la automatización COM de PowerDesigner y la API de ventanas de Windows, así que **solo funcionan en Windows**. Esto incluye las capturas (`capture_f29_views.ps1`).
- Los PNG, SVG, DOCX y PDF **sí** se revisan normalmente en la Mac.
- **DOCX y PDF:**
  - `python3 docs/academico/tools/f27b/build.py f3 f5 f8 f11` regenera los DOCX en cualquier sistema (necesita Python 3 y Pillow);
  - el PDF sale de Microsoft Word por COM (`tools/f27b/topdf.ps1`), que solo existe en Windows.

  Si se regenera un DOCX en la Mac, su PDF se vuelve a exportar desde Windows antes del commit. Si no, el DOCX y el PDF quedarían desalineados.

## Validadores

Desde la raíz del repositorio, con Python 3 (en la Mac, `python3`):

```bash
python3 docs/academico/tools/f27b/validate.py                  # coherencia F2 → F11 e integridad de los DOCX
python3 docs/academico/powerdesigner/scripts/validate_f29.py   # modelos, exportaciones, capturas, integración y F23
```

Resultado esperado: `validate.py`, 0 fallas (los requisitos fuera del alcance efectivo de la F29C aparecen como NO REQ; con `--cierre-f29c`, un PENDIENTE contaría como falla); `validate_f29.py`, 225 comprobaciones correctas y 0 fallas. Ninguno de los dos necesita PowerDesigner. `validate_f29.py` usa `git`.

## Forma de trabajar con Git

- Nuevo trabajo: rama `feature/*`, `fix/*` o `docs/*` creada desde `develop`. **No se desarrolla directamente sobre `main`.**
- Integración: *merge* explícito (`--no-ff`) a `develop` y, cuando corresponda, de `develop` a `main`.
- Sin `push --force`, sin rebase de historia publicada y sin mover ni reutilizar etiquetas.
- Sin *push*, *merge*, *release* ni etiqueta sin autorización explícita del equipo. Las reglas completas están en [`CLAUDE.md`](../../CLAUDE.md).
- `feature/phase-27-academic-f2-f11` se conserva hasta la F31 o la F32.

## Pendientes para la F31 (LOW)

| ID | Pendiente |
|---|---|
| H-14 | La cabecera del PDF del F4 no aparece en la capa de texto |
| F28-L01 | Lo mismo en la cabecera del PDF del F11 |
| F29-L01 | `RepositoryFilename` de los modelos de PowerDesigner guarda una ruta local de Windows |
| F29-L02 | Algunos rótulos de ARQ-01 rozan líneas o bordes |
| F29B-OBS-01 | PowerDesigner 16.6 no dibuja el contenido de SP-01 ni de SP-P en la vista principal del editor; se ve en sus diagramas de detalle y en las exportaciones |

## Próximo paso

El proyecto académico queda **en pausa** hasta recibir nuevas guías o formatos. Al retomarlo en la Mac:

1. actualizar `develop`;
2. crear una rama nueva desde `develop`;
3. seguir la skill `project-guardian` antes de editar.
