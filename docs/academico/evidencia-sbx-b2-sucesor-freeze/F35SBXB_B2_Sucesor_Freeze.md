# F35-SBX-B — B2-SUCCESSOR-FREEZE: cierre de la capa sucesora (AF-L02)

> **Estado: B2-SUCCESSOR-FREEZE EN CONSTRUCCIÓN: diseño y pruebas en RED, sin validador.** Fecha: 14/10/2026. Rama `feature/f35-sbx-b2-ephemeral-store`.
>
> - **Reauditoría independiente de AF-M01:** «AF-M01 REAUDITADO Y RESUELTO — REQUIERE SUCCESSOR-FREEZE ANTES DE INTEGRACIÓN» (decisión B). No hay hallazgos nuevos BLOCKER, HIGH ni MEDIUM. Queda AF-L02 (LOW).
> - **B2 = IMPLEMENTADA / CORREGIDA / REAUDITADA / APROBADA PARA FREEZE.**
>
> Este documento registra la interpretación y el diseño antes de implementar el cierre. Los resultados se añaden en el commit que lo completa.

## 1. AF-L02 y condición de resolución

AF-L02: la capa sucesora (gate vigente sobre HEAD) no tiene un ancla independiente que preserve sus bytes y su historia. Sus archivos se comparan con HEAD, pero nada posterior preserva la identidad auditada de `9d6fb157bb818574217e3675da1849e8d1010962`.

Condición fijada por el auditor: un cierre o ancla externa verificable que cumpla seis requisitos:

1. preserve la capa sucesora auditada;
2. preserve su historia;
3. conserve MAT;
4. no debilite B2;
5. no debilite B2-FREEZE;
6. permita merges `--no-ff` legítimos.

No basta otra capa que solo compruebe integridad y vuelva a omitir MAT.

## 2. Interpretación

- **Lo que se preserva.** Los tres archivos que añadió la corrección de AF-M01, con los bytes, modos, tipos e historia que tenían en `9d6fb15`. También su semántica: la evaluación material vigente sobre HEAD.
- **Cómo se conserva MAT.** Ejecutando el gate sucesor aprobado, verificado byte a byte contra `9d6fb15`. No se copia ni se reimplementa MAT, ni se alteran sus constantes. Sobre un HEAD con este cierre, el gate sucesor no puede dar 7/0, porque su alcance fijo no incluye las rutas del cierre: es la misma falla de clase A de B0 y DH-B13. Esa falla no se oculta. Se clasifica con exactitud y se exige que el resto de la evaluación pase.
- **Por qué no hay una cadena infinita de freezes.** Este cierre es la última capa de B2. Registra el commit del sucesor, que ya existe, y protege a la vez esa capa y la suya propia. Su ancla es el commit que lo completa, que el validador deriva de Git y no guarda en ningún archivo. Ese hash lo fija desde fuera el informe de la auditoría independiente, y después un incremento sucesor autorizado, igual que el sucesor registró `9961d2d`. Ningún validador adicional protege este cierre: lo protege el hash registrado fuera, más su propia comprobación de inmutabilidad desde ese commit.

## 3. Diseño

### 3.1 Archivos

Rutas nuevas, con el patrón `<capa>_freeze` de las capas anteriores:

| Ruta | Contenido |
|---|---|
| `docs/academico/tools/f35sbxb2_sucesor_freeze/validate_f35sbxb2_sucesor_freeze.py` | Validador del cierre |
| `docs/academico/tools/f35sbxb2_sucesor_freeze/b2_sucesor_freeze_manifest.json` | Manifiesto determinista, derivado de objetos Git verificados |
| `docs/academico/tools/f35sbxb2_sucesor_freeze/test_f35sbxb2_sucesor_freeze.py` | Batería SF01..SF26 |
| `docs/academico/evidencia-sbx-b2-sucesor-freeze/F35SBXB_B2_Sucesor_Freeze.md` | Este documento |

No se modifica ningún archivo existente.

### 3.2 Conjunto protegido

El conjunto se deriva de Git: es el delta entre el freeze y el sucesor (`git diff-tree -r --no-renames 9961d2d 9d6fb15`), tres rutas, todas añadidas. El validador lo contrasta con el contrato del sucesor: las carpetas de su capa (`SUCESOR_DIRS`), leídas por AST del blob del gate sucesor en `9d6fb15`, sin ejecutarlo.

| Ruta | Justificación |
|---|---|
| `docs/academico/tools/f35sbxb2_sucesor/validate_f35sbxb2_sucesor.py` | El gate auditado que compone HIS, CON, MAT y ALC; el cierre lo ejecuta desde estos bytes |
| `docs/academico/tools/f35sbxb2_sucesor/test_f35sbxb2_sucesor.py` | La batería AF01..AF14 que acredita su comportamiento; se ejecuta anclada en `9d6fb15` |
| `docs/academico/evidencia-sbx-b2-sucesor/F35SBXB_B2_Sucesor.md` | La interpretación, el diseño y la evidencia auditados |

