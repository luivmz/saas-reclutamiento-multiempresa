# Anfitrión del listado público de empleos (`/empleos`)

> **Rama local `design/anfitrion-empleos`**, del 22/11/2026, creada desde `feature/presentacion-dos-videos` = `2b87f3667dce6f98f8250083cc7dd354aa21a961`, la continuación visual más reciente (los vídeos de la portada y del detalle de oferta, de Codex, se conservan sin cambios).
>
> - **Alcance:** solo el listado público de empleos: presentación, CSS y pruebas. No cambian el backend, los permisos, los datos, ML-01, ML-02, la búsqueda, la paginación ni los vídeos de la portada y del detalle.
> - **Publicación:** sin push ni merge. Ningún estado formal cambia.

## 1. Qué es

Un personaje ilustrado (traje petróleo, carpeta marfil y apuntador) acompaña la exploración de las ofertas desde la derecha del listado.

- **Es decorativo:** `aria-hidden`, `inert` y sin eventos de puntero.
- **Nada depende de él:** ninguna información ni acción.
- **Su sonrisa invita a explorar:** no recomienda, valora ni aprueba ninguna oferta.

## 2. Recursos

Originales en la carpeta Descargas de la PC principal, conservados sin cambios y fuera de Git:

| Original | Qué es (visto entero) | Tamaño · SHA-256 |
|---|---|---|
| `playground-result-1795400090917.mp4` | **Interés.** El cuerpo apenas se mueve; sonrisa con un parpadeo o asentimiento hacia los fotogramas 24 y 72. 4,04 s, 97 fotogramas, 1080 × 1920, 24 fps, con audio. Etiqueta AIGC de Kling | 2 380 006 bytes · `90aff6f8dcc04a488fc491603ae22bd833d8813526e78ca5ed1d254877f52fb7` |
| `playground-result-1795400520065.mp4` | **Señalar.** El apuntador sube (fotogramas 21–36), pasa a media altura (≈48), baja con la mirada baja (54–66) y vuelve (≈78 y 87–96). Mismo formato | 2 782 682 bytes · `d6b73f5dbea925ecc0d7a3c95fd95e7ee7b8bad3d9f1022cb80e0d331b4e97f9` |
| `playground-result-1795399280556.jpg` | Imagen base (720 × 1280), con la misma pose de reposo pero otro encuadre | 140 299 bytes · `db5302b7aad659995547b0f9baf00c26d1a7c9cb2b3ab9422d58d93798cc5a51` |

**Copias web en `public/media/anfitrion/`:**

| Archivo | Gesto | Tamaño |
|---|---|---|
| `anfitrion-reposo.webp` | Reposo: póster transparente, fotograma 0 del clip de interés | 22 110 bytes |
| `anfitrion-interes.webm` | Reacción de interés (clip 1) | 523 940 bytes |
| `anfitrion-senala.webm` | Señalar (clip 2) | 535 439 bytes |

**Procesado.** Se usó el `ffmpeg` de la imagen de Cypress y numpy del entorno de `ml-service`, sin dependencias nuevas.

1. **Encuadre.** Un único recorte común a los dos clips (880 × 1728 desde y = 96), escalado a 286 × 562 (unos 280 px de alto a 2×).
2. **Fondo verde fuera, por desmezcla.** El fondo es un verde uniforme, RGB(18, 186, 20).
   - El alfa sale de cuánto domina el verde.
   - El borde toma el color de sus vecinos opacos.
   - En el anillo exterior, G nunca supera max(R, B).
   - No se usó `despill` sobre todo el personaje porque volvía azul marino el traje petróleo y rosada la carpeta.
3. **Silueta.** No se erosiona, para conservar el apuntador, que tiene 3–4 px. Revisados sobre fondo claro, oscuro y a cuadros, con ampliación ×2: pelo, manos, zapatos, carpeta y apuntador, sin halos verdes ni partes perdidas.
4. **Punta del apuntador.** En algunos fotogramas sale del encuadre original por la izquierda. Los primeros 10 px se funden con un degradado en lugar de cortarse en seco.
5. **Codificación.** WebM VP9 con transparencia (`yuva420p`), CRF 33, un fotograma clave cada 6, sin audio ni metadatos.

**Por qué no la imagen base.** El póster sale del fotograma 0 del clip de interés, y no de la JPG, para que póster y clips coincidan píxel a píxel. Los fotogramas de reposo de ambos clips (0 y 96) se diferencian tanto como dos fotogramas seguidos, así que el fundido entre capas no produce saltos.

## 3. Comportamiento (`JobHost`, `host-logic.ts`)

