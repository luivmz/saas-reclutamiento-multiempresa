# Fase 26 — Release, GitHub y cierre final de v1.1

**Fecha:** 25 de septiembre de 2026
**Rama:** `feature/phase-26-release-closeout` · **Base:** `2b97fe3` (cierre de la Fase 25)
**Writer principal:** Claude Code · **Auditor final e integrador:** Codex

> Fase de **cierre**, sin desarrollo. No cambia código, pruebas, base de datos, dependencias, ML ni modelos de PowerDesigner. **No se crea ninguna etiqueta ni release, ni se hace merge a `main`:** esta fase prepara todo y deja la decisión a la auditoría y al equipo. Documentos hermanos: [`../../CHANGELOG.md`](../../CHANGELOG.md) · [`release-notes-v1.1.md`](release-notes-v1.1.md) · [`release-manifest-v1.1.md`](release-manifest-v1.1.md) · [`final-acceptance-checklist.md`](final-acceptance-checklist.md).

---

## 1. Objetivo

Responder: *¿la v1.1 está lista para cerrarse formalmente, etiquetarse, documentarse y entregarse como versión académica consolidada?*

**Sí, con observaciones LOW e INFO documentadas (§12–13).** No queda trabajo técnico pendiente. Lo que falta es la auditoría y la decisión explícita del equipo sobre `main` y la etiqueta (§14–16).

## 2. Baseline

| | |
|---|---|
| `develop` = `origin/develop` = base | `2b97fe36d25fd3911bc2e4e1e24c6ab16200179a` (*merge: close phase 25 final qa*), idéntico en contenido a `7a04682` |
| `main` = `origin/main` | `4563c696ba08fd6d2a689af733020d849edebad2` (v1.0 más dos correcciones posteriores a la publicación) |
| `v1.0.0-academic` | Tag anotado `6e03f20` sobre `9a946c202ef7473230e8efa371ace13479ab889c`, intacto |
| Preflight | `git fetch`: `origin/develop` sin cambios, árbol limpio. Rama creada desde `develop` |

## 3. Estado del roadmap

| Fases | Estado | Merge |
|---|---|---|
| F0–F12 | v1.0 académica, cerrada y publicada | `9a946c2` (tag) |
| F13–F22 | Cerradas e integradas | `95c5b8b` … `2621bee` |
| F23 | Cerrada e integrada | `8211851` |
| F24 | Cerrada con observaciones e integrada | `4469128` |
| F25 | **Cerrada con observaciones e integrada** | `2b97fe3` |
| F26 | Implementada en su rama, **pendiente de auditoría** | — |

No hay Fase 27, salvo que el equipo la decida.

## 4. Alcance final de v1.1

La v1.1 es la v1.0 más:

- **ML y su integración:**
  - un servicio experimental de riesgo operacional (RF-29) y su integración con Laravel;
  - el plazo objetivo del proceso, con GAP-01 resuelto técnicamente.
- **Interfaz:**
  - rediseño de la interfaz;
  - *motion* accesible;
  - CSS 3D decorativo en la portada;
  - QA visual y de accesibilidad.
- **Modelado y documentación:**
  - especificación UML y modelos de PowerDesigner;
  - Formato 09 v1.1.
- **QA global:** con dos correcciones MEDIUM.

**Fuera de alcance, y no implementado:**

- RF-28;
- productivizar RF-29;
- RNF-C;
- RLS, microservicios, facturación, *Talent Pool* y despliegue en la nube.

## 5. Arquitectura final

- **Base:** monolito modular Laravel 13.31 (PHP 8.4.25) + React 19.3, TypeScript 5.9, Inertia 3 y Tailwind 4.3, sobre PostgreSQL 17.11 y Redis 7.4.11, en Docker Compose.
- **Multiempresa lógica:** `organization_id`, *scopes* globales y 7 Policies que comparan rol y organización.
- **Auditoría:** de solo inserción, con un *trigger* en la base.
- **CV:** en el disco privado `local`.
- **Servicio ML externo y experimental:**
  - Python 3.12, scikit-learn 1.9.1 y FastAPI 0.115.6, fuera de Compose;
  - Laravel lo llama por HTTP interno con token solo si `ML_SERVICE_ENABLED=true`;
  - si falla, cae a `descriptive_only` o `unavailable` sin romper el flujo.

