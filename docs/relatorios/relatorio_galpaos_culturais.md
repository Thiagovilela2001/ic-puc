[PONTIFÍCIA UNIVERSIDADE CATÓLICA DE SÃO PAULO]
[Ciências Sociais / Programa de Iniciação Científica]

**THIAGO VILLELA**

---

# SISTEMA MULTIAGENTE PARA IDENTIFICAÇÃO DE GALPÕES INDUSTRIAIS REUTILIZADOS COMO ESPAÇOS CULTURAIS NO ESTADO DE SÃO PAULO

São Paulo
2026

---

## RESUMO

Este relatório apresenta o desenvolvimento de um sistema automatizado, baseado em inteligência artificial generativa com arquitetura agêntica, para identificação e catalogação de imóveis industriais desativados reutilizados como espaços culturais no estado de São Paulo. O sistema utiliza o framework CrewAI para orquestrar três agentes especializados — Pesquisador, Analista e Estruturador — que executam, de forma sequencial e colaborativa, tarefas de busca, classificação e estruturação de dados. A proposta se apoia na experiência metodológica acumulada no desenvolvimento de um sistema análogo voltado ao monitoramento de investimentos produtivos (PIESP/Seade), ampliando o escopo de aplicação das arquiteturas multiagente para o campo do patrimônio industrial e da cultura urbana. O sistema gera como saída um arquivo JSON validado contendo os espaços identificados, com campos padronizados que permitem análises posteriores e integração com bases de dados institucionais.

**Palavras-chave:** Inteligência Artificial. Agentes. CrewAI. Patrimônio Industrial. Espaços Culturais. Web Scraping. São Paulo.

---

## SUMÁRIO

