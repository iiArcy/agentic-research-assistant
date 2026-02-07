from research_agent.tools.arxiv_search import search_arxiv
from research_agent.tools.web_search import search_web
from research_agent.tools.github_search import search_github
from research_agent.tools.wikipedia_search import search_wikipedia
from research_agent.tools.semantic_scholar_search import search_semantic_scholar
from research_agent.tools.huggingface_search import search_huggingface
from research_agent.tools.youtube_search import search_youtube

TOOL_REGISTRY: dict[str, callable] = {
    "arxiv": search_arxiv,
    "web": search_web,
    "github": search_github,
    "wikipedia": search_wikipedia,
    "semantic_scholar": search_semantic_scholar,
    "huggingface": search_huggingface,
    "youtube": search_youtube,
}


def get_tool(name: str):
    """Look up a tool by name. Raises KeyError if not found."""
    if name not in TOOL_REGISTRY:
        raise KeyError(f"Unknown tool: {name}. Available: {list(TOOL_REGISTRY.keys())}")
    return TOOL_REGISTRY[name]
