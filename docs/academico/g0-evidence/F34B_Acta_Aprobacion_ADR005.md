# F34B — Acta de aprobación de ADR-005 (G0-14)

> Fase F34B, versión 1 (04/10/2026); **actualizada en F34C** con evidencia real y corregida tras la auditoría F34C. Acta para que el equipo registre su decisión sobre [ADR-005](../diseno-inteligente/F33_ADR_005_G0.md), con el [paquete de aprobación de F34A](../g0-readiness/F34A_Paquete_Aprobacion_ADR005.md) como base.
>
> - **Estado canónico: ADR-005 = PROPUESTA.** El texto de ADR-005 en F33 no cambia.
> - **APROBACIÓN INTERNA DEL EQUIPO REGISTRADA** (F34C): los tres integrantes registraron `APRUEBA` con evidencia verificada (§5). Satisface G0-14.

> **Alcance de la aprobación interna.** Es la decisión **del equipo** sobre la dirección del motor. **No es una aprobación jurídica, de privacidad ni institucional**, no aprueba G0 y no desbloquea F35–F40.

## 1. Qué se decide

Si el equipo aprueba la **alternativa B** de ADR-005 (reglas, rúbricas y procedencia; nivel asignado siempre por una persona; decisión final humana), con E mantenida, C como futura, D rechazada y A como estado por defecto. Aprobar ADR-005 cierra **solo G0-14**; no aprueba G0.

## 2. Valores admitidos

- **Decisión:** `PENDIENTE`, `APRUEBA`, `APRUEBA CON OBSERVACIONES`, `RECHAZA`.
- **Estado:** `PENDIENTE` (sin evidencia) o `REGISTRADO` (con evidencia adjunta en [`adjuntos/`](adjuntos/README.md)).
- **Rol:** `Integrante del equipo` (exactamente tres filas) o `Docente del curso (consultivo, opcional)` (como máximo una).
- **Identidad:** cada fila de integrante lleva el **nombre completo** de una persona distinta de la lista de integrantes del proyecto (`CLAUDE.md`), y cada integrante aparece **exactamente una vez**. La fila del docente es de otra persona y **no sustituye** a ningún integrante.

## 3. Registro

| Responsable | Rol | Fecha | Decisión | Evidencia adjunta/referencia | Observaciones | Estado |
|---|---|---|---|---|---|---|
| Coronacion Meza Fredy | Integrante del equipo | 2026-10-04 | APRUEBA | [captura](adjuntos/G0-ADR005-ThreatModel_Fredy_Coronacion_2026-10-04.png) | Integrante: «Ninguna». Verificación: §5 | REGISTRADO |
| Peña Arroyo Anthony | Integrante del equipo | 2026-10-04 | APRUEBA | [captura](adjuntos/G0-ADR005-ThreatModel_Anthony_Pena_2026-10-04.png) | Integrante: «Ninguna». Verificación: §5 | REGISTRADO |
| Vila Meza Luis Antonio | Integrante del equipo | 2026-10-04 | APRUEBA | [original](adjuntos/G0-ADR005-ThreatModel_Luis_Vila_2026-10-04_original.png) · [confirmación](adjuntos/G0-ADR005-ThreatModel_Luis_Vila_2026-10-04.png) | Integrante: «Ninguna». OBS-F34C-01 RESUELTA por la confirmación; OBS-F34C-06 | REGISTRADO |
| — | Docente del curso (consultivo, opcional) | — | PENDIENTE | — | — | PENDIENTE |

## 4. Regla de resultado

- **Aprobación del equipo:** las tres filas de integrantes en `APRUEBA` o `APRUEBA CON OBSERVACIONES`, cada una con fecha, estado `REGISTRADO` y un adjunto existente y válido. La fila del docente es consultiva y no cuenta para el quórum.
- **Rechazo:** cualquier integrante en `RECHAZA` con evidencia; el proyecto vuelve a la alternativa A.
- **En cualquier otro caso:** no hay aprobación interna y G0-14 sigue PENDIENTE EXTERNO.
- La aprobación interna del equipo se registra aquí y en gobierno; **no cambia el estado canónico de ADR-005**, que sigue PROPUESTA, ni el texto del ADR.

