# PONTIFÍCIA UNIVERSIDADE CATÓLICA DE SÃO PAULO

**Faculdade de Ciências Sociais**

**Programa Institucional de Bolsas de Iniciação Científica — PIBIC 2025/2026**

\

\

\

## RELATÓRIO PARCIAL DE INICIAÇÃO CIENTÍFICA

\

**SISTEMA MULTIAGENTE PARA IDENTIFICAÇÃO DE GALPÕES INDUSTRIAIS REUTILIZADOS COMO ESPAÇOS CULTURAIS NO ESTADO DE SÃO PAULO**

\

\

| | |
|---|---|
| **Bolsista:** | Thiago Villela |
| **Curso:** | Ciências Sociais |
| **Orientador:** | Prof Monica Carvalho |
| **Título do projeto:** | Sistema Multiagente para Identificação de Galpões Industriais Reutilizados como Espaços Culturais no Estado de São Paulo |
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ |
| **Período de vigência da bolsa:** | Setembro de 2025 – Agosto de 2026 |
| **Período coberto por este relatório:** | Setembro de 2025 – Fevereiro de 2026 |

\

\

\

São Paulo
2026

---

\newpage

---

## SUMÁRIO

INTRODUÇÃO ................................................................................................................ 3

PARTE I — ATIVIDADES DESENVOLVIDAS ...................................................................... 4

&emsp;I.1&emsp;Sistemática de orientação adotada pelo professor ................................................ 4

&emsp;I.2&emsp;Objetivos alcançados, dificuldades encontradas e estratégias de superação ............. 5

&emsp;I.3&emsp;Alterações realizadas sobre o projeto original e suas justificativas .......................... 7

&emsp;I.4&emsp;Atividades acadêmico-científico-culturais relacionadas à pesquisa .......................... 8

PARTE II — RELATÓRIO CIENTÍFICO .............................................................................. 9

&emsp;II.1&emsp;Apresentação e discussão crítica dos resultados preliminares ................................. 9

&emsp;&emsp;&emsp;II.1.1&emsp;Contexto e fundamentos teóricos ............................................................. 9

&emsp;&emsp;&emsp;II.1.2&emsp;Metodologia: arquitetura e implementação do sistema ................................ 13

&emsp;&emsp;&emsp;II.1.3&emsp;Resultados preliminares e avaliação do sistema ........................................ 28

&emsp;II.2&emsp;Cronograma de atividades para os próximos seis meses ...................................... 31

REFERÊNCIAS BIBLIOGRÁFICAS .................................................................................... 34

---

\newpage

---

## INTRODUÇÃO

O presente documento constitui o Relatório Parcial de Iniciação Científica referente ao projeto *Sistema Multiagente para Identificação de Galpões Industriais Reutilizados como Espaços Culturais no Estado de São Paulo*, desenvolvido no âmbito do Programa Institucional de Bolsas de Iniciação Científica (PIBIC 2025/2026) da Pontifícia Universidade Católica de São Paulo (PUC-SP), Faculdade de Ciências Sociais.

O projeto insere-se no campo das metodologias computacionais aplicadas às Ciências Sociais, propondo o desenvolvimento de um sistema automatizado — baseado em inteligência artificial generativa com arquitetura multiagente — para a identificação e catalogação de imóveis industriais desativados reutilizados como espaços culturais no estado de São Paulo. O sistema é construído sobre o framework CrewAI e utiliza Grandes Modelos de Linguagem (do inglês *Large Language Models* — LLMs) para orquestrar agentes especializados nas tarefas de busca, análise e estruturação de dados.

A problemática que motiva o projeto é ao mesmo tempo empírica e metodológica. Do ponto de vista empírico, o fenômeno da reconversão cultural de imóveis industriais é socialmente relevante e geograficamente expressivo no estado de São Paulo, mas carece de um mapeamento sistemático e atualizado: as informações disponíveis encontram-se dispersas em portais jornalísticos, sites de secretarias de cultura, redes sociais e publicações especializadas, tornando sua consolidação manual trabalhosa e incompleta. Do ponto de vista metodológico, o projeto avança sobre uma lacuna identificada na literatura: a ausência de sistemas automatizados que combinem busca em fontes abertas, análise semântica e estruturação de dados para o levantamento de fenômenos urbanos difusos.

A inspiração metodológica direta provém da experiência acumulada no desenvolvimento de um sistema análogo para o monitoramento de investimentos produtivos no âmbito da Pesquisa de Investimentos Anunciados no Estado de São Paulo (PIESP), realizada pela Fundação Seade. Os resultados obtidos naquele projeto demonstraram que arquiteturas multiagente com LLMs são capazes de triar e estruturar dados jornalísticos com eficiência significativamente superior à das abordagens tradicionais de busca por palavras-chave, o que justifica sua extensão ao campo do patrimônio cultural e da requalificação urbana.

Este relatório está organizado em duas partes. A **Parte I** descreve as atividades de pesquisa desenvolvidas nos primeiros seis meses de vigência da bolsa, incluindo a sistemática de orientação, os objetivos alcançados, as dificuldades enfrentadas e as atividades complementares de formação acadêmica. A **Parte II** apresenta os resultados científicos preliminares, abrangendo a revisão da literatura, a descrição completa da metodologia e da implementação do sistema, e o cronograma de atividades para os próximos seis meses.

---

\newpage

---

## PARTE I — ATIVIDADES DESENVOLVIDAS

### I.1 Sistemática de orientação adotada pelo professor

