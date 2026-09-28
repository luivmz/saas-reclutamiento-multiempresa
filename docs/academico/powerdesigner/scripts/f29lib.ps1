# Biblioteca común de la Fase 29 (formalización académica en PowerDesigner).
#
# Maneja PowerDesigner 16.6 por COM, igual que los scripts de la F23
# (docs/v1.1/powerdesigner/scripts/pdlib.ps1), pero con rutas propias: SOLO toca
# los dos modelos de la F29 y escribe SOLO en docs/academico/powerdesigner/exports.
# Los modelos y exportaciones de la F23 no se abren ni se modifican.
#
# Reglas:
#   - InteractiveMode = 0 durante la construcción y se restaura al salir.
#   - Cada vista vive en un paquete propio (F3, F5, ...) que se borra y se vuelve a
#     generar entero: el script es reproducible y no deja restos.
#   - Las unidades organizativas (pools y carriles) son objetos del modelo (BPM no
#     admite unidades organizativas dentro de paquetes) y se reutilizan por nombre.
#
# Uso (PowerShell, en la raíz del repositorio):
#   . .\docs\academico\powerdesigner\scripts\f29lib.ps1
#   . .\docs\academico\powerdesigner\scripts\f29-f3-bpmn-asis.ps1

$ErrorActionPreference = 'Stop'

$Global:F29Root = Split-Path -Parent $PSScriptRoot
$Global:F29Models = Join-Path $F29Root 'models'
$Global:F29Exports = Join-Path $F29Root 'exports'
$Global:F29Scripts = $PSScriptRoot
$Global:F29Bpm = Join-Path $F29Models 'F29_BPM_Academico.bpm'
$Global:F29Oom = Join-Path $F29Models 'F29_UML_Academico.oom'

# Clases (Ole Automation\VBScriptConstants.vbs, PowerDesigner 16.6.1).
$Global:BpmKind = @{
    Package = 1027358877; Process = -764527244; Start = -764527236; End = -764527235
    Decision = -764527242; Flow = -764527243; OrganizationUnit = -764527233
    MessageFormat = -764527241; NoteSymbol = -1028641999
    RectangleSymbol = 906510177; TextSymbol = 906510179
}
$Global:OomKind = @{
    Package = 403775585; Class = 403775587; Interface = 403775588; Dependency = 403775593
    Actor = 403775745; UseCase = 403775746; UseCaseAssociation = 403775603
    Component = 403776257; NoteSymbol = -1028641999
    RectangleSymbol = 906510177; TextSymbol = 906510179
}

# ---------------------------------------------------------------- sesión y modelos

function Open-F29 {
    $Global:Pd = New-Object -ComObject 'PowerDesigner.Application'
    $Global:PdOrigMode = $Pd.InteractiveMode
    $Pd.InteractiveMode = 0
}

function Close-F29 { if ($Global:Pd) { $Pd.InteractiveMode = $Global:PdOrigMode } }

# Devuelve el modelo abierto con esa ruta o lo abre. Nunca abre otro archivo.
function Get-F29Model([string]$file) {
    $full = [System.IO.Path]::GetFullPath($file)
    if ($full -notin @([System.IO.Path]::GetFullPath($F29Bpm), [System.IO.Path]::GetFullPath($F29Oom))) {
        throw "F29 solo edita sus dos modelos; se pidió $full"
    }
    foreach ($m in $Pd.Models) { if ([System.IO.Path]::GetFullPath($m.FileName) -eq $full) { return $m } }
    $Pd.GetType().InvokeMember('OpenModel', 'InvokeMethod', $null, $Pd, @($full))
}

function Save-F29Model($model) {
    $file = [System.IO.Path]::GetFullPath($model.FileName)
    if ($file -notin @([System.IO.Path]::GetFullPath($F29Bpm), [System.IO.Path]::GetFullPath($F29Oom))) {
        throw "Guardado rechazado fuera de la F29: $file"
    }
    $model.Save()
    # PowerDesigner deja una copia de respaldo al guardar sobre un archivo existente.
    Get-ChildItem $F29Models -File | Where-Object { $_.Extension -in '.bpb', '.obb', '.oob', '.bak', '.pdb' } | Remove-Item -Force
}

# ---------------------------------------------------------------- acceso COM

function Get-P($o, $p) { $o.GetType().InvokeMember($p, 'GetProperty', $null, $o, $null) }
function Set-P($o, $p, $v) { $o.GetType().InvokeMember($p, 'SetProperty', $null, $o, @($v)) | Out-Null }
# Colecciones COM: la coma evita que PowerShell las desenrolle al devolverlas.
function Get-C($o, $p) { , $o.GetType().InvokeMember($p, 'GetProperty', $null, $o, $null) }

