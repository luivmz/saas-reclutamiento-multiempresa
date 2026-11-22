# Entrega académica — arranque, datos y materiales

> Rama local `feature/entrega-academica-demo`, del 07/11/2026, creada desde `2f6d0e0`. Contiene `develop` `9dd76c4` con SEG-01 a SEG-04, el RR-001 y los borradores de D-10 y D-11. **Entrega local:** sin push, merge, tag ni release.

> **Nota del 22/11/2026.** Esta entrega se integró en `main`, junto con el flujo experimental F37 y el incremento visual, como base de presentación. El arranque vigente está en [`docs/presentacion/README.md`](../presentacion/README.md). La ruta `entregaacad` de este documento sigue siendo válida como proyecto Docker aislado. Ningún estado formal cambia.

| Material | Archivo |
|---|---|
| Informe final: estado real, pruebas y clasificación de cada parte | [`informe-final.md`](informe-final.md) |
| Guion de exposición, paso a paso | [`guion-demo.md`](guion-demo.md) |
| Continuación F36–F40 (rama `feature/continuacion-f36-f40`): estado por fase, pruebas y puntos de auditoría | [`informe-continuacion.md`](informe-continuacion.md) |
| Usuarios y escenarios ficticios | [`../demo-users.md`](../demo-users.md) |
| Expediente técnico de F36-SBX | [`../academico/f36-sbx/expediente-final/README.md`](../academico/f36-sbx/expediente-final/README.md) |
| Prototipo de ML-02, estático | [`../academico/f36-sbx/prototipo-ml02/index.html`](../academico/f36-sbx/prototipo-ml02/index.html) |

**Ruta de arranque: el proyecto Docker aislado `entregaacad`.** Todos los comandos `docker compose` de este documento llevan `-p entregaacad`. Así, la demo tiene sus propios contenedores, red y volúmenes (`entregaacad_*`), con una base exclusivamente ficticia. El proyecto habitual `reclutamiento`, sus contenedores y su base de desarrollo no se usan ni se modifican.

## 1. Requisitos

- **Docker Desktop en marcha.** Laravel, PostgreSQL y Redis corren en contenedores.
- **Python 3.12,** solo para ML-01, que se ejecuta fuera de Docker.
- **Puertos libres:** 8010 (app), 8011 (E2E), 5442 (PostgreSQL, solo loopback), 6389 (Redis, solo loopback) y 8008 (ML-01).
- **Un checkout de la rama.** Se usa el worktree `entrega-academica-20261107/worktree`, o cualquier otro checkout de `feature/entrega-academica-demo`. Los comandos se ejecutan desde su raíz.

## 2. Preparar el proyecto `entregaacad` (solo la primera vez)

### 2.1 `.env` propio, que no se versiona

```powershell
Copy-Item .env.example .env
# Editar .env: APP_PORT=8010, APP_URL=http://localhost:8010, FORWARD_DB_PORT=5442,
#              FORWARD_REDIS_PORT=6389, E2E_APP_PORT=8011
```

El primer arranque genera `APP_KEY` y ejecuta `composer install`, `npm ci` y `npm run build` dentro de los volúmenes `entregaacad_vendor` y `entregaacad_node_modules`. Necesita internet y tarda varios minutos.

### 2.2 Imagen local de PHP

El compose usa la imagen local `reclutamiento-php:dev`, compartida con el proyecto habitual, y el arranque usa `--no-build` para no reconstruirla. Primero se comprueba que existe:

```powershell
docker image inspect reclutamiento-php:dev --format "{{.Id}}"
```

**Si falta** (el comando responde que la imagen no existe, o `up --no-build` falla porque no la encuentra y no puede descargarla, ya que no está publicada en ningún registro), se construye una vez desde `docker/php/Dockerfile`:

```powershell
docker compose -p entregaacad build app
```

- Esto crea la etiqueta `reclutamiento-php:dev`, la misma que usa el proyecto habitual. Si este último no la tenía, también la usará. No toca sus contenedores ni sus volúmenes.
- Si la construcción falla por red, hay que reintentarla con conexión. No hay imagen alternativa publicada.

