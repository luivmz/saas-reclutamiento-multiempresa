"""Arquitectura conceptual del sistema (Formato 11 adaptado, Fase 28).

No existe Formato 11 oficial: el entregable es una adaptación académica basada en la Guía de Práctica N.° 11.
Fuentes: F2–F9 (docs/academico/practica-0X), F9 v1.1 (docs/academico/phase-24/output), trazabilidad F2–F9,
ACADEMIC_BASELINE.md y, como referencia técnica sin modificar, docs/v1.1/uml/component-model.md (CO-01, PK-01),
deployment-model.md (DE-01), use-cases.md (UC-01), sequence-diagrams.md (SEQ-07, SEQ-08) y
docs/final-report/07-arquitectura-tecnologica.md. Los componentes son conceptuales: agrupan responsabilidades; no son
clases ni carpetas.
"""

NOTA_ADAPTACION = ('Documento adaptado académicamente a partir de la Guía de Práctica N.° 11. La institución no '
                   'proporcionó un Formato 11 oficial.')

GUIA = [
    ('G-01', 'Revisar el alcance del proyecto', 'Actividad 1 y 2.1'),
    ('G-02', 'Analizar los casos de uso', '2.2'),
    ('G-03', 'Identificar los componentes del sistema', 'Actividad 2 y 2.3'),
    ('G-04', 'Definir la relación entre componentes', 'Actividad 3 y 2.4'),
    ('G-05', 'Representar la arquitectura conceptual (diagrama de bloques)', 'Actividad 4 y 2.5'),
    ('G-06', 'Validar la arquitectura conceptual', 'Actividad 5'),
]

CONTEXTO = [
    ('Problema', 'Proceso de reclutamiento con información distribuida, seguimiento manual, evaluaciones heterogéneas, '
                 'comunicación manual e indicadores limitados (P1–P5, AS-IS preliminar, F4).'),
    ('Objetivo', 'Gestionar de forma centralizada, trazable y multiempresa el ciclo de reclutamiento, evaluación y '
                 'selección, con datos aislados por organización y la decisión final reservada a una persona autorizada.'),
    ('Usuarios', 'Área solicitante, Recursos Humanos, Aprobador / Dirección y Evaluador (personal de la organización) y '
                 'Postulante (cuenta global). No hay superadministrador ni actores comerciales.'),
    ('Entorno', 'Aplicación web usada desde el navegador. Infraestructura de desarrollo, demostración y pruebas con '
                'Docker Compose; no es una plataforma productiva (F9, OUT-09).'),
    ('Alcance incluido', 'IN-01 Requerimientos · IN-02 Vacantes · IN-03 Cuenta y postulación · IN-04 Seguimiento · '
                         'IN-05 Evaluación y entrevista · IN-06 Comparación y ranking · IN-07 Decisión y cierre · IN-08 Auditoría.'),
    ('Alcance excluido', 'Facturación, planes y superadministración SaaS (OUT-01 a OUT-03); selección automática por IA o '
                         'ML (OUT-04); inferencia de idoneidad (OUT-05); banco de talentos (OUT-06); dashboards (OUT-07, '
                         'RF-28 candidato); proveedores externos definitivos (OUT-08); infraestructura productiva (OUT-09); '
                         'integraciones externas (OUT-10); uso productivo o decisorio de RF-29 (OUT-11).'),
    ('Límites', 'Toda lectura y escritura empresarial respeta la organización. El postulante es global y solo ve lo suyo. '
                'Los componentes internos (controladores, servicios, colas, base de datos) no son actores.'),
    ('Restricciones relevantes', 'Monolito modular; multitenencia lógica sin RLS; el ranking no cambia estados ni '
                                 'selecciona; la decisión final exige autorización, confirmación y justificación; CV privados; '
                                 'datos ficticios; RF-29 opcional, experimental y solo con 15 variables operacionales (F9 §10).'),
]

