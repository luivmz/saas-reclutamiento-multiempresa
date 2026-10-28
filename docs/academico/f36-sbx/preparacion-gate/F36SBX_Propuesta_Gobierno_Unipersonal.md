# PROPUESTA — NO VIGENTE — PENDIENTE DE AUTORIZACIÓN

## F36-SBX — Propuesta de gobierno académico unipersonal

> **PROPUESTA — NO VIGENTE — PENDIENTE DE AUTORIZACIÓN.** Documento del 27/10/2026, en la rama `docs/f36-sbx-unipersonal-governance-proposal`, desde `1d5d6aa`. El solicitante pidió estudiar y preparar una adecuación transparente del gobierno de F36-SBX a un proyecto desarrollado por una sola persona.
>
> Esta propuesta **no modifica** el contrato vigente, el validador, el esquema de evidencia, el estado del gate ni ningún registro histórico. Mientras no la adopte legítimamente quien tiene autoridad para hacerlo (sección 3), rige el contrato vigente: F36-SBX-GATE = NO SUPERADO y F37-SBX = BLOQUEADA.

## 1. Hechos de partida

### 1.1 Declaración del solicitante

El 27/10/2026, el solicitante declaró dos hechos:

- el proyecto lo desarrolla **una sola persona real**;
- los tres dispositivos usados durante el desarrollo son **tres entornos de trabajo**, no tres integrantes humanos independientes.

Este documento registra esa declaración como suya. No la verifica, no la amplía y no la convierte en una decisión de gobierno.

### 1.2 Lo que consta en el repositorio

