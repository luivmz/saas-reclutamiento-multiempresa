# Ética y supervisión humana

**Fase 14 · 20 de septiembre de 2026**

El sistema gestiona procesos que afectan el acceso de personas a un empleo. Cualquier componente automático mal encuadrado terminaría, directa o indirectamente, influyendo en decisiones sobre ellas. Este documento fija la frontera y la hace verificable.

---

## 1. La frontera

**[APROBADA] `ML-ETHICS-01`** *(decisiones 1 y 9 del equipo, 20/09/2026)* — El modelo analiza **el comportamiento del proceso**. Nunca a una persona. La unidad de análisis es siempre una vacante/proceso.

### Puede estimar

Riesgo de que una convocatoria cierre fuera de su plazo operacional objetivo, y las señales agregadas de carga y backlog que lo acompañan. La unidad es la vacante, no el postulante.

### No puede, sin excepción

- Puntuar, ordenar, recomendar, filtrar, preseleccionar o descartar postulantes.
- Estimar desempeño, idoneidad, permanencia, personalidad o «ajuste cultural».
- Usar, inferir o aproximar raza, etnia, sexo, género, religión, orientación sexual, salud, discapacidad, ideología política, afiliación sindical, biometría, edad, nacionalidad o estado civil.
- Usar proxies socioeconómicos: universidad, centro de estudios, ubicación de residencia, nivel educativo del candidato.
- Alimentar, alterar o reordenar el ranking de RF-20 a RF-22.
- Intervenir en la decisión final de RF-23 a RF-25.
- Evaluar, de forma directa o indirecta, a los trabajadores que operan el proceso.

La lista exhaustiva de variables prohibidas está en [`feature-contract.md` §3](feature-contract.md).

**[LIMITACIÓN]** Si una propuesta futura necesita cruzar esta frontera, la respuesta es no. Se registra la petición como descartada, con su motivo, y se continúa.

---

## 2. Por qué esta frontera y no otra

Un modelo que puntúa candidatos reproduce y amplifica los sesgos de los datos con los que se entrena, y traslada a una función matemática una responsabilidad que pertenece a una persona identificable. En un contexto educativo y con datos sintéticos, presentarlo como capacidad sería además deshonesto: no habría forma de validar su efecto real sobre personas reales.

Estimar el riesgo de demora de un **proceso** no tiene ese problema. El sujeto de la predicción es un flujo de trabajo organizacional, el error se paga en atención del equipo de RR. HH. y nadie ve alterada su candidatura por la salida del modelo.

---

## 3. Supervisión humana

**[HECHO]** Las garantías que el sistema ya implementa y que v1.1 no puede debilitar:

| Garantía | Evidencia |
|---|---|
| El cierre exige decisión final y selección humanas previas | `app/Services/Selection/VacancyClosureService.php:44-46` |
| La decisión registra responsable, justificación e instante | `database/migrations/2026_09_13_000011_create_selection_decisions_table.php:17-22` |
| Una vacante solo puede tener un seleccionado | Índice único parcial, `…000011…:34` |
| Los estados terminales no admiten retorno | `app/Enums/ApplicationStatus.php:31` |
| Solo hay tres estados de vacante y el cierre es irreversible | `app/Enums/VacancyStatus.php:20-24` |
| La auditoría es de solo inserción | `database/migrations/2026_09_13_000012_make_audit_logs_append_only.php` |

**[PROPUESTA]** Garantías adicionales que el componente de ML deberá cumplir:

1. La estimación es **informativa**: no dispara ninguna acción automática, ni siquiera una notificación a candidatos.
2. Ningún servicio de ML puede escribir estados, postulaciones, ranking ni decisiones.
3. La plataforma funciona completa si el componente no existe o está caído.
4. La estimación se presenta lejos del ranking, de la comparación de candidatos y de la decisión final.
5. Toda salida se rotula como **estimación sintética experimental**, con su versión de modelo y de umbrales.
6. Quien vea la estimación puede ignorarla sin fricción y sin justificarlo.

---

## 4. Rotulado obligatorio en la interfaz futura

**[PROPUESTA]** Si RF-29 llegara a aprobarse, toda presentación debe incluir:

- la palabra **estimación**, no «predicción» ni «riesgo real»;
- la incertidumbre visible, no un número solo;
- el origen: datos sintéticos, prototipo académico, sin validación institucional;
- el aviso de que **no evalúa personas**;
- la versión del modelo y de los umbrales.

> **Nota de evolución (hotfix final de la Fase 21, 23/09/2026).** Este rotulado es una **propuesta condicionada a la aprobación de RF-29**, que sigue pendiente. La tarjeta experimental implementada en la Fase 16 lleva la etiqueta «Experimental», dice que estima el proceso y no a las personas, que el modelo se entrenó con datos sintéticos y que la decisión es humana, pero **no muestra incertidumbre**, porque el contrato implementado no la tiene. Si RF-29 se aprueba, cumplir o reformular ese punto es una decisión del equipo.

Texto permitido para la explicación: **«Factores operacionales asociados a la estimación de riesgo»**.
Texto prohibido: cualquier formulación que sugiera que un candidato es mejor, peor, apto o no apto.

---

## 5. Privacidad en el límite Laravel ↔ ML

**[PROPUESTA]**

- Solo cruzan el límite conteos, duraciones y días: ningún identificador de persona, ningún texto libre, ningún puntaje.
- `organization_id` **no** se envía: se usa dentro de Laravel para agrupar, no como señal.
- El registro técnico no guarda el vector completo si eso aumenta el riesgo de reidentificación; guarda versión de modelo, resultado técnico, latencia y un correlation ID.
- No se obtienen, descargan ni usan datos reales ni PII en ninguna fase del experimento.

---

## 6. Declaración de validez

**[LIMITACIÓN]** Texto obligatorio en el informe académico, en la model card y en cualquier pantalla derivada:

> Los datos sintéticos permiten demostrar metodología, entrenamiento, integración y evaluación técnica. No demuestran validez predictiva real sobre procesos del Colegio Andino de Huancayo ni autorizan uso institucional.

## Enlaces

- [Definición del problema](problem-definition.md) · [Contrato de features](feature-contract.md) · [Model card](model-card-draft.md) · [ADR-002 Supervisión humana](../architecture-decisions/ADR-002-human-oversight.md) · [Índice de la Fase 14](../phase-14-ml-definition.md)
