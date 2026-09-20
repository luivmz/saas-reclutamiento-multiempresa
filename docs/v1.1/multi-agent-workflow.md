# Fase 14.5 — Flujo de trabajo multiagente

**Fecha:** 20 de septiembre de 2026

**Rama:** `chore/phase-14-5-multi-agent`

**Alcance:** gobierno y configuración de agentes dentro del repositorio. Sin cambios funcionales.

## 1. Objetivo

Permitir que ChatGPT, OpenAI Codex y Claude Code colaboren con las mismas reglas del proyecto, una sola fuente de skills y handoffs verificables. Esta fase no inicia Fase 15, no implementa ML y no cambia Laravel, React, Docker, CI, pruebas ni dependencias.

Fuentes de gobierno:

- [`CLAUDE.md`](../../CLAUDE.md): contexto y contratos comunes del proyecto.
- [`AGENTS.md`](../../AGENTS.md): instrucciones persistentes y routing de skills para Codex.
- [`.claude/skills/`](../../.claude/skills/): fuente canónica única de las nueve skills versionadas.

## 2. Decisión de arquitectura para skills

### Decisión: puente por instrucciones, sin espejo físico

Codex leerá `AGENTS.md` al iniciar una sesión en el repositorio. Ese archivo selecciona por tipo de tarea y ordena abrir directamente los `SKILL.md` canónicos de `.claude/skills/`. No se crea `.agents/skills/`.

