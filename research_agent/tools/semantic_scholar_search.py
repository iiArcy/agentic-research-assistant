import httpx

from config.settings import settings


def search_semantic_scholar(query: str) -> list[dict]:
    """Search Semantic Scholar for academic papers matching the query.

    Returns a list of Citation dicts with source_type="semantic_scholar".
    """
    headers = {}
    if settings.semantic_scholar_api_key:
        headers["x-api-key"] = settings.semantic_scholar_api_key

    params = {
        "query": query,
        "limit": settings.semantic_scholar_max_results,
        "fields": "title,abstract,citationCount,url,year",
    }

    citations = []
    try:
        resp = httpx.get(
            "https://api.semanticscholar.org/graph/v1/paper/search/bulk",
            headers=headers,
            params=params,
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()

        for paper in data.get("data", []):
            title = paper.get("title", "Untitled")
            abstract = paper.get("abstract") or ""
            year = paper.get("year") or "N/A"
            citation_count = paper.get("citationCount") or 0
            url = paper.get("url") or ""

            snippet = abstract[:400]
            snippet += f" [Year: {year}, Citations: {citation_count}]"

            citations.append({
                "source_type": "semantic_scholar",
                "title": title,
                "url": url,
                "snippet": snippet,
            })
    except Exception:
        pass

    return citations
