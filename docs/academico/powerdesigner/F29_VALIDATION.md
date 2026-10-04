# Validación F29 — formalización en PowerDesigner

Resultado por vista, con la evidencia que lo respalda:

- los informes de [`validation/`](validation/), que escribe cada script de construcción;
- el validador independiente [`scripts/validate_f29.py`](scripts/validate_f29.py), que lee los modelos guardados sin PowerDesigner y los contrasta con las fuentes del contenido;
- la revisión visual de cada exportación;
- la prueba de persistencia.

**Criterios:**

- **PASS:** la vista cumple la especificación.
- **OBS:** cumple, con una observación que no la invalida.

Ninguna vista queda en FALLA.

## Resumen

| Vista | Recuento | Conectividad | Cobertura | Restricciones | Legibilidad | Exportación | Check Model | Resultado |
|---|---|---|---|---|---|---|---|---|
| F3 BPMN AS-IS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | **PASS** |
| F5 BPMN TO-BE | PASS | PASS | PASS | PASS | PASS | PASS | OBS (advertencia de MT-02) | **PASS con OBS** |
| F8 Casos de uso | PASS | PASS | PASS | PASS | PASS | PASS | PASS (CU-16 por especificación) | **PASS** |
| ARQ-01 Arquitectura | PASS | PASS | PASS | PASS | PASS (offsets F31) | PASS | PASS | **PASS** |

Observaciones transversales a las cuatro vistas:

- **Capturas de PowerDesigner:** COMPLETED (28/09/2026). Son 7 capturas reales, tomadas después del hotfix F29B ([registro](evidencias/capturas/CAPTURAS_PENDIENTES.md)). Hasta entonces estaban pendientes.
- **Formatos DOCX y PDF:** UPDATED (28/09/2026). Tras las auditorías F29 y F29B, las exportaciones formales son el diagrama principal de los Formatos 03, 05, 08 y 11. Hasta entonces no se habían sustituido.
- **Cierre F31:** F29-L02 RESUELTA; F29-L01 y F29B-OBS-01 ACEPTADAS como limitaciones de metadata/presentación de PowerDesigner sin pérdida de modelo ni exportación.

## F3 — «F3 - BPMN AS-IS» ([informe](validation/F3_model_check.txt))

| Criterio | Evidencia | Resultado |
|---|---|---|
| Recuento | 14 tareas (AS-01 a AS-14), SP-01, 2 compuertas (G-01, G-02) y 6 + 2 eventos, iguales al glosario. 22 flujos de secuencia y 4 de mensaje | PASS |
| Nombres | Cada nodo se rotula «ID + nombre oficial», con el nombre literal de `m_asis.py` (comprobado por `validate_f29.py`) | PASS |
| Conectividad | Toda actividad y compuerta tiene entrada y salida. AS-06 → AS-08 es flujo de secuencia. G-01 [Sí] → AS-05 y [No] → EF-01. G-02 [Sí] → AS-10 y [No] → EF-02 | PASS |
| Pools y carriles | Pool del Colegio (caja blanca) con 4 carriles, sin «Sistemas». Pool Postulante con EP-01 → AS-07 → EP-02. El responsable de cada nodo queda en el modelo; AS-11 y EF-04 son de Evaluadores | PASS |
| SP-01 | Subproceso expandido de instancia múltiple paralela (marcador \|\|\|) con SI-01 → AS-09 → G-02 → AS-10 → AS-11 → EF-04, y G-02 [No] → EF-02 | PASS |
| Mensajes | MF-01 AS-06 → EP-01, MF-02 AS-07 → AS-08 y MF-03 / MF-04 al borde del pool Postulante; todos unidireccionales | PASS |
| Anotaciones | «AS-IS preliminar derivado del análisis del equipo, sujeto a validación institucional» y, en EF-02, «No está verificado si se informa al candidato que no continúa» | PASS |
| Legibilidad | Revisión visual: flujo de izquierda a derecha, carriles horizontales, sin solapamientos ni recortes | PASS |
| Exportación | [PNG](exports/F3_BPMN_ASIS.png) (6042 × 1822) y [SVG](exports/F3_BPMN_ASIS.svg) válidos | PASS |
| Check Model | Del modelo completo, sin autocorrección: solo los hallazgos del F5 que se explican abajo; ninguno de la vista F3 | PASS |

## F5 — «F5 - BPMN TO-BE» ([informe](validation/F5_model_check.txt))

