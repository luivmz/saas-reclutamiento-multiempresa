# SEQ-01..SEQ-08. Fuente: docs/v1.1/uml/sequence-diagrams.md y puml/seq-0*.puml.
# Trabaja sobre el OOM existente: cada secuencia se crea o, si ya existe, se reemplaza.
# $env:PD_ONLY (p. ej. "SEQ-01,SEQ-02") limita qué secuencias se generan en una corrida.
. "$PSScriptRoot\pdlib.ps1"
. "$PSScriptRoot\seqlib.ps1"

$seqs = [ordered]@{}
# Espacios iniciales: la pestaña «critical» es más ancha que el margen de la guarda y
# taparía sus primeros caracteres. El texto de la guarda es «DB::transaction».
$critical = '      DB::transaction'

$seqs['SEQ-01'] = @{
    Name = 'SEQ-01 Registrar postulación (RF-10, RF-11)'; File = 'SEQ-01-registrar-postulacion'; Gap = 11000; Row = 3200
    Lifelines = @(@('POS', 'Postulante', 'actor'), @('UI', 'UI jobs/show'), @('C', 'ApplyController'), @('P', 'ApplicationPolicy'),
        @('S', 'ApplicationService'), @('DB', 'PostgreSQL'), @('A', 'AuditLogger'), @('Q', 'Cola Redis'))
    Messages = @(
        @('POS', 'UI', 'Postular'), @('UI', 'C', 'POST empleos/{vacancy}/postular'), @('C', 'P', 'apply(user)'),
        @('P', 'C', 'solo rol postulante', 'return'), @('C', 'S', 'apply(candidate, vacancy)'),
        @('S', 'DB', 'Vacancy lockForUpdate (sin global scope)'),
        @('S', 'C', 'BusinessRuleException', 'return'), @('C', 'UI', 'redirección con error', 'return'),
        @('S', 'DB', 'Application (postulado, CV más reciente)'), @('S', 'DB', 'ApplicationStageHistory (null -> postulado)'),
        @('S', 'A', 'record(ApplicationSubmitted)'),
        @('S', 'Q', 'ApplicationReceivedNotification (RF-11, afterCommit)'), @('C', 'UI', 'redirección + toast', 'return'))
    Fragments = @(
        @{ Type = 'critical'; Cond = $critical; From = 6; To = 11; Lanes = @('UI', 'A'); Pad = 3500; Nest = 0 },
        @{ Type = 'alt'; Cond = 'no abierta | perfil incompleto | sin CV | duplicada'; From = 7; To = 11; Lanes = @('UI', 'A'); Pad = 2500; Nest = 1; Else = @(, @(9, 'válida')) })
    Notes = @(, @('UNIQUE (vacancy_id, candidate_id) también rechaza el duplicado concurrente.', 9, 18000))
}

$seqs['SEQ-02'] = @{
    Name = 'SEQ-02 Aprobar o rechazar requerimiento (RF-03, RF-04)'; File = 'SEQ-02-aprobar-rechazar-requerimiento'; Gap = 11000; Row = 3200
    Lifelines = @(@('APR', 'Aprobador / Dirección', 'actor'), @('UI', 'UI job-requests/show'), @('C', 'JobRequestTransitionController'),
        @('R', 'DecideJobRequestRequest'), @('P', 'JobRequestPolicy'), @('W', 'JobRequestWorkflow'), @('DB', 'PostgreSQL'),
        @('A', 'AuditLogger'), @('Q', 'Cola Redis'))
    Messages = @(
        @('APR', 'UI', 'aprobar | rechazar (+ motivo)'), @('UI', 'C', 'POST requerimientos/{id}/decision'),
        @('C', 'R', 'authorize() + rules()'), @('R', 'P', 'decide(user, jobRequest)'),
        @('P', 'R', 'aprobador de la misma organización', 'return'),
        @('C', 'W', 'approve(jobRequest, approver, comment)'), @('C', 'W', 'reject(jobRequest, approver, comment)'),
        @('W', 'DB', 'JobRequest lockForUpdate'), @('W', 'C', 'InvalidStateTransition', 'return'),
        @('W', 'DB', 'status, decided_by, decided_at, decision_comment'), @('W', 'DB', 'JobRequestStatusHistory'),
        @('W', 'A', 'record(JobRequestApproved | JobRequestRejected)'),
        @('W', 'Q', 'JobRequestRejectedNotification al solicitante (RF-04)'), @('C', 'UI', 'redirección + toast', 'return'))
    Fragments = @(
        @{ Type = 'alt'; Cond = 'decisión = aprobar'; From = 6; To = 7; Lanes = @('C', 'W'); Pad = 3000; Nest = 0; Else = @(, @(7, 'decisión = rechazar (motivo obligatorio)')) },
        @{ Type = 'critical'; Cond = $critical; From = 8; To = 12; Lanes = @('C', 'A'); Pad = 3500; Nest = 0 },
        @{ Type = 'alt'; Cond = 'transición no permitida (no está validado)'; From = 9; To = 12; Lanes = @('C', 'A'); Pad = 2500; Nest = 1; Else = @(, @(10, 'else')) },
        @{ Type = 'opt'; Cond = 'rechazo'; From = 13; To = 13; Lanes = @('W', 'Q'); Pad = 3000; Nest = 0 })
    Notes = @()
}

