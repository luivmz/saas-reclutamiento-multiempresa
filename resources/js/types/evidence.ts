import type { Presented } from './recruitment';

/**
 * EXPERIMENTAL (rama local exp/evidencias-ml02): flujo de evidencias
 * ficticias y ayuda documental ML-02. No es la integración formal en el SaaS.
 */
export type EvidenceVersion = {
    id: number;
    code: string;
    version: number;
    type: Presented;
    source: Presented;
    state: Presented;
    description: string;
    author: { name: string; role: string } | null;
    created_at: string;
};

export type EvidenceRecord = EvidenceVersion & {
    record_code: string;
    links: { id: number; name: string }[];
    withdrawal_reason: string | null;
    versions: EvidenceVersion[];
    can: {
        link: boolean;
        review: boolean;
        correct: boolean;
        withdraw: boolean;
    };
};

export type EvidenceFragment = {
    id: number;
    code: string;
    version: number;
    type: Presented;
    source: Presented;
    state: Presented;
    description: string;
    matched_words: string[];
};

export type DocumentaryAidResult = {
    criterion: { id: number; name: string };
    method: string;
    k: number;
    query_terms: string[];
    abstained: boolean;
    results: EvidenceFragment[];
};

export type EvidenceSearchResult = {
    query: string;
    results: EvidenceFragment[];
};

export type RegistrableType = Presented & { source: Presented };

export type EvidenceHistoryEntry = {
    id: number;
    action: Presented;
    evidence: string;
    criterion: string | null;
    supersedes: string | null;
    actor: { name: string; role: string } | null;
    created_at: string;
};
