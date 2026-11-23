# Matriz de requisitos de la guía

Convierte la *Guía Práctica INDIVIDUAL de Arquitectura* (secciones III, IV, V y VII) en una checklist trazable. «Estado inicial» es lo encontrado al empezar (09/11/2026, `41a830c`); «Estado final» es lo verificado al terminar en el working tree, sin commit.

Leyenda: **C** = cumple · **P** = parcial · **N** = no existía · **N/A** = no aplica, con justificación.

**Recuento independiente Codex: 59 IDs únicos**, no 52: 5 generales + 10 arquitectura SW + 9 tecnológica + 11 Cypress + 8 Sonar + 8 Reportes + 7 Impacto + 1 Informe. Estado recibido: 56 completos y 3 parciales. Tras incorporar capturas reales de IDE y Sonar: **59 completos, 0 parciales, 0 pendientes**. Se evalúa la entrega fuente Markdown solicitada; DOCX/PDF y nota docente siguen fuera de este cierre.

## Indicaciones generales (III) y consideraciones (VII)

| ID | Actividad | Requisito | Estado inicial | Artefacto existente | Trabajo requerido | Evidencia final | Estado final |
|---|---|---|---|---|---|---|---|
| GEN-01 | General | Trabajar sobre el proyecto propio, sin crear uno nuevo | C | Repositorio SaaS | Ninguno; todo se hace sobre el repositorio existente | `git status` final (solo agregados y cambios acotados) | C |
| GEN-02 | General | Documentar decisiones arquitectónicas y tecnológicas | P | Informe v1.0/v1.1, diagramas 01–16 | Documentos de esta práctica | `arquitectura/*.md` | C |
| GEN-03 | General | APIs solo si responden a una necesidad real | C | `MlRiskClient` (RF-29, opcional) | Justificar uso y ausencia | `ARQUITECTURA_SOFTWARE.md` §10 | C |
| GEN-04 | General | Evidencias verificables | P | Evidencias Sonar V1, diagramas | Logs, JSON y capturas nuevas | `evidencias/EVIDENCIAS_MANIFEST.md` | C |
| GEN-05 | VII | Diagramas de la implementación real, no teóricos | C | 01, 02, 06, 11, 16 derivados del código | Diagrama 17 derivado del código nuevo | `arquitectura/DIAGRAMAS_REFERENCIA.md` | C |

## Actividad 1: arquitectura de software

| ID | Actividad | Requisito | Estado inicial | Artefacto existente | Trabajo requerido | Evidencia final | Estado final |
|---|---|---|---|---|---|---|---|
| ARQ-SW-01 | 1.1 | Tipo de arquitectura | P | Diagrama 01 («monolito modular») | Verificar en el código y describir | `ARQUITECTURA_SOFTWARE.md` §1 | C |
| ARQ-SW-02 | 1.1 | Capas o componentes principales | P | `laravel-saas-quality` | Tabla de capas con archivos reales | §2 | C |
| ARQ-SW-03 | 1.1 | Módulos funcionales y responsabilidades | P | Diagrama 06, matriz RF | Tabla de módulos, controladores, servicios y roles | §3 | C |
| ARQ-SW-04 | 1.1 | Comunicación entre componentes | P | Diagrama 01 | Flujo UI → backend → BD paso a paso | §4 | C |
| ARQ-SW-05 | 1.1 | Gestión e interacción con la BD | P | Migraciones | Tablas, bases por entorno, multitenencia | §5 y §9 | C |
| ARQ-SW-06 | 1.1 | Integración con APIs externas, cuando corresponda | P | RF-29 documentado | Tabla de APIs y justificación de la ausencia de terceros | §10 | C |
| ARQ-SW-07 | 1.2 | Diagrama: UI, backend, BD, módulos, APIs y comunicación | P | 01 y 06 (el 06 excluye reportes) | Reutilizar 01/06 y agregar el 17 del módulo nuevo | `DIAGRAMAS_REFERENCIA.md`, `diagramas/17_*.drawio/.svg/.png` | C |
| ARQ-SW-08 | 1.2 | Tabla de APIs: funcionalidad, información, justificación | N | — | Tabla real | §10 | C |
| ARQ-SW-09 | 1.2 | Si no hay APIs externas, explicar la comunicación interna | N | — | Explicación | §10 | C |
| ARQ-SW-10 | Evid. | Funcionamiento de las integraciones, cuando corresponda | P | Pruebas `tests/Feature/Ml` con `Http::fake()` | Indicar el estado (ML desactivado) y las pruebas existentes | §10; PHPUnit completo verde | C (servicio desactivado, probado con dobles) |

## Actividad 2: arquitectura tecnológica

