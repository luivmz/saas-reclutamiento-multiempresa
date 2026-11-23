# Incremento visual de la presentación: carpeta en vídeo y carpeta del proceso

> **Rama `design/presentacion-higgsfield`, 22/11/2026**, desde `main` = `04d3cfa1db6f82d9cda8db2254338805137cdc3c`, la base de presentación de [`README.md`](README.md).
>
> - **Estado:** candidato a auditoría independiente. La aprobación de `bb86991` no lo cubre, y no se integra en `main` sin un dictamen aplicable a este candidato.
> - **Alcance:** solo cambia la portada pública (presentación, CSS y pruebas). No cambian el backend, las rutas, los permisos, el ranking, la decisión humana (RF-23), ML-01 ni ML-02.
> - **Estados formales:** ninguno cambia.

## 1. Qué cambia

| Parte | Antes (`main`) | Ahora |
|---|---|---|
| Portada, columna derecha | Expediente ilustrativo REQ-2026-0042 con tres hojas en profundidad (CSS 3D) | Vídeo decorativo de una carpeta que se abre al bajar y se cierra al subir (Higgsfield). No se reproduce: el desplazamiento elige el fotograma |
| «Cómo avanza un proceso» | Cuatro pasos en una fila | Los cuatro pasos y, al lado, **la carpeta del proceso**: el mismo expediente con sus tres hojas. Las hojas se separan en profundidad al bajar y se apilan al subir. El cursor las desplaza aparte (paralaje) |
| VIS-L01 | Al activar el movimiento reducido con la página abierta, los bloques pendientes seguían ocultos y desplazados | Aparecen en su sitio en ese momento y no vuelven a ocultarse (§4) |
| DEF-19 | `Reveal`, la capa de profundidad y la escena leían solo la primera entrada de cada aviso de IntersectionObserver | Leen todas: un bloque ya no queda oculto si el aviso «fuera» y el «dentro» llegan juntos (§5) |

## 2. El recurso de Higgsfield

### 2.1 El original

El original es `playground-result-1795371181623.mp4`, de la carpeta Descargas de la PC principal. **Se conserva sin cambios fuera de Git**: el repositorio solo lleva la copia web. Se inspeccionó con el `ffmpeg` estático que trae la imagen `cypress/included:15.3.0`, sin dependencias nuevas, sin API, sin credenciales y sin consumir créditos.

| Dato | Valor |
|---|---|
| Tamaño y SHA-256 | 1 692 658 bytes · `7ec3b362d5179a2cbc94fcc5fa707b4dd0414e3d60b1652d8b3c8fe236907fa2` |
| Duración | 5,18 s (124 fotogramas) |
| Vídeo | 1344 × 768 · H.264 Constrained Baseline · yuv420p · 24 fps · unos 2,5 Mb/s. **Un solo fotograma clave**, el primero: buscar hacia atrás obliga a decodificar desde el inicio |
| Audio | AAC LC, 32 kHz, estéreo, 110 kb/s. **No es silencio** (volumen medio de −46,8 dB y pico de −5,5 dB) |
| Metadatos | Etiqueta AIGC con `ContentProducer: MiniMax`: contenido generado por IA |
| Contenido | Carpeta petróleo con solapa ámbar y hojas crema con líneas ilegibles, sobre fondo petróleo oscuro. Sin texto legible, personas, rostros, logotipos ni marcas de agua (fotogramas del inicio, 1,3 s, mitad, 3,9 s y final, más una hoja de contactos cada 8 fotogramas) |
| Movimiento | Las hojas se elevan y separan hasta los fotogramas 48–52 (2,0–2,2 s) y vuelven a apilarse hacia el final. **No es un bucle perfecto**: el último fotograma no coincide con el primero (la hoja superior queda unos 7 px más baja) |

### 2.2 La copia web (`public/media/portada/`)

