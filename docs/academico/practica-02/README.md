# Práctica 02 — Formato 02: Análisis del proceso

Entregable de la Práctica 02 (Fase 27B): análisis del proceso actual de reclutamiento, evaluación y selección de personal del Colegio Andino de Huancayo.

**Estado: AS-IS PRELIMINAR sujeto a validación institucional.** Es una reconstrucción del equipo. RR. HH. y la Administración del Colegio no lo han validado, y no describe el software implementado.

## Contenido

| Archivo | Qué es |
|---|---|
| [`F2_Analisis_del_Proceso_Colegio_Andino.docx`](F2_Analisis_del_Proceso_Colegio_Andino.docx) | **Entregable**, sobre la plantilla oficial del Formato 02 |
| [`F2_Analisis_del_Proceso_Colegio_Andino.pdf`](F2_Analisis_del_Proceso_Colegio_Andino.pdf) | Copia en PDF exportada con Microsoft Word |
| [`F2_Analisis_del_Proceso_Colegio_Andino.md`](F2_Analisis_del_Proceso_Colegio_Andino.md) | Espejo en Markdown del mismo contenido, para revisarlo en Git |
| [`diagramas/draft/`](diagramas/draft/) | Borrador del diagrama de flujo AS-IS en dos partes (PNG) |
| [`evidencias/`](evidencias/README.md) | Evidencias del repositorio con su ruta y su SHA-256 |

## Qué contiene el formato

- **Datos generales:** proyecto, equipo, institución, proceso, docente y fecha.
- **Descripción del proceso:** nombre, propósito, contexto y alcance (inicio y fin).
- **Diagrama de flujo AS-IS:** borrador en dos partes.
- **Actividades:** las 14 actividades AS-01 a AS-14. Desagregan las 8 actividades macro versionadas en [`docs/final-report/03-procesos-negocio.md`](../../final-report/03-procesos-negocio.md) §3.1 e indican de cuál viene cada una.
- **Actores:** los 5 actores del AS-IS (AA-01 a AA-05).
- **Relación actividades-actores:** quién ejecuta, recibe o valida cada actividad.
- **Observaciones:** O-01 a O-07, sin proponer soluciones.
- **Evidencias** del repositorio.

## Limitaciones

- **Sin documentación institucional verificada** en el repositorio: estadísticas, herramientas, organigrama y procedimientos. Canales, formatos, tiempos y responsables reales no se afirman.
- **Evaluadores del AS-IS:** su cargo concreto no está verificado.
- **Candidatos no preseleccionados:** no está verificado si se les informa (AS-09).
- **Diagrama AC-01 de la v1.1:** modela el software ya construido, no el proceso institucional. Por eso **no** se usa como AS-IS.
- **BPMN AS-IS original del equipo:** no está versionado ([`01-bpmn-as-is-report.md`](../../final-report/diagram-reports/01-bpmn-as-is-report.md)).
- **Cierre del rótulo «preliminar»:** depende de la validación con RR. HH. o la Administración del Colegio.

## Cómo se regenera

Desde la raíz del repositorio:

```
python docs/academico/tools/f27b/build.py f2
```

El generador lee la plantilla de [`00-fuentes-oficiales`](../00-fuentes-oficiales/README.md) sin modificarla. El PDF se exporta con Microsoft Word (ver [`tools/f27b/README.md`](../tools/f27b/README.md)).
