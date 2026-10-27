#!/usr/bin/env python3
"""Validador fail-closed del paquete F36-SBX (autorización, investigación y diseño), versión 5 (AF4).

Solo biblioteca estándar. No ejecuta ML ni NLP, no usa red y no escribe archivos (tampoco el índice de Git).

- Recalcula el F36-SBX-GATE y exige que coincida con el declarado.
- Valida la semántica de la evidencia de equipo (FG-02, FG-03, FG-10 y FG-12), su vínculo con el commit
  candidato auditado y su coherencia exacta con el bloque canónico del informe de auditoría o del ADR. El ADR se
  lee del blob Git de candidate_commit, nunca del árbol de trabajo.
- Valida el contrato de evidencia cerrado (v4) y, con él, el ejemplo de conformidad: estructura, hashes de
  contenido, de registro, de fragmento y de output, sello de test, provenance contextual, aislamiento entre
  tenants, cobertura mínima y contexto canónico de todo output (REL-01..REL-15).
- Consulta Git por una única vía endurecida (objetos reales, sin refs/replace) y compara el árbol de trabajo
  con el índice por sus bytes, sin confiar en assume-unchanged, skip-worktree ni en la caché de stat (AF4).

Uso: python -I -B docs/academico/tools/f36sbx/validate_f36sbx.py
"""
import ast
import csv
import datetime
import hashlib
import io
import json
import os
import re
import stat
import subprocess
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]

BASE = 'b8892af39a6492d8dd44a36290604efc602380cd'
BRANCHES = frozenset({'feature/f36-sbx-authorization-design', 'develop', 'main'})
PKG = 'docs/academico/f36-sbx'
TOOLS = 'docs/academico/tools/f36sbx'
GATE_EVIDENCE = PKG + '/gate/evidencia/'
CHARTER = PKG + '/F36SBX_Charter.md'
MATRIX = PKG + '/F36SBX_Matriz_Capacidades.md'
THREATS = PKG + '/F36SBX_Threat_Model.md'
PLAN = PKG + '/F36SBX_Plan_Evaluacion.md'
GATE_DOC = PKG + '/F36SBX_Gate_Sucesor.md'
CONTRACT = PKG + '/contrato/f36sbx_evidence_contract.json'
EXAMPLE = PKG + '/contrato/f36sbx_contract_example.json'
GATE_STATE = PKG + '/gate/f36sbx_gate_state.json'
TEAM_SCHEMA = PKG + '/gate/f36sbx_team_evidence_schema.json'
F33_MATRIX = 'docs/academico/diseno-inteligente/F33_Matriz_Capacidades_y_Restricciones.md'
PKG_DOCS = ['README.md', 'F36SBX_Charter.md', 'F36SBX_Matriz_Capacidades.md', 'F36SBX_Investigacion_Diseno.md',
            'F36SBX_Contrato_Evidencia.md', 'F36SBX_Threat_Model.md', 'F36SBX_Plan_Evaluacion.md',
            'F36SBX_Gate_Sucesor.md', 'F36SBX_Trazabilidad.md', 'F36SBX_Correccion_AF1.md', 'F36SBX_Correccion_AF2.md',
            'F36SBX_Correccion_AF3.md']
PKG_DATA = [CONTRACT, EXAMPLE, GATE_STATE, TEAM_SCHEMA]
PKG_FILES = [f'{PKG}/{n}' for n in PKG_DOCS] + PKG_DATA
GOV_FILES = ['CLAUDE.md', 'README.md', 'docs/PROGRESS.md', 'docs/academico/ACADEMIC_BASELINE.md']
F34 = 'docs/academico/datos-sinteticos/dataset/'
UPSTREAM_FILES = [F34 + 'applications.csv', F34 + 'criteria.csv', F34 + 'vacancies.csv', F34 + 'manifest.json',
                  F34 + 'competencies.csv']

# Integridad de los artefactos cerrados: SHA-256 de su JSON canónico. Cambiarlos exige un incremento auditado.
CONTRACT_SHA256 = '5587f183ab2d89a8f2b4959f6ebf62a984184cfe592bb9da737356c9ab0b695f'
TEAM_SCHEMA_SHA256 = '89cbc2286730bd301834ec43a7bf959c7343de266f2e78b10e96edd906da92f2'

# Etiquetas de dominio de los hashes de registro (sección hash_scheme del contrato).
TAG_RECORD = 'f36sbx-artifact-record-v1'
TAG_FRAGMENT = 'f36sbx-fragment-v1'
TAG_INPUT = 'f36sbx-input-manifest-v1'
TAG_OUTPUT = 'f36sbx-output-v1'
TAG_SEAL = 'f36sbx-test-seal-v2'
SEAL_ALGORITHM = 'f36sbx-test-seal-sha256-v2'

# Estado vigente de los cuatro documentos de gobierno: exactamente estas líneas, una vez cada una.
REQUIRED_STATE = ['G0 real = NO APROBADA', 'G0-09 = CUMPLIDO', 'G0-14 = CUMPLIDO', 'G0-02 = PENDIENTE EXTERNO',
                  'G0-03 = PENDIENTE EXTERNO', 'G0-12 = PENDIENTE EXTERNO', 'ADR-005 = PROPUESTA',
                  'G0-SBX = APROBADA CON RESTRICCIONES', 'F35 productiva = BLOQUEADA',
                  'F35-SBX = CERRADA Y CONGELADA', 'F36-SBX = EN DISEÑO', 'F36-SBX-GATE = NO SUPERADO',
                  'F37-SBX = BLOQUEADA', 'F36–F40 = BLOQUEADAS', 'Alcance C = BLOQUEADO', 'Datos reales = PROHIBIDOS']
MEMBERS = ('Coronacion Meza Fredy', 'Peña Arroyo Anthony', 'Vila Meza Luis Antonio')
CLAUDE_MEMBERS = 'Integrantes: Coronacion Meza Fredy, Peña Arroyo Anthony y Vila Meza Luis Antonio.'

# Afirmaciones de estado que nunca pueden aparecer en el paquete ni en el gobierno.
FORBIDDEN_CLAIMS = [
    (r'\bG0 real\s*=\s*APROBADA', 'G0 real aprobada'),
    (r'\bG0\s*=\s*APROBADA', 'G0 aprobada sin sufijo'),
    (r'ADR-005(?: canónico)?\s*=\s*APROBAD', 'ADR-005 aprobado'),
    (r'(?i)alcance C\s*=\s*+(?!BLOQUEADO)', 'alcance C no bloqueado'),
    (r'(?i)datos reales\s*=\s*+(?!PROHIBIDOS)', 'datos reales no prohibidos'),
    (r'(?i)F37-SBX(?:-[A-Z])? (?:queda|está|esta) (?:habilitada|autorizada|iniciada)', 'F37-SBX habilitada'),
    (r'(?i)RF-23\s*(?:=|es)\s*autom', 'RF-23 automática'),
]
# Afirmaciones «sujeto = ESTADO» o «sujeto: ESTADO» sobre fases, puertas, ADR, alcance y datos.
CLAIM_RX = re.compile(r'(?<![\w-])(?P<subj>G0(?: real|-SBX|-\d{2})?|ADR-\d{3}(?: canónico)?'
                      r'|F\d{2}(?:-F\d{2})?(?:-SBX(?:-[A-Z0-9]+)*)?(?: productivas?)?'
                      r'|[Aa]lcance [A-Z](?: [a-záéíóúñ]+)*|[Dd]atos reales)'
                      r'\s*(?P<sep>[:=])\s*(?P<state>[A-ZÁÉÍÓÚÑ]{2}[A-ZÁÉÍÓÚÑ ]*)')
ID_CLAIM_RX = re.compile(r'(?<![\w-])(?P<subj>EI-\d{2}|RF-\d{2})\s*(?P<sep>=)\s*(?P<state>[A-ZÁÉÍÓÚÑ]{2}[A-ZÁÉÍÓÚÑ ]*)')
# Con «:» solo cuenta como afirmación si el estado empieza por una palabra de estado; con «=», siempre.
STATE_WORDS = {'ABIERTA', 'ABIERTO', 'ACTIVA', 'ACTIVO', 'APROBADA', 'APROBADO', 'AUTORIZADA', 'AUTORIZADO',
               'BLOQUEADA', 'BLOQUEADAS', 'BLOQUEADO', 'BLOQUEADOS', 'CERRADA', 'CERRADO', 'CONGELADA', 'CUMPLIDO',
               'DESBLOQUEADA', 'DESBLOQUEADO', 'EJECUTADA', 'EN', 'HABILITADA', 'HABILITADAS', 'HABILITADO',
               'IMPLEMENTADA', 'INICIADA', 'INICIADO', 'INTEGRADA', 'LISTA', 'NO', 'PENDIENTE', 'PERMITIDO',
               'PERMITIDOS', 'PROHIBIDOS', 'PROPUESTA', 'PROPUESTO', 'REVOCADA', 'REVOCADO', 'SUPERADA', 'SUPERADO',
               'VIGENTE'}
# Tabla «Estados de gobierno que el charter preserva»: el valor de cada fila empieza por su estado.
CHARTER_STATES = {'G0 real': 'NO APROBADA', 'G0-02, G0-03 y G0-12': 'PENDIENTE EXTERNO',
                  'G0-09 y G0-14': 'CUMPLIDO', 'G0-SBX': 'APROBADA CON RESTRICCIONES', 'ADR-005': 'PROPUESTA',
                  'F35 productiva': 'BLOQUEADA', 'F35-SBX': 'CERRADA Y CONGELADA',
                  'F36-F40 productivas': 'BLOQUEADAS', 'Alcance C': 'BLOQUEADO', 'Datos reales': 'PROHIBIDOS',
                  'RF-23': 'Decisión final humana', 'RF-29': 'Experimental', 'GC-AF-L01': 'LOW, ABIERTO / DIFERIDO'}

# Matriz fijada: clase y alcance de cada EI. Reclasificar exige un incremento auditado.
EXPECTED_MATRIX = {
    'EI-01': ('ALLOWED', 'B'), 'EI-02': ('ALLOWED', 'B'), 'EI-03': ('ALLOWED', 'B'), 'EI-04': ('ALLOWED', 'B'),
    'EI-05': ('ALLOWED', 'B'), 'EI-06': ('ALLOWED', 'B'), 'EI-07': ('ALLOWED', 'B'),
    'EI-08': ('CONDITIONAL', 'C'), 'EI-09': ('CONDITIONAL', 'B'), 'EI-10': ('CONDITIONAL', 'C'),
    'EI-11': ('CONDITIONAL', 'C'), 'EI-12': ('CONDITIONAL', 'C'), 'EI-24': ('CONDITIONAL', 'C'),
    'EI-13': ('BLOCKED', '—'), 'EI-14': ('BLOCKED', '—'), 'EI-15': ('BLOCKED', 'C'), 'EI-16': ('BLOCKED', '—'),
    'EI-17': ('BLOCKED', '—'), 'EI-18': ('BLOCKED', '—'), 'EI-19': ('BLOCKED', '—'), 'EI-20': ('BLOCKED', '—'),
    'EI-21': ('BLOCKED', '—'), 'EI-22': ('BLOCKED', '—'), 'EI-23': ('BLOCKED', '—'),
}
EXPECTED_CLASSES = {ei: cls for ei, (cls, _) in EXPECTED_MATRIX.items()}
SCOPE_C_CONDITIONAL = sorted(ei for ei, (cls, sc) in EXPECTED_MATRIX.items() if cls == 'CONDITIONAL' and sc == 'C')
EI_IDS = [f'EI-{i:02d}' for i in range(1, 25)]
CLASSES = ('ALLOWED', 'CONDITIONAL', 'BLOCKED')
# Temas que deben quedar en una fila BLOCKED de la matriz (columna de capacidad).
MUST_BLOCK = ['resumen', 'veredicto', 'ocr', 'llm sobre evidencia', 'llm para generar', 'entre candidatos',
              'scoring', 'ranking', 'recomendación', 'selección automática', 'emociones', 'personalidad',
              'honestidad', 'inteligencia', 'estrés', 'nerviosismo', 'biometría', 'rostro', 'voz', 'prosodia',
              'acento', 'audio', 'ajuste fino', 'datos reales', 'endpoints', 'migraciones']
# Términos que una capacidad ALLOWED no puede nombrar: son del alcance C o están bloqueados.
NOT_ALLOWED_WORDS = [r'embedding', r'sem[aá]ntic', r'\bocr\b', r'\bllm', r'\bpdf\b', r'\bdocx\b', r'\bner\b',
                     r'extracci', r'transformer', r'whisper', r'\bstt\b', r'\baudio\b']

TEI_IDS = [f'TEI-{i:02d}' for i in range(1, 23)]
THREAT_TOPICS = ['injection', 'malicioso', 'envenenamiento', 'fuga criterio', 'organizaciones', 'pii',
                 'alucinación', 'sin respaldo', 'automatización', 'ranking encubierto', 'inferencias prohibidas',
                 'procedencia', 'deriva de modelo', 'reproducibilidad', 'dependencia externa',
                 'cadena de suministro', 'agotamiento', 'adversarial', 'abstención', 'contaminación']
M_IDS = [f'M-{i:02d}' for i in range(1, 14)]
R_IDS = [f'R-{i:02d}' for i in range(1, 6)]

# Invariantes del contrato v3 que se comprueban además de su hash.
CONTRACT_KEYS = ['contract_id', 'contract_version', 'status', 'environment', 'source_type_allowed', 'generator_policy',
                 'allowed_upstream_sources', 'upstream_files', 'global_upstream_sources', 'global_upstream_policy',
                 'upstream_manifest', 'content_upstream_bindings', 'tenant_bound_tokens', 'internal_references',
                 'global_identifiers', 'forbidden_upstream_sources',
                 'synthetic_markers', 'identifier_patterns', 'enums', 'content_field_types',
                 'artifact_envelope_fields', 'artifact_types', 'fragment_fields', 'output_fields',
                 'method_config_fields', 'top_k_range', 'output_ei', 'context_fields', 'canonical_context',
                 'provenance_fields',
                 'example_fields', 'example_id_value', 'example_coverage', 'partition_manifest_fields',
                 'partition_fields', 'threshold_fields', 'hash_scheme', 'relations', 'group_marker_only_in',
                 'forbidden_fields', 'forbidden_field_tokens', 'splits']
ALLOWED_UPSTREAM = {'docs/academico/datos-sinteticos/dataset', 'docs/academico/evidencia-sbx/fixtures'}
EXPECTED_UPSTREAM_FILES = {
    F34 + 'applications.csv': {'key': 'application_token', 'scope': 'tenant', 'cardinality': 'exactly_one_own',
                               'context': {'organization': 'organization_token', 'vacancy': 'vacancy_token',
                                           'application': 'application_token'}},
    F34 + 'criteria.csv': {'key': 'criterion_id', 'scope': 'tenant', 'cardinality': 'any_same_vacancy',
                           'context': {'vacancy': 'vacancy_token'}},
    F34 + 'vacancies.csv': {'key': 'vacancy_token', 'scope': 'tenant', 'cardinality': 'exactly_one_own',
                            'context': {'organization': 'organization_token', 'vacancy': 'vacancy_token'}},
}
REQUIRED_FORBIDDEN_SOURCES = {'docs/academico/g0-evidence', 'storage', 'database', 'http://', 'https://'}
MARKERS = {'synthetic_id_prefix': 'SBX36-', 'text_prefix': '[SINTÉTICO]', 'source_type': 'synthetic',
           'environment': 'sandbox', 'hash_algorithm': 'f36sbx-content-sha256-v1',
           'synthetic_organization_ids': ['ORG-S1', 'ORG-S2', 'ORG-S3']}
ARTIFACT_TYPES = {'cv_document': 'A', 'certificate': 'A', 'interview_transcript': 'A', 'human_observation': 'A',
                  'relevance_annotation': 'A', 'adversarial_case': 'A', 'counterfactual_pair': 'B',
                  'rendered_document': 'B'}
ENVELOPE = ['synthetic_id', 'artifact_type', 'stage', 'synthetic_organization_id', 'scenario_id', 'vacancy_token',
            'application_token', 'partition', 'template_family', 'source_type', 'environment', 'hash_algorithm',
            'content', 'content_hash', 'provenance', 'record_hash']
CONTEXT = ['synthetic_organization_id', 'scenario_id', 'vacancy_token', 'application_token', 'partition']
FRAGMENT_FIELDS = ['fragment_id', 'artifact_id', 'artifact_record_hash', *CONTEXT, 'text_path', 'char_start',
                   'char_end', 'text_hash', 'fragment_hash']
OUTPUT_FIELDS = ['output_id', 'ei', 'method_id', 'method_version', 'method_config', *CONTEXT, 'query_criterion_id',
                 'fragment_refs', 'fragment_ref_hashes', 'abstained', 'input_manifest_hash', 'output_hash']
PROVENANCE = ['generator_id', 'generator_version', 'template_id', 'template_family', 'seed', 'upstream_refs',
              'content_hash']
TENANT_TOKENS = ['author_token', 'annotator_token']
INTERNAL_REFERENCES = {'fragment_id': 'fragments', 'variant_of': 'artifacts', 'rendered_from': 'artifacts'}
EXPECTED_SPLITS = {'partitions': ['dev', 'test'], 'forbidden_partitions': ['train'], 'train_allowed': False,
                   'group_by': ['template_family', 'vacancy_token'], 'test_sealed_before_any_run': True,
                   'seal_algorithm': SEAL_ALGORITHM, 'thresholds_fit_on': 'dev', 'test_used_for_tuning': False,
                   'temporal_embargo': 'process_splits_f34', 'counterfactual_pairs_same_partition': True}
EXPECTED_COVERAGE = {'artifact_types': list(ARTIFACT_TYPES), 'min_fragments': 1, 'min_outputs_with_fragments': 1,
                     'min_abstained_outputs': 1, 'min_test_artifacts': 1, 'min_test_gold_annotations': 1,
                     'min_test_outputs': 1, 'min_tuning_outputs': 1, 'min_scenarios': 2}
EXPECTED_HASH_TAGS = {'record_hash': TAG_RECORD, 'fragment_hash': TAG_FRAGMENT, 'input_manifest_hash': TAG_INPUT,
                      'output_hash': TAG_OUTPUT, 'seal_sha256': TAG_SEAL}
REQUIRED_FORBIDDEN_FIELDS = {'name', 'dni', 'email', 'phone', 'address', 'photo', 'age', 'gender', 'score', 'rank',
                             'recommendation', 'suitability', 'suggested_level', 'emotion', 'personality',
                             'honesty', 'intelligence', 'stress', 'nervousness', 'voice', 'face', 'prosody',
                             'accent', 'audio', 'video', 'biometric'}
REQUIRED_FORBIDDEN_TOKENS = {'name', 'dni', 'email', 'phone', 'gender', 'score', 'rank', 'recommendation', 'fit',
                             'verdict', 'emotion', 'personality', 'honesty', 'intelligence', 'stress',
                             'nervousness', 'voice', 'face', 'biometric', 'level', 'hire', 'select', 'discard'}
REL_IDS = [f'REL-{i:02d}' for i in range(1, 16)]
# REL-15: el contexto canónico de una postulación es el de sus artefactos del conjunto, y lo hereda todo output.
EXPECTED_CANONICAL = {'key': 'application_token', 'source': 'artifacts', 'fields': CONTEXT,
                      'applies_to': ['outputs', 'tuning_outputs']}

FG_IDS = [f'FG-{i:02d}' for i in range(1, 15)]
FG_TEAM = ('FG-02', 'FG-03', 'FG-10', 'FG-12')
FG_NA_ALLOWED = frozenset({'FG-12'})
AUTO_STATUSES = frozenset({'CUMPLE', 'NO CUMPLE'})
TEAM_STATUSES = frozenset({'CUMPLE', 'PENDIENTE', 'NO CUMPLE'})
STATUSES = AUTO_STATUSES | TEAM_STATUSES | {'NO APLICA'}
GATE_VERSION = '3'
TEAM_SCHEMA_TAG = 'f36sbx-team-evidence/v2'
GATE_KEYS = {'gate_id', 'gate_version', 'authorizes', 'cannot_authorize', 'base_commit', 'candidate_commit',
             'team_evidence_schema', 'criteria', 'f37_authorized_ei', 'revocation', 'declared_result'}
CANNOT_AUTHORIZE = {'produccion', 'datos_reales', 'pii_real', 'audio_video_real', 'seleccion_automatica',
                    'scoring_ranking_recomendacion', 'cambio_rf23_rf21_rf29', 'g0_real', 'alcance_c_producto',
                    'endpoints_migraciones_ui', 'ei_blocked'}
