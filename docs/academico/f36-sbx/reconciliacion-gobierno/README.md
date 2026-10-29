# F36-SBX — Reconciliación de gobierno y propuesta Q2

> **PROPUESTA DOCUMENTAL — NO VIGENTE — SIN ADOPCIÓN FORMAL.** Paquete del 29/10/2026, en la rama `docs/f36-sbx-team-governance-proposal`, creada desde `develop` = `9dd76c4ce69e6686eaae22d9eb3eceb1e347caf9` (árbol `82f27c9daf4305cafce6fb23a3b7b9277906b783`). No está publicado ni integrado.
>
> **Candidato corregido.** La revisión diferenciada de Codex sobre `729babb4a5584a4bc119fe61e59c101147e7acd5` pidió correcciones: 5 MEDIUM y 2 LOW. Este candidato las implementa en commits nuevos sobre aquel, sin reescribirlo, y queda pendiente de una revisión nueva.
>
> Estados vigentes, sin cambios: G0 real = NO APROBADA; G0-SBX = APROBADA CON RESTRICCIONES; ADR-005 = PROPUESTA; F35-SBX = CERRADA Y CONGELADA; F36-SBX = EN DISEÑO; F36-SBX-GATE = NO SUPERADO; F37-SBX = BLOQUEADA; alcance C = BLOQUEADO; datos reales = PROHIBIDOS.

## Contenido

| Documento | Qué contiene | Naturaleza |
|---|---|---|
| [Reconciliación de referencias, estados y controles](F36SBX_Reconciliacion_Estado_Gobierno.md) | AF5, AF6, H y Q con sus hashes completos; el estado real de Q, H, B-01 y los gates, medido con el validador; D-10 y D-11; las observaciones; el origen de cada control; las actividades permitidas y bloqueadas con su fuente vigente; la deuda documental; las decisiones y evidencias pendientes | Hechos comprobados [H] y afirmaciones recibidas [R] |
| [Propuesta Q2, sucesora de Q](PROPUESTA_Q2_Gobierno_Equipo.md) | El gobierno de tres integrantes académicos con Luis como responsable técnico: roles, niveles propuestos, revisión diferenciada, registros, adopción de una versión fijada, transición y deltas propuestos | Propuesta [P] |
| [Roadmap propuesto F36–F40](F36SBX_Roadmap_Propuesto_F36_F40.md) | ML-01 (RF-29), ML-02 (inteligencia sobre evidencia) y la línea visual, con las condiciones para reconstruir, entrenar, experimentar e integrar | Propuesta [P] sobre hechos [H] |
| [Respuesta a la auditoría de Q2](F36SBX_Respuesta_Auditoria_Q2.md) | La matriz de Q2-M01 a Q2-L02, la correspondencia de los nueve hallazgos de Q, los escenarios de adopción y las cifras corregidas | Hechos [H] y propuesta [P] |

## Historia del paquete

| Commit | Contenido |
|---|---|
| `d32873be0d226f0409db117c114e038a713f69af` | Reconciliación |
| `3bae9a7c8c5a78469e8257591e46af49039d1466` | Propuesta Q2 |
| `729babb4a5584a4bc119fe61e59c101147e7acd5` | Roadmap y README. Es el candidato auditado, con CORRECCIONES REQUERIDAS |
| `af843eb77b6df5584125e7ab59388205006d7c6d` | Correcciones de la reconciliación |
| `6544f849307b4803d1190f92eea1dec4c2b035dc` | Correcciones de Q2 |
| `695c39076d453152d385734633c259d12cc85cec` | Correcciones del roadmap |
| El commit de esta versión del README | Respuesta a la auditoría y validación; su hash se consulta en Git |

## Lo que este paquete no hace

- **No adopta Q2,** no emite conformidades ni delegaciones, no cambia ningún estado formal y no declara cumplido ningún contrato anterior.
- **No modifica** `AGENTS.md`, `CLAUDE.md`, las skills, el contrato ni el esquema de evidencia, el validador, el estado del gate, la evidencia congelada de F35-SBX, `defects.md` ni `assumptions.md`.
- **No implementa B-01,** no registra ninguna revocación ni autorización nueva y no revierte SEG.
- **No integra AF6, H ni Q.** Los cita por commit y ruta, como `061ba68:docs/…`.
- **No crea votos, firmas, delegaciones ni aprobaciones.** Las plantillas de Q2 siguen en PENDIENTE.
- **Conserva a los tres integrantes declarados ante el curso:** Coronacion Meza Fredy, Peña Arroyo Anthony y Vila Meza Luis Antonio. No atribuye a Fredy ni a Anthony contribuciones, firmas ni aprobaciones técnicas.

## Validación del candidato corregido

Ejecutada el 29/10/2026 sobre esta rama:

| Comprobación | Resultado |
|---|---|
| Funciones de prosa del propio validador (`forbidden_claims`, `state_claims` con `allowed_states` e `invisible_chars`) y NFC, en los cinco documentos | 0 problemas. Estos documentos no están en `PKG_DOCS`, así que las reglas SEM y LNK del validador no los leen; por eso se comprobaron aparte |
| Enlaces relativos y anclas | 46 enlaces y 2 anclas, ninguno roto |
| Hashes Git citados | 54 tokens hexadecimales: 42 commits y 8 árboles que resuelven en Git. Los 4 restantes no son objetos Git: dos segmentos del UUID de la carpeta de Codex y dos prefijos de SHA-256, el del *freeze* de RF-29 y el del informe de Q |
| [`validate_f36sbx.py`](../../tools/f36sbx/validate_f36sbx.py) sobre esta rama, sin cambiar su nombre, su base ni sus reglas | 55 correctas y 4 fallas, con el mismo patrón en las 59 comprobaciones que Q2 original: «FRZ — rama admitida», por el anclaje de rama; las dos de contenido de FRZ, por las 18 rutas externas y las 11 entradas de runtime de SEG, idénticas a las de `develop`; y GATE, por FG-01 y FG-05. No se agregan rutas externas ni fallas de contenido nuevas |
| Resultados de referencia | AF5 59/0; Q 57/2; `develop` 56/3; Q2 original (`729babb`) 55/4 ([reconciliación §3.1](F36SBX_Reconciliacion_Estado_Gobierno.md#31-mediciones-del-validador-h)) |
| Alcance del diff frente a `729babb` | 5 archivos: los 4 corregidos y la respuesta a la auditoría, que es nueva; 456 inserciones y 168 eliminaciones. Nada fuera de esta carpeta |
| Alcance del diff frente a `develop` | 5 archivos nuevos en esta carpeta, con 890 inserciones; `git diff --check`, sin errores |
| Pruebas funcionales | No se ejecutaron: el incremento es solo documental y no cambia código |

## Siguiente paso

1. **Revisión.** Una revisión diferenciada nueva de Codex, sobre el commit exacto de este candidato.
2. **Actos humanos.** Solo si los integrantes deciden emitirlos, y después de una revisión favorable: R-01, las conformidades y las delegaciones, cada uno por su titular y sobre una misma versión fijada (Q2 §9).
3. **Integración.** Integrar o publicar este paquete necesita una autorización explícita (contrato 10).
