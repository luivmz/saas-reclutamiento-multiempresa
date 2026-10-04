# F34A — Modelo de amenazas del futuro módulo inteligente (G0-09)

> Fase F34A, versión 1.1 (04/10/2026), corregida tras la auditoría F34A. **Solo diseño:** no implementa controles ni cambia el runtime. Metodología **STRIDE** sobre el **alcance B** de ADR-005, con las amenazas del alcance C marcadas como futuras. Estado de G0-09: **PARCIAL** (elaborado; falta la revisión y aceptación registrada del equipo).

## 1. Alcance del modelo

- **Dentro:** módulo Laravel del alcance B (rúbricas versionadas, evidencia, valoraciones, anotaciones, alertas, ICC, `analysis_run` y eventos), su interfaz Inertia/React y su relación con lo existente (Policies, `AuditLogger`, RF-21 a RF-23).
- **Contexto existente:** servicio FastAPI de RF-29 (experimental, sin datos de personas) y dataset sintético de F34.
- **Futuro (C, bloqueado):** extractor de documentos, localizador semántico y cualquier LLM. Se modelan solo para dejar las amenazas registradas.

## 2. Activos

| ID | Activo | Sensibilidad |
|---|---|---|
| A-01 | CV y documentos de postulantes (disco privado) | Alta (datos personales) |
| A-02 | Citas de evidencia, justificaciones y anotaciones | Alta (datos personales y juicios) |
| A-03 | Valoraciones humanas y desglose RF-21 | Alta (afectan la decisión) |
| A-04 | Rúbricas, criterios y reglas versionadas | Media (integridad del proceso) |
| A-05 | `analysis_run`, eventos y hash de entrada | Media (auditoría) |
| A-06 | `audit_logs` de solo inserción | Alta (no repudio) |
| A-07 | Credenciales, sesiones y token interno del servicio ML (`ML_SERVICE_TOKEN` en Laravel, `RECRUITMENT_ML_INTERNAL_TOKEN` en el servicio) | Alta |
| A-08 | Artefacto del modelo RF-29 y su *freeze* | Media |
| A-09 | Dataset sintético de F34 | Baja (sin datos personales) |
| A-10 | Disponibilidad de la aplicación y de la cola | Media |

## 3. Actores

| Actor | Confianza | Nota |
|---|---|---|
| Postulante | Baja | Accede solo a sus propios datos |
| Evaluador | Media | Solo sesiones asignadas de su organización |
| RR. HH. | Media | Configura vacantes y rúbricas de su organización |
| Aprobador/Dirección | Media-alta | Registra la decisión final (RF-23) |
| Solicitante | Media | Solicita vacantes (requerimientos); sin acceso a evaluaciones |
| Administrador de la organización (**actor conceptual futuro**) | Alta dentro de su tenant | **No es un rol implementado.** Los roles vigentes (`UserRole`) son solicitante, RR. HH., aprobador, evaluador y postulante; se modela por si una fase futura lo crea |
| Atacante externo | Ninguna | Sin cuenta o con credenciales robadas |
| Usuario de otro tenant | Baja respecto de este tenant | Riesgo cross-tenant |
| Desarrollador u operador | Alta | Acceso a código, despliegue y datos de prueba |
| Servicio ML (RF-29) | Limitada | Sin estado ni acceso a la base de datos |

## 4. Superficies y fronteras de confianza

```
[Navegador] ──TB-1 (HTTPS, sesión, CSRF)──> [Laravel + Inertia]
                                               │  Policies + scope organization_id
                                               ├──TB-2──> [PostgreSQL]  (sin RLS)
                                               ├──TB-3──> [Disco privado de CV]
                                               ├──TB-4──> [Cola / Redis]
                                               └──TB-5 (token interno, timeout, fallback)──> [FastAPI RF-29]
[Repositorio / CI] ──TB-6──> [Despliegue y datos de prueba]
[Futuro C] [Laravel] ──TB-7 (token pseudónimo, sin estado)──> [Extractor / localizador]   (BLOQUEADO)
```

| Frontera | Qué separa | Superficie |
|---|---|---|
| TB-1 | Usuario ↔ aplicación | Formularios, rutas, props de Inertia, descargas |
| TB-2 | Aplicación ↔ datos | Consultas Eloquent, scopes globales |
| TB-3 | Aplicación ↔ archivos | Subida y descarga de CV |
| TB-4 | Petición ↔ trabajo asíncrono | Trabajos de análisis |
| TB-5 | Laravel ↔ servicio ML | API interna `/v1/predict` |
| TB-6 | Desarrollo ↔ ejecución | Código, dependencias, secretos, datos de prueba |
| TB-7 | Laravel ↔ servicio inteligente futuro | Solo alcance C (bloqueado) |

