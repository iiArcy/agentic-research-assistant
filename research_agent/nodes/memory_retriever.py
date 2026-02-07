from research_agent.memory import MemoryStore
from research_agent.state import AgentState


def memory_retriever_node(state: AgentState) -> dict:
    """Look up past research sessions relevant to the current query."""
    store = MemoryStore()
    results = store.search(state["original_query"])

    if not results:
        return {"past_context": ""}

    parts: list[str] = []
    for r in results:
        parts.append(
            f"- Previous query: \"{r['query']}\" (similarity: {r['similarity']})\n"
            f"  Summary: {r['report_summary'][:300]}"
        )

    return {"past_context": "\n".join(parts)}
