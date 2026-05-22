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

from dotenv import load_dotenv

from relatorio.crew import GalpoesCulturais
from relatorio.search import SemanticSearchPipeline
from relatorio.search.url_validator import verify_url

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


# ---------------------------------------------------------------------------
# Configurações padrão
# ---------------------------------------------------------------------------

# Escopo geográfico da pesquisa.
# Definido como estado inteiro — sem restrição a municípios específicos.
DEFAULT_MUNICIPIOS: list[str] = ["estado de São Paulo"]

# Combinações de palavras-chave base para a camada semântica.
# O SemanticQueryBuilder expande estes termos antes de executar a busca real.
DEFAULT_PALAVRAS_CHAVE: list[str] = [
    # Transformação de uso — linguagem jornalística
    'fábrica "virou espaço cultural" São Paulo -aluguel -venda -locação',
    'fábrica "se tornou centro cultural" São Paulo -aluguel -venda',
    'galpão "transformado em" "espaço cultural" São Paulo -aluguel -venda',
    'armazém "convertido em" "espaço cultural" São Paulo -aluguel',
    '"antiga fábrica" "espaço cultural" São Paulo -aluguel -locação',
    '"antigo armazém" "espaço cultural" São Paulo -aluguel',
    '"antigo galpão" "centro cultural" São Paulo -aluguel -venda',
    # Reconversão e requalificação urbana
    '"reconversão industrial" "espaço cultural" "São Paulo"',
    '"requalificação urbana" "espaço cultural" galpão São Paulo',
    '"patrimônio industrial" reutilizado "cultura" São Paulo',
    '"imóvel industrial" "espaço cultural" São Paulo -aluguel',
    # Tipos específicos de espaço cultural em galpão
    '"ateliê coletivo" galpão "São Paulo" -aluguel -venda',
    '"hub criativo" galpão "São Paulo" -aluguel -venda',
    '"centro cultural" "antiga fábrica" OR "antigo galpão" São Paulo',
    '"galeria de arte" galpão "São Paulo" -aluguel -venda',
    '"casa de shows" galpão "São Paulo" -aluguel',
    '"ocupação artística" galpão "São Paulo"',
    # Fontes institucionais e jornalísticas
    'site:g1.globo.com galpão "espaço cultural" "São Paulo"',
    'site:estadao.com.br galpão "espaço cultural"',
    'site:folha.uol.com.br galpão "espaço cultural"',
    'site:agenciabrasil.ebc.com.br galpão "espaço cultural"',
    'site:cultura.sp.gov.br galpão OR fábrica OR armazém',
    'site:sescsp.org.br galpão OR "espaço cultural"',
]

# Número máximo de candidatos que o pesquisador deve coletar.
DEFAULT_LIMITE: int = 30

# Diretório de saída para o JSON consolidado.
OUTPUT_DIR = Path("output")
OUTPUT_FILE = OUTPUT_DIR / "galpaos_culturais.json"
CACHE_DIR = OUTPUT_DIR / "cache_busca"


def _load_environment() -> None:
    """Carrega variaveis do arquivo .env antes das buscas e da crew."""
    load_dotenv()


def _build_inputs(
    municipios: list[str],
    palavras_chave: list[str],
    limite_resultados: int,
    resultados_busca: str = "",
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
        "resultados_busca": resultados_busca,
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
    Lê o arquivo de saída gerado pela crew e retorna o dicionário se válido.
    O JSON já é gravado limpo pelo CrewAI via output_pydantic; esta função
    serve como verificação final e ponto único de leitura do resultado.
    """
    if not OUTPUT_FILE.exists():
        print(f"\n[AVISO] Arquivo de saída não encontrado: {OUTPUT_FILE}")
        return None

    try:
        data = json.loads(OUTPUT_FILE.read_text(encoding="utf-8"))
        return data
    except json.JSONDecodeError as exc:
        print(f"\n[AVISO] O arquivo de saída não é JSON válido: {exc}")
        print("  Verifique o arquivo manualmente.")
        return None


def _filter_unverified_urls(data: dict) -> dict:
    """
    Remove de 'espacos_culturais' qualquer entrada cuja URL de fonte
    não responda a uma requisição HTTP real. Atualiza 'total' e
    re-salva o JSON no OUTPUT_FILE.
    """
    espacos = data.get("espacos_culturais", [])
    if not espacos:
        return data

    print(f"\n[verificação] Checando {len(espacos)} URL(s)...")
    verificados, removidos = [], []

    for esp in espacos:
        url = esp.get("fonte", "não informado")
        if url == "não informado" or not url.startswith("http"):
            print(f"  [REMOVIDO — sem URL] {esp.get('nome', 'N/A')}")
            removidos.append(esp)
            continue
        if verify_url(url):
            print(f"  [OK] {esp.get('nome', 'N/A')} — {url}")
            verificados.append(esp)
        else:
            print(f"  [REMOVIDO — URL inválida] {esp.get('nome', 'N/A')} — {url}")
            removidos.append(esp)

    if removidos:
        print(f"\n  {len(removidos)} entrada(s) removida(s) por URL inválida ou ausente.")

    data["espacos_culturais"] = verificados
    data["total"] = len(verificados)

    OUTPUT_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return data


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
    _load_environment()

    _municipios = municipios or DEFAULT_MUNICIPIOS
    _palavras_chave = palavras_chave or DEFAULT_PALAVRAS_CHAVE

    OUTPUT_DIR.mkdir(exist_ok=True)

    print("\n[busca] Coletando resultados da web pela camada semântica...")
    max_queries = min(30, max(12, len(_palavras_chave) + 8))
    search_report = SemanticSearchPipeline(cache_dir=CACHE_DIR).run(
        municipios=_municipios,
        seed_queries=_palavras_chave,
        max_queries=max_queries,
        max_per_query=5,
        max_pages=limite_resultados * 2,
        audit_file=OUTPUT_DIR / "busca_semantica.json",
    )
    resultados_busca = search_report.format_for_crew()
    _palavras_chave = search_report.queries

    inputs = _build_inputs(_municipios, _palavras_chave, limite_resultados, resultados_busca)
    _print_banner(inputs)

    GalpoesCulturais().crew().kickoff(inputs=inputs)

    data = _validate_and_save_output()
    if data:
        data = _filter_unverified_urls(data)
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
    _load_environment()
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
    _load_environment()
    if len(sys.argv) < 2:
        raise SystemExit("Uso: crewai replay <task_id>")
    try:
        GalpoesCulturais().crew().replay(task_id=sys.argv[1])
    except Exception as exc:
        raise RuntimeError(f"Erro no replay: {exc}") from exc


def test() -> None:
    """Testa a crew por N iterações com um LLM de avaliação."""
    _load_environment()
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
