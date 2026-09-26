# Procedencia — reviewing-a11y

Skill externa instalada localmente en la Fase 13. Los archivos son copia literal del origen (incluidas las versiones en japonés); se añadió el archivo `LICENSE` del repositorio de origen para conservar la atribución.

| Campo | Valor |
|---|---|
| Nombre | `reviewing-a11y` |
| Origen | https://github.com/masuP9/a11y-specialist-skills (carpeta `skills/reviewing-a11y`) |
| Propietario | Soichi Masuda (masuP9) (comunitaria) |
| Commit fijado | `6615e6eb0bfa994a2ac1b2e6edb8d3ccdf44c587` |
| Fecha del commit | 2026-09-15 |
| Licencia | MIT (`LICENSE`, © 2025 masuP9) |
| Tipo | Declarativa (Markdown + un `agents/openai.yaml` de 263 bytes) |
| Scripts / binarios / hooks | Ninguno dentro de la skill |
| Acceso de red | **Sí, declarado**: su `SKILL.md` lista `WebFetch` y herramientas MCP de Playwright en `allowed-tools` |
| Escritura fuera del repositorio | No |
| Riesgo | **MEDIO** (por la red y el navegador que declara) |
| Instalada | Sí, en `.claude/skills/reviewing-a11y/` |
| Auditada el | 2026-09-19 |

## Condición de uso (regla 8 de la Fase 13)

Los archivos instalados son inertes: no ejecutan nada por sí mismos. Aun así, **antes de usar sus flujos que requieren navegador o red hace falta autorización explícita del equipo**:

- `WebFetch` sobre URLs externas;
- herramientas MCP de Playwright (`browser_snapshot`, `browser_navigate`, `browser_click`), que necesitan un servidor MCP que **no está instalado ni configurado** en este proyecto.

Sin esa autorización, úsala solo en su modo de **revisión de código y de especificaciones**, que funciona con `Read`, `Grep` y `Glob` sobre el repositorio.

## Observación de la auditoría

El repositorio de origen incluye además un paquete ejecutable (`packages/a11y-audit`: Playwright, CLI y workflows de CI). **No se copió ni se instaló**: queda fuera del alcance de la Fase 13.

## Uso previsto

Revisión de accesibilidad de las pantallas existentes (RF-01 a RF-27), sobre todo formularios, estados, foco y contraste, como insumo para el informe académico.
