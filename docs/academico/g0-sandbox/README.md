# F34E — G0-SBX: puerta de experimentación académica sintética

Puerta **separada** de la G0 real que permite continuar el curso con trabajo sandbox, exclusivamente con datos 100 % sintéticos, sin afirmar que la G0 real esté aprobada.

**Estado:** versión 1 (04/10/2026). **F34E = LISTA PARA AUDITORÍA.**

- **G0-SBX = APROBADA CON RESTRICCIONES** (18/18 criterios SBX).
- **F35-SBX = HABILITADA** (solo sandbox sintético).
- **F35 productiva = BLOQUEADA**; **F36–F40 = BLOQUEADAS**.
- **G0 real = NO APROBADA**; G0-02, G0-03 y G0-12 siguen PENDIENTE EXTERNO.
- **ADR-005 = PROPUESTA** (canónico), con aprobación interna del equipo registrada.
- **Alcance C = BLOQUEADO.** **Los datos reales siguen PROHIBIDOS.**
- RF-23 sigue humana y RF-29 experimental e informativa.

> G0-SBX no sustituye la revisión jurídica, la de privacidad ni la validación institucional, y no cambia el runtime, las migraciones, la interfaz ni el baseline RF-01 a RF-27.

## Documentos

| Archivo | Contenido |
|---|---|
| [F34E_Definicion_G0_SBX.md](F34E_Definicion_G0_SBX.md) | Propósito, límites, estados y regla de decisión |
| [F34E_Matriz_Criterios_G0_SBX.md](F34E_Matriz_Criterios_G0_SBX.md) | SBX-01 a SBX-18 con su verificación automática |
| [F34E_Alcance_Autorizado.md](F34E_Alcance_Autorizado.md) | Qué permite F35-SBX |
| [F34E_Prohibiciones.md](F34E_Prohibiciones.md) | Prohibiciones absolutas |
| [F34E_Relacion_G0_Real_vs_SBX.md](F34E_Relacion_G0_Real_vs_SBX.md) | Las dos puertas y los pendientes reales |
| [F34E_Autorizacion_F35_SBX.md](F34E_Autorizacion_F35_SBX.md) | Condiciones de F35-SBX y criterios de salida hacia trabajo real |
| [F34E_Decision_G0_SBX.md](F34E_Decision_G0_SBX.md) | Decisión, restricciones y revocación |

## Validación

```
python docs/academico/tools/f34e/validate_f34e.py
```

Recalcula los 18 criterios SBX con comprobaciones del repositorio (dataset F34, contrato, árbol de archivos, registros de F34C, Git) y falla si la matriz o la decisión dicen otra cosa. También falla ante:

- una aprobación de G0 sin el sufijo SBX;
- datos reales fuera de la prohibición;
- F35 productiva o F36–F40 fuera de BLOQUEADA;
- scoring, recomendación o alcance C fuera de la prohibición;
- una evidencia externa inventada;
- un criterio SBX que no se cumple mientras G0-SBX figura aprobada.

Solo biblioteca estándar de Python.

## Preparación sobre F34D cerrada (05/10/2026)

- Base fija de F34E: main `9e0fc92adbe563e99a7cb16fdb07aa26f8876d68`.
- Develop publicado de F34D: `8a7e4ba54a02ab543d898f7d50981dbf1d73556f`.
- Commits F34D: A `f68aef551012a59468710d1706431e903106cc03`, B `be0dfeeccbff476d9f8b29c2d06ea0a8fdc20937`, C `2467af90ebc8a35c0aebd51eeff8cfb24d04df6c`.
- Recuperación selectiva del WIP `1b861837355e1fdbdea8b758bcd25c0604143f63`: los ocho documentos de este directorio y `tools/f34e/validate_f34e.py`; no se recuperaron los seis archivos F34D antiguos ni cachés Python. El stash permanece intacto.
- No hay commit ni publicación de F34E. Esta preparación no constituye auditoría independiente ni cierre de fase.

### Snapshot publicado protegido

`validate_f34e.py` comprueba los siguientes SHA-256 contra los documentos actuales. El hash de `validate_f34b.py` se comprueba contra el blob publicado en la base fija, no contra el validador adaptado de F34E.

| Ruta relativa a `docs/academico/` | SHA-256 del cierre F34D |
|---|---|
| `g0-evidence/F34B_Decision_G0.md` | `2f98c21178032ca25cf0e962e207bc588c1e6c82804935f1f7c98015ff588ef3` |
| `g0-evidence/F34B_Matriz_Evidencias_G0.md` | `7aa8f255a26991f82ed4d92e6d22b3278ab16f922cc7b21171f7699c06a8d2a2` |
| `g0-evidence/F34B_Validacion_Necesidad.md` | `82258284aa675348c198bfcffd12042dc483b8c126d477d088b3658f75706053` |
| `g0-evidence/README.md` | `918ea25efc7d98af56425104227272d50754c2734e4cf515460d99dacc84951e` |
| `g0-evidence/adjuntos/README.md` | `4c83d741f3a80d23ddc9260dcaf63ff27d9e266ff3c800a56e2318e1f759e1f3` |
| `tools/f34b/validate_f34b.py` (blob publicado) | `637100ed2ea580178556b812b364e6f027b22b372e09c134f121d5a162fb93a5` |

La única excepción autorizada es adaptar el alcance Git de `validate_f34b.py`: delta estricto en F34B/F34C/F34D; modo post en fases académicas posteriores, con las evidencias publicadas congeladas y las invariantes permanentes vigentes. Los errores Git fallan cerrado. Los negativos de regresión son sintéticos y en memoria; no generan evidencia real ni sustituyen las aprobaciones externas pendientes.

SHA-256 de `tools/f34b/validate_f34b.py` adaptado en F34E: `6a4b66505d493f8ce5e9e1a0d741f7e95dc3e2c9c713e355878eca00819dc8d2`. No reemplaza el hash del blob histórico. El arnés incluye 50 comprobaciones de alcance y 46 controles de la política post-F34E: Git no disponible, fallos de resolución/diff/gobierno, evidencias cerradas alteradas, rutas exactas y estados de gobierno incompatibles.

Excepción de cierre/handoff autorizada: únicamente `CLAUDE.md`, `docs/PROGRESS.md`, `docs/academico/ACADEMIC_BASELINE.md`, `README.md`, `docs/academico/handoff/F34E_MACOS_HANDOFF.md` y, si se crea, `scripts/check-macos-readiness.sh`. No permite otras rutas académicas, archivos Markdown arbitrarios, runtime ni evidencias cerradas. Los documentos de gobierno/handoff deben conservar una sección vigente explícita con G0 real NO APROBADA, F35 productiva BLOQUEADA y restricciones sintéticas; las líneas nuevas no pueden inventar aprobaciones externas.
