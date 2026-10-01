"""F30 — Validación de la investigación (sin red, salvo lo que ya está en datos/).

Comprueba:
  1. Toda cita [Sxx]/[Oxx]/[Xxx] de los documentos existe en fuentes.py y está verificada.
  2. No hay DOI ni URL duplicados; ninguna fuente tiene aviso de retractación o retirada; las excluidas no se usan.
  3. La matriz tiene todos los campos, niveles válidos y ficha para cada trabajo; cada norma tiene su fila.
  4. Las fuentes sin resumen no tienen cifras en «resultados».
  5. (con --abstracts DIR) cada cifra de «resultados» y «datos» aparece en el resumen publicado de su fuente.
  6. Cada decisión D-xx cita evidencia; las clasificaciones de herramientas son válidas y completas.
  7. Los documentos generados están al día (se regeneran en memoria y se comparan).
  8. Los enlaces relativos y sus anclas existen.
  9. Git: no hay cambios fuera de docs/academico/.
Uso: python docs/academico/tools/f30/validate_f30.py [--abstracts DIR]
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
OUT = os.path.join(ROOT, 'docs', 'academico', 'investigacion-ia')

import f30  # noqa: E402
from fuentes import FUENTES  # noqa: E402
from m_herramientas import CLASES, CLASIFICACION  # noqa: E402
from m_matriz import MATRIZ, NIVELES, OFICIALES, SR  # noqa: E402

DOCS = ['README.md', 'F30_Estado_del_Arte_IA_Reclutamiento.md', 'F30_Matriz_Evidencia_Cientifica.md',
        'F30_Analisis_Modelos_y_Tecnicas.md', 'F30_Explainability_Fairness_Gobernanza.md',
        'F30_Analisis_Herramientas_Skills.md', 'F30_Recomendaciones_F33_F40.md', 'REFERENCIAS.md']
CAMPOS = ('revision', 'objetivo', 'datos', 'tecnica', 'variables', 'metricas', 'resultados', 'limitaciones', 'sesgo',
          'aplicabilidad', 'decision', 'confianza')

PALABRAS = ('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve',
            'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty')

errores, avisos = [], []


def err(m):
    errores.append(m)


def leer(name):
    with open(os.path.join(OUT, name), encoding='utf-8') as f:
        return f.read()


def slug(h):
    h = re.sub(r'[`*_]', '', h.strip().lower())
    h = re.sub(r'[^\w\- ]', '', h)
    return h.replace(' ', '-')


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    ver = f30.VER['fuentes']
    ids = [f[0] for f in FUENTES]

    # 1. citas
    citadas = set()
    for d in DOCS:
        for grupo in re.findall(r'\[((?:[SOX]\d{2})(?:,\s*[SOX]\d{2})*)[^\]]*\]', leer(d)):
            citadas.update(re.findall(r'[SOX]\d{2}', grupo))
        for fid in re.findall(r'\b[SOX]\d{2}\b', leer(d)):
            if fid not in ids and re.match(r'[SOX]\d{2}$', fid):
                err(f'{d}: {fid} no existe en fuentes.py')
    for fid in sorted(citadas):
        if fid not in ids:
            err(f'cita inexistente {fid}')
        elif not ver.get(fid, {}).get('verificado'):
            err(f'cita no verificada {fid}')
    narrativos = set()
    for d in DOCS:
        if d not in ('F30_Matriz_Evidencia_Cientifica.md', 'REFERENCIAS.md'):
            narrativos.update(re.findall(r'\b[SOX]\d{2}\b', leer(d)))
    sin_uso = [i for i in ids if i not in narrativos]
    if sin_uso:
        avisos.append(f'fuentes que solo aparecen en la matriz (no en los documentos narrativos): {", ".join(sin_uso)}')

    # 2. duplicados y retractaciones
    dois = [f[1].lower() for f in FUENTES if f[1]]
    urls = [f[2] for f in FUENTES if f[2]]
    for x in set(dois):
        if dois.count(x) > 1:
            err(f'DOI duplicado {x}')
    for x in set(urls):
        if urls.count(x) > 1:
            err(f'URL duplicada {x}')
    for fid in ids:
        r = ver[fid]
        if not r.get('verificado'):
            err(f'{fid} no verificada')
        for a in r.get('avisos') or []:
            if any(w in a.lower() for w in ('retract', 'withdraw', 'removal', 'título')):
                err(f'{fid} tiene aviso {a}')
    for d, _, _ in f30.EXCLUIDAS:
        if d.lower() in dois:
            err(f'fuente excluida usada: {d}')

    # 3. matriz completa
    for fid in ids:
        if fid.startswith('S'):
            m = MATRIZ.get(fid)
            if not m:
                err(f'{fid} sin ficha')
                continue
            for c in CAMPOS:
                if not str(m.get(c, '')).strip():
                    err(f'{fid}: campo vacío {c}')
            if m['confianza'] not in NIVELES:
                err(f'{fid}: nivel inválido')
            # 4. sin resumen → sin cifras
            if SR in m['objetivo'] and re.search(r'\d', m['resultados']):
                err(f'{fid}: sin resumen pero con cifras en resultados')
        elif fid.startswith('O') and fid not in OFICIALES:
            err(f'{fid} sin fila de norma')

    # 5. cifras contra el resumen
    if '--abstracts' in sys.argv:
        adir = sys.argv[sys.argv.index('--abstracts') + 1]
        revisadas = 0
        for fid, m in MATRIZ.items():
            p = os.path.join(adir, fid + '.txt')
            if not os.path.exists(p):
                continue
            with open(p, encoding='utf-8') as f:
                abst = f.read().replace('\u2212', '-')
            plano = re.sub(r'[\s,]', '', abst)
            for i, w in enumerate(PALABRAS, 1):
                if re.search(r'\b' + w + r'\b', abst, re.I):
                    abst += f' {i}'
            for campo in ('resultados', 'datos'):
                for num in re.findall(r'\d[\d\s]*(?:,\d+)?', m[campo]):
                    n = num.strip().replace(' ', '')
                    variantes = {n, n.replace(',', '.'), n.replace(',', '.').lstrip('0'), n.replace(',', '')}
                    revisadas += 1
                    if not any(v and (v in abst or v in plano) for v in variantes):
                        avisos.append(f'{fid}.{campo}: la cifra «{n}» no aparece literal en el resumen (revisar)')
        print(f'cifras contrastadas con resúmenes: {revisadas}')

    # 6. decisiones y herramientas
    rec = leer('F30_Recomendaciones_F33_F40.md')
    filas = re.findall(r'^\| (D-\d{2}) \| [^|]+ \| ([^|]+) \|', rec, re.M)
    if len(filas) < 20:
        err(f'tabla de decisiones incompleta: {len(filas)} filas')
    for did, evid in filas:
        if not re.search(r'[SOX]\d{2}|ADR-\d{3}|[Cc]ontrato|[Hh]erramientas|RF-\d{2}', evid):
            err(f'{did} sin evidencia citada')
    with open(os.path.join(OUT, 'datos', 'herramientas.json'), encoding='utf-8') as f:
        H = json.load(f)
    nombres = {h['nombre'] for h in H['herramientas']}
    if nombres != set(CLASIFICACION):
        err(f'herramientas sin clasificar o sobrantes: {sorted(nombres ^ set(CLASIFICACION))}')
    for n, v in CLASIFICACION.items():
        if v[0] not in CLASES:
            err(f'{n}: clasificación inválida {v[0]}')
    faltan_gh = [h['nombre'] for h in H['herramientas'] if not h['github'].get('existe')]
    if faltan_gh:
        avisos.append(f'herramientas sin datos de GitHub: {len(faltan_gh)}')

    # 7. generados al día
    for name, fn in (('F30_Matriz_Evidencia_Cientifica.md', f30.matriz_md), ('REFERENCIAS.md', f30.referencias_md),
                     ('F30_Analisis_Herramientas_Skills.md', f30.herramientas_md)):
        if leer(name) != fn():
            err(f'{name} desactualizado: ejecutar f30.py')

    # 8. enlaces
    for d in DOCS:
        txt = leer(d)
        for link in re.findall(r'\]\(([^)\s]+)\)', txt):
            if link.startswith(('http://', 'https://', 'mailto:')):
                continue
            path, _, anchor = link.partition('#')
            target = os.path.normpath(os.path.join(OUT, path)) if path else os.path.join(OUT, d)
            if not os.path.exists(target):
                err(f'{d}: enlace roto {link}')
                continue
            if anchor and target.endswith('.md'):
                with open(target, encoding='utf-8') as f:
                    heads = {slug(h) for h in re.findall(r'^#+ (.+)$', f.read(), re.M)}
                if anchor not in heads:
                    err(f'{d}: ancla inexistente {link}')

    # 9. git
    st = subprocess.run(['git', 'status', '--porcelain', '--untracked-files=all'], cwd=ROOT, capture_output=True,
                        text=True, encoding='utf-8').stdout.splitlines()
    fuera = [ln for ln in st if not ln[3:].strip('"').startswith('docs/academico/')]
    if fuera:
        err(f'cambios fuera de docs/academico/: {fuera}')

    for a in avisos:
        print('AVISO', a)
    for e in errores:
        print('ERROR', e)
    print(f'fuentes {len(ids)}, citadas {len(citadas)}, decisiones {len(filas)}, herramientas {len(CLASIFICACION)}, '
          f'cambios en git {len(st)}')
    print('F30 VALIDACIÓN:', 'OK' if not errores else f'{len(errores)} ERRORES')
    sys.exit(1 if errores else 0)


if __name__ == '__main__':
    main()
