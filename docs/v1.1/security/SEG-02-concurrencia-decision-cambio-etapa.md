# SEG-02 — Carrera entre la decisión final y los cambios manuales de etapa (A-28)

> Investigación y reproducción del 28/10/2026 en la rama `fix/seg-02-decision-stage-concurrency`. **Resultado: REPRODUCIDO.** **No corregido:** este incremento no cambia el código funcional. Las cuatro pruebas concurrentes que reproducen el defecto quedan en RED intencionado, así que el commit es un **candidato diagnóstico no integrable**. No inicia F37-SBX, no supera ningún gate y no cambia estados formales de gobierno. Todavía sin número DEF (ver §15).

## 1. Base y entorno

| Dato | Valor |
|---|---|
| Base | `develop` = `origin/develop` = `55456943059efaa7b34fd7550de97986f0d13061`, árbol `01dc59a80eed0e9f7c26143f6787010fcefb406c` (el mismo de `main` = `origin/main` = `55f758e`) |
| Rama | `fix/seg-02-decision-stage-concurrency`, creada desde esa base en un worktree aislado. No existía ni local ni remotamente |
| Relación con SEG-01 | `fix/seg-01-internal-application-authorization` (`9d1095c`, árbol `fa8f17a`) no está integrada y no se integró aquí. Cambia `ApplicationController`, `ApplicationPolicy`, `docs/defects.md`, su documento y su prueba: nada de los servicios, modelos ni migraciones que intervienen en esta carrera, que no depende de SEG-01 |
| Commit del candidato | Se consulta en Git; este documento no puede citar el commit que lo contiene |
| Runtime | Laravel 13.31.0, PHP 8.4.25 y PostgreSQL 17.11, en Docker Desktop (motor 29.9.2) |
| Aislamiento | `READ COMMITTED`: es el `default_transaction_isolation` del servidor y el valor efectivo que informó cada proceso. `config/database.php` no fija otro. `deadlock_timeout` = 1 s y `lock_timeout` = 0 (sin límite) |
| Base de pruebas | `reclutamiento_testing`, separada de `reclutamiento` y de `reclutamiento_e2e`. `phpunit.xml` la fuerza con `force="true"` y la CI la crea con el mismo nombre |
| Datos | Solo ficticios, generados por las factories |

## 2. Regla e hipótesis

- **A-28.** «Registrada la decisión final, RR. HH. no puede hacer cambios manuales de etapa (preselección, descarte, cambio de etapa) en esa vacante; solo se permiten las transiciones de RF-24 y RF-25.»
- **A-27.** La decisión exige una postulación en `finalista` con resultados completos. Hay una sola por vacante, no se puede modificar y no cambia estados.
- **A-29, A-30 y A-31.** RF-24 pasa la elegida de `finalista` a `seleccionado`. El cierre exige la selección. El resultado final se notifica al cerrar, y las postulaciones `descartado` no reciben un segundo aviso.

**Hipótesis heredada de la revisión anterior, sin confirmar hasta ahora:** un cambio de etapa supera la comprobación de A-28, queda suspendido, se registra la decisión y el cambio continúa hasta dejar un estado incompatible con A-28.

## 3. Transacciones, locks y momento de las comprobaciones

Los controladores (`ApplicationStageController`, `FinalDecisionController`, `SelectionRegistrationController` y `VacancyClosureController`) llaman una sola vez a un servicio. Ni ellos ni sus Form Requests o Policies consultan `selection_decisions` ni toman locks: todo ocurre en los servicios.

