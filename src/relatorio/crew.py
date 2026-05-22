"""
Crew principal do sistema de identificação de galpões reutilizados para
iniciativas culturais no estado de São Paulo.

Fluxo de execução (Process.sequential):
  1. pesquisador  → pesquisa_task    : analisa candidatos coletados previamente
  2. analista     → analise_task     : classifica cada candidato
  3. estruturador → estruturacao_task: gera JSON consolidado final

Busca web:
  - A coleta de links ocorre antes da crew, em relatorio.search.SemanticSearchPipeline.
  - O pesquisador recebe resultados ja filtrados e pode usar scraping para aprofundar URLs.
  - Busca aberta pelo agente so e habilitada se CREWAI_ENABLE_AGENT_SEARCH=1.
"""

import os
from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from relatorio.models import RelatorioGalpoesCulturais
from relatorio.tools.search_tools import DuckDuckGoDirectTool, GerarConsultasBuscaTool


# ---------------------------------------------------------------------------
# Helpers de ferramentas — carregamento condicional para evitar crash
# ---------------------------------------------------------------------------

def _load_serper() -> list:
    """
    Carrega SerperDevTool configurada para busca em português no Brasil.
    n_results=10 garante mais resultados por query (padrão é 10, máximo 100).
    """
    if not os.getenv("SERPER_API_KEY"):
        return []
    try:
        from crewai_tools import SerperDevTool
        tool = SerperDevTool(
            country="br",
            locale="pt-br",
            n_results=10,
        )
        print("  [tools] SerperDevTool carregada (Brasil/pt-br, 10 resultados/busca)")
        return [tool]
    except Exception as exc:
        print(f"  [tools] Falha ao carregar SerperDevTool: {exc}")
        return []


def _load_duckduckgo() -> list:
    """Carrega DuckDuckGoDirectTool (DDGS direto, com retry) como fallback gratuito."""
    try:
        import duckduckgo_search  # noqa: F401 — verifica se está instalado
        tool = DuckDuckGoDirectTool()
        print("  [tools] DuckDuckGoDirectTool carregada (DDGS direto, com retry)")
        return [tool]
    except ImportError:
        print("  [tools] duckduckgo-search indisponível — instale duckduckgo-search")
        return []


def _load_scraper() -> list:
    """Carrega ScrapeWebsiteTool para aprofundar em URLs encontradas."""
    try:
        from crewai_tools import ScrapeWebsiteTool
        return [ScrapeWebsiteTool()]
    except Exception:
        return []


# ---------------------------------------------------------------------------
# Crew
# ---------------------------------------------------------------------------

@CrewBase
class GalpoesCulturais:
    """
    Crew de identificação de galpões reutilizados para cultura em São Paulo.

    Inputs esperados pelo kickoff (definidos em main.py):
      municipios         : str — municípios separados por vírgula
      palavras_chave     : str — queries executadas, uma por linha
      limite_resultados  : str — número máximo de candidatos
      data_coleta        : str — data no formato YYYY-MM-DD
      resultados_busca   : str — links coletados pela camada semântica
    """

    agents: List[BaseAgent]
    tasks: List[Task]

    # ------------------------------------------------------------------
    # Montagem do conjunto de ferramentas para o Pesquisador
    # ------------------------------------------------------------------

    def _search_tools(self) -> list:
        """
        Retorna ferramentas de apoio para o Pesquisador.

        Por padrao a busca web aberta fica fora do agente e acontece em
        SemanticSearchPipeline. Para depuracao, defina CREWAI_ENABLE_AGENT_SEARCH=1
        e a crew volta a carregar Serper/DuckDuckGo.
        """
        print("\n[crew] Carregando ferramentas de apoio...")

        web_tools = []
        if os.getenv("CREWAI_ENABLE_AGENT_SEARCH") == "1":
            web_tools = _load_serper() or _load_duckduckgo()
        else:
            print(
                "  [tools] Busca web aberta desativada no agente; "
                "usando resultados da camada semântica."
            )

        if not web_tools:
            print(
                "  [tools] O agente não fará novas buscas por links; "
                "apenas analisará e, se possível, raspará URLs já coletadas."
            )

        scraper = _load_scraper()
        query_generator = [] if not web_tools else [GerarConsultasBuscaTool()]

        tools = query_generator + web_tools + scraper
        print(f"  [tools] {len(tools)} ferramenta(s) carregada(s): "
              f"{[t.name if hasattr(t, 'name') else type(t).__name__ for t in tools]}\n")
        return tools

    # ------------------------------------------------------------------
    # Agentes
    # ------------------------------------------------------------------

    @agent
    def pesquisador(self) -> Agent:
        """
        Agente 1: responsável pela busca de candidatos na web.
        max_iter=60 permite ao agente fazer muitas chamadas de ferramenta
        antes de concluir, evitando que pare após 1-2 buscas.
        """
        return Agent(
            config=self.agents_config["pesquisador"],  # type: ignore[index]
            tools=self._search_tools(),
            max_iter=60,
            verbose=True,
        )

    @agent
    def analista(self) -> Agent:
        """
        Agente 2: avalia e classifica cada candidato.
        Não precisa de ferramentas de busca — trabalha sobre o texto do Pesquisador.
        """
        return Agent(
            config=self.agents_config["analista"],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def estruturador(self) -> Agent:
        """
        Agente 3: extrai campos padronizados e gera o JSON final.
        Não precisa de ferramentas de busca — trabalha sobre o texto do Analista.
        """
        return Agent(
            config=self.agents_config["estruturador"],  # type: ignore[index]
            verbose=True,
        )

    # ------------------------------------------------------------------
    # Tarefas
    # ------------------------------------------------------------------

    @task
    def pesquisa_task(self) -> Task:
        """Tarefa 1: busca de candidatos a galpões reutilizados."""
        return Task(
            config=self.tasks_config["pesquisa_task"],  # type: ignore[index]
        )

    @task
    def analise_task(self) -> Task:
        """Tarefa 2: classificação de relevância de cada candidato."""
        return Task(
            config=self.tasks_config["analise_task"],  # type: ignore[index]
        )

    @task
    def estruturacao_task(self) -> Task:
        """
        Tarefa 3: estruturação do JSON final.
        O arquivo de saída é definido aqui (não no YAML) para que o caminho
        seja controlado pelo código e não precise ser hardcoded no config.
        output_pydantic valida o JSON gerado contra o schema RelatorioGalpoesCulturais.
        """
        return Task(
            config=self.tasks_config["estruturacao_task"],  # type: ignore[index]
            output_pydantic=RelatorioGalpoesCulturais,
            output_file="output/galpaos_culturais.json",
        )

    # ------------------------------------------------------------------
    # Crew
    # ------------------------------------------------------------------

    @crew
    def crew(self) -> Crew:
        """Instancia a crew com processo sequencial."""
        return Crew(
            agents=self.agents,   # populado automaticamente pelos @agent decorators
            tasks=self.tasks,     # populado automaticamente pelos @task decorators
            process=Process.sequential,
            verbose=True,
        )