La especificación está en [`uml/`](uml/) y la formalización en [`powerdesigner/`](powerdesigner/).

## 6. RF y RNF finales

| Elemento | Estado final |
|---|---|
| RF-01 a RF-27 | **Línea base oficial**, con el mismo número y significado que en v1.0 |
| RF-23 | Decisión final **humana**: Aprobador / Dirección, con confirmación explícita y justificación |
| RF-28 | **Candidato no implementado** |
| RF-29 | **Experimental**: riesgo de demora del proceso; no productivo, no evalúa personas, no se persiste. Sigue siendo **candidato** |
| RNF-C | **Propuesta** |
| Promoción de RF-28, RF-29 y RNF-C | Decisión pendiente del equipo (preguntas 12 y 13 de [`scope-preliminary.md`](scope-preliminary.md)); la Fase 26 no la toma |

## 7. ML final

| Aspecto | Valor |
|---|---|
| Modelo | `Pipeline(StandardScaler, LogisticRegression C=10.0, class_weight=None)`, sin calibración |
| *Freeze* | `9ee1843055e75d4039dd84fd666db7a594e1a45ec7e9b354820fabfcb21ebcd2` |
| *Threshold* | `0.1679418172266036` |
| Veredicto científico (15B) | `PREDICTIVE GO WITH LIMITATIONS`, con datos **sintéticos** |
| Contrato | *Request* de 15 enteros (`extra="forbid"`, `strict`); respuesta de 6 campos, sin incertidumbre |
| Estado | Experimental; sin validación institucional ni autorización de producción |
| Frontera | Solo proceso; sin efecto en etapa, ranking ni decisión (verificado en la F25, también en vivo) |

## 8. Resultados de QA

La línea base auditada es la de la Fase 25 ([`phase-25-final-qa.md`](phase-25-final-qa.md)). La **F26 no la vuelve a ejecutar**: no cambia código.

| Suite | Resultado |
|---|---|
| PHPUnit | 411 superadas · 8 omitidas · 0 fallidas · 1498 aserciones |
| pytest | 533 superadas |
| Componentes | 42/42 |
| TypeScript | 0 errores |
| *Build* | Correcto |
| Cypress | 20 specs · 85/85 |

**Corrección a la Fase 25.** Su informe dice que el build no tiene avisos. En realidad, el plugin `laravel:fonts` muestra en cada build un aviso informativo: «Optimized font fallbacks require the optional "fontaine" package». La búsqueda de la F25 filtraba por «warn» y no lo captó. Es INFO y no un error (§12, A-01); la F26 lo reprodujo con `npm run build`.

## 9. Seguridad y multitenencia

Verificado en la Fase 25 y sin cambios desde entonces:

- sin fugas entre organizaciones: 22 pruebas cross-tenant explícitas, `CrossTenantAccessTest`, `OrganizationScopeTest`, `MlCrossTenantValidationTest` y E2E-11;
- roles y RF-23 correctos;
- CV protegido;
- auditoría de solo inserción.

Barrido final de secretos de la F26:

- sin claves, tokens ni `APP_KEY` versionados;
- `.env` y `.env.e2e` ignorados;
- los únicos `.sql` versionados son la creación de dos bases vacías y el esquema sin datos;
- no hay basura rastreada.

## 10. Artefactos académicos

- **Formato 09 v1.1:** DOCX (2 576 008 B) y PDF (2 099 904 B, 28 páginas) en `docs/academico/phase-24/output/`, sin regenerar. Sus hashes están en el [manifiesto](release-manifest-v1.1.md).
- **Originales:** los tres tienen el mismo SHA-256 registrado en la Fase 24.
- **Validador:** 93 comprobaciones OK en la F25.

## 11. UML y PowerDesigner

- **UML:** 19 `.puml`.
- **PowerDesigner:**
  - OOM (20 diagramas) y PDM (2);
  - 22 PNG y 22 SVG.
- No se abrió PowerDesigner ni se tocaron los modelos nativos.

## 12. Deuda aceptada

