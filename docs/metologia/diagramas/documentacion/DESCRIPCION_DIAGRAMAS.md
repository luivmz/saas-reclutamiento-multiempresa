# Descripción textual de los diagramas

Corte documental: 03/11/2026. Las fuentes citadas se leyeron en modo consulta. Cada bloque es una alternativa textual a la imagen, no certificación institucional ni ejecución nueva del sistema.

## 01. Arquitectura general del SaaS

**ID:** 01. **Archivo:** [01_ARQUITECTURA_GENERAL_SAAS.drawio](<../fuentes/01_ARQUITECTURA_GENERAL_SAAS.drawio>).

**Objetivo:** Separar cliente, monolito, dominio, datos y soporte.

**Fuentes:** [README.md](<../../../../README.md>); [docker-compose.yml](<../../../../docker-compose.yml>); [BelongsToOrganization.php](<../../../../app/Models/Concerns/BelongsToOrganization.php>); [Policies](<../../../../app/Policies>); [MlRiskClient.php](<../../../../app/Services/Ml/MlRiskClient.php>).

**Elementos principales:** Cinco roles humanos, React/TS, Inertia, Laravel, servicios del dominio, PostgreSQL, Redis, worker y extensión ML opcional.

**Relaciones:** Usuario interactúa con frontend; Inertia comunica con el monolito; scopes y Policies condicionan acceso por organización; persistencia y soporte son auxiliares.

**Cómo leerlo:** De cliente a aplicación, luego datos y worker. Los contenedores son agrupaciones de capas, no servicios independientes.

**Advertencias:** Monolito modular; no microservicios. Postulante puede tener cuenta sin organización. RF-29 describe demora operacional y no califica personas.

**Aplicación en Word:** Capítulos 6–7. Insertar selectivamente tras revisión nativa; conservar proporción y pie que indique estado de evidencia.

**Aplicación en PPT:** Arquitectura / stack. Usar vistas generales o una página de detalle; no pegar todas las páginas reducidas.

**Estado de evidencia:** VERIFICADO en archivos; ejecución actual NO CONSULTADA. XML y esquema válidos; revisión visual local de vistas auxiliares realizada. Interpretación por editor diagrams.net pendiente.

**Páginas / lectura textual de elementos:**

### Página 1. Arquitectura y multitenencia

Lienzo 1440 × 1160; 15 vértices editables y 8 conectores.

- CLIENTE · cinco roles humanos; sin selección automática
- [H] Solicitante · RR. HH. · Dirección / Evaluador · Postulante
- [SIS] React + TypeScript / Páginas en el navegador
- APLICACIÓN · monolito modular Laravel; frontend compilado, no microservicio
- [SIS] Inertia / Contrato servidor–cliente
- [SIS] Laravel / Rutas / middleware / Policies
- [PROC] Servicios del dominio / Requerimiento → cierre
- [DAT] organization_id + scope global + Policy (rol y organización) / Aislamiento lógico compartiendo BD; cuenta postulante sin organización
- [DAT] PostgreSQL / Registro de negocio / Auditoría append-only
- [DAT] Redis / Sesión / caché / cola
- [SIS] queue / Worker Laravel / Notificaciones
- [DOC] Extensión opcional RF-29: FastAPI local fuera de Compose; HTTP desde Laravel, con fallback. / Riesgo de demora del proceso, nunca puntuación o selección de personas.

## 02. Despliegue Docker local

**ID:** 02. **Archivo:** [02_DESPLIEGUE_DOCKER.drawio](<../fuentes/02_DESPLIEGUE_DOCKER.drawio>).

**Objetivo:** Documentar servicios, dependencias y persistencia reales.

**Fuentes:** [docker-compose.yml](<../../../../docker-compose.yml>); [Dockerfile](<../../../../docker/php/Dockerfile>); [README.md](<../../../sonarqube/README.md>).

**Elementos principales:** Tres páginas: cuatro servicios base, montajes/red y perfil E2E optativo; Sonar separado.

**Relaciones:** Flechas de la primera página indican prerrequisitos healthy. Las de montajes conectan servicio con almacenamiento; no representan consultas SQL.

**Cómo leerlo:** Leer base antes de volúmenes; consultar E2E solo si se explicará su aislamiento. Puertos son valores por defecto configurables.

**Advertencias:** No se arrancó Docker. Red default implícita, sin driver explícito. Volúmenes anónimos Sonar son evidencia histórica, conservada; no se migraron. ML no pertenece al Compose.

**Aplicación en Word:** Capítulo 10. Insertar selectivamente tras revisión nativa; conservar proporción y pie que indique estado de evidencia.

**Aplicación en PPT:** Docker / infraestructura. Usar vistas generales o una página de detalle; no pegar todas las páginas reducidas.

**Estado de evidencia:** CONFIGURACIÓN VERIFICADA; Sonar/runtime HISTÓRICO. XML y esquema válidos; revisión visual local de vistas auxiliares realizada. Interpretación por editor diagrams.net pendiente.

**Páginas / lectura textual de elementos:**

### Página 1. Servicios base y Sonar separado

Lienzo 1440 × 1120; 12 vértices editables y 3 conectores.

- HOST macOS Apple Silicon · Docker Desktop / Engine
- Compose: reclutamiento · red implícita default (driver no fijado)
- [SIS] app · reclutamiento-php:dev / PHP 8.4.25 / Laravel / APP_PORT (8000) → 8000
- [SIS] queue · misma imagen / queue:work redis / Sin puerto publicado
- [DAT] postgres:17.11-alpine / 127.0.0.1:5432 → 5432 / Puerto configurable
- [DAT] redis:7.4.11-alpine / 127.0.0.1:6379 → 6379 / Puerto configurable
- [QA] SonarQube separado / sonarqube:community / 9000:9000 / H2: evaluación local
- [DOC] No pertenece al / Compose / 4 volúmenes anónimos / conservados / Estado: HISTÓRICO, no / consultado hoy
- [DOC] Healthchecks configurados: app /health; postgres pg_isready; redis ping; queue proceso + queue:monitor. / La flecha indica prerrequisito de arranque, no flujo SQL. No se arrancaron servicios.

### Página 2. Volúmenes y montajes

Lienzo 1440 × 1090; 11 vértices editables y 4 conectores.

- [SIS] app + queue
- [DAT] .:/var/www/html / vendor:/var/www/html/vendor / node_modules:/var/www/html/node_modules
- [SIS] postgres
- [DAT] pgdata:/var/lib/postgresql/data / ./docker/postgres/init → /docker-entrypoint-initdb.d (ro)
- [SIS] redis
- [DAT] redisdata:/data
- [SIS] SonarQube (HISTÓRICO)
- [DAT] Anónimos en /opt/sonarqube/{data,extensions,logs,temp} / IDs exactos conservados en docs/sonarqube/README.md

### Página 3. Perfil E2E opcional

Lienzo 1440 × 1100; 8 vértices editables y 4 conectores.

- [DOC] Perfil e2e desactivado por defecto / app base prepara volúmenes compartidos
- [SIS] app-e2e / APP_ENV=e2e / 127.0.0.1:8001 → 8000
- [SIS] queue-e2e / APP_ENV=e2e / Sin puerto publicado
- [QA] cypress/included:15.3.0 / Electron / baseUrl http://app-e2e:8000
- [DOC] Montajes Cypress: ./cypress y cypress.config.cjs (ro). / E2E documentado: reclutamiento_e2e y Redis DB 2/3 mediante .env.e2e; no se leyó ni creó ese archivo. / No se ejecutan tests, setup ni operaciones destructivas. ML local queda fuera de este Compose.

## 03. Proceso de reclutamiento AS-IS preliminar

**ID:** 03. **Archivo:** [03_PROCESO_RECLUTAMIENTO_AS_IS.drawio](<../fuentes/03_PROCESO_RECLUTAMIENTO_AS_IS.drawio>).

**Objetivo:** Exponer las 14 actividades del modelo institucional preliminar.

**Fuentes:** [F2_Analisis_del_Proceso_Colegio_Andino.md](<../../../academico/practica-02/F2_Analisis_del_Proceso_Colegio_Andino.md>); [F3_Diagrama_BPM_ASIS_Colegio_Andino.md](<../../../academico/practica-03/F3_Diagrama_BPM_ASIS_Colegio_Andino.md>); [F2-F9-traceability.md](<../../../academico/trazabilidad/F2-F9-traceability.md>); [INFORME_FINAL_SAAS_RECLUTAMIENTO.docx](<../../entregables-finales/INFORME_FINAL_SAAS_RECLUTAMIENTO.docx>).

**Elementos principales:** AS-01 a AS-14, cinco carriles humanos, tres páginas de continuidad.

**Relaciones:** Secuencia documental de necesidad, revisión, aprobación, convocatoria, evaluación y decisión; notas delimitan caminos condicionales.

**Cómo leerlo:** Seguir AS-01…AS-14 entre páginas. Carriles vacíos en una página conservan responsabilidades y continuidad.

**Advertencias:** AS-IS PRELIMINAR — PENDIENTE DE VALIDACIÓN INSTITUCIONAL. La continuidad principal supone aprobación; no afirma herramientas, tiempos u organigrama comprobados. Vista tipo swimlane, no BPMN ejecutable.

**Aplicación en Word:** Capítulo 3.1–3.3. Insertar selectivamente tras revisión nativa; conservar proporción y pie que indique estado de evidencia.

