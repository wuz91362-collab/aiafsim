from __future__ import annotations

from langgraph.graph import END, StateGraph

from app.config import settings
from app.graph.nodes import debugger_node, generator_node, validator_node
from app.models.state import AgentState


def should_continue(state: AgentState) -> str:
    if not state["errors"]:
        return "done"
    if state["iteration"] >= settings.max_iterations:
        return "done"
    return "retry"


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("generator", generator_node)
    graph.add_node("validator", validator_node)
    graph.add_node("debugger", debugger_node)

    graph.set_entry_point("generator")
    graph.add_edge("generator", "validator")
    graph.add_conditional_edges(
        "validator",
        should_continue,
        {
            "done": END,
            "retry": "debugger",
        },
    )
    graph.add_edge("debugger", "validator")
    return graph.compile()
