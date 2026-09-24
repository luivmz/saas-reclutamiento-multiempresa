param([Parameter(Mandatory)][string]$Script, [int]$Timeout = 600)
# Guarda los .ps1 de la carpeta de scripts con BOM (PowerShell 5.1 los lee como ANSI sin
# BOM) y ejecuta el indicado en un proceso aparte con límite de tiempo.
# Uso: tools\run-pd.ps1 -Script 04-sequences.ps1   ($env:PD_ONLY limita los diagramas)
$dir = Split-Path -Parent $PSScriptRoot
foreach ($f in Get-ChildItem $dir -Filter *.ps1 -Recurse) {
    $bytes = [IO.File]::ReadAllBytes($f.FullName)
    if (-not ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF)) {
        $txt = [IO.File]::ReadAllText($f.FullName, [Text.Encoding]::UTF8)
        [IO.File]::WriteAllText($f.FullName, $txt, (New-Object Text.UTF8Encoding($true)))
    }
}
$path = Join-Path $dir $Script
$job = Start-Job -ScriptBlock { param($p) & $p } -ArgumentList $path
if (Wait-Job $job -Timeout $Timeout) { Receive-Job $job 2>&1 } else { "TIMEOUT tras $Timeout s"; Stop-Job $job }
Remove-Job $job -Force
