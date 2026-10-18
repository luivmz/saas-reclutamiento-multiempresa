"""F35-SBX-B — gate del registro del cierre formal de B2, R2-A (validate_f35sbxb2_cierre_formal.py).

Uso:  python -I docs/academico/tools/f35sbxb2_cierre_formal/validate_f35sbxb2_cierre_formal.py   (sin -I, se relanza)

Contrato: docs/academico/evidencia-sbx-b2-cierre-formal/F35SBXB_B2_Cierre_Formal.md. Registra en el gobierno el cierre
formal de B2, ya acreditado, con una transición única y monotónica (B2_CLOSURE_GOVERNANCE_BLOB →
B2_FORMAL_GOVERNANCE_BLOB), registra el ancla externa aprobada del cierre de gobierno (363273e) y conserva la evaluación
vigente: el gate del cierre de gobierno, B2-SUCCESSOR-FREEZE y el gate de B2 se ejecutan intactos y su falla de clase A
se clasifica con exactitud. Lo que esa falla enmascara se repone con reglas propias. El repositorio solo se lee; los
subgates escriben únicamente sus temporales fuera de él. Cada objeto Git que se lee se verifica recalculando su
identificador, y todo error, salida incompleta o estado no evaluable falla cerrado.

  ENT  intérprete aislado y sin PYTHONPATH, PYTHONHOME ni PYTHONUSERBASE; ninguna variable de Git que redirija el
       repositorio; Git sobre el repositorio de este archivo, con historia completa y sin injertos ni reemplazos.
  CTX  rama chore/f35-sbx-b2-r2a-final-closure, develop o main; el merge 04895aa, ancestro de HEAD.
  ANC  anclas registradas, íntegras y en cadena (8e94a60 → 3d9b783 → 72e86c5 → 12c1c36 → 2472fd6 → 9961d2d → 9d6fb15
       → 8969424 → eb02c2d → d346597 → 363273e → 04895aa); los merges eb02c2d y 04895aa con sus padres y árboles;
       blobs de gobierno de B1, de B2 y del cierre de gobierno.
  HIS  el gate del cierre de gobierno, con los bytes de su blob en 363273e, anclado sobre 363273e en un clon temporal
       sin remoto: código 0, 13/0, FRZ en 363273e y GOV en d346597.
  GCL  el mismo gate sobre HEAD: su salida es exactamente la que su lógica da sobre el estado observado, y solo falla
       por la clase A de este incremento (CTX en la rama, SUC, MAT, GOV, SEM y ALC).
  SUC  B2-SUCCESSOR-FREEZE sobre HEAD: solo VIG y ALC (clase A), ALC con rutas del cierre de gobierno y de esta capa.
  MAT  el gate de B2, con los bytes de su blob en el candidato, sobre HEAD: solo lo que predice el estado observado.
  INT  capas congeladas de B1 a B2-GOVERNMENT-CLOSURE desde sus anclas, en cada commit posterior, HEAD, índice y disco.
  FLG  ningún flag en el índice.
  GOV  transición única y monotónica en cuatro etapas, registrada; estado efectivo en HEAD, índice y disco.
  SEM  semántica del gobierno y de los documentos de la capa con las piezas verificadas del gate de B1, con el ciclo de
       vida de B2 cerrado (cerrada admitida; reapertura, aprobación, producción y demás, rechazadas).
  ALC  alcance exacto frente a 04895aa: tres rutas A de la capa y el gobierno M; sin archivos sin seguimiento.
  FRZ  nivel B: un único commit posterior a 04895aa completa la capa y, desde él, sus archivos no cambian. Su hash
       se deriva de Git y se registra fuera, nunca en un archivo.
  DEP  biblioteca estándar autorizada; la única ejecución dinámica es la carga del gate de B1 desde su blob verificado.
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
sys.pycache_prefix = os.path.join(os.path.abspath(__file__), 'sin-pyc')

import ast  # noqa: E402
import hashlib  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
import types  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))

# ---------------------------------------------------------------- anclas registradas (todas existían antes que este archivo)
B1_ANCHOR = '8e94a60274fe39ebda3e9961bc58036b389dfc00'          # ancla auditada de B1
B1_CLOSURE = '3d9b78307684a0dfb093e31d28fde290b2b1cb4a'         # cierre de B1-FREEZE
B2_BASE = '72e86c5838984ea873d6dd56c179d94217b27317'            # develop al crear la rama de B2
B2_TRANSITION = '12c1c36e409f81c048fccf7fcb3e6d2a2d5d40aa'      # transición de gobierno de B2
CANDIDATE = '2472fd6fadfc0634ec68cbcb76cfc9fbfe105194'          # candidato de B2 reauditado
FREEZE = '9961d2d65ed51a17c14aae5db0edb7d71c622c22'             # B2-FREEZE
SUCCESSOR = '9d6fb157bb818574217e3675da1849e8d1010962'          # gate sucesor (AF-M01)
SUCCESSOR_FREEZE = '89694244b81b0bd84dbe6ae5d04b5c7a198bafef'   # B2-SUCCESSOR-FREEZE: ancla externa aprobada (AF-L02)
DEVELOP_MERGE = 'eb02c2d84335347c52b81a76c1e73dc30b93e88a'      # integración de B2 en develop
CLOSURE_TRANSITION = 'd346597e988d2f7f5d0d84e119709012b67715da'  # transición del cierre de gobierno
GOV_CLOSURE = '363273ead5794ea7a2dba74c011a0efd6d59e906'        # B2-GOVERNMENT-CLOSURE: ancla externa aprobada
DEVELOP_GOV_MERGE = '04895aacd96f0f03dde84e10a558bbdf26f050c6'  # integración del cierre de gobierno en develop; base
CHAIN = (B1_ANCHOR, B1_CLOSURE, B2_BASE, B2_TRANSITION, CANDIDATE, FREEZE, SUCCESSOR, SUCCESSOR_FREEZE, DEVELOP_MERGE,
         CLOSURE_TRANSITION, GOV_CLOSURE, DEVELOP_GOV_MERGE)
# Commit de la transición de gobierno de este incremento. Se registra después de que exista, nunca en el propio commit.
FORMAL_TRANSITION = 'ddefb7dae00a7b57eb32c1046de634c0be2805de'

BRANCH = 'chore/f35-sbx-b2-r2a-final-closure'
BRANCHES = (BRANCH, 'develop', 'main')
B2_BRANCH = 'feature/f35-sbx-b2-ephemeral-store'
GC_BRANCH = 'chore/f35-sbx-b2-government-closure'
GC_BRANCHES = (GC_BRANCH, 'develop', 'main')
GOV_PATHS = ('CLAUDE.md', 'docs/PROGRESS.md')
B1_GOV_BLOBS = {'CLAUDE.md': 'b7068afbfac6cc2f1f39053dff8face38b894415',
                'docs/PROGRESS.md': '983844fd2477432b2a1ea402aa8b3130678a014a'}
B2_GOV_BLOBS = {'CLAUDE.md': '74cc4a71c56918678e0a70c7f59a3f060d87b6a0',
                'docs/PROGRESS.md': '07889bf8c82990651539a6e4b8a1098b4bd2d35a'}
CLOSURE_GOV_BLOBS = {'CLAUDE.md': 'dcf584c28f8b0f044e3ab9fc11cc117fc17e8a8c',
                     'docs/PROGRESS.md': '49390335d47a13468f0a5b4017cf6b5723ad8ecb'}
B1_GATE = 'docs/academico/tools/f35sbxb/validate_f35sbxb.py'
B2_GATE = 'docs/academico/tools/f35sbxb2/validate_f35sbxb2.py'
SF_VALIDATOR = 'docs/academico/tools/f35sbxb2_sucesor_freeze/validate_f35sbxb2_sucesor_freeze.py'
GC_GATE = 'docs/academico/tools/f35sbxb2_cierre_gobierno/validate_f35sbxb2_cierre_gobierno.py'

# Capas congeladas (INT): cada una con su ancla y sus carpetas, cuyo contenido exacto se toma del árbol del ancla. El
# gobierno no está aquí: lo protege GOV.
FROZEN = (('B1', B1_ANCHOR, ('docs/academico/evidencia-sbx-b', 'docs/academico/tools/f35sbxb')),
          ('B1-FREEZE', B1_CLOSURE, ('docs/academico/evidencia-sbx-b-freeze', 'docs/academico/tools/f35sbxb_freeze')),
          ('B2', CANDIDATE, ('docs/academico/evidencia-sbx-b2', 'docs/academico/tools/f35sbxb2')),
          ('B2-FREEZE', FREEZE, ('docs/academico/evidencia-sbx-b2-freeze', 'docs/academico/tools/f35sbxb2_freeze')),
          ('sucesor', SUCCESSOR, ('docs/academico/evidencia-sbx-b2-sucesor', 'docs/academico/tools/f35sbxb2_sucesor')),
          ('B2-SUCCESSOR-FREEZE', SUCCESSOR_FREEZE, ('docs/academico/evidencia-sbx-b2-sucesor-freeze',
                                                     'docs/academico/tools/f35sbxb2_sucesor_freeze')),
          ('B2-GOVERNMENT-CLOSURE', GOV_CLOSURE, ('docs/academico/evidencia-sbx-b2-cierre-gobierno',
                                                  'docs/academico/tools/f35sbxb2_cierre_gobierno')))

# Capa del cierre de gobierno, tal como la ve su propio gate (para predecir su clase A).
GC_LAYER_DIRS = {'docs/academico/evidencia-sbx-b2-cierre-gobierno': ('F35SBXB_B2_Cierre_Gobierno.md',),
                 'docs/academico/tools/f35sbxb2_cierre_gobierno': ('test_f35sbxb2_cierre_gobierno.py',
                                                                   'validate_f35sbxb2_cierre_gobierno.py')}
GC_LAYER_FILES = tuple(sorted(f'{folder}/{name}' for folder, names in GC_LAYER_DIRS.items() for name in names))
GC_SCOPE = {**{p: 'A' for p in GC_LAYER_FILES}, **{p: 'M' for p in GOV_PATHS}}

# Capa de este incremento (nivel B), con su contenido exacto.
LAYER_TOOLS = 'docs/academico/tools/f35sbxb2_cierre_formal'
LAYER_DIRS = {'docs/academico/evidencia-sbx-b2-cierre-formal': ('F35SBXB_B2_Cierre_Formal.md',),
              LAYER_TOOLS: ('test_f35sbxb2_cierre_formal.py', 'validate_f35sbxb2_cierre_formal.py')}
LAYER_FILES = tuple(sorted(f'{folder}/{name}' for folder, names in LAYER_DIRS.items() for name in names))
VALIDATOR = LAYER_TOOLS + '/validate_f35sbxb2_cierre_formal.py'
TESTS = LAYER_TOOLS + '/test_f35sbxb2_cierre_formal.py'
SCOPE = {**{p: 'A' for p in LAYER_FILES}, **{p: 'M' for p in GOV_PATHS}}

# Delta de gobierno del cierre formal: lista cerrada de reemplazos literales sobre B2_CLOSURE_GOVERNANCE_BLOB, cada
# bloque antiguo presente exactamente una vez (§3.3 del contrato).
_CLOSURE_SENTENCE_1 = ('F35-SBX-B INICIADA solo como sandbox sintético: B1 (gate sucesor sobre HEAD) CERRADA, CONGELADA E '
                       'INTEGRADA; B2 (almacén efímero SQLite `:memory:` por organización sintética) IMPLEMENTADA, '
                       'CORREGIDA, REAUDITADA, CONGELADA E INTEGRADA TÉCNICAMENTE, PENDIENTE DE CIERRE FORMAL, sin '
                       'pipeline funcional ni ML.')
_CLOSURE_SENTENCE_2 = ('F35-SBX-B INICIADA: su incremento B1 (gate sucesor sobre HEAD) está CERRADO, CONGELADO E '
                       'INTEGRADO en `develop` y `main` (ancla auditada `8e94a60274fe39ebda3e9961bc58036b389dfc00`, cierre '
                       '`3d9b78307684a0dfb093e31d28fde290b2b1cb4a`), registrado en [`evidencia-sbx-b-freeze`]'
                       '({root}evidencia-sbx-b-freeze/F35SBXB_B1_Freeze.md); su incremento B2 (almacén efímero aislado) '
                       'está IMPLEMENTADO, CORREGIDO, REAUDITADO, CONGELADO E INTEGRADO TÉCNICAMENTE en `develop` y `main` '
                       '(ancla aprobada `89694244b81b0bd84dbe6ae5d04b5c7a198bafef`, merges '
                       '`eb02c2d84335347c52b81a76c1e73dc30b93e88a` y `5bf4f4e58c3860be4c5d9f94d1c4b5a031570d33`), '
                       'registrado en [`evidencia-sbx-b2`]({root}evidencia-sbx-b2/README.md), y está PENDIENTE DE CIERRE '
                       'FORMAL: su incremento de cierre de gobierno está IMPLEMENTADO y es CANDIDATO A AUDITORÍA '
                       'INDEPENDIENTE, en `chore/f35-sbx-b2-government-closure` y registrado en '
                       '[`evidencia-sbx-b2-cierre-gobierno`]'
                       '({root}evidencia-sbx-b2-cierre-gobierno/F35SBXB_B2_Cierre_Gobierno.md). La integración y la '
                       'publicación de ese incremento requieren autorización explícita del equipo.')
_FORMAL_SENTENCE_1 = ('F35-SBX-B INICIADA solo como sandbox sintético: B1 (gate sucesor sobre HEAD) CERRADA, CONGELADA E '
                      'INTEGRADA; B2 (almacén efímero SQLite `:memory:` por organización sintética) CERRADA, CONGELADA E '
                      'INTEGRADA, sin pipeline funcional ni ML.')
_FORMAL_SENTENCE_2 = ('F35-SBX-B INICIADA: su incremento B1 (gate sucesor sobre HEAD) está CERRADO, CONGELADO E '
                      'INTEGRADO en `develop` y `main` (ancla auditada `8e94a60274fe39ebda3e9961bc58036b389dfc00`, cierre '
                      '`3d9b78307684a0dfb093e31d28fde290b2b1cb4a`), registrado en [`evidencia-sbx-b-freeze`]'
                      '({root}evidencia-sbx-b-freeze/F35SBXB_B1_Freeze.md); su incremento B2 (almacén efímero aislado) '
                      'está CERRADO, CONGELADO E INTEGRADO en `develop` y `main` (ancla aprobada '
                      '`89694244b81b0bd84dbe6ae5d04b5c7a198bafef`, merges `eb02c2d84335347c52b81a76c1e73dc30b93e88a` y '
                      '`5bf4f4e58c3860be4c5d9f94d1c4b5a031570d33`), registrado en [`evidencia-sbx-b2`]'
                      '({root}evidencia-sbx-b2/README.md); su cierre de gobierno está AUDITADO E INTEGRADO en `develop` y '
                      '`main` (ancla aprobada `363273ead5794ea7a2dba74c011a0efd6d59e906`, merges '
                      '`04895aacd96f0f03dde84e10a558bbdf26f050c6` y `d5a4b4e7c4ba01c1b923d215a51f0d2f22c8f163`), '
                      'registrado en [`evidencia-sbx-b2-cierre-gobierno`]'
                      '({root}evidencia-sbx-b2-cierre-gobierno/F35SBXB_B2_Cierre_Gobierno.md); su cierre formal está '
                      'registrado en [`evidencia-sbx-b2-cierre-formal`]'
                      '({root}evidencia-sbx-b2-cierre-formal/F35SBXB_B2_Cierre_Formal.md).')
FORMAL_DELTA = {
    'CLAUDE.md': [(_CLOSURE_SENTENCE_1, _FORMAL_SENTENCE_1),
                  (_CLOSURE_SENTENCE_2.format(root='docs/academico/'), _FORMAL_SENTENCE_2.format(root='docs/academico/'))],
    'docs/PROGRESS.md': [
        ('Última actualización: 2026-10-14 (F34E CERRADA; G0 real NO APROBADA; G0-SBX APROBADA CON RESTRICCIONES; '
         'F35-SBX sintética HABILITADA; F35-SBX-A CERRADA E INTEGRADA; B0 CERRADA E INTEGRADA; F35-SBX-B INICIADA: '
         'B1 CERRADA E INTEGRADA, B2 INTEGRADA TÉCNICAMENTE Y PENDIENTE DE CIERRE FORMAL).',
         'Última actualización: 2026-10-18 (F34E CERRADA; G0 real NO APROBADA; G0-SBX APROBADA CON RESTRICCIONES; '
         'F35-SBX sintética HABILITADA; F35-SBX-A CERRADA E INTEGRADA; B0 CERRADA E INTEGRADA; F35-SBX-B INICIADA: '
         'B1 CERRADA E INTEGRADA, B2 CERRADA E INTEGRADA).'),
        ('El 14/10/2026 pasó a B2 integrada técnicamente y pendiente de cierre formal, con su incremento de cierre de '
         'gobierno candidato a auditoría independiente.',
         'El 14/10/2026 pasó a B2 integrada técnicamente y pendiente de cierre formal, con su incremento de cierre de '
         'gobierno candidato a auditoría independiente. El 18/10/2026 pasó a B2 cerrada e integrada, con su cierre de '
         'gobierno auditado e integrado y su cierre formal registrado.'),
        (_CLOSURE_SENTENCE_1, _FORMAL_SENTENCE_1),
        (_CLOSURE_SENTENCE_2.format(root='academico/'), _FORMAL_SENTENCE_2.format(root='academico/'))]}
PENDING = 'PENDIENTE DE CIERRE FORMAL'
CLOSED_SECTION = ('B2 (almacén efímero SQLite `:memory:` por organización sintética) CERRADA, CONGELADA E INTEGRADA, '
                  'sin pipeline funcional ni ML.',
                  'su incremento B2 (almacén efímero aislado) está CERRADO, CONGELADO E INTEGRADO en `develop` y `main`')
CLOSED_HEADER = 'B2 CERRADA E INTEGRADA).'

# Ciclo de vida de B2 en la semántica (§3.7): cerrada es el estado registrado; la reapertura y todo estado posterior
# (aprobada, productiva, publicada, desplegada) siguen rechazados.
B2_ALLOWED = ('implementad', 'congelad', 'cerrad', 'no aprobad')
B2_FORBIDDEN_RX = re.compile(r'(?<![\w-])b2(?![\w-])((?:\s+[a-z0-9-]+){0,3}?)\s*(?:=|:|\s)\s*(productiv\w*|aprobad\w*|'
                             r'publicad\w*|desplegad\w*)\b')
B2_REOPEN_RX = re.compile(r'(?<![\w-])b2(?![\w-])((?:\s+[a-z0-9-]+){0,3}?)\s*(?:=|:|\s)\s*(reabiert\w*|reabr\w*|'
                          r'reapert\w*|pendiente\w*|abiert\w*|desarroll\w*|candidat\w*|no\s+cerrad\w*)\b')
B2_LIFECYCLE_ITEMS = frozenset({'«b2 integrada»', '«b2 integrado»', '«b2 congelada»', '«b2 congelado»', '«b2 cerrada»',
                                '«b2 cerrado»'})
# El cierre de gobierno, congelado, conserva su propio vocabulario: lo que este incremento le hace rechazar.
GC_B2_ALLOWED = ('implementad', 'congelad', 'no cerrad', 'no aprobad')
GC_B2_FORBIDDEN_RX = re.compile(r'(?<![\w-])b2(?![\w-])((?:\s+[a-z0-9-]+){0,3}?)\s*(?:=|:|\s)\s*(cerrad\w*|'
                                r'productiv\w*|aprobad\w*|publicad\w*|desplegad\w*)\b')
GC_LIFECYCLE_ITEMS = frozenset({'«b2 integrada»', '«b2 integrado»', '«b2 congelada»', '«b2 congelado»'})
GC_CLOSED_ITEMS = frozenset({'«b2 cerrada»', '«b2 cerrado»'})

DEP_ALLOWED = {VALIDATOR: frozenset({'ast', 'hashlib', 're', 'os', 'subprocess', 'sys', 'types'}),
               TESTS: frozenset({'hashlib', 'os', 'subprocess', 'sys'})}
DYNAMIC_CODE = frozenset({'__import__', 'compile', 'eval', 'exec'})
LOADER = 'load_b1_gate'                         # única función con ejecución dinámica: el gate de B1 verificado
ORDER = ('ENT', 'CTX', 'ANC', 'HIS', 'GCL', 'SUC', 'MAT', 'INT', 'FLG', 'GOV', 'SEM', 'ALC', 'FRZ', 'DEP')
PLANES = ('HEAD', 'árbol', 'índice')
TIMEOUT = 3600
REDIRECTING = ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'GIT_OBJECT_DIRECTORY', 'GIT_ALTERNATE_OBJECT_DIRECTORIES',
               'GIT_COMMON_DIR', 'GIT_NAMESPACE', 'GIT_REPLACE_REF_BASE', 'GIT_NO_REPLACE_OBJECTS', 'GIT_GRAFT_FILE',
               'GIT_SHALLOW_FILE', 'GIT_CEILING_DIRECTORIES', 'GIT_DISCOVERY_ACROSS_FILESYSTEM',
               'GIT_LITERAL_PATHSPECS', 'GIT_GLOB_PATHSPECS', 'GIT_NOGLOB_PATHSPECS', 'GIT_ICASE_PATHSPECS')
GIT_ENV = {k: v for k, v in os.environ.items() if not k.upper().startswith('GIT_')}
GIT = ('git', '--no-replace-objects', '--literal-pathspecs')

# Salidas de los subgates congelados.
FALLA_RULE = re.compile(r'FALLA ([A-Z][A-Z0-9]{2}): (\d+) violaciones — (\[.*\])')
CASE_ID = re.compile(r'(?:[PF]\d{2}|NB2-\d{2}|PB2-\d{2})')
B2_SUMMARY = re.compile(r'validate_f35sbxb2: (\d+) comprobaciones correctas, (\d+) fallas')
B2_INFO = re.compile(r'INFO transición de gobierno de B2 derivada: ([0-9a-f]{40}); registrada: ([0-9a-f]{40})')
B2_TOTAL = 119
SF_SUMMARY = re.compile(r'validate_f35sbxb2_sucesor_freeze: (\d+) comprobaciones correctas, (\d+) fallas')
SF_INFO = {
    'ANC': re.compile(r'INFO ANC: candidato ([0-9a-f]{40}); freeze ([0-9a-f]{40}); sucesor registrado ([0-9a-f]{40}); '
                      r'HEAD ([0-9a-f]{40})'),
    'VIG': re.compile(r'INFO VIG: gate sucesor sobre HEAD: código (\d+); (\d+) correctas, (\d+) fallas; reglas del '
                      r'sucesor en falla: ([^;]*); reglas del gate de B2 en falla: ([^;]*); SCP: .*'),
    'FRZ': re.compile(r'INFO FRZ: commit que completa el cierre: ([0-9a-f]{40}|ninguno); commits posteriores al '
                      r'sucesor: (\d+|no verificable)')}
SF_TOTAL = 12
SF_ALC = re.compile(r'(HEAD|árbol|índice): alcance distinto del cierre frente al sucesor: (\[.*\])')
GC_SUMMARY = re.compile(r'validate_f35sbxb2_cierre_gobierno: (\d+) comprobaciones correctas, (\d+) fallas')
GC_INFO = {
    'ANC': re.compile(r'INFO ANC: anclas registradas ((?:[0-9a-f]{12}, )*[0-9a-f]{12}); ancla aprobada de '
                      r'B2-SUCCESSOR-FREEZE ([0-9a-f]{40}); integración ([0-9a-f]{40}); HEAD ([0-9a-f]{40})'),
    'MAT': re.compile(r'INFO MAT: gate de B2 sobre HEAD: código (\d+); (\d+) correctas, (\d+) fallas; reglas en falla: '
                      r'([^;]*); casos en falla: ([^;]*); SCP: (\d+) violaciones \(previstas (\d+)\)'),
    'SUC': re.compile(r'INFO SUC: B2-SUCCESSOR-FREEZE sobre HEAD: código (\d+); (\d+) correctas, (\d+) fallas; reglas en '
                      r'falla: ([^;]*); gate sucesor en falla: ([^;]*); ancla derivada ([0-9a-f]{40}|ninguno)'),
    'HIS': re.compile(r'INFO HIS: B2-SUCCESSOR-FREEZE anclado sobre ([0-9a-f]{40}): código (\d+); (\d+) correctas, '
                      r'(\d+) fallas; ancla derivada ([0-9a-f]{40}|ninguno)'),
    'GOV': re.compile(r'INFO GOV: transición del cierre derivada: ([0-9a-f]{40}|ninguna); registrada: '
                      r'([0-9a-f]{40}|ninguna)'),
    'FRZ': re.compile(r'INFO FRZ: commit que completa la capa: ([0-9a-f]{40}|ninguno)')}
GC_TOTAL = 13
SCP_ITEM = re.compile(r'(HEAD|árbol|índice): cambio fuera del delta autorizado de B2 o con estado inesperado: A (.+)')
RULE3_ITEM = re.compile(r"([0-9a-f]{12}): regla 3: descendiente de la transición sin el blob nuevo de B2: "
                        r"\['CLAUDE\.md', 'docs/PROGRESS\.md'\]|([0-9a-f]{12}): regla 3: descendiente de la transición "
                        r"sin el blob nuevo de B2: \['(?:CLAUDE\.md|docs/PROGRESS\.md)'\]")
RULE4_ITEM = re.compile(r'regla 4: introducción del blob nuevo de gobierno fuera de la transición única: \[.*\]')
EFFECTIVE = {'árbol': '{}: árbol de HEAD distinto del blob admitido',
             'índice': '{}: índice distinto del blob admitido, con flags o en conflicto',
             'disco': '{}: disco distinto del blob admitido, enlace o ausente'}
GOV_CONTENT = '{}: contenido distinto del blob histórico de B1 y del blob nuevo de B2'
GOV_SEMANTIC = re.compile(r'(CLAUDE\.md|docs/PROGRESS\.md): declaraciones de estado contradictorias con el gobierno '
                          r'vigente: (\[.*\])')
GC_MATERIAL_CTX = "el gate de B2 sobre HEAD incumple comprobaciones materiales: reglas ['CTX']"
GC_SCP_PREFIX = 'SCP del gate de B2 con '
GC_GOV_PREFIX = 'GOV del gate de B2 no se explica solo por la divergencia de gobierno y el ciclo de vida de B2: '
GC_SUC_PREFIX = 'ALC de B2-SUCCESSOR-FREEZE no falla solo por las rutas de este incremento en los tres planos: '
GC_RULE3 = re.compile(r'([0-9a-f]{12}): regla 3: descendiente de la transición del cierre sin su blob: (\[.*\])')
GC_MORE = re.compile(r'… y (\d+) commits más con un blob de gobierno no admitido')
GC_EFFECTIVE = re.compile(r'(CLAUDE\.md|docs/PROGRESS\.md): (árbol de HEAD distinto del blob admitido|índice distinto del '
                          r'blob admitido o en conflicto|disco distinto del blob admitido, enlace o ausente)')


class GitError(Exception):
    pass


ERRORS = (GitError, OSError, ValueError, KeyError, TypeError, IndexError, SyntaxError, UnicodeDecodeError,
          subprocess.TimeoutExpired)


def git(*args, cwd=None, env=None):
    try:
        p = subprocess.run([*GIT, *args], cwd=cwd or ROOT, env=env or GIT_ENV, capture_output=True, timeout=TIMEOUT)
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


def disk_path(rel, root=None):
    parts, root = rel.split('/'), root or ROOT
    if any(linked(os.path.join(root, *parts[:k])) for k in range(1, len(parts) + 1)):
        return None
    return os.path.join(root, *parts)


def disk_bytes(rel, root=None):
    full = disk_path(rel, root)
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
    sin enlaces y con sus blobs."""
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


