#!/usr/bin/env python
"""
Ponto de entrada do sistema de identificação de galpões reutilizados para
iniciativas culturais no estado de São Paulo.

Uso básico:
    crewai run                          # executa com configurações padrão
    python -m relatorio.main            # executa diretamente com Python

Uso avançado (via run_by_municipio ou parâmetros em run()):
    from relatorio.main import run, run_by_municipio
    run(municipios=["Campinas", "Santos"], limite_resultados=10)
    run_by_municipio("Ribeirão Preto", limite=8)

Variáveis de ambiente necessárias (.env):
    OPENAI_API_KEY   — chave da OpenAI (obrigatória)
    MODEL            — modelo a usar, ex: gpt-4o (padrão)
    SERPER_API_KEY   — chave Serper para busca Google (recomendada, gratuita com limite)
"""

import json
import sys
import warnings
from datetime import datetime
from pathlib import Path

from relatorio.crew import GalpoesCulturais

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


# ---------------------------------------------------------------------------
# Configurações padrão
# ---------------------------------------------------------------------------

# Municípios do estado de São Paulo priorizados na pesquisa.
# Adicione ou remova municípios conforme o escopo desejado.
DEFAULT_MUNICIPIOS: list[str] = [
    "São Paulo",
    "Campinas",
    "Santos",
    "São Bernardo do Campo",
    "Santo André",
    "Osasco",
    "Ribeirão Preto",
    "Sorocaba",
    "São José dos Campos",
    "Mogi das Cruzes",
]

# Combinações de palavras-chave base para busca.
# O pesquisador também usa GerarConsultasBuscaTool para expandir estes termos.
DEFAULT_PALAVRAS_CHAVE: list[str] = [
    "galpão reformado centro cultural São Paulo",
    "antiga fábrica virou espaço cultural São Paulo",
    "armazém desativado ocupado por artistas SP",
    "reconversão industrial cultura São Paulo",
    "galpão reutilizado espaço cultural SP",
    "fábrica abandonada espaço cultural São Paulo",
    "hub criativo galpão industrial São Paulo",
    "ocupação artística galpão São Paulo",
    "fábrica de cultura São Paulo",
    "ateliê coletivo galpão São Paulo",
    "patrimônio industrial reutilizado cultura SP",
    "economia criativa imóvel industrial São Paulo",
    # Referências a espaços conhecidos e programas institucionais
    "SESC galpão São Paulo",
    "Matarazzo espaço cultural São Paulo",
    "Vila Itororó São Paulo espaço cultural",
    "Complexo Fábrica de Cultura SP",
    "galpão do Rock São Paulo",
    "Nave cultural galpão São Paulo",
    "Oficina Cultural galpão São Paulo",
    "armazém do campo cultura São Paulo",
]

# Número máximo de candidatos que o pesquisador deve coletar.
DEFAULT_LIMITE: int = 30

# Diretório de saída para o JSON consolidado.
OUTPUT_DIR = Path("output")
OUTPUT_FILE = OUTPUT_DIR / "galpaos_culturais.json"


# ---------------------------------------------------------------------------
# Utilitários internos
# ---------------------------------------------------------------------------

def _build_inputs(
    municipios: list[str],
    palavras_chave: list[str],
    limite_resultados: int,
) -> dict[str, str]:
    """
    Constrói o dicionário de inputs para o kickoff da crew.
    Todos os valores são strings porque o CrewAI interpola via Jinja2 nos YAMLs.
    """
    return {
        "municipios": ", ".join(municipios),
        "palavras_chave": "\n- " + "\n- ".join(palavras_chave),
        "limite_resultados": str(limite_resultados),
        "data_coleta": datetime.now().strftime("%Y-%m-%d"),
    }


def _print_banner(inputs: dict[str, str]) -> None:
    """Imprime cabeçalho informativo antes da execução."""
    sep = "=" * 65
    print(f"\n{sep}")
    print("  SISTEMA DE IDENTIFICAÇÃO DE GALPÕES CULTURAIS — SP")
    print(sep)
    print(f"  Data de coleta  : {inputs['data_coleta']}")
    print(f"  Municípios      : {inputs['municipios']}")
    print(f"  Limite          : {inputs['limite_resultados']} candidatos")
    print(f"  Saída JSON      : {OUTPUT_FILE.absolute()}")
    print(f"{sep}\n")


def _validate_and_save_output() -> dict | None:
    """
    Lê o arquivo de saída gerado pela crew, tenta fazer parse do JSON
    e retorna o dicionário se válido. Remove blocos markdown se presentes.
    """
    if not OUTPUT_FILE.exists():
        print(f"\n[AVISO] Arquivo de saída não encontrado: {OUTPUT_FILE}")
        return None

    raw = OUTPUT_FILE.read_text(encoding="utf-8").strip()

    # Remove possíveis blocos de código markdown que o LLM possa ter inserido
    if raw.startswith("```"):
        lines = raw.splitlines()
        # Remove primeira e última linha se forem delimitadores de bloco
        start = 1 if lines[0].startswith("```") else 0
        end = len(lines) - 1 if lines[-1].strip() == "```" else len(lines)
        raw = "\n".join(lines[start:end]).strip()

    try:
        data = json.loads(raw)
        # Re-escreve o arquivo limpo (sem markdown)
        OUTPUT_FILE.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return data
    except json.JSONDecodeError as exc:
        print(f"\n[AVISO] O arquivo de saída não é JSON válido: {exc}")
        print("  O conteúdo bruto foi preservado. Verifique o arquivo manualmente.")
        return None


