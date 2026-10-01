# F29F — Ejecución QA final

Ejecución real de todas las suites del proyecto el 30/09/2026 sobre `develop` `bc44303`, con el árbol limpio al iniciar. La ejecución evalúa los criterios de aceptación CA-01 a CA-07 del [Plan de Pruebas](../plan-pruebas/README.md).

**Estado:** ejecutada en la fase F29F, **pendiente de auditoría**.

| Archivo | Contenido |
|---|---|
| [`F29F_Ejecucion_QA.md`](F29F_Ejecucion_QA.md) | Entorno, resultados por herramienta, CI, evaluación de los criterios de aceptación, observaciones clasificadas y matriz CP → resultado |
| [`evidencias/`](evidencias/) | Salida completa de cada herramienta: un `.log` por paso, con comando, horas y código de salida. Incluye además `phpunit-junit.xml`, `pytest-junit.xml`, `ci-github-actions.json` y `00-resumen.tsv` |

## Resultados

- **Suites:**
  - PHPUnit: 411 aprobadas, 8 omitidas, 0 fallidas y 1498 aserciones.
  - Cypress: 85/85 en 20 specs.
  - Vitest: 42/42.
  - pytest: 533/533.
- **Verificaciones estáticas:** TypeScript y build sin errores.
- **CI:** en verde en `develop`.
- **Deudas abiertas:**
  - **CI main F29C pendiente de ejecución manual** (OBS-F29F-04).
  - Formato pendiente de Pint y `vp check` (F25-L03, LOW).

Las cifras están en [`F29F_Ejecucion_QA.md`](F29F_Ejecucion_QA.md). No se usaron números históricos.

## Reproducción

Los comandos son los del [plan](../plan-pruebas/README.md): `docker compose exec app php artisan test`, `npx tsc --noEmit`, `npm run build`, `npx vp test --run`, `ml-service/.venv/Scripts/python.exe -m pytest` y `npm run cy:run`.

El documento se regenera con:

```
python docs/academico/tools/f27b/build.py f29f
```

**Saneamiento de los registros:** se quitaron los códigos de color y se reemplazaron el nombre del equipo y la ruta temporal. No contienen secretos.
