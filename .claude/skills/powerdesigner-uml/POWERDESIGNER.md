# Llevar los modelos a PowerDesigner

PowerDesigner es una herramienta de escritorio con interfaz gráfica. **No se automatiza por defecto**: cada fase decide si se trabaja solo con artefactos intermedios y procedimientos manuales, o si se crean y editan modelos nativos. Esta guía cubre ambos casos.

## Reglas por fase

| Fase | Qué se hizo con PowerDesigner | Regla que deja |
|---|---|---|
| **Fase 22** · especificación | Nada: solo especificación UML y borradores PlantUML en `docs/v1.1/uml/`. Sin `.oom`, `.pdm` ni `.cdm`, y sin automatizar la herramienta | Una fase que solo especifica prepara artefactos intermedios y **no** toca PowerDesigner. Hasta la Fase 23 esta guía decía, en general, que PowerDesigner «no se automatiza desde este entorno» y que los `.oom`/`.pdm`/`.cdm` «no se generan aquí»: era la regla de esa etapa |
| **Fase 23** · formalización autorizada | Modelos nativos creados por PowerDesigner 16.6.1.5066 **automatizado por COM** (`PowerDesigner.Application`) desde PowerShell, con scripts versionados en `docs/v1.1/powerdesigner/scripts/`: OOM con los 19 diagramas de F22 más CL-01b, PDM por ingeniería inversa del esquema real, exportaciones PNG/SVG, validación visual y de conteos contra F22 | La automatización es válida cuando la fase la autoriza, parte de una línea base aprobada, deja todo respaldado en Git y se valida |
| **Después de la Fase 23** | — | Los modelos de `docs/v1.1/powerdesigner/models/` se **preservan**. Editarlos requiere autorización explícita; ver «Editar los modelos de v1.1» |

## Qué se puede generar desde el repositorio

| Artefacto | Viabilidad | Uso |
|---|---|---|
| `.puml` (PlantUML) | Alta | Borradores de especificación; versionables y revisables |
| Script SQL del esquema | Alta | Ingeniería inversa del modelo físico (PDM) |
| XMI del modelo de clases | Media | Importación del modelo orientado a objetos (OOM); depende de la versión de PowerDesigner |
| `.oom` / `.pdm` / `.cdm` | **Solo si la fase lo autoriza** (como la Fase 23) | Los crea y guarda PowerDesigner, a mano o por COM; **nunca se escriben a mano** ni se generan con otra herramienta |

## Automatización por COM (solo con autorización de la fase)

Condiciones, todas a la vez:

1. La fase autoriza expresamente crear o editar modelos nativos.
2. Existe una línea base aprobada que el modelo formaliza (hoy, la especificación de F22 en `docs/v1.1/uml/`).
3. Los modelos y exportaciones anteriores están versionados en Git antes de empezar.
4. El resultado se valida (exportaciones revisadas a ojo, conteos contra la fuente) y se registra.
5. No se destruye historia: ni los modelos de v1.0 ni los de la Fase 23 se sobrescriben por una reconstrucción completa.

Prácticas de la Fase 23 que se mantienen (detalle en `docs/v1.1/powerdesigner/README.md`):

- Modo *batch* (`InteractiveMode = 0`) durante el script y restaurado al terminar; guardar antes de cerrar; cerrar solo los modelos que abre el script.
- `scripts/tools/pd-status.ps1` antes de cada ejecución: `modelos abiertos: 0`.
- Scripts de comportamiento idempotentes: cada diagrama se reemplaza, sin copias. Los scripts que crean el modelo desde cero (`01`–`03`) **no** se vuelven a ejecutar sobre el modelo existente.
- Sin modelos de prueba (`zz_*`) ni copias de respaldo de PowerDesigner en el repositorio.

## Editar los modelos de v1.1

Después de la Fase 23, un cambio en un diagrama:

- necesita autorización explícita de la fase o del equipo;
- es **incremental**: se cambia el script de ese diagrama y se regenera solo él (`$env:PD_ONLY`), no el modelo entero;
- conserva la trazabilidad F22 ↔ PowerDesigner: si cambia la especificación, primero cambia `docs/v1.1/uml/` y después el modelo;
- se reexporta (PNG y SVG), se revisa y se anota en `docs/v1.1/powerdesigner/inventory.md` y, si aplica, en `f22-checklist.md`.

## Modelo físico por ingeniería inversa (recomendado)

1. Levanta el entorno y obtén el esquema real:

   ```
   docker compose up -d --wait
   docker compose exec postgres pg_dump -U <usuario> -d reclutamiento --schema-only --no-owner --no-privileges
   ```

   Guarda la salida como archivo `.sql` de trabajo **fuera del repositorio** si contiene algo específico del entorno; el esquema en sí no es un secreto, pero las credenciales sí: nunca las incluyas en el comando documentado ni en la salida versionada.

2. En PowerDesigner: *File → Reverse Engineer → Database*, elige PostgreSQL como DBMS y el script como origen. En la Fase 23 esto se hizo por COM con `scripts/pdm/` (DBMS *PostgreSQL 9.x*, el más reciente de la versión 16.6).
3. Validación obligatoria tras importar: número de tablas, FK presentes, `CHECK` de estados, índices, tipos y nombres. Anota el conteo real.
4. El diagrama conceptual (CDM) se deriva del PDM dentro de la herramienta; se ajustan manualmente los nombres de entidad en español si el informe lo requiere.

## Modelo de clases (OOM)

Si la versión de PowerDesigner disponible importa XMI:

1. Genera el XMI del modelo de clases a partir de las clases reales de `app/`.
2. *File → Import → XMI File*, seleccionando modelo orientado a objetos.
3. Verifica clases, atributos, tipos, visibilidad y asociaciones; corrige manualmente lo que la importación degrade.

Si no importa, o el resultado es incorrecto: **no insistas**. Documenta el procedimiento manual (crear el OOM, añadir las clases de la matriz de correspondencia, trazar asociaciones con sus cardinalidades). En la Fase 23 el OOM se construyó por COM a partir de la especificación de F22, sin XMI.

## Ajustes manuales habituales

- Renombrar en español para la presentación, conservando en una nota el nombre técnico real.
- Reubicar entidades para legibilidad; el diseño gráfico no cambia la semántica.
- Marcar los elementos `<<propuesto v1.1>>` con un color o estereotipo distinto de lo implementado.

## Registro

Cada importación o edición se registra con: artefacto de origen, versión de PowerDesigner, pasos ejecutados, resultado de la validación y ajustes manuales aplicados. Sin ese registro, el diagrama no es reproducible.

- **v1.0**: en el informe de diagramas correspondiente (`docs/final-report/diagram-reports/`), que no se reescribe.
- **v1.1**: en el documento de la fase (`docs/v1.1/phase-23-powerdesigner.md` para la formalización) y en `docs/v1.1/powerdesigner/inventory.md` y `f22-checklist.md`.
