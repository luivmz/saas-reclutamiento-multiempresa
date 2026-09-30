"""Variables del proyecto y matriz de operacionalización (fase F29C).

Fuentes normativas: la guía de laboratorio E1 «Desarrollo de software con Inteligencia Artificial» (Pruebas y Calidad de
Software) y su versión L1 (Taller de Investigación 2), en docs/academico/00-fuentes-oficiales/guias-ia/. Reglas que se
aplican tal como las da la guía:

- «La solución es la variable independiente. El problema es la variable dependiente. La metodología, principios y
  herramientas de apoyo suelen ser las variables intermedias.»
- Columnas de la matriz: variables, dimensiones, indicadores, ítems de medición, instrumentos de recolección de datos y
  escala de medición. Cada variable tiene varias dimensiones, cada dimensión varios indicadores y cada indicador varios
  ítems. Instrumentos: ficha de observación, lista de cotejo o cuestionario Likert.
- Los indicadores de la variable dependiente son los que usa la predicción con machine learning.

Fuentes de contenido (versionadas): problemas P1–P5 (m_problems.py, F4), objetivos y soluciones del TO-BE (m_tobe.py,
F5), RF (m_rf.py, F6), RNF (m_rnf.py, F7), CU (m_cu.py, F8), arquitectura (m_arch.py, F11), contrato de variables del
componente experimental RF-29 (docs/v1.1/ml/feature-contract.md) y capítulos 5 y 7 del informe final.

Regla de veracidad: ningún indicador trae un valor medido. La matriz define QUÉ se mide y CON QUÉ; la línea base del
AS-IS no está medida y los cuestionarios Likert no se han aplicado.
"""

HV = 'HECHO VERIFICADO'
ASP = 'AS-IS PRELIMINAR'
TBP = 'TO-BE PROPUESTO'
SI = 'SOFTWARE IMPLEMENTADO'
EXP = 'EXPERIMENTAL / PROPUESTO'
ESTADOS = (HV, ASP, TBP, SI, EXP)

FICHA = 'Ficha de observación (registros de la plataforma)'
COTEJO = 'Lista de cotejo'
LIKERT = 'Cuestionario Likert'
INSTRUMENTOS_GUIA = ('Ficha de observación', 'Lista de cotejo', 'Cuestionario Likert')

RAZON = 'Razón (conteo, %, días)'
NOMINAL = 'Nominal (Sí / No)'
ORDINAL = 'Ordinal (Likert 1–5)'
ORD_ESTADO = 'Ordinal (verificado > parcial > no verificado)'


def ind(id_, nombre, items, instrumento, escala, estado, rf=(), rnf=(), ml=(), fuente=''):
    return dict(id=id_, nombre=nombre, items=list(items), instrumento=instrumento, escala=escala, estado=estado,
                rf=list(rf), rnf=list(rnf), ml=list(ml), fuente=fuente)


