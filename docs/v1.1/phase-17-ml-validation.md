# Fase 17 — Validación ML y regresión integral

**Fecha:** 21 de septiembre de 2026
**Rama:** `feature/phase-17-ml-validation` · **Base:** `5267126` (Fase 16 corregida)
**Writer principal:** Claude Code · **Reviewer:** Codex (auditoría posterior)

> **RF-29: implementado e integrado experimentalmente, validado técnicamente en entorno de pruebas, NO validado institucionalmente ni autorizado para producción.** La decisión final sigue siendo humana (RF-23).

---

## 1. Objetivo

Cerrar la validación de la integración Laravel ↔ FastAPI con evidencia reproducible, sin tocar ninguna decisión científica de la Fase 15. Es una fase de QA: el único cambio de comportamiento es la corrección documental de una afirmación que la Fase 16 dejó desactualizada.

## 2. Observaciones LOW de la Fase 16, cerradas

### A · GAP-01 en la descripción del servicio

La descripción de OpenAPI seguía diciendo que `GAP-01` estaba abierto, cuando la Fase 16 creó `vacancies.target_completion_at`. Actualizada para distinguir dos cosas que no son la misma:

- **resuelto técnicamente**: la columna existe y `days_remaining_to_target` es computable;
- **no validado institucionalmente**: el modelo se entrenó y evaluó solo con datos sintéticos, así que el servicio sigue siendo experimental.

**Alcance ampliado deliberadamente.** La misma afirmación viajaba por otro canal: `/v1/model-info` devolvía `gap_01_open: true` y una nota que decía «`target_completion_at` no existe en Laravel». Eso ya era falso. Corregir solo OpenAPI habría dejado una respuesta servida con un dato incorrecto, así que se actualizaron ambos. El carácter experimental lo sostiene ahora `deployment_status`, que es donde corresponde: lo que impide autorizar producción no es la brecha técnica, sino la ausencia de validación institucional.

### B · Captura de `target_completion_at` en navegador

Faltaba prueba real. `cypress/e2e/e2e-14-target-completion-form.cy.js` cubre el ciclo entero con un `datetime-local` de verdad.

## 3. Pruebas añadidas

### Laravel — 36 nuevas (366 → 402)

| Archivo | Pruebas | Qué fija |
|---|---|---|
| `OperationalRiskCheckpointTest.php` | 15 | El checkpoint con fechas explícitas, la frontera de eventos, ML-FEAT-17 y ML-FEAT-18 históricos, y la separación entre reconstrucción y elegibilidad |
| `MlCrossTenantValidationTest.php` | 10 | Multiempresa adversarial: dos organizaciones pobladas, el vector de A inmune a B, la ruta que no distingue «ajena» de «inexistente» |
| `OperationalRiskAuthorizationTest.php` | 11 | Autorización **por HTTP** para los cinco roles, con una prueba que obliga a decidir el acceso de cualquier rol nuevo |

### Python — 3 nuevas (530 → 532)

`gap_01_open` como resuelto, la nota con la distinción técnica/institucional, y que la descripción de OpenAPI no reclama estar lista para producción.

### Cypress — 12 nuevas (43 → 55)

| Spec | Pruebas | Qué cubre |
|---|---|---|
| `e2e-14-target-completion-form.cy.js` | 4 | Captura, persistencia, opcionalidad, guarda del navegador e inmutabilidad tras publicar |
| `e2e-15-operational-risk-panel.cy.js` | 8 | Panel visible, sin porcentaje inventado, lenguaje neutro, roles y cross-tenant |

## 4. El checkpoint, con fechas

La prueba fuerte usa fechas fijas para que el lector no tenga que calcular nada:

```
closes_at  = 2026-06-10
checkpoint = 2026-06-11 00:00:00  (America/Lima)
```

Cuatro postulaciones alrededor de la frontera: `2026-06-05`, exactamente `2026-06-11 00:00:00`, `2026-06-11 00:00:01` y `2026-06-20`. Entran **dos**: el contrato usa `applied_at <= checkpoint`, así que la que cae justo en el instante cuenta y la del segundo siguiente no.

Lo mismo con las sesiones: una evaluación creada antes y completada **después** del checkpoint cuenta como programada y vencida, nunca como completada.

### Reconstrucción ≠ elegibilidad

Son dos preguntas distintas y la suite las separa:

| | Depende de | Consecuencia |
|---|---|---|
| **Reconstrucción del vector** | Solo del checkpoint | Determinista para siempre. Una prueba lo reconstruye en el checkpoint y meses después, con actividad de por medio, y obtiene el mismo resultado |
| **Elegibilidad para inferir** | Del momento de la consulta | Siete motivos por los que Laravel no pregunta, incluidos vacante cerrada y consulta tardía |

### ML-FEAT-18 histórico

