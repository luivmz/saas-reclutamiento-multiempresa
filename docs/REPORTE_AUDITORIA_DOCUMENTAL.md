# REPORTE DE AUDITORÍA DOCUMENTAL

## 1. Resumen ejecutivo

- Fecha de la auditoría: 26/10/2026, zona America/Lima.
- Objeto: reunir evidencia para un futuro paquete de registro; este informe no constituye ese paquete.
- Base técnica: `b8892af39a6492d8dd44a36290604efc602380cd`, main publicado consultado en GitHub.
- Rama de trabajo: `docs/registro-software-indecopi`; no se realizaron commits ni publicaciones.
- Se inventariaron 1.213 archivos versionados y se recorrieron 1.038 archivos textuales mediante análisis estático.
- Se leyeron adicionalmente ocho plantillas DOCX aportadas por el usuario; sus ejemplos no se trasladan al SaaS.
- El núcleo es un monolito modular web Laravel/Inertia/React sobre PostgreSQL, con Redis y Docker de desarrollo.
- La multiempresa está implementada mediante organización, scopes, Policies y consultas explícitas.
- RF-01 a RF-27 abarcan requerimientos, vacantes, postulaciones, evaluaciones, ranking y selección humana.
- El ranking es determinista y ponderado; RF-23 exige decisión humana, confirmación y justificación.
- RF-29 es un experimento operacional opcional: no evalúa ni selecciona personas.
- F35-SBX es un sandbox académico sintético cerrado, congelado e integrado, separado del runtime Laravel.
- G0 real no está aprobada; los datos reales están prohibidos y F36–F40 continúan bloqueadas.
- Hay código y pruebas suficientes para preparar los anexos técnicos; los resultados de ejecución citados son históricos.
- No se ejecutaron aplicaciones, pruebas, instalaciones, migraciones, seeders, contenedores ni generadores.
- Autoría legal, titularidad, datos personales, fechas oficiales, firmas y aplicabilidad del documento empresarial requieren confirmación humana.
- Los ocho DOCX del usuario se conservan íntegros; el único archivo generado por Codex es este Markdown.

## 2. Identificación del software

### Alcance y criterio de evidencia

**VERIFICADO** identifica evidencia directa del código, configuración, historial o documentos examinados. Una característica verificada está presente en las fuentes; no implica que se haya ejecutado ahora. **INFERIDO** identifica una interpretación técnica razonable y delimitada. **NO ENCONTRADO** significa ausencia de evidencia en las superficies consultadas, no prueba absoluta de inexistencia. **PENDIENTE DE CONFIRMACIÓN HUMANA** se reserva para datos legales, personales, administrativos y decisiones de alcance no demostrables por el repositorio.

AS-IS se refiere a la implementación de la base indicada. TO-BE, propuestas, catálogos candidatos y ejemplos de las plantillas no se presentan como capacidades implementadas. Los PDF, DOCX y capturas históricos se inventariaron; esta fase no realizó una revisión visual completa de los 175 archivos binarios o no UTF-8 versionados.

| Campo | Resultado | Clasificación y evidencia |
|---|---|---|
| Nombre descriptivo principal | Plataforma SaaS Multiempresa para la Gestión del Reclutamiento, Evaluación y Selección de Personal | VERIFICADO: `README.md`, título |
| Nombre abreviado encontrado | SaaS Reclutamiento / SaaS de Reclutamiento Multiempresa | VERIFICADO: `CLAUDE.md`; `resources/js/app.tsx:10` |
| Título académico extendido | Análisis y Diseño de una Plataforma SaaS Multiempresa para la Gestión del Reclutamiento, Evaluación y Selección de Personal – Caso de estudio: Colegio Andino de Huancayo | VERIFICADO: `README.md`; `docs/academico/ACADEMIC_BASELINE.md` |
| Título definitivo para registro | PENDIENTE DE CONFIRMACIÓN HUMANA | Las variantes encontradas no equivalen a una denominación legal aprobada |
| Propósito | Gestionar necesidades de personal y su proceso de reclutamiento, desde requerimiento hasta cierre y notificación | VERIFICADO: rutas, servicios de dominio y matriz RF |
| Tipo técnico | Aplicación web de gestión de reclutamiento con separación lógica entre organizaciones | VERIFICADO: `routes/web.php`, `resources/js/pages/`, `OrganizationScope` |
| Modalidad SaaS | Arquitectura compatible con servicio centralizado multiempresa; no se acredita operación comercial SaaS | INFERIDO como modalidad de explotación; NO ENCONTRADO: suscripciones, facturación, cuotas, alta autónoma de empresas o despliegue público comercial |
| Multiempresa | Una aplicación y esquema compartidos; organización por entidad de negocio, roles y controles de acceso | VERIFICADO: `OrganizationScope`, `BelongsToOrganization`, Policies y migraciones |
| Caso de estudio | Colegio Andino de Huancayo | VERIFICADO como contexto académico; no acredita titularidad, cliente contractual ni autorización institucional |
| Contexto académico | Universidad Continental, curso Pruebas y Calidad de Software, NRC 28607 | VERIFICADO documentalmente: `README.md`, baseline académico |
| Marca registrada o nombre comercial formal | NO ENCONTRADO | No se verificó un registro de marca ni un documento de aprobación del título |
| Plataforma móvil o escritorio nativa | NO ENCONTRADO | Interfaz web responsiva; no se encontró proyecto Android/iOS/Electron propio |

### Versiones e identidad reproducible

| Referencia | Identidad verificada | Interpretación |
|---|---|---|
| Base analizada y HEAD de esta rama | `b8892af39a6492d8dd44a36290604efc602380cd` | Merge publicado de main posterior al handoff; no se crea una versión nueva por este informe |
| Tree de la base | `76cb743b83fe3af425437063a9dae61b049ea81d` | Mismo árbol del candidato corregido de handoff `2ae0003` |
| Padres de la base | `06b789f9e9e99268eccfb72a15df2dd30fe47360` y `87ef831f0b930bdce09e2f0aeaa9d626104a4fac` | Integración de develop en main |
| origin/main consultado | `b8892af39a6492d8dd44a36290604efc602380cd` | Coincidió con `git ls-remote` al iniciar |
| origin/develop consultado | `87ef831f0b930bdce09e2f0aeaa9d626104a4fac` | Referencia publicada al iniciar |
| Etiqueta académica v1.0 | `v1.0.0-academic` → `9a946c202ef7473230e8efa371ace13479ab889c` | Tag anotado histórico, no modificado |
| Etiqueta académica v1.1 | `v1.1.0-academic` → `634f354ca7343d8e7cd9735bd0ba3e1d9c4e6d99` | Versión académica formal encontrada; no identifica por sí sola todos los documentos post-release |
| Versión del componente Python | `0.1.0` | `ml-service/pyproject.toml`; no es la versión del SaaS completo |
| Versión exacta a declarar en el registro | PENDIENTE DE CONFIRMACIÓN HUMANA | Elegir el alcance depositado y relacionarlo con tag, commit y manifest del futuro ejemplar |

El historial alcanzable desde la base contiene 299 commits, incluidos merges. Su primer commit es `e87ef3950fe48a723a46b0ed143e20fd798730fa`, fechado el 13/09/2026 a las 00:17:22 −05:00. El último es la base del 25/10/2026 a las 18:17:51 −05:00. Este es el **periodo Git observable**, no una certificación de inicio de creación ni de terminación oficial de la primera versión funcional. T1 solicita esa fecha de conclusión: **PENDIENTE DE CONFIRMACIÓN HUMANA**.

### Gobierno vigente que delimita el registro técnico

| Condición | Estado conservado |
|---|---|
| G0 real | NO APROBADA |
| G0-02 / G0-03 / G0-12 | PENDIENTE EXTERNO |
| G0-09 / G0-14 | CUMPLIDO |
| G0-SBX | APROBADA CON RESTRICCIONES |
| ADR-005 | PROPUESTA |
| Datos reales | PROHIBIDOS |
| Alcance C | BLOQUEADO |
| F35 productiva | BLOQUEADA |
| F35-SBX | CERRADA / CONGELADA / INTEGRADA, alcance académico y sintético |
| RF-23 / RF-29 | Decisión humana / experimental e informativa, respectivamente |
| F36–F40 / F36-SBX | BLOQUEADAS / NO INICIADA |

Fuentes vigentes: bloques de `CLAUDE.md`, `docs/PROGRESS.md`, `docs/academico/ACADEMIC_BASELINE.md`, `README.md` y guía de handoff. Una aprobación técnica de este informe no cambia ninguno de esos estados.

## 3. Stack tecnológico verificado

Las versiones de los locks son versiones **resueltas en archivos versionados**. Las de Docker son versiones **configuradas para construir**. No se inspeccionó un contenedor ni se comprobó una instalación en ejecución.

| Capa | Tecnología | Versión verificable | Evidencia |
|---|---|---|---|
| Backend | PHP | Requisito `^8.3`; imagen configurada 8.4.25 | `composer.json`; `docker/php/Dockerfile:3` |
| Backend | Laravel | Lock v13.31.0; requisito `^13.17` | `composer.lock`, paquete `laravel/framework` |
| Backend | Eloquent ORM | Incluido en Laravel 13.31.0 | Modelos que extienden `Model`; relaciones y casts |
| Integración web | Inertia Laravel | v3.3.4 | `composer.lock`, `inertiajs/inertia-laravel` |
| Autenticación | Laravel Fortify | v1.39.0 | Lock; `FortifyServiceProvider`; `config/fortify.php` |
| Autenticación | Laravel Passkeys | v0.2.1 PHP; 0.2.0 frontend | Locks; `User implements PasskeyUser`; pantalla de seguridad |
| Rutas tipadas | Laravel Wayfinder | PHP v0.1.21; plugin frontend 0.1.10 | Locks; `vite.config.ts`; imports de acciones generadas |
| Gestión PHP | Composer | Imagen 2.10.3 | `docker/php/Dockerfile:5` |
| Frontend | React / React DOM | 19.3.0 | `package-lock.json` |
| Frontend | TypeScript | 5.9.3 | Lock; `tsconfig.json` con strict, noImplicitAny y noEmit |
| Integración frontend | @inertiajs/react y @inertiajs/vite | 3.7.1 | Lock; `resources/js/app.tsx` |
| Build | Vite | 8.3.0 | Lock; configuración integrada con Vite Plus |
| Build, lint y formato | Vite Plus | 0.3.0 | `package.json`; `vite.config.ts`; comandos `vp` |
| Build | React plugin y React Compiler | Plugin 6.1.1; compiler 1.0.0 | Lock; `reactCompilerPreset` en Vite |
| Estilos | Tailwind CSS / plugin Vite | 4.3.3 | Lock; `resources/css/app.css` |
| UI | Radix UI | Por paquete: dialog 1.1.23, select 2.3.7, tooltip 1.2.16, entre otros | Entradas individuales de `package-lock.json` |
| UI | Lucide React | 0.475.0 | Lock; imports de iconos |
| UI | Sonner / input-otp | 2.0.8 / 1.5.0 | Lock; componentes de avisos y 2FA |
| UI | class-variance-authority / clsx / tailwind-merge | 0.7.1 / 2.1.1 / 3.7.0 | Lock; composición de estilos |
| Formularios y estado | Inertia Form; hooks React | Versiones de Inertia/React anteriores | Páginas de configuración, postulación y comparación; `useState`, `useEffect`, `usePage` |
| Tablas | Componente propio DataTable | Sin versión independiente | `resources/js/components/data-table.tsx`; no se atribuye a TanStack |
| Gráficos y estado global externo | NO ENCONTRADO un módulo de gráficos ni Redux/Zustand en las importaciones revisadas | No aplica | Dependencias directas e importaciones del frontend |
| Movimiento / 3D | CSS y DOM; carga diferida React | Sin motor 3D adicional | `experience-3d/recruitment-scene.tsx`; CSS; sin Three.js/WebGL |
| Runtime frontend | Node.js | Imagen configurada 22.23.2 | Dockerfile y CI |
| Gestión JS | npm | 10.9.8 documentado; no fijado independientemente en package.json | `docs/docker.md`; restauración con package-lock |
| Persistencia | PostgreSQL | Imagen `17.11-alpine` | Compose, CHECK, JSONB, trigger y consultas ILIKE |
| Memoria compartida | Redis | Imagen `7.4.11-alpine` | Compose; conexión de sesiones, caché y colas documentada |
| Cliente Redis | phpredis | 6.3.0 configurado | Dockerfile |
| Almacenamiento | Filesystem local privado | Laravel Storage | `config/filesystems.php`; `CandidateProfileService::DISK` |
| Infraestructura | Docker Compose | Requisito documentado ≥2.24 | `docs/docker.md`; uso de `env_file.required` |
| QA PHP | PHPUnit | 12.5.35 | Composer lock; `phpunit.xml` |
| QA PHP | Pint / Larastan / PHPStan | v1.32.1 / v3.12.0 / 2.2.14 | Lock; preset Laravel y nivel 7 |
| QA frontend | Vitest mediante Vite Plus | Integrado con Vite Plus 0.3.0; no se fija aquí una versión independiente | Seis `*.test.tsx` que importan `vitest` |
| E2E | Cypress | Imagen y comando 15.3.0 | Compose y `package.json`; no confundir con dependencia npm instalada |
| ML | Python | Requisito ≥3.12 | `ml-service/pyproject.toml` |
| ML | numpy / pandas / pydantic / tzdata | 2.1.3 / 2.2.3 / 2.9.2 / 2024.2, declaradas con igualdad | Pyproject |
| ML | scikit-learn / scipy / joblib | 1.9.1 / 1.18.1 / 1.6.0, declaradas con igualdad | Pyproject; no se descargaron ni verificaron en un entorno |
| Servicio experimental | FastAPI / uvicorn | 0.115.6 / 0.34.0, declaradas | Pyproject; `api/app.py` |
| QA ML | pytest / pytest-cov / httpx | 8.3.3 / 5.0.0 / 0.28.1 | Dependencias opcionales dev del pyproject |
| Sandbox académico | SQLite en memoria; biblioteca estándar Python | SQLite suministrado por el intérprete, versión no determinada | `docs/academico/tools/f35sbxb2/sbxb_store.py` |
| Modelado histórico | PowerDesigner, UML y BPMN | Artefactos nativos y exportaciones versionadas; herramienta no ejecutada | `docs/v1.1/powerdesigner/`; `docs/academico/powerdesigner/` |

