# Checklist F22 ↔ PowerDesigner (Fase 23)

Cada diagrama de PowerDesigner contra su especificación de la Fase 22 (`docs/v1.1/uml/`, sin cambios desde `4219c11`). Estados:

- **MATCH**: mismos elementos, relaciones, rótulos y notas que la fuente.
- **JUSTIFIED DIFFERENCE**: una diferencia de representación que impone la herramienta o la notación, sin cambiar el significado. Se explica abajo.
- **DIFFERENCE**: diferencia de contenido sin justificar. **No hay ninguna.**

| ID | Fuente F22 | Diagrama PowerDesigner | Estado | Diferencias |
|---|---|---|---|---|
| CL-01 | `class-model.md` · `puml/cl-01-domain.puml` | CL-01 Clases del dominio (`App\Models`) | JUSTIFIED DIFFERENCE | J-01, J-02, J-03, O-01 |
| — | `class-model.md` §enums | CL-01b Enumeraciones (`App\Enums`) | JUSTIFIED DIFFERENCE | J-04 |
| ST-01 | `state-diagrams.md` · `puml/st-01-job-request.puml` | ST-01 Estados del requerimiento | JUSTIFIED DIFFERENCE | J-20, J-21 |
| ST-02 | `state-diagrams.md` · `puml/st-02-vacancy.puml` | ST-02 Estados de la vacante | JUSTIFIED DIFFERENCE | J-20, J-21 |
| ST-03 | `state-diagrams.md` · `puml/st-03-application.puml` | ST-03 Estados de la postulación | JUSTIFIED DIFFERENCE | J-20, J-21, J-22 |
| ST-04 | `state-diagrams.md` · `puml/st-04-assessment.puml` | ST-04 Estados de evaluación y entrevista | JUSTIFIED DIFFERENCE | J-20, J-21 |
| UC-01 | `use-cases.md` · `puml/uc-01-use-cases.puml` | UC-01 Casos de uso AS-IS v1.1 | JUSTIFIED DIFFERENCE | J-05, J-06 |
| PK-01 | `component-model.md` §3 · `puml/pk-01-packages.puml` | PK-01 Paquetes del monolito | JUSTIFIED DIFFERENCE | J-05 |
| CO-01 | `component-model.md` §1–2 · `puml/co-01-components.puml` | CO-01 Componentes AS-IS v1.1 | JUSTIFIED DIFFERENCE | J-05 |
| DE-01 | `deployment-model.md` · `puml/de-01-deployment.puml` | DE-01 Despliegue AS-IS v1.1 | JUSTIFIED DIFFERENCE | J-05, J-07, J-08 |
| SEQ-01 | `sequence-diagrams.md` · `puml/seq-01-apply.puml` | SEQ-01 Registrar postulación | MATCH | Cosmética C-01 |
| SEQ-02 | `sequence-diagrams.md` · `puml/seq-02-decide-job-request.puml` | SEQ-02 Aprobar o rechazar requerimiento | MATCH | Cosmética C-01 |
| SEQ-03 | `sequence-diagrams.md` · `puml/seq-03-change-stage.puml` | SEQ-03 Cambiar etapa y notificar | MATCH | Cosmética C-01 |
| SEQ-04 | `sequence-diagrams.md` · `puml/seq-04-schedule-evaluation.puml` | SEQ-04 Programar evaluación | MATCH | Cosmética C-01 |
| SEQ-05 | `sequence-diagrams.md` · `puml/seq-05-interview.puml` | SEQ-05 Programar y registrar entrevista | JUSTIFIED DIFFERENCE | J-11 |
| SEQ-06 | `sequence-diagrams.md` · `puml/seq-06-ranking.puml` | SEQ-06 Calcular ranking y comparar | JUSTIFIED DIFFERENCE | J-10 |
| SEQ-07 | `sequence-diagrams.md` · `puml/seq-07-final-decision.puml` | SEQ-07 Registrar decisión final `<<human decision>>` | MATCH | Cosmética C-01 |
| SEQ-08 | `sequence-diagrams.md` · `puml/seq-08-operational-risk.puml` | SEQ-08 Consultar riesgo operacional `<<experimental>>` | JUSTIFIED DIFFERENCE | J-10 |
| AC-01 | `activity-diagrams.md` · `puml/ac-01-recruitment.puml` | AC-01 Proceso de reclutamiento AS-IS | JUSTIFIED DIFFERENCE | J-12, J-13, J-14 |
| AC-02 | `activity-diagrams.md` · `puml/ac-02-operational-risk.puml` | AC-02 Consulta del riesgo operacional `<<experimental>>` | JUSTIFIED DIFFERENCE | J-15 |
| — | Esquema real (no forma parte de F22) | PDM-01 y PDM-02 | JUSTIFIED DIFFERENCE | J-30, J-31, J-32 |

Todas las secuencias usan objetos reutilizados por nombre en todo el modelo (J-09); eso no cambia lo que muestra cada diagrama.

