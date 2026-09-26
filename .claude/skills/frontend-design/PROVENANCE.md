# Procedencia — frontend-design

Skill externa instalada localmente en la Fase 13. No fue modificada: `SKILL.md` y `LICENSE.txt` son copia literal del origen.

| Campo | Valor |
|---|---|
| Nombre | `frontend-design` |
| Origen | https://github.com/anthropics/skills (carpeta `skills/frontend-design`) |
| Propietario | Anthropic (fuente oficial) |
| Commit fijado | `34040c9c568585f6929bedeaad110ad08f079624` |
| Fecha del commit | 2026-09-10 |
| Licencia | Apache 2.0 (incluida en `LICENSE.txt`) |
| Tipo | Declarativa (solo Markdown) |
| Scripts / binarios / hooks | Ninguno |
| Acceso de red | No |
| Escritura fuera del repositorio | No |
| Riesgo | **BAJO** |
| Instalada | Sí, en `.claude/skills/frontend-design/` |
| Auditada el | 2026-09-19 |

## Uso previsto

Criterio visual para pantallas nuevas o rediseños del frontend.

## Límites en este proyecto

- **No autoriza rediseñar el frontend en la Fase 13**: v1.1 todavía no tiene alcance de interfaz aprobado.
- La interfaz de RF-01 a RF-27 está congelada hasta que el equipo apruebe ese alcance.
- Toda propuesta visual debe respetar los atributos `data-cy` que usa Cypress y las etiquetas de estado que provienen del backend (`present()`).
- No introduce dependencias: no se aceptan librerías de animación ni 3D por esta vía.
