# Validación de la arquitectura conceptual (F11)

Resultados: PASS · PASS CON OBSERVACIÓN · NO VERIFICADO · NO APLICA. Generado por `validate.py` (`f11_checks`) sobre el modelo `m_arch.py`. Es una validación **estructural y académica, interna del equipo**: no hay aprobación institucional. `validate.py` no juzga la calidad semántica del diseño (ver `docs/academico/trazabilidad/README.md`).

## Matriz de validación

| Criterio | Fuente | Resultado | Evidencia | Observación |
|---|---|---|---|---|
| A. Cobertura funcional RF-01..RF-27 | F6; COMPONENTS.md | PASS | 27/27 RF asignados a componentes de negocio o transversales |  |
| A. Ningún RF fuera de la línea base (salvo RF-29 experimental en C17) | F6; scope-preliminary.md | PASS | RF-29 solo en C17 |  |
| B. Cobertura CU-01..CU-20 | F8 | PASS | 20/20 CU |  |
| B. Ningún CU nuevo; CU-21 sigue DIFERIDO | F8 (D-CU-03) | PASS | Sin CU-21 ni otros |  |
| C. Alcance incluido IN-01..IN-08 representado | F9 §5 | PASS | Todos los bloques IN tienen componente (vía CU/RF) |  |
| C. Ningún componente fuera de alcance (OUT-01..OUT-11) | F9 §6 | PASS | Exclusiones listadas aparte (X-01..X-04), no como componentes |  |
| D. Los 10 RNF académicos relacionados con decisiones y componentes | F7 | PASS | 10/10 con decisión (DA) y componente |  |
| D. RNF-05 Usabilidad | F7 | PASS CON OBSERVACIÓN | DA-10; C01 | Evidencia parcial según F7 |
| D. RNF-06 Rendimiento | F7 | NO VERIFICADO | Soporte arquitectónico: DA-01, DA-09; C16 (caché y cola desacoplan el envío de notificaciones); C14 | Sin evidencia de medición; no se afirma validado |
| D. RNF-07 Disponibilidad y recuperabilidad | F7 | NO VERIFICADO | Soporte arquitectónico: DA-08, DA-09; C14 (transacciones, restricciones), C12 (envío tras el commit) | Sin evidencia de medición; no se afirma validado |
| D. RNF-08 Compatibilidad | F7 | PASS CON OBSERVACIÓN | DA-10; C01 | Evidencia parcial según F7 |
| D. RNF-09 Mantenibilidad | F7 | PASS CON OBSERVACIÓN | DA-01; Todos (módulos por dominio) | Evidencia parcial según F7 |
| E. RF-23: decisión final humana en un componente propio (C10), distinto del ranking | ADR-002; F6 RF-23; F8 CU-18 | PASS | C10 «Decisión final humana»; R-10: el ranking no elige |  |
| E. RF-29 experimental y separado de ranking, decisión y selección | ADR-001; ADR-004; OUT-11 | PASS | C17 EXPERIMENTAL; relaciones solo con C01, C05 |  |
| E. RF-28 no implementado: sin componente productivo | scope-preliminary.md; OUT-07 | PASS | X-01 lo registra como NO IMPLEMENTADO |  |
| F. Multitenencia: C03 autoriza y filtra todos los módulos de negocio | cap. 7 §7.3; RNF-02 | PASS | R-03 C03 → C04..C11, C13 | Sin RLS (DA-02) |
| G. Auditoría transversal de las acciones críticas | RF-27; A-33, A-34 | PASS | R-13 C04..C11 → C13; trigger de solo inserción | Consulta: capacidad técnica (CU-21 diferido) |
| H. Privacidad del CV: almacenamiento privado y descarga autorizada | A-12, A-15; RNF-04 | PASS | C15; R-17; DA-05 |  |
| Componentes: todos con RF/CU o justificación transversal o de soporte | COMPONENTS.md | PASS | 17 componentes |  |
| Relaciones: ningún componente aislado | RELATIONSHIPS.md | PASS | 20 relaciones |  |
| Relaciones: sin dependencias circulares entre módulos de negocio | RELATIONSHIPS.md | PASS | Grafo C04..C11 acíclico |  |
| Relaciones: flujo completo requerimiento → vacante → postulación → evaluación → ranking → decisión → selección | F5 (TO-BE); RELATIONSHIPS.md | PASS | R-05..R-12 |  |

## Validación de componentes

| Componente | Tiene RF/CU/justificación transversal | Estado | Observación |
|---|---|---|---|
| C01 Interfaz web | Sí — soporte de infraestructura / interfaz | IMPLEMENTADO |  |
| C02 Autenticación y cuentas | Sí — RF-08 | IMPLEMENTADO |  |
| C03 Autorización y contexto multiempresa | Sí — transversal | TRANSVERSAL |  |
| C04 Requerimientos de personal | Sí — RF-01, RF-02, RF-03, RF-04 | IMPLEMENTADO |  |
| C05 Vacantes y convocatorias | Sí — RF-05, RF-06, RF-07, RF-20 | IMPLEMENTADO |  |
| C06 Postulantes y CV | Sí — RF-09 | IMPLEMENTADO |  |
| C07 Postulaciones y etapas | Sí — RF-10, RF-11, RF-12, RF-13, RF-14, RF-15 | IMPLEMENTADO |  |
| C08 Evaluaciones y entrevistas | Sí — RF-16, RF-17, RF-18, RF-19, RF-20 | IMPLEMENTADO |  |
| C09 Ranking y comparación | Sí — RF-20, RF-21, RF-22 | IMPLEMENTADO |  |
| C10 Decisión final humana | Sí — RF-23 | IMPLEMENTADO |  |
| C11 Selección y cierre | Sí — RF-24, RF-25, RF-26 | IMPLEMENTADO |  |
| C12 Notificaciones | Sí — RF-04, RF-11, RF-15, RF-17, RF-26 | TRANSVERSAL |  |
| C13 Auditoría | Sí — RF-27 | TRANSVERSAL |  |
| C14 Persistencia de datos (PostgreSQL) | Sí — soporte de infraestructura / interfaz | IMPLEMENTADO |  |
| C15 Almacenamiento privado de CV | Sí — RF-09, RF-12 | IMPLEMENTADO |  |
| C16 Sesiones, caché y cola (Redis) | Sí — soporte de infraestructura / interfaz | IMPLEMENTADO |  |
| C17 Riesgo operacional del proceso (RF-29) | Sí — RF-29 | EXPERIMENTAL | RF-29 fuera de la línea base |

## Validación de relaciones

- Relaciones necesarias: R-01 a R-20 (todas las pedidas por el encargo, con la dirección de dependencia real).
- Dependencias circulares entre módulos de negocio: ninguna (C07 no depende de otro módulo de negocio; C08 y C11 dependen de C07).
- Componentes aislados: ninguno.
- Flujo completo: R-05 → R-06/R-07 → R-08 → R-09 → R-10 → R-11 → R-12.
- RF-29: C17 solo se relaciona con C05 (lectura de datos operativos) y C01 (presentación); **sin relación** con C09, C10 ni C11.
