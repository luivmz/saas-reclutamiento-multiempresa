"""F29E — Casos de prueba (CP-001…) y matriz de trazabilidad RF → CU → CP → prueba automatizada → evidencia.

Los casos se derivan del código de pruebas real y de la matriz maestra; ninguno se escribe a mano:
- PHPUnit: un CP por clase de prueba y conjunto de RF del nombre del método (`test_rf10_rf11_…` → RF-10, RF-11). Los
  métodos sin prefijo RF de una clase forman un CP con los RF que la matriz maestra asigna a esa clase o, si no tiene,
  quedan como transversales (seguridad, multitenencia, ML, soporte);
- Cypress, Vitest y pytest: un CP por spec o archivo;
- verificaciones estáticas (TypeScript, build, Compose) y CI: un CP cada una;
- casos manuales: solo los que tienen evidencia histórica o que se declaran NO EJECUTADOS.
El estado sale de la ejecución F29F (evidencia en docs/academico/qa-final/evidencias/).
"""
import csv
import io
import os
import re

import m_cu as U
import m_rf as R
import qa_data as Q

RF_NOMBRE = {r[0]: r[1] for r in R.RF}
BASE = [f'RF-{i:02d}' for i in range(1, 28)]
AUTO, MANUAL = 'AUTOMATIZADA', 'MANUAL / NO AUTOMATIZADO'
PRE_PHP = ('Contenedores `app` y `postgres` en estado healthy; base aislada `reclutamiento_testing`; cada prueba crea sus '
           'datos con fábricas y `RefreshDatabase`')
DATOS_FICTICIOS = 'Ficticios: organizaciones, usuarios por rol y registros creados por fábricas'
ALTA_RF = {'RF-03', 'RF-21', 'RF-22', 'RF-23', 'RF-24', 'RF-25', 'RF-27'}

# Clases sin RF en la matriz maestra ni en sus métodos: tipo y referencia transversal (del propio código de prueba).
TRANSVERSAL = {
    'Tenancy': ('Multitenencia', 'RNF-02'), 'Auth': ('Seguridad básica', 'RNF-01'),
    'Settings': ('Seguridad básica', 'RNF-01'), 'Testing': ('Seguridad básica', 'RNF-01; regresión de DEF-13'),
    'Routing': ('Seguridad básica', 'RNF-01'), 'Ml': ('ML experimental', 'RF-29 (EXPERIMENTAL / PROPUESTO)'),
    'Frontend': ('Regresión', 'Regresión de DEF-09 (zona horaria)'), 'Audit': ('Integración / funcional', 'RF-27'),
}


def cu_of(rfs):
    return sorted({c[0] for c in U.CU if set(c[4]) & set(rfs)})


def _tipo(rel, rfs):
    parts = rel.split('/')
    if parts[1] == 'Unit':
        return 'Unitaria'
    area = parts[2] if len(parts) > 3 else ''
    if area in TRANSVERSAL and area != 'Audit':
        return TRANSVERSAL[area][0]
    return 'Integración / funcional'


def _prioridad(tipo, rfs):
    if tipo in ('Seguridad básica', 'Multitenencia') or set(rfs) & ALTA_RF:
        return 'Alta'
    if rfs or tipo in ('ML experimental', 'Unitaria', 'Regresión'):
        return 'Media'
    return 'Baja'


def _estado(passed, failed, skipped, n):
    if n == 0:
        return 'NO EJECUTADO'
    if failed:
        return 'FALLIDO'
    if skipped == n:
        return 'OMITIDO (función del starter kit desactivada)'
    return 'APROBADO' if not skipped else 'APROBADO CON OMITIDAS'


