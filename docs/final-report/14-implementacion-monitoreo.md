# Capítulo 14. Implementación y monitoreo

> La implementación actual es un **entorno reproducible de desarrollo y demostración académica** con Docker Compose. **No existe infraestructura productiva ni despliegue en la nube.**

## 14.1 Instalación

Procedimiento completo y solución de problemas en `docs/docker.md`. Resumen:

```powershell
copy .env.example .env                                              # opcional
docker compose up -d --build --wait                                 # app, queue, postgres, redis
docker compose exec app php artisan migrate:fresh --seed --force    # datos demo ficticios
```

- Aplicación: http://localhost:8000.
- Usuarios ficticios: `docs/demo-users.md` (contraseña de demostración `password`).

## 14.2 Entorno Docker

- **Servicios:** `app`, `queue`, `postgres`, `redis`, y el perfil `e2e` (`app-e2e`, `queue-e2e`, `cypress`).
- **Versiones:** fijadas.
- **Healthchecks:** en todos los servicios de larga duración.
- **Reinicio:** `restart: unless-stopped`.
- **Puertos:** base de datos y Redis solo en *loopback*.
- **Detalle:** [capítulo 10](10-dockerizacion.md).

## 14.3 Monitoreo disponible

| Mecanismo | Uso | Cómo consultarlo |
|---|---|---|
| Endpoint de salud | `GET /health`: `{"status":"ok","checks":{"database":"ok","redis":"ok"},"time":"…"}`; responde error si falla la base de datos o Redis | `curl http://localhost:8000/health` |
| Estado de contenedores | *Healthchecks* de `app`, `queue`, `postgres` y `redis` | `docker compose ps` |
| Logs de Laravel | Canal `stack` (`single` + `stderr`): `storage/logs/laravel.log` y salida del contenedor | `docker compose logs -f app` |
| Worker de colas | Proceso `queue:work` vigilado por su *healthcheck* (proceso vivo + Redis), reinicio automático, `--tries=3` | `docker compose logs -f queue` · `docker compose ps queue` |
| Trabajos fallidos | Tabla `failed_jobs` del framework | `docker compose exec app php artisan queue:failed` |
| Auditoría funcional | `audit_logs` de solo inserción; vista `audit/index` para Aprobador/Dirección con filtro por acción | Navegador (rol Dirección) |
| Correo | *Driver* `log`: los correos se registran en el log, sin envío real | `storage/logs/laravel.log` |

**No existe:**
- monitoreo externo (Sentry, APM);
- alertas;
- métricas de infraestructura;
- centralización de logs.

## 14.4 Pruebas de humo

| Prueba | Resultado real |
|---|---|
| Instalación limpia (Fase 10) | `/health` 200, `/login` 200, `/empleos` 200 con la vacante demo; `/__e2e/reset` 404 en el entorno normal |
| Validación manual en navegador (Fase 8) | Recorrido visual 10/10 y flujo integral 12/12 (`docs/manual-smoke-test.md`) |
| Suite E2E | 14 specs, 43/43 ([capítulo 12](12-automatizacion-pruebas.md)) |

## 14.5 Operación de la demostración

- **Antes de exponer:** `docker compose up -d --wait` y `docker compose exec app php artisan migrate:fresh --seed --force`.
- **Guion:** [demo-script.md](demo-script.md).
- **Si algo falla:** revisar `docker compose ps`, `/health` y `docker compose logs app`.

---

# Conclusiones

1. **Línea base funcional.** Se cumplió íntegramente la línea base: los 27 RF (RF-01 a RF-27) están implementados con backend, interfaz y pruebas, y trazados a su código y evidencia en la matriz maestra, sin agregar requerimientos fuera del alcance. Esto atiende los problemas P1 a P4 del análisis preliminar. P5 se cubre parcialmente con la comparación y la auditoría.
2. **Decisión humana verificable.** La regla crítica se convirtió en un comportamiento comprobable. El ranking ponderado es explicable y solo apoya: calcularlo no altera estados ni decisiones (`test_rf23_calculating_the_ranking_never_selects_a_candidate`, E2E-08). La decisión final exige al Aprobador/Dirección, con confirmación explícita y justificación, y puede recaer en un candidato que no sea el primero (E2E-09).
3. **Multiempresa segura en la aplicación.** Las organizaciones quedan aisladas mediante `organization_id`, un *scope* global y Policies que comparan la organización del usuario con la del recurso. Pruebas *cross-tenant* en PHPUnit y E2E-11 muestran que los recursos ajenos se rechazan sin efectos. La defensa en profundidad con RLS queda como mejora.
4. **Calidad basada en evidencia.** TDD con RED observado, 244 pruebas PHPUnit (236 superadas, 0 fallidas) sobre PostgreSQL real y 13 defectos registrados y corregidos dan evidencia reproducible, no declarativa. Varios defectos de seguridad (auditoría modificable, datos sensibles) aparecieron precisamente al escribir primero la prueba.
5. **Automatización estable.** La suite Cypress (14 specs, 43 tests) pasó sin reintentos en corridas consecutivas y en una instalación limpia. Esto fue posible por los selectores estables, las esperas basadas en estado real y el reset limitado a una base E2E aislada, que ya no pone en riesgo los datos de demostración.
6. **Portabilidad demostrada.** Un clon limpio levantó todos los servicios, migró, cargó los datos demo y pasó las pruebas en minutos, sin dependencias locales ni rutas del equipo de desarrollo. La entrega no depende del entorno de un integrante.

