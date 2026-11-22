# Rama experimental `exp/evidencias-ml02`: evidencias y ayuda documental ML-02

> **EXPERIMENTAL, local y con datos ficticios.**
>
> - **Qué no es.** No es la integración formal en el SaaS: EI-23 sigue BLOCKED y la integración exige la G0 real, un ADR de alcance y la decisión N5.
> - **Estados.** Ningún estado formal cambia: F36-SBX-GATE = NO SUPERADO, F37-SBX = BLOQUEADA, F36–F40 = BLOQUEADAS y datos reales = PROHIBIDOS.
> - **Bandera.** Todo responde 404 salvo con `EXPERIMENTAL_EVIDENCIAS=true` (`config/experimental.php`).
> - **Publicación.** Sin push, merge, tag ni release.

## 1. Qué hace

| Capacidad | Dónde | Avance técnico | Estado formal |
|---|---|---|---|
| Evidencias de una postulación: registrar, consultar, enlazar a un criterio de la misma vacante, revisar, corregir con una versión nueva y retirar | `/postulaciones/{id}/evidencias` | Tablas de solo inserción con triggers de PostgreSQL. Reglas R-01 a R-09 del flujo F37 (policy y form requests). Auditoría sin texto. Historial | F37-SBX BLOQUEADA; integración, EI-23 BLOCKED |
| Ayuda documental ML-02: fragmentos por criterio, con su fuente, y búsqueda exacta | Panel lateral de la misma página | BM25 léxico por postulación (`EXP-BM25-LEXICO-v1`), k = 3, con abstención. Sin entrenamiento | EI-09 CONDITIONAL (F36-M02); EI-07 ALLOWED solo tras el gate |
| Evaluación con el arnés F38 | `php artisan ml02:evaluar` | Preregistro antes de ejecutar; `test` abierto una vez | Ver [resultados](../academico/preparacion-f38-ml02/resultados-exp-bm25-v1/RESULTADOS.md) |

**Qué no hace:**

- no puntúa, ordena, compara, recomienda ni descarta personas;
- la evidencia no entra en el ranking (RF-21), en la decisión de Dirección (RF-23) ni en la tarjeta de ML-01;
- la página no muestra el nombre ni los datos de contacto del postulante.

## 2. Arranque (proyecto Docker propio)

Desde el worktree de esta rama. El `.env` local no se versiona y usa los puertos 8030 (app), 8031 (E2E), 5462 (PostgreSQL) y 6409 (Redis), con `EXPERIMENTAL_EVIDENCIAS=true`. El `.env.e2e` lleva la misma bandera.

```
docker compose -p experimental up -d --wait
docker compose -p experimental exec app php artisan db:seed --force
docker compose -p experimental exec app php artisan db:seed --class=ExperimentalEvidenceSeeder --force
```

- **`db:seed`** carga `DemoSeeder` sobre una base recién migrada.
- **`ExperimentalEvidenceSeeder`** añade cinco versiones de evidencias ficticias a POS-00003. Se niega a repetirse sobre los mismos datos.

La demo de la exposición (`entregaacad`) y el proyecto `continuacion` no se usan.

## 3. Guion de cinco minutos

URL `http://localhost:8030`. Usuarios de `docs/demo-users.md`, contraseña `password`. Antes de empezar, con la base del proyecto `experimental` (nunca la de `entregaacad`), cargue los datos de la §2. Si ya se usó, reiníciela con `migrate:fresh --seed --force` y el seeder experimental. Abra una ventana privada por usuario.

