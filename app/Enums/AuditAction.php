<?php

namespace App\Enums;

use App\Enums\Concerns\HasPresentation;

enum AuditAction: string
{
    use HasPresentation;

    case UserRegistered = 'usuario.registrado';
    case CandidateProfileUpdated = 'postulante.perfil_actualizado';
    case CandidateCvUploaded = 'postulante.cv_cargado';

    case JobRequestCreated = 'requerimiento.registrado';
    case JobRequestUpdated = 'requerimiento.corregido';
    case JobRequestSubmitted = 'requerimiento.enviado';
    case JobRequestObserved = 'requerimiento.observado';
    case JobRequestValidated = 'requerimiento.validado';
    case JobRequestApproved = 'requerimiento.aprobado';
    case JobRequestRejected = 'requerimiento.rechazado';

    case VacancyCreated = 'vacante.registrada';
    case VacancyUpdated = 'vacante.configurada';
    case VacancyPublished = 'vacante.publicada';
    case VacancyClosed = 'vacante.cerrada';

    case ApplicationSubmitted = 'postulacion.registrada';
    case ApplicationStageChanged = 'postulacion.etapa_cambiada';

    case EvaluationScheduled = 'evaluacion.programada';
    case EvaluationResultRecorded = 'evaluacion.resultado_registrado';
    case InterviewScheduled = 'entrevista.programada';
    case InterviewResultRecorded = 'entrevista.resultado_registrado';

    case SelectionDecisionRecorded = 'seleccion.decision_registrada';
    case CandidateSelected = 'seleccion.candidato_registrado';
    case ProcessResultNotified = 'proceso.resultado_notificado';

    // EXPERIMENTAL (exp/evidencias-ml02, F37 flow). Metadata carry identifiers only, never the text (R-07).
    case EvidenceRegistered = 'evidencia.registrada';
    case EvidenceLinked = 'evidencia.enlazada';
    case EvidenceUnlinked = 'evidencia.enlace_retirado';
    case EvidenceReviewed = 'evidencia.revisada';
    case EvidenceCorrected = 'evidencia.corregida';
    case EvidenceWithdrawn = 'evidencia.retirada';

    public function label(): string
    {
        return match ($this) {
            self::UserRegistered => 'Cuenta registrada',
            self::CandidateProfileUpdated => 'Perfil de postulante actualizado',
            self::CandidateCvUploaded => 'CV cargado',
            self::JobRequestCreated => 'Requerimiento registrado',
            self::JobRequestUpdated => 'Requerimiento corregido',
            self::JobRequestSubmitted => 'Requerimiento enviado a validación',
            self::JobRequestObserved => 'Requerimiento observado',
            self::JobRequestValidated => 'Requerimiento validado',
            self::JobRequestApproved => 'Requerimiento aprobado',
            self::JobRequestRejected => 'Requerimiento rechazado',
            self::VacancyCreated => 'Vacante registrada',
            self::VacancyUpdated => 'Vacante configurada',
            self::VacancyPublished => 'Vacante publicada',
            self::VacancyClosed => 'Vacante cerrada',
            self::ApplicationSubmitted => 'Postulación registrada',
            self::ApplicationStageChanged => 'Cambio de etapa de postulación',
            self::EvaluationScheduled => 'Evaluación programada',
            self::EvaluationResultRecorded => 'Resultado de evaluación registrado',
            self::InterviewScheduled => 'Entrevista programada',
            self::InterviewResultRecorded => 'Resultado de entrevista registrado',
            self::SelectionDecisionRecorded => 'Decisión final registrada',
            self::CandidateSelected => 'Selección de candidato registrada',
            self::ProcessResultNotified => 'Resultado final notificado a postulantes',
            self::EvidenceRegistered => 'Evidencia registrada (experimental)',
            self::EvidenceLinked => 'Evidencia enlazada a un criterio (experimental)',
            self::EvidenceUnlinked => 'Enlace de evidencia retirado (experimental)',
            self::EvidenceReviewed => 'Evidencia revisada (experimental)',
            self::EvidenceCorrected => 'Evidencia corregida con una versión nueva (experimental)',
            self::EvidenceWithdrawn => 'Evidencia retirada (experimental)',
        };
    }

    public function tone(): string
    {
        return match ($this) {
            self::JobRequestRejected, self::JobRequestObserved => 'danger',
            self::JobRequestApproved, self::VacancyPublished, self::CandidateSelected => 'success',
            self::SelectionDecisionRecorded, self::VacancyClosed => 'warning',
            default => 'neutral',
        };
    }
}
