import json
from pathlib import Path

import pytest

from research_agent.memory import MemoryStore


@pytest.fixture
def tmp_memory(tmp_path):
    """Provide a MemoryStore backed by a temporary file."""
    return MemoryStore(path=tmp_path / "memory.json")


def test_add_and_len(tmp_memory):
    assert len(tmp_memory) == 0
    tmp_memory.add(
        query="What is LoRA?",
        findings=[{"title": "LoRA paper"}],
        report_summary="LoRA is a parameter-efficient fine-tuning method.",
    )
    assert len(tmp_memory) == 1


def test_persistence(tmp_path):
    path = tmp_path / "memory.json"
    store = MemoryStore(path=path)
    store.add(
        query="What is LoRA?",
        findings=[],
        report_summary="LoRA enables efficient fine-tuning.",
    )
    assert path.exists()

    # Reload from disk
    store2 = MemoryStore(path=path)
    assert len(store2) == 1


def test_search_returns_relevant(tmp_memory):
    tmp_memory.add(
        query="What is LoRA fine-tuning?",
        findings=[{"title": "LoRA paper"}],
        report_summary="LoRA is a low-rank adaptation method for fine-tuning LLMs.",
    )
    tmp_memory.add(
        query="How does Docker networking work?",
        findings=[{"title": "Docker docs"}],
        report_summary="Docker provides bridge, host, and overlay networking modes.",
    )

    results = tmp_memory.search("Compare LoRA with QLoRA")
    assert len(results) >= 1
    assert results[0]["query"] == "What is LoRA fine-tuning?"


def test_search_empty_store(tmp_memory):
    results = tmp_memory.search("anything")
    assert results == []


def test_search_respects_threshold(tmp_memory):
    tmp_memory.add(
        query="Python web frameworks",
        findings=[],
        report_summary="Django and Flask are popular Python web frameworks.",
    )
    # A completely unrelated query with high threshold should return nothing
    results = tmp_memory.search("quantum computing algorithms", threshold=0.9)
    assert results == []
