"""Pruebas del arnés de evaluación de ML-02 (preparación de F38). Solo biblioteca estándar.

Ejecución, desde la raíz del repositorio:
    python -I -B -m unittest discover -s docs/academico/preparacion-f38-ml02/evaluacion -v

Los valores esperados de la salida degradada están calculados a mano en
F38_Conjunto_Evaluacion_ML02.md, §5, antes de ejecutar el arnés.
"""

import copy
import json
import math
import pathlib
import re
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import f38_evaluar as f38  # noqa: E402

REFS = f38.GOLD.parent / 'salidas_de_referencia'
GOLD_DATA = f38.load(f38.GOLD)


def gold():
    return f38.Gold(copy.deepcopy(GOLD_DATA))


def submission(name):
    return f38.load(REFS / name)


class SalidaPerfecta(unittest.TestCase):
    def test_dev_cumple_todos_los_umbrales(self):
        r = f38.evaluate(gold(), submission('salida_perfecta.json'), 'dev')
        self.assertTrue(r['valid'], r['violations'])
        for key, ok in r['acceptance'].items():
            if key != 'M-07':
                self.assertIs(ok, True, key)
        self.assertEqual(r['metrics']['M-07']['recall_by_stratum'], {'alto': 1.0, 'medio': 1.0, 'nulo': 1.0})
        self.assertAlmostEqual(r['metrics']['M-07']['precision_at_k'], 4 / 9)

    def test_test_esta_sellado_y_cumple_los_umbrales(self):
        r = f38.evaluate(gold(), submission('salida_perfecta.json'), 'test')
        self.assertTrue(r['valid'], r['violations'])
        self.assertIsNone(r['acceptance']['M-04'])  # EI-04 solo tiene casos en dev
        self.assertEqual(r['metrics']['M-07']['queries'], 2)


class SalidaDegradada(unittest.TestCase):
    """Cada error sembrado a mano se refleja en su métrica con el valor calculado de antemano."""

    @classmethod
    def setUpClass(cls):
        cls.r = f38.evaluate(gold(), submission('salida_degradada.json'), 'dev')
        cls.m = cls.r['metrics']

    def test_es_valida_pero_no_se_acepta(self):
        self.assertTrue(self.r['valid'], self.r['violations'])
        self.assertFalse(any(v is True for k, v in self.r['acceptance'].items() if k not in ('M-07', 'M-11', 'M-12')))

    def test_metricas_deterministas(self):
        self.assertAlmostEqual(self.m['M-01'], 2 / 3)
        self.assertEqual(self.m['M-02'], {'precision': 0.5, 'recall': 0.5})
        self.assertEqual(self.m['M-03'], {'detection': 0.5, 'false_positives': 1})
        self.assertEqual(self.m['M-04'], 0.0)
        self.assertEqual(self.m['M-05'], {'recall': 0.5, 'false_rejections': 1})
        self.assertAlmostEqual(self.m['M-06'], 2 / 3)

    def test_metricas_de_recuperacion(self):
        m7 = self.m['M-07']
        ndcg_first = (1 / math.log2(3)) / (1 + 1 / math.log2(3))
        self.assertAlmostEqual(m7['recall_at_k'], 0.5)
        self.assertAlmostEqual(m7['precision_at_k'], 2 / 9)
        self.assertAlmostEqual(m7['mrr'], 0.5)
        self.assertAlmostEqual(m7['ndcg_at_k'], (ndcg_first + 1) / 3)
        self.assertEqual(m7['recall_by_stratum'], {'alto': 1.0, 'medio': 0.0, 'nulo': 0.0})
        self.assertEqual(m7['recall_ci95'], {'status': 'no informativo', 'units': 1})
        self.assertEqual(self.m['M-08'], {'correct_abstention': 0.0, 'false_abstentions': 0})
        self.assertEqual(self.m['M-11'], 1.0)
        self.assertEqual(self.m['M-12'], 0)


