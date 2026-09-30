# Formato 11 — Arquitectura del sistema (oficial, regularizado en F11-R)

> Espejo en Markdown de `F11_Arquitectura_del_Sistema_Colegio_Andino.docx`, generado desde el mismo contenido (`docs/academico/tools/f27b/m_f11r.py` y `f11r.py`) sobre la plantilla oficial `Formato_11_Arquitectura_del_sistema.docx`. El entregable es el DOCX.

## 1. Datos generales del proyecto

| Campo | Valor |
|---|---|
| Nombre del proyecto | Análisis y Diseño de una Plataforma SaaS Multiempresa para la Gestión del Reclutamiento, Evaluación y Selección de Personal – Caso de estudio: Colegio Andino de Huancayo |
| Integrantes del equipo | Coronacion Meza Fredy; Peña Arroyo Anthony; Vila Meza Luis Antonio |
| Módulo / Sistema | Plataforma SaaS multiempresa de reclutamiento, evaluación y selección (línea base RF-01 a RF-27) |
| Docente | Dr. Maglioni Arana Caparachin |
| Fecha | 29/09/2026 |

> **Estado de la información de este formato**
>
> **HECHO VERIFICADO:** comprobado en el repositorio (código, pruebas ejecutadas, documentos versionados).
>
> **AS-IS PRELIMINAR:** reconstrucción del proceso actual hecha por el equipo; **sujeta a validación institucional** (RR. HH. / Administración del Colegio). No es un procedimiento validado por la institución.
>
> **TO-BE PROPUESTO:** proceso mejorado diseñado por el equipo; su adopción en la institución no está validada.
>
> **SOFTWARE IMPLEMENTADO:** comportamiento de la plataforma v1.1 (etiqueta v1.1.0-academic), verificado con pruebas.
>
> **EXPERIMENTAL / PROPUESTO:** RF-28 (candidato, no implementado), RF-29 (experimental, solo sobre el proceso) y RNF-C (propuesta). No forman parte de la línea base RF-01 a RF-27.
>
> Regularización F11-R (29/09/2026): este documento vuelve a presentar sobre la **plantilla oficial del Formato 11** la arquitectura conceptual elaborada en la F28 y formalizada en PowerDesigner en la F29. **No cambia la arquitectura**: los componentes, las relaciones R-01 a R-20 y el diagrama ARQ-01 son los mismos. El F11 adaptado anterior (hecho cuando la plantilla oficial no estaba disponible) se conserva como versión histórica.
>
> La plataforma **nunca** selecciona, descarta ni contrata automáticamente: el ranking calcula, ordena y compara.
>
> La decisión final de selección es **humana**: la registra el Aprobador / Dirección con confirmación explícita y justificación (RF-23).
>
> Todos los datos de ejemplo son ficticios. No se usan datos personales reales.
>

## 2. Descripción general del sistema

**Propósito del sistema.**

**Sistema:** plataforma web SaaS multiempresa para gestionar el reclutamiento, la evaluación y la selección de personal. Caso de estudio académico: Colegio Andino de Huancayo.
**Propósito:** Gestionar de forma centralizada, trazable y multiempresa el ciclo de reclutamiento, evaluación y selección, con datos aislados por organización y la decisión final reservada a una persona autorizada.
**Problema que atiende:** Proceso de reclutamiento con información distribuida, seguimiento manual, evaluaciones heterogéneas, comunicación manual e indicadores limitados (P1–P5, AS-IS preliminar, F4).
El sistema **calcula, ordena y compara**; nunca selecciona, descarta ni contrata automáticamente. La decisión final de selección es **humana**: la registra el Aprobador / Dirección con confirmación explícita y justificación (RF-23).
Estado: **SOFTWARE IMPLEMENTADO** (plataforma v1.1, etiqueta v1.1.0-academic), salvo el componente experimental CMP-17. El AS-IS del que parte el análisis es **preliminar** y no está validado por la institución.

**Alcance general.**

