"""Datos comunes a los Formatos 02 a 08 (Fase 27B)."""

PROYECTO = ('Análisis y Diseño de una Plataforma SaaS Multiempresa para la Gestión del Reclutamiento, '
            'Evaluación y Selección de Personal – Caso de estudio: Colegio Andino de Huancayo')
EQUIPO = 'Coronacion Meza Fredy; Peña Arroyo Anthony; Vila Meza Luis Antonio'
INSTITUCION = 'Colegio Andino de Huancayo (caso de estudio académico)'
PROCESO = 'Reclutamiento, evaluación y selección de personal'
DOCENTE = 'Dr. Maglioni Arana Caparachin'
FECHA = '26/09/2026'
MODULO = 'Plataforma SaaS multiempresa de reclutamiento, evaluación y selección (línea base RF-01 a RF-27)'


def datos(kind='proceso'):
    base = {'Nombre del proyecto': PROYECTO, 'Integrantes del equipo': EQUIPO}
    if kind == 'proceso':
        base.update({'Nombre de la empresa o institución': INSTITUCION, 'Nombre del proceso analizado': PROCESO,
                     'Docente': DOCENTE, 'Fecha de elaboración': FECHA})
    elif kind == 'clave':
        base.update({'Nombre de la empresa o institución': INSTITUCION, 'Nombre del proceso clave': PROCESO,
                     'Docente': DOCENTE, 'Fecha de elaboración': FECHA})
    else:
        base.update({'Módulo / Sistema': MODULO, 'Docente': DOCENTE, 'Fecha': FECHA})
    return base


# Etiquetas de estado epistémico (principio 1 de la F27B)
HV = 'HECHO VERIFICADO'
ASP = 'AS-IS PRELIMINAR'
TBP = 'TO-BE PROPUESTO'
SI = 'SOFTWARE IMPLEMENTADO'
EXP = 'EXPERIMENTAL / PROPUESTO'

LEYENDA = [
    f'**{HV}:** comprobado en el repositorio (código, pruebas ejecutadas, documentos versionados).',
    f'**{ASP}:** reconstrucción del proceso actual hecha por el equipo; **sujeta a validación institucional** '
    '(RR. HH. / Administración del Colegio). No es un procedimiento validado por la institución.',
    f'**{TBP}:** proceso mejorado diseñado por el equipo; su adopción en la institución no está validada.',
    f'**{SI}:** comportamiento de la plataforma v1.1 (etiqueta v1.1.0-academic), verificado con pruebas.',
    f'**{EXP}:** RF-28 (candidato, no implementado), RF-29 (experimental, solo sobre el proceso) y RNF-C (propuesta). '
    'No forman parte de la línea base RF-01 a RF-27.',
]

REGLAS_FIJAS = [
    'La plataforma **nunca** selecciona, descarta ni contrata automáticamente: el ranking calcula, ordena y compara.',
    'La decisión final de selección es **humana**: la registra el Aprobador / Dirección con confirmación explícita '
    'y justificación (RF-23).',
    'Todos los datos de ejemplo son ficticios. No se usan datos personales reales.',
]

# Roles técnicos reales (users.role) — HECHO VERIFICADO: docs/final-report/04-requerimientos.md §4.1
ACTORES_SISTEMA = [
    ('ACT-01', 'Área solicitante', 'solicitante', 'Interno'),
    ('ACT-02', 'Recursos Humanos (RR. HH.)', 'rrhh', 'Interno'),
    ('ACT-03', 'Aprobador / Dirección', 'aprobador', 'Interno'),
    ('ACT-04', 'Postulante', 'postulante', 'Externo'),
    ('ACT-05', 'Evaluador', 'evaluador', 'Interno'),
]