# Casos de uso agrupados por responsabilidad arquitectónica (F8, catálogo aprobado CU-01..CU-20)
CU_GRUPOS = [
    ('Acceso', 'CU-07', 'Cuenta global del postulante; el personal accede con su cuenta y rol', 'C02, C03'),
    ('Requerimientos', 'CU-01, CU-02, CU-03', 'Flujo de estados con validación y aprobación', 'C04'),
    ('Vacantes', 'CU-04, CU-05, CU-06', 'Configuración validada antes de publicar', 'C05'),
    ('Postulantes', 'CU-08', 'Perfil mínimo y CV privado', 'C06, C15'),
    ('Postulaciones', 'CU-09, CU-10, CU-11, CU-12', 'Expediente y máquina de estados de la postulación', 'C07'),
    ('Evaluaciones y entrevistas', 'CU-13, CU-14, CU-15', 'Programación, convocatoria y registro único por criterio', 'C08'),
    ('Ranking', 'CU-16, CU-17', 'Validación de rangos y ponderaciones; cálculo explicable que **no selecciona**', 'C09'),
    ('Decisión', 'CU-18 «Registrar decisión final humana»', 'Solo el Aprobador / Dirección; confirmación y justificación', 'C10'),
    ('Selección y cierre', 'CU-19, CU-20', 'Aplican la decisión humana; cierre solo con selección', 'C11'),
    ('Notificaciones', 'Incluidas en CU-03, CU-09, CU-11, CU-12, CU-13, CU-14 y CU-20', 'Avisos automáticos tras cada evento', 'C12'),
    ('Auditoría', 'RF-27 transversal (CU-21 «Consultar auditoría»: DIFERIDO, fuera del catálogo)', 'Registro de solo inserción y consulta del Aprobador', 'C13'),
]

