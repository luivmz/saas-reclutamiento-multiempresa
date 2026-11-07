# F36-SBX — Especificación S del sucesor B-01

> **CANDIDATA A AUDITORÍA — NO IMPLEMENTADA.** Documento del 07/11/2026, en la rama local `feature/entrega-academica-demo`. Revisa la especificación de `1d5d6aa:docs/academico/f36-sbx/preparacion-gate/F36SBX_Especificacion_Sucesor_B01.md` (en adelante, «la especificación de H») según Q2 §8, §10 y §12, adoptada por RR-001 (`5036393`).
>
> **No modifica** `validate_f36sbx.py`, sus pruebas, el estado del gate ni el gobierno. Implementarla exige D-02b, que **no está emitida**: sin facultades delegadas utilizables (RR-001 §4), D-02b solo puede emitirse por el mecanismo colegiado. Estado vigente: F36-SBX = EN DISEÑO, F36-SBX-GATE = NO SUPERADO, F37-SBX = BLOQUEADA.
>
> Validador de referencia: `validate_f36sbx.py` con SHA-256 `87ad2f6fed43dd5ae4f0c4baf8721de0a2be71e0efacdb27c8d1f514ea3563ec`, idéntico en `4a2b2d7`, `9dd76c4`, `5036393` y `2f6d0e0`. Las referencias `:NNNN` son de ese archivo.

## 0. Qué cambia frente a la especificación de H

| # | Cambio | Motivo |
|---|---|---|
| S-1 | Precondición: **D-10 determinada** antes de D-02b (§2) | Si F36-SBX quedó revocada (D10-2), este gate ya no puede superarse y B-01 no tiene objeto. Si D-10 sigue abierta, no se sabe si la puerta que B-01 habilita está vigente |
| S-2 | Nueva decisión **T-09**: base, anclaje y la regla FRZ después de SEG (§5.9) | Un H que descienda de `develop` contiene los 5 archivos de `app/` y las 6 pruebas de SEG. FRZ falla frente a `b8892af`, FG-01 y FG-05 se recalculan NO CUMPLE, y el gate nunca llegaría a SUPERADO con evidencia válida. La especificación de H no lo trataba, porque es anterior a SEG |
| S-3 | **T-05 cerrado:** formato del evento de revocación y estado REVOCADO en los espejos (§5.8) | D10-2 necesita poder registrarse. El v3 no puede representar REVOCADO (`allowed_states()`, `:1290`) |
| S-4 | **T-08 según Q2:** dos variantes del registro de los criterios EQUIPO (§6) | Q2 §8 y §12. La variante unipersonal de Q (`061ba68`) queda sustituida, no se implementa |
| S-5 | **Orden de los registros** de Q2 §8 (§7) | Corrige el D-02c histórico de `1d5d6aa` (UNI-M04, UNI-M05 y UNI-L02), que hacía depender FG-03 de un gate ya superado |
| S-6 | Se conserva FG-12 en NO APLICA cuando el gate lo admite | Sin cambios de regla; se explicita para que ninguna variante lo pierda |

Lo que no cambia de la especificación de H se mantiene en su redacción. Esto incluye el comportamiento verificado (§2 de H), las superficies protegidas (§3 de H), las invariantes I-1 a I-10 (§4 de H), los espejos E1–E7 y su requisito previo (§5.2 de H), el vocabulario cerrado (§5.3), `REQUIRED_STATE(R)` (§5.4), las excepciones X1–X5 (§5.5), la identidad de H (§5.6), la sustitución de `:2877` (§5.7) y los riesgos (§8 de H). Aquí se resumen solo para que S se audite sin abrir otro commit.

## 1. Propósito y límites

Con el validador vigente, el gate **no puede** pasar a SUPERADO aunque toda la evidencia sea auténtica: `rule_gate()` exige NO SUPERADO (`:2877`), `allowed_states()` solo admite ese resultado (`:1290`) y el vínculo invalida cualquier cambio posterior al candidato fuera de la evidencia y de la columna Estado (`binding_errors()`, `:2293`, y `doc_status_only()`, `:2275`).

B-01 hace que el validador reconozca SUPERADO o REVOCADO **solo** cuando el contrato lo produce, recalculándolo desde la evidencia, y que todas las fuentes que declaran el estado lo reflejen igual.

B-01 **no** registra evidencia, no decide EI ni dependencias, no aprueba ADR, no implementa capacidades de F37-SBX, no cambia el contrato de evidencia v4 y no toca la G0 real, ADR-005, los datos reales, el alcance C, RF-23 ni RF-29.

## 2. Precondiciones de D-02b

| ID | Precondición | Estado al 07/11/2026 |
|---|---|---|
| P-S1 | D-10 determinada (D10-1, o D10-3 con una autorización nueva hacia adelante que cubra B-01). Con D10-2, B-01 no procede: haría falta un gate nuevo | Pendiente. Borrador en `decisiones-d10-d11/` |
| P-S2 | S auditada sobre un commit fijo, sin BLOCKER, HIGH ni MEDIUM que exija corrección | Pendiente. Esta versión es la candidata |
| P-S3 | T-01 a T-09 decididas, o delegadas expresamente a la implementación dentro de las opciones de S | No emitidas |
| P-S4 | Quién emite D-02b: con DF-02 y DF-03 vigentes que incluyan B01-1, un RD de Luis anclado a S, a su informe y a RR-001; sin ellas, el mecanismo colegiado | Sin facultades delegadas utilizables: mecanismo colegiado |

