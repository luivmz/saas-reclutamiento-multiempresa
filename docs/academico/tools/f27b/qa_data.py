"""Datos de la QA (F29E, F29F y F29G) leídos de fuentes reales, sin valores escritos a mano:

- el código de pruebas del repositorio (PHPUnit, Cypress, Vitest y pytest);
- la matriz maestra docs/final-report/traceability-master.md (clase de PHPUnit → RF y RF → spec de Cypress);
- la evidencia de la ejecución F29F, versionada en docs/academico/qa-final/evidencias/.
"""
import csv
import os
import re
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
EVID = os.path.join(ROOT, 'docs', 'academico', 'qa-final', 'evidencias')
EVID_REL = 'docs/academico/qa-final/evidencias'


def _read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def humanize(method):
    """test_rf10_rf11_candidate_applies… → «candidate applies…» (lo que verifica la prueba)."""
    name = re.sub(r'^test_((?:rf\d\d_)+)?', '', method)
    return name.replace('_', ' ')


def rf_tokens(method):
    m = re.match(r'test_((?:rf\d\d_)+)', method)
    return tuple('RF-' + x[2:] for x in m.group(1).strip('_').split('_')) if m else ()


# ------------------------------------------------------------------ matriz maestra
def traceability():
    """(clase de PHPUnit → RF, RF → specs E2E) según la matriz maestra."""
    cls, e2e = {}, {}
    for line in _read(os.path.join(ROOT, 'docs', 'final-report', 'traceability-master.md')).splitlines():
        m = re.match(r'\| (RF-\d\d) \|', line)
        if not m:
            continue
        cols = [c.strip() for c in line.strip().strip('|').split('|')]
        for c in re.findall(r'`([A-Za-z]+Test)(?:::|`)', cols[5]):
            cls.setdefault(c, set()).add(m.group(1))
        e2e[m.group(1)] = sorted(set(re.findall(r'E2E-\d\d', cols[6])))
    return cls, e2e


# ------------------------------------------------------------------ PHPUnit
def phpunit_classes():
    """[(ruta relativa, clase, [métodos])] en orden de archivo."""
    out = []
    base = os.path.join(ROOT, 'tests')
    for dp, _, fs in os.walk(base):
        for f in fs:
            if f.endswith('Test.php'):
                p = os.path.join(dp, f)
                rel = os.path.relpath(p, ROOT).replace('\\', '/')
                out.append((rel, f[:-4], re.findall(r'function (test_[a-z0-9_]+)', _read(p))))
    return sorted(out)


def phpunit_junit():
    """{Clase::método: dict(n, passed, failed, skipped, assertions)} de la ejecución F29F (data providers sumados)."""
    res = {}
    root = ET.parse(os.path.join(EVID, 'phpunit-junit.xml')).getroot()
    for t in root.iter('testcase'):
        key = t.attrib['class'].split('\\')[-1] + '::' + re.sub(r' with data set .*$', '', t.attrib['name'])
        r = res.setdefault(key, dict(n=0, passed=0, failed=0, skipped=0, assertions=0))
        r['n'] += 1
        r['assertions'] += int(t.attrib.get('assertions', 0))
        if t.find('failure') is not None or t.find('error') is not None:
            r['failed'] += 1
        elif t.find('skipped') is not None:
            r['skipped'] += 1
        else:
            r['passed'] += 1
    return res


# ------------------------------------------------------------------ Cypress
def cypress_specs():
    """[(archivo, título del describe, [títulos de it])]."""
    out = []
    d = os.path.join(ROOT, 'cypress', 'e2e')
    for f in sorted(os.listdir(d)):
        if f.endswith('.cy.js'):
            src = _read(os.path.join(d, f))
            desc = re.search(r"describe\(\s*['\"`]([^'\"`]+)", src)
            its = re.findall(r"\bit\(\s*['\"`]([^'\"`]+)", src)
            out.append((f, desc.group(1) if desc else f, its))
    return out