# Marcadores de posición que nunca identifican a una persona. Se comparan con placeholder_key(): sin mayúsculas,
# tildes, dígitos ni puntuación, así que «PLACEHOLDER», «<Placeholder 1>» y «place_holder» son el mismo marcador.
PLACEHOLDERS = {'auditor', 'auditora', 'independiente', 'auditor independiente', 'auditora independiente',
                'auditoria independiente', 'n a', 'na', 'n d', 'nd', 'tbd', 'tba', 'todo', 'pendiente', 'por definir',
                'por asignar', 'sin nombre', 'desconocido', 'desconocida', 'unknown', 'anonimo', 'anonima',
                'anonymous', 'none', 'null', 'nil', 'nadie', 'nobody', 'nombre', 'nombre del auditor',
                'nombre apellido', 'name', 'xxx', 'xxxx', 'test', 'prueba', 'placeholder', 'place holder',
                'marcador', 'marcador de posicion', 'lorem ipsum', 'ejemplo', 'example', 'sample', 'dummy', 'foo',
                'bar', 'foo bar', 'changeme', 'change me', 'fixme', 'reemplazar', 'completar', 'rellenar'}
# Una identidad formada solo por estas palabras es genérica: no nombra a nadie ni a ninguna sesión concreta.
GENERIC_IDENTITY_WORDS = {
    # Roles y funciones.
    'auditor', 'auditora', 'auditores', 'auditoras', 'auditoria', 'auditorias', 'revisor', 'revisora', 'revisores',
    'revisoras', 'revision', 'revisiones', 'evaluador', 'evaluadora', 'evaluadores', 'evaluacion', 'inspector',
    'inspectora', 'inspeccion', 'verificador', 'verificadora', 'verificacion', 'validador', 'validadora',
    'validacion', 'aprobador', 'aprobadora', 'aprobacion', 'examinador', 'examinadora', 'perito', 'perita',
    'analista', 'consultor', 'consultora', 'asesor', 'asesora', 'experto', 'experta', 'especialista', 'tecnico',
    'tecnica', 'profesional', 'independiente', 'independientes', 'externo', 'externa', 'externos', 'externas',
    'interno', 'interna', 'internos', 'internas', 'sesion', 'sesiones', 'equipo', 'grupo', 'comite', 'comision',
    'persona', 'personas', 'responsable', 'responsables', 'encargado', 'encargada', 'academico', 'academica',
    'docente', 'docentes', 'integrante', 'integrantes', 'miembro', 'miembros', 'participante', 'tercero', 'tercera',
    'terceros', 'parte', 'usuario', 'usuaria', 'autor', 'autora', 'firmante', 'titular', 'sistema', 'agente', 'bot',
    'administrador', 'administradora',
    # Tratamientos.
    'sr', 'sra', 'srta', 'senor', 'senora', 'senorita', 'don', 'dona', 'dr', 'dra', 'doctor', 'doctora', 'lic',
    'licenciado', 'licenciada', 'ing', 'ingeniero', 'ingeniera', 'mg', 'mgtr', 'magister', 'prof', 'profesor',
    'profesora', 'mr', 'mrs', 'ms',
    # Conectores.
    'de', 'del', 'la', 'el', 'los', 'las', 'y', 'e', 'un', 'una',
    # Inglés.
    'reviewer', 'reviewers', 'auditors', 'audit', 'auditing', 'review', 'assessor', 'evaluator', 'examiner',
    'verifier', 'approver', 'expert', 'consultant', 'independent', 'external', 'internal', 'session', 'team',
    'member', 'members', 'user', 'person', 'people', 'staff', 'officer', 'agent', 'system', 'admin', 'administrator',
    'owner', 'author', 'signer', 'party', 'third', 'the', 'a', 'an', 'of'}
# AF4-L01: palabras funcionales que tampoco identifican (preposiciones, conjunciones, negaciones, pronombres)…
IDENTITY_FUNCTION_WORDS = {'en', 'con', 'sin', 'por', 'para', 'al', 'lo', 'o', 'u', 'ni', 'no', 'su', 'sus', 'se',
                           'que', 'tal', 'aqui', 'aca', 'este', 'esta', 'ese', 'esa', 'otro', 'otra', 'and', 'or',
                           'in', 'on', 'at', 'by', 'for', 'to', 'with', 'without', 'not', 'me', 'my', 'your', 'our',
                           'here', 'this', 'that', 'other'}
# … y palabras que marcan un hueco por rellenar o una identidad ausente, ficticia o de relleno. Se suman a las
# de una sola palabra de PLACEHOLDERS.
IDENTITY_MARKER_WORDS = {
    'place', 'holder', 'posicion', 'lorem', 'ipsum', 'dolor', 'amet', 'change', 'fix', 'pending', 'pendientes',
    'desconocidos', 'desconocidas', 'anonimos', 'anonimas', 'anon', 'anonimizado', 'anonimizada', 'incognito',
    'incognita', 'ignoto', 'ignota', 'unnamed', 'unidentified', 'unspecified', 'undefined', 'unassigned', 'nn', 'sn',
    'nombres', 'apellido', 'apellidos', 'surname', 'firstname', 'lastname', 'fullname', 'username', 'definir',
    'asignar', 'confirmar', 'identificar', 'determinar', 'especificar', 'indicar', 'precisar', 'complete', 'rellene',
    'reemplace', 'sustituir', 'sustituya', 'insertar', 'inserte', 'ingresar', 'ingrese', 'escribir', 'escriba',
    'editar', 'edite', 'enter', 'insert', 'replace', 'fill', 'definido', 'definida', 'asignado', 'asignada',
    'identificado', 'identificada', 'determinado', 'determinada', 'indeterminado', 'indeterminada', 'especificado',
    'especificada', 'indicado', 'indicada', 'disponible', 'aplica', 'consta', 'tests', 'testing', 'pruebas',
    'ejemplos', 'examples', 'samples', 'muestra', 'demo', 'mock', 'stub', 'fake', 'falso', 'falsa', 'ficticio',
    'ficticia', 'ficticios', 'ficticias', 'generico', 'generica', 'generic', 'imaginario', 'imaginaria',
    'hipotetico', 'hipotetica', 'inventado', 'inventada', 'supuesto', 'supuesta', 'simulado', 'simulada', 'baz',
    'qux', 'quux', 'fulano', 'fulana', 'mengano', 'mengana', 'zutano', 'zutana', 'perengano', 'perengana',
    'alguien', 'cualquiera', 'someone', 'somebody', 'anyone', 'tbc', 'wip', 'redacted', 'omitido', 'omitida',
    'oculto', 'oculta', 'reservado', 'reservada', 'confidencial'}
IDENTITY_NOISE = frozenset(GENERIC_IDENTITY_WORDS | IDENTITY_FUNCTION_WORDS | IDENTITY_MARKER_WORDS
                           | {k for k in PLACEHOLDERS if ' ' not in k})
# Piezas de una concatenación sin separadores («auditorplaceholder»): roles y marcadores de cuatro letras o más.
IDENTITY_SEGMENTS = frozenset(w for w in IDENTITY_NOISE - IDENTITY_FUNCTION_WORDS if len(w) >= 4)
IDENTITY_FILLER = re.compile(r'(.)\1+')
LEET = str.maketrans('013457', 'oieast')
# Categorías Unicode prohibidas en identidades y en documentos humanos: control, formato (U+200B, U+202E…),
# uso privado, no asignados y separadores de línea o de párrafo.
INVISIBLE_CATEGORIES = frozenset({'Cc', 'Cf', 'Co', 'Cn', 'Zl', 'Zp'})
GIT_REGULAR_MODE = '100644'
# Vista normativa de Git (AF4-M02): objetos reales, sin las sustituciones de refs/replace ni la caché del grafo de
# commits, sin fsmonitor y sin escrituras opcionales. git_env() quita además toda variable GIT_* heredada
# (GIT_DIR, GIT_INDEX_FILE, GIT_OBJECT_DIRECTORY, GIT_REPLACE_REF_BASE, GIT_*_PATHSPECS…), que cambiaría el
# repositorio, el índice, los objetos o las rutas consultados. La única consulta con pathspec (git_blob) los trata
# literalmente. Ninguna opción desactiva los injertos (info/grafts): git_state_problems() los rechaza.
GIT_GLOBAL = ('--no-replace-objects', '--no-optional-locks', '-c', 'core.commitGraph=false',
              '-c', 'core.fsmonitor=false', '-c', 'core.untrackedCache=false')
GIT_ENV = {'GIT_NO_REPLACE_OBJECTS': '1', 'GIT_OPTIONAL_LOCKS': '0'}
# Operaciones de Git en curso: el árbol de trabajo no corresponde a ningún commit (estado ambiguo).
GIT_PENDING = ('MERGE_HEAD', 'CHERRY_PICK_HEAD', 'REVERT_HEAD', 'REBASE_HEAD', 'rebase-merge', 'rebase-apply',
               'sequencer', 'BISECT_LOG')
# Modos del índice cuyo contenido se compara con el árbol de trabajo: archivo, ejecutable y enlace simbólico.
WORKTREE_MODES = frozenset({'100644', '100755', '120000'})
HEX40 = re.compile(r'[0-9a-f]{40}')
HEX64 = re.compile(r'[0-9a-f]{64}')
INDEX = re.compile(r'0|[1-9][0-9]*')
FENCE_RX = re.compile(r'^```(?P<info>[^\n`]*)\n(?P<body>.*?)\n```[ \t]*$', re.M | re.S)
# Aserciones normativas fuera del bloque canónico (también entre comillas, como en un JSON señuelo).
COUNT_ASSERTION_RX = re.compile(r'(?i)\b(blocker|high|medium[ _]requiring[ _]fix|medium[ _]accepted|low)\b["\']?\s*[:=]\s*\d')
VERDICT_ASSERTION_RX = re.compile(r'(?i)\b(veredicto|verdict)\b["\']?\s*[:=]')
STATUS_ASSERTION_RX = re.compile(r'(?i)\b(estado|status)\b["\']?\s*[:=]')
ADR_STATUS_TOKENS = ('PROPUESTO', 'APROBADO', 'RECHAZADO', 'REVOCADO')

STDLIB = frozenset({'ast', 'copy', 'csv', 'datetime', 'hashlib', 'importlib', 'io', 'json', 'os', 're', 'subprocess',
                    'sys', 'unicodedata', 'pathlib', 'unittest', 'tempfile', 'itertools', 'contextlib', 'types',
                    'shutil', 'stat'})
LOCAL_MODULES = frozenset({'validate_f36sbx', 'test_f36sbx', 'test_f36sbx_git'})
ML_IMPORT = re.compile(r'^\s*(?:import|from)\s+(torch|transformers|sentence_transformers|spacy|sklearn|pypdf|'
                       r'pdfplumber|docx|pytesseract|ollama|openai|anthropic|faiss|chromadb|whisper|numpy|'
                       r'pandas|requests|urllib3|httpx)\b', re.M)
PII_PATTERNS = [(re.compile(r'[\w.+-]+@[\w-]+\.[A-Za-z]{2,}'), 'correo'),
                (re.compile(r'(?<![\w])9\d{8}(?![\w])'), 'teléfono'),
                (re.compile(r'(?<![\w])\d{8}(?![\w])'), 'DNI')]
RUNTIME_PREFIXES = ('app/', 'routes/', 'config/', 'database/', 'resources/', 'ml-service/', 'bootstrap/',
                    'public/', 'tests/', 'docker/', '.github/', 'cypress/')
DEPENDENCY_FILES = frozenset({'composer.json', 'composer.lock', 'package.json', 'package-lock.json',
                              'ml-service/pyproject.toml', 'docker-compose.yml', 'Dockerfile'})
F35_FROZEN = ('docs/academico/evidencia-sbx', 'docs/academico/g0-', 'docs/academico/tools/f35sbx',
              'docs/academico/datos-sinteticos/', 'docs/academico/diseno-inteligente/',
              'docs/academico/investigacion-ia/', 'docs/academico/TECHNICAL_DEBT.md')


# ---------------------------------------------------------------- utilidades

_CACHE = {}


def memo(kind, key, fn):
    """Memoriza un resultado que depende solo de key (textos inmutables o rutas que no cambian en el proceso).

    Solo acelera las baterías, que evalúan cientos de fotografías casi iguales; clear_caches() lo vacía."""
    k = (kind, key)
    if k not in _CACHE:
        _CACHE[k] = fn()
    return _CACHE[k]


def clear_caches():
    _CACHE.clear()


def norm(text):
    """NFKC y guiones unificados, para que una variante tipográfica no esquive una regla."""
    text = unicodedata.normalize('NFKC', text)
    return re.sub('[‐‑‒–—―−]', '-', text)


def slug(heading):
    heading = re.sub(r'[`*]', '', heading).strip().lower()
    return re.sub(r'[^\w\- ]', '', heading).replace(' ', '-')


def strict_json(text):
    """JSON sin claves duplicadas en ningún nivel; cualquier error devuelve None (falla cerrado)."""
    def hook(pairs):
        keys = [k for k, _ in pairs]
        if len(keys) != len(set(keys)):
            raise ValueError('clave duplicada')
        return dict(pairs)
    try:
        return json.loads(text, object_pairs_hook=hook)
    except (ValueError, TypeError, RecursionError):
        return None


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def tagged_hash(tag, obj):
    """Hash de registro con separación de dominio: sha256(etiqueta + «\\n» + JSON canónico)."""
    return sha256(tag.encode('utf-8') + b'\n' + canonical(obj))


def without(record, key):
    return {k: v for k, v in record.items() if k != key}


def artifact_record_hash(a):
    return tagged_hash(TAG_RECORD, without(a, 'record_hash'))


def fragment_record_hash(f):
    return tagged_hash(TAG_FRAGMENT, without(f, 'fragment_hash'))


def output_record_hash(o):
    return tagged_hash(TAG_OUTPUT, without(o, 'output_hash'))


def input_manifest_hash(fragments, application, partition):
    pool = sorted([f.get('fragment_id'), f.get('fragment_hash')] for f in fragments
                  if f.get('application_token') == application and f.get('partition') == partition)
    return tagged_hash(TAG_INPUT, {'application_token': application, 'partition': partition, 'fragments': pool})


def test_seal(ex, contract_version):
    """Sello v2: registros, fragmentos y outputs de test, outputs de ajuste, oro de dev y umbrales.

    Los outputs de ajuste fijan por transitividad los fragmentos y artefactos de dev que usan; el oro de dev, las
    anotaciones con las que se ajustan los umbrales. El resto de dev no se sella: es la partición de desarrollo."""
    arts = [a for a in ex['artifacts'] if a.get('partition') == 'test']
    gold = [a for a in ex['artifacts'] if a.get('partition') == 'dev' and a.get('artifact_type') == 'relevance_annotation']
    frs = [f for f in ex['fragments'] if f.get('partition') == 'test']
    outs = {o.get('output_id'): o for o in ex['outputs']}
    tests = [o for o in ex['outputs'] if o.get('partition') == 'test']
    pm = ex['partition_manifest']
    tuning = pm['thresholds']['tuning_outputs']
    preimage = {
        'seal_algorithm': SEAL_ALGORITHM, 'contract_version': contract_version,
        'test_artifacts': sorted([a.get('synthetic_id'), a.get('record_hash')] for a in arts),
        'test_fragments': sorted([f.get('fragment_id'), f.get('fragment_hash')] for f in frs),
        'test_outputs': sorted([o.get('output_id'), o.get('output_hash')] for o in tests),
        'tuning_outputs': sorted([x, (outs.get(x) or {}).get('output_hash')] for x in tuning),
        'tuning_gold': sorted([a.get('synthetic_id'), a.get('record_hash')] for a in gold),
        'thresholds': pm['thresholds'], 'test_used_for_tuning': pm['test_used_for_tuning'],
    }
    return tagged_hash(TAG_SEAL, preimage)


def resolve_text(content, path, patterns):
    """Texto apuntado por text_path si coincide con un patrón del tipo; None en cualquier otro caso."""
    if not isinstance(path, str) or not isinstance(content, dict):
        return None
    parts = path.split('/')
    if not any(len(p.split('/')) == len(parts) and all(x == y or (x == '*' and INDEX.fullmatch(y))
                                                       for x, y in zip(p.split('/'), parts)) for p in patterns):
        return None
    cur = content
    for part in parts:
        if isinstance(cur, list) and INDEX.fullmatch(part) and int(part) < len(cur):
            cur = cur[int(part)]
        elif isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return None
    return cur if isinstance(cur, str) else None


def seal_bundle(ex, contract):
    """Recalcula, en orden de dependencias, todos los hashes derivados de un ejemplo y vuelve a sellar test.

    Solo la usan quienes construyen o mutan ejemplos en memoria (pruebas y generador): el validador verifica,
    nunca corrige."""
    types = contract['artifact_types']
    arts = {}
    for a in ex['artifacts']:
        a['content_hash'] = sha256(canonical(a.get('content')))
        if isinstance(a.get('provenance'), dict):
            a['provenance']['content_hash'] = a['content_hash']
        a['record_hash'] = artifact_record_hash(a)
        arts[a.get('synthetic_id')] = a
    for f in ex['fragments']:
        a = arts.get(f.get('artifact_id'))
        if a is not None:
            f['artifact_record_hash'] = a['record_hash']
            spec = types.get(a.get('artifact_type')) or {}
            text = resolve_text(a.get('content'), f.get('text_path'), spec.get('text_paths') or [])
            s0, s1 = f.get('char_start'), f.get('char_end')
            if text is not None and type(s0) is int and type(s1) is int:
                f['text_hash'] = sha256(text[s0:s1].encode('utf-8'))
        f['fragment_hash'] = fragment_record_hash(f)
    frs = {f.get('fragment_id'): f for f in ex['fragments']}
    for o in ex['outputs']:
        refs = o.get('fragment_refs') if isinstance(o.get('fragment_refs'), list) else []
        o['fragment_ref_hashes'] = [(frs.get(r) or {}).get('fragment_hash') for r in refs]
        o['input_manifest_hash'] = input_manifest_hash(ex['fragments'], o.get('application_token'), o.get('partition'))
        o['output_hash'] = output_record_hash(o)
    test = ex['partition_manifest']['partitions']['test']
    test['seal_sha256'] = test_seal(ex, contract['contract_version'])
    return ex


