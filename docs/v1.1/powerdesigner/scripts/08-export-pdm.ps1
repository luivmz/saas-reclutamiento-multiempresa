# Exporta PDM-01 y PDM-02 en PNG y SVG desde el PDM existente, sin modificarlo.
. "$PSScriptRoot\pdlib.ps1"

Open-Pd
try {
    $m = $Pd.OpenModel((Join-Path $PdModels 'saas-recruitment-v1.1-pdm.pdm'))
    foreach ($d in @($m.PhysicalDiagrams)) {
        switch -Wildcard ($d.Name) {
            'PDM-01*' { Export-Diagram $d 'PDM-01-esquema-completo'; "PDM-01 exportado" }
            'PDM-02*' { Export-Diagram $d 'PDM-02-tablas-de-dominio'; "PDM-02 exportado" }
        }
    }
    "tablas=$(@($m.Tables).Count) referencias=$(@($m.References).Count)"
    $m.Close()
} catch {
    "ERROR linea $($_.InvocationInfo.ScriptLineNumber): $($_.Exception.Message)"
    if ($m) { try { $m.Close() } catch {} }
} finally { Close-Pd }