**Incluido (F9):** IN-01 Requerimientos · IN-02 Vacantes · IN-03 Cuenta y postulación · IN-04 Seguimiento · IN-05 Evaluación y entrevista · IN-06 Comparación y ranking · IN-07 Decisión y cierre · IN-08 Auditoría.
**Excluido (F9):** Facturación, planes y superadministración SaaS (OUT-01 a OUT-03); selección automática por IA o ML (OUT-04); inferencia de idoneidad (OUT-05); banco de talentos (OUT-06); dashboards (OUT-07, RF-28 candidato); proveedores externos definitivos (OUT-08); infraestructura productiva (OUT-09); integraciones externas (OUT-10); uso productivo o decisorio de RF-29 (OUT-11).
**Entorno:** Aplicación web usada desde el navegador. Infraestructura de desarrollo, demostración y pruebas con Docker Compose; no es una plataforma productiva (F9, OUT-09).
**Límites:** Toda lectura y escritura empresarial respeta la organización. El postulante es global y solo ve lo suyo. Los componentes internos (controladores, servicios, colas, base de datos) no son actores.

**Usuarios principales.**

**ACT-01 Área solicitante:** Interno. Registra, envía y corrige requerimientos; recibe la notificación de rechazo.
**ACT-02 Recursos Humanos:** Interno. Valida requerimientos y gestiona vacantes, postulaciones, sesiones, selección y cierre. No toma la decisión final.
**ACT-03 Aprobador / Dirección:** Interno. Aprueba o rechaza requerimientos, consulta la comparación, **registra la decisión final humana** y consulta la auditoría.
**ACT-04 Postulante:** Externo. Gestiona su cuenta, su perfil, su CV y sus postulaciones; recibe convocatorias, avisos y resultados propios.
**ACT-05 Evaluador:** Interno. Registra puntajes, resultado y observaciones de las sesiones que tiene asignadas.
No hay superadministrador ni actores comerciales. Los componentes internos (controladores, servicios, colas, base de datos) no son actores.

**Relación con requerimientos y casos de uso.**

**Línea base funcional:** RF-01 a RF-27 (Formato 06) y casos de uso CU-01 a CU-20 (Formato 08, catálogo aprobado). Cada componente de la sección 4 indica sus RF y CU. No se añaden ni se renumeran requerimientos ni casos de uso.
**Acceso:** CU-07 → CMP-02, CMP-03 (C02, C03).
**Requerimientos:** CU-01, CU-02, CU-03 → CMP-04 (C04).
**Vacantes:** CU-04, CU-05, CU-06 → CMP-05 (C05).
**Postulantes:** CU-08 → CMP-06, CMP-15 (C06, C15).
**Postulaciones:** CU-09, CU-10, CU-11, CU-12 → CMP-07 (C07).
**Evaluaciones y entrevistas:** CU-13, CU-14, CU-15 → CMP-08 (C08).
**Ranking:** CU-16, CU-17 → CMP-09 (C09).
**Decisión:** CU-18 «Registrar decisión final humana» → CMP-10 (C10).
**Selección y cierre:** CU-19, CU-20 → CMP-11 (C11).
**Notificaciones:** Incluidas en CU-03, CU-09, CU-11, CU-12, CU-13, CU-14 y CU-20 → CMP-12 (C12).
**Auditoría:** RF-27 transversal (CU-21 «Consultar auditoría»: DIFERIDO, fuera del catálogo) → CMP-13 (C13).
**RF-27** (auditoría) es transversal: su registro ocurre en todas las acciones críticas (CMP-13). CU-21 «Consultar auditoría» está **DIFERIDO** y no forma parte del catálogo.
**RF-28** (panel operativo descriptivo) es un **candidato NO IMPLEMENTADO**: no es un componente de la arquitectura.
**RF-29** (riesgo operacional del proceso) es **EXPERIMENTAL / PROPUESTO** y está fuera de la línea base: CMP-17.
**RNF académicos:** RNF-01 a RNF-10 (Formato 07), relacionados con las decisiones de la sección 7 y las restricciones de la sección 8. RNF-A a RNF-D (entre ellos RNF-D, observabilidad) son **propuestas** fuera de la línea base.

## 3. Estilo arquitectónico propuesto

**Cliente-Servidor.**

**Característica complementaria (SOFTWARE IMPLEMENTADO).** El cliente es el navegador del usuario, con páginas React 19 y TypeScript (Tailwind CSS 4 y shadcn/ui). El servidor es la aplicación Laravel 13 (PHP 8.4), que responde mediante Inertia 3, sin una API REST separada. PostgreSQL 17 y Redis 7 son servicios del lado del servidor.

