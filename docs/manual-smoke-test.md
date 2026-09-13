# Prueba de humo manual en navegador (Fase 8)

Validación real de la interfaz en un navegador. **No es la suite E2E de Cypress** (pendiente, fuera del alcance de la Fase 8): se usó Cypress solo como conductor del navegador para recorrer pantallas, ejecutar el flujo y capturar evidencia.

Fecha de ejecución: 2026-09-13 · Rama: `feature/frontend-integral` · Datos: `DemoSeeder` (ver `docs/demo-users.md`).

## Entorno

| Elemento | Valor |
|---|---|
| Aplicación | Docker Compose (`app` en `http://app:8000` dentro de la red `reclutamiento_default`, `http://localhost:8000` desde el host) |
| Navegador | Electron (Chromium) headless de la imagen `cypress/included:15.3.0` |
| Zona horaria del navegador | UTC (la del contenedor). Sirvió para detectar DEF-09. |
| `APP_TIMEZONE` | `America/Lima` |
| Resoluciones | Escritorio 1280×720, tableta 820×1180, móvil 390×844 |

Los scripts y capturas están en `storage/app/smoke/`, que Git ignora; no forman parte del repositorio. Comandos (PowerShell, desde la raíz del proyecto):

```powershell
docker compose exec app php artisan migrate:fresh --seed
docker run --rm --network reclutamiento_default -v "${PWD}/storage/app/smoke:/smoke" -w /smoke cypress/included:15.3.0 --config-file cypress.config.cjs --browser electron
docker run --rm --network reclutamiento_default -v "${PWD}/storage/app/smoke:/smoke" -w /smoke cypress/included:15.3.0 --config-file cypress.flow.config.cjs --browser electron
```

Nota: en PowerShell, `--config a=1,b=2` se interpreta como un arreglo y el ancho no se aplica. El viewport se fija en el archivo de configuración.

## 1. Recorrido visual por rol

Resultado: **10 casos, 10 pasaron, 49 capturas**. Sin errores HTTP ni excepciones JavaScript.

| Rol | Pantallas revisadas | Resultado |
|---|---|---|
| Invitado | Inicio, empleos, detalle de empleo, login, registro | OK |
| Área solicitante | Panel, lista con filtros por estado, crear, observado, corregir, rechazado | OK |
| RR. HH. | Panel, requerimientos, validación, vacantes, crear/editar vacante, vacante en borrador y publicada, postulaciones, expedientes (postulado, en evaluación, finalista), comparación pendiente y cerrada, notificaciones | OK |
| Aprobador / Dirección | Panel, decisión de requerimiento, comparación con panel de decisión, auditoría | OK (tras DEF-10) |
| Evaluador | Panel, mis evaluaciones, hoja de puntajes pendiente, entrevista realizada | OK |
| Postulante | Panel, perfil y CV, mis postulaciones, postulación seleccionada y finalista, convocatorias, notificaciones, empleo ya postulado | OK (tras DEF-09) |
| Postulante nuevo | Perfil incompleto, empleo con «Completar perfil» | OK |
| Móvil / tableta | Panel, expediente, comparación, auditoría, empleos | OK: la barra lateral pasa a menú y las tablas se desplazan horizontalmente dentro de su tarjeta |

## 2. Flujo integral por la interfaz

Resultado: **12 pasos, 12 pasaron** (45 s). Cada paso usa el rol real y los atributos `data-cy` estables.

| # | Paso | RF | Resultado |
|---|---|---|---|
| 01 | Solicitante registra «Docente de Ciencias - Flujo de validación» y lo envía a RR. HH. | RF-01 | OK |
| 02 | RR. HH. valida el requerimiento | RF-02 | OK |
| 03 | Dirección lo aprueba | RF-03 | OK |
| 04 | RR. HH. genera la vacante desde el requerimiento (ponderaciones 100), valida y publica | RF-05 a RF-07 | OK |
| 05 | Postulante nuevo completa su perfil, carga un CV PDF ficticio y postula | RF-08 a RF-11 | OK |
| 06 | RR. HH. preselecciona y programa evaluación y entrevista con el evaluador | RF-12 a RF-18 | OK |
| 07 | El evaluador registra puntajes de evaluación y entrevista con resultado | RF-19, RF-20 | OK |
| 08 | RR. HH. pasa la postulación a «Finalista» | RF-14 | OK |
| 09 | Dirección revisa el ranking y registra la decisión final con justificación y confirmación humana. Antes de esa acción no existe decisión. | RF-21 a RF-23 | OK |
| 10 | RR. HH. registra la selección y cierra la convocatoria («Cerrada con selección») | RF-24, RF-25 | OK |
| 11 | El postulante ve «Seleccionado» y la notificación de resultado | RF-26 | OK |
| 12 | Dirección ve en auditoría la decisión y el cierre | RF-27 | OK |

Verificaciones visuales del flujo:
- La hora de la evaluación (15/09 10:00) y la de la entrevista (16/09 09:30) coinciden en la notificación del servidor, la auditoría y la interfaz.
- El ranking muestra el aviso «El ranking es un apoyo para la decisión».
- Las notificaciones al postulante no exponen puntajes ni otros candidatos.

## 3. Defectos encontrados

| ID | Resumen | Estado |
|---|---|---|
| DEF-09 | Fechas en la zona horaria del navegador en lugar de `America/Lima` | Cerrado |
| DEF-10 | Auditoría con valores internos y fecha ISO en UTC | Cerrado |
| DEF-11 | Iniciales de avatar inválidas («C(») | Cerrado |

Detalle en `docs/defects.md`.

## 4. Observaciones no corregidas (sin impacto funcional)

- A 1280 px, la tabla «Mis evaluaciones» del evaluador necesita desplazamiento horizontal dentro de su tarjeta.
- En las capturas de página completa, la barra lateral y los *toasts* aparecen repetidos. Es un artefacto del cosido de capturas de Cypress, no de la aplicación.
- No se ejecutó una auditoría automática de accesibilidad (axe/Lighthouse). La revisión fue básica:
  - campos con `label`/`htmlFor`;
  - radios agrupados con `fieldset`/`legend`;
  - estados con texto y no solo color;
  - navegación por enlaces reales.
- No se revisó el modo oscuro.
