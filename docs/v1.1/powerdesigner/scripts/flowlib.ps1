# Motor de los diagramas de actividad (AC-01, AC-02) y de estados (ST-01..ST-04).
#
# Cada diagrama es un dato: nodos con su posición en una rejilla y vínculos con su
# ruta ortogonal. Reglas:
#   - Primero se colocan todos los símbolos y después se trazan los vínculos
#     (al mover un símbolo, PowerDesigner rehace las rutas de sus vínculos).
#   - Rutas: 'V' vertical, 'H' horizontal, 'VH' baja y luego gira, 'HV' gira y luego
#     baja, o una lista explícita de puntos intermedios (Via). Los extremos salen del
#     centro de un lado, que en un rombo de decisión es su vértice.
#   - Si el diagrama ya existe, se reemplaza: se borran sus nodos y vínculos y el
#     diagrama, y se vuelve a generar. Las unidades organizativas (carriles) se
#     reutilizan por nombre.

$Global:FlowClasses = @('Activity', 'Decision', 'Start', 'End', 'Flow', 'State', 'Transition')

function Remove-FlowDiagram($model, $collection, [string]$name, [string]$code) {
    $old = @($collection) | Where-Object { $_.Name -eq $name }
    foreach ($d in $old) {
        $objs = @()
        foreach ($s in @($d.Symbols)) {
            try { $o = Get-P $s 'Object' } catch { $o = $null }
            if ($o -and ($FlowClasses -contains $o.ClassName)) { $objs += $o }
        }
        # Primero los vínculos, después los nodos.
        foreach ($o in ($objs | Where-Object { $_.ClassName -in 'Flow', 'Transition' })) { try { $o.Delete() } catch {} }
        foreach ($o in ($objs | Where-Object { $_.ClassName -notin 'Flow', 'Transition' })) { try { $o.Delete() } catch {} }
        $d.Delete()
        Write-Host "  reemplazado: $name ($($objs.Count) nodos y vínculos anteriores eliminados)"
    }
    # Restos de una corrida interrumpida: todo nodo lleva el código <diagrama>_<id>.
    $left = 0
    foreach ($col in 'Activities', 'Decisions', 'Starts', 'Ends', 'States') {
        try { $items = @($model.GetCollectionByName($col)) } catch { $items = @() }
        foreach ($o in $items) { if ($o -and $o.Code -like "$($code)_*") { $o.Delete(); $left++ } }
    }
    if ($left) { Write-Host "  restos eliminados: $left" }
}

# Alto de una caja según su texto (360 unidades por carácter, 1000 por línea).
function Get-TextHeight([string]$text, [int]$w, [int]$min = 2400) {
    $lines = 0
    foreach ($l in ($text -split "`n")) { $lines += [Math]::Max(1, [Math]::Ceiling($l.Length * 390 / ($w - 1400))) }
    [Math]::Max($min, 1200 + $lines * 1000)
}

function Get-OrgUnit($model, [string]$name) {
    $o = @($model.OrganizationUnits) | Where-Object { $_.Name -eq $name } | Select-Object -First 1
    if (-not $o) {
        $o = $model.CreateObject($PdKind.OrganizationUnit)
        $o.Name = $name
        try { $o.Code = 'OU_' + ($name -replace '[^A-Za-z0-9]+', '_') } catch {}
    }
    $o
}

# Transición `evento [guarda] / efecto`: $label = @(evento, guarda, efecto). El evento es
# un objeto Event del contenedor, reutilizado por nombre (p. ej. `discard`).
function Set-TransitionLabel($container, $t, $label) {
    $ev = $null
    try { $ev = @($container.GetCollectionByName('Events')) | Where-Object { $_ -and $_.Name -eq $label[0] } | Select-Object -First 1 } catch {}
    if (-not $ev) {
        $ev = $container.CreateObject($PdKind.Event)
        $ev.Name = $label[0]
        try { $ev.Code = 'EV_' + ($label[0] -replace '[^A-Za-z0-9]+', '_') } catch {}
    }
    $t.TriggerEvent = $ev
    if ($label.Count -gt 1 -and $label[1]) { $t.ConditionAlias = $label[1] }
    if ($label.Count -gt 2 -and $label[2]) { $t.TriggerAction = $label[2] }
}

# Carril como marco gráfico: rectángulo del carril, banda de cabecera y título.
function Add-Lane($diagram, [string]$title, [int]$l, [int]$r, [int]$top, [int]$bottom) {
    $box = $diagram.Symbols.CreateNew(906510177)
    Set-Rect $box $l $top $r $bottom
    $head = $diagram.Symbols.CreateNew(906510177)
    Set-Rect $head $l $top $r ($top - 2400)
    $t = $diagram.Symbols.CreateNew(906510179)
    $t.SetAttributeText('Text', $title) | Out-Null
    Set-Rect $t ($l + 300) ($top - 400) ($r - 300) ($top - 2000)
}