A orientação ao longo dos primeiros seis meses de vigência da bolsa seguiu uma sistemática estruturada em três dimensões complementares: reuniões periódicas de acompanhamento, leituras dirigidas e supervisão técnica da implementação computacional.

As reuniões de orientação foram realizadas em periodicidade quinzenal, com duração aproximada de uma hora cada. Cada encontro foi organizado em dois momentos distintos: uma primeira etapa de revisão das leituras e discussão teórica, em que o orientador apresentava questões problematizadoras a respeito dos textos indicados, especialmente sobre a interface entre Ciências Sociais e sistemas computacionais; e uma segunda etapa de acompanhamento técnico, em que o bolsista apresentava o estado de desenvolvimento do sistema, submetendo decisões de arquitetura e de *prompt engineering* à apreciação crítica do orientador.

As leituras foram organizadas em três blocos sequenciais. O primeiro bloco, desenvolvido nos meses iniciais (setembro a outubro de 2025), concentrou-se nos fundamentos dos sistemas multiagente e na literatura sobre patrimônio industrial e cultura urbana. O segundo bloco (novembro a dezembro de 2025) aprofundou o estudo do framework CrewAI e das práticas de engenharia de *prompts*, com ênfase na documentação oficial e em artigos comparativos de frameworks concorrentes. O terceiro bloco (janeiro a fevereiro de 2026) foi dedicado à literatura sobre coleta e estruturação de dados em Ciências Sociais, incluindo metodologias de curadoria de dados e avaliação de qualidade de sistemas de informação.

A supervisão técnica da implementação foi realizada de forma assíncrona entre as reuniões presenciais: o bolsista encaminhava ao orientador, via repositório compartilhado, os arquivos de código produzidos, os logs de execução do sistema e os resultados de cada rodada de testes. O orientador retornava comentários escritos apontando inconsistências, sugerindo ajustes nos critérios de classificação e validando as decisões arquiteturais de maior impacto.

Essa sistemática mostrou-se adequada ao perfil interdisciplinar do projeto, na medida em que articulou a dimensão teórica das Ciências Sociais — especialmente os conceitos de patrimônio industrial, requalificação urbana e política cultural — com as exigências técnicas do desenvolvimento de sistemas baseados em inteligência artificial generativa.

---

### I.2 Objetivos alcançados, dificuldades encontradas e estratégias de superação

#### Objetivos alcançados

Os primeiros seis meses de desenvolvimento foram dedicados principalmente à **concepção, implementação e validação inicial da arquitetura completa do sistema**. Os objetivos estabelecidos no projeto original para esta etapa foram integralmente alcançados:

1. **Revisão bibliográfica completa**: levantamento e fichamento das referências centrais sobre sistemas multiagente, framework CrewAI, patrimônio industrial paulista e metodologias computacionais aplicadas às Ciências Sociais.

2. **Definição da arquitetura multiagente**: especificação dos três agentes especializados (Pesquisador, Analista e Estruturador), de seus respectivos perfis, ferramentas e critérios de operação; escolha do processo sequencial como modo de orquestração; e definição do schema de saída em JSON com validação via Pydantic v2.

3. **Implementação integral do sistema**: desenvolvimento de todos os módulos do sistema em Python 3.10+, incluindo os arquivos `crew.py`, `main.py`, `models.py`, `search_tools.py` e os arquivos de configuração em YAML (`agents.yaml` e `tasks.yaml`). O sistema encontra-se operacional e testado em ambiente local.

4. **Desenvolvimento da ferramenta customizada de geração de consultas**: implementação da `GerarConsultasBuscaTool`, que combina vocabulário controlado de tipos de imóvel, adjetivos de desativação, usos culturais e verbos de transformação para gerar até 30 consultas de busca otimizadas por município.

5. **Validação inicial com rodadas de teste**: realização de execuções-piloto do sistema cobrindo os dez maiores municípios do estado de São Paulo, com avaliação qualitativa dos candidatos identificados, das classificações produzidas pelo Analista e da qualidade do JSON gerado pelo Estruturador.

6. **Documentação técnica**: produção de documentação descrevendo a arquitetura, os fluxos de dados e os critérios de classificação, que serve de base para o presente relatório científico.

#### Dificuldades encontradas e estratégias de superação

O desenvolvimento do sistema confrontou o bolsista com desafios de natureza tanto técnica quanto conceitual, descritos a seguir juntamente com as estratégias adotadas para superá-los.

**a) Custo computacional das execuções com GPT-4o.** A configuração inicial do agente Pesquisador com `max_iter=60` e buscas múltiplas por município gerava execuções com consumo expressivo de tokens, tornando os testes iterativos financeiramente inviáveis para uma bolsa de iniciação científica. A estratégia adotada foi realizar os testes de desenvolvimento com o modelo `gpt-4o-mini` — suficientemente capaz para validar o fluxo lógico do sistema, embora com qualidade de classificação inferior — e reservar o GPT-4o para as execuções de validação formal. Paralelamente, o limite de iterações do Pesquisador foi parametrizado, permitindo reduzi-lo durante os testes sem alterar o comportamento esperado para produção.

**b) Instabilidade das ferramentas de busca web.** O *DuckDuckGoSearchRun*, utilizado como alternativa gratuita ao SerperDevTool, apresentou inconsistências frequentes: erros de limite de requisições, resultados truncados ou respostas em inglês que escapavam ao filtro de localização brasileira. A estratégia de mitigação foi tornar o carregamento das ferramentas estritamente condicional e com tratamento de exceção, de modo que o sistema degradasse graciosamente para o *DuckDuckGo* na ausência da chave Serper e para funcionamento sem busca web na ausência de ambas. Adicionalmente, a `GerarConsultasBuscaTool` foi implementada como módulo independente das ferramentas de busca, garantindo que a geração de *queries* otimizadas não dependesse de APIs externas.

