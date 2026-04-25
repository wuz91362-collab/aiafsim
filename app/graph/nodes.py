from __future__ import annotations

from app.config import settings
from app.models.state import AgentState
from app.rag.store import LocalKnowledgeStore
from app.validator.service import validate_script

knowledge_store = LocalKnowledgeStore(settings.knowledge_file)


def generator_node(state: AgentState) -> AgentState:
    chunks = knowledge_store.retrieve(state["requirement"], top_k=3)
    references = "\n".join([c.content for c in chunks]) if chunks else "# no references"

    # Placeholder generator; replace with LLM call.
    generated = (
        f"# requirement\n{state['requirement']}\n\n"
        f"# references\n{references}\n\n"
        "platform blue_sub WSF_PLATFORM\n"
        "  side blue\n"
        "  position 30n 30e\n"
        "end_platform\n"
    )
    return {
        "current_script": generated,
        "iteration": state["iteration"] + 1,
        "history": [f"generated iteration {state['iteration'] + 1}"],
    }


def validator_node(state: AgentState) -> AgentState:
    result = validate_script(state["current_script"])
    return {
        "errors": result["errors"],
        "history": [f"validator return_code={result['return_code']}"],
    }


def debugger_node(state: AgentState) -> AgentState:
    if not state["errors"]:
        return {"history": ["no errors to fix"]}

    # Placeholder refiner; replace with LLM-based targeted patching.
    error_hint = "\n".join(
        [f"- line {e.get('line', '?')}: {e.get('message', '')}" for e in state["errors"]]
    )
    refined = (
        f"{state['current_script']}\n"
        f"# auto_fix_hints\n{error_hint}\n"
    )
    return {
        "current_script": refined,
        "history": ["debugger appended fix hints"],
    }
