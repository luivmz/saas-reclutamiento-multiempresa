# Quita los diagramas vacíos que PowerDesigner crea por defecto al crear un paquete
# (ClassDiagram_1, UseCaseDiagram_1...). Solo borra diagramas sin símbolos y con nombre
# por defecto; si PowerDesigner exige conservar el último diagrama de un paquete, lo deja.
. "$PSScriptRoot\pdlib.ps1"

function Remove-Empty($container, [string]$path) {
    $n = 0
    foreach ($col in 'ClassDiagrams', 'UseCaseDiagrams', 'ComponentDiagrams', 'DeploymentDiagrams', 'SequenceDiagrams', 'ActivityDiagrams', 'StatechartDiagrams', 'PackageDiagrams') {
        $ds = @()
        try { $ds = @($container.GetCollectionByName($col) | Where-Object { $_ }) } catch {}
        foreach ($d in $ds) {
            if (@($d.Symbols).Count -eq 0 -and $d.Name -match '^(Class|UseCase|Component|Deployment|Sequence|Activity|Statechart|Package)Diagram_\d+$') {
                try { $d.Delete(); $n++; Write-Host "  eliminado: $path / $($d.Name)" } catch { Write-Host "  se conserva: $path / $($d.Name) ($($_.Exception.Message))" }
            }
        }
    }
    foreach ($p in @($container.Packages)) { if ($p) { $n += Remove-Empty $p ($path + '/' + $p.Name) } }
    $n
}

Open-Pd
try {
    $m = $Pd.OpenModel($OomFile)
    $n = Remove-Empty $m '(raíz)'
    "diagramas vacíos eliminados: $n"
    Save-Model $m $OomFile
    $m.Close()
} catch {
    "ERROR linea $($_.InvocationInfo.ScriptLineNumber): $($_.Exception.Message)"
    if ($m) { try { $m.Close() } catch {} }
} finally { Close-Pd }