**Capas (N-tier).**

**Característica complementaria: separación lógica por capas, no niveles físicos.** Seis capas conceptuales: Presentación (CMP-01 (C01)); Acceso y seguridad (CMP-02, CMP-03 (C02, C03)); Negocio (CMP-04, CMP-05, CMP-06, CMP-07, CMP-08, CMP-09, CMP-10, CMP-11 (C04, C05, C06, C07, C08, C09, C10, C11)); Servicios transversales (CMP-12, CMP-13 (C12, C13)); Persistencia e infraestructura (CMP-14, CMP-15, CMP-16 (C14, C15, C16)); Experimental (opcional, fuera de la línea base) (CMP-17 (C17)).
En el código, cada módulo sigue la misma separación: controladores delgados, validación en el servidor (Form Requests), autorización (Policies), servicios de dominio y modelos Eloquent (cap. 7 §7.2). Organización conceptual para leer la arquitectura. No es una arquitectura física obligatoria ni un despliegue: el despliegue real está en DE-01 (F23).

**Microservicios.**

**No adoptado.** El sistema **no** es una arquitectura de microservicios: los módulos de negocio comparten una sola aplicación, un solo despliegue y una sola base de datos.
La única pieza separada técnicamente es el servicio de inferencia de CMP-17 (Python y FastAPI, fuera de Docker Compose). Es **EXPERIMENTAL**, opcional y está desactivado por defecto (`ML_SERVICE_ENABLED=false`); sin él la aplicación funciona igual. Esa separación no convierte al sistema en microservicios.

**Monolítico.**

**Estilo principal adoptado: MONOLITO MODULAR (SOFTWARE IMPLEMENTADO).** Una sola aplicación Laravel organizada por dominios: requerimientos, vacantes, postulantes, postulaciones, evaluaciones, ranking, selección, notificaciones y auditoría (cap. 7 §7.2).

**Otros.**

No se adopta otro estilo. Como patrón transversal se aplica la **multitenencia lógica**: `organization_id` en las entidades de negocio, un scope global (`OrganizationScope`) y Policies que comprueban el rol y la organización (cap. 7 §7.3). **PostgreSQL RLS no está implementado**: queda como recomendación de defensa en profundidad.

**Justificación.**

• Un solo despliegue, simple y reproducible con Docker Compose, suficiente para el alcance del proyecto: desarrollo, demostración y pruebas, sin infraestructura productiva (F9, OUT-09; A-36).
• Módulos por dominio con trazabilidad RF → código → pruebas (DA-01). RNF-09 (mantenibilidad) tiene evidencia parcial.
• Una única base PostgreSQL hace transaccionales las reglas críticas: una decisión por vacante, un seleccionado por vacante y la auditoría de solo inserción. Así no hace falta coordinación distribuida.
• Ningún requisito aprobado pide despliegues independientes por módulo. Los microservicios añadirían red, despliegues y consistencia distribuida sin necesidad.
• No se atribuyen mejoras medidas de rendimiento, disponibilidad ni escalabilidad: RNF-06 y RNF-07 están **NO VERIFICADOS**. Fuentes: cap. 7 §7.2; F9 §10.1; decisión DA-01.

## 4. Identificación de componentes