**c) Inserção de blocos de código Markdown no output JSON.** Um problema recorrente nas primeiras execuções foi a tendência do LLM de envolver o JSON de saída em delimitadores Markdown (` ```json ` e ` ``` `), tornando-o não parseável diretamente por `json.loads()`. Embora as instruções do agente Estruturador explicitassem a proibição de blocos Markdown, o comportamento persistia em aproximadamente 40% das execuções com GPT-4o e em cerca de 70% com GPT-4o-mini. A solução implementada foi a função `_validate_and_save_output()` no módulo `main.py`, que detecta e remove automaticamente os delimitadores antes de tentar parsear o JSON, reescrevendo o arquivo de saída com o conteúdo limpo.

**d) Critérios de classificação imprecisos nas versões iniciais dos prompts.** As primeiras versões do prompt do agente Analista utilizavam critérios mais abertos para as três categorias de relevância, o que resultava em classificações inconsistentes entre execuções distintas com os mesmos candidatos. A solução foi a especificação progressivamente mais granular dos critérios de classificação, incluindo exemplos negativos explícitos ("descarte automático") e a exigência de justificativa obrigatória em uma a duas frases por candidato — o que força o modelo a explicitar seu raciocínio e torna os erros de classificação mais facilmente identificáveis na revisão humana.

**e) Ambiguidade conceitual na definição de "imóvel industrial reutilizado".** A fronteira entre um imóvel industrial genuinamente reconvertido e um espaço que incorporou elementos estéticos industriais sem ter sido efetivamente uma instalação fabril é frequentemente tênue. A estratégia adotada foi a incorporação, no critério "não relevante", da cláusula de "imóvel construído originalmente como espaço cultural" e a definição de usos anteriores elegíveis (industrial, armazém, logística ou comércio atacadista), excluindo explicitamente comércio varejista e serviços.

---

### I.3 Alterações realizadas sobre o projeto original e suas justificativas

O projeto de pesquisa submetido ao PIBIC contemplava, para esta primeira etapa, apenas o desenvolvimento conceitual do sistema (definição de arquitetura, revisão bibliográfica e especificação dos agentes). A implementação computacional estava prevista para a segunda etapa. Contudo, com o avanço mais rápido do que o esperado na revisão bibliográfica e na definição arquitetural — favorecido pela experiência prévia do bolsista com o sistema PIESP/Seade —, optou-se, com anuência do orientador, por antecipar o início da implementação computacional para o segundo mês de bolsa.

Essa antecipação gerou o benefício substantivo de dispor, ao final dos primeiros seis meses, de um sistema completamente funcional e parcialmente testado, em vez de apenas um projeto arquitetural. Isso permitirá que a segunda etapa da pesquisa seja integralmente dedicada à execução sistemática, avaliação quantitativa e aprimoramento iterativo do sistema.

Houve também uma alteração no conjunto de ferramentas de busca previsto. O projeto original previa o uso exclusivo da API Google Search (via SerperDevTool). Durante a implementação, verificou-se a conveniência de incluir o *DuckDuckGoSearchRun* como alternativa gratuita, reduzindo a dependência financeira de APIs pagas e viabilizando ciclos mais frequentes de teste. O design condicional de carregamento das ferramentas foi incorporado à arquitetura como solução permanente, por ampliar a resiliência e a portabilidade do sistema.

Por fim, a modelagem da saída JSON foi expandida em relação ao projeto original. Inicialmente, previa-se um schema simples com cinco campos por espaço. Durante a implementação, o orientador recomendou a inclusão de campos adicionais (`relevancia`, `justificativa` e `municipios_pesquisados` no schema raiz), de modo a tornar o arquivo de saída autoexplicativo e auditável sem necessidade de consultar os logs de execução. Essa expansão está formalizada nos modelos Pydantic v2 descritos na Parte II.

---

### I.4 Atividades acadêmico-científico-culturais relacionadas à pesquisa

Ao longo dos primeiros seis meses de bolsa, o bolsista desenvolveu um conjunto de atividades complementares que contribuíram de forma direta para a consolidação das competências necessárias ao projeto:

**Estudos de frameworks e bibliotecas.** Foram realizados estudos sistemáticos da documentação oficial do CrewAI (CREWAI, 2025), incluindo a leitura integral dos módulos de definição de agentes, tarefas, ferramentas e processos de orquestração. Paralelamente, foram estudados os frameworks concorrentes LangChain e AutoGen, com base no artigo comparativo de Chin e Ng (2024), o que permitiu fundamentar a escolha do CrewAI com base em critérios técnicos objetivos. Foi também realizado estudo aprofundado da biblioteca Pydantic v2 para validação de schemas JSON e do pacote LangChain Community para uso do DuckDuckGoSearchRun.

**Leituras sobre patrimônio industrial e cultura urbana.** A revisão bibliográfica sobre o tema empírico da pesquisa incluiu leituras sobre o processo de desindustrialização paulista e seus impactos urbanísticos, sobre políticas de preservação do patrimônio industrial no Brasil e no estado de São Paulo, e sobre a literatura internacional acerca da reconversão de imóveis industriais para uso cultural. Essas leituras foram fundamentais para a definição dos critérios de classificação adotados pelo agente Analista e para a escolha do vocabulário controlado utilizado na geração de consultas.

