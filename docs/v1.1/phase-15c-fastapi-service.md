# Fase 15C — Servicio FastAPI experimental

**Fecha:** 20 de septiembre de 2026
**Rama:** `feature/phase-15-ml-service` · **Base 15B:** `a36bdb8`
**Writer principal:** Claude Code · **Reviewer:** Codex (auditoría posterior)
**Alcance:** solo el servicio Python. **Laravel no consume este servicio todavía.**

> **Servicio experimental, sin autorización de despliegue.** `GAP-01` sigue abierto: `target_completion_at` no existe en Laravel, así que `days_remaining_to_target` **no es computable en producción**. RF-29 continúa siendo candidato y 15C no lo cierra.

---

## 1. Objetivo

Servir por HTTP el modelo que la Fase 15B congeló, sin tocar ninguna de sus decisiones científicas y sin integrarse con Laravel.

Lo que el servicio **sí** hace: comprobar su propio estado, publicar los metadatos del modelo y estimar la probabilidad de retraso operacional de **un** proceso de vacante.

Lo que **no** hace, por diseño: no accede a la base de datos de Laravel, no autentica usuarios, no ordena candidatos, no decide nada, no guarda peticiones ni predicciones y no almacena PII.

## 2. Contrato arquitectónico

La cadena prevista es:

```
React/Inertia → Laravel → HTTP interno → FastAPI → scikit-learn
```

**En 15C solo existe el tramo final, `FastAPI → scikit-learn`.** El cliente HTTP en Laravel, la autenticación servicio-a-servicio y la UI pertenecen a la Fase 16. El monolito modular sigue siendo el sistema; el servicio Python es un componente separado que todavía no tiene consumidor.

## 3. Estructura

```
ml-service/src/recruitment_ml/
├── api/
│   ├── app.py            aplicación FastAPI, lifespan y rutas
│   ├── schemas.py        contrato de entrada y salida (Pydantic)
│   ├── dependencies.py   estado del modelo durante la vida del proceso
│   └── errors.py         traducción de errores a respuestas seguras
└── serving/
    ├── build_artifact.py reconstrucción del modelo desde el freeze
    ├── loader.py         carga verificada contra el protocolo congelado
    ├── metadata.py       metadatos del artefacto y del servicio
    ├── paths.py          rutas del artefacto local y del freeze
    └── predictor.py      inferencia sin estado
```

La separación no es decorativa: `serving/` puede usarse sin FastAPI —y las pruebas lo hacen—, y `api/` no sabe nada de scikit-learn.

## 4. El artefacto y cómo se construye

La Fase 15B **no versionó binarios**, y esa decisión se mantiene: un `.joblib` en el repositorio es un objeto opaco que nadie puede auditar. Lo que sí está versionado es el protocolo congelado, y de él se deriva el modelo:

```
python -m recruitment_ml.serving.build_artifact
```

El comando:

1. lee `docs/v1.1/ml/phase-15b-experiment-freeze.json` y comprueba su integridad;
2. regenera el dataset sintético con la semilla y las filas del experimento;
3. **verifica que `model_ready_fingerprint` y `config_fingerprint` coinciden** con los del freeze — si no, el modelo no sería el mismo;
4. rehace la partición temporal y comprueba también su firma;
5. toma **solo `train`** y ajusta `StandardScaler` + `LogisticRegression` con los hiperparámetros congelados;
6. escribe el artefacto y sus metadatos.

No elige modelo, no ajusta hiperparámetros, no toca el umbral y **no abre el conjunto de prueba**: servir un modelo no es motivo para volver a mirarlo.

| Salida | Ruta | Versionado |
|---|---|---|
| Modelo | `ml-service/artifacts/model/risk_model.joblib` | **No** (`.gitignore:51`) |
| Metadatos | `ml-service/artifacts/model/risk_model.metadata.json` | **No** |

`RECRUITMENT_ML_ARTIFACT_DIR` permite apuntar a otro directorio. No acepta secretos ni credenciales.

## 5. Metadatos del artefacto

El binario por sí solo no dice de qué experimento salió. Los metadatos son el puente entre el `.joblib` local y el freeze versionado:

`schema_version` (`15c.1`) · `experiment_id` · `freeze_fingerprint` · `dataset_fingerprint` · `config_fingerprint` · `model_family` y `model_params` · `preprocessing` · `feature_set` y `feature_order` · **`threshold` exacto** · `seed` · `rows` · `n_train` · `built_at` · `library_versions`.

Las versiones de biblioteca se registran porque un artefacto serializado por una versión de scikit-learn y cargado por otra puede comportarse de forma distinta.

## 6. Carga verificada

Cargar un `.joblib` y confiar en él sería el error que la Fase 15B pasó tres correcciones evitando en el freeze. El loader aplica el mismo criterio y **rechaza** si:

