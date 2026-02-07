import httpx
import trafilatura


def read_webpage(url: str) -> str | None:
    """Fetch a web page and extract its main text content.

    Returns extracted text truncated to 2000 chars, or None on failure.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
    }

    try:
        resp = httpx.get(url, headers=headers, timeout=5, follow_redirects=True)
        resp.raise_for_status()
        text = trafilatura.extract(resp.text)
        if text:
            return text[:2000]
    except Exception:
        pass

    return None