| Min. | Quién | Qué hacer | Qué se ve |
|---|---|---|---|
| 0:00 | RR. HH. `rrhh@andino.test` | Vacantes → «Docente de Comunicación - Secundaria» → Postulaciones → POS-00003 → **Evidencias (experimental)** | Aviso experimental y cuatro registros ficticios. La página no muestra el nombre del postulante |
| 0:30 | RR. HH. | Registrar: tipo «Certificado» y una descripción **sin** `[SINTÉTICO]` | Error de validación, sin registro |
| 0:50 | RR. HH. | Repetir con `[SINTÉTICO] Constancia ficticia de un curso de evaluación formativa.` | Nueva evidencia con autor, fecha y fuente «Documento presentado» |
| 1:20 | RR. HH. | En esa evidencia: **Corregir con una versión nueva**, cambiar el texto y **Registrar versión nueva**. Abrir «Versiones anteriores (1)» | Versión 2 vigente; la 1 se conserva con su autor y su fuente. Nada se borra |
| 2:00 | RR. HH. | Ayuda documental: criterio «Conocimientos pedagógicos» → **Ver fragmentos** → **Abrir la evidencia EVD-…** | Fragmento con las palabras resaltadas y su fuente; la tarjeta completa de la evidencia queda destacada |
| 2:30 | RR. HH. | Criterio «Clase modelo» | Recupera la observación de la clase modelo. **Fallo esperado:** la observación de la «secuencia de actividades» es pertinente y no aparece, porque no comparte palabras |
| 2:50 | RR. HH. | Criterio «Entrevista personal» | **Abstención:** «no significa que el criterio no se cumpla» |
| 3:10 | — | Explicar los límites (§5): BM25 léxico, 12 fragmentos, Recall@3 de 0,5 en `dev` y **0 en `test`**, H2 rechazada, sin entrenamiento. No puntúa personas; decide Dirección (RF-23) | — |
| 3:40 | Evaluador `evaluador@andino.test` | Mis evaluaciones → sesión → **Evidencias (experimental)** | Solo puede registrar observaciones; no hay «Historial» |
| 4:00 | Dirección `direccion@andino.test` | La misma postulación → Historial | Solo lectura; el historial lista identificadores, nunca el texto |
| 4:15 | RR. HH. de otra organización `rrhh@demob.test` | Abrir `/postulaciones/3/evidencias` | 404 |
| 4:30 | RR. HH. | Abrir `/postulaciones/7/evidencias` («Coordinador(a) de Tutoría», ya cerrada) | «Vacante cerrada»: se consulta, pero no hay formularios. Si se cierra con la página abierta, el envío vuelve con el motivo (R-08) y no registra nada (E2E-21) |

La bandera desactivada (`EXPERIMENTAL_EVIDENCIAS=false`) quita los enlaces y deja las ocho rutas en 404. Se comprueba con `EvidenceEntryPointsTest`; no se cambia en vivo.

## 4. Pruebas

### 4.0 Corte vigente: `cc315f6` (22/11/2026)

Código de `cc315f6`, con las correcciones del recorrido de la §6.1. El commit de documentación que le sigue no cambia el código. Logs fuera de Git, en `evidencias/f37-cierre-20261122/`.

| Prueba | Resultado |
|---|---|
| PHPUnit focal: Evidence, Ml02, carreras de APP-M01, Applications y Assessments | 121 passed |
| PHPUnit completo | 525 passed, 8 skipped |
| Componentes · tipos · build · `vp check` de lo cambiado | 63 passed · 0 errores · correcto · sin errores |
| Arnés F38 y prototipo F37 | 28 OK · 23 OK |
| Cypress E2E-00 a E2E-21, una spec por contenedor, en serie | **21 de 22 specs en verde a la primera.** E2E-21 pasa 10/10. E2E-10 falló una vez y pasó al repetirla sola (1/1). El fallo esperaba el título de la vacante en la **primera** notificación del candidato. Es **compatible** con la anomalía de reloj observada (el reloj de Windows iba adelantado y sin sincronizar, y la VM oscilaba unos 11 s), pero **su causa no está demostrada**: el log no conserva las notificaciones ni sus fechas. Si reaparece con el reloj estable, hay que capturar todas las notificaciones con su fecha e identidad antes de atribuirlo al entorno o de cambiar el orden (F37-RA-L01). Las esperas se ampliaron a 30 s solo en la ejecución (`CY_TIMEOUT_MS`), sin cambiar la configuración ni las specs |

