import asyncio
import json
import sys
import uuid

from langchain_core.messages import HumanMessage


async def run(query: str) -> str:
    from master_graph import agent

    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    result = await agent.ainvoke(
        {"messages": [HumanMessage(content=query)]},
        config=config,
    )
    return result["final_report"]


def main():
    query = sys.stdin.read().strip()
    if not query:
        print(json.dumps({"error": "Empty query received."}))
        sys.exit(1)

    report = asyncio.run(run(query))
    print(json.dumps({"final_report": report}))


if __name__ == "__main__":
    main()