Cuatro vacantes con cronologías distintas alrededor del checkpoint: abierta antes y cerrada después (**cuenta**), cerrada antes (no), publicada después (no), abierta y todavía abierta (**cuenta**). El conteo es el estado **en el checkpoint**, no el estado actual de la tabla.

### ML-FEAT-17 y la lista cerrada

Se comprueba que el evento permitido más reciente antes del checkpoint es el que se usa, que uno posterior no lo desplaza, que el respaldo sin eventos es la publicación y —esto importa— que mover `invitation_sent_at`, un timestamp real de la tabla que **no** está en la lista cerrada, no cambia nada.

## 5. Fallbacks

Los tres estados, con evidencia:

| Estado | Cuándo | Prueba |
|---|---|---|
| `predictive_available` | Todo el contrato se cumple | Servicio + checkpoint + plazo vigente |
| `descriptive_only` | Científicamente no corresponde inferir | Siete motivos distintos |
| `unavailable` | Servicio o contrato fallan | Conexión, timeout, 401/422/500/503, JSON ilegible, huella, umbral o `model_version` incorrectos |

**Nunca hay score inventado.** Una prueba recorre los casos sin predicción y verifica que `score`, `flag` y `threshold` son nulos. Ninguna ruta del flujo de reclutamiento depende del servicio.

## 6. Multiempresa

Dos organizaciones con vacantes, postulaciones, transiciones, evaluaciones y entrevistas. Se comprueba que:

- cada una obtiene sus propios conteos (3 y 7);
- añadir 27 registros a B **no mueve un solo campo** del vector de A;
- borrar B por completo tampoco;
- las vacantes concurrentes nunca cuentan otra organización;
- **sin sesión iniciada** —donde `OrganizationScope` no actúa— el aislamiento se mantiene, porque el builder filtra en cada consulta;
- el payload enviado para A lleva solo los conteos de A.

Y en la ruta: una vacante ajena responde **404**, igual que un identificador inexistente. Distinguirlos filtraría qué procesos tiene la otra organización.

## 7. Autorización

Comprobada recorriendo la ruta real, no solo contra la Policy: una Policy correcta con una ruta mal conectada seguiría dejando pasar a cualquiera.

| Rol | Resultado |
|---|---|
| RR. HH. | **200** |
| Aprobador | **200** |
| Evaluador | 403 |
| Área solicitante | 403 |
| Postulante | 403, incluso con postulación en el proceso |
| Invitado | 401 |
| Otra organización | 404, sin revelar existencia |

Una prueba compara Policy y ruta rol por rol, y otra falla si alguien añade un rol al sistema sin decidir su acceso.

## 8. Seguridad del servicio

| Ruta | Sin token configurado | Token incorrecto | Token correcto |
|---|---|---|---|
| `/health` | **200**, mínimo | **200** | **200** |
| `/v1/model-info` | **503** | **401** | **200** |
| `/v1/predict` | **503** | **401** | **200** |

Sin fugas de token, payload, PII, trazas, rutas locales ni ruta del artefacto, comprobado en las respuestas de error y en el panel.

## 9. `target_completion_at` extremo a extremo

| Capa | Estado |
|---|---|
| Migración reversible con `CHECK` | ✅ |
| Nullable, sin relleno inventado | ✅ |
| Posterior a `closes_at` | ✅ en base, FormRequest y navegador (`min`) |
| Captura en UI | ✅ `datetime-local`, probado en Cypress |
| Persistencia y recarga del formulario | ✅ |
| Resource y tipo TS | ✅ |
| Visualización en la ficha | ✅ |
| Inmutable tras publicar | ✅ el enlace de edición desaparece y entrar a mano redirige |

**Detalle encontrado en el navegador.** El `min` del campo hace que un plazo anterior al cierre quede inválido y el formulario **no llegue a enviarse**. Es mejor UX que un viaje al servidor, así que la prueba se ajustó a lo que realmente ocurre en lugar de forzar el comportamiento esperado; la regla equivalente del servidor se cubre en `TargetCompletionTest`.

## 10. UI mínima

El entorno E2E corre sin servicio ML, así que lo validado en navegador es el camino que más veces recorrerá alguien real: **el panel aparece, explica por qué no hay estimación y no inventa nada**. Sin predicción no se pinta porcentaje —un 0 % se leería como «riesgo nulo»—. El panel declara «Experimental», habla del **proceso** y no de las personas, y recuerda que la decisión final es del Aprobador.

Dos pruebas recorren el texto completo del panel: una descarta `ranking`, `mejor candidato`, `recomendamos`, `debe contratar`, `debe descartar` y `puntaje del postulante`; otra descarta `ALERTA CRÍTICA`, `RIESGO SEVERO`, `URGENTE` y `PELIGRO`. Con una tasa de alerta del 73.5 %, el tono alarmista sería desproporcionado.

El camino predictivo en navegador exigiría un servicio Python dentro de la infraestructura de E2E; queda cubierto por las pruebas de integración de Laravel y por el smoke real.

