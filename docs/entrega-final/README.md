# Entrega académica — arranque, datos y materiales

> Rama local `feature/entrega-academica-demo`, del 07/11/2026, creada desde `2f6d0e0`. Contiene `develop` `9dd76c4` con SEG-01 a SEG-04, el RR-001 y los borradores de D-10 y D-11. **Entrega local:** sin push, merge, tag ni release.

| Material | Archivo |
|---|---|
| Informe final: estado real, pruebas y clasificación de cada parte | [`informe-final.md`](informe-final.md) |
| Guion de exposición, paso a paso | [`guion-demo.md`](guion-demo.md) |
| Usuarios y escenarios ficticios | [`../demo-users.md`](../demo-users.md) |
| Expediente técnico de F36-SBX | [`../academico/f36-sbx/expediente-final/README.md`](../academico/f36-sbx/expediente-final/README.md) |
| Prototipo de ML-02, estático | [`../academico/f36-sbx/prototipo-ml02/index.html`](../academico/f36-sbx/prototipo-ml02/index.html) |

## 1. Requisitos

- Docker Desktop en marcha. Laravel, PostgreSQL y Redis corren en contenedores.
- Python 3.12 en el equipo, solo para ML-01, que se ejecuta fuera de Docker.
- Puertos libres: 8000 para la app, 8001 para el entorno E2E y 8008 para ML-01. Con un proyecto aislado se pueden cambiar en `.env`; ver 2.B.

## 2. Arrancar el SaaS

### A. Desde el checkout de la rama

```powershell
docker compose up -d --wait
docker compose exec app php artisan migrate:fresh --seed --force   # BORRA la base de desarrollo y carga DemoSeeder
```

La app queda en `http://localhost:8000`. Todas las cuentas demo usan la contraseña `password` (solo demostración); los correos están en [`demo-users.md`](../demo-users.md).

### B. En un proyecto Docker aislado, sin tocar los contenedores ni los datos habituales

Así se verificó esta entrega, desde un worktree propio:

```powershell
# En el .env del worktree: APP_PORT=8010, APP_URL=http://localhost:8010, FORWARD_DB_PORT=5442,
# FORWARD_REDIS_PORT=6389 y E2E_APP_PORT=8011
docker compose -p entregaacad up -d --wait --no-build app
docker compose -p entregaacad exec app php artisan migrate:fresh --seed --force   # base propia del proyecto aislado
```

La app queda en `http://localhost:8010`. Para detener el proyecto aislado: `docker compose -p entregaacad down`. Para borrar también sus volúmenes, `-v`; solo afecta a `entregaacad_*`.

## 3. Arrancar ML-01 (RF-29, experimental y opcional)

```powershell
cd ml-service
python -m venv .venv
.venv\Scripts\python.exe -m pip install -e ".[dev]"                 # dependencias fijadas en pyproject.toml
.venv\Scripts\python.exe -m recruitment_ml.serving.build_artifact   # reconstruye el modelo desde el freeze aprobado
$env:RECRUITMENT_ML_INTERNAL_TOKEN = "<secreto local, el mismo que ML_SERVICE_TOKEN>"
.venv\Scripts\python.exe -m uvicorn recruitment_ml.api.app:app --host 0.0.0.0 --port 8008
```

En el `.env` de Laravel, que no se versiona: `ML_SERVICE_ENABLED=true`, `ML_SERVICE_URL=http://host.docker.internal:8008` y `ML_SERVICE_TOKEN=<el mismo secreto>`. Después, `docker compose exec app php artisan config:clear`.

Comprobación: `curl http://127.0.0.1:8008/health` debe devolver `{"status":"ok","model_ready":true,…}`. Sin el servicio, la plataforma funciona igual y el panel muestra su modo descriptivo.

## 4. Pruebas

```powershell
docker compose exec app php artisan test          # PHPUnit
docker compose exec app npx tsc --noEmit          # tipos
docker compose exec app npm run build             # frontend
docker compose exec app npx vp test --run         # componentes
npm run cy:run                                    # Cypress, en el entorno E2E aislado
cd ml-service; .venv\Scripts\python.exe -m pytest # ML-01
```

En un proyecto aislado, se añade `-p entregaacad` a cada `docker compose`. En lugar de `npm run cy:run`:

```powershell
docker compose -p entregaacad run --rm --no-deps --entrypoint sh app docker/php/init-e2e-env.sh
docker compose -p entregaacad --profile e2e run --rm cypress
```

## 5. Datos de prueba

Todo es ficticio: nombres con «(demo)» o «(ficticio/a)», correos `.test` y CV de ejemplo. `DemoSeeder` carga dos organizaciones y requerimientos en cada estado. Las vacantes cubren los estados de borrador, publicada con postulaciones, ranking pendiente de decisión y proceso concluido. Además, desde esta entrega, el escenario de riesgo operacional para ML-01 (DEF-18). El detalle está en [`demo-users.md`](../demo-users.md).
