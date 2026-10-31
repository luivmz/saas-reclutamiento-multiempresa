# BORRADOR — SIN EMISIÓN — SIN ADOPCIÓN

## R-01 — Declaración del responsable técnico: composición, roles, entornos y uso de IA

> **BORRADOR — SIN EMISIÓN — SIN ADOPCIÓN.** Preparado el 31/10/2026 por Claude Code a partir de los hechos ya comunicados o registrados. Solo Luis Vila Meza puede completarlo, fecharlo y emitirlo, con su propio acto ([Q2 §9.2 y §13](../reconciliacion-gobierno/PROPUESTA_Q2_Gobierno_Equipo.md)). No propone causas, explicaciones ni fechas que Luis no haya dado.

## 1. Para qué sirve

R-01 es la declaración de Luis sobre la composición y los roles reales del equipo. Es uno de los actos que citaría el registro raíz de adopción (RR). Aclara también la discrepancia entre la declaración del 27/10/2026 y las del 28 y 29/10/2026, que la [reconciliación](../reconciliacion-gobierno/F36SBX_Reconciliacion_Estado_Gobierno.md) deja pendiente (§5.4 y E-02 de su §8).

No es una conformidad con Q2 (esa es CM-01) ni una delegación.

## 2. Hechos ya comunicados o registrados

[H] hecho comprobado en el repositorio; [R] declaración recibida.

| N.º | Hecho | Naturaleza y fuente |
|---|---|---|
| 1 | El equipo declarado ante el curso es Coronacion Meza Fredy, Peña Arroyo Anthony y Vila Meza Luis Antonio | [H] Informe final v1.0, prácticas F2 a F11 y F29H; reconciliación §5.1 |
| 2 | El 28/10/2026 y el 29/10/2026 se declaró que el equipo tiene tres integrantes reales, Luis Vila Meza, Fredy Coronacion y Anthony Peña, y que Luis es el único desarrollador técnico y toma las decisiones ordinarias de programación | [R] Peticiones de SEG-01, SEG-02 y del incremento de Q2; Q2 §1 |
| 3 | El 31/10/2026, el encargo de este paquete repite que el equipo académico sigue teniendo tres integrantes y que Luis es el único desarrollador técnico | [R] Encargo de este paquete |
| 4 | El 27/10/2026 se declaró que el proyecto lo desarrolla una sola persona real y que los tres dispositivos son tres entornos de trabajo, no tres integrantes humanos independientes. La auditoría de Q registra que su encargo presentaba a Fredy Coronacion y a Anthony Peña como identificadores de entornos | [R] Q §1.1 (`061ba68`) e informe de la auditoría de Q (UNI-M01) |
| 5 | El repositorio documenta tres entornos de trabajo: el PC principal con Windows, donde está el repositorio y donde también se ejecutaron las auditorías, con su WSL; un PC secundario; y macOS. Los dos últimos tienen su guía de continuidad | [H] Q §1.2 (`061ba68`); [guía del PC secundario](../../handoff/F35SBX_SECONDARY_PC_HANDOFF.md); [guía de macOS](../../handoff/F34E_MACOS_HANDOFF.md); Q2 §5 |
| 6 | La función real de cada entorno, y quién lo usa, no se presumen: las declara el responsable | [H] Q §5.1, tabla de roles (`061ba68`) |
| 7 | Uso de IA: Claude Code implementa, Codex revisa de forma diferenciada y ChatGPT coordina. Un mismo operador humano orquesta las sesiones. Los commits llevan líneas `Co-Authored-By`. Ninguna revisión de IA es una aprobación humana | [R] y [H] Q2 §3 y §5 |
| 8 | En el repositorio no hay ninguna norma del curso sobre el uso de IA, el reparto de la contribución técnica ni la autorización docente de commits. Que no se encontraran no prueba que no existan | [H] Q2 §2; reconciliación §5.1.1 |
| 9 | Seis commits del 20/10/2026 figuran con la identidad Git «Coronacion Meza Fredy», solo en `origin/codex/mejoras-sonarqube`. Git declara la identidad, no la autentica | [H] Q2 §2; reconciliación §7 y E-05 de su §8 |

## 3. Declaración que completa Luis

| Campo | Valor |
|---|---|
| Composición real del equipo | ☐ Confirmo los hechos 1 a 3: tres integrantes reales, Luis Vila Meza, Fredy Coronacion y Anthony Peña. ☐ Declaro otra composición: PENDIENTE |
| Aclaración de la discrepancia con la declaración del 27/10/2026 (hecho 4) | PENDIENTE. La escribe Luis con sus palabras: qué describía aquella declaración y por qué difiere de las del 28 y 29/10/2026. Este borrador no propone ninguna causa |
| Rol de Luis Vila Meza | ☐ Confirmo: responsable técnico y único desarrollador técnico, que toma las decisiones ordinarias de programación. ☐ Corrijo: PENDIENTE |
| Rol de Fredy Coronacion y de Anthony Peña | Integrantes académicos. Su participación no técnica en el proyecto, si Luis la describe: PENDIENTE. No se les atribuyen contribuciones técnicas, firmas ni aprobaciones; cada uno puede confirmar o corregir lo que le concierne con su propio acto |
| Uso de los entornos de trabajo (hechos 5 y 6) | PENDIENTE. Quién usa cada entorno (PC principal, PC secundario y macOS) y para qué |
| Uso de IA (hecho 7) | ☐ Confirmo. ☐ Corrijo o completo: PENDIENTE. Cómo se declara la IA en los entregables académicos es una decisión del equipo (N4, Q2 §5) y no se decide aquí |
| Commits con la identidad «Coronacion Meza Fredy» (hecho 9), opcional | PENDIENTE. Luis puede declarar lo que le conste. La autoría no se reatribuye sin la declaración de las personas implicadas (Q2 §11) |
| Fecha | PENDIENTE |
| Canal | PENDIENTE |
| Evidencia y su SHA-256 | PENDIENTE. Se calcula sobre el archivo emitido, tal como se conserve |

## 4. Lo que R-01 no hace

- No es una conformidad con Q2 ni una delegación.
- No cambia ni reinterpreta los registros históricos. Las declaraciones del 27/10/2026, Q, las auditorías y las evidencias de F34C se conservan tal como constan (Q2 §11).
- No autentica a nadie: ni una identidad Git ni un hash prueban quién emitió algo.
- No atribuye contribuciones, firmas ni aprobaciones a Fredy ni a Anthony.
