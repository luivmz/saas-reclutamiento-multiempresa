"""Requerimientos no funcionales (Formato 07).

Catálogo académico RNF-01 a RNF-10: nombres y enunciados del F9 (tabla de RNF de las versiones 1.0 y 1.1).
Catálogo técnico: docs/final-report/04-requerimientos.md §4.3, con 11 RNF y otra numeración, citado aquí como
«cap. 4 RNF-nn». Candidatos RNF-A, RNF-B y RNF-C: docs/v1.1/scope-preliminary.md.

Estados de validación: VERIFICADO (pruebas o inspección ejecutadas y versionadas), EVIDENCIA PARCIAL (solo una
parte del criterio tiene evidencia), NO VERIFICADO (no hay evidencia del criterio) y PROPUESTO (candidato fuera de
la línea base). No se convierten pruebas exploratorias en SLA ni compatibilidad general en matriz formal.
"""

PRIORIZACION = 'priorización analítica del equipo'

# id, categoría (ISO/IEC 25010), nombre, descripción, métrica/criterio, prioridad, justificación, método, estado, evidencia
RNF = [
    ('RNF-01', 'Seguridad', 'Seguridad y control de acceso',
     'El sistema debe autenticar a todo usuario y autorizar cada operación en el servidor según su rol y su organización.',
     'Toda ruta del personal exige sesión y rol (middleware `role` y Policies). Contraseñas con hash bcrypt. Límite de 5 '
     'intentos de inicio de sesión por minuto. Las pruebas de autorización por rol pasan sin fallos.',
     'Alta', 'El sistema gestiona datos de postulantes y decisiones de contratación: un acceso indebido compromete la confidencialidad y la decisión.',
     'Pruebas automatizadas: AuthenticationTest, RoleMiddlewareTest, pruebas «solo X puede…», E2E-01 y E2E-12.',
     'VERIFICADO',
     'QA de la F25: PHPUnit 411 superadas y 0 fallidas; Cypress 85/85 (docs/v1.1/phase-25-final-qa.md).'),
    ('RNF-02', 'Seguridad', 'Multitenencia y aislamiento',
     'El sistema debe garantizar que ninguna organización acceda a los datos de otra.',
     'Toda entidad de negocio lleva `organization_id` y un scope global. Las Policies comparan rol y organización. Las '
     'pruebas cross-tenant pasan sin fallos.',
     'Alta', 'Es la condición del modelo SaaS multiempresa: una fuga entre organizaciones invalida el producto.',
     'Pruebas automatizadas: CrossTenantAccessTest, OrganizationScopeTest, pruebas cross-tenant por RF y E2E-11.',
     'VERIFICADO', 'F25: sin fugas entre organizaciones y 22 pruebas cross-tenant explícitas (phase-25-final-qa.md §14).'),
    ('RNF-03', 'Seguridad (responsabilidad)', 'Trazabilidad y auditoría',
     'El sistema debe registrar el usuario, la organización, la acción, la fecha y el objeto afectado de cada acción '
     'crítica, en un registro que no se pueda modificar.',
     'Cada acción crítica deja un registro. La tabla `audit_logs` rechaza UPDATE y DELETE mediante un trigger. Los '
     'historiales de estado registran quién, cuándo y de qué estado a cuál.',
     'Alta', 'Da sustento a la decisión humana y permite reconstruir el proceso (P2, P5).',
     'Pruebas automatizadas: AuditTrailTest, AuditLogViewTest, AuditLoggerTest y E2E-11; inspección del trigger `audit_logs_append_only`.',
     'VERIFICADO', 'DEF-07 y DEF-08 corregidos y cubiertos por pruebas (docs/defects.md).'),
    ('RNF-04', 'Seguridad (confidencialidad)', 'Privacidad',
     'El sistema debe minimizar los datos del postulante y restringir su acceso según el rol y el vínculo con la vacante.',
     'No se almacenan DNI, fecha de nacimiento ni atributos sensibles no requeridos. El CV se guarda en disco privado '
     'con nombre UUID y solo lo descargan los usuarios autorizados por la Policy. Las notificaciones no incluyen datos '
     'de otros candidatos.',
     'Alta', 'Protege a los postulantes y limita la exposición de datos personales.',
     'Pruebas automatizadas: CandidateProfileTest y ProcessResultNotificationTest; inspección de la Policy CandidateDocumentPolicy y del modelo de datos (A-15).',
     'VERIFICADO', 'Solo datos ficticios en el repositorio; barrido de secretos y PII en la F25 y la F26.'),
    ('RNF-05', 'Usabilidad', 'Usabilidad',
     'El sistema debe ofrecer formularios, mensajes y navegación comprensibles y consistentes.',
     'Interfaz en español; errores por campo; estados vacíos; navegación por rol; diseño adaptable de 320 a 1440 px; '
     'contraste AA en modo claro y oscuro; foco visible y enlace de salto.',
     'Media', 'Los usuarios del Colegio y los postulantes no son técnicos. Los errores de uso afectan a la calidad del registro.',
     'Recorrido manual (docs/manual-smoke-test.md), QA visual y de accesibilidad de la F21 (E2E-16, E2E-19, contraste automatizado) y QA de la F25.',
     'EVIDENCIA PARCIAL',
     'No hay pruebas de usabilidad con usuarios reales, y la prueba con un lector de pantalla real está pendiente. La accesibilidad WCAG 2.1 AA como requisito es el candidato RNF-A (propuesta).'),
    ('RNF-06', 'Eficiencia de desempeño', 'Rendimiento',
     'El sistema debe permitir medir sus operaciones críticas contra una línea base documentada.',
     '**Criterio propuesto:** fijar un entorno de referencia, medir una línea base de las operaciones críticas '
     '(listado de postulaciones, comparación, registro de decisión) y aprobar umbrales antes de cualquier aceptación '
     'productiva. **No hay umbral aprobado.**',
     'Media', 'Hace falta una base objetiva antes de fijar un SLA. El volumen académico es bajo.',
     'Medición en un entorno acordado (Navigation Timing o pruebas de carga), a definir.',
     'NO VERIFICADO',
     'Solo hay medición exploratoria de la F25 en un equipo potente: no es un benchmark ni un SLA. No se ejecutaron pruebas de carga. El presupuesto de rendimiento es el candidato RNF-B (propuesta).'),
    ('RNF-07', 'Fiabilidad', 'Disponibilidad y recuperabilidad',
     'El sistema debe permitir detectar fallas y recuperarse de ellas sin corromper los datos.',
     '**Criterio propuesto:** procedimiento de respaldo y restauración de la base probado, y objetivos de disponibilidad '
     'aprobados. **No definidos.**',
     'Media', 'Evita perder expedientes y decisiones. El entorno entregado es de desarrollo y demostración (A-36).',
     'Prueba de respaldo y restauración y monitoreo del servicio, a definir.',
     'NO VERIFICADO',
     'Hay controles de integridad (transacciones, notificaciones tras el commit, restricciones de la base) y healthchecks de Docker Compose, pero no pruebas de respaldo o restauración ni objetivos de disponibilidad.'),
    ('RNF-08', 'Compatibilidad', 'Compatibilidad',
     'El sistema debe operar en los navegadores modernos definidos para el entorno académico.',
     '**Criterio propuesto:** lista de navegadores y versiones aprobada, y pruebas en cada uno. **No hay matriz formal.**',
     'Baja', 'El uso académico se concentra en navegadores de escritorio y móviles actuales.',
     'Suite E2E en cada navegador de la lista, a definir.',
     'EVIDENCIA PARCIAL',
     'Cypress se ejecuta en Electron (motor Chromium), con anchos de 320 a 1440 px. Firefox y Safari no se probaron de forma sistemática.'),
    ('RNF-09', 'Mantenibilidad', 'Mantenibilidad',
     'El sistema debe mantener una arquitectura modular con separación de responsabilidades.',
     'Monolito modular por dominio: controlador delgado → Form Request → Policy → servicio → modelo, con máquinas de '
     'estado en enums. Suites automatizadas de regresión en CI: build, tsc y PHPUnit.',
     'Media', 'Facilita la evolución (v1.1) sin romper la línea base.',
     'Inspección de la estructura de `app/`; suites PHPUnit, Vitest y tsc; CI de GitHub.',
     'EVIDENCIA PARCIAL',
     'La estructura y las suites están verificadas (F25: 411 PHPUnit, 42 Vitest, tsc sin errores). No se midieron métricas de mantenibilidad (complejidad, cobertura) y hay deuda de formato aceptada (Pint, vp check).'),
    ('RNF-10', 'Seguridad (integridad)', 'Integridad de datos',
     'El sistema debe validar estados, rangos, ponderaciones y resultados antes de guardarlos.',
     'Form Requests en cada operación; máquinas de estado que rechazan transiciones inválidas; validadores de '
     'ponderaciones y puntajes; restricciones CHECK, UNIQUE y FK; un solo seleccionado por vacante; los IDs no '
     'numéricos devuelven 404.',
     'Alta', 'La integridad es la base del ranking y de la decisión (P3).',
     'Pruebas automatizadas: WeightingValidatorTest, ScoreSheetValidatorTest, ApplicationStatusTest, SelectionRegistrationTest y NumericRouteParametersTest.',
     'VERIFICADO', 'F25-M01 corregido (500 → 404) con prueba de regresión.'),
]

