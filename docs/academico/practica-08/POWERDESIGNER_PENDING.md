# Pendiente de PowerDesigner — F8 casos de uso (vista académica)

**Estado: REQUIERE POWERDESIGNER (adaptación).** Se hace en la **Fase 29**, después de que la auditoría **F27C** apruebe la vista académica y el equipo confirme los nombres de CU-01 a CU-20 (O-F8-01). En la F27B no se abrió PowerDesigner y **UC-01 de la F23 sigue sin cambios**.

## Qué debe modelarse

Un diagrama de casos de uso **nuevo**, «F8 Casos de uso — vista académica (CU-01 a CU-20)», en un paquete propio del OOM o en un modelo aparte. **No** debe editar UC-01 (vista técnica UC-RF01 a UC-RF29) ni sus 29 casos.

## Actores

Son 5: ACT-01 Área solicitante, ACT-02 Recursos Humanos, ACT-03 Aprobador / Dirección, ACT-04 Postulante y ACT-05 Evaluador.

- El Sistema no es un actor.
- No se dibujan el servicio de riesgo (RF-29) ni actores fuera del alcance.

## Casos y asociaciones

Los 20 CU y sus actores directos, tal como están en la tabla «Relación actores-casos de uso» del Formato 08. Resumen:

| Actor | Casos |
|---|---|
| ACT-01 | CU-01, CU-02 |
| ACT-02 | CU-02, CU-04, CU-05, CU-06, CU-10, CU-11, CU-12, CU-13, CU-14, CU-17, CU-19, CU-20 |
| ACT-03 | CU-03, CU-10, CU-17, CU-18 |
| ACT-04 | CU-07, CU-08, CU-09 |
| ACT-05 | CU-15 |

## Relaciones

- «include»: CU-05 → CU-16, CU-15 → CU-16 y CU-17 → CU-16.
- Nota en CU-18: «decisión humana (RF-23): la registra solo el Aprobador / Dirección; el ranking no elige».
- Nota en CU-17: «calcula, ordena y compara; no selecciona».
- Nota de auditoría: RF-27 es transversal y, según el F9, está incluido en CU-18. Si el equipo aprueba CU-21 «Consultar auditoría» (O-F8-02), se añade con asociación a ACT-03, **sin renumerar** los demás.

## Criterio de aceptación

1. **Elementos:** los 20 CU, los 5 actores y las asociaciones coinciden uno a uno con el Formato 08 aprobado.
2. **Cobertura:** los 27 RF quedan cubiertos (matriz de correspondencia del Formato 08) y no aparece ningún RF fuera de la línea base.
3. **Modelos existentes:** UC-01 y los demás diagramas de la F23 no cambian.
4. **Exportación:** PNG y SVG, y el borrador del Formato 08 se sustituye solo después de una nueva auditoría.
