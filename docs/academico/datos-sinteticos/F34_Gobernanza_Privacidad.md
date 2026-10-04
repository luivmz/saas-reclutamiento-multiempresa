# F34 — Gobernanza de datos y privacidad

> Fase F34, versión 1 (04/10/2026). Reglas de gobierno para el dataset sintético y para cualquier dato futuro del módulo inteligente. **No inventa una base legal:** la base legal para datos reales no existe hoy y debe determinarla una revisión jurídica (F33, G0-02 y G0-03).

## 1. Regla de datos

**F34 usa solo datos sintéticos.** Están prohibidos:

- CV y documentos reales;
- nombres, correos, teléfonos y documentos de identidad;
- postulaciones o entrevistas reales;
- PII de cualquier tipo;
- atributos sensibles;
- datos copiados de personas reales.

**El consentimiento **no** autoriza datos reales** en F34. F33 y G0 tampoco los autorizan.

Cualquier uso futuro de datos reales exige, como fija la regla de datos de [ADR-005 §6.10](../diseno-inteligente/F33_ADR_005_G0.md#6-decisión-propuesta):

1. autorización explícita del equipo;
2. revisión contractual (contrato 7 de `CLAUDE.md`);
3. revisión jurídica;
4. análisis de privacidad y datos personales;
5. una aprobación específica posterior, distinta de G0.

## 2. Principios aplicados

| Principio | Aplicación en F34 | Aplicación futura (si algún día hubiera datos reales) |
|---|---|---|
| **Propósito** | Probar contratos, reglas y controles; nada sobre personas | Finalidad escrita y limitada al proceso de evaluación; ningún uso secundario |
| **Minimización** | Solo tokens; sin identidad; textos de plantilla | Solo los campos del contrato; citas mínimas de evidencia; nada de copias de CV |
| **Retención** | El dataset es un artefacto versionado en Git; se reemplaza por versiones nuevas | Plazos definidos por la revisión jurídica, con borrado verificable |
| **Acceso** | Público dentro del repositorio académico (no contiene datos personales) | Por rol y organización (Policies), con registro de auditoría |
| **Segregación multiempresa** | `organization_token` en todas las entidades; ninguna fila cruza organizaciones | `organization_id` solo en Laravel; scope global; pruebas cross-tenant (contrato 5) |
| **Pseudonimización** | Tokens sintéticos sin relación con identidades | Tokens técnicos por ejecución hacia cualquier servicio; nunca IDs internos ni datos de contacto (F33 §8) |
| **Seguridad** | Sin secretos ni credenciales en el dataset | Cifrado, control de acceso y auditoría de solo inserción (contrato 6) |
| **Transparencia** | Dataset Card y manifiesto | Información previa al postulante sobre criterios y procedimiento (F30 [S86]; O13 art. 25, por contrastar) |

## 3. Datos prohibidos y sensibles

| Categoría | Ejemplos | Estado |
|---|---|---|
| Identidad y contacto | Nombre, correo, teléfono, DNI, dirección, foto | **Prohibido** en todas las tablas (PII-01, PII-02) |
| Atributos sensibles | Edad, sexo, género, etnia, nacionalidad, estado civil, religión, ideología, salud, discapacidad, afiliación sindical, biometría | **Prohibido**; no se recolecta (F30 D-10) |
| *Proxies* sensibles | Colegio o universidad de procedencia, distrito, año de egreso, años de experiencia crudos | **Prohibido** como feature; los años de experiencia, solo como comparación con un umbral (FT-02) |
| Variables posteriores a la decisión | Selección, decisión RF-23, posición en el ranking, cierre | **Prohibido** en features (LK-01) |
| Grupo de equidad | `grupo_sintetico` | **Solo sintético**, en archivo separado, nunca en features (PII-03, LK-07) |

## 4. Equidad en F34

- **No hay atributos sensibles reales.** El único atributo de grupo es `grupo_sintetico`: una etiqueta abstracta (`GS-A`, `GS-B`) asignada al azar, marcada como sintética.
- **Está separado** en `dataset/fairness_sintetico/`, fuera del feature set, del manifiesto de features y de toda tabla principal.
- **Sirve solo** para probar metodológicamente, en F37 y con datos sintéticos, que un pipeline de equidad agrega y separa correctamente.
- **No puede usarse** para scoring ni para ninguna decisión.

## 5. Roles responsables

| Rol | Responsabilidad |
|---|---|
| Equipo del proyecto | Dueño del dataset y del generador; aprueba versiones; decide G0 |
| Responsable de datos (a designar por el equipo) | Revisa el Dataset Card, los validadores y el manifiesto en cada versión |
| Revisión jurídica (externa, futura) | Base legal, finalidad, retención y evaluación de impacto antes de cualquier dato real |
| Docente o representante institucional | Valida la necesidad institucional (G0-12); no aprueba datos reales por sí solo |

No se asignan nombres de personas a estos roles en este documento.

## 6. Control de cambios

- **Versionado:** todo cambio del contrato (`schema.json`) o del generador sube `schema_version` o `generator_version`, y produce un dataset y un manifiesto nuevos.
- **Validación:** antes de versionar, el validador F34 debe pasar sin fallas, incluida la reproducibilidad.
- **Reemplazo:** un dataset nuevo nunca se mezcla con uno anterior; se reemplaza completo.

## 7. Límites

Este documento no es asesoría legal. Las normas citadas (Ley 29733, DS 016-2024-JUS y DS 115-2025-PCM) requieren la revisión jurídica y el contraste oficial que F30 y F33 ya señalaron.
