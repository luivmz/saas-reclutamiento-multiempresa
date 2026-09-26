# UC-01 · Casos de uso. Fuente: docs/v1.1/uml/use-cases.md (§1 actores, §2 casos, §3 include/extend,
# §4 notas, §5 asociaciones) y puml/uc-01-use-cases.puml.
. "$PSScriptRoot\pdlib.ps1"

$ucs = [ordered]@{
    RF01 = 'Registrar requerimiento de personal'; RF02 = 'Validar y corregir requerimiento'
    RF03 = 'Registrar aprobación o rechazo del requerimiento'; RF04 = 'Notificar rechazo del requerimiento'
    RF05 = 'Registrar perfil y criterios del puesto'; RF06 = 'Configurar y validar vacante'; RF07 = 'Publicar vacante'
    RF08 = 'Gestionar cuenta y acceso del postulante'; RF09 = 'Gestionar perfil y CV del postulante'
    RF10 = 'Registrar postulación'; RF11 = 'Confirmar postulación al postulante'
    RF12 = 'Consultar y revisar postulaciones'; RF13 = 'Registrar preselección o descarte'
    RF14 = 'Gestionar cambio de etapa de la postulación'; RF15 = 'Notificar cambio de etapa al candidato'
    RF16 = 'Programar evaluación'; RF17 = 'Generar convocatoria de evaluación'; RF18 = 'Programar entrevista'
    RF19 = 'Registrar entrevista y su resultado'; RF20 = 'Validar rangos y ponderaciones'
    RF21 = 'Calcular ranking configurable'; RF22 = 'Presentar comparación de candidatos'
    RF23 = 'Registrar decisión final de selección'; RF24 = 'Registrar selección del candidato'
    RF25 = 'Cerrar vacante o convocatoria'; RF26 = 'Notificar resultado y cierre al postulante'
    RF27 = 'Generar registro de auditoría'; RF28 = 'Panel operativo descriptivo'
    RF29 = 'Consultar riesgo operacional del proceso'
}
$stereo = @{ RF23 = 'human decision'; RF28 = 'propuesto v1.1'; RF29 = 'experimental' }

$actors = [ordered]@{
    SOL = 'Área solicitante'; RH = 'Recursos Humanos'; APR = 'Aprobador / Dirección'
    EVA = 'Evaluador'; POS = 'Postulante'; ML = 'Servicio de riesgo operacional'
}
# use-cases.md §5
$assoc = @{
    SOL = @('RF01', 'RF02')
    RH  = @('RF02', 'RF05', 'RF06', 'RF07', 'RF12', 'RF13', 'RF14', 'RF16', 'RF18', 'RF22', 'RF24', 'RF25', 'RF29')
    APR = @('RF03', 'RF12', 'RF22', 'RF23', 'RF27', 'RF29')
    EVA = @('RF19')
    POS = @('RF08', 'RF09', 'RF10')
    ML  = @('RF29')
}
# use-cases.md §3: origen -> destino (flecha de la dependencia)
$deps = @(
    @('RF04', 'RF03', 'extend', '[decisión = rechazar]'),
    @('RF06', 'RF20', 'include', ''), @('RF07', 'RF06', 'include', ''), @('RF10', 'RF11', 'include', ''),
    @('RF13', 'RF15', 'include', ''), @('RF14', 'RF15', 'include', ''), @('RF16', 'RF17', 'include', ''),
    @('RF18', 'RF17', 'include', ''), @('RF19', 'RF20', 'include', ''), @('RF21', 'RF20', 'include', ''),
    @('RF22', 'RF21', 'include', ''), @('RF23', 'RF21', 'include', '(solo instantánea)'), @('RF25', 'RF26', 'include', '')
)

