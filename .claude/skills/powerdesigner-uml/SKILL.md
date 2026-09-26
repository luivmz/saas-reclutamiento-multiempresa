---
name: powerdesigner-uml
description: Derivación de diagramas UML a partir del código real del proyecto y su formalización en PowerDesigner. Úsala al crear o revisar diagramas de casos de uso, clases, secuencia, componentes, despliegue o el modelo de datos, al producir PlantUML o artefactos intermedios, y al tocar los modelos nativos de PowerDesigner (.oom/.pdm) de v1.1. Prohíbe inventar actores, clases, componentes o tablas, y modificar modelos nativos sin autorización de la fase.
---

# UML derivado del código real

Un diagrama de este proyecto es una **lectura** del sistema, no un dibujo aspiracional. Todo elemento representado debe existir hoy en el repositorio, o estar marcado explícitamente como propuesta de v1.1.

## 1. Extraer antes de dibujar

Antes de escribir una línea de PlantUML, recoge la fuente:

| Diagrama | De dónde sale |
|---|---|
| Casos de uso | `routes/web.php` + `EnsureUserHasRole` + Policies → actores = roles reales; casos = rutas con nombre |
| Clases | `app/Models`, `app/Enums`, `app/Services`, `app/Policies` (atributos y relaciones reales) |
| Secuencia | El recorrido real: ruta → middleware → Form Request → Controller → Policy → Service → Modelo → auditoría/notificación |
| Componentes | Módulos de `app/` + frontend Inertia/React + servicios de `docker-compose.yml` |
| Despliegue | `docker-compose.yml` y `Dockerfile` (app, queue, postgres, redis, y el perfil e2e) |
| Modelo de datos | `database/migrations` (tablas, columnas, FK, `CHECK`, índices), no la imaginación |

Los actores del sistema son exactamente los roles que existen: Solicitante, Recursos Humanos, Aprobador, Evaluador y Postulante. No agregues "Administrador del sistema" ni "Gerente" si no están en el código.

## 2. Producir PlantUML

- Un archivo `.puml` por diagrama, con nombre trazable (`use-cases.puml`, `class-model.puml`, `sequence-rf23-decision.puml`).
- Nombres de clases, métodos y tablas **idénticos** a los del código.
- Cardinalidades tomadas de las relaciones Eloquent y las FK, no supuestas.
- Los elementos propuestos de v1.1 se marcan visiblemente (nota o estereotipo `<<propuesto v1.1>>`) y se listan aparte.
- Nada de rutas absolutas ni de datos personales en las etiquetas.

## 3. Matriz de correspondencia

Cada diagrama se acompaña de una tabla que justifica su contenido:

| Elemento del diagrama | Artefacto real | Ubicación | RF |
|---|---|---|---|
| `VacancyClosureService.close()` | Servicio | `app/Services/...:NN` | RF-25 |

Esta matriz es la defensa del diagrama en la sustentación: sin ella, el diagrama es una opinión.

## 4. Llevarlo a PowerDesigner

Qué se puede hacer con PowerDesigner **depende de la fase**, no de esta skill. Detalles operativos: [POWERDESIGNER.md](POWERDESIGNER.md).

| Momento | Regla |
|---|---|
| **Fase 22** (especificación UML del AS-IS, cerrada) | Solo especificación y borradores PlantUML en `docs/v1.1/uml/`. **No se generaron ni editaron archivos `.oom`, `.pdm` o `.cdm`** ni se automatizó PowerDesigner. Es la regla que tenía esta sección hasta la Fase 23 («no se editan ni se generan… en esta fase») y sigue valiendo para cualquier fase que solo especifique |
| **Fase 23** (formalización, autorizada expresamente) | Se crearon los modelos nativos de v1.1 (`docs/v1.1/powerdesigner/models/`: un OOM con los 19 diagramas de F22 más CL-01b, y un PDM por ingeniería inversa del esquema real) **automatizando PowerDesigner 16.6 por COM desde PowerShell**, con scripts versionados, exportaciones PNG/SVG, validación visual y de conteos contra F22 y registro en `docs/v1.1/phase-23-powerdesigner.md` |
| **Después de la Fase 23** | Los modelos nativos se **preservan**. Solo se modifican con **autorización explícita** de la fase o del equipo, de forma **incremental** (el script del diagrama afectado, no una reconstrucción completa), manteniendo la trazabilidad F22 ↔ PowerDesigner, reexportando y revalidando, y registrando el cambio en el inventario |

En cualquier fase:

- Genera XMI o un script SQL de ingeniería inversa **solo** si puede validarse tras la importación. Si no es viable, documenta el procedimiento manual paso a paso en lugar de forzar un archivo dudoso.
- La automatización por COM **no es la opción por defecto**: se usa solo si la fase la autoriza, hay una línea base aprobada (la especificación de F22 o su sucesora), los modelos y exportaciones previos están respaldados en Git y el resultado se valida.
- Tras cualquier importación o edición, valida en PowerDesigner: conteo de entidades, FK conservadas, cardinalidades, actores, relaciones, nombres y tipos. Registra el resultado de la validación.
- Los modelos de v1.0 se preservan como están.

## 5. Prohibiciones

- No inventes actores, clases, atributos, componentes, tablas ni relaciones.
- No presentes como existente algo que solo es una propuesta.
- No recrees los diagramas de v1.0 desde cero: si difieren del código, documenta la diferencia en `docs/v1.1/documentation-update-map.md`.
- No incluyas datos personales reales en ejemplos ni en instancias del modelo.
- No modifiques modelos nativos (`.oom`, `.pdm`, `.cdm`) sin autorización de la fase, ni borres o sobrescribas modelos históricos: los de v1.0 y los de la Fase 23 son evidencia.
- No reinterpretes la especificación de F22 ni uses PowerDesigner como ocasión para rediseñar: la herramienta formaliza lo especificado; una diferencia de representación se justifica por escrito, una de contenido no se admite.
