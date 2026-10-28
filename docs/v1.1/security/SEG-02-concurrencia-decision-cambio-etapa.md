# SEG-02 — Carrera entre la decisión final y los cambios manuales de etapa (A-28)

> Mantenimiento de seguridad del sistema existente, del 28/10/2026, en la rama `fix/seg-02-decision-stage-concurrency`. **Diagnóstico: REPRODUCIDO** (Parte I). **Corrección: implementada en la rama y pendiente de auditoría de Codex** (Parte II). Registrado como DEF-15 en el [registro de defectos](../../defects.md). No inicia F37-SBX, no supera ningún gate y no cambia estados formales de gobierno.

## Parte I — Diagnóstico (RED)

Texto entregado con el diagnóstico en el commit `e3c6647`, sin cambios. Lo que dice sobre «este incremento», el código «no corregido» o el número DEF «diferido» describe ese momento; la Parte II registra la corrección. Estado con el que se entregó:

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

## Parte II — Corrección (GREEN)

## 16. Estado recuperado y commits

| Dato | Valor |
|---|---|
| Rama | `fix/seg-02-decision-stage-concurrency`, retomada en un worktree aislado. `develop` sigue en `55456943059efaa7b34fd7550de97986f0d13061`: la rama no está por detrás |
| Evidencia RED conservada | `cde288b7a33909f0e478a18fc062cfd92aa3e83a` (pruebas, árbol `b2278c7fe59ee69d23c0fe7ad223d85424f8b605`) y `e3c6647c1c9b52fd6b8b221a7eb6f91e707481b3` (Parte I, árbol `71fe24c02bda57a677c76c7f3754ab2725177914`), sin amend ni reescritura |
| Diagnóstico revalidado | Sobre `e3c6647`, `php artisan test --group seg02`: 4 fallidas por invariante (S3 y S3b, I1; S4 y S4b, I2) y 5 aprobadas (80 aserciones), como en la Parte I |
| Instrumentación adaptada | `2b8f5df3f21d9e8539aebdbca0bf3c508aff75bf` (árbol `c37976a5deafc18d2e7ebd3c40da264ebabaf15f`), todavía en RED |
| Corrección | `4c89a958bc6f4c95e423b227e2a1957c7cf662b0` (árbol `c7b97cfebb75da2d39c734fc8c39640527ec3cf9`) |
| Este documento y DEF-15 | Commit siguiente, que se consulta en Git |
| Relación con SEG-01 | Sigue sin integrar y sin cambios. Solo comparte `docs/defects.md` con esta rama (§24) |

## 17. Corrección

`ApplicationStageService::moveTo()` es el único cambio funcional:

| Antes | Después |
|---|---|
| Comprobaba A-28 con `exists()`, fuera de toda transacción, y después llamaba a `transition()`, que solo bloquea la postulación | Abre una transacción, bloquea la fila de la vacante con `FOR SHARE`, comprueba A-28 bajo ese lock y llama a `transition()` dentro de la misma transacción, como punto de guardado |

```php
return DB::transaction(function () use ($application, $target, $hr, $comment): Application {
    Vacancy::query()->withoutGlobalScopes()->whereKey($application->vacancy_id)->sharedLock()->firstOrFail();

    if (SelectionDecision::query()->withoutGlobalScopes()->where('vacancy_id', $application->vacancy_id)->exists()) {
        throw new BusinessRuleException('La decisión final ya fue registrada; no se permiten cambios manuales de etapa en esta convocatoria.');
    }

    return $this->transition($application, $target, $hr, $comment);
});
```

- **La comprobación y la escritura confirman juntas.** El lock de la vacante dura desde la comprobación hasta el `COMMIT` del cambio de etapa: no queda ninguna ventana entre ambas.
- **`FOR SHARE`.** Choca con el `FOR UPDATE` que toman primero la decisión, la selección y el cierre. No choca con otro `FOR SHARE`, así que dos cambios manuales compatibles de la misma vacante avanzan a la vez (S8), ni con el `FOR KEY SHARE` de las claves foráneas.
- **Sin cambios:** `transition()`, `FinalDecisionService`, `SelectionRegistrationService`, `VacancyClosureService`, `AssessmentScheduler`, controladores, Form Requests, Policies, enums, migraciones y frontend. RF-24 y RF-25 siguen llamando directamente a `transition()`, sin la comprobación de A-28: sus transiciones legítimas no quedan bloqueadas.
- **Se conservan** la autorización por rol y organización, las transiciones válidas (`canTransitionTo` en `transition()`), la decisión humana con confirmación y justificación, el historial y la auditoría en la misma transacción que el cambio, y las notificaciones con `afterCommit()`. Estas se despachan ahora al confirmar la transacción externa, o se descartan si se revierte.
- **El mensaje** que recibe RR. HH. cuando ya existe la decisión no cambia.