function Set-Rect($sym, [int]$l, [int]$t, [int]$r, [int]$b) { Set-P $sym 'Rect' ($Pd.NewRect($l, $t, $r, $b)) }
function Get-Rect($sym) {
    $r = Get-P $sym 'Rect'
    [pscustomobject]@{ L = Get-P $r 'Left'; T = Get-P $r 'Top'; R = Get-P $r 'Right'; B = Get-P $r 'Bottom' }
}
function Set-Box($sym, [int]$cx, [int]$cy, [int]$w, [int]$h) {
    Set-Rect $sym ($cx - [int]($w / 2)) ($cy + [int]($h / 2)) ($cx + [int]($w / 2)) ($cy - [int]($h / 2))
}
function Get-Center($sym) { $r = Get-Rect $sym; @([int](($r.L + $r.R) / 2), [int](($r.T + $r.B) / 2)) }

function Set-DisplayPref($diagram, [hashtable]$pairs) {
    $p = [string](Get-P $diagram 'DisplayPreferences')
    foreach ($k in $pairs.Keys) {
        $rx = '(?m)^' + [regex]::Escape($k) + '=.*$'
        if ([regex]::IsMatch($p, $rx)) { $p = [regex]::Replace($p, $rx, ($k + '=' + $pairs[$k]).Replace('$', '$$')) }
        else { Write-Warning "Preferencia no encontrada: $k" }
    }
    Set-P $diagram 'DisplayPreferences' $p
}

# Cambia la fuente de todas las secciones de símbolos (Arial 8 por defecto).
function Set-DiagramFont($diagram, [int]$size) {
    $p = [string](Get-P $diagram 'DisplayPreferences')
    $p = [regex]::Replace($p, 'Font=Arial,\d+,N', "Font=Arial,$size,N")
    Set-P $diagram 'DisplayPreferences' $p
}

# ---------------------------------------------------------------- notas y textos

function Add-Note($diagram, [string]$text, [int]$l, [int]$t, [int]$r, [int]$b) {
    $n = $diagram.Symbols.CreateNew(-1028641999)
    $n.SetAttributeText('Text', $text) | Out-Null
    Set-Rect $n $l $t $r $b
    $n
}

function Add-Text($diagram, [string]$text, [int]$l, [int]$t, [int]$r, [int]$b) {
    $s = $diagram.Symbols.CreateNew(906510179)
    $s.SetAttributeText('Text', $text) | Out-Null
    Set-Rect $s $l $t $r $b
    $s
}

function Add-Frame($diagram, [int]$l, [int]$t, [int]$r, [int]$b, [int]$dash = 0) {
    $s = $diagram.Symbols.CreateNew(906510177)
    Set-Rect $s $l $t $r $b
    try { Set-P $s 'BrushStyle' 0 } catch {}
    if ($dash) { try { Set-P $s 'DashStyle' $dash } catch {} }
    $s
}

# Lleva un símbolo al frente: PowerDesigner dibuja en el orden de la colección y
# coloca los símbolos libres (notas, textos) al principio, detrás de los pools.
function Move-ToFront($diagram, $sym) {
    $c = Get-C $diagram 'Symbols'
    $c.Remove($sym) | Out-Null
    $c.Add($sym) | Out-Null
}

# Marco discontinuo de grupo como cuatro bordes finos al frente: un rectángulo tiene
# relleno opaco y, al frente, taparía los símbolos que agrupa.
function Add-DashedBox($diagram, [int]$l, [int]$t, [int]$r, [int]$b, [int]$color = 4210752) {
    foreach ($e in @(@($l, ($t + 40), $r, ($t - 40)), @($l, ($b + 40), $r, ($b - 40)), @(($l - 40), $t, ($l + 40), $b), @(($r - 40), $t, ($r + 40), $b))) {
        $s = Add-Frame $diagram $e[0] $e[1] $e[2] $e[3] 2
        Set-P $s 'LineColor' $color
        Move-ToFront $diagram $s
    }
}

# Rótulo de texto centrado en (cx, cy): PowerDesigner no muestra el nombre de los
# eventos ni de las compuertas BPMN 2.0 dentro de su icono.
function Add-Label($diagram, [string]$text, [int]$cx, [int]$cy, [int]$w = 9000, [int]$h = 2200) {
    $s = Add-Text $diagram $text ($cx - [int]($w / 2)) ($cy + [int]($h / 2)) ($cx + [int]($w / 2)) ($cy - [int]($h / 2))
    Move-ToFront $diagram $s
    $s
}

# ---------------------------------------------------------------- rutas de vínculos

