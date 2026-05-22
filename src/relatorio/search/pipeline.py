"""Pipeline de busca semantica usado antes da execucao da crew."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime
from pathlib import Path
from time import perf_counter

from relatorio.search.candidate_builder import CandidateBuilder
from relatorio.search.page_fetcher import PageFetcher
from relatorio.search.query_builder import SemanticQueryBuilder
from relatorio.search.result_filter import ResultFilter
from relatorio.search.search_client import SearchClient
from relatorio.search.semantic_parser import SemanticParser
from relatorio.search.types import RankedSearchHit, SearchRunReport


class SemanticSearchPipeline:
    """
    Orquestra interpretacao, geracao de queries, busca, deduplicacao e ranking.

    A saida desta camada e um texto rastreavel para o CrewAI trabalhar, alem de
    um JSON de auditoria opcional com queries, aceitos, rejeitados e erros.
    """

    def __init__(
        self,
        parser: SemanticParser | None = None,
        query_builder: SemanticQueryBuilder | None = None,
        search_client: SearchClient | None = None,
        result_filter: ResultFilter | None = None,
        page_fetcher: PageFetcher | None = None,
        candidate_builder: CandidateBuilder | None = None,
        cache_dir: Path | None = None,
    ) -> None:
        self.parser = parser or SemanticParser()
        self.query_builder = query_builder or SemanticQueryBuilder()
        self.search_client = search_client or SearchClient(cache_dir=cache_dir)
        self.result_filter = result_filter or ResultFilter()
        self.page_fetcher = page_fetcher or PageFetcher(cache_dir=cache_dir)
        self.candidate_builder = candidate_builder or CandidateBuilder()

    def run(
        self,
        municipios: list[str],
        seed_queries: list[str] | None = None,
        max_queries: int = 30,
        max_per_query: int = 5,
        max_pages: int = 40,
        audit_file: Path | None = None,
    ) -> SearchRunReport:
        started_at = datetime.now().isoformat(timespec="seconds")
        started = perf_counter()
        intent = self.parser.parse(municipios, seed_queries)
        queries = self.query_builder.build(intent, max_queries=max_queries)
        query_origins = self._query_origins(queries, intent.seed_queries)

        print(
            "\n[busca] Camada semantica gerou "
            f"{len(queries)} queries para {', '.join(intent.municipios)}."
        )

        hits, errors, search_stats = self.search_client.search_many(
            queries,
            max_per_query=max_per_query,
        )
        pre_accepted, pre_rejected = self.result_filter.filter_many(hits, strict=False)
        unique_hits_total = len(pre_accepted) + len(pre_rejected)

        print(
            "[busca] Pré-filtro semântico: "
            f"{len(pre_accepted)} candidatos para validação, {len(pre_rejected)} rejeitados."
        )

        to_fetch = pre_accepted[:max_pages]
        skipped_fetch = [
            replace(
                item,
                accepted=False,
                reasons=item.reasons + ("nao validado por limite de paginas",),
            )
            for item in pre_accepted[max_pages:]
        ]
        pages = self.page_fetcher.fetch_many(to_fetch)
        enriched = [
            self._attach_page(item, pages.get(item.hit.url))
            for item in to_fetch
        ]
        final_accepted, final_rejected = self.result_filter.reassess_with_pages(enriched)
        candidates = self.candidate_builder.build(final_accepted)

        print(
            "[busca] Filtro final: "
            f"{len(final_accepted)} evidências aceitas em {len(candidates)} candidato(s)."
        )

        finished_at = datetime.now().isoformat(timespec="seconds")
        report = SearchRunReport(
            intent=intent,
            queries=queries,
            query_origins=query_origins,
            accepted=final_accepted,
            rejected=final_rejected + skipped_fetch + pre_rejected,
            candidates=candidates,
            errors=errors,
            started_at=started_at,
            finished_at=finished_at,
            duration_seconds=round(perf_counter() - started, 3),
            raw_hits_total=search_stats.raw_hits_total,
            unique_hits_total=unique_hits_total,
            fetched_pages_total=len(pages),
            cache_hits_total=search_stats.cache_hits,
            search_source=search_stats.source,
        )

        if audit_file:
            report.save_json(audit_file)
            print(f"[busca] Auditoria salva em: {audit_file.absolute()}")

        return report

    def _query_origins(
        self,
        queries: list[str],
        seed_queries: tuple[str, ...],
    ) -> dict[str, str]:
        seeds = {" ".join(query.split()).lower() for query in seed_queries}
        return {
            query: "semente" if " ".join(query.split()).lower() in seeds else "gerada"
            for query in queries
        }

    def _attach_page(self, item: RankedSearchHit, page) -> RankedSearchHit:
        return replace(item, page=page)