### Infraestructura observable

| Servicio | Función y conexiones | Puertos y volúmenes |
|---|---|---|
| app | Laravel servido mediante `php artisan serve`; inicia después de PostgreSQL y Redis saludables | Host 8000 configurable; fuente montada; volúmenes vendor y node_modules |
| queue | Worker Redis, después de app saludable; reintentos y reinicio periódico configurados | Sin puerto propio; mismos volúmenes y configuración |
| postgres | Persistencia de desarrollo y base separada de PHPUnit | 5432 configurable en loopback; volumen pgdata; init SQL |
| redis | Sesiones, caché y cola según la receta Compose | 6379 configurable en loopback; volumen redisdata |
| app-e2e / queue-e2e | Perfil e2e separado; aplicación y worker de prueba | Aplicación en 8001 loopback; BD E2E y Redis DB 2/3; storage físico compartido |
| cypress | Contenedor de pruebas del perfil e2e | Sin servidor público; montajes de pruebas y configuración |
| ML | Proceso Python del host o red interna, opcional | Puerto 8008 documentado; no tiene servicio Compose propio |

La imagen es de desarrollo/demostración, con código montado y servidor CLI. No se encontró un despliegue productivo Nginx/PHP-FPM, Kubernetes, infraestructura cloud ni automatización de despliegue. Las opciones S3, MySQL o SQL Server del scaffolding de configuración no acreditan integraciones operativas ni compatibilidad real de las migraciones.

## 4. Arquitectura reconstruida

**VERIFICADO en código:** monolito modular Laravel con presentación React/Inertia. Frontend y backend comparten aplicación y rutas; la existencia del proceso FastAPI opcional no transforma el núcleo en una arquitectura de microservicios. La caracterización de «monolito modular» es también explícita en README y documentación de arquitectura.

Flujo textual principal, sin generar un diagrama:

`Persona → navegador → páginas React/Inertia → rutas web Laravel → middleware de sesión/rol → Form Request y/o Gate/Policy → controlador → servicio de dominio → Eloquent/PostgreSQL → Resource/props Inertia → navegador`.

Las capas se comprueban en `routes/web.php`, `bootstrap/app.php`, `HandleInertiaRequests`, controladores de selección, `FinalDecisionRequest`, `VacancyPolicy` y servicios. La ubicación de la autorización varía: algunas acciones usan Form Requests y otras invocan `Gate::authorize` directamente.

- **Autenticación:** Fortify, guard web de sesión, usuarios Eloquent; registro público exclusivamente de postulantes. No se encontró autenticación JWT ni una API pública Laravel separada en `routes/api.php`.
- **Autorización:** cinco roles definidos en `UserRole`; Policies sobre organización, propiedad o asignación; la navegación condicional no sustituye la autorización de servidor.
- **Persistencia:** PostgreSQL mantiene estados y decisiones. Transacciones y bloqueos de fila protegen operaciones relevantes; no debe afirmarse que toda lectura o actualización use bloqueos.
- **Asincronía:** `RecruitmentNotification implements ShouldQueue`, con `afterCommit()`; canales database y mail. Compose proporciona worker Redis. No se encontró una capa propia de jobs de negocio diferente de estos trabajos de notificación.
- **Archivos:** el CV se almacena en disco local privado; su descarga pasa por Policy. No se encontró extracción semántica ni OCR del CV dentro del runtime.
- **Integración ML:** navegador → endpoint Laravel de riesgo → autorización → checkpoint/15 features operacionales → HTTP interno con token → FastAPI → pipeline scikit-learn → validación de respuesta → tarjeta experimental. No escribe una decisión en PostgreSQL ni alimenta el ranking.
- **Dependencias externas:** restauración de paquetes y fuentes IBM Plex durante build; correo según driver configurado; ML interno opcional. No se acredita SMTP productivo, facturación electrónica ni servicios de terceros por su mera presencia en ejemplos.
- **Sandbox F35-SBX:** contratos, fixtures, almacén SQLite `:memory:`, pipeline determinista y gates en `docs/academico/`. No hay ruta de la aplicación que lo convierta en procesamiento productivo de expedientes.

Para el futuro diagrama de arquitectura deben existir estos bloques: actores y navegador; aplicación Laravel/React; módulos de dominio; frontera de autenticación/organización; PostgreSQL; disco privado; Redis; worker y canales de notificación; servicio ML opcional claramente rotulado; entorno Docker. El sandbox se representa, si se incluye, en un recuadro académico separado. No añadir cloud, balanceadores, Kubernetes, S3, API gateway o servidores no encontrados.

## 5. Inventario de módulos

En la tabla, «implementado» describe presencia de código y pruebas relacionadas; la ejecución actual no se verificó. Los RF conservan la numeración del baseline. El inventario contiene 29 archivos de controlador (incluidos el controlador base y soporte), 20 Form Requests, 31 archivos de servicio (incluidos DTO/objetos de valor), siete Policies más un trait, y 31 páginas React. Estos recuentos no equivalen al número de módulos de negocio.

| Módulo | Funcionalidad | Backend | Frontend | Evidencia |
|---|---|---|---|---|
| Acceso | Login, logout, recuperación y confirmación de contraseña | Fortify; proveedores y guard web | `auth/login.tsx`, forgot/reset/confirm-password | `config/fortify.php`; pruebas Auth |
| Registro | Autorregistro de postulantes; no permite elegir rol staff | `CreateNewUser::create` fija Candidate | `auth/register.tsx` | CandidateRegistrationTest; RegistrationTest |
| Seguridad personal | Cambio de contraseña, 2FA y soporte passkeys | `SecurityController`; Fortify y User | `settings/security.tsx`, two-factor-challenge | SecurityTest; TwoFactorChallengeTest; configuración |
| Perfil personal | Edición del nombre/correo y eliminación de cuenta con controles | `Settings/ProfileController`; Form Requests | `settings/profile.tsx` | ProfileUpdateTest; rutas settings |
| Apariencia | Tema claro/oscuro/sistema y navegación | Middleware de apariencia | `settings/appearance.tsx`; use-appearance | Código local; pruebas visuales históricas |
| Inicio | Accesos por rol, organización y aviso de decisión humana | Props compartidas Inertia | `pages/dashboard.tsx` | No consulta métricas de reclutamiento: índice de accesos |
| Organizaciones | Entidad de organización y vinculación de personal | Organization, User, FK y scopes | Nombre de organización en layout | No se encontró CRUD administrativo de empresas |
| Roles | Solicitante, RR. HH., Aprobador/Dirección, Evaluador, Postulante | Enum, middleware y Policies | `lib/navigation.ts` | No se encontró administrador de permisos dinámicos o SuperAdmin |
| Requerimientos RF-01–04 | Crear, corregir, enviar, observar, validar, aprobar/rechazar e historial | JobRequestController/TransitionController; JobRequestWorkflow | `pages/job-requests/` | JobRequestWorkflowTest; JobRequestPolicy; estados |
| Vacantes RF-05–07 | Configurar desde requerimiento aprobado, perfil, criterios y publicación | VacancyService, VacancyValidator, VacancyPolicy | `pages/vacancies/`; form/criteria-table | VacancyPublicationTest; migración vacancies |
| Portal público | Buscar por título, listar y consultar vacantes publicadas de organizaciones | PublicVacancyController; scope published | `pages/jobs/index.tsx`, show.tsx | ApplyToVacancyTest; rutas /empleos |
| Perfil postulante RF-09 | Teléfono, ciudad, formación, ocupación, experiencia y resumen | CandidateProfileService; CandidateProfileRequest | `pages/candidate/profile.tsx` | CandidateProfile; CandidateProfileTest |
| CV RF-09 | Cargar PDF y conservar referencia al documento usado al postular | CandidateCvRequest; storeCv; CandidateDocumentPolicy | Formulario de perfil y enlaces autorizados | Privacidad, tamaño y MIME comprobables en código |
| Postulación RF-10–11 | Perfil/CV requeridos, ventana de recepción, duplicado impedido, confirmación | ApplicationService; ApplyController | Detalle de empleo y mis postulaciones | Unique vacancy/candidate; ApplyToVacancyTest |
| Revisión RF-12–15 | Listar expediente, preseleccionar/descartar y mover etapas con historial | ApplicationStageService; ApplicationPolicy | `pages/applications/index.tsx`, show.tsx | ApplicationReviewTest; enums; auditoría |
| Seguimiento del postulante | Ver únicamente postulaciones propias, timeline y convocatorias | CandidateApplicationController; proyección de datos | `candidate/applications/index.tsx`, show.tsx | Sin puntajes internos ni observaciones de entrevistador |
| Sesiones RF-16–19 | Programar evaluaciones y entrevistas; asignar evaluador; convocar | AssessmentScheduler; Schedule Requests | Expediente y `pages/assessments/` | EvaluationTest; InterviewTest |
| Resultados RF-19–20 | Registrar notas por criterio y observaciones; resultado humano de entrevista | AssessmentResultRecorder; ScoreSheetValidator | `assessments/show.tsx` | Policies limitan al evaluador asignado; no regrabar sesión terminada |
| Ponderaciones RF-20 | Pesos positivos, rangos, duplicados y total configurable | WeightingValidator; CriterionDefinition | Formulario de vacante y CriteriaTable | WeightingValidatorTest; config recruitment |
| Ranking RF-21–22 | Normalización, promedio por criterio, desglose, empates e incompletos | RankingService; VacancyRankingBuilder; RankingPresenter | `pages/selection/comparison.tsx` | RankingServiceTest; RankingComparisonTest |
| Decisión RF-23 | Aprobador elige finalista completo, confirma y justifica | FinalDecisionRequest/Service; VacancyPolicy | Panel de decisión en comparison | Puede elegir a quien no esté primero; FinalDecisionTest |
| Selección RF-24 | RR. HH. aplica la decisión registrada | SelectionRegistrationService | Acción en comparison | SelectionRegistrationTest; índice único parcial |
| Cierre RF-25–26 | Cerrar tras selección, cambiar pendientes y notificar resultado propio | VacancyClosureService; ProcessResultNotification | Resumen de cierre y notificaciones | VacancyClosureTest; ProcessResultNotificationTest |
| Auditoría RF-27 | Registrar acciones y consultar resumen filtrado de solo lectura | AuditLogger; AuditLogResource; AuditLogPolicy | `pages/audit/index.tsx` | Aprobador; append-only Eloquent/PostgreSQL |
| Notificaciones | Listar, leer una o todas; canales database/mail | NotificationController; siete clases de notificación, incluida base | `pages/notifications/index.tsx`; contador | Relaciones del usuario; validación de URL de redirección |
| Riesgo RF-29 candidato | Riesgo de demora del proceso, experimental y opcional | OperationalRiskService/FeatureBuilder/MlRiskClient; FastAPI | OperationalRiskCard en detalle de vacante | Pruebas Ml; no es clasificación de personas |
| Portada y CSS 3D | Presentación decorativa diferida con póster de respaldo | Sin lógica decisoria | welcome; recruitment-depth/scene; capability hook | Pruebas experience-3d; CSS y motion |
| Operación/QA | Salud DB/Redis y soporte E2E protegido | HealthController; EnsureE2eSupportEnabled; E2eEnvironment | No es un módulo de negocio público | /health, /up, /__e2e; pruebas Testing |
| Sandbox académico | Evidencias sintéticas, almacenamiento efímero y pipeline de doce pasos | Herramientas Python F35-SBX-A/B | No se encontró interfaz productiva | Carpetas evidencia-sbx y tools/f35sbx*; cierre y freeze |

**NO ENCONTRADO como módulo operativo:** nómina, contratos laborales, firma de contratación, pagos/suscripciones, facturación, reportes PDF/Excel descargables de negocio, chat, videoconferencia integrada, grabación de entrevistas, OCR/NLP de CV, scoring de personas con IA, panel analítico RF-28, administración web de organizaciones/personal ni pipeline de etapas libremente configurable. Los informes académicos PDF y los scripts de documentación no son una funcionalidad de exportación del SaaS.

## 6. Flujos principales

### Flujo 1 — Requerimiento, aprobación y publicación

1. **Actores:** Solicitante → RR. HH. → Aprobador/Dirección → RR. HH.
2. **Entrada:** necesidad de personal, puesto, área, plazas, contrato y justificación.
3. **Proceso:** registrar borrador; enviar; observar/corregir o validar; aprobar/rechazar; crear vacante desde requerimiento aprobado; definir perfil y criterios; validar pesos, fechas y plazas; publicar.
4. **Archivos:** JobRequestWorkflow; JobRequestStatus; JobRequestPolicy; VacancyService; VacancyValidator; páginas job-requests y vacancies.
5. **Resultado:** vacante publicada y trazabilidad del requerimiento; el rechazo no genera una vacante.
6. **Evidencia:** rutas requerimientos/vacantes, JobRequestWorkflowTest y VacancyPublicationTest.

### Flujo 2 — Perfil, CV y postulación

1. **Actor:** Postulante autenticado; el visitante puede consultar empleos.
2. **Entrada:** datos de perfil, PDF ficticio y vacante publicada con recepción abierta.
3. **Proceso:** completar perfil; validar y almacenar CV privado; consultar empleo; bloquear la vacante durante registro; comprobar ventana, perfil, CV y duplicado.
4. **Archivos:** CreateNewUser; CandidateProfileService; CandidateCvRequest; PublicVacancyController; ApplicationService::apply; pages/candidate y pages/jobs.
5. **Resultado:** postulación con CV referenciado, estado inicial, historial, auditoría y aviso.
6. **Evidencia:** CandidateRegistrationTest, CandidateProfileTest, ApplyToVacancyTest y E2E-05.

### Flujo 3 — Revisión, evaluación y entrevista

1. **Actores:** RR. HH. y evaluador asignado de la misma organización.
2. **Entrada:** expediente de postulación, criterios de la vacante, fecha/modalidad/lugar y evaluador.
3. **Proceso:** preselección o descarte humano; programación en etapas admitidas; notificación; registro de todos los puntajes de la etapa y de observaciones/resultado de entrevista.
4. **Archivos:** ApplicationStageService; AssessmentScheduler; AssessmentResultRecorder; AuthorizesAssessmentSessions; pages/applications y pages/assessments.
5. **Resultado:** sesiones realizadas y resultados humanos disponibles para comparación; el candidato ve su convocatoria, no los puntajes internos.
6. **Evidencia:** ApplicationReviewTest, EvaluationTest, InterviewTest y E2E-06/07.

