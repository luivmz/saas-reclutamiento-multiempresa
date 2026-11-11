# F36-SBX — Decisiones propuestas para la revisión final

> **BORRADOR — PENDIENTE DE DECISIÓN.** Documento del 07/11/2026, en la rama local `feature/entrega-academica-demo`. Reúne las decisiones que el expediente deja preparadas. **Ninguna está emitida.** Nadie ha votado ni delegado nada en este incremento, y ningún gate cambia.

## 1. Cómo se decide cada una hoy

Sin facultades delegadas utilizables (RR-001 §4), todas las decisiones de esta tabla se toman con un acto propio de cada integrante, por su canal, sobre la misma versión fijada del documento que corresponda. El silencio no cuenta.

Las decisiones del gate (FG-03, FG-10 y FG-12) siguen el gate v3: votos 3/3 de las identidades exactas.

## 2. Orden recomendado

| # | Decisión | Documento | Opciones | Recomendación, no vinculante | Depende de |
|---|---|---|---|---|---|
| 1 | **D-11**: procedimiento colegiado del contrato 10 | [`D-11_BORRADOR_…`](../decisiones-d10-d11/D-11_BORRADOR_Autorizaciones_Operativas_Contrato10.md) | P-01 a P-06 | P-01 (i) 3/3; P-02 (ii); P-03 (i) hasta una aclaración; P-04 (ii) con fecha de fin; P-05 (i); P-06 correo institucional | — |
| 2 | **D-10**: vigencia del charter tras SEG | [`D-10_BORRADOR_…`](../decisiones-d10-d11/D-10_BORRADOR_Vigencia_Charter_F36SBX.md) | D10-1, D10-2 o D10-3, y la enmienda del Anexo 3 | D10-1 con la enmienda | Se puede decidir con tres actos aunque D-11 no esté adoptada |
| 3 | **T-09**: base y anclaje después de SEG | [S §5.9](F36SBX_B01_Especificacion_S.md#59-base-anclaje-y-frz-después-de-seg-t-09-nuevo) | (a-i), (a-ii), (b), (c) o (d) | (a-ii): una rama de H nueva desde el commit `55f758e`, con el paquete trasplantado (S §5.9.3; sondas V-1 a V-7) | D-10 solo para (b); las demás, D-02b |
| 4 | **T-01 a T-08** | [S §9](F36SBX_B01_Especificacion_S.md#9-decisiones-de-diseño) | Las de S | Las recomendaciones de S | Auditoría de S |
| 5 | **D-02b**: autorizar la implementación de B-01 | S §2 y §7 | Autorizar o no, con el alcance de S | Solo tras la auditoría favorable de S y con D-10 determinada | 2, 3 y 4 |
| 6 | **D-08**: integrar la preparación AF6, H y Q, o sustituirla por S | `88fd3d2`, `1d5d6aa`, `061ba68` | Integrar, sustituir o archivar | Sustituir H por S como base de diseño y conservar AF6, H y Q como historia | — |
| 7 | **F36-M01**: numeración de F36-SBX frente al mapa F33 | Charter §5 | Confirmar u otra | Confirmar, dentro de FG-03 | FG-02 |
| 8 | **F36-M02**: ¿EI-09 entra en el alcance B? | Matriz de capacidades | Sí o no | Excluir EI-09 de la primera autorización; así FG-12 queda en NO APLICA | — |
| 9 | **FG-03 / FG-10 / FG-12** | Gate §8 | Las del gate | Solo después de H y FG-02 | 5 |
| 10 | **Decisiones 12 y 13**: promover RF-28, RF-29 y RNF-C | `docs/v1.1/scope-preliminary.md` | Promover o no | Fuera de F36-SBX; la entrega no las necesita | — |

## 3. Lo que esta entrega no necesita decidir

La entrega académica se puede presentar con F36-SBX en diseño y el gate NO SUPERADO. El producto (RF-01 a RF-27), ML-01 experimental y la línea visual no dependen del gate (roadmap §4 y §7). F37-SBX, ML-02 implementado y F38–F40 se presentan como **BLOQUEADOS**, con su preparación y el prototipo estático de ML-02.

## 4. Evidencia que falta para cada acto

| Acto | Evidencia |
|---|---|
| D-10 y D-11 | La revisión de Codex sobre la versión fijada y los tres actos individuales sobre ella |
| D-02b | La auditoría de S, D-10 determinada y el acto de D-02b (colegiado) |
| FG-02 | Un informe de auditoría sobre H, con su bloque canónico |
| FG-03, FG-10 y FG-12 | Tres votos de las identidades exactas, o la variante RD solo con DF-02 y DF-03 vigentes |
| DF-03 | El texto íntegro del documento que el correo del 04/11 anunciaba adjuntar |