# Componentes: id, nombre, capa, responsabilidad, RF, CU, actores, estado, fuente
COMPONENTES = [
    ('C01', 'Interfaz web', 'Presentación',
     'Páginas por rol, portal público de empleos y notificaciones propias; presenta datos y envía acciones. No decide.',
     ['RF-01..RF-27 (interacción)'], 'Todos (interfaz)', 'Todos', 'IMPLEMENTADO',
     'CO-01 «Páginas Inertia», «Componentes compartidos»; resources/js/pages'),
    ('C02', 'Autenticación y cuentas', 'Acceso y seguridad',
     'Registro del postulante, inicio de sesión, 2FA y restablecimiento; identifica al usuario y su rol.',
     ['RF-08'], 'CU-07', 'Postulante; personal', 'IMPLEMENTADO', 'CO-01 «Cuenta y acceso» (Fortify)'),
    ('C03', 'Autorización y contexto multiempresa', 'Acceso y seguridad',
     'Autoriza cada operación por rol **y** organización y filtra los datos por `organization_id`. No hay gestión de '
     'organizaciones: la organización es un contexto de aislamiento.',
     ['RNF (seguridad y multitenencia); aplica a RF-01..RF-27'], 'Todos (transversal)', 'Todo el personal',
     'TRANSVERSAL', 'CO-01 «Autorización y multiempresa» (7 Policies, OrganizationScope); cap. 7 §7.3'),
    ('C04', 'Requerimientos de personal', 'Negocio',
     'Registro, envío, validación u observación, corrección y aprobación o rechazo del requerimiento, con historial.',
     ['RF-01', 'RF-02', 'RF-03', 'RF-04'], 'CU-01, CU-02, CU-03', 'Área solicitante, RR. HH., Aprobador / Dirección',
     'IMPLEMENTADO', 'PK-01 «Requerimientos»'),
    ('C05', 'Vacantes y convocatorias', 'Negocio',
     'Crea la vacante desde un requerimiento aprobado, registra perfil y criterios ponderados, valida la configuración '
     'y publica en el portal.',
     ['RF-05', 'RF-06', 'RF-07', 'RF-20'], 'CU-04, CU-05, CU-06, CU-16', 'RR. HH.', 'IMPLEMENTADO', 'PK-01 «Vacantes»'),
    ('C06', 'Postulantes y CV', 'Negocio',
     'Perfil mínimo del postulante (sin DNI ni fecha de nacimiento) y carga del CV en PDF privado.',
     ['RF-09'], 'CU-08', 'Postulante', 'IMPLEMENTADO', 'PK-01 «Postulantes»'),
    ('C07', 'Postulaciones y etapas', 'Negocio',
     'Registro único de postulación, confirmación, revisión del expediente, preselección o descarte y cambios de etapa '
     'con historial.',
     ['RF-10', 'RF-11', 'RF-12', 'RF-13', 'RF-14', 'RF-15'], 'CU-09, CU-10, CU-11, CU-12', 'Postulante, RR. HH., Aprobador / Dirección (consulta)',
     'IMPLEMENTADO', 'PK-01 «Postulaciones» y «Postulantes» (ApplicationService)'),
    ('C08', 'Evaluaciones y entrevistas', 'Negocio',
     'Programación de sesiones con evaluador de la organización, convocatoria y registro único de puntajes, resultado y '
     'observaciones, validados contra rangos.',
     ['RF-16', 'RF-17', 'RF-18', 'RF-19', 'RF-20'], 'CU-13, CU-14, CU-15, CU-16', 'RR. HH., Evaluador',
     'IMPLEMENTADO', 'PK-01 «Evaluaciones» (evaluaciones y entrevistas en un solo módulo)'),
    ('C09', 'Ranking y comparación', 'Negocio',
     'Calcula un ranking ponderado, determinista y explicable y presenta la comparación. **Es apoyo: no selecciona, no '
     'descarta ni cambia estados.**',
     ['RF-20', 'RF-21', 'RF-22'], 'CU-16, CU-17', 'RR. HH., Aprobador / Dirección', 'IMPLEMENTADO',
     'CO-01 «Cálculo de ranking»; PK-01 «Ranking y selección»'),
    ('C10', 'Decisión final humana', 'Negocio',
     'Registra la decisión del **Aprobador / Dirección** con confirmación explícita y justificación; única e inmutable '
     'por vacante. No cambia estados por sí misma.',
     ['RF-23'], 'CU-18', 'Aprobador / Dirección', 'IMPLEMENTADO', 'CO-01 FinalDecisionService; SEQ-07; ADR-002'),
    ('C11', 'Selección y cierre', 'Negocio',
     'Aplica la decisión registrando la selección y cierra la convocatoria (solo con selección); dispara el resultado '
     'a cada postulante.',
     ['RF-24', 'RF-25', 'RF-26'], 'CU-19, CU-20', 'RR. HH.', 'IMPLEMENTADO', 'PK-01 «Ranking y selección»'),
    ('C12', 'Notificaciones', 'Servicios transversales',
     'Avisos automáticos (rechazo, recepción, cambio de etapa, convocatoria, resultado) en la plataforma y por correo '
     'con driver `log`; se encolan y se envían después del commit.',
     ['RF-04', 'RF-11', 'RF-15', 'RF-17', 'RF-26'], 'Incluidas en CU-03, CU-09, CU-11, CU-12, CU-13, CU-14, CU-20',
     'Postulante, Área solicitante, Evaluador (destinatarios)', 'TRANSVERSAL', 'CO-01 «Notificaciones»'),
    ('C13', 'Auditoría', 'Servicios transversales',
     'Registra de forma de solo inserción cada acción crítica (trigger en la base) y permite al Aprobador / Dirección '
     'consultarla. La consulta no es un CU académico (CU-21 diferido).',
     ['RF-27'], 'Transversal (UC-RF27)', 'Aprobador / Dirección (consulta)', 'TRANSVERSAL', 'CO-01 «Auditoría»; A-33, A-34'),
    ('C14', 'Persistencia de datos (PostgreSQL)', 'Persistencia e infraestructura',
     'Único almacén de datos de negocio, con restricciones de integridad; historiales, notificaciones y auditoría.',
     ['Soporte de RF-01..RF-27'], '—', '—', 'IMPLEMENTADO', 'CO-01 «PostgreSQL 17»; cap. 7 §7.5'),
    ('C15', 'Almacenamiento privado de CV', 'Persistencia e infraestructura',
     'Guarda los CV en un disco privado con nombre UUID; la descarga solo pasa por la Policy.',
     ['RF-09', 'RF-12'], 'CU-08, CU-10', '—', 'IMPLEMENTADO', 'CO-01 «Almacenamiento de CV»; A-12'),
    ('C16', 'Sesiones, caché y cola (Redis)', 'Persistencia e infraestructura',
     'Sesiones, caché y cola de trabajos; el trabajador de cola envía las notificaciones.',
     ['Soporte de C02 y C12'], '—', '—', 'IMPLEMENTADO', 'CO-01 «Redis 7», «Trabajador de cola»; cap. 7 §7.6'),
    ('C17', 'Riesgo operacional del proceso (RF-29)', 'Experimental (opcional)',
     'Estima el riesgo de demora del **proceso** de una vacante con 15 variables operacionales y un servicio de '
     'inferencia externo opcional. Información descriptiva. **No evalúa candidatos, no decide, no ordena ni modifica el '
     'ranking** y no guarda su resultado.',
     ['RF-29 (candidato, experimental)'], '— (fuera del catálogo; UC-RF29)', 'RR. HH., Aprobador / Dirección (consulta)',
     'EXPERIMENTAL', 'CO-01 «Riesgo operacional» y «Servicio de inferencia»; SEQ-08; ADR-001; ADR-004'),
]

