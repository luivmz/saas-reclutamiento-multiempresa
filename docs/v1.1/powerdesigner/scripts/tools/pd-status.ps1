param([switch]$CloseMine)
# Estado de PowerDesigner: modelos abiertos. Con -CloseMine cierra, sin guardar y en modo
# batch, solo los modelos de la Fase 23 (SaaS Reclutamiento v1.1*) o de prueba (zz_*).
# Conviene ejecutarlo antes de cada script: un modelo ya abierto hace que OpenModel
# devuelva la instancia en memoria en lugar del archivo.
$pd = New-Object -ComObject 'PowerDesigner.Application'
$orig = $pd.InteractiveMode
try {
    "modelos abiertos: $($pd.Models.Count)"
    foreach ($m in @($pd.Models)) {
        "  - $($m.Name) | $($m.FileName)"
        if ($CloseMine -and ($m.Name -like 'zz_*' -or $m.Name -like 'SaaS Reclutamiento v1.1*')) {
            $pd.InteractiveMode = 0
            $m.Close()
            "    cerrado"
        }
    }
} finally { $pd.InteractiveMode = $orig }
