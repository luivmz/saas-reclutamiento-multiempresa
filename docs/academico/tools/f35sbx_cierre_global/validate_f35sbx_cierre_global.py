"""F35-SBX — gate sucesor del cierre global (validate_f35sbx_cierre_global.py).

Uso:  python -I docs/academico/tools/f35sbx_cierre_global/validate_f35sbx_cierre_global.py   (sin -I, se relanza)

Contrato: docs/academico/evidencia-sbx-cierre-global/F35SBX_Cierre_Global.md. Valida el cierre global de F35-SBX y su
registro en el gobierno con una transición única y monotónica (blobs de f082b41 → GC_BLOBS). Es el gate sucesor de B
sobre HEAD (B1, §5; DH-B13): verifica la identidad de la historia integrada, la integridad de A y de B desde sus anclas
y recalcula SBX-01..SBX-18 con la función verificada del gate de B1. No ejecuta los gates congelados, que siguen
valiendo anclados sobre sus anclas. El repositorio solo se lee; cada objeto Git se verifica recalculando su
identificador, y todo error, salida incompleta o estado no evaluable falla cerrado.

  ENT  intérprete aislado y sin PYTHONPATH, PYTHONHOME ni PYTHONUSERBASE; ninguna variable de Git que redirija el
       repositorio; Git sobre el repositorio de este archivo, con historia completa, sin injertos ni reemplazos.
  CTX  rama chore/f35-sbx-global-closure, develop o main; el merge f082b41, ancestro de HEAD.
  ANC  anclas registradas, de F35-SBX-A a la transición del cierre global, verificadas y ancestros de HEAD; f082b41 con
       los padres 53c0eb5 y 9ebb909 y el árbol de su ancla.
  INT  A idéntica a E (sus carpetas y los cinco validadores que adaptó) y B idéntica a 9ebb909 (sus carpetas, cierre
       terminal incluido), en f082b41, en cada commit posterior, HEAD, índice y disco.
  FLG  ningún flag en el índice.
  GOV  transición única y monotónica en las cuatro rutas de gobierno, registrada; estado efectivo en HEAD, índice y disco.
  SEM  semántica del gobierno y del documento de la capa con las piezas verificadas de B1 y R2-A: F35-SBX CERRADA Y
       CONGELADA, F36–F40 bloqueadas, F36-SBX sujeta a una autorización sucesora nueva y ningún otro estado cambiado.
  SBX  SBX-01..SBX-18 recalculados uno por uno sobre HEAD con sbx_eval() del gate de B1, cargado de su blob verificado;
       no se evalúan si FSY no pudo verificar la superficie física, porque SBX-15 la recorre y la lee.
  FSY  recorrido físico de las superficies materiales del contrato FSY de B1 (§8.3; TSBB-07), sin seguir enlaces y
       aunque Git las ignore o no las vea. Primero, todas sus carpetas, excepciones incluidas, se enumeran sin entrar
       en ningún enlace, unión ni punto de reanálisis, y todo error de enumeración falla cerrado (GC-AF-M02); después,
       cada archivo idéntico a su blob en el inventario autorizado de f082b41, igual al de la base de B1, y ningún
       archivo extra, generado, ausente ni enlace, salvo las excepciones de B1.
  RSK  los riesgos B3-AF-L01, B3-AF-L02 y B3-R3 (LOW), TC-AF-I01 (INFO) y TC-H4 (INFO), con su nivel y su estado.
  ALC  alcance exacto frente a f082b41: las cinco rutas A de la capa y las cuatro de gobierno M; sin archivos sin
       seguimiento.
  FRZ  nivel B: un único commit posterior a f082b41 completa la capa y, desde él, sus archivos no cambian. Su hash se
       deriva de Git y se registra fuera, nunca en un archivo.
  DEP  biblioteca estándar autorizada por archivo; la única ejecución dinámica es la carga verificada de los gates de B1
       y R2-A.
"""
import os
import sys

# Aislamiento antes de cualquier otra importación, como los gates anteriores: python -I, relanzado con os.spawnv.
if __name__ == '__main__' and not sys.flags.isolated:
    _argv = [sys.executable, '-I', '-B'] + (['-X', 'utf8'] if sys.flags.utf8_mode else []) + \
        [os.path.abspath(__file__)] + sys.argv[1:]
    if os.name == 'nt':
        _argv = ['"' + a.replace('"', '\\"') + '"' if (' ' in a or '\t' in a) else a for a in _argv]
    sys.exit(os.spawnv(os.P_WAIT, sys.executable, _argv))

_REPO = os.path.normcase(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..')))
sys.path[:] = [p for p in sys.path if not (os.path.normcase(os.path.abspath(p or os.curdir)) + os.sep).startswith(
    _REPO + os.sep)]
sys.dont_write_bytecode = True

import ast  # noqa: E402
import hashlib  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
import types  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))

# ---------------------------------------------------------------- anclas registradas (todas existían antes que este archivo)
A_ANCHOR = '61f94e23fc30b00a848a4558830b6d65f81dff87'            # commit E de F35-SBX-A
B0_CLOSURE = 'cc634eb9dcc5c0cc0d77b911bb3815182b8319c2'         # cierre de B0
B1_ANCHOR = '8e94a60274fe39ebda3e9961bc58036b389dfc00'          # ancla auditada de B1
B1_CLOSURE = '3d9b78307684a0dfb093e31d28fde290b2b1cb4a'         # cierre de B1-FREEZE
CANDIDATE = '2472fd6fadfc0634ec68cbcb76cfc9fbfe105194'          # candidato de B2
FREEZE = '9961d2d65ed51a17c14aae5db0edb7d71c622c22'             # B2-FREEZE
SUCCESSOR = '9d6fb157bb818574217e3675da1849e8d1010962'          # gate sucesor de B2 (AF-M01)
SUCCESSOR_FREEZE = '89694244b81b0bd84dbe6ae5d04b5c7a198bafef'   # B2-SUCCESSOR-FREEZE
GOV_CLOSURE = '363273ead5794ea7a2dba74c011a0efd6d59e906'        # B2-GOVERNMENT-CLOSURE
R2A_COMPLETION = 'ad193f9565bf23246fadb9f85fc0ceddf8ddf698'     # R2-A: cierre formal de B2
B3_ANCHOR = '8d39d0e547821f7d6f63dc12b9c01803f985d797'          # B3
B3_MERGE = '53c0eb55a8f64f5576c43c2bfb5dccf095e30412'           # integración de B3 en develop
TC_TRANSITION = '5517a12a4d35c6d8c3281ace2f072ddc692f16f2'      # transición del cierre terminal de F35-SBX-B
TC_ANCHOR = '9ebb90929f34079b42e88e21e144f80182ba7565'          # cierre terminal: ancla aprobada; B congelada
BASE = 'f082b4165ca756659b998716e2647494a3ec7be6'               # integración del cierre terminal en develop; base
BASE_TREE = '7e122321b88b145f832f3c0c7a69a8798cb243fb'          # árbol de TC_ANCHOR y de sus merges
# Commit de la transición de gobierno del cierre global. Se registra después de que exista, nunca en el propio commit.
GC_TRANSITION = 'c73611cb992dffd6e4be1fe49bce8b03b53506cd'
ANCHORS = (A_ANCHOR, B0_CLOSURE, B1_ANCHOR, B1_CLOSURE, CANDIDATE, FREEZE, SUCCESSOR, SUCCESSOR_FREEZE, GOV_CLOSURE,
           R2A_COMPLETION, B3_ANCHOR, B3_MERGE, TC_TRANSITION, TC_ANCHOR, BASE)

BRANCH = 'chore/f35-sbx-global-closure'
BRANCHES = (BRANCH, 'develop', 'main')
BASELINE = 'docs/academico/ACADEMIC_BASELINE.md'
GOV_PATHS = ('CLAUDE.md', 'docs/PROGRESS.md', BASELINE, 'README.md')
BASE_BLOBS = {'CLAUDE.md': 'd4ba0968e6ebbcaca667d47954db46f7088fae9a',
              'docs/PROGRESS.md': 'a6322415e7705395dde1e185a3e501155f1989f5',
              BASELINE: 'e9fb4bbbc1534802fc196cca021eeeef69414571',
              'README.md': 'a4cecb0fe904a698228f5c06910d00970b45ffa1'}
