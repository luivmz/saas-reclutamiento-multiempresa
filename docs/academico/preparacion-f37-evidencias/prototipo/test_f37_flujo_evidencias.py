"""Pruebas del prototipo del flujo de evidencias (preparación de F37). Solo biblioteca estándar.

Ejecución, desde la raíz del repositorio:
    python -I -B -m unittest discover -s docs/academico/preparacion-f37-evidencias/prototipo -v
"""

import copy
import itertools
import json
import pathlib
import re
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import f37_flujo_evidencias as f37  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parents[4]
DATA = f37.load_examples()
REASON = '[SINTÉTICO] Motivo ficticio.'


def store():
    return f37.Store(copy.deepcopy(DATA))


def params_for(action, application, evidence=None, criterion='CRI-S1-01-PLAN'):
    """Parámetros válidos de forma para cada acción, para probar solo la autorización."""
    if action == 'registrar':
        return {'application': application, 'type': 'certificado', 'source': 'documento_presentado',
                'description': '[SINTÉTICO] Prueba.'}
    if action in ('consultar', 'historial'):
        return {'application': application}
    base = {'evidence': evidence}
    if action in ('enlazar', 'desenlazar'):
        base['criterion'] = criterion
    if action == 'corregir':
        base.update(source='documento_presentado', description='[SINTÉTICO] Corrección.')
    if action == 'retirar':
        base['reason'] = REASON
    return base


class Escenarios(unittest.TestCase):
    def test_todos_los_escenarios_ficticios_dan_lo_esperado(self):
        self.assertEqual(f37.run_scenarios(DATA), [])

    def test_hay_escenarios_permitidos_y_denegados_de_cada_regla(self):
        rules = {s['rule'] for s in DATA['scenarios']}
        self.assertTrue({'R-01', 'R-02', 'R-03', 'R-04', 'R-05', 'R-08', 'R-09', 'DEF-14'} <= rules)
        expected = {s['expected'] for s in DATA['scenarios']}
        self.assertEqual(expected, {'permitido', 'denegado'})

    def test_un_escenario_con_lo_esperado_invertido_se_detecta(self):
        data = copy.deepcopy(DATA)
        data['scenarios'][10]['expected'] = 'permitido'  # ESC-11, acceso de otra organización
        errors = f37.run_scenarios(data)
        self.assertEqual(len(errors), 1)
        self.assertIn('ESC-11', errors[0])


class Aislamiento(unittest.TestCase):
    def test_ningun_actor_alcanza_otra_organizacion_con_ninguna_accion(self):
        s = store()
        apps_by_org = {o: [a for a, v in s.applications.items() if v['org'] == o] for o in DATA['organizations']}
        evidence_by_app = {e['application']: e['id'] for e in s.evidence.values()}
        for user in DATA['users']:
            for org, apps in apps_by_org.items():
                if user['org'] == org:
                    continue
                for app, action in itertools.product(apps, f37.ACTIONS):
                    ok, _ = s.decide(user['token'], action, params_for(action, app, evidence_by_app.get(app)))
                    self.assertFalse(ok, (user['token'], action, app))

    def test_postulante_y_area_solicitante_no_acceden_a_la_evidencia_interna(self):
        s = store()
        for actor, app, action in itertools.product(('USR-PST-01', 'USR-S1-SOL'), s.applications, f37.ACTIONS):
            ok, _ = s.decide(actor, action, params_for(action, app, 'EVD-S1-0001'))
            self.assertFalse(ok, (actor, action, app))

    def test_la_matriz_de_roles_es_la_de_la_especificacion_y_deniega_por_rol(self):
        # Defensa en profundidad: el rol deniega antes que la organización, y la matriz queda fijada.
        self.assertEqual({r: sorted(a) for r, a in f37.ROLE_ACTIONS.items()}, {
            'rrhh': sorted(f37.ACTIONS),
            'aprobador': ['consultar', 'historial'],
            'evaluador': ['consultar', 'corregir', 'desenlazar', 'enlazar', 'registrar'],
            'solicitante': [],
            'postulante': [],
        })
        s = store()
        for actor in ('USR-PST-01', 'USR-S1-SOL'):
            ok, reason = s.decide(actor, 'consultar', {'application': 'APP-S1-001'})
            self.assertFalse(ok)
            self.assertIn('no puede consultar', reason)

    def test_un_evaluador_no_asignado_no_actua_sobre_la_postulacion(self):
        s = store()
        for action in f37.ACTIONS:
            ok, reason = s.decide('USR-S1-EVA-B', action, params_for(action, 'APP-S1-001', 'EVD-S1-0002'))
            self.assertFalse(ok, action)

    def test_la_consulta_solo_devuelve_evidencia_de_la_propia_organizacion(self):
        s = store()
        self.assertEqual(s.visible_evidence('USR-S1-DIR', 'APP-S1-001'), ['EVD-S1-0001', 'EVD-S1-0002'])
        self.assertEqual(s.visible_evidence('USR-S2-RRHH', 'APP-S1-001'), [])
        self.assertEqual(s.visible_evidence('USR-S2-DIR', 'APP-S2-001'), ['EVD-S2-0004'])


