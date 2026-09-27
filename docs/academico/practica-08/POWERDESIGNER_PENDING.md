# Pendiente de PowerDesigner — F8 casos de uso (vista académica)

**Estado: READY FOR POWERDESIGNER (adaptación).** La decisión del equipo de la F27D cerró el catálogo:

- los 20 CU quedan aprobados;
- CU-18 se renombra;
- CU-21 queda diferido.

Se modela en la **Fase 29**. En las F27B y F27D no se abrió PowerDesigner y **UC-01 de la F23 sigue sin cambios**.

## Qué debe modelarse

Un diagrama de casos de uso **nuevo**, «F8 Casos de uso — vista académica (CU-01 a CU-20)», en un paquete propio del OOM o en un modelo aparte. **No** debe editar UC-01 (vista técnica UC-RF01 a UC-RF29) ni sus 29 casos.

## Actores

Son 5: ACT-01 Área solicitante, ACT-02 Recursos Humanos, ACT-03 Aprobador / Dirección, ACT-04 Postulante y ACT-05 Evaluador.

- El Sistema no es un actor.
- No se dibujan el servicio de riesgo (RF-29) ni actores fuera del alcance.

## Casos (catálogo aprobado, sin CU-21)

Los 20 CU con los nombres del Formato 08. **CU-18 se llama «Registrar decisión final humana»**; su alias histórico es «Registrar decisión final».

| Actor | Casos |
|---|---|
| ACT-01 | CU-01, CU-02 |
| ACT-02 | CU-02, CU-04, CU-05, CU-06, CU-10, CU-11, CU-12, CU-13, CU-14, CU-17, CU-19, CU-20 |
| ACT-03 | CU-03, CU-10, CU-17, CU-18 |
| ACT-04 | CU-07, CU-08, CU-09 |
| ACT-05 | CU-15 |

## Relaciones y notas

- «include»: CU-05 → CU-16, CU-15 → CU-16 y CU-17 → CU-16.
- **Nota en CU-18:** «decisión humana (RF-23): la registra solo el Aprobador / Dirección; el ranking no elige».
- **Nota en CU-17:** «calcula, ordena y compara; no selecciona».
- **Nota técnica de auditoría** (no es un caso de uso): «Consulta de auditoría vinculada a RF-27 y ACT-03; cubierta por la vista técnica UC-RF27 y fuera del catálogo académico CU-01..CU-20 de esta versión».
- **CU-21 «Consultar auditoría»: DIFERIDO.** No se dibuja ni queda como decisión pendiente en esta versión.

## Criterio de aceptación

1. **Elementos:** los 20 CU, los 5 actores y las asociaciones coinciden uno a uno con el Formato 08 aprobado.
2. **Cobertura:** RF-01 a RF-26 están en algún CU y RF-27 figura como nota transversal. No aparece ningún RF fuera de la línea base.
3. **Modelos existentes:** UC-01 y los demás diagramas de la F23 no cambian.
4. **Exportación:** PNG y SVG, y el borrador del Formato 08 se sustituye solo después de una nueva auditoría.
