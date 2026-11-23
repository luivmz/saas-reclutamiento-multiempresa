# Reporte de Evidencias V1 – SonarQube

## 1. Objetivo

Organizar y preservar la línea base **ANTES de las mejoras V2** del proyecto saas-reclutamiento-multiempresa para la exposición universitaria. V1/V2 identifica paquetes de evidencias y comparación de calidad; no renumera los RF ni sustituye la versión 1.1 mostrada por SonarQube.

Inventario final: **30 imágenes PNG**, todas revisadas visualmente: 25 en la primera parte y 5 nuevas en la continuación. Se conservaron los renombrados válidos 01–25 y se añadieron 26–30. Hubo 24 renombrados iniciales y 5 adicionales: **29 renombrados acumulados**; V1_02_Quality_Gate.png ya tenía un nombre adecuado. No se eliminó ninguna captura.

Se distinguen tres clases de información:

- **EVIDENCIA VISUAL:** contenido realmente legible en cada PNG; los enlaces del inventario permiten comprobarlo.
- **RESULTADO DOCUMENTADO:** medición del análisis del 20/10/2026 registrada en los documentos existentes, sin repetir ejecución ni API en esta tarea.
- **TO-BE:** propuestas para V2; no implementadas ni verificadas como corrección.

Referencias consultadas y preservadas:

- [Resultados reales del análisis](../../RESULTADOS_SONARQUBE_MAC.md), especialmente §§11–22.
- [Operación y cobertura en Mac](../../README.md).
- [Guía de exposición](../../GUIA_PRESENTACION_SONARQUBE_MAC.md).

El reporte existente identifica el análisis procesado el 20/10/2026 a las 16:01:36 America/Lima, Project Key saas-reclutamiento-multiempresa, nombre SaaS Reclutamiento Multiempresa y revisión SCM b67f6443fb2bb71e736a60a645a15bd1fa0e7de6. Es referencia documental: las capturas no muestran todos esos identificadores. La asociación con V1 se apoya en la carpeta, el proyecto, la versión y las cifras coincidentes; no se inventa una etiqueta V1 dentro de la UI.

## 2. Inventario de evidencias

Cada fila describe exclusivamente lo visible en esa imagen; los tipos tradicionales de las reglas se contrastan en §6. Las 30 imágenes son útiles como evidencia principal, complemento o respaldo.

