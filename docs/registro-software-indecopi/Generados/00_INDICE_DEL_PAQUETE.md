# Índice del paquete documental

**Estado general: BORRADOR TÉCNICO — LISTO PARA REVISIÓN HUMANA.** Estos archivos no constituyen presentación, declaración jurada firmada ni aprobación de registro.

**Título provisional — pendiente de confirmación humana:** Plataforma SaaS Multiempresa para la Gestión del Reclutamiento, Evaluación y Selección de Personal.

**Versión del registro:** [PENDIENTE DE CONFIRMACIÓN HUMANA].

**Snapshot técnico auditado:** `b8892af39a6492d8dd44a36290604efc602380cd`.

## 1 Alcance y fuentes

Fuente principal: [reporte maestro](../../REPORTE_AUDITORIA_DOCUMENTAL.md). Se reutilizaron sus conclusiones. El código se consultó para extraer fragmentos y comprobar relaciones, rutas y diagramas. Las ocho [plantillas y guías](../Plantillas/) se utilizaron como requisitos de estructura. Sus ejemplos no se adoptaron como hechos del SaaS.

El núcleo es Laravel/React/TypeScript/Inertia con PostgreSQL y Redis. El ranking es determinista y ponderado; la decisión final es humana. RF-29 es experimental, opcional y operacional: no evalúa, clasifica ni selecciona personas. El sandbox es académico, sintético y no productivo. El alcance funcional concluye en selección/cierre.

G0 real NO APROBADA; G0-SBX APROBADA CON RESTRICCIONES; datos reales PROHIBIDOS; Scope C y F35 productiva BLOQUEADOS; F35-SBX CERRADA / CONGELADA / INTEGRADA; F36–F40 BLOQUEADAS y F36 NO INICIADA. La generación documental no cambia estos estados.

## 2 Archivos y estado

| Archivo | Estado | Páginas | Pendientes |
|---|---|---|---|
| [01_Ficha_Tecnica_SaaS_Reclutamiento.docx](01_Ficha_Tecnica_SaaS_Reclutamiento.docx) | BORRADOR TÉCNICO / LISTO PARA REVISIÓN | 2 | Título, versión, titular y fechas oficiales. |
| [02_Ejemplar_del_Software_SaaS_Reclutamiento.docx](02_Ejemplar_del_Software_SaaS_Reclutamiento.docx) | BORRADOR TÉCNICO / REQUIERE CAPTURA | 4 | Soporte final, capturas, requisitos operativos y datos legales. |
| [02A_Codigo_Fuente_Representativo.docx](02A_Codigo_Fuente_Representativo.docx) | BORRADOR TÉCNICO / LISTO PARA REVISIÓN | 14 | Validación de autoría, titularidad, licencias y forma del ejemplar. |
| [03A_Declaracion_Autoria_Coronacion_Meza_Fredy.docx](03A_Declaracion_Autoria_Coronacion_Meza_Fredy.docx) | REQUIERE DATOS HUMANOS / REQUIERE FIRMA | 3 | Identidad legal, DNI, domicilio, rol, periodo, aportes, titular, autorización y firma. |
| [03B_Declaracion_Autoria_Pena_Arroyo_Anthony.docx](03B_Declaracion_Autoria_Pena_Arroyo_Anthony.docx) | REQUIERE DATOS HUMANOS / REQUIERE FIRMA | 3 | Identidad legal, DNI, domicilio, rol, periodo, aportes, titular, autorización y firma. |
| [03C_Declaracion_Autoria_Vila_Meza_Luis_Antonio.docx](03C_Declaracion_Autoria_Vila_Meza_Luis_Antonio.docx) | REQUIERE DATOS HUMANOS / REQUIERE FIRMA | 3 | Identidad legal, DNI, domicilio, rol, periodo, aportes, titular, autorización y firma. |
| [04_Lista_de_Autores_y_Roles.docx](04_Lista_de_Autores_y_Roles.docx) | REQUIERE DATOS HUMANOS / LISTO PARA REVISIÓN | 2 | Identidad legal y asignación individual de roles, componentes, periodos y aportes. |
| [05_Representacion_Legal_Titular.docx](05_Representacion_Legal_Titular.docx) | BORRADOR CONDICIONAL / REQUIERE DATOS HUMANOS / REQUIERE FIRMA | 2 | Aplicabilidad, razón social, RUC, domicilio, representante, poder, derechos, sello y firma. |
| [06_Anexos_Tecnicos_SaaS_Reclutamiento.docx](06_Anexos_Tecnicos_SaaS_Reclutamiento.docx) | BORRADOR TÉCNICO / REQUIERE CAPTURA / LISTO PARA REVISIÓN | 10 | Seis capturas ficticias, aprobación humana de diagramas, métricas no acreditadas y datos legales. |
| [07_Descripcion_Tecnica_Resumen_Funcional.docx](07_Descripcion_Tecnica_Resumen_Funcional.docx) | BORRADOR TÉCNICO / LISTO PARA REVISIÓN | 2 | Título, versión, año, autores legales y titular. |
| [08_Plantilla_Registro_General_Completada.docx](08_Plantilla_Registro_General_Completada.docx) | REQUIERE DATOS HUMANOS / LISTO PARA REVISIÓN | 2 | Campos legales, fechas, soporte, capturas y validación administrativa vigente. |

