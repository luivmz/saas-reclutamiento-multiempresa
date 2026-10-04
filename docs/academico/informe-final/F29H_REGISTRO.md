# F29H — Registro de generación del Informe Final v1

> Generado por `f29h.py`. Documenta las fuentes, las decisiones y los comandos del informe final.

## Fuentes

| Archivo | Uso | SHA-256 |
|---|---|---|
| `docs/academico/00-fuentes-oficiales/plantillas-proyecto/Plantilla_Estructura_de_proyecto_final.docx` | Plantilla oficial del informe final (estructura, portada, estilos y tabla de contenido) | `b26cfb21ca627c46d65f8f683422ffca1e022ec60c75132f0d7843b01a03fcda` |
| `docs/academico/tools/f27b/m_informe.py` | Contenido de cada sección | `b81fff2e0d6c065d215cf3ad5aef638af0198d3ff46f2b17389c53b6e4866b7e` |
| `docs/academico/tools/f27b/f29h.py` | Relleno de la plantilla, anexos horizontales y espejo Markdown | `e6b60dcf186bbad5f38d65e140483f761431fbadc359c9cfa767c2bae3956a54` |
| `docs/academico/powerdesigner/exports/ARQ-01_Arquitectura_Conceptual.png` | Figura 1 (F29) | `eb4065a2b703413730d13bab1b1567e3cd3b872eba7bee02454d25265bde2e5d` |
| `docs/v1.1/powerdesigner/exports/CL-01-clases-del-dominio.png` | Figura 2 (F23) | `8150e75d13dcee72aa6b518d3cb6b1165a9862345a9ba374ee168312e8600455` |
| `docs/v1.1/powerdesigner/exports/PDM-01-esquema-completo.png` | Figura 3 (F23) | `ef9da4f84e68560d995b9e56e66dca50c0ec9bcca1c1a81fd9f176bbb4ae24e3` |
| `docs/v1.1/powerdesigner/exports/DE-01-despliegue.png` | Figura 4 (F23) | `c96f71d083f3e132f6c092e329b0d77ff4794f0a5183b89a84a1cf02bca69206` |
| `docs/academico/powerdesigner/exports/F3_BPMN_ASIS.png` | Anexo A (F29) | `685a9380cf24b0b21d93e6efdcee67b60fd5ca8f52d3746c8930fbd1b3de2df5` |
| `docs/academico/powerdesigner/exports/F5_BPMN_TOBE.png` | Anexo B (F29) | `b3af8824cc3ad92e814e2d62d79ce584450699ad5f5a0cfec7f52f4036447d67` |
| `docs/academico/powerdesigner/exports/F8_Casos_de_Uso_Academicos.png` | Anexo C (F29) | `94dee7b176dbd529385392b82e60b81c5cc3b1ebfad829da7481b7f931f05aa3` |

## Decisiones

1. **Estructura oficial.** Se conservan la portada, la tabla de contenido, los 14 capítulos con sus 53 secciones y los apartados finales (conclusiones, recomendaciones, referencias y anexos) de la plantilla.
2. **Texto guía.** Se eliminan todos los párrafos en rojo de la plantilla, incluida la «Aclaración importante». Los títulos del capítulo 8, que la plantilla trae en rojo, se conservan sin ese color.
3. **Contenido.** Sale de `m_informe.py`:
   - las tablas se generan desde los modelos académicos (F2 a F11, F29C) y desde la evidencia de la F29D a la F29G;
   - los estados (HECHO VERIFICADO, AS-IS PRELIMINAR, TO-BE PROPUESTO, SOFTWARE IMPLEMENTADO y EXPERIMENTAL) se declaran;
   - no se afirma validación institucional, beneficios medidos, SLA, disponibilidad, rendimiento ni escalabilidad verificados;
   - las fases F30 y posteriores solo aparecen como trabajo futuro.
4. **Portada.** Lleva el título del proyecto y los tres integrantes. El código de alumno no está en el repositorio y queda «Pendiente»: lo completa el equipo.
5. **Figuras.** Son exportaciones formales de PowerDesigner, incrustadas sin modificar. Los diagramas anchos (anexos A a C) van en páginas horizontales.
6. **Tabla de contenido y reproducibilidad.** El campo de la tabla de contenido se actualiza al exportar el PDF (`topdf_toc.ps1`). El DOCX tiene fecha de ZIP fija y es reproducible; el PDF depende de Word.

## Comandos

```
python docs/academico/tools/f27b/build.py f29h
powershell -ExecutionPolicy Bypass -File docs/academico/tools/f27b/topdf_toc.ps1 docs/academico/informe-final/F29H_Informe_Final_v1_Colegio_Andino.docx
```
