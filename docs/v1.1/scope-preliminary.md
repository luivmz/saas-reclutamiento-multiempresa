# Alcance preliminar de v1.1

**Estado: borrador de planificación.** Nada de este documento está aprobado. Sirve para que el equipo decida, no para autorizar trabajo.

> **Actualización del 20 de septiembre de 2026 (Fase 14).** El equipo aprobó doce decisiones sobre el **experimento de ML**, pero **ningún requerimiento**: RF-28 a RF-31 y los RNF **siguen siendo candidatos** y no entran al baseline de v1.1 (decisión 11). Se añadió la brecha `GAP-01` —necesidad de un plazo operacional explícito, aprobada conceptualmente y sin implementar— y cinco RNF candidatos con numeración provisional. Detalle en [`ml/requirements-and-traceability-plan.md`](ml/requirements-and-traceability-plan.md); registro de decisiones en [`phase-14-ml-definition.md` §4](phase-14-ml-definition.md).

> **Estado vigente (23/09/2026, hotfix final de la Fase 21).** Este documento nació en la Fase 13 como fotografía preliminar y se conserva así: sus secciones 1 y 4 describen el repositorio **del 19/09/2026** y se anotan en lugar de reescribirse. Lo que es cierto hoy:
>
> - `main` permanece en la **v1.0 académica** (`4563c69`; tag `v1.0.0-academic` en `9a946c2`) y no contiene v1.1.
> - `develop` (`aced6da`) integra las **Fases 13 a 21**. La Fase 22 (especificación UML del AS-IS) está implementada en `feature/phase-22-uml-update` y pendiente de auditoría; la Fase 23 (PowerDesigner) **no se inició**. *(Actualizado en la Fase 22; hasta entonces decía `a316c07`, Fases 13 a 20 y la Fase 21 pendiente de cierre.)*
> - El **servicio FastAPI existe** (Fase 15) y la **integración Laravel ↔ FastAPI existe** (Fase 16, validada en pruebas en la Fase 17). Ambos son **experimentales**: validados técnicamente con datos sintéticos, no validados institucionalmente ni autorizados para producción.
> - **RF-29** está implementado experimentalmente y **sigue siendo candidato**; **RF-28** sigue siendo candidato; **RNF-C** sigue siendo **propuesta**. Nada de eso cambia RF-23: la decisión final es humana.
>
> El estado por fase se mantiene en [`../PROGRESS.md`](../PROGRESS.md) y en `CLAUDE.md`.

Leyenda:

- **Verificado** — comprobado en el repositorio o en una ejecución real.
- **Propuesta** — idea del equipo, aún sin decisión.
- **Pendiente de decisión** — requiere una decisión explícita antes de cualquier implementación.

## 1. Hechos verificados (línea base de v1.1, fotografía de la Fase 13 al 19/09/2026)

- RF-01 a RF-27 están implementados y trazados; su significado no cambia en v1.1.
- ~~`main` y `develop` contienen el mismo código publicado~~; `v1.0.0-academic` marca el release académico. *Histórico: cierto el 19/09/2026; dejó de serlo al integrar la Fase 13 solo en `develop`. Hoy `main` sigue en v1.0 y `develop` integra F13–F20 (ver «Estado vigente» arriba).*
- Última ejecución registrada de PHPUnit en v1.0: 244 pruebas, 236 aprobadas, 8 omitidas, 0 fallidas. Última ejecución registrada de Cypress: 14 especificaciones, 43 pruebas, 43 aprobadas. **No se reejecutaron en la Fase 13.**
- El entorno es Docker (Laravel 13 / PHP 8.4, PostgreSQL 17, Redis 7) y CI ejecuta la suite en GitHub Actions.
- El sistema no toma ninguna decisión automática sobre personas.

## 2. Candidatos funcionales (RF-28 en adelante)

Numeración **provisional**: estos identificadores solo se fijan cuando el equipo apruebe el requerimiento.

