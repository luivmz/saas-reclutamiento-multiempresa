"""Proceso AS-IS preliminar (Formatos 02 y 03).

Fuente única versionada del AS-IS: docs/final-report/03-procesos-negocio.md §3.1 (8 actividades
macro, responsables y problemas asociados) y docs/final-report/02-contexto-problema.md §2.1–2.2.
La F27B desagrega esas 8 actividades en 14 sin agregar hechos: cada actividad declara de qué
actividad macro proviene. Canales, herramientas, formatos, tiempos y responsables reales NO se
afirman (pendientes de validación con RR. HH. / Administración del Colegio).
"""

FUENTE_ASIS = 'docs/final-report/03-procesos-negocio.md §3.1'

# Las 8 actividades macro tal como están versionadas (§3.1): (n, actividad, responsable, problemas)
MACRO = [
    (1, 'Detectar la necesidad de personal y comunicarla', 'Área solicitante', 'P1, P2'),
    (2, 'Revisar y aprobar la necesidad', 'RR. HH. / Dirección', 'P2'),
    (3, 'Definir el perfil del puesto y difundir la convocatoria', 'RR. HH.', 'P1'),
    (4, 'Recibir las postulaciones y los CV', 'RR. HH.', 'P1, P4'),
    (5, 'Revisar y preseleccionar candidatos', 'RR. HH.', 'P2'),
    (6, 'Coordinar evaluaciones y entrevistas', 'RR. HH. / Evaluadores', 'P3, P4'),
    (7, 'Consolidar resultados y comparar candidatos', 'RR. HH.', 'P3, P5'),
    (8, 'Decidir y comunicar el resultado', 'Dirección / RR. HH.', 'P4, P5'),
]

# Actores del AS-IS preliminar (sin plataforma: el proceso actual no usa el sistema propuesto)
ACTORES = [
    ('AA-01', 'Área solicitante', 'Interno', 'Detecta la necesidad de personal y la comunica a RR. HH.'),
    ('AA-02', 'Recursos Humanos (RR. HH.)', 'Interno',
     'Revisa la necesidad, define el perfil, difunde la convocatoria, recibe postulaciones, preselecciona, '
     'coordina evaluaciones y entrevistas, consolida resultados y comunica el resultado.'),
    ('AA-03', 'Dirección', 'Interno', 'Aprueba o no la necesidad de personal y decide el candidato a contratar.'),
    ('AA-04', 'Evaluadores', 'Interno',
     'Realizan las evaluaciones y entrevistas que se les encargan. Quiénes son en concreto (cargo, área) '
     'no está verificado.'),
    ('AA-05', 'Postulante', 'Externo', 'Postula con su CV, participa en evaluaciones y entrevistas y recibe el resultado.'),
]
NOTA_SISTEMAS = ('Tipo «Sistemas»: el AS-IS preliminar **no identifica** ninguna herramienta informática '
                 'específica del Colegio. No se afirma que el proceso sea en papel, por correo ni con otra '
                 'herramienta: queda pendiente de validación.')

