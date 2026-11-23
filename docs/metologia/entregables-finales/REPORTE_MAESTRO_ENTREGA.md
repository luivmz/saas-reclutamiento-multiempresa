# Reporte maestro de entrega académica

Corte: 03/11/2026. Rama: chore/sonarqube-macos-setup. Commit base: b345d9c97077d1589a06d98ddfa9c6879ded58d1. Estado: **artefactos documentales preparados para revisión humana; validación institucional y experimental pendiente**.

| Elemento | Resultado |
| --- | --- |
| Fuentes procesadas | 5/5: Word 22 páginas, PPT 20 slides, Excel de procesos 7 hojas, PDF AI-DLC 8 páginas y matriz de registro de 177 ejemplos; originales preservados |
| Publicaciones identificadas/validadas en metadatos | 20 |
| Revisión por pares a nivel del venue | 13; no informes individuales de revisión |
| Preprints contados como publicaciones | 0 |
| RF / RNF académicos / CU | 27 / 10 / 20 |
| Macroprocesos / procedimientos / actividades / funciones | 2 / 7 / 33 / 33 (agrupación PROPUESTA con funciones reales) |
| Referencias de tests distintas por función | 26; métodos existentes, no ejecuciones de hoy |
| Funciones con evidencia Sonar individual | 4 |
| Funciones restantes | 29 bajo alcance agregado; sin coverage por función inferida |
| Secciones Word documentadas completas / parciales | 38 / 15 de 53 exigidas, más tres secciones metodológicas adicionales |
| Word / PPT finales | 49 páginas / 24 diapositivas, renderizados y revisados |
| Excel finales | 7 libros reabiertos; sin celdas error ni referencias #REF! |
| Matriz de doble entrada | 9 hojas: siete requeridas, catálogo de 20 artículos y 27 criterios del registro |
| Exigencias de fuentes y entrega | 184: 142 anteriores + 8 AI-DLC + 27 criterios del registro + 7 cruces |
| Brechas críticas / altas | 0 / 6 |
| Código, dependencias y configuración | No modificados |
| Pruebas en esta tarea | NO EJECUTADAS: alcance exclusivamente documental |
| Git add/commit/push | NO |

## Entregables

Los tres archivos principales son INFORME_FINAL_SAAS_RECLUTAMIENTO.docx, PRESENTACION_FINAL_U3_SAAS_RECLUTAMIENTO.pptx y MATRIZ_TRAZABILIDAD_SAAS_RECLUTAMIENTO.xlsx. Las matrices complementarias incluyen requisitos, trazabilidad académica, cumplimiento, artículos y variables. El Markdown fuente del Word permite auditoría textual. Los inventarios/hashes están en ../evidencias/ y los registros DOI en ../fuentes/.

## Criterios y limitaciones

La metodología y las variables para estudiar asistencia IA son PROPUESTAS y no sustituyen las variables históricas del proyecto. La literatura valida antecedentes y riesgos, no un efecto causal del desarrollo del SaaS. El AS-IS es preliminar; no se inventan organigrama, herramientas, tiempos ni aceptación del colegio. La CI se verifica como configuración; no se afirma run actual ni CD.

Sonar V1/V2: Issues 5→0; vulnerabilities 2→0; code smells 3→0. El gate final OK ignora condiciones por Small Changes; New Code Coverage = 50 %, no 80 %. Global 69.5 % tiene clasificación de tests distinta; app/ permanece en 89.6 %. Las evidencias y los informes históricos no se modifican.

## Revisión humana pendiente

Confirmar vigencia de los integrantes y docente documentados en F6, sección y fecha formal de entrega, validar contexto institucional, resolver las brechas y leer textos completos con campos científicos pendientes. Esta entrega no prueba eficacia causal, rendimiento productivo ni cumplimiento certificado de normas. La validación técnica/visual de archivos se registra en VALIDACION_ENTREGABLES.md.

## AI-DLC y fuentes adicionales

Se analizaron las ocho páginas de AI-Driven Development Lifecycle Method Definition, de Raja SP/AWS, contrastadas con su presentación oficial del 31/07/2025. Es un white paper técnico: no se cuenta como un artículo científico adicional ni se le atribuye peer review. Inception, Construction y Operations se comparan con el SaaS; Intent, Unit, Bolt y los rituales formales no se reconstruyen como hechos históricos. La correspondencia con Operations es baja: Docker y healthchecks locales no prueban operación IA productiva.

La matriz de registro original contiene 177 ejemplos de otro proyecto en una hoja Bolts. Sus commits, responsables, modelos y despliegues no son evidencia del SaaS. Se incorporaron 27 criterios de identificación, coherencia, trazabilidad y estabilidad, con estado y fuente. Se documentan alertas semánticas de sus fórmulas Y5 y equivalentes, y el subtotal BL181 vacío; no se copian sus porcentajes. Véase [análisis de fuentes](../fuentes/ANALISIS_AI_DLC_Y_REGISTRO.md).

## Matriz de doble entrada y variables

Archivo: [MATRIZ_DOBLE_ENTRADA_METODOLOGIA_IA.xlsx](MATRIZ_DOBLE_ENTRADA_METODOLOGIA_IA.xlsx), con [versión legible](MATRIZ_DOBLE_ENTRADA_METODOLOGIA_IA.md).