EXCLUIDOS = [
    ('X-01', 'Panel operativo / reportes', 'NO IMPLEMENTADO (RF-28, candidato)',
     'RF-28 es un panel descriptivo candidato; no tiene rutas, pantallas ni pruebas. No es un componente de la arquitectura. '
     'La página «panel» existente es solo la portada por rol de C01.'),
    ('X-02', 'Gestión de organizaciones / superadministración', 'FUERA DE ALCANCE (OUT-03)',
     'No hay actores ni CU de gestión comercial global. Las organizaciones solo definen el contexto de aislamiento (C03).'),
    ('X-03', 'Facturación, planes y suscripciones', 'FUERA DE ALCANCE (OUT-01, OUT-02)', 'Sin requerimiento aprobado.'),
    ('X-04', 'Selección automática, banco de talentos, integraciones externas, infraestructura en nube', 'FUERA DE ALCANCE (OUT-04 a OUT-10)',
     'Contradicen RF-23 o no están en la línea base.'),
]

# Relaciones: id, origen, destino, tipo, información, dependencia, RF/CU, observación
RELACIONES = [
    ('R-01', 'C01', 'C02', 'Solicitud', 'Credenciales, sesión', 'C01 depende de C02 para acceder a lo protegido', 'RF-08 · CU-07', ''),
    ('R-02', 'C02', 'C03', 'Contexto de seguridad', 'Usuario autenticado, rol y organización', 'C03 usa la identidad de C02', 'Todos', ''),
    ('R-03', 'C03', 'C04 a C11, C13', 'Autorización y filtro', 'Permiso por rol y organización; datos filtrados por organization_id',
     'Todos los módulos de negocio dependen de C03 antes de operar', 'RF-01..RF-27', 'El postulante solo ve lo suyo'),
    ('R-04', 'C01', 'C04 a C11, C13', 'Uso', 'Acciones del usuario y datos a presentar', 'C01 invoca los módulos; no decide',
     'CU-01..CU-20', 'Pasa por C03'),
    ('R-05', 'C04', 'C05', 'Flujo de información', 'Requerimiento aprobado (origen de la vacante y plazas)',
     'C05 depende de un requerimiento aprobado', 'RF-03 → RF-05 · CU-03 → CU-04', 'A-08: plazas ≤ aprobadas'),
    ('R-06', 'C05', 'C07', 'Flujo de información', 'Vacante publicada y vigente', 'C07 solo acepta postulaciones a vacantes publicadas',
     'RF-07 → RF-10 · CU-06 → CU-09', ''),
    ('R-07', 'C06', 'C07', 'Flujo de información', 'Perfil completo y referencia al CV vigente', 'C07 exige perfil completo y CV (A-11)',
     'RF-09 → RF-10 · CU-08 → CU-09', ''),
    ('R-08', 'C08', 'C07', 'Uso', 'Postulación elegible; avance automático de etapa al programar (A-16)',
     'C08 depende de C07', 'RF-14, RF-16, RF-18 · CU-13, CU-14', 'Sin dependencia inversa: no hay ciclo'),
    ('R-09', 'C08', 'C09', 'Flujo de información', 'Resultados de sesiones realizadas (puntajes por criterio)',
     'C09 lee los resultados de C08', 'RF-19 → RF-21 · CU-15 → CU-17', 'Solo resultados confirmados (A-23)'),
    ('R-10', 'C09', 'C10', 'Apoyo a la decisión', 'Comparación explicable; instantánea de posición y puntaje',
     'C10 usa C09 solo para mostrar y guardar la instantánea', 'RF-22 → RF-23 · CU-17 → CU-18',
     '**El ranking no elige: decide el Aprobador / Dirección**'),
    ('R-11', 'C10', 'C11', 'Precondición', 'Decisión humana registrada', 'C11 requiere una decisión previa',
     'RF-23 → RF-24 · CU-18 → CU-19', ''),
    ('R-12', 'C11', 'C07', 'Uso', 'Transición a seleccionado y a no seleccionado', 'C11 usa las transiciones de C07',
     'RF-24, RF-25 · CU-19, CU-20', 'Sin dependencia inversa'),
    ('R-13', 'C04 a C11', 'C13', 'Registro', 'Acción crítica (usuario, organización, acción, entidad, fecha)',
     'Los módulos registran en C13 en la misma transacción', 'RF-27', 'C13 no invoca a los módulos'),
    ('R-14', 'C04, C07, C08, C11', 'C12', 'Evento', 'Rechazo, recepción, cambio de etapa, convocatoria, resultado',
     'Los módulos disparan avisos; C12 no invoca a los módulos', 'RF-04, RF-11, RF-15, RF-17, RF-26', 'Después del commit'),
    ('R-15', 'C12', 'C16', 'Encolado', 'Trabajos de notificación', 'C12 depende de la cola', 'RF-04, RF-11, RF-15, RF-17, RF-26', ''),
    ('R-16', 'C04 a C13', 'C14', 'Persistencia', 'Datos de negocio, historiales, notificaciones y auditoría',
     'Todos dependen de C14', 'RF-01..RF-27', 'Auditoría protegida por trigger de solo inserción'),
    ('R-17', 'C06, C07', 'C15', 'Almacenamiento', 'Archivo del CV (escritura; descarga autorizada)', 'C06 y C07 dependen de C15',
     'RF-09, RF-12 · CU-08, CU-10', 'Descarga solo con Policy (C03)'),
    ('R-18', 'C02', 'C16', 'Sesión y caché', 'Sesión del usuario', 'C02 depende de C16', 'RF-08', ''),
    ('R-19', 'C05', 'C17', 'Consulta opcional', '15 variables operacionales del proceso de la vacante (sin identificadores ni PII)',
     'C17 lee datos de la vacante; ningún módulo depende de C17', 'RF-29 (experimental)',
     'Desactivado por defecto; sin C17 la aplicación funciona igual'),
    ('R-20', 'C17', 'C01', 'Información descriptiva', 'Riesgo operacional del proceso y su estado',
     'Solo se muestra en la tarjeta experimental de la vacante', 'RF-29', '**Sin relación con C09, C10 ni C11**'),
]

