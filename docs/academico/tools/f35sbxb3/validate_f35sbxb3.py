"""F35-SBX-B — B3: gate sucesor del pipeline determinista de evidencia sintética (validate_f35sbxb3.py).

Uso:  python -I docs/academico/tools/f35sbxb3/validate_f35sbxb3.py   (sin -I, se relanza)

Contrato: docs/academico/evidencia-sbx-b3/F35SBXB_B3_Pipeline.md. Valida B3, el pipeline de doce pasos sobre el almacén
de B2, y su registro en el gobierno con una transición única y monotónica (B2_FORMAL_GOVERNANCE_BLOB →
B3_GOVERNANCE_BLOB). Conserva la evaluación vigente: el gate de R2-A y el de B2 se ejecutan intactos, desde los bytes
verificados de sus blobs; su falla de clase A se predice desde el estado observado y se clasifica con exactitud, y lo
que esa falla enmascara se repone con reglas propias. Ejecuta el pipeline y sus pruebas, recalcula la conformidad sin
fiarse del informe y comprueba la doble ejecución, la purga y el fallo inyectado en cada paso. El repositorio solo se
lee; los subgates y el pipeline escriben únicamente sus temporales fuera de él. Cada objeto Git que se lee se verifica
recalculando su identificador, y todo error, salida incompleta o estado no evaluable falla cerrado.

  ENT  intérprete aislado y sin PYTHONPATH, PYTHONHOME ni PYTHONUSERBASE; ninguna variable de Git que redirija el
       repositorio; Git sobre el repositorio de este archivo, con historia completa y sin injertos ni reemplazos.
  CTX  rama feature/f35-sbx-b3-deterministic-pipeline, develop o main; el merge ca36875, ancestro de HEAD.
  ANC  anclas registradas, íntegras y en cadena (de 8e94a60 a ca36875 y la transición de B3); los merges eb02c2d,
       04895aa y ca36875 con sus padres y árboles; blobs de gobierno de las cinco etapas.
  HIS  el gate de R2-A, con los bytes de su blob en ad193f9, anclado sobre ad193f9 en un clon temporal sin remoto:
       código 0, 14/0, FRZ en ad193f9 y GOV en ddefb7d.
  R2A  el mismo gate sobre HEAD: su salida es exactamente la que su lógica da sobre el estado observado, y solo falla
       por la clase A de B3 (CTX en la rama, GCL, MAT, GOV, SEM y ALC).
  MAT  el gate de B2, con los bytes de su blob en el candidato, sobre HEAD: solo lo que predice el estado observado,
       con DEP limitado al pipeline.
  INT  capas congeladas, de A a R2-A, desde sus anclas, en cada commit posterior, HEAD, índice y disco.
  FLG  ningún flag en el índice.
  GOV  transición única y monotónica en cinco etapas, registrada; estado efectivo en HEAD, índice y disco.
  SEM  semántica del gobierno y del documento de la capa con las piezas verificadas del gate de B1: B2 cerrada, B3
       solo implementada y ningún otro estado cambiado.
  ALC  alcance exacto frente a ca36875: las cinco rutas A de la capa y el gobierno M; sin archivos sin seguimiento.
  FRZ  nivel B: un único commit posterior a ca36875 completa la capa y, desde él, sus archivos no cambian. Su hash se
       deriva de Git y se registra fuera, nunca en un archivo.
  DEP  biblioteca estándar autorizada por archivo; la única ejecución dinámica de cada archivo es su carga verificada;
       ningún .py fuera del pipeline y de B2 nombra el almacén.
  PIP  pipeline completo: código 0 e informe canónico, con esquema cerrado, entradas verificadas y tres runs completados.
  DET  dos ejecuciones más, en procesos nuevos: los mismos bytes.
  CNF  conformidad de nivel 1 y nivel 2 recalculada aquí, desde los fixtures de A y evidence.csv verificados.
  PUR  comprobantes de purga verificados, E-PURGADO tras la purga y ningún archivo nuevo en el árbol de trabajo.
  TSB  las pruebas del pipeline: exactamente PT01..PT30 en verde.
  FAL  fallo inyectado en cada paso de ORG-S1: fallido, código 1, sin tablas y bytes repetibles.
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
import csv  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
import types  # noqa: E402
import unicodedata  # noqa: E402

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
BASE = 'ca36875938eca035c97205921ec5f9633381c571'               # integración de R2-A en develop; base de B3
# Commit de la transición de gobierno de B3. Se registra después de que exista, nunca en el propio commit.
B3_TRANSITION = 'fa5664a0a3660519744a32b320822ecc396b1619'
CHAIN = (B1_ANCHOR, B1_CLOSURE, B2_BASE, B2_TRANSITION, CANDIDATE, FREEZE, SUCCESSOR, SUCCESSOR_FREEZE, DEVELOP_MERGE,
         CLOSURE_TRANSITION, GOV_CLOSURE, DEVELOP_GOV_MERGE, FORMAL_TRANSITION, R2A_COMPLETION, BASE, B3_TRANSITION)
MERGES = ((DEVELOP_MERGE, B2_BASE, SUCCESSOR_FREEZE), (DEVELOP_GOV_MERGE, DEVELOP_MERGE, GOV_CLOSURE),
          (BASE, DEVELOP_GOV_MERGE, R2A_COMPLETION))

BRANCH = 'feature/f35-sbx-b3-deterministic-pipeline'
BRANCHES = (BRANCH, 'develop', 'main')
R2A_BRANCH = 'chore/f35-sbx-b2-r2a-final-closure'
GOV_PATHS = ('CLAUDE.md', 'docs/PROGRESS.md')
GOV_BLOBS = {'b1': (B1_ANCHOR, {'CLAUDE.md': 'b7068afbfac6cc2f1f39053dff8face38b894415',
                                'docs/PROGRESS.md': '983844fd2477432b2a1ea402aa8b3130678a014a'}),
             'b2': (B2_TRANSITION, {'CLAUDE.md': '74cc4a71c56918678e0a70c7f59a3f060d87b6a0',
                                    'docs/PROGRESS.md': '07889bf8c82990651539a6e4b8a1098b4bd2d35a'}),
             'cierre': (CLOSURE_TRANSITION, {'CLAUDE.md': 'dcf584c28f8b0f044e3ab9fc11cc117fc17e8a8c',
                                             'docs/PROGRESS.md': '49390335d47a13468f0a5b4017cf6b5723ad8ecb'}),
             'formal': (FORMAL_TRANSITION, {'CLAUDE.md': '0f9d516fd129ba83058076e6bffb293e9be1fac1',
                                            'docs/PROGRESS.md': '60a891fbf7967d4bcc9342ed43b10f1b587540e7'}),
             'b3': (B3_TRANSITION, {'CLAUDE.md': '8e908661b96a557d078d0036a41e319b2a3bb76c',
                                    'docs/PROGRESS.md': '4146a9d331f2d3f6240aedd599eb0238c578f761'})}
STAGES = ('b1', 'b2', 'cierre', 'formal', 'b3')
B1_GATE = 'docs/academico/tools/f35sbxb/validate_f35sbxb.py'
B2_TOOLS = 'docs/academico/tools/f35sbxb2'
B2_GATE = B2_TOOLS + '/validate_f35sbxb2.py'
R2A_GATE = 'docs/academico/tools/f35sbxb2_cierre_formal/validate_f35sbxb2_cierre_formal.py'

# Capas congeladas (INT): cada una con su ancla y sus carpetas, cuyo contenido exacto se toma del árbol del ancla. El
# gobierno no está aquí: lo protege GOV.
R2A_DIRS = ('docs/academico/evidencia-sbx-b2-cierre-formal', 'docs/academico/tools/f35sbxb2_cierre_formal')
FROZEN = (('A', A_ANCHOR, ('docs/academico/evidencia-sbx', 'docs/academico/tools/f35sbx')),
          ('B1', B1_ANCHOR, ('docs/academico/evidencia-sbx-b', 'docs/academico/tools/f35sbxb')),
          ('B1-FREEZE', B1_CLOSURE, ('docs/academico/evidencia-sbx-b-freeze', 'docs/academico/tools/f35sbxb_freeze')),
          ('B2', CANDIDATE, ('docs/academico/evidencia-sbx-b2', B2_TOOLS)),
          ('B2-FREEZE', FREEZE, ('docs/academico/evidencia-sbx-b2-freeze', 'docs/academico/tools/f35sbxb2_freeze')),
          ('sucesor', SUCCESSOR, ('docs/academico/evidencia-sbx-b2-sucesor', 'docs/academico/tools/f35sbxb2_sucesor')),
          ('B2-SUCCESSOR-FREEZE', SUCCESSOR_FREEZE, ('docs/academico/evidencia-sbx-b2-sucesor-freeze',
                                                     'docs/academico/tools/f35sbxb2_sucesor_freeze')),
          ('B2-GOVERNMENT-CLOSURE', GOV_CLOSURE, ('docs/academico/evidencia-sbx-b2-cierre-gobierno',
                                                  'docs/academico/tools/f35sbxb2_cierre_gobierno')),
          ('R2-A', R2A_COMPLETION, R2A_DIRS))

# Capa de B3 (nivel B), con su contenido exacto.
LAYER_DOCS = 'docs/academico/evidencia-sbx-b3'
LAYER_TOOLS = 'docs/academico/tools/f35sbxb3'
LAYER_DIRS = {LAYER_DOCS: ('F35SBXB_B3_Pipeline.md',),
              LAYER_TOOLS: ('sbxb_pipeline.py', 'test_f35sbxb3.py', 'test_sbxb_pipeline.py', 'validate_f35sbxb3.py')}
LAYER_FILES = tuple(sorted(f'{folder}/{name}' for folder, names in LAYER_DIRS.items() for name in names))
DOC = LAYER_DOCS + '/F35SBXB_B3_Pipeline.md'
PIPELINE = LAYER_TOOLS + '/sbxb_pipeline.py'
PIPELINE_TESTS = LAYER_TOOLS + '/test_sbxb_pipeline.py'
VALIDATOR = LAYER_TOOLS + '/validate_f35sbxb3.py'
TESTS = LAYER_TOOLS + '/test_f35sbxb3.py'
SCOPE = {**{p: 'A' for p in LAYER_FILES}, **{p: 'M' for p in GOV_PATHS}}

# Delta de gobierno de B3 (§4.11): lista cerrada de reemplazos literales sobre B2_FORMAL_GOVERNANCE_BLOB, cada bloque
# antiguo presente exactamente una vez.
_FORMAL_STATE = ('F35-SBX-B INICIADA solo como sandbox sintético: B1 (gate sucesor sobre HEAD) CERRADA, CONGELADA E '
                 'INTEGRADA; B2 (almacén efímero SQLite `:memory:` por organización sintética) CERRADA, CONGELADA E '
                 'INTEGRADA, sin pipeline funcional ni ML.')
_B3_STATE = ('F35-SBX-B INICIADA solo como sandbox sintético: B1 (gate sucesor sobre HEAD) CERRADA, CONGELADA E '
             'INTEGRADA; B2 (almacén efímero SQLite `:memory:` por organización sintética) CERRADA, CONGELADA E '
             'INTEGRADA; B3 (pipeline determinista de doce pasos sobre el almacén de B2) IMPLEMENTADA, sin ML.')
_FORMAL_TAIL = ('su cierre formal está registrado en [`evidencia-sbx-b2-cierre-formal`]'
                '({root}evidencia-sbx-b2-cierre-formal/F35SBXB_B2_Cierre_Formal.md).')
_B3_TAIL = ('su cierre formal está registrado en [`evidencia-sbx-b2-cierre-formal`]'
            '({root}evidencia-sbx-b2-cierre-formal/F35SBXB_B2_Cierre_Formal.md); su incremento B3 (pipeline '
            'determinista de doce pasos sobre el almacén de B2) está IMPLEMENTADO, registrado en [`evidencia-sbx-b3`]'
            '({root}evidencia-sbx-b3/F35SBXB_B3_Pipeline.md).')
_FORMAL_HEADER = ('Última actualización: 2026-10-18 (F34E CERRADA; G0 real NO APROBADA; G0-SBX APROBADA CON '
                  'RESTRICCIONES; F35-SBX sintética HABILITADA; F35-SBX-A CERRADA E INTEGRADA; B0 CERRADA E INTEGRADA; '
                  'F35-SBX-B INICIADA: B1 CERRADA E INTEGRADA, B2 CERRADA E INTEGRADA).')
_B3_HEADER = ('Última actualización: 2026-10-19 (F34E CERRADA; G0 real NO APROBADA; G0-SBX APROBADA CON RESTRICCIONES; '
              'F35-SBX sintética HABILITADA; F35-SBX-A CERRADA E INTEGRADA; B0 CERRADA E INTEGRADA; F35-SBX-B '
              'INICIADA: B1 CERRADA E INTEGRADA, B2 CERRADA E INTEGRADA, B3 IMPLEMENTADA).')
_FORMAL_HISTORY = ('El 18/10/2026 pasó a B2 cerrada e integrada, con su cierre de gobierno auditado e integrado y su '
                   'cierre formal registrado.')
_B3_HISTORY = _FORMAL_HISTORY + (' El 19/10/2026 pasó a B3 implementada: el pipeline determinista de doce pasos sobre '
                                 'el almacén de B2.')
B3_DELTA = {'CLAUDE.md': [(_FORMAL_STATE, _B3_STATE),
                          (_FORMAL_TAIL.format(root='docs/academico/'), _B3_TAIL.format(root='docs/academico/'))],
            'docs/PROGRESS.md': [(_FORMAL_HEADER, _B3_HEADER), (_FORMAL_HISTORY, _B3_HISTORY),
                                 (_FORMAL_STATE, _B3_STATE),
                                 (_FORMAL_TAIL.format(root='academico/'), _B3_TAIL.format(root='academico/'))]}
B3_SECTION = ('B2 (almacén efímero SQLite `:memory:` por organización sintética) CERRADA, CONGELADA E INTEGRADA; B3 '
              '(pipeline determinista de doce pasos sobre el almacén de B2) IMPLEMENTADA, sin ML.',
              'su incremento B2 (almacén efímero aislado) está CERRADO, CONGELADO E INTEGRADO en `develop` y `main`',
              'su incremento B3 (pipeline determinista de doce pasos sobre el almacén de B2) está IMPLEMENTADO')
B3_HEADER = 'B2 CERRADA E INTEGRADA, B3 IMPLEMENTADA).'
NO_PIPELINE = 'sin pipeline funcional'
PENDING = 'PENDIENTE DE CIERRE FORMAL'
# Ciclo de vida de B3 (§4.15): implementada es su único estado; cerrada, congelada, integrada, aprobada, productiva,
# publicada, desplegada y la reapertura se rechazan. El texto llega normalizado por las piezas del gate de B1.
B3_FORBIDDEN_RX = re.compile(r'(?<![\w-])b3(?![\w-])(?:\s*\([^()]*\))?((?:\s+[a-z0-9-]+){0,3}?)\s*(?:=|:|\s)\s*'
                             r'(cerrad\w*|congelad\w*|integrad\w*|aprobad\w*|productiv\w*|publicad\w*|desplegad\w*|'
                             r'reabiert\w*|reabr\w*|reapert\w*)\b')

# Pipeline: informe canónico (§4.5), sus constantes y las del almacén de B2 que el informe declara.
TENANTS = ('ORG-S1', 'ORG-S2', 'ORG-S3')
STEP_NAMES = {1: 'fixture_verificado', 2: 'esquema_validado', 3: 'sintetico_verificado', 4: 'hash_calculado',
              5: 'provenance_registrada', 6: 'transformado', 7: 'tenant_validado', 8: 'revision_simulada',
              9: 'resultado_experimental', 10: 'auditoria_encadenada', 11: 'ejecucion_cerrada', 12: 'purga'}
HEADER = {'report_version': 'f35sbxb3-report-1.0.0', 'pipeline_version': 'f35sbxb-0',
          'contract_version': 'f35sbxb-contract-1.0.0', 'run_kind': 'ejecucion_sbx_b', 'environment': 'sandbox',
          'source_type': 'synthetic'}
REPORT_KEYS = frozenset(HEADER) | {'result', 'inputs'}
RUN_KEYS = frozenset({'synthetic_organization_id', 'seed', 'clock_start', 'final_state', 'steps', 'tables', 'counts',
                      'conformity', 'receipt', 'post_purge'})
FAILURE_KEYS = frozenset({'synthetic_organization_id', 'step', 'step_name', 'error_code', 'message', 'closure'})
RECEIPT_KEYS = frozenset({'closure_kind', 'pipeline_run_id', 'synthetic_organization_id', 'final_state', 'failed_event',
                          'failed_event_record', 'error_code', 'last_event_hash', 'counts', 'file_backed', 'observed',
                          'connection', 'post_close_check', 'receipt_hash'})
ENTITIES = {'tenant_context': 'SyntheticTenantContext', 'pipeline_run': 'SyntheticPipelineRun',
            'pipeline_event': 'SyntheticPipelineEvent', 'evidence_source': 'SyntheticEvidenceSource',
            'evidence_record': 'SyntheticEvidenceRecord', 'evidence_provenance': 'SyntheticEvidenceProvenance',
            'simulated_review': 'SyntheticHumanReview', 'audit_entry': 'SyntheticAuditEntry'}
COUNTS = {'tenant_context': 1, 'pipeline_run': 1, 'pipeline_event': 7, 'evidence_source': 2, 'evidence_record': 2,
          'evidence_provenance': 2, 'simulated_review': 2, 'audit_entry': 8}
PATH = ['pendiente', 'validando', 'registrado', 'transformado', 'en_revision', 'revisado', 'completado']
ACTIONS = ['fixture_verificado', 'esquema_validado', 'sintetico_verificado', 'hash_calculado', 'provenance_registrada',
           'tenant_validado', 'revision_simulada_registrada', 'ejecucion_cerrada']
A_DIR = 'docs/academico/evidencia-sbx/'
A_MANIFEST = A_DIR + 'fixtures/manifest.json'
A_MANIFEST_SHA256 = '2df919ebde68fdf959b169d0249141422d84dc3ae4cfc29a9d2601735c915a4b'
A_CONTRACT = A_DIR + 'contrato/f35sbx_contract.json'
F34_DIR = 'docs/academico/datos-sinteticos/dataset/'
F34_MANIFEST_SHA256 = '079aae87916530b99fb97f22414d8c7d4938e8b7edd7d3527e5fa9db555af431'
F34_FILES = ('evidence.csv', 'criteria.csv', 'vacancies.csv', 'applications.csv')
DATASET_VERSION = 'f34-synth-1.1.0'
HASH_ALGORITHM = 'f35sbx-content-sha256-v1'
EVIDENCE_KINDS = ('formulario', 'nota_entrevista', 'prueba')
GENESIS = '0' * 64
TS_RX = re.compile(r'20[0-9]{2}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])T([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]')
PT_LINE = re.compile(r'OK    (PT\d{2}) .+')
PT_SUMMARY = 'test_sbxb_pipeline: 30 casos correctos, 0 fallas'
PT_IDS = [f'PT{k:02d}' for k in range(1, 31)]

DEP_ALLOWED = {VALIDATOR: frozenset({'ast', 'csv', 'hashlib', 'json', 'os', 're', 'subprocess', 'sys', 'types',
                                     'unicodedata'}),
               PIPELINE: frozenset({'csv', 'hashlib', 'json', 'os', 're', 'sys', 'types', 'unicodedata'}),
               PIPELINE_TESTS: frozenset({'copy', 'hashlib', 'json', 'os', 'sbxb_pipeline', 'subprocess', 'sys'}),
               TESTS: frozenset({'hashlib', 'os', 'subprocess', 'sys'})}
LOADERS = {VALIDATOR: 'load_verified', PIPELINE: 'load_store'}   # única función con ejecución dinámica de cada archivo
DYNAMIC_CODE = frozenset({'__import__', 'compile', 'eval', 'exec'})
ORDER = ('ENT', 'CTX', 'ANC', 'HIS', 'R2A', 'MAT', 'INT', 'FLG', 'GOV', 'SEM', 'ALC', 'FRZ', 'DEP', 'PIP', 'DET', 'CNF',
         'PUR', 'TSB', 'FAL')
PIPE_RULES = ('PIP', 'DET', 'CNF', 'PUR', 'TSB', 'FAL')
PLANES = ('HEAD', 'árbol', 'índice')
TIMEOUT = 3600
# Niveles de clones compartidos admitidos bajo este repositorio: el gate de R2-A sobre HEAD anida tres más (el cierre
# de gobierno, B2-SUCCESSOR-FREEZE y el gate sucesor anclados) y Git no sigue más de seis.
MAX_ALTERNATES = 3
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
R2A_SUMMARY = re.compile(r'validate_f35sbxb2_cierre_formal: (\d+) comprobaciones correctas, (\d+) fallas')
R2A_INFO = {
    'ANC': re.compile(r'INFO ANC: anclas registradas ((?:[0-9a-f]{12}, )*[0-9a-f]{12}); ancla aprobada del cierre de '
                      r'gobierno ([0-9a-f]{40}); integración ([0-9a-f]{40}); HEAD ([0-9a-f]{40})'),
    'MAT': re.compile(r'INFO MAT: gate de B2 sobre HEAD: código (\d+); (\d+) correctas, (\d+) fallas; reglas en falla: '
                      r'([^;]*); casos en falla: ([^;]*); SCP: (\d+) violaciones \(previstas (\d+)\)'),
    'SUC': re.compile(r'INFO SUC: B2-SUCCESSOR-FREEZE sobre HEAD: código (\d+); (\d+) correctas, (\d+) fallas; reglas en '
                      r'falla: ([^;]*); gate sucesor en falla: ([^;]*); ancla derivada ([0-9a-f]{40}|ninguno)'),
    'GCL': re.compile(r'INFO GCL: B2-GOVERNMENT-CLOSURE sobre HEAD: código (\d+); (\d+) correctas, (\d+) fallas; reglas '
                      r'en falla: ([^;]*); previstas: ([^;]*)'),
    'HIS': re.compile(r'INFO HIS: B2-GOVERNMENT-CLOSURE anclado sobre ([0-9a-f]{40}): código (\d+); (\d+) correctas, '
                      r'(\d+) fallas; ancla derivada ([0-9a-f]{40}|ninguno); transición derivada ([0-9a-f]{40}|ninguna)'),
    'GOV': re.compile(r'INFO GOV: transición del cierre formal derivada: ([0-9a-f]{40}|ninguna); registrada: '
                      r'([0-9a-f]{40}|ninguna)'),
    'FRZ': re.compile(r'INFO FRZ: commit que completa la capa: ([0-9a-f]{40}|ninguno)')}
R2A_TOTAL = 14
B2_TOTAL = 119
SF_TOTAL = 12
GC_TOTAL = 13
R2A_CLASS_A = frozenset({'CTX', 'GCL', 'MAT', 'GOV', 'SEM', 'ALC'})
R2A_RULE3 = re.compile(r"([0-9a-f]{12}): regla 3: descendiente de la transición del cierre formal sin su blob: "
                       r"\[(?:'CLAUDE\.md'|'docs/PROGRESS\.md'|'CLAUDE\.md', 'docs/PROGRESS\.md')\]")
R2A_MORE = re.compile(r'… y (\d+) commits más con un blob de gobierno no admitido')
R2A_EFFECTIVE = frozenset(f'{p}: {text}' for p in GOV_PATHS for text in (
    'árbol de HEAD distinto del blob del cierre formal', 'índice distinto del blob del cierre formal o en conflicto',
    'disco distinto del blob del cierre formal, enlace o ausente'))
R2A_SEM = frozenset([f'{p}: el estado vigente no declara a B2 CERRADA, CONGELADA E INTEGRADA' for p in GOV_PATHS] +
                    ['docs/PROGRESS.md: la cabecera no declara a B2 CERRADA E INTEGRADA'])
B2_DEP_ITEM = f'{PIPELINE}: código fuera de B2 que usa el almacén o sus nombres internos'


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


def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')


def sha(obj):
    return hashlib.sha256(canon(obj)).hexdigest()


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


def untracked_all():
    """Todo archivo sin seguimiento del árbol de trabajo, ignorado o no: lo que una ejecución podría haber escrito."""
    return sorted(x for x in git('ls-files', '--others', '-z').decode('utf-8').split('\x00') if x)


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
    path = os.path.join(base, f'f35sbxb3-{label}-{os.getpid()}-{_COUNTER[0]}')
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
    directamente y del más lejano al más cercano. Git no sigue más de cinco niveles de alternates y los gates anclados
    anidan sus propios clones compartidos: así el clon no añade un nivel y lo que se ejecuta dentro no depende de lo
    anidado que esté este repositorio."""
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


