# Metodología de desarrollo asistido por IA

## Estado y definición

**PROPUESTO:** desarrollo colaborativo humano IA guiado por especificaciones y verificación. Es una descripción académica del protocolo, no un nombre comercial ni una metodología cuya eficacia causal ya haya sido demostrada en el colegio. El AS-IS verificable del repositorio combina reglas de gobierno, especificaciones RF/RNF, pruebas, revisión, commits y QA. El registro exacto de todos los prompts y tiempos de implementación no está disponible.

La categoría más defendible es human–AI collaborative / LLM-assisted software engineering. El uso de herramientas por un agente es una capacidad de ejecución acotada; no demuestra autonomía de decisiones de negocio. “Specification-driven” describe la prioridad de contratos y criterios, sin afirmar verificación formal completa. Hou et al. (2024), Barke et al. (2023), Ferrari y Spoletini (2025) y Jiang et al. (2026) respaldan estas distinciones conceptuales, no resultados del SaaS.

## Principios y control

La persona define alcance, aprueba y responde por cada cambio. La IA propone, inspecciona y ejecuta dentro del alcance autorizado. La decisión de selección de candidatos permanece humana. Se preservan RF-01–27, aislamiento organization_id, Policies, auditoría append-only y datos ficticios. Se prohíben secretos, prompts históricos inventados y métricas sin instrumento. Cada evidencia se etiqueta VERIFICADO, HISTÓRICO, PROPUESTO o PENDIENTE.

## Etapas, entradas y salidas

| Etapa | Entrada | Actividad humano / IA | Salida | Control / aceptación |
|---|---|---|---|---|
| 1 Necesidad | Caso académico y alcance | Humano delimita; IA identifica faltantes | Problema preliminar | No afirmar hechos institucionales sin acta |
| 2 Análisis | AS-IS, problemas y contratos | Contraste documental con código | Cadena AS→P→S→TB | F2–F9, distinguir relaciones indirectas |
| 3 Especificación | RF/RNF y roles | Definir criterio verificable | Requisito y CU | Sin selección automática ni cambio de RF |
| 4 Planificación | Rama y archivos autorizados | Humano autoriza; IA divide trabajo | Plan acotado | Un writer, no cambios ajenos |
| 5 Asistencia | Contexto mínimo y prompt | IA propone; humano revisa | Parche candidato | Prompt exacto, versión y límites cuando disponibles |
| 6 Revisión | Diff y contratos | Humano/IA comprueban seguridad y tenant | Cambio revisado | Sin secretos; no silenciar reglas |
| 7 Verificación | Tests y entorno aislado | Ejecutar regresión, assertions y typecheck | Salidas fechadas | Fallos no ocultos; no asumir TDD por tests existentes |
| 8 Análisis estático | Código y coverage real | Importar Clover; ejecutar Sonar | Gate, issues y métricas | Gate OK no prueba calidad absoluta |
| 9 Corrección | Hallazgos priorizados | Cambio mínimo y revisión humana | Resolución por regla | Verificar CLOSED/FIXED, no solo total |
| 10 Reevaluación | Misma key y alcance explicado | Repetir medición | V1/V2 comparables | Declarar cambio de clasificación de tests |
| 11 Evidencia | Logs, capturas, commit | Conservar baseline e inventario | Reporte y matrices | No mezclar histórico con ejecución actual |
| 12 Trazabilidad | RF→código→test→métrica | Revisión de consistencia | Entrega revisable | Publicar/commit solo con autorización |

## Riesgos y mitigaciones

Perry et al. (2023) y Pearce et al. (2022) motivan revisión de seguridad: generación útil no equivale a código seguro. Chen et al. (2024) y Wang et al. (2024) motivan generación/validación de tests, sin confundir ejecución con assertions relevantes. SWE-bench y SWE-agent muestran evaluaciones por ejecución sobre tareas acotadas, no sustituyen control humano. El prompting versionado y feedback de ejecución se apoyan en Syahputri et al. (2025) y Wang et al. (2026); no se transfieren sus porcentajes al proyecto.

Riesgos: alucinación documental, fuga de secretos, cambio de alcance, pruebas que reproducen implementación, sobreconfianza, comparación no homogénea y sesgo de selección de literatura. Mitigaciones: DOI cotejado, no PII, diff revisable, assertions útiles, métricas fechadas con denominadores, fuente primaria y estados de validación. Los estudios no permiten estimar aquí ahorro de horas ni efecto causal.

## Evidencias AS-IS y límites

AGENTS.md, CLAUDE.md, .claude/skills/project-guardian/, docs/tdd-evidence.md y docs/academico/ documentan contratos y evidencia RED/GREEN de determinadas fases. Git y tests confirman artefactos, pero no permiten atribuir retrospectivamente cada línea a IA o demostrar que cada cambio siguió TDD. Los seis prompts exactos de docs/academico/operacionalizacion/ACTIVIDAD_IA_COMPARACION.md son académicos: no se presentan como prompts originales del runtime. Sus ejecuciones reportadas no cuentan con URL/captura verificable de conversación.

## Variables e intervención

**VI propuesta:** aplicación del protocolo de desarrollo colaborativo humano IA guiado por especificaciones y verificación. **VD propuesta:** calidad del producto software, mediante hallazgos, pruebas y cobertura. La eficiencia se mantiene como dimensión exploratoria PENDIENTE: no existen horas, costos ni grupo de control. Se conserva la operacionalización histórica (SaaS→gestión del reclutamiento) en su carpeta, sin sustituirla silenciosamente.

Diseño defendible actual: estudio de caso documental con comparación técnica antes/después, no experimento causal de IA. La V1 y V2 son iteraciones del mismo producto; el cambio de clasificación de tests altera el denominador de cobertura. Para evaluar causalidad se necesita protocolo prospectivo con tareas comparables, esfuerzo registrado, control sin asistencia, revisión independiente y consentimiento aplicable.

## Tres niveles de afirmación y contraste AI-DLC

**A. Marco de literatura:** LLM-assisted / human-AI collaborative software engineering se apoya en ART-01, ART-02, ART-06 y ART-17; seguridad y verificación en ART-03, ART-04, ART-08 y ART-10. AI-DLC (Raja SP/AWS, 2025) es un marco técnico de contraste, no un ensayo ni una fuente peer-reviewed que demuestre superioridad.

**B. Práctica observada:** hay especificaciones, reglas, revisión por fases, código, Git y QA histórico. No hay evidencia completa de Intent/Unit/Bolt, tiempos, rituales de mob ni Operations agentiva en producción. El proceso presenta correspondencias con AI-DLC; no se afirma que se aplicó formalmente desde el inicio. Un módulo del monolito no es una Unit desplegable por definición.

**C. Reconstrucción propuesta:** el protocolo de esta entrega organiza necesidad→análisis→especificación→planificación→asistencia→implementación→revisión→testing→análisis estático→corrección→reevaluación→documentación→trazabilidad. Las trece filas de la matriz separan generación/implementación y documentación/evidencia para hacer sus controles auditables; son una desagregación de las doce etapas anteriores, no nuevas fases históricas.

La matriz de doble entrada contiene 20 artículos, once conceptos AI-DLC y 27 criterios del instrumento de registro. Los cruces genéricos Inception/Construction/Operations son interpretación académica; las columnas Intent/Unit/Bolt en artículos permanecen vacías. No se traslada evidencia del proyecto ejemplo de la matriz de registro. Véase ../fuentes/ANALISIS_AI_DLC_Y_REGISTRO.md y ../entregables-finales/MATRIZ_DOBLE_ENTRADA_METODOLOGIA_IA.xlsx.
