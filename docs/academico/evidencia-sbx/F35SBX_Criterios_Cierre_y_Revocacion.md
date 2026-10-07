# F35-SBX-A — Criterios de aceptación, cierre y revocación

> Fase F35-SBX-A, versión 1 (07/10/2026). Ningún validador cierra la fase por sí solo: el cierre lo registra el equipo tras su auditoría.

## 1. Criterios de aceptación

| ID | Criterio |
|---|---|
| ACS-01 | Existen los diez documentos y los cinco artefactos de la fase |
| ACS-02 | Los estados críticos se declaran una sola vez en el README y coinciden con la puerta G0-SBX vigente |
| ACS-03 | El contrato publicado es cerrado e idéntico al que construye el validador |
| ACS-04 | Los fixtures llevan los seis marcadores synthetic-only, sin PII, media ni tokens de persona |
| ACS-05 | Cada amenaza TSB tiene control, evidencia y casos negativos existentes |
| ACS-06 | `validate_f35sbx.py` termina sin fallas, con al menos 45 casos negativos y el control no forzado |
| ACS-07 | `validate_f34e.py` termina sin fallas: G0-SBX vigente con SBX-01..SBX-18 en CUMPLE |
| ACS-08 | La regresión académica local completa termina sin fallas (gate de DH-08) |
| ACS-09 | Sin cambios en runtime, baseline RF/CU/RNF, F33, F34, F34A ni en las evidencias F34B, F34C, F34D o F34E |
| ACS-10 | DH-01 a DH-09 registradas en el [alcance](F35SBX_Alcance.md#5-decisiones-humanas) |

## 2. Criterios de cierre

1. ACS-01 a ACS-10 cumplidos y auditoría del equipo con resultado PASS.
2. Commits separados, como en las fases anteriores: A, validadores y adaptación DH-02; B, documentos, contrato, fixtures y manifest; C, gobierno de cierre.
3. Sin push ni merge sin autorización expresa; la publicación solo con la regresión local completa sin fallas (DH-08).
4. Sin tag ni release. F35-SBX-B no se inicia sin una autorización nueva.

## 3. Revocación de G0-SBX

Cualquiera de estos hechos deja G0-SBX como REVOCADA y F35-SBX como BLOQUEADA. La revocación se registra en un documento nuevo; la decisión de F34E no se reescribe.

| ID | Hecho | Criterio SBX afectado |
|---|---|---|
| REV-01 | PII real en cualquier artefacto | SBX-02 |
| REV-02 | Un CV o documento real en cualquier artefacto | SBX-03 |
| REV-03 | Audio o vídeo real en cualquier artefacto | SBX-04 |
| REV-04 | Scoring en cualquier artefacto | SBX-05 |
| REV-05 | Recomendación o «mejor candidato» en cualquier artefacto | SBX-06 |
| REV-06 | Selección automática en cualquier artefacto | SBX-07 |
| REV-07 | RF-23 o RF-21 alterados | SBX-08 y SBX-09 |
| REV-08 | Aislamiento roto entre tenants | SBX-10 |
| REV-09 | Provenance no demostrable | SBX-11 |
| REV-10 | Conexión con la base del proyecto o archivos del runtime tocados | SBX-15 y SBX-16 |
| REV-11 | Alcance C en cualquier artefacto | SBX-17 |
| REV-12 | Afirmación falsa sobre el estado de la G0 real | SBX-18 |
| REV-13 | `validate_f34e.py` con fallas | Puerta G0-SBX |
| REV-14 | Decisión del equipo | Puerta G0-SBX |

## 4. Preparación de F35-SBX-B

F35-SBX-B, que requiere su propia autorización, implementaría un pipeline ejecutable con solo la biblioteca estándar en `tools/f35sbx/`. Recorrería los doce pasos sobre estos fixtures, con SQLite en memoria y triggers de solo inserción, auditoría encadenada, purga verificada del almacenamiento temporal, doble ejecución para demostrar determinismo y un informe con hashes y conteos. Seguiría sin runtime, sin `tests/` y sin dependencias nuevas. Las alertas deterministas (CAP-34) y el acuerdo entre evaluadores (CAP-33) quedarían para una autorización aparte.
