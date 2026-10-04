"""F34 — Generador del dataset 100 % sintético del módulo inteligente (alcance B + proceso E).

Reglas:
  - Nada se deriva de personas reales: organizaciones, vacantes, postulantes y evaluadores son tokens inventados.
  - Sin nombres, correos, teléfonos, documentos de identidad, direcciones ni atributos sensibles reales.
  - Los textos libres son plantillas marcadas con «[SINTÉTICO]».
  - Sin score de idoneidad ni etiquetas «contratado/seleccionado»: F33 lo bloquea.
  - Determinista: misma semilla → mismos archivos byte a byte (solo biblioteca estándar).

Modelo temporal (alineado con RF-29: feature-contract.md, ADR-004 y OperationalRiskFeatureBuilder.php):
  - Marcas de tiempo con hora (segundos), hora local America/Lima, formato ISO `YYYY-MM-DDTHH:MM:SS` sin desplazamiento.
  - `checkpoint_at` = inicio (00:00:00) del día siguiente a `closes_at` (columna date).
  - Regla universal: un evento se incluye ⟺ t <= checkpoint_at. Única excepción del contrato: «vencida» usa
    `scheduled_at < checkpoint_at`. «Abierta» = published_at <= at y (closed_at nulo o closed_at > at).
  - Días completos = floor(segundos / 86 400).
  - Ventana observacional: nada posterior a OBSERVATION_END existe en el dataset. Una vacante sin cierre a esa fecha
    queda `censored`, sin etiqueta (ADR-004, regla 16).
  - Empates deliberados en el checkpoint (sesiones creadas y vacantes publicadas exactamente a las 00:00:00) para que
    usar `<` en lugar de `<=` produzca diferencias detectables.

El factor latente por postulación (`_q`) solo existe en memoria; NO se exporta y NO representa idoneidad de nadie.

Uso:  python docs/academico/tools/f34/generate_synthetic.py [--seed N] [--out DIR]
"""
import argparse
import csv
import datetime as dt
import hashlib
import json
import math
import os
import random
import sys
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OUT = os.path.abspath(os.path.join(HERE, '..', '..', 'datos-sinteticos', 'dataset'))

SEED = 20261004
GENERATOR_VERSION = 'f34-gen-1.1.0'
SCHEMA_VERSION = 'f34-schema-1.1.0'
DATASET_VERSION = 'f34-synth-1.1.0'
FEATURE_SET_VERSION = 'f34-fs-1.0.0'
RULES_VERSION = 'f33-rules-design-0'
INPUT_HASH_ALGORITHM = 'f34-input-sha256-v1'
GENERATED_AT = '2026-10-04T00:00:00-05:00'                 # fecha lógica fija (reproducibilidad)
OBSERVATION_END = dt.datetime(2026, 9, 30, 23, 59, 59)     # fin de la ventana observacional (America/Lima)
BASE = dt.datetime(2026, 1, 5)
PREFIX = '[SINTÉTICO]'
DAY = 86400

COMPETENCIAS = [
    ('Planificación de la enseñanza', 'docente'), ('Conducción del aprendizaje', 'docente'),
    ('Evaluación formativa', 'docente'), ('Trabajo con familias y comunidad', 'docente'),
    ('Desarrollo profesional', 'ambos'), ('Gestión administrativa', 'administrativo'),
    ('Atención al usuario', 'administrativo'), ('Organización del trabajo', 'ambos'),
]
METODO_EVAL = ['prueba_escrita', 'revision_documental', 'clase_demostrativa']
REQUISITOS = ['titulo_profesional', 'colegiatura_vigente', 'experiencia_minima']
PROCESS_FEATURES = [
    'elapsed_days_since_publication', 'application_window_days', 'positions_count', 'applications_received_count',
    'configured_criteria_count', 'evaluations_scheduled_count', 'evaluations_completed_count',
    'evaluations_overdue_pending_count', 'interviews_scheduled_count', 'interviews_completed_count',
    'interviews_overdue_pending_count', 'stage_transition_count', 'days_since_last_operational_event',
    'concurrent_open_vacancies_count', 'days_remaining_to_target',
]
LEVEL_POINTS = {1: 5, 2: 10, 3: 15, 4: 20}   # correspondencia determinista nivel → puntaje (rango 0–20)

