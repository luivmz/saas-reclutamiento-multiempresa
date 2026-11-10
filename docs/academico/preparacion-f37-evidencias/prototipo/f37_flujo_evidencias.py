"""Prototipo separado del flujo mínimo de evidencias de una vacante (preparación de F37).

PREPARACIÓN — NO IMPLEMENTADO EN EL SAAS. F37-SBX = BLOQUEADA; F36-SBX-GATE = NO SUPERADO.

Qué es: un modelo ejecutable, en memoria y solo con la biblioteca estándar, de las reglas de
`F37_Flujo_Minimo_Evidencias.md`: quién puede registrar, enlazar, revisar, corregir, retirar y
consultar evidencia ficticia, con aislamiento por organización y un registro de solo inserción.

Qué no es: no implementa ninguna capacidad de la matriz EI (no organiza, no alerta, no busca,
no detecta PII ni clasifica), no lee el contenido de la evidencia, no persiste nada, no se conecta
con Laravel y no produce ninguna salida hacia RF-21, RF-23 ni RF-29. Nunca puntúa ni ordena personas.
"""

from __future__ import annotations

import copy
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
EXAMPLES = HERE.parent / 'ejemplos' / 'f37_ejemplos_ficticios.json'
CONTRACT = HERE.parents[1] / 'f36-sbx' / 'contrato' / 'f36sbx_evidence_contract.json'

SYNTHETIC_PREFIX = '[SINTÉTICO]'
WRITES = ('registrar', 'enlazar', 'desenlazar', 'revisar', 'corregir', 'retirar')
READS = ('consultar', 'historial')
ACTIONS = WRITES + READS

# Matriz de permisos por rol (§4 de la especificación). Lo que no figura está denegado.
ROLE_ACTIONS = {
    'rrhh': frozenset({'registrar', 'enlazar', 'desenlazar', 'revisar', 'corregir', 'retirar', 'consultar',
                       'historial'}),
    'aprobador': frozenset({'consultar', 'historial'}),
    'evaluador': frozenset({'registrar', 'enlazar', 'desenlazar', 'corregir', 'consultar'}),
    'solicitante': frozenset(),
    'postulante': frozenset(),
}

# Tipos declarados por una persona (§3). El evaluador solo registra sus observaciones.
EVIDENCE_TYPES = ('cv', 'certificado', 'transcripcion_revisada', 'observacion')
TYPES_BY_ROLE = {'rrhh': frozenset({'cv', 'certificado', 'transcripcion_revisada'}),
                 'evaluador': frozenset({'observacion'})}
# R-09: cada tipo tiene una sola fuente declarada posible.
SOURCE_BY_TYPE = {'cv': 'documento_presentado', 'certificado': 'documento_presentado',
                  'transcripcion_revisada': 'sesion_asignada', 'observacion': 'sesion_asignada'}

AUDIT_ACTION = {
    'registrar': 'evidencia.registrada',
    'enlazar': 'evidencia.enlazada',
    'desenlazar': 'evidencia.enlace_retirado',
    'revisar': 'evidencia.revisada',
    'corregir': 'evidencia.corregida',
    'retirar': 'evidencia.retirada',
}
AUDIT_FIELDS = ('action', 'actor', 'evidence', 'application', 'criterion')


def forbidden_tokens() -> frozenset[str]:
    """Los tokens prohibidos en nombres de campo son los del contrato v4: una sola fuente."""
    contract = json.loads(CONTRACT.read_text(encoding='utf-8'))
    return frozenset(contract['forbidden_field_tokens'])


def field_tokens(field: str) -> list[str]:
    """Palabras de un nombre de campo, con camelCase separado: `candidateScore` da candidate y score."""
    spaced = re.sub(r'(?<=[a-z0-9])(?=[A-Z])', '_', field)
    return [t for t in re.split(r'[_\W]+', spaced.lower()) if t]


