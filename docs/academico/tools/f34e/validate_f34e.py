"""F34E — Validación de G0-SBX, la puerta de experimentación académica sintética (solo biblioteca estándar).

Recalcula los 18 criterios SBX con comprobaciones del repositorio y exige que la matriz y la decisión coincidan:
  SBX-01..18  dataset F34 (reglas de validate_f34), contrato schema.json, árbol de archivos, matriz de trazabilidad,
              regla RANK de F34A, registros reales de F34C (validate_f34b) y Git (códigos de salida comprobados).
  MTX         matriz: 18 criterios, solo CUMPLE / NO CUMPLE (sin pendientes), igual al recálculo, resumen coherente.
  DEC         decisión: G0-SBX APROBADA CON RESTRICCIONES solo si los 18 cumplen; F35-SBX HABILITADA solo entonces;
              F35 productiva BLOQUEADA, G0 real NO APROBADA, ADR-005 PROPUESTA, alcance C BLOQUEADO, datos reales
              prohibidos; README coherente con la decisión.
  CLM         ninguna aprobación de G0 sin el sufijo SBX, autorización de datos reales, F35 productiva o F36–F40
              desbloqueadas, scoring o recomendación habilitados, alcance C habilitado ni evidencia externa inventada.
              F34E-M01: cada proposición se evalúa por separado (negación, predicado habilitante, «pero/sino/aunque»,
              elipsis y contexto de tabla «Permitido/Prohibido»); negar una categoría no neutraliza otra.
  STA         F34E-M02: cada estado crítico (G0 real, G0-SBX, F35 productiva, F35-SBX, F36–F40, alcance C) se declara
              exactamente una vez en la decisión, con un valor admitido y sin contradicciones en todo el paquete.
              La matriz exige exactamente una fila por SBX-01..18, sin duplicados, IDs desconocidos ni estados dobles.
  REAL        G0 real NO APROBADA, G0-02/03/12 sin cerrar, ADR-005 canónico PROPUESTA, aprobación interna registrada,
              F34C intacta (4 adjuntos con su SHA-256) y documentos F34D publicados intactos.
  GIT         solo cambian g0-sandbox/, tools/f34e/ y la adaptación autorizada del alcance Git de validate_f34b.py;
              base fija: cierre F34D en main; runtime sin cambios. Desde F35-SBX-A (DH-02) también
              evidencia-sbx/** (.md/.json) y tools/f35sbx/** (.py), comprobado aquí con una segunda llave, y los
              tres validadores históricos adaptados (F30, F33 y F34), como rutas exactas.
Incluye casos negativos y un control que demuestra que el validador también acepta un resultado NO APROBADA.
Uso: python docs/academico/tools/f34e/validate_f34e.py
"""
import hashlib
import importlib.util
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
ACAD = os.path.join(ROOT, 'docs', 'academico')
DOCS = os.path.join(ACAD, 'g0-sandbox')
BASE = '9e0fc92adbe563e99a7cb16fdb07aa26f8876d68'
FILES = ['README.md', 'F34E_Definicion_G0_SBX.md', 'F34E_Matriz_Criterios_G0_SBX.md', 'F34E_Alcance_Autorizado.md',
         'F34E_Prohibiciones.md', 'F34E_Relacion_G0_Real_vs_SBX.md', 'F34E_Autorizacion_F35_SBX.md',
         'F34E_Decision_G0_SBX.md']
SBX_IDS = [f'SBX-{i:02d}' for i in range(1, 19)]
SBX_STATES = {'CUMPLE', 'NO CUMPLE'}
G0SBX_STATES = {'APROBADA CON RESTRICCIONES', 'NO APROBADA', 'REVOCADA'}
# F34C: adjuntos reales registrados (no cambian en F34E).
F34C_ATTACHMENTS = {
    'G0-ADR005-ThreatModel_Anthony_Pena_2026-10-04.png': 'a280b48835f4b859a05fe3407f037f01bb9fc62cd2e41fca6cc780408deaba30',
    'G0-ADR005-ThreatModel_Fredy_Coronacion_2026-10-04.png': '9c95bf66797f3a170ba6a859624a7119c6c6de5270c4a398e965f66bb9d6bce9',
    'G0-ADR005-ThreatModel_Luis_Vila_2026-10-04.png': 'd2ed9dd568051780c51799031ee6ef78197c106d427a77a7c24a49cacb4d10e2',
    'G0-ADR005-ThreatModel_Luis_Vila_2026-10-04_original.png': 'ba464828a8180c0db9961ba493ea8e1d4702db51719e2d975c3463abda724f3d',
}
# F34D cerrada y publicada en BASE: estos cinco documentos deben permanecer intactos.
F34D_DELIVERED = {
    'docs/academico/g0-evidence/F34B_Decision_G0.md': '2f98c21178032ca25cf0e962e207bc588c1e6c82804935f1f7c98015ff588ef3',
    'docs/academico/g0-evidence/F34B_Matriz_Evidencias_G0.md': '7aa8f255a26991f82ed4d92e6d22b3278ab16f922cc7b21171f7699c06a8d2a2',
    'docs/academico/g0-evidence/F34B_Validacion_Necesidad.md': '82258284aa675348c198bfcffd12042dc483b8c126d477d088b3658f75706053',
    'docs/academico/g0-evidence/README.md': '918ea25efc7d98af56425104227272d50754c2734e4cf515460d99dacc84951e',
    'docs/academico/g0-evidence/adjuntos/README.md': '4c83d741f3a80d23ddc9260dcaf63ff27d9e266ff3c800a56e2318e1f759e1f3',
}
# Se conserva el hash del blob publicado, no el del validador adaptado en el árbol de F34E.
F34B_VALIDATOR = 'docs/academico/tools/f34b/validate_f34b.py'
F34D_VALIDATOR_SHA = '637100ed2ea580178556b812b364e6f027b22b372e09c134f121d5a162fb93a5'
ALLOWED = ('docs/academico/g0-sandbox/', 'docs/academico/tools/f34e/')
RUNTIME = ['app', 'routes', 'config', 'database', 'resources', 'tests', 'cypress', 'ml-service', 'composer.json',
           'composer.lock', 'package.json', 'package-lock.json', 'docker-compose.yml', 'Dockerfile']
BASELINE = ['docs/v1.1/scope-preliminary.md', 'docs/final-report/traceability-master.md', 'docs/rf-implementation-matrix.md',
            'docs/assumptions.md', 'docs/academico/diseno-inteligente', 'docs/academico/datos-sinteticos',
            'docs/academico/g0-readiness']
RUNTIME_SCAN = ['app', 'routes', 'config', 'database', 'resources', 'tests', 'cypress', os.path.join('ml-service', 'src')]
MEDIA_OR_DOC = re.compile(r'\.(pdf|docx?|odt|rtf|png|jpe?g|gif|bmp|tiff?|webp|heic|mp3|wav|m4a|ogg|flac|aac|mp4|mov|avi|'
                          r'mkv|webm|wmv)$', re.I)
SCORE_TOKENS = {'score', 'scoring', 'recommend', 'recommendation', 'recomendacion', 'ranking', 'rank', 'selected',
                'seleccionado', 'hire', 'hired', 'contratado', 'best', 'mejor'}


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, os.path.dirname(path))
    spec.loader.exec_module(mod)
    return mod