## 5. Escala

- **Probabilidad:** Baja, Media o Alta.
- **Severidad:** Baja, Media, Alta o Crítica.
- **Riesgo inherente:** combinación de ambas antes de mitigar; **riesgo residual:** tras las mitigaciones propuestas, estimado en diseño (no medido).

## 6. Amenazas

| ID | STRIDE | Amenaza | Frontera | Probabilidad | Severidad | Mitigación (E = existente, P = propuesta para F35–F38) | Riesgo residual |
|---|---|---|---|---|---|---|---|
| T-01 | S | Suplantación de un evaluador con credenciales robadas para registrar valoraciones | TB-1 | Media | Alta | E: autenticación Fortify con 2FA disponible y passkeys; P: exigir 2FA a evaluadores y aprobadores | Medio |
| T-02 | S | Suplantación del servicio ML o llamada al servicio sin autorización | TB-5 | Baja | Media | E: las rutas `/v1/*` exigen el token interno (`X-Internal-Token`) y **fallan cerrado**: sin token configurado responden 503 y con credencial ausente o inválida, 401 (comparación en tiempo constante); solo `/health` queda abierto, sin datos del experimento; servicio en red interna; validación de respuesta y *fallback* en Laravel | Bajo |
| T-03 | T | **Manipulación de reglas**, criterios o rúbricas después de publicar la vacante | TB-1/TB-2 | Media | Alta | P: congelamiento al publicar (A-07), versiones inmutables, cambios solo como versión nueva auditada | Bajo |
| T-04 | T | **Data tampering**: alterar un resultado o una evidencia vinculada después del registro | TB-2 | Media | Crítica | E: registro único de `AssessmentResultRecorder`; P: evidencia `vinculada` inmutable, anotaciones de solo inserción, hash canónico | Bajo |
| T-05 | T | Borrar o reescribir eventos de análisis o registros de auditoría | TB-2 | Baja | Alta | E: trigger `audit_logs_append_only`; P: `analysis_run_events` de solo inserción con trigger equivalente | Bajo |
| T-06 | T | **Model tampering**: sustituir el artefacto del modelo RF-29 | TB-6 | Baja | Media | E: *freeze* con hash SHA-256 congelado; el modelo es informativo y no toca personas | Bajo |
| T-07 | T | **Poisoning** de los datos con los que se entrena o prueba (RF-29 o F34) | TB-6 | Baja | Media | E: datasets sintéticos con manifiesto SHA-256 y reproducibilidad verificada; P: revisión de cambios de datos en PR | Bajo |
| T-08 | R | Repudio de una valoración, de un descarte de alerta o de la decisión final | TB-1 | Media | Alta | E: `AuditLogger` en acciones críticas; RF-23 con justificación; P: auditar descartes de alertas con motivo | Bajo |
| T-09 | R/T | **Replay**: reenviar una petición de registro de resultado o de ejecución de análisis | TB-1/TB-4 | Media | Media | E: tokens CSRF y transición `PROGRAMADA` → `REALIZADA` que impide un segundo registro; P: idempotencia por clave en `analysis_run` | Bajo |
| T-10 | I | **Fuga cross-tenant**: consulta sin scope que devuelve datos de otra organización | TB-2 | Media | Crítica | E: scope global por `organization_id` y Policies por rol **y** organización; P: pruebas cross-tenant obligatorias en cada entidad nueva (sin RLS) | Medio |
| T-11 | I | **Exfiltración de CV y evidencias** por IDOR o descarga masiva | TB-1/TB-3 | Media | Crítica | E: disco privado y Policy de descarga; P: Policy en cada evidencia, límites de descarga y auditoría de accesos | Medio |
| T-12 | I | **Token leakage**: `ML_SERVICE_TOKEN`, cookies de sesión o tokens pseudónimos expuestos en repositorio, logs o frontend | TB-6/TB-1 | Media | Alta | E: secretos fuera de Git (contrato 8); P: escaneo de secretos en CI, tokens pseudónimos por ejecución y de un solo uso | Bajo |
| T-13 | I | **Logs con PII**: citas, justificaciones o datos del postulante en logs o en `analysis_run_events` | TB-2/TB-4 | Media | Alta | E: `AuditLogger` descarta claves sensibles de los metadatos (contrato 6); conserva usuario e IP, por lo que no es anónimo; P: minimización y limitación de propósito en metadatos y *payloads*, eventos solo con estado y código de error; revisión de logs en pruebas | Bajo |
| T-14 | I | Exposición excesiva en props de Inertia: citas o justificaciones enviadas a roles sin necesidad | TB-1 | Media | Alta | P: recursos por rol, pruebas de autorización sobre las props | Medio |
| T-15 | D | **Disponibilidad**: ejecuciones de análisis masivas saturan la cola o la base de datos | TB-4 | Media | Media | P: análisis asíncrono por vacante, límites de frecuencia, estados `fallido`/`expirado` | Bajo |
| T-16 | D | Caída o lentitud del servicio ML bloquea páginas | TB-5 | Media | Baja | E: *timeout*, reintentos acotados y *fallback*; la página funciona sin el servicio | Bajo |
| T-17 | E | **Abuso de privilegios**: un evaluador ve o califica sesiones no asignadas; RR. HH. edita una rúbrica publicada | TB-1 | Media | Alta | E: Policies existentes; P: Policies específicas por sesión asignada y por versión publicada | Bajo |
| T-18 | E | Escalada por asignación masiva de `role` u `organization_id` | TB-1 | Baja | Crítica | E: Form Requests con reglas explícitas; P: `organization_id` nunca desde la petición; pruebas de escalada | Bajo |
| T-19 | T | **Prompt injection futura**: instrucciones ocultas en un CV o documento procesado por un LLM o extractor | TB-7 | — (C bloqueado) | Alta | P (solo si se aprueba C): sin LLM sobre personas (D-17), salida como fragmentos confirmados por humanos, sin acciones del modelo | No aplica hoy |
| T-20 | T | Poisoning del corpus del localizador semántico futuro | TB-7 | — (C bloqueado) | Media | P (solo C): corpus sintético versionado con hash y auditoría de sesgo | No aplica hoy |
| T-21 | T/E | Deriva funcional: introducir un campo calculado sobre personas que alimente el ranking | TB-6 | Baja | Crítica | E: ADR-001, contrato 4, columnas prohibidas de RF-29; P: prueba de alcance y revisión de nombres en auditoría | Bajo |
| T-22 | T | Cadena de suministro: dependencia nueva vulnerable o maliciosa | TB-6 | Baja | Alta | E: B sin dependencias nuevas (G0-15); P: OSV y revisión de licencia para cualquier dependencia futura | Bajo |
| T-23 | I | Introducir datos reales en el dataset sintético o en datos de prueba | TB-6 | Baja | Alta | E: contrato 7; validadores PII de F34; P: revisión de datos en PR | Bajo |
| T-24 | D | Agotamiento de almacenamiento por documentos o evidencias masivas | TB-3 | Baja | Media | E: tipo PDF y tamaño máximo de CV; P: longitud máxima de citas y cuotas por postulación | Bajo |
| T-25 | T/E | **XSS persistente**: HTML o script guardado en citas, `evidence_text`, justificaciones o anotaciones que se ejecuta al renderizarse para otro usuario (RR. HH., evaluador o aprobador) | TB-1 | Media | Alta | E: React escapa por defecto el texto interpolado. P: escaping por defecto en toda vista de estos campos; **no renderizar HTML arbitrario** (sin `dangerouslySetInnerHTML`, que hoy solo usa el modal de 2FA para el código QR); texto plano o, si se admitiera formato, sanitización con lista blanca; validación de contenido y longitud en Form Requests; CSP y controles de frontend si el despliegue los adopta; pruebas de renderizado seguro con cargas como `<script>` y `<img onerror>` | Bajo |

## 7. Resumen

| STRIDE | Amenazas |
|---|---|
| S — Suplantación | T-01, T-02 |
| T — Manipulación | T-03 a T-07, T-19 a T-22, T-25 |
| R — Repudio | T-08, T-09 |
| I — Divulgación | T-10 a T-14, T-23 |
| D — Denegación de servicio | T-15, T-16, T-24 |
| E — Elevación de privilegios | T-17, T-18, T-21, T-25 |

**Riesgos residuales medios** (requieren pruebas en F35/F38 antes de reducirse): T-01, T-10, T-11 y T-14. Ninguno queda alto si se aplican las mitigaciones propuestas; ese juicio es de diseño y debe confirmarse con pruebas reales.

## 8. Qué falta para cerrar G0-09

1. Revisión del modelo por el equipo y registro de su aceptación (con observaciones, si las hay).
2. En F35 y F38, si G0 se aprueba, una prueba por cada mitigación propuesta, con prioridad para T-10, T-11, T-14, T-17 y T-25.