def _print_summary(data: dict) -> None:
    """Imprime resumo dos resultados após a execução."""
    total = data.get("total", len(data.get("espacos_culturais", [])))
    municipios = data.get("municipios_pesquisados", [])
    espacos = data.get("espacos_culturais", [])

    print(f"\n{'=' * 65}")
    print(f"  RESULTADO FINAL")
    print(f"{'=' * 65}")
    print(f"  Espaços identificados : {total}")
    print(f"  Municípios cobertos   : {', '.join(municipios) if municipios else 'N/A'}")
    print(f"  Arquivo gerado        : {OUTPUT_FILE.absolute()}")

    if espacos:
        print(f"\n  Espaços encontrados:")
        for i, esp in enumerate(espacos, 1):
            nome = esp.get("nome", "N/A")
            municipio = esp.get("municipio", "N/A")
            relevancia = esp.get("relevancia", "N/A")
            print(f"  {i:>2}. [{relevancia[:3].upper()}] {nome} — {municipio}")

    print(f"{'=' * 65}\n")


# ---------------------------------------------------------------------------
# Funções públicas (entry points declarados em pyproject.toml)
# ---------------------------------------------------------------------------

def run(
    municipios: list[str] | None = None,
    palavras_chave: list[str] | None = None,
    limite_resultados: int = DEFAULT_LIMITE,
) -> dict | None:
    """
    Executa o sistema completo de identificação de galpões culturais.

    Args:
        municipios: Lista de municípios paulistas para priorizar na busca.
                    Padrão: os 10 maiores municípios do estado.
        palavras_chave: Lista de termos de busca em português.
                        Padrão: 12 combinações pré-definidas.
        limite_resultados: Número máximo de candidatos a coletar.
                           Padrão: 30. Aumente para buscas mais amplas.

    Returns:
        Dicionário com os dados do JSON gerado, ou None se a saída for inválida.
    """
    _municipios = municipios or DEFAULT_MUNICIPIOS
    _palavras_chave = palavras_chave or DEFAULT_PALAVRAS_CHAVE

    OUTPUT_DIR.mkdir(exist_ok=True)

    inputs = _build_inputs(_municipios, _palavras_chave, limite_resultados)
    _print_banner(inputs)

    try:
        GalpoesCulturais().crew().kickoff(inputs=inputs)
    except Exception as exc:
        raise RuntimeError(f"Erro durante a execução da crew: {exc}") from exc

    data = _validate_and_save_output()
    if data:
        _print_summary(data)

    return data


def run_by_municipio(municipio: str, limite: int = 10) -> dict | None:
    """
    Executa a busca focada em um único município paulista.
    Útil para expansão incremental do banco de dados por cidade.

    Args:
        municipio: Nome do município do estado de São Paulo.
        limite: Número máximo de candidatos. Padrão: 10.

    Returns:
        Dicionário com os dados do JSON gerado, ou None se a saída for inválida.

    Exemplo:
        from relatorio.main import run_by_municipio
        run_by_municipio("Campinas", limite=8)
    """
    palavras_chave = [
        f"galpão cultural {municipio} São Paulo",
        f"antiga fábrica espaço cultural {municipio}",
        f"armazém desativado cultura {municipio} SP",
        f"reconversão industrial {municipio} São Paulo",
        f"galpão reutilizado {municipio}",
        f"hub criativo galpão {municipio}",
        f"imóvel industrial virou espaço cultural {municipio}",
        f"fábrica abandonada artistas {municipio} SP",
    ]

    return run(
        municipios=[municipio],
        palavras_chave=palavras_chave,
        limite_resultados=limite,
    )


# ---------------------------------------------------------------------------
# Funções utilitárias para treinamento e replay (compatibilidade CrewAI CLI)
# ---------------------------------------------------------------------------

def train() -> None:
    """Treina a crew por N iterações. Uso: crewai train <n_iterations> <filename>"""
    if len(sys.argv) < 3:
        raise SystemExit("Uso: crewai train <n_iterations> <filename>")
    inputs = _build_inputs(DEFAULT_MUNICIPIOS, DEFAULT_PALAVRAS_CHAVE, DEFAULT_LIMITE)
    try:
        GalpoesCulturais().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs=inputs,
        )
    except Exception as exc:
        raise RuntimeError(f"Erro no treinamento: {exc}") from exc


def replay() -> None:
    """Reexecuta a crew a partir de uma tarefa específica. Uso: crewai replay <task_id>"""
    if len(sys.argv) < 2:
        raise SystemExit("Uso: crewai replay <task_id>")
    try:
        GalpoesCulturais().crew().replay(task_id=sys.argv[1])
    except Exception as exc:
        raise RuntimeError(f"Erro no replay: {exc}") from exc


def test() -> None:
    """Testa a crew por N iterações com um LLM de avaliação."""
    if len(sys.argv) < 3:
        raise SystemExit("Uso: crewai test <n_iterations> <eval_llm>")
    inputs = _build_inputs(DEFAULT_MUNICIPIOS, DEFAULT_PALAVRAS_CHAVE, DEFAULT_LIMITE)
    try:
        GalpoesCulturais().crew().test(
            n_iterations=int(sys.argv[1]),
            eval_llm=sys.argv[2],
            inputs=inputs,
        )
    except Exception as exc:
        raise RuntimeError(f"Erro no teste: {exc}") from exc


# ---------------------------------------------------------------------------
# Execução direta via python -m relatorio.main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run()