| Operación | Transacción | Comprobaciones y momento | Locks de fila | Orden |
|---|---|---|---|---|
| **Cambio manual**, RF-13/RF-14: `ApplicationStageService::moveTo` (preseleccionar, descartar y cambiar de etapa) | Solo `transition()` (`:53`) | **A-28 fuera de la transacción**: `exists()` sin lock en `:41`, y no se repite. Dentro: vacante cerrada y transición válida | `applications` `FOR UPDATE` (`:54`). La vacante se lee sin lock (`:55`) | Postulación |
| **Decisión**, RF-23: `FinalDecisionService::decide` | Toda la operación (`:30`) | Publicada, sin decisión previa, postulación de la vacante y «Finalista» (`:51`) **sobre una lectura sin lock** (`:41-45`). Después, el ranking (`:55`) | `vacancies` `FOR UPDATE` (`:31`). Al insertar, las claves foráneas toman `FOR KEY SHARE` de la organización, la vacante, la postulación elegida y el aprobador | Vacante |
| **Selección**, RF-24: `SelectionRegistrationService::register` | Toda (`:29`) | Publicada, decisión existente y no registrada, transición válida | `vacancies`, `selection_decisions` y `applications` `FOR UPDATE` (esta última vía `transition()`) | Vacante → decisión → postulación |
| **Cierre**, RF-25: `VacancyClosureService::close` | Toda (`:35`) | Transición de la vacante; decisión y selección registradas | `vacancies` `FOR UPDATE` y cada postulación pendiente `FOR UPDATE`, por id (vía `transition()`) | Vacante → postulaciones |
| **Programación**, RF-16/RF-17: `AssessmentScheduler`, relacionada | Toda | Vacante no cerrada y etapa compatible. **No consulta la decisión** | `applications` `FOR UPDATE` (`:113`); vacante sin lock; `transition()` sobre la misma fila (`:163`) | Postulación |

**Consecuencia: el cambio manual y la decisión no comparten ningún lock.** La decisión bloquea la fila de la vacante y el cambio manual la de la postulación, así que ninguno espera al otro.

Con `READ COMMITTED`, cada sentencia ve lo confirmado antes de empezar, un `SELECT` sin lock no espera ni bloquea, y `FOR UPDATE` solo serializa a quien pide la misma fila. Por eso una comprobación hecha sin un lock común queda obsoleta en cuanto otra transacción confirma.

### Restricciones de la base de datos

| Restricción | Qué impide | ¿Protege A-28? |
|---|---|---|
| `selection_decisions.vacancy_id` único | Dos decisiones para una vacante | No |
| Clave foránea `selected_application_id` | Elegir una postulación inexistente | No: no mira su estado |
| `CHECK` de posición, puntaje y registro | Valores incoherentes en la decisión | No |
| `applications_status_valid` | Estados fuera del catálogo | No |
| Índice único parcial `applications_one_selected_per_vacancy` | Dos `seleccionado` en una vacante (A-29) | No |
| Trigger `audit_logs_append_only` | Editar o borrar la auditoría | No; además impide corregir el rastro |

Ninguna restricción relaciona la decisión con el estado de su postulación ni prohíbe cambios de etapa posteriores a la decisión.

## 4. Instrumentación y aislamiento comprobados

- Prueba concurrente: [`DecisionStageConcurrencyTest`](../../../tests/Feature/Concurrency/DecisionStageConcurrencyTest.php).
- Proceso auxiliar: [`seg02-worker.php`](../../../tests/Feature/Concurrency/Support/seg02-worker.php).
- Controles secuenciales por HTTP: [`DecisionStageSequentialTest`](../../../tests/Feature/Concurrency/DecisionStageSequentialTest.php).

Todo es instrumentación exclusiva de pruebas: el runtime no se toca y la aplicación nunca carga el proceso auxiliar.

**Procesos reales.** Cada operación corre en un proceso PHP propio, con su propia conexión a PostgreSQL, y llama al mismo servicio que el controlador. No se simula el algoritmo.

**Fixtures confirmados.** La clase no usa `RefreshDatabase`. Crea los datos fuera de cualquier transacción para que los demás procesos los vean, y migra desde cero (`migrate:fresh`) antes y después de cada prueba, solo sobre `reclutamiento_testing`.

**Aislamiento verificado antes de escribir:**

- el orquestador comprueba el nombre de su base y la identidad del servidor, y la conexión de barrera debe coincidir con él;
- el proceso auxiliar se niega a ejecutar si su entorno no es `testing` o su base efectiva no es `reclutamiento_testing`;
- cada proceso informa entorno, base, aislamiento, pid del backend, dirección del servidor, arranque del postmaster y cola, y la prueba exige que coincidan con el orquestador. En todas las ejecuciones: `reclutamiento_testing`, `read committed`, `172.18.0.2:5432`, el mismo arranque y cola `sync`;
- `pg_stat_activity` confirma que el backend del proceso retenido está en `reclutamiento_testing`.