**Aplicación en PPT:** AS-IS; usar una página por vez. Usar vistas generales o una página de detalle; no pegar todas las páginas reducidas.

**Estado de evidencia:** PRELIMINAR; fuente documental existente, validación del colegio PENDIENTE. XML y esquema válidos; revisión visual local de vistas auxiliares realizada. Interpretación por editor diagrams.net pendiente.

**Páginas / lectura textual de elementos:**

### Página 1. AS-IS 1 de 3

Lienzo 1500 × 1500; 14 vértices editables y 4 conectores.

- Área solicitante
- RR. HH.
- Dirección
- Postulante
- Evaluadores
- [H] AS-01 Identificar / necesidad
- [H] AS-02 Comunicar / a RR. HH.
- [H] AS-03 Revisar / necesidad
- [H] AS-04 Aprobar o / no aprobar
- [H] AS-05 Definir / perfil

### Página 2. AS-IS 2 de 3

Lienzo 1500 × 1500; 14 vértices editables y 4 conectores.

- Área solicitante
- RR. HH.
- Dirección
- Postulante
- Evaluadores
- [H] AS-06 Difundir / convocatoria
- [H] AS-07 Presentar / postulación y CV
- [H] AS-08 Recibir / postulaciones y CV
- [H] AS-09 Revisar / CV y preseleccionar
- [H] AS-10 Coordinar / evaluaciones y / entrevistas

### Página 3. AS-IS 3 de 3

Lienzo 1500 × 1500; 13 vértices editables y 3 conectores.

- Área solicitante
- RR. HH.
- Dirección
- Postulante
- Evaluadores
- [H] AS-11 Realizar / evaluaciones y / entrevistas
- [H] AS-12 Consolidar / y comparar
- [H] AS-13 Decidir / candidato
- [H] AS-14 Comunicar / resultado

## 04. Proceso TO-BE apoyado por el SaaS

**ID:** 04. **Archivo:** [04_PROCESO_RECLUTAMIENTO_TO_BE.drawio](<../fuentes/04_PROCESO_RECLUTAMIENTO_TO_BE.drawio>).

**Objetivo:** Distinguir tareas humanas, automatizaciones y alcance del proceso.

**Fuentes:** [F5_Modelo_BPM_TOBE_Colegio_Andino.md](<../../../academico/practica-05/F5_Modelo_BPM_TOBE_Colegio_Andino.md>); [F2-F9-traceability.md](<../../../academico/trazabilidad/F2-F9-traceability.md>); [MATRIZ_TRAZABILIDAD_SAAS_RECLUTAMIENTO.xlsx](<../../entregables-finales/MATRIZ_TRAZABILIDAD_SAAS_RECLUTAMIENTO.xlsx>).

**Elementos principales:** TB-01 a TB-29 en continuidad; TB-30 auditoría transversal; cinco actores y carril SaaS.

**Relaciones:** Sistema registra, valida y calcula; humanos evalúan, entrevistan y deciden. La auditoría acompaña estados del proceso.

**Cómo leerlo:** Seis páginas consecutivas, etiquetas TB y notas de aprobación/observación. Evaluación y entrevista se aplican según convocatoria.

**Advertencias:** TO-BE PROPUESTO respaldado por funciones presentes. No incluye contratación, planillas o desempeño. No confundir soporte de ranking con selección automática ni TB-30 con etapa posterior al cierre.

**Aplicación en Word:** Capítulo 3.4. Insertar selectivamente tras revisión nativa; conservar proporción y pie que indique estado de evidencia.

**Aplicación en PPT:** TO-BE; síntesis por tramo. Usar vistas generales o una página de detalle; no pegar todas las páginas reducidas.

**Estado de evidencia:** PROPUESTO como proceso; funciones verificadas, resultados de pruebas HISTÓRICOS. XML y esquema válidos; revisión visual local de vistas auxiliares realizada. Interpretación por editor diagrams.net pendiente.

**Páginas / lectura textual de elementos:**

### Página 1. TO-BE tramo 1 de 6

Lienzo 1500 × 1750; 15 vértices editables y 4 conectores.

- Solicitante
- RR. HH.
- Dirección
- Postulante
- Evaluador
- Sistema
- [H] TB-01 Registrar / el requerimiento de / personal / RF-01
- [H] TB-02 Enviar el / requerimiento a RR. / HH. / RF-02
- [H] TB-03 Revisar el / requerimiento y / validarlo u observarlo / RF-02
- [H] TB-04 Corregir y / reenviar el / requerimiento / observado / RF-02
- [H] TB-05 Aprobar o / rechazar el / requerimiento / RF-03
- [DOC] TB-30 / RF-27 · Auditoría transversal de acciones críticas, no una etapa posterior al cierre. / Rechazo: TB-05→TB-06 y fin; observación: TB-03→TB-04→TB-02. / Evaluación/entrevista y cambios de etapa dependen del caso; esta secuencia es síntesis, no BPMN ejecutable.

### Página 2. TO-BE tramo 2 de 6

Lienzo 1500 × 1750; 15 vértices editables y 4 conectores.

- Solicitante
- RR. HH.
- Dirección
- Postulante
- Evaluador
- Sistema
- [SIS] TB-06 Notificar / el rechazo al área / solicitante / RF-04
- [H] TB-07 Crear la / vacante y registrar el / perfil y los criterios / ponderados / RF-05
- [H] TB-08 Configurar / la vacante / RF-06
- [SIS] TB-09 Validar la / configuración, las / ponderaciones y los / rangos / RF-06,RF-20
- [H] TB-10 Publicar la / vacante en el portal / de empleos / RF-07
- [DOC] TB-30 / RF-27 · Auditoría transversal de acciones críticas, no una etapa posterior al cierre. / Rechazo: TB-05→TB-06 y fin; observación: TB-03→TB-04→TB-02. / Evaluación/entrevista y cambios de etapa dependen del caso; esta secuencia es síntesis, no BPMN ejecutable.

### Página 3. TO-BE tramo 3 de 6

Lienzo 1500 × 1750; 15 vértices editables y 4 conectores.

- Solicitante
- RR. HH.
- Dirección
- Postulante
- Evaluador
- Sistema
- [H] TB-11 Crear la / cuenta e iniciar / sesión / RF-08
- [H] TB-12 Completar / el perfil y cargar el / CV / RF-09
- [H] TB-13 Registrar / la postulación / RF-10
- [SIS] TB-14 / Confirmar la / postulación / RF-11
- [H] TB-15 Revisar las / postulaciones y el / expediente / RF-12
- [DOC] TB-30 / RF-27 · Auditoría transversal de acciones críticas, no una etapa posterior al cierre. / Rechazo: TB-05→TB-06 y fin; observación: TB-03→TB-04→TB-02. / Evaluación/entrevista y cambios de etapa dependen del caso; esta secuencia es síntesis, no BPMN ejecutable.

### Página 4. TO-BE tramo 4 de 6

Lienzo 1500 × 1750; 15 vértices editables y 4 conectores.

- Solicitante
- RR. HH.
- Dirección
- Postulante
- Evaluador
- Sistema
- [H] TB-16 / Preseleccionar o / descartar / RF-13
- [SIS] TB-17 Notificar / el cambio de etapa al / postulante / RF-15
- [H] TB-18 Programar / la evaluación / RF-16
- [SIS] TB-19 Enviar la / convocatoria al / postulante y el aviso / al evaluador / RF-17
- [H] TB-20 Programar / la entrevista / RF-18
- [DOC] TB-30 / RF-27 · Auditoría transversal de acciones críticas, no una etapa posterior al cierre. / Rechazo: TB-05→TB-06 y fin; observación: TB-03→TB-04→TB-02. / Evaluación/entrevista y cambios de etapa dependen del caso; esta secuencia es síntesis, no BPMN ejecutable.

### Página 5. TO-BE tramo 5 de 6

Lienzo 1500 × 1750; 15 vértices editables y 4 conectores.

- Solicitante
- RR. HH.
- Dirección
- Postulante
- Evaluador
- Sistema
- [H] TB-21 Registrar / puntajes, resultado y / observaciones / RF-19
- [SIS] TB-22 Validar / los puntajes dentro / del rango de cada / criterio / RF-20
- [H] TB-23 Actualizar / la etapa de la / postulación (finalista / o descarte) / RF-14
- [SIS] TB-24 Calcular / el ranking ponderado / explicable / RF-21
- [SIS] TB-25 / Presentar la / comparación de / candidatos / RF-22
- [DOC] TB-30 / RF-27 · Auditoría transversal de acciones críticas, no una etapa posterior al cierre. / Rechazo: TB-05→TB-06 y fin; observación: TB-03→TB-04→TB-02. / Evaluación/entrevista y cambios de etapa dependen del caso; esta secuencia es síntesis, no BPMN ejecutable.

### Página 6. TO-BE tramo 6 de 6

Lienzo 1500 × 1750; 14 vértices editables y 3 conectores.

- Solicitante
- RR. HH.
- Dirección
- Postulante
- Evaluador
- Sistema
- [H] TB-26 Registrar / la decisión final / humana / RF-23
- [H] TB-27 Registrar / la selección del / candidato decidido / RF-24
- [H] TB-28 Cerrar la / convocatoria (con / selección) / RF-25
- [SIS] TB-29 Notificar / el resultado a cada / postulante / RF-26
- [DOC] TB-30 / RF-27 · Auditoría transversal de acciones críticas, no una etapa posterior al cierre. / Rechazo: TB-05→TB-06 y fin; observación: TB-03→TB-04→TB-02. / Evaluación/entrevista y cambios de etapa dependen del caso; esta secuencia es síntesis, no BPMN ejecutable.

