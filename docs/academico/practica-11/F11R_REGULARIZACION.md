# Regularización F11-R — Formato 11 oficial

**Estado:** implementada el 29/09/2026 en la rama `feature/f11-r-official-format` (creada desde `develop` `f7017c1`). Pendiente de auditoría independiente. No se hizo *push* ni *merge*.

## Qué es

El Formato 11 oficial «Arquitectura del sistema» llegó después de la Fase 28. Hasta entonces no estaba disponible, así que el F11 se hizo como **adaptación académica** de la Guía 11 sobre la base visual del F9. La F11-R **regulariza** ese entregable:

- **Qué hace:** vuelve a presentar la misma arquitectura conceptual sobre la plantilla oficial, con su estructura de 8 secciones y sus identificadores CMP-xx.
- **Qué no cambia:** la arquitectura. Los componentes, las relaciones, las capas, las decisiones, los estados y el diagrama ARQ-01 son los mismos.
- **Versión anterior:** el F11 adaptado se conserva como **versión histórica**. Fue una adaptación académica válida en las condiciones de ese momento, no un error.

| Versión | Archivos | Estado |
|---|---|---|
| **Definitiva** (F11-R) | [`F11_Arquitectura_del_Sistema_Colegio_Andino.docx`](F11_Arquitectura_del_Sistema_Colegio_Andino.docx) · [PDF](F11_Arquitectura_del_Sistema_Colegio_Andino.pdf) · [espejo `.md`](F11_Arquitectura_del_Sistema_Colegio_Andino.md) | Sobre la plantilla oficial. Pendiente de auditoría |
| **Histórica** (F28, F29) | [`F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.docx`](F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.docx) · [PDF](F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.pdf) · [espejo `.md`](F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.md) | Adaptación académica anterior. Se conserva **sin cambios** |

## Estructura real de la plantilla oficial

Cabecera con el logotipo de la Universidad Continental y «Asignatura: Pruebas y Calidad de Software». Título «Formato 11: Arquitectura del sistema». Ocho secciones numeradas:

1. **Datos generales del proyecto:** tabla con los campos Nombre del proyecto, Integrantes del equipo, Módulo / Sistema, Docente y Fecha.
2. **Descripción general del sistema:** instrucción «Describir brevemente:» y cuatro viñetas, cada una con una caja: Propósito del sistema, Alcance general, Usuarios principales y Relación con requerimientos y casos de uso.
3. **Estilo arquitectónico propuesto:** instrucción «Seleccionar y justificar el estilo arquitectónico» y seis viñetas con caja: Cliente-Servidor, Capas (N-tier), Microservicios, Monolítico, Otros y Justificación.
4. **Identificación de componentes:** tabla con las columnas ID · Componente · Descripción · Funcionalidades asociadas, y las filas de ejemplo CMP-01, CMP-02 y «…».
5. **Relación entre componentes:** tabla con las columnas Componente origen · Componente destino · Tipo de interacción · Descripción.
6. **Diagrama de Arquitectura conceptual:** instrucción «Insertar aquí el diagrama del sistema.» y una caja.
7. **Decisiones de diseño:** instrucción «Registrar decisiones clave tomadas:» y tres viñetas de líneas en blanco.
8. **Restricciones y consideraciones:** cuatro viñetas con caja: Tecnológicas, De rendimiento, De seguridad y De escalabilidad.

Tratamiento de la plantilla en el entregable:

- **Se conservan** la cabecera, los estilos, la numeración, los títulos, las viñetas, las cajas y las tablas, con sus columnas.
- **Se retiran** las instrucciones y las líneas en blanco.
- **Único añadido** fuera de la estructura: el recuadro «Estado de la información» tras los datos generales, igual que en los Formatos 02 a 08.

## Matriz de correspondencia