| ID | Componente | Descripción | Funcionalidades asociadas |
|---|---|---|---|
| CMP-01<br>(C01) | **Interfaz web**<br>SOFTWARE IMPLEMENTADO | Páginas por rol, portal público de empleos y notificaciones propias; presenta datos y envía acciones. No decide. | RF: RF-01..RF-27 (interacción)<br>CU: Todos (interfaz)<br>Actores: Todos |
| CMP-02<br>(C02) | **Autenticación y cuentas**<br>SOFTWARE IMPLEMENTADO | Registro del postulante, inicio de sesión, 2FA y restablecimiento; identifica al usuario y su rol. | RF: RF-08<br>CU: CU-07<br>Actores: Postulante; personal |
| CMP-03<br>(C03) | **Autorización y contexto multiempresa**<br>SOFTWARE IMPLEMENTADO (transversal) | Autoriza cada operación por rol **y** organización y filtra los datos por `organization_id`. No hay gestión de organizaciones: la organización es un contexto de aislamiento. | RF: RNF (seguridad y multitenencia); aplica a RF-01..RF-27<br>CU: Todos (transversal)<br>Actores: Todo el personal |
| CMP-04<br>(C04) | **Requerimientos de personal**<br>SOFTWARE IMPLEMENTADO | Registro, envío, validación u observación, corrección y aprobación o rechazo del requerimiento, con historial. | RF: RF-01, RF-02, RF-03, RF-04<br>CU: CU-01, CU-02, CU-03<br>Actores: Área solicitante, RR. HH., Aprobador / Dirección |
| CMP-05<br>(C05) | **Vacantes y convocatorias**<br>SOFTWARE IMPLEMENTADO | Crea la vacante desde un requerimiento aprobado, registra perfil y criterios ponderados, valida la configuración y publica en el portal. | RF: RF-05, RF-06, RF-07, RF-20<br>CU: CU-04, CU-05, CU-06, CU-16<br>Actores: RR. HH. |
| CMP-06<br>(C06) | **Postulantes y CV**<br>SOFTWARE IMPLEMENTADO | Perfil mínimo del postulante (sin DNI ni fecha de nacimiento) y carga del CV en PDF privado. | RF: RF-09<br>CU: CU-08<br>Actores: Postulante |
| CMP-07<br>(C07) | **Postulaciones y etapas**<br>SOFTWARE IMPLEMENTADO | Registro único de postulación, confirmación, revisión del expediente, preselección o descarte y cambios de etapa con historial. | RF: RF-10, RF-11, RF-12, RF-13, RF-14, RF-15<br>CU: CU-09, CU-10, CU-11, CU-12<br>Actores: Postulante, RR. HH., Aprobador / Dirección (consulta) |
| CMP-08<br>(C08) | **Evaluaciones y entrevistas**<br>SOFTWARE IMPLEMENTADO | Programación de sesiones con evaluador de la organización, convocatoria y registro único de puntajes, resultado y observaciones, validados contra rangos. | RF: RF-16, RF-17, RF-18, RF-19, RF-20<br>CU: CU-13, CU-14, CU-15, CU-16<br>Actores: RR. HH., Evaluador |
| CMP-09<br>(C09) | **Ranking y comparación**<br>SOFTWARE IMPLEMENTADO | Calcula un ranking ponderado, determinista y explicable y presenta la comparación. **Es apoyo: no selecciona, no descarta ni cambia estados.** | RF: RF-20, RF-21, RF-22<br>CU: CU-16, CU-17<br>Actores: RR. HH., Aprobador / Dirección |
| CMP-10<br>(C10) | **Decisión final humana**<br>SOFTWARE IMPLEMENTADO | Registra la decisión del **Aprobador / Dirección** con confirmación explícita y justificación; única e inmutable por vacante. No cambia estados por sí misma. | RF: RF-23<br>CU: CU-18<br>Actores: Aprobador / Dirección |
| CMP-11<br>(C11) | **Selección y cierre**<br>SOFTWARE IMPLEMENTADO | Aplica la decisión registrando la selección y cierra la convocatoria (solo con selección); dispara el resultado a cada postulante. | RF: RF-24, RF-25, RF-26<br>CU: CU-19, CU-20<br>Actores: RR. HH. |
| CMP-12<br>(C12) | **Notificaciones**<br>SOFTWARE IMPLEMENTADO (transversal) | Avisos automáticos (rechazo, recepción, cambio de etapa, convocatoria, resultado) en la plataforma y por correo con driver `log`; se encolan y se envían después del commit. | RF: RF-04, RF-11, RF-15, RF-17, RF-26<br>CU: Incluidas en CU-03, CU-09, CU-11, CU-12, CU-13, CU-14, CU-20<br>Actores: Postulante, Área solicitante, Evaluador (destinatarios) |
| CMP-13<br>(C13) | **Auditoría**<br>SOFTWARE IMPLEMENTADO (transversal) | Registra de forma de solo inserción cada acción crítica (trigger en la base) y permite al Aprobador / Dirección consultarla. La consulta no es un CU académico (CU-21 diferido). | RF: RF-27<br>CU: Transversal (UC-RF27)<br>Actores: Aprobador / Dirección (consulta) |
| CMP-14<br>(C14) | **Persistencia de datos (PostgreSQL)**<br>SOFTWARE IMPLEMENTADO | Único almacén de datos de negocio, con restricciones de integridad; historiales, notificaciones y auditoría. | RF: Soporte de RF-01..RF-27<br>CU: —<br>Actores: — |
| CMP-15<br>(C15) | **Almacenamiento privado de CV**<br>SOFTWARE IMPLEMENTADO | Guarda los CV en un disco privado con nombre UUID; la descarga solo pasa por la Policy. | RF: RF-09, RF-12<br>CU: CU-08, CU-10<br>Actores: — |
| CMP-16<br>(C16) | **Sesiones, caché y cola (Redis)**<br>SOFTWARE IMPLEMENTADO | Sesiones, caché y cola de trabajos; el trabajador de cola envía las notificaciones. | RF: Soporte de C02 y C12<br>CU: —<br>Actores: — |
| CMP-17<br>(C17) | **Riesgo operacional del proceso (RF-29)**<br>EXPERIMENTAL / PROPUESTO | Estima el riesgo de demora del **proceso** de una vacante con 15 variables operacionales y un servicio de inferencia externo opcional. Información descriptiva. **No evalúa candidatos, no decide, no ordena ni modifica el ranking** y no guarda su resultado. | RF: RF-29 (candidato, experimental)<br>CU: — (fuera del catálogo; UC-RF29)<br>Actores: RR. HH., Aprobador / Dirección (consulta) |

