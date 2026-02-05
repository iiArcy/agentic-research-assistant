from research_agent.state import AgentState
from research_agent.tools.registry import get_tool


def researcher_node(state: AgentState) -> dict:
    """Executes the current sub-task by calling the appropriate tool."""
    idx = state["current_task_index"]
    sub_tasks = state["sub_tasks"]

    if idx >= len(sub_tasks):
        return {"current_task_index": idx}

    task = sub_tasks[idx]
    new_findings = []
    new_errors = []

    try:
        tool_fn = get_tool(task["tool"])
        results = tool_fn(task["query"])
        new_findings = results

        sub_tasks = [dict(t) for t in sub_tasks]
        sub_tasks[idx]["status"] = "done"
        sub_tasks[idx]["findings"] = results
    except Exception as e:
        sub_tasks = [dict(t) for t in sub_tasks]
        sub_tasks[idx]["status"] = "failed"
        new_errors = [f"Task {idx} ({task['tool']}:{task['query']}): {e}"]

    return {
        "sub_tasks": sub_tasks,
        "current_task_index": idx + 1,
        "all_findings": new_findings,
        "errors": new_errors,
    }