FLUJO = [
    'El usuario se autentica (C02). El postulante crea una cuenta global; el personal entra con su rol.',
    'C03 establece el contexto: rol y organización. Toda consulta y operación posterior queda filtrada y autorizada.',
    'El **Área solicitante** registra el requerimiento y **RR. HH.** lo valida u observa (C04).',
    'El **Aprobador / Dirección** aprueba o rechaza el requerimiento (C04); el rechazo se notifica (C12).',
    'RR. HH. crea la vacante desde el requerimiento aprobado, configura criterios y publica (C05).',
    'El postulante completa su perfil y su CV (C06, C15) y postula (C07); recibe la confirmación (C12).',
    'RR. HH. revisa, preselecciona o descarta y gestiona las etapas (C07); cada cambio se notifica (C12).',
    'RR. HH. programa evaluaciones y entrevistas; el **Evaluador** registra los resultados (C08).',
    'El ranking calcula y presenta la comparación como **apoyo** (C09).',
    'El **Aprobador / Dirección** registra la **decisión final humana** con confirmación y justificación (C10).',
    'RR. HH. registra la selección y cierra la convocatoria (C11); cada postulante recibe su resultado (C12).',
    'Durante todo el proceso, cada acción crítica queda en la auditoría (C13), persistida en C14.',
    'Las notificaciones se encolan en C16 y se entregan al destinatario (C12).',
]
NOTA_FLUJO = ('Precisión respecto del esquema del encargo: el requerimiento lo **registra el Área solicitante** (RF-01) y '
              'RR. HH. lo valida (RF-02); evaluaciones y entrevistas las registra el mismo rol **Evaluador** (RF-19).')

