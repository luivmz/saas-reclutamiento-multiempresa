# F31 - ajuste incremental de rotulos en ARQ-01.
#
# No reconstruye la vista ni cambia componentes, relaciones o rutas. Aplica a los
# DependencySymbol existentes los mismos offsets declarados por el generador F29,
# guarda, reabre y vuelve a exportar para comprobar persistencia y reproducibilidad.

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'f29lib.ps1')
. (Join-Path $PSScriptRoot 'f31-arq01-label-layout.ps1')

$offsets = @{}
foreach ($id in $ArqLabelOffsets.Keys) { $offsets['ARQ01_' + ($id -replace '-', '_')] = $ArqLabelOffsets[$id] }

Open-F29
try {
    $m = Get-F29Model $F29Oom
    $d = Find-F29Diagram $m 'ARQ01' 'ARQ-01 - Arquitectura Conceptual'
    $seen = @{}
    foreach ($s in (Get-C $d 'Symbols')) {
        $o = $null
        try { $o = Get-P $s 'Object' } catch {}
        if (-not $o) { continue }
        $code = [string](Get-P $o 'Code')
        if (-not $offsets.ContainsKey($code)) { continue }
        $off = $offsets[$code]
        $id = $code -replace '^ARQ01_', '' -replace '_', '-'
        if ($ArqLabelText.ContainsKey($id)) { $o.Name = $ArqLabelText[$id] }
        $s.SetAttribute('CenterTextOffset', $Pd.NewPoint([int]$off[0], [int]$off[1])) | Out-Null
        $seen[$code] = $true
    }
    $missing = @($offsets.Keys | Where-Object { -not $seen.ContainsKey($_) })
    if ($missing.Count) { throw 'Dependencias sin simbolo: ' + ($missing -join ', ') }

    $pub = Publish-F29View $m 'ARQ01' 'ARQ-01 - Arquitectura Conceptual' 'ARQ-01_Arquitectura_Conceptual' @()
    $lines = @('F31 - ajuste incremental de rotulos ARQ-01 (' + (Get-Date -Format 'yyyy-MM-dd HH:mm') + ')')
    $lines += 'Dependencias ajustadas: ' + $seen.Count
    $lines += $pub.Lines
    $lines += $(if ($pub.Ok) { 'RESULTADO: PASS' } else { 'RESULTADO: FAIL' })
    Write-F29Report (Join-Path (Join-Path $F29Root 'validation') 'F31_ARQ01_label_cleanup.txt') $lines
    $pub.Model.Close() | Out-Null
    if (-not $pub.Ok) { throw 'La vista no fue estable tras guardar y reabrir' }
}
finally {
    Close-F29
}
