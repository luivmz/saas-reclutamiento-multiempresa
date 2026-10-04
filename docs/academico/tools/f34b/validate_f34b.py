"""F34B — Validación del registro de evidencias externas para G0 (solo biblioteca estándar).

Reglas sobre docs/academico/g0-evidence/:
  REC   cada registro (responsable, rol, fecha, decisión, evidencia, observaciones, estado) sale de PENDIENTE solo con
        responsable, fecha, decisión admitida y un adjunto EXISTENTE en adjuntos/ (sin firmas ni respuestas inventadas)
  ANS   los campos de respuesta de terceros (jurídico, privacidad) siguen vacíos mientras su registro esté PENDIENTE
  MAT   la matriz maestra tiene los 15 criterios y cada estado externo coincide con el que se DERIVA de los registros;
        «Verificada = Sí» exige evidencia; el resumen coincide con las filas
  DEC   G0 solo puede declararse APROBADA CON RESTRICCIONES si todos los criterios están CUMPLIDO o NO APLICA;
        nunca APROBADA (B + C) en este ciclo; ADR-005 solo APROBADA si su acta lo está
  SCOPE el alcance C no se habilita
  PHASE F35–F40 siguen BLOQUEADAS sin decisión G0 válida
  DATA  los datos reales siguen prohibidos
  IDN   identidad y rol (auditoría F34B-M02): roles admitidos por formulario; tres integrantes distintos del equipo
        (lista de CLAUDE.md), cada uno exactamente una vez, en el acta y en la aceptación del threat model; el docente
        consultivo no sustituye a un integrante; jurídico, privacidad y necesidad firmados por personas ajenas al equipo,
        con identidades distintas donde corresponde; ninguna fecha o decisión sin identidad coherente
  LNK   enlaces y anclas;  GIT  alcance de la rama, F34A, ADR-005, baseline y runtime sin cambios
Incluye casos negativos y un control positivo (todo en memoria; no crea adjuntos). El control positivo usa una lista
de integrantes SINTÉTICA y adjuntos simulados con prefijo CONTROL; nunca nombres reales ni archivos del repositorio.
Uso: python docs/academico/tools/f34b/validate_f34b.py
"""
import os
import re
import subprocess
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
DOCS = os.path.join(ROOT, 'docs', 'academico', 'g0-evidence')
ATT = os.path.join(DOCS, 'adjuntos')
BASE = 'develop'
FILES = ['README.md', 'F34B_Matriz_Evidencias_G0.md', 'F34B_Acta_Aprobacion_ADR005.md', 'F34B_Revision_Juridica.md',
         'F34B_Privacidad.md', 'F34B_Validacion_Necesidad.md', 'F34B_Aceptacion_Threat_Model.md',
         'F34B_Decision_G0.md']
STATES = {'CUMPLIDO', 'PARCIAL', 'PENDIENTE EXTERNO', 'RECHAZADO', 'NO APLICA'}
REC_STATES = {'PENDIENTE', 'REGISTRADO'}
# Decisiones admitidas por documento y tabla (en orden de aparición).
FORMS = {
    'F34B_Acta_Aprobacion_ADR005.md': [{'PENDIENTE', 'APRUEBA', 'APRUEBA CON OBSERVACIONES', 'RECHAZA'}],
    'F34B_Revision_Juridica.md': [{'PENDIENTE', 'SIN OBJECIÓN', 'SIN OBJECIÓN CON CONDICIONES', 'CON OBJECIÓN'},
                                  {'PENDIENTE', 'COMPLETADA', 'NO APLICA'}],
    'F34B_Privacidad.md': [{'PENDIENTE', 'APRUEBA', 'APRUEBA CON CONDICIONES', 'RECHAZA'}],
    'F34B_Validacion_Necesidad.md': [{'PENDIENTE', 'NECESIDAD VALIDADA', 'NECESIDAD NO VALIDADA'}],
    'F34B_Aceptacion_Threat_Model.md': [{'PENDIENTE', 'ACEPTA', 'ACEPTA CON OBSERVACIONES', 'RECHAZA'}],
}
EXTERNAL = {'G0-02', 'G0-03', 'G0-09', 'G0-12', 'G0-14'}
NEG = re.compile(r'\b(no|ni|sin|nunca|ningún|ninguna|sigue|siguen|hipot[eé]tico|exigiría|solo si|si y solo si)\b', re.I)
DATE = re.compile(r'\d{4}-\d{2}-\d{2}')
ATT_LINK = re.compile(r'\]\((adjuntos/[^)\s]+)\)')


# Roles admitidos (auditoría F34B-M02).
TEAM_ROLE = 'Integrante del equipo'
CONSULTIVE_ROLE = 'Docente del curso (consultivo, opcional)'
LEGAL_ROLES = {'Abogado o responsable legal', 'Abogado', 'Asesor legal', 'Responsable legal'}
PRIV_OWNER_ROLES = {'Responsable del tratamiento', 'Delegado de protección de datos', 'Oficial de privacidad'}
PRIV_LEGAL_ROLES = {'Revisión jurídica de privacidad'} | LEGAL_ROLES - {'Abogado o responsable legal'}
NEED_ROLES = {'Docente del curso', 'RR. HH.', 'Administración', 'Representante institucional'}


def read_all():
    return {n: open(os.path.join(DOCS, n), encoding='utf-8').read() if os.path.isfile(os.path.join(DOCS, n)) else ''
            for n in FILES}


def real_exists(rel):
    p = os.path.normpath(os.path.join(DOCS, rel))
    return (os.path.isfile(p) and os.path.dirname(p) == ATT and os.path.basename(p) != 'README.md'
            and os.path.getsize(p) > 0)


def ident(name):
    """Identidad normalizada: tokens alfabéticos sin tildes ni mayúsculas, sin orden."""
    s = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode().lower()
    return frozenset(re.findall(r'[a-z]+', s))


def team_roster():
    """Integrantes del proyecto según CLAUDE.md (fuente única). Lista vacía si no se puede leer: falla cerrado."""
    try:
        t = open(os.path.join(ROOT, 'CLAUDE.md'), encoding='utf-8').read()
    except OSError:
        return []
    m = re.search(r'Integrantes: (.+?)\.\s', t)
    if not m:
        return []
    return [ident(x) for x in re.split(r',\s*|\s+y\s+', m.group(1)) if x.strip()]


class Ctx:
    """Contexto de verificación: cómo se comprueba un adjunto y cuál es la lista de integrantes."""

    def __init__(self, exists, roster):
        self.exists, self.roster = exists, roster

    def __call__(self, rel):
        return self.exists(rel)


REAL = Ctx(real_exists, team_roster())


def cells(ln):
    return [c.strip() for c in ln.strip().strip('|').split('|')]