| Archivo | Uso | Estado |
|---|---|---|
| [00_DATOS_PENDIENTES_PARA_FINALIZAR.md](00_DATOS_PENDIENTES_PARA_FINALIZAR.md) | Checklist de cierre de datos y evidencia. | REQUIERE DATOS HUMANOS / REQUIERE CAPTURA / REQUIERE FIRMA |
| 00_INDICE_DEL_PAQUETE.md | Inventario, trazabilidad, controles y lista de pendientes. | LISTO PARA REVISIÓN |

La paginación corresponde a Word nativo en A4. **02A tiene 14 páginas: una introductoria y trece con código y sus rótulos. 07 ocupa 2 páginas.** Otra versión de Word o fuentes sustituidas puede cambiar saltos; revisar antes de imprimir o presentar.

03A–03C son modelos individuales sin juramento efectuado ni autorización concedida. 05 se utilizará únicamente si la definición humana del titular corresponde a una persona jurídica. Ninguna institución del caso se identifica como titular por inferencia.

## 3 Diagramas editables y exportaciones

| Diagrama | Fuente editable | Exportaciones | Evidencia |
|---|---|---|---|
| Arquitectura AS-IS | [Mermaid](diagramas/arquitectura.mmd) | [SVG](diagramas/arquitectura.svg) · [PNG](diagramas/arquitectura.png) | Reporte §4; routes/web.php; bootstrap/app.php; docker-compose.yml; servicios Laravel y API ML opcional. |
| Flujo principal de reclutamiento | [Mermaid](diagramas/flujo-reclutamiento.mmd) | [SVG](diagramas/flujo-reclutamiento.svg) · [PNG](diagramas/flujo-reclutamiento.png) | Reporte §6; JobRequestWorkflow; VacancyService; ApplicationService; servicios Assessments y Selection. |
| Modelo lógico simplificado | [Mermaid](diagramas/modelo-datos.mmd) | [SVG](diagramas/modelo-datos.svg) · [PNG](diagramas/modelo-datos.png) | Reporte §7; app/Models/; database/migrations/. Vista simplificada, sin cardinalidades exhaustivas. |
| Aislamiento multiempresa y autorización | [Mermaid](diagramas/aislamiento-multiempresa.mmd) | [SVG](diagramas/aislamiento-multiempresa.svg) · [PNG](diagramas/aislamiento-multiempresa.png) | Reporte §§7–8; OrganizationScope; BelongsToOrganization; Policies; consultas y pruebas cross-tenant. |

Los PNG están incorporados al documento 06. Mermaid conserva nodos y relaciones editables; SVG conserva la exportación vectorial; PNG permite inserción directa. Un renderizador Mermaid puede distribuir los nodos de otra manera. No se instalaron herramientas ni dependencias en el SaaS para producirlos.

## 4 Procedencia del código representativo

