# Practica de SonarQube para el sistema de reclutamiento

La practica prepara el diagnostico inicial del sistema de reclutamiento, su mejora guiada por hallazgos reales y una comparacion posterior. Se adapta la guia docente de Academia Virtual al proyecto Laravel 13, React y TypeScript existente. No sustituye sus RF ni habilita capacidades productivas o datos reales.

## Estado verificado el 20 de octubre de 2026

Rama: `codex/mejoras-sonarqube`. Base: `develop`, commit `ca36875938eca035c97205921ec5f9633381c571`.

Docker ya funciona y V1 termino sobre codigo real: 25 130 lineas, cobertura global 57,1 %, duplicacion 0,6 % y seis hallazgos. El detalle y las decisiones estan en [la revision de V1](revision-v1.md). Se aplicaron cuatro refactorizaciones locales y se documentaron dos revisiones justificadas; las reglas de negocio se conservan. Regresion posterior correcta: PHP 412 aprobadas y 8 omitidas, Python 546 aprobadas, frontend 42 aprobadas, build y TypeScript sin errores. **V2 no se ha ejecutado**, por indicacion del usuario. Tampoco se publican estos cambios locales en GitHub ni se modifica main/develop.

Comprobaciones realizadas en esta sesion: parser de PowerShell sin errores; `docker compose config --quiet` correcto; `bash -n` del ejecutor correcto; `php -l` del generador XML correcto; XML derivado conserva la base de pruebas forzada y las suites; rutas nuevas y reglas de ignorado verificadas; `git diff --check` sin errores. Se intento `Preparar` y se detuvo correctamente al detectar el motor no disponible. Estas comprobaciones estaticas no sustituyen la ejecucion en Docker.

Este trabajo es una practica de calidad separada; no abre F35 productiva ni F36-F40. Se conservan el aislamiento multiempresa, la auditoria append-only, la decision humana RF-23 y el caracter experimental de RF-29. No se modifica el baseline RF/CU/RNF ni la documentacion historica.

## Archivos preparados

- [Configuracion del scanner](../../../sonar-project.properties).
- [Compose independiente de la practica](../../../docker-compose.quality.yml).
- [Comandos de PowerShell](../../../tools/sonarqube.ps1).
- [Imagen de cobertura](../../../docker/quality/Dockerfile).
- [Ejecucion PHP y frontend](../../../docker/quality/check.sh).
- [Generador de configuracion PHPUnit](../../../docker/quality/phpunit-config.php).
- [Prompts para la segunda version](prompts.md).

Los archivos de ejecucion y las credenciales quedan en `.quality/`, ignorado por Git y por el contexto Docker. No subir esa carpeta, el token ni la clave del administrador.

## Requisitos y procedencia

Docker Desktop debe mostrar **Engine running**. PHP 8.4, Composer y Node se toman del Dockerfile existente, conservando sus versiones fijadas. No se utiliza el PHP 8.2 de XAMPP para ejecutar este proyecto Laravel 13. SonarScanner tambien corre en Docker: no requiere instalar Java o editar el PATH de Windows.

SonarQube y SonarScanner son imagenes oficiales, fijadas por digest consultado en Docker Hub el 20/10/2026. PCOV 1.0.12 procede de PECL, usa PHP License y declara compatibilidad PHP 8.4; solo se instala en la imagen de calidad. No cambia dependencias de produccion, `composer.lock`, `package-lock.json` ni configuracion global. Revision de riesgo: las imagenes y PECL ejecutan binarios en contenedores locales, sin privilegios elevados ni montaje del socket Docker. Los origenes se enlazan al final. Las versiones se fijan para hacer reproducible la practica, no como certificacion de ausencia de vulnerabilidades.

Se usa H2 embebido para esta practica local, como permite SonarSource para pruebas. Los tres volumenes de SonarQube conservan sus datos; no es una instalacion productiva. Si se transforma en un servicio compartido, debe prepararse una base compatible y su operacion por separado.

Todos los servicios pertenecen al proyecto Compose `reclutamiento-sonarqube`. La base de pruebas es un PostgreSQL exclusivo y sin puerto publicado. No se usan los contenedores, volumenes o bases de las otras copias del proyecto. PHPUnit puede limpiar **esa base ficticia de pruebas** mediante `RefreshDatabase`.

## Ejecucion desde VS Code

Abre una terminal PowerShell en la raiz de esta carpeta. Reinicia Windows si Docker presenta el error de socket y espera **Engine running**. No uses restablecimiento de fabrica ni borres volumenes para esta practica.