| Archivo | Qué es | Tamaño · SHA-256 |
|---|---|---|
| `portada-carpeta.mp4` | Fotogramas 0 a 50 (la apertura, 2,125 s). 1344 × 768, H.264 High, **todos intra** para buscar rápido, CRF 27, sin audio ni metadatos, `faststart`. SSIM frente al original: 0,991 | 699 001 bytes · `438dbe4bd00db5dd43d7e80098cab76e61738ea0cbf83176be37602ab4a8a9d0` |
| `portada-carpeta-poster.webp` | Fotograma 0, la carpeta cerrada: el póster del vídeo | 18 636 bytes · `84e5a8cb3cf8d35244bea32283f3a565fec2566683f2314a896e2654d6e243f6` |
| `portada-carpeta-abierta.webp` | Fotograma 50, la carpeta abierta: la imagen fija | 20 446 bytes · `dd252c4d4d1267afbb8501d1fe8dd4a6f84f445a5b0386461c5f4581fd590c37` |

**Por qué solo la apertura.** Con el clip entero, bajar abriría y cerraría la carpeta. Con la apertura, bajar la abre y subir la cierra, sin presuponer un bucle que el original no tiene.

### 2.3 Cómo se usa (`HeroFolderVideo`)

- **Decorativo.** `aria-hidden`, `inert`, sin controles ni foco. Todo lo que dice la portada está en el texto de al lado.
- **Desplazamiento.** El desplazamiento de la página elige el fotograma: el 0 arriba del todo y el 50 tras recorrer el 60 % de la altura de la portada. **Nunca se llama a `play()`**. El desplazamiento es el del navegador, sin captura ni suavizado.
- **Búsquedas.** No se busca antes de tener metadatos. Mientras el vídeo busca, la siguiente posición espera y solo se aplica la última (`createFrameSeeker`). A lo sumo hay una actualización por cuadro.
- **Descarga.** Solo en escritorio de 1024 px o más, sin movimiento reducido, sin ahorro de datos y en un equipo no modesto: la misma regla que la escena de ADR-003. Se sirve desde memoria (blob), porque `php artisan serve` no atiende peticiones `Range` y Chrome no busca en un recurso así: medido en Chrome, el fotograma mostrado se quedaba en 0.
- **Respaldos.**
  - En los demás casos, o si falla la descarga o la decodificación: la imagen fija.
  - Si también falla la imagen: el fondo CSS del panel (`.hero-folder`).
  - Antes de decidir no se pide nada.
- **Movimiento reducido con la página abierta.** El vídeo cede a la imagen fija y se retiran las escuchas.
- **Temas.** El panel es igual en los dos, como una fotografía enmarcada. El texto de la portada no se apoya en él.

## 3. Dónde va la carpeta

Se conservan el expediente (tarjeta), las tres hojas y su composición. Opciones comparadas:

| Opción | Utilidad | Coherencia | Legibilidad y rendimiento | Esfuerzo y reglas |
|---|---|---|---|---|
| A. Detalle público de oferta `/empleos/{id}` | Explicaría el proceso de cada oferta, pero exigiría construir un expediente con datos propios de cada una, sin copiar REQ-2026-0042 ni decisiones firmadas | La página tiene un trabajo: leer requisitos y postular. La carpeta competiría con «Postular a esta vacante» | Una escena más por oferta | **La skill `recruitment-3d-experience` no la permite**: solo autoriza la portada, la presentación del portal y, como mucho, la cabecera del listado, y prohíbe los formularios de postulación |
| **B. «Cómo avanza un proceso», en la portada** (elegida) | Pone en imagen las etapas que la sección explica en texto: vacante, evidencias y decisión humana | El expediente ya es un «ejemplo ilustrativo» de la portada y sigue diciéndolo | Una sola escena CSS, cargada al verse; los pasos siguen siendo HTML | Mínimo: la misma escena, movida dentro de la portada. **Sigue siendo una sola superficie CSS 3D** (ADR-003) |
| C. Otra ubicación (listado, panel interno) | El listado no tiene un expediente que contar; las pantallas internas tienen el 3D prohibido | — | — | Prohibido o sin contenido |

La carpeta queda en **B**. El vídeo de la portada y la carpeta del proceso no se duplican: arriba, la carpeta es una imagen sin texto; abajo, lleva el contenido del expediente y las etapas.

**En móvil, con movimiento reducido y en los demás casos del póster**, la carpeta es estática y legible: el expediente con las hojas apiladas detrás.

## 4. VIS-L01

