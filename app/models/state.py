from typing import Annotated, TypedDict
import operator


class AgentState(TypedDict):
    requirement: str
    current_script: str
    errors: list[dict]
    iteration: int
    history: Annotated[list[str], operator.add]
