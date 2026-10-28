# F36-SBX — Deuda técnica de la sexta auditoría (AF6)

> Registro documental del 27/10/2026, en la rama `docs/f36-sbx-gate-preparacion-af6`, desde `main` = `55f758e013e1852de8c8daa5d6fde95e39b02b0d`. Registra los dos hallazgos LOW que la [sexta auditoría independiente](F36SBX_Auditoria_AF6.md) dejó abiertos sobre el candidato integrado `4a2b2d7`. **No corrige el validador**: el código de [`validate_f36sbx.py`](../tools/f36sbx/validate_f36sbx.py) es el del candidato auditado. Ningún hallazgo de este registro cambia el estado de gobierno ni supera el gate. F36-SBX-GATE sigue NO SUPERADO y F37-SBX sigue BLOQUEADA.

## 1. Por qué este registro vive en el paquete

El registro general de deuda técnica es [`TECHNICAL_DEBT.md`](../TECHNICAL_DEBT.md). Este incremento no lo modifica, porque la regla FRZ del validador F36-SBX solo admite cambios dentro del paquete, de sus herramientas y de cuatro archivos de gobierno: un cambio en ese registro haría fallar el validador en esta rama y, tras integrarla, en `develop` y `main`. Replicar AF6-L01 y AF6-L02 en el registro general es la decisión pendiente D-03 de la [matriz de preparación del gate](preparacion-gate/F36SBX_Matriz_Preparacion_Gate.md#7-decisiones-que-requieren-intervención-humana). Hasta entonces, este documento es la fuente de los dos hallazgos; no se duplican en otro lugar.

## 2. Resumen

| ID | Severidad | Estado | Clase | Bloquea la integración técnica de AF5 |
|---|---|---|---|---|
| AF6-L01 | LOW | ABIERTO — NO BLOQUEANTE PARA LA INTEGRACIÓN TÉCNICA AF5 | Residuo de AF5-L01: vocabulario de relleno incompleto | No |
| AF6-L02 | LOW | ABIERTO — NO BLOQUEANTE PARA LA INTEGRACIÓN TÉCNICA AF5 | Residuo de AF5-L01: homógrafos latino/armenios | No |
| AF6-I01 | INFO | Observación de límites, sin acción obligatoria | Falsos rechazos estructurales conocidos | No |

**La clase AF5-L01 no está completamente cerrada.** La sexta auditoría confirmó corregidas sus tres reproducciones originales (`tbdplaceholder`, `placeholderxx` y `auditorfictionn`) y encontró estos dos residuos de la misma guardia.

## 3. AF6-L01 — composiciones con «relleno»

| Campo | Valor |
|---|---|
| Identificador | AF6-L01 |
| Severidad | LOW |
| Origen | Sexta auditoría independiente, sobre `4a2b2d7e78d162dc59e099325e3603407dcfb5fc` ([registro](F36SBX_Auditoria_AF6.md)) |
| Componente | Guardia estructural de identidad del validador: `IDENTITY_MARKER_WORDS`, `concatenated()` y `nondistinctive()` en [`validate_f36sbx.py`](../tools/f36sbx/validate_f36sbx.py) |
| Descripción | El validador acepta como identidad válida algunas composiciones genéricas que contienen la palabra de relleno «relleno»: `placeholderrelleno`, `placeholderconrellenonn`, `auditorrelleno` y `revisorrellenoxx` |
| Causa observada | Vocabulario estructural incompleto: contiene «rellene» y «rellenar», pero no «relleno». La gramática de composición no puede cubrir esa pieza y trata la palabra como distintiva |
| Evidencia reproducible | (1) Auditoría: con el CLI completo, un candidato sintético con FG-02 registrada a nombre de `placeholderrelleno` da 59/0 y exit 0, cuando el contrato exige el rechazo (gate §8.6). Reproducción mínima `reproduce_one.py <repositorio-fuente> <salida-nueva> placeholderrelleno`; resultados en `repro-AF6-L01/results.json` (SHA-256 `7f42e3ca99035fa4981d654068d85a25a74433e0a3bbb426326b8e63ecad930e`). (2) Reproducción propia de este incremento, en memoria y sin tocar el código, sobre el validador integrado: `identity_errors()` devuelve una lista vacía para las cuatro cadenas, y rechaza `auditorfictionn` |
| Impacto | Falso PASS acotado de la guardia estructural de identidad del registro de FG-02 |
| Limitaciones | No es autenticación de personas: el validador nunca la ofreció. No supera el gate por sí solo, porque FG-02 sigue exigiendo un informe coherente y el gate exige además FG-03, FG-10 y FG-12 con 3/3 aprobaciones humanas. No afecta al runtime de la aplicación |
| Estado | **ABIERTO — NO BLOQUEANTE PARA LA INTEGRACIÓN TÉCNICA AF5** |
| Acción correctiva propuesta | En un incremento propio, con RED y GREEN: añadir «relleno» y sus flexiones («rellenos», «rellena», «rellenas») al vocabulario de marcadores; revisar de forma sistemática las familias léxicas de cada marcador ya presente (sustantivo, verbo e imperativo); y añadir las cuatro cadenas a la batería, con un control positivo de nombres que contengan esos fragmentos |
| Criterio de aceptación futuro | Las cuatro cadenas, y las variantes de la misma familia léxica, fallan con el CLI completo con exit 1 y el motivo de identidad compuesta. Los 99 nombres plausibles de AF5-L01-P1, más `Lola Donato`, `Tempel Moreno` y `Li Wu`, siguen pasando. Una ablación de la nueva entrada del vocabulario queda detectada por un caso pertinente. Una auditoría independiente lo confirma |
| Dependencia de revisión humana | Sí. La identidad de un auditor la verifica el equipo antes de registrar FG-02, con o sin esta corrección: la guardia es estructural |

## 4. AF6-L02 — homógrafos latino/armenios

| Campo | Valor |
|---|---|
| Identificador | AF6-L02 |
| Severidad | LOW |
| Origen | Sexta auditoría independiente, sobre `4a2b2d7` |
| Componente | `identity_tokens()`, `LATIN_FOLD` y `mixed_script()` en [`validate_f36sbx.py`](../tools/f36sbx/validate_f36sbx.py) |
| Descripción | El validador acepta `auditorfictioոո`, cuyas dos letras finales son U+0578 (ARMENIAN SMALL LETTER VO), visualmente semejantes a «n». Su equivalente ASCII, `auditorfictionn`, se rechaza |
| Causa observada | Normalización y detección de escrituras mixtas incompletas: `LATIN_FOLD` no pliega U+0578, y `mixed_script()` solo detecta la mezcla del latín con el cirílico o el griego |
| Evidencia reproducible | (1) Auditoría: CLI completo con 59/0 y exit 0 sobre un candidato sintético con FG-02 a ese nombre. Reproducción `reproduce_one.py <repositorio-fuente> <salida-nueva> auditorfictioոո`; resultados en `repro-AF6-L02/results.json` (SHA-256 `931dc4fb1f8e5c4f571d5e6bbe8c8412fa0202a87fdeac647c3c3130db9e428e`). (2) Reproducción propia, en memoria: `identity_errors()` acepta la cadena (U+0578 dos veces) |
| Impacto | Evasión acotada de la guardia estructural de homógrafos |
| Limitaciones | Mismo alcance que AF6-L01: no hay autenticación, no hay habilitación automática y el gate exige actos humanos. Los nombres armenios u otros no latinos legítimos no deben prohibirse: la corrección no puede consistir en rechazar escrituras no latinas |
| Estado | **ABIERTO — NO BLOQUEANTE PARA LA INTEGRACIÓN TÉCNICA AF5** |
| Acción correctiva propuesta | En un incremento propio, con RED y GREEN: (a) tratar como homógrafo toda palabra que mezcle el latín con otra escritura (no solo el cirílico o el griego), salvo las combinaciones que se justifiquen; o (b) plegar con una tabla de confusables acotada y documentada (por ejemplo, un subconjunto de los confusables de Unicode TR39) antes de clasificar. La opción la decide el equipo |
| Criterio de aceptación futuro | `auditorfictioոո` y variantes con otras letras armenias, georgianas o cherokee semejantes a latinas fallan con exit 1; un nombre íntegramente armenio, uno íntegramente cirílico y uno griego siguen pasando; la corrección no añade dependencias; una ablación queda detectada; una auditoría independiente lo confirma |
| Dependencia de revisión humana | Sí, como en AF6-L01, y además para decidir qué escrituras admite la guardia |

## 5. AF6-I01 — límites conocidos (INFO)

La auditoría documentó falsos rechazos estructurales de palabras sueltas: `Tempel` (`temp` + `el`), `Stubb`, `Holder`, `Nil`, `Uno`, `Una` y `Dona`, además del mínimo contractual de tres letras (`Li`, `Wu` y `Ng` aislados). Los nombres completos con una palabra distintiva pasan (`Tempel Moreno`, `Li Wu`). No exige acción. Cualquier corrección de AF6-L01 o AF6-L02 debe comprobar que no empeora estos límites.

## 6. Lo que este registro no hace

- No modifica el validador, la batería, el contrato, el esquema de evidencia ni el estado del gate.
- No declara cerrada la clase AF5-L01.
- No convierte la auditoría en evidencia de equipo: ver [registro de la sexta auditoría](F36SBX_Auditoria_AF6.md#6-qué-no-es-esta-auditoría).