class Invalidaciones(unittest.TestCase):
    def test_un_campo_sobre_personas_invalida_el_resultado(self):
        s = submission('salida_perfecta.json')
        s['outputs']['EI-09'][0]['candidate_score'] = 0.9
        r = f38.evaluate(gold(), s, 'dev')
        self.assertFalse(r['valid'])
        self.assertTrue(any('personas o de juicio' in v for v in r['violations']))

    def test_texto_libre_cuenta_en_m12_e_invalida(self):
        s = submission('salida_perfecta.json')
        s['outputs']['EI-07'][0]['fragments'] = ['La persona parece idónea']
        r = f38.evaluate(gold(), s, 'dev')
        self.assertFalse(r['valid'])
        self.assertGreaterEqual(r['metrics']['M-12'], 1)

    def test_una_cita_de_otra_postulacion_falla_la_atribucion(self):
        s = submission('salida_perfecta.json')
        s['outputs']['EI-09'][0]['fragment_refs'] = ['FRG-005']  # FRG-005 es de APP-ML-002
        r = f38.evaluate(gold(), s, 'dev')
        self.assertFalse(r['valid'])
        self.assertLess(r['metrics']['M-11'], 1.0)

    def test_cambiar_un_caso_de_test_rompe_el_sello(self):
        data = copy.deepcopy(GOLD_DATA)
        data['tasks']['EI-05']['cases'][2]['expected'] = 'admision'  # PII-03, partición test
        r = f38.evaluate(f38.Gold(data), submission('salida_perfecta.json'), 'test')
        self.assertFalse(r['valid'])
        self.assertTrue(any('sello' in v for v in r['violations']))

    def test_cambiar_dev_no_toca_el_sello_de_test(self):
        data = copy.deepcopy(GOLD_DATA)
        data['tasks']['EI-05']['cases'][0]['text'] = '[SINTÉTICO] Otro texto de dev.'
        self.assertEqual(f38.Gold(data).seal(), GOLD_DATA['test_seal_sha256'])

    def test_una_salida_de_otro_conjunto_no_se_evalua(self):
        s = submission('salida_perfecta.json')
        s['set_id'] = 'otro'
        self.assertFalse(f38.evaluate(gold(), s, 'dev')['valid'])

    def test_una_clave_camelcase_sobre_personas_invalida(self):
        s = submission('salida_perfecta.json')
        s['outputs']['EI-04']['candidateScore'] = s['outputs']['EI-04']['P-1']
        r = f38.evaluate(gold(), s, 'dev')
        self.assertFalse(r['valid'])
        self.assertTrue(any('personas o de juicio' in v for v in r['violations']))

    def test_una_tarea_fuera_del_catalogo_invalida_aunque_sus_valores_parezcan_validos(self):
        for task in ('ranking', 'EI-99'):
            s = submission('salida_perfecta.json')
            s['outputs'][task] = ['APP-ML-001', 'APP-ML-002']
            r = f38.evaluate(gold(), s, 'dev')
            self.assertFalse(r['valid'], task)

    def test_un_valor_numerico_no_cuela_como_salida(self):
        s = submission('salida_perfecta.json')
        s['outputs']['EI-03'].append(0.93)
        r = f38.evaluate(gold(), s, 'dev')
        self.assertFalse(r['valid'])
        self.assertGreaterEqual(r['metrics']['M-12'], 1)

    def test_una_salida_mal_formada_se_rechaza_sin_romper_el_arnes(self):
        for bad in ('texto', {'EI-01': 'FRG-001'}, {'EI-01': ['FRG-001']}, {'EI-04': []},
                    {'EI-07': [{'query': 'Q-01', 'fragments': 'FRG-001'}]}):
            s = submission('salida_perfecta.json')
            s['outputs'] = bad
            r = f38.evaluate(gold(), s, 'dev')
            self.assertFalse(r['valid'], bad)

    def test_una_particion_no_admitida_nunca_es_valida(self):
        for partition in ('train', 'otra'):
            r = f38.evaluate(gold(), submission('salida_perfecta.json'), partition)
            self.assertFalse(r['valid'], partition)
            self.assertEqual(r['metrics'], {})

    def test_cambiar_k_rompe_el_sello(self):
        data = copy.deepcopy(GOLD_DATA)
        data['tasks']['EI-09']['k'] = 5
        r = f38.evaluate(f38.Gold(data), submission('salida_perfecta.json'), 'test')
        self.assertFalse(r['valid'])
        self.assertTrue(any('sello' in v for v in r['violations']))


