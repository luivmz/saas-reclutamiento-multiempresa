# F35-SBX-A — Alcance, objetivos y exclusiones

> Fase F35-SBX-A, versión 1 (07/10/2026). Base fija: main `b67f6443fb2bb71e736a60a645a15bd1fa0e7de6`, posterior al cierre de F34E y al handoff macOS. Rama: `feature/f35-sbx-synthetic-evidence-pipeline`.

## 1. Nombre formal

**F35-SBX-A — Diseño, contrato y validación del pipeline experimental de evidencia sintética (alcance B, sandbox).**

## 2. Objetivo

Definir, documentar y verificar de forma automática un pipeline de evidencia sintética aislado, auditable y reproducible: esquema, comprobaciones synthetic-only, hashes, provenance, tenant, revisión humana simulada, auditoría y retención. Nada de esta fase se ejecuta sobre el runtime ni evalúa a personas. Su salida es un contrato y un validador contra los que F35-SBX-B se implementará.

| ID | Objetivo |
|---|---|
| O1 | Contrato JSON cerrado: exactamente los campos permitidos |
| O2 | Provenance verificable desde cada evidencia hasta su fila F34 de origen |
| O3 | Aislamiento por tenant sintético ORG-S1, ORG-S2 y ORG-S3 |
| O4 | Fail-closed en cada comprobación: lo desconocido falla |
| O5 | Ninguna capacidad prohibida en contrato, fixtures ni documentos |
| O6 | La puerta G0-SBX sigue vigente después de la entrega |

## 3. Alcance

| Permitido en F35-SBX-A | Entregable |
|---|---|
| Documentación | Los diez documentos de este directorio |
| Contrato JSON cerrado | [`contrato/f35sbx_contract.json`](contrato/f35sbx_contract.json) |
| Fixtures sintéticos pequeños | Dos evidencias por organización, derivadas de F34 ([`fixtures/`](fixtures/manifest.json)) |
| Manifest | SHA-256 y tamaño de cada artefacto, referencias F34 y regla de selección |
| Validador | [`validate_f35sbx.py`](../tools/f35sbx/validate_f35sbx.py), solo biblioteca estándar |

## 4. Exclusiones

| Prohibido en F35-SBX-A | Motivo |
|---|---|
| Datos reales, PII, CV, documentos, audio o vídeo reales | Contrato 7; regla de datos de ADR-005 |
| Biometría o inferencias de emoción, personalidad, honestidad, inteligencia o estrés | ADR-005 §6.7 |
| Scoring, ranking automático nuevo, recomendación, «mejor candidato» o selección automática | Contratos 2 y 4; ADR-001 |
| Modificar RF-23 o reinterpretar RF-21 | RF-23 humana; RF-21 vigente |
| OCR, parsing, extracción automática, embeddings o búsqueda semántica | Alcance C, BLOQUEADO |
| Endpoints, migraciones, tablas productivas o cualquier enlace con el runtime | SBX-15 y SBX-16 |
| Pipeline ejecutable, SQLite o almacenamiento temporal | Corresponden a F35-SBX-B (DH-04, DH-07) |
| Cambios en `app/`, `routes/`, `config/`, `database/`, `resources/`, `tests/`, `cypress/` o `ml-service/` | Fuera de F35-SBX |
| Cambios de CI | DH-08 |
| F36–F40, también en sandbox | Requieren autorización propia |
| Presentar F35-SBX como aprobación jurídica, de privacidad o institucional | G0-02, G0-03 y G0-12 siguen PENDIENTE EXTERNO |

Las alertas deterministas (CAP-34) y el acuerdo entre evaluadores (CAP-33) pertenecen al alcance B de F33, pero no figuran en el alcance autorizado de F34E: quedan fuera de F35-SBX-A.

## 5. Decisiones humanas

Registradas por el equipo el 07/10/2026 al autorizar la fase.

| Decisión | Resultado |
|---|---|
| DH-01 | F35-SBX-A abierta formalmente |
| DH-02 | Adaptación mínima de `validate_f34b.py` y `validate_f34e.py`: solo `evidencia-sbx/**` (Markdown o JSON) y `tools/f35sbx/**` (Python), con contenido de texto comprobado y negativos propios |
| DH-03 | Carpetas `docs/academico/evidencia-sbx/` y `docs/academico/tools/f35sbx/` |
| DH-04 | Solo documentación, contrato cerrado, fixtures pequeños, manifest y validador; el pipeline ejecutable corresponde a F35-SBX-B |
| DH-05 | La revisión humana simulada solo cubre integridad y procedencia (`review_scope = integridad_y_procedencia`, valor único) |
| DH-06 | Ningún identificador de persona (`APP-`, `PER-S-` ni otros); solo referencias de evidencia, tenant, criterio y origen F34 |
| DH-07 | Solo JSON versionado, fixtures, manifest y hashes; SQLite en memoria y almacenamiento temporal quedan para F35-SBX-B |
| DH-08 | Sin cambios de CI; la regresión local completa es el gate |
| DH-09 | Gobierno: al inicio solo se registra que F35-SBX-A está iniciada; el estado final se registra al cierre, sin cambiar ningún estado G0 |

Ampliaciones de alcance decididas por el equipo el 07/10/2026, sin commit intermedio de gobierno:

| Decisión | Resultado |
|---|---|
| DH-10 | Adaptación mínima de `validate_f30.py`, `validate_f33.py` y `validate_f34.py`: admiten solo `CLAUDE.md` y `docs/PROGRESS.md` con exactamente la apertura de F35-SBX-A |
| DH-11 | Esas tres rutas exactas entran en las listas de `validate_f34b.py`, `validate_f34e.py` y `validate_f35sbx.py`, con su contenido comparado con la base; las excepciones exigen la rama F35-SBX y la base como ancestro de HEAD, no HEAD igual a la base |
