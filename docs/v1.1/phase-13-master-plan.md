# Fase 13 — Plan maestro de gobierno de v1.1

**Fecha:** 19 de septiembre de 2026
**Rama:** `chore/phase-13-governance` (creada desde `develop` en `dbada5e`)
**Naturaleza:** gobierno y documentación. **No se implementó ninguna funcionalidad.**

## 1. Objetivo

Preparar la versión 1.1 sin tocar el producto: auditar el estado real del repositorio, instalar de forma segura las herramientas de asistencia que el equipo usará, escribir las reglas propias del proyecto y documentar el alcance preliminar y las decisiones pendientes.

## 2. Qué sí se hizo

| Paso | Resultado |
|---|---|
| Auditoría del estado real del repositorio | Verificado en `git`: v1.0 publicada, `main` y `develop` alineadas, tag `v1.0.0-academic` intacto |
| Rama de gobierno | `chore/phase-13-governance` |
| Auditoría estática de skills externas | 3 instaladas, 3 auditadas y no instaladas (ver `skills-catalog.md`) |
| Skills propias del proyecto | 6 creadas en `.claude/skills/` |
| Reglas de trabajo | `CLAUDE.md` en la raíz |
| Alcance preliminar | `scope-preliminary.md`, `ml-feasibility.md`, `documentation-update-map.md`, 3 ADR |

## 3. Qué explícitamente no se hizo

No se implementó ni se preparó terreno técnico para: machine learning, servicio FastAPI, entrenamiento o datasets, integración Laravel–Python, rutas funcionales nuevas, migraciones, rediseño del frontend, librerías de animación, Three.js o modelos 3D, UML definitivo, archivos de PowerDesigner, cambios productivos en Docker. RF-28 y los RNF nuevos **no** existen como requerimientos aprobados: son candidatos.

## 4. Archivos que la fase podía tocar

Únicamente `CLAUDE.md`, `.claude/skills/**` y `docs/v1.1/**`. No se modificó `app/`, `routes/`, `resources/`, `database/`, `tests/`, `cypress/`, Dockerfiles, `composer.json`, `package.json`, flujos de CI, variables de entorno ni documentación histórica de v1.0.

## 5. Línea base verificada

Datos tomados de la última ejecución registrada de v1.0, **no reejecutados en esta fase**:

| Elemento | Estado en v1.0 |
|---|---|
| Requerimientos | RF-01 a RF-27 implementados y trazados |
| PHPUnit | 244 pruebas: 236 aprobadas, 8 omitidas, 0 fallidas |
| Cypress | 14 especificaciones, 43 pruebas, 43 aprobadas |
| Publicación | Tag `v1.0.0-academic` + corrección posterior de CI |
| Veredicto QA | Apto para publicación |

## 6. Hallazgos abiertos

| Hallazgo | Detalle | Estado |
|---|---|---|
| Permisos locales amplios | `.claude/settings.local.json` acumula permisos de fases anteriores, entre ellos `PowerShell(Remove-Item *)`, `PowerShell(git *)`, `PowerShell(docker compose *)` y `WebFetch(domain:api.github.com)` | **No se modificó.** Su revisión y reducción es una **compuerta de seguridad previa a la Fase 14** |
| Clones temporales de auditoría | `~/.claude/jobs/<id>/tmp/skill-audit/` — 4 repositorios, 41.24 MB, fuera del repositorio y fuera de la configuración global | **Eliminados** el 19/09/2026, tras verificar por hash que las copias instaladas son idénticas al origen |
| Prompt sin rastrear | `PROMPT_FASE_13_CLAUDE_CODE.md` en la raíz | No se tocó ni se versionará |

El archivo de permisos no se versiona (`.gitignore:35`), por lo que ninguno de estos permisos se publica; el riesgo es de ejecución local, no de exposición.

## 7. Contratos vigentes

Los diez contratos inviolables están en `CLAUDE.md` y los aplica la skill `project-guardian`. Los tres más relevantes para v1.1: RF-01 a RF-27 no cambian de número ni de significado; el sistema nunca decide por una persona; cualquier ML será operacional e informativo.

## 8. Compuerta hacia la Fase 14

La Fase 14 no debe empezar hasta que el equipo decida, de forma explícita y registrada:

1. qué candidatos de `scope-preliminary.md` se aprueban como requerimientos de v1.1;
2. si el servicio de riesgo operacional se explora o se descarta (`ml-feasibility.md`);
3. si se autoriza la experiencia 3D y las dependencias que implica;
4. si se autorizan las skills que hoy quedan pendientes por instalación global;
5. qué entregables académicos exige la siguiente evaluación y con qué fecha;
6. si se revisan y recortan los permisos de `.claude/settings.local.json` (hallazgo de la sección 6).

Hasta entonces, v1.1 permanece en estado de planificación y `develop` conserva el contenido de v1.0.

## 9. Documentos de esta fase

- [Catálogo de skills](skills-catalog.md)
- [Alcance preliminar](scope-preliminary.md)
- [Viabilidad del servicio de riesgo](ml-feasibility.md)
- [Mapa de actualización documental](documentation-update-map.md)
- [ADR-001 — Frontera del ML](architecture-decisions/ADR-001-ml-boundary.md)
- [ADR-002 — Supervisión humana](architecture-decisions/ADR-002-human-oversight.md)
- [ADR-003 — 3D progresivo](architecture-decisions/ADR-003-progressive-3d.md)
