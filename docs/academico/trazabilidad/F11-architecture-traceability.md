# Trazabilidad de la arquitectura (F11)

Componente → RF → CU → RNF → alcance F9 → artefacto técnico. Generado desde `m_arch.py`, `m_cu.py` y `validate.py`; no se inventan correspondencias: los RF y CU salen de la tabla de componentes, el alcance IN sale de los CU (F8/F9) y el artefacto técnico es la fuente citada (CO-01, PK-01, SEQ, ADR).

| Componente | RF | CU | RNF | Alcance F9 | Artefacto técnico |
|---|---|---|---|---|---|
| C01 Interfaz web | RF-01..RF-27 (interacción) | Todos (interfaz) | RNF-05, RNF-08, RNF-09 | Transversal / soporte | CO-01 «Páginas Inertia», «Componentes compartidos»; resources/js/pages |
| C02 Autenticación y cuentas | RF-08 | CU-07 | RNF-01, RNF-09 | IN-03 | CO-01 «Cuenta y acceso» (Fortify) |
| C03 Autorización y contexto multiempresa | RNF (seguridad y multitenencia); aplica a RF-01..RF-27 | Todos (transversal) | RNF-01, RNF-02, RNF-09 | Transversal / soporte | CO-01 «Autorización y multiempresa» (7 Policies, OrganizationScope); cap. 7 §7.3 |
| C04 Requerimientos de personal | RF-01, RF-02, RF-03, RF-04 | CU-01, CU-02, CU-03 | RNF-09, RNF-10 | IN-01 | PK-01 «Requerimientos» |
| C05 Vacantes y convocatorias | RF-05, RF-06, RF-07, RF-20 | CU-04, CU-05, CU-06, CU-16 | RNF-09, RNF-10 | IN-02, IN-06 | PK-01 «Vacantes» |
| C06 Postulantes y CV | RF-09 | CU-08 | RNF-04, RNF-09 | IN-03 | PK-01 «Postulantes» |
| C07 Postulaciones y etapas | RF-10, RF-11, RF-12, RF-13, RF-14, RF-15 | CU-09, CU-10, CU-11, CU-12 | RNF-09, RNF-10 | IN-03, IN-04 | PK-01 «Postulaciones» y «Postulantes» (ApplicationService) |
| C08 Evaluaciones y entrevistas | RF-16, RF-17, RF-18, RF-19, RF-20 | CU-13, CU-14, CU-15, CU-16 | RNF-09, RNF-10 | IN-05, IN-06 | PK-01 «Evaluaciones» (evaluaciones y entrevistas en un solo módulo) |
| C09 Ranking y comparación | RF-20, RF-21, RF-22 | CU-16, CU-17 | RNF-09, RNF-10 | IN-06 | CO-01 «Cálculo de ranking»; PK-01 «Ranking y selección» |
| C10 Decisión final humana | RF-23 | CU-18 | RNF-09 | IN-07 | CO-01 FinalDecisionService; SEQ-07; ADR-002 |
| C11 Selección y cierre | RF-24, RF-25, RF-26 | CU-19, CU-20 | RNF-09 | IN-07 | PK-01 «Ranking y selección» |
| C12 Notificaciones | RF-04, RF-11, RF-15, RF-17, RF-26 | CU-03, CU-09, CU-11, CU-12, CU-13, CU-14, CU-20 | RNF-04, RNF-07, RNF-09 | IN-01, IN-03, IN-04, IN-05, IN-07 | CO-01 «Notificaciones» |
| C13 Auditoría | RF-27 | Transversal (UC-RF27) | RNF-03, RNF-09 | IN-08 | CO-01 «Auditoría»; A-33, A-34 |
| C14 Persistencia de datos (PostgreSQL) | Soporte de RF-01..RF-27 | — | RNF-03, RNF-06, RNF-07, RNF-09, RNF-10 | Transversal / soporte | CO-01 «PostgreSQL 17»; cap. 7 §7.5 |
| C15 Almacenamiento privado de CV | RF-09, RF-12 | CU-08, CU-10 | RNF-04, RNF-09 | IN-03, IN-04 | CO-01 «Almacenamiento de CV»; A-12 |
| C16 Sesiones, caché y cola (Redis) | Soporte de C02 y C12 | — | RNF-06, RNF-09 | Transversal / soporte | CO-01 «Redis 7», «Trabajador de cola»; cap. 7 §7.6 |
| C17 Riesgo operacional del proceso (RF-29) | RF-29 | — (fuera del catálogo; UC-RF29) | RNF-09 | Fuera de la línea base (RF-29) | CO-01 «Riesgo operacional» y «Servicio de inferencia»; SEQ-08; ADR-001; ADR-004 |

Notas: C01, C03, C14 y C16 soportan todos los RF (interfaz, autorización y persistencia) y no se listan RF por separado. C13 es transversal (RF-27 → UC-RF27, IN-08). C17 es experimental (RF-29, fuera de la línea base). Relación con la cadena académica: [F2-F9-traceability.md](F2-F9-traceability.md).
