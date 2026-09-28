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
    ('AA-04', 'Evaluadores', 'Interno (supuesto de modelado)',
     'Realizan las evaluaciones y entrevistas que se les encargan. Quiénes son en concreto (cargo, área) '
     'no está verificado.'),
    ('AA-05', 'Postulante', 'Externo (supuesto de modelado)', 'Postula con su CV, participa en evaluaciones y entrevistas y recibe el resultado.'),
]
NOTA_SISTEMAS = ('Tipo «Sistemas»: el AS-IS preliminar **no identifica** ninguna herramienta informática '
                 'específica del Colegio. No se afirma que el proceso sea en papel, por correo ni con otra '
                 'herramienta: queda pendiente de validación.')
NOTA_SUPUESTOS = ('«Supuesto de modelado»: la fuente (cap. 3 §3.1) nombra a los evaluadores y a los postulantes, pero no '
                  'dice si los evaluadores son personal del Colegio ni describe la relación del postulante con la '
                  'institución. El tipo lo asigna el equipo para modelar; no es un hecho institucional verificado.')

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
    ('AS-09', 'Revisar el CV y preseleccionar al candidato',
     'RR. HH. revisa el CV de cada candidato y decide si continúa (dentro de SP-01, una vez por candidato). No está '
     'verificado si se informa a quien no continúa.', 5,
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

# Elementos BPMN del AS-IS (Formato 03). Especificación cerrada: F27D, hallazgos F27C H-01, H-02 y H-13.
# Nombres oficiales únicos (glosario). Cualquier artefacto (formato, borrador, pendiente de PowerDesigner) usa estos.
GLOSARIO = [
    ('EI-01', 'Evento de inicio (pool Colegio)', 'Necesidad de personal identificada'),
    ('G-01', 'Compuerta exclusiva', '¿Necesidad aprobada?'),
    ('EF-01', 'Evento de fin del proceso', 'Necesidad no aprobada'),
    ('SP-01', 'Subproceso de instancia múltiple (paralela), una instancia por candidato',
     'Evaluar al candidato'),
    ('SI-01', 'Evento de inicio de SP-01', 'Candidato a evaluar'),
    ('G-02', 'Compuerta exclusiva (dentro de SP-01)', '¿Candidato preseleccionado?'),
    ('EF-02', 'Evento de fin de SP-01', 'El candidato no continúa'),
    ('EF-04', 'Evento de fin de SP-01', 'Candidato evaluado'),
    ('EF-03', 'Evento de fin del proceso', 'Resultado comunicado'),
    ('EP-01', 'Evento de inicio de mensaje (pool Postulante)', 'Convocatoria recibida'),
    ('EP-02', 'Evento de fin (pool Postulante)', 'Postulación presentada'),
]
NOMBRE = {g[0]: g[2] for g in GLOSARIO}

POOL_POSTULANTE = (
    'Pool **Postulante**: participante externo **visible (caja blanca), con comportamiento mínimo**. Contiene: '
    f'EP-01 «{NOMBRE["EP-01"]}» (inicio de mensaje) → AS-07 «Presentar la postulación y el CV» → EP-02 '
    f'«{NOMBRE["EP-02"]}» (fin). No es un pool de caja negra. Los mensajes posteriores (citación y resultado) '
    'llegan al **borde del pool**, sin evento interno, porque el AS-IS no documenta cómo reacciona el postulante; '
    'dibujar esa reacción sería inventarla.'
)

SUBPROCESO = (
    f'**SP-01 «{NOMBRE["SP-01"]}»** es un **subproceso expandido de instancia múltiple paralela**, con una instancia por '
    'candidato cuya postulación reunió AS-08. Contiene SI-01 → AS-09 → G-02 → [No] EF-02 | [Sí] AS-10 → AS-11 → EF-04. '
    'La secuencia del pool continúa hacia AS-12 cuando **todas** las instancias terminaron. No hay otra opción de '
    'modelado.'
)

# Flujos de mensaje: id, origen, destino (participante), elemento receptor, contenido. Todos unidireccionales.
MENSAJES = [
    ('MF-01', 'AS-06 Difundir la convocatoria (Colegio, RR. HH.)', 'Postulante', 'EP-01 Convocatoria recibida', 'Convocatoria'),
    ('MF-02', 'AS-07 Presentar la postulación y el CV (Postulante)', 'Colegio, RR. HH.', 'AS-08 (tarea de recepción)',
     'Postulación y CV'),
    ('MF-03', 'AS-10 Coordinar evaluaciones y entrevistas (Colegio, RR. HH., dentro de SP-01)', 'Postulante',
     'Borde del pool Postulante', 'Citación'),
    ('MF-04', 'AS-14 Comunicar el resultado (Colegio, RR. HH.)', 'Postulante', 'Borde del pool Postulante', 'Resultado'),
]

ELEMENTOS_BPMN = [
    ('Pool (participante)', 'Contenedor de un participante del proceso.',
     '«Colegio Andino de Huancayo — reclutamiento y selección (AS-IS preliminar)», caja blanca con cuatro lanes, y '
     '«Postulante», participante externo visible con comportamiento mínimo (EP-01 → AS-07 → EP-02).'),
    ('Lane (carril)', 'Subdivisión de un pool por responsable.',
     'Área solicitante, RR. HH., Dirección y Evaluadores, dentro del pool del Colegio.'),
    ('Evento de inicio', 'Punto donde empieza el proceso.', f'EI-01 «{NOMBRE["EI-01"]}» (Área solicitante).'),
    ('Evento de inicio de mensaje', 'Inicio disparado por un mensaje.', f'EP-01 «{NOMBRE["EP-01"]}» (pool Postulante, por MF-01).'),
    ('Tarea', 'Trabajo que realiza un actor.', 'AS-01 a AS-14.'),
    ('Tarea de recepción', 'Tarea que espera un mensaje.', 'AS-08 «Recibir y reunir postulaciones y CV» recibe MF-02.'),
    ('Subproceso de instancia múltiple', 'Subproceso que se ejecuta una vez por elemento de una colección.',
     f'SP-01 «{NOMBRE["SP-01"]}», paralelo, una instancia por candidato (AS-09 a AS-11).'),
    ('Compuerta exclusiva', 'Decisión con una sola salida posible.',
     f'G-01 «{NOMBRE["G-01"]}» (Dirección) y G-02 «{NOMBRE["G-02"]}» (RR. HH., dentro de SP-01).'),
    ('Evento de fin', 'Punto donde termina un camino.',
     f'Del proceso: EF-01 «{NOMBRE["EF-01"]}» y EF-03 «{NOMBRE["EF-03"]}». De SP-01: EF-02 «{NOMBRE["EF-02"]}» y '
     f'EF-04 «{NOMBRE["EF-04"]}». Del Postulante: EP-02 «{NOMBRE["EP-02"]}».'),
    ('Flujo de secuencia', 'Orden de ejecución dentro de un pool.',
     'Dentro de cada pool. Incluye AS-06 → AS-08: la tarea de recepción sigue a la difusión.'),
    ('Flujo de mensaje', 'Comunicación entre pools, unidireccional.', 'MF-01 a MF-04 (tabla de mensajes).'),
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
    f'El proceso inicia cuando el **Área solicitante** identifica una necesidad de personal (EI-01 «{NOMBRE["EI-01"]}», '
    'AS-01) y la comunica a RR. HH. (AS-02).',
    f'**RR. HH.** revisa la necesidad (AS-03) y **Dirección** decide si procede (AS-04). En G-01 «{NOMBRE["G-01"]}», si no '
    f'se aprueba, el proceso termina en EF-01 «{NOMBRE["EF-01"]}».',
    'Si se aprueba, RR. HH. define el perfil del puesto (AS-05) y difunde la convocatoria (AS-06). MF-01 lleva la '
    f'convocatoria al pool **Postulante**, donde inicia EP-01 «{NOMBRE["EP-01"]}».',
    f'El Postulante presenta su postulación y su CV (AS-07), que llegan a RR. HH. por MF-02; su pool termina en EP-02 '
    f'«{NOMBRE["EP-02"]}». En el pool del Colegio, AS-06 continúa en **AS-08**, una tarea de recepción que reúne las '
    'postulaciones recibidas.',
    f'Con las postulaciones reunidas se ejecuta **SP-01 «{NOMBRE["SP-01"]}»**, una instancia por candidato. RR. HH. '
    f'revisa el CV (AS-09); en G-02 «{NOMBRE["G-02"]}», si no se preselecciona, la instancia termina en EF-02 '
    f'«{NOMBRE["EF-02"]}». **No está verificado** si se informa a ese candidato.',
    'Si se preselecciona, RR. HH. coordina evaluaciones y entrevistas y cita al candidato (AS-10, MF-03). Los '
    f'**Evaluadores** las realizan y entregan sus resultados (AS-11), y la instancia termina en EF-04 «{NOMBRE["EF-04"]}».',
    'Cuando todas las instancias de SP-01 terminaron, RR. HH. consolida y compara los resultados (AS-12) y Dirección '
    'decide el candidato seleccionado (AS-13).',
    f'RR. HH. comunica el resultado (AS-14, MF-04) y el proceso termina en EF-03 «{NOMBRE["EF-03"]}».',
]