| Criterio | Evidencia | Resultado |
|---|---|---|
| Recuento | 31 tareas (TB-01 a TB-30 y TB-F1), SP-P, 10 compuertas y 9 eventos, iguales a `m_tobe.py`. 51 flujos de secuencia y 8 de mensaje | PASS |
| Dos niveles | Nivel vacante en el pool de la organización. Nivel postulación en SP-P, subproceso expandido de instancia múltiple paralela, con TB-14 a TB-23 | PASS |
| Reglas | TB-15 con una sola entrada (TB-14). GM1 une GD1 [Sí] y GD3 [Sí]. GM2 une TB-18 y TB-20. GV [No] vuelve a TB-21. GF «¿Finalista?»: Sí → EFP-02 y No → EFP-03 | PASS |
| Decisión humana | TB-26 en el carril Aprobador / Dirección, con la nota «Decisión humana (RF-23): el ranking no elige». TB-24 y TB-25 anotados como apoyo | PASS |
| TB-30 y TB-F1 | TB-30 es transversal, en un grupo discontinuo y sin flujo. TB-F1 es la propuesta futura A-30: desconectada, no sale de TB-25 y no representa ninguna regla «sin candidato elegible» | PASS |
| RF-29 | No aparece en el TO-BE | PASS |
| Mensajes | MT-01 TB-10 → EP-01 «Vacante publicada». MT-02 TB-13 → borde de SP-P. MT-03 a MT-08 al borde del pool Postulante | PASS |
| Legibilidad | Revisión visual por secciones: sin cruces sobre símbolos. Los rótulos de MT-06 y MT-07 quedan separados de las divisiones de carril | PASS |
| Exportación | [PNG](exports/F5_BPMN_TOBE.png) (12174 × 2542) y [SVG](exports/F5_BPMN_TOBE.svg) válidos | PASS |
| Check Model | 3 hallazgos, cada uno explicado por aislamiento: TB-30 y TB-F1 sin flujos (2 errores, exigidos por la especificación) y MT-02 hacia el borde de SP-P (1 advertencia, límite de PowerDesigner). Ver [README](README.md#check-model) | **OBS** |

## F8 — «F8 - Casos de Uso Academicos» ([informe](validation/F8_model_check.txt))

| Criterio | Evidencia | Resultado |
|---|---|---|
| Recuento | 5 actores (ACT-01 a ACT-05), sin «Sistema». CU-01 a CU-20, sin CU-21. CU-18 «Registrar decisión final humana» | PASS |
| Matriz actor-caso | 22 asociaciones, idénticas a la matriz del Formato 08 (comparadas una a una) | PASS |
| Inclusiones | Solo CU-05, CU-15 y CU-17 → CU-16 «include»; ningún «extend» | PASS |
| Notas | CU-17 «calcula, ordena y compara; no selecciona». CU-18 «decisión humana (RF-23)…». Nota técnica de auditoría (RF-27, ACT-03, UC-RF27, fuera del catálogo CU-01..CU-20). El Sistema no es un actor | PASS |
| Áreas funcionales | A Requerimiento de personal, B Convocatoria, C Postulación, D Evaluación, E Selección y cierre | PASS |
| Legibilidad | Comprobación geométrica automática: 25 líneas, 0 atraviesan un símbolo ajeno. Revisión visual sin solapamientos | PASS |
| Exportación | [PNG](exports/F8_Casos_de_Uso_Academicos.png) (3786 × 3110) y [SVG](exports/F8_Casos_de_Uso_Academicos.svg) válidos | PASS |
| Check Model | 1 hallazgo: *Use Case/Single* de CU-16, sin actor directo por especificación (comprobado por aislamiento) | PASS |

## ARQ-01 — «ARQ-01 - Arquitectura Conceptual» ([informe](validation/ARQ01_model_check.txt))

| Criterio | Evidencia | Resultado |
|---|---|---|
| Recuento | 17 componentes, C01 a C17 (sin C18), con los nombres de `COMPONENTS.md`. 6 agrupaciones (paquetes). R-01 a R-20 en 24 dependencias, incluida «usan»: R-03, R-16 y R-17 tienen dos trazos | PASS |
| Agrupación | Cada componente pertenece a su paquete y su símbolo queda dentro del contenedor (comprobado por geometría) | PASS |
| Cadena principal | C04 → C05 → C07; C08 → C07; C08 → C09 → C10 → C11; C11 → C07 | PASS |
| Estereotipos | `<<conceptual>>` en todos. C03, C12 y C13 `<<transversal>>`; C09 `<<apoyo>>`; C10 `<<human decision>>`; C14 a C16 `<<infraestructura>>`; C17 `<<experimental>>` | PASS |
| Fronteras | C17 solo con R-19 (C05 ⇢ C17) y R-20 (C17 ⇢ C01), discontinuas y sin relación con C09, C10 ni C11. C03 es transversal, no gestión de organizaciones. Redis es apoyo (C16), no la base de datos principal | PASS |
| Exclusiones | Sin facturación, suscripciones, superadministración, banco de talentos, Kubernetes, Meilisearch, almacenamiento en la nube, API REST aparte, microservicios, IA de selección ni RF-28 | PASS |
| Notas | C10, C09, C17, la nota general «No es un despliegue: ver DE-01» y la de estereotipos | PASS |
| Legibilidad | Todos los vínculos visibles, llevados al frente de los contenedores. R-03 hacia C13 rodea C17. F31 separó los rótulos de sus líneas y bordes mediante offsets de texto, sin cambiar extremos ni rutas | **PASS** |
| Exportación | [PNG](exports/ARQ-01_Arquitectura_Conceptual.png) (4862 × 2862) y [SVG](exports/ARQ-01_Arquitectura_Conceptual.svg) válidos | PASS |
| Check Model | Solo *Use Case/Single* de CU-16 del F8; ninguno de la vista ARQ-01 | PASS |

## Reproducibilidad tras la recarga (hotfix F29B)

La prueba de persistencia original de la F29 (abajo) solo contaba símbolos y diagramas. La integración posterior detectó que la **geometría** cambiaba al reabrir: agrupaciones de ARQ-01 reducidas, casos de uso y tareas redimensionados. También detectó que el editor no mostraba el contenido de SP-01 y SP-P. El hotfix F29B lo corrige ([`F29B_HOTFIX.md`](F29B_HOTFIX.md)). Ahora cada script guarda, cierra y reabre el modelo, compara la geometría de cada símbolo (tolerancia 0), exporta desde el modelo reabierto y comprueba que una segunda recarga reproduce el SVG.

| Vista | Diagramas comprobados | Cambios tras reabrir | Exportación reproducible | Resultado |
|---|---|---|---|---|
| F3 | Principal (75 símbolos) y detalle de SP-01 (14) | 0 | Sí | PASS |
| F5 | Principal (156) y detalle de SP-P (45) | 0 | Sí | PASS |
| F8 | Principal (67) | 0 | Sí | PASS |
| ARQ-01 | Principal (55); las 6 agrupaciones conservan X, Y, ancho y alto | 0 | Sí | PASS |

La limitación que queda (**F29B-OBS-01**) está documentada: en la vista principal del editor, los recuadros de SP-01 y SP-P aparecen sin contenido. Su contenido se ve en los diagramas de detalle y en las exportaciones.

## Persistencia (F29, antes del hotfix)

Los dos modelos se cerraron y se volvieron a abrir desde el disco, y conservaron sus vistas:

- **F29_BPM_Academico.bpm:** «F3 - BPMN AS-IS» (29 símbolos) y «F5 - BPMN TO-BE» (60).
- **F29_UML_Academico.oom:** «F8 - Casos de Uso Academicos» (67 símbolos: 5 actores, 20 CU, 22 asociaciones y 3 «include») y «ARQ-01 - Arquitectura Conceptual» (55 símbolos: 7 paquetes y 24 dependencias).

## Validación independiente

`python docs/academico/powerdesigner/scripts/validate_f29.py` lee los XML guardados y comprueba:

- los nombres literales contra `m_asis.py`, `m_tobe.py`, `m_cu.py` y `COMPONENTS.md`;
- los recuentos, las restricciones (sin CU-21, sin «Sistema», sin C18 y sin RF-29 en el TO-BE) y los pools y carriles;
- la instancia múltiple de SP-01 y SP-P;
- la validez de los PNG y SVG y de sus recursos;
- que la F23 no cambió.

Resultado en la F29: 157 comprobaciones correctas, 0 fallas. Con el hotfix F29B se añadieron comprobaciones (ajuste automático al texto desactivado, geometría de las agrupaciones, diagramas de detalle, ausencia de duplicados en las exportaciones y recarga registrada en los informes), sin rebajar ninguna: **177 comprobaciones correctas, 0 fallas**.

## Seguridad del alcance

- **F23:** los 53 archivos de `docs/v1.1/powerdesigner/models` y `exports` tienen el mismo SHA-256 que antes de la F29.
- **Git:** los cambios quedan solo en `docs/academico/**`.
- **Sin cambios en:** runtime, ML, F9 publicado, etiquetas y release.
