# DE-01 · Diagrama de despliegue

| | |
|---|---|
| **Objetivo** | Mostrar dónde se ejecuta cada artefacto en el entorno real del proyecto |
| **Alcance** | Entorno de desarrollo y demostración definido en `docker-compose.yml`, más el servicio de inferencia que corre **fuera** de Compose. El perfil `e2e` va aparte, como nota. **No existe un entorno de producción desplegado** |
| **Fuente de verdad** | `docker-compose.yml`, `docker/php/Dockerfile`, `docker/php/entrypoint.sh`, `docker/postgres/init/*`, `.env.example`, `config/ml.php`, `config/filesystems.php`, `docs/v1.1/phase-16-laravel-ml-integration.md` §«Cómo ejecutarlo» |
| **Borrador textual** | [`puml/de-01-deployment.puml`](puml/de-01-deployment.puml) |
| **RF** | Transversal; RF-09 (almacenamiento de CV), RF-27 (PostgreSQL), RF-29 (servicio de inferencia) |

## 1. Nodos, entornos de ejecución y artefactos

Notación: **nodo** = máquina o contenedor; **entorno de ejecución** = runtime dentro del nodo; **artefacto** = lo que se despliega; **almacén** = datos persistentes.

| Elemento | Tipo UML | Real |
|---|---|---|
| Equipo del usuario | Nodo `<<device>>` | Navegador web |
| Navegador | Entorno de ejecución | Ejecuta el *bundle* JS/CSS compilado por Vite (React + Inertia) |
| Equipo anfitrión | Nodo `<<device>>` | Máquina que ejecuta Docker Engine y, aparte, el proceso Python del servicio de inferencia |
| Docker Engine (proyecto `reclutamiento`) | Entorno de ejecución | Orquesta los contenedores de `docker-compose.yml` |
| Contenedor `app` | Nodo `<<container>>` | Imagen `reclutamiento-php:dev` (PHP 8.4 CLI, Node 22) |
| PHP 8.4 (`php artisan serve`, puerto 8000) | Entorno de ejecución | Sirve Laravel **y** los recursos estáticos de `public/build` |
| Aplicación Laravel | Artefacto | Código montado desde el repositorio (`.:/var/www/html`) |
| `public/build` | Artefacto | *Bundle* del frontend. Lo genera `npm run build` en el `entrypoint.sh` al arrancar el contenedor |
| Contenedor `queue` | Nodo `<<container>>` | Misma imagen; ejecuta `php artisan queue:work redis --tries=3` |
| Contenedor `postgres` | Nodo `<<container>>` | `postgres:17.11-alpine`; bases `reclutamiento`, `reclutamiento_testing`, `reclutamiento_e2e`; volumen `pgdata` |
| Contenedor `redis` | Nodo `<<container>>` | `redis:7.4.11-alpine`; sesión, caché y cola; volumen `redisdata` |
| `storage/app/private` | Almacén (sistema de archivos) | CV en PDF. Vive en el árbol del repositorio montado en `app`; no es un volumen propio ni almacenamiento en la nube |
| Proceso Python (`uvicorn`, puerto 8008) | Entorno de ejecución en el **anfitrión** `<<experimental>>` | `ml-service/.venv`; `recruitment_ml.api.app:app` |
| Artefacto del modelo | Artefacto | `ml-service/artifacts/` (`.joblib` + metadatos), no versionado |

## 2. Comunicaciones

| De | A | Protocolo | Detalle |
|---|---|---|---|
| Navegador | `app` | HTTP, puerto `${APP_PORT:-8000}` | Páginas Inertia, recursos de `public/build`, JSON de riesgo operacional |
| `app`, `queue` | `postgres` | TCP 5432 (red interna de Compose) | Publicado solo en `127.0.0.1` del anfitrión |
| `app`, `queue` | `redis` | TCP 6379 (red interna) | Publicado solo en `127.0.0.1` |
| `app` | Servicio de inferencia | HTTP a `host.docker.internal:8008` | `POST /v1/predict` con `X-Internal-Token`. **Solo si `ML_SERVICE_ENABLED=true`** (por defecto `false`) |
| `queue` | Mailer `log` | Local | En desarrollo el correo se escribe en el *log*: no hay servidor SMTP ni proveedor |

## 3. Decisiones y precisiones

- **El frontend no es un servidor.** No hay contenedor de Node ni servidor de Vite en Compose: Vite compila y Laravel sirve lo compilado. Dibujar React como nodo propio sería falso.
- **FastAPI no está en Docker Compose.** Se ejecuta como proceso en el anfitrión y Laravel lo alcanza por `host.docker.internal`. Es la configuración documentada en las Fases 16 y 17, y así se dibuja: nodo anfitrión con dos entornos, Docker y Python.
- **Sin producción.** Esto es el entorno de desarrollo y demostración. No se modelan balanceadores, HTTPS, CDN, nube ni réplicas porque no existen.
- **Perfil `e2e`** (`app-e2e` en `127.0.0.1:8001`, `queue-e2e`, `cypress`): infraestructura de pruebas. Nota aparte o diagrama secundario, no parte del sistema en operación.
- **Healthchecks** (`/health`, `pg_isready`, `redis-cli ping`, `queue:monitor`): atributos de los nodos, no componentes.

## 4. Contraste con v1.0

El informe [`09-deployment-report.md`](../../final-report/diagram-reports/09-deployment-report.md) recoge que el diagrama original de v1.0 incluía **S3**, que nunca se implementó (los CV van al disco local privado). Este diagrama no lo incluye. Novedad de v1.1: el servicio de inferencia experimental en el anfitrión.

## 5. Instrucciones para F23

1. *Deployment Diagram* «DE-01 Despliegue AS-IS v1.1 (desarrollo y demostración)».
2. Nodos de §1 con estereotipos `<<device>>` y `<<container>>`; el proceso Python con `<<experimental>>`.
3. Enlaces de §2 con protocolo y puerto; el enlace a la inferencia con la condición `ML_SERVICE_ENABLED=true`.
4. Nota de que no hay entorno de producción ni componentes de nube.
