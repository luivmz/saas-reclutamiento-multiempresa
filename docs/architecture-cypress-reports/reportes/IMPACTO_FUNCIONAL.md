# Análisis del impacto funcional del módulo de reportes

> Actividad 5.3 de la guía. Este documento separa de forma explícita los **resultados medidos** (hechos verificados por ejecución) de los **beneficios potenciales** (hipótesis que requieren validación institucional). El proyecto mantiene un AS-IS **preliminar, pendiente de validación** con RR. HH. y Administración del Colegio Andino ([`F2_Analisis_del_Proceso_Colegio_Andino.md`](../../academico/practica-02/F2_Analisis_del_Proceso_Colegio_Andino.md), observación O-07). Por eso **no** se presentan reducciones de tiempo, costo ni esfuerzo atribuibles al software.

## 1. ¿Qué problema busca solucionar el software?

La plataforma digitaliza el reclutamiento y la selección de personal de una institución educativa (caso de estudio: Colegio Andino de Huancayo) en un SaaS multiempresa. El informe v1.0 identifica cinco problemas del proceso ([`docs/final-report/02-contexto-problema.md`](../../final-report/02-contexto-problema.md) §2.2), todos rotulados «pendiente de validación»:

| ID | Problema | Consecuencia |
|---|---|---|
| P1 | Información distribuida | Expediente difícil de reconstruir |
| P2 | Seguimiento manual, sin estados ni historial | Poca visibilidad del avance |
| P3 | Evaluaciones heterogéneas | Comparaciones poco objetivas |
| P4 | Comunicación manual | Demoras u omisiones |
| **P5** | **Indicadores limitados** | **Decisiones con menos sustento y baja capacidad de auditoría** |

El mismo informe declara un **«límite honesto sobre P5»**: «No se implementaron tableros de indicadores de gestión (tiempos del proceso, embudo de postulaciones ni estadísticas por periodo)». Los dejó como recomendación. El módulo de reportes (RF-28 candidato) es la respuesta directa a ese límite.

## 2. ¿Qué información permite visualizar el módulo de reportes?

Para la organización del usuario y el período y vacante elegidos (la etapa limita las postulaciones, no el conteo de vacantes publicadas):

- volumen de postulaciones recibidas y de vacantes publicadas;
- promedio de postulaciones por vacante;
- cuántas postulaciones llegaron a la preselección y en qué proporción;
- cuántas están ahora en evaluación o entrevista;
- tiempo promedio entre la postulación y la preselección registrada;
- distribución de las postulaciones por etapa actual (embudo del proceso);
- evolución semanal de las postulaciones;
- detalle por vacante (postulaciones, preseleccionadas, tasa y etapa de evaluación).

Todo sale de registros almacenados (`applications`, `application_stage_histories`, `vacancies`) y **nada identifica a personas**.

## 3. ¿Qué indicadores permiten evaluar los resultados del proceso?

| Indicador | Qué evalúa del proceso | Relación con los problemas |
|---|---|---|
| Postulaciones recibidas y promedio por vacante | Alcance de la convocatoria: si una vacante atrae suficientes postulantes | P5 (información consolidada) |
| Vacantes publicadas en el período | Carga de trabajo de RR. HH. | P2, P5 |
| Tasa de preselección | Ajuste entre el perfil publicado y quienes postulan: una tasa muy baja sugiere un perfil mal comunicado | P3, P5 |
| En evaluación o entrevista | Trabajo pendiente de los evaluadores | P2 |
| Tiempo promedio hasta la preselección | Rapidez de la primera revisión de RR. HH., la etapa donde se acumulan los postulantes | P2, P5 |
| Distribución por etapa | Dónde se concentran las postulaciones (posible cuello de botella) | P2, P5 |
| Postulaciones por semana | Picos de demanda tras publicar | P5 |

## 4. ¿Cómo facilita el software la toma de decisiones?

- **RR. HH.** puede priorizar la revisión de las vacantes con más postulaciones sin preselección, detectar convocatorias con poca respuesta para reforzar la difusión y anticipar la carga de evaluaciones y entrevistas.
- **Dirección (Aprobador)** obtiene una visión consolidada de su organización sin pedir reportes manuales, coherente con su rol de supervisión y auditoría (RF-27).
- Las decisiones que apoya son **de gestión del proceso**. El módulo no recomienda, ordena ni descarta personas; la decisión de selección sigue siendo humana y justificada (RF-23).

## 5. ¿Qué actividades o procesos pueden optimizarse?

Las actividades del AS-IS preliminar ([`F2`](../../academico/practica-02/F2_Analisis_del_Proceso_Colegio_Andino.md) §7) que la información generada puede apoyar:

| Actividad / observación | Cómo puede ayudar el reporte |
|---|---|
| O-02: avance controlado sin estados sistematizados | La distribución por etapa y los KPI de avance muestran el estado agregado sin consultar expediente por expediente |
| O-05: sin información consolidada | Los KPI y la tabla por vacante consolidan la información por período |
| Revisión inicial de postulaciones (preselección) | El tiempo promedio hasta la preselección hace visible la demora de esta etapa |
| Planificación de evaluaciones y entrevistas | El conteo «en evaluación o entrevista» anticipa la carga de los evaluadores |
| Difusión de convocatorias | Postulaciones por vacante y por semana muestran qué convocatorias necesitan más difusión |

