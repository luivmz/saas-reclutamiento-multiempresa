# Checklist de definición de terminado

Recórrela antes de dar por cerrado cualquier cambio. Si una casilla no aplica, dilo explícitamente en el reporte en lugar de omitirla.

## Alcance y rama

- [ ] El cambio está dentro del alcance declarado de la fase actual (`docs/PROGRESS.md`, `docs/v1.1/`).
- [ ] La rama es `feature/*`, `fix/*`, `docs/*` o `chore/*`, creada desde `develop`.
- [ ] `git status --short` no muestra archivos ajenos al cambio.
- [ ] `git diff` no toca archivos fuera del alcance.

## Contratos

- [ ] RF-01 a RF-27 conservan número y significado.
- [ ] Ningún requerimiento nuevo aparece como aprobado: los nuevos son candidatos.
- [ ] No existe ninguna ruta por la que el sistema seleccione, descarte o contrate automáticamente.
- [ ] La decisión final sigue exigiendo Aprobador/Dirección, confirmación humana y justificación.
- [ ] Las entidades nuevas llevan `organization_id`, scope y Policy con rol + organización.
- [ ] Las acciones críticas nuevas quedan auditadas, sin datos sensibles en los metadatos.
- [ ] La auditoría sigue siendo de solo inserción.

## Pruebas ejecutadas de verdad

- [ ] Se observó el RED de las pruebas nuevas antes de implementar.
- [ ] Caso feliz, validación, autorización (403) y acceso desde otra organización cubiertos.
- [ ] `docker compose exec app php artisan test`: 0 fallidas. Anotar el total real.
- [ ] `docker compose exec app npm run build`: correcto.
- [ ] `docker compose exec app npx tsc --noEmit`: 0 errores.
- [ ] Si el cambio afecta un flujo cubierto por E2E: `npm run cy:run` sin fallos.
- [ ] Los números reportados provienen de ejecuciones reales de esta sesión.

## Datos y seguridad

- [ ] Sin PII real: usuarios, correos y CV son ficticios.
- [ ] Sin secretos en archivos versionados ni en la documentación.
- [ ] Sin dependencias de producción nuevas salvo autorización explícita.
- [ ] Sin cambios en configuración global, permisos ampliados ni hooks externos ejecutados.

## Documentación

- [ ] Trazabilidad actualizada (`traceability-master.md`, `rf-implementation-matrix.md`).
- [ ] Evidencia TDD registrada con resultados reales (`tdd-evidence.md`).
- [ ] Defectos reales registrados (`defects.md`), con severidad y corrección.
- [ ] Supuestos nuevos documentados (`assumptions.md`, A-37 en adelante).
- [ ] `docs/PROGRESS.md` refleja el estado y el siguiente paso.

## Entrega

- [ ] Commit descriptivo, con prefijo de tipo (`feat:`, `fix:`, `test:`, `docs:`, `chore:`).
- [ ] Sin `push`, `merge`, release ni tag salvo autorización explícita.
- [ ] El reporte final distingue lo verificado de lo pendiente y no afirma resultados no medidos.