def load_verified(objs, commit, rel, name):
    """Un gate congelado desde los bytes de su blob en su ancla, verificado al leerlo; nunca desde el disco. Es la
    única ejecución dinámica de este gate: el de B1 (piezas de SEM) y el de R2-A (su lógica, para predecir su salida
    sobre HEAD)."""
    data = blob_at(objs, commit, rel)
    path = os.path.join(ROOT, *rel.split('/'))
    module = types.ModuleType(name)
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
    common = git('rev-parse', '--path-format=absolute', '--git-common-dir').decode('utf-8').strip()
    depth = alternates_depth(os.path.join(common, 'objects'))
    if depth > MAX_ALTERNATES:
        out.append(f'repositorio a {depth} niveles de clones compartidos: los gates anclados anidados superarían el '
                   f'límite de alternates de Git (se admiten {MAX_ALTERNATES})')
    head = git('rev-parse', '--verify', '-q', 'HEAD^{commit}').decode('ascii').strip()
    if not is_oid(head):
        raise GitError('HEAD no es un commit')
    return out, head, shallow


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


def gov_entries(objs, commit):
    root = commit_parts(objs, commit)[0]
    return {p: entry(objs, root, p) for p in GOV_PATHS}


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
        if gov_entries(objs, commit) != {p: ('100644', 'blob', b) for p, b in blobs.items()}:
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