Es el hallazgo LOW de Codex sobre `bb86991`.

- **Causa.** `Reveal` decidía una sola vez, al montar, si un bloque de abajo esperaba oculto (opacidad 0, 16 px más abajo). Si después se activaba el movimiento reducido, esos bloques seguían esperando un desplazamiento.
- **Corrección.** `watchReveal` también escucha la preferencia. Al pasar a «reducir», lo pendiente pasa a estático en su sitio. Cada bloque cambia de estado una sola vez: al asentarse se desconecta el observador y se retira la escucha, así que nada posterior lo vuelve a ocultar. `app.css` muestra además los bloques pendientes con movimiento reducido, aunque el script aún no haya reaccionado.
- **Regresión con la página montada.** E2E-22 lee la apariencia real con `getComputedStyle` (opacidad 1, sin transform), no solo atributos internos:
  - justo después de activar la preferencia, sin desplazarse;
  - después de recorrer la página, desactivarla y volver a recorrerla.

| Ejecución | Resultado |
|---|---|
| RED: `Reveal` y CSS de `main` | Falla: «opacidad: expected '0' to equal '1'» |
| Ablación: solo la defensa CSS, con el JS de `main` | Falla en la línea 244: los bloques siguen en estado oculto y vuelven al desactivar la preferencia |
| GREEN | 8/8 en E2E-22 |
| Unitarias de `watchReveal` | Oculto y observado debajo del borde; estático y sin escuchas al activarse; una sola entrada; nada observado al montar con movimiento reducido o ya visible; limpieza al desmontar |

**Corrección de la propia prueba.** La primera versión llamaba a `reducido(true)` y `reducido(false)` dentro de un `.then`, fuera de la cola de Cypress, así que la preferencia se activaba y se desactivaba antes de las aserciones. Sus dos ejecuciones (RED y ablación) se conservan como inválidas. La prueba vigente encola los cambios con `cy.then`, y E2E-23 se corrigió igual.

## 5. DEF-19

**Dónde se vio.** Al mover la carpeta debajo de la portada, las pruebas pasaron a desplazarse justo después de cargar. La escena dejó de montarse a veces:

- 1 de 3 ejecuciones de E2E-22, y la ejecución RED;
- 1 de 16 iteraciones de una spec de diagnóstico temporal, que no se versiona.

Siempre con los pasos de la izquierda todavía ocultos.

**Causa.** Un aviso de IntersectionObserver trae todas las entradas acumuladas desde el anterior. `Reveal`, `useSeenOnce` y la escena usaban `([entry]) =>`: si el aviso inicial («fuera») y el siguiente («dentro») llegaban juntos, se quedaban con «fuera» y no recibían otro aviso. El defecto ya estaba en `bb86991`. Fuera de las pruebas es alcanzable con una recarga que restaura el desplazamiento o con alguien que baja de inmediato.

**Corrección.** `lib/intersection.ts`:

- `someIntersecting`, para «la primera vez que se ve»: lo usan `Reveal` y `useSeenOnce`;
- `latestIntersecting`, para «¿se ve ahora?»: lo usa la escena, que enciende y apaga sus escuchas.

**Pruebas.**

- **RED:** la prueba unitaria del lote `[fuera, dentro]` falla con el `watchReveal` anterior (se quedaba oculto).
- **GREEN:** 83 pruebas de componente. E2E-22 pasó **5 de 5** ejecuciones seguidas (40/40) y, en la verificación final, 8/8.

Registrado en [`defects.md`](../defects.md).

## 6. Pruebas, atribuidas a `446b8fe5efdd697f6c3d7d593f2411bac9585f18`

Es el último commit de código. El commit de documentación que le sigue no cambia el código. Todo se ejecutó en la PC principal, en el proyecto Docker `experimental` (8030), en serie.

