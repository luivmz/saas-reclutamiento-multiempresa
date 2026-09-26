# Changelog

Cambios relevantes del proyecto académico «Plataforma SaaS multiempresa para el reclutamiento, evaluación y selección de personal — Caso Colegio Andino de Huancayo» (Universidad Continental, Pruebas y Calidad de Software, NRC 28607). Detalle por fase en [`docs/PROGRESS.md`](docs/PROGRESS.md) y [`docs/v1.1/`](docs/v1.1/).

Prototipo académico con **datos ficticios**; no es un sistema productivo. El sistema **nunca selecciona, descarta ni contrata automáticamente**: la decisión final es humana (RF-23).

## v1.1 — académica (Fases 13 a 25; cierre en la Fase 26)

Etiqueta propuesta: `v1.1.0-academic`, **pendiente de auditoría**; no creada. Línea base funcional sin cambios: **RF-01 a RF-27**. RF-28 (candidato, no implementado), RF-29 (experimental) y RNF-C (propuesta) **no** se promovieron (decisión 11 de `scope-preliminary.md`).

### Added

- **Servicio experimental de riesgo operacional (RF-29)** — Fases 14 y 15.
  - Estima el riesgo de demora del **proceso** de una vacante a partir de 15 conteos y días operacionales.
  - No evalúa, puntúa, ordena, selecciona ni descarta personas.
  - Se entrenó con un dataset **sintético**: regresión logística `C=10`, `class_weight=None`, `StandardScaler` y sin calibración.
  - Contrato congelado: *freeze* `9ee1843055e75d4039dd84fd666db7a594e1a45ec7e9b354820fabfcb21ebcd2` y *threshold* `0.1679418172266036`.
  - Veredicto: `PREDICTIVE GO WITH LIMITATIONS`.
  - Se sirve con FastAPI (`/health`, `/v1/model-info`, `/v1/predict`) fuera de Docker Compose.
- **Integración Laravel ↔ FastAPI** — Fase 16.
  - Plazo objetivo `vacancies.target_completion_at`, que resuelve técnicamente GAP-01.
  - Cliente HTTP con token interno, validación estricta de la respuesta y *fallback* sin romper el flujo, con tres estados: `predictive_available`, `descriptive_only` y `unavailable`.
  - Tarjeta de riesgo «Experimental» en el detalle de la vacante.
- **Experiencia 3D con CSS 3D** en la portada pública — Fase 20.
  - Decorativa, sin WebGL ni dependencias nuevas.
  - Póster de respaldo con movimiento reducido, en móvil, en equipos modestos o sin WebGL.
- **Especificación UML AS-IS** (19 diagramas) — Fase 22. **Modelos nativos de PowerDesigner** (OOM y PDM) con 22 diagramas exportados en PNG y SVG — Fase 23.
- **Formato 09 v1.1** (DOCX y PDF) — Fase 24.
- **Pruebas nuevas:**
  - Vitest para componentes: 42 pruebas;
  - specs Cypress E2E-14 a E2E-19;
  - pruebas de integración ML y cross-tenant;
  - pytest del servicio: 533.
- **Gobierno de v1.1** — Fases 13 y 14.5: skills del proyecto, flujo multiagente (un solo *writer*), ADR-001 a ADR-004 y mapa de divergencias documentales.

### Changed

- **Rediseño integral del frontend** — Fase 18.
  - Sistema de diseño propio: IBM Plex, tokens de estado y barra lateral.
  - `DataTable` y `Section` reutilizables.
  - Tablas que pasan a fichas en móvil sin perder semántica.
  - Modo oscuro.
- **Animación y microinteracciones** — Fase 19: tres curvas y una escala de duración, respuesta a la pulsación y respeto del movimiento reducido. Sin biblioteca nueva.
- **Documentación de estado:** `CLAUDE.md`, `PROGRESS.md`, `scope-preliminary.md` y README reflejan v1.1, conservando la historia de v1.0.

### Fixed

- **Fase 21** (QA visual y de accesibilidad):
  - alertas destructivas ilegibles en claro (alta);
  - contraste del rojo en oscuro;
  - pantallas de acceso sin `main`;
  - cabecera pública desbordada a 320 px;
  - códigos de recuperación de 2FA;
  - enlace de salto;
  - desplazamiento que ignoraba el movimiento reducido.
