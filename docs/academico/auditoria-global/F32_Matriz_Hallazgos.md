# F32 — Matriz de hallazgos

Baseline: `70f4fcde47f81087024eefe60b6d42b45177cfef`. Severidad aplicada al estado académico/documental, no a vulnerabilidades hipotéticas ni a fases futuras todavía no implementadas.

| ID | Severidad | Estado | Área | Consecuencia |
|---|---|---|---|---|
| F32-M01 | MEDIUM | RESUELTO | Reproducción / preservación histórica | Clave `f11` bloqueada antes de escribir; flujo por defecto y recetas usan el oficial `f11r` |
| F32-L01 | LOW | RESUELTO | Navegación / estado documental | README vigentes distinguen fases cerradas, snapshots históricos y cierre autorizado F32 |
| F32-L02 | LOW | RESUELTO | Handoff Git | Conservación de ramas por defecto; cualquier eliminación exige autorización explícita |
| F32-O01 | OBSERVATION | ACEPTADA / FUTURA según deuda | Verificación no funcional y manual | No existe aceptación productiva ni cobertura de código medida |
| F32-O02 | OBSERVATION | ACEPTADA | PowerDesigner | Metadata local y limitación del editor no equivalen a pérdida de modelo |
| F32-O03 | OBSERVATION | GATE FUTURO NO CUMPLIDO | IA / G0 | Investigación no autoriza evaluar personas ni implementar el motor futuro |
| F32-O04 | OBSERVATION | DISTINCIÓN HISTÓRICA CONFIRMADA | QA / CI / release | CI actual verde no sustituye retrospectivamente ejecuciones históricas |

## F32-M01 — Receta de regeneración no protege el F11 histórico

- **Archivo / ubicación original (baseline auditado):** [MAC_HANDOFF.md](../MAC_HANDOFF.md), línea 147, receta `python3 docs/academico/tools/f27b/build.py f3 f5 f8 f11`; [build.py](../tools/f27b/build.py), líneas 1227, 1309–1310, 1419–1435, 1475–1488 y 1632–1635. Las líneas describen el baseline, no la ubicación después de la corrección.
- **Evidencia histórica:** `F11_STEM` apuntaba al entregable `ADAPTADO`; el cuerpo de `build_f11()` escribía su DOCX y Markdown, COMPONENTS, RELATIONSHIPS, VALIDATION, F28_VALIDATION, trazabilidad y evidencias. El dispatcher permitía esa clave explícita y, sin argumentos, todas las claves. No había guardia que preservara automáticamente el histórico tras F11-R.
- **Reproducción de auditoría:** lectura estática de la receta, del destino `out_docx`, de `build_md(...)` y de los `write_text(...)`. No se ejecutó el generador. El cuerpo histórico incluye «Formato oficial no publicado / no disponible» y vuelve a generar notas H-14 pendiente para F31. Son notas históricas válidas si se conservan congeladas, no si se republican como estado vigente.
- **Impacto:** seguir el handoff actual puede alterar evidencia deliberadamente congelada y reintroducir estados obsoletos. No se observó pérdida actual: los hashes presentes pasan. No es una regresión del runtime.
- **Corrección aplicada:** recetas Mac/PowerDesigner pasan a `f11r`. `resolve_builder_keys()` valida el lote completo antes de ejecutarlo, rechaza `f11` y la excluye del listado por defecto. La llamada directa a `build_f11()` también se rechaza antes de crear diagramas o documentos. Su cuerpo se conserva como fuente histórica no ejecutable. No se regeneró ningún entregable en el repositorio; el builder oficial no cambia.
- **Aceptación verificada:** 10 pruebas de seguridad con mocks prueban rechazo anticipado, llamada directa, exclusión por defecto, selección oficial y expiración de excepciones; el F11 adaptado DOCX/PDF/MD sigue sin diff contra HEAD. Los validadores comprueban el F11 oficial y sus artefactos; manifiesto/evidencias se contrastan sin regenerar históricos. La reproducción DOCX/MD temporal que realizan los validadores mantiene su flujo existente.
- **Estado:** **RESUELTO**. F33 está apta para diseño; no se autoriza G0 ni implementación funcional.

## F32-L01 — Estados editoriales atrasados en entradas de navegación

- **Evidencia histórica (baseline):** [MAC_HANDOFF.md](../MAC_HANDOFF.md), línea 121, marcaba F29C «Lista para auditoría»; [README del informe](../informe-final/README.md), línea 9, mantenía «pendiente de auditoría»; [README principal](../../../README.md), línea 135, describía F31 con el verbo «sanea» y el tramo académico hasta F30. El [baseline activo](../ACADEMIC_BASELINE.md), PROGRESS y el merge F31 acreditaban el cierre posterior.
- **Impacto:** ambigüedad para lectores nuevos; los resultados y binarios históricos no son falsos por conservar su fecha.
- **Corrección aplicada:** MAC_HANDOFF, README principal y README de F29C, plan, CP, QA, métricas e informe final reflejan el cierre auditado/integrado. F32 está CERRADA CON OBSERVACIONES y su integración fue autorizada con gates CI. La CI main pendiente se rotula como observación de aquella ejecución, no como CI actual fallida ni como PASS retroactivo.
- **Aceptación:** entradas vigentes distinguen auditoría ya realizada, versión histórica y trabajo futuro. No se cambiaron DOCX/PDF/MD históricos, registros de respuestas IA, resultados ni fuentes oficiales. **RESUELTO**.

