# Registro de fuentes y validación F29H v2

Corte del 22/11/2026 en zona America/Lima. Edición documental en un worktree separado, desde origin/develop. Las fuentes de Reportes y de presentación se consultaron por objetos Git y se preservaron como cortes distintos.

| Referencia consultada | SHA completo |
|---|---|
| `origin/main` | `04d3cfa1db6f82d9cda8db2254338805137cdc3c` |
| `origin/develop` | `4371d90e6fb9682fe8076c978f33a3ce5f086b49` |
| `origin/chore/sonarqube-macos-setup` | `5e2eae37f63c7ac5d35ed2def9b2e843a644cd98` |
| `feature/presentacion-dos-videos` | `2b87f3667dce6f98f8250083cc7dd354aa21a961` |
| `design/anfitrion-empleos` | `f9703f4636d7d870cbc4244a61e545a9db1b3a2e` |
| `design/presentacion-astra` | `c1b842a70388211fcee781ebb519d1f0b76e7cbd` |
| `design/presentacion-higgsfield` | `b8f42b581456a23a482bbdfd3b9e1c0ff0dfbfc0` |
| `b1dd8cb` | `b1dd8cb9f7a57edbb2ba746de6bebb132ce4bb5a` |
| `446b8fe` | `446b8fe5efdd697f6c3d7d593f2411bac9585f18` |
| `bb86991` | `bb86991e8313b28a3daa19dafcacb57eb10f62d0` |
| `bc44303` | `bc44303d307004de494c4e03f3186ee190118c4c` |
| `e3f80a1` | `e3f80a157af8c56e0d89bff997d3c7e26f68722a` |

Los árboles de main y develop coinciden en `74f1d82c2bf691638dcfee1c87647519b4bdd12c`. La prueba de ascendencia confirma que el anfitrión hereda los dos vídeos. El commit de Reportes queda en una línea separada y la revisión de ejecución histórica corresponde al árbol de trabajo del 09/11. El código funcional se consultó en rutas, servicios, Policies, migraciones, Compose y workflow.

## Autoridades y expedientes

| Fuente | Uso | SHA-256 |
|---|---|---|
| [Plantilla Estructura de proyecto final (4).docx](plantillas/Plantilla%20Estructura%20de%20proyecto%20final%20%284%29.docx) | Estructura, instrucciones de contenido, 14 capítulos, 53 apartados y los cuatro bloques finales. | `b26cfb21ca627c46d65f8f683422ffca1e022ec60c75132f0d7843b01a03fcda` |
| [PLANTILLA_INFORME_UC_PORTADA_FORMATADA.docx](plantillas/PLANTILLA_INFORME_UC_PORTADA_FORMATADA.docx) | Portada, estilo, tipografía, tamaño de página, márgenes, encabezado/pie y numeración. Se reemplaza el lema de muestra por los datos institucionales comprobados. | `baec7dc4ba90d195d0b5cf3d2111b42fa475e6e7c3171d73246214add28e9a9d` |
| [F29H_Informe_Final_v1_Colegio_Andino.docx](F29H_Informe_Final_v1_Colegio_Andino.docx) | Base histórica F29H. El DOCX se extrajo incluyendo secciones y tablas. El Markdown permitió conservar los requisitos, cronología, capítulos y metodología. | `0d81babae195ea5a50c6dbc41917c4ac5ef08cd7314eba122e03c1c1763f3abd` |
| [F29H_Informe_Final_v1_Colegio_Andino.md](F29H_Informe_Final_v1_Colegio_Andino.md) | Base histórica F29H. El DOCX se extrajo incluyendo secciones y tablas. El Markdown permitió conservar los requisitos, cronología, capítulos y metodología. | `6a36f655dc943e69b461735d83b8d3e616e092ff21f7f670784bdb3fbb14bb72` |
| [F29H_Informe_Final_v1_Colegio_Andino.pdf](F29H_Informe_Final_v1_Colegio_Andino.pdf) | Base histórica F29H. El DOCX se extrajo incluyendo secciones y tablas. El Markdown permitió conservar los requisitos, cronología, capítulos y metodología. | `c56f88f61dcb147d79ace1cf35644b9d5a41f430fa5d0dbc81c05bbe1c75d656` |
| [README.md](README.md) | Referencias y procedimiento histórico v1. | `49becb74b3abb654da386be2ba6bb1e4b66a0c4c874cb1dc202b3815770893cd` |
| [F29H_REGISTRO.md](F29H_REGISTRO.md) | Referencias y procedimiento histórico v1. | `0cc77c0ba4bde9290f1055dc57fa74593ebe835d15dc4446bf04f82f468a6b1a` |