# Traza un vínculo ortogonal. $via: puntos intermedios @(@(x,y), ...).
function Set-OrthoLink($ls, $symA, $symB, $via, $labelOffset = @(0, 1), $sourceOffset = $null) {
    $a = Get-Rect $symA; $b = Get-Rect $symB
    $acx = [int](($a.L + $a.R) / 2); $acy = [int](($a.T + $a.B) / 2)
    $bcx = [int](($b.L + $b.R) / 2); $bcy = [int](($b.T + $b.B) / 2)
    $pts = @()
    # Salida: hacia el primer punto intermedio (o hacia el destino).
    # Sin puntos intermedios: recta vertical (mismo x) u horizontal a la altura del origen.
    if ($via.Count) { $f = $via[0] } elseif ([Math]::Abs($bcx - $acx) -lt 2) { $f = @($bcx, $bcy) } else { $f = @($bcx, $acy) }
    if ([Math]::Abs($f[0] - $acx) -lt 2) {
        if ($f[1] -gt $acy) { $pts += , @($acx, $a.T) } else { $pts += , @($acx, $a.B) }
    } else {
        if ($f[0] -gt $acx) { $pts += , @($a.R, $f[1]) } else { $pts += , @($a.L, $f[1]) }
    }
    foreach ($v in $via) { $pts += , @([int]$v[0], [int]$v[1]) }
    # Entrada: desde el último punto (o desde la salida).
    $l = $pts[-1]
    if ([Math]::Abs($l[0] - $bcx) -lt 2) {
        if ($l[1] -gt $bcy) { $pts += , @($bcx, $b.T) } else { $pts += , @($bcx, $b.B) }
    } else {
        if ($l[0] -gt $bcx) { $pts += , @($b.R, $l[1]) } else { $pts += , @($b.L, $l[1]) }
    }
    $pl = $Pd.NewPtList()
    foreach ($p in $pts) { $pl.Add($Pd.NewPoint([int]$p[0], [int]$p[1])) | Out-Null }
    Set-P $ls 'CornerStyle' 0
    $ls.SetAttribute('ListOfPoints', $pl) | Out-Null
    $ls.SetAttribute('CenterTextOffset', $Pd.NewPoint([int]$labelOffset[0], [int]$labelOffset[1])) | Out-Null
    # El rótulo de una transición es el texto de origen: se coloca junto al origen.
    if ($sourceOffset) { $ls.SetAttribute('SourceTextOffset', $Pd.NewPoint([int]$sourceOffset[0], [int]$sourceOffset[1])) | Out-Null }
}

# Convierte el tipo de ruta en puntos intermedios.
function Get-Via($symA, $symB, $route) {
    if ($route -is [array] -and $route.Count -and $route[0] -is [array]) { return , $route }
    $a = Get-Center $symA; $b = Get-Center $symB
    switch ($route) {
        'VH' { return , @(, @([int]$a[0], [int]$b[1])) }
        'HV' { return , @(, @([int]$b[0], [int]$a[1])) }
        default { return , @() }
    }
}

