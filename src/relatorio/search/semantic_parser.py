"""Interpretacao deterministica da intencao de busca."""

from __future__ import annotations

from relatorio.search.types import QueryIntent
from relatorio.search.vocabulary import (
    TERMOS_EXCLUSAO,
    TIPOS_IMOVEL,
    USOS_CULTURAIS,
    VERBOS_TRANSFORMACAO,
)


class SemanticParser:
    """
    Converte os parametros do usuario em um QueryIntent estruturado.

    Esta versao evita depender do LLM para interpretar o escopo inicial. O agente
    ainda pode avaliar os resultados depois, mas a coleta parte de campos
    controlados.
    """

    def parse(
        self,
        municipios: list[str] | tuple[str, ...],
        seed_queries: list[str] | tuple[str, ...] | None = None,
    ) -> QueryIntent:
        cleaned_municipios = tuple(
            municipio.strip()
            for municipio in municipios
            if municipio and municipio.strip()
        ) or ("estado de São Paulo",)

        cleaned_seeds = tuple(
            query.strip()
            for query in (seed_queries or ())
            if query and query.strip()
        )

        return QueryIntent(
            municipios=cleaned_municipios,
            seed_queries=cleaned_seeds,
            tipos_imovel=TIPOS_IMOVEL,
            usos_culturais=USOS_CULTURAIS,
            transformacoes=VERBOS_TRANSFORMACAO,
            exclusoes=TERMOS_EXCLUSAO,
        )
