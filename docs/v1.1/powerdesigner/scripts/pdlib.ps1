# Biblioteca común de los scripts de construcción de la Fase 23.
#
# Maneja PowerDesigner 16.6 por su interfaz COM (la misma API que usan los
# scripts VBScript de ejemplo de la instalación). No escribe archivos .oom/.pdm
# a mano: es PowerDesigner quien crea, valida y guarda los modelos.
#
# Reglas que aplica siempre:
#   - InteractiveMode = 0 (im_Batch) durante el script y se restaura al salir,
#     para que ningún diálogo bloquee la sesión ni la de quien tenga la
#     herramienta abierta.
#   - Se guarda antes de cerrar: cerrar un modelo sin guardar abre «Guardar como».
#   - Solo se cierran los modelos que abre el script.

$ErrorActionPreference = 'Stop'

$Global:PdRoot = Split-Path -Parent $PSScriptRoot
$Global:PdModels = Join-Path $PdRoot 'models'
$Global:PdExports = Join-Path $PdRoot 'exports'
$Global:OomFile = Join-Path $PdModels 'saas-recruitment-v1.1-oom.oom'

# Clases de metamodelo (Ole Automation\VBScriptConstants.vbs, PowerDesigner 16.6.1)
$Global:PdKind = @{
    Model = 403775584; Package = 403775585; Class = 403775587; Attribute = 403775589
    Association = 403775594; Dependency = 403775593; Generalization = 403775591; Realization = 403775592
    Actor = 403775745; UseCase = 403775746; UseCaseAssociation = 403775603
    Component = 403776257; Interface = 403775588
    Node = 403777025; NodeAssociation = 403777027; ComponentInstance = 403777026
    UMLObject = 403776001; Message = 403776002; InteractionFragment = -168517650; InteractionReference = -641212436
    Activity = -837026074; Decision = -837026070; Start = -837026072; End = -837026071
    Flow = -837026047; OrganizationUnit = -837026067; Synchronization = -837026069
    State = 403777281; Transition = -837026068; Event = 403777283
    NoteSymbol = -1028641999; FileObject = 1334298391
}

# Coloca un símbolo como caja de centro (cx,cy) y tamaño w x h.
function Set-Box($sym, [int]$cx, [int]$cy, [int]$w, [int]$h) {
    Set-Rect $sym ($cx - [int]($w / 2)) ($cy + [int]($h / 2)) ($cx + [int]($w / 2)) ($cy - [int]($h / 2))
}

function Open-Pd {
    $Global:Pd = New-Object -ComObject 'PowerDesigner.Application'
    $Global:PdOrigMode = $Pd.InteractiveMode
    $Pd.InteractiveMode = 0
}

function Close-Pd {
    if ($Global:Pd) { $Pd.InteractiveMode = $Global:PdOrigMode }
}

function Get-P($o, $p) { $o.GetType().InvokeMember($p, 'GetProperty', $null, $o, $null) }
function Set-P($o, $p, $v) { $o.GetType().InvokeMember($p, 'SetProperty', $null, $o, @($v)) | Out-Null }

function Set-Pos($sym, [int]$x, [int]$y) { Set-P $sym 'Position' ($Pd.NewPoint($x, $y)) }
function Set-Rect($sym, [int]$l, [int]$t, [int]$r, [int]$b) { Set-P $sym 'Rect' ($Pd.NewRect($l, $t, $r, $b)) }
function Get-Rect($sym) {
    $r = Get-P $sym 'Rect'
    [pscustomobject]@{ L = Get-P $r 'Left'; T = Get-P $r 'Top'; R = Get-P $r 'Right'; B = Get-P $r 'Bottom' }
}

function New-Obj($parent, $kind, [string]$name, [string]$code = $null) {
    $o = $parent.CreateObject($PdKind[$kind])
    $o.Name = $name
    if ($code) { $o.Code = $code } else { try { $o.SetNameToCode() | Out-Null } catch {} }
    $o
}

# Nota con texto; el tamaño se calcula para que el texto no quede cortado.
function Add-Note($diagram, [string]$text, [int]$x, [int]$y, [int]$width = 9000) {
    $n = $diagram.Symbols.CreateNew($PdKind.NoteSymbol)
    $n.SetAttributeText('Text', $text) | Out-Null
    $lines = 0
    foreach ($l in ($text -split "`n")) { $lines += [Math]::Max(1, [Math]::Ceiling($l.Length * 360 / ($width - 600))) }
    $h = 800 + $lines * 1000
    Set-Rect $n ($x - [int]($width / 2)) ($y + [int]($h / 2)) ($x + [int]($width / 2)) ($y - [int]($h / 2))
    $n
}

function Get-Center($sym) { $r = Get-Rect $sym; @((($r.L + $r.R) / 2), (($r.T + $r.B) / 2), (($r.R - $r.L) / 2), (($r.T - $r.B) / 2)) }

# Punto donde la recta que sale de (cx,cy) en dirección (dx,dy) cruza el borde del rectángulo.
function Get-BorderPoint($c, [double]$dx, [double]$dy) {
    $t = [double]::MaxValue
    if ([Math]::Abs($dx) -gt 1e-9) { $t = [Math]::Min($t, $c[2] / [Math]::Abs($dx)) }
    if ([Math]::Abs($dy) -gt 1e-9) { $t = [Math]::Min($t, $c[3] / [Math]::Abs($dy)) }
    @([int]($c[0] + $dx * $t), [int]($c[1] + $dy * $t))
}

