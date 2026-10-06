# F34E — Alcance autorizado por G0-SBX

> Fase F34E, versión 1 (04/10/2026). Vale **solo** mientras G0-SBX esté APROBADA CON RESTRICCIONES ([decisión](F34E_Decision_G0_SBX.md)). Siempre rigen las [prohibiciones](F34E_Prohibiciones.md).

## F35-SBX: pipeline experimental de evidencias sintéticas

Trabajo académico del alcance B de ADR-005 (reglas, rúbricas y procedencia, con el nivel asignado siempre por una persona), **exclusivamente con datos sintéticos** y sin conexión con el runtime productivo.

| Permitido en F35-SBX | Condición |
|---|---|
| Schemas y contratos | Derivados del contrato de F34 o nuevos, versionados |
| Validaciones | Con casos negativos y positivos |
| Almacenamiento experimental aislado | Fuera de la base de datos productiva y sin acceso desde el runtime |
| Fixtures y documentos sintéticos | Marcados `[SINTÉTICO]`, con `source_type = synthetic` y semilla reproducible |
| Hashes y provenance | Hash canónico de entrada y procedencia de cada evidencia |
| Revisión humana simulada | Actores sintéticos; ningún resultado se presenta como juicio sobre una persona real |
| Pruebas de seguridad | Sobre el [modelo de amenazas aceptado](../g0-readiness/F34A_Modelo_de_Amenazas.md), con prioridad para T-10, T-11, T-14, T-17 y T-25 |
| Aislamiento entre organizaciones | Pruebas cross-tenant con organizaciones sintéticas |
| Estados de procesamiento | `analysis_run` y eventos de solo inserción, sintéticos |
| Auditoría experimental | Sin PII; separada de `audit_logs` productivo |
| APIs o stubs aislados | Solo si no se registran en el runtime productivo ni lo afectan |

## Fuera de F35-SBX

- Cualquier cambio en `app/`, `routes/`, `config/`, `database/` (migraciones), `resources/`, el servicio ML productivo o las dependencias del proyecto.
- F36–F40, también en modo sandbox: necesitan su propia autorización explícita.
- Cualquier uso de los adjuntos de gobierno (`g0-evidence/adjuntos/`) como datos.