**Barrera determinista.** Una tercera conexión toma un lock que el primer proceso solo encuentra **después** de su propia comprobación. La prueba no avanza hasta ver en `pg_stat_activity` que ese proceso espera un lock (`wait_event_type = Lock`), que `pg_blocking_pids` incluye la barrera y que la sentencia en espera es la prevista. El sondeo cada 20 ms solo observa; el orden lo garantiza el lock.

| Barrera | Detiene | Por qué no interfiere |
|---|---|---|
| `select id from applications where id = ? for share` | El `FOR UPDATE` de `transition()` (`ApplicationStageService.php:54`), posterior a la comprobación de A-28 | No choca con el `FOR KEY SHARE` que toman las claves foráneas al insertar la decisión. Un primer intento con `FOR UPDATE` sí chocaba: la decisión esperaba a la barrera y el proceso agotó su tiempo. Fue un fallo de orquestación y no se contó como resultado |
| `lock table interview_results in access exclusive mode` | La lectura de resultados de entrevista del ranking (`VacancyRankingBuilder`), posterior a la comprobación «Finalista» | El cambio de etapa nunca lee esa tabla, y la decisión todavía no tiene ningún lock sobre la postulación |

**Orden de confirmación.** Si el segundo proceso termina mientras el primero sigue retenido, el segundo confirmó antes. Si en cambio espera un lock del primero, el runtime serializa ambas operaciones: se libera la barrera y se comprueba el resultado igual. Si esperara un lock de la propia barrera, la prueba fallaría como «ORQUESTACIÓN», nunca como invariante. El control S6 ejercita la rama serializada.

**Reloj monotónico.** Las cronologías usan `hrtime` (`CLOCK_MONOTONIC`), común a todos los procesos del contenedor. En la VM de Docker Desktop el reloj de pared salta hacia atrás: un muestreo de 150 s midió 5 saltos de entre −204 y −241 ms, uno cada 30 s aproximadamente. En la ejecución 2, la última con reloj de pared, varios eventos aparecieron desordenados por esa causa; las aserciones dieron el mismo resultado.

**Límites.**

1. La barrera alarga a voluntad una ventana que en producción dura unas pocas consultas. La prueba demuestra que el entrelazado es posible y qué estado deja; no mide su probabilidad natural, y no se hizo una prueba de estrés sin coordinación.
2. Los procesos llaman a los servicios, no a HTTP. Los controladores, Form Requests y Policies no añaden comprobaciones ni locks (verificado), y los controles secuenciales sí recorren HTTP.
3. En pruebas la cola es `sync`; en producción las notificaciones van a Redis. En ambos casos se despachan tras confirmar (`afterCommit`).
4. Hay una sola instancia de PostgreSQL 17.11 con el aislamiento por defecto.

## 5. Escenarios e invariantes

| Invariante | Enunciado |
|---|---|
| **I1**, principal | Una decisión registrada no apunta a una postulación descartada |
| **I2**, A-28 | Ningún cambio manual de etapa de la vacante se confirma después de su decisión |
| **I3** | Con una decisión registrada, RF-24 y RF-25 pueden completar el proceso |

Las aserciones aceptan cualquier resultado que produzca un orden serial —una operación completa y después la otra— y rechazan los que ningún orden serial produce. Por eso seguirán valiendo después de una corrección que serialice.

| Escenario | Tipo | Coordinación | Se comprueba |
|---|---|---|---|
| S1 | Secuencial, HTTP | Decisión y después descarte de la elegida | El descarte se rechaza |
| S1b | Secuencial, HTTP | Decisión y después descarte de otra finalista | El descarte se rechaza |
| S2 | Secuencial, HTTP | Descarte y después decisión sobre la descartada | La decisión se rechaza |
| S3 | Concurrente | El descarte de la elegida supera A-28 y queda retenido en su `FOR UPDATE`; se registra la decisión; el descarte continúa | I1, I2 e I3 |
| S3b | Concurrente | La decisión supera «Finalista» y queda retenida en el ranking; se descarta la elegida; la decisión continúa | I1, I2 e I3 |
| S4 | Concurrente | Como S3, pero el descarte es de otra postulación de la misma vacante | I1, I2 e I3 |
| S4b | Concurrente | Como S4, con un cambio de etapa de «En entrevista» a «Finalista» | I1, I2 e I3 |
| S5 | Control concurrente | Descarte en la vacante 2 mientras se decide la vacante 1 | Ambas operaciones son legítimas |
| S6 | Control del instrumento | Dos decisiones simultáneas sobre la misma vacante | La segunda espera el lock de la vacante y queda una sola decisión |

