"""F35-SBX-B — gate sucesor sobre HEAD (incremento B1).

Valida el HEAD actual de la rama de B, de develop o de main (DH-B04). No sustituye esa validación por los gates
históricos congelados, que se ejecutan anclados como evidencia complementaria (DH-B01, DH-B02). Solo biblioteca
estándar. Primero recoge el estado real (Git, índice, sistema de archivos y documentos) y después evalúa reglas puras;
los casos negativos mutan una copia del estado en memoria.

  CTX  rama permitida, HEAD no separado; E, el cierre de B0 y la base de B como ancestros de HEAD.
  AIN  F35-SBX-A idéntica a E: bytes reales, sin archivos extra ni enlaces, árbol de HEAD sin cambios (DH-B09).
  B0F  documento de B0 idéntico a su cierre auditado.
  SBX  SBX-01..SBX-18 recalculados sobre HEAD con compute_sbx() de validate_f34e.py, importado solo tras verificar
       sus bytes y los de los módulos que carga contra E (DH-B13).
  GOV  trece estados exactos; F35-SBX-B solo INICIADA; ninguna declaración de estado contradictoria (en cualquier
       forma: mayúsculas, Markdown, =, :, :=, ->) ni afirmación positiva que desbloquee nada en lo vigente o añadido.
  SCP  delta exacto respecto de la base de B en el árbol de HEAD, el árbol de trabajo, el índice y lo no seguido.
  FSY  recorrido real de las carpetas de B y de las superficies del runtime, el dataset y la evidencia: ningún archivo
       que no esté en el árbol de HEAD (aunque Git lo ignore), ningún enlace; excepciones mínimas y explícitas.
  HST  historia completa E..HEAD: ningún commit (ni merge que difiera de todos sus padres) toca F35-SBX-A, aunque
       después se restaure; repositorio superficial o historia ilegible: falla cerrado.
  FLG  sin flags del índice: solo «H» en git ls-files -v (h = assume-unchanged, S = skip-worktree, s = ambos).
  CNT  archivos de B: UTF-8 sin NUL, CR ni BOM; sin PII; solo .md, .json y .py; claves JSON sin capacidades prohibidas
       y, en los documentos mutables de B, ninguna afirmación positiva que habilite una capacidad prohibida.
  DEP  código de tools/f35sbxb: biblioteca estándar autorizada, sin importaciones dinámicas ni dependencias de ML.

Cualquier error de Git, de lectura o de importación, criterio no evaluable o estado desconocido: falla cerrado (DH-B10).
"""
import os
import sys

# B1.4 — el gate solo corre en modo aislado (python -I): sin PYTHONPATH, sin sitio del usuario y sin el directorio del
# script en sys.path. Si se invoca de otro modo, se relanza a sí mismo aislado con os.spawnv (os ya está cargado: no
# se importa nada nuevo en un entorno no verificado) y devuelve su código de salida.
if __name__ == '__main__' and not sys.flags.isolated:
    _argv = [sys.executable, '-I', '-B'] + (['-X', 'utf8'] if sys.flags.utf8_mode else []) + \
        [os.path.abspath(__file__)] + sys.argv[1:]
    if os.name == 'nt':
        _argv = ['"' + a.replace('"', '\\"') + '"' if (' ' in a or '\t' in a) else a for a in _argv]
    sys.exit(os.spawnv(os.P_WAIT, sys.executable, _argv))

# B1.3 — antes de cualquier otra importación: ninguna ruta del repositorio en sys.path (un archivo plantado no puede
# sustituir a un módulo), y ningún .pyc se reutiliza: pycache_prefix apunta debajo de un archivo regular, ruta que no
# puede existir como directorio. El gate solo ejecuta del repositorio los bytes que verificó contra E (DH-B13).
_REPO = os.path.normcase(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..')))
sys.path[:] = [p for p in sys.path if not (os.path.normcase(os.path.abspath(p or os.curdir)) + os.sep).startswith(
    _REPO + os.sep)]
sys.dont_write_bytecode = True
sys.pycache_prefix = os.path.join(os.path.abspath(__file__), 'sin-pyc')

import ast  # noqa: E402
import copy  # noqa: E402
import hashlib  # noqa: E402
import importlib.machinery  # noqa: E402
import importlib.util  # noqa: E402
import json  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
import unicodedata  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))

E = '61f94e23fc30b00a848a4558830b6d65f81dff87'          # commit E: cierre endurecido de F35-SBX-A
B0_CLOSE = 'cc634eb9dcc5c0cc0d77b911bb3815182b8319c2'   # cierre auditado de B0
B_BASE = '430f3f544c3542cabac8028a122c8a0c2a97390b'     # develop al iniciar F35-SBX-B (B0 integrada)
B_BRANCH = 'feature/f35-sbx-b-deterministic-pipeline'
BRANCHES = (B_BRANCH, 'develop', 'main')

A_PATHS = ('docs/academico/evidencia-sbx', 'docs/academico/tools/f35sbx',
           'docs/academico/tools/f30/validate_f30.py', 'docs/academico/tools/f33/validate_f33.py',
           'docs/academico/tools/f34/validate_f34.py', 'docs/academico/tools/f34b/validate_f34b.py',
           'docs/academico/tools/f34e/validate_f34e.py')
A_COUNT = 22
B0_DOC = 'docs/academico/evidencia-sbx-b/F35SBXB_B0_Sucesion_de_Gates.md'
B_DIRS = ('docs/academico/evidencia-sbx-b', 'docs/academico/tools/f35sbxb')
PYCACHE_OK = ('docs/academico/tools/f35sbx/__pycache__', 'docs/academico/tools/f35sbxb/__pycache__')
GATE = 'docs/academico/tools/f35sbxb/validate_f35sbxb.py'
# Superficies reales que se recorren en el sistema de archivos (M03): todo archivo debe estar en el árbol de HEAD.
RUNTIME_SURFACES = ('app', 'routes', 'database', 'config', 'resources', 'bootstrap', 'public', 'lang', 'tests',
                    'cypress', 'docker', '.github', 'ml-service/src', 'ml-service/tests', 'ml-service/pyproject.toml',
                    'artisan', 'composer.json', 'composer.lock', 'package.json', 'package-lock.json',
                    'docker-compose.yml', '.dockerignore', 'phpunit.xml', 'vite.config.ts',
                    'docs/academico/datos-sinteticos', 'docs/academico/g0-sandbox', 'docs/academico/g0-evidence')
# B1.3 — METADATA != CÓDIGO EJECUTABLE. Todo código ejecutable o importable de estas superficies debe ser (A) idéntico,
# byte a byte, a su blob en la base autorizada B_BASE, o (B) derivable y verificable (un .pyc cuyo código coincide con
# el que compile() produce desde su fuente hermana, con la etiqueta del intérprete actual). Lo demás queda (C) fuera
# del conjunto permitido durante B1: bundles de Vite (aunque un manifiesto los nombre), TypeScript de Wayfinder y la
# caché PHP de Laravel no están versionados ni pueden derivarse sin ejecutar un build, así que FSY no los certifica
# por su nombre ni por su extensión y falla cerrado. Solo quedan como excepciones directorios de metadatos que nada
# ejecuta ni importa, con un patrón estrecho de ruta y extensión.
RT_EXCEPTIONS = {
    'cypress/results': re.compile(r'[A-Za-z0-9_.-]+\.(json|log)'),                                # Cypress
    'ml-service/src/recruitment_ml.egg-info': re.compile(                                          # pip -e
        r'(PKG-INFO|SOURCES\.txt|dependency_links\.txt|top_level\.txt|requires\.txt)'),
}
RT_SKIP_DIRS = frozenset(RT_EXCEPTIONS)
RT_GENERATED = ('public/build/', 'public/hot', 'resources/js/actions/', 'resources/js/routes/',
                'resources/js/wayfinder/', 'bootstrap/cache/')   # generados por builds: sin origen verificable en B1
RT_PYCACHE_ROOTS = ('ml-service/src/', 'ml-service/tests/')        # __pycache__ con .pyc derivables y verificados
PYC_RX = re.compile(r'([A-Za-z_][A-Za-z0-9_]*)\.([A-Za-z0-9_-]+?)(?:\.opt-([12]))?\.pyc')
# Alcance exacto de B1 respecto de B_BASE: ruta -> estado esperado. Todas obligatorias.
SCOPE = {
    'CLAUDE.md': 'M',
    'docs/PROGRESS.md': 'M',
    'docs/academico/evidencia-sbx-b/README.md': 'M',
    'docs/academico/evidencia-sbx-b/F35SBXB_B1_Gate_Sucesor.md': 'A',
    GATE: 'A',
}
# Archivos reales que deben existir, exactamente, en las carpetas de B.
B_FILES = frozenset({'docs/academico/evidencia-sbx-b/README.md', B0_DOC,
                     'docs/academico/evidencia-sbx-b/F35SBXB_B1_Gate_Sucesor.md', GATE})
GOVERNANCE = ('CLAUDE.md', 'docs/PROGRESS.md')
STATES = ['- G0 real = NO APROBADA', '- G0-09 = CUMPLIDO', '- G0-14 = CUMPLIDO', '- G0-02 = PENDIENTE EXTERNO',
          '- G0-03 = PENDIENTE EXTERNO', '- G0-12 = PENDIENTE EXTERNO', '- ADR-005 = PROPUESTA',
          '- G0-SBX = APROBADA CON RESTRICCIONES', '- F35 productiva = BLOQUEADA', '- F35-SBX = HABILITADA',
          '- F36–F40 = BLOQUEADAS', '- Alcance C = BLOQUEADO', '- Datos reales = PROHIBIDOS']
B_STATE_RX = re.compile(r'F35-SBX-B\s+(NO\s+INICIADA|[A-ZÁÉÍÓÚÑ]{2,})')
UNLOCK = [re.compile(p) for p in (
    r'\bG0 real\s*[=:]?\s*APROBADA', r'\bG0 real\s+(HABILITAD|DESBLOQUEAD)',
    r'\bADR-005\s*[=:]?\s*(APROBAD|ACEPTAD)',
    r'\bF35 productiva\s*[=:]?\s*(HABILITAD|INICIAD|DESBLOQUEAD|APROBAD)',
    r'\b(F3[6-9]|F40)\b[^.;\n]{0,40}?\b(HABILITAD|INICIAD|DESBLOQUEAD|AUTORIZAD)',
    r'\b(Alcance|Scope) C\s*[=:]?\s*(HABILITAD|DESBLOQUEAD|APROBAD)',
    r'\b[Dd]atos reales\s*[=:]?\s*(PERMITID|AUTORIZAD|HABILITAD)')]
SBX_MODULES = ('docs/academico/tools/f34e/validate_f34e.py', 'docs/academico/tools/f34/validate_f34.py',
               'docs/academico/tools/f34a/validate_f34a.py', 'docs/academico/tools/f34b/validate_f34b.py')
SBX_IDS = [f'SBX-{i:02d}' for i in range(1, 19)]
SBX_INFO = {   # ID: (fuente, comprobación aplicada), según la matriz de criterios de F34E
    'SBX-01': ('Dataset F34, validate_f34.py', 'DQ-05..DQ-07 sin violaciones y manifiesto source = synthetic'),
    'SBX-02': ('validate_f34.py', 'PII-01..PII-03 sin violaciones'),
    'SBX-03': ('Árbol de archivos, F34', 'Solo CSV, JSON o Markdown en datos-sinteticos/ y g0-sandbox/; DQ-04'),
    'SBX-04': ('Árbol de archivos', 'Ningún audio ni vídeo en datos-sinteticos/ ni g0-sandbox/'),
    'SBX-05': ('schema.json, F34', 'Sin campos de score, ranking ni selección; LK-01 y LK-08'),
    'SBX-06': ('schema.json', 'Sin campos de recomendación'),
    'SBX-07': ('schema.json, matriz de trazabilidad', 'Sin selección ni contratación; RF-23 humana'),
    'SBX-08': ('traceability-master.md, Git', 'Fila RF-23 «humana» y baseline sin cambios'),
    'SBX-09': ('Matriz de trazabilidad, validate_f34a.py', 'Fila RF-21 sin cambios y regla RANK'),
    'SBX-10': ('F34, schema.json', 'CTX-01..CTX-10 y organization_token'),
    'SBX-11': ('schema.json, F34', 'provenance en evidence y DQ-07'),
    'SBX-12': ('Registros F34C, validate_f34b.py', 'G0-09 derivado CUMPLIDO'),
    'SBX-13': ('validate_f34b.py, ADR-005', 'G0-14 CUMPLIDO y ADR-005 canónico PROPUESTA'),
    'SBX-14': ('F34, manifest.json', 'source_type = synthetic, [SINTÉTICO] y advertencia del manifiesto'),
    'SBX-15': ('Recorrido del runtime', 'Ningún archivo del runtime referencia los datos sintéticos ni G0-SBX'),
    'SBX-16': ('Git', 'Runtime, dependencias, migraciones y baseline sin cambios frente a la base fija'),
    'SBX-17': ('F34B_Decision_G0.md', 'Alcance C no habilitado'),
    'SBX-18': ('F34B_Decision_G0.md, validate_f34b.py', 'G0 = NO APROBADA y G0-02/03/12 sin cerrar'),
}
# B1.3 — directorios que validate_f34e.py y sus módulos ponen en sys.path: su contenido debe ser exactamente el de E,
# con los mismos bytes, más un __pycache__ opcional que el gate no usa y cuyos .pyc deben ser derivables de su fuente;
# así también generate_synthetic.py, que validate_f34.py importa, queda verificado antes de ejecutar nada.
SBX_DIRS = ('docs/academico/tools/f34', 'docs/academico/tools/f34a', 'docs/academico/tools/f34b',
            'docs/academico/tools/f34e')
# B1.4 — inventario cerrado de todo el código del repositorio que compute_sbx() puede ejecutar, directa o
# transitivamente, con su referencia autorizada: E para los validadores congelados de A y sus dependencias, y la base
# de B para el runtime que B no puede modificar. El grafo se recalcula por AST, sin importar nada, y debe coincidir
# exactamente con este inventario; los bytes reales deben ser los del blob autorizado antes de ejecutar cualquiera.
EXEC_ENTRY = SBX_MODULES[0]
EXEC_INVENTORY = {
    'docs/academico/tools/f34e/validate_f34e.py': E,
    'docs/academico/tools/f34/validate_f34.py': E,
    'docs/academico/tools/f34/generate_synthetic.py': E,
    'docs/academico/tools/f34a/validate_f34a.py': E,
    'docs/academico/tools/f34b/validate_f34b.py': E,
    'docs/academico/tools/f35sbx/f35sbx_scope.py': E,
    'ml-service/src/recruitment_ml/schema.py': B_BASE,
}
PATH_FUNCS = ('os.path.join', 'os.path.dirname', 'os.path.abspath', 'os.path.normpath', 'os.path.realpath')
DYNAMIC_CALLS = ('exec', 'eval', 'compile', '__import__', 'execfile', 'breakpoint')
DYNAMIC_ATTRS = ('import_module', 'run_path', 'run_module', 'system', 'popen', 'startfile', 'execv', 'execve',
                 'execl', 'execlp', 'execvp', 'spawnv', 'spawnve', 'spawnl', 'load_source', 'load_compiled',
                 'load_dynamic', 'SourceFileLoader', 'SourcelessFileLoader', 'ExtensionFileLoader')
