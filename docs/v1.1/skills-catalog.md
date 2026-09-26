# Catálogo de skills — Fase 13

Registro de las skills de asistencia disponibles en el proyecto, su procedencia y su clasificación de riesgo. Auditoría realizada el 19 de septiembre de 2026 mediante **revisión estática**: clonado superficial en un directorio temporal fuera del proyecto, listado de archivos, lectura de metadatos y búsqueda de patrones peligrosos. **No se ejecutó ningún instalador, script ni binario.**

### Precisión sobre el método

La auditoría **sí escribió fuera del repositorio**, y conviene decirlo con exactitud: los cuatro repositorios de origen se clonaron en el directorio de trabajo temporal de la sesión, `~/.claude/jobs/<id>/tmp/skill-audit/` (1 959 archivos, 41.24 MB). Ese directorio está **fuera del proyecto** y fuera de cualquier ruta de configuración global; no se modificó `~/.claude`, `~/.config`, AppData, el PATH ni el perfil de PowerShell. `git clone` no transfiere ni ejecuta *hooks*, por lo que el clonado no ejecuta código del repositorio de origen.

Antes de eliminarlos se verificó por hash SHA-256 que **cada archivo instalado es idéntico a su origen auditado** (2/2 en `frontend-design`, 2/2 en `animate`, 13/13 en `reviewing-a11y`; el único archivo añadido por el proyecto es `PROVENANCE.md`). Hecha esa comprobación, los clones se **eliminaron** el 19 de septiembre de 2026. Los SHA fijados de esta página permiten reproducir la auditoría desde cero cuando haga falta.

## 1. Skills propias del proyecto

Escritas en esta fase, puramente declarativas (Markdown), sin scripts, sin red, sin binarios. Riesgo **BAJO** por construcción.

| Skill | Propósito | Archivos |
|---|---|---|
| `project-guardian` | Compuerta previa a cualquier cambio: rama, alcance, contratos, pruebas y documentación | `SKILL.md`, `CHECKLIST.md` |
| `laravel-saas-quality` | Patrón del backend multiempresa y su regresión obligatoria | `SKILL.md`, `PATTERNS.md` |
| `ml-risk-service` | Marco del servicio de riesgo operacional (~~no implementado~~ implementado como experimental en las Fases 15–17) | `SKILL.md`, `EVALUATION.md` |
| `academic-traceability` | Trazabilidad RF ↔ código ↔ pruebas ↔ UML ↔ entorno ↔ Formato 09 | `SKILL.md` |
| `powerdesigner-uml` | UML derivado del código real y su paso a PowerDesigner | `SKILL.md`, `POWERDESIGNER.md` |
| `recruitment-3d-experience` | 3D público, progresivo y acotado (~~no implementado~~ implementado con CSS 3D en la Fase 20, solo en la portada) | `SKILL.md`, `BUDGETS.md` |

## 2. Skills externas instaladas

Instaladas **localmente** en `.claude/skills/`, con su `PROVENANCE.md` y su licencia. Ninguna se instaló de forma global.

| Skill | Origen | Propietario | Commit fijado | Licencia | Riesgo |
|---|---|---|---|---|---|
| `frontend-design` | github.com/anthropics/skills | Anthropic | `34040c9c568585f6929bedeaad110ad08f079624` | Apache 2.0 | BAJO |
| `animate` | github.com/emilkowalski/skills | Emil Kowalski | `85e8e2363b713506e1d5b6e07a0eb2da66be1bc3` | MIT | BAJO |
| `reviewing-a11y` | github.com/masuP9/a11y-specialist-skills | Soichi Masuda (masuP9) | `6615e6eb0bfa994a2ac1b2e6edb8d3ccdf44c587` | MIT | MEDIO |

**Condición sobre `reviewing-a11y`:** su `SKILL.md` declara `WebFetch` y herramientas MCP de Playwright. Los archivos son inertes y el servidor MCP no está instalado, pero su modo con navegador o red **requiere autorización explícita del equipo**. Hasta entonces se usa solo en revisión de código y especificaciones (`Read`, `Grep`, `Glob`).