# Crea el diagrama. $spec: Lanes (opcional), Nodes, Links, Notes.
#   Lanes: @(@(nombre, izquierda, derecha), ...) con Top y Bottom del diagrama.
#   Nodes: @{ Id; Kind; Name; X; Y; W; H; Lane; Stereo; Final ('activity'|'flow') }
#   Links: @(desde, hacia, rótulo, ruta[, desplazamiento del rótulo])
# $model es el contenedor de los objetos: el modelo o un paquete.
function New-FlowDiagram($model, $collection, [string]$name, [string]$code, $spec) {
    Remove-FlowDiagram $model $collection $name $code
    $d = $collection.CreateNew()
    $d.Name = $name; $d.Code = $code

    # Carriles. PowerDesigner 16.6 reúne los carriles nativos en un solo símbolo de
    # grupo que se redimensiona solo al colocar nodos, y por COM no se consigue fijar
    # el ancho de cada carril. Por eso cada carril se dibuja como marco gráfico con
    # cabecera, y la partición queda en el modelo: cada nodo lleva su carril en el
    # atributo OrganizationUnit.
    $lanes = @{}
    foreach ($ln in @($spec.Lanes)) {
        if (-not $ln) { continue }
        $lanes[$ln[0]] = Get-OrgUnit $model $ln[0]
        Add-Lane $d $ln[0] ([int]$ln[1]) ([int]$ln[2]) ([int]$spec.Top) ([int]$spec.Bottom)
    }

    $objs = @{}; $syms = @{}
    foreach ($n in $spec.Nodes) {
        $o = $model.CreateObject($PdKind[$n.Kind])
        if ($n.Name) { $o.Name = $n.Name } else { $o.Name = $n.Id }
        try { $o.Code = ($code + '_' + $n.Id) } catch {}
        if ($n.Stereo) { $o.Stereotype = $n.Stereo }
        if ($n.Kind -eq 'End' -and $n.Final) { $o.ActivityTermination = ($n.Final -ne 'flow') }
        if ($n.Lane) { try { $o.OrganizationUnit = $lanes[$n.Lane] } catch {} }
        $objs[$n.Id] = $o
        $s = $d.AttachObject($o)
        $syms[$n.Id] = $s
        $r = Get-Rect $s
        $w = $r.R - $r.L; $h = $r.T - $r.B
        if ($n.W) { $w = $n.W }
        if ($n.H) { $h = $n.H } elseif ($n.Kind -in 'Activity', 'State') { $h = Get-TextHeight $o.Name $w }
        Set-Box $s ([int]$n.X) ([int]$n.Y) ([int]$w) ([int]$h)
    }

    # PowerDesigner calcula la posición del rótulo sobre la ruta automática que traza al
    # adjuntar el vínculo, y no la recalcula al fijar la ruta. Para un vínculo 'H' hacia
    # un estado alto (descartado, no_seleccionado), el destino se alinea un momento con
    # el origen para que esa ruta inicial ya sea horizontal. Al final se retrazan todas
    # las rutas, porque mover un símbolo rehace las de sus vínculos.
    $done = @()
    foreach ($lk in $spec.Links) {
        if ($spec.LinkKind -eq 'Transition') { $f = $model.CreateObject($PdKind.Transition) } else { $f = $model.CreateObject($PdKind.Flow) }
        $f.Source = $objs[$lk[0]]; $f.Destination = $objs[$lk[1]]
        if ($lk[2]) {
            if ($spec.LinkKind -eq 'Transition') { Set-TransitionLabel $model $f $lk[2] } else { $f.ConditionAlias = $lk[2] }
        }
        $sa = $syms[$lk[0]]; $sb = $syms[$lk[1]]
        $moved = $null
        if ($spec.AlignTarget -and $lk[3] -eq 'H') {
            $rb = Get-Rect $sb; $ca = Get-Center $sa
            if ([Math]::Abs((($rb.T + $rb.B) / 2) - $ca[1]) -gt 2) {
                $moved = $rb
                $h = $rb.T - $rb.B
                Set-Rect $sb $rb.L ([int]($ca[1] + $h / 2)) $rb.R ([int]($ca[1] - $h / 2))
            }
        }
        $ls = $d.AttachLinkObject($f, $sa, $sb)
        if ($moved) { Set-Rect $sb $moved.L $moved.T $moved.R $moved.B }
        # En tramos rectos y cortos el rótulo se aparta del trazo para que la flecha no lo tape.
        $off = @(0, 1)
        if ($lk[2] -and $lk[3] -eq 'H') { $off = @(0, 900) }
        if ($lk[2] -and $lk[3] -eq 'V') { $off = @(1100, 1) }
        if ($spec.LinkKind -eq 'Transition' -and $lk[2]) {
            # Rótulo de transición (texto de origen): se aparta del estado de origen según
            # su largo (unas 190 unidades por carácter, hasta unas 34 por línea).
            $txt = $lk[2][0]
            if ($lk[2].Count -gt 1 -and $lk[2][1]) { $txt += ' [' + $lk[2][1] + ']' }
            if ($lk[2].Count -gt 2 -and $lk[2][2]) { $txt += ' / ' + $lk[2][2] }
            $half = [Math]::Min($txt.Length, 34) * 190
            if ($lk[3] -eq 'H') {
                $sg = [Math]::Sign((Get-Center $sb)[0] - (Get-Center $sa)[0])
                $off = @([int]($sg * ($half + 600)), 900)
            } elseif ($lk[3] -eq 'V') {
                $off = @([int]($half * 0.95 + 700), 1)
            }
        }
        if ($lk.Count -gt 4 -and $lk[4]) { $off = $lk[4] }
        $done += , @($ls, $sa, $sb, $lk[3], $off)
    }
    foreach ($x in $done) {
        $via = Get-Via $x[1] $x[2] $x[3]
        if ($spec.LinkKind -eq 'Transition') { Set-OrthoLink $x[0] $x[1] $x[2] $via @(0, 1) $x[4] }
        else { Set-OrthoLink $x[0] $x[1] $x[2] $via $x[4] }
    }

    foreach ($nt in @($spec.Notes)) {
        if ($nt) { Add-Note $d $nt[0] ([int]$nt[1]) ([int]$nt[2]) ([int]$nt[3]) | Out-Null }
    }
    $d
}
