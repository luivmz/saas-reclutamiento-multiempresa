# Fuentes oficiales del curso — guías y formatos originales

Ubicación canónica de las guías de práctica y de las plantillas oficiales del curso Pruebas y Calidad de Software (Universidad Continental, NRC 28607, Dr. Maglioni Arana Caparachin). Son la base para desarrollar los Formatos 02 a 08 y el entregable de la práctica 11. Se creó en la Fase 27B-0.

Inventario con los hashes: [`inventory.md`](inventory.md). Estado académico general: [`../ACADEMIC_BASELINE.md`](../ACADEMIC_BASELINE.md).

## Qué contiene

| Carpeta | Contenido |
|---|---|
| [`guias/`](guias/) | 9 guías oficiales: prácticas 02, 03, 04, 05, 06, 07, 08, 09 y 11 (`GUIA_PRACTICA_XX.docx`) |
| [`formatos-originales/`](formatos-originales/) | 8 plantillas oficiales vacías: Formatos 02 a 09 (`Formato_XX_<descripción>.docx`) |

**Identificación verificada:**

- Las nueve guías citan el NRC 28607, al docente y el curso.
- Las ocho plantillas citan el curso, pero no el NRC ni al docente: son formularios en blanco.
- Cada archivo abre con el título de su práctica o de su formato.

**Nombres de archivo.** Se normalizaron a ASCII y sin espacios para tener rutas estables. El nombre original de cada archivo figura en el inventario. El contenido no se modificó: el SHA-256 se comprobó antes y después de cada renombrado.

## Qué no contiene

- **Formato 11 oficial: NO DISPONIBLE.** La Guía 11 existe y remite a un «Formato 11: Arquitectura del sistema», pero esa plantilla no forma parte de las fuentes recibidas. Si se desarrolla el F11, será una **adaptación académica explícita** hecha por el equipo, nunca una plantilla oficial. Se desarrolló en la Fase 28 como adaptación académica, en `docs/academico/practica-11/`, identificada como tal.
- **Guías 01 y 10 y Formatos 01 y 10:** no forman parte de estas fuentes.
- **Formatos desarrollados por el equipo:**
  - el F9 entregado (histórico y final v1.1) vive en [`../phase-24/`](../phase-24/);
  - los Formatos 02 a 08 desarrollados por el equipo (Fase 27B) viven en `docs/academico/practica-02/` a `practica-08/`.
- **Material generado:** diagramas, BPMN, modelos de PowerDesigner y exportaciones viven en `docs/final-report/` y `docs/v1.1/`.

## Política de preservación

1. **Los originales no se modifican.** Nadie edita, rellena ni vuelve a guardar un archivo de esta carpeta. Para desarrollar un formato se trabaja sobre una copia fuera de ella, en la carpeta de la fase correspondiente.
2. **Los archivos no se reemplazan.** Si llega otra versión de una guía o de una plantilla, se añade con un nombre distinto y se registra en el inventario. Si su hash es distinto, no sustituye al anterior sin una decisión documentada.
3. **Cada cambio de esta carpeta** se refleja en [`inventory.md`](inventory.md), con su SHA-256.
4. **Los hashes se verifican con:**
   ```
   sha256sum docs/academico/00-fuentes-oficiales/*/*.docx
   ```

## Relación con `phase-24`

[`../phase-24/`](../phase-24/) es **evidencia histórica del release v1.1** (Formato 09, Fase 24) y se conserva **intacta**, con sus tres fuentes en la raíz:

- `GUÍA PRÁCTICA 09.docx`;
- `Formato 09 Alcance del proyecto software.docx`;
- el F9 histórico `F9_Alcance_Proyecto_Software_Colegio_Andino_NRC30180.docx`.

Su README, su [`source-map.md`](../phase-24/source-map.md) y el manifiesto del release citan esas rutas.

La Guía 09 y el Formato 09 de esta carpeta son **copias canónicas byte a byte** de esas fuentes históricas: tienen el mismo SHA-256. Existen para que la colección de guías y formatos esté completa en un solo lugar. Si alguna vez difirieran, prevalece la copia de `phase-24` como evidencia del release.

**Origen de esta carpeta.** Los 17 archivos aparecieron como cambio local sin versionar en `docs/academico/phase-24/00-fuentes-oficiales/`. La Guía 09 y el Formato 09 se habían movido allí desde la raíz de `phase-24`, y el F9 histórico ya no estaba en su ruta.

En la Fase 27B-0:

- los tres archivos de `phase-24` se restauraron desde Git, con el hash comprobado;
- los 17 se trasladaron aquí con nombres normalizados y el hash comprobado;
- la carpeta provisional quedó vacía y se eliminó.

No se perdió ningún archivo.
