# Fase 20 — Experiencia 3D contextual y responsable

**Fecha:** 23 de septiembre de 2026
**Rama:** `feature/phase-20-3d-experience` · **Base:** `67a88a6` (cierre de la Fase 19)
**Writer principal:** Claude Code · **Reviewer:** Codex (auditoría posterior)

> Fase **exclusivamente de interfaz, y solo en la portada pública**. No cambia reglas de negocio, RF, rutas, contratos de API, modelos, Policies, el servicio ML ni ninguna decisión científica. RF-23 sigue siendo una decisión humana y RF-29 sigue siendo experimental. La Fase 18 es el diseño, la Fase 19 el movimiento y esta, la profundidad: cada una en su documento.

---

## 1. Objetivo

Añadir profundidad donde aporte algo que el diseño plano no logra, y en ningún otro sitio. El marco lo fija [ADR-003](architecture-decisions/ADR-003-progressive-3d.md): el 3D es una capa **decorativa y opcional**, solo en pantallas públicas, y su fallo nunca es un fallo del producto.

## 2. Baseline

| | |
|---|---|
| Rama base | `develop` = `origin/develop` = `67a88a6ebefb3679a735abb2de22926d259377d3`, árbol limpio |
| `app-*.js` (*bundle* inicial) | 204.27 kB, 59.93 kB gzip |
| `app-*.css` | 99.34 kB, 16.46 kB gzip |
| `welcome-*.js` (fragmento de la portada) | 6.41 kB, 2.41 kB gzip |
| Carga de la portada (mediana de 5, 1440 px) | DCL 126 ms, `load` 132 ms, 12 archivos JS, 586 KB decodificados |

La línea base se midió **antes de tocar nada**, como exige `BUDGETS.md`.

## 3. Skills aplicados

`project-guardian` (baseline, alcance, contratos), `recruitment-3d-experience` con `BUDGETS.md` (dónde, presupuestos, fallback, medición), `reviewing-a11y`, `frontend-design`, `animate` y `laravel-saas-quality` (regresión).

## 4. Dónde se usó 3D, y dónde no

**Una sola superficie: la tarjeta del expediente de la portada pública (`/`).**

| Superficie | Decisión | Motivo |
|---|---|---|
| Portada pública | **Sí** | Permitida por ADR-003; es donde se juega la identidad del producto y la primera comprensión del SaaS |
| Encabezado del listado público de empleos | No | Permitido «como mucho», pero una segunda escena no añadía nada que la portada no dijera ya. Si no aporta, se simplifica |
| Inicio de sesión y registro | No | Son formularios y no están en la lista de pantallas permitidas de ADR-003 |
| Panel interno | No | Pantalla administrativa: **prohibida** por ADR-003, aunque el encargo la proponía como ejemplo |
| Estados vacíos, vacantes, postulaciones, configuración | No | Pantallas internas: prohibidas |
| Tablas, ranking, comparación, selección, auditoría, riesgo operacional | No | Prohibidas sin excepción: sostienen decisiones sobre personas |

## 5. Propósito UX

La portada de la Fase 18 muestra **un** expediente. Lo que el producto sostiene es que **cada** requerimiento se convierte en un expediente que avanza por etapas y deja rastro. Detrás de la tarjeta, las hojas de otros expedientes se alejan en perspectiva, cada una con el borde del tono de su etapa —requerimiento, validación, aprobación, convocatoria—: el que se ve es uno entre muchos, guardado y trazable.

Es lo único que el plano sugería sin poder hacerlo espacial. **La ganancia es modesta**, y por eso tenía que costar casi nada (§15 y §16).

No representa personas, ni puntajes, ni rankings: son hojas sin contenido.

## 6. Tecnología

**CSS 3D: perspectiva y capas de DOM compuestas por la GPU. No WebGL.**

El propio encargo pide probar primero CSS 3D y subir a WebGL solo si aporta algo que CSS no puede. Para una escena sobria de cuatro hojas no aporta nada, y costaría:

| | WebGL (Three.js / R3F) | CSS 3D |
|---|---|---|
| Dependencia | ~190 KB gzip, sin autorizar | Ninguna |
| Bucle de render | Sí, hay que pausarlo | No existe |
| Contexto que se puede perder | Sí | No |
| Modo oscuro | Otro juego de colores en el shader | Los mismos tokens de la Fase 18 |
| Curvas de movimiento | Otra implementación | Las mismas de la Fase 19 |
| Fallo sin WebGL | Hay que cubrirlo | No aplica: no lo usa |

## 7. Dependencias

**Ninguna.** `package.json` no cambia.

Esto importa por gobierno, no solo por peso: la autorización de dependencias de frontend para el 3D es la pregunta abierta n.º 3 de `scope-preliminary.md` y ADR-003 exige autorización explícita. Esta fase no la necesitó, así que la pregunta sigue abierta para cualquier 3D futuro con WebGL.

## 8. Arquitectura

Aislada en `resources/js/components/experience-3d/`, sin marco propio:

