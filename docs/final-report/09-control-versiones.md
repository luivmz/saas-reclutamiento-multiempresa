# Capítulo 9. Control de versiones

## 9.1 Herramienta y estado del repositorio

- **Git**, repositorio local.
- **Sin repositorio remoto y sin `push` a la fecha de este documento.** La publicación en GitHub se hará después de la Fase 12 y de la revisión final del equipo.
- Los datos de este capítulo se obtuvieron con `git branch` y `git log --oneline --graph --decorate --all`.

## 9.2 Estrategia de ramas

Git Flow simplificado:

| Rama | Uso |
|---|---|
| `main` | Rama estable. Contiene el bootstrap inicial (`e87ef39`) y recibirá `develop` al cierre del proyecto (Fase 12). |
| `develop` | Integración: cada fase se fusiona aquí con `git merge --no-ff`, lo que conserva un commit de merge por fase. |
| `feature/*` | Una rama por fase funcional o técnica, creada desde `develop` y fusionada tras la revisión del equipo. |

Reglas aplicadas:
- sin `push`;
- sin fusionar una fase antes de su revisión;
- commits pequeños;
- mensajes con prefijos de tipo (`feat:`, `test:`, `chore:`, `docs:`);
- `.env`, `.env.e2e`, `vendor/`, `node_modules/`, `public/build` y resultados temporales excluidos por `.gitignore`.

Ramas existentes: `main`, `develop`, `feature/tenancy-roles`, `feature/job-requests-vacancies`, `feature/candidates-applications`, `feature/evaluations-interviews`, `feature/ranking-selection-closure`, `feature/notifications-audit`, `feature/frontend-integral`, `feature/cypress-e2e`, `feature/docker-portability` y `feature/final-documentation` (Fase 11, en curso).

## 9.3 Fases, ramas y commits

| Fase | Rama | Commit / merge | Propósito |
|---|---|---|---|
| 1 | `main` | `e87ef39` | `chore: bootstrap Laravel application` |
| 2 | `feature/tenancy-roles` | `3c28f28` → merge `d696032` | Organizaciones, roles y aislamiento multiempresa |
| 3 | `feature/job-requests-vacancies` | `7ccb619` → merge `5ab6e22` | RF-01 a RF-07 |
| 4 | `feature/candidates-applications` | `215cdbe` → merge `f20f0b6` | RF-08 a RF-15 |
| 5 | `feature/evaluations-interviews` | `3e66623` (checkpoint RED), `06cf5c4` → merge `40eda7d` | RF-16 a RF-19 |
| 6 | `feature/ranking-selection-closure` | `7a65bee` → merge `dda4bd0` | RF-20 a RF-25 |
| 7 | `feature/notifications-audit` | `9de66ce` → merge `cd092d1` | RF-26 y RF-27 |
| 8 | `feature/frontend-integral` | `ed11ecc` → merge `6d47e46` | Frontend integral y validación en navegador |
| 9 | `feature/cypress-e2e` | `9edb0cd` (checkpoint), `a77c916` → merge `e0c8825` | Suite E2E Cypress |
| 10 | `feature/docker-portability` | `ccf05d1`, `ff524e6` → merge `02c2505` | Docker, entorno E2E aislado y documentación Docker |
| 11 | `feature/final-documentation` | Commit de esta fase (sin fusionar) | Documentación final |

## 9.4 Grafo de historia

```text
*   02c2505 (develop) Merge branch 'feature/docker-portability' into develop
|\
| * ff524e6 docs: document Docker setup, portability validation and E2E isolation (Phase 10)
| * ccf05d1 chore(docker): pin images, isolate the E2E environment and fix E2E dates
|/
*   e0c8825 Merge branch 'feature/cypress-e2e' into develop
|\
| * a77c916 test: complete Cypress E2E suite with two stable full runs (Phase 9)
| * 9edb0cd test: add Cypress E2E suite scaffolding (Phase 9 partial checkpoint)
|/
*   6d47e46 Merge branch 'feature/frontend-integral' into develop
|\
| * ed11ecc feat: integrate and validate the frontend end to end
|/
*   cd092d1 Merge branch 'feature/notifications-audit' into develop
|\
| * 9de66ce feat: notify final results on closure and complete the audit trail
|/
*   dda4bd0 Merge branch 'feature/ranking-selection-closure' into develop
|\
| * 7a65bee feat: add candidate ranking, human final decision, selection and closure
|/
*   40eda7d Merge branch 'feature/evaluations-interviews' into develop
|\
| * 06cf5c4 feat: implement evaluations and interviews
| * 3e66623 test: add RED tests for evaluations and interviews (checkpoint)
|/
*   f20f0b6 Merge branch 'feature/candidates-applications' into develop
|\
| * 215cdbe feat: implement candidate profiles and applications
|/
*   5ab6e22 Merge branch 'feature/job-requests-vacancies' into develop
|\
| * 7ccb619 feat: implement personnel request workflow and vacancies
|/
*   d696032 Merge branch 'feature/tenancy-roles' into develop
|\
| * 3c28f28 feat: add organizations and tenant isolation
|/
* e87ef39 (main) chore: bootstrap Laravel application
```

## 9.5 Ejemplos de commits

| Tipo | Commit | Mensaje |
|---|---|---|
| Funcionalidad | `7a65bee` | `feat: add candidate ranking, human final decision, selection and closure` |
| Checkpoint TDD (RED) | `3e66623` | `test: add RED tests for evaluations and interviews (checkpoint)` |
| Pruebas | `a77c916` | `test: complete Cypress E2E suite with two stable full runs (Phase 9)` |
| Infraestructura | `ccf05d1` | `chore(docker): pin images, isolate the E2E environment and fix E2E dates` |
| Documentación | `ff524e6` | `docs: document Docker setup, portability validation and E2E isolation (Phase 10)` |

## 9.6 Merges relevantes

- **`dda4bd0`:** incorpora la regla crítica de decisión humana (RF-23) y la cadena selección → cierre.
- **`cd092d1`:** completa la línea base RF-01 a RF-27.
- **`e0c8825`:** integra la automatización E2E.
- **`02c2505`:** integra la portabilidad Docker y el aislamiento del entorno E2E; es el último merge en `develop` antes de la documentación final.

Pendiente para la Fase 12: fusionar `develop` en `main`, crear la etiqueta de versión y publicar en el repositorio remoto, previa revisión del equipo.
