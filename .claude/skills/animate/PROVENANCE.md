# Procedencia — animate

Skill externa instalada localmente en la Fase 13. `SKILL.md` y `RECIPES.md` son copia literal del origen; se añadió el archivo `LICENSE` del repositorio de origen para conservar la atribución.

| Campo | Valor |
|---|---|
| Nombre | `animate` |
| Origen | https://github.com/emilkowalski/skills (carpeta `skills/animate`) |
| Propietario | Emil Kowalski (comunitaria) |
| Commit fijado | `85e8e2363b713506e1d5b6e07a0eb2da66be1bc3` |
| Fecha del commit | 2026-09-15 |
| Licencia | MIT (`LICENSE`, © 2026 Emil Kowalski) |
| Tipo | Declarativa (solo Markdown) |
| Scripts / binarios / hooks | Ninguno |
| Acceso de red | No |
| Escritura fuera del repositorio | No |
| Riesgo | **BAJO** |
| Instalada | Sí, en `.claude/skills/animate/` |
| Auditada el | 2026-09-19 |

## Observación de la auditoría

El repositorio de origen contiene un archivo suelto llamado `.pl` en su raíz. Se verificó que está **vacío (0 bytes)** y no se copió.

## Uso previsto

Criterio de movimiento para decidir **si** una interacción debe animarse y, en tal caso, con qué propiedades, curva y duración.

## Límites en este proyecto

- **No autoriza instalar Motion, Framer Motion, GSAP ni ninguna dependencia**: eso requiere una decisión y autorización explícitas del equipo.
- Prohibido animar ranking, comparación de candidatos, decisión final, auditoría y pantallas administrativas.
- Toda animación debe respetar `prefers-reduced-motion` y nunca puede retrasar una acción de negocio.
