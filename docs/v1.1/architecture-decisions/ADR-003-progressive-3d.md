# ADR-003 — Experiencia 3D progresiva y acotada

- **Estado:** ~~propuesta (pendiente de decisión del equipo)~~ → implementada en la Fase 20 por encargo explícito del equipo (ver nota de evolución) → ampliada a una escena WebGL en «Cómo postular» el 24/11/2026, con presupuestos incumplidos (ver la segunda nota)
- **Fecha:** 19 de septiembre de 2026
- **Contexto:** Fase 13, planificación de v1.1

> **Nota de evolución — Fase 20, 23/09/2026.** El equipo encargó la Fase 20 con instrucciones explícitas de implementar una experiencia 3D. Se implementó **bajo las siete condiciones de esta ADR**, solo en la portada pública y **sin dependencias nuevas**: la escena es CSS 3D (perspectiva y capas de DOM), no WebGL. Por eso la autorización de dependencias de frontend que esta ADR exige **no llegó a ser necesaria** y sigue pendiente para cualquier 3D futuro con WebGL. La promoción formal de RNF-C al baseline de v1.1 sigue siendo decisión del equipo. Detalle y mediciones: [`phase-20-3d-experience.md`](../phase-20-3d-experience.md). El cuerpo de la ADR se conserva tal como se aprobó para discusión.

> **Nota de evolución — ampliación WebGL, 24/11/2026.** El equipo eligió la «opción A»: aceptó los términos de Spline para el prototipo académico y autorizó `@splinetool/runtime` con versión exacta. La sección «Cómo postular» de la portada muestra ahora un carrusel exportado de Spline con WebGL. Es la segunda superficie 3D y la primera con una dependencia de frontend. Registro completo: [`proceso-postulacion-spline.md`](../proceso-postulacion-spline.md).
>
> **Estado de las siete condiciones:**
>
> 1. **DOM funcional independiente del canvas:** se cumple. Pasos, explicaciones y enlaces son HTML, y el canvas es `aria-hidden` sin foco.
> 2. **Carga diferida:** se cumple. El runtime llega con `import()` en un fragmento diferido, solo cerca de la sección.
> 3. **Póster estático:** se cumple. El respaldo queda sincronizado con el paso.
> 4. **Contención del fallo:** se cumple. Con el export o el runtime bloqueados, la pérdida de contexto o la espera de 8 s, queda el respaldo sin saltos.
> 5. **Respaldo automático:** se cumple. Lo hay con menos de 1024 px, puntero táctil, movimiento reducido (también al activarlo con la página abierta), ahorro de datos y equipo modesto. Sin WebGL también, porque la carga falla y cae al respaldo.
> 6. **Presupuestos medidos:** se midieron, con incumplimientos (abajo).
> 7. **E2E:** sin cambios en los `data-cy`. E2E-29 se amplió y pasan E2E-23, E2E-27 y E2E-29.
>
> **Limitaciones reales, no aprobadas como cumplidas:**
>
> - **Llamadas de dibujo:** 99 por cuadro en reposo y 132–144 en las transiciones, frente al techo de 60. **No cumple.** Las causan las 52 mallas de la escena; sin sombras y con profundidad 0 siguen en 99. Bajarlas exige rediseñar la escena.
> - **Renderizado continuo mientras está visible:** con `renderMode: 'auto'`, el runtime dibuja unos 60 cuadros por segundo aunque no haya cambios. Fuera de la vista y con la pestaña oculta la pausa es completa (0 cuadros). El modo `manual` daría 0 cuadros en reposo, pero dejaría transiciones a medias y textos sin redibujar.
> - **Fuente externa:** el export pide Inter 600 a `fonts.gstatic.com` (162 619 B), porque su URL viene dentro del archivo. Es la única petición fuera del dominio. Evitarla exigiría alterar el export.
> - **Sin mediciones en GPU de gama media:** los 60 FPS y el primer cuadro de 0,8 s se midieron en una NVIDIA RTX 4060. Tampoco hay medición de memoria de GPU.
> - ***Bundle* inicial:** la entrada `app` crece 0,16 kB de metadatos de precarga, frente al techo de 0 KB. Ni el runtime ni el adaptador están en ella.
>
> **Licencia y alcance.** El runtime no declara licencia, su repositorio no es público y los términos de Spline lo declaran propietario. Origen, integrity y revisión están en el registro. La aceptación del equipo se formuló para el prototipo académico **local**; publicar en el VPS amplía ese uso y debe confirmarse con esos términos. La atribución de la plantilla «Carousel Tutorial for Community» sigue sin verificar. La pregunta 3 de `scope-preliminary.md` y la promoción de RNF-C siguen siendo decisiones del equipo.

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
