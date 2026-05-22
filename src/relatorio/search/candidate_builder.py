"""Agrupamento simples de resultados aceitos em candidatos com evidencias."""

from __future__ import annotations

import re
import unicodedata

from relatorio.search.types import RankedSearchHit, SearchCandidate


class CandidateBuilder:
    """Agrupa evidencias semelhantes sem tentar inferir dados nao confirmados."""

    def build(self, accepted: list[RankedSearchHit]) -> list[SearchCandidate]:
        groups: dict[str, list[RankedSearchHit]] = {}
        for item in accepted:
            key = self._candidate_key(item)
            groups.setdefault(key, []).append(item)

        candidates: list[SearchCandidate] = []
        for evidence in groups.values():
            evidence = sorted(evidence, key=lambda item: item.score, reverse=True)
            best = evidence[0]
            reasons = self._merge_reasons(evidence)
            candidates.append(
                SearchCandidate(
                    name_hint=best.hit.title,
                    score=max(item.score for item in evidence),
                    reasons=reasons,
                    evidences=tuple(evidence),
                )
            )

        return sorted(candidates, key=lambda item: item.score, reverse=True)

    def _candidate_key(self, item: RankedSearchHit) -> str:
        title = item.hit.title or item.hit.url
        title = re.sub(r"\s+[-|]\s+.*$", "", title)
        normalized = unicodedata.normalize("NFKD", title.lower())
        normalized = "".join(char for char in normalized if not unicodedata.combining(char))
        normalized = re.sub(r"[^a-z0-9]+", " ", normalized)
        return " ".join(normalized.split())[:80] or item.hit.url

    def _merge_reasons(self, evidence: list[RankedSearchHit]) -> tuple[str, ...]:
        merged: list[str] = []
        for item in evidence:
            for reason in item.reasons:
                if reason not in merged:
                    merged.append(reason)
        return tuple(merged)
