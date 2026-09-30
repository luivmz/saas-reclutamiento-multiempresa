"""Contenido del Formato 11 oficial regularizado (fase F11-R).

Fuente formal: la plantilla oficial docs/academico/00-fuentes-oficiales/formatos-originales/
Formato_11_Arquitectura_del_sistema.docx (recibida después de la F28). Fuente complementaria: la Guía de Práctica 11.

La arquitectura NO se rediseña: componentes, relaciones, capas, decisiones y estados salen de m_arch.py (F11 adaptado,
F28), que no se modifica para que el F11 adaptado histórico se siga generando igual. Este módulo solo añade lo que pide
la estructura oficial: identificadores CMP-xx (equivalencia uno a uno con los históricos Cxx), estilo arquitectónico por
opción del formato, decisiones de diseño con su estado y restricciones por categoría. Cada afirmación remite a su fuente.
"""
import re

import m_arch as AR
import m_cu as U

FECHA = '29/09/2026'
TITULO = 'Formato 11 — Arquitectura del sistema (oficial, regularizado en F11-R)'

# Equivalencia de identificadores: CMP-xx (formato oficial) = Cxx (histórico: F11 adaptado, COMPONENTS.md,
# RELATIONSHIPS.md y el diagrama ARQ-01 de PowerDesigner).
CMP = {c[0]: 'CMP-' + c[0][1:] for c in AR.COMPONENTES}


def cmp_ref(expr):
    """«C04 a C11, C13» → «CMP-04 a CMP-11, CMP-13 (C04 a C11, C13)». Conserva la expresión histórica."""
    return re.sub(r'\bC(\d\d)\b', r'CMP-\1', expr) + f' ({expr})'


ESTADO_COMPONENTE = {
    'IMPLEMENTADO': 'SOFTWARE IMPLEMENTADO',
    'TRANSVERSAL': 'SOFTWARE IMPLEMENTADO (transversal)',
    'EXPERIMENTAL': 'EXPERIMENTAL / PROPUESTO',
}

NOTA_ESTADO = [
    'Regularización F11-R (29/09/2026): este documento vuelve a presentar sobre la **plantilla oficial del Formato 11** '
    'la arquitectura conceptual elaborada en la F28 y formalizada en PowerDesigner en la F29. **No cambia la '
    'arquitectura**: los componentes, las relaciones R-01 a R-20 y el diagrama ARQ-01 son los mismos. El F11 adaptado '
    'anterior (hecho cuando la plantilla oficial no estaba disponible) se conserva como versión histórica.',
]

# ------------------------------------------------------------------ 2. Descripción general del sistema
PROPOSITO = [
    '**Sistema:** plataforma web SaaS multiempresa para gestionar el reclutamiento, la evaluación y la selección de '
    'personal. Caso de estudio académico: Colegio Andino de Huancayo.',
    '**Propósito:** ' + dict(AR.CONTEXTO)['Objetivo'],
    '**Problema que atiende:** ' + dict(AR.CONTEXTO)['Problema'],
    'El sistema **calcula, ordena y compara**; nunca selecciona, descarta ni contrata automáticamente. La decisión final '
    'de selección es **humana**: la registra el Aprobador / Dirección con confirmación explícita y justificación (RF-23).',
    'Estado: **SOFTWARE IMPLEMENTADO** (plataforma v1.1, etiqueta v1.1.0-academic), salvo el componente experimental '
    'CMP-17. El AS-IS del que parte el análisis es **preliminar** y no está validado por la institución.',
]

ALCANCE = [
    '**Incluido (F9):** ' + dict(AR.CONTEXTO)['Alcance incluido'],
    '**Excluido (F9):** ' + dict(AR.CONTEXTO)['Alcance excluido'],
    '**Entorno:** ' + dict(AR.CONTEXTO)['Entorno'],
    '**Límites:** ' + dict(AR.CONTEXTO)['Límites'],
]

USUARIOS = [f'**{a[0]} {a[1]}:** {a[2]}' for a in U.ACTORES] + [
    'No hay superadministrador ni actores comerciales. Los componentes internos (controladores, servicios, colas, base '
    'de datos) no son actores.',
]

