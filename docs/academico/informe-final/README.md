# F29H — Informe Final v1

Informe final del proyecto sobre la plantilla oficial [`Plantilla_Estructura_de_proyecto_final.docx`](../00-fuentes-oficiales/plantillas-proyecto/Plantilla_Estructura_de_proyecto_final.docx). Conserva su estructura:

- portada y contenido general;
- 14 capítulos con sus 53 secciones;
- conclusiones, recomendaciones, referencias y anexos.

**Estado vigente:** F29H **auditada, cerrada e integrada**; véase [baseline académico](../ACADEMIC_BASELINE.md). Se conserva la versión 1 del informe (30/09/2026) como snapshot histórico; no se reescriben sus resultados ni su cronología al actualizar esta entrada. No hay validación institucional ni beneficios medidos. El código de alumno de la portada queda «Pendiente»: lo completa el equipo.

| Archivo | Contenido |
|---|---|
| [`F29H_Informe_Final_v1_Colegio_Andino.docx`](F29H_Informe_Final_v1_Colegio_Andino.docx) · [PDF](F29H_Informe_Final_v1_Colegio_Andino.pdf) | Informe con cuatro figuras de PowerDesigner y los anexos A a C (BPMN AS-IS, BPMN TO-BE y casos de uso) en páginas horizontales |
| [`F29H_Informe_Final_v1_Colegio_Andino.md`](F29H_Informe_Final_v1_Colegio_Andino.md) | Espejo en Markdown, con el mismo texto y las mismas tablas |
| [`F29H_REGISTRO.md`](F29H_REGISTRO.md) | Fuentes (con SHA-256), decisiones y comandos |

## Qué integra

- **Formatos académicos:** F2 a F11 (con la F11-R), el alcance F9 y las variables de la F29C.
- **Pruebas:** el Plan de Pruebas (F29D), los casos (F29E), la QA final (F29F) y los defectos y métricas (F29G).
- **Técnica:** Git, Docker, CI y los modelos de PowerDesigner.
- **Origen del contenido:** las tablas se generan desde los modelos académicos y la evidencia.
- **Texto guía:** se eliminaron todos los textos en rojo de la plantilla.

## Límites que el informe mantiene

- La decisión final de selección es humana (RF-23).
- RF-29 es EXPERIMENTAL: no evalúa, ordena ni selecciona personas.
- No se afirma SLA, disponibilidad, rendimiento ni escalabilidad verificados.
- La cobertura de código no se midió.
- Las fases F30 y posteriores aparecen solo como trabajo futuro.

```
python docs/academico/tools/f27b/build.py f29h
powershell -ExecutionPolicy Bypass -File docs/academico/tools/f27b/topdf_toc.ps1 docs/academico/informe-final/F29H_Informe_Final_v1_Colegio_Andino.docx
```
