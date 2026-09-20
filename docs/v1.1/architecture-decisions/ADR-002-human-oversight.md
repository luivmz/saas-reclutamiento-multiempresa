# ADR-002 — Supervisión humana de la decisión

- **Estado:** aceptada (vigente desde v1.0, ratificada para v1.1)
- **Fecha:** 19 de septiembre de 2026
- **Contexto:** Fase 13, planificación de v1.1

## Contexto

La plataforma calcula un ranking de candidatos a partir de evaluaciones ponderadas (RF-20 a RF-22) y registra la selección y el cierre de vacante (RF-23 a RF-25). Existe una tentación permanente —y crecerá con el ML de v1.1— de automatizar el paso del cálculo a la decisión "porque el sistema ya sabe quién es el mejor".

## Decisión

**El sistema nunca selecciona, descarta ni contrata.** La decisión final pertenece al Aprobador/Dirección.

Garantías que v1.1 debe preservar:

1. **El servicio de ranking es puro**: calcula, ordena y compara; no escribe estado ni cambia el resultado de una postulación.
2. **Confirmación humana explícita**: el cambio a seleccionado o no seleccionado exige una acción deliberada de un usuario con el rol autorizado, más una justificación registrada.
3. **Ninguna ruta automática**: ni un evento, ni un *job* en cola, ni un comando programado, ni un servicio nuevo puede producir ese cambio de estado.
4. **Auditoría de solo inserción**: quién decidió, cuándo y con qué justificación queda registrado de forma inalterable.
5. **Separación visual**: el cálculo se presenta como insumo; la decisión, como acto humano con su responsable identificado.
6. **Pruebas que lo demuestran**: la suite incluye casos que verifican que el ranking no altera estados y que la decisión exige autorización.

Toda estimación de ML que v1.1 incorpore se muestra lejos del ranking, de la comparación de candidatos y de la decisión final ([ADR-001](ADR-001-ml-boundary.md)).

## Alternativas consideradas

1. **Selección automática del primer puesto del ranking.** Rechazada: convierte una ponderación configurable en una sentencia, sin responsable humano identificable.
2. **Preselección automática con confirmación posterior.** Rechazada: el sesgo de anclaje hace que la "confirmación" sea nominal; además diluye la responsabilidad.

## Consecuencias

**Positivas:** existe siempre una persona responsable e identificable de cada decisión; el sistema es defendible ante una auditoría académica o real; el ranking puede evolucionar sin que cambie quién decide.

**Negativas:** más pasos manuales para el usuario y menos "automatización" que mostrar. Es el costo correcto.

**Aplicación:** contrato 2 y 3 de `CLAUDE.md`, verificado por la skill `project-guardian` en cada cambio.
