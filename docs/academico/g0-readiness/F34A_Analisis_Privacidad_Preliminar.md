# F34A — Análisis preliminar de privacidad y datos personales (G0-03)

> Fase F34A, versión 1.1 (04/10/2026), corregida tras la auditoría F34A. Análisis **preliminar**, con estructura de evaluación de impacto en privacidad (PIA/DPIA), del **alcance B** de ADR-005. **No afirma cumplimiento legal** ni sustituye la revisión del responsable del tratamiento y de un profesional del derecho ([checklist jurídico](F34A_Checklist_Revision_Juridica.md)). Estado de G0-03: **PENDIENTE EXTERNO**.

> **Regla vigente: los datos reales siguen PROHIBIDOS.** El proyecto solo usa datos ficticios (contrato 7) y F34 solo datos sintéticos. **El consentimiento por sí solo NO levanta el bloqueo.** Cualquier uso futuro de datos reales exige autorización explícita del equipo, revisión contractual, revisión jurídica, este análisis aprobado y una aprobación específica distinta de G0 ([ADR-005 §6.10](../diseno-inteligente/F33_ADR_005_G0.md#6-decisión-propuesta)).

## 1. Finalidad

| Tratamiento previsto en B | Finalidad | Fuera de la finalidad |
|---|---|---|
| Citas de evidencia por criterio | Que el evaluador fundamente el nivel que asigna y que otros puedan revisarlo | Puntuar, perfilar o comparar personas de forma automática |
| Justificaciones y suficiencia | Explicar la valoración humana (RF-19) | Usarlas como feature o etiqueta de un modelo (F34, LK-08) |
| Anotaciones complementarias | Añadir contexto sin alterar el resultado | Corregir el resultado de forma encubierta |
| Alertas deterministas | Verificar la completitud y consistencia del proceso | Filtrar, descartar o recomendar postulantes |
| ICC y discrepancias | Calidad del proceso de evaluación | Evaluar el desempeño individual del evaluador |
| `analysis_run` y eventos | Auditar qué reglas se ejecutaron, con qué versión y sobre qué entrada (hash) | Guardar copias del contenido evaluado |

## 2. Categorías de datos

| Categoría | Ejemplos | Titular | ¿Existe ya en v1.1? | Nuevo en B |
|---|---|---|---|---|
| Identificación y contacto | Nombre, correo, teléfono, ciudad | Postulante | Sí (`users`, `candidate_profiles`) | No |
| Perfil profesional | Nivel educativo, título, años de experiencia, resumen | Postulante | Sí | No |
| Documentos | CV y anexos en disco privado | Postulante | Sí (`candidate_documents`, Policy de descarga) | No |
| Postulación y etapas | Estado, fechas, historial con comentario | Postulante | Sí (`applications`, historial) | No |
| Valoraciones humanas | Nivel, puntaje de rúbrica | Postulante y evaluador | Sí (RF-19) | Se añaden criterio y versión |
| **Citas de evidencia** | Fragmento mínimo y su fuente | Postulante | No | **Sí** |
| **Justificación, suficiencia y anotaciones** | Texto del evaluador | Postulante y evaluador | Parcial | **Sí** |
| Datos del evaluador | Identidad, carga, discrepancias | Evaluador | Parcial | Sí, en agregados |
| Auditoría | Acción, usuario, IP, metadatos | Usuarios del sistema | Sí (`audit_logs`, solo inserción) | Nuevas acciones |
| Atributos sensibles | Salud, origen, religión, etc. | — | No | **No se recolectan** |
| Audio, vídeo, biometría | — | — | No | **No** (CAP-27 requiere aprobación aparte) |

Los evaluadores también son titulares de datos: sus justificaciones y discrepancias no se usan para evaluarlos.

## 3. Necesidad y proporcionalidad

- **Necesidad:** sin citas y justificaciones no se puede revisar ni explicar una valoración humana. La necesidad **institucional** del alcance B no está validada (G0-12): este análisis la presupone solo como hipótesis.
- **Proporcionalidad:** B no trata más datos que el proceso actual, salvo citas mínimas y justificaciones (G0-13). Alternativa menos intrusiva considerada: guardar solo referencias (documento, página, pregunta) sin texto; se propone combinarla con citas mínimas de longitud acotada.
- **Sin decisiones automatizadas:** el sistema no selecciona, descarta ni contrata; la decisión la registra una persona (RF-23).

## 4. Minimización

- Citas mínimas, no copias del CV; referencias en lugar de texto cuando baste.
- Ningún campo de score del sistema sobre personas.
- Tokens o IDs internos en `analysis_run`; el hash prueba la entrada **sin guardarla**.
- Sin atributos sensibles ni sus *proxies* (edad derivada, foto, dirección, colegio de procedencia).
- Las features auxiliares (`evidence_sufficiency`, `evaluator_disagreement` y sus agregados) solo sirven para QA, proceso e ICC (F34).

## 5. Almacenamiento

- Laravel es el sistema de registro; PostgreSQL 17; CV en disco privado.
- Sin servicio externo en B; el servicio ML existente (RF-29) no recibe datos de personas.
- Hoy el proyecto corre en Docker local con datos ficticios; un despliegue real necesitaría su propio análisis de alojamiento y encargados (J-24).

## 6. Acceso

- Policies que comparan **rol y organización**; scope global por `organization_id`.
- Citas y justificaciones visibles solo para roles con necesidad (RR. HH., evaluador asignado, Aprobador/Dirección); el postulante no ve las de otros.
- Sin acceso de un tenant a otro; pruebas cross-tenant obligatorias (contrato 5).

## 7. Retención y borrado

| Dato | Propuesta técnica (a validar por el responsable del tratamiento) |
|---|---|
| Citas, justificaciones y anotaciones | Conservar mientras dure el proceso y el plazo que defina el responsable para reclamaciones; luego borrar o anonimizar |
| `analysis_run` y eventos | Conservar versiones y hash; sin contenido personal |
| Auditoría (`audit_logs`) | Solo inserción; conserva usuario, organización e IP según el sistema vigente; metadatos minimizados, sin PII innecesaria ni secretos; plazo a definir |
| Datos sintéticos de F34 | Sin límite: no son datos personales |

**Tensión a resolver con el responsable legal (J-17):** la auditoría inmutable y las anotaciones de solo inserción frente al derecho de cancelación. Opción técnica: guardar en la auditoría solo referencias y borrar el contenido personal en su tabla de origen.

Los plazos concretos **no se fijan en F34A**: son una decisión del responsable del tratamiento.

## 8. Multitenencia

- `organization_id` en toda entidad nueva, con scope global y Policies.
- Sin RLS en PostgreSQL: el aislamiento depende de scopes y Policies, por eso las pruebas cross-tenant son innegociables.
- Las reglas CTX-01 a CTX-10 de F34 ya prueban la coherencia de organización y vacante en datos sintéticos.

## 9. Procedencia (*provenance*)

- Cada evidencia guarda su fuente (tipo y referencia), quién la registró, cuándo y su estado (`borrador` o `vinculada`).
- B solo admite texto **registrado o introducido por una persona**: sin extracción automática.
- `analysis_run` registra `criteria_version`, `rubric_version`, `rules_version` y el hash canónico de entrada.

## 10. Logs

- `AuditLogger` registra usuario, organización, acción, objeto e IP, como en el sistema vigente, y descarta de los metadatos las claves sensibles (contraseñas, tokens, secretos, contenido de CV). **No es un registro anónimo:** se aplican minimización y limitación de propósito para no incluir PII innecesaria en metadatos ni *payloads* (contrato 6). Trigger `audit_logs_append_only`.
- `analysis_run_events` guarda estado, fecha y código de error, **sin texto de entrada**.
- Los logs de aplicación no deben contener citas ni justificaciones (amenaza T-13 del [modelo de amenazas](F34A_Modelo_de_Amenazas.md)).

## 11. Datos sensibles

No se recolectan. Si una cita de evidencia contuviera uno por accidente (por ejemplo, una mención de salud en un CV), la regla propuesta es no registrarla y, si ya se registró, permitir su retirada con anotación. El tratamiento jurídico queda en J-14.

## 12. Datos de audio

**Fuera del alcance B.** Grabar o transcribir entrevistas (CAP-27) requiere una aprobación aparte, con su propio análisis. En ningún caso se evalúan prosodia, acento, emociones ni biometría (ADR-005 §6.7).

## 13. Terceros y proveedores

En B, **ninguno**: sin servicios en la nube, sin LLM, sin APIs externas y sin dependencias nuevas. Si en el futuro se aprobara C, haría falta un análisis del servicio, de la pseudonimización y de la no persistencia (columna C de G0-03).

## 14. Riesgos y mitigaciones

| ID | Riesgo para los titulares | Probabilidad | Impacto | Mitigación | Riesgo residual |
|---|---|---|---|---|---|
| P-01 | Uso de datos reales sin autorización | Baja | Alto | Prohibición contractual; validadores PII; solo sintéticos | Bajo |
| P-02 | Fuga de citas entre organizaciones | Media | Alto | Scope y Policies; pruebas cross-tenant | Medio hasta probarlo en F35/F38 |
| P-03 | Citas excesivas (copias del CV) | Media | Medio | Longitud máxima; referencias en lugar de texto | Bajo |
| P-04 | Justificaciones con juicios sobre rasgos personales o sensibles | Media | Alto | Guía de redacción; revisión por muestreo; retirada con anotación | Medio |
| P-05 | Reutilizar justificaciones o suficiencia para puntuar personas | Baja | Alto | Prohibición de F33 y F34 (LK-08); sin campo de score | Bajo |
| P-06 | Evaluar a los evaluadores con sus discrepancias | Media | Medio | Agregados por vacante; uso solo para calidad del proceso | Bajo |
| P-07 | Retención indefinida | Media | Medio | Plazos definidos por el responsable (pendiente) | Medio hasta definirlos |
| P-08 | Conflicto entre inmutabilidad y cancelación | Media | Medio | Auditoría con referencias; contenido borrable en origen | Medio hasta la revisión jurídica |
| P-09 | Opacidad hacia el postulante | Media | Medio | Explicación por regla, evidencia y versión; transparencia a definir (J-21) | Medio |
| P-10 | Logs con PII | Baja | Alto | Contrato 6; revisión de logs | Bajo |

## 15. Conclusión preliminar

El diseño de B **reduce** la exposición frente a las alternativas C y D, pero quedan abiertas la base legal, los plazos de retención, la transparencia hacia el postulante y la tensión entre inmutabilidad y cancelación. **No hay conclusión de cumplimiento.** G0-03 se cierra solo con este análisis revisado y aprobado por el responsable del tratamiento, con revisión jurídica.