Se extrajeron los párrafos, las celdas, instrucciones, secciones, campos, pies, encabezados y referencias del paquete DOCX. Las plantillas suministradas se copiaron byte por byte desde el worktree original, donde permanecen sus dos archivos sin seguimiento. La edición conserva el borde, logos, folios y esquema tipográfico de la plantilla visual. La página horizontal del PDM adapta las dimensiones con los mismos márgenes.

| Conjunto de fuentes técnicas | Uso en v2 |
|---|---|
| docs/academico, docs/final-report y docs/v1.1 | F2–F11, proceso preliminar, requisitos, diagramas F23, línea base QA y ficha ML-01. |
| docs/metologia, docs/architecture-cypress-reports, docs/sonarqube | Diagramas editables, límites de metodología, pruebas de Reportes, V1/V2/V3 y deuda de herramientas. |
| docs/testing, docs/demo-users, docs/presentacion y docs/experimental | Flujos ficticios, evidencia F37, bandera, ML-02, arranque e incrementos visuales. |

## Procedencia de las figuras

El [inventario reproducible](recursos-v2/figuras.json) guarda cada nombre, SHA del original, SHA de la imagen incrustada, revisión, ruta fuente y recortes. En los PDFs, las figuras de Git tienen un enlace al original. Las capturas locales quedan incluidas como recursos para que el documento pueda regenerarse.

