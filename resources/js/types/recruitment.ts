export type Tone =
    | 'neutral'
    | 'info'
    | 'primary'
    | 'success'
    | 'warning'
    | 'danger';

export type Presented<V extends string = string> = {
    value: V;
    label: string;
    tone: Tone;
};

export type PaginationLink = {
    url: string | null;
    label: string;
    active: boolean;
};

export type Paginated<T> = {
    data: T[];
    meta: {
        current_page: number;
        from: number | null;
        last_page: number;
        links: PaginationLink[];
        per_page: number;
        to: number | null;
        total: number;
    };
};

export type JobRequest = {
    id: number;
    code: string;
    position_title: string;
    area: string;
    headcount: number;
    contract_type: Presented;
    justification: string;
    required_by: string | null;
    status: Presented;
    observation: string | null;
    decision_comment: string | null;
    submitted_at: string | null;
    validated_at: string | null;
    decided_at: string | null;
    created_at: string;
    requester?: { id: number; name: string };
    vacancy?: { id: number; code: string; status: Presented } | null;
};

export type StatusHistoryEntry = {
    id: number;
    from: Presented | null;
    to: Presented;
    author: string;
    comment: string | null;
    created_at: string;
};

export type Criterion = {
    id: number;
    name: string;
    stage: Presented;
    weight: number;
    min_score: number;
    max_score: number;
};

export type JobProfile = {
    education: string;
    experience: string;
    functions: string;
    competencies: string;
};

export type CandidateProfileData = {
    phone: string | null;
    city: string | null;
    education_level: Presented | null;
    professional_title: string | null;
    years_of_experience: number | null;
    summary: string | null;
};

export type DocumentSummary = {
    id: number;
    original_name: string;
    size_bytes: number;
    uploaded_at: string;
    download_url: string;
};

export type JobApplication = {
    id: number;
    code: string;
    status: Presented;
    applied_at: string;
    stage_changed_at: string | null;
    vacancy?: {
        id: number;
        code: string;
        title: string;
        status: Presented;
        organization: string | null;
    };
    candidate?: {
        id: number;
        name: string;
        email: string;
        profile: CandidateProfileData | null;
    };
    cv?: DocumentSummary | null;
};

export type AssessmentAssignment = {
    key: string;
    id: number;
    kind: Presented;
    title: string;
    candidate: string;
    vacancy: string;
    scheduled_at: string;
    modality: string;
    location: string;
    status: Presented;
    url: string;
};

export type AssessmentSummary = {
    id: number;
    kind: Presented;
    title: string;
    status: Presented;
    scheduled_at: string;
    duration_minutes: number | null;
    modality: Presented;
    location: string;
    instructions: string | null;
    observations: string | null;
    outcome: Presented | null;
    completed_at: string | null;
    evaluator?: string;
    results?: { criterion: string; score: number; max_score: number; comment: string | null }[];
};

export type AppNotification = {
    id: string;
    kind: string | null;
    title: string;
    message: string;
    url: string | null;
    read_at: string | null;
    created_at: string;
};

export type Vacancy = {
    id: number;
    code: string;
    title: string;
    summary: string;
    location: string;
    contract_type: Presented;
    positions: number;
    opens_at: string | null;
    closes_at: string | null;
    /** GAP-01: plazo objetivo de cierre del proceso. */
    target_completion_at: string | null;
    status: Presented;
    published_at: string | null;
    closed_at: string | null;
    closure_type: Presented | null;
    closure_notes: string | null;
    accepts_applications: boolean;
    organization?: { id: number; name: string };
    job_request?: {
        id: number;
        code: string;
        area: string;
        headcount: number;
    };
    profile?: JobProfile | null;
    criteria?: Criterion[];
    applications_count?: number;
};
