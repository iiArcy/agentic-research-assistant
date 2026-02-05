from research_agent.tools.arxiv_search import search_arxiv
from research_agent.tools.web_search import search_web

TOOL_REGISTRY: dict[str, callable] = {
    "arxiv": search_arxiv,
    "web": search_web,
}


def get_tool(name: str):
    """Look up a tool by name. Raises KeyError if not found."""
    if name not in TOOL_REGISTRY:
        raise KeyError(f"Unknown tool: {name}. Available: {list(TOOL_REGISTRY.keys())}")
    return TOOL_REGISTRY[name]