## 6. Cronología concurrente

Ejecución 5 de la serie de frecuencia, en milisegundos desde que la barrera toma su lock (reloj monotónico). A = RR. HH. descarta; B = el Aprobador decide; C = RF-24; D = RF-25. La postulación elegida es la #1.

**S3**

| ms | Proceso | Evento |
|---|---|---|
| 0,0 | Barrera (pid 2754) | `FOR SHARE` sobre la postulación #1 |
| 3,2 | Orquestador | Lanza A |
| 312,7 | A (pid 2755) | Llama a `discard` y supera la comprobación de A-28: aún no hay decisión |
| 354,0 | Orquestador | Ve a A esperando `Lock/transactionid`, bloqueado por 2754, en `select * from "applications" where "applications"."id" = $1 limit 1 for update` |
| 354,6 | Orquestador | Lanza B |
| 681,2 | B (pid 2756) | Llama a `decide` |
| 856,6 | B | **Decisión #1 confirmada**, eligiendo la #1, mientras A sigue retenido |
| 881,0 | Orquestador | Libera la barrera |
| 1094,1 | A | **Descarta la #1 después de la decisión** |
| 1484,6 | C | RF-24 rechazado: «No es posible cambiar la postulación de «Descartado» a «Seleccionado».» |
| 1863,6 | D | RF-25 rechazado: «Para cerrar la convocatoria primero deben registrarse la decisión final (RF-23) y la selección del candidato (RF-24).» |

**S3b**

| ms | Proceso | Evento |
|---|---|---|
| 0,0 | Barrera (pid 2762) | `ACCESS EXCLUSIVE` sobre `interview_results` |
| 0,7 | Orquestador | Lanza B |
| 311,5 | B (pid 2770) | Llama a `decide`: bloquea la vacante, comprueba «Finalista» y empieza el ranking |
| 390,9 | Orquestador | Ve a B esperando `Lock/relation`, bloqueado por 2762, en la lectura de `interview_results` |
| 391,5 | Orquestador | Lanza A |
| 704,4 | A (pid 2772) | Llama a `discard`: no hay decisión confirmada |
| 941,4 | A | **Descarta la #1** sin esperar a B |
| 952,5 | Orquestador | Libera la barrera |
| 992,5 | B | **Decisión #1 confirmada sobre una postulación ya descartada** |
| 1354,6 y 1703,8 | C y D | RF-24 y RF-25 rechazados con los mismos mensajes que en S3 |

**S4 y S4b** siguen el patrón de S3. A queda retenido en el `FOR UPDATE` de otra postulación —la #2, finalista, o la #3, en entrevista—, continúa después de la decisión confirmada de B y descarta la #2 o mueve la #3 a «Finalista». RF-24 y RF-25 terminan y la vacante se cierra.

**S6, control.** B queda retenido en el ranking con la vacante bloqueada. El segundo proceso, E, espera `Lock/transactionid` bloqueado por B en `select * from "vacancies" where "vacancies"."id" = $1 limit 1 for update`. Al liberar la barrera, B confirma y E recibe «Ya se registró la decisión final para esta vacante; no puede modificarse.»

## 7. Resultados observados

| Escenario | Serie de frecuencia: 5 ejecuciones consecutivas |
|---|---|
| S3 | **RED 5 de 5**: I1 violada |
| S3b | **RED 5 de 5**: I1 violada |
| S4 | **RED 5 de 5**: I2 violada |
| S4b | **RED 5 de 5**: I2 violada |
| S5, S6, S1, S1b y S2 | Aprobados 5 de 5 |
| Fallos de orquestación, entorno o precondición | 0 |

