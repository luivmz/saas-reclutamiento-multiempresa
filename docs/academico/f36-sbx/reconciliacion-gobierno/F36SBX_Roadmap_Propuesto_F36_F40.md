# F36-SBX — Roadmap propuesto F36–F40: ML-01, ML-02 y línea visual

> **PROPUESTA — NO VIGENTE.** Documento del 29/10/2026, en la rama `docs/f36-sbx-team-governance-proposal`. **No reescribe** el [mapa F33](../../diseno-inteligente/F33_Mapa_F34_F40.md), el contrato congelado de RF-29, la [matriz de capacidades](../F36SBX_Matriz_Capacidades.md) ni ningún gate. Este incremento no entrena modelos ni toca el ML ni el frontend.
>
> Estados vigentes, sin cambios: G0 real = NO APROBADA; F35-SBX = CERRADA Y CONGELADA; F36-SBX = EN DISEÑO; F36-SBX-GATE = NO SUPERADO; F37-SBX = BLOQUEADA; alcance C = BLOQUEADO; datos reales = PROHIBIDOS.
>
> **Versión corregida** tras la auditoría de Codex sobre `729babb`. Recoge las correcciones de Q2-M03, Q2-M04, Q2-M05 y Q2-L02, cuya matriz está en la respuesta a la auditoría de esta carpeta.

Cada afirmación lleva su naturaleza: [H] hecho comprobado; [R] afirmación recibida; [P] propuesta.

## 1. Tres numeraciones que no se confunden [H]

| Línea | Qué es | Estado |
|---|---|---|
| Fases 14 a 17 de v1.1 | ML del proceso de RF-29, anterior al mapa F33 | Implementado e integrado de forma experimental en `develop` |
| Mapa F33, F34 a F40 (producto) | Dataset y gobernanza (F34); pipeline de evidencia (F35); ML baseline del proceso, CAP-26 (F36); explicabilidad y equidad (F37); integración Laravel con ML (F38); evaluación (F39); panel (F40) | F34 se hizo solo con datos sintéticos. Las fases productivas de F35 a F40 no comienzan sin la G0 aprobada, y la G0 real = NO APROBADA |
| Variantes sandbox (`-SBX`) | G0-SBX (F34E), F35-SBX (pipeline determinista sintético), F36-SBX (autorización y diseño de la inteligencia sobre evidencia) y F37-SBX | F35-SBX = CERRADA Y CONGELADA; F36-SBX = EN DISEÑO; F37-SBX = BLOQUEADA |

F36-SBX no es la F36 del mapa ([charter §5](../F36SBX_Charter.md)). La numeración está pendiente de confirmarse (F36-M01).

## 2. ML-01: riesgo de demora del proceso (RF-29)

**Implementado [H].**

- **El servicio (F15).** El servicio `ml-service/` incluye el dataset sintético, el entrenamiento y FastAPI, con `/health`, `/v1/model-info` y `/v1/predict`. Su contrato científico está congelado:
  - *freeze* `9ee1843055e7…`;
  - umbral `0.1679418172266036`;
  - Logistic Regression con `C=10`, `class_weight=None` y `StandardScaler`.

  La calibración se evaluó y se rechazó (15B §7). El AP de test es 0,7691, frente a 0,4252 del baseline operacional, con el veredicto «PREDICTIVE GO WITH LIMITATIONS». Son resultados documentados del experimento; esta sesión no los reprodujo.
- **La integración con Laravel (F16).** `target_completion_at` (GAP-01), un cliente HTTP con validación y respaldo, la tarjeta de riesgo y `ML_SERVICE_ENABLED`.
- **La validación (F17)** está «validado técnicamente en entorno de pruebas, NO validado institucionalmente ni autorizado para producción» ([F17](../../../v1.1/phase-17-ml-validation.md)). Cypress lo cubre con E2E-15.
- **La documentación** está en `docs/v1.1/ml/`: un [*model card* en borrador](../../../v1.1/ml/model-card-draft.md), la especificación del dataset, el plan de evaluación, la ética y la supervisión humana, y los contratos.