## 05. Casos de uso académicos del SaaS

**ID:** 05. **Archivo:** [05_CASOS_DE_USO_GENERAL.drawio](<../fuentes/05_CASOS_DE_USO_GENERAL.drawio>).

**Objetivo:** Conservar actores, veinte CU y RF sin ampliar el catálogo.

**Fuentes:** [F8_Diagrama_Casos_de_Uso_Colegio_Andino.md](<../../../academico/practica-08/F8_Diagrama_Casos_de_Uso_Colegio_Andino.md>); [MATRIZ_REQUERIMIENTOS_SISTEMA.xlsx](<../../entregables-finales/MATRIZ_REQUERIMIENTOS_SISTEMA.xlsx>); [CASOS_USO_SAAS_RECLUTAMIENTO.md](<../../entregables-finales/CASOS_USO_SAAS_RECLUTAMIENTO.md>).

**Elementos principales:** CU-01…CU-20 académicos en cinco páginas, actores existentes y asociaciones con RF.

**Relaciones:** Asociaciones actor–caso sin flechas causales; CU-16 es incluido por CU-05/CU-15/CU-17, descrito en nota para evitar conectores cruzados.

**Cómo leerlo:** Abrir cada página por actor/agrupación. Revisar etiquetas RF y notas de inclusión; 20 CU únicos en todo el archivo.

**Advertencias:** No mezcla el catálogo académico de 20 CU con otros catálogos UML. RF-27 es transversal: no inventa CU-21. Los roles no constituyen organigrama institucional validado.

**Aplicación en Word:** Capítulo 4.4. Insertar selectivamente tras revisión nativa; conservar proporción y pie que indique estado de evidencia.

**Aplicación en PPT:** Actores y CU; seleccionar página. Usar vistas generales o una página de detalle; no pegar todas las páginas reducidas.

**Estado de evidencia:** CATÁLOGO ACADÉMICO VERIFICADO; aceptación institucional PENDIENTE. XML y esquema válidos; revisión visual local de vistas auxiliares realizada. Interpretación por editor diagrams.net pendiente.

**Páginas / lectura textual de elementos:**

### Página 1. Requerimientos y vacantes

Lienzo 1550 × 1220; 14 vértices editables y 7 conectores.

- LÍMITE DEL SISTEMA · Requerimientos y vacantes
- ACT-01 / Área / solicitante
- ACT-02 / RR. HH.
- ACT-03 / Aprobador / / Dirección
- CU-01 / Registrar requerimiento de personal / RF-01
- CU-02 / Validar y corregir requerimiento / RF-02
- CU-03 / Aprobar o rechazar requerimiento / RF-03, RF-04
- CU-04 / Registrar perfil y criterios del puesto / RF-05
- CU-05 / Configurar y validar vacante / RF-06, RF-20
- CU-06 / Publicar vacante / RF-07

### Página 2. Cuenta y postulación

Lienzo 1550 × 1220; 9 vértices editables y 3 conectores.

- LÍMITE DEL SISTEMA · Cuenta y postulación
- ACT-04 / Postulante
- CU-07 / Gestionar cuenta y acceso / RF-08
- CU-08 / Gestionar perfil y CV / RF-09
- CU-09 / Registrar postulación / RF-10, RF-11

### Página 3. Seguimiento

Lienzo 1550 × 1220; 10 vértices editables y 4 conectores.

- LÍMITE DEL SISTEMA · Seguimiento
- ACT-02 / RR. HH.
- ACT-03 / Aprobador / / Dirección
- CU-10 / Consultar y revisar postulaciones / RF-12
- CU-11 / Registrar preselección o descarte / RF-13
- CU-12 / Gestionar cambio de etapa / RF-14, RF-15

### Página 4. Evaluación y entrevista

Lienzo 1550 × 1220; 10 vértices editables y 3 conectores.

- LÍMITE DEL SISTEMA · Evaluación y entrevista
- ACT-02 / RR. HH.
- ACT-05 / Evaluador
- CU-13 / Programar evaluación / RF-16, RF-17
- CU-14 / Programar entrevista / RF-18
- CU-15 / Registrar resultados de evaluación y / entrevista / RF-19

### Página 5. Comparación y decisión

Lienzo 1550 × 1220; 12 vértices editables y 6 conectores.

- LÍMITE DEL SISTEMA · Comparación y decisión
- ACT-02 / RR. HH.
- ACT-03 / Aprobador / / Dirección
- CU-16 / Validar rangos y ponderaciones / RF-20
- CU-17 / Consultar ranking y comparación / RF-21, RF-22
- CU-18 / Registrar decisión final humana / RF-23
- CU-19 / Registrar selección / RF-24
- CU-20 / Cerrar convocatoria y notificar / resultado / RF-25, RF-26
- [DOC] Referencias a otras páginas: / CU-05 y CU-15 incluyen CU-16 / Sin nuevo actor ni nuevo CU

## 06. Mapa funcional de módulos reales

**ID:** 06. **Archivo:** [06_MAPA_MODULOS_SAAS.drawio](<../fuentes/06_MAPA_MODULOS_SAAS.drawio>).

**Objetivo:** Mostrar el recorrido funcional y capacidades transversales.

**Fuentes:** [MATRIZ_REQUERIMIENTOS_SISTEMA.xlsx](<../../entregables-finales/MATRIZ_REQUERIMIENTOS_SISTEMA.xlsx>); [MATRIZ_TRAZABILIDAD_SAAS_RECLUTAMIENTO.xlsx](<../../entregables-finales/MATRIZ_TRAZABILIDAD_SAAS_RECLUTAMIENTO.xlsx>); [routes](<../../../../routes>); [Services](<../../../../app/Services>); [README.md](<../../../../README.md>).

**Elementos principales:** Requerimientos, vacantes, cuentas/perfil/CV, postulaciones, evaluación, entrevistas, ranking, decisión/cierre, notificaciones y auditoría.

**Relaciones:** Agrupación funcional de capacidades; decisión humana recibe información del sistema y registra un resultado justificado.

**Cómo leerlo:** De servicios de entrada al soporte de decisión y cierre; leer notas que distinguen funciones de módulos comerciales.

**Advertencias:** No inventa banco de talentos independiente, BI, contratación, planillas ni CRUD comercial de organizaciones. Multiempresa es una restricción transversal.

**Aplicación en Word:** Capítulos 4–6. Insertar selectivamente tras revisión nativa; conservar proporción y pie que indique estado de evidencia.

**Aplicación en PPT:** Alcance y módulos. Usar vistas generales o una página de detalle; no pegar todas las páginas reducidas.

**Estado de evidencia:** FUNCIONES VERIFICADAS; agrupación de presentación PROPUESTA. XML y esquema válidos; revisión visual local de vistas auxiliares realizada. Interpretación por editor diagrams.net pendiente.

**Páginas / lectura textual de elementos:**

### Página 1. Flujo y capacidades transversales

Lienzo 1440 × 1130; 12 vértices editables y 6 conectores.

- [PROC] Requerimientos / RF-01–04
- [PROC] Vacantes / RF-05–07, RF-20
- [PROC] Cuenta / perfil / CV / RF-08–09
- [PROC] Postulaciones y seguimiento / RF-10–15
- [PROC] Evaluación y entrevista / RF-16–20
- [PROC] Ranking / comparación / RF-21–22
- [H] Decisión humana, registro de selección y cierre / RF-23–26 · Dirección decide; RR. HH. registra y cierra
- [DOC] Transversales: multitenencia lógica · usuarios / roles / Policies · notificaciones · auditoría RF-27 / No se representa un CRUD comercial de organizaciones ni una selección automática.
- [DOC] Soporte UI: DataTable y SidebarMenuSkeleton. RF-29: consulta operacional experimental y opcional, fuera de RF-01–27.

## 07. Desarrollo colaborativo humano IA

**ID:** 07. **Archivo:** [07_METODOLOGIA_DESARROLLO_IA.drawio](<../fuentes/07_METODOLOGIA_DESARROLLO_IA.drawio>).

**Objetivo:** Distribuir actividades, controles y responsabilidad de aceptación.

**Fuentes:** [METODOLOGIA_DESARROLLO_ASISTIDO_IA.md](<../../investigacion-ia/METODOLOGIA_DESARROLLO_ASISTIDO_IA.md>); [AGENTS.md](<../../../../AGENTS.md>); [MATRIZ_DOBLE_ENTRADA_METODOLOGIA_IA.xlsx](<../../entregables-finales/MATRIZ_DOBLE_ENTRADA_METODOLOGIA_IA.xlsx>).

**Elementos principales:** Doce etapas de la metodología reconstruida, dos páginas; categorías humano, IA, colaboración, QA y artefactos.

**Relaciones:** Contexto y especificación preceden generación asistida; revisión, pruebas y reevaluación condicionan aceptación humana y registro.

**Cómo leerlo:** Seguir el orden del Markdown metodológico y la continuidad entre páginas. Etiquetas explican participación; color no es el único canal.