| N° | Archivo final | Pantalla | Contenido | Uso en exposición |
| --- | --- | --- | --- | --- |
| 1 | [V1_01_Dashboard.png](V1_01_Dashboard.png) | Dashboard / Overview | Quality gate Passed, 5 issues abiertos, Coverage 66.5 %, duplicación 0.0 %; versión 1.1. | Principal: inicio de la exposición. |
| 2 | [V1_02_Quality_Gate.png](V1_02_Quality_Gate.png) | Analysis / Summary | Quality gate Passed; Overall Code: Security 2/C, Reliability 3/C, Maintainability 1/A (MQR); Coverage 66.5 %, duplicación 0.0 %, Hotspots 0. | Principal: Quality Gate y resumen MQR. |
| 3 | [V1_03_Quality_Gate_Conditions.png](V1_03_Quality_Gate_Conditions.png) | Quality gates / Sonar way | Definición global: cuatro condiciones de código nuevo; gate Built-in y Default. | Explicar umbrales; no es una evaluación individual del proyecto. |
| 4 | [V1_04_Measures_Coverage_Overview.png](V1_04_Measures_Coverage_Overview.png) | Measures / Coverage Overview | Gráfico cobertura/complejidad; panel con Coverage 66.5 %, 4379 líneas a cubrir y 1469 sin cubrir. | Principal: pantalla Measures. |
| 5 | [V1_05_Coverage.png](V1_05_Coverage.png) | Measures / Coverage | Desglose: app 89.6 %, resources/js 0.0 %, routes 0.0 %; líneas sin cubrir por carpeta. | Principal: Coverage y sus límites. |
| 6 | [V1_06_Issues_Overview.png](V1_06_Issues_Overview.png) | Analysis / Issues | Listado general: 5 issues, 45 min de esfuerzo; dos hallazgos de seguridad y comienzo de data-table. | Principal: cantidad total de Issues. |
| 7 | [V1_07_Issues_Code_Smells.png](V1_07_Issues_Code_Smells.png) | Analysis / Issues, lista desplazada | Tres tarjetas Code Smell: data-table, regex del test y rechazo Promise; sin filtro de calidad. | Respaldo; redundante con 09. |
| 8 | [V1_08_Security_Issues.png](V1_08_Security_Issues.png) | Issues / filtro Security | 2 issues, 15 min: carga de CV y generador pseudoaleatorio; ambos Open y Security Medium. | Resumen de seguridad previo al detalle 26–27. |
| 9 | [V1_09_Reliability_Issues.png](V1_09_Reliability_Issues.png) | Issues / filtro Reliability | Tres tarjetas TypeScript: roles, regex y Promise; Reliability Medium; data-table además Maintainability Low. | Resumen de los tres Code Smells. |
| 10 | [V1_10_Maintainability_Issues.png](V1_10_Maintainability_Issues.png) | Issues / filtro Maintainability | Un issue en data-table.tsx, L149; impactos Reliability Medium y Maintainability Low; 5 min. | Demostrar que un Issue puede tener dos impactos. |
| 11 | [V1_11_Lines_To_Cover.png](V1_11_Lines_To_Cover.png) | Measures / Lines to Cover | 4379 global: app 3249, resources/js 1073, routes 57; tests sin valor aplicable. | Explicar el denominador de cobertura. |
| 12 | [V1_12_Uncovered_Lines.png](V1_12_Uncovered_Lines.png) | Measures / Uncovered Lines | 1469 global: app 339, resources/js 1073, routes 57; porcentajes por carpeta. | Respaldo; mismos datos esenciales que 05. |
| 13 | [V1_13_Line_Coverage.png](V1_13_Line_Coverage.png) | Measures / Line Coverage | 66.5 % global; app 89.6 %, resources/js y routes 0.0 %; líneas sin cubrir. | Respaldo; en esta línea base repite los valores de 05. |
| 14 | [V1_14_Duplications_Overview.png](V1_14_Duplications_Overview.png) | Measures / Duplications Overview | Density 0.0 %, líneas, bloques y archivos duplicados 0; gráfico sin puntos. | Mostrar duplicación sin confundirla con imágenes duplicadas. |
| 15 | [V1_15_Cyclomatic_Complexity.png](V1_15_Cyclomatic_Complexity.png) | Measures / Cyclomatic Complexity | 2047 global: app 897, resources/js 1142, routes 8; panel cognitiva 687. | Explicar complejidad ciclomática agregada. |
| 16 | [V1_16_Cognitive_Complexity.png](V1_16_Cognitive_Complexity.png) | Measures / Cognitive Complexity | 687 global: app 359, resources/js 328, routes 0. | Complementar la complejidad ciclomática. |
| 17 | [V1_17_Reliability_MQR_Overview.png](V1_17_Reliability_MQR_Overview.png) | Measures / Reliability Overview, MQR | 3 issues, rating C y remediación 30 min; gráfico de tres componentes. | Explicar Reliability MQR, no el conteo tradicional de Bugs. |
| 18 | [V1_18_Reliability_MQR_By_Directory.png](V1_18_Reliability_MQR_By_Directory.png) | Measures / Reliability Issues, MQR | 3 global, todos en resources/js; app, routes y tests 0. | Localizar los impactos Reliability. |
| 19 | [V1_19_Reliability_MQR_Rating.png](V1_19_Reliability_MQR_Rating.png) | Measures / Reliability Rating, MQR | C global; resources/js C; app, routes y tests A. | Contrastar con Reliability tradicional A documentada. |
| 20 | [V1_20_Reliability_MQR_Remediation.png](V1_20_Reliability_MQR_Remediation.png) | Measures / Reliability Remediation, MQR | 30 min global, concentrados en resources/js. | Mostrar esfuerzo estimado Reliability, no tiempo real trabajado. |
| 21 | [V1_21_Reliability_MQR_Severity.png](V1_21_Reliability_MQR_Severity.png) | Measures / Reliability Issue Severity, MQR | Valor numérico 15 global y resources/js; demás carpetas 0. | Solo respaldo técnico: 15 no significa 15 Issues. |
| 22 | [V1_22_Maintainability_MQR_Rating.png](V1_22_Maintainability_MQR_Rating.png) | Measures / Maintainability Rating, MQR | Rating A global y por carpeta; panel: 1 issue, deuda 5 min, ratio 0.0 %. | Distinguir MQR de 3 Code Smells y deuda tradicional 30 min. |
| 23 | [V1_23_Security_Hotspots_Review_Rating.png](V1_23_Security_Hotspots_Review_Rating.png) | Measures / Security Review Rating | Security Hotspots 0, Security Review Rating A; sección marcada Deprecated. | Evidencia de Hotspots por Measures; no es la lista dedicada. |
| 24 | [V1_24_Lines_Of_Code.png](V1_24_Lines_Of_Code.png) | Measures / Size / Lines of Code | 19495 ncloc: app 6045, resources/js 13335, routes 115; panel 23919 líneas y 288 archivos. | Explicar tamaño y lenguajes del alcance analizado. |
| 25 | [V1_25_Projects_Overview.png](V1_25_Projects_Overview.png) | Projects / listado global | Tarjeta SaaS: Passed, Coverage 66.5 %, duplicación 0.0 %, indicadores MQR; aparece otro proyecto. | Respaldo de identificación; no atribuir al SaaS la otra tarjeta. |
| 26 | [V1_26_Vulnerability_PHP_S5693.png](V1_26_Vulnerability_PHP_S5693.png) | Issues / detalle php:S5693 | L20, Open, Security Medium, 5 min; límite CV construido con config('recruitment.cv.max_kb'); código marcado cubierto. | Nueva: evidencia directa del hallazgo de carga. |
| 27 | [V1_27_Vulnerability_TS_S2245.png](V1_27_Vulnerability_TS_S2245.png) | Issues / detalle typescript:S2245 | L624, Open, Security Medium, 10 min; fragmento próximo a sidebar-menu-skeleton; línea de generación fuera del recorte. | Nueva: revisar contexto de uso antes de juzgar explotabilidad. |
| 28 | [V1_28_CodeSmell_TS_S6843.png](V1_28_CodeSmell_TS_S6843.png) | Issues / detalle typescript:S6843 | L149, Open, Reliability Medium y Maintainability Low; td con role="cell" visible; 5 min. | Nueva: evidencia directa de semántica/interactividad. |
| 29 | [V1_29_CodeSmell_TS_S8786.png](V1_29_CodeSmell_TS_S8786.png) | Issues / detalle typescript:S8786 | L162, Open, Reliability Medium, 20 min; regex aplicada a markup de renderToStaticMarkup en test. | Nueva: evidencia directa de backtracking reportado. |
| 30 | [V1_30_CodeSmell_TS_S6671.png](V1_30_CodeSmell_TS_S6671.png) | Issues / detalle typescript:S6671 | L56, Open, Reliability Medium, 5 min; Promise.reject(response.status) visible. | Nueva: evidencia directa del rechazo con valor no Error. |

### Inventario original y trazabilidad del renombrado

Todas conservan formato PNG y resolución **2940 × 1912 píxeles**. Se registraron tamaño y SHA-256 antes del renombrado y se comprobó la conservación del contenido. No hubo edición, compresión, conversión ni cambio de resolución.

Los mtime observados son aproximadamente 20/10/2026 19:50:14 America/Lima para las 25 iniciales y 19:57:14 para las cinco nuevas (21/10/2026 00:50:14 y 00:57:14 UTC). Son fechas de modificación del archivo, posiblemente de copia; **no prueban la fecha del análisis**. Las denominaciones originales Screenshot indican hora de captura, pero tampoco reemplazan la fecha documental del análisis.

