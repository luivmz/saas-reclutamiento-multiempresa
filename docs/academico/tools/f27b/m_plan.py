"""F29D — Plan de Pruebas de Software: contenido.

Estructura: la de la plantilla del curso (docs/academico/00-fuentes-oficiales/plan-pruebas/
Plantilla_de_Plan_de_Pruebas_de_Software.pdf), que prevalece sobre la referencia PMO (misma estructura) y sobre el
ejemplo externo (no normativo). Los textos guía en rojo de la plantilla no se copian; cada apartado se responde con
datos del repositorio. No hay aprobación ni firma: el plan no se presenta como aprobado.
"""
import m_common as C
import m_rnf as N

FECHA = '30/09/2026'
VERSION = '1.0'
TITULO = 'Plan de pruebas de software'
BASE_COMMIT = 'bc44303'   # develop al iniciar la F29D (F29C integrada)

# Títulos de la plantilla del curso, en orden (nivel, título). El validador exige esta lista exacta.
SECCIONES = [
    (1, 'Historial de versiones'), (1, 'Información del proyecto'), (1, 'Aprobaciones'), (1, 'Resumen ejecutivo'),
    (1, 'Alcance de las pruebas'), (2, 'Elementos de pruebas'), (2, 'Nuevas funcionalidades a probar'),
    (2, 'Pruebas de regresión'), (2, 'Funcionalidades a no probar'), (2, 'Enfoque de pruebas (estrategia)'),
    (1, 'Criterios de aceptación o rechazo'), (2, 'Criterios de aceptación o rechazo'), (2, 'Criterios de suspensión'),
    (2, 'Criterios de reanudación'), (1, 'Entregables'), (1, 'Recursos'), (2, 'Requerimientos de entornos – Hardware'),
    (2, 'Requerimientos de entornos – Software'), (2, 'Herramientas de pruebas requeridas'), (2, 'Personal'),
    (2, 'Entrenamiento'), (1, 'Planificación y organización'), (2, 'Procedimientos para las pruebas'),
    (2, 'Matriz de responsabilidades'), (2, 'Cronograma'), (2, 'Premisas'), (2, 'Dependencias y Riesgos'),
    (1, 'Referencias'), (1, 'Glosario'),
]

SIN_APROBACION = 'Pendiente — sin firma'


