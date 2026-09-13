# Capítulo 4. Requerimientos

## 4.1 Actores

| Actor | Rol en el sistema (`users.role`) | Pertenece a una organización | Responsabilidades principales |
|---|---|---|---|
| Área solicitante | `solicitante` | Sí | Registrar, corregir y enviar requerimientos de personal |
| Recursos Humanos | `rrhh` | Sí | Validar u observar requerimientos, configurar y publicar vacantes, gestionar postulaciones y etapas, programar sesiones, registrar la selección y cerrar |
| Aprobador / Dirección | `aprobador` | Sí | Aprobar o rechazar requerimientos, consultar la comparación, **registrar la decisión final**, consultar la auditoría |
| Evaluador | `evaluador` | Sí | Registrar puntajes, resultado y observaciones de las sesiones que tiene asignadas |
| Postulante | `postulante` | No (cuenta global, A-04) | Crear cuenta, completar perfil y CV, postular, ver sus postulaciones y notificaciones |
| Sistema | — | — | Validar, calcular el ranking, notificar y auditar (nunca selecciona) |

Una restricción `CHECK` en la base de datos garantiza que el postulante no tenga `organization_id` y que el personal sí lo tenga (migración `2026_09_13_000002`). No existe un rol SuperAdmin (A-33).

## 4.2 Requerimientos funcionales (línea base definitiva: RF-01 a RF-27)

La línea base contiene **exactamente 27 RF**. No se agregaron RF adicionales.

| RF | Nombre | Actor principal | Descripción implementada |
|---|---|---|---|
| RF-01 | Registrar requerimiento de personal | Área solicitante | Registro con puesto, área, plazas, tipo de contrato, fecha requerida y justificación |
| RF-02 | Validar y corregir requerimiento | RR. HH. / Área solicitante | RR. HH. valida u observa con comentario; el área corrige y reenvía |
| RF-03 | Registrar aprobación o rechazo | Aprobador / Dirección | Decisión sobre requerimientos validados; el rechazo exige motivo |
| RF-04 | Notificar rechazo | Sistema → Área solicitante | Notificación automática del rechazo con su motivo |
| RF-05 | Registrar perfil y criterios | RR. HH. | Vacante creada desde un requerimiento aprobado, con perfil y criterios (etapa, ponderación, rango) |
| RF-06 | Configurar y validar vacante | RR. HH. | Configuración de la convocatoria y lista de validación previa a la publicación |
| RF-07 | Publicar vacante | RR. HH. | Publicación de vacantes válidas en el portal público de empleos |
| RF-08 | Gestionar cuenta y acceso del postulante | Postulante | Registro e inicio de sesión (Fortify) con rol postulante |
| RF-09 | Gestionar perfil y CV | Postulante | Perfil profesional y CV en PDF (máx. 5 MB) almacenado de forma privada |
| RF-10 | Registrar postulación | Postulante | Postulación única por vacante publicada y vigente, con perfil completo y CV |
| RF-11 | Confirmar postulación | Sistema → Postulante | Código de seguimiento y notificación de recepción |
| RF-12 | Consultar y revisar postulaciones | RR. HH. | Listado por vacante y expediente con datos, CV e historial |
| RF-13 | Registrar preselección o descarte | RR. HH. | Preselección, o descarte con motivo interno |
| RF-14 | Gestionar cambio de etapa | RR. HH. | Cambios de etapa según la máquina de estados, con historial |
| RF-15 | Notificar cambio de etapa | Sistema → Postulante | Aviso de cada cambio, sin observaciones internas (A-14) |
| RF-16 | Programar evaluación | RR. HH. | Evaluación con evaluador de la organización, fecha futura, modalidad y lugar |
| RF-17 | Generar convocatoria de evaluación | Sistema → Postulante y Evaluador | Convocatoria automática con fecha, modalidad, lugar e indicaciones |
| RF-18 | Programar entrevista | RR. HH. | Entrevista con evaluador asignado y convocatoria |
| RF-19 | Registrar entrevista y resultado | Evaluador | Puntajes por criterio, resultado y observaciones; una sola vez |
| RF-20 | Validar rangos y ponderaciones | Sistema (configurado por RR. HH.) | Ponderaciones válidas (suma configurable, por defecto 100) y puntajes dentro del rango |
| RF-21 | Calcular ranking configurable | Sistema | Ranking ponderado, determinista y explicable, con empates y candidatos incompletos |
| RF-22 | Presentar comparación de candidatos | RR. HH., Aprobador / Dirección | Comparación con criterios, promedios, aportes, total y posición |
| RF-23 | Registrar decisión final de selección | **Aprobador / Dirección** | **Decisión humana** con confirmación explícita y justificación; puede no ser el primero del ranking |
| RF-24 | Registrar selección del candidato | RR. HH. | Aplica la decisión: la postulación elegida pasa a `seleccionado` |
| RF-25 | Cerrar vacante o convocatoria | RR. HH. | Cierre con selección; las demás postulaciones activas pasan a `no_seleccionado` |
| RF-26 | Notificar resultado y cierre | Sistema → Postulantes | Resultado propio para cada postulante, solo al cerrar |
| RF-27 | Generar registro de auditoría | Sistema; consulta: Aprobador / Dirección | Registro de solo inserción de acciones críticas y vista segura de consulta |

Trazabilidad a código, pruebas y evidencia: [traceability-master.md](traceability-master.md).