$seqs['SEQ-03'] = @{
    Name = 'SEQ-03 Cambiar etapa y notificar (RF-13, RF-14, RF-15)'; File = 'SEQ-03-cambiar-etapa'; Gap = 11000; Row = 3200
    Lifelines = @(@('RH', 'Recursos Humanos', 'actor'), @('UI', 'UI applications/show'), @('C', 'ApplicationStageController'),
        @('R', 'StageComment / Discard / ChangeApplicationStage Request'), @('P', 'ApplicationPolicy'), @('S', 'ApplicationStageService'),
        @('DB', 'PostgreSQL'), @('A', 'AuditLogger'), @('Q', 'Cola Redis'))
    Messages = @(
        @('RH', 'UI', 'preseleccionar | descartar | cambiar etapa'), @('UI', 'C', 'POST postulaciones/{id}/preseleccionar | descartar | etapa'),
        @('C', 'R', 'authorize()'), @('R', 'P', 'changeStage(user, application)'), @('P', 'R', 'rrhh de la misma organización', 'return'),
        @('C', 'S', 'shortlist | discard | moveTo(target)'), @('S', 'DB', 'Application lockForUpdate'),
        @('S', 'C', 'excepción de negocio', 'return'), @('S', 'DB', 'status, stage_changed_at'),
        @('S', 'DB', 'ApplicationStageHistory (autor, comentario)'), @('S', 'A', 'record(ApplicationStageChanged)'),
        @('S', 'Q', 'ApplicationStageChangedNotification al postulante (RF-15)'), @('C', 'UI', 'redirección + toast', 'return'))
    Fragments = @(
        @{ Type = 'critical'; Cond = $critical; From = 7; To = 11; Lanes = @('C', 'A'); Pad = 3500; Nest = 0 },
        @{ Type = 'alt'; Cond = 'destino seleccionado/no_seleccionado | decisión final registrada (A-28) | vacante cerrada | transición inválida'; From = 8; To = 11; Lanes = @('C', 'A'); Pad = 2500; Nest = 1; Else = @(, @(9, 'else')) })
    Notes = @()
}

$seqs['SEQ-04'] = @{
    Name = 'SEQ-04 Programar evaluación (RF-16, RF-17)'; File = 'SEQ-04-programar-evaluacion'; Gap = 10000; Row = 3200
    Lifelines = @(@('RH', 'Recursos Humanos', 'actor'), @('UI', 'UI applications/show'), @('C', 'AssessmentScheduleController'),
        @('R', 'ScheduleEvaluationRequest'), @('P', 'ApplicationPolicy'), @('S', 'AssessmentScheduler'), @('ST', 'ApplicationStageService'),
        @('DB', 'PostgreSQL'), @('A', 'AuditLogger'), @('Q', 'Cola Redis'))
    Messages = @(
        @('RH', 'UI', 'tipo, modalidad, lugar, fecha, evaluador'), @('UI', 'C', 'POST postulaciones/{id}/evaluaciones'),
        @('C', 'R', 'authorize() + rules()'), @('R', 'P', 'scheduleAssessment(user, application)'),
        @('P', 'R', 'rrhh de la misma organización', 'return'), @('C', 'S', 'scheduleEvaluation(application, hr, data)'),
        @('S', 'DB', 'Application lockForUpdate'), @('S', 'C', 'BusinessRuleException', 'return'),
        @('S', 'DB', 'Evaluation (programada, invitation_sent_at)'), @('S', 'ST', 'transition(en_evaluacion, notify: false)'),
        @('S', 'A', 'record(EvaluationScheduled)'), @('S', 'Q', 'AssessmentConvocationNotification al postulante (RF-17)'),
        @('S', 'Q', 'AssessmentAssignedNotification al evaluador'), @('C', 'UI', 'redirección + toast', 'return'))
    Fragments = @(
        @{ Type = 'critical'; Cond = $critical; From = 7; To = 11; Lanes = @('C', 'A'); Pad = 3500; Nest = 0 },
        @{ Type = 'alt'; Cond = 'vacante cerrada | sin criterios de evaluación | etapa no admitida | evaluador ajeno'; From = 8; To = 11; Lanes = @('C', 'A'); Pad = 2500; Nest = 1; Else = @(, @(9, 'else')) })
    Notes = @()
}