## 18. Mapa de transacciones y orden de locks, antes y después

| Operación | Antes | Después |
|---|---|---|
| Cambio manual, `moveTo()` | A-28 sin lock; luego, en la transacción, postulación `FOR UPDATE` | En una transacción: **vacante `FOR SHARE`**, A-28 y postulación `FOR UPDATE` |
| Decisión, RF-23 | Vacante `FOR UPDATE`; lecturas sin lock; al insertar, `FOR KEY SHARE` de organización, vacante, postulación elegida y aprobador | Sin cambios |
| Selección, RF-24 | Vacante, decisión y postulación, en ese orden y `FOR UPDATE` | Sin cambios |
| Cierre, RF-25 | Vacante `FOR UPDATE` y postulaciones pendientes `FOR UPDATE`, por id | Sin cambios |
| Programación, RF-16/RF-17 | Postulación `FOR UPDATE` y `transition()` sobre la misma fila. Nunca la vacante: las sesiones no tienen clave foránea a `vacancies` | Sin cambios |
| Registro de resultados | Solo la sesión `FOR UPDATE` | Sin cambios |
| Postulación de candidatos y publicación | Solo la vacante `FOR UPDATE` | Sin cambios; ahora esperan a los cambios manuales en curso de esa vacante |

En la fila de la vacante, el `FOR SHARE` del cambio manual choca con el `FOR UPDATE` de la decisión, la selección, el cierre, la postulación y la publicación, y es compatible con otro `FOR SHARE` y con `FOR KEY SHARE`.

## 19. Ausencia de ciclos de espera nuevos

1. El único lock nuevo es el `FOR SHARE` de la vacante, y es lo primero que pide la transacción del cambio manual.
2. Después, el cambio manual solo pide la fila de su postulación y los `FOR KEY SHARE` de las claves foráneas del historial y la auditoría. Nunca pide un lock más fuerte sobre la vacante: no la modifica, y no hay `$touches` ni observadores que lo hagan. Por eso dos cambios manuales no pueden interbloquearse al intentar ampliar su lock.
3. Toda ruta que bloquea la vacante y una postulación lo hace en el orden vacante → postulación: el cambio manual, la decisión (por sus claves foráneas), la selección y el cierre.
4. La programación bloquea la postulación y nunca la vacante. Puede hacer esperar a un cambio manual (S7) o esperarlo (S7b), pero nunca espera el lock de vacante que el cambio manual tiene: no hay ciclo.
5. La postulación de candidatos y la publicación bloquean la vacante y ninguna postulación existente: pueden esperar a un cambio manual, nunca al revés.

Las pruebas lo respaldan: en S3, S3b, S4, S4b, S4c, S6, S7 y S7b los procesos se esperaron y ninguno abortó con `40P01`. Un interbloqueo llegaría al proceso como `QueryException`, que la prueba trata como error inesperado.

## 20. Cambios de instrumentación

**La coordinación de S3 a S4b no necesitó cambios.** No presuponía el orden vulnerable: ya distinguía «la segunda operación terminó mientras la primera esperaba» de «la segunda espera un lock de la primera», rama que S6 validó en la Parte I. Con la corrección solo cambia el punto de espera:

- el primer proceso sigue retenido en el `FOR UPDATE` de la postulación, pero ahora ya tiene la vacante;
- el segundo espera la vacante: la decisión, en `select * from "vacancies" … for update` (S3, S4 y S4b), y el descarte, en `… for share` (S3b y S4c).

**Añadido en `2b8f5df`:**

- S4c: la decisión está retenida en el ranking cuando llega el descarte de otra postulación de la vacante;
- S7 y S7b: la programación contra un cambio manual de la misma postulación, en ambos órdenes. Usan una barrera nueva, `lock table evaluation_criteria in access exclusive mode`, que detiene la programación cuando ya tiene la postulación, y la operación `schedule` del proceso auxiliar, con datos ficticios;
- S8: dos cambios manuales compatibles de la misma vacante no se esperan;
- S5 exige además que vacantes distintas no se esperen;
- liberación de recursos. Tras cada carrera y tras RF-24 y RF-25, la prueba exige que no quede abierta ninguna conexión de los procesos ni de la barrera: con ellas terminan sus transacciones y sus locks. Ante cualquier fallo, `tearDown()` mata los procesos, revierte la barrera y termina los backends que sigan vivos a los 5 s.

