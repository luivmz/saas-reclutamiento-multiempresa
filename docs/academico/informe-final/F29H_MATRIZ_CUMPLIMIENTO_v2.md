# Cumplimiento de la plantilla y requisitos de entrega

La plantilla de estructura se contrastó por orden, títulos y contenido. El PDF y el DOCX actualizado comparten la paginación. Las páginas indicadas son folios del documento exportado.

## Requisitos obligatorios

| Requisito | Ubicación | Evidencia y estado |
|---|---|---|
| Portada con integrantes | p. 1 | Tres integrantes y datos del curso cotejados con v1, CLAUDE.md y README. Portada, logo y folio de la plantilla visual. Desarrollado. |
| Enunciado del caso práctico | §2.1, pp. 6–7 | Enunciado, alcance, actividades y objetivos de mejora. AS-IS preliminar. Desarrollado. |
| Arquitectura grupal | §§6.1–7.4, desde p. 17 | Arquitectura general, UML, PDM, despliegue, mapeo a archivos y contexto experimental. Desarrollado. |
| Solución del caso | §§3.4, 4.2 y 8.1–8.4, desde p. 21 en desarrollo | Solución por problema, 27 RF y flujo transaccional. Decisión RF-23 a cargo de Dirección. Desarrollado. |
| Evidencias del proceso de pruebas | §§11–13, matriz en p. 27, más A.2 y A.3 | Casos, alcance, fechas, referencia y evidencias. Coberturas y limitaciones diferenciadas. Desarrollado. |
| Enlace Git | §9.1, p. 22 | Repositorio público y enlaces a revisiones, release y evidencias. Verificado. |
| Enlace de implementación | §14.2, p. 31 | Guía local reproducible y healthchecks consultados. URL pública y SHA servido pendientes de confirmación. Cumplimiento parcial. |

## Capítulos y apartados oficiales