# ---------------------------------------------------------------- GOV: cinco etapas, transición única y monotónica
def governance(objs):
    """Entradas de cada etapa: las cuatro registradas en sus commits y 'b3', con el delta aplicado al blob del cierre
    formal; el resultado debe ser el blob registrado de B3."""
    want = {stage: gov_entries(objs, GOV_BLOBS[stage][0]) for stage in STAGES[:4]}
    b3 = {}
    for path in GOV_PATHS:
        text = blob_text(objs, want['formal'][path]).decode('utf-8')
        blocks = B3_DELTA.get(path) or []
        if not blocks or any(text.count(before) != 1 for before, _ in blocks):
            raise ValueError(f'{path}: delta de B3 vacío o con un bloque antiguo que no aparece exactamente una vez')
        for before, after in blocks:
            text = text.replace(before, after, 1)
        b3[path] = ('100644', 'blob', blob_id(text.encode('utf-8')))
    if b3 != {p: ('100644', 'blob', b) for p, b in GOV_BLOBS['b3'][1].items()}:
        raise ValueError('el delta de B3 aplicado al blob del cierre formal no da el blob registrado de B3')
    want['b3'] = b3
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


def gov_problems(objs, parents, head, notes):
    want = governance(objs)
    graph = descendants(parents, B1_ANCHOR)
    order = [c for c in topological(parents) if c in graph]          # de los más antiguos a los más recientes
    out = []
    for stage, label in (('b2', 'de B2'), ('cierre', 'del cierre de gobierno'), ('formal', 'del cierre formal')):
        commit = GOV_BLOBS[stage][0]
        found = introduced(objs, parents, order, want, stage)
        if commit in parents and found != {commit: set(GOV_PATHS)}:
            out.append(f'regla 4: el blob {label} se introduce fuera de {commit[:12]}: '
                       f'{sorted(c[:12] for c in found if c != commit)[:3]}')
    b3 = introduced(objs, parents, order, want, 'b3')
    full = [c for c, paths in b3.items() if paths == set(GOV_PATHS)]
    transition = full[0] if len(full) == 1 else None
    notes['transition'] = transition
    others = sorted(c[:12] for c in b3 if c != transition)
    if others:
        out.append(f'regla 4: introducción del blob de B3 fuera de una transición única en las dos rutas: {others[:3]}')
    if transition is None:
        out.append('transición de B3 no materializada en un único commit que cambie las dos rutas a la vez')
    else:
        ps = parents[transition]
        if len(ps) != 1:
            out.append(f'regla 2: la transición de B3 {transition[:12]} no tiene un solo padre')
        else:
            if gov_entries(objs, ps[0]) != want['formal']:
                out.append(f'regla 2: el padre de la transición {transition[:12]} no tiene el blob del cierre formal')
            changed = set(name_status(git('diff-tree', '-r', '--no-renames', '--name-status', '-z', ps[0], transition)))
            if changed != set(GOV_PATHS):
                out.append(f'regla 2: la transición {transition[:12]} cambia otras rutas además del gobierno: '
                           f'{sorted(changed ^ set(GOV_PATHS))[:3]}')
        if BASE not in ancestry(objs, transition):
            out.append(f'la transición {transition[:12]} no desciende del merge de integración {BASE[:12]}')
    if transition != B3_TRANSITION:
        out.append(f'transición derivada ({transition[:12] if transition else "ninguna"}) distinta de la registrada '
                   f'({B3_TRANSITION[:12]})')
    after = {stage: (descendants(parents, GOV_BLOBS[stage][0]) | {GOV_BLOBS[stage][0]})
             if GOV_BLOBS[stage][0] in parents else set() for stage in ('b2', 'cierre', 'formal')}
    after['b3'] = (descendants(parents, transition) | {transition}) if transition else set()
    rules = {'b3': 'regla 3: descendiente de la transición de B3 sin su blob',
             'formal': 'regla 3: descendiente de la transición del cierre formal sin su blob',
             'cierre': 'regla 3: descendiente de la transición del cierre de gobierno sin su blob',
             'b2': 'regla 3: descendiente de la transición de B2 sin su blob',
             'b1': 'regla 1: commit previo a la transición de B2 sin el blob de B1'}
    bad = []
    for commit in order:
        stage = next((s for s in ('b3', 'formal', 'cierre', 'b2') if commit in after[s]), 'b1')
        diff = [p for p, e in gov_entries(objs, commit).items() if e != want[stage][p]]
        if diff:
            bad.append(f'{commit[:12]}: {rules[stage]}: {diff}')
    out += bad[:3] + ([f'… y {len(bad) - 3} commits más con un blob de gobierno no admitido'] if len(bad) > 3 else [])
    out += effective_problems(objs, head, want['b3'], ('árbol de HEAD distinto del blob de B3',
                                                       'índice distinto del blob de B3 o en conflicto',
                                                       'disco distinto del blob de B3, enlace o ausente'))
    return out