def casos():
    cls_rf, rf_e2e = Q.traceability()
    junit = Q.phpunit_junit()
    out = []

    # ---------------------------------------------------------- PHPUnit
    php = []
    for rel, cls, methods in Q.phpunit_classes():
        grupos = {}
        for m in methods:
            grupos.setdefault(Q.rf_tokens(m), []).append(m)
        for toks, ms in grupos.items():
            rfs = list(toks) if toks else sorted(cls_rf.get(cls, ()))
            tipo = _tipo(rel, rfs)
            area = rel.split('/')[2] if rel.count('/') > 2 else ''
            ref = '' if rfs else TRANSVERSAL.get(area, ('', 'Transversal'))[1]
            if cls == 'ExampleTest':
                tipo, ref = 'Regresión', 'Prueba de humo del starter kit'
            r = [junit.get(f'{cls}::{m}', dict(n=0, passed=0, failed=0, skipped=0, assertions=0)) for m in ms]
            n, ok, ko, sk = (sum(x[k] for x in r) for k in ('n', 'passed', 'failed', 'skipped'))
            if toks:
                titulo = ' / '.join(RF_NOMBRE[x] for x in rfs)
            elif rfs:
                titulo = f'Reglas complementarias de {cls} ({", ".join(rfs)})'
            else:
                titulo = f'{ref} — {cls}'
            php.append(dict(
                rfs=rfs, titulo=titulo, tipo=tipo, ref=ref, cu=cu_of(rfs),
                objetivo=f'Verificar {("«" + titulo + "»") if rfs else ref} con {len(ms)} prueba(s) automatizada(s) de `{cls}`.',
                pre=PRE_PHP, datos=DATOS_FICTICIOS,
                pasos=[f'`{m}`: {Q.humanize(m)}' for m in ms],
                esperado=f'Las {n} ejecuciones terminan sin fallos: se cumple cada comportamiento de los pasos.',
                prioridad=_prioridad(tipo, rfs), auto=AUTO, prueba=f'{rel} ({len(ms)} métodos)',
                comando=f'docker compose exec app php artisan test --filter={cls}',
                evidencia=f'{Q.EVID_REL}/04-phpunit.log; {Q.EVID_REL}/phpunit-junit.xml',
                n=n, passed=ok, failed=ko, skipped=sk, estado=_estado(ok, ko, sk, n), suite='PHPUnit'))
    # Orden: primero los casos con RF (por el primer RF), después los transversales, cada grupo por archivo.
    php.sort(key=lambda c: (0 if c['rfs'] else 1, c['rfs'][0] if c['rfs'] else c['tipo'], c['prueba']))
    out += php

    # ---------------------------------------------------------- Cypress
    cres, _ = Q.cypress_results()
    e2e_rf = {}
    for rf, specs in rf_e2e.items():
        for s in specs:
            e2e_rf.setdefault(s, set()).add(rf)
    for f, desc, its in Q.cypress_specs():
        m = re.match(r'e2e-(\d\d)', f)
        eid = f'E2E-{m.group(1)}'
        rfs = sorted(e2e_rf.get(eid, set()) | {x.replace('–', '-') for x in re.findall(r'RF-\d\d', desc) if x in BASE})
        num = int(m.group(1))
        if num in (14, 15):
            tipo, ref = 'ML experimental', 'RF-29 (EXPERIMENTAL / PROPUESTO)'
        elif num == 0:
            tipo, ref = 'Regresión', 'Regresión de DEF-12 (fechas en la zona horaria de la aplicación)'
        elif num >= 16:
            tipo, ref = 'UI / E2E (accesibilidad)', 'RNF-05 (usabilidad y accesibilidad)'
        elif num == 11:
            tipo, ref = 'Multitenencia', 'RNF-02'
        elif num == 12:
            tipo, ref = 'Seguridad básica', 'RNF-01'
        elif num == 13:
            tipo, ref = 'Aceptación (flujo completo)', ''
        else:
            tipo, ref = 'UI / E2E', ''
        r = cres.get(f, {})
        n = r.get('tests', 0)
        out.append(dict(
            rfs=rfs, titulo=f'{eid} · {desc}', tipo=tipo, ref=ref, cu=cu_of(rfs),
            objetivo=f'Verificar en navegador el comportamiento de «{desc}».',
            pre='Entorno aislado `app-e2e` y `queue-e2e` healthy; base `reclutamiento_e2e` reiniciada por la prueba '
                '(`POST /__e2e/reset`); Cypress 15.3.0 (Electron 136, 1280×800)',
            datos='Ficticios: `DemoSeeder` (usuarios demo `.test`, ver docs/demo-users.md) y fixtures de Cypress',
            pasos=[f'it: {t}' for t in its] + (['(algunas pruebas se generan en bucle: el total ejecutado es mayor que '
                                                'los `it` del código)'] if n > len(its) else []),
            esperado=f'Los {n} tests del spec pasan sin reintentos.',
            prioridad=_prioridad(tipo, rfs), auto=AUTO, prueba=f'cypress/e2e/{f}',
            comando=f'npm run cy:run -- --spec cypress/e2e/{f}',
            evidencia=f'{Q.EVID_REL}/09-cypress.log', n=n, passed=r.get('passing', 0), failed=r.get('failing', 0),
            skipped=r.get('skipped', 0) + r.get('pending', 0),
            estado=_estado(r.get('passing', 0), r.get('failing', 0), r.get('skipped', 0), n), suite='Cypress'))

    # ---------------------------------------------------------- Vitest
    vres, _ = Q.vitest_results()
    for rel, its in Q.vitest_files():
        r = vres.get(rel, {})
        n = r.get('tests', 0)
        name = os.path.basename(rel).replace('.test.tsx', '')
        out.append(dict(
            rfs=[], titulo=f'Componente de interfaz «{name}»', tipo='UI / componentes', ref='RNF-05 (usabilidad)',
            cu=[], objetivo=f'Verificar el componente «{name}» de forma aislada (renderizado, accesibilidad y estados).',
            pre='Contenedor `app` healthy; entorno de pruebas de Vitest', datos='Propiedades ficticias del componente',
            pasos=[f'test: {t}' for t in its], esperado=f'Las {n} pruebas del archivo pasan.',
            prioridad='Baja', auto=AUTO, prueba=rel, comando='docker compose exec app npx vp test --run',
            evidencia=f'{Q.EVID_REL}/07-vitest.log', n=n, passed=n if r.get('ok') else 0,
            failed=0 if r.get('ok', False) else n, skipped=0, estado=_estado(n if r.get('ok') else 0, 0 if r.get('ok') else n, 0, n),
            suite='Vitest'))

    # ---------------------------------------------------------- pytest (ML experimental)
    pres = Q.pytest_results()
    for rel, funcs in Q.pytest_files():
        r = pres.get(rel, dict(n=0, passed=0, failed=0, skipped=0))
        name = os.path.basename(rel)[5:-3].replace('_', ' ')
        out.append(dict(
            rfs=[], titulo=f'Servicio ML: {name}', tipo='ML experimental', ref='RF-29 (EXPERIMENTAL / PROPUESTO)', cu=[],
            objetivo=f'Verificar «{name}» del servicio de riesgo operacional, que no evalúa ni clasifica personas.',
            pre='Entorno virtual `ml-service/.venv` (Python 3.12.5)', datos='Dataset sintético del experimento; sin PII',
            pasos=[f'`{t}`' for t in funcs], esperado=f'Las {r["n"]} ejecuciones pasan.', prioridad='Media', auto=AUTO,
            prueba=rel, comando='cd ml-service && .venv/Scripts/python.exe -m pytest ' + rel.split('/', 1)[1],
            evidencia=f'{Q.EVID_REL}/08b-pytest.log; {Q.EVID_REL}/pytest-junit.xml', n=r['n'], passed=r['passed'],
            failed=r['failed'], skipped=r['skipped'], estado=_estado(r['passed'], r['failed'], r['skipped'], r['n']),
            suite='pytest'))

    # ---------------------------------------------------------- estáticas, entorno y CI
    pasos_ok = {p[0]: p[4] == '0' for p in Q.pasos()}
    for paso, titulo, cmd, esperado in [
        ('05-tsc', 'Tipos de TypeScript del frontend', 'docker compose exec app npx tsc --noEmit', '0 errores de tipos'),
        ('06-build', 'Compilación del frontend', 'docker compose exec app npm run build', 'Build terminado sin errores'),
        ('03-compose-config', 'Configuración de Docker Compose', 'docker compose config --quiet', 'Configuración válida'),
    ]:
        ok = pasos_ok.get(paso)
        out.append(dict(
            rfs=[], titulo=titulo, tipo='Estática / build', ref='RNF-09 (mantenibilidad)', cu=[],
            objetivo=f'Verificar: {titulo.lower()}.', pre='Contenedores healthy', datos='No aplica',
            pasos=[f'Ejecutar `{cmd}`'], esperado=esperado, prioridad='Media', auto=AUTO, prueba=cmd, comando=cmd,
            evidencia=f'{Q.EVID_REL}/{paso}.log', n=1, passed=1 if ok else 0, failed=0 if ok else 1, skipped=0,
            estado='APROBADO' if ok else 'FALLIDO', suite='Estática'))
    dev, dev_sha = Q.ci_estado('develop')
    main, main_sha = Q.ci_estado('main')
    dev_ok = bool(dev) and dev['conclusion'] == 'success'
    ci_estado = ('APROBADO' if dev_ok else 'FALLIDO') + f' en develop ({dev_sha[:7]})' + (
        '; main (' + main_sha[:7] + '): ' + (main['conclusion'] if main else 'sin ejecución — pendiente de ejecución manual'))
    out.append(dict(
        rfs=[], titulo='Integración continua (GitHub Actions `tests`)', tipo='Regresión / CI', ref='RNF-09', cu=[],
        objetivo='Verificar que cada push a `develop` y `main` ejecuta build, TypeScript y PHPUnit en verde.',
        pre='Push a `develop` o `main`', datos='Los de PHPUnit', pasos=['Consultar la ejecución del workflow `tests` del '
                                                                          'commit probado'],
        esperado='Ejecución `success`', prioridad='Alta', auto=AUTO, prueba='.github/workflows/tests.yml',
        comando='GitHub Actions (automático)', evidencia=f'{Q.EVID_REL}/ci-github-actions.json', n=1,
        passed=1 if dev_ok else 0, failed=0 if dev_ok else 1, skipped=0, estado=ci_estado, suite='CI'))

    # ---------------------------------------------------------- manuales
    for titulo, tipo, ref, objetivo, estado, evid in [
        ('Recorrido visual por rol en navegador', 'Aceptación (manual)', 'RNF-05',
         'Recorrer las pantallas de cada rol y detectar errores visibles, HTTP o de JavaScript.',
         'EJECUTADO EN LA FASE 8 (13/09/2026): 10/10; no repetido en la F29F', 'docs/manual-smoke-test.md'),
        ('Aceptación por el usuario institucional (RR. HH. / Dirección del Colegio)', 'Aceptación (manual)', 'Validación institucional',
         'Confirmar con el Colegio que el TO-BE y el sistema responden a su proceso real.',
         'NO EJECUTADO: sin validación institucional (fuera de alcance)', '—'),
        ('Rendimiento y carga', 'No funcional', 'RNF-06',
         'Medir tiempos de respuesta con usuarios concurrentes frente a un objetivo definido.',
         'NO EJECUTADO: sin herramienta de carga ni SLA (RNF-06 NO VERIFICADO)', '—'),
        ('Disponibilidad y recuperación', 'No funcional', 'RNF-07',
         'Verificar la continuidad del servicio y la restauración desde respaldos.',
         'NO EJECUTADO: sin entorno de producción (RNF-07 NO VERIFICADO)', '—'),
    ]:
        out.append(dict(rfs=[], titulo=titulo, tipo=tipo, ref=ref, cu=[], objetivo=objetivo,
                        pre='Según el caso', datos='Ficticios', pasos=['Procedimiento manual'], esperado=objetivo,
                        prioridad='Media', auto=MANUAL, prueba='—', comando='—', evidencia=evid, n=0, passed=0,
                        failed=0, skipped=0, estado=estado, suite='Manual'))

    for i, c in enumerate(out, 1):
        c['id'] = f'CP-{i:03d}'
    return out


