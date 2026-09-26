# Motor de los diagramas de secuencia (SEQ-01..SEQ-08).
#
# Cada secuencia es un dato: lifelines, mensajes en orden, fragmentos sobre rangos de
# mensajes, notas y divisores. Reglas:
#   - Actores: los de UC-01. Objetos: uno por nombre en todo el modelo (PowerDesigner
#     exige nombres únicos); si ya existe en el modelo, se reutiliza.
#   - Cada mensaje en su propia fila: PowerDesigner pone a la misma altura mensajes
#     entre lifelines distintas y el orden se vuelve ambiguo.
#   - Si el diagrama ya existe, se reemplaza: se borran sus mensajes y fragmentos y
#     el diagrama, y se vuelve a generar. No se dejan copias.

function Remove-Sequence($model, [string]$name) {
    $old = @($model.SequenceDiagrams) | Where-Object { $_.Name -eq $name }
    foreach ($d in $old) {
        $objs = @()
        foreach ($s in @($d.Symbols)) {
            try { $o = Get-P $s 'Object' } catch { $o = $null }
            if ($o -and ($o.ClassName -eq 'Message' -or $o.ClassName -like '*Fragment*')) { $objs += $o }
        }
        foreach ($o in $objs) { try { $o.Delete() } catch {} }
        $d.Delete()
        "  reemplazado: $name ($($objs.Count) mensajes y fragmentos anteriores eliminados)"
    }
}

function Get-SeqObject($model, $ll) {
    if ($ll[2] -eq 'actor') {
        $o = @($model.Actors) | Where-Object { $_.Name -eq $ll[1] } | Select-Object -First 1
        if (-not $o) { throw "actor no definido en UC-01: $($ll[1])" }
        return $o
    }
    $o = @($model.Objects) | Where-Object { $_.Name -eq $ll[1] } | Select-Object -First 1
    if (-not $o) {
        $o = $model.CreateObject($PdKind.UMLObject)
        $o.Name = $ll[1]
        try { $o.Code = 'OBJ_' + ($ll[1] -replace '[^A-Za-z0-9]+', '_') } catch {}
    }
    if ($ll.Count -gt 3 -and $ll[3]) { $o.Stereotype = $ll[3] }
    $o
}

