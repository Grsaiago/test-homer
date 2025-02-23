from nodes import SENTIMENT_NODE, TOOLS_NODE
from project_types.state_types import State


# Conditional function to redirect to tools node or not
def should_continue(state: State):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return TOOLS_NODE
    return SENTIMENT_NODE
