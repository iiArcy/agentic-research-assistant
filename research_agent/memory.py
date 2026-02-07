from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import numpy as np

from config.settings import settings

_MEMORY_DIR = Path.home() / ".agentic-research-assistant"
_MEMORY_FILE = _MEMORY_DIR / "memory.json"


class MemoryStore:
    """Persistent memory with semantic search over past research sessions.

    Stores query, findings summary, report excerpt, and embedding vectors.
    Uses sentence-transformers for encoding and numpy cosine similarity for
    retrieval.  The embedding model is loaded lazily on first write/search.
    """

    def __init__(self, path: Path = _MEMORY_FILE) -> None:
        self._path = path
        self._entries: list[dict[str, Any]] = []
        self._model = None
        self._load()

    # -- persistence --------------------------------------------------------

    def _load(self) -> None:
        if self._path.exists():
            with open(self._path, "r") as f:
                self._entries = json.load(f)

    def _save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._path, "w") as f:
            json.dump(self._entries, f, indent=2)

    # -- lazy model loading -------------------------------------------------

    def _get_model(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(settings.embedding_model)
        return self._model

    def _embed(self, text: str) -> list[float]:
        model = self._get_model()
        vec = model.encode(text, normalize_embeddings=True)
        return vec.tolist()

    # -- public API ---------------------------------------------------------

    def add(
        self,
        query: str,
        findings: list[dict],
        report_summary: str,
    ) -> None:
        """Persist a research session to memory."""
        text_to_embed = f"{query} {report_summary[:500]}"
        embedding = self._embed(text_to_embed)

        entry = {
            "query": query,
            "findings_count": len(findings),
            "report_summary": report_summary[:1000],
            "embedding": embedding,
            "timestamp": time.time(),
        }
        self._entries.append(entry)
        self._save()

    def search(self, query: str, top_k: int = 3, threshold: float = 0.35) -> list[dict]:
        """Find past sessions semantically similar to *query*.

        Returns up to *top_k* entries whose cosine similarity to the query
        exceeds *threshold*, sorted by descending similarity.
        """
        if not self._entries:
            return []

        query_vec = np.array(self._embed(query))

        scored: list[tuple[float, dict]] = []
        for entry in self._entries:
            entry_vec = np.array(entry["embedding"])
            similarity = float(np.dot(query_vec, entry_vec))
            if similarity >= threshold:
                scored.append((similarity, entry))

        scored.sort(key=lambda x: x[0], reverse=True)

        results = []
        for sim, entry in scored[:top_k]:
            results.append({
                "query": entry["query"],
                "report_summary": entry["report_summary"],
                "similarity": round(sim, 3),
            })
        return results

    def __len__(self) -> int:
        return len(self._entries)
