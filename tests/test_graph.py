from research_agent.graph import build_graph


def test_graph_compiles():
    graph = build_graph()
    assert graph is not None


def test_graph_end_to_end():
    graph = build_graph()
    result = graph.invoke({
        "original_query": "What is LoRA?",
        "all_findings": [],
        "errors": [],
        "current_task_index": 0,
        "sub_tasks": [],
        "final_report": "",
    })

    assert result["final_report"]
    assert len(result["all_findings"]) > 0
    assert len(result["sub_tasks"]) > 0
    assert all(t["status"] in ("done", "failed") for t in result["sub_tasks"])
