# Exporta DOCX a PDF con Microsoft Word actualizando antes las tablas de contenido y los campos (F29D, F29H).
# Uso: powershell -ExecutionPolicy Bypass -File topdf_toc.ps1 <ruta.docx> [<ruta.docx> ...]
# El DOCX se abre en solo lectura y no se guarda: la actualización solo afecta al PDF.
param([Parameter(Mandatory = $true, ValueFromRemainingArguments = $true)][string[]]$Files)
$ErrorActionPreference = 'Stop'
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    foreach ($f in $Files) {
        $in = (Resolve-Path $f).Path
        $out = [System.IO.Path]::ChangeExtension($in, '.pdf')
        $doc = $word.Documents.Open($in, $false, $true)
        $doc.Fields.Update() | Out-Null
        foreach ($toc in $doc.TablesOfContents) { $toc.Update() }
        $doc.Repaginate()
        foreach ($toc in $doc.TablesOfContents) { $toc.UpdatePageNumbers() }
        $pages = $doc.ComputeStatistics(2)
        $doc.SaveAs2($out, 17)
        $doc.Close(0)
        Write-Output ("OK {0} ({1} paginas)" -f $out, $pages)
    }
}
finally {
    $word.Quit()
}
