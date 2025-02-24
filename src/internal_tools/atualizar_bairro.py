from langchain_core.messages.tool import ToolMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langchain_core.tools.base import InjectedToolCallId
from langgraph.graph.state import Command
from typing_extensions import Annotated

from project_types.database_types import database_layer


@tool
def atualizar_bairro(
    tool_call_id: Annotated[str, InjectedToolCallId],
    config: RunnableConfig,
    bairro: Annotated[
        str, "O bairro no qual a pessoa informou que quer comprar uma casa"
    ],
) -> Command:
    """
    Use essa ferramenta apenas quando o usuário fornecer uma resposta explícita e direta à pergunta sobre em qual o bairro ela quer comprar a casa.
    Não use essa ferramenta se o usuário mencionar um bairro de forma casual ou em outro contexto."
    """

    if bairro == "None" or "":
        return Command(
            update={
                "messages": [
                    ToolMessage(
                        "O bairro não foi atualizado pois está vazio. Continue a conversa normalmente.",
                        tool_call_id=tool_call_id,
                    )
                ],
            }
        )
    print(f"O bairro em que o usuário quer uma casa é: {bairro}")
    thread_id = config["configurable"]["thread_id"]
    assert thread_id is not None
    # thread_id is converted to str before graph passing
    database_layer.update_neighbourhood(int(thread_id), bairro)
    return Command(
        update={
            "bairro": bairro,
            "messages": [
                ToolMessage(
                    f"O bairro no qual o usuário quer uma casa salvo como {bairro} com sucesso!",
                    tool_call_id=tool_call_id,
                )
            ],
        }
    )
