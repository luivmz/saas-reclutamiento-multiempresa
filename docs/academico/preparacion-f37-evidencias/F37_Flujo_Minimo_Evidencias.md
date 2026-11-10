# F37 · Flujo mínimo de evidencias de una vacante

> **PREPARACIÓN — NO IMPLEMENTADA EN EL SAAS.** Documento del 08/11/2026, en la rama local `feature/continuacion-f36-f40`. Prepara la línea de evidencias que el equipo numera como F37. Corresponde a F37-SBX-A, que sigue **BLOQUEADA** (F36-SBX-GATE = NO SUPERADO). La numeración F36-SBX/F37-SBX frente al mapa F33 está pendiente (F36-M01).
>
> **No crea migraciones, modelos, Policies, rutas, endpoints ni pantallas, y no toca `app/`, `database/`, `resources/` ni `routes/`.** Lo ejecutable es un prototipo separado, en memoria y con la biblioteca estándar, sobre datos ficticios (§7).

## 1. Alcance vigente

| Fuente | Qué dice | Consecuencia para F37 |
|---|---|---|
| [Matriz de capacidades](../f36-sbx/F36SBX_Matriz_Capacidades.md) | EI-01 a EI-07 son ALLOWED, pero solo para F37-SBX y «F36-SBX-GATE SUPERADO y la capacidad incluida en la autorización del equipo (FG-03)» | Hoy no se puede implementar ninguna EI, ni dentro ni fuera del SaaS |
| La misma matriz, EI-23 | BLOCKED: «datos reales o integración productiva: endpoints, migraciones, UI o salidas hacia RF-21, RF-23 o RF-29». Una autorización sandbox sucesora no puede habilitarla | Integrar evidencias en el SaaS no cabe en F37-SBX: exige la G0 real y una decisión N5 ([roadmap §5](../f36-sbx/reconciliacion-gobierno/F36SBX_Roadmap_Propuesto_F36_F40.md), fila R7) |
| [Charter §4](../f36-sbx/F36SBX_Charter.md) | Prohibiciones que rigen «aunque el gate se supere» | Nada de lo que sigue puntúa, ordena, resume ni juzga a personas |
| [Contrato de evidencia v4](../f36-sbx/F36SBX_Contrato_Evidencia.md) | Tipos, marcadores, organizaciones `ORG-S1..S3`, campos prohibidos | El prototipo toma de ahí los tokens prohibidos, sin copiarlos |

**Lo que sí se puede hacer hoy:** diseñar, escribir ejemplos ficticios y modelar el flujo en un prototipo separado, que no implementa ninguna EI. Eso es lo que contiene esta carpeta.

## 2. Qué se reutiliza del SaaS

| Pieza existente | Archivo | Qué aporta | Uso en el flujo de evidencias | Hueco |
|---|---|---|---|---|
| Ámbito por organización | `app/Models/Scopes/OrganizationScope.php` y `app/Models/Concerns/BelongsToOrganization.php` | Filtra por `organization_id` toda entidad de negocio | Toda evidencia y todo enlace llevarían `organization_id` (R-01) | Faltan las tablas |
| Acceso al expediente interno | `ApplicationPolicy::viewFile` | RR. HH. y Dirección, solo de su organización | Base de «consultar» e «historial» (§4) | — |
| Acceso a un documento presentado (SEG-03) | `CandidateDocumentPolicy::download` (A-04, A-11 y A-12) | El personal llega a un CV solo a través de una postulación de su organización que lo presentó. El evaluador, solo con una sesión asignada | Es la misma regla de lectura de la evidencia que proviene de documentos | — |
| Asignación de evaluadores | `AuthorizesAssessmentSessions` (`isAssignedEvaluator`) | Evaluación o entrevista asignada a esa persona, en su organización | R-02 | — |
| Criterios de la vacante | `EvaluationCriterion` (`vacancy_id`, `organization_id`, `name`, `stage`, `weight`) | Los criterios explícitos y ponderados | Destino de cada enlace (R-03). Equivale al `criterion_id` del contrato | — |
| Observación del evaluador | `comment` de `EvaluationResult` e `InterviewResult` | Texto libre de una persona, junto a su puntaje | Patrón de la evidencia de tipo `observacion`. **La evidencia nunca se une al puntaje** (R-06) | — |
| Tipo de documento | `App\Enums\DocumentType` | Solo `cv` | EI-06 tomaría el tipo de los metadatos declarados | Faltan `certificado`, `transcripcion_revisada` y `observacion` |
| Auditoría | `AuditLogger`, `AuditAction` y trigger `audit_logs_append_only` | Registro de solo inserción, sin PII en los metadatos (DEF-17) | Cada escritura deja una fila con identificadores, nunca con el texto (R-07) | Faltan las acciones `evidencia.*` (§5) |
| Historial de solo inserción | `ApplicationStageHistory` | Cambios como filas nuevas | Patrón de la corrección por versiones (R-04) | — |
| Pruebas cross-tenant | `tests/Feature/**` | Patrón de prueba por organización | Las pruebas de §8 seguirían ese patrón | — |
| Ranking y decisión | `RankingService`, `FinalDecisionService` | RF-21 a RF-23 | **No se tocan.** La evidencia no los alimenta (EI-23 y RF-23) | — |

