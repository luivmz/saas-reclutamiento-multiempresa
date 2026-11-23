# Casos de uso del SaaS Reclutamiento

Catálogo académico F8: 20 CU y cinco roles humanos. El sistema es comportamiento interno, no un sexto actor humano. Los identificadores técnicos UC-RFxx y los 13 CU históricos agrupados no sustituyen este catálogo.

| ID | Caso de uso | Descripción | Actor según F8 §5 |
| --- | --- | --- | --- |
| CU-01 | Registrar requerimiento de personal | El área registra la necesidad de personal. | ACT-01 Área solicitante |
| CU-02 | Validar y corregir requerimiento | RR. HH. valida u observa; el área corrige y reenvía. | ACT-01 Área solicitante; ACT-02 Recursos Humanos |
| CU-03 | Aprobar o rechazar requerimiento | La Dirección decide sobre el requerimiento validado; el rechazo se notifica. | ACT-03 Aprobador / Dirección |
| CU-04 | Registrar perfil y criterios del puesto | RR. HH. crea la vacante con perfil y criterios ponderados. | ACT-02 Recursos Humanos |
| CU-05 | Configurar y validar vacante | RR. HH. configura la convocatoria; el sistema valida. | ACT-02 Recursos Humanos |
| CU-06 | Publicar vacante | RR. HH. publica la vacante válida en el portal. | ACT-02 Recursos Humanos |
| CU-07 | Gestionar cuenta y acceso | El postulante crea su cuenta e inicia sesión. | ACT-04 Postulante |
| CU-08 | Gestionar perfil y CV | El postulante completa su perfil y carga su CV. | ACT-04 Postulante |
| CU-09 | Registrar postulación | El postulante postula y recibe la confirmación. | ACT-04 Postulante |
| CU-10 | Consultar y revisar postulaciones | Revisa el listado por vacante y el expediente. | ACT-02 Recursos Humanos; ACT-03 Aprobador / Dirección |
| CU-11 | Registrar preselección o descarte | RR. HH. preselecciona o descarta con motivo interno. | ACT-02 Recursos Humanos |
| CU-12 | Gestionar cambio de etapa | RR. HH. cambia la etapa; el postulante recibe el aviso. | ACT-02 Recursos Humanos |
| CU-13 | Programar evaluación | RR. HH. programa la evaluación; se envía la convocatoria. | ACT-02 Recursos Humanos |
| CU-14 | Programar entrevista | RR. HH. programa la entrevista; se envía la convocatoria. | ACT-02 Recursos Humanos |
| CU-15 | Registrar resultados de evaluación y entrevista | El evaluador asignado registra puntajes y resultado. | ACT-05 Evaluador |
| CU-16 | Validar rangos y ponderaciones | Validación incluida por la configuración, el registro de resultados y el ranking. | Sin actor directo: caso incluido |
| CU-17 | Consultar ranking y comparación | Ranking y comparación explicables. No selecciona. | ACT-02 Recursos Humanos; ACT-03 Aprobador / Dirección |
| CU-18 | Registrar decisión final humana | **Decisión humana** del Aprobador / Dirección, con confirmación explícita y justificación. El ranking no elige. | ACT-03 Aprobador / Dirección |
| CU-19 | Registrar selección | RR. HH. aplica la decisión registrada. | ACT-02 Recursos Humanos |
| CU-20 | Cerrar convocatoria y notificar resultado | RR. HH. cierra con selección; cada postulante recibe su resultado. | ACT-02 Recursos Humanos |

Fuente canónica: docs/academico/practica-08/F8_Diagrama_Casos_de_Uso_Colegio_Andino.md. Diagrama existente: docs/academico/powerdesigner/exports/F8_Casos_de_Uso_Academicos.png. No se regeneran modelos sin necesidad.

Vista fuente derivada: [PlantUML](CASOS_USO_SAAS_RECLUTAMIENTO.puml). No sustituye el OOM formal.
