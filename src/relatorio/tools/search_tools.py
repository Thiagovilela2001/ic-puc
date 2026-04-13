"""
Ferramenta customizada para gerar consultas de busca otimizadas em português,
focadas em encontrar galpões industriais reutilizados como espaços culturais
no estado de São Paulo.

Esta ferramenta complementa o SerperDevTool/DuckDuckGo: em vez de fazer a
busca ela mesma, ela gera as queries mais eficazes para que o agente pesquisador
possa realizar buscas diversificadas e direcionadas.
"""

from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


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