| Prueba | Resultado |
|---|---|
| `git diff --check` frente a `main` | Sin errores. Solo cambian `resources/js`, `resources/css`, `cypress/e2e` y `public/media` |
| Tipos · componentes | 0 errores · **83 passed** (11 archivos) |
| `vp check` de los 13 archivos cambiados | Sin errores de formato ni de lint |
| Build | Correcto. `app.js` inicial sin cambios (204,92 kB). Por fragmento, en gzip: portada +1,39 kB, CSS +0,16 kB y escena +0,19 kB. El vídeo (699 kB) solo se descarga en modo vídeo |
| PHPUnit | No se repite: el backend es idéntico al de `main`, verificado sobre el código de `bb86991` (525 passed, 8 skipped; [`README.md` §6.1](README.md#61-resultados-en-la-pc-principal-22112026)) |
| Cypress E2E-17 a E2E-23, una spec por contenedor | **7 de 7 specs, 63/63** a la primera: E2E-17 8/8, E2E-18 8/8, E2E-19 7/7, E2E-20 12/12, E2E-21 10/10, E2E-22 8/8 y E2E-23 10/10 |
| Funcional con la bandera encendida (8030) | 14/14: evidencias, BM25 (aciertos y abstención), proceso cerrado, roles y aislamiento siguen igual |
| Fluidez en Chrome 157 (headless, GPU) | En los dos temas, 16 pasos de rueda de 80 px, bajando y subiendo: **el fotograma mostrado coincide con el pedido en los 16**. Las 12 búsquedas del desplazamiento tardan de 1,7 a 13,3 ms; la inicial al fotograma 0, al cargar, unos 230 ms. **Ninguna búsqueda solapada ni reproducción.** Cuadros: mediana de 16,7 ms, con uno solo por encima de 33 ms |

**Cobertura de E2E-23.**

- Avance al bajar y retroceso al subir, con capturas.
- Ninguna llamada a `play()` ni búsqueda solapada.
- Vídeo que no llega (404).
- Movimiento reducido al cargar y con la página abierta.
- 390 y 320 px.
- Tema claro y oscuro.
- La carpeta del proceso, que se abre y se cierra, con paralaje a apertura fija.
- Sin desplazamiento horizontal a 1280 px.

**Cambios en las specs existentes.** E2E-18 y E2E-22 se desplazan hasta la carpeta antes de comprobar la escena, que ya no está en la portada. Sus aserciones y `data-cy` no cambian. E2E-22 suma la regresión de VIS-L01.

**No se comprobó:**

- lector de pantalla real;
- Safari y Firefox;
- dispositivos móviles físicos;
- una pantalla con ventana: la fluidez se midió en modo headless, con GPU.

## 7. Evidencias fuera de Git

En `D:\bt\pres\` de la PC principal:

- `visual/final/`: logs de esta verificación, capturas de Cypress, capturas y datos de fluidez, y manifiesto SHA-256;
- `visual/` y `visual/def19/`: el RED y la ablación de VIS-L01, las ejecuciones repetidas y el RED y GREEN de DEF-19;
- `diag/`: la spec de diagnóstico y sus datos;
- `D:\bt\higgs\`: la copia del original, los fotogramas inspeccionados y las codificaciones probadas.

## 8. Pendiente y alcance para la auditoría

- **Dictamen independiente** sobre este candidato. Sin él no se integra en `main`.
- **ADR-003.**
  - La escena CSS 3D sigue siendo una sola superficie dentro de la portada.
  - **El vídeo es una capa decorativa nueva en la portada.** No es 3D ni WebGL ni añade dependencias, y cae al póster en los mismos casos que la escena. Si cuenta como ampliación, la decide el equipo.
- **Origen del vídeo.** Lleva la etiqueta AIGC del generador. Los términos de uso del contenido generado no se revisaron aquí, y no se emite opinión jurídica.
- **VIS-L01 y DEF-19:** comprobar las correcciones y que sus pruebas fallan sin ellas.
- **Fuera del alcance:** el backend, ML-01, ML-02 y la base de datos. No hay migraciones nuevas.

## 9. Volver a servir `main` sin perder datos

La base de datos, `.env`, `.env.e2e` y `storage/` del proyecto `experimental` no dependen de la rama, y esta rama no añade migraciones. En el worktree que monta el contenedor:

```powershell
git switch main
docker compose -p experimental exec app npm run build
```

Para volver al incremento: `git switch design/presentacion-higgsfield` y el mismo `npm run build`. Ni `migrate:fresh` ni `down -v`.
