"""Arnés de evaluación de las ayudas documentales de ML-02 (preparación de F38). Solo biblioteca estándar.

PREPARACIÓN — NO HAY MÉTODO. Este arnés no implementa ninguna ayuda, no entrena y no procesa evidencia:
compara una salida dada (un archivo JSON) con el oro sintético y calcula las métricas del plan de
evaluación de F36-SBX (M-01 a M-08, M-11 y M-12). Las salidas que se usan hoy están escritas a mano.

Uso:
    python -I -B f38_evaluar.py <salida.json> [--particion dev|test]
    python -I -B f38_evaluar.py --sello      # imprime el sello de la partición test
"""

from __future__ import annotations

import hashlib
import json
import math
import pathlib
import random
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
GOLD = HERE.parent / 'conjunto' / 'ml02_casos_sinteticos.json'
CONTRACT = HERE.parents[1] / 'f36-sbx' / 'contrato' / 'f36sbx_evidence_contract.json'
SEAL_TAG = 'f38-ml02-test-seal-v1'
BOOTSTRAP_SEED = 2381  # semilla declarada en la especificación, fija para que el intervalo sea reproducible
BOOTSTRAP_ROUNDS = 2000
PARTITIONS = ('dev', 'test')  # el contrato v4 prohíbe train (train_allowed = false)

# Catálogo cerrado de tareas y forma de cada salida. Una tarea fuera del catálogo invalida el resultado.
OUTPUT_SHAPES = {'EI-01': list, 'EI-02': list, 'EI-03': list, 'EI-04': dict, 'EI-05': list, 'EI-07': list,
                 'EI-09': list}
LIST_FIELDS = {'fragments', 'fragment_refs'}

# M-12: claves y valores admitidos en cada salida. Cualquier otra clave o texto es una violación.
OUTPUT_KEYS = {
    'EI-01': {'fragment', 'group'}, 'EI-02': {'application', 'requirement'}, 'EI-05': {'id', 'decision'},
    'EI-07': {'query', 'fragments'}, 'EI-09': {'application', 'criterion', 'fragment_refs', 'abstained'},
}
ID_VALUE = re.compile(r'^(FRG|APP|REQ|CRI|LNK|PII|Q|P)-[A-Z0-9-]+$')
GROUP_VALUE = re.compile(r'^(cv|certificado|transcripcion_revisada|observacion)\|CRI-[A-Z0-9-]+\|'
                         r'(documento_presentado|sesion_asignada)$')
ENUM_VALUES = {'rechazo', 'admision'}

# Umbrales de aceptación del plan (F36SBX_Plan_Evaluacion §2). None: se fija en el preregistro.
THRESHOLDS = {'M-01': 1.0, 'M-02': 1.0, 'M-03': 1.0, 'M-04': 1.0, 'M-05': 1.0, 'M-06': 1.0, 'M-07': None,
              'M-08': 1.0, 'M-11': 1.0, 'M-12': 0}