def flags(path):
    return [item[:1] for item in git('ls-files', '-v', '-z', '--', path).split(b'\x00') if item and item[:1] != b'H']


# ---------------------------------------------------------------- subgates congelados, con bytes verificados
def verified_script(rel, expected, root=None):
    data = disk_bytes(rel, root)
    if data is None or blob_id(data) != expected:
        raise ValueError(f'{rel} distinto de su blob {expected[:12]}: no se ejecuta')
    return disk_path(rel, root)


def run_script(rel, expected, cwd):
    """Ejecuta un subgate con bytes verificados antes y después, con python -I y sin variables GIT_*."""
    path = verified_script(rel, expected, cwd)
    p = subprocess.run([sys.executable, '-I', '-B', path], cwd=cwd, env=GIT_ENV, capture_output=True, timeout=TIMEOUT)
    verified_script(rel, expected, cwd)
    return p.returncode, p.stdout, p.stderr


def parse_output(code, stdout, stderr, summary_rx, info_rx):
    """Salida estricta de un subgate: (correctas, fallas, {regla: (n, violaciones)}, [casos en falla], {INFO}). Solo
    se admiten sus líneas INFO, sus líneas FALLA y su resumen, coherentes con el código. ValueError si no."""
    if stderr.strip():
        raise ValueError(f'salida de error inesperada: «{stderr.decode("utf-8", "replace").strip()[:120]}»')
    lines = [x for x in stdout.decode('utf-8').splitlines() if x.strip()]
    if not lines or not summary_rx.fullmatch(lines[-1]):
        raise ValueError('sin su resumen final: ejecución incompleta')
    rules, cases, info = {}, [], {}
    for line in lines[:-1]:
        m = FALLA_RULE.fullmatch(line)
        if m and not CASE_ID.fullmatch(m.group(1)) and m.group(1) not in rules:
            items = ast.literal_eval(m.group(3))
            if not isinstance(items, list) or not all(isinstance(x, str) for x in items):
                raise ValueError(f'violaciones ilegibles en FALLA {m.group(1)}')
            rules[m.group(1)] = (int(m.group(2)), items)
        elif line.startswith('FALLA ') and CASE_ID.fullmatch(line.split()[1].rstrip(':')):
            cases.append(line.split()[1].rstrip(':'))
        elif line.startswith('INFO '):
            key = next((k for k, rx in info_rx.items() if rx.fullmatch(line)), None)
            if key is None or key in info:
                raise ValueError(f'línea INFO no reconocida o repetida: «{line[:80]}»')
            info[key] = info_rx[key].fullmatch(line)
        else:
            raise ValueError(f'línea no reconocida: «{line[:80]}»')
    ok, ko = (int(x) for x in summary_rx.fullmatch(lines[-1]).groups())
    if ko != len(rules) + len(cases) or code != (1 if ko else 0) or set(info) != set(info_rx):
        raise ValueError(f'resumen, líneas FALLA, INFO y código de salida incoherentes (código {code})')
    return ok, ko, rules, cases, info


