"""F29G — Registro final de defectos, leído de los registros reales del proyecto (no se escribe ningún defecto nuevo
sin evidencia):

- v1.0: docs/defects.md (DEF-01 a DEF-13).
- v1.1: cada fase registró sus defectos en su propio documento (convención D-04 de la F26): Fase 21 §16
  (docs/v1.1/phase-21-visual-qa.md), Fase 25 §26 y §27 (docs/v1.1/phase-25-final-qa.md) y Fase 26 §19
  (docs/v1.1/phase-26-release-closeout.md).
- F29F: solo las observaciones abiertas que la ejecución de hoy confirmó (F25-L03 remedido y la CI de main).

La prioridad no se registró históricamente: se asigna en la F29G por una regla explícita (PRIORIDAD) a partir de la
severidad, y así se declara.
"""
import os
import re

import qa_data as Q

PRIORIDAD = {'crítica': 'Alta', 'alta': 'Alta', 'high': 'Alta', 'media': 'Media', 'medium': 'Media',
             'media (latente)': 'Media', 'baja': 'Baja', 'low': 'Baja', 'heredada': 'Baja'}
SEV_NORMAL = {'crítica': 'Crítica', 'alta': 'Alta', 'high': 'Alta', 'media': 'Media', 'medium': 'Media',
              'media (latente)': 'Media', 'baja': 'Baja', 'low': 'Baja', 'heredada': 'Baja'}

# Pruebas de regresión de los defectos de la F21, según su propio documento (§17): visual-qa.test.tsx cubre «token de
# la alerta destructiva, token del error de campo, relleno del enlace de salto, main en acceso, plegado de los códigos
# y preferredScrollBehavior»; E2E-19 cubre «sin desborde a 320 px, main único en acceso, enlace de salto de 24 px,
# contraste de la alerta de rechazo, del error de campo y del botón destructivo».
VQA, E19 = 'resources/js/components/visual-qa.test.tsx', 'cypress/e2e/e2e-19-qa-visual-accesible.cy.js'
F21_REGRESION = {'A4': [VQA, E19], 'A2': [E19], 'A3': [VQA, E19], 'A1': [VQA, E19], 'V1': [E19], 'F19-R': [VQA],
                 'V2': [VQA, E19], 'V3': [], 'M1': [VQA]}


def _read(rel):
    with open(os.path.join(Q.ROOT, rel), encoding='utf-8') as f:
        return f.read()


def _plain(x):
    return re.sub(r'\*\*|`', '', x).strip()


def _cells(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]


def _tests_in(text):
    """Clases de PHPUnit, specs de Cypress (por archivo o por ID E2E-NN) y archivos de pytest citados en el texto."""
    specs = {re.match(r'e2e-(\d\d)', f).group(1): f for f, _, _ in Q.cypress_specs()}
    return sorted(set(re.findall(r'([A-Z][A-Za-z0-9]+Test)', text)) |
                  set(re.findall(r'(e2e-\d\d-[a-z0-9-]+\.cy\.js)', text)) |
                  {specs[n] for n in re.findall(r'E2E-(\d\d)', text) if n in specs} |
                  set(re.findall(r'(test_[a-z0-9_]+\.py)', text)))


# Defectos de v1.0 sin prueba nombrada en defects.md: su verificación de regresión es la que indica su propia fila
# («Detectado por» y «Corrección»).
REGRESION_V10 = {
    'DEF-01': 'Healthcheck de Docker Compose (servicios healthy en cada ejecución; F29F 02-entorno)',
    'DEF-02': 'La suite PHPUnit corre sobre `reclutamiento_testing` (`force="true"` en phpunit.xml)',
    'DEF-04': '`npm run build` y `tsc --noEmit` (F29F 05-tsc y 06-build)',
    'DEF-11': 'Sin prueba automatizada (así consta en docs/defects.md); verificado en capturas',
}


def v10():
    out = []
    for line in _read('docs/defects.md').splitlines():
        if re.match(r'\| DEF-\d\d \|', line):
            c = _cells(line)
            sev = SEV_NORMAL[c[2].lower()]
            out.append(dict(id=c[0], descripcion=_plain(c[1]), severidad=sev, prioridad=PRIORIDAD[c[2].lower()],
                            origen=_plain(c[3]), estado=c[4], version='v1.0', evidencia='docs/defects.md',
                            resolucion=_plain(c[5]),
                            regresion=', '.join(_tests_in(c[3] + ' ' + c[5])) or REGRESION_V10.get(c[0], '—'),
                            tipo='Software'))
    return out