GC_BLOBS = {'CLAUDE.md': '2e988f22864ad86b05395d0d8a91110d9631c4a3',
            'docs/PROGRESS.md': '200355350414dceaac1ab39ba835f1e7c18a662d',
            BASELINE: '5e523302279948389c78cb9dca70b82f5c7b92e4',
            'README.md': '0ed030e53d49f2c8a5f1dc5fca1269b6109020a3'}

LAYER_DOCS = 'docs/academico/evidencia-sbx-cierre-global'
LAYER_TOOLS = 'docs/academico/tools/f35sbx_cierre_global'
DOC = LAYER_DOCS + '/F35SBX_Cierre_Global.md'
VALIDATOR = LAYER_TOOLS + '/validate_f35sbx_cierre_global.py'
TESTS = LAYER_TOOLS + '/test_f35sbx_cierre_global.py'
FIX_DOC = LAYER_DOCS + '/F35SBX_Cierre_Global_GC-AF-M01.md'       # registro de la corrección GC-AF-M01
M02_DOC = LAYER_DOCS + '/F35SBX_Cierre_Global_GC-AF-M02.md'       # registro de la corrección GC-AF-M02
LAYER_FILES = (DOC, VALIDATOR, TESTS, FIX_DOC, M02_DOC)
LAYER_DIRS = {LAYER_DOCS: ('F35SBX_Cierre_Global.md', 'F35SBX_Cierre_Global_GC-AF-M01.md',
                           'F35SBX_Cierre_Global_GC-AF-M02.md'),
              LAYER_TOOLS: ('test_f35sbx_cierre_global.py', 'validate_f35sbx_cierre_global.py')}
SCOPE = {DOC: 'A', VALIDATOR: 'A', TESTS: 'A', FIX_DOC: 'A', M02_DOC: 'A', **{p: 'M' for p in GOV_PATHS}}

# ---------------------------------------------------------------- capas congeladas: A desde E y B desde su cierre terminal
A_DIRS = ('docs/academico/evidencia-sbx', 'docs/academico/tools/f35sbx')
A_FILES = ('docs/academico/tools/f30/validate_f30.py', 'docs/academico/tools/f33/validate_f33.py',
           'docs/academico/tools/f34/validate_f34.py', 'docs/academico/tools/f34b/validate_f34b.py',
           'docs/academico/tools/f34e/validate_f34e.py')
B_DIRS = tuple(f'docs/academico/{d}' for d in (
    'evidencia-sbx-b', 'evidencia-sbx-b-freeze', 'evidencia-sbx-b2', 'evidencia-sbx-b2-freeze', 'evidencia-sbx-b2-sucesor',
    'evidencia-sbx-b2-sucesor-freeze', 'evidencia-sbx-b2-cierre-gobierno', 'evidencia-sbx-b2-cierre-formal',
    'evidencia-sbx-b3', 'evidencia-sbx-b-cierre-terminal', 'tools/f35sbxb', 'tools/f35sbxb_freeze', 'tools/f35sbxb2',
    'tools/f35sbxb2_freeze', 'tools/f35sbxb2_sucesor', 'tools/f35sbxb2_sucesor_freeze', 'tools/f35sbxb2_cierre_gobierno',
    'tools/f35sbxb2_cierre_formal', 'tools/f35sbxb3', 'tools/f35sbxb_cierre_terminal'))
FROZEN = (('A', A_ANCHOR, A_DIRS, A_FILES), ('B', TC_ANCHOR, B_DIRS, ()))
VERIFIED = {'b1': (B1_ANCHOR, 'docs/academico/tools/f35sbxb/validate_f35sbxb.py'),
            'r2a': (R2A_COMPLETION, 'docs/academico/tools/f35sbxb2_cierre_formal/validate_f35sbxb2_cierre_formal.py')}

# ---------------------------------------------------------------- GOV: lista cerrada de reemplazos literales (§3.2)
_GC_STATE = ('F35-SBX CERRADA Y CONGELADA solo como sandbox académico y sintético: F35-SBX-A y F35-SBX-B cerradas e '
             'integradas.')
_GC_F36 = ('F36–F40 siguen BLOQUEADAS: ninguna F36-SBX empieza sin una autorización sucesora nueva, con su propia '
           'gobernanza.')
_GC_RECORD = 'F35-SBX está CERRADA Y CONGELADA, con su cierre global registrado en '
_README_STATE = ('F35-SBX CERRADA Y CONGELADA solo como sandbox académico y sintético: F35-SBX-A y F35-SBX-B cerradas e '
                 'integradas, con su cierre global registrado en ')
_README_F36 = ('F36–F40 siguen BLOQUEADAS y ninguna F36-SBX empieza sin una autorización sucesora nueva, con su '
               'propia gobernanza.')
_HEADER_OLD = ('Última actualización: 2026-10-21 (F34E CERRADA; G0 real NO APROBADA; G0-SBX APROBADA CON RESTRICCIONES; '
               'F35-SBX sintética HABILITADA; F35-SBX-A CERRADA E INTEGRADA; B0 CERRADA E INTEGRADA; F35-SBX-B CERRADA, '
               'CONGELADA E INTEGRADA: B1, B2 y B3 CERRADAS E INTEGRADAS).')
GC_HEADER = ('F35-SBX CERRADA Y CONGELADA solo como sandbox académico y sintético: F35-SBX-A, B0 y F35-SBX-B CERRADAS E '
             'INTEGRADAS; F36–F40 BLOQUEADAS).')
_HEADER_NEW = ('Última actualización: 2026-10-24 (F34E CERRADA; G0 real NO APROBADA; G0-SBX APROBADA CON RESTRICCIONES; '
               + GC_HEADER)
_HISTORY = ('El 21/10/2026 pasó a F35-SBX-B cerrada, congelada e integrada, con B3 auditada e integrada y su cierre '
            'terminal registrado.')


def _tail(prefix):
    before = (f'[`evidencia-sbx-b-cierre-terminal`]({prefix}evidencia-sbx-b-cierre-terminal/F35SBXB_Cierre_Terminal.md). '
              f'F36–F40 siguen BLOQUEADAS.')
    after = (f'[`evidencia-sbx-b-cierre-terminal`]({prefix}evidencia-sbx-b-cierre-terminal/F35SBXB_Cierre_Terminal.md). '
             f'{_GC_RECORD}[`evidencia-sbx-cierre-global`]({prefix}evidencia-sbx-cierre-global/F35SBX_Cierre_Global.md). '
             f'{_GC_F36}')
    return before, after


_STATE_LINE = ('- F35-SBX = HABILITADA\n', '- F35-SBX = CERRADA Y CONGELADA\n')
_EXCLUSIVE = ('F35-SBX exclusivamente sintético.', _GC_STATE)
GC_DELTA_TEXT = {
    'CLAUDE.md': [_STATE_LINE, _EXCLUSIVE, _tail('docs/academico/')],
    'docs/PROGRESS.md': [_STATE_LINE, _EXCLUSIVE, _tail('academico/'), (_HEADER_OLD, _HEADER_NEW),
                         (_HISTORY, _HISTORY + ' El 24/10/2026 pasó a F35-SBX cerrada y congelada, con su cierre global '
                                               'registrado.')],
    BASELINE: [_STATE_LINE, _EXCLUSIVE, _tail('')],
    'README.md': [_STATE_LINE,
                  ('F35-SBX exclusivamente sintético. F35-SBX AÚN NO INICIADA.',
                   _README_STATE + '[`evidencia-sbx-cierre-global`]'
                                   '(docs/academico/evidencia-sbx-cierre-global/F35SBX_Cierre_Global.md).'),
                  ('Próximo trabajo autorizado aquí: handoff macOS, no iniciar F35-SBX.', _README_F36)]}

# ---------------------------------------------------------------- SEM (§3.6)
RF_STATE = 'RF-23 sigue humana; RF-29 sigue experimental/informativa.'
B_CLOSED = 'F35-SBX-B CERRADA, CONGELADA E INTEGRADA solo como sandbox sintético'
GC_STATES = ['- G0 real = NO APROBADA', '- G0-09 = CUMPLIDO', '- G0-14 = CUMPLIDO', '- G0-02 = PENDIENTE EXTERNO',
             '- G0-03 = PENDIENTE EXTERNO', '- G0-12 = PENDIENTE EXTERNO', '- ADR-005 = PROPUESTA',
             '- G0-SBX = APROBADA CON RESTRICCIONES', '- F35 productiva = BLOQUEADA', '- F35-SBX = CERRADA Y CONGELADA',
             '- F36–F40 = BLOQUEADAS', '- Alcance C = BLOQUEADO', '- Datos reales = PROHIBIDOS']
