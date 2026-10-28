# BORRADOR — NO FIRMADO — SIN AUTORIZACIÓN

## Lista de comprobación de evidencias y procedimiento de verificación del F36-SBX-GATE

> **BORRADOR — NO FIRMADO — SIN AUTORIZACIÓN.** Plantilla de trabajo del 27/10/2026. Ninguna casilla está marcada y ninguna evidencia existe. No es evidencia de ningún criterio ni está en `gate/evidencia/`. Mientras sea un borrador, F36-SBX-GATE = NO SUPERADO y F37-SBX = BLOQUEADA.

## 1. Lista de comprobación por criterio

Cada casilla se marca solo cuando el hecho existe y se ha verificado. El validador comprueba la forma y la coherencia; la sección 2 cubre lo que el validador no puede comprobar.

### Común a los cuatro criterios

- [ ] El candidato del gate está decidido (D-01) y es un commit real, descendiente de `b8892af` y ancestro del HEAD que se valida.
- [ ] Entre el candidato y el árbol validado solo cambian `gate/evidencia/`, `gate/f36sbx_gate_state.json` y la columna Estado de la tabla FG.
- [ ] El estado de Git es fiable: sin `assume-unchanged`, `skip-worktree`, conflictos, operaciones en curso, `refs/replace` ni injertos.
- [ ] Cada registro usa el esquema `f36sbx-team-evidence/v2`, `gate_id = F36-SBX-GATE`, `gate_version = 3`, el `candidate_commit` del estado y un `record_id` `F36SBX-<criterio>-NNN`.
- [ ] `recorded_at` es una fecha real, no anterior a la del commit candidato.
- [ ] Ningún archivo de `gate/evidencia/` es un enlace, está ignorado por Git o queda sin citar.

### FG-02

- [ ] Hay un informe del auditor, escrito por el auditor, con el formato del gate §8.6, dentro de `gate/evidencia/`.
- [ ] El auditor es independiente del candidato y su tipo es uno de los cuatro admitidos.
- [ ] Una persona del equipo verificó la identidad del auditor (sección 2.1).
- [ ] El `verdict` y los `findings_open` son los del dictamen, sin reinterpretarlos; `blocker`, `high` y `medium_requiring_fix` valen 0.
- [ ] El SHA-256 del informe se calculó sobre el archivo que se versiona.

### FG-03

- [ ] El acta de la reunión existe y está confirmada por los tres integrantes (sección 2.2).
- [ ] La lista de EI es cerrada, sin repetidos, solo ALLOWED o CONDITIONAL, e igual a `f37_authorized_ei`.
- [ ] La numeración F36-M01 está decidida.
- [ ] Hay tres votos, uno por integrante, con su fecha y su verificación.

### FG-10

- [ ] La decisión sobre dependencias nuevas es coherente con la lista de FG-03.
- [ ] Si hay dependencias: versión con `==`, licencia admitida, consulta OSV fechada y real, SHA-256 del artefacto descargado y revisor integrante.
- [ ] Tres votos verificados.

### FG-12

Primero se decide el estado de FG-12; las casillas que no correspondan a ese estado se marcan como no pertinentes, nunca se rellenan con un archivo o una votación.

- [ ] **Si no hay ninguna EI CONDITIONAL autorizada:** FG-12 en NO APLICA, con FG-03 en CUMPLE, `evidence` nulo y **sin** `gate/evidencia/FG-12.json` (un archivo sin citar hace fallar la regla GATE). No hay votos propios de FG-12: su condición la fija FG-03, que sí los lleva.
- [ ] **Si hay alguna EI CONDITIONAL autorizada:** FG-12 en CUMPLE, con su registro.
  - [ ] Si se autoriza EI-09: `ei09_decision` vale `CABE_EN_ALCANCE_B`.
  - [ ] Si se autoriza alguna EI CONDITIONAL de alcance C: el ADR sucesor está APROBADO, versionado **dentro del candidato** y con su bloque canónico.
  - [ ] Tres votos verificados (solo en CUMPLE).