class Flujo(unittest.TestCase):
    def test_flujo_completo_registra_enlaza_revisa_corrige_y_retira(self):
        s = store()
        self.assertEqual(s.execute('USR-S1-RRHH', 'enlazar', {'evidence': 'EVD-S1-0001', 'criterion': 'CRI-S1-01-PLAN'}),
                         (True, 'permitido'))
        self.assertTrue(s.execute('USR-S1-RRHH', 'revisar', {'evidence': 'EVD-S1-0001'})[0])
        self.assertTrue(s.execute('USR-S1-RRHH', 'corregir', {'evidence': 'EVD-S1-0001', 'source': 'documento_presentado',
                                                              'description': '[SINTÉTICO] Certificado corregido.'})[0])
        self.assertEqual(s.state('EVD-S1-0001'), 'sustituida')
        self.assertEqual(s.state('EVD-S1-0005'), 'registrada')
        self.assertEqual(s.evidence['EVD-S1-0005']['supersedes'], 'EVD-S1-0001')
        self.assertEqual(s.active_links('EVD-S1-0005'), ['CRI-S1-01-PLAN'])  # hereda el enlace
        self.assertTrue(s.execute('USR-S1-RRHH', 'retirar', {'evidence': 'EVD-S1-0005', 'reason': REASON})[0])
        self.assertEqual(s.state('EVD-S1-0005'), 'retirada')
        self.assertEqual([e['action'] for e in s.audit[4:]],
                         ['evidencia.enlazada', 'evidencia.revisada', 'evidencia.corregida', 'evidencia.enlazada',
                          'evidencia.retirada'])

    def test_desenlazar_deja_constancia_y_el_enlace_deja_de_estar_vigente(self):
        s = store()
        s.execute('USR-S1-EVA-A', 'enlazar', {'evidence': 'EVD-S1-0002', 'criterion': 'CRI-S1-01-CLASE'})
        self.assertTrue(s.execute('USR-S1-EVA-A', 'desenlazar', {'evidence': 'EVD-S1-0002',
                                                                 'criterion': 'CRI-S1-01-CLASE'})[0])
        self.assertEqual(s.active_links('EVD-S1-0002'), [])
        self.assertEqual([e['action'] for e in s.events[-2:]], ['evidencia.enlazada', 'evidencia.enlace_retirado'])

    def test_solo_insercion_ningun_registro_previo_cambia(self):
        s = store()
        s.execute('USR-S1-RRHH', 'enlazar', {'evidence': 'EVD-S1-0001', 'criterion': 'CRI-S1-01-PLAN'})
        evidence_before = copy.deepcopy(s.evidence)
        events_before = copy.deepcopy(s.events)
        s.execute('USR-S1-RRHH', 'corregir', {'evidence': 'EVD-S1-0001', 'source': 'documento_presentado',
                                              'description': '[SINTÉTICO] Otra versión.'})
        s.execute('USR-S1-RRHH', 'retirar', {'evidence': 'EVD-S1-0003', 'reason': REASON})
        for key, record in evidence_before.items():
            self.assertEqual(s.evidence[key], record)
        self.assertEqual(s.events[:len(events_before)], events_before)

    def test_la_auditoria_no_lleva_texto_de_la_evidencia(self):
        s = store()
        s.execute('USR-S1-RRHH', 'retirar', {'evidence': 'EVD-S1-0003', 'reason': REASON})
        for row in s.audit:
            self.assertLessEqual(set(row), set(f37.AUDIT_FIELDS))
            self.assertNotIn('[SINTÉTICO]', json.dumps(row, ensure_ascii=False))

    def test_un_campo_prohibido_se_rechaza_en_cualquier_escritura_y_con_cualquier_grafia(self):
        s = store()
        writes = [('registrar', params_for('registrar', 'APP-S1-002')),
                  ('enlazar', {'evidence': 'EVD-S1-0001', 'criterion': 'CRI-S1-01-PLAN'}),
                  ('retirar', {'evidence': 'EVD-S1-0001', 'reason': REASON})]
        for (action, params), field in itertools.product(writes, ('candidate_score', 'candidateScore', 'CandidateName')):
            ok, reason = s.decide('USR-S1-RRHH', action, {**params, field: 'x'})
            self.assertFalse(ok, (action, field))
            self.assertIn('campo prohibido', reason)

    def test_el_tipo_fija_la_fuente_declarada(self):
        s = store()
        base = {'application': 'APP-S1-002', 'description': '[SINTÉTICO] Prueba.'}
        for kind, source, expected in (('cv', 'documento_presentado', True), ('cv', 'sesion_asignada', False),
                                       ('certificado', 'sesion_asignada', False),
                                       ('transcripcion_revisada', 'sesion_asignada', True),
                                       ('transcripcion_revisada', 'documento_presentado', False)):
            self.assertEqual(s.decide('USR-S1-RRHH', 'registrar', {**base, 'type': kind, 'source': source})[0],
                             expected, (kind, source))
        self.assertFalse(s.decide('USR-S1-EVA-A', 'registrar', {'application': 'APP-S1-001', 'type': 'observacion',
                                                                'source': 'documento_presentado',
                                                                'description': '[SINTÉTICO] Prueba.'})[0])

    def test_una_denegacion_no_escribe_nada(self):
        s = store()
        before = (copy.deepcopy(s.evidence), copy.deepcopy(s.events))
        self.assertFalse(s.execute('USR-S2-RRHH', 'retirar', {'evidence': 'EVD-S1-0001', 'reason': REASON})[0])
        self.assertEqual((s.evidence, s.events), before)


