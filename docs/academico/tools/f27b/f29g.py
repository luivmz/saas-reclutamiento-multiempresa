"""F29G — Registro final de defectos y métricas de calidad.

Solo se calculan métricas con datos existentes: la ejecución F29F, los casos de la F29E, el registro de defectos
(m_defectos.py, leído de los documentos reales) y el estado de los RNF del F7. No se mide cobertura de código: el
contenedor no tiene Xdebug ni PCOV y el proyecto nunca la midió. ISO/IEC 25010 se usa como marco, sin certificación.
"""
import collections
import os
import re

import f29e
import m_defectos as MD
import m_rnf as N
import qa_data as Q


def _pct(a, b):
    return f'{100 * a / b:.1f} %'.replace('.', ',') if b else '—'


def _f25():
    """Conteos de la QA de release F25 («tras los arreglos»), leídos de docs/v1.1/phase-25-final-qa.md."""
    with open(os.path.join(Q.ROOT, 'docs', 'v1.1', 'phase-25-final-qa.md'), encoding='utf-8') as f:
        t = f.read()
    return dict(phpunit=re.search(r'\*\*(\d+) passed · (\d+) skipped · (\d+) failed · (\d+) assertions', t).groups(),
                pytest=re.search(r'\*\*(\d+) passed · [\d,]+ s\*\*', t).group(1),
                vitest=re.search(r'\*\*(\d+) passed\*\* \|', t).group(1),
                cypress=re.search(r'\*\*20 specs · (\d+)/(\d+)', t).groups())


