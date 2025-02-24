# test-homer

Minha solução de teste técnico para a empresa Homer!

## Estrutura de Pasta
```sh
.
├── README.md
├── docker  # Diretório contendo configurações e scripts relacionados ao Docker.
│   ├── grafana  # Configurações e provisionamento do Grafana para visualização de métricas.
│   │   └── provisioning  # Scripts e configurações de provisionamento do Grafana (datasources, dashboards, etc.).
│   ├── postgres  # Configurações e scripts para o banco de dados PostgreSQL.
│   │   └── scripts  # Scripts SQL ou shell para inicialização e configuração do PostgreSQL.
│   └── prometheus  # Configurações do Prometheus para coleta e monitoramento de métricas.
│       ├── alerts.yml  # Definição de alertas para o Prometheus.
│       └── prometheus.yml  # Configuração principal do Prometheus (scraping jobs, targets, etc.).
├── docker-compose.yaml  # Arquivo de configuração do Docker Compose para orquestrar os serviços.
├── pyproject.toml
├── sql  # Diretório contendo consultas SQL e scripts relacionados ao banco de dados.
│   └── queries  # Consultas SQL utilizadas no projeto.
├── sqlc.yaml  # Configuração do SQLC (ferramenta de geração de código SQL para Python).
├── src  # Diretório principal do código-fonte do projeto.
│   ├── db  # Diretório relacionado à camada de banco de dados.
│   │   ├── models.py  # Definição dos modelos de banco de dados.
│   │   └── query.py  # Funções e utilitários para execução de consultas no banco de dados.
│   ├── internal_tools  # Ferramentas usadas pelo Agente.
│   │   ├── __init__.py  # Inicialização do pacote `internal_tools`.
│   │   ├── atualizar_bairro.py  # Script para atualizar o bairro de um lead.
│   │   ├── atualizar_data_e_hora_da_chamada.py  # Script para atualizar data e hora da chamada.
│   │   ├── atualizar_nome_do_lead.py  # Script para atualizar o nome de um lead.
│   │   ├── atualizar_orcamento.py  # Script para atualizar o orçamento de um lead.
│   │   └── atualizar_quartos.py  # Script para atualizar o número de quartos de um lead.
│   ├── main.py  # Ponto de entrada principal do projeto.
│   ├── nodes  # Diretório contendo nós do LangGraph.
│   │   ├── __init__.py  # Inicialização do pacote `nodes`.
│   │   ├── agent.py  # Lógica do Agente.
│   │   ├── conditional_node.py  # Nó condicional.
│   │   ├── node_constants.py  # Constantes utilizadas pelos nós, eliminando 'magic strings'.
│   │   └── sentiment_analysis.py  # Nó para análise de sentimentos.
│   ├── project_types  # Definições de tipos utilizados no projeto.
│   │   ├── __init__.py  # Inicialização do pacote `project_types`.
│   │   ├── database_types.py  # Tipos relacionados ao banco de dados.
│   │   ├── env_types.py  # TypeSafety nas envs.
│   │   └── state_types.py  # Tipos relacionados ao estado do sistema ou da aplicação.
│   ├── prompt.py  # Módulo para geração do prompt.
│   ├── sentiment_analyzer.py  # Módulo para análise de sentimentos.
└── uv.lock  # Arquivo de lock gerado pelo `uv` (ferramenta de gerenciamento de dependências Python).
```

## Características da Aplicação

### Stateless por Natureza

