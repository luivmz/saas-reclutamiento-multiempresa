# F34A — Checklist para la revisión jurídica (G0-02)

> Fase F34A, versión 1.1 (04/10/2026), corregida tras la auditoría F34A. **Esto no es un dictamen legal** ni una revisión jurídica aprobada. Es una lista de preguntas preparada por el equipo de un proyecto académico para que un abogado o responsable legal la responda. Nada de lo aquí escrito afirma que el proyecto cumpla o incumpla una norma. Estado de G0-02: **PENDIENTE EXTERNO**.

## 1. Cómo leer el estado de cada punto

| Estado | Significado |
|---|---|
| **VERIFICADO** | Se verificó **el texto o la fuente oficial** citada (no su interpretación jurídica). Viene de la verificación de F30 o de este repositorio |
| **LECTURA PRELIMINAR** | Lectura del equipo, sin contraste completo con la publicación oficial o sin interpretación profesional. No produce efectos jurídicos |
| **REQUIERE ABOGADO/RESPONSABLE LEGAL** | Pregunta que solo puede responder un profesional del derecho o el responsable del tratamiento |

Las fuentes [Oxx] remiten a las [referencias de F30](../investigacion-ia/REFERENCIAS.md).

## 2. Objeto de la revisión

El **alcance B** de ADR-005: reglas, rúbricas y procedencia sobre la evaluación de postulantes, con nivel asignado siempre por una persona y decisión final humana (RF-23). Sin modelos sobre personas, sin servicio externo y sin datos reales. Fuera del objeto: el alcance C (futuro) y RF-29 (ML del proceso, experimental).

## 3. Checklist

### 3.1 DS 115-2025-PCM, reglamento de la Ley 31814 [O13, O10]

| # | Punto | Estado | Fuente o nota |
|---|---|---|---|
| J-01 | El DS 115-2025-PCM existe y su ficha oficial está publicada | VERIFICADO | [O13], ficha oficial en gob.pe verificada en F30 |
| J-02 | El art. 24.1 e) clasifica de riesgo alto los sistemas de IA que determinan selección, evaluación, contratación o cese de postulantes | VERIFICADO | [O13]; corroborado en F30 con la publicación oficial |
| J-03 | ¿Es el alcance B un «sistema basado en IA» en el sentido de la Ley 31814 y su reglamento, si solo aplica reglas deterministas y la persona califica? | REQUIERE ABOGADO/RESPONSABLE LEGAL | Pregunta central de G0-02 |
| J-04 | Si B fuera sistema de IA, ¿«determina» la selección o evaluación (art. 24.1 e) cuando solo verifica el proceso y nunca califica? | REQUIERE ABOGADO/RESPONSABLE LEGAL | Depende de J-03 |
| J-05 | Art. 24.1 b): evaluación de niñas, niños y adolescentes en educación; ¿aplica a la selección de docentes de un colegio? | LECTURA PRELIMINAR | Leído en F30 en una copia no oficial; la lectura del equipo es que el objeto son estudiantes, no postulantes. Confirmar |
| J-06 | Art. 24.1 i): inferir emociones en el trabajo o centros educativos | LECTURA PRELIMINAR | Leído en F30 en una copia no oficial; B no infiere emociones (prohibición de ADR-005 §6.7) |
| J-07 | Art. 25: transparencia y explicación | LECTURA PRELIMINAR | Contrastar con la publicación oficial; B explica cada alerta por regla, evidencia y versión |
| J-08 | Art. 30: evaluación de impacto previa; ¿es obligatoria para B? ¿qué contenido y qué autoridad? | REQUIERE ABOGADO/RESPONSABLE LEGAL | Contrastar con la publicación oficial antes de producir efectos. Respuesta exigida: evaluación COMPLETADA o conclusión documentada de NO APLICABILIDAD (ver §5) |
| J-09 | Art. 31: registro; ¿debe registrarse B? | REQUIERE ABOGADO/RESPONSABLE LEGAL | Ídem |
| J-10 | Vigencia y plazos de adecuación aplicables a un proyecto académico sin uso productivo | REQUIERE ABOGADO/RESPONSABLE LEGAL | — |

### 3.2 Ley 29733 y su reglamento, DS 016-2024-JUS [O15, O09]

| # | Punto | Estado | Fuente o nota |
|---|---|---|---|
| J-11 | La Ley 29733 y el DS 016-2024-JUS están publicados y son las normas peruanas de protección de datos personales | VERIFICADO | [O15], [O09]; fuentes oficiales verificadas en F30 |
| J-12 | Principios de consentimiento, finalidad, proporcionalidad y seguridad aplicables a datos de postulantes | LECTURA PRELIMINAR | [O15] según F30; falta interpretación para citas de evidencia y justificaciones |
| J-13 | Base legal del tratamiento de citas de evidencia, justificaciones y anotaciones: ¿consentimiento, relación precontractual u otra? | REQUIERE ABOGADO/RESPONSABLE LEGAL | El consentimiento **no** levanta por sí solo la prohibición de datos reales del proyecto (contrato 7) |
| J-14 | Datos sensibles: ¿puede una cita de evidencia contener datos sensibles y cómo debe tratarse? | REQUIERE ABOGADO/RESPONSABLE LEGAL | B no recolecta atributos sensibles por diseño |
| J-15 | Inscripción del banco de datos de postulantes y obligaciones del responsable del tratamiento | REQUIERE ABOGADO/RESPONSABLE LEGAL | — |
| J-16 | Medidas de seguridad exigibles para citas de evidencia y registros de auditoría | REQUIERE ABOGADO/RESPONSABLE LEGAL | Medidas técnicas propuestas en el [modelo de amenazas](F34A_Modelo_de_Amenazas.md) |
| J-17 | Derechos del titular (acceso, rectificación, cancelación, oposición) frente a anotaciones de solo inserción y auditoría inmutable | REQUIERE ABOGADO/RESPONSABLE LEGAL | Tensión posible entre inmutabilidad y cancelación |

