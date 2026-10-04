# F33 — Mapa de habilitación F34–F40

> Fase F33, versión 1 (04/10/2026), **pendiente de auditoría**. Define qué habilita F33 en cada fase siguiente según el estado de G0 ([ADR-005 §9](F33_ADR_005_G0.md#9-puerta-g0)). **Estado vigente: G0 = NO APROBADA.**

## Regla

- **F34:** puede avanzar ya, **solo con datos sintéticos** y gobernanza, sin scoring ni recomendación de personas.
- **F35–F40:** no comienzan sin G0 aprobada. Con G0 **CON RESTRICCIONES**, solo el alcance B. Con G0 **APROBADA**, también el alcance C según su ADR adicional.
- **Siempre bloqueado en este ciclo:** scoring o recomendación de personas, inferencias desde rostro o voz, LLM sobre personas, datos reales, atributos sensibles.
- **Frontera B/C.** El alcance **B** no usa dependencias nuevas ni extrae automáticamente texto de PDF o DOCX: trabaja solo con texto y evidencia **registrados o introducidos por una persona**, y puede buscar o localizar de forma determinista dentro de ese texto. Pertenece al alcance **C** cualquier parsing o extracción automática de PDF o DOCX, el OCR, la extracción automática de CV o documentos, las dependencias nuevas de comprensión documental y la búsqueda semántica o con embeddings.
- **Regla de datos.** F34 trabaja **solo con datos sintéticos**. F33 y G0 **no autorizan datos reales de candidatos**, y el consentimiento por sí solo **no** levanta el contrato 7 ni las restricciones vigentes. Cualquier uso futuro de datos reales exige: (1) autorización explícita del equipo; (2) revisión contractual (contrato 7); (3) revisión jurídica; (4) análisis de privacidad y datos personales; y (5) una aprobación específica posterior, distinta de G0.

## Mapa por fase

| Fase | G0 NO APROBADA (hoy) | G0 APROBADA CON RESTRICCIONES (B) | G0 APROBADA (B + C) | Siempre bloqueado |
|---|---|---|---|---|
| **F34 Dataset y gobernanza** | **HABILITADA:** escenarios sintéticos (vacantes, rúbricas, evidencias y valoraciones simuladas; datos del proceso para E), dataset card, linaje SHA-256, registro, análisis de datos personales en borrador | Igual | + corpus sintético en español para el localizador, con variedad lingüística documentada | Datos reales o «consentimiento» como sustituto de la regla de datos; atributos sensibles reales; etiquetas «contratado» |
| **F35 Pipeline de evidencia** | BLOQUEADA | Rúbricas y catálogo versionados, registro de evidencia y valoración humana (`PROGRAMADA` → registro → `REALIZADA`), anotaciones complementarias, reglas de proceso, ICC, búsqueda determinista sobre texto introducido por personas (CAP-01 a 06, 08, 18, 31, 33, 34); sin dependencias nuevas | + extracción automática de PDF o DOCX, OCR y localizador en sandbox (CAP-07, 09, 20); audio solo si se aprueba aparte (CAP-27) | Sugerir niveles, puntuar, resumir personas |
| **F36 ML baseline** | BLOQUEADA | Solo ML del **proceso**, con datos sintéticos e interpretable (CAP-26); sin cambiar el contrato congelado de RF-29 sin decisión | Ídem; el localizador no se trata como «modelo sobre personas» | Modelos de idoneidad, desempeño o permanencia (CAP-25) |
| **F37 XAI y equidad** | BLOQUEADA | Explicaciones de reglas y del desglose RF-21, equidad de procedimiento, método estadístico probado solo con datos sintéticos (CAP-29, 31, 32 sintético) | + auditoría de sesgo del localizador por nombre y género, con datos sintéticos | SHAP o LIME para usuarios; afirmaciones de equidad sin base legal ni muestra |
| **F38 Integración Laravel↔ML** | BLOQUEADA | Módulo Laravel (migraciones, Policies, auditoría, pruebas cross-tenant) **sin servicio externo** | + integración asíncrona con el servicio: cola, idempotencia, timeout, reintentos, fallback, tokens pseudónimos | Escrituras del servicio sobre ranking, estados o decisión |
| **F39 Evaluación experimental** | BLOQUEADA | Escenarios sintéticos: cobertura de reglas, ICC simulado, tasa de justificaciones válidas, alertas descartadas | + precisión y exhaustividad del localizador por tramo, con datos sintéticos; WER por grupo con audio sintético si se aprobara audio | Afirmar validez predictiva o eficacia sobre candidatos reales |
| **F40 Panel** | BLOQUEADO | Evidencia, rúbricas, alertas, ICC y desglose RF-21; resumen del proceso (relación con RF-28 candidato) | + fragmentos sugeridos, solo tras la calificación | Insignias de «recomendado», semáforos sobre personas, puntajes del sistema |

## Correspondencia con las decisiones de F30

| Decisiones F30 | Tratamiento en F33 |
|---|---|
| D-01 (puerta G0) | ADR-005 §9; resultado NO APROBADA |
| D-02 (sin scoring ni recomendación) | ADR-005 §6; CAP-15 y CAP-16 BLOQUEADAS |
| D-03, D-04, D-05 (competencias, BARS, procedencia) | FF-01, FF-02; diseño §4 y §7 |
| D-06, D-07 (reglas, ICC) | FF-04; CAP-33, CAP-34 |
| D-08 (mantener RF-21) | FF-05; CAP-14 |
| D-09, D-10, D-11 (datos sintéticos, sin sensibles, sin «contratado») | F34; CAP-35, CAP-36 |
| D-12, D-13 (documentos, localizador) | CAP-07, CAP-08, CAP-09; FF-07 FUTURO |
| D-14, D-15, D-16 (audio, inferencias prohibidas) | Diseño §9; CAP-21, CAP-27, CAP-28 |
| D-17 (LLM fuera de la evaluación) | CAP-11, CAP-23 BLOQUEADAS; CAP-24 FUTURA |
| D-18, D-19 (ML del proceso, calibración) | F36; CAP-26 |
| D-20, D-21, D-22 (explicaciones, equidad, anclaje) | F37; diseño §1, §7; FF-02 paso 4 |
| D-23 a D-26 (integración, versionado, auditoría, multiempresa) | Diseño §7, §8, §10; F38 |
| D-27, D-28 (evaluación, auditoría interna) | F39 |
| D-29 (panel sin «recomendado») | F40; FF-05 |
| D-30 (herramientas) | G0-15; ninguna dependencia nueva en F33 |

## Entradas y salidas de cada fase

| Fase | Entrada mínima | Salida mínima para auditar |
|---|---|---|
| F34 | ADR-005 (propuesta) y este mapa | Generador sintético con semilla, dataset card, linaje y análisis de datos personales en borrador |
| F35 | G0 ≥ CON RESTRICCIONES (registro del equipo) | Diseño detallado, pruebas RED/GREEN y regresión completa, pruebas cross-tenant |
| F36 | G0 ≥ CON RESTRICCIONES; datos de F34 | Model card, métricas calibradas, comparación con reglas |
| F37 | F35 | Explicaciones verificables; informe de equidad de procedimiento |
| F38 | F35–F37 | Integración con regresión completa; sin rutas automáticas hacia la decisión |
| F39 | F38 | Informe de evaluación con límites explícitos |
| F40 | F38–F39 | Panel accesible sin veredictos sobre personas |
