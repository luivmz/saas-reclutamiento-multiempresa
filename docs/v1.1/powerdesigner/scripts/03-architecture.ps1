# PK-01 paquetes, CO-01 componentes y DE-01 despliegue.
# Fuentes: docs/v1.1/uml/component-model.md (§1, §2, §3) y deployment-model.md (§1, §2),
# con sus borradores puml/pk-01-packages.puml, co-01-components.puml y de-01-deployment.puml.
. "$PSScriptRoot\pdlib.ps1"

function Link-Dep($model, $diagram, $syms, $objs, [string]$from, [string]$to, [string]$label = '', [string]$stereo = '') {
    $l = $model.CreateObject($PdKind.Dependency)
    $l.Object1 = $objs[$from]; $l.Object2 = $objs[$to]
    if ($label) { $l.Name = $label } else { $l.Name = $BlankName }
    if ($stereo) { $l.Stereotype = $stereo }
    $ls = $diagram.AttachLinkObject($l, $syms[$from], $syms[$to])
    Set-StraightLink $ls $syms[$from] $syms[$to]
}

Open-Pd
try {
    $m = $Pd.OpenModel($OomFile)

    # ------------------------------------------------------------------ PK-01
    $mod = New-Obj $m 'Package' 'Módulos del monolito' 'Modulos_monolito'
    $mod.Comment = 'Paquetes de PK-01: carpetas reales del monolito Laravel, no módulos de Composer ni servicios separados.'
    $pd1 = $mod.PackageDiagrams.CreateNew()
    $pd1.Name = 'PK-01 Paquetes del monolito'; $pd1.Code = 'PK_01'
    $pk = [ordered]@{
        REQ = @('Requerimientos (RF-01..RF-04)', -36000, 20000); VAC = @('Vacantes (RF-05..RF-07)', -12000, 20000)
        CAND = @('Postulantes (RF-08..RF-11)', 12000, 20000); APP = @('Postulaciones (RF-12..RF-15)', 36000, 20000)
        ASS = @('Evaluaciones (RF-16..RF-20)', 24000, 2000); SEL = @('Ranking y selección (RF-20..RF-26)', 48000, 2000)
        RISK = @('Riesgo operacional (RF-29)', -48000, 2000)
        AUD = @('Auditoría (RF-27)', -24000, -18000); MOD = @('Modelos y enums', 0, -26000)
        SHR = @('Compartido (notificaciones, settings, support)', 30000, -26000)
    }
    $po = @{}; $ps = @{}
    foreach ($key in $pk.Keys) {
        $p = New-Obj $mod 'Package' $pk[$key][0] "PK_$key"
        if ($key -eq 'RISK') { $p.Stereotype = 'experimental' }
        $po[$key] = $p; $ps[$key] = $pd1.AttachObject($p); Set-Box $ps[$key] $pk[$key][1] $pk[$key][2] 17000 6000
    }
    foreach ($key in 'REQ', 'VAC', 'CAND', 'APP', 'ASS', 'SEL', 'RISK') { Link-Dep $mod $pd1 $ps $po $key 'MOD' }
    foreach ($key in 'REQ', 'VAC', 'CAND', 'APP', 'ASS', 'SEL') { Link-Dep $mod $pd1 $ps $po $key 'AUD' }
    Link-Dep $mod $pd1 $ps $po 'VAC' 'REQ' 'vacante desde requerimiento aprobado'
    Link-Dep $mod $pd1 $ps $po 'ASS' 'APP' 'avance de etapa al programar'
    Link-Dep $mod $pd1 $ps $po 'SEL' 'APP' 'seleccionar y cerrar'
    foreach ($key in 'REQ', 'CAND', 'APP', 'ASS', 'SEL') { Link-Dep $mod $pd1 $ps $po $key 'SHR' }
    Add-Note $pd1 "Riesgo operacional depende solo de Modelos (lectura). Ningún paquete de negocio depende de él y él no depende de Ranking y selección." -48000 -12000 18000 | Out-Null
    Add-Note $pd1 "Monolito modular por carpetas: cada paquete reparte sus piezas entre Http/Controllers, Http/Requests y Services. No hay separación física." -40000 36000 26000 | Out-Null

    # ------------------------------------------------------------------ CO-01
    $cd = $m.ComponentDiagrams.CreateNew()
    $cd.Name = 'CO-01 Componentes AS-IS v1.1'; $cd.Code = 'CO_01'
    $comp = [ordered]@{
        PAGES   = @('Páginas Inertia (React 19 + TypeScript)', '', -52000, 34000)
        SHARED  = @('Componentes compartidos (DataTable, Section, ui/*)', '', -52000, 22000)
        CARD    = @('Tarjeta de riesgo operacional', 'experimental', -24000, 34000)
        HTTP    = @('Capa HTTP (rutas, middleware auth/role, Form Requests, controladores, presenters, resources)', '', -24000, 4000)
        AUTHZ   = @('Autorización y multiempresa (7 Policies, OrganizationScope)', '', -52000, -12000)
        ACCOUNT = @('Cuenta y acceso (Fortify, passkeys)', '', -52000, 4000)
        DOMAIN  = @('Servicios de dominio (requerimientos, vacantes, postulaciones, evaluaciones, selección)', '', -24000, -12000)
        RANKING = @('Cálculo de ranking (WeightingValidator, ScoreSheetValidator, RankingService, VacancyRankingBuilder)', '', 4000, -12000)
        MODELS  = @('Modelos de dominio (17 Eloquent + enums)', '', -24000, -30000)
        AUDIT   = @('Auditoría (AuditLogger)', '', 4000, -30000)
        NOTIF   = @('Notificaciones (RecruitmentNotification x6)', '', -52000, -30000)
        CVSTORE = @('Almacenamiento de CV (disco local privado)', '', 4000, 4000)
        RISK    = @('Riesgo operacional (OperationalRiskService, OperationalRiskFeatureBuilder, MlRiskClient)', 'experimental', 32000, 4000)
        PG      = @('PostgreSQL 17', 'database', -24000, -50000)
        REDIS   = @('Redis 7 (sesión, caché, cola)', '', -52000, -50000)
        WORKER  = @('Trabajador de cola (queue:work)', '', -52000, -66000)
        MAILLOG = @('Mailer log (desarrollo)', '', -24000, -66000)
        API     = @('API FastAPI (schemas, security)', 'external service, experimental', 62000, -12000)
        SERVING = @('Serving (loader, predictor)', 'experimental', 62000, -30000)
        MODEL   = @('Artefacto .joblib + metadatos (freeze 9ee18430..., threshold 0.1679418172266036)', 'artifact', 62000, -48000)
    }
    $co = @{}; $cs = @{}
    foreach ($key in $comp.Keys) {
        $c = New-Obj $m 'Component' $comp[$key][0] "CO_$key"
        if ($comp[$key][1]) { $c.Stereotype = $comp[$key][1] }
        $co[$key] = $c; $cs[$key] = $cd.AttachObject($c); Set-Box $cs[$key] $comp[$key][2] $comp[$key][3] 20000 5000
    }
    $ifs = [ordered]@{
        I_HTTP = @('Inertia / HTTP', -38000, 19000)
        I_RISK = @('JSON riesgo operacional: GET vacantes/{id}/riesgo-operacional', -10000, 19000)
        I_PREDICT = @('POST /v1/predict · X-Internal-Token', 48000, 4000)
    }
    foreach ($key in $ifs.Keys) {
        $i = New-Obj $m 'Interface' $ifs[$key][0] "IF_$key"
        $co[$key] = $i; $cs[$key] = $cd.AttachObject($i); Set-Pos $cs[$key] $ifs[$key][1] $ifs[$key][2]
    }
    $coDeps = @(
        @('PAGES', 'I_HTTP', ''), @('CARD', 'I_RISK', ''), @('HTTP', 'I_HTTP', 'provee'), @('HTTP', 'I_RISK', 'provee'),
        @('PAGES', 'SHARED', ''), @('HTTP', 'AUTHZ', ''), @('HTTP', 'ACCOUNT', ''), @('HTTP', 'DOMAIN', ''), @('HTTP', 'RISK', ''),
        @('HTTP', 'RANKING', ''), @('HTTP', 'CVSTORE', ''), @('DOMAIN', 'MODELS', ''), @('DOMAIN', 'AUDIT', ''), @('DOMAIN', 'NOTIF', ''),
        @('DOMAIN', 'RANKING', 'instantánea en FinalDecisionService'), @('DOMAIN', 'CVSTORE', ''), @('ACCOUNT', 'AUDIT', ''),
        @('RANKING', 'MODELS', ''), @('RISK', 'MODELS', 'solo lectura'), @('RISK', 'I_PREDICT', ''), @('API', 'I_PREDICT', 'provee'),
        @('API', 'SERVING', ''), @('SERVING', 'MODEL', ''), @('AUTHZ', 'MODELS', ''), @('MODELS', 'PG', ''), @('AUDIT', 'PG', ''),
        @('NOTIF', 'REDIS', 'encola'), @('WORKER', 'REDIS', ''), @('WORKER', 'PG', 'canal database'), @('WORKER', 'MAILLOG', 'canal mail')
    )
    foreach ($x in $coDeps) { Link-Dep $m $cd $cs $co $x[0] $x[1] $x[2] }
    Add-Note $cd "Navegador: lo sirve Laravel; sin servidor de frontend propio. La escena CSS 3D de la portada es presentación, no un componente." -38000 46000 30000 | Out-Null
    Add-Note $cd "Frontera RF-29: Riesgo operacional no depende de Cálculo de ranking ni de la decisión, ni ellos de él. 15 features, sin IDs ni PII. Deshabilitado: descriptive_only; sin respuesta válida: unavailable." 32000 -12000 20000 | Out-Null
    Add-Note $cd "Contrato de /v1/predict. Petición: 15 features operacionales enteras (extra=forbid, strict), sin candidate_id, vacancy_id, organization_id, PII ni texto libre. Respuesta: risk_score, risk_flag, threshold, model_version, freeze_fingerprint, status. Sin incertidumbre." 62000 12000 24000 | Out-Null
    Add-Note $cd "training/ y synthetic/ generan el artefacto fuera de línea; no participan en la ejecución." 62000 -62000 20000 | Out-Null

    # ------------------------------------------------------------------ DE-01
    $dd = $m.DeploymentDiagrams.CreateNew()
    $dd.Name = 'DE-01 Despliegue AS-IS v1.1 (desarrollo y demostración)'; $dd.Code = 'DE_01'
    # PowerDesigner 16 no dibuja los vínculos entre nodos anidados unos dentro de otros
    # (los extremos se resuelven contra el nodo más externo). Los contenedores que solo
    # agrupan (equipo del usuario, equipo anfitrión, Docker Engine y el contenedor app)
    # van como marcos gráficos con su estereotipo; los nodos que se comunican son objetos.
    Add-Frame $dd '<<device>> Equipo del usuario' -66000 0 26000 40000 | Out-Null
    Add-Frame $dd '<<device>> Equipo anfitrión' 14000 -6000 118000 100000 | Out-Null
    Add-Frame $dd '<<execution environment>> Docker Engine · proyecto reclutamiento' -2000 -12000 80000 80000 | Out-Null
    Add-Frame $dd '<<container>> app' -20000 11000 36000 30000 | Out-Null
    $nodes = [ordered]@{
        BROWSER  = @('Navegador web', 'execution environment', -66000, -6000, 20000, 16000)
        PHP      = @('PHP 8.4 · php artisan serve :8000', 'execution environment', -20000, 14000, 30000, 14000)
        QUEUE    = @('queue', 'container', 22000, 14000, 26000, 16000)
        POSTGRES = @('postgres', 'container', -20000, -40000, 26000, 16000)
        REDIS    = @('redis', 'container', 22000, -28000, 26000, 16000)
        PY       = @('Proceso Python · uvicorn :8008', 'execution environment, experimental', 58000, -10000, 24000, 40000)
    }
    $no = @{}; $ns = @{}
    foreach ($key in $nodes.Keys) {
        $n = New-Obj $m 'Node' $nodes[$key][0] "ND_$key"
        $n.Stereotype = $nodes[$key][1]
        $no[$key] = $n; $ns[$key] = $dd.AttachObject($n)
        Set-Box $ns[$key] $nodes[$key][2] $nodes[$key][3] $nodes[$key][4] $nodes[$key][5]
    }
    # Los objetos File de PowerDesigner no admiten '/' ni ':' en el nombre: el nombre
    # usa guiones y la ruta o la orden exactas quedan en el comentario.
    $files = [ordered]@{
        F_BUNDLE  = @('Bundle JS y CSS (React + Inertia)', -66000, -10000, 'Bundle compilado por Vite, ejecutado en el navegador')
        F_LARAVEL = @('Aplicación Laravel', -27000, 10000, 'Código montado desde el repositorio (.:/var/www/html)')
        F_BUILD   = @('public-build', -13000, 10000, 'public/build: lo genera npm run build en docker/php/entrypoint.sh')
        F_CVSTORE = @('storage-app-private (CV)', -20000, 1000, 'storage/app/private: disco local de Laravel para los CV en PDF')
        F_WORKER  = @('queue work redis --tries=3', 22000, 10000, 'php artisan queue:work redis --tries=3 --sleep=1 --max-time=3600')
        F_PG      = @('PostgreSQL 17.11 - reclutamiento, _testing, _e2e', -20000, -47000, 'postgres:17.11-alpine; volumen pgdata')
        F_REDIS   = @('Redis 7.4.11 - sesión, caché, cola', 22000, -32000, 'redis:7.4.11-alpine; volumen redisdata')
        F_FASTAPI = @('recruitment_ml.api.app', 58000, -18000, 'ml-service/src/recruitment_ml/api/app.py')
        F_MODEL   = @('ml-service artifacts (.joblib + metadatos)', 58000, -24000, 'ml-service/artifacts/, no versionado')
    }
    foreach ($key in $files.Keys) {
        $f = New-Obj $m 'FileObject' $files[$key][0] "FL_$key"
        $f.Comment = $files[$key][3]
        $no[$key] = $f; $ns[$key] = $dd.AttachObject($f); Set-Pos $ns[$key] $files[$key][1] $files[$key][2]
    }
    $deSyms = @()
    $deLinks = @(
        @('BROWSER', 'PHP', 'HTTP :8000 · Inertia + JSON'), @('PHP', 'POSTGRES', 'TCP 5432'), @('PHP', 'REDIS', 'TCP 6379'),
        @('QUEUE', 'REDIS', 'TCP 6379'), @('QUEUE', 'POSTGRES', 'TCP 5432'),
        @('PHP', 'PY', 'HTTP host.docker.internal:8008 · POST /v1/predict + X-Internal-Token [ML_SERVICE_ENABLED=true]')
    )
    foreach ($x in $deLinks) {
        $l = $m.CreateObject($PdKind.NodeAssociation); $l.Object1 = $no[$x[0]]; $l.Object2 = $no[$x[1]]; $l.Name = $x[2]
        $deSyms += , @($dd.AttachLinkObject($l, $ns[$x[0]], $ns[$x[1]]), $x[0], $x[1])
    }
    # Fijar los puntos de un vínculo hace que PowerDesigner ajuste el nodo a esos extremos:
    # primero se trazan las rectas y después se restituye el tamaño final de cada nodo.
    foreach ($x in $deSyms) { Set-StraightLink $x[0] $ns[$x[1]] $ns[$x[2]] }
    foreach ($key in $nodes.Keys) { Set-Box $ns[$key] $nodes[$key][2] $nodes[$key][3] $nodes[$key][4] $nodes[$key][5] }
    Add-Note $dd "public/build lo genera npm run build en entrypoint.sh; no hay servidor de frontend separado." -66000 -34000 24000 | Out-Null
    Add-Note $dd "Perfil e2e (app-e2e :8001, queue-e2e, cypress): solo pruebas. Mailer 'log' en desarrollo: sin SMTP ni proveedor. Sin entorno de producción, nube, S3, CDN ni Kubernetes." 14000 -64000 60000 | Out-Null

    Show-LinkNames $pd1; Show-LinkNames $cd; Show-LinkNames $dd
    Export-Diagram $pd1 'PK-01-paquetes'
    Export-Diagram $cd 'CO-01-componentes'
    Export-Diagram $dd 'DE-01-despliegue'
    Save-Model $m $OomFile
    "paquetes=$(@($mod.Packages).Count) componentes=$(@($m.Components).Count) interfaces=$(@($m.Interfaces).Count) nodos=$(@($m.Nodes).Count) archivos=$(@($m.Files).Count)"
    $m.Close()
} catch {
    "ERROR linea $($_.InvocationInfo.ScriptLineNumber): $($_.Exception.Message)"
    "  $($_.InvocationInfo.Line.Trim())"
    if ($m) { try { $m.Close() } catch {} }
} finally { Close-Pd }