**Se mantienen** todos los escenarios e invariantes, los procesos y conexiones reales, las barreras deterministas, el reloj monotónico y los límites de espera: 30 s para ver el bloqueo, 60 s para el segundo proceso y 120 s por proceso. Ningún timeout cuenta como éxito y no hay pruebas omitidas.

**RED de la instrumentación nueva, antes de corregir.** Con `2b8f5df` sobre el runtime sin corregir: 4 fallidas por invariante (S3 y S3b, I1; S4 y S4b, I2) y 9 aprobadas (144 aserciones), sin fallos de orquestación, entorno ni recursos. Los escenarios nuevos ya pasaban: son controles, no la evidencia del defecto.

## 21. Resultados con la corrección

Seis ejecuciones de `php artisan test --group seg02` con la corrección: la primera, sobre el árbol de trabajo justo antes de registrar `4c89a95` con el mismo contenido, y una serie de 5 consecutivas sobre ese commit. **13 aprobadas (149 aserciones) en todas**, sin fallos de orquestación, entorno, recursos ni invariante. Cada escenario se comportó igual en la serie de 5:

| Escenario | ¿Serializado? | Resultado | Orden serial equivalente |
|---|---|---|---|
| S3 | Sí | Se confirma el descarte; la decisión se rechaza: «Solo se puede elegir a un candidato en la etapa «Finalista».» RF-24 y RF-25 se rechazan porque no hay decisión | Descarte → decisión |
| S3b | Sí | Se confirma la decisión; el descarte se rechaza: «La decisión final ya fue registrada…». RF-24 y RF-25 completan | Decisión → descarte |
| S4 | Sí | Descarte de la #2 y después la decisión; RF-24 y RF-25 completan | Descarte → decisión |
| S4b | Sí | Cambio de etapa de la #3 y después la decisión; RF-24 y RF-25 completan | Cambio → decisión |
| S4c | Sí | Se confirma la decisión; el descarte de la #2 se rechaza | Decisión → descarte |
| S5 | No | Ambas operaciones, en vacantes distintas | Independientes |
| S6 | Sí | Una sola decisión; la segunda se rechaza | Decisión → decisión |
| S7 | Sí | Programación y después descarte de la misma postulación | Programación → descarte |
| S7b | Sí | Descarte; la programación posterior se rechaza por regla de negocio | Descarte → programación |
| S8 | No | Los dos descartes | Independientes |
| S1, S1b y S2 | Secuenciales, por HTTP | Los rechazos esperados | — |

Invariantes pedidas:

- **Si la decisión gana, el cambio manual posterior se rechaza:** S3b y S4c, y en secuencia S1 y S1b.
- **Si un descarte gana, la decisión posterior no acepta esa postulación:** S3, y en secuencia S2.
- **Nunca quedan a la vez una decisión válida y su candidato descartado:** I1 en S3, S3b, S4, S4b y S4c.
- **La decisión bloquea los cambios manuales posteriores de toda su vacante:** S4c y S1b.
- **Vacantes distintas siguen independientes:** S5, sin espera.

Ninguna aserción exige que gane un proceso concreto: aceptan cualquier orden serial y rechazan los estados que ninguno produce.

Cronología de la ejecución 5 de la serie, en milisegundos (reloj monotónico). A = RR. HH. descarta la #1; B = el Aprobador decide sobre la #1.

**S3**

| ms | Proceso | Evento |
|---|---|---|
| 0,0 | Barrera (pid 1553) | `FOR SHARE` sobre la postulación #1 |
| 3,1 | Orquestador | Lanza A |
| 315,0 | A (pid 1554) | Llama a `discard`: en su transacción toma la vacante y comprueba A-28, todavía sin decisión |
| 380,3 | Orquestador | Ve a A esperando `Lock/transactionid`, bloqueado por 1553, en `select * from "applications" where "applications"."id" = $1 limit 1 for update` |
| 382,7 | Orquestador | Lanza B |
| 707,4 | B (pid 1555) | Llama a `decide` |
| 758,9 | Orquestador | Ve a B esperando `Lock/transactionid`, **bloqueado por A** (1554), en `select * from "vacancies" where "vacancies"."id" = $1 limit 1 for update`: serializado |
| 760,6 | Orquestador | Libera la barrera |
| 820,8 | B | Rechazado, porque A ya confirmó el descarte: «Solo se puede elegir a un candidato en la etapa «Finalista».» |
| 974,0 | A | Resultado «descartado», emitido después de sus notificaciones posteriores al commit |

