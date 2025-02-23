from langchain_core.messages import AIMessage
from .node_constants import (
    SENTIMENT_NODE,
    TOOLS_NODE,
)  # It's imported from this place to avoid circular import
from project_types.state_types import State


# Conditional function to redirect to tools node or not
def should_continue(state: State):
    messages = state["messages"]
    last_message = messages[-1]
    assert isinstance(last_message, AIMessage)
    if last_message.tool_calls:
        return TOOLS_NODE
    return SENTIMENT_NODE
