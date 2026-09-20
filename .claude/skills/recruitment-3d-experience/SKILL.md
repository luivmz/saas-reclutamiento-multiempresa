---
name: recruitment-3d-experience
description: Marco para incorporar experiencia 3D o visual avanzada en las pantallas públicas del portal de reclutamiento (candidato v1.1, aún NO implementado). Úsala al discutir Three.js, React Three Fiber, modelos GLB, canvas o animación de alto costo. Define dónde está permitido, los presupuestos de rendimiento y las pantallas donde el 3D está prohibido.
---

# Experiencia 3D progresiva (diseño, no implementación)

**Estado: candidato. No instales dependencias ni escribas componentes 3D todavía.** Esta skill existe para que, si el equipo lo aprueba, el 3D sume sin poner en riesgo lo que ya está evaluado y funcionando.

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

## Antes de que esto se implemente

Requiere, en este orden: aprobación explícita del equipo, un RNF candidato aprobado en `docs/v1.1/scope-preliminary.md`, autorización para añadir dependencias de frontend, y una medición previa del rendimiento actual como línea base. Las pruebas E2E existentes deben seguir pasando sin modificar sus `data-cy`.
