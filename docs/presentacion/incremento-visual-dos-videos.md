# Vídeos de la portada y del detalle público

Continuación del candidato de presentación `c1b842a70388211fcee781ebb519d1f0b76e7cbd`.

- En `/`, el vídeo del colegio ocupa el fondo del hero. El título, la explicación y los accesos son HTML con un degradado de contraste. «Cómo avanza un proceso» reúne las cuatro etapas y el expediente ficticio de la portada.
- En `/empleos/{id}`, cada oferta utiliza el mismo fondo de carpeta con opacidad del 20 %. La convocatoria, el perfil, los criterios y las acciones conservan sus superficies opacas y sus datos propios.
- `ScrollVideo` comparte la carga diferida, el blob para el servidor sin soporte Range y la cola de búsquedas. El fotograma corresponde a la posición de scroll. En móvil, con movimiento reducido y si falla la carga, la escena usa una imagen estática. El cambio dinámico de preferencia se comprueba en E2E-23.

El original del colegio es `result-01a20605-6f95-7e78-ac3e-05bb6156b8a8.mp4` (Kling, 1920 × 1080, H.264, 24 fps, 10,04 s). La copia `public/media/portada/portada-colegio.mp4` abarca de 2,0 a 8,5 s. Se codificó a 1440 × 810 y 24 fps, con un fotograma clave cada cuatro, sin audio y con faststart. El póster WebP se extrae del segundo 5,5 del original. Las ofertas usan el recorte anterior de la carpeta [documentado en el incremento de Higgsfield](incremento-visual-higgsfield.md).

Para verificar, abre el hero y desplázate en ambas direcciones. Después abre dos ofertas desde «Empleos» y comprueba el mismo gesto mientras recorres sus criterios. E2E-23 cubre ambos vídeos, temas, teclado, vista a 320 px, movimiento reducido y fallos de carga sin preparar una base de datos.
