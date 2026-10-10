"""F33 — Validación del diseño funcional del motor inteligente y ADR-005 / G0 (sin red).

Comprueba:
  1. Entregables presentes.
  2. Resultado G0 único y coherente: NO APROBADA; ningún documento declara G0 aprobada como estado vigente.
  3. ADR-005: secciones obligatorias, alternativas A–E, estado PROPUESTA, los 13 criterios G0 exigidos.
  4. Matriz: clasificaciones válidas; capacidades críticas BLOQUEADAS; resumen coherente con las filas.
  5. Mapa F34–F40: F34 habilitada; F35–F40 bloqueadas con G0 NO APROBADA.
  6. Principio central, RF-23 humana e inferencias prohibidas presentes.
  7. Citas [Sxx]/[Oxx]/[Xxx] existentes y verificadas en F30.
  8. Enlaces relativos y anclas.
  9. Diagramas reproducibles (se regeneran en memoria y se comparan) y DOCX actualizado.
 10. Git: cambios solo en docs/academico/ y nada en runtime.
Uso: python docs/academico/tools/f33/validate_f33.py
"""
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
DIR = os.path.join(ROOT, 'docs', 'academico', 'diseno-inteligente')
DOCS = ['README.md', 'F33_ADR_005_G0.md', 'F33_Diseno_Funcional_Motor_Inteligente.md',
        'F33_Matriz_Capacidades_y_Restricciones.md', 'F33_Flujos_Funcionales.md', 'F33_Mapa_F34_F40.md']
CLASES = ('PERMITIDA', 'PERMITIDA CON RESTRICCIONES', 'FUTURA', 'BLOQUEADA')
CRITICAS = ('CAP-10', 'CAP-11', 'CAP-15', 'CAP-16', 'CAP-17', 'CAP-19', 'CAP-21', 'CAP-22', 'CAP-23', 'CAP-25',
            'CAP-35', 'CAP-36')
CRITERIOS = ('Evidencia científica', 'Normativa', 'Privacidad', 'Datos disponibles', 'Calidad de etiquetas',
             'Riesgo de sesgo', 'Explicabilidad', 'Supervisión humana', 'Seguridad', 'Auditabilidad',
             'Reproducibilidad', 'Necesidad institucional', 'Proporcionalidad')
PROHIBIDAS = ('personalidad', 'honestidad', 'inteligencia', 'estrés', 'estabilidad emocional', 'liderazgo',
              'salud mental', 'idoneidad')
RUNTIME = ('app/', 'routes/', 'config/', 'database/', 'resources/', 'tests/', 'cypress/', 'ml-service/', 'bootstrap/',
           'public/', 'composer.', 'package', 'docker', 'Dockerfile', '.github/')

res = []


def check(ok, msg):
    res.append((bool(ok), msg))


def leer(n):
    with open(os.path.join(DIR, n), encoding='utf-8') as f:
        return f.read()


