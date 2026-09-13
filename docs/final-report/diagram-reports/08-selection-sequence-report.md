# Informe del diagrama de secuencia de selección y cierre

## 1. Propósito

Representar la selección del candidato y el cierre de la convocatoria.

**Artefacto original:** `Diagramas/PD/seleccionl_3.oom` (PowerDesigner, carpeta del curso, fuera del repositorio). **No se modificó.**

## 2. Elementos principales

**Líneas de vida del diagrama original:** RR. HH. (actor), React, Laravel, Policy, PostgreSQL.

**Mensajes del diagrama original, en un único flujo iniciado por RR. HH.:**
1. Seleccionar candidato finalista → Solicitar selección de candidato → Consultar resultados y ranking → Retornar resultados del candidato → Mostrar información de selección.
2. Confirmar selección del candidato → Enviar solicitud de selección → Validar permisos de selección → Usuario autorizado.
3. Verificar estado de convocatoria → Retornar estado de convocatoria.
4. Registrar candidato seleccionado → Actualizar estado de postulación → **Cerrar convocatoria** → Confirmar cambios.
5. Registrar evento de auditoría → Confirmar auditoría → Confirmar selección y cierre → Mostrar confirmación.

## 3. Relación con requerimientos

- RF-21 (ranking)
- RF-22 (comparación)
- RF-23 (decisión final)
- RF-24 (registrar selección)
- RF-25 (cierre)
- RF-26 (notificación de resultado)
- RF-27 (auditoría)

## 4. Relación con implementación: flujo vigente

La implementación final separa el proceso en **cinco pasos con responsables distintos**. Cada paso tiene su propia ruta, Policy, servicio y pruebas.

| # | Paso | Actor | Entrada | Validaciones | Servicio | Persistencia | Notificación / auditoría |
|---|---|---|---|---|---|---|---|
| 1 | **Ranking** (RF-21) | Sistema | Resultados realizados de la vacante | Configuración de ponderaciones y rangos válida (RF-20); solo postulaciones de la vacante y de la organización | `VacancyRankingBuilder` + `RankingService` (puro) | **Ninguna**: no escribe ni cambia estados | — |
| 2 | **Comparación** (RF-22) | RR. HH. o Aprobador/Dirección | `GET /vacantes/{id}/comparacion` | `VacancyPolicy::viewRanking` (rol y organización) | `VacancyComparisonController`, `RankingPresenter` | Ninguna | — |
| 3 | **Decisión humana** (RF-23) | **Aprobador/Dirección** | `POST /vacantes/{id}/decision` con postulación elegida, justificación y confirmación explícita | `VacancyPolicy::decide` (solo aprobador de la organización); `FinalDecisionRequest` (confirmación humana, justificación ≥ 20 caracteres); finalista con resultados completos; una sola decisión; vacante no cerrada. **Puede no ser el primero del ranking** | `FinalDecisionService` | `selection_decisions` (posición y puntaje al decidir). **No cambia estados** | Auditoría `seleccion.decision_registrada` |
| 4 | **Registro de selección** (RF-24) | RR. HH. | `POST /vacantes/{id}/seleccion` | `VacancyPolicy::registerSelection`; exige decisión registrada; no repetible | `SelectionRegistrationService` | Postulación elegida `finalista → seleccionado` (índice único parcial) + historial | Auditoría `seleccion.candidato_registrado` |
| 5 | **Cierre** (RF-25, RF-26) | RR. HH. | `POST /vacantes/{id}/cerrar` | `VacancyPolicy::close`; exige selección registrada (cierre sin selección no implementado, A-30); bloqueo de fila | `VacancyClosureService` | Vacante `cerrada` (`con_seleccion`); postulaciones activas restantes → `no_seleccionado` | `ProcessResultNotification` a cada postulante afectado (tras el *commit*); auditoría `vacante.cerrada` y `proceso.resultado_notificado` |

**Pruebas que representan el comportamiento vigente:**
- **PHPUnit:**
  - `RankingServiceTest`
  - `RankingComparisonTest`, incluido `test_rf23_calculating_the_ranking_never_selects_a_candidate`
  - `FinalDecisionTest` (10), incluidos `test_rf23_approver_may_choose_a_candidate_who_is_not_first_in_the_ranking` y `test_rf23_only_the_approver_can_record_the_decision`
  - `SelectionRegistrationTest` (7)
  - `VacancyClosureTest` (5)
  - `ProcessResultNotificationTest` (8)
- **Cypress:** E2E-08 (ranking sin selección), E2E-09 (decisión humana eligiendo al 2.º), E2E-10 (selección, cierre y notificación), E2E-12 (decisión no autorizada, selección tras el cierre) y E2E-13.

## 5. Consistencias

- Participantes (React, Laravel, Policy, PostgreSQL) y existencia de la consulta de resultados y ranking.
- Validación de permisos antes de modificar.
- Verificación del estado de la convocatoria.
- Actualización del estado de la postulación a seleccionado.
- Cierre de la convocatoria.
- Registro de auditoría.

## 6. Diferencias detectadas

1. **Actor de la decisión.** El diagrama preliminar muestra a **RR. HH. seleccionando directamente** al candidato. En la implementación, **la decisión final pertenece al Aprobador/Dirección** (RF-23, A-27). RR. HH. no puede registrarla (`test_rf23_only_the_approver_can_record_the_decision`, E2E-12).
2. **Pasos fusionados.** El diagrama resuelve selección, actualización de estado y cierre en **una sola transacción**. La implementación los separa en decisión (sin cambio de estado), registro de la selección y cierre, con validaciones propias en cada paso.
3. **Decisión humana explícita.** El diagrama no muestra la confirmación humana ni la justificación obligatorias, ni la posibilidad de elegir a alguien que no sea el primero del ranking.
4. **Ranking como apoyo.** El diagrama no deja explícito que calcular el ranking no selecciona a nadie.
5. **Notificación de resultado.** El diagrama no incluye la notificación de resultado (RF-26), que en la implementación se envía solo al cerrar.
6. **Postulaciones no elegidas.** El diagrama no muestra el paso de las demás postulaciones activas a `no_seleccionado`.

## 7. Limitaciones

- El artefacto está fuera del repositorio.
- Es una versión anterior a la definición de las reglas aprobadas en la Fase 6 (decisión humana del Aprobador, separación selección/cierre).
- El nombre del objeto interno es genérico (`ObjectOrientedModel_3`).

## 8. Estado para entrega

**Preliminar / pendiente de actualización gráfica.**

El comportamiento vigente es el de **RF-21 a RF-25** (más RF-26 y RF-27) y el de las **pruebas automatizadas** citadas en la sección 4, no el diagrama preliminar.

## 9. Recomendación

1. No presentar este diagrama como representación del flujo final sin una nota que remita a este informe.
2. En una futura versión gráfica:
   - separar los cinco pasos;
   - asignar la decisión final al Aprobador/Dirección, con confirmación y justificación;
   - mostrar que el ranking no cambia estados;
   - incluir la notificación de resultado al cerrar;
   - incluir el paso de las demás postulaciones a `no_seleccionado`.
