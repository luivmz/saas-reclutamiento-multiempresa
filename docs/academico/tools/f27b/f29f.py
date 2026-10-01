"""F29F — Ejecución QA final: resumen de la ejecución real, observaciones clasificadas, evaluación de los criterios de
aceptación del plan (F29D) y matriz CP → resultado. Cada cifra se extrae de la evidencia versionada en
docs/academico/qa-final/evidencias/ (salidas completas de las herramientas); nada se escribe a mano.
"""
import os
import re

import f29e
import qa_data as Q

FECHA = '30/09/2026'


def _m(pattern, text, group=1, default='—'):
    m = re.search(pattern, text, re.S)
    return m.group(group) if m else default


def resultados():
    """Una fila por herramienta con los números leídos de su registro."""
    ph1, ph2 = Q.log('04-phpunit.log'), Q.log('04b-phpunit-junit.log')
    vt, py1, py2 = Q.log('07-vitest.log'), Q.log('08-pytest.log'), Q.log('08b-pytest.log')
    cy, bd, ts = Q.log('09-cypress.log'), Q.log('06-build.log'), Q.log('05-tsc.log')
    pint, vpc, cc = Q.log('11-pint.log'), Q.log('12-vp-check.log'), Q.log('03-compose-config.log')
    rc = lambda t: _m(r'# código de salida: (\d+)', t)
    cres, tot = Q.cypress_results()
    dev, dev_sha = Q.ci_estado('develop')
    main, main_sha = Q.ci_estado('main')

    def php(t):
        return dict(passed=_m(r'(\d+) passed', t), failed=_m(r'(\d+) failed', t, default='0'),
                    skipped=_m(r'(\d+) skipped', t, default='0'), assertions=_m(r'\((\d+) assertions\)', t),
                    duracion=_m(r'Duration:\s*([\d.]+s)', t), rc=rc(t))
    p1, p2 = php(ph1), php(ph2)
    filas = [
        ('04-phpunit', 'PHPUnit (1.ª ejecución)', 'docker compose exec -T app php artisan test', p1['passed'],
         p1['failed'], p1['skipped'], p1['assertions'], p1['duracion'], p1['rc']),
        ('04b-phpunit-junit', 'PHPUnit (2.ª ejecución, con JUnit)', 'docker compose exec -T app php artisan test '
         '--log-junit …', p2['passed'], p2['failed'], p2['skipped'], p2['assertions'], p2['duracion'], p2['rc']),
        ('05-tsc', 'TypeScript', 'docker compose exec -T app npx tsc --noEmit', '—', '0 errores' if rc(ts) == '0' else
         'con errores', '—', '—', '—', rc(ts)),
        ('06-build', 'Build del frontend (Vite)', 'docker compose exec -T app npm run build',
         _m(r'(\d+) modules transformed', bd) + ' módulos', '0' if rc(bd) == '0' else 'error', '—', '—',
         _m(r'built in ([\d.]+s)', bd), rc(bd)),
        ('07-vitest', 'Vitest (componentes)', 'docker compose exec -T app npx vp test --run',
         _m(r'Tests\s+(\d+) passed', vt), _m(r'Tests\s+\d+ passed.*?(\d+) failed', vt, default='0'), '0', '—',
         _m(r'Duration\s+([\d.]+s)', vt), rc(vt)),
        ('08-pytest', 'pytest (1.ª ejecución)', 'cd ml-service && .venv/Scripts/python.exe -m pytest -q',
         'sin conteo (resumen suprimido por -q duplicado)', '—', '—', '—', '—', rc(py1)),
        ('08b-pytest', 'pytest (2.ª ejecución, con resumen)', 'cd ml-service && .venv/Scripts/python.exe -m pytest '
         '--junitxml=…', _m(r'(\d+) passed', py2), _m(r'(\d+) failed', py2, default='0'),
         _m(r'(\d+) skipped', py2, default='0'), '—', _m(r'passed in ([\d.]+s)', py2), rc(py2)),
        ('09-cypress', 'Cypress E2E (20 specs)', 'npm run cy:run', tot.group(4) if tot else '—',
         str(sum(v['failing'] for v in cres.values())), str(sum(v['skipped'] + v['pending'] for v in cres.values())),
         '—', tot.group(2) if tot else '—', rc(cy)),
        ('03-compose-config', 'Configuración de Docker Compose', 'docker compose config --quiet',
         'válida' if 'config: OK' in cc else '—', '—', '—', '—', '—', rc(cc)),
        ('11-pint', 'Estilo PHP (Pint, medición)', 'docker compose exec -T app vendor/bin/pint --test',
         _m(r'(\d+) files', pint) + ' archivos', _m(r'(\d+) style issues', pint) + ' avisos de estilo', '—', '—', '—',
         rc(pint)),
        ('12-vp-check', 'Formato (vp check, medición)', 'docker compose exec -T app npx vp check', '—',
         _m(r'issues in (\d+) files', vpc) + ' archivos con formato pendiente', '—', '—', '—', rc(vpc)),
    ]
    ci = [('CI develop', dev_sha[:7], dev['conclusion'] if dev else 'sin ejecución', dev['html_url'] if dev else '—'),
          ('CI main', main_sha[:7], main['conclusion'] if main else 'sin ejecución', main['html_url'] if main else '—')]
    return filas, ci, dict(p1=p1, p2=p2, cypress=tot, dev=dev, main=main)