def build(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    cs = f29e.casos()
    defs = MD.registro()
    L = ['# F29G — Defectos y métricas de calidad', '',
         '> Generado por `docs/academico/tools/f27b/f29g.py`: `python docs/academico/tools/f27b/build.py f29g`. Los '
         'defectos se leen de sus registros reales y las métricas se calculan con la evidencia de la F29F y los casos de '
         'la F29E. Si un dato no existe, la métrica no se calcula.', '',
         '## 1. Registro final de defectos', '',
         '**Fuentes:**', '',
         '- `docs/defects.md`, para la v1.0 (DEF-01 a DEF-13).',
         '- Los documentos de fase de la v1.1: F21 §16, F25 §26–§27 y F26 §19. Según la convención D-04 de la F26, cada '
         'fase registra ahí sus defectos.',
         '- Las observaciones abiertas que confirmó la F29F.', '',
         '**Qué no hay:** la ejecución F29F no produjo fallos, así que no hay defectos nuevos del software.', '',
         '**Prioridad:** no se registró en su momento. Se asigna aquí con una regla explícita: severidad Crítica o Alta '
         '→ Alta, Media → Media y Baja → Baja.', '',
         '| ID | Descripción | Severidad | Prioridad | Origen | Estado | Versión | Evidencia | Resolución | Prueba de regresión |',
         '|---|---|---|---|---|---|---|---|---|---|']
    esc = lambda x: str(x).replace('|', '/').replace('\n', ' ')
    for d in defs:
        desc = d['descripcion'] if len(d['descripcion']) <= 260 else d['descripcion'][:257].rsplit(' ', 1)[0] + '…'
        res = d['resolucion'] if len(d['resolucion']) <= 200 else d['resolucion'][:197].rsplit(' ', 1)[0] + '…'
        L.append(f'| {d["id"]} | {esc(desc)} | {d["severidad"]} | {d["prioridad"]} | {esc(d["origen"])} | '
                 f'{esc(d["estado"])} | {d["version"]} | {esc(d["evidencia"])} | {esc(res)} | {esc(d["regresion"])} |')
    L += ['', '*Las descripciones y resoluciones largas se abrevian; el texto completo está en la evidencia citada.*', '']

    # ---------------------------------------------------------------- métricas
    L += ['## 2. Métricas de ejecución (F29F)', '',
          '**Tasa de aprobación** = aprobadas / (ejecutadas − omitidas). Las omitidas no son fallos: dependen de una '
          'función desactivada (OBS-F29F-03).', '',
          '| Suite | Ejecutadas | Aprobadas | Fallidas | Omitidas | Tasa de aprobación |', '|---|---|---|---|---|---|']
    for s in ('PHPUnit', 'Cypress', 'Vitest', 'pytest'):
        sub = [c for c in cs if c['suite'] == s]
        n, ok, ko, sk = (sum(c[k] for c in sub) for k in ('n', 'passed', 'failed', 'skipped'))
        L.append(f'| {s} | {n} | {ok} | {ko} | {sk} | {_pct(ok, n - sk)} |')
    auto = [c for c in cs if c['suite'] in ('PHPUnit', 'Cypress', 'Vitest', 'pytest')]
    n, ok, ko, sk = (sum(c[k] for c in auto) for k in ('n', 'passed', 'failed', 'skipped'))
    L += [f'| **Total** | **{n}** | **{ok}** | **{ko}** | **{sk}** | **{_pct(ok, n - sk)}** |', '',
          'Verificaciones estáticas: TypeScript sin errores; build con '
          + re.search(r'(\d+) modules transformed', Q.log('06-build.log')).group(1) +
          ' módulos; configuración de Compose válida; CI en verde en `develop`. La CI de `main` no se ejecutó '
          '(OBS-F29F-04).', '']

    L += ['## 3. Casos de prueba (F29E)', '']
    por = lambda k: collections.Counter(c[k] for c in cs)
    L += ['| Automatización | CP |', '|---|---|'] + [f'| {k} | {v} |' for k, v in sorted(por('auto').items())] + ['']
    L += ['| Tipo de prueba | CP |', '|---|---|'] + [f'| {k} | {v} |' for k, v in sorted(por('tipo').items())] + ['']
    L += ['| Prioridad | CP |', '|---|---|'] + [f'| {k} | {v} |' for k, v in sorted(por('prioridad').items())] + ['']
    est = collections.Counter('APROBADO' if c['estado'].startswith('APROBADO') else c['estado'].split(':')[0].split(' (')[0]
                              for c in cs)
    L += ['| Estado (F29F) | CP |', '|---|---|'] + [f'| {k} | {v} |' for k, v in sorted(est.items())] + [
        '', f'Automatizados frente a manuales: {por("auto")[f29e.AUTO]} de {len(cs)} CP '
            f'({_pct(por("auto")[f29e.AUTO], len(cs))}) son automatizados.', '']

    cov = f29e.cobertura_rf(cs)
    rf_ok = sum(1 for v in cov.values() if v[0])
    cus = sorted({cu for rf, v in cov.items() if v[0] for cu in f29e.cu_of([rf])})
    rnf = collections.Counter(r[8] for r in N.RNF)
    L += ['## 4. Cobertura funcional (no es cobertura de código)', '',
          '| Métrica | Valor | Cálculo |', '|---|---|---|',
          f'| RF de la línea base con al menos un CP automatizado aprobado | {rf_ok} de 27 ({_pct(rf_ok, 27)}) | '
          'Matriz RF → CP de la F29E |',
          f'| CU cubiertos a través de sus RF | {len(cus)} de 20 ({_pct(len(cus), 20)}) | Tabla CU ↔ RF del Formato 08 |',
          '| RNF académicos por estado (F7) | ' + ', '.join(f'{v} {k}' for k, v in sorted(rnf.items())) +
          ' | docs/academico/practica-07 |',
          '| Cobertura de código (líneas o ramas) | **NO MEDIDA** | Sin Xdebug ni PCOV en el contenedor; nunca se midió |',
          '']

    L += ['## 5. Defectos', '']
    by = collections.Counter((d['version'].split()[0], d['severidad']) for d in defs)
    sevs = ['Crítica', 'Alta', 'Media', 'Baja']
    L += ['| Versión | ' + ' | '.join(sevs) + ' | Total |', '|---|' + '---|' * (len(sevs) + 1)]
    for v in ('v1.0', 'v1.1'):
        L.append(f'| {v} | ' + ' | '.join(str(by[(v, s)]) for s in sevs) + f' | {sum(by[(v, s)] for s in sevs)} |')
    L.append('| **Total** | ' + ' | '.join(str(sum(by[(v, s)] for v in ('v1.0', 'v1.1'))) for s in sevs) +
             f' | **{len(defs)}** |')
    tipos = collections.Counter(d['tipo'] for d in defs)
    abiertos = [d for d in defs if not d['estado'].startswith('Cerrado')]
    L += ['', '| Tipo | Registros |', '|---|---|'] + [f'| {k} | {v} |' for k, v in sorted(tipos.items())] + [
        '', f'**Cerrados:** {len(defs) - len(abiertos)} de {len(defs)} ({_pct(len(defs) - len(abiertos), len(defs))}).',
        '',
        f'**Abiertos:** {len(abiertos)}, ninguno del software funcional:'] + [
        f'- {d["id"]} ({d["severidad"]}): {d["estado"]}.' for d in abiertos] + [
        '', f'**Defectos de severidad Crítica o Alta abiertos:** '
        f'{sum(1 for d in abiertos if d["severidad"] in ("Crítica", "Alta"))}.',
        '', '**Métricas que no se calculan, por falta de datos:**', '',
        '- densidad de defectos por KLOC: no se midió el tamaño;',
        '- tiempo medio de corrección: no se registró la fecha de apertura y cierre de cada defecto;',
        '- defectos escapados a producción: no hay producción.', '']

    f25 = _f25()
    p1 = re.search(r'Tests:\s+(\d+) skipped, (\d+) passed \((\d+) assertions\)', Q.log('04-phpunit.log')).groups()
    p2 = re.search(r'Tests:\s+(\d+) skipped, (\d+) passed \((\d+) assertions\)', Q.log('04b-phpunit-junit.log')).groups()
    cy = Q.cypress_results()[1]
    py = sum(v['passed'] for v in Q.pytest_results().values())
    vt = Q.vitest_results()[1].group(1)
    L += ['## 6. Estabilidad y regresión', '',
          '| Suite | F25 (release v1.1, tras los arreglos) | F29F, 1.ª ejecución | F29F, 2.ª ejecución | Resultado |',
          '|---|---|---|---|---|',
          f'| PHPUnit (aprobadas / omitidas / aserciones) | {f25["phpunit"][0]} / {f25["phpunit"][1]} / {f25["phpunit"][3]} | '
          f'{p1[1]} / {p1[0]} / {p1[2]} | {p2[1]} / {p2[0]} / {p2[2]} | '
          f'{"Idéntico" if (p1[1], p1[0], p1[2]) == (p2[1], p2[0], p2[2]) == (f25["phpunit"][0], f25["phpunit"][1], f25["phpunit"][3]) else "Distinto"} |',
          f'| pytest (aprobadas) | {f25["pytest"]} | — (sin resumen) | {py} | {"Idéntico" if str(py) == f25["pytest"] else "Distinto"} |',
          f'| Vitest (aprobadas) | {f25["vitest"]} | {vt} | — | {"Idéntico" if vt == f25["vitest"] else "Distinto"} |',
          f'| Cypress (aprobadas / total) | {f25["cypress"][0]}/{f25["cypress"][1]} | {cy.group(4)}/{cy.group(3)} | — | '
          f'{"Idéntico" if (cy.group(4), cy.group(3)) == f25["cypress"] else "Distinto"} |', '',
          '**Interpretación:**', '',
          '- Sin fallos intermitentes: no hubo reintentos (Cypress `retries: 0`) y PHPUnit dio el mismo resultado en sus '
          'dos ejecuciones.',
          '- Sin regresiones frente a la QA de release de la F25.', '']

    L += ['## 7. Evaluación de calidad con ISO/IEC 25010 (marco de referencia)', '',
          '> ISO/IEC 25010 organiza la evaluación; **no se declara certificación ni conformidad con la norma**. El estado '
          'de cada RNF es el del Formato 07.', '',
          '| Característica | RNF | Estado | Evidencia del F7 |', '|---|---|---|---|']
    for r in N.RNF:
        L.append(f'| {r[1]} | {r[0]} {r[2]} | {r[8]} | {esc(r[9])} |')
    L += ['', '**Características sin evidencia suficiente:**', '',
          '- **Eficiencia de desempeño (RNF-06):** sin pruebas de carga.',
          '- **Fiabilidad y disponibilidad (RNF-07):** sin entorno de producción.',
          '- **Usabilidad, compatibilidad y mantenibilidad (RNF-05, RNF-08 y RNF-09):** evidencia parcial. En '
          'mantenibilidad, el formato pendiente se registra como F25-L03.']
    with open(os.path.join(out_dir, 'F29G_Defectos_y_Metricas.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(L).rstrip() + '\n')
    return defs
