# Diagramas utilizados en la práctica

Se **reutilizan** los diagramas editables existentes de `docs/metologia/diagramas/`, que representan la implementación real verificada en archivos. No se duplican. Solo se agrega una vista de componentes para el módulo nuevo de reportes, porque ningún diagrama previo podía representarlo: el `06` lo excluye expresamente.

Las rutas son relativas a la raíz del repositorio. Los SVG/PNG de `docs/metologia/diagramas/exportados/` son vistas auxiliares generadas localmente desde la misma geometría que el `.drawio`, no exportaciones nativas de diagrams.net (ver [`REPORTE_DIAGRAMAS_DRAWIO.md`](../../metologia/diagramas/REPORTE_DIAGRAMAS_DRAWIO.md)).

## Arquitectura de software (Actividad 1.2)

| Diagrama | Página | Editable | Vista SVG / PNG | Qué cubre de la guía |
|---|---|---|---|---|
| `01_ARQUITECTURA_GENERAL_SAAS` | 01 «Arquitectura y multitenencia» | `docs/metologia/diagramas/fuentes/01_ARQUITECTURA_GENERAL_SAAS.drawio` | `docs/metologia/diagramas/exportados/01_ARQUITECTURA_GENERAL_SAAS_p01.svg` · `…_p01.png` | Interfaz de usuario (React + TS), backend (Inertia, Laravel, Policies, servicios), base de datos (PostgreSQL), Redis y cola, aislamiento por `organization_id`, servicio externo opcional (FastAPI RF-29) y comunicación entre ellos |
| `06_MAPA_MODULOS_SAAS` | 01 «Flujo y capacidades transversales» | `docs/metologia/diagramas/fuentes/06_MAPA_MODULOS_SAAS.drawio` | `docs/metologia/diagramas/exportados/06_MAPA_MODULOS_SAAS_p01.svg` · `…_p01.png` | Módulos principales RF-01 a RF-27 y su secuencia; decisión humana; capacidades transversales |
| **`17_MODULO_REPORTES_COMPONENTES` (nuevo)** | 01 «Componentes y flujo» | [`diagramas/17_MODULO_REPORTES_COMPONENTES.drawio`](diagramas/17_MODULO_REPORTES_COMPONENTES.drawio) | [`diagramas/17_MODULO_REPORTES_COMPONENTES.svg`](diagramas/17_MODULO_REPORTES_COMPONENTES.svg) · [`.png`](diagramas/17_MODULO_REPORTES_COMPONENTES.png) | Módulo de reportes: página React, ruta, Form Request, Policy/Gate, controlador, servicio, tablas leídas y salida solo agregada |

**Vigencia del `06`.** Su subtítulo, «Sin banco de talentos, planillas, contratación o reportes BI implementados», es una fotografía del 03/11/2026 y era cierto entonces. Desde esta práctica existe un módulo de reportes **operativos internos** (RF-28 candidato), que sigue sin ser BI externo. No se editó el `06` por dos razones: sus hashes están registrados en [`MANIFIESTO_DIAGRAMAS.json`](../../metologia/diagramas/documentacion/MANIFIESTO_DIAGRAMAS.json) y sus vistas PNG/SVG salieron de un pipeline local que no está versionado. Modificar el `.drawio` habría roto el manifiesto y desalineado sus vistas. La nota de vigencia queda aquí, y el diagrama `17` cubre el módulo nuevo.

**Cómo se generó el `17`.** Lo produjo un script local a partir de una única definición de nodos y aristas: un `.drawio` con objetos nativos editables (cajas, cilindro, nota, conectores ortogonales y metadatos `sourceRef`/`evidenceState`), un SVG y un PNG renderizado con Chrome headless. Se validó que el XML esté bien formado y se revisó visualmente el PNG para descartar cruces de conectores con textos. La apertura en diagrams.net queda pendiente de revisión humana, igual que en los diagramas 01–16.

## Arquitectura tecnológica (Actividad 2.2)

| Diagrama | Páginas | Qué cubre | Uso en la práctica |
|---|---|---|---|
| `02_DESPLIEGUE_DOCKER` | 01 «Servicios base y Sonar separado», 02 «Volúmenes y montajes», 03 «Perfil E2E opcional» | Host macOS Apple Silicon, Docker Desktop, servicios `app`/`queue`/`postgres`/`redis` con versiones y puertos, SonarQube separado y perfil E2E con Cypress | **Diagrama principal** de arquitectura tecnológica e infraestructura |
| `11_ESTRATEGIA_PRUEBAS_CALIDAD` | 01 «Herramientas y ciclo» | PHPUnit, Vitest, Cypress, SonarQube y ciclo de calidad | Herramientas de automatización y análisis de calidad. Su texto dice «Cypress NO EJECUTADO en sesión Sonar» (fotografía del 20/10); en esta práctica Cypress **sí** se ejecutó, ver [`../cypress/RESULTADOS_CYPRESS.md`](../cypress/RESULTADOS_CYPRESS.md) |
| `16_FLUJO_GIT_DESARROLLO` | 01 «Estrategia documentada», 02 «Historial y referencias observadas» | Git, GitHub, ramas `main`/`develop`/`chore/*`, CI | Control de versiones y proceso de actualización |
| `01_ARQUITECTURA_GENERAL_SAAS` | 01 | Frontend/backend/BD | Tecnologías de frontend y backend en contexto |

Entre los cuatro cubren lo que pide la guía en 2.2: herramientas de desarrollo, frontend y backend, SGBD, infraestructura de alojamiento (Docker local), control de versiones, automatización y calidad. Por eso no se dibujó un diagrama tecnológico nuevo.

## Diagramas de resultados de calidad (contexto)

`12_MEJORA_SONARQUBE_V1_V2` documenta las mediciones históricas V1 y V2. Las mediciones nuevas de esta práctica (V3) se registran en [`../sonarqube/RESULTADOS_SONARQUBE.md`](../sonarqube/RESULTADOS_SONARQUBE.md) **sin sobrescribir** el histórico.
