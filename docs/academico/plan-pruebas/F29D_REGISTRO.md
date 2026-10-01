# F29D — Registro de generación del Plan de Pruebas

> Generado por `f29d.py`. Documenta cómo se construyó el plan, con qué fuentes y qué decisiones se tomaron.

## Fuentes

| Archivo | Uso | SHA-256 |
|---|---|---|
| `docs/academico/00-fuentes-oficiales/plan-pruebas/Plantilla_de_Plan_de_Pruebas_de_Software.pdf` | Plantilla del curso (estructura y títulos; prevalece) | `2dfd714e806b05908dbcd0fd3029292d82f4019dba4b839686d3f9a8e7d3856d` |
| `docs/academico/00-fuentes-oficiales/plan-pruebas/PMOInformatica_Plantilla_de_Plan_de_Pruebas_de_Software.doc` | Referencia externa PMO (misma estructura; no normativa) | `3d2bb6f87c43ea1a3484ddff88a60980e3ea8a703911d4709663fbd103686f76` |
| `docs/academico/00-fuentes-oficiales/material-referencia/Ejemplo_Plan_de_Pruebas_de_Software.pdf` | Ejemplo externo (no normativo; no se copia contenido) | `1b77a9618cddba1db9fa5158a50542eb659f1c424c3d2099237df3e70c3f5554` |
| `docs/academico/tools/f27b/m_plan.py` | Contenido del plan | `cc51a49fed08d05a670e29ee4cc4de2b2f1895775d4fd73c55cd65a32193c2d7` |
| `docs/academico/tools/f27b/f29d.py` | Generador del DOCX, del espejo y de este registro | `738a0f560b150929c6f3b6862a9fc7f5e07c6bc385e2964477135067b6d5d98f` |
| `docs/academico/tools/f27b/docxpkg.py` | Paquete Word generado desde cero | `d97b974899fe8857baca1e03d2185666cf0428f389a0e702029dd60fc499983c` |

## Decisiones

1. **Plantilla que prevalece.** La del curso: estructura, orden y títulos de sus apartados (29 títulos, del historial de versiones al glosario). La referencia PMO tiene la misma estructura, y el ejemplo externo no se usa como norma.
2. **Paquete Word generado.** La plantilla del curso solo existe en PDF, así que el DOCX se genera desde cero con `docxpkg.py`:
   - la portada y la cabecera replican la plantilla: «Área Informática», «Mg. Maglioni Arana Caparachin» y la barra azul;
   - el pie dice «Página N»;
   - los títulos usan los estilos de encabezado de Word.
3. **Textos guía.** Los textos en rojo de la plantilla no se copian: cada apartado se responde con datos del repositorio.
4. **Aprobaciones.** No se firma ni se simula ninguna aprobación: la tabla indica quién debe aprobar y queda «Pendiente — sin firma».
5. **Tabla de contenido.** Es un campo de Word. `topdf_toc.ps1` lo actualiza al exportar el PDF sin guardar el DOCX, que conserva el campo con `updateFields`.
6. **Reproducibilidad.** El DOCX tiene fecha de ZIP fija: regenerarlo da los mismos bytes. El PDF depende de Microsoft Word y no se compara byte a byte.

## Comandos

```
python docs/academico/tools/f27b/build.py f29d
powershell -ExecutionPolicy Bypass -File docs/academico/tools/f27b/topdf_toc.ps1 docs/academico/plan-pruebas/F29D_Plan_de_Pruebas_Colegio_Andino.docx
python docs/academico/tools/f27b/validate.py
```
