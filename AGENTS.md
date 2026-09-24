# Gobierno del repositorio para Codex

Este repositorio contiene el SaaS multiempresa de reclutamiento de la Universidad Continental, caso Colegio Andino de Huancayo. Antes de planificar, revisar o editar, lee [`CLAUDE.md`](CLAUDE.md): es la fuente común de contexto, contratos y seguridad para Claude Code y Codex. Este archivo añade solo reglas de operación para Codex; no sustituye ni duplica `CLAUDE.md`.

## Inicio obligatorio

1. Lee `CLAUDE.md` y verifica con Git la rama, el estado y el alcance de la fase.
2. Lee `.claude/skills/project-guardian/SKILL.md` y su `CHECKLIST.md`.
3. Consulta `docs/PROGRESS.md` y la documentación vigente de `docs/v1.1/`; distingue documentos históricos de planes actuales.
4. Lee únicamente las skills pertinentes a la tarea según el mapa siguiente. No cargues todas por defecto.
5. Contrasta documentación con código y pruebas antes de tratar una afirmación como hecho.

## Skills compartidas y disclosure progresivo

La fuente canónica única es `.claude/skills/`. No existe un espejo en `.agents/skills/`: Codex debe abrir directamente los `SKILL.md` indicados. Resuelve sus referencias relativas desde el directorio de cada skill.

| Tipo de tarea | Skills que se deben leer/aplicar |
|---|---|
| Gobernanza general | `project-guardian` |
| Backend / Laravel | `project-guardian`, `laravel-saas-quality`, `academic-traceability` |
| Machine Learning | `project-guardian`, `ml-risk-service`, `academic-traceability`, `laravel-saas-quality` |
| Frontend | `project-guardian`, `frontend-design`, `animate`, `reviewing-a11y` |
| 3D | `project-guardian`, `recruitment-3d-experience` |
| UML / documentación | `project-guardian`, `academic-traceability`, `powerdesigner-uml` |

Reglas de compatibilidad:

- No instales automáticamente skills mencionadas por otra skill pero ausentes del repositorio.
- `reviewing-a11y` se usa por defecto solo para código o especificaciones locales. Browser, MCP, WebFetch o red requieren necesidad y autorización explícitas.
- No modifiques, reinstales ni actualices las skills externas o su provenance sin una fase y autorización específicas.

## Contratos del producto

- RF-01 a RF-27 son la línea base v1.0: no se renumeran ni reinterpretan.
- La decisión final sigue siendo humana, del Aprobador / Dirección, con confirmación y justificación. Ningún agente ni ML selecciona, descarta o contrata.
- Conserva `organization_id`, scopes, Policies, roles y pruebas cross-tenant.
- Conserva la auditoría segura y append-only; no almacenes PII o secretos en sus metadatos.
- Laravel continúa como sistema de registro. El ML actual (RF-29, experimental) y cualquier ML futuro son operacionales, informativos y opcionales.
- Los candidatos v1.1 siguen siendo candidatos hasta una aprobación explícita.

## Evidencia y trazabilidad

- Distingue siempre **AS-IS** (verificado), **TO-BE** (propuesto) e **implementado** (presente y probado).
- No inventes hechos, resultados, métricas, rutas, líneas ni pruebas. Declara lo no verificado.
- Un cambio funcional debe mantener la cadena requisito → regla → código → prueba → documentación.
- Preserva los documentos y el tag de v1.0 como evidencia histórica; documenta la evolución en `docs/v1.1/`.

## Git y supply chain

- Nunca trabajes directamente en `main` o `develop`; crea desde `develop` limpio y sincronizado una rama `feature/*`, `fix/*`, `docs/*` o `chore/*`.
- No descartes cambios ajenos. Prohibidos rebase de historia publicada, `reset --hard`, force push, borrado de ramas/tags y limpieza destructiva.
- No hagas push, merge, release o tag sin autorización explícita.
- No agregues dependencias, skills, hooks, binarios, instaladores ni scripts externos sin revisión de origen, licencia, versión fijada, riesgo y autorización.
- Nunca ejecutes instaladores remotos ni amplíes permisos para eludir controles.

## Secretos, datos y configuración

- Solo datos ficticios. No uses PII, CV o credenciales reales.
- No versiones `.env`, `.env.e2e`, tokens, claves ni configuración de HOME.
- `.claude/settings.local.json` es local, está ignorado y no se modifica sin autorización.
- No escribas en configuración global de Claude, Codex o Git como efecto lateral de una tarea del repositorio.

## Testing y definición de terminado

- Pruebas proporcionales al riesgo: regla o flujo nuevo requiere test trazable; cálculo puro, test unitario; acceso multiempresa, caso cross-tenant; interfaz, conservar `data-cy` y revisar E2E afectado.
- Para cambios funcionales, ejecuta las regresiones exigidas por `project-guardian` dentro de Docker y reporta resultados reales.
- Para cambios exclusivamente documentales o de gobernanza, valida al menos alcance del diff, enlaces, rutas, formato, secretos y ausencia de código/dependencias; explica por qué no se ejecutaron suites funcionales.
- Antes de cerrar: rama correcta, diff limitado al alcance, contratos preservados, documentación/trazabilidad coherentes, pruebas aplicables ejecutadas, árbol limpio tras el commit y ninguna publicación no autorizada.

## Colaboración multiagente

Debe existir un solo **WRITER PRINCIPAL** por rama y área de trabajo. El reviewer permanece en modo lectura mientras el writer está activo y no modifica archivos salvo autorización explícita.

Patrón orientativo:

- ChatGPT: arquitectura, prompts y decisiones.
- Claude Code: implementación principal cuando la fase lo determine.
- Codex: auditoría, diseño técnico, QA, validación de diff y revisión post-implementación.

La herramienta principal puede cambiar por fase; la exclusión de escritores concurrentes no cambia. Antes del handoff, registra rama, commit base, alcance, archivos reservados, validaciones y pendientes. Flujo completo: [`docs/v1.1/multi-agent-workflow.md`](docs/v1.1/multi-agent-workflow.md).