# ---------------------------------------------------------------- SEM: semántica con piezas verificadas del gate de B1
def b3_lifecycle(b1, text):
    """B3 en un estado distinto de implementada: cerrada, congelada, integrada, aprobada, productiva, publicada,
    desplegada o reabierta, salvo negada."""
    out = []
    for body in b1.sentences(text, cite=True):
        for m in B3_FORBIDDEN_RX.finditer(body):
            if any(t in b1.NEG_WORDS or t.startswith(b1.NEG_PREFIXES) for t in m.group(1).split()):
                continue
            if b1.DECL_NEG_RX.search(re.split(r'[.,;:!?|]', body[:m.start()])[-1]):
                continue
            out.append(f'«{" ".join(m.group(0).split())}»')
    return out


def sem_problems(objs, head, b1, r2a):
    sem = r2a.semantics(b1, r2a.B2_ALLOWED)                # B2 cerrada es su estado registrado
    root = commit_parts(objs, head)[0]
    formal_root = commit_parts(objs, FORMAL_TRANSITION)[0]
    out = []
    for path in GOV_PATHS:
        text = blob_text(objs, entry(objs, root, path)).decode('utf-8')
        old = blob_text(objs, entry(objs, formal_root, path)).decode('utf-8')
        sections, header = r2a.gov_sections(text)
        if len(sections) != 1:
            out.append(f'{path}: se exige una única sección «Estado vigente F34E»')
            continue
        section = sections[0]
        if [ln for ln in section.splitlines() if re.match(r'^- [^=\n]+ = ', ln)] != b1.STATES:
            out.append(f'{path}: los trece estados de gobierno no son exactamente los vigentes')
        b_states = {' '.join(m.split()) for m in b1.B_STATE_RX.findall(section + '\n' + header)}
        if b_states != {'INICIADA'}:
            out.append(f'{path}: F35-SBX-B debe figurar solo INICIADA en el estado vigente: {sorted(b_states)}')
        if not all(fragment in section for fragment in B3_SECTION):
            out.append(f'{path}: el estado vigente no declara a B3 IMPLEMENTADA sobre B2 CERRADA, CONGELADA E '
                       f'INTEGRADA')
        if path == 'docs/PROGRESS.md' and B3_HEADER not in header:
            out.append(f'{path}: la cabecera no declara a B3 IMPLEMENTADA')
        if NO_PIPELINE in section or NO_PIPELINE in header:
            out.append(f'{path}: el estado vigente aún declara a B2 «{NO_PIPELINE}»')
        if PENDING in section or PENDING in header:
            out.append(f'{path}: el estado vigente aún declara a B2 {PENDING}')
        before = set(old.splitlines())
        added = '\n'.join(ln for ln in text.splitlines() if ln not in before)
        current = section + '\n' + header + '\n' + added
        reopen = r2a.reopening(b1, section + '\n' + header)
        if reopen:
            out.append(f'{path}: reapertura o estado de B2 distinto del cierre: {reopen[:3]}')
        b3 = b3_lifecycle(b1, current)
        if b3:
            out.append(f'{path}: B3 en un estado distinto de IMPLEMENTADA: {b3[:3]}')
        bad = r2a.contradictions(b1, sem, current, r2a.B2_FORBIDDEN_RX)
        if bad:
            out.append(f'{path}: declaraciones de estado contradictorias con el gobierno vigente: {bad[:3]}')
        claims = b1.positive_claims(added)
        if claims:
            out.append(f'{path}: líneas nuevas que afirman habilitar una capacidad prohibida: {claims[:2]}')
    out += r2a.layer_doc_problems(objs, root, b1, sem, r2a.B2_FORBIDDEN_RX, (DOC,))
    doc = entry(objs, root, DOC)
    if doc is not None:
        b3 = b3_lifecycle(b1, blob_text(objs, doc).decode('utf-8'))
        if b3:
            out.append(f'{DOC}: B3 en un estado distinto de IMPLEMENTADA: {b3[:3]}')
    return out


# ---------------------------------------------------------------- MAT: el gate de B2 sobre HEAD, con su clase A
def mat_problems(objs, parents, head, branch, gate_blob, r2a):
    """El gate de B2 con su clase A de B3: la de R2-A con las cinco rutas de esta capa en SCP, CTX solo en esta rama y
    DEP con una sola violación, la del pipeline."""
    try:
        code, stdout, stderr = run_script(B2_GATE, gate_blob, ROOT)
    except ValueError as e:
        return [str(e)], f'INFO MAT: gate de B2 sobre HEAD no ejecutado: {e}', None
    observed = (code, *parse_output(code, stdout, stderr, B2_SUMMARY, {'TRN': B2_INFO}))
    expected, cases, content = r2a.predicted_b2(objs, parents, head, branch,
                                                r2a.GC_LAYER_FILES + r2a.LAYER_FILES + LAYER_FILES,
                                                r2a.B2_LIFECYCLE_ITEMS, BRANCH)
    expected['DEP'] = (1, lambda x: x == B2_DEP_ITEM)
    return r2a.b2_problems(observed, expected, cases, content), \
        r2a.mat_line(observed, expected['SCP'][0], 'previstas'), observed


# ---------------------------------------------------------------- HIS y R2A: el gate de R2-A, anclado y sobre HEAD
def r2a_blob(objs):
    found = entry(objs, commit_parts(objs, R2A_COMPLETION)[0], R2A_GATE)
    if found is None or found[:2] != ('100644', 'blob'):
        raise GitError('el gate de R2-A no es un blob regular en su ancla')
    return found[2]


def his_problems(code, stdout, stderr):
    ok, ko, rules, cases, info = parse_output(code, stdout, stderr, R2A_SUMMARY, R2A_INFO)
    out = []
    if code != 0 or ko or rules or cases or ok != R2A_TOTAL:
        first = next((items[0] for _, (_, items) in sorted(rules.items()) if items), '')
        out.append(f'el gate de R2-A anclado sobre {R2A_COMPLETION[:12]} no da {R2A_TOTAL}/0: {sorted(rules)}'
                   + (f'; {first[:160]}' if first else ''))
    if info['FRZ'].group(1) != R2A_COMPLETION:
        out.append(f'ancla derivada {info["FRZ"].group(1)[:12]} distinta de la aprobada {R2A_COMPLETION[:12]}')
    if info['GOV'].groups() != (FORMAL_TRANSITION, FORMAL_TRANSITION):
        out.append(f'transición del cierre formal derivada o registrada distinta de {FORMAL_TRANSITION[:12]}')
    if info['ANC'].group(3) != DEVELOP_GOV_MERGE or info['ANC'].group(4) != R2A_COMPLETION:
        out.append('el gate de R2-A anclado no informa su integración y su ancla como HEAD')
    if info['HIS'].groups() != (GOV_CLOSURE, '0', str(GC_TOTAL), '0', GOV_CLOSURE, CLOSURE_TRANSITION):
        out.append('el gate de R2-A anclado no acredita el cierre de gobierno en 13/0 con su ancla y su transición')
    if info['GCL'].group(4) != info['GCL'].group(5):
        out.append('el gate de R2-A anclado no acredita que el cierre de gobierno falle solo en lo previsto')
    line = (f'INFO HIS: R2-A anclado sobre {R2A_COMPLETION}: código {code}; {ok} correctas, {ko} fallas; ancla '
            f'derivada {info["FRZ"].group(1)}; transición derivada {info["GOV"].group(1)}')
    return out, line