# Actividades AS-IS: id, nombre, descripción, macro, actores [(actor, rol)], problemas, origen
ACTIVIDADES = [
    ('AS-01', 'Identificar la necesidad de personal',
     'El área detecta que requiere cubrir un puesto (vacante, reemplazo o nueva plaza).', 1,
     [('Área solicitante', 'Ejecuta')], [], 'macro 1'),
    ('AS-02', 'Comunicar la necesidad a RR. HH.',
     'El área transmite la necesidad a RR. HH. El canal y el formato no están verificados.', 1,
     [('Área solicitante', 'Ejecuta'), ('RR. HH.', 'Recibe')], ['P1', 'P2'], 'macro 1'),
    ('AS-03', 'Revisar la necesidad',
     'RR. HH. revisa la necesidad comunicada antes de elevarla a Dirección.', 2,
     [('RR. HH.', 'Ejecuta')], ['P2'], 'macro 2 (desagregación)'),
    ('AS-04', 'Aprobar o no aprobar la necesidad',
     'Dirección decide si la necesidad procede. Si no procede, el proceso termina para esa necesidad.', 2,
     [('Dirección', 'Valida'), ('Área solicitante', 'Recibe')], ['P2'], 'macro 2 (desagregación)'),
    ('AS-05', 'Definir el perfil del puesto',
     'RR. HH. define el perfil del puesto a cubrir.', 3,
     [('RR. HH.', 'Ejecuta')], ['P1'], 'macro 3 (desagregación)'),
    ('AS-06', 'Difundir la convocatoria',
     'RR. HH. da a conocer la convocatoria. Los medios de difusión no están verificados.', 3,
     [('RR. HH.', 'Ejecuta'), ('Postulante', 'Recibe')], ['P1'], 'macro 3 (desagregación)'),
    ('AS-07', 'Presentar la postulación y el CV',
     'La persona interesada presenta su postulación y su CV.', 4,
     [('Postulante', 'Ejecuta'), ('RR. HH.', 'Recibe')], ['P4'], 'macro 4 (desagregación)'),
    ('AS-08', 'Recibir y reunir postulaciones y CV',
     'RR. HH. recibe y reúne las postulaciones de la convocatoria.', 4,
     [('RR. HH.', 'Ejecuta')], ['P1'], 'macro 4'),
    ('AS-09', 'Revisar y preseleccionar candidatos',
     'RR. HH. revisa los CV y decide qué candidatos continúan. No está verificado si se informa a quienes '
     'no continúan.', 5,
     [('RR. HH.', 'Ejecuta')], ['P2'], 'macro 5'),
    ('AS-10', 'Coordinar evaluaciones y entrevistas',
     'RR. HH. coordina fechas y participantes, y cita a los candidatos preseleccionados.', 6,
     [('RR. HH.', 'Ejecuta'), ('Evaluadores', 'Recibe'), ('Postulante', 'Recibe')], ['P4'], 'macro 6 (desagregación)'),
    ('AS-11', 'Realizar evaluaciones y entrevistas',
     'Los evaluadores evalúan y entrevistan a los candidatos y entregan sus resultados. No hay constancia '
     'de criterios, ponderaciones ni rangos comunes definidos de antemano.', 6,
     [('Evaluadores', 'Ejecuta'), ('Postulante', 'Recibe'), ('RR. HH.', 'Recibe')], ['P3'], 'macro 6 (desagregación)'),
    ('AS-12', 'Consolidar resultados y comparar candidatos',
     'RR. HH. reúne los resultados de cada candidato y los compara.', 7,
     [('RR. HH.', 'Ejecuta')], ['P3', 'P5'], 'macro 7'),
    ('AS-13', 'Decidir el candidato seleccionado',
     'Dirección decide a quién seleccionar a partir de la información consolidada.', 8,
     [('Dirección', 'Valida'), ('RR. HH.', 'Recibe')], ['P5'], 'macro 8 (desagregación)'),
    ('AS-14', 'Comunicar el resultado',
     'RR. HH. comunica el resultado a los postulantes. El canal y el alcance de la comunicación no están verificados.', 8,
     [('RR. HH.', 'Ejecuta'), ('Postulante', 'Recibe')], ['P4'], 'macro 8 (desagregación)'),
]

OBSERVACIONES = [
    ('O-01', 'La información de cada convocatoria (necesidad, perfil, CV, evaluaciones y decisión) no está '
             'centralizada en un único registro.', 'P1', 'AS-02, AS-05, AS-06, AS-08'),
    ('O-02', 'El avance de la necesidad y de cada candidato se controla sin estados ni historial sistematizados.',
     'P2', 'AS-02, AS-03, AS-04, AS-09'),
    ('O-03', 'Los candidatos no se evalúan con criterios, ponderaciones y rangos definidos de antemano y comunes '
             'a toda la convocatoria.', 'P3', 'AS-11, AS-12'),
    ('O-04', 'Los avisos a postulantes y participantes dependen de gestiones manuales.', 'P4',
     'AS-07, AS-10, AS-14'),
    ('O-05', 'No hay información consolidada para comparar candidatos ni trazabilidad de las acciones críticas.',
     'P5', 'AS-12, AS-13'),
    ('O-06', 'Punto crítico: la decisión de Dirección (AS-13) depende de la calidad de la consolidación (AS-12).',
     'P3, P5', 'AS-12, AS-13'),
    ('O-07', 'Sin validación institucional: tiempos, canales, formatos, herramientas y responsables reales de cada '
             'actividad deben confirmarse con RR. HH. / Administración del Colegio.', '—', 'Todas'),
]