RELACION_RF_CU = [
    '**Línea base funcional:** RF-01 a RF-27 (Formato 06) y casos de uso CU-01 a CU-20 (Formato 08, catálogo aprobado). '
    'Cada componente de la sección 4 indica sus RF y CU. No se añaden ni se renumeran requerimientos ni casos de uso.',
] + [f'**{g[0]}:** {g[1]} → {cmp_ref(g[3])}.' for g in AR.CU_GRUPOS] + [
    '**RF-27** (auditoría) es transversal: su registro ocurre en todas las acciones críticas (CMP-13). CU-21 «Consultar '
    'auditoría» está **DIFERIDO** y no forma parte del catálogo.',
    '**RF-28** (panel operativo descriptivo) es un **candidato NO IMPLEMENTADO**: no es un componente de la arquitectura.',
    '**RF-29** (riesgo operacional del proceso) es **EXPERIMENTAL / PROPUESTO** y está fuera de la línea base: CMP-17.',
    '**RNF académicos:** RNF-01 a RNF-10 (Formato 07), relacionados con las decisiones de la sección 7 y las '
    'restricciones de la sección 8. RNF-A a RNF-D (entre ellos RNF-D, observabilidad) son **propuestas** fuera de la '
    'línea base.',
]

# ------------------------------------------------------------------ 3. Estilo arquitectónico propuesto
ESTILO = {
    'Cliente-Servidor.': [
        '**Característica complementaria (SOFTWARE IMPLEMENTADO).** El cliente es el navegador del usuario, con páginas '
        'React 19 y TypeScript (Tailwind CSS 4 y shadcn/ui). El servidor es la aplicación Laravel 13 (PHP 8.4), que '
        'responde mediante Inertia 3, sin una API REST separada. PostgreSQL 17 y Redis 7 son servicios del lado del '
        'servidor.',
    ],
    'Capas (N-tier).': [
        '**Característica complementaria: separación lógica por capas, no niveles físicos.** Seis capas conceptuales: ' +
        '; '.join(f'{c[0]} ({cmp_ref(c[1])})' for c in AR.CAPAS) + '.',
        'En el código, cada módulo sigue la misma separación: controladores delgados, validación en el servidor (Form '
        'Requests), autorización (Policies), servicios de dominio y modelos Eloquent (cap. 7 §7.2). ' + AR.NOTA_CAPAS,
    ],
    'Microservicios.': [
        '**No adoptado.** El sistema **no** es una arquitectura de microservicios: los módulos de negocio comparten una '
        'sola aplicación, un solo despliegue y una sola base de datos.',
        'La única pieza separada técnicamente es el servicio de inferencia de CMP-17 (Python y FastAPI, fuera de Docker '
        'Compose). Es **EXPERIMENTAL**, opcional y está desactivado por defecto (`ML_SERVICE_ENABLED=false`); sin él la '
        'aplicación funciona igual. Esa separación no convierte al sistema en microservicios.',
    ],
    'Monolítico.': [
        '**Estilo principal adoptado: MONOLITO MODULAR (SOFTWARE IMPLEMENTADO).** Una sola aplicación Laravel '
        'organizada por dominios: requerimientos, vacantes, postulantes, postulaciones, evaluaciones, ranking, '
        'selección, notificaciones y auditoría (cap. 7 §7.2).',
    ],
    'Otros.': [
        'No se adopta otro estilo. Como patrón transversal se aplica la **multitenencia lógica**: `organization_id` en '
        'las entidades de negocio, un scope global (`OrganizationScope`) y Policies que comprueban el rol y la '
        'organización (cap. 7 §7.3). **PostgreSQL RLS no está implementado**: queda como recomendación de defensa en '
        'profundidad.',
    ],
    'Justificación.': [
        '• Un solo despliegue, simple y reproducible con Docker Compose, suficiente para el alcance del proyecto: '
        'desarrollo, demostración y pruebas, sin infraestructura productiva (F9, OUT-09; A-36).',
        '• Módulos por dominio con trazabilidad RF → código → pruebas (DA-01). RNF-09 (mantenibilidad) tiene evidencia '
        'parcial.',
        '• Una única base PostgreSQL hace transaccionales las reglas críticas: una decisión por vacante, un seleccionado '
        'por vacante y la auditoría de solo inserción. Así no hace falta coordinación distribuida.',
        '• Ningún requisito aprobado pide despliegues independientes por módulo. Los microservicios añadirían red, '
        'despliegues y consistencia distribuida sin necesidad.',
        '• No se atribuyen mejoras medidas de rendimiento, disponibilidad ni escalabilidad: RNF-06 y RNF-07 están '
        '**NO VERIFICADOS**. Fuentes: cap. 7 §7.2; F9 §10.1; decisión DA-01.',
    ],
}

# ------------------------------------------------------------------ 4. Identificación de componentes


def componentes():
    rows = []
    for c in AR.COMPONENTES:
        rows.append((f'{CMP[c[0]]}\n({c[0]})', f'**{c[1]}**\n{ESTADO_COMPONENTE[c[7]]}', c[3],
                     f'RF: {", ".join(c[4])}\nCU: {c[5]}\nActores: {c[6]}'))
    return rows


