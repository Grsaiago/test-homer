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