def gcl_notes(r2a, objs, parents, head, branch, b1, mat_obs):
    """Las notas que el gate de R2-A da en GCL sobre este HEAD: gcl_expected de R2-A sin la parte de SUC. Que esa
    parte no dé nota lo garantiza su SUC en verde, que la clasificación exige: el ALC de B2-SUCCESSOR-FREEZE nombra
    siempre la capa de R2-A, ajena al alcance del cierre de gobierno."""
    notes = []
    gc_ctx = ([f'rama no permitida o HEAD separado: «{branch or "HEAD separado"}»'] if branch not in r2a.GC_BRANCHES
              else []) + ([f'el merge de integración {r2a.DEVELOP_MERGE[:12]} no es ancestro de HEAD']
                          if r2a.DEVELOP_MERGE not in parents else [])
    if gc_ctx != ([f'rama no permitida o HEAD separado: «{r2a.BRANCH}»'] if branch == r2a.BRANCH else []):
        notes.append(f'CTX del cierre de gobierno no se explica solo por la rama de este incremento: {gc_ctx[:2]}')
    gc_view = r2a.predicted_b2(objs, parents, head, branch, r2a.GC_LAYER_FILES, r2a.GC_LIFECYCLE_ITEMS, r2a.GC_BRANCH)
    scp_n = mat_obs[3].get('SCP', (0,))[0]
    own_scp = 3 * (11 + len(r2a.GC_LAYER_FILES) + len(r2a.LAYER_FILES))
    for item in r2a.b2_problems(mat_obs, *gc_view):
        if item == r2a.GC_MATERIAL_CTX and branch == r2a.BRANCH:
            continue
        if item.startswith(r2a.GC_SCP_PREFIX) and scp_n == own_scp:
            continue
        if item.startswith(r2a.GC_GOV_PREFIX) and r2a.closure_lifecycle(
                ast.literal_eval(item[len(r2a.GC_GOV_PREFIX):]), gc_view[2]):
            continue
        notes.append(f'MAT del cierre de gobierno no se explica solo por este incremento: {item[:120]}')
    if r2a.gc_gov_mirror(objs, parents, head)[1]:
        notes.append('GOV del cierre de gobierno informa algo más que la transición del cierre formal')
    for item in r2a.gc_sem_mirror(objs, head, b1):
        m = re.fullmatch(r'(CLAUDE\.md|docs/PROGRESS\.md): declaraciones de estado contradictorias con el gobierno '
                         r'vigente: (\[.*\])', item)
        if item in (f'{p}: el estado vigente no declara a B2 {r2a.PENDING}' for p in GOV_PATHS):
            continue
        if m and set(ast.literal_eval(m.group(2))) <= r2a.GC_CLOSED_ITEMS:
            continue
        notes.append(f'SEM del cierre de gobierno no se explica solo por el cierre formal: {item[:120]}')
    alc = r2a.gc_alc_mirror(objs, head)
    own = sorted((p, 'A') for p in r2a.LAYER_FILES)[:3]
    if alc != [f'{plane}: alcance distinto del enumerado para este incremento: {own}' for plane in PLANES]:
        notes.append(f'ALC del cierre de gobierno no se explica solo por las rutas de esta capa: {alc[:2]}')
    return notes


def r2a_expected(r2a, objs, parents, head, branch, b1, mat_obs):
    """La salida del gate de R2-A sobre este HEAD, con su propia lógica (cargada de su blob verificado): {regla:
    violaciones} de sus reglas de clase A posibles. Las demás (ENT, ANC, HIS, SUC, INT, FLG, FRZ y DEP) tienen que pasar."""
    expected = {'CTX': r2a.ctx_problems(branch, parents),
                'GCL': gcl_notes(r2a, objs, parents, head, branch, b1, mat_obs),
                'MAT': r2a.b2_problems(mat_obs, *r2a.predicted_b2(objs, parents, head, branch,
                                                                   r2a.GC_LAYER_FILES + r2a.LAYER_FILES,
                                                                   r2a.B2_LIFECYCLE_ITEMS, r2a.BRANCH)),
                'GOV': r2a.gov_problems(objs, parents, head, {}),
                'SEM': r2a.sem_problems(objs, head, b1),
                'ALC': r2a.alc_problems(objs, head)}
    return {rid: items for rid, items in expected.items() if items}


def scope_delta(base, scope):
    """Por plano, la diferencia simétrica entre el alcance observado frente a base y el enumerado."""
    out = {}
    for plane, args in (('HEAD', ('diff', '--name-status', '--no-renames', '-z', base, 'HEAD')),
                        ('árbol', ('diff', '--name-status', '--no-renames', '-z', base)),
                        ('índice', ('diff', '--cached', '--name-status', '--no-renames', '-z', base))):
        out[plane] = set(name_status(git(*args)).items()) ^ set(scope.items())
    return out


def r2a_foreign(r2a, objs, parents, branch, expected, mat_obs):
    """Lo que, en la salida prevista del gate de R2-A, no es la clase A de B3 (§4.13)."""
    out = []
    own = set(parents) - set(ancestry(objs, BASE))       # commits de B3: fuera de la historia de la base
    layer = {(p, 'A') for p in LAYER_FILES}
    if set(expected) - R2A_CLASS_A:
        out.append(f'reglas ajenas a la clase A de B3: {sorted(set(expected) - R2A_CLASS_A)}')
    if expected.get('CTX', []) != ([f'rama no permitida o HEAD separado: «{BRANCH}»'] if branch == BRANCH else []):
        out.append(f'CTX distinto de la rama de B3: {expected.get("CTX", [])[:2]}')
    material = sorted({'DEP'} | ({'CTX'} if branch == BRANCH else set()))
    scp_n, scp_items = mat_obs[3].get('SCP', (0, []))
    allowed_scp = 3 * (11 + len(r2a.GC_LAYER_FILES) + len(r2a.LAYER_FILES))
    mat_items = [f'el gate de B2 sobre HEAD incumple comprobaciones materiales: reglas {material}',
                 f'SCP del gate de B2 con {scp_n} violaciones, no las {allowed_scp} que predice el estado: '
                 f'{scp_items[:2]}']
    if expected.get('MAT') != mat_items or scp_n != allowed_scp + 3 * len(LAYER_FILES):
        out.append(f'MAT no se explica solo por DEP del pipeline y las rutas de B3 en SCP: {expected.get("MAT", [])[:2]}')
    formal = gov_entries(objs, FORMAL_TRANSITION)
    later = descendants(parents, FORMAL_TRANSITION)
    hidden = [c for c in topological(parents) if c in later and gov_entries(objs, c) != formal and c not in own]
    for item in expected.get('GOV', []):
        m = R2A_RULE3.fullmatch(item)
        if not ((m and any(c.startswith(m.group(1)) for c in own)) or R2A_MORE.fullmatch(item) or item in R2A_EFFECTIVE):
            out.append(f'GOV ajeno a la regla 3 en los commits de B3 y al estado efectivo: {item[:120]}')
    if hidden:
        out.append(f'GOV con commits sin el blob del cierre formal fuera de B3: {[c[:12] for c in hidden[:3]]}')
    if not set(expected.get('SEM', [])) <= R2A_SEM:
        out.append(f'SEM ajeno a la declaración de B3 sobre el cierre de B2: {sorted(set(expected["SEM"]) - R2A_SEM)[:2]}')
    alc = scope_delta(DEVELOP_GOV_MERGE, r2a.SCOPE)
    if len(expected.get('ALC', [])) != len(PLANES) or any(alc[plane] != layer for plane in PLANES):
        out.append('ALC no se explica solo por las rutas de B3 en los tres planos')
    gc_alc = scope_delta(r2a.DEVELOP_MERGE, r2a.GC_SCOPE)
    gc_layer = layer | {(p, 'A') for p in r2a.LAYER_FILES}
    allowed_notes = set()
    if branch == BRANCH:
        allowed_notes.add('CTX del cierre de gobierno no se explica solo por la rama de este incremento: '
                          f"['rama no permitida o HEAD separado: «{BRANCH}»']")
    gc_scp = 3 * (11 + len(r2a.GC_LAYER_FILES))
    allowed_notes |= {f'MAT del cierre de gobierno no se explica solo por este incremento: {x[:120]}' for x in (
        f'el gate de B2 sobre HEAD incumple comprobaciones materiales: reglas {material}',
        f'SCP del gate de B2 con {scp_n} violaciones, no las {gc_scp} que predice el estado: {scp_items[:2]}')}
    notes = expected.get('GCL', [])
    alc_notes = [x for x in notes if x.startswith('ALC del cierre de gobierno no se explica solo por las rutas de esta '
                                                    'capa: ')]
    if not set(notes) - set(alc_notes) <= allowed_notes or len(alc_notes) > 1 or \
            (alc_notes and any(gc_alc[plane] != gc_layer for plane in PLANES)):
        out.append(f'GCL con notas ajenas a la clase A de B3: {sorted(set(notes) - allowed_notes)[:2]}')
    return out


def r2a_problems(observed, r2a, objs, parents, head, branch, b1, mat_obs):
    code, out_bytes, err_bytes = observed
    ok, ko, rules, cases, info = parse_output(code, out_bytes, err_bytes, R2A_SUMMARY, R2A_INFO)
    expected = r2a_expected(r2a, objs, parents, head, branch, b1, mat_obs)
    out = r2a_foreign(r2a, objs, parents, branch, expected, mat_obs)
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


# ---------------------------------------------------------------- ALC, FRZ y DEP
def alc_problems(objs, head):
    out = []
    for plane, delta in scope_delta(BASE, SCOPE).items():
        if delta:
            out.append(f'{plane}: alcance distinto del enumerado para B3: {sorted(delta)[:3]}')
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


def store_name():
    """Módulo del almacén de B2, derivado de Git: el único .py de su carpeta que no es su gate."""
    names = [x for x in git('ls-tree', '--name-only', '-z', 'HEAD', B2_TOOLS + '/').decode('utf-8').split('\x00') if x]
    stores = [x for x in names if x.endswith('.py') and x != B2_GATE]
    if len(names) != 2 or len(stores) != 1:
        raise GitError(f'la carpeta de herramientas de B2 no tiene la forma auditada: {names}')
    return stores[0]


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
    store = store_name()
    name = store.rsplit('/', 1)[1][:-3].encode('utf-8')
    tracked = [x for x in git('ls-files', '-z').decode('utf-8').split('\x00') if x.endswith('.py')]
    for p in tracked:
        if p not in (store, B2_GATE, PIPELINE) and name in (disk_bytes(p) or b''):
            out.append(f'{p}: código fuera del pipeline y de B2 que nombra el almacén')
    return out