**Advertencias:** Reconstrucción académica, no declaración de adopción prospectiva. La matriz desagrega 13 etapas analíticas y el Markdown agrupa 12; se conserva la secuencia canónica sin alterar matrices. No hay adopción causal demostrada.

**Aplicación en Word:** Capítulo 5.6. Insertar selectivamente tras revisión nativa; conservar proporción y pie que indique estado de evidencia.

**Aplicación en PPT:** Metodología / intervención. Usar vistas generales o una página de detalle; no pegar todas las páginas reducidas.

**Estado de evidencia:** METODOLOGÍA PROPUESTA/RECONSTRUIDA; evidencias históricas parciales. XML y esquema válidos; revisión visual local de vistas auxiliares realizada. Interpretación por editor diagrams.net pendiente.

**Páginas / lectura textual de elementos:**

### Página 1. Etapas 1–6

Lienzo 1440 × 1100; 10 vértices editables y 5 conectores.

- [H] 1 Necesidad / Humano delimita; IA identifica faltantes / Salida: Problema preliminar
- [PROC] 2 Análisis / Contrastar docs y código / Salida: Cadena AS→P→S→TB
- [PROC] 3 Especificación / Contratos y criterios verificables / Salida: RF / RNF / CU
- [PROC] 4 Planificación / Humano autoriza; IA divide alcance / Salida: Rama y plan acotado
- [IA] 5 Asistencia / IA propone; humano revisa / Salida: Parche candidato
- [H] 6 Revisión / Responsabilidad humana; diff y tenant / Salida: Cambio revisado
- [DOC] ACTIVIDAD HUMANA [H] · IA [IA] · COLABORATIVA [PROC] · CONTROL [QA] · ARTEFACTO [DOC] / La aceptación y la publicación siguen siendo humanas. Si un control falla, volver a asistencia/revisión y verificar. / La matriz desagrega estas 12 etapas en 13 filas: separa generación/implementación y documentación/evidencia.

### Página 2. Etapas 7–12

Lienzo 1440 × 1100; 10 vértices editables y 5 conectores.

- [QA] 7 Verificación / Tests, assertions, tipos y regresión / Salida: Salidas fechadas
- [QA] 8 Análisis estático / Código y cobertura real importada / Salida: Gate / issues / medidas
- [PROC] 9 Corrección / Cambio mínimo revisado / Salida: FIXED comprobado por regla
- [QA] 10 Reevaluación / Repetir y explicar denominadores / Salida: Comparación V1/V2
- [DOC] 11 Evidencia / Conservar logs, capturas y baseline / Salida: Reporte / matrices
- [DOC] 12 Trazabilidad / Enlazar RF→código→test→métrica / Salida: Entrega revisable
- [DOC] ACTIVIDAD HUMANA [H] · IA [IA] · COLABORATIVA [PROC] · CONTROL [QA] · ARTEFACTO [DOC] / La aceptación y la publicación siguen siendo humanas. Si un control falla, volver a asistencia/revisión y verificar. / La matriz desagrega estas 12 etapas en 13 filas: separa generación/implementación y documentación/evidencia.

## 08. AI-DLC como marco de contraste

**ID:** 08. **Archivo:** [08_AI_DLC_VS_METODOLOGIA_PROYECTO.drawio](<../fuentes/08_AI_DLC_VS_METODOLOGIA_PROYECTO.drawio>).

**Objetivo:** Comparar sin convertir correspondencias en adopción histórica.

**Fuentes:** [AI-Driven Development Lifecycle (1) (1).pdf](<../../platillas/AI-Driven Development Lifecycle (1) (1).pdf>); [ANALISIS_AI_DLC_Y_REGISTRO.md](<../../fuentes/ANALISIS_AI_DLC_Y_REGISTRO.md>); [MATRIZ_DOBLE_ENTRADA_METODOLOGIA_IA.xlsx](<../../entregables-finales/MATRIZ_DOBLE_ENTRADA_METODOLOGIA_IA.xlsx>); [METODOLOGIA_DESARROLLO_ASISTIDO_IA.md](<../../investigacion-ia/METODOLOGIA_DESARROLLO_ASISTIDO_IA.md>).

**Elementos principales:** Inception, Construction, Operations, Human Oversight; Intent, Unit y Bolt en segunda página.

**Relaciones:** Comparación de cada concepto con evidencia documental del SaaS mediante correspondencia alta, parcial o no demostrada.

**Cómo leerlo:** Leer columna AWS, nivel de correspondencia y columna de práctica; la flecha compara, no certifica adopción.

**Advertencias:** AI-DLC COMO MARCO DE CONTRASTE. White paper técnico de Raja SP/AWS, no artículo peer reviewed adicional. No se inventan rituales Mob ni Intents/Units/Bolts históricos. Operations tiene correspondencia baja/parcial.

**Aplicación en Word:** Capítulo 5.7. Insertar selectivamente tras revisión nativa; conservar proporción y pie que indique estado de evidencia.

**Aplicación en PPT:** Contraste AI-DLC. Usar vistas generales o una página de detalle; no pegar todas las páginas reducidas.

**Estado de evidencia:** CONTRASTE PROPUESTO; aplicación formal histórica NO DEMOSTRADA. XML y esquema válidos; revisión visual local de vistas auxiliares realizada. Interpretación por editor diagrams.net pendiente.

**Páginas / lectura textual de elementos:**

### Página 1. Fases y control

Lienzo 1600 × 1180; 14 vértices editables y 4 conectores.

- [IA] Inception / Propósito → requisitos/unidades
- [PROC] RF/RNF y contexto del SaaS
- [IA] Construction / Diseño → código → pruebas
- [PROC] Código, revisión y QA históricos
- [IA] Operations / Despliegue y observabilidad supervisados
- [PROC] Compose local; sin operación IA productiva
- [IA] Human Oversight / Validación y decisión humanas
- [PROC] Guardian y aceptación humana como regla

### Página 2. Artefactos y límites

Lienzo 1600 × 1180; 14 vértices editables y 4 conectores.

- [IA] Intent / Propósito de alto nivel
- [PROC] Objetivos OM como analogía; sin registro formal Intent
- [IA] Unit / Trabajo cohesivo y desplegable
- [PROC] Módulos de monolito; no unidad independiente / acreditada
- [IA] Bolt / Iteración acotada en horas/días
- [PROC] Fases/commits no prueban tiempos ni Bolts
- [IA] Contexto y trazabilidad / Artefactos persistidos y enlazados
- [PROC] Docs/Git/RF→código→test; prompts incompletos

## 09. Trazabilidad académica de extremo a extremo

**ID:** 09. **Archivo:** [09_TRAZABILIDAD_ACADEMICA.drawio](<../fuentes/09_TRAZABILIDAD_ACADEMICA.drawio>).

**Objetivo:** Explicar la cadena y un ejemplo real sin expandir todos los RF.

**Fuentes:** [MATRIZ_TRAZABILIDAD_ACADEMICA.xlsx](<../../entregables-finales/MATRIZ_TRAZABILIDAD_ACADEMICA.xlsx>); [F2-F9-traceability.md](<../../../academico/trazabilidad/F2-F9-traceability.md>); [MATRIZ_REQUERIMIENTOS_SISTEMA.xlsx](<../../entregables-finales/MATRIZ_REQUERIMIENTOS_SISTEMA.xlsx>); [MATRIZ_ARTICULOS_IA.xlsx](<../../investigacion-ia/MATRIZ_ARTICULOS_IA.xlsx>).

**Elementos principales:** Cadena conceptual y ejemplo RF-01 con P1/P2, OM-01, AS-01/02, TB-01, CU-01, FUN-001, código y prueba.

**Relaciones:** Vincula problemas preliminares y objetivos documentales con requisitos, funciones, evidencia y artículos de soporte metodológico.

**Cómo leerlo:** Primera página explica cadena; segunda instancia un caso real. Consultar matriz completa para el resto de relaciones.

**Advertencias:** Artículo respalda ingeniería/testing, no confirma hechos del colegio ni causa resultados del SaaS. La métrica agregada no acredita cumplimiento individual del RF.

**Aplicación en Word:** Capítulos 3–5 y anexos. Insertar selectivamente tras revisión nativa; conservar proporción y pie que indique estado de evidencia.

**Aplicación en PPT:** Trazabilidad resumida. Usar vistas generales o una página de detalle; no pegar todas las páginas reducidas.

**Estado de evidencia:** VÍNCULOS DOCUMENTALES VERIFICADOS; problema institucional PRELIMINAR. XML y esquema válidos; revisión visual local de vistas auxiliares realizada. Interpretación por editor diagrams.net pendiente.

**Páginas / lectura textual de elementos:**

### Página 1. Cadena conceptual

Lienzo 1560 × 1200; 17 vértices editables y 12 conectores.

- [PROC] Problema
- [PROC] Objetivo
- [PROC] AS-IS
- [PROC] TO-BE
- [PROC] Requisito
- [PROC] Caso de uso
- [PROC] Módulo
- [PROC] Función
- [SIS] Código
- [QA] Prueba
- [QA] Métrica
- [DOC] Evidencia
- [DOC] Artículo científico

### Página 2. Ejemplo RF-01

Lienzo 1560 × 1230; 16 vértices editables y 12 conectores.

