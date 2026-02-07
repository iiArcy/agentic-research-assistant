from research_agent.memory import MemoryStore
from research_agent.state import AgentState


def memory_saver_node(state: AgentState) -> dict:
    """Persist the current research session to long-term memory."""
    report = state.get("final_report", "")
    if not report:
        return {}

    store = MemoryStore()
    store.add(
        query=state["original_query"],
        findings=state.get("all_findings", []),
        report_summary=report[:1000],
    )
    return {}