# Traza un vínculo ortogonal. $via: puntos intermedios @(@(x,y), ...). Los extremos
# salen del centro de un lado del símbolo (el vértice en un rombo o un círculo).
# $toTop/$fromBottom fuerzan el lado de entrada/salida cuando la ruta es vertical.
function Get-OrthoPoints($symA, $symB, $via, $endB = $null) {
    $a = Get-Rect $symA
    $acx = [int](($a.L + $a.R) / 2); $acy = [int](($a.T + $a.B) / 2)
    if ($symB) { $b = Get-Rect $symB; $bcx = [int](($b.L + $b.R) / 2); $bcy = [int](($b.T + $b.B) / 2) }
    $pts = @()
    if ($via.Count) { $f = $via[0] } elseif ($endB) { $f = $endB } elseif ([Math]::Abs($bcx - $acx) -lt 2) { $f = @($bcx, $bcy) } else { $f = @($bcx, $acy) }
    if ([Math]::Abs($f[0] - $acx) -lt 2) {
        if ($f[1] -gt $acy) { $pts += , @($acx, $a.T) } else { $pts += , @($acx, $a.B) }
    } else {
        if ($f[0] -gt $acx) { $pts += , @($a.R, $acy) } else { $pts += , @($a.L, $acy) }
        if ([Math]::Abs($f[1] - $acy) -gt 2 -and -not $via.Count) { }
    }
    foreach ($v in $via) { $pts += , @([int]$v[0], [int]$v[1]) }
    if ($endB) { $pts += , @([int]$endB[0], [int]$endB[1]); return , $pts }
    $l = $pts[-1]
    if ([Math]::Abs($l[0] - $bcx) -lt 2) {
        if ($l[1] -gt $bcy) { $pts += , @($bcx, $b.T) } else { $pts += , @($bcx, $b.B) }
    } else {
        if ($l[0] -gt $bcx) { $pts += , @($b.R, $l[1]) } else { $pts += , @($b.L, $l[1]) }
    }
    , $pts
}

function Set-LinkPoints($ls, $pts, $center = @(0, 1), $source = $null) {
    $pl = $Pd.NewPtList()
    foreach ($p in $pts) { $pl.Add($Pd.NewPoint([int]$p[0], [int]$p[1])) | Out-Null }
    Set-P $ls 'CornerStyle' 0
    $ls.SetAttribute('ListOfPoints', $pl) | Out-Null
    $ls.SetAttribute('CenterTextOffset', $Pd.NewPoint([int]$center[0], [int]$center[1])) | Out-Null
    if ($source) { $ls.SetAttribute('SourceTextOffset', $Pd.NewPoint([int]$source[0], [int]$source[1])) | Out-Null }
}

# Ruta ortogonal entre dos rectángulos (objetos de Get-Rect) según una especificación:
#   'H'        recta horizontal entre los lados enfrentados, a la altura del origen
#   'V[:x]'    recta vertical entre los bordes enfrentados, en x (por defecto, el centro del origen)
#   'HV[:x]'   sale por un lado hasta x (por defecto, el centro del destino) y entra por arriba o abajo
#   'VH'       sale por arriba o abajo hasta la altura del destino y entra por un lado
#   'Y:v'      sale por arriba o abajo hasta y = v, cruza hasta el centro del destino y entra en vertical
#   'B:y'      como 'V', pero termina en y (borde de un pool, sin elemento receptor)
function Get-Route($s, $t, [string]$spec) {
    $sx = [int](($s.L + $s.R) / 2); $sy = [int](($s.T + $s.B) / 2)
    if ($t) { $tx = [int](($t.L + $t.R) / 2); $ty = [int](($t.T + $t.B) / 2) }
    $parts = $spec -split ':'
    switch ($parts[0]) {
        'H' { if ($tx -ge $sx) { return , @(@($s.R, $sy), @($t.L, $sy)) } else { return , @(@($s.L, $sy), @($t.R, $sy)) } }
        'V' {
            $x = $sx; if ($parts.Count -gt 1) { $x = [int]$parts[1] }
            if ($ty -lt $sy) { return , @(@($x, $s.B), @($x, $t.T)) } else { return , @(@($x, $s.T), @($x, $t.B)) }
        }
        'B' { $y = [int]$parts[1]; $x = $sx; if ($parts.Count -gt 2) { $x = [int]$parts[2] }
            if ($y -lt $sy) { return , @(@($x, $s.B), @($x, $y)) } else { return , @(@($x, $s.T), @($x, $y)) } }
        'HV' {
            $x = $tx; if ($parts.Count -gt 1) { $x = [int]$parts[1] }
            $a = $(if ($x -ge $sx) { $s.R } else { $s.L })
            $e = $(if ($sy -gt $ty) { $t.T } else { $t.B })
            return , @(@($a, $sy), @($x, $sy), @($x, $e))
        }
        'VH' {
            $a = $(if ($ty -gt $sy) { $s.T } else { $s.B })
            $e = $(if ($sx -lt $tx) { $t.L } else { $t.R })
            return , @(@($sx, $a), @($sx, $ty), @($e, $ty))
        }
        'Y' {
            $v = [int]$parts[1]
            $a = $(if ($v -gt $sy) { $s.T } else { $s.B })
            $e = $(if ($v -gt $ty) { $t.T } else { $t.B })
            return , @(@($sx, $a), @($sx, $v), @($tx, $v), @($tx, $e))
        }
    }
    throw "Ruta desconocida: $spec"
}

