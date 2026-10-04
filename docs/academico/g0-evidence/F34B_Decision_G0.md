# F34B — Decisión G0

> Fase F34B, versión 1 (04/10/2026). Reevaluación de los 15 criterios con la evidencia recibida. **Ningún documento ni validador aprueba G0 automáticamente:** este documento solo aplica la regla de [ADR-005 §9.1](../diseno-inteligente/F33_ADR_005_G0.md#91-estados-y-regla-de-decisión) a la [matriz de evidencias](F34B_Matriz_Evidencias_G0.md).

## 1. Resultado

- **G0 = NO APROBADA.**
- **ADR-005 = PROPUESTA.**
- **F35–F40 = BLOQUEADAS.**
- **Alcance C: no habilitado.**
- **Los datos reales siguen PROHIBIDOS.**
- RF-23 sigue humana; RF-29 sigue experimental e informativa.
- F34B = LISTA PARA AUDITORÍA.

**Motivo:** no se recibió ninguna evidencia externa. Faltan G0-02, G0-03, G0-12 y G0-14 (PENDIENTE EXTERNO) y la aceptación de G0-09 (PARCIAL).

## 2. Reevaluación de los 15 criterios

| Criterio | Estado F34A | Evidencia nueva en F34B | Estado F34B |
|---|---|---|---|
| G0-01 | CUMPLIDO | — | CUMPLIDO |
| G0-02 | PENDIENTE EXTERNO | Ninguna | PENDIENTE EXTERNO |
| G0-03 | PENDIENTE EXTERNO | Ninguna | PENDIENTE EXTERNO |
| G0-04 | CUMPLIDO | — | CUMPLIDO |
| G0-05 | NO APLICA | — | NO APLICA |
| G0-06 | CUMPLIDO | — | CUMPLIDO |
| G0-07 | CUMPLIDO | — | CUMPLIDO |
| G0-08 | CUMPLIDO | — | CUMPLIDO |
| G0-09 | PARCIAL | Ninguna | PARCIAL |
| G0-10 | CUMPLIDO | — | CUMPLIDO |
| G0-11 | CUMPLIDO | — | CUMPLIDO |
| G0-12 | PENDIENTE EXTERNO | Ninguna | PENDIENTE EXTERNO |
| G0-13 | CUMPLIDO | — | CUMPLIDO |
| G0-14 | PENDIENTE EXTERNO | Ninguna | PENDIENTE EXTERNO |
| G0-15 | CUMPLIDO | — | CUMPLIDO |

## 3. Regla de decisión

G0 solo puede pasar a **APROBADA CON RESTRICCIONES** si:

1. los 15 criterios están en CUMPLIDO o NO APLICA en la matriz de evidencias;
2. cada criterio externo (G0-02, G0-03, G0-09, G0-12, G0-14) tiene sus registros en `REGISTRADO` con un adjunto existente en [`adjuntos/`](adjuntos/README.md);
3. ningún criterio está RECHAZADO;
4. el equipo registra la decisión en un commit de gobierno propio, con enlaces a esa evidencia.

Si falta cualquiera de las cuatro condiciones, **G0 sigue NO APROBADA**. Un RECHAZADO devuelve el proyecto a la alternativa A.

## 4. Alcance si G0 pasara (condicional, hoy NO vigente)

Esta sección **no habilita nada hoy**. Describe qué quedaría permitido **si y solo si** G0 llegara a APROBADA CON RESTRICCIONES:

- **Solo el alcance B de ADR-005:** reglas, rúbricas y procedencia; apoyo determinista al proceso; revisión humana de toda alerta.
- **Prohibido igual:** scoring con ML, recomendación de personas, sugerencia de niveles, LLM sobre personas, inferencias desde rostro o voz.
- **Datos:** solo sintéticos o ficticios; los datos reales siguen prohibidos salvo una aprobación específica posterior, distinta de G0.
- **Alcance C:** sigue sin habilitar; exigiría G0 APROBADA (completa) y un ADR adicional que enmiende ADR-001.
- **RF-21:** el ranking vigente, determinista y sobre puntajes humanos, no cambia.

## 5. Fases

| Fase | Estado hoy | Con G0 APROBADA CON RESTRICCIONES (hipotético) |
|---|---|---|
| F35 Pipeline de evidencia | BLOQUEADA | Solo alcance B |
| F36 ML baseline | BLOQUEADA | Solo ML del proceso, sintético |
| F37 XAI y equidad | BLOQUEADA | Explicaciones de reglas; equidad de procedimiento |
| F38 Integración | BLOQUEADA | Módulo Laravel sin servicio externo |
| F39 Evaluación experimental | BLOQUEADA | Escenarios sintéticos de B |
| F40 Panel | BLOQUEADA | Evidencia, rúbricas, alertas y desglose |

## 6. Evidencias faltantes

| Criterio | Documento que falta | Quién lo produce |
|---|---|---|
| G0-14 | Acta de ADR-005 firmada por los tres integrantes | Equipo |
| G0-02 | Informe jurídico firmado y evaluación de impacto COMPLETADA o conclusión de NO APLICABILIDAD | Abogado o responsable legal |
| G0-03 | Aprobación del análisis de privacidad, con base legal y plazos de retención | Responsable del tratamiento, con revisión jurídica |
| G0-12 | Instrumento respondido por el docente o un representante institucional | Docente o representante institucional |
| G0-09 | Aceptación registrada del modelo de amenazas | Equipo |