VARIABLES = [
    # ------------------------------------------------------------------ variable independiente: la solución
    dict(
        id='VI', tipo='Independiente', rol='La solución (guía E1/L1: «la solución es la variable independiente»)',
        nombre='Plataforma SaaS multiempresa de reclutamiento, evaluación y selección de personal',
        estado=SI,
        conceptual=('Sistema de información web ofrecido como servicio a varias organizaciones, con los datos de cada una '
                    'aislados, que registra, controla y documenta el ciclo de reclutamiento, evaluación y selección de '
                    'personal y apoya —sin sustituirla— la decisión humana.'),
        operacional=('Se mide por la cobertura verificada de sus capacidades en cinco dimensiones (lista de cotejo '
                     'contra la trazabilidad RF → prueba del repositorio) y por la utilidad que perciben sus usuarios '
                     'internos (cuestionario Likert propuesto, todavía no aplicado).'),
        dimensiones=[
            dict(id='VI-D1', nombre='Registro centralizado de la convocatoria (S-01)', indicadores=[
                ind('VI-D1-I1', 'Cobertura funcional del registro único', [
                    '¿Está implementado cada RF de la dimensión (RF-01, RF-05, RF-06, RF-09, RF-10 y RF-12)?',
                    '¿Cada uno tiene al menos una prueba automatizada que lo verifica?',
                    'N.º de casos de uso de la dimensión soportados por la plataforma'],
                    COTEJO, 'Nominal (Sí / No) y razón (conteo)', HV,
                    rf=['RF-01', 'RF-05', 'RF-06', 'RF-09', 'RF-10', 'RF-12'],
                    fuente='docs/final-report/traceability-master.md'),
                ind('VI-D1-I2', 'Utilidad percibida del registro único', [
                    'La plataforma reúne en un solo lugar la información de cada convocatoria',
                    'Encuentro el expediente del postulante sin recurrir a otros medios'],
                    LIKERT + ' (RR. HH. y Área solicitante)', ORDINAL, TBP,
                    rf=['RF-01', 'RF-10', 'RF-12'], fuente='Instrumento propuesto; no aplicado'),
            ]),
            dict(id='VI-D2', nombre='Control del flujo por estados e historial (S-02)', indicadores=[
                ind('VI-D2-I1', 'Cobertura funcional del control por estados', [
                    '¿Está implementado cada RF de la dimensión (RF-02, RF-03, RF-13, RF-14, RF-24 y RF-25)?',
                    '¿Cada uno tiene al menos una prueba automatizada que lo verifica?'],
                    COTEJO, NOMINAL, HV, rf=['RF-02', 'RF-03', 'RF-13', 'RF-14', 'RF-24', 'RF-25'],
                    fuente='docs/final-report/traceability-master.md'),
                ind('VI-D2-I2', 'Transiciones de estado controladas', [
                    'N.º de transiciones permitidas definidas para requerimiento, vacante y postulación',
                    '¿Una transición no permitida se rechaza sin efectos?'],
                    COTEJO, 'Razón (conteo) y nominal (Sí / No)', HV, rf=['RF-02', 'RF-03', 'RF-14'],
                    fuente='cap. 7 §7.2 (enums de estados y transiciones); pruebas de los RF'),
            ]),
            dict(id='VI-D3', nombre='Evaluación estructurada y ranking de apoyo (S-03)', indicadores=[
                ind('VI-D3-I1', 'Cobertura funcional de la evaluación estructurada', [
                    '¿Está implementado cada RF de la dimensión (RF-16 a RF-22)?',
                    '¿Cada uno tiene al menos una prueba automatizada que lo verifica?'],
                    COTEJO, NOMINAL, HV, rf=['RF-16', 'RF-17', 'RF-18', 'RF-19', 'RF-20', 'RF-21', 'RF-22'],
                    rnf=['RNF-10'], fuente='docs/final-report/traceability-master.md'),
                ind('VI-D3-I2', 'Ranking explicable y no decisorio', [
                    '¿El ranking muestra el desglose del puntaje por criterio?',
                    '¿El ranking cambia el estado de alguna postulación? (esperado: No)',
                    '¿Se señalan los empates y los candidatos con evaluación incompleta?'],
                    COTEJO, NOMINAL, HV, rf=['RF-21', 'RF-22'],
                    fuente='cap. 7 §7.8 (RankingService puro); A-23 a A-27'),
            ]),
            dict(id='VI-D4', nombre='Comunicación automática (S-04)', indicadores=[
                ind('VI-D4-I1', 'Cobertura funcional de las notificaciones', [
                    '¿Está implementado cada RF de la dimensión (RF-04, RF-11, RF-15, RF-17 y RF-26)?',
                    '¿Cada uno tiene al menos una prueba automatizada que lo verifica?'],
                    COTEJO, NOMINAL, HV, rf=['RF-04', 'RF-11', 'RF-15', 'RF-17', 'RF-26'],
                    fuente='docs/final-report/traceability-master.md'),
                ind('VI-D4-I2', 'Eventos clave notificados automáticamente', [
                    'N.º de tipos de evento con notificación automática (rechazo, recepción, cambio de etapa, '
                    'convocatoria y resultado)',
                    '¿La notificación se encola y se envía después de confirmar la operación?'],
                    COTEJO, 'Razón (conteo) y nominal (Sí / No)', HV, rf=['RF-04', 'RF-11', 'RF-15', 'RF-17', 'RF-26'],
                    fuente='cap. 7 §7.6 (afterCommit, cola Redis)'),
            ]),
            dict(id='VI-D5', nombre='Decisión humana, trazabilidad y seguridad (S-05)', indicadores=[
                ind('VI-D5-I1', 'Decisión final humana', [
                    '¿Solo el Aprobador / Dirección puede registrar la decisión final?',
                    '¿La decisión exige confirmación explícita y justificación?',
                    '¿Se admite una sola decisión por vacante?'],
                    COTEJO, NOMINAL, HV, rf=['RF-23'],
                    fuente='cap. 7 §7.4 y §7.8 (VacancyPolicy::decide, FinalDecisionRequest); A-27; ADR-002'),
                ind('VI-D5-I2', 'Acceso, trazabilidad y aislamiento de los datos', [
                    '¿Todo acceso exige cuenta propia e inicio de sesión (cuenta del postulante: RF-08)?',
                    'N.º de acciones de negocio auditadas (AuditAction)',
                    '¿El registro de auditoría es de solo inserción?',
                    '¿El acceso a datos de otra organización se rechaza sin efectos (403 o 404)?'],
                    COTEJO, 'Razón (conteo) y nominal (Sí / No)', HV, rf=['RF-08', 'RF-27'],
                    rnf=['RNF-01', 'RNF-02', 'RNF-03', 'RNF-04'],
                    fuente='cap. 7 §7.3 y §7.7; CandidateRegistrationTest; AuthenticationTest; CrossTenantAccessTest; E2E-11'),
            ]),
        ]),
    # ------------------------------------------------------------------ variable dependiente: el problema
    dict(
        id='VD', tipo='Dependiente', rol='El problema (guía E1/L1: «el problema es la variable dependiente»)',
        nombre='Gestión del proceso de reclutamiento, evaluación y selección de personal',
        estado=ASP,
        conceptual=('Conjunto de actividades con que la organización cubre una necesidad de personal, desde el '
                    'requerimiento del área hasta la comunicación del resultado. En el caso de estudio presenta cinco '
                    'problemas (P1 a P5): información distribuida, seguimiento manual, evaluaciones heterogéneas, '
                    'comunicación manual e indicadores limitados. Es un AS-IS preliminar, sin validación institucional.'),
        operacional=('Se mide en cinco dimensiones, una por problema, con indicadores obtenidos de los registros de la '
                     'plataforma (ficha de observación), listas de cotejo y un cuestionario Likert a RR. HH. y al '
                     'Aprobador / Dirección. No hay línea base medida del AS-IS: los indicadores quedan definidos para '
                     'medir el TO-BE. Los indicadores de avance, oportunidad, carga y evaluación contienen las 15 variables '
                     'operacionales que usa el componente experimental RF-29 (la guía pide que los indicadores de la '
                     'variable dependiente sean los de la predicción).'),
        dimensiones=[
            dict(id='VD-D1', nombre='Centralización de la información (P1; OM-01)', indicadores=[
                ind('VD-D1-I1', 'Completitud del expediente', [
                    '% de postulaciones con perfil completo y CV vigente',
                    'N.º de convocatorias con requerimiento aprobado, vacante y criterios vinculados',
                    'N.º de postulaciones recibidas por vacante (ML-FEAT-05)'],
                    FICHA, RAZON, TBP, rf=['RF-01', 'RF-05', 'RF-09', 'RF-10'], ml=['ML-FEAT-05'],
                    fuente='F4 (P1); F5 (OM-01, S-01); feature-contract.md'),
                ind('VD-D1-I2', 'Dispersión de la información del proceso', [
                    'N.º de documentos del proceso que se gestionan fuera de la plataforma',
                    'La información de una convocatoria está disponible en un solo lugar'],
                    COTEJO + ' y ' + LIKERT + ' (RR. HH.)', 'Razón (conteo) y ordinal (Likert 1–5)', TBP,
                    rf=['RF-01', 'RF-10'], fuente='F4 (P1): problema AS-IS preliminar, sin línea base medida'),
            ]),
            dict(id='VD-D2', nombre='Seguimiento y oportunidad del proceso (P2; OM-02)', indicadores=[
                ind('VD-D2-I1', 'Trazabilidad del avance', [
                    '% de cambios de etapa con autor y fecha en el historial',
                    'N.º de cambios de etapa registrados (ML-FEAT-16)',
                    'N.º de postulaciones sin estado actual'],
                    FICHA, RAZON, TBP, rf=['RF-02', 'RF-03', 'RF-13', 'RF-14'], ml=['ML-FEAT-16'],
                    fuente='F4 (P2); F5 (OM-02, S-02); feature-contract.md'),
                ind('VD-D2-I2', 'Oportunidad del proceso respecto de su plazo objetivo', [
                    'Días transcurridos desde la publicación de la vacante (ML-FEAT-01)',
                    'Días restantes hasta el plazo objetivo del proceso (ML-FEAT-02)',
                    'Días desde el último evento operacional del proceso (ML-FEAT-17)',
                    '¿El proceso cerró después de su plazo objetivo? (etiqueta del modelo experimental RF-29)'],
                    FICHA, 'Razón (días) y nominal (Sí / No)', TBP + ' · uso predictivo ' + EXP,
                    ml=['ML-FEAT-01', 'ML-FEAT-02', 'ML-FEAT-17'],
                    fuente='docs/v1.1/ml/problem-definition.md (ML-PROBLEM-01) y feature-contract.md'),
                ind('VD-D2-I3', 'Carga y configuración del proceso', [
                    'Días de la ventana de postulación de la vacante (ML-FEAT-03)',
                    'N.º de plazas de la vacante (ML-FEAT-04)',
                    'N.º de vacantes de la organización abiertas en paralelo (ML-FEAT-18)'],
                    FICHA, RAZON, TBP + ' · uso predictivo ' + EXP, rf=['RF-05', 'RF-07'],
                    ml=['ML-FEAT-03', 'ML-FEAT-04', 'ML-FEAT-18'], fuente='feature-contract.md'),
            ]),
            dict(id='VD-D3', nombre='Uniformidad de la evaluación (P3; OM-03)', indicadores=[
                ind('VD-D3-I1', 'Evaluación con criterios comunes', [
                    '% de evaluaciones con puntaje en todos los criterios de la vacante',
                    'N.º de criterios ponderados configurados por vacante (ML-FEAT-06)',
                    'N.º de puntajes rechazados por estar fuera de rango'],
                    FICHA, RAZON, TBP, rf=['RF-05', 'RF-16', 'RF-19', 'RF-20'], rnf=['RNF-10'], ml=['ML-FEAT-06'],
                    fuente='F4 (P3); F5 (OM-03, S-03); feature-contract.md'),
                ind('VD-D3-I2', 'Avance de evaluaciones y entrevistas', [
                    'Evaluaciones programadas, realizadas y vencidas pendientes (ML-FEAT-08, ML-FEAT-09 y ML-FEAT-11)',
                    'Entrevistas programadas, realizadas y vencidas pendientes (ML-FEAT-12, ML-FEAT-13 y ML-FEAT-15)'],
                    FICHA, RAZON, TBP + ' · uso predictivo ' + EXP, rf=['RF-16', 'RF-17', 'RF-18', 'RF-19'],
                    ml=['ML-FEAT-08', 'ML-FEAT-09', 'ML-FEAT-11', 'ML-FEAT-12', 'ML-FEAT-13', 'ML-FEAT-15'],
                    fuente='feature-contract.md'),
            ]),
            dict(id='VD-D4', nombre='Comunicación con los postulantes (P4; OM-04)', indicadores=[
                ind('VD-D4-I1', 'Cobertura de los avisos del proceso', [
                    '% de cambios de etapa con notificación generada',
                    'N.º de postulantes sin aviso de resultado al cerrar la convocatoria',
                    'N.º de sesiones de evaluación o entrevista convocadas con aviso'],
                    FICHA, RAZON, TBP, rf=['RF-04', 'RF-11', 'RF-15', 'RF-17', 'RF-26'],
                    fuente='F4 (P4); F5 (OM-04, S-04)'),
                ind('VD-D4-I2', 'Dependencia de avisos manuales', [
                    'Los postulantes reciben su resultado sin gestiones manuales de RR. HH.',
                    'Cada etapa del proceso genera su aviso sin intervención adicional'],
                    LIKERT + ' (RR. HH.)', ORDINAL, TBP, rf=['RF-15', 'RF-26'],
                    fuente='Instrumento propuesto; no aplicado'),
            ]),
            dict(id='VD-D5', nombre='Sustento y trazabilidad de la decisión (P5; OM-05)', indicadores=[
                ind('VD-D5-I1', 'Decisión final documentada', [
                    '% de vacantes cerradas con decisión humana registrada y justificada',
                    '% de decisiones con la instantánea del ranking guardada',
                    'N.º de acciones críticas registradas en la auditoría por convocatoria'],
                    FICHA, RAZON, TBP, rf=['RF-21', 'RF-22', 'RF-23', 'RF-27'], rnf=['RNF-03'],
                    fuente='F4 (P5); F5 (OM-05, S-05)'),
                ind('VD-D5-I2', 'Transparencia percibida de la comparación', [
                    'La comparación muestra por qué cada candidato ocupa su posición',
                    'La decisión final queda justificada y se puede consultar después'],
                    LIKERT + ' (Aprobador / Dirección y RR. HH.)', ORDINAL, TBP, rf=['RF-22', 'RF-23'],
                    fuente='Instrumento propuesto; no aplicado'),
            ]),
        ]),
    # ------------------------------------------------------------------ variables intermedias: metodología, principios y herramientas
    dict(
        id='VIN-1', tipo='Intermedia', rol='Metodología (guía E1/L1: «la metodología … suele ser variable intermedia»)',
        nombre='Aseguramiento de la calidad con desarrollo guiado por pruebas (TDD) y pruebas automatizadas',
        estado=HV,
        conceptual=('Enfoque de desarrollo en que cada regla de negocio se escribe primero como una prueba que falla '
                    '(RED) y después se implementa hasta que la prueba pasa (GREEN), complementado con pruebas '
                    'automatizadas de componentes, de extremo a extremo e integración continua.'),
        operacional=('Se mide por los ciclos RED → GREEN documentados, la trazabilidad RF → prueba y los resultados de '
                     'las suites automatizadas y de la integración continua, tal como están registrados en el '
                     'repositorio y en GitHub Actions.'),
        dimensiones=[
            dict(id='VIN-1-D1', nombre='Práctica de TDD', indicadores=[
                ind('VIN-1-D1-I1', 'Ciclos RED → GREEN documentados', [
                    'N.º de ciclos documentados con la salida real de RED y de GREEN',
                    'N.º de RF con al menos una prueba `test_rfNN_*`'],
                    COTEJO, RAZON, HV, fuente='docs/tdd-evidence.md; docs/final-report/traceability-master.md'),
                ind('VIN-1-D1-I2', 'Defectos cubiertos por pruebas de regresión', [
                    'N.º de defectos registrados (DEF-01 a DEF-13)',
                    '¿Cada defecto cerrado indica la prueba o la validación que lo cubre?'],
                    COTEJO, 'Razón (conteo) y nominal (Sí / No)', HV, fuente='docs/defects.md'),
            ]),
            dict(id='VIN-1-D2', nombre='Automatización e integración continua', indicadores=[
                ind('VIN-1-D2-I1', 'Resultado de las suites automatizadas', [
                    'Pruebas PHPUnit superadas, omitidas y fallidas en la última ejecución registrada',
                    'Especificaciones Cypress superadas en la última ejecución registrada'],
                    FICHA.replace('registros de la plataforma', 'registros de ejecución'), RAZON, HV,
                    fuente='README.md (sección Pruebas); docs/testing/cypress-e2e.md'),
                ind('VIN-1-D2-I2', 'Integración continua', [
                    'N.º de ejecuciones de CI en verde sobre el total en develop y main',
                    '¿Cada integración a develop y main tiene su ejecución de CI en verde?'],
                    FICHA.replace('registros de la plataforma', 'registros de GitHub Actions'),
                    'Razón (conteo) y nominal (Sí / No)', HV, fuente='.github/workflows/tests.yml; GitHub Actions'),
            ]),
        ]),
    dict(
        id='VIN-2', tipo='Intermedia', rol='Principio / norma de calidad',
        nombre='Modelo de calidad del producto ISO/IEC 25010 (marco de referencia)',
        estado=HV,
        conceptual=('Modelo normativo que organiza la calidad del producto software en características como la '
                    'seguridad, la usabilidad, la eficiencia de desempeño, la fiabilidad, la compatibilidad y la '
                    'mantenibilidad. En el proyecto es un marco de referencia: el producto no se evaluó ni se '
                    'certificó según la norma.'),
        operacional=('Se mide por el estado de verificación de los diez RNF académicos del Formato 07, agrupados por '
                     'característica de la norma.'),
        dimensiones=[
            dict(id='VIN-2-D1', nombre='Características de calidad cubiertas', indicadores=[
                ind('VIN-2-D1-I1', 'Correspondencia de los RNF con la norma', [
                    '¿Cada RNF está asignado a una característica de la norma?',
                    'N.º de características de la norma con al menos un RNF asociado'],
                    COTEJO, 'Nominal (Sí / No) y razón (conteo)', HV,
                    rnf=['RNF-01', 'RNF-02', 'RNF-03', 'RNF-04', 'RNF-05', 'RNF-06', 'RNF-07', 'RNF-08', 'RNF-09', 'RNF-10'],
                    fuente='docs/academico/practica-07 (F7, columna de categoría); cap. 5'),
                ind('VIN-2-D1-I2', 'RNF con criterio y método de verificación', [
                    '¿Cada RNF tiene un criterio de aceptación medible?',
                    '¿Cada RNF declara su método de verificación?'],
                    COTEJO, NOMINAL, HV,
                    rnf=['RNF-01', 'RNF-02', 'RNF-03', 'RNF-04', 'RNF-05', 'RNF-06', 'RNF-07', 'RNF-08', 'RNF-09', 'RNF-10'],
                    fuente='docs/academico/practica-07 (F7)'),
            ]),
            dict(id='VIN-2-D2', nombre='Estado de verificación de los RNF', indicadores=[
                ind('VIN-2-D2-I1', 'Estado de cada RNF académico', [
                    'N.º de RNF VERIFICADOS',
                    'N.º de RNF con EVIDENCIA PARCIAL',
                    'N.º de RNF NO VERIFICADOS (RNF-06 y RNF-07)'],
                    COTEJO, ORD_ESTADO, HV,
                    rnf=['RNF-01', 'RNF-02', 'RNF-03', 'RNF-04', 'RNF-05', 'RNF-06', 'RNF-07', 'RNF-08', 'RNF-09', 'RNF-10'],
                    fuente='docs/academico/practica-07 (F7)'),
                ind('VIN-2-D2-I2', 'Evidencia y brechas declaradas', [
                    '¿Cada RNF VERIFICADO cita la ejecución o la prueba que lo respalda?',
                    '¿Cada RNF NO VERIFICADO o con EVIDENCIA PARCIAL declara qué le falta?',
                    '¿Se declaran las características no evaluadas (eficiencia de desempeño)?'],
                    COTEJO, NOMINAL, HV, rnf=['RNF-05', 'RNF-06', 'RNF-07'],
                    fuente='docs/academico/practica-07 (F7); cap. 5'),
            ]),
        ]),
    dict(
        id='VIN-3', tipo='Intermedia', rol='Herramientas y principios de arquitectura',
        nombre='Arquitectura modular multiempresa y entorno reproducible',
        estado=HV,
        conceptual=('Organización técnica del sistema como monolito modular (Laravel 13 y React 19 con Inertia, sobre '
                    'PostgreSQL 17 y Redis 7), con aislamiento lógico por organización, un entorno reproducible con '
                    'Docker Compose y control de versiones con Git.'),
        operacional=('Se mide por la modularidad de la arquitectura conceptual (F11), el aislamiento verificado entre '
                     'organizaciones y la reproducibilidad del entorno de desarrollo, demostración y pruebas.'),
        dimensiones=[
            dict(id='VIN-3-D1', nombre='Modularidad', indicadores=[
                ind('VIN-3-D1-I1', 'Componentes y dependencias', [
                    'N.º de componentes conceptuales (CMP-01 a CMP-17)',
                    'N.º de dependencias circulares entre módulos de negocio (esperado: 0)'],
                    COTEJO, RAZON, HV, rnf=['RNF-09'],
                    fuente='docs/academico/practica-11 (F11 y VALIDATION.md)'),
                ind('VIN-3-D1-I2', 'Relaciones entre componentes', [
                    'N.º de relaciones documentadas entre componentes (R-01 a R-20)',
                    '¿Cada relación declara su tipo, la información intercambiada y la dependencia?'],
                    COTEJO, 'Razón (conteo) y nominal (Sí / No)', HV, rnf=['RNF-09'],
                    fuente='docs/academico/practica-11/RELATIONSHIPS.md'),
            ]),
            dict(id='VIN-3-D2', nombre='Aislamiento y reproducibilidad', indicadores=[
                ind('VIN-3-D2-I1', 'Aislamiento multiempresa', [
                    '¿Toda entidad de negocio lleva organization_id?',
                    '¿Pasan las pruebas de acceso cruzado (CrossTenantAccessTest y E2E-11)?'],
                    COTEJO, NOMINAL, HV, rnf=['RNF-02'], fuente='cap. 7 §7.3; tests/Feature/Tenancy'),
                ind('VIN-3-D2-I2', 'Entorno reproducible', [
                    'N.º de servicios de Docker Compose con verificación de salud',
                    '¿El entorno se levanta con los comandos documentados, sin instalar PHP ni Node locales?'],
                    COTEJO, 'Razón (conteo) y nominal (Sí / No)', HV, fuente='docker-compose.yml; docs/docker.md; A-36'),
            ]),
        ]),
    dict(
        id='VIN-4', tipo='Intermedia', rol='Herramienta de apoyo para la predicción (guía E1/L1: machine learning)',
        nombre='Aprendizaje automático experimental para el riesgo operacional del proceso (RF-29)',
        estado=EXP,
        conceptual=('Modelo de clasificación supervisada (regresión logística) que estima el riesgo de que un proceso de '
                    'selección cierre después de su plazo objetivo, a partir de variables operacionales del proceso. Es '
                    'informativo: no evalúa, puntúa, ordena ni selecciona personas, y no toma la decisión.'),
        operacional=('Se describe por las 15 variables operacionales que usa (coinciden con indicadores de la variable '
                     'dependiente), la salida que entrega y sus salvaguardas. Su desempeño solo se midió con datos '
                     'sintéticos: no está validado institucionalmente ni autorizado para producción.'),
        dimensiones=[
            dict(id='VIN-4-D1', nombre='Variables de entrada del proceso', indicadores=[
                ind('VIN-4-D1-I1', 'Disponibilidad de las variables operacionales', [
                    'N.º de variables del contrato de features que la plataforma puede calcular (de 15)',
                    '¿Alguna variable identifica o describe a un candidato? (esperado: No)'],
                    COTEJO, 'Razón (conteo) y nominal (Sí / No)', EXP,
                    ml=['ML-FEAT-01', 'ML-FEAT-02', 'ML-FEAT-03', 'ML-FEAT-04', 'ML-FEAT-05', 'ML-FEAT-06',
                        'ML-FEAT-08', 'ML-FEAT-09', 'ML-FEAT-11', 'ML-FEAT-12', 'ML-FEAT-13', 'ML-FEAT-15',
                        'ML-FEAT-16', 'ML-FEAT-17', 'ML-FEAT-18'],
                    fuente='docs/v1.1/ml/feature-contract.md'),
                ind('VIN-4-D1-I2', 'Datos de entrenamiento y etiqueta', [
                    '¿El modelo se entrenó solo con datos sintéticos?',
                    '¿La etiqueta describe el proceso (cierre después del plazo objetivo) y no a una persona?'],
                    COTEJO, NOMINAL, EXP,
                    fuente='docs/v1.1/ml/dataset-specification.md; docs/v1.1/ml/problem-definition.md'),
            ]),
            dict(id='VIN-4-D2', nombre='Uso informativo y salvaguardas', indicadores=[
                ind('VIN-4-D2-I1', 'Salida limitada al riesgo del proceso', [
                    '¿El resultado se muestra solo como riesgo del proceso en la ficha de la vacante?',
                    '¿El resultado modifica el ranking, la decisión o la selección? (esperado: No)',
                    '¿La aplicación funciona igual cuando el servicio no está disponible?'],
                    COTEJO, NOMINAL, EXP,
                    fuente='ADR-001; ADR-004; docs/v1.1/phase-16-laravel-ml-integration.md'),
                ind('VIN-4-D2-I2', 'Contrato científico congelado', [
                    '¿El modelo servido coincide con la huella SHA-256 registrada en el freeze de la Fase 15B?',
                    '¿El umbral de decisión es el congelado (0.1679418172266036)?'],
                    COTEJO, NOMINAL, EXP,
                    fuente='docs/v1.1/ml/phase-15b-experiment-freeze.json; docs/v1.1/ml/model-card-draft.md'),
            ]),
        ]),
]

