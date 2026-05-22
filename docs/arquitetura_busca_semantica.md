# Arquitetura proposta: busca semantica para galpoes culturais

## Objetivo

Melhorar a confiabilidade da descoberta de links sobre galpoes, fabricas,
armazens e outros imoveis industriais reutilizados como espacos culturais no
estado de Sao Paulo.

A ideia principal e nao deixar o CrewAI atuar como motor de busca aberto. Em
vez disso, o sistema usa uma camada semantica para entender o alvo da pesquisa,
gerar consultas melhores, executar buscas com ferramentas deterministicas e
depois validar os resultados antes de entregar os links aos agentes.

## Problema observado

Quando o agente recebe uma tarefa ampla como "encontre galpoes culturais", ele
pode:

- retornar links inexistentes ou fracos;
- confundir anuncio imobiliario com caso cultural real;
- misturar aluguel, venda e logistica com reutilizacao cultural;
- depender demais do raciocinio do LLM para uma etapa que precisa de evidencia
  verificavel.

Por isso, a busca deve ser separada em etapas mais controladas.

## Pipeline sugerido

```text
Entrada do usuario
-> interpretacao semantica
-> expansao de termos
-> geracao de queries
-> busca externa via Serper, DuckDuckGo ou requests
-> coleta de URLs
-> deduplicacao
-> validacao das paginas
-> extracao estruturada
-> ranking semantico
-> resultado final com links reais
```

## Papel do CrewAI

O CrewAI deve ser usado principalmente para:

- interpretar a intencao da pesquisa;
- sugerir termos relacionados;
- avaliar se um resultado encontrado parece ser um caso cultural real;
- sintetizar e organizar os achados;
- justificar a relevancia de cada candidato.

O CrewAI nao deve ser o unico responsavel por encontrar URLs. Essa parte deve
ficar em uma camada de busca controlada, com API, requests, retry, filtros e
validacao HTTP.

## Camada semantica

A camada semantica recebe a consulta original e transforma em um objeto de
intencao. Exemplo:

```json
{
  "tema": "galpoes culturais",
  "tipos_imovel": ["galpao", "fabrica", "armazem", "barracao", "deposito"],
  "usos_culturais": ["espaco cultural", "centro cultural", "atelie coletivo", "galeria de arte", "hub criativo"],
  "transformacoes": ["virou", "foi convertido em", "se transformou em", "reutilizado", "requalificado"],
  "localizacao": "estado de Sao Paulo",
  "excluir": ["aluguel", "venda", "locacao", "condominio logistico"]
}
```

Essa estrutura evita que a busca dependa apenas de uma frase solta.

## Geracao de queries

A partir da intencao semantica, o sistema gera consultas objetivas:

```text
"antiga fabrica" "espaco cultural" "Sao Paulo" -aluguel -venda
"galpao" "virou espaco cultural" "Sao Paulo"
"armazem" "convertido em" "centro cultural" "Sao Paulo"
"patrimonio industrial" reutilizado cultura "Sao Paulo"
site:g1.globo.com galpao "espaco cultural" "Sao Paulo"
site:estadao.com.br "antiga fabrica" "centro cultural"
site:cultura.sp.gov.br galpao OR fabrica OR armazem cultura
```

As queries podem ser agrupadas por estrategia:

- transformacao de uso: "virou", "foi convertido", "se tornou";
- memoria industrial: "antiga fabrica", "patrimonio industrial";
- tipo de espaco cultural: "centro cultural", "atelie", "galeria";
- fonte confiavel: sites jornalisticos, institucionais e culturais;
- exclusao de ruido: `-aluguel`, `-venda`, `-locacao`.

## Busca externa

A etapa de busca deve ser feita por codigo previsivel, por exemplo:

- `SerperDevTool`, quando houver chave configurada;
- `duckduckgo_search.DDGS`, como fallback;
- `requests` ou `urllib` para validacao posterior das URLs;
- filtros locais para descartar dominios imobiliarios.