| Estado | Qué hace |
|---|---|
| Reposo | Póster |
| Interés | Al entrar con el cursor en una oferta, o con el foco del teclado en su enlace: el clip 1, una vez, como mucho cada 8 s. Si el cursor sale del listado durante la reacción, funde al reposo sin esperar a que termine |
| Señalar | Recorre el clip 2, fotograma a fotograma (30 por segundo), hasta la pose cuyo apuntador mira a la **zona** de la oferta activa respecto de la mano: arriba (27), media altura (48 o 78) o abajo (60). Elige el camino más corto: el clip se trata como un ciclo, porque el 96 ≈ 0 |
| Desplazamiento | Sin oferta activa, mientras la persona se desplaza (rueda, gesto táctil, teclado o barra), atiende a la oferta más cercana al centro. La restauración del desplazamiento al cambiar de página no cuenta |
| Seguimiento | El contenedor se inclina hasta 7° en horizontal y 4° en vertical hacia el cursor. El personaje no se desplaza ni se deforma |
| Vuelta al reposo | Sin oferta activa (0,9 s tras salir del listado o perder el foco), recorre el clip hasta el reposo, más deprisa, y funde al póster |

**Oferta activa.** Se resalta con un borde algo más marcado, sin cambiar su contenido. Manda la última: pasar deprisa entre tarjetas no reinicia nada ni acumula reproducciones, y hay una sola búsqueda en curso a la vez.

**Alcance real del seguimiento.** Los gestos son pregrabados. El personaje no sigue el cursor con los ojos ni con el brazo; elige, de los fotogramas que existen, la pose que apunta hacia la zona de la oferta. Son tres zonas verticales: siempre señala hacia la izquierda, donde están las ofertas.

## 4. Cuándo se carga y cuándo no

| Caso | Resultado |
|---|---|
| Menos de 1280 px | No hay columna ni anfitrión; no se descarga nada |
| 1280 px o más, con puntero táctil, movimiento reducido, ahorro de datos, equipo modesto o un navegador que no muestra la transparencia del WebM (Safari) | Solo el póster, sin descargar los clips |
| 1280 px o más con puntero fino | Los clips se descargan (blob, compartido entre visitas) la primera vez que el anfitrión se ve |
| Falla un clip | Se prescinde de él: sin el de interés, señala directamente |
| Falla el póster | El anfitrión desaparece |

**Siempre:**

- **Pausa:** la actividad se detiene con la pestaña oculta o el anfitrión fuera de la vista.
- **Desmontaje:** limpia escuchas, temporizadores, cuadros pendientes y vídeos.
- **Movimiento reducido con la página abierta:** vuelve al póster y suelta los clips.
- **Sitio propio:** una columna `sticky` dentro del área del listado, centrada en vertical. No tapa ofertas, búsqueda, paginación, navegación ni el pie.

## 5. Pruebas (22/11/2026, PC principal, proyecto Docker aislado `anfitrion`)

| Prueba | Resultado |
|---|---|
| Tipos · componentes | 0 errores · 89 passed (12 archivos; 8 nuevas de `host-logic`) |
| `vp check` de lo cambiado · build | Sin errores · correcto |
| E2E-24 (nueva) | **16/16** en tres ejecuciones seguidas |
| Specs existentes que pasan por `/empleos` | E2E-04, 05, 12, 13, 19 y 23: **6 de 6, 39/39** |
| Demo en Chrome 157 (headless, con GPU), temas claro y oscuro | Reposo, interés, señalar a media altura, abajo (60) y arriba (27), pasos rápidos (0 reproducciones nuevas), vuelta al reposo, desplazamiento con la rueda en los dos sentidos, foco con Tab y salida. 0 búsquedas solapadas |

**Hallazgos durante las pruebas, corregidos:**

- **Reacción perdida tras remontar.** Al cambiar de página, Inertia vuelve a montar el listado. Si el cursor entraba en una oferta antes de que los clips decodificaran su primer fotograma, la reacción se perdía. Ahora la disponibilidad se mide en el momento, y al terminar de cargar reacciona si hay oferta activa.
- **Restauración del desplazamiento.** El desplazamiento de restauración se tomaba como exploración. Ahora solo cuenta el que precede una entrada de la persona.

**Límites conocidos:**

- **Navegadores:** Firefox y Safari no se probaron. Safari queda con el póster por diseño.
- **Accesibilidad y uso real:** no se probaron un lector de pantalla real ni una sesión con ratón físico.
- **Electron:** después de `cy.screenshot`, Cypress con Electron reduce `requestAnimationFrame` a cerca de un cuadro por segundo. Por eso el gesto avanza con un temporizador a la cadencia del clip, y E2E-24 hace sus capturas al final de cada prueba.

## 6. Arranque local

En el worktree `Conso1_SaaS_Reclutamiento_anfitrion`, con su `.env` local (que no se versiona) en los puertos 8040 (app), 8041 (E2E), 5472 (PostgreSQL) y 6419 (Redis):

```powershell
docker compose -p anfitrion up -d --wait
docker compose -p anfitrion exec app npm run build
```

Se abre `http://localhost:8040/empleos`. Datos solo ficticios (`DemoSeeder` en su base propia).
