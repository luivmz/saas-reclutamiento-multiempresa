# Base de presentación en `main`: arranque reproducible

> **Estado al 22/11/2026.** `main` incorpora el candidato aprobado para la demostración F37 y esta guía de arranque:
>
> - **Candidato:** `design/f37-visual` = `bb86991e8313b28a3daa19dafcacb57eb10f62d0`, árbol `b5a4004b4c84e82d8311f26738b51a8a95dc1342`.
> - **Dictamen de Codex:** «APTO PARA DEMOSTRACIÓN EXPERIMENTAL F37, CON OBSERVACIÓN NO BLOQUEANTE» (VIS-L01, §1).
> - **Integración:** técnica, por autorización del responsable del repositorio. No emite votos de los demás integrantes, no aprueba la G0, no adopta ningún ADR y no supera ningún gate.
> - **Estados formales:** ninguno cambia (§1.2). Los hashes de los merges se consultan en Git; esta guía no los anticipa.

## 1. Qué contiene `main` y con qué estado

### 1.1 Contenido

| Bloque | Qué es | Cómo está disponible en `main` |
|---|---|---|
| SEG-01 a SEG-04 | Autorización del expediente interno y de las descargas de CV, serialización entre la decisión y el cambio de etapa, y metadatos de auditoría sin texto libre (DEF-14 a DEF-17, A-37 y A-38) | Siempre activo. Auditado e integrado antes en `develop` |
| Continuación del producto | Cronograma del proceso en la vacante, escenario ML-01 del `DemoSeeder` (DEF-18) y portada con roles y límites. Incluye CONT-M01 a CONT-M03 | Siempre activo |
| Portada y pulido visual | Profundidad con CSS 3D (ADR-003) y pantallas del recorrido F37 más claras | Siempre activo. **VIS-L01** (LOW, abierta y no bloqueante): si se activa el movimiento reducido con la página abierta, `Reveal` no adapta del todo los bloques pendientes |
| Flujo de evidencias y versiones (F37) y ayuda documental ML-02 | Evidencias de solo inserción, versiones conservadas, historial sin texto y búsqueda léxica BM25 por postulación | **Solo con `EXPERIMENTAL_EVIDENCIAS=true`** (§3). La migración `2026_11_10_000001_create_evidence_tables` crea siempre las tablas, aunque la bandera esté apagada |
| Documentación F36-SBX y de entrega | Q2 y su adopción RR-001, borradores D-10 y D-11, especificación S v2.2, expediente final, prototipo estático de ML-02, [entrega final](../entrega-final/README.md) | Solo documentación |

No entra en `main`:

- B-01 experimental (`exp/b01-candidato`) ni el stash publicado (`transfer/stash-f36sbx-af5-wip-20261027`);
- las ramas de SonarQube, Dependabot y registro de software;
- el vídeo de Higgsfield, que se revisa en su propia rama visual.

### 1.2 Estados formales, sin cambios

- G0 real = NO APROBADA. G0-02, G0-03 y G0-12 = PENDIENTE EXTERNO. G0-09 y G0-14 = CUMPLIDO. G0-SBX = APROBADA CON RESTRICCIONES. ADR-005 = PROPUESTA.
- F35-SBX = CERRADA Y CONGELADA. F36-SBX = EN DISEÑO. F36-SBX-GATE = NO SUPERADO. F37-SBX = BLOQUEADA. F36–F40 productivas = BLOQUEADAS.
- La integración formal de estas capacidades en el SaaS (EI-23) sigue BLOCKED. Alcance C = BLOQUEADO. Datos reales = PROHIBIDOS.
- RF-23 sigue siendo la decisión final humana de Dirección. RF-29 (ML-01) sigue experimental e informativo. RF-01 a RF-27 no cambian.