**Equivalencia de identificadores:**
• CMP-01 a CMP-17 son los identificadores del Formato 11 oficial.
• Entre paréntesis va el identificador histórico C01 a C17, que usan el F11 adaptado, `COMPONENTS.md`, `RELATIONSHIPS.md` y el diagrama ARQ-01.
• La equivalencia es uno a uno (de CMP-01 = C01 a CMP-17 = C17), sin combinar, dividir ni añadir componentes.
Son 17 componentes **conceptuales**: agrupan responsabilidades, no son clases ni carpetas.
**No son componentes:** Panel operativo / reportes (NO IMPLEMENTADO (RF-28, candidato)); Gestión de organizaciones / superadministración (FUERA DE ALCANCE (OUT-03)); Facturación, planes y suscripciones (FUERA DE ALCANCE (OUT-01, OUT-02)); Selección automática, banco de talentos, integraciones externas, infraestructura en nube (FUERA DE ALCANCE (OUT-04 a OUT-10)).

## 5. Relación entre componentes

| Componente origen | Componente destino | Tipo de interacción | Descripción |
|---|---|---|---|
| CMP-01 (C01) | CMP-02 (C02) | Solicitud | **R-01.** Credenciales, sesión. Dependencia: C01 depende de C02 para acceder a lo protegido. (RF-08 · CU-07) |
| CMP-02 (C02) | CMP-03 (C03) | Contexto de seguridad | **R-02.** Usuario autenticado, rol y organización. Dependencia: C03 usa la identidad de C02. (Todos) |
| CMP-03 (C03) | CMP-04 a CMP-11, CMP-13 (C04 a C11, C13) | Autorización y filtro | **R-03.** Permiso por rol y organización; datos filtrados por organization_id. Dependencia: Todos los módulos de negocio dependen de C03 antes de operar. El postulante solo ve lo suyo. (RF-01..RF-27) |
| CMP-01 (C01) | CMP-04 a CMP-11, CMP-13 (C04 a C11, C13) | Uso | **R-04.** Acciones del usuario y datos a presentar. Dependencia: C01 invoca los módulos; no decide. Pasa por C03. (CU-01..CU-20) |
| CMP-04 (C04) | CMP-05 (C05) | Flujo de información | **R-05.** Requerimiento aprobado (origen de la vacante y plazas). Dependencia: C05 depende de un requerimiento aprobado. A-08: plazas ≤ aprobadas. (RF-03 → RF-05 · CU-03 → CU-04) |
| CMP-05 (C05) | CMP-07 (C07) | Flujo de información | **R-06.** Vacante publicada y vigente. Dependencia: C07 solo acepta postulaciones a vacantes publicadas. (RF-07 → RF-10 · CU-06 → CU-09) |
| CMP-06 (C06) | CMP-07 (C07) | Flujo de información | **R-07.** Perfil completo y referencia al CV vigente. Dependencia: C07 exige perfil completo y CV (A-11). (RF-09 → RF-10 · CU-08 → CU-09) |
| CMP-08 (C08) | CMP-07 (C07) | Uso | **R-08.** Postulación elegible; avance automático de etapa al programar (A-16). Dependencia: C08 depende de C07. Sin dependencia inversa: no hay ciclo. (RF-14, RF-16, RF-18 · CU-13, CU-14) |
| CMP-08 (C08) | CMP-09 (C09) | Flujo de información | **R-09.** Resultados de sesiones realizadas (puntajes por criterio). Dependencia: C09 lee los resultados de C08. Solo resultados confirmados (A-23). (RF-19 → RF-21 · CU-15 → CU-17) |
| CMP-09 (C09) | CMP-10 (C10) | Apoyo a la decisión | **R-10.** Comparación explicable; instantánea de posición y puntaje. Dependencia: C10 usa C09 solo para mostrar y guardar la instantánea. **El ranking no elige: decide el Aprobador / Dirección**. (RF-22 → RF-23 · CU-17 → CU-18) |
| CMP-10 (C10) | CMP-11 (C11) | Precondición | **R-11.** Decisión humana registrada. Dependencia: C11 requiere una decisión previa. (RF-23 → RF-24 · CU-18 → CU-19) |
| CMP-11 (C11) | CMP-07 (C07) | Uso | **R-12.** Transición a seleccionado y a no seleccionado. Dependencia: C11 usa las transiciones de C07. Sin dependencia inversa. (RF-24, RF-25 · CU-19, CU-20) |
| CMP-04 a CMP-11 (C04 a C11) | CMP-13 (C13) | Registro | **R-13.** Acción crítica (usuario, organización, acción, entidad, fecha). Dependencia: Los módulos registran en C13 en la misma transacción. C13 no invoca a los módulos. (RF-27) |
| CMP-04, CMP-07, CMP-08, CMP-11 (C04, C07, C08, C11) | CMP-12 (C12) | Evento | **R-14.** Rechazo, recepción, cambio de etapa, convocatoria, resultado. Dependencia: Los módulos disparan avisos; C12 no invoca a los módulos. Después del commit. (RF-04, RF-11, RF-15, RF-17, RF-26) |
| CMP-12 (C12) | CMP-16 (C16) | Encolado | **R-15.** Trabajos de notificación. Dependencia: C12 depende de la cola. (RF-04, RF-11, RF-15, RF-17, RF-26) |
| CMP-04 a CMP-13 (C04 a C13) | CMP-14 (C14) | Persistencia | **R-16.** Datos de negocio, historiales, notificaciones y auditoría. Dependencia: Todos dependen de C14. Auditoría protegida por trigger de solo inserción. (RF-01..RF-27) |
| CMP-06, CMP-07 (C06, C07) | CMP-15 (C15) | Almacenamiento | **R-17.** Archivo del CV (escritura; descarga autorizada). Dependencia: C06 y C07 dependen de C15. Descarga solo con Policy (C03). (RF-09, RF-12 · CU-08, CU-10) |
| CMP-02 (C02) | CMP-16 (C16) | Sesión y caché | **R-18.** Sesión del usuario. Dependencia: C02 depende de C16. (RF-08) |
| CMP-05 (C05) | CMP-17 (C17) | Consulta opcional | **R-19.** 15 variables operacionales del proceso de la vacante (sin identificadores ni PII). Dependencia: C17 lee datos de la vacante; ningún módulo depende de C17. Desactivado por defecto; sin C17 la aplicación funciona igual. (RF-29 (experimental)) |
| CMP-17 (C17) | CMP-01 (C01) | Información descriptiva | **R-20.** Riesgo operacional del proceso y su estado. Dependencia: Solo se muestra en la tarjeta experimental de la vacante. **Sin relación con C09, C10 ni C11**. (RF-29) |

