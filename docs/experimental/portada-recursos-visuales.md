# Portada · recursos visuales del incremento de diseño

> **Experimental y local**, rama `design/f37-visual`. No cambia funciones del producto ni estados formales.

## 1. Qué se usó

| Recurso | Origen | Dónde |
|---|---|---|
| Escena en profundidad: tres hojas sin texto (vacante, evidencias y decisión humana) con paralaje según el cursor | CSS 3D y DOM propio, sin imágenes ni dependencias (ADR-003) | `resources/js/components/experience-3d/` |
| Póster de respaldo: las mismas tres hojas, planas | DOM propio | `recruitment-scene-poster.tsx` |
| Fondo de la portada: luces radiales en petróleo y ámbar, y una retícula que se desvanece | CSS (`.hero-backdrop` y `.hero-grid` en `app.css`) | Sección principal de `welcome.tsx` |
| Iconos | `lucide-react`, ya instalado | Portada y pantalla de evidencias |

**Higgsfield: no se usó ningún recurso.** En este entorno no hay acceso: ni herramienta, ni CLI, ni credenciales, ni archivos descargados (comprobado el 22/11/2026). La portada queda completa sin él.

## 2. Recurso pendiente: bucle ambiental para la portada

- **Ubicación prevista.** Detrás de la columna derecha de la portada, debajo de la escena CSS, entre el 20 y el 30 % de opacidad.
- **Punto exacto en el código** (`design/f37-visual`, `0d91bcb`):
  - **Archivo:** `resources/js/components/experience-3d/recruitment-depth.tsx`, componente `RecruitmentDepth`.
  - **Lugar:** dentro del `<div data-cy="recruitment-depth">`, que ya es `aria-hidden`, `inert` y `pointer-events-none`, como **primer hijo**, delante de `SceneBoundary`. Solo se renderiza cuando `showScene` es verdadero, así que hereda la misma condición y la misma carga al entrar en el viewport.
  - **Elemento:** `<video muted loop playsInline autoPlay preload="none" poster="/media/portada/portada-bucle-poster.webp">`, con dos `<source>`, primero el WebM y después el MP4.
  - **Caja:** `absolute -inset-x-16 -inset-y-24 -z-10 rounded-2xl object-cover opacity-25`, para que cubra también las hojas que asoman alrededor del expediente.
  - **Fallo:** con `onError`, el vídeo se retira y queda la escena CSS.
  - **Página:** en `welcome.tsx` no hay que tocar nada. La tarjeta `.z-10` sigue delante, plana y sobre fondo sólido.
- **Nombres de archivo:** `public/media/portada/portada-bucle.webm`, `portada-bucle.mp4` y `portada-bucle-poster.webp`.
- **Carga y respaldo.** Se carga solo cuando hoy se carga la escena (`useSceneCapability`: escritorio de 1024 px o más, sin movimiento reducido, sin ahorro de datos ni equipo modesto). En cualquier otro caso, o si el vídeo falla, queda la composición CSS actual, que ya es el respaldo.
- **Formato.**
  - 16:9, 1920 × 1080, **8 s** en bucle perfecto, 24 fps, sin audio.
  - Entrega en WebM (VP9) y MP4 (H.264), cada uno de 1,5 MB o menos.
  - Póster WebP de 1600 px y 120 KB o menos.
  - Archivos en `public/media/portada/`.
- **Contenido.** Sin personas, rostros, texto, logotipos ni datos. Nada que pueda leerse como un documento real.

**Prompt para Higgsfield (en inglés, por rendimiento del modelo):**

```
Slow, seamless 8-second cinematic loop, 16:9. A calm, softly lit school administration
desk seen from a low three-quarter angle. Three translucent frosted-glass cards float in
layered depth above the desk: a back card with thin teal bars like weighted criteria, a
middle card stacked over a dashed outline like a kept earlier version, and a front card
with a small green check mark and a hand-drawn signature line. The cards drift a few
millimetres and the light slowly moves across them, casting soft shadows on the desk.
Palette: deep petrol teal (#2f6b7d), off-white paper (#f6f8f9), a faint warm amber rim
light. Shallow depth of field, gentle film grain, no camera cut. No people, no faces, no
hands, no readable text, no letters or numbers, no logos, no screens. Calm, trustworthy,
institutional, minimal.
```

**Variante para imagen fija**, si solo se dispone de generación de imágenes:

- el mismo prompt, sin la parte de bucle ni movimiento;
- 16:9, de 2400 × 1350 a WebP de 1600 px y 120 KB o menos.

**Antes de incorporarlo:**

- comprobar visualmente que no hay texto ni rostros;
- medir el peso;
- incorporarlo con `<video muted loop playsinline preload="none" poster=…>` dentro de la capa decorativa (`aria-hidden`, `inert`).

E2E-18 y E2E-22 deben seguir pasando sin cambios.
