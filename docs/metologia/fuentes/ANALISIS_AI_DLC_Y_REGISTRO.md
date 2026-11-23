# Análisis de AI-DLC y de la matriz de registro

## Procedencia y estatuto de la fuente AI-DLC

El PDF entregado tiene 8 páginas y el título AI-Driven Development Lifecycle (AI-DLC) Method Definition. Identifica a **Raja SP, Amazon Web Services**, p. 1. Es una definición técnica del método; no contiene DOI, venue académico, protocolo experimental, muestra ni evidencia de peer review. Se mantiene separado de las 20 publicaciones científicas. La presentación pública de AWS está fechada **31 de julio de 2025**: https://aws.amazon.com/blogs/devops/ai-driven-development-life-cycle/. Enlaza al mismo origen que figura en los pies del PDF: https://prod.d13rzhkk8cj2z0.amplifyapp.com/. La fecha de impresión y creación del PDF de marzo de 2026 no se confunde con fecha de publicación. No se mezcla con la variante comunitaria denominada AI-DLC 2026, cuya procedencia es distinta.

## Lectura por página

| Página | Contenido leído | Implicación para el SaaS |
|---|---|---|
| 1 | Contexto, enfoque AI-native, conversación y decisiones humanas; diseño integrado | Contrastar colaboración supervisada; no asumir reemplazo de ingeniería humana |
| 2 | Principios: capacidad real, responsabilidad humana, riesgos, flujo adaptable | Los controles del repositorio coinciden parcialmente; beneficios de velocidad son proposiciones del documento |
| 3 | Intent, Unit, Bolt; diseño de dominio/lógico, tests y deployment units | No asignar retrospectivamente esos IDs a RF, módulos o commits |
| 4 | Inception, Construction, Operations, workflow y contexto persistente | Docs y QA se corresponden; operación IA productiva no demostrada |
| 5 | Ejemplo greenfield, aclaración, requisitos, revisión y generación | Ejemplo ajeno, no actividad efectuada en Colegio Andino |
| 6 | Testing/validación, operaciones, brownfield y estrategias de adopción | V1→V2 se asemeja a mantenimiento brownfield; no acredita adopción formal |
| 7 | Prompts de ejemplo de configuración, inception y diseño | No son prompts históricos usados para implementar el SaaS |
| 8 | Ejemplos de código, arquitectura, despliegue e IaC | No incorporar AWS, Flask o Terraform al stack real por aparecer en el PDF |

## Definiciones y contraste

Intent es el propósito de alto nivel. Unit es un paquete cohesivo derivado de ese propósito; el documento espera bajo acoplamiento y despliegue independiente. Bolt es una iteración acotada de construcción y validación, expresada en horas/días. Inception elabora requisitos; Construction transforma el contexto validado en código probado; Operations aborda despliegue, observabilidad y mantenimiento supervisados. La IA propone planes, preguntas, artefactos y acciones; las personas conservan validación, decisiones y responsabilidad. Los controles incluyen criterios, riesgos, revisión del diseño, tests y trazabilidad persistente. Los ejemplos no prueban resultados experimentales ni equivalencia automática entre un monolito y Units independientes.

**COINCIDE:** contratos, supervisión como regla, contexto persistido y trazabilidad de artefactos. **PARCIALMENTE COINCIDE:** elaboración de requisitos, construcción, pruebas y correcciones, pues faltan conversaciones y aceptaciones exhaustivas por evento. **NO COINCIDE / NO DEMOSTRADO:** IDs formales Intent/Unit/Bolt, duración de Bolts, rituales Mob Elaboration/Construction y operación IA sobre despliegue productivo. Docker local y healthchecks no sustituyen esa evidencia. El detalle de once conceptos está en AI_DLC_vs_Proyecto de la matriz de doble entrada.

Riesgos del marco al aplicarlo: sobreconfianza, errores propagados, contexto desactualizado, automatización más rápida que la revisión, falta de evidencia de seguridad y atribución de ahorro no medido. Se mitigan con alcance, contratos, revisión humana, datos ficticios, pruebas con assertions, análisis estático y medición prospectiva. Estos controles se justifican también con Perry, Pearce, Barke y Wang; el white paper no valida causalmente la metodología propuesta.

## Matriz de registro original

La hoja **Bolts** ocupa 181 filas y 78 columnas formateadas (datos hasta BY, columna 77); filas 1–4 contienen títulos/encabezados y filas 5–181 contienen **177 registros de ejemplo**, con 83 rangos combinados, 2665 fórmulas y ninguna validación de datos. Se extrajeron todas las celdas no vacías en ESTRUCTURA_MATRIZ_REGISTRO.json. Su finalidad es registrar identificación del trabajo, uso de AI-DLC, coherencia técnica, trazabilidad y estabilidad. Combina 27 criterios de registro con evidencia, subtotales y resultados. Sus referencias Rails, Aurora, Trello, modelos IA, responsables, commits, CI y despliegues pertenecen a otro proyecto; no se consultan como si fueran pruebas del SaaS.

Identificación: Intent, Bolt, descripción, modelo, fecha, dominio, ticket y responsable. AI-DLC: propósito, requerimiento, derivación, diseño, commit, tests y despliegue. Coherencia: ubicación, capas, redundancia, responsabilidades, nombres, estructura y dependencias. Trazabilidad: IDs, requisitos, PR/commit, validación y despliegue. Estabilidad: comportamiento, alcance, regresiones, retrabajo inmediato, análisis estático, seguridad, tests y review aprobado.

**Alertas semánticas de fórmulas originales:** Y5 y sus equivalentes calculan Operations consultando S/U/W, aunque S y U son evidencias de commit/CI y W el registro de despliegue; por tanto no constituyen una medición limpia de tres criterios operacionales. BL181 está vacío pese a existir los registros funcionales de esa fila: BV181 puede promediar solo BU181. No hay celdas error almacenadas, pero esto no demuestra validez conceptual de las puntuaciones. No se copian esos porcentajes ni se corrige el original.

## Adaptación e incorporación

La matriz ISO organiza Macroproceso→Procedimiento→Actividad→Función; la matriz de registro evalúa eventos de cambio. Son unidades distintas: **una función no es necesariamente un Bolt**. Registro_vs_Evidencias conserva los 27 criterios, ruta, estado y pendiente sin inventar eventos. La matriz de funciones conserva commits, pruebas, archivo y responsable de rol, no un autor IA retrospectivo. Las variables VI describen el protocolo y controles; la VD mide calidad observada. La estabilidad o retrabajo atribuible a IA requiere medición prospectiva; no se deduce de un commit posterior. Sin deployment productivo autorizado, ese campo es NO APLICA JUSTIFICADO. Sin evidencia de PR aprobado, queda PENDIENTE. Un Sonar limpio no convierte PHPStan/Pint fallidos en controles superados.

La matriz no exige por sí misma artículos ni define variables causales. La integración científica es el nuevo cruce de artículos→dimensiones→etapas→indicadores→evidencia. No se usa un puntaje aditivo para probar eficacia ni conformidad ISO. La adaptación conserva las siete hojas de la plantilla de procesos y mantiene originales intactos.
