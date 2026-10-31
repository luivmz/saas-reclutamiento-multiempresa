# BORRADOR — SIN EMISIÓN — SIN ADOPCIÓN

## F36-SBX — Paquete de adopción de Q2: borradores para los tres integrantes

> **BORRADOR — SIN EMISIÓN — SIN ADOPCIÓN.** Paquete del 31/10/2026, en la rama local `docs/f36-sbx-q2-adoption-drafts`, creada desde la versión aprobada V de Q2. Prepara los documentos con los que Luis Vila Meza, Fredy Coronacion y Anthony Peña pueden decidir, cada uno por su cuenta, sobre la adopción del modelo y sobre las delegaciones. No contiene ninguna decisión, firma, fecha de emisión ni evidencia, y no se ha enviado a nadie. Lo preparó Claude Code; no es un acto humano.
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

## Validación de este paquete

Ejecutada el 31/10/2026 sobre esta rama:

| Comprobación | Resultado |
|---|---|
| Funciones de prosa del validador de F36-SBX (`forbidden_claims`, `state_claims` con `allowed_states` e `invisible_chars`), NFC, marcadores de conflicto, espacios finales y patrones de PII del validador, en los 11 archivos | 0 problemas. El validador no lee esta carpeta, que no está en `PKG_DOCS`, así que se comprobó aparte |
| Rótulo «BORRADOR — SIN EMISIÓN — SIN ADOPCIÓN» y casillas | Presente en los 11 archivos, en el título y en el aviso inicial. Ninguna casilla marcada |
| Enlaces relativos y anclas | 48 enlaces, 13 de ellos con ancla; ninguno roto |
| Hashes citados | 9 tokens de longitud Git: 5 commits, 1 árbol y 1 blob que resuelven en Git, y 2 segmentos del UUID de la carpeta de Codex, que no son objetos Git. 3 SHA-256 completos (la propuesta en V, el informe favorable y su manifiesto), comprobados contra sus bytes |
| DF-02 frente a DF-03, y CM-02 frente a CM-03 | Iguales, salvo el titular y sus identificadores |
| [`validate_f36sbx.py`](../../tools/f36sbx/validate_f36sbx.py), sin cambiar su nombre, su base ni sus reglas | 55 correctas y 4 fallas, con el mismo patrón que V en las 59 comprobaciones: «FRZ — rama admitida», por el anclaje de rama; las dos de contenido de FRZ, por las mismas 18 rutas externas y 11 entradas de runtime de SEG; y GATE, por FG-01 y FG-05. Frente a V solo cambian el nombre de la rama y el total de rutas de FRZ, que pasa de 49 a 60 por los 11 archivos de esta carpeta, dentro del paquete |
| Alcance frente a V | 11 archivos nuevos en esta carpeta y nada fuera de ella. Los cinco documentos de Q2 y el resto del árbol son idénticos a V |
| Pruebas funcionales | No se ejecutaron: el incremento es solo documental y no cambia código |