| Archivo | Qué hace |
|---|---|
| `use-scene-capability.ts` | Único sitio donde se decide escena o póster, y por qué. Función pura y hook reactivo |
| `recruitment-scene-poster.tsx` | El póster plano: se ve al instante y es el sustituto permanente |
| `recruitment-scene.tsx` | La escena. Fragmento diferido propio |
| `recruitment-depth.tsx` | La capa: póster primero, compuerta de capacidad y de viewport, `ErrorBoundary`, `Suspense` |

En `welcome.tsx` solo cambia la envoltura de la tarjeta: la tarjeta pasa a `relative z-10` y la capa se coloca detrás. **El contenido y la semántica del expediente no se tocaron.**

## 9. Carga diferida

- La escena vive en su propio fragmento (`recruitment-scene-*.js`) cargado con `React.lazy`.
- Solo se pide si la capacidad lo permite **y** cuando la tarjeta entra en el viewport (`IntersectionObserver`, una sola vez).
- Móvil, movimiento reducido, ahorro de datos y equipos modestos **no descargan ni un byte** de la escena.

Comprobado en navegador con la API de Resource Timing —que registra también lo servido desde caché— en `e2e-18`.

## 10. Fallback

El póster es **la misma idea en plano**: la pila de hojas con sus bordes de etapa, sin perspectiva ni movimiento. Se ve siempre primero y queda cuando:

| Condición | Resultado | Cómo se prueba |
|---|---|---|
| Movimiento reducido | Póster | Emulación real de la preferencia (`e2e-18`) y función pura |
| Viewport < 1024 px | Póster | 390 px en navegador y función pura |
| Ahorro de datos (`saveData`) | Póster | Función pura |
| Equipo modesto (≤ 2 núcleos o ≤ 2 GB) | Póster | `hardwareConcurrency = 2` en navegador y función pura |
| Sin composición en perspectiva | Póster | Función pura |
| El fragmento no llega | Póster | Fragmento forzado a 500 en navegador |
| La escena lanza al montar | Póster | El mismo `ErrorBoundary` que ejercita el caso anterior —el rechazo de `React.lazy` se captura ahí—; un error de montaje no se provoca por separado |
| **Sin WebGL** | **Escena, igual** | WebGL eliminado en navegador: la escena no depende de él |

Nunca queda un hueco ni un cargador: el póster ocupa la caja desde el primer cuadro.

## 11. Movimiento reducido

Con `prefers-reduced-motion: reduce` **no se reduce la velocidad: se quita la escena**. Queda el póster, quieto, y el fragmento no se descarga. Si la persona cambia la preferencia con la página abierta, la capa se reevalúa. La política global de la Fase 19 queda además como segunda red.

### Movimiento de la escena

Usa las curvas de la Fase 19 (`var(--ease-out)`) y no introduce ninguna nueva:

- **Una sola entrada**: al montar, las hojas se abren en abanico desde detrás del expediente, 480 ms con 40 ms de escalonado. Supera los 300 ms que la Fase 19 fija para la interfaz, y la razón es que no es interfaz: es el único momento orquestado de una portada pública, que se ve una vez por visita. Son transiciones, no keyframes, así que se pueden interrumpir.
- **Seguimiento del puntero**: ±3° y ±5° de inclinación, 300 ms, solo con punteros finos. Se aplica como un único `transform` sobre el grupo, a lo sumo una vez por cuadro.
- **Ningún bucle**: sin puntero en movimiento, nada se redibuja.

## 12. Accesibilidad

- La capa es `aria-hidden="true"`, `inert` y `pointer-events: none`: fuera del árbol de accesibilidad, fuera del orden de tabulación y sin capturar el puntero.
- No contiene nada enfocable ni ningún `<canvas>`.
- **Ninguna información existe solo en la escena**: el póster y la escena no tienen texto; todo lo que la portada dice está en la tarjeta.
- El texto de la tarjeta va delante, sobre su propio fondo sólido: el contraste no depende nunca de lo que haya detrás.
- Sin parpadeo, sin bucles, sin cámara que se mueva sola.

Verificación de DOM, estilos calculados y teclado en el navegador de pruebas. **No se hizo con lector de pantalla real.**

## 13. Estrategia móvil

Por debajo de 1024 px la portada va a una columna y la escena competiría con el contenido: se muestra el póster y no se descarga la escena. Las hojas del póster asoman solo por arriba y siempre dentro del ancho de la tarjeta, así que no pueden desbordar a 390 px.

## 14. Modo oscuro

Todo son tokens de la Fase 18 (`bg-card`, `border`, `--tone-*-edge`): una sola implementación, sin destellos claros. Verificado con capturas a 1280 y 390 px.

## 15. Presupuesto

