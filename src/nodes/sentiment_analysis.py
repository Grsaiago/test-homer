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
    # get sentiment score
    messages: list[AnyMessage] = state["messages"]
    if messages is not None:
        human_messages: list[str] = [
            message.content
            for message in messages
            if isinstance(message, HumanMessage) and isinstance(message.content, str)
        ]
        message_string = ";".join(human_messages)
    messages_sentiment = sentiment_analyzer.predict(message_string)
    sentiment_score = 0.0
    match messages_sentiment.output:
        case "NEG":
            sentiment_score = 0.0
        case "NEU":
            sentiment_score = 0.5
        case "POS":
            sentiment_score = 1.0

    # get state_score
    key_weight = {
        "nome_do_lead": 0.1,
        "quantidade_de_quartos": 0.3,
        "bairro": 0.2,
        "orcamento": 0.4,
    }
    state_score = calculate_state_score(state, key_weight)

    state_weight = 0.7
    sentiment_weight = 1 - state_weight
    final_score = (state_weight * state_score) + (sentiment_weight * sentiment_score)
    if final_score >= 0.7:
        print("O lead está Quente")
    elif 0.4 <= final_score < 0.6:
        print("O lead está Morno")
    else:
        print("O lead está Frio")
    return state


def calculate_state_score(state: State, key_weight: dict[str, float]) -> float:
    final_score = 0.0
    for key, weight in key_weight.items():
        if state.get(key, None) is not None:
            final_score += weight
    return final_score