RELACIONES = [
    ('VIN-1', 'VI', 'Condiciona la calidad con que se construye la solución', HV),
    ('VIN-2', 'VI', 'Orienta las características de calidad que la solución debe cumplir', HV),
    ('VIN-3', 'VI', 'Define cómo se estructura y se despliega la solución', HV),
    ('VI', 'VD', 'Se propone que mejore la gestión del proceso (P1–P5). Relación no medida', TBP),
    ('VIN-4', 'VD', 'Estima el riesgo de demora con indicadores de la variable dependiente', EXP),
]

NOTA_RELACION = ('La relación VI → VD es la hipótesis de trabajo del proyecto (TO-BE PROPUESTO). No hay línea base del '
                 'AS-IS ni mediciones del TO-BE, así que no se afirma ningún efecto ni beneficio medido.')

# ------------------------------------------------------------------ actividad de la guía E1/L1 (enunciados 1 a 4)
# Texto de los enunciados según la guía E1 (sección «Actividades para la sesión»). «Obligatorio» indica lo que la guía
# pide de forma expresa; nada de esto se completa sin evidencia real registrada por el equipo.
ENUNCIADOS = [
    ('Enunciado 1', 'Usar ChatGPT en su versión gratuita para definir el título del proyecto; hacer con la IA la matriz '
                    'de operacionalización de variables, para conocer los indicadores de la predicción con machine '
                    'learning, y documentar en el informe la matriz y la definición conceptual.',
     'Obligatorio: P-01 a P-04 en ChatGPT gratuito (R-01 a R-04)'),
    ('Enunciado 2', 'Usar los mismos prompts en Gemini, DeepSeek y Copilot; comparar los 4 chatbots y mencionar las '
                    'diferencias cruciales encontradas.',
     'Obligatorio: P-01 a P-04 en Gemini, DeepSeek y Copilot (R-05 a R-16) y el cuadro comparativo'),
    ('Enunciado 3', 'Revisar el chat compartido por el docente y compararlo con el obtenido por el equipo: ¿es igual a lo '
                    'mostrado o hubo problemas para generar la información deseada?, ¿por qué hubo diferencias? Hacer un '
                    'cuadro comparativo de los principales cambios.',
     'Obligatorio: evidencia del chat del docente (T-01), cuadro comparativo y respuesta a las dos preguntas'),
    ('Enunciado 4', 'Usar prompts que den la información necesaria para el capítulo 1 y el capítulo 2, y documentar los '
                    'resultados en la plantilla Word.',
     'Obligatorio: P-05 y P-06 (R-17 y R-18) y su volcado en la plantilla Word'),
]

