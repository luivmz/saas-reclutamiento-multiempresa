# Prototipo ML-02 — ayudas sobre la evidencia

> **PROTOTIPO DE DISEÑO — NO IMPLEMENTADO.** Documento del 07/11/2026. Prepara F37-SBX y F38-SBX, que siguen **BLOQUEADAS** (F36-SBX-GATE = NO SUPERADO). No hay modelo, cálculo, entrenamiento ni conexión con el SaaS.

| Archivo | Qué es |
|---|---|
| [`index.html`](index.html) | Página estática y navegable que muestra EI-01 a EI-07 sobre un expediente sintético, con resultados escritos a mano. Abre directamente en el navegador, sin servidor, sin JavaScript y sin recursos externos |
| [`F36SBX_ML02_Plan_Entrenamiento_Evaluacion.md`](F36SBX_ML02_Plan_Entrenamiento_Evaluacion.md) | Plan: por qué no hay entrenamiento (EI-22 bloqueado), qué datos sintéticos, qué métricas (M-01 a M-13, R-01 a R-05) y qué protocolo |

## Por qué es estático

El charter de F36-SBX autoriza investigar y **diseñar**. No autoriza UI productiva, endpoints ni la implementación de EI (§1 y §4; EI-23 BLOCKED). Una página estática dentro del paquete documental es un artefacto de diseño: sirve para discutir la experiencia de quien evalúa sin crear ninguna capacidad.

## Cómo abrirlo

Hay que abrir `index.html` con un navegador. Respeta el tema claro u oscuro del sistema, funciona a 320 px de ancho y tiene un enlace de salto, encabezados jerárquicos, tablas con `caption` y `scope`, y foco visible.