def rows(text, first):
    return [cells(ln) for ln in text.splitlines() if ln.startswith('|') and re.fullmatch(first, cells(ln)[0])]


def records(text):
    """Tablas de registro: listas de filas bajo una cabecera «Responsable | Rol | … | Estado»."""
    tables, cur = [], None
    for ln in text.splitlines():
        if not ln.startswith('|'):
            cur = None
            continue
        c = cells(ln)
        if c[0] == 'Responsable' and len(c) == 7:
            cur = []
            tables.append(cur)
        elif cur is not None and not set(ln.replace('|', '').strip()) <= set('-: '):
            cur.append(c)
    return tables


def plain(cell):
    return re.sub(r'\s*\(.*?\)\s*', ' ', cell.replace('**', '')).strip()


def registered(r, positive, exists):
    return r[6] == 'REGISTRADO' and r[3] in positive and evidence_ok(r, exists)


def evidence_ok(r, exists):
    links = ATT_LINK.findall(r[4])
    return bool(links) and all(exists(x) for x in links)


# ---------------------------------------------------------------- reglas
def rec(D, exists):
    out = []
    for n, specs in FORMS.items():
        tabs = records(D[n])
        if len(tabs) != len(specs):
            out.append(f'{n}: {len(tabs)} tablas de registro (se esperan {len(specs)})')
            continue
        for allowed, tab in zip(specs, tabs):
            if not tab:
                out.append(f'{n}: tabla de registro vacía')
            for r in tab:
                if len(r) != 7:
                    out.append(f'{n}: fila de registro con {len(r)} columnas')
                    continue
                who, _, date, dec, ev, _, st = r
                if dec not in allowed:
                    out.append(f'{n}: decisión no admitida «{dec}»')
                if st not in REC_STATES:
                    out.append(f'{n}: estado no admitido «{st}»')
                touched = dec != 'PENDIENTE' or st != 'PENDIENTE' or who != '—' or date != '—' or ev != '—'
                if not touched:
                    continue
                if st != 'REGISTRADO' or dec == 'PENDIENTE':
                    out.append(f'{n}: registro con datos o decisión pero sin estado REGISTRADO coherente ({r[1]})')
                if who in ('', '—') or not DATE.fullmatch(date):
                    out.append(f'{n}: registro sin responsable o sin fecha válida ({r[1]})')
                if not evidence_ok(r, exists):
                    out.append(f'{n}: decisión «{dec}» sin adjunto existente en adjuntos/ (firma o aprobación sin '
                               f'evidencia) ({r[1]})')
    return out


def ans(D, exists):
    """Respuestas de terceros solo con su registro REGISTRADO."""
    out = []
    jur = records(D['F34B_Revision_Juridica.md'])
    jur_ok = bool(jur) and all(r[6] == 'REGISTRADO' for r in jur[0])
    for r in rows(D['F34B_Revision_Juridica.md'], r'J-\d\d.*'):
        if len(r) == 3 and r[2] != '—' and not jur_ok:
            out.append(f'respuesta jurídica {r[0]} registrada sin revisión REGISTRADO')
    pri = records(D['F34B_Privacidad.md'])
    pri_ok = bool(pri) and all(r[6] == 'REGISTRADO' for r in pri[0])
    sec = D['F34B_Privacidad.md'].split('## 1.')[-1].split('## 2.')[0]
    for r in rows(sec, r'.*'):
        if len(r) == 2 and r[0] not in ('Tema abierto en F34A',) and not r[0].startswith('-') and r[1] != '—' \
                and not pri_ok:
            out.append(f'definición de privacidad «{r[0]}» registrada sin aprobación REGISTRADO')
    return out


# ---------------------------------------------------------------- identidad y rol (F34B-M02)
def touched(r):
    return r[0] != '—' or r[2] != '—' or r[3] != 'PENDIENTE' or r[4] != '—' or r[6] != 'PENDIENTE'


def coherent(r):
    """Identidad plausible: al menos dos palabras y distinta del texto del rol."""
    i = ident(r[0])
    return r[0] not in ('', '—') and len(i) >= 2 and i != ident(r[1]) and not re.search(r'\d', r[0])


def roster_match(r, roster):
    """Índices de los integrantes cuyo nombre contiene todos los tokens de la identidad registrada."""
    i = ident(r[0])
    return [k for k, m in enumerate(roster) if len(i) >= 2 and i <= m]


def idn_team(n, tab, roster, consultive_allowed):
    out = []
    if not roster:
        return [f'{n}: no se pudo leer la lista de integrantes de CLAUDE.md (falla cerrado)']
    team = [r for r in tab if r[1] == TEAM_ROLE]
    cons = [r for r in tab if r[1] == CONSULTIVE_ROLE]
    other = [r for r in tab if r[1] not in (TEAM_ROLE, CONSULTIVE_ROLE) or (r[1] == CONSULTIVE_ROLE
                                                                             and not consultive_allowed)]
    out += [f'{n}: rol no admitido «{r[1]}»' for r in other]
    if len(team) != 3:
        out.append(f'{n}: {len(team)} filas de integrante (se exigen exactamente 3)')
    if len(cons) > 1:
        out.append(f'{n}: más de una fila consultiva')
    seen_ids, seen_members = [], []
    for r in team:
        if not touched(r):
            continue
        if not coherent(r):
            out.append(f'{n}: fecha o decisión sin identidad coherente («{r[0]}»)')
            continue
        m = roster_match(r, roster)
        if len(m) != 1:
            out.append(f'{n}: «{r[0]}» no corresponde a exactamente un integrante del equipo')
            continue
        if ident(r[0]) in seen_ids or m[0] in seen_members:
            out.append(f'{n}: identidad repetida: un mismo integrante firma más de una fila')
        seen_ids.append(ident(r[0]))
        seen_members.append(m[0])
    for r in cons:
        if touched(r) and (not coherent(r) or roster_match(r, roster)):
            out.append(f'{n}: la fila consultiva debe ser de una persona ajena al equipo con identidad coherente')
    return out


def idn_external(n, tab, roster, allowed_roles, unique_roles=False, distinct=True, required_roles=None):
    """Formularios firmados por terceros: roles admitidos, ajenos al equipo, identidades distintas."""
    out = []
    for r in tab:
        if r[1] not in allowed_roles:
            out.append(f'{n}: rol no admitido «{r[1]}»')
    if unique_roles:
        c = [r[1] for r in tab]
        out += [f'{n}: rol «{x}» repetido' for x in set(c) if c.count(x) > 1]
    if required_roles:
        for group in required_roles:
            if sum(r[1] in group for r in tab) != 1:
                out.append(f'{n}: se exige exactamente una fila con rol en {sorted(group)}')
    seen = []
    for r in tab:
        if not touched(r):
            continue
        if not coherent(r):
            out.append(f'{n}: fecha o decisión sin identidad coherente («{r[0]}»)')
            continue
        if roster_match(r, roster):
            out.append(f'{n}: «{r[0]}» es integrante del equipo y no puede firmar este registro')
        if distinct and ident(r[0]) in seen:
            out.append(f'{n}: identidad repetida en filas que exigen personas distintas')
        seen.append(ident(r[0]))
    return out


