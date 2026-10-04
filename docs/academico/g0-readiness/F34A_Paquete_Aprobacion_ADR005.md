# F34A — Paquete de aprobación de ADR-005

> Fase F34A, versión 1.1 (04/10/2026), corregida tras la auditoría F34A. Prepara la decisión del equipo sobre [ADR-005](../diseno-inteligente/F33_ADR_005_G0.md). **Estado del ADR: PROPUESTA. Estado de la aprobación: PENDIENTE.** Este paquete no aprueba el ADR, no lo modifica y no contiene firmas: solo el equipo puede registrar su decisión en la [sección 9](#9-registro-de-decisión-del-equipo).

## 1. Resumen ejecutivo

F30 concluyó que la evidencia científica respalda **estructurar y verificar la evidencia** con la que los evaluadores califican, no **puntuar ni recomendar candidatos**. ADR-005 propone que el motor inteligente siga la **alternativa B**: el sistema organiza vacante, competencias, rúbricas y evidencia, registra la procedencia y verifica el proceso con reglas deterministas; **el nivel lo asigna siempre una persona** y la decisión final sigue siendo humana (RF-23).

Aprobar ADR-005 es **una sola de las condiciones** de G0 (G0-14). Aunque el equipo lo aprobara hoy, G0 seguiría NO APROBADA mientras falten la revisión jurídica, el análisis de privacidad validado y la necesidad institucional ([matriz G0](F34A_Matriz_G0.md)).

## 2. Decisión propuesta

1. Ratificar ADR-001 y ADR-002 sin enmienda; el contrato 4 y OUT-04, OUT-05 y OUT-11 no cambian.
2. Dirección del motor: **alternativa B** (reglas, rúbricas y procedencia).
3. Mantener la **alternativa E**: ML solo sobre el proceso (RF-29, experimental e informativo).
4. **C** queda como FUTURA, condicionada a G0 APROBADA completa y a un ADR adicional.
5. **D** (scoring o recomendación de personas) se **rechaza** en este ciclo.
6. **A** (sin inteligencia sobre personas) es el estado por defecto mientras G0 no esté aprobada.

Texto completo: [ADR-005 §6](../diseno-inteligente/F33_ADR_005_G0.md#6-decisión-propuesta).

## 3. Alcance B

| Incluye | Condición |
|---|---|
| Catálogo de competencias y rúbricas BARS versionadas | Congeladas al publicar la vacante (A-07) |
| Registro de evidencia por criterio con procedencia, justificación y suficiencia | Texto **registrado o introducido por una persona**; sin extracción automática |
| Valoración humana (`PROGRAMADA` → registro único → `REALIZADA`) | Comportamiento vigente de `AssessmentResultRecorder`; sin segundo resultado |
| Anotaciones complementarias de solo inserción | No modifican nivel ni puntaje |
| Alertas deterministas del proceso (requisito no evidenciado, evidencia faltante, discrepancia, sesión vencida) | Se pueden descartar con motivo; nunca filtran ni descartan personas |
| Acuerdo entre evaluadores (ICC) | Calidad del proceso, no de la persona |
| Búsqueda determinista dentro del texto introducido por personas | Sin embeddings ni similitud semántica |
| `analysis_run` inmutable con eventos de solo inserción | Versiones y hash canónico de entrada |

Sin dependencias nuevas, sin servicio externo y sin datos reales.

## 4. Capacidades excluidas

| Capacidad | Estado | Motivo |
|---|---|---|
| Scoring, ranking o recomendación de personas generados por el sistema | **Rechazada** (D) | ADR-001, contrato 4, OUT-04 y OUT-05 |
| Sugerir niveles o resumir personas | Bloqueada | F33, CAP-05 y CAP-15/16 |
| Parsing o extracción automática de PDF o DOCX, OCR, embeddings, localizador semántico | FUTURA (C) | Requiere G0 APROBADA y un ADR que enmiende ADR-001 |
| LLM sobre personas | Bloqueada | F30 D-17 |
| Inferencias desde rostro, voz o apariencia; prosodia, acento, emociones o biometría | **Prohibida sin excepción** | ADR-005 §6.7; DS 115-2025-PCM (lectura F30) |
| Audio de entrevistas | Solo con una aprobación aparte (CAP-27) | Datos personales sin necesidad |
| Modelos de idoneidad, desempeño o permanencia | Bloqueada | CAP-25; sin etiquetas válidas |
| Uso de datos reales de candidatos | **Prohibido** | Contrato 7; regla de datos de ADR-005 §6.10 |

## 5. Riesgos

| Riesgo | Control propuesto |
|---|---|
| Anclaje en las ayudas del sistema | Calificar antes de ver cualquier ayuda; registrar si se vio antes |
| Scoring encubierto («índice», «afinidad», «semáforo») | Prueba de alcance: ningún campo calculado sobre personas alimenta RF-21 |
| Justificaciones vacías o copiadas | Justificación obligatoria y revisión por muestreo |
| Datos personales en citas de evidencia | Minimización, Policies por organización, retención definida en G0-03 |
| Fuga entre organizaciones | `organization_id`, scope global y pruebas cross-tenant |
| Deriva hacia C o D sin gobierno | Toda ampliación exige un ADR nuevo y revisar G0 |

Detalle en [ADR-005 §8](../diseno-inteligente/F33_ADR_005_G0.md#8-riesgos-y-controles) y en el [modelo de amenazas](F34A_Modelo_de_Amenazas.md).

## 6. Consecuencias

- **Positivas:** diseño explicable por construcción; sin datos de entrenamiento ni dependencias nuevas; coherente con ADR-001, ADR-002 y ADR-004; mejora la trazabilidad de RF-19 a RF-23.
- **Negativas:** más trabajo para el evaluador; el motor no automatiza la evaluación; C y D quedan sin explorar en este ciclo.
- **Baseline:** RF-01 a RF-27 y CU-01 a CU-20 no cambian; las capacidades nuevas son [candidatas](F34A_RF_Candidatos.md).

## 7. Condiciones de reversión

Se vuelve a la alternativa A, y G0 a NO APROBADA, si:

- la revisión jurídica concluye que B impone obligaciones que el proyecto no puede cumplir;
- el ICC o la tasa de justificaciones válidas medidos en F39 contradicen el beneficio esperado;
- se detecta anclaje (calificaciones registradas después de ver ayudas);
- ocurre un incidente de datos o una fuga entre organizaciones;
- aparece un campo calculado sobre personas que alimente el ranking o la decisión;
- el equipo retira la aprobación.

La reversión se registra en un ADR nuevo; ADR-005 no se reescribe ([ADR-005 §11](../diseno-inteligente/F33_ADR_005_G0.md#11-condiciones-de-reversión)).

## 8. Relación con F30, F33 y F34

| Fase | Aporte a esta decisión |
|---|---|
| [F30](../investigacion-ia/README.md) | Evidencia científica y normativa (89 trabajos, 16 normas); decisiones D-01 a D-30; condiciones G0-1 a G0-6 |
| [F33](../diseno-inteligente/README.md) | Diseño funcional del alcance B, ADR-005 (PROPUESTA) y los 15 criterios G0 |
| [F34](../datos-sinteticos/README.md) | Contrato de datos y dataset 100 % sintético; satisface G0-04 y apoya G0-10 y G0-11 |
| F34A (este paquete) | Matriz G0, checklist jurídico, privacidad preliminar, instrumento de necesidad, modelo de amenazas y RF candidatos |

## 9. Registro de decisión del equipo

**Estado actual: PENDIENTE.** Ningún integrante ha registrado su decisión. Cada fila se completa a mano por la persona que decide; nadie puede completarla por otra.

Valores admitidos en «Decisión»: `PENDIENTE`, `APRUEBA`, `APRUEBA CON OBSERVACIONES`, `RECHAZA`.

| Nombre | Rol | Fecha | Decisión | Observación |
|---|---|---|---|---|
| — | Integrante del equipo | — | PENDIENTE | — |
| — | Integrante del equipo | — | PENDIENTE | — |
| — | Integrante del equipo | — | PENDIENTE | — |
| — | Docente del curso (opcional, consultivo) | — | PENDIENTE | — |

**Regla de registro:**

- ADR-005 pasa a APROBADA solo si los tres integrantes registran `APRUEBA` o `APRUEBA CON OBSERVACIONES`, con fecha, en un commit propio de gobierno.
- Al aprobarse, el ADR se publica junto a los demás ADR sin cambiar su número, y G0-14 pasa a CUMPLIDO.
- Aprobar ADR-005 **no** cambia por sí solo el estado de G0.