**Estudo do sistema PIESP como referência metodológica.** O bolsista realizou análise detalhada do sistema multiagente desenvolvido para a PIESP/Seade (VILLELA; MINGARDO, 2025), examinando os logs de execução, os critérios de filtragem e os resultados comparativos entre o sistema computacional e a metodologia de clipping manual. Esse estudo foi central para a transferência de aprendizados metodológicos ao presente projeto, especialmente no que diz respeito à importância de critérios de classificação fechados, ao dimensionamento do parâmetro `max_iter` e ao tratamento de outputs malformados.

**Participação em evento de Iniciação Científica.** O bolsista participou, como ouvinte, do Encontro de Iniciação Científica da PUC-SP realizado em outubro de 2025, o que propiciou contato com projetos de outras áreas e reforçou a perspectiva interdisciplinar da pesquisa. A participação contribuiu ainda para a familiarização com os critérios de avaliação de relatórios e apresentações de IC, orientando a elaboração do presente documento.

**Elaboração de documentação técnica.** Ao longo do período, o bolsista produziu documentação interna do sistema (comentários no código, arquivos README e o próprio relatório científico ora apresentado), desenvolvendo competências de comunicação técnica e científica que serão essenciais para a elaboração do relatório final e para a apresentação nos Anais do Encontro de IC.

---

\newpage

---

## PARTE II — RELATÓRIO CIENTÍFICO

### II.1 Apresentação e discussão crítica dos resultados preliminares

#### II.1.1 Contexto e fundamentos teóricos

##### A problemática empírica: reconversão cultural de imóveis industriais no estado de São Paulo

O fenômeno da reconversão de imóveis industriais para uso cultural tem ganhado crescente relevância nas políticas urbanas brasileiras, especialmente no estado de São Paulo, onde décadas de desindustrialização deixaram um extenso parque de galpões, fábricas e armazéns desativados nas malhas urbanas. Esses imóveis constituem um patrimônio histórico e arquitetônico de grande valor simbólico, e sua reutilização como centros culturais, ateliês coletivos, hubs criativos e espaços de exposição representa uma das principais estratégias de requalificação urbana observadas em cidades paulistas nas últimas décadas.

A desindustrialização paulista, acelerada a partir da década de 1990 em decorrência de reestruturações produtivas, abertura comercial e desconcentração industrial em direção ao interior do estado e a outras regiões do país, produziu um vasto estoque de imóveis industriais subutilizados ou abandonados. Nas metrópoles — particularmente na cidade de São Paulo —, esses imóveis tenderam a concentrar-se em áreas outrora industriais que passaram por processos de esvaziamento econômico e subsequente reconversão de uso, como o bairro da Mooca, o Brás, o Belenzinho, a Lapa e Santo André. Em cidades médias do interior, o fenômeno assumiu contornos distintos, frequentemente associados à decadência de indústrias locais específicas — têxtil em Americana, calçadista em Franca, metalúrgica em Sorocaba.

A reconversão desses espaços para usos culturais não é um fenômeno espontâneo nem homogêneo. Ela resulta de dinâmicas distintas: em alguns casos, é impulsionada por políticas públicas de preservação e requalificação patrimonial (como o programa Fábricas de Cultura da Secretaria de Cultura do Estado de São Paulo); em outros, emerge de iniciativas privadas de empreendedorismo cultural ou de ocupações artísticas autônomas, que encontram nesses imóveis não apenas espaço físico amplo e acessível, mas também uma identidade arquitetônica e histórica que ressoa com determinadas estéticas e práticas culturais contemporâneas.

Apesar da relevância social, econômica e patrimonial do fenômeno, não existe até o momento um mapeamento sistemático e atualizado desses espaços no estado de São Paulo. As informações disponíveis encontram-se dispersas em portais jornalísticos, sites de secretarias de cultura, redes sociais e publicações especializadas, o que torna sua consolidação manual um processo custoso, incompleto e de difícil atualização periódica. Essa lacuna é o ponto de partida do presente projeto.

##### A experiência do sistema PIESP/CrewAI como referência metodológica

O sistema descrito neste relatório é herdeiro direto de uma arquitetura desenvolvida para a Pesquisa de Investimentos Anunciados no Estado de São Paulo (PIESP), conduzida pela Fundação Seade em parceria com pesquisadores da PUC-SP. Naquele projeto, o framework CrewAI foi utilizado para orquestrar agentes responsáveis por coletar, filtrar e estruturar notícias sobre investimentos produtivos publicadas em veículos jornalísticos, tomando como referência a metodologia de clipping manual tradicional da pesquisa.

Os resultados obtidos demonstraram que sistemas baseados em arquiteturas multiagente com LLMs apresentam desempenho significativamente superior ao das abordagens tradicionais de busca por palavras-chave na tarefa de pré-filtragem semântica. Enquanto a metodologia PIESP processou 31.966 notícias para identificar 161 investimentos relevantes (taxa de compatibilidade de 0,5%), o sistema CrewAI identificou o mesmo volume de investimentos com taxa de compatibilidade de 25,3% sobre um conjunto 45 vezes menor de documentos processados (VILLELA; MINGARDO, 2025). Esse resultado evidencia uma diferença qualitativa: o sistema multiagente é capaz de realizar triagem semântica sofisticada sem que os critérios precisem ser formalizados como regras explícitas de programação.

A experiência PIESP evidenciou também as principais limitações da abordagem: dependência de supervisão humana para classificações em domínios abertos; sensibilidade à qualidade e ao tamanho do modelo de linguagem utilizado; variabilidade nos resultados entre execuções distintas com os mesmos inputs; e potencial de alucinação de dados factuais, que exige verificação humana dos resultados. O presente sistema incorpora as lições aprendidas, adotando critérios de classificação tripartidos e explicitamente definidos, saída em formato estruturado validado por schema Pydantic e instruções precisas de preenchimento que minimizam o risco de alucinação de campos factuais.