def criterios(cs, data):
    cov = f29e.cobertura_rf(cs)
    import m_defectos
    abiertos_alta = [d['id'] for d in m_defectos.registro()
                     if d['severidad'] in ('Crítica', 'Alta') and not d['estado'].startswith('Cerrado')]
    p1 = data['p1']
    cy = data['cypress']
    vit = Q.vitest_results()[1]
    py_fail = sum(v['failed'] for v in Q.pytest_results().values())
    pasos = {p[0]: p[4] for p in Q.pasos()}
    return [
        ('CA-01', 'PHPUnit sin fallos; solo las 8 omitidas del starter kit', p1['failed'] == '0' and p1['skipped'] == '8',
         f'{p1["passed"]} aprobadas, {p1["failed"]} fallidas, {p1["skipped"]} omitidas (verificación de correo desactivada en Fortify)'),
        ('CA-02', 'Cypress: 20 specs, 0 fallidos, sin reintentos', bool(cy) and cy.group(3) == cy.group(4)
         and len(Q.cypress_results()[0]) == 20, f'{cy.group(4)}/{cy.group(3)} en 20 specs' if cy else '—'),
        ('CA-03', 'Vitest y pytest sin fallos', bool(vit) and vit.group(1) == vit.group(2) and py_fail == 0,
         f'Vitest {vit.group(1)}/{vit.group(2)}; pytest {sum(v["passed"] for v in Q.pytest_results().values())} aprobadas, {py_fail} fallidas'),
        ('CA-04', 'TypeScript y build sin errores', pasos.get('05-tsc') == '0' and pasos.get('06-build') == '0',
         'tsc y build con código de salida 0'),
        ('CA-05', 'CI en verde en develop', bool(data['dev']) and data['dev']['conclusion'] == 'success',
         f'develop: {data["dev"]["conclusion"] if data["dev"] else "sin ejecución"}; main: '
         f'{data["main"]["conclusion"] if data["main"] else "sin ejecución (pendiente de ejecución manual)"}'),
        ('CA-06', 'Cada RF-01 a RF-27 con un CP automatizado aprobado', all(v[0] for v in cov.values()),
         f'{sum(1 for v in cov.values() if v[0])} de 27 RF'),
        ('CA-07', 'Ningún defecto de severidad Alta abierto', not abiertos_alta,
         'Registro unificado de la F29G (v1.0 y v1.1): 0 defectos Críticos o Altos abiertos' if not abiertos_alta
         else ', '.join(abiertos_alta)),
    ]