def slug(h):
    h = re.sub(r'[`*_]', '', h.strip().lower())
    h = re.sub(r'[^\w\- ]', '', h)
    return h.replace(' ', '-')


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    # 1. entregables
    for n in DOCS + ['diagramas/F33-01_flujo_funcional.png', 'diagramas/F33-02_arquitectura_funcional.png',
                     'F33_Diseno_Motor_Inteligente.docx', 'F33_Diseno_Motor_Inteligente.pdf']:
        check(os.path.isfile(os.path.join(DIR, n)), f'entregable presente: {n}')
    txt = {n: leer(n) for n in DOCS}
    todo = '\n'.join(txt.values())

    # 2. G0
    for n, t in txt.items():
        check('NO APROBADA' in t, f'{n}: declara G0 NO APROBADA')
    vigente = re.findall(r'G0\s*=\s*\**\s*(APROBADA[^\n|.*]*|NO APROBADA)', todo)
    check(vigente and all(v.startswith('NO APROBADA') for v in vigente),
          f'todas las declaraciones «G0 = …» dicen NO APROBADA ({len(vigente)})')
    adr = txt['F33_ADR_005_G0.md']
    m = re.search(r'## 10\. Resultado G0 en F33\s+\*\*G0 = NO APROBADA\.\*\*', adr)
    check(m, 'ADR-005 §10: resultado explícito G0 = NO APROBADA')

    # 3. ADR-005
    for sec in ('Contexto', 'Problema', 'Fuerzas', 'Alternativas', 'Evidencia y restricciones', 'Decisión',
                'Consecuencias', 'Riesgos y controles', 'Puerta G0', 'Resultado G0', 'Condiciones de reversión',
                'Fases habilitadas y bloqueadas'):
        check(re.search(r'^## \d+\. ' + sec, adr, re.M), f'ADR-005: sección «{sec}»')
    check('**Estado:** **PROPUESTA**' in adr, 'ADR-005: estado PROPUESTA (no se autoaprueba)')
    for a in 'ABCDE':
        check(re.search(r'^\| \*\*' + a + r'\*\* \|', adr, re.M), f'ADR-005: alternativa {a}')
    for c in CRITERIOS:
        check(re.search(r'\| G0-\d\d \| \*\*' + c + r'\*\*', adr), f'G0: criterio «{c}»')
    check('Se ratifican ADR-001 y ADR-002 sin enmienda' in adr, 'ADR-005 ratifica ADR-001 y ADR-002')
    check(re.search(r'\*\*D se rechaza\*\*', adr), 'ADR-005 rechaza la alternativa D')

    # 4. matriz
    mat = txt['F33_Matriz_Capacidades_y_Restricciones.md']
    filas = re.findall(r'^\| (CAP-\d\d) \| [^|]+ \| \*\*([^*]+)\*\*', mat, re.M)
    check(len(filas) >= 18, f'matriz: {len(filas)} capacidades')
    clase = {}
    for cap, c in filas:
        base = next((k for k in sorted(CLASES, key=len, reverse=True) if c.startswith(k)), None)
        check(base, f'{cap}: clasificación válida ({c})')
        clase[cap] = base
    for cap in CRITICAS:
        check(clase.get(cap) == 'BLOQUEADA', f'{cap}: BLOQUEADA')
    resumen = dict(re.findall(r'^\| (PERMITIDA CON RESTRICCIONES|PERMITIDA|FUTURA|BLOQUEADA) \| ([^|]+) \|', mat,
                              re.M))
    for k, v in resumen.items():
        nums = {f'CAP-{int(x):02d}' for x in re.findall(r'(?:CAP-)?(\d+)', v)}
        esperado = {c for c, b in clase.items() if b == k}
        check(nums == esperado, f'resumen {k}: coincide con las filas')
    for tema in ('requisitos obligatorios', 'Rúbricas', 'Ponderaciones', 'Evidencia por competencia',
                 'Extracción automática', 'semántica', 'Búsqueda léxica', 'Resumen automático', 'Comparación',
                 'Ranking actual RF-21', 'Scoring', 'Recomendación de candidatos', 'entrevistas', 'Embeddings',
                 'LLM', 'ML supervisado', 'audio', 'Explicabilidad', 'equidad'):
        check(tema.lower() in mat.lower(), f'matriz cubre «{tema}»')

    # 5. mapa
    mapa = txt['F33_Mapa_F34_F40.md']
    check(re.search(r'^\| \*\*F34[^|]*\*\* \| \*\*HABILITADA', mapa, re.M), 'mapa: F34 HABILITADA')
    for f in ('F35', 'F36', 'F37', 'F38', 'F39', 'F40'):
        check(re.search(r'^\| \*\*' + f + r'[^|]*\*\* \| BLOQUEAD[AO] \|', mapa, re.M),
              f'mapa: {f} bloqueada con G0 NO APROBADA')

    # 6. principio y prohibiciones
    dis = txt['F33_Diseno_Funcional_Motor_Inteligente.md']
    check('RECOMENDACIÓN / APOYO DEL SISTEMA ≠ DECISIÓN FINAL HUMANA' in dis, 'principio central presente')
    check('RF-23 sigue siendo exclusivamente humana' in dis, 'RF-23 humana')
    for p in PROHIBIDAS:
        check(p in dis.lower(), f'inferencia prohibida listada: {p}')
    check('**No existe**' in dis and '`scores` del sistema' in dis, 'no se reserva un campo de score del sistema')

    # 6b. Frontera B/C (F33-M01): B sin dependencias nuevas ni extracción automática de PDF/DOCX.
    fila = lambda t, cap: next((ln for ln in t.splitlines() if ln.startswith(f'| {cap} |')), '')
    cap07, cap08 = fila(mat, 'CAP-07'), fila(mat, 'CAP-08')
    check(clase.get('CAP-07') == 'FUTURA' and 'PDF' in cap07 and 'OCR' in cap07,
          'CAP-07: extracción automática de PDF/DOCX/OCR es FUTURA (alcance C)')
    check('introducido por una persona' in cap08 and 'sin dependencias nuevas' in cap08
          and not re.search(r'(necesita|requiere|implica)[^|]*(extraer|parsing|dependencia)', cap08, re.I),
          'CAP-08: búsqueda determinista solo sobre texto introducido por personas, sin extracción ni dependencias')
    for n in ('F33_ADR_005_G0.md', 'F33_Diseno_Funcional_Motor_Inteligente.md',
              'F33_Matriz_Capacidades_y_Restricciones.md', 'F33_Mapa_F34_F40.md'):
        check('**Frontera B/C.**' in txt[n], f'{n}: declara la frontera B/C')
    check(re.search(r'^\| \*\*B\*\* \|[^|]*Sin dependencias nuevas ni extracción automática', adr, re.M),
          'ADR-005: alternativa B sin dependencias ni extracción automática')
    check('**ninguna dependencia nueva**' in fila(adr, 'G0-15'), 'G0-15: B sin dependencias nuevas')
    celdas = lambda t, pat: [c.strip() for c in next((ln for ln in t.splitlines() if re.match(pat, ln)), '|').split('|')]
    f35_mapa = celdas(mapa, r'^\| \*\*F35')
    f35_adr = celdas(adr, r'^\| F35 ')
    for nombre, c in (('mapa', f35_mapa), ('ADR-005', f35_adr)):
        b = c[3] if len(c) > 3 else ''
        check(b and not re.search(r'PDF|DOCX|OCR|embedding|extracción automática', b),
              f'{nombre}: F35 con G0 CON RESTRICCIONES no incluye extracción automática ni OCR')

    # 6c. FF-02 alineado con AssessmentResultRecorder (F33-M02).
    flu = txt['F33_Flujos_Funcionales.md']
    ff02 = flu[flu.index('## FF-02'):flu.index('## FF-03')]
    check('AssessmentResultRecorder' in ff02, 'FF-02 cita AssessmentResultRecorder')
    check('`PROGRAMADA` → registro del resultado → `REALIZADA`' in ff02, 'FF-02: PROGRAMADA → registro → REALIZADA')
    pre = ff02[ff02.index('**Precondiciones:**'):ff02.index('**Pasos:**')]
    check('`PROGRAMADA`' in pre and 'realizada' not in pre.lower(), 'FF-02: precondición sesión PROGRAMADA')
    check('ANOTACIONES COMPLEMENTARIAS' in ff02 and 'no se crea un segundo resultado' in ff02,
          'FF-02: complementos como anotaciones complementarias, sin segundo resultado')
    seg = re.compile(r'(corrección|corregir|corrige)[^.\n]{0,40}(?<!no se )(crea|registra) (un |otro )?'
                     r'(nuevo|segundo|otro)? ?(registro|resultado)', re.I)
    malos = [n for n, t in txt.items() if seg.search(t) or 'corrección es un registro nuevo' in t]
    check(not malos, f'ningún documento permite segundos resultados como corrección: {malos}')
    check('E-13' in dis and '`PROGRAMADA` → `REALIZADA`' in dis, 'diseño: estados vigentes y E-13')

    # 6d. Datos reales (F33-M03).
    malos = [n for n, t in txt.items() if re.search(r'consentid', t, re.I)]
    check(not malos, f'sin «datos consentidos» como vía de G0: {malos}')
    for n in ('F33_ADR_005_G0.md', 'F33_Diseno_Funcional_Motor_Inteligente.md',
              'F33_Matriz_Capacidades_y_Restricciones.md', 'F33_Mapa_F34_F40.md'):
        check('F33 y G0 **no autorizan datos reales de candidatos**' in txt[n]
              and 'el consentimiento por sí solo **no**' in txt[n], f'{n}: regla de datos completa')
    check('**Ningún estado de G0 autoriza datos reales de candidatos**' in adr, 'ADR-005: G0 no autoriza datos reales')
    check('solo con datos sintéticos' in fila(adr, 'G0-01'), 'G0-01: solo datos sintéticos')
    check('consentimiento por sí solo no' in fila(mat, 'CAP-36'), 'CAP-36: consentimiento no habilita datos reales')
    f34 = celdas(mapa, r'^\| \*\*F34')
    check(len(f34) > 4 and all(not re.search(r'reales|consent', x, re.I) for x in f34[2:5]),
          'mapa: F34 y sus estados G0 sin datos reales')

    # 6e. analysis_run inmutable + eventos (LOW).
    check('`analysis_run_events`' in dis and 'registro principal inmutable' in dis,
          'analysis_run inmutable con eventos de solo inserción')
    malos = [n for n, t in txt.items() if re.search(r'`analysis_run`\s*(pasa|cambia) a', t)]
    check(not malos, f'ningún documento sobrescribe el estado de analysis_run: {malos}')

    # 6f. Diagrama: localizador → confirmación humana → ayuda visible (LOW).
    with open(os.path.join(HERE, 'diagramas.py'), encoding='utf-8') as f:
        src = f.read()
    orden = [src.find(x) for x in ("'C1 · Localizador documental'", "'C2 · Revisión y confirmación humana'",
                                   "'C3 · Ayuda visible (solo confirmados)'")]
    check(all(o > 0 for o in orden) and orden == sorted(orden) and "'después de P4'" in src,
          'diagrama: localizador → confirmación humana → ayuda visible, después de P4')

    # 7. citas
    sys.path.insert(0, os.path.join(HERE, '..', 'f30'))
    from fuentes import FUENTES  # noqa: E402
    with open(os.path.join(ROOT, 'docs', 'academico', 'investigacion-ia', 'datos', 'verificacion_fuentes.json'),
              encoding='utf-8') as f:
        ver = json.load(f)['fuentes']
    ids = {x[0] for x in FUENTES}
    citadas = set()
    for g in re.findall(r'\[((?:[SOX]\d{2})(?:[^\]]*))\]', todo):
        citadas.update(re.findall(r'\b[SOX]\d{2}\b', g))
    malas = sorted(c for c in citadas if c not in ids or not ver.get(c, {}).get('verificado'))
    check(citadas and not malas, f'citas F30 existentes y verificadas ({len(citadas)}): {malas}')

    # 8. enlaces y anclas
    rotos = []
    for n, t in txt.items():
        for link in re.findall(r'\]\(([^)\s]+)\)', t):
            if link.startswith(('http://', 'https://')):
                continue
            path, _, anchor = link.partition('#')
            target = os.path.normpath(os.path.join(DIR, path)) if path else os.path.join(DIR, n)
            if not os.path.exists(target):
                rotos.append(f'{n}→{link}')
            elif anchor and target.endswith('.md'):
                with open(target, encoding='utf-8') as f:
                    if anchor not in {slug(h) for h in re.findall(r'^#+ (.+)$', f.read(), re.M)}:
                        rotos.append(f'{n}→{link}')
    check(not rotos, f'enlaces y anclas: {rotos}')

    # 9. reproducibilidad
    import diagramas  # noqa: E402
    for name, fn in (('F33-01_flujo_funcional.png', diagramas.flujo),
                     ('F33-02_arquitectura_funcional.png', diagramas.arquitectura)):
        buf = io.BytesIO()
        fn().save(buf, format='PNG', optimize=True)
        with open(os.path.join(DIR, 'diagramas', name), 'rb') as f:
            check(hashlib.sha256(buf.getvalue()).hexdigest() == hashlib.sha256(f.read()).hexdigest(),
                  f'diagrama reproducible: {name}')
    with zipfile.ZipFile(os.path.join(DIR, 'F33_Diseno_Motor_Inteligente.docx')) as z:
        doc = z.read('word/document.xml').decode('utf-8')
        media = [n for n in z.namelist() if n.startswith('word/media/')]
    check(len(media) >= 2 and 'G0 = NO APROBADA' in doc, f'DOCX con {len(media)} imágenes y resultado G0')
    check(all(re.sub(r'[*`#|]', '', h).strip()[:40] in re.sub(r'<[^>]+>', '', doc)
              for h in re.findall(r'^## (.+)$', txt['F33_ADR_005_G0.md'], re.M)),
          'DOCX contiene las secciones vigentes de ADR-005')

    # 10. git
    st = subprocess.run(['git', 'status', '--porcelain', '--untracked-files=all'], cwd=ROOT, capture_output=True,
                        text=True, encoding='utf-8').stdout.splitlines()
    rutas = [ln[3:].strip('"') for ln in st]
    # Excepción F35-SBX-A (DH-09): solo CLAUDE.md y docs/PROGRESS.md con exactamente la apertura; si no, falla.
    sys.path.append(os.path.join(ROOT, 'docs', 'academico', 'tools', 'f35sbx'))
    import f35sbx_scope
    check(all(p.startswith('docs/academico/') or f35sbx_scope.governance_ok(p, ROOT) for p in rutas),
          f'cambios solo en docs/academico ({len(rutas)})')
    for ok, m in f35sbx_scope.regressions(ROOT):
        check(ok, m)
    check(not [p for p in rutas if p.startswith(RUNTIME)], '0 cambios de runtime o producto')

    fallas = [m for ok, m in res if not ok]
    for ok, m in res:
        if not ok:
            print('FALLA', m)
    print(f'validate_f33: {len(res) - len(fallas)} comprobaciones correctas, {len(fallas)} fallas')
    sys.exit(1 if fallas else 0)


if __name__ == '__main__':
    sys.path.insert(0, HERE)
    main()
