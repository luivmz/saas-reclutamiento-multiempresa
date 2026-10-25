# Registro de deuda técnica

Deuda técnica abierta que no bloquea un cierre acreditado. Cada entrada tiene un identificador estable y no se borra: cuando se trata, cambia su estado y se enlaza la evidencia. La deuda de gobierno de la F27B sigue en [`GOVERNANCE_DEBT.md`](GOVERNANCE_DEBT.md).

## Reglas

- Cada deuda se trata en un incremento propio, con RED y GREEN, auditoría y autorización del equipo.
- Tratarla no reabre ni modifica un candidato auditado ni una capa congelada. Un cambio en un gate congelado lo hace un gate sucesor o una corrección autorizada en una rama nueva.
- Ninguna entrada de este registro cambia el estado de gobierno ni habilita una fase bloqueada.

## Deudas abiertas

| ID | Severidad | Estado | Origen | Resumen |
|---|---|---|---|---|
| GC-AF-L01 | LOW | ABIERTO / DIFERIDO | Auditoría independiente final de F35-SBX, sobre el candidato `858b5fa`, el 25/10/2026 | Una unión o un punto de reanálisis en un directorio padre de una raíz protegida puede hacer leer su destino externo antes del rechazo |

## GC-AF-L01 — Unión en un directorio padre de una raíz protegida

| Campo | Valor |
|---|---|
| Origen | Auditoría independiente final del cierre global de F35-SBX. Aprobó para integración el candidato `858b5fa71c01bf794715f78068ea0557fd56a16b` con 0 BLOCKER, 0 HIGH y 0 MEDIUM, y registró este único LOW nuevo |
| Severidad | LOW, no bloqueante para el cierre de F35-SBX |
| Estado | ABIERTO / DIFERIDO |
| Componente | El recorrido físico previo de FSY (`physical_scan`) en [`validate_f35sbx_cierre_global.py`](tools/f35sbx_cierre_global/validate_f35sbx_cierre_global.py), que pertenece a la capa congelada del cierre global |
| Descripción | El recorrido previo comprueba, sin seguirlos, los enlaces, las uniones y los puntos de reanálisis de cada raíz protegida y de todo lo que hay debajo. No comprueba los componentes padre de la ruta de cada raíz. Las raíces de varios niveles (`ml-service/src`, `ml-service/tests`, `ml-service/pyproject.toml`, `docs/academico/datos-sinteticos`, `docs/academico/g0-sandbox` y `docs/academico/g0-evidence`) se abren a través de `ml-service/`, `docs/` y `docs/academico/`. Si uno de esos padres es una unión o un punto de reanálisis, el sistema operativo lo resuelve al abrir la raíz, y el recorrido enumera el destino externo antes de que el gate rechace el estado |
| Impacto | Lectura de un destino fuera del checkout durante la verificación, antes del rechazo, en el caso delimitado: una unión o un punto de reanálisis colocado en un directorio padre de una raíz protegida de un checkout local |
| Propiedad preservada | El gate sigue fallando cerrado. Según la auditoría independiente final, FSY y SBX fallan en ese caso y no hay falso PASS |
| Alcance | Una herramienta de validación académica, sobre un checkout local manipulado. No afecta al runtime de la aplicación ni es una vulnerabilidad productiva demostrada |
| Recomendación | Comprobar, sin seguirlos, los componentes padre de cada raíz protegida, desde la raíz del repositorio, antes de cualquier enumeración. Añadir un caso de regresión con una unión en un directorio padre, como `docs/academico/` o `ml-service/`, que exija el fallo sin que ninguna línea FALLA nombre el destino, como hace GC46 con una unión dentro de una raíz |
| Tratamiento | Un incremento futuro separado, con RED y GREEN y auditoría. No reabre ni modifica el candidato auditado `858b5fa` ni la capa congelada del cierre global |
| Evidencia | El veredicto de la auditoría independiente final, comunicado por el equipo el 25/10/2026. Este registro no lo reproduce: lo registra para tratarlo después |