**Qué es simulado.** En E2E-21, el retraso, el fallo de red y el HTTP 500 de la ayuda se producen con `cy.intercept`; todo lo demás va contra el backend real.

### 4.1 Corte anterior: `153a523` (12/11/2026)

Código de `153a523`, que incluye las correcciones APP-M01 y APP-M02 de la §6. `0de8594` solo ordena los `use` de una prueba PHP (Pint), y sobre él se repitió PHPUnit, focal y completo, con el mismo resultado. El commit de documentación que le sigue no cambia el código.

| Prueba | Comando | Resultado |
|---|---|---|
| Escenarios F37, flujo, triggers, auditoría, aislamiento, método y carreras del cierre (APP-M01) | `php artisan test tests/Feature/Evidence tests/Unit/Ml02 tests/Feature/Concurrency/EvidenceClosureConcurrencyTest.php` | 71 passed |
| PHPUnit completo | `php artisan test` | 518 passed, 8 skipped (base `2b074e4`: 447 + 8) |
| Componentes y tipos | `npx vp test --run` · `npx tsc --noEmit` | 62 passed · 0 errores |
| Formato y lint de los archivos cambiados | `npx vp check <archivos>` | Sin errores |
| Build | `npm run build` | Correcto |
| Arnés F38 y prototipo F37 | `test_f38_evaluar.py` · `test_f37_flujo_evidencias.py` | 28 OK · 23 OK |
| Cypress, suite completa | Una spec por contenedor con nombre, en serie y sin `--rm` (`cy_suite.sh`) | 22 specs (E2E-00 a E2E-21), 105/105, código 0 en todas. Sin la recarga de E2E-21 |

### 4.2 Corte anterior: `400c55b` (10/11/2026), reconciliado (APP-L01)

