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
  G12   (F34D) respuesta de G0-12: sin adjunto existente (SHA-256 y formato real) no es evidencia y la fila del docente no
        puede registrarse; identidad verificada solo con el docente del proyecto (CLAUDE.md) o una variante revisada, sin
        coincidencia aproximada; fecha real; la opinión del revisor no se registra como hecho institucional.
        F34D-M01: concordancia total entre respuesta declarada, fila del registro, adjunto real y metadatos (identidad,
        rol compatible, fecha, decisión, mismo adjunto, SHA-256 y formato reales); sin archivo, ningún metadato anticipado.
        Las transcripciones declaradas deben coincidir literalmente con la respuesta recibida.
  LIM   (F34D) la validación del docente o revisor nunca se presenta como aprobación jurídica, de privacidad,
        autorización del Colegio Andino, certificación de cumplimiento, autorización de datos reales, del alcance C ni
        desbloqueo de F35. F34D-M02: cada proposición se evalúa por separado con su propia polaridad (las elipsis heredan
        la anterior; «pero/sino» y verbos afirmativos la reinician; «no solo» y «ni deja de» afirman), de modo que negar
        una categoría no neutraliza la afirmación de otra en la misma línea
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


def course_teacher():
    """Docente del curso según CLAUDE.md («docente Dr. … .»). Cadena vacía si no se puede leer: falla cerrado."""
    try:
        t = open(os.path.join(ROOT, 'CLAUDE.md'), encoding='utf-8').read()
    except OSError:
        return ''
    m = re.search(r'docente (?:Dra?\. )?([A-ZÁÉÍÓÚÑ][^.,]+)', t)
    return m.group(1).strip() if m else ''


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

    def __init__(self, exists, roster, sha=None, fmt=None, listing=None, teacher=None):
        self.exists, self.roster = exists, roster
        self.teacher = course_teacher() if teacher is None else teacher
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


def idn_forms(D, ctx):  # noqa: C901
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
                                                     roster, NEED_ROLES, unique_roles=True)
        + idn_teacher(t('F34B_Validacion_Necesidad.md'), getattr(ctx, 'teacher', REAL.teacher)),
    }


# Variantes REVISADAS del nombre del docente (F34D). Vacía: «Max Magnolie Arana» NO está revisada (OBS-F34D-02).
TEACHER_ALIASES = {}


def teacher_match(name, teacher):
    """Nombre del docente exacto (mismas palabras, sin tildes ni orden) o variante revisada. Sin coincidencia aproximada."""
    if not teacher or not name or name == '—':
        return False
    if ident(name) == ident(teacher):
        return True
    return any(ident(v) == ident(name) and ident(target) == ident(teacher) for v, target in TEACHER_ALIASES.items())


def idn_teacher(tab, teacher):
    """La fila «Docente del curso» solo se registra con la identidad del docente del proyecto (F34D)."""
    out = []
    for r in tab:
        if r[1] == 'Docente del curso' and touched(r) and not teacher_match(r[0], teacher):
            out.append(f'F34B_Validacion_Necesidad.md: «{r[0]}» no es verificable como el docente del curso '
                       f'(registro del proyecto: «{teacher or "no disponible"}»); requiere vinculación inequívoca')
    return out


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
    g12_refs = set(ATT_LINK.findall(g12_table(D['F34B_Validacion_Necesidad.md']).get('Adjunto', '')))
    for rel in ctx.listing():
        if rel not in ev and rel not in g12_refs:
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


# ---------------------------------------------------------------- G0-12: respuesta recibida y límites (F34D)
G12_KEYS = ['Estado de la respuesta', 'Adjunto', 'SHA-256', 'Formato real', 'Nombre declarado', 'Rol declarado',
            'Institución declarada', 'Fecha declarada', 'Decisión declarada', 'Verificación de identidad']
G12_STATES = {'SIN EVIDENCIA ARCHIVADA', 'EVIDENCIA ARCHIVADA'}
G12_DECISIONS = {'NECESIDAD VALIDADA', 'NECESIDAD NO VALIDADA'}
EMPTY = ('', '—')
# Rol declarado compatible con la fila «Docente del curso»: docente o profesor, nunca postulante, candidato, estudiante
# ni integrante del equipo.
ROLE_OK = re.compile(r'\b(docente|profesor[a]?)\b', re.I)
ROLE_BAD = re.compile(r'postulante|candidat|estudiante|alumn|integrante|evaluad[oa] por el sistema', re.I)
# Transcripciones literales de la respuesta recibida en F34D: son contenido declarado, no afirmaciones del proyecto,
# y no pueden modificarse (una afirmación escondida dentro de ellas falla).
DECLARED_QUOTES = {
    '**Restricciones o recomendación declaradas:**':
        'El alcance definido es adecuado y éticamente transparente. Se recomienda mantener la auditabilidad de las '
        'rúbricas y asegurar una capacitación breve a los evaluadores del Colegio Andino para optimizar el uso de las '
        'explicaciones visibles y la trazabilidad de evidencias.',
    '**Observación declarada**':
        'El Alcance B garantiza el equilibrio perfecto entre automatización operativa y control ético en el proceso de '
        'selección de personal, cumpliendo plenamente con los requerimientos y estándares institucionales.',
    '**Confirmación declarada:**': 'Declaro que esta respuesta corresponde a mi revisión real del alcance descrito.',
}


# ---- estructura obligatoria de la respuesta de G0-12 (F34D-M01-R1): falla cerrado
G12_SECTION = re.compile(r'^## \d+\. Respuesta recibida[^\n]*$', re.M)
G12_HEADER = ['Campo', 'Valor']
G12_OUTSIDE = re.compile(r'^\s*(?:[-*]\s*)?\**\s*(?:' + '|'.join(map(re.escape, G12_KEYS)) + r')\s*\**\s*:', re.M)


def g12_section(text):
    """Texto de la sección «Respuesta recibida» de G0-12 (None si no existe)."""
    m = G12_SECTION.search(text)
    if not m:
        return None
    rest = text[m.end():]
    nxt = re.search(r'^## ', rest, re.M)
    return rest[:nxt.start()] if nxt else rest


def kv_tables(text):
    """Todas las tablas «| Campo | Valor |» con todas sus filas, sin filtrar."""
    tables, cur = [], None
    for ln in text.splitlines():
        if not ln.startswith('|'):
            cur = None
            continue
        c = cells(ln)
        if c == G12_HEADER:
            cur = []
            tables.append(cur)
        elif cur is not None and not set(ln.replace('|', '').strip()) <= set('-: '):
            cur.append(c)
    return tables


def g12_table(text):
    """Metadatos de la ÚNICA tabla de la sección de G0-12; dict vacío si la sección o la tabla no son válidas."""
    sec = g12_section(text)
    tabs = kv_tables(sec) if sec is not None else []
    if len(tabs) != 1:
        return {}
    return {r[0]: r[1] for r in tabs[0] if len(r) == 2}


def g12_structure(text, n):
    """La sección de G0-12 debe tener exactamente una tabla de metadatos, dentro de la sección, bien formada, con los
    10 campos obligatorios una sola vez, sin campos vacíos ni desconocidos y sin metadatos fuera de la tabla.
    No se asume ningún valor por defecto: cualquier fallo estructural impide evaluar G0-12 (falla cerrado)."""
    sec = g12_section(text)
    if sec is None:
        return [f'{n}: falta la sección «Respuesta recibida» de G0-12 (falla cerrado)']
    in_sec, total = kv_tables(sec), kv_tables(text)
    if not in_sec:
        return [f'{n}: falta la tabla de metadatos de G0-12 en su sección (falla cerrado)']
    out = []
    if len(in_sec) > 1:
        out.append(f'{n}: hay {len(in_sec)} tablas de metadatos de G0-12 (duplicada o contradictoria)')
    if len(total) > len(in_sec):
        out.append(f'{n}: tabla de metadatos de G0-12 fuera de su sección')
    rows_ = in_sec[0]
    bad = [r for r in rows_ if len(r) != 2]
    if bad:
        out.append(f'{n}: tabla de metadatos mal formada ({len(bad)} filas sin exactamente dos columnas)')
    keys = [r[0] for r in rows_ if len(r) == 2]
    dup = sorted({k for k in keys if keys.count(k) > 1})
    if dup:
        out.append(f'{n}: campos repetidos en la tabla de metadatos: {dup}')
    miss = [k for k in G12_KEYS if k not in keys]
    if miss:
        out.append(f'{n}: faltan campos obligatorios en la tabla de metadatos: {miss}')
    unknown = [k for k in keys if k not in G12_KEYS]
    if unknown:
        out.append(f'{n}: campos no admitidos en la tabla de metadatos: {unknown}')
    empty = [r[0] for r in rows_ if len(r) == 2 and not r[1].strip()]
    if empty:
        out.append(f'{n}: campos sin valor (use «—» si no aplica): {empty}')
    outside = [m.group(0).strip() for m in G12_OUTSIDE.finditer(text)]
    if outside:
        out.append(f'{n}: metadatos de G0-12 fuera de la tabla: {outside[:2]}')
    return out


