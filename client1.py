import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama.chat_models import ChatOllama
from langchain_core.messages import ToolMessage
import json
llm=ChatOllama(model='qwen3:8B')


SERVER = {
    "arith": {
      "command": "C:\\Users\\yash\\AppData\\Local\\Programs\\Python\\Python311\\Scripts\\uv.exe",
      "args": [
        "run",
        "--with",
        "fastmcp",
        "fastmcp",
        "run",
        "C:\\Users\\yash\\OneDrive\\Documents\\claude_project\\main.py"
      ],
      "env": {},
      "transport": "stdio",
      
    },
    
}

async def main():
    client=MultiServerMCPClient(SERVER)
    tools= await client.get_tools()
    
    name_tool={}
    for tool in tools:
        name_tool[tool.name] = tool
    
    
   
    llm_with_tools=llm.bind_tools(tools)
    prompt='what is 80 -20'
    response = await llm_with_tools.ainvoke(prompt)
    if not getattr(response,"tool_calls",None):
        print("\nLLM  Reply :",response.content)
        return
    tool_message =[]
    for tc in response.tool_calls:
        selected_tool=tc['name']
        selected_args=tc.get("args") or {}
        selected_id = tc['id']

    result= await name_tool[selected_tool].ainvoke(selected_args)
    
    tool_message.append(ToolMessage(tool_call_id=selected_id,content=json.dumps(result)))
    final_response=await llm_with_tools.ainvoke([prompt,response,tool_message])
    print(f"final response:{final_response.content}")

if __name__ == '__main__':
    asyncio.run(main())