Cada relación conserva su identificador histórico **R-01 a R-20** (`RELATIONSHIPS.md` y ARQ-01). Una relación que une un componente con varios (por ejemplo, R-03 o R-16) es la **misma interacción** con cada uno: no se desdobló ni se añadió ninguna relación.
No hay dependencias circulares entre los módulos de negocio: CMP-07 no depende de otro, y CMP-08 y CMP-11 dependen de CMP-07. CMP-17 (RF-29) solo se relaciona con CMP-05 y CMP-01; **no** con CMP-09, CMP-10 ni CMP-11.

## 6. Diagrama de Arquitectura conceptual

![Figura 1. Arquitectura conceptual del sistema: vista formal ARQ-01 de PowerDesigner (F29, con el hotfix F29B), exportación `ARQ-01_Arquitectura_Conceptual.png`. Los bloques conservan los identificadores históricos C01 a C17 (CMP-xx = Cxx, sección 4), y las flechas, las relaciones R-01 a R-20 (sección 5).](../powerdesigner/exports/ARQ-01_Arquitectura_Conceptual.png)

*Figura 1. Arquitectura conceptual del sistema: vista formal ARQ-01 de PowerDesigner (F29, con el hotfix F29B), exportación `ARQ-01_Arquitectura_Conceptual.png`. Los bloques conservan los identificadores históricos C01 a C17 (CMP-xx = Cxx, sección 4), y las flechas, las relaciones R-01 a R-20 (sección 5).*