# Nombre corto (el del registro), nombre para las tablas y dirección de acceso. Las tres últimas son las de la guía.
CHATBOTS_ACCESO = [
    ('ChatGPT', 'ChatGPT (gratuito)', 'https://chatgpt.com/'),
    ('Gemini', 'Gemini', 'https://gemini.google.com/app?hl=es'),
    ('DeepSeek', 'DeepSeek', 'https://chat.deepseek.com/'),
    ('Copilot', 'Copilot', 'https://copilot.microsoft.com/'),
]
CHATBOTS = [c[1] for c in CHATBOTS_ACCESO]

# Chat compartido por el docente en la guía E1 (enunciado 3).
CHAT_DOCENTE = 'https://chatgpt.com/share/68cee8ae-8474-8012-b657-5acd8a0a871c'

CRITERIOS_COMPARACION = [
    'Título propuesto (n.º de palabras; ¿incluye norma, metodología y machine learning?)',
    'Variables identificadas (independiente, dependiente, intermedias)',
    'Diagrama conceptual: ¿el código Python se ejecutó en Google Colab sin corregirlo?',
    'Matriz: n.º de variables, dimensiones, indicadores e ítems; ¿cumple «varios» en cada nivel?',
    'Instrumentos y escalas: ¿solo ficha de observación, lista de cotejo o cuestionario Likert?',
    'Indicadores de la variable dependiente aptos para predecir el riesgo de demora del proceso',
    'Errores, omisiones, datos inventados o propuestas que evalúan o clasifican a personas',
]