**Frecuencia bajo la coordinación determinista: 100 %.** El mismo resultado se observó en las ejecuciones 2 y 3, anteriores a S6, y en la suite completa. La ejecución 1 usaba todavía la barrera `FOR UPDATE` en S3 (§4).

Mensaje real de S3; los demás están en la evidencia:

> INVARIANTE I1 VIOLADA (A-28): la decisión registrada apunta a una postulación descartada. Cambio manual = ok ("descartado"); decisión = ok (1); la segunda operación terminó mientras la primera esperaba en la barrera; RF-24 = rejected (InvalidStateTransition: No es posible cambiar la postulación de «Descartado» a «Seleccionado».); RF-25 = rejected (BusinessRuleException: Para cerrar la convocatoria primero deben registrarse la decisión final (RF-23) y la selección del candidato (RF-24).).

## 8. Causa técnica demostrada

1. **Comprobación fuera de la transacción (S3, S4 y S4b).** `moveTo()` comprueba A-28 en `ApplicationStageService.php:41`, antes de abrir la transacción, y `transition()` no la repite. Si una decisión se confirma entre esa línea y el `FOR UPDATE` de `:54`, el cambio se aplica igual.
2. **Lectura sin lock en la decisión (S3b).** `FinalDecisionService` comprueba «Finalista» (`:51`) sobre una lectura sin lock (`:41-45`). Si un descarte de esa postulación se confirma entre la comprobación y el `COMMIT` —por ejemplo, durante el ranking de `:55`—, la decisión se inserta igual.
3. **Sin lock común.** La decisión bloquea `vacancies` y el cambio manual `applications`. Ninguno espera al otro, y ninguna restricción de la base cubre el hueco (§3).

El defecto es un *check-then-act* entre dos transacciones que no comparten lock bajo `READ COMMITTED`. No interviene la multiempresa: todo ocurre en una sola organización, con usuarios autorizados.

## 9. Efectos observados

| Efecto | S3 y S3b | S4 | S4b |
|---|---|---|---|
| Decisión | Apunta a la #1, **descartada** (posición 1 de 2) | Apunta a la #1, seleccionada tras RF-24 (posición 1 de 2) | Apunta a la #1, seleccionada tras RF-24 (posición 1 de 3) |
| Selección, RF-24 | **Imposible**: `InvalidStateTransition` | Correcta | Correcta |
| Cierre, RF-25 | **Imposible**, porque exige la selección. La vacante queda `publicada` y sin salida: la decisión no puede reemplazarse (A-27) y A-28 bloquea los cambios manuales | Cerrada | Cerrada; la #2 y la #3 pasan a `no_seleccionado` |
| Ranking vigente | Solo la #2: la elegida desaparece y la posición guardada en la decisión deja de corresponder | Solo la #1, aunque la decisión registró 2 candidatos | La #1, la #2 y la #3 |
| Historial | `finalista → descartado` de la #1 | `finalista → descartado` de la #2, después de la decisión | `en_entrevista → finalista` de la #3, después de la decisión |
| Auditoría | S3: la decisión y después el cambio de etapa; S3b, al revés. Es de solo inserción y no puede corregirse | Decisión, descarte de la #2, selección y cierre | Decisión, cambio de la #3, selección, no seleccionadas y cierre |
| Notificaciones | La persona elegida recibe «… no continuará en el proceso de selección» | La #2 recibe el aviso de descarte después de la decisión y, por A-31, no recibe el resultado del cierre | La #3 recibe «avanzó a la etapa: Finalista» después de la decisión y luego «no ha sido seleccionado(a)» |

## 10. Propuesta mínima de corrección, no implementada

Llevar la comprobación de A-28 dentro de una transacción que tome primero **el mismo lock que la decisión, la selección y el cierre, la fila de la vacante**, y después el de la postulación:

```php
// ApplicationStageService::moveTo — boceto, no implementado
return DB::transaction(function () use ($application, $target, $hr, $comment): Application {
    Vacancy::query()->withoutGlobalScopes()->whereKey($application->vacancy_id)->sharedLock()->firstOrFail(); // FOR SHARE

    if (SelectionDecision::query()->withoutGlobalScopes()->where('vacancy_id', $application->vacancy_id)->exists()) {
        throw new BusinessRuleException('La decisión final ya fue registrada; no se permiten cambios manuales de etapa en esta convocatoria.');
    }

    return $this->transition($application, $target, $hr, $comment); // savepoint y FOR UPDATE de la postulación
});
```