Clasificación: **ACCEPTED** (se acepta tal cual), **DEFERRED** (queda para después, con destino), **RESOLVED** (resuelta, con evidencia) o **NOT APPLICABLE**.

| # | Origen | Ítem | Sev. | Clasificación | Justificación y destino |
|---|---|---|---|---|---|
| A-01 | F25 | Aviso opcional de Fontaine en el build | INFO | ACCEPTED | Informativo. Instalar `fontaine` sería una dependencia nueva (prohibida en el cierre) y desactivar `optimizedFallbacks` cambiaría la configuración. El build es correcto |
| A-02 | F25 | Pint: 8 archivos PHP (`Vacancy`, `AppServiceProvider`, `AssessmentResultRecorder`, `bootstrap/app.php`, `DemoSeeder`, `routes/web.php` y 2 pruebas), unas 24 líneas; orden de imports, import sin uso, FQCN y espacios | LOW | DEFERRED | Poco *churn*, pero es **código** y obligaría a repetir la regresión en una fase documental. El CI no lo verifica. Destino: *hotfix* de estilo posterior al release, con `pint` y PHPUnit |
| A-03 | F25 | `vp check`: 154 archivos | LOW | ACCEPTED (global) / DEFERRED (código) | Solo **5** son código (`resources/js`); el resto es Markdown: 49 de `docs/v1.1`, 30 de `docs/final-report` (historia de v1.0, **no se reescribe**), 28 de `.claude/skills` (incluye skills externas con procedencia, **no se modifican**), 25 de Cypress y otros sueltos. Un `--fix` global violaría contratos. Si se hace, solo `resources/js` y `cypress/`, con Vitest y Cypress |
| A-04 | F25 | Lector de pantalla real | INFO | DEFERRED | NVDA no está instalado y el Narrador no se puede verificar desde una sesión automatizada. Prueba manual del equipo |
| A-05 | F25 | Rendimiento en hardware modesto | INFO | DEFERRED | El equipo de QA no es modesto. Prueba manual o con limitación documentada |
| A-06 | F25 | Validación manual independiente a 375 px | INFO | DEFERRED | La F25 lo verificó por automatización (60 mediciones, E2E-16 ampliado); falta una revisión humana en un dispositivo real |
| B-01 | F24 L-01 | Contexto de 10 RNF académicos frente a 11 técnicos | LOW | ACCEPTED | Divergencia declarada en `phase-24`; unificar el catálogo es decisión del equipo |
| B-02 | F24 L-02 | Seis rótulos de RF abreviados en el Formato 09 | LOW | ACCEPTED | RF-01 a RF-27 presentes y sin renumerar (validador de la F25). No se regenera el DOCX en el cierre |
| B-03 | F24 L-03 | Conteo XML/RELS | LOW | ACCEPTED | Sin efecto en el documento entregado |
| B-04 | F24 I-01 | Sin validación contra XSD | INFO | ACCEPTED | Validación estructural propia (`validate_f9.py`) y apertura en Word |
| B-05 | F24 I-02 | Densidad visual de los anexos | INFO | ACCEPTED | Estético |
| C-01 | F23 | Metadatos con rutas absolutas locales en los modelos nativos | LOW | ACCEPTED | No impiden abrir los modelos (verificado en la F23). No se tocan nativos en el cierre |
| C-02 | F23 | Pestaña `critical` de SEQ-02 | LOW | ACCEPTED | Cosmético; el dato está completo en el modelo |
| C-03 | F23 | Rótulos `[sí]`/`[no]` de AC-01 rozados por flechas | LOW | ACCEPTED | Cosmético |
| C-04 | F23 | 21 diferencias justificadas F22 ↔ PowerDesigner | INFO | NOT APPLICABLE | No son deuda: son diferencias de representación, justificadas en `f22-checklist.md` |
| D-01 | F23 O-01 | `evaluation_criteria.position` fuera de CL-01 | INFO | ACCEPTED | Es un `smallint` con valor 0 por defecto que **solo ordena la presentación** de los criterios (`orderBy('position')`). No interviene en reglas de negocio ni en el ranking y figura en el PDM. Es una diferencia documental de la vista conceptual; sin cambio en los nativos |
| D-02 | F23 O-04 | Modelos de prueba `zz_*` | INFO | **RESOLVED** | No estaban versionados ni dentro del repositorio: solo en la carpeta temporal del trabajo de Claude Code. Se borraron en la F26 (11 `zz_*.oom`, 2 `probe*.oom` y `copia-oom.oom`, 14 archivos), como autoriza el §10 del encargo. No eran evidencia ni estaban referenciados por ningún artefacto |
| D-03 | F25 | Motivo `server_error` para 401 | INFO | ACCEPTED | Diseño documentado y probado (Fase 16) |
| D-04 | F25 | IDs de hallazgo por fase (`F25-M01`…) en lugar de `DEF-14+` en `defects.md` | INFO | ACCEPTED | Convención de v1.1: cada fase registra sus defectos en su documento (F21 y F25); `defects.md` es el registro de v1.0 y no se reescribe |

