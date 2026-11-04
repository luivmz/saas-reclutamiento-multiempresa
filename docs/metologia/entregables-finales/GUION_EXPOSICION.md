# Guion de exposición

Dos versiones: 24 × 25 s = 10 minutos; 24 × 37.5 s = 15 minutos. La versión de 15 minutos desarrolla la pregunta y su cautela; la de 10 resume el dato clave. Métricas históricas, sin reejecución en esta entrega.

## 1. SaaS Reclutamiento Multiempresa

Qué mostrar: La evidencia, tabla o gráfico de la diapositiva; consultar fuente si requiere detalle.

Qué decir: Calidad del software con evidencia, revisión humana y trazabilidad. El equipo y docente están documentados en F6; confirmar su vigencia y la sección. Se entrega un caso académico con evidencia, no certificación productiva.

Dato clave: Universidad Continental · Caso académico: Colegio Andino de Huancayo

Riesgo de pregunta: ¿Quiénes presentan y qué se entrega?

Respuesta sugerida: El equipo y docente están documentados en F6; confirmar su vigencia y la sección. Se entrega un caso académico con evidencia, no certificación productiva.

Tiempo: 25 s (10 min) / 37.5 s (15 min).

Fuente: AGENTS.md; CLAUDE.md.

## 2. Un caso académico, no un diagnóstico institucional

Qué mostrar: La evidencia, tabla o gráfico de la diapositiva; consultar fuente si requiere detalle.

Qué decir: El contexto organizacional requiere validación. No consta validación institucional. El AS-IS es preliminar y no se inventan herramientas, volúmenes ni tiempos.

Dato clave: El repositorio implementa un SaaS multiempresa de reclutamiento.

Riesgo de pregunta: ¿Se entrevistó al colegio?

Respuesta sugerida: No consta validación institucional. El AS-IS es preliminar y no se inventan herramientas, volúmenes ni tiempos.

Tiempo: 25 s (10 min) / 37.5 s (15 min).

Fuente: F29H, cap. 2.

## 3. Cinco problemas preliminares

Qué mostrar: La evidencia, tabla o gráfico de la diapositiva; consultar fuente si requiere detalle.

Qué decir: Centralización y seguimiento orientan el diseño. No hay medición institucional. P1–P5 son hipótesis de análisis documentadas, no pérdidas monetarias demostradas.

Dato clave: P1 Información distribuida · P2 Seguimiento manual

Riesgo de pregunta: ¿Cuánto cuesta hoy cada problema?

Respuesta sugerida: No hay medición institucional. P1–P5 son hipótesis de análisis documentadas, no pérdidas monetarias demostradas.

Tiempo: 25 s (10 min) / 37.5 s (15 min).

Fuente: F4 / F29H, cap. 2.

## 4. AS-IS: representar antes de intervenir

Qué mostrar: Síntesis editable del diagrama; abrir el modelo completo del anexo si preguntan.

Qué decir: El BPMN existe; su contenido debe validarse con responsables. Existe el modelo formal, pero el contenido es AS-IS preliminar. Las 14 actividades deben validarse con responsables.

Dato clave: 14 actividades AS-01–AS-14.

Riesgo de pregunta: ¿El BPMN describe operaciones reales confirmadas?

Respuesta sugerida: Existe el modelo formal, pero el contenido es AS-IS preliminar. Las 14 actividades deben validarse con responsables.

Tiempo: 25 s (10 min) / 37.5 s (15 min).

Fuente: docs/academico/practica-03/.

## 5. TO-BE: apoyar una decisión humana

Qué mostrar: Síntesis editable del diagrama; abrir el modelo completo del anexo si preguntan.

Qué decir: La plataforma ordena el proceso; la Dirección decide. No. El ranking apoya y la decisión final exige confirmación humana y justificación del Aprobador / Dirección.

Dato clave: Requerimiento → vacante → postulación → evaluación → ranking.

Riesgo de pregunta: ¿El sistema selecciona al candidato?

Respuesta sugerida: No. El ranking apoya y la decisión final exige confirmación humana y justificación del Aprobador / Dirección.

Tiempo: 25 s (10 min) / 37.5 s (15 min).

