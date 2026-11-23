# Responsive y auditoría técnica de cierre

**Fecha:** 23 de noviembre de 2026 (America/Lima). **Base:** 955884167817a35829ad26aab71deb80f03ada29, árbol 26c23ba8dcc6a23ef3f8a379b6df7d0ed8229f84. **Candidato probado:** 803393f643171d69110020a48f0aef784a9fcbff, árbol 69b891c4aeb8ef72477754af57a8e5412f559350. Esta revisión la realizó el mismo implementador.

## Cambios y hallazgos

| Severidad | Hallazgo reproducido | Corrección y comprobación |
|---|---|---|
| Media | A 768 px el panel fijo de 256 px reducía el espacio de Reportes. En el expediente había campos de fecha y hora recortados. | Panel modal por debajo de 1024 px, con cierre y recuperación del foco. Los formularios de programación se muestran en una columna por debajo de 1280 px. |
| Media | A 320 px se truncaba el aviso de apoyo a la decisión de Ranking y la búsqueda larga tenía poco espacio. | Se habilitó el ajuste de línea en las alertas y se apiló el buscador por debajo de 360 px. Las tablas mantienen sus encabezados y una región de desplazamiento lateral con nombre. |
| Media | A 320 px y texto al 200 %, la portada superaba el ancho disponible. | Las columnas de la portada se ciñen al ancho de la página. El texto y los CTA pueden ocupar más de una línea. |
| Media | La altura de un diálogo centrado podía dejar sus controles fuera del área visible en un viewport de 300 px. | La altura máxima depende del viewport. El contenido se desplaza y el cierre devuelve el foco. |
| Baja | La cabecera pública a 320 px solo mostraba el icono como marca y tenía objetivos de 32 px. | La marca se lee, las acciones principales miden 44 px y la cabecera sigue el flujo en pantallas estrechas. |
| Baja | En pantallas anchas, el listado podía dejar una columna vacía al faltar el anfitrión. Una tablet ancha podía solicitar vídeos decorativos. | La columna aparece si se muestra el anfitrión. Las escenas se quedan en póster cuando el puntero principal es táctil. |

La bolsa conserva las vacantes publicadas (RF-07). Cuando el servidor indica que ya no se reciben postulaciones, la interfaz pública informa el cierre de la ventana y mantiene disponible la consulta de la vacante.

## Matriz del navegador

Se usó Chrome 157.0.8103.79 para Windows con emulación de pantalla, puntero y preferencias. Se probaron 320, 360, 390, 430, 768, 1280 y 1440 px en claro y oscuro.

| Área | Recorrido comprobado | Resultado |
|---|---|---|
| Público | Portada, bolsa, resultado vacío, dos ofertas, registro y acceso | CTA accesibles, lista paginada de 14 ofertas, pósteres y texto legible. |
| RR. HH. | Panel, requerimientos, vacantes, edición, postulaciones, programación, evidencias, historial, proceso cerrado, Reportes y notificaciones | Navegación y lectura en ambos temas. El formulario de Reportes muestra el error de rango excesivo. |
| Dirección y Demo B | Ranking, auditoría, indicadores y filtros de Reportes | Aviso humano completo. Opciones de vacante propias de cada organización. |
| Solicitante, evaluador y postulante | Paneles, formulario de requerimiento, evaluación, perfil y postulaciones | Contenido y acciones disponibles según rol. |
| Interacción | Recorrido táctil del CTA, tecla Espacio, enlace de salto, cierre del panel, diálogo con viewport 320 × 300 y texto al 200 % | Se comprobó el flujo de la página y la recuperación del foco. Cypress cubre el cierre por Escape. |
| Medios | Portada y dos ofertas con fotograma inicial, avance y retroceso, movimiento reducido inicial y dinámico, bloqueo de medios, puntero táctil y fino | Chrome comparó píxeles decodificados. El vídeo del detalle conserva el 20 % de opacidad. Al bloquear vídeos y clips se mantienen los pósteres. |