- [PROC] P1 / P2 / Problemas preliminares
- [PROC] OM-01 / Centralizar información
- [PROC] AS-01 / AS-02 / Necesidad y comunicación
- [PROC] TB-01 / Registrar requerimiento
- [PROC] RF-01 / Registro de necesidad
- [PROC] CU-01 / Registrar requerimiento
- [PROC] PR-01 / Requerimiento y aprobación
- [PROC] FUN-001 / JobRequestWorkflow::register
- [SIS] Código / app/Services/JobRequests/Job / RequestWorkflow.php
- [QA] Prueba / JobRequestWorkflowTest::test_ / rf01_*
- [QA] Métrica / Assertions / resultado histórico; / sin coverage individual
- [DOC] Evidencia / F2–F9 + matriz académica
- [DOC] ART-01 / ART-10 / Marco SE/testing; no confirma / hechos del colegio

## 10. Jerarquía de procesos adoptada para la trazabilidad

**ID:** 10. **Archivo:** [10_JERARQUIA_PROCESOS_FUNCIONES.drawio](<../fuentes/10_JERARQUIA_PROCESOS_FUNCIONES.drawio>).

**Objetivo:** Desplegar las agrupaciones propuestas y todos sus vínculos actividad–función.

**Fuentes:** [MATRIZ_TRAZABILIDAD_SAAS_RECLUTAMIENTO.xlsx](<../../entregables-finales/MATRIZ_TRAZABILIDAD_SAAS_RECLUTAMIENTO.xlsx>); [MATRIZ_REQUERIMIENTOS_SISTEMA.xlsx](<../../entregables-finales/MATRIZ_REQUERIMIENTOS_SISTEMA.xlsx>).

**Elementos principales:** Dos macroprocesos, siete procedimientos y siete páginas de detalle con 33 pares actividad–función.

**Relaciones:** MP-01 agrupa PR-01…05 y PR-07; MP-02 agrupa PR-06. Cada detalle conecta ACT con FUN y RF/candidato asociado.

**Cómo leerlo:** Usar vista general para explicar la jerarquía y páginas PR para auditar cada vínculo. La pertenencia se representa por contención nativa.

**Advertencias:** Agrupación PROPUESTA; no obligación literal de cuatro niveles en ISO 9001. RF-29 sigue experimental fuera de los 27 RF. Soporte UI no se convierte en macroproceso institucional confirmado.

**Aplicación en Word:** Capítulo 3 / anexo de procesos. Insertar selectivamente tras revisión nativa; conservar proporción y pie que indique estado de evidencia.

**Aplicación en PPT:** Usar solo vista general; detalles en anexos. Usar vistas generales o una página de detalle; no pegar todas las páginas reducidas.

**Estado de evidencia:** 2/7/33/33 VERIFICADOS contra matriz; denominación macroprocedimental PROPUESTA. XML y esquema válidos; revisión visual local de vistas auxiliares realizada. Interpretación por editor diagrams.net pendiente.

**Páginas / lectura textual de elementos:**

### Página 1. Vista general

Lienzo 1600 × 1140; 13 vértices editables y 0 conectores.

- MP-01 · Gestión del reclutamiento en el sistema
- MP-02 · Soporte transversal de interfaz
- [PROC] PR-01 / Requerimiento y aprobación
- [PROC] PR-02 / Configuración y publicación de vacantes
- [PROC] PR-03 / Cuenta y postulación
- [PROC] PR-04 / Evaluaciones y seguimiento
- [PROC] PR-05 / Comparación, decisión humana y cierre
- [PROC] PR-07 / Consulta operacional experimental
- [PROC] PR-06 / Componentes transversales de interfaz

### Página 2. PR-01 · detalle

Lienzo 1760 × 1130; 16 vértices editables y 6 conectores.

- [PROC] ACT-001 / TB-01 Registrar el requerimiento de personal
- [SIS] FUN-001 · JobRequestWorkflow::register / RF-01
- [PROC] ACT-002 / TB-02 Enviar el requerimiento a RR. HH.
- [SIS] FUN-002 · JobRequestWorkflow::submit / RF-02
- [PROC] ACT-003 / TB-03 Revisar el requerimiento y validarlo u observarlo
- [SIS] FUN-003 · JobRequestWorkflow::validate / RF-02
- [PROC] ACT-004 / TB-04 Corregir y reenviar el requerimiento observado
- [SIS] FUN-004 · JobRequestWorkflow::correct / RF-02
- [PROC] ACT-005 / TB-05 Aprobar o rechazar el requerimiento
- [SIS] FUN-005 · JobRequestWorkflow::approve / RF-03
- [PROC] ACT-006 / TB-06 Notificar el rechazo al área solicitante
- [SIS] FUN-006 · JobRequestRejectedNotification::message / RF-04

### Página 3. PR-02 · detalle

Lienzo 1760 × 960; 12 vértices editables y 4 conectores.

- [PROC] ACT-007 / TB-07 Crear la vacante y registrar el perfil y los criterios ponderados
- [SIS] FUN-007 · VacancyService::create / RF-05
- [PROC] ACT-008 / TB-08 Configurar la vacante
- [SIS] FUN-008 · VacancyService::update / RF-06
- [PROC] ACT-009 / TB-09 Validar la configuración, las ponderaciones y los rangos
- [SIS] FUN-009 · VacancyValidator::issues / RF-06,RF-20
- [PROC] ACT-010 / TB-10 Publicar la vacante en el portal de empleos
- [SIS] FUN-010 · VacancyService::publish / RF-07

### Página 4. PR-03 · detalle

Lienzo 1760 × 960; 12 vértices editables y 4 conectores.

- [PROC] ACT-011 / TB-11 Crear la cuenta e iniciar sesión
- [SIS] FUN-011 · CreateNewUser::create / RF-08
- [PROC] ACT-012 / TB-12 Completar el perfil y cargar el CV
- [SIS] FUN-012 · CandidateCvRequest::rules / RF-09
- [PROC] ACT-013 / TB-13 Registrar la postulación
- [SIS] FUN-013 · ApplicationService::apply / RF-10
- [PROC] ACT-014 / TB-14 Confirmar la postulación
- [SIS] FUN-014 · ApplicationReceivedNotification::message / RF-11

### Página 5. PR-04 · detalle

Lienzo 1760 × 1490; 22 vértices editables y 9 conectores.

- [PROC] ACT-015 / TB-15 Revisar las postulaciones y el expediente
- [SIS] FUN-015 · VacancyApplicationController::__invoke / RF-12
- [PROC] ACT-016 / TB-16 Preseleccionar o descartar
- [SIS] FUN-016 · ApplicationStageService::shortlist / RF-13
- [PROC] ACT-017 / TB-17 Notificar el cambio de etapa al postulante
- [SIS] FUN-017 · ApplicationStageChangedNotification::message / RF-15
- [PROC] ACT-018 / TB-18 Programar la evaluación
- [SIS] FUN-018 · AssessmentScheduler::scheduleEvaluation / RF-16
- [PROC] ACT-019 / TB-19 Enviar la convocatoria al postulante y el aviso al evaluador
- [SIS] FUN-019 · AssessmentConvocationNotification::message / RF-17
- [PROC] ACT-020 / TB-20 Programar la entrevista
- [SIS] FUN-020 · AssessmentScheduler::scheduleInterview / RF-18
- [PROC] ACT-021 / TB-21 Registrar puntajes, resultado y observaciones
- [SIS] FUN-021 · AssessmentResultRecorder::recordEvaluation / RF-19
- [PROC] ACT-022 / TB-22 Validar los puntajes dentro del rango de cada criterio
- [SIS] FUN-022 · ScoreSheetValidator::validate / RF-20
- [PROC] ACT-023 / TB-23 Actualizar la etapa de la postulación (finalista o descarte)
- [SIS] FUN-023 · ApplicationStageService::moveTo / RF-14

### Página 6. PR-05 · detalle

Lienzo 1760 × 1250; 18 vértices editables y 7 conectores.

- [PROC] ACT-024 / TB-24 Calcular el ranking ponderado explicable
- [SIS] FUN-024 · RankingService::rank / RF-21
- [PROC] ACT-025 / TB-25 Presentar la comparación de candidatos
- [SIS] FUN-025 · VacancyComparisonController::__invoke / RF-22
- [PROC] ACT-026 / TB-26 Registrar la decisión final humana
- [SIS] FUN-026 · FinalDecisionService::decide / RF-23
- [PROC] ACT-027 / TB-27 Registrar la selección del candidato decidido
- [SIS] FUN-027 · SelectionRegistrationService::register / RF-24
- [PROC] ACT-028 / TB-28 Cerrar la convocatoria (con selección)
- [SIS] FUN-028 · VacancyClosureService::close / RF-25
- [PROC] ACT-029 / TB-29 Notificar el resultado a cada postulante
- [SIS] FUN-029 · ProcessResultNotification::message / RF-26
- [PROC] ACT-030 / TB-30 Registrar la auditoría de las acciones críticas
- [SIS] FUN-030 · AuditLogger::record / RF-27

### Página 7. PR-06 · detalle

Lienzo 1760 × 960; 8 vértices editables y 2 conectores.

- [PROC] ACT-031 / DataTable
- [SIS] FUN-031 · DataTable / Transversal UI
- [PROC] ACT-032 / SidebarMenuSkeleton
- [SIS] FUN-032 · SidebarMenuSkeleton / Transversal UI

### Página 8. PR-07 · detalle

