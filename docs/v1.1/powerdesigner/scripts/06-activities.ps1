# AC-01 y AC-02. Fuente: docs/v1.1/uml/activity-diagrams.md y puml/ac-0*.puml.
# Trabaja sobre el OOM existente: cada diagrama se crea o, si ya existe, se reemplaza.
# $env:PD_ONLY (p. ej. "AC-01") limita qué diagramas se generan en una corrida.
. "$PSScriptRoot\pdlib.ps1"
. "$PSScriptRoot\flowlib.ps1"

$acts = [ordered]@{}

# ---------------------------------------------------------------------------
# PowerDesigner exige nombres únicos: las actividades que el borrador repite
# («Notificar cambio de etapa», «Descartar con comentario») llevan el estado de
# destino real o el RF del paso para distinguirse.
#
# AC-01: seis carriles en el orden de aparición del borrador PlantUML (marcos
# gráficos; el carril de cada nodo es su OrganizationUnit). RR. HH.,
# Aprobador y Sistema tienen dos columnas: la principal y la de las ramas que
# terminan (rechazo del requerimiento y descartes).
$P = 5600                                   # paso entre filas
function Y([double]$r) { [int](-$r * $script:P) }
$xA = 9000
$xRH1 = 27000; $xRH2 = 42000; $xLoop = 19000
$xAP1 = 59000; $xAP2 = 73000
$xS1 = 89000; $xS2 = 104000
$xP = 121000; $xE = 139000
$W = 13000