##### Arquiteturas multiagente e o framework CrewAI

Sistemas multiagente (*Multi-Agent Systems* — MAS) permitem decompor tarefas complexas em subtarefas coordenadas, executadas por unidades autônomas e especializadas que interagem entre si (JENNINGS; SYCARA; WOOLDRIDGE, 1998; WOOLDRIDGE, 2009). No contexto do processamento de linguagem natural e da inteligência artificial generativa, essa abordagem supera as limitações dos pipelines sequenciais monolíticos ao favorecer: (a) a especialização funcional — cada agente é configurado para uma tarefa específica, com ferramentas e critérios adequados à sua função; (b) o intercâmbio de resultados parciais — o output de um agente serve de input ao seguinte, permitindo refinamento progressivo; e (c) a modularidade — cada componente pode ser ajustado ou substituído sem necessidade de reformulação do sistema inteiro.

O framework CrewAI foi selecionado como base de desenvolvimento por apresentar maior adequação para cenários com dados heterogêneos e fluxos dinâmicos em comparação com os principais concorrentes (VENKADESH; DIVYA; KUMAR, 2024). A decisão foi embasada na análise comparativa de Chin e Ng (2024), que avaliou CrewAI, LangChain e AutoGen em critérios de facilidade de configuração, escalabilidade, suporte a processos hierárquicos e integração com APIs de LLMs. Em relação ao LangChain, o CrewAI oferece uma camada de abstração mais elevada para a definição de agentes e fluxos, reduzindo a quantidade de código necessária para implementar comportamentos complexos. Em relação ao AutoGen, que favorece interações conversacionais entre agentes, o CrewAI apresenta melhor suporte para fluxos orientados a tarefas com outputs estruturados — característica central do presente projeto.

A configuração do sistema CrewAI baseia-se principalmente na definição de arquivos YAML para agentes e tarefas, o que reduz a dependência de intervenções de engenharia de software avançadas e facilita a manutenção e adaptação do sistema por equipes multidisciplinares (CHIN; NG, 2024). Essa característica é especialmente relevante no contexto da Iniciação Científica, onde o pesquisador não necessariamente possui formação técnica em desenvolvimento de software, mas precisa ser capaz de compreender, ajustar e documentar o comportamento do sistema.

---

#### II.1.2 Metodologia: arquitetura e implementação do sistema

##### Visão geral da arquitetura

O sistema é implementado em Python 3.10+ e organizado segundo as convenções do framework CrewAI, com separação clara entre definição de agentes, tarefas, ferramentas e lógica de execução. A arquitetura é composta pelos seguintes módulos:

- **Três agentes especializados**: Pesquisador, Analista e Estruturador, cada um com papel, ferramentas e critérios de operação distintos;
- **Ferramentas de busca e geração de consultas**: *SerperDevTool* (busca via Google Search API), *DuckDuckGoSearchRun* (fallback gratuito), *ScrapeWebsiteTool* (extração de conteúdo de páginas) e *GerarConsultasBuscaTool* (ferramenta customizada para geração programática de consultas);
- **Modelos Pydantic v2**: formalização do schema de saída para validação estrutural do JSON gerado;
- **Módulo de execução** (`main.py`): ponto de entrada do sistema, com configurações parametrizadas e tratamento de saída.

O fluxo de execução é estritamente sequencial (`Process.sequential`): cada agente recebe como contexto o output do agente anterior, formando uma cadeia de processamento progressivo que vai da busca bruta à estruturação validada:

```
[main.py] → kickoff(inputs) → [Pesquisador] → [Analista] → [Estruturador] → output/galpaos_culturais.json
```

O processo sequencial é declarado na instanciação da *crew*, e o encadeamento entre tarefas é feito pela chave `context` nos arquivos YAML:

```python
# crew.py
@crew
def crew(self) -> Crew:
    return Crew(
        agents=self.agents,
        tasks=self.tasks,
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

##### Agente 1 — Pesquisador de Patrimônio Cultural Reutilizado

O Pesquisador é responsável pela busca e documentação de candidatos a galpões reutilizados na web aberta. Seu perfil é configurado com o papel de jornalista investigativo especializado em cultura urbana e patrimônio industrial, o que orienta o estilo de raciocínio e a estratégia de busca do LLM subjacente:

```yaml
# agents.yaml
pesquisador:
  role: >
    Pesquisador de Patrimônio Cultural Reutilizado
  goal: >
    Buscar e documentar galpões industriais, armazéns, fábricas e imóveis
    logísticos ou comerciais desativados que foram convertidos em espaços
    culturais no estado de São Paulo, coletando nome, localização, histórico
    de uso e fontes verificáveis para cada candidato encontrado.
  backstory: >
    Você é jornalista investigativo com 15 anos de experiência em cultura
    urbana e patrimônio industrial. [...] Você nunca inventa endereços ou
    nomes: se não encontrou, registra que não encontrou.
```

Em `crew.py`, o agente é instanciado com `max_iter=60`, permitindo até sessenta chamadas de ferramenta antes de encerrar:

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

**1. GerarConsultasBuscaTool** — ferramenta customizada que gera, de forma programática, até 30 consultas de busca em português brasileiro otimizadas para um município específico, combinando vocabulário controlado de tipos de imóvel, adjetivos de desativação, usos culturais e verbos de transformação:

```python
# search_tools.py
TIPOS_IMOVEL = ["galpão", "fábrica", "armazém", "depósito", "usina",
                "indústria", "hangar", "barracão"]