def idn_forms(D, ctx):
    roster = getattr(ctx, 'roster', REAL.roster)
    tabs = {n: records(D[n]) for n in FORMS}

    def t(n, i=0):
        return [r for r in (tabs[n][i] if len(tabs[n]) > i else []) if len(r) == 7]
    jur = idn_external('F34B_Revision_Juridica.md', t('F34B_Revision_Juridica.md', 0), roster, LEGAL_ROLES)
    jur += idn_external('F34B_Revision_Juridica.md', t('F34B_Revision_Juridica.md', 1), roster, LEGAL_ROLES)
    return {
        'F34B_Acta_Aprobacion_ADR005.md': idn_team('F34B_Acta_Aprobacion_ADR005.md',
                                                   t('F34B_Acta_Aprobacion_ADR005.md'), roster, True),
        'F34B_Aceptacion_Threat_Model.md': idn_team('F34B_Aceptacion_Threat_Model.md',
                                                    t('F34B_Aceptacion_Threat_Model.md'), roster, False),
        'F34B_Revision_Juridica.md': jur,
        'F34B_Privacidad.md': idn_external('F34B_Privacidad.md', t('F34B_Privacidad.md'), roster,
                                           PRIV_OWNER_ROLES | PRIV_LEGAL_ROLES,
                                           required_roles=[PRIV_OWNER_ROLES, PRIV_LEGAL_ROLES]),
        'F34B_Validacion_Necesidad.md': idn_external('F34B_Validacion_Necesidad.md', t('F34B_Validacion_Necesidad.md'),
                                                     roster, NEED_ROLES, unique_roles=True),
    }


def idn(D, exists):
    return [v for vs in idn_forms(D, exists).values() for v in vs]


def derive(D, exists):
    """Estado de cada criterio externo derivado SOLO de registros con evidencia existente e identidad válida.

    Un formulario con cualquier violación de identidad o rol no produce CUMPLIDO ni RECHAZADO."""
    bad = idn_forms(D, exists)

    def tab(n, i=0):
        t = records(D[n])
        return [r for r in (t[i] if len(t) > i else []) if len(r) == 7]
    st = {}
    n = 'F34B_Acta_Aprobacion_ADR005.md'
    acta = [r for r in tab(n) if r[1] == TEAM_ROLE]
    if bad[n]:
        st['G0-14'] = 'PENDIENTE EXTERNO'
    elif any(registered(r, {'RECHAZA'}, exists) for r in acta):
        st['G0-14'] = 'RECHAZADO'
    elif len(acta) == 3 and all(registered(r, {'APRUEBA', 'APRUEBA CON OBSERVACIONES'}, exists) for r in acta):
        st['G0-14'] = 'CUMPLIDO'
    else:
        st['G0-14'] = 'PENDIENTE EXTERNO'
    n = 'F34B_Revision_Juridica.md'
    rev, eia_ = tab(n, 0), tab(n, 1)
    if bad[n]:
        st['G0-02'] = 'PENDIENTE EXTERNO'
    elif any(registered(r, {'CON OBJECIÓN'}, exists) for r in rev):
        st['G0-02'] = 'RECHAZADO'
    elif rev and eia_ and all(registered(r, {'SIN OBJECIÓN', 'SIN OBJECIÓN CON CONDICIONES'}, exists) for r in rev) \
            and all(registered(r, {'COMPLETADA', 'NO APLICA'}, exists) for r in eia_):
        st['G0-02'] = 'CUMPLIDO'
    else:
        st['G0-02'] = 'PENDIENTE EXTERNO'
    n = 'F34B_Privacidad.md'
    pri = tab(n)
    if bad[n]:
        st['G0-03'] = 'PENDIENTE EXTERNO'
    elif any(registered(r, {'RECHAZA'}, exists) for r in pri):
        st['G0-03'] = 'RECHAZADO'
    elif pri and all(registered(r, {'APRUEBA', 'APRUEBA CON CONDICIONES'}, exists) for r in pri):
        st['G0-03'] = 'CUMPLIDO'
    else:
        st['G0-03'] = 'PENDIENTE EXTERNO'
    n = 'F34B_Validacion_Necesidad.md'
    nec = tab(n)
    if bad[n]:
        st['G0-12'] = 'PENDIENTE EXTERNO'
    elif any(registered(r, {'NECESIDAD NO VALIDADA'}, exists) for r in nec):
        st['G0-12'] = 'RECHAZADO'
    elif any(r[1] in ('Docente del curso', 'Representante institucional')
             and registered(r, {'NECESIDAD VALIDADA'}, exists) for r in nec):
        st['G0-12'] = 'CUMPLIDO'
    else:
        st['G0-12'] = 'PENDIENTE EXTERNO'
    n = 'F34B_Aceptacion_Threat_Model.md'
    tm = tab(n)
    if bad[n]:
        st['G0-09'] = 'PARCIAL'
    elif any(registered(r, {'RECHAZA'}, exists) for r in tm):
        st['G0-09'] = 'RECHAZADO'
    elif len(tm) == 3 and all(registered(r, {'ACEPTA', 'ACEPTA CON OBSERVACIONES'}, exists) for r in tm):
        st['G0-09'] = 'CUMPLIDO'
    else:
        st['G0-09'] = 'PARCIAL'
    return st


def matrix_states(D):
    return {r[0]: plain(r[8]) for r in rows(D['F34B_Matriz_Evidencias_G0.md'], r'G0-\d\d') if len(r) == 10}


def mat(D, exists):
    t = D['F34B_Matriz_Evidencias_G0.md']
    rs = rows(t, r'G0-\d\d')
    out = []
    if [r[0] for r in rs] != [f'G0-{i:02d}' for i in range(1, 16)]:
        out.append('la matriz no tiene exactamente G0-01..G0-15')
    der = derive(D, exists)
    for r in rs:
        if len(r) != 10:
            out.append(f'{r[0]}: {len(r)} columnas (se esperan 10)')
            continue
        gid, ev, ver, st = r[0], r[3], r[7], plain(r[8])
        if st not in STATES:
            out.append(f'{gid}: estado «{st}» no admitido')
        if gid in der and st != der[gid]:
            out.append(f'{gid}: la matriz dice {st} pero los registros con evidencia dan {der[gid]}')
        if ver.startswith('Sí') and ev in ('Ninguna', '—', ''):
            out.append(f'{gid}: verificada sin evidencia recibida')
        if st == 'CUMPLIDO':
            if not ver.startswith('Sí') or not DATE.search(r[6]) or ev in ('Ninguna', '—', ''):
                out.append(f'{gid}: CUMPLIDO sin evidencia verificada y fechada')
            if gid in EXTERNAL and not (ATT_LINK.findall(ev) and all(exists(x) for x in ATT_LINK.findall(ev))):
                out.append(f'{gid}: criterio externo CUMPLIDO sin adjunto existente')
    final = matrix_states(D)
    for s in STATES:
        m = re.search(r'^\| ' + re.escape(s) + r' \| .*? \| (\d+) \|$', t, re.M)
        if not m or int(m.group(1)) != sum(v == s for v in final.values()):
            out.append(f'resumen de la matriz: «{s}» no coincide con las filas')
    return out


