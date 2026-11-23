# Reporte de generación de diagramas Draw.io

## Corte, recuperación y alcance

03/11/2026. Rama `chore/sonarqube-macos-setup`; HEAD `b345d9c97077d1589a06d98ddfa9c6879ded58d1`. Al recuperar el estado al inicio de esta continuación no existía `docs/metologia/diagramas/`: **0 diagramas encontrados y 0 completos**. Se recuperaron datos y extracciones temporales de la sesión académica; no se reinvestigaron artículos ni se reconstruyeron matrices. No es posible atribuir un último `.drawio` procesado a la sesión interrumpida porque no había uno persistido. El primer pendiente real era 01; la generación concluyó en 16 y luego se revisó el conjunto.

Resultado: **16/16 archivos editables, 50 páginas, 0 diagramas faltantes**. Los SVG/PNG son secundarios. No se reemplazaron originales, ni se regeneraron Word/PPT/matrices. `docs/PROGRESS.md` recibe únicamente el registro documental exigido por el gobierno del repositorio, preservando el cambio académico previo.

## Fuentes utilizadas

Se reutilizó el estado académico validado. Word final y PPT se consultaron mediante extracción de texto completa; matrices de requisitos, procesos, trazabilidad, doble entrada, artículos y operacionalización se leyeron sin escribirlas. Se contrastaron las relaciones necesarias con F2/F3/F5/F8, F2–F9, código, pruebas, Compose y Git local. Rutas específicas para cada diagrama en [descripciones](documentacion/DESCRIPCION_DIAGRAMAS.md); hashes de fuentes y entregables en [manifiesto](documentacion/MANIFIESTO_DIAGRAMAS.json).

No se accedió al token privado, a datos de bases ni a configuración global. No se ejecutaron suites, scanner, builds, migraciones o servicios: esta fase modifica solo documentación y su validación es proporcional a ese alcance.

## Inventario y validación

| ID | Páginas | XML | XSD | Editable | Estado |
| --- | --- | --- | --- | --- | --- |
| 01 | 1 | Válido | Válido | Sí | Completo documentalmente; revisión nativa pendiente |
| 02 | 3 | Válido | Válido | Sí | Completo documentalmente; revisión nativa pendiente |
| 03 | 3 | Válido | Válido | Sí | Completo documentalmente; revisión nativa pendiente |
| 04 | 6 | Válido | Válido | Sí | Completo documentalmente; revisión nativa pendiente |
| 05 | 5 | Válido | Válido | Sí | Completo documentalmente; revisión nativa pendiente |
| 06 | 1 | Válido | Válido | Sí | Completo documentalmente; revisión nativa pendiente |
| 07 | 2 | Válido | Válido | Sí | Completo documentalmente; revisión nativa pendiente |
| 08 | 2 | Válido | Válido | Sí | Completo documentalmente; revisión nativa pendiente |
| 09 | 2 | Válido | Válido | Sí | Completo documentalmente; revisión nativa pendiente |
| 10 | 8 | Válido | Válido | Sí | Completo documentalmente; revisión nativa pendiente |
| 11 | 1 | Válido | Válido | Sí | Completo documentalmente; revisión nativa pendiente |
| 12 | 2 | Válido | Válido | Sí | Completo documentalmente; revisión nativa pendiente |
| 13 | 9 | Válido | Válido | Sí | Completo documentalmente; revisión nativa pendiente |
| 14 | 1 | Válido | Válido | Sí | Completo documentalmente; revisión nativa pendiente |
| 15 | 2 | Válido | Válido | Sí | Completo documentalmente; revisión nativa pendiente |
| 16 | 2 | Válido | Válido | Sí | Completo documentalmente; revisión nativa pendiente |

### Comprobaciones ejecutadas

- Parseo de XML completo, raíz `mxfile`, al menos un `diagram` con `mxGraphModel/root/mxCell`, vértices no vacíos y referencias de padres/origen/destino válidas. Sin archivos truncados.
- Esquema oficial `mxfile.xsd`: 16/16 válidos. Se consultó un XSD declarativo, no se instaló ejecutable externo.
- Etiquetas, IDs semánticos, coordenadas, pertenencia a contenedores, ausencia de superposición de cajas y límites de lienzo. Esas pruebas geométricas no sustituyen inspección visual de conectores.
- 50 páginas revisadas en vistas de conjunto; páginas densas/especiales revisadas ampliadas. Se corrigieron cruces de conectores, etiqueta de relación que invadía un borde, una nota que cruzaba una flecha y espacio insuficiente al pie. Solo se reescribieron los diagramas que presentaron esos defectos; los demás se conservaron.
- Vistas PNG verificadas por decodificación, dimensiones y correspondencia con cada SVG. El render local espera fuentes y repintado para evitar artefactos de captura del navegador.
- Contenido editable: cajas, notas, actores UML, elipses de casos de uso, cilindros, swimlanes/contenedores, textos y aristas nativas. No hay capturas rasterizadas dentro de los `.drawio`.
- Metadatos `sourceRef`, `evidenceState` y `semanticId` por objeto facilitan auditoría; no introducen nuevos requisitos.

## Exportación: resultado y limitaciones

