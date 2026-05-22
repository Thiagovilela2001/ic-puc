"""Camada de busca semantica para descoberta de galpoes culturais."""

from relatorio.search.pipeline import SemanticSearchPipeline
from relatorio.search.types import (
    PageEvidence,
    QueryIntent,
    RankedSearchHit,
    SearchCandidate,
    SearchHit,
    SearchRunReport,
    SearchStats,
)

__all__ = [
    "PageEvidence",
    "QueryIntent",
    "RankedSearchHit",
    "SearchCandidate",
    "SearchHit",
    "SearchRunReport",
    "SearchStats",
    "SemanticSearchPipeline",
]
