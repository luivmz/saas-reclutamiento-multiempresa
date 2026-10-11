# F35-SBX-B — B1-FREEZE: cierre controlado de B1

> **Estado: B1 = FREEZE IMPLEMENTADO / PENDIENTE DE AUDITORÍA POST-FREEZE.** Fecha: 11/10/2026. Rama `feature/f35-sbx-b-deterministic-pipeline`.
>
> Este documento formaliza el cierre del incremento B1 de F35-SBX-B sin modificar el contenido auditado. Sigue el protocolo de sucesión de [B0](../evidencia-sbx-b/F35SBXB_B0_Sucesion_de_Gates.md) y el ciclo de vida del gate descrito en [B1 §5](../evidencia-sbx-b/F35SBXB_B1_Gate_Sucesor.md#5-el-gate-del-gate).

## 1. Ancla auditada y commit de cierre

| Referencia | Valor | Qué identifica |
|---|---|---|
| `AUDITED_B1_ANCHOR` | `8e94a60274fe39ebda3e9961bc58036b389dfc00` | El contenido de B1 que aprobó la auditoría independiente final. Resultado registrado: «B1 APROBADA PARA CIERRE», con el gate en 159/0 y SBX-01..SBX-18 en PASS |
| Commit de cierre | Posterior al ancla; se consulta en Git | El commit que añade este documento, el manifiesto y el validador de cierre |
| Base de B | `430f3f544c3542cabac8028a122c8a0c2a97390b` | `develop` al iniciar F35-SBX-B |

El commit de cierre no sustituye al ancla. El ancla sigue siendo la referencia histórica del contenido aprobado. Ningún archivo registra el hash del commit de cierre, que sería autorreferencial: Git lo identifica como el commit que introduce estos tres archivos.

## 2. Conjunto congelado

El conjunto congelado se deriva de Git, no del árbol de trabajo. Son las rutas que B1 cambió respecto de la base de B (`git diff --name-status --no-renames 430f3f5 8e94a60`), con su entrada en el ancla:

| Ruta | Frente a la base | Modo | Blob en el ancla | SHA-256 |
|---|---|---|---|---|
| `CLAUDE.md` | M | 100644 | `b7068afbfac6cc2f1f39053dff8face38b894415` | `1d21eb8f8684c789c457bb5851088154a26f21ac2a3b62dce4e42784a3495fd7` |
| `docs/PROGRESS.md` | M | 100644 | `983844fd2477432b2a1ea402aa8b3130678a014a` | `cd87b69896abee54a6da4502896a2b4adb3ed5a4f89dc62c88cf92ef469e664a` |
| `docs/academico/evidencia-sbx-b/F35SBXB_B1_Gate_Sucesor.md` | A | 100644 | `189c66dbdcb5d8b40a403de31f8329ae39c25297` | `b57d15185cd9b8f7179d957d14fd5339b52fc2d94ce861f0e7a48e9969efd388` |
| `docs/academico/evidencia-sbx-b/README.md` | M | 100644 | `1cf55c3f0aae1ee1b688af9c15abca394c0929b5` | `4c5f574b6820b7afbe66316e7f88dd988cc49f1046fa645216df5e61c1d735b8` |
| `docs/academico/tools/f35sbxb/validate_f35sbxb.py` | A | 100644 | `e98f3b96335e296aa66153a8a10d9a62f4bc2c49` | `3dd84bd87ad09ec0a22e821bf115edecb646fcef178056fabdb295cca1de8870` |

El [manifiesto](../tools/f35sbxb_freeze/b1_freeze_manifest.json) registra además:

- el ancla, la base de B, E y el cierre de B0;
- el tamaño de cada archivo;
- las carpetas con su contenido exacto;
- los tres archivos del cierre;
- los trece estados de gobierno vigentes.

El manifiesto es determinista: no tiene marcas de tiempo dinámicas. El validador lo contrasta con Git en cada ejecución.

Ninguna de las cinco rutas cambia en el cierre. El mecanismo vive en rutas nuevas, separadas de las de B1:

| Archivo | Contenido |
|---|---|
| `docs/academico/tools/f35sbxb_freeze/validate_f35sbxb_freeze.py` | Validador del cierre: biblioteca estándar, sin red, aislado y con fallo cerrado |
| `docs/academico/tools/f35sbxb_freeze/b1_freeze_manifest.json` | Manifiesto del conjunto congelado |
| `docs/academico/evidencia-sbx-b-freeze/F35SBXB_B1_Freeze.md` | Este documento |

## 3. Qué comprueba el validador

Uso: `python -I docs/academico/tools/f35sbxb_freeze/validate_f35sbxb_freeze.py`. Si se invoca sin `-I`, se relanza aislado igual que el gate de B1.

| ID | Comprobación |
|---|---|
| FRZ | El manifiesto coincide con Git: el ancla, la base, el conjunto derivado del delta de B1, y el modo, el blob, el SHA-256 y el tamaño en el ancla. Además: el ancla es un commit y ancestro de HEAD, la historia no es superficial, y las cinco rutas son idénticas al ancla en cuatro lugares (§4 y §5). Las cuatro carpetas de B y del cierre tienen su contenido exacto |
| B1 | Las reglas del gate de B1 sobre HEAD: CTX, AIN, HST, B0F, SBX (SBX-01..SBX-18 recalculados), GOV, FSY, FLG, CNT y DEP. El gate se carga desde los bytes ya verificados contra el ancla, nunca releyendo el archivo. SCP usa el alcance exacto de B1 más los tres archivos del cierre |
| FCN | Los tres archivos del cierre: UTF-8 sin CR ni BOM, sin PII, sin claves JSON prohibidas, sin afirmaciones que habiliten capacidades prohibidas y sin declaraciones de estado contradictorias. Se reutilizan las reglas CNT del gate |
| FDP | El validador del cierre solo importa la biblioteca estándar autorizada. Se reutiliza la regla DEP del gate |

Las reglas reutilizadas no se reinterpretan: es el mismo gate auditado, verificado byte a byte antes de ejecutarse, como prevé el principio F de B0. El validador del cierre es el único módulo del repositorio cargado antes de `compute_sbx()`. Por eso se retira de `sys.modules` mientras el gate recoge el estado. No forma parte del inventario de DH-B13 y su integridad la acredita la auditoría post-freeze.

## 4. Historia y merges

La regla de historia comprueba el contenido. Para cada commit descendiente del ancla que lleva a HEAD (`git rev-list --ancestry-path 8e94a60..HEAD`), las cinco rutas deben tener exactamente el modo, el tipo y el blob del ancla. Esa lista incluye los merges.

- **Modificación y restauración.** El commit intermedio que cambió una ruta es descendiente del ancla, así que el gate lo rechaza aunque otro commit la restaure después.
- **Merge legítimo.** Un merge `--no-ff` de la rama de B en `develop`, o de `develop` en `main`, lleva el contenido del ancla intacto. Que su otro padre no contenga B1 no importa: ese padre no desciende del ancla y no entra en la lista. El merge pasa.
- **Merge con alteración.** Un merge que resuelve una ruta congelada con otro contenido es descendiente del ancla y su árbol difiere, así que el gate lo rechaza aunque un commit posterior lo restaure.
- **Por qué no la regla de padres.** Se descartó «difiere de algún padre = alteración», porque haría fallar toda integración legítima. También se descartó «difiere de todos los padres», porque no detecta un merge que restaura la versión anterior de un padre sin B1.
- **Historia insuficiente.** Un repositorio superficial, un ancla ausente o un HEAD que no desciende del ancla fallan cerrados.

Si un incremento posterior autorizado cambia una de las cinco rutas, por ejemplo para registrar en `CLAUDE.md` el cierre de B1 tras la auditoría post-freeze, este validador fallará sobre ese HEAD, y debe fallar. Ese incremento aportará su propio gate sucesor y ejecutará este validador anclado sobre el commit de cierre (§6).

## 5. Índice, árbol de trabajo y sistema de archivos

- **Árbol de HEAD.** Cada ruta presente, con el modo 100644, el tipo y el blob del ancla. Un renombrado o una eliminación dejan la ruta ausente, y un enlace aparece con modo 120000.
- **Índice.** Una sola entrada por ruta, en etapa 0, con el modo y el blob del ancla. Además, ningún flag `h`, `S` o `s` en todo el repositorio, porque ocultaría cambios.
- **Disco.** Un archivo regular, sin enlaces en ningún componente de la ruta, con los bytes del blob del ancla y, en POSIX, sin bit de ejecución.
- **Carpetas.** `evidencia-sbx-b/`, `tools/f35sbxb/`, `evidencia-sbx-b-freeze/` y `tools/f35sbxb_freeze/` con su contenido exacto, incluidos archivos ignorados u ocultos y sin `__pycache__`.
- **Alcance.** SCP compara el árbol de HEAD, el árbol de trabajo, el índice y los archivos sin seguimiento con la base de B. FSY recorre las superficies del runtime y de la evidencia.

Los artefactos generados del checkout del equipo (`public/build/`, Wayfinder, `bootstrap/cache/` y los `.pyc` de pytest) no pertenecen al conjunto congelado. Siguen fallando en FSY del gate de B1, como documenta [B1 §10.3](../evidencia-sbx-b/F35SBXB_B1_Gate_Sucesor.md#103-m03-metadatos-no-son-código-ejecutable). El checkout no se limpia para obtener un PASS.

## 6. Sucesión de gates

| Etapa | Gate sobre HEAD | Evidencia histórica |
|---|---|---|
| B1 auditada (ancla `8e94a60`) | `validate_f35sbxb.py` | — |
| B1-FREEZE (ahora) | `validate_f35sbxb_freeze.py`, en la rama de B, `develop` y `main` | `validate_f35sbxb.py` ejecutado anclado sobre `8e94a60`, en un clon sin remoto |
| Integración futura (`--no-ff` en `develop` y `main`) | El mismo validador del cierre: los merges legítimos pasan (§4) | Igual |
| Incremento autorizado siguiente | Su propio gate sucesor | Este validador, anclado sobre el commit de cierre |

Sobre un HEAD posterior al ancla, el gate de B1 falla en SCP, porque los tres archivos del cierre quedan fuera de su alcance fijo. Es la falla de alcance histórico prevista por B0 (clase A). No se corrige modificando el gate congelado.

Mientras la auditoría post-freeze no apruebe este cierre, B1 sigue IMPLEMENTADA y pendiente de esa auditoría. Ningún archivo de gobierno se modifica en este cierre. El registro del cierre de B1 en gobierno lo hará el incremento siguiente autorizado, con su gate sucesor.

Los estados de gobierno no cambian:

- G0 real = NO APROBADA y ADR-005 = PROPUESTA;
- G0-SBX = APROBADA CON RESTRICCIONES;
- F35 productiva = BLOQUEADA y F36–F40 = BLOQUEADAS;
- Alcance C = BLOQUEADO y datos reales = PROHIBIDOS;
- F35-SBX-B sigue INICIADA y B2 no se inicia hasta la integración con CI en verde.

## 7. Pruebas del cierre

Con Git real, en clones desechables sin remoto y ya eliminados, con los tres archivos del cierre confirmados sobre el ancla (el mismo contenido del commit de cierre):

| Caso | Resultado | Regla |
|---|---|---|
| N1. Estado limpio, con invocación normal (se relanza aislado) y con `python -I` | PASS, 14/0, con SBX-01..SBX-18 en 18/18 | — |
| N2. Un byte añadido a `CLAUDE.md` sin confirmar, y un byte del gate confirmado | FAIL | FRZ |
| N3. Modo 100755 en el gate, en el índice y confirmado | FAIL | FRZ |
| N4. README eliminado y documento de B1 renombrado, ambos confirmados | FAIL | FRZ |
| N5. Enlace simbólico en lugar del README | FAIL | FRZ |
| N6. Modificar, confirmar, restaurar y confirmar | FAIL | FRZ (historia) |
| N7. assume-unchanged en `CLAUDE.md` y skip-worktree en el documento de B1, con un cambio que `git status` no ve | FAIL | FRZ |
| N8. `GIT_DIR` inválido | FAIL cerrado, sin trazas | FRZ |
| N9. Clon superficial | FAIL cerrado, sin trazas | FRZ |
| N10. `develop` tras `merge --no-ff` de la rama de B, y `main` tras `merge --no-ff` de `develop` | PASS, 14/0 en ambos | — |
| N11. Merge con el gate alterado; merge alterado y restaurado después; rama lateral que altera y restaura, integrada con un merge | FAIL | FRZ (historia) |
| Archivo ignorado añadido junto al gate | FAIL | FRZ (carpetas) |

Las 14 comprobaciones son:

- FRZ;
- las once reglas del gate de B1, con SCP en su alcance ampliado;
- FCN y FDP.

El gate de B1 da:

- sobre el HEAD posterior al cierre, 158/1: solo falla SCP, por los tres archivos del cierre, como prevé §6;
- anclado sobre `8e94a60`, 159/0, con SBX-01..SBX-18 en PASS.

Regresión mínima en un clon limpio:

- `validate.py` y `validate.py --cierre-f29`: 0 fallas;
- `validate_f29.py`: 225/0; `test_f32_safety.py`: OK; `validate_f34a.py`: 108/0;
- enlaces: 1082, 0 rotos; MANIFEST y evidencias: 0 discrepancias;
- `git diff --check`: limpio.

En el checkout del equipo, con los artefactos generados, el validador da 13/1: falla FSY del gate de B1 por esos artefactos (§5), igual que antes del cierre.

## 8. Riesgos LOW aceptados

- **Límites lingüísticos de B1.** Siguen los documentados en B1 §10.5, §11.4 y §11.5: la semántica es acotada, la prohibición alejada del verbo y la voz pasiva sin agente dan falsos positivos conservadores, y la doble negación de §11.5 pasa sin detectarse.
- **Código anterior al gate.** El que ejecuta el intérprete antes del gate (`sitecustomize` en `PYTHONPATH`, el sitio de Python) queda fuera de su alcance. El validador falla si `PYTHONPATH` está definida.
- **Bit de ejecución en Windows.** No se comprueba en el disco; se comprueba el modo del índice y del árbol.
- **Archivos de gobierno congelados.** Las cinco rutas incluyen `CLAUDE.md` y `docs/PROGRESS.md`. Cualquier cambio de gobierno posterior hace fallar este validador, y lo debe asumir el gate sucesor del incremento que lo haga (§4 y §6).

## 9. Próximo paso

Auditoría independiente post-freeze. Hasta entonces no hay integración, push, B2, SQLite, pipeline ni ML.