Lienzo 1760 × 960; 6 vértices editables y 1 conectores.

- [PROC] ACT-033 / OperationalRiskCard
- [SIS] FUN-033 · OperationalRiskCard / RF-29 EXPERIMENTAL, fuera de baseline

## 11. Estrategia de pruebas y controles de calidad

**ID:** 11. **Archivo:** [11_ESTRATEGIA_PRUEBAS_CALIDAD.drawio](<../fuentes/11_ESTRATEGIA_PRUEBAS_CALIDAD.drawio>).

**Objetivo:** Separar pruebas funcionales, análisis estático y cobertura real.

**Fuentes:** [tests](<../../../../tests>); [cypress](<../../../../cypress>); [composer.json](<../../../../composer.json>); [package.json](<../../../../package.json>); [REPORTE_EVIDENCIAS_V1_SONARQUBE.md](<../../../sonarqube/evidencias/v1/REPORTE_EVIDENCIAS_V1_SONARQUBE.md>); [REPORTE_RESULTADOS_V2_PRELIMINAR.md](<../../../sonarqube/evidencias/v2/REPORTE_RESULTADOS_V2_PRELIMINAR.md>).

**Elementos principales:** PHPUnit Unit/Feature, Vitest componentes, Cypress E2E, Sonar y ciclo de QA; controles complementarios.

**Relaciones:** Implementación lleva a pruebas, interpretación, corrección, reejecución y evidencia. PCOV/PHPUnit producen Clover que Sonar importa.

**Cómo leerlo:** Distinguir pruebas de ejecución, análisis estático y formato. Leer deuda histórica sin sumarla a Issues Sonar.

**Advertencias:** No suites ni scanner ejecutados en esta tarea. Cypress no se ejecutó en sesión Sonar aunque haya evidencia histórica de otras fases. Existencia de tests no demuestra TDD universal.

**Aplicación en Word:** Capítulos 11–13. Insertar selectivamente tras revisión nativa; conservar proporción y pie que indique estado de evidencia.

**Aplicación en PPT:** Testing / calidad. Usar vistas generales o una página de detalle; no pegar todas las páginas reducidas.

**Estado de evidencia:** HERRAMIENTAS VERIFICADAS; resultados HISTÓRICOS. XML y esquema válidos; revisión visual local de vistas auxiliares realizada. Interpretación por editor diagrams.net pendiente.

**Páginas / lectura textual de elementos:**

### Página 1. Herramientas y ciclo

Lienzo 1600 × 1160; 14 vértices editables y 5 conectores.

- [QA] PHPUnit / Unit + Feature / integración / Reglas y acceso cross-tenant
- [QA] Vitest / Pruebas de componentes React / / TS / Assertions y tipos son controles / distintos
- [QA] Cypress / E2E con BD descartable aislada / NO EJECUTADO en sesión Sonar
- [QA] SonarQube / Análisis estático y métricas / Importa cobertura; no la genera
- [SIS] Implementación
- [QA] Pruebas y assertions
- [H] Interpretar resultados
- [PROC] Corrección mínima
- [QA] Reejecución
- [DOC] Evidencia fechada
- [DOC] PCOV + PHPUnit → Clover PHP → Sonar. Sin LCOV frontend importado. / Complementarios: PHPStan/Larastan (91), Pint --test (8), TypeScript PASS, formato (298), Oxlint (5 warnings). / No sumar esas deudas a los 0 Issues Sonar V2. No asumir TDD solo por existir tests.

## 12. Mejora SonarQube V1 → V2

**ID:** 12. **Archivo:** [12_MEJORA_SONARQUBE_V1_V2.drawio](<../fuentes/12_MEJORA_SONARQUBE_V1_V2.drawio>).

**Objetivo:** Separar corrección de hallazgos de la clasificación y cobertura.

**Fuentes:** [REPORTE_EVIDENCIAS_V1_SONARQUBE.md](<../../../sonarqube/evidencias/v1/REPORTE_EVIDENCIAS_V1_SONARQUBE.md>); [REPORTE_RESULTADOS_V2_PRELIMINAR.md](<../../../sonarqube/evidencias/v2/REPORTE_RESULTADOS_V2_PRELIMINAR.md>); [REPORTE_MAESTRO_ENTREGA.md](<../../entregables-finales/REPORTE_MAESTRO_ENTREGA.md>).

**Elementos principales:** Dos páginas: cinco hallazgos y correcciones; comparación de cobertura y condiciones del Gate.

**Relaciones:** V1→análisis→corrección→regresión→scanner→V2. La segunda página separa V2 inicial y reclasificación de tests.

**Cómo leerlo:** Comparar Issues 5→0, Vulnerabilities 2→0 y Code Smells 3→0; luego leer advertencias antes de interpretar coverage.

**Advertencias:** New Code final 50 %, no 80 %. Gate OK con Small Changes / ignoredConditions=true. Global 69.5 % cambia denominador al reclasificar tests; no prueba nueva cobertura frontend. app/ 89.6 % constante; sidebar.tsx:621 sin importación LCOV.

**Aplicación en Word:** Capítulo 13. Insertar selectivamente tras revisión nativa; conservar proporción y pie que indique estado de evidencia.

**Aplicación en PPT:** Resultados antes/después. Usar vistas generales o una página de detalle; no pegar todas las páginas reducidas.

**Estado de evidencia:** HISTÓRICO documentado el 20/10/2026; servidor NO CONSULTADO en esta tarea. XML y esquema válidos; revisión visual local de vistas auxiliares realizada. Interpretación por editor diagrams.net pendiente.

**Páginas / lectura textual de elementos:**

### Página 1. Correcciones y resultados

Lienzo 1530 × 1160; 10 vértices editables y 5 conectores.

- [QA] V1 / 5 Issues: 2 Vulnerabilities + 3 Code Smells
- [H] Análisis por regla / Prioridad y contexto real
- [PROC] Correcciones mínimas / Sin silenciar reglas ni eliminar validaciones
- [QA] Nuevas pruebas y regresión / PHPUnit 414 / 8 skipped / 0 failed / Vitest 48/48
- [QA] Scanner y procesamiento / SUCCESS documentado
- [DOC] V2 / 0 Issues · 0 Vulnerabilities / 0 Code Smells; 5/5 FIXED
- [DOC] Reglas: php:S5693; typescript:S2245, S6843, S8786 y S6671. / Bugs 0→0 · Hotspots 0→0 · Duplicación 0.0 %→0.0 %. / El cierre de cinco hallazgos no certifica ausencia de defectos ni preparación productiva.

### Página 2. Cobertura y Quality Gate

Lienzo 1530 × 1130; 8 vértices editables y 2 conectores.

- [QA] V1 / Global 66.5 % / Gate OK; conditions: []
- [QA] V2 inicial / Global 65.6 % / New Code 1.7 %; Gate ERROR
- [QA] V2 tras clasificar tests / Global 69.5 % / New Code 50 %; Gate OK
- [DOC] Small Changes / ignoredConditions=true (heredado) / El Gate ignora la condición con menos de 20 líneas elegibles. / NO se alcanzó 80 %: una de dos líneas productivas elegibles está cubierta.
- [DOC] app/ 89.6 % en V1 y V2. Sin LCOV frontend; sidebar.tsx:621 queda sin cobertura importada. / 11 líneas nuevas productivas, 2 elegibles, 1 cubierta. El aumento global es reclasificación de tests, no cobertura nueva. / No comparar porcentajes como si sus denominadores fueran idénticos.

## 13. Artículos y metodología asistida por IA

**ID:** 13. **Archivo:** [13_MAPA_ARTICULOS_METODOLOGIA_IA.drawio](<../fuentes/13_MAPA_ARTICULOS_METODOLOGIA_IA.drawio>).

**Objetivo:** Explicar qué dimensión respalda cada grupo de artículos.

**Fuentes:** [MATRIZ_DOBLE_ENTRADA_METODOLOGIA_IA.xlsx](<../../entregables-finales/MATRIZ_DOBLE_ENTRADA_METODOLOGIA_IA.xlsx>); [MATRIZ_ARTICULOS_IA.xlsx](<../../investigacion-ia/MATRIZ_ARTICULOS_IA.xlsx>); [MATRIZ_ARTICULOS_IA.md](<../../investigacion-ia/MATRIZ_ARTICULOS_IA.md>).

**Elementos principales:** Nueve dimensiones, ART-01…ART-20 con autor/año, elemento metodológico y aplicación al SaaS.

**Relaciones:** Solo membresías X presentes en Articulos_vs_Dimensiones. Grupo de artículos→dimensión→control propuesto→aplicación documental.

**Cómo leerlo:** Cada página es una dimensión. Un ART puede aparecer en varias; el conteo de identidades únicas sigue siendo 20. Referencias completas en matriz.

**Advertencias:** Validación bibliográfica previa no equivale a lectura exhaustiva de contenido: métodos/muestras parcialmente verificados siguen pendientes. Ninguna agrupación implica que el paper adopte AI-DLC. No se repitió investigación.

**Aplicación en Word:** Capítulo 5 / referencias. Insertar selectivamente tras revisión nativa; conservar proporción y pie que indique estado de evidencia.

**Aplicación en PPT:** Seleccionar dimensión; no proyectar referencias completas. Usar vistas generales o una página de detalle; no pegar todas las páginas reducidas.