def canonical(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')


def load(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


class Gold:
    def __init__(self, data: dict):
        self.data = data
        self.partition_of = {v: p for p, vs in data['partitions'].items() for v in vs}
        self.vacancy_of = {a['token']: a['vacancy'] for a in data['applications']}
        self.fragments = {f['id']: f for f in data['fragments']}
        self.criteria = {c['id']: (v['token'], c['version']) for v in data['vacancies'] for c in v['criteria']}
        self.tasks = data['tasks']

    def in_partition(self, partition: str, *, application=None, vacancy=None, fragment=None) -> bool:
        if fragment is not None:
            application = self.fragments[fragment]['application']
        if application is not None:
            vacancy = self.vacancy_of[application]
        return self.partition_of.get(vacancy) == partition

    def projection(self, partition: str) -> dict:
        """Todo lo que pertenece a una partición: lo que sella el sello de test."""
        apps = sorted(a for a, v in self.vacancy_of.items() if self.partition_of.get(v) == partition)
        t = self.tasks
        return {
            'vacancies': [v for v in self.data['vacancies'] if self.partition_of.get(v['token']) == partition],
            'applications': apps,
            'fragments': [f for f in self.data['fragments'] if f['application'] in apps],
            'EI-01': [c for c in t['EI-01']['cases'] if self.in_partition(partition, fragment=c['fragment'])],
            'EI-02': {k: [x for x in t['EI-02'][k] if x['application'] in apps]
                      for k in ('declared_evidence', 'expected_alerts')},
            'EI-03': [link for link in t['EI-03']['links'] if link['application'] in apps],
            'EI-03-broken': sorted(x for x in t['EI-03']['expected_broken']
                                   if any(link['id'] == x and link['application'] in apps
                                          for link in t['EI-03']['links'])),
            'EI-04': t['EI-04'] if self.partition_of.get(t['EI-04']['vacancy']) == partition else None,
            'EI-05': [c for c in t['EI-05']['cases'] if self.partition_of.get(c['vacancy']) == partition],
            'EI-07': [q for q in t['EI-07']['queries'] if q['application'] in apps],
            'EI-09': {'annotations': [a for a in t['EI-09']['annotations'] if a['application'] in apps],
                      'no_evidence_cases': [c for c in t['EI-09']['no_evidence_cases'] if c['application'] in apps]},
            'EI-09-k': t['EI-09']['k'],  # parámetro compartido: cambiarlo altera las métricas de test
        }

    def seal(self) -> str:
        return hashlib.sha256(f'{SEAL_TAG}\n'.encode('utf-8') + canonical(self.projection('test'))).hexdigest()


def forbidden_tokens() -> frozenset[str]:
    return frozenset(load(CONTRACT)['forbidden_field_tokens'])


# ------------------------------------------------------------------------------- comprobaciones
def key_tokens(key) -> list[str]:
    """Palabras de un nombre de campo, con camelCase separado: `candidateScore` da candidate y score."""
    spaced = re.sub(r'(?<=[a-z0-9])(?=[A-Z])', '_', str(key))
    return [t for t in re.split(r'[_\W]+', spaced.lower()) if t]


def malformed(outputs) -> list[str]:
    """Problemas de forma que impiden evaluar: se rechazan antes de calcular ninguna métrica."""
    if not isinstance(outputs, dict):
        return ['outputs no es un objeto']
    problems = []
    for task, rows in outputs.items():
        shape = OUTPUT_SHAPES.get(task)
        if shape is None:
            problems.append(f'tarea no admitida: {task}')
        elif not isinstance(rows, shape):
            problems.append(f'{task}: forma no admitida')
        elif task in OUTPUT_KEYS:
            for i, row in enumerate(rows):
                if not isinstance(row, dict):
                    problems.append(f'{task}[{i}]: no es un objeto')
                    continue
                for key, value in row.items():
                    well_formed = (isinstance(value, list) and all(isinstance(x, str) for x in value)
                                   if key in LIST_FIELDS else not isinstance(value, (dict, list)))
                    if not well_formed:
                        problems.append(f'{task}[{i}].{key}: forma no admitida')
                    elif key in LIST_FIELDS and len(set(value)) != len(value):
                        problems.append(f'{task}[{i}].{key}: identificadores repetidos')
        elif task == 'EI-03' and any(isinstance(x, (dict, list)) for x in rows):
            problems.append('EI-03: elemento que no es un identificador')
    return problems


def output_violations(outputs: dict) -> tuple[list[str], list[str]]:
    """Devuelve (texto_libre, campos_prohibidos). Recorre toda la salida, a cualquier profundidad."""
    free, forbidden, tokens = [], [], forbidden_tokens()

    def walk(value, where):
        if isinstance(value, dict):
            for key, item in value.items():
                if any(t in tokens for t in key_tokens(key)):
                    forbidden.append(f'{where}.{key}')
                walk(item, f'{where}.{key}')
        elif isinstance(value, list):
            for i, item in enumerate(value):
                walk(item, f'{where}[{i}]')
        elif isinstance(value, str):
            if not (ID_VALUE.match(value) or GROUP_VALUE.match(value) or value in ENUM_VALUES):
                free.append(where)
        elif not (isinstance(value, bool) and where.endswith('.abstained')):
            free.append(where)  # un número, un nulo o un booleano fuera de `abstained` no es una salida admitida

    for task, rows in outputs.items():
        walk(rows, task)
        if task in OUTPUT_KEYS:
            for i, row in enumerate(rows):
                extra = set(row) - OUTPUT_KEYS[task] if isinstance(row, dict) else {'(no es un objeto)'}
                free += [f'{task}[{i}].{k}' for k in sorted(extra)]
    return sorted(set(free)), sorted(set(forbidden))


def attribution(gold: Gold, outputs: dict) -> tuple[int, int, list[str]]:
    """M-11: cada fragmento citado existe y es de la postulación del caso."""
    checked, bad = 0, []
    for row in outputs.get('EI-01', []):
        checked += 1
        if row.get('fragment') not in gold.fragments:
            bad.append(f'EI-01 {row.get("fragment")}')
    queries = {q['id']: q for q in gold.tasks['EI-07']['queries']}
    for row in outputs.get('EI-07', []):
        app = queries.get(row.get('query'), {}).get('application')
        for frag in row.get('fragments', []):
            checked += 1
            if gold.fragments.get(frag, {}).get('application') != app:
                bad.append(f'EI-07 {row.get("query")} {frag}')
    for row in outputs.get('EI-09', []):
        for frag in row.get('fragment_refs', []):
            checked += 1
            if gold.fragments.get(frag, {}).get('application') != row.get('application'):
                bad.append(f'EI-09 {row.get("application")} {frag}')
    return checked, len(bad), bad


# ----------------------------------------------------------------------------------- métricas
def ratio(num: int, den: int):
    return None if den == 0 else num / den


def ranking_metrics(relevant: set, ranked: list, k: int) -> dict:
    top = ranked[:k]
    hits = [1 if f in relevant else 0 for f in top]
    dcg = sum(h / math.log2(i + 2) for i, h in enumerate(hits))
    ideal = sum(1 / math.log2(i + 2) for i in range(min(len(relevant), k)))
    first = next((i + 1 for i, f in enumerate(ranked) if f in relevant), None)
    return {'recall': sum(hits) / len(relevant), 'precision': sum(hits) / k,
            'rr': 1 / first if first else 0.0, 'ndcg': dcg / ideal if ideal else 0.0}


def bootstrap_ci(per_unit: dict, rounds: int = BOOTSTRAP_ROUNDS, seed: int = BOOTSTRAP_SEED):
    """Intervalo percentil al 95 % del recall micro, remuestreando vacantes (la unidad de partición)."""
    units = sorted(per_unit)
    if len(units) < 2:
        return {'status': 'no informativo', 'units': len(units)}
    rng, values = random.Random(seed), []
    for _ in range(rounds):
        sample = [per_unit[rng.choice(units)] for _ in units]
        den = sum(d for _, d in sample)
        values.append(sum(n for n, _ in sample) / den if den else 0.0)
    values.sort()
    return {'status': 'ok', 'units': len(units), 'low': values[int(0.025 * rounds)],
            'high': values[int(0.975 * rounds) - 1]}


def evaluate(gold: Gold, submission: dict, partition: str) -> dict:
    if not isinstance(submission, dict):
        return {'set_id': gold.data['set_id'], 'method_id': None, 'partition': partition, 'metrics': {},
                'violations': [f'la raíz de la salida no es un objeto JSON: {type(submission).__name__}'],
                'valid': False, 'acceptance': {}}
    outputs = submission.get('outputs', {})
    result = {'set_id': gold.data['set_id'], 'method_id': submission.get('method_id'), 'partition': partition,
              'metrics': {}, 'violations': []}
    refused = ([f'partición no admitida: {partition}'] if partition not in PARTITIONS else []) + malformed(outputs)
    if refused:
        result.update(violations=refused, valid=False, acceptance={})
        return result
    proj = gold.projection(partition)
    if submission.get('set_id') != gold.data['set_id']:
        result['violations'].append('la salida es de otro conjunto')
    if partition == 'test' and gold.seal() != gold.data['test_seal_sha256']:
        result['violations'].append('el sello de test no coincide: el conjunto cambió después del preregistro')
    free, forbidden = output_violations(outputs)
    if forbidden:
        result['violations'].append(f'campos sobre personas o de juicio: {forbidden}')
    m = result['metrics']

    expected = {c['fragment']: c['expected_group'] for c in proj['EI-01']}
    got = {r.get('fragment'): r.get('group') for r in outputs.get('EI-01', []) if r.get('fragment') in expected}
    m['M-01'] = ratio(sum(got.get(f) == g for f, g in expected.items()), len(expected))

    gold_alerts = {(a['application'], a['requirement']) for a in proj['EI-02']['expected_alerts']}
    apps = set(proj['applications'])
    pred = {(a.get('application'), a.get('requirement')) for a in outputs.get('EI-02', [])
            if a.get('application') in apps}
    m['M-02'] = {'precision': ratio(len(pred & gold_alerts), len(pred)) if pred else (1.0 if not gold_alerts else 0.0),
                 'recall': ratio(len(pred & gold_alerts), len(gold_alerts))}

    links = {link['id'] for link in proj['EI-03']}
    broken, flagged = set(proj['EI-03-broken']), {x for x in outputs.get('EI-03', []) if x in links}
    m['M-03'] = {'detection': ratio(len(flagged & broken), len(broken)), 'false_positives': len(flagged - broken)}

    if proj['EI-04'] is not None:
        orders = outputs.get('EI-04', {})
        target = proj['EI-04']['expected_order']
        m['M-04'] = 1.0 if all(orders.get(p) == target for p in proj['EI-04']['permutations']) else 0.0

    cases = proj['EI-05']
    decisions = {r.get('id'): r.get('decision') for r in outputs.get('EI-05', [])}
    seeded = [c for c in cases if c['expected'] == 'rechazo']
    clean = [c for c in cases if c['expected'] == 'admision']
    m['M-05'] = {'recall': ratio(sum(decisions.get(c['id']) == 'rechazo' for c in seeded), len(seeded)),
                 'false_rejections': sum(decisions.get(c['id']) == 'rechazo' for c in clean)}

    answers = {r.get('query'): sorted(r.get('fragments', [])) for r in outputs.get('EI-07', [])}
    m['M-06'] = ratio(sum(answers.get(q['id']) == sorted(q['expected_fragments']) for q in proj['EI-07']),
                      len(proj['EI-07']))

    k = gold.tasks['EI-09']['k']
    runs = {(r.get('application'), r.get('criterion')): r for r in outputs.get('EI-09', [])}
    by_query, strata, per_unit = {}, {}, {}
    for a in proj['EI-09']['annotations']:
        if a['relevance'] == 'relevante':
            by_query.setdefault((a['application'], a['criterion']), set()).add(a['fragment'])
    per_query = []
    for key, relevant in sorted(by_query.items()):
        ranked = runs.get(key, {}).get('fragment_refs', [])
        per_query.append(ranking_metrics(relevant, ranked, k))
        vacancy = gold.vacancy_of[key[0]]
        n, d = per_unit.get(vacancy, (0, 0))
        per_unit[vacancy] = (n + len(set(ranked[:k]) & relevant), d + len(relevant))
    for a in proj['EI-09']['annotations']:
        if a['relevance'] == 'relevante':
            ranked = runs.get((a['application'], a['criterion']), {}).get('fragment_refs', [])
            hit, total = strata.get(a['stratum'], (0, 0))
            strata[a['stratum']] = (hit + (a['fragment'] in ranked[:k]), total + 1)
    if per_query:
        m['M-07'] = {
            'k': k, 'queries': len(per_query),
            'recall_at_k': sum(q['recall'] for q in per_query) / len(per_query),
            'precision_at_k': sum(q['precision'] for q in per_query) / len(per_query),
            'mrr': sum(q['rr'] for q in per_query) / len(per_query),
            'ndcg_at_k': sum(q['ndcg'] for q in per_query) / len(per_query),
            'recall_by_stratum': {s: ratio(h, t) for s, (h, t) in sorted(strata.items())},
            'recall_ci95': bootstrap_ci(per_unit),
        }
    empty = proj['EI-09']['no_evidence_cases']
    if empty:
        ok = sum(bool(runs.get((c['application'], c['criterion']), {}).get('abstained'))
                 and not runs.get((c['application'], c['criterion']), {}).get('fragment_refs')
                 for c in empty)
        m['M-08'] = {'correct_abstention': ratio(ok, len(empty)),
                     'false_abstentions': sum(bool(runs.get(q, {}).get('abstained')) for q in by_query)}

    checked, bad_count, bad = attribution(gold, outputs)
    m['M-11'] = ratio(checked - bad_count, checked) if checked else None
    m['M-12'] = len(free)
    if bad:
        result['violations'].append(f'citas sin atribución válida: {bad}')
    if free:
        result['violations'].append(f'texto libre o claves no admitidas: {free}')
    result['valid'] = not result['violations']
    result['acceptance'] = acceptance(m)
    return result


def acceptance(m: dict) -> dict:
    """Aplica los umbrales del plan. M-07 no tiene umbral hasta el preregistro."""
    def value(key, sub=None):
        v = m.get(key)
        return v.get(sub) if isinstance(v, dict) and sub else v
    checks = {
        'M-01': value('M-01'), 'M-02': min(value('M-02', 'precision') or 0, value('M-02', 'recall') or 0),
        'M-03': value('M-03', 'detection') if value('M-03', 'false_positives') == 0 else 0.0,
        'M-04': value('M-04'), 'M-05': value('M-05', 'recall'), 'M-06': value('M-06'),
        'M-08': value('M-08', 'correct_abstention'), 'M-11': value('M-11'),
    }
    out = {k: (None if v is None else v >= THRESHOLDS[k]) for k, v in checks.items()}
    out['M-12'] = m.get('M-12') == THRESHOLDS['M-12']
    out['M-07'] = 'sin umbral: se fija en el preregistro (EI-09 es CONDITIONAL)'
    return out


def main(argv: list[str]) -> int:
    gold = Gold(load(GOLD))
    if argv[:1] == ['--sello']:
        print(gold.seal())
        return 0
    if not argv:
        print(__doc__)
        return 2
    partition = (argv[argv.index('--particion') + 1:] or [''])[0] if '--particion' in argv else 'dev'
    result = evaluate(gold, load(pathlib.Path(argv[0])), partition)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['valid'] else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