### Después de registrar

- [ ] El validador se ejecutó sobre el árbol con la evidencia y su salida se conserva.
- [ ] Si todo está en CUMPLE, existe el incremento sucesor auditado de la decisión D-02. Sin él, la regla GATE de este validador sigue exigiendo NO SUPERADO.

## 2. Procedimiento de verificación

### 2.1 Identidad del auditor (FG-02)

El informe técnico lo emite el auditor; la verificación y el registro los hacen personas del equipo. El auditor puede ser una persona o una sesión automatizada de tipo `sesion_de_auditoria_independiente`.

1. Confirmar con el auditor, por un canal distinto del propio informe, que es el autor del informe y de su veredicto.
2. Si el auditor es una sesión automatizada:
   - dejar constancia de la sesión que lo produjo;
   - comprobar que no es la sesión que implementó o preparó el candidato y que examinó exactamente H;
   - conservar su evidencia completa con un manifiesto de hashes, como en el registro AF6 §7.

   Ni el nombre de la herramienta ni `independent_of_candidate = true` prueban por sí solos la independencia. Una sesión automatizada no es un integrante, un docente ni un revisor externo humano.
3. Si el auditor es una persona, comprobar que no es autora del candidato cuando se declara `integrante_no_autor`.
4. No aceptar como nombre un rol, un marcador ni una composición genérica, aunque el validador lo admita: los residuos AF6-L01 y AF6-L02 muestran que la guardia es estructural.

### 2.2 Votos de los integrantes (FG-03, FG-10 y FG-12)

FG-03 y FG-10 siempre llevan sus tres votos. FG-12 los lleva solo en CUMPLE.

1. Cada integrante emite su voto en persona o por un canal propio y verificable, no por medio de otro integrante. Ninguna sesión automatizada vota ni registra un voto que no ha ocurrido.
2. Quien registra el JSON no puede ser la única fuente de los votos de los demás: cada integrante confirma su voto y su fecha por escrito.
3. El acta firmada o confirmada se conserva fuera de `gate/evidencia/` (que solo admite los archivos del esquema), con su hash citado en el acta o en el commit de registro.
4. Un voto que no se pueda verificar no se registra como `APRUEBA`.

### 2.3 Procedencia y commits

1. Los registros se añaden en un commit propio, después del candidato, que solo toca las rutas de registro.
2. Ese commit no reescribe la historia: nada de amend, rebase ni force push.
3. Antes de integrar, se ejecuta el validador y se conserva su salida. Un fallo se corrige en un commit nuevo; nunca se manipulan las pruebas.
4. Los SHA-256 se calculan con una herramienta estándar sobre los bytes versionados, y el ADR sobre el blob del candidato.

## 3. Condiciones de bloqueo

Cualquiera de estas condiciones mantiene F37-SBX = BLOQUEADA:

| ID | Condición |
|---|---|
| CB-01 | Algún criterio EQUIPO sin CUMPLE (o FG-12 sin el NO APLICA admitido) |
| CB-02 | `candidate_commit` nulo o con cambios fuera de las rutas de registro después de él |
| CB-03 | `f37_authorized_ei` nulo o distinto de `authorized_ei` de FG-03 |
| CB-04 | Un voto que no sea `APRUEBA`, o uno que no se pueda verificar |
| CB-05 | Un informe de FG-02 que no sea del auditor, o con BLOCKER, HIGH o MEDIUM que exija corrección |
| CB-06 | Una EI CONDITIONAL de alcance C sin ADR sucesor APROBADO dentro del candidato |
| CB-07 | Dependencias necesarias sin revisión real o sin aprobar |
| CB-08 | El validador vigente exige NO SUPERADO y no hay incremento sucesor auditado (D-02) |
| CB-09 | Un evento de revocación |
| CB-10 | Cualquier intención de usar datos reales, producción, la G0 real o el alcance C del producto: el gate nunca puede autorizarlos |