**Estado de evidencia:** 20 IDENTIDADES BIBLIOGRÁFICAS VALIDADAS; contenido PARCIALMENTE VERIFICADO según catálogo. XML y esquema válidos; revisión visual local de vistas auxiliares realizada. Interpretación por editor diagrams.net pendiente.

**Páginas / lectura textual de elementos:**

### Página 1. Productividad - Eficiencia

Lienzo 1680 × 960; 12 vértices editables y 3 conectores.

- GRUPO DE ARTÍCULOS · respaldo temático
- [DOC] ART-05 / Vaithilingam et al. (2022)
- [DOC] ART-06 / Barke et al. (2023)
- [DOC] ART-11 / Ziegler et al. (2022)
- [PROC] DIMENSIÓN / Productividad/Eficiencia
- [PROC] ELEMENTO METODOLÓGICO / Registrar esfuerzo y control
- [SIS] APLICACIÓN AL SaaS / Eficiencia PENDIENTE: sin horas ni grupo sin IA

### Página 2. Calidad

Lienzo 1680 × 1185; 22 vértices editables y 3 conectores.

- GRUPO DE ARTÍCULOS · respaldo temático
- [DOC] ART-01 / Hou et al. (2024)
- [DOC] ART-02 / Fan et al. (2023)
- [DOC] ART-04 / Pearce et al. (2022)
- [DOC] ART-07 / Dakhel et al. (2023)
- [DOC] ART-08 / Nguyen et al. (2022)
- [DOC] ART-09 / Chen et al. (2024)
- [DOC] ART-10 / Wang et al. (2024)
- [DOC] ART-13 / Syahputri et al. (2025)
- [DOC] ART-15 / Gao et al. (2025)
- [DOC] ART-16 / Wang et al. (2026)
- [DOC] ART-17 / Ferrari y Spoletini (2025)
- [DOC] ART-18 / Jiang et al. (2026)
- [DOC] ART-20 / Jimenez et al. (2024)
- [PROC] DIMENSIÓN / Calidad
- [PROC] ELEMENTO METODOLÓGICO / Verificar salidas
- [SIS] APLICACIÓN AL SaaS / Tests, assertions y lectura prudente de Sonar

### Página 3. Seguridad

Lienzo 1680 × 960; 13 vértices editables y 3 conectores.

- GRUPO DE ARTÍCULOS · respaldo temático
- [DOC] ART-03 / Perry et al. (2023)
- [DOC] ART-04 / Pearce et al. (2022)
- [DOC] ART-14 / Zhu et al. (2025)
- [DOC] ART-15 / Gao et al. (2025)
- [PROC] DIMENSIÓN / Seguridad
- [PROC] ELEMENTO METODOLÓGICO / Revisión de seguridad
- [SIS] APLICACIÓN AL SaaS / Hallazgos por regla; Policies y multitenencia

### Página 4. Testing - TDD

Lienzo 1680 × 975; 19 vértices editables y 3 conectores.

- GRUPO DE ARTÍCULOS · respaldo temático
- [DOC] ART-01 / Hou et al. (2024)
- [DOC] ART-02 / Fan et al. (2023)
- [DOC] ART-08 / Nguyen et al. (2022)
- [DOC] ART-09 / Chen et al. (2024)
- [DOC] ART-10 / Wang et al. (2024)
- [DOC] ART-14 / Zhu et al. (2025)
- [DOC] ART-15 / Gao et al. (2025)
- [DOC] ART-16 / Wang et al. (2026)
- [DOC] ART-19 / Yang et al. (2024)
- [DOC] ART-20 / Jimenez et al. (2024)
- [PROC] DIMENSIÓN / Testing/TDD
- [PROC] ELEMENTO METODOLÓGICO / Oráculos y validación de tests
- [SIS] APLICACIÓN AL SaaS / PHPUnit/Vitest; TDD solo con RED/GREEN documentado

### Página 5. Requisitos

Lienzo 1680 × 960; 13 vértices editables y 3 conectores.

- GRUPO DE ARTÍCULOS · respaldo temático
- [DOC] ART-01 / Hou et al. (2024)
- [DOC] ART-02 / Fan et al. (2023)
- [DOC] ART-15 / Gao et al. (2025)
- [DOC] ART-17 / Ferrari y Spoletini (2025)
- [PROC] DIMENSIÓN / Requisitos
- [PROC] ELEMENTO METODOLÓGICO / Especificación y aceptación
- [SIS] APLICACIÓN AL SaaS / RF/RNF y criterios; contratos humanos

### Página 6. Human-in-the-loop

Lienzo 1680 × 960; 14 vértices editables y 3 conectores.

- GRUPO DE ARTÍCULOS · respaldo temático
- [DOC] ART-03 / Perry et al. (2023)
- [DOC] ART-05 / Vaithilingam et al. (2022)
- [DOC] ART-06 / Barke et al. (2023)
- [DOC] ART-13 / Syahputri et al. (2025)
- [DOC] ART-15 / Gao et al. (2025)
- [PROC] DIMENSIÓN / Human-in-the-loop
- [PROC] ELEMENTO METODOLÓGICO / Supervisión y aceptación
- [SIS] APLICACIÓN AL SaaS / Guardian; decisión y publicación humanas

### Página 7. Trazabilidad

Lienzo 1680 × 960; 10 vértices editables y 3 conectores.

- GRUPO DE ARTÍCULOS · respaldo temático
- [DOC] ART-13 / Syahputri et al. (2025)
- [PROC] DIMENSIÓN / Trazabilidad
- [PROC] ELEMENTO METODOLÓGICO / Persistir fuente y versión
- [SIS] APLICACIÓN AL SaaS / RF→código→test; prompts originales incompletos

### Página 8. Mantenibilidad

Lienzo 1680 × 960; 14 vértices editables y 3 conectores.

- GRUPO DE ARTÍCULOS · respaldo temático
- [DOC] ART-02 / Fan et al. (2023)
- [DOC] ART-14 / Zhu et al. (2025)
- [DOC] ART-15 / Gao et al. (2025)
- [DOC] ART-19 / Yang et al. (2024)
- [DOC] ART-20 / Jimenez et al. (2024)
- [PROC] DIMENSIÓN / Mantenibilidad
- [PROC] ELEMENTO METODOLÓGICO / Revisión de cambios y regresión
- [SIS] APLICACIÓN AL SaaS / Mantenimiento y corrección acotada de hallazgos

### Página 9. Automatización

Lienzo 1680 × 975; 19 vértices editables y 3 conectores.

- GRUPO DE ARTÍCULOS · respaldo temático
- [DOC] ART-01 / Hou et al. (2024)
- [DOC] ART-02 / Fan et al. (2023)
- [DOC] ART-09 / Chen et al. (2024)
- [DOC] ART-10 / Wang et al. (2024)
- [DOC] ART-12 / Amaro et al. (2025)
- [DOC] ART-14 / Zhu et al. (2025)
- [DOC] ART-16 / Wang et al. (2026)
- [DOC] ART-18 / Jiang et al. (2026)
- [DOC] ART-19 / Yang et al. (2024)
- [DOC] ART-20 / Jimenez et al. (2024)
- [PROC] DIMENSIÓN / Automatización
- [PROC] ELEMENTO METODOLÓGICO / Herramientas bajo alcance
- [SIS] APLICACIÓN AL SaaS / CI configurada; CD/operación productiva no demostrados

## 14. Variables y operacionalización

**ID:** 14. **Archivo:** [14_VARIABLES_OPERACIONALIZACION.drawio](<../fuentes/14_VARIABLES_OPERACIONALIZACION.drawio>).

**Objetivo:** Separar protocolo propuesto, mecanismos e indicadores observados.

**Fuentes:** [OPERACIONALIZACION_VARIABLES.xlsx](<../../investigacion-ia/OPERACIONALIZACION_VARIABLES.xlsx>); [METODOLOGIA_DESARROLLO_ASISTIDO_IA.md](<../../investigacion-ia/METODOLOGIA_DESARROLLO_ASISTIDO_IA.md>); [REPORTE_EVIDENCIAS_V1_SONARQUBE.md](<../../../sonarqube/evidencias/v1/REPORTE_EVIDENCIAS_V1_SONARQUBE.md>); [REPORTE_RESULTADOS_V2_PRELIMINAR.md](<../../../sonarqube/evidencias/v2/REPORTE_RESULTADOS_V2_PRELIMINAR.md>).

**Elementos principales:** VI: protocolo humano IA; mecanismos: contratos, supervisión y verificación; VD: calidad; indicadores y límites exploratorios.

**Relaciones:** Flechas expresan operacionalización propuesta, no causalidad; indicadores enlazan calidad observada con evidencia Sonar y pruebas.

**Cómo leerlo:** De VI a mecanismos y VD; leer nota de eficiencia pendiente y denominadores antes de comparar valores.

**Advertencias:** No efecto causal atribuido a IA, ni ahorro inventado. Eficiencia exploratoria pendiente de horas/costos/retrabajo/control sin IA. Trazabilidad no tiene porcentaje de adopción inventado.

**Aplicación en Word:** Capítulo 5.6 / operacionalización. Insertar selectivamente tras revisión nativa; conservar proporción y pie que indique estado de evidencia.

**Aplicación en PPT:** Variables y discusión. Usar vistas generales o una página de detalle; no pegar todas las páginas reducidas.

