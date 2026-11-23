# Módulo de Reportes de Reclutamiento

> Actividad 5.1 y 5.2 de la guía. Implementación **real** sobre el monolito existente, trazada al candidato **RF-28** de [`docs/v1.1/scope-preliminary.md`](../../v1.1/scope-preliminary.md): «Panel operativo de seguimiento de convocatorias: etapas, tiempos y cuellos de botella, sin datos de personas». Implementarlo **no** lo promueve al baseline: RF-01 a RF-27 no cambian (decisión 11).

## 1. Acceso

| Elemento | Valor |
|---|---|
| Ruta | `GET /reportes` (nombre `reports.index`), dentro del grupo `auth` de `routes/web.php` |
| Menú | «Reportes» (`data-cy="nav-reports"`) para **RR. HH.** (grupo Reclutamiento) y **Aprobador/Dirección** (grupo Dirección); también aparece en el panel de inicio |
| Autorización | `Gate::define('viewRecruitmentReports', [RecruitmentReportPolicy::class, 'view'])`: RR. HH. o Aprobador **con** `organization_id`. Solicitante, Evaluador y Postulante reciben **403** |
| Abrirlo localmente | `docker compose up -d --wait` → `http://localhost:8000/login` → `rrhh@andino.test` o `direccion@andino.test` (contraseña demo en [`docs/demo-users.md`](../../demo-users.md)) → menú «Reportes» |

## 2. Archivos

| Capa | Archivo | Nuevo o modificado |
|---|---|---|
| Ruta | `routes/web.php` (+2 líneas) | Modificado |
| Gate | `app/Providers/AppServiceProvider.php` (+3 líneas) | Modificado |
| Policy | `app/Policies/RecruitmentReportPolicy.php` | Nuevo |
| Form Request | `app/Http/Requests/Reports/RecruitmentReportRequest.php` | Nuevo |
| Controlador | `app/Http/Controllers/Reports/RecruitmentReportController.php` | Nuevo |
| Servicio | `app/Services/Reports/RecruitmentReportService.php` | Nuevo |
| Página | `resources/js/pages/reports/index.tsx` | Nuevo |
| Utilidades TS | `resources/js/lib/reports.ts` | Nuevo |
| Navegación | `resources/js/lib/navigation.ts` (+ entrada «Reportes») | Modificado |
| Pruebas PHPUnit | `tests/Feature/Reports/RecruitmentReportTest.php` (12 pruebas) | Nuevo |
| Pruebas Vitest | `resources/js/lib/reports.test.tsx` (6 pruebas) | Nuevo |
| Pruebas Cypress | `cypress/e2e/e2e-20-reports.cy.js` (9 escenarios) | Nuevo |

**Sin migraciones, sin tablas nuevas y sin dependencias nuevas.** Los gráficos son barras HTML/CSS con los tokens del tema (`--primary`) porque `package.json` no tenía biblioteca de gráficos y la visualización requerida (barras de una serie) no la justifica.

## 3. Indicadores (KPI)

Cinco KPI se calculan sobre las **postulaciones cuya `applied_at` cae en el período** y que cumplen los filtros de vacante y etapa, dentro de la organización del usuario. El KPI de vacantes publicadas usa `vacancies.published_at`, la misma organización y el filtro de vacante: **la etapa de postulación no le aplica**, porque no es un atributo de la vacante.

| KPI (`data-cy`) | Definición exacta | Fuente |
|---|---|---|
| Postulaciones recibidas (`kpi-applications`) | `count(applications)` filtradas | `applications` |
| Vacantes publicadas en el período (`kpi-published-vacancies`) | Vacantes no borrador con `published_at` en el período (respeta el filtro de vacante; la etapa no aplica) | `vacancies` |
| Promedio de postulaciones por vacante (`kpi-average-per-vacancy`) | postulaciones ÷ vacantes distintas que recibieron postulaciones; `null` → «—» | `applications` |
| Llegaron a la preselección + tasa (`kpi-reached-shortlist`) | Postulaciones con un registro `to_status = preseleccionado` en el historial **o** cuya etapa actual solo es alcanzable tras la preselección (preseleccionado, en evaluación, en entrevista, finalista, seleccionado). Tasa = alcanzadas ÷ postulaciones × 100, con un decimal | `application_stage_histories`, `applications` |
| En evaluación o entrevista (`kpi-in-assessment`) | Etapa actual `en_evaluacion` o `en_entrevista` | `applications` |
| Tiempo promedio hasta la preselección (`kpi-days-to-shortlist`) | Promedio, en días, de (primer `created_at` del historial hacia preseleccionado − `applied_at`). Solo sobre preselecciones con fecha registrada; `null` si no hay ninguna | `application_stage_histories` |

Los valores ausentes se muestran como «—», no como 0, para no inventar una medición.

## 4. Reportes estadísticos (gráficos y tabla)

| Visualización (`data-cy`) | Tipo | Datos |
|---|---|---|
| Postulaciones por etapa actual (`chart-by-status`) | Barras horizontales, una serie, escala desde 0 | Las 8 etapas de `ApplicationStatus`, en orden del proceso, incluidas las de valor 0 |
| Postulaciones por semana (`chart-by-week`) | Columnas (máx. 24 px) por semana lunes–domingo; las semanas sin registros valen 0 | Semanas del período; detalle al pasar el cursor y tabla equivalente oculta (`sr-only`) para lectores de pantalla |
| Detalle por vacante (`report-vacancy-table`) | Tabla accesible (`DataTable`) con barra proporcional | Vacante, estado, postulaciones, preseleccionadas, tasa y en evaluación/entrevista, ordenadas por postulaciones |