| Nombre original | Archivo final | Tamaño (bytes) | Acción |
| --- | --- | --- | --- |
| Screenshot 2026-10-20 at 7.39.07 PM.png | V1_01_Dashboard.png | 585801 | Renombrada en primera parte |
| V1_02_Quality_Gate.png | V1_02_Quality_Gate.png | 541566 | Nombre original conservado |
| Screenshot 2026-10-20 at 7.37.55 PM.png | V1_03_Quality_Gate_Conditions.png | 526557 | Renombrada en primera parte |
| Screenshot 2026-10-20 at 7.44.58 PM.png | V1_04_Measures_Coverage_Overview.png | 747109 | Renombrada en primera parte |
| Screenshot 2026-10-20 at 7.45.08 PM.png | V1_05_Coverage.png | 603897 | Renombrada en primera parte |
| Screenshot 2026-10-20 at 7.40.27 PM.png | V1_06_Issues_Overview.png | 753496 | Renombrada en primera parte |
| Screenshot 2026-10-20 at 7.40.41 PM.png | V1_07_Issues_Code_Smells.png | 765642 | Renombrada en primera parte |
| Screenshot 2026-10-20 at 7.42.05 PM.png | V1_08_Security_Issues.png | 736568 | Renombrada en primera parte |
| Screenshot 2026-10-20 at 7.42.14 PM.png | V1_09_Reliability_Issues.png | 773384 | Renombrada en primera parte |
| Screenshot 2026-10-20 at 7.42.17 PM.png | V1_10_Maintainability_Issues.png | 741152 | Renombrada en primera parte |
| Screenshot 2026-10-20 at 7.45.14 PM.png | V1_11_Lines_To_Cover.png | 613870 | Renombrada en primera parte |
| Screenshot 2026-10-20 at 7.45.19 PM.png | V1_12_Uncovered_Lines.png | 599929 | Renombrada en primera parte |
| Screenshot 2026-10-20 at 7.45.22 PM.png | V1_13_Line_Coverage.png | 601543 | Renombrada en primera parte |
| Screenshot 2026-10-20 at 7.45.44 PM.png | V1_14_Duplications_Overview.png | 583330 | Renombrada en primera parte |
| Screenshot 2026-10-20 at 7.45.57 PM.png | V1_15_Cyclomatic_Complexity.png | 612366 | Renombrada en primera parte |
| Screenshot 2026-10-20 at 7.46.01 PM.png | V1_16_Cognitive_Complexity.png | 614543 | Renombrada en primera parte |
| Screenshot 2026-10-20 at 7.46.24 PM.png | V1_17_Reliability_MQR_Overview.png | 628983 | Renombrada en primera parte |
| Screenshot 2026-10-20 at 7.46.30 PM.png | V1_18_Reliability_MQR_By_Directory.png | 600657 | Renombrada en primera parte |
| Screenshot 2026-10-20 at 7.46.34 PM.png | V1_19_Reliability_MQR_Rating.png | 611965 | Renombrada en primera parte |
| Screenshot 2026-10-20 at 7.47.14 PM.png | V1_20_Reliability_MQR_Remediation.png | 615907 | Renombrada en primera parte |
| Screenshot 2026-10-20 at 7.47.16 PM.png | V1_21_Reliability_MQR_Severity.png | 658332 | Renombrada en primera parte |
| Screenshot 2026-10-20 at 7.47.35 PM.png | V1_22_Maintainability_MQR_Rating.png | 616710 | Renombrada en primera parte |
| Screenshot 2026-10-20 at 7.47.48 PM.png | V1_23_Security_Hotspots_Review_Rating.png | 612860 | Renombrada en primera parte |
| Screenshot 2026-10-20 at 7.48.06 PM.png | V1_24_Lines_Of_Code.png | 591022 | Renombrada en primera parte |
| Screenshot 2026-10-20 at 7.34.58 PM.png | V1_25_Projects_Overview.png | 659912 | Renombrada en primera parte |
| Screenshot 2026-10-20 at 7.56.26 PM.png | V1_26_Vulnerability_PHP_S5693.png | 727321 | Nueva; renombrada en continuación |
| Screenshot 2026-10-20 at 7.56.35 PM.png | V1_27_Vulnerability_TS_S2245.png | 753593 | Nueva; renombrada en continuación |
| Screenshot 2026-10-20 at 7.56.39 PM.png | V1_28_CodeSmell_TS_S6843.png | 761885 | Nueva; renombrada en continuación |
| Screenshot 2026-10-20 at 7.56.51 PM.png | V1_29_CodeSmell_TS_S8786.png | 789691 | Nueva; renombrada en continuación |
| Screenshot 2026-10-20 at 7.56.59 PM.png | V1_30_CodeSmell_TS_S6671.png | 740281 | Nueva; renombrada en continuación |

Las cinco capturas incorporadas después de la primera inspección son 26–30. Son complementarias de los listados 06–10: añaden regla, línea y fragmento de código. **No representan cinco Issues nuevos**.

## 3. Evidencias obligatorias de la guía

| Evidencia | Archivo | Estado |
| --- | --- | --- |
| Dashboard V1 | [V1_01_Dashboard.png](V1_01_Dashboard.png) | ✅ ENCONTRADA: Overview del proyecto, no listado global. |
| Quality Gate V1 | [V1_02_Quality_Gate.png](V1_02_Quality_Gate.png) | ✅ ENCONTRADA: Summary, Passed. Interpretar con los límites de §9. |
| Measures V1 | [V1_04_Measures_Coverage_Overview.png](V1_04_Measures_Coverage_Overview.png) | ✅ ENCONTRADA: Measures, gráfico Coverage Overview. |
| Issues V1 | [V1_06_Issues_Overview.png](V1_06_Issues_Overview.png), complementada por [09](V1_09_Reliability_Issues.png) | ✅ ENCONTRADA: 5 Issues en total; listado desplazado/filtros complementan las tarjetas. |
| Coverage V1 | [V1_05_Coverage.png](V1_05_Coverage.png) | ✅ ENCONTRADA: 66.5 % global y desglose por carpeta. |

