# Capítulo 1. Información general

## Datos del proyecto

| Campo | Valor |
|---|---|
| Proyecto | Análisis y Diseño de una Plataforma SaaS Multiempresa para la Gestión del Reclutamiento, Evaluación y Selección de Personal – Caso de estudio: Colegio Andino de Huancayo |
| Universidad | Universidad Continental |
| Facultad | Facultad de Ingeniería |
| Escuela | Ingeniería de Sistemas e Informática |
| Curso | Pruebas y Calidad de Software |
| NRC | 28607 |
| Docente | Dr. Maglioni Arana Caparachin |
| Integrantes | Coronacion Meza Fredy · Peña Arroyo Anthony · Vila Meza Luis Antonio |
| Repositorio | Git local (ramas `main`, `develop` y `feature/*`); sin repositorio remoto a la fecha de este documento |
| Estado del documento | Fase 11 (documentación final), 2026-09-13 |

### Convención de niveles de información

En todo el informe se distinguen cuatro niveles. Ninguna propuesta del proyecto se presenta como hecho institucional.

| Nivel | Significado | Fuente |
|---|---|---|
| **Hecho verificado** | Información del Colegio Andino respaldada por documentos | El repositorio no contiene documentación institucional del colegio. Solo se usan el nombre del caso de estudio y su ubicación (Huancayo). |
| **AS-IS preliminar** | Descripción de la situación actual elaborada por el equipo, pendiente de validación con RR. HH./Administración | Análisis previo del equipo (capítulos 2 y 3) |
| **TO-BE propuesto** | Proceso mejorado diseñado por el proyecto | Línea base RF-01 a RF-27 y supuestos A-01 a A-36 |
| **Implementación** | Lo que existe y funciona en este repositorio | Código, pruebas PHPUnit/Cypress, Git y Docker |

Todos los datos del sistema son **ficticios** (usuarios `.test`, CV de ejemplo): `docs/demo-users.md`.

## 1.1 Resumen ejecutivo

**Problema.** En el análisis preliminar AS-IS, el reclutamiento del colegio presenta cinco problemas:

1. información distribuida;
2. seguimiento manual;
3. evaluaciones heterogéneas;
4. comunicación manual con los postulantes;
5. indicadores limitados para decidir.

La información dispersa y los criterios no uniformes dificultan la trazabilidad y la comparación objetiva de candidatos (capítulo 2).

**Solución.** Plataforma web SaaS multiempresa que cubre el proceso completo en **27 requerimientos funcionales (RF-01 a RF-27)**: requerimiento de personal y su aprobación, vacante con perfil y criterios ponderados, portal y postulación con CV, preselección y etapas, evaluaciones y entrevistas con puntajes, ranking explicable, decisión final, selección, cierre, notificaciones y auditoría.

El ranking es una herramienta de apoyo: **el sistema calcula, ordena y compara, pero la decisión final la registra una persona autorizada (Aprobador/Dirección)**. El sistema nunca selecciona automáticamente.

**Arquitectura y tecnologías.**
- Monolito modular multiempresa, con aislamiento por `organization_id` y autorización en el backend mediante Policies.
- Laravel 13 (PHP 8.4), React 19 + TypeScript + Inertia 3 + Tailwind 4.
- PostgreSQL 17, con restricciones de integridad y auditoría de solo inserción.
- Redis 7 para sesiones, caché y colas.
- Ejecución reproducible con Docker Compose.

**Enfoque de pruebas.**
- TDD (RED → GREEN → REFACTOR) con PHPUnit sobre PostgreSQL real, incluidas pruebas de autorización y de acceso entre organizaciones.
- Validación manual en navegador.
- Suite E2E automatizada con Cypress en un entorno aislado.

**Resultados reales al cierre de la Fase 10** (verificados de nuevo en la Fase 11):