| Sección oficial | Fuente en el F11 adaptado | Evidencia | Acción de regularización |
|---|---|---|---|
| 1. Datos generales del proyecto | Sección 1 «Datos generales» | m_common.py (datos del proyecto) | Tabla oficial rellenada; fecha de la regularización |
| 2. Descripción general del sistema (propósito, alcance general, usuarios principales, relación con requerimientos y casos de uso) | Secciones 2 «Contexto y alcance» y 3 «Casos de uso» | F9 v1.1; F6; F8; m_arch.CONTEXTO y CU_GRUPOS | Redistribuido en las cuatro viñetas oficiales |
| 3. Estilo arquitectónico propuesto (cliente-servidor, capas, microservicios, monolítico, otros, justificación) | Secciones 8 «Arquitectura conceptual», «Arquitectura técnica» y 9 «Decisiones» (DA-01) | cap. 7 §7.2–7.3; F9 §10.1; m_arch.TECNICA y CAPAS | Una respuesta por opción del formato: monolito modular adoptado; cliente-servidor y capas como características complementarias; microservicios no adoptado |
| 4. Identificación de componentes | Secciones 4 «Componentes» y 5 «Responsabilidades»; COMPONENTS.md | m_arch.COMPONENTES | CMP-01 a CMP-17 con equivalencia Cxx; columnas oficiales |
| 5. Relación entre componentes | Secciones 6 «Relaciones» y 7 «Flujo»; RELATIONSHIPS.md | m_arch.RELACIONES | R-01 a R-20 en las columnas oficiales, sin cambios de semántica |
| 6. Diagrama de Arquitectura conceptual | Sección 8, figura ARQ-01 | powerdesigner/exports/ARQ-01_Arquitectura_Conceptual.png | Misma exportación F29/F29B, en página horizontal, con ampliaciones |
| 7. Decisiones de diseño | Sección 9 «Decisiones arquitectónicas» (DA-01 a DA-10) | m_arch.DECISIONES; cap. 7 | Viñetas con estado ADOPTADA, IMPLEMENTADA, PROPUESTA o EXPERIMENTAL; DA-11 (Docker) añadida |
| 8. Restricciones y consideraciones (tecnológicas, de rendimiento, de seguridad, de escalabilidad) | Secciones 9 «RNF → decisiones», 11 «Limitaciones» y «Arquitectura técnica» | F7; cap. 5 §5.7; cap. 7 | Una caja por categoría; RNF-06 y RNF-07 no verificados; sin SLA ni métricas inventadas |

Las secciones del F11 adaptado sin equivalente en la plantilla oficial **no se pierden**: siguen en el F11 adaptado histórico y en sus archivos de trabajo, que no cambian.

| Sección del F11 adaptado | Dónde sigue |
|---|---|
| Correspondencia con la Guía 11 | F11 adaptado; [`F28_VALIDATION.md`](F28_VALIDATION.md) |
| Flujo de información y flujo de RF-29 | F11 adaptado; [`RELATIONSHIPS.md`](RELATIONSHIPS.md) |
| Arquitectura técnica de referencia | F11 adaptado. En el oficial, resumida en las secciones 3 y 8 |
| RNF académicos → decisiones y componentes | F11 adaptado. En el oficial, dentro de las secciones 7 y 8 |
| Validación (22 criterios) | [`VALIDATION.md`](VALIDATION.md) y `validate.py` (`f11_checks`) |
| Trazabilidad por componente | [`../trazabilidad/F11-architecture-traceability.md`](../trazabilidad/F11-architecture-traceability.md) |

## Equivalencia de identificadores CMP ↔ C

Es uno a uno: no se combinan, dividen ni añaden componentes.

- **CMP-xx:** identificador del Formato 11 oficial.
- **Cxx:** identificador histórico. Lo conservan el F11 adaptado, `COMPONENTS.md`, `RELATIONSHIPS.md` y el diagrama ARQ-01.