$seqs['SEQ-05'] = @{
    Name = 'SEQ-05 Programar y registrar entrevista (RF-18, RF-19)'; File = 'SEQ-05-programar-registrar-entrevista'; Gap = 9500; Row = 3200
    Lifelines = @(@('RH', 'Recursos Humanos', 'actor'), @('EV', 'Evaluador', 'actor'), @('UI', 'UI'), @('SC', 'AssessmentScheduleController'),
        @('S', 'AssessmentScheduler'), @('IC', 'InterviewController'), @('IP', 'InterviewPolicy'), @('REC', 'AssessmentResultRecorder'),
        @('V', 'ScoreSheetValidator'), @('DB', 'PostgreSQL'), @('A', 'AuditLogger'), @('Q', 'Cola Redis'))
    Messages = @(
        @('RH', 'UI', 'datos de la entrevista + evaluador'), @('UI', 'SC', 'POST postulaciones/{id}/entrevistas'),
        @('SC', 'S', 'scheduleInterview(application, hr, data)'), @('S', 'DB', 'Application lockForUpdate; Interview (programada)'),
        @('S', 'DB', 'postulación -> en_entrevista (notify: false)'), @('S', 'A', 'record(InterviewScheduled)'),
        @('S', 'Q', 'convocatoria al postulante (RF-17) y aviso al evaluador'),
        @('EV', 'UI', 'abre la sesión asignada'), @('UI', 'IC', 'GET entrevistas/{id}'), @('IC', 'IP', 'view()'),
        @('EV', 'UI', 'puntaje por criterio, resultado, observaciones'), @('UI', 'IC', 'POST entrevistas/{id}/resultados'),
        @('IC', 'REC', 'recordInterview(interview, evaluator, scores, outcome, observations)'),
        @('REC', 'DB', 'Interview lockForUpdate'), @('REC', 'V', 'validar puntajes de la etapa entrevista (RF-20)'),
        @('REC', 'IC', 'excepción', 'return'), @('REC', 'DB', 'InterviewResult por criterio'),
        @('REC', 'DB', 'Interview -> realizada, outcome, completed_at'), @('REC', 'A', 'record(InterviewResultRecorded)'),
        @('IC', 'UI', 'redirección + toast', 'return'))
    Fragments = @(
        @{ Type = 'critical'; Cond = $critical; From = 4; To = 6; Lanes = @('S', 'A'); Pad = 3000; Nest = 0 },
        @{ Type = 'critical'; Cond = $critical; From = 14; To = 19; Lanes = @('IC', 'A'); Pad = 3000; Nest = 0 },
        @{ Type = 'alt'; Cond = 'ya registrada | vacante cerrada | puntaje fuera de rango o criterio ajeno'; From = 16; To = 19; Lanes = @('IC', 'A'); Pad = 2000; Nest = 1; Else = @(, @(17, 'else')) })
    Notes = @(
        @('Tramo A: ScheduleAssessmentRequest -> ApplicationPolicy::scheduleAssessment.', 2, 18000),
        @('Tramo B: RecordInterviewResultRequest -> InterviewPolicy::recordResult (evaluator_id = usuario, misma organización).', 12, 18000))
    Dividers = @(@(1, 'A · Programar (RR. HH.)'), @(8, 'B · Registrar resultado (Evaluador asignado)'))
}

