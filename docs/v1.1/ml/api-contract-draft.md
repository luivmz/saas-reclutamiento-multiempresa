# Contrato Laravel ↔ servicio de inferencia — BORRADOR

**Fase 14 · 20 de septiembre de 2026**

**[LIMITACIÓN] No existe servicio, endpoint, cliente ni dependencia.** Este documento es una **propuesta** de diseño, no un contrato definitivo. Se revisa y se cierra en la fase de integración.

---

## 1. Flujo

```
React / Inertia
    ↓
Laravel  — auth, roles, tenant, reglas de negocio, SYSTEM OF RECORD,
           ensamblado del vector de features
    ↓  HTTP interno versionado, sin PII
FastAPI  — validación del vector + inferencia sin estado
    ↓
modelo scikit-learn versionado
```

### Qué hace cada lado

| Laravel | Servicio de inferencia |
|---|---|
| Autentica y autoriza al usuario final | **No** autentica usuarios finales |
| Resuelve la multitenencia | **No** conoce `organization_id` |
| Aplica las reglas de negocio | **No** conoce el dominio |
| Lee y escribe PostgreSQL | **No** accede a ninguna base de datos |
| Decide qué mostrar y qué guardar | **No** escribe estados ni decide nada |
| Ensambla el vector con la regla del checkpoint | Valida el vector y devuelve un número |

**[PROPUESTA]** «Sin autenticación de usuario final» **no** significa endpoint desprotegido. La autenticación servicio-a-servicio, la exposición solo en red interna y el aislamiento del contenedor son **decisión de arquitectura pendiente** de la fase de integración.

---

## 2. Endpoint

**[PROPUESTA]** `POST /v1/predict`, versionado en la ruta y no `/predict` a secas: un cambio del contrato de features rompe compatibilidad y debe poder convivir con la versión anterior mientras Laravel migra.

Complementos propuestos: `GET /v1/health` (vivacidad y versión de modelo cargada) y `GET /v1/model-info` (versión, hash, fecha de entrenamiento).

---

## 3. Entrada conceptual

**[PROPUESTA]**

| Campo | Regla |
|---|---|
| `schema_version` | Obligatorio. Si Laravel y el servicio no coinciden, el servicio rechaza con error de esquema y Laravel aplica el fallback |
| Features operacionales | Nombres y tipos exactos del contrato de features; enteros no negativos; rangos validados |
| `days_remaining_to_target` | **[PENDIENTE]** Laravel **no puede calcularla hoy**: depende de `GAP-01`. Mientras la brecha siga abierta, la integración de este contrato está bloqueada aunque el experimento tenga éxito |
| Prohibido | PII, texto libre, identificadores de persona, `vacancy_id`, `organization_id`, cualquier campo fuera del contrato |

Reglas de validación mínimas: todas las features requeridas presentes; tipos correctos; `elapsed_days_since_publication > 0`; `application_window_days >= 0`; todos los conteos `>= 0`; `completed <= scheduled`; `overdue_pending <= pending`; y, si el target fue aprobado, `days_remaining_to_target > 0`. Un vector que no cumpla se rechaza: **no se imputa en silencio**.

---

## 4. Salida conceptual

**[PROPUESTA]** Forma propuesta, sin valores de ejemplo que puedan leerse como una inferencia real:

```json
{
  "schema_version": "<string>",
  "model_version": "<string>",
  "risk_probability": "<float en [0,1]>",
  "risk_level": "<string|null>",
  "thresholds_version": "<string|null>",
  "factors": [
    {
      "feature": "<id del contrato de features>",
      "direction": "increases|decreases",
      "label": "<etiqueta operacional legible>"
    }
  ],
  "limitations": ["synthetic-data experimental estimate"]
}
```

Reglas:

- `risk_probability` es la probabilidad **calibrada**, siempre presente.
- `risk_level` es `null` mientras no se hayan determinado experimentalmente los umbrales en la Fase 15 (decisión 8); **nunca** se inventa una categoría.
- `thresholds_version` acompaña obligatoriamente a cualquier `risk_level` no nulo.
- `factors` contiene solo IDs del contrato de features y etiquetas operacionales. **Nunca** nombres de personas, puntajes, universidad, CV, resultado de entrevista, ranking ni decisión.
- `limitations` viaja siempre y se muestra al usuario: la estimación es sintética y experimental.

### Categorías de error conceptuales

| Situación | Respuesta del servicio | Reacción de Laravel |
|---|---|---|
| Vector inválido o incompleto | 4xx con detalle de campo | Fallback; registrar como defecto de ensamblado |
| `schema_version` incompatible | 4xx de esquema | Fallback; alertar al equipo: hay que migrar |
| Modelo no cargado | 5xx | Fallback |
| Error interno | 5xx | Fallback |
| Timeout, DNS o conexión | — | Fallback |
| JSON inválido o probabilidad fuera de `[0,1]` | — | Fallback; tratar como respuesta corrupta |

---

## 5. Fallback y disponibilidad

**[PROPUESTA]** Requisitos para la fase de integración:

1. **Timeout corto y configurable.** **[PENDIENTE]** El valor se fija tras medir latencia real; no se inventa hoy.
2. **Manejo explícito** de DNS, conexión, timeout, 4xx, 5xx, JSON inválido, esquema incompatible y probabilidad fuera de rango.
3. **Fallback silenciosamente seguro:** la pantalla se renderiza completa **sin** la estimación. Nunca un error al usuario por culpa del componente opcional.
4. **Mensaje informativo, no alarmista y accesible**, del tipo «estimación no disponible en este momento».
5. **Nunca bloquear RF-01 a RF-27.** Ningún flujo existente depende del servicio.
6. **Logging estructurado sin PII:** `model_version`, resultado técnico, latencia y correlation ID. **[PROPUESTA]** No se registra el vector completo si eso aumenta el riesgo de reidentificación.
7. **Reintentos solo para fallos transitorios**, con presupuesto total acotado que **no** exceda el timeout percibido por el usuario. Sin reintentos en cascada.
8. **Circuit breaker y caché** solo si una fase posterior demuestra que hacen falta. No se añaden por anticipado.
9. **Ninguna escritura automática** en postulaciones, ranking, decisión ni selección.

### Pruebas futuras en Laravel

**[PROPUESTA]** Con `Http::fake()`, sin red: respuesta válida; respuesta inválida; probabilidad fuera de rango; timeout; 5xx; servicio caído. Las tres últimas deben demostrar que **la pantalla sigue funcionando completa**.

### SLA

**[PENDIENTE]** No se fija ninguna cifra. Se medirá latencia p50/p95 en la fase de integración y solo entonces se propondrá un objetivo. Un SLA inventado hoy sería una afirmación sin respaldo.

## Enlaces

- [Definición del problema](problem-definition.md) · [Contrato de features](feature-contract.md) · [Plan de evaluación](evaluation-plan.md) · [ADR-001 Frontera del ML](../architecture-decisions/ADR-001-ml-boundary.md) · [Índice de la Fase 14](../phase-14-ml-definition.md)
