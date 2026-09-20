# Alcance preliminar de v1.1

**Estado: borrador de planificación.** Nada de este documento está aprobado. Sirve para que el equipo decida, no para autorizar trabajo.

Leyenda:

- **Verificado** — comprobado en el repositorio o en una ejecución real.
- **Propuesta** — idea del equipo, aún sin decisión.
- **Pendiente de decisión** — requiere una decisión explícita antes de cualquier implementación.

## 1. Hechos verificados (línea base de v1.1)

- RF-01 a RF-27 están implementados y trazados; su significado no cambia en v1.1.
- `main` y `develop` contienen el mismo código publicado; `v1.0.0-academic` marca el release académico.
- Última ejecución registrada de PHPUnit en v1.0: 244 pruebas, 236 aprobadas, 8 omitidas, 0 fallidas. Última ejecución registrada de Cypress: 14 especificaciones, 43 pruebas, 43 aprobadas. **No se reejecutaron en la Fase 13.**
- El entorno es Docker (Laravel 13 / PHP 8.4, PostgreSQL 17, Redis 7) y CI ejecuta la suite en GitHub Actions.
- El sistema no toma ninguna decisión automática sobre personas.

## 2. Candidatos funcionales (RF-28 en adelante)

Numeración **provisional**: estos identificadores solo se fijan cuando el equipo apruebe el requerimiento.

| Candidato | Descripción | Estado | Riesgo principal |
|---|---|---|---|
| RF-28 (cand.) | Panel operativo de seguimiento de convocatorias: etapas, tiempos y cuellos de botella, sin datos de personas | Propuesta | Puede confundirse con evaluación de candidatos si el diseño no es explícito |
| RF-29 (cand.) | Estimación informativa de riesgo de demora de una convocatoria | Pendiente de decisión | Depende por completo de `ml-feasibility.md`; sin no-go superado, no existe |
| RF-30 (cand.) | Exportación de reportes operativos del proceso (PDF/CSV) para el informe académico | Propuesta | Riesgo de incluir datos personales si no se filtra por diseño |
| RF-31 (cand.) | Portal público de vacantes con presentación visual mejorada | Propuesta | Alcance visual que puede desbordar hacia rediseño general |

**Descartado explícitamente:** cualquier requerimiento que puntúe, ordene, recomiende, filtre o descarte postulantes de forma automática. No se numerará ni se discutirá como candidato.

## 3. Candidatos no funcionales

| Candidato | Descripción | Estado |
|---|---|---|
| RNF-A (cand.) | Accesibilidad WCAG 2.1 AA verificada en las pantallas de RF-01 a RF-27 | Propuesta |
| RNF-B (cand.) | Presupuesto de rendimiento del frontend con línea base medida | Propuesta |
| RNF-C (cand.) | Experiencia 3D progresiva en pantallas públicas | Pendiente de decisión (ver ADR-003) |
| RNF-D (cand.) | Observabilidad del proceso: métricas operativas y registro estructurado | Propuesta |

## 4. Arquitectura propuesta

- **Laravel sigue siendo el sistema de registro.** Toda decisión, estado y dato de negocio vive en PostgreSQL bajo el control de Laravel.
- **FastAPI, si llega a existir, es un servicio de inferencia opcional y sin estado**: sin acceso a la base principal, sin conocimiento del dominio, sin capacidad de escribir. Laravel funciona completo si el servicio no responde.
- No hay integración Laravel–Python aprobada. No se ha escrito ni un cliente HTTP.

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
3. ¿Se autoriza la experiencia 3D y sus dependencias de frontend?
4. ¿Se autoriza el uso de navegador o red para `reviewing-a11y`?
5. ¿Se autoriza la instalación global de las herramientas oficiales de revisión bloqueadas por licencia?
6. ¿Qué entregables exige la próxima evaluación del curso y con qué fecha?

Ninguna implementación de v1.1 debe comenzar antes de responder 1 y 6.
