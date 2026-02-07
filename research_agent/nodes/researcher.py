from research_agent.state import AgentState
from research_agent.tools.registry import get_tool
from research_agent.tools.web_reader import read_webpage

_SKIP_ENRICHMENT = {"github"}


def _enrich_findings(results: list[dict]) -> None:
    """Enrich top 2 findings with full web page content."""
    for finding in results[:2]:
        if finding.get("source_type") in _SKIP_ENRICHMENT:
            continue
        try:
            content = read_webpage(finding["url"])
            if content:
                finding["snippet"] = content[:2000]
        except Exception:
            pass


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

        try:
            _enrich_findings(results)
        except Exception:
            pass

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
