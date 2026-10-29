# F36-SBX — Roadmap propuesto F36–F40: ML-01, ML-02 y línea visual

> **PROPUESTA — NO VIGENTE.** Documento del 29/10/2026, en la rama `docs/f36-sbx-team-governance-proposal`. **No reescribe** el [mapa F33](../../diseno-inteligente/F33_Mapa_F34_F40.md), el contrato congelado de RF-29, la [matriz de capacidades](../F36SBX_Matriz_Capacidades.md) ni ningún gate. Este incremento no entrena modelos ni toca el ML ni el frontend.
>
> Estados vigentes, sin cambios: G0 real = NO APROBADA; F35-SBX = CERRADA Y CONGELADA; F36-SBX = EN DISEÑO; F36-SBX-GATE = NO SUPERADO; F37-SBX = BLOQUEADA; alcance C = BLOQUEADO; datos reales = PROHIBIDOS.

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

  La calibración se evaluó y se rechazó (15B §7). El AP de test es 0,7691, frente a 0,4252 del baseline operacional, con el veredicto «PREDICTIVE GO WITH LIMITATIONS».
- **La integración con Laravel (F16).** `target_completion_at` (GAP-01), un cliente HTTP con validación y respaldo, la tarjeta de riesgo y `ML_SERVICE_ENABLED`.
- **La validación (F17)** está «validado técnicamente en entorno de pruebas, NO validado institucionalmente ni autorizado para producción» ([F17](../../../v1.1/phase-17-ml-validation.md)). Cypress lo cubre con E2E-15.
- **La documentación** está en `docs/v1.1/ml/`: un [*model card* en borrador](../../../v1.1/ml/model-card-draft.md), la especificación del dataset, el plan de evaluación, la ética y la supervisión humana, y los contratos.

**Falta [H].**

- Promover RF-29 al baseline: la decisión 12 está pendiente ([scope](../../../v1.1/scope-preliminary.md)).
- La validación institucional, que es N5 y externa.
- Pasar el *model card* de borrador a definitivo.
- La F36 productiva del mapa, que exige la G0 con al menos CON RESTRICCIONES y el alcance B.
- El modelo entrenado no se versiona: `ml-service/README.md` lo regenera con `recruitment_ml.training.experiment`.

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

**Los datos sintéticos no eliminan esas restricciones.** El charter §4 rige «aunque el gate se supere», y EI-21 bloquea el audio «también con voz sintética».

## 4. Línea visual, de accesibilidad y de rendimiento [H]

- **Lo que hay.** El rediseño, el *motion* con movimiento reducido, el CSS 3D solo en la portada y la QA visual y de accesibilidad están integrados (fases 18 a 21). ADR-003 limita el 3D a la tarjeta de la portada: no se amplía sin una decisión nueva del equipo. La promoción de RNF-C está pendiente (decisión 13).
- **Lo que está pendiente.** Dos pruebas manuales: con un lector de pantalla real y de rendimiento en un equipo modesto. Esta última es A-05, INFO DEFERRED en [F26](../../../v1.1/phase-26-release-closeout.md); las dos constan en las [notas de v1.1](../../../v1.1/release-notes-v1.1.md).
- **Dependencias reales.** La línea no depende de la G0, del F36-SBX-GATE ni de F37-SBX. La rigen los contratos del producto (`data-cy` y Cypress), las skills `frontend-design`, `animate` y `reviewing-a11y`, y los niveles N1 y N2 de Q2. Un cambio de interfaz que afecte a un flujo cubierto exige Cypress.
- **El panel F40 del mapa F33** es otra cosa: un panel sin veredictos sobre personas, que depende de la G0 y de F38 a F39.

## 5. Roadmap propuesto [P]

