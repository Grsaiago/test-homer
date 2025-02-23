from langgraph.graph import MessagesState


class State(MessagesState):
    nome_do_lead: str | None
    quantidade_de_quartos: int | None
    com_suite: bool | None
    orcamento: int | None
    meio_de_contato: str | None