- falta el artefacto o faltan sus metadatos;
- los metadatos son ilegibles, incompletos o traen campos desconocidos;
- `schema_version` no es el vigente;
- `freeze_fingerprint`, `experiment_id`, `model_family`, `dataset_fingerprint` o `feature_set` no coinciden con el freeze;
- el umbral no es el congelado;
- el orden de features no es el del conjunto congelado, o no coincide con el declarado en el freeze;
- el binario está corrupto o el objeto cargado no expone `predict_proba`;
- el freeze falta o fue alterado.

Si algo falla, **el servicio no finge estar listo**: sigue vivo, lo declara en `/health` y las rutas que necesitan el modelo responden 503.

## 7. Endpoints

### `GET /health`

Distingue **proceso vivo** de **modelo listo**, que no son lo mismo.

```json
{ "status": "ok", "model_ready": true, "version": "0.1.0", "detail": null }
```

Sin modelo: `model_ready: false` y `detail: "modelo no cargado"`. Nunca rutas locales ni trazas.

### `GET /v1/model-info`

Metadatos técnicos del modelo servido: familia, `experiment_id`, huella del freeze, umbral exacto, orden de features, **veredicto `PREDICTIVE GO WITH LIMITATIONS`**, `deployment_status: experimental`, `gap_01_open: true` y qué significan `risk_score` y `risk_flag`.

No devuelve datos de entrenamiento, filas individuales, PII ni rutas locales. Sin modelo cargado: **503**.

### `POST /v1/predict`

Acepta **exactamente** las 15 features model-ready del contrato de 15B, y nada más.

```json
{
  "risk_score": 0.4231,
  "risk_flag": true,
  "threshold": 0.1679418172266036,
  "model_version": "phase-15b-20260920-6000",
  "freeze_fingerprint": "9ee1843055e75d4039dd84fd666db7a594e1a45ec7e9b354820fabfcb21ebcd2",
  "status": "experimental"
}
```

## 8. Qué significa `risk_score`, y qué no

`risk_score` es la **probabilidad estimada de retraso operacional del proceso de la vacante**. No evalúa, no puntúa y no clasifica personas. No es —ni puede llamarse— *candidate score*, *suitability*, *selection score* ni *hiring score*.

`risk_flag` es literalmente `risk_score >= threshold`. Es una **señal operativa para revisión humana**: no es una decisión, ni una recomendación de contratación, ni un descarte, ni un ranking, ni dispara ninguna acción automática. La decisión final pertenece al Aprobador/Dirección, con confirmación humana explícita (RF-23).

## 9. Validación de entrada

Dos decisiones del esquema, ambas deliberadas:

- **`extra="forbid"`.** Un campo de más no es un descuido inocente: es la vía por la que entrarían `vacancy_id`, `candidate_id`, un correo o una edad. Rechazar lo desconocido convierte el contrato de features en una **frontera efectiva** y no en una recomendación.
- **`strict=True`.** En modo laxo Pydantic convertiría `"12"` en `12` y `3.5` en `3`. Las features son conteos y diferencias de días enteras; aceptar una cadena o un decimal silenciaría un error del cliente.

Los límites **provienen del contrato sintético aprobado**, no de supuestos institucionales: enteros no negativos, `days_remaining_to_target ≥ 1` porque el plazo es posterior al checkpoint, y un tope para los campos en días derivado del periodo máximo que admite `SyntheticConfig` (180 meses).

Se rechazan con **422**: campos faltantes, campos desconocidos, identificadores, atributos personales o de resultado, tipos incorrectos, decimales donde van enteros, `NaN`, `Infinity`, negativos y valores fuera de rango.

**El cuerpo del 422 no devuelve el valor recibido.** El manejador por omisión de FastAPI lo incluye; aquí se sustituye por `field`, `message` y `type`. Tiene un motivo práctico —un `NaN` en el payload no es serializable y la respuesta de error reventaría al codificarse— y uno de criterio: si alguien manda por error un dato personal en un campo prohibido, devolvérselo lo copiaría a los logs del cliente y a cualquier intermediario.

## 10. Orden de features

El JSON conserva el orden de inserción, así que construir la matriz con el orden del payload haría que dos peticiones equivalentes produjeran predicciones distintas. **El predictor reindexa siempre por `feature_order`**, el orden congelado. Hay pruebas específicas —a nivel de predictor y de endpoint— que envían el mismo payload en orden invertido y exigen idéntica respuesta.

## 11. Errores

| Situación | Código | Cuerpo |
|---|---|---|
| Payload inválido | **422** | `validation_error`, con `field`/`message`/`type`; sin el valor recibido |
| Artefacto ausente o incompatible | **503** | `model_unavailable`, con la instrucción de reconstruirlo |
| Fallo inesperado de inferencia | **500** | `inference_failed`, categoría sin detalle |

Regla: **el cliente recibe la categoría, los registros internos reciben el detalle.** Una traza o una ruta local en la respuesta convierte un fallo en información útil para quien no debería tenerla; ocultarla también en los logs haría imposible diagnosticar nada.