_COUNTER = [0]


def make_temp(label):
    base = os.path.abspath(os.environ.get('TEMP') or os.environ.get('TMP') or os.environ.get('TMPDIR') or '/tmp')
    if (os.path.normcase(base) + os.sep).startswith(_REPO + os.sep) or not os.path.isdir(base):
        raise GitError('directorio temporal no disponible fuera del repositorio')
    _COUNTER[0] += 1
    path = os.path.join(base, f'f35sbxb2-formal-{label}-{os.getpid()}-{_COUNTER[0]}')
    os.mkdir(path)
    return path


def remove_tree(path):
    if not os.path.lexists(path):
        return
    for d, dirs, files in os.walk(path, topdown=False):
        for name in files:
            full = os.path.join(d, name)
            if not os.path.islink(full):
                os.chmod(full, 0o600)
            os.remove(full)
        for name in dirs:
            full = os.path.join(d, name)
            if os.path.islink(full) and os.name != 'nt':
                os.remove(full)
            else:
                os.rmdir(full)
    os.rmdir(path)


class Anchored:
    """HIS: el gate del cierre de gobierno anclado sobre 363273e, en un clon temporal sin remoto, en paralelo."""

    def __init__(self, blob):
        self.tmp, self.proc, self.files, self.blob = make_temp('anclado'), None, [], blob
        try:
            config = os.path.join(self.tmp, 'gitconfig')
            with open(config, 'wb'):
                pass
            env = dict(GIT_ENV, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=config)
            self.repo = os.path.join(self.tmp, 'repo')
            git('clone', '-q', '--shared', '--no-checkout', '-c', 'core.autocrlf=false', ROOT, self.repo,
                cwd=self.tmp, env=env)
            git('remote', 'remove', 'origin', cwd=self.repo, env=env)
            git('checkout', '-q', '-B', GC_BRANCH, GOV_CLOSURE, cwd=self.repo, env=env)
            if git('rev-parse', '--verify', 'HEAD^{commit}', cwd=self.repo).decode('ascii').strip() != GOV_CLOSURE:
                raise GitError('el clon temporal no está en el ancla del cierre de gobierno')
            path = verified_script(GC_GATE, blob, self.repo)
            self.files = [open(os.path.join(self.tmp, name), 'wb') for name in ('salida', 'errores')]
            self.proc = subprocess.Popen([sys.executable, '-I', '-B', path], cwd=self.repo, env=GIT_ENV,
                                         stdout=self.files[0], stderr=self.files[1])
        except BaseException:
            self.close()
            raise

    def result(self):
        try:
            code = self.proc.wait(timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            self.proc.wait()
            raise
        for f in self.files:
            f.close()
        verified_script(GC_GATE, self.blob, self.repo)
        with open(os.path.join(self.tmp, 'salida'), 'rb') as f:
            out = f.read()
        with open(os.path.join(self.tmp, 'errores'), 'rb') as f:
            err = f.read()
        return code, out, err

    def close(self):
        if self.proc is not None and self.proc.poll() is None:
            self.proc.kill()
            self.proc.wait()
        for f in self.files:
            f.close()
        remove_tree(self.tmp)


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
    if DEVELOP_GOV_MERGE not in parents:
        out.append(f'el merge de integración {DEVELOP_GOV_MERGE[:12]} no es ancestro de HEAD')
    return out


def anc_problems(objs):
    out = []
    for commit in CHAIN:
        commit_parts(objs, commit)
    for older, newer in zip(CHAIN, CHAIN[1:]):
        if older not in ancestry(objs, newer):
            out.append(f'{newer[:12]} no desciende de {older[:12]}: la cadena de anclas no corresponde')
    for merge, first, second in ((DEVELOP_MERGE, B2_BASE, SUCCESSOR_FREEZE), (DEVELOP_GOV_MERGE, DEVELOP_MERGE, GOV_CLOSURE)):
        tree, parents = commit_parts(objs, merge)
        if parents != [first, second]:
            out.append(f'el merge {merge[:12]} no tiene como padres {first[:12]} y {second[:12]}')
        if tree != commit_parts(objs, second)[0]:
            out.append(f'el merge {merge[:12]} no tiene el árbol del ancla aprobada {second[:12]}')
    for commit, blobs in ((B1_ANCHOR, B1_GOV_BLOBS), (B2_TRANSITION, B2_GOV_BLOBS), (CLOSURE_TRANSITION, CLOSURE_GOV_BLOBS)):
        root = commit_parts(objs, commit)[0]
        for path, blob in blobs.items():
            if entry(objs, root, path) != ('100644', 'blob', blob):
                out.append(f'{path}: blob de gobierno de {commit[:12]} distinto del registrado')
    return out


# ---------------------------------------------------------------- INT y FLG
def frozen_layers(objs):
    """{etiqueta: (ancla, {carpeta: listado del árbol del ancla})}, con archivos regulares 100644."""
    layers = {}
    for label, anchor, folders in FROZEN:
        root = commit_parts(objs, anchor)[0]
        want = {folder: listing(objs, root, folder) for folder in folders}
        if any(found is None or not found or any(e[:2] != ('100644', 'blob') for e in found.values())
               for found in want.values()):
            raise GitError(f'capa {label}: sus carpetas no son archivos regulares en {anchor[:12]}')
        layers[label] = (anchor, want)
    return layers


def int_problems(objs, parents):
    out = []
    layers = frozen_layers(objs)
    for label, (anchor, want) in layers.items():
        if anchor not in parents:
            out.append(f'capa {label}: su ancla {anchor[:12]} no es ancestro de HEAD')
            continue
        bad = []
        for commit in sorted(descendants(parents, anchor)):
            root = commit_parts(objs, commit)[0]
            diff = [x for folder, files in want.items() for x in listing_diff(folder, listing(objs, root, folder), files)]
            if diff:
                bad.append(f'{commit[:12]}: {diff[:2]}')
        if bad:
            out.append(f'capa {label} distinta de su ancla {anchor[:12]} (modificada, eliminada, renombrada, con otro '
                       f'modo o con archivos extra, aunque se restaure): {bad[:3]}')
        files = {f'{folder}/{rel}': e for folder, found in want.items() for rel, e in found.items()}
        out += index_problems(files, list(want), f'de la capa {label}')
        for folder, found in want.items():
            out += disk_folder(folder, found)
    return out


def flg_problems():
    flagged = [item.decode('utf-8', 'replace') for item in git('ls-files', '-v', '-z').split(b'\x00')
               if item and not item.startswith(b'H ')]
    return [f'flags en el índice (assume-unchanged, skip-worktree o conflictos): {flagged[:5]}'] if flagged else []


# ---------------------------------------------------------------- GOV: cuatro etapas, transición única y monotónica
def gov_entries(objs, commit):
    root = commit_parts(objs, commit)[0]
    return {p: entry(objs, root, p) for p in GOV_PATHS}


def governance(objs):
    """Entradas de cada etapa: {'b1', 'b2', 'cierre'} registradas en sus commits y 'formal' con el delta aplicado al
    blob del cierre de gobierno."""
    want, closure = {}, {}
    for stage, commit in (('b1', B1_ANCHOR), ('b2', B2_TRANSITION), ('cierre', CLOSURE_TRANSITION)):
        want[stage] = gov_entries(objs, commit)
    for path in GOV_PATHS:
        text = blob_text(objs, want['cierre'][path]).decode('utf-8')
        blocks = FORMAL_DELTA.get(path) or []
        if not blocks or any(text.count(before) != 1 for before, _ in blocks):
            raise ValueError(f'{path}: delta del cierre formal vacío o con un bloque antiguo que no aparece exactamente '
                             f'una vez')
        for before, after in blocks:
            text = text.replace(before, after, 1)
        closure[path] = ('100644', 'blob', blob_id(text.encode('utf-8')))
    want['formal'] = closure
    return want


def introduced(objs, parents, order, want, stage):
    """{commit: rutas} de los commits que contienen el blob de una etapa sin que ninguno de sus padres lo contenga."""
    found = {}
    for commit in order:
        here = gov_entries(objs, commit)
        for p in GOV_PATHS:
            if here[p] == want[stage][p] and not any(gov_entries(objs, q)[p] == want[stage][p] for q in parents[commit]):
                found.setdefault(commit, set()).add(p)
    return found


def effective_problems(objs, head, final, texts):
    root = commit_parts(objs, head)[0]
    index = index_entries(GOV_PATHS)
    out = []
    for p in GOV_PATHS:
        if entry(objs, root, p) != final[p]:
            out.append(f'{p}: {texts[0]}')
        if index.get(p) != [(final[p][0], final[p][2], '0')]:
            out.append(f'{p}: {texts[1]}')
        data = disk_bytes(p)
        if data is None or blob_id(data) != final[p][2]:
            out.append(f'{p}: {texts[2]}')
    return out


def gov_problems(objs, parents, head, info):
    want = governance(objs)
    graph = descendants(parents, B1_ANCHOR)
    order = [c for c in topological(parents) if c in graph]          # de los más antiguos a los más recientes
    out = []
    for stage, commit, label in (('b2', B2_TRANSITION, 'de B2'), ('cierre', CLOSURE_TRANSITION, 'del cierre de gobierno')):
        found = introduced(objs, parents, order, want, stage)
        if commit in parents and found != {commit: set(GOV_PATHS)}:
            out.append(f'regla 4: el blob {label} se introduce fuera de {commit[:12]}: '
                       f'{sorted(c[:12] for c in found if c != commit)[:3]}')
    formal = introduced(objs, parents, order, want, 'formal')
    full = [c for c, paths in formal.items() if paths == set(GOV_PATHS)]
    transition = full[0] if len(full) == 1 else None
    info['transition'] = transition
    others = sorted(c[:12] for c in formal if c != transition)
    if others:
        out.append(f'regla 4: introducción del blob del cierre formal fuera de una transición única en las dos rutas: '
                   f'{others[:3]}')
    if transition is None:
        out.append('transición del cierre formal no materializada en un único commit que cambie las dos rutas a la vez')
    else:
        ps = parents[transition]
        if len(ps) != 1:
            out.append(f'regla 2: la transición del cierre formal {transition[:12]} no tiene un solo padre')
        else:
            if gov_entries(objs, ps[0]) != want['cierre']:
                out.append(f'regla 2: el padre de la transición {transition[:12]} no tiene el blob del cierre de '
                           f'gobierno')
            changed = set(name_status(git('diff-tree', '-r', '--no-renames', '--name-status', '-z', ps[0], transition)))
            if changed != set(GOV_PATHS):
                out.append(f'regla 2: la transición {transition[:12]} cambia otras rutas además del gobierno: '
                           f'{sorted(changed ^ set(GOV_PATHS))[:3]}')
        if DEVELOP_GOV_MERGE not in ancestry(objs, transition):
            out.append(f'la transición {transition[:12]} no desciende del merge de integración {DEVELOP_GOV_MERGE[:12]}')
    if FORMAL_TRANSITION is None:
        out.append('transición del cierre formal no registrada en el gate')
    elif transition != FORMAL_TRANSITION:
        out.append(f'transición derivada ({transition[:12] if transition else "ninguna"}) distinta de la registrada '
                   f'({FORMAL_TRANSITION[:12]})')
    after_b2 = descendants(parents, B2_TRANSITION) | {B2_TRANSITION}
    after_closure = (descendants(parents, CLOSURE_TRANSITION) | {CLOSURE_TRANSITION}) if CLOSURE_TRANSITION in parents \
        else set()
    after_formal = (descendants(parents, transition) | {transition}) if transition else set()
    rules = {'formal': 'regla 3: descendiente de la transición del cierre formal sin su blob',
             'cierre': 'regla 3: descendiente de la transición del cierre de gobierno sin su blob',
             'b2': 'regla 3: descendiente de la transición de B2 sin su blob',
             'b1': 'regla 1: commit previo a la transición de B2 sin el blob de B1'}
    bad = []
    for commit in order:
        stage = ('formal' if commit in after_formal else 'cierre' if commit in after_closure else
                 'b2' if commit in after_b2 else 'b1')
        diff = [p for p, e in gov_entries(objs, commit).items() if e != want[stage][p]]
        if diff:
            bad.append(f'{commit[:12]}: {rules[stage]}: {diff}')
    out += bad[:3] + ([f'… y {len(bad) - 3} commits más con un blob de gobierno no admitido'] if len(bad) > 3 else [])
    out += effective_problems(objs, head, want['formal'],
                              ('árbol de HEAD distinto del blob del cierre formal',
                               'índice distinto del blob del cierre formal o en conflicto',
                               'disco distinto del blob del cierre formal, enlace o ausente'))
    return out


def gc_gov_mirror(objs, parents, head):
    """Las violaciones de GOV que el gate del cierre de gobierno informa sobre este HEAD, con sus tres etapas y sus
    textos, y si alguna no es de la clase A de este incremento (regla 3 en commits posteriores a d346597 sin su blob y
    estado efectivo). Que esos commits desciendan de 04895aa lo exigen CTX, GOV y FRZ de este gate."""
    want = {stage: gov_entries(objs, commit) for stage, commit in (('b1', B1_ANCHOR), ('b2', B2_TRANSITION),
                                                                     ('cierre', CLOSURE_TRANSITION))}
    graph = descendants(parents, B1_ANCHOR)
    order = [c for c in topological(parents) if c in graph]
    out, foreign = [], False
    b2_intro, closure_intro = (introduced(objs, parents, order, want, s) for s in ('b2', 'cierre'))
    if b2_intro != {B2_TRANSITION: set(GOV_PATHS)}:
        out.append(f'el blob de gobierno de B2 se introduce fuera de {B2_TRANSITION[:12]} (regla 4): '
                   f'{sorted(c[:12] for c in b2_intro if c != B2_TRANSITION)[:3]}')
        foreign = True
    full = [c for c, paths in closure_intro.items() if paths == set(GOV_PATHS)]
    transition = full[0] if len(full) == 1 else None
    others = sorted(c[:12] for c in closure_intro if c != transition)
    if others:
        out.append(f'regla 4: introducción del blob del cierre fuera de una transición única en las dos rutas: {others[:3]}')
        foreign = True
    if transition is None:
        out.append('transición del cierre no materializada en un único commit que cambie las dos rutas a la vez')
        foreign = True
    else:
        ps = parents[transition]
        if len(ps) != 1:
            out.append(f'regla 2: la transición del cierre {transition[:12]} no tiene un solo padre')
            foreign = True
        else:
            if gov_entries(objs, ps[0]) != want['b2']:
                out.append(f'regla 2: el padre de la transición {transition[:12]} no tiene el blob de gobierno de B2')
                foreign = True
            changed = set(name_status(git('diff-tree', '-r', '--no-renames', '--name-status', '-z', ps[0], transition)))
            if changed != set(GOV_PATHS):
                out.append(f'regla 2: la transición {transition[:12]} cambia otras rutas además del gobierno: '
                           f'{sorted(changed ^ set(GOV_PATHS))[:3]}')
                foreign = True
        if DEVELOP_MERGE not in ancestry(objs, transition):
            out.append(f'la transición {transition[:12]} no desciende del merge de integración {DEVELOP_MERGE[:12]}')
            foreign = True
    if transition != CLOSURE_TRANSITION:
        out.append(f'transición derivada ({transition[:12] if transition else "ninguna"}) distinta de la registrada '
                   f'({CLOSURE_TRANSITION[:12]})')
        foreign = True
    after_b2 = descendants(parents, B2_TRANSITION) | {B2_TRANSITION}
    after_closure = (descendants(parents, transition) | {transition}) if transition else set()
    bad = []
    for commit in order:
        stage = 'cierre' if commit in after_closure else 'b2' if commit in after_b2 else 'b1'
        diff = [p for p, e in gov_entries(objs, commit).items() if e != want[stage][p]]
        if diff:
            rule = {'cierre': 'regla 3: descendiente de la transición del cierre sin su blob',
                    'b2': 'regla 3: descendiente de la transición de B2 sin su blob',
                    'b1': 'regla 1: commit previo a la transición de B2 sin el blob de B1'}[stage]
            bad.append(f'{commit[:12]}: {rule}: {diff}')
            foreign = foreign or stage != 'cierre'
    out += bad[:3] + ([f'… y {len(bad) - 3} commits más con un blob de gobierno no admitido'] if len(bad) > 3 else [])
    out += effective_problems(objs, head, want['cierre'] if transition else want['b2'],
                              ('árbol de HEAD distinto del blob admitido', 'índice distinto del blob admitido o en '
                               'conflicto', 'disco distinto del blob admitido, enlace o ausente'))
    return out, foreign


# ---------------------------------------------------------------- SEM: semántica con piezas verificadas del gate de B1
def load_b1_gate(objs):
    """Gate de B1 desde los bytes de su blob en el ancla, verificado al leerlo; nunca desde el disco (Q5)."""
    data = blob_text(objs, entry(objs, commit_parts(objs, B1_ANCHOR)[0], B1_GATE))
    path = os.path.join(ROOT, *B1_GATE.split('/'))
    module = types.ModuleType('f35sbxb_gate_b1_verificado_cierre_formal')
    module.__file__ = path
    exec(compile(data, path, 'exec', dont_inherit=True), module.__dict__)
    return module


def semantics(b1, allowed_b2):
    """Declaraciones de estado de B1 y de B2, como en el gate de B2, con el ciclo de vida de B2 indicado."""
    declared = [(s, a) for s, a in b1.DECLARED if s != 'b1'] + [
        ('b1', ('cerrad', 'congelad', 'implementad') + b1.LOCKED),
        ('b2', allowed_b2 + b1.LOCKED)]
    decl_rx = [(re.compile(r'(?<![\w-])(' + subj + r')(?![\w-])(?:\s*(?::=|==|=|:|->|→)\s*|\s+(no\s+)?(?:se\s+)?'
                           + b1.DECL_COPULA + r'\s+(?:[a-z]+mente\s+)?|\s+)' + b1.STATE_VALUE), allowed)
               for subj, allowed in declared]
    verb_rx = [(re.compile(r'(?<![\w-])' + b1.DECL_NEG + r'(?:se\s+)?(?:(?:lo|la|los|las)\s+)?(?<![\w-])(?:' + b1.DECL_VERB +
                           r')(?![\w-])\s+(?:[a-z]+mente\s+)?(?:(?:el|la|los|las|al|a|the)\s+)?(?P<subj>' + subj +
                           r')(?![\w-])'), allowed, rx) for (subj, allowed), (rx, _) in zip(declared, decl_rx)] + \
              [(re.compile(r'(?<![\w-])(?P<subj>' + subj + r')(?![\w-])\s+' + b1.DECL_NEG + r'se\s+(?:[a-z]+mente\s+)?(?:' +
                           b1.DECL_VERB + r')(?![\w-])'), allowed, rx) for (subj, allowed), (rx, _) in zip(declared, decl_rx)]
    return decl_rx, verb_rx


def contradictions(b1, sem, text, forbidden_rx):
    """contradictions2() del gate de B2 con el ciclo de vida de B2 indicado (permitidos y prohibidos)."""
    decl_rx, verb_rx = sem
    out = []
    for body in b1.sentences(text, cite=True):
        if b1.EXAMPLE_PREFIX_RX.match(body.strip(' |-')):
            continue
        found = []
        for rx, allowed in decl_rx:
            for m in rx.finditer(body):
                found.append((m, allowed, b1.state_value(bool(m.group(2) or m.group(3)), m.group(4), body[m.end():])))
        for rx, allowed, decl in verb_rx:
            for m in rx.finditer(body):
                if decl.match(body, m.start('subj')):
                    continue
                k = next(int(g[1:]) for g, v in m.groupdict().items() if v and g.startswith('v'))
                found.append((m, allowed, b1.state_value(bool(m.group('neg')), b1.DECL_VERBS[k][1], body[m.end():])))
        for m in forbidden_rx.finditer(body):
            if any(t in b1.NEG_WORDS or t.startswith(b1.NEG_PREFIXES) for t in m.group(1).split()):
                continue
            found.append((m, ('implementad',), m.group(2)))
        for m, allowed, value in found:
            if b1.admitted(value, allowed):
                continue
            if b1.DECL_NEG_RX.search(re.split(r'[.,;:!?|]', body[:m.start()])[-1]):
                continue
            out.append(f'«{m.group(0).strip()}»')
        out += b1.g0sbx_unrestricted(body) + b1.approval_grants(body)
    return out


def reopening(b1, text):
    """Reapertura de B2 o estado de B2 que no es el cierre (pendiente, abierta, en desarrollo, candidata, no cerrada)."""
    out = []
    for body in b1.sentences(text, cite=True):
        for m in B2_REOPEN_RX.finditer(body):
            if any(t in b1.NEG_WORDS or t.startswith(b1.NEG_PREFIXES) for t in m.group(1).split()):
                continue
            if b1.DECL_NEG_RX.search(re.split(r'[.,;:!?|]', body[:m.start()])[-1]):
                continue
            out.append(f'«{m.group(0).strip()}»')
    return out


def layer_doc_problems(objs, root, b1, sem, forbidden_rx, files):
    out = []
    for path in files:
        found = entry(objs, root, path)
        if found is None:
            out.append(f'{path}: ausente en HEAD')
            continue
        data = blob_text(objs, found)
        if len(data) > b1.MAX_BYTES or b'\x00' in data or b'\r' in data or data.startswith(b'\xef\xbb\xbf'):
            out.append(f'{path}: binario, CR, BOM o tamaño excesivo')
            continue
        text = data.decode('utf-8')
        if not path.endswith('.md'):
            continue
        hits = [m.group(0) for rx in b1.PII for m in [rx.search(text)] if m]
        if hits:
            out.append(f'{path}: posible dato personal: {hits[:2]}')
        claims = b1.positive_claims(text)
        if claims:
            out.append(f'{path}: afirmación positiva que habilita una capacidad prohibida: {claims[:2]}')
        bad = contradictions(b1, sem, text, forbidden_rx)
        if bad:
            out.append(f'{path}: declaraciones de estado contradictorias con el gobierno vigente: {bad[:3]}')
    return out


def gov_sections(text):
    sections = re.findall(r'^## Estado vigente F34E\s*\n(.*?)(?=^## |\Z)', text, re.M | re.S)
    header = '\n'.join(ln for ln in text.splitlines() if ln.startswith('Última actualización:'))
    return sections, header


def sem_problems(objs, head, b1):
    sem = semantics(b1, B2_ALLOWED)
    root = commit_parts(objs, head)[0]
    closure_root = commit_parts(objs, CLOSURE_TRANSITION)[0]
    out = []
    for path in GOV_PATHS:
        text = blob_text(objs, entry(objs, root, path)).decode('utf-8')
        old = blob_text(objs, entry(objs, closure_root, path)).decode('utf-8')
        sections, header = gov_sections(text)
        if len(sections) != 1:
            out.append(f'{path}: se exige una única sección «Estado vigente F34E»')
            continue
        section = sections[0]
        if [ln for ln in section.splitlines() if re.match(r'^- [^=\n]+ = ', ln)] != b1.STATES:
            out.append(f'{path}: los trece estados de gobierno no son exactamente los vigentes')
        b_states = {' '.join(m.split()) for m in b1.B_STATE_RX.findall(section + '\n' + header)}
        if b_states != {'INICIADA'}:
            out.append(f'{path}: F35-SBX-B debe figurar solo INICIADA en el estado vigente: {sorted(b_states)}')
        if not all(fragment in section for fragment in CLOSED_SECTION):
            out.append(f'{path}: el estado vigente no declara a B2 CERRADA, CONGELADA E INTEGRADA')
        if path == 'docs/PROGRESS.md' and CLOSED_HEADER not in header:
            out.append(f'{path}: la cabecera no declara a B2 CERRADA E INTEGRADA')
        if PENDING in section or PENDING in header:
            out.append(f'{path}: el estado vigente aún declara a B2 {PENDING}')
        reopen = reopening(b1, section + '\n' + header)
        if reopen:
            out.append(f'{path}: reapertura o estado de B2 distinto del cierre: {reopen[:3]}')
        before = set(old.splitlines())
        added = '\n'.join(ln for ln in text.splitlines() if ln not in before)
        bad = contradictions(b1, sem, section + '\n' + header + '\n' + added, B2_FORBIDDEN_RX)
        if bad:
            out.append(f'{path}: declaraciones de estado contradictorias con el gobierno vigente: {bad[:3]}')
        claims = b1.positive_claims(added)
        if claims:
            out.append(f'{path}: líneas nuevas que afirman habilitar una capacidad prohibida: {claims[:2]}')
    out += layer_doc_problems(objs, root, b1, sem, B2_FORBIDDEN_RX, LAYER_FILES)
    return out


def gc_sem_mirror(objs, head, b1):
    """Las violaciones de SEM que el gate del cierre de gobierno informa sobre este HEAD, con su vocabulario."""
    sem = semantics(b1, GC_B2_ALLOWED)
    root = commit_parts(objs, head)[0]
    b2_root = commit_parts(objs, B2_TRANSITION)[0]
    out = []
    for path in GOV_PATHS:
        text = blob_text(objs, entry(objs, root, path)).decode('utf-8')
        old = blob_text(objs, entry(objs, b2_root, path)).decode('utf-8')
        sections, header = gov_sections(text)
        if len(sections) != 1:
            out.append(f'{path}: se exige una única sección «Estado vigente F34E»')
            continue
        section = sections[0]
        if [ln for ln in section.splitlines() if re.match(r'^- [^=\n]+ = ', ln)] != b1.STATES:
            out.append(f'{path}: los trece estados de gobierno no son exactamente los vigentes')
        b_states = {' '.join(m.split()) for m in b1.B_STATE_RX.findall(section + '\n' + header)}
        if b_states != {'INICIADA'}:
            out.append(f'{path}: F35-SBX-B debe figurar solo INICIADA en el estado vigente: {sorted(b_states)}')
        if PENDING not in section:
            out.append(f'{path}: el estado vigente no declara a B2 {PENDING}')
        before = set(old.splitlines())
        added = '\n'.join(ln for ln in text.splitlines() if ln not in before)
        bad = contradictions(b1, sem, section + '\n' + header + '\n' + added, GC_B2_FORBIDDEN_RX)
        if bad:
            out.append(f'{path}: declaraciones de estado contradictorias con el gobierno vigente: {bad[:3]}')
        claims = b1.positive_claims(added)
        if claims:
            out.append(f'{path}: líneas nuevas que afirman habilitar una capacidad prohibida: {claims[:2]}')
    out += layer_doc_problems(objs, root, b1, sem, GC_B2_FORBIDDEN_RX, GC_LAYER_FILES)
    return out


# ---------------------------------------------------------------- MAT: el gate de B2 sobre HEAD, con su clase A predicha
def predicted_b2(objs, parents, head, branch, extra_paths, lifecycle, own_branch):
    """Lo que el gate de B2 tiene que informar sobre este HEAD si solo cambian la rama, las rutas posteriores al
    candidato y el gobierno: {regla: (recuento o None, comprobador de violaciones)}, los casos en falla y el contenido
    distinto. extra_paths: rutas añadidas después de B2-SUCCESSOR-FREEZE admitidas en SCP; lifecycle: ítems semánticos
    de GOV admitidos; own_branch: la única rama en la que CTX puede fallar."""
    post = name_status(git('diff-tree', '-r', '--no-renames', '--name-status', '-z', CANDIDATE, SUCCESSOR_FREEZE))
    if set(post.values()) != {'A'} or len(post) != 11:
        raise GitError('las rutas posteriores al candidato no son las once añadidas por el freeze, el sucesor y su cierre')
    allowed_scp = set(post) | set(extra_paths)
    b2 = {p: ('100644', 'blob', b) for p, b in B2_GOV_BLOBS.items()}
    b1_bytes = {p: blob_text(objs, ('100644', 'blob', b)) for p, b in B1_GOV_BLOBS.items()}
    b2_bytes = {p: blob_text(objs, ('100644', 'blob', b)) for p, b in B2_GOV_BLOBS.items()}
    graph = descendants(parents, B1_ANCHOR)
    after = descendants(parents, B2_TRANSITION) | {B2_TRANSITION}
    rule3 = {c[:12] for c in graph if c in after and gov_entries(objs, c) != b2}
    reintroduced = any(gov_entries(objs, c)[p] == b2[p] and not any(gov_entries(objs, q)[p] == b2[p] for q in parents[c])
                       for c in graph if c != B2_TRANSITION for p in GOV_PATHS)
    root, index = commit_parts(objs, head)[0], index_entries(GOV_PATHS)
    effective = []
    for p in GOV_PATHS:
        disk = disk_bytes(p)
        if entry(objs, root, p) != b2[p]:
            effective.append(EFFECTIVE['árbol'].format(p))
        if index.get(p) != [('100644', b2[p][2], '0')] or any(f for f in flags(p)):
            effective.append(EFFECTIVE['índice'].format(p))
        if disk is None or blob_id(disk) != b2[p][2]:
            effective.append(EFFECTIVE['disco'].format(p))
    b1f_count = len(rule3) + (1 if reintroduced else 0) + len(effective)

    def b1f_item(x):
        m = RULE3_ITEM.fullmatch(x)
        return (m and (m.group(1) or m.group(2)) in rule3) or (reintroduced and RULE4_ITEM.fullmatch(x)) or x in effective
    content = [GOV_CONTENT.format(p) for p in GOV_PATHS if disk_bytes(p) not in (b1_bytes[p], b2_bytes[p])]
    expected = {'SCP': (3 * len(allowed_scp), lambda x: bool((m := SCP_ITEM.fullmatch(x)) and m.group(2) in allowed_scp))}
    if branch == own_branch:
        expected['CTX'] = (1, lambda x: x == f'rama no permitida o HEAD separado: «{own_branch}»')
    if b1f_count:
        expected['B1F'] = (b1f_count, b1f_item)
        expected['DYN'] = (1, lambda x: x.startswith('P25: [') and all(
            b1f_item(y) for y in ast.literal_eval(x[5:])))
    expected['GOV'] = (None, lambda x: x in content or bool((m := GOV_SEMANTIC.fullmatch(x)) and
                                                             set(ast.literal_eval(m.group(2))) <= lifecycle))
    return expected, (['P25'] if b1f_count else []), content


def b2_problems(observed, expected, expected_cases, content):
    """Las violaciones de la evaluación material (los textos del cierre de gobierno) sobre una salida observada del gate
    de B2, frente a una predicción."""
    code, ok, ko, rules, cases, info = observed
    out = []
    if info['TRN'].groups() != (B2_TRANSITION, B2_TRANSITION):
        out.append(f'transición de B2 derivada o registrada distinta de {B2_TRANSITION[:12]}')
    if ok + ko != B2_TOTAL:
        out.append(f'el gate de B2 informa {ok + ko} comprobaciones, no {B2_TOTAL}')
    material = sorted(set(rules) - set(expected))
    if material:
        out.append(f'el gate de B2 sobre HEAD incumple comprobaciones materiales: reglas {material}')
    for rid, (count, valid) in expected.items():
        n, items = rules.get(rid, (0, []))
        if rid == 'GOV':
            if n and (n > 3 or n != len(items) or not all(valid(x) for x in items) or
                      not set(content) <= set(items)):
                out.append(f'GOV del gate de B2 no se explica solo por la divergencia de gobierno y el ciclo de vida '
                           f'de B2: {items[:3]}')
            elif not n and content:
                out.append('GOV del gate de B2 no informa la divergencia de gobierno observada')
            continue
        if n != count or len(items) != min(n, 3) or not all(valid(x) for x in items):
            out.append(f'{rid} del gate de B2 con {n} violaciones, no las {count} que predice el estado: {items[:2]}')
    if sorted(cases) != expected_cases:
        out.append(f'casos del gate de B2 en falla distintos de los previstos ({expected_cases}): {sorted(cases)[:5]}')
    return out


def mat_line(observed, scp_expected, label):
    code, ok, ko, rules, cases, _ = observed
    return (f'INFO MAT: gate de B2 sobre HEAD: código {code}; {ok} correctas, {ko} fallas; reglas en falla: '
            f'{", ".join(sorted(rules)) or "ninguna"}; casos en falla: {", ".join(sorted(cases)) or "ninguno"}; SCP: '
            f'{rules.get("SCP", (0,))[0]} violaciones ({label} {scp_expected})')


def mat_problems(objs, parents, head, branch, gate_blob):
    try:
        code, stdout, stderr = run_script(B2_GATE, gate_blob, ROOT)
    except ValueError as e:
        return [str(e)], f'INFO MAT: gate de B2 sobre HEAD no ejecutado: {e}', None
    ok, ko, rules, cases, info = parse_output(code, stdout, stderr, B2_SUMMARY, {'TRN': B2_INFO})
    observed = (code, ok, ko, rules, cases, info)
    expected, expected_cases, content = predicted_b2(objs, parents, head, branch, GC_LAYER_FILES + LAYER_FILES,
                                                     B2_LIFECYCLE_ITEMS, BRANCH)
    return b2_problems(observed, expected, expected_cases, content), \
        mat_line(observed, expected['SCP'][0], 'previstas'), observed


# ---------------------------------------------------------------- SUC: B2-SUCCESSOR-FREEZE sobre HEAD
def sf_blob(objs):
    found = entry(objs, commit_parts(objs, SUCCESSOR_FREEZE)[0], SF_VALIDATOR)
    if found is None or found[:2] != ('100644', 'blob'):
        raise GitError('el validador de B2-SUCCESSOR-FREEZE no es un blob regular en su ancla')
    return found[2]


def suc_eval(observed, head, mat_rules, allowed):
    """Las violaciones de SUC (los textos del cierre de gobierno) sobre una salida observada de B2-SUCCESSOR-FREEZE,
    con las rutas (y su estado) que su ALC puede nombrar."""
    code, ok, ko, rules, cases, info = observed
    out = []
    if set(rules) != {'VIG', 'ALC'} or cases or ok + ko != SF_TOTAL:
        out.append(f'B2-SUCCESSOR-FREEZE sobre HEAD falla en {sorted(rules)}: solo pueden fallar VIG y ALC (clase A)')
    n, items = rules.get('ALC', (0, []))
    planes = set()
    for item in items:
        m = SF_ALC.fullmatch(item)
        paths = ast.literal_eval(m.group(2)) if m else None
        if not m or not paths or not all(isinstance(t, tuple) and t in allowed for t in paths):
            planes = None
            break
        planes.add(m.group(1))
    if 'ALC' in rules and (n != len(PLANES) or planes is None or planes != set(PLANES)):
        out.append(f'{GC_SUC_PREFIX}{items[:2]}')
    vig = info['VIG']
    succ = {x.strip() for x in vig.group(4).split(',') if x.strip() and x.strip() != 'ninguna'}
    b2 = {x.strip() for x in vig.group(5).split(',') if x.strip() and x.strip() != 'ninguna'}
    if not succ or not succ <= {'ALC', 'CON', 'MAT'}:
        out.append(f'el gate sucesor sobre HEAD falla en {sorted(succ)}: solo ALC, CON o MAT (clase A)')
    if mat_rules is not None and b2 != mat_rules:
        out.append(f'VIG informa reglas del gate de B2 ({sorted(b2)}) distintas de las que observa MAT ({sorted(mat_rules)})')
    if info['ANC'].groups() != (CANDIDATE, FREEZE, SUCCESSOR, head):
        out.append('B2-SUCCESSOR-FREEZE no informa las anclas registradas y este HEAD')
    if info['FRZ'].group(1) != SUCCESSOR_FREEZE:
        out.append(f'ancla derivada {info["FRZ"].group(1)[:12]} distinta de la aprobada {SUCCESSOR_FREEZE[:12]}: '
                   f'ancla no autenticada')
    line = (f'INFO SUC: B2-SUCCESSOR-FREEZE sobre HEAD: código {code}; {ok} correctas, {ko} fallas; reglas en falla: '
            f'{", ".join(sorted(rules)) or "ninguna"}; gate sucesor en falla: {", ".join(sorted(succ)) or "ninguna"}; '
            f'ancla derivada {info["FRZ"].group(1)}')
    return out, line


def suc_problems(head, blob, mat_rules):
    try:
        code, stdout, stderr = run_script(SF_VALIDATOR, blob, ROOT)
    except ValueError as e:
        return [str(e)], f'INFO SUC: B2-SUCCESSOR-FREEZE sobre HEAD no ejecutado: {e}', None
    ok, ko, rules, cases, info = parse_output(code, stdout, stderr, SF_SUMMARY, SF_INFO)
    observed = (code, ok, ko, rules, cases, info)
    out, line = suc_eval(observed, head, mat_rules, set(GC_SCOPE.items()) | set(SCOPE.items()))
    return out, line, observed


# ---------------------------------------------------------------- HIS y GCL: el cierre de gobierno, anclado y sobre HEAD
def gc_blob(objs):
    found = entry(objs, commit_parts(objs, GOV_CLOSURE)[0], GC_GATE)
    if found is None or found[:2] != ('100644', 'blob'):
        raise GitError('el gate del cierre de gobierno no es un blob regular en su ancla')
    return found[2]


def his_problems(code, stdout, stderr):
    ok, ko, rules, cases, info = parse_output(code, stdout, stderr, GC_SUMMARY, GC_INFO)
    out = []
    if code != 0 or ko or rules or cases or ok != GC_TOTAL:
        out.append(f'el cierre de gobierno anclado sobre {GOV_CLOSURE[:12]} no da {GC_TOTAL}/0: {sorted(rules)}')
    if info['FRZ'].group(1) != GOV_CLOSURE:
        out.append(f'ancla derivada {info["FRZ"].group(1)[:12]} distinta de la aprobada {GOV_CLOSURE[:12]}')
    if info['GOV'].groups() != (CLOSURE_TRANSITION, CLOSURE_TRANSITION):
        out.append(f'transición del cierre de gobierno derivada o registrada distinta de {CLOSURE_TRANSITION[:12]}')
    if info['ANC'].group(3) != DEVELOP_MERGE or info['ANC'].group(4) != GOV_CLOSURE:
        out.append('el cierre de gobierno anclado no informa su integración y su ancla como HEAD')
    if info['HIS'].groups() != (SUCCESSOR_FREEZE, '0', str(SF_TOTAL), '0', SUCCESSOR_FREEZE):
        out.append('el cierre de gobierno anclado no acredita B2-SUCCESSOR-FREEZE en 12/0 con su ancla')
    line = (f'INFO HIS: B2-GOVERNMENT-CLOSURE anclado sobre {GOV_CLOSURE}: código {code}; {ok} correctas, {ko} fallas; '
            f'ancla derivada {info["FRZ"].group(1)}; transición derivada {info["GOV"].group(1)}')
    return out, line


def gc_alc_mirror(objs, head):
    """Las violaciones de ALC que el gate del cierre de gobierno informa sobre este HEAD."""
    out = []
    for plane, args in (('HEAD', ('diff', '--name-status', '--no-renames', '-z', DEVELOP_MERGE, 'HEAD')),
                        ('árbol', ('diff', '--name-status', '--no-renames', '-z', DEVELOP_MERGE)),
                        ('índice', ('diff', '--cached', '--name-status', '--no-renames', '-z', DEVELOP_MERGE))):
        found = name_status(git(*args))
        if found != GC_SCOPE:
            out.append(f'{plane}: alcance distinto del enumerado para este incremento: '
                       f'{sorted(set(found.items()) ^ set(GC_SCOPE.items()))[:3]}')
    untracked = [x for x in git('ls-files', '--others', '--exclude-standard', '-z').decode('utf-8').split('\x00') if x]
    if untracked:
        out.append(f'archivos sin seguimiento fuera del alcance: {untracked[:5]}')
    root = commit_parts(objs, head)[0]
    own = {}
    for folder, names in GC_LAYER_DIRS.items():
        found = listing(objs, root, folder)
        if found is None or set(found) != set(names) or any(e[:2] != ('100644', 'blob') for e in found.values()):
            out.append(f'{folder}: en HEAD no contiene exactamente sus archivos regulares')
            continue
        own.update({f'{folder}/{rel}': e for rel, e in found.items()})
        out += disk_folder(folder, found)
    out += index_problems(own, list(GC_LAYER_DIRS), 'de HEAD en esta capa')
    return out


def closure_lifecycle(items, content):
    """GOV del gate de B2 explicado solo por el contenido del gobierno y por el ciclo de vida de B2, con «cerrada»
    entre sus ítems: lo único que el cierre de gobierno rechaza por este incremento."""
    named = set()
    for x in items:
        m = GOV_SEMANTIC.fullmatch(x)
        if x in content:
            continue
        if not m:
            return False
        named |= set(ast.literal_eval(m.group(2)))
    return set(content) <= set(items) and bool(named & GC_CLOSED_ITEMS) and named <= GC_LIFECYCLE_ITEMS | GC_CLOSED_ITEMS


def gcl_expected(objs, parents, head, branch, b1, mat_obs, suc_obs):
    """Lo que el gate del cierre de gobierno tiene que informar sobre este HEAD (sus textos), y las razones por las que
    eso no sería solo la clase A de este incremento."""
    expected, notes = {}, []
    expected['CTX'] = ([f'rama no permitida o HEAD separado: «{branch or "HEAD separado"}»'] if branch not in GC_BRANCHES
                       else []) + ([f'el merge de integración {DEVELOP_MERGE[:12]} no es ancestro de HEAD']
                                   if DEVELOP_MERGE not in parents else [])
    if expected['CTX'] != ([f'rama no permitida o HEAD separado: «{BRANCH}»'] if branch == BRANCH else []):
        notes.append(f'CTX del cierre de gobierno no se explica solo por la rama de este incremento: {expected["CTX"][:2]}')
    mat_rules = set(mat_obs[3])
    gc_view = predicted_b2(objs, parents, head, branch, GC_LAYER_FILES, GC_LIFECYCLE_ITEMS, GC_BRANCH)
    expected['MAT'] = b2_problems(mat_obs, *gc_view)
    scp_n = mat_obs[3].get('SCP', (0,))[0]
    own_scp = 3 * (11 + len(GC_LAYER_FILES) + len(LAYER_FILES))
    content = gc_view[2]
    for item in expected['MAT']:
        if item == GC_MATERIAL_CTX and branch == BRANCH:
            continue
        if item.startswith(GC_SCP_PREFIX) and scp_n == own_scp:
            continue
        if item.startswith(GC_GOV_PREFIX) and closure_lifecycle(ast.literal_eval(item[len(GC_GOV_PREFIX):]), content):
            continue
        notes.append(f'MAT del cierre de gobierno no se explica solo por este incremento: {item[:120]}')
    expected['SUC'] = suc_eval(suc_obs, head, mat_rules, set(GC_SCOPE.items()))[0]
    if len(expected['SUC']) != 1 or not expected['SUC'][0].startswith(GC_SUC_PREFIX):
        notes.append(f'SUC del cierre de gobierno no se explica solo por las rutas de este incremento: '
                     f'{expected["SUC"][:2]}')
    expected['GOV'], foreign = gc_gov_mirror(objs, parents, head)
    if foreign:
        notes.append('GOV del cierre de gobierno informa algo más que la transición del cierre formal')
    expected['SEM'] = gc_sem_mirror(objs, head, b1)
    for item in expected['SEM']:
        m = re.fullmatch(r'(CLAUDE\.md|docs/PROGRESS\.md): declaraciones de estado contradictorias con el gobierno '
                         r'vigente: (\[.*\])', item)
        if item in (f'{p}: el estado vigente no declara a B2 {PENDING}' for p in GOV_PATHS):
            continue
        if m and set(ast.literal_eval(m.group(2))) <= GC_CLOSED_ITEMS:
            continue
        notes.append(f'SEM del cierre de gobierno no se explica solo por el cierre formal: {item[:120]}')
    expected['ALC'] = gc_alc_mirror(objs, head)
    own = sorted((p, 'A') for p in LAYER_FILES)[:3]
    if expected['ALC'] != [f'{plane}: alcance distinto del enumerado para este incremento: {own}' for plane in PLANES]:
        notes.append(f'ALC del cierre de gobierno no se explica solo por las rutas de esta capa: {expected["ALC"][:2]}')
    return {rid: items for rid, items in expected.items() if items}, notes, gc_view[0]['SCP'][0]


def gcl_problems(objs, parents, head, branch, blob, b1, mat_obs, suc_obs):
    if mat_obs is None or suc_obs is None:
        return ['no verificable sin la ejecución de MAT y de SUC sobre este HEAD'], \
            'INFO GCL: B2-GOVERNMENT-CLOSURE sobre HEAD no clasificado'
    try:
        code, stdout, stderr = run_script(GC_GATE, blob, ROOT)
    except ValueError as e:
        return [str(e)], f'INFO GCL: B2-GOVERNMENT-CLOSURE sobre HEAD no ejecutado: {e}'
    ok, ko, rules, cases, info = parse_output(code, stdout, stderr, GC_SUMMARY, GC_INFO)
    expected, notes, gc_scp = gcl_expected(objs, parents, head, branch, b1, mat_obs, suc_obs)
    out = list(notes)
    if set(rules) != set(expected) or cases or ok + ko != GC_TOTAL:
        out.append(f'el cierre de gobierno sobre HEAD falla en {sorted(rules)}, no en {sorted(expected)}')
    for rid, items in expected.items():
        n, shown = rules.get(rid, (0, []))
        if n != len(items) or shown != items[:3]:
            out.append(f'{rid} del cierre de gobierno con {n} violaciones distintas de las previstas: {shown[:2]}')
    if info['GOV'].groups() != (CLOSURE_TRANSITION, CLOSURE_TRANSITION):
        out.append(f'el cierre de gobierno no deriva ni registra su transición {CLOSURE_TRANSITION[:12]}')
    if info['FRZ'].group(1) != GOV_CLOSURE:
        out.append(f'el cierre de gobierno deriva su capa en {info["FRZ"].group(1)[:12]}, no en {GOV_CLOSURE[:12]}')
    if info['HIS'].groups() != (SUCCESSOR_FREEZE, '0', str(SF_TOTAL), '0', SUCCESSOR_FREEZE):
        out.append('el cierre de gobierno no acredita B2-SUCCESSOR-FREEZE anclado en 12/0 con su ancla')
    if info['ANC'].group(3) != DEVELOP_MERGE or info['ANC'].group(4) != head:
        out.append('el cierre de gobierno no informa su integración y este HEAD')
    if info['MAT'].group(0) != mat_line(mat_obs, gc_scp, 'previstas'):
        out.append('la línea INFO de MAT del cierre de gobierno no es la que da la salida del gate de B2 observada')
    if info['SUC'].group(0) != suc_eval(suc_obs, head, set(mat_obs[3]), set(GC_SCOPE.items()))[1]:
        out.append('la línea INFO de SUC del cierre de gobierno no es la que da la salida de B2-SUCCESSOR-FREEZE observada')
    line = (f'INFO GCL: B2-GOVERNMENT-CLOSURE sobre HEAD: código {code}; {ok} correctas, {ko} fallas; reglas en falla: '
            f'{", ".join(sorted(rules)) or "ninguna"}; previstas: {", ".join(sorted(expected)) or "ninguna"}')
    return out, line


# ---------------------------------------------------------------- ALC, FRZ y DEP
def alc_problems(objs, head):
    out = []
    for plane, args in (('HEAD', ('diff', '--name-status', '--no-renames', '-z', DEVELOP_GOV_MERGE, 'HEAD')),
                        ('árbol', ('diff', '--name-status', '--no-renames', '-z', DEVELOP_GOV_MERGE)),
                        ('índice', ('diff', '--cached', '--name-status', '--no-renames', '-z', DEVELOP_GOV_MERGE))):
        found = name_status(git(*args))
        if found != SCOPE:
            out.append(f'{plane}: alcance distinto del enumerado para este incremento: '
                       f'{sorted(set(found.items()) ^ set(SCOPE.items()))[:3]}')
    untracked = [x for x in git('ls-files', '--others', '--exclude-standard', '-z').decode('utf-8').split('\x00') if x]
    if untracked:
        out.append(f'archivos sin seguimiento fuera del alcance: {untracked[:5]}')
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
    if DEVELOP_GOV_MERGE not in parents:
        return [f'el merge de integración {DEVELOP_GOV_MERGE[:12]} no es ancestro de HEAD']
    after = descendants(parents, DEVELOP_GOV_MERGE)
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
        modules, dynamic = set(), []
        owner = {}
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
        authorized = sorted(dynamic) == [('compile', LOADER), ('exec', LOADER)] if path == VALIDATOR else not dynamic
        if not authorized:
            out.append(f'{path}: ejecución dinámica de código fuera de la carga verificada del gate de B1: '
                       f'{sorted(dynamic)[:4]}')
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

    check('DEP', dep_problems)
    try:
        problems, head, shallow = ent_problems()
    except ERRORS as e:
        closed([r for r in ORDER if r != 'DEP'], f'repositorio Git ({e.__class__.__name__}: {e})')
        return viol, info
    viol['ENT'] += problems
    check('FLG', flg_problems)
    if shallow:
        closed([r for r in ORDER if r not in ('ENT', 'FLG', 'DEP')], 'repositorio superficial: historia incompleta')
        return viol, info
    info.append(f'INFO ANC: anclas registradas {", ".join(c[:12] for c in CHAIN)}; ancla aprobada del cierre de gobierno '
                f'{GOV_CLOSURE}; integración {DEVELOP_GOV_MERGE}; HEAD {head}')
    objs, anchored = None, None
    try:
        objs = Objects()
        parents = branch = None
        try:
            parents = ancestry(objs, head)
            branch = current_branch()
        except ERRORS as e:
            closed(('CTX', 'GCL', 'MAT', 'INT', 'GOV', 'FRZ'), f'historia desde HEAD ({e.__class__.__name__}: {e})')
        if parents is not None:
            check('CTX', ctx_problems, branch, parents)
        check('ANC', anc_problems, objs)
        blob = gate_blob = sf = None
        try:
            blob = gc_blob(objs)
            anchored = Anchored(blob)
        except ERRORS as e:
            closed(('HIS',), f'ejecución anclada del cierre de gobierno ({e.__class__.__name__}: {e})')
            info.append(f'INFO HIS: B2-GOVERNMENT-CLOSURE anclado no ejecutado: {e}')
        try:
            gate = entry(objs, commit_parts(objs, CANDIDATE)[0], B2_GATE)
            if gate is None or gate[:2] != ('100644', 'blob'):
                raise GitError('el gate de B2 no es un blob regular en el candidato')
            gate_blob = gate[2]
        except ERRORS as e:
            closed(('MAT',), f'gate de B2 en el candidato ({e.__class__.__name__}: {e})')
        try:
            sf = sf_blob(objs)
        except ERRORS as e:
            closed(('SUC',), f'validador de B2-SUCCESSOR-FREEZE en su ancla ({e.__class__.__name__}: {e})')
        b1 = None
        try:
            b1 = load_b1_gate(objs)
        except ERRORS as e:
            closed(('SEM', 'GCL'), f'gate de B1 verificado ({e.__class__.__name__}: {e})')
        mat_obs = suc_obs = None
        if gate_blob is not None and parents is not None:
            mat = check('MAT', mat_problems, objs, parents, head, branch, gate_blob)
            if mat:
                info.append(mat[0])
                mat_obs = mat[1]
        if sf is not None:
            suc = check('SUC', suc_problems, head, sf, set(mat_obs[3]) if mat_obs else None)
            if suc:
                info.append(suc[0])
                suc_obs = suc[1]
        if blob is not None and parents is not None and b1 is not None:
            gcl = check('GCL', gcl_problems, objs, parents, head, branch, blob, b1, mat_obs, suc_obs)
            if gcl:
                info.append(gcl[0])
        elif blob is None:
            closed(('GCL',), 'gate del cierre de gobierno no verificable')
        if parents is not None:
            check('INT', int_problems, objs, parents)
            check('GOV', gov_problems, objs, parents, head, notes)
            check('FRZ', frz_problems, objs, head, parents, notes)
        if b1 is not None:
            check('SEM', sem_problems, objs, head, b1)
        check('ALC', alc_problems, objs, head)
        if anchored is not None:
            his = check('HIS', lambda: his_problems(*anchored.result()))
            if his:
                info.append(his[0])
    except ERRORS as e:
        closed(('CTX', 'ANC', 'HIS', 'GCL', 'SUC', 'MAT', 'INT', 'GOV', 'SEM', 'ALC', 'FRZ'),
               f'objetos Git ({e.__class__.__name__}: {e})')
    finally:
        if anchored is not None:
            try:
                anchored.close()
            except OSError as e:
                viol['HIS'].append(f'limpieza incompleta del clon temporal ({e.__class__.__name__}): falla cerrado')
        if objs is not None:
            objs.close()
    info.append(f'INFO GOV: transición del cierre formal derivada: {notes["transition"] or "ninguna"}; registrada: '
                f'{FORMAL_TRANSITION or "ninguna"}')
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
    print(f'validate_f35sbxb2_cierre_formal: {len(ORDER) - len(fallas)} comprobaciones correctas, {len(fallas)} fallas')
    sys.exit(1 if fallas else 0)


if __name__ == '__main__':
    main()