## 13. Riesgos residuales

### Residual Risk Summary

| Severidad | Abiertos | Detalle |
|---|---|---|
| BLOCKER | **0** | — |
| HIGH | **0** | — |
| MEDIUM | **0** | F25-M01 y F25-M02, corregidos y verificados |
| LOW | 8 | A-02 y A-03 (formato); B-01 a B-03 (F24); C-01 a C-03 (F23) |
| INFO | 9 | A-01, A-04, A-05 y A-06; B-04 y B-05; D-01, D-03 y D-04. Aparte: D-02 RESOLVED y C-04 NOT APPLICABLE |

**Riesgo de producto:** el principal riesgo residual no es técnico sino de **interpretación**. Un lector podría confundir RF-29 con una evaluación de personas o creer que está listo para producción. Lo mitigan:

- el rótulo «Experimental» y el aviso de decisión humana en la tarjeta;
- los avisos en el README, las notas de versión y el Formato 09;
- las pruebas que impiden hablar de candidatos o de ranking (E2E-15).

**Riesgo de proceso:** el CI de GitHub corre build, `tsc` y PHPUnit, pero **no** pytest, Vitest ni Cypress. Esas suites se validaron localmente en la F25.

## 14. Estrategia Git

| Paso | Quién | Estado |
|---|---|---|
| 1. Auditar `feature/phase-26-release-closeout` | Codex | Pendiente |
| 2. Integrar F26 en `develop` con `--no-ff`, como en todas las fases | Codex o el equipo, con autorización | **No ejecutado** |
| 3. Decidir y ejecutar la estrategia de `main` (§15) | Equipo, con autorización explícita | **No ejecutado** |
| 4. Crear la etiqueta y el GitHub Release (§15–16) | Equipo o Codex, con autorización | **No ejecutado** |

Ni *push*, ni *merge*, ni etiqueta en esta fase (contrato 10 de `CLAUDE.md`).

## 15. Estrategia de etiqueta y de `main`

**Etiqueta propuesta:** `v1.1.0-academic`, **anotada**, con el mismo formato que `v1.0.0-academic`: *«Academic release v1.1.0 - SaaS recruitment platform»*. **No se mueve `v1.0.0-academic`.**

**Opciones analizadas:**

| | A) Etiqueta sobre `develop`, `main` congelado en v1.0 | B) Merge controlado `develop → main` y etiqueta sobre `main` |
|---|---|---|
| Coherencia con la historia | Rompe el patrón: la v1.0 se publicó con un **merge `--no-ff` de `develop` en `main`** (`9a946c2`, «release: publish academic MVP v1.0») y la etiqueta está **sobre ese merge de `main`** | **Repite el patrón de la v1.0** |
| Qué ve GitHub | La rama por defecto (`main`) seguiría mostrando la v1.0 y el README de la v1.0 | La rama por defecto muestra la versión vigente |
| Riesgo | Ninguno técnico | Bajo. El merge es limpio: simulado con `git merge-tree`, **sin conflictos**, y el árbol resultante es **idéntico al de `develop`** (`f945b8d`). `main` solo tiene un commit que `develop` no tiene (el merge `4563c69`, cuyo contenido ya está en `develop`) |
| v1.0 | Intacta en `main` y en su etiqueta | Intacta en su etiqueta (`9a946c2`), que es la referencia histórica. `main` avanza, pero la historia no se reescribe |
| CI | Se ejecuta en `develop` | Se ejecuta en `main` al integrar: build, `tsc` y PHPUnit |

