# F36-SBX — Autorización, investigación y diseño de la inteligencia sobre evidencia

> Fase F36-SBX, versión 5 (27/10/2026), en la rama `feature/f36-sbx-authorization-design`, desde `main` = `b8892af39a6492d8dd44a36290604efc602380cd`. **No fueron aprobadas para integración** la versión 1 (`06e933e`), por la auditoría independiente AF1; la versión 2 (`2a4e68c`), por AF2; la versión 3 (`ecb22cc`), por la tercera auditoría; ni la versión 4 (`57efbfc`), por la cuarta. Esta versión es la corrección focal de esa cuarta auditoría (AF4) y es **candidata a una quinta auditoría independiente**. Solo documentación, gobierno y validadores documentales: sin ML, sin NLP, sin dependencias nuevas, sin runtime y sin datos reales.

## Estado

- **F36-SBX = EN DISEÑO.** Solo autorización, investigación y diseño documental.
- **F36-SBX-GATE = NO SUPERADO.** FG-02, FG-03, FG-10 y FG-12 están pendientes de actos del equipo. No hay evidencia registrada.
- **F37-SBX = BLOQUEADA.**
- G0 real = NO APROBADA; G0-02, G0-03 y G0-12 = PENDIENTE EXTERNO; G0-09 y G0-14 = CUMPLIDO; G0-SBX = APROBADA CON RESTRICCIONES; ADR-005 = PROPUESTA.
- F35-SBX = CERRADA Y CONGELADA, sin cambios. F36–F40 productivas = BLOQUEADAS. Alcance C = BLOQUEADO. Datos reales = PROHIBIDOS.
- RF-23 sigue siendo la decisión final humana y RF-29 sigue experimental.

## Orden de lectura

1. [Charter](F36SBX_Charter.md): qué autoriza y qué no, prohibiciones, divergencia con el mapa F33 y revocación.
2. [Matriz de capacidades](F36SBX_Matriz_Capacidades.md): 7 ALLOWED, 6 CONDITIONAL y 11 BLOCKED.
3. [Investigación y diseño](F36SBX_Investigacion_Diseno.md): tareas, enfoques, hardware, arquitectura, propuesta de ADR sucesor y hallazgos.
4. [Contrato de evidencia](F36SBX_Contrato_Evidencia.md), su [JSON cerrado](contrato/f36sbx_evidence_contract.json) y su [ejemplo de conformidad](contrato/f36sbx_contract_example.json).
5. [Threat model](F36SBX_Threat_Model.md): TEI-01..TEI-22.
6. [Plan de evaluación](F36SBX_Plan_Evaluacion.md): M-01..M-13 y R-01..R-05, sin resultados.
7. [Gate sucesor](F36SBX_Gate_Sucesor.md), [estado del gate](gate/f36sbx_gate_state.json) y [esquema de la evidencia de equipo](gate/f36sbx_team_evidence_schema.json): FG-01..FG-14 y el plan de entrada a F37-SBX.
8. [Trazabilidad](F36SBX_Trazabilidad.md).
9. [Corrección AF1](F36SBX_Correccion_AF1.md): hallazgos de la primera auditoría, falsos PASS reproducidos y cómo los impide el nuevo oracle.
10. [Corrección AF2](F36SBX_Correccion_AF2.md): bloque canónico del informe y del ADR, cadena de hashes con sello v2, aislamiento entre tenants y cobertura mínima del ejemplo (contrato v3 y esquema de evidencia v2).
11. [Corrección AF3](F36SBX_Correccion_AF3.md): el ADR de FG-12 se lee del blob Git del commit candidato, todo output hereda el contexto canónico de su postulación (contrato v4, REL-15) y los marcadores de identidad se comparan normalizados.
12. [Corrección AF4](F36SBX_Correccion_AF4.md): Git se consulta sobre objetos reales, sin `refs/replace` ni injertos; el árbol de trabajo se compara con el índice por sus bytes, sin confiar en `assume-unchanged` ni en `skip-worktree`; y una identidad tiene que contener al menos una palabra distintiva.

La evidencia de los criterios de equipo (FG-02, FG-03, FG-10 y FG-12) se archivará en `gate/evidencia/`, con el formato de la [sección 8 del gate](F36SBX_Gate_Sucesor.md#8-formato-de-la-evidencia-de-equipo), cuando exista. Hoy esa carpeta no existe.

## Validación

```sh
python -I -B docs/academico/tools/f36sbx/validate_f36sbx.py
python -I -B docs/academico/tools/f36sbx/test_f36sbx.py
python -I -B docs/academico/tools/f36sbx/test_f36sbx_git.py   # con Git real, en clones desechables
python -I -B docs/academico/tools/f36sbx/meta_f36sbx.py hojas
python -I -B docs/academico/tools/f36sbx/meta_f36sbx.py ablaciones   # lento
python -I -B docs/academico/tools/f36sbx/meta_f36sbx.py ablaciones "AF4,identidad"   # ejecución focal
```

Solo usan la biblioteca estándar de Python 3.12. El validador admite las ramas `feature/f36-sbx-authorization-design`, `develop` y `main`, y compara contra la base `b8892af`.

- **Vista de Git.** El validador consulta Git por una única vía, sobre los objetos reales: sin `refs/replace` y sin variables `GIT_*` heredadas. Compara el árbol de trabajo con el índice por sus bytes, sin confiar en `assume-unchanged`, en `skip-worktree` ni en el stat guardado, y no escribe en el repositorio. Falla cerrado ante marcas del índice, conflictos, operaciones en curso, `refs/replace` o injertos. No los corrige: retirarlos es una decisión de quien valida.
- **Pruebas con Git real.** `test_f36sbx_git.py` crea en el directorio temporal del sistema tres repositorios mínimos y tres clones locales compartidos del repositorio. En ellos registra evidencia sintética de prueba, ejecuta el validador completo y ataca la vista de Git; después lo borra todo. Comprueba que el repositorio original no cambia, tampoco su índice.

- **Anclaje.** Tras la integración, el validador sigue pasando mientras `develop` o `main` no tengan, frente a `b8892af`, cambios ajenos a F36-SBX. Un HEAD posterior con otros cambios hace fallar la regla FRZ por diseño, como DG-02 en F35-SBX. En ese caso se valida anclado en esta rama.
- **Gates congelados de F35-SBX.** Sobre esta rama fallan las mismas reglas que sobre `main`, más la de contexto (CTX), porque cada gate solo admite su rama, `develop` y `main`. El cierre global suma además SEM: trata como cambio de gobierno no autorizado cualquier estado nuevo de F36-SBX (GC09 y GC-H5). Siguen valiendo anclados en sus ramas (DG-02).
- **Artefactos cerrados.** El contrato y el esquema de evidencia están fijados por el SHA-256 de su JSON canónico, además de por sus invariantes explícitas. Cambiarlos exige un incremento auditado que actualice también el validador.
