"""F34 — Validación del dataset sintético, su contrato y su gobernanza (solo biblioteca estándar).

Familias de reglas (IDs documentados en F34_Data_Leakage_y_Calidad.md):
  DQ-01..08   calidad estructural: cabeceras, tipos, nulos, restricciones, claves, integridad, linaje, duplicados
  CON-01..12  consistencia de negocio (A-06, fechas, rúbrica, FF-02, evidencia, anotaciones, eventos, versiones,
              RF-10, ventana observacional)
  CTX-01..10  integridad contextual: organización, vacante, sesión, evaluador y criterio coherentes entre tablas
  PII-01..03  privacidad: columnas sensibles, patrones de PII en textos, atributos de grupo separados
  LK-01..11   leakage: contrato RF-29, recálculo exacto de features y etiqueta, checkpoint, particiones,
              madurez de etiquetas (purga), sensibilidad al límite <= / <
  LN-01       hash canónico del contenido de entrada de cada ejecución de análisis
  AL-01       alertas esperadas = recálculo independiente de reglas deterministas
  MF / RP     manifiesto y reproducibilidad     QA  casos intencionales     DOC / GIT  documentos y alcance
Uso: python docs/academico/tools/f34/validate_f34.py
"""
import collections
import copy
import csv
import datetime as dt
import hashlib
import importlib.util
import json
import math
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
DOCS = os.path.join(ROOT, 'docs', 'academico', 'datos-sinteticos')
DS = os.path.join(DOCS, 'dataset')
sys.path.insert(0, HERE)
import generate_synthetic as G  # noqa: E402

SCHEMA = json.load(open(os.path.join(HERE, 'schema.json'), encoding='utf-8'))
RES = {r['name']: r for r in SCHEMA['resources']}
OBS_END = G.OBSERVATION_END
SENSITIVE = {'name', 'names', 'nombre', 'nombres', 'apellido', 'apellidos', 'fullname', 'firstname', 'lastname', 'dni',
             'email', 'correo', 'mail', 'phone', 'telefono', 'address', 'direccion', 'photo', 'foto', 'age', 'edad',
             'birth', 'birthdate', 'nacimiento', 'gender', 'genero', 'sex', 'sexo', 'sexual', 'race', 'raza', 'ethnic',
             'ethnicity', 'etnia', 'nationality', 'nacionalidad', 'marital', 'religion', 'ideology', 'ideologia',
             'health', 'salud', 'disability', 'discapacidad', 'biometric', 'biometrico', 'sindical'}
LATENT = {'_q', 'operational_capacity', 'coordination_friction', 'workload_pressure', 'random_shock', 'period_effect'}
AUXILIARY = {'evidence_sufficiency', 'evaluator_disagreement', 'human_level', 'rubric_points'}
NO_PII_SCAN = {'analysis_run_id', 'input_snapshot_hash', 'synthetic_record_id'}
DOC_FILES = ['README.md', 'F34_Modelo_de_Datos.md', 'F34_Dataset_Card.md', 'F34_Matriz_Features_Labels.md',
             'F34_Gobernanza_Privacidad.md', 'F34_Data_Leakage_y_Calidad.md', 'F34_Preparacion_F35_F36.md']

# Contrato RF-29 (solo lectura): fuente única de columnas prohibidas para la tabla de features.
_spec = importlib.util.spec_from_file_location('rf29_schema', os.path.join(ROOT, 'ml-service', 'src', 'recruitment_ml',
                                                                           'schema.py'))
RF29 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(RF29)


def load(dirpath=DS):
    T = {}
    for name, r in RES.items():
        with open(os.path.join(dirpath, r['path']), encoding='utf-8', newline='') as f:
            rd = csv.DictReader(f)
            T[name] = {'cols': list(rd.fieldnames), 'rows': [dict(x) for x in rd]}
    return T


def tokens(col):
    return [t.lower() for t in re.split(r'[^A-Za-z0-9]+', re.sub(r'(?<=[a-z0-9])(?=[A-Z])', ' ', col)) if t]


def P(s):
    """Instante desde fecha (00:00) o fecha y hora ISO."""
    return dt.datetime.fromisoformat(s if 'T' in s else s + 'T00:00:00')


def days(a, b):
    return math.floor((b - a).total_seconds() / 86400)


def idx(T, n, k):
    return {r[k]: r for r in T[n]['rows']}


def org_of_evaluator(tok):
    return 'ORG-S' + tok.split('-')[1][1:]


# ---------------------------------------------------------------- DQ
def dq01(T):
    return [f'{n}: cabecera {t["cols"]} ≠ contrato' for n, t in T.items()
            if t['cols'] != [x['name'] for x in RES[n]['schema']['fields']]]


def _fields(T):
    for n, t in T.items():
        fmap = {x['name']: x for x in RES[n]['schema']['fields']}
        for i, row in enumerate(t['rows']):
            for c, v in row.items():
                if c in fmap:
                    yield n, i, c, v, fmap[c]