1. [INTRODUÇÃO](#1-introdução)
2. [CONTEXTO E FUNDAMENTOS TEÓRICOS](#2-contexto-e-fundamentos-teóricos)
   - 2.1 [A experiência do sistema PIESP/CrewAI como referência metodológica](#21-a-experiência-do-sistema-piespcrewei-como-referência-metodológica)
   - 2.2 [Arquiteturas multiagente e o framework CrewAI](#22-arquiteturas-multiagente-e-o-framework-crewai)
3. [METODOLOGIA](#3-metodologia)
   - 3.1 [Visão geral da arquitetura](#31-visão-geral-da-arquitetura)
   - 3.2 [Agentes especializados](#32-agentes-especializados)
     - 3.2.1 [Agente 1 — Pesquisador de Patrimônio Cultural Reutilizado](#321-agente-1--pesquisador-de-patrimônio-cultural-reutilizado)
     - 3.2.2 [Agente 2 — Analista de Relevância Cultural e Patrimônio Industrial](#322-agente-2--analista-de-relevância-cultural-e-patrimônio-industrial)
     - 3.2.3 [Agente 3 — Estruturador de Dados de Espaços Culturais](#323-agente-3--estruturador-de-dados-de-espaços-culturais)
   - 3.3 [Modelos de dados (Pydantic v2)](#33-modelos-de-dados-pydantic-v2)
   - 3.4 [Módulo de execução (main.py)](#34-módulo-de-execução-mainpy)
   - 3.5 [Ferramentas e dependências](#35-ferramentas-e-dependências)
4. [PROPOSTA E CONTRIBUIÇÕES ESPERADAS](#4-proposta-e-contribuições-esperadas)
   - 4.1 [Contribuição para o mapeamento do patrimônio cultural paulista](#41-contribuição-para-o-mapeamento-do-patrimônio-cultural-paulista)
   - 4.2 [Limitações previstas e estratégias de mitigação](#42-limitações-previstas-e-estratégias-de-mitigação)
   - 4.3 [Usos potenciais dos dados gerados](#43-usos-potenciais-dos-dados-gerados)
5. [CONSIDERAÇÕES FINAIS](#5-considerações-finais)

[REFERÊNCIAS](#referências)

---

## 1 INTRODUÇÃO

O fenômeno da reconversão de imóveis industriais para uso cultural tem ganhado crescente relevância nas políticas urbanas brasileiras, especialmente no estado de São Paulo, onde décadas de desindustrialização deixaram um extenso parque de galpões, fábricas e armazéns desativados nas malhas urbanas. Esses imóveis constituem um patrimônio histórico e arquitetônico de grande valor simbólico, e sua reutilização como centros culturais, ateliês coletivos, hubs criativos e espaços de exposição representa uma das principais estratégias de requalificação urbana observadas em cidades paulistas nas últimas décadas.

Apesar da relevância do fenômeno, não existe até o momento um mapeamento sistemático e atualizado desses espaços no estado. As informações disponíveis encontram-se dispersas em portais jornalísticos, sites de secretarias de cultura, redes sociais e publicações especializadas, o que torna sua consolidação manual um processo custoso e suscetível a lacunas.

Este trabalho propõe uma solução automatizada para esse problema, desenvolvida com base em uma arquitetura multiagente orquestrada pelo framework CrewAI (CREWAI, 2025). A escolha metodológica se inspira diretamente na experiência prévia com o sistema de monitoramento de investimentos produtivos da PIESP/Seade (VILLELA; MINGARDO, 2025), que demonstrou a viabilidade de arquiteturas agênticas baseadas em Large Language Models (LLMs) para tarefas de busca, filtragem semântica e estruturação de dados provenientes de fontes jornalísticas heterogêneas.

A proposta central é desenvolver um sistema capaz de:

1. Buscar automaticamente, na web aberta, evidências de imóveis industriais reconvertidos para uso cultural nos municípios paulistas;
2. Classificar cada candidato encontrado segundo critérios objetivos de relevância;
3. Estruturar os dados em formato padronizado, pronto para integração com sistemas de informação patrimonial e cultural.

---

## 2 CONTEXTO E FUNDAMENTOS TEÓRICOS

### 2.1 A experiência do sistema PIESP/CrewAI como referência metodológica

O sistema descrito neste relatório é herdeiro direto de uma arquitetura desenvolvida para a Pesquisa de Investimentos Anunciados no Estado de São Paulo (PIESP), conduzida pela Fundação Seade. Naquele projeto, o CrewAI foi utilizado para orquestrar agentes responsáveis por coletar, filtrar e estruturar notícias sobre investimentos produtivos, tomando como referência a metodologia de clipping tradicional da pesquisa.

Os resultados daquela experiência mostraram que sistemas baseados em arquiteturas multiagente com LLMs apresentam desempenho significativamente superior ao das abordagens tradicionais de busca por palavras-chave na tarefa de pré-filtragem semântica: enquanto a metodologia PIESP processou 31.966 notícias para identificar 161 investimentos (taxa de 0,5%), o sistema CrewAI identificou o mesmo volume de investimentos com taxa de compatibilidade de 25,3% sobre um conjunto 45 vezes menor de documentos processados (VILLELA; MINGARDO, 2025).

Essa experiência evidenciou, ao mesmo tempo, os pontos fortes e as limitações da abordagem: alta eficiência de triagem e cobertura ampla de fontes, mas dependência de supervisão humana para classificações abertas e sensibilidade à qualidade do modelo de linguagem utilizado. O presente sistema incorpora essas lições, adotando um fluxo de três agentes especializados com critérios de classificação explícitos e saída em formato estruturado validado.

### 2.2 Arquiteturas multiagente e o framework CrewAI

Sistemas multiagente permitem decompor tarefas complexas em subtarefas coordenadas, executadas por unidades autônomas e especializadas que interagem entre si (JENNINGS; SYCARA; WOOLDRIDGE, 1998; WOOLDRIDGE, 2009). No contexto de processamento de linguagem natural, essa abordagem supera limitações dos pipelines sequenciais ao favorecer o intercâmbio de resultados parciais entre módulos e a tomada de decisões colaborativa.

O framework CrewAI foi selecionado como base de desenvolvimento por apresentar maior adequação para cenários com dados heterogêneos e fluxos dinâmicos (VENKADESH; DIVYA; KUMAR, 2024), além de configuração simplificada, integração modular e boa escalabilidade. A maior parte da customização do sistema baseia-se na definição de prompts para criação de tarefas e configuração dos agentes em arquivos YAML, o que reduz a dependência de intervenções de engenharia de software avançadas e facilita a manutenção por equipes multidisciplinares (CHIN; NG, 2024).

---

## 3 METODOLOGIA

### 3.1 Visão geral da arquitetura

O sistema é implementado em Python 3.10+ e organizado segundo as convenções do projeto CrewAI, com separação clara entre definição de agentes, tarefas, ferramentas e lógica de execução. A arquitetura é composta por:

- **Três agentes especializados**: Pesquisador, Analista e Estruturador;
- **Ferramentas de busca e geração de consultas**: *SerperDevTool*, *DuckDuckGoSearchRun* (fallback) e *GerarConsultasBuscaTool* (customizada);
- **Modelos Pydantic v2** para validação da saída estruturada;
- **Módulo de execução** (`main.py`) com configurações parametrizadas e tratamento de saída.

O fluxo de execução é estritamente sequencial (`Process.sequential`): cada agente recebe como contexto o output do agente anterior, formando uma cadeia de processamento progressivo.

```
[main.py] → kickoff(inputs) → [Pesquisador] → [Analista] → [Estruturador] → output/galpaos_culturais.json
```

O processo sequencial é declarado na instanciação da crew, e o encadeamento entre tarefas é feito pela chave `context` nos arquivos YAML — garantindo que o output de cada agente seja passado automaticamente como entrada do seguinte:

```python
# crew.py
@crew
def crew(self) -> Crew:
    return Crew(
        agents=self.agents,   # populado automaticamente pelos @agent decorators
        tasks=self.tasks,     # populado automaticamente pelos @task decorators
        process=Process.sequential,
        verbose=True,
    )
```

```yaml
# tasks.yaml — encadeamento via context
analise_task:
  agent: analista
  context:
    - pesquisa_task        # recebe o output do Pesquisador

estruturacao_task:
  agent: estruturador
  context:
    - analise_task         # recebe o output do Analista
```

### 3.2 Agentes especializados

#### 3.2.1 Agente 1 — Pesquisador de Patrimônio Cultural Reutilizado

O Pesquisador é responsável pela busca e documentação de candidatos a galpões reutilizados na web. Seu perfil de agente (definido em `config/agents.yaml`) é configurado com o papel de jornalista investigativo especializado em cultura urbana e patrimônio industrial, o que orienta o estilo de raciocínio e a estratégia de busca do LLM subjacente:

```yaml
# agents.yaml
pesquisador:
  role: >
    Pesquisador de Patrimônio Cultural Reutilizado
  goal: >
    Buscar e documentar galpões industriais, armazéns, fábricas e imóveis
    logísticos ou comerciais desativados que foram convertidos em espaços culturais
    no estado de São Paulo, coletando nome, localização, histórico de uso e
    fontes verificáveis para cada candidato encontrado.
  backstory: >
    Você é jornalista investigativo com 15 anos de experiência em cultura urbana
    e patrimônio industrial. [...] Você nunca inventa endereços ou nomes: se não
    encontrou, registra que não encontrou.
```

Em `crew.py`, o agente é instanciado com `max_iter=60`, permitindo até sessenta chamadas de ferramenta antes de encerrar — o que garante cobertura ampla sem interromper prematuramente a pesquisa:

```python
# crew.py
@agent
def pesquisador(self) -> Agent:
    return Agent(
        config=self.agents_config["pesquisador"],
        tools=self._search_tools(),
        max_iter=60,
        verbose=True,
    )
```

O agente tem acesso a três ferramentas:

1. **GerarConsultasBuscaTool** — ferramenta customizada que gera, de forma programática, até 30 consultas de busca em português otimizadas para um município específico, combinando vocabulário controlado de tipos de imóvel (galpão, fábrica, armazém, usina, hangar), adjetivos de desativação (desativado, abandonado, fechado), usos culturais (centro cultural, ateliê coletivo, hub criativo, galeria de arte) e verbos de transformação (virou, se transformou em, abriga). A ferramenta é chamada antes das buscas efetivas para diversificar as queries;

```python
# search_tools.py — vocabulário controlado
TIPOS_IMOVEL = ["galpão", "fábrica", "armazém", "depósito", "usina", "indústria", "hangar", "barracão"]
ADJETIVOS_DESATIVACAO = ["desativado", "abandonado", "desocupado", "fechado", "desativada", "abandonada"]
USOS_CULTURAIS = ["centro cultural", "espaço cultural", "ateliê coletivo", "galeria de arte",
                  "hub criativo", "casa de shows", "fábrica de cultura", "ocupação artística"]
VERBOS_TRANSFORMACAO = ["virou", "tornou-se", "se transformou em", "foi convertido em", "recebeu", "abriga"]
```

2. **SerperDevTool** (ou **DuckDuckGoSearchRun** como fallback gratuito) — executa as buscas web propriamente ditas, configurada para o contexto brasileiro (país `br`, locale `pt-br`). As ferramentas são carregadas condicionalmente pelo método `_search_tools()`:

```python
# crew.py
def _search_tools(self) -> list:
    """Prioridade: SerperDevTool > DuckDuckGoSearchRun > sem busca web."""
    web_tools = _load_serper() or _load_duckduckgo()
    scraper = _load_scraper()
    query_generator = [GerarConsultasBuscaTool()]
    tools = query_generator + web_tools + scraper
    return tools
```

3. **ScrapeWebsiteTool** — permite ao agente acessar URLs promissoras encontradas nas buscas e extrair conteúdo completo das páginas para obter mais detalhes.

A tarefa associada (`pesquisa_task`) instrui o agente a:
- Usar a ferramenta geradora de consultas para obter queries otimizadas;
- Executar ao menos dez buscas distintas variando tipos de imóvel e usos culturais;
- Acessar URLs promissoras para aprofundar os resultados;
- Registrar a URL completa de cada resultado;
- Evitar duplicatas, mantendo o candidato mais completo quando dois resultados descrevem o mesmo espaço.

Esses critérios são impostos diretamente no prompt da tarefa:

```yaml
# tasks.yaml — pesquisa_task (trecho)
description: >
  ETAPAS DA PESQUISA:
  1. Use a ferramenta "Gerador de Consultas para Galpões Culturais" para obter
     queries otimizadas para os municípios prioritários.
  2. Execute ao menos 10 buscas distintas com diferentes combinações de termos —
     varie os tipos de imóvel (galpão, fábrica, armazém, depósito, usina) e os
     tipos de uso cultural (centro cultural, ateliê, galeria, hub criativo).
  3. Para cada resultado promissor, acesse a URL e extraia mais detalhes.
  5. Não pare após os primeiros resultados — prossiga até atingir {limite_resultados}
     candidatos ou esgotar as palavras-chave disponíveis.

expected_output: >
  Lista numerada com NO MÍNIMO 10 candidatos e no máximo {limite_resultados}.
  Não encerre a pesquisa antes de ter ao menos 10 itens na lista.
```

A saída esperada é uma lista numerada com no mínimo dez candidatos no formato padronizado:

```
N. NOME | MUNICÍPIO | ANTIGO USO | USO CULTURAL ATUAL | URL DA FONTE
```

#### 3.2.2 Agente 2 — Analista de Relevância Cultural e Patrimônio Industrial

O Analista avalia criticamente cada candidato da lista produzida pelo Pesquisador e determina sua relevância para os objetivos do mapeamento. O agente não utiliza ferramentas de busca — trabalha exclusivamente sobre o texto recebido via contexto compartilhado do CrewAI:

```python
# crew.py
@agent
def analista(self) -> Agent:
    """Não precisa de ferramentas de busca — trabalha sobre o texto do Pesquisador."""
    return Agent(
        config=self.agents_config["analista"],
        verbose=True,
    )
```

O perfil do agente é configurado como arquiteto com doutorado em patrimônio histórico industrial, o que orienta o LLM a aplicar critérios rigorosos e objetivos de classificação:

```yaml
# agents.yaml
analista:
  role: >
    Analista de Relevância Cultural e Patrimônio Industrial
  backstory: >
    Você é arquiteto com doutorado em patrimônio histórico industrial e vasta
    experiência em políticas culturais no estado de São Paulo. Já avaliou mais
    de 200 imóveis para o programa de tombamento e reconversão da Secretaria
    de Cultura do Estado. [...] Você é criterioso e objetivo: classifica como
    "relevante" apenas quando há evidência documental clara da mudança de uso.
    Quando faltam dados, você classifica como "parcialmente relevante" e indica
    o que falta confirmar.
```

A tarefa (`analise_task`) define três categorias de classificação com critérios explícitos:

| Classificação | Critérios |
|---|---|
| **relevante** | Imóvel claramente industrial/logístico/comercial; reconversão funcional real para uso cultural; evidência documental ou jornalística da transformação |
| **parcialmente relevante** | Indícios de reconversão com informações incompletas; uso misto; fonte não confirma explicitamente o antigo uso |
| **não relevante** | Construído originalmente como espaço cultural; apenas reforma estética; localizado fora de SP; informação insuficiente |

O descarte automático como "não relevante" inclui teatros municipais, museus históricos que sempre foram culturais e reformas de fachada sem mudança de uso. Para cada candidato, o Analista produz uma justificativa de uma a duas frases objetivas fundamentando a classificação. Esses critérios estão declarados diretamente no prompt da tarefa:

```yaml
# tasks.yaml — analise_task (trecho)
description: >
  CRITÉRIOS DE CLASSIFICAÇÃO:

  "relevante":
    - O imóvel era claramente industrial, logístico, portuário ou comercial
    - Passou por uma reconversão funcional real para uso cultural
    - Há evidência documental ou jornalística desta transformação

  "parcialmente relevante":
    - Há indícios de reconversão, mas as informações são incompletas
    - O uso é misto (parte cultural + parte comercial ou residencial)
    - A fonte não confirma explicitamente o antigo uso industrial

  "não relevante":
    - O imóvel foi construído originalmente como espaço cultural
    - Passou apenas por reforma estética sem mudança real de função
    - Está localizado fora do estado de São Paulo

  DESCARTE AUTOMÁTICO (classifique como "não relevante"):
    - Teatros municipais, museus e centros culturais históricos que sempre
      foram culturais desde a fundação
    - Reformas de fachada ou modernização sem mudança de uso
```

#### 3.2.3 Agente 3 — Estruturador de Dados de Espaços Culturais

O Estruturador processa apenas os candidatos classificados como "relevante" ou "parcialmente relevante" pelo Analista e gera o arquivo JSON consolidado final. Seu perfil de engenheiro de dados com experiência em cadastros culturais e sistemas de informação patrimonial orienta o LLM a seguir regras rígidas de preenchimento: apenas campos com informação confirmada nas fontes são preenchidos; para dados ausentes, usa-se exatamente a string `"não informado"`; o output deve ser JSON puro, sem texto adicional ou blocos de código markdown:

```yaml
# agents.yaml
estruturador:
  backstory: >
    Você é engenheiro de dados especializado em cadastros culturais [...].
    Você segue regras rígidas: preenche apenas campos com informação confirmada
    nas fontes, usa exatamente a string "não informado" para dados ausentes e
    nunca supõe ou extrapola. Você gera exclusivamente JSON puro e válido —
    sem texto adicional antes ou depois, sem blocos de código markdown, sem
    comentários fora do JSON. Seu output é sempre parseável por json.loads().
```

O caminho do arquivo de saída é definido diretamente no código Python — não no YAML — para que permaneça sob controle do desenvolvedor:

```python
# crew.py
@task
def estruturacao_task(self) -> Task:
    return Task(
        config=self.tasks_config["estruturacao_task"],
        output_file="output/galpaos_culturais.json",
    )
```

A tarefa (`estruturacao_task`) define os nove campos obrigatórios por espaço:

| Campo | Descrição |
|---|---|
| `nome` | Nome oficial do espaço cultural |
| `endereco` | Endereço completo (logradouro, número, bairro) |
| `municipio` | Município no estado de São Paulo |
| `antigo_uso` | Uso original do imóvel antes da conversão |
| `uso_atual_cultural` | Tipo de uso cultural atual |
| `ano_reutilizacao` | Ano aproximado da conversão cultural |
| `fonte` | URL ou nome da fonte de informação |
| `relevancia` | `"relevante"` ou `"parcialmente relevante"` |
| `justificativa` | Frase curta sobre a evidência de reconversão |

### 3.3 Modelos de dados (Pydantic v2)

O arquivo `models.py` define dois modelos Pydantic v2 que formalizam o schema de saída do sistema:

**`EspacoCultural`** — representa um único espaço identificado, com todos os campos descritos na seção anterior. Os campos `endereco` e `ano_reutilizacao` têm valor padrão `"não informado"`, refletindo a expectativa de que essas informações frequentemente não estejam disponíveis nas fontes consultadas:

```python
# models.py
class EspacoCultural(BaseModel):
    nome: str = Field(description="Nome oficial do espaço cultural")
    endereco: str = Field(
        default="não informado",
        description="Endereço completo incluindo logradouro, número e bairro",
    )
    municipio: str = Field(description="Município no estado de São Paulo")
    antigo_uso: str = Field(description="Uso original do imóvel antes da conversão cultural")
    uso_atual_cultural: str = Field(description="Tipo de uso cultural atual do espaço")
    ano_reutilizacao: str = Field(
        default="não informado",
        description="Ano aproximado em que o imóvel foi convertido para uso cultural",
    )
    fonte: str = Field(description="URL completa ou nome da fonte de informação consultada")
    relevancia: str = Field(
        description="Classificação: 'relevante', 'parcialmente relevante' ou 'não relevante'"
    )
    justificativa: str = Field(
        description="Justificativa resumida da classificação — 1 a 2 frases objetivas"
    )
```

**`RelatorioGalpoesCulturais`** — é o schema raiz do JSON de saída, contendo:
- `espacos_culturais`: lista de objetos `EspacoCultural` validados;
- `total`: contagem inteira dos espaços incluídos (relevantes + parcialmente relevantes);
- `municipios_pesquisados`: lista de municípios cobertos na execução;
- `data_coleta`: data da execução no formato `YYYY-MM-DD`.

```python
# models.py
class RelatorioGalpoesCulturais(BaseModel):
    espacos_culturais: List[EspacoCultural] = Field(
        description="Lista de espaços culturais identificados e validados"
    )
    total: int = Field(
        description="Total de espaços incluídos (relevantes + parcialmente relevantes)"
    )
    municipios_pesquisados: List[str] = Field(
        description="Lista de municípios do estado de São Paulo incluídos na pesquisa"
    )
    data_coleta: str = Field(
        description="Data em que a coleta foi realizada (formato YYYY-MM-DD)"
    )
```

### 3.4 Módulo de execução (main.py)

O ponto de entrada do sistema é o arquivo `main.py`, que expõe duas funções públicas:

**`run(municipios, palavras_chave, limite_resultados)`** — executa o sistema completo. Aceita listas de municípios, palavras-chave e um limite de resultados como parâmetros opcionais, usando valores padrão caso não sejam informados. Os municípios padrão são os dez maiores do estado (São Paulo, Campinas, Santos, São Bernardo do Campo, Santo André, Osasco, Ribeirão Preto, Sorocaba, São José dos Campos e Mogi das Cruzes). As vinte palavras-chave padrão cobrem combinações variadas de termos como *"galpão reformado centro cultural"*, *"antiga fábrica virou espaço cultural"* e referências a programas e espaços conhecidos (SESC, Complexo Fábrica de Cultura, Vila Itororó). O limite padrão é de trinta candidatos:

```python
# main.py — configurações padrão
DEFAULT_MUNICIPIOS: list[str] = [
    "São Paulo", "Campinas", "Santos", "São Bernardo do Campo",
    "Santo André", "Osasco", "Ribeirão Preto", "Sorocaba",
    "São José dos Campos", "Mogi das Cruzes",
]

DEFAULT_PALAVRAS_CHAVE: list[str] = [
    "galpão reformado centro cultural São Paulo",
    "antiga fábrica virou espaço cultural São Paulo",
    "armazém desativado ocupado por artistas SP",
    "SESC galpão São Paulo",
    "Vila Itororó São Paulo espaço cultural",
    "Complexo Fábrica de Cultura SP",
    # ... outras 14 combinações
]

DEFAULT_LIMITE: int = 30
```

**`run_by_municipio(municipio, limite)`** — versão simplificada que executa a busca focada em um único município, gerando automaticamente um conjunto de oito palavras-chave específicas para aquele contexto geográfico. Útil para expansão incremental do banco de dados por cidade:

```python
# main.py
def run_by_municipio(municipio: str, limite: int = 10) -> dict | None:
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
    return run(municipios=[municipio], palavras_chave=palavras_chave, limite_resultados=limite)
```

O fluxo interno de `run()` é:
1. Construção do dicionário de inputs (via `_build_inputs()`), convertendo todos os valores para strings para compatibilidade com a interpolação Jinja2 do CrewAI;
2. Impressão de cabeçalho informativo;
3. Instanciação e execução da crew (`GalpoesCulturais().crew().kickoff(inputs)`);
4. Leitura e validação do arquivo de saída JSON (`_validate_and_save_output()`), com remoção automática de blocos de código markdown que o LLM possa ter inserido;
5. Impressão de resumo dos resultados.

```python
# main.py — _build_inputs() e fluxo principal de run()
def _build_inputs(municipios, palavras_chave, limite_resultados) -> dict[str, str]:
    """Todos os valores são strings: o CrewAI interpola via Jinja2 nos YAMLs."""
    return {
        "municipios": ", ".join(municipios),
        "palavras_chave": "\n- " + "\n- ".join(palavras_chave),
        "limite_resultados": str(limite_resultados),
        "data_coleta": datetime.now().strftime("%Y-%m-%d"),
    }

def run(municipios=None, palavras_chave=None, limite_resultados=DEFAULT_LIMITE):
    inputs = _build_inputs(
        municipios or DEFAULT_MUNICIPIOS,
        palavras_chave or DEFAULT_PALAVRAS_CHAVE,
        limite_resultados,
    )
    GalpoesCulturais().crew().kickoff(inputs=inputs)
    data = _validate_and_save_output()
    if data:
        _print_summary(data)
    return data
```

A função `_validate_and_save_output()` trata um problema recorrente em sistemas baseados em LLMs — a inserção de blocos de código markdown no output JSON —, removendo-os antes do parse:

```python
# main.py — _validate_and_save_output()
def _validate_and_save_output() -> dict | None:
    raw = OUTPUT_FILE.read_text(encoding="utf-8").strip()

    # Remove blocos de código markdown que o LLM possa ter inserido
    if raw.startswith("```"):
        lines = raw.splitlines()
        start = 1 if lines[0].startswith("```") else 0
        end = len(lines) - 1 if lines[-1].strip() == "```" else len(lines)
        raw = "\n".join(lines[start:end]).strip()

    try:
        data = json.loads(raw)
        # Re-escreve o arquivo limpo (sem markdown)
        OUTPUT_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return data
    except json.JSONDecodeError as exc:
        print(f"\n[AVISO] O arquivo de saída não é JSON válido: {exc}")
        return None
```

### 3.5 Ferramentas e dependências

O sistema requer as seguintes variáveis de ambiente:

| Variável | Descrição |
|---|---|
| `OPENAI_API_KEY` | Chave de acesso à API da OpenAI (obrigatória) |
| `MODEL` | Identificador do modelo LLM (padrão: `gpt-4o`) |
| `SERPER_API_KEY` | Chave para a API Serper/Google Search (recomendada) |

O carregamento das ferramentas de busca é condicional: se `SERPER_API_KEY` estiver definida, o *SerperDevTool* é utilizado configurado para o contexto brasileiro; caso contrário, o sistema recorre ao *DuckDuckGoSearchRun* como fallback gratuito. Se nenhuma das duas estiver disponível, o agente opera apenas com o conhecimento interno do modelo de linguagem, com qualidade de resultados significativamente reduzida:

```python
# crew.py
def _load_serper() -> list:
    if not os.getenv("SERPER_API_KEY"):
        return []
    try:
        from crewai_tools import SerperDevTool
        return [SerperDevTool(country="br", locale="pt-br", n_results=10)]
    except Exception:
        return []

def _load_duckduckgo() -> list:
    try:
        from langchain_community.tools import DuckDuckGoSearchRun
        return [DuckDuckGoSearchRun()]
    except ImportError:
        return []
```

A escolha do modelo de linguagem é crítica para a qualidade dos resultados: a experiência do projeto PIESP mostrou que modelos menores (com menos de 10 bilhões de parâmetros) ou versões mais leves como GPT-4o-mini apresentam desempenho insatisfatório em tarefas de classificação semântica aberta. O GPT-4o demonstrou melhor equilíbrio entre custo, precisão e robustez para este tipo de aplicação.

---

## 4 PROPOSTA E CONTRIBUIÇÕES ESPERADAS

### 4.1 Contribuição para o mapeamento do patrimônio cultural paulista

A principal contribuição do sistema é operacionalizar, de forma automatizada e reproduzível, o levantamento de espaços culturais instalados em imóveis industriais reutilizados no estado de São Paulo. Atualmente, esse tipo de mapeamento depende de levantamentos manuais intermitentes, geralmente restritos a recortes geográficos específicos ou categorias de imóveis predefinidas.

O sistema proposto permite ampliar a cobertura geográfica para qualquer município paulista, diversificar as fontes consultadas (portais jornalísticos, sites institucionais, secretarias de cultura) e manter o banco de dados atualizado por meio de reexecuções periódicas.

### 4.2 Limitações previstas e estratégias de mitigação

Com base na experiência do sistema PIESP, antecipam-se as seguintes limitações:

**Classificações abertas**: a experiência anterior mostrou que LLMs tendem a gerar categorias redundantes e inconsistentes quando não há um conjunto fechado de classes predefinido. No presente sistema, esse risco foi mitigado por meio de critérios de classificação explícitos e tripartidos (relevante/parcialmente relevante/não relevante) definidos diretamente no prompt do Analista, eliminando a classificação completamente aberta.

**Supervisão humana**: o sistema não substitui a curadoria especializada. A classificação do Analista e a estruturação do Estruturador dependem da qualidade das informações nas fontes consultadas e podem requerer revisão manual, especialmente para os casos "parcialmente relevantes".

**Cobertura de fontes**: o sistema é eficaz para espaços com cobertura jornalística ou presença em fontes institucionais, mas pode ter baixa cobertura de iniciativas menores ou informais sem presença significativa na web aberta. A `GerarConsultasBuscaTool` prevê a ativação opcional de filtros `site:` para priorizar veículos confiáveis:

```python
# search_tools.py
FONTES_PRIORIZADAS = [
    "site:folha.uol.com.br",
    "site:estadao.com.br",
    "site:g1.globo.com",
    "site:agenciabrasil.ebc.com.br",
    "site:cultura.sp.gov.br",
    "site:sescsp.org.br",
]

# Ativado quando incluir_filtros_fonte=True na chamada da ferramenta
if incluir_filtros_fonte and consultas:
    filtro = " OR ".join(FONTES_PRIORIZADAS[:3])
    consultas_filtradas = [f"{q} ({filtro})" for q in consultas[:4]]
```

**Custos computacionais**: o uso de GPT-4o tem custo por token. A configuração de `max_iter=60` para o Pesquisador e a execução de buscas múltiplas podem gerar consumo expressivo de tokens por execução, especialmente em buscas amplas com muitos municípios.

### 4.3 Usos potenciais dos dados gerados

O arquivo JSON de saída (`output/galpaos_culturais.json`) foi projetado para integração com sistemas de informação mais amplos. A seguir, um exemplo prático da estrutura do arquivo gerado pelo sistema:

```json
{
  "espacos_culturais": [
    {
      "nome": "Galpão das Artes de Campinas",
      "endereco": "Rua das Indústrias, 450, Cambuí",
      "municipio": "Campinas",
      "antigo_uso": "Fábrica têxtil desativada",
      "uso_atual_cultural": "Ateliê coletivo e galeria de arte",
      "ano_reutilizacao": "2018",
      "fonte": "https://g1.globo.com/sp/campinas/.../galeria-campinas.html",
      "relevancia": "relevante",
      "justificativa": "Reportagem confirma reconversão de fábrica têxtil em ateliê coletivo em 2018."
    }
  ],
  "total": 1,
  "municipios_pesquisados": ["Campinas"],
  "data_coleta": "2026-03-04"
}
```

Os campos padronizados permitem:

- Georreferenciamento e visualização cartográfica dos espaços identificados;
- Análise da distribuição regional e municipal das reconversões;
- Cruzamento com bases de dados de tombamento e patrimônio histórico;
- Identificação de padrões temporais de reconversão por tipo de imóvel e uso cultural;
- Subsídio para políticas públicas de preservação e fomento à cultura.

---

## 5 CONSIDERAÇÕES FINAIS

Este trabalho apresentou a arquitetura, a implementação e a proposta de um sistema multiagente baseado no framework CrewAI para identificação automatizada de galpões industriais reutilizados como espaços culturais no estado de São Paulo.

O sistema apoia-se em uma cadeia de três agentes especializados — Pesquisador, Analista e Estruturador —, cada um com papel claramente definido, ferramentas adequadas à sua função e critérios explícitos de qualidade. A arquitetura herda e adapta escolhas metodológicas validadas no sistema PIESP/Seade, incorporando as lições aprendidas sobre a importância de classificações estruturadas, supervisão humana e escolha do modelo de linguagem.

A abordagem demonstra que arquiteturas agênticas baseadas em LLMs são aplicáveis a domínios além do monitoramento econômico, estendendo-se ao campo do patrimônio cultural e da requalificação urbana. A combinação de busca automatizada, análise semântica e estruturação de dados representa um avanço metodológico relevante para o mapeamento de fenômenos urbanos difusos, que dependem de informações dispersas em múltiplas fontes digitais.

Trabalhos futuros poderão explorar a ampliação das fontes de busca (redes sociais, Instagram, LinkedIn), o refinamento dos critérios de classificação com base em avaliações supervisionadas, e a integração dos dados gerados com sistemas de informação cultural e patrimonial já existentes no âmbito estadual e municipal.

---

## REFERÊNCIAS

CHIN, S. Y.; NG, K. W. Comparative of Multi-Agent System Frameworks: CrewAI, LangChain, and AutoGen. **Social Science Research Network (SSRN)**, [S. l.], n. 5367964, 2024. Disponível em: https://ssrn.com/abstract=5367964. Acesso em: 4 mar. 2026.

CREWAI. **CrewAI Framework Documentation**. [S. l.], 2025. Disponível em: https://docs.crewai.com. Acesso em: 4 mar. 2026.

JENNINGS, N. R.; SYCARA, K.; WOOLDRIDGE, M. A roadmap of agent research and development. **Autonomous Agents and Multi-Agent Systems**, [S. l.], v. 1, n. 1, p. 7-38, 1998.

VENKADESH, P.; DIVYA, S. V.; KUMAR, K. S. Unlocking AI Creativity: A Multi-Agent Approach with CrewAI. **Journal of Trends in Computer Science and Smart Technology**, [S. l.], v. 6, n. 4, p. 338-356, 2024.

VILLELA, T.; MINGARDO, L. **Metodologias de Coleta de Dados sobre Investimentos**: um estudo comparativo entre sistema multiagente e PIESP. São Paulo: Fundação Seade, 2025.

WOOLDRIDGE, M. **An Introduction to MultiAgent Systems**. 2. ed. Chichester: Wiley, 2009.

