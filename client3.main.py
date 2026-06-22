import json
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama.chat_models import ChatOllama
from langchain_core.messages import ToolMessage,HumanMessage
import asyncio
llm=ChatOllama(model='qwen3:8b')

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
    client=MultiServerMCPClient(SERVERS)
    tools=await client.get_tools()

    tool_map= {tool.name : tool for tool in tools}

    for tool in tools:
        print(tool.name)

    llm_with_tool=llm.bind_tools(tools)

    query='add 800 calories'

    response=await llm_with_tool.ainvoke([
        HumanMessage(content=query)
    ])

    tool_call = response.tool_calls[0]
    tool_name=tool_call['name']
    tool_args=tool_call['args']
    tool_id=tool_call['id']

    result=await tool_map[tool_name].ainvoke(tool_args)
    print(result)

    tool_message=ToolMessage(tool_call_id=tool_id,content=json.dumps(result))
    final_answer=await llm_with_tool.ainvoke([HumanMessage(content=query),response,tool_message])
    print(final_answer)


if __name__== "__main__":
    asyncio.run(main())