| ID | Actividad | Requisito | Estado inicial | Artefacto existente | Trabajo requerido | Evidencia final | Estado final |
|---|---|---|---|---|---|---|---|
| ARQ-TECH-01 | 2.1 | Tabla: frontend, backend, BD, framework, entorno, control de versiones, infraestructura, Cypress y SonarQube | P | Versiones dispersas en informes | Medir versiones con comandos | `ARQUITECTURA_TECNOLOGICA.md` §1; `evidencias/tecnologia/versiones-entorno.log` | C |
| ARQ-TECH-02 | 2.1 | Propósito y justificación de cada tecnología | P | — | Columnas de propósito y justificación | §1 | C |
| ARQ-TECH-03 | 2.2 | Diagrama tecnológico (herramientas, front/back, SGBD, servidores, control de versiones, automatización y calidad) | C | 02, 11, 16, 01 | Reutilizar y explicar su vigencia | `DIAGRAMAS_REFERENCIA.md` | C |
| ARQ-TECH-04 | 2.3 | Entorno de desarrollo | P | `docs/docker.md` | Describir host, contenedores y herramientas | §3.1 | C (VS Code verificado en captura real) |
| ARQ-TECH-05 | 2.3 | Herramientas de gestión del código | C | Diagrama 16 | Resumen | §3.2 | C |
| ARQ-TECH-06 | 2.3 | Procedimiento para ejecutar la aplicación | C | `CLAUDE.md`, `docs/docker.md` | Pasos verificados | §3.3; `/health` OK en el log | C |
| ARQ-TECH-07 | 2.3 | Infraestructura donde se despliega | C | Compose | Tabla de servicios; declarar que no hay despliegue productivo | §3.4 | C |
| ARQ-TECH-08 | 2.3 | Procedimiento para actualizar o publicar versiones | P | CI `tests.yml` | Flujo rama → regresión → PR → CI → integración | §3.5 | C |
| ARQ-TECH-09 | Evid. | Capturas del entorno de desarrollo y del software en ejecución | P | — | Capturas de la app y del IDE real | `evidencias/arquitectura/ARQ-TECH-09_IDE_VSCode.jpg`, `evidencias/reportes/*.png`, `versiones-entorno.log` | C |

## Actividad 3: Cypress

| ID | Actividad | Requisito | Estado inicial | Artefacto existente | Trabajo requerido | Evidencia final | Estado final |
|---|---|---|---|---|---|---|---|
| CYP-01 | 3.1 | Instalar Cypress | C | Imagen `cypress/included:15.3.0` | Verificar, sin reinstalar | `ESCENARIOS_CYPRESS.md` §1; `cypress verify` en el log | C |
| CYP-02 | 3.1 | Configurar el entorno de pruebas | C | `cypress.config.cjs`, perfil `e2e` | Documentar | §1 | C |
| CYP-03 | 3.1 | Dirección de la aplicación evaluada | C | `baseUrl` | Documentar | §1 | C |
| CYP-04 | 3.1 | Organizar archivos y escenarios | C | `cypress/e2e`, `support`, `fixtures` | Agregar `e2e-20-reports.cy.js` | spec nuevo | C |
| CYP-05 | 3.1 | Verificar que Cypress ejecuta sobre el software | P | Ejecución histórica 85/85 no repetida desde el 20/10 | Ejecutar la suite completa | `RESULTADOS_CYPRESS.md` | C |
| CYP-06 | 3.2 | Escenarios: acceso, registro, edición, eliminación, validación, navegación y procesos principales | C | 20 specs | Mapear; justificar que la eliminación no aplica | `ESCENARIOS_CYPRESS.md` §2 | C (eliminación N/A por diseño) |
| CYP-07 | 3.3 | Mínimo 5 escenarios | C | 20 specs | 11 grupos documentados (+9 de reportes) | §2 | C |
| CYP-08 | 3.3 | Ficha por escenario: ID, funcionalidad, objetivo, datos, procedimiento, esperado, obtenido, estado | N | — | Fichas completas | §2 y §3 | C |
| CYP-09 | 3.4 | Total, aprobadas, fallidas, porcentaje | N | — | Dos ejecuciones completas reales | `RESULTADOS_CYPRESS.md` §2 | C |
| CYP-10 | 3.4 | Evidencias de ejecución | N | — | Logs y capturas | `evidencias/cypress/` | C |
| CYP-11 | 3.4 | Errores encontrados y funcionalidades con problemas | N | — | Análisis de las fallas de la ejecución 1 | `RESULTADOS_CYPRESS.md` §3; DEF-14 y DEF-15 en `docs/defects.md` | C |

## Actividad 4: SonarQube