| Indicador | Resultado |
|---|---|
| RF implementados | 27 de 27 |
| PHPUnit | 244 pruebas: 236 superadas, 8 omitidas (funciones del *starter kit* desactivadas), 0 fallidas, 1074 aserciones |
| Cypress | 14 specs y 43 tests: 43/43 en instalación limpia y 43/43 en el entorno principal |
| Defectos registrados / corregidos | 13 / 13 |
| Instalación desde cero con Docker | Validada en un clon limpio (87 s hasta servicios *healthy*) |
| Cobertura porcentual de código | No medida |

## 1.2 Introducción

**Contexto.** La gestión del talento en instituciones educativas requiere procesos transparentes y comparables. El caso de estudio del Colegio Andino de Huancayo se usa para diseñar y construir una solución de software. Como plataforma SaaS, la solución puede atender a varias organizaciones con datos aislados entre sí.

**Calidad de software.** El proyecto se desarrolla en el curso de Pruebas y Calidad de Software, por lo que la calidad es un objetivo explícito:
- trazabilidad de cada RF hasta su código, sus pruebas y su evidencia;
- desarrollo guiado por pruebas;
- registro honesto de defectos;
- automatización E2E;
- portabilidad del entorno.

Como marco de referencia se usa el modelo de calidad de producto ISO/IEC 25010 (capítulo 5), sin afirmar certificación alguna.

**Propósito.** Analizar, diseñar, implementar y verificar una plataforma que resuelva los problemas identificados. La decisión humana en la selección y la evidencia verificable de calidad son requisitos centrales.

**Alcance.**

| Incluido | Fuera de alcance |
|---|---|
| RF-01 a RF-27 con backend, frontend y pruebas | Nuevos RF fuera de la línea base |
| Cinco roles: Área solicitante, RR. HH., Aprobador/Dirección, Evaluador, Postulante | Rol SuperAdmin, administración de la plataforma y facturación |
| Multiempresa por `organization_id` y Policies | RLS de PostgreSQL (recomendación futura) |
| Notificaciones en base de datos y correo con *driver* `log` | Envío real de correo, SMS y mensajería |
| Cierre de convocatoria **con selección** | Cierre sin selección (A-30) |
| Entorno reproducible de desarrollo y demostración con Docker | Despliegue en la nube, CI/CD, R2/S3, Sentry, Meilisearch, IA y *talent pool* |

**Estructura del documento.**

| Capítulo | Archivo |
|---|---|
| 1. Información general | este archivo |
| 2. Contexto y problema | [02-contexto-problema.md](02-contexto-problema.md) |
| 3. Procesos de negocio | [03-procesos-negocio.md](03-procesos-negocio.md) |
| 4. Requerimientos | [04-requerimientos.md](04-requerimientos.md) |
| 5. Planificación y calidad | [05-planificacion-calidad.md](05-planificacion-calidad.md) |
| 6. Diseño del sistema | [06-diseno-sistema.md](06-diseno-sistema.md) |
| 7. Arquitectura tecnológica | [07-arquitectura-tecnologica.md](07-arquitectura-tecnologica.md) |
| 8. Desarrollo | [08-desarrollo.md](08-desarrollo.md) |
| 9. Control de versiones | [09-control-versiones.md](09-control-versiones.md) |
| 10. Dockerización | [10-dockerizacion.md](10-dockerizacion.md) |
| 11. Estrategia de pruebas | [11-estrategia-pruebas.md](11-estrategia-pruebas.md) |
| 12. Automatización de pruebas | [12-automatizacion-pruebas.md](12-automatizacion-pruebas.md) |
| 13. Métricas de calidad | [13-metricas-calidad.md](13-metricas-calidad.md) |
| 14. Implementación y monitoreo, conclusiones, recomendaciones, referencias y anexos | [14-implementacion-monitoreo.md](14-implementacion-monitoreo.md) |

**Documentos complementarios:**
- [traceability-master.md](traceability-master.md): matriz maestra RF.
- [evidence-index.md](evidence-index.md): índice de evidencias.
- [technical-summary.md](technical-summary.md): resumen para la exposición.
- [demo-script.md](demo-script.md): guion de demostración.