## 6. Resultados medidos (hechos verificados)

Son los únicos resultados que esta práctica puede afirmar. Todos son técnicos o funcionales y se obtuvieron por ejecución:

| # | Resultado medido | Evidencia |
|---|---|---|
| M-1 | El módulo calcula los 6 KPI, 2 gráficos y la tabla desde la base de datos; con un conjunto controlado de registros los valores coinciden exactamente con los esperados (por ejemplo 5 postulaciones, tasa 80 %, 2,0 días promedio) | `RecruitmentReportTest::test_rf28_indicators_are_calculated_from_stored_records` y `…charts_and_table…` (GREEN) |
| M-2 | Con los datos de demostración (`DemoSeeder`), la organización A muestra 9 postulaciones, 3 vacantes publicadas, 8 preselecciones (88,9 %) y 1 en evaluación; la organización B muestra 1 postulación | Cypress `e2e-20-reports` (escenario 1 y 6) y capturas `E2E-20-01`, `E2E-20-06` |
| M-3 | El reporte refleja de inmediato un cambio registrado en el sistema: al preseleccionar una postulación desde la UI, el KPI pasa de 8 a 9 (100 %) | Cypress `e2e-20-reports`, escenario 5 |
| M-4 | Una organización no ve indicadores de otra, ni puede filtrar por una vacante ajena | PHPUnit (2 pruebas) y Cypress (escenarios 6 y 7) |
| M-5 | Período y vacante modifican KPI, gráficos y tabla; la etapa modifica los cinco KPI de postulaciones, gráficos y tabla, pero no el KPI de vacantes publicadas | PHPUnit (3 pruebas) y Cypress (escenarios 2, 3 y 4) |
| M-6 | El reporte no expone datos personales ni puntajes | `test_rf28_reports_expose_aggregates_only_and_no_personal_data` |
| M-7 | Antes del módulo, obtener estos indicadores exigía consultar vacante por vacante (`/vacantes/{id}/postulaciones` solo cuenta por estado y por vacante) o consultar la BD directamente; ahora hay una sola pantalla | Comparación funcional del código: `VacancyApplicationController` frente a `RecruitmentReportController` |

**Limitación de los datos.** Los valores del entorno local provienen de registros **ficticios de demostración** almacenados en PostgreSQL. El `DemoSeeder` crea todas las postulaciones en el mismo instante, de modo que el «tiempo promedio hasta la preselección» con esos datos es ≈ 0 días y **no** describe un proceso real. Solo demuestra que el cálculo funciona; las pruebas PHPUnit lo validan con fechas controladas.

## 7. Comparación antes/después

La guía pide comparar la situación anterior con la obtenida «cuando existan datos suficientes». **No existen**:

- el AS-IS no tiene tiempos, volúmenes ni herramientas institucionales validados (O-07);
- el sistema no se ha usado en un proceso real del Colegio (datos reales **prohibidos** por la gobernanza vigente, `CLAUDE.md`);
- los datos disponibles son sintéticos.

Por tanto **no se reporta ninguna mejora porcentual** (de tiempo de contratación, de horas de trabajo ni de calidad de la selección). La única comparación verificable es funcional (M-7): antes no existía una vista consolidada de indicadores, y ahora existe.

## 8. Beneficios potenciales (hipótesis, no medidos)

| # | Beneficio esperado | Cómo podría medirse en el futuro (con autorización y datos reales) |
|---|---|---|
| B-1 | Detectar antes las vacantes con baja respuesta y reforzar su difusión | Postulaciones por vacante antes y después de una acción de difusión |
| B-2 | Reducir la demora de la primera revisión (preselección) al hacerla visible | Línea base del tiempo promedio hasta la preselección en un período piloto, comparada con períodos siguientes |
| B-3 | Equilibrar la carga de evaluadores | Evolución del indicador «en evaluación o entrevista» frente a la capacidad declarada |
| B-4 | Ahorrar el tiempo de elaborar reportes manuales para Dirección | Encuesta o registro del tiempo dedicado a reportes, antes y después |
| B-5 | Mejorar el sustento de las decisiones de gestión (P5) | Revisión cualitativa de actas o justificaciones de Dirección |

Estos beneficios dependen de validar el AS-IS, de autorizar el uso de datos reales y de definir una línea base. Hoy ninguna de esas condiciones se cumple.

## 9. Alcance de la verificación independiente

Codex repitió las pruebas del módulo y las suites completas sobre registros ficticios persistidos. Se confirmó M-1 a M-6 y se contrastó M-7 con el código; no se realizó un estudio de tiempos institucionales. Las interpretaciones de tasa de preselección o carga son apoyos para revisión humana, **no relaciones causales demostradas**, ni mediciones de calidad de contratación. No se incorporaron datos reales, nuevos módulos ni decisiones automatizadas.