| Etapa | Módulo | Contenido | Condición de entrada | Estado |
|---|---|---|---|---|
| R0 | Gobierno | Adoptar Q2 o mantener el 3/3 con actos reales; resolver D-10 (FRZ tras SEG) y D-11 (autoridad de N3) | E-02, E-03 y E-04, y P4 de Q2 | Pendiente |
| R1 | ML-01 | Mantenimiento correctivo y documental dentro del contrato congelado, incluido el *model card* definitivo | N1 o N2 | Se puede hacer ya |
| R2 | ML-01 | Un experimento nuevo (variables, modelo o umbral), solo con datos sintéticos, con *freeze* y evaluación nuevos | Decisión del equipo para cambiar el contrato congelado, auditoría (N2) y RD | No emitida |
| R3 | ML-01 | F36 y F38 productivas del mapa | G0 real con al menos CON RESTRICCIONES y validación institucional (N5) | Bloqueada |
| R4 | ML-02 | Continuar el diseño (F36-SBX): D-01 a D-09, sucesor B-01 (D-02b), D-05, D-07, D-10, y fijar y auditar H (FG-02) | Las de la [reconciliación §6](F36SBX_Reconciliacion_Estado_Gobierno.md) | En diseño |
| R5 | ML-02 | F37-SBX-A: EI-01 a EI-07, y EI-09 si se confirma F36-M02; sintético y sin dependencias nuevas | Gate superado con FG-02, FG-03, FG-10 y FG-12 auténticos | Bloqueada |
| R6 | ML-02 | F37-SBX-B: EI-08, EI-10, EI-11, EI-12 y EI-24 | F37-SBX-A cerrada, ADR sucesor aprobado por los tres integrantes (no delegable) y FG-10 | Bloqueada |
| R7 | ML-02 | F38 a F40 productivas | G0 real y el ADR de alcance que corresponda | Bloqueadas |
| V1 | Visual | Las pruebas manuales pendientes: lector de pantalla y equipo modesto | N1 o N2 | Se puede hacer ya |
| V2 | Visual | Ampliar el 3D fuera de la portada | Decisión nueva del equipo (ADR-003) | No emitida |
| V3 | Visual | Promover RNF-C | Decisión 13 | Pendiente |

## 6. Diferencias frente a la distribución anterior [P]

- **Módulos con nombre propio.** El mapa F33 llamaba F36 al ML baseline del proceso, y F36-SBX reutilizó ese número para el diseño de la inteligencia sobre evidencia. Se propone nombrar los módulos ML-01 y ML-02 sin depender del número de fase, conservar las dos numeraciones sin reescribir F33 y confirmar F36-M01 en FG-03.
- **ML-01 ya existe en experimental.** Se implementó en las fases 15 a 17 de v1.1, antes del mapa. El roadmap lo registra así y no como una F36 futura. La F36 productiva sigue bloqueada.
- **La integración con Laravel de ML-01 también existe en experimental** (fase 16). La F38 productiva sigue bloqueada.
- **La línea visual es independiente** de F36–F40 y de los gates. No se confunde con el panel F40.
- **F37-SBX conserva sus dos etapas.** La aprobación del ADR del alcance C queda fuera de cualquier delegación de Q2.
- **Nada cambia de nivel de autorización.** Ningún módulo pasa a producción y ninguna EI queda autorizada.

## 7. Condiciones para entrenar, experimentar e integrar [P]

| Módulo | Entrenar | Experimentar | Integrar |
|---|---|---|---|
| ML-01 | Solo con datos sintéticos, en un experimento nuevo con su *freeze*. Cambiar el contrato congelado exige una decisión del equipo y una auditoría | Ídem, sin cambiar RF-23 ni el alcance del proceso | La integración experimental ya existe. Una productiva exige la G0 real y la validación institucional (N5) |
| ML-02 | **No** en este ciclo: EI-22 está BLOCKED | Solo en F37-SBX-A, una vez superado el gate, con datos sintéticos | **No**: EI-23 está BLOCKED, y las F38 a F40 productivas exigen la G0 real |
| Línea visual | No aplica | Como desarrollo ordinario, en N1 o N2, con Cypress | Por el flujo normal. Ampliar el 3D exige una decisión nueva |

## 8. Prohibiciones que ningún roadmap levanta [H]

- Datos reales, CV reales y PII real.
- Audio o vídeo real, biometría, reconocimiento facial e identificación por voz.
- Inferencias sobre emociones, personalidad, honestidad, inteligencia, estrés o nerviosismo, y cualquier inferencia desde el rostro, los gestos, la voz, la prosodia o el acento.
- Selección y decisión automática de contratación.
- Cambiar RF-23.
- Scoring, ranking o recomendación de candidatos.
- Alimentar producción o crear endpoints o migraciones productivas.

Rigen también en cualquier F37-SBX ([charter §4](../F36SBX_Charter.md)), y el mapa F33 los mantiene siempre bloqueados en este ciclo.
