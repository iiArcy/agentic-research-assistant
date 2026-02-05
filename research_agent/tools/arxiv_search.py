import arxiv

from config.settings import settings


def search_arxiv(query: str) -> list[dict]:
    """Search arXiv for papers matching the query.
    Returns a list of Citation dicts with title, URL, and abstract snippet.
    """
    client = arxiv.Client(
        page_size=settings.arxiv_max_results,
        delay_seconds=3.0,
        num_retries=3,
    )
    search = arxiv.Search(
        query=query,
        max_results=settings.arxiv_max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )

    citations = []
    try:
        for result in client.results(search):
            citations.append({
                "source_type": "arxiv",
                "title": result.title,
                "url": result.entry_id,
                "snippet": result.summary[:500],
            })
    except Exception:
        pass

    return citations
