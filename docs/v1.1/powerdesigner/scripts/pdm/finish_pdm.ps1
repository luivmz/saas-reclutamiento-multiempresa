# Completa el PDM recién importado: restituye los CHECK y documenta el índice parcial
# (JSON de extract_checks.py), crea PDM-01 y PDM-02 y los exporta en PNG y SVG.
# Uso: finish_pdm.ps1 -Checks <ruta del JSON>
param([Parameter(Mandatory)][string]$Checks)
$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$data = Get-Content $Checks -Raw -Encoding UTF8 | ConvertFrom-Json
$domain = @('organizations','users','job_requests','job_request_status_histories','vacancies','job_profiles',
            'evaluation_criteria','candidate_profiles','candidate_documents','applications','application_stage_histories',
            'evaluations','evaluation_results','interviews','interview_results','selection_decisions','audit_logs')

$pd = New-Object -ComObject 'PowerDesigner.Application'
$orig = $pd.InteractiveMode
$pd.InteractiveMode = 0
try {
    $m = $pd.OpenModel((Join-Path $repo 'models\saas-recruitment-v1.1-pdm.pdm'))
    $m.Comment = 'Modelo fisico obtenido por ingenieria inversa del esquema real (pg_dump --schema-only de develop 2621bee, PostgreSQL 17.11) con el DBMS PostgreSQL 9.x de PowerDesigner 16.6. Fuente: models/source/schema-postgresql.sql. No sustituye al modelo de clases CL-01 (OOM).'

    # CHECK: el importador PG9 conserva uno por tabla; se restituye la conjuncion de todos.
    $restored = 0
    foreach ($prop in $data.checks.PSObject.Properties) {
        $t = @($m.Tables) | Where-Object { $_.Code -eq $prop.Name } | Select-Object -First 1
        $items = @($prop.Value)
        $t.ServerCheckExpression = ($items | ForEach-Object { '(' + $_.expr + ')' }) -join "`r`nAND "
        $names = ($items | ForEach-Object { $_.name }) -join ', '
        $t.Comment = "Restricciones CHECK de la base ($($items.Count)): $names. El importador PostgreSQL 9.x conserva una sola por tabla; aqui se restituye su conjuncion (AND), que es equivalente."
        $restored += $items.Count
    }
    "CHECK restituidos: $restored en $(@($data.checks.PSObject.Properties).Count) tablas"

    # Indice parcial
    $pi = $data.partial_index
    $tbl = @($m.Tables) | Where-Object { $_.Code -eq $pi.table } | Select-Object -First 1
    $ix = @($tbl.Indexes) | Where-Object { $_.Code -eq $pi.name } | Select-Object -First 1
    $ix.Comment = "Indice unico PARCIAL: UNIQUE ($($pi.column)) WHERE $($pi.where). Como mucho una postulacion 'seleccionado' por vacante (RF-24). El importador PostgreSQL 9.x de PowerDesigner no conserva la clausula WHERE; se registra aqui."
    "Indice parcial documentado: $($ix.Code)"

    # Diagramas
    $full = $m.PhysicalDiagrams.Item(0)
    $full.Name = 'PDM-01 Esquema completo'
    $full.Code = 'PDM_01'
    $full.AutoLayout()

    $dom = $m.PhysicalDiagrams.CreateNew()
    $dom.Name = 'PDM-02 Tablas de dominio'
    $dom.Code = 'PDM_02'
    $syms = @{}
    foreach ($t in @($m.Tables)) {
        if ($domain -contains $t.Code) { $syms[$t.Code] = $dom.AttachObject($t) }
    }
    $links = 0
    foreach ($r in @($m.References)) {
        $p = $r.ParentTable.Code; $c = $r.ChildTable.Code
        if ($syms.ContainsKey($p) -and $syms.ContainsKey($c)) {
            $dom.AttachLinkObject($r, $syms[$c], $syms[$p]) | Out-Null; $links++
        }
    }
    $dom.AutoLayout()
    "PDM-02: tablas=$($syms.Count) referencias=$links"

    foreach ($ext in 'png', 'svg') {
        $full.ExportImage((Join-Path $repo "exports\PDM-01-esquema-completo.$ext"))
        $dom.ExportImage((Join-Path $repo "exports\PDM-02-tablas-de-dominio.$ext"))
    }

    $m.Save()
    'guardado'
    $m.Close()
} finally {
    $pd.InteractiveMode = $orig
    "abiertos: $($pd.Models.Count)"
}
