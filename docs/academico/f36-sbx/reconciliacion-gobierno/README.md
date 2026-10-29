# F36-SBX — Reconciliación de gobierno y propuesta Q2

> **PROPUESTA DOCUMENTAL — NO VIGENTE — SIN ADOPCIÓN FORMAL.** Paquete del 29/10/2026, en la rama `docs/f36-sbx-team-governance-proposal`, creada desde `develop` = `9dd76c4ce69e6686eaae22d9eb3eceb1e347caf9` (árbol `82f27c9daf4305cafce6fb23a3b7b9277906b783`). No está publicado ni integrado. Es candidato a una auditoría técnica independiente (E-04).
>
> Estados vigentes, sin cambios: G0 real = NO APROBADA; G0-SBX = APROBADA CON RESTRICCIONES; ADR-005 = PROPUESTA; F35-SBX = CERRADA Y CONGELADA; F36-SBX = EN DISEÑO; F36-SBX-GATE = NO SUPERADO; F37-SBX = BLOQUEADA; alcance C = BLOQUEADO; datos reales = PROHIBIDOS.

## Contenido

| Documento | Qué contiene | Naturaleza |
|---|---|---|
| [Reconciliación de referencias, estados y controles](F36SBX_Reconciliacion_Estado_Gobierno.md) | AF5, AF6, H y Q con sus hashes completos; el estado real de Q, H, B-01 y los gates, medido con el validador; la matriz de observaciones; el origen de cada control; las actividades permitidas y bloqueadas; la deuda documental; las decisiones y evidencias pendientes | Hechos comprobados [H] y afirmaciones recibidas [R] |
| [Propuesta Q2, sucesora de Q](PROPUESTA_Q2_Gobierno_Equipo.md) | El gobierno de tres integrantes académicos con Luis como responsable técnico: roles, niveles de decisión, revisión diferenciada, registros, adopción, transición y deltas propuestos | Propuesta [P] |
| [Roadmap propuesto F36–F40](F36SBX_Roadmap_Propuesto_F36_F40.md) | ML-01 (RF-29), ML-02 (inteligencia sobre evidencia) y la línea visual, con las condiciones para entrenar, experimentar e integrar cada uno | Propuesta [P] sobre hechos [H] |

## Lo que este paquete no hace

- **No adopta Q2,** no cambia ningún estado formal y no declara cumplido ningún contrato anterior.
- **No modifica** `AGENTS.md`, `CLAUDE.md`, las skills, el contrato ni el esquema de evidencia, el validador, el estado del gate, la evidencia congelada de F35-SBX, `defects.md` ni `assumptions.md`.
- **No integra AF6, H ni Q.** Los cita por commit y ruta, como `061ba68:docs/…`.
- **No crea votos, firmas, delegaciones ni aprobaciones.** Las plantillas de Q2 siguen en PENDIENTE.
- **Conserva a los tres integrantes declarados ante el curso:** Coronacion Meza Fredy, Peña Arroyo Anthony y Vila Meza Luis Antonio. No atribuye a Fredy ni a Anthony contribuciones, firmas ni aprobaciones técnicas.

## Validación de este paquete

Ejecutada el 29/10/2026 sobre esta rama:

| Comprobación | Resultado |
|---|---|
| Funciones de prosa del propio validador (`forbidden_claims`, `state_claims` con `allowed_states`, `invisible_chars`) y NFC, aplicadas a los cuatro documentos | 0 problemas. Estos documentos no están en `PKG_DOCS`, así que las reglas SEM y LNK del validador no los leen; por eso se comprobaron aparte |
| Enlaces relativos | 42, ninguno roto |
| Hashes citados | 38 tokens: 30 commits y 7 árboles que resuelven en Git. El restante es el prefijo del SHA-256 del *freeze* de RF-29, que no es un objeto Git y figura completo en `CLAUDE.md` |
| [`validate_f36sbx.py`](../../tools/f36sbx/validate_f36sbx.py) sobre esta rama | 55 correctas y 4 fallas. Una es el anclaje por diseño: FRZ no admite la rama. Las otras tres son las de `develop`: FRZ por los 18 archivos de SEG, con la misma lista, y GATE por FG-01 y FG-05. Este paquete no añade ninguna falla, porque sus archivos caen dentro del paquete |
| Alcance del diff frente a `develop` | Solo estos cuatro archivos nuevos; `git diff --check`, sin errores |
| Pruebas funcionales | No se ejecutaron: el incremento es solo documental y no cambia código |

## Siguiente paso

1. **E-04.** Una sesión de Codex separada audita esta rama, sobre su commit exacto.
2. **E-01.** Si existe, se recupera el informe completo de la auditoría de Q, para contrastar sus 9 hallazgos.
3. **E-02 y E-03.** Los actos humanos de Luis, Fredy y Anthony, solo si deciden emitirlos, cada uno por sí mismo.

Integrar o publicar este paquete necesita una autorización explícita (contrato 10).