def sha_file(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def read_all():
    return {n: open(os.path.join(DOCS, n), encoding='utf-8').read() if os.path.isfile(os.path.join(DOCS, n)) else ''
            for n in FILES}


class GitError(Exception):
    pass


def git(*a):
    try:
        p = subprocess.run(['git', *a], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    except OSError as e:
        raise GitError(f'git no disponible: {e}')
    if p.returncode != 0:
        raise GitError(f'git {" ".join(a[:3])} → código {p.returncode}')
    return {ln.strip() for ln in p.stdout.splitlines() if ln.strip()}


# ---------------------------------------------------------------- recálculo de los criterios SBX
def compute_sbx():
    """{SBX-xx: (cumple, detalle)} calculado solo con el repositorio."""
    r = {}
    V34 = load_module('v34', os.path.join(ACAD, 'tools', 'f34', 'validate_f34.py'))
    V34A = load_module('v34a', os.path.join(ACAD, 'tools', 'f34a', 'validate_f34a.py'))
    V34B = load_module('v34b', os.path.join(ACAD, 'tools', 'f34b', 'validate_f34b.py'))
    T = V34.load()
    res = V34.run_rules(T)
    viol = lambda *ids: [x for i in ids for x in res.get(i, ['regla inexistente'])]
    import json
    manifest = json.load(open(os.path.join(ACAD, 'datos-sinteticos', 'dataset', 'manifest.json'), encoding='utf-8'))
    schema = json.load(open(os.path.join(ACAD, 'tools', 'f34', 'schema.json'), encoding='utf-8'))
    fields = {(res_['name'], f['name']) for res_ in schema['resources'] for f in res_['schema']['fields']}
    toks = lambda s: set(re.split(r'[^a-z]+', s.lower()))
    score_fields = sorted(f'{t}.{c}' for t, c in fields if toks(c) & SCORE_TOKENS)
    files = []
    for d in (os.path.join(ACAD, 'datos-sinteticos'), DOCS):
        for base, _, fs in os.walk(d):
            files += [os.path.join(base, f) for f in fs]
    media = [f for f in files if MEDIA_OR_DOC.search(f)]
    other = [f for f in files if not re.search(r'\.(csv|json|md)$', f)]
    trace = open(os.path.join(ROOT, 'docs', 'final-report', 'traceability-master.md'), encoding='utf-8').read()
    rf23 = re.search(r'^\| RF-23 \|[^\n]*\(\*\*humana\*\*\)', trace, re.M)
    rf21 = re.search(r'^\| RF-21 \| Calcular ranking configurable', trace, re.M)
    try:
        base_changes = git('diff', '--name-only', BASE, '--', *RUNTIME, *BASELINE)
        untracked = {p for p in git('ls-files', '--others', '--exclude-standard')
                     if p.startswith(tuple(RUNTIME + BASELINE))}
        git_ok, git_detail = not (base_changes | untracked), sorted(base_changes | untracked)[:3]
    except GitError as e:
        git_ok, git_detail = False, str(e)
    refs = []
    for d in RUNTIME_SCAN:
        for base, _, fs in os.walk(os.path.join(ROOT, d)):
            if any(x in base for x in ('node_modules', 'vendor', '.venv', '__pycache__')):
                continue
            for f in fs:
                p = os.path.join(base, f)
                try:
                    if os.path.getsize(p) > 2_000_000:
                        continue
                    txt = open(p, encoding='utf-8', errors='ignore').read()
                except OSError:
                    continue
                if re.search(r'datos-sinteticos|g0-sandbox|f34-synth|\bSBX\b', txt):
                    refs.append(os.path.relpath(p, ROOT))
    DB = V34B.read_all()
    der = V34B.derive(DB, V34B.REAL)
    adr = open(os.path.join(ACAD, 'diseno-inteligente', 'F33_ADR_005_G0.md'), encoding='utf-8').read()
    dec_real = DB['F34B_Decision_G0.md']
    rank = V34A.run_doc_rules(V34A.read_all()).get('RANK', ['regla inexistente'])

    r['SBX-01'] = (not viol('DQ-05', 'DQ-06', 'DQ-07') and manifest.get('source') == 'synthetic',
                   viol('DQ-05', 'DQ-06', 'DQ-07')[:2])
    r['SBX-02'] = (not viol('PII-01', 'PII-02', 'PII-03'), viol('PII-01', 'PII-02', 'PII-03')[:2])
    r['SBX-03'] = (not other and not viol('DQ-04'), (other or viol('DQ-04'))[:2])
    r['SBX-04'] = (not media, media[:2])
    r['SBX-05'] = (not score_fields and not viol('LK-01', 'LK-08'), (score_fields or viol('LK-01', 'LK-08'))[:2])
    r['SBX-06'] = (not [f for f in score_fields if 'recommend' in f or 'recomendacion' in f], score_fields[:2])
    r['SBX-07'] = (not [f for f in score_fields if toks(f) & {'selected', 'seleccionado', 'hire', 'hired', 'contratado'}]
                   and bool(rf23), score_fields[:2])
    r['SBX-08'] = (bool(rf23) and git_ok, 'fila RF-23 «humana»' if rf23 else 'RF-23 sin «humana»')
    r['SBX-09'] = (bool(rf21) and git_ok and not rank, rank[:1])
    r['SBX-10'] = (not viol(*[f'CTX-{i:02d}' for i in range(1, 11)])
                   and all(('applications', 'organization_token') in fields for _ in [0]),
                   viol(*[f'CTX-{i:02d}' for i in range(1, 11)])[:2])
    r['SBX-11'] = (('evidence', 'provenance') in fields and not viol('DQ-07'), viol('DQ-07')[:2])
    r['SBX-12'] = (der.get('G0-09') == 'CUMPLIDO', der.get('G0-09'))
    r['SBX-13'] = (der.get('G0-14') == 'CUMPLIDO' and '- **Estado:** **PROPUESTA**' in adr, der.get('G0-14'))
    r['SBX-14'] = (not viol('DQ-04', 'DQ-07') and 'NO representa datos reales' in manifest.get('note', ''),
                   viol('DQ-04', 'DQ-07')[:2])
    r['SBX-15'] = (not refs, refs[:3])
    r['SBX-16'] = (git_ok, git_detail)
    r['SBX-17'] = ('**Alcance C: no habilitado.**' in dec_real, 'decisión G0 vigente')
    r['SBX-18'] = ('- **G0 = NO APROBADA.**' in dec_real and not V34B.g0_ok(DB, V34B.REAL)
                   and all(der.get(k) != 'CUMPLIDO' for k in ('G0-02', 'G0-03', 'G0-12')),
                   {k: der.get(k) for k in ('G0-02', 'G0-03', 'G0-12')})
    return r, der, V34B, DB


# ---------------------------------------------------------------- reglas sobre los documentos de F34E
def strip_md(s):
    """Quita envoltorios Markdown (F34E-M02-R2): **x**, *x*, _x_, __x__, `x`, ~~x~~ y sus combinaciones simples.
    Los guiones bajos internos («source_type») se conservan."""
    s = re.sub(r'[*`~]', '', s)
    return re.sub(r'(?<!\w)_+|_+(?!\w)', '', s)


def norm_cell(c):
    """Celda normalizada (F34E-M02-R1/R2): sin envoltorios Markdown, espacios colapsados y en mayúsculas."""
    return re.sub(r'\s+', ' ', strip_md(c)).strip().upper()


def rows(text, first):
    """Filas de tabla cuya primera celda normalizada cumple `first`; la sangría y la capitalización no cuentan."""
    out = []
    for ln in text.splitlines():
        s = ln.strip()
        if s.startswith('|'):
            c = [norm_cell(x) for x in s.strip('|').split('|')]
            if c and re.fullmatch(first, c[0], re.I):
                out.append(c)
    return out


# ---------------------------------------------------------------- matriz SBX (F34E-M02-A)
def matrix_rows(D):
    """Todas las filas de criterios (cualquier ID «SBX…», con o sin sangría o mayúsculas), sin colapsar duplicados.
    El ID se normaliza a «SBX-NN» para comparar («sbx-19», «SBX 05» y «SBX–05» cuentan)."""
    out = []
    for r in rows(D['F34E_Matriz_Criterios_G0_SBX.md'], r'SBX.*'):
        out.append([re.sub(r'^SBX[\s\-–—_]*', 'SBX-', r[0])] + r[1:])
    return out


def matrix_problems(D):
    """Estructura de la matriz: exactamente una fila por SBX-01..SBX-18, 5 columnas y un único estado válido."""
    out = []
    rs = matrix_rows(D)
    ids = [r[0] for r in rs]
    for k in sorted(set(ids)):
        n = ids.count(k)
        if n > 1:
            states = sorted({r[-1] for r in rs if r[0] == k})
            kind = 'contradictoria' if len(states) > 1 else 'idéntica'
            out.append(f'{k}: fila duplicada {kind} ({n} filas: {states})')
    unknown = [k for k in ids if k not in SBX_IDS]
    if unknown:
        out.append(f'IDs de criterio desconocidos: {sorted(set(unknown))}')
    missing = [k for k in SBX_IDS if k not in ids]
    if missing:
        out.append(f'faltan criterios en la matriz: {missing}')
    for r in rs:
        if len(r) != 5:
            out.append(f'{r[0]}: fila con {len(r)} columnas (se esperan 5)')
        elif r[-1] not in SBX_STATES:
            out.append(f'{r[0]}: estado «{r[-1]}» no admitido (un único estado: CUMPLE o NO CUMPLE; sin pendientes)')
    return out


def matrix_states(D):
    """{SBX-xx: estado} solo si la matriz está bien formada; si no, {} (falla cerrado en DEC)."""
    if matrix_problems(D):
        return {}
    return {r[0]: r[-1] for r in matrix_rows(D)}


def mtx(D, computed):
    out = matrix_problems(D)
    st = matrix_states(D)
    for k, v in st.items():
        if k in computed and (v == 'CUMPLE') != computed[k]:
            out.append(f'{k}: la matriz dice {v} y el recálculo da {"CUMPLE" if computed[k] else "NO CUMPLE"}')
    t = D['F34E_Matriz_Criterios_G0_SBX.md']
    plain = {r[0]: r[-1] for r in matrix_rows(D)}
    summary = rows(t, r'(?:NO )?CUMPLE')
    for s in SBX_STATES:
        m = [r[-1] for r in summary if r[0] == s]
        if len(m) != 1 or not m[0].isdigit() or int(m[0]) != sum(v == s for v in plain.values()):
            out.append(f'resumen de la matriz: «{s}» ausente, duplicado o distinto de las filas')
    return out


# ---------------------------------------------------------------- estados globales (F34E-M02-B/C)
STATE_ALLOWED = {
    'G0 real': {'NO APROBADA'},                         # esta fase nunca aprueba la G0 real
    'G0-SBX': G0SBX_STATES,
    'F35 productiva': {'BLOQUEADA'},
    'F35-SBX': {'HABILITADA', 'BLOQUEADA'},
    'F36–F40': {'BLOQUEADAS'},
    'Alcance C': {'BLOQUEADO'},
}


# Alias admitidos (ya normalizados: mayúsculas, espacios colapsados, guiones unificados) de cada estado crítico.
STATE_ALIASES = {
    'G0': 'G0 real', 'G0 REAL': 'G0 real', 'G0-SBX': 'G0-SBX', 'F35': 'F35 productiva', 'F35 PRODUCTIVA': 'F35 productiva',
    'F35-SBX': 'F35-SBX', 'F36-F40': 'F36–F40', 'F36': 'F36–F40', 'F37': 'F36–F40', 'F38': 'F36–F40', 'F39': 'F36–F40',
    'F40': 'F36–F40', 'ALCANCE C': 'Alcance C',
}
# Comienzo de un nombre de estado crítico (sin exigir límite de palabra a la derecha: «G0real» también cuenta).
STATE_SUBJECT = re.compile(r'(?<![\w-])(?:G0|F3[5-9]|F40|ALCANCE)', re.I)
STATE_KEY_TAIL = re.compile(r'([\wÁÉÍÓÚÑÜáéíóúñü–—-]+(?:[ \t]+[\wÁÉÍÓÚÑÜáéíóúñü–—-]+){0,3})[ \t]*$')
STATE_VALUE = re.compile(r'[ \t]*([A-Za-zÁÉÍÓÚÑÜáéíóúñü]+(?:[ \t]+[A-Za-zÁÉÍÓÚÑÜáéíóúñü]+)*)?')
STATE_ALT_SEP = re.compile(r'≔|≡|≝|-+>|→|⇒|←|<-+|::|:(?!=)')
STATE_WORD = re.compile(r'APROBAD|HABILITAD|DESBLOQUEAD|BLOQUEAD|AUTORIZAD|CUMPL|PENDIENTE|PARCIAL|RESTRICCI|ACTIV|'
                        r'VIGENTE|CERRAD|ABIERT|REVOCAD|SUSPENDID|PERMITID|PROHIBID')


def norm_key(k):
    """Clave normalizada: mayúsculas, espacios colapsados y guiones –/— unificados."""
    return re.sub(r'\s*[–—-]\s*', '-', re.sub(r'\s+', ' ', k.strip().upper()))


def parse_declarations(text):
    """Declaraciones «CLAVE = ESTADO» de estados críticos, normalizadas antes de interpretar (F34E-M02-R1).

    Devuelve ([(clave canónica, estado)], [problemas]). Es problema toda línea que parezca declarar un estado crítico
    con «=» usando un alias no admitido («G0 productiva», «G0real», «F36-SBX»…) o un estado vacío; los estados no
    admitidos se juzgan en `sta`. Los IDs de criterio G0-NN no son estados globales (los vigila CLM)."""
    decls, problems = [], []
    for ln in text.splitlines():
        s = strip_md(ln)
        # Separadores no admitidos («G0 real: APROBADA», «F35 → HABILITADA», «G0-SBX ≔ …»): fallan cerrado si la clave
        # es un estado crítico y lo que sigue usa vocabulario de estado (F34E-M02-R2).
        for alt in STATE_ALT_SEP.finditer(s):
            m = STATE_KEY_TAIL.search(s[:alt.start()])
            subj = STATE_SUBJECT.search(m.group(1)) if m else None
            if not subj or re.fullmatch(r'G0-\d+', norm_key(m.group(1)[subj.start():])):
                continue
            head = ' '.join((STATE_VALUE.match(s, alt.end()).group(1) or '').upper().split()[:3])
            if STATE_WORD.search(head):
                problems.append(f'declaración de estado crítico con sintaxis desconocida «{alt.group(0)}»: {ln.strip()[:90]}')
        for eq in re.finditer(r':?=', s):            # «=» canónico y «:=» (se interpretan y validan igual)
            m = STATE_KEY_TAIL.search(s[:eq.start()])
            subj = STATE_SUBJECT.search(m.group(1)) if m else None
            if not subj:
                continue
            raw = m.group(1)[subj.start():]
            key = norm_key(raw)
            if re.fullmatch(r'G0-\d+', key):
                continue
            words = (STATE_VALUE.match(s, eq.end()).group(1) or '').upper().split()
            value = ' '.join(words)
            canon = STATE_ALIASES.get(key)
            if canon is None:
                problems.append(f'declaración con alias desconocido «{raw.strip()} = {value}»: {ln.strip()[:90]}')
                continue
            # Prosa tras el estado («NO APROBADA y …»): vale el prefijo admitido más largo, salvo que el resto
            # vuelva a contener vocabulario de estado («no aprobada sino aprobada» se juzga entera).
            for i in range(len(words), 0, -1):
                if ' '.join(words[:i]) in STATE_ALLOWED[canon] and not STATE_WORD.search(' '.join(words[i:])):
                    value = ' '.join(words[:i])
                    break
            decls.append((canon, value))
    return decls, problems


def declarations(text):
    """[(clave canónica, estado normalizado)] de cada declaración «CLAVE = ESTADO» del texto."""
    return parse_declarations(text)[0]


def decision_states(text):
    """(G0-SBX, F35-SBX) declarados en un texto; None si falta o es ambiguo (más de un valor distinto)."""
    d = declarations(text)

    def one(k):
        vals = {v for kk, v in d if kk == k}
        return next(iter(vals)) if len(vals) == 1 else None
    return one('G0-SBX'), one('F35-SBX')


def sta(D, computed):
    """Cada estado crítico se declara exactamente una vez en la decisión, con un valor admitido, y todos los documentos
    del paquete coinciden (ninguna declaración simultánea contradictoria)."""
    out = []
    dec_decl = declarations(D['F34E_Decision_G0_SBX.md'])
    for k, allowed in STATE_ALLOWED.items():
        n = sum(1 for kk, _ in dec_decl if kk == k)
        if n != 1:
            out.append(f'decisión: «{k}» declarado {n} veces (se exige exactamente una declaración)')
    values = {}
    for n, t in D.items():
        decls, problems = parse_declarations(t)
        out += [f'{n}: {p}' for p in problems]
        for k, v in decls:
            values.setdefault(k, set()).add(v)
    for k, vals in values.items():
        if len(vals) > 1:
            out.append(f'«{k}» con estados contradictorios en el paquete: {sorted(vals)}')
        for v in vals:
            if v not in STATE_ALLOWED[k]:
                out.append(f'«{k} = {v or "(vacío)"}» no admitido (permitido: {sorted(STATE_ALLOWED[k])})')
    for k in STATE_ALLOWED:
        if k not in values:
            out.append(f'falta la declaración del estado «{k}»')
    return out


def dec(D, computed):
    """Coherencia: G0-SBX aprobada solo con los 18 criterios en CUMPLE (matriz bien formada y recálculo);
    F35-SBX habilitada solo con G0-SBX aprobada; README igual que la decisión."""
    out = []
    d = D['F34E_Decision_G0_SBX.md']
    g, f = decision_states(d)
    st = matrix_states(D)
    all_ok = len(st) == 18 and all(v == 'CUMPLE' for v in st.values()) and all(computed.get(k) for k in SBX_IDS)
    if g not in G0SBX_STATES:
        out.append(f'estado de G0-SBX «{g}» no admitido o ambiguo')
    if g == 'APROBADA CON RESTRICCIONES' and not all_ok:
        out.append('G0-SBX figura APROBADA CON RESTRICCIONES con criterios SBX sin cumplir o una matriz inválida')
    if f not in STATE_ALLOWED['F35-SBX']:
        out.append(f'estado de F35-SBX «{f}» no admitido o ambiguo')
    if (f == 'HABILITADA') != (g == 'APROBADA CON RESTRICCIONES'):
        out.append(f'F35-SBX = {f} incoherente con G0-SBX = {g}')
    for n in ('F34E_Decision_G0_SBX.md', 'README.md'):
        for s in ('F35 productiva = BLOQUEADA', 'G0 real = NO APROBADA', 'ADR-005 = PROPUESTA', 'Alcance C = BLOQUEADO',
                  'datos reales siguen PROHIBIDOS', 'F36–F40 = BLOQUEADAS'):
            if s not in D[n]:
                out.append(f'{n}: no declara «{s}»')
    if decision_states(D['README.md']) != (g, f):
        out.append(f'README declara {decision_states(D["README.md"])} y la decisión ({g}, {f})')
    return out


# ---------------------------------------------------------------- afirmaciones por proposición (F34E-M01)
# Categorías prohibidas: se detecta su AFIRMACIÓN en cada proposición por separado; negar una no neutraliza otra.
CLAIM_CATEGORIES = {
    'datos reales autorizados': re.compile(r'datos\s+(?:personales\s+)?reales', re.I),
    'PII real': re.compile(r'\bPII\b|\bDNI\b|correos?\s+reales?|tel[eé]fonos?\s+reales?|nombres?\s+reales?', re.I),
    'CV o documentos reales': re.compile(r'\bCVs?\b|documentos?\s+reales?', re.I),
    'audio o vídeo real': re.compile(r'\baudios?\b|v[ií]deos?', re.I),
    'scoring ML': re.compile(r'scoring|puntuaci[oó]n\s+autom|puntajes?\s+autom|'
                             r'(?:punt[uú]a|clasifica|eval[uú]a)\w*\s+a\s+(?:los\s+|las\s+)?(?:candidat|postulant|personas)',
                             re.I),
    'recomendación automática': re.compile(r'recomendaci[oó]n|recomienda', re.I),
    'mejor candidato': re.compile(r'mejor\s+candidat', re.I),
    'ranking automático nuevo': re.compile(r'ranking\s+(?:autom|nuevo)', re.I),
    'selección o decisión automática': re.compile(r'selecci[oó]n\s+autom|decisi[oó]n\s+(?:final\s+)?autom', re.I),
    # Alcance C incluye sus capacidades (CAP-07 y frontera B/C de F33): parsing o extracción automática, OCR,
    # embeddings y búsqueda o localización semántica.
    'alcance C': re.compile(r'alcance\s+c\b|\bOCR\b|embeddings?|extracci[oó]n\s+autom|parsing|'
                            r'(?:b[uú]squeda|localizaci[oó]n|localizador)\s+sem[aá]ntic', re.I),
    'integración o paso a producción': re.compile(r'producci[oó]n|productiv|despliegue|integraci[oó]n', re.I),
    'F35 productiva': re.compile(r'\bF35\b(?!-SBX)', re.I),
    'F36–F40': re.compile(r'\bF3[6-9]\b|\bF40\b', re.I),
}
G0_SUBJECT = re.compile(r'\bG0\b(?!-SBX)', re.I)
# Marcadores de negación o limitación de la proposición.
CLAIM_NEG = re.compile(r'\b(no|ni|nunca|tampoco|sin|jam[aá]s|ning[uú]n\w*|nada|prohibid\w*|bloquead\w*|excluid\w*|fuera|'
                       r'salvo|exig\w*|requier\w*|necesit\w*|pendient\w*|hasta)\b|(?:^|\s)0\s', re.I)
# Negaciones retóricas que afirman: «no solo X», «no deja de ser X», «ni deja de ser X», «no es otra cosa que X»,
# «no es sino X», «no es más que X», «no es distinto de X».
CLAIM_NOT_ONLY = re.compile(r'\bno\s+(?:s[oó]lo|solamente|[uú]nicamente)\b|\b(?:no|ni)\s+(?:deja\w*|dej[oó])\s+de\b|'
                            r'\b(?:no|ni)\s+(?:es|son|era|eran|fue|fueron|ser[aá]n?|resulta\w*|constituye\w*|supone\w*|'
                            r'implica\w*|significa\w*)\s+(?:otra\s+cosa\s+(?:que|sino)|sino|nada\s+m[aá]s\s+que|'
                            r'm[aá]s\s+que|menos\s+que|distint[oa]s?\s+(?:de|a)|diferentes?\s+(?:de|a))\b', re.I)
# Conectores que introducen una proposición afirmativa aunque no lleve verbo («No alcance C, pero recomendación
# automática»): la categoría nominal que sigue cuenta como AFIRMADA salvo negación propia (F34E-M01-R1).
# Concesivos y adversativos («sin embargo», «no obstante», «aun así», «con todo», «pese a ello», «a pesar de ello»)
# abren una proposición afirmativa nueva: la negación previa no se hereda y su «sin»/«no» no cuentan como negación
# propia (F34E-M01-R2). «con todo» solo se reconoce al inicio de la proposición.
CLAIM_CONCESSIVE = (r'sin\s+embargo|no\s+obstante|a[uú]n\s+as[ií]|pese\s+a\s+(?:ello|eso|esto)|'
                    r'a\s+pesar\s+de\s+(?:ello|eso|esto)')
CLAIM_AFFIRM_CONN = {'pero', 'sino', 'aunque', 'y', 'e', 'ademas', 'tambien', 'incluso', 'asimismo', 'igualmente',
                     'sin embargo', 'no obstante', 'aun asi', 'con todo', 'pese a ello', 'pese a eso', 'pese a esto',
                     'a pesar de ello', 'a pesar de eso', 'a pesar de esto'}
CLAIM_LEAD_CONN = re.compile(r'^(' + CLAIM_CONCESSIVE + r'|con\s+todo|pero|sino|aunque|mientras\s+que|y|e|ni|o|u|'
                             r'adem[aá]s|tambi[eé]n|incluso|asimismo|igualmente)\b', re.I)
# Predicados que afirman o habilitan: formas verbales y participios, no sustantivos («despliegue», «migraciones»,
# «integración» o «aprobada» solos no afirman nada).
CLAIM_PRED = re.compile(r'\b(s[ií]|tambi[eé]n|adem[aá]s|habilit[aeo]\w*|autoriz[aeo]\w*|permit[aei]\w*|desbloque[aeo]\w*|'
                        r'conect[aeo]\w*|aliment[aeo]\w*|integra|integran|integrar\w*|integrad[oa]s?|migra|migran|'
                        r'migrar\w*|migrad[oa]s?|despleg[aá]\w*|despliega\w*|activ[aeo]\w*|genera|generan|generar\w*|'
                        r'generad[oa]s?|produce|producen|utiliz[aeo]\w*|emple[aeo]\w*|incorpor[aeo]\w*|admit[aei]\w*|'
                        r'acept[aeo]\w*|usa|usan|usar\w*|usad[oa]s?|procesa|procesan|procesar\w*|env[ií]a\w*|'
                        r'publica|publican|publicar\w*|recomienda\w*|recomendad[oa]s?|punt[uú]a\w*|clasifica|'
                        r'clasifican|selecciona|seleccionan|descarta|descartan|contrata|contratan|ordena|ordenan)\b', re.I)
# «G0 real» aprobada solo como afirmación verbal («queda/quedó/está/fue aprobada», «se aprueba», «aprobó»).
G0_APPROVED = re.compile(r'\b(?:qued[aó]|est[aá]|fue|ha\s+sido|es|se\s+considera)\s+aprobad|\bse\s+aprueba\b|\baprob[oó]\b',
                         re.I)
CLAIM_SPLIT = re.compile(r'(\s*[,;:()—]\s*|\s+(?:' + CLAIM_CONCESSIVE + r'|pero|sino|aunque|mientras\s+que|y|e|ni|o|u)\s+)',
                         re.I)


def claim_props(sentence, context=None):
    """Proposiciones con su polaridad: 'neg', 'pos' o 'neutral'.

    pos (retórica): «no solo», «no/ni deja de», «no es otra cosa que», «no es sino»… afirman.
    neg: marcador de negación/limitación propio o tras «ni».
    pos: predicado afirmativo o habilitante propio, o introducida por un conector afirmativo («pero», «sino»,
    «aunque», «y», «además», «también»…), esté tras el separador o al inicio de la proposición («…, pero X»).
    sin marcador propio: hereda la polaridad de la proposición anterior (elipsis); la primera es neutral
    salvo que el contexto de tabla la fije («Permitido…» = pos, «Prohibido…» = neg).
    """
    parts = CLAIM_SPLIT.split(sentence)
    out, prev, sep = [], context or 'neutral', ''
    for i, p in enumerate(parts):
        if i % 2 == 1:
            sep = p.strip().lower()
            continue
        if not p.strip():
            continue
        lead = CLAIM_LEAD_CONN.match(p.strip())
        conn = re.sub(r'\s+', ' ', (lead.group(1) if lead else sep).lower())
        conn = conn.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ú', 'u')
        body = p.strip()[lead.end():] if lead else p      # el conector no es marcador propio («sin embargo»)
        if CLAIM_NOT_ONLY.search(f'{sep} {p}'):
            pol = 'pos'
        elif CLAIM_NEG.search(body) or conn == 'ni':
            pol = 'neg'
        elif conn in CLAIM_AFFIRM_CONN or CLAIM_PRED.search(p):
            pol = 'pos'
        else:
            pol = prev
        out.append((p.strip(), pol))
        prev = pol
    return out


def text_claims(text, context=None):
    found = []
    for sentence in re.split(r'(?<=[.!?])\s+', text):
        for prop, pol in claim_props(sentence, context):
            if G0_SUBJECT.search(prop) and G0_APPROVED.search(prop) and not CLAIM_NEG.search(prop):
                found.append(('G0 real aprobada', prop))    # afirmación verbal propia, aunque la elipsis sea neutral
            if pol != 'pos':
                continue
            for cat, rx in CLAIM_CATEGORIES.items():
                if rx.search(prop):
                    found.append((cat, prop))
    return found


def table_context(header_first_cell):
    h = header_first_cell.lower()
    if h.startswith('permitid'):
        return 'pos'
    if h.startswith('prohibid'):
        return 'neg'
    return None


# Afirmaciones con forma de declaración: siempre fallan (no dependen de la polaridad ni de mayúsculas o espacios).
STRICT_CLAIMS = [
    ('aprobación de G0 sin el sufijo SBX', re.compile(r'\bG0(?:\s*real)?\s*:?=\s*\**\s*APROBADA', re.I)),
    ('F35 productiva desbloqueada',
     re.compile(r'\bF35(?!\s*-\s*SBX)(?:\s+productiva)?\s*:?=\s*\**\s*(?:HABILITADA|DESBLOQUEADA)', re.I)),
    ('F36–F40 desbloqueadas',
     re.compile(r'\bF(?:3[6-9]|40)(?:\s*[–-]\s*F40)?(?:-SBX)?\s*:?=\s*\**\s*(?:HABILITADAS?|DESBLOQUEADAS?)', re.I)),
    ('alcance C habilitado', re.compile(r'alcance\s+C\s*:?=\s*\**\s*(?:HABILITAD|APROBAD|DESBLOQUEAD)', re.I)),
    ('evidencia externa inventada', re.compile(r'G0-(?:02|03|12)\s*(?::?=|:)\s*\**\s*CUMPLIDO', re.I)),
]


def clm(D, computed):
    """Ninguna afirmación positiva de una categoría prohibida, evaluada proposición por proposición (F34E-M01)."""
    out = []
    for n, t in D.items():
        header_ctx = None
        lines = [x.strip() for x in t.splitlines()]                     # la sangría no cuenta (F34E-M02-R1)
        for i, ln in enumerate(lines, 1):
            for what, rx in STRICT_CLAIMS:
                if rx.search(ln) or rx.search(strip_md(ln)):     # también sin envoltorios Markdown
                    out.append(f'{n}:{i}: {what}: {ln[:90]}')
            body = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', ln)      # enlaces: solo su texto
            body = re.sub(r'`[^`]*`|[*]', '', body)                    # código y negritas
            if ln.startswith('|'):
                cells_ = [c.strip() for c in body.strip().strip('|').split('|')]
                if set(ln.replace('|', '').strip()) <= set('-: '):
                    continue
                if i < len(lines) and lines[i].startswith('|') and set(lines[i].replace('|', '').strip()) <= set('-: '):
                    header_ctx = table_context(cells_[0])               # fila de cabecera
                    continue
                found = []
                for j, c in enumerate(cells_):
                    found += text_claims(c, header_ctx if j == 0 else None)
            else:
                header_ctx = None
                found = text_claims(body)
            for cat, prop in found:
                out.append(f'{n}:{i}: afirma «{cat}»: {prop[:80]}')
    return out


def lnk(D, computed):
    out = []

    def slug(h):
        h = re.sub(r'[`*_]', '', h.strip().lower())
        return re.sub(r'[^\w\- ]', '', h).replace(' ', '-')
    for n, t in D.items():
        for link in re.findall(r'\]\(([^)\s]+)\)', t):
            if link.startswith(('http://', 'https://')):
                continue
            path, _, anchor = link.partition('#')
            target = os.path.normpath(os.path.join(DOCS, path)) if path else os.path.join(DOCS, n)
            if not os.path.exists(target):
                out.append(f'{n}→{link}')
            elif anchor and target.endswith('.md'):
                src = D.get(os.path.basename(target)) if os.path.dirname(target) == DOCS else None
                src = src if src is not None else open(target, encoding='utf-8').read()
                if anchor not in {slug(h) for h in re.findall(r'^#+ (.+)$', src, re.M)}:
                    out.append(f'{n}→{link}')
    return out


DOC_RULES = [('MTX', mtx), ('STA', sta), ('DEC', dec), ('CLM', clm), ('LNK', lnk)]


def run_doc_rules(D, computed):
    return {rid: fn(D, computed) for rid, fn in DOC_RULES}


# ---------------------------------------------------------------- estado real, F34C/F34D y Git
def real_checks(der, V34B, DB, listing=None):
    out = []
    if '- **G0 = NO APROBADA.**' not in DB['F34B_Decision_G0.md']:
        out.append('la decisión G0 vigente ya no declara «G0 = NO APROBADA»')
    for k in ('G0-02', 'G0-03', 'G0-12'):
        if der.get(k) == 'CUMPLIDO':
            out.append(f'{k} figura CUMPLIDO: F34E no aporta evidencia externa')
    if der.get('G0-14') != 'CUMPLIDO' or der.get('G0-09') != 'CUMPLIDO':
        out.append(f'F34C alterada: G0-14={der.get("G0-14")}, G0-09={der.get("G0-09")}')
    att = os.path.join(ACAD, 'g0-evidence', 'adjuntos')
    files = sorted(f for f in os.listdir(att) if f != 'README.md') if listing is None else sorted(listing)
    if set(files) != set(F34C_ATTACHMENTS):
        out.append(f'adjuntos distintos de los de F34C (evidencia externa añadida o retirada en F34E): '
                   f'{sorted(set(files) ^ set(F34C_ATTACHMENTS))}')
    for f, h in F34C_ATTACHMENTS.items():
        p = os.path.join(att, f)
        if listing is None and (not os.path.isfile(p) or sha_file(p) != h):
            out.append(f'adjunto de F34C alterado: {f}')
    adr = open(os.path.join(ACAD, 'diseno-inteligente', 'F33_ADR_005_G0.md'), encoding='utf-8').read()
    if '- **Estado:** **PROPUESTA**' not in adr:
        out.append('ADR-005 canónico ya no es PROPUESTA')
    return out


def git_checks():
    out = []
    try:
        if git('rev-parse', '--is-inside-work-tree') != {'true'}:
            raise GitError('repositorio inválido')
        if git('rev-parse', '--verify', '--quiet', BASE + '^{commit}') != {BASE}:
            raise GitError('base F34D no resuelta')
        head = git('rev-parse', '--verify', '--quiet', 'HEAD^{commit}')
        if len(head) != 1 or not re.fullmatch(r'[0-9a-f]{40}', next(iter(head))):
            raise GitError('HEAD inválido')
        git('merge-base', '--is-ancestor', BASE, 'HEAD')
        changed = git('diff', '--name-only', BASE) | git('ls-files', '--others', '--exclude-standard')
        blob = subprocess.run(['git', 'show', BASE + ':' + F34B_VALIDATOR], cwd=ROOT, capture_output=True)
        if blob.returncode != 0 or hashlib.sha256(blob.stdout).hexdigest() != F34D_VALIDATOR_SHA:
            raise GitError('snapshot publicado de validate_f34b.py incoherente')
        V34B = load_module('f34b_scope', os.path.join(ROOT, F34B_VALIDATOR))
        violations, mode = V34B.git_scope()
        if violations or mode != 'post':
            out.append(f'alcance de validate_f34b.py debe ser post válido: {mode}, {violations}')
        if not all(ok for ok, _ in V34B.scope_regressions()):
            out.append('regresión de protección Git de validate_f34b.py')
        for p, expected in F34D_DELIVERED.items():
            if not os.path.isfile(os.path.join(ROOT, p)) or sha_file(os.path.join(ROOT, p)) != expected:
                out.append(f'documento publicado de F34D modificado: {p}')
    except (GitError, OSError) as e:
        return [f'estado Git desconocido (falla cerrado): {e}']
    for p in sorted(changed):
        if p.startswith(F35SBX_ROOTS) and not f35sbx_path(p):
            out.append(f'ruta F35-SBX no autorizada por DH-02: {p}')
        elif V34B.post_f34e_path(p):
            continue
        else:
            out.append(f'cambio fuera del alcance de F34E: {p}')
    return out


# DH-02 (F35-SBX-A), segunda llave independiente de validate_f34b.py.
F35SBX_ROOTS = ('docs/academico/evidencia-sbx', 'docs/academico/tools/f35sbx')


def f35sbx_path(p):
    if '\\' in p or any(part in ('', '.', '..') for part in p.split('/')):
        return False
    if p.startswith('docs/academico/evidencia-sbx/'):
        return p.endswith(('.md', '.json'))
    return p.startswith('docs/academico/tools/f35sbx/') and p.endswith('.py')


def f35sbx_scope_regressions(V34B):
    """Ambas llaves deben coincidir: lo que DH-02 autoriza y nada más (incluidas rutas confundibles)."""
    ok_paths = ('docs/academico/evidencia-sbx/README.md', 'docs/academico/evidencia-sbx/contrato/f35sbx_contract.json',
                'docs/academico/tools/f35sbx/validate_f35sbx.py')
    bad_paths = ('docs/academico/evidencia-sbx/foto.png', 'docs/academico/evidencia-sbx/audio.mp3',
                 'docs/academico/evidencia-sbx/informe.pdf', 'docs/academico/evidencia-sbx/x.py',
                 'docs/academico/tools/f35sbx/datos.json', 'docs/academico/evidencia-sbx-otro/a.md',
                 'docs/academico/evidencia-sbx/../g0-evidence/F34B_Decision_G0.md', 'docs/academico/tools/f35sbx-x/a.py',
                 'app/Models/SyntheticEvidence.php', 'tests/Feature/SbxTest.php', 'database/migrations/x.php')
    out = [(f35sbx_path(p) and V34B.post_f34e_path(p), f'F35-SBX: ruta autorizada {p}') for p in ok_paths]
    out += [(not f35sbx_path(p) and not V34B.post_f34e_path(p), f'F35-SBX: ruta rechazada {p}') for p in bad_paths]
    # Validadores históricos adaptados en F35-SBX-A: exactamente estas tres rutas en ambas llaves.
    out.append((getattr(V34B, 'F35SBX_HISTORICAL', None) == F35SBX_HISTORICAL,
                'F35-SBX: validate_f34b autoriza exactamente los tres validadores históricos'))
    out += [(V34B.post_f34e_path(p), f'F35-SBX: validador histórico autorizado {p}') for p in sorted(F35SBX_HISTORICAL)]
    for p in ('docs/academico/tools/f34a/validate_f34a.py', 'docs/academico/tools/f30/f30.py',
              'docs/academico/tools/f27b/validate.py', 'docs/academico/powerdesigner/scripts/validate_f29.py',
              'docs/academico/tools/f33/otro.py', 'docs/academico/tools/f34/schema.json'):
        out.append((not V34B.post_f34e_path(p), f'F35-SBX: cuarto validador o archivo no autorizado rechazado {p}'))
    return out


F35SBX_HISTORICAL = frozenset({'docs/academico/tools/f30/validate_f30.py', 'docs/academico/tools/f33/validate_f33.py',
                               'docs/academico/tools/f34/validate_f34.py'})


# ---------------------------------------------------------------- casos negativos
def sub(n, a, b):
    def f(D):
        assert a in D[n], (n, a)
        D = dict(D)
        D[n] = D[n].replace(a, b, 1)
        return D
    return f


def rsub(n, pat, rep):
    def f(D):
        D = dict(D)
        new = re.sub(pat, rep, D[n], count=1, flags=re.M)
        assert new != D[n], (n, pat)
        D[n] = new
        return D
    return f


DEC_ = 'F34E_Decision_G0_SBX.md'
MTX_ = 'F34E_Matriz_Criterios_G0_SBX.md'
ADD = '## 2. Criterios'
CASES = [
    ('N-01', 'CLM', '«G0 = APROBADA» sin sufijo SBX', sub('README.md', '**G0 real = NO APROBADA**', '**G0 = APROBADA**'), None),
    ('N-02', 'CLM', '«G0 real = APROBADA CON RESTRICCIONES»',
     sub(DEC_, '- **G0 real = NO APROBADA.**', '- **G0 real = APROBADA CON RESTRICCIONES.**'), None),
    ('N-03', 'CLM', 'Frase «la G0 real quedó aprobada»', sub(DEC_, ADD, 'Con F34E la G0 real quedó aprobada.\n\n' + ADD), None),
    ('N-04', 'CLM', 'Autorización de datos reales', sub(DEC_, ADD, 'En F35-SBX los datos reales quedan autorizados.\n\n' + ADD),
     None),
    ('N-05', 'CLM', 'F35 productiva desbloqueada',
     sub(DEC_, '- **F35 productiva = BLOQUEADA.**', '- **F35 productiva = HABILITADA.**'), None),
    ('N-06', 'CLM', 'F36 desbloqueada', sub(DEC_, ADD, '- **F36 = HABILITADA.**\n\n' + ADD), None),
    ('N-07', 'CLM', 'Scoring ML habilitado', sub(DEC_, ADD, 'En F35-SBX se habilita el scoring ML de candidatos.\n\n' + ADD),
     None),
    ('N-08', 'CLM', 'Recomendación automática del mejor candidato',
     sub(DEC_, ADD, 'F35-SBX genera la recomendación automática del mejor candidato.\n\n' + ADD), None),
    ('N-09', 'CLM', 'Alcance C habilitado', sub(DEC_, '- **Alcance C = BLOQUEADO.**', '- **Alcance C = HABILITADO.**'), None),
    ('N-10', 'CLM', 'Evidencia externa inventada en el texto («G0-02 = CUMPLIDO»)',
     sub(DEC_, ADD, '- G0-02 = CUMPLIDO por revisión interna.\n\n' + ADD), None),
    ('N-11', 'MTX', 'Criterio SBX pendiente mientras G0-SBX figura aprobada',
     rsub(MTX_, r'^(\| SBX-05 \|.*\| )CUMPLE \|$', r'\1PENDIENTE |'), None),
    ('N-12', 'DEC', 'G0-SBX aprobada aunque el recálculo de SBX-12 falla', lambda D: D, {'SBX-12': False}),
    ('N-13', 'MTX', 'La matriz dice CUMPLE pero el recálculo de SBX-16 falla', lambda D: D, {'SBX-16': False}),
    ('N-14', 'DEC', 'F35-SBX HABILITADA con G0-SBX NO APROBADA',
     sub(DEC_, '- **G0-SBX = APROBADA CON RESTRICCIONES.**', '- **G0-SBX = NO APROBADA.**'), None),
    ('N-15', 'MTX', 'Falta el criterio SBX-18 en la matriz', rsub(MTX_, r'^\| SBX-18 \|.*\n', ''), None),
    ('N-16', 'MTX', 'Resumen de la matriz incoherente', sub(MTX_, '| CUMPLE | SBX-01 a SBX-18 | 18 |', '| CUMPLE | SBX-01 a SBX-18 | 17 |'),
     None),
    ('N-17', 'DEC', 'README con un estado de G0-SBX distinto de la decisión',
     sub('README.md', '**G0-SBX = APROBADA CON RESTRICCIONES**', '**G0-SBX = NO APROBADA**'), None),
    ('N-18', 'DEC', 'Se omite que los datos reales siguen prohibidos',
     sub(DEC_, '- **Los datos reales siguen PROHIBIDOS.**', '- Datos: ver prohibiciones.'), None),
    ('N-19', 'DEC', 'Se omite que F35 productiva sigue bloqueada',
     sub(DEC_, '- **F35 productiva = BLOQUEADA.**', '- F35 productiva: sin cambios.'), None),
    ('N-20', 'DEC', 'G0-SBX «APROBADA» sin restricciones (estado no admitido)',
     sub(DEC_, '- **G0-SBX = APROBADA CON RESTRICCIONES.**', '- **G0-SBX = APROBADA.**'), None),
    ('N-21', 'DEC', 'ADR-005 omitido como PROPUESTA', sub(DEC_, '- **ADR-005 = PROPUESTA** (estado canónico)', '- ADR-005 aprobado'),
     None),
    ('N-22', 'CLM', 'Ranking automático nuevo permitido', sub(DEC_, ADD, 'Queda permitido un ranking automático nuevo.\n\n' + ADD),
     None),
]


def say(text, n=DEC_):
    """Inserta una frase antes de la sección de criterios (o al final de otro documento)."""
    if n == DEC_:
        return sub(DEC_, ADD, text + '\n\n' + ADD)
    return lambda D: dict(D, **{n: D[n] + '\n' + text + '\n'})


CASES += [
    # ---- F34E-M01: afirmaciones por proposición; una negación no neutraliza otra afirmación
    ('N-25', 'CLM', '«No cambia el runtime, pero autoriza datos reales»', say('No cambia el runtime, pero autoriza datos reales.'), None),
    ('N-26', 'CLM', '«No modifica RF-23, pero se habilita el scoring ML»',
     say('No modifica RF-23, pero se habilita el scoring ML de candidatos.'), None),
    ('N-27', 'CLM', '«F35 queda desbloqueada»', say('F35 queda desbloqueada.'), None),
    ('N-28', 'CLM', '«no datos reales, pero sí scoring»', say('No usa datos reales, pero sí scoring.'), None),
    ('N-29', 'CLM', '«no scoring, pero F35 productiva habilitada»', say('No hay scoring, pero F35 productiva queda habilitada.'), None),
    ('N-30', 'CLM', '«no alcance C, pero recomendación automática»',
     say('No habilita el alcance C, pero sí la recomendación automática.'), None),
    ('N-31', 'CLM', '«G0 real no aprobada, pero producción autorizada»',
     say('La G0 real no está aprobada, pero la producción queda autorizada.'), None),
    ('N-32', 'CLM', '«no modifica runtime, pero conecta resultados SBX a producción»',
     say('No modifica el runtime, pero conecta los resultados SBX a producción.'), None),
    ('N-33', 'CLM', '«sin datos reales, aunque se usan CV reales»', say('Sin datos reales, aunque se usan CV reales.'), None),
    ('N-34', 'CLM', '«no solo es sintético: también admite PII real»', say('No solo es sintético: también admite PII real.'), None),
    ('N-35', 'CLM', 'Scoring añadido como fila de la tabla «Permitido en F35-SBX»',
     sub('F34E_Alcance_Autorizado.md', '| Schemas y contratos |', '| Scoring ML de candidatos | Para pruebas internas |\n| Schemas y contratos |'),
     None),
    ('N-36', 'CLM', '«F35-SBX habilita F37»', say('F35-SBX habilita F37.'), None),
    ('N-37', 'CLM', '«el mejor candidato se recomienda al aprobador»', say('El mejor candidato se recomienda al aprobador.'), None),
    ('N-38', 'CLM', '«los resultados SBX migran a producción»', say('Los resultados SBX migran a producción.'), None),
    ('N-39', 'CLM', '«el sistema puntúa a los candidatos»', say('En F35-SBX el sistema puntúa a los candidatos.'), None),
    # ---- F34E-M02-A: matriz SBX
    ('N-40', 'MTX', 'SBX-05 duplicada y contradictoria (PENDIENTE y CUMPLE)',
     rsub(MTX_, r'^(\| SBX-05 \|.*\| )CUMPLE \|$', r'\1PENDIENTE |\n\g<0>'), None),
    ('N-41', 'MTX', 'SBX-07 duplicada idéntica', rsub(MTX_, r'^\| SBX-07 \|.*$', r'\g<0>\n\g<0>'), None),
    ('N-42', 'MTX', 'Criterio desconocido SBX-19',
     rsub(MTX_, r'^\| SBX-18 \|.*$', r'\g<0>' + '\n| SBX-19 | Criterio inventado | — | — | CUMPLE |'), None),
    ('N-43', 'MTX', 'Fila con dos estados («CUMPLE / PENDIENTE»)', rsub(MTX_, r'^(\| SBX-03 \|.*\| )CUMPLE \|$', r'\1CUMPLE / PENDIENTE |'),
     None),
    ('N-44', 'MTX', 'Fila mal formada (columna de más)', rsub(MTX_, r'^(\| SBX-09 \|.*\| )CUMPLE \|$', r'\1extra | CUMPLE |'), None),
    # ---- F34E-M02-B: estados globales contradictorios o ausentes
    ('N-45', 'STA', 'G0-SBX declarada NO APROBADA y APROBADA CON RESTRICCIONES', say('- **G0-SBX = NO APROBADA.**'), None),
    ('N-46', 'STA', 'F35-SBX declarada BLOQUEADA y HABILITADA', say('- **F35-SBX = BLOQUEADA.**'), None),
    ('N-47', 'STA', 'G0 real NO APROBADA y «G0 = APROBADA»', say('- G0 = APROBADA.', 'README.md'), None),
    ('N-48', 'STA', 'F35 productiva BLOQUEADA y «F35 = DESBLOQUEADA»', say('- F35 = DESBLOQUEADA.', 'F34E_Autorizacion_F35_SBX.md'),
     None),
    ('N-49', 'STA', 'F36–F40 BLOQUEADAS y «F38 = HABILITADA»', say('- **F38 = HABILITADA.**'), None),
    ('N-50', 'STA', 'Falta la declaración de «Alcance C» en la decisión',
     sub(DEC_, '- **Alcance C = BLOQUEADO.**\n', ''), None),
    # ---- F34E-M02-C: coherencia
    ('N-51', 'DEC', 'G0-SBX NO APROBADA (decisión y README) con F35-SBX HABILITADA',
     lambda D: dict(D, **{n: D[n].replace('G0-SBX = APROBADA CON RESTRICCIONES', 'G0-SBX = NO APROBADA')
                          for n in (DEC_, 'README.md')}), None),
    ('N-52', 'DEC', 'G0-SBX aprobada con una matriz inválida (fila duplicada)',
     rsub(MTX_, r'^\| SBX-11 \|.*$', r'\g<0>\n\g<0>'), None),
]

REL_ = 'F34E_Relacion_G0_Real_vs_SBX.md'
CASES += [
    # ---- F34E-M01-R1: elipsis tras conector y negaciones retóricas
    ('N-53', 'CLM', '«No alcance C, pero recomendación automática»', say('No alcance C, pero recomendación automática.'), None),
    ('N-54', 'CLM', '«No scoring, pero selección automática»', say('No scoring, pero selección automática.'), None),
    ('N-55', 'CLM', '«No producción, pero integración»', say('No producción, pero integración.'), None),
    ('N-56', 'CLM', '«No es otra cosa que autorización de datos reales»',
     say('No es otra cosa que autorización de datos reales.'), None),
    ('N-57', 'CLM', '«No es sino recomendación automática»', say('No es sino recomendación automática.'), None),
    ('N-58', 'CLM', '«No deja de ser scoring»', say('No deja de ser scoring.'), None),
    ('N-59', 'CLM', '«Ni deja de ser selección automática»', say('Ni deja de ser selección automática.'), None),
    ('N-60', 'CLM', '«Sin datos reales; además PII real»', say('Sin datos reales; además PII real.'), None),
    # ---- F34E-M02-R1: normalización de la matriz
    ('N-61', 'MTX', 'SBX-19 con sangría', rsub(MTX_, r'^\| SBX-18 \|.*$', r'\g<0>' + '\n   | SBX-19 | Criterio inventado | — | — | CUMPLE |'),
     None),
    ('N-62', 'MTX', 'SBX-19 en minúsculas («sbx-19»)',
     rsub(MTX_, r'^\| SBX-18 \|.*$', r'\g<0>' + '\n| sbx-19 | Criterio inventado | — | — | CUMPLE |'), None),
    ('N-63', 'MTX', 'SBX-05 duplicada con sangría, minúsculas y estado «pendiente»',
     rsub(MTX_, r'^\| SBX-18 \|.*$', r'\g<0>' + '\n  |  sbx-05 | Duplicado | — | — | pendiente |'), None),
    # ---- F34E-M02-R1: declaraciones normalizadas (fuera de la decisión, para no depender del recuento)
    ('N-64', 'STA', '« G0 real = aprobada »', say(' G0 real = aprobada ', 'README.md'), None),
    ('N-65', 'STA', '«g0 REAL=APROBADA»', say('g0 REAL=APROBADA', REL_), None),
    ('N-66', 'STA', 'Alias desconocido de G0 real («G0 productiva = NO APROBADA»)',
     say('- G0 productiva = NO APROBADA.', 'README.md'), None),
    ('N-67', 'STA', 'Alias desconocido pegado («G0real = NO APROBADA»)', say('- G0real = NO APROBADA.', REL_), None),
    ('N-68', 'STA', 'Estado desconocido («F35-SBX = PARCIAL»)', say('- F35-SBX = PARCIAL.', 'README.md'), None),
    ('N-69', 'STA', 'Duplicado contradictorio con otro espaciado y mayúsculas («g0-sbx  =  no aprobada»)',
     say('-  g0-sbx  =  no aprobada .', REL_), None),
    ('N-70', 'STA', 'Estado admitido seguido de otro estado («G0 real = no aprobada sino aprobada»)',
     say('- G0 real = no aprobada sino aprobada.', 'README.md'), None),
    ('N-71', 'STA', 'Alias desconocido de fase («F36-SBX = HABILITADA»)', say('- f36-sbx = habilitada.', REL_), None),
    ('N-72', 'CLM', 'Fila con sangría en la tabla «Permitido en F35-SBX»',
     sub('F34E_Alcance_Autorizado.md', '| Schemas y contratos |', '   | Scoring ML de candidatos | Para pruebas internas |\n| Schemas y contratos |'),
     None),
]

SBX19 = ' Criterio inventado | — | — | CUMPLE |'
CASES += [
    # ---- F34E-M01-R2: conectores concesivos/adversativos (la negación previa no se hereda)
    ('N-73', 'CLM', '«No scoring; sin embargo ranking automático»', say('No scoring; sin embargo ranking automático.'), None),
    ('N-74', 'CLM', '«No scoring; no obstante recomendación automática»',
     say('No scoring; no obstante recomendación automática.'), None),
    ('N-75', 'CLM', '«No producción; aun así integración productiva»', say('No producción; aun así integración productiva.'),
     None),
    ('N-76', 'CLM', '«No selección automática; con todo recomienda candidatos»',
     say('No selección automática; con todo recomienda candidatos.'), None),
    ('N-77', 'CLM', '«No alcance C; pese a ello se habilita OCR»', say('No alcance C; pese a ello se habilita OCR.'), None),
    ('N-78', 'CLM', '«No scoring; aún así, ranking automático»', say('No scoring; aún así, ranking automático.'), None),
    ('N-79', 'CLM', '«No scoring; a pesar de ello recomendación automática»',
     say('No scoring; a pesar de ello recomendación automática.'), None),
    # ---- F34E-M02-R2: envoltorios Markdown en IDs de la matriz
    ('N-80', 'MTX', '«|_SBX-19_|…»', rsub(MTX_, r'^\| SBX-18 \|.*$', r'\g<0>' + '\n|_SBX-19_|' + SBX19), None),
    ('N-81', 'MTX', '«|*SBX-19*|…»', rsub(MTX_, r'^\| SBX-18 \|.*$', r'\g<0>' + '\n|*SBX-19*|' + SBX19), None),
    ('N-82', 'MTX', '«|`SBX-19`|…»', rsub(MTX_, r'^\| SBX-18 \|.*$', r'\g<0>' + '\n|`SBX-19`|' + SBX19), None),
    ('N-83', 'MTX', 'SBX-05 duplicada como «_SBX-05_»',
     rsub(MTX_, r'^\| SBX-05 (\|.*)$', r'\g<0>' + '\n| _SBX-05_ ' + r'\1'), None),
    # ---- F34E-M02-R2: Markdown y separadores en declaraciones críticas
    ('N-84', 'STA', '«_G0 real_ = _APROBADA_»', say('- _G0 real_ = _APROBADA_', 'README.md'), None),
    ('N-85', 'STA', '«G0 real := APROBADA»', say('- G0 real := APROBADA', REL_), None),
    ('N-86', 'STA', '«`G0 real` = `APROBADA`»', say('- `G0 real` = `APROBADA`', 'README.md'), None),
    ('N-87', 'DEC', '«G0-SBX := NO APROBADA» con «F35-SBX = HABILITADA»',
     lambda D: dict(D, **{n: D[n].replace('G0-SBX = APROBADA CON RESTRICCIONES', 'G0-SBX := NO APROBADA')
                          for n in (DEC_, 'README.md')}), None),
    ('N-88', 'STA', 'Separador desconocido «G0 real: APROBADA»', say('- G0 real: APROBADA', REL_), None),
    ('N-89', 'STA', 'Separador desconocido «F35 → HABILITADA»', say('- F35 → HABILITADA', 'README.md'), None),
    ('N-90', 'STA', 'Separador desconocido con estado admitido «G0-SBX ≔ APROBADA CON RESTRICCIONES»',
     say('- G0-SBX ≔ APROBADA CON RESTRICCIONES', REL_), None),
]

# Negaciones simples que NO deben producir afirmaciones (sin falsos positivos).
CLAIM_NEGATIVE_CONTROLS = ['No autoriza datos reales.', 'No permite recomendación automática.', 'No habilita alcance C.',
                           'No conecta resultados SBX a producción.', 'Ni scoring ni recomendación automática.',
                           'No usa datos reales, pero sí datos sintéticos.', 'No scoring ni ranking automático.',
                           'No recomienda candidatos.', 'No integra con producción.', 'No obstante, no usa scoring.']


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    checks = []
    add = lambda ok, msg: checks.append((bool(ok), msg))
    for n in FILES:
        add(os.path.isfile(os.path.join(DOCS, n)), f'documento presente: {n}')
    D = read_all()
    sbx, der, V34B, DB = compute_sbx()
    computed = {k: v[0] for k, v in sbx.items()}
    for k in SBX_IDS:
        add(computed.get(k), f'{k} recalculado: {"CUMPLE" if computed.get(k) else "NO CUMPLE"} {"" if computed.get(k) else sbx[k][1]}')
    res = run_doc_rules(D, computed)
    for rid, viol in res.items():
        add(not viol, f'{rid}: {len(viol)} violaciones' + (f' — {viol[:2]}' if viol else ''))
    rv = real_checks(der, V34B, DB)
    add(not rv, f'REAL: G0 real, pendientes, ADR-005, F34C intacta: {rv}')
    gv = git_checks()
    add(not gv, f'GIT: solo F34E y adaptación de alcance F34B; F34D publicada, runtime y baseline intactos: {gv}')
    checks.extend(V34B.post_policy_regressions())
    checks.extend(f35sbx_scope_regressions(V34B))

    for cid, rule, what, mut, override in CASES:
        try:
            Dm = mut(D)
        except AssertionError as e:
            add(False, f'{cid}: la mutación no se pudo aplicar ({e})')
            continue
        comp = dict(computed, **(override or {}))
        r = run_doc_rules(Dm, comp)
        add(r.get(rule), f'{cid} detectado por {rule}: {what}')
    extra = real_checks(der, V34B, DB, listing=list(F34C_ATTACHMENTS) + ['G0-02_informe_juridico_2026-10-04.pdf'])
    add(extra, 'N-23 detectado por REAL: adjunto externo nuevo (evidencia inventada) en F34E')
    fake_der = dict(der, **{'G0-03': 'CUMPLIDO'})
    add(real_checks(fake_der, V34B, DB), 'N-24 detectado por REAL: G0-03 cerrado sin evidencia')
    add(len(CASES) >= 88, f'casos negativos: {len(CASES) + 2}')
    for s in CLAIM_NEGATIVE_CONTROLS:
        add(not text_claims(s), f'sin falso positivo: «{s}» {text_claims(s)}')
        Dp = say(s)(D)
        bad = {k: v[:1] for k, v in run_doc_rules(Dp, computed).items() if v}
        add(not bad, f'sin falso positivo en la decisión: «{s}» {bad}')

    # Control: con un criterio fallido y documentos coherentes (NO APROBADA / BLOQUEADA), el validador no fuerza nada.
    Dn = dict(D)
    Dn[MTX_] = re.sub(r'^(\| SBX-12 \|.*\| )CUMPLE \|$', r'\1NO CUMPLE |', Dn[MTX_], count=1, flags=re.M)
    Dn[MTX_] = Dn[MTX_].replace('| CUMPLE | SBX-01 a SBX-18 | 18 |', '| CUMPLE | 17 criterios | 17 |')
    Dn[MTX_] = Dn[MTX_].replace('| NO CUMPLE | — | 0 |', '| NO CUMPLE | SBX-12 | 1 |')
    for n in (DEC_, 'README.md'):
        Dn[n] = Dn[n].replace('G0-SBX = APROBADA CON RESTRICCIONES', 'G0-SBX = NO APROBADA')
        Dn[n] = Dn[n].replace('F35-SBX = HABILITADA', 'F35-SBX = BLOQUEADA')
    rn = run_doc_rules(Dn, dict(computed, **{'SBX-12': False}))
    bad = {k: v[:1] for k, v in rn.items() if v and k != 'LNK'}
    add(not bad, f'control: con SBX-12 fallido, «G0-SBX = NO APROBADA» y «F35-SBX = BLOQUEADA» se aceptan {bad}')

    fallas = [m for ok, m in checks if not ok]
    for m in fallas:
        print('FALLA', m)
    g, f = decision_states(D[DEC_])
    print(f'INFO criterios SBX: {sum(computed.values())}/18 cumplen · G0-SBX = {g} · F35-SBX = {f}')
    print(f'INFO G0 real: G0-02={der.get("G0-02")}, G0-03={der.get("G0-03")}, G0-12={der.get("G0-12")}, '
          f'G0-09={der.get("G0-09")}, G0-14={der.get("G0-14")}')
    print(f'validate_f34e: {len(checks) - len(fallas)} comprobaciones correctas, {len(fallas)} fallas')
    sys.exit(1 if fallas else 0)


if __name__ == '__main__':
    main()