def g0_ok(D, exists):
    final = matrix_states(D)
    return len(final) == 15 and all(v in ('CUMPLIDO', 'NO APLICA') for v in final.values()) and not mat(D, exists)


CLAIM_G0_FULL = re.compile(r'G0\s*=\s*\**\s*APROBADA(?! CON RESTRICCIONES)')
CLAIM_G0_B = re.compile(r'G0\s*=\s*\**\s*APROBADA CON RESTRICCIONES')
CLAIM_ADR = re.compile(r'ADR-005\s*=\s*\**\s*APROBAD|ADR-005 (?:fue|ha sido|está|queda|quedó) aprobad', re.I)


def dec(D, exists):
    out = []
    ok = g0_ok(D, exists)
    adr_ok = derive(D, exists)['G0-14'] == 'CUMPLIDO'
    for n, t in D.items():
        for i, ln in enumerate(t.splitlines(), 1):
            if CLAIM_G0_FULL.search(ln):
                out.append(f'{n}:{i}: declara G0 APROBADA (B + C), no prevista en este ciclo')
            if CLAIM_G0_B.search(ln) and not ok:
                out.append(f'{n}:{i}: declara G0 APROBADA CON RESTRICCIONES con criterios pendientes')
            if CLAIM_ADR.search(ln) and not NEG.search(ln) and not adr_ok:
                out.append(f'{n}:{i}: declara ADR-005 aprobado sin acta registrada')
    d = D['F34B_Decision_G0.md']
    if not ok and '- **G0 = NO APROBADA.**' not in d:
        out.append('faltan criterios y la decisión no declara «G0 = NO APROBADA»')
    if not adr_ok:
        for n in ('README.md', 'F34B_Decision_G0.md'):
            if 'ADR-005 = PROPUESTA' not in D[n]:
                out.append(f'{n}: no declara «ADR-005 = PROPUESTA»')
    final = matrix_states(D)
    for r in rows(d, r'G0-\d\d'):
        if len(r) == 4 and final.get(r[0]) != r[3]:
            out.append(f'{r[0]}: la decisión dice {r[3]} y la matriz {final.get(r[0])}')
    if 'Ningún documento ni validador aprueba G0 automáticamente' not in d:
        out.append('la decisión no declara que nada aprueba G0 automáticamente')
    return out


def scope(D, exists):
    out = []
    for n, t in D.items():
        for i, ln in enumerate(t.splitlines(), 1):
            if re.search(r'alcance C[^.|]*\b(?:habilitad[oa]|se habilita|permitid[oa]|autorizad[oa])', ln, re.I) \
                    and not re.search(r'\bno\b|sin habilitar|exigir', ln, re.I):
                out.append(f'{n}:{i}: habilita el alcance C')
    if '**Alcance C: no habilitado.**' not in D['F34B_Decision_G0.md']:
        out.append('la decisión no declara «Alcance C: no habilitado»')
    return out


def phase(D, exists):
    out = []
    if g0_ok(D, exists):
        return out
    for n in ('README.md', 'F34B_Decision_G0.md'):
        if 'F35–F40 = BLOQUEADAS' not in D[n]:
            out.append(f'{n}: G0 no aprobada y no declara «F35–F40 = BLOQUEADAS»')
    for n, t in D.items():
        for i, ln in enumerate(t.splitlines(), 1):
            if re.search(r'F3[5-9]|F40', ln) and re.search(r'HABILITAD|DESBLOQUEAD', ln, re.I) \
                    and not re.search(r'BLOQUEAD[OA]S?\b(?!.*HABILITAD)|\bno\b|hipot', ln, re.I):
                out.append(f'{n}:{i}: desbloquea F35–F40 sin decisión G0 válida')
    for r in rows(D['F34B_Decision_G0.md'], r'F3[5-9] .*|F40 .*'):
        if len(r) == 3 and r[1] != 'BLOQUEADA':
            out.append(f'{r[0]}: estado «{r[1]}» sin decisión G0 válida')
    return out


def data(D, exists):
    out = []
    for n, t in D.items():
        for i, ln in enumerate(t.splitlines(), 1):
            if re.search(r'datos reales (?:quedan|están|son|se|ya) (?:\w+ )?(?:autorizad|permitid|habilitad)', ln, re.I) \
                    and not re.search(r'\bno\b|salvo', ln, re.I):
                out.append(f'{n}:{i}: autoriza datos reales sin aprobación específica')
    for n in ('README.md', 'F34B_Decision_G0.md', 'F34B_Privacidad.md'):
        if 'datos reales siguen PROHIBIDOS' not in D[n]:
            out.append(f'{n}: no declara que los datos reales siguen PROHIBIDOS')
    return out


def slug(h):
    h = re.sub(r'[`*_]', '', h.strip().lower())
    return re.sub(r'[^\w\- ]', '', h).replace(' ', '-')


def lnk(D, exists):
    out = []
    for n, t in D.items():
        for link in re.findall(r'\]\(([^)\s]+)\)', t):
            if link.startswith(('http://', 'https://')):
                continue
            path, _, anchor = link.partition('#')
            if path.startswith('adjuntos/') and path != 'adjuntos/README.md':
                if not exists(path):
                    out.append(f'{n}→{link} (adjunto inexistente)')
                continue
            target = os.path.normpath(os.path.join(DOCS, path)) if path else os.path.join(DOCS, n)
            if not os.path.exists(target):
                out.append(f'{n}→{link}')
            elif anchor and target.endswith('.md'):
                src = D.get(os.path.basename(target)) if os.path.dirname(target) == DOCS else None
                src = src if src is not None else open(target, encoding='utf-8').read()
                if anchor not in {slug(h) for h in re.findall(r'^#+ (.+)$', src, re.M)}:
                    out.append(f'{n}→{link}')
    return out


RULES = [('REC', rec), ('ANS', ans), ('IDN', idn), ('MAT', mat), ('DEC', dec), ('SCOPE', scope), ('PHASE', phase),
         ('DATA', data), ('LNK', lnk)]


