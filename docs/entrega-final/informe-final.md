# Informe final de la entrega académica

> Documento del 07/11/2026. Rama local `feature/entrega-academica-demo`, creada desde `2f6d0e0` (D-10 y D-11 en borrador), que desciende de RR-001 (`5036393`) y de `develop` `9dd76c4`. El hash del commit final se consulta en Git; este documento no lo anticipa.
>
> **Entrega local:** sin push, merge, tag ni release. Ningún gate cambia: F36-SBX = EN DISEÑO; F36-SBX-GATE = NO SUPERADO; F37-SBX = BLOQUEADA; F36–F40 = BLOQUEADAS; alcance C = BLOQUEADO; datos reales = PROHIBIDOS.

## 1. Qué es cada parte

| Parte | Clasificación | Qué se puede demostrar | Dónde |
|---|---|---|---|
| Recorrido RF-01 a RF-27: requerimiento, vacante, postulación, evaluación, ranking, decisión humana, selección, cierre, notificaciones y auditoría | **FUNCIONAL** | Todo, con datos ficticios y sus pruebas | [Guion](guion-demo.md), pasos 2 a 10 |
| Multiempresa y Policies | **FUNCIONAL** | Demo B no ve los datos del Colegio Andino (404) | Guion, paso 10 |
| ML-01, riesgo de demora del proceso (RF-29) | **EXPERIMENTAL** (candidato, no validado institucionalmente) | Una estimación en vivo desde FastAPI, con el *freeze* y el umbral congelados, y el respaldo sin servicio | Guion, paso 7 |
| Portada y panel de riesgo mejorados | **FUNCIONAL** (mantenimiento visual del producto, no F39-SBX) | Roles, límites, nota de ML-01 y la línea del modelo en el panel | Guion, pasos 1 y 7 |
| Asistencia a RR. HH. con rúbricas y observaciones | **FUNCIONAL** como flujo humano existente (RF-16 a RF-19) | La persona evaluadora registra puntajes por criterio y observaciones; el sistema calcula el ponderado | Guion, paso 5 |
| ML-02, ayudas sobre la evidencia (EI-01 a EI-07) | **PROTOTIPO DE DISEÑO**, estático, sin cálculo ni modelo, más un **plan** (PROPUESTA) | Pantallas navegables con ejemplos sintéticos escritos a mano | [`prototipo-ml02/`](../academico/f36-sbx/prototipo-ml02/README.md) |
| F37-SBX (implementar EI) y F38-SBX (investigación de ML-02 con datos) | **BLOQUEADAS** | Su preparación: S, plan y prototipo | [Expediente F36-SBX](../academico/f36-sbx/expediente-final/README.md) |
| F39-SBX (diseño visual con Higgsfield) | **BLOQUEADA** como fase. Las mejoras visuales se hicieron como mantenimiento ordinario del producto. **Higgsfield no está disponible en este entorno**: se usó la alternativa local (tipografía, color y CSS existentes, sin imágenes ni dependencias nuevas) | Las mejoras de la portada y del panel de riesgo | Guion, pasos 1 y 7 |
| F40-SBX (integración y demo) | **BLOQUEADA** como fase. La integración demostrable de esta entrega es el recorrido del producto, E2E-20 y este informe | El recorrido completo | [Guion](guion-demo.md) |
| F36-SBX: D-10, D-11, S del sucesor B-01, conclusiones y decisiones | **PREPARADO, PENDIENTE DE ACTOS DEL EQUIPO** | Borradores y la candidata a auditoría | [Expediente](../academico/f36-sbx/expediente-final/README.md) |

## 2. Cambios de esta entrega