GC_REQUIRED = {'CLAUDE.md': (_GC_STATE, _GC_RECORD, _GC_F36, B_CLOSED, RF_STATE),
               'docs/PROGRESS.md': (_GC_STATE, _GC_RECORD, _GC_F36, B_CLOSED, RF_STATE),
               BASELINE: (_GC_STATE, _GC_RECORD, _GC_F36, B_CLOSED, RF_STATE),
               'README.md': (_README_STATE, _README_F36, RF_STATE)}
GC_STALE = ('F35-SBX = HABILITADA', 'F35-SBX exclusivamente sintético', 'F35-SBX AÚN NO INICIADA', 'no iniciar F35-SBX',
            'F35-SBX sintética HABILITADA', 'F35-SBX-B INICIADA', 'F35-SBX-B NO INICIADA')
_SUBJECTS = r'(?:f35-sbx|f35-sbx-a|f35-sbx-b|b1|b2|b3)'
GC_FORBIDDEN_RX = re.compile(r'(?<![\w-])' + _SUBJECTS + r'(?![\w-])((?:\s+[a-z0-9-]+){0,3}?)\s*(?:=|:|\s)\s*'
                             r'(productiv\w*|aprobad\w*|publicad\w*|desplegad\w*)\b')
GC_REOPEN_RX = re.compile(r'(?<![\w-])' + _SUBJECTS + r'(?![\w-])((?:\s+[a-z0-9-]+){0,3}?)\s*(?:=|:|\s)\s*'
                          r'(reabiert\w*|reabr\w*|reapert\w*|pendiente\w*|abiert\w*|desarroll\w*|candidat\w*|'
                          r'no\s+cerrad\w*|iniciad\w*|habilitad\w*)\b')
FENCE_RX = re.compile(r'^```.*?^```[ \t]*$', re.M | re.S)
LIMITS = ('- no aprueba la G0 real ni sustituye su evidencia externa;',
          '- no habilita la F35 productiva ni ninguna integración productiva;',
          '- no habilita F36 ni ninguna fase posterior, tampoco en sandbox;',
          '- no habilita F36-SBX: ninguna F36-SBX empieza sin una autorización sucesora nueva, con su propia gobernanza;',
          '- no permite datos reales;',
          '- no permite puntuar ni clasificar ni recomendar candidatos;',
          '- no permite la selección automática;',
          '- no habilita biometría ni inferencias de emoción, personalidad, honestidad, inteligencia o estrés;',
          '- no habilita el alcance C;',
          '- no habilita OCR ni parsing ni embeddings ni búsqueda semántica;',
          '- no cambia RF-23, que sigue siendo la decisión final humana del Aprobador/Dirección;',
          '- no cambia RF-29, que sigue experimental e informativo;',
          '- no revoca ni amplía G0-SBX, que sigue APROBADA CON RESTRICCIONES;',
          '- no reutiliza ningún artefacto SBX en trabajo real, que exige SAL-01 a SAL-05.')

# ---------------------------------------------------------------- RSK (§3.7)
_ACCEPTED = 'Aceptado, no bloqueante'
RISKS = (('B3-AF-L01', 'LOW', 'Comprobante de purga no completamente independiente del pipeline', _ACCEPTED),
         ('B3-AF-L02', 'LOW', 'La comprobación CNF no demuestra por sí sola la unicidad global de `audit_id`', _ACCEPTED),
         ('B3-R3', 'LOW', 'Los diagnósticos de los gates históricos profundamente anidados pueden quedar truncados',
          _ACCEPTED),
         ('TC-AF-I01', 'INFO', 'SEM no es un detector universal de lenguaje natural', _ACCEPTED),
         ('TC-H4', 'INFO', 'conservaba en su bloque «Estado vigente F34E» la frase «F35-SBX AÚN NO INICIADA»',
          'Corregido por la transición de este incremento (§3.2)'))
RISK_ALTERED_RX = re.compile(r'(resuelt|corregid|descartad|\bMEDIUM\b|\bHIGH\b|\bBLOCKER\b)', re.IGNORECASE)

# ---------------------------------------------------------------- DEP, entorno y orden de las reglas
DEP_ALLOWED = {VALIDATOR: frozenset({'ast', 'hashlib', 'os', 're', 'subprocess', 'sys', 'types'}),
               TESTS: frozenset({'os', 'subprocess', 'sys'})}
LOADERS = {VALIDATOR: 'load_verified'}      # única función con ejecución dinámica: los gates de B1 y R2-A verificados
DYNAMIC_CODE = frozenset({'__import__', 'compile', 'eval', 'exec'})
ORDER = ('ENT', 'CTX', 'ANC', 'INT', 'FLG', 'GOV', 'SEM', 'SBX', 'FSY', 'RSK', 'ALC', 'FRZ', 'DEP')
PLANES = ('HEAD', 'árbol', 'índice')
TIMEOUT = 3600
REDIRECTING = ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'GIT_OBJECT_DIRECTORY', 'GIT_ALTERNATE_OBJECT_DIRECTORIES',
               'GIT_COMMON_DIR', 'GIT_NAMESPACE', 'GIT_REPLACE_REF_BASE', 'GIT_NO_REPLACE_OBJECTS', 'GIT_GRAFT_FILE',
               'GIT_SHALLOW_FILE', 'GIT_CEILING_DIRECTORIES', 'GIT_DISCOVERY_ACROSS_FILESYSTEM',
               'GIT_LITERAL_PATHSPECS', 'GIT_GLOB_PATHSPECS', 'GIT_NOGLOB_PATHSPECS', 'GIT_ICASE_PATHSPECS')
GIT_ENV = {k: v for k, v in os.environ.items() if not k.upper().startswith('GIT_')}
GIT = ('git', '--no-replace-objects', '--literal-pathspecs')


class GitError(Exception):
    pass


ERRORS = (GitError, OSError, ValueError, KeyError, TypeError, IndexError, AttributeError, SyntaxError,
          UnicodeDecodeError, subprocess.TimeoutExpired)


def git(*args):
    try:
        p = subprocess.run([*GIT, *args], cwd=ROOT, env=GIT_ENV, capture_output=True, timeout=TIMEOUT)
    except OSError as e:
        raise GitError(f'git no ejecutable ({e.__class__.__name__})')
    if p.returncode != 0:
        raise GitError(f'git {" ".join(args[:2])} → {p.returncode}')
    return p.stdout


def is_oid(value):
    return isinstance(value, str) and len(value) == 40 and all(c in '0123456789abcdef' for c in value)


def blob_id(data):
    return hashlib.sha1(b'blob %d\x00' % len(data) + data).hexdigest()


def name_status(raw):
    parts = raw.split(b'\x00')
    return {parts[i + 1].decode('utf-8'): parts[i].decode('ascii') for i in range(0, len(parts) - 1, 2) if parts[i]}