class Intervalos(unittest.TestCase):
    def test_la_semilla_es_la_declarada_en_la_especificacion(self):
        self.assertEqual(f38.BOOTSTRAP_SEED, 2381)
        spec = (f38.HERE.parent / 'F38_Conjunto_Evaluacion_ML02.md').read_text(encoding='utf-8')
        self.assertIn(f'semilla {f38.BOOTSTRAP_SEED}', spec)

    def test_el_sello_publicado_coincide_con_el_conjunto_y_la_especificacion(self):
        self.assertEqual(gold().seal(), GOLD_DATA['test_seal_sha256'])
        spec = (f38.HERE.parent / 'F38_Conjunto_Evaluacion_ML02.md').read_text(encoding='utf-8')
        self.assertIn(GOLD_DATA['test_seal_sha256'], spec)

    def test_bootstrap_reproducible_por_vacante(self):
        per_unit = {'VAC-A': (1, 2), 'VAC-B': (2, 2), 'VAC-C': (0, 1)}
        a, b = f38.bootstrap_ci(per_unit), f38.bootstrap_ci(per_unit)
        self.assertEqual(a, b)
        self.assertEqual(a['status'], 'ok')
        self.assertLessEqual(a['low'], 3 / 5)
        self.assertGreaterEqual(a['high'], 3 / 5)

    def test_con_una_sola_unidad_no_es_informativo(self):
        self.assertEqual(f38.bootstrap_ci({'VAC-A': (1, 2)}), {'status': 'no informativo', 'units': 1})


class Conjunto(unittest.TestCase):
    def test_solo_particiones_dev_y_test(self):
        self.assertEqual(set(GOLD_DATA['partitions']), {'dev', 'test'})
        vacancies = [v for vs in GOLD_DATA['partitions'].values() for v in vs]
        self.assertEqual(len(vacancies), len(set(vacancies)))

    def test_todo_texto_es_sintetico_y_las_etiquetas_son_de_fragmentos(self):
        for f in GOLD_DATA['fragments']:
            self.assertTrue(f['text'].startswith('[SINTÉTICO]'))
        for a in GOLD_DATA['tasks']['EI-09']['annotations']:
            self.assertEqual(set(a), {'application', 'criterion', 'fragment', 'relevance', 'stratum'})
            self.assertIn(a['relevance'], {'relevante', 'no_relevante'})

    def test_ningun_campo_del_conjunto_usa_un_token_prohibido(self):
        tokens, bad = f38.forbidden_tokens(), []

        def walk(value):
            if isinstance(value, dict):
                for k, v in value.items():
                    if any(t in tokens for t in re.split(r'[_\W]+', k.lower()) if t):
                        bad.append(k)
                    walk(v)
            elif isinstance(value, list):
                for v in value:
                    walk(v)
        walk(GOLD_DATA)
        self.assertEqual(bad, [])

    def test_el_arnes_solo_importa_la_biblioteca_estandar(self):
        source = pathlib.Path(f38.__file__).read_text(encoding='utf-8')
        imports = set(re.findall(r'^(?:from|import) (\w+)', source, re.M))
        self.assertLessEqual(imports, {'__future__', 'hashlib', 'json', 'math', 'pathlib', 'random', 're', 'sys'})


if __name__ == '__main__':
    unittest.main()
