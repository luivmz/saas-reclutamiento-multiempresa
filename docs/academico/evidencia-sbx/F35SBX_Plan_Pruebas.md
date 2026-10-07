# F35-SBX-A — Plan de pruebas

> Fase F35-SBX-A, versión 1 (07/10/2026). Todas las pruebas son mutaciones en memoria sobre los artefactos reales: no escriben archivos, no crean evidencia y no ejecutan ningún pipeline. Las pruebas no viven en `tests/`, que es una ruta protegida.

## 1. Estrategia

1. **TDD.** El validador y sus casos negativos se escribieron antes que los documentos, el contrato y los fixtures.
2. **Doble llave.** El contrato, los hashes, la provenance y el origen F34 se recalculan; nada de lo que declaran los artefactos se da por cierto.
3. **Fail-closed.** Un archivo ausente o ilegible, un JSON mal formado, una palabra clave de esquema desconocida, un error de Git o una excepción inesperada cuentan como falla.
4. **Sin falsos positivos.** Seis frases con negaciones legítimas se insertan en un documento y no deben producir violaciones.
5. **Control no forzado.** Con G0-SBX NO APROBADA y F35-SBX BLOQUEADA en la puerta, el README y el gobierno, los documentos coherentes se aceptan y la regla GATE detiene el trabajo SBX: el validador no supone el estado vigente.

## 2. RED → GREEN

| Momento | Resultado de `validate_f35sbx.py` |
|---|---|
| RED (07/10/2026, antes de crear documentos, contrato y fixtures) | 50 comprobaciones correctas, 94 fallas, código de salida 1. Fallaban documentos y artefactos ausentes, el gobierno con «AÚN NO INICIADA» y el alcance de `validate_f34b.py`, que aún no admitía `tools/f35sbx/` |
| GREEN | 07/10/2026, tras crear documentos, contrato, fixtures, manifest y el registro de apertura en el gobierno: 144 comprobaciones correctas, 0 fallas. Tras DH-10 y DH-11: 233 correctas, 0 fallas. Tras M01, M02 y M03 de la auditoría independiente: 274 correctas, 0 fallas. Tras la segunda reauditoría (normalización Unicode, de guiones, de RF y del nombre en inglés del alcance bloqueado; manifest cerrado por tipos): 319 correctas, 0 fallas. Tras la tercera reauditoría (normalización posterior al Markdown, separadores entre RF y su predicado, JSON sin claves duplicadas, escapes Unicode decodificados): 379 correctas, 0 fallas. Tras la reauditoría final (predicado de un RF envuelto en paréntesis): 409 correctas, 0 fallas. Tras la corrección de envoltorios anidados (hasta 8 capas, fallo cerrado si no son verificables, RF coordinados y saltos de línea): 476 correctas, 0 fallas. Tras el contexto Markdown de la unión de líneas: 504 correctas, 0 fallas. Tras el escáner Markdown compartido (fences por carácter y longitud, bloques HTML, títulos setext, código indentado según CommonMark): 542 comprobaciones correctas, 0 fallas, código de salida 0. Tras los controles de transición de cierre (ciclo de vida INICIADA o CERRADA y ACADEMIC_BASELINE exacto): 657 comprobaciones correctas, 0 fallas, código de salida 0 |

## 3. Regresión (gate local, DH-08)

`validate_f35sbx.py`, `validate_f34e.py`, `validate_f34b.py`, `validate_f34a.py`, `validate_f34.py`, `validate_f33.py`, `validate.py`, `validate.py --cierre-f29`, `validate_f30.py`, `validate_f29.py`, `test_f32_safety.py`, enlaces relativos, MANIFEST de evidencias, hashes de prácticas y `git diff --check`.

## 4. Controles positivos

| Control | Resultado esperado |
|---|---|
| Artefactos reales | Ninguna violación en las 25 reglas |
| Contrato publicado | Idéntico al que construye el validador |
| Control no forzado | Solo GATE informa la detención del trabajo SBX |
| Frases con negación legítima | Ninguna violación en CLM, PHS, STO ni STA |
| Cambios legítimos en las dos carpetas | Ninguna violación de alcance Git |
| Git no disponible, base no ancestral o consulta fallida | Error de Git: falla cerrado |

