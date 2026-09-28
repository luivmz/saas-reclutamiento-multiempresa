# Capturas reales de la ventana de PowerDesigner 16.6 (integración posterior a la F29).
#
# Uso, desde la raíz del repositorio, en PowerShell y con PowerDesigner abierto:
#   . .\docs\academico\powerdesigner\scripts\f29lib.ps1
#   . .\docs\academico\powerdesigner\scripts\capture_f29_views.ps1
#   Save-F29Captures
#
# Qué hace, sin modificar los modelos:
#   1. Cierra los dos modelos de la F29 si están abiertos (se niega si tienen cambios sin guardar) y los vuelve a
#      abrir desde el disco, para que la captura muestre el estado guardado.
#   2. Para cada vista: abre el diagrama, la ajusta al lienzo (F8 «Global View» y luego CenterAndScaleView con la
#      escala que cabe en el lienzo, o un símbolo y una escala fijos para las dos partes del F5), quita la
#      selección, localiza el diagrama en el Object Browser y captura la ventana principal con PrintWindow.
#   3. Comprueba que ningún modelo quedó modificado. Nunca guarda.
#
# La captura es la ventana real de PowerDesigner (título con la ruta del modelo, Object Browser y pestaña del
# diagrama): no se dibuja ni se retoca nada.