ADJETIVOS_DESATIVACAO = ["desativado", "abandonado", "desocupado",
                         "fechado", "desativada", "abandonada"]
USOS_CULTURAIS = ["centro cultural", "espaço cultural", "ateliê coletivo",
                  "galeria de arte", "hub criativo", "casa de shows",
                  "fábrica de cultura", "ocupação artística"]
VERBOS_TRANSFORMACAO = ["virou", "tornou-se", "se transformou em",
                        "foi convertido em", "recebeu", "abriga"]
```

**2. SerperDevTool / DuckDuckGoSearchRun** — executa as buscas web propriamente ditas, com configuração prioritária para o contexto brasileiro e carregamento condicional:

```python
# crew.py
def _search_tools(self) -> list:
    """Prioridade: SerperDevTool > DuckDuckGoSearchRun > sem busca web."""
    web_tools = _load_serper() or _load_duckduckgo()
    scraper = _load_scraper()
    query_generator = [GerarConsultasBuscaTool()]
    return query_generator + web_tools + scraper

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

**3. ScrapeWebsiteTool** — permite ao agente acessar URLs promissoras encontradas nas buscas e extrair o conteúdo completo das páginas para obtenção de detalhes adicionais.

A tarefa `pesquisa_task` instrui o agente por meio de prompt estruturado que detalha as etapas, exige ao menos dez buscas distintas e define o formato exato da saída:

```yaml
# tasks.yaml — pesquisa_task (trecho)
description: >
  ETAPAS DA PESQUISA:
  1. Use a ferramenta "Gerador de Consultas" para obter queries otimizadas.
  2. Execute ao menos 10 buscas distintas com diferentes combinações de termos.
  3. Para cada resultado promissor, acesse a URL e extraia mais detalhes.
  4. Não pare após os primeiros resultados — prossiga até atingir
     {limite_resultados} candidatos ou esgotar as palavras-chave disponíveis.

expected_output: >
  Lista numerada com NO MÍNIMO 10 candidatos e no máximo {limite_resultados}.
  Formato: N. NOME | MUNICÍPIO | ANTIGO USO | USO CULTURAL ATUAL | URL DA FONTE
```

##### Agente 2 — Analista de Relevância Cultural e Patrimônio Industrial

O Analista avalia criticamente cada candidato produzido pelo Pesquisador e determina sua relevância. Opera exclusivamente sobre o texto recebido via contexto compartilhado do CrewAI — sem ferramentas de busca, pois sua tarefa é classificatória, não coletora:

```yaml
# agents.yaml
analista:
  role: >
    Analista de Relevância Cultural e Patrimônio Industrial
  backstory: >
    Você é arquiteto com doutorado em patrimônio histórico industrial e vasta
    experiência em políticas culturais no estado de São Paulo. [...] Você é
    criterioso e objetivo: classifica como "relevante" apenas quando há
    evidência documental clara da mudança de uso. Quando faltam dados, você
    classifica como "parcialmente relevante" e indica o que falta confirmar.
```

A tarefa `analise_task` define três categorias de classificação com critérios explícitos:

| Classificação | Critérios |
|---|---|
| **relevante** | Imóvel claramente industrial/logístico; reconversão funcional real para uso cultural; evidência documental ou jornalística da transformação |
| **parcialmente relevante** | Indícios de reconversão com informações incompletas; uso misto; fonte não confirma explicitamente o antigo uso industrial |
| **não relevante** | Construído originalmente como espaço cultural; apenas reforma estética; localizado fora de SP; informação insuficiente |

O prompt inclui cláusula de "descarte automático" para teatros municipais, museus históricos sempre culturais e reformas de fachada sem mudança de uso. A exigência de justificativa obrigatória por candidato funciona como mecanismo implícito de *chain-of-thought*, melhorando a consistência das classificações e facilitando a revisão humana.

##### Agente 3 — Estruturador de Dados de Espaços Culturais

O Estruturador processa apenas os candidatos classificados como "relevante" ou "parcialmente relevante" e gera o arquivo JSON consolidado final, seguindo regras rígidas de preenchimento:

```yaml
# agents.yaml
estruturador:
  backstory: >
    Você é engenheiro de dados especializado em cadastros culturais.
    Você segue regras rígidas: preenche apenas campos com informação confirmada
    nas fontes, usa exatamente a string "não informado" para dados ausentes e
    nunca supõe ou extrapola. Você gera exclusivamente JSON puro e válido —
    sem texto adicional, sem blocos de código markdown, sem comentários fora
    do JSON. Seu output é sempre parseável por json.loads().
```

O arquivo de saída é definido no código Python:

```python
# crew.py
@task
def estruturacao_task(self) -> Task:
    return Task(
        config=self.tasks_config["estruturacao_task"],
        output_file="output/galpaos_culturais.json",
    )
```

Os nove campos obrigatórios por espaço identificado são:

| Campo | Descrição |
|---|---|
| `nome` | Nome oficial do espaço cultural |
| `endereco` | Endereço completo (logradouro, número, bairro) |
| `municipio` | Município no estado de São Paulo |
| `antigo_uso` | Uso original do imóvel antes da conversão |
| `uso_atual_cultural` | Tipo de uso cultural atual |
| `ano_reutilizacao` | Ano aproximado da conversão cultural |
| `fonte` | URL completa ou nome da fonte consultada |
| `relevancia` | `"relevante"` ou `"parcialmente relevante"` |
| `justificativa` | Frase curta sobre a evidência de reconversão |

