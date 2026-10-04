# F34 — Dataset sintético, variables y gobernanza de datos

Contrato de datos del futuro módulo inteligente, dataset **100 % sintético** y reproducible, y su gobernanza: calidad, linaje, privacidad, leakage y límites.

**Estado:** versión 1.1 (04/10/2026), con los hallazgos de la auditoría F34 corregidos. **F34 = LISTA PARA AUDITORÍA**; **G0 = NO APROBADA**, ADR-005 = PROPUESTA y F35–F40 = BLOQUEADAS. No hay ML productivo, scoring, recomendación, embeddings, parsing de CV, endpoints, migraciones, integración, audio, vídeo ni frontend. No se instalaron dependencias.

> El dataset **NO representa datos reales del Colegio Andino** ni de ninguna persona. No contiene PII ni atributos sensibles reales.

## Resumen

- **Contrato:** [`schema.json`](../tools/f34/schema.json), 19 tablas y 179 campos con tipo, restricciones, claves y rol.
  - **Bloque A:** contexto de vacante.
  - **Bloque B:** evidencia.
  - **Bloque C:** evaluación humana.
  - **Bloque D:** proceso RF-29.
  - **Aparte:** un archivo de equidad sintética separado.
- **Dataset:** 19 archivos CSV y 27 404 filas (120 vacantes), con semilla `20261004`. Incluye casos borde, empates en el checkpoint, vacantes censuradas y datos faltantes controlados. Las inconsistencias de prueba viven aparte: 45 casos en [`qa_cases.json`](dataset/qa_casos/qa_cases.json).
- **Features:** 9 PERMITIDAS, 8 CONDICIONADAS y 5 BLOQUEADAS.
- **Labels:** 2 válidos para el proceso, 3 solo experimentales y 8 NO VÁLIDOS (contratado, seleccionado, decisión histórica…).
- **Validación:** `validate_f34.py` comprueba:
  - calidad, consistencia (incluido FF-02), PII y leakage, con recálculo independiente de las 15 variables RF-29 (`t <= checkpoint_at`) y de la etiqueta;
  - madurez de las etiquetas (purga por `label_known_at` y censura), integridad contextual entre organizaciones y vacantes, y hash canónico de entrada;
  - alertas, manifiesto y reproducibilidad (dos regeneraciones idénticas);
  - que los 45 casos intencionales se detecten.

## Documentos

| Archivo | Contenido |
|---|---|
| [F34_Modelo_de_Datos.md](F34_Modelo_de_Datos.md) | Contrato conceptual y lógico (bloques A–D), relaciones y correspondencia con F33 |
| [F34_Dataset_Card.md](F34_Dataset_Card.md) | Propósito, origen, generación, distribución, limitaciones, usos, privacidad, versionado y mantenimiento |
| [F34_Matriz_Features_Labels.md](F34_Matriz_Features_Labels.md) | 22 features y 13 labels clasificados |
| [F34_Gobernanza_Privacidad.md](F34_Gobernanza_Privacidad.md) | Regla de datos, minimización, retención, acceso, segregación, roles y equidad sintética |
| [F34_Data_Leakage_y_Calidad.md](F34_Data_Leakage_y_Calidad.md) | Reglas automáticas, matriz de leakage, casos de prueba y decisión sobre particiones |
| [F34_Preparacion_F35_F36.md](F34_Preparacion_F35_F36.md) | Readiness: F34 lista para auditoría, F35–F40 bloqueadas, y qué podrían consumir F35/F36 |
| [`dataset/`](dataset/) | CSV, [`manifest.json`](dataset/manifest.json), `fairness_sintetico/` y `qa_casos/` |

## Reproducción

```
python docs/academico/tools/f34/build_schema.py        # contrato schema.json
python docs/academico/tools/f34/generate_synthetic.py  # dataset (misma semilla → mismos bytes)
python docs/academico/tools/f34/validate_f34.py        # validación completa, incluida la reproducibilidad
```

Solo biblioteca estándar de Python (probado con 3.12). El validador lee el contrato de columnas prohibidas de RF-29 en `ml-service/src/recruitment_ml/schema.py` sin modificarlo.
