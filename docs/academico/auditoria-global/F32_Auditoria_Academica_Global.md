# F32 — Auditoría académica global del proyecto

## 1. Veredicto y alcance

**APROBADA CON OBSERVACIONES; M01/L01/L02 RESUELTOS.** La auditoría inicial detectó 1 MEDIUM de reproducción histórica, 2 LOW de navegación/gobierno y 4 OBSERVATION. La corrección autorizada resolvió los tres hallazgos; no hay CRITICAL/HIGH/MEDIUM/LOW abiertos de este alcance. Los contratos del producto y los artefactos presentes conservan integridad. Las cuatro observaciones aceptadas/futuras permanecen explícitas.

**APTO PARA F33 DE DISEÑO**: puede formular ADR-005 y criterios G0, no implementar scoring/recomendación de candidatos ni aprobar G0 por esta auditoría. G0 sigue **NO APROBADA**. Detalle en [readiness](F32_Readiness_F33.md) y [matriz de hallazgos](F32_Matriz_Hallazgos.md).

Fecha: 03/10/2026, America/Lima; evidencia de CI consultada después del 04/10/2026 03:18 UTC. Rama creada desde develop limpio: `feature/f32-global-academic-audit`. La auditoría inicial solo escribió cuatro Markdown de esta carpeta; la corrección posterior autorizada modifica recetas, navegación y protecciones del tooling documental. La auditoría/corrección se realizó sin commits ni publicaciones, sin cambios productivos ni regeneración de artefactos existentes. Posteriormente el usuario autorizó el cierre: **F32 CERRADA CON OBSERVACIONES**, un único commit e integración con gates CI.

## 2. Método y límites

Se aplicaron las instrucciones de CLAUDE/AGENTS y las skills compartidas project-guardian, academic-traceability, powerdesigner-uml y, para contrastar las fronteras, ml-risk-service/laravel-saas-quality. Se revisaron gobierno, cuatro ADR, formatos académicos, relaciones arquitectónicas, generadores, catálogo CSV de CP, registros QA y fuentes F30. Se muestreó código real de ranking, decisión humana, cliente ML, aislamiento de evaluaciones, almacenamiento privado y trigger de auditoría.

Se ejecutaron los validadores documentales, comprobaciones de enlaces e integridad; se inspeccionó el PNG formal ARQ-01 vigente. No se abrió PowerDesigner ni se modificaron sus modelos. La reproducción determinista que ejecuta el validador usa su flujo temporal: no se llamó al dispatcher de generación en el repositorio.

No se repitieron suites funcionales completas: F32 no modifica runtime. Se contrastaron resultados registrados con validadores/archivos de evidencia, y CI actual con la API pública de GitHub. No es una prueba de aceptación productiva, auditoría exhaustiva de todas las líneas de código, revisión jurídica profesional ni revalidación independiente del texto íntegro de 107 publicaciones. No se inventan resultados de instituciones, pruebas manuales o despliegues.

## 3. Gobierno, requisitos y exclusiones

| Control | Resultado | Evidencia / interpretación |
|---|---|---|
| Gobierno vigente | PASS CON OBSERVACIONES HISTÓRICAS | CLAUDE, PROGRESS y ACADEMIC_BASELINE registran F29/F30/F31; README vigentes actualizados, M01/L01/L02 resueltos sin reescribir historia |
| Baseline funcional | PASS | RF-01..RF-27, 27 fichas; RF-28/RF-29 separados |
| RF-23 | PASS | Decisión humana del Aprobador/Dirección, confirmación/justificación; ranking no selecciona |
| CU académicos | PASS | CU-01..CU-20; CU-18 humano; CU-21 diferido |
| Auditoría RF-27 | PASS | Transversal C13 / UC-RF27, no un CU-21 inventado |
| RNF | PASS CON LÍMITES | 10 académicos; RNF-06 y RNF-07 NO VERIFICADOS; RNF-D PROPUESTO; no forzar equivalencia 1:1 con los técnicos |
| Exclusiones | PASS | No promoción de RF-28, RNF-C o IA de selección; OUT-04/OUT-05/OUT-11 preservan las fronteras de F30 |
| Datos institucionales | PASS CON LÍMITES | AS-IS preliminar; TO-BE propuesto; no aprobación institucional ni beneficios medidos |