Los cinco indicadores de postulaciones, los gráficos y la tabla salen de **la misma colección filtrada**. El sexto indicador, vacantes publicadas, procede de una consulta independiente coherente con su propia definición y no se filtra por etapa de postulación.

## 5. Filtros

| Filtro | Parámetro | Validación (Form Request) | Afecta a |
|---|---|---|---|
| Desde | `desde` (AAAA-MM-DD) | `date_format:Y-m-d`; por defecto, hoy − 89 días | KPI, gráficos y tabla |
| Hasta | `hasta` (AAAA-MM-DD) | `date_format:Y-m-d`, `after_or_equal:desde`; por defecto, hoy | KPI, gráficos y tabla |
| Vacante | `vacante` | `exists` en `vacancies` **de la misma organización** y no en borrador | KPI (incluidas las vacantes publicadas), gráficos y tabla |
| Etapa actual | `estado` | `Rule::enum(ApplicationStatus)` | KPI de postulaciones, gráficos y tabla |
| Rango máximo | — | Dos años (731 días) | Acota la serie semanal |

Un filtro inválido redirige a `/reportes` sin filtros y muestra el error junto al campo (`$redirectRoute = 'reports.index'`).

## 6. Datos reales, no simulados

- No hay constantes ni arreglos de ejemplo: el frontend solo formatea lo que entrega el servidor.
- Los datos visibles en el entorno local provienen del **`DemoSeeder`**: registros **ficticios de demostración almacenados en PostgreSQL**, creados a través de los servicios reales del dominio (historial, auditoría y notificaciones incluidos). Ver [`docs/demo-users.md`](../../demo-users.md).
- La prueba E2E «refleja al instante una preselección registrada en el sistema» demuestra que el reporte cambia cuando cambia la base de datos: preselecciona una postulación desde la UI y el KPI pasa de 8 a 9.

## 7. Multitenencia

1. **Policy/Gate**: solo personal con organización.
2. **`OrganizationScope`** (global) sobre `Application` y `Vacancy`.
3. **Filtro explícito `organization_id`** en las tres consultas del servicio, incluida la subconsulta del historial: defensa en profundidad si en el futuro se usara `withoutGlobalScopes()`.
4. **Validación del filtro de vacante** acotada a la organización: un id de otra organización se rechaza con un error de validación, sin revelar sus datos.
5. **Opciones del selector** limitadas a las vacantes propias publicadas o cerradas.

Pruebas: `test_rf28_reports_never_include_records_of_another_organization`, `test_rf28_vacancy_of_another_organization_cannot_be_used_as_filter` (PHPUnit) y los escenarios CY-RPT-06/07 de `e2e-20-reports.cy.js`.

## 8. Contratos del proyecto que se preservan

- **Sin datos personales**: las *props* del reporte no contienen nombres, correos, ids de candidatos ni puntajes (`test_rf28_reports_expose_aggregates_only_and_no_personal_data`).
- **Sin decisión automática**: el módulo no selecciona, descarta, ordena ni puntúa personas. Solo cuenta postulaciones por etapa. RF-23 sigue siendo humana, y la página lo recuerda.
- **ML no involucrado**: no consume RF-29 ni genera predicciones.
- **Alcance**: el reporte se centra en el ingreso al proceso y la preselección. Las etapas posteriores (finalista, seleccionado) aparecen solo porque existen en el modelo actual. No se añadieron contratación, planillas ni desempeño.
- **Auditoría**: lectura sin efectos; no escribe en `audit_logs`.

## 9. Pruebas del módulo (resumen)

| Nivel | Archivo | Casos | Resultado |
|---|---|---|---|
| Feature (PHPUnit) | `tests/Feature/Reports/RecruitmentReportTest.php` | 12 (acceso, roles, cálculo, gráficos/tabla, aislamiento, filtro cross-tenant, período, vacante/etapa, validación, opciones, sin PII, organización vacía) | RED observado (12 fallidas, ruta inexistente) → GREEN 12/12 |
| Unidad TS (Vitest) | `resources/js/lib/reports.test.tsx` | 6 | 6/6 |
| E2E (Cypress) | `cypress/e2e/e2e-20-reports.cy.js` | 9 | Ver [`../cypress/RESULTADOS_CYPRESS.md`](../cypress/RESULTADOS_CYPRESS.md) |

## 10. Reauditoría Codex (09/11/2026)

Se revisaron las consultas, la subconsulta correlacionada del historial, las opciones, la Policy y la validación de vacante contra otra organización. La prueba dirigida dio **12/12 y 209 aserciones**; la regresión final completa, **426 aprobadas, 8 omitidas y 0 fallidas (1715 aserciones)**. Vitest conserva **6/6** del módulo; Cypress final, **9/9**. Evidencias actuales en [`../evidencias/codex/`](../evidencias/codex/).

Se corrigieron **solo PHPDoc** de `RecruitmentReportService` (alias del objeto agregado y contratos de colecciones/arrays). El servicio introducía 14 errores PHPStan: quedaron en 0 para ese archivo, y el proyecto volvió a sus 91 errores históricos. **No cambiaron consultas, cálculos, filtros, permisos ni código ejecutable**. RF-28 sigue siendo candidato implementado para la práctica, sin promoción del baseline RF-01–27.
