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

## 3. Recorrido de demostración

Usuarios de `docs/demo-users.md`, contraseña `password`.

1. **RR. HH. (`rrhh@andino.test`).**
   - Abra Vacantes, luego «Docente de Comunicación - Secundaria», sus postulaciones y POS-00003.
   - Pulse «Evidencias (experimental)».
2. **Evidencias.** Verá el aviso experimental y cuatro registros: un CV en versión 2, un certificado revisado y enlazado, y dos observaciones del evaluador.
3. **Versiones y permisos.**
   - En el CV, abra «Versiones anteriores (1)».
   - En una observación no aparece «Corregir»: solo la corrige su autor (CONT-M01).
4. **Ayuda documental.**
   - Con «Conocimientos pedagógicos», devuelve el certificado con las palabras resaltadas y su fuente.
   - Con «Clase modelo», devuelve la observación de la clase modelo. La de la «secuencia de actividades» es relevante pero no comparte palabras, y no aparece: es el fallo esperado del método léxico.
   - Con «Entrevista personal», se abstiene y lo explica.
5. **Registro con error.** Intente registrar un texto sin `[SINTÉTICO]`: aparece el error y no se guarda nada.
6. **Evaluador (`evaluador@andino.test`).**
   - Vaya a «Mis evaluaciones», abra la sesión y pulse «Evidencias (experimental)».
   - Solo puede registrar observaciones y no ve el historial.
7. **Dirección (`direccion@andino.test`).** Solo consulta y abre el «Historial», que lista identificadores, nunca el texto.
8. **Otra organización (`rrhh@demob.test`).** `/postulaciones/3/evidencias` responde 404.

## 4. Pruebas

### 4.1 Corte vigente: `153a523` (12/11/2026)

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

## 7. Evidencias

Fuera de Git, en `experimental-20261110/evidencias/`:

- `INVENTARIO_20261111.md` y `SHA256SUMS_20261111.txt`: el corte anterior;
- `correcciones-20261111/` y `correcciones-20261112/`: el RED y el GREEN de cada corrección, la verificación de `153a523` y la suite de Cypress, con un `00-resumen.txt` por carpeta;
- `SHA256SUMS_20261112.txt`: manifiesto de todo lo anterior;
- `correcciones-20261112/GUIA_REAUDITORIA_20261112.md`: guía para la reauditoría del delta.