Fuentes activas: [CLAUDE](../../../CLAUDE.md), [PROGRESS](../../PROGRESS.md), [baseline académico](../ACADEMIC_BASELINE.md), [deuda de gobierno](../GOVERNANCE_DEBT.md), [RF](../practica-06/F6_Requerimientos_Funcionales_Colegio_Andino.md), [RNF](../practica-07/F7_Requerimientos_No_Funcionales_Colegio_Andino.md) y [CU](../practica-08/F8_Diagrama_Casos_de_Uso_Colegio_Andino.md). ADR-003 distingue el CSS 3D implementado de la promoción pendiente de RNF-C; el cuerpo inicial sigue siendo historia, no una obligación actual de WebGL.

## 4. Arquitectura y seguridad

El [F11 oficial](../practica-11/F11_Arquitectura_del_Sistema_Colegio_Andino.md) regularizado mantiene CMP-01..CMP-17 ↔ C01..C17 y R-01..R-20. El F11 adaptado permanece histórico; F32-M01 trata la receta de regeneración, no pérdida ya ocurrida. F9 publicado y F23 histórico no se modifican.

Arquitectura: **monolito modular** Laravel 13/PHP 8.4, React 19/TypeScript/Inertia/Tailwind-shadcn; PostgreSQL 17, Redis 7, Docker/Compose. Cliente-servidor y capas son características complementarias. El servicio FastAPI operacional es opcional; no convierte todo el sistema en microservicios. No se declara PostgreSQL RLS implementado.

| Frontera | Contraste con implementación |
|---|---|
| Multitenencia | `organization_id`, scopes y Policies; AuthorizesAssessmentSessions exige organización compartida y rol/asignación |
| Ranking | RankingService calcula/ordena, servicio puro sin cambios de estado; no es ML que recomiende candidatos |
| Decisión | FinalDecisionService registra la decisión de una persona, candidata finalista de la misma vacante/organización; no elige por el primer puesto |
| Selección/cierre | Responsabilidades C10 y C11 separadas; registro de decisión no cambia etapas por sí mismo |
| CV | Disco local privado `storage/app/private`, autorización del flujo de aplicaciones; no nube productiva inventada |
| Auditoría | Trigger `audit_logs_append_only` protege UPDATE/DELETE con la excepción documental de nulificación de actor; no se exige rediseño |
| ML actual | Checkpoint operativo, 15 features sin IDs/PII; cliente valida contrato y falla sin interrumpir reclutamiento; no persiste decisión ML |

Muestreo: [RankingService](../../../app/Services/Ranking/RankingService.php), [decisión](../../../app/Services/Selection/FinalDecisionService.php), [Policy de evaluaciones](../../../app/Policies/EvaluationPolicy.php), [autorización compartida](../../../app/Policies/Concerns/AuthorizesAssessmentSessions.php), [cliente ML](../../../app/Services/Ml/MlRiskClient.php) y [servicio operacional](../../../app/Services/Ml/OperationalRiskService.php).

[ARQ-01 vigente](../powerdesigner/exports/ARQ-01_Arquitectura_Conceptual.png): 17 componentes, 6 agrupaciones conceptuales y 20 relaciones materializadas en 24 dependencias, sin componente C18. Las flechas muestran dependencias, no todas son la dirección temporal del workflow: R-08 C08 → C07 no contradice que una postulación se evalúe. C09 apoya C10; C10 humano; C17 se relaciona solo vía R-19/R-20, no con C09/C10/C11. No hay R-21 ni renumeración.

F3/F5/F8/ARQ formalizados y conservados; ver [validación PowerDesigner](../powerdesigner/F29_VALIDATION.md). Los findings aceptados F5 TB-30/TB-F1 desconectados, MT-02 de herramienta y F8 CU-16 por especificación no son PASS limpio universal ni fallos funcionales abiertos.

## 5. Trazabilidad transversal

Se cruzó el catálogo CSV de CP con las fuentes `m_cu.CU` y `m_arch.COMPONENTES`. Resultado: RF 27/27, CU 20/20. RF-27 es transversal, no falta de cobertura por no tener CU académico propio. Componentes de interfaz/autorización/persistencia soportan el conjunto aunque no dupliquen todos los RF en sus filas.

La tabla lista **CP representativos**, no toda la cobertura. El [CSV completo](../casos-prueba/F29E_Casos_de_Prueba.csv) contiene cada correspondencia y su evidencia; la [matriz F29E](../casos-prueba/F29E_Matriz_Trazabilidad.md) y [trazabilidad F11](../trazabilidad/F11-architecture-traceability.md) completan RNF/alcance/artefacto. RF-04 comparte CU-03 y RF-11 comparte CU-09: no son duplicaciones de requisito.