# Equivalencia académico ↔ técnico (cap. 4 §4.3). No se fuerza 1:1.
EQUIVALENCIA = [
    ('RNF-01 Seguridad y control de acceso', 'cap. 4 RNF-01 (autenticación) + RNF-02 (autorización)', '1 → 2', 'VERIFICADO'),
    ('RNF-02 Multitenencia y aislamiento', 'cap. 4 RNF-03 (aislamiento multiempresa)', '1 → 1', 'VERIFICADO'),
    ('RNF-03 Trazabilidad y auditoría', 'cap. 4 RNF-05 (responsabilidad) + RNF-10 (trazabilidad funcional)', '1 → 2', 'VERIFICADO'),
    ('RNF-04 Privacidad', 'cap. 4 RNF-06 (privacidad)', '1 → 1', 'VERIFICADO'),
    ('RNF-05 Usabilidad', 'cap. 4 RNF-07 (usabilidad); candidato RNF-A (accesibilidad, propuesta)', '1 → 1 (+ candidato)', 'EVIDENCIA PARCIAL'),
    ('RNF-06 Rendimiento', 'Sin equivalente técnico (el cap. 4 declara que no hay SLA ni pruebas de carga); candidato RNF-B (propuesta)', '1 → 0', 'NO VERIFICADO'),
    ('RNF-07 Disponibilidad y recuperabilidad', 'Sin equivalente técnico', '1 → 0', 'NO VERIFICADO'),
    ('RNF-08 Compatibilidad', 'Sin equivalente técnico (el cap. 4 RNF-07 cubre el diseño adaptable, no los navegadores)', '1 → 0 (parcial)', 'EVIDENCIA PARCIAL'),
    ('RNF-09 Mantenibilidad', 'cap. 4 RNF-08 (mantenibilidad)', '1 → 1', 'EVIDENCIA PARCIAL'),
    ('RNF-10 Integridad de datos', 'cap. 4 RNF-04 (integridad)', '1 → 1', 'VERIFICADO'),
]

