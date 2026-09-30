# Registro de ejecuciones de la actividad E1/L1 (F29C)

> **Lo completa el equipo con evidencia real.**
>
> - `build.py f29c` crea este archivo solo si no existe; **nunca lo sobrescribe**.
> - Requisitos, alcance y prompts: [`../ACTIVIDAD_IA_COMPARACION.md`](../ACTIVIDAD_IA_COMPARACION.md).

**Categorías:**

- **REQUISITO DE LA GUÍA:** Lo que propone la guía E1/L1 (enunciados 1 a 4). Se conserva tal cual, aunque no todo se exija en este entregable.
- **ALCANCE EFECTIVO DEL ENTREGABLE:** Lo que se exige para cerrar la F29C según el criterio docente informado por el equipo.
- **EVIDENCIA EJECUTADA:** Solo las filas del registro con estado `Completo` y la respuesta pegada.
- **NO REQUERIDO:** Fuera del alcance efectivo. No se ejecuta ni se presenta como ejecutado.

**Criterio docente informado por el equipo (30/09/2026): para este entregable no se exige ejecutar la comparación con Gemini, DeepSeek y Copilot. No es contenido de la guía E1/L1, que sí propone esa actividad comparativa, y el repositorio no contiene un documento del docente que lo respalde: lo registra el equipo.**

**Valores admitidos:**

- **Fecha:** DD/MM/AAAA.
- **Prompt usado:** `Sin cambios` o `Modificado`. Si es `Modificado`, en la sección de la respuesta se añade el prompt real entre `~~~~prompt` y `~~~~`, y una línea `Motivo del cambio: …`.
- **Enlace:** una URL `https://` o `No disponible`.
- **Captura:** rutas relativas a esta carpeta (`capturas/R-01.png`) separadas por `;`, o `No disponible`. `No aplica` solo vale si hay enlace.
- **Sin enlace ni captura:** la evidencia es el texto de la respuesta aportado por el equipo, y se declara así.
- **Estado:** `Pendiente` o `Completo`. `Completo` exige todos los campos y la respuesta pegada.
- **Respuestas:** se pegan completas entre `~~~~text` y `~~~~`. Así el código Python de P-03 no rompe el registro.
- **Columnas fijas:** no se modifican las columnas ID, Chatbot ni Prompt.

## 1. ALCANCE EFECTIVO — evidencia de ChatGPT (P-01 a P-06)

| ID | Chatbot | Prompt | Modelo / versión | Plan | Fecha | Prompt usado | Enlace | Captura | Estado |
|---|---|---|---|---|---|---|---|---|---|
| R-01 | ChatGPT | P-01 | GPT-5.6 Sol | No informado | 30/09/2026 | Sin cambios | No disponible | No disponible | Completo |
| R-02 | ChatGPT | P-02 | GPT-5.6 Sol | No informado | 30/09/2026 | Sin cambios | No disponible | No disponible | Completo |
| R-03 | ChatGPT | P-03 | GPT-5.6 Sol | No informado | 30/09/2026 | Sin cambios | No disponible | No disponible | Completo |
| R-04 | ChatGPT | P-04 | GPT-5.6 Sol | No informado | 30/09/2026 | Sin cambios | No disponible | No disponible | Completo |
| R-17 | ChatGPT | P-05 | GPT-5.6 Sol | No informado | 30/09/2026 | Sin cambios | No disponible | No disponible | Completo |
| R-18 | ChatGPT | P-06 | GPT-5.6 Sol | No informado | 30/09/2026 | Sin cambios | No disponible | No disponible | Completo |

## 2. ALCANCE EFECTIVO — integración con los capítulos 1 y 2

- **Fuente canónica:** los capítulos del repositorio, que no se sobrescriben.
- **P-05 y P-06:** son evidencia de la actividad.
- **Qué se anota:** qué coincide, qué difiere y cómo se trata cada diferencia (por ejemplo, «se descarta: dato no validado»).

