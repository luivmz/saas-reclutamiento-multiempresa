# F34B — Recolección y registro de evidencias externas para G0

Registros listos para que terceros y el equipo aporten la **evidencia real** que falta para decidir la puerta G0 de [ADR-005](../diseno-inteligente/F33_ADR_005_G0.md). Parte de los prerequisitos preparados en [F34A](../g0-readiness/README.md).

**Estado:** versión 1 (04/10/2026). **F34B = LISTA PARA AUDITORÍA.** **G0 = NO APROBADA**, **ADR-005 = PROPUESTA** y **F35–F40 = BLOQUEADAS**. RF-23 sigue humana y RF-29 experimental e informativa. **Los datos reales siguen PROHIBIDOS.**

> **Evidencias externas recibidas: 0.** Todos los registros están en PENDIENTE. F34B no contiene firmas, respuestas institucionales ni conclusiones jurídicas, y no cambia el runtime, las migraciones, la interfaz ni el baseline RF-01 a RF-27.

## Documentos

| Archivo | Criterio | Estado |
|---|---|---|
| [F34B_Matriz_Evidencias_G0.md](F34B_Matriz_Evidencias_G0.md) | Los 15 | 9 CUMPLIDO, 1 PARCIAL, 4 PENDIENTE EXTERNO, 1 NO APLICA |
| [F34B_Acta_Aprobacion_ADR005.md](F34B_Acta_Aprobacion_ADR005.md) | G0-14 | PENDIENTE |
| [F34B_Revision_Juridica.md](F34B_Revision_Juridica.md) | G0-02 | PENDIENTE (revisión y evaluación de impacto) |
| [F34B_Privacidad.md](F34B_Privacidad.md) | G0-03 | PENDIENTE |
| [F34B_Validacion_Necesidad.md](F34B_Validacion_Necesidad.md) | G0-12 | PENDIENTE |
| [F34B_Aceptacion_Threat_Model.md](F34B_Aceptacion_Threat_Model.md) | G0-09 | PENDIENTE |
| [F34B_Decision_G0.md](F34B_Decision_G0.md) | Decisión | G0 = NO APROBADA |
| [`adjuntos/`](adjuntos/README.md) | Evidencia real | Vacía |

## Cómo se completa

1. Quien decide produce su documento (acta, informe, aprobación, respuestas o constancia) y lo firma.
2. El documento se archiva en `adjuntos/` con el nombre `G0-xx_<tipo>_<AAAA-MM-DD>.<ext>`.
3. Su fila se actualiza con responsable, rol, fecha, decisión, referencia al adjunto, observaciones y estado `REGISTRADO`.
4. Se actualiza la matriz y se ejecuta `validate_f34b.py`.
5. Solo el equipo, en un commit de gobierno propio, puede registrar un cambio de estado de G0.

## Validación

```
python docs/academico/tools/f34b/validate_f34b.py
```

Falla si una aprobación aparece sin evidencia, si una firma o respuesta no tiene adjunto existente, si G0 se aprueba con pendientes, si el alcance C se habilita, si F35–F40 se desbloquean sin decisión válida o si los datos reales aparecen autorizados. También exige identidad y rol coherentes: tres integrantes distintos del equipo (lista de `CLAUDE.md`), cada uno una sola vez, en el acta de ADR-005 y en la aceptación del threat model; roles jurídicos, de privacidad e institucionales admitidos, firmados por personas ajenas al equipo; y ninguna fecha o decisión sin identidad. Incluye casos negativos y un control positivo en memoria, con integrantes sintéticos y adjuntos simulados que no existen en disco, que demuestra que la regla sí permitiría aprobar con evidencia completa. Solo biblioteca estándar de Python.