La inspección geométrica revisó 504 combinaciones de 36 pantallas sin desbordamiento de página ni errores de consola en ese recorrido. Los campos nativos de una sola línea pueden desplazar internamente valores largos durante la edición. Se revisó el texto al 200 % ajustando el tamaño raíz en el navegador y el diálogo con un viewport reducido. No hubo un teléfono físico ni se midió una tasa de fotogramas. Los errores de red provocados por bloquear medios quedan asociados a ese escenario.

## Verificación técnica

| Control | Comando o evidencia | Resultado |
|---|---|---|
| Entorno | `docker compose -p responsiveqa … ps` e inspección de montaje, red y volúmenes | App en 8068. Bases `reclutamiento`, `reclutamiento_testing` y `reclutamiento_e2e` verificadas. |
| PHPUnit | `php artisan test` | 543 aprobadas, 8 omitidas por verificación de correo desactivada en Fortify, 3.130 aserciones. |
| Compilación y tipos | `npm run build` y `npm run types:check` | Correctos. |
| Componentes | `npx vp test --run` | 102 aprobadas en 15 archivos. |
| Lint | `npx vp check` en los archivos modificados y `git diff --check` | 19 archivos con formato correcto y 18 analizados sin errores ni avisos de lint. Los componentes UI excluidos por la configuración se revisaron con tipos, diff y navegador. |
| Cypress | Cypress 15.3.0, Electron 136, 26 specs, base E2E propia | 156/156 casos aprobados en la misma ejecución, 26/26 specs, 0 fallos (08:43). |
| ML-01 | `pytest` de esquema, partición temporal y métricas. Comprobaciones FastAPI con el artefacto local existente | 123 pruebas seleccionadas. SHA-256 del modelo, freeze, 15 campos, token interno, umbral y respuesta al faltar el binario verificados. El artefacto se conservó y no se reentrenó. |
| ML-02 | PHPUnit, E2E-21 y consulta en Chrome | Recuperación BM25, procedencia, abstención y acceso según rol. El corpus de evaluación y sus resultados corresponden a su corte histórico. |

La revisión de autorización utilizó los casos de aislamiento, archivos privados, evidencias, estados cerrados, permisos de Reportes y decisión humana. PHPUnit cubrió `EXPERIMENTAL_EVIDENCIAS` con ambos valores y el respaldo descriptivo de Laravel sin ML-01. Se verificaron el diff y los archivos de entrega con Git. El alcance funcional se limitó al frontend y sus pruebas. En Chrome, con la bandera apagada, la ruta de evidencias devolvió 404 y desapareció su enlace. El panel de riesgo respondió 200 sin predicción con ML-01 desactivado y con la conexión rechazada. El entorno demo se restauró tras ambas comprobaciones.

El primer intento focal de la prueba de tablet no activó el botón con la secuencia de teclas de Cypress. Se comprobó la activación por Espacio en Chrome y se cambió el método de activación del caso E2E. Después del primer Cypress completo se corrigió el desbordamiento con texto al 200 %. La tabla usa la ejecución completa posterior. También se corrigió un aviso de lint en el helper de animaciones.

## Evidencia y referencias

- Copias locales en `D:/bt/responsive-qa/`. El manifiesto `SHA256SUMS.txt` identifica los logs, las capturas y las matrices. Los perfiles de Chrome permanecen fuera del paquete.
- Compare `antes/portada-320.png`, `antes/reportes-768.png`, `antes/ranking-320.png` y `antes/portada-1280.png` con los mismos nombres en `final/`. Las comparativas están en `comparativas/`. Las capturas de avance y retorno de los vídeos y la comparación de Reportes entre organizaciones están en `flujos-final/`.
- Los archivos DOCX y PDF F29H v2 conservan el corte académico anterior. La guía de arranque y esta nota registran el cierre de interfaz.
- SonarQube conserva su alcance histórico. Consultas del CI por rama en el [historial de ejecuciones](https://github.com/luivmz/saas-reclutamiento-multiempresa/actions/workflows/tests.yml).

Para reproducir desde un clon, siga la [guía de entrega integrada](ENTREGA_INTEGRADA.md).