| Capítulo | Fuente canónica | Evidencia | Coincidencias | Diferencias con la fuente canónica | Tratamiento |
|---|---|---|---|---|---|
| Capítulo 1 — Información general del proyecto | docs/final-report/01-informacion-general.md | R-17 | Título idéntico al de la línea base; plataforma web SaaS multiempresa; ciclo desde el requerimiento hasta el cierre (vacantes, postulaciones, evaluaciones, entrevistas, comparación, notificaciones y auditoría); monolito modular con aislamiento por organización; decisión final humana. | 1) Incluye el componente experimental de machine learning; el capítulo canónico (v1.0) deja la IA fuera de alcance, y el ML es de v1.1 (RF-29 candidato, experimental; docs/v1.1/ml/). 2) Sigue una estructura propia (descripción, objetivo general y alcance) y no la pedida por P-05 (1.1 Resumen ejecutivo y 1.2 Introducción): omite tecnologías, enfoque de pruebas y resultados. 3) Su objetivo general no dice «verificar» ni «con evidencia verificable de calidad», que sí figuran en el objetivo canónico (capítulo 2, §2.4). 4) Su alcance no precisa que solo se implementa el cierre con selección (A-30). | Se conserva el capítulo canónico sin cambios; no se incorpora texto de R-17. Queda como evidencia de la actividad. La mención al ML se mantiene solo como EXPERIMENTAL / PROPUESTO, según docs/v1.1/. |
| Capítulo 2 — Contexto organizacional y análisis del problema | docs/final-report/02-contexto-problema.md | R-18 | Colegio Andino de Huancayo como caso de estudio; proceso AS-IS PRELIMINAR sin validación institucional; decisión final humana; no se afirman beneficios medidos. Sus oportunidades de mejora equivalen a P1 (centralización), P2 (seguimiento), P3 (registro de evaluaciones y comparación), P4 (notificaciones) y P5 (trazabilidad). | 1) No desarrolla 2.1 y 2.2 con causas, consecuencias e impacto, como pedía P-06. 2) No nombra P1 a P5 ni su relación con los RF (§2.3). 3) Omite el límite honesto sobre P5 (sin tableros de indicadores de gestión) y los objetivos (§2.4). 4) Añade la idea de una plataforma «configurable, no acoplada a una sola institución», coherente con el modelo multiempresa pero ausente del capítulo canónico. | Se conserva el capítulo canónico sin cambios; no se incorpora texto de R-18. Queda como evidencia de la actividad; coincide con las restricciones del proyecto (AS-IS preliminar, decisión humana, sin beneficios medidos). |

## 3. NO REQUERIDO — Gemini, DeepSeek y Copilot (enunciado 2)

Nota histórica: la guía E1/L1 propone ejecutar P-01 a P-04 también en Gemini, DeepSeek y Copilot. Por el criterio docente informado por el equipo, no se exigen en este entregable. **No se ejecutaron** y no se presentan como ejecutados.

