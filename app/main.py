from __future__ import annotations

from app.graph.workflow import build_graph


def run_once(requirement: str) -> dict:
    """执行一次完整工作流并返回最终状态。"""
    # 构建并执行一轮完整的“生成-校验-修复”流程。
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
    # 本地冒烟测试入口，便于快速手工验证流程是否可运行。
    demo_requirement = "创建一个blue方潜艇平台，初始坐标30n 30e，速度10节向北"
    result = run_once(demo_requirement)
    print("=== FINAL SCRIPT ===")
    print(result.get("current_script", ""))
    print("=== ERRORS ===")
    print(result.get("errors", []))
    print("=== HISTORY ===")
    for item in result.get("history", []):
        print(item)
