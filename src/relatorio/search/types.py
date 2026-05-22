"""Tipos estruturados para a busca semantica."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class QueryIntent:
    """Representa a intencao de pesquisa antes da geracao das queries."""

    municipios: tuple[str, ...]
    seed_queries: tuple[str, ...] = ()
    tipos_imovel: tuple[str, ...] = ()
    usos_culturais: tuple[str, ...] = ()
    transformacoes: tuple[str, ...] = ()
    exclusoes: tuple[str, ...] = ()


@dataclass(frozen=True)
class SearchHit:
    """Resultado bruto retornado por um cliente de busca."""

    query: str
    title: str
    url: str
    snippet: str
    source: str


@dataclass(frozen=True)
class PageEvidence:
    """Conteudo real obtido de uma URL candidata."""

    url: str
    final_url: str
    status_code: int | None
    ok: bool
    content_excerpt: str = ""
    error: str = ""
    fetched_at: str = ""
    from_cache: bool = False


@dataclass(frozen=True)
class RankedSearchHit:
    """Resultado avaliado pela camada de filtros e ranking."""

    hit: SearchHit
    accepted: bool
    score: int
    reasons: tuple[str, ...]
    page: PageEvidence | None = None


@dataclass(frozen=True)
class SearchCandidate:
    """Candidato agrupado com uma ou mais evidencias."""

    name_hint: str
    score: int
    reasons: tuple[str, ...]
    evidences: tuple[RankedSearchHit, ...]


@dataclass(frozen=True)
class SearchStats:
    """Metrica agregada da etapa de busca."""

    source: str
    raw_hits_total: int
    cache_hits: int
    duration_seconds: float


@dataclass
class SearchRunReport:
    """Relatorio de uma execucao completa da busca semantica."""

    intent: QueryIntent
    queries: list[str]
    query_origins: dict[str, str]
    accepted: list[RankedSearchHit]
    rejected: list[RankedSearchHit]
    candidates: list[SearchCandidate] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    started_at: str = ""
    finished_at: str = ""
    duration_seconds: float = 0.0
    raw_hits_total: int = 0
    unique_hits_total: int = 0
    fetched_pages_total: int = 0
    cache_hits_total: int = 0
    search_source: str = ""

    def to_dict(self) -> dict:
        """Converte o relatorio em dicionario serializavel."""
        return asdict(self)

    def save_json(self, path: Path) -> None:
        """Grava auditoria da busca em JSON."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(self.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def format_for_crew(self) -> str:
        """
        Formata os resultados aceitos como texto compacto para o CrewAI.
        Inclui as queries e os motivos de ranking para preservar rastreabilidade.
        """
        lines: list[str] = [
            "RELATORIO DA BUSCA SEMANTICA",
            "",
            "Intencao interpretada:",
            f"- Municipios/escopo: {', '.join(self.intent.municipios)}",
            f"- Tipos de imovel: {', '.join(self.intent.tipos_imovel)}",
            f"- Usos culturais: {', '.join(self.intent.usos_culturais)}",
            "",
            "Queries executadas:",
        ]

        for i, query in enumerate(self.queries, 1):
            origin = self.query_origins.get(query, "desconhecida")
            lines.append(f"{i}. [{origin}] {query}")

        if self.errors:
            lines.extend(["", "Avisos da busca:"])
            lines.extend(f"- {error}" for error in self.errors)

        lines.extend(
            [
                "",
                "Resumo tecnico:",
                f"- Resultados brutos: {self.raw_hits_total}",
                f"- Resultados unicos: {self.unique_hits_total}",
                f"- Paginas verificadas: {self.fetched_pages_total}",
                f"- Fonte de busca: {self.search_source or 'nao informada'}",
                "",
                "Candidatos e evidencias aceitos para analise:",
            ]
        )

        if not self.candidates:
            lines.append("Nenhum resultado aceito pela camada semantica.")
            if self.rejected:
                lines.append("")
                lines.append("Resultados rejeitados mais informativos:")
                for item in self.rejected[:10]:
                    hit = item.hit
                    lines.append(f"- {hit.title} | {hit.url} | motivos: {', '.join(item.reasons)}")
            return "\n".join(lines)

        for i, candidate in enumerate(self.candidates, 1):
            lines.append(f"=== CANDIDATO {i} | score {candidate.score} ===")
            lines.append(f"Nome provável: {candidate.name_hint or 'N/A'}")
            lines.append(f"Motivos: {', '.join(candidate.reasons)}")
            for evidence_index, item in enumerate(candidate.evidences, 1):
                hit = item.hit
                lines.append(f"Evidência {evidence_index}:")
                lines.append(f"  Query  : {hit.query}")
                lines.append(f"  Origem : {self.query_origins.get(hit.query, 'desconhecida')}")
                lines.append(f"  Título : {hit.title or 'N/A'}")
                lines.append(f"  URL    : {hit.url or 'N/A'}")
                lines.append(f"  Trecho : {hit.snippet or 'N/A'}")
                if item.page:
                    lines.append(f"  URL final: {item.page.final_url or hit.url}")
                    lines.append(f"  Status   : {item.page.status_code or 'N/A'}")
                    lines.append(f"  Página   : {item.page.content_excerpt or 'sem texto extraído'}")
            lines.append("")

        return "\n".join(lines)