ASPECTOS_DOCENTE = [
    'Título',
    'Variables (independiente, dependiente, intermedias)',
    'Diagrama conceptual en código Python',
    'Matriz de operacionalización',
    '¿Se obtuvo la información buscada con los mismos prompts?',
]

PREGUNTAS_E3 = [
    '¿Es igual a lo mostrado por el docente o hubo problemas al generar la información deseada?',
    '¿Por qué cree que sucedieron estas diferencias?',
]

# Título vigente en la línea base académica: P-02 lo fija para que los cuatro chatbots partan del mismo título.
TITULO_BASE = ('Análisis y Diseño de una Plataforma SaaS Multiempresa para la Gestión del Reclutamiento, Evaluación y '
               'Selección de Personal – Caso de estudio: Colegio Andino de Huancayo')

# Prompts de la guía adaptados al proyecto: se conserva el texto y el orden de cada pedido de la guía y se sustituye el
# ejemplo de «productividad laboral» por el caso de estudio. P-01 incorpora el segundo pedido de la guía (añadir
# machine learning al título). (id, uso, enunciado, texto)
PROMPTS = [
    ('P-01', 'Título del proyecto', 'Enunciados 1 y 2',
     'Para comenzar, actúa como un estudiante de pregrado de la carrera universitaria de Ingeniería de Sistemas e '
     'Informática, donde debemos realizar un sistema informático web que ayude a mejorar la gestión del reclutamiento, '
     'la evaluación y la selección de personal de un colegio privado de Huancayo (caso de estudio académico), ofrecido '
     'como plataforma SaaS multiempresa. El sistema también usará herramientas de machine learning para estimar el '
     'riesgo de demora del proceso de selección, sin evaluar ni clasificar a los postulantes. Podrías redactar el título '
     'del proyecto, con máximo 25 palabras; si puedes incluir alguna normativa ISO o metodología de desarrollo en el '
     'título, entonces hazlo.'),
    ('P-02', 'Variables', 'Enunciados 1 y 2',
     f'He definido el título del proyecto de la siguiente forma: "{TITULO_BASE}". Con este título, define la variable '
     'dependiente (donde está el problema), la variable independiente (la solución planteada) y las variables '
     'intermedias (la metodología, los principios y las herramientas de apoyo a utilizarse). Ten en cuenta que el '
     'proyecto busca desarrollar una plataforma web multiempresa que registre y controle el reclutamiento, la evaluación '
     'y la selección de personal. La plataforma se desarrolla con desarrollo guiado por pruebas (TDD) y pruebas '
     'automatizadas, con la norma ISO/IEC 25010 como marco de referencia de calidad y con una arquitectura modular '
     'multiempresa desplegada con Docker. De la plataforma se exportarán indicadores del proceso para predecir, con '
     'herramientas de machine learning, el riesgo de demora del proceso de selección. La decisión final de contratación '
     'la toma siempre una persona. Muéstrame la información de forma breve.'),
    ('P-03', 'Diagrama conceptual', 'Enunciados 1 y 2',
     'Muéstrame el diagrama conceptual para visualizar la relación entre estas variables. Muéstralo en código Python '
     'para poder generar el diagrama en Google Colab.'),
    ('P-04', 'Matriz de operacionalización', 'Enunciados 1 y 2',
     'Con esto en cuenta, ahora vamos a formar la matriz de operacionalización de variables, donde debe tener las '
     'columnas de variables, dimensiones, indicadores, ítems de medición, instrumentos de recolección de datos y escala '
     'de medición: cada variable tiene varias dimensiones; cada dimensión tiene varios indicadores; cada indicador tiene '
     'varios ítems de medición; los instrumentos de medición pueden ser una ficha de observación, una lista de cotejo o '
     'un cuestionario Likert; la escala de medición está relacionada con los indicadores. Hay que tener en cuenta que '
     'los indicadores y los ítems de medición de la variable dependiente (la gestión del proceso de reclutamiento, '
     'evaluación y selección de personal) se utilizarán para predecir con machine learning el riesgo de demora del '
     'proceso; no se evaluará ni se clasificará a los postulantes.'),
    ('P-05', 'Capítulo 1 de la plantilla final', 'Enunciado 4',
     'Con la información del proyecto de esta conversación, redacta el Capítulo 1 «Información general del proyecto» '
     'del informe final, con dos secciones. 1.1 Resumen ejecutivo, de media página a una página: el problema '
     'identificado, la solución tecnológica propuesta, las tecnologías utilizadas (Laravel, React con TypeScript, '
     'PostgreSQL, Redis, Docker, PHPUnit y Cypress), el enfoque de calidad aplicado y los principales resultados '
     'obtenidos. 1.2 Introducción: el contexto general del proyecto, la importancia de las pruebas de software en el '
     'desarrollo moderno, el propósito del sistema y una breve descripción de la estructura del informe en 14 capítulos. '
     'No inventes resultados, cifras, fechas ni nombres de personas: donde falte un dato, escribe [COMPLETAR].'),
    ('P-06', 'Capítulo 2 de la plantilla final', 'Enunciado 4',
     'Redacta ahora el Capítulo 2 «Contexto organizacional y análisis del problema», con dos secciones. 2.1 Contexto de '
     'la organización: descripción del escenario (un colegio privado de Huancayo usado como caso de estudio académico), '
     'sus actividades principales, el área donde se presenta el problema (el reclutamiento, la evaluación y la selección '
     'de docentes y personal) y las herramientas tecnológicas que usa actualmente. 2.2 Identificación del problema: '
     'descripción detallada, causas, consecuencias operativas e impacto en la eficiencia del proceso. Considera cinco '
     'problemas del proceso actual: información distribuida, seguimiento manual, evaluaciones heterogéneas, '
     'comunicación manual con los postulantes e indicadores limitados para sustentar la decisión. Las herramientas '
     'actuales y las cifras del colegio no están validadas: no las inventes y escribe [COMPLETAR] donde falten.'),
]

