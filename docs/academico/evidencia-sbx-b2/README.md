# F35-SBX-B — B2: almacén efímero sintético

> **Estado: B2 = DISEÑADA / PENDIENTE DE AUDITORÍA DE DISEÑO.** Fecha: 11/10/2026. Rama `feature/f35-sbx-b2-ephemeral-store`, creada desde `develop` `72e86c5838984ea873d6dd56c179d94217b27317`.
>
> Punto de partida: B1 = CERRADA / CONGELADA / INTEGRADA.
>
> - Ancla auditada: `8e94a60274fe39ebda3e9961bc58036b389dfc00`.
> - Cierre: `3d9b78307684a0dfb093e31d28fde290b2b1cb4a` ([B1-FREEZE](../evidencia-sbx-b-freeze/F35SBXB_B1_Freeze.md)).
> - Integración: `develop` `72e86c5838984ea873d6dd56c179d94217b27317`, con CI 38179967121 en verde, y `main` `3fdfdcecdec47b08d99e96968dd915e0e1b9010b`, con CI 38180279164 en verde.

B2 es el incremento sucesor de B1. Diseña el almacén donde F35-SBX-B guardará los objetos de un run sintético: una base SQLite `:memory:` por organización sintética, con solo inserción y destrucción por cierre de la conexión. En esta sesión solo se diseña y se define cómo verificarlo.

| Documento | Contenido |
|---|---|
| [F35SBXB_B2_Diseno_Almacen.md](F35SBXB_B2_Diseno_Almacen.md) | Arquitectura, aislamiento por tenant, endurecimiento de SQLite, esquema mínimo, ciclo de vida, principal inmutable, eventos, purga, determinismo, restricciones de datos, RF-29, API interna, modelo de fallos y decisiones propuestas |
| [F35SBXB_B2_Contrato_Verificacion.md](F35SBXB_B2_Contrato_Verificacion.md) | Matriz de pruebas P01..P30 y contrato del gate sucesor de B2 |

## Qué no incluye este incremento

No existe todavía el almacén (`sbxb_store.py`), ni el runtime SQLite, ni pruebas ejecutables, ni el gate de B2. Tampoco pipeline, ML, dependencias nuevas ni cambios en el runtime, en la CI ni en el dataset.

## Gobierno

Este diseño no modifica `CLAUDE.md` ni `docs/PROGRESS.md`. Esos dos archivos forman parte del conjunto congelado de B1. Cambiarlos sin el gate de B2 dejaría HEAD sin ninguna comprobación ejecutable de la integridad de B1, y hoy el validador de B1-FREEZE la sigue acreditando sobre esta rama. Por eso todavía no registran el cierre de B1. Lo registrará el incremento que introduzca el gate de B2, con su regla de gobierno (DH-B2-07).

Los estados de gobierno no cambian:

- G0 real = NO APROBADA y ADR-005 = PROPUESTA;
- G0-SBX = APROBADA CON RESTRICCIONES;
- F35 productiva = BLOQUEADA y F36–F40 = BLOQUEADAS;
- Alcance C = BLOQUEADO y datos reales = PROHIBIDOS.

B2 no autoriza ML, scoring, recomendación ni selección automática, y no modifica RF-01..RF-27 ni RF-23. RF-29 sigue experimental y solo sobre el proceso.

## Próximo paso

Auditoría independiente del diseño. Después, y solo con autorización, el incremento de implementación: almacén, casos de prueba y gate sucesor, en ese orden de verificación.