def run_rules(D, exists=REAL):
    res = {}
    for rid, fn in RULES:
        try:
            res[rid] = fn(D, exists)
        except (KeyError, IndexError, ValueError, AttributeError) as e:
            res[rid] = [f'error estructural: {type(e).__name__}: {e}']
    return res


# ---------------------------------------------------------------- mutaciones
def sub(n, a, b, count=1):
    def f(D):
        assert a in D[n], (n, a)
        D = dict(D)
        D[n] = D[n].replace(a, b, count)
        return D
    return f


def rsub(n, pat, rep, count=1):
    def f(D):
        D = dict(D)
        new = re.sub(pat, rep, D[n], count=count, flags=re.M)
        assert new != D[n], (n, pat)
        D[n] = new
        return D
    return f


def chain(*fs):
    def f(D):
        for g in fs:
            D = g(D)
        return D
    return f


def set_rows(n, new_rows, table=0):
    """Sustituye las filas de la tabla de registro `table` de `n` por `new_rows` (lista de celdas)."""
    def f(D):
        D = dict(D)
        out, k, skipping = [], -1, False
        for ln in D[n].splitlines():
            c = cells(ln) if ln.startswith('|') else []
            if c and c[0] == 'Responsable' and len(c) == 7:
                k += 1
                skipping = k == table
                out.append(ln)
                continue
            if skipping and ln.startswith('|'):
                if set(ln.replace('|', '').strip()) <= set('-: '):
                    out.append(ln)
                    out += ['| ' + ' | '.join(r) + ' |' for r in new_rows]
                continue
            skipping = False if not ln.startswith('|') else skipping
            out.append(ln)
        assert k >= table, (n, table)
        D[n] = '\n'.join(out) + '\n'
        return D
    return f


# Contexto SIMULADO: lista de integrantes sintética y adjuntos con prefijo CONTROL que solo existen en memoria.
SYN_TEAM = ['Integrante Control Uno', 'Integrante Control Dos', 'Integrante Control Tres']
SIM = Ctx(lambda p: p.startswith('adjuntos/CONTROL-'), [ident(x) for x in SYN_TEAM])
CTRL = '[adjunto](adjuntos/CONTROL-{}.pdf)'
DAY = '2026-10-05'


def row(name, role, dec, link='x', st='REGISTRADO'):
    return [name, role, DAY if name != '—' else '—', dec, CTRL.format(link) if link else '—', '—', st]


def team_rows(names, dec, role=TEAM_ROLE, link='team'):
    return [row(nm, role, dec, f'{link}-{i}') for i, nm in enumerate(names)]


U, D2, T3 = SYN_TEAM
PEND = ['—', TEAM_ROLE, '—', 'PENDIENTE', '—', '—', 'PENDIENTE']
CONS_PEND = ['—', CONSULTIVE_ROLE, '—', 'PENDIENTE', '—', '—', 'PENDIENTE']
ACTA, TM, JUR, PRI, NEC, MATX = ('F34B_Acta_Aprobacion_ADR005.md', 'F34B_Aceptacion_Threat_Model.md',
                                 'F34B_Revision_Juridica.md', 'F34B_Privacidad.md', 'F34B_Validacion_Necesidad.md',
                                 'F34B_Matriz_Evidencias_G0.md')
ACTA_ROW = '| — | Integrante del equipo | — | PENDIENTE | — | — | PENDIENTE |'
FAKE = '[acta](adjuntos/G0-14_acta-adr005_2026-10-05.pdf)'

