# Presupuestos de rendimiento y accesibilidad

Aplican solo si el equipo aprueba la experiencia 3D. Son techos, no objetivos.

## Activos

| Recurso | Techo | Nota |
|---|---|---|
| Modelo GLB comprimido | 1.5 MB | Draco o Meshopt obligatorio |
| Triángulos en escena | 100 000 | Contando todas las instancias visibles |
| Texturas | 1024 × 1024 | Formato comprimido; sin texturas sin usar |
| Número de texturas | 4 | Reutilizar materiales |
| Llamadas de dibujo | 60 | Fusionar geometrías estáticas |
| Aumento del *bundle* inicial | 0 KB | Todo el 3D va en fragmentos diferidos |

## Ejecución

| Métrica | Techo |
|---|---|
| Cuadros por segundo en escritorio de gama media | ≥ 45 |
| Tiempo hasta el primer cuadro tras entrar en viewport | ≤ 1.5 s |
| Memoria GPU estimada | ≤ 150 MB |
| Consumo cuando el canvas no está visible | pausado (`frameloop="demand"` o desmontado) |

El bucle de render se detiene cuando la pestaña está oculta o el contenedor sale del viewport. Un canvas que sigue renderizando fuera de pantalla es un defecto.

## Accesibilidad

- `prefers-reduced-motion: reduce` ⇒ poster estático, sin animación. No es configurable por el sitio.
- El canvas es decorativo: `aria-hidden="true"` y sin foco de teclado.
- Toda la información relevante existe en el DOM, no solo en la escena.
- El contraste del texto sobre el fondo 3D cumple WCAG AA en cualquier cuadro de la animación; si no se puede garantizar, el texto va sobre una capa sólida.

## Cómo medir

1. **Línea base antes de tocar nada**: `npm run build` y registrar el tamaño de los fragmentos; medir la carga de la portada actual.
2. Tras implementar: comparar tamaño de *bundle*, tiempo de carga y FPS contra la línea base.
3. Probar con WebGL deshabilitado, con `prefers-reduced-motion` activo y en viewport móvil: las tres veces la página debe funcionar completa.
4. Ejecutar la suite Cypress: los `data-cy` y los flujos existentes no cambian.
5. Registrar los números reales medidos. Sin medición no hay aprobación.

## Criterios de rechazo

Se descarta la propuesta 3D si: supera cualquier techo y no puede reducirse, degrada la carga de la portada de forma perceptible, rompe alguna prueba E2E, obliga a modificar pantallas prohibidas, o exige dependencias que el equipo no autoriza.