FLUJO_RF29 = [
    'Solo si el servicio está habilitado (`ML_SERVICE_ENABLED=true`) y la vacante es elegible.',
    'C17 arma 15 variables operacionales del proceso de la vacante: conteos y días; sin identificadores, PII ni texto libre.',
    'C17 consulta el servicio de inferencia externo experimental.',
    'El resultado (riesgo del proceso y estado) se muestra en C01 como información descriptiva y no se guarda.',
    'Sin servicio o con respuesta inválida, el estado es «no disponible» o «solo descriptivo» y el proceso sigue igual. '
    '**Este flujo no toca el ranking, la decisión ni la selección.**',
]

CAPAS = [
    ('Presentación', 'C01'),
    ('Acceso y seguridad', 'C02, C03'),
    ('Negocio', 'C04, C05, C06, C07, C08, C09, C10, C11'),
    ('Servicios transversales', 'C12, C13'),
    ('Persistencia e infraestructura', 'C14, C15, C16'),
    ('Experimental (opcional, fuera de la línea base)', 'C17'),
]
NOTA_CAPAS = ('Organización conceptual para leer la arquitectura. No es una arquitectura física obligatoria ni un '
              'despliegue: el despliegue real está en DE-01 (F23).')

TECNICA = [
    ('Estilo', 'Monolito modular: una sola aplicación Laravel organizada por dominios (cap. 7 §7.2).'),
    ('Backend', 'Laravel 13 (PHP 8.4).'),
    ('Frontend', 'React 19 con TypeScript, servido mediante Inertia 3; sin API REST separada.'),
    ('Persistencia', 'PostgreSQL 17 (único almacén de negocio).'),
    ('Soporte', 'Redis 7 para sesiones, caché y cola; trabajador de cola para notificaciones.'),
    ('Multitenencia', '`organization_id` + scope global + Policies (rol y organización). **Sin RLS de PostgreSQL.**'),
    ('CV', 'Almacenamiento privado de Laravel (disco local privado, nombre UUID) con descarga autorizada.'),
    ('RF-29 experimental', 'Servicio FastAPI/Python externo a Docker Compose, llamado por HTTP interno autenticado; '
                           'opcional y desactivado por defecto.'),
    ('Entorno', 'Docker Compose para desarrollo, demostración y pruebas; no productivo (A-36).'),
]

DECISIONES = [
    ('DA-01', 'Monolito modular', 'Un solo despliegue simple, con módulos por dominio y trazabilidad RF → código',
     'cap. 7 §7.2; F9 §10.1', 'Mantenibilidad (RNF-09); sin microservicios generales'),
    ('DA-02', 'Multitenencia lógica (`organization_id`, scopes y Policies)', 'Aislar organizaciones en la capa de aplicación',
     'cap. 7 §7.3; A-04; F9 §10.1', 'RNF-02; RLS queda como recomendación'),
    ('DA-03', 'Decisión final humana', 'El sistema nunca selecciona; decide el Aprobador / Dirección con confirmación y justificación',
     'ADR-002; RF-23; A-27', 'C10 separado de C09; RF-23'),
    ('DA-04', 'Auditoría transversal de solo inserción', 'Trazabilidad de acciones críticas no alterable',
     'A-33, A-34; DEF-07', 'C13 y trigger; RNF-03'),
    ('DA-05', 'CV en almacenamiento privado', 'Minimizar la exposición de datos del postulante', 'A-12, A-15', 'C15; RNF-04'),
    ('DA-06', 'Ranking configurable como apoyo', 'Comparación explicable sin decidir', 'A-23 a A-27; RF-21, RF-22',
     'C09 no cambia estados; RNF-10'),
    ('DA-07', 'RF-29 separado de la selección', 'El ML solo evalúa el proceso, nunca personas', 'ADR-001; ADR-004; OUT-04, OUT-11',
     'C17 sin relación con C09, C10 ni C11'),
    ('DA-08', 'PostgreSQL como persistencia', 'Restricciones de integridad reales y el mismo motor en pruebas', 'cap. 7 §7.5; A-03',
     'C14; RNF-10'),
    ('DA-09', 'Redis como soporte', 'Sesiones, caché y cola de notificaciones', 'cap. 7 §7.6', 'C16; C12 asíncrono'),
    ('DA-10', 'Inertia entre frontend y backend', 'SPA con React sin API REST separada', 'cap. 7 §7.1–7.2', 'C01 servido por el monolito'),
]

