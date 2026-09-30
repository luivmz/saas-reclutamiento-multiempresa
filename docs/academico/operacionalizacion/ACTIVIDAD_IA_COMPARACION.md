# Actividad E1/L1 — paquete de ejecución

> Generado por `docs/academico/tools/f27b/f29c.py` desde `m_variables.py`: no se edita a mano. La evidencia se registra en [`evidencias-ia/REGISTRO_EJECUCIONES_IA.md`](evidencias-ia/REGISTRO_EJECUCIONES_IA.md), que completa el equipo.

**Estado:** La guía E1/L1 propone la actividad completa: 4 prompts en 4 chatbots, comparaciones y capítulos 1 y 2. Por el criterio docente informado por el equipo, el alcance efectivo de este entregable es la evidencia de ChatGPT (P-01 a P-06) y su integración con los capítulos 1 y 2. Gemini, DeepSeek, Copilot y el chat del docente quedan NO REQUERIDOS y no se presentan como ejecutados. La evidencia está en el registro de ejecuciones, y `validate.py --cierre-f29c` informa si está completa.

**Categorías que usa este paquete:**

| Categoría | Significado |
|---|---|
| **REQUISITO DE LA GUÍA** | Lo que propone la guía E1/L1 (enunciados 1 a 4). Se conserva tal cual, aunque no todo se exija en este entregable. |
| **ALCANCE EFECTIVO DEL ENTREGABLE** | Lo que se exige para cerrar la F29C según el criterio docente informado por el equipo. |
| **EVIDENCIA EJECUTADA** | Solo las filas del registro con estado `Completo` y la respuesta pegada. |
| **NO REQUERIDO** | Fuera del alcance efectivo. No se ejecuta ni se presenta como ejecutado. |

## 1. REQUISITO DE LA GUÍA

Texto de la guía E1 («Actividades para la sesión»). La L1 propone lo mismo.

| Enunciado | Pedido de la guía E1 | Entrega que implica |
|---|---|---|
| Enunciado 1 | Usar ChatGPT en su versión gratuita para definir el título del proyecto; hacer con la IA la matriz de operacionalización de variables, para conocer los indicadores de la predicción con machine learning, y documentar en el informe la matriz y la definición conceptual. | Obligatorio: P-01 a P-04 en ChatGPT gratuito (R-01 a R-04) |
| Enunciado 2 | Usar los mismos prompts en Gemini, DeepSeek y Copilot; comparar los 4 chatbots y mencionar las diferencias cruciales encontradas. | Obligatorio: P-01 a P-04 en Gemini, DeepSeek y Copilot (R-05 a R-16) y el cuadro comparativo |
| Enunciado 3 | Revisar el chat compartido por el docente y compararlo con el obtenido por el equipo: ¿es igual a lo mostrado o hubo problemas para generar la información deseada?, ¿por qué hubo diferencias? Hacer un cuadro comparativo de los principales cambios. | Obligatorio: evidencia del chat del docente (T-01), cuadro comparativo y respuesta a las dos preguntas |
| Enunciado 4 | Usar prompts que den la información necesaria para el capítulo 1 y el capítulo 2, y documentar los resultados en la plantilla Word. | Obligatorio: P-05 y P-06 (R-17 y R-18) y su volcado en la plantilla Word |

Chat compartido por el docente en la guía (enunciado 3): https://chatgpt.com/share/68cee8ae-8474-8012-b657-5acd8a0a871c

## 2. ALCANCE EFECTIVO DEL ENTREGABLE

**Criterio docente informado por el equipo (30/09/2026): para este entregable no se exige ejecutar la comparación con Gemini, DeepSeek y Copilot. No es contenido de la guía E1/L1, que sí propone esa actividad comparativa, y el repositorio no contiene un documento del docente que lo respalde: lo registra el equipo.**

El enunciado 3 (comparar con el chat compartido por el docente) también es una actividad comparativa. La aclaración, tal como la informó el equipo, nombra solo Gemini, DeepSeek y Copilot. El equipo decidió dejar también el enunciado 3 fuera del alcance efectivo, porque lo asocia a la misma actividad comparativa no exigida. Conviene confirmarlo con el docente.

| ID | Enunciado | Requisito de la guía | Alcance en este entregable | Dónde consta |
|---|---|---|---|---|
| REQ-01 | Enunciado 1 | P-01 a P-04 en ChatGPT (la guía pide la versión gratuita): título, variables, diagrama conceptual y matriz de operacionalización | REQUERIDO | R-01 a R-04 |
| REQ-02 | Enunciado 1 | Documentar en el informe la matriz de operacionalización y la definición conceptual | REQUERIDO | F29C_Operacionalizacion_Variables (DOCX, PDF y Markdown) |
| REQ-03 | Enunciado 2 | Usar los mismos prompts en Gemini, DeepSeek y Copilot | NO REQUERIDO PARA EL CIERRE SEGÚN ACLARACIÓN DOCENTE INFORMADA POR EL EQUIPO | R-05 a R-16 |
| REQ-04 | Enunciado 2 | Cuadro comparativo de los 4 chatbots y diferencias cruciales | NO REQUERIDO PARA EL CIERRE SEGÚN ACLARACIÓN DOCENTE INFORMADA POR EL EQUIPO | — |
| REQ-05 | Enunciado 3 | Revisar el chat compartido por el docente, cuadro comparativo y dos preguntas | NO REQUERIDO PARA EL CIERRE SEGÚN ACLARACIÓN DOCENTE INFORMADA POR EL EQUIPO | T-01 |
| REQ-06 | Enunciado 4 | Prompts para los capítulos 1 y 2 y sus resultados | REQUERIDO | R-17 y R-18 |
| REQ-07 | Enunciado 4 | Documentar esos resultados: se integran como evidencia frente a los capítulos 1 y 2 del repositorio, que siguen siendo la fuente canónica | REQUERIDO | Registro, sección «Integración con los capítulos 1 y 2» |

