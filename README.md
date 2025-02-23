# test-homer

My technical assignment for the [Homer](https://www.homer.com.br/) startup

## Goals

## Things I've kept in mind

### Stateless Memory

tl;dr: I've used ```PostgresSaver``` instead of ```MemorySaver```.
LangGraph has a 'memory' feature, which makes it capable of keeping track of state
between executions, given only that they have the same Id.
The default implementation of this feature is a in-memory store.
Having a concurrent environment in mind, I've chosen to use a postgres
implementation for this feature, making it possible for the main application to be
deployed in a HA environment.

## References

### Grafana

- [Provisioning Grafana](https://grafana.com/tutorials/provision-dashboards-and-data-sources)

- [Postgres exporter](https://grafana.com/docs/grafana-cloud/monitor-applications/asserts/enable-prom-metrics-collection/data-stores/postgresql/)

- [Postgres dashboard](https://grafana.com/grafana/dashboards/9628-postgresql-database/)

### LangGraph

- [Getting Started](https://langchain-ai.github.io/langgraph/tutorials/introduction/)

- [Passing runtime values to tools](https://langchain-ai.github.io/langgraph/how-tos/pass-run-time-values-to-tools/)

### TODOS

- [ ] The llm is still halucinating a bit when passing the args for
  the method that gets an enum. I'll look into creating each tool via
  the class Tool instead of using the function decorator. This way I can
  pass more information about each function parameter.
  - [x] I'm feeding the user's name on the prompt, as a result, when the
  user wants to change it's name, the llm changes it to the name it had before,
  because of the order and How I'm building the prompt.\
  Solved: I've taken ou the lead_name formatting for the info, moved to a directive
  at the end.