$acts['AC-01'] = @{
    Name = 'AC-01 Proceso de reclutamiento AS-IS (RF-01 a RF-27)'; File = 'AC-01-proceso-reclutamiento'
    Top = 6500; Bottom = (Y 28) - 4500
    Lanes = @(@('Área solicitante', 0, 18000), @('Recursos Humanos', 18000, 50000), @('Aprobador / Dirección', 50000, 80000),
        @('Sistema', 80000, 112000), @('Postulante', 112000, 130000), @('Evaluador', 130000, 148000))
    Nodes = @(
        @{ Id = 'i0'; Kind = 'Start'; Name = 'Inicio del requerimiento'; X = $xA; Y = (Y 0); Lane = 'Área solicitante' },
        @{ Id = 'a1'; Kind = 'Activity'; Name = 'Registrar o corregir requerimiento (RF-01)'; X = $xA; Y = (Y 1); W = $W; Lane = 'Área solicitante' },
        @{ Id = 'a2'; Kind = 'Activity'; Name = 'Enviar a RR. HH.'; X = $xA; Y = (Y 2); W = $W; Lane = 'Área solicitante' },
        @{ Id = 'd1'; Kind = 'Decision'; Name = '¿Requerimiento correcto? (RF-02)'; X = $xRH1; Y = (Y 3); W = 12500; H = 4400; Lane = 'Recursos Humanos' },
        @{ Id = 'a3'; Kind = 'Activity'; Name = 'Validar requerimiento'; X = $xRH1; Y = (Y 4); W = $W; Lane = 'Recursos Humanos' },
        @{ Id = 'd2'; Kind = 'Decision'; Name = '¿Aprobar? (RF-03)'; X = $xAP1; Y = (Y 5); W = 11000; H = 4000; Lane = 'Aprobador / Dirección' },
        @{ Id = 'a4'; Kind = 'Activity'; Name = 'Rechazar con motivo'; X = $xAP2; Y = (Y 5); W = $W; Lane = 'Aprobador / Dirección' },
        @{ Id = 'a5'; Kind = 'Activity'; Name = 'Notificar rechazo al solicitante (RF-04)'; X = $xS1; Y = (Y 5); W = $W; Lane = 'Sistema' },
        @{ Id = 'f1'; Kind = 'End'; Final = 'activity'; Name = 'Fin: requerimiento rechazado'; X = $xS1; Y = (Y 6); Lane = 'Sistema' },
        @{ Id = 'a6'; Kind = 'Activity'; Name = 'Crear vacante: datos, perfil, criterios, plazo objetivo opcional (RF-05, RF-06)'; X = $xRH1; Y = (Y 7); W = $W; Lane = 'Recursos Humanos' },
        @{ Id = 'd3'; Kind = 'Decision'; Name = '¿Configuración, rangos y ponderaciones válidos? (RF-20)'; X = $xS1; Y = (Y 8); W = 17000; H = 6400; Lane = 'Sistema' },
        @{ Id = 'a7'; Kind = 'Activity'; Name = 'Publicar vacante (RF-07)'; X = $xRH1; Y = (Y 9); W = $W; Lane = 'Recursos Humanos' },
        @{ Id = 'p1'; Kind = 'Activity'; Name = 'Crear cuenta, completar perfil y CV (RF-08, RF-09)'; X = $xP; Y = (Y 10); W = $W; Lane = 'Postulante' },
        @{ Id = 'p2'; Kind = 'Activity'; Name = 'Postular (RF-10)'; X = $xP; Y = (Y 11); W = $W; Lane = 'Postulante' },
        @{ Id = 's1'; Kind = 'Activity'; Name = 'Confirmar postulación (RF-11)'; X = $xS1; Y = (Y 12); W = $W; Lane = 'Sistema' },
        @{ Id = 'h1'; Kind = 'Activity'; Name = 'Revisar la postulación (RF-12)'; X = $xRH1; Y = (Y 13); W = $W; Lane = 'Recursos Humanos' },
        @{ Id = 'd4'; Kind = 'Decision'; Name = '¿Preseleccionar? (RF-13)'; X = $xRH1; Y = (Y 14); W = 12000; H = 4200; Lane = 'Recursos Humanos' },
        @{ Id = 'h2'; Kind = 'Activity'; Name = 'Descartar con comentario (RF-13)'; X = $xRH2; Y = (Y 14); W = $W; Lane = 'Recursos Humanos' },
        @{ Id = 's2'; Kind = 'Activity'; Name = 'Notificar cambio de etapa: descartado (RF-15)'; X = $xS2; Y = (Y 14); W = $W; Lane = 'Sistema' },
        @{ Id = 'x1'; Kind = 'End'; Final = 'flow'; Name = 'fin de esta postulación (descarte en preselección)'; X = $xS2; Y = (Y 15); Lane = 'Sistema' },
        @{ Id = 's3'; Kind = 'Activity'; Name = 'Notificar cambio de etapa: preseleccionado (RF-15)'; X = $xS1; Y = (Y 15); W = $W; Lane = 'Sistema' },
        @{ Id = 'h3'; Kind = 'Activity'; Name = 'Programar evaluación o entrevista (RF-16, RF-18)'; X = $xRH1; Y = (Y 16); W = $W; Lane = 'Recursos Humanos' },
        @{ Id = 's4'; Kind = 'Activity'; Name = 'Convocatoria al postulante y aviso al evaluador (RF-17)'; X = $xS1; Y = (Y 17); W = $W; Lane = 'Sistema' },
        @{ Id = 'e1'; Kind = 'Activity'; Name = 'Registrar puntajes y resultado (RF-19, RF-20)'; X = $xE; Y = (Y 18); W = $W; Lane = 'Evaluador' },
        @{ Id = 'd5'; Kind = 'Decision'; Name = '¿Más sesiones?'; X = $xRH1; Y = (Y 19); W = 11000; H = 4000; Lane = 'Recursos Humanos' },
        @{ Id = 'd6'; Kind = 'Decision'; Name = '¿Postulación descartada? (RF-14)'; X = $xRH1; Y = (Y 20); W = 12500; H = 4400; Lane = 'Recursos Humanos' },
        @{ Id = 'h4'; Kind = 'Activity'; Name = 'Descartar con comentario (RF-14)'; X = $xRH2; Y = (Y 20); W = $W; Lane = 'Recursos Humanos' },
        @{ Id = 's5'; Kind = 'Activity'; Name = 'Notificar cambio de etapa: descartado tras las sesiones (RF-15)'; X = $xS2; Y = (Y 20); W = 14500; Lane = 'Sistema' },
        @{ Id = 'x2'; Kind = 'End'; Final = 'flow'; Name = 'fin de esta postulación (descarte tras las sesiones)'; X = $xS2; Y = (Y 21); Lane = 'Sistema' },
        @{ Id = 'h5'; Kind = 'Activity'; Name = 'Pasar a finalista (RF-14)'; X = $xRH1; Y = (Y 21); W = $W; Lane = 'Recursos Humanos' },
        @{ Id = 's6'; Kind = 'Activity'; Name = 'Notificar cambio de etapa: finalista (RF-15)'; X = $xS1; Y = (Y 22); W = $W; Lane = 'Sistema' },
        @{ Id = 'h6'; Kind = 'Activity'; Name = 'Consultar comparación; el sistema calcula el ranking solo con postulaciones NO descartadas (RF-21, RF-22)'; X = ($xRH1 + 1500); Y = (Y 23); W = 16000; Lane = 'Recursos Humanos' },
        @{ Id = 'ap'; Kind = 'Activity'; Stereo = 'human decision'; Name = 'Elegir una postulación finalista, justificar y confirmar (RF-23)'; X = $xAP1; Y = (Y 24); W = 15000; Lane = 'Aprobador / Dirección' },
        @{ Id = 'h7'; Kind = 'Activity'; Name = 'Registrar selección (RF-24)'; X = $xRH1; Y = (Y 25); W = $W; Lane = 'Recursos Humanos' },
        @{ Id = 'h8'; Kind = 'Activity'; Name = 'Cerrar convocatoria con selección (RF-25)'; X = $xRH1; Y = (Y 26); W = $W; Lane = 'Recursos Humanos' },
        @{ Id = 's7'; Kind = 'Activity'; Name = 'Notificar resultado a seleccionada y no seleccionadas (RF-26)'; X = $xS1; Y = (Y 27); W = $W; Lane = 'Sistema' },
        @{ Id = 'f2'; Kind = 'End'; Final = 'activity'; Name = 'Fin: convocatoria cerrada'; X = $xS1; Y = (Y 28); Lane = 'Sistema' })
    Links = @(
        @('i0', 'a1', $null, 'V'), @('a1', 'a2', $null, 'V'), @('a2', 'd1', $null, 'VH'),
        @('d1', 'a1', 'no: observar con comentario', @(, @($xRH1, (Y 1)))),
        @('d1', 'a3', 'sí', 'V'), @('a3', 'd2', $null, 'VH'),
        @('d2', 'a4', 'no', 'H'), @('a4', 'a5', $null, 'H'), @('a5', 'f1', $null, 'V'),
        @('d2', 'a6', 'sí', @(@($xAP1, (Y 6.5)), @($xRH1, (Y 6.5)))),
        @('a6', 'd3', $null, 'VH'),
        @('d3', 'a6', 'no', @(, @($xS1, (Y 7)))),
        @('d3', 'a7', 'sí', 'VH'), @('a7', 'p1', $null, 'VH'), @('p1', 'p2', $null, 'V'), @('p2', 's1', $null, 'VH'),
        @('s1', 'h1', $null, 'VH'), @('h1', 'd4', $null, 'V'),
        @('d4', 'h2', 'no', 'H'), @('h2', 's2', $null, 'H'), @('s2', 'x1', $null, 'V'),
        @('d4', 's3', 'sí', 'VH'), @('s3', 'h3', $null, 'VH'), @('h3', 's4', $null, 'VH'), @('s4', 'e1', $null, 'VH'),
        @('e1', 'd5', $null, 'VH'),
        @('d5', 'h3', 'sí', @(@($xLoop, (Y 19)), @($xLoop, (Y 16)))),
        @('d5', 'd6', 'no', 'V'),
        @('d6', 'h4', 'sí', 'H'), @('h4', 's5', $null, 'H'), @('s5', 'x2', $null, 'V'),
        @('d6', 'h5', 'no', 'V'), @('h5', 's6', $null, 'VH'),
        @('s6', 'h6', $null, @(, @($xS1, (Y 23)))),
        @('h6', 'ap', $null, @(, @(($xRH1 + 1500), (Y 24)))),
        @('ap', 'h7', $null, @(, @($xAP1, (Y 25)))),
        @('h7', 'h8', $null, 'V'), @('h8', 's7', $null, 'VH'), @('s7', 'f2', $null, 'V'))
    Notes = @(
        @("Dos niveles: requerimiento y vacante (inicio y final) y, en medio, el recorrido de CADA postulación. Una vacante tiene varias: las descartadas terminan en su fin de flujo (⊗) y no llegan al ranking ni a la decisión; la vacante sigue con las demás.`nTransversal (RF-27): cada acción crítica queda en audit_logs.`nTras RF-23 no hay cambios manuales de etapa (A-28).`nCierre 'desierta' no implementado (A-30).`nEl riesgo operacional (RF-29) no participa en este flujo.", 163000, (Y 9), 26000),
        @('Nivel del requerimiento y de la vacante', $xA, (Y 5), 15000),
        @('Por cada postulación de la vacante', $xA, (Y 11), 15000),
        @('De nuevo a nivel de la vacante', $xA, (Y 23), 15000))
}