Las seis agrupaciones del diagrama son las capas conceptuales de la sección 3. Las figuras 2 y 3 amplían las dos mitades de la figura 1 para leerla mejor. Son recortes sin retoque de la misma exportación y no añaden contenido.

*Figura 2. Ampliación de la figura 1 (franja del 0 % al 55 % del ancho). Recorte sin retoque de la exportación.* (en el DOCX)

*Figura 3. Ampliación de la figura 1 (franja del 45 % al 100 % del ancho), con C17 (CMP-17, experimental) y las notas del diagrama. Recorte sin retoque de la exportación.* (en el DOCX)

## 7. Decisiones de diseño

- **DA-01 Monolito modular en lugar de microservicios.** Estado: **ADOPTADA · IMPLEMENTADA**. Un solo despliegue, con módulos por dominio y trazabilidad RF → código; ningún requisito pide despliegues independientes. Evidencia: cap. 7 §7.2; F9 §10.1.
- **DA-10 Laravel 13 + React 19 comunicados por Inertia 3.** Estado: **ADOPTADA · IMPLEMENTADA**. Interfaz de página única servida por el monolito, sin API REST separada; validación y autorización en el servidor. Evidencia: cap. 7 §7.1–7.2.
- **DA-08 PostgreSQL 17 como único almacén de negocio.** Estado: **IMPLEMENTADA**. Restricciones de integridad reales (CHECK, UNIQUE, índice único parcial) y el mismo motor en las pruebas. Evidencia: cap. 7 §7.5; A-03.
- **DA-09 Redis 7 para sesiones, caché y cola.** Estado: **IMPLEMENTADA**. Las notificaciones se encolan y se envían después del commit, sin bloquear la operación. Evidencia: cap. 7 §7.6; A-32.
- **DA-02 Multitenencia lógica con organization_id, scopes y Laravel Policies (rol y organización).** Estado: **IMPLEMENTADA · RLS PROPUESTA, no implementada**. Aislar organizaciones en la capa de aplicación; un identificador ajeno responde 403 o 404 sin efectos. Evidencia: cap. 7 §7.3–7.4; A-04; CrossTenantAccessTest; E2E-11.
- **DA-05 CV en almacenamiento privado.** Estado: **IMPLEMENTADA**. Disco privado con nombre UUID y descarga solo a través de la Policy; minimiza la exposición de datos del postulante. Evidencia: A-12; A-15.
- **DA-04 Auditoría transversal de solo inserción.** Estado: **IMPLEMENTADA**. Trazabilidad no alterable de las acciones críticas: AuditLogger y trigger `audit_logs_append_only`, sin secretos en los metadatos. Evidencia: cap. 7 §7.7; A-33; A-34; DEF-07; DEF-08.
- **DA-06 Ranking configurable como apoyo a la decisión.** Estado: **IMPLEMENTADA**. `RankingService` es puro: calcula, ordena y compara, no escribe en la base ni cambia estados. Evidencia: cap. 7 §7.8; A-23 a A-27; RF-21, RF-22.
- **DA-03 Decisión final humana.** Estado: **ADOPTADA · IMPLEMENTADA**. Solo el Aprobador / Dirección la registra (VacancyPolicy::decide), con confirmación y justificación; es única por vacante y no cambia estados por sí misma. Evidencia: ADR-002; RF-23; A-27; cap. 7 §7.8.
- **DA-07 Componente de riesgo operacional (RF-29) separado de la selección.** Estado: **EXPERIMENTAL**. El ML solo describe el proceso, nunca evalúa personas; no usa PII, no modifica el ranking ni decide; opcional y desactivado por defecto. Evidencia: ADR-001; ADR-004; F9 OUT-04 y OUT-11.
- **DA-11 Docker Compose como entorno reproducible.** Estado: **ADOPTADA · IMPLEMENTADA (desarrollo, demostración y pruebas)**. El mismo entorno (app, queue, postgres, redis y perfil e2e) en cualquier equipo; no es una configuración productiva. Evidencia: cap. 7 §7.9; cap. 10; A-36; docs/docker.md.

