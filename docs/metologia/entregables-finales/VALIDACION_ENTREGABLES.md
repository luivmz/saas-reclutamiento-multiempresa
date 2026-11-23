# Validación de entregables académicos

Fecha: 03/11/2026. Resultado técnico documental: sin errores detectados en las comprobaciones ejecutadas. La validación de archivos no sustituye la validación institucional ni un experimento causal.

| Área | Resultado comprobado | Evidencia |
|---|---|---|
| Rama y HEAD | chore/sonarqube-macos-setup; commit conservado | Git y baseline SHA-256 |
| Cinco fuentes | Hashes originales conservados | ../evidencias/MANIFIESTO_PLANTILLAS.json |
| Archivos rastreados | De 1195 originales, solo docs/PROGRESS.md cambió; ningún código funcional | Comparación SHA-256 |
| DOCX | Reabierto y renderizado; 49 páginas | ../evidencias/VALIDACION_ENTREGABLES.json |
| Estructura Word | 14 capítulos; 53 epígrafes exigidos + 5.6, 5.7 y 5.8 | Texto/XML y páginas |
| Imágenes Word | Diez figuras y logo embebidos; rutas a originales conservadas | Paquete DOCX |
| Instrucciones | Sin comentarios activos, texto rojo instructivo ni placeholders detectados | XML y revisión visual |
| Índice | Páginas cotejadas con render final; campo TOC actualizable | Índice y títulos |
| PPTX | 24 diapositivas, integridad, geometría, Arial y reimportación aprobadas | ../evidencias/VALIDACION_PPT.json |
| PPT editable | Cuatro tablas y un gráfico con workbook embebido | Paquete PPTX |
| PPT visual | Sin ejemplos de salud, placeholders ni elementos fuera del slide detectados | Render de las 24 diapositivas |
| Bibliografía | 20 identidades: 19 DOI cotejados; SWE-bench conserva acta sin inventar DOI | ../fuentes/REGISTROS_CROSSREF.json |
| Siete XLSX | Reabiertos; hojas, encabezados y filas comprobados; sin celdas error ni #REF! | ../evidencias/VALIDACION_ENTREGABLES.json |
| Excel de procesos | Siete hojas, anchos, combinaciones y validación M2:M56 conservados | Comparación con original |
| Caso académico | Sin SIGEMAD/Gestión-MPA en contenido propio de libros finales | Barrido de celdas |
| Doble entrada | Nueve hojas; siete requeridas más catálogo y registro; 20 artículos consistentes | Comparación de celdas con datos |
| Trazabilidad | 33 rutas funcionales y 26 referencias distintas de tests; métodos PHP existentes | Matriz de funciones y lectura de código |
| Requisitos | 27 RF + 10 RNF; test concreto o PENDIENTE explícito | Matrices de requisitos/doble entrada |
| Secretos | Sin tokens o asignaciones de credenciales detectados en textos/XML nuevos | Comprobación sin imprimir valores |
| Git | diff --check sin errores; sin staging, commit, push o merge | Git final |

Los PNG y PDF usados internamente para revisar Office no se adjuntan como entregables finales. Las figuras complejas conservan su fuente para ampliación; la paginación puede variar al actualizar el índice en otra versión de Word.

## Límites explícitos

Reabrir con librerías, reimportar y renderizar no equivale a controlar Microsoft Word/Excel/PowerPoint nativos. La apertura en las aplicaciones del equipo de exposición queda para revisión humana final. Se verificó identidad y contenido consultado de artículos; los campos de lectura completa pendientes se declaran. Trece publicaciones tienen revisión clasificada al nivel del venue, sin dictámenes privados. AI-DLC es una fuente técnica separada.

No se ejecutaron suites del SaaS: el alcance es documental. Las cifras Sonar/PHPUnit/Vitest son HISTÓRICAS. No se modificaron cobertura, Gate, contenedores, datos, código, tests, dependencias o configuración. No se crearon nuevos diagramas en esta continuación.

## Registros

- ../evidencias/VALIDACION_ENTREGABLES.json: comprobaciones por archivo y hashes de los nueve artefactos Office.
- ../evidencias/VALIDACION_PPT.json: recibo de integridad/geometría del PPT final.
- ../evidencias/MANIFIESTO_PLANTILLAS.json: cinco fuentes preservadas.
- ../evidencias/INVENTARIO_REPOSITORIO.json: evidencia del repositorio.
- ../fuentes/ESTRUCTURA_MATRIZ_REGISTRO.json: todas las celdas no vacías del registro original.
- ../fuentes/ANALISIS_AI_DLC_Y_REGISTRO.md: ocho páginas y 27 criterios analizados; alertas de fórmulas del ejemplo.
