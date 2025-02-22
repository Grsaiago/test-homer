from typing import Literal
from langgraph.graph import MessagesState

type PosicaoDoSol = Literal["Manhã", "Tarde"]


class State(MessagesState):
    quantidade_de_quartos: int | None
    posicao_do_sol: PosicaoDoSol | None
    nome_do_usuario: str