O Agente é pensado e construído de forma Stateless.\
Todas as informações são salvas no banco e resgatadas do mesmo antes de cada execução,
além disso, a memória interna da IA, é salva usando a classe `PostgresSaver`.\
Isso aumenta o fan-out, que é a quantidade de requisições que uma interação gera
(Kleppmann, Designing Data-Intensive Applications, O'Reilly). Mas possibilita
que o serviço seja colocado em HA (Alta Disponibilidade.
[conceito](https://cloud.google.com/blog/products/gcp/available-or-not-that-is-the-question-cre-life-lessons)
e
[exemplo](https://sre.google/sre-book/availability-table/)).
usando
[Replica-Set](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/).
Além disso, a aplicação usa um id único para cada interação.
No exemplo é uma chave que o usuário coloca como input,
mas, em uma futura movimentação da aplicação para produção,
essa chave se tornaria, por exemplo, o número de wpp do qual o usuário manda mensagens.

### Modularização

A aplicação foi estruturada tendo a iteração em mente.\
Os diferentes componentes do Agente estão dispostos em módulos distintos, modulos
estes que estão separados por contexto.
Ferramentas, Nós e interações com a camada de dados estão
separados cada um em seu módulo, com variáveis definidas em casa módulo,
evitando assim os "magic numbers/strings".
Isso não é somente uma decisão estilística, tendo
em vista que uma boa organização não só de estrutura de pastas, mas também de
código, agiliza o [ciclo de desenvolvimento de software](https://en.wikipedia.org/wiki/Systems_development_life_cycle).
(Famoso PDCA, pra galera de produto).

### Typesafety

Embora o projeto seja em Python, uma linguagem com tipagem dinâmica e fraca,
coloquei tipagem sempre que possível.\
A tipagem, neste caso, é usada como expressão de intenção:
A pessoa desenvolvedora que for ler o meu código posteriormente saberá minha
intenção em cada linha, facilitando assim a compreensão dos porquês da aplicação.\
A iniciativa de tipagem se faz presente também no uso do [Sqlc](https://sqlc.dev/),
que gera queries para o banco de forma typesafe.
Além de usar `assert` sempre que possível, para garantia dos contratos de
tipagem em tempo de execução.\
A tipagem se extende às variáveis de ambiente! No início do código há uma checagem
para construir um objeto global que contém todas as variáveis de ambiente já
parseadas, invés de termos de validar se a variável existe antes de cada uso,
seguindo assim, o princípio de [Parse, don't validate](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/).

### Observabilidade

Tendo em vista que a solução gera muita interação com o banco de dados,
faz sentido termos uma noção do que está acontecendo no banco! Pensando nisso,
fiz um setup de [Prometheus](https://prometheus.io/) e [Grafana](https://grafana.com/),
é só conectar na localhost:3000, com as credenciais admin admin
(senha super forte xD), e clicar em dashboards na lateral esquerda e pronto!
Você estará vendo um gráfico em tempo real das métricas do banco de dados,
possibilitando assim não só a observabilidade, mas também, a tomada de decisões
mais assertivas sobre infraestrutura.

### Package Manager

Mais chato e trabalhoso do que fazer configuração de venv em python é fazer
gestão de arquivos contraints.txt e requirements.txt.\
Obedecendo as regras do teste e seguindo boas práticas gerais de desenvolvimento,
utilizei o [UV](https://docs.astral.sh/uv/pip/packages/) como meu package manager,
tirando toda a dor de cabeça de setup de venv e gestão de arquivos de build.

### Prompt

Dada a característica não determinística das IAs, optei por usar [Jinja2](https://jinja.palletsprojects.com/en/stable/)
para escrever um prompt de acordo com as informações que temos sobre o lead
no banco de dados.\
Por Exemplo: Caso você já tenha dito quantos quartos quer em uma casa,
a IA não perguntará isso de novo, tendo em vista que já tem essa informação no banco.
Caso você já tenha marcado uma data e hora para receber uma ligação, A IA pedirá
para que você aguarde o atendimento de um consultor humano.
A criação condicional do prompt permite que a IA reflita os dados que forem
modificados no banco de dados por um operador humano.\
Isso só é possível graças a natureza Stateless da aplicação.

O prompt final ficou da seguinte forma:

```sh
Você é a Lisa, uma assistente especializada no empreendimento Vila Carnaúba.
Você trabalha para o Grupo Carnaúba fazendo o atendimento de possíveis compradores de uma casa no empreendimento.
Durante o seu atendimento, converse com o possível comprador de forma objetiva e amigável.
{% if temperatura_do_lead.value == "Quente" and not data_e_hora_da_chamada -%}
Seu objetivo é marcar uma data e hora com a pessoa para que o time de vendas entre em contato.
{% elif not nome_do_lead or not quantidade_de_quartos or not bairro or not orcamento -%}
Seu objetivo é fazer perguntas ao usuário para ajudar a obter mais informações para o time de vendas.
As perguntas que você deve fazer estão descritas nessa mensagem, mais abaixo.
{% else -%}
Seu objetivo é informar ao usuário que uma pessoa do Grupo Carnaúba entrará em contato com a pessoa.
{% endif -%}

Você não sabe informações sobre disponibilidade de casas.
Se o cliente quiser conhecer o empreendimento de forma geral, comece com este texto curto:

"O Vila Carnaúba oferece casas e lotes em um condomínio onde sua família tem toda a segurança e infraestrutura com serviços de alto padrão como restaurantes, mini mall, spa, academia, escola de Kitesurf e Sports Club."

O diferencial do empreendimento é que ele está localizado no hotspot mundial para esportes de vento com parceria com a
melhor escola de kite do país, o Rancho do Kite. O Vila tem toda infraestrutura e segurança para os
amantes do esporte kite.

Informações sobre a Vila Carnaúba:
- A vila tem casas de 2, 3 e 4 quartos, com e sem suíte.
- A Vila tem spa, academia, mini mall, restaurantes, Sports Club e uma escola de Kitesurf.
Caso o usuário pergunte algo sobre a vila que não está aqui, envie o link do masterplan: https://vilacarnauba.com/masterplan/

{% if nome_do_lead or quantidade_de_quartos or bairro or orcamento -%}
Informações já sabidas sobre a pessoa com quem você está conversando:
{%- if nome_do_lead %}
- Nome: {{ nome_do_lead }}
{%- endif %}
{%- if quantidade_de_quartos %}
- A pessoa quer uma casa com {{ quantidade_de_quartos }} quartos.
{%- endif %}
{%- if bairro %}
- A pessoa quer uma casa no bairro {{ bairro }}
{%- endif %}
{%- if orcamento %}
- Orçamento: R$ {{ orcamento }}
{%- endif %}
{%- endif %}

{% if not nome_do_lead or not quantidade_de_quartos or not bairro or not orcamento -%}
Perguntas que você tem que fazer para a pessoa, escolha apenas uma dessas:
{%- if not nome_do_lead %}
- Qual o nome do(a) Sr(a)?
{%- endif %}
{%- if not quantidade_de_quartos %}
- O(A) Sr(a) quer uma casa de 2, 3 ou 4 quartos?
{%- endif %}
{%- if not bairro %}
- O(A) Sr(a) quer uma casa em qual bairro?
{%- endif %}
{%- if not orcamento %}
- Qual o orçamento do(a) Sr(a) para a compra da casa.
{%- endif %}
{%- endif %}

Se achar que faz sentido compartilhar com o cliente o masterplan, envie o link:
https://vilacarnauba.com/masterplan/

1. Uso de ferramentas:
    - Use as ferramentas apenas quando o usuário fornecer uma resposta explícita e direta a uma das perguntas necessárias (nome, quantidade de quartos, suíte, orçamento ou meio de contato).
    - Nunca use as ferramentas se o usuário não fornecer uma resposta clara e direta.
    - Nunca use as ferramentas com input vazio ou se o usuário mencionar palavras-chave de forma casual ou em outro contexto.
    - Exemplo de uso correto:
        - Se você perguntar "Qual é o seu orçamento?" e o usuário responder "Meu orçamento é de R$ 300 mil", use a ferramenta para salvar o orçamento.
    - Exemplo de uso incorreto:
        - Se o usuário disser apenas "olá" ou "bom dia", não use as ferramentas.
    - Somente use uma ferramenta se você tiver feito uma pergunta antes.

2. Prioridade das perguntas:
    - Sempre priorize as perguntas listadas acima (nome, quantidade de quartos, bairro e orçamento) antes de qualquer outra coisa.
    - Nunca pergunte "quer saber mais sobre a vila carnaúba?" ou qualquer outra pergunta irrelevante enquanto houver perguntas pendentes da lista.
    - Se o usuário fizer uma pergunta sobre o empreendimento, responda de forma objetiva caso tenha certeza, ou envie o masterplan e, em seguida, retome as perguntas necessárias.

3. Atualização de informações:
    - Se o usuário disser que tem um nome diferente de {{ nome_do_lead }}, atualize o nome da pessoa para o novo nome dito.
    - Se o usuário fornecer informações adicionais (como mudança de preferência sobre quartos ou suíte), atualize os dados conforme necessário.

4. **Finalização:**
   - Se o usuário demonstrar interesse no empreendimento, pergunte a melhor data e hora para agendar uma ligação com o time de vendas.
   - Se o usuário pedir um telefone de contato, explique gentilmente que ele deve informar o meio de contato preferido (telefone ou email) e o respectivo número ou endereço.
```

## Setup da Aplicação

### Requisitos

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Python3.12 (instalação com UV)](https://docs.astral.sh/uv/guides/install-python/)
- [docker compose](https://docs.docker.com/compose/install/)
- [ollama](https://ollama.com/download)
- [modelo qwen2.5](https://ollama.com/library/qwen2.5)

### Como Rodar?

1. Garanta que você tem o qwen2.5 instalado

```bash
ollama ls | grep qwen2.5
```

Deve listar no terminal o modelo

2. Configure um arquivo .env tal qual

```sh
  POSTGRES_DB = homer-db
  POSTGRES_USER = liza
  POSTGRES_PASSWORD = senhasupersegura123
  DB_HOST = localhost
  DEBUG = 0
```

3. Suba os serviços

```bash
docker compose up -d
```

4. Rode o Agente

```bash
./src/main.py 
```

ou

```bash
python3 ./src/main.py
```

5. Informe um Id

Aqui pode ser qualquer id. A aplicação vai vai checar por uma entrada na tabela
que tenha o valor desse id como primary key. Caso não exista,
ele vai criar uma entrada nova e printar o seu novo id de conversa.

6. Prontinho
Agora é só conversar. Caso queira conectar no banco com um dbeaver
da vida para ver as variáveis mudando em tempo real, fique à vontade.

## Problemas e Possíveis Soluções

- **Problema**: Salvar a data e hora que o usuário informa no banco como varchar
dificulta o resgate e uso desse dado (já que estamos salvando-o como 'sujo')
e, por consequencia, dificulta a integração com outros serviços.\
**Possível Solução**:\
Usar o sdk da Google com o LangChain para agendar as reuniões diretamente em um calendário:
[ref](https://python.langchain.com/api_reference/google_community/calendar.html)

- **Problema**: O Agente não tem como responder à perguntas específicas sobre
o empreendimento.\
**Possível Solução**:\
Usar um vector storage (postgres com pgvector/redis vector storage) para guardar
docs de informações sobre o empreendimento, vetorizar a mensagem do usuário e
buscar no storage por docs que tenham
[similaridade](https://pt.wikipedia.org/wiki/Similaridade_por_cosseno)
e usar esses docs como parte do prompt.\
A estrutura atual do projeto permite que sejam inseridas essas informações sem
ter que mudar muita coisa, haja vista a função modularizada
`create_model_promt` em `src->prompt.py`, que por sua vez é usada em `src->nodes->agent.py`.

- **Problema**: Latência da aplicação. Uso a definição de latência como:
A diferença de tempo entre o input do usuário e a percepção do
usuário de uma resposta da aplicação (Roy Fielding,
Architectural Styles and the Design of Network-based
Software Architectures, University Of California).\
**Possível Solução**:\
Ainda de acordo com Fielding, a órdem de imposição de restrições na aplicação são:

1. **Os requisitos do domínio:** Aqui não podemos mudar nada,
o requisito tem que ser cumprido.

2. **Disposição dos elementos arquiteturais:** Aqui temos duas opções:\
  2.1:  Podemos isolar a aplicação do Agente
        e colocá-la como um consumer de uma fila. (Não gosto dessa)\
  2.2:  Podemos colocar o Agente como um serviço e fazer ele comunicar com os outros
        serviços por grpc, o que já bate na imposição de banda
        - que é outra imposição principal. (Essa é hype :D).

3. **A implementação de cada elemento:** Aqui tem uma opção legal,
investigar se cabe usar o [py03](https://pyo3.rs/main/getting-started.html?) para
implementar partes do elemento arquitetural 'Agente' em Rust, ganhando performance,
[segurança](https://www.nsa.gov/Press-Room/Press-Releases-Statements/Press-Release-View/article/3608324/us-and-international-partners-issue-recommendations-to-secure-software-products/)
e garantias na compilação.

## References

### Grafana

- [Provisioning Grafana](https://grafana.com/tutorials/provision-dashboards-and-data-sources)

- [Postgres exporter](https://grafana.com/docs/grafana-cloud/monitor-applications/asserts/enable-prom-metrics-collection/data-stores/postgresql/)

- [Postgres dashboard](https://grafana.com/grafana/dashboards/9628-postgresql-database/)

### LangGraph

- [Getting Started](https://langchain-ai.github.io/langgraph/tutorials/introduction/)

- [Passing runtime values to tools](https://langchain-ai.github.io/langgraph/how-tos/pass-run-time-values-to-tools/)
