"""Problemas del proceso P1 a P5 (Formato 04).

Base versionada: docs/final-report/02-contexto-problema.md §2.2 (problema, descripción, efecto y validación
pendiente) y §2.3 (RF que atienden cada problema), y la tabla 3.2 del F9 v1.0 (impacto). El documento
fuente original de identificación de problemas del equipo no está en el repositorio (evidence-index.md).

- Tipo: clasificación analítica del equipo según las categorías del Formato 04.
- Prioridad: **priorización analítica del equipo**, no institucional.
- Causas: **hipótesis del equipo** a validar; no son hechos institucionales.
"""

PRIORIZACION = 'priorización analítica del equipo'
ESTADO_EVIDENCIA = ('AS-IS preliminar. Problema definido en el análisis previo del equipo (cap. 2 §2.2; F9 v1.0 §3.2). '
                    'Validación institucional pendiente con {v}.')

PROBLEMAS = [
    dict(id='P1', nombre='Información distribuida', actividades=['AS-02', 'AS-05', 'AS-06', 'AS-08'],
         tipo='Calidad', tipos_sec=['Redundancia'],
         descripcion='Los datos del proceso (requerimiento, perfil del puesto, CV, evaluaciones y decisiones) no están '
                     'centralizados en un único registro por convocatoria.',
         impacto='Dificulta reconstruir el expediente y el estado integral de una postulación; riesgo de pérdida o '
                 'duplicación de información y menor trazabilidad.',
         prioridad='Alta',
         justif='Afecta a todas las etapas y es la base para atender P2, P3 y P5.',
         causa='Ausencia de un registro único por convocatoria',
         causa_desc='Cada etapa conserva su información por separado. No existe un expediente común que reúna la '
                    'necesidad, el perfil, los CV, las evaluaciones y la decisión.',
         bpmn='Pool del Colegio: AS-02 (lane Área solicitante), AS-05, AS-06 y AS-08 (lane RR. HH.) y el mensaje de '
              'postulación y CV (Postulante → AS-08).',
         validacion='RR. HH.'),
    dict(id='P2', nombre='Seguimiento manual', actividades=['AS-02', 'AS-03', 'AS-04', 'AS-09'],
         tipo='Control', tipos_sec=['Tiempo'],
         descripcion='El avance de cada requerimiento y postulación se controla sin estados ni historial sistematizados.',
         impacto='Poca visibilidad del estado del proceso y de quién hizo cada cambio; más esfuerzo para controlar '
                 'etapas y responsables.',
         prioridad='Alta',
         justif='Sin estados ni historial no se puede verificar quién decidió qué ni en qué etapa está cada candidato.',
         causa='Estados del proceso no definidos ni registrados',
         causa_desc='Las etapas del requerimiento y de la postulación no están formalizadas como estados con sus '
                    'transiciones, y los cambios no quedan registrados con autor y fecha.',
         bpmn='AS-02 → AS-03 → AS-04 y la compuerta G-01 (parte 1); AS-09 y la compuerta G-02 (parte 2).',
         validacion='RR. HH.'),
    dict(id='P3', nombre='Evaluaciones heterogéneas', actividades=['AS-11', 'AS-12'],
         tipo='Calidad', tipos_sec=['Control'],
         descripcion='Los candidatos no se evalúan con criterios, ponderaciones y rangos definidos de antemano y '
                     'comunes a toda la convocatoria.',
         impacto='Comparaciones poco objetivas y difíciles de justificar; menor comparabilidad de resultados.',
         prioridad='Alta',
         justif='Incide directamente en la equidad y en el sustento de la decisión final.',
         causa='Criterios de evaluación no definidos antes de evaluar',
         causa_desc='El perfil no fija criterios con ponderación y rango, y los resultados no se registran con una '
                    'escala común por criterio.',
         bpmn='AS-11 (lane Evaluadores) y AS-12 (lane RR. HH.), parte 2.',
         validacion='RR. HH. / Dirección'),
    dict(id='P4', nombre='Comunicación manual', actividades=['AS-07', 'AS-10', 'AS-14'],
         tipo='Tiempo', tipos_sec=['Control'],
         descripcion='Los avisos a postulantes y participantes (recepción, cambios de etapa, convocatorias y resultado) '
                     'dependen de gestiones manuales.',
         impacto='Demoras u omisiones en la comunicación; es difícil comprobar qué se comunicó y cuándo.',
         prioridad='Media',
         justif='Afecta a la experiencia del postulante y a la trazabilidad, pero no altera por sí mismo la '
                'decisión de selección.',
         causa='Avisos que dependen de una gestión manual en cada evento',
         causa_desc='Cada aviso requiere que alguien lo redacte y envíe. No hay un disparador asociado a cada evento '
                    'del proceso ni constancia del envío.',
         bpmn='Flujos de mensaje de AS-06 (convocatoria), AS-07/AS-08 (recepción), AS-10 (citación) y AS-14 (resultado).',
         validacion='RR. HH.'),
    dict(id='P5', nombre='Indicadores limitados', actividades=['AS-12', 'AS-13'],
         tipo='Control', tipos_sec=['Otros: información de gestión'],
         descripcion='No se dispone de información consolidada para comparar candidatos ni de trazabilidad de las '
                     'acciones críticas.',
         impacto='Decisiones con menos sustento, baja capacidad de auditoría y dificultad para medir demoras y '
                 'resultados del proceso.',
         prioridad='Media',
         justif='Condiciona el sustento de la decisión y la mejora continua. La parte de indicadores de gestión '
                'queda fuera de la línea base (RF-28 es un candidato no implementado).',
         causa='Datos no consolidados y sin registro de acciones críticas',
         causa_desc='Los resultados no se integran en una vista comparable y las acciones críticas no dejan un registro '
                    'auditable. Tampoco hay datos agregados del proceso para medir tiempos.',
         bpmn='AS-12 (lane RR. HH.) y AS-13 (lane Dirección), parte 2.',
         validacion='Dirección'),
]