| Techo (`BUDGETS.md`) | Resultado |
|---|---|
| Aumento del *bundle* inicial JS: 0 KB | **0 KB** (`app-*.js` 204.27 kB antes y después) |
| Todo el 3D en fragmentos diferidos | Sí: `recruitment-scene-*.js`, 2.51 kB / 1.26 kB gzip |
| Modelo GLB ≤ 1.5 MB, texturas ≤ 1024 px, ≤ 4 texturas | **Sin modelos ni texturas**: todo es DOM generado por código |
| Triángulos ≤ 100 000 | No aplica: cuatro capas de DOM |
| Llamadas de dibujo ≤ 60 | No aplica como tal —el techo está pensado para WebGL—: la escena son cinco capas que compone el navegador (grupo y cuatro hojas) |
| FPS ≥ 45 | **61** con el puntero en movimiento continuo (techo de la pantalla) |
| Primer cuadro ≤ 1.5 s tras entrar en viewport | **≈ 500 ms desde el inicio de la navegación** |
| Memoria GPU ≤ 150 MB | Estimada en **≈ 15 MB** en el peor caso (cinco capas de ~495×378 px a DPR 2). No medida: el entorno no la expone |
| Pausado fuera de pantalla | No hay bucle que pausar; la escucha del puntero solo existe mientras la escena está a la vista |

**Desviaciones declaradas:**

- `app-*.css` creció **0.11 kB gzip** (99.34 → 99.90 kB) por las utilidades del póster, que ADR-003 exige visible al instante. El 3D en sí no añade CSS: sus transformaciones van en línea dentro del fragmento diferido.
- El fragmento de la portada creció **1.46 kB gzip** (2.41 → 3.83 kB): póster, detector de capacidad y capa.

## 16. Medición real

Mediana de cinco cargas por corrida, en el contenedor E2E, a 1280 px:

| Métrica | Línea base | Después (3 corridas) |
|---|---|---|
| DCL | 126 ms | 140 · 132 · 136 ms |
| `load` | 132 ms | 145 · 136 · 144 ms |
| Archivos JS | 12 | 13 (el fragmento de la escena) |
| JS decodificado | 586 KB | 592 KB |
| Escena lista | — | 506 · 499 · 502 ms |
| FPS con puntero en movimiento | — | 61 · 61 · 61 |

La portada carga entre 6 y 14 ms más tarde que la única corrida de línea base, con unos 8 ms de dispersión entre corridas: parte es ruido del contenedor y parte, probablemente, coste real de los 4 kB más del fragmento. No es perceptible. **LCP no se informa**: Chromium no lo reporta dentro del iframe en que Cypress carga la aplicación, y un cero no es una medición.

## 17. Assets

Ninguno. No hay modelos, texturas, imágenes ni recursos remotos: las hojas son `div` con tokens. Nada que licenciar ni que comprimir.

## 18. Pruebas de componente

`experience-3d/experience-3d.test.tsx`, 13 pruebas: las siete condiciones de fallback de la función pura, que la ausencia de WebGL no afecta a la decisión, que lo primero que se pinta es el póster, que la capa es decorativa (`aria-hidden`, `inert`, sin eventos), que no hay nada enfocable ni lienzo, que la capa es absoluta —sin desplazamiento de diseño— y que el póster no contiene texto. No se prueba nada interno del motor de composición.

## 19. Cypress

`cypress/e2e/e2e-18-profundidad-portada.cy.js`, 8 pruebas: fragmento que falla → póster y portada entera; escena montada desde su propio fragmento; **no se descarga hasta entrar en el viewport**; movimiento reducido; móvil sin descarga ni desbordamiento; equipo modesto; **sin WebGL la escena se muestra igual**; capa decorativa e inerte con el texto por delante. Sin esperas de tiempo fijo.

## 20. Evidencia

`docs/v1.1/phase-20-screenshots/`: escena en claro y en oscuro a 1280 px, póster con movimiento reducido a 1280 px, póster a 768 px y póster en oscuro a 390 px. Las especificaciones de captura y de medición están en `cypress/visual/` y no forman parte de la suite.

## 21. Limitaciones

- La escena es sutil a propósito: se lee como profundidad, no como protagonista. Si el equipo quiere más presencia, el margen está en la geometría, no en cambiar de tecnología.
- Sin lector de pantalla real y sin medición de memoria GPU: la cifra de §15 es una estimación.
- El entorno de medición es un contenedor, no un escritorio de gama media: los FPS son indicativos.
- En pantallas táctiles de más de 1024 px la escena se muestra, pero quieta en su orientación de reposo: sin puntero fino no hay seguimiento del puntero.

## 22. Deuda técnica y gobierno

- **ADR-003 y RNF-C seguían marcados como «pendiente de decisión».** Esta fase se ejecutó por encargo explícito del equipo, igual que las Fases 18 y 19 se ejecutaron con RNF-A y RNF-B aún como propuesta. Ambos documentos se anotaron sin reescribir su historia (ver `documentation-update-map.md`). **La promoción formal de RNF-C al baseline de v1.1 sigue siendo decisión del equipo.**
- La autorización de dependencias para 3D con WebGL sigue sin responderse: esta fase no la necesitó.

## 23. Para la Fase 21

La auditoría visual global: revisar la portada con la escena junto con el resto de las pantallas, decidir con ojos frescos si la sutileza de la escena es la adecuada, y cerrar la decisión de gobierno sobre RNF-C.
