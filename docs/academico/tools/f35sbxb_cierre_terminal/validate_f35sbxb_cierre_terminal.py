"""F35-SBX-B — gate sucesor del cierre terminal (validate_f35sbxb_cierre_terminal.py).

Uso:  python -I docs/academico/tools/f35sbxb_cierre_terminal/validate_f35sbxb_cierre_terminal.py   (sin -I, se relanza)

Contrato: docs/academico/evidencia-sbx-b-cierre-terminal/F35SBXB_Cierre_Terminal.md. Valida el cierre terminal de
F35-SBX-B y su registro en el gobierno con una transición única y monotónica (B3_GOVERNANCE_BLOB y el
ACADEMIC_BASELINE.md previo → TC_GOVERNANCE_BLOB). Conserva la evaluación vigente: los gates de B3, de R2-A y de B2 se
ejecutan intactos, desde los bytes verificados de sus blobs; su salida se predice con su propia lógica sobre el estado
observado, su falla de clase A se clasifica con exactitud y lo que esa falla enmascara se repone con reglas propias. El
repositorio solo se lee; los subgates escriben únicamente sus temporales fuera de él. Cada objeto Git que se lee se
verifica recalculando su identificador, y todo error, salida incompleta o estado no evaluable falla cerrado.

  ENT  intérprete aislado y sin PYTHONPATH, PYTHONHOME ni PYTHONUSERBASE; ninguna variable de Git que redirija el
       repositorio; Git sobre el repositorio de este archivo, con historia completa, sin injertos ni reemplazos y a no
       más de dos niveles de clones compartidos.
  CTX  rama chore/f35-sbx-b-terminal-closure, develop o main; el merge 53c0eb5, ancestro de HEAD.
  ANC  anclas registradas, íntegras y en cadena (de 8e94a60 a 53c0eb5 y la transición del cierre); los merges eb02c2d,
       04895aa, ca36875 y 53c0eb5 con sus padres y árboles; blobs de gobierno de las seis etapas.
  HIS  el gate de B3, con los bytes de su blob en 8d39d0e, anclado sobre 8d39d0e en un clon temporal sin remoto: código
       0, 19/0, FRZ en 8d39d0e, GOV en fa5664a, el informe del pipeline con su SHA-256 registrado y R2-A anclado en 14/0.
  B3G  el mismo gate sobre HEAD: su salida es exactamente la que su lógica da sobre el estado observado, y solo falla por
       la clase A del cierre (CTX en la rama, R2A, MAT, GOV, SEM y ALC); las seis reglas del pipeline pasan.
  R2A  el gate de R2-A sobre HEAD, con la misma exigencia: solo CTX en la rama, GCL, SUC, MAT, GOV, SEM y ALC.
  MAT  el gate de B2, con los bytes de su blob en el candidato, sobre HEAD: solo su clase A, con SCP en las 26 rutas
       posteriores al candidato, DEP limitado al pipeline, GOV exacto y SBX-01..SBX-18 en verde.
  INT  capas congeladas, de A a B3, desde sus anclas, en cada commit posterior, HEAD, índice y disco.
  FLG  ningún flag en el índice.
  GOV  transición única y monotónica en seis etapas, registrada; estado efectivo en HEAD, índice y disco.
  SEM  semántica del gobierno y del documento de la capa con las piezas verificadas del gate de B1: F35-SBX-B y B3
       cerradas, congeladas e integradas, F35-SBX habilitada y ningún otro estado cambiado.
  LOW  los riesgos residuales B3-AF-L01, B3-AF-L02 y B3-R3, registrados como LOW, aceptados y no bloqueantes.
  ALC  alcance exacto frente a 53c0eb5: las tres rutas A de la capa y las tres de gobierno M; sin archivos sin seguimiento.
  FRZ  nivel B: un único commit posterior a 53c0eb5 completa la capa y, desde él, sus archivos no cambian. Su hash se
       deriva de Git y se registra fuera, nunca en un archivo.
  DEP  biblioteca estándar autorizada por archivo; la única ejecución dinámica es la carga verificada de los gates
       congelados.
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
A_ANCHOR = '61f94e23fc30b00a848a4558830b6d65f81dff87'            # commit E de F35-SBX-A: contrato, fixtures y manifest
B1_ANCHOR = '8e94a60274fe39ebda3e9961bc58036b389dfc00'          # ancla auditada de B1
B1_CLOSURE = '3d9b78307684a0dfb093e31d28fde290b2b1cb4a'         # cierre de B1-FREEZE
B2_BASE = '72e86c5838984ea873d6dd56c179d94217b27317'            # develop al crear la rama de B2
B2_TRANSITION = '12c1c36e409f81c048fccf7fcb3e6d2a2d5d40aa'      # transición de gobierno de B2
CANDIDATE = '2472fd6fadfc0634ec68cbcb76cfc9fbfe105194'          # candidato de B2 reauditado: almacén y gate de B2
FREEZE = '9961d2d65ed51a17c14aae5db0edb7d71c622c22'             # B2-FREEZE
SUCCESSOR = '9d6fb157bb818574217e3675da1849e8d1010962'          # gate sucesor (AF-M01)
SUCCESSOR_FREEZE = '89694244b81b0bd84dbe6ae5d04b5c7a198bafef'   # B2-SUCCESSOR-FREEZE: ancla externa aprobada (AF-L02)
DEVELOP_MERGE = 'eb02c2d84335347c52b81a76c1e73dc30b93e88a'      # integración de B2 en develop
CLOSURE_TRANSITION = 'd346597e988d2f7f5d0d84e119709012b67715da'  # transición del cierre de gobierno
GOV_CLOSURE = '363273ead5794ea7a2dba74c011a0efd6d59e906'        # B2-GOVERNMENT-CLOSURE: ancla externa aprobada
DEVELOP_GOV_MERGE = '04895aacd96f0f03dde84e10a558bbdf26f050c6'  # integración del cierre de gobierno en develop
FORMAL_TRANSITION = 'ddefb7dae00a7b57eb32c1046de634c0be2805de'  # transición del cierre formal (R2-A)
R2A_COMPLETION = 'ad193f9565bf23246fadb9f85fc0ceddf8ddf698'     # R2-A: ancla aprobada del registro del cierre formal
B3_BASE = 'ca36875938eca035c97205921ec5f9633381c571'            # integración de R2-A en develop; base de B3
B3_TRANSITION = 'fa5664a0a3660519744a32b320822ecc396b1619'      # transición de gobierno de B3
B3_ANCHOR = '8d39d0e547821f7d6f63dc12b9c01803f985d797'          # B3: ancla aprobada por la auditoría independiente
BASE = '53c0eb55a8f64f5576c43c2bfb5dccf095e30412'               # integración de B3 en develop; base del cierre
# Commit de la transición de gobierno del cierre terminal. Se registra después de que exista, nunca en el propio commit.
TC_TRANSITION = '5517a12a4d35c6d8c3281ace2f072ddc692f16f2'
CHAIN = (B1_ANCHOR, B1_CLOSURE, B2_BASE, B2_TRANSITION, CANDIDATE, FREEZE, SUCCESSOR, SUCCESSOR_FREEZE, DEVELOP_MERGE,
         CLOSURE_TRANSITION, GOV_CLOSURE, DEVELOP_GOV_MERGE, FORMAL_TRANSITION, R2A_COMPLETION, B3_BASE, B3_TRANSITION,
         B3_ANCHOR, BASE, TC_TRANSITION)
MERGES = ((DEVELOP_MERGE, B2_BASE, SUCCESSOR_FREEZE), (DEVELOP_GOV_MERGE, DEVELOP_MERGE, GOV_CLOSURE),
          (B3_BASE, DEVELOP_GOV_MERGE, R2A_COMPLETION), (BASE, B3_BASE, B3_ANCHOR))
REPORT_SHA256 = '7efc00ee307c932955f2f3cc10b56dc08c14cd408c1fc7b43f612a712d174967'   # informe canónico del pipeline
REPORT_BYTES = 38372

BRANCH = 'chore/f35-sbx-b-terminal-closure'
BRANCHES = (BRANCH, 'develop', 'main')
B3_BRANCH = 'feature/f35-sbx-b3-deterministic-pipeline'
GOV_PATHS = ('CLAUDE.md', 'docs/PROGRESS.md')
BASELINE = 'docs/academico/ACADEMIC_BASELINE.md'
TC_PATHS = GOV_PATHS + (BASELINE,)
BASELINE_BLOB = 'dccdf8925f3dbba6ca14c5f4f4d74bd6276496cb'      # sin cambios desde el cierre de F35-SBX-A
GOV_BLOBS = {'b1': (B1_ANCHOR, {'CLAUDE.md': 'b7068afbfac6cc2f1f39053dff8face38b894415',
                                'docs/PROGRESS.md': '983844fd2477432b2a1ea402aa8b3130678a014a'}),
             'b2': (B2_TRANSITION, {'CLAUDE.md': '74cc4a71c56918678e0a70c7f59a3f060d87b6a0',
                                    'docs/PROGRESS.md': '07889bf8c82990651539a6e4b8a1098b4bd2d35a'}),
             'cierre': (CLOSURE_TRANSITION, {'CLAUDE.md': 'dcf584c28f8b0f044e3ab9fc11cc117fc17e8a8c',
                                             'docs/PROGRESS.md': '49390335d47a13468f0a5b4017cf6b5723ad8ecb'}),
             'formal': (FORMAL_TRANSITION, {'CLAUDE.md': '0f9d516fd129ba83058076e6bffb293e9be1fac1',
                                            'docs/PROGRESS.md': '60a891fbf7967d4bcc9342ed43b10f1b587540e7'}),
             'b3': (B3_TRANSITION, {'CLAUDE.md': '8e908661b96a557d078d0036a41e319b2a3bb76c',
                                    'docs/PROGRESS.md': '4146a9d331f2d3f6240aedd599eb0238c578f761'}),
             'tc': (TC_TRANSITION, {'CLAUDE.md': 'd4ba0968e6ebbcaca667d47954db46f7088fae9a',
                                    'docs/PROGRESS.md': 'a6322415e7705395dde1e185a3e501155f1989f5',
                                    BASELINE: 'e9fb4bbbc1534802fc196cca021eeeef69414571'})}
STAGES = ('b1', 'b2', 'cierre', 'formal', 'b3', 'tc')
B1_GATE = 'docs/academico/tools/f35sbxb/validate_f35sbxb.py'
B2_GATE = 'docs/academico/tools/f35sbxb2/validate_f35sbxb2.py'
SF_GATE = 'docs/academico/tools/f35sbxb2_sucesor_freeze/validate_f35sbxb2_sucesor_freeze.py'
R2A_GATE = 'docs/academico/tools/f35sbxb2_cierre_formal/validate_f35sbxb2_cierre_formal.py'
B3_GATE = 'docs/academico/tools/f35sbxb3/validate_f35sbxb3.py'
VERIFIED = {'b1': (B1_ANCHOR, B1_GATE), 'b2': (CANDIDATE, B2_GATE), 'sf': (SUCCESSOR_FREEZE, SF_GATE),
            'r2a': (R2A_COMPLETION, R2A_GATE), 'b3': (B3_ANCHOR, B3_GATE)}

# Capas congeladas (INT): cada una con su ancla y sus carpetas, cuyo contenido exacto se toma del árbol del ancla. El
# gobierno no está aquí: lo protege GOV.
B3_DIRS = ('docs/academico/evidencia-sbx-b3', 'docs/academico/tools/f35sbxb3')
FROZEN = (('A', A_ANCHOR, ('docs/academico/evidencia-sbx', 'docs/academico/tools/f35sbx')),
          ('B1', B1_ANCHOR, ('docs/academico/evidencia-sbx-b', 'docs/academico/tools/f35sbxb')),
          ('B1-FREEZE', B1_CLOSURE, ('docs/academico/evidencia-sbx-b-freeze', 'docs/academico/tools/f35sbxb_freeze')),
          ('B2', CANDIDATE, ('docs/academico/evidencia-sbx-b2', 'docs/academico/tools/f35sbxb2')),
          ('B2-FREEZE', FREEZE, ('docs/academico/evidencia-sbx-b2-freeze', 'docs/academico/tools/f35sbxb2_freeze')),
          ('sucesor', SUCCESSOR, ('docs/academico/evidencia-sbx-b2-sucesor', 'docs/academico/tools/f35sbxb2_sucesor')),
          ('B2-SUCCESSOR-FREEZE', SUCCESSOR_FREEZE, ('docs/academico/evidencia-sbx-b2-sucesor-freeze',
                                                     'docs/academico/tools/f35sbxb2_sucesor_freeze')),
          ('B2-GOVERNMENT-CLOSURE', GOV_CLOSURE, ('docs/academico/evidencia-sbx-b2-cierre-gobierno',
                                                  'docs/academico/tools/f35sbxb2_cierre_gobierno')),
          ('R2-A', R2A_COMPLETION, ('docs/academico/evidencia-sbx-b2-cierre-formal',
                                    'docs/academico/tools/f35sbxb2_cierre_formal')),
          ('B3', B3_ANCHOR, B3_DIRS))

# Capa del cierre terminal (nivel B), con su contenido exacto.
LAYER_DOCS = 'docs/academico/evidencia-sbx-b-cierre-terminal'
LAYER_TOOLS = 'docs/academico/tools/f35sbxb_cierre_terminal'
LAYER_DIRS = {LAYER_DOCS: ('F35SBXB_Cierre_Terminal.md',),
              LAYER_TOOLS: ('test_f35sbxb_cierre_terminal.py', 'validate_f35sbxb_cierre_terminal.py')}
LAYER_FILES = tuple(sorted(f'{folder}/{name}' for folder, names in LAYER_DIRS.items() for name in names))
DOC = LAYER_DOCS + '/F35SBXB_Cierre_Terminal.md'
VALIDATOR = LAYER_TOOLS + '/validate_f35sbxb_cierre_terminal.py'
TESTS = LAYER_TOOLS + '/test_f35sbxb_cierre_terminal.py'
SCOPE = {**{p: 'A' for p in LAYER_FILES}, **{p: 'M' for p in TC_PATHS}}
# Lo que el cierre añade a la vista de alcance de cada gate congelado: sus rutas (A) y ACADEMIC_BASELINE.md (M).
TC_DELTA = frozenset({(p, 'A') for p in LAYER_FILES} | {(BASELINE, 'M')})

# Delta de gobierno del cierre (§3.3): lista cerrada de reemplazos literales sobre el blob de B3 y sobre el de
# ACADEMIC_BASELINE.md, cada bloque antiguo presente exactamente una vez.
_B3_STATE = ('F35-SBX-B INICIADA solo como sandbox sintético: B1 (gate sucesor sobre HEAD) CERRADA, CONGELADA E '
             'INTEGRADA; B2 (almacén efímero SQLite `:memory:` por organización sintética) CERRADA, CONGELADA E '
             'INTEGRADA; B3 (pipeline determinista de doce pasos sobre el almacén de B2) IMPLEMENTADA, sin ML.')
_TC_STATE = ('F35-SBX-B CERRADA, CONGELADA E INTEGRADA solo como sandbox sintético: B1 (gate sucesor sobre HEAD) '
             'CERRADA, CONGELADA E INTEGRADA; B2 (almacén efímero SQLite `:memory:` por organización sintética) CERRADA, '
             'CONGELADA E INTEGRADA; B3 (pipeline determinista de doce pasos sobre el almacén de B2) CERRADA, CONGELADA '
             'E INTEGRADA, sin ML.')
_B3_OPEN = 'F35-SBX-B INICIADA: su incremento B1 (gate sucesor sobre HEAD) está CERRADO'
_TC_OPEN = 'F35-SBX-B CERRADA, CONGELADA E INTEGRADA: su incremento B1 (gate sucesor sobre HEAD) está CERRADO'
_B3_TAIL = ('su incremento B3 (pipeline determinista de doce pasos sobre el almacén de B2) está IMPLEMENTADO, registrado '
            'en [`evidencia-sbx-b3`]({root}evidencia-sbx-b3/F35SBXB_B3_Pipeline.md).')
_TC_B3 = ('su incremento B3 (pipeline determinista de doce pasos sobre el almacén de B2) está CERRADO, CONGELADO E '
          f'INTEGRADO en `develop` y `main` (ancla aprobada `{B3_ANCHOR}`, merges `{BASE}` y '
          '`9424f1ea2a1e25dd29e8cfc0b9f446b3118b7a9a`)')
_TC_RECORD = 'su cierre terminal está registrado en [`evidencia-sbx-b-cierre-terminal`]'
_TC_TAIL = (_TC_B3 + ', registrado en [`evidencia-sbx-b3`]({root}evidencia-sbx-b3/F35SBXB_B3_Pipeline.md); ' +
            _TC_RECORD + '({root}evidencia-sbx-b-cierre-terminal/F35SBXB_Cierre_Terminal.md).')
_B3_HEADER = ('Última actualización: 2026-10-19 (F34E CERRADA; G0 real NO APROBADA; G0-SBX APROBADA CON RESTRICCIONES; '
              'F35-SBX sintética HABILITADA; F35-SBX-A CERRADA E INTEGRADA; B0 CERRADA E INTEGRADA; F35-SBX-B '
              'INICIADA: B1 CERRADA E INTEGRADA, B2 CERRADA E INTEGRADA, B3 IMPLEMENTADA).')
_TC_HEADER = ('Última actualización: 2026-10-21 (F34E CERRADA; G0 real NO APROBADA; G0-SBX APROBADA CON RESTRICCIONES; '
              'F35-SBX sintética HABILITADA; F35-SBX-A CERRADA E INTEGRADA; B0 CERRADA E INTEGRADA; F35-SBX-B '
              'CERRADA, CONGELADA E INTEGRADA: B1, B2 y B3 CERRADAS E INTEGRADAS).')
_B3_HISTORY = 'El 19/10/2026 pasó a B3 implementada: el pipeline determinista de doce pasos sobre el almacén de B2.'
_TC_HISTORY = _B3_HISTORY + (' El 21/10/2026 pasó a F35-SBX-B cerrada, congelada e integrada, con B3 auditada e '
                             'integrada y su cierre terminal registrado.')
_AB_STATE_OLD = 'Sin runtime productivo ni capacidades de alcance C. F35-SBX-B NO INICIADA. RF-23 sigue humana;'
_AB_STATE = ('Sin runtime productivo ni capacidades de alcance C. F35-SBX-B CERRADA, CONGELADA E INTEGRADA solo como '
             'sandbox sintético: B0, B1, B2 y B3 cerradas e integradas, sin ML. RF-23 sigue humana;')
_AB_TAIL_OLD = ('F35-SBX-A queda cerrada documentalmente en `feature/f35-sbx-synthetic-evidence-pipeline`, con publicación '
                'pendiente de regresión post-commits y CI. F35-SBX-B NO INICIADA; requiere autorización nueva.')
_AB_TAIL = (f'F35-SBX-A está CERRADA E INTEGRADA en `develop` y `main`, con su commit E `{A_ANCHOR}`. F35-SBX-B está '
            'CERRADA, CONGELADA E INTEGRADA, con su cierre terminal registrado en [`evidencia-sbx-b-cierre-terminal`]'
            '(evidencia-sbx-b-cierre-terminal/F35SBXB_Cierre_Terminal.md). F36–F40 siguen BLOQUEADAS.')
TC_DELTA_TEXT = {'CLAUDE.md': [(_B3_STATE, _TC_STATE), (_B3_OPEN, _TC_OPEN),
                               (_B3_TAIL.format(root='docs/academico/'), _TC_TAIL.format(root='docs/academico/'))],
                 'docs/PROGRESS.md': [(_B3_HEADER, _TC_HEADER), (_B3_HISTORY, _TC_HISTORY), (_B3_STATE, _TC_STATE),
                                      (_B3_OPEN, _TC_OPEN),
                                      (_B3_TAIL.format(root='academico/'), _TC_TAIL.format(root='academico/'))],
                 BASELINE: [(_AB_STATE_OLD, _AB_STATE), (_AB_TAIL_OLD, _AB_TAIL)]}

# SEM (§3.7): declaración canónica del cierre en lo vigente, frases anteriores que ya no pueden figurar, vocabulario.
RF_STATE = 'RF-23 sigue humana; RF-29 sigue experimental/informativa.'
TC_REQUIRED = {'CLAUDE.md': (_TC_STATE, _TC_OPEN, _TC_B3, _TC_RECORD, RF_STATE),
               'docs/PROGRESS.md': (_TC_STATE, _TC_OPEN, _TC_B3, _TC_RECORD, RF_STATE),
               BASELINE: (_AB_STATE, _AB_TAIL, RF_STATE)}
TC_HEADER = 'F35-SBX-B CERRADA, CONGELADA E INTEGRADA: B1, B2 y B3 CERRADAS E INTEGRADAS).'
TC_STALE = ('F35-SBX-B INICIADA', 'F35-SBX-B NO INICIADA', 'IMPLEMENTADA, sin ML', 'está IMPLEMENTADO', 'B3 IMPLEMENTADA',
            'sin pipeline funcional', 'PENDIENTE DE CIERRE FORMAL', 'queda cerrada documentalmente')
TC_FORBIDDEN_RX = re.compile(r'(?<![\w-])(?:f35-sbx-b|b1|b2|b3)(?![\w-])((?:\s+[a-z0-9-]+){0,3}?)\s*(?:=|:|\s)\s*'
                             r'(productiv\w*|aprobad\w*|publicad\w*|desplegad\w*)\b')
TC_REOPEN_RX = re.compile(r'(?<![\w-])(?:f35-sbx-b|b1|b2|b3)(?![\w-])((?:\s+[a-z0-9-]+){0,3}?)\s*(?:=|:|\s)\s*'
                          r'(reabiert\w*|reabr\w*|reapert\w*|pendiente\w*|abiert\w*|desarroll\w*|candidat\w*|'
                          r'no\s+cerrad\w*|iniciad\w*)\b')
FENCE_RX = re.compile(r'^```.*?^```[ \t]*$', re.M | re.S)
LIMITS = ('- no aprueba la G0 real ni sustituye su evidencia externa;',
          '- no habilita la F35 productiva ni ninguna integración productiva;',
          '- no habilita F36 ni ninguna fase posterior;',
          '- no permite datos reales;',
          '- no permite puntuar ni clasificar ni recomendar candidatos;',
          '- no permite la selección automática;',
          '- no habilita el alcance C;',
          '- no habilita OCR ni parsing ni embeddings ni búsqueda semántica;',
          '- no cambia RF-23, que sigue siendo la decisión final humana del Aprobador/Dirección;',
          '- no cambia RF-29, que sigue experimental e informativo;',
          '- mantiene F35-SBX HABILITADA, sin cerrarla.')
# LOW (§3.8): las tres filas de la tabla de riesgos residuales.
LOW_RISKS = (('B3-AF-L01', 'Comprobante de purga no completamente independiente del pipeline'),
             ('B3-AF-L02', 'La comprobación CNF no demuestra por sí sola la unicidad global de `audit_id`'),
             ('B3-R3', 'Los diagnósticos de los gates históricos profundamente anidados pueden quedar truncados'))
LOW_STATE = 'Aceptado, no bloqueante'
LOW_ALTERED_RX = re.compile(r'(resuelt|corregid|descartad|\bMEDIUM\b|\bHIGH\b|\bBLOCKER\b)', re.IGNORECASE)
PIPELINE = 'docs/academico/tools/f35sbxb3/sbxb_pipeline.py'
B2_DEP_ITEM = f'{PIPELINE}: código fuera de B2 que usa el almacén o sus nombres internos'

# Clase A del cierre en las salidas de los gates congelados (§3.5).
F35B_CLOSED = frozenset({'«f35-sbx-b cerrada»'})
B3_CLOSED_RX = re.compile(r'«b3(?: \([^()«»]*\))?(?: [a-z0-9-]+){0,3}? (?:cerrad|congelad|integrad)\w*»')
B3G_ALLOWED = frozenset({'CTX', 'R2A', 'MAT', 'GOV', 'SEM', 'ALC'})
R2A_ALLOWED = frozenset({'CTX', 'GCL', 'SUC', 'MAT', 'GOV', 'SEM', 'ALC'})
B2_ALLOWED_RULES = frozenset({'CTX', 'B1F', 'SCP', 'DEP', 'DYN', 'GOV'})

DEP_ALLOWED = {VALIDATOR: frozenset({'ast', 'hashlib', 'os', 're', 'subprocess', 'sys', 'types'}),
               TESTS: frozenset({'os', 'subprocess', 'sys'})}
LOADERS = {VALIDATOR: 'load_verified'}      # única función con ejecución dinámica: los gates congelados verificados
DYNAMIC_CODE = frozenset({'__import__', 'compile', 'eval', 'exec'})
ORDER = ('ENT', 'CTX', 'ANC', 'HIS', 'B3G', 'R2A', 'MAT', 'INT', 'FLG', 'GOV', 'SEM', 'LOW', 'ALC', 'FRZ', 'DEP')
PLANES = ('HEAD', 'árbol', 'índice')
TIMEOUT = 3600
# Niveles de clones compartidos admitidos bajo este repositorio: HIS ejecuta el gate de B3 en un clon que suma uno a la
# cadena que ese gate admite (tres), y el gate de R2-A sobre HEAD anida tres más.
MAX_ALTERNATES = 2
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
B2_INFO = {'TRN': re.compile(r'INFO transición de gobierno de B2 derivada: ([0-9a-f]{40}); registrada: ([0-9a-f]{40})')}
B3_SUMMARY = re.compile(r'validate_f35sbxb3: (\d+) comprobaciones correctas, (\d+) fallas')
B3_INFO = {
    'ANC': re.compile(r'INFO ANC: anclas registradas ((?:[0-9a-f]{12}, )*[0-9a-f]{12}); base ([0-9a-f]{40}); HEAD '
                      r'([0-9a-f]{40})'),
    'MAT': re.compile(r'INFO MAT: gate de B2 sobre HEAD: código (\d+); (\d+) correctas, (\d+) fallas; reglas en falla: '
                      r'([^;]*); casos en falla: ([^;]*); SCP: (\d+) violaciones \(previstas (\d+)\)'),
    'PIP': re.compile(r'INFO PIP: informe de (\d+) bytes, SHA-256 ([0-9a-f]{64}); resultado (\S+)'),
    'R2A': re.compile(r'INFO R2A: gate de R2-A sobre HEAD: código (\d+); (\d+) correctas, (\d+) fallas; reglas en falla: '
                      r'([^;]*); previstas: ([^;]*)'),
    'HIS': re.compile(r'INFO HIS: R2-A anclado sobre ([0-9a-f]{40}): código (\d+); (\d+) correctas, (\d+) fallas; ancla '
                      r'derivada ([0-9a-f]{40}|ninguno); transición derivada ([0-9a-f]{40}|ninguna)'),
    'GOV': re.compile(r'INFO GOV: transición de B3 derivada: ([0-9a-f]{40}|ninguna); registrada: ([0-9a-f]{40})'),
    'FRZ': re.compile(r'INFO FRZ: commit que completa la capa: ([0-9a-f]{40}|ninguno)')}
B3_TOTAL = 19
B3_PIPE_RULES = ('PIP', 'DET', 'CNF', 'PUR', 'TSB', 'FAL')
R2A_TOTAL = 14
B2_TOTAL = 119
SF_TOTAL = 12
GC_TOTAL = 13
SCP_ITEM = re.compile(r'(HEAD|árbol|índice): cambio fuera del delta autorizado de B2 o con estado inesperado: ([AM]) (.+)')


class GitError(Exception):
    pass


ERRORS = (GitError, OSError, ValueError, KeyError, TypeError, IndexError, AttributeError, SyntaxError,
          UnicodeDecodeError, subprocess.TimeoutExpired)


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


# ---------------------------------------------------------------- subgates congelados, con bytes verificados
def verified_script(rel, expected, root=None):
    data = disk_bytes(rel, root)
    if data is None or blob_id(data) != expected:
        raise ValueError(f'{rel} distinto de su blob {expected[:12]}: no se ejecuta')
    return disk_path(rel, root)


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
    path = os.path.join(base, f'f35sbxbtc-{label}-{os.getpid()}-{_COUNTER[0]}')
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


def object_stores(first):
    """Almacenes de objetos que lee un clon compartido: first y, en anchura, los de su cadena de alternates."""
    out, queue = [], [first]
    while queue:
        store = os.path.normpath(queue.pop(0))
        if any(os.path.normcase(store) == os.path.normcase(seen) for seen in out):
            continue
        out.append(store)
        alternates = os.path.join(store, 'info', 'alternates')
        if os.path.isfile(alternates):
            with open(alternates, encoding='utf-8') as f:
                for line in f.read().splitlines():
                    line = line.strip()
                    if line and not line.startswith('#'):
                        queue.append(line if os.path.isabs(line) else os.path.join(store, line))
    return out


def flatten_alternates(repo):
    """Alternates aplanados de un clon temporal compartido: cada almacén de la cadena de este repositorio, listado
    directamente y del más lejano al más cercano, para que el clon no añada un nivel a lo que se ejecuta dentro."""
    path = os.path.join(repo, '.git', 'objects', 'info', 'alternates')
    with open(path, encoding='utf-8') as f:
        first = [x.strip() for x in f.read().splitlines() if x.strip() and not x.strip().startswith('#')]
    if len(first) != 1:
        raise GitError('el clon temporal no tiene un único almacén compartido')
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(''.join(store.replace(os.sep, '/') + '\n' for store in reversed(object_stores(first[0]))))


class Background:
    """Un subgate congelado en segundo plano, con bytes verificados antes y después y su salida en un temporal propio.
    Con clone=(commit, rama), en un clon temporal sin remoto, con alternates aplanados, en ese commit; si no, sobre
    este repositorio."""

    def __init__(self, label, rel, blob, clone=None):
        self.tmp, self.proc, self.files, self.rel, self.blob, self.cwd = make_temp(label), None, [], rel, blob, ROOT
        try:
            if clone is not None:
                commit, branch = clone
                config = os.path.join(self.tmp, 'gitconfig')
                with open(config, 'wb'):
                    pass
                env = dict(GIT_ENV, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=config)
                self.cwd = os.path.join(self.tmp, 'repo')
                git('clone', '-q', '--shared', '--no-checkout', '-c', 'core.autocrlf=false', ROOT, self.cwd,
                    cwd=self.tmp, env=env)
                flatten_alternates(self.cwd)
                git('remote', 'remove', 'origin', cwd=self.cwd, env=env)
                git('checkout', '-q', '-B', branch, commit, cwd=self.cwd, env=env)
                if git('rev-parse', '--verify', 'HEAD^{commit}', cwd=self.cwd).decode('ascii').strip() != commit:
                    raise GitError(f'el clon temporal no está en {commit[:12]}')
            path = verified_script(rel, blob, self.cwd)
            self.files = [open(os.path.join(self.tmp, name), 'wb') for name in ('salida', 'errores')]
            self.proc = subprocess.Popen([sys.executable, '-I', '-B', path], cwd=self.cwd, env=GIT_ENV,
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
        verified_script(self.rel, self.blob, self.cwd)
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


def gate_blob(objs, name):
    commit, rel = VERIFIED[name]
    found = entry(objs, commit_parts(objs, commit)[0], rel)
    if found is None or found[:2] != ('100644', 'blob'):
        raise GitError(f'{rel} no es un blob regular en su ancla {commit[:12]}')
    return found[2]


def load_verified(objs, name):
    """Un gate congelado desde los bytes de su blob en su ancla, verificado al leerlo; nunca desde el disco. Es la
    única ejecución dinámica de este gate: el de B1 (piezas de SEM) y los de B2, B2-SUCCESSOR-FREEZE, R2-A y B3 (su
    lógica, para predecir su salida sobre HEAD)."""
    commit, rel = VERIFIED[name]
    data = blob_at(objs, commit, rel)
    path = os.path.join(ROOT, *rel.split('/'))
    module = types.ModuleType(f'f35sbxb_gate_{name}_verificado_tc')
    module.__file__ = path
    exec(compile(data, path, 'exec', dont_inherit=True), module.__dict__)
    return module


# ---------------------------------------------------------------- ENT, CTX y ANC
def alternates_depth(store, seen=()):
    """Máximo de niveles de alternates encadenados que Git sigue desde un almacén de objetos."""
    key = os.path.normcase(os.path.normpath(store))
    path = os.path.join(store, 'info', 'alternates')
    if key in seen or not os.path.isfile(path):
        return 0
    with open(path, encoding='utf-8') as f:
        entries = [x.strip() for x in f.read().splitlines() if x.strip() and not x.strip().startswith('#')]
    return max((1 + alternates_depth(e if os.path.isabs(e) else os.path.join(store, e), seen + (key,))
                for e in entries), default=0)


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
    common = git('rev-parse', '--path-format=absolute', '--git-common-dir').decode('utf-8').strip()
    depth = alternates_depth(os.path.join(common, 'objects'))
    if depth > MAX_ALTERNATES:
        out.append(f'repositorio a {depth} niveles de clones compartidos: los gates anclados anidados superarían el '
                   f'límite de alternates de Git (se admiten {MAX_ALTERNATES})')
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


def tc_entries(objs, commit):
    root = commit_parts(objs, commit)[0]
    return {p: entry(objs, root, p) for p in TC_PATHS}


def anc_problems(objs):
    out = []
    for commit in CHAIN:
        commit_parts(objs, commit)
    for older, newer in zip(CHAIN, CHAIN[1:]):
        if older not in ancestry(objs, newer):
            out.append(f'{newer[:12]} no desciende de {older[:12]}: la cadena de anclas no corresponde')
    if A_ANCHOR not in ancestry(objs, B1_ANCHOR):
        out.append(f'{B1_ANCHOR[:12]} no desciende del commit E de F35-SBX-A {A_ANCHOR[:12]}')
    for merge, first, second in MERGES:
        tree, parents = commit_parts(objs, merge)
        if parents != [first, second]:
            out.append(f'el merge {merge[:12]} no tiene como padres {first[:12]} y {second[:12]}')
        if tree != commit_parts(objs, second)[0]:
            out.append(f'el merge {merge[:12]} no tiene el árbol del ancla aprobada {second[:12]}')
    for stage in STAGES:
        commit, blobs = GOV_BLOBS[stage]
        want = {p: ('100644', 'blob', blobs.get(p, BASELINE_BLOB)) for p in TC_PATHS}
        if tc_entries(objs, commit) != want:
            out.append(f'blobs de gobierno de {commit[:12]} distintos de los registrados')
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
    for label, (anchor, want) in frozen_layers(objs).items():
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
            out += [f'capa {label}: {x}' for x in disk_folder(folder, found)]
    return out


def flg_problems():
    flagged = [item.decode('utf-8', 'replace') for item in git('ls-files', '-v', '-z').split(b'\x00')
               if item and not item.startswith(b'H ')]
    return [f'flags en el índice (assume-unchanged, skip-worktree o conflictos): {flagged[:5]}'] if flagged else []


# ---------------------------------------------------------------- GOV: seis etapas, transición única y monotónica
def governance(objs):
    """Entradas de cada etapa en las tres rutas: las cinco registradas en sus commits, con ACADEMIC_BASELINE.md sin
    cambios, y 'tc', con el delta aplicado al blob de B3 y al ACADEMIC_BASELINE.md previo; el resultado debe ser el blob
    registrado del cierre."""
    want = {stage: tc_entries(objs, GOV_BLOBS[stage][0]) for stage in STAGES[:5]}
    if any(want[stage][BASELINE] != ('100644', 'blob', BASELINE_BLOB) for stage in STAGES[:5]):
        raise ValueError('ACADEMIC_BASELINE.md distinto de su blob previo en alguna etapa anterior al cierre')
    tc = {}
    for path in TC_PATHS:
        text = blob_text(objs, want['b3'][path]).decode('utf-8')
        blocks = TC_DELTA_TEXT.get(path) or []
        if not blocks or any(text.count(before) != 1 for before, _ in blocks):
            raise ValueError(f'{path}: delta del cierre vacío o con un bloque antiguo que no aparece exactamente una vez')
        for before, after in blocks:
            text = text.replace(before, after, 1)
        tc[path] = ('100644', 'blob', blob_id(text.encode('utf-8')))
    if tc != {p: ('100644', 'blob', b) for p, b in GOV_BLOBS['tc'][1].items()}:
        raise ValueError('el delta del cierre aplicado al blob de B3 no da el blob registrado del cierre')
    want['tc'] = tc
    return want


def introduced(objs, parents, order, want, stage):
    """{commit: rutas} de los commits que contienen el blob de una etapa sin que ninguno de sus padres lo contenga."""
    found = {}
    for commit in order:
        here = tc_entries(objs, commit)
        for p in TC_PATHS:
            if here[p] == want[stage][p] and not any(tc_entries(objs, q)[p] == want[stage][p] for q in parents[commit]):
                found.setdefault(commit, set()).add(p)
    return found


def effective_problems(objs, head, final, texts):
    root = commit_parts(objs, head)[0]
    index = index_entries(TC_PATHS)
    out = []
    for p in TC_PATHS:
        if entry(objs, root, p) != final[p]:
            out.append(f'{p}: {texts[0]}')
        if index.get(p) != [(final[p][0], final[p][2], '0')]:
            out.append(f'{p}: {texts[1]}')
        data = disk_bytes(p)
        if data is None or blob_id(data) != final[p][2]:
            out.append(f'{p}: {texts[2]}')
    return out


def gov_problems(objs, parents, head, notes):
    want = governance(objs)
    graph = descendants(parents, B1_ANCHOR)
    order = [c for c in topological(parents) if c in graph]          # de los más antiguos a los más recientes
    out = []
    for stage, label in (('b2', 'de B2'), ('cierre', 'del cierre de gobierno'), ('formal', 'del cierre formal'),
                         ('b3', 'de B3')):
        commit = GOV_BLOBS[stage][0]
        found = introduced(objs, parents, order, want, stage)
        if commit in parents and found != {commit: set(GOV_PATHS)}:
            out.append(f'regla 4: el blob {label} se introduce fuera de {commit[:12]}: '
                       f'{sorted(c[:12] for c in found if c != commit)[:3]}')
    tc = introduced(objs, parents, order, want, 'tc')
    full = [c for c, paths in tc.items() if paths == set(TC_PATHS)]
    transition = full[0] if len(full) == 1 else None
    notes['transition'] = transition
    others = sorted(c[:12] for c in tc if c != transition)
    if others:
        out.append(f'regla 4: introducción del blob del cierre fuera de una transición única en las tres rutas: '
                   f'{others[:3]}')
    if transition is None:
        out.append('transición del cierre no materializada en un único commit que cambie las tres rutas a la vez')
    else:
        ps = parents[transition]
        if len(ps) != 1:
            out.append(f'regla 2: la transición del cierre {transition[:12]} no tiene un solo padre')
        else:
            if tc_entries(objs, ps[0]) != want['b3']:
                out.append(f'regla 2: el padre de la transición {transition[:12]} no tiene el blob de B3')
            changed = set(name_status(git('diff-tree', '-r', '--no-renames', '--name-status', '-z', ps[0], transition)))
            if changed != set(TC_PATHS):
                out.append(f'regla 2: la transición {transition[:12]} cambia otras rutas además del gobierno: '
                           f'{sorted(changed ^ set(TC_PATHS))[:3]}')
        if BASE not in ancestry(objs, transition):
            out.append(f'la transición {transition[:12]} no desciende del merge de integración {BASE[:12]}')
    if transition != TC_TRANSITION:
        out.append(f'transición derivada ({transition[:12] if transition else "ninguna"}) distinta de la registrada '
                   f'({TC_TRANSITION[:12]})')
    after = {stage: (descendants(parents, GOV_BLOBS[stage][0]) | {GOV_BLOBS[stage][0]})
             if GOV_BLOBS[stage][0] in parents else set() for stage in ('b2', 'cierre', 'formal', 'b3')}
    after['tc'] = (descendants(parents, transition) | {transition}) if transition else set()
    rules = {'tc': 'regla 3: descendiente de la transición del cierre sin su blob',
             'b3': 'regla 3: descendiente de la transición de B3 sin su blob',
             'formal': 'regla 3: descendiente de la transición del cierre formal sin su blob',
             'cierre': 'regla 3: descendiente de la transición del cierre de gobierno sin su blob',
             'b2': 'regla 3: descendiente de la transición de B2 sin su blob',
             'b1': 'regla 1: commit previo a la transición de B2 sin el blob de B1'}
    bad = []
    for commit in order:
        stage = next((s for s in ('tc', 'b3', 'formal', 'cierre', 'b2') if commit in after[s]), 'b1')
        diff = [p for p, e in tc_entries(objs, commit).items() if e != want[stage][p]]
        if diff:
            bad.append(f'{commit[:12]}: {rules[stage]}: {diff}')
    out += bad[:3] + ([f'… y {len(bad) - 3} commits más con un blob de gobierno no admitido'] if len(bad) > 3 else [])
    out += effective_problems(objs, head, want['tc'], ('árbol de HEAD distinto del blob del cierre',
                                                       'índice distinto del blob del cierre o en conflicto',
                                                       'disco distinto del blob del cierre, enlace o ausente'))
    return out


# ---------------------------------------------------------------- SEM y LOW: semántica con piezas verificadas de B1
def tc_semantics(b1):
    """Declaraciones de estado de B1 con el vocabulario del cierre: F35-SBX-B cerrada y congelada; B1, B2 y B3
    cerradas, congeladas o implementadas; el resto de entidades conserva sus valores. El gate de B1 no se modifica."""
    declared = [(s, a) for s, a in b1.DECLARED if s not in ('b1', 'f35-sbx-b')] + [
        ('f35-sbx-b', ('cerrad', 'congelad')),
        ('b1', ('cerrad', 'congelad', 'implementad') + b1.LOCKED),
        ('b2', ('implementad', 'congelad', 'cerrad', 'no aprobad') + b1.LOCKED),
        ('b3', ('implementad', 'congelad', 'cerrad') + b1.LOCKED)]
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
    """Reapertura de F35-SBX-B, B1, B2 o B3, o un estado distinto del cierre (pendiente, abierta, en desarrollo,
    candidata, no cerrada o iniciada)."""
    out = []
    for body in b1.sentences(text, cite=True):
        for m in TC_REOPEN_RX.finditer(body):
            if any(t in b1.NEG_WORDS or t.startswith(b1.NEG_PREFIXES) for t in m.group(1).split()):
                continue
            if b1.DECL_NEG_RX.search(re.split(r'[.,;:!?|]', body[:m.start()])[-1]):
                continue
            out.append(f'«{m.group(0).strip()}»')
    return out


def doc_problems(objs, root, b1, sem, r2a):
    """Los archivos de la capa: UTF-8 sin BOM, CR ni NUL; en el documento, sin datos personales, afirmaciones
    positivas ni declaraciones contradictorias (fuera de los bloques de código del delta), con los once límites."""
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
        if path != DOC:
            continue
        hits = [m.group(0) for rx in b1.PII for m in [rx.search(text)] if m]
        if hits:
            out.append(f'{path}: posible dato personal: {hits[:2]}')
        claims = b1.positive_claims(text)
        if claims:
            out.append(f'{path}: afirmación positiva que habilita una capacidad prohibida: {claims[:2]}')
        bad = r2a.contradictions(b1, sem, FENCE_RX.sub('', text), TC_FORBIDDEN_RX)
        if bad:
            out.append(f'{path}: declaraciones de estado contradictorias con el gobierno vigente: {bad[:3]}')
        lines = set(text.splitlines())
        missing = [x for x in LIMITS if x not in lines]
        if missing:
            out.append(f'{path}: faltan límites del cierre (§2.3): {missing[:3]}')
    return out


def sem_problems(objs, head, b1, r2a):
    sem = tc_semantics(b1)
    root = commit_parts(objs, head)[0]
    old_root = commit_parts(objs, B3_ANCHOR)[0]                # blob de B3 y ACADEMIC_BASELINE.md previo
    out = []
    for path in TC_PATHS:
        text = blob_text(objs, entry(objs, root, path)).decode('utf-8')
        old = blob_text(objs, entry(objs, old_root, path)).decode('utf-8')
        sections, header = r2a.gov_sections(text)
        if len(sections) != 1:
            out.append(f'{path}: se exige una única sección «Estado vigente F34E»')
            continue
        section = sections[0]
        if [ln for ln in section.splitlines() if re.match(r'^- [^=\n]+ = ', ln)] != b1.STATES:
            out.append(f'{path}: los trece estados de gobierno no son exactamente los vigentes')
        b_states = {' '.join(m.split()) for m in b1.B_STATE_RX.findall(section + '\n' + header)}
        if b_states != {'CERRADA'}:
            out.append(f'{path}: F35-SBX-B debe figurar solo CERRADA en el estado vigente: {sorted(b_states)}')
        missing = [x for x in TC_REQUIRED[path] if x not in section]
        if missing:
            out.append(f'{path}: el estado vigente no contiene la declaración canónica del cierre: '
                       f'{[x[:60] for x in missing[:2]]}')
        if path == 'docs/PROGRESS.md' and TC_HEADER not in header:
            out.append(f'{path}: la cabecera no declara a F35-SBX-B CERRADA, CONGELADA E INTEGRADA')
        stale = [x for x in TC_STALE if x in section or x in header]
        if stale:
            out.append(f'{path}: el estado vigente conserva frases anteriores al cierre: {stale[:3]}')
        reopen = reopening(b1, section + '\n' + header)
        if reopen:
            out.append(f'{path}: reapertura o estado distinto del cierre: {reopen[:3]}')
        before = set(old.splitlines())
        added = '\n'.join(ln for ln in text.splitlines() if ln not in before)
        bad = r2a.contradictions(b1, sem, section + '\n' + header + '\n' + added, TC_FORBIDDEN_RX)
        if bad:
            out.append(f'{path}: declaraciones de estado contradictorias con el gobierno vigente: {bad[:3]}')
        claims = b1.positive_claims(added)
        if claims:
            out.append(f'{path}: líneas nuevas que afirman habilitar una capacidad prohibida: {claims[:2]}')
    out += doc_problems(objs, root, b1, sem, r2a)
    return out


def low_problems(objs, head):
    found = entry(objs, commit_parts(objs, head)[0], DOC)
    if found is None:
        return [f'{DOC}: ausente en HEAD']
    text = blob_text(objs, found).decode('utf-8')
    out = []
    for rid, fragment in LOW_RISKS:
        rows = [ln for ln in text.splitlines() if ln.startswith(f'| {rid} |')]
        if len(rows) != 1:
            out.append(f'{rid}: se exige exactamente una fila en los riesgos residuales; hay {len(rows)}')
            continue
        cells = [c.strip() for c in rows[0].strip().strip('|').split('|')]
        if len(cells) != 5 or cells[1] != 'LOW' or cells[4] != LOW_STATE or fragment not in cells[2]:
            out.append(f'{rid}: la fila no lo registra como LOW, «{LOW_STATE}», con su descripción')
        altered = [ln[:80] for ln in text.splitlines() if ln.startswith('|') and rid in ln and
                   not ln.startswith(f'| {rid} |') and LOW_ALTERED_RX.search(ln)]
        if altered:
            out.append(f'{rid}: figura con otra severidad o como resuelto: {altered[:2]}')
    return out


# ---------------------------------------------------------------- HIS: el gate de B3 anclado sobre su ancla
def his_problems(code, stdout, stderr):
    ok, ko, rules, cases, info = parse_output(code, stdout, stderr, B3_SUMMARY, B3_INFO)
    out = []
    if code != 0 or ko or rules or cases or ok != B3_TOTAL:
        first = next((items[0] for _, (_, items) in sorted(rules.items()) if items), '')
        out.append(f'el gate de B3 anclado sobre {B3_ANCHOR[:12]} no da {B3_TOTAL}/0: {sorted(rules)}'
                   + (f'; {first[:160]}' if first else ''))
    if info['FRZ'].group(1) != B3_ANCHOR:
        out.append(f'ancla derivada {info["FRZ"].group(1)[:12]} distinta de la aprobada {B3_ANCHOR[:12]}')
    if info['GOV'].groups() != (B3_TRANSITION, B3_TRANSITION):
        out.append(f'transición de B3 derivada o registrada distinta de {B3_TRANSITION[:12]}')
    if info['ANC'].group(2) != B3_BASE or info['ANC'].group(3) != B3_ANCHOR:
        out.append('el gate de B3 anclado no informa su base y su ancla como HEAD')
    if info['PIP'].groups() != (str(REPORT_BYTES), REPORT_SHA256, 'completado'):
        out.append('el informe del pipeline anclado no es el registrado (bytes, SHA-256 o resultado)')
    if info['HIS'].groups() != (R2A_COMPLETION, '0', str(R2A_TOTAL), '0', R2A_COMPLETION, FORMAL_TRANSITION):
        out.append('el gate de B3 anclado no acredita R2-A anclado en 14/0 con su ancla y su transición')
    if info['R2A'].group(4) != info['R2A'].group(5):
        out.append('el gate de B3 anclado no acredita que R2-A falle solo en lo previsto')
    if info['MAT'].group(6) != info['MAT'].group(7):
        out.append('el gate de B3 anclado no acredita SCP del gate de B2 en lo previsto')
    line = (f'INFO HIS: B3 anclado sobre {B3_ANCHOR}: código {code}; {ok} correctas, {ko} fallas; ancla derivada '
            f'{info["FRZ"].group(1)}; transición derivada {info["GOV"].group(1)}; informe {info["PIP"].group(2)}')
    return out, line


# ---------------------------------------------------------------- MAT: el gate de B2 sobre HEAD, con su clase A
def later_files(objs):
    """Archivos de la capa de B3 en su ancla aprobada."""
    root = commit_parts(objs, B3_ANCHOR)[0]
    return tuple(sorted(f'{folder}/{rel}' for folder in B3_DIRS for rel in listing(objs, root, folder)))


def b2_scp_count(r2a, objs):
    """Rutas posteriores al candidato en la vista de alcance del gate de B2, en tres planos: las once del freeze, el
    sucesor y su cierre, las del cierre de gobierno, de R2-A, de B3 y de esta capa, y ACADEMIC_BASELINE.md."""
    return 3 * (11 + len(r2a.GC_LAYER_FILES) + len(r2a.LAYER_FILES) + len(later_files(objs)) + len(LAYER_FILES) + 1)


def b2_gov_items(objs, b1, b2, r2a):
    """GOV del gate de B2 sobre este HEAD, con su propia lógica (r2_gov): contenido, F35-SBX-B, declaraciones y
    afirmaciones, ruta por ruta."""
    old_root = commit_parts(objs, B1_ANCHOR)[0]
    sem = b2.semantics(b1)
    out = []
    for path in GOV_PATHS:
        data = disk_bytes(path)
        old = blob_text(objs, entry(objs, old_root, path))
        new = blob_text(objs, ('100644', 'blob', r2a.B2_GOV_BLOBS[path]))
        if data is None:
            out.append(f'{path}: ilegible o sin blob nuevo calculable (falla cerrado)')
            continue
        if data not in (old, new):
            out.append(f'{path}: contenido distinto del blob histórico de B1 y del blob nuevo de B2')
        text = data.decode('utf-8', 'replace')
        sections = re.findall(r'^## Estado vigente F34E\s*\n(.*?)(?=^## |\Z)', text, re.M | re.S)
        if len(sections) != 1:
            out.append(f'{path}: se exige una única sección «Estado vigente F34E»')
            continue
        section = sections[0]
        if [ln for ln in section.splitlines() if re.match(r'^- [^=\n]+ = ', ln)] != b1.STATES:
            out.append(f'{path}: los trece estados de gobierno no son exactamente los vigentes')
        header = '\n'.join(ln for ln in text.splitlines() if ln.startswith('Última actualización:'))
        b_states = {' '.join(m.split()) for m in b1.B_STATE_RX.findall(section + '\n' + header)}
        if b_states != {'INICIADA'}:
            out.append(f'{path}: F35-SBX-B debe figurar solo INICIADA en el estado vigente: {sorted(b_states)}')
        before = set(old.decode('utf-8', 'replace').splitlines())
        added = '\n'.join(ln for ln in text.splitlines() if ln not in before)
        bad = b2.contradictions2(b1, sem, section + '\n' + header + '\n' + added)
        if bad:
            out.append(f'{path}: declaraciones de estado contradictorias con el gobierno vigente: {bad[:3]}')
        claims = b1.positive_claims(added)
        if claims:
            out.append(f'{path}: líneas nuevas que afirman habilitar una capacidad prohibida: {claims[:2]}')
    return out


def tokens_closed(item, prefix, allowed):
    """Una violación «<prefijo>[ítems]» cuyos ítems son todos de los admitidos."""
    if not item.startswith(prefix):
        return False
    try:
        listed = ast.literal_eval(item[len(prefix):])
    except (ValueError, SyntaxError):
        return False
    return isinstance(listed, list) and bool(listed) and all(isinstance(x, str) and allowed(x) for x in listed)


def b2_gov_class(item, lifecycle):
    """Clase A del cierre en el GOV del gate de B2: contenido distinto, F35-SBX-B cerrada y las declaraciones del ciclo
    de vida de B2 ya registradas."""
    for p in GOV_PATHS:
        if item in (f'{p}: contenido distinto del blob histórico de B1 y del blob nuevo de B2',
                    f"{p}: F35-SBX-B debe figurar solo INICIADA en el estado vigente: ['CERRADA']"):
            return True
        if tokens_closed(item, f'{p}: declaraciones de estado contradictorias con el gobierno vigente: ',
                         lambda x: x in F35B_CLOSED or x in lifecycle):
            return True
    return False


def mat_problems(objs, parents, head, branch, observed, b1, b2, r2a):
    """El gate de B2 sobre HEAD frente a su predicción: recuentos y validadores de R2-A con las 26 rutas en SCP, DEP
    limitado al pipeline y GOV exacto con la lógica de B2; solo la clase A del cierre."""
    code, out_bytes, err_bytes = observed
    ok, ko, rules, cases, info = parse_output(code, out_bytes, err_bytes, B2_SUMMARY, B2_INFO)
    mat_obs = (code, ok, ko, rules, cases, info)
    b3_files = later_files(objs)
    expected, exp_cases, content = r2a.predicted_b2(objs, parents, head, branch,
                                                    r2a.GC_LAYER_FILES + r2a.LAYER_FILES + b3_files + LAYER_FILES,
                                                    r2a.B2_LIFECYCLE_ITEMS, BRANCH)
    post = set(name_status(git('diff-tree', '-r', '--no-renames', '--name-status', '-z', CANDIDATE,
                               SUCCESSOR_FREEZE)))
    allowed_a = post | set(r2a.GC_LAYER_FILES) | set(r2a.LAYER_FILES) | set(b3_files) | set(LAYER_FILES)
    scp_n = b2_scp_count(r2a, objs)
    if len(allowed_a) + 1 != scp_n // 3:
        raise ValueError('las rutas posteriores al candidato no son las previstas')
    expected['SCP'] = (scp_n, lambda x: bool((m := SCP_ITEM.fullmatch(x)) and (
        (m.group(2) == 'A' and m.group(3) in allowed_a) or (m.group(2) == 'M' and m.group(3) == BASELINE))))
    expected['DEP'] = (1, lambda x: x == B2_DEP_ITEM)
    gov = b2_gov_items(objs, b1, b2, r2a)
    out = []
    if info['TRN'].groups() != (B2_TRANSITION, B2_TRANSITION):
        out.append(f'transición de B2 derivada o registrada distinta de {B2_TRANSITION[:12]}')
    if ok + ko != B2_TOTAL:
        out.append(f'el gate de B2 informa {ok + ko} comprobaciones, no {B2_TOTAL}')
    want_rules = (set(expected) - {'GOV'}) | ({'GOV'} if gov else set())
    if set(rules) != want_rules:
        out.append(f'el gate de B2 sobre HEAD falla en {sorted(rules)}, no en {sorted(want_rules)}')
    if not set(rules) <= B2_ALLOWED_RULES or ('CTX' in rules and branch != BRANCH):
        out.append(f'el gate de B2 sobre HEAD incumple comprobaciones materiales: reglas '
                   f'{sorted(set(rules) - B2_ALLOWED_RULES) or ["CTX"]}')
    for rid, (count, valid) in expected.items():
        if rid == 'GOV':
            continue
        n, items = rules.get(rid, (0, []))
        if n != count or len(items) != min(n, 3) or not all(valid(x) for x in items):
            out.append(f'{rid} del gate de B2 con {n} violaciones, no las {count} que predice el estado: {items[:2]}')
    n, items = rules.get('GOV', (0, []))
    if n != len(gov) or items != gov[:3]:
        out.append(f'GOV del gate de B2 con {n} violaciones distintas de las que da su lógica: {items[:2]}')
    foreign = [x for x in gov if not b2_gov_class(x, r2a.B2_LIFECYCLE_ITEMS)]
    if foreign or not set(content) <= set(gov):
        out.append(f'GOV del gate de B2 no se explica solo por el gobierno del cierre: {foreign[:2]}')
    if sorted(cases) != exp_cases:
        out.append(f'casos del gate de B2 en falla distintos de los previstos ({exp_cases}): {sorted(cases)[:5]}')
    line = r2a.mat_line(mat_obs, scp_n, 'previstas')
    return out, line, mat_obs


# ---------------------------------------------------------------- R2A: el gate de R2-A sobre HEAD, con su clase A
def r2a_expected(b3, r2a, sf, objs, parents, head, branch, b1, mat_obs):
    """La salida del gate de R2-A sobre este HEAD con su propia lógica (cargada de su blob verificado, a través de las
    funciones verificadas de B3), más su SUC, derivado del ALC de B2-SUCCESSOR-FREEZE con la lógica de este."""
    expected = b3.r2a_expected(r2a, objs, parents, head, branch, b1, mat_obs)
    sf_alc = sf.alc_problems()
    expected['SUC'] = [f'{r2a.GC_SUC_PREFIX}{sf_alc[:2]}']
    return expected, sf_alc


def r2a_class(r2a, sf, objs, parents, branch, expected, mat_obs, sf_alc):
    """Lo que, en la salida prevista del gate de R2-A, no es la clase A del cierre (§3.5)."""
    out = []
    own = set(parents) - set(ancestry(objs, B3_BASE))     # commits de B3 y del cierre: fuera de la historia de su base
    b3_files = later_files(objs)
    if set(expected) - R2A_ALLOWED:
        out.append(f'reglas ajenas a la clase A del cierre: {sorted(set(expected) - R2A_ALLOWED)}')
    ctx = [f'rama no permitida o HEAD separado: «{BRANCH}»'] if branch == BRANCH else []
    if expected.get('CTX', []) != ctx:
        out.append(f'CTX distinto de la rama del cierre: {expected.get("CTX", [])[:2]}')
    material = sorted({'DEP'} | ({'CTX'} if branch == BRANCH else set()))
    scp_n = mat_obs[3].get('SCP', (0,))[0]
    gc_scp, r2a_scp = 3 * (11 + len(r2a.GC_LAYER_FILES)), 3 * (11 + len(r2a.GC_LAYER_FILES) + len(r2a.LAYER_FILES))
    if scp_n != b2_scp_count(r2a, objs):
        out.append(f'SCP del gate de B2 con {scp_n} violaciones, no las {b2_scp_count(r2a, objs)} del cierre')
    gov_prefix = r2a.GC_GOV_PREFIX
    mat_ok = (f'el gate de B2 sobre HEAD incumple comprobaciones materiales: reglas {material}',
              f'SCP del gate de B2 con {scp_n} violaciones, no las {r2a_scp} que predice el estado: ')
    for item in expected.get('MAT', []):
        if not (item == mat_ok[0] or item.startswith(mat_ok[1]) or item.startswith(gov_prefix)):
            out.append(f'MAT ajeno a la clase A del cierre: {item[:120]}')
    formal = {p: e for p, e in gov_entries(objs, FORMAL_TRANSITION).items()}
    later = descendants(parents, FORMAL_TRANSITION)
    hidden = [c for c in topological(parents) if c in later and gov_entries(objs, c) != formal and c not in own]
    rule3 = re.compile(r"([0-9a-f]{12}): regla 3: descendiente de la transición del cierre formal sin su blob: "
                       r"\[(?:'CLAUDE\.md'|'docs/PROGRESS\.md'|'CLAUDE\.md', 'docs/PROGRESS\.md')\]")
    more = re.compile(r'… y (\d+) commits más con un blob de gobierno no admitido')
    effective = {f'{p}: {t}' for p in GOV_PATHS for t in (
        'árbol de HEAD distinto del blob del cierre formal', 'índice distinto del blob del cierre formal o en conflicto',
        'disco distinto del blob del cierre formal, enlace o ausente')}
    for item in expected.get('GOV', []):
        m = rule3.fullmatch(item)
        if not ((m and any(c.startswith(m.group(1)) for c in own)) or more.fullmatch(item) or item in effective):
            out.append(f'GOV ajeno a la regla 3 en los commits de B3 y del cierre y al estado efectivo: {item[:120]}')
    if hidden:
        out.append(f'GOV con commits sin el blob del cierre formal fuera de B3 y del cierre: {[c[:12] for c in hidden[:3]]}')
    sem_ok = {f'{p}: el estado vigente no declara a B2 CERRADA, CONGELADA E INTEGRADA' for p in GOV_PATHS} | \
        {'docs/PROGRESS.md: la cabecera no declara a B2 CERRADA E INTEGRADA'} | \
        {f"{p}: F35-SBX-B debe figurar solo INICIADA en el estado vigente: ['CERRADA']" for p in GOV_PATHS}
    for item in expected.get('SEM', []):
        if item not in sem_ok and not any(tokens_closed(item, f'{p}: declaraciones de estado contradictorias con el '
                                                              f'gobierno vigente: ', lambda x: x in F35B_CLOSED)
                                          for p in GOV_PATHS):
            out.append(f'SEM ajeno a la declaración del cierre: {item[:120]}')
    layer = TC_DELTA | {(p, 'A') for p in b3_files}
    alc = scope_delta(DEVELOP_GOV_MERGE, r2a.SCOPE)
    if len(expected.get('ALC', [])) != len(PLANES) or any(alc[plane] != layer for plane in PLANES):
        out.append('ALC no se explica solo por las rutas de B3 y del cierre en los tres planos')
    gc_alc = scope_delta(r2a.DEVELOP_MERGE, r2a.GC_SCOPE)
    gc_layer = layer | {(p, 'A') for p in r2a.LAYER_FILES}
    sf_want = layer | {(p, 'A') for p in r2a.LAYER_FILES + r2a.GC_LAYER_FILES} | {(p, 'M') for p in GOV_PATHS}
    sf_delta = scope_delta(SUCCESSOR, {p: 'A' for p in sf.CLOSURE_FILES})
    if expected.get('SUC') != [f'{r2a.GC_SUC_PREFIX}{sf_alc[:2]}'] or any(sf_delta[plane] != sf_want for plane in PLANES):
        out.append('SUC no se explica solo por las rutas posteriores a B2-SUCCESSOR-FREEZE en los tres planos')
    allowed_notes = set()
    if branch == BRANCH:
        allowed_notes.add('CTX del cierre de gobierno no se explica solo por la rama de este incremento: '
                          f"['rama no permitida o HEAD separado: «{BRANCH}»']")
    mat_prefix = 'MAT del cierre de gobierno no se explica solo por este incremento: '
    sem_prefix = 'SEM del cierre de gobierno no se explica solo por el cierre formal: '
    alc_prefix = 'ALC del cierre de gobierno no se explica solo por las rutas de esta capa: '
    for note in expected.get('GCL', []):
        if note in allowed_notes:
            continue
        if note.startswith(mat_prefix):
            body = note[len(mat_prefix):]
            if body == f'el gate de B2 sobre HEAD incumple comprobaciones materiales: reglas {material}'[:120] or \
                    body.startswith(f'SCP del gate de B2 con {scp_n} violaciones, no las {gc_scp} que predice el '
                                    f'estado: '[:120]) or body.startswith(gov_prefix[:120]):
                continue
        if note.startswith(sem_prefix):
            body = note[len(sem_prefix):]
            if any(body == f"{p}: F35-SBX-B debe figurar solo INICIADA en el estado vigente: ['CERRADA']"[:120] or
                   body.startswith(f'{p}: declaraciones de estado contradictorias con el gobierno vigente: '
                                   f"['«f35-sbx-b cerrada»'") for p in GOV_PATHS):
                continue
        if note.startswith(alc_prefix) and all(gc_alc[plane] == gc_layer for plane in PLANES):
            continue
        out.append(f'GCL con una nota ajena a la clase A del cierre: {note[:120]}')
    return out


def gov_entries(objs, commit):
    root = commit_parts(objs, commit)[0]
    return {p: entry(objs, root, p) for p in GOV_PATHS}


def r2a_problems(observed, b3, r2a, sf, objs, parents, head, branch, b1, mat_obs):
    code, out_bytes, err_bytes = observed
    ok, ko, rules, cases, info = parse_output(code, out_bytes, err_bytes, b3.R2A_SUMMARY, b3.R2A_INFO)
    expected, sf_alc = r2a_expected(b3, r2a, sf, objs, parents, head, branch, b1, mat_obs)
    out = r2a_class(r2a, sf, objs, parents, branch, expected, mat_obs, sf_alc)
    if set(rules) != set(expected) or cases or ok + ko != R2A_TOTAL:
        out.append(f'el gate de R2-A sobre HEAD falla en {sorted(rules)}, no en {sorted(expected)}')
    for rid, items in expected.items():
        n, shown = rules.get(rid, (0, []))
        if n != len(items) or shown != items[:3]:
            out.append(f'{rid} del gate de R2-A con {n} violaciones distintas de las previstas: {shown[:2]}')
    anc = ', '.join(c[:12] for c in CHAIN[:12])
    if info['ANC'].groups() != (anc, GOV_CLOSURE, DEVELOP_GOV_MERGE, head):
        out.append('el gate de R2-A no informa sus anclas registradas y este HEAD')
    if info['MAT'].group(0) != r2a.mat_line(mat_obs, 3 * (11 + len(r2a.GC_LAYER_FILES) + len(r2a.LAYER_FILES)),
                                            'previstas'):
        out.append('la línea INFO de MAT del gate de R2-A no es la que da la salida del gate de B2 observada')
    suc = info['SUC'].groups()
    if suc[0] != '1' or int(suc[1]) + int(suc[2]) != SF_TOTAL or suc[3] != 'ALC, VIG' or suc[5] != SUCCESSOR_FREEZE \
            or not {x.strip() for x in suc[4].split(',')} <= {'ALC', 'CON', 'MAT'}:
        out.append('la línea INFO de SUC del gate de R2-A no es la de B2-SUCCESSOR-FREEZE con solo VIG y ALC')
    if info['GCL'].group(4) != info['GCL'].group(5) or int(info['GCL'].group(2)) + int(info['GCL'].group(3)) != GC_TOTAL:
        out.append('el cierre de gobierno sobre HEAD no falla exactamente en las reglas que el gate de R2-A prevé')
    if info['HIS'].groups() != (GOV_CLOSURE, '0', str(GC_TOTAL), '0', GOV_CLOSURE, CLOSURE_TRANSITION):
        out.append('el gate de R2-A no acredita el cierre de gobierno anclado en 13/0')
    if info['GOV'].groups() != (FORMAL_TRANSITION, FORMAL_TRANSITION):
        out.append(f'el gate de R2-A no deriva ni registra su transición {FORMAL_TRANSITION[:12]}')
    if info['FRZ'].group(1) != R2A_COMPLETION:
        out.append(f'el gate de R2-A deriva su capa en {info["FRZ"].group(1)[:12]}, no en {R2A_COMPLETION[:12]}')
    line = (f'INFO R2A: gate de R2-A sobre HEAD: código {code}; {ok} correctas, {ko} fallas; reglas en falla: '
            f'{", ".join(sorted(rules)) or "ninguna"}; previstas: {", ".join(sorted(expected)) or "ninguna"}')
    return out, line


# ---------------------------------------------------------------- B3G: el gate de B3 sobre HEAD, con su clase A
def b3_expected(b3, r2a, objs, parents, head, branch, b1, mat_obs, r2a_observed):
    """La salida del gate de B3 sobre este HEAD con su propia lógica, cargada de su blob verificado: {regla:
    violaciones} de sus reglas que no ejecutan subgates ni el pipeline, y su línea INFO de R2A."""
    b3_mat, b3_cases, b3_content = r2a.predicted_b2(objs, parents, head, branch,
                                                    r2a.GC_LAYER_FILES + r2a.LAYER_FILES + b3.LAYER_FILES,
                                                    r2a.B2_LIFECYCLE_ITEMS, b3.BRANCH)
    b3_mat['DEP'] = (1, lambda x: x == b3.B2_DEP_ITEM)
    r2a_items, r2a_line = b3.r2a_problems(r2a_observed, r2a, objs, parents, head, branch, b1, mat_obs)
    expected = {'CTX': b3.ctx_problems(branch, parents),
                'ANC': b3.anc_problems(objs),
                'R2A': r2a_items,
                'MAT': r2a.b2_problems(mat_obs, b3_mat, b3_cases, b3_content),
                'INT': b3.int_problems(objs, parents),
                'FLG': b3.flg_problems(),
                'GOV': b3.gov_problems(objs, parents, head, {}),
                'SEM': b3.sem_problems(objs, head, b1, r2a),
                'ALC': b3.alc_problems(objs, head),
                'FRZ': b3.frz_problems(objs, head, parents, {}),
                'DEP': b3.dep_problems()}
    return {rid: items for rid, items in expected.items() if items}, r2a_line


def b3_class(b3, r2a, objs, parents, branch, expected, mat_obs, r2a_rules, r2a_previstas):
    """Lo que, en la salida prevista del gate de B3, no es la clase A del cierre (§3.5)."""
    out = []
    if set(expected) - B3G_ALLOWED:
        out.append(f'reglas ajenas a la clase A del cierre: {sorted(set(expected) - B3G_ALLOWED)}')
    ctx = [f'rama no permitida o HEAD separado: «{BRANCH}»'] if branch == BRANCH else []
    if expected.get('CTX', []) != ctx:
        out.append(f'CTX distinto de la rama del cierre: {expected.get("CTX", [])[:2]}')
    r2a_ok = ('MAT no se explica solo por DEP del pipeline y las rutas de B3 en SCP: ',
              'SEM ajeno a la declaración de B3 sobre el cierre de B2: ',
              'ALC no se explica solo por las rutas de B3 en los tres planos',
              'GCL con notas ajenas a la clase A de B3: ')
    suc_only = f'el gate de R2-A sobre HEAD falla en {sorted(r2a_rules)}, no en {sorted(r2a_previstas)}'
    for item in expected.get('R2A', []):
        if item.startswith(r2a_ok) or (item == f"CTX distinto de la rama de B3: ['rama no permitida o HEAD separado: "
                                               f"«{BRANCH}»']" and branch == BRANCH):
            continue
        if item == suc_only and set(r2a_rules) - set(r2a_previstas) == {'SUC'} and set(r2a_previstas) <= set(r2a_rules):
            continue
        out.append(f'R2A de B3 ajeno a la clase A del cierre: {item[:120]}')
    scp_n = mat_obs[3].get('SCP', (0,))[0]
    b3_scp = 3 * (11 + len(r2a.GC_LAYER_FILES) + len(r2a.LAYER_FILES) + len(b3.LAYER_FILES))
    for item in expected.get('MAT', []):
        if item == "el gate de B2 sobre HEAD incumple comprobaciones materiales: reglas ['CTX']" and branch == BRANCH:
            continue
        if item.startswith(f'SCP del gate de B2 con {scp_n} violaciones, no las {b3_scp} que predice el estado: ') \
                and scp_n == b2_scp_count(r2a, objs):
            continue
        if item.startswith(r2a.GC_GOV_PREFIX):
            continue
        out.append(f'MAT de B3 ajeno a la clase A del cierre: {item[:120]}')
    own = {c[:12] for c in set(parents) - set(ancestry(objs, BASE))}      # commits del cierre: fuera de su base
    rule3 = re.compile(r"([0-9a-f]{12}): regla 3: descendiente de la transición de B3 sin su blob: "
                       r"\[(?:'CLAUDE\.md'|'docs/PROGRESS\.md'|'CLAUDE\.md', 'docs/PROGRESS\.md')\]")
    more = re.compile(r'… y (\d+) commits más con un blob de gobierno no admitido')
    effective = {f'{p}: {t}' for p in GOV_PATHS for t in (
        'árbol de HEAD distinto del blob de B3', 'índice distinto del blob de B3 o en conflicto',
        'disco distinto del blob de B3, enlace o ausente')}
    for item in expected.get('GOV', []):
        m = rule3.fullmatch(item)
        if not ((m and m.group(1) in own) or more.fullmatch(item) or item in effective):
            out.append(f'GOV de B3 ajeno a la transición del cierre: {item[:120]}')
    sem_ok = {f"{p}: F35-SBX-B debe figurar solo INICIADA en el estado vigente: ['CERRADA']" for p in GOV_PATHS} | \
        {f'{p}: el estado vigente no declara a B3 IMPLEMENTADA sobre B2 CERRADA, CONGELADA E INTEGRADA'
         for p in GOV_PATHS} | {'docs/PROGRESS.md: la cabecera no declara a B3 IMPLEMENTADA'}
    for item in expected.get('SEM', []):
        if item in sem_ok:
            continue
        if any(tokens_closed(item, f'{p}: B3 en un estado distinto de IMPLEMENTADA: ', B3_CLOSED_RX.fullmatch) or
               tokens_closed(item, f'{p}: declaraciones de estado contradictorias con el gobierno vigente: ',
                             lambda x: x in F35B_CLOSED) for p in GOV_PATHS):
            continue
        out.append(f'SEM de B3 ajeno a la declaración del cierre: {item[:120]}')
    alc = scope_delta(B3_BASE, b3.SCOPE)
    if len(expected.get('ALC', [])) != len(PLANES) or any(alc[plane] != TC_DELTA for plane in PLANES):
        out.append('ALC de B3 no se explica solo por las rutas del cierre y ACADEMIC_BASELINE.md en los tres planos')
    return out


def b3g_problems(observed, b3, r2a, objs, parents, head, branch, b1, mat_obs, r2a_observed, r2a_rules):
    code, out_bytes, err_bytes = observed
    ok, ko, rules, cases, info = parse_output(code, out_bytes, err_bytes, B3_SUMMARY, B3_INFO)
    expected, r2a_line = b3_expected(b3, r2a, objs, parents, head, branch, b1, mat_obs, r2a_observed)
    previstas = [x.strip() for x in r2a_line.split('previstas: ', 1)[1].split(',') if x.strip() != 'ninguna']
    out = b3_class(b3, r2a, objs, parents, branch, expected, mat_obs, r2a_rules, previstas)
    observed_rules = set(rules)
    if observed_rules - set(expected) - {'ENT', 'HIS', *B3_PIPE_RULES}:
        out.append(f'el gate de B3 sobre HEAD falla en {sorted(observed_rules)}, no en {sorted(expected)}')
    if observed_rules & ({'ENT', 'HIS'} | set(B3_PIPE_RULES)):
        out.append(f'el gate de B3 sobre HEAD incumple reglas que deben pasar: '
                   f'{sorted(observed_rules & ({"ENT", "HIS"} | set(B3_PIPE_RULES)))}')
    if cases or ok + ko != B3_TOTAL:
        out.append(f'el gate de B3 informa {ok + ko} comprobaciones, no {B3_TOTAL}')
    for rid, items in expected.items():
        n, shown = rules.get(rid, (0, []))
        if n != len(items) or shown != items[:3]:
            out.append(f'{rid} del gate de B3 con {n} violaciones distintas de las previstas: {shown[:2]}')
    if info['ANC'].groups() != (', '.join(c[:12] for c in b3.CHAIN), B3_BASE, head):
        out.append('el gate de B3 no informa sus anclas registradas y este HEAD')
    if info['MAT'].group(0) != r2a.mat_line(mat_obs, 3 * (11 + len(r2a.GC_LAYER_FILES) + len(r2a.LAYER_FILES) +
                                                          len(b3.LAYER_FILES)), 'previstas'):
        out.append('la línea INFO de MAT del gate de B3 no es la que da la salida del gate de B2 observada')
    if info['PIP'].groups() != (str(REPORT_BYTES), REPORT_SHA256, 'completado'):
        out.append('el informe del pipeline sobre HEAD no es el registrado (bytes, SHA-256 o resultado)')
    if info['R2A'].group(0) != r2a_line:
        out.append('la línea INFO de R2A del gate de B3 no es la que da la salida del gate de R2-A observada')
    if info['HIS'].groups() != (R2A_COMPLETION, '0', str(R2A_TOTAL), '0', R2A_COMPLETION, FORMAL_TRANSITION):
        out.append('el gate de B3 no acredita R2-A anclado en 14/0')
    if info['GOV'].groups() != (B3_TRANSITION, B3_TRANSITION):
        out.append(f'el gate de B3 no deriva ni registra su transición {B3_TRANSITION[:12]}')
    if info['FRZ'].group(1) != B3_ANCHOR:
        out.append(f'el gate de B3 deriva su capa en {info["FRZ"].group(1)[:12]}, no en la aprobada {B3_ANCHOR[:12]}')
    line = (f'INFO B3G: gate de B3 sobre HEAD: código {code}; {ok} correctas, {ko} fallas; reglas en falla: '
            f'{", ".join(sorted(rules)) or "ninguna"}; previstas: {", ".join(sorted(expected)) or "ninguna"}')
    return out, line


# ---------------------------------------------------------------- ALC, FRZ y DEP
def alc_problems(objs, head):
    out = []
    for plane, delta in scope_delta(BASE, SCOPE).items():
        if delta:
            out.append(f'{plane}: alcance distinto del enumerado para el cierre: {sorted(delta)[:3]}')
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
    info.append(f'INFO ANC: anclas registradas {", ".join(c[:12] for c in CHAIN)}; base {BASE}; HEAD {head}')
    objs, background = None, {}
    try:
        objs = Objects()
        parents = branch = None
        try:
            parents = ancestry(objs, head)
            branch = current_branch()
        except ERRORS as e:
            closed(('CTX', 'B3G', 'R2A', 'MAT', 'INT', 'GOV', 'FRZ'), f'historia desde HEAD ({e.__class__.__name__}: {e})')
        if parents is not None:
            check('CTX', ctx_problems, branch, parents)
        check('ANC', anc_problems, objs)
        blobs = {}
        for rid, name, clone in (('HIS', 'b3', (B3_ANCHOR, B3_BRANCH)), ('B3G', 'b3', None), ('R2A', 'r2a', None),
                                 ('MAT', 'b2', None)):
            try:
                blobs[name] = blobs.get(name) or gate_blob(objs, name)
                background[rid] = Background(rid.lower(), VERIFIED[name][1], blobs[name], clone)
            except ERRORS as e:
                closed((rid,), f'ejecución del gate congelado ({e.__class__.__name__}: {e})')
        mods = {}
        try:
            mods = {name: load_verified(objs, name) for name in ('b1', 'b2', 'sf', 'r2a', 'b3')}
        except ERRORS as e:
            mods = {}
            closed(('SEM', 'B3G', 'R2A', 'MAT'), f'gates congelados verificados ({e.__class__.__name__}: {e})')
        if parents is not None:
            check('INT', int_problems, objs, parents)
            check('GOV', gov_problems, objs, parents, head, notes)
            check('FRZ', frz_problems, objs, head, parents, notes)
        if mods:
            check('SEM', sem_problems, objs, head, mods['b1'], mods['r2a'])
        check('LOW', low_problems, objs, head)
        check('ALC', alc_problems, objs, head)
        outputs = {}
        for rid in ('MAT', 'R2A', 'B3G', 'HIS'):
            if rid in background:
                try:
                    outputs[rid] = background[rid].result()
                except ERRORS as e:
                    closed((rid,), f'ejecución del gate congelado ({e.__class__.__name__}: {e})')
        mat_obs = None
        if 'MAT' in outputs and mods and parents is not None:
            mat = check('MAT', mat_problems, objs, parents, head, branch, outputs['MAT'], mods['b1'], mods['b2'],
                        mods['r2a'])
            if mat:
                info.append(mat[0])
                mat_obs = mat[1]
        elif 'MAT' in outputs:
            closed(('MAT',), 'no clasificable sin la historia y los gates verificados')
        r2a_rules = None
        for rid in ('R2A', 'B3G'):
            if rid in outputs and mat_obs is None:
                closed((rid,), 'no verificable sin la salida del gate de B2')
        if 'R2A' in outputs and mat_obs is not None:
            r2 = check('R2A', r2a_problems, outputs['R2A'], mods['b3'], mods['r2a'], mods['sf'], objs, parents, head,
                       branch, mods['b1'], mat_obs)
            if r2:
                info.append(r2[0])
            try:
                r2a_rules = parse_output(*outputs['R2A'], mods['b3'].R2A_SUMMARY, mods['b3'].R2A_INFO)[2]
            except ERRORS as e:
                closed(('B3G',), f'salida del gate de R2-A ({e.__class__.__name__}: {e})')
        if 'B3G' in outputs and mat_obs is not None and r2a_rules is not None:
            g3 = check('B3G', b3g_problems, outputs['B3G'], mods['b3'], mods['r2a'], objs, parents, head, branch,
                       mods['b1'], mat_obs, outputs['R2A'], r2a_rules)
            if g3:
                info.append(g3[0])
        elif 'B3G' in outputs and mat_obs is not None:
            closed(('B3G',), 'no verificable sin la salida del gate de R2-A')
        if 'HIS' in outputs:
            his = check('HIS', his_problems, *outputs['HIS'])
            if his:
                info.append(his[0])
    except ERRORS as e:
        closed(('CTX', 'ANC', 'HIS', 'B3G', 'R2A', 'MAT', 'INT', 'GOV', 'SEM', 'LOW', 'ALC', 'FRZ'),
               f'objetos Git ({e.__class__.__name__}: {e})')
    finally:
        for rid, job in background.items():
            try:
                job.close()
            except OSError as e:
                viol[rid].append(f'limpieza incompleta del temporal ({e.__class__.__name__}): falla cerrado')
        if objs is not None:
            objs.close()
    info.append(f'INFO GOV: transición del cierre terminal derivada: {notes["transition"] or "ninguna"}; registrada: '
                f'{TC_TRANSITION}')
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
    print(f'validate_f35sbxb_cierre_terminal: {len(ORDER) - len(fallas)} comprobaciones correctas, {len(fallas)} fallas')
    sys.exit(1 if fallas else 0)


if __name__ == '__main__':
    main()