# Ejecuciones que exige la guía. R-01..R-16: P-01..P-04 en los 4 chatbots (enunciados 1 y 2). R-17 y R-18: P-05 y
# P-06 (enunciado 4), en la misma conversación de ChatGPT que R-01..R-04. (id, chatbot, prompt)
EJECUCIONES = [(f'R-{4 * k + n + 1:02d}', c[0], f'P-0{n + 1}') for k, c in enumerate(CHATBOTS_ACCESO) for n in range(4)]
EJECUCIONES_E4 = [('R-17', 'ChatGPT', 'P-05'), ('R-18', 'ChatGPT', 'P-06')]

REGISTRO = 'evidencias-ia/REGISTRO_EJECUCIONES_IA.md'

# ------------------------------------------------------------------ alcance efectivo del entregable
# La guía E1/L1 propone la actividad completa (enunciados 1 a 4). El alcance efectivo de este entregable lo fija un
# criterio docente que INFORMÓ EL EQUIPO el 30/09/2026: no es texto de la guía ni hay un documento del docente en el
# repositorio. Si el criterio cambia, basta con cambiar el alcance de cada requisito aquí y regenerar.
NO_REQUERIDO = 'NO REQUERIDO PARA EL CIERRE SEGÚN ACLARACIÓN DOCENTE INFORMADA POR EL EQUIPO'
NO_EJECUTADO = 'No ejecutado'