# ---------------------------------------------------------------- BPM: paquetes, pools, carriles

# Borra el paquete de la vista (con todo su contenido) y lo vuelve a crear con su diagrama.
function Reset-BpmView($model, [string]$pkgCode, [string]$pkgName, [string]$diagramName) {
    foreach ($pk in @($model.GetCollectionByName('Packages'))) {
        if ($pk -and $pk.Code -eq $pkgCode) { $pk.Delete() | Out-Null; Write-Host "  paquete anterior $pkgCode eliminado" }
    }
    # Pools temporales que una corrida interrumpida pudiera haber dejado.
    foreach ($o in @($model.GetCollectionByName('OrganizationUnits'))) { if ($o -and $o.Code -like 'F29TMP_*') { $o.Delete() | Out-Null } }
    $pk = $model.CreateObject($BpmKind.Package)
    $pk.Name = $pkgName; $pk.Code = $pkgCode
    $d = (Get-C $pk 'BusinessProcessDiagrams').Item(0)
    $d.Name = $diagramName; $d.Code = ($pkgCode + '_BPD')
    @{ Package = $pk; Diagram = $d }
}

function Get-OU($model, [string]$name, [string]$code, [string]$stereo) {
    foreach ($o in @($model.GetCollectionByName('OrganizationUnits'))) { if ($o -and $o.Name -eq $name) { return $o } }
    $o = $model.CreateObject($BpmKind.OrganizationUnit)
    $o.Name = $name; $o.Code = $code
    $o.Stereotype = $stereo
    $o
}

# Pool con sus carriles (de arriba hacia abajo). PowerDesigner crea un carril por
# defecto al insertar un pool; los carriles reales se obtienen insertando su unidad
# organizativa (que aparece en un pool temporal) y moviendo ese carril al pool.
function New-Pool($model, $diagram, $poolOU, $laneOUs) {
    # Pools ya presentes en el diagrama: al insertar un carril, PowerDesigner puede
    # dejarlo caer en uno de ellos en lugar de crear un pool temporal.
    $known = @{}
    foreach ($s in (Get-C $diagram 'Symbols')) {
        $kind = $null; try { $kind = Get-P $s 'ClassKind' } catch {}
        if ($kind -eq -764527219) { $known[[string](Get-P (Get-P $s 'Object') 'ObjectID')] = $true }
    }
    $ps = $diagram.AttachObject($poolOU)
    $known[[string](Get-P $poolOU 'ObjectID')] = $true
    $grp = (Get-C $ps 'SubSymbols').Item(0)
    $gsubs = Get-C $grp 'SubSymbols'
    $default = $gsubs.Item(0)
    $defaultOU = Get-P $default 'Object'
    $lanes = @{}
    $ordered = @($laneOUs)
    [array]::Reverse($ordered)            # cada carril movido queda arriba del anterior
    $i = 0
    foreach ($lo in $ordered) {
        $ts = $diagram.AttachObject($lo)
        if ((Get-P $ts 'ClassKind') -eq -764527221) { $ln = $ts; $tg = Get-P $ln 'Parent'; $tps = Get-P $tg 'Parent' }
        else { $tps = $ts; $tg = (Get-C $tps 'SubSymbols').Item(0); $ln = (Get-C $tg 'SubSymbols').Item(0) }
        $hostPool = Get-P $tps 'Object'
        $tsubs = Get-C $tg 'SubSymbols'
        $tsubs.Remove($ln) | Out-Null
        $gsubs.Add($ln) | Out-Null
        # Solo se borra el pool si es el temporal que creó la inserción.
        if ($env:F29_DEBUG) { Write-Host "  [dbg] carril $($lo.Name) cayó en $($hostPool.Name); conocidos: $($known.Keys -join ',')" }
        if (-not $known.ContainsKey([string](Get-P $hostPool 'ObjectID'))) { $hostPool.Code = 'F29TMP_' + $i; $i++; $hostPool.Delete() | Out-Null }
        $lanes[$lo.Name] = $ln
    }
    $default.Delete() | Out-Null
    if ($defaultOU -and $defaultOU.Name -like 'Default*') { $defaultOU.Delete() | Out-Null }
    # Carriles por defecto huérfanos (Default, Default2...) de corridas anteriores.
    foreach ($o in @($model.GetCollectionByName('OrganizationUnits'))) { if ($o -and $o.Code -like 'Default*' -and $o.Stereotype -eq 'Lane') { try { $o.Delete() | Out-Null } catch {} } }
    # Comprobación: el pool tiene exactamente sus carriles.
    $names = @(); $gs = Get-C $grp 'SubSymbols'
    for ($k = 0; $k -lt $gs.Count; $k++) { $x = $gs.Item($k); $names += [string]$x.Object.Name }
    if ($names.Count -ne @($laneOUs).Count) { throw "Pool $($poolOU.Name): carriles $($names -join ', ')" }
    @{ OU = $poolOU; Sym = $ps; Lanes = $lanes; Order = @($laneOUs | ForEach-Object { $_.Name }) }
}