| Formato 11 oficial | Histórico | Componente (nombre canónico) | Capa conceptual | Estado |
|---|---|---|---|---|
| CMP-01 | C01 | Interfaz web | Presentación | SOFTWARE IMPLEMENTADO |
| CMP-02 | C02 | Autenticación y cuentas | Acceso y seguridad | SOFTWARE IMPLEMENTADO |
| CMP-03 | C03 | Autorización y contexto multiempresa | Acceso y seguridad | SOFTWARE IMPLEMENTADO (transversal) |
| CMP-04 | C04 | Requerimientos de personal | Negocio | SOFTWARE IMPLEMENTADO |
| CMP-05 | C05 | Vacantes y convocatorias | Negocio | SOFTWARE IMPLEMENTADO |
| CMP-06 | C06 | Postulantes y CV | Negocio | SOFTWARE IMPLEMENTADO |
| CMP-07 | C07 | Postulaciones y etapas | Negocio | SOFTWARE IMPLEMENTADO |
| CMP-08 | C08 | Evaluaciones y entrevistas | Negocio | SOFTWARE IMPLEMENTADO |
| CMP-09 | C09 | Ranking y comparación | Negocio | SOFTWARE IMPLEMENTADO |
| CMP-10 | C10 | Decisión final humana | Negocio | SOFTWARE IMPLEMENTADO |
| CMP-11 | C11 | Selección y cierre | Negocio | SOFTWARE IMPLEMENTADO |
| CMP-12 | C12 | Notificaciones | Servicios transversales | SOFTWARE IMPLEMENTADO (transversal) |
| CMP-13 | C13 | Auditoría | Servicios transversales | SOFTWARE IMPLEMENTADO (transversal) |
| CMP-14 | C14 | Persistencia de datos (PostgreSQL) | Persistencia e infraestructura | SOFTWARE IMPLEMENTADO |
| CMP-15 | C15 | Almacenamiento privado de CV | Persistencia e infraestructura | SOFTWARE IMPLEMENTADO |
| CMP-16 | C16 | Sesiones, caché y cola (Redis) | Persistencia e infraestructura | SOFTWARE IMPLEMENTADO |
| CMP-17 | C17 | Riesgo operacional del proceso (RF-29) | Experimental (opcional) | EXPERIMENTAL / PROPUESTO |

## Relaciones R-01 a R-20

Se conservan tal como están en [`RELATIONSHIPS.md`](RELATIONSHIPS.md): mismo identificador con guion, mismo origen, destino y tipo, sin desdoblar las relaciones múltiples y sin R-21.

| ID | Origen | Destino | Tipo |
|---|---|---|---|
| R-01 | CMP-01 (C01) | CMP-02 (C02) | Solicitud |
| R-02 | CMP-02 (C02) | CMP-03 (C03) | Contexto de seguridad |
| R-03 | CMP-03 (C03) | CMP-04 a CMP-11, CMP-13 (C04 a C11, C13) | Autorización y filtro |
| R-04 | CMP-01 (C01) | CMP-04 a CMP-11, CMP-13 (C04 a C11, C13) | Uso |
| R-05 | CMP-04 (C04) | CMP-05 (C05) | Flujo de información |
| R-06 | CMP-05 (C05) | CMP-07 (C07) | Flujo de información |
| R-07 | CMP-06 (C06) | CMP-07 (C07) | Flujo de información |
| R-08 | CMP-08 (C08) | CMP-07 (C07) | Uso |
| R-09 | CMP-08 (C08) | CMP-09 (C09) | Flujo de información |
| R-10 | CMP-09 (C09) | CMP-10 (C10) | Apoyo a la decisión |
| R-11 | CMP-10 (C10) | CMP-11 (C11) | Precondición |
| R-12 | CMP-11 (C11) | CMP-07 (C07) | Uso |
| R-13 | CMP-04 a CMP-11 (C04 a C11) | CMP-13 (C13) | Registro |
| R-14 | CMP-04, CMP-07, CMP-08, CMP-11 (C04, C07, C08, C11) | CMP-12 (C12) | Evento |
| R-15 | CMP-12 (C12) | CMP-16 (C16) | Encolado |
| R-16 | CMP-04 a CMP-13 (C04 a C13) | CMP-14 (C14) | Persistencia |
| R-17 | CMP-06, CMP-07 (C06, C07) | CMP-15 (C15) | Almacenamiento |
| R-18 | CMP-02 (C02) | CMP-16 (C16) | Sesión y caché |
| R-19 | CMP-05 (C05) | CMP-17 (C17) | Consulta opcional |
| R-20 | CMP-17 (C17) | CMP-01 (C01) | Información descriptiva |

## ARQ-01

Se reutiliza la exportación formal auditada en la F29 y el hotfix F29B ([`ARQ-01_Arquitectura_Conceptual.png`](../powerdesigner/exports/ARQ-01_Arquitectura_Conceptual.png)), **sin rediseñarla ni retocarla**. Conserva los identificadores C01 a C17; el documento oficial aporta la equivalencia con CMP-xx. En el DOCX:

- va dentro de la caja de la sección 6, en una página horizontal;
- le siguen dos ampliaciones, que son recortes sin retoque.

No se modificaron los modelos de PowerDesigner de la F29 ni los de la F23.

## Diferencias entre el F11 adaptado y el Formato 11 oficial

| Aspecto | F11 adaptado (F28) | F11 oficial (F11-R) |
|---|---|---|
| Base del documento | Paquete del F9 publicado (portada, cabecera «F11 ADAPTADO», pie de página y borde) | Plantilla oficial del Formato 11 (cabecera con logotipo y asignatura) |
| Estructura | 14 secciones propias, derivadas de la Guía 11 | 8 secciones oficiales, con sus viñetas, cajas y tablas |
| Identificadores | C01 a C17 | CMP-01 a CMP-17, con el histórico Cxx al lado |
| Estilo arquitectónico | Descrito en la arquitectura técnica y en DA-01 | Respondido opción por opción del formato: monolito modular adoptado; cliente-servidor y capas como características complementarias; microservicios no adoptado |
| Decisiones | Tabla DA-01 a DA-10 | Viñetas con estado (ADOPTADA, IMPLEMENTADA, PROPUESTA, EXPERIMENTAL). Se añade DA-11 (Docker Compose), una decisión ya aplicada |
| Restricciones | Limitaciones y RNF → decisiones | Cuatro categorías oficiales, sin SLA ni métricas inventadas |
| Arquitectura | 17 componentes, R-01 a R-20, 6 capas y ARQ-01 | **Sin cambios** |

## Fuentes

SHA-256 del contenido versionado. En los archivos de texto se calcula con finales de línea LF.

| Fuente | Ruta | SHA-256 | Qué aporta |
|---|---|---|---|
| Formato_11_Arquitectura_del_sistema.docx | [`docs/academico/00-fuentes-oficiales/formatos-originales/Formato_11_Arquitectura_del_sistema.docx`](../00-fuentes-oficiales/formatos-originales/Formato_11_Arquitectura_del_sistema.docx) | `2e671f1384de14f13667156d5925f63a1b20d8231f3ea053570ad1f21b63df78` | Plantilla oficial del Formato 11 (fuente formal principal, solo lectura) |
| GUIA_PRACTICA_11.docx | [`docs/academico/00-fuentes-oficiales/guias/GUIA_PRACTICA_11.docx`](../00-fuentes-oficiales/guias/GUIA_PRACTICA_11.docx) | `c70f913787f81e250eee843eff197c8efb3ecda32896deb40afaabbfdb9689e7` | Guía de Práctica 11 (fuente complementaria) |
| COMPONENTS.md | [`docs/academico/practica-11/COMPONENTS.md`](COMPONENTS.md) | `705ffdbee4afe53781b056fe4b2aa2a570b964df29f91bfb7810489d244887be` | Componentes C01 a C17 (F28) |
| RELATIONSHIPS.md | [`docs/academico/practica-11/RELATIONSHIPS.md`](RELATIONSHIPS.md) | `e21ae3c125a198523e434b0ab00f68c418292f13427f96b5af8c8128d47df141` | Relaciones R-01 a R-20 (F28) |
| ARQ-01_Arquitectura_Conceptual.png | [`docs/academico/powerdesigner/exports/ARQ-01_Arquitectura_Conceptual.png`](../powerdesigner/exports/ARQ-01_Arquitectura_Conceptual.png) | `4084af202f7af08adca7545c4ea3fe3906c8d0d575da3e946385f168047e3ee5` | Diagrama ARQ-01 (F29 y F29B) |
| F29_UML_Academico.oom | [`docs/academico/powerdesigner/models/F29_UML_Academico.oom`](../powerdesigner/models/F29_UML_Academico.oom) | `9ce5f28d87898f44ec5bc1d2d29e72b8060ef97f1df8f61940dd32c5abdfe0d9` | Modelo fuente de ARQ-01 (sin cambios) |
| F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.docx | [`docs/academico/practica-11/F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.docx`](F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.docx) | `ff15834cab9babfddb37bc4f12c1d80d5defb745894ffde7df4a5860fa7859d5` | F11 adaptado histórico (sin cambios) |
| F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.pdf | [`docs/academico/practica-11/F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.pdf`](F11_Arquitectura_del_Sistema_ADAPTADO_Colegio_Andino.pdf) | `be590a7ae500ea3b5c164fa2b95ab865bede824458fd309f33393c69262cef1b` | PDF del F11 adaptado histórico (sin cambios) |
| m_arch.py | [`docs/academico/tools/f27b/m_arch.py`](../tools/f27b/m_arch.py) | `4ed88ac99968677bcd4d2a76ea3117e3256a5d33c5290af132d8aa2be5f420c4` | Modelo de datos de la arquitectura (sin cambios) |
| m_f11r.py | [`docs/academico/tools/f27b/m_f11r.py`](../tools/f27b/m_f11r.py) | `12e736aac690edb9c0b7d945200a43c277c90bf5b172ee9b39952da490a4bce4` | Contenido del F11 oficial: CMP-xx, estilo, decisiones y restricciones |
| f11r.py | [`docs/academico/tools/f27b/f11r.py`](../tools/f27b/f11r.py) | `22a4d0058aa4b44c9aa27e7c7515fe6656b34bdca559bc9bcfb99d3c1a6af461` | Relleno de la plantilla oficial y espejo en Markdown |
| 07-arquitectura-tecnologica.md | [`docs/final-report/07-arquitectura-tecnologica.md`](../../final-report/07-arquitectura-tecnologica.md) | `2693c5701162d64d482cd95ef797015f48f12cb9e0752ede0438e014c6507618` | Estilo, multitenencia, seguridad, PostgreSQL, Redis y despliegue |
| F7_Requerimientos_No_Funcionales_Colegio_Andino.md | [`docs/academico/practica-07/F7_Requerimientos_No_Funcionales_Colegio_Andino.md`](../practica-07/F7_Requerimientos_No_Funcionales_Colegio_Andino.md) | `c58460f8b8c55d1854a86c56a67471196d622d93b76dc603803ac7066a32f1c3` | Estado de los RNF (RNF-06 y RNF-07 no verificados; RNF-D propuesto) |

