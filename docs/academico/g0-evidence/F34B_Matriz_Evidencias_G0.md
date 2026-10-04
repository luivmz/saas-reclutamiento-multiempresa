# F34B — Matriz maestra de evidencias G0

> Fase F34B, versión 1 (04/10/2026). Registro de la evidencia de los 15 criterios G0 de [ADR-005 §9.2](../diseno-inteligente/F33_ADR_005_G0.md#92-criterios-verificables) para el **alcance B**. Parte de la [matriz de F34A](../g0-readiness/F34A_Matriz_G0.md) y solo cambia un estado cuando llega evidencia real. **A 04/10/2026 no se recibió ninguna evidencia externa.**

## 1. Estados

| Estado | Significado |
|---|---|
| **CUMPLIDO** | Evidencia válida recibida y verificada. Para un criterio externo exige un adjunto existente en [`adjuntos/`](adjuntos/README.md) |
| **PARCIAL** | El entregable interno existe, pero falta su aceptación registrada |
| **PENDIENTE EXTERNO** | Falta la evidencia que solo puede aportar un tercero o una decisión registrada del equipo |
| **RECHAZADO** | Se recibió evidencia real con decisión negativa |
| **NO APLICA** | El criterio no tiene objeto en el alcance B |

**Verificada** = «Sí» solo si la evidencia existe en el repositorio y se comprobó (por validador o adjunto). Una evidencia que no existe no se verifica.

## 2. Matriz

| G0_ID | Requisito | Evidencia requerida | Evidencia recibida | Fuente | Responsable | Fecha | Verificada | Estado | Observaciones |
|---|---|---|---|---|---|---|---|---|---|
| G0-01 | Evidencia científica | Matriz F30 que respalde reglas y rúbricas | [Matriz F30](../investigacion-ia/F30_Matriz_Evidencia_Cientifica.md) | Repositorio, develop `417ea4f` | Equipo | 2026-10-04 | Sí (`validate_f30.py`) | **CUMPLIDO** | Sin cambios desde F34A |
| G0-02 | Revisión jurídica y evaluación de impacto | Informe jurídico firmado; evaluación COMPLETADA o conclusión de NO APLICABILIDAD | Ninguna | — | Abogado o responsable legal | — | No | **PENDIENTE EXTERNO** | [Formulario](F34B_Revision_Juridica.md) sin completar |
| G0-03 | Privacidad | Análisis aprobado por el responsable del tratamiento, con revisión jurídica | Ninguna | — | Responsable del tratamiento | — | No | **PENDIENTE EXTERNO** | [Registro](F34B_Privacidad.md) sin completar |
| G0-04 | Datos disponibles | Escenarios sintéticos | [F34](../datos-sinteticos/README.md) | Repositorio, develop `417ea4f` | Equipo | 2026-10-04 | Sí (`validate_f34.py`) | **CUMPLIDO** | Solo datos sintéticos |
| G0-05 | Calidad de etiquetas | — | — | — | — | — | — | **NO APLICA** | B no tiene modelo sobre personas |
| G0-06 | Riesgo de sesgo | Controles de procedimiento definidos | [Diseño F33](../diseno-inteligente/F33_Diseno_Funcional_Motor_Inteligente.md) | Repositorio, develop `417ea4f` | Equipo | 2026-10-04 | Sí (`validate_f33.py`) | **CUMPLIDO** | En diseño; medición en F39 |
| G0-07 | Explicabilidad | Salidas explicadas por regla, evidencia y versión | [Diseño F33 §7](../diseno-inteligente/F33_Diseno_Funcional_Motor_Inteligente.md#7-procedencia-y-auditoría) | Repositorio, develop `417ea4f` | Equipo | 2026-10-04 | Sí (`validate_f33.py`) | **CUMPLIDO** | En diseño |
| G0-08 | Supervisión humana | RF-23, ADR-002; calificar antes de ver ayudas | ADR-002; RF-23; [ADR-005 §8](../diseno-inteligente/F33_ADR_005_G0.md#8-riesgos-y-controles) | Repositorio, develop `417ea4f` | Equipo | 2026-10-04 | Sí (`validate_f33.py`) | **CUMPLIDO** | En diseño |
| G0-09 | Seguridad | Modelo de amenazas aceptado por el equipo | [Modelo F34A](../g0-readiness/F34A_Modelo_de_Amenazas.md); aceptación: ninguna | Repositorio, develop `417ea4f` | Equipo | — | No (aceptación) | **PARCIAL** | [Registro de aceptación](F34B_Aceptacion_Threat_Model.md) sin completar |
| G0-10 | Auditabilidad | `analysis_run`, versiones, auditoría de solo inserción | [Diseño F33 §7](../diseno-inteligente/F33_Diseno_Funcional_Motor_Inteligente.md#7-procedencia-y-auditoría); hash canónico F34 | Repositorio, develop `417ea4f` | Equipo | 2026-10-04 | Sí (`validate_f33.py`, `validate_f34.py`) | **CUMPLIDO** | En diseño |
| G0-11 | Reproducibilidad | Versiones y congelamiento | [Dataset Card F34](../datos-sinteticos/F34_Dataset_Card.md) | Repositorio, develop `417ea4f` | Equipo | 2026-10-04 | Sí (`validate_f34.py`) | **CUMPLIDO** | En diseño |
| G0-12 | Necesidad institucional | Respuestas reales del docente o de un representante institucional | Ninguna | — | Docente o representante institucional | — | No | **PENDIENTE EXTERNO** | [Registro](F34B_Validacion_Necesidad.md) sin respuestas |
| G0-13 | Proporcionalidad | B no trata más datos que el proceso actual, salvo citas y justificaciones | [Análisis de privacidad F34A §3](../g0-readiness/F34A_Analisis_Privacidad_Preliminar.md#3-necesidad-y-proporcionalidad) | Repositorio, develop `417ea4f` | Equipo | 2026-10-04 | Sí (`validate_f34a.py`) | **CUMPLIDO** | En diseño; valoración jurídica dentro de G0-03 |
| G0-14 | Gobierno del ADR | ADR-005 aprobado por el equipo | Ninguna | — | Equipo (tres integrantes) | — | No | **PENDIENTE EXTERNO** | [Acta](F34B_Acta_Aprobacion_ADR005.md) sin firmas |
| G0-15 | Requisitos y dependencias | Candidatos registrados; sin dependencias nuevas | [RF candidatos F34A](../g0-readiness/F34A_RF_Candidatos.md) | Repositorio, develop `417ea4f` | Equipo | 2026-10-04 | Sí (`validate_f34a.py`) | **CUMPLIDO** | Sin cambios desde F34A |

## 3. Resumen

| Estado | Criterios | Total |
|---|---|---|
| CUMPLIDO | G0-01, G0-04, G0-06, G0-07, G0-08, G0-10, G0-11, G0-13, G0-15 | 9 |
| PARCIAL | G0-09 | 1 |
| PENDIENTE EXTERNO | G0-02, G0-03, G0-12, G0-14 | 4 |
| RECHAZADO | — | 0 |
| NO APLICA | G0-05 | 1 |

**Evidencias externas recibidas: 0.** Los estados no cambian respecto de F34A.
