# Guion de exposición — SaaS Reclutamiento Multiempresa

> **Rama de continuación** (`feature/continuacion-f36-f40`, 08/11/2026): el paso 7 empieza por el **cronograma del proceso**. Esta rama se ensaya en su propio proyecto Docker, `continuacion` (app en `http://localhost:8020`): con los mismos comandos, cambiando `-p entregaacad` por `-p continuacion`. La exposición auditada sigue siendo la de `feature/entrega-academica-demo` (`f5003c9`), en `entregaacad`, sin cronograma.

Duración: unos 20 minutos, más preguntas. Antes de empezar:

- el proyecto aislado `entregaacad` arrancado ([arranque §3](README.md#3-arrancar-el-saas-y-cargar-los-datos-ficticios)), con la app en `http://localhost:8010`. Las rutas de la tabla son relativas a esa dirección;
- los datos ficticios recién cargados con `docker compose -p entregaacad exec app php artisan migrate:fresh --seed --force`, que solo reinicia la base de `entregaacad`;
- ML-01 levantado ([arranque §4](README.md#4-arrancar-ml-01-rf-29-experimental-y-opcional));
- una ventana privada por rol, o cerrar sesión entre pasos.

Contraseña de todas las cuentas: `password`. Todos los datos son ficticios.

El spec `cypress/e2e/e2e-20-recorrido-demo.cy.js` recorre los pasos 1, 6, 7, 8 y 9 sobre los mismos datos. En la rama de continuación comprueba además el cronograma: hitos, hito en curso, contraste en tema claro y oscuro, y 320 px. Si pasa, el guion se puede seguir.

| # | Min | Quién (cuenta) | Dónde | Qué se muestra | Mensaje |
|---|---|---|---|---|---|
| 0 | 1 | — | Diapositiva o README | El caso: Colegio Andino, SaaS multiempresa, RF-01 a RF-27. Stack Laravel + React, PostgreSQL y Docker | «Todo el proceso, con nombre y fecha en cada paso» |
| 1 | 1 | Visitante | `/` | Portada: el expediente con profundidad CSS (decorativa), cómo avanza un proceso, quién interviene, límites y la nota de ML-01 | «El sistema no selecciona por nadie» |
| 2 | 2 | Dirección (`direccion@andino.test`) | `/requerimientos/4` | «Docente de Matemática - Secundaria», validado por RR. HH. y pendiente de Dirección: se aprueba | RF-01 a RF-04: flujo de aprobación con historia |
| 3 | 2 | RR. HH. (`rrhh@andino.test`) | `/vacantes/1` | Vacante en borrador: perfil, criterios y ponderaciones (40/30/30). Se publica | RF-05 a RF-07: no se publica sin criterios ni con el plazo vencido |
| 4 | 2 | Postulante (`postulante1@correo.test`) | `/empleos` y `/mis-postulaciones` | Vista pública y estado de sus postulaciones | RF-08 a RF-12: el postulante ve su estado, no el expediente interno (DEF-14) |
| 5 | 2 | Evaluación (`evaluador@andino.test`) | `/mis-evaluaciones` | Evaluación programada de «Claudia Vilca (ficticia)»: se registran puntajes por criterio y una observación | RF-16 a RF-19: solo lo asignado. La rúbrica la aplica una persona |
| 6 | 2 | RR. HH. | `/vacantes/3/comparacion` | Ranking de tres finalistas (85.5, 83.5 y 68.5), con el desglose ponderado de cada puntaje | RF-20 a RF-22: calcula, ordena y compara; no decide |
| 7 | 4 | RR. HH. | `/vacantes/6` | «Docente de Ciencia y Tecnología - Secundaria». Arriba, el **cronograma del proceso**: publicación y cierre de postulaciones completados, el plazo objetivo como hito en curso («Faltan 30 días») y el avance «Día 30 de 60». Son fechas registradas, sin estimaciones. A la derecha, el panel de **riesgo operacional (experimental)**. Con el servicio activo muestra una estimación (13.1 % en la verificación del 07/11/2026, por debajo del umbral), el umbral, la versión del modelo y el *freeze*. Para enseñar el respaldo, se detiene uvicorn (Ctrl+C) y se recarga la página: el panel dice «Servicio no disponible», sin cifra, y el resto de la vacante funciona igual. Para volver, se arranca uvicorn otra vez | ML-01 mide el **proceso**, no a las personas; es opcional y no toca el ranking ni la decisión |
| 8 | 3 | Dirección | `/vacantes/3/comparacion` | Se elige a la **segunda** del ranking, se escribe la justificación y se marca la confirmación humana. Los estados de las postulaciones no cambian solos | RF-23: la decisión es humana, justificada y no automática |
| 9 | 1 | Dirección | `/auditoria` | La primera fila es `seleccion.decision_registrada`. La tabla es de solo inserción (trigger `audit_logs_append_only`) | RF-27: trazabilidad sin PII en los metadatos (DEF-17) |
| 10 | 1 | RR. HH. Demo B (`rrhh@demob.test`) | `/vacantes` | Solo ve «Asistente Administrativo (Demo B)» | Multiempresa: `organization_id`, Policies y pruebas cross-tenant |
| 11 | 2 | — | `docs/academico/f36-sbx/prototipo-ml02/index.html` | Prototipo **estático** de ML-02: organización de evidencia, alertas del proceso, trazabilidad, desglose sin totales, guardia de PII y búsqueda léxica | Diseño, no implementación: F37-SBX está BLOQUEADA y el gate, NO SUPERADO |
| 12 | 1 | — | [`informe-final.md`](informe-final.md) | Pruebas y su resultado; qué es funcional, qué es experimental y qué es prototipo | Calidad demostrada con pruebas que se ejecutaron de verdad |

## Variantes

- **Sin ML-01:** el paso 7 muestra el modo sin estimación. Se explica que es el comportamiento previsto (E2E-15).
- **Con poco tiempo:** los pasos 1, 6, 7, 8 y 9 cubren el mensaje central.
- **Repetir la decisión:** volver a cargar los datos ficticios con `docker compose -p entregaacad exec app php artisan migrate:fresh --seed --force`, que solo reinicia la base de `entregaacad`.

## Preguntas previsibles

| Pregunta | Respuesta corta |
|---|---|
| ¿La IA elige al candidato? | No. Ni el ranking ni ML-01 deciden: decide Dirección con justificación (RF-23) |
| ¿Qué predice el modelo? | El riesgo de que el **proceso** no cierre a tiempo. Está entrenado solo con datos sintéticos, con *freeze* y umbral congelados. No está validado institucionalmente |
| ¿Por qué ML-02 no está implementado? | Su gate (F36-SBX-GATE) no está superado. Además, entrenarlo con evidencia está bloqueado (EI-22). Se entrega el diseño y el plan |
| ¿Hay datos reales? | No. Todo es ficticio o sintético |