CRITERIO_DOCENTE = (
    'Criterio docente informado por el equipo (30/09/2026): para este entregable no se exige ejecutar la comparación con '
    'Gemini, DeepSeek y Copilot. No es contenido de la guía E1/L1, que sí propone esa actividad comparativa, y el '
    'repositorio no contiene un documento del docente que lo respalde: lo registra el equipo.')

NOTA_E3 = (
    'El enunciado 3 (comparar con el chat compartido por el docente) también es una actividad comparativa. La aclaración, '
    'tal como la informó el equipo, nombra solo Gemini, DeepSeek y Copilot. El equipo decidió dejar también el enunciado '
    '3 fuera del alcance efectivo, porque lo asocia a la misma actividad comparativa no exigida. Conviene confirmarlo con '
    'el docente.')

# Requisitos de la guía y su alcance en este entregable: (id, enunciado, requisito de la guía, alcance, dónde consta)
REQUISITOS = [
    ('REQ-01', 'Enunciado 1', 'P-01 a P-04 en ChatGPT (la guía pide la versión gratuita): título, variables, diagrama '
                              'conceptual y matriz de operacionalización', 'REQUERIDO', 'R-01 a R-04'),
    ('REQ-02', 'Enunciado 1', 'Documentar en el informe la matriz de operacionalización y la definición conceptual',
     'REQUERIDO', 'F29C_Operacionalizacion_Variables (DOCX, PDF y Markdown)'),
    ('REQ-03', 'Enunciado 2', 'Usar los mismos prompts en Gemini, DeepSeek y Copilot', NO_REQUERIDO, 'R-05 a R-16'),
    ('REQ-04', 'Enunciado 2', 'Cuadro comparativo de los 4 chatbots y diferencias cruciales', NO_REQUERIDO, '—'),
    ('REQ-05', 'Enunciado 3', 'Revisar el chat compartido por el docente, cuadro comparativo y dos preguntas',
     NO_REQUERIDO, 'T-01'),
    ('REQ-06', 'Enunciado 4', 'Prompts para los capítulos 1 y 2 y sus resultados', 'REQUERIDO', 'R-17 y R-18'),
    ('REQ-07', 'Enunciado 4', 'Documentar esos resultados: se integran como evidencia frente a los capítulos 1 y 2 del '
                              'repositorio, que siguen siendo la fuente canónica', 'REQUERIDO',
     'Registro, sección «Integración con los capítulos 1 y 2»'),
]