## Validación

`python docs/academico/tools/f27b/validate.py` incluye el bloque «F11-R». Comprueba:

- que la plantilla está registrada y que el documento deriva de ella: cabecera, estilos y numeración idénticos;
- la estructura oficial completa y la ausencia de instrucciones y líneas en blanco;
- los datos generales;
- CMP-01 a CMP-17 = C01 a C17 y R-01 a R-20 sin cambios;
- ARQ-01 incrustado sin modificar;
- el estilo, las decisiones con estado y las restricciones sin métricas inventadas;
- la cobertura de RF-01 a RF-27 y CU-01 a CU-20;
- el PDF;
- que el F11 adaptado no cambió.

La revisión visual de todas las páginas del PDF se registra en el informe de la fase.

**Recuento de evidencias** (observación F11R-O01 de la auditoría):

- Las tablas `evidencias/README.md` de las prácticas 02 a 11 suman **121 referencias** con SHA-256 a **91 archivos distintos**, con 0 ausentes, 0 discrepancias y 0 conflictos de hash. Es el recuento general vigente.
- El «81» del primer informe de la F11-R era un subconjunto: solo las prácticas 03, 05, 08 y 11, las cuatro con integración de PowerDesigner, que suman 81 referencias a 68 archivos. No debe usarse como recuento general.

## Limitaciones

- **Sin validación institucional.** La validación es interna y académica, sin aprobación ni firma de la institución.
- **RNF sin verificar.** RNF-06 (rendimiento) y RNF-07 (disponibilidad y recuperabilidad) siguen **NO VERIFICADOS**. La escalabilidad es una consideración, no una propiedad validada.
- **Imágenes del PDF.** Microsoft Word reduce las imágenes del PDF a unos 200 ppp; el DOCX conserva la resolución de la exportación.
- **LOW para la F31:** H-14, F28-L01, F29-L01, F29-L02 y F29B-OBS-01, sin cambios.
