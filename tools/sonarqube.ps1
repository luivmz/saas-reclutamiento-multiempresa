param(
    [Parameter(Position = 0)]
    [ValidateSet('Preparar', 'Pruebas', 'Frontend', 'Iniciar', 'Analizar', 'Estado', 'Detener', 'Validar')]
    [string]$Accion = 'Estado',
    [ValidateSet('V1', 'V2')][string]$Version = 'V1'
)

$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
$local = Join-Path $repo '.quality'
$compose = Join-Path $repo 'docker-compose.quality.yml'
$localEnv = Join-Path $local 'runtime.env'
$gitCompose = $null
$server = 'http://127.0.0.1:9000'
$project = 'reclutamiento-sonarqube'
New-Item -ItemType Directory -Path $local -Force | Out-Null

function Invoke-Docker {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$DockerArgs)
    & docker @DockerArgs
    if ($LASTEXITCODE -ne 0) { throw "Docker devolvio codigo $LASTEXITCODE. Revisa el mensaje anterior." }
}

function Invoke-QualityCompose {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$ComposeArgs)
    $files = @('-f', $compose)
    if ($gitCompose) { $files += @('-f', $gitCompose) }
    Invoke-Docker compose --env-file $localEnv @files @ComposeArgs
}

function Assert-Engine {
    # Bound the probe: an unresponsive Docker Desktop must not hang this script.
    $start = New-Object System.Diagnostics.ProcessStartInfo
    $start.FileName = (Get-Command docker -ErrorAction Stop).Source
    $start.Arguments = 'info --format {{.ServerVersion}}'
    $start.UseShellExecute = $false
    $start.CreateNoWindow = $true
    $start.RedirectStandardOutput = $true
    $start.RedirectStandardError = $true
    $probe = [System.Diagnostics.Process]::Start($start)
    try {
        if (-not $probe.WaitForExit(10000)) { throw 'Docker no responde. Abre Docker Desktop y espera Engine running; si falla, reinicia Windows.' }
        if ($probe.ExitCode -ne 0) { throw 'Motor Docker no disponible. Abre Docker Desktop y espera Engine running.' }
    } finally { $probe.Dispose() }
}

function Get-SourceHash {
    $files = @(& git ls-files --cached --others --exclude-standard -- app routes resources database config bootstrap public ml-service tests cypress composer.lock package-lock.json phpunit.xml sonar-project.properties)
    # Include the new scanner configuration even before its first commit.
    $files += 'sonar-project.properties'
    $lines = foreach ($file in ($files | Sort-Object -Unique)) {
        if (Test-Path -LiteralPath $file -PathType Leaf) { "$file $((Get-FileHash -LiteralPath $file -Algorithm SHA256).Hash)" }
    }
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try { ([BitConverter]::ToString($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes(($lines -join "`n"))))).Replace('-', '').ToLowerInvariant() }
    finally { $sha.Dispose() }
}

function Write-JsonFile($Value, [string]$Path) {
    $Value | ConvertTo-Json -Depth 40 | Set-Content -LiteralPath $Path -Encoding UTF8
}

function Read-Sonar([string]$Path) {
    Invoke-RestMethod -Uri "$server/$Path" -Headers @{Authorization = "Bearer $env:SONAR_TOKEN"} -TimeoutSec 30
}

if (-not (Test-Path -LiteralPath $localEnv)) {
    $bytes = New-Object byte[] 32
    $random = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    try { $random.GetBytes($bytes) } finally { $random.Dispose() }
    "QUALITY_APP_KEY=base64:$([Convert]::ToBase64String($bytes))" | Set-Content -LiteralPath $localEnv -Encoding ASCII
}

