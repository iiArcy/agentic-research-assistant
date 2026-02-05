from langchain_core.output_parsers import JsonOutputParser

from config.settings import settings
from research_agent.llm import get_llm
from research_agent.prompts import PLANNER_PROMPT
from research_agent.state import AgentState, SubTask


def planner_node(state: AgentState) -> dict:
    """Decomposes the user's query into 2-5 actionable sub-tasks."""
    llm = get_llm()
    chain = PLANNER_PROMPT | llm | JsonOutputParser()
    result = chain.invoke({"query": state["original_query"]})

    sub_tasks: list[SubTask] = []
    for i, task in enumerate(result["sub_tasks"][:settings.max_sub_tasks]):
        sub_tasks.append(
            SubTask(
                id=i,
                query=task["query"],
                tool=task["tool"],
                status="pending",
                findings=[],
            )
        )

    return {"sub_tasks": sub_tasks, "current_task_index": 0}