Estados: **ADOPTADA** (decisión tomada), **IMPLEMENTADA** (presente en el software v1.1), **PROPUESTA** (no implementada) y **EXPERIMENTAL** (RF-29). No se atribuyen beneficios medidos. DA-01 a DA-10 son las decisiones del F11 adaptado; DA-11 registra una decisión que ya estaba aplicada.

## 8. Restricciones y consideraciones

**Tecnológicas**

**Stack real:**
• Laravel 13 (PHP 8.4) con Fortify;
• React 19 con TypeScript, Inertia 3 y Tailwind CSS 4 (shadcn/ui);
• PostgreSQL 17 y Redis 7;
• Docker Compose.
• Una sola aplicación y una sola base de datos de negocio. La multitenencia es lógica y no hay RLS de PostgreSQL.
• El entorno Docker es de desarrollo, demostración y pruebas. No hay configuración productiva ni en la nube (A-36; F9 OUT-09).
• El correo usa el driver `log`: no hay proveedor real (OUT-08) ni integraciones externas (OUT-10).
• El servicio de CMP-17 (Python 3.12 y FastAPI) está fuera de Docker Compose, es opcional y experimental.
• Solo datos ficticios.

**De rendimiento**

• **RNF-06 Rendimiento: NO VERIFICADO.** Faltan un SLA, pruebas de carga y un umbral aprobado; la medición de la F25 fue exploratoria. Este documento **no fija ni garantiza** tiempos de respuesta, concurrencia ni rendimiento por segundo.
• Decisiones que favorecen el rendimiento, **sin medición**:
  – caché y cola en Redis: el envío de notificaciones no bloquea la operación (DA-09);
  – restricciones e índices en PostgreSQL (DA-08).
• **RNF-07 Disponibilidad y recuperabilidad: NO VERIFICADO.** No hay SLA ni porcentaje de disponibilidad, y no se probaron el respaldo ni la restauración.
• **RNF-D Observabilidad:** PROPUESTO, fuera de la línea base.

**De seguridad**

• **Autenticación** (CMP-02): Fortify, con registro, inicio de sesión, 2FA y restablecimiento.
• **Autorización** (CMP-03): 7 Policies, que comprueban rol y organización. La decisión final exige el rol aprobador (cap. 7 §7.4).
• **Multitenencia:** `organization_id` y `OrganizationScope`. El acceso cruzado se rechaza con 403 o 404, verificado por `CrossTenantAccessTest` y E2E-11.
• **Validación en el servidor** (Form Requests), protección CSRF y límite de intentos de inicio de sesión (cap. 5 §5.7).
• **CV privados** (CMP-15): nombre UUID y descarga autorizada.
• **Auditoría de solo inserción** (CMP-13), sin contraseñas, tokens ni secretos (DEF-08).
• **Secretos fuera del repositorio:** `.env` y `.env.e2e` no se versionan.
• CMP-17 no usa PII ni identificadores de candidatos.
• Estado en el Formato 07: RNF-01 a RNF-04 están **VERIFICADOS**. No hay auditoría de seguridad externa ni aprobación institucional.

**De escalabilidad**

• **Consideración arquitectónica, no validada:** no hay pruebas de carga ni mediciones de volumen, y no se afirma escalabilidad horizontal.
• El monolito modular puede crecer por módulos, y un componente podría separarse en el futuro si un requisito medido lo justificara. Hoy no hay tal requisito.
• La multitenencia lógica permite varias organizaciones en una misma instancia. Está verificada para el **aislamiento**, no para el volumen.
• Redis desacopla el envío de notificaciones (cola asíncrona).
• No hay infraestructura productiva ni en la nube (OUT-09).