| ID | Chatbot | Prompt | Modelo / versión | Plan | Fecha | Prompt usado | Enlace | Captura | Estado |
|---|---|---|---|---|---|---|---|---|---|
| R-05 | Gemini | P-01 | — | — | — | — | — | — | NO REQUERIDO PARA EL CIERRE SEGÚN ACLARACIÓN DOCENTE INFORMADA POR EL EQUIPO |
| R-06 | Gemini | P-02 | — | — | — | — | — | — | NO REQUERIDO PARA EL CIERRE SEGÚN ACLARACIÓN DOCENTE INFORMADA POR EL EQUIPO |
| R-07 | Gemini | P-03 | — | — | — | — | — | — | NO REQUERIDO PARA EL CIERRE SEGÚN ACLARACIÓN DOCENTE INFORMADA POR EL EQUIPO |
| R-08 | Gemini | P-04 | — | — | — | — | — | — | NO REQUERIDO PARA EL CIERRE SEGÚN ACLARACIÓN DOCENTE INFORMADA POR EL EQUIPO |
| R-09 | DeepSeek | P-01 | — | — | — | — | — | — | NO REQUERIDO PARA EL CIERRE SEGÚN ACLARACIÓN DOCENTE INFORMADA POR EL EQUIPO |
| R-10 | DeepSeek | P-02 | — | — | — | — | — | — | NO REQUERIDO PARA EL CIERRE SEGÚN ACLARACIÓN DOCENTE INFORMADA POR EL EQUIPO |
| R-11 | DeepSeek | P-03 | — | — | — | — | — | — | NO REQUERIDO PARA EL CIERRE SEGÚN ACLARACIÓN DOCENTE INFORMADA POR EL EQUIPO |
| R-12 | DeepSeek | P-04 | — | — | — | — | — | — | NO REQUERIDO PARA EL CIERRE SEGÚN ACLARACIÓN DOCENTE INFORMADA POR EL EQUIPO |
| R-13 | Copilot | P-01 | — | — | — | — | — | — | NO REQUERIDO PARA EL CIERRE SEGÚN ACLARACIÓN DOCENTE INFORMADA POR EL EQUIPO |
| R-14 | Copilot | P-02 | — | — | — | — | — | — | NO REQUERIDO PARA EL CIERRE SEGÚN ACLARACIÓN DOCENTE INFORMADA POR EL EQUIPO |
| R-15 | Copilot | P-03 | — | — | — | — | — | — | NO REQUERIDO PARA EL CIERRE SEGÚN ACLARACIÓN DOCENTE INFORMADA POR EL EQUIPO |
| R-16 | Copilot | P-04 | — | — | — | — | — | — | NO REQUERIDO PARA EL CIERRE SEGÚN ACLARACIÓN DOCENTE INFORMADA POR EL EQUIPO |

## 4. NO REQUERIDO — comparaciones (enunciados 2 y 3)

Nota histórica: la guía propone estas comparaciones. El enunciado 3 (comparar con el chat compartido por el docente) también es una actividad comparativa. La aclaración, tal como la informó el equipo, nombra solo Gemini, DeepSeek y Copilot. El equipo decidió dejar también el enunciado 3 fuera del alcance efectivo, porque lo asocia a la misma actividad comparativa no exigida. Conviene confirmarlo con el docente.

- Cuadro comparativo de los 4 chatbots y diferencias cruciales (enunciado 2): **NO REQUERIDO PARA EL CIERRE SEGÚN ACLARACIÓN DOCENTE INFORMADA POR EL EQUIPO**
- T-01: revisión del chat compartido por el docente (https://chatgpt.com/share/68cee8ae-8474-8012-b657-5acd8a0a871c) (enunciado 3): **NO REQUERIDO PARA EL CIERRE SEGÚN ACLARACIÓN DOCENTE INFORMADA POR EL EQUIPO**
- Cuadro comparativo con el chat del docente y respuesta a sus dos preguntas (enunciado 3): **NO REQUERIDO PARA EL CIERRE SEGÚN ACLARACIÓN DOCENTE INFORMADA POR EL EQUIPO**

## 5. Respuestas completas (evidencia ejecutada)

### R-01 · ChatGPT · P-01

Respuesta completa, sin editar, entre las dos líneas `~~~~`:

~~~~text
Análisis y Diseño de una Plataforma SaaS Multiempresa para la Gestión del Reclutamiento, Evaluación y Selección de Personal con Apoyo de Machine Learning
~~~~

Evidencia: texto de la respuesta proporcionado por el equipo el 30/09/2026, de su conversación de ChatGPT (GPT-5.6 Sol). Sin enlace compartido ni captura.

Nota del registro:

- **Título propuesto por ChatGPT para el enunciado 1.** No sustituye el título de la línea base, que P-02 fija para las demás respuestas.
- **Diferencias con el título vigente:** omite «Caso de estudio: Colegio Andino de Huancayo» y añade «con Apoyo de Machine Learning».

### R-02 · ChatGPT · P-02

Respuesta completa, sin editar, entre las dos líneas `~~~~`:

~~~~text
Variable independiente:
Plataforma SaaS multiempresa para la gestión del reclutamiento, evaluación y selección de personal.

Variable dependiente:
Gestión del proceso de reclutamiento, evaluación y selección de personal.

Variables intermedias:
- TDD y pruebas automatizadas.
- ISO/IEC 25010 como marco de referencia para calidad.
- Arquitectura modular multiempresa y entorno reproducible mediante Docker.
- Machine learning experimental para estimar riesgo de demora del proceso.

La relación propuesta es que la plataforma SaaS facilite la gestión del proceso. Esa relación requiere evaluación posterior y no implica un beneficio ya demostrado.
~~~~

Evidencia: texto de la respuesta proporcionado por el equipo el 30/09/2026, de su conversación de ChatGPT (GPT-5.6 Sol). Sin enlace compartido ni captura.

### R-03 · ChatGPT · P-03

Respuesta completa, sin editar, entre las dos líneas `~~~~`:

~~~~text
Código Python propuesto:

import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12, 7))
ax.axis("off")