def cypress_results():
    """{archivo: dict(tests, passing, failing, pending, skipped, duracion)} del resumen de la ejecución F29F."""
    txt = _read(os.path.join(EVID, '09-cypress.log'))
    table = txt[txt.rfind('(Run Finished)'):]
    res, pending_name = {}, None
    for line in table.splitlines():
        m = re.match(r'\s*│\s*(✔|✖)\s+(\S+)\s+(\S+)\s+(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s*│', line)
        if m:
            name = m.group(2)
            cont = re.match(r'\s*│\s+(\S+)\s+│', '')
            res[name] = dict(ok=m.group(1) == '✔', duracion=m.group(3), tests=int(m.group(4)),
                             passing=0 if m.group(5) == '-' else int(m.group(5)),
                             failing=0 if m.group(6) == '-' else int(m.group(6)),
                             pending=0 if m.group(7) == '-' else int(m.group(7)),
                             skipped=0 if m.group(8) == '-' else int(m.group(8)))
            pending_name = name
            continue
        m2 = re.match(r'\s*│\s{4}(\S+)\s+│', line)            # continuación de un nombre partido («.js»)
        if m2 and pending_name and not pending_name.endswith('.js'):
            res[pending_name + m2.group(1)] = res.pop(pending_name)
            pending_name = None
    total = re.search(r'(✔|✖)\s+All specs passed!\s+(\S+)\s+(\d+)\s+(\d+)', table) or \
        re.search(r'✖\s+\d+ of \d+ failed.*?(\S+)\s+(\d+)\s+(\d+)', table)
    return res, total


# ------------------------------------------------------------------ Vitest
def vitest_files():
    out = []
    for dp, _, fs in os.walk(os.path.join(ROOT, 'resources', 'js')):
        for f in fs:
            if re.search(r'\.test\.tsx?$', f):
                p = os.path.join(dp, f)
                src = _read(p)
                out.append((os.path.relpath(p, ROOT).replace('\\', '/'),
                            re.findall(r"\b(?:it|test)\(\s*['\"`]([^'\"`]+)", src)))
    return sorted(out)


def vitest_results():
    txt = _read(os.path.join(EVID, '07-vitest.log'))
    res = {m.group(2): dict(ok=m.group(1) == '✓', tests=int(m.group(3)))
           for m in re.finditer(r'(✓|×|✗)\s+(\S+\.test\.tsx?)\s+\((\d+) tests?', txt)}
    tot = re.search(r'Tests\s+(\d+) passed \((\d+)\)', txt)
    return res, tot


# ------------------------------------------------------------------ pytest
def pytest_files():
    d = os.path.join(ROOT, 'ml-service', 'tests')
    return [(f'ml-service/tests/{f}', re.findall(r'^def (test_[a-z0-9_]+)', _read(os.path.join(d, f)), re.M))
            for f in sorted(os.listdir(d)) if f.startswith('test_') and f.endswith('.py')]


def pytest_results():
    root = ET.parse(os.path.join(EVID, 'pytest-junit.xml')).getroot()
    res = {}
    for t in root.iter('testcase'):
        mod = 'ml-service/' + t.attrib['classname'].split('.')[0] + '/' + t.attrib['classname'].split('.')[1] + '.py'
        r = res.setdefault(mod, dict(n=0, passed=0, failed=0, skipped=0))
        r['n'] += 1
        if t.find('failure') is not None or t.find('error') is not None:
            r['failed'] += 1
        elif t.find('skipped') is not None:
            r['skipped'] += 1
        else:
            r['passed'] += 1
    return res


# ------------------------------------------------------------------ resumen de pasos
def pasos():
    """Filas del 00-resumen.tsv: paso, comando, inicio, fin, código de salida."""
    with open(os.path.join(EVID, '00-resumen.tsv'), encoding='utf-8') as f:
        rows = [r for r in csv.reader(f, delimiter='\t') if len(r) == 5 and r[0] != 'paso']
    return rows


def log(name):
    return _read(os.path.join(EVID, name))


def ci():
    """Ejecuciones de GitHub Actions por rama, tal como las devolvió la API (evidencias/ci-github-actions.json)."""
    import json
    return json.loads(_read(os.path.join(EVID, 'ci-github-actions.json')))


def ci_estado(rama):
    c = ci()['commits'][rama]
    runs = c['runs']
    if not runs:
        return None, c['sha']
    return runs[0], c['sha']