# Fija la geometría: alto de cada carril (de arriba hacia abajo) y ancho del pool.
# PowerDesigner apila los carriles desde el borde inferior del pool.
function Set-PoolGeometry($pool, [int]$left, [int]$right, [int]$bottom, [int[]]$heights) {
    $total = ($heights | Measure-Object -Sum).Sum
    Set-Rect $pool.Sym $left ($bottom + $total) $right $bottom
    $y = $bottom
    for ($k = $pool.Order.Count - 1; $k -ge 0; $k--) {
        $ln = $pool.Lanes[$pool.Order[$k]]
        Set-Rect $ln $left ($y + $heights[$k]) $right $y
        $y += $heights[$k]
    }
    # Verificación: cada carril donde se pidió.
    $y = $bottom
    for ($k = $pool.Order.Count - 1; $k -ge 0; $k--) {
        $r = Get-Rect $pool.Lanes[$pool.Order[$k]]
        if ([Math]::Abs($r.B - $y) -gt 5 -or [Math]::Abs($r.T - ($y + $heights[$k])) -gt 5) {
            throw "Carril $($pool.Order[$k]) fuera de lugar: $($r.B)..$($r.T), se esperaba $y..$($y + $heights[$k])"
        }
        $y += $heights[$k]
    }
}

# Banda vertical (inferior, superior) de un carril.
function Get-LaneBand($pool, [string]$lane) { $r = Get-Rect $pool.Lanes[$lane]; @($r.B, $r.T) }

# Nodo BPMN (tarea, evento, compuerta...). $lane: símbolo de carril donde se coloca, o
# $null para dejarlo en el nivel superior del diagrama. $laneOU: responsable (atributo
# OrganizationUnit), que puede diferir del símbolo cuando el nodo va dentro de un subproceso.
function New-BpmNode($container, $diagram, [string]$kind, [string]$name, [string]$code, [string]$stereo, $laneSym, $laneOU, [int]$cx, [int]$cy, [int]$w, [int]$h) {
    $o = $container.CreateObject($BpmKind[$kind])
    $o.Name = $name; $o.Code = $code
    if ($stereo) { $o.Stereotype = $stereo }
    if ($laneOU) { try { Set-P $o 'OrganizationUnit' $laneOU } catch { Write-Warning "OU no asignada a $code" } }
    $s = $null
    if ($diagram) {
        $s = $diagram.AttachObject($o)
        if ($laneSym) {
            (Get-C $diagram 'Symbols').Remove($s) | Out-Null
            (Get-C $laneSym 'SubSymbols').Add($s) | Out-Null
        }
        Set-Box $s $cx $cy $w $h
    }
    @{ Obj = $o; Sym = $s }
}

function New-BpmFlow($container, $src, $dst, [string]$stereo, [string]$cond, [string]$name, $format) {
    $f = $container.CreateObject($BpmKind.Flow)
    Set-P $f 'Source' $src
    Set-P $f 'Destination' $dst
    $f.Stereotype = $stereo
    if ($name) { $f.Name = $name }
    if ($cond) { $f.ConditionAlias = $cond }
    if ($format) { Set-P $f 'Format' $format; Set-P $f 'UndefinedFormat' $false }
    $f
}

# Busca, en todo el árbol de símbolos del diagrama, el símbolo de un objeto.
function Find-SymbolDeep($symbols, $obj) {
    foreach ($s in @($symbols)) {
        if (-not $s) { continue }
        try { $o = Get-P $s 'Object' } catch { $o = $null }
        if ($o -and $o.ObjectID -eq $obj.ObjectID) { return $s }
        $subs = $null
        try { $subs = Get-C $s 'SubSymbols' } catch {}
        if ($subs -and $subs.Count) { $r = Find-SymbolDeep $subs $obj; if ($r) { return $r } }
    }
    $null
}

# Símbolo de vínculo de un flujo: el que PowerDesigner ya creó (dentro de un
# subproceso expandido) o uno nuevo en el diagrama.
function Get-FlowSymbol($diagram, $flow, $srcSym, $dstSym) {
    $s = Find-SymbolDeep (Get-C $diagram 'Symbols') $flow
    if ($s) { return $s }
    $diagram.AttachLinkObject($flow, $srcSym, $dstSym)
}

# ---------------------------------------------------------------- exportación