Open-Pd
try {
    $m = $Pd.OpenModel($OomFile)
    $d = $m.UseCaseDiagrams.CreateNew()
    $d.Name = 'UC-01 Casos de uso AS-IS v1.1'
    $d.Code = 'UC_01'

    $o = @{}; $s = @{}
    foreach ($k in $actors.Keys) {
        $a = New-Obj $m 'Actor' $actors[$k] "ACT_$k"
        if ($k -eq 'ML') { $a.Stereotype = 'external service, experimental' }
        $o[$k] = $a; $s[$k] = $d.AttachObject($a)
    }
    foreach ($k in $ucs.Keys) {
        $u = New-Obj $m 'UseCase' "$($k.Insert(2, '-')) $($ucs[$k])" "UC_$k"
        if ($stereo.ContainsKey($k)) { $u.Stereotype = $stereo[$k] }
        $o[$k] = $u; $s[$k] = $d.AttachObject($u)
    }
    # Disposición manual por bandas de proceso (la automática cruzaba todo).
    # Columnas C1 -26000 · C2 0 · C3 26000 · C4 52000; RR. HH. en el pasillo x=13000.
    $pos = @{
        RF01 = @(-26000, 0); RF02 = @(-26000, -7500); RF05 = @(-26000, -17500); RF06 = @(-26000, -25000); RF07 = @(-26000, -32500)
        RF08 = @(-26000, -45000); RF09 = @(-26000, -52500); RF10 = @(-26000, -60000); RF11 = @(-26000, -67500)
        RF03 = @(0, 0); RF04 = @(0, -7500); RF20 = @(0, -45000); RF19 = @(0, -55000)
        RF12 = @(26000, -15000); RF13 = @(26000, -22500); RF14 = @(26000, -30000); RF16 = @(26000, -37500); RF18 = @(26000, -45000)
        RF21 = @(26000, -60000); RF22 = @(26000, -67500); RF23 = @(26000, -75000); RF24 = @(26000, -82500); RF25 = @(26000, -90000)
        RF15 = @(52000, -22500); RF17 = @(52000, -37500); RF29 = @(52000, -52500); RF27 = @(52000, -75000); RF26 = @(52000, -90000); RF28 = @(52000, -102500)
        SOL = @(-56000, -3750); POS = @(-56000, -52500); RH = @(13000, -40000); EVA = @(13000, -100000)
        APR = @(84000, -10000); ML = @(84000, -52500)
    }
    foreach ($key in $pos.Keys) { Set-Pos $s[$key] $pos[$key][0] $pos[$key][1] }

    $links = @()
    foreach ($k in $assoc.Keys) {
        foreach ($uc in $assoc[$k]) {
            $l = $m.CreateObject($PdKind.UseCaseAssociation); $l.Object1 = $o[$k]; $l.Object2 = $o[$uc]
            $links += , @($d.AttachLinkObject($l, $s[$k], $s[$uc]), $k, $uc)
        }
    }
    foreach ($dp in $deps) {
        $l = $m.CreateObject($PdKind.Dependency); $l.Object1 = $o[$dp[0]]; $l.Object2 = $o[$dp[1]]
        $l.Stereotype = $dp[2]
        if ($dp[3]) { $l.Name = $dp[3] } else { $l.Name = $BlankName }
        $links += , @($d.AttachLinkObject($l, $s[$dp[0]], $s[$dp[1]]), $dp[0], $dp[1])
    }
    foreach ($x in $links) { Set-StraightLink $x[0] $s[$x[1]] $s[$x[2]] }

    # Notas de use-cases.md §4
    Add-Note $d "RF-23 <<human decision>>: solo el Aprobador de la misma organización, con confirmación explícita y justificación (>= 20 caracteres). Candidato finalista, no necesariamente el primero del ranking. No cambia estados por sí sola y no depende del ML." -6000 -78000 20000 | Out-Null
    Add-Note $d "RF-21 / RF-22: soporte a la decisión. Calculan, ordenan y comparan; no seleccionan, no descartan ni cambian el estado de ninguna postulación." -6000 -90000 20000 | Out-Null
    Add-Note $d "RF-29 <<experimental>>: riesgo operacional del PROCESO de la vacante, no del candidato. No productivo. 15 features operacionales, sin identificadores ni PII. No alimenta RF-21, RF-22 ni RF-23." 84000 -64000 20000 | Out-Null
    Add-Note $d "RF-27 transversal: AuditLogger registra 23 acciones críticas (RF-01..RF-03, RF-05..RF-10, RF-13, RF-14, RF-16, RF-18, RF-19, RF-23..RF-26). Tabla de solo inserción. El Aprobador consulta la auditoría." 84000 -80000 20000 | Out-Null
    Add-Note $d "RF-28: candidato NO implementado (<<propuesto v1.1>>). El estado descriptive_only de RF-29 no es este panel." 84000 -100000 20000 | Out-Null
    Add-Note $d "RF-07: solo RR. HH. publica. Efecto: la vacante aparece en /empleos, que cualquiera (con o sin sesión) consulta. La consulta es contexto de RF-10, no una asociación del Postulante con RF-07." -60000 -30000 20000 | Out-Null
    Add-Note $d "RF-24: precondición, decisión final registrada (RF-23)." 4000 -104000 14000 | Out-Null
    Add-Note $d "Multiempresa: todos los casos del personal operan dentro de su organización (Policy de rol y organización). El Postulante es global y solo ve lo suyo." -60000 -80000 20000 | Out-Null

    Show-LinkNames $d
    Export-Diagram $d 'UC-01-casos-de-uso'
    Save-Model $m $OomFile
    "actores=$(@($m.Actors).Count) casos=$(@($m.UseCases).Count) asociaciones=$(@($m.UseCaseAssociations).Count) dependencias=$(@($m.Dependencies).Count)"
    $m.Close()
} catch {
    "ERROR linea $($_.InvocationInfo.ScriptLineNumber): $($_.Exception.Message)"
    "  $($_.InvocationInfo.Line.Trim())"
    if ($m) { try { $m.Close() } catch {} }
} finally { Close-Pd }