nodes = {
    "VIN1": (0.12, 0.78, "TDD y pruebas\nautomatizadas"),
    "VIN2": (0.12, 0.56, "ISO/IEC 25010\ncomo referencia"),
    "VIN3": (0.12, 0.34, "Arquitectura modular\nmultiempresa + Docker"),
    "VIN4": (0.50, 0.10, "Machine learning\nexperimental"),
    "VI": (0.50, 0.58, "VI\nPlataforma SaaS\nmultiempresa"),
    "VD": (0.84, 0.58, "VD\nGestión del proceso de\nreclutamiento, evaluación\ny selección"),
}

for _, (x, y, label) in nodes.items():
    ax.text(
        x, y, label,
        ha="center",
        va="center",
        bbox=dict(boxstyle="round,pad=0.5")
    )

def arrow(a, b, label=None, linestyle="-"):
    x1, y1, _ = nodes[a]
    x2, y2, _ = nodes[b]
    ax.annotate(
        "",
        xy=(x2 - 0.08, y2),
        xytext=(x1 + 0.08, y1),
        arrowprops=dict(arrowstyle="->", linestyle=linestyle)
    )
    if label:
        ax.text(
            (x1 + x2) / 2,
            (y1 + y2) / 2 + 0.04,
            label,
            ha="center"
        )

arrow("VIN1", "VI")
arrow("VIN2", "VI")
arrow("VIN3", "VI")
arrow("VI", "VD", "Se propone que mejore")
arrow("VIN4", "VD", "Apoyo experimental", "--")

plt.title("Diseño conceptual de variables")
plt.tight_layout()
plt.show()

Interpretación:
- VIN-1, VIN-2 y VIN-3 apoyan la VI.
- VI → VD es una hipótesis de trabajo / TO-BE PROPUESTO.
- VIN-4 actúa como apoyo experimental asociado al riesgo de demora.
- ML no evalúa ni clasifica candidatos.
~~~~

Evidencia: texto de la respuesta proporcionado por el equipo el 30/09/2026, de su conversación de ChatGPT (GPT-5.6 Sol). Sin enlace compartido ni captura.

Nota del registro:

- **Ejecución en Google Colab:** no consta que el código se haya ejecutado (protocolo, paso 6) y no se afirma.
- **Anexo 2:** el diagrama del Anexo 2 lo genera `f29c.py`, no este código. La estructura coincide: VIN-1 a VIN-3 → VI, VI → VD como hipótesis y VIN-4 → VD con trazo discontinuo.

### R-04 · ChatGPT · P-04

Respuesta completa, sin editar, entre las dos líneas `~~~~`:

~~~~text
Mantén como respuesta la matriz F29C ya construida y auditada, porque desarrolla esta propuesta:

VI:
Plataforma SaaS multiempresa.

Dimensiones:
- requerimientos y vacantes;
- postulaciones;
- evaluaciones y entrevistas;
- comparación y decisión;
- auditoría y aislamiento.

VD:
Gestión del proceso de reclutamiento, evaluación y selección.

Dimensiones:
- tiempo del proceso;
- flujo del proceso;
- cumplimiento;
- seguimiento/trazabilidad;
- percepción de gestión.

VIN-1:
TDD y pruebas automatizadas.

VIN-2:
ISO/IEC 25010 como marco de referencia.

