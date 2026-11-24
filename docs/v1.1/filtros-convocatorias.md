# Filtros y comparación de convocatorias públicas

**Base del lote.** Rama local `feature/filtros-convocatorias`, continuación de `fix/identidad-claridad-ui` en `a3addd51dd486934ed735be58ec6d0619ddbac36`. La publicación de vacantes corresponde a RF-07. Este incremento afecta la consulta pública en `GET /empleos`.

| Regla de consulta | Implementación | Verificación |
|---|---|---|
| El puesto se busca en el título. Se deben cumplir simultáneamente la búsqueda y todos los filtros aplicados. | `PublicVacancyController::index` y `PublicVacancyFilterRequest` | `PublicVacancyFiltersTest` compara los códigos devueltos para cada criterio y sus intersecciones. |
| Solo las convocatorias publicadas aportan resultados y opciones. El vencimiento conserva la publicación y su distintivo. | `publishedVacancies()`, `filterOptions()`, `VacancyResource` | PHPUnit contrasta dos organizaciones públicas con una tercera que solo tiene borradores y convocatorias cerradas. Verifica el distintivo y que ya no se acepten postulaciones. |
| Un enlace representa los criterios aplicados. Las páginas conservan el total y el orden por fecha de cierre, con desempate por identificador. | Paginador de Laravel, `JobsFilters`, `job-filters.ts` | PHPUnit verifica 14 coincidencias repartidas en dos páginas y comprueba que sus códigos sean distintos. E2E-28 recarga, retrocede, avanza y quita criterios. |
| Una dirección inválida lleva al listado completo con aviso. Una página positiva sin filas de una consulta con resultados ofrece volver a su primera página con los mismos criterios. | Validación del servidor, aviso del listado y `JobsEmptyState` | PHPUnit valida tipos, límites y valores públicos. Las pruebas del componente y E2E-28 verifican los mensajes y las salidas. |

Los parámetros son `q` (hasta 150 caracteres), `organizacion` (identificador), `ubicacion` (texto exacto), `contrato` (valor del catálogo publicado) y `page` (entero positivo). Por ejemplo, `/empleos?q=docente&contrato=tiempo_completo` busca puestos que contengan «docente» con contrato a tiempo completo. Los valores disponibles dependen de las convocatorias publicadas en cada instalación.

**Uso.** En un celular, «Filtros» despliega los tres selectores. «Buscar» aplica todos los controles y vuelve a la primera página. Cada etiqueta activa permite retirar un criterio. «Limpiar filtros» conserva el puesto buscado. Cuando coexisten búsqueda y filtros, «Limpiar todo» vuelve al listado completo. El contador comunica el total de coincidencias en una región de estado. Las tarjetas tienen un único enlace al detalle y muestran los mismos campos en el mismo orden.

## Verificación local del 23 de noviembre de 2026

Compose `filtros` sirvió los recursos compilados de este worktree. PostgreSQL identificó las bases reales `reclutamiento_testing` (PHPUnit) y `reclutamiento_e2e` (Cypress y Chrome). Los resultados corresponden al trabajo de esta rama sobre la base indicada.

| Control | Resultado |
|---|---|
| `php artisan test` | 626 aprobadas, 8 omitidas, 4079 aserciones. La verificación de correo está desactivada por A-01. |
| `php artisan test --filter=PublicVacancyFiltersTest` | 21 aprobadas y 349 aserciones. Son parte de la suite anterior. |
| `npm run types:check`, `npm run build` y `vp test --run` | Tipos y compilación correctos. 117 pruebas de componentes y utilidades aprobadas en 19 archivos. El build conserva el aviso del paquete opcional de fuentes `fontaine`. |
| `vendor/bin/pint --test`, `vendor/bin/phpstan analyse`, `vp check` | Formato PHP en los tres archivos del lote, análisis estático del controlador y la solicitud de validación, y formato/lint de los siete archivos JS/TS afectados. |
| Cypress 15.3.0, Electron 136 | 63 casos aprobados en siete especificaciones afectadas. E2E-04 (2), E2E-19 (8), E2E-23 (13), E2E-24 (16), E2E-26 (10), E2E-27 (11), E2E-28 (3). |
| Chrome, carga | Con una petición real retenida en el navegador se observó el anuncio de búsqueda y el botón deshabilitado. Al liberar la petición aparecieron el total y el botón disponible. |
| Chrome, paginación con datos ficticios | Una consulta de 14 coincidencias mostró 12 y 2 en páginas sucesivas. Se conservaron el total y los criterios al recargar y navegar por el historial. Cambiar el puesto desde la segunda página volvió a la primera. |
| Chrome, revisión visual | 14 capturas de escritorio y móvil emulado (1440, 390 y 320 px), temas claro y oscuro. Las 14 vistas respondieron HTTP 200 y el ancho del documento coincidió con el ancho visible. |

En la primera instrumentación de teclado de E2E-28, Enter sobre el botón de filtros no abrió el panel en Electron. Al registrar los eventos de la simulación con `type`, el clic llegó al botón de envío. En Chrome se comprobó el recorrido completo con Tab, Enter y Tab. Cypress verifica la apertura por Espacio y el avance del foco al primer selector.

Las ocho capturas anteriores proceden del trabajo recuperado de Claude. Las catorce posteriores están en `D:/bt/propuesta-visual/lote3/despues/capturas/`; las mediciones en `despues/medidas.json` y los logs por control en `validacion/`, dentro del mismo directorio del lote. La comprobación de teclado y de la región de estado se realizó en navegador. Quedan fuera de esta evidencia el dispositivo físico y un lector de pantalla.