NOTA_COMPONENTES = [
    '**Equivalencia de identificadores:**',
    '• CMP-01 a CMP-17 son los identificadores del Formato 11 oficial.',
    '• Entre paréntesis va el identificador histórico C01 a C17, que usan el F11 adaptado, `COMPONENTS.md`, '
    '`RELATIONSHIPS.md` y el diagrama ARQ-01.',
    '• La equivalencia es uno a uno (de CMP-01 = C01 a CMP-17 = C17), sin combinar, dividir ni añadir componentes.',
    'Son 17 componentes **conceptuales**: agrupan responsabilidades, no son clases ni carpetas.',
    '**No son componentes:** ' + '; '.join(f'{x[1]} ({x[2]})' for x in AR.EXCLUIDOS) + '.',
]

# ------------------------------------------------------------------ 5. Relación entre componentes


def relaciones():
    rows = []
    for r in AR.RELACIONES:
        desc = f'**{r[0]}.** {r[4]}. Dependencia: {r[5]}.'
        if r[7]:
            desc += f' {r[7].rstrip(".")}.'
        desc += f' ({r[6]})'
        rows.append((cmp_ref(r[1]), cmp_ref(r[2]), r[3], desc))
    return rows


NOTA_RELACIONES = [
    'Cada relación conserva su identificador histórico **R-01 a R-20** (`RELATIONSHIPS.md` y ARQ-01). Una relación que '
    'une un componente con varios (por ejemplo, R-03 o R-16) es la **misma interacción** con cada uno: no se desdobló ni '
    'se añadió ninguna relación.',
    'No hay dependencias circulares entre los módulos de negocio: CMP-07 no depende de otro, y CMP-08 y CMP-11 dependen '
    'de CMP-07. CMP-17 (RF-29) solo se relaciona con CMP-05 y CMP-01; **no** con CMP-09, CMP-10 ni CMP-11.',
]

# ------------------------------------------------------------------ 6. Diagrama
FIGURA_1 = ('Figura 1. Arquitectura conceptual del sistema: vista formal ARQ-01 de PowerDesigner (F29, con el hotfix '
            'F29B), exportación `ARQ-01_Arquitectura_Conceptual.png`. Los bloques conservan los identificadores '
            'históricos C01 a C17 (CMP-xx = Cxx, sección 4), y las flechas, las relaciones R-01 a R-20 (sección 5).')
DIAGRAMA_NOTA = ('Las seis agrupaciones del diagrama son las capas conceptuales de la sección 3. Las figuras 2 y 3 '
                 'amplían las dos mitades de la figura 1 para leerla mejor. Son recortes sin retoque de la misma '
                 'exportación y no añaden contenido.')
FIGURA_2 = 'Figura 2. Ampliación de la figura 1 (franja del 0 % al 55 % del ancho). Recorte sin retoque de la exportación.'
FIGURA_3 = ('Figura 3. Ampliación de la figura 1 (franja del 45 % al 100 % del ancho), con C17 (CMP-17, experimental) y '
            'las notas del diagrama. Recorte sin retoque de la exportación.')

