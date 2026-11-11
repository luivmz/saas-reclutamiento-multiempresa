# F36-SBX — Conclusiones que respaldan las evidencias

> Documento del 07/11/2026, en la rama local `feature/entrega-academica-demo`, desde `2f6d0e0` (D-10 y D-11 en borrador) y RR-001 (`5036393`). **Solo documenta.** No registra actos, no cambia estados y no supera ningún gate.

Cada conclusión indica su grado de respaldo:

- **ACREDITADO:** consta en Git, en un registro versionado o en una ejecución de esta sesión;
- **PREPONDERANTE:** lo respaldan la mayoría de las fuentes, pero no lo cierran;
- **ABIERTO:** las fuentes no lo resuelven.

## 1. Gobierno

| # | Conclusión | Respaldo | Evidencia |
|---|---|---|---|
| C-01 | Q2 está ADOPTADA para V (`8b1f068`, árbol `b5b8171`) desde el 07/11/2026, solo hacia adelante | ACREDITADO | RR-001 (`5036393`), §1–§5 |
| C-02 | No hay facultades delegadas utilizables: DF-02 está acreditada y DF-03 está pendiente de su texto íntegro | ACREDITADO | RR-001 §2 y §4 |
| C-03 | Las operaciones del contrato 10 que no cubre una delegación van al mecanismo colegiado, que V nombra pero no define | ACREDITADO | V §4 N3 y §10; D-11 §1 |
| C-04 | Las integraciones y publicaciones de SEG-01 a SEG-04 se hicieron con autorizaciones operativas de Luis, una por operación. No consta ningún acto de Fredy ni de Anthony | ACREDITADO | D-11 §3; transcripciones fuera de Git con su SHA-256 |
| C-05 | La autorización del equipo para esas operaciones no está acreditada más allá de esos actos; su resultado técnico sí lo respaldan la auditoría, la conservación del árbol y la CI en verde | ACREDITADO | D-11 §3 |
| C-06 | Tres mensajes de merge (`b69c6c3`, `f5b7c59` y `2e53786`) dicen «authorized by the team» frente a la constancia de autorizaciones de Luis | ACREDITADO | `git log`; D-11 §3 |

## 2. Vigencia del charter (D-10)

| # | Conclusión | Respaldo | Evidencia |
|---|---|---|---|
| C-07 | SEG modificó 5 archivos de `app/` y 6 de `tests/` en `develop` después del charter, entre el 28/10 21:05:26 y el 29/10 12:37:10. No tocó dependencias, F35-SBX ni el paquete F36-SBX, y `main` no cambió | ACREDITADO | `git diff 5545694..9dd76c4`; D-10 §3 y §4 |
| C-08 | No hay ninguna revocación registrada ni una retirada de la autorización por el equipo | ACREDITADO | `f36sbx_gate_state.json`: `revocation = null` |
| C-09 | La lectura sistemática de §7 (solo cambios hechos por F36-SBX o dentro de ella) tiene más respaldo que la literal amplia, sobre todo por la regla «Anclaje», escrita antes de SEG | PREPONDERANTE | D-10 §5.2; `06e933e` |
| C-10 | Si SEG activó la cláusula | ABIERTO | Corresponde a los tres integrantes (D-10 §6 y §7) |
| C-11 | El validador v3 no puede representar REVOCADO: registrar D10-2 exige un sucesor | ACREDITADO | `allowed_states()`, `:1290`; regla GATE, `:2877`; S §5.8 |

## 3. Gate y sucesor

| # | Conclusión | Respaldo | Evidencia |
|---|---|---|---|
| C-12 | F36-SBX-GATE = NO SUPERADO: FG-02, FG-03, FG-10 y FG-12 están PENDIENTES y no hay evidencia | ACREDITADO | Estado del gate; validador |
| C-13 | Con el validador v3, el gate no puede llegar a SUPERADO ni con evidencia auténtica. Hace falta B-01 | ACREDITADO | Especificación de H §2; S §1 |
| C-14 | Un H que descienda de `develop` no podría pasar FRZ por SEG. Hace falta decidir T-09 | ACREDITADO | Validador en esta rama: 55/4, con FRZ y GATE en falla. S §5.9 |
| C-15 | El validador sigue intacto desde AF5 (SHA-256 `87ad2f6f…`) | ACREDITADO | `sha256sum` sobre `4a2b2d7` y `2f6d0e0` |

## 4. Producto y ML

| # | Conclusión | Respaldo | Evidencia |
|---|---|---|---|
| C-16 | El flujo RF-01 a RF-27 funciona de principio a fin con datos ficticios, incluida la decisión humana y su auditoría | ACREDITADO | PHPUnit, Cypress (E2E-13 y E2E-20); [informe de entrega](../../../entrega-final/informe-final.md) |
| C-17 | ML-01 (RF-29) funciona en su configuración experimental congelada: el artefacto se reconstruye desde el *freeze* `9ee1843…` con el umbral `0.1679418172266036`, y Laravel recibe una estimación en vivo para la vacante del escenario demo | ACREDITADO | pytest de `ml-service`; la estimación en vivo del informe de entrega |
| C-18 | Con los datos demo anteriores, ML-01 no se podía demostrar: ninguna vacante entraba en la ventana de consulta | ACREDITADO | DEF-18; `DemoSeederOperationalRiskScenarioTest`, RED y GREEN |
| C-19 | ML-02 no tiene implementación ni entrenamiento. F37-SBX sigue BLOQUEADA y EI-22 (entrenamiento) y EI-23 (UI productiva) están BLOCKED | ACREDITADO | Matriz de capacidades; [prototipo ML-02](../prototipo-ml02/README.md), estático y sin cálculo |
