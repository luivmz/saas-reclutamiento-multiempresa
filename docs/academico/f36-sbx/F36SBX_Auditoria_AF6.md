# F36-SBX — Registro de la sexta auditoría independiente (AF6)

> Registro documental del 27/10/2026, en la rama `docs/f36-sbx-gate-preparacion-af6`, desde `main` = `55f758e013e1852de8c8daa5d6fde95e39b02b0d`. Resume, como **antecedente técnico verificable**, la auditoría independiente del candidato AF5. **No es evidencia de equipo, no registra FG-02 y no cambia ningún estado**: F36-SBX-GATE = NO SUPERADO, F37-SBX = BLOQUEADA.

## 1. Identidad

| Dato | Valor, verificado con Git al preparar este registro |
|---|---|
| Candidato auditado | `4a2b2d7e78d162dc59e099325e3603407dcfb5fc`, rama `feature/f36-sbx-authorization-design` |
| Árbol del candidato | `01dc59a80eed0e9f7c26143f6787010fcefb406c` |
| Padre | `b2876fca59deaaa3f3f06f65d7c92bc143d0f865` |
| Base | `b8892af39a6492d8dd44a36290604efc602380cd`, ancestro del candidato |
| Merge en `develop` | `55456943059efaa7b34fd7550de97986f0d13061`, padres `87ef831` y `4a2b2d7`; CI `tests` run 40612001723, `completed/success` |
| Merge en `main` | `55f758e013e1852de8c8daa5d6fde95e39b02b0d`, padres `b8892af` y `5545694`; CI `tests` run 40612169648, `completed/success` |
| Árbol de `main` tras el merge | `01dc59a…`, idéntico al del candidato |
| Auditor | Codex, sesión de auditoría independiente, 27/10/2026 (America/Lima) |
| Corrección auditada | [Corrección AF5](F36SBX_Correccion_AF5.md) |

## 2. Alcance y método

**Alcance.** Focal sobre AF5 y sus dependencias: AF5-M01 (lectura normativa y contenido externo), AF5-L01 (identidades compuestas) y la regresión relevante de AF2, AF3 y AF4. El delta AF4 → AF5 son seis commits y 11 archivos (7 Markdown y 4 Python), solo bajo `docs/academico/f36-sbx/` y `docs/academico/tools/f36sbx/`. No cambian runtime, dependencias, Docker, CI, F34 ni F35-SBX.

**Método independiente**, según el informe:

- revisión del gobierno vigente, de las skills del proyecto y del código y la documentación AF5;
- reproducción de las baterías oficiales sin modificarlas, en Windows y en WSL (Ubuntu 24.04);
- builders propios que no importan los del implementador, en clones nuevos, con el CLI del validador como proceso separado: 60 ejecuciones propias del CLI, entre ellas la reproducción con un enlace simbólico real en Linux;
- sondeos de identidad propios: 114 identidades plausibles y 142 variantes negativas;
- 54 ablaciones focales elegidas por el auditor, sin repetir la selección del implementador;
- comprobación final de integridad del repositorio original (1.235 archivos versionados, índice, refs y stash).

Las autorizaciones y fixtures de sus pruebas son sintéticos y solo existieron en clones desechables.

## 3. Resultados reproducidos

| Prueba | Windows | WSL Ubuntu 24.04 |
|---|---|---|
| `validate_f36sbx.py` | 59/0 | 59/0 |
| `test_f36sbx.py` | 545/0 | 545/0 |
| `test_f36sbx_git.py` | 113/0 y 2 omitidos (enlaces simbólicos sin privilegio) | 115/0, sin omitidos |
| Ablaciones focales | 54 distintas, 54 detectadas por casos pertinentes y 0 supervivientes, entre ambos entornos | |

Sobre las ablaciones: en Linux hubo una superviviente, la comprobación del modo del índice, porque los enlaces reales se rechazan en otra capa. Esa misma ablación se detecta en Windows. El total de cero supervivientes es por mutante distinto entre los dos entornos.

**Ataque original de AF5-M01, en Linux:** con el validador AF4, 58/0 (falso PASS histórico); con AF5, 50/9 y exit 1, con el objetivo intacto y modificado. El recuento difiere de los 55/4 del implementador porque el auditor usó otro builder; en ambos casos el validador falla.

## 4. Hallazgos

