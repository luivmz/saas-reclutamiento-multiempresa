# Índice de evidencias

Estado de cada evidencia:
- **Repositorio:** versionada en Git.
- **Local:** existe en el equipo de desarrollo pero no está versionada.
- **Externa:** fuera del repositorio.
- **Pendiente:** no existe todavía.

| Categoría | Evidencia | Ruta | Estado |
|---|---|---|---|
| Análisis | Problemas P1 a P5 y objetivos | `docs/final-report/02-contexto-problema.md` | Repositorio |
| Análisis | Documento previo de identificación de problemas (F4) | — | Pendiente (no se encontró en el repositorio ni en la carpeta del curso) |
| Análisis | Inspección inicial y decisiones de entorno | `docs/implementation-plan.md` | Repositorio |
| BPMN | AS-IS | — | Pendiente |
| BPMN | TO-BE (BPMN formal) | — | Pendiente; flujo derivado de la implementación en `docs/final-report/03-procesos-negocio.md` |
| Requerimientos | Línea base RF-01 a RF-27, actores, RNF y casos de uso | `docs/final-report/04-requerimientos.md` | Repositorio |
| Requerimientos | Matriz de implementación por fase | `docs/rf-implementation-matrix.md` | Repositorio |
| Requerimientos | Matriz maestra de trazabilidad | `docs/final-report/traceability-master.md` | Repositorio |
| Requerimientos | Supuestos A-01 a A-36 | `docs/assumptions.md` | Repositorio |
| Arquitectura | Diseño, clases, estados, secuencias, UI y ERD | `docs/final-report/06-diseno-sistema.md` | Repositorio |
| Arquitectura | Stack y arquitectura tecnológica | `docs/final-report/07-arquitectura-tecnologica.md` | Repositorio |
| Arquitectura | Diagramas UML PowerDesigner (postulación, evaluación, selección, despliegue) | `Diagramas/PD/*.oom` (carpeta del curso) | Externa |
| Código | Backend (controladores, servicios, Policies, modelos, *enums*, notificaciones) | `app/` | Repositorio |
| Código | Esquema de base de datos | `database/migrations/` (17) | Repositorio |
| Código | Datos demo ficticios | `database/seeders/DemoSeeder.php`, `docs/demo-users.md` | Repositorio |
| Código | Frontend | `resources/js/` | Repositorio |
| Git | Estrategia de ramas, commits y merges | `docs/final-report/09-control-versiones.md` | Repositorio |
| Git | Historial | `git log --oneline --graph --decorate --all` | Repositorio |
| PHPUnit | Pruebas | `tests/Unit/`, `tests/Feature/` | Repositorio |
| PHPUnit | Evidencia TDD (RED → GREEN) por fase | `docs/tdd-evidence.md` | Repositorio |
| PHPUnit | Configuración de pruebas | `phpunit.xml` | Repositorio |
| Cypress | Specs, soporte y *fixtures* | `cypress/`, `cypress.config.cjs` | Repositorio |
| Cypress | Documentación y resultados reales | `docs/testing/cypress-e2e.md` | Repositorio |
| Cypress | Logs de las corridas | `cypress/results/*.log` | Local (ignorado por Git) |
| Validación manual | Prueba de humo en navegador (Fase 8) | `docs/manual-smoke-test.md` | Repositorio |
| Validación manual | Capturas del recorrido visual y del flujo | `storage/app/smoke/screenshots*/` | Local (ignorado por Git) |
| Docker | Configuración | `docker-compose.yml`, `docker/`, `.env.example`, `.env.e2e.example`, `.dockerignore` | Repositorio |
| Docker | Guía y validación de instalación limpia | `docs/docker.md`, `docs/final-report/10-dockerizacion.md` | Repositorio |
| Defectos | Registro DEF-01 a DEF-13 | `docs/defects.md` | Repositorio |
| Métricas | Métricas de calidad | `docs/final-report/13-metricas-calidad.md` | Repositorio |
| Progreso | Estado por fase | `docs/PROGRESS.md` | Repositorio |
| Presentación | Resumen técnico y guion de demostración | `docs/final-report/technical-summary.md`, `docs/final-report/demo-script.md` | Repositorio |

## Evidencias pendientes antes de la entrega

1. BPMN AS-IS y TO-BE (anexos A y B).
2. Documentos previos de análisis (identificación de problemas, requerimientos y casos de uso) para contrastarlos con el catálogo derivado.
3. Selección de capturas de pantalla para el informe. Las capturas locales pueden regenerarse con el entorno demo; se recomienda copiar solo las necesarias.
4. Actualización o nota aclaratoria de los diagramas UML de selección y despliegue (capítulo 6).