def parse_date(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        return None
    try:
        return datetime.date.fromisoformat(value)
    except ValueError:
        return None


def invisible_chars(text, allow_layout=False):
    """Caracteres de control, formato, privados, no asignados o separadores de línea (U+200B, U+202E…)."""
    layout = {'\n', '\t'} if allow_layout else set()
    return [c for c in text if c not in layout and unicodedata.category(c) in INVISIBLE_CATEGORIES]


def placeholder_key(value):
    """Clave de comparación de una identidad: sin mayúsculas, tildes, dígitos ni puntuación."""
    folded = unicodedata.normalize('NFKD', value.casefold())
    folded = ''.join(ch for ch in folded if not unicodedata.combining(ch))
    return re.sub(r'[\W\d_]+', ' ', folded).strip()


def identity_tokens(value):
    """Palabras alfanuméricas de una identidad (AF4-L01): camelCase separado, sin mayúsculas ni tildes, y con la
    forma compatible de cada carácter (NFKD: «ＡＵＤＩＴＯＲ» es «auditor»)."""
    chars = []
    for i, c in enumerate(value):
        if i and value[i - 1].islower() and c.isupper():
            chars.append(' ')
        chars.append(c)
    folded = unicodedata.normalize('NFKD', ''.join(chars).casefold())
    return re.findall(r'[^\W_]+', ''.join(ch for ch in folded if not unicodedata.combining(ch)))


def mixed_script(token):
    """¿La palabra mezcla letras latinas con cirílicas o griegas? Es la forma de un homógrafo («аuditor»)."""
    scripts = {unicodedata.name(c, '').split(' ')[0] for c in token if c.isalpha()}
    return 'LATIN' in scripts and bool(scripts & {'CYRILLIC', 'GREEK'})


def concatenated(word):
    """¿word es la unión, sin separadores, de roles o marcadores de cuatro letras o más («revisordesconocido»)?"""
    reach = {0}
    for i in range(4, len(word) + 1):
        if any(j in reach and word[j:i] in IDENTITY_SEGMENTS for j in range(max(0, i - 24), i - 3)):
            reach.add(i)
    return len(word) in reach


def nondistinctive(token):
    """¿La palabra no identifica a nadie? Número, inicial, rol, conector, marcador, relleno («xx», «zzz») o unión de
    roles y marcadores; también con dígitos en lugar de letras («pl4ceh0lder»)."""
    letters = re.sub(r'\d', '', token)
    if len(letters) < 2:
        return True
    for form in {letters, token.translate(LEET)}:
        if form in IDENTITY_NOISE:
            return True
        if IDENTITY_FILLER.fullmatch(form):
            return True
        if concatenated(form):
            return True
    return False


def identity_errors(value, label, min_letters=3, max_length=120):
    """Identidad declarada estructuralmente válida. No autentica a nadie: eso sigue siendo revisión humana.

    Tiene que contener al menos una palabra distintiva: no basta con combinar roles, conectores, marcadores de
    posición, rellenos, números o iniciales («Auditor placeholder», «revisor desconocido»), en ningún orden."""
    if not isinstance(value, str):
        return [f'{label}: no es texto']
    e = []
    if value != value.strip():
        e.append(f'{label}: tiene espacios al inicio o al final')
    bad = invisible_chars(value)
    if bad:
        e.append(f'{label}: contiene caracteres invisibles o de control {[f"U+{ord(c):04X}" for c in bad[:3]]}')
    if not unicodedata.is_normalized('NFC', value):
        e.append(f'{label}: no está en NFC')
    if sum(1 for c in value if unicodedata.category(c).startswith('L')) < min_letters:
        e.append(f'{label}: sin contenido visible suficiente (mínimo {min_letters} letras)')
    if len(value) > max_length:
        e.append(f'{label}: supera {max_length} caracteres')
    key = placeholder_key(value)
    tokens = identity_tokens(value)
    if not key or key in PLACEHOLDERS:
        e.append(f'{label}: es un marcador de posición')
    elif set(key.split()) <= GENERIC_IDENTITY_WORDS:
        e.append(f'{label}: es una identidad genérica, sin nombre ni identificador propio')
    elif all(nondistinctive(t) for t in tokens):
        e.append(f'{label}: es una identidad compuesta sin nombre propio (solo roles, conectores, marcadores, '
                 f'rellenos, números o iniciales)')
    if any(mixed_script(t) for t in tokens):
        e.append(f'{label}: mezcla letras latinas con cirílicas o griegas en una palabra (posible homógrafo)')
    return e


def git_env():
    """Entorno normativo de Git: el del proceso sin ninguna variable GIT_* heredada, más GIT_ENV (AF4-M02)."""
    env = {k: x for k, x in os.environ.items() if not k.upper().startswith('GIT_')}
    env.update(GIT_ENV)
    return env


def git_run(root, *args, stdin=None):
    """Única vía del validador hacia Git (AF4-M02): (código de salida, bytes de stdout); (None, b'') si no se ejecuta.

    Antepone GIT_GLOBAL y usa git_env(): objetos reales sin refs/replace, sin grafo de commits ni fsmonitor, sin
    escrituras opcionales y sin variables GIT_* heredadas. No decodifica ni convierte finales de línea."""
    try:
        r = subprocess.run(['git', *GIT_GLOBAL, *args], cwd=root, input=stdin, capture_output=True, env=git_env())
    except (OSError, ValueError):
        return None, b''
    return r.returncode, r.stdout


def git(root, *args):
    """Salida de texto de git_run (UTF-8, finales de línea normalizados); código -1 si Git no se puede ejecutar."""
    code, out = git_run(root, *args)
    return (-1 if code is None else code), out.decode('utf-8', 'replace').replace('\r\n', '\n')


def git_bytes(root, *args, stdin=None):
    """Salida binaria de git_run, sin decodificar ni convertir finales de línea; None si git falla."""
    code, out = git_run(root, *args, stdin=stdin)
    return out if code == 0 else None


def git_blob(root, sha, path):
    """Blob regular de commit:path leído de Git, nunca del árbol de trabajo. Única vía para documentos de un commit.

    Devuelve {'mode', 'type', 'object', 'data'} o {'error': motivo}. La ruta se trata literalmente (sin
    comodines) y tiene que identificar exactamente una entrada del árbol del commit; solo vale un blob regular
    (modo 100644): un árbol, un enlace simbólico, un submódulo o un ejecutable no lo son. Un archivo ignorado,
    sin versionar o añadido después del commit no existe en ese árbol. Lee objetos reales (git_run)."""
    if not (isinstance(sha, str) and HEX40.fullmatch(sha)) or not safe_repo_path(path):
        return {'error': 'commit o ruta fuera de formato'}
    out = git_bytes(root, '--literal-pathspecs', 'ls-tree', '-z', '--full-tree', sha, '--', path)
    if out is None:
        return {'error': 'no se pudo leer el árbol del commit (falla cerrado)'}
    entries = []
    for raw in (x for x in out.split(b'\0') if x):
        meta, sep, name = raw.partition(b'\t')
        fields = meta.split(b' ')
        if not sep or len(fields) != 3:
            return {'error': 'entrada del árbol ilegible (falla cerrado)'}
        entries.append([x.decode('utf-8', 'replace') for x in (*fields, name)])
    if not entries:
        return {'error': 'no existe en el árbol del commit: ignorado, sin versionar, añadido después o ruta inexistente'}
    if len(entries) != 1 or entries[0][3] != path:
        return {'error': 'la ruta no identifica exactamente una entrada del árbol del commit'}
    mode, kind, obj, _ = entries[0]
    if kind != 'blob' or mode != GIT_REGULAR_MODE:
        return {'error': f'no es un blob regular (tipo {kind}, modo {mode})', 'type': kind, 'mode': mode}
    data = git_bytes(root, 'cat-file', 'blob', obj)
    if data is None:
        return {'error': 'no se pudo leer el blob (falla cerrado)'}
    return {'mode': mode, 'type': kind, 'object': obj, 'data': data}


def git_blob_id(data):
    """Identificador de objeto Git (SHA-1) de un blob con estos bytes."""
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()


def blob_problem(blob):
    """Motivo por el que una resolución de git_blob no es un blob regular íntegro; None si lo es."""
    if not isinstance(blob, dict):
        return 'sin resolver en Git (falla cerrado)'
    if 'error' in blob:
        return str(blob['error'])
    data, obj = blob.get('data'), blob.get('object')
    if blob.get('type') != 'blob' or blob.get('mode') != GIT_REGULAR_MODE or not isinstance(data, bytes):
        return f'no es un blob regular (tipo {blob.get("type")}, modo {blob.get("mode")})'
    if not (isinstance(obj, str) and HEX40.fullmatch(obj)) or git_blob_id(data) != obj:
        return 'los bytes no son los del objeto Git resuelto (falla cerrado)'
    return None


def git_ignored(root, paths):
    """Rutas sin versionar que Git ignora y que, por tanto, ningún commit contiene; None si no se puede determinar
    (falla cerrado). Un archivo versionado nunca está ignorado."""
    paths = sorted(p for p in paths if isinstance(p, str))
    if not paths:
        return []
    code, out = git_run(root, 'check-ignore', '--stdin', '-z',
                        stdin=b''.join(p.encode('utf-8', 'surrogateescape') + b'\0' for p in paths))
    if code not in (0, 1):
        return None
    return sorted(x.decode('utf-8', 'replace') for x in out.split(b'\0') if x)


def git_commit(root, sha):
    """Commit real sha, verificado (el SHA-1 de sus bytes es sha): {'tree', 'parents', 'date'}; None si no lo es.

    date es la fecha del committer en su propia zona horaria, la de «git show -s --format=%cs». Un objeto
    inexistente, de otro tipo (también una etiqueta que apunte a un commit) o ilegible devuelve None."""
    if not (isinstance(sha, str) and HEX40.fullmatch(sha)):
        return None
    data = git_bytes(root, 'cat-file', 'commit', sha)
    if data is None:
        return None
    if hashlib.sha1(b'commit %d\0' % len(data) + data).hexdigest() != sha:
        return None
    head = data.split(b'\n\n', 1)[0].decode('utf-8', 'replace').split('\n')
    trees = [ln[5:] for ln in head if ln.startswith('tree ')]
    committer = [ln for ln in head if ln.startswith('committer ')]
    m = re.fullmatch(r'committer .* (\d+) ([+-])(\d\d)(\d\d)', committer[0]) if len(committer) == 1 else None
    if len(trees) != 1 or not HEX40.fullmatch(trees[0]) or m is None:
        return None
    try:
        offset = datetime.timedelta(hours=int(m.group(3)), minutes=int(m.group(4)))
        tz = datetime.timezone(-offset if m.group(2) == '-' else offset)
        date = datetime.datetime.fromtimestamp(int(m.group(1)), tz).date().isoformat()
    except (OverflowError, OSError, ValueError):
        return None
    return {'tree': trees[0], 'parents': [ln[7:] for ln in head if ln.startswith('parent ')], 'date': date}


def git_tree(root, sha):
    """Árbol completo del commit real sha, {ruta: (modo, objeto)}; None si no se puede leer (falla cerrado)."""
    out = git_bytes(root, 'ls-tree', '-r', '-z', '--full-tree', sha)
    if out is None:
        return None
    tree = {}
    for raw in (x for x in out.split(b'\0') if x):
        meta, sep, name = raw.partition(b'\t')
        fields = meta.decode('ascii', 'replace').split(' ')
        if not sep or len(fields) != 3:
            return None
        tree[name.decode('utf-8', 'surrogateescape')] = (fields[0], fields[2])
    return tree


def git_filemode(root):
    """¿Cuenta el bit de ejecución del árbol de trabajo? Como en Git: nunca en Windows ni con core.fileMode=false."""
    code, out = git_run(root, 'config', '--type=bool', '--get', 'core.fileMode')
    return os.name != 'nt' and not (code == 0 and out.strip() == b'false')


def same_blob(data, obj, eol=True):
    """¿Estos bytes del árbol de trabajo son el objeto obj, o su conversión exacta LF→CRLF de un checkout de Git?

    Solo se tolera la conversión completa de un blob sin CR (cada LF pasa a CRLF), como la que hace Git con
    core.autocrlf o eol=crlf. Cualquier otro cambio, aunque sea de un solo fin de línea, es un cambio."""
    if git_blob_id(data) == obj:
        return True
    lf = data.replace(b'\r\n', b'\n')
    return eol and lf != data and b'\r' not in lf and lf.replace(b'\n', b'\r\n') == data and git_blob_id(lf) == obj


def worktree_state(root):
    """Índice y árbol de trabajo vistos sin confiar en la caché ni en las marcas del índice (AF4-M01).

    - index: entradas en etapa 0 del índice, {ruta: (modo, objeto)};
    - dirty: rutas del índice cuyo archivo falta, no es del tipo del índice o no tiene los bytes de su objeto.
      Se calcula aquí, sobre los bytes, nunca con el stat cacheado, assume-unchanged ni skip-worktree;
    - untracked: archivos sin versionar que Git no ignora;
    - problems: lo que hace la vista no fiable: marcas assume-unchanged o skip-worktree, entradas sin fusionar,
      submódulos o modos desconocidos, objetos ausentes o archivos ilegibles.
    Lo que no se puede leer queda en None y añade su problema: falla cerrado."""
    st = {'index': None, 'dirty': None, 'untracked': None, 'problems': []}
    problems = st['problems']
    out = git_bytes(root, 'ls-files', '-z', '-v', '-s')
    if out is None:
        problems.append('no se pudo leer el índice de Git')
        return st
    index = {}
    marks = {'assume-unchanged': [], 'skip-worktree': [], 'sin fusionar (conflicto)': [],
             'submódulo o modo no verificable': []}
    for raw in (x for x in out.split(b'\0') if x):
        meta, sep, name = raw.partition(b'\t')
        fields = meta.decode('ascii', 'replace').split(' ')
        if not sep or len(fields) != 4 or len(fields[0]) != 1:
            problems.append('entrada del índice ilegible')
            return st
        tag, mode, obj, stage = fields
        path = name.decode('utf-8', 'surrogateescape')
        if tag.islower():
            marks['assume-unchanged'].append(path)
        if tag in 'Ss':
            marks['skip-worktree'].append(path)
        if stage != '0':
            marks['sin fusionar (conflicto)'].append(path)
        elif mode not in WORKTREE_MODES or not HEX40.fullmatch(obj):
            marks['submódulo o modo no verificable'].append(path)
        else:
            index[path] = (mode, obj)
    for kind, paths in marks.items():
        if paths:
            problems.append(f'{kind} en {len(paths)} entradas del índice: {sorted(set(paths))[:4]}')
    query = ''.join(f'{obj}\n' for obj in sorted({obj for _, obj in index.values()})).encode('ascii')
    out = git_bytes(root, 'cat-file', '--batch-check=%(objectname) %(objecttype)', stdin=query)
    kinds = dict(ln.split(' ', 1) for ln in (out or b'').decode('ascii', 'replace').splitlines() if ' ' in ln)
    unresolved = sorted(p for p, (_, obj) in index.items() if kinds.get(obj) != 'blob')
    if out is None or unresolved:
        problems.append(f'entradas del índice sin su objeto blob en el repositorio: {unresolved[:4]}')
    filemode = git_filemode(root)
    dirty, unreadable = set(), []
    for path, (mode, obj) in index.items():
        p = Path(root) / path
        try:
            info = p.lstat()
            if mode == '120000' and stat.S_ISLNK(info.st_mode):
                data = os.fsencode(os.readlink(p))
            else:
                data = p.read_bytes() if stat.S_ISREG(info.st_mode) else None
        except (FileNotFoundError, NotADirectoryError):
            data = None
        except (OSError, ValueError):
            unreadable.append(path)
            continue
        if data is None or not same_blob(data, obj, eol=mode != '120000'):
            dirty.add(path)
        elif filemode and mode != '120000' and bool(info.st_mode & stat.S_IXUSR) != (mode == '100755'):
            dirty.add(path)
    if unreadable:
        problems.append(f'archivos versionados ilegibles en el árbol de trabajo: {sorted(unreadable)[:4]}')
    out = git_bytes(root, 'ls-files', '-z', '--others', '--exclude-standard')
    if out is None:
        problems.append('no se pudieron listar los archivos sin versionar')
    else:
        st['untracked'] = {x.decode('utf-8', 'surrogateescape') for x in out.split(b'\0') if x}
    st['index'], st['dirty'] = index, dirty
    return st


def git_state_problems(root):
    """Estado del repositorio que hace ambigua la vista normativa (AF4-M02): refs/replace, injertos y operaciones en
    curso. Lista vacía si no hay ninguno; lo que no se pudo comprobar también es un problema (falla cerrado).

    Las refs/replace no cambian lo que lee el validador (git_run las ignora), pero sí lo que ve quien revisa con
    Git sin --no-replace-objects: esa ambigüedad falla cerrado. Los injertos los aplica Git siempre."""
    problems = []
    out = git_bytes(root, 'for-each-ref', '--format=%(refname)', 'refs/replace/')
    if out is None:
        problems.append('no se pudieron listar las refs/replace')
    elif out.strip():
        refs = sorted(out.decode('utf-8', 'replace').split())
        problems.append(f'refs/replace presentes, que sustituyen objetos en la vista habitual de Git: {refs[:4]}')
    names = ['info/grafts', *GIT_PENDING]
    out = git_bytes(root, 'rev-parse', *[x for name in names for x in ('--git-path', name)])
    paths = out.decode('utf-8', 'replace').splitlines() if out is not None else []
    if len(paths) != len(names):
        return problems + ['no se pudo resolver el directorio de Git']
    for name, rel in zip(names, paths):
        if os.path.lexists(Path(root) / rel):
            problems.append('injertos (info/grafts), que Git aplica aunque se desactiven los reemplazos'
                            if name == 'info/grafts' else f'operación de Git en curso ({name})')
    return problems


def changed_since(root, sha, wt):
    """Rutas en las que el índice o el árbol de trabajo difieren del commit real sha, más las no versionadas.

    Compara objetos (árbol de sha frente al índice) y bytes (árbol de trabajo frente al índice, ya calculados en
    worktree_state): no depende de las marcas del índice ni de su caché de stat. None si algo no se pudo leer."""
    if wt.get('index') is None or wt.get('dirty') is None or wt.get('untracked') is None:
        return None
    tree = git_tree(root, sha)
    if tree is None:
        return None
    index = wt['index']
    staged = {p for p in set(tree) | set(index) if tree.get(p) != index.get(p)}
    return sorted(staged.union(wt['dirty'], wt['untracked']))


def blob_text(blob):
    """Texto de un blob, con los finales de línea normalizados como al leer un archivo de texto; None si no vale."""
    if not isinstance(blob, dict) or not isinstance(blob.get('data'), bytes):
        return None
    try:
        return blob['data'].decode('utf-8').replace('\r\n', '\n').replace('\r', '\n')
    except UnicodeDecodeError:
        return None


def read(root, rel):
    try:
        return (Path(root) / rel).read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError):
        return None


def read_bytes(root, rel):
    try:
        p = Path(root) / rel
        return None if p.is_symlink() or not p.is_file() else p.read_bytes()
    except OSError:
        return None


def json_bytes(data):
    if not isinstance(data, bytes):
        return None
    try:
        return strict_json(data.decode('utf-8'))
    except UnicodeDecodeError:
        return None


def safe_repo_path(path):
    """Ruta relativa de un archivo del repositorio: sin «..», componentes vacíos, barras invertidas ni invisibles."""
    return (isinstance(path, str) and bool(path) and '\\' not in path and '..' not in path.split('/')
            and '' not in path.split('/') and not invisible_chars(path))


def safe_doc_path(path):
    return safe_repo_path(path) and path.startswith('docs/') and path.endswith('.md')


def git_facts(root, sha, wt, problems):
    """Hechos Git del commit candidato real; todo lo no evaluable queda en falso o None (falla cerrado).

    problems: lo que hace ambigua la vista de Git o del árbol de trabajo (AF4); con algo ahí, nada se vincula."""
    f = {'commit': False, 'from_base': False, 'ancestor': False, 'changed': None, 'date': None, 'gate_doc': None,
         'git_state': list(problems)}
    info = git_commit(root, sha)
    if info is None:
        return f
    f['commit'], f['date'] = True, info['date']
    f['from_base'] = git_run(root, 'merge-base', '--is-ancestor', BASE, sha)[0] == 0
    f['ancestor'] = git_run(root, 'merge-base', '--is-ancestor', sha, 'HEAD')[0] == 0
    f['changed'] = changed_since(root, sha, wt)
    f['gate_doc'] = blob_text(git_blob(root, sha, GATE_DOC))
    return f


