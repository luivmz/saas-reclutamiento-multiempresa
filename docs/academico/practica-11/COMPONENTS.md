# Componentes de la arquitectura conceptual (F11)

Generado desde `docs/academico/tools/f27b/m_arch.py`. Estados: IMPLEMENTADO · TRANSVERSAL · EXPERIMENTAL · PROPUESTO · NO IMPLEMENTADO.

| ID | Componente | Responsabilidad | RF asociados | CU asociados | Actores | Estado | Fuente |
|---|---|---|---|---|---|---|---|
| C01 | Interfaz web | Páginas por rol, portal público de empleos y notificaciones propias; presenta datos y envía acciones. No decide. | RF-01..RF-27 (interacción) | Todos (interfaz) | Todos | IMPLEMENTADO | CO-01 «Páginas Inertia», «Componentes compartidos»; resources/js/pages |
| C02 | Autenticación y cuentas | Registro del postulante, inicio de sesión, 2FA y restablecimiento; identifica al usuario y su rol. | RF-08 | CU-07 | Postulante; personal | IMPLEMENTADO | CO-01 «Cuenta y acceso» (Fortify) |
| C03 | Autorización y contexto multiempresa | Autoriza cada operación por rol **y** organización y filtra los datos por `organization_id`. No hay gestión de organizaciones: la organización es un contexto de aislamiento. | RNF (seguridad y multitenencia); aplica a RF-01..RF-27 | Todos (transversal) | Todo el personal | TRANSVERSAL | CO-01 «Autorización y multiempresa» (7 Policies, OrganizationScope); cap. 7 §7.3 |
| C04 | Requerimientos de personal | Registro, envío, validación u observación, corrección y aprobación o rechazo del requerimiento, con historial. | RF-01, RF-02, RF-03, RF-04 | CU-01, CU-02, CU-03 | Área solicitante, RR. HH., Aprobador / Dirección | IMPLEMENTADO | PK-01 «Requerimientos» |
| C05 | Vacantes y convocatorias | Crea la vacante desde un requerimiento aprobado, registra perfil y criterios ponderados, valida la configuración y publica en el portal. | RF-05, RF-06, RF-07, RF-20 | CU-04, CU-05, CU-06, CU-16 | RR. HH. | IMPLEMENTADO | PK-01 «Vacantes» |
| C06 | Postulantes y CV | Perfil mínimo del postulante (sin DNI ni fecha de nacimiento) y carga del CV en PDF privado. | RF-09 | CU-08 | Postulante | IMPLEMENTADO | PK-01 «Postulantes» |
| C07 | Postulaciones y etapas | Registro único de postulación, confirmación, revisión del expediente, preselección o descarte y cambios de etapa con historial. | RF-10, RF-11, RF-12, RF-13, RF-14, RF-15 | CU-09, CU-10, CU-11, CU-12 | Postulante, RR. HH., Aprobador / Dirección (consulta) | IMPLEMENTADO | PK-01 «Postulaciones» y «Postulantes» (ApplicationService) |
| C08 | Evaluaciones y entrevistas | Programación de sesiones con evaluador de la organización, convocatoria y registro único de puntajes, resultado y observaciones, validados contra rangos. | RF-16, RF-17, RF-18, RF-19, RF-20 | CU-13, CU-14, CU-15, CU-16 | RR. HH., Evaluador | IMPLEMENTADO | PK-01 «Evaluaciones» (evaluaciones y entrevistas en un solo módulo) |
| C09 | Ranking y comparación | Calcula un ranking ponderado, determinista y explicable y presenta la comparación. **Es apoyo: no selecciona, no descarta ni cambia estados.** | RF-20, RF-21, RF-22 | CU-16, CU-17 | RR. HH., Aprobador / Dirección | IMPLEMENTADO | CO-01 «Cálculo de ranking»; PK-01 «Ranking y selección» |
| C10 | Decisión final humana | Registra la decisión del **Aprobador / Dirección** con confirmación explícita y justificación; única e inmutable por vacante. No cambia estados por sí misma. | RF-23 | CU-18 | Aprobador / Dirección | IMPLEMENTADO | CO-01 FinalDecisionService; SEQ-07; ADR-002 |
| C11 | Selección y cierre | Aplica la decisión registrando la selección y cierra la convocatoria (solo con selección); dispara el resultado a cada postulante. | RF-24, RF-25, RF-26 | CU-19, CU-20 | RR. HH. | IMPLEMENTADO | PK-01 «Ranking y selección» |
| C12 | Notificaciones | Avisos automáticos (rechazo, recepción, cambio de etapa, convocatoria, resultado) en la plataforma y por correo con driver `log`; se encolan y se envían después del commit. | RF-04, RF-11, RF-15, RF-17, RF-26 | Incluidas en CU-03, CU-09, CU-11, CU-12, CU-13, CU-14, CU-20 | Postulante, Área solicitante, Evaluador (destinatarios) | TRANSVERSAL | CO-01 «Notificaciones» |
| C13 | Auditoría | Registra de forma de solo inserción cada acción crítica (trigger en la base) y permite al Aprobador / Dirección consultarla. La consulta no es un CU académico (CU-21 diferido). | RF-27 | Transversal (UC-RF27) | Aprobador / Dirección (consulta) | TRANSVERSAL | CO-01 «Auditoría»; A-33, A-34 |
| C14 | Persistencia de datos (PostgreSQL) | Único almacén de datos de negocio, con restricciones de integridad; historiales, notificaciones y auditoría. | Soporte de RF-01..RF-27 | — | — | IMPLEMENTADO | CO-01 «PostgreSQL 17»; cap. 7 §7.5 |
| C15 | Almacenamiento privado de CV | Guarda los CV en un disco privado con nombre UUID; la descarga solo pasa por la Policy. | RF-09, RF-12 | CU-08, CU-10 | — | IMPLEMENTADO | CO-01 «Almacenamiento de CV»; A-12 |
| C16 | Sesiones, caché y cola (Redis) | Sesiones, caché y cola de trabajos; el trabajador de cola envía las notificaciones. | Soporte de C02 y C12 | — | — | IMPLEMENTADO | CO-01 «Redis 7», «Trabajador de cola»; cap. 7 §7.6 |
| C17 | Riesgo operacional del proceso (RF-29) | Estima el riesgo de demora del **proceso** de una vacante con 15 variables operacionales y un servicio de inferencia externo opcional. Información descriptiva. **No evalúa candidatos, no decide, no ordena ni modifica el ranking** y no guarda su resultado. | RF-29 (candidato, experimental) | — (fuera del catálogo; UC-RF29) | RR. HH., Aprobador / Dirección (consulta) | EXPERIMENTAL | CO-01 «Riesgo operacional» y «Servicio de inferencia»; SEQ-08; ADR-001; ADR-004 |

