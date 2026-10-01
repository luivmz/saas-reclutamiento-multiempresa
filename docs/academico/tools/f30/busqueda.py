"""F30 — Búsqueda bibliográfica sistemática (reproducible) en OpenAlex.

Una consulta por cada tema A–T del encargo. Para cada una se registra la fecha, la consulta exacta, el total de
resultados que informa OpenAlex y los 25 primeros por relevancia (identificador, DOI, título, año, tipo, fuente y
citas), que son el conjunto cribado. El resultado se guarda en docs/academico/investigacion-ia/datos/busqueda_openalex.json.

Uso: python docs/academico/tools/f30/busqueda.py
No envía datos del proyecto ni del usuario: solo las consultas.
"""
import datetime
import json
import os
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, '..', '..', 'investigacion-ia', 'datos', 'busqueda_openalex.json'))
FIELDS = 'id,doi,title,publication_year,type,cited_by_count,primary_location'

TEMAS = [
    ('A', 'AI in recruitment / algorithmic hiring', 'algorithmic hiring artificial intelligence recruitment'),
    ('B', 'Candidate-job fit', 'person-job fit candidate job matching'),
    ('C', 'Competency-based assessment', 'competency modeling personnel selection'),
    ('D', 'Structured interviews', 'structured employment interview validity'),
    ('E', 'CV / resume NLP', 'resume parsing natural language processing'),
    ('F', 'Semantic matching', 'semantic matching job postings resumes embeddings'),
    ('G', 'Information extraction', 'skill extraction job postings information extraction'),
    ('H', 'Ranking / recommendation', 'job recommender system e-recruitment survey'),
    ('I', 'Multicriteria decision support', 'multi-criteria decision making personnel selection'),
    ('J', 'Explainable AI', 'explainable artificial intelligence interpretability survey'),
    ('K', 'Fairness / algorithmic bias', 'algorithmic fairness bias machine learning survey'),
    ('L', 'Responsible AI', 'responsible artificial intelligence governance accountability'),
    ('M', 'Human-in-the-loop', 'human-AI decision making automation bias reliance'),
    ('N', 'Uncertainty / calibration', 'probability calibration classifiers uncertainty'),
    ('O', 'Model monitoring / drift', 'concept drift dataset shift monitoring machine learning'),
    ('P', 'Auditability', 'algorithmic auditing accountability machine learning'),
    ('Q', 'Recruitment analytics', 'human resource analytics people analytics'),
    ('R', 'Document understanding', 'document understanding layout analysis PDF parsing'),
    ('S', 'Speech-to-text for interviews', 'automatic speech recognition robust weak supervision'),
    ('T', 'Interview transcript evaluation', 'automated interview assessment transcripts language'),
]


def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'f30-academic-research/0.1'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def main():
    salida = dict(fuente='OpenAlex (https://api.openalex.org)', fecha=datetime.date.today().isoformat(),
                  criterio='orden por relevancia; 25 primeros resultados de cada consulta como conjunto cribado',
                  temas=[])
    for code, tema, q in TEMAS:
        url = (f'https://api.openalex.org/works?search={urllib.parse.quote(q)}&per-page=25&select={FIELDS}')
        d = get(url)
        res = []
        for w in d['results']:
            loc = (w.get('primary_location') or {}).get('source') or {}
            res.append(dict(openalex=w['id'].rsplit('/', 1)[-1], doi=(w.get('doi') or '').replace('https://doi.org/', ''),
                            titulo=w.get('title'), anio=w.get('publication_year'), tipo=w.get('type'),
                            fuente=loc.get('display_name'), citas=w.get('cited_by_count')))
        salida['temas'].append(dict(codigo=code, tema=tema, consulta=q, total=d['meta']['count'], cribados=res))
        print(code, d['meta']['count'], len(res))
        time.sleep(0.3)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(salida, f, ensure_ascii=False, indent=1)
        f.write('\n')


if __name__ == '__main__':
    main()