Recorrido breve sugerido: 01 → 02 → 03 → 04 → 05 → 06 → 08 → detalles 26–30. Las capturas de Measures complementarias permiten responder preguntas sin mostrar todas en la exposición principal.

## 4. Evidencias complementarias

| Categoría | Evidencia | Qué respalda / límite |
| --- | --- | --- |
| Security Overview | Summary [02](V1_02_Quality_Gate.png) y filtro [08](V1_08_Security_Issues.png) | Dos impactos Security y rating C en MQR. No hay una captura dedicada a Measures / Security Overview; no se le asignó ese nombre a otra pantalla. |
| Security Hotspots | [23](V1_23_Security_Hotspots_Review_Rating.png) y Summary [02](V1_02_Quality_Gate.png) | Total 0 y Security Review Rating A. No muestran la lista dedicada ni porcentaje de revisados. |
| Vulnerabilities | [26 — PHP S5693](V1_26_Vulnerability_PHP_S5693.png), [27 — TS S2245](V1_27_Vulnerability_TS_S2245.png) | Detalle de los dos hallazgos de seguridad; clasificación tradicional Vulnerability respaldada por el reporte de resultados. |
| Code Smells | [28 — S6843](V1_28_CodeSmell_TS_S6843.png), [29 — S8786](V1_29_CodeSmell_TS_S8786.png), [30 — S6671](V1_30_CodeSmell_TS_S6671.png) | Regla, línea, estado Open e impacto MQR visibles; tipo tradicional desde el reporte. |
| Quality Gate Conditions | [03](V1_03_Quality_Gate_Conditions.png) | Definición global Sonar way, no condiciones efectivamente evaluadas en el primer análisis. |
| Reliability | [17](V1_17_Reliability_MQR_Overview.png), [18](V1_18_Reliability_MQR_By_Directory.png), [19](V1_19_Reliability_MQR_Rating.png), [20](V1_20_Reliability_MQR_Remediation.png) | MQR: 3 impactos, C y 30 min; todos los impactos en resources/js. |
| Maintainability | [22](V1_22_Maintainability_MQR_Rating.png) y [10](V1_10_Maintainability_Issues.png) | MQR: A, un Issue, 5 min; data-table comparte impacto Reliability. |
| Duplications | [14](V1_14_Duplications_Overview.png) | 0.0 % y contadores 0. |
| Complexity | [15](V1_15_Cyclomatic_Complexity.png), [16](V1_16_Cognitive_Complexity.png) | Ciclomática 2047, cognitiva 687, con desglose. |
| Size / lenguajes | [24](V1_24_Lines_Of_Code.png) | 19495 ncloc; TypeScript/PHP y tamaño por carpeta. |
| Identificación de proyecto | [25](V1_25_Projects_Overview.png) | Tarjeta SaaS en listado global. Ignorar las métricas de la otra tarjeta. |
| SonarScanner / Docker / pruebas | No hay PNG de esas pantallas en esta carpeta. | Existen resultados documentados, pero no evidencia visual aquí de EXECUTION SUCCESS, Docker ni salidas PHPUnit. |

## 5. Línea base V1

Fuente documental: [Resultados SonarQube](../../RESULTADOS_SONARQUBE_MAC.md). Cuando se indica visual, el PNG corrobora específicamente la cifra; no se atribuyen a imágenes cifras que no muestran.

| Indicador | Resultado actual |
| --- | --- |
| Quality Gate | OK documentado; Passed visible en 01 y 02. Primer análisis con conditions: [] según API documentada. |
| Coverage global / Line Coverage | 66.5 %; visual 04, 05 y 13. |
| Coverage app/ | 89.6 %; visual 05. |
| Coverage resources/js | 0.0 %; visual 05. |
| Coverage routes | 0.0 %; visual 05. |
| Líneas a cubrir / sin cubrir | 4379 / 1469; visual 04, 11 y 12. |
| Duplicación | 0.0 %; visual 01, 02 y 14. |
| Bugs tradicionales | 0; resultado documentado, no conteo explícito de Bugs en estas capturas MQR. |
| Vulnerabilities tradicionales | 2; documentado; los dos hallazgos Security son visibles en 08, 26 y 27. |
| Code Smells tradicionales | 3; documentado; tarjetas/detalles en 09 y 28–30. |
| Issues únicos abiertos | 5; documentado y visual 01, 06 y panel de detalles 26–28. |
| Security Hotspots | 0; documentado y visual 02 y 23. |
| Hotspots pendientes / revisados | 0 / 0 documentados; porcentaje de revisados no devuelto, no asumir 100 %. |
| Security Rating tradicional | C; documentado. Security MQR también C, visible 02 y 25. |
| Reliability tradicional | A con 0 Bugs; documentado. No es el rating C visible en las pantallas MQR. |
| Maintainability tradicional | A con 3 Code Smells; documentado. Rating MQR también A, pero con un Issue. |
| Security MQR | 2 impactos, C; visual 02, 08, 25. |
| Reliability MQR | 3 impactos, C; visual 02 y 17–19. |
| Maintainability MQR | 1 impacto, A; visual 02, 10 y 22. |
| Cognitive Complexity | 687; documentado y visual 16. |
| Cyclomatic Complexity | 2047; documentado y visual 15. |
| Technical Debt tradicional | 30 min, sqale_index; documentado. No hay captura dedicada a esa métrica tradicional. |
| Esfuerzo Reliability MQR | 30 min; visual 17 y 20. Coincide numéricamente, pero no es la misma métrica que sqale_index. |
| Deuda Maintainability MQR | 5 min; documentado y visual 22. |
| Esfuerzo total de los Issues | 45 min; visual 06. No sustituye ni se suma a las métricas anteriores. |
| Lines of Code (ncloc) | 19495; documentado y visual 24. |
| SonarQube | Community Build 26.10.0.133078, MQR MODE; documentado y pie visible en varias capturas. |