**Experimental disponible no es fase habilitada.** Que el código esté en `main` detrás de una bandera desactivada por omisión permite presentarlo, pero F37-SBX sigue BLOQUEADA. Para que deje de ser experimental hacen falta la G0 real, un ADR de alcance y la decisión N5 (EI-23), con F36-SBX-GATE SUPERADO ([`docs/experimental/README.md` §5](../experimental/README.md#5-lo-que-falta-para-que-deje-de-ser-experimental)).

## 2. Arranque

### 2.1 Requisitos

- Docker Desktop o Docker Engine con Compose 2.24 o superior. Laravel, Node, PostgreSQL y Redis corren en contenedores ([`docs/docker.md`](../docker.md)).
- Python 3.12, solo para ML-01 (§5).

### 2.2 Proyecto Docker

Sin `-p`, Compose usa el proyecto `reclutamiento` (puerto 8000) y su base de desarrollo. Para presentar sin tocar esa base, conviene un proyecto propio:

- **Nombre del proyecto.** Por ejemplo, `-p presentacion`, en todos los comandos.
- **`.env` local, que no se versiona.** Puertos libres para `APP_PORT`, `APP_URL`, `FORWARD_DB_PORT`, `FORWARD_REDIS_PORT` y `E2E_APP_PORT`, y un `CACHE_PREFIX` propio.

```powershell
Copy-Item .env.example .env          # y editar puertos y prefijo
docker compose -p presentacion up -d --wait
docker compose -p presentacion ps    # comprobar que los contenedores son presentacion-*
```

El primer arranque genera `APP_KEY` y ejecuta `composer install`, `npm ci` y `npm run build` en los volúmenes del proyecto. Si falta la imagen local `reclutamiento-php:dev`, se construye una vez, como indica la [entrega final §2.2](../entrega-final/README.md#22-imagen-local-de-php).

### 2.3 Datos ficticios

```powershell
docker compose -p presentacion exec app php artisan migrate:fresh --seed --force
```

- **Qué carga:** `DemoSeeder`, con dos organizaciones y todos los escenarios de [`demo-users.md`](../demo-users.md). La contraseña de todas las cuentas es `password`.
- **Cuidado:** `migrate:fresh` borra la base del proyecto indicado. Se usa solo sobre un proyecto de demostración, nunca sin `-p` si el proyecto `reclutamiento` tiene datos que conservar.

## 3. Bandera experimental

**Desactivada por omisión.** `config/experimental.php` lee `EXPERIMENTAL_EVIDENCIAS` con valor por defecto `false`, y `.env.example` no la define. Con la bandera apagada:

- no aparecen los enlaces;
- las ocho rutas de evidencias responden 404 (`EvidenceEntryPointsTest`).

**Activarla para presentar**, solo en el `.env` local:

```powershell
# 1. Añadir al .env:  EXPERIMENTAL_EVIDENCIAS=true
docker compose -p presentacion exec app php artisan config:clear
docker compose -p presentacion exec app php artisan db:seed --class=ExperimentalEvidenceSeeder --force   # una vez, sobre DemoSeeder
```

- **`ExperimentalEvidenceSeeder`** añade cinco versiones de evidencias ficticias a POS-00003, la postulación en evaluación de «Docente de Comunicación - Secundaria». Se niega a repetirse sobre los mismos datos.
- **Para Cypress,** `.env.e2e` lleva la misma línea (E2E-21 la necesita).
- **Desactivarla:** `EXPERIMENTAL_EVIDENCIAS=false` (o quitar la línea) y `config:clear`.
- **Recorrido:** el guion de cinco minutos está en [`docs/experimental/README.md` §3](../experimental/README.md#3-guion-de-cinco-minutos), con el puerto del proyecto que se use.

## 4. ML-02: ayuda documental BM25

Los resultados del experimento preregistrado no cambian ([resultados](../academico/preparacion-f38-ml02/resultados-exp-bm25-v1/RESULTADOS.md)):

| Aspecto | Valor |
|---|---|
| Método | `EXP-BM25-LEXICO-v1`: búsqueda léxica BM25 dentro de **una** postulación, k = 3, con abstención |
| Entrenamiento | Ninguno |
| Corpus evaluado | 12 fragmentos |
| Recall@3 | 0,5 en `dev` y **0 en `test`** |
| Hipótesis H2 | Rechazada |
| Qué no hace | No puntúa, ordena, compara, recomienda ni descarta personas. No entra en el ranking (RF-21), en la decisión de Dirección (RF-23) ni en ML-01 |

- **Una consulta satisfactoria no es una evaluación.** Que «Conocimientos pedagógicos» recupere su evidencia en la demo no cambia esas cifras.
- **Cualquier método nuevo** necesita otro `method_id` y otro preregistro, sin usar `test` para desarrollarlo.

## 5. ML-01: riesgo operacional (RF-29, opcional)

El código de `ml-service/` y el freeze ([`phase-15b-experiment-freeze.json`](../v1.1/ml/phase-15b-experiment-freeze.json)) están versionados. El artefacto entrenado no.

| Estado | Qué significa | Qué ve la página |
|---|---|---|
| **Reconstruible** | Hay código y freeze, pero no `ml-service/artifacts/model/risk_model.joblib` ni su `risk_model.metadata.json`. Es el estado de un clon nuevo | Modo descriptivo, sin estimación |
| **Disponible** | El artefacto se reconstruyó en esta máquina, uvicorn está levantado y Laravel tiene la bandera y el token | Estimación del riesgo de demora del **proceso**, nunca de una persona |

**Token compartido.** Un único secreto local, con el mismo valor en dos sitios: `ML_SERVICE_TOKEN` en el `.env` de Laravel y `RECRUITMENT_ML_INTERNAL_TOKEN` en el entorno de uvicorn. No se versiona ni se escribe en ningún documento. Puede generarse con `python -c "import secrets; print(secrets.token_hex(32))"`.

**Arranque**, en otra terminal, desde `ml-service/`:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -e ".[dev]"
.venv\Scripts\python.exe -m recruitment_ml.serving.build_artifact   # reconstruye el modelo desde el freeze
$env:RECRUITMENT_ML_INTERNAL_TOKEN = "<secreto local>"
.venv\Scripts\python.exe -m uvicorn recruitment_ml.api.app:app --host 0.0.0.0 --port 8008
```

En el `.env` de la raíz: `ML_SERVICE_ENABLED=true`, `ML_SERVICE_URL=http://host.docker.internal:8008` y `ML_SERVICE_TOKEN=<el mismo secreto>`. Después, `php artisan config:clear` en el contenedor.

- **Comprobación:** `curl http://127.0.0.1:8008/health` devuelve `"model_ready": true`.
- **Escenario:** «Docente de Ciencia y Tecnología - Secundaria» (DEF-18).
- **Sin el servicio** (o con `ML_SERVICE_ENABLED=false`, el valor de `.env.example`), la plataforma funciona igual y el panel queda en modo descriptivo. ML-01 puede seguir apagado durante la presentación.

## 6. Verificación

```powershell
docker compose -p presentacion exec app php artisan test        # PHPUnit, sobre su propia base reclutamiento_testing
docker compose -p presentacion exec app npx tsc --noEmit
docker compose -p presentacion exec app npx vp test --run
docker compose -p presentacion exec app npm run build
docker compose -p presentacion run --rm --no-deps --entrypoint sh app docker/php/init-e2e-env.sh   # crea .env.e2e si falta
docker compose -p presentacion --profile e2e run --rm cypress --spec "cypress/e2e/e2e-21-evidencias-experimental.cy.js"
```

Cypress usa `app-e2e`, con su propia base `reclutamiento_e2e`. Su `.env.e2e` lleva `EXPERIMENTAL_EVIDENCIAS=true` para E2E-21.

### 6.1 Resultados en la PC principal (22/11/2026)

Código de `bb86991`. Esta guía solo añade documentación: el commit de integración no cambia ningún archivo fuera de `docs/`, `CLAUDE.md` y `README.md`.

| Prueba | Resultado |
|---|---|
| `git diff --check` sobre lo que entra en `main` | Sin errores |
| Tipos · componentes · build | 0 errores · 65 passed (9 archivos) · correcto |
| `vp check` de los 21 archivos de frontend que cambian | Sin errores en 20. `resources/js/lib/format.ts` tiene cinco líneas sin formatear, **todas ya presentes en `main`** antes de F37; las líneas que añade F37 están bien formateadas. Deuda previa, no se corrige aquí |
| PHPUnit completo | 525 passed y 8 skipped (2746 aserciones), sobre `reclutamiento_testing` |
| Comprobaciones funcionales con la bandera encendida | 14 de 14, en el proyecto de la presentación, con datos de demo y solo lecturas. Cubren portada; empleos y su detalle; inicio de sesión; enlace del expediente; evidencias de POS-00003; BM25 (aciertos en «Conocimientos pedagógicos» y «Clase modelo», abstención en «Entrevista personal»); búsqueda exacta; proceso cerrado; Dirección (historial 200); evaluador (historial 403); y otra organización (404) |
| Comprobaciones funcionales con la bandera apagada | 7 de 7, en `app-e2e`, con su base aparte: las rutas de evidencias responden 404 y el expediente no ofrece el enlace |
| Cypress E2E-00 a E2E-22 | **23 de 23 specs en verde a la primera, 114 de 114 pruebas**, una spec por contenedor y en serie, con la bandera encendida en `.env.e2e`. E2E-10 pasó a la primera; el desfase de reloj entre la VM y el host fue de 0 a 1 s en todas las specs |

Que E2E-10 pasara esta vez no cierra su fragilidad (F37-RA-L01): una ejecución en verde no demuestra la causa del fallo anterior. Los resultados anteriores de la rama (525 passed y 8 skipped; 22 de 23 specs a la primera, E2E-10 repetida) están registrados en [`docs/experimental/README.md` §4 y §8](../experimental/README.md#4-pruebas). Sus logs están fuera de Git, en el paquete de auditoría.

## 7. Paquete de auditoría externo

El paquete `experimental-20261110/evidencias/` (logs, capturas y manifiestos SHA-256) está fuera de Git y **no hace falta para ejecutar la aplicación**. No estaba en la PC principal el 22/11/2026. Por eso las cifras de la §6.1 se obtuvieron de nuevo aquí. Las de la rama se citan como registradas, sin presentarlas como comprobadas en esta máquina.

## 8. Volver a servir `main` sin perder datos

La base de datos y los archivos subidos viven en los volúmenes del proyecto y en `storage/` del checkout que se sirve, no en la rama. Para volver a `main` desde otra rama que no añada migraciones:

```powershell
git switch main                       # en el checkout que monta el contenedor
git pull --ff-only
docker compose -p presentacion exec app npm run build
docker compose -p presentacion exec app php artisan config:clear
```

- **Qué se conserva:** volúmenes, `.env`, `storage/` y datos.
- **Qué no se usa:** ni `migrate:fresh` ni `down -v`.
- **Si la otra rama añadiera migraciones,** antes de cambiar habría que revisarlas, porque `main` no las conoce.
