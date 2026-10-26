# F36-SBX — Informe de investigación y diseño

> Fase F36-SBX, versión 1 (26/10/2026). Candidata a auditoría independiente. **Sin implementación ni resultados experimentales.** Toda cifra de este informe es una estimación de diseño, rotulada como tal, que F37-SBX tendría que medir.

## 1. Método y nivel de certeza

| Tipo de afirmación | Cómo se marca | Fuente |
|---|---|---|
| Hecho verificado en el repositorio | «verificado» | Git y los documentos enlazados |
| AS-IS | «AS-IS» | Lo que el sistema hace hoy: el registro humano de evidencia (RF-19), el ranking RF-21 y la decisión RF-23 |
| TO-BE propuesto | «propuesto» | Este informe |
| Software implementado | — | F36-SBX no implementa nada |
| Experimental o futuro | «F37-SBX» | Solo si el gate se supera |

**Fuentes.** La base científica es el corpus auditado de F30: 107 fuentes en la [matriz de evidencia](../investigacion-ia/F30_Matriz_Evidencia_Cientifica.md), el [análisis de modelos y técnicas](../investigacion-ia/F30_Analisis_Modelos_y_Tecnicas.md) y el [análisis de herramientas](../investigacion-ia/F30_Analisis_Herramientas_Skills.md). Esta sesión no hizo búsquedas externas nuevas. Las versiones, licencias y avisos de herramientas citados son la fotografía de F30 (septiembre y octubre de 2026) y deben volver a verificarse antes de cualquier uso (FG-10).

## 2. AS-IS

- **Verificado:** la evidencia la registra una persona. RF-19 guarda un puntaje por criterio y A-19 un registro único por sesión. F33 diseñó la cadena de procedencia y F35-SBX la probó con fixtures sintéticos, hashes y un pipeline determinista de doce pasos, sin ML ([cierre global](../evidencia-sbx-cierre-global/F35SBX_Cierre_Global.md)).
- **Verificado:** no existe en el repositorio ningún parser de documentos, OCR, embedding, índice semántico ni LLM. RF-29 es el único modelo y trata el proceso, no a las personas.
- **AS-IS preliminar:** el Colegio Andino es un caso de estudio sin validación institucional (G0-12 PENDIENTE EXTERNO). Ninguna necesidad institucional de estas ayudas está demostrada.

## 3. Tareas potenciales

| Tarea | Qué haría | Valor para el evaluador | Riesgo principal | EI |
|---|---|---|---|---|
| Clasificación documental | Asignar el tipo de documento | Bajo: el tipo ya se declara al registrar | Ninguno con metadatos; con modelo, error silencioso | EI-06 (metadatos) |
| Extracción estructurada | Pasar de texto libre a campos (formación, fechas) | Medio | Extraer atributos sensibles o *proxies*; errores no detectados | EI-08, EI-11, EI-12 |
| Recuperación de evidencia | Localizar los fragmentos que hablan de un criterio | Alto si el expediente es largo | Anclaje, omisiones silenciosas y sesgo por nombre o género [S11] | EI-07, EI-09, EI-10 |
| Búsqueda léxica determinista | Encontrar términos exactos | Medio y explicable | Bajo; no encuentra sinónimos | EI-07 |
| Recuperación semántica y embeddings | Encontrar paráfrasis | Medio o alto | Opacidad, sesgo [S11, S32] y deriva de versión | EI-10 |
| Resumen con citas | Condensar evidencia | Aparente | Alucinación [S34], sesgo [S83, S87] y anclaje [S84] | EI-13 (BLOCKED) |
| Comparación contra criterios | Decir si la evidencia «cumple» | — | Es sugerir niveles: scoring | EI-14 (BLOCKED) |
| Trazabilidad | Comprobar que cada enlace evidencia → criterio es íntegro | Alto y explicable | Bajo | EI-03 |
| NER | Detectar instituciones, títulos y fechas | Bajo o medio | Detectar entidades de persona | EI-12 |
| Guardia de PII | Impedir que entre texto con datos personales | Alto como control | Falsos negativos | EI-05 |

## 4. Comparación de enfoques