# PNG y SVG. El PNG nativo de PowerDesigner 16.6 omite el contenido de los
# subprocesos expandidos (vista compuesta); por eso el PNG se rasteriza desde el SVG
# exportado por PowerDesigner (tools/svg2png.py, Edge sin interfaz). El SVG es la
# exportación nativa; el PNG es su copia en mapa de bits, sin retoques.
function Export-F29([object]$diagram, [string]$base, [switch]$NativePng) {
    New-Item -ItemType Directory -Force $F29Exports | Out-Null
    $svg = Join-Path $F29Exports "$base.svg"
    $png = Join-Path $F29Exports "$base.png"
    $diagram.ExportImage($svg)
    if ($NativePng) { $diagram.ExportImage($png) }
    else {
        $py = Join-Path $F29Scripts 'svg2png.py'
        & python $py $svg $png 2 | Out-Null
        if ($LASTEXITCODE -ne 0) { throw "svg2png falló para $base" }
    }
    Write-Host "  exportado: $base.svg / $base.png"
}

# ---------------------------------------------------------------- verificación del modelo

# Ejecuta Check Model sin autocorrección y devuelve las comprobaciones que hallaron
# algo: categoría, comprobación, severidad (PowerDesigner: 0 advertencia, 1 error).
# Los mensajes por objeto quedan en la lista de resultados de la interfaz, que la
# automatización no expone; la categoría identifica el tipo de objeto afectado.
function Invoke-F29Check($model) {
    $opts = $model.GetPackageOptions()
    $ctrl = $opts.GetCheckModelControler()
    foreach ($cat in (Get-C $ctrl 'Categories')) {
        foreach ($chk in (Get-C $cat 'Checks')) { try { $chk.AutoCorrect = 0; $chk.Execution = 1 } catch {} }
    }
    $model.CheckModel() | Out-Null
    $found = @()
    foreach ($cat in (Get-C $ctrl 'Categories')) {
        foreach ($chk in (Get-C $cat 'Checks')) {
            $err = $false; try { $err = [bool](Get-P $chk 'ErrorFound') } catch {}
            if ($err) { $found += [pscustomobject]@{ Category = $cat.Name; Check = $chk.Name; Severity = (Get-P $chk 'Severity') } }
        }
    }
    , $found
}

# ---------------------------------------------------------------- verificación estructural BPMN

# Recorre el paquete (y los subprocesos compuestos) y devuelve nodos y flujos por código.
function Get-BpmGraph($container) {
    $nodes = @{}; $flows = New-Object System.Collections.ArrayList
    function Visit($c) {
        foreach ($cn in 'Processes', 'ProcessStarts', 'ProcessEnds', 'ProcessDecisions') {
            foreach ($o in $c.GetCollectionByName($cn)) {
                $comp = $false; if ($cn -eq 'Processes') { $comp = [bool](Get-P $o 'Composite') }
                $nodes[$o.Code] = [pscustomobject]@{ Code = $o.Code; Name = $o.Name; Stereo = $o.Stereotype; Kind = $cn; Composite = $comp }
                if ($comp) { Visit $o }
            }
        }
        foreach ($f in $c.GetCollectionByName('Flows')) {
            $src = Get-P $f 'Source'; $dst = Get-P $f 'Destination'
            [void]$flows.Add([pscustomobject]@{ Code = $f.Code; Stereo = $f.Stereotype; Src = $src.Code; Dst = $dst.Code; Cond = $f.ConditionAlias; Format = $(try { (Get-P $f 'Format').Name } catch { '' }) })
        }
    }
    Visit $container
    @{ Nodes = $nodes; Flows = $flows }
}

# Escribe un informe de verificación de la vista (texto plano, UTF-8).
function Write-F29Report([string]$file, [string[]]$lines) {
    $dir = Split-Path $file
    New-Item -ItemType Directory -Force $dir | Out-Null
    [System.IO.File]::WriteAllText($file, (($lines -join "`n") + "`n"), (New-Object System.Text.UTF8Encoding($false)))
    Write-Host "  informe: $file"
}