**Resultado F34C:** se cumple la regla de aprobación del equipo (tres integrantes distintos, `APRUEBA`, fecha concordante y evidencia válida). La fila consultiva del docente sigue PENDIENTE.

## 5. Verificación de evidencias (F34C)

Cada adjunto es una captura de un mensaje de WhatsApp aportada por el equipo. Las capturas «Única» y «Original (histórica)» dicen: «He revisado la propuesta ADR-005 y el modelo de amenazas del proyecto "SaaS Reclutamiento Colegio Andino". ADR-005: [APROBADA]. Modelo de amenazas: [ACEPTADO]. Observaciones: ["Ninguna"]. Nombre: … Fecha: 04/10/2026. Confirmación: Declaro que esta decisión corresponde a mi revisión real de los documentos indicados.» La «Confirmación adicional» de Luis Vila dice: «Confirmo que revisé la propuesta ADR-005 y el modelo de amenazas… ADR-005: APROBADA. Modelo de amenazas: ACEPTADO. Confirmo que estas decisiones corresponden a mi revisión real. La fecha correcta de esta confirmación es: 04/10/2026. Nombre: Luis Antonio Vila Meza.», enviado a las 8:12 PM.

**Método:** revisión visual de cada imagen, formato real por su firma de archivo y registro del SHA-256. Sin OCR. `validate_f34b.py` recalcula SHA-256 y formato en cada ejecución.

| Adjunto | Tipo | SHA-256 | Formato | Remitente visible | Nombre declarado | Integrante | ADR-005 | Modelo de amenazas | Fecha declarada | Confirmación | Control temporal | Observaciones |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Fredy_Coronacion](adjuntos/G0-ADR005-ThreatModel_Fredy_Coronacion_2026-10-04.png) | Única | `9c95bf66797f3a170ba6a859624a7119c6c6de5270c4a398e965f66bb9d6bce9` | JPEG | Fredy Sistemas | Freddy Coronación | Coronacion Meza Fredy | APROBADA | ACEPTADO | 2026-10-04 | Sí | CONFORME | OBS-F34C-02, 03, 04, 05 |
| [Anthony_Pena](adjuntos/G0-ADR005-ThreatModel_Anthony_Pena_2026-10-04.png) | Única | `a280b48835f4b859a05fe3407f037f01bb9fc62cd2e41fca6cc780408deaba30` | JPEG | Anthony Peña | Peña Antony | Peña Arroyo Anthony | APROBADA | ACEPTADO | 2026-10-04 | Sí | CONFORME | OBS-F34C-02, 03, 04, 05 |
| [Luis_Vila_original](adjuntos/G0-ADR005-ThreatModel_Luis_Vila_2026-10-04_original.png) | Original (histórica) | `ba464828a8180c0db9961ba493ea8e1d4702db51719e2d975c3463abda724f3d` | PNG | — (mensaje propio) | Luis Antonio Vila Meza | Vila Meza Luis Antonio | APROBADA | ACEPTADO | 2026-10-04 | Sí | RESUELTA por [confirmación](adjuntos/G0-ADR005-ThreatModel_Luis_Vila_2026-10-04.png) | OBS-F34C-01 (resuelta), 05, 06 |
| [Luis_Vila_confirmación](adjuntos/G0-ADR005-ThreatModel_Luis_Vila_2026-10-04.png) | Confirmación adicional | `d2ed9dd568051780c51799031ee6ef78197c106d427a77a7c24a49cacb4d10e2` | JPEG | — (mensaje propio) | Luis Antonio Vila Meza | Vila Meza Luis Antonio | APROBADA | ACEPTADO | 2026-10-04 | Sí | CONFORME | OBS-F34C-03, 06 |

