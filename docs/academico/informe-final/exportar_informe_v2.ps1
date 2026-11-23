# Actualiza y guarda campos de Word antes de exportar el mismo documento a PDF.
param(
    [string]$Docx = (Join-Path $PSScriptRoot 'F29H_Informe_Final_v2_Colegio_Andino.docx')
)
$ErrorActionPreference = 'Stop'
$inputPath = (Resolve-Path -LiteralPath $Docx).Path
$pdfPath = [IO.Path]::ChangeExtension($inputPath, '.pdf')
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$doc = $null
try {
    $doc = $word.Documents.Open($inputPath, $false, $false)
    if ($doc.ReadOnly) { throw 'El DOCX se abrio en solo lectura.' }
    $doc.Fields.Update() | Out-Null
    $doc.Repaginate()
    foreach ($table in $doc.TablesOfContents) { $table.Update() }
    foreach ($table in $doc.TablesOfFigures) { $table.Update() }
    $doc.Repaginate()
    foreach ($table in $doc.TablesOfContents) { $table.UpdatePageNumbers() }
    foreach ($table in $doc.TablesOfFigures) { $table.UpdatePageNumbers() }
    $doc.Save()
    $doc.ExportAsFixedFormat($pdfPath, 17, $false, 0, 0, 1, 1, 0, $true, $true, 1)
    Write-Output ("Word {0} | {1} paginas | {2}" -f $word.Version, $doc.ComputeStatistics(2), $pdfPath)
} finally {
    if ($null -ne $doc) { $doc.Close(0) }
    $word.Quit()
}
