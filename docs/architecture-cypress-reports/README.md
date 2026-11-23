# Práctica individual: arquitectura, Cypress, SonarQube y reportes

**Asignatura:** Pruebas y Calidad de Software · **Modalidad:** individual · **Estudiante:** Luis Antonio Vila Meza
**Proyecto:** SaaS Multiempresa para Reclutamiento, Evaluación y Selección de Personal
**Rama:** `chore/sonarqube-macos-setup` · **Base:** `41a830c` · **Estado:** implementado y validado en el working tree, **sin commit**, pendiente de auditoría humana (09/11/2026).


> **Entrega integrada.** El encabezado documenta la práctica al 09/11/2026. El commit `5e2eae3` publicó ese trabajo. La suite integrada usa E2E-25 para Reportes. Las pruebas de la práctica y sus capturas conservan E2E-20 como identificador histórico. Consulta la [guía de entrega](../entrega-final/ENTREGA_INTEGRADA.md).

## Objetivo

Aplicar sobre el proyecto existente (no uno nuevo) la *Guía Práctica INDIVIDUAL de Arquitectura*: documentar la arquitectura de software y la tecnológica, integrar y ejecutar Cypress y SonarQube, implementar un módulo de reportes con datos reales, analizar su impacto funcional y entregar un informe técnico individual con evidencias.

## Guías utilizadas

Están en esta carpeta, sin moverlas ni modificarlas (la carpeta `plantillas/` sugerida no existía; se respetó la ubicación original):

- `Guía Práctica INDIVIDUAL de Arquitectura.docx`: **requisito principal**, convertido en [`requisitos/MATRIZ_REQUISITOS.md`](requisitos/MATRIZ_REQUISITOS.md) y [`requisitos/MATRIZ_RUBRICA.md`](requisitos/MATRIZ_RUBRICA.md).
- `Guia desarrollo de pruebas blanca y negra.pdf`: **referencia** conceptual de caja negra y caja blanca (PDF escaneado de 39 páginas, leído como imágenes). No se copió su contenido; ver [`cypress/CAJA_NEGRA_BLANCA.md`](cypress/CAJA_NEGRA_BLANCA.md).

## Estructura

| Carpeta | Contenido |
|---|---|
| [`requisitos/`](requisitos/) | Matriz de requisitos de la guía y matriz de rúbrica (20 pts) |
| [`arquitectura/`](arquitectura/) | [Arquitectura de software](arquitectura/ARQUITECTURA_SOFTWARE.md), [arquitectura tecnológica, entorno y despliegue](arquitectura/ARQUITECTURA_TECNOLOGICA.md), [diagramas usados](arquitectura/DIAGRAMAS_REFERENCIA.md) y el diagrama nuevo `diagramas/17_MODULO_REPORTES_COMPONENTES.*` |
| [`cypress/`](cypress/) | [Escenarios](cypress/ESCENARIOS_CYPRESS.md), [resultados](cypress/RESULTADOS_CYPRESS.md) y [caja negra/blanca](cypress/CAJA_NEGRA_BLANCA.md) |
| [`sonarqube/`](sonarqube/) | [Resultados del análisis V3](sonarqube/RESULTADOS_SONARQUBE.md), comparados con V1/V2 sin sobrescribirlos |
| [`reportes/`](reportes/) | [Módulo de reportes](reportes/MODULO_REPORTES.md) e [impacto funcional](reportes/IMPACTO_FUNCIONAL.md) |
| [`evidencias/`](evidencias/) | Logs, JSON de la API de Sonar y capturas reales; índice en [`EVIDENCIAS_MANIFEST.md`](evidencias/EVIDENCIAS_MANIFEST.md) |
| [`final-report/`](final-report/) | [`INFORME_TECNICO_INDIVIDUAL.md`](final-report/INFORME_TECNICO_INDIVIDUAL.md), el artefacto fuente del informe |

## Cómo ejecutar Cypress

```sh
open -a Docker
docker compose up -d --wait            # entorno normal (necesario: app-e2e reutiliza sus volúmenes)
npm run cy:run                         # genera .env.e2e (no versionado), levanta app-e2e y corre la suite
npm run cy:run -- --spec cypress/e2e/e2e-25-reports.cy.js
```

La suite reinicia **solo** la base `reclutamiento_e2e`; la base demo `reclutamiento` no se toca (DEF-13).

## Cómo ejecutar SonarQube

Resumen; el procedimiento completo está en [`docs/sonarqube/README.md`](../sonarqube/README.md):

```sh
docker start sonarqube && curl -fsS http://localhost:9000/api/system/status      # esperar "UP"
docker compose exec -T app php -d pcov.enabled=1 vendor/bin/phpunit --coverage-clover coverage.xml --colors=never
# normalizar rutas de coverage.xml (comando documentado en docs/sonarqube/README.md)
export SONAR_HOST_URL=http://localhost:9000
export SONAR_TOKEN="$(< storage/app/private/.sonar-token)"   # archivo local ignorado por Git; nunca imprimir
sonar-scanner && unset SONAR_TOKEN
```

## Cómo abrir Reportes

1. `docker compose up -d --wait` y abrir `http://localhost:8000/login`.
2. Iniciar sesión como RR. HH. (`rrhh@andino.test`) o Dirección (`direccion@andino.test`); la contraseña demo está en [`docs/demo-users.md`](../demo-users.md).
3. Menú lateral → **Reportes** (`/reportes`). Filtros: Desde, Hasta, Vacante y Etapa actual.

## Dónde están las evidencias y el informe

- Evidencias: [`evidencias/EVIDENCIAS_MANIFEST.md`](evidencias/EVIDENCIAS_MANIFEST.md).
- Informe: [`final-report/INFORME_TECNICO_INDIVIDUAL.md`](final-report/INFORME_TECNICO_INDIVIDUAL.md).
- Registro de fase: entrada «Práctica individual de arquitectura» en [`docs/PROGRESS.md`](../PROGRESS.md).

## Auditoría independiente Codex

Resultado técnico y alcance: [`AUDITORIA_CODEX.md`](AUDITORIA_CODEX.md). Regresión final repetida: **426 PHPUnit + 8 skipped, 1715 aserciones; 54 Vitest; TypeScript sin errores; build correcto; 94/94 Cypress (21 specs, 02:37)**. Sonar V3 reejecutado: Gate OK, New Coverage 85,0 %, cobertura global 70,3 %, 0 Issues y `ignoredConditions=false`.

Se cerraron las evidencias de IDE y Sonar UI. La matriz contiene **59** requisitos, no 52; 59 cuentan con evidencia material para el cierre Markdown. Se corrigieron solo anotaciones PHPDoc nuevas del servicio de Reportes; permanecen las deudas históricas de PHPStan/Pint/formato y la falta de LCOV frontend. Sin staging ni publicación. DOCX/PDF se generan únicamente después de revisión humana.
