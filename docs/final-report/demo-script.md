# Guion de demostración (8 a 12 minutos)

Todos los datos son ficticios (`docs/demo-users.md`). Contraseña de todos los usuarios demo: `password`.

## Preparación (antes de la exposición, fuera del tiempo)

```powershell
docker compose up -d --wait
docker compose exec app php artisan migrate:fresh --seed --force
curl http://localhost:8000/health
```

- Dejar abiertas cuatro ventanas privadas del navegador, una por usuario, para no cerrar sesión en cada paso: `rrhh@andino.test`, `direccion@andino.test`, `evaluador@andino.test` y `postulante5@correo.test`.
- Tener a mano el archivo ficticio `cypress/fixtures/cv-ficticio.pdf`, por si se muestra la postulación.
- **No ejecutar la suite Cypress durante la demostración.** No toca estos datos, pero tarda unos 3,5 min; se muestran sus resultados documentados.

## Guion

| # | Tiempo | Paso | Usuario | Qué mostrar | RF |
|---|---|---|---|---|---|
| 1 | 0:45 | **Login y roles** | `direccion@andino.test` | Inicio de sesión, menú propio del rol (Requerimientos, Vacantes, Auditoría) y aviso «la decisión final la registra una persona autorizada» | RF-08, roles |
| 2 | 0:45 | **Requerimiento** | `solicitante@andino.test` (opcional) o Dirección | Lista de requerimientos en cada estado (borrador, enviado, observado, validado, aprobado, rechazado) con su historial | RF-01, RF-02 |
| 3 | 0:45 | **Aprobación** | `direccion@andino.test` | Abrir «Docente de Matemática - Secundaria» (validado), aprobar con comentario y ver el historial actualizado | RF-03 |
| 4 | 1:00 | **Vacante** | `rrhh@andino.test` | Vacante en borrador «Docente de Inglés - Primaria»: perfil, criterios con ponderación y rango, suma 100 y validación; publicarla y verla en «Empleos publicados» | RF-05 a RF-07, RF-20 |
| 5 | 1:00 | **Postulación** | `postulante.nuevo@correo.test` | Perfil incompleto → completar datos y cargar CV → postular a «Docente de Comunicación - Secundaria» → código de seguimiento y notificación | RF-08 a RF-11 |
| 6 | 0:45 | **Evaluación** | `evaluador@andino.test` | «Mis evaluaciones» → sesión programada de Claudia Vilca → puntajes dentro del rango (un valor fuera de rango no se acepta) → registrar | RF-19, RF-20 |
| 7 | 0:30 | **Entrevista** | `rrhh@andino.test` | Expediente de un finalista de «Auxiliar de Educación Inicial»: evaluación y entrevista realizadas, con resultado «Recomendado» | RF-16 a RF-19 |
| 8 | 1:00 | **Ranking** | `rrhh@andino.test` | Comparación de «Auxiliar de Educación Inicial»: fórmula visible, desglose por criterio, totales 85.5 / 83.5 / 68.5, aviso «el ranking es un apoyo» y ausencia de panel de decisión para RR. HH. | RF-21, RF-22 |
| 9 | 1:15 | **Decisión humana** | `direccion@andino.test` | En la misma comparación, elegir a **Estela Ñahui (2.º lugar)**, escribir la justificación, marcar la confirmación y registrar. Resaltar: sin confirmación ni justificación no se registra, y los estados siguen en «Finalista» | RF-23 |
| 10 | 1:00 | **Selección y cierre** | `rrhh@andino.test` | «Registrar selección» → Estela queda «Seleccionado» → «Cerrar convocatoria» → los demás pasan a «No seleccionado» y aparece el resumen «Cerrada con selección» | RF-24, RF-25 |
| 11 | 0:30 | **Notificación** | `postulante5@correo.test` | Notificación «Resultado del proceso: seleccionado(a)», sin puntajes ni datos de otros candidatos | RF-26 |
| 12 | 0:45 | **Auditoría** | `direccion@andino.test` | «Auditoría»: decisión final, selección, cierre y notificación con actor, entidad y detalle legible; mencionar que es de solo inserción | RF-27 |
| 13 | 1:00 | **Evidencia técnica** | Terminal | `docker compose ps` (servicios *healthy*); resultados PHPUnit 244 (236 superadas, 0 fallidas) y Cypress 14 specs 43/43 en `docs/testing/cypress-e2e.md`; opcionalmente, ejecutar un spec corto: `npm run cy:run -- --spec "cypress/e2e/e2e-08-*.cy.js"` | Calidad |

**Duración estimada:** unos 11 minutos. Para ajustarse a 8 minutos, omitir los pasos 2, 5 y 7.

## Mensajes a remarcar

- **Paso 8:** «El sistema calcula y ordena, pero no elige».
- **Paso 9:** «La Dirección puede elegir a alguien que no es el primero y debe justificarlo».
- **Paso 12:** «Todo queda auditado y los registros no pueden alterarse».
- **Paso 13:** «Esto mismo se instala desde cero con Docker y está cubierto por pruebas automatizadas».

## Plan B

| Si… | Hacer |
|---|---|
| La aplicación no responde | `docker compose ps`, `curl http://localhost:8000/health` y `docker compose logs app` |
| Los datos quedaron modificados por un ensayo | `docker compose exec app php artisan migrate:fresh --seed --force` (unos segundos) |
| No hay tiempo para la postulación en vivo | Mostrar «Mis postulaciones» de `postulante5@correo.test` |
