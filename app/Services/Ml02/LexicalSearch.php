<?php

namespace App\Services\Ml02;

/**
 * EXPERIMENTAL ML-02 (EI-07, ALLOWED in the F36-SBX matrix once the gate allows it). Exact lexical search inside
 * one application, and the baseline the F38 protocol asks EI-09 to beat (§6.6).
 *
 *  - `token_normalizado`: every normalized word of the query is a word of the fragment (case and accents ignored).
 *  - `subcadena`: the normalized query appears inside the normalized fragment.
 *
 * Results are identifiers in natural order: there is no ranking.
 */
class LexicalSearch
{
    public const TOKEN = 'token_normalizado';

    public const SUBSTRING = 'subcadena';

    /**
     * @param  array<string, string>  $documents
     * @return list<string>
     */
    public function search(string $query, array $documents, string $mode = self::SUBSTRING): array
    {
        $hits = [];

        if ($mode === self::TOKEN) {
            $wanted = TextAnalyzer::words($query);
            foreach ($documents as $id => $text) {
                if ($wanted !== [] && array_diff($wanted, TextAnalyzer::words($text)) === []) {
                    $hits[] = (string) $id;
                }
            }
        } else {
            $needle = trim(preg_replace('/\s+/', ' ', TextAnalyzer::normalize($query)) ?? '');
            foreach ($documents as $id => $text) {
                $haystack = preg_replace('/\s+/', ' ', TextAnalyzer::normalize($text)) ?? '';
                if ($needle !== '' && str_contains($haystack, $needle)) {
                    $hits[] = (string) $id;
                }
            }
        }

        usort($hits, 'strnatcmp');

        return $hits;
    }

    /**
     * Baseline for EI-09: fragments that contain any content word of the criterion, unstemmed, in identifier order.
     *
     * @param  array<string, string>  $documents
     * @return list<string>
     */
    public function anyContentWord(string $criterion, array $documents, int $k = 3): array
    {
        $wanted = array_values(array_diff(TextAnalyzer::words($criterion), TextAnalyzer::STOPWORDS));
        $hits = [];

        foreach ($documents as $id => $text) {
            if (array_intersect($wanted, TextAnalyzer::words($text)) !== []) {
                $hits[] = (string) $id;
            }
        }

        usort($hits, 'strnatcmp');

        return array_slice($hits, 0, $k);
    }
}