- **`FOR SHARE` en la vacante.** Choca con el `FOR UPDATE` de la decisión, la selección y el cierre, pero deja avanzar a la vez dos cambios manuales de la misma vacante, que siguen serializándose por la fila de su postulación. `FOR UPDATE` también sería correcto, con menos concurrencia.
- **Cierra las dos ventanas.** En S3, S4 y S4b, si la decisión confirma primero, el cambio espera la vacante y la nueva comprobación ve la decisión. En S3b, la decisión retiene la vacante hasta confirmar, así que el descarte espera y después se rechaza.
- **Notificación.** La de `transition()` ya usa `afterCommit()`: se despacha al confirmar la transacción externa o se descarta si se revierte.
- **Defensa opcional.** En `decide()`, leer la postulación elegida con `FOR SHARE` después de bloquear la vacante, en el orden vacante → postulación. Tras la corrección no haría falta: toda transición de una finalista (descarte manual, RF-24 y RF-25) pasa por el lock de la vacante.
- **Regresión.** Las pruebas de este incremento deberán pasar a GREEN, con «serializado por el runtime: sí» en S3, S3b, S4 y S4b. S5 debe seguir sin serializar, por ser vacantes distintas, y S6, serializada.
- **Descartadas para el incremento mínimo:**
  - `SERIALIZABLE`: detectaría el conflicto, pero exige reintentar ante `40001` en todos los servicios;
  - locks consultivos por vacante: equivalentes, pero fuera del patrón actual de bloqueo de fila;
  - un trigger en la base: no distingue los cambios manuales de RF-24 y RF-25 y, sin un lock común, repetiría la carrera.

## 11. Riesgos de locks e interbloqueos

- **No poner el lock de la vacante dentro de `transition()`.** `AssessmentScheduler` bloquea primero la postulación y luego llama a `transition()`, mientras que el cierre bloquea la vacante y después las postulaciones. Habría dos órdenes opuestos sobre las mismas filas: un interbloqueo que PostgreSQL resolvería abortando una transacción con `40P01` al cabo de `deadlock_timeout` (1 s), y que la aplicación mostraría como error 500.
- **Con la propuesta no hay ciclo posible.** Toda ruta que toma ambos locks sigue el orden vacante → postulación: el cambio manual, la decisión (con la lectura opcional), la selección y el cierre. La programación solo bloquea la postulación, el registro de resultados solo su sesión, y la postulación de candidatos (`ApplicationService`) y la publicación (`VacancyService`) solo la vacante.
- **Esperas.** No hay `lock_timeout`. Un cambio manual esperará, como mucho, lo que dure la decisión, la selección o el cierre en curso de esa vacante: milisegundos en estas pruebas. Una nueva postulación de un candidato, que bloquea la vacante con `FOR UPDATE`, también esperará a los cambios manuales en curso.
- **Superficie.** El cambio debe tocar solo `moveTo()`. `transition()` lo siguen usando la programación, la selección y el cierre.

## 12. Observaciones relacionadas, sin verificar

- **La programación no consulta A-28.** `AssessmentScheduler` cambia la etapa (`preseleccionado` o `en_evaluacion` a `en_evaluacion` o `en_entrevista`) sin comprobar si existe una decisión. Sería un hueco secuencial, no de concurrencia; no se probó y queda fuera de SEG-02.
- **Instantánea del ranking.** No se analizó si registrar resultados (`AssessmentResultRecorder`) mientras se decide puede desalinear la posición que guarda la decisión.

## 13. Pruebas ejecutadas

Todas en Docker, sobre PostgreSQL y la base aislada `reclutamiento_testing`.