TABLES = {  # nombre de archivo → columnas en orden fijo
    'organizations': ['organization_token', 'source_type', 'synthetic_record_id'],
    'competencies': ['competency_id', 'organization_token', 'competency_label', 'scope', 'catalog_version',
                     'source_type', 'synthetic_record_id'],
    'vacancies': ['vacancy_token', 'organization_token', 'area', 'positions_count', 'published_at', 'closes_at',
                  'target_completion_at', 'criteria_version', 'rubric_version', 'source_type', 'synthetic_record_id'],
    'criteria': ['criterion_id', 'vacancy_token', 'competency_id', 'stage', 'method', 'weight', 'range_min',
                 'range_max', 'criteria_version', 'source_type', 'synthetic_record_id'],
    'rubric_levels': ['rubric_level_id', 'criterion_id', 'rubric_version', 'level', 'descriptor', 'rubric_points',
                      'source_type', 'synthetic_record_id'],
    'requirements': ['requirement_id', 'vacancy_token', 'requirement_type', 'min_years', 'source_type',
                     'synthetic_record_id'],
    'applications': ['application_token', 'vacancy_token', 'organization_token', 'person_token', 'submitted_at',
                     'application_state', 'years_experience_declared', 'source_type', 'synthetic_record_id'],
    'requirement_checks': ['check_id', 'application_token', 'requirement_id', 'declared_met', 'evidence_present',
                           'source_type', 'synthetic_record_id'],
    'sessions': ['session_token', 'application_token', 'vacancy_token', 'stage', 'evaluator_token', 'created_at',
                 'scheduled_for', 'status', 'completed_at', 'source_type', 'synthetic_record_id'],
    'assessments': ['assessment_id', 'session_token', 'application_token', 'criterion_id', 'evaluator_token',
                    'human_level', 'rubric_points', 'justification', 'evidence_sufficiency', 'recorded_at',
                    'rubric_version', 'criteria_version', 'source_type', 'synthetic_record_id'],
    'evidence': ['evidence_id', 'session_token', 'application_token', 'criterion_id', 'assessment_id', 'source_type_ev',
                 'source_reference', 'evidence_text', 'provenance', 'registered_by', 'registered_at', 'state',
                 'source_type', 'synthetic_record_id'],
    'annotations': ['annotation_id', 'assessment_id', 'author_token', 'created_at', 'reason', 'annotation_text',
                    'source_type', 'synthetic_record_id'],
    'process_events': ['event_id', 'vacancy_token', 'organization_token', 'event_type', 'event_at', 'ref_token',
                       'source_type', 'synthetic_record_id'],
    'process_snapshots': ['vacancy_token', 'organization_token', 'checkpoint_at', *PROCESS_FEATURES, 'delayed',
                          'observation_status', 'dataset_version', 'source_type', 'synthetic_record_id'],
    'process_splits': ['vacancy_token', 'checkpoint_at', 'label_known_at', 'split', 'split_reason', 'source_type',
                       'synthetic_record_id'],
    'analysis_runs': ['analysis_run_id', 'vacancy_token', 'organization_token', 'trigger', 'rules_version',
                      'criteria_version', 'rubric_version', 'input_hash_algorithm', 'input_snapshot_hash',
                      'created_at', 'source_type', 'synthetic_record_id'],
    'analysis_run_events': ['event_id', 'analysis_run_id', 'seq', 'state', 'event_at', 'error_code', 'source_type',
                            'synthetic_record_id'],
    'expected_alerts': ['alert_id', 'alert_type', 'vacancy_token', 'application_token', 'criterion_id', 'ref_id',
                        'source_type', 'synthetic_record_id'],
}
FAIRNESS_TABLE = ('fairness_sintetico/synthetic_group_attributes',
                  ['person_token', 'grupo_sintetico', 'source_type', 'synthetic_record_id'])
USED_REFS = set()


def iso(x):
    """Fecha → YYYY-MM-DD; instante → YYYY-MM-DDTHH:MM:SS (America/Lima, sin desplazamiento)."""
    if x is None:
        return ''
    return x.isoformat(timespec='seconds') if isinstance(x, dt.datetime) else x.isoformat()


def whole_days(a, b):
    """Días completos de a a b: floor(segundos / 86 400), como `wholeDays` de Laravel."""
    return math.floor((b - a).total_seconds() / DAY)


def checkpoint_of(closes):
    return dt.datetime.combine(closes + dt.timedelta(days=1), dt.time(0, 0, 0))


def at_time(day, rng, lo=8, hi=18):
    return dt.datetime.combine(day, dt.time(rng.randint(lo, hi - 1), rng.randint(0, 59), 0))


