# ST-01..ST-04. Fuente: docs/v1.1/uml/state-diagrams.md y puml/st-0*.puml.
# Trabaja sobre el OOM existente: cada diagrama se crea o, si ya existe, se reemplaza.
# $env:PD_ONLY (p. ej. "ST-03") limita qué diagramas se generan en una corrida.
#
# Cada diagrama vive en su propio paquete (ST-01..ST-04): PowerDesigner exige nombres
# únicos por espacio de nombres y `borrador` es un estado real tanto del requerimiento
# como de la vacante. Así cada estado conserva su valor real, sin sufijos.
# Transiciones: evento [guarda] / efecto (TriggerEvent, ConditionAlias, TriggerAction).
# El paréntesis de actor y RF del borrador va con el evento.
. "$PSScriptRoot\pdlib.ps1"
. "$PSScriptRoot\flowlib.ps1"

$sts = [ordered]@{}
$SW = 9000                                  # ancho de un estado
$SH = 3000                                  # alto de un estado

$sts['ST-01'] = @{
    Name = 'ST-01 Estados del requerimiento (JobRequestStatus)'; File = 'ST-01-estados-requerimiento'
    Nodes = @(
        @{ Id = 'i0'; Kind = 'Start'; Name = 'Inicio ST-01'; X = 0; Y = 0 },
        @{ Id = 'borrador'; Kind = 'State'; Name = 'borrador'; X = 0; Y = -9000; W = $SW; H = $SH },
        @{ Id = 'enviado'; Kind = 'State'; Name = 'enviado'; X = 0; Y = -19000; W = $SW; H = $SH },
        @{ Id = 'observado'; Kind = 'State'; Name = 'observado'; X = 30000; Y = -19000; W = $SW; H = $SH },
        @{ Id = 'validado'; Kind = 'State'; Name = 'validado'; X = 0; Y = -29000; W = $SW; H = $SH },
        @{ Id = 'aprobado'; Kind = 'State'; Name = 'aprobado'; X = 0; Y = -40000; W = $SW; H = $SH },
        @{ Id = 'rechazado'; Kind = 'State'; Name = 'rechazado'; X = 30000; Y = -29000; W = $SW; H = $SH },
        @{ Id = 'f0'; Kind = 'End'; Name = 'Fin ST-01'; X = 0; Y = -49000 })
    Links = @(
        @('i0', 'borrador', @('register (Área solicitante, RF-01)'), 'V'),
        @('borrador', 'enviado', @('submit (dueño)'), 'V'),
        @('enviado', 'observado', @('observe (RR. HH., RF-02)', 'comentario'), @(, @(15000, -17900)), @(7000, 1000)),
        @('observado', 'enviado', @('submit tras correct (dueño, RF-02)'), @(, @(15000, -20100)), @(0, -1000)),
        @('enviado', 'validado', @('validate (RR. HH., RF-02)'), 'V'),
        @('validado', 'aprobado', @('approve (Aprobador, RF-03)'), 'V'),
        @('validado', 'rechazado', @('reject', 'motivo', 'notificar al solicitante (RF-03, RF-04)'), 'H'),
        @('aprobado', 'f0', $null, 'V'), @('rechazado', 'f0', $null, 'VH'))
    Notes = @(
        @('editable en borrador y observado (isEditable)', 20000, -9000, 16000),
        @('habilita crear UNA vacante', -16000, -40000, 12000))
}

