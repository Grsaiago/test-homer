from langchain_core.messages.tool import ToolMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langchain_core.tools.base import InjectedToolCallId
from langgraph.graph.state import Command
from typing_extensions import Annotated

from project_types.database_types import database_layer


@tool
def atualizar_data_e_hora_da_chamada(
    tool_call_id: Annotated[str, InjectedToolCallId],
    config: RunnableConfig,
    data_e_hora: Annotated[
        str,
        "A data e hora que o usuário escolheu para receber uma chamada do time de vendas",
    ],
) -> Command:
    """
    Use essa ferramenta apenas quando o usuário fornecer uma resposta explícita e direta à pergunta sobre qual data e hora ele gostaria de receber uma chamada do time de vendas.
    Não use essa ferramenta se o usuário mencionar uma data e horas de forma casual ou em outro contexto."
    """

    if data_e_hora == "None" or "":
        return Command(
            update={
                "messages": [
                    ToolMessage(
                        "A data e hora não foi atualizado pois está vazio. Continue a conversa normalmente.",
                        tool_call_id=tool_call_id,
                    )
                ],
            }
        )
    print(f"A datahora que o usuário quer receber uma chamada é: {data_e_hora}")
    thread_id = config["configurable"]["thread_id"]
    assert thread_id is not None
    # thread_id is converted to str before graph passing
    database_layer.update_call_date_time(int(thread_id), data_e_hora)
    return Command(
        update={
            "dia_e_hora_da_chamada": data_e_hora,
            "messages": [
                ToolMessage(
                    f"A data e hora que o usuário informou foi salvo com sucesso como {data_e_hora}. Uma pessoa da equipe de vendas entrará em contato com essa pessoa.",
                    tool_call_id=tool_call_id,
                )
            ],
        }
    )
