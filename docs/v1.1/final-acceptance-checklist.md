# Lista de aceptación final — v1.1 académica

Estado al terminar la implementación de la Fase 26 (25/09/2026), en `feature/phase-26-release-closeout`. `[x]` = verificado, con su evidencia. `[ ]` = pendiente de auditoría o de decisión del equipo.

| | Criterio | Evidencia |
|---|---|---|
| [x] | Git limpio | `git status` sin cambios tras los commits de la F26; `git diff --check` limpio |
| [x] | `develop` sincronizado | `develop` = `origin/develop` = `2b97fe3` tras `git fetch`; la F26 no lo movió |
| [x] | `main` protegido | `main` = `origin/main` = `4563c69`, sin cambios; no hubo *merge* ni *push* |
| [x] | Etiqueta de la v1.0 intacta | `v1.0.0-academic^{}` = `9a946c2`; no se creó ni movió ninguna etiqueta |
| [x] | QA de la F25 en verde | [`phase-25-final-qa.md`](phase-25-final-qa.md), cerrada e integrada (`2b97fe3`) |
| [x] | Laravel en verde | PHPUnit 411 superadas · 8 omitidas · 0 fallidas · 1498 aserciones (F25) |
| [x] | Python en verde | pytest 533 superadas (F25) |
| [x] | Frontend en verde | Vitest 42/42 · `tsc` 0 errores · *build* correcto (F25; aviso informativo de `fontaine`, deuda A-01) |
| [x] | Cypress en verde | 20 specs · 85/85 (F25) |
| [x] | Multitenencia aprobada | Sin fugas; pruebas cross-tenant y E2E-11 (F25 §14) |
| [x] | RF-23 humana | Confirmación y justificación del Aprobador; el ranking nunca selecciona (F25 §15) |
| [x] | RF-29 limitado | Experimental, solo proceso, sin persistencia ni efecto en ranking o decisión (F25 §9–10) |
| [x] | Formato 09 final | DOCX y PDF presentes con hashes en el [manifiesto](release-manifest-v1.1.md); validador sin fallos (F25) |
| [x] | UML final | 19 `.puml` y la especificación en [`uml/`](uml/) |
| [x] | PowerDesigner final | OOM y PDM presentes con hashes; 22 PNG y 22 SVG |
| [x] | Notas de versión | [`release-notes-v1.1.md`](release-notes-v1.1.md) |
| [x] | Changelog | [`../../CHANGELOG.md`](../../CHANGELOG.md) |
| [x] | Manifiesto | [`release-manifest-v1.1.md`](release-manifest-v1.1.md) |
| [x] | Deuda residual documentada | [`phase-26-release-closeout.md`](phase-26-release-closeout.md) §12–13: 0 BLOCKER, 0 HIGH, 0 MEDIUM, 8 LOW y 9 INFO clasificados |
| [x] | Sin secretos | Barrido de la F26: sin claves, tokens ni `.env` versionados |
| [ ] | Estrategia de etiqueta aprobada | Propuesta: `v1.1.0-academic`, anotada (§15). **Pendiente de aprobación** |
| [ ] | Estrategia de `main` aprobada | Recomendación: opción B, merge `develop → main` con `--no-ff` y la etiqueta sobre `main` (§15). **Pendiente de aprobación** |
| [ ] | F26 auditada | **Pendiente de la auditoría de Codex** |
