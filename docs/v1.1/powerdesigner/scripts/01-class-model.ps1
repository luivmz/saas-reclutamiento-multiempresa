# CL-01 · Modelo de clases del dominio.
# Fuente: docs/v1.1/uml/class-model.md (§2 clases, §3 asociaciones, §4 enums, §5 notas).
# Crea el OOM desde cero: este es el primer script de la serie.
. "$PSScriptRoot\pdlib.ps1"

$classes = [ordered]@{
    'Organization'            = @{ T = $false; A = @('name', 'slug', 'tax_id', 'is_active') }
    'User'                    = @{ T = $false; A = @('name', 'email', 'role : UserRole', 'organization_id') }
    'JobRequest'              = @{ T = $true;  A = @('organization_id', 'code', 'position_title', 'area', 'headcount', 'contract_type', 'justification', 'required_by', 'status : JobRequestStatus', 'observation', 'submitted_at', 'validated_at', 'decided_at', 'decision_comment') }
    'JobRequestStatusHistory' = @{ T = $true;  A = @('organization_id', 'from_status', 'to_status', 'comment', 'created_at') }
    'Vacancy'                 = @{ T = $true;  A = @('organization_id', 'code', 'title', 'summary', 'location', 'contract_type', 'positions', 'opens_at', 'closes_at', 'target_completion_at', 'status : VacancyStatus', 'published_at', 'closed_at', 'closure_type : VacancyClosureType', 'closure_notes') }
    'JobProfile'              = @{ T = $true;  A = @('organization_id', 'education', 'experience', 'functions', 'competencies') }
    'EvaluationCriterion'     = @{ T = $true;  A = @('organization_id', 'name', 'stage : CriterionStage', 'weight', 'min_score', 'max_score') }
    'CandidateProfile'        = @{ T = $false; A = @('phone', 'city', 'education_level', 'professional_title', 'years_of_experience', 'summary') }
    'CandidateDocument'       = @{ T = $false; A = @('type : DocumentType', 'original_name', 'stored_path', 'mime_type', 'size_bytes') }
    'Application'             = @{ T = $true;  A = @('organization_id', 'status : ApplicationStatus', 'applied_at', 'stage_changed_at') }
    'ApplicationStageHistory' = @{ T = $true;  A = @('organization_id', 'from_status', 'to_status', 'comment', 'created_at') }
    'Evaluation'              = @{ T = $true;  A = @('organization_id', 'type : EvaluationType', 'modality', 'location', 'scheduled_at', 'duration_minutes', 'instructions', 'status : AssessmentStatus', 'invitation_sent_at', 'completed_at', 'observations') }
    'EvaluationResult'        = @{ T = $true;  A = @('organization_id', 'score', 'comment') }
    'Interview'               = @{ T = $true;  A = @('organization_id', 'modality', 'location', 'scheduled_at', 'duration_minutes', 'instructions', 'status : AssessmentStatus', 'outcome : InterviewOutcome', 'invitation_sent_at', 'completed_at', 'observations') }
    'InterviewResult'         = @{ T = $true;  A = @('organization_id', 'score', 'comment') }
    'SelectionDecision'       = @{ T = $true;  A = @('organization_id', 'justification', 'selected_position', 'selected_score', 'ranked_candidates', 'decided_at', 'selection_registered_at'); S = 'human decision' }
    'AuditLog'                = @{ T = $true;  A = @('organization_id', 'action : AuditAction', 'auditable_type', 'auditable_id', 'metadata', 'ip_address', 'created_at'); S = 'append only' }
}

$enums = [ordered]@{
    'UserRole'           = @('solicitante', 'rrhh', 'aprobador', 'evaluador', 'postulante')
    'JobRequestStatus'   = @('borrador', 'enviado', 'observado', 'validado', 'aprobado', 'rechazado')
    'VacancyStatus'      = @('borrador', 'publicada', 'cerrada')
    'VacancyClosureType' = @('con_seleccion', 'desierta')
    'ApplicationStatus'  = @('postulado', 'preseleccionado', 'en_evaluacion', 'en_entrevista', 'finalista', 'seleccionado', 'no_seleccionado', 'descartado')
    'AssessmentStatus'   = @('programada', 'realizada')
    'CriterionStage'     = @('evaluacion', 'entrevista')
    'InterviewOutcome'   = @('recomendado', 'recomendado_con_reservas', 'no_recomendado')
    'EvaluationType'     = @('conocimientos', 'clase_modelo', 'practica', 'otra')
    'DocumentType'       = @('cv')
}