# Vínculo recto entre los bordes de dos símbolos. Si hay varios vínculos entre el
# mismo par, cada uno se desplaza en paralelo ($index de $count) para que sus
# roles y multiplicidades no se encimen. PowerDesigner no expone ListOfPoints como
# propiedad de escritura por IDispatch; SetAttribute sí la acepta.
function Set-StraightLink($ls, $symA, $symB, [int]$index = 0, [int]$count = 1, [int]$gap = 3400, [int]$alongA = 0, [int]$alongB = 0) {
    $a = Get-Center $symA; $b = Get-Center $symB
    $dx = $b[0] - $a[0]; $dy = $b[1] - $a[1]; $len = [Math]::Sqrt($dx * $dx + $dy * $dy)
    $ux = $dx / $len; $uy = $dy / $len; $px = -$uy; $py = $ux
    $shift = ($index - ($count - 1) / 2) * $gap
    $ca = @(($a[0] + $px * $shift), ($a[1] + $py * $shift), $a[2], $a[3])
    $cb = @(($b[0] + $px * $shift), ($b[1] + $py * $shift), $b[2], $b[3])
    $p1 = Get-BorderPoint $ca $ux $uy
    $p2 = Get-BorderPoint $cb (-$ux) (-$uy)
    $pts = $Pd.NewPtList()
    $pts.Add($Pd.NewPoint($p1[0], $p1[1])) | Out-Null
    $pts.Add($Pd.NewPoint($p2[0], $p2[1])) | Out-Null
    Set-P $ls 'CornerStyle' 0
    $ls.SetAttribute('ListOfPoints', $pts) | Out-Null
    # Un desplazamiento distinto de cero obliga a recalcular la posición de los
    # textos sobre la ruta nueva; se aparta un poco del trazo para que no lo tape.
    # Textos: los vínculos paralelos llevan sus rótulos hacia afuera, cada uno de su
    # lado; $alongA/$alongB los alejan del extremo para escalonar vecinos.
    $side = 400
    if ($count -gt 1) { $side = [Math]::Sign($index - ($count - 1) / 2 + 0.001) * 1100 }
    $sx = [int]($px * $side + $ux * $alongA); $sy = [int]($py * $side + $uy * $alongA)
    $dx2 = [int]($px * $side - $ux * $alongB); $dy2 = [int]($py * $side - $uy * $alongB)
    if ($sx -eq 0 -and $sy -eq 0) { $sy = 1 }
    if ($dx2 -eq 0 -and $dy2 -eq 0) { $dy2 = 1 }
    $ls.SetAttribute('SourceTextOffset', $Pd.NewPoint($sx, $sy)) | Out-Null
    $ls.SetAttribute('DestinationTextOffset', $Pd.NewPoint($dx2, $dy2)) | Out-Null
    $ls.SetAttribute('CenterTextOffset', $Pd.NewPoint(0, 1)) | Out-Null
}

# Marco gráfico con título arriba a la izquierda: agrupa símbolos sin ser un objeto del
# modelo. Se usa cuando la herramienta no permite anidar objetos que deben comunicarse.
function Add-Frame($diagram, [string]$title, [int]$cx, [int]$cy, [int]$w, [int]$h) {
    $r = $diagram.Symbols.CreateNew(906510177)
    Set-Box $r $cx $cy $w $h
    $t = $diagram.Symbols.CreateNew(906510179)
    $t.SetAttributeText('Text', $title) | Out-Null
    $l = $cx - [int]($w / 2) + 600; $top = $cy + [int]($h / 2) - 500
    Set-Rect $t $l $top ($l + [Math]::Max(14000, $title.Length * 380)) ($top - 1600)
    $r
}

# Muestra el nombre de dependencias y asociaciones de nodos (oculto por defecto en
# PowerDesigner); ahí van las etiquetas de F22 (condición del extend, puertos, "provee"...).
function Show-LinkNames($diagram) {
    $prefs = [string](Get-P $diagram 'DisplayPreferences')
    $prefs = $prefs.Replace('Dependency.DisplayName=No', 'Dependency.DisplayName=Yes')
    $prefs = $prefs.Replace('NodeAssociation.DisplayName=No', 'NodeAssociation.DisplayName=Yes')
    Set-P $diagram 'DisplayPreferences' $prefs
}

# Busca un diagrama por nombre en el modelo y en sus paquetes (AllDiagrams solo ve la raíz).
function Find-Diagram($container, [string]$name) {
    foreach ($d in @($container.AllDiagrams)) { if ($d.Name -eq $name) { return $d } }
    foreach ($p in @($container.Packages)) { $r = Find-Diagram $p $name; if ($r) { return $r } }
    $null
}

# Las dependencias sin rótulo en F22 llevan un espacio como nombre: con los nombres de
# dependencia visibles, PowerDesigner mostraría si no su nombre automático (Dependency_N).
$Global:BlankName = ' '

function Export-Diagram($diagram, [string]$fileBase) {
    $diagram.ExportImage((Join-Path $PdExports "$fileBase.png"))
    $diagram.ExportImage((Join-Path $PdExports "$fileBase.svg"))
}

function Save-Model($model, [string]$file) {
    $model.Save($file)
    # PowerDesigner deja una copia de respaldo (.pdb / .obb) al guardar sobre un archivo existente.
    Get-ChildItem (Split-Path $file) -File | Where-Object { $_.Extension -in '.pdb', '.oob', '.obb', '.bak' } | Remove-Item -Force
}
