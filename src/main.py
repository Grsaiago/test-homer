#!/usr/bin/env python

from langchain.globals import set_debug
from langchain_core.messages import AnyMessage, HumanMessage
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_ollama import ChatOllama
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import MessagesState, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode

import internal_tools
from project_types.database_types import (
    database_layer,
)  # Has the sqlAlchemy connection as well as a pgPool
from project_types.env_types import (
    envs,
)  # this import validates if all envs exist and places them in a typed env object
from project_types.state_types import State
from prompt import create_model_prompt
from sentiment_analyzer import sentiment_analyzer


# Conditional function to redirect to tools node or not
def should_continue(state: State):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return "sentiment_node"


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


def chatbot(state: State, model: Runnable):
    """
    The first processing step. This is the function that calls the llm to get
    a Natural Language response to be sent to the end user.

    :param state: The graph's State
    :param model: The model to be used to process the question
    """
    ## render the final template message as prompt + history of all messages
    prompt = create_model_prompt(state, state["messages"])
    message = model.invoke(prompt)
    return {"messages": [message]}


def sentiment_analysis(state: State) -> MessagesState:
    """
    The step that processes the sentiment.
    It fetches all messages sent from the user so far and classifies the user as:
    "hot", "warm", or "cold". Al of those in regards to buying intent

    :param state: The graph's State
    """
    messages: list[AnyMessage] = state["messages"]
    if messages is not None:
        human_messages: list[str] = [
            message.content
            for message in messages
            if isinstance(message, HumanMessage) and isinstance(message.content, str)
        ]
        message_string = ";".join(human_messages)
        messages_len = len(human_messages)
    result = sentiment_analyzer.predict(message_string)
    if result is None:
        return state
    print("sentiment analysis: ", result)
    return state
    if sentiment == "NEGATIVE":
        print("Usuário está frio")
    elif sentiment == "POSITIVE" and confidence > 0.8:
        print("Usuário está quente")
    else:
        print("Usuário está morno")
    return state


def main():
    # set debugging for langGraph
    set_debug(envs.debug)
    print(f"O valor de debug é : {envs.debug}")

    # memory setup
    memory = PostgresSaver(database_layer.get_lang_graph_pool())
    memory.setup()

    # setup tools (aqui começa a codebase bilingue xD)
    update_state_tools = [
        internal_tools.atualizar_quartos,
        internal_tools.atualizar_posicao_do_sol,
    ]

    # Model/Tooling initialization
    chatbot_model = ChatOllama(model="llama3.2").bind_tools(update_state_tools)
    tool_node = ToolNode(tools=update_state_tools)

    # Graph compile
    graph_builder = StateGraph(State)
    graph = (
        graph_builder.add_node("agent", lambda state: chatbot(state, chatbot_model))
        .add_node("tools", tool_node)
        .add_node("sentiment_node", sentiment_analysis)
        .set_entry_point("agent")
        .add_conditional_edges(
            "agent",
            should_continue,
            {"tools": "tools", "sentiment_node": "sentiment_node"},
        )  # decide between tool usage ot not
        .add_edge("tools", "agent")  # after tools, go back to agent
        .set_finish_point("sentiment_node")
        .compile(checkpointer=memory)
    )

    while True:
        lead_name = input("Qual o seu nome?: ")
        while True:
            try:
                user_input = input("User: ")
                match user_input.lower():
                    case "q" | "quit" | "exit":
                        print("Byeeee")
                        return
                    case "novo_nome":
                        print("Troca de nome")
                        break

                # get the initial state for a given id and append the current user message as the last message
                initial_state = get_lead_initial_sate(lead_name, user_input)
                # generate a runnableConfig based on lead's name
                user_config: RunnableConfig = {"configurable": {"thread_id": lead_name}}
                stream_graph_updates(graph, initial_state, user_config)
            except Exception as e:
                print("System: Something went wrong " + e.__str__())
                break


def get_lead_initial_sate(lead_name: str, user_input: str) -> State:
    """
    Gets the state with the initial message filled out.
    We initialize the state with what's in the lead_info table because we want
    that any changes made to the db by third party (e.g: real estate agents),
    to be reflected as soon as possible to the llm.
    This increases fan-out, but makes it so that the llm's info is always up to date.

    :param id: The id of the thread.
    :param memory_layer: The memory layer for the graph.
    :return State: The state for this id **without the messages part filled out**
    """
    synced_lead_info = database_layer.get_or_insert_lead_by_name(lead_name)
    state: State = {
        "messages": [HumanMessage(content=user_input)],
        "quantidade_de_quartos": synced_lead_info.quantidade_de_quartos,
        "posicao_do_sol": synced_lead_info.posicao_do_sol,
        "nome_do_lead": synced_lead_info.nome_do_lead,
    }
    return state


if __name__ == "__main__":
    main()
