# BORRADOR — SIN EMISIÓN — SIN ADOPCIÓN

## Q2 en pocas palabras: qué se decide y qué no

> **BORRADOR — SIN EMISIÓN — SIN ADOPCIÓN.** Explicación del 31/10/2026 para Luis Vila Meza, Fredy Coronacion y Anthony Peña. Leerla no compromete a nada: solo explica qué puede decidir cada uno, si quiere responder.

## 1. Qué es Q2

Q2 es una propuesta de reglas internas para el proyecto: quién decide cada cosa y cómo se deja constancia. **Hoy no está vigente.** Mientras nadie la adopte, siguen las reglas actuales del repositorio.

Lo que se decide es si se adopta Q2 **exactamente en esta versión**, que llamamos V:

| Dato | Valor |
|---|---|
| Commit | `8b1f068b5ac2039139ab5756096c147c11c9fcb2` |
| Árbol | `b5b81718680762f9585e4dae969ca44e69114865` |
| Documento | [`PROPUESTA_Q2_Gobierno_Equipo.md`](../reconciliacion-gobierno/PROPUESTA_Q2_Gobierno_Equipo.md) |
| SHA-256 del documento | `8829a0380bf7ea118b24d70c070de791bdf8efe4615a8f6a70372d403c0e71d0` |
| Revisión técnica | Favorable, hecha el 31/10/2026 por una sesión de Codex separada. Es una revisión, no una aprobación humana |

V fija también los otros cuatro documentos de su carpeta: la reconciliación, el roadmap, la respuesta a la auditoría y su README. Aportan hechos y contexto. Estar conforme con Q2 no adopta el roadmap, que es otra propuesta, ni decide D-10 o D-11.

Para leer el documento completo y comprobar que tu copia es la correcta, sigue el [README de esta carpeta](README.md#cómo-consultar-q2-completa).

## 2. Lo que no cambia

- **El equipo sigue teniendo tres integrantes:** Luis Vila Meza, Fredy Coronacion y Anthony Peña, los declarados ante el curso. Las guías oficiales piden equipos de tres estudiantes, y Q2 los mantiene.
- **Luis es el único desarrollador técnico.** Programa y toma las decisiones técnicas ordinarias.
- **Nadie recibe contribuciones ni firmas ficticias.** Q2 no atribuye a Fredy ni a Anthony trabajo técnico, firmas ni aprobaciones que no hayan hecho. Ninguna herramienta de IA cuenta como persona ni como voto.
- **Lo ya registrado no cambia.** Las aprobaciones de ADR-005 y del modelo de amenazas que se registraron en F34C siguen siendo lo que fueron: no cuentan como conformidad con Q2.

## 3. Dos decisiones distintas

| | Conformidad con el modelo (CM) | Delegación (DF) |
|---|---|---|
| Qué es | Decir si aceptas Q2 entera, tal como está en V | Permitir que Luis haga en nombre del equipo algunas operaciones concretas que hoy necesitan una autorización del equipo |
| Quién la emite | Los tres: Luis (CM-01), Fredy (CM-02) y Anthony (CM-03) | Solo Fredy (DF-02) y Anthony (DF-03) |
| ¿Hace falta? | Para adoptar Q2 hacen falta las tres | No. Es opcional y puede ser total, parcial o nula |
| Opciones | Conforme, conforme con condiciones o no conforme | Una lista cerrada que eliges tú, con sus límites y sus fechas |

**Aprobar el modelo no obliga a delegar.** Puedes estar conforme con Q2 y no delegar nada. En ese caso Q2 se puede adoptar igual, pero las operaciones que hoy necesitan al equipo lo siguen necesitando.

**Solo pasa a Luis lo que deleguen los dos.** Si Fredy delega unas facultades y Anthony otras, Luis solo recibe las que aparecen en las dos delegaciones, con los límites de ambas y mientras las dos estén vigentes.

## 4. Qué pasa según las respuestas

| Si… | Resultado |
|---|---|
| Los tres están conformes con V | Q2 se puede registrar como adoptada |
| Alguien está conforme con condiciones | Solo cuenta si se demuestra que las condiciones se cumplieron. Si una condición exige cambiar V, hace falta una versión nueva, su revisión y respuestas nuevas de los tres |
| Alguien está conforme solo con una parte | No se adopta: el modelo se adopta entero |
| Alguien no está conforme | No se adopta y siguen las reglas actuales |
| Alguien no responde | No se adopta. El silencio no cuenta como conformidad, y ningún plazo lo convierte en un sí |
| Alguien responde sobre otra versión | Esa respuesta no cuenta para V |

## 5. Lo que Q2 no da a nadie

Ni la adopción ni una delegación conceden por sí solas:

- **ML:** ningún permiso nuevo. Los cambios de ML siguen sujetos a sus reglas propias (el contrato congelado de RF-29 y la skill `ml-risk-service`) y, con Q2, además a una auditoría técnica previa;
- **datos reales:** siguen prohibidos;
- **producción:** nada pasa a producción;
- **gates:** ninguno se da por superado, y F37-SBX sigue bloqueada;
- **ADR y alcance C:** aprobar un ADR o decidir algo del alcance C no se puede delegar;
- **validaciones externas** (jurídicas, de privacidad o institucionales): no dependen del equipo.

## 6. Cómo responder, si decides hacerlo

1. Lee Q2 en la versión V, o pídele a Luis la copia y comprueba su SHA-256.
2. Usa tu borrador de conformidad y, si quieres, el de delegación. Eliges tú: nadie marca nada por ti.
3. Envía tu respuesta desde tu propio canal (tu cuenta), con la fecha. Escríbela tú: un mensaje de otra persona en tu nombre no vale.
4. Luis conserva tu respuesta original tal como llega, sin editarla.

No hay plazo. Puedes preguntar antes de responder, o no responder. No responder no es conformidad.

## 7. Preguntas frecuentes

- **¿Puedo estar conforme y no delegar?** Sí.
- **¿Puedo delegar sin estar conforme?** Puedes emitir la delegación, pero solo tendría efecto si Q2 se adopta, y la adopción necesita tu conformidad.
- **¿Puedo retirar una delegación?** Sí, cuando quieras y hacia adelante, con otro mensaje tuyo. Lo que Luis hizo antes con ella sigue siendo válido.
- **¿Y si cambio de opinión sobre mi conformidad antes del registro?** Q2 no lo regula expresamente. Si te ocurre, comunícalo por el mismo canal: se conservará como un acto tuyo más.
- **¿Hay que consultar al docente?** No hace falta. Es opcional.
- **¿Para qué sirve todo esto?** Para dejar escrito quién decide cada cosa y con qué constancia. Hoy, por ejemplo, publicar o integrar en GitHub necesita una autorización explícita del equipo, pero no está escrito cómo se da. Con Q2 y delegaciones, Luis podría hacerlo en nombre del equipo dentro de lo delegado. Sin delegaciones, seguiría haciendo falta el equipo.