## 3. Flujo mínimo

Una evidencia es un **registro declarado por una persona** sobre una postulación: tipo, fuente y una descripción. El sistema no lee su contenido para decidir nada.

```
registrada ──revisar (RR. HH.)──▶ revisada
    │                                │
    ├──corregir──▶ versión nueva (la anterior queda «sustituida»)
    └──retirar (con motivo)──▶ retirada
enlazar / desenlazar con un criterio de la vacante: eventos aparte, en cualquier estado vigente
```

| Acción | Qué hace | Efecto |
|---|---|---|
| `registrar` | Alta de una evidencia con `type`, `source` y `description` | Evidencia nueva en `registrada` |
| `enlazar` | Una persona vincula la evidencia con un criterio de la misma vacante | Evento `evidencia.enlazada` |
| `desenlazar` | Retira ese vínculo | Evento `evidencia.enlace_retirado`; el anterior se conserva |
| `revisar` | RR. HH. confirma los metadatos declarados | `revisada` |
| `corregir` | Crea una versión nueva que sustituye a la anterior y hereda sus enlaces vigentes | La anterior pasa a `sustituida`, sin modificarse |
| `retirar` | Deja la evidencia sin efecto, con un motivo | `retirada`; sigue en el historial |
| `consultar` | Ver las evidencias de una postulación | Lectura |
| `historial` | Ver las filas de auditoría de esas evidencias | Lectura |

## 4. Permisos por rol

Lo que no figura está denegado. Toda acción exige además R-01 y, para el evaluador, R-02.

| Rol (`UserRole`) | registrar | enlazar / desenlazar | revisar | corregir | retirar | consultar | historial |
|---|---|---|---|---|---|---|---|
| RR. HH. (`rrhh`) | Sí: `cv`, `certificado` y `transcripcion_revisada` | Sí | Sí | Sí, salvo una `observacion`: solo la corrige su autor, y RR. HH. puede retirarla con motivo | Sí | Sí | Sí |
| Dirección (`aprobador`) | No | No | No | No | No | Sí | Sí |
| Evaluador (`evaluador`) | Solo `observacion`, en postulaciones asignadas | Sí, en postulaciones asignadas | No | Solo sus observaciones | No | Sí, en postulaciones asignadas | No |
| Área solicitante (`solicitante`) | No | No | No | No | No | No | No |
| Postulante (`postulante`) | No | No | No | No | No | No (DEF-14: ve su estado, no el expediente interno) | No |

**Dirección solo consulta.** La decisión final sigue siendo suya y humana (RF-23): la evidencia la informa, pero ni la sustituye ni alimenta el ranking.

## 5. Reglas

| ID | Regla | Escenarios |
|---|---|---|
| R-01 | **Aislamiento.** La organización de quien actúa, la de la postulación, la de su vacante y la de la evidencia coinciden. Otra organización siempre se deniega, en cualquier acción | ESC-11 a ESC-13, ESC-33 y la prueba exhaustiva |
| R-02 | **Asignación.** El evaluador solo actúa sobre postulaciones en las que tiene una sesión asignada | ESC-02, ESC-16 y ESC-32 |
| R-03 | **Criterio de la misma vacante.** Un enlace solo apunta a un criterio de la vacante de la postulación; nunca a otra vacante ni a otra organización | ESC-14, ESC-15 y ESC-31 |
| R-04 | **Solo inserción.** Ningún registro se modifica ni se borra. Corregir crea una versión nueva; retirar y desenlazar son eventos nuevos | ESC-06, ESC-09, ESC-18, ESC-26 a ESC-28 |
| R-05 | **Sin campos sobre la persona ni de juicio.** En ninguna escritura, un nombre de campo contiene un token de `forbidden_field_tokens` del contrato v4 (`score`, `rank`, `select`, `name`, `level`…), tampoco en camelCase | ESC-23 y ESC-34 |
| R-06 | **Sin salidas hacia RF-21, RF-23 ni RF-29.** La evidencia no entra en el cálculo del ranking ni en la decisión | Por construcción: el prototipo no tiene esa salida |
| R-07 | **Auditoría sin texto.** Cada escritura deja una fila con acción, actor, evidencia, postulación y criterio, nunca con la descripción | Prueba `test_la_auditoria_no_lleva_texto_de_la_evidencia` |
| R-08 | **Vacante cerrada, evidencia congelada.** Con la vacante `cerrada` se puede leer, pero no escribir | ESC-10 y ESC-22 |
| R-09 | **Entrada cerrada.** Texto con el marcador `[SINTÉTICO]` y una sola fuente por tipo: `documento_presentado` para `cv` y `certificado`; `sesion_asignada` para `transcripcion_revisada` y `observacion`. Sin URL ni fuentes externas | ESC-24, ESC-25 y ESC-35 a ESC-37 |
| — | **Falla cerrado.** Un actor, una postulación o una evidencia desconocidos se deniegan | ESC-29 y ESC-30 |