**Cinco actividades que no se confunden:**

| Actividad | Qué es | Fuente vigente o condición | Estado |
|---|---|---|---|
| Reconstruir el artefacto del experimento congelado | Regenerar el modelo desde el protocolo congelado y aprobado, con `python -m recruitment_ml.serving.build_artifact`. El builder verifica el dataset, la configuración y la partición, y registra el SHA-256 del binario | `ml-service/README.md`, sección del servicio experimental (15C), y la skill `ml-risk-service`. Conserva variables, modelo, umbral y evidencia congelada, y **no abre un experimento nuevo** | Se puede hacer cuando haga falta. Este incremento no lo ejecuta |
| Mantenimiento que conserva el contrato | Correcciones, pruebas y QA del servicio y de su integración, sin cambiar variables, modelo, umbral ni evidencia | La skill `ml-risk-service`, la documentación de F15 a F17 y las reglas vigentes de calidad | Se puede hacer |
| Experimento nuevo con cambios científicos | Cambiar variables, modelo o umbral, o entrenar con otro protocolo | Una decisión expresa del equipo, un protocolo y una evaluación nuevos y su auditoría. Nunca se sobrescribe la evidencia congelada | No emitida |
| Integración experimental existente | El cliente HTTP, el respaldo y la tarjeta de riesgo (F16) | Existe. Laravel solo llama al servicio con `ML_SERVICE_ENABLED`, y sin él la página funciona igual | Existe |
| Producción | Las F36 y F38 productivas del mapa | La G0 real con al menos CON RESTRICCIONES y la validación institucional (N5) | Bloqueada |

**Falta [H].**

- Promover RF-29 al baseline: la decisión 12 está pendiente ([scope](../../../v1.1/scope-preliminary.md)).
- La validación institucional, que es externa.
- Pasar el *model card* de borrador a definitivo.
- La F36 productiva del mapa, que exige la G0 con al menos CON RESTRICCIONES y el alcance B.

## 3. ML-02: inteligencia sobre evidencia de entrevistas y candidatos

**La visión [R]** es una línea de investigación sobre la evidencia de entrevistas y de candidatos.

**El alcance que autorizan hoy los documentos [H].**

- **Qué autoriza el charter.** Solo diseño. F37-SBX = BLOQUEADA.
- **Capacidades de la matriz, según su estado:**
  - **ALLOWED** para diseño, en alcance B: EI-01 a EI-07.
  - **CONDITIONAL:** EI-09, en alcance B; EI-08, EI-10, EI-11, EI-12 y EI-24, en alcance C.
  - **BLOCKED:** EI-13 a EI-23.

| Lo que la visión no puede autorizar por inferencia | Dónde está bloqueado |
|---|---|
| Selección o rechazo laboral automatizado; scoring, ranking o recomendación | EI-19; charter §4.6 y §4.8; F33 |
| Inferencias emocionales o de personalidad, también desde rostro, gestos, voz o prosodia | EI-20; charter §4.4 y §4.5 |
| Procesar audio o vídeo, también con voz sintética, y la transcripción automática | EI-21; charter §4.2 |
| Entrenar o ajustar modelos con evidencia, también de forma multimodal | EI-22 |
| Datos reales de candidatos e integración productiva | EI-23; charter §4.1 y §4.10; contrato 7 |
| Resúmenes y veredictos sobre candidatos, un LLM sobre su evidencia, OCR y similitud entre candidatos | EI-13, EI-14, EI-16, EI-15 y EI-18 |

**Los datos sintéticos no eliminan esas restricciones.** El charter §4 rige «aunque el gate se supere», y EI-21 bloquea el audio «también con voz sintética». La frontera es la inferencia, la puntuación o la recomendación automática sobre personas en estas líneas inteligentes; no afecta a los RF existentes, como el cálculo de RF-21.