## Comprobaciones de contenido

| Comprobación | Resultado |
|---|---|
| Mensajes de SEQ-01 a SEQ-08 transcritos de los `.puml` de F22, en orden y con sus fragmentos | 125 mensajes (13 + 14 + 13 + 14 + 20 + 16 + 13 + 22) y 20 fragmentos, igual que la fuente. No se inventó ningún mensaje |
| SEQ-07: decisión humana | La persona elige, justifica y confirma. Nota: «puede no ser la primera del ranking… Sin ningún mensaje al servicio de riesgo operacional». Ningún mensaje hacia el ML |
| SEQ-08: contrato del ML | `{15 features; sin IDs ni PII}`; la nota dice «La respuesta no incluye incertidumbre» y «Ningún mensaje hacia ranking, comparación ni decisión final». `<<experimental>>` en el nombre y en las lifelines de FastAPI y del predictor |
| AC-01: descarte terminal | Los dos descartes (preselección y tras las sesiones) terminan en un **fin de flujo** ⊗ «fin de esta postulación». La rama no descartada pasa a `finalista` y sigue. Una descartada no llega a la comparación (RF-21, RF-22) ni a la decisión (RF-23). Solo el rechazo del requerimiento y el cierre usan fin de actividad. Nota de los dos niveles |
| AC-01: decisión humana | La actividad de RF-23 lleva `<<human decision>>` y está en el carril del Aprobador / Dirección |
| AC-02 | Tres desenlaces con los valores reales de `RiskAvailability` (`descriptive_only`, `unavailable`, `predictive_available`), fin sin efectos, ninguna rama hacia selección |
| ST-01 a ST-04 | Solo las transiciones de F22 (9, 4, 21 y 3, contando inicio y fin). **Ninguna transición nueva.** Estados con su valor real (`en_evaluacion`, `no_seleccionado`…). Notas de A-28, A-30 (`desierta`), RF-24 y RF-15/RF-26 |
| RF-28 | UC-RF28 `<<propuesto v1.1>>` sin asociaciones; no aparece como implementado en ningún diagrama |
| RF-29 | Experimental en UC-01, CO-01, PK-01, DE-01, SEQ-08 y AC-02; sin relación con ranking ni decisión |

## Diferencias justificadas

