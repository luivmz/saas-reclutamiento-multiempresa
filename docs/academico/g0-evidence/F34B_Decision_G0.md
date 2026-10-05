# F34B — Decisión G0

> Fase F34B, versión 1 (04/10/2026); **reevaluada en F34C y F34D**. Reevaluación de los 15 criterios con la evidencia recibida. **Ningún documento ni validador aprueba G0 automáticamente:** este documento solo aplica la regla de [ADR-005 §9.1](../diseno-inteligente/F33_ADR_005_G0.md#91-estados-y-regla-de-decisión) a la [matriz de evidencias](F34B_Matriz_Evidencias_G0.md).

## 1. Resultado

- **G0 = NO APROBADA.**
- **ADR-005 = PROPUESTA** (estado canónico, sin cambios en F33).
- **APROBACIÓN INTERNA DEL EQUIPO REGISTRADA** (F34C, [acta](F34B_Acta_Aprobacion_ADR005.md)). Satisface G0-14. Es la decisión del equipo sobre la dirección del motor: no es una aprobación jurídica, de privacidad ni institucional, y no aprueba G0.
- **F35–F40 = BLOQUEADAS.**
- **Alcance C: no habilitado.**
- **Los datos reales siguen PROHIBIDOS.**
- RF-23 sigue humana; RF-29 sigue experimental e informativa.
- F34D = LISTA PARA AUDITORÍA.

**Motivo:** F34C registró evidencia real solo para G0-14 y G0-09, que pasan a CUMPLIDO. Siguen sin evidencia G0-02 (revisión jurídica y evaluación de impacto), G0-03 (privacidad) y G0-12 (necesidad institucional), que son obligatorios para el alcance B. En F34D llegó para G0-12 una respuesta en texto (NECESIDAD VALIDADA declarada), pero sin adjunto archivado y con un nombre que no coincide con el docente registrado: G0-12 sigue PENDIENTE EXTERNO ([registro §4](F34B_Validacion_Necesidad.md#4-respuesta-recibida-en-f34d-sin-evidencia-archivada)).

## 2. Reevaluación de los 15 criterios

| Criterio | Estado F34A | Evidencia nueva (F34B/F34C) | Estado vigente (F34C) |
|---|---|---|---|
| G0-01 | CUMPLIDO | — | CUMPLIDO |
| G0-02 | PENDIENTE EXTERNO | Ninguna | PENDIENTE EXTERNO |
| G0-03 | PENDIENTE EXTERNO | Ninguna | PENDIENTE EXTERNO |
| G0-04 | CUMPLIDO | — | CUMPLIDO |
| G0-05 | NO APLICA | — | NO APLICA |
| G0-06 | CUMPLIDO | — | CUMPLIDO |
| G0-07 | CUMPLIDO | — | CUMPLIDO |
| G0-08 | CUMPLIDO | — | CUMPLIDO |
| G0-09 | PARCIAL | Capturas de los tres integrantes y confirmación de Luis Vila (F34C) | CUMPLIDO |
| G0-10 | CUMPLIDO | — | CUMPLIDO |
| G0-11 | CUMPLIDO | — | CUMPLIDO |
| G0-12 | PENDIENTE EXTERNO | Respuesta en texto sin adjunto ni identidad verificable (F34D) | PENDIENTE EXTERNO |
| G0-13 | CUMPLIDO | — | CUMPLIDO |
| G0-14 | PENDIENTE EXTERNO | Capturas de los tres integrantes y confirmación de Luis Vila (F34C) | CUMPLIDO |
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
| G0-02 | Informe jurídico firmado y evaluación de impacto COMPLETADA o conclusión de NO APLICABILIDAD | Abogado o responsable legal |
| G0-03 | Aprobación del análisis de privacidad, con base legal y plazos de retención | Responsable del tratamiento, con revisión jurídica |
| G0-12 | Respuesta archivada en `adjuntos/` (captura, PDF, correo exportado o documento firmado) y vinculación inequívoca con el docente registrado, o confirmación adicional de este (OBS-F34D-01, 02) | Docente o representante institucional |
