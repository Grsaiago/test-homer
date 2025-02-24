from typing import Optional, Literal
from langchain_core.messages import AnyMessage, HumanMessage
from langgraph.graph.graph import RunnableConfig
from db.models import Temperaturadolead
from project_types.state_types import State
from sentiment_analyzer import sentiment_analyzer
from project_types import database_layer


def sentiment_analysis(
    state: State, config: RunnableConfig
) -> Optional[dict[Literal["temperatura_do_lead"], Temperaturadolead]]:
    """
    The step that processes the sentiment.
    It analyses the sentiment of all messages sent from the user so far,
    combined with all the information the user has already provided,
    and classifies the user as: "Hot", "Warm", or "Cold" in regards to buying intent.

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

    # calculate final temperature
    state_weight = 0.7
    sentiment_weight = 1 - state_weight
    final_score = (state_weight * state_score) + (sentiment_weight * sentiment_score)
    final_temperature: Temperaturadolead
    if final_score >= 0.7:
        final_temperature = Temperaturadolead.QUENTE
    elif 0.4 <= final_score < 0.6:
        final_temperature = Temperaturadolead.MORNO
    else:
        final_temperature = Temperaturadolead.FRIO

    # conditional update on state and db
    # We can insert an api call here to behave like a webhook
    if final_temperature != state["temperatura_do_lead"]:
        thread_id = config["configurable"]["thread_id"]
        assert thread_id is not None
        database_layer.update_lead_temperature(thread_id, final_temperature)
        return {"temperatura_do_lead": final_temperature}
    return None


def calculate_state_score(state: State, key_weight: dict[str, float]) -> float:
    final_score = 0.0
    for key, weight in key_weight.items():
        if state.get(key, None) is not None:
            final_score += weight
    return final_score