Las imágenes `postgres:17.11-alpine`, `redis:7.4.11-alpine` y `cypress/included:15.3.0` se descargan solas la primera vez que se usan; también necesitan internet.

## 3. Arrancar el SaaS y cargar los datos ficticios

```powershell
docker compose -p entregaacad up -d --wait --no-build app
docker compose -p entregaacad ps                                                  # comprobar que son contenedores entregaacad-*
docker compose -p entregaacad exec app php artisan migrate:fresh --seed --force   # reinicia SOLO la base ficticia de entregaacad
```

- **La app** queda en `http://localhost:8010`. Todas las cuentas demo usan la contraseña `password` (solo demostración); los correos están en [`demo-users.md`](../demo-users.md).
- **Reiniciar los datos** (por ejemplo, para repetir la decisión del guion) es el mismo `migrate:fresh` con `-p entregaacad`. Solo borra y recarga la base del volumen `entregaacad_pgdata`, que contiene únicamente datos de `DemoSeeder`. **No se ejecuta nunca sin `-p entregaacad`**: sin esa opción apuntaría al proyecto habitual y borraría su base de desarrollo.
- **Detener:** `docker compose -p entregaacad down`, que conserva los volúmenes. Para borrarlos también, se añade `-v`; solo afecta a `entregaacad_*`.

## 4. Arrancar ML-01 (RF-29, experimental y opcional)

En otra terminal, desde `ml-service/`:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -e ".[dev]"                 # dependencias fijadas en pyproject.toml
.venv\Scripts\python.exe -m recruitment_ml.serving.build_artifact   # reconstruye el modelo desde el freeze aprobado
$env:RECRUITMENT_ML_INTERNAL_TOKEN = "<secreto local, el mismo que ML_SERVICE_TOKEN>"
.venv\Scripts\python.exe -m uvicorn recruitment_ml.api.app:app --host 0.0.0.0 --port 8008
```

Después, en el `.env` de la raíz:

```
ML_SERVICE_ENABLED=true
ML_SERVICE_URL=http://host.docker.internal:8008
ML_SERVICE_TOKEN=<el mismo secreto>
```

Y se recarga la configuración: `docker compose -p entregaacad exec app php artisan config:clear`.

- **Comprobación:** `curl http://127.0.0.1:8008/health` debe devolver `{"status":"ok","model_ready":true,…}`.
- **Respaldo:** si uvicorn se detiene (Ctrl+C), la plataforma funciona igual y el panel muestra «Servicio no disponible», sin inventar una estimación.

## 5. Pruebas

```powershell
docker compose -p entregaacad exec app php artisan test          # PHPUnit
docker compose -p entregaacad exec app npx tsc --noEmit          # tipos
docker compose -p entregaacad exec app npm run build             # frontend
docker compose -p entregaacad exec app npx vp test --run         # componentes
docker compose -p entregaacad run --rm --no-deps --entrypoint sh app docker/php/init-e2e-env.sh   # crea .env.e2e si falta
docker compose -p entregaacad --profile e2e run --rm cypress     # Cypress, con su base E2E aislada
cd ml-service; .venv\Scripts\python.exe -m pytest                # ML-01
```

- **Cypress** se ejecuta contra `app-e2e`, que tiene su propia base E2E dentro de `entregaacad`. Para detener ese entorno: `docker compose -p entregaacad --profile e2e stop app-e2e queue-e2e`.
- **Con poca memoria**, conviene ejecutar Cypress con ML-01 detenido, o solo los specs necesarios: `... run --rm cypress --spec "cypress/e2e/e2e-20-recorrido-demo.cy.js"`.

## 6. Datos de prueba

Todo es ficticio: nombres con «(demo)» o «(ficticio/a)», correos `.test` y CV de ejemplo.

`DemoSeeder` carga:

- dos organizaciones;
- requerimientos en cada estado;
- vacantes en borrador, publicada con postulaciones, con el ranking pendiente de decisión y con el proceso concluido;
- desde esta entrega, el escenario de riesgo operacional para ML-01 (DEF-18).

El detalle está en [`demo-users.md`](../demo-users.md).
