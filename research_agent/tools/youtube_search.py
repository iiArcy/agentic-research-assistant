import re

from ddgs import DDGS
from youtube_transcript_api import YouTubeTranscriptApi

from config.settings import settings


def _extract_video_id(url: str) -> str | None:
    """Extract YouTube video ID from a URL."""
    patterns = [
        r"(?:v=|/v/)([a-zA-Z0-9_-]{11})",
        r"youtu\.be/([a-zA-Z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def search_youtube(query: str) -> list[dict]:
    """Search YouTube videos and extract transcripts.

    Uses DuckDuckGo to discover videos, then fetches transcripts via
    youtube_transcript_api. Falls back to DuckDuckGo snippet if transcript
    is unavailable.

    Returns a list of Citation dicts with source_type="youtube".
    """
    citations = []
    try:
        ddgs = DDGS()
        results = ddgs.text(
            keywords=f"{query} site:youtube.com",
            max_results=settings.youtube_max_results,
        )

        ytt_api = YouTubeTranscriptApi()

        for r in results:
            url = r.get("href", "")
            title = r.get("title", "Untitled")
            fallback_snippet = r.get("body", "")[:500]

            video_id = _extract_video_id(url)
            if not video_id:
                continue

            snippet = fallback_snippet
            try:
                transcript = ytt_api.fetch(video_id)
                text = " ".join(seg.text for seg in transcript)
                if text:
                    snippet = text[:1500]
            except Exception:
                pass

            citations.append({
                "source_type": "youtube",
                "title": title,
                "url": url,
                "snippet": snippet,
            })
    except Exception:
        pass

    return citations
