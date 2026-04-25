from typing import Annotated, TypedDict
import operator


class AgentState(TypedDict):
    """定义 LangGraph 在各节点间传递的共享状态结构。"""

    requirement: str
    current_script: str
    errors: list[dict]
    iteration: int
    history: Annotated[list[str], operator.add]