Se incluyeron **573 líneas originales de 14 archivos**, contando líneas vacías de los rangos seleccionados. Se mantuvieron contenido e indentación; los ajustes de línea en Word son visuales. Los recortes no son archivos autónomos compilables. Se excluyeron configuración privada, dependencias, código generado, modelos ML y datos de postulantes.

| Archivo de origen | Rangos de líneas | Líneas | Propósito |
|---|---|---|---|
| [app/Models/Scopes/OrganizationScope.php](../../../app/Models/Scopes/OrganizationScope.php) | 1–25 | 25 | Filtro de organización |
| [app/Models/Concerns/BelongsToOrganization.php](../../../app/Models/Concerns/BelongsToOrganization.php) | 15–37 | 23 | Asociación y scope de organización |
| [app/Policies/VacancyPolicy.php](../../../app/Policies/VacancyPolicy.php) | 11–19; 54–57; 69–73 | 18 | Autorización por rol y organización |
| [app/Services/JobRequests/JobRequestWorkflow.php](../../../app/Services/JobRequests/JobRequestWorkflow.php) | 31–46; 125–148 | 40 | Registro y transición del requerimiento |
| [app/Services/Applications/ApplicationService.php](../../../app/Services/Applications/ApplicationService.php) | 25–80 | 56 | Postulación validada y transaccional |
| [app/Services/Ranking/RankingService.php](../../../app/Services/Ranking/RankingService.php) | 26–58; 117–133; 141–165 | 75 | Ranking ponderado y explicable |
| [app/Http/Requests/Selection/FinalDecisionRequest.php](../../../app/Http/Requests/Selection/FinalDecisionRequest.php) | 11–34 | 24 | Confirmación humana y validación |
| [app/Services/Selection/FinalDecisionService.php](../../../app/Services/Selection/FinalDecisionService.php) | 28–84 | 57 | Decisión humana persistida |
| [app/Services/Selection/SelectionRegistrationService.php](../../../app/Services/Selection/SelectionRegistrationService.php) | 27–68 | 42 | Registro de selección conforme a la decisión |
| [app/Services/Selection/VacancyClosureService.php](../../../app/Services/Selection/VacancyClosureService.php) | 33–94 | 62 | Cierre y estados finales |
| [app/Services/Audit/AuditLogger.php](../../../app/Services/Audit/AuditLogger.php) | 24–40; 62–75 | 31 | Auditoría y filtrado de claves |
| [resources/js/pages/selection/comparison.tsx](../../../resources/js/pages/selection/comparison.tsx) | 349–425 | 77 | Interfaz de la decisión humana |
| [tests/Feature/Tenancy/CrossTenantAccessTest.php](../../../tests/Feature/Tenancy/CrossTenantAccessTest.php) | 65–88 | 24 | Pruebas de aislamiento entre organizaciones |
| [tests/Feature/Selection/FinalDecisionTest.php](../../../tests/Feature/Selection/FinalDecisionTest.php) | 74–92 | 19 | Pruebas del carácter humano de la decisión |

### Huellas SHA-256 de fragmentos

Cada huella corresponde al fragmento con saltos LF y un LF final. Permite comparar el extracto con el snapshot, sin atribuir autoría legal.

