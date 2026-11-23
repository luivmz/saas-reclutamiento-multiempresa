# Protocolo de validación de fuentes

Cada DOI del catálogo fue consultado individualmente en Crossref y cotejado con título, autores, editorial y fecha. Las respuestas originales y fechas de consulta están en REGISTROS_CROSSREF.json. Un DOI es identificación, no prueba por sí mismo de calidad metodológica o indexación. Las consultas bibliográficas iniciales tuvieron límites HTTP 429; no se cuentan como validaciones satisfactorias.

| Venue | Fuente oficial | Alcance de la comprobación |
| --- | --- | --- |
| ACM | https://www.acm.org/publications/policies/peer-review | Acceso web directo 403; corroborar política del journal en revisión humana. No hay informes individuales de revisión en este paquete. |
| IEEE | https://journals.ieeeauthorcenter.ieee.org/submit-your-article-for-peer-review/about-the-peer-review-process/ | Política oficial: revisión por al menos dos revisores cualificados. |
| Elsevier IST | https://www.sciencedirect.com/journal/information-and-software-technology/about/insights | Journal científico; acceso directo a insights bloqueado 403; confirmar política editorial al entregar. |
| MDPI AI | https://www.mdpi.com/journal/ai | Journal científico, artículo con DOI y abstract; política individual requiere revisión humana por límite 429. |
| NeurIPS / ICLR | https://proceedings.nips.cc/ / https://proceedings.iclr.cc/ | Artículos en actas oficiales de conferencia evaluada; edición 2024 verificada. |

La etiqueta de peer review se refiere al régimen del venue publicado, no a disponer de informes privados de revisión. Se requiere revisión humana de textos completos cuando el catálogo declara métodos, muestras o resultados pendientes. No se usaron blogs para completar esos campos.

Temas buscados: generative AI / LLM in software engineering, coding assistants, pair programming, colaboración humano IA, requisitos asistidos, unit test generation, seguridad, code review, mantenimiento, agentes, prompting, especificación, trazabilidad y TDD con IA. Para TDD se usa la evidencia RED/GREEN del repositorio y Beck como fundamento; no se encontró aquí un ensayo causal que pruebe eficacia de TDD+IA en este SaaS.

## Cotejos primarios adicionales

Consulta 03/11/2026. Los abstracts/versiones de autor se cotejaron con los DOI ya registrados; no se cuentan como preprints independientes.

| DOI publicado | Fuente primaria consultada |
| --- | --- |
| 10.1109/SP46214.2022.9833571 | https://doi.org/10.1109/SP46214.2022.9833571 |
| 10.1145/3524842.3528470 | https://sanadlab.org/assets/pdf/NguyenMSR22.pdf |
| 10.1109/ICSE-FoSE59343.2023.00008 | https://coinse.github.io/publications/pdfs/Fan2023yu.pdf |
| 10.1145/3520312.3534864 | https://arxiv.org/abs/2205.06537 |

MDPI identifica oficialmente AI como revista revisada por pares: https://www.mdpi.com/journal/AI. El catálogo oficial Elsevier identifica IST como revista de archivo: https://shop.elsevier.com/journals/information-and-software-technology/0950-5849. La política ACM se publica en https://www.acm.org/publications/policies/peer-review; el acceso directo a su texto fue bloqueado. La confirmación se refiere al régimen del venue, no a inspeccionar informes privados de revisión por artículo. No se atribuye indexación bibliométrica.

## Continuación: contenido y AI-DLC

Se completaron los campos de ART-02/04/05/10/14 mediante fuentes primarias: versión de autor de Fan; abstract Pearce enlazado al DOI; póster de autores en SIGCHI; versión de autor de Wang; sitio oficial IEEE/CAA JAS de Zhu. Las fuentes están en el catálogo de doble entrada. No son cinco publicaciones adicionales ni preprints independientes. La lectura de contenidos es parcial; no se inventan métodos ni muestras faltantes. AI-DLC se cotejó con las ocho páginas locales y la presentación AWS de Raja SP (31/07/2025), como white paper técnico separado de las veinte publicaciones científicas.