# ---------------------------------------------------------------- PIP, DET, CNF, PUR, TSB y FAL: el pipeline
def no_duplicates(pairs):
    keys = [k for k, _ in pairs]
    if len(keys) != len(set(keys)):
        raise ValueError('clave duplicada')
    return dict(pairs)


def sandbox_env(sandbox):
    """Entorno del pipeline y de sus pruebas: sin variables de Git y con un temporal propio, nuevo y vacío, que tiene
    que seguir vacío al terminar (TSBB-08)."""
    return dict(GIT_ENV, TEMP=sandbox, TMP=sandbox, TMPDIR=sandbox)


def run_pipeline(env, *args):
    path = disk_path(PIPELINE)
    if path is None or not os.path.isfile(path):
        raise ValueError('pipeline ausente o enlace')
    p = subprocess.run([sys.executable, '-I', '-B', path, *args], cwd=ROOT, env=env, capture_output=True,
                       timeout=TIMEOUT)
    return p.returncode, p.stdout, p.stderr


def parse_report(raw):
    """Informe canónico: JSON UTF-8 sin claves duplicadas, exactamente en su forma canónica y con LF final."""
    try:
        report = json.loads(raw.decode('utf-8'), object_pairs_hook=no_duplicates)
    except (UnicodeDecodeError, ValueError):
        return None, ['salida que no es un informe JSON legible']
    if raw != canon(report) + b'\n':
        return report, ['informe que no está en su forma canónica con LF final']
    return report, []


class Reference:
    """Entradas verificadas desde objetos Git: contrato y fixtures de A en su ancla E, dataset F34 y almacén de B2."""

    def __init__(self, objs):
        manifest_raw = blob_at(objs, A_ANCHOR, A_MANIFEST)
        if hashlib.sha256(manifest_raw).hexdigest() != A_MANIFEST_SHA256:
            raise ValueError('manifest de A distinto del congelado en E')
        manifest = json.loads(manifest_raw.decode('utf-8'), object_pairs_hook=no_duplicates)
        self.fixtures, fixture_sha = {}, {}
        for org in TENANTS:
            raw = blob_at(objs, A_ANCHOR, A_DIR + f'fixtures/{org}_evidencias.json')
            want = manifest['files'][f'fixtures/{org}_evidencias.json']
            if hashlib.sha256(raw).hexdigest() != want['sha256'] or len(raw) != want['bytes']:
                raise ValueError(f'fixture de {org} distinto de su manifest')
            self.fixtures[org], fixture_sha[org] = json.loads(raw.decode('utf-8'), object_pairs_hook=no_duplicates), \
                want['sha256']
        contract_raw = blob_at(objs, A_ANCHOR, A_CONTRACT)
        if hashlib.sha256(contract_raw).hexdigest() != manifest['files']['contrato/f35sbx_contract.json']['sha256']:
            raise ValueError('contrato de A distinto de su manifest')
        contract = json.loads(contract_raw.decode('utf-8'), object_pairs_hook=no_duplicates)
        self.columns = {table: set(contract['$defs'][name]['properties']) for table, name in ENTITIES.items()}
        f34m_raw = blob_at(objs, BASE, F34_DIR + 'manifest.json')
        if hashlib.sha256(f34m_raw).hexdigest() != F34_MANIFEST_SHA256 or \
                manifest['f34']['manifest_sha256'] != F34_MANIFEST_SHA256:
            raise ValueError('manifest F34 distinto del registrado por A')
        f34m = json.loads(f34m_raw.decode('utf-8'), object_pairs_hook=no_duplicates)
        tables, files = {}, {}
        for name in F34_FILES:
            raw = blob_at(objs, BASE, F34_DIR + name)
            files[name] = hashlib.sha256(raw).hexdigest()
            if files[name] != f34m['files'][name]['sha256']:
                raise ValueError(f'{name} distinto de su manifest F34')
            tables[name] = list(csv.DictReader(re.split(r'(?<=\n)', raw.decode('utf-8'))))
        apps = {r['application_token']: r['organization_token'] for r in tables['applications.csv']}
        vacs = {r['vacancy_token']: r['organization_token'] for r in tables['vacancies.csv']}
        self.criteria_org = {r['criterion_id']: vacs[r['vacancy_token']] for r in tables['criteria.csv']}
        self.evidence = {r['synthetic_record_id']: dict(r, organization=apps[r['application_token']])
                         for r in tables['evidence.csv']}
        self.evidence_sha = files['evidence.csv']
        store_raw = blob_at(objs, CANDIDATE, store_name())
        self.inputs = {'dataset_version': DATASET_VERSION, 'f34_manifest_sha256': F34_MANIFEST_SHA256,
                       'f34_files_sha256': files, 'sbx_manifest_sha256': A_MANIFEST_SHA256,
                       'sbx_contract_sha256': hashlib.sha256(contract_raw).hexdigest(),
                       'store_sha256': hashlib.sha256(store_raw).hexdigest(), 'fixtures_sha256': fixture_sha}

    def selection(self, org):
        """Regla de selección de A: las dos primeras filas F34 vinculadas, sintéticas y de un tipo admitido de la
        organización, por evidence_id."""
        rows = sorted((r for r in self.evidence.values() if r['organization'] == org and r['state'] == 'vinculada' and
                       r['source_type'] == 'synthetic' and r['source_type_ev'] in EVIDENCE_KINDS),
                      key=lambda r: r['evidence_id'])
        return [r['synthetic_record_id'] for r in rows[:2]]


def t1(text):
    return ' '.join(unicodedata.normalize('NFC', text).split())


def content_hash(org, origin, criterion, kind, text):
    return sha({'algorithm': HASH_ALGORITHM, 'synthetic_organization_id': org, 'origin_record_id': origin,
                'criterion_ref': criterion, 'evidence_kind': kind, 'text': text})


def report_problems(report, ref):
    """Esquema cerrado del informe (§4.5), con sus entradas verificadas: ningún campo ajeno, como un puntaje."""
    out = []
    if type(report) is not dict:
        return ['informe ilegible']
    result = report.get('result')
    want = REPORT_KEYS | ({'runs'} if result == 'completado' else {'failure'} if result == 'fallido' else set())
    if set(report) != want:
        out.append(f'claves del informe distintas del esquema cerrado: {sorted(set(report) ^ want)[:5]}')
    if {k: report.get(k) for k in HEADER} != HEADER:
        out.append('cabecera del informe distinta de la del almacén de B2')
    if report.get('inputs') != ref.inputs:
        out.append('entradas del informe distintas de las verificadas')
    if result != 'completado':
        return out + [f'resultado {result!r}, no completado']
    runs = report.get('runs')
    if type(runs) is not list or [r.get('synthetic_organization_id') if type(r) is dict else None for r in runs] != \
            list(TENANTS):
        return out + ['runs distintos de los tres tenants, en orden']
    for r in runs:
        org = r['synthetic_organization_id']
        if set(r) != RUN_KEYS:
            out.append(f'{org}: claves del run distintas del esquema cerrado: {sorted(set(r) ^ RUN_KEYS)[:5]}')
            continue
        if r['final_state'] != 'completado' or r['post_purge'] != 'E-PURGADO' or \
                r['conformity'] != {'level1': 'conforme', 'level2': 'integra'}:
            out.append(f'{org}: run no completado, sin purga verificada o no conforme')
        steps = r['steps']
        if type(steps) is not list or [(s.get('step'), s.get('name'), s.get('result')) if type(s) is dict and
                                       set(s) == {'step', 'name', 'result', 'at'} else None for s in steps] != \
                [(k, STEP_NAMES[k], 'ok') for k in range(1, 13)]:
            out.append(f'{org}: pasos distintos de los doce del contrato')
        elif any(type(s['at']) is not str or not TS_RX.fullmatch(s['at']) for s in steps) or \
                [s['at'] for s in steps] != sorted(s['at'] for s in steps):
            out.append(f'{org}: instantes de los pasos no monótonos o fuera del formato')
        tables = r['tables']
        if type(tables) is not dict or set(tables) != set(ENTITIES) or type(r['counts']) is not dict or \
                set(r['counts']) != set(ENTITIES) or any(type(v) is not int for v in r['counts'].values()):
            out.append(f'{org}: tablas o conteos distintos de las ocho del almacén')
        elif any(type(rows) is not list or any(type(row) is not dict or set(row) != ref.columns[t] for row in rows)
                 for t, rows in tables.items()):
            out.append(f'{org}: filas con campos distintos de los del contrato de A')
        if type(r['receipt']) is not dict or set(r['receipt']) != RECEIPT_KEYS:
            out.append(f'{org}: comprobante con campos distintos de los del almacén')
        if type(r['seed']) is not int or type(r['clock_start']) is not str or not TS_RX.fullmatch(r['clock_start']):
            out.append(f'{org}: escenario ilegible')
    return out


def chain_problems(items, key, prev_key, label):
    prev, out = GENESIS, []
    for item in items:
        if item.get(prev_key) != prev:
            out.append(f'{label}: eslabón roto')
        if item.get(key) != sha({k: v for k, v in item.items() if k != key}):
            out.append(f'{label}: hash recalculado distinto')
        prev = item.get(key)
    return out