### Flujo 4 — Comparación, decisión humana, selección y cierre

1. **Actores:** RR. HH. consulta; Aprobador decide; RR. HH. registra selección y cierre.
2. **Entrada:** criterios válidos y resultados completos de un finalista.
3. **Proceso:** calcular ranking sin escribir estados; Aprobador elige, incluso fuera del primer lugar, confirma y justifica; guardar snapshot; RR. HH. aplica esa decisión; cerrar y notificar.
4. **Archivos:** RankingService::rank; VacancyRankingBuilder::forVacancy; FinalDecisionRequest/Service; SelectionRegistrationService; VacancyClosureService; comparison.tsx.
5. **Resultado:** una selección por vacante y cierre trazable; el sistema no toma la decisión.
6. **Evidencia:** RankingServiceTest, FinalDecisionTest, SelectionRegistrationTest, VacancyClosureTest y E2E-08/09/10.

### Flujo 5 — Consulta de auditoría

1. **Actor:** Aprobador/Dirección.
2. **Entrada:** filtros de consulta de acciones de su organización.
3. **Proceso:** Policy, scope de organización, paginación y proyección mediante lista blanca.
4. **Archivos:** AuditLogController, AuditLogPolicy, AuditLogResource, AuditLog y migración append-only.
5. **Resultado:** resumen de acciones sin exposición de IP ni metadata cruda en esa vista.
6. **Evidencia:** AuditLogViewTest, AuditTrailTest y AuditLoggerTest.

### Flujo 6 — Riesgo operacional experimental

1. **Actor:** RR. HH. o Aprobador autorizado.
2. **Entrada:** vacante y checkpoint al inicio del día siguiente al cierre de postulaciones.
3. **Proceso:** comprobar ventana y plazo; construir quince enteros operacionales; consultar servicio habilitado; validar contrato, freeze, umbral y coherencia; degradar si falla.
4. **Archivos:** OperationalRiskService, FeatureBuilder, MlRiskClient, config/ml.php, API FastAPI y OperationalRiskCard.
5. **Resultado:** señal informativa o estado descriptivo/no disponible; no cambia ranking ni decisiones.
6. **Evidencia:** OperationalRiskCheckpointTest, MlRiskClientTest, MlCrossTenantValidationTest y pruebas API.

Para los futuros diagramas de flujo se recomiendan **tres**: (1) requerimiento a publicación; (2) postulación a resultados humanos; (3) ranking → decisión humana → selección → cierre → notificación. El flujo ML es un anexo opcional separado; no debe sustituir el flujo principal ni sugerir selección automática.

## 7. Modelo de datos

La revisión encontró **17 clases de modelo de dominio**, más el trait y el scope de organización, y **18 archivos de migración** que declaran **26 tablas** de aplicación/framework. Al añadir la tabla interna de control de migraciones de Laravel se obtiene el total de 27 que aparece en documentación histórica; esa tabla de control no es una declaración Schema::create del proyecto. Es un recuento de definiciones de código, no un inventario de una base en ejecución.

| Entidad | Propósito | Relaciones principales | Evidencia |
|---|---|---|---|
| Organization | Organización operativa; nombre, slug, tax_id opcional y actividad | Tiene usuarios; referenciada por entidades de negocio | Organization.php; migración create_organizations |
| User | Cuenta y uno de cinco roles | Organización opcional; perfil; postulaciones; sesiones asignadas por FK | User.php; create_users; add_organization_and_role |
| JobRequest | Necesidad de personal y aprobación | Organización; solicitante, validador, decisor; historial; una vacante | JobRequest.php; create_job_requests |
| JobRequestStatusHistory | Secuencia de estados del requerimiento | Requerimiento, organización y autor del cambio | Modelo y segunda tabla de create_job_requests |
| Vacancy | Convocatoria, fechas, estado, plazas y plazo objetivo | Requerimiento único, organización, perfil, criterios, postulaciones y decisión | Vacancy.php; create_vacancies; add_target_completion_at |
| JobProfile | Requisitos del puesto | Una vacante; organización | JobProfile.php; tabla job_profiles |
| EvaluationCriterion | Criterio, etapa, peso, rango y posición | Vacante y resultados de evaluación/entrevista | EvaluationCriterion.php; tabla evaluation_criteria |
| CandidateProfile | Perfil global del postulante | User único; documentos; latestCv | CandidateProfile.php; create_candidate_profiles |
| CandidateDocument | Metadatos y ubicación privada del CV | Perfil; referenciado por postulación | CandidateDocument.php; tabla candidate_documents |
| Application | Postulación a una vacante | Organización; candidato global; CV; sesiones; historial | Application.php; create_applications |
| ApplicationStageHistory | Timeline de etapas y autor del cambio | Postulación, organización y usuario | Modelo y tabla application_stage_histories |
| Evaluation | Sesión programada/realizada | Organización, postulación, evaluador, programador y resultados | Evaluation.php; create_evaluations |
| EvaluationResult | Nota por criterio de evaluación | Evaluación, criterio y organización | EvaluationResult.php; evaluation_results |
| Interview | Entrevista programada/realizada y valoración humana | Organización, postulación, evaluador, programador y resultados | Interview.php; create_interviews |
| InterviewResult | Nota por criterio de entrevista | Entrevista, criterio y organización | InterviewResult.php; interview_results |
| SelectionDecision | Decisión final y snapshot del elegido | Vacante única; postulación elegida; decisor; registrador | SelectionDecision.php; create_selection_decisions |
| AuditLog | Acción, entidad polimórfica, actor y metadata | Organización/usuario opcionales; morph map de entidades | AuditLog.php; create_audit_logs; AppServiceProvider |

Las otras nueve tablas son `notifications` y ocho tablas de soporte: `password_reset_tokens`, `sessions`, `cache`, `cache_locks`, `jobs`, `job_batches`, `failed_jobs` y `passkeys`. `users` ya está incluida entre las 17 entidades anteriores. No se encontró tabla pivote de roles/permisos: el rol es un atributo enum de User.

### Aislamiento multiempresa comprobado

- `users.organization_id` es nullable; un CHECK exige que el postulante no tenga organización y que el personal sí la tenga.
- `BelongsToOrganization` agrega `OrganizationScope` y puede completar organización al crear desde personal autenticado.
- El scope restringe cuando el usuario autenticado tiene organización. **No filtra por sí solo a invitados ni candidatos**, cuyo acceso depende de Policies y consultas explícitas.
- `User::sharesOrganizationWith` y Policies comparan organización y rol; en sesiones se comprueba además el evaluador asignado.
- Las consultas públicas retiran el scope para mostrar vacantes publicadas de distintas organizaciones. Las consultas de candidato se limitan a su id; otras retiradas de scope requieren predicados explícitos de tenant/entidad.
- El modelo es de base/esquema compartidos. No se encontró PostgreSQL RLS ni una base de datos independiente por organización.
- Las FK referencian entidades, pero no constituyen por sí solas una garantía universal de igualdad de organización entre todas las filas relacionadas. Los servicios, Requests, Policies y pruebas son parte esencial del aislamiento.
- Evidencia específica: CrossTenantAccessTest, OrganizationScopeTest, MlCrossTenantValidationTest y E2E-11. Su existencia no equivale a una nueva ejecución de esos casos.

### Restricciones y estados relevantes

Las migraciones definen FK, índices y CHECK para roles, estados, pesos, rangos, fechas y consistencia de resultados. Hay unicidad de postulación por vacante/candidato; perfil por usuario; vacante por requerimiento; decisión por vacante; y notas por sesión/criterio. El índice parcial `applications_one_selected_per_vacancy` impide más de un seleccionado por vacante.

Los enums incluyen estados de requerimiento, vacante y postulación; modalidades, tipos de evaluación, etapas de criterio y resultados de entrevista. `ApplicationStatus::manualTargets` excluye los resultados finales. El valor de cierre «desierta» existe en el esquema pero no tiene flujo implementado. Las plazas múltiples aparecen como dato, aunque A-29 limita el MVP a un seleccionado por vacante.

### Datos y evidencias fuera de la base principal

F34 contiene un dataset versionado explícitamente sintético, con manifest `f34-synth-1.1.0` y `total_rows=27404`; no se convierte en evidencia de personas reales. El experimento ML genera sus datasets/modelos en rutas ignoradas. El sandbox B2 crea ocho tablas SQLite efímeras por contexto sintético: tenant_context, pipeline_run, pipeline_event, evidence_source, evidence_record, evidence_provenance, simulated_review y audit_entry. No son tablas productivas de PostgreSQL ni deben mezclarse con el ER del SaaS.

## 8. Seguridad implementada

### Implementado y verificable

| Control | Evidencia y alcance real |
|---|---|
| Autenticación por sesión | config/auth.php, Fortify y rutas auth; no se encontró JWT como esquema de autenticación del SaaS |
| Autorregistro limitado | CreateNewUser fija rol Postulante; datos de entrada no eligen organización o rol staff |
| Hash de contraseña | Cast hashed de User; reglas de validación; no se revelan valores |
| 2FA y passkeys | Features de Fortify, User, pantalla security y pruebas; habilitación/configuración no acredita uso por todos los usuarios |
| Rate limiting | Login y 2FA: cinco intentos/minuto; passkeys: diez; cambio de contraseña: throttle 6,1 |
| Autorización de negocio | Policies de requerimientos, vacantes, postulaciones, sesiones, documentos y auditoría |
| Multiempresa | Scope, trait, predicates explícitos y tests cross-tenant; límites detallados en §7 |
| Validación | Form Requests, enums, Rule::exists con organización en referencias relevantes, validadores de dominio y CHECK |
| CSRF | Rutas de negocio en grupo web de Laravel; análisis estático, sin prueba de explotación en esta sesión |
| Cookies | Configuración HttpOnly y SameSite; Secure depende del entorno; cookies de apariencia/sidebar exceptuadas de cifrado |
| Archivos | PDF, MIME y tamaño máximo configurable; nombre UUID; Storage local privado; descarga con Gate y nosniff |
| Decisión humana | human_confirmation aceptada y justificación de 20–2000 caracteres; finalista con resultados completos; solo Aprobador de la organización |
| Concurrencia | Transacciones y lockForUpdate en transiciones/decisión/selección/cierre y otras operaciones identificadas |
| Auditoría | AuditLogger filtra claves sensibles recursivamente; AuditLogResource expone lista blanca |
| Integridad de auditoría | Modelo impide update/delete; trigger PostgreSQL bloquea cambios salvo excepción acotada que permite poner user_id en NULL conservando el resto |
| Notificaciones | Proyección del resultado propio; no incluye ranking, notas u otros candidatos en ProcessResultNotification |
| ML | Token interno por entorno; comparación constante; sin token responde 503; credencial inválida 401; contrato rechaza campos extra |
| Fallo del ML | Deshabilitado por defecto; timeout y fallback; validación de identidad/umbral/coherencia de respuesta |
| Soporte E2E | Endpoints fuera de web/CSRF, pero exigen habilitación, no producción y token; reset verifica nombre de base E2E |
| Red local | PostgreSQL/Redis/E2E en loopback por Compose; esto no equivale a un despliegue productivo seguro |

### No encontrado o no demostrable

- No se encontró un pentest vigente, certificación de seguridad, certificación WCAG, auditoría jurídica o autorización para datos reales.
- La verificación de correo no está activada como feature de Fortify y User no implementa MustVerifyEmail; las pruebas relacionadas pueden omitirse mediante skipUnlessFortifyHas. No afirmar «correo verificado obligatorio».
- No se demostró TLS de producción, WAF, segregación de secretos mediante vault, MFA obligatorio, RLS, cifrado completo de datos en reposo ni política operativa de backups/restauración.
- La validación PDF no acredita antivirus, sandbox de documentos ni detección de contenido malicioso.
- AuditLogger filtra por **nombres de claves**, no por comprensión del texto: no garantiza eliminar toda PII de comentarios libres. La vista de auditoría oculta texto libre, IP y metadata cruda; la base conserva actor/IP y cierta información de negocio.
- El trigger append-only es una protección de aplicación/base con la excepción indicada; no prueba imposibilidad de manipulación por un administrador con privilegios de esquema.
- No se acreditan despliegue institucional, evaluaciones de privacidad ni uso de CV reales. La capacidad técnica de cargar un PDF no autoriza esos datos.

### Secretos y datos sensibles

Se recorrieron los 1.038 archivos textuales versionados con patrones de claves privadas y formatos de credenciales GitHub, AWS y OpenAI: no se encontraron coincidencias de esos formatos. Es un barrido delimitado, no una certificación de ausencia de todo secreto o de todo el historial.

Se observaron variables de contraseña/token y valores de demostración en ejemplos, tests, seeders y CI; no se reproducen sus valores en este informe. Los archivos locales `.env`, `.env.e2e`, credenciales de HOME y configuración privada no fueron abiertos. `.gitignore` excluye los entornos y artefactos sensibles/generados.

Si una revisión posterior detecta una credencial con indicios reales, debe registrarse como **POSIBLE SECRETO VERSIONADO — revisar <ruta>**, sin copiar su valor. Las identidades Git de §15 se incluyen únicamente porque fueron solicitadas para evidenciar contribuciones; no se incluyen DNI, domicilios, firmas ni datos de postulantes.

## 9. Pruebas y calidad

### Existencia de pruebas y herramientas