##### Modelos de dados (Pydantic v2)

O arquivo `models.py` define dois modelos que formalizam o schema de saída do sistema:

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

Os campos `endereco` e `ano_reutilizacao` possuem valor padrão `"não informado"`, refletindo a expectativa de que essas informações frequentemente não estejam disponíveis nas fontes consultadas.

##### Módulo de execução (main.py)

O ponto de entrada do sistema expõe duas funções públicas:

**`run(municipios, palavras_chave, limite_resultados)`** — executa o sistema completo. Os valores padrão cobrem os dez maiores municípios do estado de São Paulo, vinte combinações de palavras-chave e um limite de trinta candidatos:

```python
# main.py
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

**`run_by_municipio(municipio, limite)`** — versão simplificada que executa a busca focada em um único município, útil para expansão incremental do banco de dados:

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

O fluxo interno de `run()` compreende: construção do dicionário de inputs com conversão de todos os valores para strings (compatibilidade com Jinja2 do CrewAI); instanciação e execução da *crew*; e leitura, validação e limpeza do arquivo de saída. A função `_validate_and_save_output()` trata a inserção indevida de blocos Markdown:

```python
# main.py
def _validate_and_save_output() -> dict | None:
    raw = OUTPUT_FILE.read_text(encoding="utf-8").strip()

    if raw.startswith("```"):
        lines = raw.splitlines()
        start = 1 if lines[0].startswith("```") else 0
        end = len(lines) - 1 if lines[-1].strip() == "```" else len(lines)
        raw = "\n".join(lines[start:end]).strip()

    try:
        data = json.loads(raw)
        OUTPUT_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return data
    except json.JSONDecodeError as exc:
        print(f"\n[AVISO] O arquivo de saída não é JSON válido: {exc}")
        return None
```

##### Ferramentas, dependências e configuração de ambiente

O sistema requer as seguintes variáveis de ambiente:

| Variável | Obrigatoriedade | Descrição |
|---|---|---|
| `OPENAI_API_KEY` | Obrigatória | Chave de acesso à API da OpenAI |
| `MODEL` | Opcional (padrão: `gpt-4o`) | Identificador do modelo LLM |
| `SERPER_API_KEY` | Recomendada | Chave para a API Serper/Google Search |

A escolha do modelo de linguagem é crítica para a qualidade dos resultados. A experiência do projeto PIESP mostrou que modelos menores ou versões mais leves como GPT-4o-mini apresentam desempenho insatisfatório em tarefas de classificação semântica aberta. O GPT-4o demonstrou o melhor equilíbrio entre custo, precisão e robustez para este tipo de aplicação.

A ferramenta `GerarConsultasBuscaTool` prevê ainda a ativação opcional de filtros de fonte para priorizar veículos confiáveis:

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
```

---

#### II.1.3 Resultados preliminares e avaliação do sistema

##### Execuções-piloto realizadas

Ao longo dos primeiros seis meses, foram realizadas oito execuções-piloto do sistema em diferentes configurações, totalizando a cobertura parcial de doze municípios do estado de São Paulo: São Paulo (capital), Campinas, Santos, Santo André, São Bernardo do Campo, Osasco, Ribeirão Preto, Sorocaba, São José dos Campos, Mogi das Cruzes, Americana e Franca. As execuções variaram em termos de modelo utilizado (GPT-4o e GPT-4o-mini), ferramenta de busca (SerperDevTool e DuckDuckGoSearchRun), limite de resultados (10 a 30 candidatos por execução) e conjunto de municípios cobertos.

Os resultados indicam que o sistema é capaz de identificar candidatos relevantes de forma consistente quando operado com GPT-4o e SerperDevTool. Em execuções de referência com esses componentes, a taxa de candidatos classificados como "relevante" ou "parcialmente relevante" em relação ao total retornado pelo Pesquisador ficou entre **60% e 75%** — significativamente superior à eficiência estimada de buscas manuais por palavras-chave em motor de busca convencional, que retornam proporção de 5% a 15% de resultados diretamente relevantes para o tema.

##### Exemplo representativo de output

A estrutura típica do arquivo JSON gerado pelo sistema em execução de referência:

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

Os campos padronizados permitem: georreferenciamento e visualização cartográfica dos espaços; análise da distribuição regional e municipal das reconversões; cruzamento com bases de dados de tombamento e patrimônio histórico; identificação de padrões temporais de reconversão por tipo de imóvel e uso cultural; e subsídio para políticas públicas de preservação e fomento à cultura.

##### Limitações identificadas e estratégias de mitigação

Com base nas execuções-piloto, as seguintes limitações foram confirmadas e mitigadas:

**Cobertura assimétrica por município.** Municípios com maior cobertura jornalística digital apresentam densidade de candidatos identificados significativamente superior à de municípios menores do interior. Estratégia de mitigação: uso de filtros `site:` para portais municipais e secretarias de cultura locais nas execuções de municípios do interior.

**Variabilidade entre execuções.** O caráter estocástico dos LLMs implica que execuções distintas com os mesmos inputs podem produzir listas parcialmente diferentes. Estratégia de mitigação: execuções múltiplas (ao menos três por município) e consolidação dos resultados por deduplicação e votação majoritária.

**Risco de alucinação em campos factuais.** Endereços e anos de inauguração são os campos mais suscetíveis à alucinação, especialmente quando a fonte não contém essas informações explicitamente. Estratégia de mitigação: verificação humana obrigatória de todos os campos `endereco` e `ano_reutilizacao` marcados como preenchidos antes da incorporação ao banco de dados definitivo.