VIN-3:
Arquitectura modular multiempresa y Docker.

VIN-4:
Machine learning experimental para riesgo de demora.

Instrumentos:
- ficha de observación;
- lista de cotejo;
- cuestionario Likert.

Escalas:
- nominal Sí/No o Cumple/No cumple;
- conteo;
- días;
- porcentaje;
- Likert 1–5;
- probabilidad/clase cuando corresponda al experimento ML.

No inventar mediciones ni resultados.
~~~~

Evidencia: texto de la respuesta proporcionado por el equipo el 30/09/2026, de su conversación de ChatGPT (GPT-5.6 Sol). Sin enlace compartido ni captura.

Nota del registro:

- **Remite a la matriz de la F29C.** Esa matriz se elaboró con la evidencia del repositorio y está **pendiente de auditoría**; no está «auditada», como dice el texto.
- **Dimensiones de la VI:** agrupa las cinco de la F29C de otra forma. La F29C usa las soluciones S-01 a S-05.
- **Dimensiones de la VD:** propone tiempo, flujo, cumplimiento, seguimiento y trazabilidad, y percepción. La F29C usa P1 a P5 del F4 con OM-01 a OM-05.
- **Escala «probabilidad/clase»:** la F29C no la adopta como escala de medición. La salida del modelo RF-29 es experimental.
- **La matriz del Anexo 1 no cambia.**

### R-17 · ChatGPT · P-05

Respuesta completa, sin editar, entre las dos líneas `~~~~`:

~~~~text
Título:
Análisis y Diseño de una Plataforma SaaS Multiempresa para la Gestión del Reclutamiento, Evaluación y Selección de Personal – Caso de estudio: Colegio Andino de Huancayo.

Descripción:
El proyecto plantea el análisis, diseño e implementación de una plataforma web SaaS multiempresa orientada a centralizar y dar trazabilidad a actividades del proceso de reclutamiento, evaluación y selección de personal. La solución considera requerimientos de personal, vacantes, postulaciones, evaluaciones, entrevistas, comparación de candidatos, decisión final humana, cierre, notificaciones y auditoría.

La solución utiliza una arquitectura de monolito modular y aislamiento lógico por organización. El componente experimental de machine learning se limita a estimar riesgo operacional de demora del proceso y no toma decisiones sobre contratación ni clasifica candidatos.

Objetivo general:
Desarrollar una plataforma SaaS multiempresa que permita gestionar de manera estructurada y trazable las actividades del proceso de reclutamiento, evaluación y selección de personal.

Alcance:
Comprende la gestión desde el requerimiento de personal hasta el cierre del proceso de selección, incluyendo trazabilidad y soporte para comparación. La decisión final continúa siendo humana.
~~~~

Evidencia: texto de la respuesta proporcionado por el equipo el 30/09/2026, de su conversación de ChatGPT (GPT-5.6 Sol). Sin enlace compartido ni captura.

### R-18 · ChatGPT · P-06

Respuesta completa, sin editar, entre las dos líneas `~~~~`:

~~~~text
El caso de estudio corresponde al Colegio Andino de Huancayo.

La descripción actual del proceso institucional debe tratarse como AS-IS PRELIMINAR, ya que no existe evidencia de validación institucional formal.

A partir del análisis académico se identifican oportunidades de mejora relacionadas con:
- centralización de información;
- seguimiento de etapas;
- registro de evaluaciones;
- comparación estructurada;
- notificaciones;
- trazabilidad.

Como respuesta se propone una plataforma SaaS multiempresa configurable, evitando un diseño rígidamente acoplado a una sola institución.

El TO-BE contempla digitalización y trazabilidad de requerimientos, vacantes, postulaciones, evaluaciones, entrevistas y cierre.

La decisión final permanece bajo responsabilidad humana.

No se afirman reducciones de tiempo, mejoras porcentuales ni beneficios institucionales medidos porque no han sido evaluados formalmente.
~~~~

Evidencia: texto de la respuesta proporcionado por el equipo el 30/09/2026, de su conversación de ChatGPT (GPT-5.6 Sol). Sin enlace compartido ni captura.
