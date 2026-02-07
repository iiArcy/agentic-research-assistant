from mediawiki import MediaWiki, DisambiguationError

from config.settings import settings


def search_wikipedia(query: str) -> list[dict]:
    """Search Wikipedia for articles matching the query.

    Returns a list of Citation dicts with source_type="wikipedia".
    """
    wiki = MediaWiki(user_agent="AgenticResearchAssistant/1.0")

    citations = []
    try:
        titles = wiki.search(query, results=settings.wikipedia_max_results)
        for title in titles:
            try:
                page = wiki.page(title)
                citations.append({
                    "source_type": "wikipedia",
                    "title": page.title,
                    "url": page.url,
                    "snippet": page.summary[:500],
                })
            except DisambiguationError:
                continue
            except Exception:
                continue
    except Exception:
        pass

    return citations
