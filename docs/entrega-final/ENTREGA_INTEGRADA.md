# Entrega académica integrada

La aplicación reúne la base F37 y las correcciones SEG, Reportes, las evidencias versionadas y la ayuda documental experimental, los dos vídeos, el anfitrión, las ofertas demo adicionales y el informe F29H v2. RF-28 sigue siendo candidato. La decisión de selección la confirma y justifica Dirección (RF-23). La integración técnica conserva los estados formales y el uso de datos ficticios.

El [cierre responsive y auditoría técnica](RESPONSIVE_QA.md) registra la validación a siete anchos, la suite completa y las capturas. El apartado de verificación de esta guía documenta el corte integrado anterior. El informe académico F29H v2 mantiene su propio corte.

## Arranque desde un clon

Se requiere Git y Docker Desktop o Docker Engine con Compose V2. Los contenedores instalan Composer y Node, usan los archivos de dependencias bloqueadas, compilan Vite y ejecutan las migraciones.

```bash
git clone --branch main https://github.com/luivmz/saas-reclutamiento-multiempresa.git
cd saas-reclutamiento-multiempresa
git rev-parse HEAD
```

En el clon nuevo, copia .env.example a .env con `Copy-Item .env.example .env` en PowerShell o `cp .env.example .env` en macOS/Linux. Usa un nombre de proyecto Docker libre. Si sus puertos ya están ocupados, ajusta APP_PORT y APP_URL juntos, FORWARD_DB_PORT, FORWARD_REDIS_PORT y E2E_APP_PORT en .env. APP_PORT acepta una asignación como `127.0.0.1:8000` para limitar el acceso local. Mantén SEED_ON_BOOT=false.

Para demostrar el expediente de evidencias, configura `EXPERIMENTAL_EVIDENCIAS=true` en el .env de este clon. El valor de ejemplo es false. Con la bandera apagada, los enlaces están ocultos y las rutas del módulo responden 404. Si cambias el valor en un proyecto iniciado, ejecuta `docker compose -p entrega-colegio exec app php artisan config:clear`.

```bash
docker compose -p entrega-colegio up -d --wait --build
curl http://localhost:8000/health
docker compose -p entrega-colegio exec app php artisan db:seed --class=DemoSeeder --force
docker compose -p entrega-colegio exec app php artisan db:seed --class=DemoJobOffersSeeder --force
```

En Windows PowerShell, usa `curl.exe` para la consulta de /health. Ejecuta DemoSeeder una vez en la base recién migrada de ese proyecto. DemoJobOffersSeeder se puede repetir y conserva las ofertas existentes. Con la bandera habilitada, añade las evidencias iniciales una vez sobre la base demo:

```bash
docker compose -p entrega-colegio exec app php artisan db:seed --class=ExperimentalEvidenceSeeder --force
```

Si una base ya tiene sus datos de demostración, conserva ese volumen y carga únicamente el seeder adicional que le falte. La lista de usuarios ficticios y el alcance de cada seeder están en [Usuarios demo](../demo-users.md).

## Recorrido

