from langgraph.graph import MessagesState


class State(MessagesState):
    nome_do_lead: str | None
    quantidade_de_quartos: int | None
    bairro: str | None
    orcamento: int | None
