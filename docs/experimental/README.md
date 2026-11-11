# Rama experimental `exp/evidencias-ml02`: evidencias y ayuda documental ML-02

> **EXPERIMENTAL, local y con datos ficticios.**
>
> - **Qué no es.** No es la integración formal en el SaaS: EI-23 sigue BLOCKED y la integración exige la G0 real, un ADR de alcance y la decisión N5.
> - **Estados.** Ningún estado formal cambia: F36-SBX-GATE = NO SUPERADO, F37-SBX = BLOQUEADA, F36–F40 = BLOQUEADAS y datos reales = PROHIBIDOS.
> - **Bandera.** Todo responde 404 salvo con `EXPERIMENTAL_EVIDENCIAS=true` (`config/experimental.php`).
> - **Publicación.** Sin push, merge, tag ni release.

## 1. Qué hace

| Capacidad | Dónde | Avance técnico | Estado formal |
|---|---|---|---|
| Evidencias de una postulación: registrar, consultar, enlazar a un criterio de la misma vacante, revisar, corregir con una versión nueva y retirar | `/postulaciones/{id}/evidencias` | Tablas de solo inserción con triggers de PostgreSQL. Reglas R-01 a R-09 del flujo F37 (policy y form requests). Auditoría sin texto. Historial | F37-SBX BLOQUEADA; integración, EI-23 BLOCKED |
| Ayuda documental ML-02: fragmentos por criterio, con su fuente, y búsqueda exacta | Panel lateral de la misma página | BM25 léxico por postulación (`EXP-BM25-LEXICO-v1`), k = 3, con abstención. Sin entrenamiento | EI-09 CONDITIONAL (F36-M02); EI-07 ALLOWED solo tras el gate |
| Evaluación con el arnés F38 | `php artisan ml02:evaluar` | Preregistro antes de ejecutar; `test` abierto una vez | Ver [resultados](../academico/preparacion-f38-ml02/resultados-exp-bm25-v1/RESULTADOS.md) |

**Qué no hace:**

- no puntúa, ordena, compara, recomienda ni descarta personas;
- la evidencia no entra en el ranking (RF-21), en la decisión de Dirección (RF-23) ni en la tarjeta de ML-01;
- la página no muestra el nombre ni los datos de contacto del postulante.

## 2. Arranque (proyecto Docker propio)

Desde el worktree de esta rama. El `.env` local no se versiona y usa los puertos 8030 (app), 8031 (E2E), 5462 (PostgreSQL) y 6409 (Redis), con `EXPERIMENTAL_EVIDENCIAS=true`. El `.env.e2e` lleva la misma bandera.

```
docker compose -p experimental up -d --wait
docker compose -p experimental exec app php artisan db:seed --force
docker compose -p experimental exec app php artisan db:seed --class=ExperimentalEvidenceSeeder --force
```

- **`db:seed`** carga `DemoSeeder` sobre una base recién migrada.
- **`ExperimentalEvidenceSeeder`** añade cinco versiones de evidencias ficticias a POS-00003. Se niega a repetirse sobre los mismos datos.

La demo de la exposición (`entregaacad`) y el proyecto `continuacion` no se usan.

## 3. Recorrido de demostración

Usuarios de `docs/demo-users.md`, contraseña `password`.

1. **RR. HH. (`rrhh@andino.test`).**
   - Abra Vacantes, luego «Docente de Comunicación - Secundaria», sus postulaciones y POS-00003.
   - Pulse «Evidencias (experimental)».
2. **Evidencias.** Verá el aviso experimental y cuatro registros: un CV en versión 2, un certificado revisado y enlazado, y dos observaciones del evaluador.
3. **Versiones y permisos.**
   - En el CV, abra «Versiones anteriores (1)».
   - En una observación no aparece «Corregir»: solo la corrige su autor (CONT-M01).
4. **Ayuda documental.**
   - Con «Conocimientos pedagógicos», devuelve el certificado con las palabras resaltadas y su fuente.
   - Con «Clase modelo», devuelve la observación de la clase modelo. La de la «secuencia de actividades» es relevante pero no comparte palabras, y no aparece: es el fallo esperado del método léxico.
   - Con «Entrevista personal», se abstiene y lo explica.
5. **Registro con error.** Intente registrar un texto sin `[SINTÉTICO]`: aparece el error y no se guarda nada.
6. **Evaluador (`evaluador@andino.test`).**
   - Vaya a «Mis evaluaciones», abra la sesión y pulse «Evidencias (experimental)».
   - Solo puede registrar observaciones y no ve el historial.
7. **Dirección (`direccion@andino.test`).** Solo consulta y abre el «Historial», que lista identificadores, nunca el texto.
8. **Otra organización (`rrhh@demob.test`).** `/postulaciones/3/evidencias` responde 404.

## 4. Pruebas

| Prueba | Comando | Resultado |
|---|---|---|
| Escenarios F37 sobre los endpoints reales, flujo, triggers, auditoría, aislamiento y método | `php artisan test tests/Feature/Evidence tests/Unit/Ml02` | 57 passed |
| Ablaciones de las reglas, con restauración por `git checkout` | Ver el log de ablaciones | 9 de 9 detectadas, tras añadir 2 pruebas por 2 supervivientes |
| PHPUnit completo | `php artisan test` | 504 passed, 8 skipped (base `2b074e4`: 447 + 8) |
| Componentes (regresión completa) y tipos | `npx vp test --run` · `npx tsc --noEmit` | 62 passed (base 56 + 6 nuevas) · 0 errores |
| Cypress E2E-21 | `docker compose -p experimental --profile e2e run --name … cypress --spec cypress/e2e/e2e-21-evidencias-experimental.cy.js` | 7/7 sobre el código de `e3f80a1`, antes de acortar el título del panel y formatear (cambios sin `data-cy`). **No repetido sobre `400c55b`** |
| Cypress, regresión de la suite sobre `400c55b` con build nuevo | Una spec por contenedor con nombre | **Parcial: E2E-00 a E2E-09, 22/22.** Incluye E2E-06 y E2E-07, que visitan el expediente y la sesión modificados. El sistema detuvo la ejecución por falta de memoria (0,7 GB libres de 16) al empezar E2E-10: **E2E-10 a E2E-21 no se ejecutaron** |
| Arnés F38 con el método | `ml02:evaluar` y `f38_evaluar.py` | Ver resultados ML-02 |

Los logs completos están fuera de Git, en `experimental-20261110/evidencias/`, con SHA256SUMS.

## 5. Lo que falta para que deje de ser experimental

- **Formal.** La G0 real, un ADR de alcance, la decisión N5 de integración (EI-23) y F36-SBX-GATE SUPERADO con FG-03 que liste las EI. Ninguna es técnica.
- **Técnico.**
  - Pruebas manuales con lector de pantalla.
  - Un corpus de evaluación de tamaño real; el actual tiene 12 fragmentos.
  - Descriptores de criterio escritos por personas, si se quisiera mejorar el recall sin métodos semánticos.
- **Observación abierta.** Al reenviar el formulario GET de la ayuda desde una página que ya muestra resultados, Cypress vio el `select` deshabilitado en dos ejecuciones. La spec se ajustó para recargar la página, pero la causa no se identificó.