def level1(run, fixture, ref, org):
    """Nivel 1 (B0 §5.2), calculado aquí: proyección semántica A↔B emparejada por clave natural (organización, fila
    F34), escenario del oráculo y evidencia recalculada desde su fila F34."""
    t, out = run['tables'], []
    if run['synthetic_organization_id'] != org or (run['seed'], run['clock_start']) != \
            (fixture['run']['seed'], fixture['run']['clock_start']):
        out.append(f'{org}: tenant o escenario distintos del oráculo')
    if [(e['state'], e['error_code']) for e in t['pipeline_event']] != \
            [(e['state'], e['error_code']) for e in fixture['events']] or \
            [e['state'] for e in t['pipeline_event']] != PATH:
        out.append(f'{org}: eventos distintos del camino del oráculo')
    if [e['seq'] for e in t['pipeline_event']] != list(range(1, len(t['pipeline_event']) + 1)):
        out.append(f'{org}: seq no contiguo')
    if t['tenant_context'] != [fixture['tenant']]:
        out.append(f'{org}: contexto del tenant distinto del del oráculo')
    if [a['action'] for a in t['audit_entry']] != [a['action'] for a in fixture['audit']] or \
            [a['action'] for a in t['audit_entry']] != ACTIONS:
        out.append(f'{org}: acciones de auditoría distintas del oráculo')
    a_src = {s['source_id']: s for s in fixture['sources']}
    b_src = {s['source_id']: s for s in t['evidence_source']}
    a_rec = {(r['synthetic_organization_id'], a_src[r['source_id']]['origin_record_id']): r for r in fixture['records']}
    b_rec = {(r['synthetic_organization_id'], b_src[r['source_id']]['origin_record_id']): r for r in t['evidence_record']}
    if set(a_rec) != set(b_rec) or len(b_rec) != len(t['evidence_record']):
        return out + [f'{org}: claves naturales distintas del oráculo']
    a_prov = {p['record_id']: p for p in fixture['provenance']}
    b_prov = {p['record_id']: p for p in t['evidence_provenance']}
    a_rev = {v['record_id']: v for v in fixture['reviews']}
    b_rev = {v['record_id']: v for v in t['simulated_review']}
    for key in sorted(a_rec):
        ra, rb = a_rec[key], b_rec[key]
        pa, pb, va, vb = a_prov[ra['synthetic_id']], b_prov[rb['synthetic_id']], a_rev[ra['synthetic_id']], \
            b_rev[rb['synthetic_id']]
        sa, sb = a_src[ra['source_id']], b_src[rb['source_id']]
        for names, x, y in ((('synthetic_organization_id', 'criterion_ref', 'evidence_kind', 'text_synthetic',
                              'hash_algorithm', 'content_hash', 'validation_status', 'review_status', 'source_type',
                              'environment'), ra, rb),
                            (('origin_dataset_version', 'origin_file', 'origin_file_sha256', 'origin_record_id',
                              'source_type', 'synthetic_organization_id'), sa, sb),
                            (('provenance_kind', 'transformation_id', 'transformation_version', 'hash_before',
                              'hash_after'), pa, pb),
                            (('review_scope', 'review_status', 'reviewer_type', 'scripted', 'simulation_actor'), va, vb)):
            bad = [f for f in names if x[f] != y[f] or type(x[f]) is not type(y[f])]
            if bad:
                out.append(f'{org}: {key[1]} con {bad[:3]} distintos del oráculo')
        if pb['source_id'] != rb['source_id'] or vb['review_id'] != pb['review_id']:
            out.append(f'{org}: {key[1]}: relación evidencia ↔ fuente ↔ revisión rota')
        row = ref.evidence.get(key[1])
        if row is None or row['organization'] != org or ref.criteria_org.get(row['criterion_id']) != org:
            out.append(f'{org}: {key[1]} no es una fila F34 de su organización')
            continue
        args = (org, key[1], row['criterion_id'], row['source_type_ev'])
        if (rb['criterion_ref'], rb['evidence_kind']) != args[2:] or rb['text_synthetic'] != t1(row['evidence_text']) \
                or pb['hash_before'] != content_hash(*args, row['evidence_text']) or \
                rb['content_hash'] != content_hash(*args, t1(row['evidence_text'])) or \
                pb['hash_after'] != rb['content_hash'] or sb['origin_file_sha256'] != ref.evidence_sha:
            out.append(f'{org}: {key[1]}: evidencia distinta de la recalculada desde su fila F34')
    order_a = [a_src[next(r for r in fixture['records'] if r['synthetic_id'] == p['record_id'])['source_id']]
               ['origin_record_id'] for p in fixture['provenance']]
    order_b = [b_src[next(r for r in t['evidence_record'] if r['synthetic_id'] == p['record_id'])['source_id']]
               ['origin_record_id'] for p in t['evidence_provenance']]
    if order_a != order_b or order_b != ref.selection(org):
        out.append(f'{org}: cadena de procedencia distinta de la selección determinista de A')
    if {k: len(v) for k, v in t.items()} != COUNTS or run['counts'] != COUNTS:
        out.append(f'{org}: conteos distintos del oráculo')
    return out


def level2(run, org):
    """Nivel 2 (B0 §5.2), calculado aquí: cadenas de B eslabón por eslabón, identificadores SBB* del espacio
    <org>-<semilla> y relaciones entre las filas."""
    t = run['tables']
    out = chain_problems(t['pipeline_event'], 'event_hash', 'prev_event_hash', f'{org}: eventos') + \
        chain_problems(t['evidence_provenance'], 'provenance_hash', 'prev_provenance_hash', f'{org}: procedencia') + \
        chain_problems(t['audit_entry'], 'audit_hash', 'prev_audit_hash', f'{org}: auditoría')
    space = f'{org}-{run["seed"]:010d}'
    run_id = f'SBBR-{space}'
    if [r['pipeline_run_id'] for r in t['pipeline_run']] != [run_id]:
        out.append(f'{org}: identificador del run fuera del espacio <org>-<semilla>')
    principal = {'pipeline_run_id': run_id, 'synthetic_organization_id': org, 'run_kind': HEADER['run_kind'],
                 'pipeline_version': HEADER['pipeline_version'], 'contract_version': HEADER['contract_version'],
                 'hash_algorithm': HASH_ALGORITHM, 'seed': run['seed'], 'clock_start': run['clock_start'],
                 'environment': 'sandbox', 'source_type': 'synthetic'}
    if t['pipeline_run'] != [principal]:
        out.append(f'{org}: principal del run distinto del de B2 para su escenario')
    for table in ('pipeline_event', 'audit_entry'):
        stamps = [r['at'] for r in t[table]]
        if stamps != sorted(stamps) or any(type(x) is not str or not TS_RX.fullmatch(x) or x < run['clock_start']
                                           for x in stamps):
            out.append(f'{org}: {table} con instantes no monótonos o anteriores al reloj lógico')
    for table, key, prefix in (('pipeline_event', 'event_id', 'SBBV'), ('audit_entry', 'audit_id', 'SBBA'),
                               ('evidence_source', 'source_id', 'SBBS'), ('evidence_record', 'synthetic_id', 'SBBE'),
                               ('evidence_provenance', 'provenance_id', 'SBBP'),
                               ('simulated_review', 'review_id', 'SBBH')):
        if any(not str(r[key]).startswith(f'{prefix}-{space}-') for r in t[table]):
            out.append(f'{org}: {table} con identificadores fuera de {prefix}-{space}')
    for table, rows in t.items():
        if any(r.get('pipeline_run_id', run_id) != run_id or r.get('synthetic_organization_id', org) != org or
               r.get('target_ref', run_id) != run_id for r in rows):
            out.append(f'{org}: {table} con filas de otro run o de otro tenant')
    records = {r['synthetic_id']: r for r in t['evidence_record']}
    sources = {s['source_id'] for s in t['evidence_source']}
    reviews = {v['record_id']: v for v in t['simulated_review']}
    for p in t['evidence_provenance']:
        r = records.get(p['record_id'])
        if r is None or r['source_id'] not in sources or p['source_id'] != r['source_id'] or \
                reviews.get(p['record_id'], {}).get('review_id') != p['review_id']:
            out.append(f'{org}: procedencia sin su evidencia, su fuente o su revisión')
    if len(records) != len(t['evidence_provenance']) or set(reviews) != set(records):
        out.append(f'{org}: evidencias sin una procedencia y una revisión cada una')
    return out


def cnf_problems(report, ref):
    if type(report) is not dict or report.get('result') != 'completado' or type(report.get('runs')) is not list or \
            len(report['runs']) != len(TENANTS):
        return ['conformidad no evaluable sin un informe completo de los tres tenants']
    out = []
    for org, run in zip(TENANTS, report['runs']):
        try:
            out += level1(run, ref.fixtures[org], ref, org) + level2(run, org)
        except (KeyError, TypeError, AttributeError, StopIteration, ValueError) as e:
            out.append(f'{org}: run no evaluable contra el oráculo ({e.__class__.__name__})')
    return out


def pur_problems(report, before, after, leftover):
    out = []
    if before != after:
        out.append(f'archivos nuevos en el árbol de trabajo tras ejecutar el pipeline: {sorted(set(after) - set(before))[:3]}')
    if leftover:
        out.append(f'el pipeline o sus pruebas dejaron archivos en su temporal exclusivo: {sorted(leftover)[:3]}')
    if type(report) is not dict or report.get('result') != 'completado' or type(report.get('runs')) is not list:
        return out + ['purga no evaluable sin un informe completo']
    for position, run in zip(TENANTS, report['runs']):
        try:
            org = run['synthetic_organization_id'] if type(run) is dict else position
            r, t = run['receipt'], run['tables']
            if set(r) != RECEIPT_KEYS:
                out.append(f'{org}: comprobante con campos distintos de los del almacén')
                continue
            want = {'closure_kind': 'purga', 'final_state': 'completado', 'failed_event': 'no_aplica',
                    'failed_event_record': 'no_aplica', 'error_code': '', 'connection': 'CLOSED',
                    'post_close_check': 'ProgrammingError', 'file_backed': False, 'synthetic_organization_id': org,
                    'pipeline_run_id': t['pipeline_run'][0]['pipeline_run_id'],
                    'counts': {k: len(v) for k, v in t.items()}, 'last_event_hash': t['pipeline_event'][-1]['event_hash']}
            bad = sorted(k for k, v in want.items() if r[k] != v or type(r[k]) is not type(v))
            if bad:
                out.append(f'{org}: comprobante distinto del de una purga completa del run: {bad[:3]}')
            if r['observed'] != {'counts': r['counts'], 'last_event_hash': r['last_event_hash'],
                                 'final_state': 'completado', 'file_backed': False}:
                out.append(f'{org}: hechos observados del comprobante distintos de los informados')
            if r['receipt_hash'] != sha({k: v for k, v in r.items() if k != 'receipt_hash'}):
                out.append(f'{org}: receipt_hash no recalculable')
            if run['post_purge'] != 'E-PURGADO' or t['pipeline_event'][-1]['state'] != 'completado':
                out.append(f'{org}: el almacén no quedó inutilizable (E-PURGADO) tras la purga de un run completado')
        except (KeyError, TypeError, IndexError, AttributeError) as e:
            out.append(f'{position}: comprobante no evaluable ({e.__class__.__name__})')
    return out