### 1 Validar la configuracion y preparar imagenes

```powershell
.\tools\sonarqube.ps1 Validar
.\tools\sonarqube.ps1 Preparar
```

`Validar` comprueba Compose y no requiere motor. `Preparar` construye la base ya definida por el proyecto, agrega PCOV en una imagen separada y descarga SonarQube/scanner oficiales. La primera ejecucion requiere red y puede tardar varios minutos. No instala herramientas globales.

### 2 Ejecutar las pruebas reales antes de analizar

```powershell
.\tools\sonarqube.ps1 Pruebas
.\tools\sonarqube.ps1 Frontend
```

El primer comando ejecuta PHPUnit y genera `coverage.xml`, `test-results.xml` y `.quality/tests.log`. El XML de calidad se deriva de `phpunit.xml`, preserva sus variables forzadas de testing y amplia el filtro a las carpetas PHP analizadas, sin esconder archivos propios sin cobertura. Mantiene separadas las pruebas del codigo fuente. Un fallo detiene el proceso y no produce constancia PASS. Los reportes se vinculan al hash del codigo y no se aceptan despues de modificarlo.

El segundo comando instala las versiones bloqueadas por npm, compila Vite, revisa TypeScript y ejecuta los tests de componente. Son verificaciones de regresion; no se convierten artificialmente en cobertura JS. Cypress no se ejecuta con este atajo. Si posteriormente una correccion afecta un flujo cubierto por Cypress, debe verificarse mediante el entorno E2E aislado descrito en [la guia existente](../../testing/cypress-e2e.md).

La base de pruebas se detiene al finalizar cada comando para liberar memoria antes del analisis. No se borran sus datos. Si el equipo dispone de poca RAM, detiene tambien SonarQube antes de construir o ejecutar pruebas; no se cierran aplicaciones ajenas automaticamente.

### 3 Iniciar SonarQube y crear el proyecto

```powershell
.\tools\sonarqube.ps1 Iniciar
```

Abre <http://127.0.0.1:9000>. Espera hasta que el servidor este operativo. En una instalacion nueva el acceso inicial es `admin` / `admin`; en esta PC la clave ya fue cambiada y debe conservarse de forma privada. Es independiente de las cuentas de GitHub, GitLab y la universidad.

Selecciona crear proyecto manualmente con:

- Nombre: `SaaS Reclutamiento Multiempresa`.
- Project key: `reclutamiento-sonarqube`.
- Linea de codigo nuevo: version anterior, si el asistente solicita esa eleccion.

Genera un token de usuario para esta practica. El script necesita permiso para analizar y consultar metricas, issues y hotspots del proyecto. Introducelo en el prompt oculto de `Analizar`; no se guarda en disco ni se escribe en el comando del scanner. No compartas el token en capturas. Los tokens se pueden revocar al terminar la practica.

### 4 Registrar V1 antes de corregir el producto

```powershell
.\tools\sonarqube.ps1 Analizar -Version V1
```

El scanner y PHPUnit montan el codigo en la misma ruta `/var/www/html`; no se alteran los aciertos de cobertura ni se necesitan rutas artificiales. El comando exige pruebas PASS del mismo codigo y archivos XML sin modificaciones, comprueba el procesamiento real de SonarQube y guarda los resultados. Un contenedor iniciado, la existencia del dashboard o un log parcial no equivalen a un analisis terminado.

Las fuentes incluyen Laravel, React/TypeScript, recursos, configuracion, base de datos y el servicio Python experimental. Solo se excluyen dependencias, caches, archivos generados y pruebas de las fuentes productivas; estas ultimas se clasifican como tests. PHPUnit aporta cobertura **PHP**, no cobertura de React ni Python. La cobertura global puede ser menor que la de PHP y debe reportarse tal como la calcule SonarQube. No se ajustan exclusiones para subir la nota.

Los resultados se guardan en `.quality/evidencias/V1-<fecha>/`: `manifest.json`, `measures.json`, `quality-gate.json`, `issues.json`, `hotspots.json`, log del scanner, log de pruebas, Clover, JUnit y la configuracion. `.quality/baseline.json` identifica la primera V1 y no se sobreescribe. Los archivos contienen evidencias locales, no un informe final generado de antemano.

Guarda capturas autenticas de **Dashboard, Quality Gate, Measures, Issues y Coverage**. Captura tambien Security Hotspots y su revision cuando existan. No incluyas tokens, claves ni personas reales.

