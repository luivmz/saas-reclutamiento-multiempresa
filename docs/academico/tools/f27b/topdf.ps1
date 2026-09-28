# Exporta DOCX a PDF con Microsoft Word (la herramienta que ya usó la Fase 24 para el Formato 09).
# Uso: powershell -ExecutionPolicy Bypass -File topdf.ps1 <ruta.docx> [<ruta.docx> ...]
# El PDF se escribe junto al DOCX. Si Word no puede abrir el archivo, el script falla.
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
        $pages = $doc.ComputeStatistics(2)
        $doc.SaveAs2($out, 17)
        $doc.Close(0)
        Write-Output ("OK {0} ({1} paginas)" -f $out, $pages)
    }
}
finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