| Candidato | Descripción | Estado | Riesgo principal |
|---|---|---|---|
| RF-28 (cand.) | Panel operativo de seguimiento de convocatorias: etapas, tiempos y cuellos de botella, sin datos de personas | Propuesta | Puede confundirse con evaluación de candidatos si el diseño no es explícito |
| RF-29 (cand.) | Estimación informativa de riesgo de demora de una convocatoria | ~~Pendiente de decisión~~ Implementado e integrado **experimentalmente** (Fases 15–17): validado técnicamente con datos sintéticos, no validado institucionalmente ni autorizado para producción. **Sigue siendo candidato** (decisión 11) | Depende por completo de `ml-feasibility.md`; sin no-go superado, no existe. **Fase 14:** especificado en detalle y ~~**bloqueado** por `ML-DECISION-01` (semántica del plazo objetivo)~~ desbloqueado: `ML-DECISION-01` se resolvió el 20/09/2026 y `GAP-01` se resolvió técnicamente en la Fase 16 |
| RF-30 (cand.) | Exportación de reportes operativos del proceso (PDF/CSV) para el informe académico | Propuesta | Riesgo de incluir datos personales si no se filtra por diseño |
| RF-31 (cand.) | Portal público de vacantes con presentación visual mejorada | Propuesta | Alcance visual que puede desbordar hacia rediseño general |

**Descartado explícitamente:** cualquier requerimiento que puntúe, ordene, recomiende, filtre o descarte postulantes de forma automática. No se numerará ni se discutirá como candidato.

## 3. Candidatos no funcionales

| Candidato | Descripción | Estado |
|---|---|---|
| RNF-A (cand.) | Accesibilidad WCAG 2.1 AA verificada en las pantallas de RF-01 a RF-27 | Propuesta |
| RNF-B (cand.) | Presupuesto de rendimiento del frontend con línea base medida | Propuesta |
| RNF-C (cand.) | Experiencia 3D progresiva en pantallas públicas | ~~Pendiente de decisión~~ Implementada en la Fase 20 por encargo del equipo, sin dependencias nuevas; su promoción formal al baseline sigue pendiente (ver ADR-003) |
| RNF-D (cand.) | Observabilidad del proceso: métricas operativas y registro estructurado | Propuesta |

## 4. Arquitectura propuesta (Fase 13; implementada después en las Fases 15 a 17)

- **Laravel sigue siendo el sistema de registro.** Toda decisión, estado y dato de negocio vive en PostgreSQL bajo el control de Laravel.
- **FastAPI~~, si llega a existir,~~ es un servicio de inferencia opcional y sin estado**: sin acceso a la base principal, sin conocimiento del dominio, sin capacidad de escribir. Laravel funciona completo si el servicio no responde. *El servicio existe desde la Fase 15 y se construyó con estas condiciones.*
- ~~No hay integración Laravel–Python aprobada. No se ha escrito ni un cliente HTTP.~~ *Histórico (Fase 13). La Fase 16 escribió el cliente HTTP (`app/Services/Ml/MlRiskClient.php`) e integró Laravel ↔ FastAPI de forma experimental; la Fase 17 la validó en entorno de pruebas. Detalle en [`phase-16-laravel-ml-integration.md`](phase-16-laravel-ml-integration.md) y [`phase-17-ml-validation.md`](phase-17-ml-validation.md).*

## 5. Advertencia sobre datos

Cualquier dataset que v1.1 utilice será **sintético** y estará rotulado como tal en el archivo, en la documentación y en la interfaz. El proyecto no dispone de datos reales de reclutamiento y **no debe obtenerlos**. Toda conclusión derivada de datos sintéticos es una demostración metodológica, no una medición del mundo real, y así debe presentarse en el informe.

## 6. Riesgos

Se expresa el **riesgo de retraso**, no una duración exacta: el proyecto no tiene base histórica para estimar horas con credibilidad.

