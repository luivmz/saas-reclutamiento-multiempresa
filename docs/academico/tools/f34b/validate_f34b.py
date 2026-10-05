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
  EVD   (F34C) cada adjunto del acta y de la aceptación del threat model existe, coincide con su SHA-256 y su formato
        real registrados, declara la decisión con fecha y confirmación, su nombre declarado corresponde a un único
        integrante (el de la fila que lo usa) y no hay adjuntos sin registrar; si falla, G0-14 y G0-09 no quedan CUMPLIDO.
        Corrección F34C: identidad solo por nombre completo exacto o correspondencia REVISADA (sin distancia de edición);
        fechas reales de calendario; control temporal (DISCREPANCIA bloquea el cierre; solo la resuelve una
        «Confirmación adicional» válida del mismo integrante, con la misma fecha y decisiones, conservando la original);
        concordancia de fecha registro/evidencia; el remitente visible puede faltar (mensaje propio de WhatsApp).
        ADR-005 conserva su estado canónico PROPUESTA; la aprobación interna del equipo se registra aparte.
  LNK   enlaces y anclas;  GIT  alcance de la rama, F34A, ADR-005, baseline y runtime sin cambios
Incluye casos negativos y un control positivo (todo en memoria; no crea adjuntos). El control positivo usa una lista
de integrantes SINTÉTICA y adjuntos simulados con prefijo CONTROL; nunca nombres reales ni archivos del repositorio.
Uso: python docs/academico/tools/f34b/validate_f34b.py
"""
import datetime as dt
import hashlib
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


def real_sha(rel):
    p = os.path.normpath(os.path.join(DOCS, rel))
    if not os.path.isfile(p):
        return None
    with open(p, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def real_fmt(rel):
    """Formato real por la firma del archivo (no por la extensión)."""
    p = os.path.normpath(os.path.join(DOCS, rel))
    if not os.path.isfile(p):
        return None
    with open(p, 'rb') as f:
        head = f.read(8)
    if head.startswith(b'\xff\xd8\xff'):
        return 'JPEG'
    if head == b'\x89PNG\r\n\x1a\n':
        return 'PNG'
    if head.startswith(b'%PDF'):
        return 'PDF'
    return 'DESCONOCIDO'


def real_listing():
    return sorted('adjuntos/' + f for f in os.listdir(ATT) if f != 'README.md') if os.path.isdir(ATT) else []


class Ctx:
    """Contexto de verificación: cómo se comprueba un adjunto (existencia, SHA-256, formato, listado de la carpeta)
    y cuál es la lista de integrantes."""

    def __init__(self, exists, roster, sha=None, fmt=None, listing=None):
        self.exists, self.roster = exists, roster
        self.sha = sha or (lambda rel: None)
        self.fmt = fmt or (lambda rel: None)
        self.listing = listing or (lambda: [])

    def __call__(self, rel):
        return self.exists(rel)


REAL = Ctx(real_exists, team_roster(), real_sha, real_fmt, real_listing)


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
                if who in ('', '—') or not valid_date(date):
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
        m = canonical_member(r[0], roster)   # nombre completo exacto (F34C-M02): sin coincidencias parciales
        if m is None:
            out.append(f'{n}: «{r[0]}» no es el nombre completo de exactamente un integrante del equipo')
            continue
        if ident(r[0]) in seen_ids or m in seen_members:
            out.append(f'{n}: identidad repetida: un mismo integrante firma más de una fila')
        seen_ids.append(ident(r[0]))
        seen_members.append(m)
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


# ---------------------------------------------------------------- verificación de adjuntos (F34C, corregida F34C-M01..M03)
EVD_HEADER = ['Adjunto', 'Tipo', 'SHA-256', 'Formato', 'Remitente visible', 'Nombre declarado', 'Integrante', 'ADR-005',
              'Modelo de amenazas', 'Fecha declarada', 'Confirmación', 'Control temporal', 'Observaciones']
ALIAS_HEADER = ['Variante declarada', 'Integrante', 'Revisión']
FORMATS = {'JPEG', 'PNG', 'PDF'}
EV_TYPES = {'Única', 'Original (histórica)', 'Confirmación adicional'}
SENDER_OWN = '— (mensaje propio)'
# Correspondencias de identidad REVISADAS (F34C-M02). Sin coincidencia aproximada: cualquier variante que no esté aquí
# ni coincida exactamente con el nombre completo de un integrante requiere revisión manual y falla. Añadir una variante
# exige cambiar esta lista y la tabla del acta en el mismo cambio revisado.
REVIEWED_ALIASES = {
    'Peña Antony': 'Peña Arroyo Anthony',
    'Anthony Peña': 'Peña Arroyo Anthony',
    'Fredy Coronación': 'Coronacion Meza Fredy',
    'Freddy Coronación': 'Coronacion Meza Fredy',
    'Fredy Sistemas': 'Coronacion Meza Fredy',          # remitente visible en la captura de Fredy (F34C-M02-R1)
    'Luis Antonio Vila Meza': 'Vila Meza Luis Antonio',
}


def valid_date(s):
    """Fecha ISO real de calendario (rechaza 2026-99-99, 2026-02-30 y otros formatos)."""
    if not DATE.fullmatch(s or ''):
        return False
    try:
        dt.date.fromisoformat(s)
    except ValueError:
        return False
    return True


def canonical_member(name, roster):
    """Índice del integrante cuyo nombre completo coincide EXACTAMENTE (mismas palabras, sin tildes ni orden)."""
    i = ident(name)
    hits = [k for k, m in enumerate(roster) if len(i) >= 2 and i == m]
    return hits[0] if len(hits) == 1 else None


def declared_member(name, roster, aliases=None):
    """Integrante de un nombre declarado: coincidencia exacta con el nombre completo o correspondencia revisada.
    None si no hay correspondencia explícita (requiere revisión manual)."""
    aliases = REVIEWED_ALIASES if aliases is None else aliases
    k = canonical_member(name, roster)
    if k is not None:
        return k
    for variant, target in aliases.items():
        if ident(variant) == ident(name):
            return canonical_member(target, roster)
    return None


def table_after(text, header):
    rows_, cur = [], False
    for ln in text.splitlines():
        if not ln.startswith('|'):
            cur = False
            continue
        c = cells(ln)
        if c == header:
            cur = True
        elif cur and not set(ln.replace('|', '').strip()) <= set('-: '):
            rows_.append(c)
    return rows_


def evidence_table(text):
    return table_after(text, EVD_HEADER)


def evd(D, ctx):
    """Verificación de los adjuntos que respaldan el acta y la aceptación del threat model:
    existencia, SHA-256 y formato real; identidad por correspondencia exacta o revisada (sin coincidencia aproximada);
    fechas reales de calendario; control temporal (una discrepancia solo se resuelve con una confirmación adicional
    válida del mismo integrante, conservando la original); concordancia de fecha entre registro y evidencia; y ningún
    adjunto sin registrar."""
    out = []
    roster = getattr(ctx, 'roster', REAL.roster)
    acta = D['F34B_Acta_Aprobacion_ADR005.md']
    # Correspondencias declaradas en el acta = correspondencias revisadas del validador (ni más ni menos).
    doc_alias = {r[0]: r[1] for r in table_after(acta, ALIAS_HEADER) if len(r) == 3}
    if doc_alias != REVIEWED_ALIASES:
        extra = sorted(set(doc_alias.items()) - set(REVIEWED_ALIASES.items()))
        out.append(f'correspondencias de identidad del acta distintas de las revisadas: {extra or "faltan filas"}')
    ev = {}
    for r in evidence_table(acta):
        if len(r) != len(EVD_HEADER):
            out.append(f'evidencia con {len(r)} columnas')
            continue
        links = ATT_LINK.findall(r[0])
        if len(links) != 1:
            out.append(f'fila de evidencia sin un único adjunto: {r[0]}')
            continue
        rel = links[0]
        if rel in ev:
            out.append(f'{rel}: registrado dos veces')
        ev[rel] = r
    member, valid_ev = {}, {}
    for rel, r in ev.items():
        (_, typ, sha_, fmt_, sender, declared, integ, adr, tmd, fecha, conf, temporal, _obs) = r
        ok = True
        if not ctx.exists(rel):
            out.append(f'{rel}: adjunto inexistente')
            ok = False
        else:
            if sha_.strip('`') != ctx.sha(rel):
                out.append(f'{rel}: SHA-256 registrado distinto del archivo')
                ok = False
            if fmt_ not in FORMATS or fmt_ != ctx.fmt(rel):
                out.append(f'{rel}: formato registrado «{fmt_}» distinto del real «{ctx.fmt(rel)}»')
                ok = False
        if typ not in EV_TYPES:
            out.append(f'{rel}: tipo de evidencia «{typ}» no admitido')
            ok = False
        md = declared_member(declared, roster)
        mi = canonical_member(integ, roster)
        if md is None:
            out.append(f'{rel}: el nombre declarado «{declared}» no tiene correspondencia exacta ni revisada con un '
                       f'integrante (requiere revisión manual)')
            ok = False
        if mi is None or md != mi:
            out.append(f'{rel}: el integrante registrado «{integ}» no coincide con el nombre declarado')
            ok = False
        # Remitente visible (F34C-M02-R1). Ausente solo como «— (mensaje propio)» y con el nombre COMPLETO declarado;
        # presente solo si es el nombre completo o una variante revisada del MISMO integrante. Lo demás requiere revisión.
        if sender == SENDER_OWN:
            if canonical_member(declared, roster) is None:
                out.append(f'{rel}: remitente ausente sin nombre completo declarado en el mensaje (requiere revisión)')
                ok = False
        elif sender.startswith('—') or not sender:
            out.append(f'{rel}: remitente vacío o sin justificar; solo se admite «{SENDER_OWN}»')
            ok = False
        else:
            ms = declared_member(sender, roster)
            if ms is None:
                out.append(f'{rel}: remitente visible «{sender}» sin correspondencia exacta ni revisada (requiere revisión)')
                ok = False
            elif ms != md or ms != mi:
                out.append(f'{rel}: el remitente visible «{sender}» corresponde a otro integrante')
                ok = False
        if adr not in ('APROBADA', '—') or tmd not in ('ACEPTADO', '—') or (adr, tmd) == ('—', '—'):
            out.append(f'{rel}: la evidencia no declara ninguna decisión válida')
            ok = False
        if not valid_date(fecha):
            out.append(f'{rel}: fecha declarada «{fecha}» inexistente o con formato inválido')
            ok = False
        if conf != 'Sí':
            out.append(f'{rel}: sin confirmación explícita')
            ok = False
        member[rel] = md
        valid_ev[rel] = ok
    # Control temporal.
    temporal_ok = {}
    for rel, r in ev.items():
        typ, fecha, temporal = r[1], r[9], r[11]
        if temporal == 'CONFORME':
            temporal_ok[rel] = typ in ('Única', 'Confirmación adicional')
            if typ == 'Original (histórica)':
                out.append(f'{rel}: una evidencia original histórica debe tener su discrepancia RESUELTA')
        elif temporal == 'DISCREPANCIA':
            temporal_ok[rel] = False
        elif temporal.startswith('RESUELTA'):
            conf_links = ATT_LINK.findall(temporal)
            c = ev.get(conf_links[0]) if len(conf_links) == 1 else None
            good = (c is not None and typ == 'Original (histórica)' and c[1] == 'Confirmación adicional'
                    and c[11] == 'CONFORME' and valid_ev.get(conf_links[0]) and member.get(conf_links[0]) == member[rel]
                    and c[9] == fecha and (r[7] == '—' or c[7] == r[7]) and (r[8] == '—' or c[8] == r[8]))
            if not good:
                out.append(f'{rel}: la confirmación adicional no resuelve la discrepancia (debe ser una confirmación '
                           f'válida, CONFORME, del mismo integrante, con la misma fecha y las mismas decisiones)')
            temporal_ok[rel] = bool(good)
        else:
            out.append(f'{rel}: control temporal «{temporal}» no admitido')
            temporal_ok[rel] = False
    for rel, r in ev.items():
        if r[1] == 'Confirmación adicional' and not any(
                ATT_LINK.findall(o[11]) == [rel] for o in ev.values() if o[11].startswith('RESUELTA')):
            out.append(f'{rel}: confirmación adicional que no resuelve ninguna evidencia original')
    for rel in ctx.listing():
        if rel not in ev:
            out.append(f'{rel}: adjunto presente en adjuntos/ sin registrar ni verificar')
    # Registros del acta y de la aceptación del threat model.
    for n, col, label in (('F34B_Acta_Aprobacion_ADR005.md', 7, 'ADR-005'),
                          ('F34B_Aceptacion_Threat_Model.md', 8, 'modelo de amenazas')):
        tab = records(D[n])
        used = []
        for r in (tab[0] if tab else []):
            if len(r) != 7 or r[1] != TEAM_ROLE or r[6] != 'REGISTRADO':
                continue
            m_row = canonical_member(r[0], roster)
            usable = []
            for rel in ATT_LINK.findall(r[4]):
                e = ev.get(rel)
                if e is None:
                    out.append(f'{n}: {rel} no figura en la verificación de evidencias')
                    continue
                if m_row is None or member.get(rel) != m_row:
                    out.append(f'{n}: la fila de «{r[0]}» usa el adjunto de otra persona ({rel})')
                if rel in used:
                    out.append(f'{n}: el mismo adjunto respalda dos filas ({rel})')
                used.append(rel)
                if not temporal_ok.get(rel):
                    out.append(f'{n}: {rel} tiene una discrepancia temporal pendiente: el registro no puede cerrarse')
                elif valid_ev.get(rel) and e[col] not in ('—', ''):
                    usable.append(e)
            if not usable:
                out.append(f'{n}: la fila de «{r[0]}» no tiene evidencia válida con la decisión sobre {label}')
            elif not valid_date(r[2]) or all(e[9] != r[2] for e in usable):
                out.append(f'{n}: la fecha del registro de «{r[0]}» ({r[2]}) no concuerda con la evidencia confirmada')
    return out


def derive(D, exists):
    """Estado de cada criterio externo derivado SOLO de registros con evidencia existente e identidad válida.

    Un formulario con cualquier violación de identidad o rol no produce CUMPLIDO ni RECHAZADO; tampoco el acta ni la
    aceptación del threat model si la verificación de sus adjuntos (EVD) falla."""
    bad = idn_forms(D, exists)
    if evd(D, exists):
        bad['F34B_Acta_Aprobacion_ADR005.md'] = bad['F34B_Acta_Aprobacion_ADR005.md'] + ['EVD']
        bad['F34B_Aceptacion_Threat_Model.md'] = bad['F34B_Aceptacion_Threat_Model.md'] + ['EVD']

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
            if not ver.startswith('Sí') or not valid_date(r[6].strip()) or ev in ('Ninguna', '—', ''):
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
CLAIM_ADR_EQ = re.compile(r'ADR-005\s*=\s*\**\s*APROBAD', re.I)                       # estricta
CLAIM_ADR_VERB = re.compile(r'ADR-005 (?:fue|ha sido|está|queda|quedó) aprobad', re.I)  # admite negación en la línea
ADR_CANON = 'ADR-005 = PROPUESTA'
ADR_TEAM = 'APROBACIÓN INTERNA DEL EQUIPO REGISTRADA'
ADR_DISCLAIMER = 'no es una aprobación jurídica'


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
            # El estado canónico de ADR-005 es PROPUESTA: ningún documento lo declara APROBADO (F34C).
            if CLAIM_ADR_EQ.search(ln) or (CLAIM_ADR_VERB.search(ln) and not NEG.search(ln)):
                out.append(f'{n}:{i}: declara ADR-005 aprobado; su estado canónico sigue siendo PROPUESTA')
            if ADR_TEAM in ln and not adr_ok:
                out.append(f'{n}:{i}: declara la aprobación interna del equipo sin acta registrada y verificada')
    d = D['F34B_Decision_G0.md']
    if not ok and '- **G0 = NO APROBADA.**' not in d:
        out.append('faltan criterios y la decisión no declara «G0 = NO APROBADA»')
    for n in ('README.md', 'F34B_Decision_G0.md', 'F34B_Acta_Aprobacion_ADR005.md'):
        if ADR_CANON not in D[n]:
            out.append(f'{n}: no declara el estado canónico «{ADR_CANON}»')
    if adr_ok:
        # Aprobación interna del equipo: se registra aparte y nunca como aprobación jurídica, institucional ni de G0.
        for n in ('README.md', 'F34B_Decision_G0.md', 'F34B_Acta_Aprobacion_ADR005.md'):
            if ADR_TEAM not in D[n] or ADR_DISCLAIMER not in D[n].lower():
                out.append(f'{n}: acta válida sin «{ADR_TEAM}» y la aclaración «{ADR_DISCLAIMER}»')
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


RULES = [('REC', rec), ('ANS', ans), ('IDN', idn), ('EVD', evd), ('MAT', mat), ('DEC', dec), ('SCOPE', scope),
         ('PHASE', phase), ('DATA', data), ('LNK', lnk)]


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
CTRL_SHA = '0' * 64
SIM = Ctx(lambda p: p.startswith('adjuntos/CONTROL-'), [ident(x) for x in SYN_TEAM],
          sha=lambda p: CTRL_SHA if p.startswith('adjuntos/CONTROL-') else None,
          fmt=lambda p: 'JPEG' if p.startswith('adjuntos/CONTROL-') else None,
          listing=lambda: [])
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
SENDER_LUIS_CONF = r'(\[Luis_Vila_confirmación\].*?\| JPEG \| )— \(mensaje propio\)( \|)'
CONS_ROW = '| — | Docente del curso (consultivo, opcional) | — | PENDIENTE | — | — | PENDIENTE |'
FAKE = '[acta](adjuntos/G0-14_acta-adr005_2026-10-05.pdf)'
# Evidencia real registrada en F34C (los casos la alteran solo en memoria).
EV_A = 'adjuntos/G0-ADR005-ThreatModel_Anthony_Pena_2026-10-04.png'
EV_F = 'adjuntos/G0-ADR005-ThreatModel_Fredy_Coronacion_2026-10-04.png'
EV_L = 'adjuntos/G0-ADR005-ThreatModel_Luis_Vila_2026-10-04.png'


def set_evidence(new_rows):
    """Sustituye las filas de la tabla de verificación de evidencias del acta."""
    def f(D):
        D = dict(D)
        out, inside = [], False
        for ln in D[ACTA].splitlines():
            c = cells(ln) if ln.startswith('|') else []
            if c == EVD_HEADER:
                inside = True
                out.append(ln)
                continue
            if inside and ln.startswith('|'):
                if set(ln.replace('|', '').strip()) <= set('-: '):
                    out.append(ln)
                    out += ['| ' + ' | '.join(r) + ' |' for r in new_rows]
                continue
            inside = False
            out.append(ln)
        D[ACTA] = '\n'.join(out) + '\n'
        return D
    return f


def ctx_without(fragment, extra=()):
    """Contexto real en el que falta un adjunto (fragment) o aparecen adjuntos extra sin registrar."""
    return Ctx(lambda p: (real_exists(p) and fragment not in p) or p in extra, REAL.roster,
               lambda p: real_sha(p) if fragment not in p else None, lambda p: real_fmt(p) or ('JPEG' if p in extra else None),
               lambda: [x for x in real_listing() if fragment not in x] + list(extra))


# (id, regla, descripción, mutación, contexto simulado, criterio que NO puede quedar CUMPLIDO)
CASES = [
    ('QA-01', 'REC', 'Aprobación (fila consultiva) sin responsable, fecha ni evidencia',
     sub(ACTA, CONS_ROW, '| — | Docente del curso (consultivo, opcional) | — | APRUEBA | — | — | REGISTRADO |'), False, None),
    ('QA-02', 'REC', 'Firma inventada: nombre y fecha con un adjunto que no existe',
     sub(ACTA, CONS_ROW, f'| Docente Externo Prueba | Docente del curso (consultivo, opcional) | 2026-10-05 | APRUEBA | '
                         f'{FAKE} | — | REGISTRADO |'), False, None),
    ('QA-03', 'REC', 'Nombre y fecha registrados, pero estado y decisión en PENDIENTE (firma a medias)',
     sub(ACTA, CONS_ROW, '| Docente Externo Prueba | Docente del curso (consultivo, opcional) | 2026-10-05 | PENDIENTE | '
                         '— | — | PENDIENTE |'), False, None),
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
     rsub(TM, r'^(\| Peña Arroyo Anthony \| Integrante del equipo \| 2026-10-04 \| ACEPTA \| )[^|]*\|', r'\1— |'),
     False, 'G0-09'),
    ('QA-10', 'MAT', 'G0-12 marcado CUMPLIDO sin evidencia',
     rsub(MATX, r'(^\| G0-12 \|.*)\*\*PENDIENTE EXTERNO\*\*', r'\1**CUMPLIDO**'), False, None),
    ('QA-11', 'MAT', 'G0-12 «Verificada = Sí» sin evidencia recibida',
     rsub(MATX, r'(^\| G0-12 \|(?:[^|]*\|){6} )No( \|)', r'\1Sí\2'), False, None),
    ('QA-12', 'MAT', 'G0-02 CUMPLIDO con un adjunto inexistente',
     rsub(MATX, r'^\| G0-02 \|.*$', '| G0-02 | Revisión jurídica | Informe | [informe](adjuntos/G0-02_informe_2026-10-05.pdf) '
          '| Correo | Abogado X | 2026-10-05 | Sí | **CUMPLIDO** | — |'), False, None),
    ('QA-13', 'MAT', 'Resumen de la matriz incoherente',
     sub(MATX, '| PENDIENTE EXTERNO | G0-02, G0-03, G0-12 | 3 |', '| PENDIENTE EXTERNO | G0-02, G0-03, G0-12 | 2 |'),
     False, None),
    ('QA-14', 'DEC', 'G0 = APROBADA CON RESTRICCIONES con pendientes obligatorios',
     sub('F34B_Decision_G0.md', '- **G0 = NO APROBADA.**', '- **G0 = APROBADA CON RESTRICCIONES.**'), False, None),
    ('QA-15', 'DEC', 'G0 = APROBADA (B + C)', sub('README.md', '**G0 = NO APROBADA**', '**G0 = APROBADA**'), False, None),
    ('QA-16', 'DEC', 'ADR-005 declarada aprobada con el acta sin registrar',
     set_rows(ACTA, [PEND, PEND, PEND, CONS_PEND]), False, 'G0-14'),
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
     sub('README.md', '[`adjuntos/`](adjuntos/README.md) | Evidencia real | 4 adjuntos del equipo (G0-14 y G0-09) |',
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
    # ---- F34C: evidencia real de G0-14 y G0-09 (mutaciones en memoria; los adjuntos reales no se tocan)
    ('QA-44', 'EVD', 'Falta un adjunto (Anthony Peña) en adjuntos/', lambda D: D, ctx_without('Anthony_Pena'), 'G0-14'),
    ('QA-45', 'IDN', 'Identidad duplicada: Coronacion firma también la fila de Peña',
     rsub(ACTA, r'^\| Peña Arroyo Anthony \|', '| Coronacion Meza Fredy |'), False, 'G0-14'),
    ('QA-46', 'EVD', 'El nombre declarado en la evidencia no coincide con el equipo',
     rsub(ACTA, r'\| Peña Antony \|', '| Carlos Ruiz |'), False, 'G0-14'),
    ('QA-47', 'IDN', 'Responsable del acta ajeno al equipo',
     rsub(ACTA, r'^\| Peña Arroyo Anthony \|', '| Carlos Ruiz Pérez |'), False, 'G0-14'),
    ('QA-48', 'EVD', 'Evidencia sin aprobación de ADR-005',
     rsub(ACTA, r'(\| Peña Arroyo Anthony \| )APROBADA( \| ACEPTADO \|)', r'\1—\2'), False, 'G0-14'),
    ('QA-49', 'EVD', 'Evidencia sin aceptación del modelo de amenazas',
     rsub(ACTA, r'(\| Peña Arroyo Anthony \| APROBADA \| )ACEPTADO( \|)', r'\1—\2'), False, 'G0-09'),
    ('QA-50', 'REC', 'Referencia rota: el acta apunta a un adjunto con otra fecha',
     rsub(ACTA, r'^(\| Peña Arroyo Anthony \|.*?)ThreatModel_Anthony_Pena_2026-10-04', r'\1ThreatModel_Anthony_Pena_2026-10-05'),
     False, 'G0-14'),
    ('QA-51', 'EVD', 'SHA-256 registrado distinto del archivo (adjunto alterado)',
     sub(ACTA, '`a280b48835f4b859a05fe3407f037f01bb9fc62cd2e41fca6cc780408deaba30`', '`' + 'f' * 64 + '`'), False, 'G0-14'),
    ('QA-52', 'EVD', 'Formato registrado distinto del real (PNG frente a JPEG)',
     rsub(ACTA, r'(\[Anthony_Pena\].*?\| )JPEG( \|)', r'\1PNG\2'), False, 'G0-14'),
    ('QA-53', 'EVD', 'La fila de Peña usa el adjunto de otro integrante',
     rsub(ACTA, r'^(\| Peña Arroyo Anthony \| Integrante del equipo \| 2026-10-04 \| APRUEBA \| \[captura\]\()[^)]*\)',
          r'\1' + EV_F + ')'), False, 'G0-14'),
    ('QA-54', 'EVD', 'Adjunto presente en adjuntos/ sin registrar ni verificar', lambda D: D,
     ctx_without('__ninguno__', extra=('adjuntos/G0-extra_sin_registrar_2026-10-04.png',)), None),
    ('QA-55', 'DEC', 'G0 = APROBADA CON RESTRICCIONES con G0-02, G0-03 y G0-12 pendientes',
     sub('README.md', '**G0 = NO APROBADA**', '**G0 = APROBADA CON RESTRICCIONES**'), False, None),
    ('QA-56', 'MAT', 'G0-02 cerrado usando una captura del equipo como revisión jurídica',
     rsub(MATX, r'^\| G0-02 \|.*$', f'| G0-02 | Revisión jurídica | Informe | [captura]({EV_L}) | Equipo | Equipo | 2026-10-04 | '
          'Sí | **CUMPLIDO** | — |'), False, 'G0-02'),
    ('QA-57', 'IDN', 'G0-03 «aprobado» por un integrante del equipo con su captura',
     set_rows(PRI, [['Vila Meza Luis Antonio', 'Responsable del tratamiento', '2026-10-04', 'APRUEBA', f'[captura]({EV_L})',
                     '—', 'REGISTRADO'], ['—', 'Revisión jurídica de privacidad', '—', 'PENDIENTE', '—', '—', 'PENDIENTE']]),
     False, 'G0-03'),
    ('QA-58', 'DEC', 'ADR-005 declarada aprobada con solo dos integrantes registrados',
     rsub(ACTA, r'^\| Vila Meza Luis Antonio \| Integrante del equipo \|.*$', ACTA_ROW), False, 'G0-14'),
    ('QA-59', 'MAT', 'G0-09 CUMPLIDO en la matriz con la aceptación sin registrar',
     set_rows(TM, [PEND, PEND, PEND]), False, 'G0-09'),
    ('QA-60', 'DEC', 'Aprobación interna registrada sin aclarar que no es una aprobación jurídica ni institucional',
     sub('F34B_Decision_G0.md', 'no es una aprobación jurídica, de privacidad ni institucional',
         'es la aprobación definitiva del proyecto'), False, None),
    # ---- auditoría F34C-M01..M03: identidad explícita, fechas reales y control temporal
    ('QA-61', 'EVD', '«Luisa Vila» aceptada como Luis Antonio Vila Meza',
     rsub(ACTA, r'(\[Luis_Vila_confirmación\].*?\| — \(mensaje propio\) \| )Luis Antonio Vila Meza( \|)', r'\1Luisa Vila\2'),
     False, 'G0-14'),
    ('QA-62', 'EVD', '«Luisa Vila» añadida a las correspondencias del acta sin revisión',
     sub(ACTA, '| Luis Antonio Vila Meza | Vila Meza Luis Antonio | F34C, capturas de Luis Vila |',
         '| Luis Antonio Vila Meza | Vila Meza Luis Antonio | F34C, capturas de Luis Vila |\n'
         '| Luisa Vila | Vila Meza Luis Antonio | sin revisión |'), False, None),
    ('QA-63', 'EVD', 'Variante de nombre no registrada («Freddi Coronacion»)',
     sub(ACTA, '| Fredy Sistemas | Freddy Coronación |', '| Fredy Sistemas | Freddi Coronacion |'), False, 'G0-14'),
    ('QA-64', 'IDN', 'Nombre parcial («Luis Vila») como responsable del acta: ya no se acepta por coincidencia parcial',
     rsub(ACTA, r'^\| Vila Meza Luis Antonio \| Integrante del equipo \|', '| Luis Vila | Integrante del equipo |'),
     False, 'G0-14'),
    ('QA-65', 'EVD', 'Fecha declarada inexistente en la evidencia (2026-99-99)',
     rsub(ACTA, r'(\[Anthony_Pena\].*?\| ACEPTADO \| )2026-10-04( \|)', r'\g<1>2026-99-99\2'), False, 'G0-14'),
    ('QA-66', 'REC', 'Fecha de calendario inexistente en el registro (2026-02-30)',
     rsub(ACTA, r'^(\| Peña Arroyo Anthony \| Integrante del equipo \| )2026-10-04', r'\g<1>2026-02-30'), False, 'G0-14'),
    ('QA-67', 'EVD', 'Fecha del registro distinta de la evidencia, sin confirmación',
     rsub(ACTA, r'^(\| Peña Arroyo Anthony \| Integrante del equipo \| )2026-10-04', r'\g<1>2026-10-05'), False, 'G0-14'),
    ('QA-68', 'EVD', 'Discrepancia temporal sin confirmación: el registro de Luis usa solo la original',
     chain(rsub(ACTA, r'RESUELTA por \[confirmación\]\([^)]*\)', 'DISCREPANCIA'),
           rsub(ACTA, r'^(\| Vila Meza Luis Antonio \|.*?)\[original\]\(([^)]*)\) · \[confirmación\]\([^)]*\)',
                r'\1[original](\2)')), False, 'G0-14'),
    ('QA-69', 'EVD', 'Segunda evidencia que no resuelve la discrepancia (otra fecha declarada)',
     rsub(ACTA, r'(\[Luis_Vila_confirmación\].*?\| ACEPTADO \| )2026-10-04( \|)', r'\g<1>2026-10-03\2'), False, 'G0-14'),
    ('QA-70', 'EVD', 'Segunda evidencia que no resuelve la discrepancia (no repite la aprobación de ADR-005)',
     rsub(ACTA, r'(\[Luis_Vila_confirmación\].*?\| Vila Meza Luis Antonio \| )APROBADA( \|)', r'\1—\2'), False, 'G0-14'),
    ('QA-71', 'MAT', 'G0-09 cerrado con evidencia temporal pendiente (discrepancia sin resolver)',
     chain(rsub(ACTA, r'RESUELTA por \[confirmación\]\([^)]*\)', 'DISCREPANCIA'),
           rsub(TM, r'^(\| Vila Meza Luis Antonio \|.*?)\[original\]\(([^)]*)\) · \[confirmación\]\([^)]*\)',
                r'\1[original](\2)')), False, 'G0-09'),
    ('QA-72', 'DEC', 'ADR-005 declarada APROBADA como estado canónico',
     sub('README.md', '**ADR-005 = PROPUESTA** (estado canónico)', '**ADR-005 = APROBADA** (estado canónico)'), False, None),
    ('QA-73', 'EVD', 'Una confirmación adicional suelta que no resuelve ninguna original',
     rsub(ACTA, r'RESUELTA por \[confirmación\]\([^)]*\)', 'CONFORME'), False, 'G0-14'),
    # ---- auditoría F34C-M02-R1: remitente visible
    ('QA-74', 'EVD', 'Remitente visible «Carlos Ruiz Perez» en la confirmación de Luis',
     rsub(ACTA, SENDER_LUIS_CONF, r'\1Carlos Ruiz Perez\2'), False, ('G0-14', 'G0-09')),
    ('QA-75', 'EVD', 'Remitente visible «Luisa Vila» en la confirmación de Luis',
     rsub(ACTA, SENDER_LUIS_CONF, r'\1Luisa Vila\2'), False, ('G0-14', 'G0-09')),
    ('QA-76', 'EVD', 'Remitente visible de otro integrante («Fredy Sistemas») en la captura de Anthony',
     sub(ACTA, '| Anthony Peña | Peña Antony |', '| Fredy Sistemas | Peña Antony |'), False, ('G0-14', 'G0-09')),
    ('QA-77', 'EVD', 'Remitente visible con alias no registrado («Fredy S.»)',
     sub(ACTA, '| Fredy Sistemas | Freddy Coronación |', '| Fredy S. | Freddy Coronación |'), False, ('G0-14', 'G0-09')),
    ('QA-78', 'EVD', 'Remitente válido de Anthony pero nombre declarado de otra persona',
     sub(ACTA, '| Anthony Peña | Peña Antony |', '| Anthony Peña | Freddy Coronación |'), False, ('G0-14', 'G0-09')),
    ('QA-79', 'EVD', 'Nombre válido pero adjunto de otra persona en la aceptación del threat model',
     rsub(TM, r'^(\| Peña Arroyo Anthony \| Integrante del equipo \| 2026-10-04 \| ACEPTA \| \[captura\]\()[^)]*\)',
          r'\1' + EV_F + ')'), False, 'G0-09'),
    ('QA-80', 'EVD', 'Remitente ausente pero el mensaje solo declara un alias, no el nombre completo',
     sub(ACTA, '| Anthony Peña | Peña Antony |', '| — (mensaje propio) | Peña Antony |'), False, ('G0-14', 'G0-09')),
    ('QA-81', 'EVD', 'Remitente vacío sin justificar («—»)',
     rsub(ACTA, SENDER_LUIS_CONF, r'\1—\2'), False, ('G0-14', 'G0-09')),
    ('QA-82', 'EVD', 'Variante de remitente añadida al acta sin revisión en el validador',
     sub(ACTA, '| Luis Antonio Vila Meza | Vila Meza Luis Antonio | F34C, capturas de Luis Vila |',
         '| Luis Antonio Vila Meza | Vila Meza Luis Antonio | F34C, capturas de Luis Vila |\n'
         '| Carlos Ruiz Perez | Vila Meza Luis Antonio | sin revisión |'), False, None),
]

# Casos POSITIVOS en memoria: deben pasar todas las reglas y dejar G0-14 y G0-09 en CUMPLIDO.
POSITIVES = [
    ('POS-01', 'Variante explícita revisada («Fredy Coronación») en lugar de «Freddy Coronación»',
     sub(ACTA, '| Fredy Sistemas | Freddy Coronación |', '| Fredy Sistemas | Fredy Coronación |')),
    ('POS-02', 'Remitente ausente (mensaje propio) con el nombre completo declarado',
     sub(ACTA, '| Anthony Peña | Peña Antony |', '| — (mensaje propio) | Peña Arroyo Anthony |')),
    ('POS-05', 'Remitente visible con el nombre canónico exacto del mismo integrante',
     sub(ACTA, '| Anthony Peña | Peña Antony |', '| Peña Arroyo Anthony | Peña Antony |')),
    ('POS-06', '«Fredy Sistemas» como remitente: variante revisada y documentada de Coronacion Meza Fredy (estado real)',
     lambda D: D),
    ('POS-03', 'Nombre completo canónico declarado («Vila Meza Luis Antonio»)',
     rsub(ACTA, r'(\[Luis_Vila_confirmación\].*?\| — \(mensaje propio\) \| )Luis Antonio Vila Meza( \|)',
          r'\1Vila Meza Luis Antonio\2')),
    ('POS-04', 'Confirmación adicional válida que resuelve la discrepancia temporal (estado registrado)', lambda D: D),
]


def positive_control():
    """Con evidencia completa SIMULADA (integrantes sintéticos, roles válidos, identidades distintas y adjuntos CONTROL
    que solo existen en memoria), la regla SÍ permite G0 = APROBADA CON RESTRICCIONES sin habilitar C ni datos reales.
    Nunca usa nombres reales ni archivos del repositorio."""
    D = read_all()
    D = chain(
        set_rows(ACTA, team_rows(SYN_TEAM, 'APRUEBA', link='ev') + [CONS_PEND]),
        set_rows(TM, team_rows(SYN_TEAM, 'ACEPTA', link='ev')),
        set_evidence([[CTRL.format(f'ev-{i}'), 'Única', f'`{CTRL_SHA}`', 'JPEG', '— (mensaje propio)', nm, nm, 'APROBADA',
                       'ACEPTADO', DAY, 'Sí', 'CONFORME', 'Control'] for i, nm in enumerate(SYN_TEAM)]),
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
    'docs(governance): close F34C; G0 remains not approved',
    'docs(academic): register ADR-005 team approval and threat-model acceptance',
    'test(academic): harden F34B evidence validation for F34C',
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
        ctx = sim if isinstance(sim, Ctx) else (SIM if sim else REAL)
        try:
            Dm = mut(D)
        except AssertionError as e:
            add(False, f'{cid}: la mutación no se pudo aplicar ({e})')
            continue
        r = run_rules(Dm, ctx)
        crits = (crit,) if isinstance(crit, str) else (crit or ())
        der_m = derive(Dm, ctx)
        ok = bool(r.get(rule)) and all(der_m[c] != 'CUMPLIDO' for c in crits)
        add(ok, f'{cid} detectado por {rule}' + (f' y {"/".join(crits)} no queda CUMPLIDO' if crits else '') + f': {what}')
    add(len(CASES) >= 80, f'casos negativos: {len(CASES)}')
    for pid, what, mut in POSITIVES:
        Dm = mut(D)
        r = run_rules(Dm, REAL)
        der = derive(Dm, REAL)
        bad = {k: v[:1] for k, v in r.items() if v}
        add(not bad and der['G0-14'] == 'CUMPLIDO' and der['G0-09'] == 'CUMPLIDO', f'{pid} positivo: {what} {bad}')
    add(declared_member('Luisa Vila', REAL.roster) is None and declared_member('Luis Vila', REAL.roster) is None,
        'identidad: «Luisa Vila» y «Luis Vila» no corresponden a ningún integrante sin correspondencia revisada')
    add(not valid_date('2026-99-99') and not valid_date('2026-02-30') and not valid_date('04/10/2026')
        and valid_date('2026-10-04'), 'fechas: solo fechas reales de calendario en formato AAAA-MM-DD')

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
