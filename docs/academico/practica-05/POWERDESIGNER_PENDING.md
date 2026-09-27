# Pendiente de PowerDesigner — F5 BPMN TO-BE

**Estado: READY FOR POWERDESIGNER.** Especificación cerrada en la F27D, que resolvió los hallazgos H-03, H-04 y H-05 de la auditoría F27C. Se modela en la **Fase 29**. En las F27B y F27D no se abrió PowerDesigner ni se modificó ningún `.oom`, `.pdm` o exportación de la F23.

La especificación permite construir el modelo sin reinterpretar nada. Es un modelo de negocio, **distinto** de AC-01 (diagrama de actividad UML del software implementado, F23), que se conserva sin cambios.

Nombre: «F5 BPMN TO-BE propuesto — Reclutamiento y selección».

## Dos niveles

| Nivel | Instancias | Contenido |
|---|---|---|
| **Vacante** (convocatoria) | Una por requerimiento o vacante | A (TB-01 a TB-06), B (TB-07 a TB-10), **SP-P**, E (TB-24 a TB-29) y TB-30 (transversal) |
| **Postulación** (candidato) | **SP-P**: subproceso expandido de **instancia múltiple paralela**, una instancia por postulación registrada | Pool de la organización: TB-14 a TB-23. Pool del Postulante: TB-11 a TB-13 |

SP-P crea una instancia por cada mensaje MT-02. El nivel vacante continúa en TB-24 cuando **todas** las instancias terminaron. **El flujo principal supone al menos una postulación finalista.** El caso sin finalistas no tiene camino implementado (A-30) y no se modela como regla del sistema.

## Pools y lanes

| Pool | Lanes |
|---|---|
| Organización cliente (Colegio) con la plataforma — TO-BE propuesto | Área solicitante · RR. HH. · Aprobador / Dirección · Evaluador · Plataforma SaaS (sistema) |
| **Postulante** | Participante visible con EP-01 → TB-11 → TB-12 → TB-13 → EP-02. Los demás mensajes llegan al **borde del pool** |

## Eventos (nombres oficiales)

| ID | Tipo | Nombre |
|---|---|---|
| EI | Inicio (nivel vacante) | Necesidad de personal identificada |
| EFA | Fin (nivel vacante) | Requerimiento rechazado |
| EFE | Fin (nivel vacante) | Convocatoria cerrada con selección |
| SIP | Inicio de SP-P | Postulación registrada |
| EFP-01 | Fin de SP-P | Postulación descartada en la preselección |
| EFP-02 | Fin **de mensaje** de SP-P (envía MT-06) | Postulación finalista |
| EFP-03 | Fin **de mensaje** de SP-P (envía MT-07) | Postulación descartada tras la evaluación |
| EP-01 | Inicio de mensaje (Postulante) | Vacante publicada |
| EP-02 | Fin (Postulante) | Postulación presentada |

Los eventos de enlace A, B, C y D del borrador solo sirven para paginar las imágenes. En PowerDesigner se sustituyen por flujos directos.

## Compuertas (incluidas las uniones)

| ID | Tipo | Lane | Nombre | Salidas |
|---|---|---|---|---|
| GA1 | Exclusiva | RR. HH. | ¿Requerimiento conforme? | Observado → TB-04 (→ TB-02) · Validado → TB-05 |
| GA2 | Exclusiva | Aprobador / Dirección | ¿Requerimiento aprobado? | No → TB-06 → EFA · Sí → TB-07 |
| GB1 | Exclusiva | Plataforma | ¿Configuración válida? | No → TB-08 · Sí → TB-10 |
| GD1 | Exclusiva (SP-P) | RR. HH. | ¿Candidato preseleccionado? | No → EFP-01 · Sí → GM1 |
| GM1 | **Unión** exclusiva (SP-P) | RR. HH. | Unión antes de programar | Entradas: GD1 [Sí] y GD3 [Sí] → GD2 |
| GD2 | Exclusiva (SP-P) | RR. HH. | ¿Qué sesión se programa? | Evaluación → TB-18 · Entrevista → TB-20 |
| GM2 | **Unión** exclusiva (SP-P) | Plataforma | Unión de sesiones programadas | Entradas: TB-18 y TB-20 → TB-19 |
| GV | Exclusiva (SP-P) | Plataforma | ¿Puntajes válidos? | **No → TB-21** (el sistema rechaza, no guarda nada, y el evaluador corrige y reenvía) · Sí → GD3 |
| GD3 | Exclusiva (SP-P) | RR. HH. | ¿Otra sesión? | Sí → GM1 · No → TB-23 |
| GF | Exclusiva (SP-P) | RR. HH. | **¿Finalista?** | Sí → EFP-02 · No → EFP-03 |