Observaciones de la auditoría: del repositorio de `animate` no se copió un archivo `.pl` que está **vacío (0 bytes)**; del repositorio de `reviewing-a11y` **no se copió** el paquete ejecutable `packages/a11y-audit` (Playwright, CLI y flujos de CI), fuera del alcance de esta fase.

Detalle completo por skill: `.claude/skills/<nombre>/PROVENANCE.md`.

## 3. Skills auditadas y NO instaladas

### 3.1 Bloqueadas por licencia e instalación global

Origen: `github.com/anthropics/claude-code`, commit `bf7d404e26a5fb6167d21b46c93a2bf6c22ab274`. Su `LICENSE.md` dice: "© Anthropic PBC. All rights reserved. Use is subject to Anthropic's Commercial Terms of Service". Copiar estos archivos al repositorio sería redistribución no autorizada, y la vía oficial (marketplace de plugins) instala a nivel de usuario, es decir **global**, lo que la Fase 13 prohíbe sin autorización.

| Plugin | Contenido | Riesgo | Estado |
|---|---|---|---|
| `pr-review-toolkit` | 6 agentes de revisión + `commands/review-pr.md` (`allowed-tools`: Bash, Glob, Grep, Read, Task) | MEDIO (declara Bash) | **REQUIERE AUTORIZACIÓN PARA INSTALACIÓN GLOBAL** |
| `feature-dev` | 3 agentes + comando de desarrollo de funcionalidades | MEDIO | **REQUIERE AUTORIZACIÓN PARA INSTALACIÓN GLOBAL** |
| `security-guidance` | 13 archivos de *hooks* en Python/Bash; `ensure_agent_sdk.py` crea un entorno virtual y ejecuta `pip install`; uso extenso de `subprocess.run` | **ALTO** | **NO INSTALADA** |

`security-guidance` no se instalaría aunque se resolviera la licencia: ejecuta hooks automáticos, instala paquetes y lanza subprocesos, lo que contradice directamente las reglas de esta fase.

### 3.2 Omitidas por procedencia insuficiente

| Candidata | Motivo |
|---|---|
| Skills de PlantUML/UML de terceros (p. ej. `SpillwaveSolutions/plantuml`) | **Sin licencia declarada** y mantenimiento escaso. La necesidad queda cubierta por la skill propia `powerdesigner-uml`. |
| "responsive-design" | Sin origen oficial identificable; nombre genérico con múltiples copias no atribuibles. **REQUIERE REVISIÓN MANUAL** |

Regla aplicada: ante duda razonable sobre la seguridad o la procedencia de una skill externa, **no se instala**; se documenta y se continúa.

## 4. Reglas permanentes para incorporar skills

1. Revisión estática antes de instalar: `SKILL.md`, `README`, manifiestos, *lockfiles*, `scripts/`, `hooks/`, `bin/`, scripts de `install`/`postinstall` y flujos de CI.
2. Búsqueda obligatoria de patrones peligrosos: `curl`, `wget`, `Invoke-WebRequest`, `Invoke-Expression`, `eval`, `exec`, `subprocess`, `os.system`, `child_process`, `spawn`, `postinstall`, descarga o ejecución de binarios, escritura fuera del repositorio, lectura de credenciales o variables de entorno, telemetría.
3. Nunca instalar por nombre, ni con `curl | bash`, ni con instaladores no revisados.
4. Origen inequívoco, propietario identificado, licencia adecuada y **commit fijado** registrado en `PROVENANCE.md`.
5. Red, Bash, PowerShell, binarios, hooks, acceso a `~/.claude` o escritura fuera del repositorio ⇒ riesgo **MEDIO** como mínimo y autorización explícita antes de usarse.
6. Instalación **local** en el proyecto. Sin instalaciones globales en esta fase.
7. Instalar una skill no autoriza ejecutar sus scripts auxiliares.
8. Tras instalar, revisar el diff: solo los archivos esperados. Si aparece algo más, detenerse y pedir autorización.
9. Nunca añadir dependencias de producción, ni ejecutar `npm install`, `pip install`, `composer require` o equivalentes como efecto lateral de una skill.
10. Nunca desactivar controles de seguridad ni pedir al usuario que pegue tokens en un instalador.
