# F29 — Vista F5 «F5 - BPMN TO-BE» en F29_BPM_Academico.bpm.
#
# Especificación: docs/academico/practica-05/POWERDESIGNER_PENDING.md (cerrada en la F27D).
# Nombres: docs/academico/tools/f27b/m_tobe.py (ACTIVIDADES, FUTURAS, EVENTOS, COMPUERTAS,
# MENSAJES). Cada nodo se rotula «ID + nombre oficial».
#
# Dos niveles: el nivel vacante (pool de la organización) y el nivel postulación
# (SP-P, subproceso expandido de instancia múltiple paralela). TB-30 es transversal y
# TB-F1 una propuesta futura desconectada. RF-29 no aparece.
#
# Mismas fases que F3: objetos, geometría y rutas. Requiere f29lib.ps1 cargado.

$ErrorActionPreference = 'Stop'
Open-F29
try {
    $m = Get-F29Model $F29Bpm
    Write-Host "F5 - BPMN TO-BE en $($m.Name)"
    $v = Reset-BpmView $m 'F5' 'F5 - TO-BE propuesto' 'F5 - BPMN TO-BE'
    $pk = $v.Package; $d = $v.Diagram
    $d.Comment = 'F5 BPMN TO-BE propuesto - Reclutamiento y seleccion. Formalizacion F29 de docs/academico/practica-05/POWERDESIGNER_PENDING.md.'
    Set-DisplayPref $d @{
        'SwimlaneVert' = 'No'; 'Activate automatic link routing' = 'No'
        'ProcessStart.DisplayName' = 'Yes'; 'ProcessEnd.DisplayName' = 'Yes'
        'Process.Stereotype' = 'No'; 'ProcessStart.Stereotype' = 'No'; 'ProcessEnd.Stereotype' = 'No'
        'Decision.Stereotype' = 'No'; 'Flow.Stereotype' = 'No'; 'OrganizationUnit.Stereotype' = 'No'
    }
    Set-DiagramFont $d 9

    # ================================================================ fase 1: objetos
    $poolO = Get-OU $m 'Organización cliente (Colegio) con la plataforma — TO-BE propuesto' 'POOL_ORGANIZACION_TOBE' 'Pool'
    $poolP = Get-OU $m 'Postulante' 'POOL_POSTULANTE' 'Pool'
    $ou = @{
        A  = Get-OU $m 'Área solicitante' 'LANE_AREA_SOLICITANTE' 'Lane'
        AP = Get-OU $m 'Aprobador / Dirección' 'LANE_APROBADOR_DIRECCION' 'Lane'
        H  = Get-OU $m 'RR. HH.' 'LANE_RRHH' 'Lane'
        P  = Get-OU $m 'Plataforma SaaS (sistema)' 'LANE_PLATAFORMA' 'Lane'
        E  = Get-OU $m 'Evaluador' 'LANE_EVALUADOR' 'Lane'
        PO = Get-OU $m ' ' 'LANE_POSTULANTE' 'Lane'
    }
    # SP-P abarca RR. HH., Plataforma y Evaluador, que quedan contiguos. El orden de los
    # carriles no tiene significado en BPMN.
    $PoolOrg = New-Pool $m $d $poolO @($ou.A, $ou.AP, $ou.H, $ou.P, $ou.E)
    $PoolPos = New-Pool $m $d $poolP @($ou.PO)
    $laneSym = @{}
    foreach ($k in 'A', 'AP', 'H', 'P', 'E') { $laneSym[$k] = $PoolOrg.Lanes[$ou[$k].Name] }
    $laneSym['PO'] = $PoolPos.Lanes[$ou.PO.Name]

    $yA = 81000; $yAp = 70500; $yH = 51000; $yHu = 58000; $yPt = 39500; $yPb = 32000; $yE = 21500; $yPo = 5500
    $TW = 8800; $TH = 5000; $EV = 1500; $GW = 5200; $GH = 3600
    $SPL = 143000; $SPR = 353000; $SPT = 64400; $SPB = 16600
    $kinds = @{
        T = @('Process', 'Task'); S = @('Start', 'Start Event'); E = @('End', 'End Event'); G = @('Decision', 'Exclusive Gateway')
        MS = @('Process', 'Message Start Event'); ME = @('Process', 'Message End Event')
    }
    # id, tipo, nombre oficial, carril, x, y, dentro de SP-P
    $nodeData = @(
        @('EI', 'S', 'Necesidad de personal identificada', 'A', 6000, $yA, 0),
        @('TB-01', 'T', 'Registrar el requerimiento de personal', 'A', 17000, $yA, 0),
        @('TB-02', 'T', 'Enviar el requerimiento a RR. HH.', 'A', 29000, $yA, 0),
        @('TB-03', 'T', 'Revisar el requerimiento y validarlo u observarlo', 'H', 41000, $yH, 0),
        @('GA1', 'G', '¿Requerimiento conforme?', 'H', 52000, $yH, 0),
        @('TB-04', 'T', 'Corregir y reenviar el requerimiento observado', 'A', 52000, $yA, 0),
        @('TB-05', 'T', 'Aprobar o rechazar el requerimiento', 'AP', 63000, $yAp, 0),
        @('GA2', 'G', '¿Requerimiento aprobado?', 'AP', 75000, $yAp, 0),
        @('TB-06', 'T', 'Notificar el rechazo al área solicitante', 'P', 75000, $yPt, 0),
        @('EFA', 'E', 'Requerimiento rechazado', 'P', 86000, $yPt, 0),
        @('TB-07', 'T', 'Crear la vacante y registrar el perfil y los criterios ponderados', 'H', 87000, $yH, 0),
        @('TB-08', 'T', 'Configurar la vacante', 'H', 99000, $yH, 0),
        @('TB-09', 'T', 'Validar la configuración, las ponderaciones y los rangos', 'P', 111000, $yPt, 0),
        @('GB1', 'G', '¿Configuración válida?', 'P', 123000, $yPt, 0),
        @('TB-10', 'T', 'Publicar la vacante en el portal de empleos', 'H', 134000, $yH, 0),
        @('TB-24', 'T', 'Calcular el ranking ponderado explicable', 'P', 362000, $yPt, 0),
        @('TB-25', 'T', 'Presentar la comparación de candidatos', 'P', 374000, $yPt, 0),
        @('TB-26', 'T', 'Registrar la decisión final humana', 'AP', 386000, $yAp, 0),
        @('TB-27', 'T', 'Registrar la selección del candidato decidido', 'H', 398000, $yH, 0),
        @('TB-28', 'T', 'Cerrar la convocatoria (con selección)', 'H', 410000, $yH, 0),
        @('TB-29', 'T', 'Notificar el resultado a cada postulante', 'P', 422000, $yPt, 0),
        @('EFE', 'E', 'Convocatoria cerrada con selección', 'P', 434000, $yPt, 0),
        @('TB-30', 'T', 'Registrar la auditoría de las acciones críticas', 'P', 363000, $yPb, 0),
        @('TB-F1', 'T', 'Cerrar la convocatoria sin selección (convocatoria desierta)', 'H', 421000, $yHu, 0),
        @('EP-01', 'MS', 'Vacante publicada', 'PO', 137000, $yPo, 0),
        @('TB-11', 'T', 'Crear la cuenta e iniciar sesión', 'PO', 149000, $yPo, 0),
        @('TB-12', 'T', 'Completar el perfil y cargar el CV', 'PO', 167000, $yPo, 0),
        @('TB-13', 'T', 'Registrar la postulación', 'PO', 180000, $yPo, 0),
        @('EP-02', 'E', 'Postulación presentada', 'PO', 204000, $yPo, 0),
        @('SIP', 'S', 'Postulación registrada', 'P', 148000, $yPt, 1),
        @('TB-14', 'T', 'Confirmar la postulación', 'P', 158000, $yPt, 1),
        @('TB-15', 'T', 'Revisar las postulaciones y el expediente', 'H', 170000, $yH, 1),
        @('TB-16', 'T', 'Preseleccionar o descartar', 'H', 182000, $yH, 1),
        @('TB-17', 'T', 'Notificar el cambio de etapa al postulante', 'P', 194000, $yPt, 1),
        @('GD1', 'G', '¿Candidato preseleccionado?', 'H', 205000, $yH, 1),
        @('EFP-01', 'E', 'Postulación descartada en la preselección', 'H', 205000, $yHu, 1),
        @('GM1', 'G', 'Unión antes de programar', 'H', 215000, $yH, 1),
        @('GD2', 'G', '¿Qué sesión se programa?', 'H', 225000, $yH, 1),
        @('TB-18', 'T', 'Programar la evaluación', 'H', 237000, $yHu, 1),
        @('TB-20', 'T', 'Programar la entrevista', 'H', 237000, $yH, 1),
        @('GM2', 'G', 'Unión de sesiones programadas', 'P', 249000, $yPt, 1),
        @('TB-19', 'T', 'Enviar la convocatoria al postulante y el aviso al evaluador', 'P', 260000, $yPt, 1),
        @('TB-21', 'T', 'Registrar puntajes, resultado y observaciones', 'E', 272000, $yE, 1),
        @('TB-22', 'T', 'Validar los puntajes dentro del rango de cada criterio', 'P', 284000, $yPt, 1),
        @('GV', 'G', '¿Puntajes válidos?', 'P', 296000, $yPt, 1),
        @('GD3', 'G', '¿Otra sesión?', 'H', 308000, $yH, 1),
        @('TB-23', 'T', 'Actualizar la etapa de la postulación (finalista o descarte)', 'H', 320000, $yH, 1),
        @('GF', 'G', '¿Finalista?', 'H', 332000, $yH, 1),
        @('EFP-02', 'ME', 'Postulación finalista', 'H', 344000, $yHu, 1),
        @('EFP-03', 'ME', 'Postulación descartada tras la evaluación', 'P', 338000, $yPt, 1)
    )

    $sp = $pk.CreateObject($BpmKind.Process)
    $sp.Name = 'SP-P Gestionar la postulación'; $sp.Code = 'F5_SP_P'
    Set-P $sp 'Composite' $true
    $sp.Stereotype = 'Sub-Process'
    $sp.SetExtendedAttribute('LoopCharacteristics', 'Multi-Instance Parallel') | Out-Null
    Set-P $sp 'OrganizationUnit' $ou.H
    $sp.Comment = 'Nivel postulacion. Instancia multiple paralela: una instancia por postulacion registrada (MT-02). El nivel vacante continua en TB-24 cuando todas las instancias terminaron.'

    $n = @{}; $pos = @{}
    foreach ($nd in $nodeData) {
        $id = $nd[0]; $k = $kinds[$nd[1]]
        $w = $TW; $h = $TH
        if ($nd[1] -in 'S', 'E', 'MS', 'ME') { $w = $EV; $h = $EV } elseif ($nd[1] -eq 'G') { $w = $GW; $h = $GH }
        $laneOU = $ou[$nd[3]]; if ($nd[3] -eq 'PO') { $laneOU = $null }
        if ($nd[6]) { $cont = $sp; $diag = $null; $lsym = $null } else { $cont = $pk; $diag = $d; $lsym = $laneSym[$nd[3]] }
        $n[$id] = New-BpmNode $cont $diag $k[0] "$id $($nd[2])" ('F5_' + ($id -replace '-', '_')) $k[1] $lsym $laneOU $nd[4] $nd[5] $w $h
        $pos[$id] = @($nd[4], $nd[5], $w, $h)
    }
    $n['TB-26'].Obj.Comment = 'Decision humana (RF-23): la registra el Aprobador / Direccion con confirmacion explicita y justificacion. El ranking no elige.'
    $n['TB-30'].Obj.Comment = 'Transversal: sin flujo de secuencia. Registro de solo insercion de las acciones criticas (RF-27).'
    $n['TB-F1'].Obj.Comment = 'Propuesta futura (A-30), no implementada. Sin flujo de entrada ni de salida.'

    # Flujos de secuencia: origen, destino, condición, ruta (ver Get-Route).
    $seqData = @(
        @('EI', 'TB-01', '', 'H'), @('TB-01', 'TB-02', '', 'H'), @('TB-02', 'TB-03', '', 'HV'), @('TB-03', 'GA1', '', 'H'),
        @('GA1', 'TB-04', 'Observado', 'V'), @('TB-04', 'TB-02', '', 'Y:85200'), @('GA1', 'TB-05', 'Validado', 'HV'),
        @('TB-05', 'GA2', '', 'H'), @('GA2', 'TB-06', 'No', 'V'), @('TB-06', 'EFA', '', 'H'), @('GA2', 'TB-07', 'Sí', 'HV'),
        @('TB-07', 'TB-08', '', 'H'), @('TB-08', 'TB-09', '', 'HV'), @('TB-09', 'GB1', '', 'H'),
        @('GB1', 'TB-08', 'No', 'Y:56000'), @('GB1', 'TB-10', 'Sí', 'HV:131000'), @('TB-10', 'SP-P', '', 'H'),
        @('SP-P', 'TB-24', '', 'H'), @('TB-24', 'TB-25', '', 'H'), @('TB-25', 'TB-26', '', 'HV'), @('TB-26', 'TB-27', '', 'HV'),
        @('TB-27', 'TB-28', '', 'H'), @('TB-28', 'TB-29', '', 'HV'), @('TB-29', 'EFE', '', 'H'),
        @('EP-01', 'TB-11', '', 'H'), @('TB-11', 'TB-12', '', 'H'), @('TB-12', 'TB-13', '', 'H'), @('TB-13', 'EP-02', '', 'H'),
        @('SIP', 'TB-14', '', 'H'), @('TB-14', 'TB-15', '', 'HV'), @('TB-15', 'TB-16', '', 'H'), @('TB-16', 'TB-17', '', 'VH'),
        @('TB-17', 'GD1', '', 'VH'), @('GD1', 'EFP-01', 'No', 'V'), @('GD1', 'GM1', 'Sí', 'H'), @('GM1', 'GD2', '', 'H'),
        @('GD2', 'TB-18', 'Evaluación', 'VH'), @('GD2', 'TB-20', 'Entrevista', 'H'), @('TB-18', 'GM2', '', 'HV'),
        @('TB-20', 'GM2', '', 'VH'), @('GM2', 'TB-19', '', 'H'), @('TB-19', 'TB-21', '', 'HV'), @('TB-21', 'TB-22', '', 'HV'),
        @('TB-22', 'GV', '', 'H'), @('GV', 'TB-21', 'No', 'Y:17800'), @('GV', 'GD3', 'Sí', 'HV'), @('GD3', 'GM1', 'Sí', 'Y:61800'),
        @('GD3', 'TB-23', 'No', 'H'), @('TB-23', 'GF', '', 'H'), @('GF', 'EFP-02', 'Sí', 'VH'), @('GF', 'EFP-03', 'No', 'VH')
    )
    $inSp = @{}; foreach ($nd in $nodeData) { $inSp[$nd[0]] = [bool]$nd[6] }
    $n['SP-P'] = @{ Obj = $sp; Sym = $null }; $inSp['SP-P'] = $false
    $flows = @{}
    foreach ($f in $seqData) {
        $cont = $pk; if ($inSp[$f[0]] -and $inSp[$f[1]]) { $cont = $sp }
        $flows[$f[0] + '>' + $f[1]] = New-BpmFlow $cont $n[$f[0]].Obj $n[$f[1]].Obj 'Sequence Flow' $f[2] $null $null
    }
    $spSym = $d.AttachObject($sp)
    Set-P $spSym 'CompositeView' $true
    $n['SP-P'].Sym = $spSym

    # Mensajes MT-01 a MT-08 (lista cerrada, unidireccional). Destino: EP-01, el borde de
    # SP-P (MT-02 crea una instancia) o el borde del pool Postulante.
    foreach ($o in @($m.GetCollectionByName('MessageFormats'))) { if ($o -and $o.Code -like 'F5_MT_*') { $o.Delete() | Out-Null } }
    $msgData = @(
        @('MT-01', 'Vacante publicada en el portal', 'TB-10', 'EP-01', 'V:137000', @(-5600, 1)),
        @('MT-02', 'Postulación', 'TB-13', 'SP-P', 'V', @(4600, 1)),
        @('MT-03', 'Confirmación y código', 'TB-14', 'POOL', 'B:11000', @(-5400, 1)),
        @('MT-04', 'Aviso de preselección o descarte', 'TB-17', 'POOL', 'B:11000', @(5600, 1)),
        @('MT-05', 'Convocatoria', 'TB-19', 'POOL', 'B:11000', @(-4600, 1)),
        @('MT-06', 'Aviso de etapa: finalista (RF-15)', 'EFP-02', 'POOL', 'B:11000', @(0, 1)),
        @('MT-07', 'Aviso de etapa: descarte (RF-15)', 'EFP-03', 'POOL', 'B:11000', @(-5800, 1)),
        @('MT-08', 'Resultado propio', 'TB-29', 'POOL', 'B:11000', @(-4600, 1))
    )
    $fmt = @{}
    function New-Msg($mt) {
        if ($mt[3] -eq 'POOL') { $dst = $poolP } else { $dst = $n[$mt[3]].Obj }
        $fl = New-BpmFlow $pk $n[$mt[2]].Obj $dst 'Message Flow' '' $null $fmt[$mt[0]]
        $fl.Code = 'F5_' + ($mt[0] -replace '-', '_') + '_FLOW'
        $flows[$mt[0]] = $fl
    }
    foreach ($mt in $msgData) {
        $fo = $m.CreateObject($BpmKind.MessageFormat)
        $fo.Name = $mt[0] + ' ' + $mt[1]; $fo.Code = 'F5_' + ($mt[0] -replace '-', '_')
        $fmt[$mt[0]] = $fo
        New-Msg $mt
    }

    # ================================================================ fase 2: geometría
    $R = 452000
    function Layout {
        Set-PoolGeometry $PoolPos 0 $R -400000 @(11000)
        Set-PoolGeometry $PoolOrg 0 $R 16000 @(11000, 11000, 20000, 18000, 11000)
        Set-PoolGeometry $PoolPos 0 $R 0 @(11000)
        foreach ($id in $pos.Keys) {
            if (-not $inSp[$id] -and $n[$id].Sym) { $q = $pos[$id]; Set-Box $n[$id].Sym $q[0] $q[1] $q[2] $q[3] }
        }
        $par = Get-P $spSym 'Parent'
        if ((Get-P $par 'ClassName') -ne 'Business Process Diagram') {
            (Get-C $par 'SubSymbols').Remove($spSym) | Out-Null
            (Get-C $d 'Symbols').Add($spSym) | Out-Null
        }
        Set-Rect $spSym $SPL $SPT $SPR $SPB
        foreach ($id in $pos.Keys) {
            if (-not $inSp[$id]) { continue }
            $s = Find-SymbolDeep (Get-C $spSym 'SubSymbols') $n[$id].Obj
            if (-not $s) { throw "Sin símbolo para $id dentro de SP-P" }
            $n[$id].Sym = $s
            $q = $pos[$id]; Set-Box $s $q[0] $q[1] $q[2] $q[3]
        }
    }
    Layout
    Layout

    # ================================================================ fase 3: rutas
    foreach ($f in $seqData) {
        $key = $f[0] + '>' + $f[1]
        $ls = Get-FlowSymbol $d $flows[$key] $n[$f[0]].Sym $n[$f[1]].Sym
        $pts = Get-Route (Get-Rect $n[$f[0]].Sym) (Get-Rect $n[$f[1]].Sym) $f[3]
        $srcOff = $null
        if ($f[2]) {
            $dx = $pts[1][0] - $pts[0][0]; $dy = $pts[1][1] - $pts[0][1]
            if ([Math]::Abs($dx) -gt [Math]::Abs($dy)) { $srcOff = @([int]([Math]::Sign($dx) * 200), 700) }
            else { $srcOff = @(900, [int]([Math]::Sign($dy) * 200)) }
        }
        Set-LinkPoints $ls $pts @(0, 1) $srcOff
    }
    $poolRect = [pscustomobject]@{ L = 0; T = 11000; R = $R; B = 0 }
    function Show-Msg($mt) {
        $src = $n[$mt[2]]
        if ($mt[3] -eq 'POOL') { $dstSym = $PoolPos.Sym; $tr = $poolRect } else { $dstSym = $n[$mt[3]].Sym; $tr = Get-Rect $dstSym }
        $ls = $d.AttachLinkObject($flows[$mt[0]], $src.Sym, $dstSym)
        Set-LinkPoints $ls (Get-Route (Get-Rect $src.Sym) $tr $mt[4]) $mt[5]
        Move-ToFront $d $ls
    }
    foreach ($mt in $msgData) { Show-Msg $mt }

    # ================================================================ presentación
    # SP-P se dibuja con relleno blanco: las divisiones de carril se prolongan dentro de él.
    foreach ($y in 45000, 27000) {
        $div = Add-Frame $d ($SPL + 300) ($y + 40) ($SPR - 300) ($y - 40) 2
        Set-P $div 'LineColor' 12615680
        Move-ToFront $d $div
    }
    function Lbl($id, $dx, $dy, $w = 9000, $h = 2600) {
        $c = Get-Center $n[$id].Sym
        $t = $n[$id].Obj.Name -replace '^(\S+) ', "`$1`r`n"
        Add-Label $d $t ($c[0] + $dx) ($c[1] + $dy) $w $h | Out-Null
    }
    Lbl 'EI' 0 -2500; Lbl 'EFA' 0 -2500; Lbl 'EFE' 0 -2500 8000; Lbl 'EP-01' -5200 -2300; Lbl 'EP-02' 0 -2500
    Lbl 'SIP' 0 -2500 8000; Lbl 'EFP-01' 5600 0; Lbl 'EFP-02' 0 2600; Lbl 'EFP-03' -5800 -1800
    Lbl 'GA1' 0 -3600; Lbl 'GA2' 0 3500; Lbl 'GB1' 0 -3600
    Lbl 'GD1' -300 -3800 8600 3000; Lbl 'GM1' 300 -3800 8600 3000; Lbl 'GD2' 5000 -3800 8000 3000
    Lbl 'GM2' 0 -3800 9000 3000; Lbl 'GV' 0 3400; Lbl 'GD3' -5200 -3600 8600 3000; Lbl 'GF' 6500 2800 7000

    # Grupos: TB-30 transversal y TB-F1 propuesta futura (marcos discontinuos).
    Add-DashedBox $d 356000 36300 399000 27700
    Add-DashedBox $d 414000 61900 449000 54100
    Add-Text $d "F5 BPMN TO-BE propuesto — Reclutamiento y selección`r`nCaso de estudio: Colegio Andino de Huancayo. Modelo de negocio propuesto con la plataforma SaaS, no del software. Dos niveles: vacante (pool de la organización) y postulación (SP-P). Formalización F29 en PowerDesigner." 0 95000 200000 89500 | Out-Null
    foreach ($nt in @(
            @('Nivel vacante (una instancia por requerimiento o vacante): A = TB-01 a TB-06; B = TB-07 a TB-10; SP-P; E = TB-24 a TB-29; TB-30 transversal.', 64000, 85500, 140000, 77500),
            @('Nivel postulación: SP-P «Gestionar la postulación», subproceso expandido de instancia múltiple paralela (marcador |||), una instancia por postulación registrada (MT-02). El nivel vacante continúa en TB-24 cuando todas las instancias terminaron. El flujo principal supone al menos una postulación finalista: el caso sin finalistas no tiene camino implementado (A-30).', 4000, 26000, 128000, 17200),
            @('Decisión humana (RF-23): el ranking no elige.', 352000, 73800, 379000, 67200),
            @('TB-24 y TB-25 calculan, ordenan y comparan; no seleccionan ni cambian estados.', 357000, 61400, 383000, 55000),
            @('Transversal, sin flujo de secuencia: registra en auditoría (solo inserción) las acciones críticas; la consulta el Aprobador / Dirección (RF-27).', 369500, 35800, 398500, 28200),
            @('Propuesta futura (A-30), no implementada: sin flujo de entrada ni de salida.', 427000, 61400, 448500, 54600))) {
        Move-ToFront $d (Add-Note $d $nt[0] $nt[1] $nt[2] $nt[3] $nt[4])
    }

    # ================================================================ verificación
    $g = Get-BpmGraph $pk
    function Id($code) { if ($code -like 'F5_*') { ($code.Substring(3) -replace '_', '-') -replace '^SP-P$', 'SP-P' } else { $code } }
    $fail = @(); $out = @()
    $out += "F29 - verificación de la vista F5 - BPMN TO-BE ($(Get-Date -Format 'yyyy-MM-dd HH:mm'))"
    $out += "Modelo: docs/academico/powerdesigner/models/F29_BPM_Academico.bpm; paquete F5; diagrama «$($d.Name)»"
    $out += ''
    foreach ($nd in $nodeData) {
        $x = $g.Nodes['F5_' + ($nd[0] -replace '-', '_')]
        if (-not $x) { $fail += "falta $($nd[0])" } elseif ($x.Name -ne "$($nd[0]) $($nd[2])") { $fail += "nombre de $($nd[0])" }
    }
    $tb = @($g.Nodes.Values | Where-Object { $_.Name -like 'TB-*' })
    $gws = @($g.Nodes.Values | Where-Object { $_.Kind -eq 'ProcessDecisions' })
    $evs = @($g.Nodes.Values | Where-Object { $_.Kind -in 'ProcessStarts', 'ProcessEnds' -or $_.Stereo -in 'Message Start Event', 'Message End Event' })
    $mi = $sp.GetExtendedAttribute('LoopCharacteristics')
    $out += "Tareas TB: $($tb.Count) (esperadas 31: TB-01 a TB-30 y TB-F1) · SP-P: $mi · compuertas: $($gws.Count) (10) · eventos: $($evs.Count) (9)"
    if ($tb.Count -ne 31) { $fail += 'tareas' }; if ($gws.Count -ne 10) { $fail += 'compuertas' }; if ($evs.Count -ne 9) { $fail += 'eventos' }
    if ($mi -ne 'Multi-Instance Parallel') { $fail += 'SP-P instancia múltiple paralela' }
    $expSeq = @($seqData | ForEach-Object { $_[0] + '>' + $_[1] + $(if ($_[2]) { "[$($_[2])]" }) })
    $seq = @($g.Flows | Where-Object { $_.Stereo -eq 'Sequence Flow' } | ForEach-Object { (Id $_.Src) + '>' + (Id $_.Dst) + $(if ($_.Cond) { "[$($_.Cond)]" }) })
    $expMsg = @($msgData | ForEach-Object { $_[0] + ':' + $_[2] + '>' + $(if ($_[3] -eq 'POOL') { 'POOL_POSTULANTE' } else { $_[3] }) })
    $msg = @($g.Flows | Where-Object { $_.Stereo -eq 'Message Flow' } | ForEach-Object { ($_.Format -split ' ')[0] + ':' + (Id $_.Src) + '>' + (Id $_.Dst) })
    $d1 = Compare-Object ($expSeq | Sort-Object) ($seq | Sort-Object); $d2 = Compare-Object ($expMsg | Sort-Object) ($msg | Sort-Object)
    $out += "Flujos de secuencia: $($seq.Count) (esperados $($expSeq.Count)) · flujos de mensaje: $($msg.Count) (8, unidireccionales)"
    if ($d1) { $fail += 'secuencia: ' + (($d1 | ForEach-Object { $_.SideIndicator + $_.InputObject }) -join ' ') }
    if ($d2) { $fail += 'mensajes: ' + (($d2 | ForEach-Object { $_.SideIndicator + $_.InputObject }) -join ' ') }
    # Reglas de la especificación.
    $rules = [ordered]@{
        'TB-15 tiene una sola entrada (desde TB-14)'            = (@($seq | Where-Object { $_ -like '*>TB-15' }).Count -eq 1 -and $seq -contains 'TB-14>TB-15')
        'GM1 une GD1 [Sí] y GD3 [Sí]'                            = ($seq -contains 'GD1>GM1[Sí]' -and $seq -contains 'GD3>GM1[Sí]')
        'GM2 une TB-18 y TB-20'                                  = ($seq -contains 'TB-18>GM2' -and $seq -contains 'TB-20>GM2')
        'GV [No] vuelve a TB-21 (rechazo de TB-22)'              = ($seq -contains 'GV>TB-21[No]')
        'GF «¿Finalista?»: Sí -> EFP-02, No -> EFP-03'           = ($seq -contains 'GF>EFP-02[Sí]' -and $seq -contains 'GF>EFP-03[No]')
        'TB-F1 sin flujo de entrada ni de salida'                = (@($g.Flows | Where-Object { $_.Src -eq 'F5_TB_F1' -or $_.Dst -eq 'F5_TB_F1' }).Count -eq 0)
        'TB-F1 no está conectado desde TB-25'                    = (-not ($seq -like 'TB-25>TB-F1*'))
        'TB-30 transversal, sin flujo de secuencia'              = (@($g.Flows | Where-Object { $_.Src -eq 'F5_TB_30' -or $_.Dst -eq 'F5_TB_30' }).Count -eq 0)
        'TB-26 en el carril Aprobador / Dirección'               = ((Get-P $n['TB-26'].Obj 'OrganizationUnit').Name -eq 'Aprobador / Dirección')
        'MT-01 sale de TB-10 hacia EP-01 «Vacante publicada»'    = ($msg -contains 'MT-01:TB-10>EP-01')
        'Sin RF-29 ni riesgo operacional en el TO-BE'            = (-not (@($g.Nodes.Values | Where-Object { $_.Name -match 'RF-29|riesgo' }).Count))
    }
    foreach ($k in $rules.Keys) { $out += "  [$(if ($rules[$k]) { 'OK' } else { 'FALLA' })] $k"; if (-not $rules[$k]) { $fail += $k } }
    foreach ($nd in $g.Nodes.Values) {
        $id = Id $nd.Code
        if ($id -in 'TB-30', 'TB-F1') { continue }
        $in = @($seq | Where-Object { ($_ -replace '\[.*\]', '') -like "*>$id" }).Count
        $outc = @($seq | Where-Object { $_ -like "$id>*" }).Count
        $isStart = $nd.Kind -eq 'ProcessStarts' -or $nd.Stereo -eq 'Message Start Event'
        $isEnd = $nd.Kind -eq 'ProcessEnds' -or $nd.Stereo -eq 'Message End Event'
        if (-not $isStart -and $in -lt 1) { $fail += "$id sin entrada" }
        if (-not $isEnd -and $outc -lt 1) { $fail += "$id sin salida" }
    }
    $out += 'Conectividad: toda actividad, compuerta y evento (salvo TB-30 y TB-F1, fuera de la secuencia por especificación) tiene entrada y salida.'
    $laneOf = @{}
    foreach ($id in $n.Keys) { try { $x = Get-P $n[$id].Obj 'OrganizationUnit'; if ($x) { $laneOf[$id] = $x.Name } } catch {} }
    $out += 'Responsable (carril) por nodo: ' + (($laneOf.Keys | Sort-Object | ForEach-Object { "$_=$($laneOf[$_])" }) -join '; ')
    $ck = Test-F29BpmCheck $m
    $out += $ck.Lines
    if (-not $ck.Ok) { $fail += 'Check Model: hallazgos no explicados por la especificación' }
    $out += ''
    if ($fail.Count) { $out += 'RESULTADO: FALLA'; $out += $fail } else { $out += 'RESULTADO: PASS' }
    Write-F29Report (Join-Path $F29Root 'validation\F5_model_check.txt') $out
    $out | ForEach-Object { Write-Host "  $_" }

    Save-F29Model $m
    Export-F29 $d 'F5_BPMN_TOBE'
} finally { Close-F29 }