## 5. Casos negativos

Cada caso debe ser detectado por la regla indicada; el validador comprueba que esta tabla y su catálogo coinciden. Los casos JOIN comprueban la transformación de `join_rf_breaks`: código, bloques HTML, listas, títulos (también setext), citas, tablas, reglas horizontales y líneas en blanco nunca se unen; un fence sin cerrar deja el resto como código y, además, hace fallar DOC. `join_rf_breaks`, `doc_props`, el CLM y las tablas usan el mismo escáner Markdown (`scan_markdown`).

| Caso | Regla | Mutación en memoria |
|---|---|---|
| NS-01 | PII | Número con formato de DNI en el texto |
| NS-02 | PII | Campo `real_name` |
| NS-03 | PII | Dirección de correo en el texto |
| NS-04 | PII | Campo `dni` |
| NS-05 | MED | Campo `cv` con nombre de archivo PDF |
| NS-06 | MED | Nombre de archivo DOCX en el texto |
| NS-07 | MED | Campo `audio_ref` con archivo MP3 |
| NS-08 | MED | Nombre de archivo MP4 en el texto |
| NS-09 | MED | Imagen PNG dentro de `evidencia-sbx/` |
| NS-10 | MED | Bloque base64 en el texto |
| NS-11 | MED | Data URI en el texto |
| NS-12 | MED | Fixture con bytes NUL |
| NS-13 | SYN | `source_type` distinto de `synthetic` |
| NS-14 | SYN | Texto sin el marcador [SINTÉTICO] |
| NS-15 | SYN | `environment` distinto de `sandbox` |
| NS-16 | SCH | Campo desconocido en una evidencia |
| NS-17 | SCH | Fixture con JSON truncado |
| NS-18 | SCH | `evidence_kind` «cv» fuera del enum |
| NS-19 | SCH | Etiqueta script en el texto |
| NS-20 | ISO | `synthetic_organization_id` de otro tenant |
| NS-21 | ISO | Origen F34 de ORG-S2 en el fixture de ORG-S1 |
| NS-22 | HSH | `content_hash` alterado |
| NS-23 | HSH | `hash_before` alterado |
| NS-24 | HSH | Cadena de eventos rota |
| NS-25 | HSH | Cadena de provenance rota |
| NS-26 | PRV | Provenance ausente |
| NS-27 | PRV | Transformación fuera del registro T1 |
| NS-28 | ORI | `origin_record_id` inexistente en F34 |
| NS-29 | ORI | Texto distinto del origen F34 |
| NS-30 | ORI | Evidencia fuera de la regla de selección determinista |
| NS-31 | RUN | `pipeline_run_id` inexistente |
| NS-32 | RUN | Secuencia de eventos con un hueco |
| NS-33 | RUN | Instante anterior al reloj lógico |
| NS-34 | REV | Revisión simulada ausente |
| NS-35 | REV | `reviewer_type` distinto de `synthetic_human_simulation` |
| NS-36 | REV | `review_status` «apto» |
| NS-37 | REV | Campo de aptitud en la revisión |
| NS-38 | REV | `scripted` falso |
| NS-39 | CAP | Campo `score` |
| NS-40 | CAP | Campo `ranking_position` |
| NS-41 | CAP | Campo `recommendation` |
| NS-42 | CAP | Campo `best_candidate` |
| NS-43 | CAP | Campo `automatic_selection` |
| NS-44 | CAP | Transformación `ocr-pdf-v1` |
| NS-45 | CAP | Campo `parsing_engine` |
| NS-46 | CAP | Campo `extraction_method` |
| NS-47 | CAP | Campo `embedding` con un vector numérico |
| NS-48 | CAP | Campo `vector_ref` |
| NS-49 | CAP | Campo `semantic_search` |
| NS-50 | PER | Token `APP-` en el texto |
| NS-51 | PER | Campo `person_token` |
| NS-52 | STO | Campo `endpoint` con URL en el run |
| NS-53 | STO | Campo `storage_target` con destino pgsql |
| NS-54 | STO | `origin_file` dentro de `g0-evidence/adjuntos` |
| NS-55 | STO | Frase sobre tablas de Laravel en un documento |
| NS-56 | CLM | Frase sobre el entorno de despliegue en un documento |
| NS-57 | DEP | `import numpy` |
| NS-58 | DEP | `import sqlite3` (DH-07) |
| NS-59 | GIT | Archivo nuevo en `app/` |
| NS-60 | GIT | Migración en `database/` |
| NS-61 | GIT | Prueba en `tests/` |
| NS-62 | GIT | Matriz de trazabilidad RF tocada |
| NS-63 | GIT | Evidencia F34B tocada |
| NS-64 | GIT | Binario PNG con extensión .json en `evidencia-sbx/` |
| NS-65 | GIT | Imagen en `evidencia-sbx/` |
| NS-66 | GIT | JSON en `tools/f35sbx/` |
| NS-67 | GIT | Prefijo confundible `evidencia-sbx-otro/` |
| NS-68 | GIT | Git con error o no disponible |
| NS-69 | GIT | Archivo eliminado |
| NS-70 | GIT | Resultado UNKNOWN del alcance de `validate_f34b.py` |
| NS-71 | CLM | Frase que da por superada la puerta G0 real |
| NS-72 | STA | Declaración «G0 real» con valor distinto de NO APROBADA en el README |
| NS-73 | CLM | Frase sobre F35 productiva sin bloqueo |
| NS-74 | PHS | Frase sobre el estado de F36 |
| NS-75 | PHS | Frase sobre la decisión final de RF-23 |
| NS-76 | PHS | Frase sobre el orden de RF-21 |
| NS-77 | CLM | Frase concesiva seguida de OCR |
| NS-78 | STA | Alias desconocido «G0 productiva» |
| NS-79 | STA | F35-SBX declarada BLOQUEADA en el README con la puerta vigente |
| NS-80 | GOV | Gobierno con «AÚN NO INICIADA» |
| NS-81 | GOV | Gobierno con F35-SBX-A como cerrada |
| NS-82 | GATE | Decisión de la G0 real alterada |
| NS-83 | CON | `additionalProperties` verdadero en el contrato |
| NS-84 | CON | Campo `score` en el contrato |
| NS-85 | CON | `reviewer_type` como cadena libre en el contrato |
| NS-86 | CON | Palabra clave `patternProperties` en el contrato |
| NS-87 | MAN | Fixture con SHA-256 distinto del manifest |
| NS-88 | MAN | Manifest ausente |
| NS-89 | DOC | Documento obligatorio ausente |
| NS-90 | DOC | Enlace roto |
| NS-91 | GIT | Cuarto validador `validate_f34a.py` tocado |
| NS-92 | GIT | Línea funcional extra en `validate_f30.py` |
| NS-93 | GIT | Línea funcional extra en `validate_f33.py` |
| NS-94 | GIT | Línea funcional extra en `validate_f34.py` |
| NS-95 | GIT | Base ilegible de un validador histórico |
| NS-96 | CLM | Frase con `scoring` entre backticks |
| NS-97 | CLM | Frase con `OCR` entre backticks |
| NS-98 | PHS | Frase sobre `RF-23` entre backticks |
| NS-99 | PHS | Frase con rf-23 en minúsculas |
| NS-100 | CLM | Frase con scoring en negrita |
| NS-101 | CLM | Frase con scoring en cursiva (asterisco) |
| NS-102 | CLM | Frase con scoring en cursiva (guion bajo) |
| NS-103 | CLM | Frase con scoring tachado |
| NS-104 | CLM | Frase con OCR en negrita y backticks |
| NS-105 | CLM | Frase en mayúsculas con backticks |
| NS-106 | PHS | Frase con `rf-21` entre backticks |
| NS-107 | MAN | `note` reemplazada por una frase sobre el mejor candidato |
| NS-108 | MAN | `note` reemplazada por una declaración de la G0 real |
| NS-109 | MAN | `derivation_rule` con scoring |
| NS-110 | MAN | `note` válida con una frase añadida sobre el mejor candidato |
| NS-111 | MAN | `note` con OCR en negrita y backticks |
| NS-112 | MAN | `note` en mayúsculas |
| NS-113 | MAN | `note` con negación mixta |
| NS-114 | MAN | `derivation_rule` sobre RF-23 |
| NS-115 | MAN | `note` con una declaración de F35 productiva |
| NS-116 | MAN | Clave desconocida en el manifest |
| NS-117 | MAN | Clave desconocida en una entrada de `files` |
| NS-118 | MAN | `note` con una declaración de alcance C |
| NS-119 | MAN | `note` sobre datos reales |
| NS-120 | REV | `review_scope` anterior de tres términos |
| NS-121 | REV | `review_scope` seleccion |
| NS-122 | REV | `review_scope` evaluacion_candidato |
| NS-123 | REV | `review_scope` idoneidad |
| NS-124 | REV | `review_scope` aptitud |
| NS-125 | REV | `review_scope` recomendacion |
| NS-126 | REV | `review_scope` vacío |
| NS-127 | CON | Contrato con el `review_scope` anterior |
| NS-128 | REV | Valor anterior de `review_scope` citado en un documento |
| NS-129 | PHS | RF23 sin guion |
| NS-130 | PHS | RF 23 con espacio |
| NS-131 | PHS | RF con raya corta antes de 23 |
| NS-132 | PHS | RF con raya larga antes de 23 |
| NS-133 | PHS | RF21 sin guion |
| NS-134 | PHS | rf y 21 unidos por un guion no separable |
| NS-135 | CLM | scoring en caracteres de ancho completo |
| NS-136 | CLM | scoring con U+200B intercalado |
| NS-137 | CLM | scoring con U+2060 y U+FEFF intercalados |
| NS-138 | CLM | Scope C con participio |
| NS-139 | CLM | Scope C con verbo en presente |
| NS-140 | CLM | Alcance C con verbo en presente |
| NS-141 | PHS | scope c en minúsculas |
| NS-142 | MAN | `note` como lista |
| NS-143 | MAN | `note` como objeto |
| NS-144 | MAN | `note` nula |
| NS-145 | MAN | `note` numérica |
| NS-146 | MAN | `derivation_rule` como lista |
| NS-147 | MAN | Objeto adicional en el primer nivel del manifest |
| NS-148 | MAN | Clave desconocida en la entrada del contrato en `files` |
| NS-149 | MAN | Clave desconocida en la entrada de un fixture en `files` |
| NS-150 | MAN | Frase partida en dos campos dentro de `note` |
| NS-151 | MAN | `note` con scoring en ancho completo |
| NS-152 | MAN | `note` con scoring y U+200B |
| NS-153 | MAN | `note` con RF23 |
| NS-154 | MAN | `derivation_rule` con Scope C |
| NS-155 | MAN | `bytes` booleano en `files` |
| NS-156 | MED | Carácter invisible U+200B en un fixture |
| NS-157 | PHS | RF entre backticks, espacio y 23 |
| NS-158 | PHS | RF en negrita pegado a 23 |
| NS-159 | PHS | RF en cursiva, espacio y 23 |
| NS-160 | PHS | RF con guiones bajos pegado a 23 |
| NS-161 | CLM | Scope en negrita seguido de C, verbo en presente |
| NS-162 | CLM | Scope entre backticks seguido de C, verbo en presente |
| NS-163 | CLM | alcance en cursiva seguido de C |
| NS-164 | PHS | RF entre backticks con predicado |
| NS-165 | PHS | RF en negrita pegado a 23 con predicado |
| NS-166 | PHS | RF en cursiva con predicado |
| NS-167 | CLM | Scope en negrita seguido de C con participio |
| NS-168 | CLM | Scope entre backticks seguido de C con participio |
| NS-169 | PHS | RF-23, dos puntos y predicado |
| NS-170 | PHS | RF-21, dos puntos y predicado |
| NS-171 | PHS | RF 23, raya larga y predicado |
| NS-172 | PHS | RF23, signo igual y predicado |
| NS-173 | PHS | RF-23, flecha ASCII y predicado |
| NS-174 | PHS | RF23, dos puntos y predicado de selección |
| NS-175 | PHS | RF-21, dos puntos y participio |
| NS-176 | PHS | RF-23, flecha Unicode y predicado |
| NS-177 | MAN | `note` con RF-23, dos puntos y predicado |
| NS-178 | MAN | `derivation_rule` con RF 23, raya y predicado |
| NS-179 | MAN | Clave `note` duplicada |
| NS-180 | MAN | Clave `derivation_rule` duplicada |
| NS-181 | MAN | Clave de primer nivel duplicada |
| NS-182 | MAN | `sha256` duplicado dentro de `files` |
| NS-183 | MAN | `files` duplicado |
| NS-184 | MAN | `f34` duplicado |
| NS-185 | SCH | `synthetic_organization_id` duplicado en un fixture |
| NS-186 | CON | Clave duplicada en el contrato |
| NS-187 | MAN | `note` con U+200B escapado |
| NS-188 | MAN | `note` con U+200C escapado |
| NS-189 | MAN | `note` con U+200D escapado |
| NS-190 | MAN | `note` con U+2060 escapado |
| NS-191 | MAN | `note` con U+FEFF escapado |
| NS-192 | MAN | `note` con U+00AD escapado |
| NS-193 | MAN | `note` con ancho completo escapado |
| NS-194 | MAN | `derivation_rule` con U+200B escapado |
| NS-195 | MED | Fixture con U+2060 escapado |
| NS-196 | PHS | RF-23, dos puntos y predicado entre paréntesis |
| NS-197 | PHS | RF-21, dos puntos y predicado entre paréntesis |
| NS-198 | PHS | RF23, dos puntos y predicado compuesto entre paréntesis |
| NS-199 | PHS | RF 23, raya larga y participio entre paréntesis |
| NS-200 | PHS | RF-23, flecha Unicode y predicado entre paréntesis |
| NS-201 | PHS | RF en negrita con predicado en negrita entre paréntesis |
| NS-202 | PHS | RF entre backticks con predicado entre backticks y paréntesis |
| NS-203 | PHS | RF-23 en cursiva con predicado en cursiva entre paréntesis |
| NS-204 | PHS | RF con guiones bajos y predicado entre paréntesis |
| NS-205 | PHS | RF-23 con predicado entre paréntesis |
| NS-206 | PHS | RF 23, raya larga y predicado entre paréntesis |
| NS-207 | MAN | `note` con RF-23 y predicado entre paréntesis |
| NS-208 | MAN | `note` con RF en negrita y predicado entre paréntesis |
| NS-209 | MAN | `derivation_rule` con RF-21 y participio entre paréntesis |
| NS-210 | PHS | RF-23, dos puntos y doble paréntesis |
| NS-211 | PHS | RF-21 y doble paréntesis |
| NS-212 | PHS | RF23, dos puntos y triple paréntesis con predicado compuesto |
| NS-213 | PHS | RF 23, raya larga y doble paréntesis |
| NS-214 | PHS | RF-23, flecha Unicode y triple paréntesis |
| NS-215 | PHS | RF en negrita y doble paréntesis con negrita |
| NS-216 | PHS | RF entre backticks y doble paréntesis con backticks |
| NS-217 | PHS | RF-23 en cursiva y triple paréntesis con cursiva |
| NS-218 | PHS | RF con guiones bajos y doble paréntesis |
| NS-219 | PHS | Cinco capas de paréntesis |
| NS-220 | PHS | Ocho capas de paréntesis (cota máxima) |
| NS-221 | PHS | Nueve capas de paréntesis (cota superada) |
| NS-222 | PHS | Nueve capas con predicado inocuo (falla cerrado) |
| NS-223 | PHS | Tres aperturas y dos cierres |
| NS-224 | PHS | Desbalanceado con predicado inocuo |
| NS-225 | PHS | Solo apertura |
| NS-226 | PHS | Solo cierre |
| NS-227 | PHS | Envoltorio vacío |
| NS-228 | PHS | Envoltorio solo con espacios |
| NS-229 | PHS | Capas con espacios internos |
| NS-230 | PHS | Markdown fuera de los envoltorios |
| NS-231 | PHS | Envoltorio ambiguo |
| NS-232 | PHS | Cierre extra tras el envoltorio |
| NS-233 | MAN | `note` con doble paréntesis |
| NS-234 | MAN | `note` con Markdown y doble paréntesis |
| NS-235 | MAN | `derivation_rule` con triple paréntesis |
| NS-236 | MAN | `note` con paréntesis desbalanceados |
| NS-237 | MAN | `derivation_rule` con nueve capas |
| NS-238 | PHS | RF-21 y RF-23 con predicado envuelto |
| NS-239 | PHS | RF-23, RF-21 con predicado envuelto |
| NS-240 | PHS | Salto de línea entre RF y predicado envuelto |
| NS-241 | PHS | Salto de línea y doble paréntesis |
| NS-242 | PHS | Markdown y salto de línea sin paréntesis |
| NS-243 | PHS | Raya, salto de línea y doble paréntesis |
| NS-244 | MAN | `note` con salto de línea entre RF y predicado |
| NS-270 | DOC | Bloque de código sin cerrar en un documento |
| NS-273 | PHS | Prosa tras un fence de 4 backticks con 3 internos |
| NS-274 | PHS | Prosa tras un fence de virgulillas |
| NS-275 | DOC | Fence de 4 backticks con 3 internos sin cerrar |
| NS-276 | PHS | Prosa tras un fence de 3 backticks |
| NS-277 | CLM | Prosa tras un bloque HTML cerrado |
| NS-278 | PHS | Contenido de un bloque HTML, analizado línea a línea |
| NS-279 | CLM | Línea indentada que continúa un párrafo (no es código) |
| NS-280 | MAN | `note` con un fence |
| NS-281 | MAN | `note` con un bloque HTML |
| NS-282 | CLM | Frase dentro de un título setext |
| NS-298 | GOV | Gobierno sin estado de ciclo de vida |
| NS-299 | GOV | Estado de ciclo de vida desconocido (FINALIZADA) |
| NS-300 | GOV | Estado de ciclo de vida desconocido (COMPLETADA) |
| NS-301 | GOV | Cierre con un valor de G0 real distinto de NO APROBADA |
| NS-302 | GOV | Cierre con un valor de F35 productiva distinto de BLOQUEADA |
| NS-303 | GOV | Cierre con F35-SBX-B fuera de NO INICIADA |
| NS-304 | GOV | Cierre con un valor de alcance C distinto de BLOQUEADO |
| NS-305 | GOV | Cierre con un valor de datos reales distinto de PROHIBIDOS |
| NS-306 | GOV | Cierre con auditoría independiente distinta de PASS |
| NS-307 | GOV | Documentos de gobierno con estados distintos |
| NS-308 | GOV | ACADEMIC_BASELINE sin el registro de cierre |
| NS-309 | GOV | Cierre sin regresión GREEN registrada en el plan |
| NS-310 | GIT | ACADEMIC_BASELINE con la frase de RF-23 alterada |
| NS-311 | GIT | ACADEMIC_BASELINE con una frase añadida sobre RF-21 |
| NS-312 | GIT | ACADEMIC_BASELINE con una frase añadida sobre otro RF |
| NS-313 | GIT | ACADEMIC_BASELINE con texto arbitrario |
| NS-314 | GIT | ACADEMIC_BASELINE con la apertura en lugar del cierre |
| NS-315 | GIT | CLAUDE.md con una línea añadida al cierre |
| NS-316 | GIT | Archivo de gobierno no autorizado (README.md) |
| NS-317 | GIT | Git con error durante el cierre |
| NS-318 | GIT | Base sin relación de ancestro con HEAD |
| NS-319 | STA | README con un estado de F35-SBX-A desconocido |
| NS-245 | JOIN | Fence de backticks: join_rf_breaks no une |
| NS-246 | JOIN | Fence de virgulillas: join_rf_breaks no une |
| NS-247 | JOIN | Fence con etiqueta de lenguaje: join_rf_breaks no une |
| NS-248 | JOIN | Fence de virgulillas con etiqueta: join_rf_breaks no une |
| NS-249 | JOIN | Código indentado con cuatro espacios: join_rf_breaks no une |
| NS-250 | JOIN | Código indentado con tabulador: join_rf_breaks no une |
| NS-251 | JOIN | Lista con guion: join_rf_breaks no une |
| NS-252 | JOIN | Lista con asterisco: join_rf_breaks no une |
| NS-253 | JOIN | Lista con signo más: join_rf_breaks no une |
| NS-254 | JOIN | Lista numerada con punto: join_rf_breaks no une |
| NS-255 | JOIN | Lista numerada con paréntesis: join_rf_breaks no une |
| NS-256 | JOIN | Lista numerada de dos dígitos con punto: join_rf_breaks no une |
| NS-257 | JOIN | Lista numerada de dos dígitos con paréntesis: join_rf_breaks no une |
| NS-258 | JOIN | Cita: join_rf_breaks no une |
| NS-259 | JOIN | Cita con continuación perezosa: join_rf_breaks no une |
| NS-260 | JOIN | Título de nivel 1: join_rf_breaks no une |
| NS-261 | JOIN | Título de nivel 2: join_rf_breaks no une |
| NS-262 | JOIN | Tabla: join_rf_breaks no une |
| NS-263 | JOIN | Línea en blanco entre las dos líneas: join_rf_breaks no une |
| NS-264 | JOIN | Fence de backticks que no cierra con virgulillas: join_rf_breaks no une |
| NS-265 | JOIN | Fence sin cerrar: join_rf_breaks no une |
| NS-266 | JOIN | Continuación indentada de una lista: join_rf_breaks no une |
| NS-267 | JOIN | Regla horizontal entre las dos líneas: join_rf_breaks no une |
| NS-268 | JOIN | Prosa ordinaria (sí se une): join_rf_breaks une |
| NS-269 | JOIN | Prosa ordinaria con sujeto (sí se une): join_rf_breaks une |
| NS-271 | JOIN | Prosa ordinaria RF-21 (sí se une): join_rf_breaks une |
| NS-272 | JOIN | Prosa tras un fence cerrado (sí se une): join_rf_breaks une |
| NS-283 | JOIN | Fence de 4 backticks con 3 internos: join_rf_breaks no une |
| NS-284 | JOIN | Línea de 3 backticks dentro de un fence de 4: join_rf_breaks no une |
| NS-285 | JOIN | Virgulillas dentro de un fence de backticks: join_rf_breaks no une |
| NS-286 | JOIN | Backticks dentro de un fence de virgulillas: join_rf_breaks no une |
| NS-287 | JOIN | Bloque HTML div: join_rf_breaks no une |
| NS-288 | JOIN | Bloque HTML sin cerrar: join_rf_breaks no une |
| NS-289 | JOIN | Comentario HTML: join_rf_breaks no une |
| NS-290 | JOIN | Bloque HTML pre: join_rf_breaks no une |
| NS-291 | JOIN | Bloque HTML details: join_rf_breaks no une |
| NS-292 | JOIN | Título setext con signos igual: join_rf_breaks no une |
| NS-293 | JOIN | Título setext con guiones: join_rf_breaks no une |
| NS-294 | JOIN | Bloque HTML con líneas en blanco internas: join_rf_breaks no une |
| NS-295 | JOIN | Prosa tras un fence de 4 backticks cerrado (sí se une): join_rf_breaks une |
| NS-296 | JOIN | Prosa tras un bloque HTML cerrado (sí se une): join_rf_breaks une |
| NS-297 | JOIN | Línea indentada que continúa un párrafo (sí se une): join_rf_breaks une |
