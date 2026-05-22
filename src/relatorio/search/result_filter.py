"""Filtro, deduplicacao e ranking dos resultados de busca."""

from __future__ import annotations

import unicodedata
from urllib.parse import urlsplit, urlunsplit

from relatorio.search.types import RankedSearchHit, SearchHit
from relatorio.search.vocabulary import (
    ADJETIVOS_DESATIVACAO,
    DOMINIOS_IMOBILIARIOS,
    FONTES_PRIORIZADAS,
    TERMOS_IMOBILIARIOS,
    TERMOS_PATRIMONIO,
    TIPOS_IMOVEL,
    USOS_CULTURAIS,
    VERBOS_TRANSFORMACAO,
)


class ResultFilter:
    """Remove ruido obvio e ranqueia candidatos por sinais semanticos."""

    def filter_many(
        self,
        hits: list[SearchHit],
        strict: bool = True,
    ) -> tuple[list[RankedSearchHit], list[RankedSearchHit]]:
        unique_hits = self._deduplicate(hits)
        ranked = [self.assess(hit, strict=strict) for hit in unique_hits]

        accepted = sorted(
            (item for item in ranked if item.accepted),
            key=lambda item: item.score,
            reverse=True,
        )
        rejected = sorted(
            (item for item in ranked if not item.accepted),
            key=lambda item: item.score,
            reverse=True,
        )
        return accepted, rejected

    def reassess_with_pages(
        self,
        ranked_hits: list[RankedSearchHit],
    ) -> tuple[list[RankedSearchHit], list[RankedSearchHit]]:
        assessed = [
            self.assess(item.hit, page=item.page, strict=True)
            for item in ranked_hits
        ]
        accepted = sorted(
            (item for item in assessed if item.accepted),
            key=lambda item: item.score,
            reverse=True,
        )
        rejected = sorted(
            (item for item in assessed if not item.accepted),
            key=lambda item: item.score,
            reverse=True,
        )
        return accepted, rejected

    def assess(
        self,
        hit: SearchHit,
        page=None,
        strict: bool = True,
    ) -> RankedSearchHit:
        page_text = page.content_excerpt if page else ""
        text = self._normalize(" ".join([hit.title, hit.url, hit.snippet, page_text]))
        reasons: list[str] = []

        blocked = self._find_matches(text, DOMINIOS_IMOBILIARIOS + TERMOS_IMOBILIARIOS)
        if blocked:
            return RankedSearchHit(
                hit=hit,
                accepted=False,
                score=-10,
                reasons=(f"possivel anuncio imobiliario: {blocked[0]}",),
                page=page,
            )

        score = 0
        cultural = self._find_matches(text, USOS_CULTURAIS)
        industrial = self._find_matches(text, TIPOS_IMOVEL)
        transformation = self._find_matches(text, VERBOS_TRANSFORMACAO)
        patrimony = self._find_matches(text, TERMOS_PATRIMONIO)
        deactivation = self._find_matches(text, ADJETIVOS_DESATIVACAO)
        trusted_source = self._find_trusted_source(hit.url)
        page_ok = bool(page and page.ok)

        if cultural:
            score += 3
            reasons.append(f"uso cultural: {cultural[0]}")
        if industrial:
            score += 2
            reasons.append(f"imovel industrial: {industrial[0]}")
        if transformation:
            score += 2
            reasons.append(f"transformacao: {transformation[0]}")
        if patrimony:
            score += 2
            reasons.append(f"patrimonio/reconversao: {patrimony[0]}")
        if deactivation:
            score += 1
            reasons.append(f"desativacao/antigo uso: {deactivation[0]}")
        if trusted_source:
            score += 1
            reasons.append(f"fonte priorizada: {trusted_source}")
        if page_ok:
            score += 2
            reasons.append("url validada e pagina acessivel")
        elif strict:
            reasons.append("url nao validada antes da analise")

        conversion = bool(transformation or patrimony or deactivation)
        if strict:
            accepted = bool(cultural and industrial and conversion and page_ok)
        else:
            accepted = bool(score >= 2 and (cultural or industrial or transformation or patrimony))

        if not accepted:
            reasons.append("sem sinais semanticos suficientes")

        return RankedSearchHit(
            hit=hit,
            accepted=accepted,
            score=score,
            reasons=tuple(reasons),
            page=page,
        )

    def _deduplicate(self, hits: list[SearchHit]) -> list[SearchHit]:
        by_url: dict[str, SearchHit] = {}
        for hit in hits:
            key = self._normalize_url(hit.url)
            if not key:
                continue
            existing = by_url.get(key)
            if existing is None:
                by_url[key] = hit
                continue
            if len(hit.snippet) > len(existing.snippet):
                by_url[key] = hit
        return list(by_url.values())

    def _normalize_url(self, url: str) -> str:
        try:
            parts = urlsplit(url.strip())
        except ValueError:
            return ""
        if not parts.scheme or not parts.netloc:
            return ""
        path = parts.path.rstrip("/")
        return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, "", ""))

    def _find_matches(self, normalized_text: str, terms: tuple[str, ...]) -> list[str]:
        return [
            term
            for term in terms
            if self._normalize(term) in normalized_text
        ]

    def _find_trusted_source(self, url: str) -> str:
        normalized_url = self._normalize(url)
        for source in FONTES_PRIORIZADAS:
            domain = source.removeprefix("site:")
            if self._normalize(domain) in normalized_url:
                return domain
        return ""

    def _normalize(self, text: str) -> str:
        text = unicodedata.normalize("NFKD", text.lower())
        return "".join(char for char in text if not unicodedata.combining(char))