| Origen y rango | SHA-256 normalizado |
|---|---|
| app/Models/Scopes/OrganizationScope.php:1–25 | `e657a2ae340c59cb69fb52b42e452e0ca708c6aa005ef2930fd4cbce9bd00903` |
| app/Models/Concerns/BelongsToOrganization.php:15–37 | `9e2c80cbebfa3ad5f29067ec69c73a0122a89f80b5bfd20a9a08185364fbf958` |
| app/Policies/VacancyPolicy.php:11–19 | `a55cd49cbe35fda1d91e18638ead98939161f9f1692f46aa1d3c7baca26cef93` |
| app/Policies/VacancyPolicy.php:54–57 | `a928e44d415d496648d18a7655adf302faeaf85da5fb4f0b1acdb8a7725ccb67` |
| app/Policies/VacancyPolicy.php:69–73 | `cac9678a5a3622d6456271fdd35bdfc4c95f40300fcfd5f758aaa0b5e63e66bb` |
| app/Services/JobRequests/JobRequestWorkflow.php:31–46 | `cbff4d9623cc4373d2878a145257b38339c002eb8bb830a188fbb83081fc3e84` |
| app/Services/JobRequests/JobRequestWorkflow.php:125–148 | `16ab95d653351cb923d376348e3f817b3608eabd84f1bde50ad3a995729b6807` |
| app/Services/Applications/ApplicationService.php:25–80 | `698cbb17a3db1f2c06952728922167f30a4968ddad7a1da431bf0b54fcc71c39` |
| app/Services/Ranking/RankingService.php:26–58 | `4a50b66f891e642fcfebe06e4382799a0a163664fa9388c516b8dfba8df3d8be` |
| app/Services/Ranking/RankingService.php:117–133 | `91f918ecc2018fa16e4a774149e0b756b80f3f555981caafedcd09e87c7b2f7c` |
| app/Services/Ranking/RankingService.php:141–165 | `cf47d65951147f9187d26622e6d8dd304fcf256cfcd54ae20e835a3d69be3760` |
| app/Http/Requests/Selection/FinalDecisionRequest.php:11–34 | `7945153914bee8eedab86cfe11a39304d5e2d69b6fbce86b054badea1647ec20` |
| app/Services/Selection/FinalDecisionService.php:28–84 | `2544a4055f093be17471c363c8311934886cdba21eb5c721bbbf7e362bacfff6` |
| app/Services/Selection/SelectionRegistrationService.php:27–68 | `dd5a601aeeb6ffec8117cbf0b42e0a335d59e975f2347da25a8cf3a54bfefdc5` |
| app/Services/Selection/VacancyClosureService.php:33–94 | `6cb1825ba4ab6c6b715b44b58c602609027fb3e95781ea0380c168034ecd3d21` |
| app/Services/Audit/AuditLogger.php:24–40 | `06e7adbda79a7b440f7cd6dae7a46a670d19851798a7772de4758c5dd5a7fe2c` |
| app/Services/Audit/AuditLogger.php:62–75 | `64b522c3c9a4456f2fe60f944c6df39c2e61d3dc2117e1917ad4d810fcbed3dc` |
| resources/js/pages/selection/comparison.tsx:349–425 | `8649f88925e324d10d63901476f96a168b608afb573b960883bec3fd834ec390` |
| tests/Feature/Tenancy/CrossTenantAccessTest.php:65–88 | `8436b1a3cf28be2e3bba2fe603b971ef73df2dcf017a24ee9f6e0a62d541b5d5` |
| tests/Feature/Selection/FinalDecisionTest.php:74–92 | `d08298ac9b6945df34cd16eb98797d9172f53cb0ceea5398708c800728fe7f2c` |

## 5 Correspondencia con las plantillas

| Fuente estructural | Salida que recoge su intención |
|---|---|
| Documento 1 — Ficha técnica | 01: identificación, tecnologías, función, arquitectura y fechas con límites. |
| Documento 2 — Ejemplar | 02 y 02A: estructura Laravel/React, manual, uso, interfaces y código. |
| Documento 3 — Declaración | 03A–03C: título AUTORÍA; identificación, aportes, derechos, autorización y firma pendientes. |
| Documento 4 — Autores y roles | 04: tres integrantes académicos; tabla de roles y aportes sin atribución automática. |
| Documento 5 — Representación legal | 05: borrador condicional, identificación y poderes pendientes. |
| Documento 6 — Anexos técnicos | 06: arquitectura, flujos, datos, multiempresa, seguridad, QA, capturas y fronteras ML/SBX. |
| Plantilla general de registro | 08 y 02A: Anexo 1 con referencia al ejemplar y Anexo 2 técnico. |
| Guía general de registro | Índice/checklist y notas: soporte, licencias, firmas y validación administrativa por confirmar. |

Las pautas de estas fuentes no se presentan como requisitos administrativos oficiales vigentes. No se afirman tasas, plazos, exoneraciones ni aceptación de soportes; esos extremos deben verificarse antes de presentar.

