from langgraph.graph import StateGraph, START, END

from research_agent.nodes.memory_retriever import memory_retriever_node
from research_agent.nodes.planner import planner_node
from research_agent.nodes.researcher import researcher_node
from research_agent.nodes.synthesizer import synthesizer_node
from research_agent.nodes.memory_saver import memory_saver_node
from research_agent.state import AgentState


def should_continue(state: AgentState) -> str:
    """Route back to researcher if tasks remain, otherwise synthesize."""
    if state["current_task_index"] < len(state["sub_tasks"]):
        return "researcher"
    return "synthesizer"


def build_graph():
    """Construct and compile the research agent LangGraph."""
    graph = StateGraph(AgentState)

    graph.add_node("memory_retriever", memory_retriever_node)
    graph.add_node("planner", planner_node)
    graph.add_node("researcher", researcher_node)
    graph.add_node("synthesizer", synthesizer_node)
    graph.add_node("memory_saver", memory_saver_node)

    graph.add_edge(START, "memory_retriever")
    graph.add_edge("memory_retriever", "planner")
    graph.add_edge("planner", "researcher")
    graph.add_conditional_edges(
        "researcher",
        should_continue,
        {"researcher": "researcher", "synthesizer": "synthesizer"},
    )
    graph.add_edge("synthesizer", "memory_saver")
    graph.add_edge("memory_saver", END)

    return graph.compile()