# RNF académicos → decisiones y componentes (estado tomado del F7)
RNF_ARQ = [
    ('RNF-01', 'Seguridad y control de acceso', 'DA-02', 'C02, C03', 'VERIFICADO'),
    ('RNF-02', 'Multitenencia y aislamiento', 'DA-02', 'C03 (todos los módulos)', 'VERIFICADO'),
    ('RNF-03', 'Trazabilidad y auditoría', 'DA-04', 'C13, C14', 'VERIFICADO'),
    ('RNF-04', 'Privacidad', 'DA-05', 'C06, C15, C12 (sin datos de terceros)', 'VERIFICADO'),
    ('RNF-05', 'Usabilidad', 'DA-10', 'C01', 'EVIDENCIA PARCIAL'),
    ('RNF-06', 'Rendimiento', 'DA-01, DA-09',
     'C16 (caché y cola desacoplan el envío de notificaciones); C14. **NO VERIFICADO**: sin línea base ni umbral', 'NO VERIFICADO'),
    ('RNF-07', 'Disponibilidad y recuperabilidad', 'DA-08, DA-09',
     'C14 (transacciones, restricciones), C12 (envío tras el commit). **NO VERIFICADO**: sin respaldo/restauración probado', 'NO VERIFICADO'),
    ('RNF-08', 'Compatibilidad', 'DA-10', 'C01', 'EVIDENCIA PARCIAL'),
    ('RNF-09', 'Mantenibilidad', 'DA-01', 'Todos (módulos por dominio)', 'EVIDENCIA PARCIAL'),
    ('RNF-10', 'Integridad de datos', 'DA-06, DA-08', 'C04, C05, C07, C08, C09, C14', 'VERIFICADO'),
]

LIMITACIONES = [
    'El F11 es una **adaptación académica**: no existe Formato 11 oficial.',
    'El AS-IS de partida (F2 a F4) es **preliminar**, sin validación institucional.',
    'RNF-06 (rendimiento) y RNF-07 (disponibilidad y recuperabilidad): **no verificados**.',
    'H-14: la cabecera del PDF del F4 no aparece en la capa de texto (LOW, pendiente para la F31).',
    'RF-28: candidato **no implementado**; no se modela como componente.',
    'RF-29: **experimental**, opcional y fuera de la línea base; solo evalúa el proceso.',
    'Sin aprobación institucional: la validación de este documento es interna del equipo y académica.',
    'El diagrama es un **borrador**; la vista formal ARQ-01 se modelará en PowerDesigner (F29).',
]

CONCLUSIONES = [
    'La arquitectura conceptual organiza el sistema en **17 componentes** y seis capas conceptuales: 1 de presentación, '
    '2 de acceso y seguridad, 8 de negocio, 2 transversales, 3 de persistencia e infraestructura y 1 experimental.',
    'Cubre **RF-01 a RF-27** y **CU-01 a CU-20** sin componentes huérfanos ni requisitos nuevos.',
    'Mantiene las fronteras del proyecto: la **decisión final es humana** (C10, distinto del ranking C09), la auditoría '
    'es transversal y el riesgo operacional (C17) es **experimental y aislado** de la selección.',
    'Corresponde con la arquitectura técnica implementada (monolito modular Laravel + Inertia/React, PostgreSQL, Redis) '
    'sin confundirla con el despliegue.',
    'Queda lista para su formalización como vista ARQ-01 en PowerDesigner (F29), después de la auditoría de la F28.',
]
