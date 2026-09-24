# Inventario de diagramas PowerDesigner (Fase 23)

PowerDesigner 16.6.1.5066. Archivos nativos en `models/`, exportaciones en `exports/` (PNG y SVG de cada diagrama). Los conteos salen del propio modelo (recorrido por COM de los símbolos de cada diagrama) y se contrastan con la especificación de F22 en [`f22-checklist.md`](f22-checklist.md).

**Validación**: «Visual + conteo» = exportación revisada a ojo (legibilidad, rutas, rótulos) y conteo de elementos igual al de la fuente de F22. Las observaciones cosméticas que quedan se listan al final.

| ID | Tipo | Modelo | Nombre en PowerDesigner | Archivo nativo | Exportación | RF | Elementos (del modelo) | Validación |
|---|---|---|---|---|---|---|---|---|
| PDM-01 | Physical Diagram | PDM | PDM-01 Esquema completo | `saas-recruitment-v1.1-pdm.pdm` | `PDM-01-esquema-completo.{png,svg}` | Datos de RF-01 a RF-27; `vacancies.target_completion_at` (RF-29) | 27 tablas, 48 referencias, 1 procedimiento (función del *trigger*) | Visual + conteo |
| PDM-02 | Physical Diagram | PDM | PDM-02 Tablas de dominio | `saas-recruitment-v1.1-pdm.pdm` | `PDM-02-tablas-de-dominio.{png,svg}` | Ídem | 17 tablas de dominio, 47 referencias | Visual + conteo |
| CL-01 | Class Diagram | OOM (`App\Models`) | CL-01 Clases del dominio | `saas-recruitment-v1.1-oom.oom` | `CL-01-clases-del-dominio.{png,svg}` | RF-01 a RF-27 (y RF-29 por `target_completion_at`) | 17 clases, 37 asociaciones, 7 notas | Visual + conteo |
| CL-01b | Class Diagram (vista auxiliar) | OOM (`App\Enums`) | CL-01b Enumeraciones | `saas-recruitment-v1.1-oom.oom` | `CL-01b-enumeraciones.{png,svg}` | Estados y valores de RF-01 a RF-27 | 10 enumeraciones, 1 nota | Visual + conteo |
| UC-01 | Use Case Diagram | OOM | UC-01 Casos de uso AS-IS v1.1 | `saas-recruitment-v1.1-oom.oom` | `UC-01-casos-de-uso.{png,svg}` | RF-01 a RF-29 (RF-28 candidato) | 6 actores, 29 casos, 26 asociaciones, 13 dependencias (12 `<<include>>`, 1 `<<extend>>`), 8 notas | Visual + conteo |
| PK-01 | Package Diagram | OOM (`Módulos del monolito`) | PK-01 Paquetes del monolito | `saas-recruitment-v1.1-oom.oom` | `PK-01-paquetes.{png,svg}` | RF-01 a RF-27 por módulo; RF-29 | 10 paquetes, 21 dependencias, 2 notas | Visual + conteo |
| CO-01 | Component Diagram | OOM | CO-01 Componentes AS-IS v1.1 | `saas-recruitment-v1.1-oom.oom` | `CO-01-componentes.{png,svg}` | RF-01 a RF-27; RF-29 | 20 componentes, 3 interfaces, 30 dependencias, 4 notas | Visual + conteo |
| DE-01 | Deployment Diagram | OOM | DE-01 Despliegue AS-IS v1.1 (desarrollo y demostración) | `saas-recruitment-v1.1-oom.oom` | `DE-01-despliegue.{png,svg}` | Infraestructura; RF-29 (servicio de inferencia fuera de Compose) | 6 nodos, 6 asociaciones de nodo, 9 archivos, 4 marcos de contenedor, 2 notas | Visual + conteo |
| SEQ-01 | Sequence Diagram | OOM | SEQ-01 Registrar postulación (RF-10, RF-11) | `saas-recruitment-v1.1-oom.oom` | `SEQ-01-registrar-postulacion.{png,svg}` | RF-10, RF-11 | 8 lifelines, 13 mensajes, 2 fragmentos (`critical`, `alt`), 1 nota | Visual + conteo |
| SEQ-02 | Sequence Diagram | OOM | SEQ-02 Aprobar o rechazar requerimiento (RF-03, RF-04) | `saas-recruitment-v1.1-oom.oom` | `SEQ-02-aprobar-rechazar-requerimiento.{png,svg}` | RF-03, RF-04 | 9 lifelines, 14 mensajes, 4 fragmentos (`alt`, `critical`, `alt`, `opt`) | Visual + conteo |
| SEQ-03 | Sequence Diagram | OOM | SEQ-03 Cambiar etapa y notificar (RF-13, RF-14, RF-15) | `saas-recruitment-v1.1-oom.oom` | `SEQ-03-cambiar-etapa.{png,svg}` | RF-13, RF-14, RF-15 | 9 lifelines, 13 mensajes, 2 fragmentos | Visual + conteo |
| SEQ-04 | Sequence Diagram | OOM | SEQ-04 Programar evaluación (RF-16, RF-17) | `saas-recruitment-v1.1-oom.oom` | `SEQ-04-programar-evaluacion.{png,svg}` | RF-16, RF-17 | 10 lifelines, 14 mensajes, 2 fragmentos | Visual + conteo |
| SEQ-05 | Sequence Diagram | OOM | SEQ-05 Programar y registrar entrevista (RF-18, RF-19) | `saas-recruitment-v1.1-oom.oom` | `SEQ-05-programar-registrar-entrevista.{png,svg}` | RF-18, RF-19 (RF-17, RF-20) | 12 lifelines, 20 mensajes, 3 fragmentos, 2 notas y 2 divisores de tramo | Visual + conteo |
| SEQ-06 | Sequence Diagram | OOM | SEQ-06 Calcular ranking y comparar (RF-20, RF-21, RF-22) | `saas-recruitment-v1.1-oom.oom` | `SEQ-06-ranking-comparacion.{png,svg}` | RF-20, RF-21, RF-22 | 8 lifelines, 16 mensajes, 1 fragmento, 2 notas | Visual + conteo |
| SEQ-07 | Sequence Diagram | OOM | SEQ-07 Registrar decisión final (RF-23) `<<human decision>>` | `saas-recruitment-v1.1-oom.oom` | `SEQ-07-decision-final.{png,svg}` | RF-23 | 9 lifelines, 13 mensajes, 3 fragmentos, 1 nota | Visual + conteo |
| SEQ-08 | Sequence Diagram | OOM | SEQ-08 Consultar riesgo operacional (RF-29) `<<experimental>>` | `saas-recruitment-v1.1-oom.oom` | `SEQ-08-riesgo-operacional.{png,svg}` | RF-29 | 10 lifelines, 22 mensajes, 3 fragmentos, 2 notas | Visual + conteo |
| AC-01 | Activity Diagram | OOM | AC-01 Proceso de reclutamiento AS-IS (RF-01 a RF-27) | `saas-recruitment-v1.1-oom.oom` | `AC-01-proceso-reclutamiento.{png,svg}` | RF-01 a RF-27 | 6 carriles, 26 actividades, 6 decisiones, 1 inicio, 2 fines de actividad, 2 fines de flujo (⊗), 39 flujos, 4 notas | Visual + conteo |
| AC-02 | Activity Diagram | OOM | AC-02 Consulta del riesgo operacional (RF-29) `<<experimental>>` | `saas-recruitment-v1.1-oom.oom` | `AC-02-riesgo-operacional.{png,svg}` | RF-29 | 10 actividades, 4 decisiones, 1 inicio, 2 fines, 19 flujos, 1 nota | Visual + conteo |
| ST-01 | Statechart Diagram | OOM (`ST-01`) | ST-01 Estados del requerimiento (JobRequestStatus) | `saas-recruitment-v1.1-oom.oom` | `ST-01-estados-requerimiento.{png,svg}` | RF-01 a RF-04 | 6 estados, 9 transiciones (con inicio y fin), 2 notas | Visual + conteo |
| ST-02 | Statechart Diagram | OOM (`ST-02`) | ST-02 Estados de la vacante (VacancyStatus) | `saas-recruitment-v1.1-oom.oom` | `ST-02-estados-vacante.{png,svg}` | RF-05 a RF-07, RF-25 | 3 estados, 4 transiciones, 1 nota | Visual + conteo |
| ST-03 | Statechart Diagram | OOM (`ST-03`) | ST-03 Estados de la postulación (ApplicationStatus) | `saas-recruitment-v1.1-oom.oom` | `ST-03-estados-postulacion.{png,svg}` | RF-10, RF-13 a RF-16, RF-18, RF-24, RF-25 | 8 estados, 21 transiciones, 2 notas | Visual + conteo |
| ST-04 | Statechart Diagram | OOM (`ST-04`) | ST-04 Estados de evaluación y entrevista (AssessmentStatus) | `saas-recruitment-v1.1-oom.oom` | `ST-04-estados-sesion.{png,svg}` | RF-16, RF-18, RF-19 | 2 estados, 3 transiciones, 1 nota | Visual + conteo |

