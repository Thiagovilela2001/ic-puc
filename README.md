# Identificação de galpões culturais em São Paulo

Sistema de pesquisa assistida por agentes para localizar, verificar, classificar
e estruturar informações sobre galpões, fábricas, armazéns e outros imóveis de
origem industrial ou logística reutilizados como espaços culturais no estado de
São Paulo.

O projeto combina uma camada determinística de busca semântica com uma equipe
sequencial de agentes do CrewAI. A busca coleta URLs reais, elimina ruído
imobiliário, verifica páginas e registra evidências. Em seguida, os agentes
analisam os candidatos e produzem um JSON validado.

> **Aviso:** a execução consulta serviços externos e usa um modelo de linguagem.
> Ela pode consumir créditos da API configurada, levar vários minutos e produzir
> resultados diferentes conforme a disponibilidade das fontes na web.

## Sumário

- [O que o projeto faz](#o-que-o-projeto-faz)
- [Como o sistema funciona](#como-o-sistema-funciona)
- [Requisitos](#requisitos)
- [Instalação rápida com UV](#instalação-rápida-com-uv)
- [Configuração do arquivo `.env`](#configuração-do-arquivo-env)
- [Como executar](#como-executar)
- [Como pesquisar um município específico](#como-pesquisar-um-município-específico)
- [Como personalizar uma pesquisa](#como-personalizar-uma-pesquisa)
- [Arquivos gerados](#arquivos-gerados)
- [Estrutura do JSON final](#estrutura-do-json-final)
- [Resultados e relatórios versionados](#resultados-e-relatórios-versionados)
- [Cache e repetição de buscas](#cache-e-repetição-de-buscas)
- [Testes](#testes)
- [Comandos avançados do CrewAI](#comandos-avançados-do-crewai)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Como alterar agentes, tarefas e critérios](#como-alterar-agentes-tarefas-e-critérios)
- [Solução de problemas](#solução-de-problemas)
- [Cuidados com segurança, custo e qualidade](#cuidados-com-segurança-custo-e-qualidade)

## O que o projeto faz

A aplicação:

1. recebe um estado, município ou lista de municípios;
2. interpreta o escopo como uma intenção de busca estruturada;
3. expande palavras-chave em consultas específicas;
4. pesquisa pela Serper API ou pelo DuckDuckGo;
5. remove anúncios de aluguel, venda e outros resultados imobiliários;
6. elimina URLs duplicadas;
7. acessa as páginas candidatas e extrai texto visível;
8. exige sinais de uso industrial anterior, transformação e uso cultural;
9. agrupa evidências relacionadas ao mesmo candidato;
10. entrega apenas os candidatos filtrados à equipe de agentes;
11. classifica cada espaço como relevante, parcialmente relevante ou não
    relevante;
12. produz e valida o arquivo `output/galpaos_culturais.json`;
13. verifica novamente as URLs do resultado final e remove fontes inacessíveis;
14. salva uma auditoria completa da busca em
    `output/busca_semantica.json`.

O escopo padrão cobre o estado de São Paulo e limita a coleta a 30 candidatos.

## Como o sistema funciona

Fluxo resumido:

```text
Municípios e palavras-chave
        |
        v
Interpretação semântica determinística
        |
        v
Geração de consultas
        |
        v
Serper API ou DuckDuckGo
        |
        v
Deduplicação e filtro de anúncios
        |
        v
Download e validação das páginas
        |
        v
Ranking e agrupamento de evidências
        |
        v
Pesquisador -> Analista -> Estruturador
        |
        v
Validação Pydantic e verificação das URLs
        |
        v
JSON final + JSON de auditoria
```

### 1. Camada de busca semântica

A classe `SemanticSearchPipeline` executa a parte rastreável da pesquisa antes
dos agentes:

- `SemanticParser` transforma municípios e consultas iniciais em uma intenção;
- `SemanticQueryBuilder` cria consultas sobre transformação de uso, patrimônio
  industrial e fontes prioritárias;
- `SearchClient` usa Serper quando `SERPER_API_KEY` está disponível;
- sem Serper, `SearchClient` usa DuckDuckGo gratuitamente;
- `ResultFilter` rejeita domínios imobiliários, anúncios e resultados sem sinais
  semânticos suficientes;
- `PageFetcher` acessa as páginas e extrai até 4.000 caracteres de texto visível;
- `CandidateBuilder` agrupa evidências aprovadas;
- `SearchRunReport` grava consultas, aceitos, rejeitados, erros, métricas e
  horários da execução.

No filtro final, um resultado precisa apresentar:

- algum tipo de imóvel industrial, logístico ou comercial;
- algum uso cultural;
- evidência de transformação, reconversão, patrimônio ou desativação;
- uma página acessível e tecnicamente validada.

### 2. Equipe de agentes

Depois da busca, o CrewAI executa três agentes em sequência:

1. **Pesquisador:** lê as evidências coletadas e identifica candidatos.
2. **Analista:** classifica todos os candidatos segundo os critérios da pesquisa.
3. **Estruturador:** converte os casos aprovados para o schema JSON final.

Por padrão, o agente pesquisador não faz novas buscas abertas. Ele trabalha com
os links já coletados pela camada semântica. Isso reduz a chance de URLs
inventadas ou candidatos sem rastreabilidade.

### 3. Validação final

O resultado do estruturador é validado pelo modelo Pydantic
`RelatorioGalpoesCulturais`. O campo `total` precisa ser igual ao número de
elementos em `espacos_culturais`.

Depois disso, o programa testa cada URL final. Registros sem URL ou com URL
inacessível são removidos, o total é recalculado e o JSON é salvo novamente.

## Requisitos

- Git;
- Python 3.10, 3.11, 3.12 ou 3.13;
- acesso à internet;
- uma chave de API compatível com o modelo usado pelo CrewAI;
- UV, recomendado para instalar e executar o ambiente;
- Serper API opcional, mas recomendada para buscas mais estáveis.

O projeto fixa `crewai[tools]==1.9.3` e aceita Python `>=3.10,<3.14`.

## Instalação rápida com UV

### 1. Clonar o repositório

```bash
git clone https://github.com/Thiagovilela2001/ic-puc.git
cd ic-puc
```

### 2. Instalar o UV

Se o UV ainda não estiver instalado:

```bash
python -m pip install --upgrade uv
```

Confirme a instalação:

```bash
uv --version
```

### 3. Instalar o Python e as dependências

O Python 3.12 é uma escolha segura para este projeto:

```bash
uv python install 3.12
uv sync --python 3.12
```

O comando `uv sync`:

- cria a pasta local `.venv`;
- instala o projeto em modo executável;
- instala CrewAI, DuckDuckGo Search, python-dotenv e dependências transitivas;
- usa `pyproject.toml` e `uv.lock` para resolver o ambiente.

Não é necessário ativar manualmente o ambiente virtual ao usar comandos
iniciados por `uv run`.

### Instalação alternativa com `venv` e `pip`

No Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

No Linux ou macOS:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Configuração do arquivo `.env`

Crie um arquivo chamado `.env` na raiz do repositório, no mesmo diretório de
`pyproject.toml`.

Exemplo mínimo:

```dotenv
OPENAI_API_KEY=sua_chave_aqui
MODEL=gpt-4o
```

Configuração recomendada:

```dotenv
OPENAI_API_KEY=sua_chave_aqui
MODEL=gpt-4o
SERPER_API_KEY=sua_chave_serper_aqui
CREWAI_ENABLE_AGENT_SEARCH=0
```

### Variáveis disponíveis

| Variável | Obrigatória | Função |
| --- | --- | --- |
| `OPENAI_API_KEY` | Sim, na configuração padrão | Autentica o modelo usado pelos agentes do CrewAI. |
| `MODEL` | Não | Define o modelo selecionado pelo ambiente do CrewAI. Se omitida, vale a configuração padrão do provedor. |
| `SERPER_API_KEY` | Não | Ativa buscas pelo Google via Serper. Sem ela, o sistema usa DuckDuckGo. |
| `CREWAI_ENABLE_AGENT_SEARCH` | Não | Com valor `1`, permite busca aberta adicional dentro do agente pesquisador. O padrão é desativado. |

O `.env` já está listado no `.gitignore`. Nunca substitua os exemplos acima por
chaves reais dentro do README, código, commit ou issue.

## Como executar

Execute todos os comandos a partir da raiz do repositório.

### Opção recomendada

```bash
uv run relatorio
```

### Opção equivalente pela CLI do CrewAI

```bash
uv run crewai run
```

### Opção pelo módulo Python

```bash
uv run python -m relatorio.main
```

Durante a execução, o terminal mostra:

- número de consultas geradas;
- mecanismo de busca escolhido;
- consultas atendidas pelo cache;
- quantidade de resultados brutos;
- resultados aceitos e rejeitados;
- páginas verificadas;
- agentes e tarefas em andamento;
- URLs removidas na validação final;
- resumo dos espaços incluídos.

Ao terminar, consulte:

```text
output/busca_semantica.json
output/galpaos_culturais.json
```

Cada nova execução substitui esses dois arquivos. Faça uma cópia ou um commit
antes de executar novamente se precisar preservar uma coleta anterior.

## Como pesquisar um município específico

Abra o interpretador Python dentro do ambiente:

```bash
uv run python
```

Depois execute:

```python
from relatorio.main import run_by_municipio

resultado = run_by_municipio("Campinas", limite=8)
print(resultado)
```

`run_by_municipio` cria consultas específicas sobre galpões, antigas fábricas,
armazéns, reconversão industrial e hubs criativos na cidade informada.

O parâmetro `limite` controla o máximo de candidatos entregue aos agentes. Ele
não é o número garantido de registros finais: candidatos podem ser rejeitados
pelos filtros ou pela análise.

## Como personalizar uma pesquisa

Use a função `run` diretamente:

```python
from relatorio.main import run

resultado = run(
    municipios=["Campinas", "Santos", "Sorocaba"],
    palavras_chave=[
        '"antiga fábrica" "centro cultural" Campinas',
        '"armazém" "foi convertido em" cultura Santos',
        '"patrimônio industrial" reutilizado Sorocaba',
    ],
    limite_resultados=20,
)
```

Parâmetros:

| Parâmetro | Tipo | Padrão | Efeito |
| --- | --- | --- | --- |
| `municipios` | `list[str]` | `["estado de São Paulo"]` | Define a área geográfica priorizada. |
| `palavras_chave` | `list[str]` | Consultas definidas em `main.py` | Fornece consultas-semente para a expansão semântica. |
| `limite_resultados` | `int` | `30` | Limita os candidatos analisados pela equipe e influencia o total máximo de páginas verificadas. |

Exemplo completo no interpretador:

```bash
uv run python
```

```python
from relatorio.main import run

dados = run(
    municipios=["Ribeirão Preto"],
    palavras_chave=[
        '"antiga fábrica" "espaço cultural" "Ribeirão Preto"',
        '"galpão" "virou" "centro cultural" "Ribeirão Preto"',
    ],
    limite_resultados=10,
)

if dados:
    print(f"{dados['total']} espaços mantidos no resultado final")
```

## Arquivos gerados

### `output/busca_semantica.json`

Auditoria técnica da busca anterior aos agentes. Contém:

| Campo | Conteúdo |
| --- | --- |
| `intent` | Municípios, tipos de imóvel, usos culturais, transformações e exclusões. |
| `queries` | Todas as consultas executadas. |
| `query_origins` | Indica se cada consulta era semente ou foi gerada. |
| `accepted` | Evidências aprovadas no filtro final. |
| `rejected` | Resultados recusados e respectivos motivos. |
| `candidates` | Evidências agrupadas por candidato provável. |
| `errors` | Falhas de busca, rede ou parsing. |
| `started_at` e `finished_at` | Horários da coleta. |
| `duration_seconds` | Duração da camada semântica. |
| `raw_hits_total` | Total bruto devolvido pelo mecanismo de busca. |
| `unique_hits_total` | Total depois da deduplicação. |
| `fetched_pages_total` | Páginas acessadas para validação. |
| `cache_hits_total` | Consultas atendidas pelo cache local. |
| `search_source` | `serper` ou `duckduckgo`. |

Use esse arquivo para entender por que um link entrou ou foi rejeitado.

### `output/galpaos_culturais.json`

Resultado consolidado depois da análise dos agentes, validação Pydantic e
verificação final das URLs. Este é o arquivo indicado para análise, importação
em banco de dados ou geração de relatórios.

### `output/cache_busca/`

Cache local de pesquisas e páginas:

```text
output/cache_busca/search/
output/cache_busca/pages/
```

O cache não é versionado no Git.

## Estrutura do JSON final

Formato resumido:

```json
{
  "espacos_culturais": [
    {
      "nome": "Nome do espaço",
      "endereco": "Logradouro, número e bairro",
      "municipio": "Município",
      "antigo_uso": "Uso anterior do imóvel",
      "uso_atual_cultural": "Uso cultural atual",
      "ano_reutilizacao": "Ano ou não informado",
      "fonte": "https://fonte.example",
      "relevancia": "relevante",
      "justificativa": "Evidência resumida da reconversão."
    }
  ],
  "total": 1,
  "municipios_pesquisados": [
    "Município"
  ],
  "data_coleta": "YYYY-MM-DD"
}
```

Regras:

- `relevancia` aceita `relevante`, `parcialmente relevante` ou
  `não relevante`;
- o JSON final deve conter apenas casos relevantes ou parcialmente relevantes;
- dados ausentes usam a string `não informado`;
- `total` precisa corresponder ao tamanho de `espacos_culturais`;
- `fonte` deve ser uma URL verificável;
- `data_coleta` usa o formato `YYYY-MM-DD`.

## Resultados e relatórios versionados

O repositório contém uma coleta pronta e os documentos produzidos na pesquisa:

- [galpões culturais identificados](output/galpaos_culturais.json);
- [auditoria completa da busca semântica](output/busca_semantica.json);
- [relatório final de galpões culturais](docs/relatorios/relatorio_final_galpaos_culturais.md);
- [relatório de galpões culturais](docs/relatorios/relatorio_galpaos_culturais.md);
- [versões anteriores dos relatórios](docs/relatorios/versoes/);
- [documento de arquitetura da busca semântica](docs/arquitetura_busca_semantica.md).

Os arquivos Markdown em `docs/relatorios/` são documentos versionados. A
execução normal do programa gera os dois JSONs, mas não reescreve
automaticamente esses relatórios Markdown.

## Cache e repetição de buscas

O cache evita repetir consultas e downloads idênticos:

- resultados da Serper e do DuckDuckGo ficam em `cache_busca/search`;
- conteúdo das páginas fica em `cache_busca/pages`;
- a chave do cache considera mecanismo, consulta e limite por consulta;
- uma segunda execução com os mesmos parâmetros tende a ser mais rápida.

Para obrigar uma coleta totalmente nova, remova somente a pasta:

```text
output/cache_busca/
```

No Windows PowerShell:

```powershell
Remove-Item -LiteralPath .\output\cache_busca -Recurse
```

No Linux ou macOS:

```bash
rm -rf ./output/cache_busca
```

Confirme o caminho antes de executar. A remoção apaga apenas o cache; não apaga
os dois JSONs finais.

## Testes

Use o executor `unittest` dentro do ambiente do projeto:

```bash
uv run python -m unittest discover -s tests -v
```

O conjunto atual verifica:

- geração e origem das consultas;
- rejeição de resultado sem URL validada;
- descarte de anúncios imobiliários;
- extração de texto visível de páginas HTML;
- montagem de candidatos pelo pipeline.

Resultado esperado:

```text
Ran 5 tests

OK
```

Evite executar apenas `pytest` globalmente. Se o pacote local não estiver no
ambiente global, ele pode produzir `ModuleNotFoundError: No module named
'relatorio'` mesmo quando o projeto está instalado corretamente na `.venv`.

## Comandos avançados do CrewAI

### Treinamento

```bash
uv run crewai train -n 5 -f training_data.pkl
```

- `-n` define o número de iterações;
- `-f` define o arquivo que armazena os dados de treinamento.

### Replay de uma tarefa

```bash
uv run crewai replay -t ID_DA_TAREFA
```

Use um ID registrado por uma execução anterior do CrewAI.

### Avaliação da equipe

```bash
uv run crewai test -n 2 -m MODELO_OPENAI
```

- `-n` define o número de iterações;
- `-m` define o modelo OpenAI usado na avaliação.

Esses comandos podem fazer múltiplas chamadas ao modelo e consumir mais créditos
que uma execução comum.

## Estrutura do projeto

```text
.
|-- README.md
|-- pyproject.toml
|-- requirements.txt
|-- uv.lock
|-- docs/
|   |-- arquitetura_busca_semantica.md
|   `-- relatorios/
|       |-- relatorio_final_galpaos_culturais.md
|       |-- relatorio_galpaos_culturais.md
|       `-- versoes/
|-- knowledge/
|   `-- user_preference.txt
|-- output/
|   |-- busca_semantica.json
|   |-- galpaos_culturais.json
|   `-- cache_busca/
|-- src/
|   `-- relatorio/
|       |-- main.py
|       |-- crew.py
|       |-- models.py
|       |-- config/
|       |   |-- agents.yaml
|       |   `-- tasks.yaml
|       |-- search/
|       |   |-- cache.py
|       |   |-- candidate_builder.py
|       |   |-- page_fetcher.py
|       |   |-- pipeline.py
|       |   |-- query_builder.py
|       |   |-- result_filter.py
|       |   |-- search_client.py
|       |   |-- semantic_parser.py
|       |   |-- types.py
|       |   |-- url_validator.py
|       |   `-- vocabulary.py
|       `-- tools/
|           `-- search_tools.py
`-- tests/
    `-- test_search_pipeline.py
```

## Como alterar agentes, tarefas e critérios

### Alterar os agentes

Edite:

```text
src/relatorio/config/agents.yaml
```

Esse arquivo define papel, objetivo e contexto profissional de:

- `pesquisador`;
- `analista`;
- `estruturador`.

### Alterar as tarefas

Edite:

```text
src/relatorio/config/tasks.yaml
```

Esse arquivo define:

- campos exigidos de cada candidato;
- critérios de classificação;
- regras de descarte;
- estrutura esperada do JSON;
- dependências entre as três tarefas.

### Alterar consultas padrão e limites

Edite:

```text
src/relatorio/main.py
```

Principais constantes:

- `DEFAULT_MUNICIPIOS`;
- `DEFAULT_PALAVRAS_CHAVE`;
- `DEFAULT_LIMITE`;
- `OUTPUT_DIR`;
- `OUTPUT_FILE`;
- `CACHE_DIR`.

### Alterar vocabulário e filtros

Edite:

```text
src/relatorio/search/vocabulary.py
src/relatorio/search/result_filter.py
```

Esses módulos controlam:

- tipos de imóvel aceitos;
- usos culturais;
- verbos de transformação;
- sinais de patrimônio;
- termos imobiliários;
- domínios bloqueados;
- fontes prioritárias;
- pontuação e condições mínimas de aprovação.

### Alterar mecanismo de busca

Edite:

```text
src/relatorio/search/search_client.py
```

O cliente atual prioriza Serper e usa DuckDuckGo como fallback.

## Solução de problemas

### `ModuleNotFoundError: No module named 'relatorio'`

Execute pelo UV:

```bash
uv sync
uv run python -c "import relatorio; print(relatorio.__file__)"
```

Depois rode:

```bash
uv run relatorio
```

O erro costuma ocorrer quando o Python global é usado no lugar da `.venv`.

### `crewai` não foi encontrado

Não execute `crewai` diretamente. Use:

```bash
uv run crewai run
```

Se ainda falhar:

```bash
uv sync
```

### Erro de autenticação do modelo

Confira:

1. se `.env` está na raiz do projeto;
2. se `OPENAI_API_KEY` está escrita corretamente;
3. se não há espaços antes do nome da variável;
4. se a conta possui acesso e saldo para o modelo escolhido;
5. se o modelo definido em `MODEL` é compatível com a chave.

### Serper não é usada

O programa só escolhe Serper quando `SERPER_API_KEY` existe no ambiente.
Confirme a variável sem imprimir seu valor:

No Windows PowerShell:

```powershell
if ($env:SERPER_API_KEY) { "SERPER_API_KEY carregada" }
```

Se a chave não estiver configurada, o fallback DuckDuckGo é esperado.

### DuckDuckGo retorna poucos resultados ou bloqueia requisições

Possíveis causas:

- limitação temporária de requisições;
- indisponibilidade de rede;
- consultas muito específicas;
- bloqueio regional;
- falha do serviço externo.

Soluções:

- aguarde e execute novamente;
- configure `SERPER_API_KEY`;
- revise `output/busca_semantica.json`;
- reduza o número de consultas-semente;
- mantenha o cache para evitar chamadas repetidas.

### O JSON final ficou vazio ou com poucos casos

Inspecione em `output/busca_semantica.json`:

- `errors`;
- `accepted`;
- `rejected`;
- motivos registrados em cada item rejeitado;
- `search_source`;
- `raw_hits_total`;
- `fetched_pages_total`.

Poucos casos podem ser resultado correto: o filtro exige evidência simultânea de
imóvel industrial, transformação, uso cultural e página acessível.

### Um resultado desapareceu do JSON final

Possíveis motivos:

- foi classificado como não relevante;
- não apresentou fonte;
- a URL deixou de responder;
- o servidor rejeitou a validação HTTP;
- os campos não atenderam ao schema;
- o registro foi considerado duplicado.

Consulte o JSON de auditoria e a saída do terminal.

### Caracteres acentuados aparecem incorretamente

Os arquivos do projeto usam UTF-8. Configure o editor para UTF-8 e evite salvar
os YAMLs, Markdown ou JSONs em ANSI/Windows-1252.

No PowerShell, use `Get-Content -Encoding utf8` ao inspecionar arquivos.

## Cuidados com segurança, custo e qualidade

- Nunca publique o `.env`.
- Nunca registre chaves em Markdown, JSON, logs ou capturas de tela.
- Verifique o custo do modelo antes de aumentar limites ou executar treinamento.
- Serper e o provedor do modelo podem aplicar cotas e cobrança.
- O cache pode conter trechos de páginas públicas; revise-o antes de compartilhar.
- Os JSONs versionados contêm URLs e evidências coletadas da web.
- Links, páginas e classificações podem ficar desatualizados.
- A validação automática reduz erros, mas não substitui revisão humana.
- Confirme manualmente nome, endereço, uso anterior, uso cultural e fonte antes
  de usar os dados em publicação acadêmica.
- Preserve uma cópia dos resultados importantes antes de nova execução.

## Autor

Thiago Vilela — projeto de iniciação científica sobre reutilização cultural de
imóveis industriais no estado de São Paulo.
