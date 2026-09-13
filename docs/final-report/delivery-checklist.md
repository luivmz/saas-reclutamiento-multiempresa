# Checklist de entrega

Verificado en el QA final (Fase 12, 2026-09-13, rama `release/qa-final`). Detalle y evidencia en [qa-final-report.md](qa-final-report.md).

## Código

- [x] RF-01 a RF-27 implementados (27/27, sin RF adicionales) — [traceability-master.md](traceability-master.md)
- [x] PHPUnit: 244 pruebas · 236 superadas · **0 fallidas** · 8 omitidas · 1074 aserciones
- [x] Cypress: 14 specs · 43/43 · **0 fallidos** (entorno E2E aislado)
- [x] `npm run build` correcto
- [x] `npx tsc --noEmit` sin errores
- [x] Regla crítica: el ranking no selecciona; decide el Aprobador/Dirección (código, pruebas, interfaz y documentación coinciden)

## Seguridad

- [x] `.env` y `.env.e2e` no versionados (ignorados por Git y excluidos de la imagen)
- [x] Sin secretos, logs, *dumps*, *backups* ni CV privados en archivos versionados
- [x] `.env.example` y `.env.e2e.example` sin secretos reales
- [x] Multiempresa verificada (PHPUnit *cross-tenant* + E2E-11); RLS no implementado y no declarado
- [x] Autorización por rol verificada (403 en accesos prohibidos: PHPUnit + E2E-12)
- [x] Auditoría de solo inserción y aislada por organización
- [x] Endpoints E2E inertes en el entorno normal (404) y protegidos por token en E2E (403 sin token)

## Docker

- [x] Instalación reproducible desde cero validada (Fase 10, clon limpio)
- [x] *Healthchecks*: `app`, `queue`, `postgres`, `redis`, `app-e2e` y `queue-e2e` *healthy*
- [x] Migraciones: 17 aplicadas, 0 pendientes (normal y E2E)
- [x] *Seed* reproducible con datos ficticios (el reset E2E ejecuta `migrate:fresh --seed` en cada spec)
- [x] Entorno E2E aislado (`reclutamiento_e2e`, Redis DB 2/3)

## Documentación

- [x] 14 capítulos en `docs/final-report/`
- [x] README (instalación, Docker, usuarios demo, pruebas, documentación)
- [x] Guía Docker (`docs/docker.md`)
- [x] Documentación Cypress (`docs/testing/cypress-e2e.md`)
- [x] Matriz maestra de trazabilidad
- [x] Índice de evidencias
- [x] Informes escritos de diagramas (`docs/final-report/diagram-reports/`, 01 a 09)
- [x] Resumen técnico y guion de demostración
- [x] Referencias con fecha de consulta

## Académico

- [x] NRC 28607 (sin otros NRC en la documentación vigente)
- [x] Docente: Dr. Maglioni Arana Caparachin
- [x] Integrantes: Coronacion Meza Fredy · Peña Arroyo Anthony · Vila Meza Luis Antonio
- [x] AS-IS rotulado como preliminar y pendiente de validación
- [x] TO-BE rotulado como propuesto
- [x] Decisión final humana explícita en toda la documentación
- [ ] BPMN AS-IS y TO-BE originales anexados (**pendiente del equipo**; no están en el repositorio)
- [ ] Capturas de pantalla seleccionadas para el informe (**pendiente del equipo**; lista recomendada en el informe QA)

## Publicación

- [ ] GitHub publicado