| Tipo | Herramienta | Cobertura funcional observable | Evidencia |
|---|---|---|---|
| Unitarias PHP | PHPUnit | Ranking, estados, pesos y planillas de puntajes | tests/Unit/Ranking, Enums, Evaluation, Assessments |
| Funcionales/integración PHP | PHPUnit + PostgreSQL | Autenticación, requerimientos, vacantes, CV, postulación, sesiones, decisión, cierre, auditoría | tests/Feature; phpunit.xml |
| Seguridad multiempresa | PHPUnit y Cypress | Organización, acceso cruzado, documentos y ML | tests/Feature/Tenancy; MlCrossTenantValidationTest; E2E-11 |
| Contrato ML | pytest, TestClient/httpx | API, tipos, token, rechazo de atributos, servicio y artefacto | ml-service/tests/test_api_security.py, test_api_service.py, test_serving_artifact.py |
| Ciencia/reproducibilidad ML | pytest | Distribuciones, fuga, partición temporal, freeze, umbral y reproducción | Otros tests del componente Python |
| Componentes | Vitest vía Vite Plus | DataTable, 3D, formularios, contraseñas, motion y QA visual | Seis archivos .test.tsx en resources/js/components |
| E2E | Cypress 15.3.0 | Veinte specs del recorrido principal y negativos | cypress/e2e/e2e-00 a e2e-19 |
| Exploración visual | Cypress | Responsive, teclado, 2FA, temas y rendimiento exploratorio | cypress/visual; capturas históricas |
| Tipos frontend | TypeScript | Compilación estática noEmit | tsconfig.json; npm types:check; CI |
| Análisis PHP | PHPStan/Larastan | Nivel 7 en app, bootstrap, config, database y routes | phpstan.neon; composer types:check |
| Estilo | Pint y vp check | Preset Laravel; lint/formato configurados en Vite | pint.json; composer/package scripts; vite.config.ts |
| Integración continua | GitHub Actions tests | PostgreSQL, instalación desde locks, build, TypeScript y PHPUnit | .github/workflows/tests.yml |
| Validación académica | Scripts Python | Modelos, manifests, documentos y gates de capas sintéticas | docs/academico/tools; powerdesigner/scripts |

El inventario estático contó 48 archivos PHP `*Test.php` y 359 métodos nominales `test*`; 18 archivos Python `test_*.py` y 380 funciones de test; 20 specs Cypress con 79 declaraciones literales it/test. Estos recuentos **no son resultados ejecutados**: data providers, parametrizaciones y bucles generan otros números de casos.

No se encontró suite Pest como herramienta principal ni una configuración ESLint independiente; una autorización Composer para un plugin Pest no demuestra uso de Pest. Tampoco debe confundirse la existencia de PHPStan/Pint con su ejecución en el workflow actual: éste ejecuta directamente build, tsc y artisan test. Cypress, pytest y los validadores académicos no están incluidos en ese job.

### Resultados históricos reutilizables para un futuro resumen QA

| Evidencia histórica | Resultado documentado | Uso correcto |
|---|---|---|
| F25, PHPUnit | 411 superadas, 8 omitidas, 0 fallidas; 1498 aserciones | Atribuir al QA global F25, no a esta sesión |
| F25, pytest ML | 533 superadas | Atribuir al componente experimental y datos sintéticos |
| F25, componentes | 42/42 | Seis archivos de pruebas; resultado histórico |
| F25, TypeScript / build | Sin errores / correcto | No equivale a una compilación nueva de esta rama |
| F25, Cypress | 20 specs, 85/85 | Entorno E2E aislado histórico |
| F25/F26, observaciones | Formato pendiente y validaciones manuales de lector de pantalla/hardware modesto diferidas | No declarar certificación o rendimiento empresarial |
| Cierre global F35-SBX | Gate anclado y pruebas de capas sintéticas registradas | Evidencia académica; no certifica seguridad o producción del SaaS |

Fuentes: `docs/v1.1/phase-25-final-qa.md`, matriz QA, cierre F26 y documentos de las capas SBX. El estado CI publicado posterior no se consultó mediante API en esta fase; no se declara un nuevo CI GREEN.

T6 pide resumen de pruebas funcionales, integración, rendimiento y seguridad. Puede prepararse con casos, fuentes, fechas, base probada y límites. Las métricas de producción, cargas concurrentes, cobertura porcentual integral o benchmarks no medidos quedan **NO ENCONTRADO / PENDIENTE DE CONFIRMACIÓN HUMANA**. Una nueva ejecución requerirá una fase autorizada que permita sus escrituras.

## 10. Elementos técnicos de aporte propio

### Elementos técnicos que pueden sustentar una descripción de aporte propio

Esta selección describe combinaciones y reglas presentes en el código. No declara originalidad jurídica, exclusividad, patentabilidad ni ausencia de derechos de terceros. T1/T3/T7 solicitan describir o declarar originalidad, pero las declaraciones personales se reservan a sus firmantes.

| Elemento técnico | Descripción sustentable | Evidencia |
|---|---|---|
| Proceso de requerimiento | Secuencia de revisión con roles diferenciados, historial, comentarios y transacciones | JobRequestWorkflow y JobRequestStatus |
| Separación de organizaciones | Tenant lógico en modelos, Policies y consultas; postulante global con acceso por propiedad | OrganizationScope, BelongsToOrganization, User y Policies |
| Configuración de vacante | Perfil y criterios por etapa con validación de pesos/rangos y publicación condicionada | VacancyService, VacancyValidator y WeightingValidator |
| Ranking explicable | Promedio por criterio, normalización, ponderación, desglose e incompletos separados | RankingService, DTO de Ranking y RankingPresenter |
| Control humano | Elección explícita, justificación, snapshot y separación entre decisión y registro de selección | FinalDecisionRequest/Service y SelectionRegistrationService |
| Cierre coherente | Estados finales y notificaciones individuales después de confirmar el cierre | VacancyClosureService; ProcessResultNotification |
| Auditoría del proceso | Registro de acciones, filtrado de claves y proyección segura con protección append-only | AuditLogger; AuditLogResource; trigger |
| Experiencia de usuario | Expediente por rol, tablas móviles semánticas, avisos y movimiento reducido | DataTable, lib/navigation, pages y CSS |
| Integración operacional opcional | Ventana/checkpoint reproducible, contrato estricto y fallback | OperationalRiskService y MlRiskClient |
| Evidencia académica separada | Pipeline determinista y almacén efímero de datos sintéticos con gates de integridad | F35-SBX-B2/B3; no atribuir como automatización productiva |

El código depende de Laravel, React, Inertia, Radix y otras bibliotecas. `composer.json` conserva el nombre/description del starter kit y licencia MIT en sus metadatos; no se encontró un LICENSE raíz específico que establezca por sí solo la titularidad o la licencia de todas las aportaciones propias. Los locks contienen licencias de dependencias. Es necesario identificar el alcance propio y revisar atribuciones, plantillas, fuentes tipográficas, imágenes y asistencia de IA antes de firmar una declaración de no infracción. Esa revisión y la conclusión legal son **PENDIENTE DE CONFIRMACIÓN HUMANA**.

## 11. Código recomendado para el ejemplar de 10–15 páginas

### Requisitos extraídos de las plantillas

- **T2, «Código Fuente o Ejecutable»:** seleccionar módulos esenciales representativos; admite un ejemplar parcial y exige excluir credenciales, datos sensibles y configuración privada. Sus carpetas y comandos del ejemplo no son la estructura de este SaaS.
- **T7, Anexo 1:** pide título, tipo, lenguajes, framework, autores y titular opcional; propone **10 a 15 páginas** de clases, módulos o controladores y rótulos de procedencia del código.
- **T8, «Ejemplar del software»:** menciona al menos diez páginas representativas. Se adopta el objetivo de 10–15 páginas solicitado por el usuario; no se certifica aquí que esa extensión sea un requisito oficial vigente.
- El soporte final, formato, metadatos de autor y alcance de depósito necesitan aprobación humana. No se generó ZIP, ejecutable ni paginación final.

### Selección precisa propuesta

Los rangos indican líneas verificadas del snapshot base; se seleccionan fragmentos coherentes, sin sustituirlos por pseudocódigo. Se recomienda conservar firmas y contexto necesario. El número de páginas es una estimación editorial, no una propiedad del archivo.

| Prioridad | Archivo | Fragmento recomendado | Motivo |
|---|---|---|---|
| 1 | app/Models/Scopes/OrganizationScope.php | Método apply, líneas 17–24 | Explica el filtro tenant y su condición de aplicación |
| 1 | app/Models/Concerns/BelongsToOrganization.php | bootBelongsToOrganization y organization, líneas 17–36 | Vincula scope, creación y relación de organización |
| 1 | app/Policies/VacancyPolicy.php | Métodos view, decide y manages, líneas 16–19, 54–57 y 69–72 | Rol y organización, sin asumir que el frontend protege datos |
| 1 | app/Services/JobRequests/JobRequestWorkflow.php | register, líneas 31–46; transition, líneas 125–148 | Ciclo de negocio, estado, historial y auditoría transaccional |
| 1 | app/Services/Applications/ApplicationService.php | apply, líneas 25–80 | Perfil, CV, ventana, duplicado y registro de postulación |
| 1 | app/Services/Ranking/RankingService.php | rank, líneas 26–58; score, 117–133; assignPositions, 141–165 | Lógica propia de cálculo, completitud y empates |
| 1 | app/Http/Requests/Selection/FinalDecisionRequest.php | authorize/rules, líneas 11–34 | Validación de tenant, confirmación humana y justificación |
| 1 | app/Services/Selection/FinalDecisionService.php | decide, líneas 28–84 | Decisión humana persistida; elección fuera del primer puesto permitida |
| 1 | app/Services/Selection/SelectionRegistrationService.php | register, líneas 27–68 | Aplica decisión previa; no elige por sí mismo |
| 1 | app/Services/Selection/VacancyClosureService.php | close, líneas 33–94 | Cierre, estados y evidencia; separar notificación posterior |
| 2 | app/Services/Audit/AuditLogger.php | record, líneas 24–40; sanitize, 62–75 | Registro de acciones y filtrado recursivo de claves |
| 2 | resources/js/pages/selection/comparison.tsx | Formulario de decisión, líneas 332–425, especialmente justificación y human_confirmation | Frontend propio del control humano; acompañar con imports mínimos pertinentes |
| 2 | resources/js/components/data-table.tsx | Componente DataTable, líneas 78–169 | Tabla semántica, caption y representación móvil |
| 2 | tests/Feature/Tenancy/CrossTenantAccessTest.php | Casos de aislamiento de vacantes/postulaciones, líneas 65–88 | Evidencia de intención y regresión de la frontera multiempresa |
| 2 | tests/Feature/Selection/FinalDecisionTest.php | Casos de elección no primera y confirmación requerida, líneas 74–92 | Demuestra el contrato RF-23 sin sustituirlo por una afirmación general |
| 3, opcional | app/Services/Ml/OperationalRiskService.php | assess y checkpointFor, líneas 66–96 | Solo si se decide incluir RF-29; rotular experimental y operacional |
| 3, opcional | docs/academico/tools/f35sbxb3/sbxb_pipeline.py | run y verificación del reporte, identificados por método | Solo si el depósito incluye expresamente el sandbox académico; no mezclar con el producto |

### Propuesta de paginación, todavía no producida

Un núcleo razonable combina tenant/Policy (~55 líneas), workflow (~55), postulación (~56), ranking (~75), Request/decisión (~80), selección (~42), cierre (~62), auditoría (~32), frontend de confirmación (~70) y dos pruebas (~43): aproximadamente **570–650 líneas** con contexto y cabeceras. A unas 45–50 líneas útiles por página, permite aproximadamente **12–15 páginas**. Ajustar cuando se elijan tipografía, márgenes y títulos; no reducir legibilidad para forzar el número.

La primera selección debe priorizar backend de reclutamiento y multiempresa; al menos un fragmento React identifica la interfaz real. Si se usa DataTable o se añade ML, reemplazar fragmentos secundarios para mantener el presupuesto. T7 no obliga a mostrar todos los archivos ni todas las tecnologías.

### Exclusiones y controles del futuro ejemplar

No incluir vendor, node_modules, locks como páginas de «código propio», acciones/rutas Wayfinder generadas, caches, binarios ML, dumps de bases, CV, artefactos con datos personales, credenciales, `.env*`, auth.json ni configuración de HOME. Evitar seeders y fixtures de cuentas en el extracto público.

Docker/Compose y configuración pueden documentarse en un anexo técnico sanitizado si se autoriza, pero no son la selección principal de lógica propia. Los nombres de variables sensibles pueden explicarse sin valores. No atribuir un fragmento a una persona basándose solo en el encabezado de ejemplo de T7 o en el autor de un commit. Antes del depósito deberán fijarse commit, ruta, rango, hash y revisión de contenido de cada fragmento.

## 12. Capturas recomendadas

T2 y T6 recomiendan al menos tres capturas claras y sin datos sensibles. Sus ejemplos de inventarios, proveedores o reportes se reemplazan por pantallas reales del SaaS. T7 permite anexos gráficos opcionales. La siguiente selección propone **seis capturas imprescindibles**; no se tomó ninguna en esta fase.

### Capturas imprescindibles

| Prioridad | Pantalla | Ruta/componente | Qué demuestra |
|---|---|---|---|
| 1 | Login | /login; resources/js/pages/auth/login.tsx | Acceso real; satisface el ejemplo de login de T2/T6 sin mostrar credenciales |
| 1 | Requerimiento con historial y acciones del rol | /requerimientos/{jobRequest}; pages/job-requests/show.tsx | Aprobación/revisión y trazabilidad del flujo propio |
| 1 | Vacante configurada y validación | /vacantes/{vacancy}; pages/vacancies/show.tsx y CriteriaTable | Perfil, criterios, pesos y publicación controlada |
| 1 | Expediente de postulación | /postulaciones/{application}; pages/applications/show.tsx | Preselección/etapas, programación y separación de información interna |
| 1 | Evaluación o entrevista asignada | /evaluaciones/{evaluation} o /entrevistas/{interview}; pages/assessments/show.tsx | Registro humano de resultados y contexto de sesión |
| 1 | Comparación y decisión humana | /vacantes/{vacancy}/comparacion; pages/selection/comparison.tsx | Ranking explicable, justificación y confirmación explícita RF-23 |

Si se decide una entrega mínima de tres capturas, priorizar vacante, expediente y comparación; el login puede incorporarse como cuarta para mantener el ejemplo de acceso de las plantillas. Cada captura requiere pie con pantalla, rol, escenario ficticio, versión/commit y fecha de la futura sesión.

### Capturas adicionales posibles y pantallas no existentes

