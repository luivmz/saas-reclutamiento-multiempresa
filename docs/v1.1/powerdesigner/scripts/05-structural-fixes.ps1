# Ajustes incrementales sobre el OOM ya construido (no lo reconstruye).
# - Quita el diagrama de clases vacío que PowerDesigner crea en la raíz con el modelo.
# - Dependencias sin rótulo en F22: nombre en blanco, para que con los nombres de
#   dependencia visibles no aparezca el automático (Dependency_N).
# - Reexporta UC-01, PK-01 y CO-01.
# Los scripts 02 y 03 ya aplican lo mismo al crear; este script lleva el modelo
# existente al mismo estado sin volver a crearlo.
. "$PSScriptRoot\pdlib.ps1"

Open-Pd
try {
    $m = $Pd.OpenModel($OomFile)

    $root = @($m.ClassDiagrams) | Where-Object { $_.Name -eq 'ClassDiagram_1' }
    foreach ($d in $root) {
        if (@($d.Symbols).Count -eq 0) { $d.Delete(); 'eliminado ClassDiagram_1 (vacío)' } else { 'ClassDiagram_1 tiene símbolos: se conserva' }
    }

    $n = 0
    $deps = @($m.Dependencies)
    foreach ($p in @($m.Packages)) { $deps += @($p.Dependencies) }
    foreach ($dep in $deps) { if ($dep.Name -like 'Dependency_*') { $dep.Name = $BlankName; $n++ } }
    "dependencias con nombre automático en blanco: $n"

    foreach ($x in @(@('UC-01 Casos de uso AS-IS v1.1', 'UC-01-casos-de-uso'), @('PK-01 Paquetes del monolito', 'PK-01-paquetes'), @('CO-01 Componentes AS-IS v1.1', 'CO-01-componentes'))) {
        $d = Find-Diagram $m $x[0]
        if (-not $d) { throw "no se encontró el diagrama $($x[0])" }
        Export-Diagram $d $x[1]
        "exportado $($x[1])"
    }

    Save-Model $m $OomFile
    'guardado'
    $m.Close()
} catch {
    "ERROR linea $($_.InvocationInfo.ScriptLineNumber): $($_.Exception.Message)"
    "  $($_.InvocationInfo.Line.Trim())"
    if ($m) { try { $m.Close() } catch {} }
} finally { Close-Pd }
