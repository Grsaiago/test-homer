#!/usr/bin/env python

import sys

from langchain_core.messages import AnyMessage, HumanMessage
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_ollama import ChatOllama
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import MessagesState, StateGraph
from langgraph.graph.state import CompiledStateGraph
from psycopg_pool import ConnectionPool
from tools import atualizar_quartos
from langgraph.prebuilt import ToolNode
from project_types.types import EnvSetupException, TypedEnvs
from prompt import prompt_template
from sentiment_analyzer import sentiment_analyzer


# Conditional function to redirect to tools node or not
def should_continue(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return "sentiment_node"


def stream_graph_updates(
    graph: CompiledStateGraph,
    initial_state: MessagesState,
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


def chatbot(state: MessagesState, model: Runnable):
    """
    The first processing step. This is the function that calls the llm to get
    a Natural Language response to be sent to the end user.

    :param state: The graph's State
    :param model: The model to be used to process the question
    """
    ## render the final template message as a history of all messages + a prompt
    rendered_message = prompt_template.invoke({"msgs": state["messages"]})
    message = model.invoke(rendered_message)
    return {"messages": [message]}


def sentiment_analysis(state: MessagesState) -> MessagesState:
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


envs: TypedEnvs
try:
    envs = TypedEnvs.load_envs()
except EnvSetupException as err:
    print("Failed due to lack of envs setup:")
    for error in err.errors:
        print(f"- {error}")
    sys.exit(-1)


def main():
    db_connection_kwargs = {
        "autocommit": True,
        "prepare_threshold": 0,
    }
    db_connection_string = f"postgresql://{envs.db_user}:{envs.db_passwd}@{envs.db_host}:5432/{envs.db_name}"
    with ConnectionPool(
        conninfo=db_connection_string,
        max_size=20,
        kwargs=db_connection_kwargs,
    ) as db_pool:
        # memory setup
        memory = PostgresSaver(db_pool)
        memory.setup()

        # Model/Tooling initialization
        chatbot_model = ChatOllama(model="llama3.2").bind_tools([atualizar_quartos])
        tool_node = ToolNode(tools=[atualizar_quartos])

        # Graph compile
        graph_builder = StateGraph(MessagesState)
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
            user_id = input("Qual o seu nome?: ")
            user_config: RunnableConfig = {"configurable": {"thread_id": user_id}}
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
                    initial_state: MessagesState = {
                        "messages": [HumanMessage(content=user_input)],
                    }
                    stream_graph_updates(graph, initial_state, user_config)
                except Exception as e:
                    print("System: Something went wrong " + e.__str__())
                    break


if __name__ == "__main__":
    main()
