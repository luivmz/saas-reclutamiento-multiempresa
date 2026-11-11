<?php

namespace App\Services\Ml02;

/**
 * EXPERIMENTAL ML-02 documentary aid. Deterministic text analysis, fixed before any run (no training, no
 * learned weights, no external model):
 *
 *  1. remove the `[SINTÉTICO]` marker, lowercase and strip Spanish accents (á→a, ñ→n, ü→u);
 *  2. split on anything that is not a letter or a digit;
 *  3. drop a fixed list of Spanish function words;
 *  4. light suffix stripping: plural `-es` (5+ letters) or `-s` (4+ letters), then a final `a`, `e` or `o`
 *     (4+ letters). So «clase» and «clases» share `clas`, «planificaciones» becomes `planificacion`.
 */
class TextAnalyzer
{
    public const STOPWORDS = [
        'a', 'al', 'ante', 'con', 'como', 'de', 'del', 'e', 'el', 'en', 'entre', 'es', 'esa', 'ese', 'eso', 'esta',
        'estas', 'este', 'esto', 'estos', 'fue', 'la', 'las', 'le', 'les', 'lo', 'los', 'mas', 'muy', 'ni', 'no', 'o',
        'para', 'por', 'que', 'se', 'sin', 'sobre', 'son', 'su', 'sus', 'u', 'un', 'una', 'unas', 'uno', 'unos', 'y', 'ya',
    ];

    private const ACCENTS = ['á' => 'a', 'é' => 'e', 'í' => 'i', 'ó' => 'o', 'ú' => 'u', 'ü' => 'u', 'ñ' => 'n'];

    private const MARKER = '[sintético]';

    public static function normalize(string $text): string
    {
        $lower = mb_strtolower($text, 'UTF-8');

        return strtr(str_replace(self::MARKER, ' ', $lower), self::ACCENTS);
    }

    /**
     * Normalized words, without removing function words nor stemming (EI-07 exact search).
     *
     * @return list<string>
     */
    public static function words(string $text): array
    {
        $parts = preg_split('/[^a-z0-9]+/', self::normalize($text)) ?: [];

        return array_values(array_filter($parts, fn (string $w) => $w !== ''));
    }

    /**
     * Index terms for BM25 (EI-09): normalized words without function words, light-stemmed.
     *
     * @return list<string>
     */
    public static function terms(string $text): array
    {
        $terms = [];

        foreach (self::words($text) as $word) {
            if (in_array($word, self::STOPWORDS, true)) {
                continue;
            }

            $stem = self::stem($word);

            if (strlen($stem) >= 2) {
                $terms[] = $stem;
            }
        }

        return $terms;
    }

    public static function stem(string $word): string
    {
        if (strlen($word) >= 5 && str_ends_with($word, 'es')) {
            $word = substr($word, 0, -2);
        } elseif (strlen($word) >= 4 && str_ends_with($word, 's')) {
            $word = substr($word, 0, -1);
        }

        if (strlen($word) >= 4 && in_array(substr($word, -1), ['a', 'e', 'o'], true)) {
            $word = substr($word, 0, -1);
        }

        return $word;
    }

    /**
     * Surface words of $text whose index term is one of $terms, in order of appearance and without repeats.
     * Used to show the person why a fragment was retrieved.
     *
     * @param  list<string>  $terms
     * @return list<string>
     */
    public static function matchingWords(string $text, array $terms): array
    {
        $found = [];
        $clean = str_replace(['[SINTÉTICO]', '[sintético]'], ' ', $text);

        foreach (preg_split('/[^\p{L}\p{N}]+/u', $clean) ?: [] as $word) {
            if ($word === '' || in_array($word, $found, true)) {
                continue;
            }

            $normalized = self::normalize($word);
            if (in_array($normalized, self::STOPWORDS, true)) {
                continue;
            }

            if (in_array(self::stem($normalized), $terms, true)) {
                $found[] = $word;
            }
        }

        return $found;
    }
}
