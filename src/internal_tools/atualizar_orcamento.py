from langchain_core.tools import tool
from langgraph.graph.graph import RunnableConfig
from langgraph.graph.state import Command
from typing_extensions import Annotated
from langchain_core.tools.base import InjectedToolCallId
from langchain_core.messages.tool import ToolMessage
from project_types.database_types import database_layer


@tool
def atualizar_orcamento(
    tool_call_id: Annotated[str, InjectedToolCallId],
    config: RunnableConfig,
    orcamento: int,
) -> Command:
    """Use essa ferramenta para guardar o valor que o usuário tem para gastar com uma casa, no caso de um range, use o valor máximo."""

    print(f"O orçamento dessa pessoa é: {orcamento}")
    thread_id = config["configurable"]["thread_id"]
    assert thread_id is not None
    database_layer.update_budget(int(thread_id), budget=orcamento)
    return Command(
        update={
            "orcamento": orcamento,
            "messages": [
                ToolMessage(
                    "O orçamento desse usuário foi alterada com sucesso",
                    tool_call_id=tool_call_id,
                )
            ],
        }
    )
