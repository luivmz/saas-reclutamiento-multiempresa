# F35-SBX-B — Ejecución determinista del pipeline de evidencia sintética

**Estado:** F35-SBX-B INICIADA, solo sandbox sintético. B0 CERRADA E INTEGRADA. B1 (gate sucesor sobre HEAD) en desarrollo. No existe todavía pipeline funcional.

Segunda subfase de F35-SBX, dentro del [alcance autorizado](../g0-sandbox/F34E_Alcance_Autorizado.md) por la [decisión G0-SBX](../g0-sandbox/F34E_Decision_G0_SBX.md) y bajo sus [prohibiciones](../g0-sandbox/F34E_Prohibiciones.md). Parte de la entrega cerrada e integrada de [F35-SBX-A](../evidencia-sbx/README.md), que no se modifica.

B0 es solo documentación: registra la sucesión de gates que permite avanzar a B sin modificar ni debilitar los controles congelados de A. B1 construye el gate sucesor que valida HEAD antes de cualquier pipeline. Todavía no hay pipeline, almacenamiento SQLite, runner, fixtures nuevos ni dependencias.

## Documentos

| Archivo | Contenido |
|---|---|
| [F35SBXB_B0_Sucesion_de_Gates.md](F35SBXB_B0_Sucesion_de_Gates.md) | Gates históricos anclados y gate sucesor sobre HEAD, decisiones DH-B01..DH-B13, resolución de las auditorías del plan y de B0, modelo de amenazas TSBB-01..TSBB-13 y verificación transitoria de SBX-01..SBX-18 |
| [F35SBXB_B1_Gate_Sucesor.md](F35SBXB_B1_Gate_Sucesor.md) | Gate sucesor sobre HEAD: comprobaciones, alcance exacto de B1, DH-B13 en el gate, ciclo de vida del propio gate y pruebas |

## Estados vigentes

- G0 real = NO APROBADA; ADR-005 = PROPUESTA; G0-SBX = APROBADA CON RESTRICCIONES.
- F35 productiva = BLOQUEADA; F35-SBX = HABILITADA, solo sandbox sintético; F35-SBX-A = CERRADA E INTEGRADA.
- F35-SBX-B = INICIADA, solo sandbox sintético; F36–F40 = BLOQUEADAS; Alcance C = BLOQUEADO; Datos reales = PROHIBIDOS.
- RF-01..RF-27 sin cambios; RF-23 sigue humana y RF-29 experimental e informativa.

## Validación

```
python docs/academico/tools/f35sbxb/validate_f35sbxb.py
```
