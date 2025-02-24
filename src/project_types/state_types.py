from langgraph.graph import MessagesState

from db.models import Temperaturadolead


class State(MessagesState):
    nome_do_lead: str | None
    quantidade_de_quartos: int | None
    bairro: str | None
    orcamento: int | None
    temperatura_do_lead: Temperaturadolead
