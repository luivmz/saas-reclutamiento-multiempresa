# Capítulo 5. Planificación y calidad

## 5.1 Alcance

El alcance funcional es la línea base **RF-01 a RF-27** ([capítulo 4](04-requerimientos.md)). Las exclusiones (SuperAdmin, cierre sin selección, RLS, despliegue en la nube, CI/CD, etc.) están en el [capítulo 1](01-informacion-general.md#12-introducción).

## 5.2 Stack tecnológico

Laravel 13 (PHP 8.4), React 19 + TypeScript + Inertia 3 + Tailwind 4, PostgreSQL 17, Redis 7, PHPUnit, Cypress 15, Git y Docker Compose. El detalle y las versiones exactas están en el [capítulo 7](07-arquitectura-tecnologica.md).

Decisión inicial (Fase 0, `docs/implementation-plan.md`):
- toda la cadena de herramientas se ejecuta en Docker;
- no se usan XAMPP ni MySQL, porque el PHP local (8.2) no cumple el requisito de Laravel 13 (PHP ≥ 8.3).

## 5.3 Plan de trabajo por fases

| Fase | Contenido | Estado |
|---|---|---|
| 0 | Inspección del entorno y plan de implementación | Completada |
| 1 | Bootstrap Laravel + React/Inertia + PostgreSQL + Redis en Docker | Completada |
| 2 | Organizaciones, roles, multiempresa y auditoría base | Completada |
| 3 | RF-01 a RF-07 | Completada |
| 4 | RF-08 a RF-15 | Completada |
| 5 | RF-16 a RF-19 | Completada |
| 6 | RF-20 a RF-25 | Completada |
| 7 | RF-26 y RF-27 | Completada |
| 8 | Frontend integral y validación en navegador | Completada |
| 9 | Suite E2E con Cypress | Completada |
| 10 | Docker y portabilidad | Completada |
| 11 | Documentación final | En curso (este documento) |
| 12 | QA final | Pendiente |

La correspondencia con iteraciones y commits está en el [capítulo 8](08-desarrollo.md).

## 5.4 Estándares y buenas prácticas de referencia

**ISO/IEC 25010** se usa como **marco de referencia** para organizar las características de calidad verificadas. El producto no ha sido evaluado ni certificado según la norma.

| Característica ISO/IEC 25010 | Cómo se aborda | Evidencia |
|---|---|---|
| Adecuación funcional | 27 RF implementados y probados | [traceability-master.md](traceability-master.md) |
| Fiabilidad / integridad | Máquinas de estado, transacciones, bloqueo de fila en el cierre, restricciones de base de datos | Migraciones, `ApplicationStatusTest`, `VacancyClosureTest` |
| Seguridad | Autenticación, autorización por Policies, multiempresa, CSRF, validación en servidor, auditoría de solo inserción, protección de endpoints E2E | Sección 5.7 |
| Usabilidad / interacción | Navegación por rol, mensajes, diseño adaptable, validación en navegador | `docs/manual-smoke-test.md` |
| Mantenibilidad | Módulos por dominio, servicios, pruebas de regresión | Capítulos 6, 8 y 11 |
| Portabilidad | Docker Compose con versiones fijadas e instalación limpia validada | [capítulo 10](10-dockerizacion.md) |
| Eficiencia de desempeño | **No evaluada** (sin pruebas de carga ni SLA) | Recomendación (k6) |

**Buenas prácticas aplicadas:**
- TDD;
- pruebas en la misma base de datos que producción (PostgreSQL, no SQLite; A-03);
- datos de prueba ficticios y reproducibles;
- selectores estables `data-cy` en E2E;
- sin reintentos automáticos que oculten inestabilidad;
- registro honesto de defectos;
- commits pequeños por fase con Git Flow simplificado.

## 5.5 Plan de pruebas

| Elemento | Definición aplicada |
|---|---|
| Objetivo | Verificar RF-01 a RF-27, las reglas críticas (decisión humana, aislamiento multiempresa) y la regresión en cada fase |
| Niveles | Unitarias, *feature*/integración HTTP, autorización y acceso entre organizaciones, E2E en navegador, prueba de humo manual y de instalación limpia |
| Herramientas | PHPUnit (Laravel), Cypress 15.3.0 (Electron 136), Docker Compose |
| Entornos | PHPUnit sobre `reclutamiento_testing`; E2E sobre el entorno aislado `app-e2e` con `reclutamiento_e2e`; demostración sobre `reclutamiento` |
| Datos | Fábricas de Laravel en PHPUnit; `DemoSeeder` (ficticio y reproducible) en E2E y demostración |
| Criterio de entrada por RF | Prueba escrita y observada en RED |
| Criterio de salida por fase | Pruebas nuevas en GREEN, suite completa sin fallos, `npm run build` y `tsc` sin errores |
| Criterio de salida E2E | Suite completa en verde en dos corridas (Fase 9) y en instalación limpia más entorno principal (Fase 10) |
| Gestión de defectos | Reproducir → prueba → corregir → registrar en `docs/defects.md` |
| Fuera de alcance | Pruebas de carga, seguridad dinámica (ZAP), accesibilidad automatizada y medición de cobertura |

La estrategia detallada está en el [capítulo 11](11-estrategia-pruebas.md).

## 5.6 TDD

Cada bloque funcional siguió RED → GREEN → REFACTOR, con resultados reales registrados en `docs/tdd-evidence.md`. Ejemplo (Fase 6, RF-23): `FinalDecisionTest` **10 failed** → GREEN **18 passed (123 assertions)** junto con `RankingComparisonTest`.

## 5.7 Seguridad aplicada

| Control | Implementación |
|---|---|
| Autenticación | Laravel Fortify; límite de 5 intentos de inicio de sesión por minuto (correo + IP); contraseñas con bcrypt |
| Autorización | 7 Policies (`JobRequest`, `Vacancy`, `Application`, `Evaluation`, `Interview`, `CandidateDocument`, `AuditLog`) y middleware `role` |
| Multiempresa | *Trait* `BelongsToOrganization` con *scope* global por `organization_id`; las Policies comparan la organización del usuario con la del recurso (`sharesOrganizationWith`) |
| Validación | Form Requests en el servidor; restricciones `CHECK`, `UNIQUE`, FK e índice único parcial en PostgreSQL |
| CSRF | *Middleware* web de Laravel en todas las rutas con sesión |
| Archivos privados | CV en `storage/app/private` con nombre UUID; descarga autorizada por `CandidateDocumentPolicy` |
| Auditoría | `AuditLogger` elimina claves sensibles (`password`, `token`, `secret`, `cookie`, `authorization`, `api_key`, etc.); tabla de solo inserción mediante *trigger* (DEF-07, DEF-08) |
| Soporte E2E | Endpoints `/__e2e/*` inertes salvo `E2E_ENABLED`, nunca en producción, con token y solo sobre `E2E_DATABASE` (DEF-13) |
| Secretos | `.env` y `.env.e2e` fuera de Git y de la imagen Docker; los `.example` no tienen secretos reales |
| Datos | Solo ficticios; sin DNI ni datos sensibles no requeridos (A-15) |

No se afirma cumplimiento legal ni certificación de seguridad: no se ha realizado una evaluación formal.

## 5.8 Riesgos identificados y tratamiento

| Riesgo | Tratamiento | Estado |
|---|---|---|
| Ausencia de BPMN TO-BE y de documentos F4/F5/F6 en el repositorio | Reglas explícitas como supuestos (A-05, A-13, A-16) | Mitigado; anexos pendientes |
| PHP local incompatible con Laravel 13 | Herramientas en Docker | Resuelto |
| Pruebas contra la base de desarrollo | `force="true"` en `phpunit.xml` (DEF-02) y base E2E separada (DEF-13) | Resuelto |
| Fechas UTC en E2E | Fechas en `America/Lima` (DEF-12) | Resuelto |
| Rendimiento no evaluado | Pruebas de carga como recomendación | Abierto |
