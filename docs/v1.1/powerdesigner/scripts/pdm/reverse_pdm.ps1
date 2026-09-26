# PDM por ingeniería inversa del esquema versionado (models/source/schema-postgresql.sql)
# con el DBMS 'PostgreSQL 9.x' de PowerDesigner 16.6. Crea el modelo desde cero: solo se
# ejecuta para regenerar el PDM; después va finish_pdm.ps1.
$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$sql = Join-Path $repo 'models\source\schema-postgresql.sql'

$pd = New-Object -ComObject 'PowerDesigner.Application'
$orig = $pd.InteractiveMode
$pd.InteractiveMode = 0
try {
    $m = $pd.CreateModel(-840675807, '|DBMS=PostgreSQL 9.x|Diagram=PhysicalDiagram')
    $m.Name = 'SaaS Reclutamiento v1.1 - Modelo fisico'
    $m.Code = 'SAAS_RECLUTAMIENTO_V11_PDM'
    $opt = $m.GetPackageOptions()
    $opt.ReversedScript = $true
    $opt.ReversedFile = $sql
    $m.ReverseDatabase()

    $tables = @($m.Tables)
    $refs = @($m.References)
    $checks = 0; $keys = 0; $idx = 0; $trg = 0
    foreach ($t in $tables) {
        $keys += @($t.Keys).Count
        $idx += @($t.Indexes).Count
        $trg += @($t.Triggers).Count
        if ($t.ServerCheckExpression) { $checks++ }
    }
    "DBMS: $($m.DBMS.Name)"
    "Tablas: $($tables.Count)"
    "Referencias (FK): $($refs.Count)"
    "Claves: $keys · Indices: $idx · Triggers: $trg · Tablas con CHECK de tabla: $checks"
    "Diagramas: $(@($m.PhysicalDiagrams).Count)"
    ($tables | ForEach-Object { $_.Code } | Sort-Object) -join ' '
    $m.Save((Join-Path $repo 'models\saas-recruitment-v1.1-pdm.pdm'))
    "guardado"
    $m.Close()
} finally {
    $pd.InteractiveMode = $orig
    "abiertos: $($pd.Models.Count)"
}
