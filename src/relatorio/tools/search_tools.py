"""
Ferramentas customizadas para busca e geração de consultas otimizadas em português,
focadas em encontrar galpões industriais reutilizados como espaços culturais
no estado de São Paulo.

DuckDuckGoDirectTool  — busca web via DDGS (sem wrapper LangChain), com retry
GerarConsultasBuscaTool — gera queries otimizadas para o agente pesquisador
"""

import time

from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# DuckDuckGo direto via DDGS (sem wrapper LangChain) com retry
# ---------------------------------------------------------------------------

class DDGInput(BaseModel):
    """Parâmetros de entrada para a busca DuckDuckGo."""

    query: str = Field(description="Consulta de busca em português")


class DuckDuckGoDirectTool(BaseTool):
    """
    Busca na web via DuckDuckGo usando DDGS diretamente (sem wrapper LangChain).
    Retorna até 10 resultados com título, URL e trecho de texto.
    Usa retry automático (até 3 tentativas) para contornar rate limiting.
    """

    name: str = "DuckDuckGo Web Search"
    description: str = (
        "Realiza uma busca na web via DuckDuckGo. "
        "Retorna os 10 primeiros resultados com título, URL e trecho. "
        "Use para encontrar páginas sobre galpões culturais, espaços de arte "
        "e imóveis industriais reutilizados no estado de São Paulo."
    )
    args_schema: Type[BaseModel] = DDGInput

    def _run(self, query: str) -> str:
        try:
            from duckduckgo_search import DDGS
        except ImportError:
            return "Erro: pacote duckduckgo-search não instalado."

        last_error: str = ""
        for attempt in range(3):
            try:
                with DDGS() as ddg:
                    results = list(ddg.text(query, max_results=10))
                if not results:
                    return f"Nenhum resultado encontrado para: {query}"
                lines: list[str] = []
                for r in results:
                    lines.append(f"Título : {r.get('title', 'N/A')}")
                    lines.append(f"URL    : {r.get('href', 'N/A')}")
                    lines.append(f"Trecho : {r.get('body', 'N/A')}")
                    lines.append("")
                return "\n".join(lines)
            except Exception as exc:
                last_error = str(exc)
                if attempt < 2:
                    time.sleep(2 ** attempt)  # 1s, 2s entre tentativas
        return f"Erro na busca DuckDuckGo após 3 tentativas: {last_error}"


# ---------------------------------------------------------------------------
# Vocabulário controlado para geração de queries
# ---------------------------------------------------------------------------

TIPOS_IMOVEL = [
    "galpão",
    "fábrica",
    "armazém",
    "depósito",
    "usina",
    "indústria",
    "hangar",
    "barracão",
]

ADJETIVOS_DESATIVACAO = [
    "desativado",
    "abandonado",
    "desocupado",
    "fechado",
    "desativada",
    "abandonada",
]

USOS_CULTURAIS = [
    "centro cultural",
    "espaço cultural",
    "ateliê coletivo",
    "galeria de arte",
    "hub criativo",
    "casa de shows",
    "fábrica de cultura",
    "espaço de exposições",
    "ocupação artística",
    "economia criativa",
]

VERBOS_TRANSFORMACAO = [
    "virou",
    "tornou-se",
    "se transformou em",
    "foi convertido em",
    "recebeu",
    "abriga",
]

FONTES_PRIORIZADAS = [
    "site:folha.uol.com.br",
    "site:estadao.com.br",
    "site:g1.globo.com",
    "site:agenciabrasil.ebc.com.br",
    "site:cultura.sp.gov.br",
    "site:sescsp.org.br",
]


# ---------------------------------------------------------------------------
# Schema de entrada
# ---------------------------------------------------------------------------