**S3b**

| ms | Proceso | Evento |
|---|---|---|
| 0,0 | Barrera (pid 1561) | `ACCESS EXCLUSIVE` sobre `interview_results` |
| 0,8 | Orquestador | Lanza B |
| 317,7 | B (pid 1562) | Llama a `decide`: bloquea la vacante, comprueba «Finalista» y empieza el ranking |
| 416,3 | Orquestador | Ve a B esperando `Lock/relation`, bloqueado por 1561, en la lectura de `interview_results` |
| 417,1 | Orquestador | Lanza A |
| 729,9 | A (pid 1563) | Llama a `discard` |
| 786,3 | Orquestador | Ve a A esperando `Lock/transactionid`, **bloqueado por B** (1562), en `select * from "vacancies" where "vacancies"."id" = $1 limit 1 for share`: serializado |
| 814,1 | Orquestador | Libera la barrera |
| 861,1 | B | Decisión #1 confirmada |
| 872,5 | A | Rechazado: «La decisión final ya fue registrada; no se permiten cambios manuales de etapa en esta convocatoria.» |
| 1229,5 y 1950,2 | C y D | RF-24 («seleccionado») y RF-25 («cerrada») completan |

## 22. Regresiones

Todas en Docker, sobre PostgreSQL 17.11. Las de PHPUnit, sobre la base aislada `reclutamiento_testing`.

| Orden | Resultado real |
|---|---|
| `php artisan test --group seg02` sobre `e3c6647` | 4 fallidas por invariante y 5 aprobadas (80 aserciones): el RED recuperado |
| Igual, sobre `2b8f5df` | 4 fallidas por invariante y 9 aprobadas (144 aserciones): el RED de la instrumentación nueva |
| Igual, con la corrección de `4c89a95`, 6 ejecuciones | 13 aprobadas (149 aserciones) en cada una |
| `php artisan test` de `Applications`, `Selection`, `Assessments`, `Notifications`, `Tenancy`, `Audit` y `Candidates`, con la corrección | 16, 30, 19, 8, 11, 16 y 6 aprobadas (84, 206, 97, 64, 32, 208 y 27 aserciones), 0 fallos |
| `docker compose exec app php artisan test` | **424 aprobadas y 8 omitidas** (1647 aserciones), 0 fallos, en 89,42 s. Son las 411 de la base más las 13 de SEG-02; las 8 omitidas son las preexistentes de verificación de correo de Fortify, una función desactivada |
| `docker compose exec app npm run build` | Correcto: 2375 módulos, salida 0 |
| `docker compose exec app npx tsc --noEmit` | 0 errores, salida 0 |
| Cypress, entorno E2E aislado (`reclutamiento_e2e`): `init-e2e-env.sh` y `docker compose --profile e2e run --rm cypress`, el equivalente sin npm en el host de `npm run cy:run` | **«All specs passed!»: 20 specs y 85 de 85 pruebas**, 0 fallidas, en 06:19 (Cypress 15.3.0, Electron 136 headless). Incluye los flujos afectados: e2e-06 (preselección), e2e-09 (decisión final humana), e2e-10 (selección y cierre), e2e-12 (reglas negativas) y e2e-13 (flujo completo) |
| `vendor/bin/pint --test` sobre los archivos tocados | Correcto |
| Ruta de error de la instrumentación, con una sonda temporal no versionada | Una copia de la prueba exigía en S3 un fragmento de sentencia imposible y falló, a propósito, con A retenido y la transacción de la barrera abierta. `tearDown()` mató el proceso, revirtió la barrera y no tuvo que terminar ningún backend a la fuerza. Después, en `reclutamiento_testing`: 0 conexiones de la prueba, 0 conexiones ajenas, 0 locks, base migrada (18 migraciones) y vacía. La sonda se borró |

## 23. Archivos