| Hecho | Dónde | Relevancia |
|---|---|---|
| **Tres integrantes declarados ante el curso:** Coronacion Meza Fredy, Peña Arroyo Anthony y Vila Meza Luis Antonio | `CLAUDE.md`, la tabla «Integrantes» del [informe final v1.0](../../../final-report/01-informacion-general.md), las prácticas F2 a F11 y el informe final F29H | Es una declaración académica ante la universidad. Ninguna enmienda interna la cambia |
| **El contrato de F36-SBX ata el quórum a esas tres identidades exactas** | Esquema `team_members` y `approvals.quorum = 3/3`, fijado por su SHA-256. En el validador: `MEMBERS` (`validate_f36sbx.py:81`), la línea `CLAUDE_MEMBERS` (`:82`), que la regla GOV exige en `CLAUDE.md`, `approval_errors()` (`:2367`) y `reviewed_by` de FG-10 (`:2566`). En el gate, la sección 8.1 | Es el requisito que entra en conflicto con el desarrollo unipersonal |
| **Evidencia histórica de aprobación del equipo:** cuatro capturas de mensajes de WhatsApp de un grupo, con remitentes visibles distintos, atribuidas a los tres integrantes. Respaldan G0-14 y G0-09 (aprobación interna del equipo, F34C) | [Acta de ADR-005, §5](../../g0-evidence/F34B_Acta_Aprobacion_ADR005.md#5-verificación-de-evidencias-f34c) | Congelada (`F35_FROZEN`). Su sentido depende de la lectura de la sección 1.3 |
| **Autoría Git** | Historial completo | `main` y F36-SBX tienen como autores las identidades del responsable (`luivmz`, `Luis Vila Meza` y `Luis Antonio Vila Meza`). Seis commits del 20/10/2026 figuran con la identidad «Coronacion Meza Fredy». Están en `origin/codex/mejoras-sonarqube`, una práctica de SonarQube no integrada en `main` ni en `develop`. Git declara la identidad, no la autentica |
| **Tres entornos de trabajo documentados** | El PC principal con Windows, donde está este repositorio; un [PC secundario](../../handoff/F35SBX_SECONDARY_PC_HANDOFF.md) y [macOS](../../handoff/F34E_MACOS_HANDOFF.md) | El repositorio usa «equipo» en dos sentidos, personas y computadoras («configuración local de cada equipo»). El contrato sucesor debe distinguir **integrante** de **entorno** |
| **Ninguna norma externa del curso** sobre la composición del equipo o el trabajo individual | Se buscó «trabajo grupal», «en equipo de», «tres integrantes», «trabajo individual», «sílabo» y «rúbrica» | El requisito 3/3 es una decisión interna del proyecto. Pero que el curso admita o no un trabajo individual es un hecho externo que el repositorio no puede establecer |

### 1.3 Dos lecturas de la declaración

| Lectura | Qué significa | Consecuencia |
|---|---|---|
| **(a)** | Los tres integrantes son personas reales del curso, pero solo una desarrolla; los tres «equipos» son computadoras | Los dos integrantes no activos siguen siendo parte del contrato vigente. Una enmienda que los aparte de las decisiones necesita su conformidad expresa, o una decisión del docente. La evidencia de F34C conserva su sentido |
| **(b)** | Solo existe una persona real | Dejarían de corresponder a la realidad las atribuciones históricas a otras dos personas: la declaración del equipo ante el curso, las capturas de F34C y la identidad Git de esos seis commits. Aclararlo exige una declaración transparente del responsable ante el docente. Ninguna enmienda interna lo sustituye ni lo corrige con efecto retroactivo |

Este documento **no elige** entre (a) y (b): es una declaración que corresponde al responsable (U-01, sección 10).

## 2. Diagnóstico: el 3/3 frente a un desarrollo unipersonal

| Elemento del contrato vigente | Con una sola persona real |
|---|---|
| FG-03, FG-10 y FG-12 en CUMPLE: tres votos `APRUEBA` de tres identidades exactas | **Imposible de cumplir con autenticidad.** Una persona que registrara los tres votos estaría fabricando evidencia, y el validador la aceptaría: comprueba estructura, no autentica personas |
| FG-10: revisor de la cadena de suministro, un integrante | Solo puede revisar el responsable |
| FG-02: auditor de tipo `integrante_no_autor` | Imposible: la única persona es la autora |
| FG-02 con `docente`, `revisor_academico_externo` o `sesion_de_auditoria_independiente` | Compatible |
| FG-12 en NO APLICA | Compatible: no lleva votos propios |
| Criterios AUTO, vínculo con el candidato y controles de AF2 a AF6 | Compatibles: no dependen de cuántas personas hay |

**Consecuencia.** Con el contrato vigente y una sola persona real, el gate original no puede superarse legítimamente nunca. Es el comportamiento correcto de un contrato que falla cerrado. La salida honesta es una enmienda legítima, no un 3/3 aparente.

## 3. Origen del requisito y autoridad para enmendarlo

| Pregunta | Respuesta | Fuente |
|---|---|---|
| ¿Quién definió el contrato vigente? | El paquete F36-SBX, abierto por una «instrucción del equipo del 26/10/2026» transcrita sin adjunto firmado ([charter §1](../F36SBX_Charter.md#1-qué-es-este-incremento)), en sesiones de trabajo con Claude Code. El 3/3 reproduce el patrón de aprobación interna de F34B y F34C | Charter, gate §8.1 y F34C |
| ¿Norma externa o decisión interna? | **Interna.** No hay en el repositorio ninguna norma del curso que la imponga. Sí está atada al equipo declarado ante el curso | Sección 1.2 |
| ¿Quién puede proponer una enmienda? | El responsable, o cualquier integrante. Proponer no es adoptar | — |
| ¿Quién puede aprobarla? | El contrato vigente exige, para cambiar el gobierno, un incremento sucesor auditado y explícitamente autorizado por el equipo, y el equipo son los tres integrantes declarados. En la lectura (a): los tres, por ejemplo delegando las decisiones en el responsable. En la lectura (b): el responsable no puede validar en solitario un cambio que redefine quién es el equipo declarado ante el curso; hace falta el reconocimiento del docente | Gate §9, práctica de F35-SBX-B y `CLAUDE.md` |
| ¿Puede el responsable adoptar solo un nuevo contrato académico? | Solo con efecto prospectivo y solo con la autoridad de la fila anterior. Sin ella, adoptarlo en solitario sería una autoaprobación que reescribe quién decide | — |
| ¿Exige la revisión de un docente u otra persona? | El repositorio no lo establece. Como la composición del equipo es un hecho académico, se recomienda el reconocimiento del docente en las dos lecturas, y en la (b) es imprescindible | Sección 1.3 |
| ¿Qué no puede cambiar ninguna enmienda? | Sección 9 | — |
| ¿Cómo se conserva el historial? | El contrato vigente sigue en el repositorio y en Git. El sucesor lleva una versión nueva (`gate_version` y esquema de evidencia nuevos). Los registros de F34C y AF1 a AF6 no se tocan: cualquier aclaración es un anexo, nunca una edición | — |
| ¿Cómo se evita una autoaprobación retroactiva? | Sección 8 | — |
| ¿Qué auditoría la acompaña? | Una auditoría técnica independiente de la propuesta antes de adoptarla, y otra del candidato H que la implemente (sección 7) | — |

## 4. Clasificación: B, enmienda condicionada

- **No es A** (una enmienda interna que el responsable pueda adoptar ya). Falta la autoridad: la conformidad de los otros dos integrantes en la lectura (a), o el reconocimiento del docente en la (b). En la lectura (b), además, hay que aclarar los registros históricos.
- **No es C** (una adaptación incompatible). El 3/3 no es un requisito externo inmodificable, y el propio contrato prevé un incremento sucesor auditado.
- **Es B.** Este incremento prepara el expediente ([borrador de consulta al docente](BORRADOR_Expediente_Adecuacion_Unipersonal.md)) y la propuesta. El contrato vigente sigue en vigor, el gate original sigue en NO SUPERADO y F37-SBX sigue BLOQUEADA.

La propuesta pasaría a ser adoptable si se cumplen U-01 a U-04 (sección 10). Hasta entonces no se adopta, ni en todo ni en parte.

## 5. Contrato sucesor propuesto

### 5.1 Roles

| Rol | Quién | Puede | No puede |
|---|---|---|---|
| Responsable humano | Una persona real, identificada por U-01 | Decidir dentro del alcance académico y sintético; aprobar o rechazar propuestas; conservar la evidencia de sus decisiones; declarar los límites de su independencia | Auditarse a sí mismo; decidir sobre la G0 real, ADR-005, datos reales o el alcance C del producto; registrarse como varios integrantes |
| Integrantes no activos (solo en la lectura a) | Las personas declaradas ante el curso que no desarrollan | Consentir o no la enmienda, por escrito y con su fecha | Ser sustituidos por otra persona o por un dispositivo |
| Entornos de trabajo E-1, E-2 y E-3 | El PC principal con Windows, un PC secundario y macOS. Su función real (desarrollo, pruebas o revisión) la declara el responsable; no se presume | Ejecutar desarrollo, pruebas y revisiones | Emitir votos o decisiones. La identidad Git de un entorno es la del responsable, nunca la de otra persona |
| Claude Code | La sesión de implementación | Diseñar, implementar, ejecutar pruebas y preparar borradores | Auditar su propio trabajo, emitir decisiones o autorizaciones, o registrar actos humanos |
| Codex | Sesiones de auditoría separadas | Ejecutar auditorías técnicas independientes y emitir informes técnicos con su procedencia | Votar o decidir; presentarse como docente, integrante o revisor humano. Su independencia es técnica, no humana ni institucional |
| Docente | Autoridad académica externa | Reconocer o autorizar la adecuación; revisar | — (sus permisos no se presumen) |

### 5.2 Principios

1. Una decisión humana se atribuye solo a quien la toma, con su fecha real.
2. Ningún dispositivo, identidad Git, sesión de IA ni validador emite decisiones.
3. La enmienda es **prospectiva**: no recalifica nada anterior a su adopción.
4. Antes de cada decisión del responsable sobre el gate hay una auditoría técnica independiente favorable del mismo candidato.
5. La independencia que se declara es la que existe: técnica, entre sesiones; no humana ni institucional.
6. El alcance es académico y sintético. El alcance C queda **fuera** del modelo unipersonal salvo revisión externa (sección 6, FG-12).
7. Ningún control de seguridad se relaja (sección 9).

### 5.3 Registro de decisión del responsable

Sustituye a la lista `approvals` 3/3 en los criterios que la tenían. Campos propuestos:

| Campo | Regla |
|---|---|
| `decision_id` | `F36SBX-RD-NNN` |
| `decided_by` | La identidad del responsable que fije U-01, exacta |
| `role` | `responsable_unico` |
| `decision` | Valor cerrado del criterio, por ejemplo `AUTORIZA_INICIO_F37_SBX` o `NO_AUTORIZA` |
| `candidate_commit` | H |
| `audit_report` | Ruta y SHA-256 del informe de FG-02 sobre H |
| `decided_on` | Fecha real, no anterior a la del informe de FG-02 ni a la adopción de la enmienda |
| `independence_statement` | Texto cerrado: «Decisión de una sola persona, sin independencia humana; precedida de una auditoría técnica por una sesión separada» |
| `external_acknowledgement` | Nulo, o la referencia al reconocimiento del docente |

El validador comprobaría la estructura, la coherencia y las fechas. La autenticidad la aportan controles externos al validador: un commit firmado por el responsable (opcional) y el reconocimiento del docente (recomendado). Nunca un 3/3 aparente.

## 6. Adaptación de FG-02, FG-03, FG-10 y FG-12

| Criterio | Contrato vigente | Propuesta unipersonal | Se conserva | No se permite |
|---|---|---|---|---|
| FG-02 | Auditor de cuatro tipos, sin quórum | Admisibles: `sesion_de_auditoria_independiente` (Codex, en una sesión separada y con procedencia verificada), `docente` y `revisor_academico_externo`. `integrante_no_autor` deja de aplicar: la única persona es la autora | Informe canónico sobre H; commit y árbol exactos; veredicto y hallazgos auténticos; 0 BLOCKER, 0 HIGH y 0 MEDIUM que exija corrección; LOW declarados tal cual | Presentar una sesión de IA como revisor humano o institucional; reutilizar una auditoría de AF5 o de documentación como auditoría de H |
| FG-03 | Tres votos | Un registro de decisión del responsable, posterior a una FG-02 favorable sobre H, con la lista cerrada de EI y la numeración F36-M01. Reconocimiento del docente, recomendado | Lista cerrada de EI ALLOWED o CONDITIONAL, igual a `f37_authorized_ei`; EI BLOCKED prohibidas; decisión humana explícita | Un 1/1 disfrazado de 3/3; una autorización emitida por el validador o por una sesión de IA |
| FG-10 | Tres votos y un integrante revisor | Registro de decisión del responsable; el revisor de la cadena de suministro es el responsable | Siempre registrado; versión exacta, licencia admitida, origen, OSV real y SHA-256 de artefactos reales | NO APLICA; suprimir OSV o hashes por ser un proyecto individual |
| FG-12 | NO APLICA, o tres votos y el ADR para alcance C | NO APLICA, igual. En CUMPLE, solo para EI-09 (alcance B), con registro de decisión del responsable. **El alcance C queda fuera del modelo unipersonal:** una EI CONDITIONAL de alcance C exige además una revisión externa documentada y su ADR aprobado dentro de H | ADR dentro de H; restricciones del alcance C | Aprobar un ADR de alcance C, ADR-005 o la G0 real por decisión unipersonal |

## 7. Procedimiento de auditoría técnica independiente

1. **Sesión separada.** La sesión que audita no es la que implementó ni la que preparó lo auditado.
2. **Identidad.** Examina un commit fijo (SHA y árbol) y lo declara en su informe.
3. **Método propio.** Usa builders y pruebas propias, sin importar las del implementador, además de las oficiales.
4. **Evidencia.** Conserva la evidencia completa con un manifiesto SHA-256. Si se versiona, solo un resumen con sus hashes (como el [registro AF6](../F36SBX_Auditoria_AF6.md)).
5. **Formato.** Para FG-02, emite el informe canónico del gate §8.6.
6. **Verificación humana.** El responsable comprueba la sesión, el manifiesto y el commit examinado, y registra.
7. **Límites que se declaran siempre.** Un mismo operador humano orquesta las dos sesiones. Las auditorías AF6 y la documental se ejecutaron en el mismo PC Windows, con su WSL, que la implementación. Que los proveedores sean distintos reduce los errores correlacionados, pero no los elimina. No hay independencia institucional.
8. **Refuerzos opcionales.** Auditar desde otro entorno (E-2 o E-3), sobre un clon limpio del commit; o pedir una revisión del docente.

## 8. Plan de migración hacia H

El orden es prospectivo; nada se adelanta:

1. **U-01.** Declaración del responsable sobre la composición real del equipo, lectura (a) o (b), con su fecha.
2. **U-02.** La autoridad que corresponda: en la lectura (a), la conformidad expresa de los otros dos integrantes; en la (b), el reconocimiento del docente, mediante el [expediente](BORRADOR_Expediente_Adecuacion_Unipersonal.md). Si el docente no lo reconoce, sigue rigiendo el contrato vigente.
3. **U-03.** Auditoría técnica independiente de esta propuesta.
4. **U-04.** Adopción formal de la enmienda por esa autoridad, con un registro de fecha real. Nada anterior a ella cambia de calificación.
5. **D-02,** ya bajo el modelo adoptado, separada en tres decisiones ([borrador](BORRADOR_Autorizacion_D02.md#6-tres-decisiones-distintas-y-variantes-por-modelo-de-gobierno)).
6. **Incremento de H:**
   - el contrato sucesor (`gate_version` y esquema nuevos, con el registro de decisión);
   - el validador B-01 adaptado al modelo;
   - sus pruebas;
   - la sincronización del gobierno, con `CLAUDE.md` declarando al responsable y la condición real de los integrantes;
   - la documentación del carácter unipersonal;
   - la deuda AF6 (D-05).
7. **Congelación de H,** auditoría independiente de H, registro de decisión de FG-03 y FG-10 (y de FG-12 si procede), registro y validación ([secuencia hacia H](F36SBX_Matriz_Preparacion_Gate.md#21-secuencia-hacia-el-candidato-h)).

**Historial.** La versión vigente del contrato y del esquema se conservan. Los registros de F34C, AF1 a AF6 y esta preparación no se reescriben. En la lectura (b), cualquier aclaración sobre las atribuciones históricas es un anexo fechado.

## 9. Riesgos y controles compensatorios

| Riesgo | Control |
|---|---|
| **Autoaprobación:** quien propone, decide | Autoridad de U-02, auditoría independiente previa a cada decisión, reconocimiento del docente y alcance limitado |
| **Retroactividad** | Fechas en orden: auditoría de la propuesta, adopción, informe de FG-02 y decisión. El validador sucesor las compara. Nada anterior a la adopción se recalifica |
| **Sobredeclarar la independencia de la IA** | Declaración de independencia con texto cerrado; los tipos de auditor humanos quedan reservados a personas |
| **Evidencia fabricada:** tres votos de una sola persona | El contrato sucesor elimina el 3/3 en lugar de simularlo. Con el contrato vigente, ningún registro de 3/3 es legítimo |
| **Reescritura de la historia** | Historial intacto; aclaraciones como anexos |
| **Ampliación al alcance C** | Excluido del modelo unipersonal sin revisión externa |
| **Confundir lo académico con lo institucional** | Una aprobación académica no es una autorización institucional: G0 real = NO APROBADA, y G0-02, G0-03 y G0-12 siguen PENDIENTE EXTERNO |
| **Un único operador orquesta implementación y auditoría** | Manifiestos, clones limpios, otro entorno si es posible y revisión del docente |
| **Autoconfianza del validador** | Como en la [especificación de B-01, §8](F36SBX_Especificacion_Sucesor_B01.md#8-riesgos-y-límites-que-el-diseño-no-elimina) |

**Controles que no desaparecen:**

- la identidad Git y el vínculo exacto del candidato;
- la congelación de los archivos normativos;
- la protección frente a enlaces, puntos de reparse y rutas externas;
- el rechazo de evidencia falsa o incompatible;
- los hashes;
- la auditoría técnica independiente y el registro de decisiones humanas auténticas;
- la validación de dependencias y los controles de EI;
- la coherencia de estados y la prohibición de cambios materiales después de H;
- la separación entre la aprobación académica y la autorización institucional.

Siguen vigentes, sin excepción:

- G0 real = NO APROBADA;
- G0-SBX = APROBADA CON RESTRICCIONES;
- F35-SBX = CERRADA Y CONGELADA, e integrada;
- F36-SBX-GATE = NO SUPERADO;
- F37-SBX = BLOQUEADA;
- ADR-005 = PROPUESTA;
- RF-23, decisión final humana;
- RF-29, experimental, sobre la demora del proceso.

Siguen prohibidos los datos reales, los CV reales, la PII real, el scoring de candidatos, las inferencias de personalidad y la activación productiva del alcance C.

## 10. Autorizaciones y declaraciones todavía necesarias

| ID | Qué | De quién | Estado |
|---|---|---|---|
| U-01 | Declaración de la composición real del equipo: lectura (a) o (b) | El responsable | PENDIENTE |
| U-02 | Autoridad para adoptar la enmienda: conformidad de los otros dos integrantes (a) o reconocimiento del docente (b) | Integrantes o docente | PENDIENTE |
| U-03 | Auditoría técnica independiente de esta propuesta | Una sesión de auditoría separada | PENDIENTE |
| U-04 | Adopción formal y prospectiva de la enmienda | La autoridad de U-02 | NO EMITIDA |
| U-05 | Aclaración de las atribuciones históricas, solo en la lectura (b) | El responsable, ante el docente | PENDIENTE |
| D-02 | Las tres decisiones del sucesor B-01, ya bajo el modelo adoptado | La autoridad del modelo vigente en ese momento | NO EMITIDA |

Las decisiones D-01 a D-08 y T-01 a T-07 siguen en la [matriz de preparación](F36SBX_Matriz_Preparacion_Gate.md#7-decisiones-que-requieren-intervención-humana) y en la [especificación de B-01](F36SBX_Especificacion_Sucesor_B01.md#9-decisiones-de-diseño-pendientes-del-equipo).

## 11. Lo que esta propuesta no hace

- No adopta la enmienda ni la declara aprobada.
- No modifica el contrato vigente, el validador ni el estado del gate.
- No implementa B-01, no congela H y no inicia F37-SBX.
- No crea votos, firmas, decisiones ni identidades.
- No afirma requisitos del curso ni permisos del docente.
- No reinterpreta la evidencia histórica.
