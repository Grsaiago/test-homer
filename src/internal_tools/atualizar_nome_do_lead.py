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
    thread_id = config["configurable"]["thread_id"]
    assert thread_id is not None
    # thread_id is converted to str before graph passing
    database_layer.update_lead_name(int(thread_id), novo_nome)
    print(f"O id do usuário no banco é: {thread_id}")
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
