# Relaciones entre componentes (F11)

Generado desde `m_arch.py`. «C04 a C11» significa cada componente de ese rango. Las flechas del borrador llevan estos IDs.

| ID | Origen | Destino | Tipo de relación | Información intercambiada | Dependencia | RF/CU relacionados | Observación |
|---|---|---|---|---|---|---|---|
| R-01 | C01 | C02 | Solicitud | Credenciales, sesión | C01 depende de C02 para acceder a lo protegido | RF-08 · CU-07 |  |
| R-02 | C02 | C03 | Contexto de seguridad | Usuario autenticado, rol y organización | C03 usa la identidad de C02 | Todos |  |
| R-03 | C03 | C04 a C11, C13 | Autorización y filtro | Permiso por rol y organización; datos filtrados por organization_id | Todos los módulos de negocio dependen de C03 antes de operar | RF-01..RF-27 | El postulante solo ve lo suyo |
| R-04 | C01 | C04 a C11, C13 | Uso | Acciones del usuario y datos a presentar | C01 invoca los módulos; no decide | CU-01..CU-20 | Pasa por C03 |
| R-05 | C04 | C05 | Flujo de información | Requerimiento aprobado (origen de la vacante y plazas) | C05 depende de un requerimiento aprobado | RF-03 → RF-05 · CU-03 → CU-04 | A-08: plazas ≤ aprobadas |
| R-06 | C05 | C07 | Flujo de información | Vacante publicada y vigente | C07 solo acepta postulaciones a vacantes publicadas | RF-07 → RF-10 · CU-06 → CU-09 |  |
| R-07 | C06 | C07 | Flujo de información | Perfil completo y referencia al CV vigente | C07 exige perfil completo y CV (A-11) | RF-09 → RF-10 · CU-08 → CU-09 |  |
| R-08 | C08 | C07 | Uso | Postulación elegible; avance automático de etapa al programar (A-16) | C08 depende de C07 | RF-14, RF-16, RF-18 · CU-13, CU-14 | Sin dependencia inversa: no hay ciclo |
| R-09 | C08 | C09 | Flujo de información | Resultados de sesiones realizadas (puntajes por criterio) | C09 lee los resultados de C08 | RF-19 → RF-21 · CU-15 → CU-17 | Solo resultados confirmados (A-23) |
| R-10 | C09 | C10 | Apoyo a la decisión | Comparación explicable; instantánea de posición y puntaje | C10 usa C09 solo para mostrar y guardar la instantánea | RF-22 → RF-23 · CU-17 → CU-18 | **El ranking no elige: decide el Aprobador / Dirección** |
| R-11 | C10 | C11 | Precondición | Decisión humana registrada | C11 requiere una decisión previa | RF-23 → RF-24 · CU-18 → CU-19 |  |
| R-12 | C11 | C07 | Uso | Transición a seleccionado y a no seleccionado | C11 usa las transiciones de C07 | RF-24, RF-25 · CU-19, CU-20 | Sin dependencia inversa |
| R-13 | C04 a C11 | C13 | Registro | Acción crítica (usuario, organización, acción, entidad, fecha) | Los módulos registran en C13 en la misma transacción | RF-27 | C13 no invoca a los módulos |
| R-14 | C04, C07, C08, C11 | C12 | Evento | Rechazo, recepción, cambio de etapa, convocatoria, resultado | Los módulos disparan avisos; C12 no invoca a los módulos | RF-04, RF-11, RF-15, RF-17, RF-26 | Después del commit |
| R-15 | C12 | C16 | Encolado | Trabajos de notificación | C12 depende de la cola | RF-04, RF-11, RF-15, RF-17, RF-26 |  |
| R-16 | C04 a C13 | C14 | Persistencia | Datos de negocio, historiales, notificaciones y auditoría | Todos dependen de C14 | RF-01..RF-27 | Auditoría protegida por trigger de solo inserción |
| R-17 | C06, C07 | C15 | Almacenamiento | Archivo del CV (escritura; descarga autorizada) | C06 y C07 dependen de C15 | RF-09, RF-12 · CU-08, CU-10 | Descarga solo con Policy (C03) |
| R-18 | C02 | C16 | Sesión y caché | Sesión del usuario | C02 depende de C16 | RF-08 |  |
| R-19 | C05 | C17 | Consulta opcional | 15 variables operacionales del proceso de la vacante (sin identificadores ni PII) | C17 lee datos de la vacante; ningún módulo depende de C17 | RF-29 (experimental) | Desactivado por defecto; sin C17 la aplicación funciona igual |
| R-20 | C17 | C01 | Información descriptiva | Riesgo operacional del proceso y su estado | Solo se muestra en la tarjeta experimental de la vacante | RF-29 | **Sin relación con C09, C10 ni C11** |

## Flujo de información

1. El usuario se autentica (C02). El postulante crea una cuenta global; el personal entra con su rol.
2. C03 establece el contexto: rol y organización. Toda consulta y operación posterior queda filtrada y autorizada.
3. El **Área solicitante** registra el requerimiento y **RR. HH.** lo valida u observa (C04).
4. El **Aprobador / Dirección** aprueba o rechaza el requerimiento (C04); el rechazo se notifica (C12).
5. RR. HH. crea la vacante desde el requerimiento aprobado, configura criterios y publica (C05).
6. El postulante completa su perfil y su CV (C06, C15) y postula (C07); recibe la confirmación (C12).
7. RR. HH. revisa, preselecciona o descarta y gestiona las etapas (C07); cada cambio se notifica (C12).
8. RR. HH. programa evaluaciones y entrevistas; el **Evaluador** registra los resultados (C08).
9. El ranking calcula y presenta la comparación como **apoyo** (C09).
10. El **Aprobador / Dirección** registra la **decisión final humana** con confirmación y justificación (C10).
11. RR. HH. registra la selección y cierra la convocatoria (C11); cada postulante recibe su resultado (C12).
12. Durante todo el proceso, cada acción crítica queda en la auditoría (C13), persistida en C14.
13. Las notificaciones se encolan en C16 y se entregan al destinatario (C12).

Precisión respecto del esquema del encargo: el requerimiento lo **registra el Área solicitante** (RF-01) y RR. HH. lo valida (RF-02); evaluaciones y entrevistas las registra el mismo rol **Evaluador** (RF-19).

### Flujo separado de RF-29 (experimental)

1. Solo si el servicio está habilitado (`ML_SERVICE_ENABLED=true`) y la vacante es elegible.
2. C17 arma 15 variables operacionales del proceso de la vacante: conteos y días; sin identificadores, PII ni texto libre.
3. C17 consulta el servicio de inferencia externo experimental.
4. El resultado (riesgo del proceso y estado) se muestra en C01 como información descriptiva y no se guarda.
5. Sin servicio o con respuesta inválida, el estado es «no disponible» o «solo descriptivo» y el proceso sigue igual. **Este flujo no toca el ranking, la decisión ni la selección.**