CLASIFICACION = {
    'Problemas de tiempo (retrasos, cuellos de botella)':
        'P4 (tipo principal): avisos manuales con demoras u omisiones. P2 (secundario): sin estados ni historial, '
        'el seguimiento exige más esfuerzo y tiempo. No hay tiempos medidos del AS-IS.',
    'Problemas de calidad (errores, reprocesos)':
        'P1 (principal): riesgo de pérdida o duplicación de información. P3 (principal): comparaciones poco objetivas.',
    'Problemas de control (falta de supervisión o validación)':
        'P2 (principal): cambios sin estados ni responsable registrado. P5 (principal): sin trazabilidad de acciones '
        'críticas. P3 y P4 (secundarios): sin criterios comunes y sin constancia de comunicaciones.',
    'Problemas de redundancia (actividades duplicadas)':
        'P1 (secundario): riesgo de duplicar información entre etapas. **No se identificaron actividades duplicadas '
        'verificadas** en el AS-IS preliminar.',
    'Otros (especificar)':
        'P5 (secundario): falta de información de gestión (indicadores de tiempos y resultados). No se implementa en '
        'la línea base (RF-28 es un candidato no implementado).',
}

CONCLUSION = [
    'El AS-IS preliminar presenta cinco problemas.',
    'Tres se priorizan como **altos** (P1, P2 y P3) porque afectan a la integridad de la información, al control del '
    'avance y a la objetividad de la evaluación, que son la base de una decisión de selección justificable.',
    'P4 y P5 se priorizan como **medios**: afectan a la comunicación y a la medición, sin alterar por sí mismos la '
    'decisión.',
    f'La priorización es una **{PRIORIZACION}**. Las causas son hipótesis del equipo. Ninguna de las dos está '
    'validada por la institución, y no hay tiempos ni costos medidos que cuantifiquen el impacto.',
    'La necesidad de mejora se concreta en el TO-BE del Formato 05.',
]
