from ddgs import DDGS

from config.settings import settings


def search_web(query: str) -> list[dict]:
    """Search the web using DuckDuckGo.
    Returns a list of Citation dicts with title, URL, and body snippet.
    """
    citations = []
    try:
        ddgs = DDGS()
        results = ddgs.text(
            keywords=query,
            max_results=settings.web_max_results,
        )
        for r in results:
            citations.append({
                "source_type": "web",
                "title": r.get("title", "Untitled"),
                "url": r.get("href", ""),
                "snippet": r.get("body", "")[:500],
            })
    except Exception:
        pass

    return citations
