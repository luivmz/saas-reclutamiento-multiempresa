# Prototipo de «Cómo postular» con Spline

**Estado.** Preparación local en `feature/proceso-postulacion-3d`, desde `01b26d17e8f3aec9e89f7f44a834f8dcbcb89bf4`. La interfaz HTML, su ilustración estática y el contrato de carga están implementados. El carrusel se validó y refinó en el editor de Spline el 24/11/2026. Ese mismo día el equipo eligió la opción A, y el export quedó integrado en la portada con `@splinetool/runtime` 2.0.198. En escritorio capaz se muestra la escena y en los demás casos queda la ilustración estática. Detalle en [Integración del export](#integración-del-export-24112026).

La sección explica la consulta pública de convocatorias (RF-07), la cuenta de postulante (RF-08), el perfil y el CV (RF-09), y la postulación y su seguimiento (RF-10 a RF-11). Seleccionar un paso cambia su explicación y la ilustración. Los enlaces llevan al listado y al registro real. El encabezado principal y el bloque institucional del proceso conservan su composición.

## Export inspeccionado

Archivo Code proporcionado por el usuario, recibido el 24/11/2026. La descarga válida respondió HTTP 200 y pesa 107 924 B. SHA-256 `9745f2399976e99036a75fd45f350edc556a4031e6f52b5fd516499c9638453d`. [Export evaluado](https://prod.spline.design/Osw7wpav2hQg6Iiz/scene.splinecode)

Se abrió en Chrome aislado con `@splinetool/runtime` 2.0.219, `htmlContentMode: 'none'` y el WASM del paquete servido desde la copia de inspección. `getAllObjects()` devolvió 104 nodos, incluidos grupos, piezas y luces. `getVariables()` y `getSplineEvents()` devolvieron objetos vacíos. No se observó cambio de pose o estado al pasar el cursor y pulsar sobre `speaker`, `card`, `folder` y `bell`. La captura conserva la atribución mostrada por el export. El inventario completo está en `inventario-spline.json` y la captura en `spline-plantilla.png`, dentro de la carpeta de evidencia.

La carpeta y la campana son aprovechables. El megáfono comunica un anuncio, la tarjeta actual parece bancaria y los demás motivos distraen del flujo. Esta composición se descartó al elegir el carrusel. En su estado actual carece de los cuatro estados coordinados que requiere la portada.

## Carrusel elegido para la adaptación

La copia indicada por el equipo es **Carousel Tutorial for Community - Copy**. El enlace recibido abre el editor. El archivo de Code evaluado anteriormente pertenece a la plantilla morada y queda solo como antecedente. Su respaldo, la validación en el editor y el refinado se registran más abajo. El export sigue pendiente. [Editor de la copia](https://app.spline.design/file/fc79e84d-24a7-4d2c-bbfa-c08463c5a601)

Antes de editar, guarde un duplicado recuperable e identifique el autor y la atribución desde la ficha del original. Pruebe ambas flechas y registre el índice, límites, estados y eventos que controlan el desplazamiento. Reutilice esa navegación y adapte sus referencias a cuatro posiciones. La tarjeta seleccionada queda completa en el centro y las vecinas orientan el recorrido. El póster HTML sigue disponible en móvil y con movimiento reducido.

| Paso | Grupo | Título visible en la tarjeta | Motivo y contenido |
|---|---|---|---|
| 1 | `convocatoria` | Elija una convocatoria | Maletín y ficha de puesto con requisitos, criterios y cierre |
| 2 | `cuenta` | Cree su cuenta | Silueta de usuario y acceso como postulante |
| 3 | `perfil_cv` | Complete su perfil y cargue su CV | Carpeta abierta, documento y CV en PDF |
| 4 | `seguimiento` | Postule y siga su avance | Documento registrado e historial en Mis postulaciones y Notificaciones |

Use materiales mate y fondo compatible con ambos temas. Los colores primarios están en `resources/css/app.css`: petróleo en claro (`oklch(0.452 0.077 213)`) y turquesa en oscuro (`oklch(0.731 0.083 201)`). Colores de referencia para la escena: `#0B5D6C`, `#67B9BE`, `#FAFDFD`, `#C9D6D9` y `#45595D`. Reserve suficiente margen para la tarjeta central en el marco 16:10. Use desplazamientos cortos al seleccionar, sin autoavance.

El contrato previsto utiliza un solo índice numérico, `applicationStep` (1–4, inicial 1). La selección HTML establece el índice. Las flechas del carrusel deben notificar el valor resultante al mismo estado de React mediante el callback del cargador. La sesión local descarta valores inválidos, duplicados y eventos recibidos durante la carga, pausa o después del desmontaje. El vínculo concreto con el evento del editor queda sujeto a inspección del export. Antes de conectarlo, verifique los saltos directos desde HTML y el recorrido en ambos sentidos en Preview y en el runtime. Registre URL de Code, revisión, hash, atribución y recursos dependientes.

## Cómo conectar o sustituir un export

Use la **Code API para Web** del runtime oficial. En una fase que disponga del export, fije y revise una versión compatible de `@splinetool/runtime` y cárguela con `import()` desde el adaptador de `loadScene`. Compruebe que el entorno gráfico es compatible con el renderer del export antes de solicitar la escena. Prepare una instancia del runtime para el canvas entregado por el componente y resuelva la promesa cuando esté disponible el primer cuadro. Al resolver, el contrato `LoadApplicationScene` aplica la selección vigente. El adaptador asigna `applicationStep` mediante la API de variables, pausa y reanuda mediante la API de ejecución confirmada de la versión fijada y libera el runtime al recibir el `AbortSignal` o al desmontar. Maneje también el error de decodificación o inicialización en el adaptador. Mantenga el mismo nombre de variable y los cuatro valores al sustituir el recurso. [Code API para Web](https://docs.spline.design/exporting-your-scene/web/code-api-for-web)

La portada usa el mismo criterio de capacidad del resto de escenas para ancho, puntero, movimiento reducido, ahorro de datos y equipo modesto. Con cargador, se inicia en la franja de 120 px alrededor del viewport, se pausa al quedar fuera de la vista o al ocultar la pestaña y se desmonta al salir de la franja. El respaldo conserva la caja hasta que se confirma la carga. Un fallo, la pérdida de contexto WebGL o una espera de ocho segundos dejan el respaldo. El canvas preparado queda fuera de la secuencia del teclado. Solo acepta puntero cuando el cargador anuncia que está listo. El recorrido por teclado y la explicación permanecen en HTML.

Valide el recurso real con bloqueo de su petición, cambios de movimiento reducido, equipo táctil, pérdida de contexto y los cuatro estados de la escena. Mida transferencia total del runtime y export, primer cuadro, estabilidad, frecuencia de cuadros y pausa efectiva frente a la base. Los presupuestos de referencia están en la [guía interna](../../.claude/skills/recruitment-3d-experience/BUDGETS.md). La licencia, el origen y el hash de un archivo local o la revisión de un export alojado deben registrarse cuando exista el recurso.

### Validación del contrato del carrusel

En Docker pasaron las seis pruebas de sesión con cargador simulado, TypeScript, la compilación y el control de formato/lint de los cinco archivos afectados. Cypress E2E-29 pasó sus dos casos sobre ese build: recorrido de los cuatro pasos HTML, acceso al listado y respaldo con teclado a 320 px. Quedan pendientes las flechas en Preview, la equivalencia entre la selección HTML y la tarjeta renderizada, y las mediciones del carrusel exportado. El 24/11, sobre el mismo árbol, volvieron a pasar en Docker los tipos, las seis pruebas de sesión, el formato y lint de siete archivos y el build. Cypress E2E-29 pasó sus 2 casos. Los registros están en `spline-editor/` de la carpeta de evidencia.

### Copias de trabajo y validación en el editor (24/11/2026)

Los archivos de trabajo están en `storage/app/private/spline-prototipo/`, ignorado por Git. El original `carrusel-fuente-79de62c2.spline` y su respaldo `carousel_tutorial_for_community_copy.spline` (en la carpeta de descargas del equipo) tienen el mismo SHA-256: `79de62c2f570fbfb775cb3a2ec5ceac206a229dd5f19c8cbc5e42a6d61a97d68`. No se modifican.

| Copia | SHA-256 local | Archivo importado en Spline |
|---|---|---|
| `Prueba-minima-fondo.spline` (solo cambia el color de fondo) | `511b2a2adb322ef63f1e56f8d09cd84f28a64370c087a27e37ff108036e24e71` | `e5b22cde-359c-419c-9c5c-841828104998` |
| `Proceso-postulacion-Andino.spline` (borrador de cuatro tarjetas, generado por script sobre el formato interno) | `6dc7068990247546ee993be9e718e789774301d8c92cd1005ba56199f6a1178f` | `791fcb5a-2978-433f-a341-3d2abfa898e1` |

El equipo importó ambas copias y abren en el editor. Codex validó antes ambas copias solo con el runtime (`validacion-runtime.json`): flechas, límites 1–4, saltos con `applicationStep` y una tarjeta centrada. Eso no prueba que sean editables.

La conexión es el servidor MCP alojado de Spline (`https://mcp.spline.design/mcp`), registrado con alcance local y autenticado por el equipo. La cuenta conectada tiene el plan Free: 20 llamadas diarias a herramientas de escena. La validación del 24/11 usó 17. No se usaron la generación con IA, la restauración de versiones ni la publicación del export.

### Validación en el editor (24/11/2026)

- **Copia mínima** (`e5b22cde…`). Abre en el editor y se lee completa: 204 objetos en dos páginas, fondo `#bfdee3`, las siete variables de la plantilla (entre ellas `current`), 27 materiales y los eventos de las flechas, el panel y los clones. No se editó.
- **Carrusel** (`791fcb5a…`). Abre y se lee: 73 objetos y la variable `applicationStep` = 1. Los cuatro grupos tienen los estados «Paso 1» a «Paso 4» y cuatro eventos `VariableChange` con transiciones de 220 ms (`ease-out`). Las flechas tienen un evento `MouseDown`.
- **Defecto del borrador.** «Siguiente» y «Anterior» compartían el id de evento `00cfeff9…`: el script regeneró las condiciones, pero no el evento. Se rehízo el evento de «Siguiente» (`a21032cd…`) con una sola acción `SetVariable`, `min(applicationStep + 1, 4)`. «Anterior» conserva su condicional: si `applicationStep > 1`, resta uno. El MCP rechazó crear una acción dentro de la rama de un condicional con la firma que documenta (`addAction` no admite `{ parentActionId, branch }` como tercer argumento).
- **Guardado y reapertura.** Spline guarda de forma automática y dejó los puntos «Before AI edits» v5 y v9 antes de las ediciones. Tras abrir la copia mínima, el carrusel se volvió a abrir y `get_objects` devolvió los cambios: el evento nuevo, la cámara, el panel, las flechas y los textos.
- **Preview.** El MCP no puede pulsar las flechas. Además, las capturas del editor llegaron con 291 × 1280 px porque la pestaña del editor era muy estrecha, así que no sirven para juzgar el encuadre. La prueba manual en Preview queda pendiente.
- **Rendimiento según el analizador del editor.** 64 objetos, 62 328 polígonos, 6 materiales, 0 texturas, 2 luces direccionales con sombra y 0 recursos sin uso. Todas las métricas están en «good». El tamaño del export no se midió, porque requiere publicarlo.

### Refinado del carrusel (24/11/2026)

Cambios aplicados en el editor sobre `791fcb5a…` para el marco 16:10 de la sección:

| Elemento | Antes | Después |
|---|---|---|
| Cámara de reproducción `Camera` | z = 1320, fov 34 | z = 1150, fov 34. Es la cámara de Play y no tiene controles de órbita |
| Panel «Proceso de postulación» | (−0,99; 22; 0) | (0; 51; 0): tarjeta y flechas centradas en vertical |
| Flechas | y = −300; icono a escala 2,61 en «Anterior» y 1,8 en «Siguiente» | y = −235; ambos iconos a 2,3 |
| Títulos de las tarjetas | Tamaño 47 | Tamaño 38, cuadro de 646 de ancho |
| Tarjeta 3 | «Complete su perfil» · «Datos del perfil y CV en PDF» | «Complete su perfil y cargue su CV» · «Datos en Mi perfil y CV en PDF» |
| Materiales | 33 recursos, 27 sin uso, de la plantilla | Los 6 de la paleta, todos en uso |

La tarjeta activa ocupa cerca del 64 % del ancho del marco, con el mismo margen arriba y abajo. Las vecinas asoman a los lados y orientan el recorrido. No cambian la paleta (`#0B5D6C`, `#67B9BE`, `#FAFDFD`, `#C9D6D9`, `#45595D`), los iconos ni el número de objetos. No hay avance automático. El fondo de la escena sigue claro (`#EDF3F3`).

El MCP no descarga la escena. Por eso `refinar-local.cjs` aplica los mismos cambios, incluido el evento nuevo, a una copia local: `Proceso-postulacion-Andino-refinado-local.spline`, SHA-256 `db783dcd5052d0e5a682617acfe72b9b2f4d048ae9871a4ac4adad09af71d9c4`. `validar-refinado.py` la abrió en Chrome con el runtime 2.0.219 de la copia de inspección, a 960 × 600 y a 580 × 362 (la columna de la portada a 1440 px). Pasaron 13 comprobaciones: el inicio, ocho clics de flecha con los límites 1 y 4, y cuatro saltos por variable. Cada paso deja una sola tarjeta centrada y no hubo errores de página. A 580 × 362, el título mide unos 20 px y el detalle unos 14 px. Esta prueba usa el runtime con la copia local, no el export publicado.

El original y su respaldo conservan el SHA-256 `79de62c2…`, y las copias de trabajo, `511b2a2a…` y `6dc70689…`. Capturas y resultados: `spline-editor/` de la carpeta de evidencia.

Pendientes del editor:

1. Pulsar las flechas en Preview con una ventana amplia y revisar el encuadre en el editor.
2. Registrar el autor y la atribución de la plantilla de la Comunidad: el MCP no muestra la ficha del original.
3. Elegir el fondo para el tema oscuro al integrar: transparente o el actual, claro.

### Revisión de la dependencia del runtime (24/11/2026)

Consultas al registro público de npm y a GitHub sobre `@splinetool/runtime`, la librería que dibuja un export en la web:

- **Licencia.** Ninguna de sus 1231 versiones declara licencia, y el paquete 2.0.219 no incluye archivo de licencia. El repositorio que declara, `splinetool/spline`, no es público. Solo el envoltorio `@splinetool/react-spline` tiene licencia MIT, y depende de este runtime.
- **Términos de Spline.** Vigentes desde el 29/10/2026 en [spline.design/terms](https://spline.design/terms). Dicen que el software es propietario y confidencial y que no se transfiere ningún derecho sobre él. No tratan el uso del runtime ni de los exports en sitios de terceros, ni si pueden alojarse o empaquetarse.
- **Comunidad.** El contenido publicado se rige por la «Standard Commercial License», que permite remezclar y modificar para uso personal y comercial. Su texto no está enlazado en los términos.
- **Origen.** Lo publican personas de Spline. La versión 2.0.219 se publicó el 24/11/2026; de 2.0.214 a 2.0.218 salieron el día anterior. Pesa 36,5 MB desempaquetado, con 372 archivos.

Con estas condiciones desconocidas, el runtime **no se incorpora**. Hace falta una decisión expresa del equipo para aceptarlas o elegir una alternativa: un visor alojado por Spline o capturas del editor para el respaldo estático. Mientras tanto, la portada mantiene la ilustración estática y el contrato `LoadApplicationScene` queda sin cargador. En la validación del 24/11 la decisión quedó sin elegir: no se publicó el export, no se instaló el runtime y no se conectó la portada. Esa misma tarde el equipo eligió la opción A; su registro está en la sección siguiente.

## Integración del export (24/11/2026)

**Decisión del equipo: opción A.** El equipo acepta los términos de Spline para este prototipo académico local y autoriza `@splinetool/runtime` con estas condiciones:

- versión exacta;
- publicada preferiblemente al menos 14 días antes; si ninguna funciona con el export, la compatible más antigua, con su fecha y el motivo;
- origen, mantenedores, integrity, licencia, tamaño y riesgo documentados;
- sin ocultar la marca ni la atribución del export o del runtime.

La autorización amplía la experiencia 3D a WebGL solo en esta sección. No modifica ADR-003 ni cierra la pregunta 3 de `scope-preliminary.md`.

### Export

| Dato | Valor |
|---|---|
| Origen | Copia `791fcb5a-2978-433f-a341-3d2abfa898e1`, publicada con `3d_publish_export` (exportación de código, vanilla) |
| URL pública | https://prod.spline.design/o9V17OqJsPxpJn0x/scene.splinecode |
| Archivo servido | `public/spline/proceso-postulacion-eaa9e57f.splinecode`, 115 092 B (90 551 B con gzip -9) |
| SHA-256 | `eaa9e57f93c73319d24c07b872a65540bf44ad22c863be1e2a5b0d92f3df3246` |
| Formato | Esquema 136, editor 2.0.219 |

Se comprobó que es la escena refinada y no la plantilla:

- la variable `applicationStep` vale 1;
- están los grupos `convocatoria`, `cuenta`, `perfil_cv` y `seguimiento`, con cuatro estados cada uno;
- la tarjeta 3 se titula «Complete su perfil y cargue su CV»;
- «Siguiente» tiene su propio evento `a21032cd…` con `min(applicationStep + 1, 4)`;
- la cámara está en z = 1150 y el panel en y = 51.

El export incluye la fuente Inter 600 (`fonts.gstatic.com`) y la imagen `SplineWatermark`. El runtime dibuja esa imagen dentro del canvas como la insignia «Built with Spline», que se conserva.

### Versión del runtime

Se probaron versiones con el export real en una página aislada, fuera del repositorio, comprobando carga, variable, las dos flechas, los límites 1 y 4, y los saltos por variable. Script `probar-runtimes.py`, junto a las copias de trabajo.

| Versión | Publicada (UTC) | Resultado |
|---|---|---|
| 2.0.170, última publicada hasta el 10/11 | 10/11/2026 17:37 | El recorrido pasa, pero la consola da un error: «file format 136, this runtime reads 135» |
| 2.0.197 | 19/11/2026 13:05 | El mismo error de formato |
| **2.0.198, elegida** | **19/11/2026 13:30** | Recorrido completo sin errores; queda la advertencia «Your .splinecode file is more recent than the library» |
| 2.0.219, control | 24/11/2026 08:02 | Recorrido completo sin errores ni advertencias |

La búsqueda binaria entre 2.0.171 y 2.0.219 mostró que la 2.0.198 es la primera que lee el esquema 136. Ninguna versión con al menos 14 días lo lee sin error, así que se fijó la compatible más antigua, que tenía 5 días al instalarla. La advertencia es informativa y no afecta al funcionamiento: aparece porque el export declara la versión 2.0.219.

| Revisión de `@splinetool/runtime@2.0.198` | Valor |
|---|---|
| Declaración | `"@splinetool/runtime": "2.0.198"` en `dependencies`, sin `^` ni `~`, y la misma versión en `package-lock.json` |
| Integrity | `sha512-0I7H+ynKJBTopqyeipFYIo+5TOh2OCUsi5PL3+tcN8CJ+KJRKTXzsjox6QfbHfrl/EBlhJPY1ePE+iisa6KEFA==` (shasum `f5a3ba4b8b4e633069f873dcdca1722ca2952d45`) |
| Origen | Registro público de npm; tarball `https://registry.npmjs.org/@splinetool/runtime/-/runtime-2.0.198.tgz` |
| Mantenedores | Tres cuentas con dominio `spline.design` |
| Repositorio declarado | `github.com/splinetool/spline`, no público |
| Licencia | No declarada en npm ni en el paquete. Los términos de Spline (spline.design/terms, vigentes desde el 29/10/2026) lo declaran software propietario |
| Tamaño | 36 405 429 B desempaquetado, 372 archivos, tarball de 19 044 517 B |
| Dependencias | `on-change` 4.0.0 y `semver-compare` 1.0.0, ambas MIT |
| Auditoría | `npm audit --omit=dev` no atribuye avisos a estos paquetes. Los cuatro existentes vienen de `concurrently`/`shell-quote`, `source-map-js` y `vite`/`launch-editor` |

Riesgos:

- **Licencia.** No hay licencia abierta: el uso queda bajo los términos que el equipo aceptó, solo para este prototipo académico local.
- **Ritmo de publicación.** El paquete publica casi a diario: 1231 versiones, y 2.0.214 a 2.0.219 en dos días. Sustituir el export puede exigir una versión más nueva; cada cambio se vuelve a probar con `probar-runtimes.py` y se fija con versión exacta.
- **Petición externa.** La fuente del texto se pide a `fonts.gstatic.com`, porque su URL viene dentro del export. Servirla desde el proyecto exigiría alterar el export.

### Adaptador

`application-scene-loader.ts` es el cargador estable que recibe la portada. Importa bajo demanda `spline-application-scene.ts`, que a su vez carga el runtime con `import()` dentro del fragmento diferido. El contrato `LoadApplicationScene` no cambia. El adaptador:

- crea `Application` con `renderer: 'webgl'`, `renderMode: 'auto'` y `htmlContentMode: 'none'`, y fija `wasmPath` en `/build/spline-runtime`;
- carga el export propio con `applicationStep: 1` y la señal de cancelación, y resuelve con el evento `rendered` del primer cuadro;
- `setStep` llama a `setVariable('applicationStep', paso)`;
- al pulsar «Siguiente» o «Anterior» lee la variable en el cuadro siguiente y la entrega a `onStepChange`; la sesión descarta duplicados, valores inválidos y eventos fuera de reproducción;
- `setPlaying` llama a `play()` o `stop()`;
- `dispose` llama a `app.dispose()`, que libera el contexto WebGL, y se ejecuta al abortar o al desmontar;
- ante un fallo de decodificación o de inicialización, libera el runtime y rechaza la promesa.

La sesión ya cubre la espera de 8 s y la pérdida de contexto: en ambos casos deja el respaldo estático.

El plugin `spline-runtime-wasm` de `vite.config.ts` copia `bevel.wasm`, el único WASM que pide esta escena, de `node_modules` a `public/build/spline-runtime/` en cada build. Así no se versiona y no se pide a unpkg. En `vite dev` se usa el CDN del paquete.

**Fondo.** Es transparente (`setBackgroundColor('transparent')`): se ve el fondo de la sección en ambos temas. Las tarjetas llevan su propio fondo claro, así que el texto conserva el contraste. Se comprobó en claro y en oscuro.

**Seguridad funcional.** Seleccionar un paso solo cambia la variable de la escena y la explicación HTML. No registra postulaciones ni ejecuta acciones de negocio.

### Validación en el navegador (http://localhost:8087/)

Build real y Chrome sin interfaz, con un contexto nuevo por caso. GPU NVIDIA RTX 4060 con ANGLE/D3D11, que es de gama alta: los FPS no representan un escritorio de gama media. Script `validar-integracion.py`; resultados en `integracion/integracion.json` y capturas en `integracion/capturas/` de la carpeta de evidencia.

| Caso | Resultado |
|---|---|
| Escritorio 1440 × 900, claro y oscuro | Escena lista en la sección. Los cuatro pasos HTML mueven la tarjeta activa. Las flechas cambian la selección y la explicación HTML: 2, 3, 4, 4 en el límite, 3, 2, 1, 1 en el límite. CLS 0 |
| Teclado y foco | Los pasos reciben foco visible y se seleccionan con Espacio. El tabulador nunca llega al canvas (`tabIndex = -1`) |
| Desplazamiento | La rueda sobre el canvas desplaza la página |
| Pausa | Con la pestaña oculta o fuera de la vista, 0 cuadros, incluso si el paso cambia. Al volver dibuja el paso vigente |
| Salida de la sección | Al alejarse se desmonta el canvas y se libera el runtime. Al volver se recrea con el paso vigente |
| Móvil 390 × 844 y 320 × 740, táctil | Respaldo estático sincronizado, sin canvas, sin peticiones de Spline, desborde 0, CLS 0 |
| Movimiento reducido al cargar | Respaldo, sin peticiones de Spline |
| Movimiento reducido con la página abierta | El canvas se desmonta y el respaldo conserva el paso 3. Ver la observación sobre el CLS |
| Export bloqueado, fragmento del adaptador bloqueado, pérdida de contexto WebGL | Respaldo visible, sin canvas, la altura de la ilustración no cambia (335,75 px), CLS 0, sin errores de página |
| Insignia «Built with Spline» | Dibujada dentro del canvas; la ilustración no añade elementos al DOM |

### Mediciones

Mismas condiciones que la base documentada (`medir.py`). Bytes transferidos según Resource Timing, solo locales y sin compresión, porque el servidor local no comprime:

| Caso | Peticiones locales base → integración | Bytes base → integración | JS base → integración |
|---|---:|---:|---:|
| Escritorio, claro u oscuro, al cargar | 42 → 44 | 2 148 232 → 2 153 860 | 640 540 → 645 666 |
| Escritorio, en la sección | 42 → 96 | 2 148 232 → 4 430 798 | 640 540 → 2 683 348 |
| Móvil o movimiento reducido, al cargar y en la sección | 41 → 43 | 1 033 246 → 1 038 874 | 640 540 → 645 666 |

- Las dos peticiones nuevas de la carga inicial (+5,6 kB) eran el fragmento de control diferido, que se pedía al tener cargador. Desde la integración en main, `ApplicationProcessScene` decide la capacidad antes de montarlo. Así, en móvil, con movimiento reducido o en equipos modestos ya no se pide ni se monta; las cifras de esta tabla son anteriores a ese ajuste. El cambio también eliminó un fallo intermitente de E2E-23 a 390 px (error 177 de React durante la captura de Cypress), que solo apareció con el fragmento montado en móvil.
- La escena solo se pide en escritorio capaz, al acercarse a la sección:
  - runtime: 49 fragmentos JS, 2 019 362 B sin comprimir, 547 609 B con gzip -9;
  - WASM: 123 717 B;
  - export: 115 213 B;
  - fuente externa de `fonts.gstatic.com`: 162 619 B.

| Presupuesto (BUDGETS.md) | Medido | Estado |
|---|---|---|
| Aumento del *bundle* inicial: 0 KB | Entrada `app` +0,16 kB: el mapa de precarga gana una referencia al fragmento compartido `rolldown-runtime`. Página `welcome` +0,86 kB. Ni el runtime, ni el adaptador ni el WASM están en la entrada | Desviación menor |
| Primer cuadro ≤ 1,5 s tras entrar en la vista | 793–828 ms en claro; 338 ms en oscuro | Cumple |
| ≥ 45 FPS | 59,9–60,2 FPS en transiciones (intervalo mediano 16,7 ms, p95 17,2 ms), en una GPU de gama alta | Cumple en este equipo |
| Pausado fuera de la vista | 0 cuadros fuera de la vista y con la pestaña oculta | Cumple |
| Triángulos ≤ 100 000 | 62 328 polígonos según el analizador del editor | Cumple |
| Texturas | 0 en la escena | Cumple |
| Llamadas de dibujo ≤ 60 | 99 por cuadro en reposo (paso 1); 132 de mediana y 144 de máximo durante las transiciones. Sin sombra y con profundidad 0 sigue en 99: el coste viene de las 52 mallas | **No cumple** |
| Memoria GPU ≤ 150 MB | No medida: no hay API fiable en el navegador | Pendiente |
| CLS | 0 en escritorio, móvil y fallos | Cumple |

Observaciones:

- **Dibujo en reposo.** Con `renderMode: 'auto'`, el runtime dibuja unos 60 cuadros por segundo mientras la escena está visible, aunque no cambie nada; la pausa fuera de la vista sí es completa. El modo `manual` daría 0 cuadros en reposo, pero hay que pedir cuadros en cada transición: sin ellos la imagen queda a mitad de camino, y no se redibuja al llegar la fuente ni al cambiar el tamaño. Se mantuvo `auto` por robustez.
- **CLS con movimiento reducido en vivo.** Al activar el movimiento reducido con la página abierta, el CLS es 0,3528. Es idéntico con la escena bloqueada: lo producen el hero y el bloque del proceso al recomponerse, no esta integración.
- **Consola.** Solo queda la advertencia de versión del export. Con un recurso bloqueado aparece además el error de red del navegador.

### Pruebas

- **Adaptador.** `spline-application-scene.test.ts` (siete casos, runtime simulado): opciones de carga, primer cuadro, paso y reproducción, notificación solo desde las flechas, liberación al desmontar, cancelación durante la carga, export dañado y carga ya cancelada.
- **Componentes.** Pasan las 35 pruebas de `experience-3d`, incluidas las seis de sesión. Tipos, formato y lint de los seis archivos tocados y el build también pasan.
- **E2E-29**, ampliada a tres casos. El nuevo comprueba que la escena se pide solo cerca de la sección y que, si falla el export, queda el respaldo sincronizado.
- **E2E-27** pasó sus 11 casos contra el entorno E2E aislado del prototipo (`APP_ENV=e2e`), que se reinicia con datos demo.
- **E2E-23** pasó 12 de 13 en la primera ejecución. Falló «a 390 px: imagen fija…» con «Minified React error #177» durante `cy.screenshot`, a un ancho donde la escena no se monta. Dos repeticiones pasaron 13 de 13. Queda registrado como intermitente, sin relación demostrada con la integración; los registros están en `integracion/`.
- **PHPUnit** no se repitió: no hay cambios de backend.

### Pendientes

1. **Llamadas de dibujo por encima del techo** (99–144 frente a 60). Reducirlas exige rediseñar la escena con menos mallas, por ejemplo tarjetas como planos con textura. Requiere decisión del equipo y cuota de Spline.
2. **Atribución de la plantilla «Carousel Tutorial for Community»:** autor y licencia sin verificar. El 24/11 no se encontró en el archivo original, que no guarda metadatos de autor, ni en una búsqueda web de la comunidad de Spline. No se registra hasta poder comprobarla en la ficha original.
3. **Flechas en el Preview del editor**, si el equipo quiere esa prueba además de la del navegador.
4. **Fuente externa:** decidir si se acepta la petición a `fonts.gstatic.com` o se altera el export para servir Inter desde el proyecto.
5. **Memoria GPU** sin medir, y **FPS en un equipo de gama media** sin comprobar.
6. **Renderizado continuo** mientras la escena está visible, en el modo `auto` del runtime.
7. **Alcance de los términos:** la opción A se aceptó para el prototipo académico local. Publicarlo en el VPS amplía ese uso.
8. **Registro formal:** ADR-003 recoge la ampliación desde el 24/11. Siguen abiertas la pregunta 3 de `scope-preliminary.md` y la promoción de RNF-C.

## Comparación histórica del prototipo estático en Chrome

Dos builds del mismo worktree y servidor Docker en `http://localhost:8087/`, primero con la base sin modificar y después con la interfaz preparada. Chrome sin interfaz, con contexto nuevo por caso, sin limitación artificial de red, 1440 × 900 para escritorio y 320 × 740 para móvil táctil emulado. Se contó la navegación y los recursos locales mediante Resource Timing. Los valores incluyen encabezados HTTP.

| Caso | Solicitudes locales antes → después | Bytes transferidos antes → después | JS transferido antes → después |
|---|---:|---:|---:|
| Escritorio, claro u oscuro | 40 → 42 | 2 142 250 → 2 148 232 | 636 203 → 640 540 |
| Móvil o escritorio con movimiento reducido | 39 → 41 | 1 027 264 → 1 033 246 | 636 203 → 640 540 |

La preparación incorpora 5982 B al total local y 4337 B al JS medido. Acercarse a «Cómo postular» no generó tráfico adicional en ninguno de los casos. El vídeo del hero transfirió 1 114 986 B en escritorio y 0 B en móvil y con movimiento reducido, tanto en la base como después. Se observaron cero desplazamientos de layout sin entrada y cero píxeles de desborde. La altura de la sección se mantuvo al recorrer los cuatro pasos. El fragmento de control de escena de 2750 B queda separado y la portada lo omite mientras falta el cargador. La espera de dos cuadros de `requestAnimationFrame` tras cada clic fue de 18 a 23 ms en esta muestra de 16 interacciones. Esta medida describe la interfaz HTML y no representa FPS ni tiempo de render de Spline.

Las cinco pruebas de sesión verifican sincronización al resolver, pausa, rechazo, expiración, desmontaje y pérdida de contexto con un adaptador simulado. E2E-29 cubre navegación, controles HTML, cuatro selecciones, teclado y respaldo a 320 px. Chrome confirmó el foco visible y la selección al cambiar la preferencia de movimiento con la página abierta. Faltan el primer cuadro, las medidas de GPU y la sincronización con un export real.

En Docker, la repetición de PHPUnit con caché y sesión de prueba en memoria terminó con 626 aprobadas, 8 omitidas por la verificación de correo y 4079 aserciones. Tipos, build, 122 pruebas de componentes y formato/lint pasaron. Cypress pasó E2E-29 (2/2) sobre el build final. Antes de diferir el adaptador pasaron E2E-28 (3/3), E2E-27 (11/11) y E2E-23 (13/13). El respaldo se volvió a verificar con Chrome tras diferirlo.

Evidencia local en `D:/bt/proceso-postulacion-evidencia/`. Las carpetas `antes/` y `despues/` contienen las capturas. `antes.json` y `despues.json` contienen las mediciones originales. Los logs de build, TypeScript, componentes, lint y Cypress están en la misma carpeta.
