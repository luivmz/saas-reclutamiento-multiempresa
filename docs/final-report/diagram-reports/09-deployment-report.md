# Informe del diagrama de despliegue

## 1. Propósito

Representar los nodos físicos y lógicos donde se ejecuta el sistema y sus dependencias.

**Artefacto original:** `Diagramas/PD/deploydiagrama.oom` (PowerDesigner, carpeta del curso, fuera del repositorio). No se modificó.

## 2. Elementos principales

**Nodos y componentes del diagrama original:**
- Cliente
- Internet / HTTPS
- Servidor Web / Aplicación
- PostgreSQL
- Redis
- S3
- Queue Worker

**Despliegue implementado** (`docker-compose.yml`):

| Servicio | Imagen | Función | Exposición | Healthcheck |
|---|---|---|---|---|
| `app` | `reclutamiento-php:dev` (PHP 8.4.25, Node 22.23.2) | Laravel con `php artisan serve` | `${APP_PORT:-8000}` | `GET /health` (base de datos y Redis) |
| `queue` | `reclutamiento-php:dev` | `queue:work redis --tries=3 --max-time=3600` | — | Proceso vivo + `queue:monitor` |
| `postgres` | `postgres:17.11-alpine` | Bases `reclutamiento`, `reclutamiento_testing` y `reclutamiento_e2e` | `127.0.0.1:5432` | `pg_isready` |
| `redis` | `redis:7.4.11-alpine` | Sesiones, caché y colas | `127.0.0.1:6379` | `redis-cli ping` |
| `app-e2e` (perfil `e2e`) | `reclutamiento-php:dev` | Aplicación aislada para pruebas (`APP_ENV=e2e`) | `127.0.0.1:8001` | `GET /health` |
| `queue-e2e` (perfil `e2e`) | `reclutamiento-php:dev` | Worker del entorno E2E | — | Igual que `queue` |
| `cypress` (perfil `e2e`) | `cypress/included:15.3.0` | Suite E2E (Electron 136) | — | — |

Volúmenes: `pgdata`, `redisdata`, `vendor` y `node_modules`. Almacenamiento de CV: disco local privado `storage/app/private` (montado desde el repositorio).

## 3. Relación con requerimientos

- Soporta todos los RF.
- Redis y el worker sostienen las notificaciones: RF-04, RF-11, RF-15, RF-17 y RF-26.
- El almacenamiento de archivos sostiene RF-09.
- RNF de portabilidad (RNF-09).

## 4. Relación con implementación

- Configuración: `docker-compose.yml`, `docker/php/Dockerfile`, `docker/php/entrypoint.sh` y `docker/postgres/init/*.sql`.
- Guía: `docs/docker.md` y [capítulo 10](../10-dockerizacion.md).
- **Validación real (Fase 10):**
  - Instalación limpia en 87 s con servicios *healthy*, 17 migraciones, *seed*, *smoke*, PHPUnit 244 (236 superadas) y Cypress 43/43.
  - Entorno principal: Cypress 43/43.

## 5. Consistencias

- El servidor de aplicación (`app`), PostgreSQL, Redis y el worker de colas (`queue`) existen, con las mismas dependencias que muestra el diagrama.
- El cliente accede por HTTP al servidor de aplicación.

## 6. Diferencias detectadas

1. **S3.** El diagrama incluye S3; la implementación **no usa S3 ni R2**: los CV se almacenan en disco local privado. El almacenamiento en la nube es una mejora futura.
2. **HTTPS / Internet.** El diagrama supone acceso por Internet con HTTPS. El entorno implementado es **local de desarrollo y demostración**, con HTTP en `localhost` y sin certificado ni proxy inverso.
3. **Perfil E2E.** El diagrama no incluye el entorno de pruebas aislado (`app-e2e`, `queue-e2e`, `cypress`) ni la base `reclutamiento_e2e`.
4. **Contenedores.** El diagrama no representa Docker Compose ni los *healthchecks*.
5. **Servidor.** El servidor de aplicación usa `php artisan serve` (imagen de desarrollo), no un servidor web de producción (A-36).

## 7. Limitaciones

- El artefacto está fuera del repositorio.
- Representa un despliegue objetivo o conceptual, no el entorno Docker entregado.
- No existe infraestructura productiva ni en la nube.

## 8. Estado para entrega

**Vigente con observaciones.** Es válido como vista conceptual de nodos; el despliegue entregado es el descrito en la sección 2.

## 9. Recomendación

En una futura versión gráfica:
- reemplazar S3 por «almacenamiento local privado» (o marcar S3 como futuro);
- rotular el entorno como «Docker Compose local»;
- añadir el perfil E2E y los *healthchecks*;
- separar un diagrama de despliegue productivo futuro (HTTPS, servidor web, almacenamiento en la nube) del entorno académico actual.
