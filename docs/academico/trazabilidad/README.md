# Trazabilidad académica F2 → F9

| Archivo | Contenido |
|---|---|
| [`F11-architecture-traceability.md`](F11-architecture-traceability.md) | Arquitectura (F28): componente → RF → CU → RNF → alcance F9 → artefacto técnico |
| [`F2-F9-traceability.md`](F2-F9-traceability.md) | Cadena completa, vistas por actividad y por RF, RNF transversales, resultado de la validación y pendientes T-01 a T-12 con su resolución |

Se genera con `python docs/academico/tools/f27b/build.py trace` desde los mismos modelos que los Formatos 02 a 08.

## Qué valida `validate.py` y qué no (H-16)

`docs/academico/tools/f27b/validate.py` comprueba la **coherencia estructural** entre los modelos y los entregables:

- **Existencia de IDs:** que no falten ni sobren actividades, RF o CU.
- **Actores y métodos:** que cada actividad, RF y CU tenga su actor, y cada RNF su método de verificación.
- **Cobertura y correspondencia:**
  - la cobertura de RF-01 a RF-27;
  - la coincidencia de etiquetas entre F2 y F4;
  - la correspondencia RF → CU → bloque IN con la tabla del F9 publicado.
- **Vocabulario:** el de estados, y la ausencia de variantes de nombre retiradas.
- **Afirmaciones:** un barrido textual de afirmaciones de validación institucional sin negación.
- **DOCX:** su integridad (ZIP y XML válidos, imágenes presentes y sin campos de plantilla vacíos).

**No valida la coherencia semántica completa.** No puede decidir, por ejemplo:

- si un flujo BPMN es correcto como proceso;
- si una compuerta representa bien una decisión;
- si un problema está bien asignado a una actividad;
- si un texto afirma algo no soportado con palabras que el barrido no detecta.

Por eso **no es la única prueba**: «0 fallas» significa que la estructura es coherente, no que el contenido sea correcto.

## Revisión manual (F27D)

Después de las correcciones de la F27D se revisaron a mano, además de ejecutar `validate.py`:

| Entregable | Qué se revisó |
|---|---|
| F3 | Especificación cerrada frente al borrador: pools, SP-01, mensajes MF-01 a MF-04, AS-06 → AS-08 y glosario |
| F5 | Dos niveles; SP-P; uniones GM1 y GM2; GF «¿Finalista?»; rechazo de TB-22; TB-F1 desconectado; TB-30 transversal; mensajes MT-01 a MT-08 |
| F8 | Decisión del equipo; CU-18 renombrado en el modelo, las tablas, la matriz y el borrador; CU-21 diferido; RF-27 transversal |
| Trazabilidad | Problema directo frente a problema vía solución (AS-06 → P1 y T-12); RF-23 → CU-18 → UC-RF23 (IN-07); RF-27 → UC-RF27 (IN-08) |

La **auditoría F27E** vuelve a revisar el contenido semántico de forma independiente.