def dq02(T):
    out = []
    for n, i, c, v, f in _fields(T):
        if v == '':
            continue
        ty = f['type']
        ok = (ty == 'string' or (ty == 'integer' and re.fullmatch(r'-?\d+', v))
              or (ty == 'boolean' and v in ('true', 'false'))
              or (ty == 'date' and re.fullmatch(r'\d{4}-\d{2}-\d{2}', v))
              or (ty == 'datetime' and re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', v)))
        if ok and ty in ('date', 'datetime'):
            try:
                P(v)
            except ValueError:
                ok = False
        if not ok:
            out.append(f'{n}[{i}].{c}={v!r} no es {ty}')
    return out


def dq03(T):
    return [f'{n}[{i}].{c} obligatorio vacío' for n, i, c, v, f in _fields(T) if v == '' and f['constraints']['required']]


def dq04(T):
    out = []
    for n, i, c, v, f in _fields(T):
        if v == '':
            continue
        k = f['constraints']
        if 'enum' in k and v not in k['enum']:
            out.append(f'{n}[{i}].{c}={v!r} fuera de enum')
        if 'pattern' in k and not re.search(k['pattern'], v):
            out.append(f'{n}[{i}].{c}={v!r} no cumple patrón')
        if f['type'] == 'integer' and re.fullmatch(r'-?\d+', v):
            if 'minimum' in k and int(v) < k['minimum'] or 'maximum' in k and int(v) > k['maximum']:
                out.append(f'{n}[{i}].{c}={v} fuera de rango')
    return out


def dq05(T):
    out = []
    for n, t in T.items():
        pk = RES[n]['schema']['primaryKey']
        dup = [k for k, c in collections.Counter(r.get(pk) for r in t['rows']).items() if c > 1]
        out += [f'{n}: clave primaria duplicada {d}' for d in dup[:5]]
    return out


def dq06(T):
    out = []
    for n, t in T.items():
        for fk in RES[n]['schema']['foreignKeys']:
            ref = fk['reference']
            keys = {r[ref['fields']] for r in T[ref['resource']]['rows']}
            bad = [r[fk['fields']] for r in t['rows'] if r.get(fk['fields'], '') not in ('', None)
                   and r[fk['fields']] not in keys]
            out += [f'{n}.{fk["fields"]}={b} sin referencia en {ref["resource"]}' for b in bad[:5]]
    return out


def dq07(T):
    ids = [r['synthetic_record_id'] for t in T.values() for r in t['rows']]
    out = [f'synthetic_record_id duplicado {k}' for k, c in collections.Counter(ids).items() if c > 1][:5]
    out += [f'{n}: source_type ≠ synthetic' for n, t in T.items() if any(r['source_type'] != 'synthetic' for r in t['rows'])]
    return out


SURROGATE = {'evidence', 'process_events', 'annotations', 'analysis_run_events', 'expected_alerts', 'requirement_checks',
             'rubric_levels', 'requirements', 'criteria', 'assessments', 'sessions', 'applications'}


def dq08(T):
    """Duplicados con otra clave sustituta: misma fila de contenido con distinto ID secuencial."""
    out = []
    for n, t in T.items():
        if n not in SURROGATE:
            continue
        pk = RES[n]['schema']['primaryKey']
        keyf = lambda r: tuple((c, v) for c, v in r.items() if c not in (pk, 'synthetic_record_id', 'source_type'))
        dup = [k for k, c in collections.Counter(keyf(r) for r in t['rows']).items() if c > 1]
        out += [f'{n}: fila duplicada (sin contar IDs)' for _ in dup[:3]]
    return out


# ---------------------------------------------------------------- CON
def con01(T):
    s = collections.defaultdict(int)
    for r in T['criteria']['rows']:
        s[r['vacancy_token']] += int(r['weight'])
    return [f'{v}: pesos suman {w} (A-06)' for v, w in s.items() if w != 100]


def con02(T):
    out = []
    vac = idx(T, 'vacancies', 'vacancy_token')
    for v in vac.values():
        cp = P(v['closes_at']) + dt.timedelta(days=1)
        if not (P(v['published_at']) < cp <= P(v['target_completion_at'])):
            out.append(f'{v["vacancy_token"]}: orden de fechas inválido')
    for a in T['applications']['rows']:
        v = vac[a['vacancy_token']]
        if not P(v['published_at']) <= P(a['submitted_at']) < P(v['closes_at']) + dt.timedelta(days=1):
            out.append(f'{a["application_token"]}: postulación fuera de la ventana')
    for s in T['sessions']['rows']:
        if P(s['created_at']) > P(s['scheduled_for']):
            out.append(f'{s["session_token"]}: programada después de su fecha')
        if (s['status'] == 'realizada') != (s['completed_at'] != ''):
            out.append(f'{s["session_token"]}: estado y completed_at incoherentes')
        if s['completed_at'] and P(s['completed_at']) < P(s['scheduled_for']):
            out.append(f'{s["session_token"]}: realizada antes de lo programado')
    return out


def con03(T):
    pts = {(r['criterion_id'], r['level']): r['rubric_points'] for r in T['rubric_levels']['rows']}
    return [f'{a["assessment_id"]}: puntaje {a["rubric_points"]} ≠ rúbrica' for a in T['assessments']['rows']
            if pts.get((a['criterion_id'], a['human_level'])) != a['rubric_points']]


def con04(T):
    """FF-02: PROGRAMADA → registro único por sesión y criterio → REALIZADA (AssessmentResultRecorder)."""
    out = []
    ses = idx(T, 'sessions', 'session_token')
    crit = collections.defaultdict(set)
    for c in T['criteria']['rows']:
        crit[(c['vacancy_token'], c['stage'])].add(c['criterion_id'])
    got = collections.defaultdict(list)
    for a in T['assessments']['rows']:
        s = ses.get(a['session_token'])
        if not s:
            continue
        if s['status'] != 'realizada':
            out.append(f'{a["assessment_id"]}: valoración sobre sesión {s["status"]}')
        if a['recorded_at'] != s['completed_at'] or a['evaluator_token'] != s['evaluator_token']:
            out.append(f'{a["assessment_id"]}: fecha o evaluador distinto de la sesión')
        got[a['session_token']].append(a['criterion_id'])
    for st, cs in got.items():
        if len(cs) != len(set(cs)):
            out.append(f'{st}: más de un resultado para un criterio (sin segundo resultado)')
    for s in ses.values():
        if s['status'] == 'realizada' and set(got.get(s['session_token'], [])) != crit[(s['vacancy_token'], s['stage'])]:
            out.append(f'{s["session_token"]}: resultado incompleto para los criterios de la etapa')
    return out


def con05(T):
    out = []
    asm, ses = idx(T, 'assessments', 'assessment_id'), idx(T, 'sessions', 'session_token')
    for e in T['evidence']['rows']:
        if e['state'] == 'vinculada':
            a = asm.get(e['assessment_id'])
            if not a or a['session_token'] != e['session_token'] or a['criterion_id'] != e['criterion_id']:
                out.append(f'{e["evidence_id"]}: vinculada a una valoración incoherente')
        elif e['assessment_id'] or ses[e['session_token']]['status'] != 'programada':
            out.append(f'{e["evidence_id"]}: borrador fuera de una sesión programada')
    return out


def con06(T):
    n = collections.Counter(e['assessment_id'] for e in T['evidence']['rows'] if e['state'] == 'vinculada')
    return [f'{a["assessment_id"]}: sin evidencia y suficiencia {a["evidence_sufficiency"]}'
            for a in T['assessments']['rows'] if n[a['assessment_id']] == 0 and a['evidence_sufficiency'] != 'insuficiente']


def con07(T):
    asm = idx(T, 'assessments', 'assessment_id')
    return [f'{x["annotation_id"]}: anterior o igual al resultado' for x in T['annotations']['rows']
            if x['assessment_id'] in asm and P(x['created_at']) <= P(asm[x['assessment_id']]['recorded_at'])]


def con08(T):
    out = []
    by = collections.defaultdict(list)
    for e in T['analysis_run_events']['rows']:
        by[e['analysis_run_id']].append(e)
    for rid in {r['analysis_run_id'] for r in T['analysis_runs']['rows']}:
        ev = sorted(by.get(rid, []), key=lambda e: int(e['seq']))
        seqs = [int(e['seq']) for e in ev]
        if seqs != list(range(1, len(ev) + 1)):
            out.append(f'{rid}: secuencia de eventos no es 1..n (historial sobrescrito)')
        st = [e['state'] for e in ev]
        if not st or st[0] != 'pendiente' or st[-1] not in ('completado', 'fallido', 'expirado', 'invalidado'):
            out.append(f'{rid}: estados de eventos inválidos {st}')
    return out


def con09(T):
    out = []
    st = collections.defaultdict(set)
    for c in T['criteria']['rows']:
        st[c['vacancy_token']].add(c['stage'])
    out += [f'{v}: no tiene criterios de ambas etapas' for v, s in st.items() if s != {'evaluacion', 'entrevista'}]
    lv = collections.defaultdict(set)
    for r in T['rubric_levels']['rows']:
        lv[r['criterion_id']].add(r['level'])
    out += [f'{c}: rúbrica sin 4 niveles' for c, s in lv.items() if s != {'1', '2', '3', '4'}]
    return out


def con10(T):
    out = []
    vac = idx(T, 'vacancies', 'vacancy_token')
    ses = idx(T, 'sessions', 'session_token')
    for a in T['assessments']['rows']:
        v = vac[ses[a['session_token']]['vacancy_token']] if a['session_token'] in ses else None
        if v and (a['rubric_version'] != v['rubric_version'] or a['criteria_version'] != v['criteria_version']):
            out.append(f'{a["assessment_id"]}: versión distinta de la congelada (E-06)')
    out += [f'{c["criterion_id"]}: criteria_version distinta' for c in T['criteria']['rows']
            if c['criteria_version'] != vac[c['vacancy_token']]['criteria_version']]
    return out


def con11(T):
    c = collections.Counter((a['vacancy_token'], a['person_token']) for a in T['applications']['rows'])
    return [f'{v}/{p}: más de una postulación de la misma persona (RF-10)' for (v, p), n in c.items() if n > 1]


def con12(T):
    """Ventana observacional: ningún instante posterior a OBSERVATION_END existe en el dataset."""
    out = []
    for n, i, c, v, f in _fields(T):
        if f['type'] == 'datetime' and v and c not in ('target_completion_at', 'scheduled_for') and P(v) > OBS_END:
            out.append(f'{n}[{i}].{c}={v} posterior al fin de la observación')
    return out


# ---------------------------------------------------------------- CTX (integridad contextual)
def ctx01(T):
    vac = idx(T, 'vacancies', 'vacancy_token')
    return [f'{a["application_token"]}: organización {a["organization_token"]} ≠ la de su vacante'
            for a in T['applications']['rows'] if a['organization_token'] != vac[a['vacancy_token']]['organization_token']]


def ctx02(T):
    app, req = idx(T, 'applications', 'application_token'), idx(T, 'requirements', 'requirement_id')
    return [f'{c["check_id"]}: requisito de otra vacante' for c in T['requirement_checks']['rows']
            if c['requirement_id'] in req and c['application_token'] in app
            and req[c['requirement_id']]['vacancy_token'] != app[c['application_token']]['vacancy_token']]


def ctx03(T):
    vac, comp = idx(T, 'vacancies', 'vacancy_token'), idx(T, 'competencies', 'competency_id')
    crit = idx(T, 'criteria', 'criterion_id')
    out = [f'{c["criterion_id"]}: competencia de otra organización' for c in T['criteria']['rows']
           if c['competency_id'] in comp
           and comp[c['competency_id']]['organization_token'] != vac[c['vacancy_token']]['organization_token']]
    out += [f'{r["rubric_level_id"]}: rúbrica de otra vacante o versión' for r in T['rubric_levels']['rows']
            if r['criterion_id'] in crit and r['rubric_version'] != vac[crit[r['criterion_id']]['vacancy_token']]['rubric_version']]
    return out


def ctx04(T):
    vac, app = idx(T, 'vacancies', 'vacancy_token'), idx(T, 'applications', 'application_token')
    out = []
    for s in T['sessions']['rows']:
        a = app.get(s['application_token'])
        if a and a['vacancy_token'] != s['vacancy_token']:
            out.append(f'{s["session_token"]}: vacante distinta de la de su postulación')
        if org_of_evaluator(s['evaluator_token']) != vac[s['vacancy_token']]['organization_token']:
            out.append(f'{s["session_token"]}: evaluador de otra organización (cross-tenant)')
    return out


def ctx05(T):
    ses, crit = idx(T, 'sessions', 'session_token'), idx(T, 'criteria', 'criterion_id')
    out = []
    for a in T['assessments']['rows']:
        s, c = ses.get(a['session_token']), crit.get(a['criterion_id'])
        if not s or not c:
            continue
        if a['application_token'] != s['application_token']:
            out.append(f'{a["assessment_id"]}: postulación distinta de la de su sesión')
        if c['vacancy_token'] != s['vacancy_token'] or c['stage'] != s['stage']:
            out.append(f'{a["assessment_id"]}: criterio de otra vacante o etapa')
    return out


def ctx06(T):
    ses, crit = idx(T, 'sessions', 'session_token'), idx(T, 'criteria', 'criterion_id')
    out = []
    for e in T['evidence']['rows']:
        s, c = ses.get(e['session_token']), crit.get(e['criterion_id'])
        if not s or not c:
            continue
        if e['application_token'] != s['application_token'] or e['registered_by'] != s['evaluator_token']:
            out.append(f'{e["evidence_id"]}: postulación o autor distinto de su sesión')
        if c['vacancy_token'] != s['vacancy_token']:
            out.append(f'{e["evidence_id"]}: criterio de otra vacante')
    return out


def ctx07(T):
    asm, ses, vac = idx(T, 'assessments', 'assessment_id'), idx(T, 'sessions', 'session_token'), idx(T, 'vacancies', 'vacancy_token')
    out = []
    for x in T['annotations']['rows']:
        a = asm.get(x['assessment_id'])
        if a and a['session_token'] in ses:
            org = vac[ses[a['session_token']]['vacancy_token']]['organization_token']
            if org_of_evaluator(x['author_token']) != org:
                out.append(f'{x["annotation_id"]}: autor de otra organización')
    return out


def ctx08(T):
    vac, app, ses = idx(T, 'vacancies', 'vacancy_token'), idx(T, 'applications', 'application_token'), idx(T, 'sessions', 'session_token')
    out = []
    for e in T['process_events']['rows']:
        if e['organization_token'] != vac[e['vacancy_token']]['organization_token']:
            out.append(f'{e["event_id"]}: organización distinta de la de su vacante')
        ref = e['ref_token'].split('>')[0]
        owner = (app.get(ref) or ses.get(ref) or {}).get('vacancy_token') if ref else e['vacancy_token']
        if owner != e['vacancy_token']:
            out.append(f'{e["event_id"]}: referencia de otra vacante')
    return out


def ctx09(T):
    vac = idx(T, 'vacancies', 'vacancy_token')
    out = [f'snapshot {r["vacancy_token"]}: organización distinta' for r in T['process_snapshots']['rows']
           if r['organization_token'] != vac[r['vacancy_token']]['organization_token']]
    for r in T['analysis_runs']['rows']:
        v = vac[r['vacancy_token']]
        if (r['organization_token'], r['criteria_version'], r['rubric_version']) != (
                v['organization_token'], v['criteria_version'], v['rubric_version']):
            out.append(f'{r["analysis_run_id"]}: organización o versiones distintas de su vacante')
    return out


def ctx10(T):
    app, crit = idx(T, 'applications', 'application_token'), idx(T, 'criteria', 'criterion_id')
    out = []
    for r in T['expected_alerts']['rows']:
        if r['application_token'] and app.get(r['application_token'], {}).get('vacancy_token') != r['vacancy_token']:
            out.append(f'{r["alert_id"]}: postulación de otra vacante')
        if r['criterion_id'] and crit.get(r['criterion_id'], {}).get('vacancy_token') != r['vacancy_token']:
            out.append(f'{r["alert_id"]}: criterio de otra vacante')
    persons = {a['person_token'] for a in T['applications']['rows']}
    out += [f'grupo sintético de persona inexistente {r["person_token"]}'
            for r in T[G.FAIRNESS_TABLE[0]]['rows'] if r['person_token'] not in persons]
    return out


# ---------------------------------------------------------------- PII
def pii01(T):
    return [f'{n}.{c}: columna de identidad o atributo sensible' for n, t in T.items() for c in t['cols']
            if set(tokens(c)) & SENSITIVE]


PII_RE = [(re.compile(r'[\w.+-]+@[\w-]+\.[\w.]+'), 'correo'), (re.compile(r'https?://|www\.'), 'URL'),
          (re.compile(r'(?<![\w-])\d{8}(?![\w-])'), 'DNI'), (re.compile(r'(?<![\w-])\+?\d[\d ]{8,}\d(?![\w-])'), 'teléfono')]


def pii02(T):
    out = []
    for n, t in T.items():
        for i, r in enumerate(t['rows']):
            for c, v in r.items():
                if c in NO_PII_SCAN or not v:
                    continue
                for rx, what in PII_RE:
                    if rx.search(v):
                        out.append(f'{n}[{i}].{c}: patrón de {what}')
    return out


def pii03(T):
    fair = G.FAIRNESS_TABLE[0]
    out = [f'{n}: contiene grupo_sintetico fuera del archivo separado' for n, t in T.items()
           if n != fair and 'grupo_sintetico' in t['cols']]
    if T[fair]['cols'] != G.FAIRNESS_TABLE[1]:
        out.append('archivo de equidad sintética con columnas no previstas')
    return out


# ---------------------------------------------------------------- LK (semántica RF-29)
def lk01(T):
    allowed = {x['name'] for x in RES['process_snapshots']['schema']['fields']}
    return [f'process_snapshots.{c}: columna prohibida por el contrato RF-29 o fuera del contrato'
            for c in T['process_snapshots']['cols']
            if c not in allowed or (RF29.is_forbidden_column(c) and c not in ('vacancy_token', 'organization_token'))]


def recompute(T, inclusive=True):
    """Implementación independiente de OperationalRiskFeatureBuilder (Laravel) sobre las tablas exportadas.

    inclusive=True aplica la regla del contrato (t <= checkpoint); False reproduce el error `<` para la prueba
    de sensibilidad (LK-11)."""
    le = (lambda t, at: t <= at) if inclusive else (lambda t, at: t < at)
    vac = idx(T, 'vacancies', 'vacancy_token')
    apps = collections.defaultdict(list)
    for a in T['applications']['rows']:
        apps[a['vacancy_token']].append(a)
    sess = collections.defaultdict(list)
    for s in T['sessions']['rows']:
        sess[s['application_token']].append(s)
    hist = collections.defaultdict(list)
    closed = {}
    for e in T['process_events']['rows']:
        if e['event_type'] == 'cambio_etapa':
            hist[e['ref_token'].split('>')[0]].append(P(e['event_at']))
        if e['event_type'] == 'vacante_cerrada':
            closed[e['vacancy_token']] = P(e['event_at'])
    ncrit = collections.Counter(c['vacancy_token'] for c in T['criteria']['rows'])
    out = {}
    for vt, v in vac.items():
        at = P(v['closes_at']) + dt.timedelta(days=1)
        pub = P(v['published_at'])
        ids = [a for a in apps[vt] if le(P(a['submitted_at']), at)]
        ss = [s for a in ids for s in sess[a['application_token']]]

        def by_stage(stage):
            return [s for s in ss if s['stage'] == stage]

        def scheduled(stage):
            return sum(1 for s in by_stage(stage) if le(P(s['created_at']), at))

        def completed(stage):
            return sum(1 for s in by_stage(stage) if s['completed_at'] and le(P(s['completed_at']), at))

        def overdue(stage):
            return sum(1 for s in by_stage(stage) if le(P(s['created_at']), at) and P(s['scheduled_for']) < at
                       and (not s['completed_at'] or not le(P(s['completed_at']), at)))
        cand = [pub] if le(pub, at) else []
        cand += [P(a['submitted_at']) for a in apps[vt] if le(P(a['submitted_at']), at)]
        cand += [P(s[k]) for s in ss for k in ('created_at', 'completed_at') if s[k] and le(P(s[k]), at)]
        cand += [t for a in ids for t in hist[a['application_token']] if le(t, at)]
        others = sum(1 for x in vac.values() if x['organization_token'] == v['organization_token'] and x is not v
                     and le(P(x['published_at']), at)
                     and (x['vacancy_token'] not in closed or closed[x['vacancy_token']] > at))
        known = closed.get(vt)
        out[vt] = {
            'checkpoint_at': at.isoformat(timespec='seconds'),
            'elapsed_days_since_publication': max(0, days(pub, at)),
            'application_window_days': max(0, days(dt.datetime.combine(pub.date(), dt.time()), P(v['closes_at']))),
            'positions_count': int(v['positions_count']), 'applications_received_count': len(ids),
            'configured_criteria_count': ncrit[vt],
            'evaluations_scheduled_count': scheduled('evaluacion'), 'evaluations_completed_count': completed('evaluacion'),
            'evaluations_overdue_pending_count': overdue('evaluacion'),
            'interviews_scheduled_count': scheduled('entrevista'), 'interviews_completed_count': completed('entrevista'),
            'interviews_overdue_pending_count': overdue('entrevista'),
            'stage_transition_count': sum(1 for a in ids for t in hist[a['application_token']] if le(t, at)),
            'days_since_last_operational_event': max(0, days(max(cand), at)) if cand else 0,
            'concurrent_open_vacancies_count': others,
            'days_remaining_to_target': days(at, P(v['target_completion_at'])),
            'delayed': '' if known is None else str(int(known > P(v['target_completion_at']))),
            'observation_status': 'censored' if known is None else 'completed',
            'label_known_at': '' if known is None else known.isoformat(timespec='seconds'),
        }
    return out


def lk02(T):
    rc = recompute(T)
    out = []
    for r in T['process_snapshots']['rows']:
        for f in G.PROCESS_FEATURES:
            if f in r and r[f] != '' and int(r[f]) != rc[r['vacancy_token']][f]:
                out.append(f'{r["vacancy_token"]}.{f}: {r[f]} ≠ recálculo RF-29 ({rc[r["vacancy_token"]][f]})')
    return out


def lk03(T):
    rc = recompute(T)
    return [f'{r["vacancy_token"]}: checkpoint ≠ inicio del día siguiente a closes_at (ADR-004)'
            for r in T['process_snapshots']['rows'] if r['checkpoint_at'] != rc[r['vacancy_token']]['checkpoint_at']]


def lk04(T):
    rc = recompute(T)
    return [f'{r["vacancy_token"]}: etiqueta o estado de observación incoherente con el cierre observado'
            for r in T['process_snapshots']['rows']
            if (r['delayed'], r['observation_status']) != (rc[r['vacancy_token']]['delayed'],
                                                           rc[r['vacancy_token']]['observation_status'])]


def lk05(T):
    m = json.load(open(os.path.join(DS, 'manifest.json'), encoding='utf-8'))
    feats = [x['name'] for x in RES['process_snapshots']['schema']['fields'] if x['role'] == 'feature_process']
    return [] if m['feature_set']['process_features'] == feats == G.PROCESS_FEATURES else ['feature_set ≠ contrato']


def lk06(T):
    out = []
    snaps = {r['vacancy_token']: r for r in T['process_snapshots']['rows']}
    c = collections.Counter(r['vacancy_token'] for r in T['process_splits']['rows'])
    out += [f'{v}: aparece en {n} particiones' for v, n in c.items() if n != 1]
    out += [f'{v}: sin partición' for v in snaps if v not in c]
    for r in T['process_splits']['rows']:
        s = snaps.get(r['vacancy_token'])
        if s and (s['observation_status'] == 'censored') != (r['split'] == 'censurado'):
            out.append(f'{r["vacancy_token"]}: censurada fuera de «censurado» o etiquetada dentro')
    by = collections.defaultdict(list)
    for r in T['process_splits']['rows']:
        by[r['split']].append(P(r['checkpoint_at']))
    for a, b in (('train', 'validation'), ('validation', 'test')):
        if by[a] and by[b] and max(by[a]) > min(by[b]):
            out.append(f'{b} contiene checkpoints anteriores a {a} (leakage temporal)')
    return out


def lk07(T):
    m = json.load(open(os.path.join(DS, 'manifest.json'), encoding='utf-8'))
    out = [] if 'grupo_sintetico' not in m['feature_set']['process_features'] else ['grupo_sintetico en el feature set']
    out += [f'process_snapshots.{c}: atributo de grupo en features' for c in T['process_snapshots']['cols']
            if c == 'grupo_sintetico']
    return out


def lk08(T):
    """Datos humanos y auxiliares (suficiencia, discrepancia, nivel) nunca en la tabla de features."""
    roles = {'identifier', 'lineage', 'feature_process', 'label_process'}
    fmap = {x['name']: x['role'] for x in RES['process_snapshots']['schema']['fields']}
    bad = AUXILIARY | {'person_token', 'evaluator_token', 'justification', 'evidence_text', 'label_known_at'}
    m = json.load(open(os.path.join(DS, 'manifest.json'), encoding='utf-8'))
    out = [f'process_snapshots.{c}: dato humano, auxiliar o posterior en la tabla de proceso'
           for c in T['process_snapshots']['cols'] if c in bad or fmap.get(c) not in roles]
    out += [f'feature_set incluye {c}' for c in m['feature_set']['process_features'] if c in bad]
    return out


def lk09(T):
    return [f'{n}.{c}: factor latente del generador exportado' for n, t in T.items() for c in t['cols'] if c in LATENT]


def lk10(T):
    """Madurez de la etiqueta: ninguna etiqueta de una partición depende de hechos posteriores al inicio de la
    siguiente. La purga debe ser exacta: ni filas inmaduras dentro ni filas maduras purgadas."""
    out = []
    rc = recompute(T)
    rows = T['process_splits']['rows']
    for r in rows:
        if r['label_known_at'] != rc[r['vacancy_token']]['label_known_at']:
            out.append(f'{r["vacancy_token"]}: label_known_at ≠ cierre observado')
    start = {s: min((P(r['checkpoint_at']) for r in rows if r['split'] == s), default=None)
             for s in ('validation', 'test')}
    nxt = {'train': 'validation', 'validation': 'test'}
    for r in rows:
        if r['split'] in ('train', 'validation', 'test') and not r['label_known_at']:
            out.append(f'{r["vacancy_token"]}: fila etiquetada en {r["split"]} sin etiqueta observada')
        if r['split'] in nxt and start[nxt[r['split']]] and r['label_known_at'] \
                and P(r['label_known_at']) >= start[nxt[r['split']]]:
            out.append(f'{r["vacancy_token"]}: etiqueta de {r["split"]} no madura antes de {nxt[r["split"]]}')
        if r['split'] == 'test' and r['label_known_at'] and P(r['label_known_at']) > OBS_END:
            out.append(f'{r["vacancy_token"]}: etiqueta de test no observada')
        if r['split'] == 'purgado':
            orig = r['split_reason'].replace('etiqueta_no_madura_antes_de_', '')
            if orig not in start or not start[orig] or P(r['label_known_at']) < start[orig]:
                out.append(f'{r["vacancy_token"]}: purgada sin motivo (sobrepurga)')
    for s in ('train', 'validation', 'test'):
        if not any(r['split'] == s for r in rows):
            out.append(f'partición {s} vacía')
    return out


def lk11(T):
    """El dataset contiene empates en el checkpoint y el recálculo con `<` difiere: volver a `<` se detecta."""
    rc_le, rc_lt = recompute(T, True), recompute(T, False)
    diffs = [v for v in rc_le if any(rc_le[v][f] != rc_lt[v][f] for f in G.PROCESS_FEATURES)]
    cps = {r['vacancy_token']: r['checkpoint_at'] for r in T['process_snapshots']['rows']}
    ties = sum(1 for e in T['process_events']['rows'] if e['event_at'] == cps.get(e['vacancy_token']))
    # Límite de las vencidas (scheduled_for < checkpoint): sesiones programadas exactamente en el checkpoint.
    due = sum(1 for s in T['sessions']['rows'] if s['scheduled_for'] == cps.get(s['vacancy_token'])
              and P(s['created_at']) <= P(s['scheduled_for']))
    return [] if diffs and ties and due else [f'sin empates en el checkpoint (eventos {ties}, programadas {due}, '
                                              f'vacantes sensibles {len(diffs)})']


# ---------------------------------------------------------------- LN (hash canónico)
def canonical_hash(vac, asms, evid):
    """Algoritmo f34-input-sha256-v1 documentado, reimplementado aquí de forma independiente."""
    payload = {'algorithm': 'f34-input-sha256-v1', 'vacancy_token': vac['vacancy_token'],
               'criteria_version': vac['criteria_version'], 'rubric_version': vac['rubric_version'],
               'rules_version': G.RULES_VERSION,
               'assessments': [{k: a[k] for k in ('assessment_id', 'session_token', 'criterion_id', 'human_level',
                                                   'rubric_points', 'evidence_sufficiency', 'justification')}
                               for a in sorted(asms, key=lambda x: x['assessment_id'])],
               'evidence': [{k: e[k] for k in ('evidence_id', 'assessment_id', 'criterion_id', 'source_type_ev',
                                                'source_reference', 'evidence_text')}
                            for e in sorted(evid, key=lambda x: x['evidence_id'])]}
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode('utf-8')).hexdigest()


def ln01(T):
    vac = idx(T, 'vacancies', 'vacancy_token')
    app_v = {a['application_token']: a['vacancy_token'] for a in T['applications']['rows']}
    asms = collections.defaultdict(list)
    for a in T['assessments']['rows']:
        asms[app_v.get(a['application_token'])].append(a)
    ev = collections.defaultdict(list)
    for e in T['evidence']['rows']:
        if e['state'] == 'vinculada':
            ev[app_v.get(e['application_token'])].append(e)
    out = []
    for r in T['analysis_runs']['rows']:
        vt = r['vacancy_token']
        if r['input_hash_algorithm'] != 'f34-input-sha256-v1' or \
                r['input_snapshot_hash'] != canonical_hash(vac[vt], asms[vt], ev[vt]):
            out.append(f'{r["analysis_run_id"]}: input_snapshot_hash no corresponde al contenido canónico')
    return out


# ---------------------------------------------------------------- AL
def al01(T):
    app = idx(T, 'applications', 'application_token')
    got = collections.Counter()
    for ck in T['requirement_checks']['rows']:
        if ck['declared_met'] != 'true' or ck['evidence_present'] != 'true':
            got[('requisito_no_evidenciado', app[ck['application_token']]['vacancy_token'], ck['application_token'], '',
                 ck['check_id'])] += 1
    nev = collections.Counter(e['assessment_id'] for e in T['evidence']['rows'] if e['state'] == 'vinculada')
    for a in T['assessments']['rows']:
        if nev[a['assessment_id']] == 0:
            got[('evidencia_faltante', app[a['application_token']]['vacancy_token'], a['application_token'],
                 a['criterion_id'], a['assessment_id'])] += 1
    for s in T['sessions']['rows']:
        if s['status'] == 'programada' and P(s['scheduled_for']) < OBS_END:
            got[('sesion_vencida', s['vacancy_token'], s['application_token'], '', s['session_token'])] += 1
    grp = collections.defaultdict(list)
    for a in sorted(T['assessments']['rows'], key=lambda a: a['session_token']):
        grp[(a['application_token'], a['criterion_id'])].append(a)
    for (ap, cr), lst in grp.items():
        for later in lst[1:]:
            if abs(int(later['human_level']) - int(lst[0]['human_level'])) >= 2:
                got[('discrepancia_evaluadores', app[ap]['vacancy_token'], ap, cr, later['session_token'])] += 1
    exp = collections.Counter((r['alert_type'], r['vacancy_token'], r['application_token'], r['criterion_id'], r['ref_id'])
                              for r in T['expected_alerts']['rows'])
    diff = (got - exp) + (exp - got)
    return [f'alerta distinta del recálculo: {k}' for k in list(diff)[:5]]


RULES = [('DQ-01', dq01), ('DQ-02', dq02), ('DQ-03', dq03), ('DQ-04', dq04), ('DQ-05', dq05), ('DQ-06', dq06),
         ('DQ-07', dq07), ('DQ-08', dq08), ('CON-01', con01), ('CON-02', con02), ('CON-03', con03), ('CON-04', con04),
         ('CON-05', con05), ('CON-06', con06), ('CON-07', con07), ('CON-08', con08), ('CON-09', con09),
         ('CON-10', con10), ('CON-11', con11), ('CON-12', con12), ('CTX-01', ctx01), ('CTX-02', ctx02),
         ('CTX-03', ctx03), ('CTX-04', ctx04), ('CTX-05', ctx05), ('CTX-06', ctx06), ('CTX-07', ctx07),
         ('CTX-08', ctx08), ('CTX-09', ctx09), ('CTX-10', ctx10), ('PII-01', pii01), ('PII-02', pii02),
         ('PII-03', pii03), ('LK-01', lk01), ('LK-02', lk02), ('LK-03', lk03), ('LK-04', lk04), ('LK-05', lk05),
         ('LK-06', lk06), ('LK-07', lk07), ('LK-08', lk08), ('LK-09', lk09), ('LK-10', lk10), ('LK-11', lk11),
         ('LN-01', ln01), ('AL-01', al01)]


def run_rules(T):
    res = {}
    for rid, fn in RULES:
        try:
            res[rid] = fn(T)
        except (KeyError, ValueError, TypeError, AttributeError, IndexError) as e:
            res[rid] = [f'error estructural: {type(e).__name__}: {e}']   # una mutación rompió la estructura
    return res


# ---------------------------------------------------------------- QA (inconsistencias intencionales)
def apply_case(T, c):
    T = copy.deepcopy(T)
    t = T[c['table']]
    op = c['op']
    if op == 'set':
        t['rows'][c['row']][c['column']] = c['value']
    elif op == 'add_int':
        r = t['rows'][c['row']]
        r[c['column']] = str(int(r[c['column']]) + c['value'])
    elif op == 'dup_row':
        r = dict(t['rows'][c['row']])
        r.update(c.get('override', {}))
        t['rows'].append(r)
    elif op == 'drop_row':
        del t['rows'][c['row']]
    elif op == 'add_column':
        t['cols'].append(c['column'])
        for r in t['rows']:
            r[c['column']] = c['value']
    elif op == 'swap_points':
        r = t['rows'][c['row']]
        r['rubric_points'] = '5' if r['rubric_points'] != '5' else '20'
    elif op == 'set_match':
        r = next(x for x in t['rows'] if all(x[k] == v for k, v in c['match'].items()))
        r[c['column']] = c['value']
    elif op == 'set_match_from':
        src, sel, col = c['from']
        rows = T[src]['rows']
        srow = rows[sel] if isinstance(sel, int) else next(x for x in rows if all(x[k] == v for k, v in sel.items()))
        r = next(x for x in t['rows'] if x[c['key']] == srow[col])
        r[c['column']] = c['value']
    elif op == 'other_vacancy':
        # Toma el valor de `column` de una fila de `from_table` que pertenezca a OTRA vacante que la fila mutada.
        r = next(x for x in t['rows'] if all(x[k] == v for k, v in c['match'].items()))
        app = idx(T, 'applications', 'application_token')
        mine = app[r['application_token']]['vacancy_token'] if r.get('application_token') else r['vacancy_token']
        other = next(x for x in T[c['from_table']]['rows'] if x['vacancy_token'] != mine)
        r[c['column']] = other[c['from_column']]
    elif op == 'strict_features':
        # Simula volver a `< checkpoint`: el snapshot se recalcula con inclusión estricta.
        rc = recompute(T, inclusive=False)
        for r in t['rows']:
            for f in G.PROCESS_FEATURES:
                r[f] = str(rc[r['vacancy_token']][f])
    else:
        raise ValueError(op)
    return T


# ---------------------------------------------------------------- manifiesto y reproducibilidad
def sha(p):
    with open(p, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def manifest_checks():
    out = []
    m = json.load(open(os.path.join(DS, 'manifest.json'), encoding='utf-8'))
    for name, info in m['files'].items():
        p = os.path.join(DS, name)
        with open(p, encoding='utf-8') as f:
            rows = sum(1 for _ in f) - 1
        if sha(p) != info['sha256'] or rows != info['rows']:
            out.append(f'manifiesto ≠ archivo: {name}')
    for k in ('dataset_version', 'generator_version', 'schema_version', 'feature_set_version', 'seed', 'generated_at',
              'observation_end', 'temporal_semantics', 'input_hash_algorithm', 'rubric_versions', 'criteria_versions'):
        if not m.get(k):
            out.append(f'manifiesto sin {k}')
    if m.get('source') != 'synthetic' or 'NO representa datos reales del Colegio Andino' not in m.get('note', ''):
        out.append('manifiesto sin source=synthetic o sin la advertencia')
    if m.get('schema_version') != SCHEMA['schema_version']:
        out.append('schema_version del manifiesto ≠ schema.json')
    excl = ' '.join(m['feature_set']['excluded_from_features'])
    if not all(x in excl for x in ('evidence_sufficiency', 'evaluator_disagreement')):
        out.append('el manifiesto no excluye las features auxiliares')
    return out, m


def reproducibility(m):
    out = []
    with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b, tempfile.TemporaryDirectory() as c:
        for d_ in (a, b):
            Tg, fair = G.generate(G.SEED)
            G.write(d_, Tg, fair, G.SEED)
        Tg, fair = G.generate(G.SEED + 1)
        G.write(c, Tg, fair, G.SEED + 1)
        for name, info in m['files'].items():
            ha, hb = sha(os.path.join(a, name)), sha(os.path.join(b, name))
            if not (ha == hb == info['sha256']):
                out.append(f'RP-01 {name}: regeneración con la misma semilla no idéntica')
        if sha(os.path.join(a, 'manifest.json')) != sha(os.path.join(DS, 'manifest.json')):
            out.append('RP-01 manifest.json regenerado distinto')
        changed = sum(sha(os.path.join(c, n)) != i['sha256'] for n, i in m['files'].items())
        if changed < len(m['files']) - 2:          # organizations y competencies no dependen de la semilla
            out.append(f'RP-02 otra semilla cambia solo {changed} archivos')
    return out


def psi(a, b, bins=5):
    qs = sorted(a)
    cuts = [qs[int(len(qs) * k / bins)] for k in range(1, bins)]

    def dist(x):
        c = [0] * bins
        for v in x:
            c[sum(v > q for q in cuts)] += 1
        return [(n + 0.5) / (len(x) + 0.5 * bins) for n in c]
    p, q = dist(a), dist(b)
    return sum((pi - qi) * math.log(pi / qi) for pi, qi in zip(p, q))


def slug(h):
    h = re.sub(r'[`*_]', '', h.strip().lower())
    return re.sub(r'[^\w\- ]', '', h).replace(' ', '-')


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    checks = []
    add = lambda ok, msg: checks.append((bool(ok), msg))
    T = load()

    res = run_rules(T)
    for rid, viol in res.items():
        add(not viol, f'{rid}: {len(viol)} violaciones' + (f' — {viol[:2]}' if viol else ''))

    mviol, m = manifest_checks()
    add(not mviol, f'MF-01/02 manifiesto: {mviol}')
    rviol = reproducibility(m)
    add(not rviol, f'RP-01/02 reproducibilidad (dos regeneraciones idénticas, otra semilla distinta): {rviol}')

    cases = json.load(open(os.path.join(DS, 'qa_casos', 'qa_cases.json'), encoding='utf-8'))['cases']
    for c in cases:
        r = run_rules(apply_case(T, c))
        hit = [rid for rid in c['rule'] if r.get(rid)]
        add(hit, f'{c["id"]} detectado por {c["rule"]}: {c["what"]}')
    add(len(cases) >= 30, f'casos QA intencionales: {len(cases)}')

    split = {r['vacancy_token']: r['split'] for r in T['process_splits']['rows']}
    for f in ('elapsed_days_since_publication', 'evaluations_scheduled_count', 'days_remaining_to_target'):
        tr = [int(r[f]) for r in T['process_snapshots']['rows'] if split[r['vacancy_token']] == 'train']
        te = [int(r[f]) for r in T['process_snapshots']['rows'] if split[r['vacancy_token']] == 'test']
        print(f'INFO PSI train→test {f}: {psi(tr, te):.3f}')

    txt = {}
    for n in DOC_FILES:
        p = os.path.join(DOCS, n)
        add(os.path.isfile(p), f'documento presente: {n}')
        txt[n] = open(p, encoding='utf-8').read() if os.path.isfile(p) else ''
    add('NO representa datos reales del Colegio Andino' in txt['F34_Dataset_Card.md'], 'Dataset Card: advertencia explícita')
    rd = txt['F34_Preparacion_F35_F36.md']
    for s in ('F34 = LISTA PARA AUDITORÍA', 'F35–F40 = BLOQUEADAS', 'G0 = NO APROBADA'):
        add(s in rd, f'readiness declara «{s}»')
    todo = '\n'.join(txt.values())
    add('F34 = CERRADA' not in todo, 'ningún documento declara F34 CERRADA antes de la auditoría')
    add(not re.search(r'G0\s*=\s*\**\s*APROBADA', todo), 'ningún documento declara G0 aprobada')
    add('no alimentan ML de personas' in txt['F34_Matriz_Features_Labels.md'],
        'matriz: las features auxiliares no alimentan ML de personas')
    add('El consentimiento **no** autoriza datos reales' in txt['F34_Gobernanza_Privacidad.md'],
        'gobernanza: el consentimiento no autoriza datos reales')
    for s in ('label_known_at', 'purga', '<= checkpoint_at', 'f34-input-sha256-v1'):
        add(s in txt['F34_Data_Leakage_y_Calidad.md'], f'leakage y calidad documenta «{s}»')
    for sec in ('propósito', 'alcance', 'origen', 'proceso de generación', 'variables', 'distribución', 'limitaciones',
                'sesgos simulados', 'usos permitidos', 'usos prohibidos', 'privacidad', 'riesgos', 'versionado',
                'reproducibilidad', 'mantenimiento'):
        add(re.search(r'^## .*' + sec, txt['F34_Dataset_Card.md'], re.M | re.I), f'Dataset Card: sección «{sec}»')
    rotos = []
    for n, t in txt.items():
        for link in re.findall(r'\]\(([^)\s]+)\)', t):
            if link.startswith(('http://', 'https://')):
                continue
            path, _, anchor = link.partition('#')
            target = os.path.normpath(os.path.join(DOCS, path)) if path else os.path.join(DOCS, n)
            if not os.path.exists(target):
                rotos.append(f'{n}→{link}')
            elif anchor and target.endswith('.md'):
                heads = {slug(h) for h in re.findall(r'^#+ (.+)$', open(target, encoding='utf-8').read(), re.M)}
                if anchor not in heads:
                    rotos.append(f'{n}→{link}')
    add(not rotos, f'enlaces y anclas: {rotos}')

    st = subprocess.run(['git', 'status', '--porcelain', '--untracked-files=all'], cwd=ROOT, capture_output=True,
                        text=True, encoding='utf-8').stdout.splitlines()
    rutas = [ln[3:].strip('"') for ln in st]
    # Excepción F35-SBX-A (DH-09): solo CLAUDE.md y docs/PROGRESS.md con exactamente la apertura; si no, falla.
    sys.path.append(os.path.join(ROOT, 'docs', 'academico', 'tools', 'f35sbx'))
    import f35sbx_scope
    add(all(p.startswith('docs/academico/') or f35sbx_scope.governance_ok(p, ROOT) for p in rutas),
        f'cambios solo en docs/academico ({len(rutas)})')
    checks.extend(f35sbx_scope.regressions(ROOT))

    fallas = [m_ for ok, m_ in checks if not ok]
    for m_ in fallas:
        print('FALLA', m_)
    print(f'filas: {sum(len(t["rows"]) for t in T.values())} en {len(T)} tablas · casos QA: {len(cases)}')
    print(f'validate_f34: {len(checks) - len(fallas)} comprobaciones correctas, {len(fallas)} fallas')
    sys.exit(1 if fallas else 0)


if __name__ == '__main__':
    main()
