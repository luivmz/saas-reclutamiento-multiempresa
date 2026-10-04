# F32 — Auditoría académica global

Auditoría del baseline integrado después de F31 y correcciones autorizadas F32-M01/L01/L02. Fecha: 03/10/2026, America/Lima; las consultas de CI corresponden al 04/10/2026 UTC. No modifica el producto, fuentes oficiales, modelos, artefactos publicados ni documentos históricos.

## Entregables

- [Informe global](F32_Auditoria_Academica_Global.md): método, verificaciones transversales, trazabilidad y evidencia Git/QA.
- [Matriz de hallazgos](F32_Matriz_Hallazgos.md): severidad, evidencia, impacto y aceptación de las acciones propuestas.
- [Readiness F33](F32_Readiness_F33.md): autorización limitada al diseño; G0 no se considera aprobada.

## Baseline auditado

| Referencia | Commit |
|---|---|
| develop y origin/develop | `70f4fcde47f81087024eefe60b6d42b45177cfef` |
| main y origin/main | `3f342ab22c8ff65d4e004cfcaaab041198376b9d` |
| Rama de auditoría | `feature/f32-global-academic-audit`, creada desde develop |
| Árbol de ambas ramas integradas | `b1babd6be7dd85cfb9865e5d51912b51dcf06282` |

Resultado: **APROBADA CON OBSERVACIONES; APTO PARA F33 DE DISEÑO**. Hallazgos originales: 1 MEDIUM y 2 LOW, ahora **RESUELTOS**. Abiertos: CRITICAL 0, HIGH 0, MEDIUM 0, LOW 0; se conservan 4 OBSERVATION. G0 sigue **NO APROBADA**: no se autoriza scoring/recomendación de personas, implementación funcional, aprobación automática de ADR-005 ni nuevas dependencias.

La auditoría inicial creó los cuatro archivos de esta carpeta. El delta de corrección autorizado incluye también recetas, README vigentes, el dispatcher, pruebas de protección y excepciones de alcance limitadas a rama/base. **F32 CERRADA CON OBSERVACIONES**: el usuario autorizó un único commit del delta auditado y su integración mediante merges `--no-ff`, primero en develop y, solo tras CI verde, en main. Los hashes y checks finales se consultan en Git/GitHub. No se autoriza tag, release ni eliminación de ramas; G0 sigue NO APROBADA.

## Reproducción de las comprobaciones

Desde la raíz, ejecutar los validadores documentales existentes indicados en el informe. No ejecutar generadores para auditar. La clave histórica `f11` está bloqueada; la receta vigente usa explícitamente `f11r`. La regresión de seguridad se comprueba, sin generar entregables, con `python -B -m unittest discover -s docs/academico/tools/f27b -p test_f32_safety.py`: 10/10 PASS.

La validación de enlaces cubre destinos locales de Markdown; no prueba por sí sola anclas ni URLs externas. MANIFEST/evidencias contrastan SHA-256 contra el árbol de trabajo, con normalización LF para archivos de texto según la convención del repositorio. El informe distingue esa integridad de una revisión científica, jurídica o institucional.