| ID | Actividad | Requisito | Estado inicial | Artefacto existente | Trabajo requerido | Evidencia final | Estado final |
|---|---|---|---|---|---|---|---|
| SONAR-01 | 4.1 | Configurar SonarQube | C | Contenedor `sonarqube`, `sonar-project.properties` | Verificar sin reconfigurar | `RESULTADOS_SONARQUBE.md` §1 | C |
| SONAR-02 | 4.1 | Registrar el proyecto | C | Key `saas-reclutamiento-multiempresa` | Ninguno | §1 | C |
| SONAR-03 | 4.1 | Parámetros de análisis | C | `sonar-project.properties` | Ninguno (sin cambios) | §1 | C |
| SONAR-04 | 4.1 | Ejecutar el análisis | P | V1/V2 del 20/10 | Análisis V3 del working tree | §2; `evidencias/sonarqube/` | C |
| SONAR-05 | 4.1 | Resultados disponibles en el panel | P | Capturas V1 | Verificación independiente API y UI con sesión ya abierta | `evidencias/codex/sonar-final.json`; `evidencias/sonarqube/SONAR-UI-01_Proyecto.jpg` a `SONAR-UI-07_Limitaciones_Seguridad.jpg` | C |
| SONAR-06 | 4.2 | Métricas: Gate, Bugs, Vulnerabilities, Code Smells, Coverage, Duplicated Lines | P | V1/V2 | Métricas V3 | §3 | C |
| SONAR-07 | 4.3 | Preguntas de interpretación y propuestas de mejora | P | Informes V1/V2 | Interpretación V3 y comparación | §4–§7 | C |
| SONAR-08 | Evid. | Capturas del proyecto y del Quality Gate | P | V1 (30 capturas); V2 pendiente | Capturar V3 real, sin secretos | `evidencias/sonarqube/SONAR-UI-01_Proyecto.jpg`, `SONAR-UI-02_Quality_Gate.jpg` | C |

## Actividad 5: reportes e impacto

| ID | Actividad | Requisito | Estado inicial | Artefacto existente | Trabajo requerido | Evidencia final | Estado final |
|---|---|---|---|---|---|---|---|
| REP-01 | 5.1 | Indicadores ligados al problema | N | RF-28 candidato; límite P5 del informe v1.0 | Seleccionar indicadores compatibles con el modelo | `MODULO_REPORTES.md` §3; `IMPACTO_FUNCIONAL.md` §3 | C |
| REP-02 | 5.2 | Módulo dentro del software | N | — | Ruta, Policy, Request, Service, página y menú | `MODULO_REPORTES.md` §1–2 | C |
| REP-03 | 5.2 | Indicadores principales (al menos 3) | N | — | 6 KPI | §3 | C |
| REP-04 | 5.2 | Reportes estadísticos (tablas o gráficos) | N | — | 2 gráficos y 1 tabla | §4 | C |
| REP-05 | 5.2 | Filtros por fechas, categorías o estados | N | — | Desde, Hasta, Vacante y Etapa, validados | §5 | C |
| REP-06 | 5.2 | Información actualizada desde los registros | N | — | Consultas a PostgreSQL; prueba E2E de datos vivos | §6; CY-RPT-05 | C |
| REP-07 | 5.2 | No valores estáticos ni ficticios desconectados | N | — | Sin constantes; seeders identificados como demo en BD | §6 | C |
| REP-08 | Extra | Aislamiento multiempresa del módulo | N | Scope global | Defensa en profundidad y pruebas cross-tenant | §7; PHPUnit y Cypress | C |
| IMP-01 | 5.3 | Problema que soluciona | P | Informe v1.0 §2 | Síntesis | `IMPACTO_FUNCIONAL.md` §1 | C |
| IMP-02 | 5.3 | Información que muestra el módulo | N | — | Descripción | §2 | C |
| IMP-03 | 5.3 | Indicadores para evaluar el proceso | N | — | Tabla indicador → problema | §3 | C |
| IMP-04 | 5.3 | Apoyo a la toma de decisiones | N | — | Descripción por rol | §4 | C |
| IMP-05 | 5.3 | Actividades optimizables | N | AS-IS F2 | Mapeo a observaciones O-02/O-05 | §5 | C |
| IMP-06 | 5.3 | Beneficios esperados | N | — | Beneficios potenciales con método de medición | §8 | C |
| IMP-07 | 5.3 | Antes/después, o diferenciar potencial de medido | N | — | Medidos frente a potenciales; sin cifras inventadas | §6–§8 | C |

## Informe final (V)

| ID | Actividad | Requisito | Estado inicial | Artefacto existente | Trabajo requerido | Evidencia final | Estado final |
|---|---|---|---|---|---|---|---|
| INF-01 | V | Portada, descripción, arquitectura SW y tecnológica, Cypress, SonarQube, reportes, impacto, conclusiones y anexos (10 secciones) | N | — | Redactar | `final-report/INFORME_TECNICO_INDIVIDUAL.md` | C (borrador fuente Markdown; DOCX/PDF a generar tras la auditoría) |
