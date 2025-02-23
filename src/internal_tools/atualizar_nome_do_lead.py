from langchain_core.messages.tool import ToolMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langchain_core.tools.base import InjectedToolCallId
from langgraph.graph.state import Command
from typing_extensions import Annotated

from project_types.database_types import database_layer


@tool
def atualizar_nome_do_lead(
    tool_call_id: Annotated[str, InjectedToolCallId],
    config: RunnableConfig,
    novo_nome: str,
) -> Command:
    """Use essa ferramenta para modificar o nome do usuário, caso ele diga o nome dele ou caso ele peça para que o chame de outra forma"""

    print(f"O nome do usuário é: {novo_nome}")
    assert config["configurable"]["thread_id"] is not None
    database_layer.update_lead_name(config["configurable"]["thread_id"], novo_nome)
    return Command(
        update={
            "nome_do_lead": novo_nome,
            "messages": [
                ToolMessage(
                    f"O nome deste usuário foi salvo como {novo_nome} com sucesso!",
                    tool_call_id=tool_call_id,
                )
            ],
        }
    )
