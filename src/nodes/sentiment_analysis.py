from langchain_core.messages import AnyMessage, HumanMessage
from project_types.state_types import State
from sentiment_analyzer import sentiment_analyzer


def sentiment_analysis(state: State) -> State:
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