- **Fase 25** (QA global):
  - **F25-M01:** un identificador no numérico en rutas de modelo (`/requerimientos/create`) respondía 500 (PostgreSQL 22P02); ahora responde 404.
  - **F25-M02:** a 375 px, las fichas de tabla de auditoría y de «Mis evaluaciones» se recortaban (WCAG 1.4.10).
  - **F25-L01:** textos que aún decían que GAP-01 seguía abierto (OpenAPI, CLI y README del servicio ML).
  - **F25-L02:** la guía de Cypress seguía en los números de v1.0.
- **Fase 17:** notas de GAP-01 obsoletas en `/v1/model-info`.

### Validated

QA global de la Fase 25. Ejecuciones reales:

| Suite | Resultado |
|---|---|
| PHPUnit | 411 superadas, 8 omitidas (verificación de correo de Fortify, desactivada por diseño), 0 fallidas, 1498 aserciones |
| pytest (servicio ML) | 533 superadas, 0 fallidas |
| Componentes (Vitest) | 42/42 |
| TypeScript | 0 errores |
| *Build* | Correcto (2375 módulos) |
| Cypress | 20 specs, 85/85 |

- **Multitenencia:** sin fuga entre organizaciones.
- **RF-23:** decisión humana con confirmación y justificación.
- **RF-29:** limitado al proceso; `risk_score` no se persiste.
- **Contrato ML:** idéntico al congelado.
- **Integración Laravel ↔ FastAPI:** verificada en vivo en sus tres estados.
- **Secretos:** ninguno versionado.

### Documentation

- Documentos de fase de v1.1 (`docs/v1.1/phase-*.md`), matriz de QA de la Fase 25, notas de versión, manifiesto y lista de aceptación final (Fase 26).
- UML (`docs/v1.1/uml/`), PowerDesigner (`docs/v1.1/powerdesigner/`) y Formato 09 (`docs/academico/phase-24/`).
- Los documentos de v1.0 **no se reescribieron**: las diferencias están en `docs/v1.1/documentation-update-map.md`.

### Known limitations

- **RF-29** es experimental: se validó técnicamente con datos sintéticos, pero **no** institucionalmente, y **no** está autorizado para producción. La tasa de alerta es alta.
- **RF-28** es un candidato no implementado. **RNF-C** es una propuesta.
- **Lector de pantalla real:** no se probó (NVDA no está instalado). Queda como prueba manual.
- **Rendimiento en un equipo modesto:** no se midió. La evidencia de la Fase 25 es exploratoria y viene de un equipo potente.
- **Formato:**
  - `pint --test` marca 8 archivos PHP, con unas 24 líneas de diferencia;
  - `vp check` marca 154 archivos, casi todos Markdown, incluida la historia de v1.0 y skills externas.
  - Aplazado; el CI no lo verifica.
- **Build:** muestra un aviso informativo del plugin `laravel:fonts`, porque falta el paquete opcional `fontaine`. No se instala.
- **Observaciones heredadas de las Fases 23 y 24:**
  - metadatos con rutas locales en los modelos nativos;
  - detalles visuales de SEQ-02 y AC-01;
  - `evaluation_criteria.position` fuera de CL-01;
  - catálogo de 10 RNF académicos frente a 11 técnicos;
  - seis rótulos de RF abreviados en el Formato 09;
  - sin validación contra XSD;
  - anexos densos.

  Clasificación completa: [`docs/v1.1/phase-26-release-closeout.md`](docs/v1.1/phase-26-release-closeout.md).

## v1.0 — académica (Fases 0 a 12)

Etiqueta `v1.0.0-academic` (`9a946c2`), rama `main` (`4563c69`).

- **Requerimientos:** RF-01 a RF-27 implementados, que cubren requerimientos, vacantes, postulantes, postulaciones, evaluaciones y entrevistas, ranking, decisión humana, selección, cierre, notificaciones y auditoría.
- **Arquitectura:** monolito modular Laravel + React/Inertia, multiempresa con `organization_id`, *scopes* y Policies, auditoría de solo inserción y entorno Docker.
- **Resultados:** 244 pruebas PHPUnit (236 superadas, 8 omitidas) y 14 specs Cypress (43/43). Veredicto de la Fase 12: **APTO PARA PUBLICACIÓN**.
- **Historia completa:** `docs/final-report/`.