## 3. Resultado derivado y espejos (resumen de H §5.1–§5.7)

- **R** es `evaluate_gate()` (`:2722`) sobre el estado y la evidencia, forzado a NO SUPERADO ante cualquier falla previa de la regla GATE. Vale NO SUPERADO, SUPERADO o REVOCADO.
- **Espejos cerrados:**
  - E1, `declared_result`;
  - E2, una línea canónica del gate;
  - E3, dos viñetas del README del paquete;
  - E4–E7, dos viñetas en cada documento de gobierno.

  Fuera de ellos, solo se admiten los estados históricos.
- **Antes de H**, cada espejo debe tener una sola afirmación por sujeto. Hoy los cuatro documentos de gobierno repiten el estado en el párrafo de F36 (D-07).
- **`:2877` se sustituye** por «E1–E7 declaran exactamente R». Cualquier diferencia, en cualquier sentido, es una falla.
- **Después de H** solo cambian X1–X5, comprobadas línea a línea. X2 se compara campo a campo con el blob de H.

## 4. Invariantes que S añade

| ID | Invariante |
|---|---|
| I-11 | R = REVOCADO prevalece sobre cualquier otro resultado y no se deshace en el mismo gate. Para continuar, haría falta un gate nuevo con su autorización |
| I-12 | La base y el perímetro de FRZ no se mueven para «regularizar» hechos anteriores. Cualquier cambio de anclaje es prospectivo, explícito (T-09) y posterior a D-10 |
| I-13 | La variante del registro (3/3 o RD) se fija en el estado del gate de H y no cambia después de H |

## 5. Puntos nuevos o cerrados

### 5.8 Revocación (T-05, cerrado)

`revocation` pasa de «nulo o cualquier objeto» a un formato cerrado:

```json
{
  "revocation": {
    "date": "AAAA-MM-DD",
    "effective_from": "AAAA-MM-DDThh:mm:ss-05:00",
    "ground": "charter_7_1 | charter_7_2 | charter_7_3 | charter_7_4 | gate_5_tei21 | gate_5_retirada",
    "determination": "ruta versionada del documento de determinación",
    "evidence": ["rutas o SHA-256 de la evidencia citada"]
  }
}
```

Con `revocation` válido:

- R = REVOCADO;
- F37-SBX = BLOQUEADA en todos los espejos;
- `allowed_states()` admite REVOCADO **solo** en los espejos.

Con `revocation` mal formado, falla cerrado: NO SUPERADO y una falla. `effective_from` puede ser anterior a la fecha del registro, porque el registro es declarativo (D-10 §5.4). El validador no lo juzga; solo exige que la determinación citada exista y esté versionada.

### 5.9 Base, anclaje y FRZ después de SEG (T-09, nuevo)

**Hecho.** SEG-01 a SEG-04 cambiaron 5 archivos de `app/` y 6 de `tests/` en `develop` (`2e53786`, `2546297` y `9dd76c4`). Un H que descienda de `develop` hereda esos cambios frente a `b8892af`, y FRZ falla en dos comprobaciones: 18 rutas externas y 11 entradas de runtime. Hoy la rama de este expediente da 55/4 por esa razón y por el anclaje de rama.

| Opción | Qué es | Consecuencia |
|---|---|---|
| **T-09 (a)** | Fijar H en una rama cortada desde `main` `55f758e`, cuyo árbol es exactamente el de AF5, y validar anclado en ella | FRZ pasa sin mover la base. Es coherente con la regla «Anclaje» del README del paquete (`06e933e`, 26/10/2026). Integrar H después en `develop` hará fallar FRZ allí por diseño, como hoy. Requiere T-04 para la rama |
| **T-09 (b)** | Mover `BASE` a un commit posterior a SEG | Cambia el significado de FG-05 hacia adelante. Solo es admisible con D10-1 determinada y como decisión expresa. No regulariza nada anterior (I-12) |
| T-09 (c) | Excluir de FRZ el mantenimiento auditado fuera del paquete | **Desaconsejada:** debilita TEI-22 y convierte una cuestión de D-10 en una excepción de código |

**Recomendación técnica, no vinculante:** (a).

## 6. Criterios EQUIPO: dos variantes (T-08 según Q2)