## 3. EVIDENCIA EJECUTADA

- **Dónde está:** en el [registro](evidencias-ia/REGISTRO_EJECUCIONES_IA.md). Solo cuenta como evidencia ejecutada una fila con estado `Completo`, sus datos y la respuesta completa pegada.
- **Cuántas ejecuciones exige el alcance efectivo:** R-01 (P-01), R-02 (P-02), R-03 (P-03), R-04 (P-04), R-17 (P-05), R-18 (P-06), todas en ChatGPT.
- **Estado actual:** lo informa `python docs/academico/tools/f27b/validate.py --cierre-f29c`.
- **Capítulos 1 y 2:** P-05 y P-06 son evidencia de la actividad, no reemplazan los capítulos. La fuente canónica es la documentación del repositorio:
  - [`docs/final-report/01-informacion-general.md`](../../../docs/final-report/01-informacion-general.md).
  - [`docs/final-report/02-contexto-problema.md`](../../../docs/final-report/02-contexto-problema.md).
- **Diferencias:** las que haya entre una respuesta y la fuente canónica se anotan en el registro, sin sobrescribir el contenido validado.

## 4. NO REQUERIDO

| ID | Requisito de la guía | Estado |
|---|---|---|
| REQ-03 | Enunciado 2: Usar los mismos prompts en Gemini, DeepSeek y Copilot | NO REQUERIDO PARA EL CIERRE SEGÚN ACLARACIÓN DOCENTE INFORMADA POR EL EQUIPO |
| REQ-04 | Enunciado 2: Cuadro comparativo de los 4 chatbots y diferencias cruciales | NO REQUERIDO PARA EL CIERRE SEGÚN ACLARACIÓN DOCENTE INFORMADA POR EL EQUIPO |
| REQ-05 | Enunciado 3: Revisar el chat compartido por el docente, cuadro comparativo y dos preguntas | NO REQUERIDO PARA EL CIERRE SEGÚN ACLARACIÓN DOCENTE INFORMADA POR EL EQUIPO |

**Qué implica:**

- Las filas R-05 a R-16 (Gemini, DeepSeek y Copilot) y T-01 (chat del docente) se conservan en el registro como constancia histórica de lo que propone la guía, con ese estado.
- Nunca se marcan `Completo` ni se citan como ejecutadas.
- Si el equipo decide ejecutarlas, se cambia su alcance en `m_variables.py` y se registran como evidencia.

## 5. Protocolo de ejecución (alcance efectivo)

1. **Una conversación nueva de ChatGPT.** La guía pide la versión gratuita: anota el plan que se usó.
2. **Prompts en orden y sin editar.** Pega P-01 a P-06 en esa misma conversación, uno por mensaje, y espera a que cada respuesta termine antes del siguiente.
3. **Una respuesta por prompt.** Si regeneraste alguna, registra la que usaste.
4. **Cada respuesta se pega completa y sin editar** en su sección del registro.
5. **Enlace y captura.** Guarda el enlace compartido o una captura si puedes. Si no hay ninguno, escribe «No disponible»: la evidencia queda como texto aportado por el equipo, y así se declara.
6. **P-03:** anota si el código Python se ejecutó en Google Colab sin corregirlo.
7. **P-05 y P-06:** completa la sección «Integración con los capítulos 1 y 2» del registro. Anota coincidencias y diferencias con la fuente canónica y cómo se tratan; los capítulos del repositorio no se sobrescriben.
8. **No pegues datos personales reales:** el caso de estudio es ficticio.
9. **Comprueba el cierre:** `python docs/academico/tools/f27b/validate.py --cierre-f29c`.

## 6. Prompts listos para copiar

### P-01 — Título del proyecto (Enunciados 1 y 2)

```text
Para comenzar, actúa como un estudiante de pregrado de la carrera universitaria de Ingeniería de Sistemas e Informática, donde debemos realizar un sistema informático web que ayude a mejorar la gestión del reclutamiento, la evaluación y la selección de personal de un colegio privado de Huancayo (caso de estudio académico), ofrecido como plataforma SaaS multiempresa. El sistema también usará herramientas de machine learning para estimar el riesgo de demora del proceso de selección, sin evaluar ni clasificar a los postulantes. Podrías redactar el título del proyecto, con máximo 25 palabras; si puedes incluir alguna normativa ISO o metodología de desarrollo en el título, entonces hazlo.
```

