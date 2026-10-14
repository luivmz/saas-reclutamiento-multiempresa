# F35-SBX-B — B2-SUCCESSOR-FREEZE: cierre de la capa sucesora (AF-L02)

> **Estado: B2-SUCCESSOR-FREEZE = IMPLEMENTADO / CANDIDATO A AUDITORÍA INDEPENDIENTE.** Fecha: 14/10/2026. Rama `feature/f35-sbx-b2-ephemeral-store`.
>
> - **AF-L02 = CORREGIDO POR EL IMPLEMENTADOR / PENDIENTE DE REAUDITORÍA.**
> - **Reauditoría independiente de AF-M01:** «AF-M01 REAUDITADO Y RESUELTO — REQUIERE SUCCESSOR-FREEZE ANTES DE INTEGRACIÓN» (decisión B). No hay hallazgos nuevos BLOCKER, HIGH ni MEDIUM. Queda AF-L02 (LOW), que corrige este cierre.
> - **B2 = IMPLEMENTADA / CORREGIDA / REAUDITADA / APROBADA PARA FREEZE.**
>
> Las secciones 1 a 4 registran la interpretación y el diseño, escritos antes de implementar el cierre (commit RED `1e5677e8aee73f3267dcd81a0273bdeddd832b8b`). La sección 5 añade los resultados. Este commit completa el cierre: su hash es el ancla de nivel B (§3.5), no se guarda en ningún archivo y lo informa la línea INFO de FRZ.

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

### 5.1 RED y GREEN

| Commit | Contenido | Resultado |
|---|---|---|
| `1e5677e8aee73f3267dcd81a0273bdeddd832b8b` | Batería SF01..SF26 y este diseño (RED) | 0 casos correctos y 26 fallas, con 30 ejecuciones: el validador del cierre no existía. SF07, SF08 y SF25 ni siquiera podían prepararse, porque alteran archivos que aún faltaban |
| El que completa el cierre (este) | Validador, manifiesto y resultados (GREEN) | 26 casos correctos y 0 fallas, con 34 ejecuciones del validador |

El GREEN usa la batería del commit RED sin cambios. La primera ejecución de la batería completa contra el validador ya dio 26/0, con las reglas en falla de cada caso iguales a las esperadas.

### 5.2 Evaluación material

Resultado de VIG en los casos materiales, sobre el commit desechable del GREEN. La segunda columna resume la línea INFO de VIG, que repite el resultado del gate sucesor y las reglas del gate de B2 en falla:

| Caso | Gate sucesor y gate de B2 sobre ese HEAD | Reglas del cierre en falla |
|---|---|---|
| SF01 | Gate sucesor 5/2, solo ALC y MAT. Gate de B2: solo SCP, con 33 violaciones (las 21 del alcance del sucesor y 12 del cierre: cuatro rutas en tres planos) | Ninguna: PASS |
| SF21 (LF en `evidence.csv`) | Gate de B2: DAT, DYN, FSY, ISO, PRE, PUR, SBX y SCP (34) | VIG y ALC |
| SF22 (SHA-256 del manifiesto F34) | Gate de B2: DAT, DET, DYN, FSY, ISO, PUR, SBX, SCP (34) y STA | VIG y ALC |
| SF23 (CSV y manifiesto F34 coherentes) | Gate de B2: las mismas reglas que en SF22, con SCP en 35 | VIG y ALC |
| SF24 (artefacto ignorado en `public/build/`) | Gate de B2: FSY y SCP (33) | Solo VIG |
| SF20 (gate sucesor sin MAT en el disco) | No se ejecuta: no coincide con su blob `dcb8d7c` en el sucesor | DSK, VIG y ALC |
| SF02 (gate sucesor modificado y confirmado) | No se ejecuta, por la misma razón | HIS, ARB, IDX, DSK, VIG y ALC |

En el resto de los casos con VIG en falla, el gate sucesor detecta la alteración con sus propias reglas, y VIG lo rechaza porque su resultado ya no es el 5/2 de clase A:

- con injertos (SF14), el gate sucesor falla en ENT, CON, MAT y ALC;
- con assume-unchanged o skip-worktree (SF16), falla en CON, MAT y ALC, y el gate de B2 añade FLG;
- con el índice alterado o un objeto inesperado en una superficie del sucesor (SF17 y SF18), su ALC nombra rutas ajenas al cierre. Con el enlace simbólico, además, SCP sube a 34.

Con `git replace` (SF14), el gate sucesor no llega a ejecutarse: sus bytes en el disco no son los del blob auditado.

### 5.3 Controles de mutación

La batería se ejecutó contra cuatro validadores del cierre debilitados a propósito, en clones desechables:

| Mutación | Casos que la detectan |
|---|---|
| VIG ejecuta el gate sucesor que haya en el disco, sin verificarlo contra su blob en `9d6fb15` | SF02, donde el gate modificado se ejecuta y VIG deja de fallar; SF20, donde VIG ya no declara que el gate debilitado quedó sin ejecutar |
| Sin VIG: una capa que solo comprueba integridad y omite la evaluación material, lo que la condición de AF-L02 no admite | SF20 a SF23, que pierden VIG; SF24, que pasa a PASS |
| Sin HIS: no se inspecciona la historia posterior al sucesor | SF05, las cuatro sondas de SF06 y SF09, que pasan a PASS |
| El nivel B se autoacredita con HEAD en lugar del commit que completa el cierre | SF07, que solo falla en MAN; SF08, cuya copia alterada solo falla en DEP |

### 5.4 Validación en clon limpio

Los resultados se obtuvieron en clones limpios sin remoto, sobre un commit desechable cuyo árbol solo difiere del de este commit en el texto de esta sección 5, cuyos valores aún no estaban escritos. Con los valores ya escritos se repitieron sobre el árbol definitivo el validador del cierre, `validate.py` (con y sin `--cierre-f29`), `validate_f34e.py` y la comprobación de enlaces, MANIFEST y evidencias, con el mismo resultado. La repetición completa sobre el commit real se registra en el reporte de entrega.

| Comprobación | Resultado |
|---|---|
| `validate_f35sbxb2_sucesor_freeze.py` | 12/0, en unos 40 segundos. FRZ deriva como ancla el commit que completa el cierre |
| `test_f35sbxb2_sucesor_freeze.py` | 26/0, con 34 ejecuciones del validador, en unos 20 minutos |
| `validate_f35sbxb2_sucesor.py` anclado sobre `9d6fb15` | 7/0: el freeze derivado es `9961d2d`, el gate de B2 anclado da 119/0 con la transición `12c1c36`, y MAT da 118/1 con SCP en 21 |
| `test_f35sbxb2_sucesor.py` anclado sobre `9d6fb15` | 14/0, con 18 ejecuciones del gate sucesor |
| `validate_f35sbxb2_sucesor.py` sobre HEAD | 5/2: solo ALC, con las cuatro rutas del cierre en los tres planos, y MAT, con SCP en 33 frente a 21. Es la evolución de alcance de clase A que VIG exige (§3.4) |
| `validate_f35sbxb2_freeze.py` sobre HEAD y anclado sobre `9961d2d` | 10/0 en ambos, con el freeze derivado `9961d2d` |
| `test_f35sbxb2_freeze.py` | 27/0, con 33 ejecuciones del validador |
| Gate de B2 anclado sobre `2472fd6` | 119/0, con la transición derivada igual a la registrada (`12c1c36`) |
| Gate de B2 sobre HEAD | 118/1: solo SCP, con 33 violaciones. Son las once rutas posteriores al candidato (las siete del alcance del sucesor y las cuatro del cierre) en tres planos |
| Gate de B1 anclado sobre `8e94a60` y B1-FREEZE anclado sobre `3d9b783` | 159/0, con los 18 SBX en PASS, y 14/0, con SBX 18/18 |
| Gate de B1 y validador de B1-FREEZE sobre HEAD | 105/54 y 0/2. Fallan las mismas reglas que sobre el candidato y el sucesor (clase A desde la transición de gobierno): CTX, GOV, SCP y los 51 casos PB en B1, y FRZ y B1 en B1-FREEZE. Solo crecen los recuentos: SCP pasa de 24 a 45 y a 57, y FRZ de 12 a 17 y a 19. El resto de las líneas de falla es idéntico |
| `validate.py` y `validate.py --cierre-f29` | 0 fallas en ambos |
| `validate_f29.py`, `test_f32_safety.py`, `validate_f33.py`, `validate_f34.py` y `validate_f34a.py` | 225/0, OK (10 pruebas), 451/0, 403/0 y 108/0 |
| `validate_f34e.py` sobre `2472fd6`, `9961d2d`, `9d6fb15` y HEAD | 247/1 en los cuatro, con SBX 18/18 sobre HEAD. Es la falla histórica de la regla GIT. Su lista de rutas no autorizadas por DH-02 pasa de 12 a 16, a 19 y a 23, sin que desaparezca ninguna, y el resto del mensaje es idéntico |
| Enlaces relativos | 1120, 0 rotos |
| MANIFEST y evidencias | 61 hashes y 0 discrepancias; 0 discrepancias en las evidencias de las prácticas 03, 05, 08 y 11 |
| `git diff --check` frente a `2472fd6`, `9961d2d` y `9d6fb15` | Limpio |
| Delta frente al sucesor | Exactamente las cuatro rutas del cierre (A). Ninguna validación deja cambios en el árbol |