1. Abre http://localhost:8000 y desplázate por la portada. Usa **Ver empleos disponibles**, pasa por las tarjetas para ver los gestos del anfitrión y prueba la paginación. Entra a dos ofertas para ver el vídeo de la carpeta. Los controles de tema, los pósteres de respaldo y la preferencia de movimiento reducido están disponibles según el dispositivo.
2. En una sesión de RR. HH. del Colegio Andino demo, sigue Vacantes → **Docente de Comunicación - Secundaria** → Postulaciones → **POS-00003** → **Evidencias (experimental)**. En Ayuda documental elige **Conocimientos pedagógicos** y **Ver fragmentos**. La consulta usa el contenido de esa postulación. El [guion experimental](../experimental/README.md#3-guion-de-cinco-minutos) explica las versiones, la fuente del fragmento y la abstención.
3. En el menú de RR. HH. o Dirección abre **Reportes** (/reportes) y filtra por periodo, vacante o etapa. Compara con una sesión separada de RR. HH. de Demo B para ver el aislamiento. Los indicadores y gráficos usan agregados de la organización autenticada. La [descripción de Reportes](../architecture-cypress-reports/reportes/MODULO_REPORTES.md) explica las fórmulas.

## ML-01 y ML-02

**ML-01** es el servicio FastAPI opcional de riesgo de demora del proceso. Con ML_SERVICE_ENABLED=false, Laravel conserva el panel descriptivo. El [procedimiento de ML-01](../../ml-service/README.md#servicio-experimental-15c) usa Python 3.12 o posterior y las dependencias fijadas en pyproject.toml. Desde ml-service, crea el entorno virtual y ejecútalo con su Python:

```powershell
cd ml-service
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m recruitment_ml.serving.build_artifact
```

En macOS o Linux, usa `.venv/bin/python` en los dos últimos comandos. El constructor valida el protocolo congelado antes de escribir el artefacto en artifacts. Si lo habilitas desde Docker Desktop, fija el mismo token local en RECRUITMENT_ML_INTERNAL_TOKEN para FastAPI y en ML_SERVICE_TOKEN para Laravel. Arranca FastAPI con `python -m uvicorn recruitment_ml.api.app:app --host 0.0.0.0 --port 8008` usando el Python del entorno virtual y restringe el puerto a acceso local o privado. Verifica `/health` y `model_ready=true` antes de fijar ML_SERVICE_URL=http://host.docker.internal:8008 y ML_SERVICE_ENABLED=true en Laravel. Consulta la [guía Laravel–FastAPI](../v1.1/phase-16-laravel-ml-integration.md).

**ML-02** usa BM25 dentro de Laravel para buscar hasta tres fragmentos de evidencias de una postulación y mostrar su procedencia. Se abstiene si no encuentra coincidencias. El [resultado experimental](../academico/preparacion-f38-ml02/resultados-exp-bm25-v1/RESULTADOS.md) registra 12 fragmentos sintéticos, Recall@3 de 0,5 en dev y 0,0 en test, y las limitaciones. Su ejecución no requiere FastAPI, entrenamiento ni descargar un modelo.

## Pruebas aisladas

El proyecto Compose crea PostgreSQL y Redis propios. Antes de ejecutar PHPUnit, comprueba que el contenedor app monta el clon actual y se conecta a su servicio postgres. PHPUnit usa reclutamiento_testing, forzado en phpunit.xml. Cypress usa el servicio app-e2e con la base reclutamiento_e2e y otras bases lógicas de Redis. Genera .env.e2e con el comando indicado y habilita EXPERIMENTAL_EVIDENCIAS=true **en ese archivo local** si vas a ejecutar E2E-21. Comprueba la asignación de base antes de lanzar Cypress. Sus resets actúan sobre los datos de pruebas.

```bash
docker compose -p entrega-colegio exec -T app npm run build
docker compose -p entrega-colegio exec -T app npm run types:check
docker compose -p entrega-colegio exec -T app npx vp test --run
docker compose -p entrega-colegio exec -T app php artisan test
docker compose -p entrega-colegio run --rm --no-deps --entrypoint sh app docker/php/init-e2e-env.sh
# Editar .env.e2e, configurar EXPERIMENTAL_EVIDENCIAS=true y guardar antes de levantar E2E.
docker compose -p entrega-colegio --profile e2e up -d --wait app-e2e queue-e2e
docker compose -p entrega-colegio --profile e2e run --rm cypress
```

El spec E2E-25 de Reportes toma el lugar del nombre histórico E2E-20 de la práctica macOS. E2E-20 corresponde al recorrido demo. DEF-20 y DEF-21 son los hallazgos de celdas y Escape que esa práctica llamó DEF-14 y DEF-15. Véanse el [registro de defectos](../defects.md) y la [guía de Cypress](../testing/cypress-e2e.md).


## Verificación del 23/11/2026

El árbol funcional probado corresponde a [eb66fa6](https://github.com/luivmz/saas-reclutamiento-multiempresa/commit/eb66fa6c8f88a77ba86f51315db506dd4d03cf0a). [b84f355](https://github.com/luivmz/saas-reclutamiento-multiempresa/commit/b84f35579c21abfdef3ae08541a5a22609da6ed5) ajusta solamente dos specs. La guía, el cierre del informe y sus archivos derivados se añadieron después de las pruebas funcionales.

| Control | Resultado |
|---|---|
| PostgreSQL y Redis aislados | Proyecto entregafinalqa con volúmenes propios, bases reclutamiento, reclutamiento_testing y reclutamiento_e2e verificadas. |
| PHPUnit | 543 aprobadas, 8 omitidas y 3.130 aserciones. |
| Compilación, TypeScript y componentes | Build y tipos correctos. 101 pruebas de componentes aprobadas. |
| Lint | vp check y Pint en los archivos cambiados, correctos tras el ajuste de formato. Oxlint y sintaxis de ambos specs corregidos, correctos. |
| Cypress 15.3.0, suite completa | 148 de 153 casos y 24 de 26 specs aprobados en eb66fa6. Los 5 fallos se concentraron en E2E-24 y E2E-25. |
| Cypress, verificación focal | **35/35** en b84f355, en orden E2E-21 (10/10), E2E-24 (16/16) y E2E-25 (9/9). Se reutilizan los resultados de los specs intactos de la suite completa. |
| Chrome y datos demo | Portada y dos empleos con avance y retroceso de fotogramas, tema claro y oscuro, movimiento reducido dinámico, móvil de 390 px, anfitrión y 14 ofertas. También se comprobó BM25 con fuente y Reportes con RR. HH. y Dirección, incluidos los filtros de dos organizaciones. El seeder añadió 10 ofertas y, en la repetición, 0. |
| ML-01 | El servicio Python, cliente Laravel y configuración conservan identidad con el corte de origen. PHPUnit y Cypress cubrieron la integración Laravel y el respaldo descriptivo. Se reutiliza la referencia histórica de la suite Python. |
| SonarQube | Resultados históricos de la práctica en macOS. La entrega conserva la configuración y las evidencias de ese corte. |

E2E-24 cargó su fixture aislado antes de comprobar la segunda fila, que podía desaparecer por el cierre ejecutado en E2E-21. E2E-25 pasó a incluir las tres postulaciones retrospectivas de ML-01 que ya existen en DemoSeeder. Se conservaron las aserciones y se añadió la comprobación del total por semanas. Los primeros logs y capturas quedan archivados con los resultados focales. La primera sonda independiente de Chrome terminó por falta de WebSocket global en Node 20.16. La ejecución con la opción que habilita WebSocket pasó sus comprobaciones y guardó capturas.

El [historial de CI](https://github.com/luivmz/saas-reclutamiento-multiempresa/actions/workflows/tests.yml) permite localizar la ejecución de cada SHA publicado.

## Archivos de entrega

- El repositorio contiene los vídeos comprimidos, los pósteres y los clips del anfitrión en public/media, las migraciones, los seeders y el informe F29H v2 en [informe-final](../academico/informe-final/). Allí están el DOCX, el PDF, el Markdown, las plantillas, los recursos y el registro.
- En otro equipo se regeneran vendor, node_modules, public/build, las rutas TypeScript, las bases demo y de pruebas y, si se habilita ML-01, su entorno y artefacto local. .env, .env.e2e, claves, cachés, volúmenes y salidas crudas de las pruebas se mantienen fuera de Git.
- [Práctica de Reportes y SonarQube](../architecture-cypress-reports/README.md). Los resultados de Sonar corresponden a sus cortes históricos. La configuración y el procedimiento están disponibles para futuras mediciones.
- URL pública de la aplicación pendiente de confirmación. La URL de GitHub identifica el código y localhost identifica la demostración local.