# Check Model del BPM completo (PowerDesigner no permite limitarlo a un paquete), con
# prueba de aislamiento de los hallazgos que exige la especificación del F5:
#   - TB-30 y TB-F1 sin flujos (CheckPrcsInputFlow / CheckPrcsOutputFlow, errores):
#     se conectan de forma temporal con flujos que se borran enseguida;
#   - MT-02 hacia el borde de SP-P con formato de mensaje (CheckFlowIncohMsg, advertencia):
#     un subproceso compuesto no puede declarar un mensaje recibido en PowerDesigner
#     (Received Message es de solo lectura y la acción de recepción no está disponible en
#     su modo de implementación). Se retira el formato de MT-02 de forma temporal y se
#     restituye.
# Con todo aislado no debe quedar ningún hallazgo, y al deshacerlo deben volver solo los
# esperados. Nada de lo temporal se guarda.
function Test-F29BpmCheck($model) {
    $fmt = { param($r) if ($r.Count) { ($r | ForEach-Object { "$($_.Category)/$($_.Check)/sev$($_.Severity)" }) -join ', ' } else { 'ninguno' } }
    $key = { param($r) @($r | ForEach-Object { "$($_.Category)/$($_.Check)" } | Sort-Object) }
    $all = Invoke-F29Check $model
    $lines = @("Check Model del BPM completo (sin autocorrección): $($all.Count) hallazgos: " + (& $fmt $all))
    $f5 = $null; foreach ($x in $model.GetCollectionByName('Packages')) { if ($x.Code -eq 'F5') { $f5 = $x } }
    $expected = @()
    $isoOk = $true
    if ($f5) {
        $expected = @('Flow/CheckFlowIncohMsg', 'Process/CheckPrcsInputFlow', 'Process/CheckPrcsOutputFlow')
        $p = @{}; foreach ($x in $f5.GetCollectionByName('Processes')) { $p[$x.Code] = $x }
        $e = $null; foreach ($x in $f5.GetCollectionByName('ProcessEnds')) { if ($x.Code -eq 'F5_EFE') { $e = $x } }
        $mt02 = $null; foreach ($x in $f5.GetCollectionByName('Flows')) { if ($x.Code -eq 'F5_MT_02_FLOW') { $mt02 = $x } }
        $fm = Get-P $mt02 'Format'
        # 1) TB-30 y TB-F1 conectados de forma temporal.
        $tmp = @()
        foreach ($c in 'F5_TB_30', 'F5_TB_F1') {
            $tmp += New-BpmFlow $f5 $p['F5_TB_29'] $p[$c] 'Sequence Flow' '' $null $null
            $tmp += New-BpmFlow $f5 $p[$c] $e 'Sequence Flow' '' $null $null
        }
        $r1 = Invoke-F29Check $model
        $lines += '  1) TB-30 y TB-F1 conectados de forma temporal: ' + (& $fmt $r1)
        # 2) Además, MT-02 sin formato (el cambio de estereotipo lo retira).
        $mt02.Stereotype = 'Sequence Flow'; $mt02.Stereotype = 'Message Flow'
        $r2 = Invoke-F29Check $model
        $lines += '  2) Y MT-02 sin formato de mensaje: ' + (& $fmt $r2)
        # Deshacer: se restituye el formato y se retiran los flujos temporales.
        Set-P $mt02 'Format' $fm; Set-P $mt02 'UndefinedFormat' $false
        foreach ($t in $tmp) { $t.Delete() | Out-Null }
        $r3 = Invoke-F29Check $model
        $restored = ((Get-P $mt02 'Format').ObjectID -eq $fm.ObjectID) -and $mt02.Stereotype -eq 'Message Flow'
        $lines += '  3) Deshecho (formato de MT-02 restituido: ' + $restored + '): ' + (& $fmt $r3)
        $isoOk = ((& $key $r1) -join ',') -eq 'Flow/CheckFlowIncohMsg' -and -not $r2.Count -and $restored -and
            (-not (Compare-Object $expected (& $key $r3)))
    }
    $ok = $isoOk -and -not (Compare-Object @($expected) @(& $key $all))
    if ($ok -and $all.Count) {
        $lines += '  Los hallazgos se deben solo a TB-30 y TB-F1 (desconectados por especificación, errores) y a MT-02 con formato hacia el borde de SP-P (advertencia por límite de PowerDesigner; la especificación exige ese destino).'
    }
    [pscustomobject]@{ Ok = $ok; Lines = $lines }
}

# ---------------------------------------------------------------- OOM: paquetes y vistas

# Borra el paquete de la vista (con su contenido) y lo vuelve a crear con un diagrama del
# tipo pedido ('UseCaseDiagrams', 'ComponentDiagrams', ...). Se eliminan los diagramas
# vacíos que PowerDesigner crea por defecto en el paquete.
function Reset-OomView($model, [string]$pkgCode, [string]$pkgName, [string]$diagramCollection, [string]$diagramName) {
    foreach ($pk in @($model.GetCollectionByName('Packages'))) {
        if ($pk -and $pk.Code -eq $pkgCode) { $pk.Delete() | Out-Null; Write-Host "  paquete anterior $pkgCode eliminado" }
    }
    $pk = $model.CreateObject($OomKind.Package)
    $pk.Name = $pkgName; $pk.Code = $pkgCode
    $d = $pk.GetCollectionByName($diagramCollection).CreateNew()
    $d.Name = $diagramName; $d.Code = ($pkgCode + '_DIAG')
    foreach ($x in @($pk.AllDiagrams)) { if ($x -and $x.ObjectID -ne $d.ObjectID -and $x.Symbols.Count -eq 0) { $x.Delete() | Out-Null } }
    @{ Package = $pk; Diagram = $d }
}