La documentación oficial confirma que Codex descubre instrucciones `AGENTS.md` desde la raíz del proyecto y que sus skills repo-scoped se ubican normalmente en `.agents/skills`; también puede seguir directorios de skill enlazados. Referencias: [AGENTS.md](https://developers.openai.com/es-419/docs/agent-configuration/agents-md) y [skills](https://developers.openai.com/es-419/docs/build-skills).

### Alternativas evaluadas

| Opción | Resultado | Motivo |
|---|---|---|
| A. Symlink relativo `.agents/skills` → `.claude/skills` | Rechazada para este repositorio | Git/Windows del clon actual tiene `core.symlinks=false`; un checkout Windows puede materializar el enlace versionado como archivo plano. Developer Mode local no garantiza la configuración de otros clones |
| B. Puente en `AGENTS.md` | **Elegida** | Una fuente, rutas relativas versionadas, sin privilegios, scripts, duplicados ni configuración global; funciona igual en Windows y macOS |
| C. Junction de Windows | Rechazada | Es específica de Windows y Git no conserva de forma portable la intención de junction para macOS |
| D. Copia de las skills | Rechazada | Duplica nueve fuentes y crea riesgo inmediato de divergencia de contenido y provenance |

Consecuencia conocida: las skills canónicas no aparecerán como skills repo-scoped en el selector `/skills` de Codex. Se descubren por el routing persistente de `AGENTS.md` y se leen por ruta. Es una concesión deliberada a la portabilidad. Si OpenAI incorpora en el futuro una ruta canónica configurable dentro del repositorio, esta decisión debe revisarse sin duplicar contenido.

## 3. Inventario y compatibilidad

Auditoría estructural de Fase 14.5:

| Skill | Origen | `SKILL.md` + frontmatter | Compatibilidad observada |
|---|---|---|---|
| `project-guardian` | Propia | Válido | Instrucciones genéricas; compatible |
| `laravel-saas-quality` | Propia | Válido | Instrucciones y comandos del repositorio; compatible |
| `ml-risk-service` | Propia | Válido | Instrucciones genéricas; compatible. Su estado funcional se interpreta con la documentación vigente de Fase 14 |
| `academic-traceability` | Propia | Válido | Instrucciones genéricas; compatible |
| `powerdesigner-uml` | Propia | Válido | Instrucciones genéricas; compatible |
| `recruitment-3d-experience` | Propia | Válido | Instrucciones genéricas; compatible |
| `frontend-design` | Externa | Válido | Declarativa; provenance y SHA preservados |
| `animate` | Externa | Válido | Declarativa; menciona skills compañeras no instaladas. No se instalan: si faltan, el agente informa el límite y aplica solo las instrucciones disponibles |
| `reviewing-a11y` | Externa | Válido | El frontmatter declara nombres de herramientas Claude/MCP. El modo local de revisión de código/especificaciones es compatible; navegador, MCP y red no se autorizan por la skill |

Hallazgos comunes:

- los nueve directorios contienen `SKILL.md` con `name` y `description` coherentes con el nombre del directorio;
- no hay rutas absolutas en sus instrucciones principales;
- no hay scripts, hooks o binarios ejecutables dentro de las skills instaladas;
- las tres skills externas conservan `PROVENANCE.md`, licencia y commits fijados de Fase 13;
- no se modificó ninguna skill en esta fase.

## 4. Selección progresiva

No se cargan las nueve skills en cada tarea. `AGENTS.md` define este routing:

| Trabajo | Skills |
|---|---|
| Gobierno | `project-guardian` |
| Backend/Laravel | `project-guardian`, `laravel-saas-quality`, `academic-traceability` |
| ML | `project-guardian`, `ml-risk-service`, `academic-traceability`, `laravel-saas-quality` |
| Frontend | `project-guardian`, `frontend-design`, `animate`, `reviewing-a11y` |
| 3D | `project-guardian`, `recruitment-3d-experience` |
| UML/documentación | `project-guardian`, `academic-traceability`, `powerdesigner-uml` |

El agente lee primero el `SKILL.md`; abre referencias, recetas o checklists solo cuando el trabajo las necesita.

## 5. Responsabilidades y writer principal

| Herramienta | Responsabilidad habitual |
|---|---|
| ChatGPT | Arquitectura, prompts, decisiones y coordinación |
| Claude Code | Implementación principal cuando lo autoriza la fase |
| Codex | Auditoría, revisión científica/técnica, QA, validación de diff y revisión posterior |

La matriz no asigna propiedad permanente. Para cada fase se designan:

- **writer principal:** único agente autorizado a editar la rama/área;
- **reviewer:** trabaja en lectura y reporta hallazgos;
- **decisor humano:** resuelve cambios de alcance, dependencias, publicación y conflictos.

Nunca hay dos writers concurrentes en la misma rama o área. El reviewer no corrige mientras el writer está activo salvo autorización explícita. Si se requiere paralelismo, se usan áreas y ramas no superpuestas con ownership declarado.

## 6. Matriz orientativa por fases

| Fase | Writer o responsable principal | Revisión/apoyo |
|---|---|---|
| 15 | Claude Code — implementación | Codex — auditor científico/técnico |
| 16 | Claude Code — implementación | Codex — contrato Laravel ↔ FastAPI |
| 17 | Claude Code — correcciones/implementación | Codex — auditor fuerte de testing |
| 18 | Claude Code — frontend | Codex — estructura y accesibilidad |
| 19 | Claude Code — motion | Codex — rendimiento y reduced motion |
| 20 | Claude Code — 3D | Codex — rendimiento, WebGL y fallback |
| 21 | Claude Code — correcciones | Codex — QA/review |
| 22 | Codex — derivación UML desde código | Claude Code — apoyo documental |
| 23 | Codex — consistencia PowerDesigner | Claude Code — apoyo en artefactos |
| 24 | Claude Code — actualización documental | Codex — coherencia |
| 25 | Claude Code — correcciones | Codex — QA final |
| 26 | Codex — guardián de release/Git | Claude Code — correcciones necesarias |

Es una guía, no una restricción absoluta. El equipo puede intercambiar herramientas si registra el nuevo writer y mantiene un solo escritor activo.

## 7. Flujo de trabajo y revisión

1. El humano define fase, alcance, writer, reviewer y criterios de terminado.
2. El writer parte de `develop` limpio/sincronizado y crea la rama aprobada.
3. El writer registra el commit base y los archivos/áreas reservados.
4. El reviewer inspecciona en modo lectura mientras haya escritura activa.
5. El writer valida, muestra el diff y entrega un commit auditable.
6. El reviewer revisa el commit/diff contra contratos, skills, pruebas y documentación; no modifica durante la revisión.
7. El writer corrige hallazgos autorizados o el humano reasigna formalmente el rol.
8. Push, merge, tag y release requieren autorización humana explícita.

Un handoff incluye: rama, SHA base/actual, objetivo, archivos cambiados, decisiones, pruebas ejecutadas con resultados, pruebas no ejecutadas, riesgos y pendientes.

## 8. Política Git y supply chain

- No trabajar directamente en `main` o `develop`.
- No rebase de historia publicada, force push, `reset --hard`, limpieza destructiva ni movimiento de tags.
- No ocultar ni descartar cambios de otro agente.
- No instalar dependencias o skills por conveniencia. Toda incorporación exige procedencia, licencia, versión fijada, auditoría y autorización.
- Las skills externas instaladas no se actualizan ni reinstalan en una fase funcional.
- Browser, MCP, WebFetch y red no quedan autorizados por aparecer en una skill.

## 9. Portabilidad y clonación

### Windows

- Clonar normalmente con Git; no se requiere Developer Mode, privilegio administrativo, junction, symlink ni cambio de `core.symlinks`.
- Iniciar una sesión nueva de Codex en la raíz para que cargue `AGENTS.md`.
- Claude Code continúa leyendo `CLAUDE.md` y `.claude/skills/` como antes.

### macOS/Linux

- El mismo checkout contiene archivos reales bajo `.claude/skills/`; no depende de enlaces creados en Windows.
- Iniciar una sesión nueva de Codex en la raíz. Las rutas del puente son relativas y usan nombres versionados.
- No se necesita paso post-clone.

Codex construye su cadena de instrucciones al iniciar la sesión. Tras `git pull` que añada o cambie `AGENTS.md`, reinicia Codex para garantizar detección; no hay caché del repositorio que deba borrarse.

## 10. Qué viaja con Git

Viaja:

- `CLAUDE.md`;
- `AGENTS.md`;
- este documento;
- `.claude/skills/**`, incluidos provenance y licencias;
- el resto de configuración segura ya versionada del repositorio.

No viaja:

- `.claude/settings.local.json`, ignorado por `.gitignore`;
- permisos de sesión;
- tokens, credenciales y secretos;
- configuración bajo HOME de Codex o Claude;
- configuración global de Git o del sistema;
- estado de una sesión ya abierta.

No se crea configuración global ni script post-clone.

## 11. Prueba de descubrimiento y límites

Verificaciones estáticas de esta fase:

1. `AGENTS.md` está en la raíz, contiene el routing y queda dentro del límite normal de instrucciones de Codex.
2. Cada ruta `.claude/skills/<name>/SKILL.md` existe y puede leerse.
3. Cada skill tiene frontmatter, `name` y `description` válidos.
4. El routing diferencia gobierno, backend, ML, frontend, 3D y UML/documentación.
5. No existe espejo ni copia divergente en `.agents/skills/`.
6. `CLAUDE.md` y las skills canónicas permanecen sin cambios.

Limitación verificable: la sesión de Codex que creó estos archivos comenzó antes de que existiera `AGENTS.md`, por lo que no puede demostrar recarga automática dentro de la misma sesión. La documentación oficial indica que la cadena se reconstruye al iniciar una sesión; la verificación interactiva completa requiere una sesión nueva. No se ejecuta un segundo agente con permisos de escritura solo para demostrarlo.

## 12. Validación proporcional

Al ser un cambio exclusivo de gobernanza, se validan Git, diff/allowlist, Markdown, rutas, frontmatter, referencias, secretos, ausencia de duplicados y ausencia de código/dependencias. No se ejecutan PHPUnit, Cypress, build ni TypeScript porque ningún archivo funcional cambió.
