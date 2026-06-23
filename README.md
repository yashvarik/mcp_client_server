# Calorie Tracker MCP Agent

## Overview

This project is an AI-powered Calorie Tracking Assistant built using the Model Context Protocol (MCP). The system enables a Large Language Model (LLM) to interact with custom tools for storing and retrieving calorie information through natural language commands.

The application uses FastMCP to expose tools, SQLite for data persistence, LangChain for tool orchestration, and Ollama-hosted LLMs for intelligent interaction.

---

## Features

* Add calorie entries using natural language.
* Store calorie information in a SQLite database.
* Retrieve stored calorie records.
* MCP-based tool integration.
* Local LLM execution using Ollama.
* Asynchronous tool calling with LangChain.
* Lightweight and easy to extend.

---

## Tech Stack

* Python
* FastMCP
* LangChain
* Ollama
* SQLite
* AsyncIO

---

## Project Structure

```text
calories_tracker/
│
├── main.py                 # FastMCP server
├── calorie_db.db           # SQLite database
├── client.py               # LangChain MCP client
├── requirements.txt
└── README.md
```

---

## How It Works

1. The user sends a natural language request.
2. The LLM determines whether a tool is required.
3. LangChain invokes the appropriate MCP tool.
4. FastMCP executes the tool logic.
5. SQLite stores or retrieves calorie data.
6. The result is returned to the LLM.
7. The LLM generates a user-friendly response.

---

## Example Queries

* Add 500 calories
* Add 700 calories
* Show my calorie records
* Retrieve all calorie entries

---

## Learning Outcomes

* Building MCP servers using FastMCP.
* Integrating MCP tools with LangChain.
* Tool calling with local LLMs.
* Working with SQLite databases.
* Developing AI-powered automation workflows.
* Implementing asynchronous Python applications.

---

## Future Improvements

* Daily calorie summaries.
* User authentication.
* Food item tracking.
* Nutrition analysis.
* Streamlit dashboard.
* Cloud deployment.

---

## Author

Developed as part of hands-on learning in AI Engineering, MCP Development, and Agentic AI systems.
