"""Casos de uso (Formato 08): consolidación de las tres vistas existentes, sin destruirlas.

A) 20 CU académicos (CU-01 a CU-20): numeración y relación con RF, actores y bloques IN del F9 (tablas 5 y 8,
   versiones 1.0 y 1.1). **El F9 no registra el nombre de cada CU**: la F27B asigna a cada uno el nombre del RF
   principal que agrupa, sin renumerar.
B) 13 CU agrupados de v1.0 (CU-01 a CU-13): docs/final-report/04-requerimientos.md §4.4 y
   docs/final-report/diagram-reports/03-use-case-report.md.
C) UC-RF técnicos (UC-RF01 a UC-RF29): docs/v1.1/uml/use-cases.md y el diagrama UC-01 de PowerDesigner (F23).
"""

ACTORES = [
    ('ACT-01', 'Área solicitante', 'Interno. Registra, envía y corrige requerimientos; recibe la notificación de rechazo.'),
    ('ACT-02', 'Recursos Humanos', 'Interno. Valida requerimientos y gestiona vacantes, postulaciones, sesiones, selección y cierre. No toma la decisión final.'),
    ('ACT-03', 'Aprobador / Dirección', 'Interno. Aprueba o rechaza requerimientos, consulta la comparación, **registra la decisión final humana** y consulta la auditoría.'),
    ('ACT-04', 'Postulante', 'Externo. Gestiona su cuenta, su perfil, su CV y sus postulaciones; recibe convocatorias, avisos y resultados propios.'),
    ('ACT-05', 'Evaluador', 'Interno. Registra puntajes, resultado y observaciones de las sesiones que tiene asignadas.'),
]
NOTA_ACTORES = ('El Sistema no es un actor: valida, calcula, notifica y audita como parte de los casos (inclusiones). No '
                'existen actores de superadministración ni de facturación (OUT-01 a OUT-03). El servicio de riesgo '
                'operacional (RF-29) es un actor secundario experimental que solo aparece en la vista técnica UC-RF.')