| Área | Cambio | Archivos |
|---|---|---|
| Datos demo ([DEF-18](../defects.md)) | El escenario «Docente de Ciencia y Tecnología - Secundaria», reproducido en el pasado para que ML-01 tenga algo que estimar. Va al final del seeder, así que los identificadores de Cypress no cambian | `database/seeders/DemoSeeder.php`, `cypress/fixtures/demo.json` |
| Prueba (TDD) | RED: 2 failed, 1 passed. GREEN: 3 passed (19 assertions) | `tests/Feature/Ml/DemoSeederOperationalRiskScenarioTest.php` |
| Portada | Las secciones «Quién interviene», los límites del sistema y «Riesgo operacional del proceso (experimental)», con `data-cy` | `resources/js/pages/welcome.tsx` |
| Panel de riesgo | Con una estimación disponible, muestra la versión del modelo, el umbral y el *freeze* (`data-cy="operational-risk-model"`) | `resources/js/components/vacancies/operational-risk-card.tsx` |
| E2E | E2E-20, con 7 tests que siguen el guion. Simula la respuesta predictiva con `cy.intercept` | `cypress/e2e/e2e-20-recorrido-demo.cy.js` |
| Trazabilidad | DEF-18, evidencia TDD, la sección 10 de E2E y el escenario de demo | `docs/defects.md`, `docs/tdd-evidence.md`, `docs/testing/cypress-e2e.md`, `docs/demo-users.md` |
| F36-SBX | Expediente final y prototipo de ML-02 | `docs/academico/f36-sbx/expediente-final/`, `docs/academico/f36-sbx/prototipo-ml02/` |
| Entrega | Arranque, guion y este informe | `docs/entrega-final/` |

No cambian el contrato de RF-29 (features, modelo, umbral ni *freeze*), RF-23, las Policies, las migraciones, las dependencias, el gate, el validador, `CLAUDE.md`, `AGENTS.md` ni las skills.

## 3. Pruebas ejecutadas y sus resultados

Todas se ejecutaron el 07/11/2026 en un proyecto Docker aislado (`-p entregaacad`, puertos 8010, 8011, 5442 y 6389), desde el worktree de la rama. El proyecto habitual `reclutamiento` y sus volúmenes no se tocaron.

| Prueba | Antes de los cambios | Después |
|---|---|---|
| `php artisan test` | 444 passed, 8 skipped (2213 assertions) | **447 passed, 8 skipped (2233 assertions)**, 0 failed |
| `npx vp test --run` (componentes) | — | **42 passed (6 archivos)** |
| `npx tsc --noEmit` | — | **0 errores** |
| `npm run build` | — | **Correcto**. Chunk de la portada: 13.7 kB (4.8 kB gzip); sin imágenes, fuentes ni dependencias nuevas |
| `vp lint` y `vp fmt --check` (archivos TSX tocados) | — | 0 avisos, 0 errores; formato correcto |
| PHPStan (archivos PHP tocados) | — | **0 errores** |
| Pint (archivos PHP tocados) | — | La prueba nueva pasa. `DemoSeeder.php` tiene un aviso **preexistente** en código no tocado (`\App\Enums\ApplicationStatus` con nombre completo, línea 298), parte de la deuda conocida de Pint en la línea base |
| Cypress, suite completa | **85/85** (20 specs, 6:28) | Ver §3.1 |
| `pytest` de `ml-service` | — | **533 passed** |
| Reconstrucción del artefacto de ML-01 | — | *freeze* `9ee1843055e75d4039dd84fd666db7a594e1a45ec7e9b354820fabfcb21ebcd2`, umbral `0.1679418172266036`, 15 features, 3873 filas de entrenamiento, SHA-256 del binario `0899d3f6…c066` |
| ML-01 en vivo, Laravel ↔ FastAPI | Ninguna vacante demo en la ventana de consulta | Vacante 6: `predictive_available`, 13.1 %, `risk_flag = false`, HTTP 200 en 48 ms, `measures = proceso`, `decision_is_human = true`. Las vacantes 1 a 5 siguen en el modo descriptivo, que es su comportamiento correcto |
| Recorrido HTTP por rol, con inicio de sesión real | — | Todas las pantallas del guion responden 200 para su rol. RR. HH. recibe 403 en `/auditoria`, que es correcto. Demo B recibe 404 en la vacante 6 y en su riesgo |
| `validate_f36sbx.py` en esta rama | 55/4 | **55/4**, sin comprobaciones fallidas nuevas, y el resultado calculado sigue NO SUPERADO |
| Contraste del prototipo de ML-02 | — | Todas las parejas de color cumplen AA en tema claro y oscuro (mínimo 4.67:1, en el foco, que exige 3:1) |