| Orden | Resultado real |
|---|---|
| `php artisan test --group seg02`, ejecución 3, anterior a S6 | 4 fallidas por invariante (S3 y S3b, I1; S4 y S4b, I2) y 4 aprobadas (70 aserciones) |
| `php artisan test --group seg02 --filter s6` | 1 aprobada (10 aserciones) |
| `php artisan test --group seg02`, 5 ejecuciones consecutivas | En cada una, 4 fallidas por invariante y 5 aprobadas (80 aserciones); 0 fallos de orquestación o entorno |
| `php artisan test` de `Applications`, `Selection`, `Assessments`, `Tenancy`, `Audit` y `Notifications` | 16, 30, 19, 11, 16 y 8 aprobadas (84, 206, 97, 32, 208 y 64 aserciones), 0 fallos |
| `php artisan test` | **4 fallidas, el RED intencionado de S3, S3b, S4 y S4b; 416 aprobadas y 8 omitidas** (1578 aserciones). **La suite global no está en verde** |
| `php artisan test --exclude-group seg02` | 411 aprobadas y 8 omitidas (1498 aserciones), 0 fallos: lo mismo que la base. Las 8 omitidas son las preexistentes de verificación de correo de Fortify, una función desactivada |
| `vendor/bin/pint --test tests/Feature/Concurrency` | Correcto, 3 archivos |
| `npm run build`, `npx tsc --noEmit` y Cypress | No ejecutados: el incremento no cambia el runtime, el frontend ni los `data-cy` |

## 14. Archivos

| Archivo | Cambio |
|---|---|
| `tests/Feature/Concurrency/DecisionStageConcurrencyTest.php` | 6 pruebas concurrentes: S3, S3b, S4 y S4b en RED intencionado, y los controles S5 y S6 |
| `tests/Feature/Concurrency/Support/seg02-worker.php` | Proceso auxiliar de prueba: una operación de servicio por proceso |
| `tests/Feature/Concurrency/DecisionStageSequentialTest.php` | 3 controles secuenciales por HTTP: S1, S1b y S2 |
| `docs/v1.1/security/SEG-02-concurrencia-decision-cambio-etapa.md` | Este documento |

No cambian el código funcional, `docs/defects.md`, las evidencias de SEG-01 ni F35-SBX o F36-SBX.

Trazabilidad: A-28 (RF-13, RF-14 y RF-23), con A-27, A-29, A-30 y A-31 → `ApplicationStageService::moveTo` y `transition`, y `FinalDecisionService::decide` → `DecisionStageConcurrencyTest` (S3 a S6) y `DecisionStageSequentialTest` (S1, S1b y S2).

## 15. Estado y pendientes

- **SEG-02 queda REPRODUCIDO, sin corregir ni cerrar.** El siguiente incremento implementará la corrección de §10 y su auditoría, con estas pruebas como regresión.
- **Commit diagnóstico no integrable.** Las pruebas en RED están en la suite por defecto: integrarlo pondría en rojo `develop` y la CI.
- **Registro del defecto, diferido.** No se asigna número DEF aquí: SEG-01 usa DEF-14 en su rama, aún sin integrar, y numerar ahora arriesgaría una colisión. Se registrará con la corrección.
- **SEG01-AUD-L01**, comprobar las claves públicas en todas las convocatorias de la prueba permanente de SEG-01, sigue pendiente y no se tocó.
- **SEG-03 y SEG-04** quedan fuera de este incremento.
- **Validador de F36-SBX.** Si este cambio se integrara en `develop` o `main`, ese validador fallaría por diseño en la regla FRZ, que detecta cambios ajenos a F36-SBX desde su base: se valida anclado en su rama, como documenta su README. No es un defecto de este incremento.
- **Entorno Docker.** Para ejecutar las pruebas, `app` y `queue` se recrearon montando el worktree de esta rama; los volúmenes con nombre no se tocaron. Al terminar se ejecutó `docker compose down`, sin `-v`, y se recrearon los contenedores desde el checkout principal. Estado final verificado, igual al encontrado: los cuatro contenedores (`app`, `queue`, `postgres` y `redis`) creados y detenidos; `app`, `queue` y los scripts de inicio de `postgres` montan el checkout principal; una sola red `reclutamiento_default`; y los volúmenes `reclutamiento_pgdata`, `reclutamiento_redisdata`, `reclutamiento_vendor` y `reclutamiento_node_modules`, conservados.