# Filas de class-model.md §3: A, mult. A, mult. B, B, rol en A, rol en B, composición (todo = A).
# La fila 2 se dibuja como dos asociaciones (JobRequest y Vacancy), igual que el borrador .puml;
# la fila 35 (AuditLog -> entidad auditada, polimórfica) es una dependencia y va como nota.
$assocs = @(
    @('1',  'Organization', '0..1', '0..*', 'User', 'organization', '', $false),
    @('2a', 'Organization', '1', '0..*', 'JobRequest', 'organization', '', $false),
    @('2b', 'Organization', '1', '0..*', 'Vacancy', 'organization', '', $false),
    @('3',  'Organization', '0..1', '0..*', 'AuditLog', 'organization', '', $false),
    @('4',  'User', '1', '0..*', 'JobRequest', 'requester', '', $false),
    @('5',  'User', '0..1', '0..*', 'JobRequest', 'validator', '', $false),
    @('6',  'User', '0..1', '0..*', 'JobRequest', 'decider', '', $false),
    @('7',  'JobRequest', '1', '0..*', 'JobRequestStatusHistory', '', 'statusHistories', $true),
    @('8',  'JobRequestStatusHistory', '0..*', '1', 'User', '', 'author', $false),
    @('9',  'JobRequest', '1', '0..1', 'Vacancy', 'jobRequest', 'vacancy', $false),
    @('10', 'Vacancy', '1', '1', 'JobProfile', '', 'profile', $true),
    @('11', 'Vacancy', '1', '0..*', 'EvaluationCriterion', '', 'criteria', $true),
    @('12', 'User', '1', '0..*', 'Vacancy', 'creator', '', $false),
    @('13', 'User', '0..1', '0..*', 'Vacancy', 'publisher', '', $false),
    @('14', 'User', '0..1', '0..*', 'Vacancy', 'closer', '', $false),
    @('15', 'Vacancy', '1', '0..*', 'Application', 'vacancy', 'applications', $false),
    @('16', 'User', '1', '0..*', 'Application', 'candidate', 'applications', $false),
    @('17', 'User', '1', '0..1', 'CandidateProfile', 'user', 'candidateProfile', $true),
    @('18', 'CandidateProfile', '1', '0..*', 'CandidateDocument', 'profile', 'documents', $true),
    @('19', 'Application', '0..*', '0..1', 'CandidateDocument', '', 'cvDocument', $false),
    @('20', 'Application', '1', '0..*', 'ApplicationStageHistory', '', 'stageHistories', $true),
    @('21', 'ApplicationStageHistory', '0..*', '1', 'User', '', 'author', $false),
    @('22', 'Application', '1', '0..*', 'Evaluation', 'application', 'evaluations', $false),
    @('23', 'Application', '1', '0..*', 'Interview', 'application', 'interviews', $false),
    @('24', 'User', '1', '0..*', 'Evaluation', 'evaluator', '', $false),
    @('25', 'User', '1', '0..*', 'Interview', 'evaluator', '', $false),
    @('26', 'Evaluation', '1', '0..*', 'EvaluationResult', '', 'results', $true),
    @('27', 'Interview', '1', '0..*', 'InterviewResult', '', 'results', $true),
    @('28', 'EvaluationCriterion', '1', '0..*', 'EvaluationResult', 'criterion', '', $false),
    @('29', 'EvaluationCriterion', '1', '0..*', 'InterviewResult', 'criterion', '', $false),
    @('30', 'Vacancy', '1', '0..1', 'SelectionDecision', 'vacancy', 'selectionDecision', $false),
    @('31', 'SelectionDecision', '0..1', '1', 'Application', '', 'selectedApplication', $false),
    @('32', 'User', '1', '0..*', 'SelectionDecision', 'decider', '', $false),
    @('33', 'User', '0..1', '0..*', 'SelectionDecision', 'selectionRegistrar', '', $false),
    @('34', 'User', '0..1', '0..*', 'AuditLog', 'user', '', $false),
    @('36', 'User', '1', '0..*', 'Evaluation', 'scheduler', '', $false),
    @('37', 'User', '1', '0..*', 'Interview', 'scheduler', '', $false)
)