$sts['ST-02'] = @{
    Name = 'ST-02 Estados de la vacante (VacancyStatus)'; File = 'ST-02-estados-vacante'
    Nodes = @(
        @{ Id = 'i0'; Kind = 'Start'; Name = 'Inicio ST-02'; X = 0; Y = 0 },
        @{ Id = 'borrador'; Kind = 'State'; Name = 'borrador'; X = 22000; Y = 0; W = $SW; H = $SH },
        @{ Id = 'publicada'; Kind = 'State'; Name = 'publicada'; X = 52000; Y = 0; W = $SW; H = $SH },
        @{ Id = 'cerrada'; Kind = 'State'; Name = 'cerrada'; X = 82000; Y = 0; W = $SW; H = $SH },
        @{ Id = 'f0'; Kind = 'End'; Name = 'Fin ST-02'; X = 98000; Y = 0 })
    Links = @(
        @('i0', 'borrador', @('create (RR. HH., RF-05, RF-06)', 'requerimiento aprobado y sin vacante'), 'H'),
        @('borrador', 'publicada', @('publish (RR. HH., RF-07)', 'VacancyValidator sin observaciones'), 'H'),
        @('publicada', 'cerrada', @('close', 'decisión RF-23 y selección RF-24', 'closure_type = con_seleccion (RR. HH., RF-25)'), 'H'),
        @('cerrada', 'f0', $null, 'H'))
    Notes = @(, @("'desierta' existe en VacancyClosureType pero no tiene flujo implementado (A-30).", 82000, -8000, 17000))
}

# ST-03: eje principal vertical; `descartado` y `no_seleccionado`, a los lados, reciben
# una transición horizontal desde cada estado activo. Las transiciones que saltan un
# estado van por carriles laterales (x = ±12000); su rótulo se desplaza junto al carril.
$yP = -8000; $yS = -17000; $yEV = -26000; $yEN = -35000; $yF = -44000; $ySE = -53000; $yEnd = -62000
$sts['ST-03'] = @{
    Name = 'ST-03 Estados de la postulación (ApplicationStatus)'; File = 'ST-03-estados-postulacion'
    AlignTarget = $true
    Nodes = @(
        @{ Id = 'i0'; Kind = 'Start'; Name = 'Inicio ST-03'; X = 0; Y = 0 },
        @{ Id = 'postulado'; Kind = 'State'; Name = 'postulado'; X = 0; Y = $yP; W = $SW; H = $SH },
        @{ Id = 'preseleccionado'; Kind = 'State'; Name = 'preseleccionado'; X = 0; Y = $yS; W = $SW; H = $SH },
        @{ Id = 'en_evaluacion'; Kind = 'State'; Name = 'en_evaluacion'; X = 0; Y = $yEV; W = $SW; H = $SH },
        @{ Id = 'en_entrevista'; Kind = 'State'; Name = 'en_entrevista'; X = 0; Y = $yEN; W = $SW; H = $SH },
        @{ Id = 'finalista'; Kind = 'State'; Name = 'finalista'; X = 0; Y = $yF; W = $SW; H = $SH },
        @{ Id = 'seleccionado'; Kind = 'State'; Name = 'seleccionado'; X = 0; Y = $ySE; W = $SW; H = $SH },
        @{ Id = 'descartado'; Kind = 'State'; Name = 'descartado'; X = -44000; Y = -26000; W = 10000; H = 42000 },
        @{ Id = 'no_seleccionado'; Kind = 'State'; Name = 'no_seleccionado'; X = 44000; Y = -26000; W = 10000; H = 42000 },
        @{ Id = 'f0'; Kind = 'End'; Name = 'Fin ST-03'; X = 0; Y = $yEnd })
    Links = @(
        @('i0', 'postulado', @('apply (Postulante, RF-10)'), 'V'),
        @('postulado', 'preseleccionado', @('shortlist (RR. HH., RF-13)'), 'V'),
        @('preseleccionado', 'en_evaluacion', @('moveTo | automático al programar evaluación (RF-14, RF-16)'), 'V'),
        @('preseleccionado', 'en_entrevista', @('moveTo | automático al programar entrevista (RF-14, RF-18)'), @(@(12000, ($yS - 900)), @(12000, ($yEN - 900))), @(8200, -4100)),
        @('en_evaluacion', 'en_entrevista', @('moveTo | automático al programar entrevista'), 'V'),
        @('en_evaluacion', 'finalista', @('moveTo (RF-14)'), @(@(-12000, ($yEV - 900)), @(-12000, ($yF - 900))), @(-8900, -13100)),
        @('en_entrevista', 'finalista', @('moveTo (RF-14)'), 'V'),
        @('finalista', 'seleccionado', @('register (RR. HH., RF-24)', 'decisión final registrada'), 'V'),
        @('postulado', 'descartado', @('discard (RF-13)', 'comentario'), 'H'),
        @('preseleccionado', 'descartado', @('discard'), 'H'),
        @('en_evaluacion', 'descartado', @('discard'), 'H'),
        @('en_entrevista', 'descartado', @('discard'), 'H'),
        @('finalista', 'descartado', @('discard'), 'H'),
        @('postulado', 'no_seleccionado', @('close (RF-25)'), 'H'),
        @('preseleccionado', 'no_seleccionado', @('close'), 'H'),
        @('en_evaluacion', 'no_seleccionado', @('close'), 'H'),
        @('en_entrevista', 'no_seleccionado', @('close'), 'H'),
        @('finalista', 'no_seleccionado', @('close', 'no es la elegida'), 'H'),
        @('seleccionado', 'f0', $null, 'V'),
        @('no_seleccionado', 'f0', $null, @(, @(44000, $yEnd))),
        @('descartado', 'f0', $null, @(, @(-44000, $yEnd))))
    Notes = @(
        @("Solo por RF-24; como mucho una por vacante (índice parcial).`nLa decisión RF-23 no es una transición: la elegida sigue en finalista hasta RF-24.", 24000, $ySE, 24000),
        @("Tras la decisión final no hay cambios manuales (A-28).`nCon la vacante cerrada, ningún cambio.`nCambios manuales notifican (RF-15); automáticos y RF-24 no; el cierre notifica por RF-26.", -64000, -26000, 22000))
}