# Elementos BPMN del AS-IS (Formato 03)
ELEMENTOS_BPMN = [
    ('Pool (participante)', 'Contenedor de un participante del proceso.',
     '«Colegio Andino de Huancayo — reclutamiento y selección (AS-IS preliminar)» y «Postulante» (externo).'),
    ('Lane (carril)', 'Subdivisión de un pool por responsable.',
     'Área solicitante, RR. HH., Dirección y Evaluadores dentro del pool del Colegio.'),
    ('Evento de inicio', 'Punto donde empieza el proceso.', 'EI-01 «Necesidad de personal identificada» (Área solicitante).'),
    ('Tarea', 'Trabajo que realiza un actor.', 'AS-01 a AS-14.'),
    ('Compuerta exclusiva', 'Decisión con una sola salida posible.',
     'G-01 «¿Necesidad aprobada?» (Dirección) y G-02 «¿Candidato preseleccionado?» (RR. HH., por candidato).'),
    ('Evento de fin', 'Punto donde termina un camino del proceso.',
     'EF-01 «Necesidad no aprobada», EF-02 «Candidato no continúa» y EF-03 «Resultado comunicado».'),
    ('Flujo de secuencia', 'Orden de ejecución dentro de un pool.', 'Conecta las tareas y compuertas del Colegio.'),
    ('Flujo de mensaje', 'Comunicación entre pools.',
     'Convocatoria (AS-06 → Postulante), postulación y CV (AS-07 → AS-08), citación (AS-10 → Postulante) y '
     'resultado (AS-14 → Postulante).'),
    ('Anotación', 'Texto aclaratorio.', 'Marca «AS-IS preliminar, sujeto a validación institucional».'),
]

LANES = [
    ('Colegio Andino de Huancayo — AS-IS preliminar', 'Área solicitante'),
    ('Colegio Andino de Huancayo — AS-IS preliminar', 'RR. HH.'),
    ('Colegio Andino de Huancayo — AS-IS preliminar', 'Dirección'),
    ('Colegio Andino de Huancayo — AS-IS preliminar', 'Evaluadores'),
    ('Postulante (externo)', 'Postulante'),
]

FLUJO = [
    'El proceso inicia cuando el **Área solicitante** identifica una necesidad de personal (EI-01, AS-01) y la '
    'comunica a RR. HH. (AS-02).',
    '**RR. HH.** revisa la necesidad (AS-03) y la eleva a **Dirección**, que decide si procede (AS-04). En la '
    'compuerta G-01, si no se aprueba, el camino termina (EF-01) y el área recibe la respuesta.',
    'Si se aprueba, RR. HH. define el perfil del puesto (AS-05) y difunde la convocatoria (AS-06), que llega al '
    '**Postulante** como mensaje.',
    'El Postulante presenta su postulación y CV (AS-07). RR. HH. los recibe y reúne (AS-08).',
    'RR. HH. revisa los CV y preselecciona (AS-09). En G-02, que se evalúa por candidato, quien no es '
    'preseleccionado no continúa (EF-02). **No está verificado** si se le informa.',
    'Para los preseleccionados, RR. HH. coordina evaluaciones y entrevistas y cita a los candidatos (AS-10). Los '
    '**Evaluadores** las realizan y entregan sus resultados (AS-11).',
    'RR. HH. consolida y compara los resultados (AS-12). Dirección decide el candidato seleccionado (AS-13).',
    'RR. HH. comunica el resultado a los postulantes (AS-14) y el proceso termina (EF-03).',
]