**Remitente visible** (corrección F34C-M02-R1):

- **Ausente:** solo como «— (mensaje propio)», es decir, un mensaje enviado desde el propio WhatsApp, que no muestra remitente. Exige que el mensaje declare el **nombre completo** del integrante y que el resto de controles pase.
- **Presente:** solo si es el nombre completo o una variante revisada (tabla siguiente) del **mismo** integrante de la fila, del nombre declarado y del adjunto.
- **Desconocido o de otra persona:** requiere revisión manual; la evidencia no es válida y G0-14 y G0-09 no pueden quedar CUMPLIDO.

### Correspondencias de identidad revisadas

Sin coincidencias aproximadas: un nombre declarado vale solo si es el nombre completo de un integrante o figura en esta tabla, revisada en F34C. Cualquier otra variante requiere revisión manual y `validate_f34b.py` la rechaza.

| Variante declarada | Integrante | Revisión |
|---|---|---|
| Peña Antony | Peña Arroyo Anthony | F34C, captura de Anthony Peña |
| Anthony Peña | Peña Arroyo Anthony | F34C, remitente visible |
| Fredy Coronación | Coronacion Meza Fredy | F34C |
| Freddy Coronación | Coronacion Meza Fredy | F34C, captura de Fredy Coronacion |
| Fredy Sistemas | Coronacion Meza Fredy | F34C-M02-R1, remitente visible en la captura de Fredy Coronacion |
| Luis Antonio Vila Meza | Vila Meza Luis Antonio | F34C, capturas de Luis Vila |

**Observaciones de la verificación:**

- **OBS-F34C-01 · Fecha de envío — RESUELTA.** La captura original de Luis Vila muestra el separador «Wednesday» mientras declara 04/10/2026. Se resuelve con la confirmación adicional del mismo integrante: mismas decisiones, mismo nombre completo y la frase «La fecha correcta de esta confirmación es: 04/10/2026», con la hora visible (8:12 PM). No se registra ninguna explicación de por qué la captura original mostraba «Wednesday». La original se conserva como histórica.
- **OBS-F34C-02 · Variantes del nombre.** «Peña Antony» y «Freddy Coronación», y los remitentes «Anthony Peña» y «Fredy Sistemas», difieren del registro oficial. Se aceptan solo por las correspondencias revisadas de la tabla anterior, no por similitud; «Fredy Sistemas» es el remitente visible en la captura de Fredy Coronacion, que declara su nombre en el mensaje.
- **OBS-F34C-03 · Formato.** Las capturas de Fredy, Anthony y la confirmación de Luis son **JPEG** con extensión `.png`. La original de Luis es PNG. No se renombran.
- **OBS-F34C-04 · Nombre de archivo.** Siguen el patrón `G0-ADR005-ThreatModel_<integrante>_<fecha>` en lugar de `G0-xx_<tipo>_<fecha>`; se aceptan tal como se aportaron.
- **OBS-F34C-05 · Contenido adicional.** Las capturas incluyen elementos ajenos a la decisión (avatares, una imagen, el nombre de un archivo DOCX y otros mensajes del grupo). No contienen datos de candidatos ni de postulantes.
- **OBS-F34C-06 · Sustitución del archivo original.** La confirmación adicional se guardó con el **mismo nombre** que la captura original de Luis Vila y la sobrescribió antes de cualquier commit, aunque un adjunto archivado no debe reemplazarse. La imagen registrada inicialmente en F34C (JPEG, SHA-256 `e59c59935e51192942c31f444b3a8b9465a5ac93074e7c86011c5723bbc871f8`) ya no existe en el repositorio. La original se restauró **como archivo aparte** (`…_original.png`) desde su archivo de origen, una captura PNG de Windows de 699 × 379 con el mismo contenido verificado en F34C; tiene otro formato y otro SHA-256. La confirmación conserva el nombre de archivo con el que se aportó.
