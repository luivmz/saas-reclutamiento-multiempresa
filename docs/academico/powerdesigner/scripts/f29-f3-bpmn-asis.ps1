# F29 — Vista F3 «F3 - BPMN AS-IS» en F29_BPM_Academico.bpm.
#
# Especificación: docs/academico/practica-03/POWERDESIGNER_PENDING.md (cerrada en la F27D).
# Nombres: glosario y actividades de docs/academico/tools/f27b/m_asis.py. Cada nodo se
# rotula «ID + nombre oficial» y el nombre oficial se conserva literal.
#
# Tres fases: (1) objetos y símbolos, (2) geometría (pools, carriles, nodos y el
# subproceso expandido), (3) rutas. PowerDesigner agranda un carril cuando recibe un
# símbolo y reubica símbolos al cambiar la geometría; por eso las rutas van al final.
#
# Requiere f29lib.ps1 cargado. Reemplaza el paquete F3 entero en cada corrida.

$ErrorActionPreference = 'Stop'
Open-F29
try {
    $m = Get-F29Model $F29Bpm
    Write-Host "F3 - BPMN AS-IS en $($m.Name)"
    $v = Reset-BpmView $m 'F3' 'F3 - AS-IS preliminar' 'F3 - BPMN AS-IS'
    $pk = $v.Package; $d = $v.Diagram
    $d.Comment = 'F3 BPMN AS-IS preliminar - Reclutamiento y seleccion. Formalizacion F29 de docs/academico/practica-03/POWERDESIGNER_PENDING.md.'
    Set-DisplayPref $d @{
        'SwimlaneVert' = 'No'; 'Activate automatic link routing' = 'No'
        'ProcessStart.DisplayName' = 'Yes'; 'ProcessEnd.DisplayName' = 'Yes'
        'Process.Stereotype' = 'No'; 'ProcessStart.Stereotype' = 'No'; 'ProcessEnd.Stereotype' = 'No'
        'Decision.Stereotype' = 'No'; 'Flow.Stereotype' = 'No'; 'OrganizationUnit.Stereotype' = 'No'
    }
    Set-DiagramFont $d 9

    # ================================================================ fase 1: objetos
    $poolC = Get-OU $m 'Colegio Andino de Huancayo — AS-IS preliminar' 'POOL_COLEGIO_ASIS' 'Pool'
    $poolP = Get-OU $m 'Postulante' 'POOL_POSTULANTE' 'Pool'
    $area = Get-OU $m 'Área solicitante' 'LANE_AREA_SOLICITANTE' 'Lane'
    $dir = Get-OU $m 'Dirección' 'LANE_DIRECCION' 'Lane'
    $rrhh = Get-OU $m 'RR. HH.' 'LANE_RRHH' 'Lane'
    $eva = Get-OU $m 'Evaluadores' 'LANE_EVALUADORES' 'Lane'
    # El pool Postulante no tiene carriles; PowerDesigner exige uno, que queda sin nombre.
    $pst = Get-OU $m ' ' 'LANE_POSTULANTE' 'Lane'

    # RR. HH. y Evaluadores quedan contiguos para que SP-01 (AS-09 a AS-11) abarque los
    # dos carriles. El orden de los carriles no tiene significado en BPMN.
    $PoolCol = New-Pool $m $d $poolC @($area, $dir, $rrhh, $eva)
    $PoolPos = New-Pool $m $d $poolP @($pst)

    $yA = 56000; $yD = 46000; $yH = 30500; $yH2 = 37000; $yE = 20000; $yP = 5000
    $TW = 8800; $TH = 5000; $EV = 1500; $GW = 5200; $GH = 3600
    $n = @{}; $pos = @{}
    function Node($id, $kind, $name, $stereo, $lane, $laneOU, $x, $y, $w, $h, $container = $pk) {
        $diag = $d; if ($container -ne $pk) { $diag = $null }
        $n[$id] = New-BpmNode $container $diag $kind "$id $name" ('F3_' + ($id -replace '-', '_')) $stereo $lane $laneOU $x $y $w $h
        $pos[$id] = @($x, $y, $w, $h)
    }
    $LA = $PoolCol.Lanes[$area.Name]; $LD = $PoolCol.Lanes[$dir.Name]; $LH = $PoolCol.Lanes[$rrhh.Name]
    $LP = $PoolPos.Lanes[$pst.Name]

    Node 'EI-01' Start 'Necesidad de personal identificada' 'Start Event' $LA $area 6000 $yA $EV $EV
    Node 'AS-01' Process 'Identificar la necesidad de personal' 'Task' $LA $area 17000 $yA $TW $TH
    Node 'AS-02' Process 'Comunicar la necesidad a RR. HH.' 'Task' $LA $area 29000 $yA $TW $TH
    Node 'AS-03' Process 'Revisar la necesidad' 'Task' $LH $rrhh 40000 $yH $TW $TH
    Node 'AS-04' Process 'Aprobar o no aprobar la necesidad' 'Task' $LD $dir 51000 $yD $TW $TH
    Node 'G-01' Decision '¿Necesidad aprobada?' 'Exclusive Gateway' $LD $dir 63000 $yD $GW $GH
    Node 'EF-01' End 'Necesidad no aprobada' 'End Event' $LD $dir 75000 $yD $EV $EV
    Node 'AS-05' Process 'Definir el perfil del puesto' 'Task' $LH $rrhh 75000 $yH $TW $TH
    Node 'AS-06' Process 'Difundir la convocatoria' 'Task' $LH $rrhh 87000 $yH $TW $TH
    Node 'AS-08' Process 'Recibir y reunir postulaciones y CV' 'Receive Task' $LH $rrhh 99000 $yH $TW $TH
    Node 'AS-12' Process 'Consolidar resultados y comparar candidatos' 'Task' $LH $rrhh 180000 $yH $TW $TH
    Node 'AS-13' Process 'Decidir el candidato seleccionado' 'Task' $LD $dir 192000 $yD $TW $TH
    Node 'AS-14' Process 'Comunicar el resultado' 'Task' $LH $rrhh 204000 $yH $TW $TH
    Node 'EF-03' End 'Resultado comunicado' 'End Event' $LH $rrhh 216000 $yH $EV $EV
    Node 'EP-01' Process 'Convocatoria recibida' 'Message Start Event' $LP $null 87000 $yP $EV $EV
    Node 'AS-07' Process 'Presentar la postulación y el CV' 'Task' $LP $null 99000 $yP $TW $TH
    Node 'EP-02' End 'Postulación presentada' 'End Event' $LP $null 111000 $yP $EV $EV

    # SP-01: subproceso expandido de instancia múltiple paralela.
    $sp = $pk.CreateObject($BpmKind.Process)
    $sp.Name = 'SP-01 Evaluar al candidato'; $sp.Code = 'F3_SP_01'
    Set-P $sp 'Composite' $true
    $sp.Stereotype = 'Sub-Process'
    $sp.SetExtendedAttribute('LoopCharacteristics', 'Multi-Instance Parallel') | Out-Null
    Set-P $sp 'OrganizationUnit' $rrhh
    $sp.Comment = 'Instancia multiple paralela: una instancia por candidato cuya postulacion reunio AS-08. Termina cuando todas las instancias terminaron (EF-02 o EF-04).'
    Node 'SI-01' Start 'Candidato a evaluar' 'Start Event' $null $rrhh 108500 $yH $EV $EV $sp
    Node 'AS-09' Process 'Revisar el CV y preseleccionar al candidato' 'Task' $null $rrhh 119000 $yH $TW $TH $sp
    Node 'G-02' Decision '¿Candidato preseleccionado?' 'Exclusive Gateway' $null $rrhh 131000 $yH $GW $GH $sp
    Node 'EF-02' End 'El candidato no continúa' 'End Event' $null $rrhh 131000 $yH2 $EV $EV $sp
    Node 'AS-10' Process 'Coordinar evaluaciones y entrevistas' 'Task' $null $rrhh 143000 $yH $TW $TH $sp
    Node 'AS-11' Process 'Realizar evaluaciones y entrevistas' 'Task' $null $eva 155000 $yE $TW $TH $sp
    Node 'EF-04' End 'Candidato evaluado' 'End Event' $null $eva 164500 $yE $EV $EV $sp
    $flows = @{}
    foreach ($f in @(@('SI-01', 'AS-09', ''), @('AS-09', 'G-02', ''), @('G-02', 'EF-02', 'No'),
            @('G-02', 'AS-10', 'Sí'), @('AS-10', 'AS-11', ''), @('AS-11', 'EF-04', ''))) {
        $flows[$f[0] + '>' + $f[1]] = New-BpmFlow $sp $n[$f[0]].Obj $n[$f[1]].Obj 'Sequence Flow' $f[2] $null $null
    }
    $spSym = $d.AttachObject($sp)
    Set-P $spSym 'CompositeView' $true
    $n['SP-01'] = @{ Obj = $sp; Sym = $spSym }
    $SPL = 104000; $SPR = 171000; $SPT = 40500; $SPB = 15600

    # Flujos de secuencia del nivel del proceso y de los pools.
    foreach ($f in @(@('EI-01', 'AS-01', ''), @('AS-01', 'AS-02', ''), @('AS-02', 'AS-03', ''), @('AS-03', 'AS-04', ''),
            @('AS-04', 'G-01', ''), @('G-01', 'EF-01', 'No'), @('G-01', 'AS-05', 'Sí'), @('AS-05', 'AS-06', ''),
            @('AS-06', 'AS-08', ''), @('AS-08', 'SP-01', ''), @('SP-01', 'AS-12', ''), @('AS-12', 'AS-13', ''),
            @('AS-13', 'AS-14', ''), @('AS-14', 'EF-03', ''), @('EP-01', 'AS-07', ''), @('AS-07', 'EP-02', ''))) {
        $flows[$f[0] + '>' + $f[1]] = New-BpmFlow $pk $n[$f[0]].Obj $n[$f[1]].Obj 'Sequence Flow' $f[2] $null $null
    }

    # Mensajes MF-01 a MF-04: formato de mensaje (rótulo) y flujo de mensaje.
    foreach ($o in @($m.GetCollectionByName('MessageFormats'))) { if ($o -and $o.Code -like 'F3_MF_*') { $o.Delete() | Out-Null } }
    $msgs = @(
        @('MF-01', 'Convocatoria', 'AS-06', 'EP-01'), @('MF-02', 'Postulación y CV', 'AS-07', 'AS-08'),
        @('MF-03', 'Citación', 'AS-10', $null), @('MF-04', 'Resultado', 'AS-14', $null)
    )
    foreach ($mf in $msgs) {
        $fo = $m.CreateObject($BpmKind.MessageFormat)
        $fo.Name = $mf[0] + ' ' + $mf[1]; $fo.Code = 'F3_' + ($mf[0] -replace '-', '_')
        # MF-03 y MF-04 llegan al borde del pool Postulante (sin evento receptor).
        if ($mf[3]) { $dst = $n[$mf[3]].Obj } else { $dst = $poolP }
        $fl = New-BpmFlow $pk $n[$mf[2]].Obj $dst 'Message Flow' '' $null $fo
        $fl.Code = 'F3_' + ($mf[0] -replace '-', '_') + '_FLOW'
        $flows[$mf[0]] = $fl
    }

    # ================================================================ fase 2: geometría
    $R = 222000
    function Layout {
        # Un pool redimensionado sobre otro se fusiona con él: se aparta el Postulante,
        # se coloca el Colegio y al final el Postulante.
        Set-PoolGeometry $PoolPos 0 $R -400000 @(10000)
        Set-PoolGeometry $PoolCol 0 $R 15000 @(10000, 10000, 16000, 10000)
        Set-PoolGeometry $PoolPos 0 $R 0 @(10000)
        foreach ($id in $pos.Keys) {
            if ($n[$id].Sym) { $q = $pos[$id]; Set-Box $n[$id].Sym $q[0] $q[1] $q[2] $q[3] }
        }
        # SP-01 va en el nivel superior del diagrama, sobre RR. HH. y Evaluadores: dentro
        # de un carril quedaría recortado por él.
        $par = Get-P $spSym 'Parent'
        if ((Get-P $par 'ClassName') -ne 'Business Process Diagram') {
            (Get-C $par 'SubSymbols').Remove($spSym) | Out-Null
            (Get-C $d 'Symbols').Add($spSym) | Out-Null
        }
        Set-Rect $spSym $SPL $SPT $SPR $SPB
        foreach ($id in 'SI-01', 'AS-09', 'G-02', 'EF-02', 'AS-10', 'AS-11', 'EF-04') {
            $s = Find-SymbolDeep (Get-C $spSym 'SubSymbols') $n[$id].Obj
            if (-not $s) { throw "Sin símbolo para $id dentro de SP-01" }
            $n[$id].Sym = $s
            $q = $pos[$id]; Set-Box $s $q[0] $q[1] $q[2] $q[3]
        }
    }
    Layout
    Layout   # segunda pasada: los carriles pudieron crecer al recibir los nodos

    # ================================================================ fase 3: rutas
    function Rc($id) { Get-Rect $n[$id].Sym }
    function Route($key, $a, $b, $pts, $center = @(0, 1), $src = $null) {
        $ls = Get-FlowSymbol $d $flows[$key] $n[$a].Sym $n[$b].Sym
        Set-LinkPoints $ls $pts $center $src
    }
    function Seq($a, $b, $pts, $src = $null) { Route ($a + '>' + $b) $a $b $pts @(0, 1) $src }
    Seq 'EI-01' 'AS-01' @(@((Rc 'EI-01').R, $yA), @((Rc 'AS-01').L, $yA))
    Seq 'AS-01' 'AS-02' @(@((Rc 'AS-01').R, $yA), @((Rc 'AS-02').L, $yA))
    Seq 'AS-02' 'AS-03' @(@((Rc 'AS-02').R, $yA), @(40000, $yA), @(40000, (Rc 'AS-03').T))
    Seq 'AS-03' 'AS-04' @(@((Rc 'AS-03').R, $yH), @(51000, $yH), @(51000, (Rc 'AS-04').B))
    Seq 'AS-04' 'G-01' @(@((Rc 'AS-04').R, $yD), @((Rc 'G-01').L, $yD))
    Seq 'G-01' 'EF-01' @(@((Rc 'G-01').R, $yD), @((Rc 'EF-01').L, $yD)) @(-300, 700)
    Seq 'G-01' 'AS-05' @(@(63000, (Rc 'G-01').B), @(63000, $yH), @((Rc 'AS-05').L, $yH)) @(900, -900)
    Seq 'AS-05' 'AS-06' @(@((Rc 'AS-05').R, $yH), @((Rc 'AS-06').L, $yH))
    Seq 'AS-06' 'AS-08' @(@((Rc 'AS-06').R, $yH), @((Rc 'AS-08').L, $yH))
    Seq 'AS-08' 'SP-01' @(@((Rc 'AS-08').R, $yH), @($SPL, $yH))
    Seq 'SP-01' 'AS-12' @(@($SPR, $yH), @((Rc 'AS-12').L, $yH))
    Seq 'AS-12' 'AS-13' @(@((Rc 'AS-12').R, $yH), @(192000, $yH), @(192000, (Rc 'AS-13').B))
    Seq 'AS-13' 'AS-14' @(@((Rc 'AS-13').R, $yD), @(204000, $yD), @(204000, (Rc 'AS-14').T))
    Seq 'AS-14' 'EF-03' @(@((Rc 'AS-14').R, $yH), @((Rc 'EF-03').L, $yH))
    Seq 'EP-01' 'AS-07' @(@((Rc 'EP-01').R, $yP), @((Rc 'AS-07').L, $yP))
    Seq 'AS-07' 'EP-02' @(@((Rc 'AS-07').R, $yP), @((Rc 'EP-02').L, $yP))
    Seq 'SI-01' 'AS-09' @(@((Rc 'SI-01').R, $yH), @((Rc 'AS-09').L, $yH))
    Seq 'AS-09' 'G-02' @(@((Rc 'AS-09').R, $yH), @((Rc 'G-02').L, $yH))
    Seq 'G-02' 'EF-02' @(@(131000, (Rc 'G-02').T), @(131000, (Rc 'EF-02').B)) @(700, 200)
    Seq 'G-02' 'AS-10' @(@((Rc 'G-02').R, $yH), @((Rc 'AS-10').L, $yH)) @(-200, 700)
    Seq 'AS-10' 'AS-11' @(@((Rc 'AS-10').R, $yH), @(155000, $yH), @(155000, (Rc 'AS-11').T))
    Seq 'AS-11' 'EF-04' @(@((Rc 'AS-11').R, $yE), @((Rc 'EF-04').L, $yE))

    $pBorder = 10000   # borde superior del pool Postulante
    $n['POOL-P'] = @{ Obj = $poolP; Sym = $PoolPos.Sym }
    Route 'MF-01' 'AS-06' 'EP-01' @(@(87000, (Rc 'AS-06').B), @(87000, (Rc 'EP-01').T)) @(-5200, 1)
    Route 'MF-02' 'AS-07' 'AS-08' @(@(99000, (Rc 'AS-07').T), @(99000, (Rc 'AS-08').B)) @(6200, 1)
    Route 'MF-03' 'AS-10' 'POOL-P' @(@(143000, (Rc 'AS-10').B), @(143000, $pBorder)) @(-3600, -6300)
    Route 'MF-04' 'AS-14' 'POOL-P' @(@(204000, (Rc 'AS-14').B), @(204000, $pBorder)) @(-3800, 1)

    # SP-01 se dibuja con relleno blanco (vista compuesta). Por eso la división entre
    # RR. HH. y Evaluadores se prolonga dentro de él con una línea discontinua, y MF-03
    # se lleva al frente para que se vea desde AS-10.
    $div = Add-Frame $d ($SPL + 300) 25040 ($SPR - 300) 24960 2
    Set-P $div 'LineColor' 12615680   # azul de los carriles (RGB 0, 128, 192)
    Move-ToFront $d $div
    Move-ToFront $d (Get-FlowSymbol $d $flows['MF-03'] $null $null)

    # Rótulos de eventos y compuertas: «ID» y nombre oficial.
    function Lbl($id, $dx, $dy, $w = 9000) {
        $c = Get-Center $n[$id].Sym
        $t = $n[$id].Obj.Name -replace '^(\S+) ', "`$1`r`n"
        Add-Label $d $t ($c[0] + $dx) ($c[1] + $dy) $w | Out-Null
    }
    Lbl 'EI-01' 0 -2300; Lbl 'EF-01' 0 -2300; Lbl 'EF-03' 0 -2300 8000
    Lbl 'EP-01' 0 -2300; Lbl 'EP-02' 0 -2300
    Lbl 'G-01' 0 3300 10000
    Lbl 'SI-01' 0 -2300 7000; Lbl 'G-02' 0 -3300 10000; Lbl 'EF-02' 5600 0 9000; Lbl 'EF-04' 0 2400 7000

    # Título y anotaciones obligatorias, al frente de los pools.
    Add-Text $d "F3 BPMN AS-IS preliminar — Reclutamiento y selección`r`nCaso de estudio: Colegio Andino de Huancayo. Modelo de negocio del proceso actual, no del software. Formalización F29 en PowerDesigner." 0 68000 150000 63000 | Out-Null
    foreach ($nt in @(
            @('AS-IS preliminar derivado del análisis del equipo, sujeto a validación institucional', 120000, 59500, 176000, 53000),
            @('No está verificado si se informa al candidato que no continúa', 111000, 39800, 127000, 34200),
            @('SP-01: subproceso de instancia múltiple paralela (marcador |||), una instancia por candidato cuya postulación reunió AS-08. Continúa hacia AS-12 cuando todas las instancias terminaron (EF-02 o EF-04).', 4000, 24500, 62000, 17000))) {
        $ns = Add-Note $d $nt[0] $nt[1] $nt[2] $nt[3] $nt[4]
        Move-ToFront $d $ns
    }

    # ================================================================ verificación
    $g = Get-BpmGraph $pk
    $expNames = @{
        'EI-01' = 'Necesidad de personal identificada'; 'G-01' = '¿Necesidad aprobada?'; 'EF-01' = 'Necesidad no aprobada'
        'SP-01' = 'Evaluar al candidato'; 'SI-01' = 'Candidato a evaluar'; 'G-02' = '¿Candidato preseleccionado?'
        'EF-02' = 'El candidato no continúa'; 'EF-04' = 'Candidato evaluado'; 'EF-03' = 'Resultado comunicado'
        'EP-01' = 'Convocatoria recibida'; 'EP-02' = 'Postulación presentada'
        'AS-01' = 'Identificar la necesidad de personal'; 'AS-02' = 'Comunicar la necesidad a RR. HH.'
        'AS-03' = 'Revisar la necesidad'; 'AS-04' = 'Aprobar o no aprobar la necesidad'; 'AS-05' = 'Definir el perfil del puesto'
        'AS-06' = 'Difundir la convocatoria'; 'AS-07' = 'Presentar la postulación y el CV'; 'AS-08' = 'Recibir y reunir postulaciones y CV'
        'AS-09' = 'Revisar el CV y preseleccionar al candidato'; 'AS-10' = 'Coordinar evaluaciones y entrevistas'
        'AS-11' = 'Realizar evaluaciones y entrevistas'; 'AS-12' = 'Consolidar resultados y comparar candidatos'
        'AS-13' = 'Decidir el candidato seleccionado'; 'AS-14' = 'Comunicar el resultado'
    }
    $expSeq = @('EI-01>AS-01', 'AS-01>AS-02', 'AS-02>AS-03', 'AS-03>AS-04', 'AS-04>G-01', 'G-01>EF-01[No]', 'G-01>AS-05[Sí]',
        'AS-05>AS-06', 'AS-06>AS-08', 'AS-08>SP-01', 'SP-01>AS-12', 'AS-12>AS-13', 'AS-13>AS-14', 'AS-14>EF-03',
        'SI-01>AS-09', 'AS-09>G-02', 'G-02>EF-02[No]', 'G-02>AS-10[Sí]', 'AS-10>AS-11', 'AS-11>EF-04',
        'EP-01>AS-07', 'AS-07>EP-02')
    $expMsg = @('MF-01:AS-06>EP-01', 'MF-02:AS-07>AS-08', 'MF-03:AS-10>POOL_POSTULANTE', 'MF-04:AS-14>POOL_POSTULANTE')
    function Id($code) { if ($code -like 'F3_*') { ($code.Substring(3) -replace '_', '-') } else { $code } }
    $fail = @(); $out = @()
    $out += "F29 - verificación de la vista F3 - BPMN AS-IS ($(Get-Date -Format 'yyyy-MM-dd HH:mm'))"
    $out += "Modelo: docs/academico/powerdesigner/models/F29_BPM_Academico.bpm; paquete F3; diagrama «$($d.Name)»"
    $out += ''
    # Nombres literales.
    foreach ($id in $expNames.Keys | Sort-Object) {
        $code = 'F3_' + ($id -replace '-', '_')
        $nd = $g.Nodes[$code]
        if (-not $nd) { $fail += "falta $id" }
        elseif ($nd.Name -ne "$id $($expNames[$id])") { $fail += "nombre de ${id}: «$($nd.Name)»" }
    }
    $extra = @($g.Nodes.Keys | Where-Object { -not $expNames.ContainsKey((Id $_)) })
    if ($extra.Count) { $fail += "nodos no especificados: $($extra -join ', ')" }
    $tasks = @($g.Nodes.Values | Where-Object { $_.Stereo -in 'Task', 'Receive Task' })
    $gws = @($g.Nodes.Values | Where-Object { $_.Kind -eq 'ProcessDecisions' })
    $evs = @($g.Nodes.Values | Where-Object { $_.Kind -in 'ProcessStarts', 'ProcessEnds' -or $_.Stereo -eq 'Message Start Event' })
    $sps = @($g.Nodes.Values | Where-Object { $_.Composite })
    $mi = $sp.GetExtendedAttribute('LoopCharacteristics')
    $out += "Tareas: $($tasks.Count) (esperadas 14) · subprocesos: $($sps.Count) (1, $mi) · compuertas: $($gws.Count) (2) · eventos: $($evs.Count) (6 + 2)"
    if ($tasks.Count -ne 14) { $fail += 'tareas' }; if ($gws.Count -ne 2) { $fail += 'compuertas' }; if ($evs.Count -ne 8) { $fail += 'eventos' }
    if ($sps.Count -ne 1 -or $mi -ne 'Multi-Instance Parallel') { $fail += 'SP-01 instancia múltiple paralela' }
    # Flujos.
    $seq = @($g.Flows | Where-Object { $_.Stereo -eq 'Sequence Flow' } | ForEach-Object { (Id $_.Src) + '>' + (Id $_.Dst) + $(if ($_.Cond) { "[$($_.Cond)]" }) })
    $msg = @($g.Flows | Where-Object { $_.Stereo -eq 'Message Flow' } | ForEach-Object { ($_.Format -split ' ')[0] + ':' + (Id $_.Src) + '>' + (Id $_.Dst) })
    $d1 = Compare-Object ($expSeq | Sort-Object) ($seq | Sort-Object); $d2 = Compare-Object ($expMsg | Sort-Object) ($msg | Sort-Object)
    $out += "Flujos de secuencia: $($seq.Count) (esperados $($expSeq.Count)) · flujos de mensaje: $($msg.Count) (4, unidireccionales)"
    if ($d1) { $fail += 'secuencia: ' + (($d1 | ForEach-Object { $_.SideIndicator + $_.InputObject }) -join ' ') }
    if ($d2) { $fail += 'mensajes: ' + (($d2 | ForEach-Object { $_.SideIndicator + $_.InputObject }) -join ' ') }
    # Conectividad: toda actividad y compuerta tiene entrada y salida de secuencia.
    foreach ($nd in $g.Nodes.Values) {
        $id = Id $nd.Code
        $in = @($seq | Where-Object { ($_ -replace '\[.*\]', '') -like "*>$id" }).Count
        $ou = @($seq | Where-Object { $_ -like "$id>*" }).Count
        $isStart = $nd.Kind -eq 'ProcessStarts' -or $nd.Stereo -eq 'Message Start Event'
        if (-not $isStart -and $in -lt 1) { $fail += "$id sin entrada" }
        if ($nd.Kind -ne 'ProcessEnds' -and $ou -lt 1) { $fail += "$id sin salida" }
    }
    $out += "Conectividad: todas las actividades y compuertas tienen entrada y salida; AS-06 -> AS-08 es flujo de secuencia: $($seq -contains 'AS-06>AS-08')"
    # Carriles de cada tarea (atributo OrganizationUnit).
    $laneOf = @{}
    foreach ($id in $n.Keys) { $o = $n[$id].Obj; try { $ou = Get-P $o 'OrganizationUnit'; if ($ou) { $laneOf[$id] = $ou.Name } } catch {} }
    $out += 'Responsable (carril) por nodo: ' + (($laneOf.Keys | Sort-Object | ForEach-Object { "$_=$($laneOf[$_])" }) -join '; ')
    $ck = Test-F29BpmCheck $m
    $out += $ck.Lines
    if (-not $ck.Ok) { $fail += 'Check Model: hallazgos no explicados por la especificación' }
    $out += ''
    if ($fail.Count) { $out += 'RESULTADO: FALLA'; $out += $fail } else { $out += 'RESULTADO: PASS' }
    Write-F29Report (Join-Path $F29Root 'validation\F3_model_check.txt') $out
    $out | ForEach-Object { Write-Host "  $_" }

    Save-F29Model $m
    Export-F29 $d 'F3_BPMN_ASIS'
    Write-Host "  nodos: $($pos.Count) + SP-01; flujos: $($flows.Count)"
} finally { Close-F29 }
