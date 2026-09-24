"""Structural and content validation of the final Formato 09 DOCX (+ its PDF text)."""
import re, sys, zipfile, xml.dom.minidom
docx, pdftxt = sys.argv[1], sys.argv[2]
z = zipfile.ZipFile(docx)
assert z.testzip() is None
fails = []
def check(cond, msg):
    print(('OK   ' if cond else 'FAIL ') + msg)
    if not cond: fails.append(msg)
for n in z.namelist():
    if n.endswith(('.xml', '.rels')):
        xml.dom.minidom.parseString(z.read(n))
check(True, f'{len(z.namelist())} partes; todas las XML bien formadas')
doc = z.read('word/document.xml').decode('utf8')
text = ''.join(re.findall(r'<w:t(?:\s[^>]*)?>([^<]*)</w:t>', doc))
alltext = ' '.join(''.join(re.findall(r'<w:t(?:\s[^>]*)?>([^<]*)</w:t>', z.read(n).decode('utf8', 'ignore')))
                   for n in z.namelist() if n.endswith('.xml')) + z.read('docProps/core.xml').decode('utf8')
pdf = open(pdftxt, encoding='utf8').read()
pages = pdf.count('=====PAGE ')
check(20 <= pages <= 40, f'páginas renderizadas por Word: {pages}')
# images embedded and referenced
rels = z.read('word/_rels/document.xml.rels').decode()
emb = re.findall(r'r:embed="(rId\d+)"', doc)
for rid in emb:
    tgt = re.search(rf'Id="{rid}"[^>]*Target="([^"]+)"', rels) or re.search(rf'Target="([^"]+)"[^>]*Id="{rid}"', rels)
    check(tgt is not None and ('word/' + tgt.group(1)) in z.namelist(), f'imagen {rid} -> {tgt.group(1) if tgt else "?"} embebida')
check(len(emb) == 7, f'imágenes en el cuerpo: {len(emb)} (portada + anexos A-F)')
# headers/footers
sect = doc[doc.rindex('<w:sectPr'):]
check(sect.count('headerReference') == 2 and sect.count('footerReference') == 2 and '<w:titlePg/>' in sect,
      'encabezados y pies (default + primera página) conservados')
check('PAGE' in z.read('word/footer1.xml').decode(), 'numeración de página en el pie')
# tables not corrupt: each tr has as many tc as gridCol
for i, tbl in enumerate(re.findall(r'<w:tbl>.*?</w:tbl>', doc, re.S)):
    cols = tbl.count('<w:gridCol ')
    rows = re.findall(r'<w:tr>.*?</w:tr>', tbl, re.S)
    bad = [r for r in rows if r.count('<w:tc>') != cols]
    if bad: check(False, f'tabla {i}: filas con celdas != {cols}')
check(True, f'tablas: {len(re.findall(r"<w:tbl>", doc))}, filas coherentes con su rejilla')
# official sections present
for s in ['1.2 Información del proyecto', '3.2 Problemas oficiales', '3.4 Usuarios principales', '3.5 Entorno de uso',
          '4.1 Objetivo general', '4.2 Objetivos específicos', '5. Alcance incluido', '6. Alcance excluido',
          '7.1 Actores externos', '7.4 Entradas del sistema', '7.5 Salidas del sistema', '10.1 Tecnológicas',
          '10.2 Operativas', '10.3 Privacidad, seguridad y legales', '11.1 Supuestos principales',
          '12. Criterios de aceptación del alcance', '12.1 Correspondencia con los criterios del Formato 09']:
    check(s in text, f'sección oficial presente: {s}')
for f in ['Módulo / Sistema', 'Nombre del proyecto', 'Integrantes del equipo', 'Docente', 'Destino']:
    check(f in text, f'campo oficial: {f}')
# NRC and names
check('30180' not in alltext, 'sin «30180» en ninguna parte del DOCX (incluye propiedades)')
check(text.count('28607') >= 3, f'NRC 28607 presente ({text.count("28607")} veces)')
for n in ['Coronacion Meza Fredy', 'Peña Arroyo Anthony', 'Vila Meza Luis Antonio', 'Maglioni Arana Caparachin',
          'Colegio Andino de Huancayo', 'Pruebas y Calidad de Software']:
    check(n.lower() in text.lower(), f'nombre correcto: {n}')
# obsolete ML state and placeholders
bad_phrases = ['Laravel todavía no', 'FastAPI no es consumido', 'GAP-01 permanece abierto', 'GAP-01 sigue abierto',
               'no existe cliente HTTP', 'eventual integración', 'ausencia de integración con Laravel',
               'mientras GAP-01', 'F23 pendiente', 'F23 no iniciada', 'Fase 15C del servicio',
               'Lorem', '[pendiente]', '……']
for p in bad_phrases:
    check(p.lower() not in text.lower(), f'sin frase obsoleta o marcador: «{p}»')
for p in ['TODO', 'TBD', 'XXX', 'FIXME']:  # marcadores en mayúsculas; «todo» es una palabra española
    check(re.search(rf'\b{p}\b', text) is None, f'sin marcador: «{p}»')
check('GAP-01' not in text, 'GAP-01 ya no se menciona como estado vigente')
# contracts
check('9ee1843055e75d4039dd84fd666db7a594e1a45ec7e9b354820fabfcb21ebcd2' in text, 'freeze fingerprint exacto')
check('0.1679418172266036' in text, 'threshold exacto')
for f in ['risk_score', 'risk_flag', 'threshold', 'model_version', 'freeze_fingerprint', 'status']:
    check(f in text, f'campo de respuesta: {f}')
check('incertidumbre' in text, 'aclara que no hay campo de incertidumbre')
check(all(f'RF-{i:02d}' in text for i in range(1, 28)), 'RF-01 a RF-27 presentes')
rf_rows = re.findall(r'RF-(\d\d)', text)
check(max(int(x) for x in rf_rows) == 31, 'numeración RF máxima citada: RF-31 (candidato), sin renumeración')
check('RF-28 (candidato)' in text and 'RF-29 (candidato)' in text and 'RNF-C (propuesta)' in text,
      'RF-28, RF-29 y RNF-C rotulados como candidatos/propuesta')
check(all(a in text for a in ['Área solicitante', 'Recursos Humanos', 'Aprobador o Dirección', 'Postulante', 'Evaluador']),
      'cinco actores oficiales')
for forbidden in ['Administrador general', 'Entrevistador independiente']:
    check(forbidden not in text, f'sin actor no oficial: {forbidden}')
check('Superadministración comercial SaaS' in text, 'superadministración solo como exclusión (OUT-03)')
# TOC page numbers match rendered pages
toc = re.findall(r'<w:t>([^<]+)</w:t><w:tab/><w:t>(\d+)</w:t>', doc)
pg = {int(p.split('\n', 1)[0]): p.split('\n', 1)[1] for p in pdf.split('=====PAGE ')[1:]}
for title, n in toc:
    probe = 'Anexo A.' if title.startswith('Anexos') else title
    check(any(l.strip().startswith(probe) for l in pg[int(n)].splitlines()), f'TOC «{title}» -> p. {n}')
print('\nRESULTADO:', 'SIN FALLOS' if not fails else f'{len(fails)} FALLOS')
sys.exit(1 if fails else 0)