def tsb_problems(env):
    path = disk_path(PIPELINE_TESTS)
    if path is None or not os.path.isfile(path):
        return ['pruebas del pipeline ausentes o enlace']
    p = subprocess.run([sys.executable, '-I', '-B', path], cwd=ROOT, env=env, capture_output=True, timeout=TIMEOUT)
    lines = [x for x in p.stdout.decode('utf-8', 'replace').splitlines() if x.strip()]
    ids = [m.group(1) for m in map(PT_LINE.fullmatch, lines[:-1]) if m]
    if p.returncode != 0 or p.stderr.strip() or lines[-1:] != [PT_SUMMARY] or ids != PT_IDS or len(lines) != 31:
        failing = [x[:80] for x in lines if x.startswith('FALLA')]
        return [f'pruebas del pipeline no exactamente PT01..PT30 en verde (código {p.returncode}): '
                f'{failing[:3] or lines[-1:]}']
    return []


def fal_problems(ref, env):
    out = []
    for step in range(1, 13):
        first, second = run_pipeline(env, '--fallo', f'ORG-S1:{step}'), run_pipeline(env, '--fallo', f'ORG-S1:{step}')
        if first[1] != second[1]:
            out.append(f'paso {step}: dos ejecuciones con el mismo fallo dan bytes distintos')
        report, problems = parse_report(first[1])
        if first[0] != 1 or second[0] != 1 or first[2].strip() or problems:
            out.append(f'paso {step}: código {first[0]}/{second[0]}, salida de error o informe no canónico')
            continue
        if type(report) is not dict or report.get('result') != 'fallido' or set(report) != REPORT_KEYS | {'failure'} \
                or {k: report[k] for k in HEADER} != HEADER or report['inputs'] != ref.inputs or b'"tables"' in first[1]:
            out.append(f'paso {step}: informe fallido fuera del esquema o con resultado parcial')
            continue
        f = report['failure']
        if type(f) is not dict or set(f) != FAILURE_KEYS or (f['synthetic_organization_id'], f['step'], f['step_name'],
                                                             f['error_code']) != \
                ('ORG-S1', step, STEP_NAMES[step], 'E-INYECTADO'):
            out.append(f'paso {step}: falla distinta del fallo inyectado en ORG-S1 en ese paso')
            continue
        c = f['closure']
        if type(c) is not dict or set(c) != RECEIPT_KEYS or c['closure_kind'] != 'purga' or c['connection'] != 'CLOSED' \
                or c['post_close_check'] != 'ProgrammingError' or c['file_backed'] is not False or \
                c['final_state'] != ('fallido' if step <= 11 else 'completado') or \
                c['receipt_hash'] != sha({k: v for k, v in c.items() if k != 'receipt_hash'}):
            out.append(f'paso {step}: cierre del almacén distinto de la purga tras el fallo')
    return out


def pipeline_rules(viol, info, objs):
    """PIP, DET, CNF, PUR, TSB y FAL, con fallo cerrado propio de cada regla."""
    def closed(rids, why):
        for rid in rids:
            viol[rid].append(f'no evaluable: {why} (falla cerrado)')
    try:
        ref = Reference(objs)
    except ERRORS as e:
        closed(PIPE_RULES, f'entradas verificadas ({e.__class__.__name__}: {e})')
        return
    sandbox = None
    try:
        sandbox = make_temp('pipeline')
        env = sandbox_env(sandbox)
        before = untracked_all()
        code, out, err = run_pipeline(env)
    except ERRORS as e:
        closed(PIPE_RULES, f'ejecución del pipeline ({e.__class__.__name__}: {e})')
        if sandbox is not None:
            remove_tree(sandbox)
        return
    report, problems = parse_report(out)
    if code != 0 or err.strip():
        problems.append(f'código {code} o salida de error en la ejecución del pipeline')
    viol['PIP'] += problems + report_problems(report, ref)
    info.append(f'INFO PIP: informe de {len(out)} bytes, SHA-256 {hashlib.sha256(out).hexdigest()}; resultado '
                f'{report.get("result") if type(report) is dict else "ilegible"}')
    complete = code == 0 and type(report) is dict and report.get('result') == 'completado'
    try:
        if not complete:
            closed(('DET',), 'sin una ejecución completa del pipeline')
        else:
            for k in (2, 3):
                again = run_pipeline(env)
                if again != (0, out, b''):
                    viol['DET'].append(f'la ejecución {k}, en un proceso nuevo, no da los mismos bytes')
    except ERRORS as e:
        closed(('DET',), f'{e.__class__.__name__}: {e}')
    viol['CNF'] += cnf_problems(report, ref)
    for rid, fn in (('FAL', lambda: fal_problems(ref, env)), ('TSB', lambda: tsb_problems(env))):
        try:
            viol[rid] += fn()
        except ERRORS as e:
            closed((rid,), f'{e.__class__.__name__}: {e}')
    try:
        viol['PUR'] += pur_problems(report, before, untracked_all(), os.listdir(sandbox))
    except ERRORS as e:
        closed(('PUR',), f'{e.__class__.__name__}: {e}')
    finally:
        remove_tree(sandbox)


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
            closed(('CTX', 'R2A', 'MAT', 'INT', 'GOV', 'FRZ'), f'historia desde HEAD ({e.__class__.__name__}: {e})')
        if parents is not None:
            check('CTX', ctx_problems, branch, parents)
        check('ANC', anc_problems, objs)
        blob = None
        try:
            blob = r2a_blob(objs)
            background['HIS'] = Background('anclado', R2A_GATE, blob, (R2A_COMPLETION, R2A_BRANCH))
        except ERRORS as e:
            closed(('HIS',), f'ejecución anclada del gate de R2-A ({e.__class__.__name__}: {e})')
        try:
            if blob is not None:
                background['R2A'] = Background('r2a', R2A_GATE, blob)
        except ERRORS as e:
            closed(('R2A',), f'gate de R2-A sobre HEAD ({e.__class__.__name__}: {e})')
        b1 = r2a = None
        try:
            b1 = load_verified(objs, B1_ANCHOR, B1_GATE, 'f35sbxb_gate_b1_verificado_b3')
            r2a = load_verified(objs, R2A_COMPLETION, R2A_GATE, 'f35sbxb2_gate_r2a_verificado_b3')
        except ERRORS as e:
            closed(('SEM', 'R2A', 'MAT'), f'gates de B1 y de R2-A verificados ({e.__class__.__name__}: {e})')
        mat_obs = None
        if r2a is not None and parents is not None:
            try:
                gate = entry(objs, commit_parts(objs, CANDIDATE)[0], B2_GATE)
                if gate is None or gate[:2] != ('100644', 'blob'):
                    raise GitError('el gate de B2 no es un blob regular en el candidato')
                mat = check('MAT', mat_problems, objs, parents, head, branch, gate[2], r2a)
                if mat:
                    info.append(mat[0])
                    mat_obs = mat[1]
            except ERRORS as e:
                closed(('MAT',), f'gate de B2 en el candidato ({e.__class__.__name__}: {e})')
        if parents is not None:
            check('INT', int_problems, objs, parents)
            check('GOV', gov_problems, objs, parents, head, notes)
            check('FRZ', frz_problems, objs, head, parents, notes)
        if b1 is not None and r2a is not None:
            check('SEM', sem_problems, objs, head, b1, r2a)
        check('ALC', alc_problems, objs, head)
        pipeline_rules(viol, info, objs)
        if 'R2A' in background:
            if mat_obs is None or b1 is None or r2a is None or parents is None:
                closed(('R2A',), 'no verificable sin la salida del gate de B2 y los gates verificados')
            else:
                r2 = check('R2A', lambda: r2a_problems(background['R2A'].result(), r2a, objs, parents, head, branch,
                                                       b1, mat_obs))
                if r2:
                    info.append(r2[0])
        if 'HIS' in background:
            his = check('HIS', lambda: his_problems(*background['HIS'].result()))
            if his:
                info.append(his[0])
    except ERRORS as e:
        closed(('CTX', 'ANC', 'HIS', 'R2A', 'MAT', 'INT', 'GOV', 'SEM', 'ALC', 'FRZ') + PIPE_RULES,
               f'objetos Git ({e.__class__.__name__}: {e})')
    finally:
        for rid, job in background.items():
            try:
                job.close()
            except OSError as e:
                viol[rid].append(f'limpieza incompleta del temporal ({e.__class__.__name__}): falla cerrado')
        if objs is not None:
            objs.close()
    info.append(f'INFO GOV: transición de B3 derivada: {notes["transition"] or "ninguna"}; registrada: {B3_TRANSITION}')
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
    print(f'validate_f35sbxb3: {len(ORDER) - len(fallas)} comprobaciones correctas, {len(fallas)} fallas')
    sys.exit(1 if fallas else 0)


if __name__ == '__main__':
    main()
