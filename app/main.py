from __future__ import annotations

from app.graph.workflow import build_graph


def run_once(requirement: str) -> dict:
    graph = build_graph()
    initial_state = {
        "requirement": requirement,
        "current_script": "",
        "errors": [],
        "iteration": 0,
        "history": [],
    }
    return graph.invoke(initial_state)


if __name__ == "__main__":
    demo_requirement = "创建一个blue方潜艇平台，初始坐标30n 30e，速度10节向北"
    result = run_once(demo_requirement)
    print("=== FINAL SCRIPT ===")
    print(result.get("current_script", ""))
    print("=== ERRORS ===")
    print(result.get("errors", []))
    print("=== HISTORY ===")
    for item in result.get("history", []):
        print(item)
