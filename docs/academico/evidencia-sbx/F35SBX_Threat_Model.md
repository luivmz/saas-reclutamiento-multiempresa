# F35-SBX-A — Modelo de amenazas de F35-SBX

> Fase F35-SBX-A, versión 1 (07/10/2026). Extiende el [modelo de amenazas de F34A](../g0-readiness/F34A_Modelo_de_Amenazas.md), aceptado por el equipo (G0-09), solo para el sandbox sintético. No reemplaza ninguna amenaza T-01 a T-25 ni cambia su estado. Cada amenaza tiene al menos un caso negativo ejecutado por [`validate_f35sbx.py`](../tools/f35sbx/validate_f35sbx.py); el validador comprueba que los casos citados existen.

## Amenazas

| ID | Amenaza | Riesgo | Control | Evidencia del control | Casos negativos | Fail-closed |
|---|---|---|---|---|---|---|
| TSB-01 | Contaminación con datos reales | Alto | Contrato cerrado, detectores de PII y media, seis marcadores | Reglas SCH, PII, MED y SYN | NS-01, NS-02, NS-03, NS-04, NS-05, NS-13, NS-14, NS-156, NS-195 | Cualquier coincidencia: FAIL |
| TSB-02 | Mezcla entre tenants | Crítico | Un tenant por fixture; organización del origen F34 y del criterio comprobada | Regla ISO | NS-20, NS-21 | Organización distinta: FAIL |
| TSB-03 | Reidentificación | Alto | Sin tokens ni campos de persona (DH-06) | Regla PER | NS-50, NS-51 | Token o campo de persona: FAIL |
| TSB-04 | Provenance falsa | Alto | Una provenance por evidencia, encadenada, con origen F34 verificado | Reglas PRV y ORI | NS-26, NS-27, NS-28 | Provenance no verificable: FAIL |
| TSB-05 | Hash inconsistente | Alto | Recálculo independiente de `content_hash`, `hash_before` y las cadenas | Regla HSH | NS-22, NS-23, NS-24, NS-25 | Diferencia: FAIL |
| TSB-06 | Manipulación de fixtures o del manifest | Alto | JSON sin claves duplicadas en ningún nivel; manifest con esquema cerrado (claves y tipos exactos, sin listas ni objetos bajo campos de texto), SHA-256 y tamaño; textos decodificados (escapes JSON incluidos) sin caracteres invisibles ni de compatibilidad; cada texto normalizado (NFKC, sin caracteres invisibles) y analizado por proposiciones; texto igual a T1(texto F34); selección determinista | Reglas MAN y ORI | NS-29, NS-30, NS-87, NS-88, NS-107, NS-108, NS-109, NS-110, NS-111, NS-112, NS-113, NS-114, NS-115, NS-116, NS-117, NS-118, NS-119, NS-142, NS-143, NS-144, NS-145, NS-146, NS-147, NS-148, NS-149, NS-150, NS-151, NS-152, NS-153, NS-154, NS-155, NS-179, NS-180, NS-181, NS-182, NS-183, NS-184, NS-185, NS-186, NS-187, NS-188, NS-189, NS-190, NS-191, NS-192, NS-193, NS-194 | Hash, tamaño o selección distintos: FAIL |
| TSB-07 | Paso accidental de artefactos SBX al runtime | Crítico | Alcance Git de F35-SBX-A con doble llave (DH-02) | Regla GIT; `validate_f34b.py` y `validate_f34e.py` | NS-59, NS-60, NS-61, NS-64, NS-65, NS-66, NS-67, NS-91, NS-92, NS-93, NS-94, NS-95, NS-310, NS-311, NS-312, NS-313, NS-314, NS-315, NS-316, NS-317, NS-318 | Ruta o adaptación fuera del alcance: FAIL |
| TSB-08 | Salida experimental leída como recomendación | Crítico | Sin campos ni valores de scoring, ranking o recomendación; runs marcados como oráculo | Reglas CAP y RUN | NS-39, NS-40, NS-41, NS-42, NS-43, NS-96, NS-97, NS-100, NS-101, NS-102, NS-103, NS-104, NS-105, NS-135, NS-136, NS-137, NS-138, NS-139, NS-140, NS-141, NS-161, NS-162, NS-163, NS-167, NS-168 | Capacidad prohibida: FAIL |
| TSB-09 | Persistencia fuera del sandbox | Alto | Sin campos de destino, conexión ni endpoint; solo JSON versionado (DH-07) | Regla STO | NS-52, NS-53, NS-55 | Referencia de destino: FAIL |
| TSB-10 | Bypass de synthetic-only | Alto | Los seis marcadores exigidos a la vez en cada evidencia | Regla SYN | NS-13, NS-14, NS-15 | Un marcador ausente: FAIL |
| TSB-11 | Declaración falsa sobre la G0 real | Crítico | Analizadores de proposiciones y estados de F34E sobre todos los documentos, sin descartar el contenido marcado con Markdown, tras normalizar (NFKC, guiones, RF, Scope C) | Reglas CLM, STA y GATE | NS-71, NS-72, NS-82, NS-298, NS-299, NS-300, NS-301, NS-302, NS-303, NS-304, NS-305, NS-306, NS-307, NS-308, NS-309, NS-319 | Afirmación o estado incoherente: FAIL |
| TSB-12 | Alteración de la decisión humana de RF-23 | Crítico | Matriz de trazabilidad protegida; frases sobre RF-21 y RF-23 analizadas | Reglas PHS y GIT | NS-62, NS-75, NS-76, NS-98, NS-99, NS-106, NS-129, NS-130, NS-131, NS-132, NS-133, NS-134, NS-157, NS-158, NS-159, NS-160, NS-164, NS-165, NS-166, NS-169, NS-170, NS-171, NS-172, NS-173, NS-174, NS-175, NS-176, NS-177, NS-178, NS-196, NS-197, NS-198, NS-199, NS-200, NS-201, NS-202, NS-203, NS-204, NS-205, NS-206, NS-207, NS-208, NS-209, NS-210, NS-211, NS-212, NS-213, NS-214, NS-215, NS-216, NS-217, NS-218, NS-219, NS-220, NS-221, NS-222, NS-223, NS-224, NS-225, NS-226, NS-227, NS-228, NS-229, NS-230, NS-231, NS-232, NS-233, NS-234, NS-235, NS-236, NS-237, NS-238, NS-239, NS-240, NS-241, NS-242, NS-243, NS-244, NS-245, NS-246, NS-247, NS-248, NS-249, NS-250, NS-251, NS-252, NS-253, NS-254, NS-255, NS-256, NS-257, NS-258, NS-259, NS-260, NS-261, NS-262, NS-263, NS-264, NS-265, NS-266, NS-267, NS-268, NS-269, NS-270, NS-271, NS-272, NS-273, NS-274, NS-275, NS-276, NS-277, NS-278, NS-279, NS-280, NS-281, NS-282, NS-283, NS-284, NS-285, NS-286, NS-287, NS-288, NS-289, NS-290, NS-291, NS-292, NS-293, NS-294, NS-295, NS-296, NS-297 | Cambio o afirmación: FAIL |
| TSB-13 | XSS en texto sintético (T-25 de F34A) | Alto | Patrón de texto plano sin marcado ni caracteres de control | Regla SCH | NS-19 | Marcado HTML: FAIL |
| TSB-14 | Hash no reproducible por reloj del sistema | Medio | Reloj lógico del run e instantes monótonos | Regla RUN | NS-33 | Instante fuera del reloj: FAIL |
| TSB-15 | Adjuntos de gobierno como datos | Alto | Origen fijo en el `evidence.csv` de F34 | Regla STO | NS-54 | Ruta de `g0-evidence` o adjuntos: FAIL |
| TSB-16 | Dependencia nueva | Medio | Solo biblioteca estándar autorizada; sin `sqlite3` en F35-SBX-A | Regla DEP | NS-57, NS-58 | Importación no autorizada: FAIL |
| TSB-17 | Revisión simulada leída como evaluación de personas | Crítico | Alcance único `integridad_y_procedencia`; estados `conforme` u `observado` | Regla REV | NS-34, NS-35, NS-36, NS-37, NS-38, NS-120, NS-121, NS-122, NS-123, NS-124, NS-125, NS-126, NS-127, NS-128 | Estado o campo evaluativo: FAIL |

## Relación con F34A

| Amenaza F34A | Tratamiento en F35-SBX |
|---|---|
| T-10 (fuga cross-tenant) | TSB-02 |
| T-11 (exfiltración de evidencias) | TSB-01, TSB-03 y TSB-15 |
| T-13 (logs con PII) | La auditoría experimental guarda solo identificadores y hashes (TSB-03) |
| T-21 (deriva funcional hacia campos calculados) | TSB-08 y TSB-17 |
| T-22 (cadena de suministro) | TSB-16 |
| T-23 (datos reales en datos de prueba) | TSB-01 y TSB-10 |
| T-25 (XSS persistente) | TSB-13 |
