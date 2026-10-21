# Capturas manuales V2 — Antes vs Después

## Estado y reglas

Las capturas aún **NO existen** en esta carpeta. No se copiaron imágenes V1 ni se generó Word V2.
V1 quedó congelada con 30 imágenes, Markdown y Word. Repetir las mismas vistas permite una comparación honesta.

Proyecto: `saas-reclutamiento-multiempresa`, versión 1.1.
Análisis V2: `fad88726-7762-4095-bbe0-7239f78be6ac`, 20/10/2026 20:35:44 America/Lima.
Dashboard: [abrir proyecto local](http://localhost:9000/dashboard?id=saas-reclutamiento-multiempresa).

**Mostrar los resultados reales:** Quality Gate ERROR por New Code Coverage 1.7 % (<80 %); Overall Coverage 65.6 %, app 89.6 %, 0 Issues abiertos, 0 vulnerabilidades, 0 Code Smells, 0 Bugs y 0 Hotspots. Duplicación 0.0 %; complejidad ciclomática 2067, cognitiva 689. Los 5 Issues históricos están FIXED.

No ejecutar otro scanner ni cambiar filtros/configuración permanentemente antes de capturar esta línea base. Cambiar filtros de visualización para encontrar Issues cerrados no equivale a cambiar su estado.
Nunca mostrar token, archivo privado, .env, credenciales ni Terminal con secretos. Capturar la vista de Sonar completa, con ruta/sección y valores legibles; mantener PNG original y proporción. No sustituir una pantalla por otra parecida.

## Inventario exacto a repetir

Los nombres siguientes conservan la numeración y correspondencia real de V1. Todo permanece pendiente hasta que el usuario agregue cada captura.

| N° | Archivo esperado | Pantalla / indicación | Estado |
|---|---|---|---|
| 01 | `V2_01_Dashboard.png` | Overview actualizado: Gate ERROR, 0 Issues, Coverage 65.6 %, duplicación 0.0 %. | PENDIENTE |
| 02 | `V2_02_Quality_Gate.png` | Summary del segundo análisis: Failed / ERROR; separar New Code y Overall Code. | PENDIENTE |
| 03 | `V2_03_Quality_Gate_Conditions.png` | Sonar way y condiciones; añadir también V2_31 para la condición evaluada que falla. | PENDIENTE |
| 04 | `V2_04_Measures_Coverage_Overview.png` | Measures; gráfico Coverage Overview | PENDIENTE |
| 05 | `V2_05_Coverage.png` | Coverage: global 65.6 %, app 89.6 %, resources/js y routes 0.0 %. | PENDIENTE |
| 06 | `V2_06_Issues_Overview.png` | Issues abiertos sin filtros: 0. No confundir con los 5 históricos cerrados. | PENDIENTE |
| 07 | `V2_07_Issues_Code_Smells.png` | Vista equivalente del listado; 0 Code Smells abiertos. Los históricos FIXED van en 28–30 y 33. | PENDIENTE |
| 08 | `V2_08_Security_Issues.png` | Filtro Security; 0 Issues abiertos de seguridad. | PENDIENTE |
| 09 | `V2_09_Reliability_Issues.png` | Filtro Reliability; 0 Issues abiertos MQR. | PENDIENTE |
| 10 | `V2_10_Maintainability_Issues.png` | Filtro Maintainability; 0 Issues abiertos MQR. | PENDIENTE |
| 11 | `V2_11_Lines_To_Cover.png` | Measures; líneas a cubrir por directorio | PENDIENTE |
| 12 | `V2_12_Uncovered_Lines.png` | Measures; líneas sin cubrir por directorio | PENDIENTE |
| 13 | `V2_13_Line_Coverage.png` | Measures; Line Coverage por directorio | PENDIENTE |
| 14 | `V2_14_Duplications_Overview.png` | Measures; duplicación cero; gráfico vacío | PENDIENTE |
| 15 | `V2_15_Cyclomatic_Complexity.png` | Measures; complejidad ciclomática 2067. | PENDIENTE |
| 16 | `V2_16_Cognitive_Complexity.png` | Measures; complejidad cognitiva 689. | PENDIENTE |
| 17 | `V2_17_Reliability_MQR_Overview.png` | Measures; Reliability MQR, 0 Issues, rating A. | PENDIENTE |
| 18 | `V2_18_Reliability_MQR_By_Directory.png` | Measures; impactos Reliability por directorio, total 0. | PENDIENTE |
| 19 | `V2_19_Reliability_MQR_Rating.png` | Measures; Reliability MQR A global. | PENDIENTE |
| 20 | `V2_20_Reliability_MQR_Remediation.png` | Repetir la vista de remediación Reliability y registrar el valor que muestre la UI, sin reutilizar los 30 min V1. | PENDIENTE |
| 21 | `V2_21_Reliability_MQR_Severity.png` | Repetir agregación numérica de severidad Reliability; capturar el valor actual, no el 15 de V1. | PENDIENTE |
| 22 | `V2_22_Maintainability_MQR_Rating.png` | Measures; Maintainability MQR A, 0 Issues, deuda 0 min. | PENDIENTE |
| 23 | `V2_23_Security_Hotspots_Review_Rating.png` | Measures; Hotspots 0 y Review Rating que muestre actualmente la UI. | PENDIENTE |
| 24 | `V2_24_Lines_Of_Code.png` | Measures; ncloc 19597 y desglose. | PENDIENTE |
| 25 | `V2_25_Projects_Overview.png` | Listado global; identificar la tarjeta actualizada del SaaS. | PENDIENTE |
| 26 | `V2_26_Vulnerability_PHP_S5693.png` | Buscar el ID original de la regla php:S5693 incluyendo cerrados; mostrar estado FIXED y código actualizado. | PENDIENTE |
| 27 | `V2_27_Vulnerability_TS_S2245.png` | Buscar el ID original de la regla typescript:S2245 incluyendo cerrados; mostrar estado FIXED y código actualizado. | PENDIENTE |
| 28 | `V2_28_CodeSmell_TS_S6843.png` | Buscar el ID original de la regla typescript:S6843 incluyendo cerrados; mostrar estado FIXED y código actualizado. | PENDIENTE |
| 29 | `V2_29_CodeSmell_TS_S8786.png` | Buscar el ID original de la regla typescript:S8786 incluyendo cerrados; mostrar estado FIXED y código actualizado. | PENDIENTE |
| 30 | `V2_30_CodeSmell_TS_S6671.png` | Buscar el ID original de la regla typescript:S6671 incluyendo cerrados; mostrar estado FIXED y código actualizado. | PENDIENTE |

Las vistas 07, 12 y 13 eran redundantes pero se conservaron en V1: repetirlas sirve como respaldo, sin contabilizar métricas dos veces. 09 y 17–21 son Reliability **MQR**; no atribuirles Bugs tradicionales. 23 muestra Review Rating, no un listado detallado de hotspots.

## Evidencias adicionales imprescindibles en V2

| Archivo esperado | Qué debe mostrar | Estado |
|---|---|---|
| `V2_31_Quality_Gate_Failed_New_Code_Coverage.png` | Condiciones realmente evaluadas: new_coverage 1.7 % ERROR; duplicación nueva 0.0 % OK; nuevos Issues 0 OK. | PENDIENTE |
| `V2_32_New_Code_Coverage.png` | Medida de código nuevo: 60 líneas a cubrir, 59 sin cubrir; no confundir con 65.6 % global. | PENDIENTE |
| `V2_33_Issues_Fixed_History.png` | Lista de los cinco Issues originales con estado FIXED/CLOSED; filtro que incluya cerrados. | PENDIENTE |
| `V2_34_Analysis_History.png` | Historial con V1 y V2 del mismo proyecto, fechas e identificación del segundo análisis. | PENDIENTE |

## Cómo localizar los detalles resueltos (26–30)

En Issues, quitar el filtro exclusivo de abiertos y buscar por regla/estado Fixed. También se puede usar el ID del Issue en la búsqueda/enlace de detalle que ofrece la UI. No pulsar acciones para cambiar su clasificación o resolución.

| Captura | Regla | ID original recuperable |
|---|---|---|
| 26 | php:S5693 | b5c887a2-2ac3-439b-8a22-c3a9023d5c3e |
| 27 | typescript:S2245 | 6fce6299-f9af-4975-a5b1-5b7481b15809 |
| 28 | typescript:S6843 | 1ddb8eca-b699-4e59-a7e8-a4ffc0433ce2 |
| 29 | typescript:S8786 | 2fd88a22-9d7b-4851-a848-ead901106d67 |
| 30 | typescript:S6671 | 0911fd6d-79b0-48b8-a5e8-edb9e14bf243 |

Si la UI no muestra código actual para un Issue cerrado, conservar la captura de su estado y señalar la limitación; no usar una imagen V1 como si fuera V2. Las pantallas vacías de Issues son evidencia válida cuando se ve claramente proyecto, filtro y contador cero.

## Checklist para entregar las capturas

- [ ] Dashboard V2, Summary / Quality Gate y condiciones de Sonar way.
- [ ] Measures y Coverage global/desglose, sin ocultar 0.0 % frontend/rutas.
- [ ] Gate ERROR y cobertura nueva 1.7 % (31–32).
- [ ] Issues abiertos 0 y los 5 históricos FIXED (06, 26–30, 33).
- [ ] Security, Reliability y Maintainability con el modo MQR identificado.
- [ ] Duplicaciones, líneas de código y ambas complejidades.
- [ ] Hotspots / Review Rating, sin afirmar vulnerabilidades por un hotspot.
- [ ] Historial V1/V2 del mismo proyecto (34).
- [ ] Todas las imágenes legibles, sin secretos y sin sobreescribir V1.
- [ ] Avisar que las capturas están listas para revisar y preparar el Word comparativo; no generarlo todavía.

Resultados y explicación: [reporte V2 preliminar](REPORTE_RESULTADOS_V2_PRELIMINAR.md).
