"""F29H — Informe Final v1: contenido de cada sección de la plantilla Plantilla_Estructura_de_proyecto_final.docx.

Las claves son los títulos exactos de la plantilla (Título 2 numerado o Título 1 final). Las tablas se generan desde
los modelos académicos (F2–F11, F29C) y desde la evidencia de la F29D–F29G, para no copiar a mano lo ya verificado.
Nada de lo que aquí se afirma es validación institucional ni beneficio medido. Las fases F30 y posteriores solo se
mencionan como trabajo futuro.
"""
import collections
import re

import f29e
import m_arch as AR
import m_asis as A
import m_common as C
import m_cu as U
import m_defectos as MD
import m_plan as MP
import m_problems as P
import m_rf as R
import m_rnf as N
import m_tobe as T
import m_variables as V
import qa_data as Q

FECHA = '30/09/2026'
TITULO = C.PROYECTO
VERSION = 'Informe Final v1'
PD = 'docs/academico/powerdesigner/exports/'
PD11 = 'docs/v1.1/powerdesigner/exports/'

ESTADOS_NOTA = ('Estados de la información usados en todo el informe: HECHO VERIFICADO (comprobado en el repositorio), '
                'AS-IS PRELIMINAR (reconstrucción del equipo, sin validación institucional), TO-BE PROPUESTO (proceso '
                'diseñado, no adoptado por la institución), SOFTWARE IMPLEMENTADO (comportamiento de la plataforma '
                'verificado con pruebas) y EXPERIMENTAL / PROPUESTO (RF-29, fuera de la línea base).')


def _qa():
    cs = f29e.casos()
    tot = lambda s, k: sum(c[k] for c in cs if c['suite'] == s)
    return cs, tot


