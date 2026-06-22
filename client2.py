import asyncio
import json

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, ToolMessage


# LLM
llm = ChatOllama(model="qwen3:8b")

# MCP Server Configuration
SERVERS = {
    "Calorie Tracker": {
        "command": r"C:\Users\yash\AppData\Local\Programs\Python\Python311\Scripts\uv.exe",
        "args": [
            "run",
            "--with",
            "fastmcp",
            "fastmcp",
            "run",
            r"C:\Users\yash\Downloads\calories_tracker\main.py",
        ],
        "transport": "stdio",
    }
}


async def main():

    # Connect MCP Server
    client = MultiServerMCPClient(SERVERS)

    # Load MCP Tools
    tools = await client.get_tools()

    # Tool Dictionary
    tool_map = {tool.name: tool for tool in tools}

    print("Available Tools:")
    for tool in tools:
        print("-", tool.name)

    # Bind tools to LLM
    llm_with_tools = llm.bind_tools(tools)

    query = "Add 700 calories"

    # First LLM Call
    response = await llm_with_tools.ainvoke(
        [HumanMessage(content=query)]
    )

    print("\nTool Calls:")
    print(response.tool_calls)

    # No tool required
    if not response.tool_calls:
        print(response.content)
        return

    # Execute Tool
    tool_call = response.tool_calls[0]

    tool_name = tool_call["name"]
    tool_args = tool_call["args"]
    tool_id = tool_call["id"]

    result = await tool_map[tool_name].ainvoke(tool_args)

    print("\nTool Result:")
    print(result)

    # Create Tool Message
    tool_message = ToolMessage(
        tool_call_id=tool_id,
        content=json.dumps(result)
    )

    # Final Response
    final_response = await llm_with_tools.ainvoke(
        [
            HumanMessage(content=query),
            response,
            tool_message
        ]
    )

    print("\nFinal Response:")
    print(final_response.content)


if __name__ == "__main__":
    asyncio.run(main())