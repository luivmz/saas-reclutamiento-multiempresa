import { StatusBadge } from '@/components/status-badge';
import type { EvidenceFragment } from '@/types';

export type TextPiece = { text: string; match: boolean };

function escapeRegExp(value: string): string {
    return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * Parte un texto en trozos y marca las palabras que explican por qué se
 * recuperó el fragmento. Solo marca palabras completas, tal como aparecen.
 */
export function splitByWords(text: string, words: string[]): TextPiece[] {
    const wanted = words.filter((word) => word.trim() !== '');

    if (wanted.length === 0) {
        return [{ text, match: false }];
    }

    const pattern = new RegExp(
        `(?<![\\p{L}\\p{N}])(${wanted.map(escapeRegExp).join('|')})(?![\\p{L}\\p{N}])`,
        'gu',
    );
    const pieces: TextPiece[] = [];
    let last = 0;

    for (const found of text.matchAll(pattern)) {
        const start = found.index ?? 0;

        if (start > last) {
            pieces.push({ text: text.slice(last, start), match: false });
        }

        pieces.push({ text: found[0], match: true });
        last = start + found[0].length;
    }

    if (last < text.length) {
        pieces.push({ text: text.slice(last), match: false });
    }

    return pieces;
}

/**
 * Un fragmento con su fuente: la evidencia, su versión, su tipo y de dónde
 * dice provenir. La ayuda documental nunca muestra un fragmento sin fuente.
 */
export function EvidenceFragmentCard({
    fragment,
    rank,
}: {
    fragment: EvidenceFragment;
    rank?: number;
}) {
    return (
        <article
            className="bg-card space-y-2 rounded-lg border p-3"
            data-cy="aid-fragment"
            aria-label={`Fragmento de ${fragment.code}`}
        >
            <header className="flex flex-wrap items-center gap-2 text-xs">
                {rank !== undefined && (
                    <span className="text-muted-foreground font-mono">
                        {rank}.
                    </span>
                )}
                <span className="font-mono font-medium">{fragment.code}</span>
                <span className="text-muted-foreground">
                    versión {fragment.version}
                </span>
                <StatusBadge status={fragment.type} />
            </header>
            <p className="text-sm leading-relaxed">
                {splitByWords(fragment.description, fragment.matched_words).map(
                    (piece, index) =>
                        piece.match ? (
                            <mark
                                key={index}
                                className="bg-tone-warning text-tone-warning-foreground rounded px-0.5"
                            >
                                {piece.text}
                            </mark>
                        ) : (
                            <span key={index}>{piece.text}</span>
                        ),
                )}
            </p>
            <p className="text-muted-foreground text-xs">
                Fuente declarada: {fragment.source.label}
                {fragment.matched_words.length > 0 && (
                    <>
                        {' · '}Coincide en: {fragment.matched_words.join(', ')}
                    </>
                )}
            </p>
        </article>
    );
}
