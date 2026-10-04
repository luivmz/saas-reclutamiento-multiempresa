# Deuda de gobierno detectada en la Fase 27B

Documentos de gobierno del repositorio que quedaron en el estado **anterior al release v1.1**. La F27B **no los corrige**, porque su alcance son los entregables académicos F2 a F8. Aquí se documenta la deuda para un cambio de gobierno autorizado, sin mezclarla con los formatos.

## Estado real (verificado con Git el 26/09/2026)

| Referencia | Valor |
|---|---|
| `origin/main` | `634f354` «merge: release v1.1 academic» |
| `v1.1.0-academic` | Etiqueta anotada sobre `634f354` |
| `origin/develop` | `c712539` «merge: close phase 26 release closeout» (merge de la F26) |
| Árboles | `develop^{tree}` = `main^{tree}` = `4918cccaef87b9e06480100f8643a732d9f5c875` |
| `v1.0.0-academic` | `9a946c2`, sin cambios |

**No verificado:** el CI de `main` y la existencia del GitHub Release. `gh` no está instalado y la F27B no consulta la web de GitHub.

## Deuda

| ID | Documento | Qué dice | Estado real | Severidad |
|---|---|---|---|---|
| GD-01 | `CLAUDE.md`, «Estado actual» | `main` sigue siendo la v1.0 y no contiene la v1.1; `develop` = `2b97fe3`; la F26 está «implementada, pendiente de auditoría», con la etiqueta «no creada» | `main` contiene la v1.1 (`634f354`) con la etiqueta publicada; `develop` = `c712539` | MEDIUM |
| GD-02 | `CLAUDE.md`, «Documentación fuente» | No menciona la línea académica F27+ (`docs/academico/`, `ACADEMIC_BASELINE.md`, `practica-02` a `practica-08`) | Existe desde la F27B-0 y la F27B | LOW |
| GD-03 | `docs/PROGRESS.md` | La fila 26 dice «Implementada en `feature/phase-26-release-closeout`, pendiente de auditoría» y la cabecera, `develop` = `2b97fe3` | La F26 está integrada y publicada; no hay filas para la F27 | MEDIUM |
| GD-04 | `docs/v1.1/release-manifest-v1.1.md` | `FINAL_DEVELOP_MERGE_COMMIT` y `FINAL_MAIN_MERGE_COMMIT` están «por resolver»; la etiqueta figura como propuesta | `c712539` y `634f354`; la etiqueta está sobre `634f354`; los árboles son iguales | LOW |
| GD-05 | `docs/v1.1/final-acceptance-checklist.md` | 11 casillas `[ ]`: estrategia, auditoría y los 7 pasos de cierre | Los merges y la etiqueta existen; el CI y el GitHub Release no se verificaron | LOW |
| GD-06 | `CHANGELOG.md`, `docs/v1.1/release-notes-v1.1.md` | «Etiqueta propuesta… no creada / pendiente de auditoría» | La etiqueta existe | LOW |
| GD-07 | Entorno local | La rama `main` local está en `4563c69`, detrás de `origin/main` | Se actualiza con `git fetch` y un avance rápido, **con autorización**; la F27B no toca `main` | INFO |

## Cómo corregirla (propuesta)

1. **Rama:** hacer las correcciones en una rama de gobierno propia (por ejemplo, `docs/governance-post-release`), **no** en la rama F27.
2. **Qué actualizar:**
   - GD-01 y GD-03, conservando el texto anterior como nota histórica, como se hizo en las fases previas;
   - GD-04 a GD-06, con los hashes reales.
3. **Qué verificar antes de marcar las casillas:** el CI de `main` y el GitHub Release, en la web de GitHub o con `gh`.
4. **Cómo integrarla:** con una auditoría y la autorización del equipo (contrato 10 de `CLAUDE.md`).

Los formatos F2 a F8 **no dependen** de esta deuda: citan los hashes reales y la etiqueta verificada con Git.

## Actualización F31 (02/10/2026)

- **GD-01, GD-02 y GD-03: RESUELTAS.** `CLAUDE.md`, `README.md` y `docs/PROGRESS.md` reflejan el release v1.1 y la línea académica integrada hasta F30, sin borrar este diagnóstico histórico.
- **GD-04, GD-05 y GD-06: ACEPTADAS como historia de cierre.** Los documentos de F26 describen la secuencia previa a ejecutar y conservan valor de auditoría; las referencias Git vigentes se publican en el gobierno activo. No se reescriben retrospectivamente todos los documentos de release.
- **GD-07: NO APLICA.** `main` local y `origin/main` están sincronizados en `59849c3` al iniciar F31.
