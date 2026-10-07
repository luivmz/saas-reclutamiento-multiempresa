# F35-SBX-A — Pipeline experimental de evidencia sintética: diseño, contrato y validación

**Estado de la fase:** F35-SBX-A INICIADA — diseño, contratos, fixtures sintéticos y validación académica. Sin runtime productivo ni capacidades de alcance C.

Primera subfase de F35-SBX, dentro del [alcance autorizado](../g0-sandbox/F34E_Alcance_Autorizado.md) por la [decisión G0-SBX](../g0-sandbox/F34E_Decision_G0_SBX.md) de F34E y siempre bajo sus [prohibiciones](../g0-sandbox/F34E_Prohibiciones.md). F35-SBX-A **no ejecuta ningún pipeline** (DH-04): fija el contrato, los fixtures y las reglas que F35-SBX-B tendrá que cumplir, y un validador que recalcula todo lo declarado.

## Estados vigentes

- **G0 real = NO APROBADA**; G0-02, G0-03 y G0-12 siguen PENDIENTE EXTERNO.
- **G0-SBX = APROBADA CON RESTRICCIONES** (SBX-01..SBX-18 CUMPLE).
- **F35 productiva = BLOQUEADA**.
- **F35-SBX = HABILITADA**, solo sandbox sintético.
- **F36–F40 = BLOQUEADAS**.
- **Alcance C = BLOQUEADO**.
- **ADR-005 = PROPUESTA** (canónico), con aprobación interna del equipo registrada.
- **Datos reales = PROHIBIDOS**.
- RF-23 sigue humana, RF-21 no se reemplaza y RF-29 sigue experimental e informativa.

G0-SBX y F35-SBX-A no sustituyen la revisión jurídica (G0-02), la de privacidad (G0-03) ni la validación institucional (G0-12), y nada de esta fase toca el runtime, las migraciones, la interfaz ni el baseline RF-01 a RF-27.

## Documentos

| Archivo | Contenido |
|---|---|
| [F35SBX_Alcance.md](F35SBX_Alcance.md) | Objetivo, alcance, exclusiones y decisiones humanas DH-01 a DH-09 |
| [F35SBX_Arquitectura.md](F35SBX_Arquitectura.md) | Componentes sintéticos y flujo de doce pasos |
| [F35SBX_Contratos_Datos.md](F35SBX_Contratos_Datos.md) | Contrato cerrado, campos, marcadores e identificadores |
| [F35SBX_Provenance.md](F35SBX_Provenance.md) | Procedencia verificable y cadenas de hashes |
| [F35SBX_Revision_Humana_Simulada.md](F35SBX_Revision_Humana_Simulada.md) | Qué revisa y qué nunca evalúa la revisión simulada |
| [F35SBX_Aislamiento_y_Almacenamiento.md](F35SBX_Aislamiento_y_Almacenamiento.md) | Tenants sintéticos y reglas de almacenamiento |
| [F35SBX_Threat_Model.md](F35SBX_Threat_Model.md) | Amenazas TSB-01 a TSB-17 con control, evidencia y casos negativos |
| [F35SBX_Plan_Pruebas.md](F35SBX_Plan_Pruebas.md) | Estrategia, RED → GREEN y catálogo de casos negativos |
| [F35SBX_Criterios_Cierre_y_Revocacion.md](F35SBX_Criterios_Cierre_y_Revocacion.md) | Criterios de aceptación, cierre y revocación de G0-SBX |

## Artefactos

| Archivo | Contenido |
|---|---|
| [contrato/f35sbx_contract.json](contrato/f35sbx_contract.json) | Contrato JSON cerrado `f35sbx-contract-1.0.0` |
| [fixtures/ORG-S1_evidencias.json](fixtures/ORG-S1_evidencias.json) | Dos evidencias sintéticas de ORG-S1 derivadas de F34 |
| [fixtures/ORG-S2_evidencias.json](fixtures/ORG-S2_evidencias.json) | Dos evidencias sintéticas de ORG-S2 derivadas de F34 |
| [fixtures/ORG-S3_evidencias.json](fixtures/ORG-S3_evidencias.json) | Dos evidencias sintéticas de ORG-S3 derivadas de F34 |
| [fixtures/manifest.json](fixtures/manifest.json) | SHA-256 y tamaño de cada artefacto, referencias F34 y regla de selección |

## Validación

```
python docs/academico/tools/f35sbx/validate_f35sbx.py
```

[`validate_f35sbx.py`](../tools/f35sbx/validate_f35sbx.py) usa solo la biblioteca estándar y reutiliza los analizadores de proposiciones y de estados de [`validate_f34e.py`](../tools/f34e/validate_f34e.py). Recalcula el contrato, los hashes, la provenance, el origen F34 y el aislamiento por tenant, revisa los documentos y el alcance Git, y ejecuta los casos negativos descritos en el [plan de pruebas](F35SBX_Plan_Pruebas.md). La puerta G0-SBX se sigue comprobando con `validate_f34e.py` en cada entrega.
