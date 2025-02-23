from langchain_core.tools import tool
from langgraph.graph.graph import RunnableConfig
from langgraph.graph.state import Command
from typing_extensions import Annotated
from langchain_core.tools.base import InjectedToolCallId
from langchain_core.messages.tool import ToolMessage
from project_types.database_types import database_layer


@tool
def atualizar_com_suite(
    tool_call_id: Annotated[str, InjectedToolCallId],
    config: RunnableConfig,
    com_suite: bool,
) -> Command:
    """Use essa ferramenta para guardar se a pessoa que uma casa com suites ou não."""

    print(f"Essa pessoa quer casas com suites: {com_suite}")
    thread_id = config["configurable"]["thread_id"]
    assert thread_id is not None
    database_layer.update_with_suite(int(thread_id), with_suite=com_suite)
    return Command(
        update={
            "com_suite": com_suite,
            "messages": [
                ToolMessage(
                    "A opção do usuário sobre casas com suite ou não foi alterada com sucesso",
                    tool_call_id=tool_call_id,
                )
            ],
        }
    )