Fuente: F5 y F2-F9.

## 6. Objetivo y delimitación

Qué mostrar: La evidencia, tabla o gráfico de la diapositiva; consultar fuente si requiere detalle.

Qué decir: Verificar un producto y documentar su evolución. No. La línea base termina en selección y cierre del proceso; contratación, planillas y banco de talentos están fuera del alcance implementado.

Dato clave: Objetivo: trazabilidad requisito → función → prueba → evidencia.

Riesgo de pregunta: ¿Incluye contratación y nómina?

Respuesta sugerida: No. La línea base termina en selección y cierre del proceso; contratación, planillas y banco de talentos están fuera del alcance implementado.

Tiempo: 25 s (10 min) / 37.5 s (15 min).

Fuente: CLAUDE.md; F9.

## 7. Cinco roles, una decisión final humana

Qué mostrar: La evidencia, tabla o gráfico de la diapositiva; consultar fuente si requiere detalle.

Qué decir: Los permisos forman parte del contrato multiempresa. Con contexto organization_id, scopes y Policies en servidor, además de pruebas cross-tenant. Los postulantes tienen una cuenta global.

Dato clave: Solicitante · RR. HH. · Aprobador / Dirección

Riesgo de pregunta: ¿Cómo se evita acceso entre empresas?

Respuesta sugerida: Con contexto organization_id, scopes y Policies en servidor, además de pruebas cross-tenant. Los postulantes tienen una cuenta global.

Tiempo: 25 s (10 min) / 37.5 s (15 min).

Fuente: app/Enums/UserRole.php; app/Policies/.

## 8. Requisitos y casos de uso

Qué mostrar: La evidencia, tabla o gráfico de la diapositiva; consultar fuente si requiere detalle.

Qué decir: No se mezclan catálogos académicos y técnicos. La vista académica agrupa funciones; no hay correspondencia uno a uno. RF-27 es transversal y CU-21 está diferido.

Dato clave: 27 RF de la línea base, sin renumerarlos.

Riesgo de pregunta: ¿Por qué hay 20 CU y 27 RF?

Respuesta sugerida: La vista académica agrupa funciones; no hay correspondencia uno a uno. RF-27 es transversal y CU-21 está diferido.

Tiempo: 25 s (10 min) / 37.5 s (15 min).

Fuente: F6–F8; MATRIZ_REQUERIMIENTOS_SISTEMA.xlsx.

## 9. Arquitectura conceptual

Qué mostrar: Síntesis editable del diagrama; abrir el modelo completo del anexo si preguntan.

Qué decir: Laravel es el sistema de registro. El sistema de registro es un monolito modular Laravel con Inertia. El servicio ML es opcional y experimental, separado del núcleo.

Dato clave: React / Inertia → Laravel → PostgreSQL

Riesgo de pregunta: ¿Es microservicios?

Respuesta sugerida: El sistema de registro es un monolito modular Laravel con Inertia. El servicio ML es opcional y experimental, separado del núcleo.

Tiempo: 25 s (10 min) / 37.5 s (15 min).

Fuente: ARQ-01; docker-compose.yml.

## 10. Stack real y orquestación

Qué mostrar: La diapositiva y su fuente indicada.

Qué decir: El frontend se compila dentro del runtime del proyecto. Laravel 13 · React 19 · TypeScript · Inertia 3 PHP 8.4.25 · PostgreSQL 17.11 · Redis 7.4.11 Compose: app, queue, postgres, redis. CI configurada; CD no demostrado.

Dato clave: Laravel 13 · React 19 · TypeScript · Inertia 3

Riesgo de pregunta: ¿La CI demuestra despliegue?

