# F34B — Validación de la necesidad institucional (G0-12)

> Fase F34B, versión 1 (04/10/2026); **actualizada en F34D**. Registro de las respuestas reales al [instrumento de F34A](../g0-readiness/F34A_Validacion_Necesidad_Institucional.md). **Estado: PENDIENTE.** En F34D se recibió una respuesta en texto (§4), pero **sin evidencia archivada y con identidad no verificable**: no cierra G0-12. Ninguna respuesta se redacta en nombre de otra persona.

## 1. Cómo se registra

1. Quien responde completa el instrumento de F34A (preguntas N-01 a N-10) en un documento propio, con su nombre, rol, fecha y firma o constancia.
2. Ese documento se archiva en [`adjuntos/`](adjuntos/README.md).
3. Su fila se actualiza aquí con la decisión que resulta del criterio de cierre de F34A (§5 del instrumento).

## 2. Registro

Valores de **Decisión:** `PENDIENTE`, `NECESIDAD VALIDADA`, `NECESIDAD NO VALIDADA`. **Estado:** `PENDIENTE` o `REGISTRADO`. **Roles admitidos:** `Docente del curso`, `RR. HH.`, `Administración` y `Representante institucional`, cada uno en una sola fila. Cada fila es de una persona distinta y ninguna puede ser integrante del equipo del proyecto. Cualquier otro rol invalida el registro. **Identidad del docente (F34D):** la fila `Docente del curso` solo se registra con el nombre del docente que consta en el proyecto (`CLAUDE.md`), o con una variante revisada y documentada; sin coincidencias aproximadas.

| Responsable | Rol | Fecha | Decisión | Evidencia adjunta/referencia | Observaciones | Estado |
|---|---|---|---|---|---|---|
| — | Docente del curso | — | PENDIENTE | — | Respuesta en texto recibida en F34D, sin adjunto e identidad no verificable (§4, OBS-F34D-01 y 02) | PENDIENTE |
| — | RR. HH. | — | PENDIENTE | — | — | PENDIENTE |
| — | Administración | — | PENDIENTE | — | — | PENDIENTE |
| — | Representante institucional | — | PENDIENTE | — | — | PENDIENTE |

Si un perfil no está disponible, su fila queda en PENDIENTE; no se sustituye por una suposición del equipo.

## 3. Regla de resultado

- G0-12 pasa a CUMPLIDO si **la fila del docente o la del representante institucional** está `REGISTRADO` con `NECESIDAD VALIDADA` y adjunto existente, y ninguna fila registrada dice `NECESIDAD NO VALIDADA`.
- Si alguna fila registrada dice `NECESIDAD NO VALIDADA`, G0-12 queda RECHAZADO y la alternativa A sigue siendo el estado por defecto.
- En cualquier otro caso, PENDIENTE EXTERNO.
- Las respuestas no autorizan datos reales ni cambian ninguna prohibición vigente.

## 4. Respuesta recibida en F34D (sin evidencia archivada)

Se transcribe tal como se recibió. **No se archivó ningún adjunto** (captura, PDF, correo exportado ni documento firmado) en [`adjuntos/`](adjuntos/README.md), por lo que el texto **no es evidencia verificable** y la fila del docente sigue en PENDIENTE.

| Campo | Valor |
|---|---|
| Estado de la respuesta | SIN EVIDENCIA ARCHIVADA |
| Adjunto | — |
| SHA-256 | — |
| Formato real | — |
| Nombre declarado | Max Magnolie Arana |
| Rol declarado | Docente / Profesor Revisor |
| Institución declarada | Universidad Continental (UC Continental) |
| Fecha declarada | 2026-10-04 |
| Decisión declarada | NECESIDAD VALIDADA |
| Verificación de identidad | NO VERIFICABLE |

**Respuestas declaradas:**

1. Necesidad real de mejorar el apoyo a la evaluación o revisión: **SÍ**.
2. Utilidad de organizar evidencias, criterios y rúbricas sin reemplazar la decisión humana: **SÍ**.
3. Aceptable que **no** exista scoring con ML ni recomendación automática: **SÍ**.
4. Alcance proporcional: **SÍ**.

**Restricciones o recomendación declaradas:** «El alcance definido es adecuado y éticamente transparente. Se recomienda mantener la auditabilidad de las rúbricas y asegurar una capacitación breve a los evaluadores del Colegio Andino para optimizar el uso de las explicaciones visibles y la trazabilidad de evidencias.»

**Observación declarada** (opinión del revisor, no un hecho institucional verificado): «El Alcance B garantiza el equilibrio perfecto entre automatización operativa y control ético en el proceso de selección de personal, cumpliendo plenamente con los requerimientos y estándares institucionales.»

**Confirmación declarada:** «Declaro que esta respuesta corresponde a mi revisión real del alcance descrito.»

### Observaciones F34D

- **OBS-F34D-01 · Sin evidencia archivada.** La respuesta llegó solo como texto. Para cerrar G0-12 hace falta archivar en `adjuntos/` la respuesta original (captura, PDF, correo exportado o documento firmado) con su SHA-256 y formato real.
- **OBS-F34D-02 · Identidad no verificable.** El nombre declarado, «Max Magnolie Arana», **no coincide** con el docente registrado en el proyecto, «Dr. Maglioni Arana Caparachin» (`CLAUDE.md`, `ACADEMIC_BASELINE.md`): solo comparten «Arana». No se corrige el nombre, no se usa coincidencia aproximada y no se presume que sean la misma persona. El cierre exige que la propia evidencia o su contexto permita vincularlo sin ambigüedad con el docente, o una confirmación adicional de este.
- **OBS-F34D-03 · Límites de lo validado.** Si llegara a verificarse, la respuesta valida solo la **necesidad**, la **utilidad del alcance B**, la **proporcionalidad** y la **preservación de la decisión humana**. **No es una aprobación jurídica, no es una aprobación de privacidad, no es una autorización del Colegio Andino** y no certifica el cumplimiento institucional. Tampoco autoriza datos reales ni el alcance C. La frase sobre el cumplimiento de requerimientos y estándares institucionales se registra como opinión del revisor.

### Recomendaciones recibidas (pendientes de evidencia)

Se conservan para fases futuras **solo si la respuesta se verifica**. No modifican RF-01 a RF-27, los RF candidatos ni el alcance:

- mantener la auditabilidad de las rúbricas;
- capacitación breve a los evaluadores;
- explicaciones visibles;
- trazabilidad de evidencias.
