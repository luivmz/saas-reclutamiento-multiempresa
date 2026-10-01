"""F30 — Verificación de las fuentes candidatas (fuentes.py).

- DOI: metadatos en Crossref; si Crossref no lo tiene (p. ej. arXiv o SSRN), en DataCite. Se registran título, año,
  autores, contenedor, tipo y editorial, y si Crossref informa una retractación, corrección o retirada (`updated-by`)
  o el título la anuncia.
- URL: respuesta HTTP (con redirecciones).
- Resumen: se descarga de OpenAlex a una carpeta temporal (argumento --abstracts DIR) solo para la lectura del equipo;
  no se versiona por derechos de autor.

Salida versionada: docs/academico/investigacion-ia/datos/verificacion_fuentes.json
Uso: python docs/academico/tools/f30/verificar.py [--abstracts DIR]
"""
import datetime
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fuentes import CELEX_OFICIAL, CLAVE_URL, ELI_202, FUENTES  # noqa: E402

OUT = os.path.abspath(os.path.join(HERE, '..', '..', 'investigacion-ia', 'datos', 'verificacion_fuentes.json'))
UA = {'User-Agent': 'f30-academic-research/0.1'}


def get_json(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def crossref(doi):
    m = get_json('https://api.crossref.org/works/' + urllib.parse.quote(doi, safe='/'))['message']
    autores = [f"{a.get('family', '')}, {a.get('given', '')}".strip(', ') if 'family' in a else a.get('name', '')
               for a in m.get('author', [])]
    issued = (m.get('issued') or {}).get('date-parts', [[None]])[0][0]
    avisos = [u.get('type') for u in m.get('updated-by', [])]
    titulo = (m.get('title') or [''])[0]
    if any(w in titulo.upper() for w in ('RETRACTED', 'WITHDRAWN')):
        avisos.append('título: ' + titulo[:40])
    return dict(registro='Crossref', titulo=titulo, anio=issued, autores=autores,
                contenedor=(m.get('container-title') or [''])[0], tipo=m.get('type'), editorial=m.get('publisher'),
                avisos=avisos)


def datacite(doi):
    a = get_json('https://api.datacite.org/dois/' + urllib.parse.quote(doi.lower(), safe='/'))['data']['attributes']
    autores = [c.get('name', '') for c in a.get('creators', [])]
    return dict(registro='DataCite', titulo=(a.get('titles') or [{}])[0].get('title', ''),
                anio=a.get('publicationYear'), autores=autores, contenedor=a.get('publisher'),
                tipo=(a.get('types') or {}).get('resourceTypeGeneral'), editorial=a.get('publisher'), avisos=[])


def url_ok(url):
    """(código HTTP, URL final, título de la página o primeros caracteres del contenido)."""
    import re
    last = (0, url, '')
    # Algunos sitios bloquean uno u otro agente de forma intermitente (p. ej. iso.org con 403): se reintenta con espera.
    for agent in ('f30-academic-research/0.1', 'Mozilla/5.0 f30-academic-research', 'f30-academic-research/0.1',
                  'Mozilla/5.0 f30-academic-research'):
        time.sleep(2 if last[0] in (403, 429) else 0)
        req = urllib.request.Request(url, headers={'User-Agent': agent, 'Accept': 'text/html,*/*'})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                body = r.read(600000).decode('utf-8', 'replace')
                t = re.search(r'<title[^>]*>(.*?)</title>', body, re.S)
                last = (r.status, r.geturl(), (t.group(1) if t else body[:2000]).strip().replace('\n', ' '))
                if r.status == 200:
                    return last
        except urllib.error.HTTPError as e:
            last = (e.code, url, '')
    return last


def cellar(celex):
    """Texto oficial del Diario Oficial (XHTML) desde la Oficina de Publicaciones de la UE: primeros caracteres."""
    import re
    req = urllib.request.Request('https://publications.europa.eu/resource/celex/' + celex,
                                 headers={**UA, 'Accept': 'application/xhtml+xml', 'Accept-Language': 'eng'})
    with urllib.request.urlopen(req, timeout=120) as r:
        body = r.read(400000).decode('utf-8', 'replace')
        return r.geturl(), re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', body))[:600]


def abstract(doi):
    try:
        w = get_json('https://api.openalex.org/works/doi:' + urllib.parse.quote(doi, safe='/') +
                     '?select=abstract_inverted_index,cited_by_count')
    except Exception:
        return None, None
    inv = w.get('abstract_inverted_index')
    if not inv:
        return None, w.get('cited_by_count')
    pos = sorted((p, word) for word, ps in inv.items() for p in ps)
    return ' '.join(word for _, word in pos), w.get('cited_by_count')


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    abs_dir = sys.argv[sys.argv.index('--abstracts') + 1] if '--abstracts' in sys.argv else None
    res = dict(fecha=datetime.date.today().isoformat(), fuentes={})
    for fid, doi, url, tema, origen in FUENTES:
        r = dict(doi=doi, url=url, tema=tema, origen=origen)
        try:
            if doi:
                try:
                    r.update(crossref(doi))
                except urllib.error.HTTPError as e:
                    if e.code != 404:
                        raise
                    r.update(datacite(doi))
                r['verificado'] = True
                if abs_dir:
                    text, cites = abstract(doi)
                    r['citas_openalex'] = cites
                    if text:
                        os.makedirs(abs_dir, exist_ok=True)
                        with open(os.path.join(abs_dir, fid + '.txt'), 'w', encoding='utf-8') as f:
                            f.write(text)
            else:
                status, final, titulo = url_ok(url)
                clave = CLAVE_URL.get(fid)
                if fid in ELI_202 and status == 202:
                    url_texto, texto = cellar(CELEX_OFICIAL[fid])
                    r.update(registro='HTTP', http=status, url_final=final, texto_oficial=url_texto,
                             titulo_pagina=texto[:300], clave_esperada=clave,
                             verificado=bool(clave) and clave in texto,
                             nota='EUR-Lex responde 202 a clientes automáticos; se verificó el texto oficial del Diario '
                                  'Oficial en la Oficina de Publicaciones de la UE (CELEX ' + CELEX_OFICIAL[fid] + ')')
                else:
                    ok = status == 200 and bool(clave) and clave.lower() in titulo.lower()
                    r.update(registro='HTTP', http=status, url_final=final, titulo_pagina=titulo[:160],
                             clave_esperada=clave, verificado=ok)
        except Exception as e:  # noqa: BLE001 — se registra como no verificada
            r.update(verificado=False, error=f'{type(e).__name__}: {e}'[:200])
        res['fuentes'][fid] = r
        print(fid, r.get('verificado'), str(r.get('titulo') or r.get('http') or r.get('error') or '')[:70],
              r.get('anio', ''), r.get('avisos') or '')
        time.sleep(0.6)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
        f.write('\n')


if __name__ == '__main__':
    main()