Open-Pd
try {
    if (Test-Path $OomFile) { Remove-Item $OomFile -Force }
    $m = $Pd.CreateModel($PdKind.Model, '|Language=Analysis|Diagram=ClassDiagram')
    $m.Name = 'SaaS Reclutamiento v1.1 - UML AS-IS'
    $m.Code = 'SAAS_RECLUTAMIENTO_V11_UML'
    $m.Comment = 'Formalizacion en PowerDesigner (Fase 23) de la especificacion UML AS-IS de la Fase 22 (docs/v1.1/uml/). Base develop 2621bee.'

    $pkModels = New-Obj $m 'Package' 'App\Models' 'App_Models'
    $pkEnums = New-Obj $m 'Package' 'App\Enums' 'App_Enums'

    $obj = @{}
    foreach ($name in $classes.Keys) {
        $spec = $classes[$name]
        $c = New-Obj $pkModels 'Class' $name $name
        $st = @()
        if ($spec.T) { $st += 'tenant scoped' }
        if ($spec.S) { $st += $spec.S }
        if ($st.Count) { $c.Stereotype = ($st -join ', ') }
        foreach ($a in $spec.A) {
            $parts = $a -split ' : '
            $at = New-Obj $c 'Attribute' $parts[0] $parts[0]
            $at.Visibility = '+'
            if ($parts.Count -gt 1) { $at.DataType = $parts[1] } else { $at.DataType = '' }
        }
        $obj[$name] = $c
    }
    foreach ($name in $enums.Keys) {
        $e = New-Obj $pkEnums 'Class' $name $name
        $e.Stereotype = 'enumeration'
        foreach ($v in $enums[$name]) { $at = New-Obj $e 'Attribute' $v $v; $at.Visibility = '+'; $at.DataType = '' }
        $obj[$name] = $e
    }

    $assocObjs = @()
    foreach ($r in $assocs) {
        $as = $pkModels.CreateObject($PdKind.Association)
        $as.Object1 = $obj[$r[1]]
        $as.Object2 = $obj[$r[4]]
        $as.RoleAMultiplicity = $r[2]
        $as.RoleBMultiplicity = $r[3]
        if ($r[5]) { $as.RoleAName = $r[5] }
        if ($r[6]) { $as.RoleBName = $r[6] }
        $as.RoleANavigability = $false
        $as.RoleBNavigability = $false
        $as.Name = "A$($r[0])"
        $as.Code = "A$($r[0])"
        $as.Comment = "class-model.md §3, fila $($r[0])"
        if ($r[7]) { $as.RoleAIndicator = 'C' }
        $assocObjs += , @($as, $r)
    }

    # --- Diagrama CL-01 (clases del dominio) ---
    $d = $pkModels.ClassDiagrams.Item(0)
    $d.Name = 'CL-01 Clases del dominio'
    $d.Code = 'CL_01'
    $sym = @{}
    foreach ($name in $classes.Keys) { $sym[$name] = $d.AttachObject($obj[$name]) }
    # Disposición manual: User al centro y sus clases en anillo, para que las
    # 18 asociaciones de User salgan radiales y sus roles no se encimen.
    $pos = @{
        'User' = @(0, 0); 'Organization' = @(0, 42000); 'AuditLog' = @(30000, 38000)
        'JobRequest' = @(44000, 14000); 'JobRequestStatusHistory' = @(70000, 40000)
        'Vacancy' = @(44000, -18000); 'JobProfile' = @(80000, -8000); 'SelectionDecision' = @(30000, -44000)
        'CandidateProfile' = @(-22000, 42000); 'CandidateDocument' = @(-74000, 24000)
        'ApplicationStageHistory' = @(-44000, 20000); 'Application' = @(-48000, -8000)
        'Evaluation' = @(-34000, -40000); 'Interview' = @(0, -46000)
        'EvaluationResult' = @(-34000, -74000); 'InterviewResult' = @(0, -80000)
        'EvaluationCriterion' = @(44000, -74000)
    }
    foreach ($name in $pos.Keys) { Set-Pos $sym[$name] $pos[$name][0] $pos[$name][1] }
    # User recibe 18 asociaciones: un símbolo más grande reparte sus extremos por el borde.
    Set-Rect $sym['User'] -8500 6000 8500 -6000

    # Vínculos rectos; los que unen el mismo par de clases van en paralelo.
    $groups = @{}
    foreach ($pair in $assocObjs) { $pairKey = (@($pair[1][1], $pair[1][4]) | Sort-Object) -join "|"; $groups[$pairKey] = 1 + [int]$groups[$pairKey] }
    # Escalonado de rótulos en el extremo de User: vecinos por ángulo alternan la distancia.
    $uc = Get-Center $sym['User']
    $userLinks = @($assocObjs | Where-Object { $_[1][1] -eq 'User' -or $_[1][4] -eq 'User' } | Sort-Object {
        $other = if ($_[1][1] -eq 'User') { $_[1][4] } else { $_[1][1] }
        $oc = Get-Center $sym[$other]; [Math]::Atan2($oc[1] - $uc[1], $oc[0] - $uc[0])
    })
    $along = @{}
    for ($j = 0; $j -lt $userLinks.Count; $j++) { $along[$userLinks[$j][1][0]] = @(0, 1600, 3200, 4800)[$j % 4] }
    $seen = @{}
    foreach ($pair in $assocObjs) {
        $as = $pair[0]; $r = $pair[1]
        $pairKey = (@($r[1], $r[4]) | Sort-Object) -join "|"
        $i = [int]$seen[$pairKey]; $seen[$pairKey] = $i + 1
        $ls = $d.AttachLinkObject($as, $sym[$r[1]], $sym[$r[4]])
        $aA = 0; $aB = 0
        if ($along.ContainsKey($r[0])) { if ($r[1] -eq 'User') { $aA = $along[$r[0]] } else { $aB = $along[$r[0]] } }
        Set-StraightLink $ls $sym[$r[1]] $sym[$r[4]] $i $groups[$pairKey] 3400 $aA $aB
    }

    # Notas de class-model.md (§3 índice parcial y criterios por etapa, §5 multiempresa) y fila 35.
    Add-Note $d "Multiempresa: aislamiento lógico. Las 13 clases <<tenant scoped>> llevan organization_id, OrganizationScope y Policies de rol y organización. Solo se dibujan las asociaciones con Organization de User, JobRequest, Vacancy y AuditLog. Sin PostgreSQL RLS ni base por tenant." -64000 52000 24000 | Out-Null
    Add-Note $d "Globales: User (postulante), CandidateProfile y CandidateDocument no llevan organization_id. El CV vive en el disco privado local de Laravel." -84000 44000 18000 | Out-Null
    Add-Note $d "UNIQUE (vacancy_id, candidate_id). Índice parcial: como mucho una postulación 'seleccionado' por vacante." -82000 -26000 18000 | Out-Null
    Add-Note $d "<<human decision>>: una por vacante, inmutable. Guarda la instantánea del ranking al decidir. No depende del ML (RF-23)." 72000 -44000 18000 | Out-Null
    Add-Note $d "stage separa los criterios de evaluación y de entrevista; lo aplica ScoreSheetValidator, no una FK." 80000 -86000 18000 | Out-Null
    Add-Note $d "Fila 35: AuditLog depende de la entidad auditada (auditable_type + auditable_id, polimórfica). Trigger audit_logs_append_only: rechaza DELETE y todo UPDATE, salvo anular user_id al borrar el usuario." 74000 58000 22000 | Out-Null
    Add-Note $d "scheduler (scheduled_by, RR. HH. que programa) y evaluator (evaluator_id, evaluador asignado) son asociaciones distintas de User con Evaluation e Interview (filas 24/36 y 25/37)." -78000 -52000 18000 | Out-Null

    # --- CL-01b Enumeraciones (vista auxiliar del mismo modelo) ---
    $de = $pkEnums.ClassDiagrams.Item(0)
    $de.Name = 'CL-01b Enumeraciones'
    $de.Code = 'CL_01b'
    $j = 0
    foreach ($name in $enums.Keys) {
        $s = $de.AttachObject($obj[$name])
        Set-Pos $s (($j % 5) * 11000) (-[Math]::Floor($j / 5) * 12000)
        $j++
    }
    Add-Note $de "Valores reales de app/Enums. AuditAction (23 acciones) se documenta como diccionario, no como enumeración dibujada. VacancyClosureType.desierta existe pero no tiene flujo implementado (A-30)." 22000 -22000 30000 | Out-Null

    Export-Diagram $d 'CL-01-clases-del-dominio'
    Export-Diagram $de 'CL-01b-enumeraciones'
    Save-Model $m $OomFile
    "clases=$(@($pkModels.Classes).Count) enums=$(@($pkEnums.Classes).Count) asociaciones=$(@($pkModels.Associations).Count) composiciones=$(@(@($pkModels.Associations) | Where-Object { $_.RoleAIndicator -eq 'C' }).Count)"
    $m.Close()
} catch {
    "ERROR linea $($_.InvocationInfo.ScriptLineNumber): $($_.Exception.Message)"
    "  $($_.InvocationInfo.Line.Trim())"
    if ($m) { try { $m.Close() } catch {} }
} finally { Close-Pd }