## 12. Arranque

El modelo se carga **una vez**, mediante el `lifespan` de FastAPI —no las APIs obsoletas de `startup`/`shutdown`—. Entrenar o deserializar por petición convertiría cada llamada en segundos de CPU.

Un fallo de carga **no tumba el proceso**: el servicio sigue vivo y lo declara, que es más útil para diagnosticar que un contenedor en bucle de reinicio.

La inferencia es *stateless*. El pipeline ajustado solo se consulta, así que no hace falta sincronización, y el servicio no necesita base de datos.

## 13. Seguridad de esta fase

No se implementa autenticación: **Laravel será el boundary de aplicación en la Fase 16** y ningún contrato aprobado exige otra cosa en 15C. No hay API keys en el código, y no las habrá inventadas.

Lo que sí está puesto ahora:

- **sin CORS.** El consumidor será Laravel por red interna, no un navegador;
- validación estricta del payload, que acota también su forma;
- sin eco del input en los errores;
- sin trazas ni rutas en las respuestas;
- documentación explícita de que **no debe exponerse públicamente**: `127.0.0.1` o red interna.

## 14. Comandos

```bash
cd ml-service

# dependencias
.venv/Scripts/python.exe -m pip install -e ".[dev]"

# construir el artefacto (no se versiona)
.venv/Scripts/python.exe -m recruitment_ml.serving.build_artifact

# levantar el servicio en local
.venv/Scripts/python.exe -m uvicorn recruitment_ml.api.app:app --host 127.0.0.1 --port 8001

# pruebas
.venv/Scripts/python.exe -m pytest
.venv/Scripts/python.exe -m pytest --cov=recruitment_ml --cov-report=term-missing
```

Ejemplo ficticio de petición:

```bash
curl -X POST http://127.0.0.1:8001/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"elapsed_days_since_publication":34,"application_window_days":21,
       "positions_count":2,"applications_received_count":18,
       "configured_criteria_count":5,"evaluations_scheduled_count":12,
       "evaluations_completed_count":7,"evaluations_overdue_pending_count":2,
       "interviews_scheduled_count":6,"interviews_completed_count":3,
       "interviews_overdue_pending_count":1,"stage_transition_count":9,
       "days_since_last_operational_event":4,"concurrent_open_vacancies_count":5,
       "days_remaining_to_target":12}'
```

## 15. Pruebas

**480 pruebas, 0 fallos, 0 avisos, 98 % de cobertura.** Las 388 anteriores siguen pasando; 92 son nuevas. Los módulos `api/` y `serving/` quedan al 100 %, salvo `build_artifact.py` (90 %: ramas defensivas de incoherencia entre dataset y freeze).

| Archivo nuevo | Pruebas | Garantía |
|---|---|---|
| `test_api_service.py` | 51 | Endpoints extremo a extremo: health, metadata, predicción, validación, identificadores y atributos personales rechazados, 503 sin modelo, 500 sin traza, OpenAPI, sin CORS |
| `test_serving_artifact.py` | 34 | Construcción derivada del freeze, metadatos, carga verificada, mismatches, artefacto corrupto, determinismo, orden de features |
| `test_serving_cli.py` | 7 | Comando de construcción, guarda del esquema y ramas restantes |

Las pruebas de API atraviesan la aplicación entera con `TestClient`: probar las funciones sueltas dejaría fuera precisamente lo que puede fallar en un servicio.

## 16. Límites de la fase

1. **No es producción** y no hay autorización de despliegue.
2. **Laravel no consume el servicio.** El cliente HTTP, la autenticación servicio-a-servicio y la UI son Fase 16.
3. **`GAP-01` sigue abierto.** El endpoint acepta `days_remaining_to_target` porque existe en el contrato ML sintético, pero **Laravel todavía no puede producir esa feature**: `target_completion_at` no existe. Por tanto `/v1/predict` **no está autorizado para integración productiva**.
4. **El modelo arrastra las limitaciones de 15B**: datos 100 % sintéticos, tasa de alerta alta (73.5 % en test), heterogeneidad por organización, censura informativa, colinealidad, `concurrent_open_vacancies_count` como posible proxy temporal y contaminación procedimental menor. El veredicto sigue siendo `PREDICTIVE GO WITH LIMITATIONS`.
5. **Sin Docker, Redis, colas, jobs ni despliegue.** No pertenecen a esta fase.

## Enlaces

- Experimento congelado: [`phase-15b-training-evaluation.md`](phase-15b-training-evaluation.md)
- Model card: [`ml/model-card-draft.md`](ml/model-card-draft.md)
- Protocolo: [`ml/phase-15b-experiment-freeze.json`](ml/phase-15b-experiment-freeze.json)
- Componente Python: [`../../ml-service/README.md`](../../ml-service/README.md)