EJECUCIONES_REQUERIDAS = [e for e in EJECUCIONES + EJECUCIONES_E4 if e[1] == 'ChatGPT']
EJECUCIONES_NO_REQUERIDAS = [e for e in EJECUCIONES if e[1] != 'ChatGPT']
T01_REQUERIDO = False

# Capítulos 1 y 2: la fuente canónica es la documentación del repositorio; P-05 y P-06 son evidencia de la actividad.
CAPITULOS = [
    ('Capítulo 1 — Información general del proyecto', 'docs/final-report/01-informacion-general.md', 'R-17'),
    ('Capítulo 2 — Contexto organizacional y análisis del problema', 'docs/final-report/02-contexto-problema.md', 'R-18'),
]

ESTADO_ACTIVIDAD = (
    'La guía E1/L1 propone la actividad completa: 4 prompts en 4 chatbots, comparaciones y capítulos 1 y 2. Por el '
    'criterio docente informado por el equipo, el alcance efectivo de este entregable es la evidencia de ChatGPT (P-01 a '
    'P-06) y su integración con los capítulos 1 y 2. Gemini, DeepSeek, Copilot y el chat del docente quedan NO '
    'REQUERIDOS y no se presentan como ejecutados. La evidencia está en el registro de ejecuciones, y '
    '`validate.py --cierre-f29c` informa si está completa.')

NOTA_ELABORACION = ('La matriz y el diagrama de la F29C los elaboró el asistente de IA del equipo (Claude, en Claude Code) '
                    'a partir de la evidencia versionada del repositorio, siguiendo las reglas de la guía. No sustituyen '
                    'la actividad de la guía con ChatGPT, que se registra aparte.')
