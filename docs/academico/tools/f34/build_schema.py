"""F34 — Contrato de datos formal (schema.json), al estilo Frictionless Table Schema, sin dependencias.

Cada campo declara: tipo, obligatoriedad, restricciones (enum, mínimo, máximo, patrón), y su **rol**:
identifier · foreign_key · context · human_record · free_text_synthetic · feature_process · label_process ·
lineage · split · fairness_synthetic. F35/F36 leen este archivo; el validador F34 lo aplica.

Uso: python docs/academico/tools/f34/build_schema.py   → escribe docs/academico/tools/f34/schema.json
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from generate_synthetic import (FAIRNESS_TABLE, PROCESS_FEATURES, SCHEMA_VERSION, TABLES)  # noqa: E402

S, I, D, B, DT = 'string', 'integer', 'date', 'boolean', 'datetime'


def f(name, typ, role, required=True, **c):
    out = {'name': name, 'type': typ, 'role': role, 'constraints': {'required': required, **c}}
    return out


ORG = dict(pattern=r'^ORG-S\d$')
VAC = dict(pattern=r'^VAC-\d{4}$')
APP = dict(pattern=r'^APP-\d{5}$')
CRI = dict(pattern=r'^CRI-\d{4}$')
EVT = dict(pattern=r'^EV-S\d-\d{2}$')
SES = dict(pattern=r'^SES-\d{5}$')
ASM = dict(pattern=r'^ASM-\d{5}$')
CV = dict(pattern=r'^CV-VAC-\d{4}-\d+$')
RV = dict(pattern=r'^RV-VAC-\d{4}-\d+$')
TXT = dict(pattern=r'^\[SINTÉTICO\] ')

FIELDS = {
    'organizations': [f('organization_token', S, 'identifier', **ORG)],
    'competencies': [f('competency_id', S, 'identifier', pattern=r'^CMP-S\d-\d{2}$'),
                     f('organization_token', S, 'foreign_key', **ORG),
                     f('competency_label', S, 'context'),
                     f('scope', S, 'context', enum=['docente', 'administrativo', 'ambos']),
                     f('catalog_version', S, 'lineage', pattern=r'^CAT-S\d-v\d+$')],
    'vacancies': [f('vacancy_token', S, 'identifier', **VAC), f('organization_token', S, 'foreign_key', **ORG),
                  f('area', S, 'context', enum=['docente', 'administrativo']),
                  f('positions_count', I, 'context', minimum=1, maximum=3),
                  f('published_at', DT, 'context'), f('closes_at', D, 'context'),
                  f('target_completion_at', DT, 'context'),
                  f('criteria_version', S, 'lineage', **CV), f('rubric_version', S, 'lineage', **RV)],
    'criteria': [f('criterion_id', S, 'identifier', **CRI), f('vacancy_token', S, 'foreign_key', **VAC),
                 f('competency_id', S, 'foreign_key', pattern=r'^CMP-S\d-\d{2}$'),
                 f('stage', S, 'context', enum=['evaluacion', 'entrevista']),
                 f('method', S, 'context', enum=['prueba_escrita', 'revision_documental', 'clase_demostrativa',
                                                 'entrevista_estructurada']),
                 f('weight', I, 'context', minimum=1, maximum=100),
                 f('range_min', I, 'context', minimum=0, maximum=0), f('range_max', I, 'context', minimum=20, maximum=20),
                 f('criteria_version', S, 'lineage', **CV)],
    'rubric_levels': [f('rubric_level_id', S, 'identifier', pattern=r'^CRI-\d{4}-L[1-4]$'),
                      f('criterion_id', S, 'foreign_key', **CRI), f('rubric_version', S, 'lineage', **RV),
                      f('level', I, 'context', minimum=1, maximum=4),
                      f('descriptor', S, 'free_text_synthetic', **TXT),
                      f('rubric_points', I, 'context', minimum=5, maximum=20)],
    'requirements': [f('requirement_id', S, 'identifier', pattern=r'^REQ-\d{4}$'),
                     f('vacancy_token', S, 'foreign_key', **VAC),
                     f('requirement_type', S, 'context', enum=['titulo_profesional', 'colegiatura_vigente',
                                                                'experiencia_minima']),
                     f('min_years', I, 'context', required=False, minimum=1, maximum=5)],
    'applications': [f('application_token', S, 'identifier', **APP), f('vacancy_token', S, 'foreign_key', **VAC),
                     f('organization_token', S, 'foreign_key', **ORG),
                     f('person_token', S, 'identifier', pattern=r'^PER-S-\d{5}$'),
                     f('submitted_at', DT, 'context'),
                     f('application_state', S, 'context', enum=['activa', 'descartada']),
                     f('years_experience_declared', I, 'human_record', required=False, minimum=0, maximum=20)],
    'requirement_checks': [f('check_id', S, 'identifier', pattern=r'^CHK-\d{5}$'),
                           f('application_token', S, 'foreign_key', **APP),
                           f('requirement_id', S, 'foreign_key', pattern=r'^REQ-\d{4}$'),
                           f('declared_met', B, 'human_record', required=False),
                           f('evidence_present', B, 'human_record')],
    'sessions': [f('session_token', S, 'identifier', **SES), f('application_token', S, 'foreign_key', **APP),
                 f('vacancy_token', S, 'foreign_key', **VAC),
                 f('stage', S, 'context', enum=['evaluacion', 'entrevista']),
                 f('evaluator_token', S, 'identifier', **EVT), f('created_at', DT, 'context'),
                 f('scheduled_for', DT, 'context'), f('status', S, 'context', enum=['programada', 'realizada']),
                 f('completed_at', DT, 'context', required=False)],
    'assessments': [f('assessment_id', S, 'identifier', **ASM), f('session_token', S, 'foreign_key', **SES),
                    f('application_token', S, 'foreign_key', **APP), f('criterion_id', S, 'foreign_key', **CRI),
                    f('evaluator_token', S, 'identifier', **EVT),
                    f('human_level', I, 'human_record', minimum=1, maximum=4),
                    f('rubric_points', I, 'human_record', minimum=5, maximum=20),
                    f('justification', S, 'free_text_synthetic', **TXT),
                    f('evidence_sufficiency', S, 'human_record', enum=['suficiente', 'parcial', 'insuficiente']),
                    f('recorded_at', DT, 'context'), f('rubric_version', S, 'lineage', **RV),
                    f('criteria_version', S, 'lineage', **CV)],
    'evidence': [f('evidence_id', S, 'identifier', pattern=r'^EVD-\d{6}$'),
                 f('session_token', S, 'foreign_key', **SES), f('application_token', S, 'foreign_key', **APP),
                 f('criterion_id', S, 'foreign_key', **CRI),
                 f('assessment_id', S, 'foreign_key', required=False, **ASM),
                 f('source_type_ev', S, 'context', enum=['cv', 'documento', 'prueba', 'formulario', 'nota_entrevista']),
                 f('source_reference', S, 'context',
                   pattern=r'^((cv|documento|prueba|formulario):DOC-S-\d{4}#p\d|pregunta:PRG-\d{3})$'),
                 f('evidence_text', S, 'free_text_synthetic', **TXT),
                 f('provenance', S, 'lineage', enum=['registro_humano']),
                 f('registered_by', S, 'identifier', **EVT), f('registered_at', DT, 'context'),
                 f('state', S, 'context', enum=['borrador', 'vinculada'])],
    'annotations': [f('annotation_id', S, 'identifier', pattern=r'^ANN-\d{4}$'),
                    f('assessment_id', S, 'foreign_key', **ASM), f('author_token', S, 'identifier', **EVT),
                    f('created_at', DT, 'context'), f('reason', S, 'context', enum=['aclaracion', 'fuente_adicional']),
                    f('annotation_text', S, 'free_text_synthetic', **TXT)],
    'process_events': [f('event_id', S, 'identifier', pattern=r'^PEV-\d{5}$'),
                       f('vacancy_token', S, 'foreign_key', **VAC), f('organization_token', S, 'foreign_key', **ORG),
                       f('event_type', S, 'context', enum=[
                           'vacante_publicada', 'postulacion_recibida', 'evaluacion_programada',
                           'evaluacion_realizada', 'entrevista_programada', 'entrevista_realizada', 'cambio_etapa',
                           'vacante_cerrada']),
                       f('event_at', DT, 'context'), f('ref_token', S, 'context', required=False)],
    'process_snapshots': [f('vacancy_token', S, 'identifier', **VAC), f('organization_token', S, 'lineage', **ORG),
                          f('checkpoint_at', DT, 'lineage')]
    + [f(n, I, 'feature_process', minimum=-365 if n == 'days_remaining_to_target' else 0, maximum=1000)
       for n in PROCESS_FEATURES]
    + [f('delayed', I, 'label_process', required=False, minimum=0, maximum=1),
       f('observation_status', S, 'lineage', enum=['completed', 'censored']),
       f('dataset_version', S, 'lineage', pattern=r'^f34-synth-\d+\.\d+\.\d+$')],
    'process_splits': [f('vacancy_token', S, 'identifier', **VAC), f('checkpoint_at', DT, 'lineage'),
                       f('label_known_at', DT, 'lineage', required=False),
                       f('split', S, 'split', enum=['train', 'validation', 'test', 'purgado', 'censurado']),
                       f('split_reason', S, 'split', enum=['temporal', 'etiqueta_no_madura_antes_de_validation',
                                                           'etiqueta_no_madura_antes_de_test', 'sin_cierre_observado'])],
    'analysis_runs': [f('analysis_run_id', S, 'identifier',
                        pattern=r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'),
                      f('vacancy_token', S, 'foreign_key', **VAC), f('organization_token', S, 'lineage', **ORG),
                      f('trigger', S, 'context', enum=['resultado_registrado']),
                      f('rules_version', S, 'lineage'), f('criteria_version', S, 'lineage', **CV),
                      f('rubric_version', S, 'lineage', **RV),
                      f('input_hash_algorithm', S, 'lineage', enum=['f34-input-sha256-v1']),
                      f('input_snapshot_hash', S, 'lineage', pattern=r'^[0-9a-f]{64}$'), f('created_at', DT, 'lineage')],
    'analysis_run_events': [f('event_id', S, 'identifier', pattern=r'^ARE-\d{5}$'),
                            f('analysis_run_id', S, 'foreign_key'), f('seq', I, 'lineage', minimum=1, maximum=10),
                            f('state', S, 'lineage', enum=['pendiente', 'en_proceso', 'completado', 'fallido',
                                                           'expirado', 'invalidado']),
                            f('event_at', DT, 'lineage'), f('error_code', S, 'lineage', required=False, enum=['E-10'])],
    'expected_alerts': [f('alert_id', S, 'identifier', pattern=r'^ALR-\d{5}$'),
                        f('alert_type', S, 'context', enum=['requisito_no_evidenciado', 'evidencia_faltante',
                                                           'sesion_vencida', 'discrepancia_evaluadores']),
                        f('vacancy_token', S, 'foreign_key', **VAC),
                        f('application_token', S, 'foreign_key', required=False, **APP),
                        f('criterion_id', S, 'foreign_key', required=False, **CRI), f('ref_id', S, 'context')],
    FAIRNESS_TABLE[0]: [f('person_token', S, 'identifier', pattern=r'^PER-S-\d{5}$'),
                        f('grupo_sintetico', S, 'fairness_synthetic', enum=['GS-A', 'GS-B'])],
}
LINEAGE = [f('source_type', S, 'lineage', enum=['synthetic']),
           f('synthetic_record_id', S, 'lineage', pattern=r'^SYN-\d{6}$', unique=True)]

KEYS = {
    'organizations': ('organization_token', []),
    'competencies': ('competency_id', [('organization_token', 'organizations', 'organization_token')]),
    'vacancies': ('vacancy_token', [('organization_token', 'organizations', 'organization_token')]),
    'criteria': ('criterion_id', [('vacancy_token', 'vacancies', 'vacancy_token'),
                                  ('competency_id', 'competencies', 'competency_id')]),
    'rubric_levels': ('rubric_level_id', [('criterion_id', 'criteria', 'criterion_id')]),
    'requirements': ('requirement_id', [('vacancy_token', 'vacancies', 'vacancy_token')]),
    'applications': ('application_token', [('vacancy_token', 'vacancies', 'vacancy_token'),
                                           ('organization_token', 'organizations', 'organization_token')]),
    'requirement_checks': ('check_id', [('application_token', 'applications', 'application_token'),
                                        ('requirement_id', 'requirements', 'requirement_id')]),
    'sessions': ('session_token', [('application_token', 'applications', 'application_token'),
                                   ('vacancy_token', 'vacancies', 'vacancy_token')]),
    'assessments': ('assessment_id', [('session_token', 'sessions', 'session_token'),
                                      ('application_token', 'applications', 'application_token'),
                                      ('criterion_id', 'criteria', 'criterion_id')]),
    'evidence': ('evidence_id', [('session_token', 'sessions', 'session_token'),
                                 ('application_token', 'applications', 'application_token'),
                                 ('criterion_id', 'criteria', 'criterion_id'),
                                 ('assessment_id', 'assessments', 'assessment_id')]),
    'annotations': ('annotation_id', [('assessment_id', 'assessments', 'assessment_id')]),
    'process_events': ('event_id', [('vacancy_token', 'vacancies', 'vacancy_token'),
                                    ('organization_token', 'organizations', 'organization_token')]),
    'process_snapshots': ('vacancy_token', [('vacancy_token', 'vacancies', 'vacancy_token')]),
    'process_splits': ('vacancy_token', [('vacancy_token', 'process_snapshots', 'vacancy_token')]),
    'analysis_runs': ('analysis_run_id', [('vacancy_token', 'vacancies', 'vacancy_token')]),
    'analysis_run_events': ('event_id', [('analysis_run_id', 'analysis_runs', 'analysis_run_id')]),
    'expected_alerts': ('alert_id', [('vacancy_token', 'vacancies', 'vacancy_token'),
                                     ('application_token', 'applications', 'application_token'),
                                     ('criterion_id', 'criteria', 'criterion_id')]),
    FAIRNESS_TABLE[0]: ('person_token', []),
}


def build():
    resources = []
    for name, fields in FIELDS.items():
        cols = TABLES.get(name) or FAIRNESS_TABLE[1]
        allf = fields + LINEAGE
        assert [x['name'] for x in allf] == cols, (name, [x['name'] for x in allf], cols)
        pk, fks = KEYS[name]
        resources.append({'name': name, 'path': f'{name}.csv', 'schema': {
            'fields': allf, 'primaryKey': pk,
            'foreignKeys': [{'fields': a, 'reference': {'resource': r, 'fields': b}} for a, r, b in fks]}})
    return {'profile': 'f34-table-schema (inspirado en Frictionless Table Schema)', 'schema_version': SCHEMA_VERSION,
            'encoding': 'utf-8', 'missing_values': [''], 'boolean_values': ['true', 'false'],
            'date_format': 'date: YYYY-MM-DD; datetime: YYYY-MM-DDTHH:MM:SS (America/Lima, sin desplazamiento)',
            'temporal_semantics': 'RF-29: t <= checkpoint_at; vencida: scheduled_at < checkpoint_at; abierta: '
                                  'published_at <= at y (closed_at nulo o > at); días completos = floor(segundos/86400)',
            'resources': resources}


if __name__ == '__main__':
    out = os.path.join(HERE, 'schema.json')
    with open(out, 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(build(), fh, ensure_ascii=False, indent=1)
        fh.write('\n')
    print('escrito schema.json')
