# F33 — Diseño funcional del motor inteligente y ADR-005 / G0

Diseño formal del futuro motor inteligente de reclutamiento del SaaS (caso Colegio Andino de Huancayo). Define sus límites, la arquitectura funcional, las entradas y salidas, la gobernanza y los criterios para aprobar la puerta **G0**.

**Estado:** versión 1 (04/10/2026), **pendiente de auditoría**. Es solo diseño. No hay ML productivo, scoring, motor de recomendación, embeddings, endpoints, migraciones, UI, integración Laravel↔ML ni transcripción. No se instalaron dependencias.

## Resultado

- **G0 = NO APROBADA.** Falta, en particular:
  - la aprobación de ADR-005 por el equipo;
  - la revisión jurídica y la evaluación de impacto;
  - el análisis de datos personales;
  - la necesidad institucional validada.

  El detalle está en [ADR-005 §10](F33_ADR_005_G0.md#10-resultado-g0-en-f33).
- **ADR-005 (PROPUESTA):**
  - ratifica ADR-001 y ADR-002 sin enmienda;
  - dirige el motor hacia la **alternativa B** (reglas, rúbricas y procedencia; el nivel siempre lo asigna una persona);
  - mantiene **E** (ML solo sobre el proceso, RF-29);
  - deja **C** (asistencia documental) como FUTURA;
  - **rechaza D** (scoring o recomendación de candidatos).
- **Principio:** RECOMENDACIÓN / APOYO DEL SISTEMA ≠ DECISIÓN FINAL HUMANA. **RF-23 sigue siendo exclusivamente humana.**
- **Frontera B/C:** B no tiene dependencias nuevas ni extracción automática de PDF o DOCX; todo parsing, OCR o búsqueda semántica es C.
- **Datos:** F34 solo usa datos sintéticos. G0 no autoriza datos reales y el consentimiento por sí solo no los habilita.
- **Habilitado ahora:**
  - solo **F34**, con datos sintéticos y gobernanza;
  - **F35–F40 bloqueadas** hasta que G0 se apruebe.

## Documentos

| Archivo | Contenido |
|---|---|
| [F33_ADR_005_G0.md](F33_ADR_005_G0.md) | ADR-005: contexto, problema, fuerzas, alternativas A–E, decisión, consecuencias, riesgos, criterios G0, resultado, reversión y fases |
| [F33_Diseno_Funcional_Motor_Inteligente.md](F33_Diseno_Funcional_Motor_Inteligente.md) | Diseño funcional:<br>• actores, entidades, entradas y salidas, estados<br>• procedencia y auditoría, privacidad y multitenencia<br>• entrevistas y audio, arquitectura funcional<br>• requisitos candidatos, errores, límites, consistencia con el baseline y riesgos |
| [F33_Matriz_Capacidades_y_Restricciones.md](F33_Matriz_Capacidades_y_Restricciones.md) | 37 capacidades clasificadas: PERMITIDA, PERMITIDA CON RESTRICCIONES, FUTURA o BLOQUEADA |
| [F33_Flujos_Funcionales.md](F33_Flujos_Funcionales.md) | Flujos FF-01 a FF-08 con actores, precondiciones, pasos, postcondiciones, errores y límites |
| [F33_Mapa_F34_F40.md](F33_Mapa_F34_F40.md) | Qué se habilita en F34–F40 según el estado de G0 y cómo se corresponde con las decisiones de F30 |
| [`diagramas/`](diagramas/) | F33-01 (flujo funcional) y F33-02 (arquitectura funcional), en PNG reproducible |
| [F33_Diseno_Motor_Inteligente.docx](F33_Diseno_Motor_Inteligente.docx) · [PDF](F33_Diseno_Motor_Inteligente.pdf) | Consolidado de los documentos anteriores, con los diagramas |

## Cómo se reproduce

```
python docs/academico/tools/f33/diagramas.py      # diagramas PNG
python docs/academico/tools/f33/f33.py            # consolidado DOCX
powershell -ExecutionPolicy Bypass -File docs/academico/tools/f27b/topdf_toc.ps1 docs/academico/diseno-inteligente/F33_Diseno_Motor_Inteligente.docx
python docs/academico/tools/f33/validate_f33.py   # validación de F33
```

Los scripts usan solo la biblioteca estándar, Pillow (ya usado por las herramientas académicas) y Microsoft Word para el PDF.

## Fuentes y límites

- **Fuentes:** la evidencia y las normas citadas ([Sxx], [Oxx]) remiten a la [matriz de F30](../investigacion-ia/F30_Matriz_Evidencia_Cientifica.md). Las restricciones vienen de [F32](../auditoria-global/F32_Readiness_F33.md) y de ADR-001 a ADR-004.
- **Baseline:** no cambia. RF-01 a RF-27, CU-01 a CU-20, el F11 y ARQ-01 quedan intactos. Los requisitos nuevos se proponen como **candidatos** (RF-32 en adelante) y no se registran hasta que G0 avance.
- **Alcance de la validación:** el diseño no prueba eficacia. No hay datos reales, validación institucional, revisión jurídica ni SLA (RNF-06 y RNF-07 del F9 siguen sin verificar).