def contenido():
    s = dict((t, []) for _, t in SECCIONES)   # títulos repetidos (criterios) se resuelven por orden abajo
    B = []

    def h(level, text):
        B.append(('h1' if level == 1 else 'h2', text))

    h(1, 'Historial de versiones')
    B.append(('table', ['Fecha', 'Versión', 'Autor', 'Organización', 'Descripción'], [
        (FECHA, VERSION, 'Equipo del proyecto (redacción asistida por Claude)', 'Universidad Continental — Pruebas y '
         'Calidad de Software, NRC 28607', 'Primera versión del plan maestro de pruebas (fase F29D), sobre la plantilla '
         'del curso, para la versión v1.1 del sistema.'),
    ], [0.12, 0.10, 0.26, 0.23, 0.29]))

    h(1, 'Información del proyecto')
    B.append(('table', ['Campo', 'Valor'], [
        ('Empresa / Organización', 'Universidad Continental — Facultad de Ingeniería, Ingeniería de Sistemas e '
                                   'Informática. Proyecto académico del curso Pruebas y Calidad de Software (NRC 28607)'),
        ('Proyecto', C.PROYECTO),
        ('Fecha de preparación', FECHA),
        ('Cliente', 'Colegio Andino de Huancayo, como caso de estudio académico. No hay relación contractual ni '
                    'validación institucional del proceso ni del sistema'),
        ('Patrocinador principal', 'No aplica: proyecto académico sin financiamiento'),
        ('Gerente / Líder de proyecto', 'Sin asignación formal registrada en el repositorio: responsabilidad compartida '
                                        'del equipo (' + C.EQUIPO + ')'),
        ('Gerente / Líder de pruebas de software', 'Sin asignación formal: responsabilidad compartida del equipo. La '
                                                   'ejecución y el registro de la F29F los hizo el asistente de IA del '
                                                   'equipo bajo su dirección'),
        ('Docente', C.DOCENTE),
    ], [0.32, 0.68]))

    h(1, 'Aprobaciones')
    B.append(('p', 'El plan **no está aprobado ni firmado**. La tabla indica quién debe aprobarlo; no se simula ninguna '
                   'firma ni aprobación institucional.'))
    B.append(('table', ['Nombre y apellido', 'Cargo', 'Departamento u organización', 'Fecha', 'Firma'], [
        (C.DOCENTE, 'Docente del curso', 'Universidad Continental', 'Pendiente', SIN_APROBACION),
        ('Integrantes del equipo', 'Autores del plan', 'Universidad Continental (NRC 28607)', 'Pendiente', SIN_APROBACION),
        ('RR. HH. / Administración del Colegio Andino', 'Usuario del caso de estudio', 'Colegio Andino de Huancayo',
         'No aplica', 'No aplica: no hay validación institucional'),
    ], [0.24, 0.17, 0.25, 0.12, 0.22]))

    h(1, 'Resumen ejecutivo')
    B.append(('p', 'Este es el **plan maestro** de pruebas de la plataforma SaaS multiempresa de reclutamiento, '
                   'evaluación y selección de personal, en su versión v1.1 (rama `develop`, commit ' + BASE_COMMIT + '). '
                   'Cubre la línea base funcional RF-01 a RF-27, los casos de uso CU-01 a CU-20, los diez RNF académicos '
                   'del Formato 07 y el componente experimental RF-29.'))
    B.append(('ul', [
        '**Propósito:** definir qué se prueba, cómo, con qué criterios y con qué evidencia se da por aceptada la '
        'versión, y dejar trazado cada requisito hasta sus casos de prueba (F29E) y su ejecución (F29F).',
        '**Relación con el proyecto:** el plan acompaña la entrega académica final. Las pruebas automatizadas existen '
        'desde la Fase 3 (TDD) y el plan las formaliza; no describe un esfuerzo nuevo ni reemplaza la evidencia '
        'histórica.',
        '**Restricciones:** equipo de tres integrantes, un solo equipo de cómputo con Docker, sin entorno de '
        'producción, sin datos reales (solo ficticios) y sin validación institucional del Colegio.',
        '**Límites declarados:** no se mide cobertura de código, no hay pruebas de carga ni de disponibilidad (RNF-06 y '
        'RNF-07 no verificados) y la aceptación por el usuario institucional no se realizó.',
    ]))

    h(1, 'Alcance de las pruebas')
    h(2, 'Elementos de pruebas')
    B.append(('p', 'Áreas funcionales y componentes que se prueban (componentes del Formato 11, CMP-xx):'))
    B.append(('table', ['Área funcional', 'Componentes', 'RF'], [
        ('Requerimientos de personal', 'CMP-04', 'RF-01 a RF-04'),
        ('Vacantes y publicación', 'CMP-05', 'RF-05 a RF-07'),
        ('Postulantes y postulaciones', 'CMP-06, CMP-07', 'RF-08 a RF-15'),
        ('Evaluaciones y entrevistas', 'CMP-08', 'RF-16 a RF-19'),
        ('Ranking y comparación (apoyo)', 'CMP-09', 'RF-20 a RF-22'),
        ('Decisión humana, selección y cierre', 'CMP-10, CMP-11', 'RF-23 a RF-26'),
        ('Auditoría', 'CMP-13', 'RF-27'),
        ('Autenticación, roles y multiempresa', 'CMP-02, CMP-03', 'Transversal (RNF-01, RNF-02)'),
        ('Notificaciones y cola', 'CMP-12, CMP-16', 'RF-04, RF-11, RF-15, RF-17, RF-26'),
        ('Interfaz web', 'CMP-01', 'Todos (E2E y componentes)'),
        ('Servicio de riesgo operacional', 'CMP-17', 'RF-29 (EXPERIMENTAL / PROPUESTO)'),
    ], [0.40, 0.25, 0.35]))

    h(2, 'Nuevas funcionalidades a probar')
    B.append(('p', 'Funcionalidades de la versión v1.1 respecto de la v1.0 académica (tag `v1.0.0-academic`), vistas '
                   'desde el usuario:'))
    B.append(('ul', [
        '**Plazo objetivo de la vacante** (`target_completion_at`): RR. HH. registra la fecha objetivo del proceso '
        '(Fase 16).',
        '**Tarjeta de riesgo operacional** en la ficha de la vacante (RF-29, EXPERIMENTAL): muestra el riesgo de '
        'demora del proceso o un panel descriptivo si el servicio no está disponible. No evalúa personas ni cambia el '
        'ranking.',
        '**Interfaz rediseñada** con movimiento reducido, tablas accesibles en móvil y portada con experiencia CSS 3D '
        '(Fases 18 a 21).',
    ]))

    h(2, 'Pruebas de regresión')
    B.append(('p', 'Toda la línea base RF-01 a RF-27 entra en regresión, porque las fases de v1.1 tocaron la interfaz, '
                   'la ficha de vacante y la configuración del entorno:'))
    B.append(('ul', [
        'la suite completa de PHPUnit (unitarias y de integración, con autorización por rol y aislamiento entre '
        'organizaciones);',
        'la suite E2E de Cypress, desde el inicio de sesión hasta el flujo completo de reclutamiento;',
        'la integración continua en GitHub Actions, que en cada push a `develop` y `main` ejecuta build, TypeScript y '
        'PHPUnit;',
        'los defectos corregidos DEF-01 a DEF-13, cada uno con su prueba de regresión (`docs/defects.md`).',
    ]))

    h(2, 'Funcionalidades a no probar')
    B.append(('table', ['Funcionalidad', 'Razón', 'Riesgo asumido'], [
        ('RF-28 (candidato)', 'No está implementado', 'Ninguno sobre el software; se declara NO IMPLEMENTADO'),
        ('Rendimiento y carga (RNF-06)', 'No hay herramienta de carga ni SLA definido', 'Comportamiento desconocido con '
         'volumen real; RNF-06 queda NO VERIFICADO'),
        ('Disponibilidad y recuperación (RNF-07)', 'No hay entorno de producción ni respaldos probados',
         'RNF-07 queda NO VERIFICADO'),
        ('Envío real de correo y SMS', 'El correo usa el driver `log` (fuera de alcance)', 'Entregabilidad real no probada'),
        ('Despliegue en la nube, SuperAdmin y facturación', 'Fuera del alcance del proyecto', 'Ninguno para la entrega académica'),
        ('Aceptación por el usuario institucional', 'No hay validación con RR. HH. / Administración del Colegio',
         'El AS-IS sigue preliminar y el TO-BE, propuesto'),
        ('Pruebas de penetración', 'Fuera del alcance académico', 'Solo seguridad básica automatizada'),
        ('Validez institucional del modelo RF-29', 'Solo hay datos sintéticos', 'El modelo sigue EXPERIMENTAL; no se '
         'autoriza en producción'),
    ], [0.30, 0.35, 0.35]))

    h(2, 'Enfoque de pruebas (estrategia)')
    B.append(('p', 'Estrategia en niveles, con prioridad de la automatización y registro de la evidencia real de cada '
                   'ejecución. Los datos son siempre ficticios: fábricas de PHPUnit, `DemoSeeder` para Cypress y el '
                   'dataset sintético del servicio ML.'))
    B.append(('table', ['Nivel / tipo', 'Herramienta', 'Alcance', 'Automatización'], [
        ('Unitarias', 'PHPUnit (`tests/Unit`, 6 archivos)', 'Estados, validadores de puntajes y ponderaciones, '
         'servicio de ranking', 'Automatizada'),
        ('Integración / funcionales', 'PHPUnit (`tests/Feature`, 42 archivos) sobre PostgreSQL 17 real', 'RF-01 a '
         'RF-27, autorización, notificaciones y auditoría', 'Automatizada'),
        ('Seguridad básica', 'PHPUnit (autenticación, roles, soporte E2E) y Cypress E2E-12', 'Acceso por rol, límites '
         'de intentos, reglas negativas', 'Automatizada'),
        ('Multitenencia', 'PHPUnit (`CrossTenantAccessTest`, `OrganizationScopeTest`) y Cypress E2E-11', 'Ninguna '
         'organización accede a datos de otra', 'Automatizada'),
        ('UI / E2E', 'Cypress 15.3.0 (20 specs) en el entorno aislado `app-e2e`', 'Flujos por rol y flujo completo',
         'Automatizada'),
        ('Componentes frontend', 'Vitest (`vp test`, 6 archivos)', 'Componentes de interfaz y accesibilidad',
         'Automatizada'),
        ('Estático y build', '`tsc --noEmit` y `npm run build`', 'Tipos y compilación del frontend', 'Automatizada'),
        ('Regresión continua', 'GitHub Actions (`tests.yml`)', 'Build, TypeScript y PHPUnit en cada push', 'Automatizada'),
        ('ML experimental', 'pytest (18 archivos) y PHPUnit `tests/Feature/Ml`', 'Dataset, entrenamiento, contrato '
         'congelado, API e integración RF-29', 'Automatizada'),
        ('Aceptación', 'Recorrido manual por rol (Fase 8) y flujo E2E-13', 'Flujo de punta a punta', 'Parcial: sin '
         'aceptación institucional'),
        ('No funcionales', 'Cypress E2E-16 a E2E-19 y medición puntual de la F25', 'Accesibilidad, responsive y '
         'tiempos puntuales', 'Parcial: sin carga ni disponibilidad'),
    ], [0.18, 0.30, 0.34, 0.18]))
    B.append(('p', 'Configuraciones: equipo Windows 11 con Docker Desktop, navegador Electron 136 headless, viewport '
                   '1280×800 (y móvil en E2E-16). Nivel de regresión: completo en cada ejecución de cierre.'))

    h(1, 'Criterios de aceptación o rechazo')
    h(2, 'Criterios de aceptación o rechazo')
    B.append(('p', 'El plan se da por completado y la versión se acepta **solo si se cumplen todos** estos criterios, '
                   'medidos en la ejecución de la F29F:'))
    B.append(('table', ['ID', 'Criterio de aceptación'], [
        ('CA-01', 'PHPUnit: 0 pruebas fallidas. Las únicas omitidas son las 8 de funciones del starter kit '
                  'desactivadas.'),
        ('CA-02', 'Cypress: 20 specs y 0 tests fallidos, sin reintentos.'),
        ('CA-03', 'Vitest y pytest: 0 pruebas fallidas.'),
        ('CA-04', 'TypeScript sin errores y build del frontend sin errores.'),
        ('CA-05', 'Integración continua en verde en `develop`.'),
        ('CA-06', 'Cada RF-01 a RF-27 tiene al menos un caso de prueba automatizado ejecutado y aprobado (F29E y F29F).'),
        ('CA-07', 'Ningún defecto de severidad Alta abierto (F29G).'),
    ], [0.12, 0.88]))
    B.append(('p', '**Rechazo:** cualquier prueba fallida sin clasificar, una regresión real, un RF sin caso de prueba '
                   'aprobado o un defecto de severidad Alta abierto. La cobertura de código **no** es criterio: no se '
                   'mide con herramienta.'))
    h(2, 'Criterios de suspensión')
    B.append(('ul', [
        'El entorno Docker no está healthy (servicios `app`, `postgres`, `redis`, `app-e2e` o `queue-e2e`).',
        'La base de datos de pruebas no es la aislada (`reclutamiento_testing` para PHPUnit, `reclutamiento_e2e` para '
        'Cypress): se detiene la ejecución para no afectar los datos de demostración (DEF-13).',
        'Un defecto bloquea un flujo principal e impide ejecutar los casos que dependen de él.',
        'La integración continua falla por una causa externa (servicio de GitHub o dependencia de red).',
    ]))
    h(2, 'Criterios de reanudación')
    B.append(('ul', [
        'El entorno vuelve a estar healthy y se repite la suite completa afectada, no solo el caso que falló.',
        'La causa del fallo está clasificada (regresión real, flaky, ambiente, dependencia externa o documental). Si '
        'es una regresión real, se corrige con autorización del equipo y con su prueba de regresión.',
        'Toda ejecución repetida se registra junto a la anterior; no se sustituye ni se oculta el primer resultado.',
    ]))

    h(1, 'Entregables')
    B.append(('table', ['Entregable', 'Ubicación'], [
        ('Plan de pruebas (este documento)', 'docs/academico/plan-pruebas/'),
        ('Casos de prueba y matriz de trazabilidad RF → CU → CP → prueba → evidencia (F29E)', 'docs/academico/casos-prueba/'),
        ('Ejecución QA: registros de cada herramienta, resumen y matriz CP → resultado (F29F)', 'docs/academico/qa-final/'),
        ('Registro de defectos y métricas de calidad (F29G)', 'docs/academico/metricas-calidad/'),
        ('Evidencia TDD (ciclos RED → GREEN)', 'docs/tdd-evidence.md'),
        ('Registro histórico de defectos DEF-01 a DEF-13', 'docs/defects.md'),
        ('Reportes de herramientas: salida de PHPUnit, Cypress, Vitest, pytest, TypeScript, build y CI', 'docs/academico/qa-final/evidencias/'),
    ], [0.62, 0.38]))

    h(1, 'Recursos')
    h(2, 'Requerimientos de entornos – Hardware')
    B.append(('table', ['Recurso', 'Especificación (verificada el ' + FECHA + ')'], [
        ('Equipo de pruebas', 'AMD Ryzen 9 5900X (12 núcleos), 31,9 GB de RAM, Windows 11 Pro'),
        ('Máquina virtual de Docker Desktop', '24 CPU y 16,7 GB de memoria asignados'),
        ('Integración continua', 'Ejecutor `ubuntu-latest` de GitHub Actions'),
        ('Red', 'Acceso a internet para GitHub, imágenes Docker y dependencias; servicios locales publicados solo en '
                '127.0.0.1 salvo `app`'),
    ], [0.32, 0.68]))
    h(2, 'Requerimientos de entornos – Software')
    B.append(('table', ['Software', 'Versión'], [
        ('Docker / Docker Compose', '29.7.2 / v5.5.1'),
        ('Contenedor `app`', 'PHP 8.4.25, Node 22.23.2, Laravel 13'),
        ('Base de datos y caché', 'PostgreSQL 17.11, Redis 7.4.11'),
        ('Frontend', 'React 19, TypeScript, Inertia 3, Tailwind 4, Vite (`vp`)'),
        ('Servicio ML', 'Python 3.12.5 en `ml-service/.venv` (fuera de Docker Compose)'),
        ('Cypress', 'Imagen `cypress/included:15.3.0`, Electron 136'),
        ('Bases de prueba', '`reclutamiento_testing` (PHPUnit) y `reclutamiento_e2e` (Cypress); nunca la de demostración'),
    ], [0.32, 0.68]))
    h(2, 'Herramientas de pruebas requeridas')
    B.append(('ul', [
        '**PHPUnit** (vía `php artisan test`): unitarias e integración.',
        '**Cypress 15.3.0**: E2E en navegador, desde su imagen oficial.',
        '**Vitest** (vía `vp test`): componentes de React.',
        '**pytest**: servicio ML experimental.',
        '**TypeScript** (`tsc --noEmit`) y **Vite** (`npm run build`).',
        '**GitHub Actions**: integración continua (`.github/workflows/tests.yml`).',
        '**Git**: control de versiones y trazabilidad de cada ejecución al commit probado.',
        'Técnica: **TDD** (RED → GREEN → REFACTOR) para cada regla de negocio.',
    ]))
    h(2, 'Personal')
    B.append(('table', ['Rol', 'Quién', 'Función en las pruebas'], [
        ('Equipo del proyecto (3)', C.EQUIPO, 'Decide el alcance, revisa resultados, aprueba correcciones y es '
         'responsable de la entrega'),
        ('Implementador asistido por IA', 'Claude (Claude Code)', 'Escribe pruebas y documentos, ejecuta las suites y '
         'registra la evidencia, bajo la dirección del equipo'),
        ('Auditor asistido por IA', 'Codex', 'Revisa cada fase de forma independiente antes de integrarla'),
        ('Docente', C.DOCENTE, 'Revisión académica del plan y de sus resultados'),
    ], [0.24, 0.30, 0.46]))
    h(2, 'Entrenamiento')
    B.append(('p', 'Necesidades de entrenamiento para operar el plan (no se afirma que se hayan cubierto con cursos '
                   'formales):'))
    B.append(('ul', [
        'Pruebas de Laravel con PHPUnit sobre PostgreSQL y fábricas de datos.',
        'Cypress con entornos aislados y reset de datos.',
        'Docker Compose: levantar, verificar salud y aislar las bases de prueba.',
        'pytest y el contrato congelado del experimento ML.',
        'Lectura de la matriz de trazabilidad y registro de defectos.',
    ]))

    h(1, 'Planificación y organización')
    h(2, 'Procedimientos para las pruebas')
    B.append(('ul', [
        '**Desarrollo:** TDD. Cada regla nueva empieza con una prueba que falla (RED observado) y termina en verde; se '
        'registra en `docs/tdd-evidence.md`.',
        '**Ejecución de cierre:** con el árbol de trabajo limpio, se ejecutan en orden: configuración de Compose, '
        'PHPUnit, TypeScript, build, Vitest, pytest y Cypress. Se guarda la salida completa, el comando, la hora y el '
        'código de salida.',
        '**Comandos reales:** `docker compose exec app php artisan test` · `docker compose exec app npx tsc --noEmit` · '
        '`docker compose exec app npm run build` · `docker compose exec app npx vp test --run` · '
        '`ml-service/.venv/Scripts/python.exe -m pytest` · `npm run cy:run`.',
        '**Fallos:** se clasifican (regresión real, flaky, ambiente, dependencia externa, documental o no aplicable). '
        'Nunca se ocultan, y el runtime no se corrige sin autorización del equipo.',
        '**Defectos:** se registran como DEF-NN con síntoma, causa, corrección y prueba de regresión.',
        '**Integración:** rama `feature/*` desde `develop`, auditoría y merge `--no-ff` con la CI en verde.',
    ]))
    h(2, 'Matriz de responsabilidades')
    B.append(('p', 'Matriz RACI (R: responsable, A: aprueba, C: consultado, I: informado).'))
    B.append(('table', ['Actividad', 'Equipo del proyecto', 'Claude (implementador)', 'Codex (auditor)', 'Docente'], [
        ('Definir alcance y criterios', 'A', 'R', 'C', 'I'),
        ('Escribir pruebas automatizadas (TDD)', 'A', 'R', 'C', 'I'),
        ('Ejecutar suites y registrar evidencia', 'A', 'R', 'I', 'I'),
        ('Clasificar fallos y registrar defectos', 'A', 'R', 'C', 'I'),
        ('Corregir regresiones del runtime', 'A', 'R (con autorización)', 'C', 'I'),
        ('Auditar la fase', 'I', 'C', 'R', 'I'),
        ('Integrar y publicar', 'A', 'R', 'C', 'I'),
        ('Revisión académica', 'R', 'I', 'I', 'A'),
    ], [0.32, 0.17, 0.19, 0.16, 0.16]))
    h(2, 'Cronograma')
    B.append(('p', 'Hitos de pruebas con sus fechas reales (fecha de integración en `develop`). Las actividades aún no '
                   'realizadas no tienen fecha.'))
    B.append(('table', ['Hito', 'Actividad', 'Fecha', 'Depende de'], [
        ('H1', 'Base multiempresa, roles y RF-01 a RF-27 con TDD (Fases 1 a 7)', '13/09/2026', '—'),
        ('H2', 'Validación manual en navegador (Fase 8)', '13/09/2026', 'H1'),
        ('H3', 'Suite E2E con Cypress (Fase 9) y portabilidad Docker (Fase 10)', '13/09/2026', 'H2'),
        ('H4', 'Servicio ML: pruebas y validación (Fases 15 a 17)', '21/09/2026', 'H3'),
        ('H5', 'QA visual y accesibilidad (Fase 21)', '23/09/2026', 'H4'),
        ('H6', 'QA global de release v1.1 (Fase 25)', '25/09/2026', 'H5'),
        ('H7', 'Plan de pruebas (F29D) y casos de prueba (F29E)', FECHA, 'H6'),
        ('H8', 'Ejecución QA final (F29F), defectos y métricas (F29G)', FECHA, 'H7'),
        ('H9', 'Auditoría final de F29D a F29H', 'Pendiente', 'H8'),
    ], [0.08, 0.58, 0.16, 0.18]))
    h(2, 'Premisas')
    B.append(('ul', [
        'Los datos son ficticios y no se usa información personal real.',
        'El entorno Docker del equipo representa el entorno de ejecución; no existe un entorno de producción.',
        'Las pruebas automatizadas existentes son válidas como casos de prueba porque su trazabilidad a los RF está '
        'verificada.',
        'La decisión final de selección es humana (RF-23): ninguna prueba espera que el sistema seleccione, descarte o '
        'contrate.',
        'El tiempo disponible es el del calendario académico, sin personal de QA dedicado.',
    ]))
    h(2, 'Dependencias y Riesgos')
    B.append(('p', 'Dependencias: imágenes Docker publicadas (`postgres`, `redis`, `cypress/included`), dependencias '
                   'de Composer y npm fijadas por sus archivos lock, GitHub Actions y el entorno virtual del servicio ML.'))
    B.append(('table', ['ID', 'Riesgo', 'Probabilidad', 'Impacto', 'Mitigación', 'Contingencia'], [
        ('R-01', 'El reset E2E borra datos de demostración', 'Baja', 'Alto', 'Entorno E2E aislado y rechazo del reset '
         'fuera de la base E2E (DEF-13)', 'Restaurar con `migrate:fresh --seed` en el entorno de demostración'),
        ('R-02', 'Pruebas inestables por fechas y zona horaria', 'Media', 'Medio', 'Fechas en `APP_TIMEZONE` (DEF-12) y '
         'sin reintentos', 'Clasificar como flaky y repetir la suite completa'),
        ('R-03', 'Falla externa de la CI o de la red', 'Media', 'Medio', 'Misma suite ejecutable en local con Docker',
         'Re-ejecutar la CI y registrar la ejecución local'),
        ('R-04', 'Disponibilidad limitada del equipo', 'Media', 'Medio', 'Automatización y ejecución con un solo '
         'comando por herramienta', 'Priorizar criterios CA-01 a CA-06'),
        ('R-05', 'Rendimiento y disponibilidad sin verificar', 'Alta', 'Medio', 'Se declaran NO VERIFICADOS (RNF-06 y '
         'RNF-07)', 'Recomendación de pruebas de carga como trabajo futuro'),
        ('R-06', 'Premisa del AS-IS no validada por el Colegio', 'Alta', 'Medio', 'Se declara AS-IS PRELIMINAR',
         'Validación institucional como trabajo futuro'),
        ('R-07', 'Interpretar RF-29 como evaluación de personas', 'Baja', 'Alto', 'Pruebas que comprueban que la '
         'salida no menciona candidatos ni cambia el ranking', 'Desactivar el servicio: la aplicación funciona igual'),
    ], [0.07, 0.19, 0.13, 0.10, 0.27, 0.24], 14))

    h(1, 'Referencias')
    B.append(('ul', [
        'Plantilla de Plan de Pruebas de Software del curso (docs/academico/00-fuentes-oficiales/plan-pruebas/).',
        'Referencia externa PMO Informática y ejemplo externo de plan de pruebas (no normativos).',
        'Especificación de requerimientos: Formatos 06 (RF) y 07 (RNF); casos de uso: Formato 08.',
        'Alcance: Formato 09. Arquitectura: Formato 11 (F11-R). Variables y operacionalización: F29C.',
        'Diseño y arquitectura tecnológica: docs/final-report/06-diseno-sistema.md y 07-arquitectura-tecnologica.md.',
        'Estrategia y automatización de pruebas de la v1.0: docs/final-report/11 a 13.',
        'Trazabilidad: docs/final-report/traceability-master.md; TDD: docs/tdd-evidence.md; defectos: docs/defects.md.',
        'Suite E2E: docs/testing/cypress-e2e.md. Entorno: docs/docker.md. QA de release v1.1: docs/v1.1/phase-25-final-qa.md.',
        'Norma ISO/IEC 25010, usada solo como marco de referencia de calidad (sin certificación).',
    ]))

    h(1, 'Glosario')
    B.append(('table', ['Término', 'Definición'], [
        ('CP', 'Caso de prueba (CP-001 en adelante), definido en la F29E'),
        ('CU', 'Caso de uso del Formato 08 (CU-01 a CU-20)'),
        ('RF / RNF', 'Requerimiento funcional (RF-01 a RF-27) y no funcional (RNF-01 a RNF-10)'),
        ('TDD', 'Desarrollo guiado por pruebas: prueba que falla, implementación mínima y refactorización'),
        ('E2E', 'Prueba de extremo a extremo en navegador (Cypress)'),
        ('Regresión', 'Repetición de pruebas ya aprobadas para detectar fallos introducidos por cambios'),
        ('Multitenencia', 'Aislamiento de los datos de cada organización (`organization_id`)'),
        ('Flaky', 'Prueba que falla de forma intermitente sin cambios en el código'),
        ('CI', 'Integración continua: ejecución automática de pruebas en cada push (GitHub Actions)'),
        ('RACI', 'Responsable, Aprueba, Consultado, Informado'),
        ('EXPERIMENTAL / PROPUESTO', 'Estado de RF-29: validado solo con datos sintéticos, fuera de la línea base'),
    ], [0.25, 0.75]))
    return B


def rnf_tabla():
    return [(r[0], r[2], r[1], r[8]) for r in N.RNF]
