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
    novo_nome: Annotated[str, "O nome que o usuário informou ser o dele ou dela"],
) -> Command:
    """
    Use essa ferramenta apenas quando o usuário fornecer uma resposta explícita e direta à pergunta sobre qual o nome dele.
    Não use essa ferramenta se o usuário mencionar um nome de forma casual ou em outro contexto."
    """

    if novo_nome == "None" or "":
        return Command(
            update={
                "messages": [
                    ToolMessage(
                        "O nome do contato não foi atualizado pois está vazio. Continue a conversa normalmente.",
                        tool_call_id=tool_call_id,
                    )
                ],
            }
        )
    print(f"O nome do usuário é: {novo_nome}")
    thread_id = config["configurable"]["thread_id"]
    assert thread_id is not None
    # thread_id is converted to str before graph passing
    database_layer.update_lead_name(int(thread_id), novo_nome)
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
