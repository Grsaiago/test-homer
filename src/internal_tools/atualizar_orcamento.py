from langchain_core.messages.tool import ToolMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langchain_core.tools.base import InjectedToolCallId
from langgraph.graph.state import Command
from typing_extensions import Annotated

from project_types.database_types import database_layer


@tool
def atualizar_orcamento(
    tool_call_id: Annotated[str, InjectedToolCallId],
    config: RunnableConfig,
    orcamento: Annotated[
        int, "O orçamento que a pessoa informou que tem para comprar uma casa"
    ],
) -> Command:
    """
    Use essa ferramenta apenas quando o usuário fornecer uma resposta explícita e direta à pergunta sobre qual o orçamento dele para comprar uma casa.
    Não use essa ferramenta se o usuário mencionar um orçamento de forma casual ou em outro contexto."
    """

    if orcamento < 0:
        return Command(
            update={
                "messages": [
                    ToolMessage(
                        "O orçamento não foi atualizado pois é um número menor que 0. Continue a conversa normalmente.",
                        tool_call_id=tool_call_id,
                    )
                ],
            }
        )
    thread_id = config["configurable"]["thread_id"]
    assert thread_id is not None
    # thread_id is converted to str before graph passing
    database_layer.update_budget(int(thread_id), orcamento)
    return Command(
        update={
            "orcamento": orcamento,
            "messages": [
                ToolMessage(
                    f"O orçamento deste usuário foi salvo como {orcamento} com sucesso!",
                    tool_call_id=tool_call_id,
                )
            ],
        }
    )