$seqs['SEQ-06'] = @{
    Name = 'SEQ-06 Calcular ranking y comparar (RF-20, RF-21, RF-22)'; File = 'SEQ-06-ranking-comparacion'; Gap = 11000; Row = 3200
    Lifelines = @(@('RH', 'Recursos Humanos', 'actor'), @('UI', 'UI selection/comparison'), @('C', 'VacancyComparisonController'),
        @('P', 'VacancyPolicy'), @('B', 'VacancyRankingBuilder'), @('RS', 'RankingService'), @('PR', 'RankingPresenter'), @('DB', 'PostgreSQL'))
    Messages = @(
        @('RH', 'UI', 'abrir comparación'), @('UI', 'C', 'GET vacantes/{id}/comparacion'), @('C', 'P', 'viewRanking(user, vacancy)'),
        @('P', 'C', 'rrhh o aprobador de la misma organización', 'return'), @('C', 'B', 'forVacancy(vacancy)'),
        @('B', 'DB', 'postulaciones (excepto descartadas)'), @('B', 'DB', 'puntajes de sesiones realizadas'),
        @('B', 'RS', 'rank(criteria, candidates)'), @('RS', 'RS', 'validar configuración y puntajes (RF-20)'),
        @('RS', 'RS', 'promedios, aportes ponderados, total, empates, incompletos'),
        @('RS', 'C', 'InvalidRankingInput', 'return'), @('C', 'C', 'ranking vacío + mensaje de error'),
        @('RS', 'B', 'RankingResult', 'return'), @('B', 'C', 'RankingResult', 'return'),
        @('C', 'PR', 'present(result, applications)'), @('C', 'UI', "Inertia::render('selection/comparison')", 'return'))
    Fragments = @(
        @{ Type = 'alt'; Cond = 'entrada inválida'; From = 11; To = 14; Lanes = @('C', 'RS'); Pad = 3500; Nest = 0; Else = @(, @(13, 'else')) })
    Notes = @(
        @('El ranking no se guarda y no cambia ninguna postulación. Soporte a la decisión, no decisión.', 10, 18000),
        @('El mismo flujo lo ejecuta el Aprobador / Dirección (VacancyPolicy::viewRanking); la lifeline de actor es la de UC-01.', 1, 18000))
}

$seqs['SEQ-07'] = @{
    Name = 'SEQ-07 Registrar decisión final (RF-23) <<human decision>>'; File = 'SEQ-07-decision-final'; Gap = 11000; Row = 3200
    Lifelines = @(@('APR', 'Aprobador / Dirección', 'actor'), @('UI', 'UI selection/comparison'), @('C', 'FinalDecisionController'),
        @('R', 'FinalDecisionRequest'), @('P', 'VacancyPolicy'), @('S', 'FinalDecisionService'), @('B', 'VacancyRankingBuilder'),
        @('DB', 'PostgreSQL'), @('A', 'AuditLogger'))
    Messages = @(
        @('APR', 'UI', 'elige finalista, justificación, confirmación humana'), @('UI', 'C', 'POST vacantes/{id}/decision'),
        @('C', 'R', 'rules(): application_id, justification (20..2000), human_confirmation (accepted)'),
        @('R', 'P', 'decide(user, vacancy)'), @('P', 'R', 'SOLO aprobador de la misma organización', 'return'),
        @('C', 'S', 'decide(vacancy, approver, applicationId, justification)'), @('S', 'DB', 'Vacancy lockForUpdate'),
        @('S', 'C', 'BusinessRuleException', 'return'), @('S', 'B', 'forVacancy(vacancy) — solo instantánea'),
        @('S', 'C', 'BusinessRuleException', 'return'),
        @('S', 'DB', 'SelectionDecision (elegida, decisor, justificación, selected_position, selected_score, ranked_candidates)'),
        @('S', 'A', 'record(SelectionDecisionRecorded)'), @('C', 'UI', 'redirección + toast', 'return'))
    Fragments = @(
        @{ Type = 'critical'; Cond = $critical; From = 7; To = 12; Lanes = @('C', 'A'); Pad = 3500; Nest = 0 },
        @{ Type = 'alt'; Cond = 'no publicada/cerrada | ya decidida | postulación ajena | no finalista'; From = 8; To = 12; Lanes = @('C', 'A'); Pad = 2500; Nest = 1; Else = @(, @(9, 'else')) },
        @{ Type = 'alt'; Cond = 'sin resultados completos'; From = 10; To = 12; Lanes = @('C', 'A'); Pad = 1500; Nest = 2; Else = @(, @(11, 'else')) })
    Notes = @(, @('La persona decide; puede no ser la primera del ranking. No cambia el estado de ninguna postulación (RF-24/RF-25 lo hacen). Única e inmutable. Sin ningún mensaje al servicio de riesgo operacional.', 7, 20000))
}

