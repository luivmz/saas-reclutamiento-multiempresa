# Llevar los modelos a PowerDesigner

PowerDesigner es una herramienta de escritorio con interfaz gráfica: no se automatiza desde este entorno. Lo que sí se puede preparar son artefactos intermedios correctos y un procedimiento manual reproducible.

## Qué se puede generar desde el repositorio

| Artefacto | Viabilidad | Uso |
|---|---|---|
| `.puml` (PlantUML) | Alta | Fuente de los diagramas del informe; versionable y revisable |
| Script SQL del esquema | Alta | Ingeniería inversa del modelo físico (PDM) |
| XMI del modelo de clases | Media | Importación del modelo orientado a objetos (OOM); depende de la versión de PowerDesigner |
| `.oom` / `.pdm` / `.cdm` | No se generan aquí | Se crean y editan solo en la herramienta |

## Modelo físico por ingeniería inversa (recomendado)

1. Levanta el entorno y obtén el esquema real:

   ```
   docker compose up -d --wait
   docker compose exec postgres pg_dump -U <usuario> -d reclutamiento --schema-only --no-owner --no-privileges
   ```

   Guarda la salida como archivo `.sql` de trabajo **fuera del repositorio** si contiene algo específico del entorno; el esquema en sí no es un secreto, pero las credenciales sí: nunca las incluyas en el comando documentado ni en la salida versionada.

2. En PowerDesigner: *File → Reverse Engineer → Database*, elige PostgreSQL como DBMS y el script como origen.
3. Validación obligatoria tras importar: número de tablas, FK presentes, `CHECK` de estados, índices, tipos y nombres. Anota el conteo real.
4. El diagrama conceptual (CDM) se deriva del PDM dentro de la herramienta; se ajustan manualmente los nombres de entidad en español si el informe lo requiere.

## Modelo de clases (OOM)

Si la versión de PowerDesigner disponible importa XMI:

1. Genera el XMI del modelo de clases a partir de las clases reales de `app/`.
2. *File → Import → XMI File*, seleccionando modelo orientado a objetos.
3. Verifica clases, atributos, tipos, visibilidad y asociaciones; corrige manualmente lo que la importación degrade.

Si no importa, o el resultado es incorrecto: **no insistas**. Documenta el procedimiento manual (crear el OOM, añadir las clases de la matriz de correspondencia, trazar asociaciones con sus cardinalidades) y deja PlantUML como fuente de verdad del informe.

## Ajustes manuales habituales

- Renombrar en español para la presentación, conservando en una nota el nombre técnico real.
- Reubicar entidades para legibilidad; el diseño gráfico no cambia la semántica.
- Marcar los elementos `<<propuesto v1.1>>` con un color o estereotipo distinto de lo implementado.

## Registro

Cada importación se registra en el informe de diagramas correspondiente (`docs/final-report/diagram-reports/`) con: artefacto de origen, versión de PowerDesigner, pasos ejecutados, resultado de la validación y ajustes manuales aplicados. Sin ese registro, el diagrama no es reproducible.