# (id, regla, descripción, mutación, contexto simulado, criterio que NO puede quedar CUMPLIDO)
CASES = [
    ('QA-01', 'REC', 'Aprobación de ADR-005 sin responsable, fecha ni evidencia',
     sub(ACTA, ACTA_ROW, '| — | Integrante del equipo | — | APRUEBA | — | — | REGISTRADO |'), False, None),
    ('QA-02', 'REC', 'Firma inventada: nombre y fecha con un adjunto que no existe',
     sub(ACTA, ACTA_ROW, f'| Integrante A | Integrante del equipo | 2026-10-05 | APRUEBA | {FAKE} | — | REGISTRADO |'),
     False, None),
    ('QA-03', 'REC', 'Nombre y fecha registrados, pero estado y decisión en PENDIENTE (firma a medias)',
     sub(ACTA, ACTA_ROW, '| Integrante A | Integrante del equipo | 2026-10-05 | PENDIENTE | — | — | PENDIENTE |'),
     False, None),
    ('QA-04', 'REC', 'Evaluación de impacto COMPLETADA sin documento adjunto',
     rsub(JUR, r'(## 3\. Decisión sobre la evaluación de impacto[\s\S]*?)\| — \| Abogado o responsable '
          r'legal \| — \| PENDIENTE \| — \| — \| PENDIENTE \|',
          r'\1| Abogado X | Abogado o responsable legal | 2026-10-05 | COMPLETADA | — | — | REGISTRADO |'), False, None),
    ('QA-05', 'REC', 'Evaluación de impacto «PLANIFICADA» como decisión',
     rsub(JUR, r'(## 3\. Decisión sobre la evaluación de impacto[\s\S]*?\| — \| Abogado o responsable '
          r'legal \| — \| )PENDIENTE', r'\1PLANIFICADA'), False, None),
    ('QA-06', 'ANS', 'Conclusión jurídica escrita sin revisión registrada',
     rsub(JUR, r'^(\| J-03 \|.*\| )—( \|)$', r'\1B no es un sistema de IA\2'), False, None),
    ('QA-07', 'ANS', 'Plazo de retención definido sin aprobación de privacidad',
     sub(PRI, '| Plazos de retención y borrado | — |', '| Plazos de retención y borrado | 2 años |'), False, None),
    ('QA-08', 'REC', 'Respuesta institucional inventada: necesidad validada sin adjunto',
     sub(NEC, '| — | Docente del curso | — | PENDIENTE | — | — | PENDIENTE |',
         '| Docente | Docente del curso | 2026-10-05 | NECESIDAD VALIDADA | — | — | REGISTRADO |'), False, None),
    ('QA-09', 'REC', 'Threat model aceptado sin evidencia',
     sub(TM, ACTA_ROW, '| — | Integrante del equipo | — | ACEPTA | — | — | REGISTRADO |'), False, None),
    ('QA-10', 'MAT', 'G0-14 marcado CUMPLIDO sin acta registrada',
     rsub(MATX, r'(^\| G0-14 \|.*)\*\*PENDIENTE EXTERNO\*\*', r'\1**CUMPLIDO**'), False, None),
    ('QA-11', 'MAT', 'G0-12 «Verificada = Sí» sin evidencia recibida',
     rsub(MATX, r'(^\| G0-12 \|(?:[^|]*\|){6} )No( \|)', r'\1Sí\2'), False, None),
    ('QA-12', 'MAT', 'G0-02 CUMPLIDO con un adjunto inexistente',
     rsub(MATX, r'^\| G0-02 \|.*$', '| G0-02 | Revisión jurídica | Informe | [informe](adjuntos/G0-02_informe_2026-10-05.pdf) '
          '| Correo | Abogado X | 2026-10-05 | Sí | **CUMPLIDO** | — |'), False, None),
    ('QA-13', 'MAT', 'Resumen de la matriz incoherente',
     sub(MATX, '| PENDIENTE EXTERNO | G0-02, G0-03, G0-12, G0-14 | 4 |',
         '| PENDIENTE EXTERNO | G0-02, G0-03, G0-12, G0-14 | 3 |'), False, None),
    ('QA-14', 'DEC', 'G0 = APROBADA CON RESTRICCIONES con pendientes obligatorios',
     sub('F34B_Decision_G0.md', '- **G0 = NO APROBADA.**', '- **G0 = APROBADA CON RESTRICCIONES.**'), False, None),
    ('QA-15', 'DEC', 'G0 = APROBADA (B + C)', sub('README.md', '**G0 = NO APROBADA**', '**G0 = APROBADA**'), False, None),
    ('QA-16', 'DEC', 'ADR-005 = APROBADA sin acta registrada',
     sub('README.md', '**ADR-005 = PROPUESTA**', '**ADR-005 = APROBADA**'), False, None),
    ('QA-17', 'DEC', 'La decisión contradice la matriz (G0-02 CUMPLIDO)',
     sub('F34B_Decision_G0.md', '| G0-02 | PENDIENTE EXTERNO | Ninguna | PENDIENTE EXTERNO |',
         '| G0-02 | PENDIENTE EXTERNO | Ninguna | CUMPLIDO |'), False, None),
    ('QA-18', 'SCOPE', 'Alcance C habilitado automáticamente',
     sub('F34B_Decision_G0.md', '- **Alcance C: no habilitado.**', '- **Alcance C: habilitado junto con B.**'),
     False, None),
    ('QA-19', 'SCOPE', 'Frase que habilita el alcance C',
     sub('F34B_Decision_G0.md', '## 5. Fases', 'Con esta fase el alcance C queda habilitado.\n\n## 5. Fases'),
     False, None),
    ('QA-20', 'PHASE', 'F35–F40 desbloqueadas sin decisión G0 válida',
     sub('F34B_Decision_G0.md', '- **F35–F40 = BLOQUEADAS.**', '- **F35–F40 = HABILITADAS.**'), False, None),
    ('QA-21', 'PHASE', 'F35 marcada HABILITADA en la tabla de fases',
     sub('F34B_Decision_G0.md', '| F35 Pipeline de evidencia | BLOQUEADA |', '| F35 Pipeline de evidencia | HABILITADA |'),
     False, None),
    ('QA-22', 'DATA', 'Datos reales autorizados sin aprobación específica',
     sub('F34B_Decision_G0.md', '## 6. Evidencias faltantes',
         'Los datos reales quedan autorizados con consentimiento.\n\n## 6. Evidencias faltantes'), False, None),
    ('QA-23', 'DATA', 'Se elimina la prohibición de datos reales',
     sub(PRI, '**Los datos reales siguen PROHIBIDOS.**', '**Los datos reales pueden usarse.**'), False, None),
    ('QA-24', 'LNK', 'Enlace a un adjunto inexistente',
     sub('README.md', '[`adjuntos/`](adjuntos/README.md) | Evidencia real | Vacía |',
         '[`adjuntos/`](adjuntos/README.md) | Evidencia real | [acta](adjuntos/G0-14_acta.pdf) |'), False, None),
    # ---- auditoría F34B-M02: identidad, quórum y roles (contexto simulado: el adjunto existe, solo falla la identidad)
    ('QA-25', 'IDN', 'ADR-005: la misma identidad firma las tres filas de integrante',
     set_rows(ACTA, team_rows([U, U, U], 'APRUEBA') + [CONS_PEND]), True, 'G0-14'),
    ('QA-26', 'IDN', 'ADR-005: un integrante repetido y otro ausente',
     set_rows(ACTA, team_rows([U, D2, U], 'APRUEBA') + [CONS_PEND]), True, 'G0-14'),
    ('QA-27', 'IDN', 'ADR-005: firma como integrante una persona ajena al equipo',
     set_rows(ACTA, team_rows([U, D2, 'Persona Externa Control'], 'APRUEBA') + [CONS_PEND]), True, 'G0-14'),
    ('QA-28', 'MAT', 'ADR-005: el docente consultivo sustituye al tercer integrante y la matriz marca CUMPLIDO',
     chain(set_rows(ACTA, team_rows([U, D2], 'APRUEBA') + [PEND, row('Persona Docente Control', CONSULTIVE_ROLE,
                                                                       'APRUEBA', 'cons')]),
           rsub(MATX, r'^\| G0-14 \|.*$', '| G0-14 | Gobierno del ADR | Acta | ' + CTRL.format('acta') +
                ' | Adjunto | Equipo | 2026-10-05 | Sí | **CUMPLIDO** | — |')), True, 'G0-14'),
    ('QA-29', 'IDN', 'ADR-005: cuatro filas de integrante (quórum alterado)',
     set_rows(ACTA, team_rows([U, D2, T3], 'APRUEBA') + [PEND, CONS_PEND]), True, 'G0-14'),
    ('QA-30', 'IDN', 'Jurídico: firma con rol de Postulante',
     set_rows(JUR, [row('Persona Legal Control', 'Postulante', 'SIN OBJECIÓN', 'jur')]), True, 'G0-02'),
    ('QA-31', 'IDN', 'Jurídico: lo firma un integrante del equipo como abogado',
     set_rows(JUR, [row(U, 'Abogado', 'SIN OBJECIÓN', 'jur')]), True, 'G0-02'),
    ('QA-32', 'IDN', 'Privacidad: aprobación con rol de Evaluador',
     set_rows(PRI, [row('Persona Responsable Control', 'Evaluador', 'APRUEBA', 'p1'),
                    row('Persona Asesora Control', 'Revisión jurídica de privacidad', 'APRUEBA', 'p2')]), True, 'G0-03'),
    ('QA-33', 'IDN', 'Privacidad: la misma persona firma como responsable y como revisión jurídica',
     set_rows(PRI, [row('Persona Responsable Control', 'Responsable del tratamiento', 'APRUEBA', 'p1'),
                    row('Persona Responsable Control', 'Revisión jurídica de privacidad', 'APRUEBA', 'p2')]),
     True, 'G0-03'),
    ('QA-34', 'IDN', 'Privacidad: dos filas jurídicas y ningún responsable del tratamiento',
     set_rows(PRI, [row('Persona Asesora Control', 'Revisión jurídica de privacidad', 'APRUEBA', 'p1'),
                    row('Persona Legal Control', 'Abogado', 'APRUEBA', 'p2')]), True, 'G0-03'),
    ('QA-35', 'IDN', 'Necesidad: validación firmada con rol de Postulante',
     set_rows(NEC, [row('Persona Docente Control', 'Postulante', 'NECESIDAD VALIDADA', 'n1'),
                    ['—', 'RR. HH.', '—', 'PENDIENTE', '—', '—', 'PENDIENTE'],
                    ['—', 'Administración', '—', 'PENDIENTE', '—', '—', 'PENDIENTE'],
                    ['—', 'Representante institucional', '—', 'PENDIENTE', '—', '—', 'PENDIENTE']]), True, 'G0-12'),
    ('QA-36', 'IDN', 'Necesidad: rol arbitrario «Coordinador académico»',
     sub(NEC, '| — | Administración | — |', '| — | Coordinador académico | — |'), False, None),
    ('QA-37', 'IDN', 'Necesidad: la misma persona firma como docente y como representante institucional',
     set_rows(NEC, [row('Persona Docente Control', 'Docente del curso', 'NECESIDAD VALIDADA', 'n1'),
                    ['—', 'RR. HH.', '—', 'PENDIENTE', '—', '—', 'PENDIENTE'],
                    ['—', 'Administración', '—', 'PENDIENTE', '—', '—', 'PENDIENTE'],
                    row('Persona Docente Control', 'Representante institucional', 'NECESIDAD VALIDADA', 'n2')]),
     True, 'G0-12'),
    ('QA-38', 'IDN', 'Threat model: identidad duplicada en la aceptación del equipo',
     set_rows(TM, team_rows([U, U, D2], 'ACEPTA')), True, 'G0-09'),
    ('QA-39', 'REC', 'Aprobación con identidades y roles válidos pero sin adjunto',
     set_rows(ACTA, [[n, TEAM_ROLE, DAY, 'APRUEBA', '—', '—', 'REGISTRADO'] for n in SYN_TEAM] + [CONS_PEND]),
     True, 'G0-14'),
    ('QA-40', 'IDN', 'Fecha y decisión con el rol escrito como identidad',
     set_rows(TM, [row(TEAM_ROLE, TEAM_ROLE, 'ACEPTA', 't1')] + team_rows([D2, T3], 'ACEPTA')), True, 'G0-09'),
    ('QA-41', 'IDN', 'Fecha y decisión con una identidad de una sola palabra',
     set_rows(JUR, [row('Abogado', 'Abogado', 'SIN OBJECIÓN', 'jur')]), True, 'G0-02'),
    ('QA-42', 'IDN', 'ADR-005: un integrante del equipo firma también la fila consultiva del docente',
     set_rows(ACTA, team_rows([U, D2, T3], 'APRUEBA') + [row(U, CONSULTIVE_ROLE, 'APRUEBA', 'cons')]), True, 'G0-14'),
    ('QA-43', 'IDN', 'Jurídico: rol cambiado en una fila pendiente de la plantilla',
     sub(JUR, '| — | Abogado o responsable legal | — | PENDIENTE |', '| — | Postulante | — | PENDIENTE |'), False, None),
]