# id, nombre asignado, descripción, actores directos, RF, CU agrupado v1.0, UC-RF, bloque IN (F9), columna y fila del diagrama
CU = [
    ('CU-01', 'Registrar requerimiento de personal', 'El área registra la necesidad de personal.',
     ['ACT-01'], ['RF-01'], 'CU-01', 'UC-RF01', 'IN-01', 0, 1.2),
    ('CU-02', 'Validar y corregir requerimiento', 'RR. HH. valida u observa; el área corrige y reenvía.',
     ['ACT-01', 'ACT-02'], ['RF-02'], 'CU-01 (corregir) · CU-02 (validar)', 'UC-RF02', 'IN-01', 2, 0),
    ('CU-03', 'Aprobar o rechazar requerimiento', 'La Dirección decide sobre el requerimiento validado; el rechazo se notifica.',
     ['ACT-03'], ['RF-03', 'RF-04'], 'CU-03', 'UC-RF03, UC-RF04 «extend»', 'IN-01', 2, 12),
    ('CU-04', 'Registrar perfil y criterios del puesto', 'RR. HH. crea la vacante con perfil y criterios ponderados.',
     ['ACT-02'], ['RF-05'], 'CU-04', 'UC-RF05', 'IN-02', 2, 1),
    ('CU-05', 'Configurar y validar vacante', 'RR. HH. configura la convocatoria; el sistema valida.',
     ['ACT-02'], ['RF-06'], 'CU-04', 'UC-RF06', 'IN-02', 2, 2),
    ('CU-06', 'Publicar vacante', 'RR. HH. publica la vacante válida en el portal.',
     ['ACT-02'], ['RF-07'], 'CU-04', 'UC-RF07', 'IN-02', 2, 3),
    ('CU-07', 'Gestionar cuenta y acceso', 'El postulante crea su cuenta e inicia sesión.',
     ['ACT-04'], ['RF-08'], 'CU-05', 'UC-RF08', 'IN-03', 0, 3.5),
    ('CU-08', 'Gestionar perfil y CV', 'El postulante completa su perfil y carga su CV.',
     ['ACT-04'], ['RF-09'], 'CU-05', 'UC-RF09', 'IN-03', 0, 4.5),
    ('CU-09', 'Registrar postulación', 'El postulante postula y recibe la confirmación.',
     ['ACT-04'], ['RF-10', 'RF-11'], 'CU-06', 'UC-RF10, UC-RF11 «include»', 'IN-03', 0, 5.5),
    ('CU-10', 'Consultar y revisar postulaciones', 'Revisa el listado por vacante y el expediente.',
     ['ACT-02', 'ACT-03'], ['RF-12'], 'CU-07', 'UC-RF12', 'IN-04', 2, 10),
    ('CU-11', 'Registrar preselección o descarte', 'RR. HH. preselecciona o descarta con motivo interno.',
     ['ACT-02'], ['RF-13'], 'CU-07', 'UC-RF13, UC-RF15 «include»', 'IN-04', 2, 4),
    ('CU-12', 'Gestionar cambio de etapa', 'RR. HH. cambia la etapa; el postulante recibe el aviso.',
     ['ACT-02'], ['RF-14', 'RF-15'], 'CU-07', 'UC-RF14, UC-RF15 «include»', 'IN-04', 2, 5),
    ('CU-13', 'Programar evaluación', 'RR. HH. programa la evaluación; se envía la convocatoria.',
     ['ACT-02'], ['RF-16', 'RF-17'], 'CU-08', 'UC-RF16, UC-RF17 «include»', 'IN-05', 2, 6),
    ('CU-14', 'Programar entrevista', 'RR. HH. programa la entrevista; se envía la convocatoria.',
     ['ACT-02'], ['RF-18'], 'CU-08', 'UC-RF18, UC-RF17 «include»', 'IN-05', 2, 7),
    ('CU-15', 'Registrar resultados de evaluación y entrevista', 'El evaluador asignado registra puntajes y resultado.',
     ['ACT-05'], ['RF-19'], 'CU-09', 'UC-RF19', 'IN-05', 0, 8.5),
    ('CU-16', 'Validar rangos y ponderaciones', 'Validación incluida por la configuración, el registro de resultados y el ranking.',
     [], ['RF-20'], 'CU-04 · CU-09', 'UC-RF20', 'IN-06', 1, 6.5),
    ('CU-17', 'Consultar ranking y comparación', 'Ranking y comparación explicables. No selecciona.',
     ['ACT-02', 'ACT-03'], ['RF-21', 'RF-22'], 'CU-10', 'UC-RF21, UC-RF22', 'IN-06', 2, 11),
    ('CU-18', 'Registrar decisión final humana', '**Decisión humana** del Aprobador / Dirección, con confirmación explícita y '
     'justificación. El ranking no elige.',
     ['ACT-03'], ['RF-23'], 'CU-11', 'UC-RF23 «human decision»', 'IN-07', 2, 13),
    ('CU-19', 'Registrar selección', 'RR. HH. aplica la decisión registrada.',
     ['ACT-02'], ['RF-24'], 'CU-12', 'UC-RF24', 'IN-07', 2, 8),
    ('CU-20', 'Cerrar convocatoria y notificar resultado', 'RR. HH. cierra con selección; cada postulante recibe su resultado.',
     ['ACT-02'], ['RF-25', 'RF-26'], 'CU-12', 'UC-RF25, UC-RF26 «include»', 'IN-07', 2, 9),
]

INCLUDES = [('CU-05', 'CU-16', 'include'), ('CU-15', 'CU-16', 'include'), ('CU-17', 'CU-16', 'include')]

# Los 13 CU agrupados de v1.0 (se conservan con su numeración)
AGRUPADOS = [
    ('CU-01', 'Gestionar requerimiento de personal', 'Área solicitante', 'RF-01, RF-02'),
    ('CU-02', 'Validar requerimiento', 'RR. HH.', 'RF-02'),
    ('CU-03', 'Aprobar o rechazar requerimiento', 'Aprobador / Dirección', 'RF-03, RF-04'),
    ('CU-04', 'Configurar y publicar vacante', 'RR. HH.', 'RF-05, RF-06, RF-07, RF-20'),
    ('CU-05', 'Registrarse y gestionar perfil/CV', 'Postulante', 'RF-08, RF-09'),
    ('CU-06', 'Postular a una vacante', 'Postulante', 'RF-10, RF-11'),
    ('CU-07', 'Revisar postulaciones y gestionar etapas', 'RR. HH.', 'RF-12, RF-13, RF-14, RF-15'),
    ('CU-08', 'Programar evaluación o entrevista', 'RR. HH.', 'RF-16, RF-17, RF-18'),
    ('CU-09', 'Registrar resultados de evaluación/entrevista', 'Evaluador', 'RF-19, RF-20'),
    ('CU-10', 'Consultar ranking y comparación', 'RR. HH., Aprobador / Dirección', 'RF-21, RF-22'),
    ('CU-11', 'Registrar decisión final', 'Aprobador / Dirección', 'RF-23'),
    ('CU-12', 'Registrar selección y cerrar convocatoria', 'RR. HH.', 'RF-24, RF-25, RF-26'),
    ('CU-13', 'Consultar auditoría', 'Aprobador / Dirección', 'RF-27'),
]