class Store:
    """Catálogo ficticio, evidencias inmutables y un registro de eventos de solo inserción.

    Ningún registro se modifica ni se borra después de escribirse (R-04). El estado de una
    evidencia y la vigencia de un enlace se derivan siempre del registro de eventos.
    """

    def __init__(self, data: dict):
        self.users = {u['token']: u for u in data['users']}
        self.vacancies = {v['token']: v for v in data['vacancies']}
        self.applications = {a['token']: a for a in data['applications']}
        self.assignments = {(a['evaluator'], a['application']) for a in data['assignments']}
        self.evidence: dict[str, dict] = {}
        self.events: list[dict] = []
        self._next = 1
        self._tokens = forbidden_tokens()
        for item in data.get('initial_evidence', []):
            params = {k: v for k, v in item.items() if k != 'registered_by'}
            ok, reason = self.execute(item['registered_by'], 'registrar', params)
            if not ok:
                raise ValueError(f'evidencia inicial inválida: {reason}')

    # ------------------------------------------------------------ estado derivado
    def state(self, evidence_id: str) -> str:
        if any(e['supersedes'] == evidence_id for e in self.evidence.values()):
            return 'sustituida'
        actions = {e['action'] for e in self.events if e['evidence'] == evidence_id}
        if 'evidencia.retirada' in actions:
            return 'retirada'
        if 'evidencia.revisada' in actions:
            return 'revisada'
        return 'registrada'

    def is_linked(self, evidence_id: str, criterion: str) -> bool:
        last = None
        for event in self.events:
            if event['evidence'] == evidence_id and event.get('criterion') == criterion:
                last = event['action']
        return last == 'evidencia.enlazada'

    def active_links(self, evidence_id: str) -> list[str]:
        criteria = {e['criterion'] for e in self.events if e['evidence'] == evidence_id and 'criterion' in e}
        return sorted(c for c in criteria if self.is_linked(evidence_id, c))

    @property
    def audit(self) -> list[dict]:
        """Lo que se auditaría: acción, actor y referencias, nunca el texto de la evidencia (R-07)."""
        return [{k: v for k, v in e.items() if k in AUDIT_FIELDS} for e in self.events]

    # ----------------------------------------------------------------- decisión
    def decide(self, actor_token: str, action: str, params: dict) -> tuple[bool, str]:
        """Devuelve (permitido, motivo). Falla cerrado ante cualquier dato desconocido."""
        actor = self.users.get(actor_token)
        if actor is None:
            return False, 'actor desconocido'
        if action not in ACTIONS:
            return False, 'acción desconocida'
        if action not in ROLE_ACTIONS.get(actor['role'], frozenset()):
            return False, f'el rol {actor["role"]} no puede {action}'

        evidence = None
        if 'evidence' in params:
            evidence = self.evidence.get(params['evidence'])
            if evidence is None:
                return False, 'evidencia desconocida'
            app_token = evidence['application']
        else:
            app_token = params.get('application')
        application = self.applications.get(app_token)
        if application is None:
            return False, 'postulación desconocida'
        vacancy = self.vacancies[application['vacancy']]

        # R-01: aislamiento entre organizaciones.
        if actor['org'] != application['org'] or vacancy['org'] != application['org']:
            return False, 'otra organización'
        if evidence is not None and evidence['org'] != application['org']:
            return False, 'evidencia de otra organización'
        # R-02: el evaluador solo actúa sobre postulaciones asignadas.
        if actor['role'] == 'evaluador' and (actor_token, app_token) not in self.assignments:
            return False, 'evaluador no asignado a esta postulación'
        # R-08: con la vacante cerrada, la evidencia queda congelada.
        if action in WRITES and vacancy['status'] == 'cerrada':
            return False, 'vacante cerrada: evidencia congelada'
        # R-05: en ninguna escritura, un campo sobre la persona ni de juicio, con cualquier grafía.
        if action in WRITES:
            bad = sorted(k for k in params if any(t in self._tokens for t in field_tokens(k)))
            if bad:
                return False, f'campo prohibido: {bad}'

        current = self.state(evidence['id']) if evidence is not None else None
        if action == 'registrar':
            if evidence is not None:
                return False, 'registrar no recibe una evidencia existente'
            return self._check_new_item(actor, params)
        if evidence is None and action in ('enlazar', 'desenlazar', 'revisar', 'corregir', 'retirar'):
            return False, 'falta la evidencia'
        if action in ('enlazar', 'desenlazar'):
            if current in ('sustituida', 'retirada'):
                return False, 'solo se enlaza evidencia vigente'
            criterion = params.get('criterion')
            if criterion not in vacancy['criteria']:  # R-03
                return False, 'criterio ajeno a la vacante de la postulación'
            linked = self.is_linked(evidence['id'], criterion)
            if action == 'enlazar' and linked:
                return False, 'enlace ya existente'
            if action == 'desenlazar' and not linked:
                return False, 'no hay enlace que retirar'
            return True, 'permitido'
        if action == 'revisar':
            if current != 'registrada':
                return False, 'solo se revisa evidencia registrada y vigente'
            return True, 'permitido'
        if action == 'corregir':
            if current in ('sustituida', 'retirada'):
                return False, 'solo se corrige evidencia vigente'
            if actor['role'] == 'evaluador' and evidence['registered_by'] != actor_token:
                return False, 'el evaluador solo corrige sus propias observaciones'
            # Se autoriza por la evidencia original, antes de mirar los datos de reemplazo.
            if evidence['type'] == 'observacion' and evidence['registered_by'] != actor_token:
                return False, 'una observación solo la corrige su autor'
            fields = {k: v for k, v in params.items() if k != 'evidence'}
            return self._check_new_item(actor, {**fields, 'type': params.get('type', evidence['type'])})
        if action == 'retirar':
            if current in ('sustituida', 'retirada'):
                return False, 'solo se retira evidencia vigente'
            if not str(params.get('reason', '')).startswith(SYNTHETIC_PREFIX):
                return False, 'retirar exige un motivo'
            return True, 'permitido'
        return True, 'permitido'  # consultar e historial, ya filtrados por rol, organización y asignación

    def _check_new_item(self, actor: dict, params: dict) -> tuple[bool, str]:
        kind = params.get('type')
        if kind not in TYPES_BY_ROLE.get(actor['role'], frozenset()):
            return False, 'tipo de evidencia no admitido para este rol'
        if not str(params.get('description', '')).startswith(SYNTHETIC_PREFIX):
            return False, 'el texto debe empezar por [SINTÉTICO]'
        if params.get('source') != SOURCE_BY_TYPE[kind]:
            return False, 'fuente no admitida para este tipo'
        return True, 'permitido'

    # ------------------------------------------------------------------ efecto
    def execute(self, actor_token: str, action: str, params: dict) -> tuple[bool, str]:
        ok, reason = self.decide(actor_token, action, params)
        if not ok or action in READS:
            return ok, reason
        evidence_id = params.get('evidence')
        if action in ('registrar', 'corregir'):
            evidence_id = self._new_item(actor_token, params)
        application = self.evidence[evidence_id]['application']
        event = {'action': AUDIT_ACTION[action], 'actor': actor_token, 'evidence': evidence_id,
                 'application': application}
        if action in ('enlazar', 'desenlazar'):
            event['criterion'] = params['criterion']
        if action == 'retirar':
            event['reason'] = params['reason']
        self.events.append(event)
        if action == 'corregir':
            # La versión nueva hereda los enlaces vigentes de la anterior, como eventos nuevos.
            for criterion in self.active_links(params['evidence']):
                self.events.append({'action': 'evidencia.enlazada', 'actor': actor_token,
                                    'evidence': evidence_id, 'application': application,
                                    'criterion': criterion})
        return ok, reason

    def _new_item(self, actor_token: str, params: dict) -> str:
        org = self.users[actor_token]['org']
        evidence_id = f'EVD-{org.split("-")[1]}-{self._next:04d}'
        self._next += 1
        previous = self.evidence.get(params.get('evidence', ''))
        self.evidence[evidence_id] = {
            'id': evidence_id,
            'org': org,
            'application': previous['application'] if previous else params['application'],
            'type': params.get('type', previous['type'] if previous else None),
            'source': params['source'],
            'description': params['description'],
            'registered_by': actor_token,
            'supersedes': previous['id'] if previous else None,
        }
        return evidence_id

    def visible_evidence(self, actor_token: str, application: str) -> list[str]:
        ok, _ = self.decide(actor_token, 'consultar', {'application': application})
        if not ok:
            return []
        return sorted(e['id'] for e in self.evidence.values() if e['application'] == application)


def load_examples(path: pathlib.Path = EXAMPLES) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


def run_scenarios(data: dict) -> list[str]:
    """Ejecuta cada escenario sobre un estado nuevo y devuelve las discrepancias con lo esperado."""
    errors = []
    for scenario in data['scenarios']:
        store = Store(copy.deepcopy(data))
        for step in scenario.get('setup', []):
            ok, reason = store.execute(step['actor'], step['action'], step['params'])
            if not ok:
                errors.append(f'{scenario["id"]}: la preparación falló ({reason})')
        ok, reason = store.decide(scenario['actor'], scenario['action'], scenario['params'])
        expected = scenario['expected'] == 'permitido'
        if ok != expected:
            errors.append(f'{scenario["id"]}: esperado {scenario["expected"]}, obtenido '
                          f'{"permitido" if ok else "denegado"} ({reason})')
    return errors


def main() -> int:
    data = load_examples()
    errors = run_scenarios(data)
    for line in errors:
        print('FALLA', line)
    print(f'f37_flujo_evidencias: {len(data["scenarios"]) - len(errors)} escenarios conformes, '
          f'{len(errors)} fallas')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