## 11. Smoke real

FastAPI en `0.0.0.0:8008` con token, Laravel en Docker vía `host.docker.internal`.

| Caso | Resultado |
|---|---|
| `/health` | `200`, `model_ready: true` |
| `/v1/model-info` sin token | **401** |
| `/v1/model-info` con token | **200**, `gap_01_open: false` |
| Vacante con plazo, checkpoint `2026-09-12` | Elegible |
| Consulta elegible | `predictive_available`, score 0.4411, `model_version` y huella verificados, 15 features |
| Servicio apagado | `unavailable`, `connection_failed`, score `null` |
| Sin `target_completion_at` | `descriptive_only`, `missing_target_completion_at` |
| Consulta tardía | `descriptive_only`, `query_after_target` |
| Token incorrecto | `unavailable`, `server_error`, respuesta descartada |
| Otro tenant | Policy niega y la vacante no es visible; su propio RR. HH. sí la ve |
| **Vector tras eventos posteriores** | **Idéntico**: 9 postulaciones en la tabla, **5 en el vector** |

Servidores detenidos y datos ficticios eliminados.

## 12. Resultados

| Suite | Resultado | Duración |
|---|---|---|
| **Laravel** | **402 pasan**, 0 fallos, **8 saltadas** | ~47 s |
| **Python** | **532 pasan**, 0 fallos, **0 avisos**, **98 %** cobertura | ~114 s |
| **Cypress** | **16 specs, 55 pruebas**, todas pasan | ~4 min 28 s |
| `npx tsc --noEmit` | exit 0 | — |
| `npm run build` | correcto | ~20 s |
| `php artisan optimize:clear` | correcto | — |
| `git diff --check` | limpio | — |

**Las 8 pruebas saltadas** son las de soporte E2E (`/__e2e/*`), que se omiten porque `E2E_ENABLED=false` en el entorno de desarrollo: esos endpoints solo existen en el servicio aislado `app-e2e`. Es el comportamiento esperado y previo a esta fase.

## 13. GAP-01 y RF-29

**GAP-01: RESUELTO TÉCNICAMENTE.** La columna existe, es auditable, inmutable tras publicar y capturable desde la interfaz. **No equivale a validación institucional.**

**RF-29:**

- ✅ implementado experimentalmente (Fase 15);
- ✅ integrado internamente (Fase 16);
- ✅ **validado técnicamente en entorno de pruebas** (Fase 17);
- ❌ **no validado institucionalmente**;
- ❌ **no autorizado para producción**;
- ✅ la decisión final es humana (RF-23), y nada de esta fase la toca.

## 14. Limitaciones que permanecen

Ninguna de estas la resuelve una fase de QA:

1. **Datos 100 % sintéticos.** Es la limitación dominante: el desempeño en el Colegio Andino es desconocido.
2. **Tasa de alerta 73.5 %** en test, sin coste de revisión modelado.
3. **Heterogeneidad por organización**: AP entre 0.476 y 0.840, con la organización peor evaluada en n=67.
4. **Censura informativa** por diseño: el supervisado está sesgado hacia procesos que cerraron.
5. **Colinealidad fuerte**: los coeficientes no son interpretables como importancia.
6. **`concurrent_open_vacancies_count`** puede actuar como proxy temporal.
7. **Contaminación procedimental menor**, documentada en la Fase 15B.
8. **Sin validación institucional.**
9. **Token compartido interno**: apropiado para red interna, insuficiente si el servicio saliera de ahí.
10. **Llamada síncrona** de hasta 3 s por consulta.
11. **Sin caché.**

## 15. Riesgos residuales

1. **Checkpoint único.** El modelo solo observa el día siguiente al cierre. Fuera de esa ventana no hay estimación, y dentro de ella el valor no cambia con el tiempo. Un seguimiento continuo exigiría reentrenar con checkpoints múltiples.
2. **El camino predictivo no se prueba en navegador.** Requiere FastAPI dentro de la infraestructura de E2E.
3. **`build_artifact.py` al 90 %**: cuatro ramas defensivas de incoherencia dataset↔freeze sin prueba.
4. **Validación cruzada de una sola instancia.** No hay pruebas de concurrencia ni de carga sobre el servicio.
5. **La auditoría de esta fase la ejecutó quien escribió el código**, igual que en la Fase 15D. Una revisión independiente sigue siendo más fuerte.

## Enlaces

- Integración: [`phase-16-laravel-ml-integration.md`](phase-16-laravel-ml-integration.md)
- Servicio: [`phase-15c-fastapi-service.md`](phase-15c-fastapi-service.md)
- Experimento: [`phase-15b-training-evaluation.md`](phase-15b-training-evaluation.md)
- Contrato de features: [`ml/feature-contract.md`](ml/feature-contract.md)
- Suite E2E: [`../testing/cypress-e2e.md`](../testing/cypress-e2e.md)