## F32-L02 — Anuncio de limpieza de rama histórica sin decisión

- **Evidencia histórica (baseline):** [MAC_HANDOFF.md](../MAC_HANDOFF.md), línea 12: la rama integrada y conservada «Se limpiará en la F31 o la F32»; otra instrucción conservaba trazabilidad hasta esas fases. La tarea F32 no autoriza borrar ramas.
- **Impacto:** expectativa editorial de una operación no necesaria para cerrar la auditoría. No se ejecutó borrado ni existe pérdida de historia.
- **Corrección / aceptación:** ambas entradas del handoff ahora indican conservación por defecto y autorización explícita para cualquier eliminación local o remota. No se borraron ramas ni se ejecutó limpieza. **RESUELTO**.

## Observaciones no bloqueantes

### F32-O01 — Límites de QA y validación académica

Los 128 CP incluyen 124 automatizados y 4 manuales: CP-125 tiene evidencia histórica F8; CP-126–128 no fueron ejecutados por falta de validación institucional, entorno/SLA de rendimiento y entorno productivo de disponibilidad. RNF-06/RNF-07 continúan NO VERIFICADOS. Cobertura de código: NO MEDIDA. ISO/IEC 25010 es marco, no certificación. Lector real, hardware modesto y revisión manual exacta a 375 px siguen FUTURAS. Mantener esas limitaciones; no sustituirlas por CI verde.

### F32-O02 — Deuda PowerDesigner aceptada con alcance explícito

F29-L01: metadata `RepositoryFilename` local, no una ruta requerida por los scripts. F29B-OBS-01: presentación del composite en editor; detalle y exports preservan objetos. F31 no fingió corregirlas: las marcó ACEPTADAS. F29-L02 sí está resuelta en el export actual. Mantener la distinción; no editar XML histórico por cosmética ni abrir PowerDesigner durante esta auditoría.

### F32-O03 — Investigación y G0 no equivalen a autorización

F30 conserva 107 fuentes citadas con registro de verificación, 30 decisiones propuestas y 49 herramientas evaluadas. El validador comprueba integridad, citas y consistencia, no reproduce una revisión completa de todos los artículos ni otorga dictamen jurídico. La puerta G0 tiene seis condiciones acumulativas; no existe ADR-005 aprobado en el baseline. El plan por fase que menciona impacto «iniciado» no debe interpretarse como cumplimiento de G0-3: prevalece el documento con revisión jurídica exigido en la tabla G0. F33 debe resolver esa condición sin rebajarla.

### F32-O04 — Snapshots de CI y cierre de release

F29F/G preservan la falta de ejecución de main sobre `60ebcb2` en aquella fecha. La CI de main sobre `3f342ab` sí pasó hoy; no es una ejecución retroactiva del commit anterior. GD-04–06 quedaron aceptadas como historia prepublicación en F31. F32 verifica release/tag actuales sin reescribir notas publicadas ni mover etiquetas. La CI `tests` incluye PHPUnit, TypeScript y build, no Cypress/Vitest/pytest completos.

## Verificación de las correcciones

La regresión `test_f32_safety.py` pasó de RED (la llamada directa alcanzaba la generación histórica, interceptada por un mock antes de escribir) a GREEN: **10/10 PASS**. Las excepciones de los validadores se acotan a la rama F32 y al HEAD base aprobado; expiran al confirmar o cambiar de rama. Solo permiten README principal, dos README de navegación protegidos y el hash del README PowerDesigner en MANIFEST, nunca binarios, runtime o modelos.

Se actualizó exclusivamente ese SHA-256 de MANIFEST al cambiar la receta; las evidencias y los artefactos no cambiaron. No se alteraron validaciones semánticas existentes ni se añadieron PASS tautológicos.

## Cierre autorizado y siguiente paso

1. Informe y correcciones M01/L01/L02 aprobados: PASS WITH OBSERVATIONS, APTO PARA COMMIT, sin promover G0 ni modificar producto.
2. Confirmar todo el delta F32 en un único commit y publicar/integrar con gates CI obligatorios de develop y main; detenerse si falla cualquier gate. Hashes y resultados finales en Git/GitHub.
3. Conservar los históricos y las observaciones aceptadas/futuras sin atribuir resultados nuevos.
4. Comenzar F33 como diseño/ADR; la implementación posterior conserva todos los gates G0.

No hay CRITICAL/HIGH/MEDIUM/LOW abiertos en estos hallazgos: M01/L01/L02 **RESUELTOS**. Se mantienen cuatro OBSERVATION; G0 **NO APROBADA**. F33 **APTO PARA DISEÑO**, no para implementación funcional.
