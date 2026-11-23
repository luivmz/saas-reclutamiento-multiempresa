# Usuarios y escenarios de demostración

Todos los datos son **ficticios** (nombres, correos con dominios `.test`, teléfonos y CV de ejemplo). No corresponden a personas ni al personal real del Colegio Andino.

En una base demo recién migrada, carga `docker compose exec app php artisan db:seed --class=DemoSeeder --force`. Usa el nombre del proyecto de tu entorno si corresponde. Consulta la [guía de entrega](entrega-final/ENTREGA_INTEGRADA.md) para las ofertas adicionales y la carga opcional de evidencias.

**Contraseña de todos los usuarios demo:** `password` (solo para desarrollo/demostración).

## Organización «Colegio Andino de Huancayo (Demo)»

| Rol | Nombre | Correo |
|---|---|---|
| Área solicitante | Carmen Rojas (demo) | `solicitante@andino.test` |
| Recursos Humanos | Luis Paredes (demo) | `rrhh@andino.test` |
| Aprobador / Dirección | Rosa Huamán (demo) | `direccion@andino.test` |
| Evaluador | Jorge Salazar (demo) | `evaluador@andino.test` |
| Evaluador | Elena Quispe (demo) | `evaluador2@andino.test` |

## Organización «Organización Demo B» (aislamiento multiempresa)

| Rol | Nombre | Correo |
|---|---|---|
| Área solicitante | Pedro Castro (demo B) | `solicitante@demob.test` |
| Recursos Humanos | Ana Torres (demo B) | `rrhh@demob.test` |
| Aprobador / Dirección | Mario Díaz (demo B) | `direccion@demob.test` |
| Evaluador | Sofía Ramos (demo B) | `evaluador@demob.test` |

## Postulantes (cuentas globales)

| Nombre | Correo | Perfil / CV |
|---|---|---|
| Andrea Poma (ficticia) | `postulante1@correo.test` | Completo, CV ficticio |
| Bruno Cárdenas (ficticio) | `postulante2@correo.test` | Completo, CV ficticio |
| Claudia Vilca (ficticia) | `postulante3@correo.test` | Completo, CV ficticio |
| Diego Mendoza (ficticio) | `postulante4@correo.test` | Completo, CV ficticio |
| Estela Ñahui (ficticia) | `postulante5@correo.test` | Completo, CV ficticio |
| Fabio Llanos (ficticio) | `postulante6@correo.test` | Completo, CV ficticio |
| Gabriela Nueva (ficticia) | `postulante.nuevo@correo.test` | Sin perfil ni CV (para completar y postular) |

## Escenarios cargados (Colegio Andino)

| Escenario | Datos | RF |
|---|---|---|
| Requerimientos en cada estado | Borrador (Educación Física), enviado (Arte), observado (Psicólogo/a Escolar), validado pendiente de Dirección (Matemática), rechazado (Asistente de Biblioteca), aprobado sin vacante (Religión) | RF-01 a RF-04 |
| Vacante en borrador válida | «Docente de Inglés - Primaria», lista para publicar | RF-05 a RF-07 |
| Vacante publicada con postulaciones | «Docente de Comunicación - Secundaria»: postulante1 postulado, postulante2 preseleccionado, postulante3 en evaluación con evaluación programada para `evaluador@andino.test` | RF-10 a RF-17, RF-19 |
| Ranking y decisión pendiente | «Auxiliar de Educación Inicial»: postulante4 (85.5), postulante5 (83.5) y postulante6 (68.5) finalistas con resultados completos | RF-20 a RF-23 |
| Proceso concluido | «Coordinador(a) de Tutoría»: decisión de Dirección, selección de postulante5, cierre; postulante6 y postulante1 no seleccionados; notificaciones de resultado y auditoría | RF-23 a RF-27 |
| Organización Demo B | «Asistente Administrativo (Demo B)» publicada con una postulación de postulante2 | Aislamiento |
| Riesgo operacional (ML-01, experimental) | «Docente de Ciencia y Tecnología - Secundaria»: proceso ficticio reproducido en el pasado. Se publicó hace 30 días, cerró postulaciones hace 10, sigue abierto y tiene un plazo objetivo a 30 días. Tiene postulaciones de postulante1, postulante3 y postulante6, con postulante1 preseleccionado y sin evaluaciones asignadas. Con el servicio ML levantado y `ML_SERVICE_ENABLED=true`, su panel muestra una estimación; sin el servicio, el modo descriptivo | RF-29 (candidato, experimental) |

## Ofertas adicionales para el listado público (opcional)

Diez ofertas ficticias más, para que `/empleos` tenga varias páginas y más tarjetas que explorar. No las carga `DemoSeeder` ni el entorno E2E: se añaden a mano, sobre una base ya sembrada con `DemoSeeder`.

```
docker compose exec app php artisan db:seed --class=DemoJobOffersSeeder --force
```

- **Idempotente:** la primera ejecución añade exactamente diez y las siguientes no añaden nada. Cada oferta lleva en su requerimiento la clave estable `clave demo-ofertas-NN`.
- **Flujo real:** cada oferta pasa por requerimiento aprobado, vacante con perfil y criterios (ponderaciones que suman 100) y publicación. Abre el día de la carga y cierra entre 30 y 45 días después.
- **Sin postulaciones:** no crea postulaciones, evaluaciones ni decisiones.
- **Códigos:** dependen de lo que ya existe, porque son secuenciales por organización y año. Sobre una base recién sembrada son `VAC-2026-0006` a `VAC-2026-0011` (Colegio Andino) y `VAC-2026-0002` a `VAC-2026-0005` (Demo B).

| Organización | Ofertas |
|---|---|
| Colegio Andino de Huancayo (Demo) | Docente de Matemática - Secundaria (2 plazas) · Docente de Inglés - Primaria · Docente de Educación Física · Psicólogo/a educativo/a · Bibliotecario/a escolar · Asistente de soporte informático |
| Organización Demo B | Analista de Recursos Humanos · Asistente de Contabilidad (2 plazas) · Coordinador/a de Operaciones · Técnico/a de Soporte TI |

«Docente de Inglés - Primaria» coincide en título con la vacante en borrador de `DemoSeeder` (RF-05 a RF-07). Son dos vacantes distintas: la nueva está publicada y tiene su propio código.
