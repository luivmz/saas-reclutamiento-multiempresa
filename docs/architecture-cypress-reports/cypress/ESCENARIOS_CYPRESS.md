# Escenarios automatizados con Cypress

> La descripción de los resultados conserva los nombres de la práctica del 09/11/2026. En la entrega integrada, el comando para Reportes usa E2E-25.

> Actividad 3 de la guía. Cypress **ya estaba integrado** en el proyecto (Fase 9 y siguientes). No se reinstaló: se inspeccionó, se ejecutó y se amplió con el spec del módulo nuevo (`e2e-20-reports.cy.js`). Todos los escenarios corren sobre la **aplicación real** (Laravel + React compilado) en el entorno E2E aislado, con datos **ficticios** de `DemoSeeder`.

## 1. Configuración verificada

| Elemento | Valor real | Archivo |
|---|---|---|
| Versión | Cypress **15.3.0** (imagen `cypress/included:15.3.0`, navegador Electron) | `docker-compose.yml` (servicio `cypress`), `package.json` (`cy:open` usa `cypress@15.3.0`) |
| Instalación | En contenedor Docker, no como dependencia npm del proyecto. `npx cypress verify` no aplica en el host porque el binario vive en la imagen; la verificación equivalente es que la imagen ejecute la suite (sección 4) | `docker-compose.yml` |
| Configuración | `cypress.config.cjs` | raíz |
| `baseUrl` | `http://localhost:8001` en el host; `CYPRESS_baseUrl=http://app-e2e:8000` dentro de Compose | `cypress.config.cjs`, `docker-compose.yml` |
| Specs | `cypress/e2e/**/*.cy.js` (21 specs tras esta práctica). `cypress/visual/` contiene specs de QA visual (fases 18–21) que no entran en el `specPattern` por defecto | `cypress.config.cjs` |
| Soporte | `cypress/support/commands.js`: `dataCy`, `resetDatabase`, `loginAs` (con `cy.session`), `waitForQueue`, `appRequest`, `idFromPath`; `dates.js` (fechas en `America/Lima`) | `cypress/support/` |
| Fixtures | `users.json` (correos demo por rol), `demo.json` (ids de DemoSeeder), `cv-ficticio.pdf` | `cypress/fixtures/` |
| Aislamiento | Perfil `e2e`: `app-e2e`/`queue-e2e` con `APP_ENV=e2e`, base `reclutamiento_e2e` y Redis DB 2/3. `POST /__e2e/reset` protegido por token (`.env.e2e`, **no versionado**) y rechazado si la base no es la E2E (DEF-13) | `docker/php/init-e2e-env.sh`, `app/Http/Controllers/Testing/E2eController.php` |
| Política de calidad | `testIsolation: true`, `retries: 0` (una falla intermitente se investiga, no se oculta), `video: false`, captura automática al fallar | `cypress.config.cjs` |
| Selectores | Atributos `data-cy` estables; sin selectores CSS de presentación | todos los specs |
| Esperas | Sin `cy.wait(ms)` arbitrarios en los escenarios; la única espera fija es el intervalo de sondeo de 250 ms dentro de `waitForQueue`, que comprueba el estado real de la cola | `commands.js` |

Comandos (scripts reales de `package.json`):

```sh
npm run cy:run                                   # prepara .env.e2e y ejecuta la suite completa en Docker
npm run cy:run -- --spec cypress/e2e/e2e-25-reports.cy.js   # un spec en la entrega integrada
npm run cy:open                                  # modo interactivo en el host (requiere Cypress local)
```

## 2. Escenarios seleccionados (11 grupos, cobertura de la guía)

La guía pide al menos 5 escenarios. Se documentan **11 grupos de escenarios reales**: 10 ya existentes y 1 nuevo (Reportes, con 9 casos). Abarcan los tipos que pide la guía 3.2: acceso y autenticación, registro, edición, validación de formularios, navegación, procesos principales y, en este caso, reportes.

**Eliminación de información: no aplica por diseño.** Las rutas de negocio se declaran `->except('destroy')` (`routes/web.php`) para preservar la trazabilidad y la auditoría *append-only*. Las decisiones negativas se registran como transiciones de estado (descartar, rechazar, cerrar), no como borrados. Por eso no se creó una prueba de eliminación artificial; el descarte con motivo obligatorio está cubierto en CY-07.