| Pantalla | Evidencia y utilidad | Límite |
|---|---|---|
| Panel de inicio | /dashboard; dashboard.tsx | Muestra enlaces por rol, no estadísticas ni «KPIs» |
| Empleos públicos | /empleos y /empleos/{vacancy}; pages/jobs | Portal y búsqueda de vacantes publicadas |
| Perfil y seguimiento propios | /mi-perfil y /mis-postulaciones/{application} | Portal del postulante; ocultar cualquier dato personal real |
| Auditoría | /auditoria; pages/audit/index.tsx | Vista segura, tenant y acciones; rol Aprobador |
| Notificaciones | /notificaciones | Comunicación individual y estados de lectura |
| Riesgo operacional | Detalle de vacante y OperationalRiskCard | Opcional: siempre con etiqueta experimental y explicación sobre procesos |
| Organizaciones / usuarios administrativos / reportes | NO ENCONTRADO módulo de interfaz correspondiente | No fabricar capturas a partir de modelos o de ejemplos de plantillas |
| Pipeline libre o tablero Kanban | NO ENCONTRADO | Las etapas reales se gestionan en el expediente; no existe evidencia de un diseñador de pipeline |
| Firma o contratación | NO ENCONTRADO | El flujo termina en selección/cierre, no en firma de contrato |

Existen 40 archivos de captura versionados en carpetas phase-18, phase-20 y phase-21-screenshots. Son evidencia histórica inventariada; no se certifica en esta fase que sus píxeles correspondan al snapshot actual. Reutilizarlos exige revisar legibilidad, fecha, contenido ficticio y alcance. No se extrajeron ni generaron imágenes nuevas; únicamente se visualizaron en memoria dos imágenes ya incrustadas en las plantillas del usuario.

## 13. Diagramas recomendados

| Diagrama futuro | Objetivo | Elementos y relaciones | Evidencia |
|---|---|---|---|
| Arquitectura AS-IS | Cumplir T1 opcional y T6 arquitectura; explicar el conjunto | Navegador/React/Inertia → Laravel → PostgreSQL y disco privado; Laravel → Redis/worker; ML interno opcional; Docker | §4; routes, servicios, Compose y API |
| Flujo del negocio | Cumplir T6 flujo y T7 funcionamiento | Tres recorridos recomendados en §6, con actores, decisiones y errores; la elección RF-23 debe pertenecer al Aprobador | Enums, workflows y pruebas RF |
| Modelo de datos | Respaldar persistencia y separación lógica | 17 entidades de dominio, notificaciones y tablas de soporte en vista aparte; FK y cardinalidades; candidatos globales | Modelos y 18 migraciones; §7 |
| Aislamiento y autorización | Explicar cómo se preserva la frontera entre organizaciones | Usuario/rol/organización → middleware → Policy/scope/consulta → entidad; excepción de portal público y propiedad del candidato | Scope, trait, Policies y pruebas cross-tenant |
| Secuencia de decisión y cierre, opcional | Mostrar el contrato humano en detalle | Consulta ranking → confirmación → Request → Policy → servicio/transacción → selección → cierre → notificación | FinalDecisionRequest/Service; Closure; tests |
| Integración ML, opcional | Documentar el componente existente sin exagerarlo | Endpoint autorizado → checkpoint → 15 features → token → FastAPI → respuesta validada/fallback | Código Laravel y Python |
| Sandbox, solo si se incluye en el alcance | Separar investigación y producto | Fixtures sintéticos → validaciones → SQLite efímero → revisión simulada → comprobación/purga | F35-SBX-A/B; fuera del diagrama productivo |

Existen especificaciones UML AS-IS en `docs/v1.1/uml/`, modelos y exportaciones PowerDesigner de F23 y modelos académicos F29. Deben cotejarse con la base del futuro depósito. Los BPMN académicos TO-BE, RF candidatos y propuestas de F33 no prueban implementación. No se dibujó ni se regeneró ningún diagrama en esta fase.

## 14. Manual técnico — información disponible

T2 solicita requisitos, instalación, configuración inicial, uso básico y mantenimiento; T6 añade manual de usuario/instalación, glosario e historial como complementos. Aquí se reúne la información disponible, sin ejecutar comandos ni convertir este apartado en el manual final.

### Requisitos

**VERIFICADO:** Git, Docker Desktop/Engine con Compose ≥2.24, puertos configurables y navegador web. PHP/Composer/Node/PostgreSQL/Redis están definidos en contenedores. Python ≥3.12 es necesario para ML/validadores, no para el núcleo Laravel con ML desactivado. `docs/docker.md` registra versiones y pruebas históricas de entorno.

**PENDIENTE DE CONFIRMACIÓN HUMANA:** sistemas operativos a declarar formalmente compatibles, hardware mínimo y recomendado, navegadores/versions probados para el depósito. No copiar Windows/Ubuntu/Python de los ejemplos de T2.

### Instalación

**VERIFICADO:** restauración PHP desde composer.lock y JS desde package-lock.json. La receta soportada está en `docs/docker.md` y el handoff post-F35-SBX. Referencias de comando para el futuro manual, **no ejecutadas**: `docker compose up -d --build --wait`; `docker compose exec -T app composer install --no-interaction --prefer-dist`; `docker compose exec -T app npm ci`; `docker compose exec -T app npm run build`.

El entrypoint puede copiar el entorno, instalar dependencias, generar clave, compilar, migrar y sembrar si se habilita. No es una operación de lectura y requiere un destino local nuevo y ficticio. No utilizar `composer setup` como si fuera una comprobación inocua: contiene instalaciones, generación de clave, migración y npm install. No copiar `pip install -r requirements.txt`, scripts /db o `manage.py` del ejemplo de T2: no describen este proyecto.

### Variables de entorno

**VERIFICADO:** plantillas `.env.example` y `.env.e2e.example`. Solo deben aparecer nombres, finalidad y tratamiento, sin valores privados.

| Grupo | Nombres relevantes | Información para el futuro manual |
|---|---|---|
| Aplicación | APP_NAME, APP_ENV, APP_KEY, APP_DEBUG, APP_URL, APP_PORT, APP_TIMEZONE | Identidad local, entorno, clave generada localmente, zona America/Lima; revisar exposición de debug |
| Base | DB_CONNECTION, DB_HOST, DB_PORT, DB_DATABASE, DB_USERNAME, DB_PASSWORD, DB_URL, FORWARD_DB_PORT | Usar PostgreSQL del entorno previsto; credenciales locales privadas; no apuntar pruebas a una base valiosa |
| Redis | REDIS_CLIENT, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB, REDIS_CACHE_DB, REDIS_PREFIX | Sesiones/cola y caché separados por configuración |
| Caché/sesión/cola | CACHE_STORE, CACHE_PREFIX, SESSION_DRIVER, SESSION_LIFETIME, SESSION_SECURE_COOKIE, QUEUE_CONNECTION | El fallback de config genérica puede diferir del ejemplo Compose; confirmar entorno final |
| Correo | MAIL_MAILER, MAIL_HOST, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, MAIL_FROM_ADDRESS | Driver log en receta de desarrollo; SMTP productivo no acreditado |
| Archivos | FILESYSTEM_DISK, CV_MAX_KB | Disco privado; PDF; máximo documentado configurable de 5120 KiB |
| Demostración/E2E | SEED_ON_BOOT, E2E_ENABLED, E2E_TOKEN, E2E_DATABASE, E2E_APP_PORT | Sin seeding automático para handoff; E2E aislado y descartable |
| ML opcional | ML_SERVICE_ENABLED, ML_SERVICE_URL, ML_SERVICE_TOKEN, ML_SERVICE_CONNECT_TIMEOUT, ML_SERVICE_TIMEOUT, ML_SERVICE_RETRIES | Desactivado por defecto; URL interna; token no versionado; timeout/fallback |
| ML Python | RECRUITMENT_ML_INTERNAL_TOKEN | Mismo secreto compartido por mecanismo seguro; nunca copiarlo al documento |
| Frontend | VITE_APP_NAME | Identidad mostrada; no introducir secretos en variables expuestas al cliente |

Las variables se identificaron en plantillas versionadas y código de configuración, no en los archivos privados del equipo. El valor efectivo del entorno actual es **NO VERIFICADO**.

### Base de datos

**VERIFICADO:** PostgreSQL con migraciones, JSONB, constraints e índice parcial; init SQL crea la base de PHPUnit en volúmenes nuevos. No se ejecutó SQL ni se consultó una base. El futuro manual debe explicar esquema, destino, migraciones y restauración controlada. Los seeders son de demostración; no constituyen datos de una empresa real.

**PENDIENTE DE CONFIRMACIÓN HUMANA:** política de backup, retención, responsable, destino cifrado y prueba de restauración. La frecuencia semanal del ejemplo de T2 no es una política aprobada del SaaS.

### Redis

**VERIFICADO:** servicio Compose, conexiones configurables y healthcheck; worker usa Redis. phpunit.xml fuerza caché/sesión array y cola sync, de modo que esa suite no requiere Redis como servicio. No confundir esto con el funcionamiento normal de la aplicación.

### Frontend

**VERIFICADO:** compilación Vite Plus, React, Inertia, Tailwind y generación Wayfinder. No hay contenedor frontend separado. Los archivos bajo actions/routes/wayfinder y public/build se generan y se ignoran. El build puede descargar fuentes tipográficas; no acredita independencia total de red durante la instalación.

El script build:ssr existe, pero no se encontró un servicio SSR desplegado en Compose ni un entrypoint SSR propio versionado en resources/js; no presentarlo como un modo operativo ya validado.

### Backend

**VERIFICADO:** servidor Laravel, rutas web, Fortify, Policies, servicios, modelos, notificaciones y worker. La ruta /health prueba DB/Redis; /up es una sonda distinta de Laravel. El futuro manual debe explicar ambas y los permisos de cada rol.

No crear ni describir un «usuario administrador» basándose en T2: los roles reales no incluyen ese administrador. El aprovisionamiento de personal y organizaciones del entorno demostrado se realiza mediante seeders; su procedimiento operativo definitivo requiere confirmación.

### Docker

**VERIFICADO:** siete servicios contando el perfil E2E; cuatro volúmenes con nombre; montajes y puertos en §3. La imagen utiliza servidor CLI y está documentada como desarrollo/demostración, no como infraestructura empresarial productiva.

Los datos de postgres/redis sobreviven en volúmenes. No se ejecutaron comandos de arranque, parada, borrado o reconstrucción. El futuro manual debe distinguir parar servicios de eliminar volúmenes y evitar recetas destructivas rutinarias.

### Ejecución

**VERIFICADO:** recetas de acceso local y healthcheck; no se levantó el software. El uso básico debe recorrer los cinco roles y los flujos reales de §6, usando datos ficticios. RF-29 es opcional y el sandbox no se arranca como parte del producto.

**PENDIENTE DE CONFIRMACIÓN HUMANA:** entorno de demostración autorizado para capturas y validación de la versión que se deposite.

### Pruebas

**VERIFICADO:** comandos y precauciones de PHPUnit, componentes, TypeScript, build y Cypress en docs/testing y CI. El futuro manual debe distinguir base PHPUnit de base E2E, token E2E, montajes de storage y efectos de reset. En esta fase no se ejecutó ninguno.

### Mantenimiento

**VERIFICADO:** CHANGELOG, locks, documentación de deuda y scripts de calidad. Las actualizaciones requieren revisión y regresiones proporcionales; no se adopta la periodicidad automática de las plantillas. Los contratos RF, tenant, auditoría y decisión humana deben mantenerse.

**NO ENCONTRADO como procedimiento operativo completo:** monitoreo/SLA productivo, continuidad de negocio, RPO/RTO, rotación de claves institucional, política de soporte o plan de recuperación probado. Datos y responsables: **PENDIENTE DE CONFIRMACIÓN HUMANA**.

## 15. Evidencia de autores y contribuciones

### Evidencia técnica de contribución encontrada en Git

Fuente: `git shortlog -sne HEAD` y recorrido de los 299 commits alcanzables desde la base. Los conteos incluyen merges; no son horas trabajadas, porcentaje de código propio ni reparto de derechos.

| Identidad de autor Git | Correo registrado | Commits | Periodo de autor observable |
|---|---|---:|---|
| luivmz | luisvilameza314@gmail.com | 295 | 13/09/2026–25/10/2026 |
| Luis Antonio Vila Meza | luisvilameza314@gmail.com | 4 | 24/09/2026, 11:50:57–13:00:13 −05:00 |

La coincidencia de correo sugiere alias de una misma persona (**INFERIDO**), pero el vínculo de identidad y su alcance legal son **PENDIENTE DE CONFIRMACIÓN HUMANA**. Los datos Git pueden configurarse; no sustituyen identificación o firma.

Los cuatro commits con el nombre completo son `a925053b434508fd7b1d8ff9bdcc884ae3066a71`, `fff6ae2ad9666baae354c4859cdfa3771fbdc298`, `8ebaf70353da9d245231b32cf6f84c652a32fc76` y `4469128a7363ecc9221999cbc53b2288445d1ad7`: fuentes, entregable, sincronización de gobierno y merge de F24. El historial de la cuenta luivmz registra cambios en backend, frontend, ML y documentación. Esto acredita operaciones registradas por esas identidades, no autoría humana exclusiva de cada archivo.

README y ACADEMIC_BASELINE nombran a **Coronacion Meza Fredy**, **Peña Arroyo Anthony** y **Vila Meza Luis Antonio** como integrantes. Es evidencia documental académica, distinta de Git. No se encontraron commits bajo los dos primeros nombres en el historial alcanzable examinado; no debe inferirse que no hayan contribuido por otros medios.

Se encontraron trailers Co-Authored-By que mencionan herramientas de IA: 154 con la etiqueta Claude Opus 5.5 y 56 con Claude Opus 5. Se documentan como evidencia de asistencia registrada, no como autores naturales ni titulares. La política de atribución y la revisión de aportaciones asistidas requieren decisión humana.

### Información legal que requiere confirmación humana

T3 solicita identificación individual, rol, reconocimiento de coautores, originalidad, autorización al titular, juramento y firma. T4 agrega módulo, periodo y descripción de aportes; su tabla no puede rellenarse asignando automáticamente cargos por el número de commits.