def g12(D, ctx):
    """Respuesta de G0-12 (§4) con concordancia total (F34D-M01) entre:
    A) respuesta declarada, B) fila del registro, C) adjunto real y D) metadatos del adjunto.
    Sin archivo existente: adjunto, SHA-256 y formato vacíos, estado SIN EVIDENCIA ARCHIVADA y G0-12 sin cerrar
    (ningún metadato anticipado). Con archivo: SHA-256 y formato reales. Una fila del docente en el registro exige
    misma identidad, fecha, decisión y adjunto que la respuesta, rol compatible e identidad verificada."""
    out = []
    n = 'F34B_Validacion_Necesidad.md'
    structural = g12_structure(D[n], n)
    if structural:
        return structural            # sin tabla válida no hay nada que evaluar: G0-12 no puede cerrarse
    f = g12_table(D[n])
    links = ATT_LINK.findall(f['Adjunto'])
    has_file = bool(links) and all(ctx.exists(x) for x in links)
    state, sha_, fmt_ = f['Estado de la respuesta'], f['SHA-256'].strip('`'), f['Formato real']
    if state == 'SIN EVIDENCIA ARCHIVADA' and f['Verificación de identidad'] != 'NO VERIFICABLE':
        out.append(f'{n}: sin evidencia archivada la identidad solo puede figurar como NO VERIFICABLE')
    if state not in G12_STATES:
        out.append(f'{n}: estado de la respuesta «{state}» no admitido')
    if (state == 'EVIDENCIA ARCHIVADA') != has_file:
        out.append(f'{n}: el estado de la respuesta no coincide con la existencia de su adjunto')
    if f['Adjunto'] not in EMPTY and not links:
        out.append(f'{n}: el campo Adjunto no enlaza un archivo de adjuntos/')
    if not has_file:
        # Ningún metadato anticipado para un archivo inexistente.
        if links:
            out.append(f'{n}: la respuesta enlaza un adjunto que no existe')
        if sha_ not in EMPTY:
            out.append(f'{n}: SHA-256 registrado sin archivo existente (metadato anticipado)')
        if fmt_ not in EMPTY:
            out.append(f'{n}: formato registrado sin archivo existente (metadato anticipado)')
    else:
        for x in links:
            if sha_ != ctx.sha(x):
                out.append(f'{n}: SHA-256 de la respuesta distinto del archivo')
            if fmt_ != ctx.fmt(x):
                out.append(f'{n}: formato registrado «{fmt_}» distinto del real «{ctx.fmt(x)}»')
    if not valid_date(f['Fecha declarada']):
        out.append(f'{n}: fecha declarada «{f["Fecha declarada"]}» inexistente o con formato inválido')
    if f['Decisión declarada'] not in G12_DECISIONS:
        out.append(f'{n}: decisión declarada «{f["Decisión declarada"]}» no admitida')
    if not ROLE_OK.search(f['Rol declarado']) or ROLE_BAD.search(f['Rol declarado']):
        out.append(f'{n}: rol declarado «{f["Rol declarado"]}» incompatible con la fila «Docente del curso»')
    teacher = getattr(ctx, 'teacher', REAL.teacher)
    verified = teacher_match(f['Nombre declarado'], teacher)
    if f['Verificación de identidad'] == 'VERIFICADA' and not verified:
        out.append(f'{n}: identidad «{f["Nombre declarado"]}» marcada VERIFICADA sin coincidir con el docente registrado')
    if f['Verificación de identidad'] not in ('VERIFICADA', 'NO VERIFICABLE'):
        out.append(f'{n}: verificación de identidad «{f["Verificación de identidad"]}» no admitida')
    # Concordancia entre la respuesta (A, C, D) y la fila del docente en el registro (B).
    tab = records(D[n])
    for r in (tab[0] if tab else []):
        if len(r) != 7 or r[1] != 'Docente del curso' or not touched(r):
            continue
        who, _, date, dec_, ev, _, st = r
        if st == 'REGISTRADO' and (not has_file or not verified or f['Verificación de identidad'] != 'VERIFICADA'):
            out.append(f'{n}: la fila del docente se registra sin evidencia archivada o sin identidad verificada')
        if ident(who) != ident(f['Nombre declarado']):
            out.append(f'{n}: la identidad del registro («{who}») no coincide con la de la respuesta')
        if date != f['Fecha declarada']:
            out.append(f'{n}: la fecha del registro ({date}) no coincide con la fecha declarada ({f["Fecha declarada"]})')
        if dec_ != f['Decisión declarada']:
            out.append(f'{n}: la decisión del registro («{dec_}») contradice la respuesta («{f["Decisión declarada"]}»)')
        if set(ATT_LINK.findall(ev)) != set(links):
            out.append(f'{n}: el adjunto del registro no es el mismo que el de la respuesta')
    for ln in D[n].splitlines():
        if 'cumpliendo plenamente' in ln and 'opinión del revisor' not in ln:
            out.append(f'{n}: la frase sobre cumplimiento institucional no figura como opinión del revisor')
        for head, quote in DECLARED_QUOTES.items():
            if ln.startswith(head):
                q = re.findall(r'«(.*?)»', ln)
                if q != [quote]:
                    out.append(f'{n}: la transcripción «{head.strip("*: ")}» no coincide con la respuesta recibida')
    t = D[n]
    for s in ('No es una aprobación jurídica', 'no es una aprobación de privacidad', 'no es una autorización del Colegio Andino'):
        if s not in t:
            out.append(f'{n}: falta el límite «{s}»')
    return out


# ---------------------------------------------------------------- LIM: afirmaciones por proposición (F34D-M02)
# Categorías que la respuesta del docente nunca puede ser. Cada una se evalúa en cada proposición por separado: la
# negación de una categoría no neutraliza la afirmación de otra en la misma línea.
LIM_CATEGORIES = {
    'aprobación jurídica': re.compile(r'jur[ií]dic', re.I),
    'aprobación de privacidad': re.compile(r'privacidad', re.I),
    'autorización del Colegio Andino o institucional': re.compile(
        r'colegio andino|autoriza\w*\s+institucional|autorizaci[oó]n\s+(?:de\s+la\s+)?instituci', re.I),
    'certificación o cumplimiento institucional': re.compile(
        r'certific\w*|cumplimiento\s+(?:institucional|normativo|de\s+(?:los\s+)?est[aá]ndares)|cumpl\w*\s+(?:plenamente\s+)?'
        r'con\s+(?:los\s+)?(?:requerimientos|est[aá]ndares)', re.I),
    'autorización de datos reales': re.compile(r'datos\s+reales', re.I),
    'autorización del alcance C': re.compile(r'alcance\s+c\b', re.I),
    'desbloqueo de F35': re.compile(r'\bF35\b(?!-SBX)|F35[–-]F40', re.I),
}
LIM_SUBJECT = re.compile(r'docente|revisor|G0-12|F34D|necesidad|respuesta|validaci[oó]n', re.I)
# Marcadores que niegan o limitan la proposición en la que aparecen.
LIM_NEG = re.compile(r'\b(no|ni|nunca|tampoco|sin|jam[aá]s|ningun\w*|prohibid\w*|bloquead\w*|pendient\w*|exig\w*|requier\w*|'
                     r'falt\w*|salvo|excluid\w*)\b', re.I)
# «no solo», «no sólo», «no únicamente» afirman, no niegan.
LIM_NOT_ONLY = re.compile(r'\bno\s+(?:s[oó]lo|solamente|[uú]nicamente)\b|\b(?:no|ni)\s+(?:deja\w*|dej[oó]|dejar[aá])\s+de\b'
                          r'|\bno\s+(?:es|son)\s+(?:menos|otra\s+cosa)\b', re.I)  # «no solo», «ni deja de ser»: afirman
LIM_AFFIRM = re.compile(r'\b(s[ií]|es|son|ser[aá]|constituye\w*|equivale\w*|sirve\w*|sustituye\w*|reemplaza\w*|'
                        r'autoriza\w*|certifica\w*|aprueba\w*|aprobad\w*|habilita\w*|desbloque\w*|cumple\w*|'
                        r'garantiza\w*|valida\w*|acredita\w*|implica\w*|permite\w*|otorga\w*|concede\w*|tambi[eé]n|'
                        r'adem[aá]s|incluso)\b', re.I)
LIM_SPLIT = re.compile(r'(\s*[,;:()—]\s*|\s+(?:pero|sino|aunque|mientras\s+que|y|e|ni|o|u)\s+)', re.I)


def propositions(sentence):
    """Divide una oración en proposiciones y asigna a cada una su polaridad (True = afirmativa).

    - Con un marcador de negación o limitación: negativa (salvo «no solo», que afirma).
    - Tras «ni»: negativa (continúa la negación).
    - Tras «pero», «sino» o «aunque», o con un verbo o marcador afirmativo propio: afirmativa.
    - Sin verbo propio (elipsis, p. ej. «, de privacidad»): hereda la polaridad de la proposición anterior.
    """
    parts = LIM_SPLIT.split(sentence)
    out, prev, sep = [], True, ''
    for i, p in enumerate(parts):
        if i % 2 == 1:
            sep = p.strip().lower()
            continue
        if not p.strip():
            continue
        if LIM_NOT_ONLY.search(f'{sep} {p}'):     # el separador cuenta: «… ni deja de ser …» afirma
            pol = True
        elif LIM_NEG.search(p):
            pol = False
        elif sep == 'ni':
            pol = False
        elif sep in ('pero', 'sino', 'aunque') or LIM_AFFIRM.search(p):
            pol = True
        else:
            pol = prev
        out.append((p.strip(), pol))
        prev = pol
    return out


def lim_claims(text):
    """Afirmaciones positivas de categorías prohibidas en un texto: [(categoría, proposición)]."""
    found = []
    for sentence in re.split(r'(?<=[.!?])\s+|\s*\|\s*', text):
        for prop, pol in propositions(sentence):
            if not pol:
                continue
            for cat, rx in LIM_CATEGORIES.items():
                if rx.search(prop):
                    found.append((cat, prop))
    return found


def strip_declared(ln):
    """Quita de una línea la transcripción literal declarada (verificada en G12), si es la registrada."""
    for head, quote in DECLARED_QUOTES.items():
        if ln.startswith(head):
            return ln.replace('«' + quote + '»', '')
    return ln


