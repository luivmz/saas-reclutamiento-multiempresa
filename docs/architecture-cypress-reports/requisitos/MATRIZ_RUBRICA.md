# Matriz de rúbrica (20 puntos)

Mapeo de la sección VI de la guía principal con lo verificado por Codex el 09/11/2026. **Estimación conservadora, no nota docente ni certificación de producción.** Las evidencias originales se preservan y la entrega permanece local, sin commit.

| Indicador | Máximo | Evidencia auditada | Resultado | Estimación | Reserva o límite |
|---|---|---|---|---|---|
| Arquitectura de software | 4 | `arquitectura/ARQUITECTURA_SOFTWARE.md`, diagramas 01/06 históricos y 17 editable, revisión de rutas, Requests, Policies, servicios y modelos | Monolito modular, Inertia/React, PostgreSQL compartido y aislamiento lógico. RF-29 opcional y desactivado, sin afirmar integración ML activa | **3/4** | Se reserva un punto de forma conservadora por revisión humana en editor nativo del conjunto de diagramas y valoración docente de las integraciones. El diagrama 17 tiene XML válido y SVG/PNG revisados; no se inventa una demostración de ML en vivo |
| Arquitectura tecnológica | 3 | `ARQUITECTURA_TECNOLOGICA.md`, versiones reales, Compose, `/health`, `evidencias/arquitectura/ARQ-TECH-09_IDE_VSCode.jpg` | Stack y servicios contrastados; IDE real y entorno local documentados | **3/3** | No demuestra despliegue productivo ni CD; no se requiere inventarlos |
| Cypress | 5 | Configuración, 11 grupos con fichas, 21 specs; `evidencias/codex/cypress-final.log` y verificación de binario | **94/94, 0 fallidas, 0 omitidas, 100 %, 02:37**; Reportes 9/9; e2e-16 7/7 y e2e-17 8/8 sin eliminar aserciones importantes | **5/5** | La anomalía histórica de e2e-03 no se reprodujo; causa no demostrada. Capturas históricas de fallos perdidas, logs preservados |
| SonarQube | 4 | `sonarqube/RESULTADOS_SONARQUBE.md`, scanner/CE SUCCESS, API completa y siete capturas `SONAR-UI-*` | Gate **OK evaluado**, nueva cobertura **85,0 %**, global **70,3 %**, 0 Bugs/Vulnerabilities/Code Smells/Hotspots; V2 histórico separado | **4/4** | Sin LCOV frontend (0 % importado). Community Build tiene alcance de seguridad limitado y H2 es solo evaluación. El Gate no certifica ausencia de problemas |
| Reportes e impacto | 4 | Servicio, Request, Policy, página, 12 PHPUnit/209 aserciones, 6 Vitest, 9 Cypress; `MODULO_REPORTES.md` e `IMPACTO_FUNCIONAL.md` | 6 KPI, 2 gráficos y tabla desde PostgreSQL; filtros reales y aislamiento A/B probado; medido separado de potencial | **4/4** | La etapa no aplica al KPI de vacantes publicadas, por definición. AS-IS pendiente de validación; sin métricas institucionales de ahorro ni decisiones automáticas |
| **Total estimado** | **20** | 59 requisitos materiales de la guía con evidencia en la matriz | Cierre técnico del Markdown, sujeto a revisión humana | **19/20** | La calificación final pertenece al docente |

## Cierre de pendientes recibidos

| Pendiente recibido | Evidencia de cierre | Estado |
|---|---|---|
| Captura del IDE (ARQ-TECH-09) | `evidencias/arquitectura/ARQ-TECH-09_IDE_VSCode.jpg` | Cerrado |
| Proyecto y Quality Gate en UI (SONAR-05/08) | `SONAR-UI-01_Proyecto.jpg`, `SONAR-UI-02_Quality_Gate.jpg`, más Measures/Issues/Hotspots | Cerrado |
| Repetir regresiones y Sonar del working tree | `evidencias/codex/` y `AUDITORIA_CODEX.md` | Ejecutado y documentado |

## Pendientes humanos fuera de esta auditoría

1. Revisar y aprobar el diff; no se hizo staging ni publicación.
2. Revisar los `.drawio` en diagrams.net antes de incorporar los diagramas a la entrega formal.
3. Autorizar la generación de DOCX/PDF a partir del Markdown auditado.
4. Aceptar o planificar por separado la deuda histórica de PHPStan, Pint, formato y cobertura frontend. No se intentó sanearla masivamente.
