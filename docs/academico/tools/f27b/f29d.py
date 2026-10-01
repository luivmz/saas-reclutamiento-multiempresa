"""F29D — Plan de Pruebas de Software: DOCX (paquete generado con docxpkg), espejo Markdown y registro de generación.

La plantilla del curso existe solo en PDF, así que el DOCX se genera desde cero: títulos y orden de la plantilla,
cabecera que replica la suya («Área Informática» y el docente, con la barra azul) y pie «Página N». La tabla de
contenido es un campo de Word que se actualiza al exportar el PDF (topdf_toc.ps1).
"""
import hashlib
import os

import docxpkg as D
import m_common as C
import m_plan as M

STEM = 'F29D_Plan_de_Pruebas_Colegio_Andino'

FUENTES = [
    ('docs/academico/00-fuentes-oficiales/plan-pruebas/Plantilla_de_Plan_de_Pruebas_de_Software.pdf',
     'Plantilla del curso (estructura y títulos; prevalece)'),
    ('docs/academico/00-fuentes-oficiales/plan-pruebas/PMOInformatica_Plantilla_de_Plan_de_Pruebas_de_Software.doc',
     'Referencia externa PMO (misma estructura; no normativa)'),
    ('docs/academico/00-fuentes-oficiales/material-referencia/Ejemplo_Plan_de_Pruebas_de_Software.pdf',
     'Ejemplo externo (no normativo; no se copia contenido)'),
    ('docs/academico/tools/f27b/m_plan.py', 'Contenido del plan'),
    ('docs/academico/tools/f27b/f29d.py', 'Generador del DOCX, del espejo y de este registro'),
    ('docs/academico/tools/f27b/docxpkg.py', 'Paquete Word generado desde cero'),
]


def bloques():
    head = [('p', '**Tabla de contenido**'), ('toc',), ('pagebreak',),
            ('note', 'Estado del documento: versión ' + M.VERSION + ' del ' + M.FECHA + ', elaborada por el equipo con '
                     'asistencia de IA. No está aprobada ni firmada; la aprobación académica está pendiente y no hay '
                     'validación institucional del Colegio Andino de Huancayo.')]
    return head + M.contenido()


def build(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    B = bloques()
    D.write_docx(os.path.join(out_dir, STEM + '.docx'), B, M.TITULO + ' — ' + C.PROYECTO, C.EQUIPO,
                 cover=(M.TITULO, C.PROYECTO, 'Fecha: ' + M.FECHA))
    md = D.to_md([b for b in B if b[0] not in ('toc', 'pagebreak') and b != ('p', '**Tabla de contenido**')],
                 M.TITULO + ' — ' + C.PROYECTO,
                 preface=['> Espejo en Markdown de [`' + STEM + '.docx`](' + STEM + '.docx) (y su [PDF](' + STEM + '.pdf)). '
                          'Se genera con `python docs/academico/tools/f27b/build.py f29d`; no se edita a mano.', '',
                          f'**Proyecto:** {C.PROYECTO} · **Fecha:** {M.FECHA} · **Versión:** {M.VERSION}', ''])
    with open(os.path.join(out_dir, STEM + '.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(md)


def sha256(path):
    with open(path, 'rb') as f:
        data = f.read()
    if path.endswith(('.md', '.py')):
        data = data.replace(b'\r\n', b'\n')
    return hashlib.sha256(data).hexdigest()


def build_registro(path, root):
    L = ['# F29D — Registro de generación del Plan de Pruebas', '',
         '> Generado por `f29d.py`. Documenta cómo se construyó el plan, con qué fuentes y qué decisiones se tomaron.', '',
         '## Fuentes', '',
         '| Archivo | Uso | SHA-256 |', '|---|---|---|']
    for rel, uso in FUENTES:
        L.append(f'| `{rel}` | {uso} | `{sha256(os.path.join(root, rel))}` |')
    L += ['', '## Decisiones', '',
          '1. **Plantilla que prevalece.** La del curso: estructura, orden y títulos de sus apartados (29 títulos, del '
          'historial de versiones al glosario). La referencia PMO tiene la misma estructura, y el ejemplo externo no se '
          'usa como norma.',
          '2. **Paquete Word generado.** La plantilla del curso solo existe en PDF, así que el DOCX se genera desde cero '
          'con `docxpkg.py`:',
          '   - la portada y la cabecera replican la plantilla: «Área Informática», «Mg. Maglioni Arana Caparachin» y '
          'la barra azul;',
          '   - el pie dice «Página N»;',
          '   - los títulos usan los estilos de encabezado de Word.',
          '3. **Textos guía.** Los textos en rojo de la plantilla no se copian: cada apartado se responde con datos del '
          'repositorio.',
          '4. **Aprobaciones.** No se firma ni se simula ninguna aprobación: la tabla indica quién debe aprobar y queda '
          '«Pendiente — sin firma».',
          '5. **Tabla de contenido.** Es un campo de Word. `topdf_toc.ps1` lo actualiza al exportar el PDF sin guardar el '
          'DOCX, que conserva el campo con `updateFields`.',
          '6. **Reproducibilidad.** El DOCX tiene fecha de ZIP fija: regenerarlo da los mismos bytes. El PDF depende de '
          'Microsoft Word y no se compara byte a byte.',
          '', '## Comandos', '', '```',
          'python docs/academico/tools/f27b/build.py f29d',
          'powershell -ExecutionPolicy Bypass -File docs/academico/tools/f27b/topdf_toc.ps1 docs/academico/plan-pruebas/' + STEM + '.docx',
          'python docs/academico/tools/f27b/validate.py', '```']
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(L) + '\n')