### 5 Preparar las correcciones y V2

Prioriza problemas reales de seguridad/fiabilidad y despues mantenibilidad, complejidad, duplicacion y cobertura. Usa [los prompts preparados](prompts.md) con la regla, archivo y linea del issue real. Preserva comportamiento, autorizacion por organizacion y auditoria. Un hotspot exige revision humana: no se marca seguro solo para mejorar el resultado.

Registra cada cambio y su prueba. Despues vuelve a ejecutar:

```powershell
.\tools\sonarqube.ps1 Pruebas
.\tools\sonarqube.ps1 Frontend
.\tools\sonarqube.ps1 Analizar -Version V2
```

V2 requiere una linea base V1 real y codigo distinto. Se usa el mismo proyecto de SonarQube con `sonar.projectVersion=2.0`, conservando el historial y las copias de V1. La rama Git separa este trabajo; no se pasa `sonar.branch.name`, que no es necesario para esta practica local.

Las correcciones locales y las dos alertas que requieren clasificacion manual estan en [revision-v1.md](revision-v1.md). No se renombra simplemente la misma ejecucion como V2 ni se modifica codigo para fabricar defectos de partida. El usuario ejecutara V2 y revisara el estado de las alertas; no hay una segunda medicion que declarar todavia.

## Registro de comparacion

V1 contiene resultados reales; la columna V2 queda pendiente de la ejecucion del usuario. Los valores de ejemplo de la guia no son resultados de este proyecto. Las calificaciones son las de MQR MODE de este servidor.

| Indicador | V1 | V2 |
|---|---|---|
| Quality Gate | OK; condicion new_violations = 0 | No ejecutada |
| Security | C; 2 impactos | No ejecutada |
| Reliability | C; 4 impactos | No ejecutada |
| Maintainability | A; 1 impacto | No ejecutada |
| Security Hotspots y revisados | 0; no aplica porcentaje revisado | No ejecutada |
| Coverage y alcance de cobertura | 57,1 % global; solo PHP aporta reporte | No ejecutada |
| Duplicated Lines | 0,6 % | No ejecutada |
| Issues | 6 distintos | No ejecutada |
| Cognitive Complexity | 1034 | No ejecutada |
| Technical Debt | 30 minutos (sqale_index) | No ejecutada |

Un Quality Gate aprobado no certifica que todo el sistema sea correcto, accesible o validado con usuarios. Tampoco un fallo del gate significa que el scanner fallo: un analisis exitoso puede revelar calidad insuficiente. El script conserva el resultado real incluso si el gate es ERROR.

La guia menciona ISO 25001 al preparar la siguiente version. La relacion con ese marco debe justificarse en el informe; ejecutar SonarQube por si solo no constituye una certificacion ISO.

## Estado y parada

```powershell
.\tools\sonarqube.ps1 Estado
.\tools\sonarqube.ps1 Detener
```

`Detener` solo para los contenedores de esta practica; conserva volumenes. No utiliza `down -v`, `docker system prune`, borrado de volumenes ni cambios en otros proyectos.

Si falla el inicio de Elasticsearch, consulta sus logs y los requisitos oficiales del host antes de cambiar configuraciones. No desactives comprobaciones de seguridad para forzar el arranque. Si el puerto 9000 esta ocupado, identifica primero su propietario.

## Referencias tecnicas verificadas

- [Instalacion oficial con Docker y opcion H2 para pruebas](https://docs.sonarsource.com/sonarqube-community-build/server-installation/from-docker-image/set-up-and-start-container).
- [Persistencia con volumenes](https://docs.sonarsource.com/sonarqube-community-build/server-installation/from-docker-image/prepare-installation).
- [SonarScanner CLI oficial](https://docs.sonarsource.com/sonarqube-community-build/analyzing-source-code/scanners/sonarscanner).
- [Cobertura PHP generada antes del scanner](https://docs.sonarsource.com/sonarqube-community-build/analyzing-source-code/test-coverage/php-test-coverage).
- [PCOV 1.0.12 y licencia](https://pecl.php.net/package/pcov/1.0.12).
- [Tokens](https://docs.sonarsource.com/sonarqube-community-build/user-guide/managing-tokens) y [Web API](https://docs.sonarsource.com/sonarqube-community-build/extension-guide/web-api).
- [Imagen oficial SonarQube](https://hub.docker.com/_/sonarqube) e [imagen oficial SonarScanner](https://hub.docker.com/r/sonarsource/sonar-scanner-cli).
