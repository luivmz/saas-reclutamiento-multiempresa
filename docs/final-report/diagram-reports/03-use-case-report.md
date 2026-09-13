# Informe del diagrama de casos de uso

## 1. Propósito

Mostrar qué funciones ofrece el sistema a cada actor y delimitar el alcance funcional frente a la línea base RF-01 a RF-27.

**Disponibilidad:**
- El diagrama y la especificación de casos de uso validados previamente por el equipo (práctica de casos de uso) **no están versionados en el repositorio**.
- En la carpeta del curso no hay un diagrama de casos de uso: los archivos `.oom` de `Diagramas/PD` contienen diagramas de secuencia y de despliegue.

Este informe describe por escrito el catálogo derivado de la línea base ([capítulo 4, sección 4.4](../04-requerimientos.md#44-casos-de-uso)). No es un diagrama nuevo.

## 2. Elementos principales

**Actores** (coinciden con los roles reales de `users.role`):

| Actor | Rol |
|---|---|
| Área solicitante | `solicitante` |
| Recursos Humanos | `rrhh` |
| Aprobador / Dirección | `aprobador` |
| Evaluador | `evaluador` |
| Postulante | `postulante` |

No existe SuperAdmin ni hay actores comerciales (facturación, planes).

**Casos de uso:**

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

Los RF-04, RF-11, RF-15, RF-17, RF-26 y RF-27 (registro) los ejecuta el sistema como efecto de otros casos de uso: son relaciones de inclusión, no casos iniciados por un actor.

## 3. Relación con requerimientos

Los 27 RF aparecen en al menos un caso de uso, sin RF adicionales. Ver [traceability-master.md](../traceability-master.md).

## 4. Relación con implementación

| CU | Rutas y controladores reales | Páginas |
|---|---|---|
| CU-01, CU-02, CU-03 | `requerimientos` (`JobRequestController`), `requerimientos/{id}/enviar\|observar\|validar\|decision` (`JobRequestTransitionController`) | `job-requests/*` |
| CU-04 | `vacantes` (`VacancyController`), `vacantes/{id}/publicar` | `vacancies/*` |
| CU-05 | Fortify (`register`, `login`), `mi-perfil`, `mi-perfil/cv` | `auth/*`, `candidate/profile` |
| CU-06 | `empleos`, `empleos/{id}/postular` | `jobs/*`, `candidate/applications/*` |
| CU-07 | `vacantes/{id}/postulaciones`, `postulaciones/{id}`, `postulaciones/{id}/preseleccionar\|descartar\|etapa` | `applications/*` |
| CU-08 | `postulaciones/{id}/evaluaciones\|entrevistas` | `applications/show` |
| CU-09 | `mis-evaluaciones`, `evaluaciones/{id}/resultados`, `entrevistas/{id}/resultados` | `assessments/*` |
| CU-10, CU-11, CU-12 | `vacantes/{id}/comparacion\|decision\|seleccion\|cerrar` | `selection/comparison` |
| CU-13 | `auditoria` | `audit/index` |

La autorización por actor se aplica con Policies y el middleware `role`, verificada en PHPUnit (`RoleMiddlewareTest` y pruebas «solo X puede…») y en E2E-01 y E2E-12.

## 5. Consistencias

- Los cinco actores coinciden con los roles implementados y con la restricción `CHECK` de `users`.
- Cada caso de uso tiene rutas, páginas y pruebas reales.
- La decisión final (CU-11) pertenece exclusivamente al Aprobador/Dirección, igual que en el código (`VacancyPolicy::decide`).

## 6. Diferencias detectadas

No pueden compararse con el diagrama o la especificación originales porque no están en el repositorio. Posibles diferencias a revisar al anexarlos:
- nombres o agrupación de los casos;
- si el original asignaba la decisión final a RR. HH. (la implementación la asigna al Aprobador/Dirección);
- casos fuera de la línea base (p. ej., cierre sin selección).

## 7. Limitaciones

Catálogo derivado; el diagrama y la especificación originales no están disponibles.

## 8. Estado para entrega

**Vigente con observaciones**, como catálogo escrito derivado de la línea base. El diagrama original es **evidencia externa pendiente**.

## 9. Recomendación

1. Anexar el diagrama de casos de uso original y contrastarlo con esta tabla.
2. Si el original difiere en la decisión final o en casos fuera de la línea base, anotar que la versión vigente es la de RF-01 a RF-27 y las pruebas automatizadas.