**Estado de evidencia:** VARIABLES PROPUESTAS; métricas históricas observadas y eficiencia PENDIENTE. XML y esquema válidos; revisión visual local de vistas auxiliares realizada. Interpretación por editor diagrams.net pendiente.

**Páginas / lectura textual de elementos:**

### Página 1. Protocolo y calidad

Lienzo 1500 × 1210; 10 vértices editables y 6 conectores.

- [PROC] VARIABLE INDEPENDIENTE PROPUESTA / Aplicación del protocolo colaborativo humano IA / Guiado por especificaciones y verificación
- [PROC] Contratos y contexto / RF/RNF, alcance y trazabilidad
- [PROC] Supervisión humana / Revisión y aceptación
- [PROC] Verificación / Pruebas y análisis de calidad
- [QA] VARIABLE DEPENDIENTE PROPUESTA / Calidad del producto software / Indicadores: Issues, Vulnerabilities, Code Smells, coverage, tests y duplicación
- [DOC] Eficiencia EXPLORATORIA: PENDIENTE de horas, costos, retrabajo y control sin IA. / Trazabilidad: vínculos presentes; no inventar porcentaje de adopción del protocolo. / Métricas Sonar son históricas y la cobertura cambia de denominador al clasificar tests.

## 15. Del requisito a la evidencia

**ID:** 15. **Archivo:** [15_REQUISITO_A_EVIDENCIA.drawio](<../fuentes/15_REQUISITO_A_EVIDENCIA.drawio>).

**Objetivo:** Seguir ejemplos reales de CV privado y decisión final humana.

**Fuentes:** [MATRIZ_REQUERIMIENTOS_SISTEMA.xlsx](<../../entregables-finales/MATRIZ_REQUERIMIENTOS_SISTEMA.xlsx>); [MATRIZ_TRAZABILIDAD_SAAS_RECLUTAMIENTO.xlsx](<../../entregables-finales/MATRIZ_TRAZABILIDAD_SAAS_RECLUTAMIENTO.xlsx>); [MATRIZ_TRAZABILIDAD_ACADEMICA.xlsx](<../../entregables-finales/MATRIZ_TRAZABILIDAD_ACADEMICA.xlsx>); [CandidateCvRequest.php](<../../../../app/Http/Requests/Candidates/CandidateCvRequest.php>); [CandidateProfileTest.php](<../../../../tests/Feature/Candidates/CandidateProfileTest.php>); [REPORTE_RESULTADOS_V2_PRELIMINAR.md](<../../../sonarqube/evidencias/v2/REPORTE_RESULTADOS_V2_PRELIMINAR.md>).

**Elementos principales:** Dos páginas: RF-09/CU-08 (CV) y RF-23/caso académico asociado (decisión), código, prueba, Sonar y matrices.

**Relaciones:** Del problema preliminar a necesidad, RF, CU, código, prueba y evidencia. Cada página conserva la ruta real de archivo y método.

**Cómo leerlo:** Seguir flechas en serpentina; consultar el vínculo de fuente para copiar rutas continuas, ya que se parten visualmente para caber.

**Advertencias:** RF-09 tiene php:S5693 FIXED documentado. RF-23 no tiene métrica Sonar individual de aceptación: solo alcance agregado y pruebas funcionales históricas. Sonar no sustituye aceptación.

**Aplicación en Word:** Capítulos 4, 11 y 13. Insertar selectivamente tras revisión nativa; conservar proporción y pie que indique estado de evidencia.

**Aplicación en PPT:** Ejemplo trazable RF-09 o RF-23. Usar vistas generales o una página de detalle; no pegar todas las páginas reducidas.

**Estado de evidencia:** CADENA VERIFICADA en archivos/matriz; resultado de ejecución HISTÓRICO. XML y esquema válidos; revisión visual local de vistas auxiliares realizada. Interpretación por editor diagrams.net pendiente.

**Páginas / lectura textual de elementos:**

### Página 1. RF-09

Lienzo 1680 × 1250; 11 vértices editables y 7 conectores.

- [PROC] Necesidad / solución / Perfil y CV privado por convocatoria (S-01; / problema preliminar P1)
- [DOC] RF-09 / El sistema debe permitir al postulante completar / su perfil y cargar su CV en PDF de forma privada.
- [DOC] CU-08 / Catálogo académico F8
- [SIS] Código / app/Http/Requests/Candidates/CandidateCvRequ / est.php
- [QA] Prueba / tests/Feature/Candidates/CandidateProfileTest.ph / p / test_rf09_cv_cannot_exceed_five_megabytes_ev / en_with_a_larger_configuration
- [QA] SonarQube / php:S5693 FIXED documentado; Clover / importado
- [DOC] Evidencia / Informe V2 y métodos de tests presentes; no / reejecutados
- [DOC] Matriz / Requisitos + procesos + trazabilidad académica

### Página 2. RF-23

Lienzo 1680 × 1250; 11 vértices editables y 7 conectores.

- [PROC] Necesidad / solución / Sustento de decisión humana (S-05; problema / preliminar P5)
- [DOC] RF-23 / El sistema debe permitir al Aprobador / Dirección / registrar la decisión final humana, con / confirmación explícita y justificación.
- [DOC] CU-18 / Catálogo académico F8
- [SIS] Código / app/Services/Selection/FinalDecisionService.php
- [QA] Prueba / tests/Feature/Selection/FinalDecisionTest.php / test_rf23_approver_records_the_final_decision_fo / r_a_ranked_finalist
- [QA] SonarQube / Alcance agregado: no hay métrica individual de / aceptación RF-23
- [DOC] Evidencia / Informe V2 y métodos de tests presentes; no / reejecutados
- [DOC] Matriz / Requisitos + procesos + trazabilidad académica

## 16. Git: estrategia documentada e historial real

**ID:** 16. **Archivo:** [16_FLUJO_GIT_DESARROLLO.drawio](<../fuentes/16_FLUJO_GIT_DESARROLLO.drawio>).

**Objetivo:** Evitar atribuir una GitFlow ideal o sincronía inexistente.

**Fuentes:** [AGENTS.md](<../../../../AGENTS.md>); [CLAUDE.md](<../../../../CLAUDE.md>); [tests.yml](<../../../../.github/workflows/tests.yml>); [PROGRESS.md](<../../../PROGRESS.md>).

**Elementos principales:** Dos páginas: estrategia documentada y fotografía de commits/ramas locales/remotas disponibles.

**Relaciones:** Primera página describe norma; segunda solo relaciones de padres verificadas y referencias existentes en la copia local.

**Cómo leerlo:** Distinguir política develop→rama acotada de historia b67f644→a88cd3c→b345d9c. Referencias no conectadas no implican merges.

**Advertencias:** Sin fetch: caché remota no prueba estado online actual. main/develop locales difieren de origin y no se sincronizaron. No se importó F35-SBX remoto. CI configurada no equivale a run verde actual ni a CD.

**Aplicación en Word:** Capítulo 9. Insertar selectivamente tras revisión nativa; conservar proporción y pie que indique estado de evidencia.

**Aplicación en PPT:** Versionamiento y límites CI. Usar vistas generales o una página de detalle; no pegar todas las páginas reducidas.

**Estado de evidencia:** GIT LOCAL VERIFICADO; remotos son referencias disponibles, no consulta online. XML y esquema válidos; revisión visual local de vistas auxiliares realizada. Interpretación por editor diagrams.net pendiente.

**Páginas / lectura textual de elementos:**

### Página 1. Estrategia documentada

Lienzo 1520 × 1120; 10 vértices editables y 5 conectores.

- [DOC] develop limpio y sincronizado / Base exigida por gobierno
- [PROC] Rama acotada / feature/* / fix/* / docs/* / chore/*
- [PROC] Implementación o documentación / Un writer; contratos preservados
- [QA] Revisión y pruebas proporcionales / Diff y evidencia
- [H] Integración / publicación / Solo con autorización
- [DOC] main / release / tags / No trabajo directo; historia protegida
- [DOC] Es una ESTRATEGIA DOCUMENTADA, no prueba de que cada cambio histórico siguió ese flujo. / CI: push main/develop/release//fix/, PR y manual. chore/ no activa push CI. / CD productivo no demostrado. En esta tarea se detiene antes de staging o publicación.

### Página 2. Historial y referencias observadas

Lienzo 1580 × 1220; 9 vértices editables y 2 conectores.

- [DOC] b67f644 / Merge del handoff macOS / Padres: 853d423 y 36660ae
- [DOC] a88cd3c / Correcciones Sonar + evidencia / Padre: b67f644
- [DOC] b345d9c · HEAD / Reportes auditoría Sonar / Padre: a88cd3c
- [PROC] Rama actual: chore/sonarqube-macos-setup en b345d9c / Coincide con su origin/chore/sonarqube-macos-setup; cambios académicos locales sin commit.
- [DOC] REFERENCIAS LOCALES (no inferir sincronía) / main: 8a00505 · develop: f7017c1 · feature/phase-24-academic-documentation: 8ebaf70 / Hay ramas remotas feature/*, chore/*, fix/github-actions-ci, release/qa-final y codex/mejoras-sonarqube.
- [DOC] REFERENCIAS REMOTAS DISPONIBLES / origin/main: b8892af · origin/develop: 87ef831 (más recientes que el contexto de esta rama). / No se incorporaron sus estados F35-SBX al alcance académico local ni se actualizó ninguna referencia.
