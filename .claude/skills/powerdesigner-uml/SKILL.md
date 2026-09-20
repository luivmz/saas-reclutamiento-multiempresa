---
name: powerdesigner-uml
description: Derivación de diagramas UML a partir del código real del proyecto y preparación de su importación en PowerDesigner. Úsala al crear o revisar diagramas de casos de uso, clases, secuencia, componentes, despliegue o el modelo de datos, y al producir PlantUML o artefactos intermedios. Prohíbe inventar actores, clases, componentes o tablas.
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

La importación automática es útil solo cuando es viable y verificable. Detalles y pasos manuales: [POWERDESIGNER.md](POWERDESIGNER.md).

- Genera XMI o un script SQL de ingeniería inversa **solo** si puede validarse tras la importación.
- Si no es viable, documenta el procedimiento manual paso a paso en lugar de forzar un archivo dudoso.
- **No se editan ni se generan archivos `.oom`, `.pdm` o `.cdm` en esta fase**; los modelos de v1.0 se preservan como están.
- Tras cualquier importación, valida en PowerDesigner: conteo de entidades, FK conservadas, cardinalidades, nombres y tipos. Registra el resultado de la validación.

## 5. Prohibiciones

- No inventes actores, clases, atributos, componentes, tablas ni relaciones.
- No presentes como existente algo que solo es una propuesta.
- No recrees los diagramas de v1.0 desde cero: si difieren del código, documenta la diferencia en `docs/v1.1/documentation-update-map.md`.
- No incluyas datos personales reales en ejemplos ni en instancias del modelo.