function New-Sequence($model, [string]$name, [string]$code, $spec) {
    Remove-Sequence $model $name | ForEach-Object { Write-Host $_ }
    $sd = $model.SequenceDiagrams.CreateNew()
    $sd.Name = $name; $sd.Code = $code
    $objs = @{}; $syms = @{}; $x = 0
    foreach ($ll in $spec.Lifelines) {
        $o = Get-SeqObject $model $ll
        $objs[$ll[0]] = $o
        $syms[$ll[0]] = $sd.AttachObject($o)
        Set-Pos $syms[$ll[0]] $x 0
        $x += $spec.Gap
    }
    $lastX = $x - $spec.Gap

    $msgSyms = @()
    foreach ($ms in $spec.Messages) {
        $m = $model.CreateObject($PdKind.Message)
        $m.Object1 = $objs[$ms[0]]; $m.Object2 = $objs[$ms[1]]
        $m.Name = $ms[2]
        if ($ms.Count -gt 3 -and $ms[3] -eq 'return') { try { $m.ControlFlow = 'R' } catch {} }
        $msgSyms += $sd.AttachLinkObject($m, $syms[$ms[0]], $syms[$ms[1]])
    }

    # Al adjuntar los mensajes PowerDesigner recoloca algunas lifelines: se vuelven a
    # fijar sobre la rejilla y los objetos se ensanchan para que su nombre quepa.
    $x = 0
    foreach ($ll in $spec.Lifelines) {
        $s = $syms[$ll[0]]; $r = Get-Rect $s
        $w = $r.R - $r.L
        $t = $r.T
        if ($ll[2] -ne 'actor') {
            $w = [Math]::Min($spec.Gap - 1500, 9500)
            # Ancho propio: un estereotipo largo que se parte en dos líneas se encima con el nombre.
            if ($ll.Count -gt 4 -and $ll[4]) { $w = [int]$ll[4] }
            if ($ll[1].Length -gt 40 -or ($ll.Count -gt 3 -and $ll[3])) { $t = $r.B + 4900 }
        }
        Set-Rect $s ([int]($x - $w / 2)) $t ([int]($x + $w / 2)) $r.B
        $x += $spec.Gap
    }

    # Espacio extra antes de un mensaje que abre un fragmento o un else: la guarda del
    # operando y el rótulo del mensaje quedan así en filas distintas.
    $opens = @{}
    foreach ($fr in $spec.Fragments) {
        $opens[[int]$fr.From] = 1 + [int]$opens[[int]$fr.From]
        foreach ($e in @($fr.Else)) { if ($e) { $opens[[int]$e[0]] = 1 + [int]$opens[[int]$e[0]] } }
    }
    # Y antes del mensaje que sigue a un fragmento: su rótulo no pisa el borde inferior.
    $closes = @{}
    foreach ($fr in $spec.Fragments) { $closes[[int]$fr.To + 1] = 1 }
    $ys = @()
    $y = -6000 + $spec.Row
    for ($i = 0; $i -lt $msgSyms.Count; $i++) {
        $ms = $spec.Messages[$i]
        $y = $y - $spec.Row - 2600 * [int]$opens[$i + 1] - 1500 * [int]$closes[$i + 1]
        $x1 = [int](Get-Center $syms[$ms[0]])[0]; $x2 = [int](Get-Center $syms[$ms[1]])[0]
        $pts = $Pd.NewPtList()
        if ($ms[0] -eq $ms[1]) {
            # Automensaje: bucle a la derecha de la lifeline.
            $pts.Add($Pd.NewPoint($x1, $y + 500)) | Out-Null
            $pts.Add($Pd.NewPoint($x1 + 2600, $y + 500)) | Out-Null
            $pts.Add($Pd.NewPoint($x1 + 2600, $y - 500)) | Out-Null
            $pts.Add($Pd.NewPoint($x1, $y - 500)) | Out-Null
        } else {
            $pts.Add($Pd.NewPoint($x1, $y)) | Out-Null
            $pts.Add($Pd.NewPoint($x2, $y)) | Out-Null
        }
        $msgSyms[$i].SetAttribute('ListOfPoints', $pts) | Out-Null
        # Un desplazamiento mínimo obliga a recalcular el rótulo sobre la fila nueva.
        # En un automensaje el rótulo va a la derecha del bucle, fuera de la lifeline.
        $dx = 0; if ($ms[0] -eq $ms[1]) { $dx = [int]([Math]::Min($ms[2].Length, 40) * 175 + 1500) }
        $msgSyms[$i].SetAttribute('CenterTextOffset', $Pd.NewPoint($dx, 1)) | Out-Null
        $ys += $y
    }

    foreach ($fr in $spec.Fragments) {
        $xs = @($fr.Lanes | ForEach-Object { (Get-Center $syms[$_])[0] })
        $l = ($xs | Measure-Object -Minimum).Minimum - $fr.Pad
        $r = ($xs | Measure-Object -Maximum).Maximum + $fr.Pad
        $top = $ys[$fr.From - 1] + 2800 + $fr.Nest * 450
        # Un fragmento anidado cierra por encima del que lo contiene.
        $bottom = $ys[$fr.To - 1] - 1700 + $fr.Nest * 400
        $f = $model.CreateObject($PdKind.InteractionFragment)
        $f.FragmentType = $fr.Type
        # Regiones antes de adjuntar el símbolo: el símbolo toma la geometría de las
        # regiones al crearse. La guarda del primer operando va en la primera región;
        # alt nace con dos y la segunda es el else.
        $regs = @($f.Regions)
        if ($regs.Count -gt 0) { if ($fr.Cond) { $regs[0].Condition = $fr.Cond } } elseif ($fr.Cond) { $f.Condition = $fr.Cond }
        if ($fr.Else) {
            # El separador va justo bajo el último mensaje del primer operando; el hueco
            # restante queda para la guarda del else y el rótulo del mensaje siguiente.
            $cut = [int]($ys[$fr.Else[0][0] - 2] - 1300)
            if ($regs.Count -gt 0) { try { $regs[0].Size = [int]($top - $cut) } catch {} }
            $j = 1
            foreach ($e in $fr.Else) {
                $regs = @($f.Regions)
                if ($regs.Count -gt $j) { $rg = $regs[$j] } else { $rg = $f.Regions.CreateNew() }
                $rg.Condition = $e[1]
                try { $rg.Size = [int]($cut - $bottom) } catch {}
                $j++
            }
        } elseif ($regs.Count -gt 0) {
            try { $regs[0].Size = [int]($top - $bottom) } catch {}
        }
        $fs = $sd.AttachObject($f)
        Set-Rect $fs ([int]$l) ([int]$top) ([int]$r) ([int]$bottom)
    }

    # Notas a la derecha de la última lifeline, a la altura del mensaje indicado.
    foreach ($nt in $spec.Notes) {
        $w = $nt[2]
        Add-Note $sd $nt[0] ([int]($lastX + $w / 2 + 6000)) $ys[$nt[1] - 1] $w | Out-Null
    }
    # Divisores de tramo a la izquierda de la primera lifeline.
    foreach ($dv in $spec.Dividers) {
        Add-Note $sd $dv[1] -12000 ($ys[$dv[0] - 1] + 1200) 14000 | Out-Null
    }
    # El marco de la interacción se ensancha para abarcar notas y divisores. Su borde
    # inferior no se toca: las lifelines conservan su largo propio.
    $left = -11000; if ($spec.Dividers.Count) { $left = -20500 }
    $right = $lastX + $spec.Gap / 2
    foreach ($nt in $spec.Notes) { $right = [Math]::Max($right, $lastX + $nt[2] + 7500) }
    foreach ($s in @($sd.Symbols)) {
        if ((Get-P $s 'ClassName') -eq 'Interaction Symbol') {
            $r = Get-Rect $s
            Set-Rect $s ([int]$left) $r.T ([int]$right) $r.B
        }
    }
    $sd
}
