"""F30 — Datos verificables de herramientas, paquetes y servidores MCP candidatos (sin instalar nada).

Para cada herramienta: repositorio en GitHub (existencia, licencia, archivado, última actividad, estrellas, issues
abiertos, propietario), paquete en PyPI (última versión, fecha, licencia declarada, número de dependencias) y avisos de
seguridad en OSV (total histórico y los que afectan a la última versión publicada).
Salida: docs/academico/investigacion-ia/datos/herramientas.json
Uso: python docs/academico/tools/f30/herramientas.py [--completar]
  --completar: conserva el JSON existente y solo vuelve a consultar las herramientas sin datos de GitHub (la API sin
  autenticación admite 60 consultas por hora) o que falten en él. Cada herramienta registra su fecha de consulta.
"""
import datetime
import json
import os
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, '..', '..', 'investigacion-ia', 'datos', 'herramientas.json'))
UA = {'User-Agent': 'f30-academic-research/0.1'}

# (nombre, categoría, repositorio GitHub, ecosistema OSV, paquete)
HERRAMIENTAS = [
    ('scikit-learn', 'ML', 'scikit-learn/scikit-learn', 'PyPI', 'scikit-learn'),
    ('XGBoost', 'ML', 'dmlc/xgboost', 'PyPI', 'xgboost'),
    ('LightGBM', 'ML', 'microsoft/LightGBM', 'PyPI', 'lightgbm'),
    ('CatBoost', 'ML', 'catboost/catboost', 'PyPI', 'catboost'),
    ('InterpretML (EBM)', 'Explicabilidad', 'interpretml/interpret', 'PyPI', 'interpret'),
    ('SHAP', 'Explicabilidad', 'shap/shap', 'PyPI', 'shap'),
    ('LIME', 'Explicabilidad', 'marcotcr/lime', 'PyPI', 'lime'),
    ('Fairlearn', 'Equidad', 'fairlearn/fairlearn', 'PyPI', 'fairlearn'),
    ('AIF360', 'Equidad', 'Trusted-AI/AIF360', 'PyPI', 'aif360'),
    ('MLflow', 'Seguimiento de experimentos / registro de modelos', 'mlflow/mlflow', 'PyPI', 'mlflow'),
    ('DVC', 'Versionado de datos', 'iterative/dvc', 'PyPI', 'dvc'),
    ('Evidently', 'Monitoreo / deriva', 'evidentlyai/evidently', 'PyPI', 'evidently'),
    ('Pandera', 'Validación de datos', 'unionai-oss/pandera', 'PyPI', 'pandera'),
    ('Great Expectations', 'Validación de datos', 'great-expectations/great_expectations', 'PyPI', 'great-expectations'),
    ('spaCy', 'NLP', 'explosion/spaCy', 'PyPI', 'spacy'),
    ('sentence-transformers', 'Embeddings', 'UKPLab/sentence-transformers', 'PyPI', 'sentence-transformers'),
    ('Hugging Face Transformers', 'NLP / modelos', 'huggingface/transformers', 'PyPI', 'transformers'),
    ('Microsoft Presidio', 'Anonimización de PII', 'microsoft/presidio', 'PyPI', 'presidio-analyzer'),
    ('pgvector', 'Búsqueda vectorial', 'pgvector/pgvector', None, None),
    ('FAISS', 'Búsqueda vectorial', 'facebookresearch/faiss', 'PyPI', 'faiss-cpu'),
    ('Qdrant', 'Búsqueda vectorial', 'qdrant/qdrant', 'PyPI', 'qdrant-client'),
    ('Whisper (OpenAI)', 'Voz a texto', 'openai/whisper', 'PyPI', 'openai-whisper'),
    ('faster-whisper', 'Voz a texto', 'SYSTRAN/faster-whisper', 'PyPI', 'faster-whisper'),
    ('whisper.cpp', 'Voz a texto', 'ggml-org/whisper.cpp', None, None),
    ('Vosk', 'Voz a texto', 'alphacep/vosk-api', 'PyPI', 'vosk'),
    ('pyannote.audio', 'Diarización de hablantes', 'pyannote/pyannote-audio', 'PyPI', 'pyannote.audio'),
    ('FFmpeg', 'Audio / video', 'FFmpeg/FFmpeg', None, None),
    ('Apache Tika', 'Análisis de documentos', 'apache/tika', 'Maven', 'org.apache.tika:tika-core'),
    ('PyMuPDF', 'PDF', 'pymupdf/PyMuPDF', 'PyPI', 'pymupdf'),
    ('pypdf', 'PDF', 'py-pdf/pypdf', 'PyPI', 'pypdf'),
    ('pdfplumber', 'PDF', 'jsvine/pdfplumber', 'PyPI', 'pdfplumber'),
    ('Docling', 'Análisis de documentos', 'docling-project/docling', 'PyPI', 'docling'),
    ('Unstructured', 'Análisis de documentos', 'Unstructured-IO/unstructured', 'PyPI', 'unstructured'),
    ('python-docx', 'Documentos Word', 'python-openxml/python-docx', 'PyPI', 'python-docx'),
    ('Tesseract OCR', 'OCR', 'tesseract-ocr/tesseract', None, None),
    ('JupyterLab', 'Notebooks', 'jupyterlab/jupyterlab', 'PyPI', 'jupyterlab'),
    ('nbstripout', 'Notebooks / reproducibilidad', 'kynan/nbstripout', 'PyPI', 'nbstripout'),
    ('pip-audit', 'Seguridad de dependencias', 'pypa/pip-audit', 'PyPI', 'pip-audit'),
    ('OSV-Scanner', 'Seguridad de dependencias', 'google/osv-scanner', None, None),
    ('Mermaid', 'Diagramas', 'mermaid-js/mermaid', 'npm', 'mermaid'),
    ('Ollama', 'LLM local', 'ollama/ollama', None, None),
    ('Zotero', 'Gestión bibliográfica', 'zotero/zotero', None, None),
    ('Better BibTeX for Zotero', 'Gestión bibliográfica', 'retorquere/zotero-better-bibtex', None, None),
    # Servidores MCP candidatos (externos; solo se evalúan)
    ('MCP Reference Servers (fetch, filesystem, git)', 'MCP', 'modelcontextprotocol/servers', None, None),
    ('GitHub MCP Server', 'MCP', 'github/github-mcp-server', None, None),
    ('Hugging Face MCP Server', 'MCP', 'huggingface/hf-mcp-server', None, None),
    ('arXiv MCP Server', 'MCP', 'blazickjp/arxiv-mcp-server', 'PyPI', 'arxiv-mcp-server'),
    ('Zotero MCP', 'MCP', '54yyyu/zotero-mcp', 'PyPI', 'zotero-mcp'),
    ('Context7 MCP', 'MCP', 'upstash/context7', 'npm', '@upstash/context7-mcp'),
]