**Custo por execução.** Uma execução completa com GPT-4o, SerperDevTool e `max_iter=60` para dez municípios consome em média entre 200.000 e 400.000 tokens, representando custo de aproximadamente US$ 2,00 a US$ 4,00. Esse custo precisa ser considerado no planejamento das execuções sistemáticas da segunda etapa.

---

### II.2 Cronograma de atividades para os próximos seis meses

O cronograma a seguir detalha as atividades previstas para o período de março a agosto de 2026, segunda e última etapa da bolsa PIBIC 2025/2026. As atividades estão organizadas em cinco eixos: (A) execução sistemática e expansão do banco de dados; (B) avaliação e aprimoramento do sistema; (C) validação humana e curadoria dos dados; (D) análises e produtos finais; e (E) elaboração do relatório final e produção científica.

| Mês | Eixo | Atividade |
|---|---|---|
| **Março/2026** | A | Execução sistemática do sistema para os 20 municípios paulistas com maior população, usando GPT-4o e SerperDevTool. Meta: ao menos 100 candidatos avaliados. |
| **Março/2026** | B | Análise qualitativa dos resultados das execuções-piloto e identificação de padrões de erro. Ajuste fino dos prompts dos agentes Pesquisador e Analista. |
| **Março/2026** | E | Submissão de resumo expandido ao Encontro de Iniciação Científica da PUC-SP. |
| **Abril/2026** | A | Expansão da cobertura para municípios do interior paulista com histórico industrial documentado (Americana, Franca, Sorocaba, Piracicaba, São Carlos, Araraquara). Meta: ao menos 80 candidatos adicionais avaliados. |
| **Abril/2026** | B | Implementação de execuções múltiplas por município (3 execuções por cidade) e desenvolvimento de rotina de deduplicação e consolidação dos resultados. |
| **Abril/2026** | C | Início da revisão humana dos candidatos classificados como "relevante": verificação de endereços, anos e fontes. |
| **Maio/2026** | A | Expansão para municípios da Região Metropolitana de São Paulo não cobertos anteriormente (Guarulhos, Mauá, Diadema, São Caetano do Sul, Barueri, Carapicuíba). |
| **Maio/2026** | B | Avaliação quantitativa do desempenho do sistema: cálculo de precisão e cobertura com base na revisão humana; comparação com busca manual como linha de base. |
| **Maio/2026** | C | Revisão humana dos candidatos "parcialmente relevantes": identificação de casos reclassificáveis como "relevantes" com busca complementar. |
| **Maio/2026** | D | Início do georreferenciamento dos espaços confirmados: geocodificação de endereços e produção de mapa preliminar de distribuição geográfica. |
| **Junho/2026** | A | Cobertura de municípios com histórico de ocupações culturais alternativas (Campinas, Santos, São José dos Campos, Jundiaí, Bauru). |
| **Junho/2026** | B | Testes com fontes alternativas de busca: portais de secretarias de cultura municipais e sites especializados em patrimônio industrial. |
| **Junho/2026** | C | Consolidação do banco de dados JSON com todos os espaços validados; documentação dos critérios de inclusão e exclusão aplicados na revisão humana. |
| **Junho/2026** | D | Análise estatística descritiva dos dados consolidados: distribuição por município, por tipo de antigo uso, por tipo de uso cultural atual e por período de reconversão. |
| **Julho/2026** | D | Produção de visualizações cartográficas e gráficas; identificação de padrões territoriais e temporais das reconversões. |
| **Julho/2026** | D | Análise comparativa dos resultados com dados disponíveis em bases institucionais (Secretaria de Cultura do Estado de SP, IPHAN). |
| **Julho/2026** | E | Redação do relatório final de IC: elaboração das seções de metodologia, resultados, discussão e conclusões; revisão bibliográfica complementar. |
| **Agosto/2026** | E | Finalização e entrega do relatório final. Submissão do artigo completo aos Anais do Encontro de IC da PUC-SP 2026. |
| **Agosto/2026** | E | Apresentação oral dos resultados no Encontro de Iniciação Científica da PUC-SP (agosto/2026). |

---

\newpage

---

## REFERÊNCIAS BIBLIOGRÁFICAS

CHIN, S. Y.; NG, K. W. Comparative of Multi-Agent System Frameworks: CrewAI, LangChain, and AutoGen. **Social Science Research Network (SSRN)**, [S. l.], n. 5367964, 2024. Disponível em: https://ssrn.com/abstract=5367964. Acesso em: 4 mar. 2026.

CREWAI. **CrewAI Framework Documentation**. [S. l.], 2025. Disponível em: https://docs.crewai.com. Acesso em: 4 mar. 2026.

JENNINGS, N. R.; SYCARA, K.; WOOLDRIDGE, M. A roadmap of agent research and development. **Autonomous Agents and Multi-Agent Systems**, [S. l.], v. 1, n. 1, p. 7-38, 1998.

VENKADESH, P.; DIVYA, S. V.; KUMAR, K. S. Unlocking AI Creativity: A Multi-Agent Approach with CrewAI. **Journal of Trends in Computer Science and Smart Technology**, [S. l.], v. 6, n. 4, p. 338-356, 2024.

VILLELA, T.; MINGARDO, L. **Metodologias de Coleta de Dados sobre Investimentos**: um estudo comparativo entre sistema multiagente e PIESP. São Paulo: Fundação Seade, 2025.

WOOLDRIDGE, M. **An Introduction to MultiAgent Systems**. 2. ed. Chichester: Wiley, 2009.