### P-02 — Variables (Enunciados 1 y 2)

```text
He definido el título del proyecto de la siguiente forma: "Análisis y Diseño de una Plataforma SaaS Multiempresa para la Gestión del Reclutamiento, Evaluación y Selección de Personal – Caso de estudio: Colegio Andino de Huancayo". Con este título, define la variable dependiente (donde está el problema), la variable independiente (la solución planteada) y las variables intermedias (la metodología, los principios y las herramientas de apoyo a utilizarse). Ten en cuenta que el proyecto busca desarrollar una plataforma web multiempresa que registre y controle el reclutamiento, la evaluación y la selección de personal. La plataforma se desarrolla con desarrollo guiado por pruebas (TDD) y pruebas automatizadas, con la norma ISO/IEC 25010 como marco de referencia de calidad y con una arquitectura modular multiempresa desplegada con Docker. De la plataforma se exportarán indicadores del proceso para predecir, con herramientas de machine learning, el riesgo de demora del proceso de selección. La decisión final de contratación la toma siempre una persona. Muéstrame la información de forma breve.
```

### P-03 — Diagrama conceptual (Enunciados 1 y 2)

```text
Muéstrame el diagrama conceptual para visualizar la relación entre estas variables. Muéstralo en código Python para poder generar el diagrama en Google Colab.
```

### P-04 — Matriz de operacionalización (Enunciados 1 y 2)

```text
Con esto en cuenta, ahora vamos a formar la matriz de operacionalización de variables, donde debe tener las columnas de variables, dimensiones, indicadores, ítems de medición, instrumentos de recolección de datos y escala de medición: cada variable tiene varias dimensiones; cada dimensión tiene varios indicadores; cada indicador tiene varios ítems de medición; los instrumentos de medición pueden ser una ficha de observación, una lista de cotejo o un cuestionario Likert; la escala de medición está relacionada con los indicadores. Hay que tener en cuenta que los indicadores y los ítems de medición de la variable dependiente (la gestión del proceso de reclutamiento, evaluación y selección de personal) se utilizarán para predecir con machine learning el riesgo de demora del proceso; no se evaluará ni se clasificará a los postulantes.
```

### P-05 — Capítulo 1 de la plantilla final (Enunciado 4)

```text
Con la información del proyecto de esta conversación, redacta el Capítulo 1 «Información general del proyecto» del informe final, con dos secciones. 1.1 Resumen ejecutivo, de media página a una página: el problema identificado, la solución tecnológica propuesta, las tecnologías utilizadas (Laravel, React con TypeScript, PostgreSQL, Redis, Docker, PHPUnit y Cypress), el enfoque de calidad aplicado y los principales resultados obtenidos. 1.2 Introducción: el contexto general del proyecto, la importancia de las pruebas de software en el desarrollo moderno, el propósito del sistema y una breve descripción de la estructura del informe en 14 capítulos. No inventes resultados, cifras, fechas ni nombres de personas: donde falte un dato, escribe [COMPLETAR].
```

### P-06 — Capítulo 2 de la plantilla final (Enunciado 4)

```text
Redacta ahora el Capítulo 2 «Contexto organizacional y análisis del problema», con dos secciones. 2.1 Contexto de la organización: descripción del escenario (un colegio privado de Huancayo usado como caso de estudio académico), sus actividades principales, el área donde se presenta el problema (el reclutamiento, la evaluación y la selección de docentes y personal) y las herramientas tecnológicas que usa actualmente. 2.2 Identificación del problema: descripción detallada, causas, consecuencias operativas e impacto en la eficiencia del proceso. Considera cinco problemas del proceso actual: información distribuida, seguimiento manual, evaluaciones heterogéneas, comunicación manual con los postulantes e indicadores limitados para sustentar la decisión. Las herramientas actuales y las cifras del colegio no están validadas: no las inventes y escribe [COMPLETAR] donde falten.
```

## 7. Evidencia mínima por ejecución

| Campo | Qué se registra |
|---|---|
| Chatbot y modelo | Nombre del chatbot y modelo o versión que muestra la interfaz |
| Plan | Gratuito u otro; «No informado» si no se registró |
| Fecha | Día de la ejecución, en formato DD/MM/AAAA |
| Prompt usado | «Sin cambios», o «Modificado» con el prompt real y el motivo |
| Respuesta | Texto completo, sin editar, entre `~~~~text` y `~~~~` |
| Enlace | Enlace compartido o «No disponible»; nunca uno inventado |
| Captura | Ruta en `evidencias-ia/capturas/`, «No disponible», o «No aplica» si hay enlace |

## Qué no se hace

- No se escribe ninguna respuesta, cifra ni conclusión sin la ejecución real que la respalde.
- No se presenta como ejecutado nada NO REQUERIDO, ni como texto de la guía el criterio docente informado por el equipo.
- La matriz y el diagrama de la F29C los elaboró el asistente de IA del equipo (Claude, en Claude Code) a partir de la evidencia versionada del repositorio, siguiendo las reglas de la guía. No sustituyen la actividad de la guía con ChatGPT, que se registra aparte.