| RF | CU académico | Componentes explícitos | CP representativos |
|---|---|---|---|
| RF-01 | CU-01 | C04 | CP-001, CP-079 |
| RF-02 | CU-02 | C04 | CP-003, CP-079 |
| RF-03 | CU-03 | C04 | CP-004, CP-080 |
| RF-04 | CU-03 | C04, C12 | CP-006, CP-080 |
| RF-05 | CU-04 | C05 | CP-008, CP-081 |
| RF-06 | CU-05 | C05 | CP-010, CP-081 |
| RF-07 | CU-06 | C05 | CP-011, CP-081 |
| RF-08 | CU-07 | C02 | CP-012, CP-082 |
| RF-09 | CU-08 | C06, C15 | CP-014, CP-082 |
| RF-10 | CU-09 | C07 | CP-016, CP-082 |
| RF-11 | CU-09 | C07, C12 | CP-017, CP-082 |
| RF-12 | CU-10 | C07, C15 | CP-019, CP-083 |
| RF-13 | CU-11 | C07 | CP-022, CP-083 |
| RF-14 | CU-12 | C07 | CP-023, CP-083 |
| RF-15 | CU-12 | C07, C12 | CP-021, CP-083 |
| RF-16 | CU-13 | C08 | CP-025, CP-090 |
| RF-17 | CU-13 | C08, C12 | CP-027, CP-090 |
| RF-18 | CU-14 | C08 | CP-029, CP-090 |
| RF-19 | CU-15 | C08 | CP-030, CP-084 |
| RF-20 | CU-16 | C05, C08, C09 | CP-031, CP-084 |
| RF-21 | CU-17 | C09 | CP-038, CP-085 |
| RF-22 | CU-17 | C09 | CP-041, CP-085 |
| RF-23 | CU-18 | C10 | CP-042, CP-086 |
| RF-24 | CU-19 | C11 | CP-044, CP-087 |
| RF-25 | CU-20 | C11 | CP-045, CP-087 |
| RF-26 | CU-20 | C11, C12 | CP-047, CP-087 |
| RF-27 | Transversal / UC-RF27 | C13 | CP-048, CP-088 |

La cadena termina en [evidencia QA](../qa-final/F29F_Ejecucion_QA.md) y en el [informe F29H](../informe-final/F29H_Informe_Final_v1_Colegio_Andino.md). La pertenencia de cada prueba ejecutada a CP y los recuentos reales se contrastan por `validate.py`; no se equipara cobertura de requisitos con cobertura de código. ML-FEAT es un catálogo operacional separado, no nuevos RF/CU del baseline.

## 6. QA e informe final

| Control | Resultado contrastado | Alcance temporal |
|---|---|---|
| CP | 128: 124 automatizados, 4 manuales | Catálogo F29E vigente |
| Estados CP | 121 APROBADO + 1 CI aprobado en develop con OBS main histórica + 2 OMITIDO + 1 manual histórico + 3 NO EJECUTADO | No inventar ejecución de los manuales |
| PHPUnit | 411 passed, 8 skipped, 1498 assertions; JUnit 419 casos | Evidencia F29F del commit `bc44303d307004de494c4e03f3186ee190118c4c` |
| Cypress | 20 specs, 85/85 | Registro F29F |
| Vitest | 42/42 | Registro F29F |
| pytest | 533/533 | Registro/JUnit F29F |
| TypeScript / build | PASS; aviso informativo Fontaine | Registro F29F, no afirmar cero avisos |
| Docker Compose | PASS | Validación de configuración registrada, no SLA productivo |
| Defectos F29G | 31 registros, 29 cerrados, 2 abiertos en aquel snapshot | Estilo y CI main histórica; ninguno crítico/alto funcional |
| Cobertura de código | NO MEDIDA | CI también configura `coverage: none` |

Los 8 skips son de verificación de correo desactivada; no se ocultaron como passed. RNF-05/08/09 conservan evidencia parcial/observaciones, RNF-06/07 NO VERIFICADOS. La plantilla de pruebas del curso prevalece sobre referencia PMO y ejemplo externo; aprobaciones/firma quedan pendientes, no atribuidas a la institución.

[F29H](../informe-final/F29H_Informe_Final_v1_Colegio_Andino.md) es un snapshot v1 de 30/09/2026: 14 capítulos, 53 secciones y apartados finales (87 títulos de plantilla), PDF de 28 páginas validado. Códigos de alumno «Pendiente», ausencia de beneficios medidos y trabajo F30+ futuro son límites explícitos. No es falso por no narrar fases posteriores a su fecha; F32 proporciona el contraste actual. Su README incorpora ahora el cierre auditado y preserva la fecha del snapshot: F32-L01 resuelto.

