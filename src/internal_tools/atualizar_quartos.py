from langchain_core.tools import tool
from langgraph.graph.graph import RunnableConfig
from langgraph.graph.state import Command
from typing_extensions import Annotated
from langchain_core.tools.base import InjectedToolCallId
from langchain_core.messages.tool import ToolMessage
from project_types.database_types import database_layer


@tool
def atualizar_quartos(
    tool_call_id: Annotated[str, InjectedToolCallId],
    config: RunnableConfig,
    quantidade_de_quartos: int,
) -> Command:
    """Use essa ferramenta para atualizar quantos quartos o usuário vai querer no apto que o usuário está procurando"""

    print(f"A quantidade de quartos que o usuário quer é: {quantidade_de_quartos}")
    thread_id = config["configurable"]["thread_id"]
    assert thread_id is not None
    database_layer.update_room_ammount(int(thread_id), quantidade_de_quartos)
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
