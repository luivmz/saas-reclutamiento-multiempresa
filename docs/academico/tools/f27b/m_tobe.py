"""Proceso TO-BE propuesto (Formato 05).

Base versionada:
- docs/final-report/03-procesos-negocio.md §3.3–3.5: cinco subprocesos, flujo implementado y reglas.
- docs/assumptions.md: A-05, A-13, A-16, A-27 a A-31.
- docs/final-report/02-contexto-problema.md §2.3: relación problema → RF.
- Antecedente: TO-BE original del equipo, anexo A del F9 v1.0 (imagen). Incluye la rama «cerrar sin
  selección», que el prototipo no implementa (A-30).

Estado: TO-BE PROPUESTO (su adopción en el Colegio no está validada), soportado por el SOFTWARE
IMPLEMENTADO v1.1 salvo donde se indica «propuesta futura».
"""

SUBPROCESOS = {
    'A': 'Requerimiento de personal',
    'B': 'Convocatoria',
    'C': 'Postulación',
    'D': 'Evaluación',
    'E': 'Selección y cierre',
    'T': 'Transversal',
}

# id, subproceso, actividad, descripción, actor, RF, origen AS-IS
ACTIVIDADES = [
    ('TB-01', 'A', 'Registrar el requerimiento de personal',
     'Registra puesto, área, número de plazas, tipo de contrato, fecha requerida y justificación.',
     'Área solicitante', ['RF-01'], ['AS-01', 'AS-02']),
    ('TB-02', 'A', 'Enviar el requerimiento a RR. HH.',
     'Envía el requerimiento registrado. Queda en estado «enviado», con historial.',
     'Área solicitante', ['RF-02'], ['AS-02']),
    ('TB-03', 'A', 'Revisar el requerimiento y validarlo u observarlo',
     'RR. HH. lo valida o lo observa con un comentario.',
     'RR. HH.', ['RF-02'], ['AS-03']),
    ('TB-04', 'A', 'Corregir y reenviar el requerimiento observado',
     'El área corrige lo observado y lo reenvía a RR. HH.',
     'Área solicitante', ['RF-02'], ['AS-03']),
    ('TB-05', 'A', 'Aprobar o rechazar el requerimiento',
     'Decide sobre el requerimiento validado. El rechazo exige un motivo.',
     'Aprobador / Dirección', ['RF-03'], ['AS-04']),
    ('TB-06', 'A', 'Notificar el rechazo al área solicitante',
     'Aviso automático del rechazo con su motivo.',
     'Sistema', ['RF-04'], ['AS-04']),
    ('TB-07', 'B', 'Crear la vacante y registrar el perfil y los criterios ponderados',
     'Crea la vacante desde un requerimiento aprobado, con perfil del puesto y criterios (etapa, ponderación y rango).',
     'RR. HH.', ['RF-05'], ['AS-05']),
    ('TB-08', 'B', 'Configurar la vacante',
     'Define plazas (sin superar las aprobadas), fechas y demás datos de la convocatoria.',
     'RR. HH.', ['RF-06'], ['AS-05']),
    ('TB-09', 'B', 'Validar la configuración, las ponderaciones y los rangos',
     'Validación automática previa a la publicación. Si no es válida, la vacante no se publica.',
     'Sistema', ['RF-06', 'RF-20'], ['AS-05']),
    ('TB-10', 'B', 'Publicar la vacante en el portal de empleos',
     'La vacante válida queda visible en el portal público.',
     'RR. HH.', ['RF-07'], ['AS-06']),
    ('TB-11', 'C', 'Crear la cuenta e iniciar sesión',
     'El postulante crea su cuenta global de postulante.',
     'Postulante', ['RF-08'], ['AS-07']),
    ('TB-12', 'C', 'Completar el perfil y cargar el CV',
     'Perfil mínimo (sin DNI ni fecha de nacimiento) y CV en PDF privado.',
     'Postulante', ['RF-09'], ['AS-07']),
    ('TB-13', 'C', 'Registrar la postulación',
     'Una sola postulación por vacante publicada y vigente, con perfil completo y CV.',
     'Postulante', ['RF-10'], ['AS-07']),
    ('TB-14', 'C', 'Confirmar la postulación',
     'Código de seguimiento y aviso de recepción al postulante.',
     'Sistema', ['RF-11'], ['AS-07']),
    ('TB-15', 'D', 'Revisar las postulaciones y el expediente',
     'Listado por vacante y expediente con datos, CV e historial.',
     'RR. HH.', ['RF-12'], ['AS-08']),
    ('TB-16', 'D', 'Preseleccionar o descartar',
     'Preselecciona o descarta. El descarte lleva un motivo interno, que no se envía al postulante.',
     'RR. HH.', ['RF-13'], ['AS-09']),
    ('TB-17', 'D', 'Notificar el cambio de etapa al postulante',
     'Aviso de cada cambio de etapa, sin observaciones internas.',
     'Sistema', ['RF-15'], ['AS-09']),
    ('TB-18', 'D', 'Programar la evaluación',
     'Evaluador de la organización, fecha futura, modalidad y lugar.',
     'RR. HH.', ['RF-16'], ['AS-10']),
    ('TB-19', 'D', 'Enviar la convocatoria al postulante y el aviso al evaluador',
     'Convocatoria automática con fecha, modalidad, lugar e indicaciones.',
     'Sistema', ['RF-17'], ['AS-10']),
    ('TB-20', 'D', 'Programar la entrevista',
     'Entrevista con evaluador asignado. Usa la misma convocatoria que la evaluación.',
     'RR. HH.', ['RF-18'], ['AS-10']),
    ('TB-21', 'D', 'Registrar puntajes, resultado y observaciones',
     'El evaluador asignado registra una sola vez los puntajes de todos los criterios de la etapa.',
     'Evaluador', ['RF-19'], ['AS-11']),
    ('TB-22', 'D', 'Validar los puntajes dentro del rango de cada criterio',
     'Rechaza puntajes fuera de rango o de criterios ajenos.',
     'Sistema', ['RF-20'], ['AS-11']),
    ('TB-23', 'D', 'Actualizar la etapa de la postulación (finalista o descarte)',
     'Cambios de etapa según la máquina de estados, con historial.',
     'RR. HH.', ['RF-14'], ['AS-11']),
    ('TB-24', 'E', 'Calcular el ranking ponderado explicable',
     'Ranking determinista con aportes por criterio, empates marcados y candidatos incompletos aparte. '
     '**No selecciona ni cambia estados.**',
     'Sistema', ['RF-21'], ['AS-12']),
    ('TB-25', 'E', 'Presentar la comparación de candidatos',
     'Comparación con criterios, promedios, aportes, total y posición. La consultan RR. HH. y el Aprobador / Dirección.',
     'Sistema', ['RF-22'], ['AS-12']),
    ('TB-26', 'E', 'Registrar la decisión final humana',
     '**Decisión humana** con confirmación explícita y justificación. Puede recaer en un finalista que no sea el primero '
     'del ranking. Es única e inmutable por vacante.',
     'Aprobador / Dirección', ['RF-23'], ['AS-13']),
    ('TB-27', 'E', 'Registrar la selección del candidato decidido',
     'Aplica la decisión: la postulación elegida pasa a «seleccionado».',
     'RR. HH.', ['RF-24'], ['AS-14']),
    ('TB-28', 'E', 'Cerrar la convocatoria (con selección)',
     'Solo después de la selección. Las demás postulaciones activas pasan a «no seleccionado».',
     'RR. HH.', ['RF-25'], ['AS-14']),
    ('TB-29', 'E', 'Notificar el resultado a cada postulante',
     'Resultado propio de cada postulante, solo al cerrar, sin puntajes ni datos de otros candidatos.',
     'Sistema', ['RF-26'], ['AS-14']),
    ('TB-30', 'T', 'Registrar la auditoría de las acciones críticas',
     'Registro de solo inserción de cada acción crítica. Lo consulta el Aprobador / Dirección.',
     'Sistema', ['RF-27'], []),
]