## 7. F30, ciencia, legal y herramientas

La investigación conserva 107 fuentes citadas y registros de verificación, 89 fichas científicas, 30 decisiones propuestas y 49 herramientas. La validez de DOI/URL/metadata no transforma abstracts en evidencia local de eficacia. Claims fuertes se acotan al caso actual y se mantiene evidencia en tensión; no hay autorización científica para puntuar/recomendar candidatos con los datos presentes.

F30 respalda entrevista estructurada, rúbricas, procedencia y revisión humana; fairness no se declara medida, human+AI no garantiza mejora y predicción docente limitada no es una métrica de este sistema. No se propone LLM como juez, inferencia emocional/de personalidad ni biometría. Audio por defecto no; cualquier excepción exige necesidad, base legal y G0.

G0 sigue **PROPUESTA / NO APROBADA**. ADR-001 y contrato 4 prevalecen. El [plan F30](../investigacion-ia/F30_Recomendaciones_F33_F40.md) exige ratificación/enmienda explícita, revisión jurídica/impacto, análisis de datos, requisitos candidatos y dependencias autorizadas. DS 115-2025-PCM/Ley 29733 requieren aplicación jurídica al caso concreto; F32 no certifica cumplimiento. Se contrastó el calendario europeo con el [texto oficial 2026/1744](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX%3A32026R1744), no se reutilizó una fecha secundaria como conclusión definitiva.

Las clasificaciones RECOMENDADO/SANDBOX/NO NECESARIO/EVITAR son recomendaciones de investigación. Licencias, CVEs, owners y compatibilidad son snapshots: no implican instalación autorizada ni ausencia futura de vulnerabilidades. La precisión F30 de PyMuPDF distingue opciones de licencia; `organization_id` permanece contexto Laravel y no se añade al contrato RF-29.

## 8. Deuda F31

| Deuda | Estado verificado F32 | Resultado |
|---|---|---|
| H-14 F4 | RESUELTA | Validación del texto PDF «Asignatura: Pruebas y Calidad de Software» pasa |
| F28-L01 cabecera histórica | NO APLICA | Limitación de extracción no equivale a ausencia visual; no regenerar histórico |
| F29-L01 metadata local | ACEPTADA | No se presentó falsamente como eliminada; no afecta rutas relativas de scripts |
| F29-L02 ARQ etiquetas | RESUELTA | Inspección del PNG actual: R-06/R-07/R-08 diferenciadas y etiquetas separadas de cajas/bordes |
| F29B-OBS-01 composite editor | ACEPTADA | Detalles y exports completos; no pérdida de objetos |
| Pint / vp check | FUTURA | Deuda de formato, no test/build roto; no churn masivo en F32 |
| Lector real / hardware modesto / manual 375 px | FUTURA | No atribuir validación no ejecutada |
| Fontaine / F23–F24 / position | ACEPTADA según registro | No son autorización productiva ni promoción de RNF |

El [registro F31](../F31_DOCUMENTATION_DEBT_CLEANUP.md) conserva la primera corrección visual insuficiente y la corrección posterior auditada. F32-M01 detectó una instrucción residual no saneada y ahora está resuelto por protección del dispatcher y recetas oficiales, no solo por integridad de hashes. No se reabrieron ni alteraron los fixes y artefactos F31.

## 9. Git, CI y release

| Referencia | SHA completo |
|---|---|
| develop / origin/develop / HEAD base F32 | `70f4fcde47f81087024eefe60b6d42b45177cfef` |
| main / origin/main | `3f342ab22c8ff65d4e004cfcaaab041198376b9d` |
| Árbol de main/develop | `b1babd6be7dd85cfb9865e5d51912b51dcf06282` |
| v1.0.0-academic, peeled | `9a946c202ef7473230e8efa371ace13479ab889c` |
| v1.1.0-academic, peeled | `634f354ca7343d8e7cd9735bd0ba3e1d9c4e6d99` |
| F31 A | `99aa4bc972d57b0b67e44cd1b7f8a9dd346f5095` |
| F31 B | `359122e8589e0d2e2ba7b5d0de13ad111e7013d7` |
| F31 C | `711968837cc608461533a18e99555852331443dd` |

CI del baseline auditado comprobada por SHA, no por el nombre de rama solamente:

