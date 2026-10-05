# Adjuntos de evidencia G0

Carpeta para archivar la **evidencia real** que reciban los registros de F34B: actas firmadas, informes jurídicos, aprobaciones de privacidad, instrumentos respondidos y constancias de aceptación.

**Estado (F34C): 4 adjuntos**, verificados en el [acta de ADR-005 §5](../F34B_Acta_Aprobacion_ADR005.md#5-verificación-de-evidencias-f34c):

| Archivo | Respalda |
|---|---|
| `G0-ADR005-ThreatModel_Fredy_Coronacion_2026-10-04.png` | G0-14 y G0-09 (Coronacion Meza Fredy) |
| `G0-ADR005-ThreatModel_Anthony_Pena_2026-10-04.png` | G0-14 y G0-09 (Peña Arroyo Anthony) |
| `G0-ADR005-ThreatModel_Luis_Vila_2026-10-04_original.png` | G0-14 y G0-09 (Vila Meza Luis Antonio), original histórica |
| `G0-ADR005-ThreatModel_Luis_Vila_2026-10-04.png` | G0-14 y G0-09 (Vila Meza Luis Antonio), confirmación adicional |

Tres son imágenes JPEG con extensión `.png` y la original de Luis Vila es PNG; siguen un patrón de nombre distinto del indicado abajo (OBS-F34C-03 y 04) y se conservan tal como se aportaron. La confirmación de Luis Vila sobrescribió su captura original antes del primer commit; la original se restauró como archivo aparte (OBS-F34C-06). Una confirmación nueva debe tener **otro nombre** de archivo. No hay adjuntos para G0-02, G0-03 ni G0-12. La respuesta de G0-12 recibida en F34D llegó solo como texto y **no se archivó** aquí (OBS-F34D-01).

## Reglas

- Solo se archiva un documento **producido por quien decide** (firma manuscrita escaneada, firma digital, correo institucional exportado o constancia equivalente). Nadie lo redacta ni lo firma por otra persona.
- Nombre del archivo: `G0-xx_<tipo>_<AAAA-MM-DD>.<ext>`, por ejemplo `G0-14_acta-adr005_2026-10-20.pdf`.
- Un registro solo puede salir de PENDIENTE si su columna «Evidencia adjunta/referencia» enlaza un archivo de esta carpeta que exista. `validate_f34b.py` lo comprueba.
- **Sin datos de candidatos ni datos reales de postulantes.** Las únicas personas identificadas en estos documentos son quienes deciden, con su nombre y rol.
- Sin secretos ni credenciales.
- Un adjunto archivado no se reemplaza: una corrección es un adjunto nuevo con su propia fecha.
