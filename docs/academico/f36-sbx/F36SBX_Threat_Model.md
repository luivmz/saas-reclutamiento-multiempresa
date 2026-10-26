# F36-SBX — Threat model de la inteligencia sobre evidencia

> Fase F36-SBX, versión 1 (26/10/2026). Candidata a auditoría independiente. Extiende el [modelo de F34A](../g0-readiness/F34A_Modelo_de_Amenazas.md), aceptado por el equipo (G0-09), y el de [F35-SBX](../evidencia-sbx/F35SBX_Threat_Model.md). **No reemplaza ninguna de sus amenazas** y solo vale para el sandbox sintético.

## Alcance

Cubre lo que F37-SBX podría hacer si el gate se supera: las capacidades ALLOWED y CONDITIONAL de la [matriz](F36SBX_Matriz_Capacidades.md). También cubre las capacidades BLOCKED **solo** para fijar el control que las mantiene bloqueadas. En F36-SBX los controles están diseñados, no implementados; la verificación de F36-SBX es la de [`validate_f36sbx.py`](../tools/f36sbx/validate_f36sbx.py).

## Amenazas

| ID | Amenaza | Relación | Riesgo | Control | Fail-closed |
|---|---|---|---|---|---|
| TEI-01 | Entrada de datos reales o de PII real en el corpus o en los fixtures | T-23, TSB-01 | Crítico | Fuentes cerradas del contrato, seis marcadores, guardia EI-05 y revisión del manifiesto | Un marcador ausente, una coincidencia de PII o una fuente no listada: se rechaza el artefacto entero |
| TEI-02 | PII o texto de evidencia en logs, manifiestos o mensajes de error | T-13 | Alto | Los manifiestos guardan identificadores y hashes, nunca texto. Los errores nombran la regla, no el contenido | Un manifiesto con texto libre es inválido |
| TEI-03 | Prompt injection o document injection: instrucciones incrustadas en un documento | T-19 | Alto | Ningún componente interpreta el texto como instrucción: los LLM están BLOCKED (EI-16) y los métodos son deterministas o de similitud. Los casos `adversarial_case` exigen que la salida no cambie de forma | Si una instrucción incrustada altera el método, la ruta o el formato de salida, la ejecución falla |
| TEI-04 | Contenido malicioso en documentos: PDF malformado, DOCX como bomba ZIP, entidades XML, scripts embebidos | T-22, T-24 | Alto (solo EI-11) | Proceso aislado, límites de bytes, páginas, entradas ZIP y tiempo, sin resolver entidades externas y sin ejecutar contenido activo | Al superar un límite o fallar el análisis, el documento se rechaza sin salida parcial |
| TEI-05 | Fuga entre organizaciones o entre postulaciones | T-10, TSB-02 | Crítico | Un índice por organización sintética y postulación; ninguna consulta abarca dos | Un fragmento de otra postulación en la salida: la ejecución falla |
| TEI-06 | Envenenamiento del corpus o de las anotaciones de oro | T-07, T-20 | Medio | Generador versionado con semilla, manifiesto SHA-256, doble anotación y acuerdo medido | Un hash distinto al del manifiesto sellado invalida la evaluación |
| TEI-07 | Fuga criterio → evidencia: la plantilla copia el texto del criterio y la búsqueda acierta por construcción | Hallazgo del [contrato §2](F36SBX_Contrato_Evidencia.md#2-qué-se-reutiliza) | Medio | Estratos de solapamiento léxico; métricas por estrato | Un estrato `nulo` con solapamiento de términos del criterio se rechaza |
| TEI-08 | Contaminación entre `dev` y `test` | F34 leakage | Alto | Partición por familia de plantilla y vacante, `test` sellado antes de ejecutar, umbrales fijados en `dev` | Un artefacto en dos particiones, o un `test` modificado después del sellado, invalida la evaluación |
| TEI-09 | Alucinación: un texto en la salida que no existe en la fuente | [S34] | Alto | La salida es solo `fragment_id` con offsets; no hay texto generado (EI-13 y EI-16 BLOCKED) | Si el texto de un fragmento no coincide byte a byte con la fuente en sus offsets, la ejecución falla |
| TEI-10 | Afirmaciones sin respaldo: salidas sin cita o con una cita que no corresponde | [S55] | Alto | Cada salida lleva `source_ref`, offsets, `criteria_version` y hash | Si falta un campo o no se verifica, la salida se descarta |
| TEI-11 | Bypass de la abstención: devolver siempre algo aunque no haya evidencia | [S70] | Alto | Umbral fijado en `dev` y casos sin evidencia relevante en `test` | Si un caso sin evidencia no produce abstención, la regla de evaluación falla |
| TEI-12 | Pérdida de procedencia entre artefacto, fragmento y salida | TSB-04 | Alto | Cadena de provenance del contrato §5 | Un eslabón no verificable descarta la salida |
| TEI-13 | Sesgo de automatización y anclaje | [S63, S84] | Alto | Las ayudas solo se muestran después de la calificación humana y se registra si la persona las vio antes. Sin puntaje visible | Una consulta antes de registrar la calificación se rechaza |
| TEI-14 | Ranking encubierto: ordenar personas por número de fragmentos, cobertura u otro agregado | T-21, TSB-08 | Crítico | La salida es por postulación y sin agregados entre personas. Los campos de ranking están prohibidos por el contrato | Un campo prohibido o un agregado por persona invalida la salida |
| TEI-15 | Inferencias prohibidas, también al reinterpretar una observación humana como inferencia del sistema | CAP-21, ADR-005 §6.7 | Crítico | EI-20 BLOCKED, los campos prohibidos del contrato y `author_kind` obligatorio en las observaciones | Una salida con vocabulario de inferencia prohibida, o una observación sin autor humano, se rechaza |
| TEI-16 | Deriva de modelo o de versión | G0-11 | Medio | `method_version` y hash del artefacto del modelo en cada salida; el modelo se fija por hash | Un hash distinto del registrado detiene la ejecución |
| TEI-17 | Cadena de suministro y artefactos de modelo: dependencias vulnerables, pesos sin verificar, deserialización insegura | T-22, TSB-16 | Alto | Dependencia autorizada con versión, licencia y OSV. Pesos en formato sin código ejecutable, con hash previo. Sin descargas en tiempo de ejecución | Un artefacto sin hash registrado, una descarga o un formato con ejecución de código: falla |
| TEI-18 | Dependencia externa: red, API o servicio en la nube | ADR-005, regla de datos | Alto | Ejecución sin red | Cualquier conexión saliente detiene la ejecución |
| TEI-19 | Agotamiento de recursos: memoria, CPU, disco o tiempo | T-15, T-24 | Medio | Límites por artefacto y por ejecución, y memoria de WSL2 fijada | Al superar un límite, la ejecución se aborta sin resultado parcial |
| TEI-20 | Evidencia adversarial para engañar a la recuperación: repetición de palabras clave, texto invisible, homoglifos | — | Medio | Normalización NFKC, eliminación de caracteres de control y de formato, y casos adversariales en `test` | Un caso adversarial que cambie el resultado más allá de lo declarado se registra como fallo de robustez |
| TEI-21 | Falta de reproducibilidad: hilos, semillas o versiones no fijados | G0-11, TSB-14 | Medio | CPU con hilos fijos, semilla declarada y comparación de hash de salida entre dos ejecuciones | Dos ejecuciones con hashes de salida distintos: la evaluación es inválida |
| TEI-22 | Deriva de alcance: un artefacto sandbox llega al runtime, o el alcance C se habilita en la práctica | TSB-07, F34E | Crítico | Superficies prohibidas (`app/`, `routes/`, `config/`, `database/`, `resources/`, `ml-service/` y los archivos de dependencias) y regla CAP de la matriz | Un cambio en una superficie prohibida, o una capacidad C sin ADR sucesor, hace fallar a `validate_f36sbx.py` |

## Relación con amenazas anteriores

| Amenaza anterior | Tratamiento en F36-SBX |
|---|---|
| T-10 y TSB-02 | TEI-05 |
| T-13 | TEI-02 |
| T-19 (prompt injection futura) | TEI-03 |
| T-20 (poisoning del localizador) | TEI-06 |
| T-21 y TSB-08 | TEI-14 |
| T-22 y TSB-16 | TEI-17 |
| T-23 y TSB-01 | TEI-01 |
| T-24 y T-15 | TEI-19 |
| TSB-07 | TEI-22 |

## Controles que F36-SBX ya verifica

En este incremento, `validate_f36sbx.py` verifica TEI-01 (sin PII en el paquete), TEI-14 y TEI-15 (la matriz bloquea scoring, ranking e inferencias), TEI-17 y TEI-18 (sin importaciones fuera de la biblioteca estándar en `tools/f36sbx`) y TEI-22 (ninguna superficie congelada, productiva ni de dependencias cambia). Los demás controles se diseñan aquí y se prueban en F37-SBX, si el gate se supera.
