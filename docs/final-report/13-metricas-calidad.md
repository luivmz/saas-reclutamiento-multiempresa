# Capítulo 13. Métricas de calidad

Todas las métricas provienen de ejecuciones reales. **Última verificación: QA final de la Fase 12 (2026-09-13, rama `release/qa-final`, base `904ce72`).**

| Verificación QA final | Resultado |
|---|---|
| PHPUnit completo | 244 pruebas · 236 superadas · 0 fallidas · 8 omitidas · 1074 aserciones · 32,25 s |
| Cypress completo (entorno E2E aislado) | 14 specs · 43 tests · 43 superados · 0 fallidos · 0 omitidos · 03:32 · Electron 136 |
| `npm run build` | Correcto (19,90 s) |
| `npx tsc --noEmit` | 0 errores |
| Migraciones | 17 aplicadas, 0 pendientes (entornos normal y E2E) |
| Cobertura porcentual de código | **No medida** |

## 13.1 Pruebas PHPUnit

| Métrica | Valor |
|---|---|
| Pruebas totales | **244** |
| Superadas | **236** |
| Fallidas | **0** |
| Omitidas | **8** (*starter kit*: funciones de Fortify desactivadas) |
| Aserciones | **1074** |
| Suite Unit | 62 casos superados (85 aserciones), de 6 clases y 34 métodos |
| Suite Feature | 174 superados + 8 omitidos (989 aserciones), de 33 clases y 182 métodos |
| Tasa de aprobación sobre ejecutadas | 236 / 236 = **100 %** |
| Tasa de aprobación sobre el total | 236 / 244 = **96,7 %** (las omitidas no son fallos) |
| Métodos nombrados por RF (`test_rfNN_*`) | 106 |
| Cobertura porcentual de código | **No medida** |

**Evolución de la suite completa** (cierre de cada fase):

| Fase | Pruebas | Superadas | Omitidas | Fallidas | Aserciones |
|---|---|---|---|---|---|
| 2 | 39 | 31 | 8 | 0 | — (no registrado) |
| 3 | 99 | 91 | 8 | 0 | — |
| 4 | 137 | 129 | 8 | 0 | — |
| 5 | 160 | 152 | 8 | 0 | 532 |
| 6 | 211 | 203 | 8 | 0 | 779 |
| 7 | 230 | 222 | 8 | 0 | 1017 |
| 8 | 233 | 225 | 8 | 0 | 1045 |
| 9 | 240 | 232 | 8 | 0 | 1064 |
| 10 | 244 | 236 | 8 | 0 | 1074 |
| 12 (QA final) | 244 | 236 | 8 | 0 | 1074 |

En las fases 2 a 4 el total se calcula como superadas + omitidas, porque las aserciones no se registraron (`docs/tdd-evidence.md`).

## 13.2 Pruebas E2E (Cypress)

| Métrica | Valor |
|---|---|
| Specs | **14** (E2E-01 a E2E-13 + `e2e-00` de soporte) |
| Tests | **43** |
| Superados / fallidos / omitidos (última corrida) | **43 / 0 / 0** |
| Tasa de aprobación | **100 %** |
| Corridas completas consecutivas en verde | 2 en la Fase 9 (40/40), 2 en la Fase 10 (43/43: instalación limpia y entorno principal) y 1 en el QA final de la Fase 12 (43/43, 03:32) |
| Reintentos automáticos | 0 (deshabilitados) |
| Duración de la suite | 03:26 a 04:01 según la corrida |
| Navegador | Electron 136 (*headless*) |

## 13.3 Validación manual (Fase 8)

| Métrica | Valor |
|---|---|
| Recorrido visual por rol | 10/10 casos, 49 capturas |
| Flujo integral manual | 12/12 pasos |

## 13.4 Requerimientos

| Métrica | Valor |
|---|---|
| RF en la línea base | 27 |
| RF implementados | 27 (**100 %**) |
| RF con pruebas PHPUnit | 27 (**100 %**) |
| RF ejercidos por Cypress | 27 (**100 %**; RF-04 y RF-17 verifican parte del comportamiento solo en PHPUnit) |
| Supuestos documentados | 36 (A-01 a A-36) |

## 13.5 Defectos

Fuente: `docs/defects.md`.

