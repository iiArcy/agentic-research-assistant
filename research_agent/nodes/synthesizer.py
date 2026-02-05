from research_agent.llm import get_llm
from research_agent.prompts import SYNTHESIZER_PROMPT
from research_agent.state import AgentState


def synthesizer_node(state: AgentState) -> dict:
    """Combines all findings into a cited markdown report."""
    llm = get_llm()

    findings_text = _format_findings(state["all_findings"])
    errors_text = "\n".join(state.get("errors", [])) or "None"

    chain = SYNTHESIZER_PROMPT | llm
    result = chain.invoke({
        "query": state["original_query"],
        "findings": findings_text,
        "errors": errors_text,
    })

    return {"final_report": result.content}


def _format_findings(findings: list[dict]) -> str:
    """Format citations into numbered text for the LLM context."""
    if not findings:
        return "No findings were retrieved."

    parts = []
    for i, f in enumerate(findings, 1):
        parts.append(
            f"[{i}] ({f['source_type']}) {f['title']}\n"
            f"    URL: {f['url']}\n"
            f"    Excerpt: {f['snippet']}\n"
        )
    return "\n".join(parts)