| Persona o identidad encontrada | Información disponible | Información que falta para T3/T4 |
|---|---|---|
| Coronacion Meza Fredy | Nombre en integrantes académicos | Nombre legal, DNI, domicilio, rol oficial, módulos, periodo y firma: PENDIENTE DE CONFIRMACIÓN HUMANA |
| Peña Arroyo Anthony | Nombre en integrantes académicos | Nombre legal, DNI, domicilio, rol oficial, módulos, periodo y firma: PENDIENTE DE CONFIRMACIÓN HUMANA |
| Vila Meza Luis Antonio / Luis Antonio Vila Meza / luivmz | Nombres académicos e identidades Git con correo coincidente | Vinculación de identidades, datos legales, distribución de aportes, titularidad y firma: PENDIENTE DE CONFIRMACIÓN HUMANA |
| Otros posibles colaboradores | NO ENCONTRADO un padrón legal completo | Existencia de otros autores o cesiones: PENDIENTE DE CONFIRMACIÓN HUMANA |

Ni la universidad del curso, ni el colegio del caso de estudio, ni las organizaciones ficticias de seeders se convierten automáticamente en titulares. No se reprodujeron firmas o identificadores personales de los adjuntos académicos.

## 16. Información legal pendiente

La tabla recoge campos pedidos por T1–T8 y por el encargo. Ninguno se completa con los ejemplos de las plantillas, con tax_id de una organización demo ni con inferencias del historial.

| Campo | Estado |
|---|---|
| Título definitivo y versión que se declararán | PENDIENTE DE CONFIRMACIÓN HUMANA |
| Nombre legal completo de cada autor | PENDIENTE DE CONFIRMACIÓN HUMANA |
| DNI u otro identificador de cada autor | PENDIENTE DE CONFIRMACIÓN HUMANA |
| Domicilio completo de cada autor | PENDIENTE DE CONFIRMACIÓN HUMANA |
| Relación completa de coautores | PENDIENTE DE CONFIRMACIÓN HUMANA |
| Rol oficial y descripción individual de aportes | PENDIENTE DE CONFIRMACIÓN HUMANA |
| Periodo oficial de participación de cada autor | PENDIENTE DE CONFIRMACIÓN HUMANA |
| Fecha oficial de creación/finalización de la primera versión funcional | PENDIENTE DE CONFIRMACIÓN HUMANA |
| Año y fecha de publicación a declarar | PENDIENTE DE CONFIRMACIÓN HUMANA |
| Persona natural o jurídica titular; identificación de todos los titulares | PENDIENTE DE CONFIRMACIÓN HUMANA |
| Aplicabilidad del documento de representación empresarial | PENDIENTE DE CONFIRMACIÓN HUMANA |
| Razón social exacta y RUC, si corresponde | PENDIENTE DE CONFIRMACIÓN HUMANA |
| Domicilio legal/fiscal registrado | PENDIENTE DE CONFIRMACIÓN HUMANA |
| Nombre completo y DNI del representante | PENDIENTE DE CONFIRMACIÓN HUMANA |
| Cargo del representante y facultades para el trámite | PENDIENTE DE CONFIRMACIÓN HUMANA |
| Documento y vigencia del poder, si corresponde | PENDIENTE DE CONFIRMACIÓN HUMANA |
| Cadena de derechos patrimoniales y cesiones/licencias aplicables | PENDIENTE DE CONFIRMACIÓN HUMANA |
| Acuerdos laborales, académicos o institucionales relevantes | PENDIENTE DE CONFIRMACIÓN HUMANA |
| Autorización al titular para gestionar el registro | PENDIENTE DE CONFIRMACIÓN HUMANA |
| Declaraciones personales de originalidad/no infracción | PENDIENTE DE CONFIRMACIÓN HUMANA |
| Revisión de licencias y atribuciones de componentes de terceros | PENDIENTE DE CONFIRMACIÓN HUMANA |
| Tratamiento y declaración de asistencia de IA | PENDIENTE DE CONFIRMACIÓN HUMANA |
| Firmas, fecha/lugar de firma y sello, cuando corresponda | PENDIENTE DE CONFIRMACIÓN HUMANA |
| Formulario oficial vigente y modalidad de presentación | PENDIENTE DE CONFIRMACIÓN HUMANA |
| Tarifa, comprobante de pago y datos administrativos vigentes | PENDIENTE DE CONFIRMACIÓN HUMANA |
| Soporte/formato final admitido para el ejemplar y adjuntos | PENDIENTE DE CONFIRMACIÓN HUMANA |

La guía T8 contiene referencias administrativas fechadas, enlaces, plazos y afirmaciones sobre derechos. Esta auditoría técnica no verificó su vigencia normativa ni los presenta como hechos actuales. Deben contrastarse con la autoridad y/o asesoría correspondiente antes de una presentación; no se realiza aquí una solicitud, pago, declaración o conclusión jurídica.

## 17. Matriz documento por documento

### Fuentes de requisitos aportadas por el usuario

Se identifican con T1–T8 para poder rastrear requisitos sin copiar ejemplos. Todos son DOCX locales agregados manualmente por el usuario durante la auditoría; no pertenecían al inventario Git inicial ni fueron generados por Codex. Se leyeron el XML de párrafos/tablas y dos imágenes incrustadas directamente en memoria, sin conversiones, edición ni archivos auxiliares.

| ID | Plantilla local conservada | Bytes | SHA-256 al recibir la actualización |
|---|---|---:|---|
| T1 | [Documento 1 - Ficha técnica de software.docx](<registro-software-indecopi/Plantillas/Documento 1 - Ficha técnica de software.docx>) | 18226 | `d41b0a7eb25d5b71f3c45acbbd4df038001ce313509a5c57f1ec6837795a6ed5` |
| T2 | [Documento 2 - Ejemplar del software.docx](<registro-software-indecopi/Plantillas/Documento 2 - Ejemplar del software.docx>) | 18024 | `f1c4242d7cc59ebb6643e8523c6b17e66b183d6307d41bb67905747663f1dc90` |
| T3 | [Documento 3 - Declaración jurada de auditoría.docx](<registro-software-indecopi/Plantillas/Documento 3 - Declaración jurada de auditoría.docx>) | 21426 | `6d805eb4b1fae0199fd75296d31923bd6020fd4c3d184e5b4aeae9fb2013dfe7` |
| T4 | [Documento 4 - Lista de autores y roles.docx](<registro-software-indecopi/Plantillas/Documento 4 - Lista de autores y roles.docx>) | 18432 | `8ef7dccd05152a67b7dbba10a906e72d5238afea95cf42567ab55448e1285521` |
| T5 | [Documento 5 - Representación legal de la empresa.docx](<registro-software-indecopi/Plantillas/Documento 5 - Representación legal de la empresa.docx>) | 17291 | `f1df36af8bf877791585b2280888da67187573bcef19ea0d599f5dd3f6a85bdd` |
| T6 | [Documento 6 - Anexos técnicos.docx](<registro-software-indecopi/Plantillas/Documento 6 - Anexos técnicos.docx>) | 17817 | `e49268c50883d97854eaf2d5c8b8a750a4e77a74d62bb95441d84d6eb51fa97f` |
| T7 | [Plantilla_Registro_General_Software.docx](<registro-software-indecopi/Plantillas/Plantilla_Registro_General_Software.docx>) | 53226 | `c6d4c6e1846805156e3f545cf19401cd054420871c43f00ac5aa2a3fc380d78f` |
| T8 | [Registro_Software_INDECOPI.docx](<registro-software-indecopi/Plantillas/Registro_Software_INDECOPI.docx>) | 30019 | `c39a7be467413e4f2158b92036ee2067ba96caed6c5a6ce0a7e5ea761f50adf2` |

Los títulos/secciones de las plantillas se usan como localizadores. No se asignan números de página sin render. No se revisó maquetación ni se certifica que estas referencias sean formularios oficiales vigentes.

**Significado de los estados:** LISTO indica que un dato o insumo técnico está disponible y respaldado, no que se haya creado un documento final. PARCIAL indica que existe una base reutilizable con límites o faltantes. REQUIERE INFORMACIÓN HUMANA identifica decisiones/datos personales, administrativos o legales. REQUIERE PRODUCIR EVIDENCIA identifica una captura, anexo, selección, ejecución o ensamblado que aún no se realizó.

### Comparación explícita con cada plantilla

| Documento | Requisito de la plantilla | Información encontrada en el SaaS | Evidencia | Falta | Estado |
|---|---|---|---|---|---|
| Documento 1 — Ficha técnica | T1 §1: título único/representativo y versión | Denominaciones descriptivas y tag académico v1.1 | README, app.tsx, Git tags; §2 | Aprobar título y versión exactos del depósito | REQUIERE INFORMACIÓN HUMANA |
| Documento 1 — Ficha técnica | T1 §2: lenguajes y librerías principales | PHP, TypeScript/JS, SQL; Python opcional experimental | Locks, Dockerfile, pyproject; §3 | Decidir si el alcance incluye componente ML | PARCIAL |
| Documento 1 — Ficha técnica | T1 §3: funcionalidad principal concreta | Proceso de reclutamiento RF-01–27 con decisión humana | Inventario y flujos §§5–6 | Redacción final coherente con el título aprobado | LISTO |
| Documento 1 — Ficha técnica | T1 §4: conclusión de primera versión funcional y periodo | Periodo de commits y tags académicos | Git y documentos de cierre | Fecha oficial, diferenciada de metadatos Git | REQUIERE INFORMACIÓN HUMANA |
| Documento 1 — Ficha técnica | T1 §5: arquitectura opcional y componentes | Monolito Laravel/Inertia; PostgreSQL/Redis; ML opcional | Código, Compose; §4 | Gráfico final y decisión de incluir sandbox | REQUIERE PRODUCIR EVIDENCIA |
| Documento 1 — Ficha técnica | T1 §6: observaciones consistentes | Restricciones académicas, datos ficticios y alcance | CLAUDE, PROGRESS y §2 | Revisión del texto final por el equipo | PARCIAL |
| Documento 2 — Ejemplar | T2 §1: código fuente o ejecutable representativo, limpio | Rutas y fragmentos propios identificados | §11; app y resources/js | Selección aprobada, exportación y manifest del ejemplar | REQUIERE PRODUCIR EVIDENCIA |
| Documento 2 — Ejemplar | T2 §1: estructura y documentación adjunta | app, resources/js, database/migrations y docs | Inventario Git; §22 | Adaptar estructura real; no usar carpetas del ejemplo ajeno | PARCIAL |
| Documento 2 — Ejemplar | T2 §2.1: requisitos de SO, lenguaje, DB y navegador | Entorno Docker y versiones configuradas | Dockerfile, Compose, docs/docker | Mínimos de hardware y matriz de compatibilidad probada | PARCIAL |
| Documento 2 — Ejemplar | T2 §2.2–2.3: instalación/configuración inicial | Locks, entrypoint, variables y recetas | §14; handoff y docs/docker | Manual ensamblado y recorrido comprobado en fase autorizada | REQUIERE PRODUCIR EVIDENCIA |
| Documento 2 — Ejemplar | T2 §2.4: uso básico | Flujos por los cinco roles reales | §6; páginas y E2E | Texto/ilustraciones finales; no inventar administrador ni reportes | REQUIERE PRODUCIR EVIDENCIA |
| Documento 2 — Ejemplar | T2 §2.5: mantenimiento e historial | CHANGELOG, deudas y controles de versión | §14; documentación de release | Política de backup, soporte y actualización aprobada | REQUIERE INFORMACIÓN HUMANA |
| Documento 2 — Ejemplar | T2 §3: al menos tres capturas claras, sin datos sensibles | Seis pantallas prioritarias existentes; capturas históricas | §12; React y rutas | Capturas del alcance elegido, pies y revisión de datos ficticios | REQUIERE PRODUCIR EVIDENCIA |
| Documento 3 — Declaración de autoría | T3 §2: nombre, DNI, domicilio y título | Nombres académicos e identidades Git | §15; README; Git | Identidad legal completa y título definitivo | REQUIERE INFORMACIÓN HUMANA |
| Documento 3 — Declaración de autoría | T3 §3: rol, lenguajes, función y participación | Stack y componentes; operaciones registradas en Git | §§3, 5 y 15 | Rol y aportes individuales confirmados, no deducidos | REQUIERE INFORMACIÓN HUMANA |
| Documento 3 — Declaración de autoría | T3 §4: coautores y declaración de cada uno | Tres integrantes nombrados; padrón legal no establecido | README; baseline | Lista completa, DNI y declaraciones individuales | REQUIERE INFORMACIÓN HUMANA |
| Documento 3 — Declaración de autoría | T3 §5: originalidad y no infracción | Elementos técnicos propios y dependencia de terceros | §10; locks; historial | Revisión de derechos/licencias y declaración de cada firmante | REQUIERE INFORMACIÓN HUMANA |
| Documento 3 — Declaración de autoría | T3 §6: titular/RUC y autorización | No se acredita titular patrimonial | §16 | Determinar titular, cadena de derechos y autorización aplicable | REQUIERE INFORMACIÓN HUMANA |
| Documento 3 — Declaración de autoría | T3 §7–8: juramento, firma y fecha | NO ENCONTRADO instrumento individual de registro confirmado | Plantilla y §16 | Decisión, firma y fecha por cada persona; sin generar firmas | REQUIERE INFORMACIÓN HUMANA |
| Documento 4 — Autores y roles | T4 §2–3: identificación del software y tabla de seis campos | Base Git, nombres y componentes | §15; Git | Nombre legal/DNI, rol, módulo, periodo y detalle individual aprobados | REQUIERE INFORMACIÓN HUMANA |
| Documento 4 — Autores y roles | T4 §4: explicación de funciones del equipo | Existen backend, frontend, datos y QA | Código e inventario | Asignación real de esas funciones a personas | REQUIERE INFORMACIÓN HUMANA |
| Documento 4 — Autores y roles | T4 §5–6: validación, representante, cargo, firma y fecha | NO ENCONTRADO representante autorizado para este expediente | §16 | Titular/aplicabilidad y validación por quien corresponda | REQUIERE INFORMACIÓN HUMANA |
| Documento 5 — Representación legal | T5 §2: razón social, RUC, domicilio legal y software | Caso académico y organizaciones ficticias; no empresa titular acreditada | Organization y README | Determinar si aplica persona jurídica; documentos empresariales reales | REQUIERE INFORMACIÓN HUMANA |
| Documento 5 — Representación legal | T5 §3: representante, DNI, cargo y vigencia de poder | NO ENCONTRADO en la evidencia técnica una representación válida del titular | §16 | Datos y documento de poder vigente, si corresponde | REQUIERE INFORMACIÓN HUMANA |
| Documento 5 — Representación legal | T5 §4–6: titularidad, facultades y responsabilidad | Git no demuestra esos extremos | §15; catálogo de dependencias | Cadena de derechos, facultades y revisión humana de declaraciones | REQUIERE INFORMACIÓN HUMANA |
| Documento 5 — Representación legal | T5 §7: firma, sello y fecha | NO ENCONTRADO documento final del expediente | Plantilla | Firma/datos autorizados; no copiar los ejemplos | REQUIERE INFORMACIÓN HUMANA |
| Documento 6 — Anexos | T6 §1: flujo del sistema, notación y legibilidad | Tres flujos reales recomendados | §§6 y 13; servicios y enums | Diagramas específicos del depósito | REQUIERE PRODUCIR EVIDENCIA |
| Documento 6 — Anexos | T6 §2: arquitectura y relaciones entre componentes | Reconstrucción del monolito y sus fronteras | §§3–4 y 13; Compose | Lámina final; no asumir nube ni escalamiento probado | REQUIERE PRODUCIR EVIDENCIA |
| Documento 6 — Anexos | T6 §3: capturas de módulos clave, al menos tres | Pantallas reales y límites identificados | §12 | Conjunto final fechado con escenarios ficticios | REQUIERE PRODUCIR EVIDENCIA |
| Documento 6 — Anexos | T6 §4: QA funcional e integración | Pruebas existentes y resultados históricos F25/F26 | §9; tests y E2E | Resumen con base y fecha, y decidir si requiere ejecución nueva | PARCIAL |
| Documento 6 — Anexos | T6 §4: seguridad y rendimiento | Controles estáticos y exploración histórica, con pendientes | §§8–9; reportes QA | Evidencia adicional si se desean afirmaciones de carga/seguridad actual | REQUIERE PRODUCIR EVIDENCIA |
| Documento 6 — Anexos | T6 §5: manual usuario/instalación, glosario e historial opcionales | Recetas, flujos, diccionarios/estados y CHANGELOG | §14; documentación existente | Ensamblar y revisar coherencia del paquete final | PARCIAL |
| Plantilla general | T7 Anexo 1: título, tipo, lenguajes, framework, autores y titular opcional | Datos técnicos disponibles; datos legales sin aprobar | §§2–3, 15–16 | Decisiones legales; no asumir que debe existir empresa | PARCIAL |
| Plantilla general | T7 Anexo 1: 10–15 páginas de código representativo | Archivos, métodos, rangos y estimación identificados | §11 | Paginar, revisar secretos/licencias y fijar manifest de extractos | REQUIERE PRODUCIR EVIDENCIA |
| Plantilla general | T7 Anexo 2: título, versión, autores y año | Nombres/versiones técnicas y periodo Git | §§2 y 15 | Valores oficiales comunes a todo el paquete | REQUIERE INFORMACIÓN HUMANA |
| Plantilla general | T7 Anexo 2 §§1–3: propósito, estructura y características | Funciones y arquitectura reales reconstruidas | §§4–8 | Resumen final, evitando JWT/exportaciones/otros ejemplos no implementados | PARCIAL |
| Plantilla general | T7 Anexo 2 §4: originalidad | Elementos técnicos descritos con evidencia | §10 | Revisión y conclusión humana; no inferir por presencia de ML | REQUIERE INFORMACIÓN HUMANA |
| Plantilla general | T7 Anexo 2 §5: entorno y requisitos | Docker y versiones declaradas, PostgreSQL/Redis | §§3 y 14 | Compatibilidad y recursos mínimos confirmados | PARCIAL |
| Plantilla general | T7 Anexo 2 §6: imágenes opcionales | Propuesta de capturas, arquitectura, flujos y estructura | §§12–13 | Producción posterior autorizada | REQUIERE PRODUCIR EVIDENCIA |
| Guía general INDECOPI | T8 §2: formulario, autores/titulares y datos del trámite | NO ENCONTRADO un formulario oficial vigente completado para este SaaS | Plantilla; §16 | Confirmación humana y fuente administrativa vigente | REQUIERE INFORMACIÓN HUMANA |
| Guía general INDECOPI | T8 §2: ejemplar y descripción técnica de 1–3 páginas | Base técnica suficiente para redactarlos | §§4–11; matriz anterior | Documento breve y ejemplar final; no son este informe extenso | REQUIERE PRODUCIR EVIDENCIA |
| Guía general INDECOPI | T8 §2–3: comprobante y modalidad/formatos de presentación | NO ENCONTRADO comprobante o decisión de modalidad de este expediente | §16 | Requisitos y pago vigentes confirmados por el responsable | REQUIERE INFORMACIÓN HUMANA |
| Guía general INDECOPI | T8 §§4–5: plazos, resultado y derechos | Son afirmaciones de una referencia aportada, no evidencia del software | T8 | Verificar vigencia; no usarlas como conclusión jurídica de la auditoría | REQUIERE INFORMACIÓN HUMANA |