**MQR y métricas tradicionales no son intercambiables.** Los cinco Issues tradicionales son 2 Vulnerabilities y 3 Code Smells, sin Bugs. En MQR tienen 2 impactos Security, 3 Reliability y 1 Maintainability: un mismo Issue (S6843) impacta dos cualidades. Por tanto, 2 + 3 + 1 no significa seis Issues. De igual modo, cinco impactos Medium y uno Low no representan seis incidencias distintas.

El valor 15 de [21](V1_21_Reliability_MQR_Severity.png) pertenece a la métrica titulada Reliability Issue Severity on Overall Code. No se lo interpreta como 15 Issues, 15 Bugs ni 15 minutos; su fórmula no se verifica en esta tarea.

## 6. Issues SonarQube detectados

Los identificadores I-01 a I-05 son índices locales de este reporte, **no IDs internos de la API ni DEF del proyecto**. Archivo completo y tipo/severidad tradicionales proceden del reporte existente (§19); las nuevas capturas corroboran reglas, líneas y severidades de impacto MQR.

| ID | Regla | Archivo | Tipo | Severidad | Descripción | Captura |
| --- | --- | --- | --- | --- | --- | --- |
| I-01 | php:S5693 | app/Http/Requests/Candidates/CandidateCvRequest.php:20 | Vulnerability tradicional | MAJOR documentada; Security Medium visible | Revisar seguridad del límite del CV. Se observa max construido con recruitment.cv.max_kb; la captura no muestra su valor efectivo. | [26 — detalle](V1_26_Vulnerability_PHP_S5693.png), [08 — listado](V1_08_Security_Issues.png) |
| I-02 | typescript:S2245 | resources/js/components/ui/sidebar.tsx:624 | Vulnerability tradicional | MAJOR documentada; Security Medium visible | Revisar uso seguro de generador pseudoaleatorio. La línea afectada se identifica en la cabecera, pero la llamada concreta queda fuera del recorte. | [27 — detalle](V1_27_Vulnerability_TS_S2245.png), [08 — listado](V1_08_Security_Issues.png) |
| I-03 | typescript:S8786 | resources/js/components/experience-3d/experience-3d.test.tsx:162 | Code Smell tradicional | MAJOR documentada; Reliability Medium visible | Regex con posible coste superlineal por backtracking, aplicada al markup generado en una prueba. | [29 — detalle](V1_29_CodeSmell_TS_S8786.png), [09 — listado](V1_09_Reliability_Issues.png) |
| I-04 | typescript:S6843 | resources/js/components/data-table.tsx:149 | Code Smell tradicional | MAJOR documentada; Reliability Medium y Maintainability Low visibles | Conflicto semántico/interactivo reportado; el fragmento muestra td con role="cell". Debe revisarse el contexto completo. | [28 — detalle](V1_28_CodeSmell_TS_S6843.png), [10 — filtro](V1_10_Maintainability_Issues.png) |
| I-05 | typescript:S6671 | resources/js/components/vacancies/operational-risk-card.tsx:56 | Code Smell tradicional | MAJOR documentada; Reliability Medium visible | Rechazo de Promise con response.status en vez de un Error. | [30 — detalle](V1_30_CodeSmell_TS_S6671.png), [09 — listado](V1_09_Reliability_Issues.png) |

Los cinco están Open en la evidencia. Las capturas no prueban explotación ni un fallo funcional observado. En especial, "hallazgo de seguridad reportado por SonarQube que requiere revisión" no equivale a vulnerabilidad explotable confirmada. No se resolvió, aceptó ni reclasificó ningún Issue.

## 7. Problemas prioritarios para V2

**Problemas detectados para mejorar en V2 — propuestas, NO implementadas.** La prioridad técnica es una recomendación de este reporte; no sustituye la severidad Sonar ni una revisión de seguridad contextual.

| Prioridad | Problema | Motivo | Estrategia recomendada |
| --- | --- | --- | --- |
| ALTA | I-01 / php:S5693 — límite de carga de CV | Entrada de archivos: revisar coherencia de límites y potencial consumo de recursos. Hay validación max dinámica visible, por lo que no se afirma que falte todo límite ni que exista una explotación. Evidencia 26. | Comprobar valor efectivo, límites PHP/servidor y regla de negocio; revisar unidades y casos al límite/sobretamaño con pruebas. No reducir arbitrariamente el límite para silenciar Sonar. Documentar la decisión y validar el hallazgo. |
| MEDIA | I-02 / typescript:S2245 — generador pseudoaleatorio | Hallazgo Security Medium. El fragmento próximo al skeleton sugiere contexto visual, pero no demuestra el flujo completo ni uso criptográfico. Evidencia 27. | Revisar llamada y consumidores: si es solo presentación, valorar solución determinista y documentar contexto; si participa en seguridad, sustituir el mecanismo según ese requisito. No afirmar explotabilidad ni cambiar a ciegas. Elevar prioridad si se confirma uso sensible. |
| MEDIA | I-04 / typescript:S6843 — semántica/interacción de tabla | Posible impacto en accesibilidad/fiabilidad de interacción; Sonar señala role="cell" y dos cualidades. La captura no muestra todos los handlers/contexto. Evidencia 28. | Revisar DOM nativo, roles y eventos completos; conservar semántica de tabla y comprobar teclado/tecnología asistiva antes de decidir el cambio. No quitar roles indiscriminadamente. |
| MEDIA | I-05 / typescript:S6671 — rechazo con status numérico | Dificulta uniformidad y diagnóstico de errores asíncronos; no demuestra por sí solo caída del componente. Evidencia 30. | Proponer Error tipado que conserve el status requerido; revisar los consumidores/catch y probar ruta HTTP fallida sin alterar el carácter informativo del riesgo operacional. |
| BAJA | I-03 / typescript:S8786 — regex en test | El fragmento procesa markup generado en una prueba, no acredita entrada hostil en producción. Puede afectar robustez/tiempo del test; no se demuestra ReDoS explotable. Evidencia 29. | Evitar backtracking mediante una extracción/aserción apropiada para ese test, conservando su intención. Probar equivalencia y entradas relevantes; no excluir el archivo solo para reducir Issues. |

