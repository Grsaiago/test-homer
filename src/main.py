#!/usr/bin/env python

import sys

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langchain_ollama import ChatOllama
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph
from psycopg_pool import ConnectionPool

from project_types.types import EnvSetupException, State, TypedEnvs
from prompt import prompt_template
from sentiment_analyzer import sentiment_analyzer


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
        if "chatbot" not in event:
            continue
        for value in event.values():
            if "messages" in value:
                print("Assistant: ", value["messages"][-1].content)


def chatbot(state: State, model: BaseChatModel):
    """
    The first processing step. This is the function that calls the ai to get
    a Natural Language response to be sent to the end user.

    :param state: The graph's State
    :param model: The model to be used to process the question
    """
    ## render the final template message as a history of all messages + a prompt
    rendered_message = prompt_template.invoke({"msgs": state["messages"]})
    message = model.invoke(rendered_message)
    return {"messages": [message]}


def sentiment_analysis(state: State) -> State:
    """
    The step that processes the sentiment.
    It fetches all messages sent from the user so far and classifies the user as:
    "hot", "warm", or "cold". Al of those in regards to buying intent

    :param state: The graph's State
    """
    # messages = memory.get(context)
    messages = state["messages"]
    if messages is not None:
        print("O valor de memória atual é: ", messages)
    return state
    result = sentiment_analyzer(state["messages"][-2].content)
    if result is None:
        return state
    sentiment = result["label"]
    confidence = result["score"]

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
        memory = PostgresSaver(db_pool)
        memory.setup()

        chatbot_model = ChatOllama(model="splitpierre/bode-alpaca-pt-br:latest")
        graph_builder = StateGraph(State)
        graph = (
            graph_builder.add_sequence(
                [
                    (
                        "chatbot",
                        lambda state: chatbot(state, chatbot_model),
                    ),
                    ("sentiment_node", sentiment_analysis),
                ]
            )
            .set_entry_point("chatbot")
            .set_finish_point("sentiment_node")
            .compile(checkpointer=memory)
        )

        while True:
            user_id = input("Qual o seu nome?: ")
            user_config: RunnableConfig = {"configurable": {"thread_id": user_id}}
            while True:
                try:
                    # print("O valor de memória atual é: ", memory.get(user_config))
                    updated_memory = memory.get(user_config)
                    if updated_memory is not None:
                        print(
                            "o valor de state é",
                            updated_memory["channel_values"]["messages"],
                        )
                    user_input = input("User: ")
                    if user_input.lower() in ["quit", "q", "exit"]:
                        print("Byeeee")
                        return
                    if user_input.lower() in ["novo_nome"]:
                        print("Troca de nome")
                        break
                    initial_state: State = {
                        "messages": [HumanMessage(content=user_input)],
                        "placeholder": "",
                    }
                    stream_graph_updates(graph, initial_state, user_config)
                except Exception as e:
                    print("System: Something went wrong " + e.__str__())
                    break


if __name__ == "__main__":
    main()