def input_snapshot_hash(vac, asms, evid):
    """Hash canónico del contenido de entrada de una ejecución de reglas (no solo de sus IDs).

    JSON canónico (claves ordenadas, sin espacios, UTF-8) con versiones y el contenido relevante de valoraciones y
    evidencias vinculadas, ordenado por ID. Solo datos sintéticos; sin tokens de persona ni de evaluador.
    """
    payload = {
        'algorithm': INPUT_HASH_ALGORITHM, 'vacancy_token': vac['vacancy_token'],
        'criteria_version': vac['criteria_version'], 'rubric_version': vac['rubric_version'],
        'rules_version': RULES_VERSION,
        'assessments': [{k: str(a[k]) for k in ('assessment_id', 'session_token', 'criterion_id', 'human_level',
                                                 'rubric_points', 'evidence_sufficiency', 'justification')}
                        for a in sorted(asms, key=lambda x: x['assessment_id'])],
        'evidence': [{k: str(e[k]) for k in ('evidence_id', 'assessment_id', 'criterion_id', 'source_type_ev',
                                              'source_reference', 'evidence_text')}
                     for e in sorted(evid, key=lambda x: x['evidence_id'])],
    }
    canon = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(canon.encode('utf-8')).hexdigest()


def generate(seed=SEED):
    rng = random.Random(seed)
    USED_REFS.clear()
    T = {k: [] for k in TABLES}
    fair = []
    rid = [0]

    def add(table, row, fairness=False):
        rid[0] += 1
        row = dict(row)
        row['source_type'] = 'synthetic'
        row['synthetic_record_id'] = f'SYN-{rid[0]:06d}'
        (fair if fairness else T[table]).append(row)
        return row

    # --- organizaciones, evaluadores y catálogos
    orgs = ['ORG-S1', 'ORG-S2', 'ORG-S3']
    evaluators = {o: [f'EV-{o[4:]}-{i:02d}' for i in range(1, 5)] for o in orgs}
    catalog = {}
    for o in orgs:
        add('organizations', {'organization_token': o})
        catalog[o] = []
        for i, (label, scope) in enumerate(COMPETENCIAS, 1):
            cid = f'CMP-{o[4:]}-{i:02d}'
            catalog[o].append((cid, label, scope))
            add('competencies', {'competency_id': cid, 'organization_token': o, 'competency_label': label,
                                 'scope': scope, 'catalog_version': f'CAT-{o[4:]}-v1'})

    # --- vacantes, criterios, rúbricas y requisitos
    vacancies, crit_by_vac, req_by_vac = [], {}, {}
    n_crit = n_req = 0
    for v in range(1, 121):
        o = orgs[(v - 1) % 3]
        area = 'docente' if rng.random() < 0.7 else 'administrativo'
        pub = at_time((BASE + dt.timedelta(days=rng.randint(0, 230))).date(), rng)
        prev = [x for x in vacancies if x['organization_token'] == o]
        if v % 10 == 3 and prev:     # empate deliberado: publicada justo en el checkpoint de otra vacante
            pub = prev[-1]['checkpoint_at']
        window = rng.randint(7, 21)
        closes = pub.date() + dt.timedelta(days=window)
        target = dt.datetime.combine(closes + dt.timedelta(days=rng.randint(15, 45)), dt.time(18, 0, 0))
        vt = f'VAC-{v:04d}'
        cv, rv = f'CV-{vt}-1', f'RV-{vt}-1'
        vac = dict(vacancy_token=vt, organization_token=o, area=area,
                   positions_count=rng.choices([1, 2, 3], [70, 20, 10])[0], published_at=pub, closes_at=closes,
                   target_completion_at=target, criteria_version=cv, rubric_version=rv,
                   checkpoint_at=checkpoint_of(closes))
        vacancies.append(vac)
        add('vacancies', {k: (iso(x) if isinstance(x, (dt.date, dt.datetime)) else x) for k, x in vac.items()
                          if k != 'checkpoint_at'})
        pool = [c for c in catalog[o] if c[2] in (area, 'ambos')]
        k = rng.randint(4, min(6, len(pool)))
        chosen = rng.sample(pool, k)
        n_eval = (k + 1) // 2
        raw = [rng.randint(10, 40) for _ in range(k)]
        tot = sum(raw)
        w = [r * 100 // tot for r in raw]
        rest = sorted(range(k), key=lambda i: -((raw[i] * 100) % tot))
        for i in rest[:100 - sum(w)]:
            w[i] += 1
        crits = []
        for i, (cid, label, _) in enumerate(chosen):
            n_crit += 1
            crid = f'CRI-{n_crit:04d}'
            stage = 'evaluacion' if i < n_eval else 'entrevista'
            method = rng.choice(METODO_EVAL) if stage == 'evaluacion' else 'entrevista_estructurada'
            crits.append(dict(criterion_id=crid, stage=stage, label=label))
            add('criteria', {'criterion_id': crid, 'vacancy_token': vt, 'competency_id': cid, 'stage': stage,
                             'method': method, 'weight': w[i], 'range_min': 0, 'range_max': 20,
                             'criteria_version': cv})
            for lv in range(1, 5):
                add('rubric_levels', {'rubric_level_id': f'{crid}-L{lv}', 'criterion_id': crid, 'rubric_version': rv,
                                      'level': lv, 'descriptor': f'{PREFIX} Nivel {lv} del criterio «{label}»: '
                                      'descriptor conductual de ejemplo.', 'rubric_points': LEVEL_POINTS[lv]})
        crit_by_vac[vt] = crits
        reqs = []
        for rt in rng.sample(REQUISITOS, rng.randint(1, 3)):
            n_req += 1
            rq = dict(requirement_id=f'REQ-{n_req:04d}', requirement_type=rt,
                      min_years=rng.randint(1, 5) if rt == 'experiencia_minima' else None)
            reqs.append(rq)
            add('requirements', {**rq, 'vacancy_token': vt, 'min_years': rq['min_years'] if rq['min_years'] else ''})
        req_by_vac[vt] = reqs
    vac_by = {v['vacancy_token']: v for v in vacancies}
    period = {v['vacancy_token']: (v['published_at'] - BASE).days // 60 for v in vacancies}   # efecto de periodo

    # --- postulaciones (VAC-0007 sin postulaciones: caso borde) e historial inicial de etapa
    apps, n_app, persons = [], 0, []
    histories = []          # (vacancy, organization, instante, ref) — application_stage_histories
    for vac in vacancies:
        vt = vac['vacancy_token']
        n = 0 if vt == 'VAC-0007' else rng.randint(2, 14)
        end = dt.datetime.combine(vac['closes_at'], dt.time(23, 59, 0))
        for _ in range(n):
            n_app += 1
            used_here = {x['person_token'] for x in apps if x['vacancy_token'] == vt}
            reuse = [p for p in persons if p not in used_here]
            if reuse and rng.random() < 0.08:             # misma persona sintética en OTRA vacante (caso borde)
                person = rng.choice(reuse)
            else:
                person = f'PER-S-{len(persons) + 1:05d}'
                persons.append(person)
            span = int((end - vac['published_at']).total_seconds()) // 60
            applied = vac['published_at'] + dt.timedelta(minutes=rng.randint(60, max(61, span)))
            years = None if rng.random() < 0.10 else rng.randint(0, 20)
            state = 'descartada' if rng.random() < 0.10 else 'activa'
            a = dict(application_token=f'APP-{n_app:05d}', vacancy_token=vt, organization_token=vac['organization_token'],
                     person_token=person, submitted_at=applied, application_state=state, years=years, _q=rng.random())
            apps.append(a)
            add('applications', {'application_token': a['application_token'], 'vacancy_token': vt,
                                 'organization_token': a['organization_token'], 'person_token': person,
                                 'submitted_at': iso(applied), 'application_state': state,
                                 'years_experience_declared': '' if years is None else years})
            histories.append((vt, vac['organization_token'], applied, f'{a["application_token"]}>recibida'))
            if state == 'descartada':
                t = applied + dt.timedelta(days=rng.randint(1, 5), hours=rng.randint(1, 6))
                if t <= OBSERVATION_END:
                    histories.append((vt, vac['organization_token'], t, f'{a["application_token"]}>descartada'))

    # --- requisitos declarados y alertas esperadas
    alerts = []

    def alert(kind, vt, app='', crit='', ref=''):
        alerts.append(dict(alert_type=kind, vacancy_token=vt, application_token=app, criterion_id=crit, ref_id=ref))

    n_chk = 0
    for a in apps:
        for rq in req_by_vac[a['vacancy_token']]:
            n_chk += 1
            if rq['requirement_type'] == 'experiencia_minima':
                met = None if a['years'] is None else a['years'] >= rq['min_years']
            else:
                met = None if rng.random() < 0.05 else rng.random() < 0.9
            present = rng.random() < 0.85
            ck = f'CHK-{n_chk:05d}'
            add('requirement_checks', {'check_id': ck, 'application_token': a['application_token'],
                                       'requirement_id': rq['requirement_id'],
                                       'declared_met': '' if met is None else str(met).lower(),
                                       'evidence_present': str(present).lower()})
            if met is not True or not present:
                alert('requisito_no_evidenciado', a['vacancy_token'], a['application_token'], '', ck)

    # --- sesiones, valoraciones, evidencias y anotaciones (nada posterior al fin de la observación)
    n_ses = n_asm = n_ev = n_ann = 0
    sessions, assessments, evidence = [], [], []
    for a in apps:
        if a['application_state'] != 'activa':
            continue
        vac = vac_by[a['vacancy_token']]
        vt, o, cp = vac['vacancy_token'], vac['organization_token'], vac['checkpoint_at']
        plan = [('evaluacion', rng.choice(evaluators[o]))]
        if rng.random() < 0.15:                                    # doble calificación para ICC
            plan.append(('evaluacion', rng.choice([e for e in evaluators[o] if e != plan[0][1]])))
        if rng.random() < 0.8:
            plan.append(('entrevista', rng.choice(evaluators[o])))
        first_level, staged = {}, set()
        for stage, ev in plan:
            if stage == 'evaluacion':
                created = a['submitted_at'] + dt.timedelta(days=rng.randint(1, 5), hours=rng.randint(0, 8))
                if rng.random() < 0.06 and a['submitted_at'] < cp:
                    created = cp                                   # empate deliberado con el checkpoint
            else:
                created = cp + dt.timedelta(days=rng.randint(0, 6), hours=rng.randint(9, 17))
            if created > OBSERVATION_END:
                continue                                           # aún no existe al cierre de la observación
            sched = created + dt.timedelta(days=rng.randint(2, 12) + period[vt], hours=rng.randint(0, 6))
            if stage == 'evaluacion' and created + dt.timedelta(days=2) <= cp and rng.random() < 0.08:
                sched = cp                                         # empate deliberado: programada justo en el checkpoint
            completed = sched + dt.timedelta(days=rng.randint(0, 4), hours=rng.randint(1, 5))
            done = rng.random() < 0.9 and completed <= OBSERVATION_END
            if not done:
                completed = None
            n_ses += 1
            st = f'SES-{n_ses:05d}'
            s = dict(session_token=st, application_token=a['application_token'], vacancy_token=vt, stage=stage,
                     evaluator_token=ev, created_at=created, scheduled_for=sched,
                     status='realizada' if done else 'programada', completed_at=completed)
            sessions.append(s)
            add('sessions', {**s, 'created_at': iso(created), 'scheduled_for': iso(sched), 'completed_at': iso(completed)})
            if stage not in staged:
                staged.add(stage)
                histories.append((vt, o, created, f'{a["application_token"]}>{stage}'))
            if not done and sched < OBSERVATION_END:
                alert('sesion_vencida', vt, a['application_token'], '', st)
            for c in [c for c in crit_by_vac[vt] if c['stage'] == stage]:
                n_evd = rng.choices([0, 1, 2, 3], [8, 30, 42, 20])[0]
                if not done:          # sesión PROGRAMADA: solo borradores de evidencia, sin valoración (FF-02)
                    for _ in range(rng.choice([0, 0, 1])):
                        n_ev += 1
                        evidence.append(add('evidence', evidence_row(rng, n_ev, s, c, '', 'borrador', created)))
                    continue
                key = (a['application_token'], c['criterion_id'])
                if key in first_level:
                    r = rng.random()
                    delta = 0 if r < 0.65 else (rng.choice([-1, 1]) if r < 0.88 else rng.choice([-2, 2]))
                    level = min(4, max(1, first_level[key] + delta))
                    if abs(level - first_level[key]) >= 2:
                        alert('discrepancia_evaluadores', vt, a['application_token'], c['criterion_id'], st)
                else:
                    level = min(4, max(1, 1 + int(a['_q'] * 4) + (rng.choice([-1, 1]) if rng.random() < 0.3 else 0)))
                    first_level[key] = level
                suff = ('insuficiente' if n_evd == 0 else
                        rng.choice(['parcial', 'suficiente']) if n_evd == 1 else
                        rng.choice(['suficiente', 'suficiente', 'parcial']))
                n_asm += 1
                aid = f'ASM-{n_asm:05d}'
                asm = dict(assessment_id=aid, session_token=st, application_token=a['application_token'],
                           criterion_id=c['criterion_id'], evaluator_token=ev, human_level=level,
                           rubric_points=LEVEL_POINTS[level],
                           justification=f'{PREFIX} Nivel {level}: la evidencia registrada corresponde al descriptor; '
                           f'para el nivel {min(4, level + 1)} faltaría un ejemplo más completo.',
                           evidence_sufficiency=suff, recorded_at=completed,
                           rubric_version=vac['rubric_version'], criteria_version=vac['criteria_version'])
                assessments.append(asm)
                add('assessments', {**asm, 'recorded_at': iso(completed)})
                if n_evd == 0:
                    alert('evidencia_faltante', vt, a['application_token'], c['criterion_id'], aid)
                for _ in range(n_evd):
                    n_ev += 1
                    evidence.append(add('evidence', evidence_row(rng, n_ev, s, c, aid, 'vinculada', completed)))
                ann_at = completed + dt.timedelta(days=rng.randint(1, 10))
                if rng.random() < 0.05 and ann_at <= OBSERVATION_END:
                    n_ann += 1
                    add('annotations', {'annotation_id': f'ANN-{n_ann:04d}', 'assessment_id': aid, 'author_token': ev,
                                        'created_at': iso(ann_at), 'reason': rng.choice(['aclaracion', 'fuente_adicional']),
                                        'annotation_text': f'{PREFIX} Anotación complementaria: no modifica el nivel '
                                        'ni el puntaje registrados.'})

    # --- cierre simulado (fuente de la etiqueta) y censura al final de la observación
    ses_by_vac = {}
    for s in sessions:
        ses_by_vac.setdefault(s['vacancy_token'], []).append(s)
    closed_at = {}
    for vac in vacancies:
        vt = vac['vacancy_token']
        done = [s['completed_at'] for s in ses_by_vac.get(vt, []) if s['completed_at']]
        base_t = max(done) if done else vac['checkpoint_at']
        closed = base_t + dt.timedelta(days=rng.randint(2, 12) + period[vt], hours=rng.randint(1, 8))
        closed_at[vt] = closed if closed <= OBSERVATION_END else None   # None = sin cierre observado (censurada)

    # --- eventos del proceso (línea de tiempo truncada al fin de la observación)
    n_pe = 0
    order = {'vacante_publicada': 0, 'postulacion_recibida': 1, 'cambio_etapa': 2, 'evaluacion_programada': 3,
             'entrevista_programada': 3, 'evaluacion_realizada': 4, 'entrevista_realizada': 4, 'vacante_cerrada': 5}
    raw_events = []
    for vac in vacancies:
        vt, o = vac['vacancy_token'], vac['organization_token']
        raw_events.append((vt, o, 'vacante_publicada', vac['published_at'], ''))
        for a in [a for a in apps if a['vacancy_token'] == vt]:
            raw_events.append((vt, o, 'postulacion_recibida', a['submitted_at'], a['application_token']))
        for s in ses_by_vac.get(vt, []):
            raw_events.append((vt, o, f'{s["stage"]}_programada', s['created_at'], s['session_token']))
            if s['completed_at']:
                raw_events.append((vt, o, f'{s["stage"]}_realizada', s['completed_at'], s['session_token']))
        if closed_at[vt]:
            raw_events.append((vt, o, 'vacante_cerrada', closed_at[vt], ''))
    raw_events += [(vt, o, 'cambio_etapa', t, ref) for vt, o, t, ref in histories]
    # Orden determinista: vacante, instante, prioridad del tipo, referencia (los empates no cambian la inclusión).
    for vt, o, kind, t, ref in sorted(raw_events, key=lambda e: (e[0], e[3], order[e[2]], e[4])):
        n_pe += 1
        add('process_events', {'event_id': f'PEV-{n_pe:05d}', 'vacancy_token': vt, 'organization_token': o,
                               'event_type': kind, 'event_at': iso(t), 'ref_token': ref})

    # --- snapshots del proceso (semántica RF-29: t <= checkpoint_at)
    snaps = []
    for vac in vacancies:
        vt = vac['vacancy_token']
        feats = process_features(vac, vac['checkpoint_at'], [e for e in raw_events if e[0] == vt],
                                 {s['session_token']: s for s in ses_by_vac.get(vt, [])},
                                 [x for x in vacancies if x['organization_token'] == vac['organization_token']],
                                 closed_at, len(crit_by_vac[vt]))
        observed = closed_at[vt] is not None
        row = {'vacancy_token': vt, 'organization_token': vac['organization_token'],
               'checkpoint_at': iso(vac['checkpoint_at']), **feats,
               'delayed': int(closed_at[vt] > vac['target_completion_at']) if observed else '',
               'observation_status': 'completed' if observed else 'censored', 'dataset_version': DATASET_VERSION}
        snaps.append((row, vac['checkpoint_at'], closed_at[vt]))
        add('process_snapshots', row)

    # --- partición temporal con purga por madurez de la etiqueta (embargo)
    labeled = sorted([x for x in snaps if x[2] is not None], key=lambda x: (x[1], x[0]['vacancy_token']))
    n = len(labeled)
    split = {}
    for i, (row, cp, known) in enumerate(labeled):
        # 50/30/20: cada bloque dura más que la maduración de la etiqueta (~35 días), así la purga no lo vacía.
        split[row['vacancy_token']] = 'train' if i < int(n * 0.50) else ('validation' if i < int(n * 0.80) else 'test')
    starts = {s: min(cp for row, cp, _ in labeled if split[row['vacancy_token']] == s) for s in ('validation', 'test')}
    nxt = {'train': 'validation', 'validation': 'test'}
    for row, cp, known in sorted(snaps, key=lambda x: (x[1], x[0]['vacancy_token'])):
        vt = row['vacancy_token']
        if known is None:
            sp, why = 'censurado', 'sin_cierre_observado'
        elif split[vt] in nxt and known >= starts[nxt[split[vt]]]:
            sp, why = 'purgado', 'etiqueta_no_madura_antes_de_' + nxt[split[vt]]
        else:
            sp, why = split[vt], 'temporal'
        add('process_splits', {'vacancy_token': vt, 'checkpoint_at': iso(cp), 'label_known_at': iso(known),
                               'split': sp, 'split_reason': why})

    # --- análisis (registro inmutable), eventos de solo inserción y hash canónico del contenido
    n_are = 0
    for vac in vacancies:
        vt = vac['vacancy_token']
        app_set = {a['application_token'] for a in apps if a['vacancy_token'] == vt}
        asms = [x for x in assessments if x['application_token'] in app_set]
        if not asms:
            continue
        evid = [e for e in evidence if e['assessment_id'] in {x['assessment_id'] for x in asms}]
        failed_first = rng.random() < 0.08
        for attempt in range(2 if failed_first else 1):
            created = max(x['recorded_at'] for x in asms) + dt.timedelta(days=attempt, hours=1)
            if created > OBSERVATION_END:
                break
            run_id = str(uuid.UUID(int=rng.getrandbits(128), version=4))
            add('analysis_runs', {'analysis_run_id': run_id, 'vacancy_token': vt,
                                  'organization_token': vac['organization_token'], 'trigger': 'resultado_registrado',
                                  'rules_version': RULES_VERSION, 'criteria_version': vac['criteria_version'],
                                  'rubric_version': vac['rubric_version'], 'input_hash_algorithm': INPUT_HASH_ALGORITHM,
                                  'input_snapshot_hash': input_snapshot_hash(vac, asms, evid), 'created_at': iso(created)})
            states = ['pendiente', 'en_proceso', 'fallido' if (failed_first and attempt == 0) else 'completado']
            for seq, stt in enumerate(states, 1):
                n_are += 1
                add('analysis_run_events', {'event_id': f'ARE-{n_are:05d}', 'analysis_run_id': run_id, 'seq': seq,
                                            'state': stt, 'event_at': iso(created + dt.timedelta(minutes=seq - 1)),
                                            'error_code': 'E-10' if stt == 'fallido' else ''})

    # --- alertas esperadas (oráculo del generador; el validador las recalcula de forma independiente)
    for i, al in enumerate(sorted(alerts, key=lambda x: (x['alert_type'], x['ref_id'])), 1):
        add('expected_alerts', {'alert_id': f'ALR-{i:05d}', **al})

    # --- atributos de grupo SINTÉTICOS (separados; solo pruebas metodológicas de equidad)
    for p in persons:
        add(None, {'person_token': p, 'grupo_sintetico': rng.choice(['GS-A', 'GS-B'])}, fairness=True)
    return T, fair


def evidence_row(rng, n, s, c, aid, state, when):
    # La fuente es única por sesión y criterio: dos evidencias iguales en la misma valoración serían duplicados.
    while True:
        if s['stage'] == 'entrevista':
            src, ref = 'nota_entrevista', f'pregunta:PRG-{rng.randint(1, 40):03d}'
        else:
            src = rng.choice(['cv', 'documento', 'prueba', 'formulario'])
            ref = f'{src}:DOC-S-{rng.randint(1, 9999):04d}#p{rng.randint(1, 6)}'
        if (s['session_token'], c['criterion_id'], ref) not in USED_REFS:
            USED_REFS.add((s['session_token'], c['criterion_id'], ref))
            break
    text = rng.choice([
        f'{PREFIX} Describe una situación concreta relacionada con «{c["label"]}».',
        f'{PREFIX} Menciona una práctica general vinculada a «{c["label"]}», sin ejemplo concreto.',
        f'{PREFIX} Aporta un ejemplo con propósito, acción y resultado para «{c["label"]}».',
    ])
    return {'evidence_id': f'EVD-{n:06d}', 'session_token': s['session_token'],
            'application_token': s['application_token'], 'criterion_id': c['criterion_id'], 'assessment_id': aid,
            'source_type_ev': src, 'source_reference': ref, 'evidence_text': text, 'provenance': 'registro_humano',
            'registered_by': s['evaluator_token'], 'registered_at': iso(when), 'state': state}


def process_features(vac, at, events, ses, org_vacs, closed_at, n_criteria):
    """Las 15 variables RF-29 con la semántica de OperationalRiskFeatureBuilder (t <= at)."""
    pre = [e for e in events if e[3] <= at]
    cnt = lambda kind: sum(1 for e in pre if e[2] == kind)
    done = {e[4] for e in pre if e[2].endswith('_realizada')}

    def overdue(stage):        # created_at <= at, scheduled_at < at, sin completar en at
        return sum(1 for e in pre if e[2] == f'{stage}_programada' and ses[e[4]]['scheduled_for'] < at
                   and e[4] not in done)
    last = max((e[3] for e in pre if e[2] != 'vacante_cerrada'), default=vac['published_at'])
    open_others = sum(1 for x in org_vacs if x['vacancy_token'] != vac['vacancy_token'] and x['published_at'] <= at
                      and (closed_at[x['vacancy_token']] is None or closed_at[x['vacancy_token']] > at))
    start = dt.datetime.combine(vac['published_at'].date(), dt.time(0, 0))
    return {
        'elapsed_days_since_publication': max(0, whole_days(vac['published_at'], at)),
        'application_window_days': max(0, whole_days(start, dt.datetime.combine(vac['closes_at'], dt.time(0, 0)))),
        'positions_count': vac['positions_count'],
        'applications_received_count': cnt('postulacion_recibida'),
        'configured_criteria_count': n_criteria,
        'evaluations_scheduled_count': cnt('evaluacion_programada'),
        'evaluations_completed_count': cnt('evaluacion_realizada'),
        'evaluations_overdue_pending_count': overdue('evaluacion'),
        'interviews_scheduled_count': cnt('entrevista_programada'),
        'interviews_completed_count': cnt('entrevista_realizada'),
        'interviews_overdue_pending_count': overdue('entrevista'),
        'stage_transition_count': cnt('cambio_etapa'),
        'days_since_last_operational_event': max(0, whole_days(last, at)),
        'concurrent_open_vacancies_count': open_others,
        'days_remaining_to_target': whole_days(at, vac['target_completion_at']),
    }


def sha(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def write(out, T, fair, seed):
    os.makedirs(os.path.join(out, 'fairness_sintetico'), exist_ok=True)
    files = {}
    items = [(k, TABLES[k], T[k]) for k in TABLES] + [(FAIRNESS_TABLE[0], FAIRNESS_TABLE[1], fair)]
    for name, cols, rows in items:
        path = os.path.join(out, name + '.csv')
        with open(path, 'w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, fieldnames=cols, lineterminator='\n', extrasaction='raise')
            w.writeheader()
            for r in rows:
                w.writerow({c: ('' if r.get(c) is None else r.get(c)) for c in cols})
        files[name + '.csv'] = {'rows': len(rows), 'columns': len(cols), 'sha256': sha(path)}
    manifest = {
        'dataset_version': DATASET_VERSION, 'generator_version': GENERATOR_VERSION, 'schema_version': SCHEMA_VERSION,
        'feature_set_version': FEATURE_SET_VERSION, 'rules_version': RULES_VERSION, 'seed': seed,
        'generated_at': GENERATED_AT, 'observation_end': iso(OBSERVATION_END), 'source': 'synthetic',
        'python_random': 'random.Random (Mersenne Twister)', 'input_hash_algorithm': INPUT_HASH_ALGORITHM,
        'temporal_semantics': {'timezone': 'America/Lima', 'granularity': 'segundo',
                               'checkpoint': 'inicio del día siguiente a closes_at (ADR-004)',
                               'inclusion': 't <= checkpoint_at (scheduled_at < checkpoint_at para vencidas)',
                               'open_vacancy': 'published_at <= at y (closed_at nulo o closed_at > at)',
                               'whole_days': 'floor(segundos / 86400)'},
        'rubric_versions': sorted({r['rubric_version'] for r in T['vacancies']}),
        'criteria_versions': sorted({r['criteria_version'] for r in T['vacancies']}),
        'feature_set': {'process_features': PROCESS_FEATURES, 'target': 'delayed',
                        'excluded_from_features': ['grupo_sintetico (archivo separado)', 'textos libres',
                                                   'human_level', 'rubric_points', 'evidence_sufficiency',
                                                   'evaluator_disagreement y agregados derivados',
                                                   'tokens e identificadores', 'label_known_at']},
        'files': files,
        'total_rows': sum(v['rows'] for v in files.values()),
        'note': 'Dataset 100 % sintético. NO representa datos reales del Colegio Andino.',
    }
    with open(os.path.join(out, 'manifest.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
        f.write('\n')
    return manifest


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed', type=int, default=SEED)
    ap.add_argument('--out', default=DEFAULT_OUT)
    a = ap.parse_args()
    T, fair = generate(a.seed)
    m = write(a.out, T, fair, a.seed)
    for k, v in m['files'].items():
        print(f'{k:48} {v["rows"]:6d} filas  {v["sha256"][:16]}')
    print('total', m['total_rows'], 'filas · semilla', a.seed)


if __name__ == '__main__':
    main()
