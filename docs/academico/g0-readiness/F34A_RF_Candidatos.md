# F34A — Requisitos candidatos del módulo inteligente (G0-15)

> Fase F34A, versión 1.1 (04/10/2026), corregida tras la auditoría F34A. Registro de **requisitos candidatos** para el alcance B y las fases futuras F35–F40. **No son requisitos productivos ni forman parte del baseline.** RF-01 a RF-27 y CU-01 a CU-20 no cambian, y este registro no modifica `docs/v1.1/scope-preliminary.md` ni la matriz de trazabilidad.

## 1. Reglas del registro

- Identificador **RF-CAND-xx**, propio de este registro. No ocupa la numeración RF-28 en adelante.
- Estado de todos los candidatos: **CANDIDATO**. Ninguno se implementa mientras G0 = NO APROBADA y F35–F40 = BLOQUEADAS.
- Promover un candidato al baseline es una **decisión del equipo distinta de G0**, como la pendiente para RF-28 y RF-29 (decisión 11 de `scope-preliminary.md`). Al promoverse recibiría el siguiente número RF libre; F33 propuso reservar RF-32 a RF-36 ([diseño §11](../diseno-inteligente/F33_Diseno_Funcional_Motor_Inteligente.md#11-requisitos-candidatos-propuestos)).
- Ningún candidato del nuevo motor puede puntuar, ordenar, recomendar, filtrar ni descartar personas, ni alimentar RF-21 con un valor calculado por el sistema. El ranking vigente de RF-21, determinista y basado en puntajes humanos, se mantiene sin cambios.
- Sin dependencias nuevas en el alcance B.

## 2. Candidatos

| ID | Requisito candidato | Tema | Alcance | Relación con el baseline (sin reinterpretarlo) | Propuesta F33 | Fase futura | Estado |
|---|---|---|---|---|---|---|---|
| RF-CAND-01 | Gestionar el catálogo de competencias y las rúbricas BARS versionadas por organización | Versionado | B | Extiende RF-05 y RF-06 | RF-32 (cand.) | F35 | CANDIDATO |
| RF-CAND-02 | Registrar la evidencia por criterio con su procedencia (tipo, referencia, autor, fecha y estado), justificación y suficiencia | Provenance | B | Extiende RF-19 | RF-33 (cand.) | F35 | CANDIDATO |
| RF-CAND-03 | Verificar con reglas deterministas la completitud y consistencia del proceso (requisito no evidenciado, evidencia faltante, discrepancia, sesión vencida) | Análisis de evidencia | B | Apoya RF-20 a RF-22 | RF-34 (cand.) | F35 | CANDIDATO |
| RF-CAND-04 | Medir el acuerdo entre evaluadores (ICC) en los criterios con doble calificación | Calidad del proceso | B | Calidad del proceso de RF-19 | RF-35 (cand.) | F35, F39 | CANDIDATO |
| RF-CAND-05 | Registrar anotaciones complementarias de solo inserción que no modifican el resultado | Revisión humana | B | Conserva `AssessmentResultRecorder` de RF-19 | FF-02 de F33 | F35 | CANDIDATO |
| RF-CAND-06 | Registrar cada ejecución de análisis (`analysis_run`) inmutable, con eventos de solo inserción | Eventos de `analysis_run` | B | Relación con RF-27 | RNF-E (cand.) | F35, F38 | CANDIDATO |
| RF-CAND-07 | Permitir que una persona descarte una alerta con motivo registrado, y que el evaluador califique antes de ver cualquier ayuda | Revisión humana | B | Apoya RF-23 y ADR-002 | ADR-005 §8 | F35 | CANDIDATO |
| RF-CAND-08 | Explicar cada alerta por regla, evidencia y versión, y el desglose del ranking RF-21 | Explicaciones | B | Explica RF-21 sin cambiar su cálculo | G0-07 | F37, F40 | CANDIDATO |
| RF-CAND-09 | Auditar las acciones críticas del módulo con `AuditLogger` (usuario e IP según el sistema vigente), con metadatos minimizados: sin texto de evidencia ni PII innecesaria | Auditoría | B | Extiende RF-27 | Diseño F33 §7 | F35 | CANDIDATO |
| RF-CAND-10 | Congelar `criteria_version`, `rubric_version` y `rules_version` al publicar, y registrar el hash canónico de la entrada de cada análisis | Versionado | B | Coherente con A-07 | RNF-E (cand.) | F35 | CANDIDATO |
| RF-CAND-11 | Restringir evidencias, citas y justificaciones por rol **y** organización, con pruebas cross-tenant | Control de acceso | B | Contrato 5; Policies existentes | Diseño F33 §8 | F35, F38 | CANDIDATO |
| RF-CAND-12 | Localizar evidencia en documentos para confirmación humana | Análisis de evidencia | **C (futuro)** | — | RF-36 (cand.) | Solo con G0 APROBADA y un ADR adicional | CANDIDATO (BLOQUEADO) |

**RNF-E (cand.)** de F33 (trazabilidad del análisis: versiones, hash de entrada y procedencia) se conserva como está; RF-CAND-06 y RF-CAND-10 lo concretan.

## 3. Fuera del registro a propósito

- Cualquier score, índice, afinidad, semáforo o recomendación sobre personas (ADR-001, contrato 4).
- Sugerencia de niveles, resúmenes de personas o LLM sobre personas.
- Audio, vídeo, biometría o inferencias de emociones.
- Modelos de idoneidad, desempeño o permanencia.
- Uso de datos reales de candidatos.

## 4. Verificación

`validate_f34a.py` comprueba que todos los candidatos tienen estado CANDIDATO, que su identificador es RF-CAND-xx, que ningún documento de F34A los declara parte del baseline y que los archivos del baseline (`scope-preliminary.md`, matriz de trazabilidad y matriz RF) no cambiaron en esta rama.