Se conserva como se registró; el [inventario del 11/11/2026](#7-evidencias) lo corrige donde estaba mal.

| Prueba | Resultado registrado | Reconciliación |
|---|---|---|
| Escenarios F37 y método | 57 passed | Sin cambios |
| Ablaciones de las reglas | 9 de 9 detectadas, tras añadir 2 pruebas por 2 supervivientes | Sin cambios |
| PHPUnit completo | 504 passed, 8 skipped | Sin cambios |
| Componentes y tipos | 62 passed · 0 errores | Sin cambios |
| Cypress E2E-21 | 7/7 sobre `e3f80a1` | La spec recargaba la página antes de la segunda consulta y eludía APP-M02 |
| Cypress, suite sobre `400c55b` | «E2E-00 a E2E-09, 22/22; E2E-10 a E2E-21 no se ejecutaron» | **Incorrecto.** El sistema detuvo solo el proceso envoltorio: el bucle siguió. E2E-00 a E2E-10 y E2E-12 a E2E-21 pasaron, con log completo y código 0. E2E-11 falló por infraestructura (`EAI_AGAIN app-e2e`), porque `app-e2e` se estaba deteniendo a mano. La línea del resumen que invalidaba E2E-10 fue un error: su log está completo, con código 0 y `OOMKilled=false` |
| Manifiesto `SHA256SUMS.txt` | 54 entradas | Dos no coinciden: `00-resumen.txt`, que siguió creciendo, y `e2e-12-negative-rules.log`, cuyo hash era el de un log a medio escribir. Se conserva; `SHA256SUMS_20261111.txt` cubre los 64 archivos de ese corte |

## 5. Lo que falta para que deje de ser experimental

- **Formal.** La G0 real, un ADR de alcance, la decisión N5 de integración (EI-23) y F36-SBX-GATE SUPERADO con FG-03 que liste las EI. Ninguna es técnica.
- **Técnico.**
  - Pruebas manuales con lector de pantalla, también del aviso de fallo y del estado «en curso» de la ayuda.
  - Un corpus de evaluación de tamaño real; el actual tiene 12 fragmentos.
  - Descriptores de criterio escritos por personas, si se quisiera mejorar el recall sin métodos semánticos.
- **ML-02 v1 no cambia.** Recall@3 de 0,5 en `dev` y 0 en `test`; H2 rechazada. Cualquier método nuevo necesitaría otro `method_id` y otro preregistro, sin usar `test` para desarrollarlo. La [errata del preregistro](../academico/preparacion-f38-ml02/preregistro/ERRATA_PREREGISTRO_EXP-BM25-LEXICO-v1.md) corrige el número de palabras vacías (49, no 51) sin tocar el método.

## 6. Correcciones de la auditoría de Codex (10/11/2026)

Candidato auditado: `e5f83a4`. Informe de Codex, con SHA-256 `713d4d7d555b0e3e2d5347d9c68e4cd4c17e362df8ea24c9b215acfe68f0711c` (fuera del repositorio).

| ID | Hallazgo | Corrección | Commit | Prueba y resultado |
|---|---|---|---|---|
| APP-M01 | La política leía la vacante antes de escribir: un cierre confirmado entre medias dejaba pasar la escritura (R-08) | Cada escritura toma un bloqueo compartido de la vacante, primero en su transacción y antes del bloqueo de la postulación (el orden del cierre), y vuelve a comprobar el cierre bajo ese bloqueo | `fd87b78` | `EvidenceClosureConcurrencyTest`: las seis escrituras en los dos órdenes, con procesos PHP y conexiones PostgreSQL reales. Sin el arreglo, 12/12 fallan; con él, 12/12 pasan serializadas. Además, el rollback de una corrección cuya auditoría falla y la doble corrección de la misma versión |
| APP-M02 | Al reenviar la ayuda documental sin recargar, `cy.select()` veía el select «deshabilitado» | **Causa:** las dos consultas son GET a la misma página, y la opción por defecto de Inertia para GET (`preserveState: false`) remontaba la página entera en cada respuesta. El foco caía al cuerpo; con dos envíos solapados (doble clic, o Enter, que Cypress envía dos veces), la segunda respuesta sustituía el select mientras se elegía otro criterio. El error «disabled» de Cypress es su comprobación de foco. **Arreglo:** la página se conserva montada (estado y desplazamiento); la sección indica la consulta en curso y avisa del fallo de red o del servidor, sin el diálogo de Inertia | `153a523` | E2E-21 sin la recarga: consultas sucesivas con Enter y con doble clic, que conservan el mismo nodo, la elección y el foco; consulta en curso, fallo de red, HTTP 500 y recuperación. Sin el arreglo, 2 de 8 fallan; con él, 8/8 |
| APP-L01 | La guía y el manifiesto no reflejaban los logs reales | Inventario fechado del 11/11/2026 y la reconciliación de la §4.2, sin borrar el corte anterior | Este commit | Manifiestos en las evidencias |
| APP-L02 | El preregistro decía 51 palabras vacías; el método tiene 49 | Errata fechada. El preregistro, el método y los resultados no cambian | Este commit | Conteo sobre el blob `3196300c…`, idéntico en `e3f80a1` y en `153a523` |

### 6.1 Cierre del recorrido F37 (22/11/2026)

Defectos del recorrido encontrados al revisar la cadena pantalla → ruta → autorización → servicio → almacenamiento → respuesta → pantalla. Commit `cc315f6`.

| ID | Defecto | Corrección | Prueba |
|---|---|---|---|
| F37-UX-01 | Si el proceso se cerraba con la página abierta, el envío de RR. HH. o del evaluador asignado recibía un 403 sin explicación | El rechazo (R-08) vuelve a la página con el motivo del cierre, visible en un aviso. A quien no podía escribir con el proceso abierto se le sigue respondiendo 403/404. No se inserta nada | `EvidenceClosedProcessTest`: RED de 2 de 4 (403), GREEN de 4 de 4. E2E-21: el cierre con la página abierta y el proceso ya cerrado |
| F37-UX-02 | La ayuda documental mostraba la fuente del fragmento, pero no permitía abrir la evidencia; las versiones anteriores no mostraban su procedencia | Cada fragmento enlaza con la tarjeta completa de su evidencia (foco y realce, sin otra visita). Cada versión anterior muestra su autor y su fuente | Vitest: RED de 1 de 7 con el componente anterior y GREEN de 7 de 7. E2E-21 abre la fuente recuperada |
| F37-UX-03 | No había prueba de los puntos de entrada ni del enlace con la bandera desactivada | Solo cobertura: el expediente (RR. HH. y Dirección) y la sesión asignada muestran el enlace; con la bandera desactivada no aparece y las ocho rutas responden 404 | `EvidenceEntryPointsTest`, 3 de 3 |

## 7. Evidencias

Fuera de Git, en `experimental-20261110/evidencias/`:

- `INVENTARIO_20261111.md` y `SHA256SUMS_20261111.txt`: el corte anterior;
- `correcciones-20261111/` y `correcciones-20261112/`: el RED y el GREEN de cada corrección, la verificación de `153a523` y la suite de Cypress, con un `00-resumen.txt` por carpeta;
- `SHA256SUMS_20261112.txt`: manifiesto de todo lo anterior;
- `correcciones-20261112/GUIA_REAUDITORIA_20261112.md`: guía para la reauditoría del delta.
- `f37-cierre-20261122/`: el RED y el GREEN de la §6.1, la verificación y Cypress sobre `cc315f6`, y la guía de entrega a Codex (`GUIA_REAUDITORIA_20261122.md`), con su manifiesto `SHA256SUMS_20261122.txt`.
- `visual-20261122/`: el incremento visual de la §8, con las capturas de referencia y las finales, la verificación, Cypress, el diagnóstico de E2E-10 y su manifiesto `SHA256SUMS_visual_20261122.txt`.

## 8. Incremento visual (rama `design/f37-visual`, 22/11/2026)

Sale de `53d8e22`, el candidato que Codex dio por apto para la demostración experimental. Solo cambia la presentación: portada con profundidad (CSS 3D, ADR-003) y pulido de las pantallas del recorrido F37. No cambia PHP, rutas, permisos, BM25, ML-01, el ranking ni la decisión humana. Los recursos visuales y el vídeo pendiente de Higgsfield están en [`portada-recursos-visuales.md`](portada-recursos-visuales.md).

**Resultados sobre `0d91bcb`.** Bundle `2d7f7c95…`; logs en `evidencias/visual-20261122/`.

| Prueba | Resultado |
|---|---|
| Build · tsc · Vitest · `vp check` de lo cambiado | Correcto · 0 errores · 65 passed · sin errores |
| PHPUnit | No se repite: el backend es idéntico a `cc315f6` (525 passed, 8 skipped) |
| Cypress E2E-00 a E2E-22, una spec por contenedor y en serie, con control de memoria antes de cada una | **22 de 23 specs en verde a la primera**, incluidas E2E-18 (8/8), E2E-20 (12/12), E2E-21 (10/10) y la nueva E2E-22 (7/7). E2E-10 falló una vez con la misma aserción que en `cc315f6` y pasó al repetirla sola (1/1) |

**E2E-10, con datos (F37-RA-L01).**
- Tras la repetición se exportaron las notificaciones del segundo candidato con su fecha (`13-diag-e2e10/`).
- **Los datos:** la notificación sembrada «Coordinador(a) de Tutoría» tiene las 13:20:38 y la del cierre de E2E-10, las 13:20:46. El margen es de 8 s y `created_at` solo distingue segundos. En ese momento, la VM iba 11 s por detrás del host.
- **Mecanismo plausible:** un salto de reloj de ese tamaño entre la siembra y el cierre invertiría el orden. Es exactamente la aserción que falla.
- **Lo que no se demostró:** no se capturó la corrida fallida misma.
- **Antigüedad:** la fragilidad es anterior a este incremento, porque E2E-10 no toca nada de lo cambiado. No se cambia el orden de las notificaciones.
