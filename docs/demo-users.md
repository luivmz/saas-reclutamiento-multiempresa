# Usuarios y escenarios de demostración

Todos los datos son **ficticios** (nombres, correos con dominios `.test`, teléfonos y CV de ejemplo). No corresponden a personas ni al personal real del Colegio Andino.

Carga: `docker compose exec app php artisan migrate:fresh --seed` (borra la base de desarrollo y ejecuta `Database\Seeders\DemoSeeder`).

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
