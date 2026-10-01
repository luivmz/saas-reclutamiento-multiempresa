# F29G — Defectos y métricas de calidad

> Generado por `docs/academico/tools/f27b/f29g.py`: `python docs/academico/tools/f27b/build.py f29g`. Los defectos se leen de sus registros reales y las métricas se calculan con la evidencia de la F29F y los casos de la F29E. Si un dato no existe, la métrica no se calcula.

## 1. Registro final de defectos

**Fuentes:**

- `docs/defects.md`, para la v1.0 (DEF-01 a DEF-13).
- Los documentos de fase de la v1.1: F21 §16, F25 §26–§27 y F26 §19. Según la convención D-04 de la F26, cada fase registra ahí sus defectos.
- Las observaciones abiertas que confirmó la F29F.

**Qué no hay:** la ejecución F29F no produjo fallos, así que no hay defectos nuevos del software.

**Prioridad:** no se registró en su momento. Se asigna aquí con una regla explícita: severidad Crítica o Alta → Alta, Media → Media y Baja → Baja.

| ID | Descripción | Severidad | Prioridad | Origen | Estado | Versión | Evidencia | Resolución | Prueba de regresión |
|---|---|---|---|---|---|---|---|---|---|
| DEF-01 | El contenedor app quedaba unhealthy: php artisan serve recarga .env en sus procesos hijos, por lo que REDIS_HOST=127.0.0.1 sobrescribía la variable REDIS_HOST=redis de Docker Compose y fallaba la conexión a Redis (sesiones). | Alta | Alta | Healthcheck de Docker Compose (Iteración 1) | Cerrado | v1.0 | docs/defects.md | .env.example usa los hostnames de servicio (postgres, redis); /health se registra fuera del grupo web para no abrir sesión. | Healthcheck de Docker Compose (servicios healthy en cada ejecución; F29F 02-entorno) |
| DEF-02 | 16 pruebas del starter kit fallaban dentro de Docker: env_file: .env inyectaba variables reales (SESSION_DRIVER=redis, DB_DATABASE=reclutamiento) que PHPUnit no sobrescribía, por lo que las pruebas corrían contra la base de desarrollo. | Crítica | Alta | php artisan test (Iteración 1) | Cerrado | v1.0 | docs/defects.md | Se eliminó env_file de docker-compose.yml (Laravel ya lee .env) y se agregó force="true" a las variables de phpunit.xml. Resultado posterior: 31 passed, 8 skipped. | La suite PHPUnit corre sobre `reclutamiento_testing` (`force="true"` en phpunit.xml) |
| DEF-03 | La creación de vacantes fallaba con MassAssignmentException: JobProfile::firstOrNew(['vacancy_id' => …]) asignaba masivamente un atributo protegido. | Alta | Alta | VacancyPublicationTest (Iteración 2) | Cerrado | v1.0 | docs/defects.md | Búsqueda explícita del perfil y asignación directa de vacancy_id/organization_id en VacancyService::saveProfile(). | VacancyPublicationTest |
| DEF-04 | El build de Vite y tsc fallaban: al desactivar la verificación de correo (A-01) Wayfinder dejó de generar @/routes/verification, pero settings/profile.tsx y auth/verify-email.tsx seguían importándolo. | Media | Media | npm run build / npm run types:check (Iteración 2) | Cerrado | v1.0 | docs/defects.md | Se retiró el bloque de verificación del perfil, la página huérfana y la vista de Fortify asociada. | `npm run build` y `tsc --noEmit` (F29F 05-tsc y 06-build) |
| DEF-05 | Las páginas de detalle (requerimiento, vacante, expediente) recibían sus props envueltas en { data: … } porque Laravel envuelve cada JsonResource individual; el frontend leía vacancy.title y habría fallado en tiempo de ejecución. tsc no lo detecta. | Alta | Alta | ApplicationReviewTest::test_rf12_hr_reviews_the_application_file (Iteración 3) | Cerrado | v1.0 | docs/defects.md | JsonResource::withoutWrapping() en AppServiceProvider (las colecciones paginadas conservan data/meta) y aserciones de regresión sobre vacancy.code y application.id. | ApplicationReviewTest |
| DEF-06 | El registro de resultados de evaluación terminaba el proceso PHP («Premature end of PHP process»): RecordScoresRequest declaraba un método session() que sobrescribía Illuminate\Http\Request::session(), usado internamente por Laravel. | Crítica | Alta | EvaluationTest::test_assigned_evaluator_records_evaluation_scores (Iteración 4) | Cerrado | v1.0 | docs/defects.md | Método renombrado a assessmentSession() en la clase base y sus subclases. | EvaluationTest |
| DEF-07 | La inmutabilidad de audit_logs dependía solo de eventos de Eloquent: DB::table('audit_logs')->update() y ->delete() (consultas masivas) modificaban o borraban registros sin error. | Alta | Alta | AuditTrailTest::test_rf27_audit_logs_are_append_only_at_database_level (Iteración 6, RED) | Cerrado | v1.0 | docs/defects.md | Trigger de PostgreSQL audit_logs_append_only que rechaza UPDATE/DELETE, salvo el SET NULL de user_id al eliminar una cuenta (A-34). | AuditTrailTest |
| DEF-08 | La eliminación de datos sensibles en AuditLogger no cubría claves cookie, authorization ni api_key. No se encontraron registros existentes con esos valores (brecha latente, ningún servicio los enviaba). | Media | Media | AuditTrailTest::test_rf27_sensitive_values_are_never_stored_in_metadata (Iteración 6, RED) | Cerrado | v1.0 | docs/defects.md | Patrón ampliado a password\ | AuditTrailTest |
| DEF-09 | Fechas y horas inconsistentes entre pantallas: el frontend formateaba con la zona horaria del navegador, no con APP_TIMEZONE=America/Lima. En un navegador en UTC, la convocatoria de las 10:00 (hora de Lima, correcta en la notificación generada por el… | Media | Media | Validación visual en navegador (Fase 8, captura Cypress en contenedor con TZ UTC) | Cerrado | v1.0 | docs/defects.md | La vista raíz expone <meta name="app-timezone"> y lib/format.ts usa ese timeZone en los Intl.DateTimeFormat; las fechas de calendario (YYYY-MM-DD) se formatean sin desplazamiento. Prueba:… | AppTimezoneTest |
| DEF-10 | El detalle de la auditoría (RF-27) mostraba valores internos: en_evaluacion, con_seleccion, clase_modelo y la fecha programada en ISO-8601 UTC. | Baja | Baja | Validación visual en navegador (Fase 8) | Cerrado | v1.0 | docs/defects.md | AuditLogResource traduce estados, tipo de evaluación, resultado de entrevista y tipo de cierre a sus etiquetas y muestra la fecha programada en hora local (d/m/Y H:i). Los metadatos almacenados no… | AuditLogViewTest |
| DEF-11 | El avatar mostraba iniciales inválidas («C(», «L(») para nombres terminados en un sufijo sin letras, p. ej. «Carmen Rojas (demo)». | Baja | Baja | Validación visual en navegador (Fase 8) | Cerrado | v1.0 | docs/defects.md | useInitials ignora las palabras que no empiezan con una letra. Sin prueba automatizada (Vitest fuera del alcance de la Fase 8); verificado en las capturas posteriores. | Sin prueba automatizada (así consta en docs/defects.md); verificado en capturas |
| DEF-12 | Los specs E2E-04 y E2E-13 calculaban la fecha de inicio y cierre de postulaciones con la fecha UTC del contenedor de Cypress, mientras la aplicación opera en America/Lima. Entre las 19:00 y las 24:00 de Lima la fecha UTC ya es el día siguiente, lo que… | Media | Media | Revisión de la Fase 9 (limitación documentada) | Cerrado | v1.0 | docs/defects.md | Helper cypress/support/dates.js (appDate) con Intl.DateTimeFormat en APP_TIMEZONE; specs actualizados. Prueba: e2e-00-app-dates.cy.js (instante fijo 21:30 Lima = día siguiente en UTC). | e2e-00-app-dates.cy.js |
| DEF-13 | El reset E2E (e2e:reset, POST /__e2e/reset) ejecutaba migrate:fresh --seed sobre la base de desarrollo/demostración reclutamiento: la suite borraba los datos del entorno normal. | Alta | Alta | Revisión de la Fase 9 (limitación documentada) | Cerrado | v1.0 | docs/defects.md | Entorno E2E aislado (app-e2e/queue-e2e, APP_ENV=e2e, .env.e2e, base reclutamiento_e2e, Redis DB 2/3). E2E_ENABLED=false en el entorno normal. El reset se rechaza (409 / comando fallido / excepción… | E2eEnvironmentTest, E2eSupportTest |
| F21-A4 | Alertas destructivas en claro: rechazo de requerimiento (RF-04), error de flujo, error de ranking, AlertError: La Fase 18 cambió --destructive-foreground a casi blanco —el color que va *sobre* el relleno rojo— y la variante de alerta lo usaba como color de… | Alta | Alta | QA visual y accesibilidad (Fase 21) | Cerrado | v1.1 | docs/v1.1/phase-21-visual-qa.md §16 | ui/alert.tsx: texto con --tone-danger-foreground (7.25:1 en claro), el tono de peligro para texto; el motivo ya no se atenúa al 80 % | resources/js/components/visual-qa.test.tsx, cypress/e2e/e2e-19-qa-visual-accesible.cy.js |
| F21-A2 | Botón destructivo, oscuro: --destructive con L = 0.612: blanco encima a 4.14:1 | Media | Media | QA visual y accesibilidad (Fase 21) | Cerrado | v1.1 | docs/v1.1/phase-21-visual-qa.md §16 | app.css: L = 0.56 → 5.13:1; el borde inválido queda en 3.27:1 | cypress/e2e/e2e-19-qa-visual-accesible.cy.js |
| F21-A3 | Error de campo, oscuro: Rojo de relleno usado como texto: 4.06:1 | Media | Media | QA visual y accesibilidad (Fase 21) | Cerrado | v1.1 | docs/v1.1/phase-21-visual-qa.md §16 | input-error.tsx: text-tone-danger-foreground → 9.65:1 | resources/js/components/visual-qa.test.tsx, cypress/e2e/e2e-19-qa-visual-accesible.cy.js |
| F21-A1 | Inicio de sesión, registro, recuperar y restablecer contraseña, confirmar contraseña: El diseño de acceso no tenía main: un lector de pantalla no tenía a dónde saltar | Media | Media | QA visual y accesibilidad (Fase 21) | Cerrado | v1.1 | docs/v1.1/phase-21-visual-qa.md §16 | auth-simple-layout.tsx: la columna del formulario es main | resources/js/components/visual-qa.test.tsx, cypress/e2e/e2e-19-qa-visual-accesible.cy.js |
| F21-V1 | Cabecera pública a 320 px: Fila única de altura fija: +47 px de desborde (WCAG 1.4.10) | Media | Media | QA visual y accesibilidad (Fase 21) | Cerrado | v1.1 | docs/v1.1/phase-21-visual-qa.md §16 | public-layout.tsx: flex-wrap y min-h-16 | cypress/e2e/e2e-19-qa-visual-accesible.cy.js |
| F21-F19-R | Códigos de recuperación plegados: Relleno fuera del elemento recortado de la fila 0fr: franja de 12 px visible | Media | Media | QA visual y accesibilidad (Fase 21) | Cerrado | v1.1 | docs/v1.1/phase-21-visual-qa.md §16 | two-factor-recovery-codes.tsx: relleno dentro de min-h-0 | resources/js/components/visual-qa.test.tsx |
| F21-V2 | Enlace de salto enfocado: not-sr-only anulaba el relleno: 22 px de alto | Baja | Baja | QA visual y accesibilidad (Fase 21) | Cerrado | v1.1 | docs/v1.1/phase-21-visual-qa.md §16 | skip-link.tsx: focus:px-4 focus:py-2 | resources/js/components/visual-qa.test.tsx, cypress/e2e/e2e-19-qa-visual-accesible.cy.js |
| F21-V3 | Botones de 2FA a 1024 px: Fila sin salto de línea en columna angosta | Baja | Baja | QA visual y accesibilidad (Fase 21) | Cerrado | v1.1 | docs/v1.1/phase-21-visual-qa.md §16 | two-factor-recovery-codes.tsx: sm:flex-wrap | — |
| F21-M1 | Desplazamiento a los códigos: behavior: 'smooth' explícito ignoraba el movimiento reducido | Baja | Baja | QA visual y accesibilidad (Fase 21) | Cerrado | v1.1 | docs/v1.1/phase-21-visual-qa.md §16 | lib/motion.ts + uso en el componente | resources/js/components/visual-qa.test.tsx |
| F25-M01 | Rutas / robustez: GET /requerimientos/create (o /vacantes/abc, /postulaciones/x…) como RR. HH. → 500; log: SQLSTATE[22P02] invalid input syntax for type bigint: "create" | Media | Media | QA global de release (Fase 25) | Cerrado | v1.1 | docs/v1.1/phase-25-final-qa.md §26–§27 | app/Providers/AppServiceProvider.php (Route::patterns numéricos para application, document, evaluation, interview, jobRequest, vacancy) | NumericRouteParametersTest |
| F25-M02 | UI móvil / WCAG 1.4.10: A 375 px, auditoría y «Mis evaluaciones»: la ficha llega a 419 px de ancho en un viewport de 376 y el texto se corta | Media | Media | QA global de release (Fase 25) | Cerrado | v1.1 | docs/v1.1/phase-25-final-qa.md §26–§27 | resources/js/components/data-table.tsx (block md:table), status-badge.tsx (parte línea solo en móvil), pages/assessments/index.tsx (md:whitespace-nowrap), cypress/e2e/e2e-16-… (fichas dentro del… | e2e-16-tabla-accesible-movil.cy.js |
| F25-L01 | Documentación del contrato ML: Descripción OpenAPI de days_remaining_to_target, *docstring* de serving, línea de la CLI, comentario de schema.py y README: «GAP-01 abierto», puerto 8001 | Baja | Baja | QA global de release (Fase 25) | Cerrado | v1.1 | docs/v1.1/phase-25-final-qa.md §26–§27 | ml-service/src/recruitment_ml/api/schemas.py, schema.py, serving/__init__.py, serving/build_artifact.py, ml-service/README.md, pruebas en test_api_service.py y test_serving_cli.py | test_api_service.py, test_serving_cli.py |
| F25-L02 | Documentación de pruebas: docs/testing/cypress-e2e.md en «14 specs y 43 tests» | Baja | Baja | QA global de release (Fase 25) | Cerrado | v1.1 | docs/v1.1/phase-25-final-qa.md §26–§27 | docs/testing/cypress-e2e.md (§9 nueva) | Documental |
| F25-L03 | Estilo: pint --test: 8 archivos; vp check: 154 archivos con formato pendiente | Baja | Baja | QA global de release (Fase 25) | Abierto (remedido en la F29F: OBS-F29F-05) | v1.1 | docs/v1.1/phase-25-final-qa.md §26–§27; qa-final/evidencias/11-pint.log y 12-vp-check.log | Pendiente: aplicar `pint` y `vp check --fix` en un commit propio | — |
| F26-M01 | El manifiesto y §15 presentaban f945b8d123f419d7e038962a8a92c99008e950e0 como el árbol que tendría main tras el release. Ese hash es el árbol del baseline pre-F26, y cualquier cambio documental posterior lo vuelve obsoleto | Media | Media | Auditoría del release (Fase 26) | Cerrado | v1.1 (documentación) | docs/v1.1/phase-26-release-closeout.md §19 | f945b8d… queda identificado solo como «árbol del baseline develop pre-F26». No se fija ningún hash de «árbol final»: la integridad se verifica en el cierre con develop^{tree} == main^{tree} (Bash… | — (documental) |
| F26-M02 | La secuencia proponía crear la etiqueta y publicar, y después comprobar el CI de main | Media | Media | Auditoría del release (Fase 26) | Cerrado | v1.1 (documentación) | docs/v1.1/phase-26-release-closeout.md §19 | Secuencia de 12 pasos (§15): CI de develop en verde, merge a main, CI de main en verde, igualdad de árboles, y solo entonces la etiqueta sobre el merge verificado de main, su *push* y el release | — (documental) |
| F26-M02-R1 | La §15 conservaba, para la opción A, la frase «la etiqueta se pone sobre el merge de F26 en develop», que contradecía la estrategia final | Media | Media | Auditoría del release (Fase 26) | Cerrado | v1.1 (documentación) | docs/v1.1/phase-26-release-closeout.md §19 | Se eliminó la frase. La opción A queda marcada como descartada para v1.1, solo como antecedente y sin pasos ejecutables. La opción B es la única estrategia activa, y el único destino de la… | — (documental) |
| OBS-F29F-04 | El merge F29C en main (60ebcb2) no generó ejecución de GitHub Actions | Baja | Media | Ejecución QA final (F29F) | Abierto: CI main F29C pendiente de ejecución manual | v1.1 (proceso) | docs/academico/qa-final/evidencias/ci-github-actions.json | Ejecutar el workflow `tests` en main (workflow_dispatch) y verificar success | — (proceso) |

*Las descripciones y resoluciones largas se abrevian; el texto completo está en la evidencia citada.*

## 2. Métricas de ejecución (F29F)

**Tasa de aprobación** = aprobadas / (ejecutadas − omitidas). Las omitidas no son fallos: dependen de una función desactivada (OBS-F29F-03).

| Suite | Ejecutadas | Aprobadas | Fallidas | Omitidas | Tasa de aprobación |
|---|---|---|---|---|---|
| PHPUnit | 419 | 411 | 0 | 8 | 100,0 % |
| Cypress | 85 | 85 | 0 | 0 | 100,0 % |
| Vitest | 42 | 42 | 0 | 0 | 100,0 % |
| pytest | 533 | 533 | 0 | 0 | 100,0 % |
| **Total** | **1079** | **1071** | **0** | **8** | **100,0 %** |

Verificaciones estáticas: TypeScript sin errores; build con 2375 módulos; configuración de Compose válida; CI en verde en `develop`. La CI de `main` no se ejecutó (OBS-F29F-04).

## 3. Casos de prueba (F29E)

| Automatización | CP |
|---|---|
| AUTOMATIZADA | 124 |
| MANUAL / NO AUTOMATIZADO | 4 |

| Tipo de prueba | CP |
|---|---|
| Aceptación (flujo completo) | 1 |
| Aceptación (manual) | 2 |
| Estática / build | 3 |
| Integración / funcional | 42 |
| ML experimental | 28 |
| Multitenencia | 4 |
| No funcional | 2 |
| Regresión | 4 |
| Regresión / CI | 1 |
| Seguridad básica | 15 |
| UI / E2E | 10 |
| UI / E2E (accesibilidad) | 4 |
| UI / componentes | 6 |
| Unitaria | 6 |

| Prioridad | CP |
|---|---|
| Alta | 40 |
| Baja | 11 |
| Media | 77 |

| Estado (F29F) | CP |
|---|---|
| APROBADO | 122 |
| EJECUTADO EN LA FASE 8 | 1 |
| NO EJECUTADO | 3 |
| OMITIDO | 2 |

Automatizados frente a manuales: 124 de 128 CP (96,9 %) son automatizados.

## 4. Cobertura funcional (no es cobertura de código)

| Métrica | Valor | Cálculo |
|---|---|---|
| RF de la línea base con al menos un CP automatizado aprobado | 27 de 27 (100,0 %) | Matriz RF → CP de la F29E |
| CU cubiertos a través de sus RF | 20 de 20 (100,0 %) | Tabla CU ↔ RF del Formato 08 |
| RNF académicos por estado (F7) | 3 EVIDENCIA PARCIAL, 2 NO VERIFICADO, 5 VERIFICADO | docs/academico/practica-07 |
| Cobertura de código (líneas o ramas) | **NO MEDIDA** | Sin Xdebug ni PCOV en el contenedor; nunca se midió |

## 5. Defectos

| Versión | Crítica | Alta | Media | Baja | Total |
|---|---|---|---|---|---|
| v1.0 | 2 | 5 | 4 | 2 | 13 |
| v1.1 | 0 | 1 | 10 | 7 | 18 |
| **Total** | 2 | 6 | 14 | 9 | **31** |

| Tipo | Registros |
|---|---|
| Documentación | 2 |
| Documentación / proceso | 3 |
| Estilo | 1 |
| Proceso / CI | 1 |
| Software | 24 |

**Cerrados:** 29 de 31 (93,5 %).

**Abiertos:** 2, ninguno del software funcional:
- F25-L03 (Baja): Abierto (remedido en la F29F: OBS-F29F-05).
- OBS-F29F-04 (Baja): Abierto: CI main F29C pendiente de ejecución manual.

**Defectos de severidad Crítica o Alta abiertos:** 0.

**Métricas que no se calculan, por falta de datos:**

- densidad de defectos por KLOC: no se midió el tamaño;
- tiempo medio de corrección: no se registró la fecha de apertura y cierre de cada defecto;
- defectos escapados a producción: no hay producción.

## 6. Estabilidad y regresión

| Suite | F25 (release v1.1, tras los arreglos) | F29F, 1.ª ejecución | F29F, 2.ª ejecución | Resultado |
|---|---|---|---|---|
| PHPUnit (aprobadas / omitidas / aserciones) | 411 / 8 / 1498 | 411 / 8 / 1498 | 411 / 8 / 1498 | Idéntico |
| pytest (aprobadas) | 533 | — (sin resumen) | 533 | Idéntico |
| Vitest (aprobadas) | 42 | 42 | — | Idéntico |
| Cypress (aprobadas / total) | 85/85 | 85/85 | — | Idéntico |

**Interpretación:**

- Sin fallos intermitentes: no hubo reintentos (Cypress `retries: 0`) y PHPUnit dio el mismo resultado en sus dos ejecuciones.
- Sin regresiones frente a la QA de release de la F25.

## 7. Evaluación de calidad con ISO/IEC 25010 (marco de referencia)

> ISO/IEC 25010 organiza la evaluación; **no se declara certificación ni conformidad con la norma**. El estado de cada RNF es el del Formato 07.

| Característica | RNF | Estado | Evidencia del F7 |
|---|---|---|---|
| Seguridad | RNF-01 Seguridad y control de acceso | VERIFICADO | QA de la F25: PHPUnit 411 superadas y 0 fallidas; Cypress 85/85 (docs/v1.1/phase-25-final-qa.md). |
| Seguridad | RNF-02 Multitenencia y aislamiento | VERIFICADO | F25: sin fugas entre organizaciones y 22 pruebas cross-tenant explícitas (phase-25-final-qa.md §14). |
| Seguridad (responsabilidad) | RNF-03 Trazabilidad y auditoría | VERIFICADO | DEF-07 y DEF-08 corregidos y cubiertos por pruebas (docs/defects.md). |
| Seguridad (confidencialidad) | RNF-04 Privacidad | VERIFICADO | Solo datos ficticios en el repositorio; barrido de secretos y PII en la F25 y la F26. |
| Usabilidad | RNF-05 Usabilidad | EVIDENCIA PARCIAL | No hay pruebas de usabilidad con usuarios reales, y la prueba con un lector de pantalla real está pendiente. La accesibilidad WCAG 2.1 AA como requisito es el candidato RNF-A (propuesta). |
| Eficiencia de desempeño | RNF-06 Rendimiento | NO VERIFICADO | Solo hay medición exploratoria de la F25 en un equipo potente: no es un benchmark ni un SLA. No se ejecutaron pruebas de carga. El presupuesto de rendimiento es el candidato RNF-B (propuesta). |
| Fiabilidad | RNF-07 Disponibilidad y recuperabilidad | NO VERIFICADO | Hay controles de integridad (transacciones, notificaciones tras el commit, restricciones de la base) y healthchecks de Docker Compose, pero no pruebas de respaldo o restauración ni objetivos de disponibilidad. |
| Compatibilidad | RNF-08 Compatibilidad | EVIDENCIA PARCIAL | Cypress se ejecuta en Electron (motor Chromium), con anchos de 320 a 1440 px. Firefox y Safari no se probaron de forma sistemática. |
| Mantenibilidad | RNF-09 Mantenibilidad | EVIDENCIA PARCIAL | La estructura y las suites están verificadas (F25: 411 PHPUnit, 42 Vitest, tsc sin errores). No se midieron métricas de mantenibilidad (complejidad, cobertura) y hay deuda de formato aceptada (Pint, vp check). |
| Seguridad (integridad) | RNF-10 Integridad de datos | VERIFICADO | F25-M01 corregido (500 → 404) con prueba de regresión. |

**Características sin evidencia suficiente:**

- **Eficiencia de desempeño (RNF-06):** sin pruebas de carga.
- **Fiabilidad y disponibilidad (RNF-07):** sin entorno de producción.
- **Usabilidad, compatibilidad y mantenibilidad (RNF-05, RNF-08 y RNF-09):** evidencia parcial. En mantenibilidad, el formato pendiente se registra como F25-L03.