TECNICOS_SIN_EQUIVALENTE = [
    ('cap. 4 RNF-09', 'Portabilidad: ejecución completa con Docker e instalación desde cero documentada',
     'VERIFICADO (docs/docker.md; validación en un clon limpio, cap. 10)'),
    ('cap. 4 RNF-11', 'Adecuación (localización): fechas y horas en America/Lima',
     'VERIFICADO (AppTimezoneTest, DEF-09)'),
]

CANDIDATOS = [
    ('RNF-A', 'Accesibilidad WCAG 2.1 AA verificada en las pantallas de RF-01 a RF-27', 'PROPUESTO',
     'Hay evidencia parcial de la F21 y la F25; falta un lector de pantalla real'),
    ('RNF-B', 'Presupuesto de rendimiento del frontend con línea base medida', 'PROPUESTO', 'Sin línea base aprobada'),
    ('RNF-C', 'Experiencia 3D progresiva en pantallas públicas', 'PROPUESTO',
     'Implementada en la F20 (portada, CSS 3D), pero **no promovida**: implementar no promueve un requisito (decisión 11)'),
    ('RNF-D', 'Observabilidad del proceso: métricas operativas y registro estructurado', 'PROPUESTO',
     'Candidato de `docs/v1.1/scope-preliminary.md`, refinado como «observabilidad operacional» en '
     '`docs/v1.1/ml/requirements-and-traceability-plan.md`. Añadido al F7 en la F27D (H-10); **no** forma parte de los 10 '
     'RNF académicos'),
]

CLASIFICACION = [
    ('Rendimiento', 'RNF-06'),
    ('Seguridad', 'RNF-01, RNF-02, RNF-03, RNF-04, RNF-10'),
    ('Usabilidad', 'RNF-05'),
    ('Disponibilidad', 'RNF-07'),
    ('Compatibilidad', 'RNF-08'),
    ('Mantenibilidad', 'RNF-09'),
]

# RNF relevantes por RF (para la trazabilidad; los RNF son transversales)
RNF_POR_RF = {
    'default': ['RNF-01', 'RNF-02', 'RNF-03', 'RNF-10'],
    'RF-08': ['RNF-01', 'RNF-04'], 'RF-09': ['RNF-04', 'RNF-05'], 'RF-10': ['RNF-04', 'RNF-10'],
    'RF-11': ['RNF-04'], 'RF-15': ['RNF-04'], 'RF-17': ['RNF-04'], 'RF-26': ['RNF-04'], 'RF-04': ['RNF-02'],
    'RF-20': ['RNF-10'], 'RF-21': ['RNF-10', 'RNF-06'], 'RF-22': ['RNF-02', 'RNF-05', 'RNF-06'],
    'RF-23': ['RNF-01', 'RNF-02', 'RNF-03'], 'RF-27': ['RNF-03', 'RNF-02'], 'RF-12': ['RNF-02', 'RNF-04', 'RNF-06'],
}