**50 SVG y 50 PNG auxiliares locales**, una pareja por página, en `exportados/`. Las primitivas se dibujaron desde las mismas etiquetas/geometrías que el XML y se renderizaron con Chrome headless aislado, sin modificar perfil ni configuración global. El original editable sigue siendo el `.drawio`. Estas vistas no contienen la semántica editable completa de diagrams.net y pueden diferir de sus detalles de enrutamiento o forma.

**Exportación nativa: PENDIENTE — .DRAWIO VALIDADO.** No existe draw.io Desktop utilizable. El intento de modo embed web no recibió inicialización utilizable dentro del tiempo acotado, incluso al repetir el diagnóstico de conexión; se detuvo ese enfoque. No se instaló aplicación ni se forzó automatización, permisos o configuración del sistema. No se verificó apertura interactiva en diagrams.net, por lo que no se presenta como comprobada. La validación XML/XSD es evidencia estructural, no un sustituto de ese paso.

Referencias técnicas oficiales consultadas: [generación XML](https://www.drawio.com/docs/reference/diagram-generation/), [modo embed](https://www.drawio.com/docs/reference/embed-mode/), [exportación](https://www.drawio.com/docs/manual/export/export-diagram/) y [XSD de mxfile](https://raw.githubusercontent.com/jgraph/drawio-mcp/main/shared/mxfile.xsd). Ninguna de estas consultas reinició la investigación científica.

## Conteos y discrepancias conservadas

| Concepto | Fuente académica | Diagramas / criterio |
| --- | --- | --- |
| Artículos | 20 identidades | 20 ART únicos; se repiten por dimensión solo cuando la matriz marca X |
| RF | RF-01 a RF-27 | Se conserva línea base de 27; RF-29 experimental no se suma |
| RNF académicos | 10 | No se reemplazan por otros catálogos técnicos |
| Casos de uso académicos | 20 | CU-01…CU-20; RF-27 transversal no origina CU-21 |
| Macroprocesos | 2 propuestos | MP-01 / MP-02; no procesos institucionales certificados |
| Procedimientos | 7 | PR-01…PR-07 |
| Actividades / funciones | 33 / 33 | 33 pares ACT–FUN en siete páginas de detalle |
| Metodología | Markdown 12 etapas; matriz 13 desagregaciones | Se preserva agrupación de 12; no se cambia silenciosamente ninguna fuente |

Otros catálogos históricos de CU/RNF divergen, como ya indica la documentación académica: no se fusionan con los 20 CU/10 RNF de esta entrega. TO-BE conserva TB-30 como auditoría transversal; no es una contratación ni una actividad posterior al cierre. El RF-29 opcional representa riesgo de demora del proceso, nunca selección de candidatos.

## Advertencias académicas y relaciones no demostradas

1. AS-IS PRELIMINAR / PENDIENTE DE VALIDACIÓN INSTITUCIONAL; no herramientas ni tiempos del colegio inventados. TO-BE es una propuesta trazada a funciones reales.
2. Jerarquía 2→7→33→33 adoptada por la plantilla; no se atribuye como obligación literal de ISO 9001.
3. AI-DLC COMO MARCO DE CONTRASTE: no aplicación formal desde el inicio. Intent/Unit/Bolt y operación IA productiva no demostrados; white paper AWS no cuenta como artículo peer reviewed adicional.
4. Metodología humano IA reconstruida y variables propuestas: antes/después no demuestra causalidad. Eficiencia sigue pendiente de esfuerzo/costos/retrabajo y comparación controlada.
5. Los 20 artículos conservan validación bibliográfica previa; métodos/muestras/texto completo pendientes según catálogo. No se convierten relaciones temáticas en prueba de eficacia en el colegio.
6. Sonar V1/V2 es histórico: Issues 5→0, Vulnerabilities 2→0, Code Smells 3→0, Bugs/Hotspots/duplicación en 0. V1 Gate OK con `conditions: []`; V2 inicial ERROR, New Code 1.7 %. Final Gate OK por Small Changes con `ignoredConditions=true`, New Code 50 % (1/2 líneas elegibles; 11 líneas nuevas productivas), **no 80 %**. Global 66.5→69.5 % implica clasificación distinta de tests, no cobertura frontend nueva; app/ permanece 89.6 %. No LCOV importado, sidebar.tsx:621 pendiente.
7. Git es fotografía local sin fetch. `main`/`develop` locales no coinciden con referencias remotas disponibles; no se importaron estados remotos F35-SBX a esta rama. Estrategia documentada no equivale a GitFlow histórico perfecto. CI configurada no prueba ejecución de hoy, CD ni producción.
8. Diagramas de proceso son swimlanes/documentación, no BPMN ejecutable. Casos de uso son visualización del catálogo académico, no validación por sí mismos de todos los RF.

## Recomendaciones de revisión y uso

Abrir cada `.drawio` en diagrams.net, recorrer todas las páginas por su nombre y comprobar textos/conectores en el motor nativo. Exportar SVG/PNG nativos después de la aprobación visual; conservar estos originales editables. En Word utilizar vistas generales y anexos con detalle; en PPT elegir páginas y evitar miniaturizar tablas/rutas. Conservar proporciones, contraste, fuente legible y descripción textual.

No se realizaron staging, commit, push, merge, cambio de rama, corrección de software ni modificaciones a Docker/configuración/dependencias. Las evidencias V1/V2, los originales y entregables académicos previos se preservaron. El control de integridad final se registra en `documentacion/VALIDACION_DIAGRAMAS.json`.