OBSERVACIONES = [
    ('O-F8-01', 'Nombres de CU-01 a CU-20', '**Resuelto (decisión del equipo, F27D).** El F9 solo numeraba los CU; la F27B '
     'les asignó el nombre del RF principal que agrupan. El equipo aprobó los 20 CU, con CU-18 renombrado a «Registrar '
     'decisión final humana».'),
    ('O-F8-02', 'Consulta de auditoría', '**CU-21 «Consultar auditoría»: DIFERIDO (decisión del equipo, F27D).** No se '
     'añade al catálogo de esta versión. Consulta de auditoría vinculada a RF-27 y ACT-03; cubierta por la vista técnica '
     'UC-RF27 y fuera del catálogo académico CU-01..CU-20 de esta versión.'),
    ('O-F8-03', 'CU-16 sin actor directo', 'Es un caso incluido («include») por CU-05, CU-15 y CU-17. Sus actores '
     'indirectos son RR. HH. (al configurar) y el Evaluador (al registrar). En UML es válido; no es un caso huérfano.'),
    ('O-F8-04', 'CU-10 y el Aprobador', 'El F9 asigna CU-10 solo a RR. HH. La implementación también permite la consulta '
     'del Aprobador / Dirección (UC-RF12), así que se asocian ambos. El F9 publicado no se modifica.'),
    ('O-F8-05', 'Convocatoria de la entrevista', 'La entrevista también envía la convocatoria de RF-17 (UC-RF18 incluye '
     'UC-RF17), aunque el nombre del RF dice «evaluación».'),
    ('O-F8-06', 'Antecedente superado', 'El diagrama de CU del F9 v1.0 (anexo B) mostraba al Administrador de la '
     'Organización, al Superadministrador SaaS, suscripciones y banco de talentos, que están fuera del alcance. La F24 '
     'lo sustituyó por UC-01 (D-04). Se conserva solo como antecedente.'),
    ('O-F8-07', 'Extensiones', 'RF-28 (candidato) y RF-29 (experimental) no forman parte de los 20 CU. Solo aparecen en la '
     'vista técnica UC-RF (UC-RF28 «propuesto v1.1», UC-RF29 «experimental»).'),
]

# Decisión del equipo sobre los casos de uso (F27D, tras la auditoría F27C)
DECISION = [
    ('D-CU-01', 'Los 20 casos de uso académicos (CU-01 a CU-20) quedan **aprobados**. No se amplía el catálogo.'),
    ('D-CU-02', 'CU-18 se renombra a **«Registrar decisión final humana»**. RF-23 conserva su ID. Alias histórico: '
                '«Registrar decisión final» (F27B y CU-11 agrupado de v1.0).'),
    ('D-CU-03', 'CU-21 «Consultar auditoría»: **DIFERIDO**. No forma parte del catálogo de esta versión.'),
    ('D-CU-04', 'La consulta de auditoría se documenta como **capacidad técnica vinculada a RF-27**, sin crear un CU académico.'),
]
NOTA_AUDITORIA = ('Consulta de auditoría vinculada a RF-27 y ACT-03; cubierta por la vista técnica UC-RF27 y fuera del '
                  'catálogo académico CU-01..CU-20 de esta versión.')

# RF transversal sin CU académico propio (H-07): no se mezcla con RF-23
TRANSVERSAL = {
    'RF-27': dict(cu='— (transversal; fuera del catálogo CU-01..CU-20)', agrupado='CU-13', uc='UC-RF27', actor='Sistema (registro) · ACT-03 (consulta)',
                  inb='IN-08', f9='El F9 lo rotula «Incluido en CU-18»; desde la F27D se separa de RF-23 (decisión D-CU-04)'),
}