# Variables que alteran qué código carga el intérprete al arrancar un script (PYTHONSTARTUP solo afecta al modo
# interactivo y no se considera).
ENV_VARS = ('PYTHONPATH', 'PYTHONHOME', 'PYTHONUSERBASE')
STDLIB_OK = {'ast', 'copy', 'hashlib', 'importlib', 'json', 'os', 're', 'subprocess', 'sys', 'unicodedata'}
PII = [re.compile(p) for p in (
    r'[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}',                          # correo
    r'\bDNI\b\D{0,10}\d{8}(?![0-9A-Za-z])',                                    # DNI
    r'(?<![0-9A-Za-z])(\+?51[\s-]?)?9\d{2}[\s-]?\d{3}[\s-]?\d{3}(?![0-9A-Za-z])',  # celular
    r'(?<![0-9A-Za-z])(10|20)\d{9}(?![0-9A-Za-z])')]                           # RUC
JSON_KEY_RX = re.compile(r'score|rank|recommend|recomend|best|mejor|select|selecci|hire|contrat|ocr|pars|extract|'
                         r'extracc|embedding|vector|semantic|semántic|llm', re.I)
MAX_BYTES = 1_000_000


class GitError(Exception):
    pass


def git(*args):
    try:
        p = subprocess.run(['git', *args], cwd=ROOT, capture_output=True)
    except OSError:
        return None, b''
    return p.returncode, p.stdout


def blob_id(data):
    return hashlib.sha1(b'blob %d\x00' % len(data) + data).hexdigest()


def real_bytes(rel):
    """Bytes reales de un archivo regular; enlaces, otros tipos y errores de lectura → None (falla cerrado)."""
    full = os.path.join(ROOT, rel)
    if os.path.islink(full) or not os.path.isfile(full):
        return None
    try:
        with open(full, 'rb') as f:
            return f.read()
    except OSError:
        return None


def walk(roots, skip_dirs=frozenset(), skip_files=frozenset(), pycache_roots=()):
    """Archivos reales bajo las rutas, sin seguir enlaces y con archivos ocultos. Solo se omiten los __pycache__
    autorizados (con archivos regulares .pyc directos) y las excepciones explícitas. (conjunto de rutas, problemas)."""
    found, problems = set(), []

    def visit(rel):
        full = os.path.join(ROOT, rel)
        try:
            with os.scandir(full) as entries:
                for entry in entries:
                    sub = f'{rel}/{entry.name}'
                    if entry.is_symlink():
                        problems.append(f'enlace en una ruta protegida: {sub}')
                    elif entry.is_dir(follow_symlinks=False) and sub in skip_dirs:
                        continue
                    elif entry.is_dir(follow_symlinks=False):
                        if sub in PYCACHE_OK or (entry.name == '__pycache__' and sub.startswith(pycache_roots)):
                            bad = []
                            for e in os.scandir(entry.path):
                                if e.name.endswith('.pyc') and not e.is_symlink() and e.is_file(follow_symlinks=False):
                                    problem = pyc_problem(f'{sub}/{e.name}')
                                    if problem:
                                        problems.append(problem)
                                else:
                                    bad.append(e.name)
                            if bad:
                                problems.append(f'entradas no permitidas en {sub}: {sorted(bad)[:3]}')
                        else:
                            visit(sub)
                    elif entry.is_file(follow_symlinks=False):
                        if sub not in skip_files:
                            found.add(sub)
                    else:
                        problems.append(f'objeto especial en una ruta protegida: {sub}')
        except OSError as e:
            problems.append(f'{rel} ilegible ({e.__class__.__name__}): falla cerrado')

    for rel in roots:
        full = os.path.join(ROOT, rel)
        if os.path.islink(full):
            problems.append(f'ruta protegida convertida en enlace: {rel}')
        elif os.path.isdir(full):
            visit(rel)
        elif os.path.lexists(full):
            found.add(rel)
    return found, problems


def load_pyc(path, name):
    return importlib.machinery.SourcelessFileLoader(name, path).get_code(name)


def pyc_problem(rel, load=load_pyc):
    """B1.3 — un .pyc solo se admite si es derivable y verificable: etiqueta del intérprete que ejecuta el gate,
    fuente hermana real y código idéntico al que compile() produce desde esa fuente. Lo demás (otra versión de
    Python, .pyc reescrito por pytest, sin fuente o distinto) no se certifica y falla cerrado."""
    folder, name = rel.rsplit('/', 1)
    m = PYC_RX.fullmatch(name)
    if not m or m.group(2) != sys.implementation.cache_tag:
        return (f'{rel}: .pyc no derivable con este intérprete ({sys.implementation.cache_tag}) o generado por otra '
                f'herramienta: no se certifica (falla cerrado)')
    src_rel = f'{folder.rsplit("/", 1)[0]}/{m.group(1)}.py'
    src = real_bytes(src_rel)
    if src is None:
        return f'{rel}: sin fuente hermana {src_rel}: no se certifica (falla cerrado)'
    try:
        loaded = load(os.path.join(ROOT, rel), m.group(1))
        built = compile(src, os.path.join(ROOT, src_rel), 'exec', dont_inherit=True, optimize=int(m.group(3) or 0))
    except Exception as e:          # cabecera, marshal o fuente inválidos: no verificable
        return f'{rel}: .pyc o fuente no verificable ({e.__class__.__name__}): falla cerrado'
    return None if loaded == built else f'{rel}: no corresponde a {src_rel}: no se certifica (falla cerrado)'


def exception_problems(reader=real_bytes):
    """Contenido de las excepciones de FSY (solo metadatos): patrón de ruta y tipo de cada archivo, sin enlaces."""
    out = []
    for rel, rx in sorted(RT_EXCEPTIONS.items()):
        full = os.path.join(ROOT, rel)
        if os.path.islink(full):
            out.append(f'excepción convertida en enlace: {rel}')
            continue
        if not os.path.lexists(full):
            continue
        if not os.path.isdir(full):
            out.append(f'excepción que no es un directorio: {rel}')
            continue
        for d, dirs, files in os.walk(full):
            for name in dirs + files:
                p = os.path.join(d, name)
                sub = os.path.relpath(p, full).replace(os.sep, '/')
                if os.path.islink(p):
                    out.append(f'enlace dentro de una excepción: {rel}/{sub}')
                elif name in files and not (os.path.isfile(p) and rx.fullmatch(sub)):
                    out.append(f'archivo no autorizado dentro de la excepción {rel}: {sub}')
            dirs[:] = [x for x in dirs if not os.path.islink(os.path.join(d, x))]
    return out


def name_status(data):
    parts = data.split(b'\x00')
    return {(parts[i].decode(), parts[i + 1].decode('utf-8', 'replace')) for i in range(0, len(parts) - 1, 2)
            if parts[i]}


def _norm_rel(path):
    """Ruta relativa al repositorio, normalizada sin tocar el sistema de archivos ('..' inicial = fuera del repo)."""
    parts = []
    for p in path.replace('\\', '/').split('/'):
        if p in ('', '.'):
            continue
        if p == '..' and parts and parts[-1] != '..':
            parts.pop()
        else:
            parts.append(p)
    return '/'.join(parts) or '.'