| Enfoque | Datos que necesita | Explicabilidad | Reproducibilidad | Dependencias | Encaje con los contratos | Uso propuesto |
|---|---|---|---|---|---|---|
| Reglas y determinismo | Ninguno | Total | Total | Ninguna (biblioteca estándar) | Total (alcance B) | Base de F37-SBX-A: EI-01 a EI-07 |
| IR clásico (BM25, TF-IDF) | Corpus sintético y anotación de relevancia | Alta: términos coincidentes | Total si se fija la tokenización | Ninguna: se implementa con la biblioteca estándar | Frontera B/C (F36-M02) | EI-09, línea base obligatoria de cualquier método semántico |
| Modelos pequeños locales (bi-encoder de oraciones) | Anotación de relevancia para evaluar, no para entrenar | Media: la similitud es opaca | Alta con pesos fijados por hash y CPU determinista | sentence-transformers y PyTorch (F30: EVALUAR EN SANDBOX) | Alcance C (CAP-09) | EI-10, solo si supera a BM25 por un margen declarado antes |
| Transformers grandes o cross-encoders | Ídem | Baja o media | Media | Pesada | Alcance C | No se propone: no es proporcional para un corpus pequeño |
| LLM | Ninguno para usarlo, mucho para validarlo | Baja | Baja | Pesada | Incompatible con personas (CAP-11, CAP-23) | BLOCKED (EI-16 y EI-17) |
| Híbrido (léxico y luego semántico) | Ídem | Media | Alta | Las del semántico | Alcance C | Variante de EI-10, solo si EI-10 se autoriza |

**Regla de escalera (propuesta).** Un método más complejo solo se propone si el más simple falla en un umbral **declarado antes de medir**, en el mismo conjunto de prueba sellado: reglas → BM25 → bi-encoder pequeño → híbrido. Si BM25 alcanza el umbral, EI-10 no se pide. Así se evita la complejidad que no se ha justificado (proporcionalidad, G0-13).

## 5. Viabilidad de hardware

PC secundaria declarada por el equipo: Intel Core i5-10400F (6 núcleos y 12 hilos), 16 GB de RAM, NVIDIA GTX 1660 SUPER con unos 6 GB de VRAM, Windows 11, WSL2 con Ubuntu 24.04, Docker Desktop y Python 3.12. **No se midió nada en esta sesión.** Las cifras siguientes son órdenes de magnitud de diseño.

| Enfoque | Memoria estimada | Tiempo estimado (corpus ≤ 10⁴ fragmentos) | GPU | Viabilidad |
|---|---|---|---|---|
| Reglas, búsqueda exacta y PII | Decenas de MB | Milisegundos por consulta | No | Viable |
| BM25 o TF-IDF con la biblioteca estándar | Decenas a cientos de MB | Milisegundos por consulta; indexado en segundos | No | Viable |
| Bi-encoder pequeño (del orden de 10⁷ a 10⁸ parámetros) en CPU | Del orden de 1 GB, con el runtime | Minutos para codificar el corpus; consultas en milisegundos | Opcional | Viable en CPU |
| Cross-encoder de reordenamiento | Similar | Un coste por par: crece con el número de candidatos a reordenar | Opcional | Posible, pero no se propone |
| LLM de 7 a 8 B cuantizado a 4 bits | Cerca del límite de 6 GB de VRAM, con poco margen para el contexto | Segundos por respuesta | Necesaria | Al límite. Además BLOCKED |

**Decisiones de diseño derivadas:**

1. **CPU primero.** La línea base reproducible corre en CPU, con hilos fijados y semillas declaradas. La GPU solo serviría para comparar latencia, nunca para producir el resultado de referencia.
2. **GPU sin núcleos tensoriales.** La familia GTX 16 no los tiene, así que la precisión mixta no obtiene la aceleración que esos núcleos dan en otras GPU. Si alguna vez se usa la GPU, se prefiere FP32. F37-SBX debe medir el comportamiento en FP16 antes de usarlo.
3. **Memoria compartida.** Docker Desktop y WSL2 compiten con el host por los 16 GB. F37-SBX debe fijar en WSL2 un límite de memoria explícito y medir el pico de cada ejecución (plan de evaluación, métrica R-03).
4. **Sin descargas implícitas.** Ningún modelo se descarga en tiempo de ejecución: un artefacto se registra antes con su hash SHA-256, su licencia y su origen (TEI-17).

## 6. Arquitectura conceptual propuesta para F37-SBX

Solo diseño. Sigue la forma de F35-SBX-B: herramientas académicas fuera del runtime.

