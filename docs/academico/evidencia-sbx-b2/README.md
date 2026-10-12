# F35-SBX-B — B2: almacén efímero sintético

> **Estado: B2 = DISEÑADA / CORREGIDA / PENDIENTE DE REAUDITORÍA FINAL FOCAL.** Fecha: 11/10/2026. Rama `feature/f35-sbx-b2-ephemeral-store`, creada desde `develop` `72e86c5838984ea873d6dd56c179d94217b27317`.
>
> - **Versión 1 del diseño** (`ae25e8c60c538ce2336fadd98489de8eee9e0983`): veredicto «B2-DESIGN APROBADO CON CORRECCIONES PREVIAS», sin hallazgos BLOCKER ni HIGH.
> - **Versión 2** (`eaac2120ede71289cd282a283baf6cc8698ca87b`): resuelve sus cinco MEDIUM (B2-M01..B2-M05) y fija las decisiones Q1–Q9. La reauditoría dio M01–M04 por resueltos y M05 como parcialmente resuelto.
> - **Versión 2.1**: completa M05 y Q1 con una transición de gobierno única y monotónica.
>
> Punto de partida: B1 = CERRADA / CONGELADA / INTEGRADA.
>
> - Ancla auditada: `8e94a60274fe39ebda3e9961bc58036b389dfc00`.
> - Cierre: `3d9b78307684a0dfb093e31d28fde290b2b1cb4a` ([B1-FREEZE](../evidencia-sbx-b-freeze/F35SBXB_B1_Freeze.md)).
> - Integración: `develop` `72e86c5838984ea873d6dd56c179d94217b27317`, con CI 38179967121 en verde, y `main` `3fdfdcecdec47b08d99e96968dd915e0e1b9010b`, con CI 38180279164 en verde.

B2 es el incremento sucesor de B1. Diseña el almacén donde F35-SBX-B guardará los objetos de un run sintético: una base SQLite `:memory:` por organización sintética y escenario, que solo admite inserciones de contenido F34 autorizado y se destruye cerrando la conexión. En esta fase solo se diseña y se define cómo verificarlo.

| Documento | Contenido |
|---|---|
| [F35SBXB_B2_Diseno_Almacen.md](F35SBXB_B2_Diseno_Almacen.md) | Correcciones de la versión 2, arquitectura, aislamiento por tenant, frontera SQL y preflight, esquema mínimo, ciclo de vida y cierre excepcional, principal inmutable, eventos, purga, identidad y determinismo, contrato sintético y procedencia, RF-29, API interna, modelo de fallos y decisiones |
| [F35SBXB_B2_Contrato_Verificacion.md](F35SBXB_B2_Contrato_Verificacion.md) | Matriz de pruebas P01..P33, contrato del gate sucesor de B2 (con B1F desde el ancla y desde el cierre), verificación de las sesiones de diseño y decisiones Q1–Q9 |

## Qué no incluye este incremento

No existe todavía el almacén (`sbxb_store.py`), ni el runtime SQLite, ni pruebas ejecutables, ni el gate de B2. Tampoco pipeline, ML, dependencias nuevas ni cambios en el runtime, en la CI ni en el dataset.

## Gobierno

Este diseño no modifica `CLAUDE.md` ni `docs/PROGRESS.md`, que forman parte del conjunto auditado de B1. Por eso todavía no registran el cierre de B1. Lo hará el incremento ejecutable del gate de B2 (Q1, DH-B2-07) en una única transición monotónica y auditada, del blob histórico de B1 al blob nuevo de B2. Sus descendientes no pueden volver atrás, y el contenido histórico de B1 no se reescribe.

Los estados de gobierno no cambian:

- G0 real = NO APROBADA y ADR-005 = PROPUESTA;
- G0-SBX = APROBADA CON RESTRICCIONES;
- F35 productiva = BLOQUEADA y F36–F40 = BLOQUEADAS;
- Alcance C = BLOQUEADO y datos reales = PROHIBIDOS.

B2 no autoriza ML, scoring, recomendación ni selección automática, y no modifica RF-01..RF-27 ni RF-23. RF-29 sigue experimental y solo sobre el proceso.

## Próximo paso

Reauditoría final focal independiente de la versión 2.1 del diseño. Solo después, y con autorización, vendrá el incremento de implementación: almacén, casos de prueba y gate sucesor.
