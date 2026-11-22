<?php

namespace App\Services\Ml02;

/**
 * EXPERIMENTAL ML-02 (EI-09, CONDITIONAL in the F36-SBX matrix: F36-M02 pending). Okapi BM25 over the fragments of
 * ONE application, with the criterion text as the query.
 *
 * - Statistics (N, document frequency, average length) come only from that application's fragments, so the result
 *   for one application never depends on another candidate's documents.
 * - k1 = 1.2 and b = 0.75 (the usual defaults), idf = ln(1 + (N - n + 0.5) / (n + 0.5)), fixed before any run.
 * - Only fragments sharing at least one term with the query are returned, best first, ties by identifier.
 * - No shared term: it abstains. Abstaining says nothing about the person: only that the texts share no words.
 *
 * The scores rank fragments for one query and are never returned nor shown: they are not a measure of anyone.
 */
class Bm25Retriever
{
    public const K1 = 1.2;

    public const B = 0.75;

    public const METHOD_ID = 'EXP-BM25-LEXICO-v1';

    /**
     * @param  array<string, string>  $documents  identifier => text
     * @return array{hits: list<array{id: string, terms: list<string>}>, abstained: bool, query_terms: list<string>}
     */
    public function retrieve(string $query, array $documents, int $k = 3): array
    {
        $queryTerms = array_values(array_unique(TextAnalyzer::terms($query)));
        $analyzed = array_map(fn (string $text) => TextAnalyzer::terms($text), $documents);

        $n = count($analyzed);
        if ($n === 0 || $queryTerms === []) {
            return ['hits' => [], 'abstained' => true, 'query_terms' => $queryTerms];
        }

        $avgLength = max(1.0, array_sum(array_map('count', $analyzed)) / $n);
        $df = [];
        foreach ($queryTerms as $term) {
            $df[$term] = count(array_filter($analyzed, fn (array $terms) => in_array($term, $terms, true)));
        }

        $scored = [];
        foreach ($analyzed as $id => $terms) {
            $counts = array_count_values($terms);
            $score = 0.0;
            $matched = [];

            foreach ($queryTerms as $term) {
                $tf = $counts[$term] ?? 0;
                if ($tf === 0) {
                    continue;
                }

                $idf = log(1 + ($n - $df[$term] + 0.5) / ($df[$term] + 0.5));
                $norm = $tf + self::K1 * (1 - self::B + self::B * count($terms) / $avgLength);
                $score += $idf * ($tf * (self::K1 + 1)) / $norm;
                $matched[] = $term;
            }

            if ($matched !== []) {
                $scored[] = ['id' => (string) $id, 'score' => $score, 'terms' => $matched];
            }
        }

        usort($scored, fn (array $a, array $b) => abs($a['score'] - $b['score']) > 1e-12
            ? $b['score'] <=> $a['score']
            : strnatcmp($a['id'], $b['id']));

        $hits = array_map(fn (array $row) => ['id' => $row['id'], 'terms' => $row['terms']], array_slice($scored, 0, $k));

        return ['hits' => $hits, 'abstained' => $hits === [], 'query_terms' => $queryTerms];
    }
}
