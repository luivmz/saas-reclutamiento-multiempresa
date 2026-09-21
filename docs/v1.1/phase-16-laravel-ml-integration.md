# Fase 16 — Integración Laravel ↔ FastAPI

**Fecha:** 21 de septiembre de 2026
**Rama:** `feature/phase-16-laravel-ml-integration` · **Base:** `485f0e12` (`develop`, Fase 15 cerrada)
**Writer principal:** Claude Code · **Reviewer:** Codex (auditoría posterior)

> **`GAP-01` queda resuelto** del lado de Laravel: `vacancies.target_completion_at` existe y `days_remaining_to_target` es computable. **El servicio sigue siendo experimental**: el modelo se validó solo con datos sintéticos, y ninguna respuesta decide nada. La decisión final pertenece al Aprobador/Dirección (RF-23).

---

## 1. Qué se integró

La cadena completa ya existe:

```
React/Inertia → Laravel → HTTP interno → FastAPI → scikit-learn
```

La Fase 15C dejó el tramo final. Esta fase construye los tres anteriores: el cálculo de features desde el dominio real, el cliente HTTP con validación de la respuesta, y la presentación mínima.

Lo que **no** se hizo, por estar fuera de alcance: rediseño visual, animaciones, 3D, Docker del servicio ML, Redis, colas, despliegue en la nube y cualquier forma de *scoring* de personas.

## 2. GAP-01 resuelto

### La decisión

`ML-FEAT-02` (`days_remaining_to_target`) era la única feature del núcleo sin fuente en Laravel. Ahora la tiene: **`vacancies.target_completion_at`**, un `timestamp` nullable.

Tres decisiones, cada una con su consecuencia:

| Decisión | Por qué |
|---|---|
| Vive en `vacancies`, no en `job_requests` | La unidad que el modelo puntúa es el proceso de la vacante, donde ya están `published_at`, `closes_at` y `positions`. La Fase 14 **descartó** `job_requests.required_by`: es cuándo el área pide cubrir el puesto, no un compromiso de cierre del proceso |
| Es nullable y **no se rellena** | Las vacantes existentes no tienen plazo y no se les inventa uno. Fabricar un valor por retrocompatibilidad contaminaría justo la feature que justifica la fase. Quedan con panel descriptivo |
| **Inmutable tras publicar** | Es lo que hace utilizable a la feature. Si el plazo pudiera correrse durante el proceso, se movería la meta cada vez que hubiera retraso, la feature filtraría información del desenlace y el contrato la prohibiría |

### La migración

`database/migrations/2026_09_21_000001_add_target_completion_at_to_vacancies.php`

- añade la columna después de `closes_at`;
- impone en la base `CHECK (target_completion_at IS NULL OR closes_at IS NULL OR target_completion_at > closes_at)`;
- es **reversible**: `down()` elimina la restricción y la columna;
- no toca datos de ninguna organización.

### Reglas del plazo

| Regla | Dónde vive |
|---|---|
| Posterior al cierre de postulaciones | `CHECK` en la tabla **y** `after:closes_at` en `VacancyFormRequest` |
| Opcional | Sin él la vacante funciona igual; solo se queda sin estimación |
| Editable solo en borrador | `VacancyService::update()` ya rechaza cualquier cambio fuera de borrador; `Vacancy::targetCompletionIsEditable()` lo expone |
| Auditable | `AuditLogger` registra su valor en `vacante.registrada` y `vacante.configurada`, así que su inmutabilidad es comprobable y no solo declarada |
| Acotado al tenant | La vacante ya pertenece a una organización; la policy y el scope global hacen el resto |

## 3. Cálculo de features

`app/Services/Ml/OperationalRiskFeatureBuilder.php` produce **exactamente** las 15 features de `docs/v1.1/ml/feature-contract.md`, con las fuentes reales del dominio:

| Feature | Fuente |
|---|---|
| `elapsed_days_since_publication` | `vacancies.published_at` |
| `application_window_days` | `closes_at − opens_at`, con respaldo en `published_at` |
| `positions_count` | `vacancies.positions` |
| `applications_received_count` | `applications.applied_at ≤ checkpoint` |
| `configured_criteria_count` | `evaluation_criteria` |
| `evaluations_scheduled/completed/overdue_pending_count` | `evaluations` |
| `interviews_scheduled/completed/overdue_pending_count` | `interviews` |
| `stage_transition_count` | `application_stage_histories`, **total sin desagregar** |
| `days_since_last_operational_event` | máximo de una lista **cerrada** de eventos |
| `concurrent_open_vacancies_count` | `vacancies` de la misma organización abiertas en el checkpoint |
| `days_remaining_to_target` | `target_completion_at − checkpoint` |