def positive_control():
    """Con evidencia completa SIMULADA (integrantes sintéticos, roles válidos, identidades distintas y adjuntos CONTROL
    que solo existen en memoria), la regla SÍ permite G0 = APROBADA CON RESTRICCIONES sin habilitar C ni datos reales.
    Nunca usa nombres reales ni archivos del repositorio."""
    D = read_all()
    D = chain(
        set_rows(ACTA, team_rows(SYN_TEAM, 'APRUEBA', link='acta') + [CONS_PEND]),
        set_rows(TM, team_rows(SYN_TEAM, 'ACEPTA', link='tm')),
        set_rows(JUR, [row('Persona Legal Control', 'Abogado o responsable legal', 'SIN OBJECIÓN', 'jur')], 0),
        set_rows(JUR, [row('Persona Legal Control', 'Abogado o responsable legal', 'NO APLICA', 'eia')], 1),
        set_rows(PRI, [row('Persona Responsable Control', 'Responsable del tratamiento', 'APRUEBA', 'p1'),
                       row('Persona Asesora Control', 'Revisión jurídica de privacidad', 'APRUEBA', 'p2')]),
        set_rows(NEC, [row('Persona Docente Control', 'Docente del curso', 'NECESIDAD VALIDADA', 'nec'),
                       ['—', 'RR. HH.', '—', 'PENDIENTE', '—', '—', 'PENDIENTE'],
                       ['—', 'Administración', '—', 'PENDIENTE', '—', '—', 'PENDIENTE'],
                       ['—', 'Representante institucional', '—', 'PENDIENTE', '—', '—', 'PENDIENTE']]),
    )(D)
    m = D[MATX]
    for gid in sorted(EXTERNAL):
        m = re.sub(r'^\| ' + gid + r' \| ([^|]*) \| ([^|]*) \|.*$',
                   lambda x: f'| {gid} | {x.group(1)} | {x.group(2)} | {CTRL.format(gid)} | Adjunto simulado | Control | '
                             f'{DAY} | Sí | **CUMPLIDO** | Control positivo |', m, flags=re.M)
    m = re.sub(r'^\| CUMPLIDO \| .*$', '| CUMPLIDO | (14 criterios) | 14 |', m, flags=re.M)
    m = re.sub(r'^\| (PARCIAL|PENDIENTE EXTERNO) \| .*$', r'| \1 | — | 0 |', m, flags=re.M)
    D[MATX] = m
    d = D['F34B_Decision_G0.md']
    d = re.sub(r'^(\| G0-\d\d \| [^|]* \| [^|]* \| )(PENDIENTE EXTERNO|PARCIAL)( \|)$', r'\1CUMPLIDO\3', d, flags=re.M)
    d = d.replace('- **G0 = NO APROBADA.**', '- **G0 = APROBADA CON RESTRICCIONES.**')
    d = d.replace('- **ADR-005 = PROPUESTA.**', '- **ADR-005 = APROBADA.**')
    D['F34B_Decision_G0.md'] = d
    return D, run_rules(D, SIM)


