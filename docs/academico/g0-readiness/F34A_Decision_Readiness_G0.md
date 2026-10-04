# F34A — Decisión de readiness G0 y criterios de salida

> Fase F34A, versión 1.1 (04/10/2026), corregida tras la auditoría F34A. Resultado de F34A y criterios exactos para que el equipo pueda cambiar el estado de G0. **F34A no cambia G0.**

## 1. Estado

- **G0 = NO APROBADA.**
- **ADR-005 = PROPUESTA** (registro de aprobación: PENDIENTE).
- **F35–F40 = BLOQUEADAS.**
- RF-23 sigue siendo humana; RF-29 sigue siendo experimental e informativa.
- **Los datos reales siguen PROHIBIDOS**; el consentimiento por sí solo no levanta el bloqueo.
- F34A = LISTA PARA AUDITORÍA.

**Motivo:** de los 15 criterios, 4 son PENDIENTE EXTERNO (G0-02, G0-03, G0-12, G0-14) y 1 es PARCIAL (G0-09) ([matriz G0](F34A_Matriz_G0.md)). La regla de ADR-005 §9.1 exige que **todos** los criterios obligatorios del alcance B se cumplan.

## 2. Qué resolvió F34A

| Criterio | Antes (F33) | Después (F34A) | Por qué |
|---|---|---|---|
| G0-04 | CUMPLE (B) | CUMPLIDO | F34 cerrada con dataset sintético |
| G0-09 | PENDIENTE | PARCIAL | [Modelo de amenazas](F34A_Modelo_de_Amenazas.md) elaborado; falta la aceptación del equipo |
| G0-15 | PENDIENTE | CUMPLIDO | [RF candidatos](F34A_RF_Candidatos.md) registrados; sin dependencias nuevas |
| G0-02 | PENDIENTE | PENDIENTE EXTERNO | [Checklist jurídico](F34A_Checklist_Revision_Juridica.md) preparado; requiere abogado |
| G0-03 | PENDIENTE | PENDIENTE EXTERNO | [Análisis de privacidad preliminar](F34A_Analisis_Privacidad_Preliminar.md); requiere responsable del tratamiento |
| G0-12 | NO EVIDENCIADA | PENDIENTE EXTERNO | [Instrumento](F34A_Validacion_Necesidad_Institucional.md) preparado, sin respuestas |
| G0-14 | NO CUMPLE (propuesta) | PENDIENTE EXTERNO | [Paquete de aprobación](F34A_Paquete_Aprobacion_ADR005.md) con registro vacío |

## 3. Criterios de salida: NO APROBADA → APROBADA CON RESTRICCIONES

G0 solo puede pasar a **APROBADA CON RESTRICCIONES** (alcance B) si se cumplen **todas** estas condiciones, cada una con evidencia **real**, fechada y archivada en el repositorio:

| # | Condición | Evidencia exigida | Quién la produce | Criterio |
|---|---|---|---|---|
| S-01 | ADR-005 aprobado | Registro de la [sección 9 del paquete](F34A_Paquete_Aprobacion_ADR005.md#9-registro-de-decisión-del-equipo) con los tres integrantes en `APRUEBA` o `APRUEBA CON OBSERVACIONES`, con fecha | Equipo | G0-14 |
| S-02 | Revisión jurídica | Informe firmado y fechado que responda J-03, J-04 y J-08 del checklist, con una evaluación de impacto **COMPLETADA** y documentada, si aplica, o una conclusión jurídica documentada de **NO APLICABILIDAD**; una evaluación solo planificada NO cierra G0-02 ([regla de cierre](F34A_Checklist_Revision_Juridica.md#5-regla-de-cierre-de-g0-02-evaluación-de-impacto)) | Abogado o responsable legal | G0-02 |
| S-03 | Privacidad | Análisis de G0-03 revisado y aprobado por el responsable del tratamiento, con base legal y plazos de retención definidos | Responsable del tratamiento, con revisión jurídica | G0-03 |
| S-04 | Necesidad institucional | Respuestas reales del instrumento, fechadas y con constancia, que cumplan su criterio de cierre | Docente o representante institucional | G0-12 |
| S-05 | Modelo de amenazas | Registro de aceptación del equipo, con observaciones si las hay | Equipo | G0-09 |
| S-06 | RF candidatos | Registro F34A vigente y sin contaminación del baseline | Equipo (ya cumplido) | G0-15 |
| S-07 | Criterios de diseño | G0-01, G0-04, G0-06, G0-07, G0-08, G0-10, G0-11 y G0-13 siguen cumplidos; G0-05 sigue sin aplicar | Equipo | ADR-005 §9.2 |
| S-08 | Decisión registrada | Un registro fechado del equipo que declare el nuevo estado de G0 con enlaces a S-01 a S-07, en un commit de gobierno propio | Equipo | ADR-005 §9.1 |

**Reglas:**

- Si **cualquier** condición depende de un tercero y falta su evidencia, G0 **sigue NO APROBADA**.
- Ningún validador, auditor ni documento aprueba G0 automáticamente; `validate_f34a.py` solo comprueba que nadie declare una aprobación sin evidencia.
- APROBADA CON RESTRICCIONES habilita **solo el alcance B** (y E, ya permitido). No habilita C, D ni datos reales.
- **APROBADA** (B + C) no está prevista en este ciclo: exigiría además las columnas C de los 15 criterios y un ADR que enmiende ADR-001.
- Si se cumple una condición de reversión de [ADR-005 §11](../diseno-inteligente/F33_ADR_005_G0.md#11-condiciones-de-reversión), G0 vuelve a NO APROBADA.

## 4. Qué falta exactamente para aprobar G0 (alcance B)

1. **S-01:** la firma o constancia de decisión de los tres integrantes del equipo sobre ADR-005.
2. **S-02:** un informe jurídico firmado sobre el DS 115-2025-PCM y la Ley 31814 (J-03, J-04, J-08), con la evaluación de impacto COMPLETADA o la conclusión documentada de NO APLICABILIDAD; una evaluación solo planificada NO cierra G0-02.
3. **S-03:** la aprobación del análisis de privacidad por el responsable del tratamiento, con base legal y plazos.
4. **S-04:** respuestas reales al instrumento de necesidad, como mínimo del docente.
5. **S-05:** la aceptación registrada del modelo de amenazas por el equipo.
6. **S-08:** el registro de decisión del equipo con todo lo anterior.

Ninguna de estas evidencias puede producirla F34A.

## 5. Datos reales

Incluso con G0 APROBADA CON RESTRICCIONES, **los datos reales siguen prohibidos**. Su uso exigiría, además, autorización explícita del equipo, revisión contractual del contrato 7, revisión jurídica, el análisis de privacidad aprobado y una aprobación específica distinta de G0 (ADR-005 §6.10).
