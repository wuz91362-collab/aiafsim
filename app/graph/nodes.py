from __future__ import annotations

from app.llm.client import build_llm_client
from app.models.state import AgentState
from app.rag.store import build_knowledge_store
from app.validator.service import validate_script

knowledge_store = build_knowledge_store()
llm_client = build_llm_client()


def generator_node(state: AgentState) -> AgentState:
    """根据需求与检索上下文生成脚本初稿。"""
    chunks = knowledge_store.retrieve(state["requirement"], top_k=3)
    references = "\n".join([c.content for c in chunks]) if chunks else "# no references"

    # 由 LLM 客户端生成脚本；在未接通模型时会自动降级为占位实现。
    generated = llm_client.generate_script(state["requirement"], references)
    return {
        "current_script": generated,
        "iteration": state["iteration"] + 1,
        "history": [f"generated iteration {state['iteration'] + 1}"],
    }


def validator_node(state: AgentState) -> AgentState:
    """调用校验器执行脚本检查并写回错误列表。"""
    result = validate_script(state["current_script"])
    return {
        "errors": result["errors"],
        "history": [f"validator return_code={result['return_code']}"],
    }


def debugger_node(state: AgentState) -> AgentState:
    """根据校验错误补充修复提示并推进迭代计数。"""
    if not state["errors"]:
        return {"history": ["no errors to fix"]}

    debug_query = f"{state['requirement']}\n" + "\n".join(
        [str(item.get("message", "")) for item in state["errors"]]
    )
    chunks = knowledge_store.retrieve(debug_query, top_k=3)
    references = "\n".join([c.content for c in chunks]) if chunks else "# no references"
    refined = llm_client.refine_script(state["current_script"], state["errors"], references)
    return {
        "current_script": refined,
        "iteration": state["iteration"] + 1,
        "history": ["debugger appended fix hints"],
    }