## 6 Controles de generación documental

- Once DOCX con XML y relaciones internas revisados; título provisional uniforme y versión pendiente en los once.
- Revisión visual de las **47 páginas** representadas por Word: A4, tablas legibles, títulos jerarquizados y código monoespaciado. Las imágenes de inspección permanecieron fuera del repositorio.
- No se detectaron nombres o ejemplos de proyectos ajenos ni patrones de credenciales en el control del contenido generado. Las variables de entorno aparecen sin valores.
- Capturas de la aplicación pendientes. No se levantó la aplicación, Docker ni servidores.
- **Resultados históricos documentados; no fueron ejecutados nuevamente durante la generación documental.** Fuente principal: docs/v1.1/phase-25-final-qa.md, reutilizada a través del reporte y citada en el Anexo F.
- No se ejecutaron instalaciones, migraciones, seeders, suites funcionales ni compilaciones. No se cambió configuración.
- Rama documental: `docs/registro-software-documentos`, creada desde `docs/registro-software-indecopi` conservando el snapshot base. No se ejecutaron git add, commit, push, merge o rebase.

### Integridad de las fuentes

Las siguientes huellas se comprobaron antes y después de la generación; el reporte y las ocho plantillas permanecen idénticos.

| Fuente preservada | SHA-256 | Comprobación |
|---|---|---|
| docs/REPORTE_AUDITORIA_DOCUMENTAL.md | `f4a7b884c16bbc004a212ab744b4d189ce1e0171a95ed55ff2ba1c962bd17e39` | Sin cambios |
| docs/registro-software-indecopi/Plantillas/Documento 1 - Ficha técnica de software.docx | `d41b0a7eb25d5b71f3c45acbbd4df038001ce313509a5c57f1ec6837795a6ed5` | Sin cambios |
| docs/registro-software-indecopi/Plantillas/Documento 2 - Ejemplar del software.docx | `f1c4242d7cc59ebb6643e8523c6b17e66b183d6307d41bb67905747663f1dc90` | Sin cambios |
| docs/registro-software-indecopi/Plantillas/Documento 3 - Declaración jurada de auditoría.docx | `6d805eb4b1fae0199fd75296d31923bd6020fd4c3d184e5b4aeae9fb2013dfe7` | Sin cambios |
| docs/registro-software-indecopi/Plantillas/Documento 4 - Lista de autores y roles.docx | `8ef7dccd05152a67b7dbba10a906e72d5238afea95cf42567ab55448e1285521` | Sin cambios |
| docs/registro-software-indecopi/Plantillas/Documento 5 - Representación legal de la empresa.docx | `f1df36af8bf877791585b2280888da67187573bcef19ea0d599f5dd3f6a85bdd` | Sin cambios |
| docs/registro-software-indecopi/Plantillas/Documento 6 - Anexos técnicos.docx | `e49268c50883d97854eaf2d5c8b8a750a4e77a74d62bb95441d84d6eb51fa97f` | Sin cambios |
| docs/registro-software-indecopi/Plantillas/Plantilla_Registro_General_Software.docx | `c6d4c6e1846805156e3f545cf19401cd054420871c43f00ac5aa2a3fc380d78f` | Sin cambios |
| docs/registro-software-indecopi/Plantillas/Registro_Software_INDECOPI.docx | `c39a7be467413e4f2158b92036ee2067ba96caed6c5a6ce0a7e5ea761f50adf2` | Sin cambios |

El reporte y las ocho plantillas ya existían sin seguimiento al inicio de esta generación. Los 25 archivos del paquete se encuentran exclusivamente en Generados/: 11 DOCX, 2 Markdown y 12 archivos de diagramas. Los auxiliares de construcción y las representaciones de revisión se mantuvieron en un temporal externo.

**Residuo de Word excluido del expediente:** `~$_Ficha_Tecnica_SaaS_Reclutamiento.docx`, 162 bytes. Es un archivo temporal de bloqueo creado durante la representación, no un documento del paquete. La revisión automática rechazó su eliminación con «blocked by policy», sin indicar otro motivo; el cierre normal de Word no lo retiró. Permanece sin seguimiento y no debe incorporarse a la entrega. Esta observación no implica alteración de la ficha DOCX.

