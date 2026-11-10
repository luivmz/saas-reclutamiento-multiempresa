# F36-SBX — Expediente técnico para la revisión final

> Documento del 07/11/2026, en la rama local `feature/entrega-academica-demo`, desde `2f6d0e0`. **Solo documenta y prepara.** No emite actos, no cambia el gate, el validador ni el gobierno, y no inicia F37-SBX.
>
> Estado vigente, sin cambios: F36-SBX = EN DISEÑO; F36-SBX-GATE = NO SUPERADO; F37-SBX = BLOQUEADA; F36–F40 = BLOQUEADAS; alcance C = BLOQUEADO; datos reales = PROHIBIDOS. Q2 está ADOPTADA (RR-001, `5036393`), sin facultades delegadas utilizables.

## 1. Contenido

| Pieza | Documento | Estado |
|---|---|---|
| D-10 · Vigencia del charter tras SEG | [`../decisiones-d10-d11/D-10_BORRADOR_Vigencia_Charter_F36SBX.md`](../decisiones-d10-d11/D-10_BORRADOR_Vigencia_Charter_F36SBX.md) | BORRADOR — PENDIENTE DE DECISIÓN (incorporado en `2f6d0e0`) |
| D-11 · Autorizaciones operativas del contrato 10 | [`../decisiones-d10-d11/D-11_BORRADOR_Autorizaciones_Operativas_Contrato10.md`](../decisiones-d10-d11/D-11_BORRADOR_Autorizaciones_Operativas_Contrato10.md) | BORRADOR — PENDIENTE DE DECISIÓN (incorporado en `2f6d0e0`) |
| Especificación S del sucesor B-01, versión 2.2 (T-09 (a-ii) medido, revocación, criterios de aceptación, pruebas y dependencias) | [`F36SBX_B01_Especificacion_S.md`](F36SBX_B01_Especificacion_S.md) | CANDIDATA A AUDITORÍA — NO IMPLEMENTADA |
| Sondas de S: T-09, revocación y trasplante | [`sondas-b01/README.md`](sondas-b01/README.md) | PREPARACIÓN, sin cambios en el validador |
| Conclusiones que respaldan las evidencias | [`F36SBX_Conclusiones_Evidencias.md`](F36SBX_Conclusiones_Evidencias.md) | Documental |
| Decisiones propuestas y su orden | [`F36SBX_Decisiones_Propuestas.md`](F36SBX_Decisiones_Propuestas.md) | BORRADOR — PENDIENTE DE DECISIÓN |
| Preparación de F37-SBX y F38-SBX (ML-02) | [`../prototipo-ml02/README.md`](../prototipo-ml02/README.md) | PROTOTIPO DE DISEÑO, estático, y PROPUESTA de plan |

## 2. Antecedentes que se citan y no se modifican

- **AF6:** `88fd3d2`, en `docs/f36-sbx-gate-preparacion-af6`.
- **H preliminar:** `1d5d6aa`, con la especificación y el plan de pruebas de B-01, en `feature/f36-sbx-gate-transition-h`.
- **Q:** `061ba68`.

Las tres son ramas locales, conservadas sin integrar. S revisa la especificación de H sin copiarla ni sustituir su historia (D-08).

- **Q2 V:** `8b1f068`.
- **Borradores de adopción:** `1dd3f24`.
- **RR-001:** `5036393`.
- **Reconciliación tras SEG:** `reconciliacion-gobierno/F36SBX_Reconciliacion_Estado_Gobierno.md`.

## 3. Validador en esta rama

`python -I -B docs/academico/tools/f36sbx/validate_f36sbx.py` da **55/4**: las cuatro fallas son la rama no admitida, las 18 rutas de SEG fuera del paquete, sus 11 entradas de runtime y, derivada de ellas, la divergencia de FG-01 y FG-05. Es el mismo resultado que los candidatos Q2 anteriores.

Los archivos de producto de esta entrega (`app/`, `database/`, `resources/`, `tests/` y `cypress/`) alargan esas dos listas, pero no añaden ninguna comprobación fallida. El resultado calculado sigue NO SUPERADO. S §5.9 (T-09) explica por qué un H de `develop` no pasaría FRZ.

## 4. Para Codex (auditoría única final)

- **Revisar:** D-10, D-11, S, las conclusiones (C-01 a C-19), las decisiones propuestas y el prototipo de ML-02. En la rama de continuación, los puntos de S v2 están en su §12.
- **Comprobar:** que nada de lo anterior afirme un acto, un voto, una delegación o un gate superado, y que el prototipo no implemente ninguna EI.
- **Producto:** los cambios están descritos en el [informe de la entrega](../../../entrega-final/informe-final.md).