| ID | Funcionalidad | Objetivo | Precondiciones | Datos de prueba | Procedimiento (acciones de Cypress) | Resultado esperado | Spec |
|---|---|---|---|---|---|---|---|
| CY-01 | Acceso y autenticación | Verificar que cada rol inicia sesión y ve solo su menú | BD E2E reiniciada | 5 usuarios demo (`users.json`), contraseña demo por variable de entorno | Visita `/login`, escribe correo y contraseña, pulsa ingresar; comprueba la ruta y los `nav-*` visibles u ocultos | Redirige a `/dashboard`; badge del rol; menú propio visible y ajeno inexistente | `e2e-01-login` (5 casos) |
| CY-02 | Autenticación negativa | Rechazar credenciales inválidas | idem | correo de RR. HH. y contraseña incorrecta | Envía el login | Mensaje `login-error`; permanece en `/login`; `/dashboard` responde 302 | `e2e-01-login` |
| CY-03 | Registro de información | Registrar y enviar un requerimiento (RF-01) | Solicitante autenticado | Puesto «Docente de Ciencias - Secundaria (E2E)», 2 plazas | Abre «Nuevo requerimiento», completa el formulario, guarda y envía a RR. HH. | Requerimiento en Borrador → «Enviado a RR. HH.» y listado actualizado | `e2e-02` caso 1 |
| CY-04 | Validación de formularios | Impedir registros incompletos o inválidos | idem | Formulario vacío; ponderaciones que no suman 100 | Envía el formulario vacío; edita un criterio a 10 % y guarda | No se crea el requerimiento; la vacante muestra observaciones y «Publicar» queda deshabilitado | `e2e-02` caso 2, `e2e-04` caso 2 |
| CY-05 | Registro y edición de vacante | Crear una vacante desde un requerimiento aprobado, editar su configuración y publicarla | RR. HH. autenticado; requerimiento aprobado sin vacante | Título, fechas, perfil y criterios ficticios; plazo objetivo | Genera la vacante, completa campos y guarda; edita la vacante en borrador (plazo objetivo); publica | Vacante «Publicada» visible en `/empleos`; el valor editado persiste al reabrir el formulario | `e2e-04` caso 1, `e2e-14` |
| CY-06 | Proceso principal: postulación | El postulante completa su perfil, sube su CV y postula | Postulante demo sin postulación | `cv-ficticio.pdf` | Completa el perfil, carga el CV, postula a la vacante publicada | Confirmación y notificación de recepción | `e2e-05` |
| CY-07 | Cambio de etapa | RR. HH. preselecciona una postulación y el postulante es notificado; descartar exige motivo | Postulación en estado «Postulación registrada» | Comentario ficticio | Abre el expediente, escribe un comentario y preselecciona; intenta descartar sin motivo | Badge «Preseleccionado», historial actualizado, notificación; sin motivo no se descarta | `e2e-06` |
| CY-08 | Evaluación | El evaluador registra puntajes dentro del rango de cada criterio | Evaluación asignada en la demo | Puntajes 0–20 | Abre «Mis evaluaciones» y registra los puntajes | Evaluación completada; rango validado | `e2e-07` |
| CY-09 | Navegación entre módulos / flujo integral | Recorrer el proceso completo entre módulos y roles | BD reiniciada | Datos generados por el propio flujo | 12 pasos: requerimiento → validación → aprobación → vacante → postulación → preselección → evaluación y entrevista → finalista → ranking → decisión humana → selección y cierre → notificación → auditoría | Cada módulo recibe el estado del anterior; decisión final humana; auditoría registrada | `e2e-13` (12 casos) |
| CY-10 | Aislamiento multiempresa | Una organización no ve ni modifica recursos de otra | Usuarios de las organizaciones A y B | Ids de `demo.json` | Lista vacantes y auditoría por organización; pide ids ajenos por HTTP | Solo datos propios; 403/404 ante ids ajenos | `e2e-11` (4 casos) |
| CY-11 | **Reportes (nuevo)** | Ver los 9 casos CY-RPT-01 a 09 de abajo | — | — | — | — | `e2e-20-reports` (9 casos) |

### CY-11 · Escenarios del módulo de reportes (`cypress/e2e/e2e-20-reports.cy.js`)

Datos de prueba: estado conocido de `DemoSeeder` tras `resetDatabase()` (organización A: 9 postulaciones en 3 vacantes publicadas hoy; organización B: 1 postulación).