| # | Diagrama | Diferencia | Por qué |
|---|---|---|---|
| J-01 | CL-01 | Atributos con su nombre real; solo los que toman valores de un enum llevan ese tipo (p. ej. `action : AuditAction`), los demás van sin tipo de dato | La especificación de F22 fija nombres, multiplicidades y reglas; los tipos físicos están en el PDM, que sale del esquema real y no se duplica a mano |
| J-02 | CL-01 | La fila 2 de la tabla de asociaciones («`Organization` 1 — 0..* `JobRequest`, `Vacancy` y demás `<<T>>`», tipo «Asociación (nota)») se dibuja como dos asociaciones (`JobRequest` y `Vacancy`) más la nota del aislamiento | Es la regla de F22: solo se dibujan las asociaciones con `Organization` de `User`, `JobRequest`, `Vacancy` y `AuditLog`; las demás clases heredan el aislamiento y lo explica una nota. Sigue habiendo 37 asociaciones |
| J-03 | CL-01 | La fila 35 («`AuditLog` → entidad auditada», polimórfica) va como nota y no como dependencia | «Entidad auditada» no es una clase: la relación es polimórfica (`auditable_type` + `auditable_id`). Una dependencia necesitaría un destino inexistente |
| J-04 | CL-01b | Las enumeraciones van en una vista auxiliar en el paquete `App\Enums`, fuera de CL-01 | Con 17 clases y 37 asociaciones, CL-01 no admite 10 enumeraciones más sin perder legibilidad; F22 las describe en su propia sección |
| J-05 | UC-01, PK-01, CO-01, DE-01 | Las dependencias sin rótulo en F22 llevan por nombre un espacio | PowerDesigner rechaza el nombre vacío y, al mostrar los nombres (necesario para ver las etiquetas de F22), enseñaría `Dependency_N` |
| J-06 | UC-01 | Quedan cruces menores entre asociaciones de actores | 6 actores y 29 casos en un solo diagrama; se priorizó agrupar los casos por módulo como en F22 |
| J-07 | DE-01 | Los contenedores de F22 (equipo del usuario, equipo anfitrión, Docker Engine y el contenedor `app`) son marcos gráficos con su estereotipo en el título, no nodos anidados | PowerDesigner no dibuja asociaciones entre nodos anidados, y las comunicaciones entre contenedores son el contenido principal de DE-01. Los artefactos van junto al nodo que los ejecuta |
| J-08 | DE-01 | Los nombres de los artefactos no llevan `/` ni `:` (p. ej. «public-build», «storage-app-private (CV)») | PowerDesigner no admite esos caracteres en el nombre de un objeto *File*; la ruta o la orden exactas (`public/build`, `storage/app/private`, `php artisan queue:work redis …`) quedan en el comentario de cada artefacto |
| J-09 | SEQ-01 a SEQ-08 | Cada objeto de secuencia existe una sola vez en el modelo y cada diagrama lo reutiliza por nombre; los actores son los de UC-01 | PowerDesigner exige nombres únicos por espacio de nombres |
| J-10 | SEQ-06, SEQ-08 | El actor de F22 «RR. HH. / Aprobador» es la lifeline «Recursos Humanos», con una nota que dice que el Aprobador / Dirección ejecuta el mismo flujo y con qué método de `VacancyPolicy` | Las lifelines de actor son los actores de UC-01, donde RR. HH. y el Aprobador son dos actores distintos. La nota conserva que ambos pueden hacerlo |
| J-11 | SEQ-05 | Los separadores `== A · Programar (RR. HH.) ==` y `== B · Registrar resultado (Evaluador asignado) ==` son notas a la izquierda, a la altura de su tramo | PowerDesigner no tiene separadores de tramo en el diagrama de secuencia |
| J-12 | AC-01 | Los seis carriles son marcos gráficos con cabecera; la partición está en el modelo, porque cada actividad y decisión lleva su carril en el atributo `OrganizationUnit` | PowerDesigner 16.6 agrupa los carriles nativos en un solo símbolo que se redimensiona solo al colocar los nodos; por COM no se consigue fijar el ancho de cada carril |
| J-13 | AC-01 | Las actividades que el borrador repite llevan el estado de destino real o el RF del paso: «Notificar cambio de etapa: descartado / preseleccionado / descartado tras las sesiones / finalista (RF-15)», «Descartar con comentario (RF-13)» y «(RF-14)»; los fines de flujo, «fin de esta postulación (descarte en preselección / tras las sesiones)» | PowerDesigner exige nombres únicos. Los añadidos son los estados reales (ST-03) y los RF de la tabla de F22 |
| J-14 | AC-01 | Los comentarios de nivel del borrador (`' ---- Desde aquí, por cada postulación ----`) son notas visibles en el carril del Área solicitante | F22 pide «añadir la nota de los dos niveles»; así se ve dónde empieza y termina el tramo por postulación |
| J-15 | AC-02 | Las ramas que siguen llevan `[sí]` (en el borrador son el `else` implícito), el acceso denegado es la actividad «403» con su fin, y las tres salidas no predictivas llegan a «Mostrar tarjeta» por rutas separadas, sin nodo de fusión | Mismo flujo que el borrador; en PowerDesigner cada flujo necesita su rótulo y su destino explícitos |
| J-20 | ST-01 a ST-04 | Cada diagrama está en su propio paquete `ST-01` … `ST-04` | `borrador` es un estado real del requerimiento y de la vacante; en paquetes distintos cada estado conserva su valor real, sin sufijos |
| J-21 | ST-01 a ST-04 | Transición = evento `[guarda]` `/ efecto` (evento, `ConditionAlias` y `TriggerAction`). El paréntesis de actor y RF del borrador va con el evento: «observe (RR. HH., RF-02) [comentario]» en lugar de «observe [comentario] (RR. HH., RF-02)». Los eventos repetidos (`discard`, `close`, `moveTo (RF-14)`) son un único evento del paquete | Es la notación UML que PowerDesigner dibuja; el texto es el mismo. Inicio y fin llevan nombre («Inicio ST-01», «Fin ST-01») porque PowerDesigner lo exige; no se muestra |
| J-22 | ST-03 | `descartado` y `no_seleccionado` son estados altos a los lados, y cada estado activo les llega con una transición horizontal. Las transiciones que saltan un estado van por carriles laterales | Son 10 transiciones hacia dos estados finales; así ninguna cruza el eje principal y cada rótulo queda junto a su origen |
| J-30 | PDM | DBMS *PostgreSQL 9.x* | PowerDesigner 16.6 no trae un DBMS más reciente. La base real es PostgreSQL 17.11 |
| J-31 | PDM | El lector PG9 conserva un solo CHECK por tabla; se restituyen los 32 como una conjunción (`AND`) en la expresión de la tabla, con sus nombres en el comentario | Es lógicamente equivalente a los CHECK separados |
| J-32 | PDM | El índice único parcial `applications_one_selected_per_vacancy` pierde su `WHERE`; se registra en el comentario del índice | El lector PG9 no conserva la cláusula. Regla de negocio (RF-24): como mucho una postulación `seleccionado` por vacante |

## Observación (sin cambio)

| # | Observación |
|---|---|
| O-01 | `evaluation_criteria.position` existe en el esquema (PDM) y no figura entre los atributos de `EvaluationCriterion` en la especificación de F22. CL-01 sigue a F22; se deja anotado para una revisión de la especificación, no se corrige en esta fase |

## Cosmética

| # | Diagramas | Detalle |
|---|---|---|
| C-01 | SEQ con `critical` | La pestaña del operador tapa el corchete inicial de la guarda; el texto `DB::transaction` se ve completo |