| | Variante 3/3 (vigente) | Variante RD (Q2 con delegación) |
|---|---|---|
| Cuándo | Siempre disponible | Solo con RR-001 vigente y DF-02 y DF-03 vigentes que incluyan GATE-1 (FG-03) o GATE-2 (FG-10). Hoy **no disponible** |
| Formato | `gate_version = 3`, esquema `f36sbx-team-evidence/v2`, `approvals` de las tres identidades exactas (`MEMBERS`, `:81`) | `gate_version = 4`, esquema v3: un `decision_record` en lugar de `approvals`, que cita el RD, RR-001, DF-02 y DF-03 con sus fechas, y una FG-02 favorable sobre H. El RD es posterior a las tres |
| FG-02 | Igual en las dos: informe canónico del auditor elegible sobre H, sin quórum propio |
| FG-03 | 3/3 `APRUEBA`, `AUTORIZA_INICIO_F37_SBX`, lista cerrada de EI idéntica a `f37_authorized_ei` y F36-M01 confirmada | RD bajo GATE-1, con las mismas condiciones de contenido. EI-09 solo con F36-M02 confirmada por actos auténticos. GATE-3 no existe |
| FG-10 | 3/3 siempre, nunca NO APLICA | RD bajo GATE-2, solo para declarar que no hay dependencias nuevas. Con dependencias, 3/3 |
| FG-12 | **NO APLICA** si FG-03 no autoriza ninguna EI CONDITIONAL, sin archivo ni votos. Si no, 3/3 con la decisión sobre EI-09 y, con alcance C, un ADR sucesor APROBADO dentro de H | Igual. El ADR y el alcance C no son delegables |

`approval_errors()` (`:2367`) se conserva para la variante 3/3. La variante RD añade `decision_record_errors()`, con su propio RED/GREEN. Ninguna variante relaja la otra (I-13).

## 7. Orden de los registros (Q2 §8)

1. Auditoría de S.
2. D-10 determinada (P-S1).
3. D-02b, por el mecanismo que corresponda (P-S4).
4. Implementación: RED, validador, documentos normativos previos a H (D-07), batería y metapruebas del plan de `1d5d6aa`, más los casos de §8.
5. H fijado, según T-09.
6. FG-02 favorable sobre H.
7. FG-03, FG-10 y FG-12, referidos a H.
8. Registro permitido por el sucesor.
9. Validación anclada.
10. Inicio de F37-SBX, solo si R = SUPERADO.

FG-03 es una entrada del gate: no puede exigir un gate ya superado.

## 8. Casos de prueba que S añade al plan de `1d5d6aa`

| ID | Caso | Esperado |
|---|---|---|
| S-T01 | `revocation` con el formato de §5.8 y la determinación versionada | R = REVOCADO; espejos en REVOCADO y BLOQUEADA; 0 fallas |
| S-T02 | `revocation` sin `determination`, con `ground` desconocido o con un tipo distinto | NO SUPERADO y una falla |
| S-T03 | `revocation` válido y espejos en NO SUPERADO | Falla (I-2) |
| S-T04 | H descendiente de `develop` con SEG, base `b8892af` | FRZ falla; R = NO SUPERADO aun con evidencia válida |
| S-T05 | H en una rama desde `55f758e`, admitida por T-04, con evidencia válida y sintética en un clon | R = SUPERADO; 0 fallas |
| S-T06 | Variante RD con una DF cuya fecha es posterior al RD | Falla |
| S-T07 | Variante RD con FG-10 y dependencias declaradas | Falla: exige 3/3 |
| S-T08 | Variante fijada en H como 3/3 y evidencia con `decision_record` | Falla (I-13) |
| S-T09 | FG-12 en NO APLICA con FG-03 sin EI CONDITIONAL y sin `FG-12.json` | Admitido |
| S-T10 | FG-12 en NO APLICA con una EI CONDITIONAL autorizada | NO SUPERADO |

Los controles positivos (S-T01 y S-T05) solo se crean en memoria o en clones desechables, nunca sobre H (H §8).

## 9. Decisiones de diseño

| ID | Decisión | Recomendación técnica, no vinculante | Estado |
|---|---|---|---|
| T-01 | Lista de espejos E1–E7 y reescritura previa | Aceptar la de H §5.2 | NO EMITIDA |
| T-02 | Estado de F37-SBX con R = SUPERADO | Un único estado de habilitación, por ejemplo «AUTORIZADA PARA INICIAR», sin enumerar EI en el gobierno | NO EMITIDA |
| T-03 | ¿Cambia el estado de F36-SBX en la transición? | No; su cierre sería un incremento propio | NO EMITIDA |
| T-04 | Rama de H y de los registros | Admitir de forma explícita una sola rama de H, con su prueba (ligada a T-09 (a)) | NO EMITIDA |
| T-05 | Formato de la revocación | §5.8 | **Cerrado en S**, pendiente de auditoría |
| T-06 | Refuerzo de independencia de `integrante_no_autor` | Opcional | NO EMITIDA |
| T-07 | Versión del gate y del esquema | `gate_version = 3` y esquema v2 si se elige solo la variante 3/3; 4 y v3 si se implementa también la variante RD | NO EMITIDA |
| T-08 | Variante de registro | Implementar la 3/3 ahora y dejar la RD especificada. Con las DF actuales, la RD no se puede usar | NO EMITIDA |
| T-09 | Base, anclaje y FRZ después de SEG | (a), una rama de H desde `55f758e` | NO EMITIDA |