Respuesta sugerida: No: workflow configurado no es ejecución actual ni CD. chore/** no activa su push; Docker local no prueba operación productiva.

Tiempo: 25 s (10 min) / 37.5 s (15 min).

Artículo o marco de respaldo: composer.lock; package-lock.json; Dockerfile; Compose; .github/workflows/tests.yml.

## 11. Desarrollo colaborativo humano IA

Qué mostrar: La evidencia, tabla o gráfico de la diapositiva; consultar fuente si requiere detalle.

Qué decir: La IA asiste; las personas delimitan y revisan. Es una propuesta descriptiva apoyada en literatura; se reconoce colaboración humano IA y verificación, sin afirmar eficacia causal local.

Dato clave: Propuesta descriptiva: guiado por especificaciones y verificación.

Riesgo de pregunta: ¿Es una metodología científica ya validada?

Respuesta sugerida: Es una propuesta descriptiva apoyada en literatura; se reconoce colaboración humano IA y verificación, sin afirmar eficacia causal local.

Tiempo: 25 s (10 min) / 37.5 s (15 min).

Fuente: Hou et al., 2024; Barke et al., 2023; Ferrari & Spoletini, 2025.

## 12. AI-DLC como marco de contraste

Qué mostrar: La diapositiva y su fuente indicada.

Qué decir: Correspondencias; adopción formal no demostrada. Inception: requisitos. Construction: código y validación. Operations: solo soporte local; sin operación IA productiva. Intent / Unit / Bolt y rituales formales: sin registro histórico.

Dato clave: Inception: requisitos. Construction: código y validación.

Riesgo de pregunta: ¿Aplicaron AI-DLC formalmente?

Respuesta sugerida: No está demostrado. Se usa como marco técnico de contraste; no inventamos Intents, Units o Bolts históricos.

Tiempo: 25 s (10 min) / 37.5 s (15 min).

Artículo o marco de respaldo: Raja SP, AWS, 2025 (fuente técnica); contraste con AGENTS.md y PROGRESS.md.

## 13. Variables propuestas

Qué mostrar: La evidencia, tabla o gráfico de la diapositiva; consultar fuente si requiere detalle.

Qué decir: Una comparación técnica no prueba causalidad de IA. No con los datos disponibles: faltan horas, tareas comparables y control sin IA. La VD propuesta medible aquí es calidad del producto.

Dato clave: VI: protocolo humano IA guiado por especificaciones.

Riesgo de pregunta: ¿Se puede demostrar que IA mejoró productividad?

Respuesta sugerida: No con los datos disponibles: faltan horas, tareas comparables y control sin IA. La VD propuesta medible aquí es calidad del producto.

Tiempo: 25 s (10 min) / 37.5 s (15 min).

Fuente: OPERACIONALIZACION_VARIABLES.xlsx.

## 14. Operacionalización

Qué mostrar: La evidencia, tabla o gráfico de la diapositiva; consultar fuente si requiere detalle.

Qué decir: Cada indicador necesita instrumento y denominador. Cada indicador necesita fuente, fecha, alcance y denominador. Una clasificación distinta de tests altera la cobertura global sin nuevas pruebas.

Dato clave: Issues y vulnerabilidades: Sonar API + estado por regla.

Riesgo de pregunta: ¿Por qué no basta un porcentaje?

Respuesta sugerida: Cada indicador necesita fuente, fecha, alcance y denominador. Una clasificación distinta de tests altera la cobertura global sin nuevas pruebas.

Tiempo: 25 s (10 min) / 37.5 s (15 min).

Fuente: Matriz de variables; informes Sonar V1/V2.

## 15. Estrategia de pruebas

Qué mostrar: La evidencia, tabla o gráfico de la diapositiva; consultar fuente si requiere detalle.

Qué decir: Las herramientas verifican aspectos complementarios. No por sí solo. Hay evidencia RED/GREEN en fases concretas; no se atribuye retrospectivamente TDD a toda edición del repositorio.

Dato clave: PHPUnit: reglas, integración y aislamiento multiempresa.

Riesgo de pregunta: ¿Tener tests demuestra TDD?

Respuesta sugerida: No por sí solo. Hay evidencia RED/GREEN en fases concretas; no se atribuye retrospectivamente TDD a toda edición del repositorio.

Tiempo: 25 s (10 min) / 37.5 s (15 min).

Fuente: docs/tdd-evidence.md; F29D–F29F.

## 16. Matriz de doble entrada

Qué mostrar: Matriz visual resumida; abrir el Excel solo si se solicita detalle.

Qué decir: La literatura respalda controles; el SaaS aporta evidencia. 20 artículos; 13 con régimen peer review del venue confirmado. 7 cruces principales + catálogo y 27 criterios del registro. X = relación sustentada; vacíos = no demostrada. Sin causalidad atribuida.

Dato clave: 20 artículos; 13 con régimen peer review del venue confirmado.

Riesgo de pregunta: ¿Qué significa una X?

Respuesta sugerida: Respaldo temático verificable o asociación directa. No mide causalidad. El catálogo conserva DOI y límites; vacío indica relación no establecida.

Tiempo: 25 s (10 min) / 37.5 s (15 min).

Artículo o marco de respaldo: MATRIZ_DOBLE_ENTRADA_METODOLOGIA_IA.xlsx; ART-03, ART-06, ART-10, ART-17.

## 17. SonarQube V1: la línea base

Qué mostrar: La evidencia, tabla o gráfico de la diapositiva; consultar fuente si requiere detalle.

Qué decir: Cinco hallazgos antes de las correcciones. No. La V1 conservó cinco hallazgos y el primer análisis no evaluó condiciones de nuevo código.

Dato clave: 2 Vulnerabilities · 3 Code Smells · 0 Bugs

Riesgo de pregunta: ¿Gate OK significa ausencia de fallos?

Respuesta sugerida: No. La V1 conservó cinco hallazgos y el primer análisis no evaluó condiciones de nuevo código.

Tiempo: 25 s (10 min) / 37.5 s (15 min).

Fuente: docs/sonarqube/evidencias/v1/REPORTE_EVIDENCIAS_V1_SONARQUBE.md.

## 18. Cinco correcciones verificadas históricamente

Qué mostrar: La evidencia, tabla o gráfico de la diapositiva; consultar fuente si requiere detalle.

Qué decir: La resolución se comprobó por regla, no solo por total. El informe V2 registra el estado CLOSED/FIXED de cada regla original, sin NOSONAR ni rebajar el umbral.

Dato clave: php:S5693 · typescript:S2245

Riesgo de pregunta: ¿Se ocultaron los hallazgos?

Respuesta sugerida: El informe V2 registra el estado CLOSED/FIXED de cada regla original, sin NOSONAR ni rebajar el umbral.

Tiempo: 25 s (10 min) / 37.5 s (15 min).

Fuente: docs/sonarqube/evidencias/v2/REPORTE_RESULTADOS_V2_PRELIMINAR.md.

## 19. V1 → V2: hallazgos

Qué mostrar: La evidencia, tabla o gráfico de la diapositiva; consultar fuente si requiere detalle.

Qué decir: Los cinco hallazgos abiertos pasan a cero. No. Es el resultado de analizadores y reglas en un alcance concreto; no sustituye pruebas funcionales ni revisión de seguridad.

Dato clave: Issues: 5 → 0

Riesgo de pregunta: ¿Cero Issues implica cero riesgos?

Respuesta sugerida: No. Es el resultado de analizadores y reglas en un alcance concreto; no sustituye pruebas funcionales ni revisión de seguridad.

Tiempo: 25 s (10 min) / 37.5 s (15 min).

Fuente: docs/sonarqube/evidencias/v2/REPORTE_RESULTADOS_V2_PRELIMINAR.md.

## 20. Coverage: leer el denominador

Qué mostrar: La evidencia, tabla o gráfico de la diapositiva; consultar fuente si requiere detalle.

Qué decir: 69.5 % global no equivale a nueva cobertura frontend. Se clasificaron ocho tests TypeScript como TESTS. Es una corrección del denominador, no cobertura frontend nueva; app/ permanece en 89.6 %.

Dato clave: V1 66.5 % → V2 inicial 65.6 % → V2 reclasificada 69.5 %.

Riesgo de pregunta: ¿Por qué subió de 65.6 a 69.5 %?

Respuesta sugerida: Se clasificaron ocho tests TypeScript como TESTS. Es una corrección del denominador, no cobertura frontend nueva; app/ permanece en 89.6 %.

Tiempo: 25 s (10 min) / 37.5 s (15 min).

Fuente: docs/sonarqube/evidencias/v2/REPORTE_RESULTADOS_V2_PRELIMINAR.md.

## 21. Quality Gate: OK con una salvedad esencial

Qué mostrar: La evidencia, tabla o gráfico de la diapositiva; consultar fuente si requiere detalle.

Qué decir: New Code Coverage real: 50 %, no 80 %. No: fue 50 %, una de dos líneas elegibles. Small Changes heredado ignoró la condición por menos de 20 líneas; por eso el gate figura OK.

Dato clave: 11 líneas nuevas productivas; 2 elegibles, 1 cubierta.

Riesgo de pregunta: ¿Se llegó al 80 % de cobertura nueva?

Respuesta sugerida: No: fue 50 %, una de dos líneas elegibles. Small Changes heredado ignoró la condición por menos de 20 líneas; por eso el gate figura OK.

Tiempo: 25 s (10 min) / 37.5 s (15 min).

Fuente: docs/sonarqube/evidencias/v2/REPORTE_RESULTADOS_V2_PRELIMINAR.md.

## 22. Resultados y deudas pendientes

Qué mostrar: La evidencia, tabla o gráfico de la diapositiva; consultar fuente si requiere detalle.

Qué decir: Las pruebas pasan; la deuda estática permanece visible. Las herramientas miden aspectos diferentes. PHPStan, Pint, formato y Oxlint mantienen deuda histórica que no se mezcla con los cinco Issues Sonar.

Dato clave: PHPUnit: 414 passed, 8 skipped, 0 failed; 1506 assertions.

Riesgo de pregunta: ¿Por qué hay deuda si las pruebas pasan?

Respuesta sugerida: Las herramientas miden aspectos diferentes. PHPStan, Pint, formato y Oxlint mantienen deuda histórica que no se mezcla con los cinco Issues Sonar.

Tiempo: 25 s (10 min) / 37.5 s (15 min).

Fuente: docs/sonarqube/evidencias/v2/REPORTE_RESULTADOS_V2_PRELIMINAR.md.

## 23. Discusión y conclusiones

Qué mostrar: La diapositiva y su fuente indicada.

Qué decir: Mejora técnica demostrada, eficacia institucional pendiente. Fortaleza: cinco hallazgos corregidos y trazabilidad preservada. Límite: métricas históricas y cobertura no homogénea. Recomendación: validar AS-IS, RNF y registrar esfuerzo/prompts prospectivamente.

Dato clave: Fortaleza: cinco hallazgos corregidos y trazabilidad preservada.

Riesgo de pregunta: ¿Qué falta para concluir eficacia?

Respuesta sugerida: Validación institucional y protocolo prospectivo con tiempos/control. Una comparación Sonar del producto no mide efecto causal de IA.

Tiempo: 25 s (10 min) / 37.5 s (15 min).

Artículo o marco de respaldo: Informes Sonar; BRECHAS_ENTREGA_FINAL.md.

## 24. Referencias clave

Qué mostrar: La diapositiva y su fuente indicada.

Qué decir: Fuentes científicas y marco técnico, con alcances distintos. Perry et al. (2023): seguridad y sobreconfianza. Barke et al. (2023): interacción humano IA. Ferrari y Spoletini (2025): especificación; Raja SP (2025): AI-DLC técnico.

Dato clave: Perry et al. (2023): seguridad y sobreconfianza.

Riesgo de pregunta: ¿AI-DLC es un paper peer-reviewed?

Respuesta sugerida: Es un white paper técnico de AWS, separado de veinte publicaciones; no se cuenta entre las trece con revisión a nivel de venue.

Tiempo: 25 s (10 min) / 37.5 s (15 min).

Artículo o marco de respaldo: Referencias APA 7 completas: REFERENCIAS_APA7.md; catálogo de 20 artículos.

## Apoyo bibliográfico y tiempos

Las 24 diapositivas conservan versiones de 10 y 15 minutos. La literatura se cita en la 11 (Hou/Barke/Ferrari), 12 (Raja SP técnico), 13–14 (variables propuestas y operacionalización), 16 (Perry/Barke/Wang/Ferrari) y 24 (referencias). Las afirmaciones empíricas del SaaS proceden de informes históricos, no de los artículos. En la versión larga se explica el límite de causalidad y Small Changes; no se ocultan en la corta.