La revisión comienza por los dos hallazgos de seguridad, aunque su prioridad final dependa del contexto. Las propuestas no autorizan cambios funcionales ni reinterpretación de RF-01 a RF-27.

## 8. Cobertura

Evidencia visual principal: [05 — Coverage](V1_05_Coverage.png). Denominadores: [11](V1_11_Lines_To_Cover.png); respaldo de líneas sin cubrir: [12](V1_12_Uncovered_Lines.png).

| Alcance | Coverage V1 | Líneas a cubrir | Sin cubrir |
| --- | --- | --- | --- |
| Global Sonar | 66.5 % | 4379 | 1469 |
| app/ | 89.6 % | 3249 | 339 |
| resources/js | 0.0 % | 1073 | 1073 |
| routes | 0.0 % | 57 | 57 |

Según los resultados y README existentes, PHP dispone de un reporte Clover real generado con PCOV dentro de Docker; su colección se limita a app/. No hay LCOV frontend ni reporte de cobertura propio que cubra routes en el análisis actual. El 0.0 % importado **no demuestra que nunca se hayan ejecutado pruebas sobre esos flujos**: describe la evidencia de cobertura disponible para Sonar.

El reporte documentado Clover contiene 151 archivos, 2777 sentencias y 2499 cubiertas (aproximadamente 90.0 % de sentencias). Esa medida no reemplaza el 89.6 % de líneas calculado para app/ ni el 66.5 % global. La captura 26 marca algunas líneas como cubiertas, pero no muestra ni valida por sí sola el XML completo.

V2 podría incorporar cobertura frontend real si el tiempo lo permite y ampliar de manera justificada la colección PHP a rutas. No se deben excluir artificialmente frontend, rutas o código propio para elevar el porcentaje. Mantener alcance comparable y documentar cualquier cambio legítimo de denominador.

No se regeneró coverage.xml, no se ejecutaron pruebas y no se modificó la configuración de cobertura durante esta tarea.

## 9. Quality Gate

Estado de línea base: **OK documentado / Passed visible** en [02](V1_02_Quality_Gate.png) y [01](V1_01_Dashboard.png). La definición global Sonar way está en [03](V1_03_Quality_Gate_Conditions.png).

El reporte real (§13) registra que el primer análisis devolvió **conditions: []**. Esa respuesta de API no está capturada en PNG; es un resultado documental. La UI "Passed" o "All conditions passed" no justifica afirmar que toda la calidad global esté aprobada.

> El Quality Gate aparece OK en la línea base actual, pero este primer análisis no evaluó todavía condiciones de código nuevo.

Sonar way mostrado define estas condiciones sobre código nuevo:

| Condición | Umbral para cumplir |
| --- | --- |
| Nuevos Issues | 0 |
| Nuevos Security Hotspots revisados | 100 %, cuando corresponda |
| Cobertura de código nuevo | ≥80 % |
| Duplicación de código nuevo | ≤3 % |

El 66.5 % global y los cinco Issues existentes no se vuelven inexistentes por el Gate OK. Tampoco el Security Review Rating A con cero hotspots demuestra ausencia de vulnerabilidades ni una revisión del 100 %: el porcentaje no fue devuelto según el reporte. En V2 debe comprobarse qué condiciones efectivamente se evalúan y cuál es el periodo de código nuevo, sin cambiar la definición para conseguir un resultado favorable.

## 10. Otras deudas de calidad

**Otras deudas encontradas fuera de los 5 Issues Sonar.** Son resultados previos reales del [reporte de análisis](../../RESULTADOS_SONARQUBE_MAC.md), no ejecuciones de esta tarea documental. SonarQube y las herramientas siguientes se complementan; sus conteos no se suman para calcular Issues Sonar.

| Herramienta | Resultado documentado | Interpretación / pendiente |
| --- | --- | --- |
| PHPStan / Larastan | ❌ FAILED, 91 errores | Deuda de análisis estático; revisar por causa y alcance en fase propia. |
| Laravel Pint | ❌ FAILED, 8 problemas en 256 archivos | Estilo PHP; no se aplicó corrector. |
| Vite Plus / Oxfmt | ❌ FAILED, 297 archivos pendientes de formato | Deuda global medida antes de este nuevo reporte. No se ejecutó check hoy y no se afirma que el conteo global permanezca exactamente igual después de añadirlo. |
| Oxlint | ❌ FAILED, 5 warnings, 0 errors | denyWarnings hace fallar el comando; no son cinco Bugs Sonar. |
| TypeScript | ✅ PASSED | Comprobación de tipos aprobada en la ejecución documentada. |
| Vitest | ✅ PASSED, 42 pruebas en 6 archivos | No implica que se haya generado/importado LCOV frontend. |
| PHPUnit | ✅ PASSED, 411 passed, 8 skipped, 0 failed, 1498 assertions | 419 casos totales; los skipped no se cuentan como aprobados. |
| Cypress | ⏭️ NO EJECUTADO en la sesión del análisis | Requería entorno E2E destructivo aislado. No se atribuyen resultados históricos a esa sesión ni a esta. |

En esta organización no se ejecutaron PHPUnit, PHPStan, Pint, TypeScript, Vite Plus, Vitest, Cypress, scanner ni formatters. No se modificó código para reducir ninguna cifra.

## 11. Plan recomendado para V2

**TO-BE, NO ejecutar como parte de esta tarea:**

1. Revisar los dos hallazgos de seguridad con contexto completo; acordar y autorizar correcciones justificadas sin alterar reglas de negocio.
2. Corregir los Code Smells seleccionados con pruebas apropiadas, preservando accesibilidad, aislamiento multiempresa y comportamiento informativo/humano del sistema. No cambiar alcance Sonar para ocultar hallazgos.
3. Ejecutar las pruebas y controles proporcionales; registrar passed, failed y skipped reales. Tratar PHPStan/estilo/formato como deudas separadas y acotadas.
4. Regenerar coverage.xml mediante el procedimiento ya documentado. Si se incorpora cobertura frontend, conservar su reporte real y documentar el cambio de medición.
5. Ejecutar SonarScanner según el README existente; comprobar procesamiento, Gate y métricas del nuevo análisis.
6. Capturar las mismas pantallas V2 de §13, conservando estos PNG V1 sin sobrescribirlos. Si un Issue queda resuelto, capturar su estado resuelto o evidencia del filtro correspondiente.
7. Completar la comparación Antes vs Después con métricas equivalentes, mismo modo tradicional/MQR y denominadores explícitos. Explicar también lo que no haya mejorado.

