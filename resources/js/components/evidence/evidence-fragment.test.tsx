import { renderToStaticMarkup } from 'react-dom/server';
import { describe, expect, test } from 'vitest';
import {
    EvidenceFragmentCard,
    splitByWords,
} from '@/components/evidence/evidence-fragment';
import type { EvidenceFragment } from '@/types';

/**
 * Ayuda documental ML-02 (experimental): cada fragmento se muestra con su
 * fuente y con las palabras que explican por qué se recuperó.
 */
const fragment: EvidenceFragment = {
    id: 7,
    code: 'EVD-00007',
    version: 2,
    type: { value: 'cv', label: 'CV presentado', tone: 'neutral' },
    source: {
        value: 'documento_presentado',
        label: 'Documento presentado',
        tone: 'neutral',
    },
    state: { value: 'registrada', label: 'Registrada', tone: 'info' },
    description:
        '[SINTÉTICO] Elaboró la planificación anual y las unidades didácticas.',
    matched_words: ['planificación'],
};

describe('splitByWords', () => {
    test('marca solo palabras completas, tal como aparecen', () => {
        expect(splitByWords('clase y subclase, Clase.', ['clase'])).toEqual([
            { text: 'clase', match: true },
            { text: ' y subclase, Clase.', match: false },
        ]);
    });

    test('sin palabras devuelve el texto entero sin marcar', () => {
        expect(splitByWords('texto', [])).toEqual([
            { text: 'texto', match: false },
        ]);
    });

    test('no interpreta caracteres especiales como expresión regular', () => {
        expect(splitByWords('a.b ab', ['a.b'])).toEqual([
            { text: 'a.b', match: true },
            { text: ' ab', match: false },
        ]);
    });
});

describe('EvidenceFragmentCard', () => {
    test('muestra la fuente, la versión y la coincidencia resaltada', () => {
        const html = renderToStaticMarkup(
            <EvidenceFragmentCard fragment={fragment} rank={1} />,
        );

        expect(html).toContain('EVD-00007');
        expect(html).toContain('versión 2');
        expect(html).toContain('Fuente declarada: Documento presentado');
        expect(html).toContain('<mark');
        expect(html).toMatch(/<mark[^>]*>planificación<\/mark>/);
        expect(html).toContain('Coincide en: planificación');
    });

    test('sin coincidencias no resalta nada ni inventa una explicación', () => {
        const html = renderToStaticMarkup(
            <EvidenceFragmentCard
                fragment={{ ...fragment, matched_words: [] }}
            />,
        );

        expect(html).not.toContain('<mark');
        expect(html).not.toContain('Coincide en');
    });

    test('enlaza a la tarjeta de la evidencia de la que sale el fragmento', () => {
        const html = renderToStaticMarkup(
            <EvidenceFragmentCard fragment={fragment} rank={1} />,
        );

        expect(html).toMatch(
            /<a href="#evidence-7"[^>]*data-cy="aid-open-source"[^>]*>.*Abrir la evidencia EVD-00007<\/a>/,
        );
    });

    test('nunca muestra un puntaje', () => {
        const html = renderToStaticMarkup(
            <EvidenceFragmentCard fragment={fragment} rank={1} />,
        );

        expect(html.toLowerCase()).not.toMatch(/puntaje|score|%/);
    });
});