Push-Location $repo
try {
    # JGit does not resolve this Windows worktree correctly inside Linux.
    # Build scanner-only metadata with the real commit, index and shared objects.
    # No source file or ref in the user's original Git repository is modified.
    if (Test-Path -LiteralPath (Join-Path $repo '.git') -PathType Leaf) {
        $common = [IO.Path]::GetFullPath((& git rev-parse --path-format=absolute --git-common-dir).Trim())
        $gitDir = [IO.Path]::GetFullPath((& git rev-parse --absolute-git-dir).Trim())
        $prefix = $common.TrimEnd('\', '/') + [IO.Path]::DirectorySeparatorChar
        if (-not $gitDir.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)) { throw 'La metadata del worktree no pertenece al repositorio esperado.' }
        $snapshot = Join-Path $local 'scanner-repository'
        $snapshotGit = Join-Path $snapshot '.git'
        if (-not (Test-Path -LiteralPath $snapshotGit)) {
            & git init --quiet $snapshot
            if ($LASTEXITCODE -ne 0) { throw 'No se pudo preparar metadata aislada del scanner.' }
        }
        $alternate = Join-Path $snapshotGit 'objects/info/alternates'
        [IO.File]::WriteAllText($alternate, "$($common.Replace('\', '/'))/objects`n", [Text.UTF8Encoding]::new($false))
        $head = (& git rev-parse HEAD).Trim()
        $branch = (& git branch --show-current).Trim()
        if (-not $branch) { throw 'El scanner requiere una rama Git identificable.' }
        & git --git-dir=$snapshotGit --work-tree=$repo update-ref "refs/heads/$branch" $head
        if ($LASTEXITCODE -ne 0) { throw 'No se pudo fijar el commit real para el scanner.' }
        & git --git-dir=$snapshotGit --work-tree=$repo symbolic-ref HEAD "refs/heads/$branch"
        & git --git-dir=$snapshotGit --work-tree=$repo read-tree $head
        if ($LASTEXITCODE -ne 0) { throw 'No se pudo preparar el indice real para el scanner.' }
        & git --git-dir=$snapshotGit config core.worktree /var/www/html
        [IO.File]::WriteAllText($alternate, "/opt/reclutamiento-git/objects`n", [Text.UTF8Encoding]::new($false))
        $pointer = Join-Path $local 'scanner.git'
        [IO.File]::WriteAllText($pointer, "gitdir: /opt/scanner-git`n", [Text.UTF8Encoding]::new($false))
        $commonYaml = $common.Replace('\', '/') | ConvertTo-Json -Compress
        $pointerYaml = $pointer.Replace('\', '/') | ConvertTo-Json -Compress
        $snapshotYaml = $snapshotGit.Replace('\', '/') | ConvertTo-Json -Compress
        $gitCompose = Join-Path $local 'scanner-worktree.yml'
        @"
services:
  scanner:
    volumes:
      - type: bind
        source: $commonYaml
        target: /opt/reclutamiento-git
        read_only: true
      - type: bind
        source: $pointerYaml
        target: /var/www/html/.git
        read_only: true
      - type: bind
        source: $snapshotYaml
        target: /opt/scanner-git
        read_only: true
"@ | Set-Content -LiteralPath $gitCompose -Encoding UTF8
    }
    if ($Accion -eq 'Validar') {
        Invoke-QualityCompose --profile tests --profile sonar config --quiet
        Write-Host 'Configuracion Compose valida. Esto no ejecuta pruebas ni analiza codigo.'
        return
    }
    Assert-Engine
    switch ($Accion) {
        'Preparar' {
            Invoke-Docker build --target base -t reclutamiento-sonar-base:local -f docker/php/Dockerfile .
            Invoke-QualityCompose --profile tests build qa-app
            Invoke-QualityCompose --profile sonar pull sonarqube scanner
            Write-Host 'Imagenes preparadas. Ejecuta Pruebas antes de Analizar.'
        }
        'Pruebas' {
            $proof = Join-Path $local 'tests-proof.json'
            Write-JsonFile @{status = 'RUNNING'; started = (Get-Date).ToString('o')} $proof
            $before = Get-SourceHash
            try {
                Invoke-QualityCompose --profile tests up --detach --wait postgres
                Invoke-QualityCompose --profile tests run --rm qa-app tests 2>&1 | Tee-Object -FilePath (Join-Path $local 'tests.log')
                if ((Get-SourceHash) -ne $before) { throw 'El codigo cambio durante las pruebas. Repite Pruebas.' }
                foreach ($file in @('coverage.xml', 'test-results.xml')) {
                    if (-not (Test-Path -LiteralPath $file)) { throw "No se genero $file" }
                    [xml](Get-Content -LiteralPath $file -Raw) | Out-Null
                }
                Write-JsonFile @{status = 'PASS'; at = (Get-Date).ToString('o'); commit = (& git rev-parse HEAD); sourceHash = $before; coverageHash = (Get-FileHash coverage.xml).Hash; junitHash = (Get-FileHash test-results.xml).Hash} $proof
                Write-Host 'Pruebas correctas; cobertura y JUnit generados de esta ejecucion.'
            } finally {
                # Release RAM before starting SonarQube; preserve the testing volume.
                Invoke-QualityCompose --profile tests stop postgres
            }
        }
        'Frontend' {
            Invoke-QualityCompose --profile tests up --detach --wait postgres
            try { Invoke-QualityCompose --profile tests run --rm qa-app frontend 2>&1 | Tee-Object -FilePath (Join-Path $local 'frontend.log') }
            finally { Invoke-QualityCompose --profile tests stop postgres }
        }
        'Iniciar' {
            Invoke-QualityCompose --profile sonar up --detach sonarqube
            Write-Host "Abre $server cuando el servidor este operativo. Usa tu cuenta local; admin / admin solo sirve antes del primer cambio de clave."
        }
        'Analizar' {
            $proofPath = Join-Path $local 'tests-proof.json'
            if (-not (Test-Path -LiteralPath $proofPath)) { throw 'Primero ejecuta Pruebas para generar cobertura real.' }
            $proof = Get-Content -LiteralPath $proofPath -Raw | ConvertFrom-Json
            if ($proof.status -ne 'PASS' -or $proof.sourceHash -ne (Get-SourceHash)) { throw 'Pruebas ausentes, fallidas o de otro codigo. Repite Pruebas.' }
            if ($proof.coverageHash -ne (Get-FileHash coverage.xml).Hash -or $proof.junitHash -ne (Get-FileHash test-results.xml).Hash) { throw 'Los reportes cambiaron despues de las pruebas.' }
            $baselinePath = Join-Path $local 'baseline.json'
            if ($Version -eq 'V2' -and -not (Test-Path -LiteralPath $baselinePath)) { throw 'Falta el analisis V1 y su linea base. No se puede simular la comparacion.' }
            if (Test-Path -LiteralPath $baselinePath) {
                $baseline = Get-Content -LiteralPath $baselinePath -Raw | ConvertFrom-Json
                if ($Version -eq 'V1' -and $baseline.sourceHash -ne $proof.sourceHash) { throw 'La linea base V1 ya existe para otro codigo. Conserva esa evidencia y usa V2.' }
                if ($Version -eq 'V2' -and $baseline.sourceHash -eq $proof.sourceHash) { throw 'V2 tiene el mismo codigo que V1. Primero aplica y verifica las mejoras.' }
            }
            $status = Invoke-RestMethod -Uri "$server/api/system/status" -TimeoutSec 10
            if ($status.status -ne 'UP') { throw 'SonarQube todavia no esta operativo.' }
            $previousToken = $env:SONAR_TOKEN
            try {
                if (-not $env:SONAR_TOKEN) {
                    $secure = Read-Host 'Token de tu SonarQube local (oculto; no se guardara)' -AsSecureString
                    $pointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
                    try { $env:SONAR_TOKEN = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($pointer) }
                    finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($pointer) }
                }
                $folder = Join-Path $local ("evidencias/{0}-{1}" -f $Version, (Get-Date -Format 'yyyyMMdd-HHmmssfff'))
                New-Item -ItemType Directory -Path $folder -Force | Out-Null
                $number = if ($Version -eq 'V1') { '1.0' } else { '2.0' }
                Invoke-QualityCompose --profile sonar run --rm --no-deps scanner "-Dsonar.projectVersion=$number" '-Dsonar.qualitygate.wait=false' '-Dsonar.working.directory=/var/www/html/.scannerwork' 2>&1 | Tee-Object -FilePath (Join-Path $folder 'scanner.log')
                $taskFile = Join-Path $repo '.scannerwork/report-task.txt'
                if (-not (Test-Path -LiteralPath $taskFile)) { throw 'El scanner no genero report-task.txt.' }
                $task = Get-Content -LiteralPath $taskFile -Raw | ConvertFrom-StringData
                if ($task.projectKey -ne $project -or $task.ceTaskId -notmatch '^[A-Za-z0-9_-]+$') { throw 'El reporte del scanner no corresponde a este proyecto.' }
                $deadline = (Get-Date).AddMinutes(5)
                do {
                    $ce = Read-Sonar "api/ce/task?id=$($task.ceTaskId)"
                    if ($ce.task.status -eq 'SUCCESS') { break }
                    if ($ce.task.status -in @('FAILED', 'CANCELED')) { throw 'SonarQube no pudo procesar el analisis. Revisa el servidor.' }
                    if ((Get-Date) -gt $deadline) { throw 'El procesamiento sigue pendiente. No se declararan metricas finales.' }
                    Start-Sleep -Seconds 3
                } while ($true)
                $metrics = 'security_rating,reliability_rating,sqale_rating,software_quality_security_rating,software_quality_reliability_rating,software_quality_maintainability_rating,software_quality_security_issues,software_quality_reliability_issues,software_quality_maintainability_issues,security_hotspots,security_hotspots_reviewed,coverage,line_coverage,duplicated_lines_density,violations,cognitive_complexity,sqale_index,ncloc,bugs,vulnerabilities,code_smells'
                $measures = Read-Sonar "api/measures/component?component=$project&metricKeys=$metrics"
                $lines = @($measures.component.measures | Where-Object metric -eq 'ncloc')
                if ($lines.Count -ne 1 -or [double]$lines[0].value -le 0) { throw 'Analisis invalido: no se contabilizo codigo propio. No se guardara como linea base.' }
                $gate = Read-Sonar "api/qualitygates/project_status?analysisId=$($ce.task.analysisId)"
                Write-JsonFile $measures (Join-Path $folder 'measures.json')
                Write-JsonFile $gate (Join-Path $folder 'quality-gate.json')
                $issues = @()
                $page = 1
                do {
                    $result = Read-Sonar "api/issues/search?componentKeys=$project&ps=500&p=$page"
                    $issues += @($result.issues)
                    $page++
                } while ($issues.Count -lt $result.paging.total)
                Write-JsonFile $issues (Join-Path $folder 'issues.json')
                $hotspots = @()
                $page = 1
                do {
                    $result = Read-Sonar "api/hotspots/search?projectKey=$project&ps=500&p=$page"
                    $hotspots += @($result.hotspots)
                    $page++
                } while ($hotspots.Count -lt $result.paging.total)
                Write-JsonFile $hotspots (Join-Path $folder 'hotspots.json')
                Copy-Item -LiteralPath coverage.xml, test-results.xml, sonar-project.properties -Destination $folder
                Copy-Item -LiteralPath (Join-Path $local 'tests.log') -Destination $folder
                $manifest = @{status = 'ANALYZED'; version = $Version; at = (Get-Date).ToString('o'); commit = (& git rev-parse HEAD); sourceHash = $proof.sourceHash; analysisId = $ce.task.analysisId; serverVersion = $status.version; qualityGate = $gate.projectStatus.status; evidence = $folder; gitStatus = @(& git status --short)}
                Write-JsonFile $manifest (Join-Path $folder 'manifest.json')
                if ($Version -eq 'V1' -and -not (Test-Path -LiteralPath $baselinePath)) { Write-JsonFile $manifest $baselinePath }
                Write-Host "Analisis real completado. Quality Gate: $($gate.projectStatus.status). Evidencia: $folder"
                Write-Host "Abre $server/dashboard?id=$project y guarda capturas de Dashboard, Quality Gate, Measures, Issues y Coverage."
            } finally { $env:SONAR_TOKEN = $previousToken }
        }
        'Estado' {
            Invoke-QualityCompose --profile tests --profile sonar ps -a
            try { Invoke-RestMethod -Uri "$server/api/system/status" -TimeoutSec 5 | Format-Table }
            catch { Write-Host 'SonarQube no responde todavia.' }
        }
        'Detener' {
            # No down -v, volume deletion, factory reset or changes to other Compose projects.
            Invoke-QualityCompose --profile tests --profile sonar stop
        }
    }
} finally { Pop-Location }