class CoherenciaConElSaaS(unittest.TestCase):
    def test_los_roles_son_exactamente_los_de_UserRole(self):
        source = (REPO / 'app/Enums/UserRole.php').read_text(encoding='utf-8')
        roles = set(re.findall(r"case \w+ = '([a-z]+)';", source))
        self.assertEqual(roles, set(f37.ROLE_ACTIONS))

    def test_las_acciones_de_auditoria_son_candidatas_y_no_existen_todavia(self):
        source = (REPO / 'app/Enums/AuditAction.php').read_text(encoding='utf-8')
        existing = set(re.findall(r"= '([a-z_.]+)';", source))
        self.assertTrue(existing)
        self.assertEqual(existing & set(f37.AUDIT_ACTION.values()), set())

    def test_los_tokens_prohibidos_vienen_del_contrato_v4(self):
        tokens = f37.forbidden_tokens()
        self.assertTrue({'score', 'rank', 'select', 'name', 'email', 'level'} <= tokens)

    def test_el_prototipo_solo_importa_la_biblioteca_estandar(self):
        source = pathlib.Path(f37.__file__).read_text(encoding='utf-8')
        imports = set(re.findall(r'^(?:from|import) (\w+)', source, re.M))
        self.assertLessEqual(imports, {'__future__', 'copy', 'json', 'pathlib', 're', 'sys'})


class DatosFicticios(unittest.TestCase):
    def test_los_ejemplos_no_contienen_correos_ni_numeros_de_documento(self):
        raw = f37.EXAMPLES.read_text(encoding='utf-8')
        self.assertNotIn('@', raw)
        self.assertIsNone(re.search(r'(?<!\d)\d{8}(?!\d)', raw))

    def test_todo_texto_libre_es_sintetico(self):
        for item in DATA['initial_evidence']:
            self.assertTrue(item['description'].startswith('[SINTÉTICO]'))
        self.assertTrue(DATA['note'].startswith('[SINTÉTICO]'))


if __name__ == '__main__':
    unittest.main()