def lim(D, ctx):
    """La respuesta del docente o revisor nunca se presenta como aprobación jurídica, de privacidad, autorización del
    Colegio Andino, certificación de cumplimiento institucional, autorización de datos reales, del alcance C ni como
    desbloqueo de F35. Se evalúa cada proposición por separado (F34D-M02)."""
    out = []
    for n, t in D.items():
        whole = n == 'F34B_Validacion_Necesidad.md'
        for i, ln in enumerate(t.splitlines(), 1):
            if not (whole or LIM_SUBJECT.search(ln)):
                continue
            if not whole and not re.search(r'docente|revisor|G0-12|F34D', ln, re.I):
                continue
            body = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', strip_declared(ln))   # enlaces: solo su texto
            body = re.sub(r'[*`]', '', body)
            for cat, prop in lim_claims(body):
                out.append(f'{n}:{i}: afirma «{cat}» sobre la validación del revisor: {prop[:70]}')
    return out


def derive(D, exists):
    """Estado de cada criterio externo derivado SOLO de registros con evidencia existente e identidad válida.

    Un formulario con cualquier violación de identidad o rol no produce CUMPLIDO ni RECHAZADO; tampoco el acta ni la
    aceptación del threat model si la verificación de sus adjuntos (EVD) falla."""
    bad = idn_forms(D, exists)
    if evd(D, exists):
        bad['F34B_Acta_Aprobacion_ADR005.md'] = bad['F34B_Acta_Aprobacion_ADR005.md'] + ['EVD']
        bad['F34B_Aceptacion_Threat_Model.md'] = bad['F34B_Aceptacion_Threat_Model.md'] + ['EVD']
    if g12(D, exists):
        bad['F34B_Validacion_Necesidad.md'] = bad['F34B_Validacion_Necesidad.md'] + ['G12']

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