## Elementos no incluidos como componentes

| ID | Elemento | Estado | Motivo |
|---|---|---|---|
| X-01 | Panel operativo / reportes | NO IMPLEMENTADO (RF-28, candidato) | RF-28 es un panel descriptivo candidato; no tiene rutas, pantallas ni pruebas. No es un componente de la arquitectura. La página «panel» existente es solo la portada por rol de C01. |
| X-02 | Gestión de organizaciones / superadministración | FUERA DE ALCANCE (OUT-03) | No hay actores ni CU de gestión comercial global. Las organizaciones solo definen el contexto de aislamiento (C03). |
| X-03 | Facturación, planes y suscripciones | FUERA DE ALCANCE (OUT-01, OUT-02) | Sin requerimiento aprobado. |
| X-04 | Selección automática, banco de talentos, integraciones externas, infraestructura en nube | FUERA DE ALCANCE (OUT-04 a OUT-10) | Contradicen RF-23 o no están en la línea base. |

## Capas conceptuales

| Capa | Componentes |
|---|---|
| Presentación | C01 |
| Acceso y seguridad | C02, C03 |
| Negocio | C04, C05, C06, C07, C08, C09, C10, C11 |
| Servicios transversales | C12, C13 |
| Persistencia e infraestructura | C14, C15, C16 |
| Experimental (opcional, fuera de la línea base) | C17 |

Organización conceptual para leer la arquitectura. No es una arquitectura física obligatoria ni un despliegue: el despliegue real está en DE-01 (F23).
