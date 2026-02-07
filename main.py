"""
Agentic Research Assistant - CLI Entry Point
Usage: python main.py "What are the latest fine-tuning techniques for LLMs?"
"""
import sys
import time

from research_agent.graph import build_graph


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py \"<your research question>\"")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    print(f"\nResearch question: {query}")
    print("=" * 60)

    graph = build_graph()
    start = time.time()

    result = graph.invoke({
        "original_query": query,
        "all_findings": [],
        "errors": [],
        "current_task_index": 0,
        "sub_tasks": [],
        "final_report": "",
        "past_context": "",
    })

    elapsed = time.time() - start

    print(result["final_report"])
    print(f"\n{'=' * 60}")
    print(f"Completed in {elapsed:.1f}s")

    if result.get("errors"):
        print(f"\n{len(result['errors'])} error(s) during research:")
        for e in result["errors"]:
            print(f"  - {e}")


if __name__ == "__main__":
    main()