class GerarConsultasInput(BaseModel):
    """Parâmetros de entrada para o gerador de consultas."""

    municipio: str = Field(
        default="São Paulo",
        description=(
            "Município do estado de São Paulo para direcionar as buscas. "
            "Use 'São Paulo' para a capital ou o nome de outro município paulista."
        ),
    )
    max_consultas: int = Field(
        default=12,
        ge=3,
        le=30,
        description="Número máximo de consultas a gerar (mínimo 3, máximo 30).",
    )
    incluir_filtros_fonte: bool = Field(
        default=False,
        description=(
            "Se True, adiciona filtros site: às queries para priorizar "
            "fontes jornalísticas e institucionais confiáveis."
        ),
    )


# ---------------------------------------------------------------------------
# Ferramenta
# ---------------------------------------------------------------------------

class GerarConsultasBuscaTool(BaseTool):
    """
    Gera uma lista de consultas de busca em português otimizadas para
    identificar galpões industriais e armazéns reutilizados como espaços
    culturais em um município específico do estado de São Paulo.

    Use esta ferramenta no início da pesquisa para obter um conjunto
    diversificado de queries antes de executar as buscas reais.
    """

    name: str = "Gerador de Consultas para Galpões Culturais"
    description: str = (
        "Gera uma lista de consultas de busca em português direcionadas a encontrar "
        "galpões industriais, armazéns e fábricas desativadas que foram reutilizados "
        "como espaços culturais em um município do estado de São Paulo. "
        "Fornece ao menos 8 combinações distintas de termos de busca. "
        "Use esta ferramenta antes de iniciar as buscas para ter queries mais efetivas."
    )
    args_schema: Type[BaseModel] = GerarConsultasInput

    def _run(
        self,
        municipio: str = "São Paulo",
        max_consultas: int = 12,
        incluir_filtros_fonte: bool = False,
    ) -> str:
        consultas: list[str] = []

        # Grupo 1 — tipo + desativação + uso cultural + município
        for tipo in TIPOS_IMOVEL[:4]:
            for uso in USOS_CULTURAIS[:3]:
                q = f'"{tipo}" {ADJETIVOS_DESATIVACAO[0]} "{uso}" {municipio}'
                consultas.append(q)
                if len(consultas) >= max_consultas:
                    break
            if len(consultas) >= max_consultas:
                break

        # Grupo 2 — "antiga X virou Y" + município
        if len(consultas) < max_consultas:
            for tipo in TIPOS_IMOVEL[:3]:
                for verbo in VERBOS_TRANSFORMACAO[:2]:
                    for uso in USOS_CULTURAIS[:2]:
                        q = f"antiga {tipo} {verbo} {uso} {municipio} São Paulo"
                        consultas.append(q)
                        if len(consultas) >= max_consultas:
                            break
                    if len(consultas) >= max_consultas:
                        break
                if len(consultas) >= max_consultas:
                    break

        # Grupo 3 — reconversão + município
        if len(consultas) < max_consultas:
            extras = [
                f"reconversão industrial cultura {municipio} São Paulo",
                f"patrimônio industrial reutilizado cultura {municipio}",
                f"imóvel industrial espaço cultural {municipio} SP",
                f"requalificação urbana cultura {municipio} São Paulo",
            ]
            for q in extras:
                consultas.append(q)
                if len(consultas) >= max_consultas:
                    break

        # Limita ao máximo solicitado
        consultas = consultas[:max_consultas]

        # Adiciona filtros de fonte se solicitado
        if incluir_filtros_fonte and consultas:
            filtro = " OR ".join(FONTES_PRIORIZADAS[:3])
            consultas_filtradas = [f"{q} ({filtro})" for q in consultas[:4]]
            consultas = consultas_filtradas + consultas[4:]

        # Formata saída
        linhas = [f"{i + 1}. {q}" for i, q in enumerate(consultas)]
        resultado = (
            f"Consultas de busca geradas para '{municipio}', estado de São Paulo:\n\n"
            + "\n".join(linhas)
            + f"\n\nTotal: {len(consultas)} consultas prontas para uso.\n"
            "Execute cada uma delas com a ferramenta de busca web (SerperDevTool "
            "ou DuckDuckGo) e colete os resultados mais relevantes."
        )
        return resultado