| ID | Severidad | Estado tras AF6 |
|---|---|---|
| AF5-M01 | MEDIUM | Cerrado técnicamente para el candidato auditado |
| AF5-L01 | LOW | Sus tres reproducciones originales están corregidas. **La clase no se declara completamente cerrada** |
| AF6-L01 | LOW | Nuevo, abierto y no bloqueante: composiciones con «relleno» |
| AF6-L02 | LOW | Nuevo, abierto y no bloqueante: homógrafo latino/armenio |
| AF6-I01 | INFO | Límites y falsos rechazos estructurales conocidos |

Totales de hallazgos nuevos: 0 BLOCKER, 0 HIGH, 0 MEDIUM, 2 LOW y 1 INFO. AF2, AF3 y AF4: sin reapertura material en las regresiones ejecutadas. AF6-L01 y AF6-L02 se registran en [deuda técnica AF6](F36SBX_Deuda_Tecnica_AF6.md).

**Veredicto técnico del auditor:** «F36-SBX AF5 APROBADO TÉCNICAMENTE PARA INTEGRACIÓN». El propio informe precisa que esa conclusión no autoriza F37-SBX, no supera el F36-SBX-GATE, no aprueba la G0 real ni ADR-005, y no constituye aprobación humana del equipo.

## 5. Limitaciones de la auditoría

- Es focal sobre AF5 y sus dependencias; no prueba la ausencia de defectos.
- No ejecutó la carrera de un escritor local concurrente, que queda fuera del modelo declarado.
- En Windows no se crearon enlaces simbólicos de archivo (sin privilegio); se probaron en WSL. No se simuló cada proveedor de puntos de reparse de Windows.
- Los nombres de sus sondeos son sintéticos y no autentican a nadie.

## 6. Qué no es esta auditoría

Su existencia **no satisface FG-02** ni ningún otro criterio EQUIPO. FG-02 exige un acto del equipo con un formato cerrado ([gate §8.2](F36SBX_Gate_Sucesor.md#82-fg-02--auditoría-independiente)):

- un registro `gate/evidencia/FG-02.json`;
- un informe `.md` **dentro de `gate/evidencia/`**, con las secciones «Alcance», «Hallazgos» y «Conclusión» y un único bloque canónico `f36sbx-audit-metadata` coherente con el registro;
- un `candidate_commit` igual al del estado del gate, que hoy es nulo.

El informe AF6 no tiene ese formato, vive fuera del repositorio y no lo ha registrado nadie. Cómo y si se usa para FG-02 es una decisión del equipo, que se analiza en la [matriz de preparación del gate](preparacion-gate/F36SBX_Matriz_Preparacion_Gate.md).

Tampoco es una autorización institucional externa ni una autorización para ejecutar capacidades experimentales.

## 7. Ubicación y trazabilidad de la evidencia

La evidencia completa de la auditoría **no se versiona** en el repositorio. Incluye clones, bundles Git, archivos tar con los bytes normativos, logs de cientos de kilobytes y rutas temporales. Copiarla introduciría artefactos voluminosos y referencias a un equipo concreto.

Se conserva fuera del repositorio, en el directorio de la sesión de auditoría del equipo que la ejecutó (`AF6-F36-SBX/`, en el almacenamiento local de Codex del integrante que la encargó). Su integridad se fija con estos hashes:

| Artefacto | SHA-256 |
|---|---|
| `Informe_AF6_F36-SBX_AF5.md` | `819d54eede8e93dc0c0a976ed1d3c7d38db2763a8c81d8b40c267f7f1c21783b` |
| `findings.json` | `aad7ada9bbc04904ca9a0b53070ff0f983cb8bdf5b68b1f07643e32510f9a0fa` |
| `SHA256SUMS.txt` (manifiesto de todos los artefactos) | `81e8e1d87127fad6a78697ab14eb91a26447d4ef2fce5a994b57a490662e3da6` |
| `metatest-summary.json` | `54639aeb0a855280a47f19bce2cd26c925ca829b0bbfbfe9c182618431b23763` |
| `integrity-comparison.json` | `77691446d95fa59b6426d6081337515c6f63e02f2d13105bf5020e9eebd11459` |
| `repro-AF6-L01/results.json` | `7f42e3ca99035fa4981d654068d85a25a74433e0a3bbb426326b8e63ecad930e` |
| `repro-AF6-L02/results.json` | `931dc4fb1f8e5c4f571d5e6bbe8c8412fa0202a87fdeac647c3c3130db9e428e` |

Las referencias estables en el repositorio son los SHA del candidato, de los merges y de las ejecuciones de CI de la sección 1. Si el equipo decide usar la auditoría para FG-02, conservar el directorio completo, o una copia con su manifiesto verificable, es condición previa (decisión D-04 de la matriz).
