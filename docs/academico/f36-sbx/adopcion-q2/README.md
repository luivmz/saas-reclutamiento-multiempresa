# BORRADOR — SIN EMISIÓN — SIN ADOPCIÓN

## F36-SBX — Paquete de adopción de Q2: borradores para los tres integrantes

> **BORRADOR — SIN EMISIÓN — SIN ADOPCIÓN.** Paquete del 31/10/2026, corregido el 01/11/2026 tras una revisión de Codex ([correcciones](#revisión-de-codex-y-correcciones)), en la rama local `docs/f36-sbx-q2-adoption-drafts`, creada desde la versión aprobada V de Q2. Prepara los documentos con los que Luis Vila Meza, Fredy Coronacion y Anthony Peña pueden decidir, cada uno por su cuenta, sobre la adopción del modelo y sobre las delegaciones. No contiene ninguna decisión, firma, fecha de emisión ni evidencia, y no se ha enviado a nadie. Lo preparó Claude Code; no es un acto humano.
>
> Estados vigentes, sin cambios: G0 real = NO APROBADA; G0-SBX = APROBADA CON RESTRICCIONES; ADR-005 = PROPUESTA; F35-SBX = CERRADA Y CONGELADA; F36-SBX = EN DISEÑO; F36-SBX-GATE = NO SUPERADO; F37-SBX = BLOQUEADA; alcance C = BLOQUEADO; datos reales = PROHIBIDOS. Q2 sigue siendo una propuesta no adoptada.

## La versión V

| Dato | Valor |
|---|---|
| Commit | `8b1f068b5ac2039139ab5756096c147c11c9fcb2` |
| Árbol | `b5b81718680762f9585e4dae969ca44e69114865` |
| Rama | `docs/f36-sbx-team-governance-proposal` |
| Propuesta | [`PROPUESTA_Q2_Gobierno_Equipo.md`](../reconciliacion-gobierno/PROPUESTA_Q2_Gobierno_Equipo.md): blob `8d83d17bf94b917d9cb654d6aca6d7dd4ff73d3b`, 28342 bytes |
| SHA-256 de la propuesta | `8829a0380bf7ea118b24d70c070de791bdf8efe4615a8f6a70372d403c0e71d0` |
| Revisión favorable | De Codex, del 31/10/2026: APROBADA COMO PROPUESTA DOCUMENTAL. La ubicación y los hashes están en [E §3](E_Preparacion_RR.md#3-informe-favorable-ubicación-y-comprobación) |

Esta rama no modifica ninguno de los cinco documentos de la [carpeta de Q2](../reconciliacion-gobierno/README.md): son los mismos de V.

## Cómo consultar Q2 completa

1. **En el repositorio:** [`PROPUESTA_Q2_Gobierno_Equipo.md`](../reconciliacion-gobierno/PROPUESTA_Q2_Gobierno_Equipo.md). En esta rama es el mismo archivo que en V.
2. **La copia exacta de V desde Git**, en Git Bash, macOS o Linux:

   ```text
   git cat-file blob 8b1f068:docs/academico/f36-sbx/reconciliacion-gobierno/PROPUESTA_Q2_Gobierno_Equipo.md > Q2_V_8b1f068.md
   ```

   En Windows PowerShell 5.1 no se usa `>`, que reescribe el archivo en UTF-16 y cambia sus bytes. Se puede usar Git Bash, o el mismo comando dentro de `cmd /c "…"`.
3. **Comprobar la copia.** Su SHA-256 tiene que ser `8829a0380bf7ea118b24d70c070de791bdf8efe4615a8f6a70372d403c0e71d0`:
   - Windows: `certutil -hashfile Q2_V_8b1f068.md SHA256`;
   - macOS: `shasum -a 256 Q2_V_8b1f068.md`;
   - Git Bash o Linux: `sha256sum Q2_V_8b1f068.md`.
4. **Sin Git.** Luis comparte el archivo y quien lo recibe compara el SHA-256. El hash prueba que el contenido es el de V, pero no prueba quién lo envió.

## Contenido

| Archivo | Qué es | Lo emitiría | Estado |
|---|---|---|---|
| [A. Explicación](A_Explicacion_para_integrantes.md) | Qué se decide y qué no, en lenguaje sencillo | No es un acto | Borrador |
| [B. R-01](B_BORRADOR_R-01_Luis_Vila_Meza.md) | Declaración de Luis sobre la composición, los roles, los entornos y el uso de IA | Luis Vila Meza | Sin emitir |
| [C1. CM-01](C1_BORRADOR_CM-01_Luis_Vila_Meza.md) | Conformidad con V | Luis Vila Meza | Sin emitir |
| [C2. CM-02](C2_BORRADOR_CM-02_Fredy_Coronacion.md) | Conformidad con V | Fredy Coronacion | Sin emitir |
| [C3. CM-03](C3_BORRADOR_CM-03_Anthony_Pena.md) | Conformidad con V | Anthony Peña | Sin emitir |
| [D1. DF-02](D1_BORRADOR_DF-02_Fredy_Coronacion.md) | Delegación opcional en Luis | Fredy Coronacion | Sin emitir |
| [D2. DF-03](D2_BORRADOR_DF-03_Anthony_Pena.md) | Delegación opcional en Luis | Anthony Peña | Sin emitir |
| [E. Preparación del RR](E_Preparacion_RR.md) | Estructura y requisitos del registro raíz | Un incremento posterior | Sin RR |
| [F. Textos y conservación](F_Textos_para_compartir_y_conservacion.md) | Mensajes que Luis puede compartir y cómo conservar las respuestas | Luis, si decide compartir | Borrador |
| [G. Continuidad](G_Continuidad.md) | Etapas desde los borradores hasta B-01, H y el gate | No es un acto | Borrador |

## Lo que este paquete no hace

- **No emite actos:** ni R-01, ni CM, ni DF, ni un RR. No adopta Q2, no envía mensajes y no contacta a nadie.
- **No modifica** V, los cinco documentos de Q2, los contratos, las skills, los validadores, el JSON del gate ni los estados formales.
- **No concede facultades.** Una delegación solo existe cuando su titular la emite, y solo pasa a Luis la intersección, después de un RR.
- **No autoriza** ML, datos reales, producción, el alcance C ni un ADR, ni supera ningún gate.
- **No determina D-10,** no emite D-11 y no autoriza B-01.
- **No atribuye** contribuciones, firmas ni aprobaciones a Fredy ni a Anthony, y no presenta ninguna IA como persona.

## Revisión de Codex y correcciones

Una sesión de Codex separada revisó el candidato `23dc4187a7936c5fe832d35b5d8a446786ae39bf` el 01/11/2026. Su veredicto fue **CORRECCIONES REQUERIDAS**, con 0 BLOCKER, 0 HIGH, 2 MEDIUM, 0 LOW y 0 INFO. El informe está fuera del repositorio, donde Codex lo dejó:

`C:/Users/Vila/.codex/visualizations/2026/10/27/01a17ebf-75df-7883-a55e-3ede1b24ee18/F36-Q2-Adoption-Drafts-23dc418/Informe_Revision_Borradores_Adopcion_Q2_23dc418.md`

Su SHA-256 es `43102ddf54a7ffab2ee6e02e6a1037462b8362192d77e5b679d541289c2f6b2b`, y figura en el manifiesto `SHA256SUMS.txt` de su carpeta, cuyo SHA-256 es `3f894bc65953233a9ad320aa10cd9aee9037d3bf4a1751479d258e69a7d0e8e6`.

| Hallazgo | Corrección | Dónde | Estado |
|---|---|---|---|
| **Q2AD-M01**, MEDIUM: el catálogo Git añadía operaciones que V no enumera en N3 | Se retiró GIT-1 (push de ramas de trabajo), y GIT-3 quedó en el merge en `main`, sin su push. Lo que no está en la lista conserva la autorización del contrato 10. GIT-2 a GIT-5 conservan su número | DF-02 y DF-03, §2.1 y §2.2; explicación, §7; ejemplo de E, §5; correo de F, §4 | Implementada; pendiente de reauditoría |
| **Q2AD-M02**, MEDIUM: GATE-3 permitía a Luis decidir por sí solo la frontera entre los alcances B y C | Se retiró GATE-3. La confirmación de EI-09 (F36-M02) queda para actos auténticos y el procedimiento vigente. GATE-1 ya no remite a GATE-3: para EI-09 exige esa confirmación y las condiciones de la matriz | DF-02 y DF-03, §2.3; ejemplo de E, §5 | Implementada; pendiente de reauditoría |

Lo retirado se conserva, para su trazabilidad, en notas «Fuera de la lista, sin casilla». Ningún hallazgo se da por cerrado aquí: eso corresponde a la reauditoría.

## Validación de este paquete

Ejecutada el 01/11/2026 sobre esta rama, después de las correcciones:

| Comprobación | Resultado |
|---|---|
| Funciones de prosa del validador de F36-SBX (`forbidden_claims`, `state_claims` con `allowed_states` e `invisible_chars`), NFC, marcadores de conflicto, espacios finales y patrones de PII del validador, en los 11 archivos | 0 problemas. El validador no lee esta carpeta, que no está en `PKG_DOCS`, así que se comprobó aparte |
| Rótulo «BORRADOR — SIN EMISIÓN — SIN ADOPCIÓN», casillas, fechas y canales | Rótulo presente en los 11 archivos, en el título y en el aviso inicial. Ninguna casilla marcada. Las fechas, los canales y las evidencias de emisión siguen en PENDIENTE |
| Facultades retiradas | GIT-1, el `push` de `main` y GATE-3 solo aparecen en las notas «Fuera de la lista, sin casilla» de las delegaciones y en la sección anterior. Ningún ejemplo las computa |
| Catálogo frente a V | GIT-2 a GIT-5 corresponden a operaciones que enumera el nivel N3 (Q2 §4 y §10); B01-1, a D-02b (Q2 §8 y §10); GATE-1 y GATE-2, a FG-03 y FG-10 con un contrato sucesor (Q2 §8) |
| Enlaces relativos y anclas | 51 enlaces, 16 de ellos con ancla; ninguno roto |
| Hashes citados | 11 tokens de longitud Git: 7 commits, 1 árbol y 1 blob que resuelven en Git, y 2 segmentos del UUID de la carpeta de Codex, que no son objetos Git. 5 SHA-256 completos (la propuesta en V, el informe favorable y su manifiesto, y el informe de la revisión de estos borradores y su manifiesto), comprobados contra sus bytes |
| DF-02 frente a DF-03, y CM-02 frente a CM-03 | Iguales, salvo el titular y sus identificadores |
| [`validate_f36sbx.py`](../../tools/f36sbx/validate_f36sbx.py), sin cambiar su nombre, su base ni sus reglas | 55 correctas y 4 fallas, con el mismo patrón que V en las 59 comprobaciones: «FRZ — rama admitida», por el anclaje de rama; las dos de contenido de FRZ, por las mismas 18 rutas externas y 11 entradas de runtime de SEG; y GATE, por FG-01 y FG-05. Frente a V solo cambian el nombre de la rama y el total de rutas de FRZ, que pasa de 49 a 60 por los 11 archivos de esta carpeta, dentro del paquete |
| Alcance | Frente a V, 11 archivos nuevos en esta carpeta y nada fuera de ella; los cinco documentos de Q2 y el resto del árbol son idénticos a V. Frente a `23dc418`, solo cambian 6 archivos de esta carpeta |
| Pruebas funcionales | No se ejecutaron: el incremento es solo documental y no cambia código |