def _dotted(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _dotted(node.value)
        return f'{base}.{node.attr}' if base else None
    return None


def _eval_path(node, env):
    """Evalúa estáticamente una expresión de ruta: literales, nombres de módulo ya resueltos y os.path.*. None si no
    es resoluble (y entonces la carga falla cerrada)."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.Name):
        return env.get(node.id)
    if isinstance(node, ast.Call) and _dotted(node.func) in PATH_FUNCS and node.args and not node.keywords:
        args = [_eval_path(a, env) for a in node.args]
        if None in args:
            return None
        name = _dotted(node.func)
        if name == 'os.path.join':
            return _norm_rel('/'.join(args))
        if name == 'os.path.dirname':
            return _norm_rel(args[0].rsplit('/', 1)[0] if '/' in _norm_rel(args[0]) else '.')
        return _norm_rel(args[0])
    return None


def scan_module(rel, tree):
    """Análisis estático de un módulo del inventario (sin importarlo): cargas de código por ruta, rutas añadidas a
    sys.path, nombres importados y construcciones de ejecución dinámica no verificables."""
    env = {'__file__': rel}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            value = _eval_path(node.value, env)
            if value is not None:
                env[node.targets[0].id] = value
    loads, dirs, imports, problems = set(), set(), set(), []
    loaders = {}     # función propia que carga por ruta: nombre -> (índice del parámetro, añade su directorio)
    for fn in [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]:
        params = [a.arg for a in fn.args.args]
        for call in [n for n in ast.walk(fn) if isinstance(n, ast.Call)]:
            name = _dotted(call.func) or ''
            if name.endswith('spec_from_file_location') and len(call.args) > 1 and \
                    isinstance(call.args[1], ast.Name) and call.args[1].id in params:
                loaders[fn.name] = (params.index(call.args[1].id), loaders.get(fn.name, (0, False))[1])
        for call in [n for n in ast.walk(fn) if isinstance(n, ast.Call)]:
            name = _dotted(call.func) or ''
            if name in ('sys.path.insert', 'sys.path.append') and fn.name in loaders:
                arg = call.args[-1] if call.args else None
                if isinstance(arg, ast.Call) and _dotted(arg.func) == 'os.path.dirname' and arg.args and \
                        isinstance(arg.args[0], ast.Name) and arg.args[0].id in params:
                    loaders[fn.name] = (loaders[fn.name][0], True)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports |= {a.name.split('.')[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                problems.append(f'{rel}: importación relativa no verificable')
            imports.add((node.module or '').split('.')[0])
        elif isinstance(node, ast.Call):
            name = _dotted(node.func) or ''
            if (isinstance(node.func, ast.Name) and name in DYNAMIC_CALLS) or name.split('.')[-1] in DYNAMIC_ATTRS:
                problems.append(f'{rel}: ejecución dinámica no verificable ({name})')
            elif name.startswith('subprocess.'):
                first = node.args[0] if node.args else None
                if not (isinstance(first, (ast.List, ast.Tuple)) and first.elts and isinstance(first.elts[0], ast.Constant)
                        and first.elts[0].value == 'git'):
                    problems.append(f'{rel}: subproceso distinto de git ({name})')
            elif name.endswith('spec_from_file_location'):
                arg = node.args[1] if len(node.args) > 1 else None
                if isinstance(arg, ast.Name) and any(arg.id in [a.arg for a in fn.args.args]
                                                      for fn in ast.walk(tree) if isinstance(fn, ast.FunctionDef)
                                                      and fn.name in loaders):
                    continue
                target = _eval_path(arg, env) if arg is not None else None
                if target is None:
                    problems.append(f'{rel}: carga de código por una ruta no resoluble estáticamente')
                else:
                    loads.add(target)
            elif isinstance(node.func, ast.Name) and name in loaders:
                index, adds_dir = loaders[name]
                target = _eval_path(node.args[index], env) if len(node.args) > index else None
                if target is None:
                    problems.append(f'{rel}: carga de código por una ruta no resoluble estáticamente ({name})')
                else:
                    loads.add(target)
                    if adds_dir:
                        dirs.add(_eval_path(ast.Call(func=ast.parse('os.path.dirname', mode='eval').body,
                                                     args=[ast.Constant(target)], keywords=[]), env))
            elif name in ('sys.path.insert', 'sys.path.append'):
                arg = node.args[-1] if node.args else None
                target = _eval_path(arg, env) if arg is not None else None
                if target is not None:
                    dirs.add(target)
                elif not any(n is node for fn in ast.walk(tree) if isinstance(fn, ast.FunctionDef) and fn.name in loaders
                             and loaders[fn.name][1] for n in ast.walk(fn)):
                    problems.append(f'{rel}: ruta añadida a sys.path no resoluble estáticamente')
    imports.discard('')
    return loads, dirs, imports, problems


def exec_graph(sources, exists=os.path.lexists):
    """B1.4 — grafo del código del repositorio que ejecutaría compute_sbx(), calculado por AST sobre bytes ya
    verificados (sin importar nada). Un nombre importado que existe como módulo del repositorio en un directorio de
    sys.path debe estar en el inventario; si no, o si una carga no es resoluble, falla cerrado. (cierre, problemas)."""
    seen, todo, dirs, imports, problems = set(), [EXEC_ENTRY], set(), set(), []
    while True:
        while todo:
            rel = todo.pop()
            if rel in seen:
                continue
            seen.add(rel)
            if rel not in sources:
                problems.append(f'código del repositorio fuera del inventario verificado: {rel}')
                continue
            try:
                tree = ast.parse(sources[rel].decode('utf-8'), filename=rel)
            except (SyntaxError, ValueError) as e:
                problems.append(f'{rel}: no analizable ({e.__class__.__name__})')
                continue
            loads, more_dirs, names, found = scan_module(rel, tree)
            problems += found
            dirs |= more_dirs
            imports |= names
            for target in loads:
                if target.startswith('..') or not target.endswith('.py'):
                    problems.append(f'{rel}: carga de código fuera del repositorio o que no es fuente: {target}')
                else:
                    todo.append(target)
        for d in sorted(dirs):
            if d.startswith('..'):
                problems.append(f'ruta de importación fuera del repositorio: {d}')
                continue
            for name in sorted(imports):
                for cand in (f'{d}/{name}.py', f'{d}/{name}.pyc', f'{d}/{name}.pyw', f'{d}/{name}.pyd', f'{d}/{name}.so',
                             f'{d}/{name}'):
                    if exists(os.path.join(ROOT, cand)):
                        if cand in sources and cand not in seen:
                            todo.append(cand)
                        elif cand not in sources:
                            problems.append(f'{cand}: módulo del repositorio importable por compute_sbx() y fuera del '
                                            f'inventario verificado (falla cerrado)')
        if not todo:
            break
    if not problems and seen != set(EXEC_INVENTORY):
        problems.append(f'el grafo estático no coincide con el inventario: {sorted(seen ^ set(EXEC_INVENTORY))}')
    return seen, sorted(set(problems))


def _no_link(rel):
    """Ningún componente de la ruta es un enlace."""
    parts = rel.split('/')
    return not any(os.path.islink(os.path.join(ROOT, *parts[:k])) for k in range(1, len(parts) + 1))


def verify_inventory(must, reader=real_bytes):
    """B1.4 — bytes reales de cada archivo del inventario idénticos a su blob en la referencia autorizada, como archivo
    regular 100644 y sin enlaces en la ruta. ({ruta: bytes verificados}, error)."""
    verified = {}
    for rel, ref in EXEC_INVENTORY.items():
        meta = must('ls-tree', ref, '--', rel).decode().split('\t')[0].split()
        data = reader(rel) if _no_link(rel) else None
        if len(meta) != 3 or meta[:2] != ['100644', 'blob'] or data is None or blob_id(data) != meta[2]:
            return None, f'{rel}: distinto de su blob autorizado en {ref[:7]}; no se ejecuta (falla cerrado)'
        verified[rel] = data
    return verified, None


def repo_key(path):
    return os.path.normcase(os.path.abspath(path))


def in_repo(path):
    key = repo_key(path)
    return key == _REPO or key.startswith(_REPO + os.sep)


def repo_modules(skip=()):
    """Módulos ya cargados cuyo origen está en el repositorio (salvo el propio gate)."""
    out = []
    for name, mod in list(sys.modules.items()):
        if mod is None or any(mod is x for x in skip):
            continue
        spec = getattr(mod, '__spec__', None)
        locs = [getattr(mod, '__file__', None), getattr(spec, 'origin', None)]
        locs += list(getattr(spec, 'submodule_search_locations', None) or [])
        if any(isinstance(p, str) and os.path.isabs(p) and in_repo(p) for p in locs):
            out.append(name)
    return sorted(out)


class ExecGuard:
    """B1.4 — mientras corre compute_sbx(), el código del repositorio solo se carga desde los bytes ya verificados
    (sin releer el archivo: sin ventana entre verificación y ejecución) y cualquier otro código del repositorio
    (fuente, .pyc sin fuente, extensión nativa o paquete) se rechaza antes de ejecutarse. Restaura todo al salir."""

    def __init__(self, verified):
        self.verified = {repo_key(os.path.join(ROOT, rel)): data for rel, data in verified.items()}
        self.refused = []

    def find_spec(self, name, path=None, target=None):
        spec = importlib.machinery.PathFinder.find_spec(name, path, target)
        if spec is None:
            return None
        locs = ([spec.origin] if spec.origin else []) + list(spec.submodule_search_locations or [])
        if not any(os.path.isabs(p) and in_repo(p) for p in locs):
            return None
        if spec.origin and repo_key(spec.origin) in self.verified and spec.submodule_search_locations is None \
                and type(spec.loader) is importlib.machinery.SourceFileLoader:
            return spec
        self.refused.append(f'módulo {name} ({spec.origin or "paquete"})')
        raise ImportError(f'{name}: código del repositorio no verificado; no se ejecuta')

    def __enter__(self):
        guard = self
        self.saved_path, self.saved_modules = list(sys.path), set(sys.modules)
        SFL, SLL, EFL = (importlib.machinery.SourceFileLoader, importlib.machinery.SourcelessFileLoader,
                         importlib.machinery.ExtensionFileLoader)
        self.patched = [(SFL, 'get_data', SFL.__dict__.get('get_data')), (SLL, 'get_data', SLL.__dict__.get('get_data')),
                        (EFL, 'create_module', EFL.__dict__.get('create_module'))]
        source_get, sourceless_get, ext_create = SFL.get_data, SLL.get_data, EFL.create_module

        def get_source(loader, path):
            if not in_repo(path):
                return source_get(loader, path)
            if repo_key(path) != repo_key(loader.path):
                raise OSError('bytecode del repositorio: no se reutiliza')
            if repo_key(path) in guard.verified:
                return guard.verified[repo_key(path)]
            guard.refused.append(f'fuente {path}')
            raise ImportError(f'{path}: código del repositorio no verificado; no se ejecuta')

        def get_sourceless(loader, path):
            if in_repo(path):
                guard.refused.append(f'bytecode sin fuente {path}')
                raise ImportError(f'{path}: bytecode del repositorio; no se ejecuta')
            return sourceless_get(loader, path)

        def create_extension(loader, spec):
            if in_repo(loader.path):
                guard.refused.append(f'extensión nativa {loader.path}')
                raise ImportError(f'{loader.path}: extensión nativa del repositorio; no se carga')
            return ext_create(loader, spec)
        SFL.get_data, SLL.get_data, EFL.create_module = get_source, get_sourceless, create_extension
        sys.meta_path.insert(0, self)
        importlib.invalidate_caches()
        return self

    def __exit__(self, *exc):
        if self in sys.meta_path:
            sys.meta_path.remove(self)
        for cls, attr, original in self.patched:
            if original is None:
                delattr(cls, attr)
            else:
                setattr(cls, attr, original)
        sys.path[:] = self.saved_path
        for name in set(sys.modules) - self.saved_modules:
            del sys.modules[name]
        importlib.invalidate_caches()
        return False


def sbx_eval(must, reader=real_bytes, lister=os.listdir, exists=os.path.lexists):
    """DH-B13: verificar contra E los bytes de validate_f34e.py y de los módulos que carga, y (B1.3) el contenido
    completo de los directorios que esos módulos ponen en sys.path; solo entonces ejecutar compute_sbx() con los bytes
    verificados. (resultados, error)."""
    try:
        for folder in SBX_DIRS:
            tree = {}
            for entry in must('ls-tree', '-z', f'{E}:{folder}').split(b'\x00'):
                if entry:
                    meta, _, name = entry.partition(b'\t')
                    tree[name.decode()] = tuple(meta.decode().split())
            full = os.path.join(ROOT, folder)
            if os.path.islink(full) or not os.path.isdir(full):
                return None, f'{folder}: no es un directorio real; no se importa (falla cerrado)'
            names = set(lister(full))
            pycache = os.path.join(full, '__pycache__')
            if '__pycache__' in names:
                if os.path.islink(pycache) or not os.path.isdir(pycache):
                    return None, f'{folder}/__pycache__: no es un directorio real; no se importa (falla cerrado)'
                for name in sorted(os.listdir(pycache)):     # el gate no los usa, pero tampoco los certifica sin verificar
                    p = os.path.join(pycache, name)
                    problem = (pyc_problem(f'{folder}/__pycache__/{name}') if name.endswith('.pyc') and not
                               os.path.islink(p) and os.path.isfile(p) else f'{folder}/__pycache__/{name}: no es un .pyc regular')
                    if problem:
                        return None, f'{problem}; no se importa'
            extra = sorted(names - set(tree) - {'__pycache__'})
            if extra:
                return None, f'{folder}: entradas ajenas a E en una ruta de importación {extra[:3]}; no se importa (falla cerrado)'
            for name, meta in tree.items():
                data = reader(f'{folder}/{name}')
                if meta[:2] != ('100644', 'blob') or data is None or blob_id(data) != meta[2]:
                    return None, f'{folder}/{name}: distinto de su blob en E; no se importa (falla cerrado)'
        verified, err = verify_inventory(must, reader)
        if err:
            return None, err.replace('no se ejecuta', 'no se importa ni se ejecuta')
        _, problems = exec_graph(verified, exists)
        if problems:
            return None, f'grafo de código no verificable; no se importa ni se ejecuta: {problems[:3]}'
        foreign = repo_modules(skip=(sys.modules.get(__name__),))
        if foreign:
            return None, f'módulos del repositorio ya cargados {foreign[:3]}; no se importa ni se ejecuta (falla cerrado)'
        path = os.path.join(ROOT, EXEC_ENTRY)
        with ExecGuard(verified) as guard:
            spec = importlib.util.spec_from_file_location('f35sbxb_validate_f34e', path)
            module = importlib.util.module_from_spec(spec)
            exec(compile(verified[EXEC_ENTRY], path, 'exec', dont_inherit=True), module.__dict__)
            results = module.compute_sbx()[0]
        if guard.refused:
            return None, f'código del repositorio no verificado rechazado durante compute_sbx(): {guard.refused[:3]}; no se importa (falla cerrado)'
        return {k: (v[0] is True, v[1]) for k, v in results.items()}, None
    except Exception as e:          # cualquier fallo de evaluación deja los criterios como no evaluables
        return None, f'compute_sbx() no evaluable ({e.__class__.__name__}: {e}): falla cerrado'


def a_history(must):
    """Commits de E..HEAD que tocan F35-SBX-A, con la historia completa (rev-list sin filtrar por rutas) y cada
    commit comparado con cada padre: un commit normal la toca si cambia contenido, modo, altas o bajas (sin
    detección de renombrados); un merge, si su versión difiere de la de todos sus padres. Un cambio revertido después
    sigue siendo su propio commit. [(commit, rutas)]."""
    touching = []
    for line in must('rev-list', '--parents', f'{E}..HEAD').decode().splitlines():
        ids = line.split()
        if len(ids) < 2 or not all(re.fullmatch(r'[0-9a-f]{40}', x) for x in ids):
            raise GitError('commit sin padres o no verificable en E..HEAD')
        commit, parents = ids[0], ids[1:]
        diffs = [{x for x in must('diff-tree', '-r', '--no-renames', '--name-only', '-z', p, commit, '--', *A_PATHS)
                  .decode('utf-8', 'replace').split('\x00') if x} for p in parents]
        touched = set.intersection(*diffs)
        if touched:
            touching.append((commit, sorted(touched)))
    return touching


def collect(runner=git, reader=real_bytes):
    """Estado real de HEAD. Cualquier error de Git queda en S['errors'] y hace fallar CTX."""
    S = {'errors': [], 'env': [f'el gate debe ejecutarse aislado (python -I): falla cerrado'] * (not sys.flags.isolated)
         + [f'variable de entorno {v} definida: entorno de Python no verificable (falla cerrado)'
            for v in ENV_VARS if os.environ.get(v)]}

    def must(*args):
        rc, out = runner(*args)
        if rc != 0:
            raise GitError(f'git {" ".join(args[:3])} → {rc}')
        return out
    try:
        S['inside'] = must('rev-parse', '--is-inside-work-tree').strip() == b'true'
        S['branch'] = must('branch', '--show-current').decode().strip()
        S['head'] = must('rev-parse', '--verify', 'HEAD^{commit}').decode().strip()
        S['ancestors'] = {}
        for name, commit in (('E', E), ('B0', B0_CLOSE), ('base de B', B_BASE)):
            rc, _ = runner('merge-base', '--is-ancestor', commit, 'HEAD')
            if rc not in (0, 1):
                raise GitError(f'merge-base {name} → {rc}')
            S['ancestors'][name] = rc == 0
        S['flags'] = [x.decode('utf-8', 'replace') for x in must('ls-files', '-v', '-z').split(b'\x00')
                      if x and not x.startswith(b'H ')]
        expected = {}
        for entry in must('ls-tree', '-r', '-z', '--full-tree', E, '--', *A_PATHS).split(b'\x00'):
            if entry:
                meta, _, path = entry.partition(b'\t')
                expected[path.decode()] = tuple(meta.decode().split())
        S['a_expected'] = expected
        S['a_real'] = {p: (None if (d := reader(p)) is None else blob_id(d)) for p in expected}
        S['a_fs'], S['a_walk'] = walk(A_PATHS)
        S['shallow'] = must('rev-parse', '--is-shallow-repository').strip() != b'false'
        S['a_history'] = a_history(must)
        S['rt_tracked'] = {x for x in must('ls-tree', '-r', '--name-only', '-z', 'HEAD', '--', *RUNTIME_SURFACES)
                           .decode('utf-8', 'replace').split('\x00') if x}
        S['rt_base'] = {}
        for entry in must('ls-tree', '-r', '-z', B_BASE, '--', *RUNTIME_SURFACES).split(b'\x00'):
            if entry:
                meta, _, path = entry.partition(b'\t')
                S['rt_base'][path.decode('utf-8', 'replace')] = tuple(meta.decode().split())
        S['rt_fs'], S['rt_walk'] = walk(RUNTIME_SURFACES, RT_SKIP_DIRS, frozenset(), RT_PYCACHE_ROOTS)
        S['rt_real'] = {p: (None if (d := reader(p)) is None else blob_id(d)) for p in sorted(S['rt_fs'] & set(S['rt_base']))}
        S['rt_exc'] = exception_problems(reader)
        S['a_head_diff'] = [x for x in must('diff', '--name-only', '-z', E, 'HEAD', '--', *A_PATHS).decode().split('\x00') if x]
        S['b0_blob'] = must('rev-parse', f'{B0_CLOSE}:{B0_DOC}').decode().strip()
        S['b0_real'] = None if (d := reader(B0_DOC)) is None else blob_id(d)
        S['delta'] = {
            'HEAD': name_status(must('diff', '--name-status', '--no-renames', '-z', B_BASE, 'HEAD')),
            'árbol': name_status(must('diff', '--name-status', '--no-renames', '-z', B_BASE)),
            'índice': name_status(must('diff', '--cached', '--name-status', '--no-renames', '-z', B_BASE)),
        }
        S['untracked'] = {x for x in must('ls-files', '--others', '--exclude-standard', '-z').decode().split('\x00') if x}
        S['b_fs'], S['b_walk'] = walk(B_DIRS)
        S['links'] = sorted(p for p in set(SCOPE) | B_FILES if os.path.islink(os.path.join(ROOT, p)))
        S['files'] = {p: reader(p) for p in sorted(B_FILES)}
        S['gov'] = {p: reader(p) for p in GOVERNANCE}
        S['gov_base'] = {p: must('show', f'{B_BASE}:{p}') for p in GOVERNANCE}
        S['sbx'], S['sbx_error'] = sbx_eval(must, reader)
    except (GitError, OSError, ValueError) as e:
        S['errors'].append(f'estado Git o de archivos no verificable: {e}')
    return S


# ---------------------------------------------------------------- semántica acotada (CNT y GOV)
# No es un detector lingüístico universal: normaliza (minúsculas, acentos, Markdown básico, guiones), divide en
# oraciones y en segmentos (comas, dos puntos, punto y coma, celdas de tabla y paréntesis) y busca, por familia,
# un término de capacidad y un verbo o estado que la habilite. Ninguno de los dos cuenta si una negación o
# prohibición aparece en las tres palabras anteriores dentro de su segmento. Las citas entre comillas solo se
# descartan cuando la oración que las rodea las rechaza o las presenta como ejemplo; si no, se analizan.
NEG_WORDS = frozenset({'no', 'nunca', 'ni', 'sin', 'jamas', 'tampoco', 'ningun', 'ninguna', 'ninguno', 'nada',
                       'not', 'never', 'without', 'nor', 'none'})
NEG_PREFIXES = ('prohib', 'bloque', 'rechaz', 'imped', 'impid', 'deneg', 'evit', 'detect', 'intent', 'attempt',
                'reject', 'forbid', 'prevent', 'block', 'revoc', 'exclu', 'fall', 'fail')
ENABLE_RX = re.compile(r'^(habilit|permit|implement|activ|autoriz|desbloque|aprob|enable|allow|approv|unlock|'
                       r'incorpor|despleg|deploy|introduc|admit)')
REJECT_CTX_RX = re.compile(r'\b(rechaz\w*|prohib\w*|detect\w*|fall\w*|fail\w*|bloque\w*|ejemplo\w*|negativ\w*|'
                           r'cita\w*|reject\w*|forbid\w*|nunca|no debe\w*)\b')
EXAMPLE_PREFIX_RX = re.compile(r'^(ejemplo negativo|caso negativo|prueba negativa|negativo|negative example|'
                               r'bypass( reproducido| confirmado)?|ataque|attack)\b')
QUOTE_RX = re.compile(r"«[^«»]*»|“[^“”]*”|‘[^‘’]*’|\"[^\"]*\"|(?<![a-z0-9])'[^'\n]*'(?![a-z0-9])")
# B1.2 — acciones inequívocas sobre personas candidatas y estados predicativos automáticos.
PERSON_RX = re.compile(r'^(candidat|postulant|aspirant|ganador|ganadora|apto|apta|aptos|aptas|mejor|mejores|person|'
                       r'applicant|candidate|winner|best|seleccionad|elegid|finalist)')
# B1.4 — objeto de una decisión sobre personas: la persona candidata, «quién» o la plaza.
DECISION_OBJ_RX = re.compile(r'^(quien|quienes|who|whom|plaza|plazas|puesto|vacante|position|job|role)$')
# B1.4 — finalidad decisional de un ordenamiento o una clasificación hecha por el sistema.
PURPOSE_RX = re.compile(r'^(seleccion|selection|decidir|decision|decide|elegir|eleccion|choose|contratar|contratacion|'
                        r'hire|hiring|select|shortlist\w*|preseleccion\w*)$')
AUTO_RX = re.compile(r'^(automatic|automated|autonom)')
PROHIB_RX = re.compile(r'^(prohib|bloque|rechaz|forbid|deneg|vedad|impid|imped|block)')
# B1.3 — las formas verbales se generan por clase de conjugación (presente, pasado, futuro, primera persona del
# plural, condicional, gerundio y participio), no frase por frase. Las formas que coinciden con sustantivos del
# dominio («descarte», «contrato») se excluyen expresamente.
AR = r'(a|an|as|ar|ara|aran|aras|are|aremos|aria|arian|o|e|en|amos|ando|ado|ada|ados|adas|aron)'
AR_NOUNSAFE = r'(a|an|as|ar|ara|aran|aras|are|aremos|aria|arian|amos|ando|ado|ada|ados|adas|aron)'
ER_IR = r'(e|en|es|er|ir|era|eran|ira|iran|eremos|iremos|eria|iria|io|imos|ieron|iendo|ido|ida|idos|idas)'
ACTIONS = [   # (familia, formas verbales explícitas; exige persona candidata; exige «automático»)
    ('scoring', re.compile(r'^(puntu' + AR + r'|scores?|scored)$'), True, False),
    ('scoring', re.compile(r'^((calific|clasific|evalu)' + AR + r'|rates?|rated|grades?|graded|classifie[sd]|'
                           r'evaluates?|evaluated)$'), True, True),
    ('recomendación', re.compile(r'^(recomiend(a|an|as|o|e|en)|recomend' + AR + r'|recommends?|recommended|'
                                 r'recommending|sugier(a|an|e|en|o)|suger' + ER_IR + r'|suggests?|suggested)$'),
     True, False),
    ('mejor candidato', re.compile(r'^(elig(e|en|es|o|io|iendo)|(eleg|escog)' + ER_IR + r'|escoj(a|an|o)|'
                                   r'identific(a|an|ar|ara|aran|aremos|o|amos)|choose|chooses|chose|chosen|'
                                   r'picks?|picked)$'), True, False),
    ('selección automática', re.compile(r'^(seleccion' + AR + r'|(descart|contrat)' + AR_NOUNSAFE +
                                        r'|selects?|selected|hires?|hired)$'), True, False),
    ('selección automática', re.compile(r'^(decid' + ER_IR + r'|determin' + AR + r'|resuelv(e|en|a|an)|resolv' +
                                        ER_IR + r'|decides?|decided|determines?|determined)$'), False, True),
    ('ranking automático', re.compile(r'^(rankea\w*|rank|ranks|ranked|(orden|prioriz|jerarquiz)' + AR +
                                      r'|prioriti[sz]es?|prioriti[sz]ed|ordered|orders|sorts?|sorted|'
                                      r'classifies)$'), True, True),
]
# B1.5 — recomendación implícita: el sistema recomienda o sugiere «quién» continúa, avanza, pasa a la siguiente etapa
# o es seleccionado, aunque no nombre a la persona candidata.
RECOMMEND_RX = next(rx for family, rx, _, _ in ACTIONS if family == 'recomendación')
WHO_RX = re.compile(r'^(quien|quienes|who|whom)$')
PROGRESS_RX = re.compile(r'^(continu\w*|avanz\w*|avanc\w*|pas(a|an|e|en|ar|ara|aran)|seleccionad\w*|elegid\w*|'
                         r'proceed\w*|advance\w*|progress\w*|selected|chosen)$')
CONJUNCTIONS = frozenset({'y', 'e', 'pero', 'mas', 'sino', 'and', 'but'})
# B1.4 — decidir, determinar, elegir o seleccionar con el sistema como agente y una persona, «quién» o la plaza como
# objeto: es una decisión automática aunque no diga «automático» (RF-23).
DECIDE_RX = re.compile(r'^(decid' + ER_IR + r'|determin' + AR + r'|resuelv(e|en|a|an)|elig(e|en|es|o|io|iendo)|'
                       r'(eleg|escog)' + ER_IR + r'|escoj(a|an|o)|seleccion' + AR + r'|decides?|decided|determines?|'
                       r'determined|chooses?|chose|chosen|picks?|picked|selects?|selected)$')
# B1.4 — asignar o calcular notas, calificaciones o puntajes de personas candidatas, por el sistema o automáticamente.
SCORE_VERB_RX = re.compile(r'^((asign|otorg|calcul|comput|atribu|gener|emit)' + AR + r'|assigns?|assigned|gives?|gave|'
                           r'given|computes?|computed|calculates?|calculated|generates?|generated|awards?|awarded)$')
SCORE_NOUN_RX = re.compile(r'^(nota|notas|calificacion|calificaciones|puntuacion|puntuaciones|puntaje|puntajes|score|'
                           r'scores|rating|ratings|grade|grades)$')
# B1.3 — tomar o ejecutar la decisión: verbo de ejecución con la decisión o la selección como objeto directo
# («realizará la selección final», «la decisión final la tomará»), con «automático» o con un agente de sistema.
DECISION_NOUN = r'(seleccion|selecciones|decision|decisiones|contratacion|descarte|eleccion|selection|decision|' \
                r'decisions|hiring|choice)'
OBJ_VERB = r'((tom|adopt|emit|realiz|efectu|ejecut)' + AR + r'|takes?|took|taken|makes?|made|performs?|' \
           r'performed|executes?|executed)'
OBJ_RXS = [re.compile(r'\b(?P<verb>' + OBJ_VERB + r') (?:(?:la|el|las|los|una|un|su|sus|the|a|an|its|their) )?'
                      r'(?:(?:final|definitiva|ultima) )?' + DECISION_NOUN + r'\b'),
           re.compile(r'\b' + DECISION_NOUN + r'(?: (?:final|definitiva))? (?:(?:la|lo|las|los) )?(?P<verb>' +
                      OBJ_VERB + r')\b')]
# Agentes. Un agente de sistema introducido como instrumento («con apoyo del sistema») no es el agente.
SYSTEM_RX = re.compile(r'^(sistema|sistemas|motor|plataforma|algoritmo|algoritmos|modelo|modelos|ia|ai|engine|'
                       r'system|platform|algorithm|model|bot|servicio|service)$')
INSTRUMENTAL = frozenset({'con', 'apoyo', 'ayuda', 'mediante', 'usando', 'utilizando', 'asistido', 'asistida',
                          'with', 'using', 'via', 'support', 'assisted'})
HUMAN_RX = re.compile(r'^(aprobador|aprobadora|aprobadores|direccion|comite|evaluador|evaluadora|evaluadores|'
                      r'reclutador|reclutadora|reclutadores|jurado|approver|approvers|committee|recruiter|recruiters|'
                      r'director|directora|directores)$')
MANUAL_RX = re.compile(r'^(manual|manualmente|manually)$')
STATE_NOUNS = r'(seleccion|decision|contratacion|descarte|eleccion|recomendacion|puntuacion|calificacion|ranking|' \
              r'ordenamiento|selection|decision|hiring|scoring|recommendation)'
COPULAS = r'(sera|seran|es|son|esta|estan|estara|queda|quedan|quedara|pasa a ser|pasara a ser|pasa a|se vuelve|' \
          r'resulta|is|are|will be|becomes)'
PREDICATIVE_RX = re.compile(r'\b' + STATE_NOUNS + r'\b((?: [a-z0-9-]+){0,3}?) ' + COPULAS +
                            r'((?: [a-z0-9-]+){0,2}?) (automatic\w*|automated)\b')


def unprohibited(toks, start, end):
    """Una prohibición no negada en el mismo tramo, después de la acción, la convierte en prohibición."""
    return not any(PROHIB_RX.match(t) and not negated(toks, k) for k, t in enumerate(toks) if k > start)


def system_agent(segs):
    """Agente de sistema no negado y no instrumental en la oración."""
    return any(SYSTEM_RX.match(t) and not negated(toks, i) and not set(toks[max(0, i - 2):i]) & INSTRUMENTAL
               for toks in segs for i, t in enumerate(toks))


def agent_of(segs, s, i):
    """B1.4 — agente de la acción en (s, i): el agente no negado más cercano antes del verbo (sistema no instrumental o
    persona responsable); si no hay, el primero después: un sistema pospuesto («lo decidirá el sistema») o una persona
    introducida por «por» o «by». Devuelve 'system', 'human' o None."""
    agents = []
    for a, toks in enumerate(segs):
        for b, t in enumerate(toks):
            if negated(toks, b):
                continue
            if SYSTEM_RX.match(t) and not set(toks[max(0, b - 2):b]) & INSTRUMENTAL:
                agents.append(((a, b), 'system', True))
            elif HUMAN_RX.match(t):
                agents.append(((a, b), 'human', bool({'por', 'by'} & set(toks[max(0, b - 3):b]))))
    before = [x for x in agents if x[0] < (s, i)]
    if before:
        return before[-1][1]
    after = [x for x in agents if x[0] > (s, i) and (x[1] == 'system' or x[2])]
    return after[0][1] if after else None


def human_exempt(segs, s, i):
    """B1.3/B1.4 — la acción la ejecuta una persona: su agente es una persona responsable (Aprobador, Dirección,
    comité…) o, sin agente, «manualmente» está en su tramo. Nunca exime con «automático» en la oración ni cuando el
    agente es el sistema: «sin intervención humana» o «con confirmación humana» no son agentes."""
    if any(AUTO_RX.match(t) and not negated(toks, b) for toks in segs for b, t in enumerate(toks)):
        return False
    agent = agent_of(segs, s, i)
    if agent == 'human':
        return True
    return agent is None and any(MANUAL_RX.match(t) and not negated(segs[s], b) for b, t in enumerate(segs[s]))


def prohibited_clause(toks, i):
    """B1.5 — la acción está dentro de una subordinada prohibida («está prohibido que el sistema recomiende…»): una
    prohibición no negada seguida de «que» o «that» antes del verbo, sin una conjunción que abra otra cláusula."""
    for j in range(i - 1):
        if PROHIB_RX.match(toks[j]) and not negated(toks, j) and toks[j + 1] in ('que', 'that') \
                and not CONJUNCTIONS & set(toks[j + 2:i]):
            return True
    return False


def action_claims(segs, sentence):
    """Acciones positivas inequívocas: verbo de la familia sobre personas candidatas (o con «automático»), toma o
    ejecución de la decisión por el sistema y estados predicativos («la selección final será automática»), sin
    negación ni prohibición que los alcance y sin un agente humano que ejecute la acción."""
    toks_all = [t for seg in segs for t in seg]
    has_person = any(PERSON_RX.match(t) for t in toks_all)
    has_auto = any(AUTO_RX.match(t) for t in toks_all)
    has_object = has_person or any(DECISION_OBJ_RX.match(t) for t in toks_all)
    has_purpose = any(PURPOSE_RX.match(t) and not negated(toks, i) for toks in segs for i, t in enumerate(toks))
    hits = []

    def live(s, i):
        toks = segs[s]
        return not negated(toks, i) and unprohibited(toks, i, len(toks)) and not human_exempt(segs, s, i)
    positions = [(s, i, t) for s, toks in enumerate(segs) for i, t in enumerate(toks)]
    for family, verb_rx, needs_person, needs_auto in ACTIONS:
        if needs_person and not has_person:
            continue
        # «automático», o (B1.4) el sistema como agente con una finalidad decisional («para la selección»)
        if any(verb_rx.match(t) and live(s, i) and (not needs_auto or has_auto or (
                has_purpose and agent_of(segs, s, i) == 'system')) for s, i, t in positions):
            hits.append(family)
    if has_object and any(DECIDE_RX.match(t) and agent_of(segs, s, i) == 'system' and live(s, i)
                          for s, i, t in positions):
        hits.append('selección automática')
    for k, (s, i, t) in enumerate(positions):
        if RECOMMEND_RX.match(t) and agent_of(segs, s, i) == 'system' and live(s, i) and not prohibited_clause(segs[s], i):
            after = [x[2] for x in positions[k + 1:]]
            who = next((n for n, x in enumerate(after) if WHO_RX.match(x)), None)
            if who is not None and any(PROGRESS_RX.match(x) for x in after[who + 1:]):
                hits.append('recomendación')
                break
    if has_person and any(SCORE_NOUN_RX.match(t) for t in toks_all) and any(
            SCORE_VERB_RX.match(t) and live(s, i) and (has_auto or agent_of(segs, s, i) == 'system')
            for s, i, t in positions):
        hits.append('scoring')
    live_auto = any(AUTO_RX.match(t) and not negated(toks, i) for toks in segs for i, t in enumerate(toks))
    if live_auto or system_agent(segs):
        for s, toks in enumerate(segs):
            joined = ' '.join(toks)
            for rx in OBJ_RXS:
                for m in rx.finditer(joined):
                    at = joined[:m.start('verb')].count(' ')
                    if not negated(toks, at) and unprohibited(toks, at, len(toks)) and not human_exempt(segs, s, at):
                        hits.append('selección automática')
    for toks in segs:
        joined = ' '.join(toks)
        for m in PREDICATIVE_RX.finditer(joined):
            between = (m.group(2) + ' ' + m.group(4)).split()
            at = joined[:m.start()].count(' ')
            if not any(t in NEG_WORDS for t in between) and not negated(toks, at) and unprohibited(toks, at, len(toks)):
                hits.append('selección automática')
    return sorted(set(hits))
# familia: (términos, verbos propios de la familia o None, términos que ya son una acción por sí mismos o None)
FAMILIES = {
    'scoring': (r'\b(scoring|score|scores|puntaje\w*|puntuacion\w*|calificacion automatica)\b',
                r'^(calcul|asign|otorg|comput|puntu|calific)' + AR + r'$',
                r'\bpuntua(n|r)?\b'),
    'recomendación': (r'\b(recomendacion\w*|recommendation\w*)\b', None, r'\b(recomiend\w*|recomendar|recommends?)\b'),
    'mejor candidato': (r'\b(mejor(es)? candidat\w*|best candidates?)\b', r'^(identific|elig|escog|select)', None),
    # B1.3 — capacidad nombrada como «automática» en cualquier orden, con hasta dos palabras intermedias no negativas.
    'selección automática': (r'\b(seleccion|contratacion|descarte|decision|eleccion|puntuacion|calificacion|'
                             r'clasificacion|priorizacion|ordenamiento|ranking|recomendacion)'
                             r'(?: (?!no\b|ni\b|sin\b|nunca\b)[a-z0-9-]+){0,2} automatic\w*|'
                             r'\b(automatic|automated|autonomous)(?: (?!not\b|no\b|without\b|never\b)[a-z0-9-]+){0,2} '
                             r'(selection|hiring|ranking|scoring|prioriti[sz]ation|recommendation|decision|screening|'
                             r'shortlisting)s?\b',
                             None, r'\b(selecciona\w*|descarta\w*|contrata\w*) automaticamente\b'),
    'ranking automático': (r'\b(ranking automatico|nuevo ranking|ranking nuevo|automatic ranking)\b', None, r'\brankea\w*\b'),
    'OCR o extracción': (r'\b(ocr|parsing|parseo|extraccion\w*|extraction)\b', None, r'\b(extrae\w*|parsea\w*)\b'),
    'embeddings': (r'\b(embedding\w*|vectoriz\w*)\b', None, None),
    'búsqueda semántica': (r'\b(busqueda semantica|semantic search)\b', None, None),
    'ML': (r'\b(ml|machine learning|aprendizaje automatico)\b', r'^(entren|train)', None),
    'alcance C': (r'\b(alcance|scope) c\b', None, None),
    'datos reales': (r'\b(datos reales|real data|pii|cvs? reales|curriculos reales|audios? reales|videos? reales|'
                     r'documentos reales|candidatos reales)\b', r'^(carg|import|ingest|utiliz|recib)|^(usa|usar|usan)$', None),
    'producción': (r'\b(produccion|productiv\w*|endpoints?|migracion\w*|migrations?)\b', r'^(registr|conect|expon)', None),
    'F36–F40': (r'\b(f3[6-9]|f40|f36-f40)\b', r'^(inici|abr|comenz|empez|start)', None),
    'G0 real': (r'\bg0 real\b', None, None),
    'RF-23': (r'\brf-?23\b', r'^(automati|modific|reemplaz|elimin|sustitu|cambi)', None),
}
# RF-23 se evalúa por oración con patrones explícitos: «RF-23 … automática/modifica/reemplaza…» o
# «automatiza/modifica/reemplaza… RF-23», sin negación dentro del tramo ni en las tres palabras anteriores al verbo.
RF23_RX = re.compile(r'\brf-?23\b((?:\s+\S+){0,4}?)\s+(automati\w*|modific\w*|reemplaz\w*|elimin\w*|sustitu\w*|decidid\w*|resuelt\w*)\b|'
                     r'\b(automatiz\w*|modific\w*|reemplaz\w*|elimin\w*|sustitu\w*)((?:\s+\S+){0,2}?)\s+rf-?23\b')


def rf23_claim(segs):
    toks = [t for seg in segs for t in seg]
    joined = ' '.join(toks)
    for m in RF23_RX.finditer(joined):
        between = (m.group(1) or m.group(4) or '').split()
        verb_at = joined[:m.start(2) if m.group(2) else m.start(3)].count(' ')
        if not any(t in NEG_WORDS or t.startswith(NEG_PREFIXES) for t in between) and not negated(toks, verb_at):
            return True
    return False


FAMILY_RX = {k: (re.compile(t), re.compile(v) if v else None, re.compile(a) if a else None)
             for k, (t, v, a) in FAMILIES.items()}


def fold(text):
    """Minúsculas, sin acentos, sin Markdown básico (* _ ~ `), guiones unificados y espacios colapsados."""
    text = unicodedata.normalize('NFKD', text)
    text = ''.join(c for c in text if not unicodedata.combining(c)).lower()
    text = re.sub(r'[‐-―−]', '-', text)
    text = re.sub(r'[*_~`]', '', text)
    return re.sub(r'[ \t]+', ' ', text)


def quoted_lines(text, cite=False):
    """Las citas se resuelven por línea, antes de dividir en oraciones (una cita puede contener «;» o «.»). Con
    cite=True se descartan siempre (declaraciones de gobierno); si no, solo cuando la línea las rechaza o las presenta
    como ejemplo, y en otro caso se analizan sin las comillas."""
    out = []
    for line in fold(text).splitlines():
        if QUOTE_RX.search(line):
            outside = QUOTE_RX.sub(' ', line)
            line = outside if cite or REJECT_CTX_RX.search(outside) else re.sub(r'[«»“”"]', ' ', line)
        out.append(line)
    return out


def sentences(text, cite=False, exempt=lambda row: False):
    """Unidades de análisis: cada celda de una fila de tabla (salvo filas exentas) y cada oración de la prosa."""
    out = []
    for line in quoted_lines(text, cite):
        if line.lstrip().startswith('|'):
            if not exempt(line):
                for cell in line.strip().strip('|').split('|'):
                    out += [x for x in re.split(r'(?<=[.!?;])\s+', cell) if x.strip()]
        else:
            out += [s for s in re.split(r'(?<=[.!?;])\s+', line) if s.strip()]
    return out


def segments(sentence):
    """Segmentos de una oración con sus tokens; la negación no cruza comas, dos puntos, celdas ni paréntesis."""
    return [re.findall(r'[a-z0-9]+(?:-[a-z0-9]+)*', seg) for seg in re.split(r'[,:;|()\[\]]', sentence)]


def negated(tokens, i):
    return any(t in NEG_WORDS or t.startswith(NEG_PREFIXES) for t in tokens[max(0, i - 3):i])


def matches(rx, tokens):
    """Índices de token donde empieza cada coincidencia del patrón sobre el segmento."""
    joined = ' '.join(tokens)
    return [joined[:m.start()].count(' ') for m in rx.finditer(joined)]


def positive_claims(text, exempt=lambda s: False):
    """Afirmaciones positivas que habilitan una capacidad prohibida: [(familia, oración)]."""
    hits = []
    for sentence in sentences(text, exempt=exempt):
        body = sentence.strip(' |-')
        if EXAMPLE_PREFIX_RX.match(body):
            continue
        segs = segments(sentence)
        if rf23_claim(segs):
            hits.append(('RF-23', sentence.strip()[:120]))
        hits += [(family, sentence.strip()[:120]) for family in action_claims(segs, sentence)]
        for family, (term_rx, verb_rx, action_rx) in FAMILY_RX.items():
            if family == 'RF-23':
                continue
            terms = [(s, i) for s, toks in enumerate(segs) for i in matches(term_rx, toks) if not negated(toks, i)]
            if not terms:
                continue
            verbs = [(s, i) for s, toks in enumerate(segs) for i, t in enumerate(toks)
                     if (ENABLE_RX.match(t) or (verb_rx and verb_rx.match(t))) and not negated(toks, i)]
            actions = action_rx and [(s, i) for s, toks in enumerate(segs) for i in matches(action_rx, toks)
                                     if not negated(toks, i)]
            if verbs or actions:
                hits.append((family, sentence.strip()[:120]))
    return hits


# Declaraciones de estado de gobierno: sujeto, separador opcional (=, :, :=, ==, ->, →) y valor.
STATE_VALUE = (r'(no\s+)?(aprobad\w*|habilitad\w*|desbloquead\w*|permitid\w*|autorizad\w*|iniciad\w*|activ\w*|'
               r'bloquead\w*|prohibid\w*|propuest\w*|cerrad\w*|congelad\w*|implementad\w*|aceptad\w*)')
LOCKED = ('no aprobad', 'no habilitad', 'no desbloquead', 'no autorizad', 'no iniciad', 'no activ', 'no implementad',
          'no aceptad', 'no permitid')     # negar un estado positivo es coherente con un estado restrictivo
DECLARED = [   # (sujeto, valores admitidos: prefijo del valor normalizado)
    (r'g0 real', ('no aprobad',) + LOCKED),
    (r'g0(?!\s+real)(?![\w-])', ('no aprobad',) + LOCKED),
    (r'adr-005(?: canonico)?', ('propuest',) + LOCKED),
    (r'g0-sbx', ('aprobad con restricciones',)),
    (r'f35 productiva', ('bloquead',) + LOCKED),
    (r'f35-f40(?: productivas)?', ('bloquead',) + LOCKED),
    (r'f36-f40', ('bloquead',) + LOCKED),
    (r'(?:alcance|scope) c', ('bloquead',) + LOCKED),
    (r'datos reales', ('prohibid',) + LOCKED),
    (r'f35-sbx-a', ('cerrad',)),
    (r'f35-sbx-b', ('iniciad',)),
    (r'f35-sbx', ('habilitad',)),
    (r'b0', ('cerrad',)),
    (r'b1', ('implementad', 'pendiente')),
]
DECL_COPULA = (r'(?:ha sido|han sido|ha quedado|han quedado|ha pasado a(?: ser)?|has been|have been|'
               r'queda\w*|quedo|quedaron|fue|fueron|esta|estan|estara\w*|es|son|sera\w*|pasa\w* a(?: ser)?|'
               r'paso a(?: ser)?|declara\w*|resulta\w*|permanece\w*|sigue|siguen|continua\w*|como|is|was|are|were|'
               r'becomes|remains)')
DECL_RX = [(re.compile(r'(?<![\w-])(' + subj + r')(?![\w-])(?:\s*(?::=|==|=|:|->|→)\s*|\s+(no\s+)?(?:se\s+)?'
                       + DECL_COPULA + r'\s+(?:[a-z]+mente\s+)?|\s+)' + STATE_VALUE), allowed)
           for subj, allowed in DECLARED]
# B1.3 — declaración por verbo finito sobre la entidad («se aprueba ADR-005», «aprobamos ADR-005», «ADR-005 se
# aprueba»). Se traduce al estado equivalente y se compara con los valores admitidos de esa entidad. Sin infinitivo
# ni subjuntivo: «falta aprobar ADR-005» o «antes de que se habilite F36» no son declaraciones.
FIN = r'(a|an|o|amos|aron|ara|aran|aremos)'
DECL_VERBS = [
    (r'aprueb(a|an|o)|aprob(o|amos|aron|ara|aran|aremos)|approves?|approved', 'aprobad'),
    (r'habilit' + FIN + r'|enables?|enabled', 'habilitad'),
    (r'desbloque' + FIN + r'|unlocks?|unlocked', 'desbloquead'),
    (r'autoriz' + FIN + r'|authori[sz]es?|authori[sz]ed', 'autorizad'),
    (r'activ' + FIN + r'|activates?|activated', 'activ'),
    (r'inici' + FIN + r'|starts?|started', 'iniciad'),
    (r'acept' + FIN + r'|accepts?|accepted', 'aceptad'),
    (r'permit(e|en|io|imos|ieron|ira|iran|iremos)|permits?|permitted|allows?|allowed', 'permitid'),
    (r'cierr(a|an|o)|cerr(o|amos|aron|ara|aran|aremos)|closes?|closed', 'cerrad'),
    (r'congel' + FIN + r'|freezes?|frozen', 'congelad'),
    (r'implement' + FIN + r'|implements?|implemented', 'implementad'),
    (r'bloque' + FIN + r'|blocks?|blocked', 'bloquead'),
    (r'prohib(e|en|io|imos|ieron|ira|iran|iremos)|prohibits?|prohibited', 'prohibid'),
]
# B1.4 — tiempos compuestos con «haber» («hemos aprobado ADR-005», «se ha aprobado ADR-005»).
PERFECT = r'(?:he|has|ha|hemos|han|habia|habias|habiamos|habian|hubo|habra|habran)\s+'
DECL_VERBS = [(p + '|' + PERFECT + (v if v != 'activ' else 'activad') + r'(?:o|a|os|as)', v) for p, v in DECL_VERBS]
DECL_VERB = '|'.join(f'(?P<v{k}>{p})' for k, (p, _) in enumerate(DECL_VERBS))
DECL_NEG = r'(?:(?P<neg>no|nunca|jamas|tampoco)\s+)?'
VERB_DECL_RX = [(re.compile(r'(?<![\w-])' + DECL_NEG + r'(?:se\s+)?(?:(?:lo|la|los|las)\s+)?(?<![\w-])(?:' + DECL_VERB +
                            r')(?![\w-])\s+(?:[a-z]+mente\s+)?(?:(?:el|la|los|las|al|a|the)\s+)?(?P<subj>' + subj +
                            r')(?![\w-])'), allowed, rx)
                for (subj, allowed), (rx, _) in zip(DECLARED, DECL_RX)] + \
               [(re.compile(r'(?<![\w-])(?P<subj>' + subj + r')(?![\w-])\s+' + DECL_NEG + r'se\s+(?:[a-z]+mente\s+)?(?:' +
                            DECL_VERB + r')(?![\w-])'), allowed, rx)
                for (subj, allowed), (rx, _) in zip(DECLARED, DECL_RX)]
STEM_RX = re.compile(r'(aprobad|habilitad|desbloquead|permitid|autorizad|iniciad|activ|bloquead|prohibid|propuest|'
                     r'cerrad|congelad|implementad|aceptad)')
RESTRICTIONS = r'(restricciones|restriccion|limitaciones|condiciones|salvaguardas|restrictions|limitations)\b'
# B1.4 — «ya no tiene restricciones» o «deja de tener restricciones» afirman la eliminación aunque contengan «no».
UNRESTRICTED_RX = re.compile(r'\b((ya no|no|no longer|nunca mas) (tiene|tienen|tendra|tendran|cuenta con|contara con|'
                             r'mantiene|mantendra|conserva|conservara|has|have|carries|keeps)(?: (any|las|sus|ninguna|'
                             r'mas|its))? ' + RESTRICTIONS + r'|(deja|dejan|dejara|dejaran|dejo|dejaron|ceases to|ceased '
                             r'to|stops) (de )?(tener|estar sujeta a|aplicar|mantener|conservar|have|having|be subject '
                             r'to)(?: (las|sus|its|any))? ' + RESTRICTIONS + r'|(has|have) no ' + RESTRICTIONS +
                             r'|no longer (restricted|subject to (any )?restrictions)\b|'
                             r'sin (restricciones|restriccion|limitaciones|condiciones|salvaguardas)\b|irrestrict\w*|'
                             r'without restrictions\b|unrestricted\b|(plena|total|completa)mente (habilitad|aprobad|'
                             r'autorizad|activ|desbloquead|irrestrict)\w*|(plena|total|completa) (habilitacion|'
                             r'aprobacion|autorizacion)\b|fully (enabled|approved|unlocked|authori[sz]ed)\b)')
RESTRICTION_RX = re.compile(r'^(restricciones|restriccion|restrictions?|limitaciones|condiciones|salvaguardas)$')
# B1.4 — aprobación como objeto: «ADR-005 recibe aprobación», «se concede la aprobación de ADR-005».
APPROVAL_RX = re.compile(r'^(aprobacion|autorizacion|habilitacion|desbloqueo|approval|authori[sz]ation|sign-off)$')
GRANT_RX = re.compile(r'^(recib(e|en|io|ieron|ira|iran|ido|ida)|obtien(e|en)|obtuv(o|ieron)|obtendra|obtendran|'
                      r'obtenid(o|a)|consigu(e|en|io|ieron|ira|iran|ido|ida)|(logr|alcanz|otorg)(a|an|o|aron|ara|aran|'
                      r'ado|ada)|conced(e|en|io|ieron|era|eran|ido|ida)|da|dan|dio|dieron|dara|daran|dado|dada|'
                      r'receives?|received|gets?|got|gotten|obtains?|obtained|gains?|gained|grants?|granted|gives?|'
                      r'gave|given)$')
REMOVE_RX = re.compile(r'^((elimin|levant|retir|quit|anul|derog)' + AR + r'|suprim' + ER_IR +
                       r'|removes?|removed|lifts?|lifted|drops?|dropped|waives?|waived)$')
DECL_NEG_RX = re.compile(r'\b(no|nunca|jamas)\s+(\w+\s+){0,2}(declar\w*|figur\w*|registr\w*|afirm\w*|indic\w*|'
                         r'decir|escrib\w*|pon\w*)|\b(rechaz\w*|prohib\w*|detect\w*|impid\w*|imped\w*|ejemplo\w*|'
                         r'negativ\w*|intent\w*)\b')


def state_value(negated_value, word, rest):
    """Estado normalizado: «no » opcional, raíz del valor y, si sigue, «con restricciones» o «sin restricciones»."""
    value = ('no ' if negated_value else '') + STEM_RX.match(word).group(1)
    rest = rest.lstrip()
    if rest.startswith('con restricciones'):
        value += ' con restricciones'
    elif UNRESTRICTED_RX.match(rest):
        value += ' sin restricciones'
    return value


def admitted(value, allowed):
    """Valor admitido para la entidad; negar un estado irrestricto siempre es coherente."""
    return value.startswith(allowed) or (value.startswith('no ') and value.endswith(' sin restricciones'))


REJECT_RX = re.compile(r'^(rechaz|prohib|detect|impid|imped|ejemplo|negativ|intent|reject|forbid)')


def g0sbx_unrestricted(body):
    """B1.3 — G0-SBX sin restricciones, plenamente habilitada o con sus restricciones eliminadas, en cualquier orden.
    Un marcador cuenta si ninguna negación lo precede desde la mención de G0-SBX (o en sus tres palabras anteriores)
    y si la cláusula que abre esa mención no es un rechazo, una prohibición o un ejemplo («|» marca cada cláusula)."""
    toks = [t for seg in segments(body) for t in seg + ['|']]
    subj = [k for k, t in enumerate(toks) if t == 'g0-sbx']
    if not subj:
        return []

    def rejected(at):
        start = max((x for x in range(at) if toks[x] == '|'), default=-1) + 1
        return any(REJECT_RX.match(t) for t in toks[start:at])
    out = []
    for k in matches(UNRESTRICTED_RX, toks):
        prev = [j for j in subj if j < k]
        anchor = prev[-1] if prev else k
        span = toks[anchor + 1:k] if prev else toks[max(0, k - 3):k]
        if not any(t in NEG_WORDS or t.startswith(NEG_PREFIXES) for t in span) and not rejected(anchor):
            out.append(f'«G0-SBX … {" ".join(toks[k:k + 2])}»')
    for k, t in enumerate(toks):
        if REMOVE_RX.match(t) and not negated(toks, k) and not rejected(k) and any(
                RESTRICTION_RX.match(r) and not set(toks[max(0, j - 2):j]) & NEG_WORDS for j, r in enumerate(toks)):
            out.append(f'«{t} … restricciones de G0-SBX»')
    return out


def approval_grants(body):
    """B1.4 — una entidad restrictiva recibe, obtiene o se le concede aprobación o autorización en el mismo tramo, sin
    negación del verbo ni rechazo, prohibición o ejemplo en la cláusula."""
    out = []
    for seg in segments(body):
        joined = ' '.join(seg)
        for subj, allowed in DECLARED:
            if allowed[0].startswith('aprobad') or not re.search(r'(?<![\w-])' + subj + r'(?![\w-])', joined):
                continue
            if not any(APPROVAL_RX.match(t) for t in seg) or any(REJECT_RX.match(t) for t in seg):
                continue
            for k, t in enumerate(seg):
                if GRANT_RX.match(t) and not negated(seg, k):
                    out.append(f'«{joined[:60]}»')
                    break
    return out


def contradictions(text, exempt=lambda row: False):
    """Declaraciones de estado distintas de las vigentes, por separador o cópula («ADR-005 queda APROBADA»), por verbo
    finito sobre la entidad («se aprueba ADR-005») y G0-SBX sin restricciones. No cuentan las citas ni las que una
    prohibición o un ejemplo introducen dentro de su propio tramo (desde el último signo de puntuación)."""
    out = []
    for body in sentences(text, cite=True, exempt=exempt):
        if EXAMPLE_PREFIX_RX.match(body.strip(' |-')):
            continue
        found = []
        for rx, allowed in DECL_RX:
            for m in rx.finditer(body):
                found.append((m, allowed, state_value(bool(m.group(2) or m.group(3)), m.group(4), body[m.end():])))
        for rx, allowed, decl_rx in VERB_DECL_RX:
            for m in rx.finditer(body):
                if decl_rx.match(body, m.start('subj')):     # la entidad abre su propia declaración: se evalúa arriba
                    continue
                k = next(int(g[1:]) for g, v in m.groupdict().items() if v and g.startswith('v'))
                found.append((m, allowed, state_value(bool(m.group('neg')), DECL_VERBS[k][1], body[m.end():])))
        for m, allowed, value in found:
            if admitted(value, allowed):
                continue
            before = re.split(r'[.,;:!?|]', body[:m.start()])[-1]
            if DECL_NEG_RX.search(before):
                continue
            out.append(f'«{m.group(0).strip()}»')
        out += g0sbx_unrestricted(body) + approval_grants(body)
    return out


# ---------------------------------------------------------------- reglas puras sobre el estado
def text_of(data):
    if data is None:
        return None
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError:
        return None


def r_ctx(S):
    out = list(S['errors'])
    if out:
        return out
    out += S['env']
    if not S.get('inside'):
        out.append('no es un árbol de trabajo Git')
    if S.get('branch') not in BRANCHES:
        out.append(f'rama no permitida o HEAD separado: «{S.get("branch")}»')
    out += [f'{name} no es ancestro de HEAD' for name, ok in S.get('ancestors', {}).items() if not ok]
    if len(S.get('ancestors', {})) != 3:
        out.append('ascendencia no verificable')
    return out


def r_ain(S):
    if S['errors']:
        return ['integridad de A no verificable (falla cerrado)']
    out = []
    exp = S['a_expected']
    if len(exp) != A_COUNT:
        out.append(f'F35-SBX-A en E debería tener {A_COUNT} archivos protegidos y tiene {len(exp)}')
    bad = [p for p, meta in exp.items() if meta[:2] != ('100644', 'blob') or S['a_real'].get(p) != meta[2]]
    if bad:
        out.append(f'F35-SBX-A distinta de E, eliminada o ilegible: {sorted(bad)[:5]}')
    extra = sorted(S['a_fs'] - set(exp))
    if extra:
        out.append(f'archivos extra en F35-SBX-A: {extra[:5]}')
    out += S['a_walk']
    if S['a_head_diff']:
        out.append(f'árbol de HEAD cambia F35-SBX-A respecto de E: {S["a_head_diff"][:5]}')
    return out


def r_b0f(S):
    if S['errors']:
        return ['B0 no verificable (falla cerrado)']
    return [] if S['b0_real'] == S['b0_blob'] else [f'{B0_DOC}: distinto de su cierre auditado']


def r_sbx(S):
    if S['errors']:
        return ['SBX-01..SBX-18 no evaluables (falla cerrado)']
    if S['sbx'] is None:
        return [S['sbx_error'] or 'SBX-01..SBX-18 no evaluables (falla cerrado)']
    out = []
    if set(S['sbx']) != set(SBX_IDS):
        out.append(f'criterios no evaluables o desconocidos: {sorted(set(SBX_IDS) ^ set(S["sbx"]))}')
    out += [f'{k} incumplido (clase B): {S["sbx"][k][1]}' for k in SBX_IDS if k in S['sbx'] and not S['sbx'][k][0]]
    return out


def r_gov(S):
    if S['errors']:
        return ['gobierno no verificable (falla cerrado)']
    out = []
    for path in GOVERNANCE:
        text, base = text_of(S['gov'][path]), text_of(S['gov_base'][path])
        if text is None or base is None:
            out.append(f'{path}: ilegible (falla cerrado)')
            continue
        sections = re.findall(r'^## Estado vigente F34E\s*\n(.*?)(?=^## |\Z)', text, re.M | re.S)
        if len(sections) != 1:
            out.append(f'{path}: se exige una única sección «Estado vigente F34E»')
            continue
        section = sections[0]
        states = [ln for ln in section.splitlines() if re.match(r'^- [^=\n]+ = ', ln)]
        if states != STATES:
            out.append(f'{path}: los trece estados de gobierno no son exactamente los vigentes')
        header = '\n'.join(ln for ln in text.splitlines() if ln.startswith('Última actualización:'))
        b_states = [' '.join(m.split()) for m in B_STATE_RX.findall(section + '\n' + header)]
        if not b_states or set(b_states) != {'INICIADA'}:
            out.append(f'{path}: F35-SBX-B debe figurar solo INICIADA en el estado vigente: {sorted(set(b_states))}')
        added = '\n'.join(ln for ln in text.splitlines() if ln not in set(base.splitlines()))
        current = section + '\n' + header + '\n' + added
        bad = contradictions(current)
        if bad:
            out.append(f'{path}: declaraciones de estado contradictorias con el gobierno vigente: {bad[:3]}')
        claims = positive_claims(added)
        if claims:
            out.append(f'{path}: líneas añadidas que afirman habilitar una capacidad prohibida: {claims[:2]}')
    return out


def r_scp(S):
    if S['errors']:
        return ['alcance no verificable (falla cerrado)']
    out = []
    for where, delta in S['delta'].items():
        for status, path in sorted(delta):
            if SCOPE.get(path) != status:
                out.append(f'{where}: cambio fuera del alcance de B1 o con estado inesperado: {status} {path}')
    present = {p for st, p in S['delta']['HEAD'] | S['delta']['árbol']} | {p for p in S['untracked'] if SCOPE.get(p) == 'A'}
    missing = sorted(set(SCOPE) - present)
    if missing:
        out.append(f'rutas obligatorias de B1 ausentes del delta: {missing}')
    stray = sorted(p for p in S['untracked'] if SCOPE.get(p) != 'A')
    if stray:
        out.append(f'archivos sin seguimiento fuera del alcance de B1: {stray[:5]}')
    return out


def r_fsy(S):
    if S['errors']:
        return ['sistema de archivos no verificable (falla cerrado)']
    out = list(S['b_walk']) + list(S['rt_walk']) + list(S['rt_exc'])
    if S['b_fs'] != B_FILES:
        out.append(f'carpetas de B distintas de la lista exacta: extra={sorted(S["b_fs"] - B_FILES)[:3]} '
                   f'faltan={sorted(B_FILES - S["b_fs"])[:3]}')
    if S['links']:
        out.append(f'enlaces en rutas de B o de gobierno: {S["links"][:3]}')
    if S['rt_tracked'] != set(S['rt_base']):
        out.append(f'el árbol de HEAD difiere de la base autorizada en el runtime, el dataset o la evidencia: '
                   f'{sorted(S["rt_tracked"] ^ set(S["rt_base"]))[:5]}')
    generated = sorted(p for p in S['rt_fs'] - set(S['rt_base']) if p.startswith(RT_GENERATED))
    if generated:
        out.append(f'código generado y no versionado (bundle de Vite, Wayfinder o caché de Laravel): su origen no es '
                   f'verificable frente a la base y no se certifica por nombre ni extensión (falla cerrado): '
                   f'{generated[:5]}')
    extra = sorted(p for p in S['rt_fs'] - set(S['rt_base']) if not p.startswith(RT_GENERATED))
    if extra:
        out.append(f'archivos en el runtime, el dataset o la evidencia que no están en la base autorizada (aunque Git '
                   f'los ignore): {extra[:5]}')
    missing = sorted(set(S['rt_base']) - S['rt_fs'])
    if missing:
        out.append(f'archivos de la base ausentes o reemplazados en el runtime, el dataset o la evidencia: {missing[:5]}')
    changed = sorted(p for p, meta in S['rt_base'].items() if p in S['rt_real'] and (
        meta[:2] not in (('100644', 'blob'), ('100755', 'blob')) or S['rt_real'][p] != meta[2]))
    if changed:
        out.append(f'bytes reales distintos de su blob en la base autorizada {B_BASE[:7]} (código no certificado): '
                   f'{changed[:5]}')
    return out


def r_hst(S):
    if S['errors']:
        return ['historia de F35-SBX-A no verificable (falla cerrado)']
    out = []
    if S['shallow']:
        out.append('repositorio superficial: la historia E..HEAD no es completa (falla cerrado)')
    out += [f'el commit {c[:12]} toca F35-SBX-A después de E: {paths[:3]}' for c, paths in S['a_history']]
    return out


def r_flg(S):
    if S['errors']:
        return ['índice no verificable (falla cerrado)']
    return [f'flags del índice que ocultan cambios: {S["flags"][:5]}'] if S['flags'] else []


def row_cell(text):
    return ' '.join(re.sub(r'[«»“”"]', ' ', fold(text)).split())


def case_row(sentence):
    """Una fila «| NB-xx | REGLA | descripción |» solo describe un negativo si coincide con un caso del gate."""
    cells = tuple(row_cell(c) for c in sentence.strip().strip('|').split('|'))
    return len(cells) == 3 and cells in CASE_ROWS


def r_cnt(S):
    if S['errors']:
        return ['contenido no verificable (falla cerrado)']
    out = []
    for path, data in S['files'].items():
        if not path.endswith(('.md', '.json', '.py')):
            out.append(f'{path}: tipo de archivo no autorizado')
            continue
        if data is None or len(data) > MAX_BYTES or b'\x00' in data or b'\r' in data or data.startswith(b'\xef\xbb\xbf'):
            out.append(f'{path}: ilegible, binario, CR, BOM o tamaño excesivo')
            continue
        text = text_of(data)
        if text is None:
            out.append(f'{path}: no es UTF-8')
            continue
        if not path.endswith('.py'):
            hits = [m.group(0) for rx in PII for m in [rx.search(text)] if m]
            if hits:
                out.append(f'{path}: posible dato personal: {hits[:2]}')
        if path.endswith('.md') and path != B0_DOC:      # B0 está congelado por B0F
            claims = positive_claims(text, exempt=case_row)
            if claims:
                out.append(f'{path}: afirmación positiva que habilita una capacidad prohibida: {claims[:2]}')
            bad = contradictions(text, exempt=case_row)
            if bad:
                out.append(f'{path}: declaraciones de estado contradictorias con el gobierno vigente: {bad[:2]}')
        if path.endswith('.json'):
            try:
                keys = []

                def walk_keys(o):
                    if isinstance(o, dict):
                        for k, v in o.items():
                            keys.append(k)
                            walk_keys(v)
                    elif isinstance(o, list):
                        for v in o:
                            walk_keys(v)
                walk_keys(json.loads(text))
                bad = [k for k in keys if JSON_KEY_RX.search(k)]
                if bad:
                    out.append(f'{path}: claves con capacidades prohibidas: {bad[:3]}')
            except ValueError:
                out.append(f'{path}: JSON inválido')
    return out


def r_dep(S):
    if S['errors']:
        return ['código no verificable (falla cerrado)']
    out = []
    for path, data in S['files'].items():
        if not path.endswith('.py'):
            continue
        try:
            tree = ast.parse(text_of(data) or '')
        except (SyntaxError, ValueError) as e:
            out.append(f'{path}: código ilegible ({e.__class__.__name__})')
            continue
        mods = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                mods |= {a.name.split('.')[0] for a in node.names}
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    out.append(f'{path}: importación relativa')
                mods.add((node.module or '').split('.')[0])
            elif isinstance(node, ast.Call):
                fn = node.func
                name = fn.id if isinstance(fn, ast.Name) else fn.attr if isinstance(fn, ast.Attribute) else ''
                if name in ('__import__', 'import_module'):
                    out.append(f'{path}: importación dinámica')
        out += [f'{path}: dependencia no autorizada «{m}»' for m in sorted(mods - STDLIB_OK)]
    return out


RULES = {'CTX': r_ctx, 'AIN': r_ain, 'HST': r_hst, 'B0F': r_b0f, 'SBX': r_sbx, 'GOV': r_gov, 'SCP': r_scp,
         'FSY': r_fsy, 'FLG': r_flg, 'CNT': r_cnt, 'DEP': r_dep}


def run_rules(S):
    return {rid: fn(S) for rid, fn in RULES.items()}


# ---------------------------------------------------------------- casos negativos (estado mutado en memoria)
def mutate(fn):
    def apply(S):
        T = copy.deepcopy(S)
        fn(T)
        return T
    return apply


def gov_sub(old, new):
    def fn(T):
        for p in GOVERNANCE:
            text = T['gov'][p].decode('utf-8')
            assert old in text, old
            T['gov'][p] = text.replace(old, new, 1).encode('utf-8')
    return mutate(fn)


def doc_add(line):
    return mutate(lambda T: T['files'].__setitem__(B1_DOC, T['files'][B1_DOC] + f'\n{line}\n'.encode('utf-8')))


def gov_add(line):
    return mutate(lambda T: T['gov'].__setitem__('CLAUDE.md', T['gov']['CLAUDE.md'] + f'\n{line}\n'.encode('utf-8')))


B1_DOC = 'docs/academico/evidencia-sbx-b/F35SBXB_B1_Gate_Sucesor.md'
README_B = 'docs/academico/evidencia-sbx-b/README.md'
CASES = [
    ('NB-01', 'SBX', 'SBX-05 incumplido (campo de puntaje en schema.json)',
     mutate(lambda T: T['sbx'].__setitem__('SBX-05', (False, ['applications.score'])))),
    ('NB-02', 'GOV', 'G0 real declarada APROBADA', gov_sub('- G0 real = NO APROBADA', '- G0 real = APROBADA')),
    ('NB-03', 'CNT', 'dato personal real en un documento de B',
     mutate(lambda T: T['files'].__setitem__(B1_DOC, T['files'][B1_DOC] + b'\nContacto: maria.quispe@colegio.edu.pe\n'))),
    ('NB-04', 'AIN', 'archivo protegido de F35-SBX-A alterado',
     mutate(lambda T: T['a_real'].__setitem__(sorted(T['a_real'])[0], '0' * 40))),
    ('NB-05', 'SCP', 'cambio productivo fuera del alcance (app/)',
     mutate(lambda T: T['delta']['árbol'].add(('M', 'app/Models/User.php')))),
    ('NB-06', 'FSY', 'archivo extra no autorizado en evidencia-sbx-b (ignorado por Git)',
     mutate(lambda T: T['b_fs'].add('docs/academico/evidencia-sbx-b/oculto.md'))),
    ('NB-07', 'FSY', 'enlace simbólico en una ruta de B', mutate(lambda T: T['links'].append(README_B))),
    ('NB-08', 'FLG', 'assume-unchanged en CLAUDE.md', mutate(lambda T: T['flags'].append('h CLAUDE.md'))),
    ('NB-09', 'FLG', 'skip-worktree en el documento de B0', mutate(lambda T: T['flags'].append(f'S {B0_DOC}'))),
    ('NB-10', 'CTX', 'error de Git', lambda S: collect(runner=lambda *a: (128, b''))),
    ('NB-11', 'CTX', 'estado desconocido: HEAD separado', mutate(lambda T: T.__setitem__('branch', ''))),
    ('NB-12', 'SBX', 'estado desconocido: criterio SBX-18 no evaluable',
     mutate(lambda T: T['sbx'].pop('SBX-18'))),
    ('NB-13', 'GOV', 'intento de habilitar F36–F40', gov_sub('- F36–F40 = BLOQUEADAS', '- F36–F40 = HABILITADAS')),
    ('NB-14', 'GOV', 'línea añadida que habilita el alcance C', gov_add('Alcance C = HABILITADO para F35-SBX-B.')),
    ('NB-15', 'GOV', 'F35-SBX-B declarada CERRADA en el estado vigente',
     gov_sub('F35-SBX-B INICIADA solo como sandbox', 'F35-SBX-B CERRADA solo como sandbox')),
    ('NB-16', 'B0F', 'documento de B0 modificado', mutate(lambda T: T.__setitem__('b0_real', '1' * 40))),
    ('NB-17', 'DEP', 'dependencia de ML en el código de B',
     mutate(lambda T: T['files'].__setitem__(GATE, T['files'][GATE] + b'\nimport sklearn\n'))),
    ('NB-18', 'CNT', 'JSON de B con un campo de puntaje',
     mutate(lambda T: T['files'].__setitem__('docs/academico/evidencia-sbx-b/x.json', b'{"candidate_score": 1}'))),
    # B1.1 — M01: afirmaciones positivas en Markdown autorizado (familias, mayúsculas, Markdown, español e inglés).
    ('NB-20', 'CNT', 'Markdown de B que afirma habilitar scoring y recomendación del mejor candidato',
     doc_add('**Se habilita** scoring de candidatos y recomendación automática del *mejor candidato*.')),
    ('NB-21', 'CNT', 'mayúsculas: OCR y alcance C habilitados', doc_add('SE HABILITA OCR Y SCOPE C EN B.')),
    ('NB-22', 'CNT', 'inglés: scoring y búsqueda semántica habilitados',
     doc_add('Candidate scoring and semantic search are enabled for B.')),
    ('NB-23', 'CNT', 'datos reales permitidos', doc_add('Queda permitido cargar datos reales de postulantes.')),
    ('NB-24', 'CNT', 'RF-23 automatizada', doc_add('RF-23 pasa a ser automática.')),
    ('NB-25', 'CNT', 'F36 autorizada', doc_add('Se autoriza iniciar F36 en este sandbox.')),
    ('NB-26', 'CNT', 'endpoints productivos activados', doc_add('Se activan endpoints productivos para B.')),
    # B1.1 — M02: estados contradictorios junto a los canónicos (mayúsculas, Markdown, :=, flecha).
    ('NB-27', 'GOV', 'estado canónico más «g0 real = aprobada»', gov_add('g0 real = aprobada')),
    ('NB-28', 'GOV', 'contradicción con Markdown en F35 productiva', gov_add('**F35 productiva** = Habilitada')),
    ('NB-29', 'GOV', 'contradicción con := en el alcance C', gov_add('scope c := habilitado')),
    ('NB-30', 'GOV', 'contradicción con dos puntos en datos reales', gov_add('Datos Reales: PERMITIDOS')),
    ('NB-31', 'GOV', 'contradicción con flecha en G0 real', gov_add('G0 real → APROBADA')),
    ('NB-32', 'GOV', 'B1 declarada cerrada', gov_add('B1 = CERRADA')),
    # B1.1 — M03: superficies del runtime.
    ('NB-33', 'FSY', 'archivo de runtime que no está en HEAD (ignorado)',
     mutate(lambda T: T['rt_fs'].add('app/Models/B1AuditHidden.php'))),
    ('NB-34', 'FSY', 'archivo de HEAD ausente del runtime', mutate(lambda T: T['rt_fs'].discard(sorted(T['rt_tracked'])[0]))),
    ('NB-35', 'FSY', 'enlace en una superficie del runtime',
     mutate(lambda T: T['rt_walk'].append('enlace en una ruta protegida: routes/enlace.php'))),
    # B1.1 — M04: historia de F35-SBX-A.
    ('NB-36', 'HST', 'commit posterior a E que toca F35-SBX-A (aunque se restaure)',
     mutate(lambda T: T['a_history'].append(('f' * 40, ['docs/academico/tools/f35sbx/f35sbx_scope.py'])))),
    ('NB-37', 'HST', 'repositorio superficial', mutate(lambda T: T.__setitem__('shallow', True))),
    ('NB-38', 'CNT', 'RF-23 declarada automática con dos puntos', doc_add('RF-23: automática.')),
    # B1.2 — M01 residual: acciones inequívocas y selección automática (frases distintas de las de la auditoría).
    ('NB-39', 'CNT', 'acción de puntuar candidatos', doc_add('Ahora permitimos puntuar candidatos.')),
    ('NB-40', 'CNT', 'recomendación automática del candidato más apto',
     doc_add('El sistema recomienda automáticamente al candidato más apto.')),
    ('NB-41', 'CNT', 'selección final predicada como automática', doc_add('La selección final será automática.')),
    ('NB-42', 'CNT', 'el sistema selecciona al candidato ganador', doc_add('El sistema seleccionará al candidato ganador.')),
    ('NB-43', 'CNT', 'el motor decide automáticamente', doc_add('El motor decide automáticamente la selección final.')),
    ('NB-44', 'CNT', 'RF-23 decidido automáticamente', doc_add('RF-23 será decidido automáticamente por el motor.')),
    ('NB-45', 'CNT', 'inglés: ranking automático de candidatos', doc_add('We now rank candidates automatically.')),
    ('NB-46', 'CNT', 'el motor elige a los mejores postulantes', doc_add('El motor elegirá a los mejores postulantes.')),
    ('NB-47', 'CNT', 'contratación predicada como automática', doc_add('La contratación pasa a ser automática.')),
    # B1.2 — M02 residual: declaraciones directas con verbo copulativo (varias entidades).
    ('NB-48', 'GOV', 'ADR-005 queda APROBADA', gov_add('ADR-005 queda APROBADA')),
    ('NB-49', 'GOV', 'ADR-005 fue o está APROBADA', gov_add('ADR-005 está APROBADA')),
    ('NB-50', 'GOV', 'alcance C pasa a HABILITADO', gov_add('Scope C pasa a HABILITADO')),
    ('NB-51', 'GOV', 'F35 productiva no está BLOQUEADA', gov_add('F35 productiva no está BLOQUEADA')),
    ('NB-52', 'GOV', 'datos reales están permitidos', gov_add('Datos reales están permitidos')),
    # B1.2 — M03 residual: abuso de una excepción de FSY.
    ('NB-53', 'FSY', 'código no autorizado dentro de una excepción de FSY',
     mutate(lambda T: T['rt_exc'].append('archivo no autorizado dentro de la excepción cypress/results: x.php'))),
    # B1.3 — M01 y RF-23: conjugaciones, objeto de decisión, sistema como agente y contexto humano que no exime.
    ('NB-54', 'CNT', 'primera persona del futuro: asignaremos una calificación automática',
     doc_add('Asignaremos una calificación automática al candidato.')),
    ('NB-55', 'CNT', 'inglés: ranking automático de candidatos habilitado', doc_add('Automatic candidate ranking enabled.')),
    ('NB-56', 'CNT', 'futuro: el motor priorizará automáticamente candidatos',
     doc_add('El motor priorizará automáticamente candidatos para selección.')),
    ('NB-57', 'CNT', 'la decisión final la tomará el sistema',
     doc_add('La decisión final la tomará automáticamente el sistema.')),
    ('NB-58', 'CNT', 'inglés: el sistema elige al postulante final', doc_add('The system chooses the final applicant.')),
    ('NB-59', 'CNT', 'el sistema realizará la selección final', doc_add('El sistema realizará la selección final.')),
    ('NB-60', 'CNT', 'la plataforma escoge al ganador sin intervención humana',
     doc_add('La plataforma escogerá al ganador sin intervención humana.')),
    ('NB-61', 'CNT', 'variante: el algoritmo efectuará la contratación final',
     doc_add('El algoritmo efectuará la contratación final.')),
    ('NB-62', 'CNT', 'variante: el sistema selecciona y el Aprobador solo recibe aviso',
     doc_add('El sistema seleccionará al candidato y el Aprobador será notificado manualmente.')),
    # B1.3 — M02: verbo finito sobre la entidad, «ha sido» y G0-SBX sin restricciones.
    ('NB-63', 'GOV', 'verbo antes de la entidad: se aprueba ADR-005', gov_add('Se aprueba ADR-005')),
    ('NB-64', 'GOV', 'primera persona: aprobamos ADR-005', gov_add('Aprobamos ADR-005')),
    ('NB-65', 'GOV', 'ADR-005 ha sido aprobada', gov_add('ADR-005 ha sido aprobada')),
    ('NB-66', 'GOV', 'G0-SBX queda sin restricciones', gov_add('G0-SBX queda SIN RESTRICCIONES')),
    ('NB-67', 'GOV', 'se eliminan las restricciones de G0-SBX', gov_add('Se eliminan las restricciones de G0-SBX')),
    ('NB-68', 'GOV', 'G0-SBX queda plenamente habilitada', gov_add('G0-SBX queda plenamente habilitada')),
    ('NB-69', 'CNT', 'Markdown de B: se aprobó ADR-005', doc_add('Se aprobó ADR-005.')),
    # B1.3 — M03: código ejecutable sin origen verificable.
    ('NB-70', 'FSY', 'bundle de Vite no versionado aunque el manifiesto lo nombre',
     mutate(lambda T: T['rt_fs'].update({'public/build/manifest.json', 'public/build/assets/app-AbCdEf12.js'}))),
    ('NB-71', 'FSY', 'TypeScript de Wayfinder no versionado', mutate(lambda T: T['rt_fs'].add('resources/js/routes/index.ts'))),
    ('NB-72', 'FSY', 'caché PHP de Laravel no versionada', mutate(lambda T: T['rt_fs'].add('bootstrap/cache/packages.php'))),
    ('NB-73', 'FSY', 'archivo del runtime con bytes distintos de la base autorizada',
     mutate(lambda T: T['rt_real'].__setitem__(sorted(T['rt_real'])[0], '0' * 40))),
    # B1.4 — entorno del intérprete (los casos de integridad previa a la ejecución están en integrity_cases).
    ('NB-84', 'CTX', 'intérprete no aislado o con PYTHONPATH',
     mutate(lambda T: T['env'].append('variable de entorno PYTHONPATH definida'))),
    # B1.4 — M01, RF-23 y M02 residuales.
    ('NB-85', 'CNT', 'el sistema asigna notas automáticamente a los postulantes',
     doc_add('El sistema asignará notas automáticamente a los postulantes.')),
    ('NB-86', 'CNT', 'inglés: candidatos ordenados automáticamente para la selección',
     doc_add('Candidates are automatically ordered for selection.')),
    ('NB-87', 'CNT', 'el motor sugiere qué candidato debe avanzar', doc_add('El motor sugerirá qué candidato debe avanzar.')),
    ('NB-88', 'CNT', 'el sistema calcula la calificación de cada candidato',
     doc_add('El sistema calculará la calificación de cada candidato.')),
    ('NB-89', 'CNT', 'el sistema determina al seleccionado sin decir automático', doc_add('El sistema determinará al seleccionado.')),
    ('NB-90', 'CNT', 'la plataforma decide quién obtiene la plaza', doc_add('La plataforma decidirá quién obtiene la plaza.')),
    ('NB-91', 'CNT', 'inglés: el motor determina al postulante elegido',
     doc_add('The engine determines the successful applicant.')),
    ('NB-92', 'GOV', 'ADR-005 recibe aprobación', gov_add('ADR-005 recibe aprobación')),
    ('NB-93', 'GOV', 'tiempo compuesto: hemos aprobado ADR-005', gov_add('Hemos aprobado ADR-005')),
    ('NB-94', 'GOV', 'G0-SBX ya no tiene restricciones', gov_add('G0-SBX ya no tiene restricciones')),
    ('NB-95', 'GOV', 'G0-SBX deja de tener restricciones', gov_add('G0-SBX deja de tener restricciones')),
    # B1.5 — recomendación implícita del sistema sobre quién continúa.
    ('NB-96', 'CNT', 'el motor recomienda quién debe continuar', doc_add('El motor recomendará quién debe continuar.')),
]
CASE_ROWS = {(row_cell(cid), row_cell(rule), row_cell(what)) for cid, rule, what, _ in CASES}
# Controles positivos de B1.1: negación, prohibición, cita rechazada y ejemplo negativo no son afirmaciones.
LEGIT_TEXTS = ['No se habilita scoring.', 'Scoring permanece prohibido.',
               'El gate debe rechazar «G0 real = APROBADA».', 'Ejemplo negativo: Scope C habilitado.',
               'Intento de habilitar F36–F40.', 'Sin scoring, recomendación ni selección automática.',
               'No debe declararse G0 real = APROBADA.', 'Nunca se permiten datos reales.',
               'El gate rechaza «F36–F40 = HABILITADAS» y «datos reales = permitidos».',
               'Selección automática y RF-23 sin cambios.', 'RF-23 no se modifica.',
               'La selección final permanece bajo decisión humana.', 'La selección automática está prohibida.',
               "El gate debe rechazar: 'la selección final será automática'.", 'Puntuar candidatos está prohibido.',
               'Bypass reproducido: el sistema seleccionará al candidato ganador.', 'ADR-005 permanece PROPUESTA.',
               'ADR-005 no está APROBADA.', 'El gate debe rechazar ADR-005 queda APROBADA.',
               # B1.3
               'El Aprobador seleccionará manualmente al candidato, con confirmación humana.',
               'La decisión final corresponde al Aprobador.', 'RF-23 permanece como decisión humana.',
               'El gate debe rechazar “el sistema realizará la selección final”.',
               'El sistema no realizará la selección final.', 'La Dirección escogerá al candidato con justificación humana.',
               'ADR-005 no ha sido aprobada.', 'No se aprueba ADR-005.', 'El gate debe rechazar “Se aprueba ADR-005”.',
               'Ejemplo negativo: “ADR-005 queda aprobada”.', 'G0-SBX = APROBADA CON RESTRICCIONES.',
               'Las restricciones de G0-SBX permanecen vigentes.', 'G0-SBX no está aprobada sin restricciones.',
               'El gate debe rechazar “G0-SBX queda sin restricciones”.',
               # B1.4
               'El evaluador asigna notas a los postulantes según la rúbrica.',
               'El sistema muestra el ranking y el Aprobador elige al candidato.',
               'La Dirección decide quién obtiene la plaza.', 'El sistema no decide quién obtiene la plaza.',
               'La decisión final requiere confirmación humana.', 'ADR-005 no recibe aprobación.',
               'No hemos aprobado ADR-005.', 'ADR-005 requiere aprobación externa.', 'G0-SBX mantiene restricciones.',
               'No se eliminan las restricciones de G0-SBX.', 'G0-SBX nunca deja de tener restricciones.',
               # B1.5
               'El motor no recomendará quién debe continuar.',
               'Está prohibido que el sistema recomiende quién debe avanzar.',
               'El gate debe rechazar “El motor recomendará quién debe continuar”.',
               'Ejemplo negativo: “The engine recommends who should continue”.',
               'El Aprobador decide quién debe continuar.', 'Dirección determina quién avanza.',
               'El sistema muestra información y el Aprobador decide quién continúa.']


def integrity_cases(S):
    """DH-B13: un módulo de compute_sbx() alterado no se importa (lectura simulada, sin tocar archivos). B1.3: tampoco
    con un archivo ajeno en su ruta de importación ni con generate_synthetic.py alterado; un .pyc distinto de su
    fuente o reescrito por pytest no se certifica, y uno derivable sí."""
    def must(*args):
        rc, out = git(*args)
        if rc != 0:
            raise GitError(str(rc))
        return out
    out = []
    tampered = lambda rel: (real_bytes(rel) or b'') + (b'\n# alterado\n' if rel == SBX_MODULES[1] else b'')
    res, err = sbx_eval(must, tampered)
    out.append((res is None and bool(err) and 'no se importa' in err,
                f'NB-19 SBX: módulo de compute_sbx() alterado no se importa (falla cerrado) — {err}'))
    res, err = sbx_eval(must, lister=lambda d: os.listdir(d) + (['csv.py'] if d.endswith('f34') else []))
    out.append((res is None and bool(err) and 'no se importa' in err,
                f'NB-74 SBX: archivo ajeno en una ruta de importación de compute_sbx() (falla cerrado) — {err}'))
    synth = 'docs/academico/tools/f34/generate_synthetic.py'
    res, err = sbx_eval(must, lambda rel: (real_bytes(rel) or b'') + (b'\n# alterado\n' if rel == synth else b''))
    out.append((res is None and bool(err) and 'no se importa' in err,
                f'NB-75 SBX: generate_synthetic.py alterado no se importa (falla cerrado) — {err}'))
    pyc = f'{GATE.rsplit("/", 1)[0]}/__pycache__/validate_f35sbxb.{sys.implementation.cache_tag}.pyc'
    bad = pyc_problem(pyc, load=lambda path, name: compile(b'import sklearn\n', path, 'exec', dont_inherit=True))
    out.append((bool(bad) and 'no corresponde' in bad, f'NB-76 FSY: .pyc distinto de su fuente no se certifica — {bad}'))
    bad = pyc_problem('ml-service/tests/__pycache__/test_api.cpython-312-pytest-8.3.3.pyc')
    out.append((bool(bad) and 'no derivable' in bad, f'NB-77 FSY: .pyc reescrito por pytest no se certifica — {bad}'))
    src = real_bytes(GATE) or b''
    good = pyc_problem(pyc, load=lambda path, name: compile(src, path, 'exec', dont_inherit=True))
    out.append((good is None, f'PB: .pyc derivable de su fuente se verifica y se admite — {good}'))
    # B1.4 — H01: ningún código del repositorio se ejecuta antes de verificarse. La carga útil solo marcaría sys.
    payload = b'import sys\nsys._f35sbxb_marca = True\n'
    for cid, rel in (('NB-78', 'ml-service/src/recruitment_ml/schema.py'),
                     ('NB-79', 'docs/academico/tools/f35sbx/f35sbx_scope.py')):
        res, err = sbx_eval(must, lambda r, rel=rel: (real_bytes(r) or b'') + (b'\n' + payload if r == rel else b''))
        ran = getattr(sys, '_f35sbxb_marca', False)
        out.append((res is None and bool(err) and 'ni se ejecuta' in err and not ran,
                    f'{cid} SBX: {rel} alterado no se ejecuta (marcador ausente: {not ran}) — {err}'))
    planted = {'docs/academico/tools/f34/csv.py', 'docs/academico/tools/f35sbx/json.py'}
    res, err = sbx_eval(must, exists=lambda p: os.path.lexists(p) or os.path.relpath(p, ROOT).replace(os.sep, '/') in planted)
    out.append((res is None and bool(err) and 'ni se ejecuta' in err,
                f'NB-80 SBX: módulo plantado que sombrearía una importación de compute_sbx() (falla cerrado) — {err}'))
    verified, err = verify_inventory(must)
    if verified:
        bad = dict(verified)
        bad['docs/academico/tools/f34a/validate_f34a.py'] += b"\nexec('x = 1')\n"
        _, problems = exec_graph(bad)
        out.append((any('ejecución dinámica' in p for p in problems),
                    f'NB-81 SBX: ejecución dinámica en el grafo estático no verificable — {problems[:1]}'))
    else:
        out.append((False, f'NB-81 SBX: inventario no verificable — {err}'))
    fake = type(sys)('f35sbxb_modulo_falso')
    fake.__file__ = os.path.join(ROOT, 'docs', 'academico', 'tools', 'f34', 'csv.py')
    sys.modules['f35sbxb_modulo_falso'] = fake
    try:
        res, err = sbx_eval(must)
    finally:
        sys.modules.pop('f35sbxb_modulo_falso', None)
    out.append((res is None and bool(err) and 'ya cargados' in err,
                f'NB-82 SBX: módulo del repositorio ya cargado no se acepta — {err}'))
    refused = False
    with ExecGuard({}) as guard:
        sys.path.insert(0, os.path.join(ROOT, 'docs', 'academico', 'tools', 'f34'))
        try:
            importlib.util.find_spec('generate_synthetic')
        except ImportError:
            refused = True
    out.append((refused and bool(guard.refused) and 'generate_synthetic' not in sys.modules,
                f'NB-83 SBX: la guarda rechaza código del repositorio no verificado antes de ejecutarlo — {guard.refused[:1]}'))
    return out


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    checks = []
    add = lambda ok, msg: checks.append((bool(ok), msg))
    S = collect()
    res = run_rules(S)
    for rid, viol in res.items():
        add(not viol, f'{rid}: {len(viol)} violaciones' + (f' — {viol[:3]}' if viol else ''))
    print('SBX-01..SBX-18 sobre HEAD (DH-B13):')
    for k in SBX_IDS:
        ok, detail = (S.get('sbx') or {}).get(k, (False, S.get('sbx_error') or 'no evaluable'))
        fuente, comprobacion = SBX_INFO[k]
        motivo = '' if ok else f' | motivo: {str(detail)[:120]}'
        print(f'  {k} | {"PASS" if ok else "FAIL"} | fuente: {fuente} | comprobación: {comprobacion}{motivo}')
    for cid, rule, what, mut in CASES:
        try:
            T = mut(S)
        except (AssertionError, KeyError, IndexError, TypeError, AttributeError, ValueError) as e:
            add(False, f'{cid}: la mutación no se pudo aplicar ({e.__class__.__name__}: {e})')
            continue
        add(run_rules(T)[rule], f'{cid} detectado por {rule}: {what}')
    try:
        for ok, msg in integrity_cases(S):
            add(ok, msg)
    except Exception as e:          # estado Git o de archivos no verificable: los casos de integridad fallan cerrados
        add(False, f'NB-19 y NB-74..NB-83: casos de integridad no evaluables ({e.__class__.__name__}): falla cerrado')
    for text in LEGIT_TEXTS:
        try:
            rc = run_rules(doc_add(text)(S))['CNT']
            rg = run_rules(gov_add(text)(S))['GOV']
        except (KeyError, TypeError, AttributeError, ValueError) as e:   # estado incompleto: falla cerrado
            add(False, f'PB: control no aplicable sobre un estado no verificable ({e.__class__.__name__}): «{text}»')
            continue
        add(not rc and not rg, f'PB: texto legítimo aceptado por CNT y GOV: «{text}» {(rc + rg)[:1]}')
    fallas = [m for ok, m in checks if not ok]
    for m in fallas:
        print('FALLA', m)
    print(f'validate_f35sbxb: {len(checks) - len(fallas)} comprobaciones correctas, {len(fallas)} fallas')
    sys.exit(1 if fallas else 0)


if __name__ == '__main__':
    main()