# Punto del borde de un símbolo en la dirección (ux, uy) desde su centro: elipse para
# casos de uso, rectángulo para lo demás.
function Get-EdgePoint($sym, [double]$ux, [double]$uy, [switch]$Ellipse) {
    $r = Get-Rect $sym
    $cx = ($r.L + $r.R) / 2; $cy = ($r.T + $r.B) / 2; $a = ($r.R - $r.L) / 2; $b = ($r.T - $r.B) / 2
    if ($Ellipse) { $t = 1 / [Math]::Sqrt([Math]::Pow($ux / $a, 2) + [Math]::Pow($uy / $b, 2)) }
    else {
        $t = [double]::MaxValue
        if ([Math]::Abs($ux) -gt 1e-9) { $t = [Math]::Min($t, $a / [Math]::Abs($ux)) }
        if ([Math]::Abs($uy) -gt 1e-9) { $t = [Math]::Min($t, $b / [Math]::Abs($uy)) }
    }
    @([int]($cx + $ux * $t), [int]($cy + $uy * $t))
}

# Vínculo recto de borde a borde entre dos símbolos.
function Set-EdgeLink($ls, $symA, $symB, [bool]$ellA, [bool]$ellB) {
    $a = Get-Center $symA; $b = Get-Center $symB
    $dx = $b[0] - $a[0]; $dy = $b[1] - $a[1]; $len = [Math]::Sqrt($dx * $dx + $dy * $dy)
    $ux = $dx / $len; $uy = $dy / $len
    $p1 = Get-EdgePoint $symA $ux $uy -Ellipse:$ellA
    $p2 = Get-EdgePoint $symB (-$ux) (-$uy) -Ellipse:$ellB
    Set-LinkPoints $ls @($p1, $p2)
    , @($p1, $p2)
}

# Legibilidad: devuelve los pares (vínculo, símbolo) en que un segmento atraviesa un
# símbolo ajeno a sus extremos (elipse o rectángulo ampliados en $margin).
function Test-LinkClearance($segments, $shapes, [int]$margin = 250) {
    $hits = @()
    foreach ($sg in $segments) {
        foreach ($sh in $shapes) {
            if ($sh.Id -in $sg.Ends) { continue }
            $a = $sh.A + $margin; $b = $sh.B + $margin
            for ($i = 0; $i -le 200; $i++) {
                $x = $sg.P1[0] + ($sg.P2[0] - $sg.P1[0]) * $i / 200; $y = $sg.P1[1] + ($sg.P2[1] - $sg.P1[1]) * $i / 200
                $dx = ($x - $sh.X) / $a; $dy = ($y - $sh.Y) / $b
                if (($sh.Ellipse -and ($dx * $dx + $dy * $dy) -lt 1) -or (-not $sh.Ellipse -and [Math]::Abs($dx) -lt 1 -and [Math]::Abs($dy) -lt 1)) {
                    $hits += "$($sg.Name) atraviesa $($sh.Id)"; break
                }
            }
        }
    }
    , $hits
}

# Check Model del OOM completo con prueba de aislamiento: la especificación del F8 exige
# CU-16 sin actor directo (se llega por «include» desde CU-05, CU-15 y CU-17) y
# PowerDesigner lo señala como caso de uso aislado (Use Case/Single). Se asocia CU-16 a
# ACT-02 de forma temporal; con ello no debe quedar ningún hallazgo. Nada se guarda.
function Test-F29OomCheck($model) {
    $fmt = { param($r) if ($r.Count) { ($r | ForEach-Object { "$($_.Category)/$($_.Check)/sev$($_.Severity)" }) -join ', ' } else { 'ninguno' } }
    $all = Invoke-F29Check $model
    $lines = @("Check Model del OOM completo (sin autocorrección): $($all.Count) hallazgos: " + (& $fmt $all))
    $f8 = $null; foreach ($x in $model.GetCollectionByName('Packages')) { if ($x.Code -eq 'F8') { $f8 = $x } }
    $expected = @(); $isoOk = $true
    if ($f8) {
        $expected = @('Use Case/Single')
        $act = $null; $cu = $null
        foreach ($x in $f8.GetCollectionByName('Actors')) { if ($x.Code -eq 'F8_ACT_02') { $act = $x } }
        foreach ($x in $f8.GetCollectionByName('UseCases')) { if ($x.Code -eq 'F8_CU_16') { $cu = $x } }
        $tmp = $f8.CreateObject($OomKind.UseCaseAssociation); $tmp.Object1 = $act; $tmp.Object2 = $cu
        $iso = Invoke-F29Check $model
        $tmp.Delete() | Out-Null
        $after = Invoke-F29Check $model
        $lines += '  Aislamiento (CU-16 del F8 asociado a un actor de forma temporal): ' + (& $fmt $iso)
        $lines += '  Tras retirar la asociación temporal: ' + (& $fmt $after)
        $isoOk = (-not $iso.Count) -and ((@($after | ForEach-Object { "$($_.Category)/$($_.Check)" }) -join ',') -eq 'Use Case/Single')
    }
    $ok = $isoOk -and ((@($all | ForEach-Object { "$($_.Category)/$($_.Check)" }) -join ',') -eq ($expected -join ','))
    if ($ok -and $all.Count) { $lines += '  El único hallazgo se debe a CU-16 del F8, sin actor directo por especificación.' }
    [pscustomobject]@{ Ok = $ok; Lines = $lines }
}
