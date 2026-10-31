# BORRADOR — SIN EMISIÓN — SIN ADOPCIÓN

## DF-02 — Delegación opcional de Fredy Coronacion en Luis Vila Meza

> **BORRADOR — SIN EMISIÓN — SIN ADOPCIÓN.** Opcional. Solo Fredy Coronacion (Coronacion Meza Fredy) puede emitirla, con su propio acto. Es independiente de su conformidad (CM-02): puede estar conforme y no delegar nada. Ninguna casilla está marcada y este borrador no concede ninguna facultad.

## 1. Cómo funciona

Según [Q2 §7 y §9.4 a §9.6](../reconciliacion-gobierno/PROPUESTA_Q2_Gobierno_Equipo.md#9-adopción-versión-conformidad-delegación-y-entrada-en-vigor):

- **Solo tiene efecto si Q2 se adopta.** Una facultad delegada existe desde la fecha del registro raíz (RR), o desde la fecha posterior que indique la delegación, nunca antes. Sin RR y delegaciones vigentes, no existe.
- **Solo pasa a Luis la intersección.** Una facultad pasa a Luis solo si la delegan los dos, Fredy (DF-02) y Anthony (DF-03), en delegaciones vigentes. Para cada facultad común rigen los límites de las dos, y solo durante el periodo en que ambas están vigentes.
- **Lo que no deleguen los dos sigue como hoy:** en el mecanismo colegiado del contrato 10 o, para los criterios de equipo del gate, en el 3/3.
- **Se revoca hacia adelante**, cuando quieras, con otro acto tuyo. Lo que Luis haya hecho antes con una facultad vigente conserva su validez.
- **Cada uso deja constancia.** Luis registra cada decisión que tome con una facultad delegada en un RD con fecha real, que cita el RR y las delegaciones vigentes en esa fecha.
- **Puede ser total, parcial o nula.** No emitir DF-02 o decir «no delego ninguna facultad» tiene el mismo efecto: no se delega nada.

## 2. Facultades que se pueden elegir

Marca solo las que delegues. La lista es cerrada: nada que no esté en ella se delega. Al responder, copia el texto completo de cada facultad que delegues, y no solo su identificador, para que tu delegación se entienda sin este borrador.

### 2.1 Operaciones Git (contrato 10; nivel N3 de Q2)

Hoy, el contrato 10 de [`CLAUDE.md`](../../../../CLAUDE.md) exige una autorización explícita del equipo para `push`, `merge`, release o tag. Con Q2 adoptada, Luis podría decidir estas operaciones en representación del equipo solo dentro de las delegaciones vigentes de los dos (Q2 §4 y §10).

| Marca | ID | Facultad | Alcance |
|---|---|---|---|
| ☐ | GIT-1 | Publicar ramas de trabajo | `push` de ramas `feature/*`, `fix/*`, `docs/*` y `chore/*`, sin integrarlas en `develop` ni en `main` |
| ☐ | GIT-2 | Integrar en `develop` | `merge` en `develop` y `push` de `develop` |
| ☐ | GIT-3 | Integrar en `main` | `merge` en `main` y `push` de `main` |
| ☐ | GIT-4 | Crear y publicar etiquetas | Solo etiquetas nuevas. Nunca mover, borrar ni reutilizar una existente |
| ☐ | GIT-5 | Crear y publicar releases | Solo releases nuevas. Sin modificar ni borrar las existentes |

Borrar ramas o etiquetas remotas no está en la lista y sigue necesitando al equipo. El force push y la reescritura de historia publicada no se hacen nunca (§3.1).

### 2.2 B-01, el sucesor del gate (Q2 §8 y §10)

| Marca | ID | Facultad | Alcance |
|---|---|---|---|
| ☐ | B01-1 | Emitir D-02b: autorizar la implementación del sucesor B-01 | Mediante un RD anclado al commit de la especificación S del sucesor ya auditada, a su informe de auditoría y al RR. La implementación se limita a lo que S describe, con las opciones de diseño T-01 a T-07 elegidas entre las que S plantea |

- **S todavía no existe.** La especificación de `1d5d6aa` no está auditada, y Q2 §12 prevé completarla (la variante de Q2 y T-08) antes de auditarla. Sin una S auditada, B01-1 no se puede usar.
- **B01-1 no incluye:** iniciar F37-SBX, que es FG-03; registrar evidencia de FG-02, FG-03, FG-10 o FG-12; aprobar un ADR; integrar o publicar, que son GIT-2 a GIT-5; ni declarar superado el gate, que exige además H, una FG-02 favorable sobre H y el resto de los requisitos del gate.

### 2.3 Criterios de equipo del gate (Q2 §8)

> **Solo con un contrato sucesor.** Con el [gate vigente](../F36SBX_Gate_Sucesor.md) (`gate_version` 3), FG-03, FG-10 y FG-12 exigen los votos reales de los tres integrantes, con sus identidades exactas, y una delegación no los sustituye. Estas facultades solo podrían usarse si un contrato sucesor (`gate_version` 4 y esquema v3), implementado mediante D-02b dentro de H y auditado, sustituye los votos 3/3 por un RD de Luis que cite el RR, las delegaciones y una FG-02 favorable sobre H. Adoptar Q2 no crea ese contrato.

| Marca | ID | Facultad | Alcance |
|---|---|---|---|
| ☐ | GATE-1 | FG-03: decidir y registrar la autorización de inicio de F37-SBX-A | Con una FG-02 favorable sobre H. Una lista cerrada de EI de alcance B en ALLOWED (EI-01 a EI-07) y la confirmación de la numeración (F36-M01). EI-09, solo si existe una decisión válida sobre ella: GATE-3 o los actos de los tres |
| ☐ | GATE-2 | FG-10: aprobar el registro de dependencias que declara que no hay ninguna nueva | Solo esa declaración. No aprueba ninguna dependencia: solo las justificarían EI-10, EI-11 o EI-12, del alcance C |
| ☐ | GATE-3 | FG-12, solo la decisión sobre EI-09 (F36-M02): si la recuperación léxica de fragmentos cabe en el alcance B | Sin ADR sucesor. Delegarla permite a Luis decidir por sí solo esta frontera entre los alcances B y C. Si EI-09 no cabe en B, pasa a necesitar un ADR y queda fuera de la delegación |

### 2.4 Lo que no se puede delegar

Nada de esto está en la lista, y escribirlo en una delegación no tendría efecto:

- **aprobar un ADR sucesor** o cualquier excepción a ADR-005 (F36-M03) (Q2 §4);
- **cualquier decisión del alcance C**, incluidas EI-08, EI-10, EI-11, EI-12 y EI-24 (Q2 §4 y §8);
- **FG-02, la auditoría independiente:** la hace una sesión de revisión separada, y nadie se audita a sí mismo (Q2 §3 y §5);
- **lo externo (N5):** G0-02, G0-03 y G0-12, las aprobaciones jurídicas, de privacidad o institucionales, los datos reales, producción y el alcance C del producto (Q2 §4 y §6);
- **lo que el gate no puede autorizar:** producción, datos reales, PII real, audio o vídeo reales, decisión o selección automática, scoring, ranking o recomendación de personas, cambios en RF-21, RF-23 o RF-29, la G0 real, nuevos endpoints, migraciones o UI, y las EI BLOCKED, de EI-13 a EI-23 (gate §6);
- **los actos personales:** tu conformidad, tus delegaciones y cualquier acto en nombre de otra persona (Q2 §7);
- **las excepciones** a los contratos 1 a 10 o a las prohibiciones del charter (Q2 §7).

Otras decisiones académicas del nivel N4, como las declaraciones ante el curso o presentar un entregable como trabajo del equipo, se podrían delegar con un alcance definido (Q2 §4). Este borrador no las incluye: delegarlas exigiría un texto propio.

## 3. Límites

### 3.1 Límites que siempre rigen

La delegación no puede quitarlos:

- los contratos 1 a 10 de `CLAUDE.md`, sin excepciones;
- para publicar, la CI `tests` en verde; nunca force push ni reescritura de historia publicada; y la etiqueta `v1.0.0-academic` no se mueve, no se borra y no se reutiliza ([reconciliación §5.3](../reconciliacion-gobierno/F36SBX_Reconciliacion_Estado_Gobierno.md); contrato 9);
- un RD por cada uso, con fecha real, que cite el RR y las delegaciones vigentes (Q2 §7);
- nada de lo que enumera §2.4.

### 3.2 Límites adicionales, opcionales

| Marca | Límite |
|---|---|
| ☐ | Solo sobre las ramas, carpetas o fases que indico: PENDIENTE |
| ☐ | Solo después de una revisión técnica diferenciada favorable del commit exacto |
| ☐ | Avisarme antes de cada operación |
| ☐ | Otros: PENDIENTE |

### 3.3 Inicio, fin y revocación

| Campo | Opciones |
|---|---|
| Inicio | ☐ Desde la fecha del RR · ☐ Desde una fecha posterior: PENDIENTE |
| Fin | ☐ Hasta una fecha: PENDIENTE · ☐ Sin fecha de fin, hasta que la revoque |
| Revocación | Siempre posible, hacia adelante, con otro acto mío por mi propio canal |

## 4. Emisión

| Campo | Valor |
|---|---|
| Registro | DF-02 |
| Quién delega | Fredy Coronacion (Coronacion Meza Fredy) |
| En quién | Luis Vila Meza, responsable técnico |
| Versión de Q2 | Commit `8b1f068b5ac2039139ab5756096c147c11c9fcb2`, árbol `b5b81718680762f9585e4dae969ca44e69114865` |
| Facultades delegadas | PENDIENTE: las elegidas en §2, o «ninguna» |
| Límites adicionales | PENDIENTE |
| Inicio y fin | PENDIENTE |
| Fecha | PENDIENTE |
| Canal | PENDIENTE |
| Evidencia y su SHA-256 | PENDIENTE |

## 5. Texto que puedes copiar y completar

> Yo, Fredy Coronacion (Coronacion Meza Fredy), delego en Luis Vila Meza, responsable técnico, solo si Q2 en la versión del commit 8b1f068b5ac2039139ab5756096c147c11c9fcb2 y el árbol b5b81718680762f9585e4dae969ca44e69114865 se registra como adoptada, estas facultades: [copia aquí el ID y el texto completo de cada facultad elegida]. Límites adicionales: [ninguno | …]. Desde: [la fecha del registro | fecha]. Hasta: [fecha | que la revoque]. Puedo revocarla hacia adelante. Fecha: [día/mes/año].

O bien:

> Yo, Fredy Coronacion (Coronacion Meza Fredy), no delego ninguna facultad.
