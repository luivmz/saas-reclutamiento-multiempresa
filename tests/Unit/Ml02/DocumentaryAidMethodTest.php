<?php

namespace Tests\Unit\Ml02;

use App\Services\Ml02\Bm25Retriever;
use App\Services\Ml02\LexicalSearch;
use App\Services\Ml02\TextAnalyzer;
use PHPUnit\Framework\TestCase;

/**
 * EXPERIMENTAL ML-02. The method that really runs: deterministic analysis, BM25 per application and exact search.
 */
class DocumentaryAidMethodTest extends TestCase
{
    public function test_analysis_removes_the_marker_accents_function_words_and_plurals(): void
    {
        $this->assertSame(['planificacion', 'ensenanz'], TextAnalyzer::terms('[SINTÉTICO] Planificación de la enseñanza'));
        $this->assertSame(TextAnalyzer::terms('clase'), TextAnalyzer::terms('CLASES'));
        $this->assertSame(['planificacion'], TextAnalyzer::terms('planificaciones'));
        $this->assertSame(['inicio', 'la', 'clase'], TextAnalyzer::words('Inició la CLASE'));
    }

    public function test_bm25_returns_only_fragments_that_share_terms_best_first(): void
    {
        $documents = [
            'FRG-1' => '[SINTÉTICO] Organizó la secuencia de actividades con metas por sesión.',
            'FRG-2' => '[SINTÉTICO] Elaboró la planificación anual y las unidades didácticas del área.',
            'FRG-3' => '[SINTÉTICO] Planificación de la clase y planificación del trimestre.',
        ];

        $result = (new Bm25Retriever)->retrieve('[SINTÉTICO] Planificación de la enseñanza', $documents);

        $this->assertFalse($result['abstained']);
        $this->assertSame(['FRG-3', 'FRG-2'], array_column($result['hits'], 'id'), 'dos apariciones pesan más; FRG-1 no comparte términos');
        $this->assertSame(['planificacion'], $result['hits'][0]['terms']);
    }

    public function test_bm25_abstains_without_shared_terms_and_is_deterministic(): void
    {
        $documents = ['B' => 'Curso de ofimática.', 'A' => 'Dos años como auxiliar administrativo.'];
        $retriever = new Bm25Retriever;

        $this->assertSame(['hits' => [], 'abstained' => true, 'query_terms' => ['atencion', 'famili']], $retriever->retrieve('Atención a familias', $documents));
        $this->assertSame($retriever->retrieve('auxiliar ofimática', $documents), $retriever->retrieve('auxiliar ofimática', $documents));
        $this->assertSame(['B', 'A'], array_column($retriever->retrieve('auxiliar ofimatica', $documents)['hits'], 'id'), 'un término cada uno: pesa más el texto más corto');

        $tie = ['B' => 'auxiliar de ofimática', 'A' => 'ofimática de auxiliar'];
        $this->assertSame(['A', 'B'], array_column($retriever->retrieve('auxiliar', $tie)['hits'], 'id'), 'empate exacto: orden por identificador');
    }

    public function test_k_limits_the_result(): void
    {
        $documents = array_combine(['D1', 'D2', 'D3', 'D4'], array_fill(0, 4, 'planificación'));

        $this->assertCount(3, (new Bm25Retriever)->retrieve('planificación', $documents)['hits']);
        $this->assertCount(1, (new Bm25Retriever)->retrieve('planificación', $documents, 1)['hits']);
    }

    public function test_exact_search_modes(): void
    {
        $documents = [
            'FRG-002' => '[SINTÉTICO] Elaboró la planificación anual.',
            'FRG-004' => '[SINTÉTICO] Inició la clase modelo presentando los objetivos.',
        ];
        $search = new LexicalSearch;

        $this->assertSame(['FRG-002'], $search->search('PLANIFICACIÓN', $documents, LexicalSearch::TOKEN));
        $this->assertSame([], $search->search('planifica', $documents, LexicalSearch::TOKEN), 'el modo de token no acepta prefijos');
        $this->assertSame(['FRG-004'], $search->search('clase  modelo', $documents, LexicalSearch::SUBSTRING));
        $this->assertSame([], $search->search('  ', $documents, LexicalSearch::SUBSTRING));
    }

    public function test_matching_words_explain_the_hit_in_the_original_spelling(): void
    {
        $this->assertSame(['planificación'], TextAnalyzer::matchingWords('[SINTÉTICO] Elaboró la planificación anual.', ['planificacion']));
        $this->assertSame(['clase', 'Clases'], TextAnalyzer::matchingWords('Una clase modelo. Clases de la tarde.', ['clas']));
    }
}