## 4.3 Requerimientos no funcionales

Solo se incluyen RNF respaldados por la implementación o por los supuestos documentados. **No se definieron SLA ni métricas de rendimiento**, y no se ejecutaron pruebas de carga.

| RNF | Categoría (ISO/IEC 25010) | Requerimiento | Evidencia |
|---|---|---|---|
| RNF-01 | Seguridad: autenticación | Acceso autenticado, contraseñas con *hash* bcrypt y límite de 5 intentos de inicio de sesión por minuto | Laravel Fortify, `FortifyServiceProvider`, `AuthenticationTest` |
| RNF-02 | Seguridad: autorización | Autorización en el servidor por rol y organización en cada operación | `app/Policies/*`, middleware `role`, `RoleMiddlewareTest` |
| RNF-03 | Seguridad: aislamiento multiempresa | Una organización nunca accede a datos de otra | `BelongsToOrganization` + `OrganizationScope`, `CrossTenantAccessTest`, `OrganizationScopeTest`, E2E-11 |
| RNF-04 | Seguridad: integridad | Validación en el servidor (Form Requests), protección CSRF y restricciones de base de datos | `app/Http/Requests/*`, *middleware* web de Laravel, restricciones `CHECK`, `UNIQUE` y FK en las migraciones |
| RNF-05 | Seguridad: responsabilidad | Auditoría de solo inserción de acciones críticas, sin datos sensibles | `AuditLogger`, trigger `audit_logs_append_only`, `AuditTrailTest` |
| RNF-06 | Privacidad | Minimización de datos (sin DNI ni fecha de nacimiento, A-15); CV en disco privado con nombre UUID y descarga autorizada | `CandidateDocumentPolicy`, `CandidateProfileTest` |
| RNF-07 | Usabilidad | Interfaz en español, navegación por rol, estados vacíos, mensajes de error y éxito, y diseño adaptable (móvil, tableta y escritorio) | `docs/manual-smoke-test.md` (recorrido visual 10/10) |
| RNF-08 | Mantenibilidad | Monolito modular por dominio, servicios y *enums* con máquinas de estado, pruebas automatizadas | Estructura `app/`, 244 pruebas PHPUnit |
| RNF-09 | Portabilidad | Ejecución completa con Docker sin dependencias locales, e instalación desde cero documentada | `docker-compose.yml`, `docs/docker.md` (validación en clon limpio) |
| RNF-10 | Trazabilidad funcional | Historial de estados y trazabilidad RF → código → prueba | Historiales de requerimiento y postulación, `traceability-master.md` |
| RNF-11 | Adecuación (localización) | Fechas y horas en `America/Lima` en servidor y cliente | `APP_TIMEZONE`, `AppTimezoneTest`, DEF-09 |

## 4.4 Casos de uso

El documento de casos de uso validado previamente por el equipo (práctica de casos de uso) **no está en el repositorio**. El catálogo siguiente se deriva de la línea base y de la implementación, y debe contrastarse con ese entregable al armar el informe.

| CU | Caso de uso | Actor | RF |
|---|---|---|---|
| CU-01 | Gestionar requerimiento de personal | Área solicitante | RF-01, RF-02 |
| CU-02 | Validar requerimiento | RR. HH. | RF-02 |
| CU-03 | Aprobar o rechazar requerimiento | Aprobador / Dirección | RF-03, RF-04 |
| CU-04 | Configurar y publicar vacante | RR. HH. | RF-05, RF-06, RF-07, RF-20 |
| CU-05 | Registrarse y gestionar perfil/CV | Postulante | RF-08, RF-09 |
| CU-06 | Postular a una vacante | Postulante | RF-10, RF-11 |
| CU-07 | Revisar postulaciones y gestionar etapas | RR. HH. | RF-12, RF-13, RF-14, RF-15 |
| CU-08 | Programar evaluación o entrevista | RR. HH. | RF-16, RF-17, RF-18 |
| CU-09 | Registrar resultados de evaluación/entrevista | Evaluador | RF-19, RF-20 |
| CU-10 | Consultar ranking y comparación | RR. HH., Aprobador / Dirección | RF-21, RF-22 |
| CU-11 | Registrar decisión final | Aprobador / Dirección | RF-23 |
| CU-12 | Registrar selección y cerrar convocatoria | RR. HH. | RF-24, RF-25, RF-26 |
| CU-13 | Consultar auditoría | Aprobador / Dirección | RF-27 |

Los diagramas de secuencia UML disponibles (PowerDesigner) cubren CU-06, CU-09 y CU-11/CU-12. Su correspondencia con la implementación se analiza en el [capítulo 6](06-diseno-sistema.md).

## 4.5 Reglas de negocio críticas

1. **El sistema no selecciona automáticamente.** El ranking es apoyo; la decisión final la registra el Aprobador/Dirección (A-27).
2. Registrar la decisión final no cambia por sí solo el estado de ninguna postulación (A-27).
3. El candidato elegido puede no ser el primero del ranking; la decisión requiere confirmación explícita y justificación (A-27).
4. Tras la decisión, RR. HH. no puede preseleccionar, descartar ni cambiar etapas en esa vacante (A-28).
5. Las postulaciones activas restantes pasan a `no_seleccionado` solo al cerrar (A-30).
6. RF-25 implementa únicamente el cierre con selección (A-30).

El detalle de los 36 supuestos está en `docs/assumptions.md`.