| Archivo | Cambio | Commit |
|---|---|---|
| `app/Services/Applications/ApplicationStageService.php` | `moveTo()`: lock `FOR SHARE` de la vacante y A-28 en la misma transacción que el cambio | `4c89a95` |
| `tests/Feature/Concurrency/DecisionStageConcurrencyTest.php` | Escenarios S4c, S7, S7b y S8, independencia en S5 y liberación de recursos | `2b8f5df` |
| `tests/Feature/Concurrency/Support/seg02-worker.php` | Operación `schedule` | `2b8f5df` |
| `docs/defects.md` | Fila DEF-15 | Commit de este documento |
| `docs/v1.1/security/SEG-02-concurrencia-decision-cambio-etapa.md` | Esta Parte II | Commit de este documento |

`DecisionStageSequentialTest` y las pruebas existentes no cambian. Trazabilidad: A-28 (RF-13, RF-14 y RF-23), con A-27, A-29, A-30 y A-31 → `ApplicationStageService::moveTo` → `DecisionStageConcurrencyTest` (S3 a S8) y `DecisionStageSequentialTest` (S1, S1b y S2).

## 24. Riesgos y límites

- **Espera de la decisión tras cambios manuales.** PostgreSQL deja pasar un nuevo `FOR SHARE` aunque haya un `FOR UPDATE` esperando, si los locks presentes son todos compartidos. En teoría, una sucesión continua de cambios manuales sobre la misma vacante podría retrasar la decisión. Son acciones humanas de milisegundos y no se observó.
- **Esperas sin límite configurado.** No hay `lock_timeout`. Un cambio manual espera, como mucho, lo que dure la decisión, la selección o el cierre en curso de su vacante; una postulación nueva o una publicación esperan a los cambios manuales en curso. Fueron milisegundos en estas pruebas.
- **Ventanas alargadas.** Las barreras fuerzan cada entrelazado a voluntad. Prueban qué ocurre en cada orden, no la probabilidad natural; no se hizo una prueba de estrés sin coordinación.
- **Servicios, no HTTP.** Los procesos llaman a los servicios. Los controladores no añaden comprobaciones ni locks, y los controles secuenciales y la suite completa sí recorren HTTP.
- **Cola.** En pruebas es `sync`; en producción las notificaciones van a Redis, con el mismo `afterCommit`.
- **Cypress** comprueba que los flujos siguen funcionando, no la concurrencia.
- **Integración con SEG-01.** Ambas ramas añaden una fila después de DEF-13 en `docs/defects.md`. Al integrarlas habrá un conflicto textual trivial, que se resuelve conservando DEF-14 y después DEF-15.
- **Validador de F36-SBX.** Como con SEG-01, si esta rama se integra, ese validador fallará por diseño en la regla FRZ; se valida anclado en su rama.

## 25. Estado y pendientes

- **SEG-02 corregido en la rama y pendiente de auditoría de Codex.** No está integrado, publicado ni cerrado.
- **Gobierno.** No cambia ningún estado formal ni inicia F37-SBX.
- **Fuera de alcance, sin cambios:**
  - la programación sin comprobación de A-28 (§12), que sigue sin verificar;
  - SEG-03 y SEG-04;
  - la observación LOW SEG01-AUD-L01;
  - el ML, el frontend, las skills, los permisos y la configuración global.
- **Recursos aislados creados y estado final.**
  - **Worktree** temporal en `.claude/worktrees/seg02`, sobre esta rama. Contenía archivos ignorados por Git: un `.env` generado por el entrypoint desde `.env.example`, con clave propia (el `.env` real no se copió), un `.env.e2e` generado por `init-e2e-env.sh`, `public/build` y cachés. Se elimina al terminar; la rama se conserva.
  - **Contenedores.** `app` y `queue` se recrearon montando el worktree, y el perfil E2E levantó `app-e2e` y `queue-e2e`. Al terminar se ejecutó `docker compose --profile e2e down`, sin `-v`, y se recrearon los contenedores desde el checkout principal. Estado final verificado, igual al encontrado: los cuatro contenedores (`app`, `queue`, `postgres` y `redis`) creados y detenidos; `app`, `queue` y los scripts de inicio de `postgres` montan el checkout principal; una sola red `reclutamiento_default`; sin contenedores E2E.
  - **Volúmenes** `reclutamiento_pgdata`, `reclutamiento_redisdata`, `reclutamiento_vendor` y `reclutamiento_node_modules`: conservados, ninguno se borró ni recreó.
  - **Bases de datos.** `reclutamiento_testing` quedó migrada y vacía. `reclutamiento_e2e` la reinició Cypress, como está previsto. La base de desarrollo `reclutamiento` solo recibió el `php artisan migrate --force` del entrypoint, sin migraciones pendientes porque esta rama no añade ninguna; no se ejecutó ninguna migración destructiva sobre ella.
