# F35-SBX-B — B2: almacén efímero sintético

> **Estado: B2 = IMPLEMENTADA / CANDIDATA A AUDITORÍA INDEPENDIENTE.** Fecha: 12/10/2026. Rama `feature/f35-sbx-b2-ephemeral-store`, creada desde `develop` `72e86c5838984ea873d6dd56c179d94217b27317`.
>
> - **Versión 1 del diseño** (`ae25e8c60c538ce2336fadd98489de8eee9e0983`): veredicto «B2-DESIGN APROBADO CON CORRECCIONES PREVIAS», sin hallazgos BLOCKER ni HIGH.
> - **Versión 2** (`eaac2120ede71289cd282a283baf6cc8698ca87b`): resuelve sus cinco MEDIUM (B2-M01..B2-M05) y fija las decisiones Q1–Q9. La reauditoría dio M01–M04 por resueltos y M05 como parcialmente resuelto.
> - **Versión 2.1** (`24e4ed911ca1580c5d4afeace0e97e3f515f10e8`): completa M05 y Q1 con una transición de gobierno única y monotónica. Su reauditoría final focal dio el veredicto «B2-DESIGN APROBADO PARA IMPLEMENTACIÓN».
> - **Implementación** (12/10/2026): almacén, casos P01..P33 y gate sucesor, sin cambios de diseño. Es código de desarrollo NO AUDITADO (Q6).
>
> Punto de partida: B1 = CERRADA / CONGELADA / INTEGRADA.
>
> - Ancla auditada: `8e94a60274fe39ebda3e9961bc58036b389dfc00`.
> - Cierre: `3d9b78307684a0dfb093e31d28fde290b2b1cb4a` ([B1-FREEZE](../evidencia-sbx-b-freeze/F35SBXB_B1_Freeze.md)).
> - Integración: `develop` `72e86c5838984ea873d6dd56c179d94217b27317`, con CI 38179967121 en verde, y `main` `3fdfdcecdec47b08d99e96968dd915e0e1b9010b`, con CI 38180279164 en verde.

B2 es el incremento sucesor de B1. Implementa el almacén donde F35-SBX-B guardará los objetos de un run sintético: una base SQLite `:memory:` por organización sintética y escenario, que solo admite inserciones de contenido F34 autorizado y se destruye cerrando la conexión.

| Archivo | Contenido |
|---|---|
| [F35SBXB_B2_Diseno_Almacen.md](F35SBXB_B2_Diseno_Almacen.md) | Correcciones de la versión 2, arquitectura, aislamiento por tenant, frontera SQL y preflight, esquema mínimo, ciclo de vida y cierre excepcional, principal inmutable, eventos, purga, identidad y determinismo, contrato sintético y procedencia, RF-29, API interna, modelo de fallos y decisiones |
| [F35SBXB_B2_Contrato_Verificacion.md](F35SBXB_B2_Contrato_Verificacion.md) | Matriz de pruebas P01..P33, contrato del gate sucesor de B2 (con B1F desde el ancla y desde el cierre), decisiones Q1–Q9 y, en §5, la evidencia de la implementación: commits, resultados, delta de gobierno, historias de B1F, negativos NB2 y observaciones |
| [sbxb_store.py](../tools/f35sbxb2/sbxb_store.py) | Almacén: API interna cerrada, catálogo fijo de sentencias, preflight, esquema `STRICT`, procedencia, ciclo de vida, cierre excepcional y purga |
| [validate_f35sbxb2.py](../tools/f35sbxb2/validate_f35sbxb2.py) | Gate sucesor sobre HEAD: CTX, B1F, AIN, B0F, HST, SBX, SCP, FSY, FLG, DEP, PRE, STA, DYN, DET, ISO, PUR, DAT, CAP y GOV, con P01..P33, las historias F01–F21 y los negativos NB2 |

Uso, desde la raíz del repositorio: `python -I docs/academico/tools/f35sbxb2/validate_f35sbxb2.py`. La referencia es un clon limpio sin remoto: en un árbol de trabajo con artefactos locales (bundles de Vite o `.pyc` de pytest), FSY falla igual que en el gate de B1.

## Qué no incluye este incremento

No hay pipeline funcional ni ML, ni dependencias nuevas, ni cambios en el runtime, en la CI, en el dataset, en A, en B0, en B1 ni en B1-FREEZE. B2 no persiste nada de RF-29 ni ningún puntaje, ranking, recomendación o selección.

## Gobierno

`CLAUDE.md` y `docs/PROGRESS.md` forman parte del conjunto auditado de B1. Solo cambian en una única transición monotónica (Q1, DH-B2-07), del blob histórico de B1 al blob nuevo de B2, con el delta cerrado que enumera el [contrato, §5.2](F35SBXB_B2_Contrato_Verificacion.md#52-delta-y-transición-de-gobierno). Esa transición registra B1 cerrada e integrada y B2 implementada y candidata a auditoría independiente. Sus descendientes no pueden volver atrás, y el contenido histórico de B1 no se reescribe. El gate deriva el commit de la transición de la historia y lo compara con el registrado.

Los estados de gobierno no cambian:

- G0 real = NO APROBADA y ADR-005 = PROPUESTA;
- G0-SBX = APROBADA CON RESTRICCIONES;
- F35 productiva = BLOQUEADA y F36–F40 = BLOQUEADAS;
- Alcance C = BLOQUEADO y datos reales = PROHIBIDOS.

B2 no autoriza ML, scoring, recomendación ni selección automática, y no modifica RF-01..RF-27 ni RF-23. RF-29 sigue experimental y solo sobre el proceso.

## Próximo paso

Auditoría independiente de la implementación. B2 no se declara cerrada, integrada ni productiva: el cierre, el freeze, la integración y la publicación requieren autorización explícita del equipo.