def f21():
    txt = _read('docs/v1.1/phase-21-visual-qa.md')
    sec = txt[txt.index('## 16. Defectos encontrados y corregidos'):]
    sec = sec[:sec.index('\n## ', 5)]
    out = []
    for line in sec.splitlines():
        m = re.match(r'\| \*\*([A-Z0-9-]+)\*\* \|', line)
        if m:
            c = _cells(line)
            sev_raw = _plain(c[1]).lower()
            out.append(dict(id='F21-' + m.group(1), descripcion=f'{_plain(c[2])}: {_plain(c[3])}',
                            severidad=SEV_NORMAL[sev_raw], prioridad=PRIORIDAD[sev_raw],
                            origen='QA visual y accesibilidad (Fase 21)', estado='Cerrado', version='v1.1',
                            evidencia='docs/v1.1/phase-21-visual-qa.md §16', resolucion=_plain(c[4]),
                            regresion=', '.join(F21_REGRESION.get(m.group(1), [])) or '—', tipo='Software'))
    return out


def f25():
    txt = _read('docs/v1.1/phase-25-final-qa.md')
    fixes = {}
    s27 = txt[txt.index('## 27. Fixes'):]
    for line in s27[:s27.index('\n## ', 5)].splitlines():
        m = re.match(r'\| (F25-[ML]\d\d) \|', line)
        if m:
            c = _cells(line)
            fixes[m.group(1)] = (c[1], c[2])
    out = []
    s26 = txt[txt.index('## 26. Defectos encontrados'):]
    for line in s26[:s26.index('\n## ', 5)].splitlines():
        m = re.match(r'\| \*\*(F25-[ML]\d\d)\*\* \|', line)
        if m:
            c = _cells(line)
            fid = m.group(1)
            fx = fixes.get(fid)
            tipo = 'Software' if fid in ('F25-M01', 'F25-M02') else ('Estilo' if fid == 'F25-L03' else 'Documentación')
            abierto = fid == 'F25-L03'
            out.append(dict(
                id=fid, descripcion=f'{_plain(c[2])}: {_plain(c[3])}', severidad=SEV_NORMAL[c[1].lower()],
                prioridad=PRIORIDAD[c[1].lower()], origen='QA global de release (Fase 25)',
                estado='Abierto (remedido en la F29F: OBS-F29F-05)' if abierto else 'Cerrado', version='v1.1',
                evidencia='docs/v1.1/phase-25-final-qa.md §26–§27' + ('; qa-final/evidencias/11-pint.log y 12-vp-check.log'
                                                                       if abierto else ''),
                resolucion=(_plain(fx[0]) if fx else 'Pendiente: aplicar `pint` y `vp check --fix` en un commit propio'),
                regresion=(', '.join(_tests_in(fx[0] + ' ' + fx[1])) or _plain(fx[1])) if fx else '—', tipo=tipo))
    return out


def f26():
    txt = _read('docs/v1.1/phase-26-release-closeout.md')
    out = []
    for line in txt.splitlines():
        m = re.match(r'\| \*\*(F26-M\d\d(?:-R\d)?)\*\* \(MEDIUM\) \|', line)
        if m:
            c = _cells(line)
            out.append(dict(id=m.group(1), descripcion=_plain(c[1]), severidad='Media', prioridad='Media',
                            origen='Auditoría del release (Fase 26)', estado='Cerrado', version='v1.1 (documentación)',
                            evidencia='docs/v1.1/phase-26-release-closeout.md §19', resolucion=_plain(c[2]),
                            regresion='— (documental)', tipo='Documentación / proceso'))
    return out


def f29f():
    return [dict(id='OBS-F29F-04', descripcion='El merge F29C en main (60ebcb2) no generó ejecución de GitHub Actions',
                 severidad='Baja', prioridad='Media', origen='Ejecución QA final (F29F)',
                 estado='Abierto: CI main F29C pendiente de ejecución manual', version='v1.1 (proceso)',
                 evidencia='docs/academico/qa-final/evidencias/ci-github-actions.json',
                 resolucion='Ejecutar el workflow `tests` en main (workflow_dispatch) y verificar success',
                 regresion='— (proceso)', tipo='Proceso / CI')]


def registro():
    return v10() + f21() + f25() + f26() + f29f()