**Totales del OOM**: 27 clases (17 del dominio y 10 enumeraciones), 37 asociaciones, 6 actores, 29 casos de uso, 20 componentes, 6 nodos, 40 objetos de secuencia, 125 mensajes, 20 fragmentos, 36 actividades, 10 decisiones, 58 flujos, 6 unidades organizativas, 19 estados, 37 transiciones y 23 eventos. **Sin objetos de prueba (`zz_*`) ni diagramas vacíos.**

**Cobertura de la F22**: los 19 diagramas especificados (CL-01, ST-01 a ST-04, UC-01, PK-01, CO-01, DE-01, SEQ-01 a SEQ-08, AC-01, AC-02) más una vista auxiliar (CL-01b) y dos diagramas físicos (PDM-01, PDM-02): 22 en total.

## Observaciones cosméticas que quedan

No cambian ningún dato del modelo; el texto completo está en el objeto.

- **SEQ, fragmentos `critical`**: la pestaña del operador tapa el corchete inicial de la guarda (`DB::transaction]`). La guarda lleva espacios delante para que el texto quede visible.
- **SEQ-08**: la guarda «fuera de alcance» toca el comienzo del rótulo del primer mensaje del operando.
- **AC-01**: en los tramos más cortos (`¿Aprobar?` → «Rechazar», `¿Preseleccionar?` → «Descartar», `¿Más sesiones?` → `¿Postulación descartada?`) la punta de la flecha roza el rótulo `[no]` / `[sí]`.
- **Rótulos largos**: PowerDesigner parte algunas líneas por su cuenta, a veces con un paréntesis solo en la línea siguiente.