O objetivo e entregar ao agente um conjunto de resultados ja coletados, em vez
de pedir que ele "navegue" sozinho.

## Validacao e filtros

Antes de passar os resultados ao CrewAI, o sistema deve validar:

- se a URL responde com status HTTP valido;
- se o resultado nao e anuncio imobiliario;
- se o titulo ou trecho menciona uso cultural;
- se ha indicio de reutilizacao de imovel industrial;
- se a fonte e minimamente confiavel;
- se a URL ja apareceu antes.

Exemplo de criterios de descarte:

```text
Dominio contem: imovelweb, zapimoveis, vivareal, olx, quintoandar
Texto contem: galpao para alugar, galpao a venda, locacao de galpao
URL ausente ou status HTTP >= 400
```

## Extracao estruturada

Cada resultado aprovado deve ser transformado em um registro padronizado:

```json
{
  "nome": "Nome do espaco",
  "municipio": "Campinas",
  "tipo_imovel_original": "antiga fabrica",
  "uso_atual": "espaco cultural",
  "fonte": "https://...",
  "evidencia": "Trecho curto que sustenta a classificacao",
  "relevancia": "alta",
  "score": 0.87
}
```

Essa estrutura ajuda o relatorio final, a revisao humana e a reproducibilidade
da pesquisa.

## Ranking semantico

Depois da extracao, os resultados podem receber uma pontuacao:

```text
+ fonte jornalistica ou institucional confiavel
+ menciona claramente antigo uso industrial
+ menciona claramente uso cultural atual
+ informa municipio ou endereco
+ tem mais de uma fonte confirmando
- parece anuncio imobiliario
- menciona apenas aluguel, venda ou logistica
- link nao verificavel
```

O ranking final deve priorizar evidencia, nao apenas correspondencia de
palavras-chave.

## Esqueleto de implementacao

```python
class SemanticSearchPipeline:
    def run(self, user_query: str):
        intent = semantic_parser.parse(user_query)
        queries = query_builder.build(intent)
        urls = search_client.search_many(queries)
        urls = deduplicator.clean(urls)
        pages = scraper.fetch_many(urls)
        candidates = extractor.extract(pages)
        ranked = ranker.rank(candidates, intent)
        return ranked
```

## Integracao com o projeto atual

O projeto ja possui algumas pecas alinhadas com essa arquitetura:

- `main.py` executa buscas antes de iniciar os agentes;
- `search_tools.py` possui ferramenta para DuckDuckGo;
- `GerarConsultasBuscaTool` ja expande termos relacionados;
- ha filtros para remover anuncios imobiliarios;
- ha verificacao posterior de URLs.

O proximo passo natural seria organizar essas responsabilidades em modulos
menores:

```text
src/relatorio/search/semantic_parser.py
src/relatorio/search/query_builder.py
src/relatorio/search/search_client.py
src/relatorio/search/result_filter.py
src/relatorio/search/url_validator.py
src/relatorio/search/ranker.py
```

Isso deixaria o `main.py` mais limpo e faria a busca ficar mais facil de testar.

## MVP recomendado

1. Criar um `QueryIntent` com campos estruturados.
2. Criar um `SemanticQueryBuilder` que gere queries a partir desse intent.
3. Reaproveitar o DuckDuckGo e o Serper como clientes de busca.
4. Centralizar filtros de imoveis em um `ResultFilter`.
5. Guardar queries geradas, links aceitos e links rejeitados em JSON.
6. Passar ao CrewAI apenas resultados ja filtrados e rastreaveis.

## Beneficio esperado

Essa arquitetura torna o sistema mais confiavel porque separa claramente:

- raciocinio semantico;
- busca real na web;
- verificacao tecnica dos links;
- avaliacao qualitativa dos resultados;
- escrita do relatorio.

Com isso, o agente deixa de "inventar caminhos" e passa a trabalhar sobre uma
base de evidencias coletada por uma camada deterministica.