def collect(root=ROOT):
    """Fotografía de todo lo que evalúan las reglas. Las pruebas la mutan en memoria."""
    texts = {rel: read(root, rel) for rel in PKG_FILES + GOV_FILES + [F33_MATRIX]}
    upstream = {rel: read_bytes(root, rel) for rel in UPSTREAM_FILES}
    tools = {}
    tdir = Path(root) / TOOLS
    if tdir.is_dir():
        for p in sorted(tdir.rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts:
                tools[p.relative_to(root).as_posix()] = read(root, p.relative_to(root).as_posix())
    evidence = {}
    edir = Path(root) / GATE_EVIDENCE
    if edir.exists() or edir.is_symlink():
        if edir.is_symlink() or not edir.is_dir():
            evidence[GATE_EVIDENCE] = None
        else:
            for p in sorted(edir.rglob('*')):
                rel = p.relative_to(root).as_posix()
                if p.is_symlink() or (not p.is_file() and not p.is_dir()):
                    evidence[rel] = None
                elif p.is_file():
                    evidence[rel] = read_bytes(root, rel)
    # Estado de Git y del árbol de trabajo, visto sin refs/replace ni marcas del índice (AF4).
    wt = worktree_state(root)
    git_state = git_state_problems(root) + wt['problems']
    code, branch = git(root, 'rev-parse', '--abbrev-ref', 'HEAD')
    branch = branch.strip() if code == 0 else None
    base_ok = git_run(root, 'merge-base', '--is-ancestor', BASE, 'HEAD')[0] == 0
    changed = changed_since(root, BASE, wt)
    changed = None if changed is None else set(changed)
    base_gov = {rel: blob_text(git_blob(root, BASE, rel)) for rel in GOV_FILES}
    changed_py = {rel: read(root, rel) for rel in sorted(changed or ()) if rel.endswith('.py')}
    # Commits candidatos citados por el estado del gate o por la evidencia, y ADR sucesores citados por FG-12.
    shas, adr_paths = set(), set()
    state = strict_json(texts.get(GATE_STATE) or '')
    if isinstance(state, dict) and isinstance(state.get('candidate_commit'), str):
        shas.add(state['candidate_commit'])
    for data in evidence.values():
        ev = json_bytes(data)
        if isinstance(ev, dict):
            if isinstance(ev.get('candidate_commit'), str):
                shas.add(ev['candidate_commit'])
            adr = ev.get('successor_adr')
            if isinstance(adr, dict) and safe_doc_path(adr.get('path')):
                adr_paths.add(adr['path'])
    candidates = sorted(sha for sha in shas if HEX40.fullmatch(sha))
    facts = {sha: git_facts(root, sha, wt, git_state) for sha in candidates}
    # El ADR se lee del árbol Git de cada commit candidato citado, nunca del árbol de trabajo (AF3-M01).
    adr_blobs = {(sha, p): git_blob(root, sha, p) for sha in candidates for p in sorted(adr_paths)}
    # Lo que Git ignora no puede formar parte de ningún commit: ni evidencia (AF3) ni ninguna otra entrada
    # normativa leída del árbol de trabajo (AF4): paquete, gobierno, herramientas y fuentes F34.
    inputs = [p for src in (texts, upstream, tools, evidence) for p in src if p != GATE_EVIDENCE]
    ignored = git_ignored(root, inputs)
    return {'root': str(root), 'texts': texts, 'upstream': upstream, 'tools': tools, 'evidence': evidence,
            'branch': branch, 'base_ok': base_ok, 'changed': changed, 'base_gov': base_gov,
            'changed_py': changed_py, 'facts': facts, 'adr_blobs': adr_blobs, 'ignored': ignored,
            'git_state': git_state}


def state_block(text):
    """Bloque «Estado vigente» de un documento de gobierno, hasta el siguiente encabezado de nivel 2."""
    if text is None:
        return None
    m = re.search(r'^## Estado vigente[^\n]*\n(.*?)(?=^## )', text, re.M | re.S)
    return m.group(1) if m else None


def bullets(block):
    return [ln[2:].strip() for ln in block.splitlines() if ln.startswith('- ')]


def table_rows(text, prefix):
    rows = []
    for ln in (text or '').splitlines():
        if ln.startswith(f'| {prefix}'):
            rows.append([c.strip() for c in ln.strip().strip('|').split(' | ')])
    return rows


def section(text, heading_prefix):
    m = re.search(rf'^## {re.escape(heading_prefix)}[^\n]*\n(.*?)(?=^## |\Z)', text or '', re.M | re.S)
    return m.group(1) if m else None


# ---------------------------------------------------------------- reglas del paquete

def rule_str(s):
    out = []
    missing = [p for p in PKG_FILES if s['texts'].get(p) is None]
    out.append((not missing, f'paquete completo ({len(PKG_FILES)} archivos); faltan: {missing}'))
    readme = s['texts'].get(f'{PKG}/README.md') or ''
    unlinked = [n for n in PKG_DOCS[1:] if f']({n})' not in readme]
    unlinked += [p for p in PKG_DATA if f']({p[len(PKG) + 1:]})' not in readme]
    out.append((not unlinked, f'el README enlaza todos los artefactos; sin enlace: {unlinked}'))
    return out


def rule_lnk(s):
    root = Path(s['root'])
    broken = []
    texts_by_path = {str((root / k).resolve()): v for k, v in s['texts'].items() if v is not None}
    for rel in [p for p in PKG_FILES if p.endswith('.md')] + GOV_FILES:
        text = s['texts'].get(rel)
        if text is None:
            continue
        links = re.findall(r'\]\(([^)\s]+)\)', text)
        if rel in GOV_FILES:
            # En gobierno solo se verifican los enlaces nuevos, hacia el paquete F36-SBX.
            links = [link for link in links if 'f36-sbx' in link]
        for link in links:
            if re.match(r'^[a-z]+:', link):
                continue
            path, _, anchor = link.partition('#')
            target = (root / rel).parent / path if path else root / rel
            try:
                target = target.resolve()
            except OSError:
                broken.append(f'{rel}→{link}')
                continue
            content = texts_by_path.get(str(target))
            if content is None:
                if not memo('exists', str(target), target.exists):
                    broken.append(f'{rel}→{link}')
                    continue
                if anchor and target.suffix == '.md':
                    content = memo('read', str(target), lambda: target.read_text(encoding='utf-8'))
            if anchor and target.suffix == '.md' and content is not None:
                if anchor not in {slug(h) for h in re.findall(r'^#+ (.+)$', content, re.M)}:
                    broken.append(f'{rel}→{link}')
    return [(not broken, f'enlaces y anclas resueltos; rotos: {broken}')]


def rule_gov(s):
    out = []
    required = sorted(norm(r) for r in REQUIRED_STATE)
    for rel in GOV_FILES:
        block = state_block(s['texts'].get(rel))
        if block is None:
            out.append((False, f'{rel}: sin bloque «Estado vigente» (falla cerrado)'))
            continue
        bl = [norm(b) for b in bullets(block)]
        unknown = sorted(set(bl) - set(required))
        missing = sorted(set(required) - set(bl))
        dup = sorted({b for b in bl if bl.count(b) > 1})
        out.append((not unknown and not missing and not dup,
                    f'{rel}: el estado vigente tiene exactamente las {len(required)} líneas cerradas; '
                    f'desconocidas: {unknown}, ausentes: {missing}, repetidas: {dup}'))
        base_block = state_block(s['base_gov'].get(rel))
        if base_block is None:
            out.append((False, f'{rel}: no se pudo leer el estado vigente de la base {BASE[:7]} (falla cerrado)'))
        else:
            lost = [b for b in (norm(x) for x in bullets(base_block)) if b not in bl]
            out.append((not lost, f'{rel}: conserva todos los estados de la base; perdidos: {lost}'))
    out.append((CLAUDE_MEMBERS in (s['texts'].get('CLAUDE.md') or ''),
                'CLAUDE.md declara exactamente a los tres integrantes que exige el quórum del gate'))
    return out


def allowed_states(subj):
    if subj in ('G0', 'G0 real'):
        return {'NO APROBADA'}
    fixed = {'G0-SBX': {'APROBADA CON RESTRICCIONES'}, 'G0-02': {'PENDIENTE EXTERNO'},
             'G0-03': {'PENDIENTE EXTERNO'}, 'G0-12': {'PENDIENTE EXTERNO'}, 'G0-09': {'CUMPLIDO'},
             'G0-14': {'CUMPLIDO'}, 'ADR-005': {'PROPUESTA'}, 'ADR-005 canónico': {'PROPUESTA'},
             'F35 productiva': {'BLOQUEADA'}, 'F35-SBX': {'CERRADA Y CONGELADA'}, 'F36-SBX': {'EN DISEÑO'},
             'F36-SBX-GATE': {'NO SUPERADO'}}
    if subj in fixed:
        return fixed[subj]
    m = re.match(r'F(\d{2})', subj)
    if m and (int(m.group(1)) >= 36 or '-F' in subj):
        return {'BLOQUEADA', 'BLOQUEADAS', 'BLOQUEADO'}
    if subj.lower().startswith('alcance '):
        return {'BLOQUEADO'}
    if subj.lower() == 'datos reales':
        return {'PROHIBIDOS'}
    return set()


def state_claims(text):
    t = re.sub(r'[*`_]', '', norm(text))
    for rx in (CLAIM_RX, ID_CLAIM_RX):
        for m in rx.finditer(t):
            state = m.group('state').strip()
            if m.group('sep') == '=' or state.split(' ')[0] in STATE_WORDS:
                yield m.group('subj'), state


def forbidden_claims(text):
    # Sin marcado Markdown: «**F37-SBX** = …» no esquiva la regla.
    t = re.sub(r'[*`_]', '', norm(text))
    return [f'{label} «{t[m.start():m.start() + 40].strip()}»' for pattern, label in FORBIDDEN_CLAIMS
            for m in re.finditer(norm(pattern), t)]


def rule_sem(s):
    hits = []
    for rel in PKG_FILES + GOV_FILES:
        text = s['texts'].get(rel)
        if text is not None:
            hits += [f'{rel}: {h}' for h in memo('claims', text, lambda: forbidden_claims(text))]
    out = [(not hits, f'sin afirmaciones de estado prohibidas; encontradas: {hits}')]
    bad = []
    scopes = {p: s['texts'].get(p) for p in PKG_FILES if p.endswith('.md')}
    scopes.update({p: state_block(s['texts'].get(p)) for p in GOV_FILES})
    for rel, text in scopes.items():
        for subj, st in memo('states', text or '', lambda: list(state_claims(text or ''))):
            if st not in allowed_states(subj):
                bad.append(f'{rel}: «{subj} = {st}»')
    out.append((not bad, f'cada afirmación «sujeto = ESTADO» usa un estado admitido para su sujeto; '
                         f'no admitidas: {bad}'))
    sec = section(s['texts'].get(CHARTER) or '', '2. Estados de gobierno')
    rows = {}
    for ln in (sec or '').splitlines():
        cells = [c.strip() for c in ln.strip().strip('|').split(' | ')] if ln.startswith('| ') else []
        if len(cells) == 2 and cells[0] not in ('Estado', '---') and not cells[0].startswith('---'):
            rows[norm(cells[0])] = norm(cells[1])
    tab = [k for k, v in CHARTER_STATES.items() if not rows.get(k, '').startswith(v)]
    extra = sorted(set(rows) - set(CHARTER_STATES))
    out.append((sec is not None and not tab and not extra,
                f'la tabla de estados del charter coincide con el gobierno; distintas: {tab}, desconocidas: {extra}'))
    return out


def f33_classes(text):
    out = {}
    for cells in table_rows(text, 'CAP-'):
        if len(cells) < 3:
            continue
        cls = cells[2].replace('*', '').strip()
        for name in ('BLOQUEADA', 'FUTURA', 'PERMITIDA CON RESTRICCIONES', 'PERMITIDA'):
            if cls.startswith(name):
                out[cells[0]] = name
                break
    return out


def matrix_rows(text):
    rows, bad = {}, []
    for cells in table_rows(text, 'EI-'):
        if len(cells) != 7:
            bad.append(f'{cells[0]}: {len(cells)} columnas')
            continue
        ei, cap_text, cls, scope, caps, cond, stage = cells
        if ei in rows:
            bad.append(ei)
        rows[ei] = {'capacity': cap_text, 'class': cls.replace('*', '').strip(), 'scope': scope,
                    'caps': re.findall(r'CAP-\d\d', caps), 'cond': cond, 'stage': stage}
    return rows, bad


def rule_cap(s):
    out = []
    f33 = f33_classes(s['texts'].get(F33_MATRIX))
    out.append((len(f33) == 37, f'matriz F33 legible: {len(f33)} de 37 CAP'))
    rows, bad = matrix_rows(s['texts'].get(MATRIX))
    out.append((not bad, f'filas EI bien formadas y sin duplicados; problemas: {bad}'))
    out.append((sorted(rows) == EI_IDS, f'EI-01..EI-24 presentes exactamente; hay {sorted(rows)}'))
    pinned = [ei for ei in EI_IDS if ei in rows and (rows[ei]['class'], rows[ei]['scope']) != EXPECTED_MATRIX[ei]]
    out.append((not pinned, f'clase y alcance de cada EI iguales a la matriz fijada; reclasificadas: {pinned}'))
    errs = []
    for ei, r in rows.items():
        if r['class'] not in CLASSES:
            errs.append(f'{ei}: clase desconocida {r["class"]!r}')
            continue
        if r['scope'] not in ('B', 'C', '—'):
            errs.append(f'{ei}: alcance desconocido {r["scope"]!r}')
        for cap in r['caps']:
            if cap not in f33:
                errs.append(f'{ei}: {cap} no existe en F33')
            elif f33[cap] == 'BLOQUEADA' and r['class'] != 'BLOCKED':
                errs.append(f'{ei}: cita {cap} BLOQUEADA en F33 y no es BLOCKED')
            elif f33[cap] == 'FUTURA' and r['class'] == 'ALLOWED':
                errs.append(f'{ei}: cita {cap} FUTURA en F33 y es ALLOWED')
        if r['class'] == 'ALLOWED':
            if r['scope'] != 'B':
                errs.append(f'{ei}: ALLOWED fuera del alcance B')
            low = r['capacity'].lower()
            words = [w for w in NOT_ALLOWED_WORDS if re.search(w, low)]
            if words:
                errs.append(f'{ei}: capacidad ALLOWED que nombra {words}')
    out.append((not errs, f'clases coherentes con F33 y con la frontera B/C; errores: {errs}'))
    blocked_text = ' '.join(r['capacity'].lower() for r in rows.values() if r['class'] == 'BLOCKED')
    unblocked = [t for t in MUST_BLOCK if t not in blocked_text]
    out.append((not unblocked, f'todo lo prohibido está en una fila BLOCKED; sin bloquear: {unblocked}'))
    text = s['texts'].get(MATRIX) or ''
    summary = {}
    for cls in CLASSES:
        m = re.search(rf'^\| {cls} \| ([^|]+) \|$', text, re.M)
        summary[cls] = sorted(re.findall(r'EI-\d\d', m.group(1))) if m else None
    expected = {cls: sorted(k for k, v in rows.items() if v['class'] == cls) for cls in CLASSES}
    out.append((summary == expected, f'el resumen coincide con las filas: {summary} frente a {expected}'))
    return out


# ---------------------------------------------------------------- contrato de evidencia v3

def field_tokens(name):
    return set(name.lower().split('_'))


def contract_semantic_errors(c, root):
    """Invariantes del contrato v3 con mensajes explícitos (el hash fija además todo lo demás)."""
    e = []

    def need(cond, msg):
        if not cond:
            e.append(msg)

    need(list(c) == CONTRACT_KEYS, f'claves de primer nivel distintas del contrato cerrado: '
                                   f'faltan {sorted(set(CONTRACT_KEYS) - set(c))}, sobran {sorted(set(c) - set(CONTRACT_KEYS))}')
    need(c.get('contract_id') == 'f36sbx-evidence-contract' and c.get('contract_version') == '4'
         and c.get('status') == 'DISENO', 'identidad: f36sbx-evidence-contract v4 en estado DISENO')
    need(c.get('canonical_context') == EXPECTED_CANONICAL,
         'contexto canónico: clave application_token, fuente artifacts, los cinco campos de contexto y aplicación a '
         'outputs y tuning_outputs')
    need(c.get('environment') == 'sandbox', 'environment debe ser sandbox')
    need(c.get('source_type_allowed') == ['synthetic'], 'source_type_allowed debe ser exactamente ["synthetic"]')
    need(c.get('generator_policy') == {'llm_allowed': False, 'template_based': True, 'seed_required': True,
                                       'byte_reproducible': True}, 'política del generador distinta: sin LLM, '
                                                                   'con plantillas, semilla y bytes reproducibles')
    up = c.get('allowed_upstream_sources')
    need(isinstance(up, list) and set(up) == ALLOWED_UPSTREAM and len(up) == len(set(up))
         and all((Path(root) / u).is_dir() for u in up), 'fuentes upstream admitidas fuera de la lista cerrada')
    need(c.get('upstream_files') == EXPECTED_UPSTREAM_FILES,
         'archivos upstream distintos de las tres tablas F34 tipadas por tenant, con su contexto y cardinalidad')
    need(c.get('global_upstream_sources') == [], 'fuentes globales: la allowlist debe estar cerrada y vacía en v3')
    need(isinstance(c.get('global_upstream_policy'), str) and c['global_upstream_policy'].strip(),
         'falta la política documentada de fuentes globales')
    need(c.get('upstream_manifest') == F34 + 'manifest.json', 'manifiesto upstream distinto del de F34')
    need(c.get('content_upstream_bindings') == {'criterion_id': F34 + 'criteria.csv'},
         'provenance: falta el vínculo de criterion_id con criteria.csv')
    need(c.get('tenant_bound_tokens') == TENANT_TOKENS, 'tokens ligados al tenant: author_token y annotator_token')
    need(c.get('internal_references') == INTERNAL_REFERENCES,
         'referencias internas: fragment_id a fragments, variant_of y rendered_from a artifacts')
    gid = c.get('global_identifiers') if isinstance(c.get('global_identifiers'), dict) else None
    need(gid is not None and list(gid) == ['question_id'] and all(
        isinstance(v, dict) and set(v) == {'scope', 'personal', 'resolved_upstream', 'semantics'}
        and v['scope'] == 'global' and v['personal'] is False and v['resolved_upstream'] is False
        and isinstance(v['semantics'], str) and v['semantics'].strip() for v in gid.values()),
         'identificadores globales: solo question_id, tipado, no personal, sin resolución upstream y documentado')
    need(isinstance(c.get('forbidden_upstream_sources'), list)
         and REQUIRED_FORBIDDEN_SOURCES <= set(c['forbidden_upstream_sources']),
         f'fuentes prohibidas incompletas: deben incluir {sorted(REQUIRED_FORBIDDEN_SOURCES)}')
    need(c.get('synthetic_markers') == MARKERS, 'marcadores synthetic-only distintos de los exigidos')
    pats = c.get('identifier_patterns') if isinstance(c.get('identifier_patterns'), dict) else {}
    for key in ('artifact_id', 'fragment_id', 'output_id'):
        need(isinstance(pats.get(key), str) and pats[key].startswith('^SBX36-(ORG-S[1-3])-'),
             f'patrón {key}: debe fijar el prefijo SBX36- y la organización sintética')
    need(pats.get('author_token') == '^EV-(S[1-3])-[0-9]{2}$'
         and pats.get('annotator_token') == '^ANT36-(S[1-3])-[0-9]{2}$',
         'patrones de autor y anotador: deben fijar el tenant en su grupo S1..S3')
    for key, value in pats.items():
        try:
            re.compile(value)
        except (re.error, TypeError):
            e.append(f'patrón {key} no compila')
    enums = c.get('enums') if isinstance(c.get('enums'), dict) else {}
    for key, value in enums.items():
        need(isinstance(value, list) and value and all(isinstance(x, str) and x for x in value)
             and len(value) == len(set(value)), f'enumerado {key}: lista no vacía de valores únicos')
        need(not (isinstance(value, list) and 'train' in value), f'enumerado {key}: contiene train')
    need(enums.get('partition') == ['dev', 'test'], 'partition: solo dev y test')
    need(enums.get('author_kind') == ['human_synthetic'], 'author_kind: solo human_synthetic')
    need(enums.get('review_status') == ['revisada_sintetica'], 'review_status: solo revisada_sintetica')
    need(enums.get('transcript_kind') == ['texto_sintetico_revisado'], 'transcript_kind: solo texto sintético revisado')
    need(enums.get('stage') == ['A', 'B'], 'stage: solo A y B')
    need(enums.get('normalization') == ['nfkc_casefold'], 'normalization: solo nfkc_casefold')
    need(set(enums.get('observation_kind') or []) <= {'conducta_observada', 'aclaracion'},
         'observation_kind: solo conducta observada o aclaración, nunca una inferencia')
    need(set(enums.get('format') or []) <= {'pdf', 'docx'}, 'format: solo pdf o docx')
    types = c.get('artifact_types') if isinstance(c.get('artifact_types'), dict) else {}
    need(enums.get('artifact_type') == list(ARTIFACT_TYPES) and list(types) == list(ARTIFACT_TYPES),
         f'tipos de artefacto distintos de los ocho cerrados: {list(types)}')
    cft = c.get('content_field_types') if isinstance(c.get('content_field_types'), dict) else {}
    for field, kind in cft.items():
        ok = kind in ('text', 'list') or (isinstance(kind, str) and (
            (kind.startswith('enum:') and kind[5:] in enums) or (kind.startswith('pattern:') and kind[8:] in pats)))
        need(ok, f'tipo de campo de contenido desconocido: {field} = {kind!r}')
    # Todo identificador con patrón del contenido tiene exactamente una clase: tenant, upstream, interno o global.
    classes = [set(c.get('tenant_bound_tokens') or []), set(c.get('content_upstream_bindings') or {}),
               set(c.get('internal_references') or {}), set(gid or {})]
    pattern_fields = {f for f, k in cft.items() if isinstance(k, str) and k.startswith('pattern:')}
    need(set().union(*classes) == pattern_fields and sum(map(len, classes)) == len(pattern_fields),
         f'identificadores del contenido sin clase única (tenant, upstream, interno o global): '
         f'{sorted(pattern_fields ^ set().union(*classes))}')
    record_fields = []
    for name, spec in types.items():
        if not isinstance(spec, dict) or set(spec) != {'stage', 'content_fields', 'list_items', 'text_paths',
                                                       'fragmentable'}:
            e.append(f'{name}: especificación con claves distintas del contrato')
            continue
        need(spec['stage'] == ARTIFACT_TYPES.get(name), f'{name}: etapa distinta de la fijada')
        cf = spec['content_fields'] if isinstance(spec['content_fields'], list) else []
        need(bool(cf) and all(f in cft for f in cf), f'{name}: campos de contenido sin tipo declarado')
        items = spec['list_items'] if isinstance(spec['list_items'], dict) else {}
        need(all(cft.get(k) == 'list' and k in cf and all(x in cft for x in v) for k, v in items.items())
             and all(k in items for k in cf if cft.get(k) == 'list'), f'{name}: listas sin estructura cerrada')
        need(isinstance(spec['fragmentable'], bool) and spec['fragmentable'] == bool(spec['text_paths']),
             f'{name}: fragmentable incoherente con text_paths')
        need(('grupo_sintetico' in cf) == (name == 'counterfactual_pair'), f'{name}: marcador de grupo fuera de lugar')
        record_fields += cf + [x for v in items.values() for x in v]
    need(c.get('artifact_envelope_fields') == ENVELOPE, 'sobre del artefacto distinto del cerrado: exige record_hash')
    need(c.get('fragment_fields') == FRAGMENT_FIELDS, 'campos del fragmento distintos: la cadena exige artifact_id, '
                                                      'artifact_record_hash, text_path, offsets, text_hash y fragment_hash')
    need(c.get('output_fields') == OUTPUT_FIELDS, 'campos del output distintos: exige method_config, fragment_refs, '
                                                  'fragment_ref_hashes, abstained, input_manifest_hash y output_hash, '
                                                  'sin texto ni puntaje')
    need(c.get('method_config_fields') == ['normalization', 'top_k'] and c.get('top_k_range') == [1, 20],
         'configuración del método distinta de {normalization, top_k 1..20}')
    need(c.get('context_fields') == CONTEXT, 'campos de contexto distintos de organización, escenario, vacante, '
                                             'postulación y partición')
    need(c.get('output_ei') == ['EI-07', 'EI-09', 'EI-10'] and all(
        EXPECTED_CLASSES.get(x) in ('ALLOWED', 'CONDITIONAL') for x in c.get('output_ei') or []),
         'output_ei: solo las EI de localización EI-07, EI-09 y EI-10')
    prov = c.get('provenance_fields') if isinstance(c.get('provenance_fields'), dict) else {}
    need(prov == {'artifact': PROVENANCE, 'upstream_ref': ['source', 'ref', 'sha256']},
         'provenance: faltan campos obligatorios del artefacto o de la referencia upstream')
    need(c.get('example_fields') == ['example_id', 'contract_version', 'example_only', 'note', 'artifacts',
                                     'fragments', 'outputs', 'partition_manifest'], 'campos del ejemplo distintos')
    need(c.get('example_id_value') == 'f36sbx-contract-example', 'identificador cerrado del ejemplo distinto')
    need(c.get('example_coverage') == EXPECTED_COVERAGE, 'cobertura mínima del ejemplo distinta de la exigida')
    need(c.get('partition_manifest_fields') == ['partitions', 'thresholds', 'test_used_for_tuning']
         and c.get('partition_fields') == {'dev': ['artifacts'],
                                           'test': ['artifacts', 'sealed', 'seal_algorithm', 'seal_sha256']}
         and c.get('threshold_fields') == ['tuning_partition', 'tuning_outputs'],
         'manifiesto de particiones distinto: test debe estar sellado con el sello v2 y los umbrales, ajustados con dev')
    hs = c.get('hash_scheme') if isinstance(c.get('hash_scheme'), dict) else {}
    need(all(isinstance(hs.get(k), dict) and hs[k].get('tag') == tag for k, tag in EXPECTED_HASH_TAGS.items())
         and all(isinstance(hs.get(k), str) for k in ('canonical_json', 'tagged_hash', 'content_hash', 'text_hash')),
         'esquema de hashes distinto: etiquetas de registro, fragmento, manifiesto, output y sello v2')
    need(isinstance(c.get('relations'), dict) and sorted(c['relations']) == REL_IDS
         and all(isinstance(v, str) and v for v in c['relations'].values()), 'relaciones REL-01..REL-15 incompletas')
    need(c.get('group_marker_only_in') == ['counterfactual_pair'], 'el marcador de grupo solo va en counterfactual_pair')
    forb = c.get('forbidden_fields') if isinstance(c.get('forbidden_fields'), list) else []
    need(REQUIRED_FORBIDDEN_FIELDS <= set(forb), f'campos prohibidos incompletos: '
                                                 f'faltan {sorted(REQUIRED_FORBIDDEN_FIELDS - set(forb))}')
    toks = c.get('forbidden_field_tokens') if isinstance(c.get('forbidden_field_tokens'), list) else []
    need(REQUIRED_FORBIDDEN_TOKENS <= set(toks), f'tokens prohibidos incompletos: '
                                                 f'faltan {sorted(REQUIRED_FORBIDDEN_TOKENS - set(toks))}')
    record_fields += ENVELOPE + FRAGMENT_FIELDS + OUTPUT_FIELDS + PROVENANCE + [
        'source', 'ref', 'sha256', 'partitions', 'thresholds', 'tuning_partition', 'tuning_outputs', 'sealed',
        'seal_algorithm', 'seal_sha256', 'artifacts', 'normalization', 'top_k']
    leaked = sorted({f for f in record_fields if f in forb or field_tokens(f) & set(toks)})
    need(not leaked, f'campos de registro prohibidos o con tokens prohibidos: {leaked}')
    need(c.get('splits') == EXPECTED_SPLITS, 'garantías de partición distintas: solo dev y test, train prohibido, '
                                             'separación por familia y vacante, test sellado con el sello v2, '
                                             'umbrales en dev, test sin ajuste, embargo temporal y pares en la '
                                             'misma partición')
    return e


def load_upstream(c, upstream):
    """Tablas F34 indexadas por su clave y hashes (manifiesto, archivo); None si algo no se puede leer."""
    try:
        files = json.loads(upstream[c['upstream_manifest']].decode('utf-8'))['files']
        tables, hashes = {}, {}
        for path, spec in c['upstream_files'].items():
            data = upstream[path]
            declared = (files.get(path.rsplit('/', 1)[1]) or {}).get('sha256')
            hashes[path] = (declared, sha256(data))
            key = spec['key']
            tables[path] = {r[key]: r for r in csv.DictReader(io.StringIO(data.decode('utf-8'))) if key in r}
        return tables, hashes
    except Exception:  # noqa: BLE001 — una tabla ilegible falla cerrado
        return None


def bundle_errors(c, ex, upstream):
    """Invariantes REL-01..REL-15 de un conjunto de registros frente al contrato. Lista vacía = conforme."""
    errs = []
    try:
        _bundle(c, ex, upstream, errs.append)
    except Exception as exc:  # noqa: BLE001 — cualquier error de evaluación falla cerrado
        errs.append(f'registros no evaluables: {exc.__class__.__name__} (falla cerrado)')
    return errs


def _bundle(c, ex, upstream, add):
    up = load_upstream(c, upstream)
    if up is None:
        add('REL-02 tablas o manifiesto F34 ilegibles (falla cerrado)')
        return
    tables, hashes = up
    for path, (declared, actual) in hashes.items():
        if declared != actual:
            add(f'REL-02 {path}: hash distinto del declarado en el manifiesto F34')
    src_by_key = {spec['key']: path for path, spec in c['upstream_files'].items()}
    app_src, vac_src = src_by_key.get('application_token'), src_by_key.get('vacancy_token')
    cri_src = c['content_upstream_bindings'].get('criterion_id')
    if app_src not in tables or vac_src not in tables or cri_src not in tables:
        add('REL-02 el contrato no vincula la postulación, la vacante y el criterio con tablas F34 (falla cerrado)')
        return
    if not isinstance(ex, dict):
        add('REL-01 ejemplo: JSON inválido, vacío o con claves duplicadas')
        return
    if set(ex) != set(c['example_fields']):
        add(f'REL-01 ejemplo: campos distintos del contrato: {sorted(set(ex) ^ set(c["example_fields"]))}')
    prefix = c['synthetic_markers']['text_prefix']
    if ex.get('example_id') != c['example_id_value']:
        add(f'REL-14 ejemplo: example_id debe ser exactamente {c["example_id_value"]!r}')
    if ex.get('example_only') is not True or ex.get('contract_version') != c['contract_version'] \
            or not isinstance(ex.get('note'), str) or not ex['note'].startswith(prefix) or invisible_chars(ex['note']):
        add('REL-01 ejemplo: debe declararse solo ejemplo, de la versión del contrato y [SINTÉTICO]')
    pats = {k: re.compile(v) for k, v in c['identifier_patterns'].items()}
    enums, types, cft = c['enums'], c['artifact_types'], c['content_field_types']
    lists = {}
    for key in ('artifacts', 'fragments', 'outputs'):
        value = ex.get(key)
        if not isinstance(value, list) or not all(isinstance(x, dict) for x in value):
            add(f'REL-01 ejemplo: {key} debe ser una lista de objetos')
            value = [x for x in value if isinstance(x, dict)] if isinstance(value, list) else []
        lists[key] = value
    ids = [r.get(k) for key, k in (('artifacts', 'synthetic_id'), ('fragments', 'fragment_id'),
                                   ('outputs', 'output_id')) for r in lists[key]]
    dup = sorted({str(i) for i in ids if ids.count(i) > 1})
    if dup:
        add(f'REL-03 identificadores repetidos: {dup}')
    arts = {a.get('synthetic_id'): a for a in lists['artifacts'] if isinstance(a.get('synthetic_id'), str)}
    vac_scenario = {}
    for a in arts.values():
        vac_scenario.setdefault(a.get('vacancy_token'), a.get('scenario_id'))

    def check_org(rid, kind, org, label):
        m = pats[kind].fullmatch(rid) if isinstance(rid, str) else None
        if not m:
            add(f'REL-01 {label}: identificador {rid!r} fuera de patrón')
        elif m.group(1) != org:
            add(f'REL-03 {label}: el identificador es de {m.group(1)} y el registro de {org!r}')

    def check_context(rec, label):
        if rec.get('synthetic_organization_id') not in c['synthetic_markers']['synthetic_organization_ids']:
            add(f'REL-01 {label}: organización sintética desconocida {rec.get("synthetic_organization_id")!r}')
        for field in ('scenario_id', 'vacancy_token', 'application_token'):
            if not (isinstance(rec.get(field), str) and pats[field].fullmatch(rec[field])):
                add(f'REL-01 {label}: {field} fuera de patrón')
        part = rec.get('partition')
        if part in c['splits']['forbidden_partitions']:
            add(f'REL-11 {label}: partición {part!r} prohibida')
        elif part not in enums['partition']:
            add(f'REL-11 {label}: partición desconocida {part!r}')
        vac = tables[vac_src].get(rec.get('vacancy_token')) if isinstance(rec.get('vacancy_token'), str) else None
        app = tables[app_src].get(rec.get('application_token')) \
            if isinstance(rec.get('application_token'), str) else None
        if vac is None:
            add(f'REL-04 {label}: la vacante {rec.get("vacancy_token")!r} no existe en F34')
        elif vac.get('organization_token') != rec.get('synthetic_organization_id'):
            add(f'REL-04 {label}: la vacante F34 es de otra organización')
        if app is None:
            add(f'REL-04 {label}: la postulación {rec.get("application_token")!r} no existe en F34')
        elif (app.get('vacancy_token'), app.get('organization_token')) != (rec.get('vacancy_token'),
                                                                            rec.get('synthetic_organization_id')):
            add(f'REL-04 {label}: la postulación F34 es de otra vacante u organización')

    def check_text(label, where, value):
        if not isinstance(value, str) or not value.startswith(prefix):
            add(f'REL-12 {label}: {where} sin el prefijo [SINTÉTICO]')
        elif not unicodedata.is_normalized('NFC', value):
            add(f'REL-12 {label}: {where} no está en NFC')
        elif invisible_chars(value):
            add(f'REL-12 {label}: {where} contiene caracteres invisibles o de control')
        elif any(p.search(value) for p, _ in PII_PATTERNS):
            add(f'REL-12 {label}: {where} contiene un patrón de PII')
        elif len(value) > 4000:
            add(f'REL-12 {label}: {where} supera 4000 caracteres')

    def check_value(label, field, value, spec, where):
        kind = cft.get(field)
        if kind == 'text':
            check_text(label, f'{where}{field}', value)
        elif kind == 'list':
            item_fields = spec['list_items'].get(field)
            if not isinstance(value, list) or not value or item_fields is None:
                add(f'REL-01 {label}: {where}{field} debe ser una lista no vacía')
                return
            for i, item in enumerate(value):
                if not isinstance(item, dict) or set(item) != set(item_fields):
                    add(f'REL-01 {label}: {where}{field}/{i} con campos distintos de {item_fields}')
                    continue
                for sub in item_fields:
                    check_value(label, sub, item[sub], spec, f'{where}{field}/{i}/')
        elif isinstance(kind, str) and kind.startswith('enum:'):
            if not isinstance(value, str) or value not in enums[kind[5:]]:
                add(f'REL-01 {label}: {where}{field} con valor desconocido {value!r}')
        elif isinstance(kind, str) and kind.startswith('pattern:'):
            if not (isinstance(value, str) and pats[kind[8:]].fullmatch(value)):
                add(f'REL-01 {label}: {where}{field} fuera de patrón')
        else:
            add(f'REL-01 {label}: campo de contenido desconocido {where}{field}')

    def ref_context(src, row):
        """Contexto del registro F34 citado: organización, vacante, postulación y escenario del ejemplo."""
        spec = c['upstream_files'][src]
        ctx = {dim: row.get(col) for dim, col in spec['context'].items()}
        if 'vacancy' in ctx and 'organization' not in ctx:
            vrow = tables[vac_src].get(ctx['vacancy'])
            ctx['organization'] = vrow.get('organization_token') if vrow else None
        if 'vacancy' in ctx and ctx['vacancy'] in vac_scenario:
            ctx['scenario'] = vac_scenario[ctx['vacancy']]
        return ctx

    dims = {'organization': ('synthetic_organization_id', 'de otra organización'),
            'scenario': ('scenario_id', 'de otro escenario'), 'vacancy': ('vacancy_token', 'de otra vacante'),
            'application': ('application_token', 'de otra postulación')}

    # REL-01, REL-02, REL-04, REL-12 y REL-13: cada artefacto.
    for a in lists['artifacts']:
        aid = a.get('synthetic_id', '?')
        label = f'artefacto {aid}'
        if set(a) != set(c['artifact_envelope_fields']):
            add(f'REL-01 {label}: sobre distinto del contrato: faltan '
                f'{sorted(set(c["artifact_envelope_fields"]) - set(a))}, sobran {sorted(set(a) - set(c["artifact_envelope_fields"]))}')
        check_org(aid, 'artifact_id', a.get('synthetic_organization_id'), label)
        t = a.get('artifact_type')
        spec = types.get(t) if isinstance(t, str) else None
        if spec is None:
            add(f'REL-01 {label}: artifact_type desconocido {t!r}')
        elif a.get('stage') != spec['stage']:
            add(f'REL-01 {label}: etapa {a.get("stage")!r} distinta de la del tipo')
        check_context(a, label)
        if not (isinstance(a.get('template_family'), str) and pats['template_family'].fullmatch(a['template_family'])):
            add(f'REL-01 {label}: template_family fuera de patrón')
        if a.get('source_type') not in c['source_type_allowed']:
            add(f'REL-01 {label}: source_type desconocido {a.get("source_type")!r}')
        if a.get('environment') != c['environment']:
            add(f'REL-01 {label}: environment distinto de sandbox')
        if a.get('hash_algorithm') != c['synthetic_markers']['hash_algorithm']:
            add(f'REL-01 {label}: hash_algorithm distinto del marcador')
        content = a.get('content')
        if not isinstance(content, dict):
            add(f'REL-01 {label}: content ausente o mal formado')
        elif spec is not None:
            if set(content) != set(spec['content_fields']):
                add(f'REL-01 {label}: contenido distinto del tipo: faltan '
                    f'{sorted(set(spec["content_fields"]) - set(content))}, sobran {sorted(set(content) - set(spec["content_fields"]))}')
            for field in spec['content_fields']:
                if field in content:
                    check_value(label, field, content[field], spec, '')
            for field in c['tenant_bound_tokens']:
                m = pats[field].fullmatch(content[field]) if isinstance(content.get(field), str) else None
                if field in content and m and f'ORG-{m.group(1)}' != a.get('synthetic_organization_id'):
                    add(f'REL-13 {label}: {field} {content[field]!r} es de ORG-{m.group(1)}, no de la organización '
                        f'del artefacto (cross-tenant)')
        if not (isinstance(content, dict) and a.get('content_hash') == sha256(canonical(content))):
            add(f'REL-01 {label}: content_hash incorrecto')
        if a.get('record_hash') != artifact_record_hash(a):
            add(f'REL-01 {label}: record_hash incorrecto: el registro cambió sin recalcular su hash')
        p = a.get('provenance')
        if not isinstance(p, dict):
            add(f'REL-02 {label}: provenance ausente o mal formada')
            continue
        if set(p) != set(c['provenance_fields']['artifact']):
            add(f'REL-02 {label}: provenance distinta del contrato: faltan '
                f'{sorted(set(c["provenance_fields"]["artifact"]) - set(p))}, sobran {sorted(set(p) - set(c["provenance_fields"]["artifact"]))}')
        if not (isinstance(p.get('generator_id'), str) and pats['generator_id'].fullmatch(p['generator_id'])
                and isinstance(p.get('generator_version'), str) and pats['semver'].fullmatch(p['generator_version'])):
            add(f'REL-02 {label}: generador o versión fuera de patrón')
        mt = pats['template_id'].fullmatch(p['template_id']) if isinstance(p.get('template_id'), str) else None
        mf = pats['template_family'].fullmatch(a['template_family']) \
            if isinstance(a.get('template_family'), str) else None
        if not mt or not mf or mt.group(1) != mf.group(1) or p.get('template_family') != a.get('template_family'):
            add(f'REL-02 {label}: la plantilla de la provenance no pertenece a la familia del artefacto')
        if type(p.get('seed')) is not int or p['seed'] < 0:
            add(f'REL-02 {label}: semilla ausente o inválida')
        if p.get('content_hash') != a.get('content_hash'):
            add(f'REL-02 {label}: el content_hash de la provenance no es el del artefacto')
        refs = p.get('upstream_refs')
        if not isinstance(refs, list) or not refs:
            add(f'REL-02 {label}: sin referencias upstream')
            refs = []
        seen, per_source = set(), {}
        for r in refs:
            if not isinstance(r, dict) or set(r) != set(c['provenance_fields']['upstream_ref']):
                add(f'REL-02 {label}: referencia upstream mal formada')
                continue
            src, ref = r['source'], r['ref']
            if not isinstance(src, str) or not isinstance(ref, str) or (src, ref) in seen:
                add(f'REL-02 {label}: referencia upstream repetida o inválida')
                continue
            seen.add((src, ref))
            if src not in c['upstream_files']:
                kind = 'global no admitida (allowlist cerrada)' if src not in c['global_upstream_sources'] else 'global'
                add(f'REL-13 {label}: fuente upstream {kind}: {src!r}')
                continue
            per_source.setdefault(src, []).append(ref)
            if r['sha256'] != hashes[src][0] or r['sha256'] != hashes[src][1]:
                add(f'REL-02 {label}: hash de {src} distinto del manifiesto F34 o del archivo')
            row = tables[src].get(ref)
            if row is None:
                add(f'REL-02 {label}: {ref!r} no existe en {src}')
                continue
            ctx = ref_context(src, row)
            for dim, (field, wording) in dims.items():
                if dim in ctx and ctx[dim] != a.get(field):
                    add(f'REL-13 {label}: referencia upstream {ref!r} {wording} ({ctx[dim]!r} frente a {a.get(field)!r})')
        for src, spec_src in c['upstream_files'].items():
            got = per_source.get(src, [])
            if spec_src['cardinality'] == 'exactly_one_own':
                own = a.get(spec_src['key'])
                if got != [own]:
                    add(f'REL-02 {label}: debe citar exactamente su {spec_src["key"]} en {src}; cita {got}')
        if isinstance(content, dict):
            for field, src in c['content_upstream_bindings'].items():
                if field in content and content[field] not in per_source.get(src, []):
                    add(f'REL-02 {label}: falta la referencia upstream de content.{field}')

    # REL-05: aislamiento de vacante, postulación, familia y partición.
    def unique(key, value, message):
        seen = {}
        for a in arts.values():
            seen.setdefault(key(a), set()).add(value(a))
        for k, vs in sorted(seen.items(), key=lambda kv: str(kv[0])):
            if len(vs) > 1:
                add(f'REL-05 {message} {k}: {sorted(map(str, vs))}')
    unique(lambda a: a.get('vacancy_token'), lambda a: (a.get('synthetic_organization_id'), a.get('scenario_id')),
           'vacante mezclada entre organizaciones o escenarios')
    unique(lambda a: a.get('application_token'),
           lambda a: (a.get('synthetic_organization_id'), a.get('scenario_id'), a.get('vacancy_token')),
           'postulación mezclada entre organizaciones, escenarios o vacantes')
    unique(lambda a: a.get('template_family'), lambda a: a.get('partition'), 'familia de plantilla en varias particiones')
    unique(lambda a: a.get('vacancy_token'), lambda a: a.get('partition'), 'vacante en varias particiones')

    # REL-06: fragmentos.
    frs = {}
    for f in lists['fragments']:
        fid = f.get('fragment_id', '?')
        label = f'fragmento {fid}'
        if set(f) != set(c['fragment_fields']):
            add(f'REL-06 {label}: campos distintos del contrato: faltan {sorted(set(c["fragment_fields"]) - set(f))}, '
                f'sobran {sorted(set(f) - set(c["fragment_fields"]))}')
        check_org(fid, 'fragment_id', f.get('synthetic_organization_id'), label)
        if isinstance(fid, str):
            frs[fid] = f
        if f.get('fragment_hash') != fragment_record_hash(f):
            add(f'REL-06 {label}: fragment_hash incorrecto: el fragmento cambió sin recalcular su hash')
        a = arts.get(f.get('artifact_id'))
        if a is None:
            add(f'REL-06 {label}: referencia un artefacto inexistente {f.get("artifact_id")!r}')
            continue
        if f.get('artifact_record_hash') != a.get('record_hash'):
            add(f'REL-06 {label}: artifact_record_hash no es el record_hash vigente de su artefacto')
        spec = types.get(a.get('artifact_type'))
        if not spec or not spec['fragmentable']:
            add(f'REL-06 {label}: su artefacto no es fragmentable')
            continue
        for k in c['context_fields']:
            if f.get(k) != a.get(k):
                add(f'REL-06 {label}: mezcla de {k} con su artefacto ({f.get(k)!r} frente a {a.get(k)!r})')
        text = resolve_text(a.get('content'), f.get('text_path'), spec['text_paths'])
        if text is None:
            add(f'REL-06 {label}: text_path {f.get("text_path")!r} no apunta a un texto del artefacto')
            continue
        s0, s1 = f.get('char_start'), f.get('char_end')
        if type(s0) is not int or type(s1) is not int or not 0 <= s0 < s1 <= len(text):
            add(f'REL-06 {label}: offsets fuera del texto')
        elif f.get('text_hash') != sha256(text[s0:s1].encode('utf-8')):
            add(f'REL-06 {label}: text_hash incorrecto')

    # REL-15: contexto canónico de cada postulación, el de sus artefactos del conjunto. Es la única fuente del
    # contexto de un output: también de una abstención, que no cita fragmentos, y de un output de ajuste.
    canon_spec = c['canonical_context']
    canon = {}
    for a in arts.values():
        canon.setdefault(a.get(canon_spec['key']), set()).add(tuple(a.get(k) for k in canon_spec['fields']))

    def canonical_errors(rec, label):
        expected = canon.get(rec.get(canon_spec['key']))
        if not expected:
            return [f'REL-15 {label}: su postulación {rec.get(canon_spec["key"])!r} no tiene artefactos en el conjunto: '
                    f'el output no tiene contexto canónico']
        if len(expected) != 1:
            return [f'REL-15 {label}: el contexto canónico de su postulación es ambiguo (falla cerrado)']
        errs = []
        for k, val in zip(canon_spec['fields'], next(iter(expected))):
            if rec.get(k) != val:
                errs.append(f'REL-15 {label}: {k} {rec.get(k)!r} distinto del contexto canónico de su postulación '
                            f'({val!r})')
        return errs

    # REL-07: outputs.
    outs = {}
    mc_fields = c['method_config_fields']
    k_min, k_max = c['top_k_range']
    for o in lists['outputs']:
        oid = o.get('output_id', '?')
        label = f'output {oid}'
        if set(o) != set(c['output_fields']):
            add(f'REL-07 {label}: campos distintos del contrato: faltan {sorted(set(c["output_fields"]) - set(o))}, '
                f'sobran {sorted(set(o) - set(c["output_fields"]))}')
        check_org(oid, 'output_id', o.get('synthetic_organization_id'), label)
        check_context(o, label)
        for err in canonical_errors(o, label):
            add(err)
        if isinstance(oid, str):
            outs[oid] = o
        if o.get('output_hash') != output_record_hash(o):
            add(f'REL-07 {label}: output_hash incorrecto: el output cambió sin recalcular su hash')
        ei = o.get('ei')
        if ei not in c['output_ei']:
            add(f'REL-07 {label}: EI {ei!r} no admitida para outputs'
                + (' (BLOCKED)' if EXPECTED_CLASSES.get(ei) == 'BLOCKED' else ''))
        if not (isinstance(o.get('method_id'), str) and pats['method_id'].fullmatch(o['method_id'])
                and isinstance(o.get('method_version'), str) and pats['semver'].fullmatch(o['method_version'])):
            add(f'REL-07 {label}: método o versión fuera de patrón')
        mc = o.get('method_config')
        if not isinstance(mc, dict) or set(mc) != set(mc_fields) or mc.get('normalization') not in enums['normalization'] \
                or type(mc.get('top_k')) is not int or not k_min <= mc['top_k'] <= k_max:
            add(f'REL-07 {label}: method_config fuera de la configuración cerrada')
        row = tables[cri_src].get(o.get('query_criterion_id')) if isinstance(o.get('query_criterion_id'), str) else None
        if row is None or row.get('vacancy_token') != o.get('vacancy_token'):
            add(f'REL-07 {label}: el criterio de la consulta no existe en F34 o es de otra vacante')
        refs = o.get('fragment_refs')
        if not isinstance(refs, list) or not all(isinstance(r, str) for r in refs) or len(set(refs)) != len(refs):
            add(f'REL-07 {label}: fragment_refs debe ser una lista de identificadores únicos')
            refs = [r for r in refs if isinstance(r, str)] if isinstance(refs, list) else []
        for r in refs:
            f = frs.get(r)
            if f is None:
                add(f'REL-07 {label}: referencia un fragmento inexistente {r!r}')
                continue
            for k in c['context_fields']:
                if f.get(k) != o.get(k):
                    add(f'REL-07 {label}: mezcla de {k} con el fragmento {r}')
        ref_hashes = o.get('fragment_ref_hashes')
        if ref_hashes != [(frs.get(r) or {}).get('fragment_hash') for r in refs]:
            add(f'REL-07 {label}: fragment_ref_hashes no coincide con los fragment_hash vigentes de sus fragmentos')
        ab = o.get('abstained')
        if type(ab) is not bool:
            add(f'REL-07 {label}: abstained debe ser booleano')
        elif ab != (len(refs) == 0):
            add(f'REL-07 {label}: la abstención no coincide con la ausencia de fragmentos')
        if o.get('input_manifest_hash') != input_manifest_hash(lists['fragments'], o.get('application_token'),
                                                               o.get('partition')):
            add(f'REL-07 {label}: input_manifest_hash incorrecto')

    # REL-08, REL-09 y REL-10: referencias entre artefactos.
    for aid, a in arts.items():
        content = a.get('content') if isinstance(a.get('content'), dict) else {}
        t = a.get('artifact_type')
        label = f'artefacto {aid}'
        if t == 'relevance_annotation':
            f = frs.get(content.get('fragment_id')) if isinstance(content.get('fragment_id'), str) else None
            if f is None:
                add(f'REL-08 {label}: la anotación referencia un fragmento inexistente')
            else:
                for k in c['context_fields']:
                    if f.get(k) != a.get(k):
                        add(f'REL-08 {label}: mezcla de {k} con el fragmento anotado')
            row = tables[cri_src].get(content.get('criterion_id')) if isinstance(content.get('criterion_id'), str) else None
            if row is None or row.get('vacancy_token') != a.get('vacancy_token'):
                add(f'REL-08 {label}: el criterio no existe en F34 o es de otra vacante')
        elif t == 'counterfactual_pair':
            b = arts.get(content.get('variant_of')) if isinstance(content.get('variant_of'), str) else None
            if b is None or b is a:
                add(f'REL-09 {label}: la variante referencia un artefacto inexistente')
            elif not types.get(b.get('artifact_type'), {}).get('fragmentable'):
                add(f'REL-09 {label}: la variante no es un artefacto fragmentable')
            else:
                for k in ('synthetic_organization_id', 'scenario_id', 'vacancy_token', 'partition', 'template_family'):
                    if b.get(k) != a.get(k):
                        add(f'REL-09 {label}: mezcla de {k} con su variante')
        elif t == 'rendered_document':
            b = arts.get(content.get('rendered_from')) if isinstance(content.get('rendered_from'), str) else None
            if b is None or b.get('artifact_type') != 'cv_document':
                add(f'REL-10 {label}: el origen no existe o no es un cv_document')
            else:
                for k in c['context_fields'] + ['template_family']:
                    if b.get(k) != a.get(k):
                        add(f'REL-10 {label}: mezcla de {k} con su origen')

    # REL-11: manifiesto de particiones, sello v2 de test y ajuste solo con dev.
    pm = ex.get('partition_manifest')
    if not isinstance(pm, dict) or set(pm) != set(c['partition_manifest_fields']):
        add('REL-11 manifiesto de particiones ausente o con campos distintos del contrato')
        return
    parts = pm['partitions']
    if not isinstance(parts, dict):
        add('REL-11 particiones mal formadas')
        return
    for name in parts:
        if name not in c['splits']['partitions']:
            kind = 'prohibida' if name in c['splits']['forbidden_partitions'] else 'desconocida'
            add(f'REL-11 partición {kind} en el manifiesto: {name!r}')
    if set(parts) != set(c['splits']['partitions']):
        add('REL-11 el manifiesto debe declarar exactamente dev y test')
    listed = {}
    for name, spec in parts.items():
        expected = c['partition_fields'].get(name)
        if expected is None:
            continue
        if not isinstance(spec, dict) or set(spec) != set(expected):
            add(f'REL-11 partición {name}: campos distintos de {expected}')
            continue
        pids = spec['artifacts']
        if not isinstance(pids, list) or not all(isinstance(i, str) for i in pids) or len(set(pids)) != len(pids):
            add(f'REL-11 partición {name}: lista de artefactos inválida')
            continue
        for i in pids:
            if i in listed:
                add(f'REL-11 {i} figura en dos particiones')
            listed[i] = name
            if i not in arts:
                add(f'REL-11 partición {name}: artefacto inexistente {i!r}')
            elif arts[i].get('partition') != name:
                add(f'REL-11 {i} está en {name} y declara {arts[i].get("partition")!r}')
    missing = sorted(set(arts) - set(listed))
    if missing:
        add(f'REL-11 artefactos fuera del manifiesto: {missing}')
    th = pm['thresholds']
    tuning = []
    if not isinstance(th, dict) or set(th) != set(c['threshold_fields']):
        add('REL-11 umbrales mal formados')
    else:
        if th['tuning_partition'] != c['splits']['thresholds_fit_on']:
            add(f'REL-11 umbrales ajustados en {th["tuning_partition"]!r}: solo se ajusta con dev')
        if not isinstance(th['tuning_outputs'], list) or len(set(map(str, th['tuning_outputs']))) != len(th['tuning_outputs']):
            add('REL-11 tuning_outputs debe ser una lista sin repetidos')
        else:
            tuning = th['tuning_outputs']
            for x in tuning:
                if x not in outs:
                    add(f'REL-11 output de ajuste inexistente {x!r}')
                elif outs[x].get('partition') != 'dev':
                    add(f'REL-11 el output de ajuste {x} es de {outs[x].get("partition")!r}: test no puede ajustar')
                else:
                    # La partición que cuenta es la canónica de su postulación, no la que declara el output.
                    exp = canon.get(outs[x].get(canon_spec['key'])) or set()
                    parts_of = {dict(zip(canon_spec['fields'], ctx)).get('partition') for ctx in exp}
                    if parts_of != {c['splits']['thresholds_fit_on']}:
                        add(f'REL-11 el output de ajuste {x} no es de dev por el contexto canónico de su postulación '
                            f'({sorted(map(str, parts_of))})')
    if pm['test_used_for_tuning'] is not False:
        add('REL-11 test_used_for_tuning debe ser false')
    test = parts.get('test')
    if isinstance(test, dict) and set(test) == set(c['partition_fields']['test']):
        if test['sealed'] is not True:
            add('REL-11 la partición test no está sellada')
        if test['seal_algorithm'] != c['splits']['seal_algorithm']:
            add('REL-11 algoritmo de sello distinto del sello v2')
        if isinstance(th, dict) and set(th) == set(c['threshold_fields']) and isinstance(th['tuning_outputs'], list):
            if test['seal_sha256'] != test_seal(ex, c['contract_version']):
                add('REL-11 el sello de test no coincide: un registro, fragmento u output de test, un output de ajuste '
                    'o los umbrales cambiaron sin volver a sellar')

    # REL-14: cobertura mínima del ejemplo.
    cov = c['example_coverage']
    present = {a.get('artifact_type') for a in arts.values()}
    test_arts = [a for a in arts.values() if a.get('partition') == 'test']
    checks = [
        (set(cov['artifact_types']) <= present, f'faltan tipos de artefacto {sorted(set(cov["artifact_types"]) - present)}'),
        (len(frs) >= cov['min_fragments'], 'sin fragmentos suficientes'),
        (sum(1 for o in outs.values() if o.get('fragment_refs')) >= cov['min_outputs_with_fragments'],
         'sin outputs con fragmentos'),
        (sum(1 for o in outs.values() if o.get('abstained') is True) >= cov['min_abstained_outputs'],
         'sin outputs con abstención'),
        (len(test_arts) >= cov['min_test_artifacts'], 'test sin artefactos'),
        (sum(1 for a in test_arts if a.get('artifact_type') == 'relevance_annotation') >= cov['min_test_gold_annotations'],
         'test sin anotaciones de oro'),
        (sum(1 for o in outs.values() if o.get('partition') == 'test') >= cov['min_test_outputs'], 'test sin outputs'),
        (len(tuning) >= cov['min_tuning_outputs'], 'sin outputs de ajuste en dev'),
        (len({a.get('scenario_id') for a in arts.values()}) >= cov['min_scenarios'], 'menos de dos escenarios'),
    ]
    for cond, msg in checks:
        if not cond:
            add(f'REL-14 cobertura mínima del ejemplo: {msg}')


def rule_ctr(s):
    out = []
    c = strict_json(s['texts'].get(CONTRACT) or '')
    if not isinstance(c, dict):
        return [(False, 'contrato de evidencia: JSON inválido o con claves duplicadas (falla cerrado)')]
    digest = sha256(canonical(c))
    out.append((digest == CONTRACT_SHA256, f'contrato idéntico a la versión cerrada v4 (SHA-256 canónico '
                                           f'{digest[:12]}, esperado {CONTRACT_SHA256[:12]})'))
    errs = contract_semantic_errors(c, s['root'])
    out.append((not errs, f'invariantes del contrato: solo sintético, cerrado, hashes, provenance y particiones; '
                          f'errores: {errs}'))
    if errs:
        out.append((False, 'ejemplo de conformidad no evaluado: el contrato no es válido (falla cerrado)'))
        return out
    ex = strict_json(s['texts'].get(EXAMPLE) or '')
    berrs = bundle_errors(c, ex, s['upstream'])
    out.append((not berrs, f'ejemplo de conformidad conforme a REL-01..REL-15; errores: {berrs}'))
    return out


def rule_thr(s):
    rows = table_rows(s['texts'].get(THREATS), 'TEI-')
    ids = [r[0] for r in rows]
    out = [(ids == TEI_IDS, f'TEI-01..TEI-22 en orden y sin huecos; hay {ids}')]
    weak = [r[0] for r in rows if len(r) != 6 or any(not c or c in ('—', '-') for c in (r[4], r[5]))]
    out.append((not weak, f'cada amenaza tiene control y comportamiento fail-closed; incompletas: {weak}'))
    text = ' '.join(r[1].lower() for r in rows if len(r) == 6)
    missing = [t for t in THREAT_TOPICS if t not in text]
    out.append((not missing, f'el modelo cubre los temas exigidos; faltan: {missing}'))
    return out


def rule_eva(s):
    text = s['texts'].get(PLAN) or ''
    mrows = table_rows(text, 'M-')
    rrows = table_rows(text, 'R-')
    out = [([r[0] for r in mrows] == M_IDS, f'M-01..M-13 presentes; hay {[r[0] for r in mrows]}'),
           ([r[0] for r in rrows] == R_IDS, f'R-01..R-05 presentes; hay {[r[0] for r in rrows]}')]
    covered = set()
    for r in mrows:
        if len(r) > 1:
            covered |= set(re.findall(r'EI-\d\d', r[1]))
    needed = sorted(k for k, v in EXPECTED_CLASSES.items() if v in ('ALLOWED', 'CONDITIONAL'))
    uncovered = [e for e in needed if e not in covered]
    out.append((not uncovered, f'cada EI ALLOWED o CONDITIONAL tiene métrica; sin métrica: {uncovered}'))
    blocked = sorted(e for e in covered if EXPECTED_CLASSES.get(e) not in ('ALLOWED', 'CONDITIONAL'))
    out.append((not blocked, f'ninguna EI BLOCKED o desconocida tiene métrica; con métrica: {blocked}'))
    m = re.search(r'^## 6\. Resultados\n+(.*)', text, re.M | re.S)
    out.append((bool(m) and m.group(1).strip().startswith('**No hay resultados.**'),
                'el plan declara que no hay resultados'))
    return out


def rule_frz(s):
    out = [(s['branch'] in BRANCHES, f'rama admitida: {s["branch"]}'),
           (s['base_ok'], f'la base {BASE[:7]} es ancestro de HEAD')]
    # AF4: con una vista de Git ambigua (marcas del índice, conflictos, operaciones en curso, refs/replace o
    # injertos) no se puede afirmar nada sobre el alcance ni sobre el vínculo con un candidato.
    problems = s['git_state']
    out.append((problems == [], f'estado Git fiable: sin assume-unchanged ni skip-worktree, conflictos, operaciones '
                                f'en curso, refs/replace ni injertos; problemas: {problems}'))
    ignored = s['ignored']
    unversioned = ['no se pudo comprobar con Git (falla cerrado)'] if ignored is None else \
        [p for p in ignored if not p.startswith(GATE_EVIDENCE)]
    out.append((not unversioned, f'las entradas normativas leídas del árbol de trabajo son versionables (Git no '
                                 f'ignora ninguna); ignoradas: {unversioned}'))
    changed = s['changed']
    if changed is None:
        out.append((False, 'estado Git desconocido: no se puede verificar el alcance (falla cerrado)'))
        return out
    allowed = [p for p in changed if p.startswith(PKG + '/') or p.startswith(TOOLS + '/') or p in GOV_FILES]
    outside = sorted(set(changed) - set(allowed))
    out.append((not outside, f'cambios solo en el paquete, sus herramientas y el gobierno ({len(changed)}); '
                             f'fuera de alcance: {outside}'))
    runtime = sorted(p for p in changed if p.startswith(RUNTIME_PREFIXES) or p in DEPENDENCY_FILES)
    out.append((not runtime, f'0 cambios de runtime, producto o dependencias; encontrados: {runtime}'))
    frozen = sorted(p for p in changed if p.startswith(F35_FROZEN))
    out.append((not frozen, f'F35-SBX, G0 y los antecedentes congelados intactos; tocados: {frozen}'))
    return out


def tool_errors(rel, src):
    try:
        tree = ast.parse(src or '')
    except SyntaxError:
        return [f'{rel}: no se puede analizar']
    errs = []
    for node in ast.walk(tree):
        names = []
        if isinstance(node, ast.Import):
            names = [a.name.split('.')[0] for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            names = [(node.module or '').split('.')[0]]
        errs += [f'{rel}: importa {n}' for n in names if n not in STDLIB and n not in LOCAL_MODULES]
    if '\x08' in (src or ''):
        errs.append(f'{rel}: contiene bytes de retroceso (0x08), que anulan patrones como \\b')
    return errs


def rule_dep(s):
    errs = []
    for rel, src in sorted(s['tools'].items()):
        if rel.endswith('.py'):
            errs += memo('dep', (rel, src), lambda: tool_errors(rel, src))
    for rel, src in sorted(s['changed_py'].items()):
        errs += [f'{rel}: importa {m.group(1)} (ML, NLP o red)' for m in ML_IMPORT.finditer(src or '')]
    return [(not errs, f'solo biblioteca estándar y ningún import de ML, NLP o red; encontrados: {sorted(set(errs))}')]


def rule_pii(s):
    hits = []
    scope = {p: s['texts'].get(p) for p in PKG_FILES}
    scope.update({p: t for p, t in s['tools'].items() if p.endswith('.py')})
    scope.update({p: b.decode('utf-8', 'replace') for p, b in s['evidence'].items() if isinstance(b, bytes)})
    scope.update({f'{p} ({sha[:12]})': b['data'].decode('utf-8', 'replace') for (sha, p), b in s['adr_blobs'].items()
                  if isinstance(b, dict) and isinstance(b.get('data'), bytes)})
    for rel, text in scope.items():
        if text:
            hits += [f'{rel}: {label}' for label in memo('pii', text, lambda: [
                label for pattern, label in PII_PATTERNS if pattern.search(text)])]
    return [(not hits, f'sin patrones de PII en el paquete, sus herramientas, la evidencia ni el ADR citado; '
                       f'encontrados: {hits}')]


# ---------------------------------------------------------------- evidencia de equipo y gate

def team_schema_errors(sch):
    """Invariantes del esquema de evidencia de equipo (su hash fija además todo lo demás)."""
    if not isinstance(sch, dict):
        return ['esquema ilegible']
    e = []

    def need(cond, msg):
        if not cond:
            e.append(msg)
    crit = sch.get('criteria') if isinstance(sch.get('criteria'), dict) else {}
    get = lambda fg, k: (crit.get(fg) or {}).get(k)  # noqa: E731
    need(sch.get('schema_tag') == TEAM_SCHEMA_TAG and sch.get('gate_id') == 'F36-SBX-GATE'
         and sch.get('gate_version') == GATE_VERSION, 'identidad del esquema y del gate')
    need(sch.get('evidence_paths') == {fg: f'{GATE_EVIDENCE}{fg}.json' for fg in FG_TEAM},
         'rutas fijas de la evidencia de FG-02, FG-03, FG-10 y FG-12')
    need(sch.get('team_members') == list(MEMBERS), 'lista cerrada de los tres integrantes')
    need((sch.get('candidate_binding') or {}).get('descends_from') == BASE, 'el candidato desciende de la base')
    vi = sch.get('visible_identity') if isinstance(sch.get('visible_identity'), dict) else {}
    need(vi.get('min_letters') == 3 and vi.get('max_length') == 120 and 'autenticada' in str(vi.get('limit')),
         'identidad visible: mínimo 3 letras, máximo 120 caracteres y límite documentado')
    hd = sch.get('human_document') if isinstance(sch.get('human_document'), dict) else {}
    need(hd.get('min_letters_outside_block') == 200, 'documento humano: mínimo 200 letras fuera del bloque canónico')
    ap = sch.get('approvals') if isinstance(sch.get('approvals'), dict) else {}
    need(ap.get('required_vote') == 'APRUEBA' and ap.get('quorum') == '3/3', 'aprobación explícita con quórum 3/3')
    need(set(get('FG-02', 'passing_verdicts') or []) <= {'APROBADO_PARA_INTEGRACION', 'APROBADO_CON_OBSERVACIONES'}
         and set(get('FG-02', 'must_be_zero') or []) >= {'blocker', 'high', 'medium_requiring_fix'},
         'FG-02: solo veredictos aprobatorios y cero BLOCKER, HIGH y MEDIUM que requiere corrección')
    need(get('FG-02', 'report_block') == 'f36sbx-audit-metadata'
         and get('FG-02', 'report_metadata_schema') == 'f36sbx-audit-report/v1'
         and set(get('FG-02', 'coherence') or []) >= {'candidate_commit', 'auditor', 'verdict', 'findings_open'}
         and bool(get('FG-02', 'report_headings')),
         'FG-02: bloque canónico del informe y coherencia exacta con el registro')
    need(get('FG-03', 'passing_decision') == 'AUTORIZA_INICIO_F37_SBX'
         and get('FG-03', 'authorizable_classes') == ['ALLOWED', 'CONDITIONAL'],
         'FG-03: autorización explícita y solo EI ALLOWED o CONDITIONAL')
    need(get('FG-10', 'passing_approval_status') == 'APROBADA'
         and str(get('FG-10', 'version_pattern') or '').startswith('^==')
         and get('FG-10', 'dependency_ei') == ['EI-10', 'EI-11', 'EI-12'],
         'FG-10: dependencias aprobadas, con versión exacta y solo para EI-10, EI-11 y EI-12')
    need(get('FG-12', 'passing_adr_status') == 'APROBADO' and get('FG-12', 'coverable_ei') == SCOPE_C_CONDITIONAL
         and get('FG-12', 'ei09_passing_decision') == 'CABE_EN_ALCANCE_B'
         and not any(re.fullmatch(str(get('FG-12', 'adr_id_pattern') or ''), f'ADR-00{i}') for i in range(1, 6)),
         'FG-12: ADR sucesor APROBADO y distinto de ADR-001..ADR-005, cobertura solo de EI CONDITIONAL de alcance C')
    need(get('FG-12', 'adr_block') == 'f36sbx-adr-metadata' and get('FG-12', 'adr_metadata_schema') == 'f36sbx-adr/v1'
         and bool(get('FG-12', 'adr_headings'))
         and {'gate_id', 'gate_version', 'base_commit'} <= set(get('FG-12', 'adr_metadata_fields') or [])
         and 'applies_to_candidate_commit' not in (get('FG-12', 'adr_metadata_fields') or []),
         'FG-12: bloque canónico del ADR, con contexto de gate, versión y base (nunca el commit que lo contiene)')
    need('candidate_commit' in (get('FG-02', 'report_metadata_fields') or []),
         'FG-02: los metadatos del informe nombran el commit candidato auditado')
    return e


def doc_status_only(old, new):
    """El documento del gate solo cambió en la columna Estado de la tabla FG."""
    if old is None or new is None:
        return False
    a, b = old.split('\n'), new.split('\n')
    if len(a) != len(b):
        return False
    for x, y in zip(a, b):
        if x == y:
            continue
        cx = [c.strip() for c in x.strip().strip('|').split(' | ')]
        cy = [c.strip() for c in y.strip().strip('|').split(' | ')]
        if not (x.startswith('| FG-') and y.startswith('| FG-') and len(cx) == len(cy) == 5 and cx[:4] == cy[:4]
                and cy[4] in STATUSES):
            return False
    return True


def binding_errors(sha, facts, gate_doc):
    """Vínculo reproducible con el candidato: commit de la rama, ancestro de HEAD y sin cambios materiales después."""
    if not isinstance(sha, str) or not HEX40.fullmatch(sha):
        return ['candidate_commit fuera de formato (40 hexadecimales en minúscula)']
    f = facts.get(sha)
    if not isinstance(f, dict):
        return [f'sin datos Git del candidato {sha[:12]} (falla cerrado)']
    e = []
    if not f.get('commit'):
        e.append(f'{sha[:12]} no es un commit del repositorio')
    if not f.get('from_base'):
        e.append(f'{sha[:12]} no desciende de la base {BASE[:7]}')
    if not f.get('ancestor'):
        e.append(f'{sha[:12]} no es ancestro de HEAD')
    gs = f.get('git_state')
    if not isinstance(gs, list) or gs:
        e.append(f'estado Git no fiable: el vínculo con el candidato no es evaluable (falla cerrado): {gs}')
    changed = f.get('changed')
    if changed is None:
        e.append('cambios posteriores al candidato no evaluables (falla cerrado)')
    else:
        outside = sorted(p for p in changed if not (p.startswith(GATE_EVIDENCE) or p in (GATE_STATE, GATE_DOC)))
        if outside:
            e.append(f'el paquete cambió después del commit auditado: {outside[:6]}')
        if GATE_DOC in changed and not doc_status_only(f.get('gate_doc'), gate_doc):
            e.append('el documento del gate cambió fuera de la columna Estado de la tabla FG')
    if parse_date(f.get('date')) is None:
        e.append('fecha del commit candidato ilegible')
    return e


def human_document(data, label, block_info, headings, min_letters):
    """Documento humano con un único bloque canónico: devuelve (metadatos, texto exterior, errores)."""
    if not isinstance(data, bytes) or not data.strip():
        return None, '', [f'{label}: no existe o está vacío']
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError:
        return None, '', [f'{label}: no es UTF-8']
    e = []
    if not unicodedata.is_normalized('NFC', text):
        e.append(f'{label}: no está en NFC')
    bad = invisible_chars(text, allow_layout=True)
    if bad:
        e.append(f'{label}: contiene caracteres invisibles o de control {[f"U+{ord(c):04X}" for c in bad[:3]]}')
    fences = list(FENCE_RX.finditer(text))
    mine = [m for m in fences if m.group('info').strip() == block_info]
    others = [m for m in fences if m not in mine and 'f36sbx' in m.group('info').casefold()]
    if len(mine) != 1:
        return None, text, e + [f'{label}: debe contener exactamente un bloque «{block_info}» (hay {len(mine)})']
    if others:
        e.append(f'{label}: otro bloque f36sbx ambiguo además del canónico')
    m = mine[0]
    meta = strict_json(m.group('body'))
    outside = text[:m.start()] + text[m.end():]
    if not isinstance(meta, dict):
        e.append(f'{label}: el bloque canónico no es un objeto JSON válido sin claves duplicadas')
        meta = None
    lines = [ln.strip() for ln in outside.splitlines() if ln.strip()]
    if not lines or not lines[0].startswith('# '):
        e.append(f'{label}: debe empezar con un título de nivel 1')
    missing = [h for h in headings if h not in lines]
    if missing:
        e.append(f'{label}: faltan las secciones {missing}')
    letters = sum(1 for ch in outside if unicodedata.category(ch).startswith('L'))
    if letters < min_letters:
        e.append(f'{label}: contenido humano insuficiente fuera del bloque ({letters} letras, mínimo {min_letters})')
    return meta, outside, e


def approval_errors(fg, ev, ctx, cdate, rdate):
    rule, members = ctx['schema']['approvals'], ctx['schema']['team_members']
    ap = ev.get('approvals')
    if not isinstance(ap, list):
        return [f'{fg}: approvals debe ser una lista']
    e, names = [], []
    for i, a in enumerate(ap):
        if not isinstance(a, dict) or set(a) != set(rule['fields']):
            e.append(f'{fg}: aprobación {i} con campos distintos de {rule["fields"]}')
            continue
        names.append(a['member'])
        if a['member'] not in members:
            e.append(f'{fg}: integrante no reconocido {a["member"]!r} (se exige la identidad exacta)')
        if a['vote'] not in rule['votes']:
            e.append(f'{fg}: voto desconocido {a["vote"]!r}')
        elif a['vote'] != rule['required_vote']:
            e.append(f'{fg}: {a["member"]} no aprueba ({a["vote"]})')
        d = parse_date(a['date'])
        if d is None or (cdate and d < cdate) or (rdate and d > rdate):
            e.append(f'{fg}: fecha de aprobación de {a["member"]!r} inválida o fuera del registro')
    if len(names) != len(set(map(str, names))):
        e.append(f'{fg}: integrante duplicado en las aprobaciones')
    approving = {a['member'] for a in ap if isinstance(a, dict) and a.get('member') in members
                 and a.get('vote') == rule['required_vote']}
    if approving != set(members) or len(ap) != len(members):
        e.append(f'{fg}: quórum incompleto {len(approving)}/{len(members)}')
    if ev.get('quorum') != rule['quorum']:
        e.append(f'{fg}: quorum declarado distinto de {rule["quorum"]}')
    return e


def authorized_list_errors(fg, lst, ctx):
    allowed = ctx['schema']['criteria']['FG-03']['authorizable_classes']
    if not isinstance(lst, list) or not lst:
        return [f'{fg}: falta la lista explícita y cerrada de EI autorizadas']
    e = []
    if len({str(x) for x in lst}) != len(lst):
        e.append(f'{fg}: EI repetidas')
    for x in lst:
        cls = ctx['classes'].get(x) if isinstance(x, str) else None
        if cls is None:
            e.append(f'{fg}: EI desconocida o fuera de la matriz {x!r}')
        elif cls not in allowed:
            e.append(f'{fg}: {x} es {cls}: no se puede autorizar')
    return e


def findings_errors(fo, c, label):
    if not isinstance(fo, dict) or set(fo) != set(c['findings_fields']):
        return [f'{label}: findings_open con campos distintos del esquema']
    e = []
    for k in c['findings_fields']:
        n = fo[k]
        if type(n) is not int or n < 0:
            e.append(f'{label}: findings_open.{k} debe ser un entero no negativo')
        elif k in c['must_be_zero'] and n:
            e.append(f'{label}: {k} abiertos = {n}')
    return e


def auditor_errors(au, c, label):
    if not isinstance(au, dict) or set(au) != set(c['auditor_fields']):
        return [f'{label}: auditor con campos distintos del esquema']
    e = identity_errors(au['name'], f'{label}: identidad del auditor')
    if au['kind'] not in c['auditor_kinds']:
        e.append(f'{label}: tipo de auditor desconocido {au["kind"]!r}')
    if au['independent_of_candidate'] is not True:
        e.append(f'{label}: el auditor no se declara independiente del candidato')
    return e


def fg02_errors(ev, ctx, cdate, rdate):
    c, e = ctx['schema']['criteria']['FG-02'], []
    min_letters = ctx['schema']['human_document']['min_letters_outside_block']
    e += auditor_errors(ev.get('auditor'), c, 'FG-02')
    verdict = ev.get('verdict')
    if verdict not in c['verdicts']:
        e.append(f'FG-02: veredicto desconocido {verdict!r}')
    elif verdict not in c['passing_verdicts']:
        e.append(f'FG-02: veredicto {verdict}: no aprueba el candidato')
    e += findings_errors(ev.get('findings_open'), c, 'FG-02')
    rep = ev.get('audit_report')
    if not isinstance(rep, dict) or set(rep) != set(c['audit_report_fields']):
        return e + ['FG-02: referencia al informe de auditoría mal formada']
    p = rep['path']
    if not (isinstance(p, str) and p.startswith(GATE_EVIDENCE) and p.endswith('.md')
            and '..' not in p.split('/') and '\\' not in p):
        return e + ['FG-02: el informe debe ser un .md dentro de gate/evidencia/']
    data = ctx['evidence'].get(p)
    if not isinstance(data, bytes) or sha256(data) != rep['sha256']:
        return e + ['FG-02: el informe de auditoría no existe o su SHA-256 es distinto del declarado']
    meta, outside, derr = human_document(data, 'FG-02: informe', c['report_block'], c['report_headings'], min_letters)
    e += derr
    for token in c['verdicts']:
        if token in outside:
            e.append(f'FG-02: informe: el token canónico {token} aparece fuera del bloque (segunda fuente)')
    if COUNT_ASSERTION_RX.search(outside) or VERDICT_ASSERTION_RX.search(outside):
        e.append('FG-02: informe: aserciones de veredicto o de recuentos fuera del bloque canónico (segunda fuente)')
    if meta is None:
        return e
    if set(meta) != set(c['report_metadata_fields']):
        return e + [f'FG-02: informe: metadatos con campos distintos: faltan '
                    f'{sorted(set(c["report_metadata_fields"]) - set(meta))}, sobran {sorted(set(meta) - set(c["report_metadata_fields"]))}']
    if meta['metadata_schema'] != c['report_metadata_schema'] or meta['gate_id'] != ctx['schema']['gate_id'] \
            or meta['gate_version'] != ctx['schema']['gate_version'] or meta['criterion_id'] != 'FG-02':
        e.append('FG-02: informe: metadatos de otro esquema, gate, versión o criterio (otro contexto)')
    if meta['candidate_commit'] != ev.get('candidate_commit'):
        e.append('FG-02: informe: el commit de los metadatos no es el candidato del registro')
    # Coherencia exacta: se comparan los JSON canónicos, para que 1 y true o 0 y false no pasen por iguales.
    e += auditor_errors(meta['auditor'], c, 'FG-02: informe')
    if canonical(meta['auditor']) != canonical(ev.get('auditor')):
        e.append('FG-02: informe: el auditor de los metadatos no coincide con el del registro')
    if canonical(meta['verdict']) != canonical(verdict):
        e.append(f'FG-02: informe: el veredicto del informe ({meta["verdict"]!r}) no coincide con el del registro '
                 f'({verdict!r})')
    e += findings_errors(meta['findings_open'], c, 'FG-02: informe')
    if canonical(meta['findings_open']) != canonical(ev.get('findings_open')):
        e.append('FG-02: informe: los recuentos de hallazgos del informe no coinciden con los del registro')
    d = parse_date(meta['report_date'])
    if d is None or (cdate and d < cdate) or (rdate and d > rdate):
        e.append('FG-02: informe: report_date inválida o fuera del intervalo del candidato y del registro')
    return e


def fg03_errors(ev, ctx, cdate, rdate):
    c, e = ctx['schema']['criteria']['FG-03'], []
    if ev.get('decision') not in c['decisions']:
        e.append(f'FG-03: decisión desconocida {ev.get("decision")!r}')
    elif ev['decision'] != c['passing_decision']:
        e.append('FG-03: el equipo no autoriza el inicio de F37-SBX')
    if ev.get('numbering_f36_m01') not in c['numbering_values']:
        e.append('FG-03: falta la confirmación de la numeración F36-M01')
    elif ev['numbering_f36_m01'] != c['passing_numbering']:
        e.append('FG-03: numeración F36-M01 no confirmada')
    e += authorized_list_errors('FG-03', ev.get('authorized_ei'), ctx)
    if ev.get('authorized_ei') != ctx['state'].get('f37_authorized_ei'):
        e.append('FG-03: authorized_ei distinta de f37_authorized_ei del estado del gate')
    return e + approval_errors('FG-03', ev, ctx, cdate, rdate)


def fg03_list(ctx):
    """EI autorizadas por una FG-03 válida; None si FG-03 no tiene evidencia válida."""
    if team_evidence_errors('FG-03', ctx):
        return None
    return json_bytes(ctx['evidence'].get(ctx['schema']['evidence_paths']['FG-03']))['authorized_ei']


def fg10_errors(ev, ctx, cdate, rdate):
    c, e = ctx['schema']['criteria']['FG-10'], []
    auth = fg03_list(ctx)
    if auth is None:
        e.append('FG-10: requiere una autorización FG-03 válida')
        auth = []
    nd, deps = ev.get('new_dependencies'), ev.get('dependencies')
    if type(nd) is not bool:
        e.append('FG-10: new_dependencies debe ser booleano')
    if not isinstance(deps, list):
        e.append('FG-10: dependencies debe ser una lista')
        deps = []
    need = sorted(set(auth) & set(c['dependency_ei']))
    if nd is False and deps:
        e.append('FG-10: declara que no hay dependencias nuevas y lista dependencias')
    if nd is False and need:
        e.append(f'FG-10: {need} requieren dependencias registradas y aprobadas')
    if nd is True and not deps:
        e.append('FG-10: declara dependencias nuevas y no lista ninguna')
    names, covered = [], set()
    for i, d in enumerate(deps):
        if not isinstance(d, dict) or set(d) != set(c['dependency_fields']):
            e.append(f'FG-10: dependencia {i} con estructura desconocida o incompleta')
            continue
        n = d['name']
        if not (isinstance(n, str) and re.fullmatch(c['name_pattern'], n)):
            e.append(f'FG-10: dependencia {i} con nombre inválido')
            continue
        names.append(n.lower())
        if not (isinstance(d['version'], str) and re.fullmatch(c['version_pattern'], d['version'])):
            e.append(f'FG-10: {n}: versión no fijada con == exacto')
        purpose = d['purpose']
        if not isinstance(purpose, str) or invisible_chars(purpose) or not 10 <= len(purpose.strip()) <= 300 \
                or sum(1 for ch in purpose if unicodedata.category(ch).startswith('L')) < 10:
            e.append(f'FG-10: {n}: propósito ausente, genérico o con caracteres invisibles')
        if d['license'] not in c['licenses']:
            e.append(f'FG-10: {n}: licencia fuera de la lista admitida')
        if d['source'] not in c['sources']:
            e.append(f'FG-10: {n}: origen no admitido')
        if d['source_url'] != c['source_url_template'].format(name=n):
            e.append(f'FG-10: {n}: URL de origen distinta de la canónica')
        sc = d['supply_chain_review']
        if not isinstance(sc, dict) or set(sc) != set(c['supply_chain_fields']):
            e.append(f'FG-10: {n}: revisión de cadena de suministro mal formada')
        else:
            od = parse_date(sc['osv_checked_on'])
            if od is None or (cdate and od < cdate) or (rdate and od > rdate):
                e.append(f'FG-10: {n}: fecha de la consulta OSV inválida')
            if type(sc['open_vulnerabilities']) is not int or sc['open_vulnerabilities'] != 0:
                e.append(f'FG-10: {n}: vulnerabilidades abiertas o recuento inválido')
            if not (isinstance(sc['artifact_sha256'], str) and HEX64.fullmatch(sc['artifact_sha256'])):
                e.append(f'FG-10: {n}: SHA-256 del artefacto inválido')
            if sc['reviewed_by'] not in ctx['schema']['team_members']:
                e.append(f'FG-10: {n}: revisor no reconocido')
        rel = d['related_ei']
        if not isinstance(rel, list) or not rel or len({str(x) for x in rel}) != len(rel):
            e.append(f'FG-10: {n}: EI relacionadas ausentes o repetidas')
        else:
            for x in rel:
                if x not in auth:
                    e.append(f'FG-10: {n}: {x!r} no está entre las EI autorizadas por FG-03')
                elif x not in c['dependency_ei']:
                    e.append(f'FG-10: {n}: {x} no justifica dependencias nuevas')
                else:
                    covered.add(x)
        if d['approval_status'] not in c['approval_statuses']:
            e.append(f'FG-10: {n}: estado de aprobación desconocido')
        elif d['approval_status'] != c['passing_approval_status']:
            e.append(f'FG-10: {n}: dependencia no APROBADA ({d["approval_status"]})')
    if len(names) != len(set(names)):
        e.append('FG-10: dependencias repetidas')
    if nd is True and set(need) - covered:
        e.append(f'FG-10: {sorted(set(need) - covered)} sin dependencia aprobada que las cubra')
    return e + approval_errors('FG-10', ev, ctx, cdate, rdate)


def fg12_errors(ev, ctx, cdate, rdate):
    c, e = ctx['schema']['criteria']['FG-12'], []
    min_letters = ctx['schema']['human_document']['min_letters_outside_block']
    auth = fg03_list(ctx)
    if auth is None:
        e.append('FG-12: requiere una autorización FG-03 válida')
        auth = []
    need = sorted(x for x in auth if x in c['coverable_ei'])
    cov = ev.get('covered_ei')
    if not isinstance(cov, list) or len({str(x) for x in cov}) != len(cov):
        e.append('FG-12: covered_ei debe ser una lista sin repetidos')
        cov = []
    for x in cov:
        cls = ctx['classes'].get(x) if isinstance(x, str) else None
        if cls is None:
            e.append(f'FG-12: EI desconocida {x!r}')
        elif cls == 'BLOCKED':
            e.append(f'FG-12: intenta autorizar {x}, que es BLOCKED')
        elif x not in c['coverable_ei']:
            e.append(f'FG-12: {x} no es una EI CONDITIONAL de alcance C')
    d09 = ev.get('ei09_decision')
    if d09 not in c['ei09_decisions']:
        e.append('FG-12: falta la decisión explícita sobre EI-09')
    elif 'EI-09' in auth and d09 != c['ei09_passing_decision']:
        e.append(f'FG-12: EI-09 autorizada sin la decisión {c["ei09_passing_decision"]}')
    adr = ev.get('successor_adr')
    if adr is None:
        if need:
            e.append(f'FG-12: {need} exigen un ADR sucesor APROBADO')
        if cov:
            e.append('FG-12: covered_ei sin ADR sucesor')
        return e + approval_errors('FG-12', ev, ctx, cdate, rdate)
    if not isinstance(adr, dict) or set(adr) != set(c['adr_fields']):
        return e + ['FG-12: successor_adr con campos distintos del esquema'] + approval_errors('FG-12', ev, ctx, cdate, rdate)
    if not (isinstance(adr['id'], str) and re.fullmatch(c['adr_id_pattern'], adr['id'])):
        e.append('FG-12: id de ADR inválido o reservado (ADR-001..ADR-005)')
    if adr['status'] not in c['adr_statuses']:
        e.append(f'FG-12: estado de ADR desconocido {adr["status"]!r}')
    elif adr['status'] != c['passing_adr_status']:
        e.append(f'FG-12: el ADR sucesor está {adr["status"]}, no {c["passing_adr_status"]}')
    if adr['relation_to_adr005'] not in c['relations_to_adr005']:
        e.append('FG-12: relación con ADR-005 no admitida')
    if adr['scope'] not in c['scopes']:
        e.append('FG-12: alcance del ADR no admitido')
    if set(need) - set(cov):
        e.append(f'FG-12: el ADR no cubre {sorted(set(need) - set(cov))}')
    e += approval_errors('FG-12', ev, ctx, cdate, rdate)
    if not safe_doc_path(adr['path']):
        return e + ['FG-12: ruta del ADR inválida']
    # Pertenencia al candidato: solo cuentan los bytes del blob candidate_commit:path, leídos de Git (AF3-M01).
    blob = ctx['adr_blobs'].get((ev.get('candidate_commit'), adr['path']))
    why = blob_problem(blob)
    if why is not None:
        return e + [f'FG-12: el ADR sucesor no es un blob regular versionado en el commit candidato: {why}']
    data = blob['data']
    if sha256(data) != adr['sha256']:
        return e + ['FG-12: el SHA-256 declarado no es el del blob del ADR en el commit candidato']
    meta, outside, derr = human_document(data, 'FG-12: ADR', c['adr_block'], c['adr_headings'], min_letters)
    e += derr
    lines = [ln.strip() for ln in outside.splitlines() if ln.strip()]
    if not (lines and isinstance(adr['id'], str) and lines[0].startswith('# ') and adr['id'] in lines[0]
            and 'F36-SBX' in outside and 'ADR-005' in outside):
        e.append('FG-12: ADR: el título no nombra su id o el texto no cita F36-SBX y ADR-005 (otro contexto)')
    if STATUS_ASSERTION_RX.search(outside) or any(re.search(rf'\b{t}\b', outside) for t in ADR_STATUS_TOKENS):
        e.append('FG-12: ADR: aserción o token de estado fuera del bloque canónico (segunda fuente)')
    for token in c['relations_to_adr005'] + c['scopes'] + c['ei09_decisions']:
        if token in outside:
            e.append(f'FG-12: ADR: el token canónico {token} aparece fuera del bloque (segunda fuente)')
    if meta is None:
        return e
    if set(meta) != set(c['adr_metadata_fields']):
        return e + [f'FG-12: ADR: metadatos con campos distintos: faltan '
                    f'{sorted(set(c["adr_metadata_fields"]) - set(meta))}, sobran {sorted(set(meta) - set(c["adr_metadata_fields"]))}']
    # El ADR está dentro del commit candidato: su contexto es el gate, su versión y la base, nunca el propio commit.
    if meta['metadata_schema'] != c['adr_metadata_schema'] or meta['gate_id'] != ctx['schema']['gate_id'] \
            or meta['gate_version'] != ctx['schema']['gate_version'] or meta['base_commit'] != BASE:
        e.append('FG-12: ADR: metadatos de otro esquema, gate, versión o base (otro contexto)')
    for reg, key in (('id', 'adr_id'), ('status', 'status'), ('relation_to_adr005', 'relation_to_adr005'),
                     ('scope', 'scope')):
        if canonical(meta[key]) != canonical(adr[reg]):
            e.append(f'FG-12: ADR: {key} de los metadatos ({meta[key]!r}) no coincide con el registro ({adr[reg]!r})')
    mcov = meta['covered_ei']
    if not isinstance(mcov, list) or not all(isinstance(x, str) for x in mcov) or len(set(mcov)) != len(mcov) \
            or sorted(mcov) != sorted(map(str, cov)):
        e.append(f'FG-12: ADR: covered_ei de los metadatos ({mcov!r}) no coincide con el registro ({cov!r})')
    if canonical(meta['ei09_decision']) != canonical(d09):
        e.append(f'FG-12: ADR: ei09_decision de los metadatos ({meta["ei09_decision"]!r}) no coincide con el registro')
    dd = parse_date(meta['decided_on'])
    if dd is None or cdate is None or dd > cdate:
        e.append('FG-12: ADR: decided_on inválida o posterior al commit candidato que contiene el ADR')
    return e


SPECIFIC = {'FG-02': fg02_errors, 'FG-03': fg03_errors, 'FG-10': fg10_errors, 'FG-12': fg12_errors}


def team_evidence_errors(fg, ctx):
    """Errores semánticos de la evidencia de un criterio de EQUIPO. Lista vacía = evidencia válida."""
    sch, state = ctx.get('schema'), ctx['state']
    if not isinstance(sch, dict):
        return [f'{fg}: esquema de evidencia no verificado (falla cerrado)']
    path = sch['evidence_paths'][fg]
    crit = next((c for c in state.get('criteria') or [] if isinstance(c, dict) and c.get('id') == fg), {})
    e = []
    if crit.get('evidence') != path:
        e.append(f'{fg}: el estado del gate debe citar exactamente {path}')
    ev = json_bytes(ctx['evidence'].get(path))
    if not isinstance(ev, dict) or not ev:
        return e + [f'{fg}: {path} no existe, está vacío, no es JSON o tiene claves duplicadas']
    expected = set(sch['common_fields']) | set(sch['criteria'][fg]['fields'])
    if set(ev) != expected:
        return e + [f'{fg}: campos distintos del esquema: faltan {sorted(expected - set(ev))}, '
                    f'sobran {sorted(set(ev) - expected)}']
    if ev['schema'] != sch['schema_tag'] or ev['criterion_id'] != fg or ev['gate_id'] != sch['gate_id'] \
            or ev['gate_version'] != sch['gate_version']:
        e.append(f'{fg}: esquema, criterio, gate o versión distintos (evidencia de otro contexto)')
    cand = ev['candidate_commit']
    if cand != state.get('candidate_commit'):
        e.append(f'{fg}: candidate_commit distinto del candidato declarado en el estado del gate')
    e += [f'{fg}: {x}' for x in binding_errors(cand, ctx['facts'], ctx['gate_doc'])]
    if not (isinstance(ev['record_id'], str) and re.fullmatch(sch['record_id_pattern'], ev['record_id'])
            and ev['record_id'].startswith(f'F36SBX-{fg}-')):
        e.append(f'{fg}: record_id inválido')
    cdate = parse_date((ctx['facts'].get(cand) or {}).get('date')) if isinstance(cand, str) else None
    rdate = parse_date(ev['recorded_at'])
    if rdate is None:
        e.append(f'{fg}: recorded_at no es una fecha válida')
    elif cdate is not None and rdate < cdate:
        e.append(f'{fg}: recorded_at anterior al commit candidato')
    return e + SPECIFIC[fg](ev, ctx, cdate, rdate)


def evaluate_gate(state, classes, team_errors):
    """Regla de decisión del F36-SBX-GATE. Cualquier situación no prevista devuelve NO SUPERADO."""
    no = 'NO SUPERADO'
    if not isinstance(state, dict):
        return no
    if state.get('revocation') is not None:
        return 'REVOCADO'
    if state.get('authorizes') != ['F37-SBX']:
        return no
    crit = state.get('criteria')
    if not isinstance(crit, list) or not all(isinstance(c, dict) for c in crit) \
            or [c.get('id') for c in crit] != FG_IDS:
        return no
    st = {c['id']: c.get('status') for c in crit}
    for fg, v in st.items():
        admitted = (TEAM_STATUSES | ({'NO APLICA'} if fg in FG_NA_ALLOWED else set())) if fg in FG_TEAM \
            else AUTO_STATUSES
        if v not in admitted:
            return no
    auth = state.get('f37_authorized_ei')
    if auth is not None:
        if not isinstance(auth, list) or not auth or len({str(x) for x in auth}) != len(auth):
            return no
        if any(classes.get(x) not in ('ALLOWED', 'CONDITIONAL') for x in auth):
            return no
    for fg in FG_TEAM:
        if st[fg] == 'CUMPLE':
            try:
                if team_errors(fg):
                    return no
            except Exception:  # noqa: BLE001 — una evidencia no evaluable nunca supera el gate
                return no
    conditional = auth is not None and any(classes.get(x) == 'CONDITIONAL' for x in auth)
    for fg, v in st.items():
        if v == 'NO APLICA':
            if st['FG-03'] != 'CUMPLE' or auth is None or conditional:
                return no
        elif v != 'CUMPLE':
            return no
    if auth is None or not isinstance(state.get('candidate_commit'), str):
        return no
    return 'SUPERADO'


def rule_gate(s, auto):
    out = []
    state = strict_json(s['texts'].get(GATE_STATE) or '')
    if not isinstance(state, dict):
        return [(False, 'estado del gate: JSON inválido o con claves duplicadas (falla cerrado)')], 'NO SUPERADO'
    out.append((set(state) == GATE_KEYS, f'estado del gate con esquema cerrado; diferencias: '
                                         f'{sorted(set(state) ^ GATE_KEYS)}'))
    out.append((state.get('gate_id') == 'F36-SBX-GATE' and state.get('gate_version') == GATE_VERSION
                and state.get('base_commit') == BASE and state.get('team_evidence_schema') == TEAM_SCHEMA_TAG,
                'identidad, versión, base y esquema de evidencia del gate'))
    ca = state.get('cannot_authorize')
    scope_ok = state.get('authorizes') == ['F37-SBX'] and isinstance(ca, list) and set(ca) == CANNOT_AUTHORIZE \
        and len(ca) == len(CANNOT_AUTHORIZE)
    out.append((scope_ok, 'el gate solo autoriza F37-SBX y declara la lista cerrada de lo que no puede autorizar'))
    schema = strict_json(s['texts'].get(TEAM_SCHEMA) or '')
    schema_ok = isinstance(schema, dict) and sha256(canonical(schema)) == TEAM_SCHEMA_SHA256
    out.append((schema_ok, f'esquema de evidencia EQUIPO idéntico a la versión cerrada {TEAM_SCHEMA_TAG}'))
    serr = team_schema_errors(schema)
    out.append((not serr, f'invariantes del esquema de evidencia EQUIPO; errores: {serr}'))
    crit = state.get('criteria') if isinstance(state.get('criteria'), list) else []
    struct = []
    if [c.get('id') if isinstance(c, dict) else None for c in crit] != FG_IDS:
        struct.append('los criterios deben ser exactamente FG-01..FG-14, en orden')
    for c in crit:
        if not isinstance(c, dict):
            continue
        fg, team = c.get('id'), c.get('id') in FG_TEAM
        keys = {'id', 'kind', 'status', 'evidence'} if team else {'id', 'kind', 'status'}
        if set(c) != keys or c.get('kind') != ('team' if team else 'auto'):
            struct.append(f'{fg}: claves o tipo distintos ({"EQUIPO" if team else "AUTO"})')
        admitted = (TEAM_STATUSES | ({'NO APLICA'} if fg in FG_NA_ALLOWED else set())) if team else AUTO_STATUSES
        if c.get('status') not in admitted:
            struct.append(f'{fg}: estado {c.get("status")!r} no admitido para este criterio')
        if team and c.get('status') != 'CUMPLE' and c.get('evidence') is not None:
            struct.append(f'{fg}: solo un criterio en CUMPLE cita evidencia')
    out.append((not struct, f'criterios cerrados: tipos, claves, estados admitidos y evidencia; errores: {struct}'))
    computed_auto = {
        'FG-01': all(auto.values()), 'FG-04': auto['GOV'], 'FG-05': auto['FRZ'], 'FG-06': auto['CAP'],
        'FG-07': auto['CTR'], 'FG-08': auto['THR'], 'FG-09': auto['EVA'], 'FG-11': auto['CAP'] and auto['SEM'],
        'FG-13': scope_ok, 'FG-14': state.get('revocation') is None,
    }
    status = {c.get('id'): c.get('status') for c in crit if isinstance(c, dict)}
    mismatch = [fg for fg, ok in computed_auto.items() if status.get(fg) != ('CUMPLE' if ok else 'NO CUMPLE')]
    out.append((not mismatch, f'los criterios AUTO declarados coinciden con los recalculados; difieren: {mismatch}'))
    cand = state.get('candidate_commit')
    cumple = [fg for fg in FG_TEAM if status.get(fg) == 'CUMPLE']
    if cand is None:
        cand_err = [f'{cumple} en CUMPLE sin candidate_commit'] if cumple else []
    else:
        cand_err = binding_errors(cand, s['facts'], s['texts'].get(GATE_DOC))
    out.append((not cand_err, f'vínculo con el commit candidato auditado (nulo mientras no haya evidencia); '
                              f'errores: {cand_err}'))
    ctx = {'state': state, 'schema': schema if schema_ok and not serr else None, 'evidence': s['evidence'],
           'facts': s['facts'], 'adr_blobs': s['adr_blobs'], 'classes': EXPECTED_CLASSES,
           'gate_doc': s['texts'].get(GATE_DOC)}

    def team_errors(fg):
        return team_evidence_errors(fg, ctx)
    invalid = {}
    for fg in cumple:
        try:
            errs = team_errors(fg)
        except Exception as exc:  # noqa: BLE001 — cualquier error de evaluación falla cerrado
            errs = [f'{fg}: evidencia no evaluable ({exc.__class__.__name__}, falla cerrado)']
        if errs:
            invalid[fg] = errs
    out.append((not invalid, f'cada criterio EQUIPO en CUMPLE tiene evidencia semánticamente válida y coherente '
                             f'con su informe o ADR; inválidas: {invalid}'))
    referenced = {f'{GATE_EVIDENCE}{fg}.json' for fg in cumple}
    fg02 = json_bytes(s['evidence'].get(f'{GATE_EVIDENCE}FG-02.json'))
    if 'FG-02' in cumple and isinstance(fg02, dict) and isinstance(fg02.get('audit_report'), dict):
        referenced.add(fg02['audit_report'].get('path'))
    stray = sorted(p for p in s['evidence'] if p not in referenced)
    unreadable = sorted(p for p, b in s['evidence'].items() if not isinstance(b, bytes))
    out.append((not stray and not unreadable, f'gate/evidencia/ solo contiene evidencia citada y archivos regulares; '
                                              f'sin citar: {stray}; enlaces o ilegibles: {unreadable}'))
    ignored = s['ignored']
    ign_err = ['no se pudo comprobar con Git si la evidencia es versionable (falla cerrado)'] if ignored is None \
        else [f'{p}: Git lo ignora, así que ningún commit puede contenerlo' for p in ignored
              if p.startswith(GATE_EVIDENCE)]
    out.append((not ign_err, f'la evidencia de equipo es versionable: Git no ignora ningún archivo de gate/evidencia/; '
                             f'errores: {ign_err}'))
    auth = state.get('f37_authorized_ei')
    auth_err = []
    if auth is not None:
        if not isinstance(auth, list) or not auth or len({str(x) for x in auth}) != len(auth) \
                or any(EXPECTED_CLASSES.get(x) not in ('ALLOWED', 'CONDITIONAL') for x in auth):
            auth_err.append(f'f37_authorized_ei solo admite una lista de EI ALLOWED o CONDITIONAL: {auth}')
        if status.get('FG-03') != 'CUMPLE':
            auth_err.append('f37_authorized_ei declarada sin FG-03 en CUMPLE')
    out.append((not auth_err, f'autorización de F37-SBX coherente con la matriz y con FG-03; errores: {auth_err}'))
    result = evaluate_gate(state, EXPECTED_CLASSES, team_errors)
    if result == 'SUPERADO' and (mismatch or struct or cand_err or invalid or not schema_ok or serr or ign_err):
        result = 'NO SUPERADO'
    out.append((state.get('declared_result') == result,
                f'resultado declarado {state.get("declared_result")!r} = recalculado {result!r}'))
    doc = norm(s['texts'].get(GATE_DOC) or '')
    rows = {r[0]: r for r in table_rows(doc, 'FG-')}
    doc_err = []
    for c in crit:
        if not isinstance(c, dict):
            continue
        r = rows.get(c.get('id'))
        if not r or len(r) != 5:
            doc_err.append(f'{c.get("id")}: sin fila')
        elif r[2] != ('EQUIPO' if c.get('kind') == 'team' else 'AUTO') or r[4] != c.get('status'):
            doc_err.append(f'{c.get("id")}: tipo o estado distinto del JSON')
    out.append((not doc_err and sorted(rows) == FG_IDS, f'tabla FG del documento = JSON; diferencias: {doc_err}'))
    phrase = f'F36-SBX-GATE = {result}'
    where = [rel for rel in [GATE_DOC, f'{PKG}/README.md'] if phrase not in norm(s['texts'].get(rel) or '')]
    out.append((not where, f'«{phrase}» declarado en el gate y en el README; falta en: {where}'))
    out.append((result == 'NO SUPERADO', f'el gobierno de esta versión exige F36-SBX-GATE = NO SUPERADO; '
                                         f'el gate da {result}'))
    return out, result


RULES = [('STR', rule_str), ('LNK', rule_lnk), ('GOV', rule_gov), ('SEM', rule_sem), ('CAP', rule_cap),
         ('CTR', rule_ctr), ('THR', rule_thr), ('EVA', rule_eva), ('FRZ', rule_frz), ('DEP', rule_dep),
         ('PII', rule_pii)]


def run(s):
    """Devuelve [(regla, ok, mensaje)] y el resultado del gate."""
    results, auto = [], {}
    for name, fn in RULES:
        checks = fn(s)
        auto[name] = all(ok for ok, _ in checks)
        results += [(name, ok, msg) for ok, msg in checks]
    gate_checks, gate = rule_gate(s, auto)
    results += [('GATE', ok, msg) for ok, msg in gate_checks]
    return results, gate


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    s = collect(ROOT)
    results, gate = run(s)
    fails = [r for r in results if not r[1]]
    for name, ok, msg in results:
        print(f'{"OK   " if ok else "FALLA"} {name}: {msg}')
    print(f'INFO F36-SBX-GATE = {gate} · rama {s["branch"]} · base {BASE[:7]}')
    print(f'validate_f36sbx: {len(results) - len(fails)} comprobaciones correctas, {len(fails)} fallas')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
