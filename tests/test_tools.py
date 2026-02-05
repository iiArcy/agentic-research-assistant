from research_agent.tools.arxiv_search import search_arxiv
from research_agent.tools.web_search import search_web
from research_agent.tools.registry import get_tool, TOOL_REGISTRY

import pytest


def test_arxiv_search_returns_citations():
    results = search_arxiv("LoRA fine-tuning")
    assert isinstance(results, list)
    assert len(results) > 0
    for r in results:
        assert r["source_type"] == "arxiv"
        assert "title" in r
        assert "url" in r
        assert "snippet" in r


def test_web_search_returns_list():
    """DuckDuckGo can be flaky; verify it returns a list without crashing."""
    results = search_web("python programming language")
    assert isinstance(results, list)
    for r in results:
        assert r["source_type"] == "web"
        assert "title" in r
        assert "url" in r
        assert "snippet" in r


def test_registry_has_tools():
    assert "arxiv" in TOOL_REGISTRY
    assert "web" in TOOL_REGISTRY


def test_get_tool_returns_callable():
    tool = get_tool("arxiv")
    assert callable(tool)


def test_get_tool_raises_on_unknown():
    with pytest.raises(KeyError, match="Unknown tool"):
        get_tool("nonexistent")
