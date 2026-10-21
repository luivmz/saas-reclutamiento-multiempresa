# Revision de los seis hallazgos de V1

Fecha: 20/10/2026. Rama local: `codex/mejoras-sonarqube`.

Esta revision conserva el orden del PDF de capturas aportado por el usuario.
El analisis V1 corresponde al codigo del commit `fb1bfcb36dd853ebae37c7c1b8e332fc4b45adf8`.
Las lineas de esta tabla son las de V1; pueden desplazarse con los comentarios y cambios.
No se ha ejecutado V2 ni cambiado el estado de ningun issue en SonarQube.
No se han publicado estos cambios en GitHub ni modificado `main` o `develop`.

## Evidencia inicial

V1 finalizo correctamente y analizo 25 130 lineas de codigo propio.
Cobertura global: 57,1 %; duplicacion: 0,6 %; seis issues distintos.
En modo MQR: seguridad C (2 impactos), fiabilidad C (4) y mantenibilidad A (1).
Un mismo issue afecta a mas de una categoria; no son siete issues.
Complejidad cognitiva agregada: 1034; deuda tecnica del indicador `sqale_index`: 30 minutos.

Quality Gate: OK. Su condicion exportada es `new_violations = 0` sobre codigo nuevo;
ese resultado no significa que el codigo global no tenga problemas o alcance 80 % de cobertura.
PHPUnit aporta cobertura PHP, no cobertura React ni Python. No se cambiaron las exclusiones.
La advertencia de version de Python queda registrada; no se cambia el alcance/configuracion
del analisis entre V1 y la futura V2 para mejorar artificialmente las metricas.

Los JSON, Clover, JUnit, log y manifiesto V1 se conservan localmente en la carpeta
ignorada `.quality/evidencias/V1-20261020-192649737/`. La exportacion inicial se interrumpio
al consultar hotspots con `projectKey`; se recuperaron los datos del mismo analisis usando
el parametro `project`, sin ejecutar otro scanner. `.quality/baseline.json` identifica V1.
No publicar `.quality/`: contiene configuracion y credenciales locales.

## 1. Limite del CV - php:S5693

- V1: `app/Http/Requests/Candidates/CandidateCvRequest.php:20`.
- Revision: la regla ya exige un archivo PDF y un limite configurable. El valor predeterminado
  de `config/recruitment.php` y `.env.example` es 5120 KB. La imagen PHP establece
  `upload_max_filesize=6M` y `post_max_size=8M`. El CV se almacena de forma privada.
- Decision: conservar el control; no sustituirlo por una carga sin limite ni quitar la regla.
  La alerta solicita revision y no demuestra por si sola una vulnerabilidad.
- Evidencia: `CandidateProfileTest::test_rf09_cv_rejects_invalid_type_and_oversized_files`
  ya cubre tipo invalido y exceso; se agrega
  `test_rf09_cv_accepts_the_size_limit_and_rejects_one_kilobyte_more`, que acepta 5120 KB,
  rechaza 5121 KB y verifica que el rechazo no crea otro documento.
- Pendiente manual: documentar esta revision en SonarQube y clasificar la alerta segun el
  alcance probado. Verificar los limites efectivos si se cambia la configuracion de despliegue.
  Esta revision no certifica todas las medidas de seguridad de los PDF.

## 2. Numero aleatorio decorativo - typescript:S2245

- V1: `resources/js/components/ui/sidebar.tsx:624`.
- Revision: `Math.random()` solo variaba entre 50 % y 89 % el ancho de un skeleton.
  No generaba identificadores, tokens ni decisiones de seguridad.
- Cambio: ancho fijo del 70 %, dentro del intervalo anterior; se elimina la generacion
  aleatoria y el estado usado exclusivamente para ese estilo. El resto del componente
  y la animacion de carga existente se conservan. El ancho es estable tambien en SSR.
- Verificacion: compilacion, TypeScript y suite de componentes. No se agrega una prueba
  que simplemente copie el valor del estilo: el cambio es visual y de bajo impacto.

## 3. Denominador del calculo SMD - python:S1244

- V1: `ml-service/src/recruitment_ml/synthetic/generator.py:319`.
- Revision: `pooled` es la raiz de la media de dos varianzas, por lo que no es negativo
  para entradas validas. La comparacion con cero evita dividir entre cero.
- Cambio: se comprueba `pooled <= 0.0` para la rama sin division. No se introduce una
  tolerancia ni se redondean a cero varianzas positivas pequenas.
- Evidencia: los nuevos casos de `tests/test_sonar_regressions.py` fijan la politica
  existente para varianza cero y grupos constantes, y conservan SMD = -2 para un
  ejemplo con varianzas positivas muy pequenas. No se cambia la politica cientifica,
  las features, el dataset, el modelo entrenado ni su umbral congelado.

