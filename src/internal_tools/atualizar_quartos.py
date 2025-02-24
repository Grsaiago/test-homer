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
    quantidade_de_quartos: Annotated[
        int, "O número de quartos que o usuário informou querer em uma casa"
    ],
) -> Command:
    """
    Use essa ferramenta apenas quando o usuário fornecer uma resposta explícita e direta à pergunta sobre quantos quartos ele quer na casa.
    Não use essa ferramenta se o usuário mencionar quartos de forma casual ou se o usuário perguntar quantos quartos tem as casas que vocês tem.
    """

    if quantidade_de_quartos == 0 or quantidade_de_quartos < 0:
        return Command(
            update={
                "messages": [
                    ToolMessage(
                        "A quantidade de quartos não foi atualizada pois é menor que 0. continue a conversa normalmente.",
                        tool_call_id=tool_call_id,
                    )
                ],
            }
        )
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
