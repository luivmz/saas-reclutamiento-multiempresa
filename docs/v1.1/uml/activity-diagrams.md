# AC-01 y AC-02 · Diagramas de actividad

## AC-01 · Proceso de reclutamiento de extremo a extremo

| | |
|---|---|
| **Objetivo** | Mostrar el proceso completo, con sus decisiones y el responsable de cada actividad |
| **Alcance** | Desde el requerimiento hasta el cierre y la notificación del resultado. Una vacante, su requerimiento y sus postulaciones |
| **Fuente de verdad** | Enums de estado (`allowedTransitions()`), servicios de cada módulo, Policies, `docs/assumptions.md` (A-28, A-30) |
| **Borrador textual** | [`puml/ac-01-recruitment.puml`](puml/ac-01-recruitment.puml) |
| **RF** | RF-01 a RF-27 |

**Particiones (*swimlanes*)**: Área solicitante · Recursos Humanos · Aprobador / Dirección · Postulante · Evaluador · Sistema.

### Flujo

| # | Partición | Actividad o decisión | RF |
|---|---|---|---|
| 1 | Área solicitante | Registrar requerimiento (`borrador`) y enviarlo (`enviado`) | RF-01 |
| 2 | RR. HH. | ◇ ¿Requerimiento correcto? — **No**: observar con comentario (`observado`) → el solicitante corrige y reenvía (vuelve a 1). **Sí**: validar (`validado`) | RF-02 |
| 3 | Aprobador | ◇ ¿Aprobar? — **No**: rechazar con motivo (`rechazado`) → Sistema notifica al solicitante → **fin** | RF-03, RF-04 |
| 4 | RR. HH. | Crear la vacante desde el requerimiento aprobado: datos, perfil del puesto, criterios con etapa, ponderación y rango, plazo objetivo opcional | RF-05, RF-06 |
| 5 | Sistema | Validar configuración, rangos y ponderaciones; ◇ si no es válida, RR. HH. corrige (vuelve a 4) | RF-06, RF-20 |
| 6 | RR. HH. | Publicar (`publicada`); la vacante aparece en `/empleos` | RF-07 |
| 7 | Postulante | Crear cuenta, completar perfil y cargar CV en PDF | RF-08, RF-09 |
| 8 | Postulante | Postular. ◇ Vacante abierta, perfil completo, CV y sin postulación previa → **Sí**: postulación `postulado`; **No**: error y fin para ese intento | RF-10 |
| 9 | Sistema | Confirmar la postulación al postulante | RF-11 |
| 10 | RR. HH. | Revisar postulaciones. ◇ Preseleccionar o descartar (con comentario) | RF-12, RF-13 |
| 11 | Sistema | Notificar el cambio de etapa | RF-15 |
| 12 | RR. HH. | Programar evaluación y/o entrevista con un evaluador de la organización; la postulación avanza a `en_evaluacion` / `en_entrevista` | RF-16, RF-18 |
| 13 | Sistema | Enviar la convocatoria al postulante y el aviso al evaluador | RF-17 |
| 14 | Evaluador | Registrar puntajes por criterio (y resultado de la entrevista); el sistema valida los rangos | RF-19, RF-20 |
| 15 | RR. HH. | Gestionar etapas hasta `finalista` o `descartado`, con notificación en cada cambio | RF-14, RF-15 |
| 16 | RR. HH. o Aprobador | Consultar la comparación; el sistema calcula el ranking en ese momento | RF-21, RF-22 |
| 17 | **Aprobador** | **◇ Decisión humana**: elegir un finalista con resultados completos, justificar y confirmar. Puede no ser el primero | **RF-23** |
| 18 | RR. HH. | Registrar la selección: la elegida pasa a `seleccionado` | RF-24 |
| 19 | RR. HH. | Cerrar la convocatoria (`cerrada`, `con_seleccion`): las demás postulaciones activas pasan a `no_seleccionado` | RF-25 |
| 20 | Sistema | Notificar el resultado a la seleccionada y a las no seleccionadas | RF-26 |
| — | Sistema | **Transversal**: auditar cada acción crítica (nota, no una actividad en cada paso) | RF-27 |

### Reglas que el diagrama debe mostrar

- **Paralelismo**: el Postulante (7–9) actúa desde que la vacante está publicada, en paralelo con la revisión de RR. HH.; la postulación es por postulante. Se dibuja con la vacante publicada como punto de sincronización, no como bifurcación del sistema.
- **Bucles reales**: observación y corrección del requerimiento (2 → 1); reconfiguración de la vacante (5 → 4); varias evaluaciones o entrevistas por postulación (12–14).
- **Bloqueos**: después de 17, RR. HH. ya no cambia etapas en esa vacante (A-28). Tras 19 no se admiten postulaciones, sesiones ni resultados.
- **No implementado**: cierre `desierta` (sin selección, A-30). No se dibuja como camino del proceso; como mucho, nota.
- **Sin ML en este proceso**: el riesgo operacional no forma parte del flujo de decisión (AC-02 es aparte).

## AC-02 · Consulta del riesgo operacional `<<experimental>>`

| | |
|---|---|
| **Objetivo** | Mostrar cuándo se estima el riesgo del proceso y cuándo no, y qué ve el usuario en cada caso |
| **Alcance** | Una consulta de la tarjeta de riesgo de una vacante |
| **Fuente de verdad** | `OperationalRiskService::outOfScopeReason`, `MlRiskClient::predict`, `RiskAvailability`, `operational-risk-card.tsx` |
| **Borrador textual** | [`puml/ac-02-operational-risk.puml`](puml/ac-02-operational-risk.puml) |
| **RF** | RF-29 |

### Flujo

1. RR. HH. o Aprobador de la organización abre el detalle de la vacante; la tarjeta pide la estimación.
2. ◇ **Elegibilidad**, en este orden (el primero que falle decide): vacante publicada → tiene `closes_at` → tiene `target_completion_at` → ya pasó el *checkpoint* (día siguiente a `closes_at`) → no está cerrada → el plazo es posterior al *checkpoint* → la consulta no es posterior al plazo. Si falla alguno → **`descriptive_only`** con su motivo.
3. Construir las 15 features **en el *checkpoint***, no en el momento de la consulta.
4. ◇ ¿Integración habilitada? **No** → `descriptive_only` (`service_disabled`).
5. Enviar las features al servicio de inferencia.
6. ◇ ¿Respuesta válida y compatible con el contrato congelado? **No** → **`unavailable`** con su motivo.
7. **Sí** → **`predictive_available`**: porcentaje de `risk_score` y señal de `risk_flag`.
8. Mostrar la tarjeta: etiqueta «Experimental», mensaje explicativo y aviso de que la decisión es humana.

**Fin sin efectos**: no se guarda nada, no cambia ninguna postulación ni el ranking, no hay notificación. No hay ninguna rama hacia selección o descarte: **no es una actividad de selección**.

## Instrucciones para F23

1. *Activity Diagram* «AC-01 Proceso de reclutamiento AS-IS» con las seis particiones y los nodos de decisión de la tabla; nota transversal de auditoría.
2. *Activity Diagram* «AC-02 Riesgo operacional (experimental)» con los tres desenlaces nombrados como los valores reales de `RiskAvailability`.
3. Marcar la actividad 17 con `<<human decision>>` y AC-02 con `<<experimental>>`.