Tres reglas gobiernan el archivo entero:

1. **Truncado al checkpoint.** Ningún conteo mira más allá del instante de observación.
2. **Scoping explícito por organización.** `OrganizationScope` solo filtra cuando hay sesión; en consola o en cola no hace nada. Cada consulta repite el filtro a propósito: la multiempresa no puede depender de que exista sesión. Hay una prueba que corre **sin autenticar** y comprueba que las filas ajenas no se cuentan.
3. **Cero datos de personas.** `interviews.outcome`, `evaluation_results.score`, `evaluator_id` y `candidate_id` no se leen. Dos pruebas lo fijan: cambiar el `outcome` de una entrevista o el estado destino de una transición **no altera el vector**.

`OperationalRiskFeatures` rechaza cualquier conjunto que no sea exactamente esas 15 claves, así que un identificador no puede colarse ni por descuido.

## 4. Alcance del modelo: cuándo Laravel **no** pregunta

El experimento observó siempre el mismo instante: el día siguiente al cierre de postulaciones. Preguntar en otro punto es extrapolar, y un número obtenido así aparentaría un rigor que no tiene. `OperationalRiskService` devuelve el panel descriptivo, sin llamar al servicio, cuando:

| Situación | `reason` |
|---|---|
| La vacante no está publicada | `vacancy_not_published` |
| No hay `target_completion_at` | `missing_target_completion_at` |
| Las postulaciones siguen abiertas | `application_window_still_open` |
| El plazo objetivo ya venció | `target_completion_reached` |

El último merece explicación: el contrato del servicio exige `days_remaining_to_target ≥ 1`, y **el valor no se recorta a uno**. Un plazo vencido describe un proceso que el modelo nunca vio, porque el dataset solo contiene plazos futuros. Falsear el número aquí fabricaría exactamente la feature que justifica toda la integración.

Es una restricción deliberada, revisable si una fase futura entrena con checkpoints múltiples.

## 5. Cliente HTTP

`app/Services/Ml/MlRiskClient.php`, sobre el cliente HTTP de Laravel.

### No confía en la respuesta

Que el servicio conteste `200` no significa que esté sirviendo el modelo auditado. Antes de aceptar una predicción se comprueba:

- presencia de `risk_score`, `risk_flag`, `threshold`, `model_version` y `freeze_fingerprint`;
- `risk_score` numérico, finito y en **[0, 1]**;
- `risk_flag` booleano de verdad;
- **`freeze_fingerprint` idéntica** a `9ee18430…`, comparada con `hash_equals`;
- **`threshold` idéntico** a `0.1679418172266036` — su versión redondeada se rechaza, porque clasifica distinto en la frontera;
- `status` sigue siendo `experimental`;
- coherencia interna: `risk_flag == (risk_score >= threshold)`.

Cualquier discrepancia descarta la respuesta y el panel cae a `unavailable`.

### Modos de fallo

| Situación | Resultado | `reason` |
|---|---|---|
| Integración desactivada | `descriptive_only` | `service_disabled` |
| Conexión rechazada | `unavailable` | `connection_failed` |
| Timeout | `unavailable` | `timeout` |
| `503` | `unavailable` | `model_unavailable` |
| `422` | `unavailable` | `payload_rejected` |
| `401`, `500`, otro error | `unavailable` | `server_error` |
| Cuerpo ilegible | `unavailable` | `invalid_json` |
| Contrato incompatible | `unavailable` | `incompatible_contract` |

**El cliente no lanza excepciones hacia arriba.** El reclutamiento no puede depender de que el servicio esté sano.

### Tiempos y reintentos

Connect 1 s, request 3 s: una estimación es información auxiliar y no debe hacer esperar a nadie en el flujo principal. **Un reintento como máximo y solo ante fallos de conexión**; un `422` o un `503` no mejoran por repetirlos y solo añaden latencia y carga a un servicio que ya está mal.

## 6. Fallback

Tres estados, y ninguno inventa un número:

| Estado | Significado |
|---|---|
| `predictive_available` | Hay estimación verificada contra el experimento aprobado |
| `descriptive_only` | El proceso queda fuera del alcance del modelo, o falta el plazo |
| `unavailable` | El servicio no respondió, o respondió algo inaceptable |

Cuando no hay predicción, `risk_score`, `risk_flag` y `threshold` son **nulos**, y esa nulidad llega hasta la interfaz. Un cero se leería como «riesgo nulo», que es una afirmación que nadie ha medido.

**La selección humana nunca se bloquea.** Ninguna ruta del flujo de reclutamiento depende del servicio.

