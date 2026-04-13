"""
Modelos Pydantic para representar e validar a saída estruturada do sistema
de identificação de galpões reutilizados para iniciativas culturais em São Paulo.
"""

from typing import List, Literal

from pydantic import BaseModel, Field, model_validator


class EspacoCultural(BaseModel):
    """
    Representa um espaço cultural identificado em um imóvel industrial reutilizado.
    Campos marcados como Optional podem ser preenchidos com "não informado".
    """

    nome: str = Field(
        description="Nome oficial do espaço cultural"
    )
    endereco: str = Field(
        default="não informado",
        description="Endereço completo incluindo logradouro, número e bairro",
    )
    municipio: str = Field(
        description="Município no estado de São Paulo onde o espaço está localizado"
    )
    antigo_uso: str = Field(
        description=(
            "Descrição do uso original do imóvel antes da conversão cultural "
            "(ex: fábrica têxtil, armazém de grãos, depósito logístico)"
        )
    )
    uso_atual_cultural: str = Field(
        description=(
            "Tipo de uso cultural atual do espaço "
            "(ex: centro cultural, galeria, ateliê coletivo, hub criativo)"
        )
    )
    ano_reutilizacao: str = Field(
        default="não informado",
        description="Ano aproximado em que o imóvel foi convertido para uso cultural",
    )
    fonte: str = Field(
        description="URL completa ou nome da fonte de informação consultada"
    )
    relevancia: Literal["relevante", "parcialmente relevante", "não relevante"] = Field(
        description=(
            "Classificação de relevância: "
            "'relevante', 'parcialmente relevante' ou 'não relevante'"
        )
    )
    justificativa: str = Field(
        description=(
            "Justificativa resumida da classificação — "
            "1 a 2 frases objetivas sobre a evidência de reconversão"
        )
    )


class RelatorioGalpoesCulturais(BaseModel):
    """
    Relatório consolidado de galpões reutilizados para cultura no estado de São Paulo.
    Este é o schema raiz do arquivo JSON de saída.
    """

    espacos_culturais: List[EspacoCultural] = Field(
        description="Lista de espaços culturais identificados e validados"
    )
    total: int = Field(
        description=(
            "Total de espaços incluídos no relatório "
            "(relevantes + parcialmente relevantes)"
        )
    )

    @model_validator(mode="after")
    def total_deve_bater_com_lista(self) -> "RelatorioGalpoesCulturais":
        esperado = len(self.espacos_culturais)
        if self.total != esperado:
            raise ValueError(
                f"'total' ({self.total}) não corresponde ao número de espaços "
                f"em 'espacos_culturais' ({esperado})."
            )
        return self
    municipios_pesquisados: List[str] = Field(
        description="Lista de municípios do estado de São Paulo incluídos na pesquisa"
    )
    data_coleta: str = Field(
        description="Data em que a coleta de dados foi realizada (formato YYYY-MM-DD)"
    )