$sts['ST-04'] = @{
    Name = 'ST-04 Estados de evaluación y entrevista (AssessmentStatus)'; File = 'ST-04-estados-sesion'
    Nodes = @(
        @{ Id = 'i0'; Kind = 'Start'; Name = 'Inicio ST-04'; X = 0; Y = 0 },
        @{ Id = 'programada'; Kind = 'State'; Name = 'programada'; X = 0; Y = -10000; W = $SW; H = $SH },
        @{ Id = 'realizada'; Kind = 'State'; Name = 'realizada'; X = 0; Y = -21000; W = $SW; H = $SH },
        @{ Id = 'f0'; Kind = 'End'; Name = 'Fin ST-04'; X = 0; Y = -30000 })
    Links = @(
        @('i0', 'programada', @('scheduleEvaluation | scheduleInterview (RR. HH., RF-16, RF-18)'), 'V'),
        @('programada', 'realizada', @('recordEvaluation | recordInterview (Evaluador asignado, RF-19)'), 'V'),
        @('realizada', 'f0', $null, 'V'))
    Notes = @(, @('sin cancelación ni reprogramación implementadas', -20000, -21000, 15000))
}

$only = @()
if ($env:PD_ONLY) { $only = $env:PD_ONLY -split ',' | ForEach-Object { $_.Trim() } }

Open-Pd
try {
    $m = $Pd.OpenModel($OomFile)
    foreach ($key in $sts.Keys) {
        if ($only.Count -and ($only -notcontains $key)) { continue }
        $sp = $sts[$key]
        $sp.LinkKind = 'Transition'
        $pkg = @($m.Packages) | Where-Object { $_.Name -eq $key } | Select-Object -First 1
        if (-not $pkg) { $pkg = $m.Packages.CreateNew(); $pkg.Name = $key; $pkg.Code = $key.Replace('-', '_') }
        $d = New-FlowDiagram $pkg $pkg.StatechartDiagrams $sp.Name ($key.Replace('-', '_')) $sp
        Export-Diagram $d $sp.File
        "$key : estados=$(@($sp.Nodes | Where-Object { $_.Kind -eq 'State' }).Count) transiciones=$($sp.Links.Count)"
    }
    Save-Model $m $OomFile
    $n = 0; foreach ($pk in @($m.Packages)) { if ($pk.Name -like 'ST-0*') { $n += @($pk.StatechartDiagrams).Count } }
    "diagramas de estados=$n"
    $m.Close()
} catch {
    "ERROR linea $($_.InvocationInfo.ScriptLineNumber): $($_.Exception.Message)"
    "  $($_.InvocationInfo.Line.Trim())"
    if ($m) { try { $m.Close() } catch {} }
} finally { Close-Pd }