## 7 Campos pendientes consolidados

La búsqueda de **PENDIENTE** en los once DOCX encontró **166 apariciones**, incluidas reiteraciones y capturas. Su presencia es intencional; no equivale a datos completados.

| Documento | Apariciones de PENDIENTE | Campos o evidencias que deben cerrarse |
|---|---|---|
| 01_Ficha_Tecnica_SaaS_Reclutamiento.docx | 9 | Título, versión, titular y fechas oficiales. |
| 02_Ejemplar_del_Software_SaaS_Reclutamiento.docx | 8 | Soporte final, capturas, requisitos operativos y datos legales. |
| 02A_Codigo_Fuente_Representativo.docx | 5 | Validación de autoría, titularidad, licencias y forma del ejemplar. |
| 03A_Declaracion_Autoria_Coronacion_Meza_Fredy.docx | 25 | Identidad legal, DNI, domicilio, rol, periodo, aportes, titular, autorización y firma. |
| 03B_Declaracion_Autoria_Pena_Arroyo_Anthony.docx | 25 | Identidad legal, DNI, domicilio, rol, periodo, aportes, titular, autorización y firma. |
| 03C_Declaracion_Autoria_Vila_Meza_Luis_Antonio.docx | 25 | Identidad legal, DNI, domicilio, rol, periodo, aportes, titular, autorización y firma. |
| 04_Lista_de_Autores_y_Roles.docx | 23 | Identidad legal y asignación individual de roles, componentes, periodos y aportes. |
| 05_Representacion_Legal_Titular.docx | 20 | Aplicabilidad, razón social, RUC, domicilio, representante, poder, derechos, sello y firma. |
| 06_Anexos_Tecnicos_SaaS_Reclutamiento.docx | 15 | Seis capturas ficticias, aprobación humana de diagramas, métricas no acreditadas y datos legales. |
| 07_Descripcion_Tecnica_Resumen_Funcional.docx | 3 | Título, versión, año, autores legales y titular. |
| 08_Plantilla_Registro_General_Completada.docx | 8 | Campos legales, fechas, soporte, capturas y validación administrativa vigente. |

### Identificación del software

- Título jurídico definitivo, versión del registro, año, fecha oficial de creación y primera versión funcional.
- Alcance del ejemplar, snapshot elegido y forma final del soporte.

### Autores y declaraciones

- Identidad legal de cada integrante, DNI, domicilio, rol oficial, componentes, periodo y aportes individuales.
- Relación legal de coautores y declaración personal sobre originalidad y derechos de terceros.
- Titular, RUC si aplica, autorizaciones o cesiones y contenido del juramento que revisará el declarante.
- Nombre y DNI del firmante, firma, lugar y fecha. Git continúa como evidencia técnica complementaria.

### Titular y representación condicional

- Persona natural o jurídica titular de los derechos patrimoniales.
- Razón social, RUC, domicilio legal, representante, DNI, cargo, vigencia de poder y facultades, si corresponde.
- Documentos sustentatorios de derechos y representación, responsabilidad, fecha, sello y firma.

### Evidencias y cierre

- Seis capturas legibles con datos ficticios y snapshot identificado: login, requerimiento, vacante, expediente, evaluación/entrevista y comparación/decisión humana.
- Revisión humana de diagramas y del ejemplar de código; sus fuentes técnicas ya se generaron.
- Métricas no acreditadas y nuevas ejecuciones QA, solo si se requieren en una fase autorizada.
- Requisitos mínimos del equipo, soporte, mantenimiento, retención y restauración cuando deban declararse.
- Revisión de licencias, atribuciones y tratamiento de asistencia IA.
- Validación administrativa vigente, forma final del ejemplar, revisión integral, firmas y fechas antes de presentar.

Checklist de trabajo: [00_DATOS_PENDIENTES_PARA_FINALIZAR.md](00_DATOS_PENDIENTES_PARA_FINALIZAR.md).