| Riesgo | Impacto | Probabilidad | Mitigación |
|---|---|---|---|
| El ML consume el tiempo de los entregables académicos | Alto | Media | Criterios de no-go tempranos; el ML es lo último que se implementa |
| El dataset sintético no es representativo y las métricas engañan | Alto | Media | Línea base honesta, partición temporal, rótulo explícito, no-go si no supera la línea base |
| El 3D degrada el rendimiento o rompe E2E | Medio | Media | Presupuestos de `recruitment-3d-experience`, carga diferida, poster, medición previa |
| Ampliar el alcance rompe la trazabilidad de v1.0 | Alto | Baja | `project-guardian` + `academic-traceability` en cada cambio |
| La accesibilidad se revisa tarde y obliga a rehacer pantallas | Medio | Media | Revisión con `reviewing-a11y` desde el primer cambio de interfaz |
| Dependencias nuevas sin autorización | Medio | Baja | Regla: ninguna dependencia productiva sin aprobación explícita |

## 7. Decisiones pendientes

1. ¿Qué candidatos de la sección 2 se aprueban como requerimientos de v1.1?
2. ¿Se explora el servicio de riesgo operacional o se descarta de entrada?
3. ¿Se autoriza la experiencia 3D y sus dependencias de frontend? — *23/09/2026: la experiencia se encargó e implementó en la Fase 20 **sin dependencias**, así que la parte de dependencias sigue abierta para cualquier 3D futuro con WebGL.*
4. ¿Se autoriza el uso de navegador o red para `reviewing-a11y`?
5. ¿Se autoriza la instalación global de las herramientas oficiales de revisión bloqueadas por licencia?
6. ¿Qué entregables exige la próxima evaluación del curso y con qué fecha?

Ninguna implementación de v1.1 debe comenzar antes de responder 1 y 6.

### Añadidas por la Fase 14

7. ~~`ML-DECISION-01` — fuente y semántica de `target_completion_at`~~ → **Resuelta el 20/09/2026** (decisión 3): `required_by` descartado; plazo explícito aprobado conceptualmente; implementación en `GAP-01`.
8. ~~Metas de precision y recall~~ → **Política aprobada** (decisión 8); las **cifras** se determinan experimentalmente en la Fase 15 y se documentan.
9. ~~Contrato de features y estrategia de dataset~~ → **Aprobados** (decisiones 4 y 9).
10. ~~**¿Se autoriza, por separado, crear código Python e instalar dependencias en la Fase 15?** → **PENDIENTE.** Es la única condición que falta del gate científico.~~ → **Superada:** la Fase 15 se ejecutó por encargo del equipo y se cerró el 21/09/2026 (`phase-15-closeout.md`). *Anotado en el hotfix documental de la Fase 21.*
11. ~~**¿Cuándo y cómo se resuelve `GAP-01`?** → **PENDIENTE.** Bloquea la integración del modelo en Laravel, aunque no el experimento.~~ → **Resuelta técnicamente en la Fase 16:** `vacancies.target_completion_at` existe y `days_remaining_to_target` es computable. El modelo sigue siendo experimental (`phase-16-laravel-ml-integration.md` §2). *Anotado en el hotfix documental de la Fase 21.*
12. **¿Pasan RF-28 y RF-29 al baseline de v1.1?** → **PENDIENTE.** La decisión 11 los mantiene como candidatos.
13. **¿Pasa RNF-C al baseline de v1.1?** → **PENDIENTE — propuesta de la Fase 21 (23/09/2026).** La Fase 20 fue autorizada explícitamente por el equipo y la experiencia 3D está implementada, auditada e integrada, pero implementar no promueve un requisito: RF-29 también está integrado y sigue siendo candidato por la decisión 11. Se propone al equipo decidir RNF-C junto con RF-28 y RF-29.

Las dos compuertas —científica y de integración— están detalladas en [`phase-14-ml-definition.md` §8](phase-14-ml-definition.md).