Superficies reservadas: las dos carpetas que creó el sucesor, `docs/academico/tools/f35sbxb2_sucesor/` y `docs/academico/evidencia-sbx-b2-sucesor/`. Deben tener exactamente esas tres rutas.

No hacen falta rutas adicionales, porque el resto de la semántica ya está protegido por las capas que el cierre compone:

- el almacén, el gate de B2, sus documentos y el gobierno, por el nivel A del freeze;
- la capa del freeze, por el nivel B del freeze y por CON del sucesor, con su ancla registrada;
- el dataset, el runtime, A, B0 y SBX, por la evaluación material del gate de B2 dentro de MAT.

Congelar más rutas sería congelar el repositorio arbitrariamente.

### 3.3 Reglas del validador

| ID | Comprueba |
|---|---|
| ENT | Intérprete aislado y sin `PYTHONPATH`, `PYTHONHOME` ni `PYTHONUSERBASE`. Ninguna variable de Git que redirija el repositorio, el índice, los objetos o las referencias (`GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, `GIT_OBJECT_DIRECTORY`, etc.): con ellas falla cerrado. Git sobre el repositorio del validador, con historia completa y sin injertos ni objetos de reemplazo |
| ANC | Anclas registradas: el candidato `2472fd6`, el freeze `9961d2d` y el sucesor `9d6fb15` son commits íntegros (objetos verificados) y forman una cadena: candidato → freeze → sucesor → HEAD. El conjunto protegido derivado de Git coincide con el contrato del sucesor, y sus superficies son carpetas nuevas en el sucesor |
| MAN | El manifiesto es, byte a byte, la serialización canónica de lo que se deriva de los objetos del sucesor y del freeze |
| HIS | En cada commit posterior al sucesor que lleva a HEAD, merges incluidos, el conjunto protegido y las superficies reservadas son idénticos al sucesor |
| ARB | Árbol de HEAD idéntico al sucesor en el conjunto y las superficies |
| IDX | Índice en etapa 0 con el modo y el blob del sucesor, sin entradas extra en las superficies |
| FLG | Ningún flag en el índice del repositorio (assume-unchanged, skip-worktree o conflictos) |
| DSK | Disco: archivos regulares sin enlaces con los bytes del sucesor; superficies exactas, incluidos ignorados, ocultos y `__pycache__` |
| VIG | Evaluación material vigente: el gate sucesor, verificado contra su blob en `9d6fb15`, se ejecuta sobre HEAD sin variables `GIT_*`. Su resultado tiene que ser exactamente la evolución de alcance de clase A de este cierre (§3.4) |
| ALC | Alcance exacto del cierre: frente al sucesor, HEAD, el índice y el árbol de trabajo solo añaden las cuatro rutas del cierre, y no hay archivos sin seguimiento |
| FRZ | Nivel B del cierre: un único commit posterior al sucesor completa la capa del cierre y HEAD desciende de él. Desde él, cada commit, HEAD, el índice y el disco tienen exactamente sus archivos |
| DEP | Los archivos Python del cierre solo importan la biblioteca estándar autorizada y no ejecutan código dinámico |

### 3.4 VIG: la evaluación material, sin ocultar SCP

Sobre un HEAD válido con este cierre, el gate sucesor da 5/2, y VIG solo lo acepta si se cumple todo lo siguiente:

- **ENT, ANC, HIS, CON y DEP del sucesor pasan.** HIS informa el gate de B2 anclado en código 0 y sin fallas, con la transición `12c1c36`. CON informa el freeze en código 0 y sin fallas, con el freeze derivado `9961d2d`.
- **MAT tiene una sola violación**: SCP con 3 × (7 + 4) = 33 violaciones frente a las 21 de su alcance. Su línea INFO dice «reglas en falla: SCP; casos en falla: 0». Es decir, el gate de B2 ejecutado sobre HEAD solo incumple SCP, y solo por las rutas enumeradas.
- **ALC tiene exactamente tres violaciones**, una por plano (HEAD, árbol de trabajo e índice), y cada una nombra únicamente rutas del cierre en estado `A`.

Cualquier otra falla del gate sucesor hace fallar VIG, y la línea INFO de VIG repite las reglas del gate de B2 en falla. Por ejemplo: una regla material de B2 (SBX, FSY, PRE, STA…), otra violación de ALC, un CON o HIS que no pasan, o un recuento distinto.

### 3.5 Raíz de confianza y acreditación externa

- **Nivel A (el sucesor):** el hash del sucesor (`9d6fb15`), que ya existe, está registrado en el validador. Cada objeto se lee y se verifica recalculando su identificador con el formato de objetos de Git, y el manifiesto no puede acreditar nada por sí mismo.
- **Nivel B (el cierre):** su ancla es el commit que completa la capa, que el validador deriva e imprime en la línea INFO de FRZ. Ningún archivo guarda ese hash.

Para acreditar el cierre, el auditor:

1. anota ese commit;
2. comprueba que los blobs de la capa en HEAD coinciden con los de ese commit;
3. ejecuta el validador con los bytes de ese commit;
4. exige que el ancla derivada coincida con la anotada.

Un cierre reconstruido con los mismos bytes en otra historia pasa el validador, pero informa otra ancla (SF26). Por eso el PASS aislado no autentica la capa sin el hash registrado fuera.

### 3.6 Lo que no cambia

- **Gates congelados.** El gate de B2, el validador del freeze y el gate sucesor conservan sus bytes y no se ejecutan con constantes alteradas.
- **Resultados anclados.** Siguen siendo evidencia histórica: el gate de B2 sobre `2472fd6` (119/0), el freeze sobre `9961d2d` (10/0) y el sucesor sobre `9d6fb15` (7/0, con su batería en 14/14).
- **Gobierno.** `CLAUDE.md` y `docs/PROGRESS.md` no cambian. El contrato de B2 (§2.3) solo admite la transición `12c1c36`, y el freeze congela esos archivos en su nivel A, así que cambiarlos ahora rompería la cadena. Actualización de gobierno pendiente de incremento sucesor autorizado.

## 4. Pruebas

Cada caso trabaja en un clon desechable de HEAD, fuera del repositorio, y ejecuta el validador del cierre con `python -I`. Pasa si fallan exactamente las reglas esperadas. En los casos materiales, además, la línea INFO de VIG tiene que nombrar las reglas del gate de B2 que detectan el incumplimiento.

| Caso | Escenario | Reglas en falla esperadas |
|---|---|---|
| SF01 | Estado válido; el ancla derivada es el commit que completa el cierre | Ninguna (PASS) |
| SF02 | Gate sucesor modificado y confirmado | HIS, ARB, IDX, DSK, VIG y ALC; el gate alterado no se ejecuta |
| SF03 | Batería del sucesor modificada y confirmada | HIS, ARB, IDX, DSK y ALC |
| SF04 | Documento del sucesor modificado y confirmado | HIS, ARB, IDX, DSK y ALC |
| SF05 | Modificar → restaurar un artefacto del sucesor | HIS |
| SF06 | Renombrar, eliminar, cambiar el modo o el tipo, y restaurar | HIS en las cuatro sondas |
| SF07 | Manifiesto del cierre alterado y confirmado | MAN y FRZ |
| SF08 | Validador del cierre alterado y confirmado: copia de confianza; copia alterada | FRZ; FRZ y DEP |
| SF09 | Rama lateral que altera y restaura el sucesor, integrada con merge `--no-ff` | HIS |
| SF10 | Merge `--no-ff` en `develop` (`72e86c5`) | Ninguna (PASS) |
| SF11 | Commit posterior sin cambios de contenido (como un registro) | Ninguna (PASS) |
| SF12 | Merge `--no-ff` de `develop` en `main` (`3fdfdce`) | Ninguna (PASS) |
| SF13 | Clon superficial | Fallo cerrado en todo salvo FLG y DEP |
| SF14 | (a) Sucesor sustituido con `git replace` para ocultar una alteración; (b) injertos | (a) ENT, HIS, ARB, IDX, DSK, VIG y ALC; (b) ENT y VIG |
| SF15 | `GIT_DIR`, `GIT_WORK_TREE` y `GIT_INDEX_FILE` presentes, sobre un estado válido | ENT |
| SF16 | assume-unchanged y skip-worktree con un cambio que `git status` no ve | FLG, DSK y VIG |
| SF17 | Índice distinto con el disco correcto | IDX, ALC y VIG |
| SF18 | En una superficie reservada: (a) archivo ignorado; (b) enlace simbólico nuevo; (c) gitlink en el índice | (a) DSK y VIG; (b) DSK, ALC y VIG; (c) IDX, ALC y VIG |
| SF19 | Sucesor reconstruido con los mismos bytes en otra historia | ANC, HIS y FRZ |
| SF20 | Gate sucesor debilitado (sin MAT) en el disco | DSK, VIG y ALC; el gate debilitado no se ejecuta |
| SF21 | LF añadido a `evidence.csv` | VIG y ALC; VIG nombra SBX, FSY y PRE |
| SF22 | SHA-256 de `evidence.csv` alterado en el manifiesto F34 | VIG y ALC; VIG nombra SBX, FSY y STA |
| SF23 | CSV y manifiesto F34 alterados de forma coherente | VIG y ALC; VIG nombra SBX, FSY y STA |
| SF24 | Artefacto ignorado en `public/build/` | Solo VIG; nombra FSY |
| SF25 | Archivo del sucesor y manifiesto del cierre alterados de forma coherente | MAN, HIS, ARB, IDX, DSK, ALC y FRZ |
| SF26 | Cierre reconstruido con los mismos bytes en otra historia | Ninguna (PASS), con un ancla derivada distinta del commit que completa el cierre |

SF24 a SF26 se suman a los casos mínimos pedidos, porque cubren propiedades distintas:

- **SF24:** lo que solo la evaluación material detecta.
- **SF25:** que el manifiesto del cierre no puede acreditar una alteración coherente.
- **SF26:** el límite que obliga a registrar fuera el ancla del cierre.

## 5. Resultados

Pendientes: se registrarán en el commit que completa el cierre.