### Anexos técnicos adicionales que sí pueden prepararse

Para ampliar T6 sin inventar funcionalidades, se puede producir posteriormente: mapa backend/frontend con rutas; ER de las entidades reales; explicación del aislamiento por organización y pruebas negativas; controles de CV y auditoría; matriz QA con resultados fechados; infraestructura Compose con puertos y volúmenes; y secuencia del ML experimental si entra en el alcance. El informe identifica sus fuentes, pero no produce esos anexos finales.

T2 propone código o ejecutable, mientras T7 concreta un extracto de 10–15 páginas. El plan actual responde al extracto solicitado. El eventual ZIP de código, instalador, dump SQL, formato de entrega o ejecutable **no se da por obligatorio ni se genera** sin decisión humana sobre el soporte requerido.

## 18. Inconsistencias o riesgos documentales

Estos son riesgos para la preparación fiel del expediente; no se han corregido y no implican por sí solos una vulnerabilidad de producción.

| ID | Hallazgo | Evidencia / impacto | Tratamiento posterior |
|---|---|---|---|
| RD-01 | Varias denominaciones del proyecto | README, CLAUDE y appName; puede variar el título entre documentos | Aprobar una ficha de campos canónicos |
| RD-02 | Versión académica vs snapshot post-release | Tag v1.1 en 634f354, base actual b8892af | Elegir versión/commit del depósito; no llamar v1.0 a todo por un ejemplo |
| RD-03 | Fecha Git no equivale a fecha oficial de creación | Primer commit y tags no certifican fin de primera versión | Confirmación humana de T1/T7 |
| RD-04 | Integrantes académicos distintos de identidades de commits | Tres nombres documentales; dos identidades Git con mismo correo | Confirmar padrón y aportes; no excluir ni asignar roles automáticamente |
| RD-05 | Titularidad empresarial no acreditada | tax_id/modelo Organization y caso escolar no son título patrimonial | Determinar persona natural/jurídica y aplicabilidad de T5 |
| RD-06 | T3 mezcla «Autoría» y «Auditoría» | Nombre del archivo y ejemplo final difieren del título inicial | Conservar la plantilla; aprobar después el título del documento real |
| RD-07 | Ejemplos de otros proyectos | T1–T7 contienen tecnologías y módulos ajenos | No copiar nombres, empresas, DNI/RUC, direcciones, fechas ni código ajeno |
| RD-08 | T5 presupone empresa; T7 la trata como opcional | Divergencia de aplicabilidad de las referencias | Confirmación humana; no inventar empresa o representante |
| RD-09 | Datos administrativos de T8 fechados | Tarifa y referencias de trámite no verificadas ahora | Validar vigencia en fase administrativa; no presentarlos como actuales |
| RD-10 | Ficha podría exagerar «SaaS empresarial» | No hay billing, onboarding de empresas o despliegue productivo demostrado | Describir arquitectura multiempresa y alcance académico |
| RD-11 | Dashboard puede confundirse con analítica | dashboard.tsx es índice de accesos | No prometer gráficos, KPIs ni RF-28 implementado |
| RD-12 | Plazas múltiples no equivalen a selección múltiple | A-29; decisión única e índice parcial | Declarar límite de un seleccionado por vacante en el MVP |
| RD-13 | Estado «desierta» no es un flujo | Enum/esquema y A-30 | No incluir cierre sin selección en manual o capturas |
| RD-14 | Riesgo de atribuir IA decisoria | RF-29 operacional; F33 es propuesta; SBX es sintético | Separar módulos, fronteras y estados de gobierno |
| RD-15 | Configuración genérica aparenta soportar otros motores | config/database y filesystem conservan opciones del framework | PostgreSQL es la ruta soportada; no prometer MySQL/S3/SQL Server |
| RD-16 | Defaults genéricos pueden diferir del entorno documentado | Config fallback database/SQLite vs receta PostgreSQL/Redis | Explicar variables requeridas y no inferir el .env privado |
| RD-17 | Documentos históricos conservan estados antiguos | Release manifest/notes, scope-preliminary, README ML y cierres de fases | Usar gobierno vigente y Git; conservar la historia |
| RD-18 | Resultados QA históricos no son una ejecución actual | F25/F26 frente a esta lectura estática | Citar base, fecha, suite y omisiones; no inventar cobertura o métricas |
| RD-19 | Capturas antiguas no prueban cada pixel actual | Carpetas F18/F20/F21 | Revisar/reproducir en fase autorizada con datos ficticios |
| RD-20 | Licencia/autoría no se resuelven por metadatos del starter | composer conserva laravel/react-starter-kit; no LICENSE raíz específico | Revisar alcance propio, dependencias y derechos con humanos |
| RD-21 | Asistencia IA registrada | Trailers Co-Authored-By | Confirmar tratamiento y atribuciones sin declarar a la herramienta autor natural |
| RD-22 | Filtros de auditoría no garantizan ausencia semántica de PII | AuditLogger por clave; comentarios libres posibles | Descripción precisa de controles, sin afirmar anonimización universal |
| RD-23 | Plantillas son archivos locales sin commit | Ocho archivos aportados por el usuario | Preservar hashes; su publicación requiere decisión posterior |
| RD-24 | Gates congelados pueden fallar en HEAD posterior | Contratos del cierre/handoff, reglas de contexto/gobierno/alcance | No reinterpretar fallas de ciclo de vida como regresión; no ejecutar ahora |
| RD-25 | Seguridad/operación productivas no certificadas | Docker dev, pendientes de privacidad y QA manual | Evitar afirmaciones «listo para uso empresarial» del ejemplo T6 |

**Deuda existente GC-AF-L01:** LOW, ABIERTO / DIFERIDO, no bloqueante para F35-SBX. Afecta a la enumeración de un destino externo si un padre de una raíz protegida es una unión/punto de reanálisis. Según el registro, FSY/SBX siguen fallando cerrado sin falso PASS. No es una vulnerabilidad productiva demostrada. Se recomienda revisar componentes padre y añadir regresión en un incremento separado, sin tocar la capa congelada. Fuente: `docs/academico/TECHNICAL_DEBT.md`. No depende del archivo local antiguo de deuda.

Las observaciones de formato, modelos/diagramas y QA manual F25/F26/F31 son antecedentes documentados, no trabajos autorizados en esta fase. Ninguna plantilla permite reabrir F35-SBX o iniciar F36.

## 19. Campos que deben permanecer coherentes en todos los documentos

| Campo canónico futuro | Información candidata sustentada | Regla de coherencia |
|---|---|---|
| Título del software | Denominaciones de §2 | Una denominación aprobada idéntica en T1–T7, firmas y anexos |
| Versión y commit | Tag académico y base b8892af | Diferenciar versión del producto, componente ML y snapshot del depósito |
| Tipo | Aplicación/plataforma web | No afirmar móvil nativa, ERP o escritorio |
| Descripción | Gestión del reclutamiento hasta cierre con decisión humana | Igual alcance funcional en ficha, resumen, manual y ejemplar |
| Stack | Versiones verificadas de §3 | No intercambiar requisitos, versiones resueltas y runtime ejecutado |
| Base y persistencia | PostgreSQL y esquema compartido | No declarar base por tenant ni MySQL por defaults del framework |
| Multiempresa | Scopes, Policies y consultas explícitas | Explicar candidato global y límites del scope |
| Autores | Padrón humano confirmado, con Git como evidencia complementaria | Mismo orden/nombres legales y roles validados en lista y declaraciones |
| Titular | PENDIENTE DE CONFIRMACIÓN HUMANA | No confundir organización demo, colegio, universidad y titular |
| Fechas | Periodo Git observable separado de fechas oficiales | Año/fecha idénticos una vez confirmados; no copiar ejemplos |
| Roles del producto | Cinco roles de UserRole | No añadir Administrador/SuperAdmin sin código y autorización |
| RF-23 | Decisión humana, confirmación y justificación | No describir selección automática por ranking o ML |
| RF-29 | Experimental, operacional y opcional | Mismo rotulado en capturas, arquitectura, código y descripción |
| Sandbox | Académico/sintético, congelado | No mezclar sus SQLite/pipeline con PostgreSQL o runtime del SaaS |
| Datos/capturas | Exclusivamente ficticios | No incluir documentos, credenciales, nombres o expedientes reales |
| QA | Resultados con fuente, fecha/base y límites | No presentar pruebas existentes como ejecutadas ahora |
| Código representativo | Fragmentos de §11 con manifest posterior | Rutas/rangos/hash y versión consistentes con capturas y arquitectura |
| Documentos legales | Aplicabilidad, poderes y firmas confirmados | No firmar ni completar automáticamente información faltante |

## 20. Checklist maestro

### Ya disponible

- [x] Base Git publicada, tree, tags y periodo observable identificados.
- [x] Rama documental separada, creada desde el main publicado por instrucción específica del usuario.
- [x] Inventario de código, rutas, modelos, migraciones, frontend, tests e infraestructura.
- [x] Stack contrastado con manifests/locks, con versiones declaradas y resueltas diferenciadas.
- [x] Explicación de multiempresa, autorización, ranking y decisión humana.
- [x] Separación entre producto, ML experimental, sandbox y propuestas.
- [x] Resultados QA históricos localizados, sin atribuir nueva ejecución.
- [x] Selección de archivos/fragmentos para aproximadamente 10–15 páginas.
- [x] Recomendación de seis capturas y diagramas basados en pantallas/código reales.
- [x] Ocho plantillas leídas y requisitos cotejados, sin copiar sus ejemplos.
- [x] Hashes iniciales de las plantillas registrados para comprobar conservación.
- [x] Pendientes legales y documentales enumerados.