- develop: workflow `tests`, [run 37173452329](https://github.com/luivmz/saas-reclutamiento-multiempresa/actions/runs/37173452329), SHA `70f4fcde...`, completed/success, actualizado `2026-10-04T03:14:53Z`.
- main: workflow `tests`, [run 37173609859](https://github.com/luivmz/saas-reclutamiento-multiempresa/actions/runs/37173609859), SHA `3f342ab2...`, completed/success, actualizado `2026-10-04T03:18:11Z`.

El [workflow](../../../.github/workflows/tests.yml) corre PHPUnit/TypeScript/build. No corre la totalidad de Cypress/Vitest/pytest. Se conservaron ramas y merges; la auditoría no publicó la rama F32. El cierre posterior autorizado exige verificar CI del nuevo merge develop antes de avanzar a main y CI del nuevo merge main para terminar. No se presentan las ejecuciones del baseline como checks de commits futuros.

[Release v1.1](https://github.com/luivmz/saas-reclutamiento-multiempresa/releases/tag/v1.1.0-academic), id `397073336`: publicado `2026-09-26T04:03:29Z`, no draft ni prerelease; título esperado. Body sin enlaces `file://` ni rutas locales C:/D:. La API expone estos digests, coincidentes con los assets canónicos del repositorio:

| Asset | Bytes | SHA-256 |
|---|---|---|
| F9 DOCX | 2576008 | `ee288eb237dfd26af10820784b146ffeb8d93df02e40c6e0741b1546430627a5` |
| F9 PDF | 2099904 | `a0ffc2917bfd790365c64a0d14460dd3e1b2050fca9702dcd6b48d98312068af` |

No se descargaron y hashearon nuevamente los assets remotos: la comparación usa el digest publicado por GitHub y la evidencia local validada. Que main contenga fases académicas posteriores no mueve el tag v1.1; el tag conserva su cierre técnico.

## 10. Validaciones y alcance final

| Comprobación ejecutada | Resultado |
|---|---|
| `python -B docs/academico/tools/f27b/validate.py` | 0 fallas; F11-R 16/16 PASS |
| Mismo validador `--cierre-f29` | 0 fallas; cierre ADMITIDO con OBS main histórica explícita |
| `python -B docs/academico/tools/f30/validate_f30.py` | OK; 107 fuentes/citas, 30 decisiones, 49 herramientas |
| `python -B docs/academico/powerdesigner/scripts/validate_f29.py` | 225 correctas, 0 fallas |
| `python -B -m unittest discover -s docs/academico/tools/f27b -p test_f32_safety.py` | 10/10 PASS; mocks sin regenerar entregables; F11 adaptado intacto |
| Enlaces locales académicos | 798 referencias; 0 rotos tras las correcciones (791 en la auditoría inicial; 747 antes de F32) |
| MANIFEST, árbol de trabajo | 61 referencias / 61 archivos únicos; 0 discrepancias |
| Evidencias de prácticas | 121 referencias / 91 archivos únicos; 0 discrepancias |
| `git diff --check` | PASS; comprobar también texto nuevo no rastreado |

Integridad ejecutada con el helper read-only de QA ya existente fuera del repositorio, sin incorporarlo como dependencia ni usar opciones de escritura. Convención SHA textual normalizada LF; hashes binarios directos. Los nuevos informes no se agregan al manifiesto de artefactos PowerDesigner, porque no son modelos/exports/capturas ni documentos generados de ese paquete.

El delta inicial F32 fueron cuatro Markdown nuevos. La corrección autorizada añade cambios al dispatcher, pruebas, README vigentes, SHA del README PowerDesigner en MANIFEST y excepciones de alcance de los validadores. Estas excepciones exigen rama/base exactas, expiran al confirmar o cambiar de rama y no permiten binarios ni runtime. No hay modificación de ML, RF/CU/RNF, fuentes oficiales, F9, F23, modelos, exports, documentos históricos, tags o release. En la auditoría los informes y helpers nuevos estaban sin staging; el cierre autorizado incorpora todo el delta en un único commit.

## 11. Recomendación de integración

La propuesta inicial de separar commits queda sustituida por la autorización explícita del usuario: **un único commit** `docs(academic): add F32 global audit and F33 readiness safeguards` con todo el delta auditado. F32 está **CERRADA CON OBSERVACIONES**. Publicar la feature, integrar `--no-ff` en develop, verificar CI verde, integrar `--no-ff` develop en main y verificar CI verde. Detenerse si falla un gate. Los hashes y resultados finales se consultan en Git/GitHub, no se inventan ni se autorreferencian aquí. No crear tags/releases ni borrar ramas. M01/L01/L02 están resueltos y comprobados; las observaciones aceptadas/futuras se conservan. F33 está **APTO PARA DISEÑO** con ADR-005 y seis condiciones G0; no como implementación ya aprobada. G0 sigue **NO APROBADA**.