## 7. Seguridad

### Token de servicio a servicio

`ml-service/src/recruitment_ml/api/security.py`. Un secreto compartido, proporcionado al problema: los dos extremos son componentes del mismo despliegue y no hay usuarios que autenticar en FastAPI — ese boundary es Laravel.

- el secreto vive **solo en el entorno** (`ML_SERVICE_TOKEN` en Laravel, `RECRUITMENT_ML_INTERNAL_TOKEN` en FastAPI);
- nunca se versiona ni se registra en logs;
- comparación en **tiempo constante** (`hmac.compare_digest`), para que la latencia no filtre cuántos caracteres son correctos;
- protege `/v1/predict` y `/v1/model-info`;
- **`/health` queda abierto**: es una sonda de vida que devuelve estado, si hay modelo y la versión del componente — ni rutas, ni huellas, ni nada del experimento. Pedirle token complicaría los chequeos del despliegue sin proteger nada;
- sin variable definida la autenticación queda desactivada, admisible en desarrollo local, y el arranque lo **avisa en el log** para que nadie lo confunda con estar protegido.

Nada de esto convierte al servicio en publicable: sigue siendo experimental y debe permanecer en localhost o red interna.

### Registro sin PII

Se registran **categoría, estado HTTP y duración**. No se registran el payload —contiene el estado operativo de una vacante concreta—, la respuesta completa ni el token.

```
ml.risk.predict {"outcome":"ok","status":200,"duration_ms":28}
ml.risk.predict {"outcome":"incompatible_contract","status":200,"duration_ms":7,"detail":"fingerprint_mismatch"}
```

### Sin caché

Ninguna. La integración se mantiene simple y correcta; cachear una estimación introduce la pregunta de cuándo invalidarla, y no hay evidencia de que haga falta.

## 8. Multiempresa y autorización

| Garantía | Cómo |
|---|---|
| Features solo de la organización de la vacante | Filtro explícito en **cada** consulta del builder, además del scope global |
| Vacante ajena invisible | `OrganizationScope` → la vinculación de ruta devuelve **404** |
| Defensa en profundidad | `VacancyPolicy::viewOperationalRisk()` niega aunque alguien resolviera la vacante sin el scope |
| Solo roles de gestión | RR. HH. y Aprobador de la misma organización |
| Postulante y evaluador | **403**. No porque se les oculte una puntuación suya —el modelo no puntúa personas—, sino porque es información de gestión interna |

## 9. Presentación mínima

`resources/js/components/vacancies/operational-risk-card.tsx`, en la ficha de una vacante ya publicada.

Muestra: disponibilidad, distintivo **Experimental**, porcentaje de riesgo cuando lo hay, la señal, un mensaje humano, el momento de consulta y el recordatorio de que la decisión final es humana.

**No muestra**, y no debe: ranking de candidatos, puntuación de personas, recomendación automática, causalidad, «debe contratar» o «debe descartar».

### Tono

La tasa de alerta del modelo es del **73.5 %** en el conjunto de prueba. Presentar la señal como alarma crítica sería desproporcionado, así que el texto es «**Señal de riesgo para revisión**» y nunca «ALERTA CRÍTICA» ni «RIESGO SEVERO». Hay una prueba que lo verifica.

## 10. Configuración

`config/ml.php`, alimentado por entorno (`.env.example` trae los valores de referencia):

| Clave | Por omisión | Nota |
|---|---|---|
| `ML_SERVICE_ENABLED` | `false` | La integración se activa a conciencia |
| `ML_SERVICE_URL` | `http://127.0.0.1:8008` | Desde Docker: `http://host.docker.internal:8008`. **8008 y no 8001**: ese puerto ya lo ocupa `app-e2e` |
| `ML_SERVICE_CONNECT_TIMEOUT` / `ML_SERVICE_TIMEOUT` | `1.0` / `3.0` | Segundos |
| `ML_SERVICE_RETRIES` | `1` | Solo fallos de conexión |
| `ML_SERVICE_TOKEN` | vacío | Secreto; nunca un valor real en el repositorio |
| `ML_EXPECTED_FREEZE_FINGERPRINT` | `9ee18430…` | Identidad del experimento aprobado |
| `ML_EXPECTED_THRESHOLD` | `0.1679418172266036` | Umbral exacto |

## 11. Comandos

