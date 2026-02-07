from __future__ import annotations

import operator
from typing import Annotated, TypedDict


class Citation(TypedDict):
    """A single citation source."""
    source_type: str  # "arxiv" | "web" | "github" | "wikipedia" | "semantic_scholar" | "huggingface" | "youtube"
    title: str
    url: str
    snippet: str


class SubTask(TypedDict):
    """A single research sub-task."""
    id: int
    query: str
    tool: str  # "arxiv" | "web" | "github" | "wikipedia" | "semantic_scholar" | "huggingface" | "youtube"
    status: str  # "pending" | "done" | "failed"
    findings: list[Citation]


class AgentState(TypedDict):
    """Central state for the research agent graph."""
    original_query: str
    sub_tasks: list[SubTask]
    current_task_index: int
    all_findings: Annotated[list[Citation], operator.add]
    final_report: str
    errors: Annotated[list[str], operator.add]
    past_context: str