### Requiere confirmación humana

- [ ] Título y versión exactos del registro; alcance de ML/sandbox en el ejemplar.
- [ ] Padrón completo de autores, identidades legales, DNI, domicilios y roles.
- [ ] Aportes/periodos individuales y tratamiento de asistencia IA.
- [ ] Fecha oficial de creación, finalización y publicación.
- [ ] Titular natural/jurídico; cesiones/licencias y relación académica/laboral.
- [ ] Aplicabilidad de representación legal, RUC, domicilio y poderes.
- [ ] Declaraciones de originalidad/no infracción, autorizaciones y firmas.
- [ ] Datos administrativos vigentes, modalidad, formato y pago.
- [ ] Política operativa de backup/soporte y compatibilidad a declarar.
- [ ] Publicación o versionado posterior de plantillas y documentos.

### Debe producirse posteriormente

- [ ] Ficha técnica final, con campos humanos confirmados.
- [ ] Extracto de 10–15 páginas con procedencia, revisión y manifest.
- [ ] Resumen funcional breve; T8 propone 1–3 páginas como referencia.
- [ ] Manual técnico/instalación y uso básico por roles.
- [ ] Capturas finales claras y ficticias con pies, versión y fecha.
- [ ] Diagramas AS-IS de arquitectura, flujos y datos, cotejados con el código.
- [ ] Resumen QA que diferencie evidencia histórica y nueva, si se autoriza ejecutarla.
- [ ] Lista de autores/roles y declaraciones individuales revisadas por humanos.
- [ ] Documentación del titular/representante, únicamente si corresponde.
- [ ] Revisión cruzada de consistencia y de ausencia de secretos antes de cualquier entrega.

## 21. Recomendación para la siguiente fase

1. Revisar este informe y aprobar una hoja única de título, versión/commit, alcance y responsables.
2. Recoger de las personas autorizadas los campos de §16 y confirmar quién es autor y quién es titular.
3. Decidir qué partes de las referencias son aplicables; resolver la ambigüedad del título de T3 y la condicionalidad de T5 sin modificar las plantillas originales.
4. Preparar en una nueva fase autorizada los extractos, manual, resumen, capturas y diagramas. Empezar por código del proceso/tenant y seis pantallas de §12.
5. Si se requiere nueva evidencia QA o reproducibilidad de instalación, autorizar expresamente un entorno aislado y sus escrituras; no reutilizar una ejecución histórica como resultado actual.
6. Contrastar los requisitos administrativos vigentes antes de preparar o firmar documentación legal.
7. Revisar coherencia, datos ficticios, licencias y secretos en el conjunto. El versionado/publicación posterior sigue pendiente de autorización.

Esta recomendación no inicia F36, no propone corregir código durante la auditoría y no produce documentos finales de registro.

## 22. Evidencia técnica consultada

### Método y dimensión

Se inventariaron los 1.213 archivos de Git y se leyeron para búsquedas/recorridos estáticos 1.038 archivos textuales UTF-8; 175 binarios o no UTF-8 se clasificaron sin revisión visual integral. Dentro del recorrido inicial se extrajeron datos de 491 archivos de código/configuración/pruebas del núcleo y se realizó lectura dirigida de las piezas críticas citadas en el informe. Se leyeron ocho DOCX adicionales del usuario, incluyendo su tabla y dos imágenes incrustadas, directamente en memoria. Por tanto, hubo aproximadamente **1.046 archivos con inspección textual/documental**, de distinta profundidad; esto no equivale a ejecutar ni revisar visualmente cada artefacto.

Las técnicas utilizadas fueron lectura de archivos, Git, búsqueda de texto, lectura estructurada de JSON y de configuración TOML, extracción de símbolos y XML/ZIP de las plantillas. No se importaron módulos del repositorio para ejecutar sus funciones. No se crearon scripts auxiliares, manifests nuevos, logs, imágenes o temporales dentro del repositorio.

### Gobierno, alcance e historia

- [README](../README.md), [CLAUDE](../CLAUDE.md) y [AGENTS](../AGENTS.md).
- [PROGRESS](PROGRESS.md) y [ACADEMIC_BASELINE](academico/ACADEMIC_BASELINE.md).
- [Alcance preliminar](v1.1/scope-preliminary.md), [mapa de evolución](v1.1/documentation-update-map.md).
- [Trazabilidad RF](final-report/traceability-master.md), [reglas/assumptions](assumptions.md), [defectos](defects.md).
- [QA F25](v1.1/phase-25-final-qa.md), [matriz QA](v1.1/phase-25-qa-matrix.md), [cierre F26](v1.1/phase-26-release-closeout.md).
- [Release notes](v1.1/release-notes-v1.1.md), [release manifest](v1.1/release-manifest-v1.1.md), [CHANGELOG](../CHANGELOG.md).
- [Deuda técnica](academico/TECHNICAL_DEBT.md), [deuda de gobierno](academico/GOVERNANCE_DEBT.md).
- [Handoff vigente](academico/handoff/F35SBX_SECONDARY_PC_HANDOFF.md) y receta F34E enlazada desde él.
- [ADR-005/G0](academico/diseno-inteligente/F33_ADR_005_G0.md), cierre F35-SBX y evidencias de B2/B3.

### Stack e infraestructura

- [composer.json](../composer.json), [composer.lock](../composer.lock), [package.json](../package.json), [package-lock.json](../package-lock.json).
- [Dockerfile](../docker/php/Dockerfile), [Compose](../docker-compose.yml), [entrypoint](../docker/php/entrypoint.sh), scripts init PostgreSQL/E2E.
- [Docker y portabilidad](docker.md), [Cypress](testing/cypress-e2e.md), [workflow tests](../.github/workflows/tests.yml).
- [Vite](../vite.config.ts), [TypeScript](../tsconfig.json), [PHPUnit](../phpunit.xml), [PHPStan](../phpstan.neon), [Pint](../pint.json).
- .env.example y .env.e2e.example: solo plantillas; .gitignore y .dockerignore. No se consultaron entornos privados.

### Backend y persistencia

- [Rutas web](../routes/web.php), [settings](../routes/settings.php), [bootstrap](../bootstrap/app.php) y providers.
- [User](../app/Models/User.php), [OrganizationScope](../app/Models/Scopes/OrganizationScope.php), [trait de organización](../app/Models/Concerns/BelongsToOrganization.php).
- Los 17 modelos de dominio, Policies y 18 migraciones descritos en §7.
- [JobRequestWorkflow](../app/Services/JobRequests/JobRequestWorkflow.php), [VacancyService](../app/Services/Vacancies/VacancyService.php), [VacancyValidator](../app/Services/Vacancies/VacancyValidator.php).
- [ApplicationService](../app/Services/Applications/ApplicationService.php), [ApplicationStageService](../app/Services/Applications/ApplicationStageService.php), CandidateProfileService y Requests de CV.
- [AssessmentScheduler](../app/Services/Assessments/AssessmentScheduler.php), [AssessmentResultRecorder](../app/Services/Assessments/AssessmentResultRecorder.php), ScoreSheetValidator y WeightingValidator.
- [RankingService](../app/Services/Ranking/RankingService.php), [VacancyRankingBuilder](../app/Services/Ranking/VacancyRankingBuilder.php).
- [FinalDecisionRequest](../app/Http/Requests/Selection/FinalDecisionRequest.php), [FinalDecisionService](../app/Services/Selection/FinalDecisionService.php), SelectionRegistrationService y VacancyClosureService.
- [AuditLogger](../app/Services/Audit/AuditLogger.php), [AuditLogResource](../app/Http/Resources/AuditLogResource.php), AuditLog y trigger.
- RecruitmentNotification, ProcessResultNotification, NotificationController, HealthController y protecciones E2E.

### Frontend y pruebas

- [App Inertia](../resources/js/app.tsx), pages, layouts, lib/navigation y estilos.
- [Dashboard](../resources/js/pages/dashboard.tsx), [comparación/decisión](../resources/js/pages/selection/comparison.tsx), [DataTable](../resources/js/components/data-table.tsx).
- Perfil/expediente, empleos, vacantes, evaluaciones, auditoría, notificaciones y ajustes citados en §5.
- Componentes experience-3d, use-scene-capability, lib/motion y OperationalRiskCard.
- [CrossTenantAccessTest](../tests/Feature/Tenancy/CrossTenantAccessTest.php), [FinalDecisionTest](../tests/Feature/Selection/FinalDecisionTest.php), [RankingServiceTest](../tests/Unit/Ranking/RankingServiceTest.php).
- Otros tests Feature/Unit del inventario y veinte specs cypress/e2e; seis pruebas de componente.
- Carpetas históricas phase-18/20/21-screenshots: inventario y documentación, no nuevas capturas.

### ML, sandbox y modelos documentales

- [Pyproject](../ml-service/pyproject.toml), [README ML](../ml-service/README.md), src/recruitment_ml/api, training, synthetic y serving; tests asociados.
- [OperationalRiskService](../app/Services/Ml/OperationalRiskService.php), [MlRiskClient](../app/Services/Ml/MlRiskClient.php), FeatureBuilder y config/ml.php.
- Dataset/manifest sintético F34; sbxb_store.py y sbxb_pipeline.py; gates de congelación/cierre como evidencia estática.
- [Manifiesto de modelos F29](academico/powerdesigner/MANIFEST.md), especificaciones UML y modelos/exportaciones F23/F29, sin regenerarlos.
- Las ocho plantillas de §17, con hashes y localizadores por sección, son la fuente documental de campos. No se atribuye a sus ejemplos valor de evidencia técnica del SaaS.

## 23. Verificación final del repositorio

### Estado inicial y rama

El inicio registró `feature/f35-sbx-b2-ephemeral-store`, HEAD `89694244b81b0bd84dbe6ae5d04b5c7a198bafef`, con working tree limpio. Se ejecutaron primero git status, branch, remote y log conforme al encargo.

El main local estaba en `ecc9e73393600bf755fd2542677a2568c04aa7ce`, atrasado respecto del remoto. Se explicó al usuario y se creó **solo la rama nueva** desde origin/main verificado, mediante `git switch --no-track -c docs/registro-software-indecopi origin/main`. No se actualizó ni reescribió el main local. La instrucción específica de partir del main publicado se aplicó como excepción al flujo genérico desde develop.

Base de la rama: `b8892af39a6492d8dd44a36290604efc602380cd`; remoto fetch/push canónico: `https://github.com/luivmz/saas-reclutamiento-multiempresa.git`. Se registraron 299 commits alcanzables y las identidades descritas en §15; los últimos merges relevantes son el handoff y el cierre F35-SBX identificados en §2.

### Archivos agregados manualmente por el usuario

Durante la auditoría el usuario informó la incorporación de los siguientes ocho archivos. Son aportes ajenos autorizados, conservados sin editar, renombrar, mover, eliminar o convertir:

- `docs/registro-software-indecopi/Plantillas/Documento 1 - Ficha técnica de software.docx`
- `docs/registro-software-indecopi/Plantillas/Documento 2 - Ejemplar del software.docx`
- `docs/registro-software-indecopi/Plantillas/Documento 3 - Declaración jurada de auditoría.docx`
- `docs/registro-software-indecopi/Plantillas/Documento 4 - Lista de autores y roles.docx`
- `docs/registro-software-indecopi/Plantillas/Documento 5 - Representación legal de la empresa.docx`
- `docs/registro-software-indecopi/Plantillas/Documento 6 - Anexos técnicos.docx`
- `docs/registro-software-indecopi/Plantillas/Plantilla_Registro_General_Software.docx`
- `docs/registro-software-indecopi/Plantillas/Registro_Software_INDECOPI.docx`

### Archivo generado por Codex

- `docs/REPORTE_AUDITORIA_DOCUMENTAL.md`, este informe.
- No se generaron documentos finales de registro, DOCX, PDF, imágenes, diagramas, ejecutables ni archivos auxiliares.

### Resultado de la comprobación de cierre

**VERIFICADO en esta sesión:** la rama activa es `docs/registro-software-indecopi` y HEAD continúa en la base `b8892af39a6492d8dd44a36290604efc602380cd`, sin nuevos commits. Git muestra exactamente nueve archivos sin seguimiento: las ocho plantillas del usuario listadas arriba y el Markdown de Codex. No hay archivos versionados modificados, eliminados, renombrados ni preparados en el índice.

Se ejecutaron `git status --untracked-files=all`, `git branch --show-current`, `git diff --name-only`, `git diff --stat`, `git diff` y `git diff --check`. Los diffs de archivos versionados están vacíos. También se comprobó el Markdown nuevo sin incorporarlo al índice.

Validación documental de lectura: las 23 secciones principales coinciden con las solicitadas; el resumen tiene 17 líneas de contenido; los 74 enlaces relativos apuntan a destinos existentes; los ocho DOCX conservan exactamente el tamaño y SHA-256 de §17. No se detectaron ejemplos ajenos trasladados al informe ni valores de credenciales de los ejemplos examinados. La referencia a `routes/api.php` es una ausencia explícitamente documentada, no un enlace roto.

La comprobación de definiciones contó 26 tablas declaradas por las migraciones del proyecto y 40 capturas históricas versionadas. No se ejecutaron suites funcionales ni validadores que pudieran regenerar artefactos. Estas verificaciones no alteran la evidencia histórica ni el software.

Se deben distinguir archivos **sin seguimiento** de modificaciones a archivos ya versionados: git diff y git diff --stat no muestran por sí solos el contenido de los nuevos archivos. No se ejecutará git add para hacerlos aparecer en el diff.

No se ejecutaron commit, push, merge, rebase, cherry-pick, reset, clean, migraciones, seeders, instalaciones, actualizaciones, autofixes, arranques de servicios ni pruebas que generen estado. No se accedió a bases de datos ni se alteró su contenido. F36 no fue iniciada.
