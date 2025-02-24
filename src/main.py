#!/usr/bin/env python

from langchain.globals import set_debug
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langchain_ollama import ChatOllama
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode

import internal_tools
from nodes import (
    AGENT_NODE,
    SENTIMENT_NODE,
    TOOLS_NODE,
    sentiment_analysis,
    chatbot,
    should_continue,
)
from project_types import (
    database_layer,  # has the sqlAlchemy connection as well as a pgPool
    envs,  # this import validates if all envs exist and places them in a typed env object,
    State,
)


def stream_graph_updates(
    graph: CompiledStateGraph,
    initial_state: State,
    config: RunnableConfig | None = None,
) -> None:
    """
    Runs the 'graph' with 'config' and it's initial state as 'initial_state'.

    :param graph: the compiled final graph to run
    :param initial_state: The initial state to be pushed to the graph
    :return: None
    """
    for event in graph.stream(initial_state, config):
        # os eventos vem com o nome do chatbot e o estado depois de passar por cada nó
        if "agent" not in event:
            continue
        for value in event.values():
            # Pega a chave mensagens se ela existir e se a última mensagem não for um tool_call
            if "messages" in value and "tool_calls" not in value["messages"][-1]:
                print("Assistant: ", value["messages"][-1].content)


def main():
    # set debugging for langGraph (or not)
    set_debug(envs.debug)
    print(f"O valor de debug é : {envs.debug}")

    # memory setup
    memory = PostgresSaver(database_layer.get_lang_graph_pool())
    memory.setup()

    # setup tools (aqui começa a codebase bilingue xD)
    update_state_tools = [
        internal_tools.atualizar_quartos,
        internal_tools.atualizar_nome_do_lead,
        internal_tools.atualizar_bairro,
        internal_tools.atualizar_orcamento,
    ]

    # Model/Tooling initialization
    chatbot_model = ChatOllama(model="qwen2.5:7b").bind_tools(update_state_tools)
    tool_node = ToolNode(tools=update_state_tools)

    # Graph compile
    graph_builder = StateGraph(State)
    graph = (
        graph_builder.add_node(AGENT_NODE, lambda state: chatbot(state, chatbot_model))
        .add_node(TOOLS_NODE, tool_node)
        .add_node(SENTIMENT_NODE, sentiment_analysis)
        .set_entry_point(AGENT_NODE)
        .add_conditional_edges(
            "agent",
            should_continue,
            {
                TOOLS_NODE: TOOLS_NODE,
                SENTIMENT_NODE: SENTIMENT_NODE,
            },
        )  # decides between tool usage ot not
        .add_edge(TOOLS_NODE, AGENT_NODE)  # after tools, go back to agent
        .set_finish_point(SENTIMENT_NODE)
        .compile(checkpointer=memory)
    )

    # main event loop
    while True:
        lead_id = input("Qual o Id dessa conversa?: ")
        # TODO: Validate to see if it's a valid number representation and if n > 0
        while True:
            try:
                user_input = input("User: ")
                match user_input.lower():
                    case "q" | "quit" | "exit":
                        print("Byeeee")
                        return
                    case "nova_conversa":
                        print("Fechando nossa conversa, até outra hora!")
                        break

                # get the initial state for a given id and append the current user message as the last message
                lead_info, is_new_lead = database_layer.get_or_create_lead_by_id(
                    int(lead_id)
                )
                assert lead_info is not None
                lead_id = lead_info.id  # atualizar o lead_id para o que exista
                if is_new_lead:
                    print("Opa! Um novo lead xD")
                # We initialize the state with what's in the lead_info table because we want
                # that any changes made to the db by third party (e.g: real estate agents)
                # to be reflected as soon as possible to the llm.
                # This increases fan-out, but makes it so that the llm's info is always up to date.
                initial_state: State = {
                    "nome_do_lead": lead_info.nome_do_lead,
                    "quantidade_de_quartos": lead_info.quantidade_de_quartos,
                    "bairro": lead_info.bairro,
                    "orcamento": lead_info.orcamento,
                    "messages": [HumanMessage(content=user_input)],
                }
                # generate a runnableConfig based on lead's name
                user_config: RunnableConfig = {
                    "configurable": {"thread_id": str(lead_id)}
                }
                stream_graph_updates(graph, initial_state, user_config)
            except Exception as e:
                print("System: Something went wrong " + e.__str__())
                break


if __name__ == "__main__":
    main()