RULES = [('REC', rec), ('ANS', ans), ('IDN', idn), ('EVD', evd), ('G12', g12), ('LIM', lim), ('MAT', mat),
         ('DEC', dec), ('SCOPE', scope),
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
SIM = Ctx(lambda p: p.startswith('adjuntos/CONTROL-'), [ident(x) for x in SYN_TEAM], teacher='Persona Docente Control',
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
DOC_ROW = r'^\| — \| Docente del curso \| — \| PENDIENTE \| — \|[^|]*\| PENDIENTE \|$'
G12_CTRL = 'adjuntos/G0-12_necesidad_CONTROL_2026-10-04.png'   # adjunto SIMULADO solo en memoria (no existe en disco)
G12_CTRL2 = 'adjuntos/G0-12_otra_CONTROL_2026-10-04.png'        # segundo adjunto SIMULADO (para «adjunto diferente»)
G12_SIM = {G12_CTRL: ('1' * 64, 'PNG'), G12_CTRL2: ('2' * 64, 'PNG')}
G12_CTX = Ctx(lambda p: real_exists(p) or p in G12_SIM, REAL.roster,
              lambda p: real_sha(p) or G12_SIM.get(p, (None, None))[0],
              lambda p: real_fmt(p) or G12_SIM.get(p, (None, None))[1],
              lambda: real_listing() + [G12_CTRL])


def g12_coherent():
    """Respuesta de G0-12 coherente en todo (identidad, rol, fecha, decisión, adjunto, SHA-256 y formato) con un
    adjunto SIMULADO que solo existe en memoria. Base de POS-07 y de los negativos de concordancia (F34D-M01)."""
    return chain(
        rsub(NEC, DOC_ROW, f'| {REAL.teacher} | Docente del curso | 2026-10-04 | NECESIDAD VALIDADA | [respuesta]({G12_CTRL}) | '
                           '— | REGISTRADO |'),
        sub(NEC, '| Estado de la respuesta | SIN EVIDENCIA ARCHIVADA |', '| Estado de la respuesta | EVIDENCIA ARCHIVADA |'),
        sub(NEC, '| Adjunto | — |', f'| Adjunto | [respuesta]({G12_CTRL}) |'),
        sub(NEC, '| SHA-256 | — |', '| SHA-256 | `' + '1' * 64 + '` |'),
        sub(NEC, '| Formato real | — |', '| Formato real | PNG |'),
        sub(NEC, '| Nombre declarado | Max Magnolie Arana |', f'| Nombre declarado | {REAL.teacher} |'),
        sub(NEC, '| Verificación de identidad | NO VERIFICABLE |', '| Verificación de identidad | VERIFICADA |'),
    )


def on_coherent(*fs):
    return lambda D: chain(*fs)(g12_coherent()(D))


OBS_F34D = '### Observaciones F34D'


def claim(text, n=None):
    """Inserta una frase antes de las observaciones F34D (o al final de otro documento)."""
    if n is None:
        return sub(NEC, OBS_F34D, text + '\n\n' + OBS_F34D)
    return lambda D: dict(D, **{n: D[n] + '\n' + text + '\n'})
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
     rsub(NEC, r'^\| — \| Docente del curso \| — \| PENDIENTE \| — \|[^|]*\| PENDIENTE \|$',
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
    ('QA-83', 'REC', 'G0-12: decisión del docente registrada sin adjunto',
     rsub(NEC, DOC_ROW, '| Maglioni Arana Caparachin | Docente del curso | 2026-10-04 | NECESIDAD VALIDADA | — | — | REGISTRADO |'),
     False, 'G0-12'),
    ('QA-84', 'IDN', 'G0-12: identidad no verificable («Max Magnolie Arana») aunque haya adjunto',
     rsub(NEC, DOC_ROW, f'| Max Magnolie Arana | Docente del curso | 2026-10-04 | NECESIDAD VALIDADA | [respuesta]({G12_CTRL}) | — '
          '| REGISTRADO |'), G12_CTX, 'G0-12'),
    ('QA-85', 'IDN', 'G0-12: nombre distinto aceptado por coincidencia aproximada («Magnolie Arana Caparachin»)',
     rsub(NEC, DOC_ROW, f'| Magnolie Arana Caparachin | Docente del curso | 2026-10-04 | NECESIDAD VALIDADA | '
          f'[respuesta]({G12_CTRL}) | — | REGISTRADO |'), G12_CTX, 'G0-12'),
    ('QA-86', 'REC', 'G0-12: fecha de calendario inválida en el registro (2026-10-32)',
     rsub(NEC, DOC_ROW, f'| Maglioni Arana Caparachin | Docente del curso | 2026-10-32 | NECESIDAD VALIDADA | '
          f'[respuesta]({G12_CTRL}) | — | REGISTRADO |'), G12_CTX, 'G0-12'),
    ('QA-87', 'G12', 'G0-12: fecha declarada inválida en la respuesta (2026-02-30)',
     sub(NEC, '| Fecha declarada | 2026-10-04 |', '| Fecha declarada | 2026-02-30 |'), False, None),
    ('QA-88', 'IDN', 'G0-12: rol incompatible («Postulante») para el docente',
     rsub(NEC, DOC_ROW, f'| Maglioni Arana Caparachin | Postulante | 2026-10-04 | NECESIDAD VALIDADA | [respuesta]({G12_CTRL}) '
          '| — | REGISTRADO |'), G12_CTX, 'G0-12'),
    ('QA-89', 'LIM', 'Opinión del docente tratada como aprobación jurídica',
     sub(NEC, '### Observaciones F34D', 'La respuesta del docente es la aprobación jurídica del alcance B.\n\n### Observaciones F34D'),
     False, None),
    ('QA-90', 'LIM', 'Opinión del revisor tratada como aprobación de privacidad',
     sub(NEC, '### Observaciones F34D', 'La validación del revisor equivale a la aprobación de privacidad.\n\n### Observaciones F34D'),
     False, None),
    ('QA-91', 'LIM', 'Opinión del revisor tratada como autorización institucional del Colegio Andino',
     sub(NEC, '### Observaciones F34D', 'La respuesta del revisor constituye la autorización del Colegio Andino.\n\n'
                                        '### Observaciones F34D'), False, None),
    ('QA-92', 'LIM', 'Opinión del revisor tratada como autorización de datos reales',
     sub(NEC, '### Observaciones F34D', 'Con la necesidad validada por el docente se autorizan datos reales.\n\n'
                                        '### Observaciones F34D'), False, None),
    ('QA-93', 'PHASE', 'F35 desbloqueada tras G0-12 con G0-02 y G0-03 pendientes',
     sub('F34B_Decision_G0.md', '- **F35–F40 = BLOQUEADAS.**', '- **F35–F40 = HABILITADAS** tras validar G0-12.'), False, None),
    ('QA-94', 'MAT', 'G0-12 marcado CUMPLIDO solo con la respuesta en texto',
     rsub(MATX, r'(^\| G0-12 \|.*)\*\*PENDIENTE EXTERNO\*\*', r'\1**CUMPLIDO**'), False, 'G0-12'),
    ('QA-95', 'G12', 'Identidad marcada VERIFICADA con un nombre que no coincide con el docente',
     sub(NEC, '| Verificación de identidad | NO VERIFICABLE |', '| Verificación de identidad | VERIFICADA |'), False, None),
    ('QA-96', 'G12', 'Respuesta marcada EVIDENCIA ARCHIVADA sin adjunto existente',
     sub(NEC, '| Estado de la respuesta | SIN EVIDENCIA ARCHIVADA |', '| Estado de la respuesta | EVIDENCIA ARCHIVADA |'),
     False, None),
    ('QA-97', 'G12', 'La frase de cumplimiento institucional registrada como hecho, no como opinión del revisor',
     sub(NEC, '(opinión del revisor, no un hecho institucional verificado)', '(hecho institucional)'), False, None),
    # ---- F34D-M01: concordancia completa (respuesta, registro, adjunto y metadatos) sobre una base coherente simulada
    ('QA-98', 'G12', 'Decisión contradictoria: respuesta NECESIDAD NO VALIDADA y registro VALIDADA',
     on_coherent(sub(NEC, '| Decisión declarada | NECESIDAD VALIDADA |', '| Decisión declarada | NECESIDAD NO VALIDADA |')),
     G12_CTX, 'G0-12'),
    ('QA-99', 'G12', 'Fecha del registro distinta de la fecha declarada',
     on_coherent(rsub(NEC, r'^(\| Maglioni Arana Caparachin \| Docente del curso \| )2026-10-04', r'\g<1>2026-10-05')),
     G12_CTX, 'G0-12'),
    ('QA-100', 'G12', 'Rol declarado incompatible («Postulante»)',
     on_coherent(sub(NEC, '| Rol declarado | Docente / Profesor Revisor |', '| Rol declarado | Postulante |')), G12_CTX, 'G0-12'),
    ('QA-101', 'G12', 'El adjunto del registro no es el de la respuesta',
     on_coherent(rsub(NEC, r'^(\| Maglioni Arana Caparachin \|.*?\[respuesta\]\()[^)]*\)', r'\1' + G12_CTRL2 + ')')),
     G12_CTX, 'G0-12'),
    ('QA-102', 'G12', 'SHA-256 inventado sin archivo (respuesta real sin adjunto)',
     sub(NEC, '| SHA-256 | — |', '| SHA-256 | `' + 'a' * 64 + '` |'), False, 'G0-12'),
    ('QA-103', 'G12', 'Formato inventado sin archivo (respuesta real sin adjunto)',
     sub(NEC, '| Formato real | — |', '| Formato real | PNG |'), False, 'G0-12'),
    ('QA-104', 'G12', 'SHA-256 incorrecto para el archivo existente',
     on_coherent(sub(NEC, '| SHA-256 | `' + '1' * 64 + '` |', '| SHA-256 | `' + 'f' * 64 + '` |')), G12_CTX, 'G0-12'),
    ('QA-105', 'G12', 'Formato registrado distinto del formato real',
     on_coherent(sub(NEC, '| Formato real | PNG |', '| Formato real | JPEG |')), G12_CTX, 'G0-12'),
    ('QA-106', 'G12', 'Identidad del registro distinta de la respuesta',
     on_coherent(rsub(NEC, r'^\| Maglioni Arana Caparachin \| Docente del curso \|', '| Max Magnolie Arana | Docente del curso |')),
     G12_CTX, 'G0-12'),
    ('QA-107', 'G12', 'Identidad de la respuesta distinta del registro',
     on_coherent(sub(NEC, '| Nombre declarado | Maglioni Arana Caparachin |', '| Nombre declarado | Max Magnolie Arana |')),
     G12_CTX, 'G0-12'),
    ('QA-108', 'G12', 'Archivo existente con el SHA-256 sin registrar',
     on_coherent(sub(NEC, '| SHA-256 | `' + '1' * 64 + '` |', '| SHA-256 | — |')), G12_CTX, 'G0-12'),
    ('QA-109', 'G12', 'Adjunto enlazado que no existe, con metadatos anticipados',
     chain(sub(NEC, '| Adjunto | — |', '| Adjunto | [respuesta](adjuntos/G0-12_inexistente_2026-10-04.png) |'),
           sub(NEC, '| SHA-256 | — |', '| SHA-256 | `' + 'b' * 64 + '` |'), sub(NEC, '| Formato real | — |', '| Formato real | PNG |')),
     False, 'G0-12'),
    ('QA-110', 'G12', 'Registro REGISTRADO con la identidad marcada NO VERIFICABLE',
     on_coherent(sub(NEC, '| Verificación de identidad | VERIFICADA |', '| Verificación de identidad | NO VERIFICABLE |')),
     G12_CTX, 'G0-12'),
    ('QA-111', 'G12', 'Decisión declarada no admitida',
     sub(NEC, '| Decisión declarada | NECESIDAD VALIDADA |', '| Decisión declarada | VALIDADA PARCIALMENTE |'), False, None),
    # ---- F34D-M02: afirmaciones por proposición; una negación no neutraliza otra afirmación
    ('QA-112', 'LIM', '«es aprobación jurídica, no de privacidad»',
     claim('La respuesta del docente es la aprobación jurídica del alcance B, no una aprobación de privacidad.'), False, None),
    ('QA-113', 'LIM', '«no es jurídica, pero sí autorización institucional»',
     claim('La respuesta del docente no es jurídica, pero sí autorización institucional.'), False, None),
    ('QA-114', 'LIM', '«no autoriza datos reales, pero certifica cumplimiento institucional»',
     claim('La validación del revisor no autoriza datos reales, pero certifica el cumplimiento institucional.'), False, None),
    ('QA-115', 'LIM', '«no aprueba el alcance C, pero autoriza al Colegio Andino»',
     claim('La respuesta no aprueba el alcance C, pero autoriza al Colegio Andino.'), False, None),
    ('QA-116', 'LIM', '«no es de privacidad; es la aprobación jurídica»',
     claim('La respuesta del docente no es una aprobación de privacidad; es la aprobación jurídica.'), False, None),
    ('QA-117', 'LIM', '«no solo es jurídica: también autoriza datos reales»',
     claim('No solo es una aprobación jurídica: también autoriza datos reales.'), False, None),
    ('QA-118', 'LIM', 'Doble negación: «ni deja de ser la aprobación jurídica»',
     claim('Ni es de privacidad ni deja de ser la aprobación jurídica del alcance B.'), False, None),
    ('QA-119', 'LIM', 'La validación del docente desbloquea F35',
     claim('La validación del docente desbloquea F35.'), False, None),
    ('QA-120', 'LIM', '«no es otra cosa que la aprobación jurídica»',
     claim('La respuesta no es otra cosa que la aprobación jurídica del alcance B.'), False, None),
    ('QA-121', 'G12', 'Afirmación escondida dentro de la transcripción declarada',
     sub(NEC, 'cumpliendo plenamente con los requerimientos y estándares institucionales.»',
         'cumpliendo plenamente con los requerimientos y estándares institucionales. Es la aprobación jurídica.»'),
     False, None),
    ('QA-122', 'LIM', 'Afirmación mixta en otro documento: «G0-12 es aprobación de privacidad, no jurídica»',
     claim('La validación de G0-12 es la aprobación de privacidad, no jurídica.', 'F34B_Decision_G0.md'), False, None),
    ('QA-123', 'LIM', '«sin observaciones, autoriza datos reales»',
     claim('La respuesta del revisor, sin observaciones, autoriza datos reales.'), False, None),
    ('QA-82', 'EVD', 'Variante de remitente añadida al acta sin revisión en el validador',
     sub(ACTA, '| Luis Antonio Vila Meza | Vila Meza Luis Antonio | F34C, capturas de Luis Vila |',
         '| Luis Antonio Vila Meza | Vila Meza Luis Antonio | F34C, capturas de Luis Vila |\n'
         '| Carlos Ruiz Perez | Vila Meza Luis Antonio | sin revisión |'), False, None),
]

# ---- F34D-M01-R1: estructura obligatoria de la tabla de metadatos de G0-12 (sobre la base coherente simulada, para
# que lo único que falle sea la estructura).
G12_TABLE_RX = r'^\| Campo \| Valor \|\n\|---\|---\|\n(?:\|.*\|\n)+'


def move_g12_table(D):
    t = D[NEC]
    m = re.search(G12_TABLE_RX, t, re.M)
    assert m, 'tabla de metadatos'
    t = t.replace(m.group(0), '', 1).replace('## 1. Cómo se registra', m.group(0) + '\n## 1. Cómo se registra', 1)
    return dict(D, **{NEC: t})


def team_capture_bypass(D):
    """Bypass reproducido: sin tabla de metadatos, docente registrado con una captura del equipo y matriz/decisión
    alineadas con G0-12 CUMPLIDO."""
    ev = f'[respuesta]({EV_L})'
    t = re.sub(G12_TABLE_RX, '', D[NEC], count=1, flags=re.M)
    t = re.sub(DOC_ROW, f'| {REAL.teacher} | Docente del curso | 2026-10-04 | NECESIDAD VALIDADA | {ev} | — | REGISTRADO |', t,
               count=1, flags=re.M)
    m = re.sub(r'(^\| G0-12 \|.*)\*\*PENDIENTE EXTERNO\*\*', r'\1**CUMPLIDO**', D[MATX], count=1, flags=re.M)
    d = D['F34B_Decision_G0.md'].replace('| G0-12 | PENDIENTE EXTERNO | Respuesta en texto sin adjunto ni identidad '
                                         'verificable (F34D) | PENDIENTE EXTERNO |',
                                         '| G0-12 | PENDIENTE EXTERNO | Respuesta en texto sin adjunto ni identidad '
                                         'verificable (F34D) | CUMPLIDO |')
    return dict(D, **{NEC: t, MATX: m, 'F34B_Decision_G0.md': d})


CASES += [
    ('QA-124', 'G12', 'Tabla de metadatos de G0-12 ausente', on_coherent(rsub(NEC, G12_TABLE_RX, '')), G12_CTX, 'G0-12'),
] + [
    (f'QA-{125 + i}', 'G12', f'Falta el campo obligatorio «{k}» en la tabla de metadatos',
     on_coherent(rsub(NEC, r'^\| ' + re.escape(k) + r' \|.*\n', '')), G12_CTX, 'G0-12') for i, k in enumerate(G12_KEYS)
] + [
    ('QA-135', 'G12', 'Tabla de metadatos duplicada y contradictoria',
     on_coherent(sub(NEC, '| Verificación de identidad | VERIFICADA |',
                     '| Verificación de identidad | VERIFICADA |\n\n| Campo | Valor |\n|---|---|\n'
                     '| Decisión declarada | NECESIDAD NO VALIDADA |')), G12_CTX, 'G0-12'),
    ('QA-136', 'G12', 'Tabla de metadatos mal formada (fila con tres columnas)',
     on_coherent(sub(NEC, '| Rol declarado | Docente / Profesor Revisor |', '| Rol declarado | Docente | Profesor Revisor |')),
     G12_CTX, 'G0-12'),
    ('QA-137', 'G12', 'Campo obligatorio con valor vacío',
     on_coherent(sub(NEC, '| Institución declarada | Universidad Continental (UC Continental) |',
                     '| Institución declarada |  |')), G12_CTX, 'G0-12'),
    ('QA-138', 'G12', 'Campo repetido con valores contradictorios',
     on_coherent(sub(NEC, '| Decisión declarada | NECESIDAD VALIDADA |',
                     '| Decisión declarada | NECESIDAD VALIDADA |\n| Decisión declarada | NECESIDAD NO VALIDADA |')),
     G12_CTX, 'G0-12'),
    ('QA-139', 'G12', 'Campo desconocido añadido a la tabla («Aprobación jurídica»)',
     on_coherent(sub(NEC, '| Verificación de identidad | VERIFICADA |',
                     '| Verificación de identidad | VERIFICADA |\n| Aprobación jurídica | SÍ |')), G12_CTX, 'G0-12'),
    ('QA-140', 'G12', 'Tabla de metadatos movida fuera de su sección', on_coherent(move_g12_table), G12_CTX, 'G0-12'),
    ('QA-141', 'G12', 'Metadatos repartidos fuera de la tabla (SHA-256 en una línea aparte)',
     on_coherent(rsub(NEC, r'^\| SHA-256 \|.*\n', ''),
                 sub(NEC, '**Respuestas declaradas:**', '- **SHA-256:** `' + '1' * 64 + '`\n\n**Respuestas declaradas:**')),
     G12_CTX, 'G0-12'),
    ('QA-142', 'G12', 'Bypass completo: sin tabla, docente registrado con una captura del equipo, matriz y decisión '
                      'en CUMPLIDO', team_capture_bypass, False, 'G0-12'),
    ('QA-143', 'G12', 'Sección «Respuesta recibida» ausente (encabezado cambiado)',
     on_coherent(rsub(NEC, r'^## 4\. Respuesta recibida en F34D.*$', '## 4. Notas')), G12_CTX, 'G0-12'),
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
        # §4 de G0-12 coherente con la fila simulada del docente (F34D)
        sub(NEC, '| Estado de la respuesta | SIN EVIDENCIA ARCHIVADA |', '| Estado de la respuesta | EVIDENCIA ARCHIVADA |'),
        sub(NEC, '| Adjunto | — |', '| Adjunto | ' + CTRL.format('nec') + ' |'),
        sub(NEC, '| SHA-256 | — |', f'| SHA-256 | `{CTRL_SHA}` |'),
        sub(NEC, '| Formato real | — |', '| Formato real | JPEG |'),
        sub(NEC, '| Nombre declarado | Max Magnolie Arana |', '| Nombre declarado | Persona Docente Control |'),
        sub(NEC, '| Fecha declarada | 2026-10-04 |', f'| Fecha declarada | {DAY} |'),
        sub(NEC, '| Verificación de identidad | NO VERIFICABLE |', '| Verificación de identidad | VERIFICADA |'),
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
def git_rc(*a):
    try:
        p = subprocess.run(['git', *a], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    except OSError:
        return None, ''
    return p.returncode, p.stdout


class GitError(Exception):
    pass


def q(runner, *args, ok=(0,)):
    rc, out = runner(*args)
    if rc not in ok:
        raise GitError(f'git {" ".join(args[:4])} → código {rc}; UNKNOWN')
    return rc, out


def paths(out):
    return {ln.strip() for ln in out.splitlines() if ln.strip()}


F34A_VALIDATOR = 'docs/academico/tools/f34a/validate_f34a.py'   # corregido en F34B-M01 por encargo de la auditoría
GOVERNANCE_FILES = frozenset({'CLAUDE.md', 'README.md', 'docs/PROGRESS.md',
                              'docs/academico/ACADEMIC_BASELINE.md'})
CLOSURE_SUBJECTS = [
    'docs(governance): close F34D with G0-12 still pending',
    'docs(academic): record unverified G0-12 response and keep criterion pending',
    'test(academic): harden G0-12 evidence validation for F34D',
]


def closure_scope(subjects, committed, dirty):
    """Solo admite el gobierno ya comprometido en C tras B/A; nunca nuevas ediciones ni fases futuras."""
    if subjects != CLOSURE_SUBJECTS or not committed or not committed <= GOVERNANCE_FILES or dirty:
        return frozenset()
    return frozenset(committed)


OWN_BRANCHES = frozenset({'feature/f34b-g0-external-evidence', 'feature/f34c-g0-evidence-update',
                         'feature/f34d-g0-12-institutional-validation'})
# Ancla fija: cierre publicado de F34D. No usar una rama móvil para congelar las evidencias.
POST_ANCHOR = '9e0fc92adbe563e99a7cb16fdb07aa26f8876d68'
IMMUTABLE = ('docs/academico/g0-evidence/',)
POST_F34E_ALLOWLIST = frozenset({
    'CLAUDE.md', 'docs/PROGRESS.md', 'docs/academico/ACADEMIC_BASELINE.md', 'README.md',
    'docs/academico/handoff/F34E_MACOS_HANDOFF.md', 'scripts/check-macos-readiness.sh',
})
POST_F34E_ARTIFACTS = frozenset({
    'docs/academico/g0-sandbox/' + n for n in (
        'README.md', 'F34E_Definicion_G0_SBX.md', 'F34E_Matriz_Criterios_G0_SBX.md',
        'F34E_Alcance_Autorizado.md', 'F34E_Prohibiciones.md', 'F34E_Relacion_G0_Real_vs_SBX.md',
        'F34E_Autorizacion_F35_SBX.md', 'F34E_Decision_G0_SBX.md')
}) | frozenset({'docs/academico/tools/f34e/validate_f34e.py',
               'docs/academico/tools/f34b/validate_f34b.py'})
POST_F34E_STATES = {
    'G0 real': 'NO APROBADA', 'G0-09': 'CUMPLIDO', 'G0-14': 'CUMPLIDO',
    'G0-02': 'PENDIENTE EXTERNO', 'G0-03': 'PENDIENTE EXTERNO', 'G0-12': 'PENDIENTE EXTERNO',
    'ADR-005': 'PROPUESTA', 'G0-SBX': 'APROBADA CON RESTRICCIONES',
    'F35 productiva': 'BLOQUEADA', 'F35-SBX': 'HABILITADA', 'F36–F40': 'BLOQUEADAS',
    'Alcance C': 'BLOQUEADO', 'Datos reales': 'PROHIBIDOS',
}


# DH-02 (F35-SBX-A): únicas carpetas futuras autorizadas, con extensión fija y contenido de texto comprobado.
F35SBX_DOCS = 'docs/academico/evidencia-sbx/'
F35SBX_TOOLS = 'docs/academico/tools/f35sbx/'
F35SBX_MAX_BYTES = 262144
F35SBX_STARTED = 'F35-SBX-A INICIADA'
F35SBX_CLOSED = 'F35-SBX-A CERRADA'


def post_f35sbx_path(path):
    """Markdown/JSON en evidencia-sbx/ y Python en tools/f35sbx/; sin rutas relativas, binarios ni media."""
    if '\\' in path or any(part in ('', '.', '..') for part in path.split('/')):
        return False
    if path.startswith(F35SBX_DOCS):
        return path.endswith(('.md', '.json'))
    if path.startswith(F35SBX_TOOLS):
        return path.endswith('.py')
    return False


def f35sbx_content(path, data):
    """Contenido de una ruta F35-SBX: existente, UTF-8, sin NUL ni CR, acotado y JSON válido si es .json."""
    import json
    if data is None:
        return [f'{path}: ausente o ilegible (falla cerrado)']
    out = []
    if len(data) > F35SBX_MAX_BYTES or b'\x00' in data or b'\r' in data:
        out.append(f'{path}: binario, CR o tamaño excesivo')
    try:
        text = data.decode('utf-8')
        if path.endswith('.json'):
            json.loads(text)
    except (UnicodeDecodeError, ValueError):
        out.append(f'{path}: no es texto UTF-8 o JSON válido')
    return out


def disk_reader(path):
    try:
        with open(os.path.join(ROOT, path), 'rb') as f:
            return f.read()
    except OSError:
        return None


# F35-SBX-A: los tres validadores históricos adaptados, como rutas exactas; su contenido se verifica contra la base.
F35SBX_HISTORICAL = frozenset({'docs/academico/tools/f30/validate_f30.py', 'docs/academico/tools/f33/validate_f33.py',
                               'docs/academico/tools/f34/validate_f34.py'})


def f35sbx_scope_module():
    """Módulo de excepciones de F35-SBX-A; None si no se puede cargar (falla cerrado)."""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            'f34b_f35sbx_scope', os.path.join(ROOT, 'docs', 'academico', 'tools', 'f35sbx', 'f35sbx_scope.py'))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    except (OSError, ImportError, SyntaxError, AttributeError):
        return None


def post_f34e_path(path):
    """Excepción autorizada: rutas exactas de F34E y, desde F35-SBX-A, las dos carpetas de DH-02 y los tres
    validadores históricos adaptados (rutas exactas)."""
    return (path in POST_F34E_ALLOWLIST or path in POST_F34E_ARTIFACTS or post_f35sbx_path(path)
            or path in F35SBX_HISTORICAL)


def post_doc_rules(path, text, additions=None):
    """Gobierno/handoff autorizado, con estados explícitos y sin aprobaciones externas inventadas.

    Las fotografías históricas se conservan. La sección vigente es obligatoria; también se revisan TODAS
    las líneas añadidas a gobierno, no solo esa sección. El handoff se revisa completo.
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location('f34e_post_policy',
                                                os.path.join(ROOT, 'docs/academico/tools/f34e/validate_f34e.py'))
    policy = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(policy)
    out = []
    sections = re.findall(r'^## Estado vigente F34E\s*\n(.*?)(?=^## |\Z)', text, re.M | re.S)
    if len(sections) != 1:
        return [f'{path}: se exige una sección única «Estado vigente F34E»']
    section = sections[0]
    expected = {policy.norm_key(k): v for k, v in POST_F34E_STATES.items()}
    declared = {}
    for line in section.splitlines():
        plain_line = policy.strip_md(line).strip().removeprefix('- ').strip()
        if '=' not in plain_line:
            continue
        key, value = plain_line.split('=', 1)
        key = policy.norm_key(key)
        value = ' '.join(value.strip().upper().split())
        declared.setdefault(key, []).append(value)
    for key, value in expected.items():
        if declared.get(key) != [value]:
            out.append(f'{path}: {key} debe declararse una sola vez como {value}')
    for key in declared.keys() - expected.keys():
        out.append(f'{path}: declaración desconocida en estado vigente: {key}')
    out += [f'{path}: {v}' for v in policy.sta({'F34E_Decision_G0_SBX.md': section}, {})]
    candidate = text if additions is None else additions
    out += policy.clm({path: candidate}, {})
    legal = re.compile(r'aprobaci[oó]n\s+(?:legal|jur[ií]dica)|privacidad(?:\s+\w+){0,3}\s+aprobada|'
                       r'validaci[oó]n\s+institucional\s+obtenida', re.I)
    for line in policy.strip_md(candidate).splitlines():
        for prop, polarity in policy.claim_props(line):
            if polarity != 'neg' and legal.search(prop):
                out.append(f'{path}: aprobación externa no respaldada: {prop}')
    for required in ('F35-SBX exclusivamente sintético', 'RF-23 sigue humana', 'RF-29 sigue experimental/informativa',
                     'Sin scoring, recomendación ni selección automática'):
        if required not in section:
            out.append(f'{path}: falta la restricción «{required}»')
    # DH-09 y cierre: exactamente un estado del ciclo de vida de F35-SBX-A (antes de F35-SBX-A, INICIADA o CERRADA);
    # ningún otro estado en mayúsculas. CERRADA exige auditoría independiente PASS y F35-SBX-B NO INICIADA.
    found = [st for st in ('F35-SBX AÚN NO INICIADA', F35SBX_STARTED, F35SBX_CLOSED) if st in section]
    words = set(re.findall(r'F35-SBX-A\s+([A-ZÁÉÍÓÚÑ]{4,})\b', section))
    if len(found) != 1 or not words <= {'INICIADA', 'CERRADA'} or len(words) > 1:
        out.append(f'{path}: estado de F35-SBX-A ausente, contradictorio o desconocido')
    elif found[0] == F35SBX_CLOSED and ('auditoría independiente PASS' not in section
                                       or re.search(r'auditor[ií]a[^.;]*\bFAIL\b', section, re.I)
                                       or 'F35-SBX-B NO INICIADA' not in section):
        out.append(f'{path}: el cierre de F35-SBX-A exige auditoría independiente PASS y F35-SBX-B NO INICIADA')
    if re.search(r'F35-SBX-B\s+(?!NO\s+INICIADA)[A-ZÁÉÍÓÚÑ]{2,}\b', section):
        out.append(f'{path}: F35-SBX-B no puede figurar iniciada')
    return out


def post_document_checks(changed, runner=git_rc):
    out = []
    for path in sorted(changed & (GOVERNANCE_FILES | {'docs/academico/handoff/F34E_MACOS_HANDOFF.md'})):
        try:
            text = open(os.path.join(ROOT, path), encoding='utf-8').read()
            additions = None
            if path in GOVERNANCE_FILES:
                diff = q(runner, 'diff', '--no-ext-diff', '--unified=0', POST_ANCHOR, '--', path)[1]
                additions = '\n'.join(line[1:] for line in diff.splitlines()
                                      if line.startswith('+') and not line.startswith('+++'))
            out += post_doc_rules(path, text, additions)
        except (OSError, ValueError) as exc:
            out.append(f'{path}: contenido desconocido (falla cerrado): {exc}')
    return out


def post_policy_regressions():
    sample = '## Estado vigente F34E\n' + '\n'.join(f'- {k} = {v}' for k, v in POST_F34E_STATES.items())
    sample += ('\nF35-SBX exclusivamente sintético. F35-SBX AÚN NO INICIADA. RF-23 sigue humana. '
               'RF-29 sigue experimental/informativa. Sin scoring, recomendación ni selección automática.\n')
    results = [(not post_doc_rules('CLAUDE.md', sample), 'POST: gobierno explícito válido')]
    for path in sorted(POST_F34E_ALLOWLIST | POST_F34E_ARTIFACTS):
        results.append((post_f34e_path(path), f'POST: ruta exacta permitida {path}'))
    for path in ('docs/academico/handoff/otro.md', 'scripts/otro.sh', 'app/Models/X.php',
                 'routes/web.php', 'config/app.php', 'database/migrations/x.php',
                 'docs/academico/g0-evidence/README.md', 'docs/academico/otro.md'):
        results.append((not post_f34e_path(path), f'POST: ruta no autorizada rechazada {path}'))
    for key, value in POST_F34E_STATES.items():
        bad = sample.replace(f'{key} = {value}', f'{key} = ESTADO INCOMPATIBLE')
        results.append((bool(post_doc_rules('docs/academico/ACADEMIC_BASELINE.md', bad)),
                        f'POST: invariante {key} no puede cambiar'))
    for claim in ('G0 = APROBADA', 'Se obtuvo aprobación legal', 'La privacidad está aprobada',
                  'Se obtuvo validación institucional obtenida', 'F35 productiva = DESBLOQUEADA',
                  'Se autorizan datos reales', 'No cambia runtime, pero autoriza datos reales'):
        results.append((bool(post_doc_rules('README.md', sample, claim)), f'POST: afirmación rechazada {claim}'))
    results.append((bool(post_doc_rules('docs/academico/handoff/F34E_MACOS_HANDOFF.md', 'Solo instalación')),
                    'POST: handoff sin estados/restricciones rechazado'))
    # DH-02/DH-09 (F35-SBX-A): registro de inicio y rutas futuras autorizadas.
    started = sample.replace('F35-SBX AÚN NO INICIADA.', F35SBX_STARTED + ' — diseño, contratos, fixtures sintéticos '
                             'y validación académica. Sin runtime productivo ni capacidades de alcance C.')
    results.append((not post_doc_rules('CLAUDE.md', started), 'POST: F35-SBX-A INICIADA aceptada'))
    results.append((bool(post_doc_rules('CLAUDE.md', started.replace(F35SBX_STARTED, F35SBX_STARTED + '. F35-SBX AÚN '
                                                                     'NO INICIADA'))),
                    'POST: inicio contradictorio (iniciada y no iniciada) rechazado'))
    results.append((bool(post_doc_rules('CLAUDE.md', sample.replace('F35-SBX AÚN NO INICIADA.', ''))),
                    'POST: estado de inicio ausente rechazado'))
    # Cierre de F35-SBX-A: estado CERRADA coherente aceptado; combinaciones y estados no canónicos rechazados.
    closed = sample.replace('F35-SBX AÚN NO INICIADA.', F35SBX_CLOSED + ' — diseño, contratos, fixtures sintéticos y '
                            'validador completados, tras auditoría independiente PASS. Sin runtime productivo ni '
                            'capacidades de alcance C. F35-SBX-B NO INICIADA.')
    results.append((not post_doc_rules('CLAUDE.md', closed), 'POST: F35-SBX-A CERRADA coherente aceptada'))
    for label, bad in (('INICIADA y CERRADA', closed.replace(F35SBX_CLOSED, F35SBX_STARTED + '. ' + F35SBX_CLOSED, 1)),
                       ('FINALIZADA', closed.replace(F35SBX_CLOSED, 'F35-SBX-A FINALIZADA', 1)),
                       ('COMPLETADA', closed.replace(F35SBX_CLOSED, 'F35-SBX-A COMPLETADA', 1)),
                       ('auditoría FAIL', closed.replace('auditoría independiente PASS', 'auditoría independiente FAIL', 1)),
                       ('F35-SBX-B INICIADA', closed.replace('F35-SBX-B NO INICIADA', 'F35-SBX-B INICIADA', 1)),
                       ('G0 real APROBADA', closed.replace('G0 real = NO APROBADA', 'G0 real = APROBADA', 1)),
                       ('F35 productiva HABILITADA', closed.replace('F35 productiva = BLOQUEADA', 'F35 productiva = HABILITADA', 1)),
                       ('alcance C HABILITADO', closed.replace('Alcance C = BLOQUEADO', 'Alcance C = HABILITADO', 1)),
                       ('datos reales PERMITIDOS', closed.replace('Datos reales = PROHIBIDOS', 'Datos reales = PERMITIDOS', 1))):
        results.append((bool(post_doc_rules('CLAUDE.md', bad)), f'POST: cierre F35-SBX-A con {label} rechazado'))
    for path in ('docs/academico/evidencia-sbx/README.md', 'docs/academico/evidencia-sbx/fixtures/manifest.json',
                 'docs/academico/tools/f35sbx/validate_f35sbx.py'):
        results.append((post_f34e_path(path), f'POST: ruta F35-SBX permitida {path}'))
    for path in ('docs/academico/evidencia-sbx/foto.png', 'docs/academico/evidencia-sbx/informe.pdf',
                 'docs/academico/evidencia-sbx/x.py', 'docs/academico/evidencia-sbx/datos.sqlite',
                 'docs/academico/tools/f35sbx/datos.json', 'docs/academico/evidencia-sbx-otro/a.md',
                 'docs/academico/evidencia-sbx/../g0-evidence/a.md', 'docs/academico/evidencia-sbx//a.md',
                 'docs/academico/tools/f35sbx-otro/x.py', 'docs/academico/evidencia-sbx\\a.md'):
        results.append((not post_f34e_path(path), f'POST: ruta F35-SBX no autorizada rechazada {path}'))
    for label, data, ok in (('texto', b'# F35-SBX-A\n', True), ('ausente', None, False), ('NUL', b'a\x00b', False),
                            ('CR', b'a\r\n', False), ('no UTF-8', b'\xff\xfe', False),
                            ('tamaño', b'a' * (F35SBX_MAX_BYTES + 1), False)):
        results.append(((not f35sbx_content('docs/academico/evidencia-sbx/a.md', data)) == ok,
                        f'POST: contenido F35-SBX {label}'))
    results.append((bool(f35sbx_content('docs/academico/evidencia-sbx/a.json', b'{"a": ')),
                    'POST: JSON F35-SBX inválido rechazado'))
    return results
PROTECTED = ['app', 'routes', 'config', 'database', 'resources', 'tests', 'cypress', 'ml-service', 'composer.json',
             'composer.lock', 'package.json', 'package-lock.json', 'docker-compose.yml', 'Dockerfile',
             'docs/v1.1/scope-preliminary.md', 'docs/final-report/traceability-master.md',
             'docs/rf-implementation-matrix.md', 'docs/assumptions.md', 'docs/academico/diseno-inteligente',
             'docs/academico/datos-sinteticos', 'docs/academico/g0-readiness', 'docs/academico/tools/f34a']


def protected_path(p):
    return any(p == x or p.startswith(x.rstrip('/') + '/') for x in PROTECTED)


def git_scope(runner=git_rc, reader=disk_reader):
    """Delta propio estricto; post permite académicos nuevos, sin cambiar evidencias cerradas.

    Todas las consultas pasan por q. Solo rc=1 en resolución de ancla o prueba de ancestro tiene significado.
    Ancla ausente/no ancestral en una fase posterior, Git ausente o consulta inesperada: UNKNOWN/FAIL cerrado.
    En post, cada ruta F35-SBX (DH-02) se lee con reader y debe ser texto: una ruta ausente o ilegible falla.
    """
    try:
        if q(runner, 'rev-parse', '--is-inside-work-tree')[1].strip() != 'true':
            raise GitError('repositorio inválido')
        head = q(runner, 'rev-parse', '--verify', '--quiet', 'HEAD^{commit}')[1].strip()
        branch = q(runner, 'rev-parse', '--abbrev-ref', 'HEAD')[1].strip()
        if not re.fullmatch(r'[0-9a-f]{40}', head) or not branch or branch == 'HEAD':
            raise GitError('HEAD o rama desconocidos')
        rc, anchor = q(runner, 'rev-parse', '--verify', '--quiet', POST_ANCHOR + '^{commit}', ok=(0, 1))
        own = branch in OWN_BRANCHES
        if rc == 1:
            if not own:
                raise GitError('ancla inexistente fuera de rama propia')
        else:
            if anchor.strip() != POST_ANCHOR:
                raise GitError('resolución de ancla incoherente')
            ancestral = q(runner, 'merge-base', '--is-ancestor', POST_ANCHOR, 'HEAD', ok=(0, 1))[0] == 0
            if not ancestral and not own:
                raise GitError('fase posterior sin cierre F34D en su historia')
        mode = 'delta' if own else 'post'
        base = BASE if own else POST_ANCHOR
        resolved = q(runner, 'rev-parse', '--verify', '--quiet', base + '^{commit}')[1].strip()
        if not re.fullmatch(r'[0-9a-f]{40}', resolved):
            raise GitError('base inválida')
        changed = paths(q(runner, 'diff', '--name-only', base)[1])
        untracked = paths(q(runner, 'ls-files', '--others', '--exclude-standard')[1])
        touched = paths(q(runner, 'diff', '--name-only', base, '--', *PROTECTED)[1])
        touched |= {p for p in untracked if protected_path(p)}
        if own:
            touched.discard(F34A_VALIDATOR)  # excepción histórica autorizada solo en el delta propio
        changed |= untracked
        out = []
        if own:
            subjects = q(runner, 'log', '-3', '--format=%s')[1].splitlines()
            committed = paths(q(runner, 'diff-tree', '--no-commit-id', '--name-only', '-r', 'HEAD')[1])
            dirty = paths(q(runner, 'diff', '--name-only', 'HEAD', '--', *sorted(GOVERNANCE_FILES))[1])
            gov = closure_scope(subjects, committed, dirty)
            outside = {p for p in changed if not p.startswith(('docs/academico/g0-evidence/',
                        'docs/academico/tools/f34b/')) and p != F34A_VALIDATOR and p not in gov}
        else:
            frozen = paths(q(runner, 'diff', '--name-only', POST_ANCHOR, '--', *IMMUTABLE)[1])
            frozen |= {p for p in untracked if p.startswith(IMMUTABLE)}
            if frozen:
                out.append(f'evidencias F34B/C/D cerradas modificadas: {sorted(frozen)[:5]}')
            outside = {p for p in changed if not post_f34e_path(p)}
            for p in sorted(p for p in changed if post_f35sbx_path(p)):
                out += f35sbx_content(p, reader(p))
            hist = sorted(changed & F35SBX_HISTORICAL)
            scope = f35sbx_scope_module() if hist else None
            for p in hist:
                if scope is None or not scope.validator_ok(p, ROOT, lambda root, *a: runner(*a),
                                                           lambda root, path: reader(path)):
                    out.append(f'{p}: adaptación distinta de la autorizada en F35-SBX-A (falla cerrado)')
            out += post_document_checks(changed, runner)
        if outside:
            out.append(f'cambios fuera del alcance {mode}: {sorted(outside)[:5]}')
        if touched:
            out.append(f'runtime, baseline, F33, F34 o F34A modificados: {sorted(touched)[:5]}')
        return out, mode
    except GitError as e:
        return [f'UNKNOWN: {e}; falla cerrado'], 'unknown'


def git_checks(runner=git_rc):
    out, mode = git_scope(runner)
    adr = open(os.path.join(ROOT, 'docs', 'academico', 'diseno-inteligente', 'F33_ADR_005_G0.md'), encoding='utf-8').read()
    if '- **Estado:** **PROPUESTA**' not in adr or 'G0 = NO APROBADA' not in adr:
        out.append('ADR-005 debe seguir PROPUESTA y G0 NO APROBADA')
    return out


def scope_regressions():
    """Git simulado en memoria: no escribe objetos, archivos ni evidencia externa."""
    own = sorted(OWN_BRANCHES)[0]
    post = 'feature/f34e-g0-sbx-synthetic-authorization'
    def fake(branch=post, changed='', untracked='', protected='', frozen='', anchor_rc=0,
             ancestor_rc=0, fault=None, fault_rc=128, inside='true', head='a' * 40, shows=None):
        def runner(*args):
            if fault is not None and args[:len(fault)] == fault:
                return fault_rc, ''
            if args == ('rev-parse', '--is-inside-work-tree'):
                return 0, inside
            if args == ('branch', '--show-current'):
                return 0, branch
            if args[:1] == ('show',) and shows is not None:
                return (0, shows[args[1]]) if args[1] in shows else (128, '')
            if args == ('rev-parse', '--verify', '--quiet', 'HEAD^{commit}'):
                return 0, head
            if args == ('rev-parse', '--abbrev-ref', 'HEAD'):
                return 0, branch
            if args == ('rev-parse', '--verify', '--quiet', POST_ANCHOR + '^{commit}'):
                return anchor_rc, POST_ANCHOR if anchor_rc == 0 else ''
            if args[:3] == ('rev-parse', '--verify', '--quiet'):
                return 0, 'b' * 40
            if args[:2] == ('merge-base', '--is-ancestor'):
                return ancestor_rc, ''
            if args[:2] == ('diff', '--name-only'):
                if '--' not in args:
                    return 0, changed
                return 0, frozen if args[args.index('--') + 1:] == IMMUTABLE else protected
            if args[:2] == ('ls-files', '--others'):
                return 0, untracked
            if args[:1] == ('log',):
                return 0, ''
            if args[:1] == ('diff-tree',):
                return 0, ''
            raise AssertionError(f'consulta no cubierta por arnés: {args}')
        return runner
    cases = [
        ('delta propio legítimo', fake(branch=own, changed='docs/academico/g0-evidence/README.md'), True),
        ('post académico legítimo', fake(untracked='docs/academico/g0-sandbox/README.md'), True),
        ('delta propio rechaza fase futura', fake(branch=own, untracked='docs/academico/g0-sandbox/README.md'), False),
        ('documento cerrado', fake(frozen='docs/academico/g0-evidence/F34B_Validacion_Necesidad.md'), False),
        ('adjunto nuevo no registrado', fake(untracked='docs/academico/g0-evidence/adjuntos/nuevo.png'), False),
        ('runtime', fake(changed='app/Models/User.php', protected='app/Models/User.php'), False),
        ('ADR', fake(protected='docs/academico/diseno-inteligente/F33_ADR_005_G0.md'), False),
        ('F34A cerrado', fake(protected='docs/academico/g0-readiness/README.md'), False),
        ('fuera de alcance', fake(changed='docs/README.md'), False),
        ('ancla ausente propia segura', fake(branch=own, anchor_rc=1), True),
        ('ancla ausente post', fake(anchor_rc=1), False),
        ('ancla no ancestral post', fake(ancestor_rc=1), False),
        ('repositorio inválido', fake(inside='false'), False),
        ('HEAD vacío', fake(head=''), False),
        ('HEAD inválido rc 1', fake(fault=('rev-parse', '--verify', '--quiet', 'HEAD^{commit}'), fault_rc=1), False),
        ('base propia no resuelta', fake(branch=own, fault=('rev-parse', '--verify', '--quiet', BASE + '^{commit}')), False),
        ('diff de protegidos fallido', fake(fault=('diff', '--name-only', POST_ANCHOR, '--', *PROTECTED)), False),
        ('diff de evidencias cerradas fallido', fake(fault=('diff', '--name-only', POST_ANCHOR, '--', *IMMUTABLE)), False),
        ('Git no disponible', fake(fault=(), fault_rc=None), False),
    ]
    queries = [('rev-parse', '--is-inside-work-tree'), ('rev-parse', '--verify', '--quiet', 'HEAD^{commit}'),
               ('rev-parse', '--abbrev-ref'), ('rev-parse', '--verify', '--quiet', POST_ANCHOR + '^{commit}'),
               ('merge-base', '--is-ancestor'), ('diff', '--name-only'), ('ls-files', '--others')]
    for query in queries:
        for rc in (2, 128, 129):
            cases.append((f'Git fallo {rc} {query}', fake(fault=query, fault_rc=rc), False))
    for query in [('log',), ('diff-tree',), ('diff', '--name-only', 'HEAD')]:
        cases.append((f'consulta gobierno falla {query}', fake(branch=own, fault=query), False))
    for path in ('docs/academico/handoff/otro.md', 'scripts/otro.sh', 'app/Models/X.php',
                 'routes/web.php', 'config/app.php', 'database/migrations/x.php',
                 'docs/academico/g0-evidence/README.md'):
        cases.append((f'post rechaza {path}', fake(changed=path, frozen=path if path.startswith(IMMUTABLE) else ''), False))
    # DH-02 (F35-SBX-A): carpetas autorizadas con contenido de texto; todo lo demás sigue fallando cerrado.
    sbx_md, sbx_json = 'docs/academico/evidencia-sbx/README.md', 'docs/academico/evidencia-sbx/fixtures/ORG-S1.json'
    sbx_py = 'docs/academico/tools/f35sbx/validate_f35sbx.py'
    text = {sbx_md: b'# F35-SBX-A\n', sbx_json: b'{"a": 1}\n', sbx_py: b'import json\n'}
    f35 = [
        ('F35-SBX legítimo', fake(untracked='\n'.join(text)), True, text),
        ('F35-SBX binario con extensión .json', fake(untracked=sbx_json), False, {sbx_json: b'\x89PNG\x00'}),
        ('F35-SBX JSON inválido', fake(untracked=sbx_json), False, {sbx_json: b'{"a": '}),
        ('F35-SBX archivo ilegible', fake(untracked=sbx_md), False, {}),
        ('F35-SBX imagen', fake(untracked='docs/academico/evidencia-sbx/foto.png'), False, {}),
        ('F35-SBX vídeo', fake(untracked='docs/academico/evidencia-sbx/sesion.mp4'), False, {}),
        ('F35-SBX Python fuera de tools', fake(untracked='docs/academico/evidencia-sbx/x.py'), False, {}),
        ('F35-SBX JSON en tools', fake(untracked='docs/academico/tools/f35sbx/datos.json'), False,
         {'docs/academico/tools/f35sbx/datos.json': b'{}'}),
        ('F35-SBX con runtime', fake(untracked=sbx_md + '\napp/Models/X.php', protected='app/Models/X.php'), False,
         text),
        ('F35-SBX con tests/', fake(untracked=sbx_md + '\ntests/Feature/SbxTest.php'), False, text),
        ('F35-SBX con evidencias cerradas', fake(untracked=sbx_md, frozen='docs/academico/g0-evidence/README.md',
                                                 changed='docs/academico/g0-evidence/README.md'), False, text),
        ('F35-SBX con baseline RF', fake(untracked=sbx_md, changed='docs/final-report/traceability-master.md',
                                         protected='docs/final-report/traceability-master.md'), False, text),
        ('F35-SBX con Git no disponible', fake(untracked=sbx_md, fault=(), fault_rc=None), False, text),
    ]
    # F35-SBX-A: tres validadores históricos, solo con la adaptación exacta comprobada contra la base fija.
    result = []
    scope = f35sbx_scope_module()
    bases = {p: git_rc('show', f'{scope.F35SBX_BASE}:{p}')[1] for p in sorted(F35SBX_HISTORICAL)} if scope else {}
    if not scope or not all(bases.values()):
        result.append((False, 'SCOPE: módulo o base de F35-SBX-A ilegibles (falla cerrado)'))
    else:
        shows = {f'{scope.F35SBX_BASE}:{p}': b for p, b in bases.items()}
        good = {p: scope.expected_validator(p, b).encode('utf-8') for p, b in bases.items()}
        extra = {p: t + b"\nprint('cambio no autorizado')\n" for p, t in good.items()}
        br = scope.F35SBX_BRANCH
        f34 = 'docs/academico/tools/f34/validate_f34.py'
        f35 += [
            ('F35-SBX validadores históricos adaptados', fake(branch=br, changed='\n'.join(good), shows=shows), True, good),
            ('F35-SBX validador histórico con HEAD posterior a la base',
             fake(branch=br, changed=f34, shows=shows, head='c' * 40), True, good),
            ('F35-SBX validador histórico en otra rama', fake(branch='feature/otra', changed=f34, shows=shows), False, good),
            ('F35-SBX validador histórico con base ilegible', fake(branch=br, changed=f34, shows={}), False, good),
            ('F35-SBX cuarto validador no autorizado', fake(branch=br, changed='docs/academico/tools/f34a/validate_f34a.py',
                                                            protected='docs/academico/tools/f34a/validate_f34a.py',
                                                            shows=shows), False, good),
            ('F35-SBX otro archivo de tools/f30', fake(branch=br, changed='docs/academico/tools/f30/f30.py', shows=shows),
             False, good),
            ('F35-SBX validate_f29 no autorizado', fake(branch=br, shows=shows,
                                                        changed='docs/academico/powerdesigner/scripts/validate_f29.py'),
             False, good),
        ]
        for p in sorted(F35SBX_HISTORICAL):
            f35.append((f'F35-SBX cambio funcional extra en {p}', fake(branch=br, changed=p, shows=shows), False,
                        dict(good, **{p: extra[p]})))
    for label, runner, expected, *files in cases + f35:
        reader = (lambda p, f=files[0]: f.get(p)) if files else disk_reader
        violations, mode = git_scope(runner, reader)
        result.append(((not violations) == expected, f'SCOPE: {label} → {mode}: {violations}'))
    return result


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
    add(len(CASES) >= 140, f'casos negativos: {len(CASES)}')
    add(not g12_structure(D[NEC], NEC) and derive(D, REAL)['G0-12'] == 'PENDIENTE EXTERNO',
        'G0-12 real: tabla de metadatos única, completa y bien formada; sigue PENDIENTE EXTERNO')
    # Positivo F34D (simulado en memoria): evidencia válida + identidad verificable + necesidad validada → G0-12 CUMPLIDO.
    Dg = g12_coherent()(D)
    rg = run_rules(Dg, G12_CTX)
    bad_g = {k: v[:1] for k, v in rg.items() if v and k in ('REC', 'IDN', 'EVD', 'G12', 'LIM', 'PHASE', 'DATA', 'SCOPE')}
    add(not bad_g and derive(Dg, G12_CTX)['G0-12'] == 'CUMPLIDO' and not real_exists(G12_CTRL)
        and not real_exists(G12_CTRL2) and derive(D, REAL)['G0-12'] == 'PENDIENTE EXTERNO',
        f'POS-07 positivo (simulado): adjunto válido + identidad del docente verificable + necesidad validada → '
        f'G0-12 CUMPLIDO {bad_g}')
    add(REAL.teacher == 'Maglioni Arana Caparachin', f'docente del curso leído de CLAUDE.md: «{REAL.teacher}»')
    ok_text = ('La respuesta del docente no es una aprobación jurídica, de privacidad ni una autorización del Colegio '
               'Andino, y tampoco autoriza datos reales ni el alcance C.')
    add(not lim(claim(ok_text)(D), REAL), 'LIM positivo: una frase con todas las categorías negadas no falla')
    add(not teacher_match('Max Magnolie Arana', REAL.teacher) and not teacher_match('Maglioni Arana', REAL.teacher),
        'identidad del docente: «Max Magnolie Arana» y nombres parciales no se aceptan sin variante revisada')
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
    checks.extend(scope_regressions())
    checks.extend(post_policy_regressions())
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
