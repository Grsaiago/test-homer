from langchain_core.tools import tool
from langgraph.graph.graph import RunnableConfig
from langgraph.graph.state import Command
from typing_extensions import Annotated
from langchain_core.tools.base import InjectedToolCallId
from langchain_core.messages.tool import ToolMessage
from project_types.database_types import database_layer


@tool
def atualizar_meio_de_contato(
    tool_call_id: Annotated[str, InjectedToolCallId],
    config: RunnableConfig,
    meio_de_contato: str,
) -> Command:
    """Use essa ferramenta para atualizar o valor da forma de entrar em contato com a pessoa."""

    print(f"A forma de entrar em contato com o usuário é através de: {meio_de_contato}")
    thread_id = config["configurable"]["thread_id"]
    assert thread_id is not None
    database_layer.update_means_of_contact(
        int(thread_id), means_of_contact=meio_de_contato
    )
    return Command(
        update={
            "meio_de_contato": meio_de_contato,
            "messages": [
                ToolMessage(
                    "A forma de entrar em contato com este usuário foi alterada com sucesso",
                    tool_call_id=tool_call_id,
                )
            ],
        }
    )