## 4. Busqueda de decimales - python:S8786

- V1: `ml-service/src/recruitment_ml/training/freeze.py:241`.
- Revision: `search()` con el patron anterior reintentaba cada sufijo de una secuencia
  larga de digitos sin punto. La alerta de rendimiento es reproducible.
- Cambio: `(?<!\d)[+-]?\d+\.\d+` permite comenzar solo al inicio de una secuencia de
  digitos, evitando esos reintentos. Se mantiene el requisito de encontrar un decimal
  dentro de la lectura de ablation, sin hacer mas permisivo el gate del freeze.
- Evidencia: validacion publica de lecturas con signo, Unicode, enteros, texto sin cifras,
  notacion cientifica y cadenas largas. Una comparacion adicional de 55 987 cadenas
  sinteticas cortas dio las mismas decisiones de presencia de decimal en ambos patrones.
  Es una comprobacion finita, no una demostracion para todas las entradas.
- Microcomprobacion local con 16 000 digitos sin punto: patron anterior 0,497267 s;
  patron nuevo 0,000299 s. Son mediciones de esta PC para ese caso, no una garantia
  de rendimiento productivo ni un umbral temporal impuesto a los tests.

## 5. Semantica de celda - typescript:S6843

- V1: `resources/js/components/data-table.tsx:149`.
- Revision: el elemento es un `td` dentro de `table role="table"`, no un control
  interactivo ni una celda de un grid interactivo. El layout movil usa flex/block;
  los roles explicitos son intencionados para preservar su semantica.
- Decision: conservar `role="cell"`, los encabezados, `headers` y el contenido de las
  acciones. No sustituir por `gridcell`, borrar roles ni reescribir la tabla para
  satisfacer una clasificacion estatica que no representa este contexto.
- Evidencia: la suite existente `data-table.test.tsx` comprueba los roles y la
  correspondencia de celdas y encabezados. La especificacion permite `cell` en este
  contexto, aunque normalmente sea redundante: [ARIA in HTML](https://www.w3.org/TR/html-aria/).
- Pendiente manual: propuesta de falso positivo fundamentado en SonarQube. La revision
  de codigo y markup no sustituye una prueba con lectores de pantalla reales ni
  certifica conformidad WCAG completa.

## 6. Error en consulta de riesgo operacional - typescript:S6671

- V1: `resources/js/components/vacancies/operational-risk-card.tsx:56`.
- Cambio: ante HTTP no satisfactorio se rechaza con ``new Error(`HTTP ${response.status}`)``
  en lugar del numero suelto. El error no incluye cuerpos de respuesta, tokens ni PII.
- Se conserva el `catch`, el aviso al usuario, la proteccion al desmontar y la consulta
  existente. No se alteran autorizaciones, RF-23 humano ni RF-29 experimental/informativo.
- Verificacion: compilacion, TypeScript y suite de componentes. No se afirma que haya
  una nueva prueba del ciclo de vida HTTP del componente.

## Verificacion local

Los 13 casos nuevos de caracterizacion Python pasaron antes de las refactorizaciones.
No se presenta un RED inventado: son refactorizaciones que deben conservar resultados.
Regresion posterior: PHPUnit 420 casos (412 aprobados y 8 omitidos), cero fallidos,
1503 aserciones; Python 546 aprobados en 203,76 segundos. Frontend: build correcto
(1 minuto 58 segundos), TypeScript sin errores y 42 tests aprobados en seis archivos.
El aviso de dependencia opcional `fontaine` y el resumen de tiempos de plugins son
informativos; no se agregan dependencias de produccion para ocultarlos.
No se ejecuto Cypress: no cambia ningun flujo, selector o contrato E2E; el unico ajuste
visual es el ancho fijo de un placeholder. La estructura y roles de la tabla se conservan.
La revision de accesibilidad es estatica y de markup, no con lector de pantalla real.
La suite Python se ejecuto en `.quality/ml-venv`, entorno local ignorado con las versiones
declaradas en `ml-service/pyproject.toml`, sin modificar dependencias de produccion.
Las correcciones de exportacion tambien preservan arrays JSON vacios, sin alterar el scanner.
No hay reglas de negocio nuevas ni cambios de requisito que promover o renumerar.

## Accion posterior del usuario

Ejecutar V2 solo despues de comprobar las pruebas locales. Mantener las capturas V1.
Registrar la revision justificada de 1 y 5 en SonarQube; no marcarlas corregidas sin
su explicacion. Las otras cuatro correcciones deben confirmarse mediante el analisis
V2. No se promete cero alertas ni una cobertura mayor por estas refactorizaciones.
Comparar con V1 usando la misma configuracion. La publicacion en GitHub queda pendiente
de una autorizacion posterior del usuario.