Este plan requiere una fase posterior de implementación/revisión. No se realizó ninguna de sus acciones técnicas aquí.

## 12. Tabla preparada para Antes vs Después

V1 se rellena con la línea base visual/documentada; **V2 Después y Variación permanecen PENDIENTE**, sin metas presentadas como resultados.

| Métrica | V1 Antes | V2 Después | Variación |
| --- | --- | --- | --- |
| Quality Gate | OK; primer análisis conditions: [] | PENDIENTE | PENDIENTE |
| Coverage global | 66.5 % | PENDIENTE | PENDIENTE |
| Coverage app/ | 89.6 % | PENDIENTE | PENDIENTE |
| Coverage resources/js | 0.0 % | PENDIENTE | PENDIENTE |
| Coverage routes | 0.0 % | PENDIENTE | PENDIENTE |
| Líneas a cubrir | 4379 | PENDIENTE | PENDIENTE |
| Líneas sin cubrir | 1469 | PENDIENTE | PENDIENTE |
| Duplicación | 0.0 % | PENDIENTE | PENDIENTE |
| Bugs tradicionales | 0 | PENDIENTE | PENDIENTE |
| Vulnerabilities tradicionales | 2 | PENDIENTE | PENDIENTE |
| Code Smells tradicionales | 3 | PENDIENTE | PENDIENTE |
| Issues únicos abiertos | 5 | PENDIENTE | PENDIENTE |
| Security Hotspots | 0 | PENDIENTE | PENDIENTE |
| Security Rating tradicional | C | PENDIENTE | PENDIENTE |
| Reliability tradicional | A | PENDIENTE | PENDIENTE |
| Maintainability tradicional | A | PENDIENTE | PENDIENTE |
| Security MQR | 2 / C | PENDIENTE | PENDIENTE |
| Reliability MQR | 3 / C | PENDIENTE | PENDIENTE |
| Maintainability MQR | 1 / A | PENDIENTE | PENDIENTE |
| Cognitive Complexity | 687 | PENDIENTE | PENDIENTE |
| Cyclomatic Complexity | 2047 | PENDIENTE | PENDIENTE |
| Technical Debt tradicional | 30 min | PENDIENTE | PENDIENTE |
| Remediación Reliability MQR | 30 min | PENDIENTE | PENDIENTE |
| Deuda Maintainability MQR | 5 min | PENDIENTE | PENDIENTE |
| ncloc | 19495 | PENDIENTE | PENDIENTE |
| PHPStan / Larastan | 91 errores | PENDIENTE | PENDIENTE |
| Pint | 8 problemas | PENDIENTE | PENDIENTE |
| Vite Plus / formato | 297 archivos, ejecución previa | PENDIENTE | PENDIENTE |
| Oxlint | 5 warnings, 0 errors | PENDIENTE | PENDIENTE |
| TypeScript | PASSED | PENDIENTE | PENDIENTE |
| Vitest | 42 PASSED | PENDIENTE | PENDIENTE |
| PHPUnit | 411 passed, 8 skipped, 0 failed; 1498 assertions | PENDIENTE | PENDIENTE |
| Cypress | NO EJECUTADO en la sesión del análisis | PENDIENTE | PENDIENTE |

Las variaciones de porcentaje se expresarán en puntos porcentuales y las de ratings como cambio de categoría, no como porcentajes inventados. Conservar separados Technical Debt tradicional, esfuerzo Reliability MQR y deuda Maintainability MQR.

## 13. Capturas requeridas para V2

Repetir las cinco evidencias obligatorias (01, 02, 04, 05, 06) y los complementos marcados "Repetir". La tabla es el mapa exacto de pantallas V1 a capturas futuras; **no existen todavía esos archivos V2 como resultado de esta tarea**. Los respaldos opcionales no son necesarios en la exposición principal, pero se identifican para reproducibilidad.

Guardar las nuevas evidencias en un paquete V2 separado, sin mover ni sobrescribir V1. Mantener proyecto, escala legible y modo MQR comparables. Para los detalles 26–30 mostrar la misma regla/ubicación o su estado resuelto; en 27 procurar incluir la línea completa del generador, ausente en el recorte V1.

