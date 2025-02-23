from typing import Literal
from langgraph.graph import MessagesState

type PosicaoDoSol = Literal["Manhã", "Tarde"]


class State(MessagesState):
    nome_do_lead: str | None
    quantidade_de_quartos: int | None
    posicao_do_sol: PosicaoDoSol | None
