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
Ferramentas, nós e interações com a camada de dados estão
separados cada um em seu módulo. Isso não é somente uma decisão estilística, tendo
em vista que uma boa organização não só de estrutura de pastas, mas de código, agiliza
o [ciclo de desenvolvimento de software](https://en.wikipedia.org/wiki/Systems_development_life_cycle).
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
        - que é outra imposição principal. (Essa é hype :D).\
3. **A implementação de cada elemento:** Aqui tem uma opção legal,
investigar se cabe usar o [py03](https://pyo3.rs/main/getting-started.html?) para
implementar partes do elemento arquitetural 'Agente' em Rust, ganhando performance,
[segurança](https://www.nsa.gov/Press-Room/Press-Releases-Statements/Press-Release-View/article/3608324/us-and-international-partners-issue-recommendations-to-secure-software-products/)
e garantias na compilação.


### Setup da Aplicaçã1. 


## References

### Grafana

- [Provisioning Grafana](https://grafana.com/tutorials/provision-dashboards-and-data-sources)

- [Postgres exporter](https://grafana.com/docs/grafana-cloud/monitor-applications/asserts/enable-prom-metrics-collection/data-stores/postgresql/)

- [Postgres dashboard](https://grafana.com/grafana/dashboards/9628-postgresql-database/)

### LangGraph

- [Getting Started](https://langchain-ai.github.io/langgraph/tutorials/introduction/)

- [Passing runtime values to tools](https://langchain-ai.github.io/langgraph/how-tos/pass-run-time-values-to-tools/)
