from typing import Optional
from langgraph.graph import MessagesState

from db.models import Temperaturadolead


class State(MessagesState):
    nome_do_lead: Optional[str]
    quantidade_de_quartos: Optional[int]
    bairro: Optional[str]
    orcamento: Optional[int]
    temperatura_do_lead: Temperaturadolead
    data_e_hora_da_chamada: Optional[str]
