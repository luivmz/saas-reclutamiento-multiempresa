# Fase 19 — Animaciones y microinteracciones

**Fecha:** 22 de septiembre de 2026
**Rama:** `feature/phase-19-animations` · **Base:** `11832ac` (cierre de la Fase 18)
**Writer principal:** Claude Code · **Reviewer:** Codex (auditoría posterior)

> Fase **exclusivamente de interfaz**. No cambia reglas de negocio, RF, rutas, contratos de API, modelos, Policies, el servicio ML ni ninguna decisión científica de las Fases 14 a 17. RF-23 sigue siendo una decisión humana y RF-29 sigue siendo experimental.

---

## 1. Objetivo

La Fase 18 dejó el sistema visual; esta lo pone en movimiento. El criterio no es «que se vea animado», sino que el movimiento responda a una de estas cinco razones: dar respuesta a una acción, mantener la continuidad espacial, hacer legible un cambio de estado, evitar que algo aparezca de golpe, o confirmar que la interfaz oyó. Lo que no cabe en esa lista no se anima.

Aplicado con honestidad, el resultado es que **se anima poco**. Buena parte del trabajo fue corregir el movimiento que ya existía —heredado del kit de inicio— y quitar el que sobraba.

## 2. Auditoría previa

El proyecto ya tenía movimiento, sin sistema:

| Hallazgo | Dónde | Problema |
|---|---|---|
| `ease-linear` en la barra lateral | `ui/sidebar.tsx` (4 usos) | Sin aceleración: el panel arranca y frena de golpe |
| `transition` a secas y 500 ms de apertura | `ui/sheet.tsx` | Anima diez propiedades y hace lento un panel de uso diario |
| Menús sin duración ni curva | `ui/dropdown-menu.tsx`, `select`, `tooltip` | Heredaban `ease`, la curva más floja del navegador |
| Menús creciendo desde el centro | `ui/dropdown-menu.tsx`, `tooltip` | Un menú anclado a un botón debe crecer desde ese botón |
| `transition-all` | `ui/sidebar.tsx`, `ui/input-otp.tsx`, `two-factor-recovery-codes.tsx` | Anima cualquier propiedad que cambie, incluidas las caras |
| `h-0` → `h-auto` con 300 ms | `two-factor-recovery-codes.tsx` | `auto` no es interpolable: la altura saltaba y la transición no hacía nada |
| Botones sin respuesta a la pulsación | `ui/button.tsx` | Solo cambiaban de color |
| «Movimiento reducido» = cero movimiento | `resources/css/app.css` | Quitaba también lo que ayuda a entender un cambio |
| Nombres accesibles en inglés | `ui/sidebar.tsx` | «Toggle sidebar», «Sidebar», «Displays the mobile sidebar» |
| El foco se perdía al cerrar la navegación móvil | `ui/sidebar.tsx` | Ver §8 |

**No se instaló ninguna biblioteca de motion.** `tw-animate-css` ya estaba, y todo lo que hacía falta se resuelve con transiciones y keyframes de CSS, que además siguen corriendo cuando el hilo principal está ocupado.

## 3. Sistema de motion

Tres curvas y una escala de duración, en `resources/css/app.css`. No son valores inventados: son curvas establecidas, y se declaran **con los nombres de token que Tailwind ya usa**, de modo que cada `transition-*` y cada `animate-in` que ya existía en los componentes pasa a moverse igual sin tocar una clase.

```css
--ease-out: cubic-bezier(0.23, 1, 0.32, 1);      /* entra y sale */
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);  /* se desplaza en pantalla */
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);   /* cajón */
--default-transition-timing-function: var(--ease-out);
```

| Duración | Para qué |
|---|---|
| 100–150 ms | Respuesta a una pulsación, cambio de color, tooltip |
| 200 ms | Desplegables, menús, diálogos, barra lateral |
| 250 ms | Cajón de navegación móvil |

Nada de interfaz pasa de 300 ms. **`ease-in` no se usa nunca**: empieza lento justo en el instante que la persona está mirando.

## 4. Qué se anima y qué no

| Superficie | Decisión |
|---|---|
| Botones | Ceden un 2 % mientras están pulsados, 100 ms. Es el único movimiento en un elemento que se usa cientos de veces al día, y por eso es casi imperceptible. Un botón deshabilitado no cede |
| Menús, selects, tooltips | Atenuación y escala corta desde el punto de anclaje, 150–200 ms |
| Diálogos | Atenuación y escala desde el centro —no están anclados a nada—, 200 ms |
| Navegación móvil | Cajón con la curva de cajón, 250 ms al abrir y 200 ms al cerrar |
| Barra lateral de escritorio | Curva de cajón en lugar de lineal |
| Errores de formulario | Entran atenuándose con un desplazamiento mínimo, 150 ms. **Nunca una sacudida**: un formulario que tiembla castiga a quien se equivocó |
| Riesgo operacional | El resultado sustituye al esqueleto con una atenuación de 200 ms, sin desplazamiento |
| Códigos de recuperación | Se pliegan con `grid-template-rows`, que sí se puede animar |
| **Transiciones entre páginas** | **No.** Se navega decenas de veces al día; la barra de progreso de Inertia ya da la respuesta inmediata, y animar cada visita solo añadiría espera |
| **Entrada de filas de tabla** | **No.** Los datos que alguien está leyendo no se mueven por estética |
| **Contadores y cifras** | **No.** Ninguna cifra sube desde cero, empezando por el porcentaje de riesgo |
| **Estados vacíos y badges** | **No.** Aparecen al cargar una lista, que es constante; y un badge que late convierte un estado en una alarma |