$seqs['SEQ-08'] = @{
    Name = 'SEQ-08 Consultar riesgo operacional (RF-29) <<experimental>>'; File = 'SEQ-08-riesgo-operacional'; Gap = 11000; Row = 3200
    Lifelines = @(@('RH', 'Recursos Humanos', 'actor'), @('UI', 'OperationalRiskCard (vacancies/show)'), @('C', 'VacancyOperationalRiskController'),
        @('P', 'VacancyPolicy'), @('S', 'OperationalRiskService'), @('FB', 'OperationalRiskFeatureBuilder'), @('MC', 'MlRiskClient'),
        @('DB', 'PostgreSQL', 'object', $null, 6500), @('API', 'FastAPI /v1/predict', 'object', 'external service, experimental', 13000),
        @('M', 'Predictor + modelo congelado', 'object', 'experimental', 8000))
    Messages = @(
        @('RH', 'UI', 'abre el detalle de la vacante'), @('UI', 'C', 'GET vacantes/{id}/riesgo-operacional'),
        @('C', 'P', 'viewOperationalRisk(user, vacancy)'), @('P', 'C', 'rrhh o aprobador de la misma organización', 'return'),
        @('C', 'S', 'assess(vacancy)'), @('S', 'S', 'outOfScopeReason() (7 motivos)'),
        @('S', 'C', 'descriptive(motivo) — sin llamar al servicio', 'return'),
        @('S', 'FB', 'build(vacancy, checkpoint = día siguiente a closes_at)'), @('FB', 'DB', 'conteos y días hasta el checkpoint'),
        @('FB', 'S', '15 features enteras', 'return'), @('S', 'MC', 'predict(features)'),
        @('MC', 'S', 'descriptive(service_disabled)', 'return'),
        @('MC', 'API', 'POST /v1/predict + X-Internal-Token {15 features; sin IDs ni PII}'),
        @('API', 'API', 'token; PredictionRequest (extra=forbid, strict)'), @('API', 'M', 'predecir'),
        @('M', 'API', 'probabilidad', 'return'),
        @('API', 'MC', 'risk_score, risk_flag, threshold, model_version, freeze_fingerprint, status', 'return'),
        @('MC', 'MC', 'validar tipos, rango, coherencia de risk_flag, threshold y freeze congelados'),
        @('MC', 'S', 'unavailable(motivo)', 'return'), @('MC', 'S', 'predictive(...)', 'return'),
        @('C', 'UI', 'JSON (disponibilidad, %, señal, mensaje, is_experimental, measures: proceso, decision_is_human)', 'return'),
        @('UI', 'RH', 'tarjeta «Experimental»'))
    Fragments = @(
        @{ Type = 'alt'; Cond = 'fuera de alcance'; From = 7; To = 20; Lanes = @('C', 'M'); Pad = 3500; Nest = 0; Else = @(, @(8, 'elegible')) },
        @{ Type = 'alt'; Cond = 'ML_SERVICE_ENABLED = false'; From = 12; To = 20; Lanes = @('S', 'M'); Pad = 2500; Nest = 1; Else = @(, @(13, 'habilitado')) },
        @{ Type = 'alt'; Cond = 'timeout | conexión | 503 | 422 | 5xx | JSON inválido | contrato incompatible'; From = 19; To = 20; Lanes = @('S', 'MC'); Pad = 1500; Nest = 2; Else = @(, @(20, 'válida')) })
    Notes = @(
        @('Estima el PROCESO, no a las personas. Nada se persiste. Ningún mensaje hacia ranking, comparación ni decisión final. La respuesta no incluye incertidumbre.', 13, 20000),
        @('El mismo flujo lo ejecuta el Aprobador / Dirección (VacancyPolicy::viewOperationalRisk); la lifeline de actor es la de UC-01.', 1, 20000))
}

$only = @()
if ($env:PD_ONLY) { $only = $env:PD_ONLY -split ',' | ForEach-Object { $_.Trim() } }

Open-Pd
try {
    $m = $Pd.OpenModel($OomFile)
    foreach ($key in $seqs.Keys) {
        if ($only.Count -and ($only -notcontains $key)) { continue }
        $sp = $seqs[$key]
        if (-not $sp.Dividers) { $sp.Dividers = @() }
        $d = New-Sequence $m $sp.Name ($key.Replace('-', '_')) $sp
        Export-Diagram $d $sp.File
        "$key : mensajes=$($sp.Messages.Count) fragmentos=$($sp.Fragments.Count)"
    }
    Save-Model $m $OomFile
    "secuencias en el modelo=$(@($m.SequenceDiagrams).Count) mensajes totales=$(@($m.Messages).Count)"
    $m.Close()
} catch {
    "ERROR linea $($_.InvocationInfo.ScriptLineNumber): $($_.Exception.Message)"
    "  $($_.InvocationInfo.Line.Trim())"
    if ($m) { try { $m.Close() } catch {} }
} finally { Close-Pd }