Las acciones de auditoría candidatas son `evidencia.registrada`, `evidencia.enlazada`, `evidencia.enlace_retirado`, `evidencia.revisada`, `evidencia.corregida` y `evidencia.retirada`. Una prueba comprueba que **todavía no existen** en `AuditAction`.

## 6. Ejemplos ficticios

[`ejemplos/f37_ejemplos_ficticios.json`](ejemplos/f37_ejemplos_ficticios.json) contiene:

- dos organizaciones (`ORG-S1` y `ORG-S2`);
- nueve usuarios ficticios, que cubren los cinco roles;
- tres vacantes, una de ellas cerrada, con sus criterios;
- cuatro postulaciones y tres asignaciones de evaluador;
- cuatro evidencias iniciales;
- **38 escenarios** con su resultado esperado: 12 permitidos y 26 denegados.

Los textos empiezan por `[SINTÉTICO]`. No hay correos, teléfonos, números de documento ni nombres de personas.

## 7. Prototipo separado

| Archivo | Qué es |
|---|---|
| [`prototipo/f37_flujo_evidencias.py`](prototipo/f37_flujo_evidencias.py) | Modelo en memoria del flujo, la matriz y las reglas R-01 a R-09. Solo biblioteca estándar |
| [`prototipo/test_f37_flujo_evidencias.py`](prototipo/test_f37_flujo_evidencias.py) | 23 pruebas: escenarios, aislamiento exhaustivo, flujo completo, corrección autorizada por la evidencia original, solo inserción, auditoría sin texto y coherencia con el SaaS (`UserRole` y `AuditAction`) |

```
python -I -B docs/academico/preparacion-f37-evidencias/prototipo/f37_flujo_evidencias.py
python -I -B -m unittest discover -s docs/academico/preparacion-f37-evidencias/prototipo -v
```

**Lo que no hace:** no implementa ninguna EI. No organiza por tipo o criterio (EI-01), no genera alertas (EI-02), no comprueba la integridad de las citas (EI-03), no desglosa (EI-04), no detecta PII (EI-05), no infiere el tipo (EI-06) y no busca (EI-07). Tampoco persiste nada ni se conecta con Laravel.

**Ablaciones verificadas** (08/11/2026). Se desactivó cada regla en una copia y se restauró después. La suite falló en los seis casos:

| Ablación | Pruebas fallidas |
|---|---|
| Sin R-01 | 5 |
| Sin R-02 | 3 |
| Sin R-08 | 2 |
| Sin R-05 | 2 |
| Sin herencia de enlaces al corregir | 1 |
| Con `consultar` para el postulante | 1. La primera vez sobrevivió, porque R-01 la cubría; se añadió la prueba que fija la matriz |

## 8. Qué existe y qué falta para integrarlo

**Existe:** esta especificación, los ejemplos ficticios, el prototipo con sus pruebas y las piezas reutilizables del SaaS (§2).

**Falta, en dos niveles con requisitos distintos:**

| Nivel | Qué falta | Requisito exacto |
|---|---|---|
| A. Sandbox F37-SBX-A, fuera del producto | Llevar el modelo al patrón de F35-SBX (`docs/academico/tools/`, almacén efímero), implementar las EI autorizadas sobre el contrato v4 con RED/GREEN y el preregistro del plan de evaluación | F36-SBX-GATE = SUPERADO, anclado en H, con FG-02, FG-03 (lista cerrada de EI), FG-10 y FG-12. Antes: auditoría de S, D-10 determinada y D-02b ([S §7 y §11](../f36-sbx/expediente-final/F36SBX_B01_Especificacion_S.md)) |
| B. SaaS (producto) | Migraciones `evidence_items` y `evidence_links` con `organization_id`; modelo con `BelongsToOrganization`; `EvidencePolicy` con R-01 a R-03 y R-08; servicio de solo inserción; casos nuevos en `DocumentType` y `AuditAction`; controlador, rutas y pantalla; pruebas Feature de autorización y cross-tenant; Cypress | **Bloqueado en F37-SBX (EI-23).** Exige la G0 real (G0-02, G0-03 y G0-12 PENDIENTE EXTERNO), un ADR de alcance y la decisión N5 de integración productiva (roadmap, fila R7). Ninguna autorización sandbox lo habilita |

**Cómo se verificaría la integración, cuando proceda:** cada escenario de §6 se convertiría en una prueba Feature con usuarios de dos organizaciones, siguiendo el patrón cross-tenant del proyecto. La matriz de §4 se convertiría en una prueba de la Policy, y R-04 en una prueba de que la tabla no admite `UPDATE` ni `DELETE`, como el trigger de auditoría.

## 9. Puntos para la auditoría

1. Que nada de esta carpeta implemente una EI ni toque el runtime del SaaS.
2. Que la matriz de §4 sea coherente con las Policies vigentes (`viewFile`, `CandidateDocumentPolicy` y `AuthorizesAssessmentSessions`).
3. Que los requisitos de §8 sean los exactos: el nivel B no es alcanzable en F37-SBX.
4. Que los ejemplos sean ficticios y que el prototipo use solo la biblioteca estándar.