def get(url, data=None):
    headers = dict(UA)
    if data is not None:
        headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def github(repo):
    try:
        d = get('https://api.github.com/repos/' + repo)
    except urllib.error.HTTPError as e:
        return dict(existe=False, http=e.code)
    return dict(existe=True, nombre=d['full_name'], propietario_tipo=d['owner']['type'],
                licencia=(d.get('license') or {}).get('spdx_id'), archivado=d['archived'],
                ultima_actividad=d['pushed_at'][:10], creado=d['created_at'][:10], estrellas=d['stargazers_count'],
                issues_abiertos=d['open_issues_count'], redirigido=d['full_name'].lower() != repo.lower())


def pypi(pkg):
    try:
        d = get(f'https://pypi.org/pypi/{pkg}/json')
    except urllib.error.HTTPError as e:
        return dict(existe=False, http=e.code)
    info = d['info']
    files = d['releases'].get(info['version'], [])
    fecha = max((f['upload_time'][:10] for f in files), default=None)
    lic = info.get('license_expression') or info.get('license') or ''
    return dict(existe=True, version=info['version'], fecha=fecha, licencia=lic[:60],
                dependencias=len(info.get('requires_dist') or []))


def npm(pkg):
    try:
        d = get('https://registry.npmjs.org/' + pkg.replace('/', '%2F'))
    except urllib.error.HTTPError as e:
        return dict(existe=False, http=e.code)
    v = d['dist-tags']['latest']
    return dict(existe=True, version=v, fecha=d['time'].get(v, '')[:10], licencia=str(d.get('license') or '')[:60],
                dependencias=len(d['versions'][v].get('dependencies') or {}))


def osv(eco, pkg, version=None):
    q = {'package': {'name': pkg, 'ecosystem': eco}}
    if version:
        q['version'] = version
    d = get('https://api.osv.dev/v1/query', json.dumps(q).encode())
    vulns = [v for v in d.get('vulns', []) if not v.get('withdrawn')]
    return sorted({v['id'] for v in vulns})


def main():
    import sys
    previas = {}
    if '--completar' in sys.argv and os.path.exists(OUT):
        with open(OUT, encoding='utf-8') as f:
            prev = json.load(f)
        previas = {h['nombre']: h for h in prev['herramientas'] if h['github'].get('existe')}
        for h in previas.values():
            h.setdefault('consultado', prev['fecha'])
    res = dict(fecha=datetime.date.today().isoformat(), fuentes=['api.github.com', 'pypi.org', 'registry.npmjs.org',
                                                                'api.osv.dev'], herramientas=[])
    for nombre, cat, repo, eco, pkg in HERRAMIENTAS:
        if nombre in previas:
            res['herramientas'].append(previas[nombre])
            continue
        r = dict(nombre=nombre, categoria=cat, repo=repo, ecosistema=eco, paquete=pkg,
                 consultado=datetime.date.today().isoformat(), github=github(repo))
        if eco == 'PyPI':
            r['registro'] = pypi(pkg)
        elif eco == 'npm':
            r['registro'] = npm(pkg)
        if eco and pkg:
            try:
                r['osv_historico'] = osv(eco, pkg)
                ver = (r.get('registro') or {}).get('version')
                r['osv_ultima_version'] = osv(eco, pkg, ver) if ver else None
            except Exception as e:  # noqa: BLE001
                r['osv_error'] = str(e)[:120]
        res['herramientas'].append(r)
        g = r['github']
        print(nombre, g.get('existe'), g.get('licencia'), g.get('ultima_actividad'), g.get('estrellas'),
              (r.get('registro') or {}).get('version'), len(r.get('osv_historico') or []),
              len(r.get('osv_ultima_version') or []) if r.get('osv_ultima_version') is not None else '-')
        time.sleep(0.4)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
        f.write('\n')


if __name__ == '__main__':
    main()
