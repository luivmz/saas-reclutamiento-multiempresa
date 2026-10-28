# F36-SBX — Plan de pruebas del sucesor B-01

> Plan del 27/10/2026, en la rama `feature/f36-sbx-gate-transition-h`, para la [especificación del sucesor B-01](F36SBX_Especificacion_Sucesor_B01.md). **No hay implementación ni pruebas nuevas ejecutadas:** este plan fija qué se probará si el equipo autoriza D-02. Las únicas ejecuciones que cita son las de la sección 1, sobre el validador vigente. F36-SBX-GATE = NO SUPERADO y F37-SBX = BLOQUEADA.

## 1. Situación de partida

- **Validador vigente**, sobre el árbol de la preparación y en una rama admitida: 59/0, con 545/0 en memoria. Con Git real, 113/0 y 2 omitidos en Windows, y 115/0 en WSL ([registro AF6](../F36SBX_Auditoria_AF6.md#3-resultados-reproducidos)).
- **Controles positivos E00 y E00b** de [`test_f36sbx.py`](../../tools/f36sbx/test_f36sbx.py): prueban que la función de decisión da SUPERADO con evidencia sintética válida, en memoria. No pasan por la regla GATE completa.
- **La comprobación final de la regla GATE** (`validate_f36sbx.py:2877`, «el gobierno de esta versión exige NO SUPERADO»): **ninguna prueba existente la observa.**
  - Su ablación en memoria se ejecutó el 27/10/2026 contra las dos baterías, en un clon de `88fd3d2` con la rama local `develop`. La línea base no tenía ninguna falla, ni en memoria ni con Git real, y la ablación no hizo fallar ningún caso: **sobrevive**.
  - Es coherente con lo que hay: ninguna prueba registra los cuatro criterios en una fotografía del repositorio, así que ninguna llega a SUPERADO por la regla GATE completa.
  - No es una vulnerabilidad: retirarla sin más no permite superar el gate ([especificación, §2](F36SBX_Especificacion_Sucesor_B01.md#2-comportamiento-actual-verificado)).
  - Sí es un hueco de cobertura (PREP-H-I01, INFO). El sucesor sustituye esa comprobación (especificación, §5.7), y NB-16, NB-18, NB-19, NB-20 y PB-02 la cubrirán con su ablación detectada.

## 2. Reglas del plan

1. **RED antes de GREEN.** Toda prueba nueva se escribe y se ve fallar con el validador vigente antes de implementar. La salida real del RED y del GREEN se registra.
2. **Fixtures sintéticos aislados.**
   - Los controles positivos solo existen en memoria o en clones desechables, sobre un candidato sintético **creado dentro del clon**, nunca sobre H ni sobre otro commit real.
   - Nunca se escriben en `gate/evidencia/` del repositorio, ni se presentan como evidencia auténtica.
   - Usan los nombres literales de los integrantes porque el esquema los exige, pero no representan ningún voto real.
3. **Sin reducir pruebas.** Ninguna prueba existente se elimina ni se debilita para obtener verde. Las que fijan literalmente NO SUPERADO o BLOQUEADA (M02, M03, M09, M11, M12, M13, M17, GR16 y GR25) siguen siendo negativas cuando el resultado derivado es NO SUPERADO. Si alguna tuviera que evolucionar, se justifica caso por caso y se sustituye por una de cobertura igual o mayor.
4. **Cada comprobación nueva tiene una ablación** detectada por un caso pertinente (sección 5).
5. **Windows y Linux.** Las pruebas de enlaces simbólicos reales se ejecutan en WSL. En Windows se informan como omitidas, nunca como correctas.

## 3. Pruebas negativas: el resultado sigue en NO SUPERADO y el validador falla o lo mantiene

| ID | Escenario | Esperado | Batería |
|---|---|---|---|
| NB-01 | Falta FG-02 (PENDIENTE), con el resto válido | NO SUPERADO; un espejo en SUPERADO falla | Memoria y Git |
| NB-02 | Falta FG-03 | NO SUPERADO | Memoria |
| NB-03 | Falta FG-10 | NO SUPERADO | Memoria |
| NB-04 | FG-12 exigible (EI CONDITIONAL autorizada) y en PENDIENTE o NO APLICA | NO SUPERADO | Memoria |
| NB-05 | Un voto `RECHAZA` en FG-03, FG-10 o FG-12 | Evidencia inválida | Memoria |
| NB-06 | Una abstención (`SE_ABSTIENE`) que impide el 3/3 | Evidencia inválida | Memoria |
| NB-07 | Votos duplicados de un integrante, o un integrante ausente | Evidencia inválida | Memoria |
| NB-08 | Auditor con `independent_of_candidate` falso, o de un tipo no admitido | FG-02 inválida | Memoria |
| NB-09 | Evidencia que cita otro SHA distinto del `candidate_commit` del estado | Vínculo inválido | Memoria y Git |
| NB-10 | Informe de FG-02 distinto del registro (veredicto, recuentos o auditor) | FG-02 inválida | Memoria |
| NB-11 | H cambia después de la auditoría: un commit posterior toca el paquete, las herramientas o el gobierno fuera de las líneas canónicas | Vínculo inválido | Git |
| NB-12 | Cambio normativo fuera de las excepciones X1–X5: otra línea del README, de un documento de gobierno o de la prosa del gate | Vínculo inválido | Git |
| NB-13 | Autorización de una EI BLOCKED, o `f37_authorized_ei` distinta de `authorized_ei` (también en el orden) | NO SUPERADO | Memoria |
| NB-14 | Falta una dependencia exigida por EI-10, EI-11 o EI-12, o `new_dependencies` falso con una de ellas autorizada | FG-10 inválida | Memoria |
| NB-15 | Falta el ADR sucesor exigido por una EI CONDITIONAL de alcance C, o el ADR está fuera de H | FG-12 inválida | Memoria y Git |
| NB-16 | Espejos contradictorios: E1 en SUPERADO y E3 en NO SUPERADO, o al revés | Falla de coherencia | Memoria |
| NB-17 | Un archivo de evidencia que es un enlace simbólico, una unión de directorios o un tipo especial | Falla (AF5) | Git (WSL para enlaces) |
| NB-18 | Resultado impuesto: `declared_result` y todos los espejos en SUPERADO sin evidencia válida | Falla; R sigue en NO SUPERADO | Memoria y Git |
| NB-19 | Resultado escondido: evidencia válida y espejos en NO SUPERADO | Falla de coherencia: no se puede declarar menos que lo derivado | Memoria |
| NB-20 | Espejo actualizado a medias: el gobierno cambia, pero el gate o el README no | Falla de coherencia | Memoria y Git |
| NB-21 | Una segunda afirmación del resultado dentro del ámbito de un espejo | Falla | Memoria |
| NB-22 | Afirmación de SUPERADO, o de F37-SBX habilitada, en un documento que no es espejo, con R en SUPERADO | Falla SEM | Memoria |
| NB-23 | H «precocinado»: el estado del gate en H ya trae evidencia, candidato o un resultado distinto de NO SUPERADO | Falla (I-7) | Git |
| NB-24 | Un campo del JSON del estado fuera de X2 cambia después de H (`authorizes`, `cannot_authorize`, `base_commit` o el tipo de un criterio) | Falla (X2) | Git |
| NB-25 | Las herramientas del validador cambian después de H | Vínculo inválido | Git |
| NB-26 | `FG-12.json` presente con FG-12 en NO APLICA | Falla: evidencia sin citar | Memoria y Git |
| NB-27 | FG-12 en NO APLICA con EI-09 autorizada | NO SUPERADO | Memoria |
| NB-28 | FG-10 en NO APLICA | NO SUPERADO (estado no admitido) | Memoria |
| NB-29 | Revocación registrada con espejos en SUPERADO | Falla; R en REVOCADO | Memoria |
| NB-30 | Intentos de modo de excepción: variables de entorno, argumentos o archivos de configuración | Ningún efecto. Comprobación sobre el AST: el único acceso al entorno es `git_env()` y `main()` no lee argumentos | Memoria |
| NB-31 | Ataques ya cubiertos (`refs/replace`, injertos, marcas del índice, caché de stat, enlaces y uniones) repetidos sobre un registro posterior a H | Falla | Git |

## 4. Pruebas positivas, solo con fixtures sintéticos

| ID | Escenario | Esperado |
|---|---|---|
| PB-01 | Estado actual del repositorio: sin evidencia y espejos en NO SUPERADO | 0 fallas; R en NO SUPERADO (sin regresión) |
| PB-02 | Candidato sintético en un clon; registro posterior con FG-02, FG-03 (solo EI ALLOWED) y FG-10 sin dependencias, FG-12 en NO APLICA sin archivo, y los espejos E1–E7 en SUPERADO | 0 fallas; R en SUPERADO |
| PB-03 | Como PB-02, con EI-09 autorizada y FG-12 en CUMPLE con `CABE_EN_ALCANCE_B`, sin ADR | 0 fallas; R en SUPERADO |
| PB-04 | Como PB-02, con una EI CONDITIONAL de alcance C, su ADR APROBADO dentro del candidato sintético y FG-10 coherente | 0 fallas; R en SUPERADO |
| PB-05 | Revocación registrada después de PB-02, con los espejos en REVOCADO y F37-SBX en BLOQUEADA | 0 fallas; R en REVOCADO |
| PB-06 | Derivación, no imposición: en PB-02, cambiar un solo voto a `RECHAZA` hace que el validador falle hasta que los espejos vuelven a NO SUPERADO, y entonces da 0 fallas | Demuestra que el estado sigue a la evidencia |

Ningún control positivo cita H ni un commit real. Todos se borran con su clon.

## 5. Metapruebas

Ablaciones nuevas, cada una detectada por al menos un caso pertinente, y nunca solo por una excepción:

- derivación de los espejos a partir de R;
- `REQUIRED_STATE(R)`;
- `allowed_states()` dependiente del ámbito;
- `FORBIDDEN_CLAIMS` dependiente del ámbito;
- comparación línea a línea de X3–X5;
- comparación campo a campo de X2;
- H sin evidencia;
- la comprobación que sustituye a `:2877`.

Además, se repiten las ablaciones focales de AF4, AF5 y de las identidades, más `meta_f36sbx.py hojas`, si el sucesor toca algo que ejerciten.

## 6. Regresión

- `validate_f36sbx.py`, `test_f36sbx.py` y `test_f36sbx_git.py`, en Windows y en WSL.
- Las familias AF2 a AF6: coherencia del registro, hashes y sello, tenants, contrato, ADR del candidato, contexto canónico, identidades, índice y `refs/replace`, y lectura normativa.
- Controles de congelación (F35, runtime y dependencias), integridad de rutas y archivos, alcance del delta y `git diff --check`.
- Si el incremento incluye la corrección de AF6-L01 y AF6-L02 (decisión D-05), sus reproducciones exactas, `placeholderrelleno` y `auditorfictioոո`, y los 99 nombres plausibles de AF5-L01-P1.

## 7. Criterios de aceptación de la implementación

- Todas las negativas fallan por su motivo y todas las positivas dan 0 fallas, en las dos plataformas.
- Ninguna prueba existente queda debilitada.
- Todas las ablaciones nuevas quedan detectadas.
- El repositorio sigue sin `gate/evidencia/` y con el gate en NO SUPERADO.
- Una auditoría independiente del candidato H confirma todo lo anterior antes de registrar ninguna evidencia.