No hay dos secuencias que converjan sin una unión: TB-15 tiene una sola entrada (desde TB-14), y las convergencias se resuelven en GM1 y GM2.

## Secuencias

- **Nivel vacante:** EI → TB-01 → TB-02 → TB-03 → GA1 → TB-05 → GA2 → TB-07 → TB-08 → TB-09 → GB1 → TB-10 → **SP-P** → TB-24 → TB-25 → TB-26 → TB-27 → TB-28 → TB-29 → EFE.
- **SP-P:** SIP → TB-14 → TB-15 → TB-16 → TB-17 → GD1 → GM1 → GD2 → (TB-18 | TB-20) → GM2 → TB-19 → TB-21 → TB-22 → GV → GD3 → TB-23 → GF → (EFP-02 | EFP-03).
- **Postulante:** EP-01 → TB-11 → TB-12 → TB-13 → EP-02.

## Flujos de mensaje (lista cerrada, unidireccional)

| ID | Origen | Destino | Elemento receptor | Contenido |
|---|---|---|---|---|
| MT-01 | TB-10 (organización) | Postulante | EP-01 | Vacante publicada en el portal |
| MT-02 | TB-13 (Postulante) | Organización | Borde de SP-P (crea una instancia) | Postulación |
| MT-03 | TB-14 (Plataforma, SP-P) | Postulante | Borde del pool | Confirmación y código |
| MT-04 | TB-17 (Plataforma, SP-P) | Postulante | Borde del pool | Aviso de preselección o descarte |
| MT-05 | TB-19 (Plataforma, SP-P) | Postulante | Borde del pool | Convocatoria. El aviso al evaluador es interno al pool, no un mensaje |
| MT-06 | EFP-02 (fin de mensaje) | Postulante | Borde del pool | Aviso de etapa: finalista (RF-15) |
| MT-07 | EFP-03 (fin de mensaje) | Postulante | Borde del pool | Aviso de etapa: descarte (RF-15) |
| MT-08 | TB-29 (Plataforma) | Postulante | Borde del pool | Resultado propio |

## Elementos fuera de la secuencia

| Elemento | Cómo se modela |
|---|---|
| **TB-26** «Registrar la decisión final humana» | En el lane del **Aprobador / Dirección**, con la anotación «decisión humana (RF-23): el ranking no elige». |
| **TB-30** «Registrar la auditoría de las acciones críticas» | Transversal, **sin flujo de secuencia**. Almacén de datos «Auditoría» con asociaciones desde las tareas críticas, o tarea en un grupo anotado «transversal». |
| **TB-F1** «Cerrar la convocatoria sin selección» | Grupo aparte con la anotación «Propuesta futura (A-30), no implementada». **Sin flujo de entrada ni de salida** y sin ninguna condición del sistema: no se representa ninguna regla «sin candidato elegible». |

## Criterio de aceptación

1. **Elementos:** TB-01 a TB-30, TB-F1, SP-P, las 10 compuertas, los 9 eventos y los 8 mensajes coinciden uno a uno con el Formato 05.
2. **Decisión final:** está en el lane del Aprobador / Dirección. Ninguna tarea del sistema decide, selecciona ni descarta.
3. **TB-F1:** queda desconectado y RF-29 no aparece en el TO-BE base.
4. **Modelos existentes:** AC-01 y los demás diagramas de la F23 se conservan sin cambios.
5. **Exportación:** PNG y SVG, y el Formato 05 se actualiza solo después de una nueva auditoría.
