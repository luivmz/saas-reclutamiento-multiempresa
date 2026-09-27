# Adenda académica post-release al Formato 09 v1.1

**Esta adenda no es una nueva versión oficial del Formato 09.** El entregable publicado sigue siendo [`phase-24/output/F9_Alcance_Proyecto_Software_Colegio_Andino_FINAL_v1.1.docx`](../phase-24/output/F9_Alcance_Proyecto_Software_Colegio_Andino_FINAL_v1.1.docx) (y su PDF), con los mismos SHA-256 del [manifiesto del release](../../v1.1/release-manifest-v1.1.md). No se modificó.

La adenda registra lo que ocurrió **después** de su redacción (Fase 24, 24/09/2026) y lo que aportaron los Formatos 02 a 08 de la Fase 27B.

## 1. Estado post-release

Verificado con Git el 26/09/2026:

| Hecho | Detalle |
|---|---|
| `main` contiene la v1.1 | `origin/main` = `634f354` «merge: release v1.1 academic» |
| Etiqueta publicada | `v1.1.0-academic`, anotada, sobre `634f354` y presente en `origin` |
| Árbol del release | `develop` y `main` comparten el árbol `4918cccaef87b9e06480100f8643a732d9f5c875` |
| v1.0 intacta | `v1.0.0-academic` → `9a946c2` |
| GitHub Release | **No verificado en esta fase**: `gh` no está disponible |

El F9 publicado es anterior al release. Por eso dice que la «Fase 25 realizará el QA global final» y cita como última regresión la de la Fase 21: Laravel 408 + 8 omitidas; Python 532; componentes 42; Cypress 20 specs y 84 pruebas.

## 2. QA global de la Fase 25

Resultados registrados en [`docs/v1.1/phase-25-final-qa.md`](../../v1.1/phase-25-final-qa.md). La F27B no los volvió a ejecutar.

| Suite | Resultado |
|---|---|
| PHPUnit | 411 superadas, 8 omitidas, 0 fallidas, 1498 aserciones |
| pytest (servicio ML) | 533 superadas |
| Componentes (Vitest) | 42/42 |
| TypeScript | 0 errores |
| Cypress | 20 specs, 85/85 |

Hallazgos corregidos en la F25:

- **F25-M01:** un ID no numérico en la ruta devolvía 500; ahora devuelve 404.
- **F25-M02:** las fichas de tabla se cortaban a 375 px.

No cambia el alcance del F9: RF-01 a RF-27 siguen siendo la línea base. RF-28, RF-29 y RNF-C siguen como candidatos.

## 3. Divergencias conocidas del F9 y cómo quedan resueltas

| Tema | En el F9 publicado | Resolución académica (F27B) |
|---|---|---|
| Rótulos de RF | 13 rótulos distintos del nombre canónico (la F24 registró «seis», L-02) | [F6](../practica-06/README.md): tabla de nombre canónico y alias histórico. Los IDs no cambian |
| Catálogo de CU | CU-01 a CU-20 numerados, sin nombre. Diverge del catálogo de 13 CU y de UC-RF (D-08) | [F8](../practica-08/README.md): nombres asignados (O-F8-01, a confirmar por el equipo) y matriz de correspondencia entre las 3 vistas, que coincide con la tabla RF → CU → IN del F9 (comprobado por `validate.py`) |
| CU-10 | Solo con RR. HH. | F8 agrega al Aprobador / Dirección, como en la implementación (UC-RF12) |
| Consulta de auditoría | RF-27 «incluido en CU-18» | Sin CU académico propio. Se **propone** CU-21 (O-F8-02), pendiente de decisión |
| Catálogo de RNF | 10 RNF académicos frente a 11 técnicos (D-09, L-01) | [F7](../practica-07/README.md): equivalencia no 1:1 y estado real de cada RNF (5 verificados, 3 con evidencia parcial, 2 no verificados) |
| TO-BE (anexo A) | Rama «cerrar sin selección» | [F5](../practica-05/README.md): **propuesta futura** TB-F1, no implementada (A-30) |

## 4. Qué no cambia

- **Decisión final:** es **humana** y la registra el Aprobador / Dirección (RF-23). El sistema no selecciona, descarta ni contrata.
- **RF-29:** experimental y solo sobre el proceso; no evalúa candidatos. **RF-28:** candidato no implementado. **RNF-C:** propuesta.
- **AS-IS:** sigue siendo **preliminar** y sujeto a validación institucional.

Si el equipo decide emitir una versión 1.2 del Formato 09, esta adenda y la [trazabilidad F2–F9](../trazabilidad/F2-F9-traceability.md) son su insumo. Esa emisión requiere una decisión y una auditoría propias.
