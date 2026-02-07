import httpx

from config.settings import settings


def search_github(query: str) -> list[dict]:
    """Search GitHub repositories matching the query.

    Returns a list of Citation dicts with source_type="github".
    Uses GITHUB_TOKEN env var for higher rate limits when available.
    """
    headers = {"Accept": "application/vnd.github+json"}
    if settings.github_token:
        headers["Authorization"] = f"Bearer {settings.github_token}"

    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": settings.github_max_results,
    }

    citations = []
    try:
        resp = httpx.get(
            "https://api.github.com/search/repositories",
            headers=headers,
            params=params,
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()

        for repo in data.get("items", []):
            language = repo.get("language") or "Unknown"
            stars = repo.get("stargazers_count", 0)
            description = repo.get("description") or "No description"

            citations.append({
                "source_type": "github",
                "title": repo["full_name"],
                "url": repo["html_url"],
                "snippet": (
                    f"{description} "
                    f"[{language}, {stars:,} stars]"
                )[:500],
            })
    except Exception:
        pass

    return citations
