# F34A — Matriz de criterios G0

> Fase F34A, versión 1.1 (04/10/2026), corregida tras la auditoría F34A, **lista para auditoría**. Revisa los 15 criterios de la puerta G0 definidos en [ADR-005 §9.2](../diseno-inteligente/F33_ADR_005_G0.md#92-criterios-verificables) para el **alcance B** (APROBADA CON RESTRICCIONES). No cambia ningún criterio, no aprueba nada y no sustituye la decisión registrada del equipo.

## 1. Clasificación

| Estado | Significado en esta matriz |
|---|---|
| **CUMPLIDO** | La evidencia que exige ADR-005 para el alcance B existe en el repositorio, auditada, y **no depende de terceros**. En los criterios de diseño, «cumplido» significa cumplido **en diseño**: la verificación de la implementación corresponde a F35–F40 |
| **PARCIAL** | F34A produjo la evidencia, pero falta un acto que el equipo puede realizar sin terceros externos (revisión o aceptación) |
| **PENDIENTE EXTERNO** | Solo puede cerrarlo una persona o entidad con autoridad propia: el equipo mediante decisión registrada, el docente, un responsable legal o un representante institucional. F34A deja el instrumento preparado, pero **no puede producir la evidencia** |
| **BLOQUEADO** | No puede avanzar en este ciclo por una decisión vigente (se usa para el alcance C) |
| **NO APLICA** | El criterio no tiene objeto en el alcance B |

**Regla:** ningún criterio que dependa de un tercero aparece como CUMPLIDO. El validador [`validate_f34a.py`](../tools/f34a/validate_f34a.py) lo comprueba.

## 2. Matriz

| ID | Requisito (alcance B) | Estado en F33 | Evidencia disponible | Responsable de aprobación | ¿Puede cerrarse en F34A? | Acción requerida | Evidencia futura necesaria | Estado final F34A | Alcance C |
|---|---|---|---|---|---|---|---|---|---|
| G0-01 | Evidencia científica que respalde reglas y rúbricas | CUMPLE (B) | [Matriz F30](../investigacion-ia/F30_Matriz_Evidencia_Cientifica.md) [S13, S15, S19, S20]; F30 integrada y auditada | Equipo | Sí (ya cumplido) | Ninguna | Ninguna para B | **CUMPLIDO** | BLOQUEADO |
| G0-02 | Revisión jurídica: ¿es B un «sistema basado en IA» según la Ley 31814 y el DS 115-2025-PCM? Si lo es, evaluación de impacto (art. 30) | PENDIENTE | [Checklist jurídico](F34A_Checklist_Revision_Juridica.md) con lecturas preliminares; F30 corroboró solo el art. 24.1 e) | Responsable legal o abogado designado | No | Entregar el checklist a un responsable legal | Informe firmado y fechado del responsable legal con una evaluación de impacto **COMPLETADA** y documentada, si aplica, o una conclusión jurídica documentada de **NO APLICABILIDAD**; una evaluación solo planificada NO cierra G0-02 | **PENDIENTE EXTERNO** | BLOQUEADO |
| G0-03 | Análisis de datos personales: base legal, finalidad, minimización, retención y seguridad de citas y justificaciones (Ley 29733, DS 016-2024-JUS) | PENDIENTE | [Análisis de privacidad preliminar](F34A_Analisis_Privacidad_Preliminar.md) (tipo PIA, sin afirmar cumplimiento) | Responsable del tratamiento, con revisión legal | No | Validar base legal, plazos de retención y medidas de seguridad | Análisis aprobado por el responsable del tratamiento y revisado jurídicamente | **PENDIENTE EXTERNO** | BLOQUEADO |
| G0-04 | Datos disponibles: sin datos de entrenamiento; escenarios sintéticos | CUMPLE (B) | [F34](../datos-sinteticos/README.md) CERRADA: dataset 100 % sintético, reproducible y validado | Equipo | Sí (ya cumplido) | Ninguna | Ninguna para B | **CUMPLIDO** | BLOQUEADO |
| G0-05 | Calidad de etiquetas | NO APLICA (B) | B no tiene modelo sobre personas | — | — | Ninguna | — | **NO APLICA** | BLOQUEADO |
| G0-06 | Riesgo de sesgo: controles de procedimiento definidos (mismas preguntas, BARS, doble calificación, CV minimizado) | DEFINIDO (B), no medido | [Diseño F33 §4, §7 y §8](../diseno-inteligente/F33_Diseno_Funcional_Motor_Inteligente.md#8-privacidad-y-multitenencia); controles de equidad en [F34](../datos-sinteticos/F34_Gobernanza_Privacidad.md) | Equipo | Sí (ya cumplido en diseño) | Ninguna para G0; la medición queda en F39 | ICC y tasa de justificaciones válidas medidos en F39 (sintéticos) | **CUMPLIDO** (diseño; no medido) | BLOQUEADO |
| G0-07 | Explicabilidad: toda salida se explica por regla, evidencia y versión | CUMPLE en diseño (B) | [Diseño F33 §7](../diseno-inteligente/F33_Diseno_Funcional_Motor_Inteligente.md#7-procedencia-y-auditoría) | Equipo | Sí (ya cumplido en diseño) | Ninguna | Pruebas de explicación en F35/F37 | **CUMPLIDO** (diseño) | BLOQUEADO |
| G0-08 | Supervisión humana: RF-23 y ADR-002 vigentes; calificación antes de cualquier ayuda; descartar alertas con motivo | CUMPLE en diseño | ADR-002, RF-23 vigentes; flujo FF-02 en F33 | Equipo | Sí (ya cumplido en diseño) | Ninguna | Pruebas de orden «calificar antes de ver ayudas» en F35 | **CUMPLIDO** (diseño) | BLOQUEADO |
| G0-09 | Seguridad: modelo de amenazas del módulo (autorización, cross-tenant, auditoría con PII minimizada) | PENDIENTE | [Modelo de amenazas F34A](F34A_Modelo_de_Amenazas.md) (STRIDE, 25 amenazas) | Equipo | Parcialmente: se elaboró; falta su revisión | Revisión y aceptación del modelo por el equipo, registrada | Registro de aceptación; en F35/F38, pruebas de cada mitigación | **PARCIAL** | BLOQUEADO |
| G0-10 | Auditabilidad: `analysis_run`, versiones y auditoría de solo inserción | CUMPLE en diseño | [Diseño F33 §7](../diseno-inteligente/F33_Diseno_Funcional_Motor_Inteligente.md#7-procedencia-y-auditoría); hash canónico `f34-input-sha256-v1` de F34 | Equipo | Sí (ya cumplido en diseño) | Ninguna | Pruebas de inmutabilidad en F35/F38 | **CUMPLIDO** (diseño) | BLOQUEADO |
| G0-11 | Reproducibilidad: `criteria_version`, `rubric_version`, reglas versionadas; congelamiento al publicar (A-07) | CUMPLE en diseño (B) | Diseño F33; contrato y [Dataset Card F34](../datos-sinteticos/F34_Dataset_Card.md) | Equipo | Sí (ya cumplido en diseño) | Ninguna | Pruebas de congelamiento en F35 | **CUMPLIDO** (diseño) | BLOQUEADO |
| G0-12 | Necesidad institucional validada por un representante institucional o, en el marco académico, por el docente | NO EVIDENCIADA | [Instrumento de validación](F34A_Validacion_Necesidad_Institucional.md) sin respuestas | Docente o representante institucional | No | Aplicar el instrumento y archivar respuestas reales | Respuestas fechadas y firmadas, sin inventar | **PENDIENTE EXTERNO** | BLOQUEADO |
| G0-13 | Proporcionalidad: B no trata más datos que el proceso actual, salvo citas de evidencia y justificaciones | CUMPLE en diseño (B) | Diseño F33 §8; inventario de datos del [análisis de privacidad](F34A_Analisis_Privacidad_Preliminar.md#2-categorías-de-datos) | Equipo (diseño); la valoración jurídica va en G0-03 | Sí (ya cumplido en diseño) | Ninguna para el diseño | Confirmación jurídica dentro de G0-03 | **CUMPLIDO** (diseño) | BLOQUEADO |
| G0-14 | Gobierno del ADR: ADR-005 aprobado por el equipo | NO CUMPLE (propuesta) | [Paquete de aprobación](F34A_Paquete_Aprobacion_ADR005.md) con registro de firmas vacío | Equipo (los tres integrantes) | No | Decisión del equipo registrada en el paquete | Registro fechado con nombre, rol y decisión de cada integrante | **PENDIENTE EXTERNO** | BLOQUEADO |
| G0-15 | Requisitos nuevos registrados como candidatos; ninguna dependencia nueva | PENDIENTE | [RF candidatos F34A](F34A_RF_Candidatos.md) (RF-CAND-01 a 12); sin dependencias nuevas (verificado por `validate_f34a.py`) | Equipo | Sí | Registro realizado en F34A | Su promoción a baseline es otra decisión, fuera de G0 | **CUMPLIDO** | BLOQUEADO |

## 3. Resumen

| Estado final | Criterios | Total |
|---|---|---|
| CUMPLIDO | G0-01, G0-04, G0-06, G0-07, G0-08, G0-10, G0-11, G0-13, G0-15 | 9 |
| PARCIAL | G0-09 | 1 |
| PENDIENTE EXTERNO | G0-02, G0-03, G0-12, G0-14 | 4 |
| BLOQUEADO | — (todo el alcance C) | 0 |
| NO APLICA | G0-05 | 1 |

**Consecuencia:** faltan criterios obligatorios del alcance B, por lo que **G0 = NO APROBADA** ([decisión de readiness](F34A_Decision_Readiness_G0.md)). Las columnas del alcance C siguen BLOQUEADAS: no están previstas en este ciclo (ADR-005 §10).
