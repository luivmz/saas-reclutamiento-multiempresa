---
name: project-guardian
description: Guardián del proyecto SaaS de reclutamiento. Úsala antes de planificar o editar cualquier cosa en este repositorio - código, pruebas, documentación, Docker o configuración - para verificar rama, alcance y contratos, y para saber qué pruebas y qué documentación exige el cambio. También cuando dudes si algo está permitido en la fase actual.
---

# Guardián del proyecto

Antes de escribir una línea, verifica que el cambio es legítimo, está en la rama correcta y no rompe un contrato. Este proyecto ya tiene una versión publicada y evaluada: el costo de romperla es mayor que el de ir despacio.

## 1. Leer antes de editar

No edites con supuestos. Lee lo que corresponda al cambio:

- `docs/PROGRESS.md`: en qué fase estamos y qué está permitido ahora.
- `docs/v1.1/scope-preliminary.md`: qué es candidato y qué está aprobado en v1.1.
- `docs/final-report/traceability-master.md`: qué RF toca el cambio y con qué código y pruebas está trazado.
- `docs/assumptions.md`: la regla de negocio probablemente ya está decidida ahí (A-01 a A-36).
- `docs/defects.md`: puede que el problema ya se haya visto y corregido antes.
- El código real del módulo afectado, no solo su documentación.

## 2. Validar antes de empezar

| Verificación | Cómo |
|---|---|
| Rama correcta | `git branch --show-current`. Nunca trabajes en `main` ni en `develop`; crea `feature/*`, `fix/*`, `docs/*` o `chore/*` desde `develop`. |
| Árbol limpio | `git status --short`. Si hay cambios ajenos sin commitear, detente y pregunta. |
| Alcance de la fase | Si el archivo que vas a tocar no está en el alcance declarado de la fase, detente. |
| Sincronía | La rama base debe estar al día con su remoto antes de ramificar. |

## 3. Contratos que el cambio no puede romper

1. **RF-01 a RF-27**: mismo número, mismo significado. Un requerimiento nuevo es RF-28 en adelante y empieza como **candidato**, no como aprobado.
2. **Nunca decisión automática**: ni selección, ni descarte, ni contratación. El ranking calcula, ordena y compara; la decisión la registra el Aprobador/Dirección con confirmación humana y justificación.
3. **Multiempresa**: toda entidad de negocio lleva `organization_id`, usa el scope global y su Policy compara rol **y** organización. Todo cambio de acceso necesita prueba cross-tenant.
4. **Auditoría**: `AuditLogger` para acciones críticas, sin datos sensibles, y la tabla sigue siendo de solo inserción.
5. **Datos**: solo ficticios. Ni PII real, ni CV reales, ni correos reales.
6. **Secretos**: jamás versionados. `.env` y `.env.e2e` quedan fuera de Git y de la imagen.
7. **Historia**: `v1.0.0-academic` no se mueve ni se reutiliza; la historia de v1.0 no se reescribe.

## 4. Pruebas proporcionales

El tamaño de la prueba lo fija el riesgo del cambio, pero el mínimo no es negociable:

- **Regla de negocio o flujo nuevo**: prueba Feature con RED observado antes de implementar, más el caso de autorización y el cross-tenant.
- **Cálculo puro**: prueba unitaria.
- **Cambio de interfaz**: mantener `data-cy` y, si afecta un flujo cubierto, actualizar el spec de Cypress.
- **Regresión obligatoria antes de cerrar**: `php artisan test` sin fallos, `npm run build` correcto y `npx tsc --noEmit` sin errores.
- **Nunca declares un resultado que no ejecutaste.** Si no corriste la suite, dilo.

## 5. Documentación que acompaña al cambio

Un cambio sin rastro documental está incompleto. Según el caso, actualiza `docs/final-report/traceability-master.md`, `docs/rf-implementation-matrix.md`, `docs/tdd-evidence.md` (RED/GREEN reales), `docs/defects.md` y `docs/PROGRESS.md`. Consulta la skill `academic-traceability`.

## 6. Cuándo detenerte y preguntar

Detente, muestra la evidencia y pide autorización si el cambio implica:

- operaciones destructivas: `git push --force`, rebase de historia publicada, borrar ramas o tags, `migrate:fresh` fuera del entorno E2E;
- `push`, `merge`, release o tag;
- tocar archivos fuera del alcance de la fase;
- agregar dependencias de producción, instalar skills globales o ejecutar hooks externos;
- ampliar permisos en `.claude/settings.local.json`;
- cualquier cosa que debilite un contrato de la sección 3.

## 7. Definición de terminado

La checklist completa está en [CHECKLIST.md](CHECKLIST.md). Resumen: el cambio está en su rama, tiene pruebas que pasaron de verdad, la regresión está verde, la documentación y la trazabilidad están actualizadas, no hay secretos ni datos reales, el diff no sale del alcance y nada se publicó sin autorización.