# Recomendaciones (mejoras futuras, no implementadas)

| # | Recomendación | Motivo |
|---|---|---|
| 1 | Validar el AS-IS y el TO-BE con RR. HH./Administración del colegio y anexar los BPMN definitivos | El análisis actual es preliminar |
| 2 | Row Level Security de PostgreSQL por `organization_id` | Defensa en profundidad del aislamiento multiempresa |
| 3 | Integración continua (p. ej., GitHub Actions) con PHPUnit, *build*, `tsc` y Cypress | Regresión automática en cada cambio |
| 4 | Análisis estático (PHPStan/Larastan) y medición de cobertura | Métricas de calidad hoy no disponibles |
| 5 | Pruebas de carga (k6) y definición de objetivos de rendimiento | La eficiencia de desempeño no se evaluó |
| 6 | Pruebas dinámicas de seguridad (OWASP ZAP) y revisión según OWASP Top 10 | Complementar los controles implementados |
| 7 | Monitoreo de errores (p. ej., Sentry) y alertas | Hoy solo hay `/health` y logs |
| 8 | Almacenamiento de archivos en la nube (S3/R2) y despliegue con imagen de producción, HTTPS y usuario no *root* | La imagen actual es de desarrollo y demostración (A-36) |
| 9 | Indicadores de gestión del proceso (tiempos, embudo) | Completar la atención de P5 |
| 10 | Ampliación del SaaS: administración de organizaciones, cierre sin selección si el TO-BE lo define, envío real de correo | Fuera de la línea base actual |
| 11 | Actualizar los diagramas UML de selección y despliegue a la implementación final | Ver discrepancias en el capítulo 6 |

# Referencias

Solo fuentes oficiales o de uso estándar para la tecnología y las normas empleadas. Las fechas de consulta deben completarse al preparar la versión final del informe.

- Beck, K. (2003). *Test-driven development: By example*. Addison-Wesley.
- Chacon, S., & Straub, B. (2014). *Pro Git* (2.ª ed.). Apress. https://git-scm.com/book
- Cypress.io. (s. f.). *Cypress documentation*. https://docs.cypress.io
- Docker Inc. (s. f.). *Docker Compose documentation*. https://docs.docker.com/compose/
- Inertia.js. (s. f.). *Inertia.js documentation*. https://inertiajs.com
- International Organization for Standardization. (2023). *ISO/IEC 25010:2023. Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — Product quality model*. https://www.iso.org/standard/78176.html
- Laravel. (s. f.). *Laravel documentation (13.x)*. https://laravel.com/docs/13.x
- Meta Open Source. (s. f.). *React documentation*. https://react.dev
- OWASP Foundation. (s. f.). *OWASP Top Ten*. https://owasp.org/www-project-top-ten/
- PHPUnit. (s. f.). *PHPUnit manual*. https://docs.phpunit.de
- PostgreSQL Global Development Group. (s. f.). *PostgreSQL 17 documentation*. https://www.postgresql.org/docs/17/
- Redis Ltd. (s. f.). *Redis documentation*. https://redis.io/docs/
- Tailwind Labs. (s. f.). *Tailwind CSS documentation*. https://tailwindcss.com/docs

# Índice de anexos

Rutas y estado de cada evidencia: [evidence-index.md](evidence-index.md).

| Anexo | Contenido | Ubicación | Estado |
|---|---|---|---|
| A | BPMN AS-IS | — | **Pendiente**: no está en el repositorio |
| B | BPMN TO-BE | — | **Pendiente**: no está en el repositorio (flujo derivado de la implementación en el capítulo 3) |
| C | Casos de uso | [04-requerimientos.md](04-requerimientos.md#44-casos-de-uso) | Catálogo derivado; falta contrastarlo con la práctica de casos de uso |
| D | Arquitectura y despliegue | [06-diseno-sistema.md](06-diseno-sistema.md), [10-dockerizacion.md](10-dockerizacion.md), `Diagramas/PD/deploydiagrama.oom` (carpeta del curso, fuera del repositorio) | Disponible (el diagrama `.oom` difiere parcialmente) |
| E | Modelo de datos (ERD) | [06-diseno-sistema.md](06-diseno-sistema.md#67-modelo-de-datos), `database/migrations` | Disponible |
| F | Diagramas de secuencia | [06-diseno-sistema.md](06-diseno-sistema.md#65-secuencias-principales), `Diagramas/PD/*.oom` | Disponible (el de selección difiere) |
| G | Matriz de trazabilidad RF | [traceability-master.md](traceability-master.md), `docs/rf-implementation-matrix.md` | Disponible |
| H | Evidencia TDD | `docs/tdd-evidence.md` | Disponible |
| I | Suite Cypress y resultados | `docs/testing/cypress-e2e.md`, `cypress/` | Disponible |
| J | Docker y portabilidad | `docs/docker.md`, `docker-compose.yml`, `docker/` | Disponible |
| K | Historial Git | [09-control-versiones.md](09-control-versiones.md) | Disponible |
| L | Defectos y supuestos | `docs/defects.md`, `docs/assumptions.md` | Disponible |
| M | Validación manual en navegador | `docs/manual-smoke-test.md` (las capturas son locales y no están versionadas) | Documento disponible; capturas pendientes de seleccionar |