### 3.1 Cypress, suite completa después de los cambios

**92/92: 21 specs, 0 failed, 0 pending, 0 skipped, 6:55** (Cypress 15.3.0 en el contenedor `cypress/included:15.3.0`, contra `app-e2e`, con ML desactivado como siempre en E2E).

- **Los 20 specs anteriores siguen en verde** (85 tests). E2E-13 recorre el flujo completo con un postulante nuevo, y E2E-11, la multiempresa.
- **E2E-20, nuevo, pasa sus 7 tests.**

**Incidencia de la ejecución.** Durante esta corrida, el sistema detuvo, por falta de memoria del equipo, el proceso de terminal que la había lanzado y el servicio ML-01 (uvicorn). El contenedor de Cypress siguió hasta terminar con código 0, y el resumen anterior es su salida completa. La verificación en vivo de ML-01 (§3) se había hecho antes de la detención. Para la exposición hay que volver a levantar el servicio ([arranque §3](README.md#3-arrancar-ml-01-rf-29-experimental-y-opcional)).

## 4. Accesibilidad, legibilidad y rendimiento

- **Medido automáticamente:**
  - en las secciones nuevas de la portada, contraste de al menos 4.5:1 en los dos temas, reflujo a 320 px y un único `h1` (E2E-20);
  - sin regresiones en E2E-16 a E2E-19: tabla en móvil, movimiento reducido, póster 3D en equipos modestos o con movimiento reducido, y QA visual.
- **Rendimiento:** solo se añadió texto. La escena 3D sigue en su propio fragmento diferido (E2E-18), y el panel de riesgo hace una sola petición, como antes.
- **Pendiente, como antes de esta entrega (V1 del roadmap):** las pruebas manuales con un lector de pantalla real y en un equipo modesto. Esta sesión no las hizo.

## 5. Lo que no se hizo, y por qué

| Pedido | Estado real | Motivo |
|---|---|---|
| Demo de F37-SBX dentro del SaaS | No implementada | F36-SBX-GATE = NO SUPERADO. EI-23 bloquea la UI productiva de estas capacidades, y el charter §1 solo autoriza el diseño |
| Prototipo y entrenamiento de ML-02 | Prototipo estático y plan; **sin entrenamiento** | EI-22 (entrenar con evidencia) está BLOCKED en este ciclo |
| Recursos de Higgsfield | No usados | No hay acceso en este entorno. Se usó la alternativa local |
| Decisiones D-10, D-11, D-02b, FG-02, FG-03, FG-10 y FG-12 | Preparadas, no emitidas | Son actos de los tres integrantes. No se atribuyen votos ni delegaciones |
| Sincronizar `CLAUDE.md`, `PROGRESS.md`, `README.md` y `ACADEMIC_BASELINE.md` | No hecho | Son archivos de gobierno que la regla GOV vigila. Necesitan su propio incremento autorizado (deuda de la reconciliación §7) |

## 6. Para la revisión final de Codex

Se audita la rama completa frente a `2f6d0e0`. Lo central:

1. DEF-18: que el escenario no cambia el contrato de RF-29 ni los identificadores de Cypress, y que no asigna evaluaciones.
2. La portada y el panel: los textos no prometen nada que el producto no haga, y la línea del modelo no habla de personas.
3. E2E-20.
4. El expediente F36-SBX: D-10, D-11, S, las conclusiones y las decisiones propuestas, sin actos ni gates simulados.
5. El prototipo de ML-02: estático, sin EI implementadas.