```
fixtures sintéticos (contrato F36-SBX v1, sellados por manifiesto)
  → guardia de entrada: marcadores synthetic-only, PII y tamaños (falla cerrado)
  → índice por postulación (organización sintética + postulación; nunca global)
  → consulta iniciada por el evaluador simulado, después de su calificación
  → fragmentos con cita, fuente, offsets y versión; sin puntaje visible
  → abstención explícita si nada supera el umbral
  → manifiesto de ejecución (versiones, hashes de entrada y salida, semilla)
```

- Vive en `docs/academico/tools/f37sbx*/`, o donde lo fije la autorización de F37-SBX. Sin servidor, red, base de datos productiva ni cambios en `app/`, `routes/`, `config/`, `database/`, `resources/` o `ml-service/`.
- Tenant: cada índice pertenece a una sola organización sintética y a una sola postulación. Una consulta entre postulaciones es imposible por construcción (TEI-05).
- Salida cerrada: lista de fragmentos `{fragment_id, source_ref, offsets, criteria_version, method_version}`, sin campo de puntaje, orden por candidato ni texto generado.

## 7. Propuesta para un ADR sucesor (alcance C solo sintético)

**Estado: PROPUESTA de F36-SBX, sin número de ADR asignado.** El número lo fija el equipo. F36-SBX no lo aprueba ni lo da por aprobado.

- **Contexto.** ADR-005 §6.4 abre el alcance C solo con la G0 real APROBADA y un ADR que enmiende ADR-001. La G0 real está NO APROBADA y depende de pendientes externos (G0-02, G0-03 y G0-12).
- **Decisión propuesta.** Permitir, **solo en el sandbox académico y con datos 100 % sintéticos**, el estudio de EI-08, EI-10, EI-11, EI-12 y EI-24, bajo el F36-SBX-GATE y con todas las prohibiciones del [charter](F36SBX_Charter.md#4-prohibiciones-duras).
- **Lo que no cambia.** El alcance C del producto sigue BLOQUEADO. ADR-001, ADR-002, el contrato 4 y ADR-005 no se enmiendan para producción. No se autorizan datos reales, despliegue ni salida hacia RF-21, RF-23 o RF-29.
- **Revocación.** Cualquier incidente de la sección 7 del charter, o cualquier resultado que dé apariencia de puntuar personas, revoca la excepción.
- **Alternativas.** (a) No estudiar C hasta la G0 real; es la opción por defecto si el equipo no aprueba el ADR. (b) Estudiar solo EI-11, sin semántica.

## 8. Limitaciones

- El valor para un evaluador real no puede demostrarse con datos sintéticos. Lo que se mide es el comportamiento del método sobre un oráculo sintético.
- Un corpus sintético en español no tiene la variedad lingüística de expedientes reales. Las métricas no se extrapolan.
- Las anotaciones de relevancia del oráculo las haría el propio equipo: hay riesgo de circularidad, que se mitiga con doble anotación y acuerdo medido (plan de evaluación, A-01).

## 9. Hallazgos de diseño

| ID | Severidad | Hallazgo | Tratamiento |
|---|---|---|---|
| F36-M01 | MEDIUM | El mapa F33 llama «F36» al ML baseline del proceso, y F36-SBX trata otro objeto | Divergencia declarada en el [charter §5](F36SBX_Charter.md#5-divergencia-con-el-mapa-f33). El equipo confirma la numeración antes de F37-SBX (FG-03) |
| F36-M02 | MEDIUM | No está resuelto si ordenar fragmentos por relevancia léxica (EI-09) cabe en el alcance B | EI-09 queda CONDITIONAL hasta una confirmación escrita del equipo |
| F36-M03 | MEDIUM | El alcance C sintético exige un ADR sucesor que excepcione ADR-005 §6.4 en el sandbox | Sin ese ADR APROBADO, F37-SBX-B no puede empezar (FG-12) |
| F36-L01 | LOW | La autorización de inicio de F36-SBX consta como instrucción transcrita en la sesión, sin adjunto firmado | No afecta al diseño. FG-03 exige para F37-SBX un registro fechado con quórum |
| F36-L02 | LOW | Los datos de herramientas son la fotografía de F30 | Se vuelven a verificar en FG-10 antes de usarlos |
| F36-L03 | LOW | En la PC de esta sesión, con Pillow 13.0.0 en un entorno temporal, la regeneración de los PNG de F29C y F33 no reproduce los mismos bytes. Ocurre ya sobre `main`, antes de F36-SBX | Ambiental y anterior a F36-SBX. Se registra; no se corrige aquí |