# ---------------------------------------------------------------- objetos Git verificados (técnica de B2-FREEZE)
class Objects:
    """git cat-file --batch: cada objeto leído se verifica recalculando su identificador antes de usarlo."""

    def __init__(self):
        self.raw, self.trees = {}, {}
        try:
            self.proc = subprocess.Popen([*GIT, 'cat-file', '--batch'], cwd=ROOT, env=GIT_ENV, stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        except OSError as e:
            raise GitError(f'git no ejecutable ({e.__class__.__name__})')

    def read(self, oid):
        if oid in self.raw:
            return self.raw[oid]
        if not is_oid(oid):
            raise GitError(f'identificador de objeto no válido: {oid!r}')
        try:
            self.proc.stdin.write(oid.encode('ascii') + b'\n')
            self.proc.stdin.flush()
            header = self.proc.stdout.readline().split()
            if len(header) != 3 or header[0] != oid.encode('ascii'):
                raise GitError(f'objeto {oid[:12]} ausente')
            kind, size = header[1], int(header[2])
            data, end = self.proc.stdout.read(size), self.proc.stdout.read(1)
        except (OSError, ValueError) as e:
            raise GitError(f'lectura del objeto {oid[:12]} interrumpida ({e.__class__.__name__})')
        if len(data) != size or end != b'\n' or hashlib.sha1(kind + b' %d\x00' % size + data).hexdigest() != oid:
            raise GitError(f'el objeto {oid[:12]} no corresponde a su identificador')
        self.raw[oid] = (kind.decode('ascii'), data)
        return self.raw[oid]

    def close(self):
        for stream in (self.proc.stdin, self.proc.stdout):
            try:
                stream.close()
            except OSError:
                pass
        try:
            self.proc.wait(timeout=30)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            self.proc.wait()


def commit_parts(objs, oid):
    """(árbol, padres) de un commit verificado, leídos como los lee Git: los padres siguen a la línea del árbol."""
    kind, data = objs.read(oid)
    if kind != 'commit':
        raise GitError(f'{oid[:12]} no es un commit')
    lines = data.split(b'\n\n', 1)[0].split(b'\n')
    tree = lines[0][5:].decode('ascii') if lines[0].startswith(b'tree ') else ''
    parents = []
    for line in lines[1:]:
        if not line.startswith(b'parent '):
            break
        parents.append(line[7:].decode('ascii'))
    if not is_oid(tree) or not all(is_oid(p) for p in parents):
        raise GitError(f'commit {oid[:12]} malformado')
    return tree, parents


def tree_items(objs, oid):
    if oid not in objs.trees:
        kind, data = objs.read(oid)
        if kind != 'tree':
            raise GitError(f'{oid[:12]} no es un árbol')
        out, i = {}, 0
        while i < len(data):
            space = data.index(b' ', i)
            nul = data.index(b'\x00', space)
            mode = data[i:space].decode('ascii').zfill(6)
            name, child = data[space + 1:nul].decode('utf-8'), data[nul + 1:nul + 21].hex()
            if len(child) != 40 or not name or name in out:
                raise GitError(f'árbol {oid[:12]} malformado')
            out[name] = (mode, 'tree' if mode == '040000' else 'commit' if mode == '160000' else 'blob', child)
            i = nul + 21
        objs.trees[oid] = out
    return objs.trees[oid]


def entry(objs, tree, path):
    parts = path.split('/')
    for k, name in enumerate(parts):
        found = tree_items(objs, tree).get(name)
        if found is None or (k < len(parts) - 1 and found[1] != 'tree'):
            return None
        if k == len(parts) - 1:
            return found
        tree = found[2]
    return None


def listing(objs, tree, folder):
    top = entry(objs, tree, folder)
    if top is None or top[1] != 'tree':
        return None
    out, stack = {}, [('', top[2])]
    while stack:
        prefix, oid = stack.pop()
        for name, found in tree_items(objs, oid).items():
            if found[1] == 'tree':
                stack.append((prefix + name + '/', found[2]))
            else:
                out[prefix + name] = found
    return out


def listing_diff(folder, found, want):
    if found is None:
        return [folder + '/']
    return [f'{folder}/{rel}' for rel in sorted(set(found) | set(want)) if found.get(rel) != want.get(rel)]


def blob_text(objs, found):
    if found is None or found[:2] != ('100644', 'blob'):
        raise GitError('se esperaba un blob regular 100644')
    kind, data = objs.read(found[2])
    if kind != 'blob':
        raise GitError(f'{found[2][:12]} no es un blob')
    return data


def blob_at(objs, commit, path):
    return blob_text(objs, entry(objs, commit_parts(objs, commit)[0], path))


def ancestry(objs, head):
    """{commit: padres} de todos los ancestros de head, incluido, desde objetos verificados."""
    parents, stack = {}, [head]
    while stack:
        commit = stack.pop()
        if commit not in parents:
            parents[commit] = commit_parts(objs, commit)[1]
            stack.extend(p for p in parents[commit] if p not in parents)
    return parents


def descendants(parents, base):
    """Commits del grafo que descienden de base, sin incluirla (lo mismo que rev-list --ancestry-path base..head)."""
    children = {}
    for commit, ps in parents.items():
        for p in ps:
            children.setdefault(p, []).append(commit)
    out, stack = set(), [base]
    while stack:
        for child in children.get(stack.pop(), ()):
            if child not in out:
                out.add(child)
                stack.append(child)
    return out


def topological(parents):
    """Commits de parents ordenados de modo que cada uno sigue a sus padres."""
    order, state = [], {}
    for start in sorted(parents):
        stack = [(start, False)]
        while stack:
            commit, done = stack.pop()
            if done:
                state[commit] = 2
                order.append(commit)
                continue
            if state.get(commit):
                continue
            state[commit] = 1
            stack.append((commit, True))
            stack.extend((p, False) for p in parents.get(commit, ()) if p in parents and not state.get(p))
    return order


# ---------------------------------------------------------------- índice y disco
def index_entries(paths):
    found = {}
    for item in git('ls-files', '-s', '-z', '--', *paths).split(b'\x00'):
        if item:
            meta, _, path = item.partition(b'\t')
            mode, oid, stage = meta.decode('ascii').split()
            found.setdefault(path.decode('utf-8'), []).append((mode, oid, stage))
    return found


def index_problems(want, paths, label):
    expected = {p: [(e[0], e[2], '0')] for p, e in want.items()}
    found = index_entries(paths)
    diff = sorted(p for p in set(expected) | set(found) if expected.get(p) != found.get(p))
    return [f'índice distinto {label} (entrada ausente, extra, en conflicto o con otro modo, tipo o blob): '
            f'{diff[:5]}'] if diff else []


def linked(full):
    return os.path.islink(full) or bool(getattr(os.path, 'isjunction', lambda _: False)(full))


def disk_path(rel):
    parts = rel.split('/')
    if any(linked(os.path.join(ROOT, *parts[:k])) for k in range(1, len(parts) + 1)):
        return None
    return os.path.join(ROOT, *parts)


def disk_bytes(rel):
    full = disk_path(rel)
    if full is None or not os.path.isfile(full):
        return None
    try:
        with open(full, 'rb') as f:
            return f.read()
    except OSError:
        return None


def file_problems(rel, want):
    data = disk_bytes(rel)
    if data is None:
        return [f'{rel}: ausente, enlace, objeto especial o ilegible en el disco']
    if blob_id(data) != want[2]:
        return [f'{rel}: bytes del disco distintos del blob esperado']
    if os.name != 'nt' and os.stat(disk_path(rel)).st_mode & 0o111:
        return [f'{rel}: permiso de ejecución en el disco (se espera {want[0]})']
    return []


def disk_folder(folder, want):
    """Carpeta del disco con exactamente los archivos esperados (también ignorados, ocultos y __pycache__), regulares,
    sin enlaces y con sus blobs. Solo se admiten las subcarpetas que contienen archivos esperados."""
    base = disk_path(folder)
    if base is None or not os.path.isdir(base):
        return [f'{folder}: ausente, enlace o no es un directorio']
    out, found, stack = [], set(), [('', base)]
    while stack:
        prefix, path = stack.pop()
        try:
            with os.scandir(path) as it:
                items = sorted(it, key=lambda x: x.name)
        except OSError as e:
            out.append(f'{folder}/{prefix}: ilegible ({e.__class__.__name__})')
            continue
        for item in items:
            rel = prefix + item.name
            if linked(item.path):
                out.append(f'{folder}/{rel}: enlace')
            elif item.is_dir(follow_symlinks=False):
                if not any(name.startswith(rel + '/') for name in want):
                    out.append(f'{folder}/{rel}: carpeta inesperada')
                stack.append((rel + '/', item.path))
            elif item.is_file(follow_symlinks=False):
                found.add(rel)
            else:
                out.append(f'{folder}/{rel}: objeto especial')
    extra, missing = sorted(found - set(want)), sorted(set(want) - found)
    if extra or missing:
        out.append(f'{folder}: contenido del disco distinto del esperado: extra={extra[:3]} faltan={missing[:3]}')
    for rel in sorted(found & set(want)):
        out += file_problems(f'{folder}/{rel}', want[rel])
    return out


def scope_delta(base, scope):
    """Por plano, la diferencia simétrica entre el alcance observado frente a base y el enumerado."""
    out = {}
    for plane, args in (('HEAD', ('diff', '--name-status', '--no-renames', '-z', base, 'HEAD')),
                        ('árbol', ('diff', '--name-status', '--no-renames', '-z', base)),
                        ('índice', ('diff', '--cached', '--name-status', '--no-renames', '-z', base))):
        out[plane] = set(name_status(git(*args)).items()) ^ set(scope.items())
    return out


def untracked():
    return [x for x in git('ls-files', '--others', '--exclude-standard', '-z').decode('utf-8').split('\x00') if x]


def load_verified(objs, name):
    """Un gate congelado desde los bytes de su blob en su ancla, verificado al leerlo; nunca desde el disco. Es la
    única ejecución dinámica de este gate: el de B1 (SBX y piezas de SEM) y el de R2-A (piezas de SEM)."""
    commit, rel = VERIFIED[name]
    data = blob_at(objs, commit, rel)
    path = os.path.join(ROOT, *rel.split('/'))
    module = types.ModuleType(f'f35sbx_gate_{name}_verificado_gc')
    module.__file__ = path
    exec(compile(data, path, 'exec', dont_inherit=True), module.__dict__)
    return module


# ---------------------------------------------------------------- ENT, CTX y ANC
def ent_problems():
    out = []
    if not sys.flags.isolated:
        out.append('intérprete no aislado: se exige python -I')
    out += [f'{name} definida: el intérprete podría cargar código ajeno' for name in
            ('PYTHONPATH', 'PYTHONHOME', 'PYTHONUSERBASE') if os.environ.get(name)]
    hostile = sorted(name for name in os.environ if name.upper() in REDIRECTING)
    if hostile:
        out.append(f'variables de Git que redirigen el repositorio, el índice o los objetos: {hostile}')
    if not os.path.samefile(git('rev-parse', '--show-toplevel').decode('utf-8').strip(), ROOT):
        out.append('la raíz del repositorio no es la de este gate')
    shallow = git('rev-parse', '--is-shallow-repository').strip() != b'false'
    if shallow:
        out.append('repositorio superficial: la historia no es completa')
    grafts = git('rev-parse', '--git-path', 'info/grafts').decode('utf-8').strip()
    if os.path.lexists(grafts if os.path.isabs(grafts) else os.path.join(ROOT, grafts)):
        out.append('injertos en info/grafts: Git mostraría otra historia')
    replaced = [x for x in git('for-each-ref', '--format=%(refname)', 'refs/replace/').decode('utf-8').splitlines() if x]
    if replaced:
        out.append(f'objetos de reemplazo en refs/replace ({len(replaced)}): Git mostraría otros objetos')
    head = git('rev-parse', '--verify', '-q', 'HEAD^{commit}').decode('ascii').strip()
    if not is_oid(head):
        raise GitError('HEAD no es un commit')
    return out, head, shallow


def current_branch():
    p = subprocess.run([*GIT, 'symbolic-ref', '-q', '--short', 'HEAD'], cwd=ROOT, env=GIT_ENV, capture_output=True,
                       timeout=TIMEOUT)
    if p.returncode not in (0, 1):
        raise GitError(f'git symbolic-ref → {p.returncode}')
    return p.stdout.decode('utf-8').strip() if p.returncode == 0 else None


def ctx_problems(branch, parents):
    out = []
    if branch not in BRANCHES:
        out.append(f'rama no permitida o HEAD separado: «{branch or "HEAD separado"}»')
    if BASE not in parents:
        out.append(f'el merge de integración {BASE[:12]} no es ancestro de HEAD')
    return out


def anc_problems(objs, parents):
    out = []
    for commit in ANCHORS:
        commit_parts(objs, commit)
        if commit not in parents:
            out.append(f'el ancla registrada {commit[:12]} no es ancestro de HEAD')
    tree, ps = commit_parts(objs, BASE)
    if ps != [B3_MERGE, TC_ANCHOR]:
        out.append(f'el merge {BASE[:12]} no tiene como padres {B3_MERGE[:12]} y {TC_ANCHOR[:12]}')
    if tree != BASE_TREE or commit_parts(objs, TC_ANCHOR)[0] != BASE_TREE:
        out.append(f'el merge {BASE[:12]} o su ancla {TC_ANCHOR[:12]} no tienen el árbol registrado {BASE_TREE[:12]}')
    return out


# ---------------------------------------------------------------- INT y FLG
def frozen_layers(objs):
    """{etiqueta: (ancla, {carpeta: listado del árbol del ancla}, {archivo: entrada del ancla})}."""
    layers = {}
    for label, anchor, folders, files in FROZEN:
        root = commit_parts(objs, anchor)[0]
        dirs = {folder: listing(objs, root, folder) for folder in folders}
        single = {path: entry(objs, root, path) for path in files}
        if any(found is None or not found or any(e[:2] != ('100644', 'blob') for e in found.values())
               for found in dirs.values()) or any(e is None or e[:2] != ('100644', 'blob') for e in single.values()):
            raise GitError(f'capa {label}: sus rutas no son archivos regulares en {anchor[:12]}')
        layers[label] = (anchor, dirs, single)
    return layers


def int_problems(objs, parents):
    out = []
    commits = sorted({BASE} | descendants(parents, BASE)) if BASE in parents else []
    for label, (anchor, dirs, single) in frozen_layers(objs).items():
        bad = []
        for commit in commits:
            root = commit_parts(objs, commit)[0]
            diff = [x for folder, files in dirs.items() for x in listing_diff(folder, listing(objs, root, folder), files)]
            diff += [path for path, want in single.items() if entry(objs, root, path) != want]
            if diff:
                bad.append(f'{commit[:12]}: {diff[:2]}')
        if bad:
            out.append(f'capa {label} distinta de su ancla {anchor[:12]} (modificada, eliminada, renombrada, con otro '
                       f'modo o con archivos extra, aunque se restaure): {bad[:3]}')
        files = {f'{folder}/{rel}': e for folder, found in dirs.items() for rel, e in found.items()}
        files.update(single)
        out += index_problems(files, list(dirs) + list(single), f'de la capa {label}')
        for folder, found in dirs.items():
            out += [f'capa {label}: {x}' for x in disk_folder(folder, found)]
        for path, want in single.items():
            out += [f'capa {label}: {x}' for x in file_problems(path, want)]
    return out


def flg_problems():
    flagged = [item.decode('utf-8', 'replace') for item in git('ls-files', '-v', '-z').split(b'\x00')
               if item and not item.startswith(b'H ')]
    return [f'flags en el índice (assume-unchanged, skip-worktree o conflictos): {flagged[:5]}'] if flagged else []


# ---------------------------------------------------------------- GOV: transición única y monotónica
def gov_entries(objs, commit):
    root = commit_parts(objs, commit)[0]
    return {p: entry(objs, root, p) for p in GOV_PATHS}


def governance(objs):
    """(entradas de f082b41, entradas del cierre global): el delta cerrado aplicado a los blobs de f082b41 debe dar los
    blobs registrados."""
    base = gov_entries(objs, BASE)
    if base != {p: ('100644', 'blob', b) for p, b in BASE_BLOBS.items()}:
        raise ValueError(f'blobs de gobierno de {BASE[:12]} distintos de los registrados')
    new = {}
    for path in GOV_PATHS:
        text = blob_text(objs, base[path]).decode('utf-8')
        blocks = GC_DELTA_TEXT[path]
        if not blocks or any(text.count(before) != 1 for before, _ in blocks):
            raise ValueError(f'{path}: delta del cierre global vacío o con un bloque que no aparece exactamente una vez')
        for before, after in blocks:
            text = text.replace(before, after, 1)
        new[path] = ('100644', 'blob', blob_id(text.encode('utf-8')))
    if new != {p: ('100644', 'blob', b) for p, b in GC_BLOBS.items()}:
        raise ValueError('el delta del cierre global aplicado a los blobs de la base no da los blobs registrados')
    return base, new


def gov_problems(objs, parents, head, notes):
    base, new = governance(objs)
    if BASE not in parents:
        return [f'el merge de integración {BASE[:12]} no es ancestro de HEAD']
    after = descendants(parents, BASE)
    order = [c for c in topological(parents) if c in after]
    out = []
    intro = [c for c in order if gov_entries(objs, c) == new and not any(gov_entries(objs, p) == new for p in parents[c])]
    transition = intro[0] if len(intro) == 1 else None
    notes['transition'] = transition
    if len(intro) > 1:
        out.append(f'regla 4: el blob del cierre global se introduce fuera de una transición única: '
                   f'{[c[:12] for c in intro][:3]}')
    if transition is None:
        out.append('transición del cierre global no materializada en un único commit que cambie las cuatro rutas a la vez')
    else:
        ps = parents[transition]
        if len(ps) != 1:
            out.append(f'regla 2: la transición {transition[:12]} no tiene un solo padre')
        else:
            if gov_entries(objs, ps[0]) != base:
                out.append(f'regla 2: el padre de la transición {transition[:12]} no tiene los blobs de {BASE[:12]}')
            changed = set(name_status(git('diff-tree', '-r', '--no-renames', '--name-status', '-z', ps[0], transition)))
            if changed != set(GOV_PATHS):
                out.append(f'regla 2: la transición {transition[:12]} cambia otras rutas además del gobierno: '
                           f'{sorted(changed ^ set(GOV_PATHS))[:3]}')
    if transition != GC_TRANSITION:
        out.append(f'transición derivada ({transition[:12] if transition else "ninguna"}) distinta de la registrada '
                   f'({GC_TRANSITION[:12]})')
    closed = (descendants(parents, transition) | {transition}) if transition else set()
    bad = []
    for commit in order:
        want = new if commit in closed else base
        diff = [p for p, e in gov_entries(objs, commit).items() if e != want[p]]
        if diff:
            rule = ('regla 3: descendiente de la transición sin el blob del cierre global' if commit in closed else
                    'regla 1: commit sin la transición con un blob distinto de la base')
            bad.append(f'{commit[:12]}: {rule}: {diff}')
    out += bad[:3] + ([f'… y {len(bad) - 3} commits más con un blob de gobierno no admitido'] if len(bad) > 3 else [])
    root = commit_parts(objs, head)[0]
    index = index_entries(GOV_PATHS)
    for p in GOV_PATHS:
        if entry(objs, root, p) != new[p]:
            out.append(f'{p}: árbol de HEAD distinto del blob del cierre global')
        if index.get(p) != [(new[p][0], new[p][2], '0')]:
            out.append(f'{p}: índice distinto del blob del cierre global o en conflicto')
        data = disk_bytes(p)
        if data is None or blob_id(data) != new[p][2]:
            out.append(f'{p}: disco distinto del blob del cierre global, enlace o ausente')
    return out


# ---------------------------------------------------------------- SEM: semántica con piezas verificadas de B1 y R2-A
def gc_semantics(b1):
    """Declaraciones de estado de B1 con el vocabulario del cierre global: F35-SBX cerrada o congelada; F35-SBX-B, B1,
    B2 y B3 cerradas o congeladas; F36 y F36-SBX bloqueadas; el resto conserva sus valores. B1 no se modifica."""
    declared = [(s, a) for s, a in b1.DECLARED if s not in ('b1', 'f35-sbx-b', 'f35-sbx')] + [
        ('f35-sbx', ('cerrad', 'congelad')),
        ('f35-sbx-b', ('cerrad', 'congelad')),
        ('b1', ('cerrad', 'congelad', 'implementad') + b1.LOCKED),
        ('b2', ('implementad', 'congelad', 'cerrad', 'no aprobad') + b1.LOCKED),
        ('b3', ('implementad', 'congelad', 'cerrad') + b1.LOCKED),
        ('f36(?:-sbx)?', ('bloquead',) + b1.LOCKED)]
    decl_rx = [(re.compile(r'(?<![\w-])(' + subj + r')(?![\w-])(?:\s*(?::=|==|=|:|->|→)\s*|\s+(no\s+)?(?:se\s+)?'
                           + b1.DECL_COPULA + r'\s+(?:[a-z]+mente\s+)?|\s+)' + b1.STATE_VALUE), allowed)
               for subj, allowed in declared]
    verb_rx = [(re.compile(r'(?<![\w-])' + b1.DECL_NEG + r'(?:se\s+)?(?:(?:lo|la|los|las)\s+)?(?<![\w-])(?:' + b1.DECL_VERB +
                           r')(?![\w-])\s+(?:[a-z]+mente\s+)?(?:(?:el|la|los|las|al|a|the)\s+)?(?P<subj>' + subj +
                           r')(?![\w-])'), allowed, rx) for (subj, allowed), (rx, _) in zip(declared, decl_rx)] + \
              [(re.compile(r'(?<![\w-])(?P<subj>' + subj + r')(?![\w-])\s+' + b1.DECL_NEG + r'se\s+(?:[a-z]+mente\s+)?(?:' +
                           b1.DECL_VERB + r')(?![\w-])'), allowed, rx) for (subj, allowed), (rx, _) in zip(declared, decl_rx)]
    return decl_rx, verb_rx


def reopening(b1, text):
    """Reapertura de F35-SBX, F35-SBX-A, F35-SBX-B, B1, B2 o B3, o un estado distinto del cierre."""
    out = []
    for body in b1.sentences(text, cite=True):
        for m in GC_REOPEN_RX.finditer(body):
            if any(t in b1.NEG_WORDS or t.startswith(b1.NEG_PREFIXES) for t in m.group(1).split()):
                continue
            if b1.DECL_NEG_RX.search(re.split(r'[.,;:!?|]', body[:m.start()])[-1]):
                continue
            out.append(f'«{m.group(0).strip()}»')
    return out


def doc_problems(objs, root, b1, sem, r2a):
    """Los archivos de la capa: UTF-8 sin BOM, CR ni NUL; en el documento, sin datos personales, afirmaciones
    positivas ni declaraciones contradictorias (fuera de los bloques de código del delta), y en el principal, con los
    catorce límites."""
    out = []
    for path in LAYER_FILES:
        found = entry(objs, root, path)
        if found is None:
            out.append(f'{path}: ausente en HEAD')
            continue
        data = blob_text(objs, found)
        if len(data) > b1.MAX_BYTES or b'\x00' in data or b'\r' in data or data.startswith(b'\xef\xbb\xbf'):
            out.append(f'{path}: binario, CR, BOM o tamaño excesivo')
            continue
        text = data.decode('utf-8')
        if path not in (DOC, FIX_DOC, M02_DOC):
            continue
        hits = [m.group(0) for rx in b1.PII for m in [rx.search(text)] if m]
        if hits:
            out.append(f'{path}: posible dato personal: {hits[:2]}')
        claims = b1.positive_claims(text)
        if claims:
            out.append(f'{path}: afirmación positiva que habilita una capacidad prohibida: {claims[:2]}')
        bad = r2a.contradictions(b1, sem, FENCE_RX.sub('', text), GC_FORBIDDEN_RX)
        if bad:
            out.append(f'{path}: declaraciones de estado contradictorias con el gobierno vigente: {bad[:3]}')
        lines = set(text.splitlines())
        missing = [x for x in LIMITS if x not in lines]
        if path == DOC and missing:
            out.append(f'{path}: faltan límites del cierre (§2.5): {missing[:3]}')
    return out


def sem_problems(objs, head, b1, r2a):
    sem = gc_semantics(b1)
    root = commit_parts(objs, head)[0]
    base_root = commit_parts(objs, BASE)[0]
    out = []
    for path in GOV_PATHS:
        text = blob_text(objs, entry(objs, root, path)).decode('utf-8')
        old = blob_text(objs, entry(objs, base_root, path)).decode('utf-8')
        sections, header = r2a.gov_sections(text)
        if len(sections) != 1:
            out.append(f'{path}: se exige una única sección «Estado vigente F34E»')
            continue
        section = sections[0]
        if [ln for ln in section.splitlines() if re.match(r'^- [^=\n]+ = ', ln)] != GC_STATES:
            out.append(f'{path}: los trece estados de gobierno no son exactamente los del cierre global')
        missing = [x for x in GC_REQUIRED[path] if x not in section]
        if missing:
            out.append(f'{path}: el estado vigente no contiene la declaración canónica del cierre: '
                       f'{[x[:60] for x in missing[:2]]}')
        if path == 'docs/PROGRESS.md' and GC_HEADER not in header:
            out.append(f'{path}: la cabecera no declara a F35-SBX CERRADA Y CONGELADA')
        stale = [x for x in GC_STALE if x in section or x in header]
        if stale:
            out.append(f'{path}: el estado vigente conserva frases anteriores al cierre: {stale[:3]}')
        reopen = reopening(b1, section + '\n' + header)
        if reopen:
            out.append(f'{path}: reapertura o estado distinto del cierre: {reopen[:3]}')
        before = set(old.splitlines())
        added = '\n'.join(ln for ln in text.splitlines() if ln not in before)
        bad = r2a.contradictions(b1, sem, section + '\n' + header + '\n' + added, GC_FORBIDDEN_RX)
        if bad:
            out.append(f'{path}: declaraciones de estado contradictorias con el gobierno vigente: {bad[:3]}')
        claims = b1.positive_claims(added)
        if claims:
            out.append(f'{path}: líneas nuevas que afirman habilitar una capacidad prohibida: {claims[:2]}')
    out += doc_problems(objs, root, b1, sem, r2a)
    return out


# ---------------------------------------------------------------- SBX: DH-B13 con la función verificada de B1
def sbx_problems(b1):
    """sbx_eval() del gate de B1 verifica contra E validate_f34e.py y todo lo que carga, y solo entonces ejecuta su
    compute_sbx() con esos bytes. El propio gate se aparta de sys.modules durante la llamada, como en B1-FREEZE: B1
    rechaza evaluar con otro código del repositorio cargado."""
    running = sys.modules.pop('__main__', None)
    try:
        results, error = b1.sbx_eval(git, b1.real_bytes)
    finally:
        if running is not None:
            sys.modules['__main__'] = running
    if results is None:
        return [f'SBX-01..SBX-18 no evaluables: {error}'], []
    out, info = [], []
    for sid in b1.SBX_IDS:
        ok, detail = results.get(sid, (False, 'criterio ausente del recálculo'))
        source, check = b1.SBX_INFO[sid]
        info.append(f'INFO {sid}: {"PASS" if ok else "FAIL"} — fuente: {source}; comprobación: {check}'
                    + ('' if ok else f'; motivo: {detail}'))
        if not ok:
            out.append(f'{sid}: FAIL — {detail}')
    return out, info


# ---------------------------------------------------------------- FSY: superficies físicas (GC-AF-M01 y GC-AF-M02)
def surface_inventory(objs, commit, surfaces):
    """{ruta: entrada} de los archivos de las superficies en el árbol verificado de un commit."""
    root = commit_parts(objs, commit)[0]
    files = {}
    for surface in surfaces:
        found = entry(objs, root, surface)
        if found is None:
            continue
        if found[1] == 'tree':
            files.update({f'{surface}/{rel}': e for rel, e in listing(objs, root, surface).items()})
        else:
            files[surface] = found
    return files


JUNCTION_TAG = 0xA0000003           # IO_REPARSE_TAG_MOUNT_POINT: unión de directorio de Windows
REPARSE_POINT = 0x400               # FILE_ATTRIBUTE_REPARSE_POINT: enlace, unión u otro punto de reanálisis de NTFS
S_IFMT, S_IFDIR, S_IFLNK = 0o170000, 0o040000, 0o120000             # tipo de archivo en st_mode, sin el módulo stat


def physical_scan(roots):
    """Primer recorrido de FSY (GC-AF-M02), antes de cualquier recorrido heredado de B1 o de F34E: enumera todas las
    carpetas de las superficies, también las excepciones de B1 y las cachés de Python, y señala sin entrar en ellos los
    enlaces simbólicos, las uniones de directorio y cualquier otro punto de reanálisis (GC-FIX-L01). Todo error al leer
    los metadatos de una entrada o al enumerar una carpeta es un problema: lo que no se pudo recorrer nunca cuenta como
    limpio (falla cerrado)."""
    out, stack = [], []

    def visit(rel, st):
        if st.st_mode & S_IFMT == S_IFLNK:
            kind = 'enlace simbólico'
        elif getattr(st, 'st_file_attributes', 0) & REPARSE_POINT:
            kind = ('unión de directorio (enlace de Windows)' if getattr(st, 'st_reparse_tag', 0) == JUNCTION_TAG
                    else 'punto de reanálisis de NTFS')
        else:
            if st.st_mode & S_IFMT == S_IFDIR:
                stack.append(rel)
            return
        out.append(f'{kind} en una ruta protegida, sin seguirlo: {rel}')

    for rel in roots:
        try:
            st = os.lstat(os.path.join(ROOT, *rel.split('/')))
        except FileNotFoundError:
            continue                    # superficie ausente: el inventario dice si falta alguno de sus archivos
        except OSError as e:
            out.append(f'{rel}: metadatos ilegibles ({e.__class__.__name__}): no se puede verificar (falla cerrado)')
            continue
        visit(rel, st)
    while stack:
        rel = stack.pop()
        try:
            with os.scandir(os.path.join(ROOT, *rel.split('/'))) as entries:
                for item in entries:
                    visit(f'{rel}/{item.name}', item.stat(follow_symlinks=False))
        except OSError as e:
            out.append(f'{rel}: carpeta no enumerable ({e.__class__.__name__}): no se puede verificar (falla cerrado)')
    return sorted(out)


def fsy_problems(objs, head, b1, scan):
    """FSY de B1 (§8.3 y B1.3; TSBB-07) sobre HEAD, con sus piezas verificadas: el recorrido real de sus superficies
    materiales, sin seguir enlaces y aunque Git las ignore o no las vea, sus excepciones de metadatos y los .pyc
    derivables de su fuente. El inventario autorizado es el árbol de esas superficies en f082b41, que debe coincidir
    con el de HEAD y con el de la base de B1. Ni .gitignore ni .git/info/exclude deciden qué archivo físico es
    legítimo. scan son los problemas del recorrido físico previo: si hay alguno, los recorridos heredados de B1, que
    siguen las uniones como carpetas y callan los errores de enumeración en las excepciones, no se ejecutan."""
    surfaces = b1.RUNTIME_SURFACES
    want = surface_inventory(objs, BASE, surfaces)
    out = []
    head_files = surface_inventory(objs, head, surfaces)
    if head_files != want:
        diff = sorted(p for p in set(head_files) | set(want) if head_files.get(p) != want.get(p))
        out.append(f'el árbol de HEAD difiere del inventario autorizado de {BASE[:12]} en las superficies materiales: '
                   f'{diff[:5]}')
    if surface_inventory(objs, b1.B_BASE, surfaces) != want:
        out.append(f'el inventario de {BASE[:12]} difiere del de la base autorizada de B1 {b1.B_BASE[:12]}')
    if scan:
        return out + scan
    found, problems = b1.walk(surfaces, b1.RT_SKIP_DIRS, frozenset(), b1.RT_PYCACHE_ROOTS)
    out += problems + b1.exception_problems()
    extra = sorted(found - set(want))
    generated = [p for p in extra if p.startswith(b1.RT_GENERATED)]
    if generated:
        out.append(f'código generado y no versionado (bundle de Vite, Wayfinder o caché de Laravel): su origen no es '
                   f'verificable frente al inventario y no se certifica por nombre ni extensión (falla cerrado): '
                   f'{generated[:5]}')
    others = [p for p in extra if not p.startswith(b1.RT_GENERATED)]
    if others:
        out.append(f'archivos físicos en el runtime, el dataset o la evidencia fuera del inventario autorizado (aunque '
                   f'Git los ignore o no los vea): {others[:5]}')
    missing = sorted(set(want) - found)
    if missing:
        out.append(f'archivos del inventario autorizado ausentes o reemplazados en el disco: {missing[:5]}')
    changed = []
    for path, e in sorted(want.items()):
        if path in found:
            data = disk_bytes(path)
            if e[:2] not in (('100644', 'blob'), ('100755', 'blob')) or data is None or blob_id(data) != e[2]:
                changed.append(path)
    if changed:
        out.append(f'bytes físicos ilegibles o distintos de su blob en el inventario autorizado: {changed[:5]}')
    return out


# ---------------------------------------------------------------- RSK, ALC, FRZ y DEP
def rsk_problems(objs, head):
    found = entry(objs, commit_parts(objs, head)[0], DOC)
    if found is None:
        return [f'{DOC}: ausente en HEAD']
    text = blob_text(objs, found).decode('utf-8')
    out = []
    for rid, level, fragment, state in RISKS:
        rows = [ln for ln in text.splitlines() if ln.startswith(f'| {rid} |')]
        if len(rows) != 1:
            out.append(f'{rid}: se exige exactamente una fila en los riesgos residuales; hay {len(rows)}')
            continue
        cells = [c.strip() for c in rows[0].strip().strip('|').split('|')]
        if len(cells) != 5 or cells[1] != level or cells[4] != state or fragment not in cells[2]:
            out.append(f'{rid}: la fila no lo registra como {level}, «{state}», con su descripción')
        altered = [ln[:80] for ln in text.splitlines() if ln.startswith('|') and rid in ln and
                   not ln.startswith(f'| {rid} |') and RISK_ALTERED_RX.search(ln)]
        if altered:
            out.append(f'{rid}: figura con otra severidad o como resuelto: {altered[:2]}')
    return out


def alc_problems(objs, head):
    out = []
    for plane, delta in scope_delta(BASE, SCOPE).items():
        if delta:
            out.append(f'{plane}: alcance distinto del enumerado para el cierre global: {sorted(delta)[:3]}')
    extra = untracked()
    if extra:
        out.append(f'archivos sin seguimiento fuera del alcance: {extra[:5]}')
    root = commit_parts(objs, head)[0]
    own = {}
    for folder, names in LAYER_DIRS.items():
        found = listing(objs, root, folder)
        if found is None or set(found) != set(names) or any(e[:2] != ('100644', 'blob') for e in found.values()):
            out.append(f'{folder}: en HEAD no contiene exactamente sus archivos regulares')
            continue
        own.update({f'{folder}/{rel}': e for rel, e in found.items()})
        out += disk_folder(folder, found)
    out += index_problems(own, list(LAYER_DIRS), 'de HEAD en esta capa')
    return out


def frz_problems(objs, head, parents, notes):
    cache = {}

    def layer(commit):
        if commit not in cache:
            tree = commit_parts(objs, commit)[0]
            cache[commit] = {folder: listing(objs, tree, folder) for folder in LAYER_DIRS}
        return cache[commit]

    def complete(found):
        return all(found[folder] is not None and all(n in found[folder] for n in names)
                   for folder, names in LAYER_DIRS.items())
    if BASE not in parents:
        return [f'el merge de integración {BASE[:12]} no es ancestro de HEAD']
    after = descendants(parents, BASE)
    seals = sorted(c for c in after if complete(layer(c)) and not any(complete(layer(p)) for p in parents[c]))
    notes['completion'] = seals[0] if len(seals) == 1 else None
    if len(seals) != 1:
        return ['ningún commit posterior a la base completa la capa' if not seals else
                f'la capa se completa en más de un commit: {[c[:12] for c in seals]}']
    completion = seals[0]
    want, out = layer(completion), []
    for folder, names in LAYER_DIRS.items():
        if set(want[folder]) != set(names) or any(e[:2] != ('100644', 'blob') for e in want[folder].values()):
            out.append(f'{folder}: en el commit que completa la capa no contiene exactamente sus archivos regulares')
    later = descendants(parents, completion)
    if head != completion and head not in later:
        out.append(f'HEAD no desciende del commit que completa la capa {completion[:12]}')
    for commit in sorted(later):
        diff = [x for folder in LAYER_DIRS for x in listing_diff(folder, layer(commit)[folder], want[folder])]
        if diff:
            out.append(f'{commit[:12]}: capa distinta del commit que la completa (modificada, eliminada, renombrada, '
                       f'con otro modo o con archivos extra): {diff[:3]}')
    files = {f'{folder}/{rel}': e for folder, found in want.items() for rel, e in found.items()}
    out += index_problems(files, list(LAYER_DIRS), 'del commit que completa la capa')
    for folder in LAYER_DIRS:
        out += disk_folder(folder, want[folder])
    return out


def dep_problems():
    out = []
    for path, allowed in DEP_ALLOWED.items():
        data = disk_bytes(path)
        if data is None:
            out.append(f'{path}: ausente o ilegible')
            continue
        tree = ast.parse(data.decode('utf-8'), filename=path)
        modules, dynamic, owner = set(), [], {}
        for fn in ast.walk(tree):
            if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for node in ast.walk(fn):
                    owner.setdefault(id(node), fn.name)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules.update(alias.name.split('.')[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                modules.add(node.module.split('.')[0] if node.level == 0 and node.module else '(relativa)')
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in DYNAMIC_CODE:
                dynamic.append((node.func.id, owner.get(id(node))))
        if modules - allowed:
            out.append(f'{path}: importaciones fuera de la biblioteca estándar autorizada: {sorted(modules - allowed)}')
        loader = LOADERS.get(path)
        if sorted(dynamic) != ([('compile', loader), ('exec', loader)] if loader else []):
            out.append(f'{path}: ejecución dinámica de código fuera de su carga verificada: {sorted(dynamic)[:4]}')
    return out


# ---------------------------------------------------------------- evaluación con fallo cerrado
def evaluate():
    viol, info, notes = {rid: [] for rid in ORDER}, [], {'completion': None, 'transition': None}

    def closed(rids, why):
        for rid in rids:
            viol[rid].append(f'no evaluable: {why} (falla cerrado)')

    def check(rid, fn, *args):
        try:
            result = fn(*args)
        except ERRORS as e:
            closed((rid,), f'{e.__class__.__name__}: {e}')
            return None
        problems, rest = (result[0], result[1:]) if isinstance(result, tuple) else (result, ())
        viol[rid] += problems
        return rest

    try:
        problems, head, shallow = ent_problems()
    except ERRORS as e:
        check('DEP', dep_problems)
        closed([r for r in ORDER if r != 'DEP'], f'repositorio Git ({e.__class__.__name__}: {e})')
        return viol, info
    viol['ENT'] += problems
    check('FLG', flg_problems)
    check('DEP', dep_problems)
    if shallow:
        closed([r for r in ORDER if r not in ('ENT', 'FLG', 'DEP')], 'repositorio superficial: historia incompleta')
        return viol, info
    info.append(f'INFO ANC: anclas registradas {", ".join(c[:12] for c in ANCHORS + (GC_TRANSITION,))}; base {BASE}; '
                f'HEAD {head}')
    objs = None
    try:
        objs = Objects()
        parents = branch = None
        try:
            parents = ancestry(objs, head)
            branch = current_branch()
        except ERRORS as e:
            closed(('CTX', 'ANC', 'INT', 'GOV', 'FRZ'), f'historia desde HEAD ({e.__class__.__name__}: {e})')
        if parents is not None:
            check('CTX', ctx_problems, branch, parents)
            check('ANC', anc_problems, objs, parents)
            check('INT', int_problems, objs, parents)
            check('GOV', gov_problems, objs, parents, head, notes)
            check('FRZ', frz_problems, objs, head, parents, notes)
        mods = {}
        try:
            mods = {name: load_verified(objs, name) for name in ('b1', 'r2a')}
        except ERRORS as e:
            closed(('SEM', 'SBX', 'FSY'), f'gates congelados verificados ({e.__class__.__name__}: {e})')
        if mods:
            check('SEM', sem_problems, objs, head, mods['b1'], mods['r2a'])
            try:
                scan = physical_scan(mods['b1'].RUNTIME_SURFACES)
            except ERRORS as e:
                scan = [f'recorrido físico no evaluable ({e.__class__.__name__}: {e}) (falla cerrado)']
            if scan:
                closed(('SBX',), 'la superficie física no está verificada (FSY): SBX-15 la recorrería y la leería con el '
                                 'código de F34E, que sigue las uniones y calla los errores de enumeración')
            else:
                sbx = check('SBX', sbx_problems, mods['b1'])
                if sbx:
                    info += sbx[0]
            check('FSY', fsy_problems, objs, head, mods['b1'], scan)
        check('RSK', rsk_problems, objs, head)
        check('ALC', alc_problems, objs, head)
    except ERRORS as e:
        closed(('CTX', 'ANC', 'INT', 'GOV', 'SEM', 'SBX', 'FSY', 'RSK', 'ALC', 'FRZ'),
               f'objetos Git ({e.__class__.__name__}: {e})')
    finally:
        if objs is not None:
            objs.close()
    info.append(f'INFO GOV: transición del cierre global derivada: {notes["transition"] or "ninguna"}; registrada: '
                f'{GC_TRANSITION}')
    info.append(f'INFO FRZ: commit que completa la capa: {notes["completion"] or "ninguno"}')
    return viol, info


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    try:
        viol, info = evaluate()
    except Exception as e:      # cualquier fallo inesperado: todas las reglas fallan cerradas
        viol = {rid: [f'evaluación interrumpida ({e.__class__.__name__}): falla cerrado'] for rid in ORDER}
        info = []
    for line in info:
        print(line)
    fallas = [rid for rid in ORDER if viol[rid]]
    for rid in fallas:
        print(f'FALLA {rid}: {len(viol[rid])} violaciones — {viol[rid][:3]}')
    print(f'validate_f35sbx_cierre_global: {len(ORDER) - len(fallas)} comprobaciones correctas, {len(fallas)} fallas')
    sys.exit(1 if fallas else 0)


if __name__ == '__main__':
    main()