```bash
# 1. Artefacto del modelo (no se versiona)
cd ml-service
.venv/Scripts/python.exe -m recruitment_ml.serving.build_artifact

# 2. Servicio, con token
RECRUITMENT_ML_INTERNAL_TOKEN=<secreto> \
  .venv/Scripts/python.exe -m uvicorn recruitment_ml.api.app:app --host 0.0.0.0 --port 8008

# 3. Laravel
docker compose up -d --wait
docker compose exec app php artisan migrate --force

# 4. Pruebas
docker compose exec app php artisan test
cd ml-service && .venv/Scripts/python.exe -m pytest --cov=recruitment_ml --cov-report=term-missing
```

Para que Laravel llame al servicio, en `.env`: `ML_SERVICE_ENABLED=true`, `ML_SERVICE_URL=http://host.docker.internal:8008` y `ML_SERVICE_TOKEN` igual al del servicio.

## 12. Pruebas

**Laravel: 321 pruebas, 0 fallos** (236 previas + 85 nuevas + 8 saltadas). **Python: 527, 0 fallos, 0 avisos, 98 % de cobertura** (506 de la Fase 15 + 21 de autenticación).

| Archivo | Pruebas | Garantía |
|---|---|---|
| `tests/Feature/Ml/TargetCompletionTest.php` | 11 | GAP-01: esquema, `CHECK`, cast, validación, inmutabilidad tras publicar, auditoría, multiempresa |
| `tests/Feature/Ml/OperationalRiskFeatureBuilderTest.php` | 19 | Las 15 features exactas, valores, truncado al checkpoint, **sin PII**, `outcome` nunca leído, scoping sin sesión |
| `tests/Feature/Ml/MlRiskClientTest.php` | 31 | Éxito, timeout, conexión, 401/422/500/503, JSON inválido, huella y umbral incorrectos, score fuera de rango, reintentos |
| `tests/Feature/Ml/OperationalRiskServiceTest.php` | 12 | Predicción, los cuatro fallbacks, servicio caído, respuesta incompatible, tono neutro |
| `tests/Feature/Ml/VacancyOperationalRiskRouteTest.php` | 12 | Autorización por rol, cross-tenant, contenido de la respuesta, sin fugas |
| `ml-service/tests/test_api_security.py` | 21 | Token obligatorio, comparación constante, `/health` abierto, sin eco del secreto |

### Smoke de integración real

Ejecutado con FastAPI en `0.0.0.0:8008` y Laravel en Docker, con token:

| Caso | Resultado |
|---|---|
| Servicio disponible | `predictive_available`, score 0.6209, huella y umbral verificados |
| Sin `target_completion_at` | `descriptive_only`, score `null` — no se inventa |
| Huella incompatible | `unavailable`, `incompatible_contract`, respuesta descartada |
| Servicio apagado | `unavailable`, `connection_failed`, flujo intacto |
| Tenant incorrecto | Policy niega y la vacante ajena no es visible |

## 13. RF-29

**`integrated internally` — no productivo.**

- ✅ implementado experimentalmente (Fase 15);
- ✅ integrado internamente en Laravel (Fase 16);
- ⚠️ **limitado por validación sintética**: el modelo nunca vio datos reales, así que su desempeño en el Colegio Andino es desconocido;
- ⚠️ tasa de alerta alta (73.5 %), sin coste de revisión modelado;
- ⚠️ sin autenticación institucional ni despliegue productivo;
- ✅ la decisión final sigue siendo humana (RF-23), y nada en esta fase la toca.

## 14. Limitaciones

1. **Validación solo sintética.** Es la limitación dominante y no la resuelve ninguna integración.
2. **Checkpoint único.** El modelo observa el proceso tras el cierre de postulaciones; antes de eso, Laravel no pregunta.
3. **Tasa de alerta alta.** El punto de operación marca tres de cada cuatro procesos en test. El coste de revisar cada señal no está modelado.
4. **Un solo tenant de entrenamiento.** El dataset es sintético y sus organizaciones son ficticias; la heterogeneidad observada (AP 0.476–0.840) sugiere que el desempeño por organización puede variar bastante.
5. **Sin caché ni cola.** Cada consulta es una llamada sincrónica de hasta 3 s. Con volumen alto habría que revisarlo.
6. **Autenticación mínima.** Un token compartido es apropiado para red interna; no sustituye a autenticación institucional si el servicio saliera de ahí.
7. **El servicio no debe exponerse públicamente.** Sigue sin haber autorización de despliegue.

## Enlaces

- Experimento: [`phase-15b-training-evaluation.md`](phase-15b-training-evaluation.md)
- Servicio: [`phase-15c-fastapi-service.md`](phase-15c-fastapi-service.md)
- Contrato de features: [`ml/feature-contract.md`](ml/feature-contract.md)
- Model card: [`ml/model-card-draft.md`](ml/model-card-draft.md)
