"""Geracao de queries a partir de uma intencao semantica."""

from __future__ import annotations

from relatorio.search.types import QueryIntent
from relatorio.search.vocabulary import FONTES_PRIORIZADAS, TERMOS_PATRIMONIO


class SemanticQueryBuilder:
    """Monta consultas web objetivas e deduplicadas."""

    def build(self, intent: QueryIntent, max_queries: int = 30) -> list[str]:
        queries: list[str] = []

        for query in intent.seed_queries:
            self._append_unique(queries, query, max_queries)

        for municipio in intent.municipios:
            location = self._format_location(municipio)
            self._build_transformation_queries(queries, intent, location, max_queries)
            self._build_patrimony_queries(queries, location, max_queries)
            self._build_source_queries(queries, location, max_queries)
            if len(queries) >= max_queries:
                break

        return queries[:max_queries]

    def _build_transformation_queries(
        self,
        queries: list[str],
        intent: QueryIntent,
        location: str,
        max_queries: int,
    ) -> None:
        exclusion = self._format_exclusions(intent.exclusoes)
        pairs = (
            ("fábrica", "espaço cultural"),
            ("fábrica", "centro cultural"),
            ("galpão", "espaço cultural"),
            ("armazém", "espaço cultural"),
            ("galpão", "ateliê coletivo"),
            ("galpão", "galeria de arte"),
            ("imóvel industrial", "hub criativo"),
        )
        verbs = ("virou", "se tornou", "foi convertido em", "se transformou em")

        for tipo, uso in pairs:
            for verbo in verbs:
                query = f'"{tipo}" "{verbo}" "{uso}" {location} {exclusion}'.strip()
                self._append_unique(queries, query, max_queries)
                if len(queries) >= max_queries:
                    return

    def _build_patrimony_queries(
        self,
        queries: list[str],
        location: str,
        max_queries: int,
    ) -> None:
        templates = (
            '"antiga fábrica" "espaço cultural" {location} -aluguel -venda',
            '"antigo armazém" "centro cultural" {location} -aluguel -venda',
            '"antigo galpão" "centro cultural" {location} -aluguel -venda',
            '"patrimônio industrial" reutilizado cultura {location}',
            '"reconversão industrial" "espaço cultural" {location}',
            '"requalificação urbana" galpão cultura {location}',
        )

        for template in templates:
            self._append_unique(
                queries,
                template.format(location=location),
                max_queries,
            )
            if len(queries) >= max_queries:
                return

        for termo in TERMOS_PATRIMONIO:
            query = f'"{termo}" cultura {location}'
            self._append_unique(queries, query, max_queries)
            if len(queries) >= max_queries:
                return

    def _build_source_queries(
        self,
        queries: list[str],
        location: str,
        max_queries: int,
    ) -> None:
        source_templates = (
            '{source} galpão "espaço cultural" {location}',
            '{source} "antiga fábrica" cultura {location}',
            '{source} armazém "centro cultural" {location}',
        )

        for source in FONTES_PRIORIZADAS:
            for template in source_templates:
                self._append_unique(
                    queries,
                    template.format(source=source, location=location),
                    max_queries,
                )
                if len(queries) >= max_queries:
                    return

    def _format_location(self, municipio: str) -> str:
        text = municipio.strip()
        lower = text.lower()
        if "estado de" in lower:
            return '"São Paulo"'
        if lower in {"sp", "são paulo", "sao paulo"}:
            return '"São Paulo"'
        if "são paulo" in lower or "sao paulo" in lower:
            return f'"{text}"'
        return f'"{text}" "São Paulo"'

    def _format_exclusions(self, exclusoes: tuple[str, ...]) -> str:
        return " ".join(f"-{term}" for term in exclusoes[:4])

    def _append_unique(self, queries: list[str], query: str, max_queries: int) -> None:
        if len(queries) >= max_queries:
            return
        normalized = " ".join(query.split()).lower()
        seen = {" ".join(existing.split()).lower() for existing in queries}
        if normalized not in seen:
            queries.append(" ".join(query.split()))