# ---------------------------------------------------------------- git
def git(*a):
    p = subprocess.run(['git', *a], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    if p.returncode != 0:
        raise RuntimeError(f'consulta Git fallida (código {p.returncode}); alcance desconocido')
    return p.stdout


F34A_VALIDATOR = 'docs/academico/tools/f34a/validate_f34a.py'   # corregido en F34B-M01 por encargo de la auditoría
GOVERNANCE_FILES = frozenset({'CLAUDE.md', 'README.md', 'docs/PROGRESS.md',
                              'docs/academico/ACADEMIC_BASELINE.md'})
CLOSURE_SUBJECTS = [
    'docs(governance): close F34B with G0 still not approved',
    'docs(academic): add F34B external evidence package and validator',
    'test(academic): harden F34A validator for later phases',
]


def closure_scope(subjects, committed, dirty):
    """Solo admite el gobierno ya comprometido en C tras B/A; nunca nuevas ediciones ni fases futuras."""
    if subjects != CLOSURE_SUBJECTS or not committed or not committed <= GOVERNANCE_FILES or dirty:
        return frozenset()
    return frozenset(committed)


def git_checks():
    out = []
    changed = set(git('diff', '--name-only', BASE).split()) | set(git('ls-files', '--others', '--exclude-standard').split())
    allowed = ('docs/academico/g0-evidence/', 'docs/academico/tools/f34b/')
    subjects = git('log', '-3', '--format=%s').splitlines()
    committed = set(git('diff-tree', '--no-commit-id', '--name-only', '-r', 'HEAD').splitlines())
    dirty = set(git('diff', '--name-only', 'HEAD', '--', *sorted(GOVERNANCE_FILES)).splitlines())
    governance = closure_scope(subjects, committed, dirty)
    fuera = sorted(p for p in changed if not p.startswith(allowed) and p != F34A_VALIDATOR and p not in governance)
    if fuera:
        out.append(f'cambios fuera del alcance de F34B: {fuera[:5]}')
    protected = ['app', 'routes', 'config', 'database', 'resources', 'tests', 'cypress', 'ml-service', 'composer.json',
                 'composer.lock', 'package.json', 'package-lock.json', 'docker-compose.yml', 'Dockerfile',
                 'docs/v1.1/scope-preliminary.md', 'docs/final-report/traceability-master.md',
                 'docs/rf-implementation-matrix.md', 'docs/assumptions.md', 'docs/academico/diseno-inteligente',
                 'docs/academico/datos-sinteticos', 'docs/academico/g0-readiness', 'docs/academico/tools/f34a']
    tocados = [p for p in git('diff', '--name-only', BASE, '--', *protected).split() if p != F34A_VALIDATOR]
    if tocados:
        out.append(f'runtime, baseline, F33, F34 o documentos F34A modificados: {tocados[:5]}')
    adr = open(os.path.join(ROOT, 'docs', 'academico', 'diseno-inteligente', 'F33_ADR_005_G0.md'), encoding='utf-8').read()
    if '- **Estado:** **PROPUESTA**' not in adr:
        out.append('ADR-005 ya no figura como PROPUESTA')
    return out


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    checks = []
    add = lambda ok, msg: checks.append((bool(ok), msg))
    for n in FILES + [os.path.join('adjuntos', 'README.md')]:
        add(os.path.isfile(os.path.join(DOCS, n)), f'documento presente: {n}')
    add(len(REAL.roster) == 3, f'lista de integrantes leída de CLAUDE.md: {len(REAL.roster)} integrantes')
    D = read_all()
    res = run_rules(D)
    for rid, viol in res.items():
        add(not viol, f'{rid}: {len(viol)} violaciones' + (f' — {viol[:2]}' if viol else ''))

    for cid, rule, what, mut, sim, crit in CASES:
        ctx = SIM if sim else REAL
        try:
            Dm = mut(D)
        except AssertionError as e:
            add(False, f'{cid}: la mutación no se pudo aplicar ({e})')
            continue
        r = run_rules(Dm, ctx)
        ok = bool(r.get(rule)) and (crit is None or derive(Dm, ctx)[crit] != 'CUMPLIDO')
        add(ok, f'{cid} detectado por {rule}' + (f' y {crit} no queda CUMPLIDO' if crit else '') + f': {what}')
    add(len(CASES) >= 40, f'casos negativos: {len(CASES)}')

    Dp, rp = positive_control()
    bad = {k: v for k, v in rp.items() if v}
    add(not bad and g0_ok(Dp, SIM) and all(v == 'CUMPLIDO' for v in derive(Dp, SIM).values()),
        f'control positivo (simulado): identidades distintas y roles válidos permiten G0 APROBADA CON RESTRICCIONES {bad}')
    add(not g0_ok(Dp, REAL) and run_rules(Dp)['REC'],
        'control positivo: con los archivos reales del repositorio no es evidencia (los adjuntos CONTROL no existen)')
    ctrl_links = set(re.findall(r'adjuntos/CONTROL-[^)\s]+', '\n'.join(Dp.values())))
    add(ctrl_links and not any(real_exists(p) for p in ctrl_links),
        f'control positivo: ninguno de sus {len(ctrl_links)} adjuntos simulados existe en disco')
    add(not ({ident(x) for x in SYN_TEAM} & set(REAL.roster)),
        'control positivo: los integrantes sintéticos no coinciden con integrantes reales')

    gv = git_checks()
    add(not gv, f'GIT: alcance de F34B; runtime, baseline, ADR-005, F33, F34 y documentos F34A sin cambios: {gv}')
    add(closure_scope(CLOSURE_SUBJECTS, {'CLAUDE.md'}, set()) == {'CLAUDE.md'},
        'cierre: admite únicamente el gobierno comprometido en C tras B/A')
    add(not closure_scope(CLOSURE_SUBJECTS, {'CLAUDE.md'}, {'CLAUDE.md'}),
        'cierre: rechaza nuevas ediciones de gobierno pendientes')
    add(not closure_scope(['fase futura', *CLOSURE_SUBJECTS[1:]], {'CLAUDE.md'}, set()),
        'cierre: no habilita commits de fases futuras')
    add(not closure_scope(CLOSURE_SUBJECTS, {'app/Models/User.php'}, set()),
        'cierre: rechaza archivos fuera de los cuatro documentos de gobierno autorizados')

    atts = sorted(f for f in os.listdir(ATT) if f != 'README.md') if os.path.isdir(ATT) else []
    add(not any('CONTROL' in f.upper() for f in atts), 'adjuntos/: ningún archivo de control mezclado con evidencia real')
    der = derive(D, REAL)
    fallas = [m for ok, m in checks if not ok]
    for m in fallas:
        print('FALLA', m)
    print(f'INFO adjuntos reales: {len(atts)} {atts} · estados derivados de los registros: {der}')
    print(f'INFO G0 aprobable con la evidencia actual: {"sí" if g0_ok(D, REAL) else "no"}')
    print(f'validate_f34b: {len(checks) - len(fallas)} comprobaciones correctas, {len(fallas)} fallas')
    sys.exit(1 if fallas else 0)


if __name__ == '__main__':
    main()
