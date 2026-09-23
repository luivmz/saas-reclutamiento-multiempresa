---
name: recruitment-3d-experience
description: Marco para la experiencia 3D o visual avanzada en las pantallas públicas del portal de reclutamiento (implementada en la Fase 20, solo en la portada, con CSS 3D y sin dependencias). Úsala al discutir Three.js, React Three Fiber, modelos GLB, canvas o animación de alto costo. Define dónde está permitido, los presupuestos de rendimiento y las pantallas donde el 3D está prohibido.
---

# Experiencia 3D progresiva

**Estado: implementada y acotada.** La Fase 20 la incorporó por encargo del equipo, bajo [ADR-003](../../../docs/v1.1/architecture-decisions/ADR-003-progressive-3d.md), en **una sola superficie**: la tarjeta del expediente de la portada pública, con **CSS 3D** (perspectiva y capas de DOM) y **sin dependencias nuevas**. El código vive en `resources/js/components/experience-3d/` y su detalle, con las mediciones, en [`docs/v1.1/phase-20-3d-experience.md`](../../../docs/v1.1/phase-20-3d-experience.md).

Esta skill sigue existiendo para que el 3D sume sin poner en riesgo lo que ya está evaluado y funcionando. **Implementada no significa ampliable**: cualquier otra superficie, cualquier escena WebGL o cualquier dependencia nueva vuelve a pasar por las condiciones del final.

> Historia: hasta la Fase 20 esta skill decía «Estado: candidato. No instales dependencias ni escribas componentes 3D todavía.» Se actualizó en la Fase 21 (23/09/2026) para reflejar lo implementado; las reglas de uso no cambiaron.

## Dónde sí y dónde no

**Permitido**, solo como capa decorativa: portada pública, presentación del portal de empleo y, como mucho, el encabezado del listado público de vacantes.

**Prohibido**, sin excepción:

- ranking y comparación de candidatos (RF-20 a RF-22);
- evaluaciones, entrevistas y registro de resultados;
- decisión final y cierre de vacante (RF-23 a RF-25);
- consulta de auditoría (RF-27);
- cualquier pantalla administrativa o de gestión interna;
- formularios de postulación y de datos del candidato.

La razón es simple: esas pantallas sostienen decisiones sobre personas y evidencia académica. Deben ser rápidas, legibles, accesibles y auditables, no impresionantes.

## Progresivo de verdad

El 3D es un adorno que puede no cargar. La pantalla debe funcionar completa sin él:

1. **El DOM funcional es independiente del canvas.** Títulos, textos, enlaces, botones y formularios existen y operan aunque el canvas nunca se monte. El contenido no se renderiza *dentro* del canvas.
2. **Carga diferida**: `React.lazy` + `Suspense`, fuera del *bundle* principal, y solo cuando el contenedor entra en viewport.
3. **Poster estático** (imagen optimizada) visible mientras carga y como sustituto permanente cuando el 3D no procede.
4. **ErrorBoundary** alrededor del canvas: si falla, cae al poster sin romper la página ni ensuciar la consola del usuario.
5. **Sin bloquear la interacción**: nunca capture el scroll ni el foco del teclado.

## Cuándo no se muestra el 3D

Se cae al poster automáticamente si: el navegador no soporta WebGL, el dispositivo es móvil o de gama baja, la conexión es limitada (`navigator.connection` ahorro de datos), o el usuario declaró `prefers-reduced-motion: reduce`. Esta última no es opcional: es un requisito de accesibilidad, y la skill `reviewing-a11y` lo verifica.

## Presupuestos

Los valores y el procedimiento de medición están en [BUDGETS.md](BUDGETS.md). Límites de referencia: modelo GLB comprimido ≤ 1.5 MB, ≤ 100k triángulos en escena, texturas ≤ 1024 px, ≤ 60 llamadas de dibujo, y ningún aumento del *bundle* inicial. Si una propuesta no entra en el presupuesto, se reduce la propuesta, no el presupuesto.

## Lo implementado, y cómo mantenerlo

- Una escena, en la portada, detrás del expediente: decorativa (`aria-hidden`, `inert`), sin información propia y con el texto por delante sobre fondo sólido.
- Póster estático visible desde el primer cuadro, que queda con movimiento reducido, en pantallas de menos de 1024 px, con ahorro de datos, en equipos modestos o si el fragmento falla.
- Fragmento diferido propio, cargado solo al entrar en el viewport. *Bundle* inicial JS: +0 KB.
- Sin bucle de render: movimiento por evento, con las curvas de la Fase 19.
- Protegido por `cypress/e2e/e2e-18-profundidad-portada.cy.js` y por las pruebas de componente de `experience-3d/`: si alguna falla, la escena se arregla o se retira, no se relajan las pruebas.

## Antes de ampliarlo

Ampliar el 3D —otra superficie, una escena WebGL, un modelo GLB o una dependencia nueva— requiere, en este orden: aprobación explícita del equipo para esa ampliación, autorización para añadir dependencias de frontend si las hubiera (la pregunta 3 de `scope-preliminary.md` sigue abierta para WebGL), y una medición previa del rendimiento actual como línea base. La promoción formal de RNF-C al baseline de v1.1 es una decisión del equipo, igual que la de RF-28 y RF-29. Las pruebas E2E existentes deben seguir pasando sin modificar sus `data-cy`.
