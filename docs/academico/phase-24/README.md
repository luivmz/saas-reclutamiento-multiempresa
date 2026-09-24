# Formato 09 — Alcance del proyecto software (Fase 24)

Material académico del Formato 09 del curso Pruebas y Calidad de Software (NRC 28607, Universidad Continental), para el proyecto *Análisis y Diseño de una Plataforma SaaS Multiempresa para la gestión del reclutamiento, evaluación y selección de personal — Caso de estudio: Colegio Andino de Huancayo*.

## Qué hay que presentar al docente

**[`output/F9_Alcance_Proyecto_Software_Colegio_Andino_FINAL_v1.1.docx`](output/F9_Alcance_Proyecto_Software_Colegio_Andino_FINAL_v1.1.docx)**, con su copia en PDF [`output/F9_Alcance_Proyecto_Software_Colegio_Andino_FINAL_v1.1.pdf`](output/F9_Alcance_Proyecto_Software_Colegio_Andino_FINAL_v1.1.pdf) (28 páginas). Microsoft Word exportó el PDF desde ese mismo DOCX.

Los tres DOCX de la raíz son **fuentes**: no se entregan y no se modifican.

## Archivos

| Archivo | Qué es | Papel en la Fase 24 |
|---|---|---|
| `GUÍA PRÁCTICA 09.docx` | Guía oficial de la práctica 9 (NRC 28607, Dr. Maglioni Arana Caparachin) | Fuente de **instrucciones**: propósito, actividades 1 a 5 y entregables (contexto, incluidas, excluidas, límites y alcance validado) |
| `Formato 09 Alcance del proyecto software.docx` | Plantilla oficial vacía | Fuente de **estructura**: siete apartados y sus campos (datos generales, contexto, objetivos, IN/OUT, límites, restricciones y supuestos, criterios de aceptación) |
| `F9_Alcance_Proyecto_Software_Colegio_Andino_NRC30180.docx` | Formato 09 desarrollado por el equipo, versión 1.0 del 20/09/2026 | **Documento histórico** y base principal de contenido. Usa el NRC 30180, que no es el vigente |
| `output/…FINAL_v1.1.docx` | **Entregable final**, versión 1.1 del 24/09/2026 | Actualización del documento histórico al estado v1.1, con NRC 28607 |
| `output/…FINAL_v1.1.pdf` | PDF del entregable final | Copia para lectura e impresión |
| [`source-map.md`](source-map.md) | Mapa de fuentes | De dónde sale cada sección del entregable y qué cambió respecto de la versión 1.0 |
| `tools/` | Scripts de construcción y validación | Permiten reproducir y verificar el entregable (ver abajo) |

SHA-256 de los originales, idénticos antes y después de la fase:

```
89d3f2783941b11aa7be0ccba7450cec5b6a821c480e528ac23d20e7e6c37c6d  GUÍA PRÁCTICA 09.docx
1fe92a08110c9e4cad18644fa01d3baf38cba807a6db054c1a7276a69c0cfc63  Formato 09 Alcance del proyecto software.docx
1bb2fd17fbeea600f9fa6a36a2ceb4ed1c21b2f2fbba2c57a2ea8f618512a72a  F9_Alcance_Proyecto_Software_Colegio_Andino_NRC30180.docx
```

## Anexos del entregable

Los anexos están **dentro** del DOCX y del PDF:

| Anexo | Contenido | Fuente |
|---|---|---|
| A | Proceso TO-BE propuesto (BPMN) | Imagen del documento histórico, con leyenda actualizada |
| B | Casos de uso, UML AS-IS v1.1 (UC-01) | [`docs/v1.1/powerdesigner/exports/UC-01-casos-de-uso.png`](../../v1.1/powerdesigner/exports/UC-01-casos-de-uso.png), girado 90° |
| C | Componentes (CO-01) | [`CO-01-componentes.png`](../../v1.1/powerdesigner/exports/CO-01-componentes.png) |
| D | Despliegue (DE-01) | [`DE-01-despliegue.png`](../../v1.1/powerdesigner/exports/DE-01-despliegue.png), girado 90° |
| E | Actividad del proceso de reclutamiento (AC-01) | [`AC-01-proceso-reclutamiento.png`](../../v1.1/powerdesigner/exports/AC-01-proceso-reclutamiento.png) |
| F | Clases del dominio (CL-01) | [`CL-01-clases-del-dominio.png`](../../v1.1/powerdesigner/exports/CL-01-clases-del-dominio.png) |

En el DOCX los diagramas se ven a tamaño de página. Para leerlos al detalle conviene usar los PNG y SVG de [`docs/v1.1/powerdesigner/exports/`](../../v1.1/powerdesigner/exports/). Los anexos B y C de la versión 1.0 (casos de uso y arquitectura conceptual) **se sustituyeron**: incluían actores y servicios fuera del alcance, como el Superadministrador SaaS, las suscripciones y planes o el banco de talentos. Siguen disponibles en el documento histórico.

## Reproducir y validar

Los scripts de `tools/` usan solo Python 3 de la biblioteca estándar, Swift/PDFKit de macOS y Microsoft Word para Mac. No instalan nada.

```
# 1. construir (sin índice) → 2. exportar a PDF con Word → 3. calcular páginas → 4. reconstruir con índice
python3 tools/build.py <F9 histórico.docx> <salida.docx> docs/v1.1/powerdesigner/exports -
tools/topdf.sh <salida.docx> <salida.pdf>
swiftc -O tools/pdftext.swift -o pdftext && ./pdftext <salida.pdf> > salida.txt
python3 tools/toc.py salida.txt toc.json
python3 tools/build.py <F9 histórico.docx> <salida.docx> docs/v1.1/powerdesigner/exports toc.json
# validar
python3 tools/validate_f9.py <salida.docx> salida.txt
```

`build.py` edita `word/document.xml` como texto, sin reserializar el XML. Así se conservan la portada, los estilos, el encabezado con el logotipo, el pie con la numeración y el borde de página del documento histórico. `topdf.sh` trabaja en el contenedor de Word (`~/Library/Containers/com.microsoft.Word/Data/`), porque Word para Mac no puede escribir fuera de él. Detalle de la validación en [`docs/v1.1/phase-24-academic-documentation.md`](../../v1.1/phase-24-academic-documentation.md) §14.
