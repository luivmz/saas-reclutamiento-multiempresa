# F32 — Readiness para F33

## Decisión

**APTO PARA F33 DE DISEÑO** y formulación de ADR-005. G0 sigue **NO APROBADA**; no se autoriza scoring/recomendación de personas, implementación funcional ni aprobación automática de G0.

El producto v1.1 y su línea académica tienen evidencia suficiente para discutir el diseño siguiente. [F32-M01/L01/L02](F32_Matriz_Hallazgos.md) están **RESUELTOS**: recetas vigentes usan `f11r`, el F11 adaptado queda protegido, la navegación refleja fases cerradas y las ramas se conservan por defecto. F32 está **CERRADA CON OBSERVACIONES**, con commit/publicación e integración autorizados mediante gates CI. Esta decisión no reabre el release técnico ni permite evaluar candidatos con IA.

## Gates para F33 y fases posteriores

| Área | Estado actual | Criterio antes de continuar |
|---|---|---|
| RF-01..RF-27 / CU-01..CU-20 | Baseline preservado | No renumerar ni reinterpretar |
| RF-23 | Humano, confirmación y justificación | ADR-005 debe ratificarlo; ranking sigue siendo apoyo |
| RF-28 | Candidato no implementado | No presentar reportes/panel como feature productiva |
| RF-29 | Riesgo operacional experimental, informativo y opcional | Sin PII/IDs en request actual, sin modificar ranking/etapa/selección |
| Arquitectura | Monolito modular; Laravel sistema de registro | No transformar el conjunto en microservicios generales |
| Multitenencia / CV / auditoría | Scopes y Policies; storage privado; append-only | Todo diseño nuevo hereda autorización por organización y auditoría sin PII/secrets |
| QA | Evidencia histórica y CI actual verde | Pruebas nuevas proporcionales si después se autoriza implementación |
| RNF-06 / RNF-07 | NO VERIFICADOS | No inventar SLA, rendimiento, disponibilidad ni validación institucional |
| F11 / ARQ-01 | Oficial vigente; 17 componentes, 20 relaciones conceptuales | No sobrescribir F11 adaptado, F9 publicado o F23 histórico |
| Herramientas de F30 | Evaluación de snapshot; ninguna adopción implícita | Versión/licencia/seguridad/compatibilidad y autorización en el momento de adopción |

## ADR-005 y G0

Aplicar las seis condiciones de [F30, puerta G0](../investigacion-ia/F30_Recomendaciones_F33_F40.md). Su estado en F32 es **NO APROBADA**:

1. ADR-005 propuesto y posteriormente aprobado por el equipo, ratificando o enmendando ADR-001 explícitamente. Esta auditoría no aprueba una enmienda.
2. Revisión autorizada del contrato 4 solo si la enmienda la requiere; mientras tanto sigue prohibida la evaluación de personas por ML.
3. Evaluación de impacto previa documentada, revisión jurídica y contraste oficial de artículos aplicables. «Iniciada» no equivale a gate cumplido.
4. Análisis de datos personales: base legal, finalidad, minimización, retención y seguridad. Resolver público/privado y responsables institucionales sin inventar respuestas.
5. Requisitos nuevos como candidatos, según la planificación F30 desde RF-32; no promover por mera implementación ni alterar RF-01..RF-27.
6. Dependencias nuevas solo con autorización explícita, versión, licencia y revisión de seguridad actuales.

F34 puede diseñar datos **sintéticos** en paralelo, sin scoring/recomendación de personas. F35–F40 no comienzan sin G0 completa. No usar el rótulo «motor inteligente» para eludir estas fronteras.

## Alcance admisible del diseño funcional

- Estructurar rúbricas, preguntas, evidencia y procedencia; preservar la calificación humana previa a cualquier ayuda del sistema.
- Verificaciones deterministas del proceso: evidencia faltante, inconsistencias y desacuerdo entre evaluadores. No sugerir niveles, puntuar, descartar o recomendar personas.
- Mantener suma ponderada RF-21, separación C09 → C10 → C11 y selección final humana.
- Servicio futuro opcional con Laravel como registro, contratos explícitos, fallback y aislamiento por organización. `organization_id` no entra automáticamente al request RF-29; cualquier contexto futuro requiere justificación y minimización.
- Audio/vídeo: por defecto no grabar. Necesidad, base legal, G0 y revisión humana antes de cualquier diseño que contemple audio. Nada de emociones, personalidad, rostro, prosodia o huella de voz.
- Explicabilidad ligada a evidencia y justificación verificable; no atribuir métricas de equidad ni validez predictiva a muestras inexistentes. SHAP interno no es justificación de contratación.

## Evidencia de apoyo y límites

- [Informe F32](F32_Auditoria_Academica_Global.md): cadena RF → CU → componentes → CP → evidencias → informe.
- [ADR-001](../../v1.1/architecture-decisions/ADR-001-ml-boundary.md) y [ADR-002](../../v1.1/architecture-decisions/ADR-002-human-oversight.md): fronteras vigentes.
- [F11 definitivo](../practica-11/F11_Arquitectura_del_Sistema_Colegio_Andino.md): arquitectura oficial actual.
- [F30 gobernanza](../investigacion-ia/F30_Explainability_Fairness_Gobernanza.md): hipótesis, límites científicos y obligaciones a contrastar.

La literatura es fundamento de propuestas, no prueba de eficacia del futuro motor en Colegio Andino. No hay beneficios medidos ni aprobación institucional. En F32 se contrastó el cambio de calendario europeo con la norma oficial, no solo con prensa: [Reglamento (UE) 2026/1744](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX%3A32026R1744). Eso no determina por sí solo su aplicabilidad territorial al proyecto. Para Perú prevalecen la revisión jurídica y los textos oficiales requeridos por G0, no una certificación del auditor.

## Handoff

Antes de escribir funcionalidad: acordar responsable/aprobador de ADR-005 y cumplir los criterios de aceptación de G0. El flujo documental F32-M01 ya está protegido y las correcciones L01/L02 están resueltas. F33 puede preparar borradores de diseño sin activar estas propuestas. Conservar LOW/OBS aceptadas/futuras y la historia QA; no afirmar que fueron ejecutadas nuevamente.

No se autoriza runtime, nuevas dependencias, datos reales, cambios de tags/release ni modificaciones de fuentes oficiales. El cierre autorizado comprende un único commit F32, push de la feature y merges `--no-ff` hacia develop y main con CI verde obligatorio. Consultar los hashes/resultados finales en Git/GitHub; no se anticipan en este documento.