## 4. Línea visual, de accesibilidad y de rendimiento [H]

- **Lo que hay.** El rediseño, el *motion* con movimiento reducido, el CSS 3D solo en la portada y la QA visual y de accesibilidad están integrados (fases 18 a 21). ADR-003 limita el 3D a la tarjeta de la portada: no se amplía sin una decisión nueva del equipo. La promoción de RNF-C está pendiente (decisión 13).
- **Lo que está pendiente.** Dos pruebas manuales, con herramientas reales y datos ficticios: con un lector de pantalla y de rendimiento en un equipo modesto. Esta última es A-05, INFO DEFERRED en [F26](../../../v1.1/phase-26-release-closeout.md); las dos constan en las [notas de v1.1](../../../v1.1/release-notes-v1.1.md).
- **Fuente vigente.** La línea no depende de la G0, del F36-SBX-GATE ni de F37-SBX. La rigen hoy los contratos del producto (`data-cy` y Cypress), las skills `frontend-design`, `animate` y `reviewing-a11y`, y ADR-003. Un cambio de interfaz que afecte a un flujo cubierto exige Cypress. Q2 clasificaría estas tareas como N1 o N2 si se adopta, pero esa clasificación **no es la fuente** de los permisos actuales.
- **El panel F40 del mapa F33** es otra cosa: un panel sin veredictos sobre personas, que depende de la G0 y de F38 a F39.

## 5. Roadmap propuesto [P]

La columna «Clasificación en Q2» no crea permisos: solo dice cómo se clasificaría cada etapa si Q2 se adoptara.

| Etapa | Módulo | Contenido | Fuente vigente o condición actual | Clasificación en Q2 | Estado |
|---|---|---|---|---|---|
| R0 | Gobierno | Adoptar una versión fijada de Q2 o mantener el mecanismo colegiado con actos reales; D-10, pendiente: determinación fundada de hechos, ámbito, periodo y posibles efectos históricos conforme al contrato aplicable, con registro declarativo, mientras que cualquier autorización nueva o enmienda normativa regirá únicamente hacia adelante; D-11, la autoridad del contrato 10 hacia adelante | Q2 §9 y [reconciliación §3.3 y §5.6](F36SBX_Reconciliacion_Estado_Gobierno.md) | N4 | Pendiente |
| R1 | ML-01 | Mantenimiento correctivo y documental dentro del contrato congelado, incluido el *model card* definitivo | La skill `ml-risk-service` y las reglas vigentes | N1 o N2 | Se puede hacer ya |
| R1b | ML-01 | Reconstruir el artefacto del experimento congelado | `ml-service/README.md` (15C) | N1 | Se puede hacer cuando haga falta |
| R2 | ML-01 | Un experimento nuevo con cambios científicos, solo con datos sintéticos | Decisión expresa del equipo, protocolo y evaluación nuevos, y auditoría | N2, con la decisión expresa | No emitida |
| R3 | ML-01 | F36 y F38 productivas del mapa | G0 real con al menos CON RESTRICCIONES y validación institucional | N5 | Bloqueada |
| R4 | ML-02 | Continuar el diseño de F36-SBX: D-01 a D-09 y el sucesor B-01 (D-02b). Si se elige la estrategia H, también D-05, D-06 y D-07, y fijar y auditar H (FG-02) | Charter §1 y las condiciones de la reconciliación §6 | N2 y N4 | En diseño |
| R5 | ML-02 | F37-SBX-A: EI-01 a EI-07, y EI-09 si se confirma F36-M02; sintético y sin dependencias nuevas | El gate superado con FG-02, FG-03, FG-10 y FG-12 auténticos, y la vigencia material de la autorización de F36-SBX determinada (D-10) | N4 | Bloqueada |
| R6 | ML-02 | F37-SBX-B: EI-08, EI-10, EI-11, EI-12 y EI-24 | F37-SBX-A cerrada, el ADR sucesor aprobado por los tres integrantes y FG-10 | N4, no delegable | Bloqueada |
| R7 | ML-02 | F38 a F40 productivas | La G0 real y el ADR de alcance que corresponda | N5 | Bloqueadas |
| V1 | Visual | Las pruebas manuales pendientes: lector de pantalla y equipo modesto | Las skills de frontend, ADR-003, `data-cy` y Cypress | N1 o N2 | Se puede hacer ya |
| V2 | Visual | Ampliar el 3D fuera de la portada | Una decisión nueva del equipo (ADR-003) | N4 | No emitida |
| V3 | Visual | Promover RNF-C | La decisión 13 | N4 | Pendiente |