### 3.3 Decisiones automatizadas, alto riesgo y supervisión humana

| # | Punto | Estado | Fuente o nota |
|---|---|---|---|
| J-18 | La Ley 29733 reconoce un derecho del titular frente a decisiones basadas únicamente en tratamiento automatizado que evalúa aspectos de su persona | LECTURA PRELIMINAR | Ubicar el artículo y contrastar con el texto oficial |
| J-19 | ¿Basta RF-23 (decisión humana con confirmación y justificación) y ADR-002 para que B no sea una decisión automatizada? | REQUIERE ABOGADO/RESPONSABLE LEGAL | Diseño: el sistema nunca selecciona, descarta ni contrata |
| J-20 | ¿Qué grado de supervisión humana y de explicación exige la norma peruana si B fuera de riesgo alto? | REQUIERE ABOGADO/RESPONSABLE LEGAL | — |
| J-21 | Transparencia hacia el postulante: ¿debe informarse del uso de reglas de verificación del proceso? | REQUIERE ABOGADO/RESPONSABLE LEGAL | — |

### 3.4 Retención y transferencias

| # | Punto | Estado | Fuente o nota |
|---|---|---|---|
| J-22 | Plazo de conservación de citas de evidencia, justificaciones, anotaciones y eventos de análisis | REQUIERE ABOGADO/RESPONSABLE LEGAL | Propuesta técnica en el [análisis de privacidad](F34A_Analisis_Privacidad_Preliminar.md#7-retención-y-borrado) |
| J-23 | Transferencias o flujo transfronterizo | LECTURA PRELIMINAR | B no usa servicios externos ni terceros; **no aplica mientras sea así**. Si se usara un proveedor en la nube o el alcance C, debe revisarse |
| J-24 | Encargados del tratamiento (alojamiento, respaldos) | REQUIERE ABOGADO/RESPONSABLE LEGAL | Hoy el proyecto corre en Docker local con datos ficticios |

### 3.5 Referencia comparativa: Reglamento (UE) 2024/1689 [O01, O16, O02]

No aplica directamente en Perú; se usa solo para comparar el diseño.

| # | Punto | Estado | Fuente o nota |
|---|---|---|---|
| J-25 | Anexo III, 4.a: el reclutamiento y la evaluación de candidatos son de alto riesgo | VERIFICADO | [O01], texto contrastado en el Diario Oficial (F30) |
| J-26 | Art. 14: supervisión humana capaz de ignorar o revertir el resultado y consciente del sesgo de automatización | VERIFICADO | [O01] |
| J-27 | Art. 5.1.f: prohibición de inferir emociones en el trabajo y la educación | VERIFICADO | [O01]; no modificada por [O16] |
| J-28 | Calendario: requisitos de alto riesgo del Anexo III desde el 2/12/2027 | VERIFICADO | [O16] |
| J-29 | RGPD art. 22: derecho a no ser objeto de decisiones exclusivamente automatizadas | VERIFICADO | [O02], referencia comparada |

## 4. Resultado esperado de la revisión

Para cerrar G0-02 se necesita un documento **firmado y fechado** por el abogado o responsable legal que:

1. responda J-03 y J-04 (¿es B un sistema de IA y de riesgo alto?);
2. concluya de forma documentada si la evaluación de impacto (J-08) aplica al alcance B y aporte, según el caso, la evaluación **COMPLETADA** y documentada o la conclusión jurídica de **NO APLICABILIDAD** (§5);
3. confirme o corrija las lecturas preliminares (J-05 a J-07, J-12, J-18, J-23);
4. responda los puntos de datos personales (J-13 a J-17, J-22, J-24) o los derive al análisis de G0-03.

## 5. Regla de cierre de G0-02: evaluación de impacto

G0-02 solo puede cerrarse con una de estas dos evidencias, firmadas y fechadas por el responsable legal:

| Situación | Evidencia que cierra G0-02 |
|---|---|
| La evaluación de impacto **aplica** al alcance B | La evaluación de impacto **COMPLETADA** y documentada, archivada con el informe jurídico |
| La evaluación de impacto **no aplica** | Una conclusión jurídica documentada de **NO APLICABILIDAD**, con su fundamento |

**Una evaluación de impacto planificada, en curso o comprometida para el futuro NO cierra G0-02.** Esta regla aplica el criterio G0-02 de [ADR-005 §9.2](../diseno-inteligente/F33_ADR_005_G0.md#92-criterios-verificables) («si lo es, evaluación de impacto (art. 30)») y la condición S-02 de la [decisión de readiness](F34A_Decision_Readiness_G0.md#3-criterios-de-salida-no-aprobada--aprobada-con-restricciones).

## 6. Resumen

| Estado | Puntos | Total |
|---|---|---|
| VERIFICADO | J-01, J-02, J-11, J-25 a J-29 | 8 |
| LECTURA PRELIMINAR | J-05, J-06, J-07, J-12, J-18, J-23 | 6 |
| REQUIERE ABOGADO/RESPONSABLE LEGAL | J-03, J-04, J-08, J-09, J-10, J-13 a J-17, J-19 a J-22, J-24 | 15 |

**F34A no presenta este checklist como revisión jurídica aprobada.** G0-02 sigue PENDIENTE EXTERNO.
