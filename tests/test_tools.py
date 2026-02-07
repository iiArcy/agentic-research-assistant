from research_agent.tools.arxiv_search import search_arxiv
from research_agent.tools.web_search import search_web
from research_agent.tools.github_search import search_github
from research_agent.tools.wikipedia_search import search_wikipedia
from research_agent.tools.semantic_scholar_search import search_semantic_scholar
from research_agent.tools.huggingface_search import search_huggingface
from research_agent.tools.youtube_search import search_youtube
from research_agent.tools.web_reader import read_webpage
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


def test_github_search_returns_citations():
    results = search_github("langchain")
    assert isinstance(results, list)
    assert len(results) > 0
    for r in results:
        assert r["source_type"] == "github"
        assert "title" in r
        assert "url" in r
        assert "snippet" in r


def test_wikipedia_search_returns_citations():
    results = search_wikipedia("Python programming language")
    assert isinstance(results, list)
    assert len(results) > 0
    for r in results:
        assert r["source_type"] == "wikipedia"
        assert "title" in r
        assert "url" in r
        assert "snippet" in r


def test_semantic_scholar_search_returns_citations():
    results = search_semantic_scholar("transformer attention mechanism")
    assert isinstance(results, list)
    assert len(results) > 0
    for r in results:
        assert r["source_type"] == "semantic_scholar"
        assert "title" in r
        assert "url" in r
        assert "snippet" in r


def test_huggingface_search_returns_citations():
    results = search_huggingface("text-generation")
    assert isinstance(results, list)
    assert len(results) > 0
    for r in results:
        assert r["source_type"] == "huggingface"
        assert "title" in r
        assert "url" in r
        assert "snippet" in r


def test_youtube_search_returns_list():
    """YouTube/DuckDuckGo can be flaky; verify it returns a list without crashing."""
    results = search_youtube("machine learning tutorial")
    assert isinstance(results, list)
    for r in results:
        assert r["source_type"] == "youtube"
        assert "title" in r
        assert "url" in r
        assert "snippet" in r


def test_read_webpage_returns_content():
    content = read_webpage("https://en.wikipedia.org/wiki/Python_(programming_language)")
    assert content is not None
    assert len(content) > 100
    assert isinstance(content, str)


def test_registry_has_tools():
    assert "arxiv" in TOOL_REGISTRY
    assert "web" in TOOL_REGISTRY
    assert "github" in TOOL_REGISTRY
    assert "wikipedia" in TOOL_REGISTRY
    assert "semantic_scholar" in TOOL_REGISTRY
    assert "huggingface" in TOOL_REGISTRY
    assert "youtube" in TOOL_REGISTRY


def test_get_tool_returns_callable():
    tool = get_tool("arxiv")
    assert callable(tool)


def test_get_tool_raises_on_unknown():
    with pytest.raises(KeyError, match="Unknown tool"):
        get_tool("nonexistent")