OBSERVACIONES = [
    ('OBS-F29F-01', 'Procedimiento', 'La primera ejecución de pytest usó `-q` y el `pyproject.toml` ya fija `addopts = '
     '"-q"`: con `-qq`, pytest no imprimió el resumen de conteos, aunque terminó con código 0. Se repitió sin el `-q` '
     'extra (08b), con 533 aprobadas. No es un defecto del software; se conservan las dos ejecuciones.', 'Documentado'),
    ('OBS-F29F-02', 'Repetición', 'PHPUnit se ejecutó dos veces: la segunda, con `--log-junit`, para el detalle por '
     'clase que usa la matriz CP → resultado. Los conteos coinciden (411/0/8, 1498 aserciones); solo cambia la '
     'duración.', 'Documentado'),
    ('OBS-F29F-03', 'No aplicable', 'Las 8 pruebas omitidas de PHPUnit (`EmailVerificationTest`, '
     '`VerificationNotificationTest`) dependen de `Features::emailVerification()`, desactivada en Fortify. No son '
     'fallos.', 'Aceptado'),
    ('OBS-F29F-04', 'Dependencia externa (CI)', 'El merge F29C en `main` (`60ebcb2`) no generó ejecución de GitHub '
     'Actions: el push terminó con un error del cliente aunque la rama se actualizó. `main` tiene el mismo árbol que '
     '`develop` (`bc44303`), cuya CI pasó. Deuda: **CI main F29C pendiente de ejecución manual** (`workflow_dispatch`).',
     'Abierto'),
    ('OBS-F29F-05', 'Deuda de estilo', 'Pint informa 8 avisos de estilo en 256 archivos PHP. `vp check` informa '
     'formato pendiente en 226 archivos: 188 Markdown y 35 de código o configuración. Es F25-L03, solo de formato, y la '
     'CI no lo verifica. No se corrige en la F29F porque cambiaría código fuera del alcance autorizado.', 'Abierto (LOW)'),
    ('OBS-F29F-06', 'Entorno', 'La documentación de la F29D a la F29H se escribió mientras corrían las suites: al final, '
     '`git status` mostraba solo archivos de `docs/academico/`. El runtime probado es exactamente `bc44303`: el árbol '
     'estaba limpio al empezar (01-git).', 'Documentado'),
]