## 6. Diferencias frente a la distribución anterior [P]

- **Módulos con nombre propio.** El mapa F33 llamaba F36 al ML baseline del proceso, y F36-SBX reutilizó ese número para el diseño de la inteligencia sobre evidencia. Se propone nombrar los módulos ML-01 y ML-02 sin depender del número de fase, conservar las dos numeraciones sin reescribir F33 y confirmar F36-M01 en FG-03.
- **ML-01 ya existe en experimental.** Se implementó en las fases 15 a 17 de v1.1, antes del mapa, y su artefacto se reconstruye desde el *freeze* aprobado (R1b) sin abrir un experimento nuevo. El roadmap lo registra así, no como una F36 futura. La F36 productiva sigue bloqueada.
- **La integración con Laravel de ML-01 también existe en experimental** (fase 16). La F38 productiva sigue bloqueada.
- **La línea visual es independiente** de F36–F40 y de los gates. No se confunde con el panel F40.
- **F37-SBX conserva sus dos etapas.** La aprobación del ADR del alcance C queda fuera de cualquier delegación de Q2.
- **Nada cambia de nivel de autorización.** Ningún módulo pasa a producción y ninguna EI queda autorizada.

## 7. Condiciones para reconstruir, entrenar, experimentar e integrar [P]

| Módulo | Reconstruir lo congelado | Entrenar un experimento nuevo | Experimentar | Integrar |
|---|---|---|---|---|
| ML-01 | Sí, desde el *freeze* aprobado, sin cambiar variables, modelo, umbral ni evidencia (15C) | Solo con datos sintéticos, con decisión expresa del equipo, protocolo, evaluación y auditoría nuevos, sin sobrescribir la evidencia congelada | Dentro del experimento existente, o de uno nuevo si se decide | La integración experimental ya existe. Una productiva exige la G0 real y la validación institucional |
| ML-02 | No aplica: no hay un modelo congelado | **No** en este ciclo: EI-22 está BLOCKED | Solo en F37-SBX-A, una vez superado el gate | **No**: EI-23 está BLOCKED, y las F38 a F40 productivas exigen la G0 real |
| Línea visual | No aplica | No aplica | Como desarrollo ordinario, con Cypress | Por el flujo normal. Ampliar el 3D exige una decisión nueva |

Esta distinción no habilita ML-02 ni producción.

## 8. Prohibiciones que ningún roadmap levanta [H]

- Datos reales, CV reales y PII real.
- Audio o vídeo real, biometría, reconocimiento facial e identificación por voz.
- Inferencias sobre emociones, personalidad, honestidad, inteligencia, estrés o nerviosismo, y cualquier inferencia desde el rostro, los gestos, la voz, la prosodia o el acento.
- Selección y decisión automática de contratación.
- Cambiar RF-23.
- Scoring, ranking o recomendación de candidatos.
- Alimentar producción o crear endpoints o migraciones productivas.

Rigen también en cualquier F37-SBX ([charter §4](../F36SBX_Charter.md)), y el mapa F33 los mantiene siempre bloqueados en este ciclo.