def secciones():
    cs, tot = _qa()
    cov = f29e.cobertura_rf(cs)
    defs = MD.registro()
    abiertos = [d for d in defs if not d['estado'].startswith('Cerrado')]
    dev, dev_sha = Q.ci_estado('develop')
    main, main_sha = Q.ci_estado('main')
    rnf_estado = collections.Counter(r[8] for r in N.RNF)
    S = {}

    # ------------------------------------------------------------ capítulo 1
    S['Resumen Ejecutivo'] = [
        ('note', ESTADOS_NOTA),
        ('p', '**Problema (AS-IS PRELIMINAR).** El análisis del proceso de reclutamiento, evaluación y selección del '
              'Colegio Andino de Huancayo (caso de estudio académico) identificó cinco problemas: información distribuida '
              '(P1), seguimiento manual (P2), evaluaciones heterogéneas (P3), comunicación manual con los postulantes (P4) '
              'e indicadores limitados para sustentar la decisión (P5). No hay validación institucional de este análisis.'),
        ('p', '**Solución (SOFTWARE IMPLEMENTADO).** Plataforma web SaaS multiempresa que cubre el proceso completo en '
              '27 requerimientos funcionales (RF-01 a RF-27): requerimiento de personal y su aprobación, vacante con '
              'perfil y criterios ponderados, postulación con CV, preselección y etapas, evaluaciones y entrevistas, '
              'ranking explicable, decisión final, selección, cierre, notificaciones y auditoría. El ranking calcula, '
              'ordena y compara; **la decisión final la registra una persona** (Aprobador / Dirección, RF-23).'),
        ('p', '**Tecnologías.** Laravel 13 (PHP 8.4), React 19 con TypeScript e Inertia 3, Tailwind 4, PostgreSQL 17, '
              'Redis 7 y Docker Compose. La versión v1.1 agrega un servicio experimental (Python, scikit-learn y FastAPI) '
              'que estima el riesgo de demora del **proceso** (RF-29, EXPERIMENTAL): no evalúa, ordena ni selecciona '
              'personas.'),
        ('p', '**Enfoque de calidad.** Desarrollo guiado por pruebas (TDD), pruebas automatizadas en cuatro suites, '
              'integración continua en GitHub Actions, registro de defectos con prueba de regresión e ISO/IEC 25010 '
              'como marco de referencia (sin certificación).'),
        ('p', f'**Resultados (HECHO VERIFICADO, ejecución QA del {FECHA} sobre el commit bc44303).** PHPUnit '
              f'{tot("PHPUnit", "passed")} pruebas aprobadas y {tot("PHPUnit", "skipped")} omitidas, sin fallos; Cypress '
              f'{tot("Cypress", "passed")}/{tot("Cypress", "n")}; Vitest {tot("Vitest", "passed")}/{tot("Vitest", "n")}; '
              f'pytest {tot("pytest", "passed")}/{tot("pytest", "n")}; TypeScript y build sin errores. Los 27 RF tienen al '
              'menos un caso de prueba automatizado aprobado. No se midió cobertura de código ni rendimiento, y no hay '
              'beneficios medidos en la institución.'),
    ]
    S['Introducción'] = [
        ('p', '**Contexto.** La gestión del talento en una institución educativa exige procesos trazables y '
              'comparables. El proyecto toma como caso de estudio académico al Colegio Andino de Huancayo y diseña una '
              'plataforma SaaS: una sola aplicación que atiende a varias organizaciones con los datos de cada una '
              'aislados (`organization_id`).'),
        ('p', '**Importancia de las pruebas.** El proyecto pertenece al curso Pruebas y Calidad de Software. Cada '
              'regla de negocio se escribió primero como una prueba que falla (TDD); la regresión automática protege '
              'cada cambio; la integración continua repite build, TypeScript y PHPUnit en cada push; y cada defecto '
              'encontrado quedó registrado con su prueba de regresión.'),
        ('p', '**Propósito.** Analizar, diseñar, implementar y verificar una plataforma que atienda los problemas '
              'identificados, con la decisión humana de selección y la evidencia verificable de calidad como '
              'requisitos centrales.'),
        ('p', '**Estructura.** Los capítulos 2 y 3 describen el contexto y el proceso (AS-IS y TO-BE); el 4, los '
              'requerimientos; el 5, la planificación y el plan de calidad; el 6 y el 7, el diseño y la arquitectura; el '
              '8 al 10, el desarrollo, el control de versiones y la dockerización; el 11 al 13, la estrategia, la '
              'automatización y las métricas de pruebas; y el 14, la implementación y el monitoreo. Siguen las '
              'conclusiones, las recomendaciones, las referencias y los anexos.'),
    ]

    # ------------------------------------------------------------ capítulo 2
    S['Contexto de la Organización'] = [
        ('p', 'El Colegio Andino de Huancayo es el **caso de estudio académico** del proyecto. El repositorio no '
              'contiene documentación institucional verificada: no hay estadísticas de contratación, número de '
              'postulantes, organigrama ni herramientas actuales confirmadas. El contexto se describe como AS-IS '
              'PRELIMINAR, pendiente de validación con RR. HH. y la Administración del colegio.'),
        ('ul', ['**Actividades principales (AS-IS PRELIMINAR):** ' + '; '.join(f'{m[0]}) {m[1]}' for m in A.MACRO) + '.',
                '**Área donde se presenta el problema:** reclutamiento, evaluación y selección de docentes y personal, '
                'con participación del área solicitante, RR. HH., la Dirección, los evaluadores y los postulantes.',
                '**Herramientas actuales:** no identificadas. El AS-IS preliminar no identifica ninguna herramienta '
                'informática del Colegio, y no se afirma que el proceso sea en papel, por correo ni con otra '
                'herramienta: queda pendiente de validación.']),
        ('p', 'Fuentes: Formato 02 (análisis del proceso) en docs/academico/practica-02 y capítulo 2 de la documentación v1.0.'),
    ]
    S['Identificación del Problema'] = [
        ('p', 'Problemas del proceso actual (AS-IS PRELIMINAR, Formato 04). Ninguno se midió: son hallazgos del análisis '
              'del equipo pendientes de validación.'),
        ('table', ['ID', 'Problema', 'Descripción', 'Causa', 'Impacto (consecuencia operativa)', 'Prioridad'],
         [(p['id'], p['nombre'], p['descripcion'], p['causa'], p['impacto'], p['prioridad']) for p in P.PROBLEMAS],
         [0.06, 0.13, 0.27, 0.18, 0.26, 0.10], 14),
        ('p', '**Impacto en la eficiencia del proceso:** la falta de un registro único, de estados sistematizados y de '
              'criterios comunes dificulta reconstruir cada convocatoria, justificar la decisión y comunicar a tiempo a '
              'los postulantes. No se cuantificó ese impacto (no hay línea base medida).'),
    ]

    # ------------------------------------------------------------ capítulo 3
    S['Descripción del Proceso Actual'] = [
        ('p', f'El proceso actual (AS-IS PRELIMINAR) se modeló en el Formato 02 con {len(A.ACTIVIDADES)} actividades '
              '(AS-01 a AS-' + f'{len(A.ACTIVIDADES):02d}) agrupadas en {len(A.MACRO)} macroactividades:'),
        ('table', ['#', 'Macroactividad', 'Responsable', 'Problemas'], [m for m in A.MACRO], [0.06, 0.52, 0.24, 0.18], 16),
    ]
    S['Modelado del Proceso Actual (AS-IS)'] = [
        ('p', 'El diagrama BPMN AS-IS se formalizó en PowerDesigner (Formato 03 y fase F29): pools del Colegio y del '
              'Postulante, carriles por actor y mensajes entre pools. Se reproduce en el **Anexo A**.'),
        ('table', ['ID', 'Actividad', 'Descripción'], [(a[0], a[1], a[2]) for a in A.ACTIVIDADES], [0.09, 0.33, 0.58], 14),
    ]
    S['Problemas del Proceso Actual'] = [
        ('p', 'Relación entre los problemas y las actividades del AS-IS en las que aparecen (Formato 04):'),
        ('table', ['Problema', 'Actividades AS-IS', 'Validación pendiente con'],
         [(f'{p["id"]} {p["nombre"]}', ', '.join(p['actividades']), p['validacion']) for p in P.PROBLEMAS],
         [0.36, 0.40, 0.24], 16),
    ]
    S['Modelado del Proceso Propuesto (TO-BE)'] = [
        ('p', 'El proceso propuesto (TO-BE PROPUESTO, Formato 05) atiende cada problema con una solución y un objetivo '
              'de mejora. El BPMN TO-BE formal de PowerDesigner está en el **Anexo B**. Su adopción por la institución '
              'no está validada.'),
        ('table', ['Problema', 'Solución', 'Descripción', 'RF'], [(s[0], f'{s[1]} {s[3]}', s[2], ', '.join(s[5])) for s in T.SOLUCIONES],
         [0.10, 0.22, 0.46, 0.22], 14),
        ('table', ['Objetivo de mejora', 'Descripción', 'Problema'], [o for o in T.OBJETIVOS_MEJORA], [0.16, 0.70, 0.14], 16),
    ]

    # ------------------------------------------------------------ capítulo 4
    S['Identificación de Actores del Sistema'] = [
        ('table', ['ID', 'Actor', 'Rol en el sistema', 'Tipo'], [a for a in C.ACTORES_SISTEMA], [0.12, 0.40, 0.28, 0.20], 16),
        ('p', 'Además actúa el **Sistema** en las notificaciones automáticas (RF-04, RF-11, RF-15, RF-17 y RF-26). No hay '
              'rol de superadministración (fuera de alcance, OUT-03).'),
    ]
    S['Requerimientos Funcionales'] = [
        ('p', 'Línea base de 27 requerimientos funcionales (Formato 06), todos SOFTWARE IMPLEMENTADO y con prueba '
              'automatizada. RF-28 es candidato no implementado y RF-29 es EXPERIMENTAL / PROPUESTO: ninguno de los dos '
              'forma parte de la línea base.'),
        ('table', ['RF', 'Requerimiento', 'Descripción', 'Actor'], [r[:4] for r in R.RF], [0.08, 0.26, 0.48, 0.18], 14),
    ]
    S['Requerimientos no Funcionales'] = [
        ('p', f'Diez RNF académicos (Formato 07), clasificados con ISO/IEC 25010 como marco de referencia. Estado: '
              f'{rnf_estado["VERIFICADO"]} verificados, {rnf_estado["EVIDENCIA PARCIAL"]} con evidencia parcial y '
              f'{rnf_estado["NO VERIFICADO"]} no verificados.'),
        ('table', ['RNF', 'Característica', 'Nombre', 'Criterio', 'Estado'], [(r[0], r[1], r[2], r[4], r[8]) for r in N.RNF],
         [0.08, 0.16, 0.18, 0.44, 0.14], 14),
    ]
    S['Casos de Uso del Sistema'] = [
        ('p', 'Veinte casos de uso (Formato 08), formalizados en PowerDesigner. El diagrama está en el **Anexo C**.'),
        ('table', ['CU', 'Caso de uso', 'Descripción', 'RF'], [(c[0], c[1], c[2], ', '.join(c[4])) for c in U.CU],
         [0.08, 0.28, 0.46, 0.18], 14),
    ]

    # ------------------------------------------------------------ capítulo 5
    S['Alcance del Proyecto'] = [
        ('p', 'Alcance del Formato 09 (entregable final v1.1): ocho bloques incluidos y once exclusiones explícitas.'),
        ('table', ['Incluido', 'Bloque'], [('IN-01', 'Requerimientos'), ('IN-02', 'Vacantes'), ('IN-03', 'Cuenta y postulación'),
                                            ('IN-04', 'Seguimiento'), ('IN-05', 'Evaluación y entrevista'),
                                            ('IN-06', 'Comparación y ranking'), ('IN-07', 'Decisión y cierre'), ('IN-08', 'Auditoría')],
         [0.25, 0.75], 16),
        ('table', ['Excluido', 'Descripción'], [
            ('OUT-01, OUT-02', 'Facturación SaaS, planes y suscripciones'), ('OUT-03', 'Superadministración comercial'),
            ('OUT-04, OUT-05', 'Selección automática por IA o ML e inferencia de personalidad o idoneidad'),
            ('OUT-06, OUT-07', 'Banco de talentos; dashboards e indicadores avanzados'),
            ('OUT-08 a OUT-10', 'Proveedores externos, infraestructura productiva en la nube, integraciones no especificadas'),
            ('OUT-11', 'Uso productivo o decisorio del riesgo operacional ML (RF-29)')], [0.25, 0.75], 16),
    ]
    S['Herramientas Tecnológicas del Proyecto'] = [
        ('table', ['Área', 'Herramienta'], [
            ('Backend', 'PHP 8.4, Laravel 13, Fortify, Inertia 3'), ('Frontend', 'React 19, TypeScript, Tailwind 4, Vite'),
            ('Datos', 'PostgreSQL 17, Redis 7'), ('ML experimental', 'Python 3.12, scikit-learn, FastAPI (fuera de Compose)'),
            ('Pruebas', 'PHPUnit, Cypress 15.3.0, Vitest, pytest'), ('Entorno', 'Docker Desktop y Docker Compose'),
            ('Versiones y CI', 'Git, GitHub y GitHub Actions'), ('Modelado', 'PowerDesigner (BPMN, UML y modelo físico)'),
            ('Asistencia', 'Claude (implementación asistida) y Codex (auditoría), bajo dirección del equipo')], [0.25, 0.75], 16),
    ]
    S['Normas y Estándares de Calidad'] = [
        ('p', 'ISO/IEC 25010 se usa como **marco de referencia** para clasificar los RNF y organizar la evaluación de '
              'calidad (capítulo 13). No se declara certificación ni conformidad con la norma.'),
        ('ul', ['Estándares de práctica: TDD, integración continua, revisión independiente de cada fase y registro de '
                'defectos con prueba de regresión.',
                'Accesibilidad: criterios WCAG 2.2 revisados en la Fase 21 (contraste AA, reflow y foco visible), sin '
                'auditoría formal externa.',
                'Datos: solo ficticios; ninguna información personal real.']),
    ]
    S['Plan de Pruebas del Proyecto'] = [
        ('p', 'El plan formal está en el Plan de Pruebas de Software (F29D, docs/academico/plan-pruebas/), sobre la '
              'plantilla del curso. Define alcance, estrategia en niveles, criterios de aceptación CA-01 a CA-07, '
              'suspensión y reanudación, recursos, RACI, cronograma y riesgos. No está aprobado ni firmado: la aprobación '
              'académica está pendiente.'),
        ('table', ['Criterio', 'Descripción'], [
            ('CA-01', 'PHPUnit sin fallos; solo las 8 omitidas del starter kit'), ('CA-02', 'Cypress 20 specs sin fallos ni reintentos'),
            ('CA-03', 'Vitest y pytest sin fallos'), ('CA-04', 'TypeScript y build sin errores'), ('CA-05', 'CI en verde en develop'),
            ('CA-06', 'Cada RF-01 a RF-27 con un caso automatizado aprobado'), ('CA-07', 'Ningún defecto Alto abierto')],
         [0.15, 0.85], 16),
    ]
    S['Lineamientos de Seguridad Informática'] = [
        ('ul', ['Autenticación con Fortify; contraseñas con hash; límite de intentos de inicio de sesión (RNF-01).',
                'Autorización en el servidor con Policies que comparan rol **y** organización; middleware de rol.',
                'Aislamiento multiempresa por `organization_id` con scope global y pruebas de acceso cruzado (RNF-02).',
                'Auditoría de solo inserción: la tabla `audit_logs` rechaza UPDATE y DELETE con un trigger (RNF-03).',
                'Privacidad: perfil mínimo del postulante y CV en almacenamiento privado (RNF-04).',
                'Endpoints de soporte E2E inertes fuera del entorno aislado y protegidos por token (DEF-13).',
                'Secretos fuera de Git (`.env`, `.env.e2e`); Postgres y Redis publicados solo en 127.0.0.1.',
                'Límites: sin pruebas de penetración ni análisis dinámico (OWASP ZAP); RLS de PostgreSQL no implementado.']),
    ]

    # ------------------------------------------------------------ capítulo 6
    S['Arquitectura Conceptual del Sistema'] = [
        ('p', 'Monolito modular SaaS multiempresa (Formato 11, regularizado en la F11-R). Diecisiete componentes '
              'conceptuales (CMP-01 a CMP-17) y veinte relaciones (R-01 a R-20). CMP-17 (RF-29) es EXPERIMENTAL y '
              'opcional: la aplicación funciona igual sin él.'),
        ('img', PD + 'ARQ-01_Arquitectura_Conceptual.png', 'Figura 1. Arquitectura conceptual ARQ-01 (PowerDesigner, F29).'),
        ('table', ['CMP', 'Componente', 'Capa'], [(f'CMP-{c[0][1:]}', c[1], c[2]) for c in AR.COMPONENTES], [0.12, 0.50, 0.38], 14),
    ]
    S['Modelo UML del Sistema'] = [
        ('p', 'La especificación UML del sistema implementado (AS-IS del software, Fase 22) se formalizó en PowerDesigner '
              '(Fase 23): clases del dominio, enumeraciones, componentes, paquetes, despliegue, ocho diagramas de '
              'secuencia, estados del requerimiento y de la vacante, y actividades. Exportaciones en docs/v1.1/powerdesigner/.'),
        ('img', PD11 + 'CL-01-clases-del-dominio.png', 'Figura 2. Diagrama de clases del dominio CL-01 (PowerDesigner, F23).'),
    ]
    S['Diseño de Interfaces de Usuario'] = [
        ('p', 'Interfaz Inertia / React con navegación por rol. La v1.1 la rediseñó (Fases 18 a 21): sistema de diseño '
              'propio con modo oscuro, tablas que se convierten en fichas en móvil sin perder semántica, microinteracciones '
              'que respetan el movimiento reducido y una portada con profundidad en CSS 3D, decorativa y con póster de '
              'respaldo.'),
        ('ul', ['Accesibilidad verificada con pruebas automatizadas (E2E-16 a E2E-19 y componentes Vitest): contraste AA, '
                '`main` en todas las pantallas, enlace de salto, foco visible, reflow a 320 px.',
                'La tarjeta de riesgo operacional (RF-29) se muestra solo en la ficha de la vacante, rotulada como '
                'experimental, y nunca junto a candidatos ni al ranking.']),
    ]
    S['Diseño de Base de Datos'] = [
        ('p', 'Modelo físico PostgreSQL con restricciones de integridad (claves foráneas, CHECK y únicos), '
              '`organization_id` en las entidades de negocio y un trigger que convierte `audit_logs` en tabla de solo '
              'inserción. Se formalizó como modelo físico en PowerDesigner (PDM-01 y PDM-02, Fase 23).'),
        ('img', PD11 + 'PDM-01-esquema-completo.png', 'Figura 3. Modelo físico de datos PDM-01 (PowerDesigner, F23).'),
    ]

    # ------------------------------------------------------------ capítulo 7
    S['Tecnologías del Frontend'] = [
        ('table', ['Tecnología', 'Uso'], [('React 19 + TypeScript', 'Páginas y componentes'), ('Inertia 3', 'Puente SPA con Laravel, sin API separada'),
                                          ('Tailwind 4 (componentes shadcn/ui)', 'Estilos y sistema de diseño'),
                                          ('Vite (vite-plus `vp`)', 'Empaquetado, pruebas de componentes y formato'),
                                          ('Laravel Wayfinder', 'Rutas tipadas')], [0.40, 0.60], 16),
    ]
    S['Tecnologías del Backend'] = [
        ('table', ['Tecnología', 'Uso'], [('PHP 8.4 + Laravel 13', 'Aplicación y reglas de negocio (monolito modular)'),
                                          ('Fortify', 'Autenticación'), ('Policies y Form Requests', 'Autorización y validación en el servidor'),
                                          ('Colas con Redis', 'Notificaciones asíncronas enviadas tras confirmar la transacción'),
                                          ('Servicio ML (FastAPI)', 'RF-29 EXPERIMENTAL, llamado solo si `ML_SERVICE_ENABLED=true`')],
         [0.40, 0.60], 16),
    ]
    S['Base de Datos del Sistema'] = [
        ('ul', ['PostgreSQL 17 con tres bases: `reclutamiento` (desarrollo y demostración), `reclutamiento_testing` '
                '(PHPUnit) y `reclutamiento_e2e` (Cypress). Las pruebas nunca tocan la de demostración.',
                'Redis 7 para sesiones, caché y colas; el entorno E2E usa sus propias bases de Redis.',
                'Datos de demostración ficticios generados por `DemoSeeder` (docs/demo-users.md).']),
    ]
    S['Infraestructura de Desarrollo'] = [
        ('p', 'Todo el entorno corre en Docker Compose con versiones fijadas; no se usan PHP ni Node del equipo host. '
              'Servicios: `app`, `queue`, `postgres`, `redis` y, en el perfil e2e, `app-e2e`, `queue-e2e` y `cypress`. '
              'El servicio ML corre fuera de Compose, en su entorno virtual. La integración continua usa GitHub Actions.'),
    ]

    # ------------------------------------------------------------ capítulo 8
    S['Iteración 1: Configuración Inicial del Proyecto'] = [
        ('ul', ['Repositorio Git con `main` y `develop`; bootstrap de Laravel (`e87ef39`).',
                'Frontend React + Inertia + TypeScript y backend Laravel desde el kit inicial.',
                'PostgreSQL y Redis en Docker; autenticación, organizaciones, roles y aislamiento multiempresa '
                '(`feature/tenancy-roles`, merge `d696032`).',
                'Defectos DEF-01 y DEF-02 (entorno Docker y variables de PHPUnit), corregidos en esta iteración.']),
    ]
    S['Iteración 2: Desarrollo de Funcionalidades Básicas'] = [
        ('ul', ['Requerimientos de personal y vacantes: RF-01 a RF-07 (merge `5ab6e22`), con máquinas de estado y '
                'validación de ponderaciones.',
                'Primeras páginas Inertia conectadas a controladores delgados que delegan en servicios.',
                'Ciclos TDD registrados en docs/tdd-evidence.md.']),
    ]
    S['Iteración 3: Implementación de Módulos Funcionales'] = [
        ('ul', ['Postulantes y postulaciones: RF-08 a RF-15 (merge `f20f0b6`).',
                'Evaluaciones y entrevistas: RF-16 a RF-19 (merge `40eda7d`), con checkpoint RED previo (`3e66623`).',
                'Ranking, decisión humana, selección y cierre: RF-20 a RF-25 (merge `dda4bd0`).',
                'Notificaciones y auditoría: RF-26 y RF-27 (merge `cd092d1`). Formularios, validaciones y operaciones '
                'CRUD con autorización por rol y organización.']),
    ]
    S['Iteraciones Posteriores'] = [
        ('table', ['Iteración', 'Contenido', 'Problemas y soluciones'], [
            ('Fase 8', 'Frontend integral y validación manual en navegador', 'DEF-09 a DEF-11 (zona horaria, etiquetas, iniciales)'),
            ('Fases 9 y 10', 'Suite E2E con Cypress; Docker y entorno E2E aislado', 'DEF-12 y DEF-13 (fechas E2E, reset aislado)'),
            ('Fases 13 a 17', 'Gobierno de v1.1; servicio ML experimental y su integración (RF-29)', 'GAP-01 resuelto técnicamente (`target_completion_at`)'),
            ('Fases 18 a 21', 'Rediseño, movimiento accesible, CSS 3D en la portada y QA visual', 'Hallazgos F21 A1–A4, V1–V3, F19-R y M1, corregidos'),
            ('Fases 22 a 26', 'UML, PowerDesigner, Formato 09, QA global y release v1.1', 'F25-M01 y F25-M02 corregidos; F25-L03 abierto (formato)'),
            ('F27 a F29H', 'Formatos académicos F2–F11, variables (F29C), plan, casos, QA final, métricas e informe', 'Sin fallos en la QA final'),
        ], [0.16, 0.46, 0.38], 14),
    ]

    # ------------------------------------------------------------ capítulo 9
    S['Repositorio del Proyecto'] = [
        ('p', 'Repositorio Git publicado en GitHub (`luivmz/saas-reclutamiento-multiempresa`). Al '
              f'{FECHA}, `develop` tiene 145 commits (33 merges) y existen las etiquetas `v1.0.0-academic` '
              '(`9a946c2`, línea base académica) y `v1.1.0-academic`. Los secretos (`.env`, `.env.e2e`) no se versionan.'),
    ]
    S['Estrategia de Control de Versiones'] = [
        ('ul', ['Git Flow simplificado: `main` estable, `develop` de integración y ramas `feature/*` por fase.',
                'Cada fase se integra con `git merge --no-ff` tras su auditoría y con la CI en verde.',
                'Commits convencionales (`feat`, `test`, `docs`, `chore`) y checkpoints TDD (RED) como commits propios.',
                'Nunca `push --force`, rebase de historia publicada ni etiquetas movidas.']),
    ]
    S['Gestión de Ramas del Proyecto'] = [
        ('table', ['Rama', 'Uso'], [('main', 'Versiones publicadas (v1.0 y v1.1 académicas)'),
                                    ('develop', 'Integración de todas las fases'),
                                    ('feature/*', 'Una rama por fase (por ejemplo, feature/f29d-h-finalization)')], [0.25, 0.75], 16),
    ]
    S['Registro de Commits Relevantes'] = [
        ('table', ['Commit', 'Descripción'], [
            ('e87ef39', 'Bootstrap de la aplicación Laravel'), ('3e66623', 'Checkpoint RED de evaluaciones y entrevistas (TDD)'),
            ('7a65bee', 'Ranking, decisión final humana, selección y cierre'), ('a77c916', 'Suite E2E de Cypress completa'),
            ('ccf05d1', 'Imágenes Docker fijadas y entorno E2E aislado'), ('9a946c2', 'Etiqueta v1.0.0-academic'),
            ('2b97fe3', 'Cierre de la Fase 25 (QA global v1.1)'), ('bc44303', 'Integración de la F29C (variables); commit probado en la QA final')],
         [0.18, 0.82], 16),
    ]

    # ------------------------------------------------------------ capítulo 10
    S['Introducción a Docker en el Proyecto'] = [
        ('p', 'Docker Compose permite levantar el sistema completo con un solo comando (`docker compose up -d --wait`) y '
              'garantiza que las pruebas y la demostración usen las mismas versiones. Todas las imágenes están fijadas.'),
    ]
    S['Dockerización del Backend'] = [
        ('p', 'Imagen `reclutamiento-php:dev` (PHP 8.4.25 con Composer y Node). El contenedor `app` instala dependencias '
              'si faltan, compila los assets, migra y sirve la aplicación; `queue` procesa las notificaciones. Su '
              'healthcheck `GET /health` verifica la base de datos y Redis.'),
    ]
    S['Dockerización del Frontend'] = [
        ('p', 'El frontend no tiene contenedor propio: Vite compila los assets dentro de la imagen de la aplicación '
              '(`npm run build`) y Laravel los sirve con Inertia. TypeScript, Vitest y el build se ejecutan en el mismo '
              'contenedor.'),
    ]
    S['Orquestación con Docker Compose'] = [
        ('table', ['Servicio', 'Imagen', 'Función'], [
            ('app', 'reclutamiento-php:dev', 'Aplicación (healthcheck /health)'), ('queue', 'reclutamiento-php:dev', 'Worker de notificaciones'),
            ('postgres', 'postgres:17.11-alpine', 'Bases de desarrollo, pruebas y E2E'), ('redis', 'redis:7.4.11-alpine', 'Sesiones, caché y colas'),
            ('app-e2e, queue-e2e', 'reclutamiento-php:dev', 'Entorno aislado para Cypress (perfil e2e)'),
            ('cypress', 'cypress/included:15.3.0', 'Suite E2E')], [0.24, 0.30, 0.46], 16),
        ('img', PD11 + 'DE-01-despliegue.png', 'Figura 4. Diagrama de despliegue DE-01 (PowerDesigner, F23).'),
    ]

    # ------------------------------------------------------------ capítulo 11
    S['Enfoque de Pruebas del Proyecto'] = [
        ('p', 'Enfoque guiado por pruebas: cada regla se especifica primero como una prueba que falla y la '
              'automatización tiene prioridad sobre la prueba manual. La estrategia completa está en el Plan de Pruebas '
              '(F29D). Los datos son siempre ficticios y las bases de prueba están aisladas de la de demostración.'),
    ]
    S['Niveles de Pruebas Aplicados'] = [
        ('table', ['Nivel', 'Herramienta', 'Alcance'], [
            ('Unitario', 'PHPUnit (tests/Unit)', 'Estados, validadores y servicio de ranking'),
            ('Integración / funcional', 'PHPUnit (tests/Feature) sobre PostgreSQL real', 'RF-01 a RF-27, autorización, notificaciones, auditoría'),
            ('Sistema (E2E)', 'Cypress 15.3.0', 'Flujos por rol y flujo completo en navegador'),
            ('Componentes', 'Vitest', 'Componentes de interfaz y accesibilidad'),
            ('Aceptación', 'Flujo E2E-13 y recorrido manual (Fase 8)', 'Sin aceptación institucional')], [0.22, 0.34, 0.44], 16),
    ]
    tipos = collections.Counter(c['tipo'] for c in cs)
    S['Tipos de Pruebas Ejecutadas'] = [
        ('p', f'Distribución de los {len(cs)} casos de prueba de la F29E por tipo (el detalle está en docs/academico/casos-prueba/):'),
        ('table', ['Tipo de prueba', 'Casos'], sorted(tipos.items()), [0.70, 0.30], 16),
    ]
    S['Plan de Ejecución de Pruebas'] = [
        ('p', 'Orden de ejecución de cierre (F29F), con el árbol de trabajo limpio y la salida completa de cada '
              'herramienta guardada como evidencia: configuración de Compose → PHPUnit → TypeScript → build → Vitest → '
              'pytest → Cypress. Cualquier fallo se clasifica (regresión real, flaky, ambiente, dependencia externa, '
              'documental o no aplicable) y nunca se oculta; el runtime no se corrige sin autorización del equipo.'),
    ]

    # ------------------------------------------------------------ capítulo 12
    S['Herramientas de Automatización'] = [
        ('table', ['Herramienta', 'Suite', 'Archivos'], [
            ('PHPUnit 12', 'Unitarias e integración', '6 unitarios, 42 de integración'), ('Cypress 15.3.0', 'E2E', '20 specs'),
            ('Vitest (vp test)', 'Componentes', '6 archivos'), ('pytest', 'Servicio ML experimental', '18 archivos'),
            ('GitHub Actions', 'Integración continua', '.github/workflows/tests.yml')], [0.28, 0.40, 0.32], 16),
    ]
    S['Configuración del Entorno de Pruebas'] = [
        ('ul', ['PHPUnit fuerza `DB_DATABASE=reclutamiento_testing` en phpunit.xml (DEF-02) y usa RefreshDatabase.',
                'Cypress corre en su imagen oficial contra `app-e2e`, con `.env.e2e` generado por `npm run e2e:setup` '
                '(token y clave aleatorios, nunca versionados) y reset por endpoint protegido.',
                'Sin reintentos en Cypress (`retries: 0`): un fallo intermitente se investiga.',
                'El servicio ML se prueba en su entorno virtual con dataset sintético y contrato congelado.']),
    ]
    S['Scripts de Pruebas Automatizadas'] = [
        ('p', 'Las pruebas viven con el código: `tests/Unit`, `tests/Feature`, `cypress/e2e`, `resources/js/**/*.test.tsx` y '
              '`ml-service/tests`. Los nombres `test_rfNN_*` enlazan cada prueba con su RF, y la matriz de trazabilidad '
              '(F29E) enlaza RF → CU → caso de prueba → prueba automatizada → evidencia.'),
    ]
    S['Ejecución Automática de Pruebas'] = [
        ('p', 'GitHub Actions ejecuta en cada push a `develop` y `main` la instalación de dependencias, el build, '
              'TypeScript y PHPUnit. Cypress, Vitest y pytest se ejecutan en local con Docker y el entorno virtual.'),
        ('table', ['Rama', 'Commit', 'Resultado'], [
            ('develop', dev_sha[:7], dev['conclusion'] if dev else 'sin ejecución'),
            ('main', main_sha[:7], main['conclusion'] if main else 'sin ejecución: pendiente de ejecución manual')], [0.2, 0.2, 0.6], 16),
    ]

    # ------------------------------------------------------------ capítulo 13
    S['Ejecución de Casos de Pruebas'] = [
        ('p', f'Ejecución QA final del {FECHA} sobre el commit `bc44303` (F29F). Resultados reales:'),
        ('table', ['Suite', 'Ejecutadas', 'Aprobadas', 'Fallidas', 'Omitidas'],
         [(s, tot(s, 'n'), tot(s, 'passed'), tot(s, 'failed'), tot(s, 'skipped')) for s in ('PHPUnit', 'Cypress', 'Vitest', 'pytest')],
         [0.28, 0.18, 0.18, 0.18, 0.18], 16),
        ('p', 'TypeScript sin errores y build sin errores. Las 8 omitidas de PHPUnit dependen de la verificación de correo, '
              'desactivada en Fortify. Se cumplen los siete criterios de aceptación del plan.'),
    ]
    sev = collections.Counter(d['severidad'] for d in defs)
    S['Registro de Defectos'] = [
        ('p', f'Registro unificado de la F29G: {len(defs)} registros (13 de la v1.0 y {len(defs) - 13} de la v1.1, '
              f'incluidos hallazgos documentales y de proceso). Por severidad: {sev["Crítica"]} críticos, {sev["Alta"]} '
              f'altos, {sev["Media"]} medios y {sev["Baja"]} bajos. Cerrados: {len(defs) - len(abiertos)}. La QA final '
              'no produjo defectos nuevos del software.'),
        ('table', ['Abierto', 'Severidad', 'Estado'], [(d['id'], d['severidad'], d['estado']) for d in abiertos], [0.22, 0.18, 0.60], 16),
    ]
    rf_ok = sum(1 for v in cov.values() if v[0])
    S['Métricas de Calidad del Software'] = [
        ('table', ['Métrica', 'Valor'], [
            ('Tasa de aprobación (aprobadas / ejecutadas no omitidas)', '100 % en PHPUnit, Cypress, Vitest y pytest'),
            ('Cobertura funcional de RF (CP automatizado aprobado)', f'{rf_ok} de 27'),
            ('CU cubiertos a través de sus RF', '20 de 20'),
            ('Casos automatizados', f'{sum(1 for c in cs if c["auto"] == f29e.AUTO)} de {len(cs)}'),
            ('Estabilidad', 'Resultados idénticos a la QA de release F25 y entre las dos ejecuciones de PHPUnit'),
            ('Cobertura de código', 'NO MEDIDA (sin Xdebug ni PCOV)'),
            ('Rendimiento y disponibilidad', 'NO MEDIDOS (RNF-06 y RNF-07 no verificados)')], [0.55, 0.45], 16),
    ]
    S['Evaluación de Calidad basada en Estándares'] = [
        ('p', 'Evaluación organizada con ISO/IEC 25010, sin certificación: seguridad (confidencialidad, integridad y '
              'responsabilidad) verificada por RNF-01 a RNF-04 y RNF-10; usabilidad, compatibilidad y mantenibilidad con '
              'evidencia parcial; eficiencia de desempeño y fiabilidad no verificadas. Detalle en '
              'docs/academico/metricas-calidad/.'),
    ]

    # ------------------------------------------------------------ capítulo 14
    S['Preparación del Entorno de Implementación'] = [
        ('p', 'La implementación es un **entorno de desarrollo y demostración** con Docker: no existe entorno de '
              'producción. Requisitos: Docker Desktop, Git y el `.env` generado desde `.env.example` (docs/docker.md).'),
    ]
    S['Implementación del Sistema'] = [
        ('p', 'Instalación: clonar el repositorio, `docker compose up -d --wait` y cargar los datos ficticios con '
              '`docker compose exec app php artisan migrate:fresh --seed`. La aplicación queda en http://localhost:8000 '
              'con usuarios demo (docs/demo-users.md). El servicio ML es opcional y se activa con `ML_SERVICE_ENABLED=true`.'),
    ]
    S['Verificación de Funcionamiento'] = [
        ('p', 'La verificación de funcionamiento es la ejecución QA final (F29F): servicios healthy, suites sin fallos '
              'y flujo completo E2E-13 aprobado. No se verificó en un entorno institucional ni con usuarios reales.'),
    ]
    S['Monitoreo del Sistema'] = [
        ('table', ['Mecanismo', 'Uso'], [
            ('GET /health', 'Estado de la base de datos y Redis'), ('Healthchecks de Compose', 'app, queue, postgres y redis'),
            ('Logs de Laravel', 'storage/logs y salida del contenedor'), ('Tabla failed_jobs', 'Trabajos de cola fallidos'),
            ('Auditoría', 'audit_logs de solo inserción, consultable por Dirección')], [0.35, 0.65], 16),
        ('p', 'No hay monitoreo de errores en producción, alertas ni SLA: no se afirma disponibilidad ni rendimiento verificados.'),
    ]

    # ------------------------------------------------------------ finales
    S['CONCLUSIONES'] = [
        ('ul', [
            'Se implementó y verificó una plataforma SaaS multiempresa que cubre los 27 RF de la línea base, con la '
            'decisión final de selección siempre humana (RF-23).',
            f'La QA final del {FECHA} no registró fallos en ninguna suite y cumplió los siete criterios de aceptación; '
            'los 27 RF tienen al menos un caso automatizado aprobado.',
            'El proceso de pruebas (TDD, regresión automática, CI y registro de defectos con prueba de regresión) dejó '
            'trazabilidad completa RF → CU → caso de prueba → prueba → evidencia.',
            'El componente de riesgo operacional (RF-29) quedó como EXPERIMENTAL: validado solo con datos sintéticos, '
            'no evalúa personas y no está autorizado para producción.',
            'Los beneficios sobre el proceso del colegio no se midieron: la relación entre la plataforma y la gestión '
            'del proceso es una hipótesis (TO-BE PROPUESTO) y el AS-IS sigue preliminar.',
        ]),
    ]
    S['RECOMENDACIONES'] = [
        ('p', 'Trabajo futuro (fases posteriores; nada de esto está implementado):'),
        ('ul', ['Validar el AS-IS y el TO-BE con RR. HH. y la Administración del colegio.',
                'Ejecutar la CI de `main` pendiente (OBS-F29F-04) y aplicar el formato pendiente en un commit propio (F25-L03).',
                'Medir cobertura de código (PCOV) y agregar análisis estático.',
                'Pruebas de carga y objetivos de rendimiento (RNF-06); estrategia de disponibilidad y respaldo (RNF-07).',
                'Pruebas dinámicas de seguridad (OWASP ZAP) y Row Level Security en PostgreSQL.',
                'Monitoreo de errores y alertas; despliegue con imagen de producción y HTTPS.',
                'Decidir la promoción de RF-28 y RF-29 (candidatos) y validar institucionalmente cualquier uso del ML.']),
    ]
    S['REFERENCIAS'] = [
        ('ul', ['Universidad Continental. Guías de práctica 02 a 11 y Formatos oficiales del curso Pruebas y Calidad de '
                'Software (docs/academico/00-fuentes-oficiales/).',
                'Guía de laboratorio E1: Desarrollo de Software con Inteligencia Artificial (docs/academico/00-fuentes-oficiales/guias-ia/).',
                'Plantilla de Plan de Pruebas de Software del curso y Plantilla de estructura del proyecto final.',
                'ISO/IEC 25010, Systems and software quality models (usada como marco de referencia).',
                'W3C. Web Content Accessibility Guidelines (WCAG) 2.2.',
                'Documentación oficial de Laravel, React, Inertia, PostgreSQL, Redis, Docker, PHPUnit, Cypress, Vitest, '
                'pytest, scikit-learn y FastAPI.',
                'Repositorio del proyecto: documentación técnica (docs/), trazabilidad (docs/final-report/traceability-master.md) '
                'y entregables académicos (docs/academico/).']),
    ]
    S['ANEXOS'] = [
        ('table', ['Anexo', 'Contenido', 'Ubicación'], [
            ('A', 'BPMN AS-IS (PowerDesigner)', 'Página siguiente; docs/academico/practica-03'),
            ('B', 'BPMN TO-BE (PowerDesigner)', 'Página siguiente; docs/academico/practica-05'),
            ('C', 'Diagrama de casos de uso (PowerDesigner)', 'Página siguiente; docs/academico/practica-08'),
            ('D', 'Formatos académicos F2 a F11 (incluido F11-R) y alcance F9', 'docs/academico/practica-02 a practica-11; phase-24/output'),
            ('E', 'Variables y matriz de operacionalización (F29C)', 'docs/academico/operacionalizacion/'),
            ('F', 'Plan de Pruebas (F29D)', 'docs/academico/plan-pruebas/'),
            ('G', 'Casos de prueba y matriz de trazabilidad (F29E)', 'docs/academico/casos-prueba/'),
            ('H', 'Ejecución QA final y evidencias (F29F)', 'docs/academico/qa-final/'),
            ('I', 'Defectos y métricas (F29G)', 'docs/academico/metricas-calidad/'),
            ('J', 'Modelos PowerDesigner y exportaciones', 'docs/academico/powerdesigner/; docs/v1.1/powerdesigner/'),
            ('K', 'Docker, TDD y trazabilidad técnica', 'docs/docker.md; docs/tdd-evidence.md; docs/final-report/')],
         [0.08, 0.50, 0.42], 16),
    ]
    return S


# Diagramas anchos que van en páginas horizontales al final (anexos A a C).
ANEXOS_IMG = [
    (PD + 'F3_BPMN_ASIS.png', 'Anexo A. BPMN AS-IS del proceso de reclutamiento (AS-IS PRELIMINAR; PowerDesigner, F29).'),
    (PD + 'F5_BPMN_TOBE.png', 'Anexo B. BPMN TO-BE propuesto (TO-BE PROPUESTO; PowerDesigner, F29).'),
    (PD + 'F8_Casos_de_Uso_Academicos.png', 'Anexo C. Diagrama de casos de uso CU-01 a CU-20 (PowerDesigner, F29).'),
]
