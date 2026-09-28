# Pendiente de PowerDesigner — F11 arquitectura conceptual (ARQ-01)

**Actualización F29 (27/09/2026): FORMALIZED / DONE**, pendiente de la auditoría F29. Diagrama «ARQ-01 - Arquitectura Conceptual» en [`F29_UML_Academico.oom`](../powerdesigner/models/F29_UML_Academico.oom) (paquete ARQ01); exportaciones [PNG](../powerdesigner/exports/ARQ-01_Arquitectura_Conceptual.png) y [SVG](../powerdesigner/exports/ARQ-01_Arquitectura_Conceptual.svg); verificación en [`F29_VALIDATION.md`](../powerdesigner/F29_VALIDATION.md). El estado anterior se conserva a continuación.

**Estado: READY FOR POWERDESIGNER, condicionado a la auditoría de la F28.** Se modela en la **Fase 29**. En la F28 no se abrió PowerDesigner ni se modificó ningún `.oom`, `.pdm` o exportación de la F23.

Esta especificación permite construir la vista sin reinterpretar nada: si algo no está aquí, no se dibuja.

## Qué debe modelarse

**Nombre:** «ARQ-01 — Arquitectura conceptual del sistema».

- **Qué tipo de vista es:** conceptual, de bloques. Va en un paquete propio del OOM, por ejemplo «Arquitectura conceptual (F11 adaptado)», o en un modelo aparte.
- **Qué no es:** no sustituye a CO-01 (componentes técnicos), PK-01 (paquetes) ni DE-01 (despliegue), y no los edita.
- **Tipo de diagrama sugerido:** diagrama de componentes UML usado a nivel conceptual. Cada bloque es un componente con estereotipo `<<conceptual>>` y los grupos son paquetes o marcos.

## Bloques (17) y agrupaciones (6)

| Agrupación | Bloques (ID y nombre exacto) | Estereotipo adicional |
|---|---|---|
| Capa de presentación | C01 Interfaz web | — |
| Capa de acceso y seguridad | C02 Autenticación y cuentas · C03 Autorización y contexto multiempresa | C03: `<<transversal>>` |
| Capa de negocio | C04 Requerimientos de personal · C05 Vacantes y convocatorias · C06 Postulantes y CV · C07 Postulaciones y etapas · C08 Evaluaciones y entrevistas · C09 Ranking y comparación · C10 Decisión final humana · C11 Selección y cierre | C10: `<<human decision>>` · C09: `<<apoyo>>` |
| Servicios transversales | C12 Notificaciones · C13 Auditoría | `<<transversal>>` |
| Persistencia e infraestructura | C14 Persistencia de datos (PostgreSQL) · C15 Almacenamiento privado de CV · C16 Sesiones, caché y cola (Redis) | `<<infraestructura>>` |
| Experimental (opcional) | C17 Riesgo operacional del proceso (RF-29) | `<<experimental>>`, borde discontinuo |

**Actores**, fuera del marco del sistema: Área solicitante, Recursos Humanos, Aprobador / Dirección, Evaluador y Postulante. Se dibujan como un solo grupo que se relaciona con C01.

## Relaciones (dirección de la flecha = dependencia o flujo, como en RELATIONSHIPS.md)

| ID | Flecha | Etiqueta |
|---|---|---|
| — | Actores → C01 | usan |
| R-01 | C01 → C02 | credenciales / sesión |
| R-02 | C02 → C03 | identidad, rol, organización |
| R-03 | C03 → marco «Capa de negocio» y C13 | autoriza y filtra por organización |
| R-04 | C01 → marco «Capa de negocio» | uso (a través de C03). Si satura el diagrama, va solo como nota |
| R-05 | C04 → C05 | requerimiento aprobado |
| R-06 | C05 → C07 | vacante publicada |
| R-07 | C06 → C07 | perfil y CV |
| R-08 | C08 → C07 | postulación elegible / avance de etapa |
| R-09 | C08 → C09 | resultados realizados |
| R-10 | C09 → C10 | comparación (apoyo; **no elige**) |
| R-11 | C10 → C11 | decisión humana registrada |
| R-12 | C11 → C07 | transiciones seleccionado / no seleccionado |
| R-13 | marco «Capa de negocio» → C13 | registro de acciones críticas |
| R-14 | marco «Capa de negocio» → C12 | eventos de notificación |
| R-15 | C12 → C16 | encolado |
| R-16 | marco «Capa de negocio» y C13 → C14 | persistencia |
| R-17 | C06 y C07 → C15 | CV (escritura y descarga autorizada) |
| R-18 | C02 → C16 | sesión |
| R-19 | C05 ⇢ C17 (discontinua) | 15 variables operacionales (opcional) |
| R-20 | C17 ⇢ C01 (discontinua) | información descriptiva de riesgo |

## Notas obligatorias

- **En C10:** «Decisión HUMANA (RF-23): la registra el Aprobador / Dirección con confirmación y justificación».
- **En C09:** «Calcula, ordena y compara; no selecciona ni cambia estados».
- **En C17:** «Experimental y opcional (RF-29): solo el proceso; no evalúa personas; sin relación con C09, C10 ni C11; desactivado por defecto».
- **Nota general:** «Arquitectura conceptual (adaptación académica de la Guía 11). No es un despliegue: ver DE-01».

## Qué NO mostrar

- **Elementos fuera de alcance:** servidores, puertos, contenedores, versiones o trabajadores. Van en DE-01.
- **Elementos inexistentes:** clases, controladores o carpetas; facturación, suscripciones, superadministración, banco de talentos, reportes o panel operativo (RF-28 es un candidato no implementado); microservicios, nube o Kubernetes.
- **Relaciones prohibidas:** ninguna relación de C17 con C09, C10 o C11, y ningún bloque «motor de selección».
- **Casos de uso:** CU-21 (diferido) ni ningún caso de uso nuevo.

## Criterio de aceptación

1. **Elementos:** 17 bloques, 6 agrupaciones y relaciones R-01 a R-20, con los mismos IDs y nombres que `COMPONENTS.md` y `RELATIONSHIPS.md`.
2. **Fronteras:** C10 separado de C09 y C17 aislado de la selección.
3. **Modelos existentes:** no se modifica CO-01, PK-01, DE-01 ni ninguna otra vista de la F23.
4. **Exportación:** PNG y SVG, y el borrador del F11 se sustituye solo después de una nueva auditoría.
