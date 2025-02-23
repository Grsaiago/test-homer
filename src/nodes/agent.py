from langchain_core.runnables import Runnable

from project_types.state_types import State
from prompt import create_model_prompt


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
