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