FUTURAS = [
    ('TB-F1', 'E', 'Cerrar la convocatoria sin selección (convocatoria desierta)',
     '**Propuesta futura, NO implementada.** Figura en el TO-BE original del equipo (anexo A del F9 v1.0). El '
     'prototipo solo cierra con selección (A-30, RF-25). Para implementarla hace falta un cambio de alcance con un '
     'RF nuevo o una redefinición aprobada de RF-25, y sus pruebas.',
     'RR. HH.', [], []),
]

# Relación problema → solución → mejora → actividades TO-BE → RF (cap. 2 §2.3)
SOLUCIONES = [
    ('P1', 'S-01', 'Registro único por convocatoria en la plataforma multiempresa: requerimiento, vacante con perfil y '
                   'criterios, perfil del postulante con CV privado y expediente de postulación.',
     'Centralización de la información',
     ['TB-01', 'TB-07', 'TB-08', 'TB-12', 'TB-13', 'TB-15'], ['RF-01', 'RF-05', 'RF-06', 'RF-09', 'RF-10', 'RF-12']),
    ('P2', 'S-02', 'Estados e historial sistematizados del requerimiento y de la postulación (quién, cuándo y de qué '
                   'estado a cuál), con transiciones controladas.',
     'Control del avance y responsables identificados',
     ['TB-02', 'TB-03', 'TB-04', 'TB-05', 'TB-16', 'TB-23', 'TB-27', 'TB-28'],
     ['RF-02', 'RF-03', 'RF-13', 'RF-14', 'RF-24', 'RF-25']),
    ('P3', 'S-03', 'Criterios con ponderación y rango definidos antes de publicar; puntajes validados; ranking '
                   'ponderado explicable y comparación común.',
     'Evaluación uniforme y comparable',
     ['TB-07', 'TB-09', 'TB-18', 'TB-19', 'TB-20', 'TB-21', 'TB-22', 'TB-24', 'TB-25'],
     ['RF-05', 'RF-16', 'RF-17', 'RF-18', 'RF-19', 'RF-20', 'RF-21', 'RF-22']),
    ('P4', 'S-04', 'Notificaciones automáticas en cada evento clave: rechazo, recepción, cambio de etapa, '
                   'convocatoria y resultado. No incluyen datos confidenciales.',
     'Comunicación oportuna y con constancia',
     ['TB-06', 'TB-14', 'TB-17', 'TB-19', 'TB-29'], ['RF-04', 'RF-11', 'RF-15', 'RF-17', 'RF-26']),
    ('P5', 'S-05', 'Comparación explicable como apoyo a la decisión humana y auditoría de solo inserción consultable por '
                   'Dirección. **Límite:** los indicadores de gestión del proceso (tiempos, embudo) no se implementan; '
                   'RF-28 es un candidato no implementado.',
     'Sustento y trazabilidad de la decisión (parcial)',
     ['TB-24', 'TB-25', 'TB-26', 'TB-30'], ['RF-21', 'RF-22', 'RF-23', 'RF-27']),
]