# ------------------------------------------------------------------ 7. Decisiones de diseño
# id, decisión, estado, justificación, evidencia. Los ID DA-01 a DA-10 son los del F11 adaptado; DA-11 consolida una
# decisión ya aplicada (Docker Compose) que la plantilla oficial pide registrar.
DECISIONES = [
    ('DA-01', 'Monolito modular en lugar de microservicios', 'ADOPTADA · IMPLEMENTADA',
     'Un solo despliegue, con módulos por dominio y trazabilidad RF → código; ningún requisito pide despliegues '
     'independientes', 'cap. 7 §7.2; F9 §10.1'),
    ('DA-10', 'Laravel 13 + React 19 comunicados por Inertia 3', 'ADOPTADA · IMPLEMENTADA',
     'Interfaz de página única servida por el monolito, sin API REST separada; validación y autorización en el servidor',
     'cap. 7 §7.1–7.2'),
    ('DA-08', 'PostgreSQL 17 como único almacén de negocio', 'IMPLEMENTADA',
     'Restricciones de integridad reales (CHECK, UNIQUE, índice único parcial) y el mismo motor en las pruebas',
     'cap. 7 §7.5; A-03'),
    ('DA-09', 'Redis 7 para sesiones, caché y cola', 'IMPLEMENTADA',
     'Las notificaciones se encolan y se envían después del commit, sin bloquear la operación',
     'cap. 7 §7.6; A-32'),
    ('DA-02', 'Multitenencia lógica con organization_id, scopes y Laravel Policies (rol y organización)',
     'IMPLEMENTADA · RLS PROPUESTA, no implementada',
     'Aislar organizaciones en la capa de aplicación; un identificador ajeno responde 403 o 404 sin efectos',
     'cap. 7 §7.3–7.4; A-04; CrossTenantAccessTest; E2E-11'),
    ('DA-05', 'CV en almacenamiento privado', 'IMPLEMENTADA',
     'Disco privado con nombre UUID y descarga solo a través de la Policy; minimiza la exposición de datos del postulante',
     'A-12; A-15'),
    ('DA-04', 'Auditoría transversal de solo inserción', 'IMPLEMENTADA',
     'Trazabilidad no alterable de las acciones críticas: AuditLogger y trigger `audit_logs_append_only`, sin secretos '
     'en los metadatos', 'cap. 7 §7.7; A-33; A-34; DEF-07; DEF-08'),
    ('DA-06', 'Ranking configurable como apoyo a la decisión', 'IMPLEMENTADA',
     '`RankingService` es puro: calcula, ordena y compara, no escribe en la base ni cambia estados',
     'cap. 7 §7.8; A-23 a A-27; RF-21, RF-22'),
    ('DA-03', 'Decisión final humana', 'ADOPTADA · IMPLEMENTADA',
     'Solo el Aprobador / Dirección la registra (VacancyPolicy::decide), con confirmación y justificación; es única por '
     'vacante y no cambia estados por sí misma', 'ADR-002; RF-23; A-27; cap. 7 §7.8'),
    ('DA-07', 'Componente de riesgo operacional (RF-29) separado de la selección', 'EXPERIMENTAL',
     'El ML solo describe el proceso, nunca evalúa personas; no usa PII, no modifica el ranking ni decide; opcional y '
     'desactivado por defecto', 'ADR-001; ADR-004; F9 OUT-04 y OUT-11'),
    ('DA-11', 'Docker Compose como entorno reproducible', 'ADOPTADA · IMPLEMENTADA (desarrollo, demostración y pruebas)',
     'El mismo entorno (app, queue, postgres, redis y perfil e2e) en cualquier equipo; no es una configuración '
     'productiva', 'cap. 7 §7.9; cap. 10; A-36; docs/docker.md'),
]
NOTA_DECISIONES = ('Estados: **ADOPTADA** (decisión tomada), **IMPLEMENTADA** (presente en el software v1.1), **PROPUESTA** '
                   '(no implementada) y **EXPERIMENTAL** (RF-29). No se atribuyen beneficios medidos. DA-01 a DA-10 '
                   'son las decisiones del F11 adaptado; DA-11 registra una decisión que ya estaba aplicada.')