### 5.5 Checkout del equipo

El checkout original conserva los 20 artefactos preexistentes que FSY no certifica, tal como los identificó la reauditoría: los 19 `.pyc` de pytest y una incidencia agrupada de artefactos generados (`public/build`, cachés y Wayfinder). No se limpian. Con ellos, el gate de B2 sobre HEAD falla en FSY y el gate sucesor falla en MAT por esa regla, así que el cierre debe fallar solo en VIG. SF24 reproduce esa condición en un clon. Sobre el checkout original, la medición solo es posible con este commit ya presente en él; se registra en el reporte de entrega.

La certificación se hace en un clon limpio.

### 5.6 Sucesión vigente

| Gate | Papel | Dónde | Resultado en clon limpio |
|---|---|---|---|
| `validate_f35sbxb2_sucesor_freeze.py` | Gate sobre HEAD, en la rama de B2, `develop` y `main`. Protege la capa sucesora y la del cierre, y ejecuta el gate sucesor | HEAD | 12/0 |
| `validate_f35sbxb2_sucesor.py` | Evaluación material vigente (dentro de VIG) | HEAD | 5/2, solo ALC y MAT de clase A |
| `validate_f35sbxb2_sucesor.py` | Gate sucesor auditado | Anclado sobre `9d6fb15` | 7/0 |
| `validate_f35sbxb2.py` | Gate histórico de B2 (dentro de HIS del sucesor) | Anclado sobre `2472fd6` | 119/0 |
| `validate_f35sbxb2.py` | Evaluación material (dentro de MAT del sucesor) | HEAD | 118/1, solo SCP de clase A |
| `validate_f35sbxb2_freeze.py` | Integridad del candidato y del freeze (dentro de CON del sucesor) | HEAD, y anclado sobre `9961d2d` | 10/0 |
| `validate_f35sbxb.py` y `validate_f35sbxb_freeze.py` | Gates históricos de B1 y B1-FREEZE | Anclados sobre `8e94a60` y `3d9b783` | 159/0 y 14/0 |

Esta tabla supera la de §5.6 del documento del sucesor, congelado en `9d6fb15`. El gate sucesor sigue vigente, pero dentro del cierre y no como único gate sobre HEAD.

### 5.7 Riesgos residuales

| # | Nivel | Riesgo | Tratamiento |
|---|---|---|---|
| R1 | INFO | El ancla de nivel B solo autentica el cierre si se registra fuera: un cierre reconstruido con los mismos bytes en otra historia pasa con otra ancla (SF26) | La auditoría independiente anota el commit que informa FRZ, y un incremento sucesor autorizado lo registra. Es el último eslabón de B2: ningún archivo puede guardar el hash de su propio commit, y no se añade otra capa de freeze |
| R2 | INFO | VIG lee la salida textual del gate sucesor, que a su vez resume la del gate de B2 y muestra como mucho tres violaciones por regla | El formato se valida de forma estricta: líneas INFO, líneas FALLA y resumen, coherentes con el código de salida, con recuentos exactos y solo rutas del cierre en estado `A` |
| R3 | INFO | Cada ejecución tarda unos 40 segundos, porque el gate sucesor ejecuta dos veces el gate de B2 y una el validador del freeze | Es el coste de conservar la evaluación material completa |
| R4 | INFO | En el checkout del equipo, VIG falla por FSY (artefactos preexistentes) | Es deliberado: el checkout no se limpia y la certificación es en clon limpio |
| R5 | INFO | Cualquier cambio fuera de las cuatro rutas del cierre hace fallar ALC y VIG, incluido uno legítimo de un incremento futuro. Ningún commit posterior puede tocar la capa sucesora ni la del cierre | Es una falla de clase A para ese incremento, que aportará su propio gate sucesor. Las dos capas quedan inmutables |
| R6 | INFO | `CLAUDE.md` y `docs/PROGRESS.md` siguen describiendo B2 como candidata a auditoría | Actualización de gobierno pendiente de incremento sucesor autorizado |
| R7 | INFO | F34E lista las cuatro rutas nuevas entre las no autorizadas por DH-02 | Es la misma regla, como con B0..el sucesor |

### 5.8 Próximo paso

Auditoría independiente de B2-SUCCESSOR-FREEZE (reauditoría de AF-L02), que anota como ancla el commit que informa la línea INFO de FRZ. Hasta entonces:

- B2-SUCCESSOR-FREEZE no se aprueba;
- B2 no se declara cerrada, congelada ni integrada;
- no hay push, merge, tag ni release.
