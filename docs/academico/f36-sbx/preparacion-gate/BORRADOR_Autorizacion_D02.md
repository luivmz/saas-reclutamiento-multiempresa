# BORRADOR — NO FIRMADO — SIN AUTORIZACIÓN

## Autorización D-02: incremento sucesor B-01 del F36-SBX-GATE

> **BORRADOR — NO FIRMADO — SIN AUTORIZACIÓN.** Plantilla del 27/10/2026, en la rama `feature/f36-sbx-gate-transition-h`, para que el equipo decida si autoriza implementar el [sucesor B-01](F36SBX_Especificacion_Sucesor_B01.md). No contiene ninguna decisión, voto, firma ni fecha de aprobación. Mientras no exista una autorización auténtica, **no se modifica el validador ni el gobierno normativo**, F36-SBX-GATE = NO SUPERADO y F37-SBX = BLOQUEADA.

## 1. Quién puede autorizar

- **El contrato no fija un quórum para D-02.** El [gate §9](../F36SBX_Gate_Sucesor.md#9-vínculo-con-el-candidato-auditado) exige «un incremento sucesor auditado que actualice el gobierno y el validador».
- **La práctica del proyecto exige una autorización explícita del equipo** para los incrementos sucesores de gobierno: así ocurrió en el cierre de gobierno de F35-SBX-B. `CLAUDE.md` exige además autorización explícita del equipo para publicar o integrar.
- **El [charter](../F36SBX_Charter.md#1-qué-es-este-incremento) solo autoriza investigar, diseñar y los validadores documentales del paquete.** Un validador capaz de dar el gate por superado excede ese alcance.

**Propuesta, no requisito:** registrar D-02 con los tres integrantes, como los criterios FG-03, FG-10 y FG-12, porque habilita el mecanismo que después podría autorizar F37-SBX. El equipo decide la forma.

Una instrucción operativa de una sola persona no sustituye los votos de las demás. Tampoco una sesión automatizada puede emitir esta autorización.

**Actualización del 27/10/2026.** El solicitante declaró que el proyecto lo desarrolla una sola persona real. Si es así, la autorización de tres integrantes no puede obtenerse con autenticidad. La vía legítima para D-02 depende de la [propuesta de gobierno unipersonal](F36SBX_Propuesta_Gobierno_Unipersonal.md), que no está vigente, y de sus condiciones U-01 a U-04 (sección 6).

## 2. Qué se autorizaría

| Elemento | Alcance propuesto |
|---|---|
| Código | `docs/academico/tools/f36sbx/` (validador, baterías y metapruebas), solo según la especificación B-01 |
| Documentos del paquete | Los de `docs/academico/f36-sbx/`, incluida la sección del resultado canónico del gate |
| Gobierno | Solo las líneas canónicas de los espejos E4–E7 y la reescritura previa de los párrafos que duplican estados (D-07) |
| Decisiones de diseño | T-01 a T-07 de la especificación, cada una con su opción elegida |
| Deuda AF6 | Si se incluye la corrección de AF6-L01 y AF6-L02 en el mismo candidato (D-05) |

## 3. Qué no se autorizaría

- El inicio de F37-SBX, ni ninguna capacidad, dependencia, endpoint, migración o UI.
- El registro de evidencia de FG-02, FG-03, FG-10 o FG-12, que sigue siendo un acto posterior y separado.
- La aprobación de la G0 real, de ADR-005 o de un ADR sucesor.
- Datos reales, producción, el alcance C del producto, scoring, ranking, recomendación o selección automática.
- Cambios en el contrato de evidencia, en el esquema de evidencia de equipo o en F35-SBX, salvo una decisión explícita adicional.
- Publicar o integrar sin una autorización posterior.

## 4. Condiciones

1. RED antes de GREEN, con el [plan de pruebas](F36SBX_Plan_Pruebas_Sucesor_B01.md).
2. Ningún modo de excepción en el validador.
3. Commits ordinarios, sin reescribir historia.
4. Congelar el candidato H solo cuando no quede ningún cambio material previsto ([secuencia](F36SBX_Matriz_Preparacion_Gate.md#21-secuencia-hacia-el-candidato-h)).
5. Auditoría independiente de H antes de registrar cualquier evidencia.

## 5. Decisión y votos

| Campo | Valor |
|---|---|
| Decisión | NO EMITIDA |
| Opciones elegidas para T-01 a T-07 | NO EMITIDA |
| Inclusión de AF6-L01 y AF6-L02 (D-05) | NO EMITIDA |
| Inclusión de la sincronización del gobierno (D-07) | NO EMITIDA |
| Fecha | PENDIENTE |

| Integrante | Voto | Fecha | Canal de verificación |
|---|---|---|---|
| Coronacion Meza Fredy | PENDIENTE | PENDIENTE | PENDIENTE |
| Peña Arroyo Anthony | PENDIENTE | PENDIENTE | PENDIENTE |
| Vila Meza Luis Antonio | PENDIENTE | PENDIENTE | PENDIENTE |

Sin firmas. La autorización real se emite y se conserva por el procedimiento de la [lista de comprobación](BORRADOR_Checklist_Evidencias_y_Verificacion.md#22-votos-de-los-integrantes-fg-03-fg-10-y-fg-12), adaptado a esta decisión.

Esta tabla corresponde al contrato vigente. Si se adoptara el modelo unipersonal, la sustituiría un único registro de decisión del responsable ([propuesta, §5.3](F36SBX_Propuesta_Gobierno_Unipersonal.md#53-registro-de-decisión-del-responsable)), nunca tres votos emitidos por una sola persona.

## 6. Tres decisiones distintas y variantes por modelo de gobierno

D-02 agrupa tres decisiones que no se confunden ni se infieren unas de otras:

| Decisión | Qué autoriza | Con el contrato vigente | Con el modelo unipersonal, si se adopta | Estado |
|---|---|---|---|---|
| D-02a | Preparar y diseñar el sucesor | Dentro del alcance del charter (investigar y diseñar), solo como documentación. Así se hizo la [especificación](F36SBX_Especificacion_Sucesor_B01.md) y el [plan de pruebas](F36SBX_Plan_Pruebas_Sucesor_B01.md), sin tocar código | Igual | Realizada como documentación; no autoriza código |
| D-02b | Implementar el sucesor en el validador y en el gobierno | Autorización explícita del equipo: los tres integrantes declarados | Un registro de decisión del responsable, posterior a la adopción de la enmienda (U-04) y a una auditoría técnica independiente de la especificación | NO EMITIDA |
| D-02c | Iniciar F37-SBX | No es D-02: es FG-03, después de superar el gate aplicable con un candidato H auditado | Igual: FG-03 con un registro de decisión del responsable, tras una FG-02 favorable sobre H | NO EMITIDA. F37-SBX = BLOQUEADA |

Ninguna de las tres se puede retrofechar. Ninguna la emite una sesión de IA ni el validador.