# ------------------------------------------------------------------ 8. Restricciones y consideraciones
RESTRICCIONES = {
    'Tecnológicas': [
        '**Stack real:**',
        '• Laravel 13 (PHP 8.4) con Fortify;',
        '• React 19 con TypeScript, Inertia 3 y Tailwind CSS 4 (shadcn/ui);',
        '• PostgreSQL 17 y Redis 7;',
        '• Docker Compose.',
        '• Una sola aplicación y una sola base de datos de negocio. La multitenencia es lógica y no hay RLS de PostgreSQL.',
        '• El entorno Docker es de desarrollo, demostración y pruebas. No hay configuración productiva ni en la nube '
        '(A-36; F9 OUT-09).',
        '• El correo usa el driver `log`: no hay proveedor real (OUT-08) ni integraciones externas (OUT-10).',
        '• El servicio de CMP-17 (Python 3.12 y FastAPI) está fuera de Docker Compose, es opcional y experimental.',
        '• Solo datos ficticios.',
    ],
    'De rendimiento': [
        '• **RNF-06 Rendimiento: NO VERIFICADO.** Faltan un SLA, pruebas de carga y un umbral aprobado; la medición de '
        'la F25 fue exploratoria. Este documento **no fija ni garantiza** tiempos de respuesta, concurrencia ni '
        'rendimiento por segundo.',
        '• Decisiones que favorecen el rendimiento, **sin medición**:\n'
        '  – caché y cola en Redis: el envío de notificaciones no bloquea la operación (DA-09);\n'
        '  – restricciones e índices en PostgreSQL (DA-08).',
        '• **RNF-07 Disponibilidad y recuperabilidad: NO VERIFICADO.** No hay SLA ni porcentaje de disponibilidad, y no '
        'se probaron el respaldo ni la restauración.',
        '• **RNF-D Observabilidad:** PROPUESTO, fuera de la línea base.',
    ],
    'De seguridad': [
        '• **Autenticación** (CMP-02): Fortify, con registro, inicio de sesión, 2FA y restablecimiento.',
        '• **Autorización** (CMP-03): 7 Policies, que comprueban rol y organización. La decisión final exige el rol '
        'aprobador (cap. 7 §7.4).',
        '• **Multitenencia:** `organization_id` y `OrganizationScope`. El acceso cruzado se rechaza con 403 o 404, '
        'verificado por `CrossTenantAccessTest` y E2E-11.',
        '• **Validación en el servidor** (Form Requests), protección CSRF y límite de intentos de inicio de sesión (cap. '
        '5 §5.7).',
        '• **CV privados** (CMP-15): nombre UUID y descarga autorizada.',
        '• **Auditoría de solo inserción** (CMP-13), sin contraseñas, tokens ni secretos (DEF-08).',
        '• **Secretos fuera del repositorio:** `.env` y `.env.e2e` no se versionan.',
        '• CMP-17 no usa PII ni identificadores de candidatos.',
        '• Estado en el Formato 07: RNF-01 a RNF-04 están **VERIFICADOS**. No hay auditoría de seguridad externa ni '
        'aprobación institucional.',
    ],
    'De escalabilidad': [
        '• **Consideración arquitectónica, no validada:** no hay pruebas de carga ni mediciones de volumen, y no se '
        'afirma escalabilidad horizontal.',
        '• El monolito modular puede crecer por módulos, y un componente podría separarse en el futuro si un requisito '
        'medido lo justificara. Hoy no hay tal requisito.',
        '• La multitenencia lógica permite varias organizaciones en una misma instancia. Está verificada para el '
        '**aislamiento**, no para el volumen.',
        '• Redis desacopla el envío de notificaciones (cola asíncrona).',
        '• No hay infraestructura productiva ni en la nube (OUT-09).',
    ],
}

# ------------------------------------------------------------------ equivalencias con el F11 adaptado (registro F11-R)
CORRESPONDENCIA = [
    ('1. Datos generales del proyecto', 'Sección 1 «Datos generales»', 'm_common.py (datos del proyecto)',
     'Tabla oficial rellenada; fecha de la regularización'),
    ('2. Descripción general del sistema (propósito, alcance general, usuarios principales, relación con requerimientos '
     'y casos de uso)', 'Secciones 2 «Contexto y alcance» y 3 «Casos de uso»', 'F9 v1.1; F6; F8; m_arch.CONTEXTO y CU_GRUPOS',
     'Redistribuido en las cuatro viñetas oficiales'),
    ('3. Estilo arquitectónico propuesto (cliente-servidor, capas, microservicios, monolítico, otros, justificación)',
     'Secciones 8 «Arquitectura conceptual», «Arquitectura técnica» y 9 «Decisiones» (DA-01)',
     'cap. 7 §7.2–7.3; F9 §10.1; m_arch.TECNICA y CAPAS', 'Una respuesta por opción del formato: monolito modular '
     'adoptado; cliente-servidor y capas como características complementarias; microservicios no adoptado'),
    ('4. Identificación de componentes', 'Secciones 4 «Componentes» y 5 «Responsabilidades»; COMPONENTS.md',
     'm_arch.COMPONENTES', 'CMP-01 a CMP-17 con equivalencia Cxx; columnas oficiales'),
    ('5. Relación entre componentes', 'Secciones 6 «Relaciones» y 7 «Flujo»; RELATIONSHIPS.md', 'm_arch.RELACIONES',
     'R-01 a R-20 en las columnas oficiales, sin cambios de semántica'),
    ('6. Diagrama de Arquitectura conceptual', 'Sección 8, figura ARQ-01', 'powerdesigner/exports/ARQ-01_Arquitectura_Conceptual.png',
     'Misma exportación F29/F29B, en página horizontal, con ampliaciones'),
    ('7. Decisiones de diseño', 'Sección 9 «Decisiones arquitectónicas» (DA-01 a DA-10)', 'm_arch.DECISIONES; cap. 7',
     'Viñetas con estado ADOPTADA, IMPLEMENTADA, PROPUESTA o EXPERIMENTAL; DA-11 (Docker) añadida'),
    ('8. Restricciones y consideraciones (tecnológicas, de rendimiento, de seguridad, de escalabilidad)',
     'Secciones 9 «RNF → decisiones», 11 «Limitaciones» y «Arquitectura técnica»', 'F7; cap. 5 §5.7; cap. 7',
     'Una caja por categoría; RNF-06 y RNF-07 no verificados; sin SLA ni métricas inventadas'),
]
