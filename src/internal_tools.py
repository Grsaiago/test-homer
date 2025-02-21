from langchain_core.messages.tool import ToolMessage
from langchain_core.tools import tool
from langchain_core.tools.base import InjectedToolCallId
from langgraph.graph.state import Command
from typing_extensions import Annotated

from project_types.state_types import PosicaoDoSol


@tool
def atualizar_quartos(
    tool_call_id: Annotated[str, InjectedToolCallId], quantidade_de_quartos: int
) -> Command:
    """Use essa ferramenta para atualizar quantos quartos o usuário vai querer no apto que o usuário está procurando"""

    print(f"A quantidade de quartos que o usuário quer é: {quantidade_de_quartos}")
    return Command(
        update={
            "quantidade_de_quartos": quantidade_de_quartos,
            "messages": [
                ToolMessage(
                    "A quantidade de quartos para este usuário foi alterada com sucesso",
                    tool_call_id=tool_call_id,
                )
            ],
        }
    )


@tool
def atualizar_posicao_do_sol(
    tool_call_id: Annotated[str, InjectedToolCallId],
    posicao_do_sol: PosicaoDoSol,
) -> Command:
    """Use essa ferramenta para modificar a posição do sol que o usuário vai querer no apartamento que o usuário está procurando: sol da tarde ou sol da manhã"""

    print(f"A posição do sol que o usuário quer é: {posicao_do_sol}")
    return Command(
        update={
            "posicao_do_sol": posicao_do_sol,
            "messages": [
                ToolMessage(
                    "A posicao do sol para este usuário foi alterada com sucesso",
                    tool_call_id=tool_call_id,
                )
            ],
        }
    )
