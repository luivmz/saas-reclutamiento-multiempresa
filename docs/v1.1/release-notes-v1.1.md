# v1.1 académica — Plataforma SaaS multiempresa de reclutamiento

**Etiqueta propuesta:** `v1.1.0-academic` · **Estado:** preparada en la Fase 26, pendiente de auditoría. La etiqueta se crea sobre el merge de `develop` en `main` **después** de que el CI de `main` esté en verde y de verificar `develop^{tree} == main^{tree}`.

Universidad Continental · Pruebas y Calidad de Software (NRC 28607) · Caso de estudio: Colegio Andino de Huancayo.

> ⚠️ **Prototipo académico, no productivo.** Todos los datos son ficticios. La decisión final de selección es **siempre humana**: el Aprobador / Dirección la registra con confirmación explícita y justificación (RF-23). El sistema **nunca** selecciona, descarta ni contrata automáticamente.

> ⚠️ **RF-29 no evalúa personas.** El riesgo operacional es **experimental**:
> - estima si el **proceso** de una vacante podría demorarse;
> - no puntúa, ordena, clasifica, selecciona ni descarta candidatos;
> - no toca el ranking ni la decisión, y su resultado no se guarda.
>
> Se validó técnicamente con datos sintéticos, **no** institucionalmente, y **no** está autorizado para producción.

## Resumen

La v1.1 conserva intacta la línea base de la v1.0 (RF-01 a RF-27) y agrega:

- un servicio experimental de riesgo operacional del proceso;
- su integración con Laravel;
- un rediseño completo de la interfaz, con movimiento accesible y una experiencia 3D decorativa en la portada;
- QA visual y de accesibilidad;
- la formalización UML en PowerDesigner y el Formato 09 actualizado;
- un QA global final.

## Principales mejoras

- **Riesgo operacional experimental (RF-29).**
  - Servicio FastAPI con modelo congelado: regresión logística con *freeze* y *threshold* fijos.
  - Integración Laravel ↔ FastAPI con token interno, validación del contrato y *fallback*.
  - Plazo objetivo del proceso (`target_completion_at`, GAP-01 resuelto técnicamente).
  - Tarjeta «Experimental» en el detalle de la vacante.
- **Interfaz rediseñada:**
  - sistema de diseño propio y modo oscuro;
  - tablas que se vuelven fichas en móvil sin perder semántica;
  - microinteracciones que respetan el movimiento reducido;
  - portada con profundidad en CSS 3D y póster de respaldo.
- **Accesibilidad:** contraste AA en claro y oscuro, `main` en todas las pantallas, enlace de salto, foco visible, *reflow* a 320 px y tablas legibles a 375 px.
- **Robustez** (Fase 25): un identificador de ruta mal formado responde 404 en lugar de 500.

## Arquitectura

- Monolito modular Laravel 13 (PHP 8.4) con React 19, TypeScript, Inertia 3 y Tailwind 4, sobre PostgreSQL 17 y Redis 7, en Docker Compose.
- Multiempresa lógica: `organization_id`, *scopes* globales y Policies que comparan rol **y** organización. Sin RLS.
- Servicio ML **externo y experimental** (`ml-service/`, Python, scikit-learn, FastAPI), fuera de Compose. Solo se consulta si `ML_SERVICE_ENABLED=true`; sin él, la aplicación funciona igual. **No es una arquitectura de microservicios.**

## Seguridad

Verificado en la Fase 25:

- sin fugas entre organizaciones (22 pruebas cross-tenant explícitas, más *scope*, ML y E2E);
- el CV solo se descarga con Policy de rol y organización;
- auditoría de solo inserción protegida por un *trigger* en la base;
- sin secretos versionados.

## Calidad y pruebas

Resultados reales del QA global, Fase 25:

| Suite | Resultado |
|---|---|
| PHPUnit | **411 superadas**, 8 omitidas (verificación de correo desactivada por diseño), 0 fallidas, 1498 aserciones |
| pytest (servicio ML) | **533 superadas** |
| Componentes (Vitest) | **42/42** |
| TypeScript | 0 errores |
| *Build* | correcto |
| Cypress E2E | **20 specs, 85/85** |

## Modelado y documentación académica

- **UML AS-IS** (Fase 22): 19 diagramas especificados a partir del código.
- **PowerDesigner** (Fase 23): OOM y PDM nativos, 22 diagramas exportados en PNG y SVG.
- **Formato 09 v1.1** (Fase 24): DOCX y PDF de 28 páginas. RF-01 a RF-27 son la línea base; RF-28, RF-29 y RNF-C figuran como candidatos, sin promoción.

## Limitaciones conocidas

- **RF-29:** experimental, con tasa de alerta alta y sin validación institucional. **RF-28:** no implementado. **RNF-C:** propuesta.
- **Pruebas manuales pendientes:** lector de pantalla real y rendimiento en un equipo modesto.
- **Formato del código:** deuda de Pint y `vp check` aplazada.
- **Build:** muestra un aviso informativo porque falta el paquete opcional `fontaine`.
- **Observaciones heredadas de F23 y F24:** detalles visuales de dos diagramas, metadatos locales en los modelos nativos, divergencia entre los catálogos académico y técnico de RNF y rótulos abreviados en el Formato 09.

Lista completa y clasificación: [`phase-26-release-closeout.md`](phase-26-release-closeout.md).

## Documentación

- Cambios: [`CHANGELOG.md`](../../CHANGELOG.md)
- Cierre y deuda: [`phase-26-release-closeout.md`](phase-26-release-closeout.md) · Manifiesto: [`release-manifest-v1.1.md`](release-manifest-v1.1.md) · Aceptación: [`final-acceptance-checklist.md`](final-acceptance-checklist.md)
- QA global: [`phase-25-final-qa.md`](phase-25-final-qa.md) · [`phase-25-qa-matrix.md`](phase-25-qa-matrix.md)
- Estado por fase: [`../PROGRESS.md`](../PROGRESS.md) · Divergencias con v1.0: [`documentation-update-map.md`](documentation-update-map.md)
- Puesta en marcha: [`../docker.md`](../docker.md) · Usuarios demo ficticios: [`../demo-users.md`](../demo-users.md)