| ID | Objetivo | Procedimiento | Resultado esperado |
|---|---|---|---|
| CY-RPT-01 | El módulo se abre desde el menú y muestra indicadores de la BD | RR. HH. pulsa `nav-reports`; lee `data-value` de los KPI, las barras por etapa, las columnas semanales y la tabla | 9 postulaciones, 3 vacantes, promedio 3, 8 preselecciones (88,9 %), 1 en evaluación; postulado 1, finalista 3, no seleccionado 2; una semana con 9; 3 filas sin la vacante de B ni el borrador |
| CY-RPT-02 | El filtro por vacante recalcula todo | Selecciona «Auxiliar de Educación Inicial» y pulsa Aplicar | URL con `vacante=3`; 3 postulaciones, 1 vacante, 3 finalistas, 1 fila |
| CY-RPT-03 | El filtro por etapa limita el conjunto | Selecciona «No seleccionado» | 2 postulaciones; barras coherentes |
| CY-RPT-04 | Un período sin registros no inventa datos; Limpiar restablece | Escribe 01/01/2025–31/01/2025, aplica y luego pulsa Limpiar | KPI 0, tasa «—», estado vacío y sin gráficos; tras Limpiar, 9 de nuevo |
| CY-RPT-05 | Los datos son vivos | Lee el KPI (8), preselecciona una postulación desde su expediente y vuelve a Reportes | KPI 9 (100 %); «postulado» 0 y «preseleccionado» 2 |
| CY-RPT-06 | Multiempresa: B solo ve lo suyo | RR. HH. de B abre Reportes | 1 postulación, 1 vacante, 1 fila de B; el selector no ofrece vacantes de A |
| CY-RPT-07 | Multiempresa: filtro ajeno rechazado | RR. HH. de B visita `/reportes?vacante=<id de A>` | Redirige a `/reportes` sin parámetros, muestra el error y sigue en datos de B |
| CY-RPT-08 | Autorización | Solicitante, evaluador y postulante abren el panel y piden `/reportes` | Sin entrada de menú; HTTP 403 |
| CY-RPT-09 | Aprobador y responsive | Aprobador en viewport 390×844 | 9 postulaciones; tabla visible; `scrollWidth ≤ 390` (sin desplazamiento horizontal) |

## 3. Resultado obtenido por escenario

Ver [`RESULTADOS_CYPRESS.md`](RESULTADOS_CYPRESS.md): ahí están los totales de las dos ejecuciones completas, la duración y el análisis de los errores encontrados.

| ID | Resultado obtenido (ejecución completa 2, 09/11/2026) | Estado |
|---|---|---|
| CY-01 | Los 5 roles inician sesión, llegan a `/dashboard` y ven solo su menú (`e2e-01`: 5/5 casos de rol) | Aprobado |
| CY-02 | Mensaje de error; sigue en `/login`; `/dashboard` → 302 | Aprobado |
| CY-03 | Requerimiento creado en Borrador y enviado («Enviado a RR. HH.») | Aprobado |
| CY-04 | Formulario vacío: no se crea registro. Ponderación del 10 %: observaciones visibles y «Publicar» deshabilitado | Aprobado |
| CY-05 | Vacante creada, publicada y visible en `/empleos`; el plazo objetivo editado persiste (`e2e-04` 2/2, `e2e-14` 4/4) | Aprobado |
| CY-06 | Postulación registrada con confirmación y notificación (`e2e-05` 1/1) | Aprobado |
| CY-07 | Preselección con historial y notificación; descarte sin motivo bloqueado (`e2e-06` 2/2) | Aprobado |
| CY-08 | Puntajes registrados dentro del rango (`e2e-07` 1/1) | Aprobado |
| CY-09 | Flujo integral de 12 pasos completo (`e2e-13` 12/12) | Aprobado |
| CY-10 | Sin acceso cruzado entre organizaciones (`e2e-11` 4/4) | Aprobado |
| CY-RPT-01 | 9 / 3 / 3 / 8 (88.9 %) / 1; barras y tabla coherentes | Aprobado |
| CY-RPT-02 | 3 postulaciones, 1 vacante, 3 finalistas, 1 fila | Aprobado |
| CY-RPT-03 | 2 postulaciones no seleccionadas | Aprobado |
| CY-RPT-04 | 0, «—», estado vacío; Limpiar → 9 | Aprobado |
| CY-RPT-05 | KPI 8 → 9 (100 %) tras preseleccionar desde la UI | Aprobado |
| CY-RPT-06 | B: 1 postulación, 1 vacante, selector con 1 opción propia | Aprobado |
| CY-RPT-07 | Redirige con «La vacante seleccionada no está disponible en su organización.»; datos de B | Aprobado |
| CY-RPT-08 | Sin menú; 403 para solicitante, evaluador y postulante | Aprobado |
| CY-RPT-09 | Aprobador ve 9; tabla visible; sin desbordamiento a 390 px | Aprobado |

Los otros specs de la suite (e2e-00, 03, 08, 09, 10, 12, 15 a 19) también aprobaron en la ejecución 2; ver el detalle por spec en `RESULTADOS_CYPRESS.md`. En la ejecución 1, ninguno de los escenarios de esta tabla falló: las 7 fallas fueron de e2e-16 y e2e-17 (DEF-14 y DEF-15).