| Capítulo / apartado | Página de inicio | Desarrollo en v2 |
|---|---:|---|
| 1.1. Resumen Ejecutivo | 6 | Problema, solución, decisiones de alcance y corte por rama. |
| 1.2. Introducción | 6 | Objetivos vinculados con P1 a P5 y método de lectura. |
| 2.1. Contexto de la Organización | 6 | Actores, alcance del caso y enunciado práctico. |
| 2.2. Identificación del Problema | 7 | Cinco problemas, prioridades e impacto sin medición institucional. |
| 3.1. Descripción del Proceso Actual | 8 | Ocho macroactividades y sus responsables. |
| 3.2. Modelado del Proceso Actual (AS-IS) | 8 | AS-01 a AS-14 y lámina AS-IS del anexo. |
| 3.3. Problemas del Proceso Actual | 9 | Actividades afectadas y responsables de validar hipótesis. |
| 3.4. Modelado del Proceso Propuesto (TO-BE) | 9 | Soluciones S-01 a S-05, objetivos y lámina TO-BE. |
| 4.1. Identificación de Actores del Sistema | 10 | Cinco roles, alcance y notificaciones del sistema. |
| 4.2. Requerimientos Funcionales | 11 | RF-01 a RF-27 con actor y descripción, RF candidatos contextualizados. |
| 4.3. Requerimientos no Funcionales | 12 | Diez RNF con criterios y estado de evidencia. |
| 4.4. Casos de Uso del Sistema | 13 | CU-01 a CU-20, trazabilidad y figura de casos de uso. |
| 5.1. Alcance del Proyecto | 14 | Ocho bloques, exclusiones y alcance experimental en Git. |
| 5.2. Herramientas Tecnológicas del Proyecto | 15 | Stack real, herramientas y límites metodológicos. |
| 5.3. Normas y Estándares de Calidad | 16 | ISO/IEC 25010, TDD, WCAG, acceso y uso ficticio. |
| 5.4. Plan de Pruebas del Proyecto | 16 | Plan F29D, criterios CA-01 a CA-07 y enlace reproducible. |
| 5.5. Lineamientos de Seguridad Informática | 16 | Autenticación, Policies, aislamiento, auditoría y CV privado. |
| 6.1. Arquitectura Conceptual del Sistema | 17 | Arquitectura grupal, figura 1 y correspondencia con el código. |
| 6.2. Modelo UML del Sistema | 17 | UML F22/F23, secuencia RF-23 y catálogo de modelos. |
| 6.3. Diseño de Interfaces de Usuario | 18 | Pantallas reales, navegación y casos de interfaz en anexos. |
| 6.4. Diseño de Base de Datos | 19 | Relaciones, restricciones e imagen PDM de dominio. |
| 7.1. Tecnologías del Frontend | 20 | React, Inertia, Wayfinder y compilación del cliente. |
| 7.2. Tecnologías del Backend | 20 | Laravel, validación, autorización, cola y ML-01 opcional. |
| 7.3. Base de Datos del Sistema | 20 | PostgreSQL, migraciones, aislamiento de pruebas y Redis. |
| 7.4. Infraestructura de Desarrollo | 21 | Entorno Compose y ejecución separada de FastAPI. |
| 8.1. Iteración 1: Configuración Inicial del Proyecto | 21 | Inicialización del repositorio, aplicación, autenticación y datos. |
| 8.2. Iteración 2: Desarrollo de Funcionalidades Básicas | 21 | Requerimientos y vacantes con primeras páginas Inertia. |
| 8.3. Iteración 3: Implementación de Módulos Funcionales | 21 | Postulación, evaluación, ranking, decisión y auditoría. |
| 8.4. Iteraciones Posteriores | 21 | Etapas posteriores, evidencias, BM25, Reportes e interfaz. |
| 9.1. Repositorio del Proyecto | 22 | Repositorio público, release y evidencias enlazadas. |
| 9.2. Estrategia de Control de Versiones | 22 | Ramas, commits, checkpoints y revisión. |
| 9.3. Gestión de Ramas del Proyecto | 22 | Tabla de ramas con SHA y estado de integración. |
| 9.4. Registro de Commits Relevantes | 23 | Selección de commits históricos y del corte. |
| 10.1. Introducción a Docker en el Proyecto | 23 | Beneficios de contenedores y reproducibilidad. |
| 10.2. Dockerización del Backend | 23 | Imagen PHP, dependencias y ejecución del servidor. |
| 10.3. Dockerización del Frontend | 23 | Vite compila React y Laravel sirve las páginas Inertia. |
| 10.4. Orquestación con Docker Compose | 24 | Topología local y figura de Docker, base, Redis y worker. |
| 11.1. Enfoque de Pruebas del Proyecto | 25 | TDD y evidencia de casos positivos y negativos. |
| 11.2. Niveles de Pruebas Aplicados | 25 | Unitarias, integración, componentes, E2E y aceptación técnica. |
| 11.3. Tipos de Pruebas Ejecutadas | 25 | Pruebas funcionales, autorización, aislamiento y UI. |
| 11.4. Plan de Ejecución de Pruebas | 26 | Orden de ejecución y RACI con calendario F29D. |
| 12.1. Herramientas de Automatización | 26 | Herramientas y archivos de prueba versionados. |
| 12.2. Configuración del Entorno de Pruebas | 26 | Bases aisladas, variables E2E y servicio Python. |
| 12.3. Scripts de Pruebas Automatizadas | 27 | Casos reales en PHPUnit y Cypress con enlace a código. |
| 12.4. Ejecución Automática de Pruebas | 27 | Workflow y dos ejecuciones de GitHub Actions por SHA. |
| 13.1. Ejecución de Casos de Pruebas | 27 | Matriz de ejecución con alcance, revisión, fecha y evidencia. |
| 13.2. Registro de Defectos | 28 | Defectos, severidad registrada, corrección y regresión. |
| 13.3. Métricas de Calidad del Software | 29 | Cobertura funcional y Sonar V3 por ámbito con deuda visible. |
| 13.4. Evaluación de Calidad basada en Estándares | 30 | ISO 25010, límites y métricas sintéticas de ML. |
| 14.1. Preparación del Entorno de Implementación | 30 | Preparación con Compose y guía de datos ficticios. |
| 14.2. Implementación del Sistema | 31 | Implementación local reproducible y URL pública pendiente. |
| 14.3. Verificación de Funcionamiento | 31 | Comprobación de servicios y evidencia de flujo. |
| 14.4. Monitoreo del Sistema | 31 | Healthchecks, logs, cola fallida y alcance de observabilidad. |
| Conclusiones | 31 | Objetivos, calidad, estados por rama y resultados ML. |
| Recomendaciones | 32 | Validación, instrumentación, seguridad operacional y publicación. |
| Referencias | 32 | Fuentes institucionales, técnicas y científicas enlazadas. |
| Anexos | 33 | Modelos, capturas, evidencias y catálogos editables. |
| A.5. Cierre técnico de la entrega integrada | 42 | Revisiones de origen, controles del candidato, alcance y enlace de publicación. |

## Formato institucional

| Elemento | Verificación |
|---|---|
| Portada y páginas interiores | Modelo visual conservado en A4, con el encabezado, pie, márgenes y borde de la plantilla. Una página horizontal para el PDM. |
| Contenido general e índices | Campos TOC actualizados y enlaces PDF. Índice de 17 figuras e índice de 30 tablas. |
| Tablas, figuras y referencias | Encabezados de tabla repetidos y notas de procedencia. Rótulos SEQ y referencias REF evaluadas. |
| Entregables y reproducción | DOCX, PDF, Markdown, figuras y comandos en el mismo directorio. |
