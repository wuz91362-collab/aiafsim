from __future__ import annotations

from langgraph.graph import END, StateGraph

from app.config import settings
from app.graph.nodes import debugger_node, generator_node, validator_node
from app.models.state import AgentState


def should_continue(state: AgentState) -> str:
    """根据错误状态与重试次数决定流程走向。"""
    # 无错误或达到最大重试次数时结束流程，否则继续修复循环。
    if not state["errors"]:
        return "done"
    if state["iteration"] >= settings.max_iterations:
        return "done"
    return "retry"


def build_graph():
    """构建并编译 LangGraph 工作流。"""
    # 工作流：generator -> validator -> (done | debugger -> validator ...)
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
