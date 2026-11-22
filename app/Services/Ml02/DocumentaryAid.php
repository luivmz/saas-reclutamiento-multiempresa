<?php

namespace App\Services\Ml02;

use App\Models\EvaluationCriterion;
use App\Models\EvidenceItem;
use App\Services\Evidence\EvidenceLedger;

/**
 * EXPERIMENTAL ML-02 documentary aid over the CURRENT evidence versions of one application.
 *
 * - `byCriterion`: EI-09, BM25 retrieval with the criterion name as the query; returns at most k fragments with the
 *   words that matched, or abstains.
 * - `search`: EI-07, exact normalized search typed by the person.
 *
 * It ranks fragments for one query, never people: it does not score, compare, recommend nor discard anyone, and its
 * output goes nowhere but the screen of the person who asked (no ranking, no RF-23 decision, no ML-01 card).
 */
class DocumentaryAid
{
    public const K = 3;

    public function __construct(
        private readonly Bm25Retriever $retriever,
        private readonly LexicalSearch $search,
    ) {}

    /**
     * @return array{query_terms: list<string>, abstained: bool, hits: list<array{item: EvidenceItem, words: list<string>}>}
     */
    public function byCriterion(EvidenceLedger $ledger, EvaluationCriterion $criterion): array
    {
        $current = $ledger->currentItems()->keyBy('id');
        $documents = $current->map(fn (EvidenceItem $item) => $item->description)->all();

        $result = $this->retriever->retrieve($criterion->name, $documents, self::K);

        return [
            'query_terms' => $result['query_terms'],
            'abstained' => $result['abstained'],
            'hits' => array_map(fn (array $hit) => [
                'item' => $current[(int) $hit['id']],
                'words' => TextAnalyzer::matchingWords($current[(int) $hit['id']]->description, $hit['terms']),
            ], $result['hits']),
        ];
    }

    /**
     * @return list<EvidenceItem>
     */
    public function search(EvidenceLedger $ledger, string $query): array
    {
        $current = $ledger->currentItems()->keyBy('id');
        $documents = $current->map(fn (EvidenceItem $item) => $item->description)->all();

        return array_map(
            fn (string $id) => $current[(int) $id],
            $this->search->search($query, $documents, LexicalSearch::SUBSTRING),
        );
    }
}