## 5. Movimiento reducido

Reemplaza a la política anterior, que apagaba todo. «Reducido» no es «ninguno»: lo que molesta es el desplazamiento y el escalado, no que un color cambie.

- se conservan las transiciones de color, opacidad y sombra, acortadas a 120 ms;
- se elimina `transform` de la lista de propiedades animadas, con lo que nada se desplaza ni escala;
- las animaciones de entrada y salida quedan en 0,01 ms: el estado final se aplica igual;
- **el spinner sigue girando**, más lento: su giro es información sobre una espera, no adorno;
- **el esqueleto deja de latir** pero sigue ocupando su sitio y diciendo que falta algo.

Está implementado y probado: `cypress/e2e/e2e-17-motion-accesible.cy.js` emula `prefers-reduced-motion: reduce` con el protocolo del navegador y comprueba la política real, no la declarada.

## 6. Accesibilidad

| Verificado | Cómo |
|---|---|
| El foco no se pierde ni se queda atrapado | Menú de usuario, navegación móvil y diálogo abren con teclado, cierran con Escape y **devuelven el foco al control que los abrió** |
| El anillo de foco no se anima | No hay transición sobre `outline`; el foco sigue siendo inmediato |
| El movimiento no es necesario para entender nada | Ningún estado se comunica solo con movimiento |
| Nada parpadea | No se añadió ninguna animación repetida; las dos infinitas que hay son el spinner y el esqueleto, ambas funcionales |
| La tabla conserva su semántica también con movimiento reducido | Comprobado en `e2e-17` |
| Nombres accesibles en español | «Mostrar u ocultar la navegación», «Navegación», «Secciones disponibles para su rol» |

### Un defecto de foco encontrado y corregido

El panel de navegación móvil se abre por estado y no con un `SheetTrigger` de Radix, así que la biblioteca no sabía a dónde devolver el foco y lo dejaba en `body`: **quien navega con teclado terminaba al principio del documento cada vez que cerraba la navegación**. Se comprobó en el navegador antes de tocar nada y ahora `SidebarTrigger` devuelve el foco al botón que abrió el panel. La prueba que lo fija falla si alguien lo deshace.

## 7. Responsive y modo oscuro

Capturas reales a 1280 y 390 px, en claro y en oscuro, de los estados que el movimiento toca: menú de tema, menú de usuario, diálogo, navegación móvil abierta, panel de riesgo y formulario con errores. Sin destellos claros al cambiar de estado y sin desbordamiento: `cypress/visual/phase-18-overflow.cy.js` sigue en **0 desbordes** sobre 24 páginas × 4 anchos.

## 8. Rendimiento

- Todo lo añadido anima `transform` y `opacity`, que no obligan a recalcular el diseño.
- Se eliminaron los tres `transition-all` que quedaban y se sustituyeron por listas explícitas de propiedades.
- El único `height` que se animaba —y que no animaba nada— pasó a `grid-template-rows`.
- Sin biblioteca nueva: **0 bytes** de dependencia añadida.
- Queda una deuda declarada: la barra lateral de escritorio sigue animando `left`, `right` y `width`, porque su maquetación depende de un espaciador de ancho variable. Cambiarlo a `transform` exige rehacer la estructura del componente, que es alcance de otra fase.

## 9. Pruebas

| Suite | Antes | Ahora |
|---|---|---|
| Componente (`vp test`) | 22 | **23** |
| Cypress | 17 specs / 61 | **18 specs / 69** |
| Laravel | 408 + 8 omitidas | sin cambios |
| Python | 532 | sin cambios |

`e2e-17` cubre: teclado y devolución del foco en menú, navegación móvil y diálogo; la curva del sistema aplicada de verdad; la política de movimiento reducido sobre estilos calculados; spinner y esqueleto bajo movimiento reducido; la tabla intacta con movimiento reducido; y el panel de riesgo entrando sin latido ni alarma. No se mide ninguna duración exacta y no se usa ninguna espera fija arbitraria dentro de la suite.

`motion.test.tsx` fija las decisiones que costaría recuperar: el botón responde a la pulsación y no usa `transition-all`, el error de campo no se sacude, las filas de tabla no entran animadas y el plegado de códigos usa una altura que sí se puede animar.

## 10. Limitaciones

- La verificación de accesibilidad es de DOM, estilos calculados y navegación por teclado real en el navegador de pruebas. **No se hizo con un lector de pantalla.**
- El plegado de los códigos de recuperación de dos pasos no pudo verse en el entorno de demostración porque los usuarios ficticios no tienen la verificación en dos pasos activada. Está cubierto por prueba de componente, no por captura.
- Cómo *se siente* una animación no se decide leyendo código. Lo que queda por revisar con ojos frescos: la apertura del cajón móvil y la respuesta del botón a la pulsación.

## 11. Deuda para fases siguientes

1. La barra lateral de escritorio anima `left`/`right`/`width` (§8): rehacerla con `transform` implica reestructurar el componente.
2. Sigue sin haber pruebas con lector de pantalla real.
3. Fuera del diff de esta fase, la deuda histórica de formato (Pint y `npm run check` sobre archivos anteriores) permanece sin tocar.