if (-not ('F29Win' -as [type])) {
    Add-Type -AssemblyName System.Drawing
    Add-Type @"
using System; using System.Text; using System.Collections.Generic; using System.Runtime.InteropServices;
public class F29Win {
 public delegate bool EnumProc(IntPtr h, IntPtr l);
 [DllImport("user32.dll")] public static extern bool EnumChildWindows(IntPtr p, EnumProc f, IntPtr l);
 [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
 [DllImport("user32.dll")] public static extern int GetClassName(IntPtr h, StringBuilder s, int n);
 [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
 [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr hdc, uint f);
 [DllImport("user32.dll")] public static extern bool PostMessage(IntPtr h, uint m, IntPtr w, IntPtr l);
 public struct RECT { public int L, T, R, B; }
 public static List<IntPtr> Kids(IntPtr p) { var l = new List<IntPtr>(); EnumChildWindows(p, (h, x) => { l.Add(h); return true; }, IntPtr.Zero); return l; }
 public static string Cls(IntPtr h) { var s = new StringBuilder(256); GetClassName(h, s, 256); return s.ToString(); }
}
"@
}

# Píxeles por unidad de PowerDesigner y por punto de escala, medido en esta pantalla (escala 16 % -> 971 px para
# 456 000 unidades). Solo sirve para elegir la escala que cabe en el lienzo.
$Global:F29PxPerUnit = 1.331e-4

function Send-F29Key($hwnd, [int]$vk) {
    [F29Win]::PostMessage($hwnd, 0x100, [IntPtr]$vk, [IntPtr]1) | Out-Null
    [F29Win]::PostMessage($hwnd, 0x101, [IntPtr]$vk, [IntPtr]0xC0000001) | Out-Null
}

function Get-F29Canvas($main) {
    # El lienzo del diagrama es la ventana visible más grande de clase S_Window.
    $best = $null; $area = 0
    foreach ($k in [F29Win]::Kids($main)) {
        if (-not [F29Win]::IsWindowVisible($k) -or [F29Win]::Cls($k) -ne 'S_Window') { continue }
        $r = New-Object F29Win+RECT; [F29Win]::GetWindowRect($k, [ref]$r) | Out-Null
        $a = ($r.R - $r.L) * ($r.B - $r.T)
        if ($a -gt $area) { $area = $a; $best = @{ H = $k; W = $r.R - $r.L; Ht = $r.B - $r.T } }
    }
    $best
}

function Find-F29SymbolDeep($symbols, [scriptblock]$test) {
    foreach ($sy in $symbols) {
        $ob = $null; try { $ob = Get-P $sy 'Object' } catch {}
        if ($ob -and (& $test $sy $ob)) { $sy }
        $sub = $null; try { $sub = Get-C $sy 'SubSymbols' } catch {}
        if ($sub -and $sub.Count) { Find-F29SymbolDeep $sub $test }
    }
}

function Save-F29Capture($model, [string]$pkg, [string]$diagram, [string]$out, [string]$centerCode = '', [int]$scale = 0, [double]$fill = 0.94) {
    $d = Find-F29Diagram $model $pkg $diagram
    if (-not $d) { throw "Diagrama no encontrado: $diagram" }
    $Pd.InteractiveMode = $PdOrigMode
    $d.OpenView() | Out-Null
    Start-Sleep -Milliseconds 1200
    $main = [IntPtr]$Pd.MainWindowHandle
    # Espera a que la ventana y el lienzo tengan un tamaño estable (PowerDesigner puede redimensionar la ventana
    # principal al abrir la primera vista tras reabrir los modelos).
    $cv = $null; $prev = ''
    for ($i = 0; $i -lt 20; $i++) {
        Start-Sleep -Milliseconds 500
        $wr = New-Object F29Win+RECT; [F29Win]::GetWindowRect($main, [ref]$wr) | Out-Null
        $cv = Get-F29Canvas $main
        $now = "$($wr.R - $wr.L)x$($wr.B - $wr.T)/$($cv.W)x$($cv.Ht)"
        if ($now -eq $prev -and $cv.W -gt 400) { break }
        $prev = $now
    }
    if (-not $cv -or $cv.W -lt 800 -or $cv.Ht -lt 500) {
        throw "La ventana de PowerDesigner está minimizada o es demasiado pequeña ($prev): maximícela y repita."
    }
    Send-F29Key $cv.H 0x77                                   # F8: Global View
    Start-Sleep -Milliseconds 800
    if ($centerCode) {
        $target = @(Find-F29SymbolDeep (Get-C $d 'Symbols') { param($sy, $ob) (Get-P $ob 'Code') -eq $centerCode })[0]
        if (-not $target) { throw "Símbolo no encontrado: $centerCode" }
    } else {
        # Escala que hace caber el rectángulo usado en el lienzo, centrada en el símbolo más próximo a su centro.
        $u = $d.GetUsedRectangle()
        $l = Get-P $u 'Left'; $r = Get-P $u 'Right'; $t = Get-P $u 'Top'; $b = Get-P $u 'Bottom'
        $scale = [int][math]::Floor($fill * [math]::Min(($cv.W - 20) / ([math]::Abs($r - $l) * $F29PxPerUnit),
                                                         ($cv.Ht - 20) / ([math]::Abs($t - $b) * $F29PxPerUnit)))
        $mx = ($l + $r) / 2; $my = ($t + $b) / 2
        $cands = @(Find-F29SymbolDeep (Get-C $d 'Symbols') { param($sy, $ob) (Get-P $sy 'ClassName') -notmatch 'Pool|Lane|Swimlane|Flow|Link|Association|Dependency|Package' })
        $target = $cands | Sort-Object { $c = Get-Center $_; [math]::Pow($c[0] - $mx, 2) + [math]::Pow($c[1] - $my, 2) } | Select-Object -First 1
    }
    $d.CenterAndScaleView($target, $scale) | Out-Null
    Start-Sleep -Milliseconds 800
    # Clic en el fondo del lienzo y Esc: quitan la selección que deja CenterAndScaleView.
    $lp = [IntPtr]((12 -shl 16) -bor 12)
    [F29Win]::PostMessage($cv.H, 0x201, [IntPtr]1, $lp) | Out-Null; Start-Sleep -Milliseconds 150
    [F29Win]::PostMessage($cv.H, 0x202, [IntPtr]0, $lp) | Out-Null
    Send-F29Key $cv.H 0x1B
    Start-Sleep -Milliseconds 500
    $Pd.ActiveWorkspace.SelectObject($d) | Out-Null           # localiza el diagrama en el Object Browser
    Start-Sleep -Milliseconds 1500
    $wr = New-Object F29Win+RECT; [F29Win]::GetWindowRect($main, [ref]$wr) | Out-Null
    $bmp = New-Object System.Drawing.Bitmap ($wr.R - $wr.L), ($wr.B - $wr.T)
    $g = [System.Drawing.Graphics]::FromImage($bmp); $hdc = $g.GetHdc()
    [F29Win]::PrintWindow($main, $hdc, 2) | Out-Null
    $g.ReleaseHdc($hdc); $g.Dispose()
    $bmp.Save($out, [System.Drawing.Imaging.ImageFormat]::Png); $bmp.Dispose()
    $d.CloseView() | Out-Null
    $Pd.InteractiveMode = 0
    "captura $out · escala $scale · modelo modificado: $($model.Modified)"
}

function Save-F29Captures([string]$outDir = (Join-Path $F29Root 'evidencias\capturas')) {
    Open-F29
    try {
        foreach ($m in @($Pd.Models)) {
            $f = [System.IO.Path]::GetFullPath($m.FileName)
            if ($f -in @([System.IO.Path]::GetFullPath($F29Bpm), [System.IO.Path]::GetFullPath($F29Oom))) {
                if ($m.Modified) { throw "El modelo $f tiene cambios sin guardar: no se cierra." }
                $m.Close() | Out-Null
            }
        }
        $bpm = Get-F29Model $F29Bpm
        $oom = Get-F29Model $F29Oom
        Save-F29Capture $bpm 'F3' 'F3 - BPMN AS-IS' (Join-Path $outDir 'F3_BPMN_ASIS_PowerDesigner.png')
        Save-F29Capture $bpm 'F3' 'SP-01 Evaluar al candidato — detalle' (Join-Path $outDir 'F3_SP-01_detalle_PowerDesigner.png') -fill 0.8
        Save-F29Capture $bpm 'F5' 'F5 - BPMN TO-BE' (Join-Path $outDir 'F5_BPMN_TOBE_PowerDesigner_parte1.png') 'F5_TB_09' 64
        Save-F29Capture $bpm 'F5' 'F5 - BPMN TO-BE' (Join-Path $outDir 'F5_BPMN_TOBE_PowerDesigner_parte2.png') 'F5_EFP_03' 64
        Save-F29Capture $bpm 'F5' 'SP-P Gestionar la postulación — detalle' (Join-Path $outDir 'F5_SP-P_detalle_PowerDesigner.png')
        Save-F29Capture $oom 'F8' 'F8 - Casos de Uso Academicos' (Join-Path $outDir 'F8_Casos_de_Uso_PowerDesigner.png')
        Save-F29Capture $oom 'ARQ01' 'ARQ-01 - Arquitectura Conceptual' (Join-Path $outDir 'ARQ01_Arquitectura_Conceptual_PowerDesigner.png') -fill 0.85
        foreach ($m in @($bpm, $oom)) { if ($m.Modified) { throw "El modelo $($m.FileName) quedó modificado." } }
    } finally { Close-F29 }
}