OBJETIVOS_MEJORA = [
    ('OM-01', 'Centralizar la información de cada convocatoria en un único registro por organización.', 'P1'),
    ('OM-02', 'Controlar el avance con estados, transiciones válidas e historial con autor y fecha.', 'P2'),
    ('OM-03', 'Evaluar con criterios, ponderaciones y rangos comunes definidos antes de publicar.', 'P3'),
    ('OM-04', 'Eliminar la dependencia de avisos manuales en los eventos clave del proceso.', 'P4'),
    ('OM-05', 'Dar sustento y trazabilidad a la decisión final, que sigue siendo humana.', 'P5'),
]

REGLAS_TOBE = [
    'El ranking **no** cambia estados ni elige a nadie (A-23 a A-27).',
    'La **decisión final** la registra solo el **Aprobador / Dirección** de la organización, con confirmación explícita '
    'y justificación. Puede recaer en un finalista que no sea el primero del ranking (A-27, RF-23).',
    'RR. HH. **aplica** la decisión (selección, RF-24) y cierra (RF-25). No decide.',
    'Tras la decisión no se permiten cambios manuales de etapa (A-28).',
    'La convocatoria solo se cierra **con selección**. El cierre sin selección es una propuesta futura (TB-F1, A-30).',
    'El resultado final se notifica solo al cerrar (A-31).',
    'La consulta del riesgo operacional (RF-29, **experimental**) **no** forma parte del TO-BE base: es informativa, '
    'sobre el proceso, y no interviene en el ranking ni en la decisión.',
]

CORRECCIONES = [
    ('C-01', 'Decisión final', 'Se mantiene **humana** y a cargo del **Aprobador / Dirección** (RF-23). RR. HH. solo '
                               'registra la selección y cierra. Coincide con el TO-BE original del equipo («Aprobador '
                               'toma decisión final»).'),
    ('C-02', 'Cierre sin selección', 'El TO-BE original tenía la rama «cerrar sin selección». Se conserva como '
                                     '**propuesta futura no implementada** (TB-F1), fuera del flujo principal.'),
    ('C-03', 'Ranking', 'Se presenta como apoyo que calcula, ordena y compara. No selecciona (A-23 a A-27).'),
    ('C-04', 'Riesgo operacional (RF-29)', 'Queda fuera del TO-BE base: es experimental y no evalúa personas.'),
    ('C-05', 'Indicadores de gestión (P5)', 'No se presentan como resueltos: RF-28 es un candidato no implementado.'),
]