# ---------------------------------------------------------------------------
# AC-02: una sola columna principal; las salidas que no son predictivas van a la
# derecha y vuelven a la tarjeta por rutas separadas.
$x0 = 0; $xL = -20000; $xR = 22000
$yCard = -65000
$acts['AC-02'] = @{
    Name = 'AC-02 Consulta del riesgo operacional (RF-29) <<experimental>>'; File = 'AC-02-riesgo-operacional'
    Nodes = @(
        @{ Id = 'i0'; Kind = 'Start'; Name = 'Inicio de la consulta'; X = $x0; Y = 0 },
        @{ Id = 'b1'; Kind = 'Activity'; Name = 'RR. HH. o Aprobador abre el detalle de la vacante'; X = $x0; Y = -5000; W = 15000 },
        @{ Id = 'b2'; Kind = 'Activity'; Name = 'La tarjeta pide GET vacantes/{id}/riesgo-operacional'; X = $x0; Y = -10000; W = 15000 },
        @{ Id = 'q1'; Kind = 'Decision'; Name = '¿Misma organización y rol autorizado?'; X = $x0; Y = -15500; W = 13000; H = 4400 },
        @{ Id = 'b3'; Kind = 'Activity'; Name = '403'; X = $xL; Y = -15500; W = 9000 },
        @{ Id = 'fA'; Kind = 'End'; Final = 'activity'; Name = 'Fin: acceso denegado'; X = $xL; Y = -21000 },
        @{ Id = 'q2'; Kind = 'Decision'; Name = '¿Elegible? publicada, closes_at, target_completion_at, checkpoint alcanzado, no cerrada, plazo > checkpoint, consulta antes del plazo'; X = $x0; Y = -25500; W = 22000; H = 8000 },
        @{ Id = 'b4'; Kind = 'Activity'; Name = 'descriptive_only (motivo)'; X = ($xR + 4000); Y = -25500; W = 12000 },
        @{ Id = 'b5'; Kind = 'Activity'; Name = 'Construir 15 features en el checkpoint'; X = $x0; Y = -33500; W = 15000 },
        @{ Id = 'q3'; Kind = 'Decision'; Name = '¿ML_SERVICE_ENABLED?'; X = $x0; Y = -39000; W = 18000; H = 4400 },
        @{ Id = 'b6'; Kind = 'Activity'; Name = 'descriptive_only (service_disabled)'; X = $xR; Y = -39000; W = 14000 },
        @{ Id = 'b7'; Kind = 'Activity'; Name = 'POST /v1/predict + X-Internal-Token'; X = $x0; Y = -45500; W = 15000 },
        @{ Id = 'q4'; Kind = 'Decision'; Name = '¿Respuesta válida y contrato congelado?'; X = $x0; Y = -51500; W = 13000; H = 4800 },
        @{ Id = 'b8'; Kind = 'Activity'; Name = 'unavailable (motivo)'; X = $xR; Y = -51500; W = 14000 },
        @{ Id = 'b9'; Kind = 'Activity'; Name = 'predictive_available (risk_score, risk_flag)'; X = $x0; Y = -58500; W = 17000 },
        @{ Id = 'b10'; Kind = 'Activity'; Name = "Mostrar tarjeta «Experimental» con mensaje y aviso de decisión humana"; X = $x0; Y = $yCard; W = 17000; H = 3800 },
        @{ Id = 'fB'; Kind = 'End'; Final = 'activity'; Name = 'Fin de la consulta'; X = $x0; Y = -71000 })
    Links = @(
        @('i0', 'b1', $null, 'V'), @('b1', 'b2', $null, 'V'), @('b2', 'q1', $null, 'V'),
        @('q1', 'b3', 'no', 'H'), @('b3', 'fA', $null, 'V'), @('q1', 'q2', 'sí', 'V'),
        @('q2', 'b4', 'no', 'H'), @('q2', 'b5', 'sí', 'V'), @('b5', 'q3', $null, 'V'),
        @('q3', 'b6', 'no', 'H'), @('q3', 'b7', 'sí', 'V'), @('b7', 'q4', $null, 'V'),
        @('q4', 'b8', 'no', 'H'), @('q4', 'b9', 'sí', 'V'), @('b9', 'b10', $null, 'V'),
        @('b4', 'b10', $null, @(@(37000, -25500), @(37000, ($yCard - 1100)))),
        @('b6', 'b10', $null, @(@(34000, -39000), @(34000, $yCard))),
        @('b8', 'b10', $null, @(@(31000, -51500), @(31000, ($yCard + 1100)))),
        @('b10', 'fB', $null, 'V'))
    Notes = @(, @('Sin efectos: no se persiste, no cambia postulaciones ni ranking, no notifica. No es una actividad de selección.', 48000, $yCard, 17000))
}

$only = @()
if ($env:PD_ONLY) { $only = $env:PD_ONLY -split ',' | ForEach-Object { $_.Trim() } }

Open-Pd
try {
    $m = $Pd.OpenModel($OomFile)
    foreach ($key in $acts.Keys) {
        if ($only.Count -and ($only -notcontains $key)) { continue }
        $sp = $acts[$key]
        $d = New-FlowDiagram $m $m.ActivityDiagrams $sp.Name ($key.Replace('-', '_')) $sp
        Export-Diagram $d $sp.File
        "$key : nodos=$($sp.Nodes.Count) flujos=$($sp.Links.Count) carriles=$(@($sp.Lanes).Count)"
    }
    Save-Model $m $OomFile
    "diagramas de actividad=$(@($m.ActivityDiagrams).Count) actividades=$(@($m.Activities).Count) flujos=$(@($m.Flows).Count)"
    $m.Close()
} catch {
    "ERROR linea $($_.InvocationInfo.ScriptLineNumber): $($_.Exception.Message)"
    "  $($_.InvocationInfo.Line.Trim())"
    if ($m) { try { $m.Close() } catch {} }
} finally { Close-Pd }