def cobertura_rf(cs):
    """RF → (CP automatizados aprobados, todos los CP)."""
    res = {}
    for rf in BASE:
        todos = [c['id'] for c in cs if rf in c['rfs']]
        ok = [c['id'] for c in cs if rf in c['rfs'] and c['auto'] == AUTO and c['estado'].startswith('APROBADO')]
        res[rf] = (ok, todos)
    return res


# ------------------------------------------------------------------ salidas
def _md(x):
    return str(x).replace('|', '\\|').replace('\n', '<br>')


def build(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    cs = casos()
    cov = cobertura_rf(cs)
    # Catálogo completo.
    L = ['# F29E — Casos de prueba', '',
         '> Generado por `docs/academico/tools/f27b/f29e.py` desde el código de pruebas, la matriz maestra y la evidencia '
         'de la F29F: `python docs/academico/tools/f27b/build.py f29e`. No se edita a mano.', '',
         '## Resumen', '',
         '| Suite | CP | Ejecuciones | Aprobadas | Fallidas | Omitidas |', '|---|---|---|---|---|---|']
    for s in ('PHPUnit', 'Cypress', 'Vitest', 'pytest', 'Estática', 'CI', 'Manual'):
        sub = [c for c in cs if c['suite'] == s]
        L.append(f'| {s} | {len(sub)} | {sum(c["n"] for c in sub)} | {sum(c["passed"] for c in sub)} | '
                 f'{sum(c["failed"] for c in sub)} | {sum(c["skipped"] for c in sub)} |')
    L += [f'| **Total** | **{len(cs)}** | {sum(c["n"] for c in cs)} | {sum(c["passed"] for c in cs)} | '
          f'{sum(c["failed"] for c in cs)} | {sum(c["skipped"] for c in cs)} |', '',
          '**Criterios del catálogo:**', '',
          '- **Tipo:**',
          '  - unitaria (`tests/Unit`);',
          '  - integración / funcional (`tests/Feature` de negocio);',
          '  - seguridad básica (autenticación, roles, soporte E2E, rutas);',
          '  - multitenencia;',
          '  - UI / E2E (Cypress);',
          '  - UI / componentes (Vitest);',
          '  - ML experimental (pytest, `tests/Feature/Ml` y E2E-14/15);',
          '  - estática / build;',
          '  - regresión / CI;',
          '  - aceptación;',
          '  - no funcional.',
          '- **Prioridad:**',
          '  - Alta: seguridad, multitenencia, CI o RF de decisión, cierre y auditoría (RF-03, RF-21 a RF-25 y RF-27).',
          '  - Media: el resto de RF, las unitarias, el ML y la regresión.',
          '  - Baja: componentes visuales y accesibilidad.',
          '- **Automatización:** `AUTOMATIZADA` solo si existe la prueba en el repositorio. En otro caso, `MANUAL / NO '
          'AUTOMATIZADO`.',
          '- **Estado:** sale de la ejecución F29F. Un caso manual sin ejecución queda `NO EJECUTADO`, con su razón.', '',
          '## Catálogo', '']
    for c in cs:
        L += [f'### {c["id"]} — {c["titulo"]}', '',
              '| Campo | Valor |', '|---|---|',
              f'| RF relacionado | {", ".join(c["rfs"]) or "—"} |',
              f'| CU relacionado | {", ".join(c["cu"]) or "—"} |',
              f'| Referencia transversal | {c["ref"] or "—"} |',
              f'| Objetivo | {_md(c["objetivo"])} |',
              f'| Precondiciones | {_md(c["pre"])} |',
              f'| Datos | {_md(c["datos"])} |',
              f'| Pasos | {"<br>".join(f"{i}. {_md(p)}" for i, p in enumerate(c["pasos"], 1))} |',
              f'| Resultado esperado | {_md(c["esperado"])} |',
              f'| Tipo de prueba | {c["tipo"]} |',
              f'| Prioridad | {c["prioridad"]} |',
              f'| Automatización | {c["auto"]} |',
              f'| Prueba automática asociada | `{c["prueba"]}` |' if c['prueba'] != '—' else '| Prueba automática asociada | — |',
              f'| Comando | `{c["comando"]}` |' if c['comando'] != '—' else '| Comando | — |',
              f'| Evidencia | {c["evidencia"]} |',
              f'| Estado (F29F) | **{c["estado"]}** ({c["passed"]}/{c["n"]} aprobadas{", " + str(c["skipped"]) + " omitidas" if c["skipped"] else ""}) |', '']
    with open(os.path.join(out_dir, 'F29E_Casos_de_Prueba.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(L).rstrip() + '\n')

    # Matriz de trazabilidad RF → CU → CP → prueba → evidencia.
    T = ['# F29E — Matriz de trazabilidad RF → CU → CP → prueba automatizada → evidencia', '',
         '> Generada por `f29e.py`, igual que el catálogo ([`F29E_Casos_de_Prueba.md`](F29E_Casos_de_Prueba.md)). Los CU '
         'se derivan de los RF con la tabla del Formato 08. Las columnas de pruebas y evidencia remiten a archivos '
         'reales.', '',
         '## Cobertura de RF-01 a RF-27', '',
         '| RF | Requerimiento | CU | CP automatizados aprobados | Todos los CP | Pruebas automatizadas | Evidencia |',
         '|---|---|---|---|---|---|---|']
    for rf in BASE:
        ok, todos = cov[rf]
        pruebas = sorted({c['prueba'].split(' (')[0] for c in cs if rf in c['rfs'] and c['auto'] == AUTO})
        evid = sorted({e.strip() for c in cs if rf in c['rfs'] for e in c['evidencia'].split(';')})
        T.append(f'| {rf} | {RF_NOMBRE[rf]} | {", ".join(cu_of([rf])) or "—"} | {", ".join(ok) or "**NINGUNO**"} | '
                 f'{", ".join(todos)} | {"<br>".join("`" + p + "`" for p in pruebas)} | {"<br>".join(evid)} |')
    sin = [rf for rf in BASE if not cov[rf][0]]
    cus = sorted({cu for rf in BASE for cu in cu_of([rf]) if cov[rf][0]})
    T += ['', f'**Resultado:** {27 - len(sin)} de 27 RF con al menos un CP automatizado aprobado'
          + (f'; sin cobertura: {", ".join(sin)}' if sin else '') + f'. CU cubiertos a través de sus RF: {len(cus)} de 20.', '',
          '## Casos transversales y fuera de la línea base', '',
          '| CP | Título | Tipo | Referencia | Estado |', '|---|---|---|---|---|']
    for c in cs:
        if not c['rfs']:
            T.append(f'| {c["id"]} | {_md(c["titulo"])} | {c["tipo"]} | {c["ref"] or "—"} | {c["estado"]} |')
    with open(os.path.join(out_dir, 'F29E_Matriz_Trazabilidad.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(T).rstrip() + '\n')

    # CSV para hojas de cálculo.
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator='\n')
    w.writerow(['ID', 'Título', 'RF', 'CU', 'Referencia', 'Tipo', 'Prioridad', 'Automatización', 'Prueba automática',
                'Comando', 'Evidencia', 'Ejecuciones', 'Aprobadas', 'Fallidas', 'Omitidas', 'Estado'])
    for c in cs:
        w.writerow([c['id'], c['titulo'], ' '.join(c['rfs']), ' '.join(c['cu']), c['ref'], c['tipo'], c['prioridad'],
                    c['auto'], c['prueba'], c['comando'], c['evidencia'], c['n'], c['passed'], c['failed'],
                    c['skipped'], c['estado']])
    with open(os.path.join(out_dir, 'F29E_Casos_de_Prueba.csv'), 'w', encoding='utf-8', newline='') as f:
        f.write(buf.getvalue())
    return cs
