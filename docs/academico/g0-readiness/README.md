# F34A — Cierre de prerequisitos de G0

Prepara, sin inventar aprobaciones, todo lo que la puerta G0 de [ADR-005](../diseno-inteligente/F33_ADR_005_G0.md) necesita del proyecto: matriz de criterios, paquete de aprobación del ADR, checklist jurídico, análisis de privacidad preliminar, instrumento de necesidad institucional, modelo de amenazas y requisitos candidatos.

**Estado:** versión 1.1 (04/10/2026), corregida tras la auditoría F34A. **F34A = LISTA PARA AUDITORÍA.** **G0 = NO APROBADA**, **ADR-005 = PROPUESTA** y **F35–F40 = BLOQUEADAS**. RF-23 sigue humana y RF-29 experimental e informativa. **Los datos reales siguen PROHIBIDOS.**

> F34A no es una revisión jurídica, no afirma cumplimiento legal, no contiene firmas ni respuestas institucionales y no cambia el runtime, las migraciones, la interfaz ni el baseline RF-01 a RF-27.

## Resultado

| Estado final | Criterios G0 |
|---|---|
| CUMPLIDO | 9: G0-01, G0-04, G0-06, G0-07, G0-08, G0-10, G0-11, G0-13, G0-15 |
| PARCIAL | 1: G0-09 |
| PENDIENTE EXTERNO | 4: G0-02, G0-03, G0-12, G0-14 |
| NO APLICA | 1: G0-05 |

Lo que falta para G0 está en la [decisión de readiness](F34A_Decision_Readiness_G0.md#4-qué-falta-exactamente-para-aprobar-g0-alcance-b).

## Documentos

| Archivo | Contenido |
|---|---|
| [F34A_Matriz_G0.md](F34A_Matriz_G0.md) | Los 15 criterios G0 con estado, evidencia, responsable y acción |
| [F34A_Paquete_Aprobacion_ADR005.md](F34A_Paquete_Aprobacion_ADR005.md) | Resumen, decisión propuesta, alcance B, exclusiones, riesgos, reversión y registro de decisión (PENDIENTE) |
| [F34A_Checklist_Revision_Juridica.md](F34A_Checklist_Revision_Juridica.md) | 29 puntos: VERIFICADO, LECTURA PRELIMINAR o REQUIERE ABOGADO/RESPONSABLE LEGAL |
| [F34A_Analisis_Privacidad_Preliminar.md](F34A_Analisis_Privacidad_Preliminar.md) | Análisis tipo PIA/DPIA preliminar, sin afirmar cumplimiento |
| [F34A_Validacion_Necesidad_Institucional.md](F34A_Validacion_Necesidad_Institucional.md) | Instrumento para docente, RR. HH., Administración y representante institucional, sin respuestas |
| [F34A_Modelo_de_Amenazas.md](F34A_Modelo_de_Amenazas.md) | STRIDE: activos, actores, fronteras y 25 amenazas con mitigación y riesgo residual |
| [F34A_RF_Candidatos.md](F34A_RF_Candidatos.md) | RF-CAND-01 a RF-CAND-12, fuera del baseline |
| [F34A_Decision_Readiness_G0.md](F34A_Decision_Readiness_G0.md) | Estado, criterios de salida S-01 a S-08 y lo que falta |

## Validación

```
python docs/academico/tools/f34a/validate_f34a.py
```

Comprueba que ningún documento afirma una aprobación inexistente, que ningún criterio externo aparece CUMPLIDO, que ADR-005 sigue PROPUESTA, que G0 sigue NO APROBADA, que los RF candidatos no contaminan el baseline, que F35–F40 siguen bloqueadas, que los datos reales siguen prohibidos y que no hay dependencias nuevas. Tras la auditoría F34A también comprueba que una evaluación de impacto planificada NO cierra G0-02, que la auditoría no se presenta como libre de PII, que la prohibición de ordenar personas se limita al nuevo motor (RF-21 se mantiene), que `/v1/*` falla cerrado, que no se presentan roles no implementados como vigentes y que existe la amenaza de XSS persistente. Incluye casos negativos que mutan los documentos en memoria. Solo biblioteca estándar de Python.