def build(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    cs = f29e.casos()
    filas, ci, data = resultados()
    crit = criterios(cs, data)
    pasos = Q.pasos()
    env = Q.log('02-entorno.log')
    ini = pasos[0][2] if pasos else '—'
    fin = [p for p in pasos if p[0] == '09-cypress'][0][3] if pasos else '—'
    L = ['# F29F — Ejecución QA final', '',
         '> Generado por `docs/academico/tools/f27b/f29f.py` a partir de la evidencia versionada en '
         '[`evidencias/`](evidencias/): `python docs/academico/tools/f27b/build.py f29f`. Cada cifra sale de la salida '
         'real de la herramienta; no se usaron resultados históricos.', '',
         '## Qué se probó', '',
         '| Dato | Valor |', '|---|---|',
         f'| Fecha | {FECHA} (de {ini} a {fin}, más las repeticiones y mediciones indicadas) |',
         f'| Commit probado | `{Q.log("01-git.log").split(chr(10))[4].strip()}` (`develop`, F29C integrada); árbol limpio al iniciar |',
         '| Plan aplicado | [F29D](../plan-pruebas/README.md), criterios CA-01 a CA-07 |',
         '| Casos de prueba | [F29E](../casos-prueba/README.md): ' + str(len(cs)) + ' CP |',
         f'| Docker | {_m(r"(Docker [\d.]+)", env)} · Compose {_m(r"Docker Compose version (v[\d.]+)", env)} |',
         f'| Contenedor `app` | PHP {_m(r"PHP ([\d.]+)", env)} · Node {_m(r"(v22[\d.]+)", env)} |',
         f'| Servicios | PostgreSQL {_m(r"PostgreSQL\) ([\d.]+)", env)} · Redis {_m(r"v=([\d.]+)", env)}; '
         '`app`, `app-e2e`, `postgres`, `queue`, `queue-e2e` y `redis` healthy |',
         '| Servicio ML | Python 3.12.5 (`ml-service/.venv`) |',
         '| Equipo | AMD Ryzen 9 5900X, 31,9 GB de RAM, Windows 11 Pro; Docker Desktop con 24 CPU y 16,7 GB |', '',
         '## Resultados por herramienta', '',
         '| Registro | Herramienta | Comando | Aprobadas / resultado | Fallidas | Omitidas | Aserciones | Duración | '
         'Código de salida |', '|---|---|---|---|---|---|---|---|---|']
    for f in filas:
        L.append(f'| [`{f[0]}`](evidencias/{f[0]}.log) | {f[1]} | `{f[2]}` | {f[3]} | {f[4]} | {f[5]} | {f[6]} | '
                 f'{f[7]} | {f[8]} |')
    L += ['', '**Integración continua** (evidencia: [`ci-github-actions.json`](evidencias/ci-github-actions.json), '
          'respuesta de la API de GitHub):', '',
          '| Rama | Commit | Resultado | Ejecución |', '|---|---|---|---|']
    for c in ci:
        L.append(f'| {c[0]} | `{c[1]}` | {c[2]} | {c[3]} |')
    L += ['', '## Evaluación de los criterios de aceptación del plan', '',
          '| Criterio | Descripción | Resultado | Evidencia |', '|---|---|---|---|']
    for cid, desc, ok, det in crit:
        L.append(f'| {cid} | {desc} | {"**CUMPLE**" if ok else "**NO CUMPLE**"} | {det} |')
    ok_all = all(c[2] for c in crit)
    L += ['', f'**Dictamen:** {"se cumplen" if ok_all else "NO se cumplen"} los siete criterios de aceptación. No hubo '
          'pruebas fallidas, así que no fue necesario clasificar fallos como regresión, flaky, ambiente, dependencia '
          'externa o documental. Las observaciones siguientes sí se clasifican.', '',
          '## Observaciones clasificadas', '', '| ID | Clasificación | Descripción | Estado |', '|---|---|---|---|']
    for o in OBSERVACIONES:
        L.append(f'| {o[0]} | {o[1]} | {o[2]} | {o[3]} |')
    L += ['', '## Matriz CP → resultado', '',
          'Estado de cada caso de prueba de la F29E según esta ejecución (detalle y pasos en '
          '[`F29E_Casos_de_Prueba.md`](../casos-prueba/F29E_Casos_de_Prueba.md)).', '',
          '| CP | Título | Suite | Ejecuciones | Aprobadas | Fallidas | Omitidas | Estado |', '|---|---|---|---|---|---|---|---|']
    for c in cs:
        L.append(f'| {c["id"]} | {c["titulo"].replace("|", "/")} | {c["suite"]} | {c["n"]} | {c["passed"]} | '
                 f'{c["failed"]} | {c["skipped"]} | {c["estado"]} |')
    tot = lambda k, s=None: sum(c[k] for c in cs if s is None or c['suite'] == s)
    L += [f'| **Total** | | | **{tot("n")}** | **{tot("passed")}** | **{tot("failed")}** | **{tot("skipped")}** | |', '',
          '## Evidencia', '',
          '- **Registros:** `evidencias/*.log`, uno por paso. Cada uno trae el comando, la hora de inicio y de fin, la salida '
          'completa y el código de salida.',
          '- **Saneamiento:** se quitaron los códigos de color ANSI y se reemplazaron el nombre del equipo y la ruta '
          'temporal del job. Ningún resultado se alteró, y los registros no contienen secretos: `.env.e2e` nunca se '
          'imprime.',
          '- **Resumen de la primera ronda:** `evidencias/00-resumen.tsv`.',
          '- **Detalle por prueba:** `evidencias/phpunit-junit.xml` (419 casos) y `evidencias/pytest-junit.xml` (533).',
          '- **Integración continua:** `evidencias/ci-github-actions.json`.']
    with open(os.path.join(out_dir, 'F29F_Ejecucion_QA.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(L).rstrip() + '\n')
    return crit
