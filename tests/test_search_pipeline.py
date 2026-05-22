from __future__ import annotations

import unittest

from relatorio.search.page_fetcher import PageFetcher
from relatorio.search.pipeline import SemanticSearchPipeline
from relatorio.search.query_builder import SemanticQueryBuilder
from relatorio.search.result_filter import ResultFilter
from relatorio.search.semantic_parser import SemanticParser
from relatorio.search.types import PageEvidence, SearchHit, SearchStats


class FakeSearchClient:
    def __init__(self, hits: list[SearchHit]) -> None:
        self.hits = hits

    def search_many(self, queries: list[str], max_per_query: int = 5):
        return self.hits, [], SearchStats(
            source="fake",
            raw_hits_total=len(self.hits),
            cache_hits=0,
            duration_seconds=0.01,
        )


class FakePageFetcher:
    def fetch_many(self, ranked_hits):
        pages = {}
        for item in ranked_hits:
            pages[item.hit.url] = PageEvidence(
                url=item.hit.url,
                final_url=item.hit.url,
                status_code=200,
                ok=True,
                content_excerpt=(
                    "Antiga fábrica desativada virou centro cultural, "
                    "com ateliê coletivo e exposições."
                ),
                fetched_at="2026-05-22T10:00:00",
            )
        return pages


class SearchPipelineTests(unittest.TestCase):
    def test_query_builder_marks_seed_and_generated_queries(self) -> None:
        intent = SemanticParser().parse(
            ["Campinas"],
            ['"antiga fábrica" "espaço cultural" Campinas'],
        )
        queries = SemanticQueryBuilder().build(intent, max_queries=8)

        self.assertEqual(8, len(queries))
        self.assertEqual('"antiga fábrica" "espaço cultural" Campinas', queries[0])
        self.assertTrue(any('"Campinas" "São Paulo"' in query for query in queries[1:]))

    def test_result_filter_rejects_unvalidated_result_in_strict_mode(self) -> None:
        hit = SearchHit(
            query="q",
            title="Antiga fábrica virou espaço cultural",
            url="https://g1.globo.com/exemplo",
            snippet="Galpão desativado agora abriga centro cultural.",
            source="test",
        )

        ranked = ResultFilter().assess(hit, strict=True)

        self.assertFalse(ranked.accepted)
        self.assertIn("url nao validada antes da analise", ranked.reasons)

    def test_result_filter_rejects_real_estate_noise(self) -> None:
        hit = SearchHit(
            query="q",
            title="Galpão para alugar em Campinas",
            url="https://www.imovelweb.com.br/anuncio",
            snippet="Locação de galpão comercial com IPTU incluso.",
            source="test",
        )

        ranked = ResultFilter().assess(hit, strict=False)

        self.assertFalse(ranked.accepted)
        self.assertLess(ranked.score, 0)

    def test_page_fetcher_extracts_visible_text(self) -> None:
        html = """
        <html>
          <head><style>.x{display:none}</style><script>alert(1)</script></head>
          <body><h1>Galpão Cultural</h1><p>Antiga fábrica virou espaço cultural.</p></body>
        </html>
        """

        text = PageFetcher().extract_visible_text(html)

        self.assertIn("Galpão Cultural", text)
        self.assertIn("Antiga fábrica virou espaço cultural.", text)
        self.assertNotIn("alert", text)

    def test_pipeline_fetches_pages_and_builds_candidates(self) -> None:
        hits = [
            SearchHit(
                query='"antiga fábrica" "espaço cultural" Campinas',
                title="Galpão Cultural Campinas",
                url="https://g1.globo.com/galpao-cultural",
                snippet="Antiga fábrica agora recebe exposições.",
                source="fake",
            ),
            SearchHit(
                query="galpão Campinas",
                title="Galpão para alugar em Campinas",
                url="https://www.imovelweb.com.br/galpao",
                snippet="Aluguel de galpão comercial.",
                source="fake",
            ),
        ]

        report = SemanticSearchPipeline(
            search_client=FakeSearchClient(hits),
            page_fetcher=FakePageFetcher(),
        ).run(
            municipios=["Campinas"],
            seed_queries=['"antiga fábrica" "espaço cultural" Campinas'],
            max_queries=4,
        )

        self.assertEqual(1, len(report.accepted))
        self.assertEqual(1, len(report.candidates))
        self.assertEqual(2, report.raw_hits_total)
        self.assertEqual(1, report.fetched_pages_total)
        self.assertEqual("fake", report.search_source)


if __name__ == "__main__":
    unittest.main()