| Hoja | Contenido |
|---|---|
| Articulos_vs_Dimensiones | 20 artículos; respaldo temático sin relaciones forzadas |
| Articulos_vs_AI_DLC | 20 artículos; fases como correspondencias analíticas, no adopción atribuida |
| AI_DLC_vs_Proyecto | 11 conceptos con definición, evidencia y nivel de correspondencia |
| Metodologia_vs_Evidencias | 13 etapas desagregadas del protocolo propuesto |
| Requisitos_vs_Pruebas | 37 requisitos con test concreto o pendiente explícito |
| Requisitos_vs_Modulos | 27 RF y 10 RNF cruzados con módulos reales |
| Evidencias_vs_Indicadores | 25 indicadores y controles, históricos o pendientes prospectivos |
| Catalogo_Articulos | Identidad, DOI, autores, fuente, límites y aplicación de los 20 artículos |
| Registro_vs_Evidencias | 27 criterios de la matriz de registro con su aplicabilidad |

X significa respaldo temático o vínculo directo, no efecto causal. Una celda vacía representa relación no establecida. Testing no acredita TDD. Las columnas Intent/Unit/Bolt de artículos permanecen vacías. La literatura se utiliza para justificar controles; los valores del producto provienen del repositorio.

**Metodología propuesta:** desarrollo colaborativo humano IA guiado por especificaciones y verificación. **VI:** aplicación de ese protocolo. **VD:** calidad del producto software. Eficiencia queda exploratoria y PENDIENTE: no hay horas, costos ni control sin IA. Las dimensiones bibliográficas son productividad/eficiencia, calidad, seguridad, testing, requisitos, supervisión humana, trazabilidad, mantenibilidad y automatización. No todas disponen de una medida local. Las variables históricas SaaS→gestión del reclutamiento se preservan como estudio distinto.

## Índice de entregables

| Entregable | Archivo |
|---|---|
| Word de 14 capítulos | [Informe](INFORME_FINAL_SAAS_RECLUTAMIENTO.docx) |
| PPT de 24 diapositivas | [Presentación](PRESENTACION_FINAL_U3_SAAS_RECLUTAMIENTO.pptx) |
| Procesos | [Matriz adaptada](MATRIZ_TRAZABILIDAD_SAAS_RECLUTAMIENTO.xlsx) |
| Requisitos y CU | [Matriz de requisitos](MATRIZ_REQUERIMIENTOS_SISTEMA.xlsx) |
| Trazabilidad académica | [Matriz](MATRIZ_TRAZABILIDAD_ACADEMICA.xlsx) |
| Cumplimiento y fuentes adicionales | [Matriz](MATRIZ_CUMPLIMIENTO_INFORME.xlsx) |
| Artículos | [Excel](../investigacion-ia/MATRIZ_ARTICULOS_IA.xlsx) y [Markdown](../investigacion-ia/MATRIZ_ARTICULOS_IA.md) |
| Método | [Metodología IA](../investigacion-ia/METODOLOGIA_DESARROLLO_ASISTIDO_IA.md) |
| Operacionalización | [Excel](../investigacion-ia/OPERACIONALIZACION_VARIABLES.xlsx) y [Markdown](../investigacion-ia/OPERACIONALIZACION_VARIABLES.md) |
| Exposición | [Guion de 10 y 15 minutos](GUION_EXPOSICION.md) |
| Bibliografía | [APA 7](REFERENCIAS_APA7.md) y [fuentes descartadas](../investigacion-ia/FUENTES_RECHAZADAS.md) |
| Exigencias | [Reporte de requisitos](REPORTE_REQUISITOS_PLANTILLAS.md) |
| Brechas | [Doce brechas documentadas](BRECHAS_ENTREGA_FINAL.md) |
| Validaciones | [Reporte técnico documental](VALIDACION_ENTREGABLES.md) |

## Validaciones y límites finales

Se reabrieron los nueve artefactos Office; el Word se renderizó a 49 páginas y el PPT a 24 diapositivas. Las tablas y el gráfico PPT son editables; el recibo de integridad/geometría corresponde al hash final. Los siete libros Excel no contienen celdas error ni #REF!. La matriz de procesos conserva sus hojas, anchos, combinaciones y validación. Los cinco originales conservan sus hashes. No se alteraron evidencias V1/V2. La comparación de 1195 archivos rastreados del inicio muestra únicamente docs/PROGRESS.md modificado, como registro de esta fase documental.

Se comprobó bibliografía, rutas y métodos de pruebas, valores de matrices, secretos y alcance del diff. No se controló Microsoft Office nativo: la apertura nativa en el equipo de exposición queda como revisión humana final, diferenciada del render/reimportación verificados.

No faltan archivos obligatorios. Permanecen seis brechas ALTAS, cinco MEDIAS y una BAJA de validación/evidencia, no se completan con supuestos. Confirmar contexto institucional, aprobación del plan, nómina/fecha de entrega, textos completos, modalidad de revisión de siete venues/tracks y registros originales de IA. Una fase técnica separada puede abordar LCOV real, RNF y QA actual; no se ejecutó aquí.

Próximo paso recomendado: preparar diagramas editables diagrams.net/draw.io a partir de los entregables académicos validados. **No iniciado.** Se conserva el PlantUML generado en la preparación anterior; no se crearon diagramas adicionales en esta continuación. Sin git add, commit, push o merge.