**Recomendación: opción B**, condicionada a la auditoría de Codex y a la autorización explícita del equipo:

1. Integrar F26 en `develop` con `git merge --no-ff feature/phase-26-release-closeout`.
2. Desde `main`, hacer el merge de `develop` con `--no-ff` y el mensaje «release: publish academic v1.1».
3. Crear en ese merge la etiqueta `git tag -a v1.1.0-academic -m "Academic release v1.1.0 - SaaS recruitment platform"`.
4. Hacer *push* de `main`, `develop` y la etiqueta, y comprobar que el CI de `main` pasa.

Motivos:

- es el mismo procedimiento con el que se publicó la v1.0;
- deja la rama por defecto de GitHub en la versión vigente;
- la v1.0 queda preservada por su etiqueta, que no se mueve.

La opción A solo conviene si el equipo quiere que `main` siga mostrando la v1.0 como entrega evaluada. En ese caso, la etiqueta se pone sobre el merge de F26 en `develop`.

Al ejecutar la opción B, la frase de `CLAUDE.md` «`main` sigue siendo la v1.0 académica y no contiene v1.1» deberá actualizarse en el mismo cierre, conservándola como historia.

## 16. Estrategia de GitHub Release

| Campo | Propuesta |
|---|---|
| Título | `v1.1 académica — Plataforma SaaS multiempresa de reclutamiento` |
| Etiqueta | `v1.1.0-academic` |
| Cuerpo | [`release-notes-v1.1.md`](release-notes-v1.1.md). Los enlaces relativos deben convertirse en enlaces absolutos a la etiqueta al pegarlos en GitHub |
| Artefactos adjuntos | `F9_Alcance_Proyecto_Software_Colegio_Andino_FINAL_v1.1.pdf` (2,1 MB) y `F9_…_FINAL_v1.1.docx` (2,6 MB). Opcionales: PNG de UC-01, CO-01 y DE-01 |
| No adjuntar | Binarios del runtime, `vendor`, `node_modules`, el modelo ML (se reconstruye desde el protocolo congelado y no se versiona), `.env*` ni modelos nativos: ya están en el repositorio |
| Marca | *Pre-release*: **no**, es la entrega académica final. Aviso de «no productivo» en la primera línea del cuerpo |
| Herramienta | `gh` **no** está instalado en el equipo: se crea desde la web de GitHub o lo hace quien integre |

## 17. Criterios de cierre

Lista completa: [`final-acceptance-checklist.md`](final-acceptance-checklist.md). En resumen:

- Git limpio;
- `develop`, `main` y `v1.0.0-academic` intactos;
- QA de la F25 en verde;
- contratos preservados;
- artefactos académicos y de modelado presentes;
- documentos de release listos;
- deuda clasificada;
- sin secretos;
- estrategias propuestas.

**Pendiente:** la auditoría de la F26 y la aprobación de las estrategias de etiqueta y de `main`.

## 18. Handoff final

**Para Codex (auditoría final):**

1. Revisar el diff de `feature/phase-26-release-closeout`: solo documentación de cierre y el README.
2. Verificar:
   - los hashes del manifiesto contra los blobs;
   - la clasificación de la deuda (§12);
   - la ausencia de secretos;
   - que `develop`, `main` y la etiqueta de la v1.0 no se movieron.
3. Aprobar o ajustar la recomendación B y, **solo con autorización del equipo**, ejecutar la estrategia Git (§14–15) y el release (§16).
4. Tras el release, actualizar `CLAUDE.md`, `PROGRESS.md` y la lista de aceptación: F26 cerrada, v1.1 publicada.

**Después del cierre**, solo con una fase nueva y autorizada: el *hotfix* de estilo (A-02 y A-03 de código), las pruebas manuales (A-04 a A-06) y las decisiones del equipo sobre RF-28, RF-29, RNF-C y los catálogos de RNF y CU.
