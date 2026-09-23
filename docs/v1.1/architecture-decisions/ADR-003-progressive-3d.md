# ADR-003 — Experiencia 3D progresiva y acotada

- **Estado:** ~~propuesta (pendiente de decisión del equipo)~~ → implementada en la Fase 20 por encargo explícito del equipo (ver nota de evolución)
- **Fecha:** 19 de septiembre de 2026
- **Contexto:** Fase 13, planificación de v1.1

> **Nota de evolución — Fase 20, 23/09/2026.** El equipo encargó la Fase 20 con instrucciones explícitas de implementar una experiencia 3D. Se implementó **bajo las siete condiciones de esta ADR**, solo en la portada pública y **sin dependencias nuevas**: la escena es CSS 3D (perspectiva y capas de DOM), no WebGL. Por eso la autorización de dependencias de frontend que esta ADR exige **no llegó a ser necesaria** y sigue pendiente para cualquier 3D futuro con WebGL. La promoción formal de RNF-C al baseline de v1.1 sigue siendo decisión del equipo. Detalle y mediciones: [`phase-20-3d-experience.md`](../phase-20-3d-experience.md). El cuerpo de la ADR se conserva tal como se aprobó para discusión.

## Contexto

Se propone incorporar 3D en el portal para mejorar su presentación. El sistema ya está publicado, evaluado y cubierto por 43 pruebas E2E; sus pantallas internas sostienen decisiones sobre personas y evidencia académica. Un canvas 3D añade peso de descarga, consumo de GPU, riesgos de accesibilidad y una superficie nueva de fallo.

## Decisión

Si el equipo lo aprueba, el 3D entra **solo** en las pantallas públicas (portada, presentación del portal de empleo, encabezado del listado público), como capa **decorativa y opcional**.

Condiciones inseparables de la aprobación:

1. **El DOM funcional es independiente del canvas.** Textos, enlaces, botones y formularios existen y operan aunque el canvas nunca se monte.
2. **Carga diferida** fuera del *bundle* principal, activada al entrar en viewport.
3. **Poster estático** durante la carga y como sustituto permanente cuando el 3D no procede.
4. **ErrorBoundary**: si el canvas falla, la página sigue completa.
5. **Fallback automático** sin WebGL, en móvil o gama baja, con ahorro de datos, o con `prefers-reduced-motion: reduce`.
6. **Presupuestos medidos** (`.claude/skills/recruitment-3d-experience/BUDGETS.md`), con línea base tomada **antes** de implementar.
7. **Cero impacto en E2E**: los `data-cy` y los flujos existentes no cambian.

**Prohibido:** 3D en ranking, comparación, evaluaciones, entrevistas, decisión final, cierre de vacante, auditoría, pantallas administrativas y formularios de datos del candidato.

## Alternativas consideradas

1. **3D en toda la aplicación.** Rechazada: degrada pantallas críticas, complica la accesibilidad y pone en riesgo la suite E2E.
2. **Sin 3D, mejorando tipografía, espaciado y jerarquía visual.** Sigue siendo la opción por defecto y la de mejor relación beneficio/riesgo; el 3D solo se justifica si aporta algo que el diseño plano no logra.
3. **Video en lugar de 3D.** Menor riesgo técnico, pero también menor valor demostrativo; queda como alternativa si los presupuestos no se cumplen.

## Consecuencias

**Positivas:** el portal público gana presencia sin que el sistema evaluado pierda rendimiento, accesibilidad ni cobertura de pruebas; el fallo del 3D nunca es un fallo del producto.

**Negativas:** más complejidad en el frontend, dependencias nuevas que requieren autorización explícita, y trabajo de medición que compite con los entregables académicos. Si esa competencia aprieta, el 3D se descarta primero.

**Aplicación:** la skill `recruitment-3d-experience`. Candidato RNF-C en `../scope-preliminary.md`.