| Captura V1 que se compara | Nombre propuesto para V2 | Repetición |
| --- | --- | --- |
| V1_01_Dashboard.png | V2_01_Dashboard.png | Repetir |
| V1_02_Quality_Gate.png | V2_02_Quality_Gate.png | Repetir |
| V1_03_Quality_Gate_Conditions.png | V2_03_Quality_Gate_Conditions.png | Repetir |
| V1_04_Measures_Coverage_Overview.png | V2_04_Measures_Coverage_Overview.png | Repetir |
| V1_05_Coverage.png | V2_05_Coverage.png | Repetir |
| V1_06_Issues_Overview.png | V2_06_Issues_Overview.png | Repetir |
| V1_07_Issues_Code_Smells.png | V2_07_Issues_Code_Smells.png | Respaldo opcional |
| V1_08_Security_Issues.png | V2_08_Security_Issues.png | Repetir |
| V1_09_Reliability_Issues.png | V2_09_Reliability_Issues.png | Repetir |
| V1_10_Maintainability_Issues.png | V2_10_Maintainability_Issues.png | Repetir |
| V1_11_Lines_To_Cover.png | V2_11_Lines_To_Cover.png | Repetir |
| V1_12_Uncovered_Lines.png | V2_12_Uncovered_Lines.png | Respaldo opcional |
| V1_13_Line_Coverage.png | V2_13_Line_Coverage.png | Respaldo opcional |
| V1_14_Duplications_Overview.png | V2_14_Duplications_Overview.png | Repetir |
| V1_15_Cyclomatic_Complexity.png | V2_15_Cyclomatic_Complexity.png | Repetir |
| V1_16_Cognitive_Complexity.png | V2_16_Cognitive_Complexity.png | Repetir |
| V1_17_Reliability_MQR_Overview.png | V2_17_Reliability_MQR_Overview.png | Repetir |
| V1_18_Reliability_MQR_By_Directory.png | V2_18_Reliability_MQR_By_Directory.png | Repetir |
| V1_19_Reliability_MQR_Rating.png | V2_19_Reliability_MQR_Rating.png | Repetir |
| V1_20_Reliability_MQR_Remediation.png | V2_20_Reliability_MQR_Remediation.png | Repetir |
| V1_21_Reliability_MQR_Severity.png | V2_21_Reliability_MQR_Severity.png | Respaldo opcional |
| V1_22_Maintainability_MQR_Rating.png | V2_22_Maintainability_MQR_Rating.png | Repetir |
| V1_23_Security_Hotspots_Review_Rating.png | V2_23_Security_Hotspots_Review_Rating.png | Repetir |
| V1_24_Lines_Of_Code.png | V2_24_Lines_Of_Code.png | Repetir |
| V1_25_Projects_Overview.png | V2_25_Projects_Overview.png | Respaldo opcional |
| V1_26_Vulnerability_PHP_S5693.png | V2_26_Vulnerability_PHP_S5693.png | Repetir |
| V1_27_Vulnerability_TS_S2245.png | V2_27_Vulnerability_TS_S2245.png | Repetir |
| V1_28_CodeSmell_TS_S6843.png | V2_28_CodeSmell_TS_S6843.png | Repetir |
| V1_29_CodeSmell_TS_S8786.png | V2_29_CodeSmell_TS_S8786.png | Repetir |
| V1_30_CodeSmell_TS_S6671.png | V2_30_CodeSmell_TS_S6671.png | Repetir |

Si se desea ampliar la evidencia futura, añadir capturas dedicadas de Security Overview, lista Security Hotspots, condiciones realmente evaluadas del análisis y SonarScanner SUCCESS. **No están disponibles como pantallas dedicadas en este paquete V1** y no deben presentarse como comparativas visuales existentes.

## 14. Observaciones

- Evidencia generada en Mac; el entorno macOS Apple Silicon/arm64 y Docker está registrado en los documentos de preparación. Las capturas muestran Safari y localhost, no toda la arquitectura runtime.
- Entorno académico/local. SonarQube usa H2 embebido según el README; el aviso visible insiste en uso de evaluación. **No es producción** ni una configuración apta para demostrar escalabilidad o migraciones seguras de servidor.
- El paquete V1 contiene 30 PNG; las cinco nuevas completan el detalle de los mismos cinco Issues. No se ejecutó un análisis nuevo para generarlos.
- Se aplicaron project-guardian y academic-traceability para preservar contratos/historia y separar evidencia visual, resultados documentados y propuestas. El alcance explícito mantiene este reporte en evidencias/v1; no se editaron PROGRESS, matrices RF ni documentación histórica.
- Se conservaron sin cambios los dos reportes de auditoría y los tres documentos Sonar de referencia. Tampoco se leyó el archivo de token ni se utilizó autenticación en esta tarea.
- La rama verificada fue chore/sonarqube-macos-setup. El árbol ya tenía cambios previos en .gitignore, docker/php/Dockerfile y docker/php/php.ini, además de archivos sin rastrear de preparación; se preservaron y no se atribuyen a esta continuación.
- No se corrigió código durante esta tarea. No se modificaron app/, resources/, routes/, database/, tests/, sonar-project.properties, Dockerfile ni php.ini.
- No se hicieron git add, commit, push, merge ni cambios de rama. No se ejecutaron pruebas, scanner ni formatters: no son necesarios para renombrar archivos y están expresamente fuera de alcance.
- Validación de organización: conteo y hashes de imágenes conservados; enlaces locales y estructura del reporte revisados; controles Git de cierre sin cambios adicionales al alcance. Los PNG estaban sin rastrear, por lo que Git no presenta necesariamente sus movimientos como renames; el mapa y los hashes respaldan la trazabilidad.
- La evidencia no permite afirmar ausencia de todos los defectos, explotabilidad de los hallazgos de seguridad ni cumplimiento integral de calidad. Solo respalda las observaciones y resultados delimitados en este reporte.

## Capturas duplicadas o redundantes

**0 duplicados idénticos por SHA-256.** Se identifican **3 capturas redundantes respecto de sus principales**, distribuidas en **2 grupos** de contenido visual semejante. No son tres pares idénticos ni tres Issues adicionales. No se borró ninguna.

| Archivo | Equivalente | Recomendación |
| --- | --- | --- |
| [V1_07_Issues_Code_Smells.png](V1_07_Issues_Code_Smells.png) | [V1_09_Reliability_Issues.png](V1_09_Reliability_Issues.png) | Conservar como respaldo del listado sin filtro. Mismas tres tarjetas; 09 documenta el filtro Reliability. No usar ambas seguidas salvo para explicar el filtro. |
| [V1_12_Uncovered_Lines.png](V1_12_Uncovered_Lines.png) | [V1_05_Coverage.png](V1_05_Coverage.png) | Conservar; presenta los mismos porcentajes/líneas sin cubrir con otra métrica seleccionada y orden de columnas. Usar 05 como principal. |
| [V1_13_Line_Coverage.png](V1_13_Line_Coverage.png) | [V1_05_Coverage.png](V1_05_Coverage.png) | Conservar como respaldo: en V1 Line Coverage y Coverage coinciden. No generalizar esa equivalencia a futuros reportes con condiciones/ramas. |

Los detalles nuevos 26–30 **no son duplicados** de 08–10: permiten leer la regla y el contexto individual. Las vistas de complejidad, ratings y esfuerzo tampoco son duplicados solo por compartir interfaz. El listado global 25 y la métrica numérica 21 son respaldos opcionales por pertinencia para la exposición, no duplicados adicionales.