| ID | Categoría | Severidad | Descripción | Detección | Corrección | Estado |
|---|---|---|---|---|---|---|
| DEF-01 | Entorno | Alta | Contenedor `app` *unhealthy*: `artisan serve` recargaba `.env` y rompía la conexión a Redis | *Healthcheck* de Docker | Hosts de servicio en `.env.example`; `/health` fuera del grupo `web` | Cerrado |
| DEF-02 | Entorno / pruebas | Crítica | PHPUnit corría contra la base de desarrollo por variables de `env_file` | `php artisan test` | Sin `env_file`; `force="true"` en `phpunit.xml` | Cerrado |
| DEF-03 | Funcional | Alta | `MassAssignmentException` al crear el perfil de la vacante | `VacancyPublicationTest` | Asignación explícita en `VacancyService::saveProfile()` | Cerrado |
| DEF-04 | Build / frontend | Media | *Build* y `tsc` rotos por rutas de verificación de correo inexistentes | `npm run build` / `tsc` | Se retiraron las referencias huérfanas | Cerrado |
| DEF-05 | Funcional | Alta | Props de detalle envueltas en `data` (fallo en tiempo de ejecución no detectado por `tsc`) | `ApplicationReviewTest` | `JsonResource::withoutWrapping()` y aserciones de regresión | Cerrado |
| DEF-06 | Funcional | Crítica | `session()` sobrescrito en un Form Request terminaba el proceso PHP | `EvaluationTest` | Renombrado a `assessmentSession()` | Cerrado |
| DEF-07 | Seguridad | Alta | La auditoría podía modificarse o borrarse con consultas masivas | `AuditTrailTest` (RED) | *Trigger* PostgreSQL de solo inserción | Cerrado |
| DEF-08 | Seguridad | Media | Sin eliminación de `cookie`, `authorization` y `api_key` en la auditoría | `AuditTrailTest` (RED) | Patrón de claves sensibles ampliado | Cerrado |
| DEF-09 | UI / localización | Media | Fechas en la zona horaria del navegador y no en `America/Lima` | Validación en navegador | `<meta name="app-timezone">` + `Intl` con `timeZone`; `AppTimezoneTest` | Cerrado |
| DEF-10 | UI | Baja | Auditoría con valores internos y fecha en UTC | Validación en navegador | Etiquetas y hora local en `AuditLogResource`; prueba nueva | Cerrado |
| DEF-11 | UI | Baja | Iniciales de avatar inválidas («C(») | Validación en navegador | `useInitials` ignora palabras sin letras (verificado en capturas) | Cerrado |
| DEF-12 | Pruebas | Media | Fechas E2E en UTC, con riesgo entre las 19:00 y las 24:00 de Lima (no observado) | Revisión de la Fase 9 | `appDate()` en `America/Lima`; `e2e-00-app-dates` | Cerrado |
| DEF-13 | Pruebas / entorno | Alta | El reset E2E borraba la base de desarrollo y demostración | Revisión de la Fase 9 | Entorno E2E aislado + reset limitado a `E2E_DATABASE`; `E2eSupportTest`, `E2eEnvironmentTest` | Cerrado |

**Resumen de defectos:**

| Métrica | Valor |
|---|---|
| Registrados | 13 |
| Corregidos (cerrados) | 13 (**100 %**) |
| Por severidad | Crítica 2 · Alta 5 · Media 4 · Baja 2 |
| Por categoría | Funcional 3 (DEF-03, 05, 06) · Seguridad 2 (DEF-07, 08) · UI y localización 3 (DEF-09, 10, 11) · Entorno 1 (DEF-01) · Entorno/pruebas 2 (DEF-02, 13) · Pruebas 1 (DEF-12) · *Build* 1 (DEF-04) |
| Detectados por pruebas automatizadas (PHPUnit/*build*) | 7 (DEF-02 a DEF-08) |
| Detectados en validación en navegador | 3 (DEF-09 a DEF-11) |
| Detectados por el entorno o en revisión | 3 (DEF-01, DEF-12, DEF-13) |
| Tests E2E corregidos por expectativas erróneas (no son defectos del producto) | 2 |

## 13.6 Construcción

| Métrica | Último resultado |
|---|---|
| `npm run build` | Correcto |
| `npx tsc --noEmit` | 0 errores |
| Migraciones en instalación limpia | 17 ejecutadas, 0 pendientes |
| Arranque desde cero con Docker | 87 s hasta servicios *healthy* |

## 13.7 Métricas no disponibles

No se reportan porque no se midieron:
- cobertura porcentual de código;
- tiempos de respuesta y carga;
- vulnerabilidades por análisis dinámico o estático;
- deuda técnica;
- complejidad ciclomática;
- métricas de accesibilidad.