| Figura | Evidencia | Revisión | Procedencia |
|---|---|---|---|
| 1 | Arquitectura general del proyecto grupal | `5e2eae3` | [01_ARQUITECTURA_GENERAL_SAAS_p01.png](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/5e2eae37f63c7ac5d35ed2def9b2e843a644cd98/docs/metologia/diagramas/exportados/01_ARQUITECTURA_GENERAL_SAAS_p01.png) |
| 2 | Secuencia UML de decisión final RF-23 | `04d3cfa` | [SEQ-07-decision-final.png](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/v1.1/powerdesigner/exports/SEQ-07-decision-final.png) |
| 3 | Comparación ponderada y decisión humana | `04d3cfa` | [11-comparacion-1024.png](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/v1.1/phase-21-screenshots/11-comparacion-1024.png) |
| 4 | Despliegue Docker local y SonarQube | `5e2eae3` | [02_DESPLIEGUE_DOCKER_p01.png](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/5e2eae37f63c7ac5d35ed2def9b2e843a644cd98/docs/metologia/diagramas/exportados/02_DESPLIEGUE_DOCKER_p01.png) |
| 5 | Quality Gate de SonarQube V3 | `5e2eae3` | [SONAR-UI-02_Quality_Gate.jpg](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/5e2eae37f63c7ac5d35ed2def9b2e843a644cd98/docs/architecture-cypress-reports/evidencias/sonarqube/SONAR-UI-02_Quality_Gate.jpg) |
| 6 | Proceso AS-IS preliminar del caso | `5e2eae3` | [03_PROCESO_RECLUTAMIENTO_AS_IS_p01.png](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/5e2eae37f63c7ac5d35ed2def9b2e843a644cd98/docs/metologia/diagramas/exportados/03_PROCESO_RECLUTAMIENTO_AS_IS_p01.png) |
| 7 | Proceso TO-BE para el requerimiento | `5e2eae3` | [04_PROCESO_RECLUTAMIENTO_TO_BE_p01.png](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/5e2eae37f63c7ac5d35ed2def9b2e843a644cd98/docs/metologia/diagramas/exportados/04_PROCESO_RECLUTAMIENTO_TO_BE_p01.png) |
| 8 | Actores y casos de uso de requerimientos y vacantes | `5e2eae3` | [05_CASOS_DE_USO_GENERAL_p01.png](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/5e2eae37f63c7ac5d35ed2def9b2e843a644cd98/docs/metologia/diagramas/exportados/05_CASOS_DE_USO_GENERAL_p01.png) |
| 9 | Modelo físico de las tablas del dominio | `04d3cfa` | [PDM-02-tablas-de-dominio.png](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/v1.1/powerdesigner/exports/PDM-02-tablas-de-dominio.png) |
| 10 | Componentes del módulo de Reportes | `5e2eae3` | [17_MODULO_REPORTES_COMPONENTES.png](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/5e2eae37f63c7ac5d35ed2def9b2e843a644cd98/docs/architecture-cypress-reports/arquitectura/diagramas/17_MODULO_REPORTES_COMPONENTES.png) |
| 11 | Reportes filtrados por vacante | `5e2eae3` | [E2E-20-02-filtro-por-vacante.png](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/5e2eae37f63c7ac5d35ed2def9b2e843a644cd98/docs/architecture-cypress-reports/evidencias/reportes/E2E-20-02-filtro-por-vacante.png) |
| 12 | Evidencia versionada y ayuda documental léxica | `446b8fe` | `D:/bt/pres/visual/final/cypress/capturas-e2e-21-evidencias-experimental/e2e-21-escritorio.png` |
| 13 | Panel opcional de riesgo operacional ML-01 | `04d3cfa` | [22-riesgo-operacional-oscuro-1280.png](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/04d3cfa1db6f82d9cda8db2254338805137cdc3c/docs/v1.1/phase-21-screenshots/22-riesgo-operacional-oscuro-1280.png) |
| 14 | Resumen de Cypress de la práctica de Reportes | `5e2eae3` | [CYP_ejecucion2_resumen_terminal.png](https://github.com/luivmz/saas-reclutamiento-multiempresa/blob/5e2eae37f63c7ac5d35ed2def9b2e843a644cd98/docs/architecture-cypress-reports/evidencias/cypress/CYP_ejecucion2_resumen_terminal.png) |
| 15 | Portada con el vídeo del colegio | `2b87f36` | `D:/bt/pres/visual/dos-videos-20261122/portada-claro/apertura.png` |
| 16 | Vídeo de carpeta en una oferta ficticia | `2b87f36` | `D:/bt/pres/visual/dos-videos-20261122/empleo-2-oscuro/apertura.png` |
| 17 | Anfitrión en el listado público de empleos | `b1dd8cb` | `D:/bt/anfitrion/entrega/capturas/claro-4-senala-arriba.png` |

**Selección.** Se conservaron las láminas legibles de procesos y casos de uso. Las exportaciones completas de BPMN, UML y PDM se mantienen enlazadas en el anexo A.1. Se omitieron duplicados, iteraciones visuales anteriores, variantes claro/oscuro repetidas, logs de diagnóstico y pantallas de datos personales. Sonar se recortó al panel pertinente, excluyendo pestañas ajenas. Reportes se recortó a filtros e indicadores. Las dos áreas de evidencia léxica proceden de la misma captura. Los correos y adjuntos privados quedaron fuera.

## Evidencia que permanece fuera de Git

| Conjunto | Ubicación local | Contenido verificado |
|---|---|---|
| Base de presentación | `D:/bt/pres/base/` y `D:/bt/pres/visual/final/` | Guía de main y verificaciones fechadas. La captura E2E-21 insertada proviene del corte visual 446b8fe. |
| Dos vídeos | `D:/bt/pres/visual/dos-videos-20261122/ENTREGA.txt` y sus logs | 81 componentes y E2E-18/22/23 con 8/8, 8/8 y 13/13. Evidencia para el commit 2b87f36. |
| Anfitrión | `D:/bt/anfitrion/entrega/00-RESUMEN.md`, `verificacion/`, `cy-r8/` y `cy-afectadas/` | 89 componentes, E2E-24 con 16/16 y seis specs con 39/39. Corte b1dd8cb, anterior al seeder adicional. |

## Comprobaciones editoriales y límites

- GitHub respondió con repositorio público, homepage vacío y cero despliegues en su API. Actions devolvió success para [main](https://github.com/luivmz/saas-reclutamiento-multiempresa/actions/runs/45080426261) y [develop](https://github.com/luivmz/saas-reclutamiento-multiempresa/actions/runs/45079940215) en los SHA de corte. Se cotejaron 55 enlaces a archivos y directorios con objetos Git.
- En lectura, /health de los proyectos locales en 8000, 8030 y 8040 devolvió database y redis en estado ok. La sonda a FastAPI en 8008 no pudo conectar. El documento cita la ejecución histórica comprobada de F17.
- La tarea no requirió reiniciar bases, ejecutar suites ni repetir SonarScanner. Las cifras del capítulo 13 se atribuyen al código y la fecha de cada ejecución. Los resultados históricos de código nuevo y las herramientas complementarias conservan sus límites.
- El nombre de los integrantes, docente y NRC coinciden con CLAUDE.md y README del proyecto y F29H v1. El formato de portada prioriza la plantilla visual, que carece de campo para códigos de estudiante. El equipo puede completarlos si el curso los solicita.

## Validación del paquete final

- Word de escritorio 16 actualizó los campos y guardó el DOCX a partir del cual exportó el PDF etiquetado. Se contrastaron los 14 títulos de capítulo, los 53 apartados y los cuatro títulos de cierre con la plantilla estructural.
- La comprobación del PDF confirmó 41 páginas, 17 figuras y 30 tablas con foliación en sus índices. La página 36 usa orientación horizontal para el modelo físico. Los encabezados de las tablas se repiten al cambiar de página. Se comprobó el contenido de los campos de índice y referencias, junto con los enlaces internos del PDF.
- Se renderizaron las 41 páginas con Poppler y se revisaron visualmente. La revisión incluyó la portada, la continuidad de tablas e índices, la orientación, el encuadre de figuras y la presencia de su procedencia en la misma página. El archivo fuente de la figura 9 permite ampliar los atributos del modelo.
- SHA-256 del DOCX `12a3642163198c644b79c824f022718ccdf4f75535e8eb183946733eb57bc707`.
- SHA-256 del PDF `e4ff2e9dda20dd1790059e696c495f5ef8d7295f925644082e9dec14ea201308`.

## Pendientes del equipo

1. Confirmar la URL pública de implementación y el commit servido o informar al curso que la entrega es local. No se encontró ese enlace en las fuentes consultadas.
2. Aportar validación institucional del AS-IS y TO-BE y confirmación de la aprobación académica del plan si la asignatura exige constancia. No hay base para agregar firmas.

## Reproducción

Usar Python con python-docx 1.2.0 y Pillow 10.4.0. Ejecutar desde la raíz del worktree. Word de escritorio actualiza y guarda los campos del DOCX, repagina y exporta su PDF etiquetado. Las figuras curadas y ambas plantillas se incluyen en este directorio.

```powershell
python docs/academico/informe-final/generar_informe_v2.py
powershell -NoProfile -File docs/academico/informe-final/exportar_informe_v2.ps1
```
